"""
GO Explanation Service

LLM-based natural language explanation generation for GO enrichment results (Phase 2).
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from cellsem_llm_client.agents.agent_connection import LiteLLMAgent


def generate_explanations(
    enrichment_output: dict[str, Any],
    model: str = "gpt-4o",
    api_key: str | None = None,
    temperature: float = 0.1,
    max_tokens: int = 3000,
) -> dict[str, Any]:
    """
    Generate natural language explanations for GO enrichment results using LLM.

    This is the main entry point for Phase 2 explanation generation. It:
    1. Loads co-located prompt YAML
    2. Formats enrichment data for LLM consumption
    3. Calls LLM with structured output (JSON schema enforcement)
    4. Returns explanations matching go_explanation_output schema

    Args:
        enrichment_output: Phase 1 output (from run_go_enrichment)
        model: LLM model identifier. Must support structured outputs.
            Supported models:
            - OpenAI: "gpt-4o", "gpt-4o-mini" (NOT "gpt-4")
            - Anthropic: "claude-sonnet-4-20250514", "claude-opus-4-20250514"
        api_key: API key for LLM provider (if None, uses env vars)
        temperature: LLM temperature (default: 0.1 for consistency)
        max_tokens: Maximum tokens for LLM response

    Returns:
        Dictionary matching go_explanation_output.schema.json:
        {
            'enrichment_data': {...},  # Original Phase 1 output
            'explanations': [          # Per-cluster explanations
                {
                    'cluster_index': 0,
                    'cluster_name': '...',
                    'summary': '...',
                    'detailed_explanation': '...',
                    'key_insights': [...],
                    'key_genes': [...],
                    'statistical_context': '...'
                },
                ...
            ],
            'overall_summary': '...',  # Synthesized narrative
            'generation_metadata': {...}
        }

    Raises:
        FileNotFoundError: If prompt file not found
        ValueError: If input is invalid or API key missing
        Exception: If LLM call or validation fails

    Example:
        >>> result = run_go_enrichment(["TP53", "BRCA1"], "human")
        >>> explanations = generate_explanations(
        ...     enrichment_output=result,
        ...     model="gpt-4"
        ... )
        >>> print(explanations['explanations'][0]['summary'])
    """
    # Validate input
    if not enrichment_output:
        raise ValueError("enrichment_output cannot be empty")

    if "clusters" not in enrichment_output or "metadata" not in enrichment_output:
        raise ValueError("enrichment_output must have 'clusters' and 'metadata' keys")

    clusters = enrichment_output["clusters"]
    if not clusters:
        # No clusters - return minimal explanation output
        return _empty_explanation(enrichment_output, model)

    print("=" * 80)
    print("GO Explanation Generation - Phase 2")
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

    # Format enrichment data for LLM
    print("\n[2/4] Formatting enrichment data for LLM...")
    enrichment_context = _format_enrichment_for_llm(enrichment_output)
    user_prompt = user_prompt_template.format(enrichment_data=enrichment_context)

    print(f"  Clusters to explain: {len(clusters)}")
    print(f"  Context size: {len(enrichment_context)} characters")

    # Load explanation schema
    print("\n[3/4] Calling LLM for explanation generation...")
    schema_path = Path(__file__).parent.parent / "schemas" / "go_explanation_output.schema.json"
    with open(schema_path) as f:
        explanation_schema = json.load(f)

    # Call LLM with structured output
    agent = LiteLLMAgent(model=model, api_key=api_key, max_tokens=max_tokens)

    try:
        result = agent.query_unified(
            message=user_prompt,
            system_message=system_prompt,
            schema=explanation_schema,
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

    # Build output
    print("\n[4/4] Building output structure...")
    if result.model is None:
        raise RuntimeError("LLM response validation failed - no model instance returned")

    # Convert Pydantic model to dict
    explanation_dict = result.model.model_dump()

    # Add metadata
    explanation_dict["generation_metadata"] = {
        "model": model,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "clusters_explained": len(explanation_dict.get("explanations", [])),
    }

    # Add enrichment data
    explanation_dict["enrichment_data"] = enrichment_output

    print("\n" + "=" * 80)
    print(f"Explanation generation complete!")
    print(f"  Clusters explained: {explanation_dict['generation_metadata']['clusters_explained']}")
    print(f"  Overall summary length: {len(explanation_dict.get('overall_summary', ''))} characters")
    print("=" * 80)

    return explanation_dict


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
                # Format evidence codes
                evidence_codes = [ev["code"] for ev in annot.get("evidence", [])]
                evidence_str = ", ".join(evidence_codes) if evidence_codes else "unknown"
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


def _empty_explanation(enrichment_output: dict[str, Any], model: str) -> dict[str, Any]:
    """
    Build empty explanation output when no clusters to explain.

    Args:
        enrichment_output: Phase 1 enrichment output (with no clusters)
        model: Model name for metadata

    Returns:
        Minimal explanation output matching schema
    """
    return {
        "enrichment_data": enrichment_output,
        "explanations": [],
        "overall_summary": (
            "No significant GO enrichment was found for the provided gene list. "
            "This could indicate that the genes do not share common functional themes, "
            "or that the sample size is too small for statistical significance."
        ),
        "generation_metadata": {
            "model": model,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "clusters_explained": 0,
        },
    }
