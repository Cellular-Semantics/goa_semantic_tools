# GOA Semantic Tools - Development Roadmap

**Last Updated**: 2026-03-13

## What This Tool Does

GO enrichment analysis produces long lists of statistically significant terms with heavy redundancy (parent-child overlaps, near-identical gene sets). GOA Semantic Tools reduces this to a structured set of biological themes with LLM-generated provenance-labeled explanations and literature-backed references.

**Pipeline**: Gene list → ORA enrichment → Leaf-first theme extraction → Depth-anchor hierarchy → LLM explanation → Reference injection

---

## Ring 0: Shipped

### Phase 1: GO Enrichment with Hierarchical Clustering

- ORA via GOATOOLS against GO BP namespace
- Automatic download/caching of GO OBO and GAF annotation files
- CLI runner (`goa-semantic-tools`) with `--genes` / `--genes-file` input
- JSON + Markdown output

### Phase 2: LLM-Based Explanations

- Provenance-labeled biological summaries via OpenAI-compatible LLMs
- Tag system: `[DATA]`, `[INFERENCE]`, `[EXTERNAL]`, `[GO-HIERARCHY]`
- Hub gene identification (genes appearing across 3+ themes)
- Markdown report generation with `--explain` flag
- Dry-run mode (`--dry-run`) to preview prompts without LLM calls

### Phase 3: Bottom-Up Depth-Anchor Algorithm + Reference Retrieval

Replaced the original top-N roots approach entirely.

**Enrichment algorithm** (`go_hierarchy.py`):
1. Compute enrichment leaves (most specific enriched terms with no enriched descendants)
2. Build hierarchical themes using depth-anchor selection (depth 4-7, min 2 children, max 30 genes)
3. Group specific terms under anchors; standalone leaves kept as flat themes
4. Uses both `is_a` and `part_of` relationships

**Reference retrieval** (`reference_retrieval_service.py`, `reference_index.py`):
- Builds gene→GO→PMID index from GAF annotations
- Extracts atomic assertions from LLM explanations (parses `[INFERENCE]` and `[EXTERNAL]` claims)
- Programmatic PMID lookup for simple/multi-gene claims
- Exports unresolved assertions to `*_artl_queries.json` for artl-mcp literature search
- Injects verified PMIDs into final markdown output
- CLI: `--add-references` flag

**Test coverage**: 60% (Ring 0 standard), 204 unit tests across 12 files.

**Benchmark results** (MSigDB Hallmark sets, v1 leaf-first):

| Gene Set | Enriched Terms | Themes | Reduction |
|----------|---------------|--------|-----------|
| Apoptosis | 56 | 21 | 63% |
| DNA Repair | 201 | 51 | 75% |
| Hypoxia | 29 | 7 | 76% |
| Inflammatory | 264 | 106 | 60% |
| OxPhos | 17 | 8 | 53% |
| P53 | 47 | 21 | 55% |

---

## Ring 1: In Progress

### 1a. artl-mcp Literature Search — DONE

Integrated Europe PMC literature search for assertions that GAF-based lookup cannot resolve (complex and [EXTERNAL] claims). Uses `cellsem-llm-client` MCPToolSource + LiteLLMAgent (~$0.003-0.006/assertion).

- `artl_literature_service.py` — single MCPToolSource session for batch, graceful degradation
- `--no-literature-search` CLI flag (opt-out; `--add-references` includes literature search by default)
- 25 unit tests (mocked), 1 integration test (real API)

### 1b. Output Quality Tuning — DONE

JSON intermediate architecture: LLM fills structured `EnrichmentExplanation` JSON (schema-enforced) → programmatic markdown render → inline reference injection. Key additions:

- `rank_genes_for_theme()` — data-driven gene selection, avoids fame bias (RELA/IL6 always winning)
- `validate_explanation_json()` — post-generation check: hallucinated genes/GO IDs caught and warned
- `render_explanation_to_markdown()` — deterministic renderer places `[REF:GENE]` markers
- `inject_references_inline()` — replaces markers with inline PMIDs (capped at 3, deduplicated)

**Known issue: ~100 unresolved assertions per run.** The post-hoc pipeline extracts `[INFERENCE]`/`[EXTERNAL]` tagged narrative sentences, does GAF+artl-mcp lookup, but ~100 remain unresolvable. Root cause is the architecture: LLM generates claims from latent knowledge first, then we search for papers to support them — the tail end has claims that are too vague, too general, or slightly mismatched with what literature indexing can find. See Ring 1c below.

