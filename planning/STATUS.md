# NeeGOA Semantic Tools - Development Status

**Date**: 2026-02-15
**Branch**: ring1_artl_mcp_references (current), main (Ring 0 shipped)

## Current State: Ring 1 — artl-mcp Literature Reference Integration

Ring 0 shipped (depth-anchor enrichment + LLM explanation + GAF reference injection). Now integrating artl-mcp for resolving complex/[EXTERNAL] assertions that GAF annotations can't cover.

## Historical: Ring 0 Algorithm Development

### Problem Solved
Original top-N clustering selected overly general terms (e.g., "membrane" with 107 genes) and created hierarchical redundancy (4 vascular terms reporting same 8-14 genes).

---

## Algorithm Evolution

### v1: Leaf-First Clustering (05_leaf_first_clustering.py)

**Algorithm**:
1. Find enrichment leaves (enriched terms with no enriched descendants)
2. Merge leaves with identical gene sets (keeps lowest FDR)
3. Filter overly general terms (>50 genes)
4. Check parent contribution (include if adds 20-200% new genes)
5. Dual FDR threshold: 0.05 (high confidence) + 0.10 (moderate)

**Output structure**:
```python
BiologicalTheme:
  primary_term: EnrichedTerm  # Most specific (leaf)
  broader_term: EnrichedTerm | None  # Parent if adds significant genes
  confidence: "high" | "moderate"
```

**Limitations**:
- Only traverses one level up (leaf → parent)
- Uses is_a relationships only (not part_of)
- Flat output: siblings under same parent stored as separate themes
- Duplicate parent info when multiple leaves share an anchor

---

### v2: Two-Pass Hierarchical (07_hierarchical_themes.py) [IN PROGRESS]

**Algorithm**:
1. Run ORA at FDR 0.10 → get all enriched terms
2. Find leaves at TWO thresholds:
   - Leaves_0.05 = high-confidence terms with no high-confidence descendants
   - Leaves_0.10 = all terms with no enriched descendants
3. Identify anchors: terms in Leaves_0.05 but NOT in Leaves_0.10
   - These have moderate-confidence children worth grouping
4. Group children under shared anchors
5. Use is_a + part_of relationships (not just is_a)

**Output structure**:
```python
HierarchicalTheme:
  anchor_term: EnrichedTerm        # Parent (or standalone leaf)
  specific_terms: list[EnrichedTerm]  # Children grouped under anchor
  anchor_confidence: "high" | "moderate"
```

**Improvements**:
- Captures more hierarchy depth via two-pass approach
- Groups siblings under shared parent (no duplication)
- Uses part_of relationships for better biological coverage
- Parent-centric output better for LLM summarization

**Current results** (inflammatory response test):
- 102 themes total (vs 106 in v1)
- 5 anchors with nested children found
- Examples: "antigen receptor signaling" → "T cell receptor signaling", "MAPK cascade" → "ERK1/2 cascade"

**Limitation**: Only 5 anchors found because algorithm requires anchors to be leaves at FDR 0.05.

---

### v3: Tested Approaches [2026-02-11]

#### Option B: Multi-threshold (08_multi_threshold_hierarchy.py)

Thresholds: 0.01, 0.03, 0.05, 0.07, 0.10

**Results** (inflammatory response):
- 102 total themes, 16 with nested children
- 16 total nested specific terms
- Simple linear hierarchy based on FDR thresholds

**Limitation**: Only captures single parent-child relationships at threshold boundaries.

---

#### Option C: Depth-based anchors (09_depth_anchors.py) ✅ BEST

Parameters: depth_range=(4,7), min_children=2, max_genes=30, no_overlap=True

**Results** (inflammatory response):
- 87 total themes, 21 with nested children
- **87 total nested specific terms** (5x more than Option B)
- Captures deep multi-level hierarchy

**Example hierarchies captured:**
```
"positive regulation of lymphocyte activation" (26 genes, d=7)
   └─ positive regulation of T cell activation (21 genes)
   └─ positive regulation of lymphocyte proliferation (16 genes)
   └─ positive regulation of T cell proliferation (14 genes)
   └─ ... and 17 more children

"immune response-activating signaling pathway" (25 genes, d=7)
   └─ pattern recognition receptor signaling pathway (16 genes)
   └─ cell surface toll-like receptor signaling pathway (8 genes)
   └─ ... and 13 more children

"cellular response to cytokine stimulus" (21 genes, d=5)
   └─ cellular response to interleukin-1 (8 genes)
   └─ cellular response to tumor necrosis factor (8 genes)
   └─ cellular response to type II interferon (4 genes)
```

