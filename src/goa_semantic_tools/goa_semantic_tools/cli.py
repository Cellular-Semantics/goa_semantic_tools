"""
CLI Runner for GO Enrichment Analysis

Simple command-line interface for running hierarchical GO enrichment.

Pipeline phases:
  Phase 1:  genes → enrichment             → _enrichment.json
  Phase 1b: enrichment → literature        → _literature.json
  Phase 2:  enrichment + literature → LLM  → _explanation.md

By default the full pipeline runs. Use --stop-after to exit early,
or --enrichment-json / --literature-json to resume from intermediates.
"""
import argparse
import copy
import csv as _csv
import json
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml

from .services import generate_markdown_explanation, run_go_enrichment
from .services.go_markdown_explanation_service import write_themes_csv


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


def _load_and_validate_json(path: Path, required_key: str, label: str) -> dict:
    """Load a JSON file and validate it contains the required key."""
    if not path.exists():
        raise ValueError(f"{label} file not found: {path}")
    with open(path) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{label} must be a JSON object, got {type(data).__name__}")
    if required_key not in data:
        raise ValueError(f"{label} missing required key '{required_key}'")
    return data


def _determine_input_mode(args: argparse.Namespace) -> str:
    """Determine which pipeline phase to start from based on input args.

    Returns one of: 'genes', 'enrichment', 'literature'
    """
    if args.literature_json:
        return "literature"
    if args.enrichment_json:
        return "enrichment"
    return "genes"


def _warn_ignored_params(args: argparse.Namespace, input_mode: str) -> None:
    """Warn about enrichment params that are ignored when resuming."""
    if input_mode == "genes":
        return
    enrichment_params = {
        "species": "human",
        "fdr": 0.05,
        "min_ic": 3.0,
        "min_leaves": 2,
        "max_genes": 30,
        "namespace": None,
    }
    changed = []
    for param, default in enrichment_params.items():
        if getattr(args, param, default) != default:
            changed.append(f"--{param.replace('_', '-')}")
    if changed:
        warnings.warn(
            f"Enrichment parameters {', '.join(changed)} are ignored when resuming from "
            f"{'enrichment' if input_mode == 'enrichment' else 'literature'} JSON.",
            stacklevel=2,
        )


def _save_literature_json(
    base_output: Path,
    enrichment_source: str,
    gaf_pmids: dict | None,
    gaf_abstracts: dict | None,
    hub_gene_abstracts: dict | None,
    snippet_evidence: dict | None,
    hub_gene_snippets: dict | None,
    co_annotation_snippets: dict | None = None,
    cross_theme_snippets: dict | None = None,
    cross_theme_gaf_snippets: dict | None = None,
) -> Path:
    """Save all Phase 1b literature evidence as a single sidecar JSON."""
    literature_data: dict[str, Any] = {
        "enrichment_source": str(enrichment_source),
        "gaf_pmids": {str(k): v for k, v in (gaf_pmids or {}).items()},
        "gaf_abstracts": {str(k): v for k, v in (gaf_abstracts or {}).items()},
        "hub_gene_abstracts": hub_gene_abstracts or {},
        "snippet_evidence": {str(k): v for k, v in (snippet_evidence or {}).items()},
        "hub_gene_snippets": hub_gene_snippets or {},
        "co_annotation_snippets": {str(k): v for k, v in (co_annotation_snippets or {}).items()},
        "cross_theme_snippets": cross_theme_snippets or {},
        "cross_theme_gaf_snippets": cross_theme_gaf_snippets or {},
    }
    lit_path = base_output.parent / f"{base_output.name}_literature.json"
    with open(lit_path, "w") as f:
        json.dump(literature_data, f, indent=2)
    return lit_path


def _load_literature_json(path: Path) -> dict[str, Any]:
    """Load literature JSON and return its evidence dicts with proper key types."""
    data = _load_and_validate_json(path, "enrichment_source", "Literature JSON")

    def _int_keys(d: dict | None) -> dict:
        if not d:
            return {}
        return {int(k): v for k, v in d.items()}

    def _int_keys_nested(d: dict | None) -> dict:
        """Convert outer keys to int; inner values are dicts (gene→snippets)."""
        if not d:
            return {}
        return {int(k): v for k, v in d.items()}

    return {
        "enrichment_source": data["enrichment_source"],
        "gaf_pmids": _int_keys(data.get("gaf_pmids")),
        "gaf_abstracts": _int_keys(data.get("gaf_abstracts")),
        "hub_gene_abstracts": data.get("hub_gene_abstracts") or {},
        "snippet_evidence": _int_keys(data.get("snippet_evidence")),
        "hub_gene_snippets": data.get("hub_gene_snippets") or {},
        "co_annotation_snippets": _int_keys_nested(data.get("co_annotation_snippets")),
        "cross_theme_snippets": data.get("cross_theme_snippets") or {},
        "cross_theme_gaf_snippets": data.get("cross_theme_gaf_snippets") or {},
    }


