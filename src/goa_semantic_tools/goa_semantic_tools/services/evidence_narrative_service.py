"""
Per-Gene Evidence Narrative Service (Phase 1c)

Generates focused mechanistic narratives for individual genes via parallel
LLM subagent calls. Each gene gets only its own evidence — snippets, GAF
annotations, abstracts — and produces a 1-2 sentence narrative with inline
PMID citations.

These pre-digested narratives replace raw snippet dumps in the synthesiser
context, enabling the Phase 2 LLM to incorporate evidence it would otherwise
ignore in a ~90K character blob.
"""
from __future__ import annotations

import concurrent.futures
import os
from pathlib import Path
from typing import Any

import yaml
from cellsem_llm_client.agents.agent_connection import LiteLLMAgent

_MAX_PARALLEL_WORKERS = 8
_NARRATIVE_MAX_TOKENS = 300
_CALL_TIMEOUT = 30  # seconds per LLM call


def _load_prompt() -> dict[str, str]:
    """Load the evidence_narrative prompt YAML."""
    prompt_path = Path(__file__).parent / "evidence_narrative.prompt.yaml"
    with open(prompt_path) as f:
        return yaml.safe_load(f)


def _build_gene_evidence_context(
    gene: str,
    theme_context: str,
    snippets: list[dict[str, Any]] | None = None,
    abstracts: list[dict[str, Any]] | None = None,
    gaf_annotations: list[str] | None = None,
) -> str:
    """Assemble all evidence for one gene into a focused prompt section.

    Args:
        gene: Gene symbol
        theme_context: Brief context about the gene's role (e.g. theme names)
        snippets: ASTA snippet dicts for this gene
        abstracts: Paper dicts with abstracts for this gene
        gaf_annotations: GAF annotation strings (e.g. "FST→activin binding [GO:0048185]")

    Returns:
        Formatted evidence string for injection into the user prompt.
    """
    parts: list[str] = []

    if gaf_annotations:
        parts.append("GO Annotations:")
        for ann in gaf_annotations[:10]:
            parts.append(f"  - {ann}")

    if snippets:
        parts.append("Literature Snippets:")
        for s in snippets[:5]:
            pmid = s.get("pmid", "")
            title = s.get("title", "")
            text = s.get("snippet_text", "")
            pmid_label = f"PMID:{pmid}" if pmid else s.get("paperId", "unknown")
            preview = text[:500] + "..." if len(text) > 500 else text
            parts.append(f"  [{pmid_label}] {title}")
            parts.append(f"  {preview}")

    if abstracts:
        parts.append("Abstracts:")
        for a in abstracts[:3]:
            pmid = a.get("pmid", "")
            title = a.get("title", "")
            abstract = a.get("abstract", "")
            preview = abstract[:400] + "..." if len(abstract) > 400 else abstract
            parts.append(f"  [PMID:{pmid}] {title}")
            if preview:
                parts.append(f"  {preview}")

    if not parts:
        parts.append("No literature evidence available. Use latent knowledge if possible.")

    return "\n".join(parts)


def _call_narrative_agent(
    gene: str,
    context: str,
    evidence: str,
    system_prompt: str,
    user_prompt_template: str,
    model: str,
    api_key: str,
) -> tuple[str, dict[str, Any] | None]:
    """Make a single LLM call to generate a gene narrative.

    Args:
        gene: Gene symbol
        context: Theme context string
        evidence: Formatted evidence string
        system_prompt: System prompt from YAML
        user_prompt_template: User prompt template from YAML
        model: LLM model identifier
        api_key: API key

    Returns:
        (narrative_text, usage_dict_or_None)
    """
    user_prompt = user_prompt_template.format(
        gene=gene,
        context=context,
        evidence=evidence,
    )

    agent = LiteLLMAgent(model=model, api_key=api_key, max_tokens=_NARRATIVE_MAX_TOKENS)
    result = agent.query_unified(
        message=user_prompt,
        system_message=system_prompt,
        track_usage=True,
    )

    narrative = (result.text or "").strip()
    usage = None
    if result.usage:
        usage = {
            "input_tokens": result.usage.input_tokens,
            "output_tokens": result.usage.output_tokens,
            "estimated_cost_usd": result.usage.estimated_cost_usd,
        }

    return narrative, usage


