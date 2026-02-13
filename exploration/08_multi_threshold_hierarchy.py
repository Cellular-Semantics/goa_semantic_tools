#!/usr/bin/env python3
"""
Prototype: Multi-threshold hierarchical theme building (Option B).

Uses multiple FDR thresholds to capture intermediate hierarchy levels:
- 0.01, 0.03, 0.05, 0.07, 0.10

At each threshold, find leaves. Terms that are leaves at a stricter threshold
but not at a looser one have children at that intermediate level.

This creates a multi-level tree structure based on statistical significance.
"""

import json
import subprocess
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
    depth: int = 0

    def __hash__(self):
        return hash(self.go_id)

    def __eq__(self, other):
        return self.go_id == other.go_id


@dataclass
class HierarchicalTheme:
    """A hierarchical theme with anchor and nested specifics."""
    anchor_term: EnrichedTerm
    specific_terms: list[EnrichedTerm]
    anchor_confidence: str  # threshold level label

    @property
    def all_genes(self) -> set:
        genes = set(self.anchor_term.genes)
        for specific in self.specific_terms:
            genes.update(specific.genes)
        return genes


def get_all_descendants(go_id: str, godag: GODag) -> set[str]:
    """Get all descendants using is_a and part_of relationships."""
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

    # Also check part_of reverse relationships
    for term_id, dag_term in godag.items():
        if hasattr(dag_term, 'relationship') and dag_term.relationship:
            for rel_type, rel_terms in dag_term.relationship.items():
                if rel_type == 'part_of':
                    for rel_term in rel_terms:
                        if rel_term.id == go_id and term_id not in descendants:
                            descendants.add(term_id)

    return descendants


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
    """Find enrichment leaves at a specific FDR threshold."""
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


def merge_identical_gene_sets(term_ids: set[str], terms: dict[str, EnrichedTerm]) -> set[str]:
    """Merge terms with identical gene sets, keeping lowest FDR."""
    gene_set_to_terms = defaultdict(list)
    for go_id in term_ids:
        if go_id in terms:
            gene_key = terms[go_id].genes
            gene_set_to_terms[gene_key].append(go_id)

    merged = set()
    for gene_set, group in gene_set_to_terms.items():
        if len(group) == 1:
            merged.add(group[0])
        else:
            best = min(group, key=lambda x: (terms[x].fdr, -terms[x].fold_enrichment))
            merged.add(best)

    return merged