def _print_dry_run(genes: list[str] | None, args: any, input_mode: str) -> None:
    """Print dry-run information to stdout without executing analysis."""
    print("=" * 80)
    print("GO Enrichment Analysis - DRY RUN")
    print("=" * 80)

    # Input configuration
    print(f"\n## INPUT MODE: {input_mode}")
    if input_mode == "genes" and genes:
        print(f"Gene count: {len(genes)}")
        if len(genes) <= 20:
            print(f"Genes: {', '.join(genes)}")
        else:
            print(f"First 10: {', '.join(genes[:10])}")
            print(f"Last 10: {', '.join(genes[-10:])}")
    elif input_mode == "enrichment":
        print(f"Resuming from: {args.enrichment_json}")
    elif input_mode == "literature":
        print(f"Resuming from: {args.literature_json}")

    # Prepare output paths
    base_output = Path(args.output)
    if base_output.suffix:
        base_output = base_output.with_suffix("")
    enrichment_path = base_output.parent / f"{base_output.name}_enrichment.json"
    literature_path = base_output.parent / f"{base_output.name}_literature.json"
    explanation_path = base_output.parent / f"{base_output.name}_explanation.md"
    csv_path = base_output.parent / f"{base_output.name}_themes.csv"

    stop_after = getattr(args, "stop_after", None)

    if input_mode == "genes":
        print(f"\nSpecies: {args.species}")
        print(f"Min IC: {args.min_ic}")
        print(f"Min leaves: {args.min_leaves}")
        print(f"Max genes: {args.max_genes}")
        print(f"FDR threshold: {args.fdr}")

    print(f"\nOutput files:")
    if input_mode == "genes":
        print(f"  Enrichment: {enrichment_path}")
    if stop_after != "enrichment":
        print(f"  Literature: {literature_path}")
    if stop_after is None:
        print(f"  Explanation: {explanation_path}")

    # Phase 1 plan
    if input_mode == "genes":
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
        print("6. Build hierarchical themes using MRCEA-B algorithm")
        print(f"   - Anchor candidates: IC ≥ {args.min_ic}")
        print(f"   - Require ≥{args.min_leaves} enriched leaves per theme")
        print("7. Identify hub genes (appearing in 3+ themes)")
        print(f"\nOutput: {enrichment_path}")

    if stop_after == "enrichment":
        print("\n--stop-after enrichment: pipeline stops here")
    else:
        # Phase 1b plan
        if input_mode in ("genes", "enrichment"):
            print("\n" + "=" * 80)
            print("## PHASE 1b: LITERATURE PRE-FETCH")
            print("=" * 80)
            print("\nSteps that would be executed:")
            print("1. Build GAF reference index for themes")
            print("2. ASTA snippet search (if ASTA_API_KEY set)")
            print("3. Europe PMC abstract fetch for GAF PMIDs")
            print("4. Europe PMC abstract fetch for hub genes")
            print(f"\nOutput: {literature_path}")

        if stop_after == "literature":
            print("\n--stop-after literature: pipeline stops here")
        else:
            # Phase 2 plan
            print("\n" + "=" * 80)
            print("## PHASE 2: LLM EXPLANATION GENERATION")
            print("=" * 80)
            print(f"\nModel: {args.model}")
            print(f"Output format: Markdown")
            print(f"Temperature: 0.1")

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

            print(f"\nOutput: {explanation_path}")

    print("\n" + "=" * 80)
    print("DRY RUN COMPLETE - No analysis was executed")
    print("=" * 80)


