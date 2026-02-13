#!/usr/bin/env python3
"""
Benchmark leaf-first clustering across MSigDB hallmark test sets.

Tests:
- Positive controls: Hallmark gene sets (should show expected biology)
- Negative controls: Random gene sets (should show minimal/no enrichment)

Metrics:
- Number of enriched terms (raw ORA)
- Number of themes (after leaf-first)
- Reduction ratio
- Whether expected biology is captured (for positive controls)
"""

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from goatools.obo_parser import GODag

# Import from our prototype (using importlib to handle numeric prefix)
import importlib.util
spec = importlib.util.spec_from_file_location(
    "leaf_first",
    Path(__file__).parent / "05_leaf_first_clustering.py"
)
leaf_first = importlib.util.module_from_spec(spec)
spec.loader.exec_module(leaf_first)

load_enriched_terms = leaf_first.load_enriched_terms
build_biological_themes = leaf_first.build_biological_themes
themes_to_dict = leaf_first.themes_to_dict


@dataclass
class BenchmarkResult:
    """Results from benchmarking a single gene set."""
    name: str
    n_input_genes: int
    n_mapped_genes: int
    n_enriched_terms_bp: int
    n_themes: int
    n_high_confidence: int
    n_moderate_confidence: int
    top_themes: list[str]
    reduction_pct: float


def run_enrichment(gene_file: Path, output_dir: Path, fdr: float = 0.05) -> Path:
    """Run GO enrichment via CLI and return output path."""
    # CLI adds _enrichment.json automatically
    output_base = output_dir / gene_file.stem
    output_file = output_dir / f"{gene_file.stem}_enrichment.json"

    cmd = [
        "uv", "run", "go-enrichment",
        "--genes-file", str(gene_file),
        "--fdr", str(fdr),
        "--output", str(output_base),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)

    if result.returncode != 0:
        print(f"  Warning: Enrichment failed for {gene_file.name}")
        print(f"  stderr: {result.stderr[:500]}")
        return None

    return output_file


def benchmark_gene_set(
    gene_file: Path,
    godag: GODag,
    output_dir: Path,
    fdr: float = 0.05
) -> BenchmarkResult | None:
    """Run full benchmark on a single gene set."""

    print(f"\nProcessing: {gene_file.name}")

    # Count input genes
    with open(gene_file) as f:
        input_genes = [line.strip() for line in f if line.strip()]
    n_input = len(input_genes)
    print(f"  Input genes: {n_input}")

    # Run enrichment
    enrichment_file = run_enrichment(gene_file, output_dir, fdr)
    if not enrichment_file or not enrichment_file.exists():
        return None

    # Load results
    with open(enrichment_file) as f:
        enrichment_data = json.load(f)

    n_mapped = enrichment_data["metadata"].get("genes_with_annotations",
                                                enrichment_data["metadata"].get("mapped_genes_count", n_input))
    print(f"  Mapped genes: {n_mapped}")

    # Extract BP terms
    bp_terms = load_enriched_terms(enrichment_data, namespace="biological_process")
    n_bp_terms = len(bp_terms)
    print(f"  Enriched BP terms: {n_bp_terms}")

    if n_bp_terms == 0:
        return BenchmarkResult(
            name=gene_file.stem,
            n_input_genes=n_input,
            n_mapped_genes=n_mapped,
            n_enriched_terms_bp=0,
            n_themes=0,
            n_high_confidence=0,
            n_moderate_confidence=0,
            top_themes=[],
            reduction_pct=0.0
        )

    # Build themes
    themes = build_biological_themes(
        bp_terms,
        godag,
        fdr_high_confidence=0.05,
        min_gene_addition_pct=0.20,
        max_gene_addition_pct=2.0,
        max_genes_for_specific=50
    )

    n_themes = len(themes)
    n_high = sum(1 for t in themes if t.confidence == "high")
    n_moderate = sum(1 for t in themes if t.confidence == "moderate")

    reduction = ((n_bp_terms - n_themes) / n_bp_terms * 100) if n_bp_terms > 0 else 0

    top_theme_names = [t.primary_term.name for t in themes[:5]]

    print(f"  Themes: {n_themes} (high: {n_high}, moderate: {n_moderate})")
    print(f"  Reduction: {reduction:.1f}%")

    # Save themes
    theme_file = output_dir / f"{gene_file.stem}_themes.json"
    with open(theme_file, "w") as f:
        json.dump({
            "metadata": {
                "input_file": str(gene_file),
                "n_input_genes": n_input,
                "n_mapped_genes": n_mapped,
                "n_enriched_bp_terms": n_bp_terms,
                "n_themes": n_themes,
                "fdr_threshold": fdr
            },
            "themes": themes_to_dict(themes)
        }, f, indent=2)

    return BenchmarkResult(
        name=gene_file.stem,
        n_input_genes=n_input,
        n_mapped_genes=n_mapped,
        n_enriched_terms_bp=n_bp_terms,
        n_themes=n_themes,
        n_high_confidence=n_high,
        n_moderate_confidence=n_moderate,
        top_themes=top_theme_names,
        reduction_pct=reduction
    )


