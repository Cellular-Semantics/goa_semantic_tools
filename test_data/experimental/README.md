# Experimental Gene Sets

Real experimentally-derived gene sets with published GO analysis for comparison.
Used for validating pipeline output quality against known biology and published results.

**Note**: Unlike `input_data/` (gitignored — large reference files), this `test_data/` directory
is tracked by git. Files here are small enough to commit and serve as regression
test inputs for `goa_semantic_tools_validation_tools`.

Contrast with MSigDB Hallmark sets (used during development in `input_data/benchmark_sets/`)
which are synthetic curated sets ~5× more GO-dense than typical experimental data.

---

## himes2014_airway/

**Source**: Himes et al. 2014, PMID: 24926665, PMC4057123
**GEO**: GSE52778
**Experiment**: Dexamethasone-treated human airway smooth muscle cells (4h, 18h, 24h)
**Analysis**: DESeq2-equivalent (Cufflinks/Cuffdiff), BH-corrected p<0.05

### Files

| File | Description |
|------|-------------|
| `himes2014_dex_airway_DEGs.txt` | 314 unique DEG symbols (from 316 reported; 2 duplicates removed) |
| `david_enrichment_clusters.md` | Published DAVID functional annotation clusters (Supplement 4) used as comparison baseline |

### Enrichment characteristics

- 80 total enriched GO terms at FDR<0.05 (0.28 terms/gene)
- 24 leaves, 24 themes (3 hierarchical, 21 standalone)
- Top themes: hormone response, ECM, cell migration, vascular development
- 100% gene coverage in top-24 themes (no long-tail coverage problem)

### Comparison results (2026-03-13)

Our top themes vs published DAVID clusters — see `david_enrichment_clusters.md` for details.
**5/6 major DAVID clusters recovered**. Circadian signal (PER1, FKBP5) absorbed into
hormone response theme rather than being called out distinctly.

### Bugs identified during testing

1. **Fold enrichment stored as `study_count/pop_count`** instead of
   `(study_count/study_total) / (pop_count/pop_total)` — values show as 0.0x–0.1x
   for significantly enriched terms. Fixed in go_enrichment_service.py.

2. **Theme content mismatch for sparse late themes** — LLM writes wrong narrative
   for themes 12–15 when themes are very sparse (1–4 genes). Validator detects
   it (wrong genes/GO IDs) but renderer still outputs the bad content.
   Fixed: renderer now falls back to data-only stub for flagged themes.

### Gene symbol notes

26/314 genes not found in GOA human annotations — mostly outdated HGNC symbols:
- CTGF → CCN2, CYR61 → CCN1, NOV → CCN3
- WARS → WARS1, GALNTL2 → GALNT16
- Several C[N]orf[N] loci now renamed

### Intended use with validation tools

These datasets are candidates for use as reference data in `goa_semantic_tools_validation_tools`
regression tests. Each dataset has:
- Known enriched terms (via DAVID comparison)
- Published biological interpretation for narrative quality assessment
- Sparse enrichment profile (representative of real experimental data)

---

## Adding new datasets

Add a subfolder per study with at minimum:
- Gene list `.txt` file (one symbol per line, `#` comments allowed)
- `published_go_analysis.md` or equivalent (DAVID / clusterProfiler / Enrichr results)

Update this README with enrichment characteristics and comparison results.
