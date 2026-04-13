# GOA Semantic Tools

[![Tests](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml)
[![coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Cellular-Semantics/goa_semantic_tools/main/.github/badges/coverage.json)](https://github.com/Cellular-Semantics/goa_semantic_tools/actions/workflows/test.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

**Hierarchical GO enrichment analysis with IC-based theme grouping, provenance-labeled LLM explanations, and literature-grounded references**

GO enrichment analysis typically produces hundreds of statistically significant terms with heavy redundancy from parent-child overlaps. GOA Semantic Tools reduces these to a structured set of biological themes using MRCEA-B, a bottom-up information-content algorithm, then generates provenance-labeled explanations grounded in curated GAF citations and full-text evidence from ASTA (Semantic Scholar) and Europe PMC.

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
# Full pipeline: enrichment → literature → per-gene narratives → LLM explanation
# Requires OPENAI_API_KEY or ANTHROPIC_API_KEY
uv run go-enrichment --genes-file genes.txt -o results/my_analysis

# Enrichment only (no API keys needed)
uv run go-enrichment --genes-file genes.txt -o results/my_analysis --stop-after enrichment

# Stop after literature fetch (no LLM call)
uv run go-enrichment --genes-file genes.txt -o results/my_analysis --stop-after literature

# Enable external literature search (Europe PMC for hub genes, unscoped ASTA widening)
uv run go-enrichment --genes-file genes.txt -o results/my_analysis --literature-search

# Resume from enrichment JSON (runs Phase 1b + 1c + 2)
uv run go-enrichment --enrichment-json results/my_analysis_enrichment.json -o results/my_analysis

# Resume from literature JSON (runs Phase 1c + 2 only)
uv run go-enrichment --literature-json results/my_analysis_literature.json -o results/my_analysis

# Preview what would run without executing
uv run go-enrichment --genes-file genes.txt -o results/my_analysis --dry-run

# Comma-separated genes directly
uv run go-enrichment --genes TP53,BRCA1,BRCA2,PTEN,RB1,APC -o results/my_analysis
```

### Batch Mode

Process multiple gene lists from a CSV file in a single run — useful for analysing all clusters from a single-cell study or a suite of differential expression comparisons.

```bash
# Run all gene lists in a project CSV
uv run go-enrichment --project input_data/my_project/project.csv

# Enrichment only for every gene list (no API keys needed)
uv run go-enrichment --project input_data/my_project/project.csv --stop-after enrichment

# Preview batch plan without executing
uv run go-enrichment --project input_data/my_project/project.csv --dry-run
```

The project CSV requires `name` and `genes` columns; `species` and `description` are optional per-row overrides:

```csv
name,genes,species,description
C1_RTK_Rho,"EGFR,FGFR3,RHOA,CDC42,RAC1",human,RTK and Rho signalling cluster
C2_immune,"LYN,PTPRC,CD247,CD3D",human,Immune response cluster
C3_metabolic,"ACSL1,IRS2,PDK4,LEP",mouse,Metabolic cluster
```

Results are saved under `results/{project_name}/{name}/{datestamp}/` and a `batch_run.json` manifest is appended after each run.

Output files are auto-named from the base path:
- `*_enrichment.json` - Structured enrichment results (themes, leaves, hub genes)
- `*_literature.json` - Pre-fetched literature evidence (GAF PMIDs, snippets, abstracts)
- `*_explanation.md` - Provenance-labeled biological summary with inline citations; includes a clickable theme index at the top
- `*_themes.csv` - Full theme table with all genes (semicolon-separated), fold enrichment, namespace, FDR, confidence
- `*_gaf_pmids.json` - Curated GAF citation index (for interactive use)

### CLI Options

**Input** (mutually exclusive, one required):

| Option | Description |
|--------|-------------|
| `--genes` | Comma-separated gene symbols |
| `--genes-file` | File with gene symbols (one per line, `#` for comments) |
| `--enrichment-json` | Resume from enrichment JSON (skips Phase 1) |
| `--literature-json` | Resume from literature JSON (skips Phase 1 + 1b) |
| `--project CSV` | Batch mode: process all gene lists in project CSV (see [Batch Mode](#batch-mode)) |

**Pipeline control:**

| Option | Default | Description |
|--------|---------|-------------|
| `-o`, `--output` | *(required)* | Output base path (extensions added automatically) |
| `--stop-after` | *(run all)* | `enrichment` or `literature` — stop after specified phase |
| `--literature-search` | off | Enable external literature search (Europe PMC hub gene abstracts, unscoped ASTA widening). Results are non-deterministic. |
| `--dry-run` | off | Preview analysis plan without executing |

**Enrichment parameters:**

| Option | Default | Description |
|--------|---------|-------------|
| `--species` | `human` | `human` or `mouse` |
| `--fdr` | `0.05` | FDR significance threshold |
| `--min-ic` | `3.0` | Minimum information content for anchor terms |
| `--min-leaves` | `2` | Min enriched leaves to qualify as anchor |
| `--max-genes` | `30` | Filter overly general terms |
| `--namespace` | all | GO namespace(s): `BP`, `MF`, `CC` |

**LLM parameters:**

| Option | Default | Description |
|--------|---------|-------------|
| `--model` | `gpt-4o` | LLM model (`gpt-4o`, `gpt-4o-mini`, `gpt-5`, `claude-sonnet-4-20250514`) |
| `--max-tokens` | model default | Override LLM output token limit (gpt-5: 32000, others: 16000) |

### Environment Variables

| Variable | Required for | Description |
|----------|-------------|-------------|
| `OPENAI_API_KEY` | OpenAI models | API key for gpt-4o, gpt-4o-mini, gpt-5 |
| `ANTHROPIC_API_KEY` | Anthropic models | API key for Claude models |
| `ASTA_API_KEY` | ASTA snippets | Semantic Scholar API key for full-text snippet search (optional but recommended) |

## How It Works

### 1. GO Enrichment (Phase 1)

Runs over-representation analysis (ORA) via GOATOOLS with Fisher's exact test and BH-corrected FDR. Downloads and caches GO ontology and GAF annotations automatically.

### 2. Leaf-First Theme Building via MRCEA-B (Phase 1)

Instead of selecting top-N most significant terms (which creates redundancy), the algorithm works bottom-up using **MRCEA-B** (Most Recent Common Enriched Ancestor, all-paths BFS):

1. **Enrichment leaves**: Find the most specific enriched terms (no enriched descendants in the enriched set)
2. **IC computation**: Calculate Resnik information content for all enriched terms from GAF annotations (higher IC = more specific)
3. **All-paths BFS**: For each leaf, traverse upward through all enriched parents simultaneously (using is_a + part_of edges from leaves; regulates edges at higher levels)
4. **Greedy anchor selection**: Iteratively pick the ancestor that maximises IC × number of uncovered leaves; leaves sharing no qualifying ancestor become standalone themes
5. **Hub gene identification**: Flag genes appearing in 3+ themes as biological coordinators

Typical reduction: 50–75% fewer terms while preserving the biological signal. On coherent gene communities (e.g. RTK/Rho signalling), MRCEA-B achieves ~1.8× compression vs the prior depth-anchor approach.

### 3. Literature Pre-fetch (Phase 1b)

All evidence is gathered **before** the LLM call (lit-first approach):

1. **GAF citation lookup** (no API): For each theme, find curated PMIDs from the GO Annotation File — the original experimental papers establishing each gene→GO term relationship. Also builds a cross-theme index for genes annotated across multiple themes.
2. **ASTA snippet search** (Semantic Scholar, requires `ASTA_API_KEY`): Full-text snippet search scoped to GAF PMIDs, within-theme co-annotations, and cross-theme co-annotations. Provides body-text evidence passages rather than just abstracts.
3. **GAF abstract fetch** (Europe PMC): Retrieve title + abstract for each GAF PMID.
4. **Hub gene + cross-theme PMID snippets** (with `--literature-search`): Unscoped ASTA and Europe PMC searches for hub genes and cross-theme GAF PMIDs.

### 4. Per-Gene Evidence Narratives (Phase 1c)

Each gene gets a focused, cheap LLM call (gpt-4o-mini, ~$0.001/gene) with **only its own evidence** — snippets, GAF annotations, abstracts. The output is a 1-2 sentence mechanistic narrative with inline PMID citations. This solves the problem of the synthesiser ignoring evidence buried in a ~90K character context blob.

Three categories run in parallel:
- **Hub gene narratives**: Gene + cross-theme evidence + snippets
- **Per-theme key gene narratives**: Gene + theme-specific evidence
- **Co-annotation narratives**: Gene + the GO terms it bridges

### 5. LLM Explanation (Phase 2)

The synthesiser LLM receives pre-digested gene narratives instead of raw snippet dumps, enabling it to incorporate evidence it would otherwise overlook. It generates a structured JSON explanation that is programmatically rendered to markdown.

Provenance tags distinguish claim sources:

| Tag | Meaning |
|-----|---------|
| **[DATA]** | Direct observations from enrichment (FDR values, gene counts, co-occurrence) |
| **[INFERENCE]** | Logical deductions from co-annotation patterns (verified against literature where possible) |
| **[EXTERNAL]** | Claims cited from pre-fetched paper abstracts or snippets |
| **[GO-HIERARCHY]** | Facts derived from GO parent-child structure |

Statements tagged [INFERENCE] without PMID citations are flagged with a disclaimer in the output as hypotheses requiring validation.

## Python API

```python
from goa_semantic_tools.services import run_go_enrichment, generate_markdown_explanation

# Phase 1: Enrichment + theme building (MRCEA-B)
result = run_go_enrichment(
    gene_symbols=["TP53", "BRCA1", "BRCA2", "PTEN", "RB1", "APC"],
    species="human",
    fdr_threshold=0.05,
    min_ic=3.0,      # minimum Resnik IC for anchor terms
    min_leaves=2,    # min enriched leaves to form a group
    max_genes=30,
)

# Access structured results
print(f"Enrichment leaves: {len(result['enrichment_leaves'])}")
print(f"Themes: {len(result['themes'])}")
print(f"Hub genes: {list(result['hub_genes'].keys())}")

# Phase 2: LLM explanation (requires API key in environment)
# Use the CLI (--explain --add-references) for the full lit-first pipeline.
# For programmatic use without literature pre-fetch:
markdown = generate_markdown_explanation(
    enrichment_output=result,
    model="gpt-4o",
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
│   ├── go_markdown_explanation_service.py    # LLM explanation + markdown render
│   ├── go_explanation.prompt.yaml            # Synthesiser prompt template
│   ├── evidence_narrative_service.py         # Per-gene subagent narratives (Phase 1c)
│   ├── evidence_narrative.prompt.yaml        # Subagent prompt template
│   ├── asta_literature_service.py            # ASTA (Semantic Scholar) snippet search
│   ├── artl_literature_service.py            # Europe PMC abstract pre-fetch
│   ├── reference_retrieval_service.py        # GAF PMID lookup + claim extraction
│   └── reference_retrieval.prompt.yaml       # Assertion extraction prompt
├── utils/
│   ├── data_downloader.py                    # Download & cache GO/GAF data
│   ├── go_data_loader.py                     # Load data with GOATOOLS
│   ├── go_hierarchy.py                       # Leaf-first + MRCEA-B IC-based grouping
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