def build_multi_threshold_themes(
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    thresholds: list[float] = [0.01, 0.03, 0.05, 0.07, 0.10],
    max_genes: int = 30
) -> list[HierarchicalTheme]:
    """
    Build hierarchical themes using multiple FDR thresholds.

    At each threshold boundary, terms that become non-leaves
    (gain children) become anchors for those children.
    """
    print(f"Total enriched terms: {len(terms)}")

    # Filter overly general terms
    terms = {k: v for k, v in terms.items() if len(v.genes) <= max_genes}
    print(f"After filtering >{max_genes} genes: {len(terms)}")

    # Find leaves at each threshold
    threshold_leaves = {}
    for t in thresholds:
        leaves = find_leaves_at_threshold(terms, godag, t)
        leaves = merge_identical_gene_sets(leaves, terms)
        threshold_leaves[t] = leaves
        print(f"Leaves at FDR<{t}: {len(leaves)}")

    # Build hierarchy by comparing adjacent thresholds
    # Terms that are leaves at threshold[i] but not at threshold[i+1]
    # have children that appear between those thresholds

    themes = []
    assigned = set()  # Track assigned terms to avoid duplicates

    # Process thresholds from strictest to loosest
    for i, strict_t in enumerate(thresholds[:-1]):
        loose_t = thresholds[i + 1]

        # Anchors: leaves at strict threshold but NOT leaves at loose threshold
        anchors = threshold_leaves[strict_t] - threshold_leaves[loose_t]

        print(f"\nThreshold {strict_t} → {loose_t}:")
        print(f"  Potential anchors: {len(anchors)}")

        for anchor_id in anchors:
            if anchor_id in assigned:
                continue

            anchor_term = terms.get(anchor_id)
            if not anchor_term:
                continue

            # Find children: terms that are leaves at loose threshold,
            # are descendants of anchor, and pass loose but not strict
            descendants = get_all_descendants(anchor_id, godag)

            children = []
            for child_id in threshold_leaves[loose_t]:
                if child_id in assigned:
                    continue
                if child_id not in descendants:
                    continue
                if child_id not in terms:
                    continue
                child_term = terms[child_id]
                # Child should pass loose threshold but not strict
                if child_term.fdr >= strict_t and child_term.fdr < loose_t:
                    children.append(child_term)
                    assigned.add(child_id)

            if children:
                children.sort(key=lambda x: x.fdr)
                theme = HierarchicalTheme(
                    anchor_term=anchor_term,
                    specific_terms=children,
                    anchor_confidence=f"FDR<{strict_t}"
                )
                themes.append(theme)
                assigned.add(anchor_id)
                print(f"  Anchor: {anchor_term.name[:40]} with {len(children)} children")

    # Add standalone leaves from loosest threshold
    loosest = thresholds[-1]
    for leaf_id in threshold_leaves[loosest]:
        if leaf_id not in assigned and leaf_id in terms:
            leaf_term = terms[leaf_id]
            # Determine confidence level
            for t in thresholds:
                if leaf_term.fdr < t:
                    conf = f"FDR<{t}"
                    break
            else:
                conf = f"FDR<{loosest}"

            theme = HierarchicalTheme(
                anchor_term=leaf_term,
                specific_terms=[],
                anchor_confidence=conf
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
    print("MULTI-THRESHOLD HIERARCHICAL THEMES")
    print("=" * 80 + "\n")

    n_with_children = sum(1 for t in themes if t.specific_terms)
    n_standalone = sum(1 for t in themes if not t.specific_terms)

    print(f"Themes with children: {n_with_children}")
    print(f"Standalone themes: {n_standalone}")
    print()

    for i, theme in enumerate(themes[:30], 1):  # Show first 30
        anchor = theme.anchor_term
        conf = theme.anchor_confidence

        if theme.specific_terms:
            print(f"{i}. [{conf}] {anchor.name} ({len(anchor.genes)} genes)")
            for specific in theme.specific_terms:
                print(f"   └─ {specific.name} ({len(specific.genes)} genes, FDR {specific.fdr:.2e})")
        else:
            print(f"{i}. [{conf}] {anchor.name} ({len(anchor.genes)} genes)")
        print()


def run_enrichment(gene_file: Path, output_dir: Path, fdr: float = 0.10) -> Path:
    """Run GO enrichment via CLI."""
    output_base = output_dir / f"{gene_file.stem}_fdr{int(fdr*100)}"
    output_file = output_dir / f"{gene_file.stem}_fdr{int(fdr*100)}_enrichment.json"

    if output_file.exists():
        print(f"Using existing enrichment: {output_file}")
        return output_file

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

    parser = argparse.ArgumentParser(description="Multi-threshold hierarchical theme building")
    parser.add_argument("--genes-file", type=Path,
                        default=Path("input_data/benchmark_sets/test_lists/hallmark_inflammatory_response.txt"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/benchmark"))
    parser.add_argument("--max-genes", type=int, default=30)
    args = parser.parse_args()

    args.output_dir.mkdir(exist_ok=True)

    # Load GO DAG
    print("Loading GO ontology...")
    godag = GODag(
        "reference_data/go-basic.obo",
        optional_attrs={"relationship"},
        prt=None
    )

    # Run enrichment at loosest threshold
    enrichment_file = run_enrichment(args.genes_file, args.output_dir, fdr=0.10)

    if not enrichment_file or not enrichment_file.exists():
        print("Enrichment failed")
        exit(1)

    with open(enrichment_file) as f:
        enrichment_data = json.load(f)

    print(f"Input genes: {enrichment_data['metadata']['input_genes_count']}")

    # Extract BP terms
    bp_terms = load_enriched_terms(enrichment_data, namespace="biological_process")
    print(f"Found {len(bp_terms)} BP terms")

    # Build themes
    thresholds = [0.01, 0.03, 0.05, 0.07, 0.10]
    themes = build_multi_threshold_themes(
        bp_terms,
        godag,
        thresholds=thresholds,
        max_genes=args.max_genes
    )

    # Print results
    print_themes(themes)

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total themes: {len(themes)}")
    print(f"  With nested children: {sum(1 for t in themes if t.specific_terms)}")
    print(f"  Standalone: {sum(1 for t in themes if not t.specific_terms)}")

    # Count by confidence level
    conf_counts = defaultdict(int)
    for t in themes:
        conf_counts[t.anchor_confidence] += 1
    for conf, count in sorted(conf_counts.items()):
        print(f"  {conf}: {count}")

    total_children = sum(len(t.specific_terms) for t in themes)
    print(f"  Total nested specific terms: {total_children}")

    # Save
    output_file = args.output_dir / f"{args.genes_file.stem}_multi_threshold.json"
    with open(output_file, "w") as f:
        json.dump({
            "metadata": {
                "algorithm": "multi-threshold hierarchical",
                "input_file": str(args.genes_file),
                "thresholds": thresholds,
                "max_genes": args.max_genes,
                "n_themes": len(themes),
                "n_with_children": sum(1 for t in themes if t.specific_terms)
            },
            "themes": themes_to_dict(themes)
        }, f, indent=2)

    print(f"\nThemes saved to: {output_file}")
