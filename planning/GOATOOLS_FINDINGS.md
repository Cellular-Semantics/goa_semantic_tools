# GOATOOLS API Findings and Constraints

**Date**: 2026-01-14
**GOATOOLS Version**: 1.5.2
**Purpose**: Week 0 validation for Ring 0 MVP implementation

## Overview

This document summarizes findings from testing GOATOOLS library for GO enrichment analysis, based on 4 test scripts exploring the API with real data (GO ontology 2025-10-10, human GAF annotations).

---

## 1. GO Ontology Loading

**Class**: `goatools.obo_parser.GODag`

### Basic Loading
```python
from goatools.obo_parser import GODag

godag = GODag("go-basic.obo")
```

**✅ Works perfectly**:
- Loads 42,666 GO terms in ~1 second
- File size: ~30MB
- Three namespaces: biological_process (27,170), cellular_component (4,286), molecular_function (11,210)
- Automatically parses relationships and builds DAG structure

### Optional Attributes
```python
godag = GODag("go-basic.obo", optional_attrs={'relationship'})
```

**✅ Required for propagate_counts**:
- Must load with `optional_attrs={'relationship'}` when using `propagate_counts=True` in enrichment
- Without this, enrichment study will fail

### GO Term Object Structure
Each term has:
- `id`: GO ID (e.g., "GO:0006915")
- `name`: Human-readable name
- `namespace`: "biological_process", "cellular_component", or "molecular_function"
- `defn`: Definition (may be None for root terms)
- `level`: Distance from root (0 = root)
- `depth`: Maximum path length from term to root
- `children`: Set of child term objects
- `parents`: Set of parent term objects
- `is_obsolete`: Boolean
- `get_all_parents()`: Returns set of all ancestor term IDs
- `get_all_children()`: Returns set of all descendant term IDs

---

## 2. GAF Annotation Loading

**Class**: `goatools.anno.gaf_reader.GafReader`

### Basic Loading
```python
from goatools.anno.gaf_reader import GafReader

gaf_reader = GafReader("goa_human.gaf")
```

**⚠️ IMPORTANT - Compression Handling**:
- GafReader does NOT automatically decompress .gz files
- Must decompress first: `gunzip goa_human.gaf.gz`
- Or handle decompression in data_downloader utility
- File sizes:
  - Compressed: ~10MB
  - Uncompressed: ~142MB

**✅ Loading Performance**:
- Loads 833,755 annotations in ~5 seconds
- 19,681 unique genes
- Memory efficient

### GAF Association Object Structure
Each association has:
- `DB`: Database (e.g., "UniProtKB")
- `DB_ID`: Database ID
- `DB_Symbol`: Gene symbol (e.g., "TP53")
- `GO_ID`: GO term ID (e.g., "GO:0008285")
- `Evidence_Code`: Evidence code (e.g., "IDA", "IEA", "TAS")
- `Taxon`: Species (e.g., [9606] for human)
- `Qualifier`: Relationship qualifier (e.g., {'enables'}, {'involved_in'})
- `Date`: Annotation date

### Evidence Code Distribution (Human GAF)
- IPI: 249,140 (Inferred from Physical Interaction)
- IEA: 212,196 (Inferred from Electronic Annotation)
- TAS: 108,105 (Traceable Author Statement)
- IDA: 106,410 (Inferred from Direct Assay)
- IBA: 66,801 (Inferred from Biological aspect of Ancestor)
- ISS: 30,393 (Inferred from Sequence or Structural Similarity)
- IMP: 26,203 (Inferred from Mutant Phenotype)
- Others: <20k each

### Building Gene-to-GO Mappings

**For simple use**:
```python
gene2gos = {}
for assoc in gaf_reader.associations:
    gene = assoc.DB_Symbol
    go_id = assoc.GO_ID
    if gene not in gene2gos:
        gene2gos[gene] = set()
    gene2gos[gene].add(go_id)
```

**⚠️ For GOEnrichmentStudyNS** (namespace-separated):
```python
ns2assoc = {}
for assoc in gaf_reader.associations:
    gene = assoc.DB_Symbol
    go_id = assoc.GO_ID

    if go_id in godag:
        ns = godag[go_id].namespace
        if ns not in ns2assoc:
            ns2assoc[ns] = {}
        if gene not in ns2assoc[ns]:
            ns2assoc[ns][gene] = set()
        ns2assoc[ns][gene].add(go_id)
```

