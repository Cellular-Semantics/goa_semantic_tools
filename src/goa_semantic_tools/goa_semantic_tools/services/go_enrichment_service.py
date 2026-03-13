"""
GO Enrichment Service

Main service for hierarchical GO enrichment analysis with depth-anchor clustering.
"""
from datetime import datetime, timezone
from typing import Any

from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS

from ..utils.data_downloader import ensure_gaf_data, ensure_go_data
from ..utils.go_data_loader import load_gene_annotations, load_go_data
from ..utils.go_hierarchy import (
    EnrichedTerm,
    build_depth_anchor_themes,
    compute_enrichment_leaves,
    compute_hub_genes,
    enriched_terms_to_dict,
    themes_to_dict,
)


NAMESPACE_MAP: dict[str, str] = {
    "BP": "biological_process",
    "MF": "molecular_function",
    "CC": "cellular_component",
}

_ALL_NAMESPACES = list(NAMESPACE_MAP.values())


def run_go_enrichment(
    gene_symbols: list[str],
    species: str = "human",
    fdr_threshold: float = 0.05,
    depth_range: tuple[int, int] = (4, 7),
    min_children: int = 2,
    max_genes: int = 30,
    namespaces: list[str] | None = None,
) -> dict[str, Any]:
    """
    Run hierarchical GO enrichment analysis with depth-anchor clustering.

    This is the main entry point for GO enrichment. It:
    1. Downloads and caches GO/GAF data if needed
    2. Loads GO ontology and gene annotations
    3. Runs enrichment analysis with GOATOOLS
    4. Computes enrichment leaves (most specific terms) FIRST
    5. Builds hierarchical themes on top of leaves
    6. Returns structured results

    Args:
        gene_symbols: List of gene symbols to analyze (e.g., ["TP53", "BRCA1"])
        species: Species for annotations ("human" or "mouse")
        fdr_threshold: FDR significance threshold (Benjamini-Hochberg correction)
        depth_range: GO depth range for anchor candidates
        min_children: Minimum enriched descendants to qualify as anchor
        max_genes: Filter overly general terms with > max_genes
        namespaces: GO namespace codes to include, e.g. ["BP"] or ["BP", "MF"].
            Valid values: "BP" (biological_process), "MF" (molecular_function),
            "CC" (cellular_component). Default (None) = all three namespaces.

    Returns:
        Dictionary with enrichment results:
        {
            'enrichment_leaves': [...],  # Most specific enriched terms
            'themes': [...],             # Hierarchical groupings of leaves
            'hub_genes': {...},          # Genes appearing in 3+ themes
            'metadata': {...}
        }

    Raises:
        ValueError: If input parameters are invalid
        FileNotFoundError: If data files cannot be found or downloaded
        Exception: If enrichment analysis fails

    Example:
        >>> result = run_go_enrichment(
        ...     gene_symbols=["TP53", "BRCA1", "BRCA2"],
        ...     species="human",
        ...     depth_range=(4, 7)
        ... )
        >>> print(f"Found {len(result['enrichment_leaves'])} leaves")
        >>> print(f"Grouped into {len(result['themes'])} themes")
    """
    # Validate inputs
    if not gene_symbols:
        raise ValueError("gene_symbols cannot be empty")

    if species not in ["human", "mouse"]:
        raise ValueError(f"Unsupported species: {species}")

    if not 0 < fdr_threshold <= 1:
        raise ValueError("fdr_threshold must be between 0 and 1")

    if namespaces is not None:
        invalid = [n for n in namespaces if n.upper() not in NAMESPACE_MAP]
        if invalid:
            raise ValueError(f"Invalid namespace(s): {invalid}. Valid: {list(NAMESPACE_MAP.keys())}")

    ns_to_run = (
        [NAMESPACE_MAP[n.upper()] for n in namespaces] if namespaces else _ALL_NAMESPACES
    )

    print("=" * 80)
    print("GO Enrichment Analysis")
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
        return _empty_result(gene_symbols, species, fdr_threshold, depth_range)

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
        return _empty_result(gene_symbols, species, fdr_threshold, depth_range)

    # Convert GOATOOLS results to EnrichedTerm format
    enriched_terms = _convert_to_enriched_terms(goea_results_sig, godag)

    # Step 5: Compute enrichment leaves FIRST (correct data flow)
    print(f"\n[5/6] Computing enrichment leaves and hierarchical themes...")

    # Compute leaves FIRST - the complete set of most specific terms
    all_leaves = []
    for namespace in ns_to_run:
        ns_terms = {k: v for k, v in enriched_terms.items() if v.namespace == namespace}
        if ns_terms:
            ns_leaves = compute_enrichment_leaves(
                ns_terms, godag, fdr_threshold=fdr_threshold, max_genes=max_genes
            )
            all_leaves.extend(ns_leaves)

    # Sort all leaves by FDR
    all_leaves.sort(key=lambda x: x.fdr)
    print(f"  Enrichment leaves: {len(all_leaves)} (most specific terms)")

    # Build themes ON TOP of leaves (hierarchical grouping)
    all_themes = []
    for namespace in ns_to_run:
        ns_terms = {k: v for k, v in enriched_terms.items() if v.namespace == namespace}
        if ns_terms:
            themes = build_depth_anchor_themes(
                ns_terms,
                godag,
                depth_range=depth_range,
                min_children=min_children,
                max_genes=max_genes,
                fdr_threshold=fdr_threshold,
            )
            all_themes.extend(themes)

    # Sort all themes by FDR
    all_themes.sort(key=lambda t: t.anchor_term.fdr)

    n_with_children = sum(1 for t in all_themes if t.specific_terms)
    n_standalone = sum(1 for t in all_themes if not t.specific_terms)
    print(f"  Themes: {len(all_themes)} ({n_with_children} hierarchical, {n_standalone} standalone)")

    # Convert to dict format
    leaves_dict = enriched_terms_to_dict(all_leaves)
    themes_dict = themes_to_dict(all_themes)

    # Compute hub genes
    hub_genes = compute_hub_genes(themes_dict, min_themes=3)
    print(f"  Hub genes: {len(hub_genes)} (appearing in 3+ themes)")

    # Step 6: Build output
    print("\n[6/6] Building output structure...")
    output = _build_output(
        enrichment_leaves=leaves_dict,
        themes=themes_dict,
        hub_genes=hub_genes,
        input_genes=gene_symbols,
        study_set=study_set,
        total_enriched=len(goea_results_sig),
        fdr_threshold=fdr_threshold,
        species=species,
        depth_range=depth_range,
    )

    print("\n" + "=" * 80)
    print("Enrichment analysis complete!")
    print(f"  Enrichment leaves: {len(output['enrichment_leaves'])}")
    print(f"  Themes: {len(output['themes'])}")
    print(f"  Hub genes: {len(output['hub_genes'])}")
    print(f"  Total enriched terms: {output['metadata']['total_enriched_terms']}")
    print("=" * 80)

    return output


