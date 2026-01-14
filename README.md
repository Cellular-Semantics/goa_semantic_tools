# goa_semantic_tools

[![Tests](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml)
[![coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Cellular-Semantics/goa_semantic_tools/main/.github/badges/coverage.json)](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

**Hierarchical GO enrichment analysis with top-N roots clustering**

Performs Gene Ontology (GO) enrichment analysis and organizes results into interpretable hierarchical clusters. Reduces hundreds of enriched terms to a small number of meaningful biological themes.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Cellular-Semantics/goa_semantic_tools.git
cd goa_semantic_tools

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create environment and install dependencies
uv sync
```

**First run**: GO ontology (~30MB) and gene annotations (~140MB) will be downloaded automatically and cached in `reference_data/`.

### Usage

#### Command Line (Recommended for Quick Testing)

```bash
# Comma-separated gene list
uv run go-enrichment --genes TP53,BRCA1,BRCA2,PTEN,RB1,APC --output results/

# From a file (one gene per line, # for comments)
uv run go-enrichment --genes-file genes.txt --output results/

# With custom parameters
uv run go-enrichment \
  --genes TP53,BRCA1,BRCA2 \
  --species mouse \
  --top-n 10 \
  --fdr 0.01 \
  --output results/ \
  --name my_analysis
```

**Available options:**
- `--genes`: Comma-separated gene symbols
- `--genes-file`: File with gene symbols (one per line)
- `--output`, `-o`: Output directory (required)
- `--species`: `human` or `mouse` (default: `human`)
- `--top-n`: Number of cluster roots per namespace (default: `5`)
- `--fdr`: FDR threshold (default: `0.05`)
- `--name`: Custom name for output file (default: auto-generated)

#### Python API

```python
from goa_semantic_tools.services import run_go_enrichment

# Run enrichment analysis
result = run_go_enrichment(
    gene_symbols=["TP53", "BRCA1", "BRCA2", "PTEN", "RB1", "APC"],
    species="human",         # or "mouse"
    top_n_roots=5,           # Number of cluster roots per namespace
    fdr_threshold=0.05       # FDR significance threshold
)

# Access results
print(f"Found {len(result['clusters'])} clusters")
print(f"Total enriched terms: {result['metadata']['total_enriched_terms']}")

# Explore first cluster
cluster = result['clusters'][0]
print(f"\nCluster: {cluster['root_term']['name']}")
print(f"  FDR: {cluster['root_term']['fdr']:.2e}")
print(f"  Fold enrichment: {cluster['root_term']['fold_enrichment']:.2f}x")
print(f"  Study genes: {cluster['root_term']['study_genes']}")
print(f"  Member terms: {len(cluster['member_terms'])}")
```

### Example Output

```python
{
    "clusters": [
        {
            "root_term": {
                "go_id": "GO:0008285",
                "name": "negative regulation of cell population proliferation",
                "namespace": "biological_process",
                "fdr": 3.98e-09,
                "fold_enrichment": 25.10,
                "study_count": 10,
                "study_genes": ["APC", "ATM", "BRCA2", "CDKN2A", ...]
            },
            "member_terms": [
                # Descendant enriched terms...
            ],
            "contributing_genes": [
                {
                    "gene_symbol": "TP53",
                    "direct_annotations": [
                        {
                            "go_id": "GO:0008285",
                            "go_name": "negative regulation of...",
                            "evidence_code": "IDA"
                        }
                    ]
                }
            ]
        }
    ],
    "metadata": {
        "input_genes_count": 14,
        "genes_with_annotations": 14,
        "total_enriched_terms": 282,
        "clusters_count": 15,
        "fdr_threshold": 0.05,
        "species": "human"
    }
}
```

## 🎯 What It Does

1. **Downloads reference data** (first run only):
   - GO ontology from GO Consortium PURL
   - Gene annotations (GAF) from EBI QuickGO
   - Cached in `reference_data/` for subsequent runs

2. **Runs GO enrichment** using GOATOOLS:
   - Fisher's exact test with FDR correction
   - Propagates counts up GO hierarchy
   - Finds significantly enriched terms

3. **Clusters results hierarchically**:
   - Selects top-N most significant terms as "cluster roots"
   - Groups descendant terms under appropriate roots
   - Reduces 100+ terms to 5-10 interpretable themes

4. **Provides gene drill-down**:
   - Shows which genes contribute to each cluster
   - Lists direct GO annotations with evidence codes
   - Explains where enrichment comes from

## 📊 Output Structure

The result follows `go_enrichment_output.schema.json`:

- **`clusters`**: Array of hierarchical clusters
  - **`root_term`**: Most significant term (cluster root)
    - GO ID, name, namespace
    - P-value, FDR, fold enrichment
    - Study genes annotated to this term
  - **`member_terms`**: Descendant enriched terms in same hierarchy
  - **`contributing_genes`**: Genes with their direct annotations

- **`metadata`**: Analysis summary
  - Input/found gene counts
  - Total enriched terms before clustering
  - Number of clusters created
  - Parameters used

## 🛠️ Development

### Running Tests

```bash
# Integration tests (requires downloaded data)
uv run pytest -m integration

# All tests
uv run pytest
```

### Project Structure

```
src/goa_semantic_tools/goa_semantic_tools/
├── services/
│   └── go_enrichment_service.py    # Main enrichment pipeline
├── utils/
│   ├── data_downloader.py           # Download & cache GO/GAF data
│   ├── go_data_loader.py            # Load data with GOATOOLS
│   └── go_hierarchy.py              # Top-N clustering algorithm
└── schemas/
    ├── go_enrichment_input.schema.json
    └── go_enrichment_output.schema.json
```

### Dependencies

- **Python 3.14+**
- **GOATOOLS**: GO enrichment analysis
- **requests**: Data downloads
- **jsonschema**: Schema validation

All managed via `uv` - see `pyproject.toml`.

### Data Sources

- **GO Ontology**: http://purl.obolibrary.org/obo/go/go-basic.obo
- **Human annotations**: http://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/
- **Mouse annotations**: http://ftp.ebi.ac.uk/pub/databases/GO/goa/MOUSE/

Data is downloaded on first run and cached in `reference_data/` (gitignored).

## 📖 Documentation

- **`GOATOOLS_FINDINGS.md`**: Detailed API behavior and constraints from Week 0 validation
- **`CLAUDE.md`**: Development philosophy and Ring-based approach
- **`SCAFFOLD_GUIDE.md`**: Project scaffold and architecture decisions

## 🚧 Roadmap

**Current Status**: Ring 0 Phase 1 Complete ✅
- Hierarchical GO enrichment with top-N clustering
- CLI runner (`go-enrichment` command)
- Python API
- Download-and-cache data strategy

**Phase 2** (next):
- LLM-based natural language explanations of enrichment results
- Batch processing support

**Ring 1** (after user validation):
- GO term definitions in explanations
- DeepSearch integration for experimental context
- RAG with literature references
- Graph visualizations

## 📄 License

MIT License - see `LICENSE` for details.

---

**Questions?** See `GOATOOLS_FINDINGS.md` for technical details or `CLAUDE.md` for development guidelines.
