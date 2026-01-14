"""
Integration Tests for GO Enrichment Service

Tests the full GO enrichment pipeline with real GOATOOLS and downloaded data.
Requires GO ontology and GAF files (downloaded on first run).
"""
import os

import pytest
from jsonschema import validate

from goa_semantic_tools.schemas import load_schema
from goa_semantic_tools.services import run_go_enrichment


@pytest.mark.integration
def test_go_enrichment_with_tumor_suppressors() -> None:
    """
    Test GO enrichment with tumor suppressor genes.

    Uses a well-characterized set of genes that should show strong enrichment
    for cell cycle, DNA repair, and apoptosis terms.
    """
    # Well-characterized tumor suppressor genes
    tumor_suppressors = [
        "TP53",  # Guardian of the genome
        "BRCA1",  # Breast cancer susceptibility
        "BRCA2",  # Breast cancer susceptibility
        "PTEN",  # Phosphatase and tensin homolog
        "RB1",  # Retinoblastoma
        "APC",  # Adenomatous polyposis coli
        "VHL",  # Von Hippel-Lindau
        "CDKN2A",  # Cyclin-dependent kinase inhibitor 2A
        "ATM",  # Ataxia telangiectasia mutated
        "MLH1",  # MutL homolog 1
        "MSH2",  # MutS homolog 2
        "NF1",  # Neurofibromin 1
        "TSC1",  # Tuberous sclerosis 1
        "TSC2",  # Tuberous sclerosis 2
    ]

    # Run enrichment
    result = run_go_enrichment(
        gene_symbols=tumor_suppressors, species="human", top_n_roots=5, fdr_threshold=0.05
    )

    # Validate against schema
    output_schema = load_schema("go_enrichment_output.schema.json")
    validate(instance=result, schema=output_schema)

    # Check metadata
    metadata = result["metadata"]
    assert metadata["input_genes_count"] == len(tumor_suppressors)
    assert metadata["genes_with_annotations"] == len(tumor_suppressors)  # All should be found
    assert metadata["total_enriched_terms"] > 0, "Should find enriched terms for tumor suppressors"
    assert metadata["clusters_count"] > 0, "Should create at least one cluster"
    assert metadata["fdr_threshold"] == 0.05
    assert metadata["species"] == "human"

    # Check clusters exist
    clusters = result["clusters"]
    assert len(clusters) > 0, "Should have at least one cluster"

    # Check first cluster structure
    first_cluster = clusters[0]
    assert "root_term" in first_cluster
    assert "member_terms" in first_cluster
    assert "contributing_genes" in first_cluster

    # Validate root term
    root = first_cluster["root_term"]
    assert root["go_id"].startswith("GO:")
    assert len(root["name"]) > 0
    assert root["namespace"] in ["biological_process", "cellular_component", "molecular_function"]
    assert 0 <= root["p_value"] <= 1
    assert 0 <= root["fdr"] <= 0.05  # Below threshold
    assert root["fold_enrichment"] > 1.0  # Should be enriched, not depleted
    assert root["study_count"] > 0
    assert root["population_count"] > 0
    assert len(root["study_genes"]) > 0

    # Validate contributing genes
    contributing_genes = first_cluster["contributing_genes"]
    assert len(contributing_genes) > 0, "Should have contributing genes"

    first_gene = contributing_genes[0]
    assert "gene_symbol" in first_gene
    assert "direct_annotations" in first_gene
    assert len(first_gene["direct_annotations"]) > 0

    # Validate annotations
    first_annot = first_gene["direct_annotations"][0]
    assert first_annot["go_id"].startswith("GO:")
    assert len(first_annot["go_name"]) > 0
    assert len(first_annot["evidence_code"]) > 0

    # Check expected enrichment categories (tumor suppressors should enrich these)
    all_cluster_names = [c["root_term"]["name"].lower() for c in clusters]
    all_cluster_text = " ".join(all_cluster_names)

    # Should find cell cycle related terms
    assert any(
        keyword in all_cluster_text
        for keyword in ["cell cycle", "proliferation", "mitotic", "division"]
    ), "Should find cell cycle related enrichment"

    print(f"\n✓ Found {len(clusters)} clusters")
    print(f"✓ Total enriched terms: {metadata['total_enriched_terms']}")
    print(f"✓ Top cluster: {first_cluster['root_term']['name']}")
    print(f"  - FDR: {first_cluster['root_term']['fdr']:.2e}")
    print(f"  - Fold enrichment: {first_cluster['root_term']['fold_enrichment']:.2f}x")
    print(f"  - Contributing genes: {len(contributing_genes)}")


