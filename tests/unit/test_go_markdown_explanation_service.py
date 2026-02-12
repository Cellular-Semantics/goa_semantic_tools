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
    _add_go_term_hyperlinks,
    _add_pmid_hyperlinks,
    _count_provenance_tags,
    _empty_markdown_explanation,
    _format_enrichment_for_llm,
    _get_api_key_for_model,
    _load_prompt,
    _validate_citations,
    generate_markdown_explanation,
)


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
