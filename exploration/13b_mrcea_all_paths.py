#!/usr/bin/env python3
"""
Exploration 13b: MRCEA bottom-up anchor algorithm — all-paths BFS.

Strategy
--------
For each enrichment leaf, BFS upward through ALL enriched parents
simultaneously. This finds every possible grouping, not just the ones
reachable via the single highest-IC path.

Option B regulates (as agreed):
  - First step from any leaf: is_a + part_of parents only.
  - Subsequent steps: additionally follow regulates/positively_regulates/
    negatively_regulates. Once we're above the leaf, regulatory terms can
    link to their process anchors.

Stopping criterion:
  BFS continues while IC(candidate node) >= min_ic. Nodes with IC below
  min_ic are excluded (too general to be useful anchors). This means the
  BFS may terminate at different depths in different GO branches.

Anchor selection:
  For each enriched term that is an ancestor of >=2 leaves, it is a
  candidate anchor. Greedy selection maximises IC x n_uncovered_leaves.

Compared to 13a (highest-IC path):
  13a may miss groupings if a valid shared ancestor is not on the
  highest-IC path from either leaf. 13b finds all such groupings but
  may be slower due to wider BFS.

Usage
-----
    uv run python exploration/13b_mrcea_all_paths.py [--min-ic FLOAT] [--min-leaves INT]

Output
------
    results/13b_mrcea_all_paths.json
    Console report: theme count, leaves/theme ratio, timing, top themes,
    leukocyte migration grouping, comparison vs production baseline and 13a.
"""

import argparse
import json
import math
import time
from collections import defaultdict, deque
from pathlib import Path

from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS
from goatools.obo_parser import GODag

from goa_semantic_tools.utils.data_downloader import ensure_gaf_data, ensure_go_data
from goa_semantic_tools.utils.go_data_loader import load_gene_annotations, load_go_data
from goa_semantic_tools.utils.go_hierarchy import (
    EnrichedTerm,
    build_depth_anchor_themes,
    compute_enrichment_leaves,
)
from goa_semantic_tools.services.go_enrichment_service import _convert_to_enriched_terms

GENE_LIST_PATH = Path(__file__).parent.parent / "input_data/benchmark_sets/test_lists/hallmark_inflammatory_response.txt"
RESULTS_DIR = Path(__file__).parent.parent / "results"
OUTPUT_JSON = RESULTS_DIR / "13b_mrcea_all_paths.json"

FDR_THRESHOLD = 0.05
MAX_GENES = 30
NAMESPACE = "biological_process"

REG_RELS = frozenset({"regulates", "positively_regulates", "negatively_regulates"})


# ─── IC computation ───────────────────────────────────────────────────────────

def compute_ic(ns2assoc: dict, godag: GODag, namespace: str = NAMESPACE) -> tuple[dict[str, float], int]:
    """Compute Resnik IC for all GO terms from GAF annotations (is_a propagation)."""
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
    """Return enriched parents via is_a, part_of, and (optionally) regulates."""
    if go_id not in godag:
        return set()
    term = godag[go_id]
    parents: set[str] = set()

    for p in term.parents:
        if p.id in enriched_ids:
            parents.add(p.id)

    if hasattr(term, "relationship") and term.relationship:
        for rel_type, rel_terms in term.relationship.items():
            if rel_type == "part_of" or (include_regulates and rel_type in REG_RELS):
                for rt in rel_terms:
                    if rt.id in enriched_ids:
                        parents.add(rt.id)

    return parents


