"""
Unit tests for GO Hierarchy utility functions.

Tests the depth-anchor algorithm and supporting functions.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from goa_semantic_tools.utils.go_hierarchy import (
    EnrichedTerm,
    HierarchicalTheme,
    _determine_confidence,
    build_depth_anchor_themes,
    compute_enrichment_leaves,
    compute_hub_genes,
    enriched_terms_to_dict,
    find_leaves,
    get_all_descendants,
    is_descendant,
    merge_identical_gene_sets,
    themes_to_dict,
)


# =============================================================================
# Mock GO DAG Helper
# =============================================================================


class MockGOTerm:
    """Mock GO term for testing."""

    def __init__(self, go_id: str, name: str, depth: int, children: list | None = None):
        self.id = go_id
        self.name = name
        self.depth = depth
        self.children = children or []
        self.relationship = {}
        self._all_parents: set[str] = set()

    def get_all_parents(self) -> set[str]:
        return self._all_parents

    def set_parents(self, parents: set[str]):
        self._all_parents = parents


def create_mock_godag() -> dict:
    """
    Create a mock GO DAG for testing.

    Structure:
    GO:0008150 (biological_process, depth=0)
    └── GO:0006950 (response to stress, depth=1)
        └── GO:0006954 (inflammatory response, depth=2)
            ├── GO:0006955 (immune response, depth=3)
            │   └── GO:0002376 (immune system process, depth=4)
            └── GO:0071222 (cellular response to LPS, depth=3)
    """
    # Create terms
    root = MockGOTerm("GO:0008150", "biological_process", 0)
    stress = MockGOTerm("GO:0006950", "response to stress", 1)
    inflammatory = MockGOTerm("GO:0006954", "inflammatory response", 2)
    immune = MockGOTerm("GO:0006955", "immune response", 3)
    immune_sys = MockGOTerm("GO:0002376", "immune system process", 4)
    lps = MockGOTerm("GO:0071222", "cellular response to LPS", 3)

    # Set up parent-child relationships
    root.children = [stress]
    stress.children = [inflammatory]
    inflammatory.children = [immune, lps]
    immune.children = [immune_sys]

    # Set up ancestry
    stress.set_parents({"GO:0008150"})
    inflammatory.set_parents({"GO:0008150", "GO:0006950"})
    immune.set_parents({"GO:0008150", "GO:0006950", "GO:0006954"})
    immune_sys.set_parents({"GO:0008150", "GO:0006950", "GO:0006954", "GO:0006955"})
    lps.set_parents({"GO:0008150", "GO:0006950", "GO:0006954"})

    return {
        "GO:0008150": root,
        "GO:0006950": stress,
        "GO:0006954": inflammatory,
        "GO:0006955": immune,
        "GO:0002376": immune_sys,
        "GO:0071222": lps,
    }


# =============================================================================
# Test EnrichedTerm Dataclass
# =============================================================================


@pytest.mark.unit
class TestEnrichedTerm:
    """Tests for EnrichedTerm dataclass."""

    def test_creation(self):
        """Test basic EnrichedTerm creation."""
        term = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
            genes=frozenset(["IL1B", "TNF", "IL6"]),
            depth=5,
        )

        assert term.go_id == "GO:0006954"
        assert term.name == "inflammatory response"
        assert term.fdr == 0.001
        assert len(term.genes) == 3
        assert term.depth == 5

    def test_default_genes(self):
        """Test EnrichedTerm with default empty genes."""
        term = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.01,
            fold_enrichment=3.0,
        )

        assert term.genes == frozenset()
        assert term.depth == 0

    def test_hash(self):
        """Test EnrichedTerm hashing (based on go_id)."""
        term1 = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
        )
        term2 = EnrichedTerm(
            go_id="GO:0006954",
            name="different name",  # Different name, same ID
            namespace="biological_process",
            fdr=0.05,
            fold_enrichment=2.0,
        )
        term3 = EnrichedTerm(
            go_id="GO:0006955",  # Different ID
            name="immune response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
        )

        # Same GO ID should have same hash
        assert hash(term1) == hash(term2)
        # Different GO ID should have different hash (usually)
        assert hash(term1) != hash(term3)

    def test_equality(self):
        """Test EnrichedTerm equality (based on go_id)."""
        term1 = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
        )
        term2 = EnrichedTerm(
            go_id="GO:0006954",
            name="different name",
            namespace="biological_process",
            fdr=0.05,
            fold_enrichment=2.0,
        )
        term3 = EnrichedTerm(
            go_id="GO:0006955",
            name="immune response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
        )

        assert term1 == term2  # Same GO ID
        assert term1 != term3  # Different GO ID
        assert term1 != "not a term"  # Different type

    def test_set_membership(self):
        """Test that EnrichedTerms can be used in sets."""
        term1 = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
        )
        term2 = EnrichedTerm(
            go_id="GO:0006954",
            name="different",
            namespace="biological_process",
            fdr=0.05,
            fold_enrichment=2.0,
        )
        term3 = EnrichedTerm(
            go_id="GO:0006955",
            name="immune response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
        )

        term_set = {term1, term2, term3}
        # term1 and term2 have same GO ID, so only one should be in set
        assert len(term_set) == 2


# =============================================================================
# Test HierarchicalTheme Dataclass
# =============================================================================


@pytest.mark.unit
class TestHierarchicalTheme:
    """Tests for HierarchicalTheme dataclass."""

    def test_creation(self):
        """Test HierarchicalTheme creation."""
        anchor = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
            genes=frozenset(["IL1B", "TNF"]),
        )
        specific1 = EnrichedTerm(
            go_id="GO:0006955",
            name="immune response",
            namespace="biological_process",
            fdr=0.005,
            fold_enrichment=4.0,
            genes=frozenset(["IL1B", "IL6"]),
        )

        theme = HierarchicalTheme(
            anchor_term=anchor,
            specific_terms=[specific1],
            anchor_confidence="FDR<0.01",
        )

        assert theme.anchor_term.go_id == "GO:0006954"
        assert len(theme.specific_terms) == 1
        assert theme.anchor_confidence == "FDR<0.01"

    def test_all_genes_property(self):
        """Test all_genes property combines genes from anchor and specifics."""
        anchor = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
            genes=frozenset(["IL1B", "TNF"]),
        )
        specific1 = EnrichedTerm(
            go_id="GO:0006955",
            name="immune response",
            namespace="biological_process",
            fdr=0.005,
            fold_enrichment=4.0,
            genes=frozenset(["IL1B", "IL6"]),  # IL1B overlaps with anchor
        )
        specific2 = EnrichedTerm(
            go_id="GO:0071222",
            name="cellular response to LPS",
            namespace="biological_process",
            fdr=0.01,
            fold_enrichment=3.0,
            genes=frozenset(["NFKB1", "RELA"]),
        )

        theme = HierarchicalTheme(
            anchor_term=anchor,
            specific_terms=[specific1, specific2],
            anchor_confidence="FDR<0.01",
        )

        all_genes = theme.all_genes
        assert all_genes == {"IL1B", "TNF", "IL6", "NFKB1", "RELA"}
        assert len(all_genes) == 5  # IL1B not counted twice

    def test_all_genes_empty_specifics(self):
        """Test all_genes with no specific terms."""
        anchor = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.05,
            fold_enrichment=2.0,
            genes=frozenset(["IL1B", "TNF"]),
        )

        theme = HierarchicalTheme(
            anchor_term=anchor,
            specific_terms=[],
            anchor_confidence="FDR<0.05",
        )

        assert theme.all_genes == {"IL1B", "TNF"}


# =============================================================================
# Test is_descendant Function
# =============================================================================


@pytest.mark.unit
class TestIsDescendant:
    """Tests for is_descendant function."""

    def test_direct_descendant(self):
        """Test detection of direct descendants."""
        godag = create_mock_godag()

        # stress is direct child of root
        assert is_descendant("GO:0006950", "GO:0008150", godag) is True

    def test_indirect_descendant(self):
        """Test detection of indirect descendants."""
        godag = create_mock_godag()

        # immune_sys is indirect descendant of stress
        assert is_descendant("GO:0002376", "GO:0006950", godag) is True
        # immune_sys is indirect descendant of root
        assert is_descendant("GO:0002376", "GO:0008150", godag) is True

    def test_not_descendant(self):
        """Test non-descendants return False."""
        godag = create_mock_godag()

        # root is not descendant of stress
        assert is_descendant("GO:0008150", "GO:0006950", godag) is False
        # lps is not descendant of immune
        assert is_descendant("GO:0071222", "GO:0006955", godag) is False

    def test_same_term(self):
        """Test that a term is not its own descendant."""
        godag = create_mock_godag()

        assert is_descendant("GO:0006954", "GO:0006954", godag) is False

    def test_missing_term(self):
        """Test behavior with missing terms."""
        godag = create_mock_godag()

        # Missing term_id
        assert is_descendant("GO:9999999", "GO:0008150", godag) is False
        # Missing potential_ancestor_id
        assert is_descendant("GO:0006954", "GO:9999999", godag) is False


# =============================================================================
# Test get_all_descendants Function
# =============================================================================


@pytest.mark.unit
class TestGetAllDescendants:
    """Tests for get_all_descendants function."""

    def test_descendants_of_root(self):
        """Test getting descendants of root term."""
        godag = create_mock_godag()

        descendants = get_all_descendants("GO:0008150", godag)

        # Root should have all other terms as descendants
        assert "GO:0006950" in descendants
        assert "GO:0006954" in descendants
        assert "GO:0006955" in descendants
        assert "GO:0002376" in descendants
        assert "GO:0071222" in descendants
        assert len(descendants) == 5

    def test_descendants_of_intermediate(self):
        """Test getting descendants of intermediate term."""
        godag = create_mock_godag()

        descendants = get_all_descendants("GO:0006954", godag)

        assert "GO:0006955" in descendants
        assert "GO:0002376" in descendants
        assert "GO:0071222" in descendants
        assert "GO:0008150" not in descendants  # Ancestor, not descendant
        assert "GO:0006950" not in descendants  # Ancestor, not descendant

    def test_descendants_of_leaf(self):
        """Test getting descendants of leaf term."""
        godag = create_mock_godag()

        descendants = get_all_descendants("GO:0002376", godag)

        assert len(descendants) == 0  # Leaf has no descendants

    def test_missing_term(self):
        """Test behavior with missing term."""
        godag = create_mock_godag()

        descendants = get_all_descendants("GO:9999999", godag)

        assert descendants == set()


# =============================================================================
# Test find_leaves Function
# =============================================================================


@pytest.mark.unit
class TestFindLeaves:
    """Tests for find_leaves function."""

    def test_find_leaves_basic(self):
        """Test finding leaves in a set of enriched terms."""
        godag = create_mock_godag()

        terms = {
            "GO:0006954": EnrichedTerm("GO:0006954", "inflammatory response", "biological_process", 0.01, 3.0),
            "GO:0006955": EnrichedTerm("GO:0006955", "immune response", "biological_process", 0.02, 2.5),
            "GO:0002376": EnrichedTerm("GO:0002376", "immune system process", "biological_process", 0.03, 2.0),
        }

        leaves = find_leaves(terms, godag, fdr_threshold=0.05)

        # GO:0002376 is a leaf (no enriched descendants)
        # GO:0006954 is not a leaf (has enriched descendants GO:0006955 and GO:0002376)
        # GO:0006955 is not a leaf (has enriched descendant GO:0002376)
        assert "GO:0002376" in leaves
        assert "GO:0006954" not in leaves
        assert "GO:0006955" not in leaves

    def test_find_leaves_with_fdr_filter(self):
        """Test that FDR threshold filters terms correctly."""
        godag = create_mock_godag()

        terms = {
            "GO:0006954": EnrichedTerm("GO:0006954", "inflammatory response", "biological_process", 0.01, 3.0),
            "GO:0006955": EnrichedTerm("GO:0006955", "immune response", "biological_process", 0.06, 2.5),  # Above threshold
            "GO:0002376": EnrichedTerm("GO:0002376", "immune system process", "biological_process", 0.03, 2.0),
        }

        leaves = find_leaves(terms, godag, fdr_threshold=0.05)

        # GO:0006955 is filtered out by FDR threshold
        # GO:0002376 is the only leaf among passing terms
        # GO:0006954 would be a leaf since GO:0006955 doesn't pass, but GO:0002376 does
        assert "GO:0002376" in leaves


# =============================================================================
# Test merge_identical_gene_sets Function
# =============================================================================


@pytest.mark.unit
class TestMergeIdenticalGeneSets:
    """Tests for merge_identical_gene_sets function."""

    def test_no_duplicates(self):
        """Test with no duplicate gene sets."""
        terms = {
            "GO:0006954": EnrichedTerm("GO:0006954", "inflammatory", "biological_process", 0.01, 3.0, frozenset(["A", "B"])),
            "GO:0006955": EnrichedTerm("GO:0006955", "immune", "biological_process", 0.02, 2.5, frozenset(["C", "D"])),
        }

        merged = merge_identical_gene_sets({"GO:0006954", "GO:0006955"}, terms)

        assert len(merged) == 2
        assert "GO:0006954" in merged
        assert "GO:0006955" in merged

    def test_merge_duplicates_keep_best_fdr(self):
        """Test merging duplicate gene sets - keep best FDR."""
        terms = {
            "GO:0006954": EnrichedTerm("GO:0006954", "term1", "biological_process", 0.01, 3.0, frozenset(["A", "B"])),
            "GO:0006955": EnrichedTerm("GO:0006955", "term2", "biological_process", 0.02, 2.5, frozenset(["A", "B"])),  # Same genes
            "GO:0071222": EnrichedTerm("GO:0071222", "term3", "biological_process", 0.03, 2.0, frozenset(["C", "D"])),
        }

        merged = merge_identical_gene_sets({"GO:0006954", "GO:0006955", "GO:0071222"}, terms)

        assert len(merged) == 2
        assert "GO:0006954" in merged  # Best FDR for gene set {A, B}
        assert "GO:0006955" not in merged
        assert "GO:0071222" in merged

    def test_merge_duplicates_tiebreaker_fold_enrichment(self):
        """Test merging when FDR is identical - use fold enrichment."""
        terms = {
            "GO:0006954": EnrichedTerm("GO:0006954", "term1", "biological_process", 0.01, 3.0, frozenset(["A", "B"])),
            "GO:0006955": EnrichedTerm("GO:0006955", "term2", "biological_process", 0.01, 5.0, frozenset(["A", "B"])),  # Same FDR, higher fold
        }

        merged = merge_identical_gene_sets({"GO:0006954", "GO:0006955"}, terms)

        assert len(merged) == 1
        assert "GO:0006955" in merged  # Higher fold enrichment wins


# =============================================================================
# Test _determine_confidence Function
# =============================================================================


@pytest.mark.unit
class TestDetermineConfidence:
    """Tests for _determine_confidence function."""

    def test_high_confidence(self):
        """Test FDR < 0.01."""
        assert _determine_confidence(0.001) == "FDR<0.01"
        assert _determine_confidence(0.009) == "FDR<0.01"

    def test_medium_confidence(self):
        """Test 0.01 <= FDR < 0.05."""
        assert _determine_confidence(0.01) == "FDR<0.05"
        assert _determine_confidence(0.02) == "FDR<0.05"
        assert _determine_confidence(0.049) == "FDR<0.05"

    def test_low_confidence(self):
        """Test 0.05 <= FDR < 0.10."""
        assert _determine_confidence(0.05) == "FDR<0.10"
        assert _determine_confidence(0.07) == "FDR<0.10"
        assert _determine_confidence(0.099) == "FDR<0.10"


# =============================================================================
# Test themes_to_dict Function
# =============================================================================


@pytest.mark.unit
class TestThemesToDict:
    """Tests for themes_to_dict function."""

    def test_conversion_basic(self):
        """Test basic theme to dict conversion."""
        anchor = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.001,
            fold_enrichment=5.0,
            genes=frozenset(["IL1B", "TNF"]),
            depth=5,
        )
        specific = EnrichedTerm(
            go_id="GO:0006955",
            name="immune response",
            namespace="biological_process",
            fdr=0.005,
            fold_enrichment=4.0,
            genes=frozenset(["IL1B", "IL6"]),
            depth=6,
        )

        theme = HierarchicalTheme(
            anchor_term=anchor,
            specific_terms=[specific],
            anchor_confidence="FDR<0.01",
        )

        result = themes_to_dict([theme])

        assert len(result) == 1
        theme_dict = result[0]

        # Check anchor
        assert theme_dict["anchor_term"]["go_id"] == "GO:0006954"
        assert theme_dict["anchor_term"]["name"] == "inflammatory response"
        assert theme_dict["anchor_term"]["fdr"] == 0.001
        assert theme_dict["anchor_term"]["depth"] == 5
        assert sorted(theme_dict["anchor_term"]["genes"]) == ["IL1B", "TNF"]

        # Check specific terms
        assert theme_dict["n_specific_terms"] == 1
        assert len(theme_dict["specific_terms"]) == 1
        assert theme_dict["specific_terms"][0]["go_id"] == "GO:0006955"

        # Check confidence
        assert theme_dict["anchor_confidence"] == "FDR<0.01"

        # Check all_genes
        assert set(theme_dict["all_genes"]) == {"IL1B", "TNF", "IL6"}

    def test_empty_specific_terms(self):
        """Test conversion with no specific terms."""
        anchor = EnrichedTerm(
            go_id="GO:0006954",
            name="inflammatory response",
            namespace="biological_process",
            fdr=0.05,
            fold_enrichment=2.0,
            genes=frozenset(["IL1B"]),
            depth=5,
        )

        theme = HierarchicalTheme(
            anchor_term=anchor,
            specific_terms=[],
            anchor_confidence="FDR<0.05",
        )

        result = themes_to_dict([theme])

        assert result[0]["n_specific_terms"] == 0
        assert result[0]["specific_terms"] == []


# =============================================================================
# Test compute_hub_genes Function
# =============================================================================


@pytest.mark.unit
class TestComputeHubGenes:
    """Tests for compute_hub_genes function."""

    def test_find_hub_genes(self):
        """Test identification of hub genes."""
        themes = [
            {
                "anchor_term": {
                    "name": "inflammatory response",
                    "go_id": "GO:0006954",
                    "genes": ["IL1B", "TNF", "IL6"],
                },
                "specific_terms": [
                    {"go_id": "GO:0006955", "genes": ["IL1B", "IFNG"]},
                ],
            },
            {
                "anchor_term": {
                    "name": "immune response",
                    "go_id": "GO:0002376",
                    "genes": ["IL1B", "CD4"],
                },
                "specific_terms": [],
            },
            {
                "anchor_term": {
                    "name": "cytokine signaling",
                    "go_id": "GO:0019221",
                    "genes": ["IL1B", "STAT3"],
                },
                "specific_terms": [],
            },
        ]

        hub_genes = compute_hub_genes(themes, min_themes=3)

        # IL1B appears in all 3 themes
        assert "IL1B" in hub_genes
        assert hub_genes["IL1B"]["theme_count"] == 3

        # TNF only appears in 1 theme
        assert "TNF" not in hub_genes

    def test_min_themes_threshold(self):
        """Test that min_themes threshold is respected."""
        themes = [
            {
                "anchor_term": {"name": "t1", "go_id": "GO:0001", "genes": ["A", "B"]},
                "specific_terms": [],
            },
            {
                "anchor_term": {"name": "t2", "go_id": "GO:0002", "genes": ["A", "C"]},
                "specific_terms": [],
            },
        ]

        # A appears in 2 themes
        hub_genes_2 = compute_hub_genes(themes, min_themes=2)
        assert "A" in hub_genes_2

        hub_genes_3 = compute_hub_genes(themes, min_themes=3)
        assert "A" not in hub_genes_3

    def test_hub_genes_sorted_by_count(self):
        """Test that hub genes are sorted by theme count."""
        themes = [
            {"anchor_term": {"name": "t1", "go_id": "GO:0001", "genes": ["A", "B"]}, "specific_terms": []},
            {"anchor_term": {"name": "t2", "go_id": "GO:0002", "genes": ["A", "B"]}, "specific_terms": []},
            {"anchor_term": {"name": "t3", "go_id": "GO:0003", "genes": ["A"]}, "specific_terms": []},
        ]

        hub_genes = compute_hub_genes(themes, min_themes=2)

        gene_list = list(hub_genes.keys())
        # A appears in 3 themes, B in 2 - A should be first
        assert gene_list[0] == "A"
        assert hub_genes["A"]["theme_count"] == 3
        assert hub_genes["B"]["theme_count"] == 2


# =============================================================================
# Test build_depth_anchor_themes Function
# =============================================================================


@pytest.mark.unit
class TestBuildDepthAnchorThemes:
    """Tests for build_depth_anchor_themes function."""

    def test_basic_theme_building(self):
        """Test basic theme building with simple hierarchy."""
        godag = create_mock_godag()

        # Create enriched terms at different depths
        terms = {
            "GO:0006950": EnrichedTerm(
                "GO:0006950", "response to stress", "biological_process",
                0.01, 5.0, frozenset(["A", "B", "C"]), depth=1
            ),
            "GO:0006954": EnrichedTerm(
                "GO:0006954", "inflammatory response", "biological_process",
                0.02, 4.0, frozenset(["A", "B"]), depth=2
            ),
            "GO:0006955": EnrichedTerm(
                "GO:0006955", "immune response", "biological_process",
                0.03, 3.0, frozenset(["A"]), depth=3
            ),
        }

        # With depth range 1-3, GO:0006950 could be anchor with GO:0006954 and GO:0006955 as children
        themes = build_depth_anchor_themes(
            terms, godag,
            depth_range=(1, 3),
            min_children=2,
            max_genes=30,
            fdr_threshold=0.10
        )

        assert len(themes) >= 1

    def test_max_genes_filter(self):
        """Test that terms with too many genes are filtered."""
        godag = create_mock_godag()

        terms = {
            "GO:0006954": EnrichedTerm(
                "GO:0006954", "inflammatory response", "biological_process",
                0.01, 5.0, frozenset([f"G{i}" for i in range(50)]), depth=5  # 50 genes
            ),
            "GO:0006955": EnrichedTerm(
                "GO:0006955", "immune response", "biological_process",
                0.02, 4.0, frozenset(["A", "B"]), depth=6
            ),
        }

        themes = build_depth_anchor_themes(
            terms, godag,
            depth_range=(4, 7),
            min_children=1,
            max_genes=30,  # Filter terms with > 30 genes
            fdr_threshold=0.10
        )

        # GO:0006954 should be filtered out due to too many genes
        for theme in themes:
            assert theme.anchor_term.go_id != "GO:0006954"


# =============================================================================
# Test compute_enrichment_leaves Function
# =============================================================================


@pytest.mark.unit
class TestComputeEnrichmentLeaves:
    """Tests for compute_enrichment_leaves function."""

    def test_basic_leaf_computation(self):
        """Test basic enrichment leaf computation."""
        godag = create_mock_godag()

        terms = {
            "GO:0006954": EnrichedTerm(
                "GO:0006954", "inflammatory response", "biological_process",
                0.01, 3.0, frozenset(["A", "B"]), depth=2
            ),
            "GO:0006955": EnrichedTerm(
                "GO:0006955", "immune response", "biological_process",
                0.02, 2.5, frozenset(["A"]), depth=3
            ),
            "GO:0002376": EnrichedTerm(
                "GO:0002376", "immune system process", "biological_process",
                0.03, 2.0, frozenset(["C"]), depth=4
            ),
        }

        leaves = compute_enrichment_leaves(terms, godag, fdr_threshold=0.05)

        # Should return list of EnrichedTerm objects
        assert isinstance(leaves, list)
        assert all(isinstance(t, EnrichedTerm) for t in leaves)

        # GO:0002376 is a leaf (no enriched descendants)
        leaf_ids = [t.go_id for t in leaves]
        assert "GO:0002376" in leaf_ids

    def test_leaves_sorted_by_fdr(self):
        """Test that leaves are sorted by FDR."""
        godag = create_mock_godag()

        # All leaf terms (no parent-child relationships in enriched set)
        terms = {
            "GO:0071222": EnrichedTerm(
                "GO:0071222", "cellular response to LPS", "biological_process",
                0.03, 2.0, frozenset(["A"]), depth=3
            ),
            "GO:0002376": EnrichedTerm(
                "GO:0002376", "immune system process", "biological_process",
                0.01, 3.0, frozenset(["B"]), depth=4
            ),
        }

        leaves = compute_enrichment_leaves(terms, godag, fdr_threshold=0.05)

        # Should be sorted by FDR (lowest first)
        if len(leaves) >= 2:
            assert leaves[0].fdr <= leaves[1].fdr

    def test_max_genes_filter(self):
        """Test that terms with too many genes are filtered."""
        godag = create_mock_godag()

        terms = {
            "GO:0002376": EnrichedTerm(
                "GO:0002376", "immune system process", "biological_process",
                0.01, 3.0, frozenset([f"G{i}" for i in range(50)]), depth=4  # 50 genes
            ),
            "GO:0071222": EnrichedTerm(
                "GO:0071222", "cellular response to LPS", "biological_process",
                0.02, 2.0, frozenset(["A", "B"]), depth=3  # 2 genes
            ),
        }

        leaves = compute_enrichment_leaves(terms, godag, fdr_threshold=0.05, max_genes=30)

        # GO:0002376 should be filtered out due to too many genes
        leaf_ids = [t.go_id for t in leaves]
        assert "GO:0002376" not in leaf_ids
        assert "GO:0071222" in leaf_ids


# =============================================================================
# Test enriched_terms_to_dict Function
# =============================================================================


@pytest.mark.unit
class TestEnrichedTermsToDict:
    """Tests for enriched_terms_to_dict function."""

    def test_basic_conversion(self):
        """Test basic conversion of EnrichedTerm to dict."""
        terms = [
            EnrichedTerm(
                go_id="GO:0006954",
                name="inflammatory response",
                namespace="biological_process",
                fdr=0.001,
                fold_enrichment=5.0,
                genes=frozenset(["IL1B", "TNF"]),
                depth=5,
            ),
            EnrichedTerm(
                go_id="GO:0006955",
                name="immune response",
                namespace="biological_process",
                fdr=0.01,
                fold_enrichment=3.0,
                genes=frozenset(["IL1B"]),
                depth=6,
            ),
        ]

        result = enriched_terms_to_dict(terms)

        assert len(result) == 2
        assert result[0]["go_id"] == "GO:0006954"
        assert result[0]["name"] == "inflammatory response"
        assert result[0]["fdr"] == 0.001
        assert result[0]["depth"] == 5
        assert sorted(result[0]["genes"]) == ["IL1B", "TNF"]

    def test_empty_list(self):
        """Test conversion of empty list."""
        result = enriched_terms_to_dict([])

        assert result == []

    def test_genes_sorted(self):
        """Test that genes are sorted in output."""
        terms = [
            EnrichedTerm(
                go_id="GO:0006954",
                name="test",
                namespace="biological_process",
                fdr=0.01,
                fold_enrichment=2.0,
                genes=frozenset(["ZEBRA", "ALPHA", "BETA"]),
                depth=3,
            ),
        ]

        result = enriched_terms_to_dict(terms)

        assert result[0]["genes"] == ["ALPHA", "BETA", "ZEBRA"]