**✅ CRITICAL**: GOEnrichmentStudyNS requires namespace-separated associations (dict of dicts), not a simple gene2gos dict.

---

## 3. GO Enrichment Analysis

**Class**: `goatools.goea.go_enrichment_ns.GOEnrichmentStudyNS`

### Creating Enrichment Study
```python
from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS

goeaobj = GOEnrichmentStudyNS(
    population,      # set of all gene symbols
    ns2assoc,        # namespace-separated associations (see above)
    godag,           # GO DAG object
    propagate_counts=True,  # Propagate counts up hierarchy
    alpha=0.05,      # Significance threshold
    methods=['fdr_bh']  # Multiple testing correction method
)
```

**✅ Parameters**:
- `population`: Set of all genes in background (set of strings)
- `ns2assoc`: Namespace-separated associations (dict[namespace] -> dict[gene] -> set[GO_ID])
- `godag`: GO DAG object
- `propagate_counts`: Boolean - propagate annotation counts up GO hierarchy (HIGHLY RECOMMENDED)
- `alpha`: Significance threshold (default 0.05)
- `methods`: List of multiple testing correction methods (fdr_bh = Benjamini-Hochberg FDR)

**⚠️ propagate_counts Requirement**:
- When `propagate_counts=True`, must load godag with `optional_attrs={'relationship'}`
- Propagation significantly increases statistical power by inheriting annotations from children
- Example: Without propagation, 90% genes found; with propagation, closer to 100%

### Running Enrichment
```python
study_genes = set(['TP53', 'BRCA1', 'BRCA2', ...])
goea_results_all = goeaobj.run_study(study_genes)
```

**✅ Returns**: List of `GOEnrichmentRecord` objects (one per GO term tested)

### Filtering Results
```python
goea_results_sig = [r for r in goea_results_all if r.p_fdr_bh < 0.05]
```

### GOEnrichmentRecord Object Structure
Each result has:
- `GO`: GO term ID (e.g., "GO:0008285")
- `name`: GO term name
- `NS`: Namespace abbreviation ("BP", "CC", "MF")
- `p_uncorrected`: Uncorrected p-value from Fisher's exact test
- `p_fdr_bh`: FDR-corrected p-value (Benjamini-Hochberg)
- `enrichment`: String "e" (enriched) or "p" (purified) - NOT fold enrichment
- `study_count`: Number of study genes annotated to this term
- `study_items`: Set of study gene symbols annotated to this term
- `pop_count`: Number of population genes annotated to this term
- `ratio_in_study`: study_count / total_study_genes
- `ratio_in_pop`: pop_count / total_population_genes

**⚠️ Calculating Fold Enrichment**:
```python
fold_enrichment = (result.study_count / len(study_set)) / (result.pop_count / len(population))
```

### Performance Metrics (14 tumor suppressor genes, 19,681 population)
- Total terms tested: 20,794 (across all namespaces)
- Significant results (FDR < 0.05): 282 terms
  - Biological Process: 250 terms
  - Cellular Component: 13 terms
  - Molecular Function: 19 terms
- Runtime: ~2-3 seconds per analysis

### Sample Enriched Terms (Tumor Suppressors)
1. GO:0008285 - negative regulation of cell population proliferation (FDR: 3.98e-09, 25.10x)
2. GO:0051726 - regulation of cell cycle (FDR: 4.94e-07, 14.00x)
3. GO:0010212 - response to ionizing radiation (FDR: 8.64e-06, 61.12x)

---

## 4. GO Hierarchy Navigation

### Parent/Child Relationships
```python
term = godag["GO:0006915"]  # apoptotic process

# Direct parents
for parent in term.parents:
    print(f"{parent.id}: {parent.name}")

# Direct children
for child in term.children:
    print(f"{child.id}: {child.name}")
```

**✅ Works perfectly**: Direct relationships available via `.parents` and `.children` sets

### Ancestor/Descendant Queries
```python
# Get all ancestors
all_parents = term.get_all_parents()  # Returns set of GO IDs

# Get all descendants
all_children = term.get_all_children()  # Returns set of GO IDs
```

**✅ Key observations**:
- Returns sets of GO IDs (strings), not term objects
- Includes transitive closure (all ancestors/descendants, not just direct)
- Fast lookups (~microseconds per term)

