"""
GO Hierarchy Utility

Implements depth-based anchor hierarchical clustering algorithm for GO enrichment results.
"""
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from goatools.obo_parser import GODag


# =============================================================================
# Data Classes for Depth-Anchor Algorithm
# =============================================================================


@dataclass
class EnrichedTerm:
    """Represents an enriched GO term with statistics and depth information."""

    go_id: str
    name: str
    namespace: str
    fdr: float
    fold_enrichment: float
    genes: frozenset = field(default_factory=frozenset)
    depth: int = 0

    def __hash__(self):
        return hash(self.go_id)

    def __eq__(self, other):
        if not isinstance(other, EnrichedTerm):
            return False
        return self.go_id == other.go_id


@dataclass
class HierarchicalTheme:
    """A hierarchical theme with anchor term and nested specific terms."""

    anchor_term: EnrichedTerm
    specific_terms: list[EnrichedTerm]
    anchor_confidence: str  # "FDR<0.01", "FDR<0.05", "FDR<0.10"

    @property
    def all_genes(self) -> set:
        """Get all genes across anchor and specific terms."""
        genes = set(self.anchor_term.genes)
        for specific in self.specific_terms:
            genes.update(specific.genes)
        return genes


# =============================================================================
# Hierarchy Navigation Functions
# =============================================================================


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
    if term_id not in godag or potential_ancestor_id not in godag:
        return False

    if term_id == potential_ancestor_id:
        return False

    all_parents = godag[term_id].get_all_parents()
    return potential_ancestor_id in all_parents


def get_all_descendants(go_id: str, godag: GODag) -> set[str]:
    """
    Get all descendants of a GO term using is_a and part_of relationships.

    Args:
        go_id: GO term identifier
        godag: GO DAG object

    Returns:
        Set of GO IDs that are descendants of the given term
    """
    if go_id not in godag:
        return set()

    term = godag[go_id]
    descendants = set()
    to_visit = list(term.children)

    while to_visit:
        child = to_visit.pop()
        if child.id not in descendants:
            descendants.add(child.id)
            to_visit.extend(child.children)

    # Check part_of reverse relationships
    for term_id, dag_term in godag.items():
        if hasattr(dag_term, "relationship") and dag_term.relationship:
            for rel_type, rel_terms in dag_term.relationship.items():
                if rel_type == "part_of":
                    for rel_term in rel_terms:
                        if rel_term.id == go_id and term_id not in descendants:
                            descendants.add(term_id)

    return descendants


# =============================================================================
# Depth-Anchor Theme Building Functions
# =============================================================================


def find_leaves(
    all_terms: dict[str, EnrichedTerm], godag: GODag, fdr_threshold: float
) -> set[str]:
    """
    Find enrichment leaves at FDR threshold.

    A leaf is an enriched term that has no enriched descendants.

    Args:
        all_terms: Dictionary of GO ID to EnrichedTerm
        godag: GO DAG object
        fdr_threshold: FDR threshold for significance

    Returns:
        Set of GO IDs that are leaves (no enriched descendants)
    """
    passing_ids = {go_id for go_id, term in all_terms.items() if term.fdr < fdr_threshold}

    leaves = set()
    for go_id in passing_ids:
        if go_id not in godag:
            continue
        descendants = get_all_descendants(go_id, godag)
        enriched_descendants = passing_ids & descendants
        if len(enriched_descendants) == 0:
            leaves.add(go_id)

    return leaves


def merge_identical_gene_sets(
    term_ids: set[str], terms: dict[str, EnrichedTerm]
) -> set[str]:
    """
    Merge terms with identical gene sets, keeping the one with best FDR.

    Args:
        term_ids: Set of GO IDs to consider
        terms: Dictionary mapping GO ID to EnrichedTerm

    Returns:
        Set of GO IDs after merging duplicates
    """
    gene_set_to_terms: dict[frozenset, list[str]] = defaultdict(list)
    for go_id in term_ids:
        if go_id in terms:
            gene_key = terms[go_id].genes
            gene_set_to_terms[gene_key].append(go_id)

    merged = set()
    for gene_set, group in gene_set_to_terms.items():
        if len(group) == 1:
            merged.add(group[0])
        else:
            # Keep term with best FDR, then highest fold enrichment
            best = min(group, key=lambda x: (terms[x].fdr, -terms[x].fold_enrichment))
            merged.add(best)

    return merged


