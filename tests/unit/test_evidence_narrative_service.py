"""
Unit tests for Per-Gene Evidence Narrative Service (Phase 1c).

Tests cover evidence context building, gene collection helpers, and
the narrative generation orchestration with mocked LiteLLMAgent.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


# =============================================================================
# Test _build_gene_evidence_context
# =============================================================================


@pytest.mark.unit
class TestBuildGeneEvidenceContext:
    """Tests for _build_gene_evidence_context helper."""

    def test_includes_gaf_annotations(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _build_gene_evidence_context,
        )

        result = _build_gene_evidence_context(
            "FST",
            "Hub gene in 3 themes",
            gaf_annotations=["FST→activin binding [GO:0048185] PMID:1269767"],
        )

        assert "GO Annotations:" in result
        assert "FST→activin binding" in result
        assert "PMID:1269767" in result

    def test_includes_snippets(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _build_gene_evidence_context,
        )

        snippets = [
            {
                "pmid": "19188590",
                "title": "FOXO3 in melanoma",
                "snippet_text": "FOXO3 suppresses melanoma cell migration through...",
            }
        ]
        result = _build_gene_evidence_context("FOXO3", "Theme context", snippets=snippets)

        assert "Literature Snippets:" in result
        assert "PMID:19188590" in result
        assert "FOXO3 suppresses melanoma" in result

    def test_includes_abstracts(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _build_gene_evidence_context,
        )

        abstracts = [
            {
                "pmid": "28652107",
                "title": "ENPP1 in bone",
                "abstract": "ENPP1 regulates pyrophosphate metabolism...",
            }
        ]
        result = _build_gene_evidence_context("ENPP1", "Context", abstracts=abstracts)

        assert "Abstracts:" in result
        assert "PMID:28652107" in result
        assert "ENPP1 regulates pyrophosphate" in result

    def test_no_evidence_fallback(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _build_gene_evidence_context,
        )

        result = _build_gene_evidence_context("UNKNOWN", "Some context")

        assert "No literature evidence available" in result

    def test_snippet_text_truncation(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _build_gene_evidence_context,
        )

        long_text = "A" * 600
        snippets = [{"pmid": "123", "title": "Title", "snippet_text": long_text}]
        result = _build_gene_evidence_context("GENE", "ctx", snippets=snippets)

        assert "..." in result
        assert len(result) < len(long_text) + 200


# =============================================================================
# Test _collect_gene_snippets
# =============================================================================


@pytest.mark.unit
class TestCollectGeneSnippets:
    """Tests for _collect_gene_snippets helper."""

    def test_collects_hub_gene_snippets(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _collect_gene_snippets,
        )

        hub_snips = {
            "FST": [{"pmid": "111", "snippet_text": "FST text"}],
            "OTHER": [{"pmid": "222", "snippet_text": "other"}],
        }
        result = _collect_gene_snippets("FST", None, hub_snips, None, None, None)

        assert len(result) == 1
        assert result[0]["pmid"] == "111"

    def test_collects_cross_theme_snippets(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _collect_gene_snippets,
        )

        cross = {"FST": [{"pmid": "333", "snippet_text": "cross-theme FST"}]}
        result = _collect_gene_snippets("FST", None, None, None, cross, None)

        assert len(result) == 1
        assert result[0]["pmid"] == "333"

    def test_deduplicates_by_pmid(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _collect_gene_snippets,
        )

        hub_snips = {"FST": [{"pmid": "111", "snippet_text": "from hub"}]}
        cross = {"FST": [{"pmid": "111", "snippet_text": "from cross"}]}
        result = _collect_gene_snippets("FST", None, hub_snips, None, cross, None)

        assert len(result) == 1  # Deduped

    def test_collects_theme_specific_snippets(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _collect_gene_snippets,
        )

        snippet_ev = {
            0: [{"pmid": "444", "snippet_text": "FST is involved in something", "paperId": ""}]
        }
        result = _collect_gene_snippets("FST", snippet_ev, None, None, None, None, theme_idx=0)

        assert len(result) == 1

    def test_collects_co_annotation_snippets_for_theme(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _collect_gene_snippets,
        )

        co_annot = {0: {"FST": [{"pmid": "555", "snippet_text": "co-annot text"}]}}
        result = _collect_gene_snippets("FST", None, None, co_annot, None, None, theme_idx=0)

        assert len(result) == 1
        assert result[0]["pmid"] == "555"


# =============================================================================
# Test _collect_gene_gaf_annotations
# =============================================================================


@pytest.mark.unit
class TestCollectGeneGafAnnotations:
    """Tests for _collect_gene_gaf_annotations helper."""

    def test_collects_annotations_across_themes(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _collect_gene_gaf_annotations,
        )

        gaf_pmids = {
            0: [{"pmid": "111", "gene_go_named": {"FST": ["activin binding [GO:0048185]"]}}],
            1: [{"pmid": "222", "gene_go_named": {"FST": ["TGF-beta signaling [GO:0007179]"]}}],
        }

        result = _collect_gene_gaf_annotations("FST", gaf_pmids)
        assert len(result) == 2
        assert any("activin" in a for a in result)
        assert any("TGF-beta" in a for a in result)

    def test_scopes_to_theme(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _collect_gene_gaf_annotations,
        )

        gaf_pmids = {
            0: [{"pmid": "111", "gene_go_named": {"FST": ["activin binding [GO:0048185]"]}}],
            1: [{"pmid": "222", "gene_go_named": {"FST": ["TGF-beta signaling [GO:0007179]"]}}],
        }

        result = _collect_gene_gaf_annotations("FST", gaf_pmids, theme_idx=0)
        assert len(result) == 1
        assert "activin" in result[0]

    def test_empty_gaf_pmids(self):
        from goa_semantic_tools.services.evidence_narrative_service import (
            _collect_gene_gaf_annotations,
        )

        result = _collect_gene_gaf_annotations("FST", None)
        assert result == []


# =============================================================================
# Test generate_gene_narratives (orchestration)
# =============================================================================


@pytest.mark.unit
class TestGenerateGeneNarratives:
    """Tests for generate_gene_narratives orchestration."""

    def _mock_enrichment(self):
        return {
            "themes": [
                {
                    "anchor_term": {
                        "name": "cell migration",
                        "go_id": "GO:0016477",
                        "genes": ["FOXO3", "FST", "KANK1"],
                        "fdr": 0.001,
                        "fold_enrichment": 5.0,
                    },
                    "specific_terms": [
                        {"name": "cell motility", "go_id": "GO:0048870", "genes": ["FOXO3", "FST"]},
                    ],
                    "anchor_confidence": "high",
                },
            ],
            "hub_genes": {
                "FOXO3": {"theme_count": 3, "themes": ["cell migration", "apoptosis", "metabolism"]},
            },
            "enrichment_leaves": [],
            "metadata": {"species": "human", "input_genes_count": 100,
                         "genes_with_annotations": 80, "total_enriched_terms": 50,
                         "fdr_threshold": 0.05},
        }

    @patch("goa_semantic_tools.services.evidence_narrative_service._call_narrative_agent")
    def test_generates_hub_gene_narratives(self, mock_call):
        from goa_semantic_tools.services.evidence_narrative_service import (
            generate_gene_narratives,
        )

        mock_call.return_value = (
            "FOXO3 suppresses melanoma migration via PI3K/AKT PMID:19188590.",
            {"input_tokens": 100, "output_tokens": 30, "estimated_cost_usd": 0.001},
        )

        result = generate_gene_narratives(
            self._mock_enrichment(),
            model="gpt-4o-mini",
            api_key="test-key",
        )

        assert "FOXO3" in result["hub_genes"]
        assert "PMID:19188590" in result["hub_genes"]["FOXO3"]
        assert result["usage"]["n_calls"] > 0

    @patch("goa_semantic_tools.services.evidence_narrative_service._call_narrative_agent")
    def test_generates_theme_gene_narratives(self, mock_call):
        from goa_semantic_tools.services.evidence_narrative_service import (
            generate_gene_narratives,
        )

        mock_call.return_value = (
            "Gene narrative text.",
            {"input_tokens": 100, "output_tokens": 30, "estimated_cost_usd": 0.001},
        )

        result = generate_gene_narratives(
            self._mock_enrichment(),
            model="gpt-4o-mini",
            api_key="test-key",
        )

        # FST and KANK1 should be theme genes (not hub genes)
        # FOXO3 is a hub gene so should NOT appear in theme_genes
        assert "FOXO3" not in result.get("theme_genes", {}).get(0, {})

    @patch("goa_semantic_tools.services.evidence_narrative_service._call_narrative_agent")
    def test_handles_failed_calls_gracefully(self, mock_call):
        from goa_semantic_tools.services.evidence_narrative_service import (
            generate_gene_narratives,
        )

        mock_call.side_effect = Exception("LLM timeout")

        result = generate_gene_narratives(
            self._mock_enrichment(),
            model="gpt-4o-mini",
            api_key="test-key",
        )

        # Should not crash, but narratives will be empty
        assert result["hub_genes"] == {}
        assert result["usage"]["n_calls"] == 0

    @patch("goa_semantic_tools.services.evidence_narrative_service._call_narrative_agent")
    def test_empty_enrichment_returns_empty(self, mock_call):
        from goa_semantic_tools.services.evidence_narrative_service import (
            generate_gene_narratives,
        )

        result = generate_gene_narratives(
            {"themes": [], "hub_genes": {}, "enrichment_leaves": [],
             "metadata": {"species": "human", "input_genes_count": 0,
                          "genes_with_annotations": 0, "total_enriched_terms": 0,
                          "fdr_threshold": 0.05}},
            model="gpt-4o-mini",
            api_key="test-key",
        )

        assert result["hub_genes"] == {}
        assert result["theme_genes"] == {}
        assert result["usage"]["n_calls"] == 0
        mock_call.assert_not_called()

    @patch("goa_semantic_tools.services.evidence_narrative_service._call_narrative_agent")
    def test_usage_tracking(self, mock_call):
        from goa_semantic_tools.services.evidence_narrative_service import (
            generate_gene_narratives,
        )

        mock_call.return_value = (
            "Narrative text.",
            {"input_tokens": 200, "output_tokens": 50, "estimated_cost_usd": 0.002},
        )

        result = generate_gene_narratives(
            self._mock_enrichment(),
            model="gpt-4o-mini",
            api_key="test-key",
        )

        usage = result["usage"]
        assert usage["total_input_tokens"] > 0
        assert usage["total_output_tokens"] > 0
        assert usage["total_cost"] > 0
