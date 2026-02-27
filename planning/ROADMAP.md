# GOA Semantic Tools - Development Roadmap

**Last Updated**: 2026-02-24

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

### Future Ring 1 (after 1b)

### 1c. Paper-Grounded Narrative Generation

**Problem**: The current pipeline generates narrative from latent knowledge, then post-hoc searches for papers to support it. This produces ~100 unresolved assertions per run — claims the LLM made that no paper explicitly confirms.

**Root cause**: The post-hoc direction is fundamentally harder than the pre-hoc direction. Finding a paper that matches a vague LLM-generated claim is harder than having the LLM write a claim based on a paper it has in context.

**Proposed architectural shift**: Fetch papers *before* the LLM explanation call, and provide them as grounding context. The LLM then cites papers it is actually summarising rather than making claims that need retrospective validation.

Three possible approaches:

#### Option A: RAG per theme (pre-fetch, then generate)

```text
For each theme:
  1. artl-mcp: search for papers on ranked key genes + anchor GO term name
  2. Pass top 3-5 paper abstracts as context to LLM
  3. LLM generates narrative with inline citations (e.g., "as shown in [1]")
  4. Map citation numbers back to PMIDs in post-processing
```

Advantages: eliminates the unresolved assertion problem; LLM narrative is grounded.
Disadvantages: artl-mcp cost moves from ~$0.06/run (post-hoc, only unresolved) to ~cost × n_themes upfront; slower.

#### Option B: Reuse key-gene PMIDs for narrative claims (cheaper fix)

```text
After artl-mcp runs for key genes, build gene→PMIDs map.
For narrative sentences containing gene symbols, automatically attach
the same PMIDs already found for that gene's key-gene entry.
```

Advantages: zero extra artl-mcp cost; reuses work already done.
Disadvantages: PMID is about the gene broadly, not specifically about the claim sentence. Acceptable for `[EXTERNAL]` single-gene claims; less appropriate for multi-gene `[INFERENCE]` claims.

#### Option C: Tighter claim extraction (cheapest fix)

```text
Current extract_claims() parses every [INFERENCE]/[EXTERNAL] sentence as a claim.
Many produce no usable assertions (no gene match, or gene match too vague).
Filter: only create assertions where ≥1 gene from the enrichment gene set is mentioned.
This would reduce 102 → maybe 20-30 genuinely meaningful unresolved claims.
```

Recommendation: Implement Option C first (filter low-signal claims), then evaluate whether Option B suffices or Option A is needed. Option A is the architecturally correct long-term solution but carries runtime and cost implications worth validating with users first.

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

## Ring 2: Speculative

### Semantic Similarity Clustering
Use GO term IC-based or embedding-based similarity as alternative/complement to hierarchy-based clustering. May help in sparse GO branches.

### Multi-Ontology Support
The architecture after flat enriched terms is ontology-agnostic if abstracted to: term→parent/child, term→genes, gene→annotation refs. Could extend to HPO, Disease Ontology, Reactome.

### Evidence Aggregation from Child Annotations
For enrichment leaves, pull PMIDs from non-significant child term annotations to explain WHY enrichment exists at the parent level.

---

## Technical Debt

- [ ] Add population counts to theme output (fold enrichment transparency)
- [ ] Cache GO DAG loading (currently ~1s per run)
- [ ] Schema updates for HierarchicalTheme structure (JSON schema → Pydantic)
- [ ] Benchmark depth-anchor algorithm (Option C) across all hallmark sets
- [ ] Consider IC calculation for term specificity metrics
- [ ] Additional test cases: rare disease genes (sparse GO), small gene sets (<20 genes)

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
│ LLM EXPLANATION (go_markdown_explanation_service.py)     │
│ Provenance-labeled summary: [DATA] [INFERENCE]          │
│ [EXTERNAL] [GO-HIERARCHY]                               │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ REFERENCE INJECTION (reference_retrieval_service.py)    │
│ Parse claims → GAF PMID lookup → artl-mcp escalation    │
│ → inject [Refs: PMID:xxx] into markdown                 │
└──────────────────────────┬──────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│ OUTPUT: Markdown report + JSON themes + artl queries     │
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