**Comparison:**

| Metric | Option B | Option C |
|--------|----------|----------|
| Total themes | 102 | 87 |
| With children | 16 | 21 |
| Nested terms | 16 | 87 |

**Conclusion**: Option C (depth-based anchors) is clearly superior for LLM-friendly hierarchical explanation. Depth is imperfect but effective for finding intermediate-level groupings.

---

#### Option D: MSCA (not yet tested)
- For clusters of leaves, find lowest common ancestor
- May be useful as complement to Option C

### Benchmark Results

Tested on MSigDB Hallmark sets (`exploration/06_benchmark_leaf_first.py`):

| Gene Set | BP Terms | Themes | Reduction |
|----------|----------|--------|-----------|
| Apoptosis | 56 | 21 | 62.5% |
| DNA Repair | 201 | 51 | 74.6% |
| Hypoxia | 29 | 7 | 75.9% |
| Inflammatory | 264 | 106 | 59.8% |
| OxPhos | 17 | 8 | 52.9% |
| P53 | 47 | 21 | 55.3% |

**Average reduction: 63%** while preserving expected biology in top themes.

---

## LLM Summarization Approach

### Key Insights

1. Leaf-first themes alone produce better summaries than hierarchical clusters
2. Hub gene analysis provides mechanistic depth
3. Provenance labeling critical for credibility

### Hub Gene Analysis

Genes appearing in 3+ themes reveal biological coordinators:

| Gene | Themes | Role |
|------|--------|------|
| RELA | 24/106 | NF-κB p65 - master inflammatory TF |
| IL6 | 19/106 | Pleiotropic cytokine |
| IL1B | 18/106 | Pro-inflammatory, fever, angiogenesis |
| TLR2 | 17/106 | Pattern recognition receptor |
| TLR3 | 15/106 | Viral dsRNA sensor |
| EDN1 | 14/106 | Inflammation-cardiovascular link |

### Example Summary Output (Inflammatory Response)

**Core Architecture**: LPS response pathway (FDR 4.22e-22, 22 genes) most enriched, converging on TLR4 signaling through CD14-LY96-MYD88 axis. Parallel recognition via TLR2 (Gram-positive) and NOD2 (muramyl dipeptide). Chemokine-mediated signaling (FDR 6.33e-13) coordinates leukocyte recruitment.

**Hub Gene Rationale**: RELA (24 themes) controls inflammatory transcription - its appearance across LPS, cytokine, viral, and angiogenesis themes reflects NF-κB target gene breadth. IL1B (18 themes) has pleiotropic effects: acute phase response, JAK-STAT activation, wound healing, fever via hypothalamic prostaglandin synthesis.

**Novel Finding**: EDN1 (14 themes) links inflammation to cardiovascular physiology - inflammatory cytokines induce EDN1 in endothelium, while EDN1 promotes leukocyte adhesion. Molecular link between systemic inflammation and cardiovascular complications.

### Provenance Labeling System

Critical for biologist credibility - distinguish data from grence from external knowledge:

**[DATA]** - Direct observations from enrichment:
> "RELA appears in 24 of 106 themes including LPS response, IL-6 production, angiogenesis"
> "Cellular response to LPS is most enriched (FDR 4.22e-22, 22 genes)"

**[INFERENCE]** - Logical deductions from co-annotation patterns:
> "The co-annotation of TLR2, TLR3, TLR4, and NOD2 across overlapping cytokine themes suggests these distinct sensors feed into a shared downstream effector program"
> "The appearance of RELA across diverse themes suggests it functions as a central transcriptional coordinator"

**[EXTERNAL]** - Claims requiring training knowledge (need literature refs):
> "RELA encodes the p65 subunit of NF-κB, the master transcription factor for inflammatory gene expression"
> "IL-1β induces fever by stimulating prostaglandin E2 synthesis in the hypothalamus"

