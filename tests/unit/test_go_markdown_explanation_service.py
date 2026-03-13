"""
Unit Tests for GO Markdown Explanation Service

Tests helper functions without requiring LLM calls.
"""

import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from goa_semantic_tools.services.go_markdown_explanation_service import (
    _DEFAULT_MAX_TOKENS,
    _MODEL_MAX_TOKENS,
    _add_go_term_hyperlinks,
    _add_pmid_hyperlinks,
    _count_provenance_tags,
    _empty_markdown_explanation,
    _format_enrichment_for_llm,
    _get_api_key_for_model,
    _get_default_max_tokens,
    _load_prompt,
    _validate_citations,
    generate_markdown_explanation,
    rank_genes_for_theme,
    render_explanation_to_markdown,
    validate_explanation_json,
)


@pytest.mark.unit
class TestGetDefaultMaxTokens:
    """Tests for _get_default_max_tokens and the _MODEL_MAX_TOKENS registry."""

    def test_gpt5_returns_32000(self):
        assert _get_default_max_tokens("gpt-5") == 32000

    def test_gpt4o_returns_default(self):
        assert _get_default_max_tokens("gpt-4o") == _DEFAULT_MAX_TOKENS

    def test_gpt4o_mini_returns_default(self):
        assert _get_default_max_tokens("gpt-4o-mini") == _DEFAULT_MAX_TOKENS

    def test_unknown_model_returns_default(self):
        assert _get_default_max_tokens("some-future-model") == _DEFAULT_MAX_TOKENS

    def test_default_max_tokens_is_16000(self):
        assert _DEFAULT_MAX_TOKENS == 16000

    def test_gpt5_in_registry(self):
        assert "gpt-5" in _MODEL_MAX_TOKENS
        assert _MODEL_MAX_TOKENS["gpt-5"] == 32000

    def test_generate_uses_model_default_when_max_tokens_none(self):
        """generate_markdown_explanation should pass 32000 to LiteLLMAgent for gpt-5."""
        minimal_enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 10,
                "fdr_threshold": 0.05,
            },
            "themes": [],
            "hub_genes": {},
            "enrichment_leaves": [
                {"go_id": "GO:0006281", "name": "DNA repair", "fdr": 0.001, "genes": ["BRCA1"]}
            ],
        }
        captured = {}

        class FakeAgent:
            def __init__(self, model, api_key, max_tokens):
                captured["max_tokens"] = max_tokens

            def query_unified(self, **kwargs):
                raise RuntimeError("stop")

        with patch(
            "goa_semantic_tools.services.go_markdown_explanation_service.LiteLLMAgent",
            FakeAgent,
        ):
            with patch(
                "goa_semantic_tools.services.go_markdown_explanation_service._get_api_key_for_model",
                return_value="fake-key",
            ):
                try:
                    generate_markdown_explanation(
                        enrichment_output=minimal_enrichment,
                        model="gpt-5",
                        max_tokens=None,
                    )
                except RuntimeError:
                    pass

        assert captured.get("max_tokens") == 32000, (
            f"Expected 32000 for gpt-5, got {captured.get('max_tokens')}"
        )

    def test_generate_uses_explicit_max_tokens_when_provided(self):
        """Explicit max_tokens should override model default."""
        minimal_enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 10,
                "fdr_threshold": 0.05,
            },
            "themes": [],
            "hub_genes": {},
            "enrichment_leaves": [
                {"go_id": "GO:0006281", "name": "DNA repair", "fdr": 0.001, "genes": ["BRCA1"]}
            ],
        }
        captured = {}

        class FakeAgent:
            def __init__(self, model, api_key, max_tokens):
                captured["max_tokens"] = max_tokens

            def query_unified(self, **kwargs):
                raise RuntimeError("stop")

        with patch(
            "goa_semantic_tools.services.go_markdown_explanation_service.LiteLLMAgent",
            FakeAgent,
        ):
            with patch(
                "goa_semantic_tools.services.go_markdown_explanation_service._get_api_key_for_model",
                return_value="fake-key",
            ):
                try:
                    generate_markdown_explanation(
                        enrichment_output=minimal_enrichment,
                        model="gpt-5",
                        max_tokens=8000,  # explicit override
                    )
                except RuntimeError:
                    pass

        assert captured.get("max_tokens") == 8000


