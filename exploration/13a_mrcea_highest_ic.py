#!/usr/bin/env python3
"""
Exploration 13a: MRCEA bottom-up anchor algorithm — highest-IC parent path.

Strategy
--------
For each enrichment leaf, walk upward through the GO DAG following the
single parent with the highest Information Content (IC) at each step.
This traces the "most informative" ancestral lineage.

Option B regulates (as agreed):
  - First step from any leaf: is_a + part_of parents only.
    Preserves the clean leaf-level distinction between a process and its
    regulation (which may have different molecular bases).
  - Subsequent steps: additionally follow regulates/positively_regulates/
    negatively_regulates. Allows regulatory terms already grouped with
    their process anchor to further merge upward.

Stopping criterion:
  Walk continues while IC(candidate parent) >= min_ic.
  IC(t) = -log2(count(t) / total_genes) where count(t) is the number of
  genes annotated to t or any is_a descendant in the full GAF.

Anchor selection:
  For each enriched term that appears in >=2 leaf ancestor chains, it is
  a candidate anchor. Greedy selection maximises IC x n_uncovered_leaves
  at each round.

Usage
-----
    uv run python exploration/13a_mrcea_highest_ic.py [--min-ic FLOAT] [--min-leaves INT]

Output
------
    results/13a_mrcea_highest_ic.json
    Console report: theme count, leaves/theme ratio, timing, top themes,
    leukocyte migration grouping, comparison vs production baseline.
"""

import argparse
import json
import math
import time
from collections import defaultdict
from pathlib import Path

from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS
from goatools.obo_parser import GODag

from goa_semantic_tools.utils.data_downloader import ensure_gaf_data, ensure_go_data
from goa_semantic_tools.utils.go_data_loader import load_gene_annotations, load_go_data
from goa_semantic_tools.utils.go_hierarchy import (
    EnrichedTerm,
    build_depth_anchor_themes,
    compute_enrichment_leaves,
    merge_identical_gene_sets,
    find_leaves,
)
from goa_semantic_tools.services.go_enrichment_service import (
    _convert_to_enriched_terms,
    _namespace_abbrev_to_full,
)

GENE_LIST_PATH = Path(__file__).parent.parent / "input_data/benchmark_sets/test_lists/hallmark_inflammatory_response.txt"
RESULTS_DIR = Path(__file__).parent.parent / "results"
OUTPUT_JSON = RESULTS_DIR / "13a_mrcea_highest_ic.json"

FDR_THRESHOLD = 0.05
MAX_GENES = 30
NAMESPACE = "biological_process"

# ─── Regulates relationship types (for option B) ──────────────────────────────

REG_RELS = frozenset({"regulates", "positively_regulates", "negatively_regulates"})


# ─── IC computation ───────────────────────────────────────────────────────────

def compute_ic(ns2assoc: dict, godag: GODag, namespace: str = NAMESPACE) -> tuple[dict[str, float], int]:
    """Compute Resnik IC for all GO terms from GAF annotations.

    Propagates annotations upward via is_a only (standard Resnik).
    Returns (ic_dict, total_annotated_genes).
    """
    gene_to_terms = ns2assoc.get(namespace, {})
    total_genes = len(gene_to_terms)
    if total_genes == 0:
        return {}, 0

    print(f"  Computing IC from {total_genes:,} annotated genes...")
    term_genes: dict[str, set[str]] = defaultdict(set)

    for gene, go_ids in gene_to_terms.items():
        for go_id in go_ids:
            term_genes[go_id].add(gene)
            if go_id in godag:
                for ancestor in godag[go_id].get_all_parents():
                    term_genes[ancestor].add(gene)

    ic: dict[str, float] = {}
    for go_id, genes in term_genes.items():
        p = len(genes) / total_genes
        ic[go_id] = -math.log2(p) if p > 0 else 0.0

    print(f"  IC computed for {len(ic):,} GO terms")
    return ic, total_genes


# ─── Upward traversal ─────────────────────────────────────────────────────────

