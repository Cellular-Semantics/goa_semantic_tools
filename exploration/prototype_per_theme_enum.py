"""Prototype: per-theme synthesis with dynamic enum via JSON schema manipulation.

Tests whether injecting enum constraints directly into the JSON schema dict
(bypassing Pydantic) eliminates gene/GO ID hallucination at the token level.

Usage:
    uv run python exploration/prototype_per_theme_enum.py
"""

import copy
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

THEME_SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "src/goa_semantic_tools/goa_semantic_tools/schemas/theme_explanation.schema.json"
)


def inject_enums(schema: dict, valid_genes: list[str], valid_go_ids: list[str]) -> dict:
    """Inject enum constraints into a theme explanation JSON schema.

    Modifies the schema dict in-place to constrain:
    - key_genes[].gene → enum of valid genes
    - key_genes[].go_id → enum of valid GO IDs
    - key_insights[].go_id → enum of valid GO IDs

    Also removes the 'pattern' constraint on go_id fields (redundant with enum
    and incompatible with OpenAI strict mode when enum is present).

    Args:
        schema: Theme explanation JSON schema dict (will be modified in-place).
        valid_genes: Sorted list of valid gene symbols for this theme.
        valid_go_ids: Sorted list of valid GO IDs for this theme.

    Returns:
        The modified schema dict (same object, returned for convenience).
    """
    kg_props = schema["properties"]["key_genes"]["items"]["properties"]
    kg_props["gene"]["enum"] = valid_genes
    kg_props["go_id"]["enum"] = valid_go_ids
    kg_props["go_id"].pop("pattern", None)

    ki_props = schema["properties"]["key_insights"]["items"]["properties"]
    ki_props["go_id"]["enum"] = valid_go_ids
    ki_props["go_id"].pop("pattern", None)

    return schema


def format_theme_context(theme: dict, hub_genes: dict) -> str:
    """Format a single theme's data for the LLM prompt."""
    lines = []
    anchor = theme["anchor_term"]

    lines.append(f"## Theme: {anchor['name']} ({anchor['go_id']})")
    lines.append(f"FDR: {anchor['fdr']:.2e}")
    lines.append(f"Fold Enrichment: {anchor.get('fold_enrichment', 'N/A')}")
    lines.append(f"Namespace: {anchor.get('namespace', 'unknown')}")
    lines.append(f"Genes ({len(anchor.get('genes', []))}): {', '.join(sorted(anchor.get('genes', [])))}")
    lines.append("")

    specific_terms = theme.get("specific_terms", [])
    if specific_terms:
        lines.append(f"### Specific Terms ({len(specific_terms)} nested)")
        for s in specific_terms[:5]:
            lines.append(
                f"  - {s.get('name', '')} ({s.get('go_id', '')}): "
                f"FDR={s.get('fdr', 0):.2e}, "
                f"{len(s.get('genes', []))} genes: {', '.join(sorted(s.get('genes', []))[:8])}"
            )
        lines.append("")

    # Candidate genes
    all_genes = set(anchor.get("genes", []))
    for s in specific_terms:
        all_genes.update(s.get("genes", []))

    lines.append("### Candidate Key Genes (select 2-5):")
    for i, gene in enumerate(sorted(all_genes)[:8], 1):
        is_hub = gene in hub_genes
        hub_label = f" [hub: {hub_genes[gene]['theme_count']} themes]" if is_hub else ""
        lines.append(f"  {i}. {gene}{hub_label}")
    lines.append("")

    return "\n".join(lines)


def collect_valid_sets(theme: dict) -> tuple[list[str], list[str]]:
    """Collect sorted valid gene and GO ID lists from a theme."""
    anchor = theme["anchor_term"]
    genes = set(anchor.get("genes", []))
    go_ids = {anchor["go_id"]}
    for s in theme.get("specific_terms", []):
        genes.update(s.get("genes", []))
        if s.get("go_id"):
            go_ids.add(s["go_id"])
    return sorted(genes), sorted(go_ids)