def print_summary(results: list[BenchmarkResult], title: str):
    """Print summary table."""
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print(f"{'=' * 80}")

    print(f"\n{'Gene Set':<45} {'Genes':>6} {'BP Terms':>9} {'Themes':>7} {'Reduc%':>7}")
    print("-" * 80)

    for r in results:
        print(f"{r.name:<45} {r.n_mapped_genes:>6} {r.n_enriched_terms_bp:>9} {r.n_themes:>7} {r.reduction_pct:>6.1f}%")

    print("-" * 80)

    # Averages
    if results:
        avg_terms = sum(r.n_enriched_terms_bp for r in results) / len(results)
        avg_themes = sum(r.n_themes for r in results) / len(results)
        avg_reduction = sum(r.reduction_pct for r in results) / len(results)
        print(f"{'AVERAGE':<45} {'-':>6} {avg_terms:>9.1f} {avg_themes:>7.1f} {avg_reduction:>6.1f}%")


def main():
    # Setup
    project_root = Path(__file__).parent.parent
    test_dir = project_root / "input_data" / "benchmark_sets" / "test_lists"
    output_dir = project_root / "results" / "benchmark"
    output_dir.mkdir(exist_ok=True)

    # Load GO DAG
    print("Loading GO ontology...")
    godag = GODag(
        str(project_root / "reference_data" / "go-basic.obo"),
        optional_attrs={"relationship"},
        prt=None
    )

    # Define test sets
    positive_controls = sorted(test_dir.glob("hallmark_*.txt"))
    negative_controls = sorted(test_dir.glob("random_*.txt"))

    print(f"\nFound {len(positive_controls)} positive controls")
    print(f"Found {len(negative_controls)} negative controls")

    # Run benchmarks
    positive_results = []
    for gene_file in positive_controls:
        result = benchmark_gene_set(gene_file, godag, output_dir, fdr=0.05)
        if result:
            positive_results.append(result)

    negative_results = []
    for gene_file in negative_controls:
        result = benchmark_gene_set(gene_file, godag, output_dir, fdr=0.05)
        if result:
            negative_results.append(result)

    # Print summaries
    print_summary(positive_results, "POSITIVE CONTROLS (Hallmark Gene Sets)")
    print_summary(negative_results, "NEGATIVE CONTROLS (Random Gene Sets)")

    # Print top themes for positive controls
    print(f"\n{'=' * 80}")
    print("TOP THEMES BY GENE SET (Do they match expected biology?)")
    print(f"{'=' * 80}")

    for r in positive_results:
        print(f"\n{r.name}:")
        for i, theme in enumerate(r.top_themes[:3], 1):
            print(f"  {i}. {theme}")

    # Save full results
    summary_file = output_dir / "benchmark_summary.json"
    with open(summary_file, "w") as f:
        json.dump({
            "positive_controls": [
                {
                    "name": r.name,
                    "n_input_genes": r.n_input_genes,
                    "n_mapped_genes": r.n_mapped_genes,
                    "n_enriched_terms_bp": r.n_enriched_terms_bp,
                    "n_themes": r.n_themes,
                    "n_high_confidence": r.n_high_confidence,
                    "n_moderate_confidence": r.n_moderate_confidence,
                    "reduction_pct": r.reduction_pct,
                    "top_themes": r.top_themes
                }
                for r in positive_results
            ],
            "negative_controls": [
                {
                    "name": r.name,
                    "n_input_genes": r.n_input_genes,
                    "n_mapped_genes": r.n_mapped_genes,
                    "n_enriched_terms_bp": r.n_enriched_terms_bp,
                    "n_themes": r.n_themes,
                    "reduction_pct": r.reduction_pct,
                    "top_themes": r.top_themes
                }
                for r in negative_results
            ]
        }, f, indent=2)

    print(f"\n\nResults saved to: {output_dir}")


if __name__ == "__main__":
    main()
