"""
GO Markdown Explanation Service

LLM-based markdown report generation for GO enrichment results (Phase 2, markdown format).
Generates provenance-labeled explanations with [DATA], [INFERENCE], [EXTERNAL], [GO-HIERARCHY] tags.
"""
import copy
import csv
import json
import os
import re
from pathlib import Path
from typing import Any

import yaml
from cellsem_llm_client.agents.agent_connection import LiteLLMAgent
from cellsem_llm_client.schema.adapters import OpenAISchemaAdapter
from cellsem_llm_client.schema.manager import SchemaManager

# =============================================================================
# EnrichmentExplanation: schema-first model generated from JSON schema.
# Source of truth: schemas/enrichment_explanation.schema.json
# Fixed in cellsem_llm_client v2.1.1 — SchemaManager now handles nested arrays
# of objects correctly via recursive _json_type_to_python_type.
# =============================================================================
_schema_manager = SchemaManager()
_EXPLANATION_SCHEMA_PATH = (
    Path(__file__).parent.parent / "schemas" / "enrichment_explanation.schema.json"
)
_THEME_SCHEMA_PATH = (
    Path(__file__).parent.parent / "schemas" / "theme_explanation.schema.json"
)
EnrichmentExplanation = _schema_manager.get_pydantic_model(
    json.loads(_EXPLANATION_SCHEMA_PATH.read_text())
)

# Per-model output token defaults.  Add new models here as their ceilings become known.
_MODEL_MAX_TOKENS: dict[str, int] = {
    "gpt-5": 32000,
    # gpt-4o / gpt-4o-mini ceiling is 16,384 — covered by _DEFAULT_MAX_TOKENS
}
_DEFAULT_MAX_TOKENS = 16000


def _get_default_max_tokens(model: str) -> int:
    """Return a sensible max_tokens default for the given model name."""
    return _MODEL_MAX_TOKENS.get(model, _DEFAULT_MAX_TOKENS)


def _is_openai_model(model: str) -> bool:
    """Return True if *model* uses the OpenAI structured-output path."""
    return "gpt" in model.lower() or model.startswith("openai/")


# ---------------------------------------------------------------------------
# Per-theme synthesis helpers
# ---------------------------------------------------------------------------

def _collect_valid_sets(theme: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Return (sorted_valid_genes, sorted_valid_go_ids) for a theme."""
    anchor = theme.get("anchor_term", {})
    genes: set[str] = set(anchor.get("genes", []))
    go_ids: set[str] = {anchor.get("go_id", "")}
    for s in theme.get("specific_terms", []):
        genes.update(s.get("genes", []))
        gid = s.get("go_id", "")
        if gid:
            go_ids.add(gid)
    go_ids.discard("")
    return sorted(genes), sorted(go_ids)


def _inject_enums(
    schema: dict[str, Any],
    valid_genes: list[str],
    valid_go_ids: list[str],
) -> dict[str, Any]:
    """Inject gene/GO ID enum constraints into a theme explanation schema dict.

    Modifies the dict in-place and returns it for convenience.  The ``pattern``
    key is removed from go_id fields because it is redundant with ``enum`` and
    incompatible with OpenAI strict mode when both are present.
    """
    kg_props = schema["properties"]["key_genes"]["items"]["properties"]
    kg_props["gene"]["enum"] = valid_genes
    kg_props["go_id"]["enum"] = valid_go_ids
    kg_props["go_id"].pop("pattern", None)

    ki_props = schema["properties"]["key_insights"]["items"]["properties"]
    ki_props["go_id"]["enum"] = valid_go_ids
    ki_props["go_id"].pop("pattern", None)

    return schema


def _ensure_additional_properties_false(schema: dict[str, Any]) -> None:
    """Recursively set ``additionalProperties: false`` on all objects.

    OpenAI strict mode requires this on every object in the schema.
    """
    if not isinstance(schema, dict):
        return
    if schema.get("type") == "object" and "additionalProperties" not in schema:
        schema["additionalProperties"] = False
    for value in schema.values():
        if isinstance(value, dict):
            _ensure_additional_properties_false(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _ensure_additional_properties_false(item)


def _build_theme_schema(theme: dict[str, Any]) -> dict[str, Any]:
    """Load the base theme schema and inject enum constraints for *theme*."""
    schema = json.loads(_THEME_SCHEMA_PATH.read_text())
    valid_genes, valid_go_ids = _collect_valid_sets(theme)
    _inject_enums(schema, valid_genes, valid_go_ids)
    _ensure_additional_properties_false(schema)
    return schema


def _call_per_theme(
    adapter: OpenAISchemaAdapter,
    model: str,
    system_prompt: str,
    theme_context: str,
    theme_schema: dict[str, Any],
    max_tokens: int = 2000,
) -> dict[str, Any] | None:
    """Make a single per-theme LLM call and return the parsed JSON, or None on failure."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Explain this enrichment theme:\n\n{theme_context}"},
    ]
    try:
        raw = adapter.apply_schema(
            messages=messages,
            schema_dict=theme_schema,
            model=model,
            max_tokens=max_tokens,
        )
        content = raw.choices[0].message.content
        result = json.loads(content)
        # Extract token usage
        usage = raw.usage
        tokens_in = usage.prompt_tokens if usage else 0
        tokens_out = usage.completion_tokens if usage else 0
        result["_usage"] = {"input_tokens": tokens_in, "output_tokens": tokens_out}
        return result
    except Exception as e:
        print(f"    ✗ LLM call failed: {e}")
        return None


def _format_single_theme_context(
    theme_index: int,
    theme: dict[str, Any],
    hub_genes: dict[str, Any],
    snippet_evidence: dict[int, list[dict[str, Any]]] | None = None,
    gaf_pmids: dict[int, list[dict[str, Any]]] | None = None,
    gaf_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    co_annotation_snippets: dict[int, dict[str, list[dict[str, Any]]]] | None = None,
    gene_narratives: dict[str, Any] | None = None,
    paper_abstracts: dict[int, list[dict[str, Any]]] | None = None,
) -> str:
    """Format a single theme's enrichment data + evidence for the LLM prompt.

    This mirrors the per-theme block inside ``_format_enrichment_for_llm`` but
    returns just the context for one theme (no study overview or hub genes).
    """
    i = theme_index
    anchor = theme.get("anchor_term", {})
    specific_terms = theme.get("specific_terms", [])
    confidence = theme.get("anchor_confidence", "")

    lines: list[str] = []
    lines.append(f"## Theme: {anchor.get('name', 'Unknown')} ({anchor.get('go_id', '')})")
    lines.append(f"- Namespace: {anchor.get('namespace', '')}")
    lines.append(f"- FDR: {anchor.get('fdr', 0):.2e}")
    lines.append(f"- Fold enrichment: {anchor.get('fold_enrichment', 0):.1f}x")
    lines.append(f"- Confidence: {confidence}")
    lines.append(f"- Genes ({len(anchor.get('genes', []))}): {', '.join(sorted(anchor.get('genes', [])))}")
    lines.append("")

    if specific_terms:
        lines.append(f"### Specific Terms ({len(specific_terms)} nested)")
        for s in specific_terms[:5]:
            lines.append(
                f"  - {s.get('name', '')} ({s.get('go_id', '')}): "
                f"FDR={s.get('fdr', 0):.2e}, "
                f"{len(s.get('genes', []))} genes: "
                f"{', '.join(sorted(s.get('genes', []))[:8])}"
            )
        if len(specific_terms) > 5:
            lines.append(f"  - ... and {len(specific_terms) - 5} more")
        lines.append("")

    ranked = rank_genes_for_theme(theme, hub_genes)
    if ranked:
        lines.append("### Candidate Key Genes (ranked by theme-specificity, select 2-5):")
        for rank_num, entry in enumerate(ranked, 1):
            specific_label = (
                f"in {entry['in_specific_terms']} specific term(s)"
                if entry["in_specific_terms"] > 0
                else "anchor-only"
            )
            lines.append(
                f"  {rank_num}. {entry['gene']}  "
                f"[{specific_label}, appears in {entry['n_themes']} theme(s), score: {entry['score']:.2f}]"
            )
        lines.append("")

    # ASTA snippet evidence
    has_snippets = bool(snippet_evidence and i in snippet_evidence and snippet_evidence[i])
    if has_snippets:
        lines.append("### Available Evidence Snippets (full-text passages, prefer these for citations):")
        lines.append("Cite the PMID inline: '[EXTERNAL] FOXO3 suppresses migration PMID:19188590.'")
        for snippet in snippet_evidence[i]:  # type: ignore[index]
            pmid = snippet.get("pmid", "")
            title = snippet.get("title", "")
            snippet_text = snippet.get("snippet_text", "")
            pmid_label = f"PMID:{pmid}" if pmid else snippet.get("paperId", "")
            lines.append(f"[{pmid_label}] {title}")
            if snippet_text:
                preview = snippet_text[:600] + "..." if len(snippet_text) > 600 else snippet_text
                lines.append(f"Evidence: {preview}")
            lines.append("")

    # Co-annotation evidence
    has_co_annot = bool(co_annotation_snippets and i in co_annotation_snippets and co_annotation_snippets[i])
    if has_co_annot:
        lines.append("### Co-Annotation Evidence:")
        for gene, gene_snippets in co_annotation_snippets[i].items():  # type: ignore[index]
            if not gene_snippets:
                continue
            lines.append(f"**{gene}** (multi-process co-annotation)")
            for snippet in gene_snippets:
                pmid = snippet.get("pmid", "")
                title = snippet.get("title", "")
                snippet_text = snippet.get("snippet_text", "")
                pmid_label = f"PMID:{pmid}" if pmid else snippet.get("paperId", "")
                lines.append(f"[{pmid_label}] {title}")
                if snippet_text:
                    preview = snippet_text[:600] + "..." if len(snippet_text) > 600 else snippet_text
                    lines.append(f"Evidence: {preview}")
                lines.append("")

    # Gene narratives from Phase 1c
    theme_gene_narrs = (gene_narratives or {}).get("theme_genes", {}).get(i, {})
    co_annot_narrs = (gene_narratives or {}).get("co_annotations", {}).get(i, {})
    all_theme_narrs = {**theme_gene_narrs, **co_annot_narrs}
    if all_theme_narrs:
        lines.append("### Gene Evidence Narratives:")
        for gene_name, narr in all_theme_narrs.items():
            lines.append(f"- **{gene_name}**: {narr}")
        lines.append("")

    # GAF citations
    if gaf_pmids and i in gaf_pmids and gaf_pmids[i]:
        lines.append("### Available GAF Citations (curated gene→GO annotations):")
        gaf_entry_by_pmid: dict[str, dict[str, Any]] = {
            e.get("pmid", ""): e for e in gaf_pmids[i]
        }
        has_abstracts = bool(gaf_abstracts and i in gaf_abstracts and gaf_abstracts[i])
        if has_abstracts:
            for paper in gaf_abstracts[i]:  # type: ignore[index]
                pmid = paper.get("pmid", "")
                title = paper.get("title", "")
                abstract = paper.get("abstract", "")
                lines.append(f"[PMID:{pmid}] {title}")
                lines.append(_format_gene_go_annotations(gaf_entry_by_pmid.get(pmid, {})))
                if abstract:
                    preview = abstract[:400] + "..." if len(abstract) > 400 else abstract
                    lines.append(f"Abstract: {preview}")
                lines.append("")
        else:
            for entry in gaf_pmids[i]:
                pmid = entry.get("pmid", "")
                lines.append(f"- PMID:{pmid}")
                lines.append(f"  {_format_gene_go_annotations(entry)}")
        lines.append("")

    # Deprecated paper_abstracts fallback
    elif paper_abstracts and i in paper_abstracts and paper_abstracts[i]:
        lines.append("### Available Literature:")
        for paper in paper_abstracts[i]:
            pmid = paper.get("pmid", "")
            title = paper.get("title", "No title")
            abstract = paper.get("abstract", "")
            lines.append(f"[PMID:{pmid}] {title}")
            if abstract:
                preview = abstract[:400] + "..." if len(abstract) > 400 else abstract
                lines.append(f"Abstract: {preview}")
            lines.append("")

    return "\n".join(lines)