def _collect_gene_snippets(
    gene: str,
    snippet_evidence: dict[int, list[dict[str, Any]]] | None,
    hub_gene_snippets: dict[str, list[dict[str, Any]]] | None,
    co_annotation_snippets: dict[int, dict[str, list[dict[str, Any]]]] | None,
    cross_theme_snippets: dict[str, list[dict[str, Any]]] | None,
    cross_theme_gaf_snippets: dict[str, list[dict[str, Any]]] | None,
    theme_idx: int | None = None,
) -> list[dict[str, Any]]:
    """Collect all available snippets for a gene across all sources.

    Args:
        gene: Gene symbol
        snippet_evidence: Per-theme GAF-scoped snippets
        hub_gene_snippets: Hub gene unscoped snippets
        co_annotation_snippets: Per-theme co-annotation snippets
        cross_theme_snippets: Cross-theme co-annotation snippets
        cross_theme_gaf_snippets: Cross-theme GAF PMID snippets
        theme_idx: If set, also collect theme-specific snippets

    Returns:
        Deduplicated list of snippet dicts for this gene.
    """
    seen_pmids: set[str] = set()
    collected: list[dict[str, Any]] = []

    def _add(snips: list[dict[str, Any]]) -> None:
        for s in snips:
            key = s.get("pmid", "") or s.get("paperId", "") or s.get("snippet_text", "")[:80]
            if key not in seen_pmids:
                seen_pmids.add(key)
                collected.append(s)

    # Hub gene snippets
    if hub_gene_snippets and gene in hub_gene_snippets:
        _add(hub_gene_snippets[gene])

    # Cross-theme co-annotation snippets
    if cross_theme_snippets and gene in cross_theme_snippets:
        _add(cross_theme_snippets[gene])

    # Cross-theme GAF PMID snippets
    if cross_theme_gaf_snippets and gene in cross_theme_gaf_snippets:
        _add(cross_theme_gaf_snippets[gene])

    # Theme-specific GAF-scoped snippets (check if gene mentioned in snippet)
    if theme_idx is not None and snippet_evidence and theme_idx in snippet_evidence:
        for s in snippet_evidence[theme_idx]:
            text = s.get("snippet_text", "")
            if gene.upper() in text.upper():
                key = s.get("pmid", "") or s.get("paperId", "")
                if key and key not in seen_pmids:
                    seen_pmids.add(key)
                    collected.append(s)

    # Theme-specific co-annotation snippets
    if theme_idx is not None and co_annotation_snippets and theme_idx in co_annotation_snippets:
        gene_snips = co_annotation_snippets[theme_idx].get(gene, [])
        _add(gene_snips)

    return collected


def _collect_gene_gaf_annotations(
    gene: str,
    gaf_pmids: dict[int, list[dict[str, Any]]] | None,
    theme_idx: int | None = None,
) -> list[str]:
    """Collect GAF annotation strings for a gene.

    Returns strings like "FST→activin binding [GO:0048185] PMID:1234567"
    """
    if not gaf_pmids:
        return []

    annotations: list[str] = []
    seen: set[str] = set()

    indices = [theme_idx] if theme_idx is not None else list(gaf_pmids.keys())
    for idx in indices:
        if idx not in gaf_pmids:
            continue
        for entry in gaf_pmids[idx]:
            pmid = entry.get("pmid", "")
            gene_go_named = entry.get("gene_go_named", {})
            if gene in gene_go_named:
                for term_name in gene_go_named[gene]:
                    ann = f"{gene}→{term_name}"
                    if pmid:
                        ann += f" PMID:{pmid}"
                    if ann not in seen:
                        seen.add(ann)
                        annotations.append(ann)

    return annotations


def _collect_gene_abstracts(
    gene: str,
    gaf_abstracts: dict[int, list[dict[str, Any]]] | None,
    hub_gene_abstracts: dict[str, list[dict[str, Any]]] | None,
    cross_theme_gaf_abstracts: dict[str, list[dict[str, Any]]] | None,
    theme_idx: int | None = None,
) -> list[dict[str, Any]]:
    """Collect abstracts relevant to a gene."""
    seen_pmids: set[str] = set()
    collected: list[dict[str, Any]] = []

    def _add(papers: list[dict[str, Any]]) -> None:
        for p in papers:
            pmid = p.get("pmid", "")
            if pmid and pmid not in seen_pmids:
                seen_pmids.add(pmid)
                collected.append(p)

    # Hub gene abstracts
    if hub_gene_abstracts and gene in hub_gene_abstracts:
        _add(hub_gene_abstracts[gene])

    # Cross-theme GAF abstracts
    if cross_theme_gaf_abstracts and gene in cross_theme_gaf_abstracts:
        _add(cross_theme_gaf_abstracts[gene])

    # Theme-specific GAF abstracts
    if theme_idx is not None and gaf_abstracts and theme_idx in gaf_abstracts:
        _add(gaf_abstracts[theme_idx])

    return collected