### Provenance-Labeled Example

> [DATA] The inflammatory response gene set is dominated by hub genes: RELA (24 themes), IL6 (19), IL1B (18), TLR2 (17). [DATA] Most significant enrichment is "cellular response to LPS" (FDR 4.22e-22, 22 genes). [EXTERNAL] RELA encodes NF-κB p65, the master transcription factor for inflammatory gene expression. [INFERENCE] RELA's appearance across pathogen responses, cytokine production, and angiogenesis suggests it integrates multiple inflammatory inputs into a unified transcriptional response.

This labeling allows biologists to see exactly which claims need literature verification.

### LLM Summary Prompt Template

Used for depth-based anchor output (09_depth_anchors.py):

```
Generate a provenance-labeled biological summary of this GO enrichment analysis.

Use these tags to distinguish claim sources:
- [DATA]: Direct observations from enrichment (FDR values, gene counts, co-occurrence facts)
- [GO-HIERARCHY]: Facts derived from GO parent-child structure (subsumption, specialization)
- [INFERENCE]: Logical deductions from co-annotation patterns
- [EXTERNAL]: Claims requiring training/latent knowledge (need literature support)

Guidelines:
- Focus on biology, not ontology structure
- Avoid depth numbers - use "more/less specific" or "specialized" language
- Do not describe GO organization (e.g., "flat categorization under umbrella term")
- Explain biological significance of hierarchical groupings
- Highlight hub genes and their pathway convergence patterns
```

---

## GO Annotation Reference Analysis [2026-02-11]

Analysis of PMID-backed annotations for inflammatory response genes:

### Coverage Statistics

| Metric | Count |
|--------|-------|
| Genes in analysis | 151 |
| GO terms in themes | 174 |
| Total annotations for genes | 15,108 |
| Annotations with PMIDs | 8,144 (54%) |
| Unique PMIDs | 2,716 |
| Genes with PMID-backed annotations | 151/151 (100%) |

### High-Value References

**PMIDs annotating ≥2 genes to SAME theme GO term: 73**

These are particularly valuable - same paper provides evidence for multiple genes in same process:

| PMID | Genes | GO Term |
|------|-------|---------|
| 19593445 | 5 (CD40, IL1B, IRF1, NFKB1, TLR3) | cellular response to mechanical stimulus |
| 10653850 | 4 (IL18, IL18R1, IL1B, IL1R1) | positive regulation of type II IFN production |
| 12782716 | 3 (CXCL10, CXCL11, CXCL9) | adenylate cyclase-activating GPCR signaling |
| 16880211 | 3 (CD14, TLR1, TLR2) | cellular response to triacyl bacterial lipopeptide |
| 10383454 | 3 (IL1B, IL1R1, IRAK2) | interleukin-1-mediated signaling pathway |

**PMIDs annotating to ≥2 different theme GO terms: 92**

These papers connect multiple biological processes:

| PMID | GO terms | Genes |
|------|----------|-------|
| 20027291 | 5 | 3 |
| 16880211 | 4 | 3 |
| 9407497 | 4 | 3 |

**Multi-gene PMIDs (any GO term): 323**

Top papers by gene coverage in our set:
- PMID:32296183 - 53 genes
- PMID:33961781 - 32 genes
- PMID:25416956 - 25 genes

### Implications for [DATA] Claims

GO annotation PMIDs can directly support [DATA] claims about:
1. Gene-process associations (607 PMID-backed annotations to theme GO terms)
2. Co-annotation patterns (73 PMIDs annotate ≥2 genes to same process)
3. Cross-process connections (92 PMIDs span multiple theme GO terms)

### Same-Gene Multi-Process Annotations

PMIDs that annotate a single gene to multiple theme GO terms directly support [INFERENCE] claims about pathway convergence:

| Gene | Multi-process PMIDs | Example |
|------|---------------------|---------|
| IL12B | 8 | PMID:20027291 → NK activation + NKT activation + IFN-γ + IL-12 |
| RELA | 8 | PMID:12048232 → canonical + non-canonical NF-κB |
| IL18 | 7 | PMID:10653850 → Th1 cytokines + IFN-γ production |
| NOD2 | 7 | PMID:31649195 → bacterial defense + PRR signaling + NOD2 pathway |
| TLR2 | 6 | PMID:19931471 → diacyl + triacyl lipopeptide response |
| CD14 | 4 | PMID:12594207 → LPS + lipoteichoic acid + TNF production |