def get_ancestor_set_all_paths(
    leaf_id: str,
    godag: GODag,
    enriched_ids: set[str],
    ic: dict[str, float],
    min_ic: float,
) -> set[str]:
    """BFS upward through ALL enriched parents from a leaf.

    Option B: first step from the leaf is is_a + part_of only.
    All subsequent steps add regulates edges.
    Nodes with IC < min_ic are pruned (not added to ancestor set,
    but their enriched parents are still explored one level further
    to avoid missing intermediate valid anchors).
    """
    ancestors: set[str] = set()
    visited: set[str] = {leaf_id}

    # First step: is_a + part_of only (Option B)
    first_parents = get_enriched_parents(leaf_id, godag, enriched_ids, include_regulates=False)
    queue: deque[str] = deque()
    for p in first_parents:
        if p not in visited:
            visited.add(p)
            queue.append(p)

    while queue:
        current = queue.popleft()
        current_ic = ic.get(current, 0.0)

        if current_ic >= min_ic:
            ancestors.add(current)
            # Continue BFS upward from this node (with regulates)
            for p in get_enriched_parents(current, godag, enriched_ids, include_regulates=True):
                if p not in visited:
                    visited.add(p)
                    queue.append(p)
        # If IC too low, still try its parents in case of IC non-monotonicity
        # (rare in practice, but DAG structure means a low-IC node can have
        # a higher-IC parent if it has multiple children outside our study set)
        else:
            for p in get_enriched_parents(current, godag, enriched_ids, include_regulates=True):
                if p not in visited and ic.get(p, 0.0) >= min_ic:
                    visited.add(p)
                    queue.append(p)

    return ancestors


# ─── Greedy anchor selection ──────────────────────────────────────────────────

def select_anchors_greedy(
    leaf_ids: set[str],
    leaf_ancestors: dict[str, set[str]],
    ic: dict[str, float],
    min_leaves: int = 2,
    max_secondary: int = 3,
) -> tuple[list[tuple[str, set[str]]], list[str], dict[str, list[str]], dict[str, list[str]]]:
    """Greedy anchor selection maximising IC × n_uncovered_leaves.

    Returns:
        themes:              [(anchor_id, primary_leaves), ...]
        standalones:         [leaf_id, ...]  (no primary anchor)
        primary_of:          {leaf_id: anchor_id}  (primary assignment)
        secondary_of:        {leaf_id: [anchor_id, ...]}  (secondary memberships,
                              capped at max_secondary, ranked by IC descending)
    """
    anchor_to_leaves: dict[str, set[str]] = defaultdict(set)
    for leaf_id, ancestors in leaf_ancestors.items():
        for anc in ancestors:
            anchor_to_leaves[anc].add(leaf_id)

    unassigned = set(leaf_ids)
    used_anchors: set[str] = set()
    themes: list[tuple[str, set[str]]] = []
    primary_of: dict[str, str] = {}

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
        for lid in best_covered:
            primary_of[lid] = best_anchor
        unassigned -= best_covered

    standalones = list(unassigned)

    # Secondary membership: for each leaf, all selected anchors in its ancestor
    # set OTHER than its primary anchor, ranked by IC, capped at max_secondary.
    selected_anchor_ids = {anchor_id for anchor_id, _ in themes}
    secondary_of: dict[str, list[str]] = {}
    for lid in leaf_ids:
        candidate_secondaries = [
            a for a in leaf_ancestors.get(lid, set())
            if a in selected_anchor_ids and a != primary_of.get(lid)
        ]
        candidate_secondaries.sort(key=lambda a: -ic.get(a, 0.0))
        secondary_of[lid] = candidate_secondaries[:max_secondary]

    return themes, standalones, primary_of, secondary_of


# ─── Absorption of stranded leaves into existing themes ───────────────────────

def absorb_stranded_into_themes(
    stranded: list[str],
    themes: list[tuple[str, set[str]]],
    godag: GODag,
    ic: dict[str, float],
) -> dict[str, str]:
    """For each stranded leaf, find the best existing theme to absorb it into.

    Uses FULL GO DAG ancestry (not enriched-only BFS) to bridge gaps caused
    by non-enriched intermediates. For each stranded leaf, walks all GO
    ancestors and returns the selected primary theme anchor with the highest IC.

    This is the multi-inheritance absorption approach: stranded leaves are
    added as secondary members of their most semantically specific existing
    theme, even when the enriched-only path doesn't connect them directly.

    Returns:
        {leaf_id: anchor_id}  absorption assignment (only for leaves that
        find a matching theme anchor; unabsorbable leaves are omitted)
    """
    selected_anchors: set[str] = {anchor_id for anchor_id, _ in themes}
    absorb_to: dict[str, str] = {}

    for lid in stranded:
        if lid not in godag:
            continue
        # Walk ALL ancestors in full GO DAG (not enriched-only)
        all_go_ancestors = godag[lid].get_all_parents()
        # Add part_of and regulates ancestors
        if hasattr(godag[lid], "relationship") and godag[lid].relationship:
            for rel_type, rel_terms in godag[lid].relationship.items():
                for rt in rel_terms:
                    if rt.id in godag:
                        all_go_ancestors |= {rt.id} | godag[rt.id].get_all_parents()

        # Find selected theme anchors reachable via full DAG
        reachable_anchors = all_go_ancestors & selected_anchors
        if reachable_anchors:
            best = max(reachable_anchors, key=lambda a: ic.get(a, 0.0))
            absorb_to[lid] = best

    return absorb_to


