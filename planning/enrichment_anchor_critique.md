# Enrichment Anchor Algorithm — Critique & Design Notes

**Date**: 2026-03-03
**Dataset analysed**: `results/hm_inflam_enrichment.json` (200 human inflammation genes, MSigDB Hallmark Inflammatory Response)

---

## 1. Coverage: What fraction of genes end up in the summary?

**92% (184/200)** input genes appear in at least one theme (via the `all_genes` field on each theme).

The 16 missing genes are likely: annotated only to terms filtered out by `max_genes=30`; or annotated only to terms with a single enriched descendant that became a standalone theme with zero `all_genes` (theme 135, "RNA processing", is an example); or unannotated.

However, the 92% figure is somewhat misleading. Hub gene counts reveal the real picture: IL6 appears in **65/223 themes (29%)**, IL1B in 57, EDN1 in 57. The same genes are heavily recycled across semantically redundant themes — high coverage does not mean high information density.

---

## 2. Compression failure — the core structural problem

| Layer | Count | Ratio to previous |
|---|---|---|
| Total enriched terms | 1042 | — |
| Enrichment leaves | 253 | 24% of enriched terms |
| Themes | 223 | **88% of leaves** |

The leaf computation does useful work (reduces 1042 → 253). But the theme-building barely improves on the leaves: **themes:leaves ratio = 0.88**.

- **125/223 themes (56%) are standalone** — leaves that couldn't be grouped under any anchor
- **51/125 standalone themes have ≤3 genes** — these are small, weakly enriched, biologically marginal terms
- The `min_children=2` threshold creates a hard cliff: any enriched term with fewer than 2 siblings that share an anchor becomes a standalone theme

The output is essentially the leaf set with thin hierarchical wrapping on top. A user is given 223 "themes" when arguably 30–50 would tell the full biological story.

---

## 3. Is the bloat example-specific?

Almost certainly yes, and significantly so. The MSigDB Hallmark Inflammatory Response set is a **worst-case scenario** for GO term bloat:

1. **Dense annotation domain** — the GO immune branch is the most annotated domain. Curated inflammation sets select for genes known to be well-annotated, maximising redundant term hits.
2. **Regulatory proliferation** — GO explicitly represents positive/negative/canonical variants of every immune process: every process generates ~3–5 enriched terms.
3. **Pleiotropy of immune signalling** — CCL5, IL6, IL1B are annotated to hundreds of GO terms individually.

A metabolic, kinase, or stress-response gene set of similar size would likely show far fewer enriched terms (~200–300 rather than 1042). **Empirical test needed**: run the algorithm against `hallmark_oxidative_phosphorylation.txt` (200 genes, Ring 0 benchmark) and compare the themes:leaves ratio.

---

## 4. The anchor redundancy problem

Looking at the top themes reveals a clear failure mode. Themes 2, 4, 5, 7, 13, 18, 23, 31, and 38 are all variants of leukocyte migration/chemotaxis, each appearing as a separate top-level anchor:

| Theme | GO term | FDR |
|---|---|---|
| 2 | regulation of leukocyte migration | 2.32e-20 |
| 4 | leukocyte migration | 2.08e-17 |
| 5 | positive regulation of leukocyte migration | 6.67e-17 |
| 7 | positive regulation of leukocyte cell-cell adhesion | 5.54e-16 |
| 13 | leukocyte chemotaxis | 7.66e-14 |
| 18 | regulation of mononuclear cell migration | 1.46e-12 |
| 23 | regulation of leukocyte chemotaxis | 3.68e-11 |

**Root cause**: "regulation of leukocyte migration" and "leukocyte migration" sit in **entirely different `is_a` subtrees**. In GO OBO:

```
GO:0002685  regulation of leukocyte migration
    is_a:  regulation of cell migration
    is_a:  regulation of immune system process
    relationship: regulates GO:0050900 ! leukocyte migration
```

The `regulates` edge connects them, but the algorithm traverses only `is_a` and `part_of`. As a result, each becomes its own independent anchor with its own subtree of children. The gene sets overlap heavily — these themes are telling the same biology from different angles — but the algorithm has no mechanism to group them.

---

## 5. Comparison with other approaches

The dominant approach in the field is **semantic similarity-based clustering** rather than hierarchical-position-based grouping.

### REVIGO (Supek et al. 2011)

Computes all-vs-all semantic similarity using the **SimRel / Schlicker measure** (default):

```
sim(A, B) = [2 × IC(MICA) / (IC(A) + IC(B))] × (1 - p(MICA))
```

Where IC(t) = -log₂(p(t)) and p(t) = fraction of background genes annotated to t or descendants. The `(1 - p(MICA))` term penalises if the Most Informative Common Ancestor is a general term — preventing superficially high scores when two terms share only a broad ancestor.

REVIGO greedy algorithm: sort enriched terms by p-value; assign each term a "dispensability" = max SimRel similarity to any already-chosen representative; suppress if dispensability > threshold (0.4–0.9). Output: 10–30 representative terms from hundreds of enriched terms.