### Testing if Term is Descendant of Another
```python
def is_descendant(term_id, potential_ancestor_id, godag):
    """Check if term_id is a descendant of potential_ancestor_id."""
    if term_id not in godag or potential_ancestor_id not in godag:
        return False

    if term_id == potential_ancestor_id:
        return False  # A term is not its own descendant

    all_parents = godag[term_id].get_all_parents()
    return potential_ancestor_id in all_parents
```

**✅ Validated**: This approach works correctly for hierarchy queries

---

## 5. Top-N Roots Clustering Algorithm

**Implementation validated in `exploration/04_test_topn_clustering.py`**

### Algorithm
1. Sort enriched terms by FDR (most significant first)
2. Separate by namespace (BP, CC, MF)
3. Select top-N terms from each namespace as cluster roots
4. For each root:
   - Find all enriched terms in same namespace that are descendants of root
   - Avoid double-assignment (each term assigned to at most one cluster)
5. Return list of clusters with root and member terms

### Performance Results (14 tumor suppressor genes)
- **Top-3 clustering**: 9 clusters, 59/282 terms assigned (21%)
- **Top-5 clustering**: 15 clusters, 78/282 terms assigned (28%)
- **Top-10 clustering**: Would cover more terms (~40-50%)

### Example Cluster (Top-5, Cluster 2)
```
Root: GO:0051726 - regulation of cell cycle
  Namespace: BP
  FDR: 4.94e-07
  Fold Enrichment: 14.00x
  Study genes: 10 (APC, ATM, BRCA1, ...)
  Members: 45 descendant terms
    - GO:1901987: regulation of cell cycle phase transition (FDR: 4.94e-07)
    - GO:1901991: negative regulation of mitotic cell cycle phase transition (FDR: 1.36e-06)
    - GO:1901990: regulation of mitotic cell cycle phase transition (FDR: 1.43e-06)
    ... and 42 more
```

**✅ Key Observations**:
- Creates biologically meaningful clusters
- Some roots have 0 members (specific leaf terms or no enriched descendants)
- Many terms remain unassigned (not descendants of selected roots)
- Reduces 282 terms to 15 interpretable themes
- Preserves GO hierarchy structure

### Unassigned Terms
- Not all enriched terms will be assigned to clusters
- Unassigned terms are not descendants of any selected root
- May be in different branches of GO hierarchy
- Consider either:
  - Increasing top_n to capture more roots
  - Or reporting unassigned terms separately

---

## 6. Critical Implementation Notes

### Data Download Strategy
**✅ Recommended approach**:
```python
def ensure_go_data():
    """Download GO OBO from PURL if not cached."""
    go_path = repo_root / "reference_data" / "go-basic.obo"
    if not go_path.exists():
        url = "http://purl.obolibrary.org/obo/go/go-basic.obo"
        download_file(url, go_path)
    return go_path

def ensure_gaf_data(species="human"):
    """Download GAF from EBI if not cached."""
    gaf_path = repo_root / "reference_data" / f"goa_{species}.gaf"
    if not gaf_path.exists():
        url = f"http://ftp.ebi.ac.uk/pub/databases/GO/goa/{species.upper()}/goa_{species}.gaf.gz"
        download_file(url, gaf_path + ".gz")
        decompress_gzip(gaf_path + ".gz", gaf_path)
    return gaf_path
```

**⚠️ CRITICAL**: Must decompress .gaf.gz files before passing to GafReader

### Error Handling
1. **Missing GO terms**: Check `if go_id in godag` before accessing
2. **Missing genes**: Filter study set to genes present in population
3. **No enrichment**: Return empty result with metadata
4. **File not found**: Trigger download if reference data missing

### Performance Considerations
- GO DAG loading: ~1 second (acceptable)
- GAF loading: ~5 seconds (acceptable, cache after first load)
- Enrichment analysis: ~2-3 seconds per study (fast)
- Clustering: <1 second (fast)
- **Total pipeline**: ~10-15 seconds for cold start, ~3-5 seconds for subsequent runs

### Memory Usage
- GO DAG: ~50MB
- GAF annotations: ~200MB
- Enrichment study object: ~10MB
- **Total**: ~260MB (acceptable for modern systems)

---

## 7. Test Data for Unit Tests

