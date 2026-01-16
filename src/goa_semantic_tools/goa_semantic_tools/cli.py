"""
CLI Runner for GO Enrichment Analysis

Simple command-line interface for running hierarchical GO enrichment.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import yaml

from .services import generate_markdown_explanation, run_go_enrichment


def parse_gene_list(genes_arg: Optional[str], genes_file: Optional[str]) -> list[str]:
    """
    Parse gene list from command-line argument or file.

    Args:
        genes_arg: Comma-separated gene symbols
        genes_file: Path to file with gene symbols (one per line)

    Returns:
        List of gene symbols

    Raises:
        ValueError: If neither or both arguments provided, or file not found
    """
    if genes_arg and genes_file:
        raise ValueError("Provide either --genes or --genes-file, not both")

    if not genes_arg and not genes_file:
        raise ValueError("Must provide either --genes or --genes-file")

    if genes_arg:
        # Parse comma-separated list
        genes = [g.strip().upper() for g in genes_arg.split(",")]
        genes = [g for g in genes if g]  # Remove empty strings
        return genes

    if genes_file:
        # Read from file
        genes_path = Path(genes_file)
        if not genes_path.exists():
            raise ValueError(f"Gene list file not found: {genes_file}")

        with open(genes_path) as f:
            genes = [line.strip().upper() for line in f if line.strip()]

        # Remove comments and empty lines
        genes = [g for g in genes if g and not g.startswith("#")]
        return genes

    raise ValueError("Unreachable: should have gene list by now")


def _print_dry_run(genes: list[str], args: any) -> None:
    """
    Print dry-run information to stdout without executing analysis.

    Shows what would be executed including inputs, prompts, and schemas.
    """
    print("=" * 80)
    print("GO Enrichment Analysis - DRY RUN")
    print("=" * 80)

    # Input configuration
    print("\n## INPUT CONFIGURATION")
    print(f"Gene count: {len(genes)}")
    if len(genes) <= 20:
        print(f"Genes: {', '.join(genes)}")
    else:
        print(f"First 10: {', '.join(genes[:10])}")
        print(f"Last 10: {', '.join(genes[-10:])}")

    # Prepare output paths
    base_output = Path(args.output)
    if base_output.suffix:
        base_output = base_output.with_suffix("")
    enrichment_path = base_output.parent / f"{base_output.name}_enrichment.json"
    explanation_path = base_output.parent / f"{base_output.name}_explanation.md"

    print(f"\nSpecies: {args.species}")
    print(f"Top-N roots per namespace: {args.top_n}")
    print(f"FDR threshold: {args.fdr}")
    print(f"\nOutput files:")
    print(f"  Enrichment: {enrichment_path}")
    if args.explain:
        print(f"  Explanation: {explanation_path}")

    # Phase 1 plan
    print("\n" + "=" * 80)
    print("## PHASE 1: GO ENRICHMENT ANALYSIS")
    print("=" * 80)
    print("\nSteps that would be executed:")
    print("1. Download/cache GO ontology (if needed)")
    print("2. Download/cache GAF gene annotations (if needed)")
    print("3. Load GO DAG and gene annotations")
    print("4. Run GOATOOLS enrichment analysis")
    print("   - Fisher's exact test with FDR correction")
    print("   - Propagate counts up GO hierarchy")
    print(f"   - Filter by FDR < {args.fdr}")
    print(f"5. Cluster enriched terms using top-{args.top_n} roots per namespace")
    print("6. Build hierarchical output with contributing genes")

    print(f"\nOutput: {enrichment_path}")

    # Phase 2 plan (if requested)
    if args.explain:
        print("\n" + "=" * 80)
        print("## PHASE 2: LLM EXPLANATION GENERATION")
        print("=" * 80)
        print(f"\nModel: {args.model}")
        print(f"Output format: Markdown")
        print(f"Temperature: 0.1")
        print(f"Max tokens: 16000")

        # Load and display prompt
        print("\n### Prompt Configuration")
        prompt_path = Path(__file__).parent / "services" / "go_explanation.prompt.yaml"
        try:
            with open(prompt_path) as f:
                prompt_config = yaml.safe_load(f)

            print("\nSystem Prompt:")
            print("-" * 80)
            print(prompt_config["system_prompt"])

            print("\nUser Prompt Template:")
            print("-" * 80)
            print(prompt_config["user_prompt"])

        except FileNotFoundError:
            print("(Prompt file not found)")

        print("\n### Output Format")
        print("Markdown report with:")
        print("  - Per-cluster biological explanations")
        print("  - GO IDs hyperlinked to GO ontology")
        print("  - PMIDs hyperlinked to PubMed")
        print("  - Key genes with evidence and citations")
        print("  - Overall biological summary")

        print(f"\nOutput: {explanation_path}")

    print("\n" + "=" * 80)
    print("DRY RUN COMPLETE - No analysis was executed")
    print("=" * 80)


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run hierarchical GO enrichment analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Comma-separated genes
  %(prog)s --genes TP53,BRCA1,BRCA2 --output results/

  # From file
  %(prog)s --genes-file genes.txt --output results/

  # With custom parameters
  %(prog)s --genes TP53,BRCA1 --species mouse --top-n 10 --fdr 0.01 --output results/
        """,
    )

    # Gene input (mutually exclusive)
    gene_group = parser.add_mutually_exclusive_group(required=True)
    gene_group.add_argument(
        "--genes", type=str, help="Comma-separated gene symbols (e.g., TP53,BRCA1,BRCA2)"
    )
    gene_group.add_argument(
        "--genes-file",
        type=str,
        help="Path to file with gene symbols (one per line, # for comments)",
    )

    # Required output
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=True,
        help="Output base path (e.g., results/my_analysis). Extensions added automatically: _enrichment.json, _explanation.md",
    )

    # Optional parameters
    parser.add_argument(
        "--species",
        type=str,
        default="human",
        choices=["human", "mouse"],
        help="Species for gene annotations (default: human)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="Number of top enriched terms to use as cluster roots per namespace (default: 5)",
    )
    parser.add_argument(
        "--fdr",
        type=float,
        default=0.05,
        help="FDR significance threshold (default: 0.05)",
    )

    # Explanation options
    parser.add_argument(
        "--explain",
        action="store_true",
        default=False,
        help="Generate LLM explanations (Phase 2). Requires API key (OPENAI_API_KEY or ANTHROPIC_API_KEY)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="LLM model for explanations (default: gpt-4o). Examples: gpt-4o, gpt-4o-mini, claude-sonnet-4-20250514",
    )

    # Utility options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print analysis plan without executing. Shows inputs, prompts, and schemas.",
    )

    args = parser.parse_args()

    try:
        # Parse gene list
        genes = parse_gene_list(args.genes, args.genes_file)

        # Validate parameters
        if args.fdr <= 0 or args.fdr > 1:
            raise ValueError("FDR threshold must be between 0 and 1")

        if args.top_n < 1:
            raise ValueError("top-n must be >= 1")

        # Handle dry-run mode
        if args.dry_run:
            _print_dry_run(genes, args)
            return 0

        # Normal execution mode
        print("=" * 80)
        print("GO Enrichment Analysis - CLI Runner")
        print("=" * 80)

        print(f"\n✓ Parsed {len(genes)} gene symbols")
        if len(genes) <= 20:
            print(f"  Genes: {', '.join(genes)}")
        else:
            print(f"  First 10: {', '.join(genes[:10])}...")
            print(f"  Last 10: {', '.join(genes[-10:])}...")

        print(f"\n✓ Parameters:")
        print(f"  Species: {args.species}")
        print(f"  Top-N roots: {args.top_n}")
        print(f"  FDR threshold: {args.fdr}")
        if args.explain:
            print(f"  Generate explanations: Yes")
            print(f"  LLM model: {args.model}")
        else:
            print(f"  Generate explanations: No (use --explain to enable)")

        # Prepare output paths with auto-added extensions
        base_output = Path(args.output)
        # Remove any existing extension from base
        if base_output.suffix:
            base_output = base_output.with_suffix("")

        # Create output directory
        base_output.parent.mkdir(parents=True, exist_ok=True)

        # Build output file paths
        enrichment_path = base_output.parent / f"{base_output.name}_enrichment.json"
        explanation_path = base_output.parent / f"{base_output.name}_explanation.md"

        print(f"\n✓ Output files:")
        print(f"  Enrichment: {enrichment_path.absolute()}")
        if args.explain:
            print(f"  Explanation: {explanation_path.absolute()}")

        # Run enrichment (Phase 1)
        print("\n" + "=" * 80)
        result = run_go_enrichment(
            gene_symbols=genes,
            species=args.species,
            top_n_roots=args.top_n,
            fdr_threshold=args.fdr,
        )
        print("=" * 80)

        # Always save enrichment JSON (Phase 1)
        with open(enrichment_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n✓ Enrichment data saved to: {enrichment_path.absolute()}")

        # Phase 2: Generate markdown explanation if requested
        if args.explain:
            print("\n" + "=" * 80)
            try:
                explanation_markdown = generate_markdown_explanation(
                    enrichment_output=result, model=args.model, temperature=0.1, max_tokens=16000
                )

                # Save markdown output
                with open(explanation_path, "w") as f:
                    f.write(explanation_markdown)

                print(f"\n✓ Explanation saved to: {explanation_path.absolute()}")

            except Exception as e:
                print(f"\n❌ Error: Explanation generation failed: {e}", file=sys.stderr)
                import traceback

                traceback.print_exc()
                return 1

        print("=" * 80)

        # Print summary
        metadata = result["metadata"]
        clusters = result["clusters"]

        print("\n" + "=" * 80)
        print("Summary")
        print("=" * 80)
        print(f"  Input genes: {metadata['input_genes_count']}")
        print(f"  Found in annotations: {metadata['genes_with_annotations']}")
        print(f"  Total enriched terms: {metadata['total_enriched_terms']}")
        print(f"  Clusters created: {metadata['clusters_count']}")

        if clusters:
            print(f"\nTop 3 Clusters:")
            for i, cluster in enumerate(clusters[:3], 1):
                root = cluster["root_term"]
                print(f"\n  {i}. {root['name']}")
                print(f"     Namespace: {root['namespace']}")
                print(f"     FDR: {root['fdr']:.2e}")
                print(f"     Fold enrichment: {root['fold_enrichment']:.2f}x")
                print(
                    f"     Study genes: {root['study_count']} / {metadata['input_genes_count']}"
                )
                print(f"     Member terms: {len(cluster['member_terms'])}")

        print("\n" + "=" * 80)
        print(f"✓ Analysis complete!")
        print(f"  Enrichment: {enrichment_path.name}")
        if args.explain:
            print(f"  Explanation: {explanation_path.name}")
        print("=" * 80)

        return 0

    except ValueError as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError as e:
        print(f"\n❌ File not found: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