def get_enriched_parents(
    go_id: str,
    godag: GODag,
    enriched_ids: set[str],
    include_regulates: bool,
) -> set[str]:
    """Return enriched parents of go_id.

    Follows is_a, part_of, and (if include_regulates) regulates edges.
    Only returns parents that are themselves enriched.
    """
    if go_id not in godag:
        return set()
    term = godag[go_id]
    parents: set[str] = set()

    # is_a parents
    for p in term.parents:
        if p.id in enriched_ids:
            parents.add(p.id)

    # part_of (and optionally regulates) from relationship dict
    if hasattr(term, "relationship") and term.relationship:
        for rel_type, rel_terms in term.relationship.items():
            if rel_type == "part_of" or (include_regulates and rel_type in REG_RELS):
                for rt in rel_terms:
                    if rt.id in enriched_ids:
                        parents.add(rt.id)

    return parents


def get_ancestor_chain_highest_ic(
    leaf_id: str,
    godag: GODag,
    enriched_ids: set[str],
    ic: dict[str, float],
    min_ic: float,
) -> list[str]:
    """Walk upward from leaf following the single highest-IC enriched parent.

    Option B: first step uses is_a + part_of only; subsequent steps add regulates.
    Stops when no valid parent above min_ic, or a cycle is detected.
    Returns ordered list of enriched ancestors (nearest first).
    """
    chain: list[str] = []
    current = leaf_id
    first_step = True
    visited = {leaf_id}

    while True:
        parents = get_enriched_parents(
            current, godag, enriched_ids, include_regulates=not first_step
        )
        valid = {p for p in parents if ic.get(p, 0.0) >= min_ic and p not in visited}
        if not valid:
            break
        best = max(valid, key=lambda p: ic.get(p, 0.0))
        visited.add(best)
        chain.append(best)
        current = best
        first_step = False

    return chain


# ─── Greedy anchor selection ──────────────────────────────────────────────────

def select_anchors_greedy(
    leaf_ids: set[str],
    leaf_ancestors: dict[str, list[str]],
    ic: dict[str, float],
    min_leaves: int = 2,
) -> tuple[list[tuple[str, set[str]]], list[str]]:
    """Greedy anchor selection maximising IC × n_uncovered_leaves.

    Returns (themes, standalones) where:
      themes = list of (anchor_go_id, set of leaf_go_ids)
      standalones = list of unassigned leaf_go_ids
    """
    # anchor → set of all leaves that have it in their chain
    anchor_to_leaves: dict[str, set[str]] = defaultdict(set)
    for leaf_id, chain in leaf_ancestors.items():
        for anc in chain:
            anchor_to_leaves[anc].add(leaf_id)

    unassigned = set(leaf_ids)
    used_anchors: set[str] = set()
    themes: list[tuple[str, set[str]]] = []

    while True:
        best_anchor = None
        best_score = -1.0
        best_covered: set[str] = set()

        for anchor_id, all_leaves in anchor_to_leaves.items():
            if anchor_id in used_anchors:
                continue
            available = all_leaves & unassigned
            if len(available) < min_leaves:
                continue
            score = ic.get(anchor_id, 0.0) * len(available)
            if score > best_score:
                best_score = score
                best_anchor = anchor_id
                best_covered = available

        if best_anchor is None:
            break

        themes.append((best_anchor, best_covered))
        used_anchors.add(best_anchor)
        unassigned -= best_covered

    standalones = list(unassigned)
    return themes, standalones


# ─── Report helpers ───────────────────────────────────────────────────────────

def print_theme_stats(label: str, n_themes: int, n_with_children: int, n_standalone: int,
                      n_leaves: int, elapsed: float) -> None:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Leaves (input)  : {n_leaves}")
    print(f"  Themes          : {n_themes}")
    print(f"  With children   : {n_with_children}")
    print(f"  Standalone      : {n_standalone}")
    print(f"  Leaves/theme    : {n_leaves / n_themes:.2f}" if n_themes else "  Leaves/theme: n/a")
    print(f"  Time            : {elapsed:.1f}s")


