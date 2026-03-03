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
from .services.reference_retrieval_service import (
    AtomicAssertion,
    extract_claims,
    extract_genes_from_text,
    find_references_for_assertion,
    format_references_needing_artl_mcp,
    inject_references_inline,
)
from .utils.reference_index import get_descendants_closure, load_gaf_with_pmids


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
    print(f"Depth range: {args.depth_min}-{args.depth_max}")
    print(f"Min children: {args.min_children}")
    print(f"Max genes: {args.max_genes}")
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
    print("5. Compute enrichment leaves (most specific terms)")
    print(f"   - Filter terms with >{args.max_genes} genes")
    print("6. Build hierarchical themes using depth-anchors algorithm")
    print(f"   - Anchor candidates: GO depth {args.depth_min}-{args.depth_max}")
    print(f"   - Require ≥{args.min_children} enriched descendants")
    print("7. Identify hub genes (appearing in 3+ themes)")

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

    # Phase 1b plan (if references + explain requested)
    if args.add_references and args.explain and not args.no_literature_search:
        print("\n" + "=" * 80)
        print("## PHASE 1b: LITERATURE PRE-FETCH (lit-first)")
        print("=" * 80)
        print("\nSteps that would be executed:")
        print("1. Open artl-mcp (Europe PMC) session")
        print("2. For each theme: query top-ranked genes + anchor GO term name")
        print("3. Fetch paper abstracts (up to 10 per theme)")
        print("4. Inject abstracts into theme context for Phase 2 LLM call")
        print("\nThe LLM will cite papers inline (PMID:xxxxx) rather than from")
        print("latent knowledge, eliminating unresolved assertions.")

    print("\n" + "=" * 80)
    print("DRY RUN COMPLETE - No analysis was executed")
    print("=" * 80)


