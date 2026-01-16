"""
GO Hierarchy Utility

Implements top-N roots hierarchical clustering algorithm for GO enrichment results.
"""
from collections import defaultdict
from typing import Any

from goatools.obo_parser import GODag


def is_descendant(term_id: str, potential_ancestor_id: str, godag: GODag) -> bool:
    """
    Check if term_id is a descendant of potential_ancestor_id in GO hierarchy.

    A term is a descendant if the potential ancestor appears in its
    transitive closure of parents.

    Args:
        term_id: GO ID to check (e.g., "GO:0006915")
        potential_ancestor_id: Potential ancestor GO ID
        godag: GO DAG object

    Returns:
        True if term_id is a descendant of potential_ancestor_id, False otherwise

    Example:
        >>> is_descendant("GO:0006915", "GO:0008150", godag)  # apoptosis -> BP root
        True
        >>> is_descendant("GO:0008150", "GO:0006915", godag)  # root -> apoptosis
        False
    """
    # Validate inputs
    if term_id not in godag or potential_ancestor_id not in godag:
        return False

    # A term is not its own descendant
    if term_id == potential_ancestor_id:
        return False

    # Get all parents (ancestors) of term_id
    all_parents = godag[term_id].get_all_parents()

    # Check if potential_ancestor_id is in the ancestry
    return potential_ancestor_id in all_parents


def cluster_by_top_n_roots(
    enriched_terms: list[Any], godag: GODag, top_n: int = 5
) -> list[dict[str, Any]]:
    """
    Cluster enriched GO terms using top-N roots algorithm.

    Algorithm:
    1. Sort enriched terms by FDR (most significant first)
    2. Separate terms by namespace (BP, CC, MF)
    3. Select top-N terms from each namespace as cluster roots
    4. For each root, find all enriched terms that are descendants
    5. Avoid double-assignment (each term belongs to at most one cluster)
    6. Return clusters with root and member terms

    Args:
        enriched_terms: List of GOEnrichmentRecord objects (must have .p_fdr_bh, .GO, .NS)
        godag: GO DAG object
        top_n: Number of cluster roots to select per namespace (default: 5)

    Returns:
        List of cluster dictionaries:
        [
            {
                'root': GOEnrichmentRecord (cluster root term),
                'members': [GOEnrichmentRecord, ...] (descendant terms)
            },
            ...
        ]

    Example:
        >>> clusters = cluster_by_top_n_roots(sig_results, godag, top_n=5)
        >>> for cluster in clusters:
        ...     print(f"Root: {cluster['root'].name}")
        ...     print(f"  Members: {len(cluster['members'])}")
    """
    # Sort by FDR (most significant first)
    sorted_terms = sorted(enriched_terms, key=lambda x: x.p_fdr_bh)

    # Group by namespace
    ns_terms: dict[str, list[Any]] = defaultdict(list)
    for term in sorted_terms:
        ns_terms[term.NS].append(term)

    # Select top-N roots from each namespace
    all_roots: list[Any] = []
    for ns, terms in ns_terms.items():
        n_for_ns = min(top_n, len(terms))  # Don't exceed available terms
        all_roots.extend(terms[:n_for_ns])

    # Build clusters
    clusters: list[dict[str, Any]] = []
    used_terms: set[str] = set()  # Track assigned terms by GO ID

    for root in all_roots:
        root_id = root.GO
        root_ns = root.NS

        # Find descendant members
        members: list[Any] = []

        for term in sorted_terms:
            # Skip if same as root
            if term.GO == root_id:
                continue

            # Only same namespace
            if term.NS != root_ns:
                continue

            # Skip if already assigned
            if term.GO in used_terms:
                continue

            # Check if descendant
            if is_descendant(term.GO, root_id, godag):
                members.append(term)
                used_terms.add(term.GO)

        # Mark root as used
        used_terms.add(root_id)

        # Create cluster
        clusters.append({"root": root, "members": members})

    return clusters


def get_cluster_contributing_genes(
    cluster: dict[str, Any], gene_to_annotations: dict[str, list[dict[str, Any]]], godag: GODag
) -> list[dict[str, Any]]:
    """
    Get contributing genes for a cluster with their direct annotations.

    For each gene in the cluster, find all direct GO annotations that are
    either the root term, member terms, or descendants of cluster terms.
    This accounts for GO count propagation (genes annotated to children
    count for parents in enrichment).

    Args:
        cluster: Cluster dictionary with 'root' and 'members' keys
        gene_to_annotations: Mapping from gene symbol to list of annotations
            (from build_gene_to_go_mapping)
        godag: GO DAG object for checking term ancestry

    Returns:
        List of contributing gene dictionaries:
        [
            {
                'gene_symbol': 'TP53',
                'direct_annotations': [
                    {
                        'go_id': 'GO:0008285',
                        'go_name': 'negative regulation of...',
                        'evidence_code': 'IDA'
                    },
                    ...
                ]
            },
            ...
        ]
    """
    # Get all GO IDs in this cluster
    cluster_go_ids = {cluster["root"].GO}
    for member in cluster["members"]:
        cluster_go_ids.add(member.GO)

    # Get all genes mentioned in cluster (root + members)
    cluster_genes = set(cluster["root"].study_items)
    for member in cluster["members"]:
        cluster_genes.update(member.study_items)

    # Build contributing genes list
    contributing_genes: list[dict[str, Any]] = []

    for gene in sorted(cluster_genes):
        if gene not in gene_to_annotations:
            continue

        # Find annotations in this cluster
        # Include exact matches OR annotations where the term is a child of cluster terms
        gene_annotations = gene_to_annotations[gene]
        cluster_annotations = []

        for annot in gene_annotations:
            annot_go_id = annot["go_id"]

            # Direct match: annotation is in cluster
            if annot_go_id in cluster_go_ids:
                cluster_annotations.append(annot)
            # Propagated match: annotation is descendant of cluster term
            elif annot_go_id in godag:
                # Check if annotation is descendant of any cluster term
                for cluster_go_id in cluster_go_ids:
                    if is_descendant(annot_go_id, cluster_go_id, godag):
                        cluster_annotations.append(annot)
                        break  # Don't add same annotation multiple times

        if cluster_annotations:
            contributing_genes.append(
                {
                    "gene_symbol": gene,
                    "direct_annotations": cluster_annotations,
                }
            )

    return contributing_genes
