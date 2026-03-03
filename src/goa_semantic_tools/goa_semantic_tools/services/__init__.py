"""Integration-facing services (LLM clients, Deepsearch, etc.)."""

from __future__ import annotations

from .artl_literature_service import (
    fetch_abstracts_for_hub_genes,
    fetch_abstracts_for_themes,
    resolve_assertions_via_literature,
)
from .go_enrichment_service import run_go_enrichment
from .go_markdown_explanation_service import generate_markdown_explanation
from .reference_retrieval_service import (
    AtomicAssertion,
    ReferenceMatch,
    extract_claims,
    extract_genes_from_text,
    find_references_for_assertion,
    format_references_needing_artl_mcp,
    get_gaf_pmids_for_themes,
    inject_references,
    inject_references_inline,
)

__all__ = [
    "run_go_enrichment",
    "generate_markdown_explanation",
    "fetch_abstracts_for_hub_genes",
    "fetch_abstracts_for_themes",
    "resolve_assertions_via_literature",
    "AtomicAssertion",
    "ReferenceMatch",
    "extract_claims",
    "extract_genes_from_text",
    "find_references_for_assertion",
    "format_references_needing_artl_mcp",
    "get_gaf_pmids_for_themes",
    "inject_references",
    "inject_references_inline",
]