# ─── Rescue pass ──────────────────────────────────────────────────────────────

def rescue_stranded_leaves(
    stranded: list[str],
    leaf_ancestors: dict[str, set[str]],
    ic: dict[str, float],
    min_ic_rescue: float = 4.0,
    min_leaves_group: int = 2,
) -> tuple[list[tuple[str, set[str]]], list[str]]:
    """Attempt to assign stranded leaves that the main greedy pass left behind.

    Two-stage rescue:
    1. Mini-greedy among stranded leaves only: find ancestors shared by
       >= min_leaves_group stranded leaves (no interaction with already-assigned
       leaves). Uses IC × n_stranded_covered scoring, same as main greedy.
    2. Singleton rescue: remaining stranded leaves with any ancestor above
       min_ic_rescue get a single-leaf theme at their highest-IC ancestor.

    Args:
        stranded:          leaf IDs not assigned by the main greedy pass.
        leaf_ancestors:    full ancestor sets (same as passed to main greedy).
        ic:                IC values for all GO terms.
        min_ic_rescue:     IC floor for rescue anchors (default 4.0 — slightly
                           higher than main min_ic=3.0 to avoid very general
                           rescue anchors).
        min_leaves_group:  minimum stranded leaves for a group rescue anchor.

    Returns:
        rescue_themes:  [(anchor_id, leaf_ids), ...]  new themes from rescue
        still_stranded: leaf IDs that could not be rescued
    """
    stranded_set = set(stranded)

    # Build anchor → stranded leaves mapping
    anchor_to_stranded: dict[str, set[str]] = defaultdict(set)
    for lid in stranded_set:
        for anc in leaf_ancestors.get(lid, set()):
            if ic.get(anc, 0.0) >= min_ic_rescue:
                anchor_to_stranded[anc].add(lid)

    # Stage 1: mini-greedy on stranded leaves
    unrescued = set(stranded_set)
    used_rescue_anchors: set[str] = set()
    rescue_themes: list[tuple[str, set[str]]] = []

    while True:
        best_anchor = None
        best_score = -1.0
        best_covered: set[str] = set()

        for anchor_id, all_stranded in anchor_to_stranded.items():
            if anchor_id in used_rescue_anchors:
                continue
            available = all_stranded & unrescued
            if len(available) < min_leaves_group:
                continue
            score = ic.get(anchor_id, 0.0) * len(available)
            if score > best_score:
                best_score = score
                best_anchor = anchor_id
                best_covered = available

        if best_anchor is None:
            break

        rescue_themes.append((best_anchor, best_covered))
        used_rescue_anchors.add(best_anchor)
        unrescued -= best_covered

    # Stage 2: singleton rescue — highest-IC ancestor above floor
    for lid in list(unrescued):
        candidates = [
            a for a in leaf_ancestors.get(lid, set())
            if ic.get(a, 0.0) >= min_ic_rescue
        ]
        if candidates:
            best = max(candidates, key=lambda a: ic.get(a, 0.0))
            rescue_themes.append((best, {lid}))
            unrescued.discard(lid)

    return rescue_themes, list(unrescued)


# ─── Two-pass anchor selection ────────────────────────────────────────────────

