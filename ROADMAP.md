# GOA Semantic Tools - Development Roadmap

**Last Updated**: 2026-02-10

## Current Status

**Ring 0 Phase 1** (Complete): GO enrichment with top-N clustering
**Ring 0 Phase 2** (Complete): LLM-based explanations
**Ring 0 Phase 2.5** (In Progress): Improved clustering algorithm

---

## Ring 0 Phase 2.5: Leaf-First Clustering

### Problem with Top-N Roots
The original algorithm selects top-N most significant terms as cluster roots, but this creates:
- **Hierarchical redundancy**: Parent and children both selected (e.g., 4 vascular terms for same 8-14 genes)
- **Overly general terms**: "membrane" (107 genes) provides little insight
- **Context window bloat**: Redundant clusters waste tokens in LLM explanations

### Solution: Leaf-First Clustering
Instead of top-down (most significant), go bottom-up (most specific):

1. **Find enrichment leaves**: Terms with no enriched descendants
2. **Merge identical gene sets**: Collapse redundant siblings
3. **Check parent contribution**: Only include parent if adds >20% new genes
4. **Filter general terms**: Skip terms with >50 genes or >200% parent addition
5. **Two-threshold approach**: FDR 0.05 (high confidence) + FDR 0.10 (moderate)

### Results (Astrocytoma test case)
- **Before**: 12 clusters, 4 redundant vascular, general CC terms
- **After**: 15 themes, distinct biology, no redundancy
- **New discoveries**: Amyloid regulation, cAMP signaling at relaxed FDR

### Implementation Status
- [x] Prototype in `exploration/05_leaf_first_clustering.py`
- [ ] Integrate into main `go_hierarchy.py`
- [ ] Update CLI to use new algorithm
- [ ] Update explanation service for new format

---

## Future Enhancements (Ring 1+)

### 1. Annotation Depth Classification
Distinguish enrichment types based on where genes are annotated:

- **Specific enrichment**: Genes annotated directly to leaf term (e.g., BBB transport - 8 genes all directly annotated)
- **Category enrichment**: Genes annotated to general term, specific subtype unknown (e.g., cell adhesion - 17/23 directly annotated to parent)

This affects interpretation confidence and suggests where literature mining could help.

### 2. Literature Mining for Missing Themes

When we have "category enrichment" (genes at general level), mine literature to find common themes not captured in GO:

#### 2a. Direct Annotation References
- Extract PMIDs from gene annotations
- Identify papers that annotate multiple genes to same term
- Look for shared themes/mechanisms in those papers
- **Easier**: Data already available in GAF

#### 2b. Broader Literature Search
- Use DeepSearch/Perplexity to find connections
- Search for co-occurrence in abstracts/full text
- **Harder**: Requires external API, potential hallucination

### 3. Cross-Namespace Co-annotation

Strengthen biological interpretation by combining evidence across namespaces:

#### 3a. BP Co-annotation
- If genes share BP annotation from same reference → strong functional link
- Could reveal sub-themes within "category enrichment" cases
- Example: 5 genes annotated to "cell adhesion" from PMID:X might share specific mechanism

#### 3b. CC Co-annotation
- Genes in same cellular location + same BP = stronger evidence
- Example: "plasma membrane" + "cell adhesion" from same paper

#### 3c. Reference Co-occurrence Analysis
- Build graph: genes connected if annotated from same paper
- Cluster to find functionally coherent sub-groups
- Especially useful for broad categories

### 4. Evidence Aggregation

For enrichment leaves, aggregate evidence from child annotations:
- If gene is annotated to non-significant child term, pull up the PMID
- Show "evidence from more specific annotations" in reports
- Helps explain WHY the enrichment exists

### 5. Semantic Similarity Clustering

Alternative/complement to hierarchy-based clustering:
- Use GO term semantic similarity (IC-based) OR use embedding based similarity.
- Cluster terms by meaning, not just hierarchy
- Could help in sparse GO branches where IC heuristics fail

### 6. Improved LLM Explanations

Update explanation service for leaf-first output:
- Show core genes vs additional genes at broader level
- Flag "category enrichment" vs "specific enrichment"
- Include literature references from annotations
- Add confidence indicators

---

## Technical Debt / Improvements

- [ ] Add population counts to theme output (for fold enrichment transparency)
- [ ] Cache GO DAG loading (currently ~1s each run)
- [ ] Add integration tests for leaf-first clustering
- [ ] Schema updates for new theme structure
- [ ] Consider IC calculation for term specificity metrics

---

## Test Cases

### Astrocytoma Cluster 0 (200 genes)
Primary test case for algorithm development:
- Shows vascular hierarchy redundancy
- Has "category enrichment" example (cell adhesion)
- Has "specific enrichment" example (BBB transport)
- Brain-relevant terms (amyloid, cAMP)

### Benchmark Test Sets (MSigDB Hallmark)

Located in `input_data/benchmark_sets/test_lists/`:

**Positive controls** (should show expected enrichment):
- `hallmark_apoptosis.txt` - 161 genes
- `hallmark_dna_repair.txt` - 150 genes
- `hallmark_hypoxia.txt` - 200 genes
- `hallmark_inflammatory_response.txt` - 200 genes
- `hallmark_p53_pathway.txt` - 200 genes
- `hallmark_oxidative_phosphorylation.txt` - 200 genes

**Negative controls** (random, should show minimal enrichment):
- `random_50_genes.txt`, `random_100_genes.txt`, `random_200_genes.txt`

**Raw data** in `input_data/benchmark_sets/`:
- `hallmark_gene_sets.gmt` - All 50 MSigDB hallmark sets
- `gobp_gene_sets.gmt` - 7,608 GO BP gene sets from MSigDB

### Additional Test Cases Needed
- [ ] Rare disease genes (sparse GO coverage)
- [ ] Small gene set (<20 genes)

---

## Related Work / Comparison

Methods addressing GO enrichment redundancy:
- **topGO elim/weight** - Removes genes from parent terms if child is significant
- **REVIGO** - Semantic similarity clustering of GO terms
- **evoGO** (2025 preprint) - Redundancy minimization approach

---

## References

- `exploration/05_leaf_first_clustering.py` - Prototype implementation
- `results/leaf_first_themes.json` - Example output
- `results/fdr01_enrichment.json` - Test data (FDR 0.10)
- `GOATOOLS_FINDINGS.md` - GOATOOLS API documentation