def _run_phase1(args: argparse.Namespace, genes: list[str], enrichment_path: Path) -> dict:
    """Run Phase 1: GO enrichment analysis."""
    print("\n" + "=" * 80)
    result = run_go_enrichment(
        gene_symbols=genes,
        species=args.species,
        fdr_threshold=args.fdr,
        min_ic=args.min_ic,
        min_leaves=args.min_leaves,
        max_genes=args.max_genes,
        namespaces=args.namespace,
    )
    print("=" * 80)

    with open(enrichment_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n✓ Enrichment data saved to: {enrichment_path.absolute()}")
    return result


def _run_phase1b(
    enrichment_output: dict,
    args: argparse.Namespace,
    base_output: Path,
    enrichment_path: Path,
) -> tuple[dict | None, dict | None, dict | None, dict | None, dict | None, dict | None, dict | None, dict | None]:
    """Run Phase 1b: Literature pre-fetch.

    Returns (gaf_pmids, gaf_abstracts, hub_gene_abstracts, snippet_evidence,
             hub_gene_snippets, co_annotation_snippets, cross_theme_snippets,
             cross_theme_gaf_snippets).
    """
    all_themes = enrichment_output.get("themes", [])
    hub_genes_data = enrichment_output.get("hub_genes", {})

    # Cap themes for literature fetch + explanation
    max_explained = getattr(args, "max_explained_themes", None) or len(all_themes)
    themes = all_themes[:max_explained]
    if len(all_themes) > max_explained:
        print(f"\n⚠ Capping literature search to first {max_explained} of {len(all_themes)} themes")

    gaf_pmids = None
    gaf_abstracts = None
    hub_gene_abstracts = None
    snippet_evidence = None
    hub_gene_snippets = None
    co_annotation_snippets = None
    cross_theme_snippets = None
    cross_theme_gaf_snippets = None

    print("\n" + "=" * 80)
    print("Reference Pre-fetch - Phase 1b")
    print("=" * 80)

    # Always: GAF-curated PMIDs per theme (runs on ALL themes, not capped)
    if all_themes:
        try:
            from .services.reference_retrieval_service import get_gaf_pmids_for_themes
            from .utils.data_downloader import ensure_gaf_data, ensure_go_data
            from .utils.go_data_loader import load_go_data
            from .utils.reference_index import get_descendants_closure, load_gaf_with_pmids

            print(f"\nBuilding GAF reference index for {len(all_themes)} theme(s)...")
            gaf_path = ensure_gaf_data(species=args.species)
            go_path = ensure_go_data()
            godag = load_go_data(go_path)

            all_genes: set[str] = set()
            all_go_ids: set[str] = set()
            for t in all_themes:
                all_genes.update(t.get("anchor_term", {}).get("genes", []))
                anchor_go = t.get("anchor_term", {}).get("go_id", "")
                if anchor_go:
                    all_go_ids.add(anchor_go)
                for st in t.get("specific_terms", []):
                    all_genes.update(st.get("genes", []))
                    st_go = st.get("go_id", "")
                    if st_go:
                        all_go_ids.add(st_go)

            ref_index = load_gaf_with_pmids(gaf_path, godag, genes_of_interest=all_genes)
            descendants_closure = get_descendants_closure(all_go_ids, godag)
            gaf_pmids = get_gaf_pmids_for_themes(
                all_themes, ref_index, descendants_closure=descendants_closure
            )

            # Resolve GO IDs to names so LLM context shows gene→term_name
            for _theme_entries in gaf_pmids.values():
                for entry in _theme_entries:
                    gene_go_map = entry.get("gene_go_map", {})
                    named_map: dict[str, list[str]] = {}
                    for gene, go_ids_list in gene_go_map.items():
                        names = []
                        for gid in go_ids_list:
                            term = godag.get(gid)
                            names.append(f"{term.name} [{gid}]" if term else gid)
                        named_map[gene] = names
                    entry["gene_go_named"] = named_map

            themes_with_pmids = sum(1 for v in gaf_pmids.values() if v)
            total_pmids = sum(len(v) for v in gaf_pmids.values())
            n_coannot = sum(
                1
                for entries in gaf_pmids.values()
                for e in entries
                if len(e.get("genes_covered", [])) >= 2
            )
            print(f"✓ Found {total_pmids} GAF PMIDs across {themes_with_pmids}/{len(all_themes)} themes")
            if n_coannot:
                print(f"  ({n_coannot} co-annotation PMIDs covering 2+ genes)")

            # Save GAF PMIDs as sidecar JSON for interactive skill use
            gaf_pmids_path = base_output.parent / f"{base_output.name}_gaf_pmids.json"
            with open(gaf_pmids_path, "w") as f:
                json.dump({str(k): v for k, v in gaf_pmids.items()}, f, indent=2)
            print(f"✓ GAF PMIDs saved to: {gaf_pmids_path.name}")
        except Exception as e:
            print(f"\n⚠ GAF reference index failed: {e}")
            print("  Continuing without GAF citations...")

    # Filter gaf_pmids to explained themes only (sidecar already saved with all themes)
    if gaf_pmids and len(all_themes) > max_explained:
        gaf_pmids = {k: v for k, v in gaf_pmids.items() if k < max_explained}

    # Determine literature search scope based on --literature-search flag
    # Always: GAF-scoped ASTA snippets, scoped co-annotations, GAF abstracts
    # --literature-search only: unscoped widening, hub gene ASTA, hub gene Europe PMC
    lit_search = getattr(args, "literature_search", False)

    if lit_search:
        print("\n⚠ Literature search enabled — external search results are non-deterministic and paper quality varies")

    # Deprecation warning for --no-literature-search
    if getattr(args, "no_literature_search", False):
        warnings.warn(
            "--no-literature-search is deprecated and ignored. "
            "External literature APIs now require --literature-search to enable.",
            DeprecationWarning,
            stacklevel=1,
        )

    # ASTA snippet search (preferred when API key available)
    asta_api_key = os.getenv("ASTA_API_KEY")
    if asta_api_key:
        print("\nUsing ASTA (Semantic Scholar) for full-text snippet search...")
        try:
            from .services.asta_literature_service import (
                fetch_snippets_for_co_annotations,
                fetch_snippets_for_cross_theme_co_annotations,
                fetch_snippets_for_cross_theme_pmids,
                fetch_snippets_for_gaf_pmids,
                fetch_snippets_for_hub_genes,
            )
            from .services.go_markdown_explanation_service import _build_cross_theme_index

            # Always: GAF-scoped snippet search
            if gaf_pmids:
                snippet_evidence = fetch_snippets_for_gaf_pmids(
                    gaf_pmids, themes, asta_api_key
                )
                themes_with_snippets = sum(1 for v in snippet_evidence.values() if v)
                total_snippets = sum(len(v) for v in snippet_evidence.values())
                print(f"✓ Found {total_snippets} snippets across {themes_with_snippets}/{len(themes)} themes")

            # --literature-search only: hub gene unscoped ASTA
            if hub_genes_data and lit_search:
                hub_gene_snippets = fetch_snippets_for_hub_genes(
                    hub_genes_data, themes, asta_api_key
                )
                genes_with_snippets = sum(1 for v in hub_gene_snippets.values() if v)
                print(f"✓ Found snippets for {genes_with_snippets}/{min(len(hub_genes_data), 20)} hub genes")

            # Always: scoped co-annotation queries; widening only with --literature-search
            if gaf_pmids:
                print("\nSearching for co-annotation evidence...")
                co_annotation_snippets = fetch_snippets_for_co_annotations(
                    gaf_pmids, themes, asta_api_key,
                    widen_on_miss=lit_search,
                    snippet_evidence=snippet_evidence,
                )
                n_co = sum(
                    len(snippets)
                    for gene_snips in (co_annotation_snippets or {}).values()
                    for snippets in gene_snips.values()
                )
                print(f"✓ Found {n_co} within-theme co-annotation snippet(s)")

                cross_theme_index = _build_cross_theme_index(gaf_pmids, themes)
                if cross_theme_index:
                    cross_theme_snippets = fetch_snippets_for_cross_theme_co_annotations(
                        cross_theme_index, asta_api_key,
                        widen_on_miss=lit_search,
                    )
                    n_ct = sum(len(v) for v in (cross_theme_snippets or {}).values())
                    print(f"✓ Found {n_ct} cross-theme co-annotation snippet(s)")

                    # Fetch snippets scoped to cross-theme GAF PMIDs
                    print("\nFetching snippets for cross-theme GAF PMIDs...")
                    cross_theme_gaf_snippets = fetch_snippets_for_cross_theme_pmids(
                        cross_theme_index, asta_api_key,
                    )
                    n_ctg = sum(len(v) for v in (cross_theme_gaf_snippets or {}).values())
                    print(f"✓ Found {n_ctg} cross-theme GAF PMID snippet(s)")

        except Exception as e:
            print(f"⚠ ASTA search failed: {e}")
            print("  Falling back to Europe PMC abstracts...")
    else:
        print("\nNote: Set ASTA_API_KEY for richer full-text snippet evidence.")

    # Always: Fetch abstracts for GAF PMIDs via Europe PMC
    if gaf_pmids:
        print(f"\nFetching abstracts for GAF PMIDs via Europe PMC...")
        try:
            from .services.artl_literature_service import fetch_abstracts_for_gaf_pmids
            gaf_abstracts = fetch_abstracts_for_gaf_pmids(gaf_pmids)
        except Exception as e:
            print(f"\n⚠ GAF PMID abstract fetch failed: {e}")
            print("  Continuing without GAF abstracts (PMID anchors still available)...")

    # --literature-search only: Europe PMC search for top hub genes
    if hub_genes_data and lit_search:
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

    # Save literature evidence
    lit_path = _save_literature_json(
        base_output,
        str(enrichment_path),
        gaf_pmids,
        gaf_abstracts,
        hub_gene_abstracts,
        snippet_evidence,
        hub_gene_snippets,
        co_annotation_snippets,
        cross_theme_snippets,
        cross_theme_gaf_snippets,
    )
    print(f"\n✓ Literature evidence saved to: {lit_path.name}")

    return gaf_pmids, gaf_abstracts, hub_gene_abstracts, snippet_evidence, hub_gene_snippets, co_annotation_snippets, cross_theme_snippets, cross_theme_gaf_snippets


def _run_phase1c(
    enrichment_output: dict,
    args: argparse.Namespace,
    gaf_pmids: dict | None,
    gaf_abstracts: dict | None,
    hub_gene_abstracts: dict | None,
    snippet_evidence: dict | None,
    hub_gene_snippets: dict | None,
    co_annotation_snippets: dict | None = None,
    cross_theme_snippets: dict | None = None,
    cross_theme_gaf_snippets: dict | None = None,
) -> dict | None:
    """Run Phase 1c: Per-gene evidence narrative generation.

    Each gene gets a focused LLM call with its evidence, producing a
    1-2 sentence mechanistic narrative. These replace raw snippets in the
    synthesiser context.

    Returns:
        Gene narratives dict or None if no evidence available.
    """
    # Check if there's any evidence to narrate
    has_evidence = any([
        snippet_evidence,
        hub_gene_snippets,
        co_annotation_snippets,
        cross_theme_snippets,
        cross_theme_gaf_snippets,
        gaf_pmids,
    ])
    if not has_evidence:
        return None

    print("\n" + "=" * 80)
    print("Per-Gene Evidence Narratives - Phase 1c")
    print("=" * 80)

    try:
        from .services.evidence_narrative_service import generate_gene_narratives

        # Use gpt-4o-mini for cost-effective subagent calls
        narrative_model = "gpt-4o-mini"
        print(f"  Model: {narrative_model} (cost-optimised subagent)")

        gene_narratives = generate_gene_narratives(
            enrichment_output=enrichment_output,
            gaf_pmids=gaf_pmids,
            gaf_abstracts=gaf_abstracts,
            snippet_evidence=snippet_evidence,
            hub_gene_snippets=hub_gene_snippets,
            hub_gene_abstracts=hub_gene_abstracts,
            co_annotation_snippets=co_annotation_snippets,
            cross_theme_snippets=cross_theme_snippets,
            cross_theme_gaf_snippets=cross_theme_gaf_snippets,
            model=narrative_model,
        )

        usage = gene_narratives.get("usage", {})
        if usage.get("n_calls", 0) > 0:
            print(f"\n✓ Phase 1c complete: {usage['n_calls']} narrative(s) generated")
            if usage.get("total_cost", 0) > 0:
                print(f"  Phase 1c cost: ${usage['total_cost']:.4f} USD")
        else:
            print("\n  No narratives generated (no genes matched)")
            return None

        return gene_narratives

    except Exception as e:
        print(f"\n⚠ Phase 1c failed: {e}")
        print("  Continuing without gene narratives...")
        return None


def _run_phase2(
    enrichment_output: dict,
    args: argparse.Namespace,
    explanation_path: Path,
    gaf_pmids: dict | None,
    gaf_abstracts: dict | None,
    hub_gene_abstracts: dict | None,
    snippet_evidence: dict | None,
    hub_gene_snippets: dict | None,
    co_annotation_snippets: dict | None = None,
    cross_theme_snippets: dict | None = None,
    gene_narratives: dict | None = None,
    csv_path: Path | None = None,
) -> str:
    """Run Phase 2: LLM explanation generation."""
    csv_filename = csv_path.name if csv_path is not None else None
    print("\n" + "=" * 80)
    explanation_markdown = generate_markdown_explanation(
        enrichment_output=enrichment_output,
        model=args.model,
        temperature=0.1,
        max_tokens=args.max_tokens,
        gaf_pmids=gaf_pmids,
        gaf_abstracts=gaf_abstracts,
        hub_gene_abstracts=hub_gene_abstracts,
        snippet_evidence=snippet_evidence,
        hub_gene_snippets=hub_gene_snippets,
        co_annotation_snippets=co_annotation_snippets,
        cross_theme_snippets=cross_theme_snippets,
        gene_narratives=gene_narratives,
        csv_filename=csv_filename,
    )

    with open(explanation_path, "w") as f:
        f.write(explanation_markdown)
    print(f"\n✓ Explanation saved to: {explanation_path.absolute()}")

    if csv_path is not None:
        write_themes_csv(enrichment_output, csv_path)
        print(f"✓ Themes CSV saved to:  {csv_path.absolute()}")

    return explanation_markdown


def _print_summary(result: dict) -> None:
    """Print enrichment summary."""
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


def _parse_project_csv(csv_path: Path) -> list[dict]:
    """Parse a project CSV and return a list of row dicts.

    Required columns: ``name``, ``genes`` (comma-separated gene symbols).
    Optional columns: ``species``, ``description`` (any others are preserved).

    Raises:
        FileNotFoundError: If *csv_path* does not exist.
        ValueError: If required columns are missing or the file is empty.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Project CSV not found: {csv_path}")
    with open(csv_path, newline="") as fh:
        reader = _csv.DictReader(fh)
        rows = list(reader)
    if not rows:
        raise ValueError(f"Project CSV is empty: {csv_path}")
    headers = set(rows[0].keys())
    for col in ("name", "genes"):
        if col not in headers:
            raise ValueError(
                f"Project CSV missing required column '{col}' — found: {sorted(headers)}"
            )
    return rows


def _run_pipeline(
    args: argparse.Namespace,
    input_mode: str,
    genes: list[str] | None,
    base_output: Path,
) -> None:
    """Execute the analysis pipeline from the given starting point.

    Handles all three input modes (genes / enrichment / literature), respects
    ``args.stop_after``, and prints progress to stdout.  Raises on error so
    callers can handle failures independently (e.g. batch mode continues after
    a single list failure).

    Args:
        args: Parsed CLI namespace (may be a per-row copy with overrides).
        input_mode: One of ``"genes"``, ``"enrichment"``, ``"literature"``.
        genes: Gene symbols — required when *input_mode* is ``"genes"``.
        base_output: Base output path stem (parent dir is created if needed).
            All output files are written as ``{base_output.name}_{suffix}``.
    """
    base_output.parent.mkdir(parents=True, exist_ok=True)

    enrichment_path = base_output.parent / f"{base_output.name}_enrichment.json"
    explanation_path = base_output.parent / f"{base_output.name}_explanation.md"
    csv_path = base_output.parent / f"{base_output.name}_themes.csv"

    print("=" * 80)
    print("GO Enrichment Analysis - CLI Runner")
    print("=" * 80)

    # --- Phase 1: Enrichment ---
    if input_mode == "genes":
        assert genes is not None
        print(f"\n✓ Parsed {len(genes)} gene symbols")
        if len(genes) <= 20:
            print(f"  Genes: {', '.join(genes)}")
        else:
            print(f"  First 10: {', '.join(genes[:10])}...")
            print(f"  Last 10: {', '.join(genes[-10:])}...")

        print(f"\n✓ Parameters:")
        print(f"  Species: {args.species}")
        print(f"  Min IC: {args.min_ic}")
        print(f"  Min leaves: {args.min_leaves}")
        print(f"  Max genes: {args.max_genes}")
        print(f"  FDR threshold: {args.fdr}")

        enrichment_output = _run_phase1(args, genes, enrichment_path)
    elif input_mode == "enrichment":
        enrichment_path = Path(args.enrichment_json)
        enrichment_output = _load_and_validate_json(
            enrichment_path, "themes", "Enrichment JSON"
        )
        n_themes = len(enrichment_output.get("themes", []))
        print(f"\n✓ Loaded enrichment from: {enrichment_path}")
        print(f"  Themes: {n_themes}")
    else:
        # literature mode — load enrichment from the path recorded in literature JSON
        lit_path = Path(args.literature_json)
        lit_data = _load_literature_json(lit_path)
        enrichment_source = lit_data["enrichment_source"]
        enrichment_path = Path(enrichment_source)
        enrichment_output = _load_and_validate_json(
            enrichment_path, "themes", "Enrichment JSON (referenced by literature JSON)"
        )
        print(f"\n✓ Loaded literature from: {lit_path}")
        print(f"  Enrichment source: {enrichment_path}")

    if args.stop_after == "enrichment":
        _print_summary(enrichment_output)
        print("\n" + "=" * 80)
        print(f"✓ Stopped after enrichment (--stop-after enrichment)")
        print(f"  Enrichment: {enrichment_path.name}")
        print("=" * 80)
        return

    # --- Phase 1b: Literature pre-fetch ---
    if input_mode == "literature":
        gaf_pmids = lit_data["gaf_pmids"] or None
        gaf_abstracts = lit_data["gaf_abstracts"] or None
        hub_gene_abstracts = lit_data["hub_gene_abstracts"] or None
        snippet_evidence = lit_data["snippet_evidence"] or None
        hub_gene_snippets = lit_data["hub_gene_snippets"] or None
        co_annotation_snippets = lit_data.get("co_annotation_snippets") or None
        cross_theme_snippets = lit_data.get("cross_theme_snippets") or None
        cross_theme_gaf_snippets = lit_data.get("cross_theme_gaf_snippets") or None
    else:
        (gaf_pmids, gaf_abstracts, hub_gene_abstracts, snippet_evidence,
         hub_gene_snippets, co_annotation_snippets, cross_theme_snippets,
         cross_theme_gaf_snippets) = (
            _run_phase1b(enrichment_output, args, base_output, enrichment_path)
        )

    if args.stop_after == "literature":
        _print_summary(enrichment_output)
        print("\n" + "=" * 80)
        print(f"✓ Stopped after literature fetch (--stop-after literature)")
        print(f"  Enrichment: {enrichment_path.name}")
        lit_path_out = base_output.parent / f"{base_output.name}_literature.json"
        print(f"  Literature: {lit_path_out.name}")
        print("=" * 80)
        return

    # Trim themes for Phase 1c + Phase 2 (gaf_pmids already filtered in phase1b)
    max_explained = getattr(args, "max_explained_themes", None)
    all_themes_count = len(enrichment_output.get("themes", []))
    if max_explained and max_explained < all_themes_count:
        explained_output = {**enrichment_output, "themes": enrichment_output["themes"][:max_explained]}
    else:
        explained_output = enrichment_output

    # --- Phase 1c: Per-gene evidence narratives ---
    gene_narratives = _run_phase1c(
        explained_output, args,
        gaf_pmids, gaf_abstracts, hub_gene_abstracts,
        snippet_evidence, hub_gene_snippets,
        co_annotation_snippets, cross_theme_snippets,
        cross_theme_gaf_snippets,
    )

    # --- Phase 2: LLM explanation ---
    try:
        _run_phase2(
            explained_output,
            args,
            explanation_path,
            gaf_pmids,
            gaf_abstracts,
            hub_gene_abstracts,
            snippet_evidence,
            hub_gene_snippets,
            co_annotation_snippets,
            cross_theme_snippets,
            gene_narratives,
            csv_path=csv_path,
        )
    except Exception as e:
        print(f"\n❌ Error: Explanation generation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise

    print("=" * 80)
    _print_summary(enrichment_output)
    print("\n" + "=" * 80)
    print(f"✓ Analysis complete!")
    print(f"  Enrichment: {enrichment_path.name}")
    print(f"  Explanation: {explanation_path.name}")
    print("=" * 80)


def _run_batch(args: argparse.Namespace) -> int:
    """Run batch mode: process all gene lists defined in the project CSV.

    For each row the full pipeline (or up to ``args.stop_after``) is run.
    A single failure does not abort the batch — remaining lists are processed
    and the final return code is 1 if any list failed, 0 otherwise.

    Results are written under::

        results/{project_name}/{name}/{datestamp}/{name}_*.{ext}

    A ``batch_run.json`` manifest is appended to ``results/{project_name}/``.
    """
    csv_path = Path(args.project)
    rows = _parse_project_csv(csv_path)

    project_name = csv_path.stem
    datestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    results_dir = Path("results") / project_name
    n_total = len(rows)

    print("=" * 80)
    print(f"Batch Mode — Project: {project_name}")
    print(f"  {n_total} gene list(s) | {datestamp}")
    print(f"  Model: {args.model} | Stop after: {args.stop_after or 'full pipeline'}")
    print("=" * 80)

    # --- Dry-run: print plan only ---
    if args.dry_run:
        for i, row in enumerate(rows, 1):
            name = row["name"]
            genes = [g.strip() for g in row["genes"].split(",") if g.strip()]
            species = row.get("species") or args.species
            base_output = results_dir / name / datestamp / name
            print(f"\n[{i}/{n_total}] {name}")
            print(f"  Genes: {len(genes)} | Species: {species}")
            print(f"  Output: {base_output.parent}/")
        return 0

    run_results: list[dict] = []
    results_dir.mkdir(parents=True, exist_ok=True)

    for i, row in enumerate(rows, 1):
        name = row["name"].strip()
        raw_genes = row.get("genes", "")
        genes = [g.strip() for g in raw_genes.split(",") if g.strip()]
        species = (row.get("species") or "").strip() or args.species

        print(f"\n{'=' * 80}")
        print(f"[{i}/{n_total}] {name} — {len(genes)} genes (species: {species})")
        print("=" * 80)

        if not genes:
            print(f"  ⚠ Skipping: empty gene list", file=sys.stderr)
            run_results.append({"name": name, "n_genes": 0, "status": "skipped",
                                 "error": "empty gene list"})
            continue

        base_output = results_dir / name / datestamp / name
        args_row = copy.copy(args)
        args_row.species = species

        try:
            _run_pipeline(args_row, "genes", genes, base_output)
            run_results.append({
                "name": name,
                "n_genes": len(genes),
                "status": "ok",
                "path": str(base_output.parent),
            })
        except Exception as e:
            print(f"\n❌ [{name}] Failed: {e}", file=sys.stderr)
            run_results.append({
                "name": name,
                "n_genes": len(genes),
                "status": "error",
                "error": str(e),
            })

    # --- Write / append manifest ---
    manifest_path = results_dir / "batch_run.json"
    manifest_entry: dict[str, Any] = {
        "datestamp": datestamp,
        "project_csv": str(csv_path),
        "model": args.model,
        "stop_after": args.stop_after,
        "rows": run_results,
    }
    existing: list = []
    if manifest_path.exists():
        try:
            with open(manifest_path) as fh:
                existing = json.load(fh)
        except Exception:
            existing = []
    existing.append(manifest_entry)
    with open(manifest_path, "w") as fh:
        json.dump(existing, fh, indent=2)
    print(f"\n✓ Manifest saved: {manifest_path}")

    # --- Print batch summary ---
    n_ok = sum(1 for r in run_results if r["status"] == "ok")
    n_failed = sum(1 for r in run_results if r["status"] == "error")
    n_skipped = sum(1 for r in run_results if r["status"] == "skipped")
    print("\n" + "=" * 80)
    parts = [f"{n_ok}/{n_total} succeeded"]
    if n_failed:
        parts.append(f"{n_failed} failed")
    if n_skipped:
        parts.append(f"{n_skipped} skipped")
    print("Batch complete: " + ", ".join(parts))
    for r in run_results:
        if r["status"] == "error":
            print(f"  ✗ {r['name']}: {r.get('error', 'unknown error')}")
    print("=" * 80)

    return 0 if n_failed == 0 else 1


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Run hierarchical GO enrichment analysis with literature-grounded explanations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pipeline phases:
  Phase 1:  genes → enrichment             (saved as *_enrichment.json)
  Phase 1b: enrichment → literature        (saved as *_literature.json)
  Phase 2:  enrichment + literature → LLM  (saved as *_explanation.md)

Examples:
  # Full pipeline (enrichment → literature → explanation)
  %(prog)s --genes-file genes.txt -o results/my_analysis

  # Stop after enrichment only (no API keys needed)
  %(prog)s --genes-file genes.txt -o results/my_analysis --stop-after enrichment

  # Stop after literature fetch (no LLM call)
  %(prog)s --genes-file genes.txt -o results/my_analysis --stop-after literature

  # Resume from enrichment JSON (runs Phase 1b + 2)
  %(prog)s --enrichment-json results/my_analysis_enrichment.json -o results/my_analysis

  # Resume from literature JSON (runs Phase 2 only)
  %(prog)s --literature-json results/my_analysis_literature.json -o results/my_analysis
        """,
    )

    # Input (mutually exclusive — required=False to allow --project batch mode)
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        "--genes", type=str, help="Comma-separated gene symbols (e.g., TP53,BRCA1,BRCA2)"
    )
    input_group.add_argument(
        "--genes-file",
        type=str,
        help="Path to file with gene symbols (one per line, # for comments)",
    )
    input_group.add_argument(
        "--enrichment-json",
        type=str,
        help="Resume from enrichment JSON (skips Phase 1, runs Phase 1b + 2)",
    )
    input_group.add_argument(
        "--literature-json",
        type=str,
        help="Resume from literature JSON (skips Phase 1 + 1b, runs Phase 2 only)",
    )
    input_group.add_argument(
        "--project",
        type=str,
        metavar="CSV",
        help="Path to project CSV for batch mode. Processes all gene lists in the CSV. "
             "Project name = CSV filename stem. "
             "Results saved under results/{project_name}/{name}/{datestamp}/. "
             "Cannot be combined with --output.",
    )

    # Output (required for single-run; derived automatically in batch mode)
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        required=False,
        default=None,
        help="Output base path (e.g., results/my_analysis). Extensions added automatically. "
             "Not used with --project.",
    )

    # Pipeline control
    parser.add_argument(
        "--stop-after",
        type=str,
        choices=["enrichment", "literature"],
        default=None,
        help="Stop after the specified phase instead of running the full pipeline.",
    )
    parser.add_argument(
        "--literature-search",
        action="store_true",
        default=False,
        help="Enable external literature search (Europe PMC abstracts for hub genes, "
        "unscoped ASTA widening, hub gene ASTA). Results are non-deterministic.",
    )
    parser.add_argument(
        "--no-literature-search",
        action="store_true",
        default=False,
        help="(Deprecated) Use --literature-search instead. This flag is ignored.",
    )

    # Enrichment parameters
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
    parser.add_argument(
        "--min-ic",
        type=float,
        default=3.0,
        help="Minimum Information Content for anchor candidates (default: 3.0)",
    )
    parser.add_argument(
        "--min-leaves",
        type=int,
        default=2,
        help="Min leaves required to form a multi-leaf theme (default: 2)",
    )
    parser.add_argument(
        "--max-genes",
        type=int,
        default=30,
        help="Filter terms with > max-genes (default: 30)",
    )
    parser.add_argument(
        "--namespace",
        nargs="+",
        choices=["BP", "MF", "CC"],
        default=None,
        metavar="NS",
        help="GO namespace(s) to include: BP, MF, CC. Default: all three.",
    )

    # LLM parameters
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

    # Utility
    parser.add_argument(
        "--max-explained-themes",
        type=int,
        default=30,
        help="Max themes to fetch literature for and explain with LLM (default: 30). "
        "GAF PMID lookup still runs on all themes for the reference table.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Print analysis plan without executing.",
    )

    args = parser.parse_args()

    # --- Batch mode ---
    if args.project:
        if args.output:
            parser.error("--project and --output are mutually exclusive")
        try:
            return _run_batch(args)
        except (ValueError, FileNotFoundError) as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1

    # --- Single-run mode ---
    try:
        # Require --output for single-run
        if not args.output:
            parser.error("--output / -o is required (or use --project for batch mode)")

        # Require an input source
        if not any([args.genes, args.genes_file, args.enrichment_json, args.literature_json]):
            parser.error(
                "one of --genes, --genes-file, --enrichment-json, --literature-json is required"
            )

        input_mode = _determine_input_mode(args)

        # Parse genes (only needed for gene-based input)
        genes: list[str] | None = None
        if input_mode == "genes":
            genes = parse_gene_list(args.genes, args.genes_file)

        # Validate parameters
        if input_mode == "genes":
            if args.fdr <= 0 or args.fdr > 1:
                raise ValueError("FDR threshold must be between 0 and 1")

        # Warn about ignored enrichment params when resuming
        _warn_ignored_params(args, input_mode)

        # Warn about --model being ignored with --stop-after enrichment/literature
        if args.stop_after in ("enrichment", "literature") and args.model != "gpt-4o":
            warnings.warn(
                f"--model {args.model} is ignored when using --stop-after {args.stop_after} "
                "(no LLM explanation generated).",
                stacklevel=1,
            )

        # Warn about incompatible --stop-after with resume inputs
        if args.stop_after == "enrichment" and input_mode in ("enrichment", "literature"):
            raise ValueError(
                f"--stop-after enrichment is incompatible with --{input_mode}-json "
                "(enrichment already done)"
            )
        if args.stop_after == "literature" and input_mode == "literature":
            raise ValueError(
                "--stop-after literature is incompatible with --literature-json "
                "(literature already done)"
            )

        # Handle dry-run mode
        if args.dry_run:
            _print_dry_run(genes, args, input_mode)
            return 0

        base_output = Path(args.output)
        if base_output.suffix:
            base_output = base_output.with_suffix("")

        _run_pipeline(args, input_mode, genes, base_output)
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
