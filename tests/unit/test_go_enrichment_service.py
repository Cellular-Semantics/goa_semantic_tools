"""
Unit Tests for GO Enrichment Service

Tests the service layer functions with mocked dependencies.
"""

import pytest

from goa_semantic_tools.services.go_enrichment_service import (
    _build_output,
    _empty_result,
    _namespace_abbrev_to_full,
    run_go_enrichment,
)


@pytest.mark.unit
class TestNamespaceConversion:
    """Tests for _namespace_abbrev_to_full function."""

    def test_biological_process(self):
        """BP should convert to biological_process."""
        assert _namespace_abbrev_to_full("BP") == "biological_process"

    def test_cellular_component(self):
        """CC should convert to cellular_component."""
        assert _namespace_abbrev_to_full("CC") == "cellular_component"

    def test_molecular_function(self):
        """MF should convert to molecular_function."""
        assert _namespace_abbrev_to_full("MF") == "molecular_function"

    def test_unknown_raises(self):
        """Unknown abbreviation should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown namespace abbreviation"):
            _namespace_abbrev_to_full("XX")


@pytest.mark.unit
class TestEmptyResult:
    """Tests for _empty_result function."""

    def test_returns_correct_structure(self):
        """Should return dict with all required keys."""
        result = _empty_result(
            gene_symbols=["TP53", "BRCA1"],
            species="human",
            fdr_threshold=0.05,
            min_ic=3.0,
            min_leaves=2,
        )

        assert "enrichment_leaves" in result
        assert "themes" in result
        assert "hub_genes" in result
        assert "metadata" in result

    def test_lists_are_empty(self):
        """All list fields should be empty."""
        result = _empty_result(
            gene_symbols=["TP53"],
            species="human",
            fdr_threshold=0.05,
            min_ic=3.0,
            min_leaves=2,
        )

        assert result["enrichment_leaves"] == []
        assert result["themes"] == []
        assert result["hub_genes"] == {}

    def test_metadata_gene_count(self):
        """Metadata should reflect input gene count."""
        result = _empty_result(
            gene_symbols=["TP53", "BRCA1", "BRCA2"],
            species="human",
            fdr_threshold=0.05,
            min_ic=3.0,
            min_leaves=2,
        )

        assert result["metadata"]["input_genes_count"] == 3
        assert result["metadata"]["genes_with_annotations"] == 0

    def test_metadata_parameters(self):
        """Metadata should include analysis parameters."""
        result = _empty_result(
            gene_symbols=["TP53"],
            species="mouse",
            fdr_threshold=0.01,
            min_ic=4.0,
            min_leaves=3,
        )

        assert result["metadata"]["species"] == "mouse"
        assert result["metadata"]["fdr_threshold"] == 0.01
        assert result["metadata"]["min_ic"] == 4.0
        assert result["metadata"]["min_leaves"] == 3

    def test_metadata_has_timestamp(self):
        """Metadata should include timestamp."""
        result = _empty_result(
            gene_symbols=["TP53"],
            species="human",
            fdr_threshold=0.05,
            min_ic=3.0,
            min_leaves=2,
        )

        assert "timestamp" in result["metadata"]
        assert len(result["metadata"]["timestamp"]) > 10  # ISO format


@pytest.mark.unit
class TestBuildOutput:
    """Tests for _build_output function."""

    def test_returns_correct_structure(self):
        """Should return dict with all required keys."""
        result = _build_output(
            enrichment_leaves=[],
            themes=[],
            hub_genes={},
            input_genes=["TP53"],
            study_set={"TP53"},
            total_enriched=5,
            fdr_threshold=0.05,
            species="human",
            min_ic=3.0,
            min_leaves=2,
        )

        assert "enrichment_leaves" in result
        assert "themes" in result
        assert "hub_genes" in result
        assert "metadata" in result

    def test_passes_through_data(self):
        """Should pass through enrichment_leaves, themes, hub_genes."""
        leaves = [{"go_id": "GO:0006281", "name": "DNA repair"}]
        themes = [{"anchor_term": {"go_id": "GO:0006915"}}]
        hub = {"TP53": {"theme_count": 3}}

        result = _build_output(
            enrichment_leaves=leaves,
            themes=themes,
            hub_genes=hub,
            input_genes=["TP53"],
            study_set={"TP53"},
            total_enriched=5,
            fdr_threshold=0.05,
            species="human",
            min_ic=3.0,
            min_leaves=2,
        )

        assert result["enrichment_leaves"] == leaves
        assert result["themes"] == themes
        assert result["hub_genes"] == hub

    def test_metadata_counts(self):
        """Metadata should have correct counts."""
        leaves = [{"go_id": "GO:0001"}, {"go_id": "GO:0002"}]
        themes = [
            {"n_specific_terms": 3},
            {"n_specific_terms": 0},
            {"n_specific_terms": 2},
        ]
        hub = {"TP53": {}, "BRCA1": {}}

        result = _build_output(
            enrichment_leaves=leaves,
            themes=themes,
            hub_genes=hub,
            input_genes=["TP53", "BRCA1", "BRCA2"],
            study_set={"TP53", "BRCA1"},
            total_enriched=10,
            fdr_threshold=0.05,
            species="human",
            min_ic=3.0,
            min_leaves=2,
        )

        assert result["metadata"]["input_genes_count"] == 3
        assert result["metadata"]["genes_with_annotations"] == 2
        assert result["metadata"]["enrichment_leaves_count"] == 2
        assert result["metadata"]["themes_count"] == 3
        assert result["metadata"]["themes_with_children"] == 2  # 2 themes have n_specific_terms > 0
        assert result["metadata"]["hub_genes_count"] == 2
        assert result["metadata"]["total_enriched_terms"] == 10


@pytest.mark.unit
class TestRunGoEnrichmentValidation:
    """Tests for run_go_enrichment input validation (without full execution)."""

    def test_empty_genes_raises(self):
        """Empty gene list should raise before any processing."""
        with pytest.raises(ValueError, match="gene_symbols cannot be empty"):
            run_go_enrichment(gene_symbols=[])

    def test_invalid_species_raises(self):
        """Invalid species should raise before any processing."""
        with pytest.raises(ValueError, match="Unsupported species"):
            run_go_enrichment(gene_symbols=["TP53"], species="fish")

    def test_human_species_accepted(self):
        """Human should be a valid species (validation passes, may fail later)."""
        # This will fail at data loading, but validation should pass
        # We're just testing that 'human' doesn't raise at validation
        try:
            run_go_enrichment(gene_symbols=["TP53"], species="human")
        except ValueError as e:
            # Should not be a species validation error
            assert "species" not in str(e).lower()
        except Exception:
            # Other errors are fine - we're just testing validation
            pass

    def test_mouse_species_accepted(self):
        """Mouse should be a valid species."""
        try:
            run_go_enrichment(gene_symbols=["Tp53"], species="mouse")
        except ValueError as e:
            assert "species" not in str(e).lower()
        except Exception:
            pass

    def test_fdr_zero_raises(self):
        """FDR of 0 should raise ValueError (must be > 0)."""
        with pytest.raises(ValueError, match="fdr_threshold must be between 0 and 1"):
            run_go_enrichment(gene_symbols=["TP53"], fdr_threshold=0.0)

    def test_fdr_negative_raises(self):
        """Negative FDR should raise ValueError."""
        with pytest.raises(ValueError, match="fdr_threshold must be between 0 and 1"):
            run_go_enrichment(gene_symbols=["TP53"], fdr_threshold=-0.1)

    def test_fdr_above_one_raises(self):
        """FDR above 1 should raise ValueError."""
        with pytest.raises(ValueError, match="fdr_threshold must be between 0 and 1"):
            run_go_enrichment(gene_symbols=["TP53"], fdr_threshold=1.5)

    def test_fdr_one_accepted(self):
        """FDR of 1 should be accepted."""
        try:
            run_go_enrichment(gene_symbols=["TP53"], fdr_threshold=1.0)
        except ValueError as e:
            assert "fdr" not in str(e).lower()
        except Exception:
            pass

    def test_single_gene_accepted(self):
        """Single gene should pass validation."""
        try:
            run_go_enrichment(gene_symbols=["TP53"])
        except ValueError as e:
            # Should not be a gene count validation error
            assert "empty" not in str(e).lower()
        except Exception:
            pass


@pytest.mark.unit
class TestNamespaceFiltering:
    """Tests for the namespaces parameter of run_go_enrichment."""

    def test_invalid_namespace_raises(self):
        """Invalid namespace code raises ValueError."""
        with pytest.raises(ValueError, match="Invalid namespace"):
            run_go_enrichment(gene_symbols=["TP53"], namespaces=["XX"])

    def test_invalid_namespace_message_contains_valid_codes(self):
        """Error message lists valid namespace codes."""
        try:
            run_go_enrichment(gene_symbols=["TP53"], namespaces=["INVALID"])
        except ValueError as e:
            msg = str(e)
            assert "BP" in msg or "MF" in msg or "CC" in msg

    def test_none_namespaces_passes_validation(self):
        """None (default) namespaces does not raise ValueError for namespace."""
        try:
            run_go_enrichment(gene_symbols=["TP53"], namespaces=None)
        except ValueError as e:
            assert "namespace" not in str(e).lower()
        except Exception:
            pass

    def test_bp_only_namespace_passes_validation(self):
        """['BP'] passes namespace validation."""
        try:
            run_go_enrichment(gene_symbols=["TP53"], namespaces=["BP"])
        except ValueError as e:
            assert "namespace" not in str(e).lower()
        except Exception:
            pass

    def test_namespace_map_contains_all_three(self):
        """NAMESPACE_MAP has BP, MF, CC keys."""
        from goa_semantic_tools.services.go_enrichment_service import NAMESPACE_MAP

        assert "BP" in NAMESPACE_MAP
        assert "MF" in NAMESPACE_MAP
        assert "CC" in NAMESPACE_MAP

    def test_namespace_map_values_are_full_names(self):
        """NAMESPACE_MAP values are full namespace names."""
        from goa_semantic_tools.services.go_enrichment_service import NAMESPACE_MAP

        assert NAMESPACE_MAP["BP"] == "biological_process"
        assert NAMESPACE_MAP["MF"] == "molecular_function"
        assert NAMESPACE_MAP["CC"] == "cellular_component"

    def test_case_insensitive_namespace(self):
        """Namespace codes are case-insensitive (bp accepted like BP)."""
        try:
            run_go_enrichment(gene_symbols=["TP53"], namespaces=["bp"])
        except ValueError as e:
            assert "namespace" not in str(e).lower()
        except Exception:
            pass


@pytest.mark.unit
class TestFoldEnrichmentFormula:
    """Tests for fold enrichment calculation in _convert_to_enriched_terms."""

    def _make_mock_goea_result(self, ratio_in_study, ratio_in_pop, go_id="GO:0006954", name="inflammatory response"):
        """Create a minimal mock GOATOOLS OEA result object."""
        from unittest.mock import MagicMock
        result = MagicMock()
        result.GO = go_id
        result.name = name
        result.NS = "BP"
        result.p_fdr_bh = 1e-5
        result.ratio_in_study = ratio_in_study
        result.ratio_in_pop = ratio_in_pop
        result.study_items = frozenset(["GENE1", "GENE2"])
        return result

    def _make_mock_godag(self, go_id="GO:0006954"):
        from unittest.mock import MagicMock
        term = MagicMock()
        term.depth = 5
        godag = {go_id: term}
        return godag

    def test_fold_enrichment_uses_rates_not_raw_counts(self):
        """Fold enrichment should be (study_n/study_total)/(pop_n/pop_total)."""
        from goa_semantic_tools.services.go_enrichment_service import _convert_to_enriched_terms

        # 10 study hits out of 100 study genes
        # 100 pop hits out of 10000 pop genes
        # Correct: (10/100) / (100/10000) = 0.1 / 0.01 = 10.0x
        # Wrong (old): 10 / 100 = 0.1x
        result = self._make_mock_goea_result(
            ratio_in_study=(10, 100),
            ratio_in_pop=(100, 10000),
        )
        godag = self._make_mock_godag()

        terms = _convert_to_enriched_terms([result], godag)

        assert "GO:0006954" in terms
        fold = terms["GO:0006954"].fold_enrichment
        assert abs(fold - 10.0) < 0.01, f"Expected ~10.0x, got {fold}"

    def test_fold_enrichment_depleted_term_below_one(self):
        """A depleted term should have fold enrichment < 1."""
        from goa_semantic_tools.services.go_enrichment_service import _convert_to_enriched_terms

        # 5 study hits out of 100, 1000 pop hits out of 10000
        # (5/100) / (1000/10000) = 0.05 / 0.1 = 0.5x
        result = self._make_mock_goea_result(
            ratio_in_study=(5, 100),
            ratio_in_pop=(1000, 10000),
        )
        godag = self._make_mock_godag()

        terms = _convert_to_enriched_terms([result], godag)

        fold = terms["GO:0006954"].fold_enrichment
        assert fold < 1.0, f"Expected depleted (fold < 1), got {fold}"
        assert abs(fold - 0.5) < 0.01, f"Expected ~0.5x, got {fold}"

    def test_fold_enrichment_zero_pop_count_returns_zero(self):
        """Zero pop_total should return 0 (avoid division by zero)."""
        from goa_semantic_tools.services.go_enrichment_service import _convert_to_enriched_terms

        result = self._make_mock_goea_result(
            ratio_in_study=(5, 100),
            ratio_in_pop=(0, 0),
        )
        godag = self._make_mock_godag()

        terms = _convert_to_enriched_terms([result], godag)

        assert terms["GO:0006954"].fold_enrichment == 0.0