**Total: 117 gene-PMID pairs** where same gene annotated to ≥2 theme GO terms.

### Reference-Backed [INFERENCE] Format

Example of how references support inference claims:

```
[DATA] CD14 appears in all four bacterial response pathways.

[INFERENCE] CD14 functions as a shared co-receptor routing different
bacterial patterns to appropriate receptors.
[Refs: PMID:12594207, PMID:16880211]
```

**Mapping inference claims to supporting PMIDs:**

| Inference Claim | PMIDs | Evidence Type |
|-----------------|-------|---------------|
| CD14 shared co-receptor | 4 | Same gene → multiple bacterial pathways |
| RELA pathway convergence | 8 | Same gene → signaling + cytokine production |
| IL12B-IL18 lymphocyte module | 8 | Both genes → T/NK/NKT activation terms |
| TLR specificity | 4 | TLR2 → bacterial; TLR3 → viral/IFN |

### Descendant Term References

Annotations may be to terms MORE specific than our themes. Including descendants:

| Scope | GO Terms | PMIDs |
|-------|----------|-------|
| Strict (theme terms only) | 174 | 380 |
| Expanded (+ descendants) | 821 | 422 (+11%) |

Example valid descendant reference:
```
Gene: TLR3 (in enrichment)
Annotated to: "toll-like receptor 3 signaling pathway" (descendant)
Supports theme: "innate immune response-activating signaling pathway"
```

**Decision**: Include descendant refs - they provide more specific evidence for theme claims.

### Reference Selection Strategy

**Current (deterministic, no external lookup):**
1. Coverage: PMIDs annotating most GO terms for that gene
2. Recency: Newer PMIDs as tiebreaker
3. Limit: Top 2-3 per inference claim

**Future (with artl-mcp citation data):**
1. Citation count (high-impact evidence)
2. Recency weighting
3. Review vs primary article preference

### Reference Addition: Post-LLM Programmatic Step

References are NOT passed to the LLM. Pipeline:

```
1. LLM generates provenance-labeled summary
   - [DATA], [INFERENCE], [GO-HIERARCHY], [EXTERNAL] claims
   - No references yet

2. Programmatic reference injection (post-LLM)
   - Parse [INFERENCE] claims → identify genes + processes mentioned
   - Lookup supporting PMIDs from pre-computed reference map
   - Inject [Refs: PMID:xxx, PMID:yyy] after relevant claims
   - For [EXTERNAL] claims → query literature API (artl-mcp)
```

Benefits:
- LLM focuses on biological narrative, not reference formatting
- Deterministic reference selection (reproducible)
- Can update references without re-running LLM
- Separates "what to say" from "how to support it"

### Gap: [EXTERNAL] Claims

The 7 [EXTERNAL] claims in the summary (mechanistic explanations like "RELA is NF-κB p65") require literature search beyond GO annotations.

**Planned approach (with artl-mcp):**
1. Query literature API for hub gene + mechanism keywords
2. Rank by citation count
3. Select top 1-2 supporting refs per [EXTERNAL] claim
4. Flag novel findings where literature support is weak

### Exploration Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `exploration/05_leaf_first_clustering.py` | v1: Leaf-first algorithm | ✅ Complete |
| `exploration/06_benchmark_leaf_first.py` | Benchmark runner for v1 | ✅ Complete |
| `exploration/07_hierarchical_themes.py` | v2: Two-pass hierarchical | ✅ Complete |
| `exploration/08_multi_threshold_hierarchy.py` | v3 Option B: Multi-threshold | ✅ Complete |
| `exploration/09_depth_anchors.py` | v3 Option C: Depth-based anchors | ✅ Best results |

### Key Output Files

| File | Purpose |
|------|---------|
| `results/benchmark/` | Benchmark outputs |
| `results/benchmark/inflammatory_enriched_for_summary.json` | Hub gene example |
| `results/benchmark/hallmark_*_themes.json` | v1 theme outputs |
| `results/benchmark/hallmark_*_hierarchical.json` | v2 theme outputs |
| `ROADMAP.md` | Future enhancements |