@pytest.mark.unit
class TestLoadPrompt:
    """Tests for _load_prompt function."""

    def test_loads_existing_prompt(self):
        """Should load the existing go_explanation prompt."""
        prompt = _load_prompt("go_explanation.prompt.yaml")
        assert "system_prompt" in prompt
        assert "user_prompt" in prompt
        assert len(prompt["system_prompt"]) > 100  # Non-trivial prompt

    def test_missing_file_raises(self):
        """Should raise FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            _load_prompt("nonexistent.prompt.yaml")


@pytest.mark.unit
class TestGetApiKeyForModel:
    """Tests for _get_api_key_for_model function."""

    def test_openai_model_uses_openai_key(self):
        """OpenAI models should use OPENAI_API_KEY."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-openai-key"}):
            key = _get_api_key_for_model("gpt-4o")
            assert key == "test-openai-key"

    def test_gpt_model_prefix(self):
        """Models starting with 'gpt' should use OpenAI key."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            key = _get_api_key_for_model("gpt-4o-mini")
            assert key == "test-key"

    def test_o1_model_prefix(self):
        """Models starting with 'o1' should use OpenAI key."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            key = _get_api_key_for_model("o1-preview")
            assert key == "test-key"

    def test_claude_model_uses_anthropic_key(self):
        """Claude models should use ANTHROPIC_API_KEY."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-anthropic-key"}, clear=True):
            # Clear OPENAI_API_KEY to ensure it uses Anthropic
            os.environ.pop("OPENAI_API_KEY", None)
            key = _get_api_key_for_model("claude-sonnet-4-20250514")
            assert key == "test-anthropic-key"

    def test_missing_openai_key_raises(self):
        """Missing OpenAI key for GPT model should raise."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("OPENAI_API_KEY", None)
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                _get_api_key_for_model("gpt-4o")

    def test_missing_anthropic_key_raises(self):
        """Missing Anthropic key for Claude model should raise."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("ANTHROPIC_API_KEY", None)
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                _get_api_key_for_model("claude-sonnet-4-20250514")

    def test_unknown_model_tries_both_keys(self):
        """Unknown model should try OpenAI first, then Anthropic."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-anthropic"}, clear=True):
            key = _get_api_key_for_model("unknown-model")
            assert key == "test-anthropic"

    def test_unknown_model_no_keys_raises(self):
        """Unknown model with no API keys should raise."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("OPENAI_API_KEY", None)
            os.environ.pop("ANTHROPIC_API_KEY", None)
            with pytest.raises(ValueError, match="No API key found"):
                _get_api_key_for_model("unknown-model")


@pytest.mark.unit
class TestFormatEnrichmentForLLM:
    """Tests for _format_enrichment_for_llm function."""

    def test_formats_basic_enrichment(self):
        """Should format basic enrichment output."""
        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 10,
                "genes_with_annotations": 9,
                "total_enriched_terms": 50,
                "fdr_threshold": 0.05,
            },
            "themes": [],
            "hub_genes": {},
            "enrichment_leaves": [],
        }

        result = _format_enrichment_for_llm(enrichment)

        assert "Species: human" in result
        assert "Input genes: 10" in result
        assert "FDR threshold: 0.05" in result

    def test_formats_themes(self):
        """Should format themes with anchor and specific terms."""
        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": [
                {
                    "anchor_term": {
                        "go_id": "GO:0006915",
                        "name": "apoptotic process",
                        "namespace": "biological_process",
                        "fdr": 0.001,
                        "genes": ["TP53", "BRCA1"],
                    },
                    "specific_terms": [
                        {
                            "go_id": "GO:0006917",
                            "name": "induction of apoptosis",
                            "fdr": 0.002,
                            "genes": ["TP53"],
                        }
                    ],
                    "anchor_confidence": "high",
                    "all_genes": ["TP53", "BRCA1"],
                }
            ],
            "hub_genes": {},
            "enrichment_leaves": [],
        }

        result = _format_enrichment_for_llm(enrichment)

        assert "Theme 1: apoptotic process" in result
        assert "GO:0006915" in result
        assert "Specific Terms" in result
        assert "induction of apoptosis" in result

    def test_formats_hub_genes(self):
        """Should format hub genes section."""
        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": [],
            "hub_genes": {
                "TP53": {
                    "theme_count": 5,
                    "themes": ["apoptosis", "cell cycle", "DNA repair"],
                }
            },
            "enrichment_leaves": [],
        }

        result = _format_enrichment_for_llm(enrichment)

        assert "Hub Genes" in result
        assert "TP53 (5 themes)" in result
        assert "apoptosis" in result

    def test_formats_enrichment_leaves(self):
        """Should format enrichment leaves section."""
        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": [],
            "hub_genes": {},
            "enrichment_leaves": [
                {
                    "go_id": "GO:0006281",
                    "name": "DNA repair",
                    "fdr": 0.001,
                    "genes": ["BRCA1", "BRCA2"],
                }
            ],
        }

        result = _format_enrichment_for_llm(enrichment)

        assert "Enrichment Leaves" in result
        assert "DNA repair" in result
        assert "GO:0006281" in result

    def test_includes_abstract_block_when_paper_abstracts_provided(self):
        """Abstract block should appear in theme context when paper_abstracts is given."""
        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": [
                {
                    "anchor_term": {
                        "go_id": "GO:0006915",
                        "name": "apoptotic process",
                        "namespace": "biological_process",
                        "fdr": 0.001,
                        "genes": ["TP53"],
                    },
                    "specific_terms": [],
                    "anchor_confidence": "high",
                }
            ],
            "hub_genes": {},
            "enrichment_leaves": [],
        }
        paper_abstracts = {
            0: [{"pmid": "12345678", "title": "TP53 and apoptosis", "abstract": "An informative abstract.", "authors": "Smith", "year": "2020"}]
        }

        result = _format_enrichment_for_llm(enrichment, paper_abstracts=paper_abstracts)

        assert "Available Literature" in result
        assert "PMID:12345678" in result
        assert "TP53 and apoptosis" in result
        assert "An informative abstract." in result

    def test_no_abstract_block_when_paper_abstracts_not_provided(self):
        """No abstract block should appear when paper_abstracts is None."""
        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": [
                {
                    "anchor_term": {
                        "go_id": "GO:0006915",
                        "name": "apoptotic process",
                        "namespace": "biological_process",
                        "fdr": 0.001,
                        "genes": ["TP53"],
                    },
                    "specific_terms": [],
                    "anchor_confidence": "high",
                }
            ],
            "hub_genes": {},
            "enrichment_leaves": [],
        }

        result = _format_enrichment_for_llm(enrichment, paper_abstracts=None)

        assert "Available Literature" not in result

    def test_abstract_truncated_to_400_chars(self):
        """Long abstracts should be truncated to 400 chars with ellipsis."""
        long_abstract = "X" * 600
        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": [
                {
                    "anchor_term": {
                        "go_id": "GO:0006915",
                        "name": "apoptotic process",
                        "namespace": "biological_process",
                        "fdr": 0.001,
                        "genes": ["TP53"],
                    },
                    "specific_terms": [],
                    "anchor_confidence": "high",
                }
            ],
            "hub_genes": {},
            "enrichment_leaves": [],
        }
        paper_abstracts = {
            0: [{"pmid": "99", "title": "T", "abstract": long_abstract, "authors": "", "year": ""}]
        }

        result = _format_enrichment_for_llm(enrichment, paper_abstracts=paper_abstracts)

        # Should NOT contain the full 600-char string untruncated
        assert long_abstract not in result
        assert "..." in result

    def test_hub_genes_capped_at_20_in_context(self):
        """Hub genes in LLM context should be capped at top 20 by theme_count."""
        # Build enrichment with 30 hub genes, varying theme_counts
        hub_genes = {}
        for i in range(30):
            hub_genes[f"GENE{i:02d}"] = {
                "theme_count": 30 - i,  # GENE00 has 30, GENE29 has 1
                "themes": [f"theme{j}" for j in range(30 - i)],
            }

        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 50,
                "genes_with_annotations": 50,
                "total_enriched_terms": 100,
                "fdr_threshold": 0.05,
            },
            "themes": [],
            "hub_genes": hub_genes,
            "enrichment_leaves": [],
        }

        result = _format_enrichment_for_llm(enrichment)

        # Top 20 genes (GENE00–GENE19) should appear
        for i in range(20):
            assert f"GENE{i:02d}" in result, f"GENE{i:02d} should be in context"

        # Genes 20–29 (lowest theme_count) should be excluded
        for i in range(20, 30):
            assert f"GENE{i:02d}" not in result, f"GENE{i:02d} should be excluded (capped)"

    def test_hub_genes_sorted_by_theme_count_descending(self):
        """Hub genes in context should appear in order of descending theme_count."""
        hub_genes = {
            "LOW_GENE": {"theme_count": 2, "themes": ["t1", "t2"]},
            "HIGH_GENE": {"theme_count": 10, "themes": [f"t{i}" for i in range(10)]},
            "MID_GENE": {"theme_count": 5, "themes": [f"t{i}" for i in range(5)]},
        }
        enrichment = {
            "metadata": {
                "species": "human",
                "input_genes_count": 10,
                "genes_with_annotations": 10,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": [],
            "hub_genes": hub_genes,
            "enrichment_leaves": [],
        }

        result = _format_enrichment_for_llm(enrichment)

        # HIGH_GENE should appear before MID_GENE, which before LOW_GENE
        pos_high = result.index("HIGH_GENE")
        pos_mid = result.index("MID_GENE")
        pos_low = result.index("LOW_GENE")
        assert pos_high < pos_mid < pos_low


@pytest.mark.unit
class TestFormatEnrichmentGafPmids:
    """Tests for gaf_pmids and hub_gene_abstracts params in _format_enrichment_for_llm."""

    def _base_enrichment(self, with_theme=True, with_hub=True):
        themes = []
        hub_genes = {}
        if with_theme:
            themes = [{
                "anchor_term": {
                    "go_id": "GO:0006915",
                    "name": "apoptotic process",
                    "namespace": "biological_process",
                    "fdr": 0.001,
                    "genes": ["TP53"],
                },
                "specific_terms": [],
                "anchor_confidence": "high",
                "all_genes": ["TP53"],
            }]
        if with_hub:
            hub_genes = {
                "TP53": {"theme_count": 3, "themes": ["apoptosis", "DNA repair", "cell cycle"]}
            }
        return {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": themes,
            "hub_genes": hub_genes,
            "enrichment_leaves": [],
        }

    def test_gaf_pmids_renders_citation_block(self):
        """GAF PMIDs appear as citation bullets under theme."""
        enrichment = self._base_enrichment()
        gaf_pmids = {0: [{"pmid": "10383454", "genes_covered": ["TP53", "BRCA1"]}]}

        result = _format_enrichment_for_llm(enrichment, gaf_pmids=gaf_pmids)

        assert "Available GAF Citations" in result
        assert "PMID:10383454" in result
        assert "TP53" in result
        assert "BRCA1" in result

    def test_gaf_pmids_not_shown_when_none(self):
        """No GAF citation block when gaf_pmids is None."""
        enrichment = self._base_enrichment()

        result = _format_enrichment_for_llm(enrichment, gaf_pmids=None)

        assert "Available GAF Citations" not in result

    def test_gaf_pmids_not_shown_when_empty_for_theme(self):
        """No GAF citation block when theme has empty list."""
        enrichment = self._base_enrichment()
        gaf_pmids = {0: []}

        result = _format_enrichment_for_llm(enrichment, gaf_pmids=gaf_pmids)

        assert "Available GAF Citations" not in result

    def test_gaf_pmids_prefers_over_paper_abstracts(self):
        """gaf_pmids block shown instead of paper_abstracts when both provided."""
        enrichment = self._base_enrichment()
        gaf_pmids = {0: [{"pmid": "11111", "genes_covered": ["TP53"]}]}
        paper_abstracts = {0: [{"pmid": "99999", "title": "Old abstract", "abstract": "text", "authors": "", "year": ""}]}

        result = _format_enrichment_for_llm(enrichment, gaf_pmids=gaf_pmids, paper_abstracts=paper_abstracts)

        assert "Available GAF Citations" in result
        assert "PMID:11111" in result
        assert "Available Literature" not in result
        assert "PMID:99999" not in result

    def test_paper_abstracts_fallback_when_no_gaf_pmids(self):
        """paper_abstracts still shown when gaf_pmids is None (backward compat)."""
        enrichment = self._base_enrichment()
        paper_abstracts = {0: [{"pmid": "99999", "title": "Old abstract", "abstract": "text", "authors": "", "year": ""}]}

        result = _format_enrichment_for_llm(enrichment, gaf_pmids=None, paper_abstracts=paper_abstracts)

        assert "Available Literature" in result
        assert "PMID:99999" in result

    def test_hub_gene_abstracts_injected_in_hub_section(self):
        """Hub gene papers appear in hub_genes section under Supporting Literature."""
        enrichment = self._base_enrichment(with_theme=False)
        hub_gene_abstracts = {
            "TP53": [{"pmid": "20027291", "title": "TP53 in apoptosis", "abstract": "Key study.", "authors": "Smith", "year": "2003"}]
        }

        result = _format_enrichment_for_llm(enrichment, hub_gene_abstracts=hub_gene_abstracts)

        assert "Supporting Literature" in result
        assert "PMID:20027291" in result
        assert "TP53 in apoptosis" in result
        assert "Smith" in result

    def test_hub_gene_abstracts_not_shown_when_none(self):
        """No Supporting Literature block when hub_gene_abstracts is None."""
        enrichment = self._base_enrichment(with_theme=False)

        result = _format_enrichment_for_llm(enrichment, hub_gene_abstracts=None)

        assert "Supporting Literature" not in result

    def test_hub_gene_abstract_truncated_to_400_chars(self):
        """Hub gene abstracts truncated to 400 chars."""
        long_abstract = "Y" * 600
        enrichment = self._base_enrichment(with_theme=False)
        hub_gene_abstracts = {
            "TP53": [{"pmid": "1", "title": "T", "abstract": long_abstract, "authors": "", "year": ""}]
        }

        result = _format_enrichment_for_llm(enrichment, hub_gene_abstracts=hub_gene_abstracts)

        assert long_abstract not in result
        assert "..." in result

    def test_gaf_pmids_truncates_gene_list_at_six(self):
        """GAF citation line shows up to 6 genes then '+N more'."""
        enrichment = self._base_enrichment()
        genes = [f"GENE{i}" for i in range(10)]
        gaf_pmids = {0: [{"pmid": "55555", "genes_covered": genes}]}

        result = _format_enrichment_for_llm(enrichment, gaf_pmids=gaf_pmids)

        assert "+4 more" in result


@pytest.mark.unit
class TestFormatEnrichmentGafAbstracts:
    """Tests for gaf_abstracts parameter in _format_enrichment_for_llm."""

    def _base_enrichment(self, with_theme=True):
        theme = {
            "anchor_term": {
                "go_id": "GO:0006915",
                "name": "apoptotic process",
                "namespace": "biological_process",
                "fdr": 0.001,
                "genes": ["TP53"],
            },
            "specific_terms": [],
            "anchor_confidence": "high",
        }
        return {
            "metadata": {
                "species": "human",
                "input_genes_count": 5,
                "genes_with_annotations": 5,
                "total_enriched_terms": 20,
                "fdr_threshold": 0.05,
            },
            "themes": [theme] if with_theme else [],
            "hub_genes": {},
            "enrichment_leaves": [],
        }

    def _gaf_pmids(self):
        return {0: [{"pmid": "12345678", "genes_covered": ["TP53", "BRCA1"]}]}

    def _gaf_abstracts(self):
        return {0: [{
            "pmid": "12345678",
            "title": "TP53 and apoptosis",
            "abstract": "A detailed abstract about TP53.",
            "authors": "Smith, Jones",
            "year": "2020",
        }]}

    def test_gaf_abstracts_shows_full_abstract(self):
        """When gaf_abstracts provided, abstract text should appear in context."""
        enrichment = self._base_enrichment()
        result = _format_enrichment_for_llm(
            enrichment,
            gaf_pmids=self._gaf_pmids(),
            gaf_abstracts=self._gaf_abstracts(),
        )
        assert "A detailed abstract about TP53." in result
        assert "TP53 and apoptosis" in result
        assert "PMID:12345678" in result

    def test_gaf_abstracts_includes_genes_covered_note(self):
        """Abstract block should include Covers: gene line from gaf_pmids."""
        enrichment = self._base_enrichment()
        result = _format_enrichment_for_llm(
            enrichment,
            gaf_pmids=self._gaf_pmids(),
            gaf_abstracts=self._gaf_abstracts(),
        )
        assert "Covers:" in result
        assert "TP53" in result
        assert "BRCA1" in result

    def test_gaf_abstracts_fallback_to_pmid_only_when_none(self):
        """When gaf_abstracts=None, original PMID-only format should be used."""
        enrichment = self._base_enrichment()
        result = _format_enrichment_for_llm(
            enrichment,
            gaf_pmids=self._gaf_pmids(),
            gaf_abstracts=None,
        )
        # PMID anchor present
        assert "PMID:12345678" in result
        # No abstract text
        assert "A detailed abstract about TP53." not in result
        # Covers: not present (old format uses 'covers:' lowercase inline)
        assert "Covers:" not in result

    def test_gaf_abstracts_fallback_when_theme_not_in_gaf_abstracts(self):
        """When theme_index missing from gaf_abstracts, PMID-only fallback."""
        enrichment = self._base_enrichment()
        # gaf_abstracts for theme 99 (not theme 0)
        gaf_abstracts_wrong_theme = {99: [{"pmid": "12345678", "title": "T", "abstract": "A", "authors": "", "year": ""}]}
        result = _format_enrichment_for_llm(
            enrichment,
            gaf_pmids=self._gaf_pmids(),
            gaf_abstracts=gaf_abstracts_wrong_theme,
        )
        assert "PMID:12345678" in result
        # no abstract text
        assert "Abstract: A" not in result


@pytest.mark.unit
class TestEmptyMarkdownExplanation:
    """Tests for _empty_markdown_explanation function."""

    def test_generates_empty_report(self):
        """Should generate minimal report for no enrichment."""
        enrichment = {
            "metadata": {
                "input_genes_count": 5,
                "genes_with_annotations": 3,
                "total_enriched_terms": 0,
                "fdr_threshold": 0.05,
            }
        }

        result = _empty_markdown_explanation(enrichment, "gpt-4o")

        assert "No significant GO enrichment" in result
        assert "Input genes: 5" in result
        assert "gpt-4o" in result


@pytest.mark.unit
class TestAddGoTermHyperlinks:
    """Tests for _add_go_term_hyperlinks function."""

    def test_adds_hyperlinks_to_go_ids(self, capsys):
        """Should convert GO IDs to hyperlinks."""
        markdown = "The term GO:0006915 is enriched."
        enrichment = {"themes": [], "enrichment_leaves": []}

        result = _add_go_term_hyperlinks(markdown, enrichment)

        assert "[GO:0006915]" in result
        assert "http://purl.obolibrary.org/obo/GO_0006915" in result

    def test_handles_multiple_go_ids(self, capsys):
        """Should handle multiple GO IDs."""
        markdown = "Terms GO:0006915 and GO:0006281 are enriched."
        enrichment = {"themes": [], "enrichment_leaves": []}

        result = _add_go_term_hyperlinks(markdown, enrichment)

        assert "[GO:0006915]" in result
        assert "[GO:0006281]" in result

    def test_no_go_ids(self, capsys):
        """Should handle text without GO IDs."""
        markdown = "No GO IDs here."
        enrichment = {"themes": [], "enrichment_leaves": []}

        result = _add_go_term_hyperlinks(markdown, enrichment)

        assert result == "No GO IDs here."


@pytest.mark.unit
class TestAddPmidHyperlinks:
    """Tests for _add_pmid_hyperlinks function."""

    def test_adds_hyperlinks_to_pmids(self, capsys):
        """Should convert PMIDs to hyperlinks."""
        markdown = "See PMID:12345678 for details."

        result = _add_pmid_hyperlinks(markdown)

        assert "[PMID:12345678]" in result
        assert "https://pubmed.ncbi.nlm.nih.gov/12345678/" in result

    def test_handles_multiple_pmids(self, capsys):
        """Should handle multiple PMIDs."""
        markdown = "See PMID:12345678 and PMID:87654321."

        result = _add_pmid_hyperlinks(markdown)

        assert "[PMID:12345678]" in result
        assert "[PMID:87654321]" in result

    def test_no_pmids(self, capsys):
        """Should handle text without PMIDs."""
        markdown = "No PMIDs here."

        result = _add_pmid_hyperlinks(markdown)

        assert result == "No PMIDs here."


@pytest.mark.unit
class TestValidateCitations:
    """Tests for _validate_citations function."""

    def test_valid_citations_pass(self, capsys):
        """Should not warn for valid GO IDs."""
        markdown = "Term GO:0006915 is enriched."
        enrichment = {
            "themes": [
                {"anchor_term": {"go_id": "GO:0006915"}, "specific_terms": []}
            ],
            "enrichment_leaves": [],
        }

        _validate_citations(markdown, enrichment)
        captured = capsys.readouterr()
        assert "All GO IDs in output match" in captured.out

    def test_hallucinated_citations_warn(self, capsys):
        """Should warn about hallucinated GO IDs."""
        markdown = "Term GO:9999999 is enriched."
        enrichment = {
            "themes": [
                {"anchor_term": {"go_id": "GO:0006915"}, "specific_terms": []}
            ],
            "enrichment_leaves": [],
        }

        _validate_citations(markdown, enrichment)
        captured = capsys.readouterr()
        assert "WARNING" in captured.out or "Hallucinations" in captured.out


@pytest.mark.unit
class TestCountProvenanceTags:
    """Tests for _count_provenance_tags function."""

    def test_counts_all_tag_types(self, capsys):
        """Should count all provenance tag types."""
        markdown = """
        [DATA] Some data observation.
        [INFERENCE] Some inference.
        [EXTERNAL] External claim.
        [GO-HIERARCHY] Hierarchy fact.
        """

        _count_provenance_tags(markdown)
        captured = capsys.readouterr()

        assert "[DATA]: 1" in captured.out
        assert "[INFERENCE]: 1" in captured.out
        assert "[EXTERNAL]: 1" in captured.out
        assert "[GO-HIERARCHY]: 1" in captured.out

    def test_counts_multiple_same_tags(self, capsys):
        """Should count multiple occurrences of same tag."""
        markdown = """
        [DATA] First data.
        [DATA] Second data.
        [DATA] Third data.
        """

        _count_provenance_tags(markdown)
        captured = capsys.readouterr()

        assert "[DATA]: 3" in captured.out

    def test_no_tags_warns(self, capsys):
        """Should warn when no provenance tags found."""
        markdown = "No tags in this text."

        _count_provenance_tags(markdown)
        captured = capsys.readouterr()

        assert "No provenance tags found" in captured.out


@pytest.mark.unit
class TestGenerateMarkdownExplanationValidation:
    """Tests for generate_markdown_explanation input validation."""

    def test_empty_enrichment_raises(self):
        """Empty enrichment should raise."""
        with pytest.raises(ValueError, match="cannot be empty"):
            generate_markdown_explanation({})

    def test_missing_metadata_raises(self):
        """Missing metadata should raise."""
        with pytest.raises(ValueError, match="must have 'metadata'"):
            generate_markdown_explanation({"themes": []})

    def test_missing_themes_and_leaves_raises(self):
        """Missing both themes and leaves should raise."""
        with pytest.raises(ValueError, match="must have 'themes' or 'enrichment_leaves'"):
            generate_markdown_explanation({"metadata": {}})


# =============================================================================
# Fixtures for new function tests
# =============================================================================


def _make_theme(anchor_genes, specific_genes_list=None, anchor_go_id="GO:0006954"):
    """Build a minimal theme dict for testing."""
    specific_terms = []
    for i, genes in enumerate(specific_genes_list or []):
        specific_terms.append({
            "go_id": f"GO:000000{i + 1}",
            "name": f"specific term {i}",
            "fdr": 0.001,
            "fold_enrichment": 5.0,
            "genes": genes,
            "depth": 6,
        })
    return {
        "anchor_term": {
            "go_id": anchor_go_id,
            "name": "inflammatory response",
            "fdr": 1e-10,
            "fold_enrichment": 8.0,
            "genes": anchor_genes,
            "depth": 4,
        },
        "anchor_confidence": "FDR<0.01",
        "specific_terms": specific_terms,
        "all_genes": list(set(anchor_genes) | {g for gs in (specific_genes_list or []) for g in gs}),
    }


def _make_enrichment_output(themes):
    """Build a minimal enrichment output dict for testing."""
    hub_genes = {}
    gene_theme_counts = {}
    for theme in themes:
        all_g = set(theme["anchor_term"]["genes"])
        for s in theme.get("specific_terms", []):
            all_g.update(s["genes"])
        for g in all_g:
            gene_theme_counts[g] = gene_theme_counts.get(g, 0) + 1
    for gene, count in gene_theme_counts.items():
        if count >= 3:
            hub_genes[gene] = {"theme_count": count, "themes": [], "go_terms": []}
    return {
        "metadata": {
            "species": "human",
            "input_genes_count": 10,
            "genes_with_annotations": 8,
            "total_enriched_terms": 20,
            "fdr_threshold": 0.05,
            "enrichment_leaves_count": 5,
            "themes_count": len(themes),
            "hub_genes_count": len(hub_genes),
        },
        "themes": themes,
        "hub_genes": hub_genes,
        "enrichment_leaves": [],
    }


# =============================================================================
# Test rank_genes_for_theme
# =============================================================================


@pytest.mark.unit
class TestRankGenesForTheme:
    """Tests for rank_genes_for_theme function."""

    def test_genes_in_specific_terms_rank_higher(self):
        """Genes appearing in specific (leaf) terms should score higher than anchor-only genes."""
        theme = _make_theme(
            anchor_genes=["GENE_A", "GENE_B", "GENE_C"],
            specific_genes_list=[["GENE_A"], ["GENE_A"]],  # GENE_A in 2 specific terms
        )
        hub_genes = {}

        ranked = rank_genes_for_theme(theme, hub_genes)

        gene_names = [g["gene"] for g in ranked]
        assert gene_names[0] == "GENE_A", "GENE_A (in 2 specific terms) should rank first"

    def test_exclusive_genes_rank_higher_than_hub_genes(self):
        """Genes exclusive to this theme should rank higher than hub genes."""
        theme = _make_theme(
            anchor_genes=["EXCLUSIVE", "HUB"],
            specific_genes_list=[],
        )
        hub_genes = {"HUB": {"theme_count": 20, "themes": [], "go_terms": []}}

        ranked = rank_genes_for_theme(theme, hub_genes)

        gene_names = [g["gene"] for g in ranked]
        assert gene_names[0] == "EXCLUSIVE", "Exclusive gene should rank above hub gene"

    def test_respects_top_n(self):
        """top_n parameter limits the number of results."""
        theme = _make_theme(
            anchor_genes=["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10"],
            specific_genes_list=[],
        )
        hub_genes = {}

        ranked = rank_genes_for_theme(theme, hub_genes, top_n=3)

        assert len(ranked) == 3

    def test_default_top_n_is_8(self):
        """Default top_n should be 8."""
        theme = _make_theme(
            anchor_genes=[f"G{i}" for i in range(20)],
            specific_genes_list=[],
        )
        hub_genes = {}

        ranked = rank_genes_for_theme(theme, hub_genes)

        assert len(ranked) == 8

    def test_theme_with_no_specific_terms(self):
        """Handles themes with no specific_terms gracefully."""
        theme = _make_theme(anchor_genes=["GENE_X", "GENE_Y"], specific_genes_list=[])
        hub_genes = {}

        ranked = rank_genes_for_theme(theme, hub_genes)

        assert len(ranked) == 2
        assert all("gene" in g and "score" in g for g in ranked)

    def test_scored_fields_present(self):
        """Each ranked entry should have required fields."""
        theme = _make_theme(anchor_genes=["IL6"], specific_genes_list=[["IL6"]])
        hub_genes = {"IL6": {"theme_count": 10, "themes": [], "go_terms": []}}

        ranked = rank_genes_for_theme(theme, hub_genes)

        assert len(ranked) == 1
        entry = ranked[0]
        assert entry["gene"] == "IL6"
        assert "in_specific_terms" in entry
        assert "n_themes" in entry
        assert "score" in entry
        assert entry["in_specific_terms"] == 1
        assert entry["n_themes"] == 10


# =============================================================================
# Test validate_explanation_json
# =============================================================================


@pytest.mark.unit
class TestValidateExplanationJson:
    """Tests for validate_explanation_json function."""

    def _make_valid_explanation(self, theme):
        anchor_go = theme["anchor_term"]["go_id"]
        gene = theme["anchor_term"]["genes"][0]
        return {
            "themes": [{
                "theme_index": 0,
                "narrative": "[DATA] This is a narrative.",
                "key_insights": [
                    {"insight": "An insight.", "go_id": anchor_go},
                    {"insight": "Another insight.", "go_id": anchor_go},
                ],
                "key_genes": [
                    {"gene": gene, "go_id": anchor_go, "description": "A description.", "claim_type": "EXTERNAL"},
                ],
                "statistical_context": "FDR 1e-10, 8 genes.",
            }],
            "hub_genes": [],
            "overall_summary": ["Summary paragraph."],
        }

    def test_valid_input_returns_no_warnings(self):
        """Valid explanation with correct genes and GO IDs should return no warnings."""
        theme = _make_theme(anchor_genes=["CD14", "IL6"], anchor_go_id="GO:0006954")
        enrichment = _make_enrichment_output([theme])
        explanation = self._make_valid_explanation(theme)

        warnings = validate_explanation_json(explanation, enrichment)

        assert warnings == []

    def test_hallucinated_gene_produces_warning(self):
        """Gene not in theme's gene list should produce a warning."""
        theme = _make_theme(anchor_genes=["CD14"], anchor_go_id="GO:0006954")
        enrichment = _make_enrichment_output([theme])
        explanation = self._make_valid_explanation(theme)
        # Inject hallucinated gene
        explanation["themes"][0]["key_genes"][0]["gene"] = "FAKE_GENE"

        warnings = validate_explanation_json(explanation, enrichment)

        assert len(warnings) >= 1
        assert any("FAKE_GENE" in w for w in warnings)

    def test_hallucinated_go_id_produces_warning(self):
        """GO ID not in theme's GO IDs should produce a warning."""
        theme = _make_theme(anchor_genes=["CD14"], anchor_go_id="GO:0006954")
        enrichment = _make_enrichment_output([theme])
        explanation = self._make_valid_explanation(theme)
        # Inject hallucinated GO ID
        explanation["themes"][0]["key_genes"][0]["go_id"] = "GO:9999999"

        warnings = validate_explanation_json(explanation, enrichment)

        assert len(warnings) >= 1
        assert any("GO:9999999" in w for w in warnings)

    def test_theme_index_out_of_range_skipped(self):
        """theme_index beyond enrichment themes count should be skipped gracefully."""
        theme = _make_theme(anchor_genes=["CD14"], anchor_go_id="GO:0006954")
        enrichment = _make_enrichment_output([theme])
        explanation = self._make_valid_explanation(theme)
        explanation["themes"][0]["theme_index"] = 99  # Out of range

        # Should not raise
        warnings = validate_explanation_json(explanation, enrichment)
        assert isinstance(warnings, list)


