# Real Data Validation — Theme Algorithm Benchmark

Track enrichment algorithm behaviour across real experimental gene sets.
Contrasts with Hallmark synthetic sets used in algorithm development.

---

## Motivation

MSigDB Hallmark gene sets are atypically dense for GO enrichment (~5× more
enriched terms per gene than typical experimental data). Algorithm problems
observed on Hallmark sets (e.g. 224 themes from 200 genes) may not reflect
real-world use cases. This doc tracks behaviour on experimentally-derived DEG
lists with published GO analysis for comparison.

**Key metrics per dataset:**
- Terms/gene ratio (enrichment density)
- Leaf count (algorithm input size)
- Topologically isolated leaves (irreducible standalones)
- Stranded leaves (had ancestors, but ungroupable)
- MRCEA-A / MRCEA-B L/T ratio vs production baseline
- Gene coverage at top-20 / top-30 theme cutoff
- Qualitative match to published GO/pathway results

---

## Datasets

### 1. Himes et al. 2014 — Airway smooth muscle, dexamethasone (GSE52778)

**Source:** PMID 24926665 / PMC4057123
**GEO:** GSE52778
**Design:** Dexamethasone-treated vs untreated human airway smooth muscle cells (4 cell lines)
**DEG count:** 314 unique gene symbols (FDR < 0.05, DESeq2)
**Gene list:** `input_data/benchmark_sets/experimental/himes2014_dex_airway_DEGs.txt`
**Published comparison:** Supplement 4 — DAVID GO cluster analysis

**Enrichment stats (FDR < 0.05, goatools):**

| Metric | Value |
|---|---|
| Input genes | 314 |
| Genes with annotations | 288 |
| Total enriched terms | 80 |
| Terms/gene | 0.28 |
| Enriched leaves | 22 |

**Theme algorithm results:**

| Algorithm | Themes | Standalone | L/T | Groups formed |
|---|---|---|---|---|
| Production (depth-anchor 4–7) | 22 | 19 | 1.00 | 3 small |
| MRCEA-A (highest-IC path) | 22 | 22 | 1.00 | 0 |
| MRCEA-B (all-paths BFS) | 22 | 22 | 1.00 | 0 |

**Leaf structure:**
- 13/22 topologically isolated (no enriched ancestor in DAG)
- 9/22 stranded (had IC≥4–10 ancestors, none shared with other leaves)
- 0 secondary memberships

**Gene coverage at theme cutoffs:**

| Top-N | Genes covered | % of 288 annotated |
|---|---|---|
| 10 | 102 | 35.4% |
| 20 | 125 | 43.4% |
| 24 (all) | 141 | 49.0% |

Note: 49% ceiling reflects genes not enriched at FDR<0.05, not a grouping failure.

**Qualitative match to published DAVID clusters:**

| DAVID cluster | Score | Our pipeline |
|---|---|---|
| ECM / glycoprotein / secreted | 4.72 | Theme 2: extracellular matrix ✓ |
| Vasculature / blood vessel morphogenesis | 3.38 | Theme 9: branching in blood vessel morphogenesis ✓ |
| Response to nutrient / extracellular stimulus | 3.13 | Themes 11, 18 ✓ |
| Hormone / steroid / glucocorticoid response | 3.02 | Theme 1: cellular response to hormone stimulus ✓ (most significant, FDR 8e-6) |
| Rhythmic process / circadian (PER1, FKBP5) | 2.42 | Not captured (too sparse for a theme) |
| Regulation of cell migration / locomotion | 2.28 | Themes 3, 7, 22 ✓ |

**Assessment:** Good match to published results for top biology. 22 themes fit
well within the 30-theme cap with 100% theme coverage. The pipeline is
appropriate for this enrichment density.

---

### 2. Hoang et al. 2019 — NAFLD liver (Sci Rep)