### Next Steps

**Hierarchy algorithm:**
- [x] Evaluate v3 options - Option C (depth-based anchors) is best
- [ ] Integrate Option C algorithm into main `go_hierarchy.py`
- [ ] Update CLI to use new algorithm
- [ ] Benchmark Option C across all hallmark sets

**LLM summarization:**
- [ ] Implement provenance-labeled explanation generation in production
- [ ] Test LLM summarization with hierarchical (Option C) output
- [ ] Add GO annotation references (PMIDs) to support [DATA] claims
- [ ] Consider same-paper co-annotation as signal for process+mechanism stories

---

## Ring 1 Goals

### Exploratory Sub-Threshold Term Discovery

**Status**: Planned
**Plan**: [`planning/exploratory_sub_threshold_terms.md`](planning/exploratory_sub_threshold_terms.md)

Surface GO annotation structure beneath statistically significant enrichment thresholds to guide further exploration. Enrichment doesn't mean all necessary components are present, and lack of enrichment doesn't mean unimportant -- a single rate-limiting gene may suffice to activate a function.

**Approach**: For each significantly enriched theme anchor, enumerate child GO terms that have gene overlap with the input list but didn't reach FDR significance. Rank by overlap proportion (input genes / total annotated genes), show top 5 per parent. Clearly flagged as exploratory with new `[EXPLORATORY]` provenance tag.

**Key design**: No second p-value cutoff. Report gene counts instead. Opt-in via `--exploratory` CLI flag. Leverages `goea_results_all` already computed but currently discarded after FDR filtering.

**Future**: May add semantic clustering of exploratory terms to reduce redundancy. Could fold in other evidence types beyond enrichment.

---

## Ring 1 Architecture Notes

### Modularity Principle

The system has natural separation points that should be preserved:

```
┌─────────────────────────────────────────────────────────────────┐
│ INPUT LAYER (swappable)                                         │
│ - GO enrichment (current)                                       │
│ - Other ontology enrichment (HPO, DO, Reactome...)             │
│ - Any system returning: terms + FDR + genes + hierarchy edges   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ HIERARCHY BUILDING (reusable)                                   │
│ - Depth-based anchor selection                                  │
│ - Parent-child grouping                                         │
│ - Hub gene identification                                       │
│ - Pre-compute descendant closure for each theme                 │
│ Input: flat enriched terms + ontology graph                     │
│ Output: HierarchicalTheme objects + relevant_go_terms set       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ LLM EXPLANATION (reusable)                                      │
│ - Provenance labeling ([DATA], [INFERENCE], [EXTERNAL])        │
│ - Hub gene narrative                                            │
│ - NO references at this stage                                   │
│ Input: hierarchical themes                                      │
│ Output: provenance-labeled biological summary                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ REFERENCE INJECTION (programmatic, post-LLM)                    │
│ - Parse claims from LLM output                                  │
│ - Lookup PMIDs using pre-computed relevant_go_terms             │
│ - Simple set membership (no hierarchy traversal)                │
│ - Citation ranking (via artl-mcp)                               │
│ - Query literature API for [EXTERNAL] claims                    │
│ Input: LLM summary + annotation database + relevant_go_terms    │
│ Output: summary with injected references                        │
└─────────────────────────────────────────────────────────────────┘
```

**Key insight**: Everything after "flat list of enriched terms" is ontology-agnostic if we abstract:
- Term → parent/child relationships
- Term → gene associations
- Gene → annotation references

This enables reuse across GO, HPO, Disease Ontology, Reactome pathways, etc.

### Research Context

Compared to existing methods (see `research/GO Enrichment Redundancy Methods.md`):
- **evoGO** (2025): Similar bottom-up philosophy, 30% reduction, 96% TP recovery
- **topGO elim**: Removes genes from ancestors, slower
- **Our novelty**: Explicit theme structure, dual thresholds, hub gene analysis, provenance labeling

---

## Reference Retrieval Exploration [2026-02-11]

### Exploration Script

`exploration/10_reference_retrieval.py` - Interactive workflow with human/LLM steps.

### Results Summary