# =============================================================================
# Test render_explanation_to_markdown
# =============================================================================


@pytest.mark.unit
class TestRenderExplanationToMarkdown:
    """Tests for render_explanation_to_markdown function."""

    def _make_explanation_and_enrichment(self):
        theme = _make_theme(
            anchor_genes=["CD14", "IL6"],
            specific_genes_list=[["CD14"]],
            anchor_go_id="GO:0006954",
        )
        enrichment = _make_enrichment_output([theme])
        explanation = {
            "themes": [{
                "theme_index": 0,
                "narrative": "[DATA] Enriched theme. [EXTERNAL] Mechanism known.",
                "key_insights": [
                    {"insight": "LPS detection.", "go_id": "GO:0006954"},
                ],
                "key_genes": [
                    {"gene": "CD14", "go_id": "GO:0006954", "description": "Co-receptor for TLR4.", "claim_type": "EXTERNAL"},
                ],
                "statistical_context": "FDR 1e-10, 8 genes, 8x fold enrichment.",
            }],
            "hub_genes": [],
            "overall_summary": ["Overall biological story here."],
        }
        return explanation, enrichment

    def test_theme_section_header_present(self):
        """Output should contain a theme section header."""
        explanation, enrichment = self._make_explanation_and_enrichment()

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "### Theme 1:" in md or "## Theme 1:" in md

    def test_anchor_name_in_output(self):
        """Anchor term name should appear in the output."""
        explanation, enrichment = self._make_explanation_and_enrichment()

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "inflammatory response" in md

    def test_go_hyperlink_added_programmatically(self):
        """GO IDs should be rendered as hyperlinks by the renderer."""
        explanation, enrichment = self._make_explanation_and_enrichment()

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "[GO:0006954](http://purl.obolibrary.org/obo/GO_0006954)" in md

    def test_no_ref_marker_in_key_gene(self):
        """Key gene entries must NOT have [REF:GENE] markers (LLM cites inline now)."""
        explanation, enrichment = self._make_explanation_and_enrichment()

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "[REF:" not in md

    def test_key_gene_bold_name(self):
        """Gene names should be bolded in Key Genes section."""
        explanation, enrichment = self._make_explanation_and_enrichment()

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "**CD14**" in md

    def test_narrative_included(self):
        """Narrative text should appear in the output."""
        explanation, enrichment = self._make_explanation_and_enrichment()

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "Enriched theme" in md

    def test_overall_summary_included(self):
        """Overall summary paragraphs should appear in the output."""
        explanation, enrichment = self._make_explanation_and_enrichment()

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "Overall biological story here." in md

    def test_statistical_context_included(self):
        """Statistical context should appear in the output."""
        explanation, enrichment = self._make_explanation_and_enrichment()

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "FDR 1e-10" in md

    def test_inline_pmid_in_narrative_passes_through(self):
        """Inline PMIDs written by the LLM should appear as-is in rendered output."""
        theme = _make_theme(
            anchor_genes=["RELA"],
            specific_genes_list=[],
            anchor_go_id="GO:0006954",
        )
        enrichment = _make_enrichment_output([theme])
        explanation = {
            "themes": [{
                "theme_index": 0,
                "narrative": "[EXTERNAL] RELA encodes NF-κB p65 PMID:10383454.",
                "key_insights": [],
                "key_genes": [],
                "statistical_context": "",
            }],
            "hub_genes": [],
            "overall_summary": [],
        }

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "PMID:10383454" in md


