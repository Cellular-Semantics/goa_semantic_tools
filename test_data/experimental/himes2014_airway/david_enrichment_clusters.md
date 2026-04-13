# DAVID GO Enrichment Results — Himes et al. 2014

**Source**: Himes et al. 2014, PMID: 24926665 (PMC4057123)
**Dataset**: GSE52778 — dexamethasone-treated human airway smooth muscle cells
**Tool**: DAVID functional annotation clustering (published in paper Supplement 4)
**Input**: 316 DEGs (BH-corrected p<0.05, Cufflinks/Cuffdiff)

---

## Annotation Clusters (top 10 by enrichment score)

DAVID clusters GO terms by the overlap of their associated gene lists (kappa statistics).
Enrichment score = geometric mean of member term p-values (–log scale).

| Cluster | Score | Representative terms | Key genes |
|---------|-------|---------------------|-----------|
| 1 | 4.72 | extracellular matrix; glycoprotein; secreted; signal; disulphide bond | COL4A1, ADAMTS1, ADAMTS5, ADAMTS14, FBN2, SERPINA3 |
| 2 | 3.38 | vasculature development; blood vessel morphogenesis; tube morphogenesis | VEGFA, DLL4, COL4A1, TGFBR2 |
| 3 | 3.15 | blood circulation; cardiovascular system development; heart development | VEGFA, TGFBR2, SOX9, DLL4 |
| 4 | 3.13 | response to nutrient; response to extracellular stimulus; response to alcohol | ACSL1, IRS2, DUSP1, FOXO1 |
| 5 | 3.06 | steroid metabolic process; lipid metabolic process; monocarboxylic acid metabolic process | ACSL1, HSD11B1, PDK4, NR4A3 |
| 6 | 3.02 | response to organic substance; response to hormone stimulus; response to steroid hormone; response to glucocorticoid | FKBP5, DUSP1, TSC22D3, KLF15, MAOA, SERPINA3 |
| 7 | 2.72 | negative regulation of cell proliferation; apoptosis | CDKN2B, FOXO3, CITED2, GDF15 |
| 8 | 2.42 | rhythmic process; female gonad development; ovulation cycle; reproductive process | PER1, FKBP5, NR4A3, ACSL1 |
| 9 | 2.38 | negative regulation of cell migration; cell adhesion; cytoskeleton organisation | DUSP1, FOXO3, ADAMTS1, DAPK2 |
| 10 | 2.28 | regulation of cell migration; regulation of locomotion; regulation of cell motility | EPHB2, EPHB3, VEGFA, ADAMTS1, DAAM2 |

---

## Notes for Comparison

- **Cluster 1 (ECM)** = our Theme 2 (extracellular matrix, FDR 5e-5) ✅
- **Cluster 2/3 (vascular)** = our Theme 9 (branching in blood vessel morphogenesis, FDR 1.2e-2) ✅ (partially — smaller than DAVID cluster)
- **Cluster 4 (nutrient/extracellular)** = our Theme 18 (response to nutrient, FDR 4.2e-2) ✅ (low rank)
- **Cluster 6 (hormone/glucocorticoid)** = our Theme 1 (cellular response to hormone stimulus, FDR 8e-6) ✅ (top hit)
- **Cluster 8 (rhythmic/circadian)** = NOT separately surfaced in our top themes ❌ (PER1, FKBP5 absorbed into Theme 1)
- **Cluster 10 (cell migration)** = our Theme 3 (negative regulation of locomotion, FDR 3.8e-3) ✅

Key DAVID-captured biology NOT distinctly called out in our output:
- Circadian rhythm (PER1, FKBP5) — grouped with broader hormone response in Theme 1
- Lipid/steroid metabolism (ACSL1, HSD11B1, PDK4) — split across Themes 12, 18

Overall concordance: 5/6 major DAVID clusters captured; circadian signal diluted.
