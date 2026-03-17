"""
Unit tests for ASTA (Semantic Scholar) Snippet Search Service.

Tests cover snippet parsing, filtering, deduplication, and the
fetch_snippets_for_gaf_pmids / fetch_snippets_for_hub_genes orchestration.
"""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest


# =============================================================================
# Test _parse_snippet_results
# =============================================================================


@pytest.mark.unit
class TestParseSnippetResults:
    """Tests for _parse_snippet_results helper."""

    def test_parses_data_wrapped_format(self):
        """Test parsing ASTA response with data wrapper."""
        from goa_semantic_tools.services.asta_literature_service import _parse_snippet_results

        raw = json.dumps({
            "data": [
                {
                    "paper": {
                        "paperId": "abc123",
                        "title": "FOXO3 in melanoma",
                        "authors": [{"name": "Smith"}, {"name": "Jones"}],
                        "externalIds": {"PubMed": "19188590"},
                    },
                    "snippetText": "FOXO3 suppresses melanoma cell migration through...",
                    "score": 0.85,
                }
            ]
        })

        snippets = _parse_snippet_results(raw)

        assert len(snippets) == 1
        assert snippets[0]["paperId"] == "abc123"
        assert snippets[0]["pmid"] == "19188590"
        assert snippets[0]["title"] == "FOXO3 in melanoma"
        assert "Smith" in snippets[0]["authors"]
        assert "FOXO3 suppresses" in snippets[0]["snippet_text"]
        assert snippets[0]["score"] == 0.85

    def test_parses_bare_list_format(self):
        """Test parsing bare list of snippet objects."""
        from goa_semantic_tools.services.asta_literature_service import _parse_snippet_results

        raw = json.dumps([
            {
                "paper": {"paperId": "def456", "title": "Paper 2"},
                "snippetText": "Evidence text here",
                "score": 0.5,
            }
        ])

        snippets = _parse_snippet_results(raw)
        assert len(snippets) == 1
        assert snippets[0]["paperId"] == "def456"

    def test_empty_string_returns_empty(self):
        from goa_semantic_tools.services.asta_literature_service import _parse_snippet_results
        assert _parse_snippet_results("") == []

    def test_invalid_json_returns_empty(self):
        from goa_semantic_tools.services.asta_literature_service import _parse_snippet_results
        assert _parse_snippet_results("not json") == []

    def test_skips_items_without_snippet_text(self):
        from goa_semantic_tools.services.asta_literature_service import _parse_snippet_results

        raw = json.dumps({
            "data": [
                {"paper": {"paperId": "a"}, "score": 0.9},  # no snippet text
                {"paper": {"paperId": "b"}, "snippetText": "Has text", "score": 0.8},
            ]
        })

        snippets = _parse_snippet_results(raw)
        assert len(snippets) == 1
        assert snippets[0]["paperId"] == "b"

    def test_authors_et_al_for_many_authors(self):
        """Test that >3 authors get 'et al.' suffix."""
        from goa_semantic_tools.services.asta_literature_service import _parse_snippet_results

        raw = json.dumps({
            "data": [{
                "paper": {
                    "paperId": "x",
                    "title": "T",
                    "authors": [{"name": "A"}, {"name": "B"}, {"name": "C"}, {"name": "D"}],
                },
                "snippetText": "text",
                "score": 0.5,
            }]
        })

        snippets = _parse_snippet_results(raw)
        assert "et al." in snippets[0]["authors"]
        assert "D" not in snippets[0]["authors"]

    def test_missing_external_ids_yields_empty_pmid(self):
        """Papers without externalIds should have empty pmid."""
        from goa_semantic_tools.services.asta_literature_service import _parse_snippet_results

        raw = json.dumps({
            "data": [{
                "paper": {"paperId": "noPmid", "title": "T"},
                "snippetText": "text",
                "score": 0.5,
            }]
        })

        snippets = _parse_snippet_results(raw)
        assert snippets[0]["pmid"] == ""


# =============================================================================
# Test _filter_snippets
# =============================================================================


@pytest.mark.unit
class TestFilterSnippets:
    """Tests for _filter_snippets helper."""

    def test_filters_below_threshold(self):
        from goa_semantic_tools.services.asta_literature_service import _filter_snippets

        snippets = [
            {"snippet_text": "good", "score": 0.5},
            {"snippet_text": "bad", "score": 0.1},
            {"snippet_text": "borderline", "score": 0.2},
        ]

        filtered = _filter_snippets(snippets, min_score=0.2)
        assert len(filtered) == 2
        assert all(s["score"] >= 0.2 for s in filtered)

    def test_default_threshold_is_0_2(self):
        from goa_semantic_tools.services.asta_literature_service import _filter_snippets

        snippets = [
            {"snippet_text": "a", "score": 0.19},
            {"snippet_text": "b", "score": 0.21},
        ]

        filtered = _filter_snippets(snippets)
        assert len(filtered) == 1
        assert filtered[0]["score"] == 0.21

    def test_empty_list_returns_empty(self):
        from goa_semantic_tools.services.asta_literature_service import _filter_snippets
        assert _filter_snippets([]) == []


# =============================================================================
# Test _deduplicate_snippets
# =============================================================================