| Source | Assertions | With Refs | Coverage |
|--------|------------|-----------|----------|
| GO Annotations (programmatic) | 15 | 7 | 47% |
| artl-mcp (literature search) | 8 | 8 | 100% |
| **Combined** | **15** | **12** | **80%** |

### Key Insight: GO Annotations Support [EXTERNAL] Claims Too

Originally assumed GO annotation PMIDs only support `[INFERENCE]` claims. However:

```
[EXTERNAL] IL-18 synergizes with IL-12 to drive IFN-γ production by T cells and NK cells.
[Refs: PMID:20027291, PMID:19088061] (GO annotation refs - both IL18 and IL12B annotated to IFN-γ production)
```

When genes in an `[EXTERNAL]` claim happen to be annotated to the relevant biological process, GO annotation PMIDs can serve as a first-pass reference source **before** escalating to literature search.

**Updated strategy**: Check GO annotation PMIDs for ALL claim types first, then escalate to artl-mcp.

### Reference Lookup by Assertion Complexity

| Assertion Type | Example | Best Source |
|----------------|---------|-------------|
| Single gene, single process | RELA → NF-κB | GO annotation PMID |
| Multi-gene, same process | IL1B + IL1R1 + IRAK2 → IL-1 signaling | GO annotation (PMID:10383454) |
| Multi-gene, multi-process | RELA + NFKB1 across bacterial + cytokine + angiogenesis | artl-mcp |
| [EXTERNAL] with relevant annotation | IL18 + IL12B IFN-γ synergy | GO annotation first, then artl-mcp |
| [EXTERNAL] mechanistic | IL-1β fever via PGE2 | artl-mcp |

### Tiered Reference Validation Strategy

Lazy evaluation - escalate effort only as needed:

```
Tier 1: Abstract scan (cheap, fast)
   │
   ├─ Found support? → Done ✓
   │
   └─ Promising candidates? → Tier 2
                │
Tier 2: Full text + keyword grep (moderate cost)
   │
   ├─ Found support? → Done ✓
   │
   └─ Still promising? → Tier 3
                │
Tier 3: Section-targeted read (Results > Conclusions > Intro, skip Methods)
   │
   ├─ Found support? → Done ✓
   │
   └─ Not found → Flag for user + suggest deep search
```

**Design principles**:
- Early stopping: First adequate reference wins (not doing literature review)
- Candidate limit: Top 5 PMIDs per assertion to bound costs
- Section priority: Results > Conclusions > Intro (Methods rarely has interpretation)
- Graceful degradation: Flag unsupported claims honestly

**Goal**: Credibility, not completeness. Users own final literature synthesis.

### Workflow Validated

```
Themes → LLM Summary → Claim Extraction → Atomic Assertions
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    │ Simple/Multi-gene                Complex/External │
                    ↓                                                   ↓
           GO Annotation PMIDs                                   artl-mcp
           (check first for ALL                              (tiered search)
            claim types)                                            │
                    │                                                   │
                    └─────────────────────────┬─────────────────────────┘
                                              ↓
                                    Inject References
```

### LLM Step: Atomic Assertion Extraction

Claims must be parsed into atomic assertions with:
- `genes`: List of gene symbols mentioned
- `go_term_ids`: Mapped from natural language to theme GO term IDs
- `is_multi_gene`: Boolean
- `is_multi_process`: Boolean

**Process name → GO term mapping**: LLM maps claim language to GO terms from bounded theme set (87-106 terms). Fallback: embedding similarity.

### Output Files

| File | Purpose |
|------|---------|
| `results/reference_retrieval/llm_input_themes.txt` | Themes formatted for LLM |
| `results/reference_retrieval/llm_summary.txt` | Provenance-labeled summary |
| `results/reference_retrieval/atomic_assertions.json` | Parsed assertions |
| `results/reference_retrieval/checkpoint_step8_references.json` | Programmatic ref results |
| `results/reference_retrieval/artl_mcp_references.json` | Literature search results |
| `results/reference_retrieval/final_referenced_summary.md` | Combined output |

### High-Quality Reference Matches

