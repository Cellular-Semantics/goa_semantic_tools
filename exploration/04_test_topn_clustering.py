"""
Test Script 4: Test Top-N Roots Clustering Algorithm

This script tests the top-N roots hierarchical clustering algorithm
described in the PDF discussion.
"""
from pathlib import Path
from goatools.obo_parser import GODag
from goatools.anno.gaf_reader import GafReader
from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS
from collections import defaultdict
# Paths
GO_OBO_PATH = Path(__file__).parent.parent / "reference_data" / "go-basic.obo"
GAF_PATH = Path(__file__).parent.parent / "reference_data" / "goa_human.gaf"

def is_descendant(term_id, potential_ancestor_id, godag):
    """
    Check if term_id is a descendant of potential_ancestor_id.

    A term is a descendant if potential_ancestor_id is in its ancestors.
    """
    if term_id not in godag or potential_ancestor_id not in godag:
        return False

    if term_id == potential_ancestor_id:
        return False  # A term is not its own descendant

    # Get all parents (ancestors) of term_id
    all_parents = godag[term_id].get_all_parents()
    return potential_ancestor_id in all_parents

def cluster_by_top_n_roots(enriched_terms, godag, top_n=5):
    """
    Cluster enriched terms using top-N roots algorithm.

    Algorithm:
    1. Sort enriched terms by FDR (most significant first)
    2. Select top-N terms as cluster roots
    3. For each root, find all enriched terms that are descendants
    4. Return list of clusters with root and member terms

    Args:
        enriched_terms: List of GOEnrichmentRecord objects (already filtered for significance)
        godag: GO DAG object
        top_n: Number of cluster roots (default: 5)

    Returns:
        List of clusters, each containing:
        - root: GOEnrichmentRecord (cluster root)
        - members: List of GOEnrichmentRecord (descendants)
    """
    # Sort by FDR (most significant first)
    sorted_terms = sorted(enriched_terms, key=lambda x: x.p_fdr_bh)

    # Select top-N as roots (filter to same namespace to avoid mixing BP/MF/CC)
    # Group by namespace first
    ns_terms = defaultdict(list)
    for term in sorted_terms:
        ns_terms[term.NS].append(term)

    # Get top-N from each namespace
    all_roots = []
    for ns, terms in ns_terms.items():
        n_for_ns = min(top_n, len(terms))  # Don't exceed available terms
        all_roots.extend(terms[:n_for_ns])

    # For each root, find descendants
    clusters = []
    used_terms = set()  # Track which terms have been assigned to clusters

    for root in all_roots:
        root_id = root.GO
        root_ns = root.NS

        # Find members: enriched terms in same namespace that are descendants of root
        members = []
        for term in sorted_terms:
            if term.GO == root_id:
                continue  # Skip the root itself

            if term.NS != root_ns:
                continue  # Only same namespace

            if term.GO in used_terms:
                continue  # Already assigned to another cluster

            # Check if term is descendant of root
            if is_descendant(term.GO, root_id, godag):
                members.append(term)
                used_terms.add(term.GO)

        # Mark root as used
        used_terms.add(root_id)

        clusters.append({
            'root': root,
            'members': members
        })

    return clusters

def main():
    print("=" * 80)
    print("Test Script 4: Top-N Roots Clustering")
    print("=" * 80)

    # Load GO DAG
    print(f"\n1. Loading GO ontology...")
    godag = GODag(str(GO_OBO_PATH), optional_attrs={'relationship'})

    # Load GAF
    print(f"\n2. Loading GAF annotations...")
    gaf_reader = GafReader(str(GAF_PATH))

    # Build ns2assoc
    print(f"\n3. Building namespace-separated associations...")
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

    # Get population
    all_genes = set()
    for ns_genes in ns2assoc.values():
        all_genes.update(ns_genes.keys())
    population = all_genes

    # Define study set (tumor suppressors)
    study_genes = [
        'TP53', 'BRCA1', 'BRCA2', 'PTEN', 'RB1', 'APC', 'VHL',
        'CDKN2A', 'ATM', 'MLH1', 'MSH2', 'NF1', 'TSC1', 'TSC2'
    ]
    study_set = set([g for g in study_genes if g in all_genes])

    # Run enrichment
    print(f"\n4. Running enrichment...")
    goeaobj = GOEnrichmentStudyNS(
        population,
        ns2assoc,
        godag,
        propagate_counts=True,
        alpha=0.05,
        methods=['fdr_bh']
    )

    goea_results_all = goeaobj.run_study(study_set)
    goea_results_sig = [r for r in goea_results_all if r.p_fdr_bh < 0.05]
    print(f"   Found {len(goea_results_sig)} significant terms")

    # Test clustering with different top-N values
    for top_n in [3, 5, 10]:
        print(f"\n{'=' * 80}")
        print(f"Testing Top-{top_n} Roots Clustering")
        print(f"{'=' * 80}")

        clusters = cluster_by_top_n_roots(goea_results_sig, godag, top_n=top_n)

        print(f"\nTotal clusters: {len(clusters)}")

        # Count terms coverage
        total_assigned = sum(len(c['members']) + 1 for c in clusters)  # +1 for root
        print(f"Terms assigned to clusters: {total_assigned} / {len(goea_results_sig)}")

        # Show each cluster
        for i, cluster in enumerate(clusters, 1):
            root = cluster['root']
            members = cluster['members']

            # Calculate fold enrichment for root
            ratio_study = root.study_count / len(study_set)
            ratio_pop = root.pop_count / len(population)
            fold_enrichment = ratio_study / ratio_pop if ratio_pop > 0 else 0

            print(f"\nCluster {i}: {root.GO} - {root.name}")
            print(f"  Namespace: {root.NS}")
            print(f"  FDR: {root.p_fdr_bh:.2e}")
            print(f"  Fold Enrichment: {fold_enrichment:.2f}x")
            print(f"  Study genes: {len(root.study_items)} ({', '.join(sorted(root.study_items)[:3])}...)")
            print(f"  Members: {len(members)} descendant terms")

            if members:
                print(f"  Sample members:")
                for member in members[:5]:
                    ratio_study_m = member.study_count / len(study_set)
                    ratio_pop_m = member.pop_count / len(population)
                    fold_m = ratio_study_m / ratio_pop_m if ratio_pop_m > 0 else 0

                    print(f"    - {member.GO}: {member.name}")
                    print(f"      FDR: {member.p_fdr_bh:.2e}, Fold: {fold_m:.2f}x")

                if len(members) > 5:
                    print(f"    ... and {len(members) - 5} more")

        # Analyze unassigned terms
        all_cluster_terms = set()
        for cluster in clusters:
            all_cluster_terms.add(cluster['root'].GO)
            for member in cluster['members']:
                all_cluster_terms.add(member.GO)

        unassigned = [t for t in goea_results_sig if t.GO not in all_cluster_terms]
        if unassigned:
            print(f"\nUnassigned terms: {len(unassigned)}")
            print(f"Sample unassigned (top 5 by FDR):")
            for term in sorted(unassigned, key=lambda x: x.p_fdr_bh)[:5]:
                print(f"  - {term.GO}: {term.name} (FDR: {term.p_fdr_bh:.2e}, NS: {term.NS})")

    print("\n" + "=" * 80)
    print("Test completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    main()