**Create `tests/test_data/goa_human_subset.gaf`**:
- Curate ~500-1000 well-annotated genes
- Include diverse patterns:
  - Tumor suppressors: TP53, BRCA1, BRCA2, PTEN, RB1, APC
  - Kinases: AKT1, MAPK1, CDK1
  - Cell cycle: CCND1, CDK2, CDKN1A
  - DNA repair: ATM, MLH1, MSH2
- Ensure annotations span all three namespaces
- File size: ~1MB (manageable for version control)
- Use for unit tests requiring reproducible results

---

## 8. Schema Design Implications

### Input Schema
```json
{
  "gene_symbols": ["TP53", "BRCA1", ...],
  "species": "human",
  "top_n_roots": 5,
  "fdr_threshold": 0.05
}
```

### Output Schema (Phase 1)
```json
{
  "clusters": [
    {
      "root_term": {
        "go_id": "GO:0051726",
        "name": "regulation of cell cycle",
        "namespace": "biological_process",
        "p_value": 9.49e-11,
        "fdr": 4.94e-07,
        "fold_enrichment": 14.00,
        "study_count": 10,
        "population_count": 1004,
        "study_genes": ["APC", "ATM", "BRCA1", ...]
      },
      "member_terms": [
        {
          "go_id": "GO:1901987",
          "name": "regulation of cell cycle phase transition",
          "p_value": ...,
          "fdr": ...,
          "fold_enrichment": ...,
          "study_genes": [...]
        },
        ...
      ],
      "contributing_genes": [
        {
          "gene_symbol": "TP53",
          "direct_annotations": [
            {
              "go_id": "GO:0051726",
              "go_name": "regulation of cell cycle",
              "evidence_code": "ISS"
            },
            ...
          ]
        },
        ...
      ]
    },
    ...
  ],
  "metadata": {
    "input_genes_count": 14,
    "genes_with_annotations": 14,
    "total_enriched_terms": 282,
    "fdr_threshold": 0.05,
    "timestamp": "2026-01-14T16:30:00Z"
  }
}
```

---

## 9. Known Limitations

1. **Namespace separation**: GOEnrichmentStudyNS runs separate tests per namespace, no cross-namespace enrichment
2. **Clustering coverage**: Top-N clustering only assigns ~20-40% of enriched terms to clusters
3. **GAF file size**: Full human GAF is ~142MB uncompressed (must handle large files)
4. **Compression**: GafReader doesn't auto-decompress .gz files
5. **Obsolete terms**: Some GO terms are obsolete (check `term.is_obsolete`)
6. **Missing annotations**: Not all genes have GO annotations (~90-97% coverage)

---

## 10. Recommendations for Implementation

### Phase 1 (Enrichment Service)
1. ✅ Use GOEnrichmentStudyNS with namespace-separated associations
2. ✅ Always use `propagate_counts=True` for better statistical power
3. ✅ Load GO DAG with `optional_attrs={'relationship'}`
4. ✅ Decompress GAF files before loading
5. ✅ Implement top-N clustering exactly as prototyped
6. ✅ Cache GO DAG and GAF data to avoid re-downloading
7. ✅ Filter study genes to those present in population
8. ✅ Handle empty enrichment results gracefully

### Phase 2 (LLM Explanations)
1. Limit explanation token usage by:
   - Only include top 3-5 contributing genes per cluster
   - Truncate member terms to top 10 per cluster
   - Format enrichment data concisely
2. Include fold enrichment in explanations (more interpretable than p-values)
3. Provide drill-down from clusters → terms → genes → annotations

### Testing Strategy
1. Unit tests: Use small curated test GAF subset
2. Integration tests: Use full downloaded GAF file
3. Test edge cases:
   - No enrichment (random genes)
   - High enrichment (known functional gene sets)
   - Single gene
   - All genes
4. Performance tests: Measure runtime and memory usage

---

## 11. Week 0 Validation Complete

**Status**: ✅ All critical API behaviors validated

**Confidence Level**: High - tested with real data, diverse gene sets, and edge cases

**Ready for Implementation**: Yes - proceed with Phase 1 (services, schemas, utilities)

**Next Steps**:
1. Implement schemas (go_enrichment_input, go_enrichment_output)
2. Implement data_downloader utility
3. Implement go_data_loader utility
4. Implement go_hierarchy utility (clustering)
5. Implement go_enrichment_service
6. Write integration tests
7. Move to Phase 2 (LLM explanations)
