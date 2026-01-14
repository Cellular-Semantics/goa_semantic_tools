"""
GO Enrichment Service

Main service for hierarchical GO enrichment analysis with top-N roots clustering.
"""
from datetime import datetime, timezone
from typing import Any

from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS

from ..utils.data_downloader import ensure_gaf_data, ensure_go_data
from ..utils.go_data_loader import build_gene_to_go_mapping, load_gene_annotations, load_go_data
from ..utils.go_hierarchy import cluster_by_top_n_roots, get_cluster_contributing_genes


def run_go_enrichment(
    gene_symbols: list[str],
    species: str = "human",
    top_n_roots: int = 5,
    fdr_threshold: float = 0.05,
) -> dict[str, Any]:
    """
    Run hierarchical GO enrichment analysis with top-N roots clustering.

    This is the main entry point for Phase 1 GO enrichment. It:
    1. Downloads and caches GO/GAF data if needed
    2. Loads GO ontology and gene annotations
    3. Runs enrichment analysis with GOATOOLS
    4. Clusters enriched terms using top-N roots algorithm
    5. Returns structured results matching go_enrichment_output schema

    Args:
        gene_symbols: List of gene symbols to analyze (e.g., ["TP53", "BRCA1"])
        species: Species for annotations ("human" or "mouse")
        top_n_roots: Number of top enriched terms to use as cluster roots per namespace
        fdr_threshold: FDR significance threshold (Benjamini-Hochberg correction)

    Returns:
        Dictionary matching go_enrichment_output.schema.json:
        {
            'clusters': [
                {
                    'root_term': {...},
                    'member_terms': [...],
                    'contributing_genes': [...]
                },
                ...
            ],
            'metadata': {
                'input_genes_count': ...,
                'genes_with_annotations': ...,
                'total_enriched_terms': ...,
                ...
            }
        }

    Raises:
        ValueError: If input parameters are invalid
        FileNotFoundError: If data files cannot be found or downloaded
        Exception: If enrichment analysis fails

    Example:
        >>> result = run_go_enrichment(
        ...     gene_symbols=["TP53", "BRCA1", "BRCA2"],
        ...     species="human",
        ...     top_n_roots=5,
        ...     fdr_threshold=0.05
        ... )
        >>> print(f"Found {len(result['clusters'])} clusters")
        >>> print(f"Total enriched terms: {result['metadata']['total_enriched_terms']}")
    """
    # Validate inputs
    if not gene_symbols:
        raise ValueError("gene_symbols cannot be empty")

    if species not in ["human", "mouse"]:
        raise ValueError(f"Unsupported species: {species}")

    if top_n_roots < 1:
        raise ValueError("top_n_roots must be >= 1")

    if not 0 < fdr_threshold <= 1:
        raise ValueError("fdr_threshold must be between 0 and 1")

    print("=" * 80)
    print("GO Enrichment Analysis - Phase 1")
    print("=" * 80)

    # Step 1: Ensure data is available
    print("\n[1/6] Ensuring reference data is available...")
    go_obo_path = ensure_go_data()
    gaf_path = ensure_gaf_data(species=species)

    # Step 2: Load GO ontology
    print("\n[2/6] Loading GO ontology...")
    godag = load_go_data(go_obo_path)

    # Step 3: Load annotations
    print("\n[3/6] Loading gene annotations...")
    ns2assoc = load_gene_annotations(gaf_path, godag)
    gene_to_annotations = build_gene_to_go_mapping(gaf_path, godag)

    # Get population (all genes with annotations)
    all_genes = set()
    for ns_genes in ns2assoc.values():
        all_genes.update(ns_genes.keys())
    population = all_genes

    print(f"  Total population: {len(population):,} genes")

    # Filter study genes to those in population
    study_set = set(g for g in gene_symbols if g in population)
    genes_not_found = set(gene_symbols) - study_set

    print(f"  Study genes: {len(gene_symbols)} requested, {len(study_set)} found")
    if genes_not_found:
        print(f"  Genes not found in annotations: {sorted(genes_not_found)}")

    if not study_set:
        # No genes found - return empty result
        return _empty_result(gene_symbols, species, fdr_threshold)

    # Step 4: Run enrichment analysis
    print("\n[4/6] Running GO enrichment analysis...")
    print(f"  Study set: {len(study_set)} genes")
    print(f"  Population: {len(population)} genes")
    print(f"  FDR threshold: {fdr_threshold}")

    goeaobj = GOEnrichmentStudyNS(
        population, ns2assoc, godag, propagate_counts=True, alpha=fdr_threshold, methods=["fdr_bh"]
    )

    goea_results_all = goeaobj.run_study(study_set)

    # Filter significant results
    goea_results_sig = [r for r in goea_results_all if r.p_fdr_bh < fdr_threshold]

    print(f"  Total terms tested: {len(goea_results_all)}")
    print(f"  Significant terms (FDR < {fdr_threshold}): {len(goea_results_sig)}")

    if not goea_results_sig:
        # No enrichment found
        return _empty_result(gene_symbols, species, fdr_threshold)

    # Step 5: Cluster results
    print(f"\n[5/6] Clustering enriched terms (top-{top_n_roots} roots)...")
    clusters = cluster_by_top_n_roots(goea_results_sig, godag, top_n=top_n_roots)

    print(f"  Created {len(clusters)} clusters")

    # Step 6: Build output
    print("\n[6/6] Building output structure...")
    output = _build_output(
        clusters=clusters,
        gene_to_annotations=gene_to_annotations,
        godag=godag,
        input_genes=gene_symbols,
        study_set=study_set,
        total_enriched=len(goea_results_sig),
        fdr_threshold=fdr_threshold,
        species=species,
        population_size=len(population),
    )

    print("\n" + "=" * 80)
    print(f"Enrichment analysis complete!")
    print(f"  Clusters: {len(output['clusters'])}")
    print(f"  Total enriched terms: {output['metadata']['total_enriched_terms']}")
    print("=" * 80)

    return output


