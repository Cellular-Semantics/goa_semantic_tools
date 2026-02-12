"""
Unit tests for Reference Index utility functions.

Tests PMID extraction and reference lookup from GAF data.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from goa_semantic_tools.utils.reference_index import (
    PMID_PATTERN,
    find_pmids_covering_genes,
    get_descendants_closure,
    get_genes_for_pmid,
    get_pmids_for_gene_term,
    load_gaf_with_pmids,
)


# =============================================================================
# Mock Helpers
# =============================================================================


class MockGOTerm:
    """Mock GO term for testing."""

    def __init__(self, go_id: str, name: str, children: list | None = None):
        self.id = go_id
        self.name = name
        self.children = children or []


def create_mock_godag() -> dict:
    """Create a mock GO DAG for testing."""
    root = MockGOTerm("GO:0008150", "biological_process")
    apoptosis = MockGOTerm("GO:0006915", "apoptotic process")
    intrinsic = MockGOTerm("GO:0097193", "intrinsic apoptotic signaling pathway")
    extrinsic = MockGOTerm("GO:0097194", "extrinsic apoptotic signaling pathway")

    root.children = [apoptosis]
    apoptosis.children = [intrinsic, extrinsic]

    return {
        "GO:0008150": root,
        "GO:0006915": apoptosis,
        "GO:0097193": intrinsic,
        "GO:0097194": extrinsic,
    }


class MockAssociation:
    """Mock GAF association for testing."""

    def __init__(self, gene: str, go_id: str, refs: list[str]):
        self.DB_Symbol = gene
        self.GO_ID = go_id
        self.DB_Reference = refs


# =============================================================================
# Test PMID Pattern
# =============================================================================


@pytest.mark.unit
class TestPMIDPattern:
    """Tests for PMID regex pattern."""

    def test_valid_pmid(self):
        """Test matching valid PMID format."""
        match = PMID_PATTERN.match("PMID:12345678")
        assert match is not None
        assert match.group(1) == "12345678"

    def test_pmid_short(self):
        """Test matching short PMID."""
        match = PMID_PATTERN.match("PMID:123")
        assert match is not None
        assert match.group(1) == "123"

    def test_pmid_long(self):
        """Test matching long PMID."""
        match = PMID_PATTERN.match("PMID:123456789012")
        assert match is not None
        assert match.group(1) == "123456789012"

    def test_non_pmid(self):
        """Test non-PMID references don't match."""
        assert PMID_PATTERN.match("GO_REF:0000001") is None
        assert PMID_PATTERN.match("DOI:10.1234/foo") is None
        assert PMID_PATTERN.match("REACTOME:R-HSA-123") is None

    def test_pmid_at_start_only(self):
        """Test that pattern matches at start of string."""
        # match() only matches at start
        assert PMID_PATTERN.match("foo PMID:12345") is None
        assert PMID_PATTERN.match("PMID:12345 bar") is not None


# =============================================================================
# Test load_gaf_with_pmids Function
# =============================================================================


@pytest.mark.unit
class TestLoadGafWithPmids:
    """Tests for load_gaf_with_pmids function."""

    def test_basic_loading(self):
        """Test basic GAF loading with mocked reader."""
        godag = create_mock_godag()

        # Create mock associations
        associations = [
            MockAssociation("TP53", "GO:0006915", ["PMID:12345678", "GO_REF:0000001"]),
            MockAssociation("TP53", "GO:0097193", ["PMID:23456789"]),
            MockAssociation("BRCA1", "GO:0006915", ["PMID:12345678"]),  # Same PMID as TP53
        ]

        with patch("goa_semantic_tools.utils.reference_index.GafReader") as MockReader:
            mock_reader_instance = MagicMock()
            mock_reader_instance.associations = associations
            MockReader.return_value = mock_reader_instance

            ref_index = load_gaf_with_pmids("/fake/path.gaf", godag)

        # Check gene_go_pmids structure
        assert "TP53" in ref_index["gene_go_pmids"]
        assert "GO:0006915" in ref_index["gene_go_pmids"]["TP53"]
        assert "12345678" in ref_index["gene_go_pmids"]["TP53"]["GO:0006915"]

        # Check pmid_gene_gos structure
        assert "12345678" in ref_index["pmid_gene_gos"]
        assert "TP53" in ref_index["pmid_gene_gos"]["12345678"]
        assert "BRCA1" in ref_index["pmid_gene_gos"]["12345678"]

        # Check GO term names
        assert ref_index["go_term_names"]["GO:0006915"] == "apoptotic process"

    def test_filter_genes_of_interest(self):
        """Test filtering to genes of interest."""
        godag = create_mock_godag()

        associations = [
            MockAssociation("TP53", "GO:0006915", ["PMID:12345678"]),
            MockAssociation("BRCA1", "GO:0006915", ["PMID:23456789"]),
            MockAssociation("OTHER", "GO:0006915", ["PMID:34567890"]),
        ]

        with patch("goa_semantic_tools.utils.reference_index.GafReader") as MockReader:
            mock_reader_instance = MagicMock()
            mock_reader_instance.associations = associations
            MockReader.return_value = mock_reader_instance

            ref_index = load_gaf_with_pmids(
                "/fake/path.gaf",
                godag,
                genes_of_interest={"TP53", "BRCA1"},
            )

        # Only TP53 and BRCA1 should be present
        assert "TP53" in ref_index["gene_go_pmids"]
        assert "BRCA1" in ref_index["gene_go_pmids"]
        assert "OTHER" not in ref_index["gene_go_pmids"]

    def test_non_pmid_refs_ignored(self):
        """Test that non-PMID references are ignored."""
        godag = create_mock_godag()

        associations = [
            MockAssociation("TP53", "GO:0006915", ["GO_REF:0000001", "REACTOME:R-HSA-123"]),
        ]

        with patch("goa_semantic_tools.utils.reference_index.GafReader") as MockReader:
            mock_reader_instance = MagicMock()
            mock_reader_instance.associations = associations
            MockReader.return_value = mock_reader_instance

            ref_index = load_gaf_with_pmids("/fake/path.gaf", godag)

        # No PMIDs should be found
        assert len(ref_index["pmid_gene_gos"]) == 0