**Source:** PMID 31467298 / PMC6715650
**GEO:** Not directly; gene list from supplement 5 (Bayesian network analysis)
**Design:** Liver biopsies across NAFLD spectrum (healthy → steatosis → NASH → cirrhosis)
**Gene list:** `input_data/benchmark_sets/experimental/hoang2019_nafld_DEGs.txt`
**Published comparison:** Supplement 3 (C_1: RTK/Rho GTPase signalling), Supplement 4 (C_3: Cell cycle/proteasome)

**Enrichment stats (FDR < 0.05, goatools):**

| Metric | Value |
|---|---|
| Input genes | 637 (Bayesian network genes, posterior_prob > 0.95) |
| Genes with annotations | 623 |
| Total enriched terms | 2060 |
| Terms/gene | 3.23 |
| Enrichment leaves | 477 |

Note: Gene communities from the paper (Louvain clustering):
- C_1 (150): RTK/Rho signalling — SRC, CDC42, RAC1, RHOA, EGFR
- C_2 (109): Transcriptional regulation — JUN, CREBBP, AR, SIRT1, SMAD4
- C_3 (152): Cell cycle/proteasome — CDK1, CDKN1A, PSMx subunits
- C_8 (51): Chaperones/proteostasis — HSPA8, HSP90AA1, VCP
- C_11 (26): Immune/chemokine — CCL2, CXCR4, CCR5

**Theme algorithm results:**

| Algorithm | Themes | Standalone | L/T |
|---|---|---|---|
| Production (depth-anchor 4–7) | 420 | 254 | 1.14 |
| MRCEA-A (highest-IC path) | 359 | 294 | 1.33 |
| MRCEA-B (all-paths BFS) | 331 | 264 | **1.44** |

332/477 leaves have enriched ancestors — density drives groupability (cf. 9/22 for Himes).
119 stranded leaves; 14 absorbable via full DAG.

**Gene coverage at theme cutoffs:**

| Top-N | Genes covered | % of 623 annotated | Anchor FDR at position N |
|---|---|---|---|
| 10 | 146 | 23.4% | 4.7e-13 |
| 20 | 233 | 37.4% | 3.6e-11 |
| 30 (cap) | 270 | 43.3% | 6.5e-10 |
| 50 | 381 | 61.2% | 1.7e-07 |
| 100 | 486 | 78.0% | 8.7e-06 |
| 200 | 553 | 88.8% | 4.3e-04 |
| 300 | 587 | 94.2% | 3.9e-03 |
| All 582 | 605 | 97.1% | ~0.05 |

**Genes exclusively invisible at top-30 cap: 335 (54% of annotated)**
Dropped themes at position 31+ still highly significant (FDR 7e-10 at rank 31).

**Assessment:** Dense real dataset — 3.23 terms/gene is ~12× Himes, within range of Hallmark sets.
The 30-theme cap causes severe coverage loss in real dense disease transcriptomics.
MRCEA-B provides meaningful compression (1.44 L/T) consistent with Hallmark results.

#### 2a. NAFLD C_1 community — RTK/Rho GTPase (150 genes)

**Gene list:** `input_data/benchmark_sets/experimental/hoang2019_nafld_C1_RTK_Rho.txt`

| Metric | Value |
|---|---|
| Terms/gene | 3.10 |
| Enrichment leaves | 232 |
| Themes | 207 |
| Top-30 gene coverage | 85% (126/149) |

Top GO themes: *actin cytoskeleton organization* (FDR 1.3e-19), *lamellipodium*, *cell-cell junction*, *positive regulation of locomotion*

Published Reactome (Supplement 3): Signaling by RTKs, Rho GTPase cycle, FCGR phagocytosis, Axon guidance

**Match:** Conceptually aligned — GO captures the cytoskeletal/motility effectors of Rho GTPase signalling (what the pathway *does*) rather than naming the pathway. Different vocabulary, same biology.

#### 2b. NAFLD C_3 community — Cell cycle / proteasome (152 genes)

**Gene list:** `input_data/benchmark_sets/experimental/hoang2019_nafld_C3_cellcycle.txt`

| Metric | Value |
|---|---|
| Terms/gene | 2.18 |
| Enrichment leaves | 147 |
| Themes | 139 |
| Top-30 gene coverage | 80% (118/148) |