Other IC-based measures supported: **Resnik** (`sim = IC(MICA)`), **Lin** (`sim = 2×IC(MICA)/(IC(A)+IC(B))`), **Jiang & Conrath** (distance-based).

### rrvgo (Sayols 2023)

Wraps GOSemSim. Computes full pairwise similarity matrix → hierarchical clustering on `(1 - similarity)` → picks lowest-FDR term per cluster. Supports all IC-based measures plus:

**Wang (2007)** — graph-structural, no corpus required:
- Each term A gets a semantic value vector S_A(t) for every ancestor t, propagated from S_A(A) = 1.0 upward with edge-type weights (is_a: 0.8, part_of: 0.6)
- `sim(A, B) = Σ(t in ancestors(A) ∩ B) [S_A(t) + S_B(t)] / (ΣS_A + ΣS_B)`
- Used by clusterProfiler `simplify()` as default

### Critical difference from our approach

REVIGO/rrvgo measure **similarity between the enriched terms themselves**, regardless of their position in the DAG. This handles cross-branch redundancy. Our approach uses **hierarchical position** — terms can only be grouped if they share an ancestor in the depth 4–7 range, which means:

- Cross-branch redundancy (the leukocyte migration family) is completely invisible to the algorithm
- The "regulation of X" pattern, mediated by `regulates` not `is_a`, can never be collapsed

### The complementarity exception

Not all cross-branch similarity represents redundancy. **GO:0070098** (chemokine-mediated signalling) and **GO:0030595** (leukocyte chemotaxis) share only "cellular process" as their MICA — near-zero SimRel score. REVIGO would correctly not merge them. These are causally complementary: the signalling pathway is the mechanism that drives the chemotaxis output. Having both themes enables the narrative: *"CCL5/CCR7 activate downstream GPCR cascades [signalling theme] which direct leukocyte migration toward inflammatory sites [chemotaxis theme]."* This is exactly the kind of biological story the LLM explanation layer is designed to tell.

The boundary to maintain: merge `is_a`-adjacent regulatory variants ("regulation of X" / "positive regulation of X"); preserve causally distinct processes in different ontological branches.

---

## 6. Depth as a proxy for Information Content

The current anchor selection requires depth 4–7. This is a structural proxy for term specificity. The real criterion should be **Information Content (IC)**:

```
IC(t) = -log₂(p(t))     where p(t) = annotated_genes(t) / total_genes
```