def _build_output(
    enrichment_leaves: list[dict[str, Any]],
    themes: list[dict[str, Any]],
    hub_genes: dict[str, Any],
    input_genes: list[str],
    study_set: set[str],
    total_enriched: int,
    fdr_threshold: float,
    species: str,
    depth_range: tuple[int, int],
) -> dict[str, Any]:
    """
    Build output structure for enrichment results.

    Args:
        enrichment_leaves: List of enrichment leaf dictionaries
        themes: List of theme dictionaries from themes_to_dict
        hub_genes: Hub gene dictionary from compute_hub_genes
        input_genes: Original input gene list
        study_set: Filtered study genes
        total_enriched: Total enriched terms
        fdr_threshold: FDR threshold used
        species: Species analyzed
        depth_range: Depth range for anchors

    Returns:
        Dictionary with enrichment_leaves, themes, hub_genes, and metadata
    """
    metadata = {
        "input_genes_count": len(input_genes),
        "genes_with_annotations": len(study_set),
        "total_enriched_terms": total_enriched,
        "enrichment_leaves_count": len(enrichment_leaves),
        "themes_count": len(themes),
        "themes_with_children": sum(1 for t in themes if t.get("n_specific_terms", 0) > 0),
        "hub_genes_count": len(hub_genes),
        "fdr_threshold": fdr_threshold,
        "species": species,
        "depth_range": list(depth_range),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return {
        "enrichment_leaves": enrichment_leaves,
        "themes": themes,
        "hub_genes": hub_genes,
        "metadata": metadata,
    }


def _empty_result(
    gene_symbols: list[str], species: str, fdr_threshold: float, depth_range: tuple[int, int]
) -> dict[str, Any]:
    """
    Build empty result when no enrichment is found.

    Args:
        gene_symbols: Input gene symbols
        species: Species analyzed
        fdr_threshold: FDR threshold used
        depth_range: Depth range for anchors

    Returns:
        Empty result matching schema
    """
    return {
        "enrichment_leaves": [],
        "themes": [],
        "hub_genes": {},
        "metadata": {
            "input_genes_count": len(gene_symbols),
            "genes_with_annotations": 0,
            "total_enriched_terms": 0,
            "enrichment_leaves_count": 0,
            "themes_count": 0,
            "themes_with_children": 0,
            "hub_genes_count": 0,
            "fdr_threshold": fdr_threshold,
            "species": species,
            "depth_range": list(depth_range),
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


def _convert_to_enriched_terms(goea_results: list[Any], godag: Any) -> dict[str, EnrichedTerm]:
    """
    Convert GOATOOLS enrichment results to EnrichedTerm format.

    Args:
        goea_results: List of GOEnrichmentRecord objects
        godag: GO DAG for depth lookup

    Returns:
        Dictionary mapping GO ID to EnrichedTerm
    """
    terms = {}

    for result in goea_results:
        go_id = result.GO
        depth = godag[go_id].depth if go_id in godag else 0

        # Calculate fold enrichment: (study_count/study_total) / (pop_count/pop_total)
        # ratio_in_study and ratio_in_pop are (count, total) tuples from GOATOOLS
        study_n, study_total = result.ratio_in_study
        pop_n, pop_total = result.ratio_in_pop
        study_rate = study_n / study_total if study_total > 0 else 0
        pop_rate = pop_n / pop_total if pop_total > 0 else 0
        fold = study_rate / pop_rate if pop_rate > 0 else 0

        terms[go_id] = EnrichedTerm(
            go_id=go_id,
            name=result.name,
            namespace=_namespace_abbrev_to_full(result.NS),
            fdr=float(result.p_fdr_bh),
            fold_enrichment=float(fold),
            genes=frozenset(result.study_items),
            depth=depth,
        )

    return terms