### 1c. Paper-Grounded Narrative Generation — DONE

**Problem solved**: The post-hoc reference pipeline generated narrative from latent knowledge, then searched for papers to support it, leaving ~100 unresolved assertions per run.

**Solution implemented**: Lit-first architecture — fetch Europe PMC abstracts *before* the LLM explanation call.

```text
themes + hub_genes
    ↓
fetch_abstracts_for_themes()   [artl-mcp, single MCPToolSource session]
    ↓  dict[theme_index → list[{pmid, title, abstract, ...}]]
_format_enrichment_for_llm()   [injects "Available Literature" blocks per theme]
    ↓
LLM  [cites provided PMIDs inline: "PMID:10383454"]
    ↓
render_explanation_to_markdown()   [no [REF:GENE] markers]
    ↓
Final markdown with inline citations
```

Key changes:
- `fetch_abstracts_for_themes()` in `artl_literature_service.py` — calls `search_europepmc_papers` tool handler directly (no LLM for search phase)
- `_format_enrichment_for_llm()` — accepts `paper_abstracts` dict, injects abstract blocks per theme (400-char truncation)
- `go_explanation.prompt.yaml` — instructs LLM to cite inline as `PMID:xxx`, only from provided papers
- `cli.py` — Phase 1b pre-fetch before Phase 2 LLM; old post-hoc `_add_references_to_explanation()` bypassed

### 1d. Report Quality + Token Budget Robustness — DONE

Bug fixes and rendering improvements to the markdown report:

**Theme index fix**: LLM context now includes explicit `theme_index` field per theme block, eliminating the off-by-one that caused theme headings to mismatch narrative content.

**Report structure**:
- Methodology note at top explaining theme cap (top 30 by FDR), how themes are selected, and what anchors are
- `anchor_confidence` rendered on each theme summary line
- Full theme reference table at end of report (all themes, minimal detail)
- PMID hyperlink wiring: `_add_pmid_hyperlinks()` now called in the render pipeline

**Markdown quality**:
- LLM prose fields constrained to plain text via schema descriptions + prompt rule (prevents `**bold**`, `##`, etc. in narrative)
- `mdformat` post-processing (`wrap=no`) normalises whitespace and blank lines
- Blank-line rendering fix: `"".join(lines)` was silently discarding empty strings — changed to `"\n"` tokens throughout `render_explanation_to_markdown()`
- Subheadings promoted from inline bold to proper `####` headings

**Token budget**:
- Hub gene cap: top 20 by theme_count in both JSON schema (`maxItems: 20`) and LLM context (was unordered all-genes); matches `fetch_abstracts_for_hub_genes(max_hub_genes=20)`
- `max_tokens` default raised 8000 → 16000 for all models
- Per-model token defaults: `gpt-5` auto-gets 32000 via `_get_default_max_tokens()` lookup
- `--max-tokens` CLI flag added for user overrides on any model

**302 unit tests, 68% coverage**

### 2. Exploratory Sub-Threshold Term Discovery

Surface GO annotation structure beneath FDR significance thresholds. For each enriched theme anchor, enumerate child GO terms with gene overlap that didn't reach significance. Rank by overlap proportion, show top 5 per parent. Flagged with `[EXPLORATORY]` provenance tag. Opt-in via `--exploratory` CLI flag.

Plan: [`planning/exploratory_sub_threshold_terms.md`](planning/exploratory_sub_threshold_terms.md)

### 3. Tiered Reference Validation

Full implementation of the tiered validation strategy explored in `exploration/10_reference_retrieval.py`:
- Tier 1: Abstract scan (cheap, fast)
- Tier 2: Full text + keyword grep
- Tier 3: Section-targeted read (Results > Conclusions > Intro)
- Early stopping on first adequate reference
- Graceful degradation for unsupported claims

### 4. Wikipedia Fallback for Textbook Knowledge

For well-established mechanisms (e.g., "IL-1B induces fever via PGE2") where no single paper states the claim explicitly. Use Wikipedia API to find cited PMIDs, then validate those PMIDs support the claim.

### 5. Annotation Depth Classification

Distinguish **specific enrichment** (genes annotated directly to leaf term) from **category enrichment** (genes annotated to general parent). Affects interpretation confidence and identifies where literature mining would add most value.

### 6. Cross-Namespace Co-annotation

