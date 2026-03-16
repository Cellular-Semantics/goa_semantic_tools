"""
Reference Index Utility

Builds and queries a reference index from GO Annotation File (GAF) data.
Used for programmatic PMID lookup to support literature references.
"""
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from goatools.anno.gaf_reader import GafReader
from goatools.obo_parser import GODag


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class GOAnnotation:
    """A GO annotation with supporting references."""

    gene: str
    go_id: str
    go_name: str
    evidence_code: str
    references: set[str] = field(default_factory=set)  # PMIDs


# =============================================================================
# Reference Index Building
# =============================================================================


# Compiled regex for PMID extraction (reused for efficiency)
PMID_PATTERN = re.compile(r"PMID:(\d+)")


def load_gaf_with_pmids(
    gaf_path: Path | str,
    godag: GODag,
    genes_of_interest: set[str] | None = None,
) -> dict[str, Any]:
    """
    Load GAF annotations and build reference index.

    Parses a GAF (Gene Association File) and extracts PMID references
    for each gene-GO annotation pair. This index enables programmatic
    lookup of literature references for GO annotations.

    Args:
        gaf_path: Path to GAF file
        godag: GO DAG object for term name lookup
        genes_of_interest: Optional set of gene symbols to filter to.
            If None, loads all genes.

    Returns:
        Dictionary with structure:
        {
            'gene_go_pmids': {gene: {go_id: set(pmids)}},
            'pmid_gene_gos': {pmid: {gene: set(go_ids)}},
            'go_term_names': {go_id: name}
        }

    Example:
        >>> ref_index = load_gaf_with_pmids("goa_human.gaf", godag, {"TP53", "BRCA1"})
        >>> pmids = ref_index['gene_go_pmids']['TP53']['GO:0006915']
        >>> print(f"Found {len(pmids)} PMIDs for TP53 apoptosis annotations")
    """
    gaf_reader = GafReader(str(gaf_path))

    gene_go_pmids: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    pmid_gene_gos: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    go_term_names: dict[str, str] = {}

    for assoc in gaf_reader.associations:
        gene = assoc.DB_Symbol
        go_id = assoc.GO_ID
        refs = assoc.DB_Reference

        # Filter to genes of interest if specified
        if genes_of_interest and gene not in genes_of_interest:
            continue

        # Store GO term name
        if go_id in godag and go_id not in go_term_names:
            go_term_names[go_id] = godag[go_id].name

        # Extract PMIDs from references
        for ref in refs:
            match = PMID_PATTERN.match(ref)
            if match:
                pmid = match.group(1)
                gene_go_pmids[gene][go_id].add(pmid)
                pmid_gene_gos[pmid][gene].add(go_id)

    return {
        "gene_go_pmids": dict(gene_go_pmids),
        "pmid_gene_gos": dict(pmid_gene_gos),
        "go_term_names": go_term_names,
    }


def get_descendants_closure(go_ids: set[str], godag: GODag) -> dict[str, set[str]]:
    """
    Pre-compute descendant closure for each GO term.

    This is useful for reference lookup where we want to match
    annotations to more specific terms (descendants) of query terms.

    Args:
        go_ids: Set of GO IDs to compute closure for
        godag: GO DAG object

    Returns:
        Dictionary mapping GO ID to set of all descendant GO IDs:
        {go_id: set(all_descendant_ids)}

    Example:
        >>> closure = get_descendants_closure({"GO:0006915"}, godag)
        >>> descendants = closure["GO:0006915"]
        >>> print(f"Apoptosis has {len(descendants)} descendant terms")
    """
    closure: dict[str, set[str]] = {}

    for go_id in go_ids:
        if go_id not in godag:
            closure[go_id] = set()
            continue

        descendants: set[str] = set()
        to_visit = list(godag[go_id].children)

        while to_visit:
            child = to_visit.pop()
            if child.id not in descendants:
                descendants.add(child.id)
                to_visit.extend(child.children)

        closure[go_id] = descendants

    return closure