# =============================================================================
# Test get_descendants_closure Function
# =============================================================================


@pytest.mark.unit
class TestGetDescendantsClosure:
    """Tests for get_descendants_closure function."""

    def test_single_term_closure(self):
        """Test computing closure for a single term."""
        godag = create_mock_godag()

        closure = get_descendants_closure({"GO:0006915"}, godag)

        assert "GO:0006915" in closure
        descendants = closure["GO:0006915"]

        # Apoptosis should have intrinsic and extrinsic as descendants
        assert "GO:0097193" in descendants
        assert "GO:0097194" in descendants
        assert len(descendants) == 2

    def test_leaf_term_closure(self):
        """Test computing closure for a leaf term (no descendants)."""
        godag = create_mock_godag()

        closure = get_descendants_closure({"GO:0097193"}, godag)

        # Intrinsic apoptosis is a leaf - no descendants
        assert "GO:0097193" in closure
        assert len(closure["GO:0097193"]) == 0

    def test_missing_term(self):
        """Test handling of missing terms."""
        godag = create_mock_godag()

        closure = get_descendants_closure({"GO:9999999"}, godag)

        assert "GO:9999999" in closure
        assert closure["GO:9999999"] == set()

    def test_multiple_terms(self):
        """Test computing closure for multiple terms."""
        godag = create_mock_godag()

        closure = get_descendants_closure({"GO:0008150", "GO:0006915"}, godag)

        assert len(closure) == 2
        assert "GO:0006915" in closure["GO:0008150"]  # Root includes apoptosis


# =============================================================================
# Test get_pmids_for_gene_term Function
# =============================================================================


@pytest.mark.unit
class TestGetPmidsForGeneTerm:
    """Tests for get_pmids_for_gene_term function."""

    def test_direct_match(self):
        """Test getting PMIDs for direct gene-term match."""
        ref_index = {
            "gene_go_pmids": {
                "TP53": {
                    "GO:0006915": {"12345678", "23456789"},
                    "GO:0097193": {"34567890"},
                },
            },
        }

        pmids = get_pmids_for_gene_term("TP53", "GO:0006915", ref_index)

        assert pmids == {"12345678", "23456789"}

    def test_with_descendants(self):
        """Test getting PMIDs including descendant terms."""
        ref_index = {
            "gene_go_pmids": {
                "TP53": {
                    "GO:0006915": {"12345678"},
                    "GO:0097193": {"23456789"},  # Descendant of GO:0006915
                },
            },
        }

        descendants_closure = {
            "GO:0006915": {"GO:0097193", "GO:0097194"},
        }

        pmids = get_pmids_for_gene_term(
            "TP53",
            "GO:0006915",
            ref_index,
            descendants_closure=descendants_closure,
        )

        # Should include PMIDs from both direct and descendant terms
        assert "12345678" in pmids
        assert "23456789" in pmids

    def test_gene_not_found(self):
        """Test behavior when gene is not in index."""
        ref_index = {"gene_go_pmids": {}}

        pmids = get_pmids_for_gene_term("UNKNOWN", "GO:0006915", ref_index)

        assert pmids == set()

    def test_term_not_found(self):
        """Test behavior when term is not annotated for gene."""
        ref_index = {
            "gene_go_pmids": {
                "TP53": {
                    "GO:0097193": {"12345678"},
                },
            },
        }

        pmids = get_pmids_for_gene_term("TP53", "GO:0006915", ref_index)

        assert pmids == set()