Top GO themes: *proteasome complex* (FDR 3.1e-42), *mitotic cell cycle phase transition*, *proteasome storage granule*, *regulation of cell cycle G1/S phase transition*, *cyclin-dependent protein kinase holoenzyme complex*

Published Reactome (Supplement 4): Cell Cycle / Mitotic, Cell Cycle Checkpoints, DNA Replication, Generic Transcription

**Match: Excellent.** Proteasome dominates because C_3 contains all PSMx subunits. Cell cycle progression and CDK regulation captured precisely. Note: individual coherent communities (150 genes) show better top-30 coverage (80–85%) than the mixed 637-gene list (43%), confirming that the long-tail problem scales with signal heterogeneity.

---

### 3. Kaizer et al. 2007 — Type 1 diabetes, peripheral blood (GSE9006)

**Source:** PMID 17595242
**GEO:** GSE9006
**Design:** PBMCs, new-onset T1D vs healthy controls and T2DM (children)
**Status:** Original paper not open access. Li et al. 2019 reanalysis (PMC6601337)
  only reports 44 DEGs — too sparse for meaningful validation. Gene list
  to be sourced from user or alternative dataset.

---

### 4. Labadorf et al. 2015 — Huntington's disease brain (GSE64810)

**Source:** PMID 26636579 / PMC4670106
**GEO:** GSE64810
**Design:** Post-mortem prefrontal cortex, HD (n=20) vs neurologically normal controls (n=49)
**Notes:** 5480 DEGs (19% of detected genes) — would be the densest real dataset tested.
  Expected to show even more severe top-30 coverage collapse than NAFLD.
  Supplement gene list not accessible via PMC tool. Gene list to be sourced from user or GEO.

---

## Cross-dataset summary

| Dataset | Type | Terms/gene | Leaves | L/T (prod) | L/T (MRCEA-B) | Genes lost at top-30 |
|---|---|---|---|---|---|---|
| Himes 2014 airway | Real, sparse | 0.28 | 22 | 1.00 | 1.00 | 0 (all 24 fit) |
| NAFLD C_1 RTK/Rho | Real, coherent community | 3.10 | 232 | — | — | 15% |
| NAFLD C_3 cell cycle | Real, coherent community | 2.18 | 147 | — | — | 20% |
| Hoang 2019 NAFLD (full) | **Real, mixed signal** | 3.23 | 477 | 1.14 | **1.44** | **54%** |
| hm_inflam (synthetic) | Synthetic | 5.22 | 50 | 1.00 | 1.46 | 23% |
| Kaizer 2007 T1D | Real | — | — | — | — | — |
| Labadorf 2015 HD | Real | — | — | — | — | — |

---

## Conclusions (updated 2026-03-13)

1. **The long-tail coverage problem is real in experimental data** — NAFLD (3.23 terms/gene)
   shows 54% gene loss at top-30, with dropped themes still FDR<7e-10. This is NOT a
   synthetic-dataset artifact.

2. **Enrichment density is the key variable** — Himes (0.28 terms/gene) fits in 24 themes;
   NAFLD (3.23) generates 582 themes. The 30-theme cap is appropriate for sparse datasets
   but severely inadequate for dense disease transcriptomics.

3. **MRCEA-B provides consistent compression when density is sufficient** — L/T 1.44 for
   NAFLD (477 leaves, 332 with ancestors) vs 1.00 for Himes (22 leaves, 9 with ancestors).
   The improvement scales with the fraction of leaves that have shared enriched ancestors.

4. **Coverage-driven theme selection is needed** — FDR-rank cutoff silently drops
   highly significant biology. For dense datasets, need coverage-aware selection
   (see planning/enrichment_anchor_critique.md, Section 12).

5. **More real data needed** — Labadorf HD (5480 DEGs) would likely be even more extreme
   than NAFLD. Two datasets sampled so far span the sparse–dense range; need 1–2 more
   to establish typical distribution.