def main():
    # Load test theme
    with open("/tmp/prototype_theme.json") as f:
        data = json.load(f)

    theme = data["theme"]
    hub_genes = data.get("hub_genes", {})
    anchor = theme["anchor_term"]

    valid_genes, valid_go_ids = collect_valid_sets(theme)

    print(f"Theme: {anchor['name']} ({anchor['go_id']})")
    print(f"Valid genes ({len(valid_genes)}): {valid_genes[:5]}...")
    print(f"Valid GO IDs ({len(valid_go_ids)}): {valid_go_ids}")
    print()

    # Load static schema and inject enums
    base_schema = json.loads(THEME_SCHEMA_PATH.read_text())
    schema = inject_enums(copy.deepcopy(base_schema), valid_genes, valid_go_ids)

    # Show what changed
    print("=== Injected enum on key_genes.gene ===")
    print(json.dumps(schema["properties"]["key_genes"]["items"]["properties"]["gene"], indent=2))
    print()
    print("=== Injected enum on key_insights.go_id ===")
    print(json.dumps(schema["properties"]["key_insights"]["items"]["properties"]["go_id"], indent=2))
    print()

    # Format context
    context = format_theme_context(theme, hub_genes)
    print(f"=== Theme Context ({len(context)} chars) ===")
    print(context[:500])
    print("...\n")

    # Build messages
    system_prompt = (
        "You are a biological enrichment analyst. Generate a structured explanation "
        "for one GO enrichment theme. Follow these rules strictly:\n"
        "- Use ONLY genes and GO IDs from the input data\n"
        "- Quote gene symbols in backticks in narrative and insight text (e.g. `BRCA1`)\n"
        "- Tag EVERY narrative sentence with [DATA], [GO-HIERARCHY], [INFERENCE], or [EXTERNAL]\n"
        "- For key_genes descriptions, explain the MECHANISM, don't just restate the annotation\n"
        "- Cite PMIDs inline where available (e.g. PMID:12345678)\n"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Explain this enrichment theme:\n\n{context}"},
    ]

    # Call OpenAI directly via the adapter (no Pydantic round-trip)
    from cellsem_llm_client.schema.adapters import OpenAISchemaAdapter

    adapter = OpenAISchemaAdapter()
    model = "gpt-4o-mini"

    print(f"=== Calling {model} with enum-constrained JSON schema (no Pydantic) ===")
    raw_response = adapter.apply_schema(
        messages=messages,
        schema_dict=schema,
        model=model,
        max_tokens=2000,
    )

    # Parse response
    content = raw_response.choices[0].message.content
    explanation = json.loads(content)

    print("\n=== LLM Output ===")
    print(json.dumps(explanation, indent=2))

    # Token usage
    usage = raw_response.usage
    if usage:
        print(f"\nTokens: {usage.prompt_tokens} in / {usage.completion_tokens} out")

    # Validate structured fields
    print("\n=== Validation ===")
    errors = []
    for kg in explanation.get("key_genes", []):
        if kg["gene"] not in valid_genes:
            errors.append(f"Hallucinated gene: {kg['gene']}")
        if kg["go_id"] not in valid_go_ids:
            errors.append(f"Hallucinated GO ID in key_gene: {kg['go_id']}")

    for ki in explanation.get("key_insights", []):
        if ki["go_id"] not in valid_go_ids:
            errors.append(f"Hallucinated GO ID in insight: {ki['go_id']}")

    # Validate backtick-quoted genes in narrative
    narrative = explanation.get("narrative", "")
    backtick_genes = re.findall(r"`([^`]+)`", narrative)
    for g in backtick_genes:
        if g not in valid_genes:
            errors.append(f"Hallucinated gene in narrative: `{g}`")

    valid_bt = [g for g in backtick_genes if g in valid_genes]
    invalid_bt = [g for g in backtick_genes if g not in valid_genes]

    if errors:
        print(f"FAILURES ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("✓ Zero hallucinations in structured fields (gene, go_id)")

    if valid_bt:
        print(f"✓ {len(valid_bt)} backtick-quoted gene(s) in narrative are valid: {valid_bt}")
    if not backtick_genes:
        print("⚠ No backtick-quoted genes found in narrative")

    # Check for unquoted gene mentions in narrative
    unquoted = []
    for g in valid_genes:
        # Gene mentioned but not in backticks
        if g in narrative and f"`{g}`" not in narrative:
            unquoted.append(g)
    if unquoted:
        print(f"⚠ {len(unquoted)} gene(s) mentioned without backticks: {unquoted[:5]}")


if __name__ == "__main__":
    main()