def check_leukocyte_migration(themes_desc: list[tuple[str, str, int]], enriched_terms: dict) -> None:
    """Print which theme(s) contain leukocyte migration terms."""
    lm_terms = {
        go_id for go_id, t in enriched_terms.items()
        if "leukocyte migration" in t.name.lower()
    }
    print(f"\n  Leukocyte migration cluster ({len(lm_terms)} enriched terms):")
    for anchor_id, anchor_name, n_leaves in themes_desc:
        if anchor_id in lm_terms:
            print(f"    ANCHOR: {anchor_name} ({anchor_id}), {n_leaves} leaves")
        else:
            covered = {go_id for go_id in lm_terms if go_id != anchor_id}
            if covered:  # placeholder — real check done in main
                pass


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-ic", type=float, default=3.0,
                        help="Minimum IC for anchor candidates (default: 3.0)")
    parser.add_argument("--min-leaves", type=int, default=2,
                        help="Minimum leaves per anchor theme (default: 2)")
    parser.add_argument("--gene-file", type=Path, default=GENE_LIST_PATH,
                        help="Path to gene list file (default: hallmark_inflammatory_response.txt)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("  13a: MRCEA — highest-IC parent path")
    print(f"  min_ic={args.min_ic}  min_leaves={args.min_leaves}")
    print(f"{'='*60}\n")

    # ── 1. Data loading ──────────────────────────────────────────────────────
    t0 = time.time()
    gene_file = args.gene_file
    genes = [g.strip() for g in gene_file.read_text().splitlines() if g.strip() and not g.startswith("#")]
    print(f"Gene list: {len(genes)} genes from {gene_file.name}")

    go_obo_path = ensure_go_data()
    gaf_path = ensure_gaf_data(species="human")
    godag = load_go_data(go_obo_path)
    ns2assoc = load_gene_annotations(gaf_path, godag)

    population = set()
    for ns_genes in ns2assoc.values():
        population.update(ns_genes.keys())
    study_set = {g for g in genes if g in population}
    print(f"Study set: {len(study_set)} genes in population")

    # ── 2. IC computation ────────────────────────────────────────────────────
    print("\nComputing IC...")
    ic, total_genes = compute_ic(ns2assoc, godag)

    # ── 3. GO enrichment ─────────────────────────────────────────────────────
    print("\nRunning GO enrichment...")
    goeaobj = GOEnrichmentStudyNS(
        population, ns2assoc, godag,
        propagate_counts=True, alpha=FDR_THRESHOLD, methods=["fdr_bh"]
    )
    goea_results_all = goeaobj.run_study(study_set)
    goea_sig = [r for r in goea_results_all if r.p_fdr_bh < FDR_THRESHOLD]
    print(f"  Significant terms: {len(goea_sig)}")

    enriched_terms: dict[str, EnrichedTerm] = _convert_to_enriched_terms(goea_sig, godag)

    # Filter to BP, max_genes
    bp_terms = {
        k: v for k, v in enriched_terms.items()
        if v.namespace == NAMESPACE and len(v.genes) <= MAX_GENES
    }
    enriched_ids = set(bp_terms.keys())
    print(f"  BP terms (max_genes={MAX_GENES}): {len(bp_terms)}")

    # ── 4. Baseline: production depth-anchor ─────────────────────────────────
    print("\nRunning production baseline (depth-anchor 4-7)...")
    t_base = time.time()
    baseline_themes = build_depth_anchor_themes(
        bp_terms, godag, depth_range=(4, 7), min_children=2,
        max_genes=MAX_GENES, fdr_threshold=FDR_THRESHOLD
    )
    elapsed_base = time.time() - t_base
    n_base_with_children = sum(1 for t in baseline_themes if t.specific_terms)
    n_base_standalone = sum(1 for t in baseline_themes if not t.specific_terms)

    # ── 5. Enrichment leaves ─────────────────────────────────────────────────
    print("\nComputing enrichment leaves...")
    leaves = compute_enrichment_leaves(bp_terms, godag, fdr_threshold=FDR_THRESHOLD, max_genes=MAX_GENES)
    leaf_ids = {leaf.go_id for leaf in leaves}
    print(f"  Leaves: {len(leaf_ids)}")

    # ── 6. MRCEA — highest-IC path ───────────────────────────────────────────
    print(f"\nRunning MRCEA (highest-IC path, min_ic={args.min_ic})...")
    t_mrcea = time.time()

    leaf_ancestors: dict[str, list[str]] = {}
    for leaf_id in leaf_ids:
        chain = get_ancestor_chain_highest_ic(leaf_id, godag, enriched_ids, ic, args.min_ic)
        leaf_ancestors[leaf_id] = chain

    n_with_ancestors = sum(1 for c in leaf_ancestors.values() if c)
    print(f"  Leaves with >=1 enriched ancestor: {n_with_ancestors}/{len(leaf_ids)}")

    themes, standalones = select_anchors_greedy(leaf_ids, leaf_ancestors, ic, args.min_leaves)
    elapsed_mrcea = time.time() - t_mrcea

    n_mrcea_themes = len(themes) + len(standalones)
    n_mrcea_with_children = len(themes)
    n_mrcea_standalone = len(standalones)

    # ── 7. Report ────────────────────────────────────────────────────────────
    print_theme_stats(
        "BASELINE (depth-anchor 4-7)",
        len(baseline_themes), n_base_with_children, n_base_standalone,
        len(leaf_ids), elapsed_base
    )
    print_theme_stats(
        f"MRCEA-A (highest-IC path, min_ic={args.min_ic})",
        n_mrcea_themes, n_mrcea_with_children, n_mrcea_standalone,
        len(leaf_ids), elapsed_mrcea
    )

    # Leukocyte migration cluster
    lm_go_ids = {go_id for go_id, t in bp_terms.items() if "leukocyte migration" in t.name.lower()}
    print(f"\n  Leukocyte migration enriched terms: {len(lm_go_ids)}")
    print("  Baseline anchors containing leukocyte migration terms:")
    for t in baseline_themes:
        if t.anchor_term.go_id in lm_go_ids:
            n_children = len(t.specific_terms)
            print(f"    ANCHOR: {t.anchor_term.name} ({t.anchor_term.go_id}), {n_children} children")
    print("  MRCEA-A themes containing leukocyte migration terms:")
    for anchor_id, covered_leaves in themes:
        if anchor_id in lm_go_ids:
            print(f"    ANCHOR: {bp_terms[anchor_id].name} ({anchor_id}), {len(covered_leaves)} leaves")
        # Check if any covered leaves are LM terms
        lm_leaves = covered_leaves & lm_go_ids
        if lm_leaves and anchor_id not in lm_go_ids:
            print(f"    Theme anchor={bp_terms.get(anchor_id, {}).name if anchor_id in bp_terms else anchor_id}, "
                  f"LM leaves under it: {[bp_terms[l].name for l in lm_leaves if l in bp_terms]}")

    # Top themes by IC
    print(f"\n  Top 20 MRCEA-A themes by anchor IC:")
    sorted_themes = sorted(themes, key=lambda x: -ic.get(x[0], 0))
    for anchor_id, covered_leaves in sorted_themes[:20]:
        name = bp_terms[anchor_id].name if anchor_id in bp_terms else anchor_id
        anchor_ic = ic.get(anchor_id, 0)
        print(f"    IC={anchor_ic:.2f}  n_leaves={len(covered_leaves):3d}  {name}")

    # ── 8. Save JSON ─────────────────────────────────────────────────────────
    RESULTS_DIR.mkdir(exist_ok=True)
    result = {
        "algorithm": "mrcea_highest_ic",
        "params": {"min_ic": args.min_ic, "min_leaves": args.min_leaves},
        "n_enriched_bp_terms": len(bp_terms),
        "n_leaves": len(leaf_ids),
        "baseline": {
            "n_themes": len(baseline_themes),
            "n_with_children": n_base_with_children,
            "n_standalone": n_base_standalone,
            "leaves_per_theme": round(len(leaf_ids) / len(baseline_themes), 2) if baseline_themes else 0,
            "elapsed_s": round(elapsed_base, 2),
        },
        "mrcea_a": {
            "n_themes": n_mrcea_themes,
            "n_with_children": n_mrcea_with_children,
            "n_standalone": n_mrcea_standalone,
            "leaves_per_theme": round(len(leaf_ids) / n_mrcea_themes, 2) if n_mrcea_themes else 0,
            "elapsed_s": round(elapsed_mrcea, 2),
        },
        "delta_vs_baseline": len(baseline_themes) - n_mrcea_themes,
        "lm_baseline_anchors": [
            t.anchor_term.name for t in baseline_themes if t.anchor_term.go_id in lm_go_ids
        ],
        "lm_mrcea_anchors": [
            bp_terms[a].name for a, _ in themes if a in lm_go_ids and a in bp_terms
        ],
        "top_themes": [
            {
                "anchor_id": a,
                "anchor_name": bp_terms[a].name if a in bp_terms else a,
                "anchor_ic": round(ic.get(a, 0), 3),
                "n_leaves": len(lv),
            }
            for a, lv in sorted(themes, key=lambda x: -ic.get(x[0], 0))[:30]
        ],
    }
    OUTPUT_JSON.write_text(json.dumps(result, indent=2))
    print(f"\nResults saved to {OUTPUT_JSON}")
    print(f"Total elapsed: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
