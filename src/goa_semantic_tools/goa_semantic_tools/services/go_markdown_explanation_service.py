"""
GO Markdown Explanation Service

LLM-based markdown report generation for GO enrichment results (Phase 2, markdown format).
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
    max_tokens: int = 3000,
) -> str:
    """
    Generate markdown report explaining GO enrichment results using LLM.

    This bypasses JSON schema validation entirely - the LLM generates
    a markdown report directly. Uses the same structured prompt as the
    JSON mode but asks for markdown output.

    Args:
        enrichment_output: Phase 1 output (from run_go_enrichment)
        model: LLM model identifier. Examples:
            - OpenAI: "gpt-4o", "gpt-4o-mini"
            - Anthropic: "claude-sonnet-4-20250514"
        api_key: API key for LLM provider (if None, uses env vars)
        temperature: LLM temperature (default: 0.1 for consistency)
        max_tokens: Maximum tokens for LLM response

    Returns:
        Markdown-formatted explanation string

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

    if "clusters" not in enrichment_output or "metadata" not in enrichment_output:
        raise ValueError("enrichment_output must have 'clusters' and 'metadata' keys")

    clusters = enrichment_output["clusters"]
    if not clusters:
        # No clusters - return minimal explanation
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
    print(f"  Output format: Markdown")

    # Format enrichment data for LLM
    print("\n[2/3] Formatting enrichment data for LLM...")
    enrichment_context = _format_enrichment_for_llm(enrichment_output)

    # Modify user prompt to request markdown output
    user_prompt = user_prompt_template.format(enrichment_data=enrichment_context)
    user_prompt += "\n\n**IMPORTANT**: Generate your response as a well-formatted Markdown document with clear sections, headers, and formatting. Do not return JSON."

    print(f"  Clusters to explain: {len(clusters)}")
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

    return yaml.safe_load(prompt_path.read_text())


def _get_api_key_for_model(model: str) -> str:
    """
    Get appropriate API key from environment based on model.

    Args:
        model: Model identifier

    Returns:
        API key from environment

    Raises:
        ValueError: If API key not found in environment
    """
    model_lower = model.lower()

    if "gpt" in model_lower or "o1" in model_lower:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable required for OpenAI models")
        return api_key

    if "claude" in model_lower:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable required for Anthropic models")
        return api_key

    if "gemini" in model_lower or "palm" in model_lower:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable required for Google models")
        return api_key

    # Default fallback - try common keys
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            f"No API key found for model {model}. "
            "Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GOOGLE_API_KEY"
        )

    return api_key