Strengthen biological interpretation by combining evidence across GO namespaces:
- BP co-annotation from same reference → strong functional link
- CC co-annotation → subcellular context
- Reference co-occurrence graphs for functionally coherent sub-groups

---

## Ring 2: Post-Ring-1 Features

### Semantic Similarity Clustering
Use GO term IC-based or embedding-based similarity as alternative/complement to hierarchy-based clustering. May help in sparse GO branches.

See: [Enrichment Anchor Critique](enrichment_anchor_critique.md) for analysis of current compression failure, comparison with REVIGO/rrvgo semantic similarity measures, and the `regulates`-extended anchor proposal.

### Multi-Axis Narrative Structure

Organise themes into 3–5 LLM-defined biological axes (e.g. "immune regulation", "metabolism", "ECM remodelling"), each with a tree-structured narrative. Two-phase: Phase A (axis identification, ~4–6k tokens) → Phase B (per-axis narrative, existing pipeline). Deferred until MRCEA-B theme quality is improved — axis identification over 153 cleaner themes will produce better results than over 224 semi-redundant depth-anchor themes.

See: [Enrichment Anchor Critique §10](enrichment_anchor_critique.md) for context efficiency analysis and design notes.

### Multi-Ontology Support
The architecture after flat enriched terms is ontology-agnostic if abstracted to: term→parent/child, term→genes, gene→annotation refs. Could extend to HPO, Disease Ontology, Reactome.

### Evidence Aggregation from Child Annotations
For enrichment leaves, pull PMIDs from non-significant child term annotations to explain WHY enrichment exists at the parent level.

---

## Technical Debt

- [x] **Fold enrichment formula** — was computing `study_count/pop_count` instead of `(study_count/study_total)/(pop_count/pop_total)`. Fixed 2026-03-13 in `go_enrichment_service.py`. See [Enrichment Anchor Critique §13](enrichment_anchor_critique.md).
- [x] **Theme content mismatch** — LLM narrative rendered even when validator detected wrong genes/GO IDs (late sparse themes). Fixed 2026-03-13: renderer falls back to data-only stub for flagged themes. See [Enrichment Anchor Critique §13](enrichment_anchor_critique.md).
- [ ] Add population counts to theme output (fold enrichment transparency)
- [ ] Cache GO DAG loading (currently ~1s per run)
- [ ] Schema updates for HierarchicalTheme structure (JSON schema → Pydantic)
- [ ] Benchmark depth-anchor algorithm (Option C) across all hallmark sets
- [ ] Consider IC calculation for term specificity metrics (see [Enrichment Anchor Critique](enrichment_anchor_critique.md) — depth is a poor IC proxy in dense annotation branches)
- [ ] Gene symbol normalisation — 26/314 Himes genes not found in GOA (outdated HGNC: CTGF→CCN2, CYR61→CCN1, WARS→WARS1 etc.). Pre-processing step needed.
- [ ] Additional test cases: rare disease genes (sparse GO), small gene sets (<20 genes)

---

## Ring 3: Validation Tooling

### `goa_semantic_tools_validation_tools` — Flesh Out

The validation package skeleton exists but is largely empty. Needs to be developed to support systematic quality assessment as the pipeline evolves.

**Planned components:**

| Component | Description |
|-----------|-------------|
| `comparisons/theme_concordance.py` | Compare pipeline themes against published GO clusters (DAVID/clusterProfiler); compute recall/precision per cluster |
| `comparisons/run_diff.py` | Diff two enrichment JSON outputs (e.g. depth-anchor vs MRCEA-B) on same gene list |
| `metrics/compression_metrics.py` | L/T ratio, coverage at N themes, standalone fraction, hub gene concentration |
| `metrics/narrative_quality.py` | Count `[DATA]` vs `[EXTERNAL]` vs unfilled placeholders; citation density |
| `visualizations/theme_coverage.py` | Gene coverage curve as function of top-N themes |

**Reference datasets for regression tests**: Experimental sets in `input_data/experimental/` with published GO analysis. Each test checks that key biological themes are recovered and that specific genes appear in expected theme positions.

