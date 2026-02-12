"""
Integration Tests for GO Enrichment Service

Tests the full GO enrichment pipeline with real GOATOOLS and downloaded data.
Requires GO ontology and GAF files (downloaded on first run).

IMPORTANT: These tests use REAL API calls and data downloads.
Use minimal gene sets to reduce cost and time.
"""
import os

import pytest

from goa_semantic_tools.services import run_go_enrichment


# =============================================================================
# Minimal End-to-End Test (RECOMMENDED for CI/quick validation)
# =============================================================================


@pytest.mark.integration
def test_minimal_enrichment_end_to_end() -> None:
    """
    Minimal end-to-end test with just 3 genes.

    Uses TP53, BRCA1, BRCA2 - well-characterized genes that should show
    enrichment for DNA repair and cell cycle terms.

    This is the CHEAPEST integration test - use for quick validation.
    """
    # Minimal gene set - 3 genes
    genes = ["TP53", "BRCA1", "BRCA2"]

    result = run_go_enrichment(
        gene_symbols=genes,
        species="human",
        fdr_threshold=0.05,
        depth_range=(4, 7),
        min_children=2,
        max_genes=30,
    )

    # Validate structure
    assert "enrichment_leaves" in result
    assert "themes" in result
    assert "hub_genes" in result
    assert "metadata" in result

    # Validate metadata
    metadata = result["metadata"]
    assert metadata["input_genes_count"] == 3
    assert metadata["genes_with_annotations"] == 3  # All should be found
    assert metadata["species"] == "human"
    assert metadata["fdr_threshold"] == 0.05

    # Should find some enrichment
    assert metadata["total_enriched_terms"] > 0

    # Validate enrichment_leaves structure
    leaves = result["enrichment_leaves"]
    if leaves:
        first_leaf = leaves[0]
        assert "go_id" in first_leaf
        assert first_leaf["go_id"].startswith("GO:")
        assert "name" in first_leaf
        assert "fdr" in first_leaf
        assert 0 <= first_leaf["fdr"] <= 0.05
        assert "genes" in first_leaf
        assert len(first_leaf["genes"]) > 0

    # Validate themes structure
    themes = result["themes"]
    if themes:
        first_theme = themes[0]
        assert "anchor_term" in first_theme
        assert "anchor_confidence" in first_theme
        assert first_theme["anchor_term"]["go_id"].startswith("GO:")

    print(f"\n✓ Minimal e2e test passed")
    print(f"  - Enrichment leaves: {len(leaves)}")
    print(f"  - Themes: {len(themes)}")
    print(f"  - Hub genes: {len(result['hub_genes'])}")


# =============================================================================
# Standard Tests (more comprehensive, higher cost)
# =============================================================================


@pytest.mark.integration
def test_go_enrichment_with_tumor_suppressors() -> None:
    """
    Test GO enrichment with tumor suppressor genes.

    Uses a medium set of genes that should show strong enrichment
    for cell cycle, DNA repair, and apoptosis terms.
    """
    # Medium gene set - 5 genes
    tumor_suppressors = [
        "TP53",   # Guardian of the genome
        "BRCA1",  # Breast cancer susceptibility
        "BRCA2",  # Breast cancer susceptibility
        "ATM",    # Ataxia telangiectasia mutated
        "CHEK2",  # Checkpoint kinase 2
    ]

    result = run_go_enrichment(
        gene_symbols=tumor_suppressors,
        species="human",
        fdr_threshold=0.05,
        depth_range=(4, 7),
    )

    # Validate structure
    assert "enrichment_leaves" in result
    assert "themes" in result
    assert "hub_genes" in result
    assert "metadata" in result

    metadata = result["metadata"]
    assert metadata["input_genes_count"] == len(tumor_suppressors)
    assert metadata["genes_with_annotations"] == len(tumor_suppressors)
    assert metadata["total_enriched_terms"] > 0

    # Check themes exist and are valid
    themes = result["themes"]
    assert len(themes) > 0, "Should have at least one theme"

    first_theme = themes[0]
    anchor = first_theme["anchor_term"]
    assert anchor["go_id"].startswith("GO:")
    assert len(anchor["name"]) > 0
    assert anchor["fdr"] <= 0.05

    # Check hub genes (all 5 genes should appear in multiple themes)
    hub_genes = result["hub_genes"]
    assert len(hub_genes) > 0, "Should have hub genes"

    print(f"\n✓ Tumor suppressors test passed")
    print(f"  - Themes: {len(themes)}")
    print(f"  - Hub genes: {len(hub_genes)}")
    if hub_genes:
        top_hub = list(hub_genes.keys())[0]
        print(f"  - Top hub: {top_hub} ({hub_genes[top_hub]['theme_count']} themes)")


@pytest.mark.integration
def test_go_enrichment_input_validation() -> None:
    """Test input validation for GO enrichment service."""
    # Empty gene list
    with pytest.raises(ValueError, match="gene_symbols cannot be empty"):
        run_go_enrichment(gene_symbols=[])

    # Invalid species
    with pytest.raises(ValueError, match="Unsupported species"):
        run_go_enrichment(gene_symbols=["TP53"], species="invalid")

    # Invalid FDR threshold
    with pytest.raises(ValueError, match="fdr_threshold must be between 0 and 1"):
        run_go_enrichment(gene_symbols=["TP53"], fdr_threshold=1.5)

    print("\n✓ All input validation tests passed")


@pytest.mark.integration
def test_go_enrichment_with_missing_genes() -> None:
    """Test GO enrichment when some genes are not in the annotation database."""
    # Mix of real genes and fake genes
    mixed_genes = ["TP53", "BRCA1", "FAKEGENE1", "FAKEGENE2", "BRCA2"]

    result = run_go_enrichment(
        gene_symbols=mixed_genes,
        species="human",
        fdr_threshold=0.05,
    )

    metadata = result["metadata"]
    assert metadata["input_genes_count"] == len(mixed_genes)
    assert metadata["genes_with_annotations"] == 3  # Only real genes found

    print(f"\n✓ Mixed genes test passed")
    print(f"  - Input genes: {metadata['input_genes_count']}")
    print(f"  - Found genes: {metadata['genes_with_annotations']}")


@pytest.mark.integration
def test_go_enrichment_with_no_enrichment() -> None:
    """
    Test GO enrichment with random genes that may not show enrichment.

    Uses a very small set of unrelated housekeeping genes.
    """
    # Very small set - may or may not enrich
    random_genes = ["ACTB", "GAPDH"]

    result = run_go_enrichment(
        gene_symbols=random_genes,
        species="human",
        fdr_threshold=0.05,
    )

    # Should still return valid structure even if no enrichment
    assert "enrichment_leaves" in result
    assert "themes" in result
    assert "hub_genes" in result
    assert "metadata" in result

    metadata = result["metadata"]
    assert metadata["input_genes_count"] == len(random_genes)

    print(f"\n✓ Low enrichment test passed")
    print(f"  - Enriched terms: {metadata['total_enriched_terms']}")
    print(f"  - Themes: {metadata.get('themes_count', 0)}")