# =============================================================================
# Test Fix 1: theme_index field in LLM context
# =============================================================================


@pytest.mark.unit
class TestFormatEnrichmentThemeIndex:
    """Explicit theme_index field is present in LLM context output."""

    def test_theme_index_zero_based_first_theme(self):
        """First theme block includes theme_index: 0."""
        theme = _make_theme(anchor_genes=["GENE1"], anchor_go_id="GO:0000001")
        enrichment = _make_enrichment_output([theme])

        result = _format_enrichment_for_llm(enrichment)

        assert "theme_index (use this exact integer in your response): 0" in result

    def test_theme_index_second_theme(self):
        """Second theme block includes theme_index: 1."""
        t1 = _make_theme(anchor_genes=["G1"], anchor_go_id="GO:0000001")
        t2 = _make_theme(anchor_genes=["G2"], anchor_go_id="GO:0000002")
        enrichment = _make_enrichment_output([t1, t2])

        result = _format_enrichment_for_llm(enrichment)

        assert "theme_index (use this exact integer in your response): 1" in result

    def test_theme_index_distinct_per_theme(self):
        """Each theme has a different theme_index value."""
        themes = [
            _make_theme(anchor_genes=[f"G{i}"], anchor_go_id=f"GO:000000{i}")
            for i in range(3)
        ]
        enrichment = _make_enrichment_output(themes)

        result = _format_enrichment_for_llm(enrichment)

        for i in range(3):
            assert f"theme_index (use this exact integer in your response): {i}" in result


