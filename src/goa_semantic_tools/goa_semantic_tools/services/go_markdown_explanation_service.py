"""
GO Markdown Explanation Service

LLM-based markdown report generation for GO enrichment results (Phase 2, markdown format).
Generates provenance-labeled explanations with [DATA], [INFERENCE], [EXTERNAL], [GO-HIERARCHY] tags.
"""
import os
import re
from pathlib import Path
from typing import Any

import yaml
from cellsem_llm_client.agents.agent_connection import LiteLLMAgent


def generate_markdown_explanation(
    enrichment_output: dict[str, Any],
    model: str = "gpt-4o",
    api_key: str | None = None,
    temperature: float = 0.1,
    max_tokens: int = 8000,
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
    print("\n[1/3] Loading prompt configuration...")
    prompt_config = _load_prompt("go_explanation.prompt.yaml")
    system_prompt = prompt_config["system_prompt"]
    user_prompt_template = prompt_config["user_prompt"]

    # Get API key
    if api_key is None:
        api_key = _get_api_key_for_model(model)

    print(f"  Model: {model}")
    print(f"  Temperature: {temperature}")
    print(f"  Max tokens: {max_tokens}")
    print(f"  Output format: Markdown with provenance tags")

    # Format enrichment data for LLM
    print("\n[2/3] Formatting enrichment data for LLM...")
    enrichment_context = _format_enrichment_for_llm(enrichment_output)

    # Modify user prompt to request markdown output
    user_prompt = user_prompt_template.format(enrichment_data=enrichment_context)
    user_prompt += "\n\n**IMPORTANT**: Generate your response as a well-formatted Markdown document with clear sections and provenance tags ([DATA], [INFERENCE], [EXTERNAL], [GO-HIERARCHY]) on every claim. Do not return JSON."

    print(f"  Themes to explain: {len(themes)}")
    print(f"  Enrichment leaves: {len(enrichment_leaves)}")
    print(f"  Hub genes: {len(enrichment_output.get('hub_genes', {}))}")
    print(f"  Context size: {len(enrichment_context)} characters")

    # Call LLM WITHOUT schema enforcement
    print("\n[3/3] Calling LLM for markdown generation...")
    agent = LiteLLMAgent(model=model, api_key=api_key, max_tokens=max_tokens)

    try:
        result = agent.query_unified(
            message=user_prompt,
            system_message=system_prompt,
            track_usage=True,
        )

        print(f"  LLM call successful")
        if result.usage:
            print(f"  Input tokens: {result.usage.input_tokens:,}")
            print(f"  Output tokens: {result.usage.output_tokens:,}")
            if result.usage.estimated_cost_usd:
                print(f"  Estimated cost: ${result.usage.estimated_cost_usd:.4f} USD")

        markdown_output = result.text or ""

        print("\n[Post-processing]")
        # Add hyperlinks to GO IDs and PMIDs
        markdown_output = _add_go_term_hyperlinks(markdown_output, enrichment_output)
        markdown_output = _add_pmid_hyperlinks(markdown_output)

        # Validate GO IDs and PMIDs to detect hallucinations
        _validate_citations(markdown_output, enrichment_output)

        # Count provenance tags
        _count_provenance_tags(markdown_output)

        print("\n" + "=" * 80)
        print(f"Markdown explanation generation complete!")
        print(f"  Output length: {len(markdown_output)} characters")
        print("=" * 80)

        return markdown_output

    except Exception as e:
        print(f"  ❌ LLM call failed: {e}")
        raise


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


def _format_enrichment_for_llm(enrichment_output: dict[str, Any]) -> str:
    """
    Format enrichment output as readable text for LLM.

    Converts structured JSON to natural text that explains:
    - Study parameters
    - Hub genes and their theme participation
    - Hierarchical themes with anchor and specific terms
    - Enrichment leaves (most specific terms)

    Args:
        enrichment_output: Phase 1 enrichment output (new format)

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

        for gene, data in list(hub_genes.items())[:15]:  # Top 15 hub genes
            theme_count = data.get("theme_count", 0)
            theme_names = data.get("themes", [])[:5]  # Top 5 themes
            lines.append(f"## {gene} ({theme_count} themes)")
            lines.append(f"- Themes: {', '.join(theme_names)}")
            if len(data.get("themes", [])) > 5:
                lines.append(f"- ... and {len(data['themes']) - 5} more")
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
            all_genes = theme.get("all_genes", [])

            lines.append(f"## Theme {i+1}: {anchor.get('name', 'Unknown')}")
            lines.append(f"- GO ID: {anchor.get('go_id', '')}")
            lines.append(f"- Namespace: {anchor.get('namespace', '')}")
            lines.append(f"- FDR: {anchor.get('fdr', 0):.2e}")
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
                        f"{len(specific.get('genes', []))} genes"
                    )
                if len(specific_terms) > 5:
                    lines.append(f"  - ... and {len(specific_terms) - 5} more")
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
