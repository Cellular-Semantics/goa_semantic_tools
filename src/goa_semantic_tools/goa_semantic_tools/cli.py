"""
CLI Runner for GO Enrichment Analysis

Simple command-line interface for running hierarchical GO enrichment.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .services import generate_explanations, run_go_enrichment


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
        help="Output directory for results (will create if doesn't exist)",
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
    parser.add_argument(
        "--name",
        type=str,
        help="Analysis name for output files (default: auto-generated from gene count)",
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

    args = parser.parse_args()

    try:
        # Parse gene list
        print("=" * 80)
        print("GO Enrichment Analysis - CLI Runner")
        print("=" * 80)

        genes = parse_gene_list(args.genes, args.genes_file)
        print(f"\n✓ Parsed {len(genes)} gene symbols")
        if len(genes) <= 20:
            print(f"  Genes: {', '.join(genes)}")
        else:
            print(f"  First 10: {', '.join(genes[:10])}...")
            print(f"  Last 10: {', '.join(genes[-10:])}...")

        # Validate parameters
        if args.fdr <= 0 or args.fdr > 1:
            raise ValueError("FDR threshold must be between 0 and 1")

        if args.top_n < 1:
            raise ValueError("top-n must be >= 1")

        print(f"\n✓ Parameters:")
        print(f"  Species: {args.species}")
        print(f"  Top-N roots: {args.top_n}")
        print(f"  FDR threshold: {args.fdr}")
        if args.explain:
            print(f"  Generate explanations: Yes")
            print(f"  LLM model: {args.model}")
        else:
            print(f"  Generate explanations: No (use --explain to enable)")

        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n✓ Output directory: {output_dir.absolute()}")

        # Run enrichment
        print("\n" + "=" * 80)
        result = run_go_enrichment(
            gene_symbols=genes,
            species=args.species,
            top_n_roots=args.top_n,
            fdr_threshold=args.fdr,
        )
        print("=" * 80)

        # Generate output filename
        if args.name:
            output_name = args.name
        else:
            output_name = f"enrichment_{len(genes)}_genes"

        # Save Phase 1 results
        phase1_file = output_dir / f"{output_name}.json"
        with open(phase1_file, "w") as f:
            json.dump(result, f, indent=2)

        print(f"\n✓ Phase 1 results saved to: {phase1_file.absolute()}")

        # Phase 2: Generate explanations if requested
        final_result = result
        if args.explain:
            print("\n" + "=" * 80)
            try:
                explanation_result = generate_explanations(
                    enrichment_output=result, model=args.model, temperature=0.1, max_tokens=3000
                )

                # Save Phase 2 results
                phase2_file = output_dir / f"{output_name}_with_explanations.json"
                with open(phase2_file, "w") as f:
                    json.dump(explanation_result, f, indent=2)

                print(f"\n✓ Phase 2 results saved to: {phase2_file.absolute()}")
                final_result = explanation_result

            except Exception as e:
                print(f"\n❌ Warning: Explanation generation failed: {e}", file=sys.stderr)
                print(f"   Phase 1 results are still available in {phase1_file.name}")
                # Continue with Phase 1 results only

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
        if args.explain and "explanations" in final_result:
            print(f"✓ Analysis complete! Results saved:")
            print(f"  Phase 1: {phase1_file.name}")
            print(f"  Phase 2: {phase2_file.name}")
        else:
            print(f"✓ Analysis complete! Results saved to {phase1_file.name}")
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
