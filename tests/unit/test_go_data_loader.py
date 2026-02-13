"""
Unit Tests for GO Data Loader

Tests helper functions and validation without loading real data.
"""

import pytest
from pathlib import Path

from goa_semantic_tools.utils.go_data_loader import (
    load_go_data,
    load_gene_annotations,
    build_gene_to_go_mapping,
    _collapse_annotations_by_go_term,
)


@pytest.mark.unit
class TestLoadGoDataValidation:
    """Tests for load_go_data validation."""

    def test_missing_file_raises(self):
        """Should raise FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError, match="GO OBO file not found"):
            load_go_data(Path("/nonexistent/go.obo"))


@pytest.mark.unit
class TestLoadGeneAnnotationsValidation:
    """Tests for load_gene_annotations validation."""

    def test_missing_file_raises(self):
        """Should raise FileNotFoundError for missing file."""
        # Create a mock godag (won't be used due to validation)
        with pytest.raises(FileNotFoundError, match="GAF file not found"):
            load_gene_annotations(Path("/nonexistent/goa.gaf"), godag=None)


@pytest.mark.unit
class TestBuildGeneToGoMappingValidation:
    """Tests for build_gene_to_go_mapping validation."""

    def test_missing_file_raises(self):
        """Should raise FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError, match="GAF file not found"):
            build_gene_to_go_mapping(Path("/nonexistent/goa.gaf"), godag=None)


@pytest.mark.unit
class TestCollapseAnnotationsByGoTerm:
    """Tests for _collapse_annotations_by_go_term function."""

    def test_empty_input(self):
        """Should handle empty input."""
        result = _collapse_annotations_by_go_term({})
        assert result == {}

    def test_single_annotation(self):
        """Should handle single annotation per gene."""
        input_data = {
            "TP53": [
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": ["PMID:12345"],
                }
            ]
        }

        result = _collapse_annotations_by_go_term(input_data)

        assert "TP53" in result
        assert len(result["TP53"]) == 1
        assert result["TP53"][0]["go_id"] == "GO:0006281"
        assert len(result["TP53"][0]["evidence"]) == 1
        assert result["TP53"][0]["evidence"][0]["code"] == "IDA"

    def test_collapses_duplicate_go_terms(self):
        """Should collapse multiple evidence codes for same GO term."""
        input_data = {
            "TP53": [
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": ["PMID:12345"],
                },
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IMP",
                    "references": ["PMID:67890"],
                },
            ]
        }

        result = _collapse_annotations_by_go_term(input_data)

        assert "TP53" in result
        assert len(result["TP53"]) == 1  # Collapsed to single GO term
        assert result["TP53"][0]["go_id"] == "GO:0006281"
        assert len(result["TP53"][0]["evidence"]) == 2  # Two evidence codes

    def test_merges_references_for_same_evidence(self):
        """Should merge references for same evidence code."""
        input_data = {
            "TP53": [
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": ["PMID:12345"],
                },
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": ["PMID:67890"],
                },
            ]
        }

        result = _collapse_annotations_by_go_term(input_data)

        assert len(result["TP53"]) == 1
        assert len(result["TP53"][0]["evidence"]) == 1  # Single evidence code
        assert len(result["TP53"][0]["evidence"][0]["references"]) == 2  # Two references

    def test_keeps_different_go_terms_separate(self):
        """Should keep different GO terms separate."""
        input_data = {
            "TP53": [
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": ["PMID:12345"],
                },
                {
                    "go_id": "GO:0006915",
                    "go_name": "apoptotic process",
                    "namespace": "biological_process",
                    "evidence_code": "IMP",
                    "references": ["PMID:67890"],
                },
            ]
        }

        result = _collapse_annotations_by_go_term(input_data)

        assert len(result["TP53"]) == 2  # Two different GO terms

    def test_multiple_genes(self):
        """Should handle multiple genes."""
        input_data = {
            "TP53": [
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": [],
                }
            ],
            "BRCA1": [
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": [],
                }
            ],
        }

        result = _collapse_annotations_by_go_term(input_data)

        assert "TP53" in result
        assert "BRCA1" in result

    def test_sorts_evidence_codes(self):
        """Should sort evidence codes alphabetically."""
        input_data = {
            "TP53": [
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IMP",
                    "references": [],
                },
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": [],
                },
            ]
        }

        result = _collapse_annotations_by_go_term(input_data)

        evidence_codes = [e["code"] for e in result["TP53"][0]["evidence"]]
        assert evidence_codes == ["IDA", "IMP"]  # Alphabetically sorted

    def test_sorts_references(self):
        """Should sort references within each evidence code."""
        input_data = {
            "TP53": [
                {
                    "go_id": "GO:0006281",
                    "go_name": "DNA repair",
                    "namespace": "biological_process",
                    "evidence_code": "IDA",
                    "references": ["PMID:99999", "PMID:11111"],
                }
            ]
        }

        result = _collapse_annotations_by_go_term(input_data)

        refs = result["TP53"][0]["evidence"][0]["references"]
        assert refs == ["PMID:11111", "PMID:99999"]  # Sorted