@pytest.mark.integration
def test_go_enrichment_with_no_enrichment() -> None:
    """
    Test GO enrichment with random genes that should not show enrichment.

    Uses a small set of unrelated housekeeping genes that should not
    cluster into functional categories.
    """
    # Random unrelated genes (housekeeping genes from different pathways)
    random_genes = ["ACTB", "GAPDH", "TUBB"]  # Very few genes, unlikely to enrich

    result = run_go_enrichment(
        gene_symbols=random_genes, species="human", top_n_roots=5, fdr_threshold=0.05
    )

    # Validate against schema
    output_schema = load_schema("go_enrichment_output.schema.json")
    validate(instance=result, schema=output_schema)

    # Should still return valid structure even if no enrichment
    assert "clusters" in result
    assert "metadata" in result

    metadata = result["metadata"]
    assert metadata["input_genes_count"] == len(random_genes)

    # May or may not find enrichment with such a small set
    # Just verify structure is valid
    print(f"\n✓ Random genes test completed")
    print(f"  - Enriched terms: {metadata['total_enriched_terms']}")
    print(f"  - Clusters: {metadata['clusters_count']}")


@pytest.mark.integration
def test_go_enrichment_input_validation() -> None:
    """Test input validation for GO enrichment service."""
    # Empty gene list
    with pytest.raises(ValueError, match="gene_symbols cannot be empty"):
        run_go_enrichment(gene_symbols=[], species="human")

    # Invalid species
    with pytest.raises(ValueError, match="Unsupported species"):
        run_go_enrichment(gene_symbols=["TP53"], species="invalid")

    # Invalid top_n_roots
    with pytest.raises(ValueError, match="top_n_roots must be >= 1"):
        run_go_enrichment(gene_symbols=["TP53"], top_n_roots=0)

    # Invalid FDR threshold
    with pytest.raises(ValueError, match="fdr_threshold must be between 0 and 1"):
        run_go_enrichment(gene_symbols=["TP53"], fdr_threshold=1.5)

    print("\n✓ All input validation tests passed")


@pytest.mark.integration
def test_go_enrichment_with_missing_genes() -> None:
    """Test GO enrichment when some genes are not in the annotation database."""
    # Mix of real genes and fake genes
    mixed_genes = ["TP53", "BRCA1", "FAKEGENE1", "FAKEGENE2", "BRCA2"]

    result = run_go_enrichment(gene_symbols=mixed_genes, species="human", top_n_roots=5)

    # Validate against schema
    output_schema = load_schema("go_enrichment_output.schema.json")
    validate(instance=result, schema=output_schema)

    metadata = result["metadata"]
    assert metadata["input_genes_count"] == len(mixed_genes)
    assert metadata["genes_with_annotations"] == 3  # Only real genes found
    assert metadata["total_enriched_terms"] >= 0  # May or may not enrich with 3 genes

    print(f"\n✓ Mixed genes test completed")
    print(f"  - Input genes: {metadata['input_genes_count']}")
    print(f"  - Found genes: {metadata['genes_with_annotations']}")


@pytest.mark.integration
def test_go_enrichment_different_top_n() -> None:
    """Test GO enrichment with different top_n_roots values."""
    tumor_suppressors = ["TP53", "BRCA1", "BRCA2", "PTEN", "RB1"]

    # Test with top-3
    result_top3 = run_go_enrichment(
        gene_symbols=tumor_suppressors, species="human", top_n_roots=3, fdr_threshold=0.05
    )

    # Test with top-10
    result_top10 = run_go_enrichment(
        gene_symbols=tumor_suppressors, species="human", top_n_roots=10, fdr_threshold=0.05
    )

    # Both should be valid
    output_schema = load_schema("go_enrichment_output.schema.json")
    validate(instance=result_top3, schema=output_schema)
    validate(instance=result_top10, schema=output_schema)

    # top-10 should have same or more clusters (unless not enough enriched terms)
    clusters_top3 = len(result_top3["clusters"])
    clusters_top10 = len(result_top10["clusters"])

    print(f"\n✓ Different top_n test completed")
    print(f"  - Top-3 clusters: {clusters_top3}")
    print(f"  - Top-10 clusters: {clusters_top10}")

    # If there are enough enriched terms, top-10 should have more clusters
    total_enriched = result_top3["metadata"]["total_enriched_terms"]
    if total_enriched > 30:  # Enough terms for meaningful difference
        assert clusters_top10 >= clusters_top3, "top-10 should create same or more clusters"