def select_anchors_two_pass(
    leaf_ids: set[str],
    leaf_ancestors: dict[str, set[str]],
    ic: dict[str, float],
    min_leaves: int = 2,
    max_secondary: int = 3,
) -> tuple[list[tuple[str, set[str]]], list[str], dict[str, str], dict[str, list[str]]]:
    """Two-pass anchor selection: decouple anchor selection from leaf assignment.

    Pass 1 — anchor selection (non-destructive):
        Select all candidate anchors with >= min_leaves total leaves,
        without removing leaves from the pool. Leaves can count toward
        multiple anchors simultaneously. This avoids the greedy stranding
        problem where a leaf's ancestor drops below min_leaves because
        another anchor claimed its siblings first.

    Pass 2 — primary assignment:
        Each leaf independently chooses its highest-IC selected anchor
        as its primary theme. Anchors that end up with < min_leaves
        primary members are pruned (they 'won' no leaves in the contest).

    The key difference from select_anchors_greedy: anchor quality is judged
    on the full leaf set, not the residual uncovered set. Enforcement of
    single-inheritance happens in pass 2, not pass 1.
    """
    anchor_to_all_leaves: dict[str, set[str]] = defaultdict(set)
    for lid, ancestors in leaf_ancestors.items():
        for anc in ancestors:
            anchor_to_all_leaves[anc].add(lid)

    # Pass 1: select anchors with >= min_leaves total leaves (no removal)
    selected_anchors: set[str] = {
        aid for aid, lv in anchor_to_all_leaves.items()
        if len(lv) >= min_leaves
    }

    # Pass 2: each leaf → highest-IC selected ancestor
    primary_of: dict[str, str] = {}
    for lid in leaf_ids:
        candidates = [a for a in leaf_ancestors.get(lid, set()) if a in selected_anchors]
        if candidates:
            primary_of[lid] = max(candidates, key=lambda a: ic.get(a, 0.0))

    # Build themes from primary assignment; prune anchors with < min_leaves primary
    theme_leaves: dict[str, set[str]] = defaultdict(set)
    for lid, anchor in primary_of.items():
        theme_leaves[anchor].add(lid)
    themes = [(aid, lv) for aid, lv in theme_leaves.items() if len(lv) >= min_leaves]

    # Re-derive primary_of for pruned set; standalones = leaves not in any theme
    primary_of_final: dict[str, str] = {lid: aid for aid, lv in themes for lid in lv}
    standalones = [lid for lid in leaf_ids if lid not in primary_of_final]

    # Secondary membership (same logic as greedy variant)
    selected_anchor_ids = {aid for aid, _ in themes}
    secondary_of: dict[str, list[str]] = {}
    for lid in leaf_ids:
        candidates_sec = [
            a for a in leaf_ancestors.get(lid, set())
            if a in selected_anchor_ids and a != primary_of_final.get(lid)
        ]
        candidates_sec.sort(key=lambda a: -ic.get(a, 0.0))
        secondary_of[lid] = candidates_sec[:max_secondary]

    return themes, standalones, primary_of_final, secondary_of


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
    print("  13b: MRCEA — all-paths BFS")
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
    bp_terms = {
        k: v for k, v in enriched_terms.items()
        if v.namespace == NAMESPACE and len(v.genes) <= MAX_GENES
    }
    enriched_ids = set(bp_terms.keys())
    print(f"  BP terms (max_genes={MAX_GENES}): {len(bp_terms)}")

    # ── 4. Baseline ──────────────────────────────────────────────────────────
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

    # ── 6. MRCEA — all paths BFS ─────────────────────────────────────────────
    print(f"\nRunning MRCEA all-paths BFS (min_ic={args.min_ic})...")
    t_mrcea = time.time()

    leaf_ancestors: dict[str, set[str]] = {}
    for leaf_id in leaf_ids:
        ancestors = get_ancestor_set_all_paths(leaf_id, godag, enriched_ids, ic, args.min_ic)
        leaf_ancestors[leaf_id] = ancestors

    n_with_ancestors = sum(1 for ancs in leaf_ancestors.values() if ancs)
    avg_ancestors = sum(len(a) for a in leaf_ancestors.values()) / len(leaf_ids) if leaf_ids else 0
    print(f"  Leaves with >=1 enriched ancestor: {n_with_ancestors}/{len(leaf_ids)}")
    print(f"  Avg enriched ancestors per leaf: {avg_ancestors:.1f}")

    themes, standalones, primary_of, secondary_of = select_anchors_greedy(
        leaf_ids, leaf_ancestors, ic, args.min_leaves
    )
    elapsed_mrcea = time.time() - t_mrcea

    n_mrcea_themes = len(themes) + len(standalones)
    n_mrcea_with_children = len(themes)
    n_mrcea_standalone = len(standalones)

    # Absorption of stranded leaves via full GO DAG ancestry
    stranded = [lid for lid in standalones if leaf_ancestors.get(lid)]
    truly_isolated = [lid for lid in standalones if not leaf_ancestors.get(lid)]
    absorb_to = absorb_stranded_into_themes(stranded, themes, godag, ic)

    # Rescue pass
    rescue_themes, still_stranded = rescue_stranded_leaves(
        stranded, leaf_ancestors, ic, min_ic_rescue=4.0
    )
    n_rescued_total = len(themes) + len(rescue_themes) + len(truly_isolated) + len(still_stranded)
    n_rescued_with_children = len(themes) + sum(1 for _, lv in rescue_themes if len(lv) >= 2)
    n_rescued_standalone = len(truly_isolated) + len(still_stranded) + sum(1 for _, lv in rescue_themes if len(lv) == 1)

    # Two-pass variant
    t_tp = time.time()
    themes_tp, standalones_tp, primary_of_tp, secondary_of_tp = select_anchors_two_pass(
        leaf_ids, leaf_ancestors, ic, args.min_leaves
    )
    elapsed_tp = time.time() - t_tp
    n_tp_themes = len(themes_tp) + len(standalones_tp)
    n_tp_with_children = len(themes_tp)
    n_tp_standalone = len(standalones_tp)

    # ── 7. Report ────────────────────────────────────────────────────────────
    print_theme_stats(
        "BASELINE (depth-anchor 4-7)",
        len(baseline_themes), n_base_with_children, n_base_standalone,
        len(leaf_ids), elapsed_base
    )
    print_theme_stats(
        f"MRCEA-B (all-paths BFS, min_ic={args.min_ic})",
        n_mrcea_themes, n_mrcea_with_children, n_mrcea_standalone,
        len(leaf_ids), elapsed_mrcea
    )

    # Absorption report
    print(f"\n{'='*60}")
    print("  ABSORPTION: stranded leaves → existing themes (full DAG)")
    print(f"{'='*60}")
    print(f"  Stranded leaves: {len(stranded)}")
    print(f"  Absorbable (reach a theme via full DAG): {len(absorb_to)}")
    print(f"  Unabsorbable: {len(stranded) - len(absorb_to)}")

    # Which themes absorb the most stranded leaves
    theme_absorb_count: dict[str, list[str]] = defaultdict(list)
    for lid, anchor_id in absorb_to.items():
        theme_absorb_count[anchor_id].append(lid)
    print(f"\n  Themes absorbing most stranded leaves:")
    for anchor_id, absorbed_lids in sorted(theme_absorb_count.items(), key=lambda x: -len(x[1]))[:10]:
        anchor_name = bp_terms[anchor_id].name if anchor_id in bp_terms else anchor_id
        n_primary = sum(1 for lid, a in primary_of.items() if a == anchor_id)
        print(f"    +{len(absorbed_lids)} absorbed  ({n_primary} primary)  {anchor_name}")
        for lid in sorted(absorbed_lids, key=lambda x: -ic.get(x, 0))[:4]:
            name = bp_terms[lid].name if lid in bp_terms else lid
            print(f"      IC={ic.get(lid,0):.2f}  {name}")

    print(f"\n  Unabsorbable stranded leaves (no theme reachable via full DAG):")
    unabsorbable = [lid for lid in stranded if lid not in absorb_to]
    for lid in sorted(unabsorbable, key=lambda x: -ic.get(x, 0))[:10]:
        name = bp_terms[lid].name if lid in bp_terms else lid
        print(f"    IC={ic.get(lid,0):.2f}  {name}")

    print_theme_stats(
        f"MRCEA-B + rescue pass (min_ic={args.min_ic}, rescue_ic=4.0)",
        n_rescued_total, n_rescued_with_children, n_rescued_standalone,
        len(leaf_ids), elapsed_mrcea
    )
    n_group_rescued = sum(1 for _, lv in rescue_themes if len(lv) >= 2)
    n_singleton_rescued = sum(1 for _, lv in rescue_themes if len(lv) == 1)
    print(f"  Rescue detail: {n_group_rescued} group themes, {n_singleton_rescued} singletons, "
          f"{len(still_stranded)} unrescuable")

    print_theme_stats(
        f"MRCEA-B two-pass (min_ic={args.min_ic})",
        n_tp_themes, n_tp_with_children, n_tp_standalone,
        len(leaf_ids), elapsed_tp
    )

    # Leukocyte migration analysis
    lm_go_ids = {go_id for go_id, t in bp_terms.items() if "leukocyte migration" in t.name.lower()}
    print(f"\n  Leukocyte migration enriched terms: {len(lm_go_ids)}")
    print("  Baseline anchors containing leukocyte migration terms:")
    for t in baseline_themes:
        if t.anchor_term.go_id in lm_go_ids:
            print(f"    ANCHOR: {t.anchor_term.name} ({t.anchor_term.go_id}), {len(t.specific_terms)} children")
    print("  MRCEA-B themes containing leukocyte migration terms as ANCHOR:")
    for anchor_id, covered_leaves in themes:
        if anchor_id in lm_go_ids:
            print(f"    ANCHOR: {bp_terms[anchor_id].name} ({anchor_id}), {len(covered_leaves)} leaves")
    print("  MRCEA-B themes with leukocyte migration terms as LEAVES under non-LM anchor:")
    for anchor_id, covered_leaves in themes:
        lm_leaves = covered_leaves & lm_go_ids
        if lm_leaves and anchor_id not in lm_go_ids:
            lm_names = [bp_terms[l].name for l in lm_leaves if l in bp_terms]
            anchor_name = bp_terms[anchor_id].name if anchor_id in bp_terms else anchor_id
            print(f"    anchor={anchor_name}: LM leaves={lm_names}")

    print("\n  TWO-PASS leukocyte migration anchors:")
    for anchor_id, covered_leaves in themes_tp:
        if anchor_id in lm_go_ids:
            print(f"    ANCHOR: {bp_terms[anchor_id].name} ({anchor_id}), {len(covered_leaves)} primary leaves")

    # Stranded comparison
    stranded_greedy = {lid for lid in standalones if leaf_ancestors.get(lid)}
    stranded_tp = {lid for lid in standalones_tp if leaf_ancestors.get(lid)}
    rescued_by_tp = stranded_greedy - stranded_tp
    print(f"\n  Stranded leaves: greedy={len(stranded_greedy)}, two-pass={len(stranded_tp)}")
    print(f"  Rescued by two-pass: {len(rescued_by_tp)}")
    if rescued_by_tp:
        rescued_sorted = sorted(rescued_by_tp, key=lambda lid: -ic.get(lid, 0))[:10]
        for lid in rescued_sorted:
            name = bp_terms[lid].name if lid in bp_terms else lid
            new_anchor = primary_of_tp.get(lid, "?")
            anchor_name = bp_terms[new_anchor].name if new_anchor in bp_terms else new_anchor
            print(f"    IC={ic.get(lid,0):.2f}  {name}")
            print(f"      → primary in two-pass: {anchor_name}")

    # Top themes by IC
    print(f"\n  Top 20 MRCEA-B themes by anchor IC:")
    sorted_themes = sorted(themes, key=lambda x: -ic.get(x[0], 0))
    for anchor_id, covered_leaves in sorted_themes[:20]:
        name = bp_terms[anchor_id].name if anchor_id in bp_terms else anchor_id
        anchor_ic = ic.get(anchor_id, 0)
        fdr = bp_terms[anchor_id].fdr if anchor_id in bp_terms else float("nan")
        print(f"    IC={anchor_ic:.2f}  n_leaves={len(covered_leaves):3d}  FDR={fdr:.2e}  {name}")

    # Ancestor coverage stats by IC band
    print("\n  Ancestor count per leaf (IC coverage):")
    for band_min, band_max in [(0, 2), (2, 4), (4, 6), (6, 99)]:
        in_band = sum(
            1 for ancs in leaf_ancestors.values()
            if any(band_min <= ic.get(a, 0) < band_max for a in ancs)
        )
        print(f"    IC [{band_min}, {band_max}): {in_band} leaves have >=1 ancestor")

    # ── Secondary membership analysis ────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  SECONDARY MEMBERSHIP ANALYSIS")
    print(f"{'='*60}")

    # Distribution of secondary membership count across all leaves
    sec_counts = [len(secondary_of.get(lid, [])) for lid in leaf_ids]
    for n in range(4):
        count = sum(1 for c in sec_counts if c == n)
        label = f"  {n} secondary memberships" if n < 3 else "  3 secondary memberships (capped)"
        print(f"    {label}: {count} leaves")

    # Standalones rescued by secondary membership
    stranded = [lid for lid in standalones if leaf_ancestors.get(lid)]
    rescued = [lid for lid in stranded if secondary_of.get(lid)]
    truly_isolated = [lid for lid in standalones if not leaf_ancestors.get(lid)]
    print(f"\n  Standalones: {len(standalones)} total")
    print(f"    Topologically isolated (no enriched ancestor): {len(truly_isolated)}")
    print(f"    Stranded (had ancestors, not assigned primarily): {len(stranded)}")
    print(f"    Stranded with >=1 secondary membership:  {len(rescued)}")
    print(f"    Stranded with no secondary membership:   {len(stranded) - len(rescued)}")

    # Top 5 rescued standalones (highest IC, with their secondary anchors)
    if rescued:
        print(f"\n  Top rescued stranded leaves (by IC):")
        rescued_sorted = sorted(rescued, key=lambda lid: -ic.get(lid, 0))[:8]
        for lid in rescued_sorted:
            t = bp_terms.get(lid)
            name = t.name if t else lid
            leaf_ic = ic.get(lid, 0)
            sec_names = [
                bp_terms[a].name if a in bp_terms else a
                for a in secondary_of[lid]
            ]
            print(f"    IC={leaf_ic:.2f}  {name}")
            for s in sec_names:
                print(f"      → secondary: {s}")

    # Themes with most secondary members
    theme_secondary_count: dict[str, int] = defaultdict(int)
    for lid in leaf_ids:
        for sec_anchor in secondary_of.get(lid, []):
            theme_secondary_count[sec_anchor] += 1

    print(f"\n  Themes with most secondary members (top 10):")
    top_sec_themes = sorted(theme_secondary_count.items(), key=lambda x: -x[1])[:10]
    for anchor_id, n_sec in top_sec_themes:
        name = bp_terms[anchor_id].name if anchor_id in bp_terms else anchor_id
        n_primary = sum(1 for lid, a in primary_of.items() if a == anchor_id)
        print(f"    {n_sec:3d} secondary  ({n_primary:3d} primary)  {name}")

    # Hub gene secondary exposure
    # For each leaf, which genes appear? Count gene → n_secondary_themes
    gene_secondary_themes: dict[str, set[str]] = defaultdict(set)
    for lid, sec_anchors in secondary_of.items():
        t = bp_terms.get(lid)
        if not t:
            continue
        for gene in t.genes:
            for sec_anchor in sec_anchors:
                gene_secondary_themes[gene].add(sec_anchor)

    print(f"\n  Genes with most secondary theme exposure (top 10):")
    top_sec_genes = sorted(gene_secondary_themes.items(), key=lambda x: -len(x[1]))[:10]
    for gene, sec_theme_set in top_sec_genes:
        # count primary themes this gene appears in
        n_primary_themes = sum(
            1 for anchor_id, covered in themes
            if any(gene in bp_terms[lid].genes for lid in covered if lid in bp_terms)
        )
        print(f"    {gene}: {len(sec_theme_set)} secondary themes  ({n_primary_themes} primary themes)")

    # ── 8. Save JSON ─────────────────────────────────────────────────────────
    RESULTS_DIR.mkdir(exist_ok=True)
    result = {
        "algorithm": "mrcea_all_paths",
        "params": {"min_ic": args.min_ic, "min_leaves": args.min_leaves},
        "n_enriched_bp_terms": len(bp_terms),
        "n_leaves": len(leaf_ids),
        "avg_ancestors_per_leaf": round(avg_ancestors, 2),
        "baseline": {
            "n_themes": len(baseline_themes),
            "n_with_children": n_base_with_children,
            "n_standalone": n_base_standalone,
            "leaves_per_theme": round(len(leaf_ids) / len(baseline_themes), 2) if baseline_themes else 0,
            "elapsed_s": round(elapsed_base, 2),
        },
        "mrcea_b": {
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
                "anchor_fdr": bp_terms[a].fdr if a in bp_terms else None,
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