def compute_enrichment_leaves(
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    fdr_threshold: float = 0.05,
    max_genes: int = 30,
) -> list[EnrichedTerm]:
    """
    Compute ALL enrichment leaves FIRST before building themes.

    Enrichment leaves are the most specific enriched terms - those with no
    enriched descendants at the given FDR threshold. After finding leaves,
    identical gene sets are merged (keeping best FDR).

    This is the foundational layer that captures the complete picture of
    specific enriched processes. Themes are built on top of these leaves.

    Args:
        terms: Dictionary mapping GO ID to EnrichedTerm
        godag: GO DAG object
        fdr_threshold: FDR threshold for significance
        max_genes: Filter out overly general terms (> max_genes)

    Returns:
        List of EnrichedTerm objects that are leaves, sorted by FDR
    """
    # Filter overly general terms
    filtered_terms = {k: v for k, v in terms.items() if len(v.genes) <= max_genes}

    # Find leaves (no enriched descendants)
    leaf_ids = find_leaves(filtered_terms, godag, fdr_threshold)

    # Merge identical gene sets (keep best FDR)
    merged_ids = merge_identical_gene_sets(leaf_ids, filtered_terms)

    # Build list of leaf terms
    leaves = [filtered_terms[go_id] for go_id in merged_ids if go_id in filtered_terms]

    # Sort by FDR
    leaves.sort(key=lambda x: x.fdr)

    return leaves


def enriched_terms_to_dict(terms: list[EnrichedTerm]) -> list[dict]:
    """
    Convert EnrichedTerm objects to JSON-serializable dictionaries.

    Args:
        terms: List of EnrichedTerm objects

    Returns:
        List of dictionaries suitable for JSON serialization
    """
    return [
        {
            "go_id": t.go_id,
            "name": t.name,
            "namespace": t.namespace,
            "fdr": t.fdr,
            "fold_enrichment": t.fold_enrichment,
            "genes": sorted(t.genes),
            "depth": t.depth,
        }
        for t in terms
    ]


def _determine_confidence(fdr: float) -> str:
    """Determine confidence level based on FDR."""
    if fdr < 0.01:
        return "FDR<0.01"
    elif fdr < 0.05:
        return "FDR<0.05"
    else:
        return "FDR<0.10"


def build_depth_anchor_themes(
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    depth_range: tuple[int, int] = (4, 7),
    min_children: int = 2,
    max_genes: int = 30,
    fdr_threshold: float = 0.10,
) -> list[HierarchicalTheme]:
    """
    Build hierarchical themes using depth-based non-leaf anchors.

    Algorithm:
    1. Filter terms by max_genes
    2. Find all enriched terms at intermediate depths with ≥min_children
    3. These become anchors; their enriched descendants become children
    4. Enforce no-overlap: each term assigned to at most one anchor
       (prefer more specific anchor = higher depth)
    5. Remaining leaves become standalone themes

    Args:
        terms: Dictionary mapping GO ID to EnrichedTerm
        godag: GO DAG object
        depth_range: Tuple of (min_depth, max_depth) for anchor candidates
        min_children: Minimum enriched descendants to qualify as anchor
        max_genes: Filter out overly general terms (> max_genes)
        fdr_threshold: FDR threshold for significance

    Returns:
        List of HierarchicalTheme objects sorted by anchor FDR
    """
    # Filter overly general terms
    terms = {k: v for k, v in terms.items() if len(v.genes) <= max_genes}

    enriched_ids = set(terms.keys())

    # Find anchor candidates: intermediate depth with ≥min_children enriched descendants
    anchor_candidates = []

    for go_id, term in terms.items():
        if go_id not in godag:
            continue

        # Check depth range
        if not (depth_range[0] <= term.depth <= depth_range[1]):
            continue

        # Count enriched descendants
        descendants = get_all_descendants(go_id, godag)
        enriched_descendants = descendants & enriched_ids

        if len(enriched_descendants) >= min_children:
            anchor_candidates.append(
                {
                    "go_id": go_id,
                    "term": term,
                    "depth": term.depth,
                    "n_enriched_children": len(enriched_descendants),
                    "enriched_children": enriched_descendants,
                }
            )

    # Sort by depth (prefer more specific = higher depth) then by FDR
    anchor_candidates.sort(key=lambda x: (-x["depth"], x["term"].fdr))

    # Assign children to anchors (no overlap - each child assigned to first anchor)
    assigned: set[str] = set()
    themes: list[HierarchicalTheme] = []

    for candidate in anchor_candidates:
        anchor_id = candidate["go_id"]

        if anchor_id in assigned:
            continue

        # Collect unassigned enriched descendants
        children = []
        for child_id in candidate["enriched_children"]:
            if child_id in assigned:
                continue
            if child_id == anchor_id:
                continue
            if child_id in terms:
                children.append(terms[child_id])

        if len(children) >= min_children:
            anchor_term = candidate["term"]
            children.sort(key=lambda x: x.fdr)

            theme = HierarchicalTheme(
                anchor_term=anchor_term,
                specific_terms=children,
                anchor_confidence=_determine_confidence(anchor_term.fdr),
            )
            themes.append(theme)

            # Mark anchor and children as assigned
            assigned.add(anchor_id)
            for child in children:
                assigned.add(child.go_id)

    # Find leaves for unassigned terms
    leaves = find_leaves(terms, godag, fdr_threshold)
    leaves = merge_identical_gene_sets(leaves, terms)

    # Add unassigned leaves as standalone themes
    for leaf_id in leaves:
        if leaf_id not in assigned and leaf_id in terms:
            leaf_term = terms[leaf_id]

            theme = HierarchicalTheme(
                anchor_term=leaf_term,
                specific_terms=[],
                anchor_confidence=_determine_confidence(leaf_term.fdr),
            )
            themes.append(theme)

    # Sort by anchor FDR
    themes.sort(key=lambda x: x.anchor_term.fdr)

    return themes