def generate_gene_narratives(
    enrichment_output: dict,
    gaf_pmids: dict | None = None,
    gaf_abstracts: dict | None = None,
    snippet_evidence: dict | None = None,
    hub_gene_snippets: dict | None = None,
    hub_gene_abstracts: dict | None = None,
    co_annotation_snippets: dict | None = None,
    cross_theme_snippets: dict | None = None,
    cross_theme_gaf_abstracts: dict | None = None,
    cross_theme_gaf_snippets: dict | None = None,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    max_workers: int = _MAX_PARALLEL_WORKERS,
) -> dict:
    """Generate per-gene mechanistic narratives via parallel LLM calls.

    Processes three categories of genes:
    1. Hub genes — cross-theme coordinators with all their evidence
    2. Per-theme key genes — top-ranked genes per theme
    3. Co-annotation genes — genes linking 2+ GO processes

    Each gene gets a focused LLM call with only its evidence, producing
    a 1-2 sentence mechanistic narrative with inline PMID citations.

    Args:
        enrichment_output: Phase 1 enrichment output
        gaf_pmids: {theme_idx: [{pmid, gene_go_named, ...}]}
        gaf_abstracts: {theme_idx: [{pmid, title, abstract, ...}]}
        snippet_evidence: {theme_idx: [snippet_dicts]}
        hub_gene_snippets: {gene: [snippet_dicts]}
        hub_gene_abstracts: {gene: [{pmid, title, abstract}]}
        co_annotation_snippets: {theme_idx: {gene: [snippet_dicts]}}
        cross_theme_snippets: {gene: [snippet_dicts]}
        cross_theme_gaf_abstracts: {gene: [{pmid, title, abstract}]}
        cross_theme_gaf_snippets: {gene: [snippet_dicts]}
        model: LLM model for subagent calls (default: gpt-4o-mini for cost)
        api_key: API key (auto-detected if None)
        max_workers: Max parallel LLM calls

    Returns:
        {
            "hub_genes": {gene: narrative_str, ...},
            "theme_genes": {theme_idx: {gene: narrative_str, ...}, ...},
            "co_annotations": {theme_idx: {gene: narrative_str, ...}, ...},
            "usage": {"total_cost": float, "total_input_tokens": int,
                      "total_output_tokens": int, "n_calls": int}
        }
    """
    themes = enrichment_output.get("themes", [])
    hub_genes_data = enrichment_output.get("hub_genes", {})

    # Resolve API key
    if api_key is None:
        api_key = _get_api_key(model)

    # Load prompt
    prompt_config = _load_prompt()
    system_prompt = prompt_config["system_prompt"]
    user_prompt_template = prompt_config["user_prompt"]

    # Import rank function for per-theme gene selection
    from .go_markdown_explanation_service import rank_genes_for_theme

    # Build all tasks: (key, gene, context, evidence)
    tasks: list[tuple[tuple, str, str, str]] = []

    # 1. Hub gene tasks
    hub_genes_sorted = sorted(
        hub_genes_data.items(),
        key=lambda x: x[1].get("theme_count", 0),
        reverse=True,
    )[:20]

    for gene, data in hub_genes_sorted:
        theme_names = data.get("themes", [])[:5]
        context = f"Hub gene appearing in {data.get('theme_count', 0)} themes: {', '.join(theme_names)}"

        snippets = _collect_gene_snippets(
            gene, snippet_evidence, hub_gene_snippets,
            co_annotation_snippets, cross_theme_snippets,
            cross_theme_gaf_snippets,
        )
        annotations = _collect_gene_gaf_annotations(gene, gaf_pmids)
        abstracts = _collect_gene_abstracts(
            gene, gaf_abstracts, hub_gene_abstracts, cross_theme_gaf_abstracts,
        )

        evidence = _build_gene_evidence_context(
            gene, context, snippets=snippets,
            abstracts=abstracts, gaf_annotations=annotations,
        )
        tasks.append((("hub", gene), gene, context, evidence))

    # 2. Per-theme key gene tasks
    for theme_idx, theme in enumerate(themes):
        ranked = rank_genes_for_theme(theme, hub_genes_data, top_n=5)
        anchor_name = theme.get("anchor_term", {}).get("name", "")

        for entry in ranked:
            gene = entry["gene"]
            # Skip if already covered as hub gene
            if gene in dict(hub_genes_sorted):
                continue

            context = f"Key gene in theme '{anchor_name}' (theme {theme_idx})"

            snippets = _collect_gene_snippets(
                gene, snippet_evidence, hub_gene_snippets,
                co_annotation_snippets, cross_theme_snippets,
                cross_theme_gaf_snippets,
                theme_idx=theme_idx,
            )
            annotations = _collect_gene_gaf_annotations(gene, gaf_pmids, theme_idx=theme_idx)
            abstracts = _collect_gene_abstracts(
                gene, gaf_abstracts, hub_gene_abstracts, cross_theme_gaf_abstracts,
                theme_idx=theme_idx,
            )

            evidence = _build_gene_evidence_context(
                gene, context, snippets=snippets,
                abstracts=abstracts, gaf_annotations=annotations,
            )
            tasks.append((("theme", theme_idx, gene), gene, context, evidence))

    # 3. Co-annotation gene tasks
    if co_annotation_snippets:
        for theme_idx, gene_snips in co_annotation_snippets.items():
            for gene in gene_snips:
                # Skip if already covered
                if gene in dict(hub_genes_sorted):
                    continue
                if any(t[0] == ("theme", theme_idx, gene) for t in tasks):
                    continue

                anchor_name = ""
                if isinstance(theme_idx, int) and theme_idx < len(themes):
                    anchor_name = themes[theme_idx].get("anchor_term", {}).get("name", "")

                context = f"Co-annotated gene in theme '{anchor_name}' (theme {theme_idx})"

                snippets = _collect_gene_snippets(
                    gene, snippet_evidence, hub_gene_snippets,
                    co_annotation_snippets, cross_theme_snippets,
                    cross_theme_gaf_snippets,
                    theme_idx=theme_idx,
                )
                annotations = _collect_gene_gaf_annotations(gene, gaf_pmids, theme_idx=theme_idx)
                abstracts = _collect_gene_abstracts(
                    gene, gaf_abstracts, hub_gene_abstracts, cross_theme_gaf_abstracts,
                    theme_idx=theme_idx,
                )

                evidence = _build_gene_evidence_context(
                    gene, context, snippets=snippets,
                    abstracts=abstracts, gaf_annotations=annotations,
                )
                tasks.append((("co_annot", theme_idx, gene), gene, context, evidence))

    if not tasks:
        return {
            "hub_genes": {},
            "theme_genes": {},
            "co_annotations": {},
            "usage": {"total_cost": 0.0, "total_input_tokens": 0, "total_output_tokens": 0, "n_calls": 0},
        }

    print(f"\n  Generating {len(tasks)} gene narrative(s) via {model}...")

    # Execute all in parallel
    results_map: dict[tuple, str] = {}
    total_usage = {"total_cost": 0.0, "total_input_tokens": 0, "total_output_tokens": 0, "n_calls": 0}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_key = {
            pool.submit(
                _call_narrative_agent,
                gene, context, evidence,
                system_prompt, user_prompt_template,
                model, api_key,
            ): key
            for key, gene, context, evidence in tasks
        }

        for future in concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            try:
                narrative, usage = future.result(timeout=_CALL_TIMEOUT)
                results_map[key] = narrative
                if usage:
                    total_usage["total_cost"] += usage.get("estimated_cost_usd", 0) or 0
                    total_usage["total_input_tokens"] += usage.get("input_tokens", 0) or 0
                    total_usage["total_output_tokens"] += usage.get("output_tokens", 0) or 0
                    total_usage["n_calls"] += 1
            except Exception as e:
                gene_name = key[1] if len(key) > 1 else str(key)
                print(f"  ⚠ Narrative failed for {gene_name}: {e}")
                results_map[key] = ""

    # Organize results
    hub_narratives: dict[str, str] = {}
    theme_narratives: dict[int, dict[str, str]] = {}
    co_annot_narratives: dict[int, dict[str, str]] = {}

    for key, narrative in results_map.items():
        if not narrative:
            continue
        if key[0] == "hub":
            hub_narratives[key[1]] = narrative
        elif key[0] == "theme":
            theme_idx = key[1]
            gene = key[2]
            theme_narratives.setdefault(theme_idx, {})[gene] = narrative
        elif key[0] == "co_annot":
            theme_idx = key[1]
            gene = key[2]
            co_annot_narratives.setdefault(theme_idx, {})[gene] = narrative

    print(f"  ✓ Generated {len(hub_narratives)} hub gene + "
          f"{sum(len(v) for v in theme_narratives.values())} theme gene + "
          f"{sum(len(v) for v in co_annot_narratives.values())} co-annotation narrative(s)")
    if total_usage["total_cost"] > 0:
        print(f"  Cost: ${total_usage['total_cost']:.4f} USD "
              f"({total_usage['total_input_tokens']:,} in / {total_usage['total_output_tokens']:,} out)")

    return {
        "hub_genes": hub_narratives,
        "theme_genes": theme_narratives,
        "co_annotations": co_annot_narratives,
        "usage": total_usage,
    }


def _get_api_key(model: str) -> str:
    """Get API key for the given model."""
    if model.startswith("gpt") or model.startswith("o1"):
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY not found")
        return key
    elif model.startswith("claude"):
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY not found")
        return key
    else:
        key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY.")
        return key
