"""Integration-facing services (LLM clients, Deepsearch, etc.)."""

from __future__ import annotations

from .go_enrichment_service import run_go_enrichment

__all__ = ["run_go_enrichment"]
