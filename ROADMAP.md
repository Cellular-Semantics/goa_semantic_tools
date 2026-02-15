# GOA Semantic Tools - Development Roadmap

**Last Updated**: 2026-02-15

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

**Test coverage**: 60% (Ring 0 standard), 68 unit tests across 9 files.

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

## Ring 1: Planned (Pending User Feedback)

### 1. Exploratory Sub-Threshold Term Discovery

Surface GO annotation structure beneath FDR significance thresholds. For each enriched theme anchor, enumerate child GO terms with gene overlap that didn't reach significance. Rank by overlap proportion, show top 5 per parent. Flagged with `[EXPLORATORY]` provenance tag. Opt-in via `--exploratory` CLI flag.

Plan: [`planning/exploratory_sub_threshold_terms.md`](planning/exploratory_sub_threshold_terms.md)

### 2. Tiered Reference Validation

Full implementation of the tiered validation strategy explored in `exploration/10_reference_retrieval.py`:
- Tier 1: Abstract scan (cheap, fast)
- Tier 2: Full text + keyword grep
- Tier 3: Section-targeted read (Results > Conclusions > Intro)
- Early stopping on first adequate reference
- Graceful degradation for unsupported claims

### 3. Wikipedia Fallback for Textbook Knowledge

For well-established mechanisms (e.g., "IL-1B induces fever via PGE2") where no single paper states the claim explicitly. Use Wikipedia API to find cited PMIDs, then validate those PMIDs support the claim.

### 4. Annotation Depth Classification

Distinguish **specific enrichment** (genes annotated directly to leaf term) from **category enrichment** (genes annotated to general parent). Affects interpretation confidence and identifies where literature mining would add most value.

### 5. Cross-Namespace Co-annotation

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
| `services/go_explanation.prompt.yaml` | LLM explanation prompt |
| `services/reference_retrieval.prompt.yaml` | Assertion extraction prompt |