| PMID | Claim | Match Quality |
|------|-------|---------------|
| 10383454 | IL-1 signaling axis (IL1B, IL1R1, IRAK2) | Excellent - multi-gene same process |
| 20027291 | IL18/IL12B IFN-γ synergy | Excellent - both genes annotated |
| 40917792 | C3AR1/C5AR1 angiogenesis | Excellent - abstract directly states "C3a and C5a...facilitating angiogenesis" |
| 16880211 | CD14/TLR1/TLR2 bacterial sensing | Excellent - multi-gene same process |

### Final Testing Round [2026-02-11]

**Tier 1 (Abstract) Validation:**

| PMID | Claim | Abstract Evidence | Result |
|------|-------|-------------------|--------|
| 10383454 | IL-1 signaling axis | "signal transducer for interleukin-1" | ✅ Pass |
| 20027291 | IL18/IL12B → IFN-γ | "IL-18...induced IL-12 production...IFN-gamma" | ✅ Pass |
| 16880211 | TLR2/TLR1 sensing | "TLR2 forms heterodimers with TLR1 and TLR6" | ✅ Pass |

**Tier 2 (Full-text grep) Validation:**

| PMID | Claim | Tier 1 | Tier 2 | Result |
|------|-------|--------|--------|--------|
| 39583895 | IL-1β → PGE2 → fever | PGE2/hypothalamus ✓, IL-1β ✗ | N/A | ⚠️ Partial |
| 41298282 | IL-1β → fever | No mechanism | grep "IL-1" → 0 hits | ❌ Reject |

**Findings:**
1. GO annotation PMIDs are high quality - all tested passed Tier 1
2. Tiered approach correctly filters non-supporting papers
3. [EXTERNAL] mechanistic claims ("IL-1β induces fever via PGE2") are harder - textbook knowledge not always in single papers

### Wikipedia Strategy for Textbook Knowledge

**Problem**: Well-established mechanisms (e.g., "IL-1β induces fever via PGE2") are textbook knowledge but may not have a single paper stating them explicitly in abstract.

**Solution**: Use Wikipedia as an intermediary source for textbook claims.

**Rationale**:
- Wikipedia articles on biological mechanisms typically cite primary literature
- Search pattern: `"{mechanism} wikipedia"` → extract refs from Wikipedia article
- Example: "IL-1β induces fever via PGE2 wikipedia" → Fever and IL-1β pages both have this info with refs

**Implementation approach**:
1. For [EXTERNAL] claims where artl-mcp doesn't find direct support
2. Search Wikipedia for the mechanism
3. Extract cited PMIDs from Wikipedia article
4. Validate those PMIDs support the claim

**Technical note**: Wikipedia blocks simple web fetch. Requires:
- Playwright MCP for JavaScript rendering, OR
- Wikipedia API for structured content extraction

**Decision**: Defer Wikipedia integration to Ring 1. For MVP, flag unsupported [EXTERNAL] claims for user review.

### Next Steps

**Reference retrieval:**
- [x] Build exploration script with interactive workflow
- [x] Test GO annotation programmatic lookup
- [x] Test artl-mcp for complex/[EXTERNAL] claims
- [x] Document tiered validation strategy
- [x] Test abstract retrieval for relevance scoring
- [x] Test full-text grep for keyword validation
- [x] Final testing round complete

**Implementation (MVP):**
- [x] Review existing code structure
- [x] Read SCAFFOLD_GUIDE.md for implementation patterns
- [x] Create implementation plan
- [x] Implement reference retrieval pipeline
- [x] Achieve 60% test coverage (CONSTRAINT)
- [x] Add to CLI as `--add-references` flag

---

## artl-mcp via cellsem-llm-client [2026-02-15]

### Context

Ring 0 Phase 3 exports unresolved assertions (complex multi-gene/multi-process claims and [EXTERNAL] claims without GO annotation support) to `*_artl_queries.json`. These need literature search via Europe PMC to find supporting references. The `cellsem-llm-client` library now has `MCPToolSource` which can connect to MCP servers and expose their tools to LLM agents.

**Branch**: `ring1_artl_mcp_references`
**Exploration script**: `exploration/11_artl_mcp_via_llm.py`

### Architecture: LLM-Driven Tool Use

