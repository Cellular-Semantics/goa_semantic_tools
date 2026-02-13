#!/usr/bin/env python3
"""
Prototype: Depth-based non-leaf anchors (Option C).

Find intermediate-depth terms with ≥2 enriched children as anchors,
regardless of whether they are leaves themselves.

Parameters:
- depth_range: (4, 7) - GO depth range for anchor candidates
- min_children: 2 - minimum enriched descendants to qualify as anchor
- max_genes: 30 - filter overly general terms
- no_overlap: True - each term assigned to at most one anchor

Note: GO depth is imperfect (inconsistent across branches) but useful
for finding intermediate-level terms that can aid explanation.
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
    anchor_confidence: str

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

    # Check part_of reverse relationships
    for term_id, dag_term in godag.items():
        if hasattr(dag_term, 'relationship') and dag_term.relationship:
            for rel_type, rel_terms in dag_term.relationship.items():
                if rel_type == 'part_of':
                    for rel_term in rel_terms:
                        if rel_term.id == go_id and term_id not in descendants:
                            descendants.add(term_id)

    return descendants


def load_enriched_terms(
    enrichment_json: dict,
    godag: GODag,
    namespace: str = "biological_process"
) -> dict[str, EnrichedTerm]:
    """Extract enriched terms from enrichment output with depth info."""
    terms = {}

    for cluster in enrichment_json["clusters"]:
        root = cluster["root_term"]
        if root["namespace"] == namespace:
            go_id = root["go_id"]
            depth = godag[go_id].depth if go_id in godag else 0
            terms[go_id] = EnrichedTerm(
                go_id=go_id,
                name=root["name"],
                namespace=root["namespace"],
                fdr=root["fdr"],
                fold_enrichment=root["fold_enrichment"],
                genes=frozenset(root["study_genes"]),
                depth=depth
            )

        for member in cluster.get("member_terms", []):
            if member["namespace"] == namespace and member["go_id"] not in terms:
                go_id = member["go_id"]
                depth = godag[go_id].depth if go_id in godag else 0
                terms[go_id] = EnrichedTerm(
                    go_id=go_id,
                    name=member["name"],
                    namespace=member["namespace"],
                    fdr=member["fdr"],
                    fold_enrichment=member["fold_enrichment"],
                    genes=frozenset(member["study_genes"]),
                    depth=depth
                )

    return terms


def find_leaves(all_terms: dict[str, EnrichedTerm], godag: GODag, fdr_threshold: float) -> set[str]:
    """Find enrichment leaves at FDR threshold."""
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
    """Merge terms with identical gene sets."""
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


def build_depth_anchor_themes(
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    depth_range: tuple[int, int] = (4, 7),
    min_children: int = 2,
    max_genes: int = 30,
    fdr_threshold: float = 0.10
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
    """
    print(f"Total enriched terms: {len(terms)}")

    # Filter overly general terms
    terms = {k: v for k, v in terms.items() if len(v.genes) <= max_genes}
    print(f"After filtering >{max_genes} genes: {len(terms)}")

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
            anchor_candidates.append({
                'go_id': go_id,
                'term': term,
                'depth': term.depth,
                'n_enriched_children': len(enriched_descendants),
                'enriched_children': enriched_descendants
            })

    # Sort by depth (prefer more specific = higher depth) then by FDR
    anchor_candidates.sort(key=lambda x: (-x['depth'], x['term'].fdr))

    print(f"\nAnchor candidates (depth {depth_range[0]}-{depth_range[1]}, ≥{min_children} children):")
    print(f"  Found: {len(anchor_candidates)}")

    # Assign children to anchors (no overlap - each child assigned to first anchor)
    assigned = set()
    themes = []

    for candidate in anchor_candidates:
        anchor_id = candidate['go_id']

        if anchor_id in assigned:
            continue

        # Collect unassigned enriched descendants
        children = []
        for child_id in candidate['enriched_children']:
            if child_id in assigned:
                continue
            if child_id == anchor_id:
                continue
            if child_id in terms:
                children.append(terms[child_id])

        if len(children) >= min_children:
            anchor_term = candidate['term']
            children.sort(key=lambda x: x.fdr)

            # Determine anchor confidence
            if anchor_term.fdr < 0.01:
                conf = "FDR<0.01"
            elif anchor_term.fdr < 0.05:
                conf = "FDR<0.05"
            else:
                conf = "FDR<0.10"

            theme = HierarchicalTheme(
                anchor_term=anchor_term,
                specific_terms=children,
                anchor_confidence=conf
            )
            themes.append(theme)

            # Mark anchor and children as assigned
            assigned.add(anchor_id)
            for child in children:
                assigned.add(child.go_id)

            print(f"  Anchor: depth={candidate['depth']} | {len(children)} children | {anchor_term.name[:45]}")

    # Find leaves for unassigned terms
    leaves = find_leaves(terms, godag, fdr_threshold)
    leaves = merge_identical_gene_sets(leaves, terms)

    # Add unassigned leaves as standalone themes
    for leaf_id in leaves:
        if leaf_id not in assigned and leaf_id in terms:
            leaf_term = terms[leaf_id]

            if leaf_term.fdr < 0.01:
                conf = "FDR<0.01"
            elif leaf_term.fdr < 0.05:
                conf = "FDR<0.05"
            else:
                conf = "FDR<0.10"

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
                "genes": sorted(anchor.genes),
                "depth": anchor.depth
            },
            "anchor_confidence": theme.anchor_confidence,
            "specific_terms": [
                {
                    "go_id": s.go_id,
                    "name": s.name,
                    "fdr": s.fdr,
                    "fold_enrichment": s.fold_enrichment,
                    "genes": sorted(s.genes),
                    "depth": s.depth
                }
                for s in theme.specific_terms
            ],
            "n_specific_terms": len(theme.specific_terms)
        }
        result.append(theme_dict)

    return result


