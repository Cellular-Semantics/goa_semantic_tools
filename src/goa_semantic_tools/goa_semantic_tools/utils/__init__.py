"""Repo-specific utilities that do not belong in agents/services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

# GO enrichment utilities
from .data_downloader import ensure_gaf_data, ensure_go_data, get_reference_data_dir
from .go_data_loader import build_gene_to_go_mapping, load_gene_annotations, load_go_data
from .go_hierarchy import (
    EnrichedTerm,
    HierarchicalTheme,
    build_depth_anchor_themes,
    compute_enrichment_leaves,
    compute_hub_genes,
    enriched_terms_to_dict,
    find_leaves,
    get_all_descendants,
    is_descendant,
    merge_identical_gene_sets,
    themes_to_dict,
)
from .reference_index import (
    find_pmids_covering_genes,
    get_descendants_closure,
    get_genes_for_pmid,
    get_pmids_for_gene_term,
    load_gaf_with_pmids,
)


def chunk_items(items: Iterable[str], size: int = 10) -> List[List[str]]:
    """Simple batching helper for splitting sequences in tooling scripts."""
    batch: List[str] = []
    result: List[List[str]] = []
    for item in items:
        batch.append(item)
        if len(batch) >= size:
            result.append(batch)
            batch = []
    if batch:
        result.append(batch)
    return result


@dataclass
class ToolingContext:
    """Context object that CLI scripts can extend with repo-specific settings."""

    workspace: str
    dry_run: bool = False