def _add_references_to_explanation(
    explanation_markdown: str,
    enrichment_output: dict,
    species: str = "human",
    output_path: Path | None = None,
    no_literature_search: bool = False,
) -> str:
    """
    Add literature references to explanation markdown.

    Uses a two-tier approach:
    1. Programmatic lookup via GO annotations (GAF)
    2. Export unresolved assertions for artl-mcp processing

    Args:
        explanation_markdown: Generated explanation markdown
        enrichment_output: Enrichment results (for extracting GO terms and genes)
        species: Species for GAF lookup
        output_path: Optional base path for exporting artl-mcp queries

    Returns:
        Explanation markdown with appended references section
    """
    from .utils.data_downloader import ensure_gaf_data, ensure_go_data
    from .utils.go_data_loader import load_go_data

    print("\n[1/5] Loading reference data...")

    # Load GO and GAF data
    go_obo_path = ensure_go_data()
    gaf_path = ensure_gaf_data(species=species)
    godag = load_go_data(go_obo_path)

    # Build mappings from enrichment data
    all_genes: set[str] = set()
    all_go_ids: set[str] = set()
    go_name_to_id: dict[str, str] = {}  # Map GO term names to IDs
    go_id_to_genes: dict[str, set[str]] = {}  # Map GO ID to genes

    # From enrichment leaves
    for leaf in enrichment_output.get("enrichment_leaves", []):
        genes = leaf.get("genes", [])
        go_id = leaf.get("go_id", "")
        go_name = leaf.get("name", "")
        all_genes.update(genes)
        if go_id:
            all_go_ids.add(go_id)
            go_name_to_id[go_name.lower()] = go_id
            go_id_to_genes[go_id] = set(genes)

    # From themes
    for theme in enrichment_output.get("themes", []):
        anchor = theme.get("anchor_term", {})
        genes = anchor.get("genes", [])
        go_id = anchor.get("go_id", "")
        go_name = anchor.get("name", "")
        all_genes.update(genes)
        if go_id:
            all_go_ids.add(go_id)
            go_name_to_id[go_name.lower()] = go_id
            go_id_to_genes[go_id] = set(genes)

        for specific in theme.get("specific_terms", []):
            genes = specific.get("genes", [])
            go_id = specific.get("go_id", "")
            go_name = specific.get("name", "")
            all_genes.update(genes)
            if go_id:
                all_go_ids.add(go_id)
                go_name_to_id[go_name.lower()] = go_id
                go_id_to_genes[go_id] = set(genes)

    print(f"  Found {len(all_genes)} genes, {len(all_go_ids)} GO terms")

    print("\n[2/5] Building reference index from GAF...")
    ref_index = load_gaf_with_pmids(gaf_path, godag, genes_of_interest=all_genes)
    print(f"  Indexed {len(ref_index.get('pmid_gene_gos', {}))} unique PMIDs")

    print("\n[3/5] Computing GO term descendants...")
    descendants_closure = get_descendants_closure(all_go_ids, godag)

    print("\n[4/5] Extracting claims and mapping to GO terms...")
    claims = extract_claims(explanation_markdown)

    inference_claims = claims.get("INFERENCE", [])
    external_claims = claims.get("EXTERNAL", [])

    print(f"  Found {len(inference_claims)} [INFERENCE] claims")
    print(f"  Found {len(external_claims)} [EXTERNAL] claims")

    # Build assertions with smart GO term mapping
    assertion_refs: list[tuple[AtomicAssertion, list]] = []
    needs_artl_mcp: list[AtomicAssertion] = []

    def _map_claim_to_go_ids(claim_text: str) -> list[str]:
        """Map claim text to relevant GO term IDs based on term name matches."""
        claim_lower = claim_text.lower()
        matched_ids = []

        # Check if any GO term names appear in the claim
        for name, go_id in go_name_to_id.items():
            # Match if GO term name (or significant portion) appears in claim
            if len(name) > 10 and name in claim_lower:
                matched_ids.append(go_id)
            elif any(word in claim_lower for word in name.split() if len(word) > 5):
                matched_ids.append(go_id)

        return matched_ids[:3] if matched_ids else []  # Limit to 3

    for claim_type, claim_list in [("INFERENCE", inference_claims), ("EXTERNAL", external_claims)]:
        for claim_text in claim_list:
            # Extract genes from claim text
            genes = extract_genes_from_text(claim_text, known_genes=all_genes)

            if not genes:
                continue

            # Map claim to specific GO terms (not all GO terms!)
            go_ids = _map_claim_to_go_ids(claim_text)

            # Determine complexity based on actual matches, not all terms
            is_multi_gene = len(genes) > 1
            is_multi_process = len(go_ids) > 1

            assertion = AtomicAssertion(
                claim_type=claim_type,
                original_text=claim_text,
                genes=genes[:5],  # Limit to 5 genes
                go_term_ids=go_ids if go_ids else list(all_go_ids)[:1],  # Fallback to first GO term
                is_multi_gene=is_multi_gene,
                is_multi_process=is_multi_process,
            )

            refs = find_references_for_assertion(
                assertion, ref_index, descendants_closure, max_refs=3
            )

            if refs:
                assertion_refs.append((assertion, refs))
            else:
                needs_artl_mcp.append(assertion)

    print(f"\n  References found for {len(assertion_refs)} assertions")
    print(f"  Assertions needing artl-mcp: {len(needs_artl_mcp)}")

    # Resolve via artl-mcp literature search (unless opted out)
    if needs_artl_mcp and not no_literature_search:
        print(f"\n[4b/5] Resolving {len(needs_artl_mcp)} assertions via artl-mcp...")
        try:
            from .services.artl_literature_service import resolve_assertions_via_literature

            literature_results = resolve_assertions_via_literature(
                needs_artl_mcp,
                max_refs_per_assertion=3,
            )

            # Move resolved assertions to assertion_refs, keep unresolved
            still_unresolved = []
            for assertion, refs in literature_results:
                if refs:
                    assertion_refs.append((assertion, refs))
                else:
                    still_unresolved.append(assertion)

            resolved_count = len(needs_artl_mcp) - len(still_unresolved)
            print(f"  ✓ Resolved {resolved_count}/{len(needs_artl_mcp)} via literature search")
            needs_artl_mcp = still_unresolved

        except Exception as e:
            print(f"  ⚠ Literature search failed: {e}")
            print("  Continuing with GAF-only references...")

    print("\n[5/5] Injecting references and exporting unresolved...")

    # Inject references into markdown
    if assertion_refs:
        explanation_markdown = inject_references_inline(explanation_markdown, assertion_refs)
        print(f"  ✓ Injected {len(assertion_refs)} reference blocks")

    # Export unresolved assertions for artl-mcp
    if needs_artl_mcp and output_path:
        artl_queries = format_references_needing_artl_mcp(needs_artl_mcp)
        artl_path = output_path.parent / f"{output_path.name}_artl_queries.json"
        with open(artl_path, "w") as f:
            json.dump(artl_queries, f, indent=2)
        print(f"  ✓ Exported {len(needs_artl_mcp)} queries to: {artl_path.name}")

        # Add note to markdown about unresolved assertions
        if needs_artl_mcp:
            search_note = (
                "via GO annotations or automated literature search"
                if not no_literature_search
                else "via GO annotations (literature search was skipped; rerun without --no-literature-search)"
            )
            lines = [
                explanation_markdown,
                "",
                "---",
                "",
                "## Unresolved Assertions",
                "",
                f"The following {len(needs_artl_mcp)} assertions could not be resolved {search_note}.",
                "They have been exported to `_artl_queries.json` for manual review:",
                "",
            ]
            for i, assertion in enumerate(needs_artl_mcp[:10], 1):
                genes_str = ", ".join(assertion.genes[:3])
                lines.append(f"{i}. **[{assertion.claim_type}]** ({genes_str})")
                preview = assertion.original_text[:80]
                if len(assertion.original_text) > 80:
                    preview += "..."
                lines.append(f"   {preview}")
                lines.append("")

            if len(needs_artl_mcp) > 10:
                lines.append(f"... and {len(needs_artl_mcp) - 10} more (see `_artl_queries.json`)")

            explanation_markdown = "\n".join(lines)

    return explanation_markdown


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
  %(prog)s --genes TP53,BRCA1 --species mouse --fdr 0.01 --output results/

  # With explanation
  %(prog)s --genes TP53,BRCA1,BRCA2 --output results/ --explain
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
        "--fdr",
        type=float,
        default=0.05,
        help="FDR significance threshold (default: 0.05)",
    )

    # Depth-anchor options
    parser.add_argument(
        "--depth-min",
        type=int,
        default=4,
        help="Min GO depth for anchor terms (default: 4)",
    )
    parser.add_argument(
        "--depth-max",
        type=int,
        default=7,
        help="Max GO depth for anchor terms (default: 7)",
    )
    parser.add_argument(
        "--min-children",
        type=int,
        default=2,
        help="Min enriched children to qualify as anchor (default: 2)",
    )
    parser.add_argument(
        "--max-genes",
        type=int,
        default=30,
        help="Filter terms with > max-genes (default: 30)",
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
        help="LLM model for explanations (default: gpt-4o). Examples: gpt-4o, gpt-4o-mini, gpt-5, claude-sonnet-4-20250514",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Override LLM output token limit (default: model-specific; gpt-5=32000, all others=16000).",
    )

    # Reference options
    parser.add_argument(
        "--add-references",
        action="store_true",
        default=False,
        help="Add literature references to explanation. Uses GO annotations for programmatic lookup, plus artl-mcp literature search for unresolved assertions.",
    )
    parser.add_argument(
        "--no-literature-search",
        action="store_true",
        default=False,
        help="Disable artl-mcp literature search (only use GAF-based lookup). Unresolved assertions are exported to *_artl_queries.json.",
    )

    parser.add_argument(
        "--namespace",
        nargs="+",
        choices=["BP", "MF", "CC"],
        default=None,
        metavar="NS",
        help="GO namespace(s) to include: BP (biological_process), MF (molecular_function), CC (cellular_component). Default: all three. Example: --namespace BP",
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
        print(f"  Depth range: {args.depth_min}-{args.depth_max}")
        print(f"  Min children: {args.min_children}")
        print(f"  Max genes: {args.max_genes}")
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
            fdr_threshold=args.fdr,
            depth_range=(args.depth_min, args.depth_max),
            min_children=args.min_children,
            max_genes=args.max_genes,
            namespaces=args.namespace,
        )
        print("=" * 80)

        # Always save enrichment JSON (Phase 1)
        with open(enrichment_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n✓ Enrichment data saved to: {enrichment_path.absolute()}")

        # Phase 1b: Build reference index + fetch hub gene abstracts
        gaf_pmids = None
        hub_gene_abstracts = None
        if args.explain and args.add_references:
            themes = result.get("themes", [])
            hub_genes_data = result.get("hub_genes", {})

            print("\n" + "=" * 80)
            print("Reference Pre-fetch - Phase 1b")
            print("=" * 80)

            # Always: GAF-curated PMIDs per theme (no API calls, uses cached GAF data)
            if themes:
                try:
                    from .services.reference_retrieval_service import get_gaf_pmids_for_themes
                    from .utils.reference_index import load_gaf_with_pmids
                    from .utils.data_downloader import ensure_gaf_data
                    from .utils.go_data_loader import load_go_data

                    print(f"\nBuilding GAF reference index for {len(themes)} theme(s)...")
                    gaf_path = ensure_gaf_data(species=args.species)
                    from .utils.data_downloader import ensure_go_data
                    go_path = ensure_go_data()
                    godag = load_go_data(go_path)

                    all_genes: set[str] = set()
                    for t in themes:
                        all_genes.update(t.get("anchor_term", {}).get("genes", []))
                        for st in t.get("specific_terms", []):
                            all_genes.update(st.get("genes", []))

                    ref_index = load_gaf_with_pmids(gaf_path, godag, genes_of_interest=all_genes)
                    gaf_pmids = get_gaf_pmids_for_themes(themes, ref_index)
                    themes_with_pmids = sum(1 for v in gaf_pmids.values() if v)
                    total_pmids = sum(len(v) for v in gaf_pmids.values())
                    print(f"✓ Found {total_pmids} GAF PMIDs across {themes_with_pmids}/{len(themes)} themes")

                    # Save GAF PMIDs as sidecar JSON for interactive skill use
                    gaf_pmids_path = base_output.parent / f"{base_output.name}_gaf_pmids.json"
                    # Serialise with string keys (JSON requires string keys)
                    with open(gaf_pmids_path, "w") as f:
                        json.dump({str(k): v for k, v in gaf_pmids.items()}, f, indent=2)
                    print(f"✓ GAF PMIDs saved to: {gaf_pmids_path.name}")
                except Exception as e:
                    print(f"\n⚠ GAF reference index failed: {e}")
                    print("  Continuing without GAF citations...")

            # Optional: Europe PMC search for top hub genes
            if hub_genes_data and not args.no_literature_search:
                n_hub = len(hub_genes_data)
                print(f"\nFetching Europe PMC abstracts for top hub genes (up to 20 of {n_hub})...")
                try:
                    from .services.artl_literature_service import fetch_abstracts_for_hub_genes
                    hub_gene_abstracts = fetch_abstracts_for_hub_genes(
                        hub_genes_data, max_hub_genes=20
                    )
                    genes_with_papers = sum(1 for v in hub_gene_abstracts.values() if v)
                    print(f"✓ Fetched abstracts for {genes_with_papers}/{min(n_hub, 20)} hub genes")
                except Exception as e:
                    print(f"\n⚠ Hub gene abstract fetch failed: {e}")
                    print("  Continuing without hub gene abstracts...")

        # Phase 2: Generate markdown explanation if requested
        if args.explain:
            print("\n" + "=" * 80)
            try:
                explanation_markdown = generate_markdown_explanation(
                    enrichment_output=result,
                    model=args.model,
                    temperature=0.1,
                    max_tokens=args.max_tokens,  # None → auto-derived per model
                    gaf_pmids=gaf_pmids,
                    hub_gene_abstracts=hub_gene_abstracts,
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

        print("\n" + "=" * 80)
        print("Summary")
        print("=" * 80)
        print(f"  Input genes: {metadata['input_genes_count']}")
        print(f"  Found in annotations: {metadata['genes_with_annotations']}")
        print(f"  Total enriched terms: {metadata['total_enriched_terms']}")

        enrichment_leaves = result.get("enrichment_leaves", [])
        themes = result.get("themes", [])
        hub_genes = result.get("hub_genes", {})

        print(f"  Enrichment leaves: {len(enrichment_leaves)}")
        print(f"  Themes created: {metadata.get('themes_count', len(themes))}")
        print(f"  Hub genes: {len(hub_genes)}")

        if enrichment_leaves:
            print(f"\nTop 3 Enrichment Leaves:")
            for i, leaf in enumerate(enrichment_leaves[:3], 1):
                print(f"\n  {i}. {leaf['name']}")
                print(f"     GO ID: {leaf['go_id']} (depth {leaf['depth']})")
                print(f"     FDR: {leaf['fdr']:.2e}")
                print(f"     Genes: {len(leaf['genes'])}")

        if themes:
            print(f"\nTop 3 Themes:")
            for i, theme in enumerate(themes[:3], 1):
                anchor = theme["anchor_term"]
                n_specific = theme.get("n_specific_terms", 0)
                print(f"\n  {i}. [{theme['anchor_confidence']}] {anchor['name']}")
                print(f"     GO ID: {anchor['go_id']} (depth {anchor['depth']})")
                print(f"     FDR: {anchor['fdr']:.2e}")
                print(f"     Genes: {len(anchor['genes'])}")
                if n_specific > 0:
                    print(f"     Specific terms: {n_specific}")

        if hub_genes:
            print(f"\nTop Hub Genes:")
            for gene, data in list(hub_genes.items())[:5]:
                print(f"  - {gene}: {data['theme_count']} themes")

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