def print_themes(themes: list[HierarchicalTheme], max_show: int = 30) -> None:
    """Pretty print hierarchical themes."""
    print("\n" + "=" * 80)
    print("DEPTH-BASED ANCHOR THEMES")
    print("=" * 80 + "\n")

    n_with_children = sum(1 for t in themes if t.specific_terms)
    n_standalone = sum(1 for t in themes if not t.specific_terms)

    print(f"Themes with children: {n_with_children}")
    print(f"Standalone themes: {n_standalone}")
    print()

    shown = 0
    for i, theme in enumerate(themes, 1):
        if shown >= max_show:
            print(f"... and {len(themes) - shown} more themes")
            break

        anchor = theme.anchor_term
        conf = theme.anchor_confidence

        if theme.specific_terms:
            print(f"{i}. [{conf}] (d={anchor.depth}) {anchor.name} ({len(anchor.genes)} genes)")
            for specific in theme.specific_terms[:5]:  # Show max 5 children
                print(f"   └─ (d={specific.depth}) {specific.name} ({len(specific.genes)} genes)")
            if len(theme.specific_terms) > 5:
                print(f"   └─ ... and {len(theme.specific_terms) - 5} more")
            shown += 1
        else:
            print(f"{i}. [{conf}] (d={anchor.depth}) {anchor.name} ({len(anchor.genes)} genes)")
            shown += 1
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

    parser = argparse.ArgumentParser(description="Depth-based anchor theme building")
    parser.add_argument("--genes-file", type=Path,
                        default=Path("input_data/benchmark_sets/test_lists/hallmark_inflammatory_response.txt"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/benchmark"))
    parser.add_argument("--depth-min", type=int, default=4)
    parser.add_argument("--depth-max", type=int, default=7)
    parser.add_argument("--min-children", type=int, default=2)
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

    # Show depth distribution
    print("\nGO depth distribution (BP terms):")
    depth_counts = defaultdict(int)
    for term in godag.values():
        if term.namespace == 'biological_process':
            depth_counts[term.depth] += 1
    for d in sorted(depth_counts.keys())[:12]:
        print(f"  Depth {d:2d}: {depth_counts[d]:5d} terms")

    # Run enrichment
    enrichment_file = run_enrichment(args.genes_file, args.output_dir, fdr=0.10)

    if not enrichment_file or not enrichment_file.exists():
        print("Enrichment failed")
        exit(1)

    with open(enrichment_file) as f:
        enrichment_data = json.load(f)

    print(f"\nInput genes: {enrichment_data['metadata']['input_genes_count']}")

    # Extract BP terms with depth
    bp_terms = load_enriched_terms(enrichment_data, godag, namespace="biological_process")
    print(f"Found {len(bp_terms)} BP terms")

    # Show enriched term depth distribution
    print("\nEnriched BP terms by depth:")
    enriched_depth = defaultdict(int)
    for t in bp_terms.values():
        enriched_depth[t.depth] += 1
    for d in sorted(enriched_depth.keys()):
        print(f"  Depth {d:2d}: {enriched_depth[d]:3d} terms")

    # Build themes
    themes = build_depth_anchor_themes(
        bp_terms,
        godag,
        depth_range=(args.depth_min, args.depth_max),
        min_children=args.min_children,
        max_genes=args.max_genes,
        fdr_threshold=0.10
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

    total_children = sum(len(t.specific_terms) for t in themes)
    print(f"  Total nested specific terms: {total_children}")

    # Depth stats for anchors with children
    anchor_depths = [t.anchor_term.depth for t in themes if t.specific_terms]
    if anchor_depths:
        print(f"  Anchor depth range: {min(anchor_depths)}-{max(anchor_depths)}")

    # Save
    output_file = args.output_dir / f"{args.genes_file.stem}_depth_anchors.json"
    with open(output_file, "w") as f:
        json.dump({
            "metadata": {
                "algorithm": "depth-based anchors",
                "input_file": str(args.genes_file),
                "depth_range": [args.depth_min, args.depth_max],
                "min_children": args.min_children,
                "max_genes": args.max_genes,
                "n_themes": len(themes),
                "n_with_children": sum(1 for t in themes if t.specific_terms),
                "total_nested_children": total_children
            },
            "themes": themes_to_dict(themes)
        }, f, indent=2)

    print(f"\nThemes saved to: {output_file}")
