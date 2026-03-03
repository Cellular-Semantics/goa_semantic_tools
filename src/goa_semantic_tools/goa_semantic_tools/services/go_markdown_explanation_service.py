"""
GO Markdown Explanation Service

LLM-based markdown report generation for GO enrichment results (Phase 2, markdown format).
Generates provenance-labeled explanations with [DATA], [INFERENCE], [EXTERNAL], [GO-HIERARCHY] tags.
"""
import json
import os
import re
from pathlib import Path
from typing import Any

import mdformat
import yaml
from cellsem_llm_client.agents.agent_connection import LiteLLMAgent
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


def generate_markdown_explanation(
    enrichment_output: dict[str, Any],
    model: str = "gpt-4o",
    api_key: str | None = None,
    temperature: float = 0.1,
    max_tokens: int | None = None,  # None → auto-derived per model via _get_default_max_tokens
    paper_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    gaf_pmids: dict[int, list[dict[str, Any]]] | None = None,
    hub_gene_abstracts: dict[str, list[dict[str, Any]]] | None = None,
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

    # Format enrichment data for LLM (includes ranked gene candidates per theme)
    print("\n[2/4] Formatting enrichment data for LLM...")
    enrichment_context = _format_enrichment_for_llm(
        enrichment_output,
        paper_abstracts=paper_abstracts,
        gaf_pmids=gaf_pmids,
        hub_gene_abstracts=hub_gene_abstracts,
    )
    user_prompt = user_prompt_template.format(enrichment_data=enrichment_context)

    print(f"  Themes to explain: {len(themes)}")
    print(f"  Enrichment leaves: {len(enrichment_leaves)}")
    print(f"  Hub genes: {len(enrichment_output.get('hub_genes', {}))}")
    print(f"  Context size: {len(enrichment_context)} characters")

    # Call LLM WITH schema enforcement (pass Pydantic model directly — avoids
    # cellsem_llm_client's basic JSON-schema-to-Pydantic converter which can't
    # handle nested arrays of objects and produces missing 'type' keys)
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
    warnings = validate_explanation_json(explanation, enrichment_output)
    for w in warnings:
        print(f"  ⚠ {w}")

    # Render structured JSON → markdown programmatically
    markdown_output = render_explanation_to_markdown(explanation, enrichment_output)

    # Add hyperlinks for any bare GO IDs remaining in narrative text
    markdown_output = _add_go_term_hyperlinks(markdown_output, enrichment_output)

    # Add hyperlinks to inline PMID citations
    markdown_output = _add_pmid_hyperlinks(markdown_output)

    # Normalise markdown formatting (blank lines, spacing, thematic breaks)
    # wrap_width=0 disables line-wrapping so long gene lists / table cells are preserved
    markdown_output = mdformat.text(markdown_output, options={"wrap": "no"})

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


def _format_enrichment_for_llm(
    enrichment_output: dict[str, Any],
    paper_abstracts: dict[int, list[dict[str, Any]]] | None = None,
    gaf_pmids: dict[int, list[dict[str, Any]]] | None = None,
    hub_gene_abstracts: dict[str, list[dict[str, Any]]] | None = None,
) -> str:
    """
    Format enrichment output as readable text for LLM.

    Converts structured JSON to natural text that explains:
    - Study parameters
    - Hub genes and their theme participation (with abstracts if hub_gene_abstracts provided)
    - Hierarchical themes with anchor and specific terms
    - Enrichment leaves (most specific terms)

    Args:
        enrichment_output: Phase 1 enrichment output (new format)
        paper_abstracts: Deprecated. Theme-level paper abstracts (lit-first).
        gaf_pmids: Optional dict mapping theme index to curated GAF PMIDs
            [{pmid, genes_covered}]. Injected as citation anchors per theme.
        hub_gene_abstracts: Optional dict mapping gene → paper dicts with abstracts.
            Injected under each hub gene in the hub genes section.

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

            # Inject hub gene abstracts if available
            if hub_gene_abstracts and gene in hub_gene_abstracts and hub_gene_abstracts[gene]:
                lines.append("### Supporting Literature (cite as PMID:xxxxx for cross-theme claims):")
                for paper in hub_gene_abstracts[gene]:
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

            # GAF-curated citations per theme (preferred)
            if gaf_pmids and i in gaf_pmids and gaf_pmids[i]:
                lines.append("### Available GAF Citations (cite as PMID:xxxxx for gene→GO annotations):")
                for entry in gaf_pmids[i]:
                    pmid = entry.get("pmid", "")
                    genes_covered = entry.get("genes_covered", [])
                    genes_str = ", ".join(genes_covered[:6])
                    if len(genes_covered) > 6:
                        genes_str += f" +{len(genes_covered) - 6} more"
                    lines.append(f"- PMID:{pmid} (covers: {genes_str})")
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

    # Find all GO IDs and replace with hyperlinks
    original = markdown
    markdown = re.sub(r"GO:\d{7}", replace_go_id, markdown)

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


def render_explanation_to_markdown(
    explanation: dict[str, Any],
    enrichment_output: dict[str, Any],
) -> str:
    """
    Programmatically render a structured explanation dict to markdown.

    No LLM involvement — all structure (headers, hyperlinks, [REF:GENE] markers)
    is added deterministically. GO IDs are converted to hyperlinks by this function.

    Args:
        explanation: Structured explanation dict (from LLM via model.model_dump())
        enrichment_output: Phase 1 enrichment output (for theme metadata)

    Returns:
        Markdown string ready for display
    """
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
        f" A complete reference table of all themes follows at the end."
        if n_explained < n_total else ""
    )
    lines.append(
        f"> **Methods note:** Enrichment themes are built using a depth-anchor algorithm. "
        f"Each theme is headed by an **anchor** — an intermediate GO term (depth 4–7 in "
        f"the GO hierarchy) chosen to best group the enriched leaf terms beneath it. "
        f"Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster "
        f"under the anchor.{theme_count_note}\n"
    )
    lines.append("\n")

    # Per-theme sections
    for exp_theme in explanation.get("themes", []):
        idx = exp_theme.get("theme_index", -1)
        if not isinstance(idx, int) or idx < 0 or idx >= len(enrichment_themes):
            continue

        enrichment_theme = enrichment_themes[idx]
        anchor = enrichment_theme.get("anchor_term", {})
        anchor_name = anchor.get("name", "Unknown")
        anchor_go_id = anchor.get("go_id", "")

        # Section header
        lines.append(f"### Theme {idx + 1}: {anchor_name}\n")
        lines.append("\n")

        # Summary line with linked GO ID and anchor confidence
        go_link = _go_id_to_link(anchor_go_id)
        confidence = enrichment_theme.get("anchor_confidence", "")
        confidence_str = f"  · Anchor confidence: **{confidence}**" if confidence else ""
        lines.append(f"**Summary:** {anchor_name} ({go_link}){confidence_str}\n")
        lines.append("\n")

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

    # Full theme reference table (all themes, including uncovered ones)
    if enrichment_themes:
        _NS_ABBREV = {
            "biological_process": "BP",
            "molecular_function": "MF",
            "cellular_component": "CC",
        }
        cap_note = (
            f"Top {n_explained} have narrative summaries above. "
            if n_explained < n_total
            else ""
        )
        lines.append("---\n")
        lines.append("\n")
        lines.append("## All Enrichment Themes (Reference)\n")
        lines.append("\n")
        lines.append(
            f"_{n_total} themes ranked by FDR (most significant first). "
            f"{cap_note}_\n"
        )
        lines.append("\n")
        lines.append("| # | Theme | GO ID | NS | FDR | Genes |\n")
        lines.append("|---|-------|-------|----|-----|-------|\n")
        for i, theme in enumerate(enrichment_themes):
            anchor = theme.get("anchor_term", {})
            name = anchor.get("name", "Unknown")
            go_id = anchor.get("go_id", "")
            ns_full = anchor.get("namespace", "")
            ns = _NS_ABBREV.get(ns_full, ns_full[:2].upper() if ns_full else "?")
            fdr = anchor.get("fdr", 0)
            genes = sorted(anchor.get("genes", []))
            gene_preview = ", ".join(genes[:5])
            if len(genes) > 5:
                gene_preview += f", … ({len(genes)})"
            elif genes:
                gene_preview += f" ({len(genes)})"
            lines.append(f"| {i + 1} | {name} | {go_id} | {ns} | {fdr:.2e} | {gene_preview} |\n")
        lines.append("\n")

    return "".join(lines)


def _go_id_to_link(go_id: str) -> str:
    """Convert a bare GO ID to a markdown hyperlink."""
    if not go_id:
        return ""
    purl_id = go_id.replace(":", "_")
    purl = f"http://purl.obolibrary.org/obo/{purl_id}"
    return f"[{go_id}]({purl})"
