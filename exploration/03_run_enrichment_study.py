"""
Test Script 3: Run Basic GO Enrichment Study

This script tests running a GO enrichment study with GOATOOLS.
"""
from pathlib import Path
from goatools.obo_parser import GODag
from goatools.anno.gaf_reader import GafReader
from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS

# Paths
GO_OBO_PATH = Path(__file__).parent.parent / "reference_data" / "go-basic.obo"
GAF_PATH = Path(__file__).parent.parent / "reference_data" / "goa_human.gaf"

def main():
    print("=" * 80)
    print("Test Script 3: Run GO Enrichment Study")
    print("=" * 80)

    # Load GO DAG
    print(f"\n1. Loading GO ontology...")
    godag = GODag(str(GO_OBO_PATH), optional_attrs={'relationship'})
    print(f"   GO DAG loaded: {len(godag)} terms")

    # Load GAF annotations
    print(f"\n2. Loading GAF annotations...")
    gaf_reader = GafReader(str(GAF_PATH))
    print(f"   Loaded {len(gaf_reader.associations):,} associations")

    # Build gene to GO mapping - use namespace-specific format
    print(f"\n3. Building gene to GO mapping...")

    # First build simple gene2gos
    gene2gos_simple = {}
    for assoc in gaf_reader.associations:
        gene = assoc.DB_Symbol
        go_id = assoc.GO_ID

        if gene not in gene2gos_simple:
            gene2gos_simple[gene] = set()

        gene2gos_simple[gene].add(go_id)

    print(f"   Total unique genes: {len(gene2gos_simple):,}")

    # Now build namespace-separated associations for GOATOOLS
    # This matches what GafReader returns in get_ns2assc() method
    ns2assoc = {}
    for assoc in gaf_reader.associations:
        gene = assoc.DB_Symbol
        go_id = assoc.GO_ID

        if go_id in godag:
            ns = godag[go_id].namespace
            if ns not in ns2assoc:
                ns2assoc[ns] = {}
            if gene not in ns2assoc[ns]:
                ns2assoc[ns][gene] = set()
            ns2assoc[ns][gene].add(go_id)

    print(f"   Namespaces in associations: {list(ns2assoc.keys())}")

    # Get all genes as population
    population = set(gene2gos_simple.keys())
    print(f"   Population size: {len(population):,} genes")

    # Define study genes (tumor suppressors and related genes)
    study_genes = [
        'TP53', 'BRCA1', 'BRCA2', 'PTEN', 'RB1', 'APC', 'VHL',
        'CDKN2A', 'ATM', 'MLH1', 'MSH2', 'NF1', 'TSC1', 'TSC2'
    ]

    # Filter to genes in our data
    study_set = set([g for g in study_genes if g in gene2gos_simple])
    print(f"\n4. Study Set:")
    print(f"   Requested genes: {len(study_genes)}")
    print(f"   Found in data: {len(study_set)}")
    print(f"   Study genes: {sorted(study_set)}")

    # Create GO Enrichment Study
    print(f"\n5. Creating GO Enrichment Study...")
    goeaobj = GOEnrichmentStudyNS(
        population,
        ns2assoc,
        godag,
        propagate_counts=True,
        alpha=0.05,
        methods=['fdr_bh']
    )
    print(f"   Study created successfully")

    # Run enrichment
    print(f"\n6. Running Enrichment Analysis...")
    goea_results_all = goeaobj.run_study(study_set)
    print(f"   Total results: {len(goea_results_all)}")

    # Filter significant results
    goea_results_sig = [r for r in goea_results_all if r.p_fdr_bh < 0.05]
    print(f"   Significant results (FDR < 0.05): {len(goea_results_sig)}")

    # Show top 20 results
    print(f"\n7. Top 20 Enriched Terms:")
    goea_results_sig.sort(key=lambda x: x.p_fdr_bh)

    for i, result in enumerate(goea_results_sig[:20], 1):
        # Calculate fold enrichment
        ratio_study = result.study_count / len(study_set)
        ratio_pop = result.pop_count / len(population)
        fold_enrichment = ratio_study / ratio_pop if ratio_pop > 0 else 0

        print(f"\n   {i}. {result.GO} - {result.name}")
        print(f"      Namespace: {result.NS}")
        print(f"      P-value: {result.p_uncorrected:.2e}")
        print(f"      FDR: {result.p_fdr_bh:.2e}")
        print(f"      Fold Enrichment: {fold_enrichment:.2f}x")
        print(f"      Study count: {result.study_count} / {len(study_set)} ({ratio_study*100:.1f}%)")
        print(f"      Population count: {result.pop_count} / {len(population)} ({ratio_pop*100:.1f}%)")
        print(f"      Study genes: {', '.join(sorted(result.study_items)[:5])}" +
              (f" + {len(result.study_items)-5} more" if len(result.study_items) > 5 else ""))

    # Analyze by namespace
    print(f"\n8. Enrichment by Namespace:")
    ns_counts = {}
    for result in goea_results_sig:
        ns = result.NS
        ns_counts[ns] = ns_counts.get(ns, 0) + 1

    for ns, count in sorted(ns_counts.items()):
        print(f"   {ns}: {count} enriched terms")

    # Test GO hierarchy - show levels of enriched terms
    print(f"\n9. Hierarchy Levels of Enriched Terms:")
    level_counts = {}
    for result in goea_results_sig:
        if result.GO in godag:
            level = godag[result.GO].level
            level_counts[level] = level_counts.get(level, 0) + 1

    for level in sorted(level_counts.keys()):
        print(f"   Level {level}: {level_counts[level]} terms")

    # Test depth distribution
    print(f"\n10. Depth Distribution of Enriched Terms:")
    depth_counts = {}
    for result in goea_results_sig:
        if result.GO in godag:
            depth = godag[result.GO].depth
            depth_counts[depth] = depth_counts.get(depth, 0) + 1

    for depth in sorted(depth_counts.keys()):
        print(f"   Depth {depth}: {depth_counts[depth]} terms")

    print("\n" + "=" * 80)
    print("Test completed successfully!")
    print("=" * 80)

    return godag, gene2gos_simple, goeaobj, goea_results_sig

if __name__ == "__main__":
    godag, gene2gos, goeaobj, results = main()