def _run_per_theme_synthesis(
    enrichment_output: dict[str, Any],
    model: str,
    api_key: str | None,
    temperature: float,
    max_tokens: int,
    prompt_config: dict[str, Any],
    snippet_evidence: dict[int, list[dict[str, Any]]] | None = None,
    gaf_pmids: dict[int, list[dict[str, Any]]] | None = None,
    gaf_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    co_annotation_snippets: dict[int, dict[str, list[dict[str, Any]]]] | None = None,
    gene_narratives: dict[str, Any] | None = None,
    paper_abstracts: dict[int, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """Run per-theme LLM synthesis with enum-constrained schemas.

    Each theme gets its own LLM call with a dynamically built JSON schema
    that enum-constrains gene and GO ID fields.  Results are assembled into
    the same ``explanation`` dict shape that the single-call path produces.

    Returns:
        An explanation dict compatible with ``render_explanation_to_markdown``.
    """
    themes = enrichment_output.get("themes", [])[:30]
    hub_genes = enrichment_output.get("hub_genes", {})
    system_prompt = prompt_config["system_prompt"]
    adapter = OpenAISchemaAdapter()

    # Per-theme max_tokens: each theme needs far fewer tokens than the full call
    per_theme_max = min(2000, max_tokens)

    theme_explanations: list[dict[str, Any]] = []
    total_in = 0
    total_out = 0

    for i, theme in enumerate(themes):
        anchor = theme.get("anchor_term", {})
        print(f"  [{i + 1}/{len(themes)}] {anchor.get('name', '?')} ...", end=" ", flush=True)

        theme_schema = _build_theme_schema(theme)
        theme_context = _format_single_theme_context(
            theme_index=i,
            theme=theme,
            hub_genes=hub_genes,
            snippet_evidence=snippet_evidence,
            gaf_pmids=gaf_pmids,
            gaf_abstracts=gaf_abstracts,
            co_annotation_snippets=co_annotation_snippets,
            gene_narratives=gene_narratives,
            paper_abstracts=paper_abstracts,
        )

        result = _call_per_theme(
            adapter=adapter,
            model=model,
            system_prompt=system_prompt,
            theme_context=theme_context,
            theme_schema=theme_schema,
            max_tokens=per_theme_max,
        )

        if result is not None:
            usage = result.pop("_usage", {})
            total_in += usage.get("input_tokens", 0)
            total_out += usage.get("output_tokens", 0)
            result["theme_index"] = i
            theme_explanations.append(result)
            print("✓")
        else:
            print("✗ (will use data-only stub)")

    print(f"\n  Per-theme synthesis: {len(theme_explanations)}/{len(themes)} themes explained")
    print(f"  Total tokens: {total_in:,} in / {total_out:,} out")

    # --- Summary call: hub_genes + overall_summary ---
    print("\n  Generating hub genes and overall summary...")
    summary_explanation = _run_summary_call(
        enrichment_output=enrichment_output,
        theme_explanations=theme_explanations,
        model=model,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        prompt_config=prompt_config,
        gene_narratives=gene_narratives,
    )

    # Assemble into the standard explanation dict
    explanation: dict[str, Any] = {
        "themes": theme_explanations,
        "hub_genes": summary_explanation.get("hub_genes", []),
        "overall_summary": summary_explanation.get("overall_summary", []),
    }
    return explanation


def _run_summary_call(
    enrichment_output: dict[str, Any],
    theme_explanations: list[dict[str, Any]],
    model: str,
    api_key: str | None,
    temperature: float,
    max_tokens: int,
    prompt_config: dict[str, Any],
    gene_narratives: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate hub_genes + overall_summary via a single LLM call.

    Uses the existing EnrichmentExplanation schema (full) but provides a
    context that focuses on hub genes and theme summaries rather than
    per-theme detail (that's already done).
    """
    hub_genes = enrichment_output.get("hub_genes", {})
    themes = enrichment_output.get("themes", [])[:30]
    metadata = enrichment_output.get("metadata", {})

    lines: list[str] = []
    lines.append("# Task: Generate hub gene explanations and overall summary")
    lines.append("")
    lines.append("The per-theme explanations have already been generated.")
    lines.append("Your job is to produce ONLY the hub_genes and overall_summary sections.")
    lines.append("For the themes array, return an empty array [].")
    lines.append("")
    lines.append(f"# Study: {metadata.get('species', 'unknown')} — "
                 f"{metadata.get('input_genes_count', '?')} input genes, "
                 f"{len(themes)} themes")
    lines.append("")

    # Theme summaries (so the LLM can write a coherent overall narrative)
    lines.append("# Theme Summaries")
    for exp in theme_explanations:
        idx = exp.get("theme_index", -1)
        if 0 <= idx < len(themes):
            anchor = themes[idx].get("anchor_term", {})
            lines.append(f"- Theme {idx + 1}: {anchor.get('name', '?')} "
                         f"({anchor.get('go_id', '')}) — "
                         f"{len(anchor.get('genes', []))} genes, "
                         f"FDR {anchor.get('fdr', 0):.2e}")
    lines.append("")

    # Hub genes detail
    if hub_genes:
        lines.append("# Hub Genes (appearing in 3+ themes)")
        hub_sorted = sorted(
            hub_genes.items(), key=lambda x: x[1].get("theme_count", 0), reverse=True
        )[:20]
        for gene, data in hub_sorted:
            theme_count = data.get("theme_count", 0)
            theme_names = data.get("themes", [])[:5]
            lines.append(f"## {gene} ({theme_count} themes): {', '.join(theme_names)}")
            hub_narratives = (gene_narratives or {}).get("hub_genes", {})
            if gene in hub_narratives:
                lines.append(f"  Mechanistic narrative: {hub_narratives[gene]}")
        lines.append("")

    context = "\n".join(lines)
    system_prompt = prompt_config["system_prompt"]
    user_prompt = prompt_config["user_prompt"].format(enrichment_data=context)

    agent = LiteLLMAgent(
        model=model,
        api_key=api_key or _get_api_key_for_model(model),
        max_tokens=max_tokens,
    )

    try:
        result = agent.query_unified(
            message=user_prompt,
            system_message=system_prompt,
            schema=EnrichmentExplanation,
            track_usage=True,
        )
        if result.model is not None:
            summary = result.model.model_dump()
            if result.usage:
                print(f"  Summary call: {result.usage.input_tokens:,} in / "
                      f"{result.usage.output_tokens:,} out")
            return summary
    except Exception as e:
        print(f"  ⚠ Summary call failed: {e}")

    # Fallback: empty summary
    return {"hub_genes": [], "overall_summary": ["Analysis complete. See individual themes above."]}


def generate_markdown_explanation(
    enrichment_output: dict[str, Any],
    model: str = "gpt-4o",
    api_key: str | None = None,
    temperature: float = 0.1,
    max_tokens: int | None = None,  # None → auto-derived per model via _get_default_max_tokens
    paper_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    gaf_pmids: dict[int, list[dict[str, Any]]] | None = None,
    gaf_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    hub_gene_abstracts: dict[str, list[dict[str, Any]]] | None = None,
    snippet_evidence: dict[int, list[dict[str, Any]]] | None = None,
    hub_gene_snippets: dict[str, list[dict[str, Any]]] | None = None,
    co_annotation_snippets: dict[int, dict[str, list[dict[str, Any]]]] | None = None,
    cross_theme_snippets: dict[str, list[dict[str, Any]]] | None = None,
    gene_narratives: dict[str, Any] | None = None,
    max_correction_retries: int = 2,
    csv_filename: str | None = None,
) -> str:
    """
    Generate provenance-labeled markdown report explaining GO enrichment results using LLM.

    The LLM generates a markdown report with provenance tags:
    - [DATA]: Direct observations from enrichment
    - [GO-HIERARCHY]: Facts from GO parent-child structure
    - [INFERENCE]: Logical deductions from co-annotation patterns
    - [EXTERNAL]: Claims requiring literature support

    Args:
        enrichment_output: Phase 1 output (from run_go_enrichment)
            Must contain: enrichment_leaves, themes, hub_genes, metadata
        model: LLM model identifier. Examples:
            - OpenAI: "gpt-4o", "gpt-4o-mini"
            - Anthropic: "claude-sonnet-4-20250514"
        api_key: API key for LLM provider (if None, uses env vars)
        temperature: LLM temperature (default: 0.1 for consistency)
        max_tokens: Maximum tokens for LLM response
        paper_abstracts: Deprecated. Optional dict mapping theme index to list of
            paper dicts. Use gaf_pmids + hub_gene_abstracts instead.
        gaf_pmids: Optional dict mapping theme index to list of curated GAF PMID
            dicts ({pmid, genes_covered}). Injected per theme as citation anchors.
        hub_gene_abstracts: Optional dict mapping gene symbol to list of paper
            dicts ({pmid, title, abstract, authors, year}). Injected into hub gene
            section so LLM can ground cross-theme coordination claims.
        snippet_evidence: Optional dict mapping theme index to ASTA snippet dicts.
            Preferred over gaf_abstracts when available (body-text evidence).
        hub_gene_snippets: Optional dict mapping gene symbol to ASTA snippet dicts.
            Preferred over hub_gene_abstracts when available.

    Returns:
        Markdown-formatted explanation string with provenance tags

    Raises:
        FileNotFoundError: If prompt file not found
        ValueError: If input is invalid or API key missing
        Exception: If LLM call fails

    Example:
        >>> result = run_go_enrichment(["TP53", "BRCA1"], "human")
        >>> markdown = generate_markdown_explanation(
        ...     enrichment_output=result,
        ...     model="gpt-4o"
        ... )
        >>> print(markdown)
    """
    # Resolve max_tokens: explicit value takes precedence; otherwise derive from model
    if max_tokens is None:
        max_tokens = _get_default_max_tokens(model)

    # Validate input
    if not enrichment_output:
        raise ValueError("enrichment_output cannot be empty")

    if "metadata" not in enrichment_output:
        raise ValueError("enrichment_output must have 'metadata' key")

    # Check for new format (themes) or legacy format (clusters)
    has_themes = "themes" in enrichment_output
    has_leaves = "enrichment_leaves" in enrichment_output

    if not has_themes and not has_leaves:
        raise ValueError("enrichment_output must have 'themes' or 'enrichment_leaves' keys")

    themes = enrichment_output.get("themes", [])
    enrichment_leaves = enrichment_output.get("enrichment_leaves", [])

    if not themes and not enrichment_leaves:
        # No enrichment - return minimal explanation
        return _empty_markdown_explanation(enrichment_output, model)

    print("=" * 80)
    print("GO Markdown Explanation Generation - Phase 2")
    print("=" * 80)

    # Load prompt configuration
    print("\n[1/4] Loading prompt configuration...")
    prompt_config = _load_prompt("go_explanation.prompt.yaml")
    system_prompt = prompt_config["system_prompt"]
    user_prompt_template = prompt_config["user_prompt"]

    # Get API key
    if api_key is None:
        api_key = _get_api_key_for_model(model)

    print(f"  Model: {model}")
    print(f"  Temperature: {temperature}")
    print(f"  Max tokens: {max_tokens}")
    print(f"  Output format: Structured JSON → programmatic markdown render")

    print(f"  Themes to explain: {len(themes)}")
    print(f"  Enrichment leaves: {len(enrichment_leaves)}")
    print(f"  Hub genes: {len(enrichment_output.get('hub_genes', {}))}")

    # -------------------------------------------------------------------
    # Branch: per-theme synthesis (OpenAI) vs single-call (other providers)
    # -------------------------------------------------------------------
    use_per_theme = _is_openai_model(model)

    if use_per_theme:
        print(f"\n[2/4] Per-theme synthesis with enum-constrained schemas...")
        explanation = _run_per_theme_synthesis(
            enrichment_output=enrichment_output,
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            prompt_config=prompt_config,
            snippet_evidence=snippet_evidence,
            gaf_pmids=gaf_pmids,
            gaf_abstracts=gaf_abstracts,
            co_annotation_snippets=co_annotation_snippets,
            gene_narratives=gene_narratives,
            paper_abstracts=paper_abstracts,
        )
    else:
        # Legacy single-call path (non-OpenAI models)
        print("\n[2/4] Formatting enrichment data for LLM...")
        enrichment_context = _format_enrichment_for_llm(
            enrichment_output,
            paper_abstracts=paper_abstracts,
            gaf_pmids=gaf_pmids,
            gaf_abstracts=gaf_abstracts,
            hub_gene_abstracts=hub_gene_abstracts,
            snippet_evidence=snippet_evidence,
            hub_gene_snippets=hub_gene_snippets,
            co_annotation_snippets=co_annotation_snippets,
            cross_theme_snippets=cross_theme_snippets,
            gene_narratives=gene_narratives,
        )
        user_prompt = user_prompt_template.format(enrichment_data=enrichment_context)
        print(f"  Context size: {len(enrichment_context)} characters")

        print("\n[3/4] Calling LLM for structured explanation generation...")
        agent = LiteLLMAgent(model=model, api_key=api_key, max_tokens=max_tokens)

        try:
            result = agent.query_unified(
                message=user_prompt,
                system_message=system_prompt,
                schema=EnrichmentExplanation,
                track_usage=True,
            )

            print(f"  LLM call successful")
            if result.usage:
                print(f"  Input tokens: {result.usage.input_tokens:,}")
                print(f"  Output tokens: {result.usage.output_tokens:,}")
                if result.usage.estimated_cost_usd:
                    print(f"  Estimated cost: ${result.usage.estimated_cost_usd:.4f} USD")

        except Exception as e:
            print(f"  ❌ LLM call failed: {e}")
            raise

        if result.model is None:
            raise RuntimeError("LLM response validation failed — no model instance returned")

        explanation = result.model.model_dump()

    # Validate post-generation (warn on violations, do not crash)
    print("\n[4/4] Validating and rendering...")

    # Build PMID whitelist from all literature context
    pmid_whitelist = build_pmid_whitelist(
        gaf_pmids=gaf_pmids,
        gaf_abstracts=gaf_abstracts,
        hub_gene_abstracts=hub_gene_abstracts,
        snippet_evidence=snippet_evidence,
        hub_gene_snippets=hub_gene_snippets,
        co_annotation_snippets=co_annotation_snippets,
        cross_theme_snippets=cross_theme_snippets,
        paper_abstracts=paper_abstracts,
        gene_narratives=gene_narratives,
    )
    if pmid_whitelist:
        print(f"  PMID whitelist: {len(pmid_whitelist)} unique PMIDs from literature context")

    # Deterministic claim_type correction (always, free)
    claim_corrections = correct_claim_types(explanation, pmid_whitelist)
    for c in claim_corrections:
        print(f"  ✓ claim_type corrected: {c}")

    # Gene/GO validation (existing)
    validation_warnings = validate_explanation_json(explanation, enrichment_output)
    for w in validation_warnings:
        print(f"  ⚠ {w}")

    # PMID validation
    pmid_warnings, hallucinated_by_loc = validate_pmids_in_explanation(
        explanation, pmid_whitelist
    )
    for w in pmid_warnings:
        print(f"  ⚠ {w}")
    validation_warnings.extend(pmid_warnings)

    # LLM correction loop (bounded) — needs an agent for correction calls
    if api_key is None:
        api_key = _get_api_key_for_model(model)
    correction_agent = LiteLLMAgent(model=model, api_key=api_key, max_tokens=max_tokens)

    retries = 0
    total_correction_cost = 0.0
    while hallucinated_by_loc and retries < max_correction_retries:
        retries += 1
        n_bad = sum(len(v) for v in hallucinated_by_loc.values())
        print(f"\n  Correction attempt {retries}/{max_correction_retries} "
              f"({n_bad} hallucinated PMID(s))...")
        try:
            sys_p, usr_p = _build_correction_prompt(
                explanation, pmid_warnings, pmid_whitelist
            )
            correction_result = correction_agent.query_unified(
                message=usr_p,
                system_message=sys_p,
                schema=EnrichmentExplanation,
                track_usage=True,
            )
            if correction_result.model is not None:
                explanation = correction_result.model.model_dump()
                if correction_result.usage and correction_result.usage.estimated_cost_usd:
                    total_correction_cost += correction_result.usage.estimated_cost_usd
                # Re-apply deterministic corrections and re-validate
                correct_claim_types(explanation, pmid_whitelist)
                pmid_warnings, hallucinated_by_loc = validate_pmids_in_explanation(
                    explanation, pmid_whitelist
                )
                if hallucinated_by_loc:
                    n_remaining = sum(len(v) for v in hallucinated_by_loc.values())
                    print(f"  {n_remaining} hallucinated PMID(s) remain after correction")
                else:
                    print(f"  ✓ All PMIDs now grounded")
            else:
                print(f"  Correction attempt {retries} failed (no model returned)")
                break
        except Exception as e:
            print(f"  Correction attempt {retries} failed: {e}")
            break

    if total_correction_cost > 0:
        print(f"  Correction loop cost: ${total_correction_cost:.4f} USD")

    # Final strip of any remaining hallucinated PMIDs
    if hallucinated_by_loc:
        stripped = strip_hallucinated_pmids(explanation, hallucinated_by_loc)
        if stripped:
            print(f"  ⚠ Stripped {stripped} unresolvable hallucinated PMID(s) from output")
            # Re-check claim_types after stripping
            correct_claim_types(explanation, pmid_whitelist)

    # Narrative gene hallucination check: extract backtick-quoted genes and validate
    narrative_findings = validate_narrative_genes(explanation, enrichment_output)
    if narrative_findings:
        print(f"\n  Narrative gene hallucination check:")
        for nf in narrative_findings:
            print(f"    ⚠ {nf['location']}: `{nf['gene']}` not in valid gene set")
            print(f"      Sentence: {nf['sentence'][:120]}...")
        n_stripped = strip_hallucinated_gene_sentences(explanation, narrative_findings)
        if n_stripped:
            print(f"    Stripped {n_stripped} sentence(s) containing hallucinated genes")
    else:
        print("  ✓ No hallucinated genes found in narrative text")

    # Build per-theme set of flagged theme indices (those with content mismatches)
    flagged_themes: set[int] = set()
    for w in validation_warnings:
        # Warning format: "Theme {idx}: ..."
        m = re.match(r"Theme (\d+):", w)
        if m:
            flagged_themes.add(int(m.group(1)))
    if flagged_themes:
        print(f"  ⚠ {len(flagged_themes)} theme(s) with content mismatches will use data-only rendering: {sorted(flagged_themes)}")

    # Warn if LLM skipped themes — add missing ones to flagged_themes for data-only stubs
    n_input_themes = len(enrichment_output.get("themes", []))
    covered_indices = {
        t["theme_index"]
        for t in explanation.get("themes", [])
        if isinstance(t.get("theme_index"), int)
    }
    missing_indices = set(range(n_input_themes)) - covered_indices
    if missing_indices:
        print(
            f"  ⚠ LLM only covered {len(covered_indices)}/{n_input_themes} themes"
            f" — {len(missing_indices)} theme(s) will use data-only stubs: {sorted(missing_indices)[:10]}"
            + ("..." if len(missing_indices) > 10 else "")
        )
        flagged_themes.update(missing_indices)

    # Render structured JSON → markdown programmatically
    markdown_output = render_explanation_to_markdown(explanation, enrichment_output, flagged_themes=flagged_themes, csv_filename=csv_filename)

    # Add hyperlinks for any bare GO IDs remaining in narrative text
    markdown_output = _add_go_term_hyperlinks(markdown_output, enrichment_output)

    # Add hyperlinks to inline PMID citations
    markdown_output = _add_pmid_hyperlinks(markdown_output)

    # Count provenance tags
    _count_provenance_tags(markdown_output)

    print("\n" + "=" * 80)
    print(f"Markdown explanation generation complete!")
    print(f"  Output length: {len(markdown_output)} characters")
    print("=" * 80)

    return markdown_output


def _load_prompt(prompt_file: str) -> dict[str, Any]:
    """
    Load co-located prompt YAML file.

    Args:
        prompt_file: Name of prompt file (e.g., "go_explanation.prompt.yaml")

    Returns:
        Dictionary with system_prompt, user_prompt, presets

    Raises:
        FileNotFoundError: If prompt file not found
    """
    prompt_path = Path(__file__).parent / prompt_file
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path) as f:
        return yaml.safe_load(f)


def _get_api_key_for_model(model: str) -> str:
    """
    Get appropriate API key for model.

    Args:
        model: Model identifier

    Returns:
        API key string

    Raises:
        ValueError: If required API key not found
    """
    if model.startswith("gpt") or model.startswith("o1"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return api_key
    elif model.startswith("claude"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        return api_key
    else:
        # Try OpenAI first, then Anthropic
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable."
            )
        return api_key


def _format_gene_go_annotations(entry: dict[str, Any]) -> str:
    """Format a GAF PMID entry's gene→GO annotations for LLM context.

    Uses gene_go_named (resolved names) if available, falls back to
    gene_go_map (raw GO IDs), then genes_covered (no GO info).

    Examples:
        "Annotates: FOXO3→negative regulation of apoptotic process [GO:0043066], KANK1→cell migration [GO:0016477]"
        "Annotates: FOXO3→GO:0043066, KANK1→GO:0016477"
        "Covers: FOXO3, KANK1"
    """
    gene_go_named = entry.get("gene_go_named", {})
    gene_go_map = entry.get("gene_go_map", {})
    genes_covered = entry.get("genes_covered", [])

    if gene_go_named:
        parts = []
        for gene, term_names in sorted(gene_go_named.items()):
            for name in term_names:
                parts.append(f"{gene}→{name}")
        return f"Annotates: {', '.join(parts)}"

    if gene_go_map:
        parts = []
        for gene, go_ids in sorted(gene_go_map.items()):
            for gid in go_ids:
                parts.append(f"{gene}→{gid}")
        return f"Annotates: {', '.join(parts)}"

    # Fallback: no GO term info
    genes_str = ", ".join(genes_covered[:6])
    if len(genes_covered) > 6:
        genes_str += f" +{len(genes_covered) - 6} more"
    return f"Covers: {genes_str}"


def _build_cross_theme_index(
    gaf_pmids: dict[int, list[dict[str, Any]]] | None,
    themes: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Build per-gene index of GAF PMIDs that span 2+ themes.

    Returns:
        {gene: [{pmid, themes: [{index, name}], annotations: [{go_term_named}]}]}
        Only includes genes where at least one PMID spans 2+ themes.
    """
    if not gaf_pmids:
        return {}

    # pmid → {gene → {theme_idx → [go_term_named]}}
    pmid_gene_themes: dict[str, dict[str, dict[int, list[str]]]] = {}

    for theme_idx, entries in gaf_pmids.items():
        for entry in entries:
            pmid = entry.get("pmid", "")
            if not pmid:
                continue
            gene_go_named = entry.get("gene_go_named", {})
            genes_covered = entry.get("genes_covered", [])

            for gene in genes_covered:
                if pmid not in pmid_gene_themes:
                    pmid_gene_themes[pmid] = {}
                if gene not in pmid_gene_themes[pmid]:
                    pmid_gene_themes[pmid][gene] = {}
                terms = gene_go_named.get(gene, [])
                pmid_gene_themes[pmid][gene][theme_idx] = terms

    # Collect per-gene cross-theme PMIDs
    result: dict[str, list[dict[str, Any]]] = {}
    for pmid, gene_data in pmid_gene_themes.items():
        for gene, theme_map in gene_data.items():
            if len(theme_map) < 2:
                continue
            if gene not in result:
                result[gene] = []
            theme_info = []
            all_annotations = []
            for tidx in sorted(theme_map.keys()):
                tname = ""
                if isinstance(tidx, int) and tidx < len(themes):
                    tname = themes[tidx].get("anchor_term", {}).get("name", "")
                theme_info.append({"index": tidx, "name": tname})
                for term_name in theme_map[tidx]:
                    all_annotations.append(f"{tname}: {term_name}")
            result[gene].append({
                "pmid": pmid,
                "themes": theme_info,
                "annotations": all_annotations,
            })

    # Sort each gene's entries by number of themes spanned (desc)
    for gene in result:
        result[gene].sort(key=lambda x: len(x["themes"]), reverse=True)

    return result


def _format_enrichment_for_llm(
    enrichment_output: dict[str, Any],
    paper_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    gaf_pmids: dict[int, list[dict[str, Any]]] | None = None,
    gaf_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    hub_gene_abstracts: dict[str, list[dict[str, Any]]] | None = None,
    snippet_evidence: dict[int, list[dict[str, Any]]] | None = None,
    hub_gene_snippets: dict[str, list[dict[str, Any]]] | None = None,
    co_annotation_snippets: dict[int, dict[str, list[dict[str, Any]]]] | None = None,
    cross_theme_snippets: dict[str, list[dict[str, Any]]] | None = None,
    gene_narratives: dict[str, Any] | None = None,
) -> str:
    """
    Format enrichment output as readable text for LLM.

    Converts structured JSON to natural text that explains:
    - Study parameters
    - Hub genes and their theme participation (with abstracts/snippets)
    - Hierarchical themes with anchor and specific terms
    - Enrichment leaves (most specific terms)

    Args:
        enrichment_output: Phase 1 enrichment output (new format)
        paper_abstracts: Deprecated. Theme-level paper abstracts (lit-first).
        gaf_pmids: Optional dict mapping theme index to curated GAF PMIDs
            [{pmid, genes_covered}]. Injected as citation anchors per theme.
        gaf_abstracts: Optional dict mapping theme index to paper dicts with abstracts.
        hub_gene_abstracts: Optional dict mapping gene → paper dicts with abstracts.
            Injected under each hub gene in the hub genes section.
        snippet_evidence: Optional dict mapping theme index to ASTA snippet dicts.
            Preferred over gaf_abstracts (body-text evidence is more specific).
        hub_gene_snippets: Optional dict mapping gene → ASTA snippet dicts.
            Preferred over hub_gene_abstracts.

    Returns:
        Formatted string for LLM consumption
    """
    metadata = enrichment_output["metadata"]
    themes = enrichment_output.get("themes", [])
    hub_genes = enrichment_output.get("hub_genes", {})
    enrichment_leaves = enrichment_output.get("enrichment_leaves", [])

    # Build context string
    lines = []

    # Study metadata
    lines.append("# Study Overview")
    lines.append(f"- Species: {metadata['species']}")
    lines.append(f"- Input genes: {metadata['input_genes_count']}")
    lines.append(f"- Genes with annotations: {metadata['genes_with_annotations']}")
    lines.append(f"- Total enriched terms: {metadata['total_enriched_terms']}")
    lines.append(f"- FDR threshold: {metadata['fdr_threshold']}")
    lines.append(f"- Enrichment leaves: {metadata.get('enrichment_leaves_count', len(enrichment_leaves))}")
    lines.append(f"- Themes: {metadata.get('themes_count', len(themes))}")
    lines.append(f"- Hub genes: {metadata.get('hub_genes_count', len(hub_genes))}")
    lines.append("")

    # Build cross-theme PMID index for hub gene evidence
    cross_theme_index = _build_cross_theme_index(gaf_pmids, themes)

    # Hub genes (important for understanding cross-theme patterns)
    if hub_genes:
        lines.append("# Hub Genes (appearing in 3+ themes)")
        lines.append("")
        lines.append("These genes appear across multiple functional themes, suggesting they are biological coordinators:")
        lines.append("")

        hub_genes_sorted = sorted(
            hub_genes.items(), key=lambda x: x[1].get("theme_count", 0), reverse=True
        )[:20]  # Top 20 hub genes by theme_count — matches schema maxItems cap
        for gene, data in hub_genes_sorted:
            theme_count = data.get("theme_count", 0)
            theme_names = data.get("themes", [])[:5]  # Top 5 themes
            lines.append(f"## {gene} ({theme_count} themes)")
            lines.append(f"- Themes: {', '.join(theme_names)}")
            if len(data.get("themes", [])) > 5:
                lines.append(f"- ... and {len(data['themes']) - 5} more")

            # Inject hub gene snippets (preferred) or abstracts
            has_hub_snippets = bool(hub_gene_snippets and gene in hub_gene_snippets and hub_gene_snippets[gene])
            has_hub_abstracts = bool(hub_gene_abstracts and gene in hub_gene_abstracts and hub_gene_abstracts[gene])

            if has_hub_snippets:
                lines.append("### Supporting Evidence Snippets (full-text passages, cite PMID:xxxxx):")
                for snippet in hub_gene_snippets[gene]:  # type: ignore[index]
                    pmid = snippet.get("pmid", "")
                    title = snippet.get("title", "")
                    authors = snippet.get("authors", "")
                    snippet_text = snippet.get("snippet_text", "")
                    pmid_label = f"PMID:{pmid}" if pmid else snippet.get("paperId", "")
                    header = f"[{pmid_label}] {title}"
                    if authors:
                        header += f" — {authors}"
                    lines.append(header)
                    if snippet_text:
                        preview = snippet_text[:600] + "..." if len(snippet_text) > 600 else snippet_text
                        lines.append(f"Evidence: {preview}")
                    lines.append("")
            elif has_hub_abstracts:
                lines.append("### Supporting Literature (cite as PMID:xxxxx for cross-theme claims):")
                for paper in hub_gene_abstracts[gene]:  # type: ignore[index]
                    pmid = paper.get("pmid", "")
                    title = paper.get("title", "No title")
                    authors = paper.get("authors", "")
                    year = paper.get("year", "")
                    abstract = paper.get("abstract", "")
                    author_year = (
                        f"{authors} ({year})" if authors and year else authors or year
                    )
                    header = f"[PMID:{pmid}] {title}"
                    if author_year:
                        header += f" — {author_year}"
                    lines.append(header)
                    if abstract:
                        preview = abstract[:400] + "..." if len(abstract) > 400 else abstract
                        lines.append(f"Abstract: {preview}")
                lines.append("")

            # Cross-theme GAF evidence (same gene annotated across themes)
            if gene in cross_theme_index:
                cross_entries = cross_theme_index[gene][:3]  # Top 3
                lines.append("### Cross-theme GAF Evidence (this gene links these themes via curated annotations):")
                for ct in cross_entries:
                    ct_pmid = ct["pmid"]
                    ct_themes = [t["name"] for t in ct["themes"] if t["name"]]
                    lines.append(f"[PMID:{ct_pmid}] Links {len(ct['themes'])} themes: {', '.join(ct_themes)}")
                    for ann in ct["annotations"]:
                        lines.append(f"  - {ann}")
                lines.append("")

            # Cross-theme evidence snippets (full-text linking evidence)
            if cross_theme_snippets and gene in cross_theme_snippets and cross_theme_snippets[gene]:
                lines.append("### Cross-theme Evidence Snippets (full-text linking evidence):")
                for snippet in cross_theme_snippets[gene]:
                    pmid = snippet.get("pmid", "")
                    title = snippet.get("title", "")
                    authors = snippet.get("authors", "")
                    snippet_text = snippet.get("snippet_text", "")
                    pmid_label = f"PMID:{pmid}" if pmid else snippet.get("paperId", "")
                    header = f"[{pmid_label}] {title}"
                    if authors:
                        header += f" — {authors}"
                    lines.append(header)
                    if snippet_text:
                        preview = snippet_text[:600] + "..." if len(snippet_text) > 600 else snippet_text
                        lines.append(f"Evidence: {preview}")
                    lines.append("")

            # Pre-digested mechanistic narrative (from Phase 1c subagent)
            hub_narratives = (gene_narratives or {}).get("hub_genes", {})
            if gene in hub_narratives:
                lines.append("### Mechanistic Narrative (from focused evidence analysis):")
                lines.append(hub_narratives[gene])
                lines.append("")

            lines.append("")

        lines.append("---")
        lines.append("")

    # Hierarchical themes
    if themes:
        lines.append("# Hierarchical Themes")
        lines.append("")
        lines.append("Each theme groups related GO terms under an anchor (intermediate-depth term):")
        lines.append("")

        for i, theme in enumerate(themes[:30]):  # Top 30 themes
            anchor = theme.get("anchor_term", {})
            specific_terms = theme.get("specific_terms", [])
            confidence = theme.get("anchor_confidence", "")

            lines.append(f"## Theme {i+1}: {anchor.get('name', 'Unknown')}")
            lines.append(f"- theme_index (use this exact integer in your response): {i}")
            lines.append(f"- GO ID: {anchor.get('go_id', '')}")
            lines.append(f"- Namespace: {anchor.get('namespace', '')}")
            lines.append(f"- FDR: {anchor.get('fdr', 0):.2e}")
            lines.append(f"- Fold enrichment: {anchor.get('fold_enrichment', 0):.1f}x")
            lines.append(f"- Confidence: {confidence}")
            lines.append(f"- Genes ({len(anchor.get('genes', []))}): {', '.join(sorted(anchor.get('genes', []))[:10])}")
            if len(anchor.get('genes', [])) > 10:
                lines.append(f"  ... and {len(anchor.get('genes', [])) - 10} more")
            lines.append("")

            # Specific terms (nested under anchor)
            if specific_terms:
                lines.append(f"### Specific Terms ({len(specific_terms)} nested)")
                for specific in specific_terms[:5]:  # Top 5 specific terms
                    lines.append(
                        f"  - {specific.get('name', '')} ({specific.get('go_id', '')}): "
                        f"FDR={specific.get('fdr', 0):.2e}, "
                        f"{len(specific.get('genes', []))} genes: "
                        f"{', '.join(sorted(specific.get('genes', []))[:8])}"
                    )
                if len(specific_terms) > 5:
                    lines.append(f"  - ... and {len(specific_terms) - 5} more")
                lines.append("")

            # Ranked candidate key genes
            ranked = rank_genes_for_theme(theme, hub_genes)
            if ranked:
                lines.append(f"### Candidate Key Genes (ranked by theme-specificity, select 2-5):")
                for rank_num, entry in enumerate(ranked, 1):
                    specific_label = (
                        f"in {entry['in_specific_terms']} specific term(s)"
                        if entry["in_specific_terms"] > 0
                        else "anchor-only"
                    )
                    lines.append(
                        f"  {rank_num}. {entry['gene']}  "
                        f"[{specific_label}, appears in {entry['n_themes']} theme(s), score: {entry['score']:.2f}]"
                    )
                lines.append("")

            # ASTA snippet evidence per theme (preferred over abstracts)
            has_snippets = bool(snippet_evidence and i in snippet_evidence and snippet_evidence[i])
            if has_snippets:
                lines.append("### Available Evidence Snippets (full-text passages, prefer these for citations):")
                lines.append("These are body-text passages from papers with specific experimental evidence.")
                lines.append("Cite the PMID inline: '[EXTERNAL] FOXO3 suppresses migration PMID:19188590.'")
                for snippet in snippet_evidence[i]:  # type: ignore[index]
                    pmid = snippet.get("pmid", "")
                    title = snippet.get("title", "")
                    authors = snippet.get("authors", "")
                    snippet_text = snippet.get("snippet_text", "")
                    pmid_label = f"PMID:{pmid}" if pmid else snippet.get("paperId", "")
                    header = f"[{pmid_label}] {title}"
                    if authors:
                        header += f" — {authors}"
                    lines.append(header)
                    if snippet_text:
                        preview = snippet_text[:600] + "..." if len(snippet_text) > 600 else snippet_text
                        lines.append(f"Evidence: {preview}")
                    lines.append("")
                lines.append("")

            # Within-theme co-annotation evidence (gene linked to 2+ GO processes)
            has_co_annot = bool(co_annotation_snippets and i in co_annotation_snippets and co_annotation_snippets[i])
            if has_co_annot:
                lines.append("### Co-Annotation Evidence (gene linked to multiple GO processes in this theme):")
                lines.append("These snippets describe how a gene connects different biological processes within this theme.")
                for gene, gene_snippets in co_annotation_snippets[i].items():  # type: ignore[index]
                    if not gene_snippets:
                        continue
                    # Show which GO terms this gene co-annotates
                    co_terms = []
                    if gaf_pmids and i in gaf_pmids:
                        for entry in gaf_pmids[i]:
                            gene_go_named = entry.get("gene_go_named", {})
                            if gene in gene_go_named and len(gene_go_named[gene]) >= 2:
                                co_terms = [t.split(" [GO:")[0] for t in gene_go_named[gene][:3]]
                                break
                    if co_terms:
                        lines.append(f"**{gene}** annotated to: {', '.join(co_terms)}")
                    else:
                        lines.append(f"**{gene}** (multi-process co-annotation)")
                    for snippet in gene_snippets:
                        pmid = snippet.get("pmid", "")
                        title = snippet.get("title", "")
                        authors = snippet.get("authors", "")
                        snippet_text = snippet.get("snippet_text", "")
                        pmid_label = f"PMID:{pmid}" if pmid else snippet.get("paperId", "")
                        header = f"[{pmid_label}] {title}"
                        if authors:
                            header += f" — {authors}"
                        lines.append(header)
                        if snippet_text:
                            preview = snippet_text[:600] + "..." if len(snippet_text) > 600 else snippet_text
                            lines.append(f"Evidence: {preview}")
                        lines.append("")
                lines.append("")

            # Pre-digested gene narratives for this theme (from Phase 1c subagent)
            theme_gene_narrs = (gene_narratives or {}).get("theme_genes", {}).get(i, {})
            co_annot_narrs = (gene_narratives or {}).get("co_annotations", {}).get(i, {})
            all_theme_narrs = {**theme_gene_narrs, **co_annot_narrs}
            if all_theme_narrs:
                lines.append("### Gene Evidence Narratives (mechanistic summaries from focused analysis):")
                for gene_name, narr in all_theme_narrs.items():
                    lines.append(f"- **{gene_name}**: {narr}")
                lines.append("")

            # GAF-curated citations per theme (preferred, highest confidence)
            if gaf_pmids and i in gaf_pmids and gaf_pmids[i]:
                lines.append("### Available GAF Citations (curated gene→GO annotations):")
                lines.append("Use these PMIDs in [DATA] and [EXTERNAL] tags for gene→GO claims:")

                # Build per-PMID lookup from gaf_pmids entries
                gaf_entry_by_pmid: dict[str, dict[str, Any]] = {
                    e.get("pmid", ""): e for e in gaf_pmids[i]
                }

                has_abstracts = bool(gaf_abstracts and i in gaf_abstracts and gaf_abstracts[i])
                if has_abstracts:
                    for paper in gaf_abstracts[i]:  # type: ignore[index]
                        pmid = paper.get("pmid", "")
                        title = paper.get("title", "")
                        abstract = paper.get("abstract", "")
                        authors = paper.get("authors", "")
                        year = paper.get("year", "")
                        author_year = (
                            f"{authors} ({year})" if authors and year else authors or year
                        )
                        header = f"[PMID:{pmid}] {title}"
                        if author_year:
                            header += f" — {author_year}"
                        lines.append(header)
                        lines.append(_format_gene_go_annotations(gaf_entry_by_pmid.get(pmid, {})))
                        if abstract:
                            preview = abstract[:400] + "..." if len(abstract) > 400 else abstract
                            lines.append(f"Abstract: {preview}")
                        lines.append("")
                else:
                    # Fallback: PMID + gene→GO annotations only (no API calls needed)
                    for entry in gaf_pmids[i]:
                        pmid = entry.get("pmid", "")
                        lines.append(f"- PMID:{pmid}")
                        lines.append(f"  {_format_gene_go_annotations(entry)}")
                lines.append("")

            # Fallback: full abstracts from deprecated paper_abstracts param
            elif paper_abstracts and i in paper_abstracts and paper_abstracts[i]:
                lines.append("### Available Literature (cite inline as PMID:xxxxx where relevant):")
                for paper in paper_abstracts[i]:
                    pmid = paper.get("pmid", "")
                    title = paper.get("title", "No title")
                    authors = paper.get("authors", "")
                    year = paper.get("year", "")
                    abstract = paper.get("abstract", "")

                    author_year = (
                        f"{authors} ({year})" if authors and year
                        else authors or year
                    )
                    header = f"[PMID:{pmid}] {title}"
                    if author_year:
                        header += f" — {author_year}"
                    lines.append(header)
                    if abstract:
                        preview = abstract[:400] + "..." if len(abstract) > 400 else abstract
                        lines.append(f"Abstract: {preview}")
                    lines.append("")
                lines.append("")

            lines.append("---")
            lines.append("")

    # Enrichment leaves (most specific terms)
    if enrichment_leaves:
        lines.append("# Enrichment Leaves (Most Specific Terms)")
        lines.append("")
        lines.append("These are the most specific enriched terms (no enriched descendants):")
        lines.append("")

        for i, leaf in enumerate(enrichment_leaves[:20]):  # Top 20 leaves
            lines.append(
                f"- {leaf.get('name', '')} ({leaf.get('go_id', '')}): "
                f"FDR={leaf.get('fdr', 0):.2e}, "
                f"{len(leaf.get('genes', []))} genes"
            )

        if len(enrichment_leaves) > 20:
            lines.append(f"- ... and {len(enrichment_leaves) - 20} more")
        lines.append("")

    return "\n".join(lines)


def _empty_markdown_explanation(enrichment_output: dict[str, Any], model: str) -> str:
    """
    Build empty markdown explanation when no enrichment to explain.

    Args:
        enrichment_output: Phase 1 enrichment output (with no themes)
        model: Model name for metadata

    Returns:
        Minimal markdown explanation
    """
    metadata = enrichment_output["metadata"]

    markdown = f"""# GO Enrichment Analysis Report

## Summary

No significant GO enrichment was found for the provided gene list.

**Analysis Details:**
- Input genes: {metadata['input_genes_count']}
- Genes with annotations: {metadata['genes_with_annotations']}
- FDR threshold: {metadata['fdr_threshold']}
- Total enriched terms: {metadata['total_enriched_terms']}

## Interpretation

This could indicate that:
- The genes do not share common functional themes
- The sample size is too small for statistical significance
- The genes may represent diverse biological processes

**Generated by:** {model}
"""

    return markdown


def _add_go_term_hyperlinks(markdown: str, enrichment_output: dict[str, Any]) -> str:
    """
    Add hyperlinks to GO IDs in markdown output.

    Converts patterns like "GO:1234567" to "[GO:1234567](http://purl.obolibrary.org/obo/GO_1234567)"

    Args:
        markdown: LLM-generated markdown
        enrichment_output: Phase 1 enrichment output (not used but kept for consistency)

    Returns:
        Markdown with hyperlinked GO IDs
    """
    # Pattern: GO:1234567 -> [GO:1234567](purl)
    def replace_go_id(match):
        go_id = match.group(0)
        go_purl_id = go_id.replace(":", "_")
        purl = f"http://purl.obolibrary.org/obo/{go_purl_id}"
        return f"[{go_id}]({purl})"

    # Find bare GO IDs (not already inside a markdown link like [GO:...])
    original = markdown
    markdown = re.sub(r"(?<!\[)GO:\d{7}", replace_go_id, markdown)

    # Count replacements
    hyperlinks_added = markdown.count("[GO:") - original.count("[GO:")

    if hyperlinks_added > 0:
        print(f"  ✓ Added {hyperlinks_added} GO ID hyperlink(s)")
    else:
        print(f"  ℹ No GO IDs found to hyperlink")

    return markdown


def _add_pmid_hyperlinks(markdown: str) -> str:
    """
    Add hyperlinks to PMIDs in markdown output.

    Converts patterns like "PMID:12345" to "[PMID:12345](https://pubmed.ncbi.nlm.nih.gov/12345/)"

    Args:
        markdown: Markdown text

    Returns:
        Markdown with hyperlinked PMIDs
    """
    # Pattern: PMID:12345 -> [PMID:12345](pubmed_url)
    def replace_pmid(match):
        pmid = match.group(0)
        pmid_number = match.group(1)
        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid_number}/"
        return f"[{pmid}]({pubmed_url})"

    # Find all PMIDs and replace with hyperlinks
    original = markdown
    markdown = re.sub(r"PMID:(\d+)", replace_pmid, markdown)

    # Count replacements
    hyperlinks_added = markdown.count("[PMID:") - original.count("[PMID:")

    if hyperlinks_added > 0:
        print(f"  ✓ Added {hyperlinks_added} PMID hyperlink(s)")
    else:
        print(f"  ℹ No PMIDs found to hyperlink")

    return markdown


def _validate_citations(markdown: str, enrichment_output: dict[str, Any]) -> None:
    """
    Validate GO IDs in LLM output to detect hallucinations.

    Cross-checks all GO IDs mentioned in the markdown against the
    enrichment input data. Prints warnings for any hallucinated citations.

    Args:
        markdown: LLM-generated markdown
        enrichment_output: Phase 1 enrichment output (source of valid citations)
    """
    # Extract all GO IDs from markdown output
    go_id_pattern = r"GO:\d{7}"
    output_go_ids = set(re.findall(go_id_pattern, markdown))

    # Build set of valid GO IDs from enrichment input
    valid_go_ids = set()

    # From themes
    for theme in enrichment_output.get("themes", []):
        anchor = theme.get("anchor_term", {})
        if anchor.get("go_id"):
            valid_go_ids.add(anchor["go_id"])

        for specific in theme.get("specific_terms", []):
            if specific.get("go_id"):
                valid_go_ids.add(specific["go_id"])

    # From enrichment leaves
    for leaf in enrichment_output.get("enrichment_leaves", []):
        if leaf.get("go_id"):
            valid_go_ids.add(leaf["go_id"])

    # Validate GO IDs
    if output_go_ids:
        hallucinated_go_ids = output_go_ids - valid_go_ids
        if hallucinated_go_ids:
            print("\n" + "⚠" * 40)
            print("WARNING: Potential GO ID Hallucinations Detected")
            print("⚠" * 40)
            print(f"\nThe LLM output contains {len(hallucinated_go_ids)} GO ID(s) that were NOT in the input data:")
            for go_id in sorted(hallucinated_go_ids):
                print(f"  - {go_id}")
            print("\nThese may be:")
            print("  1. Hallucinated by the LLM (incorrect)")
            print("  2. Valid GO IDs from the LLM's training data (plausible but unverified)")
            print("\nPlease verify these GO IDs manually if they appear in key conclusions.")
            print("⚠" * 40 + "\n")
        else:
            print("  ✓ GO ID validation: All GO IDs in output match input data")
    else:
        print("  ℹ GO ID validation: No GO IDs found in LLM output")


def _count_provenance_tags(markdown: str) -> None:
    """
    Count and report provenance tags in LLM output.

    Args:
        markdown: LLM-generated markdown
    """
    tags = {
        "[DATA]": len(re.findall(r"\[DATA\]", markdown)),
        "[INFERENCE]": len(re.findall(r"\[INFERENCE\]", markdown)),
        "[EXTERNAL]": len(re.findall(r"\[EXTERNAL\]", markdown)),
        "[GO-HIERARCHY]": len(re.findall(r"\[GO-HIERARCHY\]", markdown)),
    }

    total = sum(tags.values())

    if total > 0:
        print(f"  ✓ Provenance tags found: {total} total")
        for tag, count in tags.items():
            if count > 0:
                print(f"    - {tag}: {count}")
    else:
        print("  ⚠ No provenance tags found in LLM output")
        print("    The LLM should label claims with [DATA], [INFERENCE], [EXTERNAL], [GO-HIERARCHY]")


# =============================================================================
# New public functions (Ring 1b output quality)
# =============================================================================


def rank_genes_for_theme(
    theme: dict[str, Any],
    hub_genes: dict[str, Any],
    top_n: int = 8,
) -> list[dict[str, Any]]:
    """
    Rank genes within a theme by theme-intrinsic signals only.

    Scoring:
        score = (in_specific_terms * 2.0) + (1.0 / n_themes)

    Genes in more specific (leaf) terms score higher; genes exclusive to this
    theme score higher than hub genes that appear everywhere.

    Args:
        theme: Single theme dict from enrichment output
        hub_genes: hub_genes dict from enrichment output (gene → {theme_count, ...})
        top_n: Maximum number of candidates to return (default 8)

    Returns:
        List of dicts with keys: gene, in_specific_terms, n_themes, score
        Sorted by descending score, capped at top_n.
    """
    anchor_genes = set(theme.get("anchor_term", {}).get("genes", []))
    specific_terms = theme.get("specific_terms", [])

    # Collect all genes in this theme
    all_genes: set[str] = set(anchor_genes)
    for s in specific_terms:
        all_genes.update(s.get("genes", []))

    scored = []
    for gene in all_genes:
        in_specific = sum(1 for s in specific_terms if gene in s.get("genes", []))
        n_themes = hub_genes[gene]["theme_count"] if gene in hub_genes else 1
        score = (in_specific * 2.0) + (1.0 / n_themes)
        scored.append({
            "gene": gene,
            "in_specific_terms": in_specific,
            "n_themes": n_themes,
            "score": score,
        })

    scored.sort(key=lambda x: -x["score"])
    return scored[:top_n]


def validate_explanation_json(
    explanation: dict[str, Any],
    enrichment_output: dict[str, Any],
) -> list[str]:
    """
    Post-generation validation of LLM-produced explanation JSON.

    Checks that genes and GO IDs in key_genes and key_insights actually appear
    in the corresponding enrichment theme. Logs warnings; does NOT crash.

    Args:
        explanation: Structured explanation dict (from LLM via model.model_dump())
        enrichment_output: Phase 1 enrichment output

    Returns:
        List of warning strings (empty if no violations found)
    """
    warnings: list[str] = []
    enrichment_themes = enrichment_output.get("themes", [])

    for exp_theme in explanation.get("themes", []):
        idx = exp_theme.get("theme_index", -1)
        if not isinstance(idx, int) or idx < 0 or idx >= len(enrichment_themes):
            continue

        enrichment_theme = enrichment_themes[idx]

        # Build valid gene set for this theme
        valid_genes: set[str] = set(enrichment_theme["anchor_term"].get("genes", []))
        for s in enrichment_theme.get("specific_terms", []):
            valid_genes.update(s.get("genes", []))

        # Build valid GO ID set for this theme
        valid_go_ids: set[str] = {enrichment_theme["anchor_term"].get("go_id", "")}
        for s in enrichment_theme.get("specific_terms", []):
            go_id = s.get("go_id", "")
            if go_id:
                valid_go_ids.add(go_id)
        valid_go_ids.discard("")

        # Validate key_genes
        for kg in exp_theme.get("key_genes", []):
            gene = kg.get("gene", "")
            if gene and gene not in valid_genes:
                warnings.append(f"Theme {idx}: gene '{gene}' not found in theme gene list")

            go_id = kg.get("go_id", "")
            if go_id and go_id not in valid_go_ids:
                warnings.append(f"Theme {idx}: GO ID '{go_id}' not found in theme GO IDs")

        # Validate key_insights GO IDs
        for ki in exp_theme.get("key_insights", []):
            go_id = ki.get("go_id", "")
            if go_id and go_id not in valid_go_ids:
                warnings.append(f"Theme {idx}: insight GO ID '{go_id}' not found in theme GO IDs")

    return warnings


def validate_narrative_genes(
    explanation: dict[str, Any],
    enrichment_output: dict[str, Any],
) -> list[dict[str, Any]]:
    """Find hallucinated gene symbols in narrative free-text fields.

    Scans backtick-quoted tokens in ``narrative``,
    ``key_insights[].insight``, and ``key_genes[].description`` for each
    theme, plus ``hub_genes[].narrative``.  Any token that looks like a gene
    symbol (all-caps, may contain digits/hyphens) but is not in the valid
    set for that theme is reported.

    Returns:
        List of dicts, each with keys:
        - location: e.g. "theme.0.narrative", "hub_gene.BRCA1.narrative"
        - gene: the hallucinated gene symbol
        - sentence: the full sentence containing the hallucination
        - valid_genes: the valid gene set for context (only for themes)
    """
    enrichment_themes = enrichment_output.get("themes", [])
    all_input_genes: set[str] = set()
    for t in enrichment_themes:
        all_input_genes.update(t.get("anchor_term", {}).get("genes", []))
        for s in t.get("specific_terms", []):
            all_input_genes.update(s.get("genes", []))

    # Also include hub genes as valid in hub_gene narratives
    hub_gene_names = set(enrichment_output.get("hub_genes", {}).keys())

    findings: list[dict[str, Any]] = []

    # --- Per-theme fields ---
    for exp_theme in explanation.get("themes", []):
        idx = exp_theme.get("theme_index", -1)
        if not isinstance(idx, int) or idx < 0 or idx >= len(enrichment_themes):
            continue

        et = enrichment_themes[idx]
        valid_genes: set[str] = set(et.get("anchor_term", {}).get("genes", []))
        for s in et.get("specific_terms", []):
            valid_genes.update(s.get("genes", []))

        # Check narrative
        _check_text_for_hallucinated_genes(
            exp_theme.get("narrative", ""),
            valid_genes,
            f"theme.{idx}.narrative",
            findings,
        )
        # Check key_insights
        for j, ki in enumerate(exp_theme.get("key_insights", [])):
            _check_text_for_hallucinated_genes(
                ki.get("insight", ""),
                valid_genes,
                f"theme.{idx}.key_insights.{j}",
                findings,
            )
        # Check key_genes descriptions
        for j, kg in enumerate(exp_theme.get("key_genes", [])):
            _check_text_for_hallucinated_genes(
                kg.get("description", ""),
                valid_genes,
                f"theme.{idx}.key_genes.{j}.description",
                findings,
            )

    # --- Hub gene narratives ---
    for hg in explanation.get("hub_genes", []):
        gene = hg.get("gene", "")
        _check_text_for_hallucinated_genes(
            hg.get("narrative", ""),
            all_input_genes | hub_gene_names,
            f"hub_gene.{gene}.narrative",
            findings,
        )

    return findings


def _check_text_for_hallucinated_genes(
    text: str,
    valid_genes: set[str],
    location: str,
    findings: list[dict[str, Any]],
) -> None:
    """Extract backtick-quoted gene symbols from *text* and flag invalid ones."""
    backtick_tokens = re.findall(r"`([^`]+)`", text)
    for token in backtick_tokens:
        # Heuristic: gene symbols are typically uppercase, may contain digits/hyphens
        if not re.match(r"^[A-Z][A-Z0-9\-]+$", token):
            continue
        if token not in valid_genes:
            # Find the sentence containing this gene
            sentence = _find_sentence(text, token)
            findings.append({
                "location": location,
                "gene": token,
                "sentence": sentence,
            })


def _find_sentence(text: str, token: str) -> str:
    """Return the sentence in *text* that contains *token*."""
    # Split on sentence-ending punctuation followed by space or end
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for s in sentences:
        if token in s:
            return s.strip()
    return text.strip()


def strip_hallucinated_gene_sentences(
    explanation: dict[str, Any],
    findings: list[dict[str, Any]],
) -> int:
    """Remove sentences containing hallucinated genes from narrative fields.

    Modifies *explanation* in-place.  Returns the number of sentences stripped.
    """
    if not findings:
        return 0

    # Group findings by location
    by_location: dict[str, set[str]] = {}
    for f in findings:
        by_location.setdefault(f["location"], set()).add(f["gene"])

    stripped_count = 0

    for location, bad_genes in by_location.items():
        parts = location.split(".")
        # Navigate to the text field
        text = _get_nested_text(explanation, parts)
        if text is None:
            continue

        # Split into sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)
        clean_sentences = []
        for s in sentences:
            # Check if any hallucinated gene is backtick-quoted in this sentence
            has_bad = any(f"`{g}`" in s for g in bad_genes)
            if has_bad:
                stripped_count += 1
            else:
                clean_sentences.append(s)

        new_text = " ".join(clean_sentences)
        _set_nested_text(explanation, parts, new_text)

    return stripped_count


def _get_nested_text(explanation: dict[str, Any], parts: list[str]) -> str | None:
    """Navigate the explanation dict by dotted path parts and return the text."""
    try:
        if parts[0] == "theme":
            idx = int(parts[1])
            theme = next(
                (t for t in explanation.get("themes", []) if t.get("theme_index") == idx),
                None,
            )
            if theme is None:
                return None
            if parts[2] == "narrative":
                return theme.get("narrative")
            elif parts[2] == "key_insights":
                j = int(parts[3])
                return theme.get("key_insights", [{}])[j].get("insight")
            elif parts[2] == "key_genes":
                j = int(parts[3])
                return theme.get("key_genes", [{}])[j].get("description")
        elif parts[0] == "hub_gene":
            gene = parts[1]
            for hg in explanation.get("hub_genes", []):
                if hg.get("gene") == gene:
                    return hg.get("narrative")
    except (IndexError, KeyError, ValueError):
        pass
    return None


def _set_nested_text(explanation: dict[str, Any], parts: list[str], text: str) -> None:
    """Set text at the dotted path in the explanation dict."""
    try:
        if parts[0] == "theme":
            idx = int(parts[1])
            theme = next(
                (t for t in explanation.get("themes", []) if t.get("theme_index") == idx),
                None,
            )
            if theme is None:
                return
            if parts[2] == "narrative":
                theme["narrative"] = text
            elif parts[2] == "key_insights":
                j = int(parts[3])
                theme["key_insights"][j]["insight"] = text
            elif parts[2] == "key_genes":
                j = int(parts[3])
                theme["key_genes"][j]["description"] = text
        elif parts[0] == "hub_gene":
            gene = parts[1]
            for hg in explanation.get("hub_genes", []):
                if hg.get("gene") == gene:
                    hg["narrative"] = text
                    return
    except (IndexError, KeyError, ValueError):
        pass


def write_themes_csv(enrichment_output: dict[str, Any], csv_path: Path) -> None:
    """Write a CSV file with all enrichment themes and their full gene lists.

    Args:
        enrichment_output: Phase 1 enrichment output containing themes.
        csv_path: Destination path for the CSV file.
    """
    _NS_ABBREV = {
        "biological_process": "BP",
        "molecular_function": "MF",
        "cellular_component": "CC",
    }
    enrichment_themes = enrichment_output.get("themes", [])
    with open(csv_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([
            "theme_number", "theme_name", "go_id", "namespace",
            "fdr", "fold_enrichment", "anchor_confidence", "n_genes", "genes",
        ])
        for i, theme in enumerate(enrichment_themes):
            anchor = theme.get("anchor_term", {})
            name = anchor.get("name", "Unknown")
            go_id = anchor.get("go_id", "")
            ns_full = anchor.get("namespace", "")
            ns = _NS_ABBREV.get(ns_full, ns_full[:2].upper() if ns_full else "?")
            fdr = anchor.get("fdr", 0)
            fold_enrichment = anchor.get("fold_enrichment", "")
            conf = theme.get("anchor_confidence", "")
            all_genes = sorted(theme.get("all_genes", anchor.get("genes", [])))
            writer.writerow([
                i + 1, name, go_id, ns, f"{fdr:.2e}", fold_enrichment,
                conf, len(all_genes), ";".join(all_genes),
            ])


def _header_to_anchor(header_text: str) -> str:
    """Convert a markdown header string to a GFM anchor fragment."""
    text = header_text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return f"#{text}"


def render_explanation_to_markdown(
    explanation: dict[str, Any],
    enrichment_output: dict[str, Any],
    flagged_themes: set[int] | None = None,
    csv_filename: str | None = None,
) -> str:
    """
    Programmatically render a structured explanation dict to markdown.

    No LLM involvement — all structure (headers, hyperlinks, [REF:GENE] markers)
    is added deterministically. GO IDs are converted to hyperlinks by this function.

    Args:
        explanation: Structured explanation dict (from LLM via model.model_dump())
        enrichment_output: Phase 1 enrichment output (for theme metadata)
        flagged_themes: Set of theme indices that failed content validation.
            These themes are rendered as data-only stubs (anchor name, FDR, genes)
            rather than using the potentially-incorrect LLM narrative.

    Returns:
        Markdown string ready for display
    """
    if flagged_themes is None:
        flagged_themes = set()
    enrichment_themes = enrichment_output.get("themes", [])
    metadata = enrichment_output.get("metadata", {})
    lines: list[str] = []

    # Document title
    species = metadata.get("species", "")
    title_suffix = f" — {species}" if species else ""
    lines.append(f"# GO Enrichment Analysis Report{title_suffix}\n")
    lines.append("\n")

    # Methodology note
    n_explained = sum(
        1 for t in explanation.get("themes", [])
        if isinstance(t.get("theme_index"), int)
        and 0 <= t["theme_index"] < len(enrichment_themes)
    )
    n_total = len(enrichment_themes)
    theme_count_note = (
        f" This report provides detailed narrative for the top "
        f"**{n_explained} of {n_total} themes**, ranked by FDR ascending."
        f" All themes are listed in the Theme Index below."
        if n_explained < n_total else ""
    )
    lines.append(
        f"> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). "
        f"Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, "
        f"chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. "
        f"Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster "
        f"under the anchor.{theme_count_note}\n"
    )
    lines.append("\n")

    # Build a lookup from theme_index → LLM explanation dict
    exp_theme_by_idx: dict[int, dict] = {
        t["theme_index"]: t
        for t in explanation.get("themes", [])
        if isinstance(t.get("theme_index"), int)
        and 0 <= t["theme_index"] < len(enrichment_themes)
    }

    # Theme index table (all themes, linking to their sections)
    _NS_ABBREV = {
        "biological_process": "BP",
        "molecular_function": "MF",
        "cellular_component": "CC",
    }
    if enrichment_themes:
        lines.append("## Theme Index\n")
        lines.append("\n")
        if csv_filename:
            lines.append(f"Full gene listings: [{csv_filename}]({csv_filename})\n")
            lines.append("\n")
        lines.append("| # | Theme | NS | FDR | Genes | Confidence |\n")
        lines.append("|---|-------|----|-----|-------|------------|\n")
        for i, et in enumerate(enrichment_themes):
            anc = et.get("anchor_term", {})
            t_name = anc.get("name", "Unknown")
            t_go_id = anc.get("go_id", "")
            ns_full = anc.get("namespace", "")
            ns = _NS_ABBREV.get(ns_full, ns_full[:2].upper() if ns_full else "?")
            fdr = anc.get("fdr", 0)
            n_genes = len(et.get("all_genes", anc.get("genes", [])))
            conf = et.get("anchor_confidence", "")
            anchor_link = _header_to_anchor(f"Theme {i + 1} {t_name}")
            go_link = _go_id_to_link(t_go_id)
            lines.append(
                f"| [{i + 1}]({anchor_link}) | [{t_name}]({anchor_link}) {go_link}"
                f" | {ns} | {fdr:.2e} | {n_genes} | {conf} |\n"
            )
        lines.append("\n")
        lines.append("---\n")
        lines.append("\n")

    # Per-theme sections — iterate all enrichment themes in order so flagged
    # (missing) themes also get data-only stubs rendered
    for idx, enrichment_theme in enumerate(enrichment_themes):
        # Skip themes that are neither covered by LLM nor flagged
        if idx not in exp_theme_by_idx and idx not in flagged_themes:
            continue

        exp_theme = exp_theme_by_idx.get(idx, {})
        anchor = enrichment_theme.get("anchor_term", {})
        anchor_name = anchor.get("name", "Unknown")
        anchor_go_id = anchor.get("go_id", "")

        # Section header (always uses trusted enrichment data, not LLM)
        lines.append(f"### Theme {idx + 1}: {anchor_name}\n")
        lines.append("\n")

        # Summary line with linked GO ID and anchor confidence
        go_link = _go_id_to_link(anchor_go_id)
        confidence = enrichment_theme.get("anchor_confidence", "")
        confidence_str = f"  · Anchor confidence: **{confidence}**" if confidence else ""
        lines.append(f"**Summary:** {anchor_name} ({go_link}){confidence_str}\n")
        lines.append("\n")

        if idx in flagged_themes:
            # Data-only stub: LLM content failed validation or was not generated
            fdr = anchor.get("fdr", 0)
            genes = sorted(anchor.get("genes", []))
            gene_str = ", ".join(genes[:15])
            if len(genes) > 15:
                gene_str += f" … (+{len(genes) - 15} more)"
            stub_reason = (
                "Not covered by LLM narrative — showing data only."
                if idx not in exp_theme_by_idx
                else "Content validation failed for this theme — showing data only."
            )
            lines.append(f"> ⚠ {stub_reason}\n")
            lines.append("\n")
            lines.append(f"**FDR**: {fdr:.2e} · **Genes ({len(genes)})**: {gene_str}\n")
            lines.append("\n")
        else:
            # Narrative (free prose from LLM — provenance tags are inside)
            narrative = exp_theme.get("narrative", "")
            if narrative:
                lines.append(f"{narrative}\n")
                lines.append("\n")

            # Key Insights
            key_insights = exp_theme.get("key_insights", [])
            if key_insights:
                lines.append("#### Key Insights\n")
                lines.append("\n")
                for ki in key_insights:
                    insight = ki.get("insight", "")
                    go_id = ki.get("go_id", "")
                    go_link = f" ({_go_id_to_link(go_id)})" if go_id else ""
                    lines.append(f"- {insight}{go_link}\n")
                lines.append("\n")

            # Key Genes
            key_genes = exp_theme.get("key_genes", [])
            if key_genes:
                lines.append("#### Key Genes\n")
                lines.append("\n")
                for kg in key_genes:
                    gene = kg.get("gene", "")
                    go_id = kg.get("go_id", "")
                    desc = kg.get("description", "")
                    claim_type = kg.get("claim_type", "INFERENCE")
                    go_link = f" ({_go_id_to_link(go_id)})" if go_id else ""
                    lines.append(f"- **{gene}**: [{claim_type}] {desc}{go_link}\n")
                lines.append("\n")

            # Statistical context
            stat_ctx = exp_theme.get("statistical_context", "")
            if stat_ctx:
                lines.append("#### Statistical Context\n")
                lines.append("\n")
                lines.append(f"{stat_ctx}\n")
                lines.append("\n")

        lines.append("---\n")
        lines.append("\n")

    # Hub genes section
    hub_genes_exp = explanation.get("hub_genes", [])
    if hub_genes_exp:
        lines.append("## Hub Genes\n")
        lines.append("\n")
        for hg in hub_genes_exp:
            gene = hg.get("gene", "")
            narrative = hg.get("narrative", "")
            claim_type = hg.get("claim_type", "INFERENCE")
            lines.append(f"- **{gene}**: [{claim_type}] {narrative}\n")
        lines.append("\n")

    # Overall summary
    overall = explanation.get("overall_summary", [])
    if overall:
        lines.append("## Overall Summary\n")
        lines.append("\n")
        for para in overall:
            lines.append(f"{para}\n")
            lines.append("\n")

    # Inference disclaimer
    lines.append("> **Note:** Statements tagged \\[INFERENCE\\] without PMID citations are based on the LLM's "
                 "latent biological knowledge and have not been independently verified against the literature. "
                 "These should be treated as hypotheses requiring validation.\n")
    lines.append("\n")

    return "".join(lines)


# =============================================================================
# PMID validation, claim_type correction, and stripping
# =============================================================================

_PMID_RE = re.compile(r"PMID:(\d+)")


def build_pmid_whitelist(
    gaf_pmids: dict[int, list[dict[str, Any]]] | None = None,
    gaf_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    hub_gene_abstracts: dict[str, list[dict[str, Any]]] | None = None,
    snippet_evidence: dict[int, list[dict[str, Any]]] | None = None,
    hub_gene_snippets: dict[str, list[dict[str, Any]]] | None = None,
    co_annotation_snippets: dict[int, dict[str, list[dict[str, Any]]]] | None = None,
    cross_theme_snippets: dict[str, list[dict[str, Any]]] | None = None,
    paper_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    gene_narratives: dict[str, Any] | None = None,
) -> set[str]:
    """Collect all PMIDs from literature context sources into a whitelist.

    Returns:
        Set of PMID strings (digits only, e.g. {"12345678"}).
    """
    pmids: set[str] = set()

    def _collect_from_list_of_dicts(data: dict | None) -> None:
        """Extract pmid from dict[key, list[{pmid: ...}]]."""
        if not data:
            return
        for entries in data.values():
            if isinstance(entries, list):
                for entry in entries:
                    p = entry.get("pmid", "") if isinstance(entry, dict) else ""
                    if p:
                        pmids.add(str(p))

    _collect_from_list_of_dicts(gaf_pmids)
    _collect_from_list_of_dicts(gaf_abstracts)
    _collect_from_list_of_dicts(hub_gene_abstracts)
    _collect_from_list_of_dicts(snippet_evidence)
    _collect_from_list_of_dicts(hub_gene_snippets)
    _collect_from_list_of_dicts(cross_theme_snippets)
    _collect_from_list_of_dicts(paper_abstracts)

    # co_annotation_snippets: dict[int, dict[str, list[{pmid: ...}]]]
    if co_annotation_snippets:
        for theme_genes in co_annotation_snippets.values():
            if isinstance(theme_genes, dict):
                for gene_entries in theme_genes.values():
                    if isinstance(gene_entries, list):
                        for entry in gene_entries:
                            p = entry.get("pmid", "") if isinstance(entry, dict) else ""
                            if p:
                                pmids.add(str(p))

    # gene_narratives: extract PMIDs from narrative text via regex
    if gene_narratives:
        for section in ("hub_genes", "theme_genes", "co_annotations"):
            section_data = gene_narratives.get(section, {})
            if isinstance(section_data, dict):
                for value in section_data.values():
                    if isinstance(value, str):
                        for m in _PMID_RE.finditer(value):
                            pmids.add(m.group(1))
                    elif isinstance(value, dict):
                        # theme_genes: {theme_idx: {gene: narrative}}
                        for narr in value.values():
                            if isinstance(narr, str):
                                for m in _PMID_RE.finditer(narr):
                                    pmids.add(m.group(1))

    return pmids


def validate_pmids_in_explanation(
    explanation: dict[str, Any],
    pmid_whitelist: set[str],
) -> tuple[list[str], dict[str, set[str]]]:
    """Validate PMIDs in explanation JSON against the literature whitelist.

    Returns:
        Tuple of (warnings list, hallucinated_by_location dict).
        hallucinated_by_location maps location keys to sets of bad PMID strings.
    """
    warnings: list[str] = []
    hallucinated: dict[str, set[str]] = {}

    def _check_text(text: str, location: str, context_label: str) -> None:
        for m in _PMID_RE.finditer(text):
            pmid = m.group(1)
            if len(pmid) >= 9:
                warnings.append(
                    f"{context_label}: PMID:{pmid} has invalid format "
                    f"(9+ digits, likely hallucinated)"
                )
                hallucinated.setdefault(location, set()).add(pmid)
            elif pmid not in pmid_whitelist:
                warnings.append(
                    f"{context_label}: PMID:{pmid} not in provided literature context"
                )
                hallucinated.setdefault(location, set()).add(pmid)

    # Theme narratives and key_genes
    for theme in explanation.get("themes", []):
        idx = theme.get("theme_index", 0)
        narrative = theme.get("narrative", "")
        if narrative:
            _check_text(narrative, f"theme_{idx}_narrative", f"Theme {idx} narrative")

        for kg in theme.get("key_genes", []):
            gene = kg.get("gene", "unknown")
            desc = kg.get("description", "")
            if desc:
                _check_text(desc, f"theme_{idx}_key_gene_{gene}",
                            f"Theme {idx} key_gene '{gene}'")

    # Hub genes
    for hg in explanation.get("hub_genes", []):
        gene = hg.get("gene", "unknown")
        narr = hg.get("narrative", "")
        if narr:
            _check_text(narr, f"hub_gene_{gene}", f"Hub gene '{gene}'")

    # Overall summary
    for i, para in enumerate(explanation.get("overall_summary", [])):
        if para:
            _check_text(para, f"overall_summary_{i}", f"Overall summary paragraph {i}")

    return warnings, hallucinated


def correct_claim_types(
    explanation: dict[str, Any],
    pmid_whitelist: set[str],
) -> list[str]:
    """Correct claim_type based on PMID presence. Mutates explanation in place.

    EXTERNAL = cites a whitelisted PMID; INFERENCE = no whitelisted PMID.

    Returns:
        List of correction messages for logging.
    """
    corrections: list[str] = []

    for theme in explanation.get("themes", []):
        idx = theme.get("theme_index", 0)
        for kg in theme.get("key_genes", []):
            gene = kg.get("gene", "unknown")
            desc = kg.get("description", "")
            cited_pmids = set(_PMID_RE.findall(desc))
            has_whitelisted = bool(cited_pmids & pmid_whitelist)
            expected = "EXTERNAL" if has_whitelisted else "INFERENCE"
            current = kg.get("claim_type", "INFERENCE")
            if current != expected:
                kg["claim_type"] = expected
                corrections.append(
                    f"Theme {idx} key_gene '{gene}': {current} -> {expected}"
                )

    for hg in explanation.get("hub_genes", []):
        gene = hg.get("gene", "unknown")
        narr = hg.get("narrative", "")
        cited_pmids = set(_PMID_RE.findall(narr))
        has_whitelisted = bool(cited_pmids & pmid_whitelist)
        expected = "EXTERNAL" if has_whitelisted else "INFERENCE"
        current = hg.get("claim_type", "INFERENCE")
        if current != expected:
            hg["claim_type"] = expected
            corrections.append(
                f"Hub gene '{gene}': {current} -> {expected}"
            )

    return corrections


def strip_hallucinated_pmids(
    explanation: dict[str, Any],
    hallucinated_by_location: dict[str, set[str]],
) -> int:
    """Remove hallucinated PMIDs from explanation text fields. Mutates in place.

    Returns:
        Count of PMIDs stripped.
    """
    if not hallucinated_by_location:
        return 0

    count = 0

    def _strip_from_text(text: str, bad_pmids: set[str]) -> tuple[str, int]:
        n = 0
        for pmid in bad_pmids:
            pattern = re.compile(rf"\s*PMID:{re.escape(pmid)}")
            text, subs = pattern.subn("", text)
            n += subs
        # Clean double spaces
        text = re.sub(r"  +", " ", text)
        return text.strip(), n

    for theme in explanation.get("themes", []):
        idx = theme.get("theme_index", 0)

        loc_key = f"theme_{idx}_narrative"
        if loc_key in hallucinated_by_location:
            theme["narrative"], n = _strip_from_text(
                theme.get("narrative", ""), hallucinated_by_location[loc_key]
            )
            count += n

        for kg in theme.get("key_genes", []):
            gene = kg.get("gene", "unknown")
            loc_key = f"theme_{idx}_key_gene_{gene}"
            if loc_key in hallucinated_by_location:
                kg["description"], n = _strip_from_text(
                    kg.get("description", ""), hallucinated_by_location[loc_key]
                )
                count += n

    for hg in explanation.get("hub_genes", []):
        gene = hg.get("gene", "unknown")
        loc_key = f"hub_gene_{gene}"
        if loc_key in hallucinated_by_location:
            hg["narrative"], n = _strip_from_text(
                hg.get("narrative", ""), hallucinated_by_location[loc_key]
            )
            count += n

    for i, para in enumerate(explanation.get("overall_summary", [])):
        loc_key = f"overall_summary_{i}"
        if loc_key in hallucinated_by_location:
            explanation["overall_summary"][i], n = _strip_from_text(
                para, hallucinated_by_location[loc_key]
            )
            count += n

    return count


def _build_correction_prompt(
    explanation: dict[str, Any],
    pmid_warnings: list[str],
    pmid_whitelist: set[str],
) -> tuple[str, str]:
    """Build a focused correction prompt for hallucinated PMIDs.

    Returns:
        Tuple of (system_prompt, user_prompt).
    """
    prompt_config = _load_prompt("go_explanation_correction.prompt.yaml")
    system_prompt = prompt_config["system_prompt"]
    user_prompt_template = prompt_config["user_prompt"]

    # Compact JSON (saves tokens)
    explanation_json = json.dumps(explanation, separators=(",", ":"))

    # Error list
    error_list = "\n".join(f"- {w}" for w in pmid_warnings)

    # Valid PMIDs (cap at 200 to keep prompt small)
    sorted_pmids = sorted(pmid_whitelist)
    if len(sorted_pmids) > 200:
        valid_pmids = ", ".join(sorted_pmids[:200]) + f" ... ({len(sorted_pmids)} total)"
    else:
        valid_pmids = ", ".join(sorted_pmids) if sorted_pmids else "(none)"

    user_prompt = user_prompt_template.format(
        explanation_json=explanation_json,
        error_list=error_list,
        valid_pmids=valid_pmids,
    )

    return system_prompt, user_prompt


def _go_id_to_link(go_id: str) -> str:
    """Convert a bare GO ID to a markdown hyperlink."""
    if not go_id:
        return ""
    purl_id = go_id.replace(":", "_")
    purl = f"http://purl.obolibrary.org/obo/{purl_id}"
    return f"[{go_id}]({purl})"