```
MCPToolSource("uvx artl-mcp")     cellsem-llm-client
        │                              │
        │  stdio transport             │  LiteLLMAgent
        │  discovers 6 tools           │  query_unified(tools=...)
        ↓                              ↓
┌─────────────────┐            ┌──────────────────┐
│ artl-mcp server │◄──────────►│ LLM (gpt-4o-mini)│
│ (Europe PMC)    │  tool calls│                  │
│                 │  & results │                  │
└─────────────────┘            └──────────────────┘
```

Key pattern:
```python
from cellsem_llm_client import LiteLLMAgent, MCPToolSource

with MCPToolSource("uvx artl-mcp") as source:
    agent = LiteLLMAgent(model="gpt-4o-mini", api_key=key, max_tokens=2000)
    result = agent.query_unified(
        message=user_prompt,
        system_message=system_prompt,
        tools=source.tools,
        max_turns=8,
    )
```

### Test Results (exploration/11_artl_mcp_via_llm.py)

Four progressive tests, all passing:

| Step | What | LLM? | Result |
|------|------|------|--------|
| 1 | MCPToolSource discovers artl-mcp tools | No | 6 tools found via stdio |
| 2 | Direct tool call (search_europepmc_papers) | No | Papers returned correctly |
| 3 | LLM agent + tools: single assertion | Yes | 3 refs found, $0.003 |
| 4 | Batch from real artl_queries.json (2 assertions) | Yes | Both resolved, $0.007 total |

### Step 3 Detail: Single Assertion

**Input**: "ATM and BRCA1 cooperate in DNA damage response, with ATM phosphorylating BRCA1 to activate homologous recombination repair."

**Output** (gpt-4o-mini, 1 search tool call):
- PMID:41183146 - ATM-TGS1-BRCA1 axis in pancreatic cancer
- PMID:41597237 - Daxx-dependent HR repair via ATM/ATR phosphorylation
- PMID:41243967 - GSK3B and BRCA1-independent PARP inhibitor sensitivity

**Cost**: $0.0026 (14k input + 480 output tokens)

### Step 4 Detail: Batch from Real Queries

Used `results/ref_test_artl_queries.json` (P53/DNA damage gene set, 14 assertions exported from Phase 3).

**Assertion 1**: "Co-occurrence of ATM, BRCA1, BRCA2, TP53 suggests robust regulatory network"
- Europe PMC returned 503 on first query, LLM retried with simpler terms
- Found references including review on hereditary cancer syndromes
- Cost: $0.0056

**Assertion 2**: "ATM and BRCA1 in DNA repair and apoptosis under oxidative challenge"
- Found refs on obesity-induced oxidative stress + DNA damage response
- Cost: $0.0015

### Key Findings

1. **MCPToolSource works with stdio**: `"uvx artl-mcp"` connects cleanly, discovers all 6 tools
2. **Tool loop handles errors**: When Europe PMC returns 503, LLM retries with different queries
3. **Cost is low**: ~$0.003-0.006 per assertion with gpt-4o-mini
4. **max_turns=8 needed**: Complex assertions trigger multiple search/validate cycles
5. **Pydantic warnings are cosmetic**: LiteLLM emits serialization warnings, don't affect results
6. **Session lifecycle clean**: Context manager handles MCP server startup/shutdown

### Observations for Production Integration

**What works well**:
- LLM autonomously picks good search terms from assertion text
- LLM uses get_europepmc_paper_by_id to validate candidates before returning
- JSON output format is consistent and parseable

**What needs design work**:
- Currently one MCPToolSource per batch = one artl-mcp server process per batch; should reuse across assertions
- No tiered validation yet (abstract → full text → section read) — LLM just searches and returns
- Need to decide: let LLM validate relevance (current) vs programmatic abstract grep (cheaper, more reproducible)
- Cost projection: 14 assertions × $0.004 = ~$0.06 per analysis — acceptable

### Next Steps

- [ ] Decide validation approach: LLM-judged vs programmatic abstract grep vs hybrid
- [ ] Implement production service wrapping MCPToolSource + LiteLLMAgent
- [ ] Single MCPToolSource session for all assertions in a batch
- [ ] Add to CLI pipeline: after Phase 3 GAF lookup, run artl-mcp for unresolved
- [ ] Integration test with real API
- [ ] Update ROADMAP.md with revised Ring 1 scope