**Priority**: Implement after Ring 1 is fully stable and MRCEA-B is in production. Validation tooling is needed to confidently compare algorithm variants.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│ INPUT: Gene list + GO OBO + GAF annotations             │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ ENRICHMENT (go_enrichment_service.py)                   │
│ ORA via GOATOOLS → flat enriched terms with FDR + genes │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ HIERARCHY (go_hierarchy.py)                             │
│ Enrichment leaves → depth-anchor grouping → hub genes   │
│ Uses is_a + part_of edges                               │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ PHASE 1b: LITERATURE PRE-FETCH (artl_literature_service)│
│ Per theme: Europe PMC search (top genes + anchor name)  │
│ Per hub gene: Europe PMC search (gene + theme)          │
│ GAF PMIDs: gene→GO→PMID index (reference_index.py)     │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ LLM EXPLANATION (go_markdown_explanation_service.py)    │
│ Abstracts + GAF PMIDs injected into theme context       │
│ LLM cites inline: PMID:xxxxx within provenance tags     │
│ [DATA] [INFERENCE] [EXTERNAL] [GO-HIERARCHY]            │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ RENDER + POST-PROCESS                                   │
│ render_explanation_to_markdown() → PMID hyperlinks      │
│ mdformat normalisation → final markdown report          │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ OUTPUT: Markdown report + JSON themes                   │
└─────────────────────────────────────────────────────────┘
```

---

## Related Work

Methods addressing GO enrichment redundancy:
- **topGO elim/weight** - Removes genes from parent terms if child is significant
- **REVIGO** - Semantic similarity clustering of GO terms
- **evoGO** (2025) - Bottom-up redundancy minimization, 30% reduction, 96% TP recovery

Our approach differs by producing explicit hierarchical theme structures with provenance-labeled LLM explanations and programmatic reference injection.

---

## Test Cases

### MSigDB Hallmark Benchmark Sets

Located in `input_data/benchmark_sets/test_lists/`:

**Positive controls**: `hallmark_apoptosis.txt` (161 genes), `hallmark_dna_repair.txt` (150), `hallmark_hypoxia.txt` (200), `hallmark_inflammatory_response.txt` (200), `hallmark_p53_pathway.txt` (200), `hallmark_oxidative_phosphorylation.txt` (200)

**Negative controls**: `random_50_genes.txt`, `random_100_genes.txt`, `random_200_genes.txt`

**Caveat**: Hallmark sets are synthetic (curated for GO-density) — ~5× more enriched terms/gene than typical experimental data. Not representative of real-world use.

### Experimental Benchmark Sets

Located in `test_data/experimental/` (git-tracked; small committed files). Real bulk RNA-seq datasets with published GO analysis for quality comparison.

| Study | File | Genes | Published analysis | Key biology |
|-------|------|-------|--------------------|-------------|
| Himes et al. 2014 (PMID:24926665) | `test_data/experimental/himes2014_airway/himes2014_dex_airway_DEGs.txt` | 314 | DAVID clusters (Supplement 4) | Glucocorticoid response, ECM, cell migration |

**Intended future use**: Reference datasets for `goa_semantic_tools_validation_tools` regression tests (narrative quality, theme concordance with published clusters). See Ring 3 below.

### Exploration Scripts

| Script | Purpose |
|--------|---------|
| `exploration/05_leaf_first_clustering.py` | v1: Leaf-first algorithm prototype |
| `exploration/06_benchmark_leaf_first.py` | Benchmark runner |
| `exploration/07_hierarchical_themes.py` | v2: Two-pass hierarchical |
| `exploration/08_multi_threshold_hierarchy.py` | v3 Option B: Multi-threshold |
| `exploration/09_depth_anchors.py` | v3 Option C: Depth-based anchors (best) |
| `exploration/10_reference_retrieval.py` | Reference retrieval workflow |
| `exploration/11_artl_mcp_via_llm.py` | artl-mcp literature search proof-of-concept |

---

## Key Files

| File | Role |
|------|------|
| `cli.py` | CLI entry point (`goa-semantic-tools`) |
| `services/go_enrichment_service.py` | ORA enrichment via GOATOOLS |
| `services/go_markdown_explanation_service.py` | LLM explanation generation |
| `services/reference_retrieval_service.py` | Claim extraction + PMID injection |
| `utils/go_hierarchy.py` | Leaf-first + depth-anchor theme building |
| `utils/reference_index.py` | GAF gene→GO→PMID index |
| `services/artl_literature_service.py` | Europe PMC literature search via artl-mcp |
| `services/go_explanation.prompt.yaml` | LLM explanation prompt |
| `services/reference_retrieval.prompt.yaml` | Assertion extraction prompt |
| `services/artl_literature_search.prompt.yaml` | Literature search agent prompt |