@pytest.mark.unit
class TestDeduplicateSnippets:
    """Tests for _deduplicate_snippets helper."""

    def test_keeps_highest_scored_per_paper(self):
        from goa_semantic_tools.services.asta_literature_service import _deduplicate_snippets

        snippets = [
            {"paperId": "a", "snippet_text": "first", "score": 0.3},
            {"paperId": "a", "snippet_text": "second", "score": 0.8},
            {"paperId": "b", "snippet_text": "other", "score": 0.5},
        ]

        deduped = _deduplicate_snippets(snippets)
        assert len(deduped) == 2
        paper_a = next(s for s in deduped if s["paperId"] == "a")
        assert paper_a["score"] == 0.8

    def test_deduplicates_by_pmid_when_no_paperId(self):
        from goa_semantic_tools.services.asta_literature_service import _deduplicate_snippets

        snippets = [
            {"paperId": "", "pmid": "12345", "snippet_text": "a", "score": 0.3},
            {"paperId": "", "pmid": "12345", "snippet_text": "b", "score": 0.7},
        ]

        deduped = _deduplicate_snippets(snippets)
        assert len(deduped) == 1
        assert deduped[0]["score"] == 0.7

    def test_empty_list_returns_empty(self):
        from goa_semantic_tools.services.asta_literature_service import _deduplicate_snippets
        assert _deduplicate_snippets([]) == []


# =============================================================================
# Test fetch_snippets_for_gaf_pmids (orchestration)
# =============================================================================


