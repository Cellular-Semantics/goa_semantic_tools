# Literature Search Strategy

**Date**: 2026-03-13

---

## Current approach (Ring 1c/1d — lit-first)

Europe PMC abstract search via artl-mcp, injected into LLM context before generation:

- **Per theme**: keyword search `{rank1_gene} {rank2_gene} {rank3_gene} {anchor_name}` (max 5 results)
- **Per hub gene**: `{gene} {gene.themes[0]}` (max 5 results)
- **GAF PMIDs**: curated gene→GO citations fetched by PMID via `get_europepmc_paper_by_id`

**Limitation**: Abstract-only. Misses findings in results/discussion sections; recall limited by keyword matching against title/abstract text.

---

## Candidate upgrade: ASTA snippet search (deferred — Ring 2)

**What it offers**: Pre-embedded full-text corpus returning ranked snippets — full-text recall without context-saturating complete papers.

**Why deferred**: Orthogonal to current enrichment strategy work. Evaluate after theme compression is stable so snippet volume can be assessed against a representative theme structure.

### Constraints to validate (Week 0 for ASTA integration)

- **Snippet flood risk** — well-studied processes (leukocyte migration, apoptosis, TNF signalling) have thousands of papers; measure raw snippet count per theme on both:
  - Immune dataset (worst case — `hm_inflam_enrichment.json`, 223 themes, highly annotated)
  - Metabolic dataset (typical case — `hallmark_oxidative_phosphorylation`)
- **Query strategy** — current `{gene} {anchor_name}` form is gene-centric and designed for keyword search. Semantic snippet search may perform better with:
  - Anchor term alone
  - Anchor term + top 2–3 hub genes
  - Test both and compare snippet relevance
- **Budget**: determine a safe `max_snippets_per_theme` that keeps total context within model limits across theme counts of 50–200

### Integration point

Replace or supplement `fetch_abstracts_for_themes()` in `artl_literature_service.py`. The `gaf_abstracts` and `hub_gene_abstracts` paths would be unchanged.
