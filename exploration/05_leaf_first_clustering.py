#!/usr/bin/env python3
"""
Prototype: Leaf-first clustering algorithm for GO enrichment.

Instead of top-N roots (which picks general terms), this approach:
1. Finds "enrichment leaves" - enriched terms with no enriched descendants
2. Merges leaves with identical gene sets
3. Checks if parent terms add significant new genes (>20%)
4. Builds hierarchical themes from bottom-up

This reduces redundancy and produces more interpretable biological themes.
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from goatools.obo_parser import GODag


@dataclass
class EnrichedTerm:
    """Represents an enriched GO term."""
    go_id: str
    name: str
    namespace: str
    fdr: float
    fold_enrichment: float
    genes: set = field(default_factory=set)

    def __hash__(self):
        return hash(self.go_id)


@dataclass
class BiologicalTheme:
    """A biological theme built from enrichment leaves."""
    primary_term: EnrichedTerm  # Most specific (leaf)
    broader_term: EnrichedTerm | None = None  # Parent if adds significant genes
    unique_genes_at_parent: set = field(default_factory=set)
    confidence: str = "high"  # "high" (FDR<0.05) or "moderate" (0.05-0.10)

    @property
    def all_genes(self) -> set:
        genes = self.primary_term.genes.copy()
        if self.broader_term:
            genes.update(self.broader_term.genes)
        return genes

    @property
    def core_genes(self) -> set:
        return self.primary_term.genes


def load_enriched_terms(enrichment_json: dict, namespace: str = "biological_process") -> dict[str, EnrichedTerm]:
    """
    Extract enriched terms from enrichment output.

    Args:
        enrichment_json: Output from run_go_enrichment
        namespace: Filter to specific namespace (default: biological_process)

    Returns:
        Dict mapping GO ID to EnrichedTerm
    """
    terms = {}

    for cluster in enrichment_json["clusters"]:
        root = cluster["root_term"]
        if root["namespace"] == namespace:
            terms[root["go_id"]] = EnrichedTerm(
                go_id=root["go_id"],
                name=root["name"],
                namespace=root["namespace"],
                fdr=root["fdr"],
                fold_enrichment=root["fold_enrichment"],
                genes=set(root["study_genes"])
            )

        for member in cluster.get("member_terms", []):
            if member["namespace"] == namespace and member["go_id"] not in terms:
                terms[member["go_id"]] = EnrichedTerm(
                    go_id=member["go_id"],
                    name=member["name"],
                    namespace=member["namespace"],
                    fdr=member["fdr"],
                    fold_enrichment=member["fold_enrichment"],
                    genes=set(member["study_genes"])
                )

    return terms


def find_enrichment_leaves(
    terms: dict[str, EnrichedTerm],
    godag: GODag
) -> list[EnrichedTerm]:
    """
    Find enrichment leaves - enriched terms with no enriched descendants.

    Args:
        terms: Dict of enriched terms
        godag: GO DAG for hierarchy navigation

    Returns:
        List of leaf EnrichedTerms
    """
    enriched_ids = set(terms.keys())
    leaves = []

    for go_id, term in terms.items():
        if go_id not in godag:
            continue

        # Get all descendants of this term
        all_children = godag[go_id].get_all_children()

        # Check if any descendants are also enriched
        enriched_descendants = enriched_ids & all_children

        if len(enriched_descendants) == 0:
            leaves.append(term)

    return leaves


def merge_identical_leaves(leaves: list[EnrichedTerm]) -> list[EnrichedTerm]:
    """
    Merge leaves with identical gene sets, keeping the more specific term.

    Args:
        leaves: List of enrichment leaves

    Returns:
        Deduplicated list of leaves
    """
    # Group by gene set
    gene_set_to_leaves = defaultdict(list)
    for leaf in leaves:
        gene_key = frozenset(leaf.genes)
        gene_set_to_leaves[gene_key].append(leaf)

    # For each group, pick the leaf with lowest FDR (or highest fold enrichment as tiebreaker)
    merged = []
    for gene_set, group in gene_set_to_leaves.items():
        if len(group) == 1:
            merged.append(group[0])
        else:
            # Pick best representative
            best = min(group, key=lambda x: (x.fdr, -x.fold_enrichment))
            merged.append(best)

    return merged


def find_parent_contribution(
    leaf: EnrichedTerm,
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    min_gene_addition_pct: float = 0.20,
    max_gene_addition_pct: float = 2.0,
    max_parent_genes: int = 50
) -> tuple[EnrichedTerm | None, set]:
    """
    Check if any enriched parent adds significant new genes.

    Args:
        leaf: The enrichment leaf term
        terms: All enriched terms
        godag: GO DAG
        min_gene_addition_pct: Minimum % of new genes for parent to be included
        max_gene_addition_pct: Maximum % - skip if parent adds too many (too general)
        max_parent_genes: Skip parents with more genes than this (too general)

    Returns:
        Tuple of (parent term or None, unique genes at parent level)
    """
    if leaf.go_id not in godag:
        return None, set()

    # Get all ancestors
    all_parents = godag[leaf.go_id].get_all_parents()
    enriched_ancestors = [terms[p] for p in all_parents if p in terms]

    if not enriched_ancestors:
        return None, set()

    # Sort ancestors by depth (most specific first), then by FDR
    # We want the closest parent that adds meaningful genes, not the most significant
    def sort_key(parent):
        if parent.go_id in godag:
            depth = godag[parent.go_id].depth
        else:
            depth = 0
        return (-depth, parent.fdr)  # Higher depth first, then lower FDR

    enriched_ancestors.sort(key=sort_key)

    # Find the closest ancestor that adds meaningful (but not too many) genes
    for parent in enriched_ancestors:
        # Skip overly general parents
        if len(parent.genes) > max_parent_genes:
            continue

        unique_genes = parent.genes - leaf.genes
        addition_pct = len(unique_genes) / len(leaf.genes) if leaf.genes else 0

        # Must add enough genes, but not too many
        if min_gene_addition_pct <= addition_pct <= max_gene_addition_pct:
            return parent, unique_genes

    return None, set()


def build_biological_themes(
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    fdr_high_confidence: float = 0.05,
    min_gene_addition_pct: float = 0.20,
    max_gene_addition_pct: float = 2.0,
    max_genes_for_specific: int = 50
) -> list[BiologicalTheme]:
    """
    Build biological themes using leaf-first approach.

    Args:
        terms: All enriched terms
        godag: GO DAG
        fdr_high_confidence: FDR threshold for high confidence
        min_gene_addition_pct: Minimum % new genes for parent inclusion
        max_gene_addition_pct: Maximum % - skip if parent too general
        max_genes_for_specific: Skip leaves with more genes (too general)

    Returns:
        List of BiologicalThemes
    """
    # Step 1: Find enrichment leaves
    leaves = find_enrichment_leaves(terms, godag)
    print(f"Found {len(leaves)} enrichment leaves")

    # Step 2: Merge identical gene sets
    leaves = merge_identical_leaves(leaves)
    print(f"After merging identical: {len(leaves)} leaves")

    # Step 3: Filter overly general terms
    leaves = [l for l in leaves if len(l.genes) <= max_genes_for_specific]
    print(f"After filtering general terms: {len(leaves)} leaves")

    # Step 4: Build themes with parent contribution check
    themes = []
    for leaf in leaves:
        parent, unique_genes = find_parent_contribution(
            leaf, terms, godag, min_gene_addition_pct,
            max_gene_addition_pct, max_genes_for_specific
        )

        confidence = "high" if leaf.fdr < fdr_high_confidence else "moderate"

        theme = BiologicalTheme(
            primary_term=leaf,
            broader_term=parent,
            unique_genes_at_parent=unique_genes,
            confidence=confidence
        )
        themes.append(theme)

    # Sort by FDR
    themes.sort(key=lambda x: x.primary_term.fdr)

    return themes


def print_themes(themes: list[BiologicalTheme]) -> None:
    """Pretty print biological themes."""
    print("\n" + "=" * 80)
    print("BIOLOGICAL THEMES (Leaf-First Clustering)")
    print("=" * 80 + "\n")

    for i, theme in enumerate(themes, 1):
        primary = theme.primary_term
        conf_marker = "⚠️ " if theme.confidence == "moderate" else ""

        print(f"{i}. {conf_marker}{primary.name}")
        print(f"   GO ID: {primary.go_id}")
        print(f"   FDR: {primary.fdr:.2e}, Fold: {primary.fold_enrichment:.1f}x")
        print(f"   Core genes ({len(primary.genes)}): {', '.join(sorted(primary.genes))}")

        if theme.broader_term:
            broader = theme.broader_term
            print(f"   ")
            print(f"   Broader context: {broader.name} ({broader.go_id})")
            print(f"   Additional genes ({len(theme.unique_genes_at_parent)}): {', '.join(sorted(theme.unique_genes_at_parent))}")

        print()

    print("=" * 80)
    print(f"Total themes: {len(themes)}")
    print(f"  High confidence (FDR<0.05): {sum(1 for t in themes if t.confidence == 'high')}")
    print(f"  Moderate confidence (FDR 0.05-0.10): {sum(1 for t in themes if t.confidence == 'moderate')}")
    print("=" * 80)


def themes_to_dict(themes: list[BiologicalTheme]) -> list[dict]:
    """Convert themes to JSON-serializable dict."""
    result = []
    for theme in themes:
        primary = theme.primary_term
        theme_dict = {
            "primary_term": {
                "go_id": primary.go_id,
                "name": primary.name,
                "fdr": primary.fdr,
                "fold_enrichment": primary.fold_enrichment,
                "genes": sorted(primary.genes)
            },
            "confidence": theme.confidence,
            "broader_term": None,
            "unique_genes_at_broader": []
        }

        if theme.broader_term:
            broader = theme.broader_term
            theme_dict["broader_term"] = {
                "go_id": broader.go_id,
                "name": broader.name,
                "fdr": broader.fdr,
                "fold_enrichment": broader.fold_enrichment,
                "genes": sorted(broader.genes)
            }
            theme_dict["unique_genes_at_broader"] = sorted(theme.unique_genes_at_parent)

        result.append(theme_dict)

    return result


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    # Load GO DAG
    print("Loading GO ontology...")
    godag = GODag(
        "reference_data/go-basic.obo",
        optional_attrs={"relationship"},
        prt=None
    )

    # Load enrichment results (FDR 0.10 for more terms)
    print("Loading enrichment results...")
    results_file = Path("results/fdr01_enrichment.json")
    with open(results_file) as f:
        enrichment_data = json.load(f)

    print(f"Input: {enrichment_data['metadata']['input_genes_count']} genes")
    print(f"Total enriched terms: {enrichment_data['metadata']['total_enriched_terms']}")

    # Extract BP terms
    print("\nExtracting biological process terms...")
    bp_terms = load_enriched_terms(enrichment_data, namespace="biological_process")
    print(f"Found {len(bp_terms)} BP terms")

    # Build themes
    print("\nBuilding biological themes...")
    themes = build_biological_themes(
        bp_terms,
        godag,
        fdr_high_confidence=0.05,
        min_gene_addition_pct=0.20,
        max_genes_for_specific=50
    )

    # Print results
    print_themes(themes)

    # Save to JSON
    output_file = Path("results/leaf_first_themes.json")
    with open(output_file, "w") as f:
        json.dump({
            "metadata": {
                "algorithm": "leaf-first clustering",
                "fdr_threshold": 0.10,
                "fdr_high_confidence": 0.05,
                "min_gene_addition_pct": 0.20,
                "max_genes_for_specific": 50,
                "namespace": "biological_process"
            },
            "themes": themes_to_dict(themes)
        }, f, indent=2)

    print(f"\nThemes saved to: {output_file}")