@pytest.mark.unit
class TestFetchSnippetsForGafPmids:
    """Tests for fetch_snippets_for_gaf_pmids."""

    def _make_theme(self, name="T cell activation"):
        return {
            "anchor_term": {
                "name": name,
                "go_id": "GO:0050870",
                "genes": ["RELA", "IL6", "TNF"],
            },
            "specific_terms": [],
        }

    def _make_snippet_response(self, n=2):
        """Build a realistic ASTA snippet response JSON string."""
        items = []
        for i in range(n):
            items.append({
                "paper": {
                    "paperId": f"paper_{i}",
                    "title": f"Paper Title {i}",
                    "authors": [{"name": f"Author{i}"}],
                    "externalIds": {"PubMed": f"1111111{i}"},
                },
                "snippetText": f"Evidence passage {i} with experimental detail.",
                "score": 0.5 + i * 0.1,
            })
        return json.dumps({"data": items})

    def _make_mock_source(self, return_json):
        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.return_value = return_json

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]

        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        return mock_ctx, mock_tool

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_empty_gaf_pmids_returns_empty(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_gaf_pmids
        result = fetch_snippets_for_gaf_pmids({}, [], "test-key")
        assert result == {}
        mock_mcp_cls.assert_not_called()

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_returns_snippets_per_theme(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_gaf_pmids

        mock_ctx, mock_tool = self._make_mock_source(self._make_snippet_response(2))
        mock_mcp_cls.return_value = mock_ctx

        gaf_pmids = {
            0: [{"pmid": "11111", "genes_covered": ["RELA"]}],
            1: [{"pmid": "22222", "genes_covered": ["IL6"]}],
        }
        themes = [self._make_theme("Theme A"), self._make_theme("Theme B")]

        result = fetch_snippets_for_gaf_pmids(gaf_pmids, themes, "test-key")

        assert 0 in result
        assert 1 in result
        assert len(result[0]) > 0
        assert "snippet_text" in result[0][0]

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_builds_query_with_anchor_name(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_gaf_pmids

        mock_ctx, mock_tool = self._make_mock_source(self._make_snippet_response(1))
        mock_mcp_cls.return_value = mock_ctx

        gaf_pmids = {0: [{"pmid": "11111", "genes_covered": ["RELA"]}]}
        themes = [self._make_theme("positive regulation of immune response")]

        fetch_snippets_for_gaf_pmids(gaf_pmids, themes, "test-key")

        call_args = mock_tool.handler.call_args[0][0]
        assert call_args["query"] == "positive regulation of immune response"
        assert "PMID:11111" in call_args["paper_ids"]

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_graceful_degradation_session_failure(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_gaf_pmids

        mock_mcp_cls.side_effect = Exception("ASTA connection refused")

        gaf_pmids = {0: [{"pmid": "11111", "genes_covered": ["X"]}]}
        result = fetch_snippets_for_gaf_pmids(gaf_pmids, [], "test-key")

        assert result == {0: []}

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_graceful_degradation_per_theme_failure(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_gaf_pmids

        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.side_effect = [
            RuntimeError("Timeout"),
            self._make_snippet_response(1),
        ]
        mock_source = MagicMock()
        mock_source.tools = [mock_tool]
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        mock_mcp_cls.return_value = mock_ctx

        gaf_pmids = {
            0: [{"pmid": "11111", "genes_covered": ["A"]}],
            1: [{"pmid": "22222", "genes_covered": ["B"]}],
        }
        themes = [self._make_theme("Fail"), self._make_theme("Succeed")]

        result = fetch_snippets_for_gaf_pmids(gaf_pmids, themes, "test-key")
        assert result[0] == []
        assert len(result[1]) > 0

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_tool_not_found_returns_empty_lists(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_gaf_pmids

        mock_source = MagicMock()
        mock_source.tools = []  # no tools
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        mock_mcp_cls.return_value = mock_ctx

        gaf_pmids = {0: [{"pmid": "11111", "genes_covered": ["X"]}]}
        result = fetch_snippets_for_gaf_pmids(gaf_pmids, [], "test-key")
        assert result == {0: []}


# =============================================================================
# Test fetch_snippets_for_hub_genes (orchestration)
# =============================================================================


@pytest.mark.unit
class TestFetchSnippetsForHubGenes:
    """Tests for fetch_snippets_for_hub_genes."""

    def _make_hub_genes(self, names_counts):
        return {
            gene: {"theme_count": count, "themes": [f"theme_{i}" for i in range(min(count, 3))]}
            for gene, count in names_counts.items()
        }

    def _make_snippet_response(self, n=1):
        items = []
        for i in range(n):
            items.append({
                "paper": {
                    "paperId": f"paper_{i}",
                    "title": f"Title {i}",
                    "authors": [{"name": f"Auth{i}"}],
                    "externalIds": {"PubMed": f"9999999{i}"},
                },
                "snippetText": f"Hub gene evidence {i}.",
                "score": 0.6,
            })
        return json.dumps({"data": items})

    def _make_mock_source(self, return_json):
        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.return_value = return_json

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]

        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        return mock_ctx, mock_tool

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_empty_hub_genes_returns_empty(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_hub_genes
        result = fetch_snippets_for_hub_genes({}, [], "test-key")
        assert result == {}
        mock_mcp_cls.assert_not_called()

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_selects_top_n_by_theme_count(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_hub_genes

        mock_ctx, _ = self._make_mock_source(self._make_snippet_response(1))
        mock_mcp_cls.return_value = mock_ctx

        hub_genes = self._make_hub_genes({"A": 50, "B": 30, "C": 20, "D": 10})
        result = fetch_snippets_for_hub_genes(hub_genes, [], "test-key", max_hub_genes=2)

        assert "A" in result
        assert "B" in result
        assert "C" not in result

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_builds_query_from_gene_and_theme(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_hub_genes

        mock_ctx, mock_tool = self._make_mock_source(self._make_snippet_response(1))
        mock_mcp_cls.return_value = mock_ctx

        hub_genes = {"IL6": {"theme_count": 5, "themes": ["inflammatory response"]}}
        fetch_snippets_for_hub_genes(hub_genes, [], "test-key")

        call_args = mock_tool.handler.call_args[0][0]
        assert "IL6" in call_args["query"]
        assert "inflammatory response" in call_args["query"]

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_graceful_degradation_session_failure(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_hub_genes

        mock_mcp_cls.side_effect = Exception("Connection refused")

        hub_genes = self._make_hub_genes({"IL6": 10, "TNF": 8})
        result = fetch_snippets_for_hub_genes(hub_genes, [], "test-key")

        assert result == {"IL6": [], "TNF": []}

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_graceful_degradation_per_gene_failure(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_hub_genes

        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.side_effect = [
            Exception("Timeout"),
            self._make_snippet_response(1),
        ]
        mock_source = MagicMock()
        mock_source.tools = [mock_tool]
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        mock_mcp_cls.return_value = mock_ctx

        hub_genes = {"IL6": {"theme_count": 10, "themes": ["t1"]},
                     "TNF": {"theme_count": 8, "themes": ["t2"]}}
        result = fetch_snippets_for_hub_genes(hub_genes, [], "test-key")

        assert result["IL6"] == []
        assert len(result["TNF"]) > 0


# =============================================================================
# Test _format_enrichment_for_llm snippet integration
# =============================================================================


@pytest.mark.unit
class TestFormatEnrichmentWithSnippets:
    """Test that _format_enrichment_for_llm renders snippet blocks."""

    def _minimal_enrichment(self):
        return {
            "metadata": {
                "species": "human",
                "input_genes_count": 10,
                "genes_with_annotations": 8,
                "total_enriched_terms": 5,
                "fdr_threshold": 0.05,
            },
            "themes": [{
                "anchor_term": {
                    "name": "immune response",
                    "go_id": "GO:0006955",
                    "namespace": "biological_process",
                    "fdr": 0.001,
                    "fold_enrichment": 5.0,
                    "genes": ["IL6", "TNF"],
                    "depth": 3,
                },
                "specific_terms": [],
                "anchor_confidence": "high",
            }],
            "hub_genes": {"IL6": {"theme_count": 3, "themes": ["immune response", "inflammation"]}},
            "enrichment_leaves": [],
        }

    def test_snippet_evidence_appears_in_output(self):
        from goa_semantic_tools.services.go_markdown_explanation_service import (
            _format_enrichment_for_llm,
        )

        enrichment = self._minimal_enrichment()
        snippet_evidence = {
            0: [{
                "paperId": "abc",
                "pmid": "12345678",
                "title": "IL6 in immune response",
                "authors": "Smith, Jones",
                "snippet_text": "IL6 activates downstream JAK-STAT signaling in T cells...",
                "score": 0.8,
            }]
        }

        result = _format_enrichment_for_llm(enrichment, snippet_evidence=snippet_evidence)

        assert "Available Evidence Snippets" in result
        assert "PMID:12345678" in result
        assert "IL6 in immune response" in result
        assert "IL6 activates downstream" in result

    def test_hub_gene_snippets_appear_in_output(self):
        from goa_semantic_tools.services.go_markdown_explanation_service import (
            _format_enrichment_for_llm,
        )

        enrichment = self._minimal_enrichment()
        hub_gene_snippets = {
            "IL6": [{
                "paperId": "def",
                "pmid": "87654321",
                "title": "IL6 coordinates inflammation",
                "authors": "Brown",
                "snippet_text": "IL6 plays a central role in coordinating...",
                "score": 0.7,
            }]
        }

        result = _format_enrichment_for_llm(enrichment, hub_gene_snippets=hub_gene_snippets)

        assert "Supporting Evidence Snippets" in result
        assert "PMID:87654321" in result
        assert "IL6 coordinates inflammation" in result

    def test_snippets_preferred_over_abstracts_for_hub_genes(self):
        """When both snippets and abstracts exist, snippets should appear."""
        from goa_semantic_tools.services.go_markdown_explanation_service import (
            _format_enrichment_for_llm,
        )

        enrichment = self._minimal_enrichment()
        hub_gene_abstracts = {
            "IL6": [{"pmid": "111", "title": "Abstract paper", "abstract": "...", "authors": "X", "year": "2020"}]
        }
        hub_gene_snippets = {
            "IL6": [{"paperId": "s1", "pmid": "222", "title": "Snippet paper", "authors": "Y", "snippet_text": "evidence", "score": 0.9}]
        }

        result = _format_enrichment_for_llm(
            enrichment,
            hub_gene_abstracts=hub_gene_abstracts,
            hub_gene_snippets=hub_gene_snippets,
        )

        assert "Supporting Evidence Snippets" in result
        assert "Snippet paper" in result
        # Abstract-based section should NOT appear when snippets exist
        assert "Supporting Literature" not in result

    def test_falls_back_to_abstracts_when_no_snippets(self):
        """When no snippets, abstract section should still appear."""
        from goa_semantic_tools.services.go_markdown_explanation_service import (
            _format_enrichment_for_llm,
        )

        enrichment = self._minimal_enrichment()
        hub_gene_abstracts = {
            "IL6": [{"pmid": "111", "title": "Abstract paper", "abstract": "An abstract.", "authors": "X", "year": "2020"}]
        }

        result = _format_enrichment_for_llm(enrichment, hub_gene_abstracts=hub_gene_abstracts)

        assert "Supporting Literature" in result
        assert "Abstract paper" in result

    def test_co_annotation_snippets_appear_in_output(self):
        """Within-theme co-annotation snippets should render per theme."""
        from goa_semantic_tools.services.go_markdown_explanation_service import (
            _format_enrichment_for_llm,
        )

        enrichment = self._minimal_enrichment()
        co_annotation_snippets = {
            0: {
                "IL6": [{
                    "paperId": "co1",
                    "pmid": "55555555",
                    "title": "IL6 links sprouting and migration",
                    "authors": "Wang",
                    "snippet_text": "IL6 regulates both sprouting angiogenesis and trophoblast migration...",
                    "score": 0.75,
                }]
            }
        }
        gaf_pmids = {
            0: [{
                "pmid": "55555555",
                "genes_covered": ["IL6"],
                "gene_go_map": {"IL6": ["GO:001", "GO:002"]},
                "gene_go_named": {"IL6": ["sprouting angiogenesis [GO:001]", "trophoblast migration [GO:002]"]},
            }]
        }

        result = _format_enrichment_for_llm(
            enrichment,
            gaf_pmids=gaf_pmids,
            co_annotation_snippets=co_annotation_snippets,
        )

        assert "Co-Annotation Evidence" in result
        assert "IL6" in result
        assert "PMID:55555555" in result
        assert "sprouting angiogenesis" in result
        assert "IL6 regulates both" in result

    def test_cross_theme_snippets_appear_in_hub_gene_section(self):
        """Cross-theme co-annotation snippets should appear under hub genes."""
        from goa_semantic_tools.services.go_markdown_explanation_service import (
            _format_enrichment_for_llm,
        )

        enrichment = self._minimal_enrichment()
        cross_theme_snippets = {
            "IL6": [{
                "paperId": "ct1",
                "pmid": "66666666",
                "title": "IL6 bridges immune response and inflammation",
                "authors": "Chen et al.",
                "snippet_text": "IL6 coordinates signaling between immune activation and inflammatory cascades...",
                "score": 0.82,
            }]
        }

        result = _format_enrichment_for_llm(
            enrichment,
            cross_theme_snippets=cross_theme_snippets,
        )

        assert "Cross-theme Evidence Snippets" in result
        assert "PMID:66666666" in result
        assert "IL6 bridges immune response" in result
        assert "IL6 coordinates signaling" in result

    def test_co_annotation_without_snippets_shows_nothing(self):
        """Empty co-annotation snippets should not add section."""
        from goa_semantic_tools.services.go_markdown_explanation_service import (
            _format_enrichment_for_llm,
        )

        enrichment = self._minimal_enrichment()
        result = _format_enrichment_for_llm(enrichment, co_annotation_snippets={})
        assert "Co-Annotation Evidence" not in result


# =============================================================================
# Test fetch_snippets_for_co_annotations (orchestration)
# =============================================================================


@pytest.mark.unit
class TestFetchSnippetsForCoAnnotations:
    """Tests for fetch_snippets_for_co_annotations."""

    def _make_gaf_pmids(self):
        """Build gaf_pmids with a gene co-annotated to 2 GO terms."""
        return {
            0: [{
                "pmid": "11111111",
                "genes_covered": ["VEGFA"],
                "gene_go_map": {"VEGFA": ["GO:001", "GO:002"]},
                "gene_go_named": {
                    "VEGFA": ["pos reg sprouting angiogenesis [GO:001]", "pos reg trophoblast migration [GO:002]"]
                },
            }]
        }

    def _make_themes(self):
        return [{
            "anchor_term": {"name": "angiogenesis", "go_id": "GO:0001525", "genes": ["VEGFA"]},
            "specific_terms": [],
        }]

    def _make_snippet_response(self, n=1):
        items = []
        for i in range(n):
            items.append({
                "paper": {
                    "paperId": f"co_paper_{i}",
                    "title": f"Co-annot Paper {i}",
                    "authors": [{"name": f"Auth{i}"}],
                    "externalIds": {"PubMed": f"8888888{i}"},
                },
                "snippetText": f"Co-annotation evidence {i}.",
                "score": 0.6,
            })
        return json.dumps({"data": items})

    def _make_mock_source(self, return_json):
        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.return_value = return_json

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]

        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        return mock_ctx, mock_tool

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_empty_gaf_returns_empty(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations
        result = fetch_snippets_for_co_annotations({}, [], "test-key")
        assert result == {}

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_finds_within_theme_co_annotations(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations

        mock_ctx, mock_tool = self._make_mock_source(self._make_snippet_response(1))
        mock_mcp_cls.return_value = mock_ctx

        result = fetch_snippets_for_co_annotations(
            self._make_gaf_pmids(), self._make_themes(), "test-key"
        )

        assert 0 in result
        assert "VEGFA" in result[0]
        assert len(result[0]["VEGFA"]) == 1

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_query_contains_gene_and_term_names(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations

        mock_ctx, mock_tool = self._make_mock_source(self._make_snippet_response(1))
        mock_mcp_cls.return_value = mock_ctx

        fetch_snippets_for_co_annotations(
            self._make_gaf_pmids(), self._make_themes(), "test-key"
        )

        call_args = mock_tool.handler.call_args_list[0][0][0]
        assert "VEGFA" in call_args["query"]
        assert "sprouting angiogenesis" in call_args["query"]
        assert "PMID:11111111" in call_args["paper_ids"]

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_widen_on_miss_retries_unscoped(self, mock_mcp_cls):
        """When scoped search returns empty, should retry without paper_ids."""
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations

        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        # First call (scoped) returns empty, second (widened) returns result
        mock_tool.handler.side_effect = [
            json.dumps({"data": []}),
            self._make_snippet_response(1),
        ]

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        mock_mcp_cls.return_value = mock_ctx

        result = fetch_snippets_for_co_annotations(
            self._make_gaf_pmids(), self._make_themes(), "test-key",
            widen_on_miss=True,
        )

        assert len(result[0]["VEGFA"]) == 1
        # Second call should NOT have paper_ids
        second_call_args = mock_tool.handler.call_args_list[1][0][0]
        assert "paper_ids" not in second_call_args

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_widen_disabled_no_retry(self, mock_mcp_cls):
        """When widen_on_miss=False, should not retry."""
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations

        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.return_value = json.dumps({"data": []})

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        mock_mcp_cls.return_value = mock_ctx

        result = fetch_snippets_for_co_annotations(
            self._make_gaf_pmids(), self._make_themes(), "test-key",
            widen_on_miss=False,
        )

        assert result[0]["VEGFA"] == []
        assert mock_tool.handler.call_count == 1

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_skips_genes_with_single_go_term(self, mock_mcp_cls):
        """Genes with only 1 GO term should not trigger co-annotation queries."""
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations

        gaf_pmids = {
            0: [{
                "pmid": "22222222",
                "genes_covered": ["TP53"],
                "gene_go_map": {"TP53": ["GO:001"]},  # Only 1 term
                "gene_go_named": {"TP53": ["apoptosis [GO:001]"]},
            }]
        }
        themes = [{"anchor_term": {"name": "apoptosis", "go_id": "GO:0006915", "genes": ["TP53"]}}]

        result = fetch_snippets_for_co_annotations(gaf_pmids, themes, "test-key")
        assert result == {}
        mock_mcp_cls.assert_not_called()


# =============================================================================
# Test fetch_snippets_for_cross_theme_co_annotations (orchestration)
# =============================================================================


@pytest.mark.unit
class TestFetchSnippetsForCrossThemeCoAnnotations:
    """Tests for fetch_snippets_for_cross_theme_co_annotations."""

    def _make_cross_theme_index(self):
        return {
            "IL6": [{
                "pmid": "33333333",
                "themes": [{"index": 0, "name": "immune response"}, {"index": 1, "name": "inflammation"}],
                "annotations": ["immune response: IL6 function", "inflammation: IL6 signaling"],
            }]
        }

    def _make_snippet_response(self, n=1):
        items = []
        for i in range(n):
            items.append({
                "paper": {
                    "paperId": f"ct_paper_{i}",
                    "title": f"Cross-theme Paper {i}",
                    "authors": [{"name": f"Auth{i}"}],
                    "externalIds": {"PubMed": f"7777777{i}"},
                },
                "snippetText": f"Cross-theme evidence {i}.",
                "score": 0.7,
            })
        return json.dumps({"data": items})

    def _make_mock_source(self, return_json):
        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.return_value = return_json

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]

        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        return mock_ctx, mock_tool

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_empty_index_returns_empty(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_cross_theme_co_annotations
        result = fetch_snippets_for_cross_theme_co_annotations({}, "test-key")
        assert result == {}

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_returns_snippets_for_cross_theme_genes(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_cross_theme_co_annotations

        mock_ctx, _ = self._make_mock_source(self._make_snippet_response(1))
        mock_mcp_cls.return_value = mock_ctx

        result = fetch_snippets_for_cross_theme_co_annotations(
            self._make_cross_theme_index(), "test-key"
        )

        assert "IL6" in result
        assert len(result["IL6"]) == 1

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_query_contains_gene_and_theme_names(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_cross_theme_co_annotations

        mock_ctx, mock_tool = self._make_mock_source(self._make_snippet_response(1))
        mock_mcp_cls.return_value = mock_ctx

        fetch_snippets_for_cross_theme_co_annotations(
            self._make_cross_theme_index(), "test-key"
        )

        call_args = mock_tool.handler.call_args_list[0][0][0]
        assert "IL6" in call_args["query"]
        assert "immune response" in call_args["query"]
        assert "PMID:33333333" in call_args["paper_ids"]

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_widen_on_miss_retries_unscoped(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_cross_theme_co_annotations

        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.side_effect = [
            json.dumps({"data": []}),
            self._make_snippet_response(1),
        ]
        mock_source = MagicMock()
        mock_source.tools = [mock_tool]
        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        mock_mcp_cls.return_value = mock_ctx

        result = fetch_snippets_for_cross_theme_co_annotations(
            self._make_cross_theme_index(), "test-key",
            widen_on_miss=True,
        )

        assert len(result["IL6"]) == 1
        second_call_args = mock_tool.handler.call_args_list[1][0][0]
        assert "paper_ids" not in second_call_args

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_graceful_degradation_session_failure(self, mock_mcp_cls):
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_cross_theme_co_annotations

        mock_mcp_cls.side_effect = Exception("Connection refused")

        result = fetch_snippets_for_cross_theme_co_annotations(
            self._make_cross_theme_index(), "test-key"
        )

        assert result == {"IL6": []}


# =============================================================================
# Test _parallel_snippet_search
# =============================================================================


@pytest.mark.unit
class TestParallelSnippetSearch:
    """Tests for _parallel_snippet_search helper."""

    def test_returns_results_in_order(self):
        """Results list must match query order regardless of execution order."""
        from goa_semantic_tools.services.asta_literature_service import _parallel_snippet_search

        # Use a deterministic mapping so call order doesn't matter
        def _handler(args):
            return f"result_{args['query']}"

        mock_tool = MagicMock()
        mock_tool.handler.side_effect = _handler

        queries = [{"query": "a"}, {"query": "b"}, {"query": "c"}]
        results = _parallel_snippet_search(mock_tool, queries, max_workers=2)

        assert len(results) == 3
        assert results[0] == "result_a"
        assert results[1] == "result_b"
        assert results[2] == "result_c"

    def test_handles_individual_failures(self):
        from goa_semantic_tools.services.asta_literature_service import _parallel_snippet_search

        mock_tool = MagicMock()
        mock_tool.handler.side_effect = [
            "ok_0",
            Exception("fail"),
            "ok_2",
        ]

        queries = [{"query": "a"}, {"query": "b"}, {"query": "c"}]
        results = _parallel_snippet_search(mock_tool, queries, max_workers=1)

        assert results[0] == "ok_0"
        assert results[1] is None
        assert results[2] == "ok_2"

    def test_empty_queries_returns_empty(self):
        from goa_semantic_tools.services.asta_literature_service import _parallel_snippet_search

        mock_tool = MagicMock()
        results = _parallel_snippet_search(mock_tool, [])
        assert results == []
        mock_tool.handler.assert_not_called()


# =============================================================================
# Test _select_best_paper_snippets
# =============================================================================


@pytest.mark.unit
class TestSelectBestPaperSnippets:
    """Tests for _select_best_paper_snippets helper."""

    def test_returns_top_paper_and_runner_up(self):
        from goa_semantic_tools.services.asta_literature_service import _select_best_paper_snippets

        snippets = [
            {"paperId": "A", "snippet_text": "a1", "score": 0.9},
            {"paperId": "A", "snippet_text": "a2", "score": 0.8},
            {"paperId": "A", "snippet_text": "a3", "score": 0.7},
            {"paperId": "A", "snippet_text": "a4", "score": 0.6},
            {"paperId": "B", "snippet_text": "b1", "score": 0.85},
            {"paperId": "B", "snippet_text": "b2", "score": 0.5},
        ]

        selected = _select_best_paper_snippets(snippets, max_from_top=3, max_from_runner_up=1, max_total=4)

        assert len(selected) == 4
        paper_ids = [s["paperId"] for s in selected]
        assert paper_ids.count("A") == 3
        assert paper_ids.count("B") == 1
        # Should be sorted by score desc
        scores = [s["score"] for s in selected]
        assert scores == sorted(scores, reverse=True)

    def test_single_paper_returns_max_from_top(self):
        from goa_semantic_tools.services.asta_literature_service import _select_best_paper_snippets

        snippets = [
            {"paperId": "A", "snippet_text": "a1", "score": 0.9},
            {"paperId": "A", "snippet_text": "a2", "score": 0.8},
            {"paperId": "A", "snippet_text": "a3", "score": 0.7},
            {"paperId": "A", "snippet_text": "a4", "score": 0.6},
        ]

        selected = _select_best_paper_snippets(snippets, max_from_top=3, max_from_runner_up=1, max_total=4)

        assert len(selected) == 3
        assert all(s["paperId"] == "A" for s in selected)

    def test_empty_returns_empty(self):
        from goa_semantic_tools.services.asta_literature_service import _select_best_paper_snippets
        assert _select_best_paper_snippets([]) == []

    def test_respects_max_total(self):
        from goa_semantic_tools.services.asta_literature_service import _select_best_paper_snippets

        snippets = [
            {"paperId": "A", "snippet_text": "a1", "score": 0.9},
            {"paperId": "A", "snippet_text": "a2", "score": 0.8},
            {"paperId": "A", "snippet_text": "a3", "score": 0.7},
            {"paperId": "B", "snippet_text": "b1", "score": 0.85},
        ]

        selected = _select_best_paper_snippets(snippets, max_from_top=3, max_from_runner_up=1, max_total=2)
        assert len(selected) == 2


# =============================================================================
# Test GAF-skip logic in fetch_snippets_for_co_annotations
# =============================================================================


@pytest.mark.unit
class TestCoAnnotationGafSkip:
    """Tests for GAF-skip logic in fetch_snippets_for_co_annotations."""

    def _make_mock_source(self, return_json):
        mock_tool = MagicMock()
        mock_tool.name = "snippet_search"
        mock_tool.handler.return_value = return_json

        mock_source = MagicMock()
        mock_source.tools = [mock_tool]

        mock_ctx = MagicMock()
        mock_ctx.__enter__ = MagicMock(return_value=mock_source)
        mock_ctx.__exit__ = MagicMock(return_value=False)
        return mock_ctx, mock_tool

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_skips_gene_when_gaf_pmid_already_has_snippets(self, mock_mcp_cls):
        """When snippet_evidence already covers the co-annotating PMID, skip."""
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations

        gaf_pmids = {
            0: [{
                "pmid": "11111111",
                "genes_covered": ["VEGFA"],
                "gene_go_map": {"VEGFA": ["GO:001", "GO:002"]},
                "gene_go_named": {
                    "VEGFA": ["sprouting angiogenesis [GO:001]", "migration [GO:002]"]
                },
            }]
        }
        themes = [{"anchor_term": {"name": "angiogenesis", "go_id": "GO:X", "genes": ["VEGFA"]}}]

        # snippet_evidence already has a snippet from PMID 11111111
        snippet_evidence = {
            0: [{"paperId": "x", "pmid": "11111111", "title": "T", "snippet_text": "ev", "score": 0.5}]
        }

        result = fetch_snippets_for_co_annotations(
            gaf_pmids, themes, "test-key",
            snippet_evidence=snippet_evidence,
        )

        # Should skip entirely — no MCP session needed
        assert result == {}
        mock_mcp_cls.assert_not_called()

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_does_not_skip_when_no_snippet_evidence(self, mock_mcp_cls):
        """Without snippet_evidence, co-annotation query should proceed."""
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations

        snippet_response = json.dumps({
            "data": [{
                "paper": {"paperId": "p1", "title": "T", "externalIds": {"PubMed": "999"}},
                "snippetText": "evidence text",
                "score": 0.6,
            }]
        })
        mock_ctx, mock_tool = self._make_mock_source(snippet_response)
        mock_mcp_cls.return_value = mock_ctx

        gaf_pmids = {
            0: [{
                "pmid": "11111111",
                "genes_covered": ["VEGFA"],
                "gene_go_map": {"VEGFA": ["GO:001", "GO:002"]},
                "gene_go_named": {
                    "VEGFA": ["sprouting angiogenesis [GO:001]", "migration [GO:002]"]
                },
            }]
        }
        themes = [{"anchor_term": {"name": "angiogenesis", "go_id": "GO:X", "genes": ["VEGFA"]}}]

        result = fetch_snippets_for_co_annotations(
            gaf_pmids, themes, "test-key",
            snippet_evidence=None,
        )

        assert 0 in result
        assert "VEGFA" in result[0]
        assert len(result[0]["VEGFA"]) > 0

    @patch("goa_semantic_tools.services.asta_literature_service.MCPToolSource")
    def test_partial_skip_only_skips_covered_genes(self, mock_mcp_cls):
        """With 2 genes, only the one with covered PMIDs should be skipped."""
        from goa_semantic_tools.services.asta_literature_service import fetch_snippets_for_co_annotations

        snippet_response = json.dumps({
            "data": [{
                "paper": {"paperId": "p1", "title": "T", "externalIds": {"PubMed": "999"}},
                "snippetText": "evidence text",
                "score": 0.6,
            }]
        })
        mock_ctx, mock_tool = self._make_mock_source(snippet_response)
        mock_mcp_cls.return_value = mock_ctx

        gaf_pmids = {
            0: [
                {
                    "pmid": "11111111",
                    "genes_covered": ["VEGFA", "FGF2"],
                    "gene_go_map": {
                        "VEGFA": ["GO:001", "GO:002"],
                        "FGF2": ["GO:003", "GO:004"],
                    },
                    "gene_go_named": {
                        "VEGFA": ["term1 [GO:001]", "term2 [GO:002]"],
                        "FGF2": ["term3 [GO:003]", "term4 [GO:004]"],
                    },
                },
                {
                    "pmid": "22222222",
                    "genes_covered": ["FGF2"],
                    "gene_go_map": {"FGF2": ["GO:003", "GO:004"]},
                    "gene_go_named": {"FGF2": ["term3 [GO:003]", "term4 [GO:004]"]},
                },
            ]
        }
        themes = [{"anchor_term": {"name": "angiogenesis", "go_id": "GO:X", "genes": ["VEGFA", "FGF2"]}}]

        # VEGFA's PMID 11111111 is covered; FGF2 has PMID 22222222 NOT covered
        snippet_evidence = {
            0: [{"paperId": "x", "pmid": "11111111", "title": "T", "snippet_text": "ev", "score": 0.5}]
        }

        result = fetch_snippets_for_co_annotations(
            gaf_pmids, themes, "test-key",
            snippet_evidence=snippet_evidence,
            max_queries_per_theme=3,
        )

        assert 0 in result
        # FGF2 should be queried (not skipped), VEGFA should be skipped
        # FGF2 has PMIDs {11111111, 22222222} — not a subset of {11111111}
        assert "FGF2" in result[0]


# =============================================================================
# Test resolve_missing_pmids
# =============================================================================


@pytest.mark.unit
class TestResolveMissingPmids:
    """Tests for resolve_missing_pmids."""

    def test_skips_snippets_with_pmid(self):
        """Snippets that already have a PMID should not be resolved."""
        from goa_semantic_tools.services.asta_literature_service import resolve_missing_pmids

        snippets = [
            {"paperId": "abc123", "pmid": "19188590", "snippet_text": "text"},
        ]

        # Should not even open an ASTA source since no resolution needed
        with patch("goa_semantic_tools.services.asta_literature_service._open_asta_source") as mock_source:
            result = resolve_missing_pmids(snippets, "test-key")

        mock_source.assert_not_called()
        assert result[0]["pmid"] == "19188590"

    def test_resolves_missing_pmid(self):
        """Snippets with paperId but no PMID should be resolved via batch API."""
        from goa_semantic_tools.services.asta_literature_service import resolve_missing_pmids

        snippets = [
            {"paperId": "abc123", "pmid": "", "snippet_text": "text1"},
            {"paperId": "def456", "pmid": "", "snippet_text": "text2"},
        ]

        mock_batch_tool = MagicMock()
        mock_batch_tool.name = "get_paper_batch"
        mock_batch_tool.handler.return_value = json.dumps([
            {"paperId": "abc123", "externalIds": {"PubMed": "11111111"}},
            {"paperId": "def456", "externalIds": {"PubMed": "22222222"}},
        ])

        mock_source = MagicMock()
        mock_source.tools = [mock_batch_tool]
        mock_source.__enter__ = MagicMock(return_value=mock_source)
        mock_source.__exit__ = MagicMock(return_value=False)

        with patch("goa_semantic_tools.services.asta_literature_service._open_asta_source", return_value=mock_source):
            result = resolve_missing_pmids(snippets, "test-key")

        assert result[0]["pmid"] == "11111111"
        assert result[1]["pmid"] == "22222222"

    def test_handles_missing_batch_tool(self):
        """Should return snippets unchanged if get_paper_batch not found."""
        from goa_semantic_tools.services.asta_literature_service import resolve_missing_pmids

        snippets = [{"paperId": "abc123", "pmid": "", "snippet_text": "text"}]

        mock_source = MagicMock()
        mock_source.tools = []  # No tools
        mock_source.__enter__ = MagicMock(return_value=mock_source)
        mock_source.__exit__ = MagicMock(return_value=False)

        with patch("goa_semantic_tools.services.asta_literature_service._open_asta_source", return_value=mock_source):
            result = resolve_missing_pmids(snippets, "test-key")

        assert result[0]["pmid"] == ""

    def test_handles_partial_resolution(self):
        """Some papers may not have PMIDs — those should remain empty."""
        from goa_semantic_tools.services.asta_literature_service import resolve_missing_pmids

        snippets = [
            {"paperId": "abc123", "pmid": "", "snippet_text": "text1"},
            {"paperId": "def456", "pmid": "", "snippet_text": "text2"},
        ]

        mock_batch_tool = MagicMock()
        mock_batch_tool.name = "get_paper_batch"
        mock_batch_tool.handler.return_value = json.dumps([
            {"paperId": "abc123", "externalIds": {"PubMed": "11111111"}},
            {"paperId": "def456", "externalIds": {}},  # No PMID
        ])

        mock_source = MagicMock()
        mock_source.tools = [mock_batch_tool]
        mock_source.__enter__ = MagicMock(return_value=mock_source)
        mock_source.__exit__ = MagicMock(return_value=False)

        with patch("goa_semantic_tools.services.asta_literature_service._open_asta_source", return_value=mock_source):
            result = resolve_missing_pmids(snippets, "test-key")

        assert result[0]["pmid"] == "11111111"
        assert result[1]["pmid"] == ""

    def test_empty_snippets(self):
        """Empty list should be returned immediately."""
        from goa_semantic_tools.services.asta_literature_service import resolve_missing_pmids

        result = resolve_missing_pmids([], "test-key")
        assert result == []


# =============================================================================
# Test fetch_snippets_for_cross_theme_pmids
# =============================================================================


@pytest.mark.unit
class TestFetchSnippetsForCrossThemePmids:
    """Tests for fetch_snippets_for_cross_theme_pmids."""

    def test_builds_scoped_queries(self):
        """Should build queries scoped to each gene's PMIDs."""
        from goa_semantic_tools.services.asta_literature_service import (
            fetch_snippets_for_cross_theme_pmids,
        )

        cross_theme_index = {
            "FOXO3": [
                {
                    "pmid": "111",
                    "themes": [{"index": 0, "name": "migration"}, {"index": 1, "name": "apoptosis"}],
                    "annotations": ["migration: cell motility", "apoptosis: cell death"],
                },
            ],
        }

        mock_snippet_tool = MagicMock()
        mock_snippet_tool.name = "snippet_search"
        mock_snippet_tool.handler.return_value = json.dumps({
            "data": [
                {
                    "paper": {
                        "paperId": "x1",
                        "title": "FOXO3 paper",
                        "externalIds": {"PubMed": "111"},
                    },
                    "snippet": {"text": "FOXO3 suppresses migration..."},
                    "score": 0.8,
                }
            ]
        })

        mock_source = MagicMock()
        mock_source.tools = [mock_snippet_tool]
        mock_source.__enter__ = MagicMock(return_value=mock_source)
        mock_source.__exit__ = MagicMock(return_value=False)

        with patch("goa_semantic_tools.services.asta_literature_service._open_asta_source", return_value=mock_source):
            result = fetch_snippets_for_cross_theme_pmids(cross_theme_index, "test-key")

        assert "FOXO3" in result
        assert len(result["FOXO3"]) == 1

        # Verify query was scoped to PMIDs
        call_args = mock_snippet_tool.handler.call_args[0][0]
        assert "PMID:111" in call_args["paper_ids"]

    def test_empty_index_returns_empty(self):
        from goa_semantic_tools.services.asta_literature_service import (
            fetch_snippets_for_cross_theme_pmids,
        )

        result = fetch_snippets_for_cross_theme_pmids({}, "test-key")
        assert result == {}

    def test_respects_max_genes(self):
        from goa_semantic_tools.services.asta_literature_service import (
            fetch_snippets_for_cross_theme_pmids,
        )

        # Create 5 genes
        cross_theme_index = {
            f"GENE{i}": [{"pmid": str(i), "themes": [{"index": 0, "name": "t0"}, {"index": 1, "name": "t1"}], "annotations": []}]
            for i in range(5)
        }

        mock_snippet_tool = MagicMock()
        mock_snippet_tool.name = "snippet_search"
        mock_snippet_tool.handler.return_value = json.dumps({"data": []})

        mock_source = MagicMock()
        mock_source.tools = [mock_snippet_tool]
        mock_source.__enter__ = MagicMock(return_value=mock_source)
        mock_source.__exit__ = MagicMock(return_value=False)

        with patch("goa_semantic_tools.services.asta_literature_service._open_asta_source", return_value=mock_source):
            result = fetch_snippets_for_cross_theme_pmids(
                cross_theme_index, "test-key", max_genes=2
            )

        # Should only query 2 genes
        assert mock_snippet_tool.handler.call_count == 2
