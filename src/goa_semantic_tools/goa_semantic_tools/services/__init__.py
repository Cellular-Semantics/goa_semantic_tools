"""Integration-facing services (LLM clients, Deepsearch, etc.)."""

from __future__ import annotations

from .artl_literature_service import resolve_assertions_via_literature
from .go_enrichment_service import run_go_enrichment
from .go_markdown_explanation_service import generate_markdown_explanation
from .reference_retrieval_service import (
    AtomicAssertion,
    ReferenceMatch,
    extract_claims,
    extract_genes_from_text,
    find_references_for_assertion,
    format_references_needing_artl_mcp,
    inject_references,
)

__all__ = [
    "run_go_enrichment",
    "generate_markdown_explanation",
    "resolve_assertions_via_literature",
    "AtomicAssertion",
    "ReferenceMatch",
    "extract_claims",
    "extract_genes_from_text",
    "find_references_for_assertion",
    "format_references_needing_artl_mcp",
    "inject_references",
]