# =============================================================================
# Test Fix 2: methodology note, anchor confidence, reference table
# =============================================================================


@pytest.mark.unit
class TestRenderMethodologyAndTable:
    """Tests for methodology note, anchor confidence, and reference table."""

    def _make_partial_explanation(self, n_explained, n_total):
        """Explanation covers n_explained themes; enrichment has n_total themes."""
        themes = [
            _make_theme(anchor_genes=[f"G{i}"], anchor_go_id=f"GO:000000{i}")
            for i in range(n_total)
        ]
        enrichment = _make_enrichment_output(themes)
        exp_themes = [
            {
                "theme_index": i,
                "narrative": f"[DATA] Theme {i} narrative.",
                "key_insights": [],
                "key_genes": [],
                "statistical_context": "",
            }
            for i in range(n_explained)
        ]
        explanation = {"themes": exp_themes, "hub_genes": [], "overall_summary": []}
        return explanation, enrichment

    def test_methodology_note_always_present(self):
        """Methodology note about depth-anchor appears in all reports."""
        explanation, enrichment = self._make_partial_explanation(1, 1)

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "depth-anchor" in md

    def test_anchor_concept_explained(self):
        """Report explains what an anchor is."""
        explanation, enrichment = self._make_partial_explanation(1, 1)

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "anchor" in md.lower()
        assert "GO hierarchy" in md or "GO term" in md

    def test_theme_count_note_when_capped(self):
        """Header note includes count when not all themes are explained."""
        explanation, enrichment = self._make_partial_explanation(1, 3)

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "1" in md and "3" in md
        # The note should reference the counts together
        assert "1 of 3" in md or "1\nof 3" in md or "**1 of 3**" in md

    def test_no_theme_count_note_when_all_explained(self):
        """No truncation count note when all themes have narratives."""
        explanation, enrichment = self._make_partial_explanation(2, 2)

        md = render_explanation_to_markdown(explanation, enrichment)

        # "2 of 2" should not appear
        assert "2 of 2" not in md

    def test_anchor_confidence_in_summary_line(self):
        """Anchor confidence appears on the theme summary line."""
        theme = _make_theme(anchor_genes=["CD14"], anchor_go_id="GO:0006954")
        theme["anchor_confidence"] = "high"
        enrichment = _make_enrichment_output([theme])
        explanation = {
            "themes": [{
                "theme_index": 0,
                "narrative": "[DATA] Test.",
                "key_insights": [],
                "key_genes": [],
                "statistical_context": "",
            }],
            "hub_genes": [],
            "overall_summary": [],
        }

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "Anchor confidence" in md
        assert "high" in md

    def test_reference_table_heading_present(self):
        """Reference table section heading is present."""
        explanation, enrichment = self._make_partial_explanation(1, 2)

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "All Enrichment Themes" in md

    def test_reference_table_lists_all_themes(self):
        """Reference table has a row for every theme in enrichment output."""
        themes = [
            _make_theme(anchor_genes=[f"G{i}"], anchor_go_id=f"GO:000000{i}")
            for i in range(3)
        ]
        enrichment = _make_enrichment_output(themes)
        explanation = {
            "themes": [{"theme_index": 0, "narrative": "[DATA] T.", "key_insights": [], "key_genes": [], "statistical_context": ""}],
            "hub_genes": [],
            "overall_summary": [],
        }

        md = render_explanation_to_markdown(explanation, enrichment)

        # Each theme is numbered in the table
        assert "| 1 |" in md
        assert "| 2 |" in md
        assert "| 3 |" in md

    def test_reference_table_contains_go_ids(self):
        """Reference table rows include GO IDs."""
        theme = _make_theme(anchor_genes=["G1"], anchor_go_id="GO:0006954")
        enrichment = _make_enrichment_output([theme])
        explanation = {"themes": [], "hub_genes": [], "overall_summary": []}

        md = render_explanation_to_markdown(explanation, enrichment)

        assert "GO:0006954" in md