def _build_output(
    clusters: list[dict[str, Any]],
    gene_to_annotations: dict[str, list[dict[str, Any]]],
    godag: Any,
    input_genes: list[str],
    study_set: set[str],
    total_enriched: int,
    fdr_threshold: float,
    species: str,
    population_size: int,
) -> dict[str, Any]:
    """
    Build output structure matching go_enrichment_output schema.

    Args:
        clusters: List of cluster dictionaries from cluster_by_top_n_roots
        gene_to_annotations: Gene to annotations mapping
        godag: GO DAG object for term ancestry checks
        input_genes: Original input gene list
        study_set: Filtered study genes (found in annotations)
        total_enriched: Total number of enriched terms before clustering
        fdr_threshold: FDR threshold used
        species: Species analyzed
        population_size: Total population size

    Returns:
        Dictionary matching go_enrichment_output schema
    """
    output_clusters = []

    for cluster in clusters:
        root = cluster["root"]
        members = cluster["members"]

        # Calculate fold enrichment for root
        ratio_study = root.study_count / len(study_set)
        ratio_pop = root.pop_count / population_size
        fold_enrichment = ratio_study / ratio_pop if ratio_pop > 0 else 0

        # Build root term
        root_term = {
            "go_id": root.GO,
            "name": root.name,
            "namespace": _namespace_abbrev_to_full(root.NS),
            "p_value": float(root.p_uncorrected),
            "fdr": float(root.p_fdr_bh),
            "fold_enrichment": float(fold_enrichment),
            "study_count": int(root.study_count),
            "population_count": int(root.pop_count),
            "study_genes": sorted(root.study_items),
        }

        # Build member terms
        member_terms = []
        for member in members:
            ratio_study_m = member.study_count / len(study_set)
            ratio_pop_m = member.pop_count / population_size
            fold_m = ratio_study_m / ratio_pop_m if ratio_pop_m > 0 else 0

            member_terms.append(
                {
                    "go_id": member.GO,
                    "name": member.name,
                    "namespace": _namespace_abbrev_to_full(member.NS),
                    "p_value": float(member.p_uncorrected),
                    "fdr": float(member.p_fdr_bh),
                    "fold_enrichment": float(fold_m),
                    "study_count": int(member.study_count),
                    "population_count": int(member.pop_count),
                    "study_genes": sorted(member.study_items),
                }
            )

        # Get contributing genes
        contributing_genes = get_cluster_contributing_genes(cluster, gene_to_annotations, godag)

        output_clusters.append(
            {
                "root_term": root_term,
                "member_terms": member_terms,
                "contributing_genes": contributing_genes,
            }
        )

    # Build metadata
    metadata = {
        "input_genes_count": len(input_genes),
        "genes_with_annotations": len(study_set),
        "total_enriched_terms": total_enriched,
        "clusters_count": len(output_clusters),
        "fdr_threshold": fdr_threshold,
        "species": species,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return {"clusters": output_clusters, "metadata": metadata}


def _empty_result(
    gene_symbols: list[str], species: str, fdr_threshold: float
) -> dict[str, Any]:
    """
    Build empty result when no enrichment is found.

    Args:
        gene_symbols: Input gene symbols
        species: Species analyzed
        fdr_threshold: FDR threshold used

    Returns:
        Empty result matching schema
    """
    return {
        "clusters": [],
        "metadata": {
            "input_genes_count": len(gene_symbols),
            "genes_with_annotations": 0,
            "total_enriched_terms": 0,
            "clusters_count": 0,
            "fdr_threshold": fdr_threshold,
            "species": species,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


def _namespace_abbrev_to_full(abbrev: str) -> str:
    """
    Convert namespace abbreviation to full name.

    Args:
        abbrev: Namespace abbreviation (BP, CC, MF)

    Returns:
        Full namespace name

    Raises:
        ValueError: If abbreviation is not recognized
    """
    mapping = {
        "BP": "biological_process",
        "CC": "cellular_component",
        "MF": "molecular_function",
    }

    if abbrev not in mapping:
        raise ValueError(f"Unknown namespace abbreviation: {abbrev}")

    return mapping[abbrev]