# =============================================================================
# Test get_genes_for_pmid Function
# =============================================================================


@pytest.mark.unit
class TestGetGenesForPmid:
    """Tests for get_genes_for_pmid function."""

    def test_basic_lookup(self):
        """Test basic PMID to gene lookup."""
        ref_index = {
            "pmid_gene_gos": {
                "12345678": {
                    "TP53": {"GO:0006915", "GO:0097193"},
                    "BRCA1": {"GO:0006915"},
                },
            },
        }

        genes = get_genes_for_pmid("12345678", ref_index)

        assert "TP53" in genes
        assert "BRCA1" in genes
        assert "GO:0006915" in genes["TP53"]

    def test_pmid_not_found(self):
        """Test behavior when PMID is not in index."""
        ref_index = {"pmid_gene_gos": {}}

        genes = get_genes_for_pmid("99999999", ref_index)

        assert genes == {}


# =============================================================================
# Test find_pmids_covering_genes Function
# =============================================================================


@pytest.mark.unit
class TestFindPmidsCoveringGenes:
    """Tests for find_pmids_covering_genes function."""

    def test_find_multi_gene_pmids(self):
        """Test finding PMIDs that cover multiple genes."""
        ref_index = {
            "gene_go_pmids": {
                "TP53": {"GO:0006915": {"12345678", "23456789"}},
                "BRCA1": {"GO:0006915": {"12345678"}},  # Same PMID as TP53
                "ATM": {"GO:0006915": {"34567890"}},  # Different PMID
            },
            "pmid_gene_gos": {},  # Not used in this function
        }

        results = find_pmids_covering_genes(
            genes=["TP53", "BRCA1", "ATM"],
            go_ids=["GO:0006915"],
            ref_index=ref_index,
            min_genes=2,
        )

        # Only PMID 12345678 covers 2+ genes
        assert len(results) >= 1
        pmid_12345678 = next((r for r in results if r["pmid"] == "12345678"), None)
        assert pmid_12345678 is not None
        assert set(pmid_12345678["genes_covered"]) == {"TP53", "BRCA1"}

    def test_with_descendants(self):
        """Test finding PMIDs with descendant closure."""
        ref_index = {
            "gene_go_pmids": {
                "TP53": {"GO:0006915": {"12345678"}},
                "BRCA1": {"GO:0097193": {"12345678"}},  # Descendant term
            },
            "pmid_gene_gos": {},
        }

        descendants_closure = {
            "GO:0006915": {"GO:0097193", "GO:0097194"},
        }

        results = find_pmids_covering_genes(
            genes=["TP53", "BRCA1"],
            go_ids=["GO:0006915"],
            ref_index=ref_index,
            descendants_closure=descendants_closure,
            min_genes=2,
        )

        # PMID 12345678 should cover both genes (via direct and descendant match)
        assert len(results) >= 1
        assert results[0]["pmid"] == "12345678"

    def test_no_results(self):
        """Test when no PMIDs meet criteria."""
        ref_index = {
            "gene_go_pmids": {
                "TP53": {"GO:0006915": {"12345678"}},
                "BRCA1": {"GO:0006915": {"23456789"}},  # Different PMID
            },
            "pmid_gene_gos": {},
        }

        results = find_pmids_covering_genes(
            genes=["TP53", "BRCA1"],
            go_ids=["GO:0006915"],
            ref_index=ref_index,
            min_genes=2,  # Require 2+ genes per PMID
        )

        # No single PMID covers both genes
        assert len(results) == 0

    def test_sorted_by_coverage(self):
        """Test results are sorted by gene coverage."""
        ref_index = {
            "gene_go_pmids": {
                "TP53": {"GO:0006915": {"11111111", "22222222"}},
                "BRCA1": {"GO:0006915": {"11111111", "22222222"}},
                "ATM": {"GO:0006915": {"11111111"}},  # Only in first PMID
            },
            "pmid_gene_gos": {},
        }

        results = find_pmids_covering_genes(
            genes=["TP53", "BRCA1", "ATM"],
            go_ids=["GO:0006915"],
            ref_index=ref_index,
            min_genes=2,
        )

        # PMID 11111111 covers 3 genes, 22222222 covers 2
        assert len(results) == 2
        assert len(results[0]["genes_covered"]) >= len(results[1]["genes_covered"])
