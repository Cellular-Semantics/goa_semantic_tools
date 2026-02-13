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

# With LLM explanations (Phase 2)
# Requires OPENAI_API_KEY or ANTHROPIC_API_KEY in environment
uv run go-enrichment \
  --genes TP53,BRCA1,BRCA2,PTEN,RB1,APC \
  --output results/ \
  --explain \
  --model gpt-4o
```

**Available options:**
- `--genes`: Comma-separated gene symbols
- `--genes-file`: File with gene symbols (one per line)
- `--output`, `-o`: Output directory (required)
- `--species`: `human` or `mouse` (default: `human`)
- `--top-n`: Number of cluster roots per namespace (default: `5`)
- `--fdr`: FDR threshold (default: `0.05`)
- `--name`: Custom name for output file (default: auto-generated)
- `--explain`: Generate LLM explanations (Phase 2, requires API key)
- `--model`: LLM model for explanations (default: `gpt-4o`)
  - Supported: `gpt-4o`, `gpt-4o-mini`, `claude-sonnet-4-20250514`
  - **Not supported**: `gpt-4` (old model, no structured output)

#### Python API

**Phase 1: GO Enrichment Analysis**

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

**Phase 2: LLM-Generated Explanations**

```python
from goa_semantic_tools.services import run_go_enrichment, generate_explanations

# Phase 1: Run enrichment
enrichment_result = run_go_enrichment(
    gene_symbols=["TP53", "BRCA1", "BRCA2", "PTEN", "RB1", "APC"],
    species="human"
)

# Phase 2: Generate natural language explanations
# Requires OPENAI_API_KEY or ANTHROPIC_API_KEY in environment
explanation_result = generate_explanations(
    enrichment_output=enrichment_result,
    model="gpt-4o",          # or "gpt-4o-mini", "claude-sonnet-4-20250514"
    temperature=0.1,
    max_tokens=3000
)

# Access explanations
for explanation in explanation_result['explanations']:
    print(f"\nCluster: {explanation['cluster_name']}")
    print(f"Summary: {explanation['summary']}")
    print(f"\nDetailed Explanation:\n{explanation['detailed_explanation']}")
    print(f"\nKey Insights:")
    for insight in explanation['key_insights']:
        print(f"  • {insight}")

# Overall summary synthesizing all clusters
print(f"\nOverall Summary:\n{explanation_result['overall_summary']}")
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
│   ├── go_enrichment_service.py     # Phase 1: Enrichment pipeline
│   ├── go_explanation_service.py    # Phase 2: LLM explanations
│   └── go_explanation.prompt.yaml   # Explanation prompt template
├── utils/
│   ├── data_downloader.py           # Download & cache GO/GAF data
│   ├── go_data_loader.py            # Load data with GOATOOLS
│   └── go_hierarchy.py              # Top-N clustering algorithm
└── schemas/
    ├── go_enrichment_input.schema.json
    ├── go_enrichment_output.schema.json
    └── go_explanation_output.schema.json
```

### Dependencies

- **Python 3.14+**
- **GOATOOLS**: GO enrichment analysis
- **cellsem-llm-client**: LLM client for structured output generation
- **requests**: Data downloads
- **jsonschema**: Schema validation
- **pydantic**: Data validation and modeling

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

**Current Status**: Ring 0 Complete ✅

**Phase 1** (Complete):
- Hierarchical GO enrichment with top-N clustering
- CLI runner (`go-enrichment` command)
- Python API (`run_go_enrichment`)
- Download-and-cache data strategy

**Phase 2** (Complete):
- LLM-based natural language explanations of enrichment results
- Research biologist-focused explanations (WHY/WHAT/HOW)
- Python API (`generate_explanations`)
- CLI integration (`--explain` flag)

**Next Steps** (Awaiting User Feedback):
- Batch processing support
- Integration tests with real LLM calls

**Ring 1** (after user validation):
- GO term definitions in explanations
- Technical bioinformatician explanations (optional mode)
- DeepSearch integration for experimental context
- RAG with literature references
- Graph visualizations

## 📄 License

MIT License - see `LICENSE` for details.

---

**Questions?** See `GOATOOLS_FINDINGS.md` for technical details or `CLAUDE.md` for development guidelines.