def get_pmids_for_gene_term(
    gene: str,
    go_id: str,
    ref_index: dict[str, Any],
    descendants_closure: dict[str, set[str]] | None = None,
) -> set[str]:
    """
    Get PMIDs for a gene annotated to a GO term (or its descendants).

    Args:
        gene: Gene symbol
        go_id: GO term ID
        ref_index: Reference index from load_gaf_with_pmids
        descendants_closure: Optional pre-computed descendant closure.
            If provided, includes PMIDs for annotations to descendant terms.

    Returns:
        Set of PMIDs supporting the annotation

    Example:
        >>> pmids = get_pmids_for_gene_term("TP53", "GO:0006915", ref_index)
        >>> print(f"Found {len(pmids)} supporting references")
    """
    gene_go_pmids = ref_index.get("gene_go_pmids", {})

    if gene not in gene_go_pmids:
        return set()

    gene_annotations = gene_go_pmids[gene]
    pmids: set[str] = set()

    # Direct match
    if go_id in gene_annotations:
        pmids.update(gene_annotations[go_id])

    # Include descendants if closure provided
    if descendants_closure and go_id in descendants_closure:
        for desc_id in descendants_closure[go_id]:
            if desc_id in gene_annotations:
                pmids.update(gene_annotations[desc_id])

    return pmids


def get_genes_for_pmid(
    pmid: str,
    ref_index: dict[str, Any],
) -> dict[str, set[str]]:
    """
    Get all genes and their GO annotations supported by a PMID.

    Args:
        pmid: PubMed ID (without "PMID:" prefix)
        ref_index: Reference index from load_gaf_with_pmids

    Returns:
        Dictionary mapping gene symbol to set of GO IDs:
        {gene: set(go_ids)}

    Example:
        >>> genes = get_genes_for_pmid("12345678", ref_index)
        >>> for gene, go_ids in genes.items():
        ...     print(f"{gene}: {len(go_ids)} GO terms")
    """
    pmid_gene_gos = ref_index.get("pmid_gene_gos", {})
    return pmid_gene_gos.get(pmid, {})


def find_pmids_covering_genes(
    genes: list[str],
    go_ids: list[str],
    ref_index: dict[str, Any],
    descendants_closure: dict[str, set[str]] | None = None,
    min_genes: int = 1,
) -> list[dict[str, Any]]:
    """
    Find PMIDs that annotate multiple genes to relevant GO terms.

    Useful for finding references that support multi-gene assertions.

    Args:
        genes: List of gene symbols
        go_ids: List of GO term IDs to consider
        ref_index: Reference index from load_gaf_with_pmids
        descendants_closure: Optional pre-computed descendant closure
        min_genes: Minimum number of genes a PMID must cover

    Returns:
        List of dictionaries with PMID info, sorted by gene coverage:
        [{'pmid': str, 'genes_covered': list, 'go_terms': list}, ...]

    Example:
        >>> results = find_pmids_covering_genes(
        ...     ["IL1B", "TNF", "IL6"],
        ...     ["GO:0006954"],
        ...     ref_index,
        ...     min_genes=2
        ... )
    """
    # Expand GO IDs to include descendants
    expanded_go_ids = set(go_ids)
    if descendants_closure:
        for go_id in go_ids:
            if go_id in descendants_closure:
                expanded_go_ids.update(descendants_closure[go_id])

    gene_go_pmids = ref_index.get("gene_go_pmids", {})
    pmid_gene_gos = ref_index.get("pmid_gene_gos", {})

    # Track which PMIDs annotate which genes to relevant terms
    pmid_coverage: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))

    for gene in genes:
        if gene not in gene_go_pmids:
            continue

        gene_annotations = gene_go_pmids[gene]

        for go_id in expanded_go_ids:
            if go_id in gene_annotations:
                for pmid in gene_annotations[go_id]:
                    pmid_coverage[pmid][gene].add(go_id)

    # Filter and format results
    results = []
    for pmid, gene_terms in pmid_coverage.items():
        if len(gene_terms) >= min_genes:
            results.append(
                {
                    "pmid": pmid,
                    "genes_covered": list(gene_terms.keys()),
                    "go_terms": list(set().union(*gene_terms.values())),
                    "gene_go_map": {g: sorted(gos) for g, gos in gene_terms.items()},
                }
            )

    # Sort by number of genes covered (descending), then by PMID (newer = higher)
    results.sort(key=lambda x: (len(x["genes_covered"]), int(x["pmid"])), reverse=True)

    return results