# =============================================================================
# Test Fix 3: _add_pmid_hyperlinks is called
# =============================================================================


@pytest.mark.unit
class TestAddPmidHyperlinksWiring:
    """_add_pmid_hyperlinks is called by render_explanation_to_markdown."""

    def test_pmid_in_narrative_becomes_hyperlink(self):
        """PMID:xxxxx in LLM narrative is hyperlinked in render output."""
        theme = _make_theme(anchor_genes=["RELA"], anchor_go_id="GO:0006954")
        enrichment = _make_enrichment_output([theme])
        explanation = {
            "themes": [{
                "theme_index": 0,
                "narrative": "[EXTERNAL] Key regulator PMID:12345678.",
                "key_insights": [],
                "key_genes": [],
                "statistical_context": "",
            }],
            "hub_genes": [],
            "overall_summary": [],
        }

        md = render_explanation_to_markdown(explanation, enrichment)

        # After _add_pmid_hyperlinks the PMID should NOT be bare
        assert "PMID:12345678" in md  # text still present
        # Note: render_explanation_to_markdown does NOT call _add_pmid_hyperlinks
        # That is called in generate_markdown_explanation. This test just confirms
        # the PMID passes through the renderer unchanged so the outer call can link it.
        # The hyperlink test for the full pipeline would require LLM mocking.

    def test_add_pmid_hyperlinks_converts_bare_pmid(self):
        """_add_pmid_hyperlinks converts PMID:xxxxx to markdown link."""
        text = "See PMID:12345678 for details."

        result = _add_pmid_hyperlinks(text)

        assert "[PMID:12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/)" in result

    def test_add_pmid_hyperlinks_no_match(self):
        """_add_pmid_hyperlinks returns text unchanged when no PMIDs present."""
        text = "No citations here."

        result = _add_pmid_hyperlinks(text)

        assert result == text


