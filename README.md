# GOA Semantic Tools

[![Tests](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml)
[![coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Cellular-Semantics/goa_semantic_tools/main/.github/badges/coverage.json)](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

**Hierarchical GO enrichment analysis with depth-anchor clustering, provenance-labeled LLM explanations, and literature-grounded references**

GO enrichment analysis typically produces hundreds of statistically significant terms with heavy redundancy from parent-child overlaps. GOA Semantic Tools reduces these to a structured set of biological themes using a bottom-up depth-anchor algorithm, then generates provenance-labeled explanations grounded in real paper abstracts fetched from Europe PMC before the LLM call.

## Quick Start

### Installation

```bash
git clone https://github.com/Cellular-Semantics/goa_semantic_tools.git
cd goa_semantic_tools
curl -LsSf https://astral.sh/uv/install.sh | sh  # if uv not installed
uv sync
```

**First run**: GO ontology (~30MB) and gene annotations (~140MB) are downloaded automatically and cached in `reference_data/`.

### Usage

```bash
# Basic enrichment analysis
uv run go-enrichment --genes TP53,BRCA1,BRCA2,PTEN,RB1,APC -o results/my_analysis

# From a gene list file (one gene per line, # for comments)
uv run go-enrichment --genes-file genes.txt -o results/my_analysis

# With LLM explanation (requires OPENAI_API_KEY or ANTHROPIC_API_KEY)
uv run go-enrichment --genes-file genes.txt -o results/my_analysis --explain

# With LLM explanation + literature references (pre-fetches Europe PMC abstracts before LLM call)
uv run go-enrichment --genes-file genes.txt -o results/my_analysis --explain --add-references

# With references but without Europe PMC literature search (GAF annotations only)
uv run go-enrichment --genes-file genes.txt -o results/my_analysis --explain --add-references --no-literature-search

# Preview what would run without executing
uv run go-enrichment --genes-file genes.txt -o results/my_analysis --explain --dry-run
```

Output files are auto-named from the base path:
- `*_enrichment.json` - Structured enrichment results (themes, leaves, hub genes)
- `*_explanation.md` - Provenance-labeled biological summary with inline citations (if `--explain`)

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--genes` | | Comma-separated gene symbols |
| `--genes-file` | | File with gene symbols (one per line) |
| `-o`, `--output` | *(required)* | Output base path |
| `--species` | `human` | `human` or `mouse` |
| `--fdr` | `0.05` | FDR significance threshold |
| `--depth-min` | `4` | Min GO depth for anchor terms |
| `--depth-max` | `7` | Max GO depth for anchor terms |
| `--min-children` | `2` | Min enriched descendants to qualify as anchor |
| `--max-genes` | `30` | Filter overly general terms |
| `--explain` | off | Generate LLM explanation |
| `--model` | `gpt-4o` | LLM model (`gpt-4o`, `gpt-4o-mini`, `gpt-5`, `claude-sonnet-4-20250514`) |
| `--max-tokens` | model default | Override LLM output token limit (gpt-5 defaults to 32000; others 16000) |
| `--add-references` | off | Pre-fetch Europe PMC abstracts and inject inline citations (requires `--explain`) |
| `--no-literature-search` | off | Skip Europe PMC pre-fetch (use with `--add-references`) |
| `--dry-run` | off | Preview analysis plan without executing |

## How It Works

### 1. GO Enrichment (Phase 1)

Runs over-representation analysis (ORA) via GOATOOLS with Fisher's exact test and BH-corrected FDR. Downloads and caches GO ontology and GAF annotations automatically.

### 2. Leaf-First Theme Building (Phase 1)

Instead of selecting top-N most significant terms (which creates redundancy), the algorithm works bottom-up:

1. **Enrichment leaves**: Find the most specific enriched terms (no enriched descendants)
2. **Depth-anchor grouping**: Select intermediate-depth terms (depth 4-7) with 2+ enriched descendants as anchors, group specific terms beneath them
3. **Hub gene identification**: Flag genes appearing in 3+ themes as biological coordinators

Typical reduction: 50-75% fewer terms while preserving the biological signal.

### 3. Literature Pre-fetch + LLM Explanation (Phases 1b + 2)

When `--add-references` is used, paper abstracts are fetched from Europe PMC **before** the LLM call:

1. **Phase 1b**: For each theme, search Europe PMC (via artl-mcp) using top-ranked genes + anchor GO term name. All returned abstracts are injected into the theme context.
2. **Phase 2**: The LLM generates a provenance-labeled biological summary with inline citations (e.g. `PMID:10383454`) for claims grounded in the provided papers.

Provenance tags distinguish claim sources:

- **[DATA]**: Direct observations from enrichment (FDR values, gene counts, co-occurrence)
- **[INFERENCE]**: Logical deductions from co-annotation patterns
- **[EXTERNAL]**: Claims about known biology, cited from pre-fetched papers where available
- **[GO-HIERARCHY]**: Facts derived from GO parent-child structure

This lit-first approach eliminates the unresolved assertion problem: the LLM cites papers it has actually read rather than making claims that require retrospective validation.

## Python API

```python
from goa_semantic_tools.services import run_go_enrichment, generate_markdown_explanation

# Phase 1: Enrichment + theme building
result = run_go_enrichment(
    gene_symbols=["TP53", "BRCA1", "BRCA2", "PTEN", "RB1", "APC"],
    species="human",
    fdr_threshold=0.05,
    depth_range=(4, 7),
    min_children=2,
    max_genes=30,
)

# Access structured results
print(f"Enrichment leaves: {len(result['enrichment_leaves'])}")
print(f"Themes: {len(result['themes'])}")
print(f"Hub genes: {list(result['hub_genes'].keys())}")

# Phase 1b: Pre-fetch literature abstracts (optional, requires artl-mcp)
from goa_semantic_tools.services import fetch_abstracts_for_themes
paper_abstracts = fetch_abstracts_for_themes(
    themes=result["themes"],
    hub_genes=result["hub_genes"],
)

# Phase 2: LLM explanation (requires API key in environment)
# max_tokens defaults to 16000; gpt-5 automatically gets 32000
markdown = generate_markdown_explanation(
    enrichment_output=result,
    model="gpt-4o",
    paper_abstracts=paper_abstracts,  # LLM cites inline from provided abstracts
)
```

## Output Structure

The enrichment JSON contains:

- **`enrichment_leaves`**: Most specific enriched terms (GO ID, name, FDR, genes, depth)
- **`themes`**: Hierarchical groupings
  - `anchor_term`: Intermediate-depth grouping term
  - `specific_terms`: More specific terms grouped under the anchor
  - `anchor_confidence`: `"high"` (FDR < 0.05) or `"moderate"`
- **`hub_genes`**: Genes appearing across 3+ themes with theme count and list
- **`metadata`**: Input gene count, annotation coverage, total enriched terms, theme count

## Development

### Running Tests

```bash
uv run pytest -m unit          # Unit tests (CI)
uv run pytest -m integration   # Integration tests (requires downloaded data)
uv run pytest --cov            # With coverage
```

### Project Structure

```
src/goa_semantic_tools/goa_semantic_tools/
├── cli.py                                    # CLI entry point (go-enrichment)
├── services/
│   ├── go_enrichment_service.py              # ORA enrichment via GOATOOLS
│   ├── go_markdown_explanation_service.py    # LLM explanation (lit-first)
│   ├── go_explanation.prompt.yaml            # Explanation prompt template
│   ├── artl_literature_service.py            # Europe PMC abstract pre-fetch
│   ├── artl_literature_search.prompt.yaml    # Literature search prompt
│   ├── reference_retrieval_service.py        # Claim extraction + PMID utilities
│   └── reference_retrieval.prompt.yaml       # Assertion extraction prompt
├── utils/
│   ├── data_downloader.py                    # Download & cache GO/GAF data
│   ├── go_data_loader.py                     # Load data with GOATOOLS
│   ├── go_hierarchy.py                       # Leaf-first + depth-anchor algorithm
│   └── reference_index.py                    # GAF gene→GO→PMID index
└── schemas/
    ├── go_enrichment_input.schema.json
    ├── go_enrichment_output.schema.json
    └── enrichment_explanation.schema.json
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

## Documentation

- **[`ROADMAP.md`](ROADMAP.md)**: Development roadmap, architecture, and Ring 1+ plans
- **[`GOATOOLS_FINDINGS.md`](GOATOOLS_FINDINGS.md)**: GOATOOLS API behavior and constraints
- **[`CLAUDE.md`](CLAUDE.md)**: Development philosophy and Ring-based approach

## License

MIT License - see `LICENSE` for details.