def themes_to_dict(themes: list[HierarchicalTheme]) -> list[dict]:
    """
    Convert themes to JSON-serializable dictionaries.

    Args:
        themes: List of HierarchicalTheme objects

    Returns:
        List of dictionaries suitable for JSON serialization
    """
    result = []
    for theme in themes:
        anchor = theme.anchor_term
        theme_dict = {
            "anchor_term": {
                "go_id": anchor.go_id,
                "name": anchor.name,
                "namespace": anchor.namespace,
                "fdr": anchor.fdr,
                "fold_enrichment": anchor.fold_enrichment,
                "genes": sorted(anchor.genes),
                "depth": anchor.depth,
            },
            "anchor_confidence": theme.anchor_confidence,
            "specific_terms": [
                {
                    "go_id": s.go_id,
                    "name": s.name,
                    "namespace": s.namespace,
                    "fdr": s.fdr,
                    "fold_enrichment": s.fold_enrichment,
                    "genes": sorted(s.genes),
                    "depth": s.depth,
                }
                for s in theme.specific_terms
            ],
            "n_specific_terms": len(theme.specific_terms),
            "all_genes": sorted(theme.all_genes),
        }
        result.append(theme_dict)

    return result


# =============================================================================
# Hub Gene Analysis
# =============================================================================


def compute_hub_genes(themes: list[dict], min_themes: int = 3) -> dict:
    """
    Find genes appearing in multiple themes.

    Hub genes are those that participate in multiple biological themes,
    suggesting they may be key regulators or connectors.

    Args:
        themes: List of theme dictionaries (from themes_to_dict)
        min_themes: Minimum number of themes to qualify as hub

    Returns:
        Dictionary mapping gene symbol to hub information:
        {gene: {'theme_count': N, 'themes': [theme_names], 'go_terms': [go_ids]}}
    """
    gene_themes: dict[str, dict] = defaultdict(lambda: {"themes": [], "go_terms": set()})

    for theme in themes:
        anchor = theme["anchor_term"]
        anchor_genes = set(anchor["genes"])

        # Include specific term genes
        all_genes = anchor_genes.copy()
        for specific in theme.get("specific_terms", []):
            all_genes.update(specific["genes"])

        theme_name = anchor["name"]
        theme_go_ids = {anchor["go_id"]}
        for specific in theme.get("specific_terms", []):
            theme_go_ids.add(specific["go_id"])

        for gene in all_genes:
            gene_themes[gene]["themes"].append(theme_name)
            gene_themes[gene]["go_terms"].update(theme_go_ids)

    # Filter to hub genes
    hub_genes = {}
    for gene, data in gene_themes.items():
        if len(data["themes"]) >= min_themes:
            hub_genes[gene] = {
                "theme_count": len(data["themes"]),
                "themes": data["themes"][:10],  # Top 10
                "go_terms": list(data["go_terms"]),
            }

    # Sort by theme count
    return dict(sorted(hub_genes.items(), key=lambda x: x[1]["theme_count"], reverse=True))