Depth is a poor proxy for IC in the immune branch. A term at depth 5–6 in the dense immune branch has many genes annotated to it → low IC (it's too general). The same depth in a sparse branch (e.g., metal ion homeostasis) has high IC. Selecting anchors by IC range rather than depth range would produce more semantically appropriate groupings regardless of branch density.

---

## 7. Embedding-based similarity (modern alternative)

Beyond IC-based measures, GO term *text* can be embedded using sentence transformers. The term name + definition captures semantic content that the DAG structure may miss.

**Practical implementation:**
1. Retrieve GO term definition from OBO file for each enriched term
2. Embed `"{term_name}: {definition}"` using a sentence transformer (e.g., `all-MiniLM-L6-v2` or a biomedical model like `BiomedNLP-BiomedBERT-large`)
3. Compute cosine similarity matrix between anchor terms
4. Merge/suppress anchors with similarity > threshold (e.g., 0.85)

**Advantages**: Captures cross-branch semantic redundancy that MICA-based measures miss; no annotation corpus dependency; handles synonymous GO terms naturally.

**Limitations**: General models may conflate "positive regulation" and "negative regulation" of the same process (both about regulation, but biologically opposite). Best used as a *post-filter* on existing depth-anchor groupings rather than as a replacement.

---

## 8. The `regulates` proposal — a clean architectural split

The core insight from examining the GO structure: `is_a`/`part_of` and `regulates` serve different ontological roles and should be used at different layers of the algorithm.

### Proposed split

| Layer | Relationships used | Rationale |
|---|---|---|
| **Enrichment leaves** | `is_a` + `part_of` only | Leaves = most specific in the ontological hierarchy. `regulates` would blur what "specific" means — "regulation of leukocyte migration" is not a more specific *kind* of "leukocyte migration" |
| **Anchor grouping** | `is_a` + `part_of` + **`regulates`** | Process term absorbs its regulatory variants, telling one coherent biological story |

### What this achieves for the leukocyte migration cluster

Instead of 3+ separate themes:
```
Theme: regulation of leukocyte migration         ← separate anchor
Theme: leukocyte migration                        ← separate anchor
Theme: positive regulation of leukocyte migration ← separate anchor
```

One coherent theme:
```
Theme: leukocyte migration
  ├── [is_a]      myeloid leukocyte migration
  ├── [is_a]      mononuclear cell migration
  ├── [is_a]      leukocyte migration involved in inflammatory response
  ├── [regulates] regulation of leukocyte migration
  └── [regulates] positive/negative regulation of leukocyte migration
```

Narrative: "these genes drive leukocyte migration; these modulate it" — one coherent story rather than three redundant summaries.

### Implementation

In `utils/go_hierarchy.py`, `get_all_descendants` already has a reverse-scan loop for `part_of`:

```python
# Existing part_of reverse scan:
for term_id, dag_term in godag.items():
    if hasattr(dag_term, "relationship") and dag_term.relationship:
        for rel_type, rel_terms in dag_term.relationship.items():
            if rel_type == "part_of":   # extend to also include regulates here
```

Extending `rel_type` checks to `regulates`, `positively_regulates`, `negatively_regulates` is the minimal change. The assignment priority rule should remain: is_a/part_of grouping takes precedence; `regulates`-linked absorption is a second pass to avoid double-assignment.

---

## 9. Pilot results — `regulates` grouping (exploration/12_regulates_anchor.py)

Three approaches to the `regulates` merge were tested against the inflammation dataset using ~570 terms reconstructed from the existing enrichment JSON (not a full re-run). Results are approximate but directionally reliable.

| Variant | Themes | vs Baseline | Leukocyte migration cluster |
|---|---|---|---|
| BASELINE (is_a + part_of, current production) | 224 | — | 3 separate anchors |
| REG-ONLY (+ regulates in descendant traversal, same sort) | 214 | −10 | 3 separate anchors (unchanged) |
| REG+PRIO (+ regulates + process-first sort) | 225 | −1 (worse) | 1 merged anchor |
| **POST-HOC** (baseline + ontology-guided merge pass) | **208** | **−16** | **1 merged anchor** |

**Key finding**: The `regulates` extension is necessary but not sufficient when used inside the greedy anchor algorithm, because regulatory terms are deeper and therefore processed first — they lock in as their own anchors before the process term can absorb them. Three approaches were tried:

**V1 — REG-ONLY**: Extending `get_all_descendants` to follow `regulates`/`positively_regulates`/`negatively_regulates` gives −10 themes via unrelated paths, but fails to merge the leukocyte migration cluster because "regulation of leukocyte migration" (d=6) is still processed as an anchor before "leukocyte migration" (d=4).

**V2 — REG+PRIO**: Changing the sort key to `(is_regulatory, -depth, fdr)` — process terms before regulatory terms regardless of depth — successfully merges the leukocyte migration cluster, but globally disrupts existing good groupings (regulatory terms at d=5 are now shunted after process terms at d=4, breaking previously valid sub-clusters). Net result marginally worse than baseline.

**V3 — POST-HOC**: Run the baseline algorithm unchanged, then do a single ontology-guided merge pass: for each regulatory theme anchor with a `regulates` edge pointing at another theme anchor, absorb the regulatory theme (its anchor term + all its specific_terms) as additional specific_terms of the process theme. Only 16 valid merge pairs were found (out of ~122 regulatory themes), but these 16 cover the most important biological cases:

- `leukocyte migration` absorbs both `regulation of leukocyte migration` and `positive regulation of leukocyte migration`
- `leukocyte chemotaxis` absorbs `regulation of leukocyte chemotaxis`
- `T cell activation` absorbs `regulation of T cell activation`
- `lymphocyte activation` absorbs `positive regulation of lymphocyte activation`
- `hemopoiesis`, `endocytosis`, `metal ion transport`, `monoatomic ion transport`, `hormone secretion`, `lymphocyte proliferation`, `extrinsic apoptotic signaling pathway` — each absorbs their regulation counterpart

The other ~106 regulatory themes have no matching process theme anchor (the process term either didn't pass enrichment, or was too general/specific to become an anchor itself) and are left unchanged.

**Coverage is preserved**: 184/200 genes covered in both baseline and post-hoc (genes_covered unchanged).

**Limitation of this pilot**: The 570 reconstructed terms represent the terms that survived into the final output, not the full 1042 enriched terms used in production. The 16 merge pairs might differ slightly in a full re-run. The direction and the mechanism are reliable; the exact count is approximate.

---

## 10. Priority-ordered next steps

1. **Test on non-immune gene set** — run against `hallmark_oxidative_phosphorylation.txt` or `hallmark_dna_repair.txt` to quantify how much bloat is dataset-specific vs. algorithmic
2. **Implement post-hoc merge (v3) in production** — add a `post_hoc_regulatory_merge(themes, godag)` step at the end of `build_depth_anchor_themes` in `go_hierarchy.py`; the `post_hoc_merge` function in `exploration/12_regulates_anchor.py` is the reference implementation
3. **Raise `min_children` to 3–4** — reduces the standalone theme flood (51 themes with ≤3 genes currently)
4. **IC-based anchor selection** — replace `depth_range=(4,7)` with IC range to avoid selecting overly general anchors in dense branches
5. **Semantic similarity post-filter on anchors** — catch residual cross-branch redundancy after the above; Wang or SimRel, or embedding-based for the "regulation of X" family
