#!/usr/bin/env python3
"""
Exploration 12: Regulates-based anchor grouping pilot (v2).

Tests whether extending get_all_descendants() to follow regulates
relationships, COMBINED with de-prioritising regulatory terms as anchor
candidates, achieves "X and its regulation" theme merging.

Background
----------
In the current production algorithm, "leukocyte migration" and
"regulation of leukocyte migration" live in different is_a subtrees
connected only via a `regulates` edge. They can never be grouped under
a common anchor, so each spawns its own cluster of near-identical themes.

V1 finding (regulates descendant extension alone)
-------------------------------------------------
Adding regulates to get_all_descendants DID make "leukocyte migration"
see its regulatory variants as descendants — but the greedy algorithm's
depth-first sort processed "regulation of leukocyte migration" (d=6)
and "positive regulation of leukocyte migration" (d=7) as anchors BEFORE
"leukocyte migration" (d=4) got its turn. By the time "leukocyte migration"
was tried as an anchor, both regulatory variants were already assigned.
Result: 10 fewer themes overall (other processes merged), but zero
"regulation of X" standalone merges, and leukocyte migration unchanged.

V2 fix: priority sort for process terms
----------------------------------------
Change the anchor candidate sort key from:
    (-depth, fdr)
to:
    (is_regulatory, -depth, fdr)
where is_regulatory = 1 if "regulation of" in name.lower() else 0.

Non-regulatory terms (is_regulatory=0) sort first, so "leukocyte migration"
(d=4, non-regulatory) is tried before "regulation of leukocyte migration"
(d=6, regulatory). It absorbs regulatory variants as children, and the
regulatory terms are marked assigned before they can become anchors.

The semantic result: anchor = "X", specific_terms includes "regulation of X",
"positive regulation of X", "negative regulation of X" — i.e., one theme
"X (and its regulation)" replaces 2–4 separate themes.

Architecture note
-----------------
Leaves (is_a + part_of only) define ontological specificity — unchanged.
Anchor grouping (is_a + part_of + regulates + priority sort) groups
causally related clusters into coherent biological story units.

Data note
---------
Works with ~570 terms reconstructed from results/hm_inflam_enrichment.json
(leaves + anchor terms + specific terms), not the full 1042 enriched terms.

Usage
-----
    uv run python exploration/12_regulates_anchor.py

Output
------
    results/12_regulates_anchor_comparison.json
    Console report comparing three variants:
      BASELINE   — current production (is_a + part_of, depth-first sort)
      REG-ONLY   — regulates extension, same sort (v1 result)
      REG+PRIO   — regulates extension + process-first sort (v2 result)
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from goatools.obo_parser import GODag


# =============================================================================
# Data classes (minimal local copies — no core lib edits)
# =============================================================================


@dataclass
class EnrichedTerm:
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
    anchor_term: EnrichedTerm
    specific_terms: list[EnrichedTerm]
    anchor_confidence: str

    @property
    def all_genes(self) -> set:
        genes = set(self.anchor_term.genes)
        for s in self.specific_terms:
            genes.update(s.genes)
        return genes


# =============================================================================
# Two descendant traversal functions — the only difference between runs
# =============================================================================

_REGULATES_RELS = {"regulates", "positively_regulates", "negatively_regulates"}
_ANCHOR_RELS_BASELINE = {"part_of"}
_ANCHOR_RELS_REGULATES = {"part_of"} | _REGULATES_RELS


def _get_all_descendants(go_id: str, godag: GODag, extra_rels: set[str]) -> set[str]:
    """Shared traversal core. is_a via term.children; extra_rels via reverse scan."""
    if go_id not in godag:
        return set()

    term = godag[go_id]
    descendants: set[str] = set()
    to_visit = list(term.children)

    while to_visit:
        child = to_visit.pop()
        if child.id not in descendants:
            descendants.add(child.id)
            to_visit.extend(child.children)

    # Reverse scan: find terms that point *at* go_id via extra_rels
    for term_id, dag_term in godag.items():
        if hasattr(dag_term, "relationship") and dag_term.relationship:
            for rel_type, rel_terms in dag_term.relationship.items():
                if rel_type in extra_rels:
                    for rel_term in rel_terms:
                        if rel_term.id == go_id and term_id not in descendants:
                            descendants.add(term_id)

    return descendants


def get_descendants_baseline(go_id: str, godag: GODag) -> set[str]:
    """is_a + part_of. Matches current production logic."""
    return _get_all_descendants(go_id, godag, _ANCHOR_RELS_BASELINE)


def get_descendants_with_regulates(go_id: str, godag: GODag) -> set[str]:
    """is_a + part_of + regulates / positively_regulates / negatively_regulates."""
    return _get_all_descendants(go_id, godag, _ANCHOR_RELS_REGULATES)


# =============================================================================
# Theme building — parameterised on descendant function
# =============================================================================


DescendantsFn = Callable[[str, GODag], set[str]]


def _is_regulatory(name: str) -> int:
    """1 if term name starts with a regulation prefix, else 0.
    Used as primary sort key so process terms are tried as anchors first."""
    low = name.lower()
    return 1 if (
        low.startswith("regulation of")
        or low.startswith("positive regulation of")
        or low.startswith("negative regulation of")
    ) else 0


def _find_leaves(
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    fdr_threshold: float,
    descendants_fn: DescendantsFn,
) -> set[str]:
    passing = {go_id for go_id, t in terms.items() if t.fdr < fdr_threshold}
    leaves = set()
    for go_id in passing:
        if go_id not in godag:
            continue
        if not (passing & descendants_fn(go_id, godag)):
            leaves.add(go_id)
    return leaves


def _merge_identical_gene_sets(term_ids: set[str], terms: dict[str, EnrichedTerm]) -> set[str]:
    groups: dict[frozenset, list[str]] = defaultdict(list)
    for go_id in term_ids:
        if go_id in terms:
            groups[terms[go_id].genes].append(go_id)
    merged = set()
    for group in groups.values():
        merged.add(
            group[0]
            if len(group) == 1
            else min(group, key=lambda x: (terms[x].fdr, -terms[x].fold_enrichment))
        )
    return merged


def _conf(fdr: float) -> str:
    return "FDR<0.01" if fdr < 0.01 else "FDR<0.05" if fdr < 0.05 else "FDR<0.10"


def build_themes(
    terms: dict[str, EnrichedTerm],
    godag: GODag,
    descendants_fn: DescendantsFn,
    priority_sort: bool = False,
    depth_range: tuple[int, int] = (4, 7),
    min_children: int = 2,
    max_genes: int = 30,
    fdr_threshold: float = 0.10,
) -> list[HierarchicalTheme]:
    """Build hierarchical themes using the supplied descendant traversal function.

    Args:
        priority_sort: If True, sort process terms before regulatory terms
            regardless of depth — (is_regulatory, -depth, fdr).
            If False, use production sort — (-depth, fdr).
    """
    terms = {k: v for k, v in terms.items() if len(v.genes) <= max_genes}
    enriched_ids = set(terms.keys())

    # --- Anchor candidates ---
    candidates = []
    for go_id, term in terms.items():
        if go_id not in godag:
            continue
        if not (depth_range[0] <= term.depth <= depth_range[1]):
            continue
        enriched_desc = descendants_fn(go_id, godag) & enriched_ids
        if len(enriched_desc) >= min_children:
            candidates.append(
                {"go_id": go_id, "term": term, "depth": term.depth, "children": enriched_desc}
            )

    if priority_sort:
        # Process terms first (is_regulatory=0 < 1), then depth-descending within each group.
        # This lets "leukocyte migration" (d=4, non-regulatory) absorb
        # "regulation of leukocyte migration" (d=6, regulatory) before the
        # latter can lock itself in as an anchor.
        candidates.sort(
            key=lambda x: (_is_regulatory(x["term"].name), -x["depth"], x["term"].fdr)
        )
    else:
        # Production sort: most specific (deepest) first, then best FDR.
        candidates.sort(key=lambda x: (-x["depth"], x["term"].fdr))

    # --- Assign children to anchors (no overlap) ---
    assigned: set[str] = set()
    themes: list[HierarchicalTheme] = []

    for cand in candidates:
        anchor_id = cand["go_id"]
        if anchor_id in assigned:
            continue

        children = [
            terms[cid]
            for cid in cand["children"]
            if cid not in assigned and cid != anchor_id and cid in terms
        ]

        if len(children) >= min_children:
            children.sort(key=lambda x: x.fdr)
            themes.append(
                HierarchicalTheme(
                    anchor_term=cand["term"],
                    specific_terms=children,
                    anchor_confidence=_conf(cand["term"].fdr),
                )
            )
            assigned.add(anchor_id)
            for child in children:
                assigned.add(child.go_id)

    # --- Unassigned leaves → standalone themes ---
    leaves = _find_leaves(terms, godag, fdr_threshold, descendants_fn)
    leaves = _merge_identical_gene_sets(leaves, terms)
    for leaf_id in leaves:
        if leaf_id not in assigned and leaf_id in terms:
            leaf = terms[leaf_id]
            themes.append(
                HierarchicalTheme(
                    anchor_term=leaf,
                    specific_terms=[],
                    anchor_confidence=_conf(leaf.fdr),
                )
            )

    themes.sort(key=lambda x: x.anchor_term.fdr)
    return themes


# =============================================================================
# Load terms from enrichment JSON
# =============================================================================


def load_terms_from_json(
    data: dict, godag: GODag
) -> dict[str, EnrichedTerm]:
    """Reconstruct EnrichedTerm dict from stored leaves + theme anchor/specific terms."""
    terms: dict[str, EnrichedTerm] = {}

    def add(d: dict) -> None:
        go_id = d["go_id"]
        if go_id in terms or d["namespace"] != "biological_process":
            return
        depth = godag[go_id].depth if go_id in godag else d.get("depth", 0)
        terms[go_id] = EnrichedTerm(
            go_id=go_id,
            name=d["name"],
            namespace=d["namespace"],
            fdr=d["fdr"],
            fold_enrichment=d["fold_enrichment"],
            genes=frozenset(d["genes"]),
            depth=depth,
        )

    for leaf in data["enrichment_leaves"]:
        add(leaf)

    for theme in data["themes"]:
        add(theme["anchor_term"])
        for s in theme["specific_terms"]:
            add(s)

    return terms


# =============================================================================
# Reporting helpers
# =============================================================================


def summarise(label: str, themes: list[HierarchicalTheme], n_leaves: int) -> dict:
    n = len(themes)
    n_with = sum(1 for t in themes if t.specific_terms)
    n_solo = n - n_with
    genes = set()
    for t in themes:
        genes.update(t.all_genes)
    ratio = round(n_leaves / n, 2) if n else float("inf")

    print(f"\n{'='*62}")
    print(f"  {label}")
    print(f"{'='*62}")
    print(f"  Total themes:           {n:>4}")
    print(f"  With children:          {n_with:>4}")
    print(f"  Standalone:             {n_solo:>4}")
    print(f"  Leaves : themes ratio:  {ratio:>6.2f}  (lower = better compression)")
    print(f"  Unique genes covered:   {len(genes):>4}")

    return {
        "n_themes": n,
        "n_with_children": n_with,
        "n_standalone": n_solo,
        "leaves_per_theme": ratio,
        "genes_covered": len(genes),
    }


def show_cluster(label: str, themes: list[HierarchicalTheme], keyword: str) -> None:
    """Show all themes where anchor or any specific term contains keyword."""
    print(f"\n--- {label}: '{keyword}' cluster ---")
    relevant = [
        t for t in themes
        if keyword in t.anchor_term.name.lower()
        or any(keyword in s.name.lower() for s in t.specific_terms)
    ]
    if not relevant:
        print("  (none found)")
        return
    for t in relevant:
        tag = "[anchor]" if t.specific_terms else "[solo]  "
        print(f"  {tag} d={t.anchor_term.depth}  {t.anchor_term.name}")
        for s in t.specific_terms:
            if keyword in s.name.lower() or "regulation" in s.name.lower():
                print(f"           └─ d={s.depth}  {s.name}")


def show_regulation_merges(
    label: str,
    themes_baseline: list[HierarchicalTheme],
    themes_new: list[HierarchicalTheme],
) -> None:
    """Report 'regulation of X' standalones absorbed into X themes, and displaced anchors."""
    # Baseline: "regulation of X" terms that were standalone
    solo_reg = {
        t.anchor_term.go_id: t.anchor_term.name
        for t in themes_baseline
        if not t.specific_terms and "regulation of" in t.anchor_term.name.lower()
    }

    # New run: which of those are now children?
    now_child: dict[str, tuple[str, str]] = {}
    for t in themes_new:
        for s in t.specific_terms:
            if s.go_id in solo_reg:
                now_child[s.go_id] = (solo_reg[s.go_id], t.anchor_term.name)

    # Also: baseline anchors (with children) that are now children in new run
    # i.e. "regulation of X" that WAS an anchor, now absorbed under X
    base_anchors_reg = {
        t.anchor_term.go_id: t.anchor_term.name
        for t in themes_baseline
        if t.specific_terms and "regulation of" in t.anchor_term.name.lower()
    }
    displaced_anchors: dict[str, tuple[str, str]] = {}
    for t in themes_new:
        for s in t.specific_terms:
            if s.go_id in base_anchors_reg:
                displaced_anchors[s.go_id] = (base_anchors_reg[s.go_id], t.anchor_term.name)

    print(f"\n--- {label}: 'regulation of X' terms absorbed ---")
    print(f"  'regulation of' STANDALONES in baseline:      {len(solo_reg)}")
    print(f"  → now children (absorbed from standalone):    {len(now_child)}")
    print(f"  'regulation of' ANCHORS in baseline:          {len(base_anchors_reg)}")
    print(f"  → now children (displaced from anchor):       {len(displaced_anchors)}")

    if now_child or displaced_anchors:
        print()
        all_absorbed = {**{go_id: (n, a, "was standalone") for go_id, (n, a) in now_child.items()},
                        **{go_id: (n, a, "was anchor") for go_id, (n, a) in displaced_anchors.items()}}
        for go_id, (reg_name, anchor_name, was) in sorted(all_absorbed.items(), key=lambda x: x[1][1]):
            print(f"  [{was:12}]  {reg_name[:48]:<48}  →  {anchor_name[:35]}")


# =============================================================================
# V3: Post-hoc merge
# =============================================================================


def post_hoc_merge(
    themes: list[HierarchicalTheme],
    godag: GODag,
) -> tuple[list[HierarchicalTheme], list[tuple[str, str, str]]]:
    """Merge 'regulation of X' themes into their 'X' themes using ontology edges.

    Algorithm
    ---------
    1. For every theme anchor, check if it has a `regulates/*` relationship
       in the ontology pointing at another theme anchor.
    2. If so, absorb the regulatory theme (its anchor + all its specific_terms)
       as additional specific_terms of the process theme. Multiple regulatory
       themes can merge into the same process theme in one pass.
    3. All other themes are returned unchanged.

    Returns
    -------
    merged_themes : list of HierarchicalTheme
        Full theme list after merging (len ≤ len(themes)).
    merge_log : list of (regulatory_name, process_name, "anchor"|"solo")
        One entry per regulatory theme absorbed.
    """
    by_anchor = {t.anchor_term.go_id: t for t in themes}

    # Discover merge pairs: regulatory_go_id → target_go_id
    # A term can only point to one primary target (take first regulates hit).
    to_absorb: dict[str, str] = {}  # reg_go_id → target_go_id
    for go_id in by_anchor:
        dag_term = godag.get(go_id)
        if not dag_term or not hasattr(dag_term, "relationship") or not dag_term.relationship:
            continue
        for rel_type, rel_targets in dag_term.relationship.items():
            if rel_type in _REGULATES_RELS:
                for target in rel_targets:
                    if target.id in by_anchor and target.id != go_id:
                        to_absorb[go_id] = target.id
                        break  # first valid target wins
                if go_id in to_absorb:
                    break

    # Group by target: which regulatory themes merge into each process theme
    from collections import defaultdict
    merges_into: dict[str, list[str]] = defaultdict(list)
    for reg_id, tgt_id in to_absorb.items():
        merges_into[tgt_id].append(reg_id)

    # Build merged theme list
    absorbed: set[str] = set(to_absorb.keys())
    merge_log: list[tuple[str, str, str]] = []
    merged_themes: list[HierarchicalTheme] = []

    for go_id, theme in by_anchor.items():
        if go_id in absorbed:
            continue  # this regulatory theme is being merged elsewhere

        extra: list[EnrichedTerm] = []
        for reg_id in merges_into.get(go_id, []):
            reg_theme = by_anchor[reg_id]
            was = "anchor" if reg_theme.specific_terms else "solo"
            merge_log.append((reg_theme.anchor_term.name, theme.anchor_term.name, was))
            # Flatten: reg anchor becomes a child, its children also join
            extra.append(reg_theme.anchor_term)
            extra.extend(reg_theme.specific_terms)

        if extra:
            extra.sort(key=lambda x: x.fdr)
            merged_themes.append(
                HierarchicalTheme(
                    anchor_term=theme.anchor_term,
                    specific_terms=list(theme.specific_terms) + extra,
                    anchor_confidence=theme.anchor_confidence,
                )
            )
        else:
            merged_themes.append(theme)

    merged_themes.sort(key=lambda x: x.anchor_term.fdr)
    return merged_themes, merge_log


def show_merge_log(merge_log: list[tuple[str, str, str]]) -> None:
    print(f"\n--- POST-HOC MERGE: regulatory themes absorbed ({len(merge_log)} merges) ---")
    # Group by target for cleaner display
    by_target: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for reg_name, tgt_name, was in merge_log:
        by_target[tgt_name].append((reg_name, was))
    for tgt_name in sorted(by_target):
        print(f"  [{tgt_name[:45]}]")
        for reg_name, was in sorted(by_target[tgt_name]):
            print(f"    ← [{was:6}]  {reg_name}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("Loading GO DAG (with relationship attrs)...")
    godag = GODag(
        "reference_data/go-basic.obo",
        optional_attrs={"relationship"},
        prt=None,
    )

    print("Loading enrichment JSON...")
    with open("results/hm_inflam_enrichment.json") as f:
        data = json.load(f)

    terms = load_terms_from_json(data, godag)
    n_leaves = data["metadata"]["enrichment_leaves_count"]
    print(
        f"Reconstructed {len(terms)} BP terms "
        f"(of {data['metadata']['total_enriched_terms']} total enriched in production run)"
    )
    print(f"Production: {data['metadata']['themes_count']} themes from {n_leaves} leaves")

    # --- Run three variants ---
    print("\nRunning BASELINE (is_a + part_of, depth-first sort)...")
    themes_base = build_themes(
        terms, godag, get_descendants_baseline, priority_sort=False
    )

    print("Running REG-ONLY (+ regulates, same sort — v1)...")
    themes_reg = build_themes(
        terms, godag, get_descendants_with_regulates, priority_sort=False
    )

    print("Running REG+PRIO (+ regulates, process-first sort — v2)...")
    themes_reg_prio = build_themes(
        terms, godag, get_descendants_with_regulates, priority_sort=True
    )

    print("Running POST-HOC MERGE (baseline + ontology-guided regulatory merge — v3)...")
    themes_posthoc, merge_log = post_hoc_merge(themes_base, godag)

    # --- Summary statistics ---
    stats_base  = summarise("BASELINE    (is_a + part_of,  depth-first sort)", themes_base, n_leaves)
    stats_reg   = summarise("REG-ONLY    (+ regulates,     depth-first sort) [v1]", themes_reg, n_leaves)
    stats_prio  = summarise("REG+PRIO    (+ regulates,  process-first sort) [v2]", themes_reg_prio, n_leaves)
    stats_posth = summarise("POST-HOC    (baseline + ontology merge)         [v3]", themes_posthoc, n_leaves)

    print(f"\n  REG-ONLY   reduction vs baseline:  {stats_base['n_themes'] - stats_reg['n_themes']:+d}")
    print(f"  REG+PRIO   reduction vs baseline:  {stats_base['n_themes'] - stats_prio['n_themes']:+d}")
    print(f"  POST-HOC   reduction vs baseline:  {stats_base['n_themes'] - stats_posth['n_themes']:+d}")

    # --- Leukocyte migration cluster (the key case) ---
    show_cluster("BASELINE ", themes_base,     "leukocyte migrat")
    show_cluster("REG-ONLY ", themes_reg,      "leukocyte migrat")
    show_cluster("REG+PRIO ", themes_reg_prio, "leukocyte migrat")
    show_cluster("POST-HOC ", themes_posthoc,  "leukocyte migrat")

    # --- Regulation absorption detail ---
    show_regulation_merges("REG-ONLY  vs BASELINE", themes_base, themes_reg)
    show_regulation_merges("REG+PRIO  vs BASELINE", themes_base, themes_reg_prio)
    show_regulation_merges("POST-HOC  vs BASELINE", themes_base, themes_posthoc)

    # --- Post-hoc merge log ---
    show_merge_log(merge_log)

    # --- Collateral: what did the priority sort displace? ---
    # Show any themes that gained extra children in REG+PRIO vs REG-ONLY
    reg_by_id   = {t.anchor_term.go_id: t for t in themes_reg}
    prio_by_id  = {t.anchor_term.go_id: t for t in themes_reg_prio}
    print(f"\n--- Anchors that gained regulatory children (REG+PRIO vs REG-ONLY) ---")
    gained = []
    for go_id, t_prio in prio_by_id.items():
        t_reg = reg_by_id.get(go_id)
        n_before = len(t_reg.specific_terms) if t_reg else 0
        n_after = len(t_prio.specific_terms)
        if n_after > n_before:
            gained.append((t_prio.anchor_term.name, n_before, n_after, t_prio.specific_terms))
    gained.sort(key=lambda x: -(x[2] - x[1]))
    for name, n_bef, n_aft, children in gained[:15]:
        print(f"  {name[:55]:<55}  {n_bef} → {n_aft} children")
        new_children = children[n_bef:] if n_bef < n_aft else children
        for c in new_children[:6]:
            print(f"    + d={c.depth}  {c.name}")

    # --- Save results ---
    out_path = Path("results/12_regulates_anchor_comparison.json")
    out_path.write_text(
        json.dumps(
            {
                "note": (
                    f"{len(terms)} terms reconstructed from JSON "
                    f"(not full {data['metadata']['total_enriched_terms']}). "
                    "Anchor candidate selection is approximate; "
                    "regulates grouping effect is faithfully demonstrated."
                ),
                "n_leaves": n_leaves,
                "baseline":   stats_base,
                "reg_only":   stats_reg,
                "reg_prio":   stats_prio,
                "post_hoc":   stats_posth,
                "reduction_reg_only_vs_baseline":   stats_base["n_themes"] - stats_reg["n_themes"],
                "reduction_reg_prio_vs_baseline":   stats_base["n_themes"] - stats_prio["n_themes"],
                "reduction_posthoc_vs_baseline":    stats_base["n_themes"] - stats_posth["n_themes"],
                "posthoc_n_merges":                 len(merge_log),
            },
            indent=2,
        )
    )
    print(f"\nSaved to {out_path}")
