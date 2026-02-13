#!/usr/bin/env python3
"""
Prototype: Two-pass hierarchical theme building for GO enrichment.

Improvements over leaf-first (05_leaf_first_clustering.py):
1. Two-pass leaf finding at FDR 0.05 and 0.10 to capture more hierarchy
2. Uses is_a + part_of relationships (not just is_a)
3. Groups specific terms under shared parent anchors
4. Parent-centric output structure for better summarization

Algorithm:
1. Run ORA at FDR 0.10 → get all enriched terms
2. Partition: high confidence (FDR<0.05) vs moderate (0.05-0.10)
3. Find leaves at EACH threshold:
   - Leaves_0.05 = high-confidence terms with no high-confidence descendants
   - Leaves_0.10 = all terms with no enriched descendants
4. Terms in Leaves_0.05 but NOT in Leaves_0.10 have moderate children → anchors
5. Build hierarchy grouping children under anchors
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from goatools.obo_parser import GODag


@dataclass
class EnrichedTerm:
    """Represents an enriched GO term."""
    go_id: str
    name: str
    namespace: str
    fdr: float
    fold_enrichment: float
    genes: frozenset = field(default_factory=frozenset)

    def __hash__(self):
        return hash(self.go_id)

    def __eq__(self, other):
        return self.go_id == other.go_id


@dataclass
class HierarchicalTheme:
    """A hierarchical theme with anchor and nested specifics."""
    anchor_term: EnrichedTerm           # Parent/broader term (or standalone leaf)
    specific_terms: list[EnrichedTerm]  # Children grouped under anchor
    anchor_confidence: str              # "high" or "moderate" based on anchor's FDR

    @property
    def all_genes(self) -> set:
        genes = set(self.anchor_term.genes)
        for specific in self.specific_terms:
            genes.update(specific.genes)
        return genes


def get_all_descendants_with_relationships(go_id: str, godag: GODag) -> set[str]:
    """
    Get all descendants using is_a AND part_of relationships.

    Args:
        go_id: GO term ID
        godag: GO DAG with relationships loaded

    Returns:
        Set of all descendant GO IDs
    """
    if go_id not in godag:
        return set()

    term = godag[go_id]
    descendants = set()
    to_visit = list(term.children)  # is_a children

    # Also add part_of children (terms where this term is in their part_of)
    # In GO, if B part_of A, then B is a "child" of A in the broader sense
    # goatools stores relationships as term.relationship where key is rel type

    while to_visit:
        child = to_visit.pop()
        if child.id not in descendants:
            descendants.add(child.id)
            to_visit.extend(child.children)

    # For part_of, we need to find terms that have this term in their part_of
    # This requires scanning - goatools doesn't index reverse relationships well
    # For now, we'll use the relationship dict if available
    for term_id, dag_term in godag.items():
        if hasattr(dag_term, 'relationship'):
            for rel_type, rel_terms in dag_term.relationship.items():
                if rel_type == 'part_of':
                    for rel_term in rel_terms:
                        if rel_term.id == go_id and term_id not in descendants:
                            descendants.add(term_id)
                            # Recursively get descendants of this term too
                            descendants.update(get_all_descendants_with_relationships(term_id, godag))

    return descendants


def get_all_ancestors_with_relationships(go_id: str, godag: GODag) -> set[str]:
    """
    Get all ancestors using is_a AND part_of relationships.

    Args:
        go_id: GO term ID
        godag: GO DAG with relationships loaded

    Returns:
        Set of all ancestor GO IDs
    """
    if go_id not in godag:
        return set()

    term = godag[go_id]
    ancestors = set()

    # is_a parents
    to_visit = list(term.parents)

    # part_of parents
    if hasattr(term, 'relationship') and 'part_of' in term.relationship:
        to_visit.extend(term.relationship['part_of'])

    while to_visit:
        parent = to_visit.pop()
        if parent.id not in ancestors:
            ancestors.add(parent.id)
            to_visit.extend(parent.parents)
            if hasattr(parent, 'relationship') and 'part_of' in parent.relationship:
                to_visit.extend(parent.relationship['part_of'])

    return ancestors


def load_enriched_terms(enrichment_json: dict, namespace: str = "biological_process") -> dict[str, EnrichedTerm]:
    """Extract enriched terms from enrichment output."""
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
                genes=frozenset(root["study_genes"])
            )

        for member in cluster.get("member_terms", []):
            if member["namespace"] == namespace and member["go_id"] not in terms:
                terms[member["go_id"]] = EnrichedTerm(
                    go_id=member["go_id"],
                    name=member["name"],
                    namespace=member["namespace"],
                    fdr=member["fdr"],
                    fold_enrichment=member["fold_enrichment"],
                    genes=frozenset(member["study_genes"])
                )

    return terms


def find_leaves_at_threshold(
    all_terms: dict[str, EnrichedTerm],
    godag: GODag,
    fdr_threshold: float
) -> set[str]:
    """
    Find enrichment leaves at a specific FDR threshold.

    A leaf is a term passing the threshold with no descendants also passing.
    Uses is_a + part_of relationships.

    Args:
        all_terms: All enriched terms
        godag: GO DAG
        fdr_threshold: FDR cutoff

    Returns:
        Set of GO IDs that are leaves at this threshold
    """
    # Terms passing this threshold
    passing_ids = {go_id for go_id, term in all_terms.items() if term.fdr < fdr_threshold}

    leaves = set()
    for go_id in passing_ids:
        if go_id not in godag:
            continue

        # Get descendants using is_a + part_of
        descendants = get_all_descendants_with_relationships(go_id, godag)

        # Check if any descendants also pass the threshold
        enriched_descendants = passing_ids & descendants

        if len(enriched_descendants) == 0:
            leaves.add(go_id)

    return leaves


def merge_identical_gene_sets(
    term_ids: set[str],
    terms: dict[str, EnrichedTerm]
) -> set[str]:
    """
    Merge terms with identical gene sets, keeping lowest FDR.

    Returns:
        Set of GO IDs after merging
    """
    gene_set_to_terms = defaultdict(list)
    for go_id in term_ids:
        if go_id in terms:
            gene_key = terms[go_id].genes  # Already frozenset
            gene_set_to_terms[gene_key].append(go_id)

    merged = set()
    for gene_set, group in gene_set_to_terms.items():
        if len(group) == 1:
            merged.add(group[0])
        else:
            # Keep term with lowest FDR
            best = min(group, key=lambda x: (terms[x].fdr, -terms[x].fold_enrichment))
            merged.add(best)

    return merged


def build_hierarchical_themes(
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    fdr_high: float = 0.05,
    fdr_moderate: float = 0.10,
    max_genes: int = 50
) -> list[HierarchicalTheme]:
    """
    Build hierarchical themes using two-pass leaf finding.

    Args:
        terms: All enriched terms (at FDR < fdr_moderate)
        godag: GO DAG with relationships
        fdr_high: Threshold for high confidence
        fdr_moderate: Threshold for moderate confidence
        max_genes: Filter out terms with more genes (too general)

    Returns:
        List of HierarchicalThemes
    """
    print(f"Total enriched terms: {len(terms)}")

    # Filter overly general terms
    terms = {k: v for k, v in terms.items() if len(v.genes) <= max_genes}
    print(f"After filtering >50 genes: {len(terms)}")

    # Step 1: Find leaves at both thresholds
    leaves_high = find_leaves_at_threshold(terms, godag, fdr_high)
    leaves_moderate = find_leaves_at_threshold(terms, godag, fdr_moderate)

    print(f"Leaves at FDR<{fdr_high}: {len(leaves_high)}")
    print(f"Leaves at FDR<{fdr_moderate}: {len(leaves_moderate)}")

    # Step 2: Merge identical gene sets within each leaf set
    leaves_high = merge_identical_gene_sets(leaves_high, terms)
    leaves_moderate = merge_identical_gene_sets(leaves_moderate, terms)

    print(f"After merging identical gene sets:")
    print(f"  High confidence leaves: {len(leaves_high)}")
    print(f"  All leaves (moderate): {len(leaves_moderate)}")

    # Step 3: Identify anchor terms
    # Terms that are leaves at 0.05 but NOT at 0.10 → they have moderate children
    potential_anchors = leaves_high - leaves_moderate
    print(f"Potential anchors (high leaves with moderate children): {len(potential_anchors)}")

    # Step 4: For each potential anchor, find its moderate-confidence descendants
    anchor_to_children: dict[str, list[str]] = defaultdict(list)
    assigned_leaves = set()

    for anchor_id in potential_anchors:
        descendants = get_all_descendants_with_relationships(anchor_id, godag)
        # Find moderate leaves that are descendants of this anchor
        moderate_only = leaves_moderate - leaves_high
        child_leaves = descendants & moderate_only

        if child_leaves:
            anchor_to_children[anchor_id] = list(child_leaves)
            assigned_leaves.update(child_leaves)

    # Step 5: Remaining leaves become standalone themes
    # High-confidence true leaves: in both leaf sets, not used as anchors
    standalone_high = (leaves_high & leaves_moderate) - potential_anchors

    # Moderate-only leaves: only pass moderate threshold, not assigned to anchor
    standalone_moderate = (leaves_moderate - leaves_high) - assigned_leaves

    print(f"Anchors with children: {len(anchor_to_children)}")
    print(f"Standalone high-confidence: {len(standalone_high)}")
    print(f"Standalone moderate: {len(standalone_moderate)}")

    # Step 6: Build themes
    themes = []

    # Anchors with children
    for anchor_id, child_ids in anchor_to_children.items():
        anchor_term = terms[anchor_id]
        specific_terms = [terms[c] for c in child_ids if c in terms]
        # Sort children by FDR
        specific_terms.sort(key=lambda x: x.fdr)

        theme = HierarchicalTheme(
            anchor_term=anchor_term,
            specific_terms=specific_terms,
            anchor_confidence="high" if anchor_term.fdr < fdr_high else "moderate"
        )
        themes.append(theme)

    # Standalone high-confidence leaves
    for leaf_id in standalone_high:
        if leaf_id in terms:
            theme = HierarchicalTheme(
                anchor_term=terms[leaf_id],
                specific_terms=[],
                anchor_confidence="high"
            )
            themes.append(theme)

    # Standalone moderate leaves
    for leaf_id in standalone_moderate:
        if leaf_id in terms:
            theme = HierarchicalTheme(
                anchor_term=terms[leaf_id],
                specific_terms=[],
                anchor_confidence="moderate"
            )
            themes.append(theme)

    # Sort by anchor FDR
    themes.sort(key=lambda x: x.anchor_term.fdr)

    return themes


def themes_to_dict(themes: list[HierarchicalTheme]) -> list[dict]:
    """Convert themes to JSON-serializable dict."""
    result = []
    for theme in themes:
        anchor = theme.anchor_term
        theme_dict = {
            "anchor_term": {
                "go_id": anchor.go_id,
                "name": anchor.name,
                "fdr": anchor.fdr,
                "fold_enrichment": anchor.fold_enrichment,
                "genes": sorted(anchor.genes)
            },
            "anchor_confidence": theme.anchor_confidence,
            "specific_terms": [
                {
                    "go_id": s.go_id,
                    "name": s.name,
                    "fdr": s.fdr,
                    "fold_enrichment": s.fold_enrichment,
                    "genes": sorted(s.genes)
                }
                for s in theme.specific_terms
            ],
            "n_specific_terms": len(theme.specific_terms)
        }
        result.append(theme_dict)

    return result


def print_themes(themes: list[HierarchicalTheme]) -> None:
    """Pretty print hierarchical themes."""
    print("\n" + "=" * 80)
    print("HIERARCHICAL THEMES (Two-Pass Algorithm)")
    print("=" * 80 + "\n")

    n_with_children = sum(1 for t in themes if t.specific_terms)
    n_standalone = sum(1 for t in themes if not t.specific_terms)

    print(f"Themes with children: {n_with_children}")
    print(f"Standalone themes: {n_standalone}")
    print()

    for i, theme in enumerate(themes, 1):
        anchor = theme.anchor_term
        conf = "🔴" if theme.anchor_confidence == "high" else "🟡"

        if theme.specific_terms:
            print(f"{i}. {conf} {anchor.name} ({len(anchor.genes)} genes)")
            print(f"   GO: {anchor.go_id}, FDR: {anchor.fdr:.2e}")
            for j, specific in enumerate(theme.specific_terms, 1):
                s_conf = "🔴" if specific.fdr < 0.05 else "🟡"
                print(f"   └─ {s_conf} {specific.name} ({len(specific.genes)} genes)")
                print(f"      GO: {specific.go_id}, FDR: {specific.fdr:.2e}")
        else:
            print(f"{i}. {conf} {anchor.name} ({len(anchor.genes)} genes)")
            print(f"   GO: {anchor.go_id}, FDR: {anchor.fdr:.2e}")
        print()


# ============================================================================
# Main
# ============================================================================

def run_enrichment(gene_file: Path, output_dir: Path, fdr: float = 0.10) -> Path:
    """Run GO enrichment via CLI and return output path."""
    import subprocess

    output_base = output_dir / f"{gene_file.stem}_fdr{int(fdr*100)}"
    output_file = output_dir / f"{gene_file.stem}_fdr{int(fdr*100)}_enrichment.json"

    cmd = [
        "uv", "run", "go-enrichment",
        "--genes-file", str(gene_file),
        "--fdr", str(fdr),
        "--output", str(output_base),
    ]

    print(f"Running enrichment at FDR {fdr}...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)

    if result.returncode != 0:
        print(f"Enrichment failed: {result.stderr[:500]}")
        return None

    return output_file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Two-pass hierarchical theme building")
    parser.add_argument("--genes-file", type=Path,
                        default=Path("input_data/benchmark_sets/test_lists/hallmark_inflammatory_response.txt"),
                        help="Input gene list file")
    parser.add_argument("--output-dir", type=Path, default=Path("results/benchmark"),
                        help="Output directory")
    parser.add_argument("--fdr-high", type=float, default=0.05, help="High confidence FDR threshold")
    parser.add_argument("--fdr-moderate", type=float, default=0.10, help="Moderate confidence FDR threshold")
    parser.add_argument("--max-genes", type=int, default=50, help="Max genes per term")
    args = parser.parse_args()

    args.output_dir.mkdir(exist_ok=True)

    # Load GO DAG with relationships
    print("Loading GO ontology with relationships...")
    godag = GODag(
        "reference_data/go-basic.obo",
        optional_attrs={"relationship"},
        prt=None
    )
    print(f"Loaded {len(godag)} GO terms")

    # Check relationship coverage
    n_with_rels = sum(1 for t in godag.values() if hasattr(t, 'relationship') and t.relationship)
    print(f"Terms with relationships: {n_with_rels}")

    # Run enrichment at FDR 0.10 to get all terms
    enrichment_file = run_enrichment(args.genes_file, args.output_dir, fdr=args.fdr_moderate)

    if not enrichment_file or not enrichment_file.exists():
        print("Enrichment failed")
        exit(1)

    with open(enrichment_file) as f:
        enrichment_data = json.load(f)

    print(f"Input genes: {enrichment_data['metadata']['input_genes_count']}")

    # Extract BP terms
    print("\nExtracting biological process terms...")
    bp_terms = load_enriched_terms(enrichment_data, namespace="biological_process")
    print(f"Found {len(bp_terms)} BP terms")

    # Build hierarchical themes
    print("\nBuilding hierarchical themes...")
    themes = build_hierarchical_themes(
        bp_terms,
        godag,
        fdr_high=args.fdr_high,
        fdr_moderate=args.fdr_moderate,
        max_genes=args.max_genes
    )

    # Print results
    print_themes(themes)

    # Summary stats
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total themes: {len(themes)}")
    print(f"  With nested children: {sum(1 for t in themes if t.specific_terms)}")
    print(f"  Standalone: {sum(1 for t in themes if not t.specific_terms)}")
    print(f"  High confidence: {sum(1 for t in themes if t.anchor_confidence == 'high')}")
    print(f"  Moderate confidence: {sum(1 for t in themes if t.anchor_confidence == 'moderate')}")

    total_children = sum(len(t.specific_terms) for t in themes)
    print(f"  Total nested specific terms: {total_children}")

    # Save to JSON
    output_file = args.output_dir / f"{args.genes_file.stem}_hierarchical.json"
    with open(output_file, "w") as f:
        json.dump({
            "metadata": {
                "algorithm": "two-pass hierarchical",
                "input_file": str(args.genes_file),
                "fdr_high": args.fdr_high,
                "fdr_moderate": args.fdr_moderate,
                "max_genes": args.max_genes,
                "uses_part_of": True,
                "n_themes": len(themes),
                "n_with_children": sum(1 for t in themes if t.specific_terms),
                "n_standalone": sum(1 for t in themes if not t.specific_terms)
            },
            "themes": themes_to_dict(themes)
        }, f, indent=2)

    print(f"\nThemes saved to: {output_file}")