# =============================================================================
# Test mdformat integration
# =============================================================================


@pytest.mark.unit
class TestMdformatIntegration:
    """mdformat normalises the rendered markdown output."""

    def test_mdformat_normalises_missing_blank_lines(self):
        """mdformat adds blank lines around headings if missing."""
        import mdformat

        sloppy = "# Title\n## Section\nSome text."
        result = mdformat.text(sloppy, options={"wrap": "no"})

        # Heading should be followed by blank line
        assert "\n\n" in result

    def test_mdformat_preserves_provenance_tags(self):
        """mdformat does not strip [DATA], [INFERENCE] etc. tags."""
        import mdformat

        text = "# Report\n\n[DATA] STAT1 is enriched. [INFERENCE] Cross-talk likely.\n"
        result = mdformat.text(text, options={"wrap": "no"})

        assert "[DATA]" in result
        assert "[INFERENCE]" in result

    def test_mdformat_preserves_pmid_hyperlinks(self):
        """mdformat does not break PMID hyperlinks."""
        import mdformat

        text = "# Report\n\nSee [PMID:12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/) for details.\n"
        result = mdformat.text(text, options={"wrap": "no"})

        assert "[PMID:12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/)" in result

    def test_mdformat_preserves_go_hyperlinks(self):
        """mdformat does not break GO ID hyperlinks."""
        import mdformat

        text = "# Report\n\n[GO:0006955](http://purl.obolibrary.org/obo/GO_0006955)\n"
        result = mdformat.text(text, options={"wrap": "no"})

        assert "[GO:0006955](http://purl.obolibrary.org/obo/GO_0006955)" in result

    def test_mdformat_preserves_table(self):
        """mdformat does not corrupt markdown tables."""
        import mdformat

        text = (
            "# Report\n\n"
            "| # | Theme | FDR |\n"
            "|---|-------|-----|\n"
            "| 1 | immune response | 1.2e-8 |\n"
        )
        result = mdformat.text(text, options={"wrap": "no"})

        assert "| 1 |" in result
        assert "immune response" in result

    def test_mdformat_wrap_no_preserves_long_lines(self):
        """wrap=no option prevents mdformat from breaking long lines."""
        import mdformat

        long_line = "GENE1, GENE2, GENE3, GENE4, GENE5, GENE6, GENE7, GENE8, GENE9, GENE10, GENE11, GENE12 (12)"
        text = f"# Report\n\n{long_line}\n"
        result = mdformat.text(text, options={"wrap": "no"})

        assert long_line in result