def _format_enrichment_for_llm(enrichment_output: dict[str, Any]) -> str:
    """
    Format enrichment output as readable text for LLM.

    Converts structured JSON to natural text that explains:
    - Study parameters and gene list
    - Each cluster with root term, statistics, member terms, contributing genes
    - Direct annotations showing evidence

    Args:
        enrichment_output: Phase 1 enrichment output

    Returns:
        Formatted string for LLM consumption
    """
    metadata = enrichment_output["metadata"]
    clusters = enrichment_output["clusters"]

    # Build context string
    lines = []

    # Study metadata
    lines.append("# Study Overview")
    lines.append(f"- Species: {metadata['species']}")
    lines.append(f"- Input genes: {metadata['input_genes_count']}")
    lines.append(f"- Genes with annotations: {metadata['genes_with_annotations']}")
    lines.append(f"- Total enriched terms: {metadata['total_enriched_terms']}")
    lines.append(f"- FDR threshold: {metadata['fdr_threshold']}")
    lines.append(f"- Clusters: {metadata['clusters_count']}")
    lines.append("")

    # Clusters
    lines.append("# Enrichment Clusters")
    lines.append("")

    for i, cluster in enumerate(clusters):
        root = cluster["root_term"]
        members = cluster["member_terms"]
        genes = cluster["contributing_genes"]

        lines.append(f"## Cluster {i}: {root['name']}")
        lines.append(f"- GO ID: {root['go_id']}")
        lines.append(f"- Namespace: {root['namespace']}")
        lines.append(f"- FDR: {root['fdr']:.2e}")
        lines.append(f"- Fold enrichment: {root['fold_enrichment']:.2f}x")
        lines.append(
            f"- Study genes: {root['study_count']} / {metadata['genes_with_annotations']} "
            f"({100 * root['study_count'] / metadata['genes_with_annotations']:.1f}%)"
        )
        lines.append(f"- Gene symbols: {', '.join(root['study_genes'])}")
        lines.append("")

        # Member terms
        if members:
            lines.append(f"### Member Terms ({len(members)} descendant terms)")

            # Add statistical summary for member terms
            if members:
                fdr_values = [m['fdr'] for m in members]
                fold_values = [m['fold_enrichment'] for m in members]
                study_counts = [m['study_count'] for m in members]

                lines.append(f"**Statistical Summary:**")
                lines.append(f"  - FDR range: {min(fdr_values):.2e} to {max(fdr_values):.2e}")
                lines.append(f"  - Fold enrichment range: {min(fold_values):.2f}x to {max(fold_values):.2f}x")
                lines.append(f"  - Study count range: {min(study_counts)} to {max(study_counts)} genes")
                lines.append("")

            # Show top 5 member terms
            lines.append("**Top member terms:**")
            for member in members[:5]:  # Show top 5 members
                lines.append(
                    f"  - {member['name']} ({member['go_id']}): "
                    f"FDR={member['fdr']:.2e}, "
                    f"Fold={member['fold_enrichment']:.2f}x"
                )
            if len(members) > 5:
                lines.append(f"  - ... and {len(members) - 5} more")
            lines.append("")

        # Contributing genes with annotations
        lines.append(f"### Contributing Genes ({len(genes)} genes)")
        for gene_info in genes[:5]:  # Show top 5 genes
            gene_symbol = gene_info["gene_symbol"]
            annotations = gene_info["direct_annotations"]

            lines.append(f"  - {gene_symbol}:")
            for annot in annotations[:3]:  # Show top 3 annotations per gene
                # Format evidence codes and references
                evidence_items = []
                for ev in annot.get("evidence", []):
                    code = ev.get("code", "")
                    refs = ev.get("references", [])
                    # Filter for PMIDs only
                    pmids = [ref for ref in refs if ref.startswith("PMID:")]
                    if pmids:
                        evidence_items.append(f"{code} ({', '.join(pmids[:2])})")
                    else:
                        evidence_items.append(code)

                evidence_str = ", ".join(evidence_items) if evidence_items else "unknown"
                lines.append(
                    f"    - {annot['go_name']} ({annot['go_id']}), " f"evidence: {evidence_str}"
                )
            if len(annotations) > 3:
                lines.append(f"    - ... and {len(annotations) - 3} more annotations")

        if len(genes) > 5:
            lines.append(f"  - ... and {len(genes) - 5} more genes")

        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def _empty_markdown_explanation(enrichment_output: dict[str, Any], model: str) -> str:
    """
    Build empty markdown explanation when no clusters to explain.

    Args:
        enrichment_output: Phase 1 enrichment output (with no clusters)
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
    Validate GO IDs and PMIDs in LLM output to detect hallucinations.

    Cross-checks all citations mentioned in the markdown against the
    enrichment input data. Prints warnings for any hallucinated citations.

    Args:
        markdown: LLM-generated markdown
        enrichment_output: Phase 1 enrichment output (source of valid citations)
    """
    # Extract all GO IDs from markdown output
    go_id_pattern = r"GO:\d{7}"
    output_go_ids = set(re.findall(go_id_pattern, markdown))

    # Extract all PMIDs from markdown output
    pmid_pattern = r"PMID:(\d+)"
    output_pmids = set(re.findall(pmid_pattern, markdown))

    # Build set of valid GO IDs from enrichment input
    valid_go_ids = set()
    valid_pmids = set()

    for cluster in enrichment_output.get("clusters", []):
        # Root term
        root = cluster.get("root_term", {})
        if root.get("go_id"):
            valid_go_ids.add(root["go_id"])

        # Member terms
        for member in cluster.get("member_terms", []):
            if member.get("go_id"):
                valid_go_ids.add(member["go_id"])

        # Contributing genes annotations
        for gene_info in cluster.get("contributing_genes", []):
            for annot in gene_info.get("direct_annotations", []):
                if annot.get("go_id"):
                    valid_go_ids.add(annot["go_id"])

                # Extract PMIDs from references
                for evidence in annot.get("evidence", []):
                    for ref in evidence.get("references", []):
                        # Reference format: "PMID:12345" or "GO_REF:..."
                        if ref.startswith("PMID:"):
                            pmid_number = ref.replace("PMID:", "")
                            valid_pmids.add(pmid_number)

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

    # Validate PMIDs
    if output_pmids:
        hallucinated_pmids = output_pmids - valid_pmids
        if hallucinated_pmids:
            print("\n" + "⚠" * 40)
            print("WARNING: Potential PMID Hallucinations Detected")
            print("⚠" * 40)
            print(f"\nThe LLM output contains {len(hallucinated_pmids)} PMID(s) that were NOT in the input data:")
            for pmid in sorted(hallucinated_pmids):
                print(f"  - PMID:{pmid}")
            print("\nThese may be:")
            print("  1. Hallucinated by the LLM (incorrect)")
            print("  2. Valid PMIDs from the LLM's training data (plausible but unverified)")
            print("\nPlease verify these PMIDs manually if they support key claims.")
            print("⚠" * 40 + "\n")
        else:
            print("  ✓ PMID validation: All PMIDs in output match input data")
    else:
        print("  ℹ PMID validation: No PMIDs found in LLM output")
