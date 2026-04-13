"""
ASTA (Semantic Scholar) Snippet Search Service

Fetches full-text evidence snippets (~500 words each) from Semantic Scholar's
ASTA MCP server. Snippets provide specific experimental evidence from paper body
text, which is often more informative than abstracts for grounding gene->GO claims.

Requires ASTA_API_KEY environment variable. When unavailable, the CLI falls back
to artl-mcp (Europe PMC) abstract-based evidence.
"""
from __future__ import annotations

import concurrent.futures
import json
import os
from typing import Any

import httpx

# Lazy imports for MCPToolSource (optional dependency)
MCPToolSource = None

_ASTA_MCP_URL = "https://asta-tools.allen.ai/mcp/v1"
_CALL_TIMEOUT = 15  # seconds per snippet_search call
_MAX_PARALLEL_WORKERS = 5


def _ensure_imports():
    """Lazy import cellsem-llm-client components."""
    global MCPToolSource
    if MCPToolSource is None:
        from cellsem_llm_client import MCPToolSource as _MCP

        MCPToolSource = _MCP


def _open_asta_source(api_key: str):
    """Create MCPToolSource for ASTA using streamable HTTP with auth headers.

    The ASTA MCP server uses streamable HTTP transport (not SSE). Headers must
    be passed via a pre-configured httpx.AsyncClient since
    streamable_http_client() doesn't accept headers directly.

    Args:
        api_key: ASTA API key for x-api-key header

    Returns:
        MCPToolSource configured for ASTA streamable HTTP
    """
    _ensure_imports()
    return MCPToolSource(
        _ASTA_MCP_URL,
        transport="streamable_http",
        http_client=httpx.AsyncClient(headers={"x-api-key": api_key}),
    )


def _call_with_timeout(fn, args, timeout=_CALL_TIMEOUT):
    """Call a function with a timeout to prevent hanging MCP calls.

    Args:
        fn: Callable to invoke
        args: Arguments dict for the callable
        timeout: Max seconds to wait

    Returns:
        Result from fn, or None on timeout

    Raises:
        concurrent.futures.TimeoutError: propagated as None return
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(fn, args)
        return future.result(timeout=timeout)


def _parallel_snippet_search(
    snippet_tool,
    queries: list[dict[str, Any]],
    max_workers: int = _MAX_PARALLEL_WORKERS,
    timeout: int = _CALL_TIMEOUT,
) -> list[str | None]:
    """Execute multiple snippet_search calls in parallel with per-call timeout.

    Args:
        snippet_tool: MCP tool object with a .handler(args) callable
        queries: List of argument dicts for snippet_search
        max_workers: Max concurrent threads
        timeout: Per-call timeout in seconds

    Returns:
        List of raw JSON strings (or None on failure), same order as queries.
    """
    if not queries:
        return []

    results: list[str | None] = [None] * len(queries)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_idx = {
            pool.submit(snippet_tool.handler, q): i
            for i, q in enumerate(queries)
        }
        for future in concurrent.futures.as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result(timeout=timeout)
            except Exception:
                results[idx] = None

    return results


# =============================================================================
# Public API
# =============================================================================


def fetch_snippets_for_gaf_pmids(
    gaf_pmids: dict[int, list[dict[str, Any]]],
    themes: list[dict[str, Any]],
    asta_api_key: str,
    max_snippets_per_theme: int = 5,
) -> dict[int, list[dict[str, Any]]]:
    """Fetch targeted snippets for GAF-curated PMIDs via ASTA snippet_search.

    For each theme, builds a query from anchor_term name + top genes,
    scoped to that theme's GAF PMIDs. Returns snippets with paper metadata.
    All theme queries run in parallel.

    Args:
        gaf_pmids: {theme_index: [{pmid, genes_covered}, ...]} from
            get_gaf_pmids_for_themes()
        themes: List of theme dicts from enrichment output
        asta_api_key: ASTA API key for authentication
        max_snippets_per_theme: Maximum snippets to return per theme

    Returns:
        {theme_index: [{paperId, title, authors, snippet_text, score}, ...]}
    """
    if not gaf_pmids:
        return {}

    results: dict[int, list[dict[str, Any]]] = {}

    try:
        with _open_asta_source(asta_api_key) as source:
            snippet_tool = _find_tool(source.tools, "snippet_search")
            if snippet_tool is None:
                print("  ⚠ snippet_search tool not found in ASTA MCP")
                return {i: [] for i in gaf_pmids}

            # Build all queries up front
            query_list: list[dict[str, Any]] = []
            theme_indices: list[int] = []

            for theme_idx, entries in gaf_pmids.items():
                pmids = [e.get("pmid", "") for e in entries if e.get("pmid")]
                if not pmids:
                    results[theme_idx] = []
                    continue

                anchor_name = ""
                if isinstance(theme_idx, int) and theme_idx < len(themes):
                    anchor_name = themes[theme_idx].get("anchor_term", {}).get("name", "")

                paper_ids = ",".join(f"PMID:{p}" for p in pmids)
                query = anchor_name or "gene function"

                print(f"  [Theme {theme_idx}] Snippet search: {query[:50]}... ({len(pmids)} papers)")

                query_list.append({
                    "query": query,
                    "paper_ids": paper_ids,
                    "limit": max_snippets_per_theme,
                })
                theme_indices.append(theme_idx)

            # Execute all in parallel
            raw_results = _parallel_snippet_search(snippet_tool, query_list)

            for i, theme_idx in enumerate(theme_indices):
                raw = raw_results[i]
                snippets = _parse_snippet_results(raw or "")
                snippets = _filter_snippets(snippets)
                snippets = _deduplicate_snippets(snippets)[:max_snippets_per_theme]
                results[theme_idx] = snippets
                print(f"    [Theme {theme_idx}] {len(snippets)} snippet(s) found")

    except Exception as e:
        print(f"  ⚠ ASTA MCP session failed: {e}")
        results = {i: [] for i in gaf_pmids}

    return results


def fetch_snippets_for_co_annotations(
    gaf_pmids: dict[int, list[dict[str, Any]]],
    themes: list[dict[str, Any]],
    asta_api_key: str,
    max_queries_per_theme: int = 3,
    max_snippets_per_query: int = 2,
    widen_on_miss: bool = True,
    snippet_evidence: dict[int, list[dict[str, Any]]] | None = None,
) -> dict[int, dict[str, list[dict[str, Any]]]]:
    """Fetch ASTA snippets for within-theme co-annotations.

    Finds genes annotated to 2+ GO terms within the same theme and searches
    for full-text evidence linking those processes. First tries scoped to the
    co-annotating PMID(s); widens to unscoped search if no snippets found.

    Skips genes where a GAF PMID already co-annotates the gene AND the scoped
    GAF snippet search already returned evidence (GAF-skip optimisation).

    Args:
        gaf_pmids: {theme_index: [{pmid, gene_go_map, gene_go_named, ...}]}
        themes: List of theme dicts from enrichment output
        asta_api_key: ASTA API key for authentication
        max_queries_per_theme: Max co-annotation queries per theme
        max_snippets_per_query: Max snippets per query
        widen_on_miss: If True, retry unscoped when scoped search returns 0
        snippet_evidence: Optional {theme_idx: [snippet_dicts]} from
            fetch_snippets_for_gaf_pmids. When provided, genes that already
            have scoped GAF snippets covering their co-annotating PMIDs are
            skipped.

    Returns:
        {theme_idx: {gene: [snippet_dicts]}}
    """
    if not gaf_pmids:
        return {}

    # Build set of PMIDs that already have snippets per theme for GAF-skip
    covered_pmids_per_theme: dict[int, set[str]] = {}
    if snippet_evidence:
        for theme_idx, snippets in snippet_evidence.items():
            covered_pmids_per_theme[theme_idx] = {
                s.get("pmid", "") for s in snippets if s.get("pmid")
            }

    # Scan for within-theme co-annotations
    co_annot_targets: dict[int, list[tuple[str, list[str], list[str]]]] = {}
    # Each tuple: (gene, [term_names], [pmids])
    for theme_idx, entries in gaf_pmids.items():
        gene_terms: dict[str, dict[str, list[str]]] = {}  # gene -> {term_name -> [pmids]}
        gene_pmids: dict[str, set[str]] = {}
        for entry in entries:
            pmid = entry.get("pmid", "")
            if not pmid:
                continue
            gene_go_named = entry.get("gene_go_named", {})
            gene_go_map = entry.get("gene_go_map", {})
            for gene, go_ids in gene_go_map.items():
                if len(go_ids) < 2:
                    continue
                # This gene has 2+ GO terms in this PMID within this theme
                if gene not in gene_terms:
                    gene_terms[gene] = {}
                    gene_pmids[gene] = set()
                gene_pmids[gene].add(pmid)
                named = gene_go_named.get(gene, go_ids)
                for name in named:
                    gene_terms[gene].setdefault(name, [])
                    if pmid not in gene_terms[gene][name]:
                        gene_terms[gene][name].append(pmid)

        if gene_terms:
            # GAF-skip: remove genes whose co-annotating PMIDs already have
            # scoped snippets from the GAF search
            covered = covered_pmids_per_theme.get(theme_idx, set())
            filtered_genes = {}
            for gene in gene_terms:
                if covered and gene_pmids[gene].issubset(covered):
                    continue  # All co-annotating PMIDs already have snippets
                filtered_genes[gene] = gene_terms[gene]

            if not filtered_genes:
                continue

            # Sort by number of distinct GO terms (desc), take top N
            ranked = sorted(
                filtered_genes.keys(),
                key=lambda g: len(filtered_genes[g]),
                reverse=True,
            )[:max_queries_per_theme]
            targets = []
            for gene in ranked:
                term_names = list(filtered_genes[gene].keys())[:2]  # First 2 terms for query
                pmids = list(gene_pmids[gene])
                targets.append((gene, term_names, pmids))
            co_annot_targets[theme_idx] = targets

    if not co_annot_targets:
        return {}

    results: dict[int, dict[str, list[dict[str, Any]]]] = {}

    try:
        with _open_asta_source(asta_api_key) as source:
            snippet_tool = _find_tool(source.tools, "snippet_search")
            if snippet_tool is None:
                print("  ⚠ snippet_search tool not found in ASTA MCP")
                return {}

            # Build all scoped queries
            scoped_queries: list[dict[str, Any]] = []
            query_keys: list[tuple[int, str, list[str], list[str]]] = []
            # Each key: (theme_idx, gene, term_names, pmids)

            for theme_idx, targets in co_annot_targets.items():
                results[theme_idx] = {}
                for gene, term_names, pmids in targets:
                    clean_terms = [t.split(" [GO:")[0] for t in term_names]
                    query = f"{gene} {' '.join(clean_terms)}"
                    paper_ids = ",".join(f"PMID:{p}" for p in pmids)

                    print(f"  [Theme {theme_idx}] Co-annotation: {query[:60]}... (scoped to {len(pmids)} PMIDs)")

                    scoped_queries.append({
                        "query": query,
                        "paper_ids": paper_ids,
                        "limit": 10,  # Fetch more for best-paper selection
                    })
                    query_keys.append((theme_idx, gene, term_names, pmids))

            # Execute scoped queries in parallel
            scoped_results = _parallel_snippet_search(snippet_tool, scoped_queries)

            # Identify queries that need widening
            widen_queries: list[dict[str, Any]] = []
            widen_indices: list[int] = []  # index into query_keys

            for i, (theme_idx, gene, term_names, pmids) in enumerate(query_keys):
                raw = scoped_results[i]
                snippets = _parse_snippet_results(raw or "")
                snippets = _filter_snippets(snippets)
                selected = _select_best_paper_snippets(snippets, max_total=max_snippets_per_query)

                if selected:
                    results[theme_idx][gene] = selected
                    print(f"    {len(selected)} snippet(s) for {gene}")
                elif widen_on_miss:
                    # Queue for widened search
                    clean_terms = [t.split(" [GO:")[0] for t in term_names]
                    query = f"{gene} {' '.join(clean_terms)}"
                    print(f"    0 scoped for {gene} → queuing widened search...")
                    widen_queries.append({
                        "query": query,
                        "limit": 10,
                    })
                    widen_indices.append(i)
                else:
                    results[theme_idx][gene] = []
                    print(f"    0 snippet(s) for {gene}")

            # Execute widened queries in parallel
            if widen_queries:
                widen_results = _parallel_snippet_search(snippet_tool, widen_queries)
                for j, orig_idx in enumerate(widen_indices):
                    theme_idx, gene, _, _ = query_keys[orig_idx]
                    raw = widen_results[j]
                    snippets = _parse_snippet_results(raw or "")
                    snippets = _filter_snippets(snippets)
                    selected = _select_best_paper_snippets(snippets, max_total=max_snippets_per_query)
                    results[theme_idx][gene] = selected
                    print(f"    {len(selected)} snippet(s) for {gene} (widened)")

    except Exception as e:
        print(f"  ⚠ ASTA MCP session failed: {e}")
        return {}

    return results


def fetch_snippets_for_cross_theme_co_annotations(
    cross_theme_index: dict[str, list[dict[str, Any]]],
    asta_api_key: str,
    max_genes: int = 10,
    max_snippets_per_query: int = 2,
    widen_on_miss: bool = True,
) -> dict[str, list[dict[str, Any]]]:
    """Fetch ASTA snippets for cross-theme co-annotations.

    For genes annotated to GO terms in different themes, searches for
    full-text evidence linking those functional domains. Scoped to the
    cross-theme PMIDs first, widened if no results. All queries run in parallel.

    Args:
        cross_theme_index: Output from _build_cross_theme_index():
            {gene: [{pmid, themes: [{index, name}], annotations: [...]}]}
        asta_api_key: ASTA API key for authentication
        max_genes: Maximum number of genes to query
        max_snippets_per_query: Maximum snippets per query
        widen_on_miss: If True, retry unscoped when scoped search returns 0

    Returns:
        {gene: [snippet_dicts]}
    """
    if not cross_theme_index:
        return {}

    # Select genes with most cross-theme PMIDs
    sorted_genes = sorted(
        cross_theme_index.items(),
        key=lambda x: len(x[1]),
        reverse=True,
    )[:max_genes]

    results: dict[str, list[dict[str, Any]]] = {}

    try:
        with _open_asta_source(asta_api_key) as source:
            snippet_tool = _find_tool(source.tools, "snippet_search")
            if snippet_tool is None:
                print("  ⚠ snippet_search tool not found in ASTA MCP")
                return {gene: [] for gene, _ in sorted_genes}

            # Build all scoped queries
            scoped_queries: list[dict[str, Any]] = []
            gene_query_data: list[tuple[str, str]] = []  # (gene, query_text)

            for gene, entries in sorted_genes:
                theme_names = []
                pmids = set()
                for entry in entries:
                    for t in entry.get("themes", []):
                        name = t.get("name", "")
                        if name and name not in theme_names:
                            theme_names.append(name)
                    pmids.add(entry["pmid"])

                query = f"{gene} {' '.join(theme_names[:2])}".strip()
                paper_ids = ",".join(f"PMID:{p}" for p in pmids)

                print(f"  [{gene}] Cross-theme co-annotation: {query[:60]}... (scoped to {len(pmids)} PMIDs)")

                scoped_queries.append({
                    "query": query,
                    "paper_ids": paper_ids,
                    "limit": 10,  # Fetch more for best-paper selection
                })
                gene_query_data.append((gene, query))

            # Execute scoped queries in parallel
            scoped_results = _parallel_snippet_search(snippet_tool, scoped_queries)

            # Identify queries that need widening
            widen_queries: list[dict[str, Any]] = []
            widen_indices: list[int] = []

            for i, (gene, query) in enumerate(gene_query_data):
                raw = scoped_results[i]
                snippets = _parse_snippet_results(raw or "")
                snippets = _filter_snippets(snippets)
                selected = _select_best_paper_snippets(snippets, max_total=max_snippets_per_query)

                if selected:
                    results[gene] = selected
                    print(f"    {len(selected)} snippet(s) for {gene}")
                elif widen_on_miss:
                    print(f"    0 scoped for {gene} → queuing widened search...")
                    widen_queries.append({
                        "query": query,
                        "limit": 10,
                    })
                    widen_indices.append(i)
                else:
                    results[gene] = []
                    print(f"    0 snippet(s) for {gene}")

            # Execute widened queries in parallel
            if widen_queries:
                widen_results = _parallel_snippet_search(snippet_tool, widen_queries)
                for j, orig_idx in enumerate(widen_indices):
                    gene, _ = gene_query_data[orig_idx]
                    raw = widen_results[j]
                    snippets = _parse_snippet_results(raw or "")
                    snippets = _filter_snippets(snippets)
                    selected = _select_best_paper_snippets(snippets, max_total=max_snippets_per_query)
                    results[gene] = selected
                    print(f"    {len(selected)} snippet(s) for {gene} (widened)")

    except Exception as e:
        print(f"  ⚠ ASTA MCP session failed: {e}")
        results = {gene: [] for gene, _ in sorted_genes}

    return results


def fetch_snippets_for_hub_genes(
    hub_genes: dict[str, Any],
    themes: list[dict[str, Any]],
    asta_api_key: str,
    max_hub_genes: int = 20,
    max_snippets_per_gene: int = 3,
) -> dict[str, list[dict[str, Any]]]:
    """Fetch supporting snippets for hub genes via ASTA snippet_search.

    For each hub gene, searches "{gene} {top_theme_name}" unscoped
    to discover supporting literature for cross-theme claims.
    All queries run in parallel.

    Args:
        hub_genes: hub_genes dict from enrichment output
            {gene: {"theme_count": int, "themes": [str, ...]}}
        themes: List of theme dicts (unused but kept for interface consistency)
        asta_api_key: ASTA API key for authentication
        max_hub_genes: Maximum number of hub genes to search
        max_snippets_per_gene: Maximum snippets per hub gene

    Returns:
        {gene_symbol: [{paperId, title, authors, snippet_text, score}, ...]}
    """
    if not hub_genes:
        return {}

    # Select top hub genes by theme_count
    sorted_genes = sorted(
        hub_genes.items(), key=lambda x: x[1].get("theme_count", 0), reverse=True
    )[:max_hub_genes]

    results: dict[str, list[dict[str, Any]]] = {}

    try:
        with _open_asta_source(asta_api_key) as source:
            snippet_tool = _find_tool(source.tools, "snippet_search")
            if snippet_tool is None:
                print("  ⚠ snippet_search tool not found in ASTA MCP")
                return {gene: [] for gene, _ in sorted_genes}

            # Build all queries
            query_list: list[dict[str, Any]] = []
            gene_names: list[str] = []

            for gene, data in sorted_genes:
                top_theme = data.get("themes", [""])[0] if data.get("themes") else ""
                query = f"{gene} {top_theme}".strip()
                print(f"  [{gene}] Snippet search: {query[:70]}...")

                query_list.append({
                    "query": query,
                    "limit": max_snippets_per_gene,
                })
                gene_names.append(gene)

            # Execute all in parallel
            raw_results = _parallel_snippet_search(snippet_tool, query_list)

            for i, gene in enumerate(gene_names):
                raw = raw_results[i]
                snippets = _parse_snippet_results(raw or "")
                snippets = _filter_snippets(snippets)
                snippets = _deduplicate_snippets(snippets)[:max_snippets_per_gene]
                results[gene] = snippets
                print(f"    [{gene}] {len(snippets)} snippet(s) found")

    except Exception as e:
        print(f"  ⚠ ASTA MCP session failed: {e}")
        results = {gene: [] for gene, _ in sorted_genes}

    return results


# =============================================================================
# Internal Helpers
# =============================================================================


def _find_tool(tools: list, name: str):
    """Find a tool by name in the MCP tool list."""
    return next((t for t in tools if t.name == name), None)


def _select_best_paper_snippets(
    snippets: list[dict[str, Any]],
    max_from_top: int = 3,
    max_from_runner_up: int = 1,
    max_total: int = 4,
) -> list[dict[str, Any]]:
    """Select snippets using top-paper + runner-up strategy.

    Groups snippets by paperId, returns up to ``max_from_top`` from the
    highest-scoring paper and ``max_from_runner_up`` from the runner-up,
    capped at ``max_total``.

    Args:
        snippets: Parsed, filtered snippet dicts (need not be deduplicated)
        max_from_top: Max snippets from the top-scoring paper
        max_from_runner_up: Max snippets from the runner-up paper
        max_total: Overall cap

    Returns:
        Selected snippet list, sorted by score descending.
    """
    if not snippets:
        return []

    # Group by paper
    by_paper: dict[str, list[dict[str, Any]]] = {}
    for s in snippets:
        key = s.get("paperId", "") or s.get("pmid", "") or s.get("snippet_text", "")[:100]
        by_paper.setdefault(key, []).append(s)

    # Sort each group by score desc
    for key in by_paper:
        by_paper[key].sort(key=lambda s: s.get("score", 0.0), reverse=True)

    # Rank papers by their best snippet score
    ranked_papers = sorted(
        by_paper.items(),
        key=lambda kv: kv[1][0].get("score", 0.0),
        reverse=True,
    )

    selected: list[dict[str, Any]] = []

    # Top paper
    if ranked_papers:
        _, top_snippets = ranked_papers[0]
        selected.extend(top_snippets[:max_from_top])

    # Runner-up
    if len(ranked_papers) > 1:
        _, runner_snippets = ranked_papers[1]
        selected.extend(runner_snippets[:max_from_runner_up])

    # Cap and sort
    selected = selected[:max_total]
    selected.sort(key=lambda s: s.get("score", 0.0), reverse=True)
    return selected


def _parse_snippet_results(raw: str) -> list[dict[str, Any]]:
    """Parse ASTA snippet_search response into snippet dicts.

    Args:
        raw: Raw JSON string from the ASTA snippet_search handler

    Returns:
        List of snippet dicts with keys: paperId, title, authors,
        snippet_text, score. Returns empty list on parse failure.
    """
    if not raw:
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []

    # ASTA returns {"data": [...]} or a bare list
    if isinstance(data, dict):
        items = data.get("data", data.get("snippets", data.get("results", [])))
    elif isinstance(data, list):
        items = data
    else:
        return []

    snippets = []
    for item in items:
        if not isinstance(item, dict):
            continue

        # Extract paper info — ASTA nests under "paper" key
        paper = item.get("paper", {})
        if not isinstance(paper, dict):
            paper = {}

        paper_id = str(
            paper.get("paperId", paper.get("corpusId", item.get("paperId", "")))
        ).strip()
        title = paper.get("title", item.get("title", ""))

        # Authors
        authors_list = paper.get("authors", item.get("authors", []))
        if isinstance(authors_list, list):
            surnames = [
                a.get("name", "") if isinstance(a, dict) else str(a)
                for a in authors_list[:3]
            ]
            authors = ", ".join(s for s in surnames if s)
            if len(authors_list) > 3:
                authors += " et al."
        else:
            authors = ""

        # Snippet text: nested under "snippet.text" or flat "snippetText"
        snippet_obj = item.get("snippet", {})
        if isinstance(snippet_obj, dict):
            snippet_text = snippet_obj.get("text", "")
        elif isinstance(snippet_obj, str):
            snippet_text = snippet_obj
        else:
            snippet_text = ""
        if not snippet_text:
            snippet_text = item.get("snippetText", item.get("text", ""))
        score = item.get("score", 0.0)

        # Extract PMID from externalIds if available
        external_ids = paper.get("externalIds", {})
        if isinstance(external_ids, dict):
            pmid = external_ids.get("PubMed", "")
        else:
            pmid = ""

        if snippet_text:
            snippets.append({
                "paperId": paper_id,
                "pmid": str(pmid) if pmid else "",
                "title": title,
                "authors": authors,
                "snippet_text": snippet_text,
                "score": float(score) if score else 0.0,
            })

    return snippets


def _filter_snippets(
    snippets: list[dict[str, Any]],
    min_score: float = 0.2,
) -> list[dict[str, Any]]:
    """Filter out low-relevance snippets.

    Args:
        snippets: List of snippet dicts
        min_score: Minimum relevance score threshold

    Returns:
        Filtered list of snippets above the score threshold
    """
    return [s for s in snippets if s.get("score", 0.0) >= min_score]


def _deduplicate_snippets(snippets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove near-duplicate snippets from the same paper.

    Keeps the highest-scored snippet per paper ID.

    Args:
        snippets: List of snippet dicts

    Returns:
        Deduplicated list of snippets
    """
    seen: dict[str, dict[str, Any]] = {}
    for s in snippets:
        key = s.get("paperId", "") or s.get("pmid", "")
        if not key:
            # No dedup key — keep as-is
            key = s.get("snippet_text", "")[:100]

        if key not in seen or s.get("score", 0) > seen[key].get("score", 0):
            seen[key] = s

    return list(seen.values())


def resolve_missing_pmids(
    snippets: list[dict[str, Any]],
    asta_api_key: str,
) -> list[dict[str, Any]]:
    """Batch-resolve paperId → PMID for snippets missing a PMID.

    Uses Semantic Scholar get_paper_batch API to look up externalIds for
    any snippet that has a paperId but no PMID. Updates snippet dicts
    in-place and returns the same list.

    Args:
        snippets: List of snippet dicts (modified in-place)
        asta_api_key: ASTA API key for authentication

    Returns:
        The same list of snippets, with pmid fields filled where possible.
    """
    # Identify snippets needing resolution
    needs_resolution: dict[str, list[int]] = {}  # paperId → [indices]
    for idx, s in enumerate(snippets):
        if s.get("pmid"):
            continue
        paper_id = s.get("paperId", "").strip()
        if not paper_id:
            continue
        needs_resolution.setdefault(paper_id, []).append(idx)

    if not needs_resolution:
        return snippets

    try:
        with _open_asta_source(asta_api_key) as source:
            batch_tool = _find_tool(source.tools, "get_paper_batch")
            if batch_tool is None:
                print("  ⚠ get_paper_batch tool not found in ASTA MCP")
                return snippets

            paper_ids = list(needs_resolution.keys())
            result = _call_with_timeout(
                batch_tool.handler,
                {"ids": paper_ids, "fields": "externalIds"},
                timeout=_CALL_TIMEOUT,
            )

            if not result:
                return snippets

            try:
                papers = json.loads(result) if isinstance(result, str) else result
            except (json.JSONDecodeError, TypeError):
                return snippets

            if not isinstance(papers, list):
                return snippets

            for paper in papers:
                if not isinstance(paper, dict):
                    continue
                paper_id = paper.get("paperId", "")
                external_ids = paper.get("externalIds", {})
                if not isinstance(external_ids, dict):
                    continue
                pmid = external_ids.get("PubMed", "")
                if pmid and paper_id in needs_resolution:
                    for idx in needs_resolution[paper_id]:
                        snippets[idx]["pmid"] = str(pmid)

    except Exception as e:
        print(f"  ⚠ PMID batch resolution failed: {e}")

    resolved = sum(1 for s in snippets if s.get("pmid"))
    total = len(snippets)
    print(f"  PMID resolution: {resolved}/{total} snippets have PMIDs")

    return snippets


def fetch_snippets_for_cross_theme_pmids(
    cross_theme_index: dict[str, list[dict[str, Any]]],
    asta_api_key: str,
    max_genes: int = 10,
    max_snippets_per_gene: int = 3,
) -> dict[str, list[dict[str, Any]]]:
    """Fetch ASTA snippets scoped to cross-theme GAF PMIDs.

    For each gene in the cross-theme index, collects its PMIDs and searches
    ASTA for snippets scoped to those papers + gene name. This enriches
    the cross-theme GAF PMID entries (which otherwise have no paper content)
    with actual full-text evidence.

    Args:
        cross_theme_index: Output from _build_cross_theme_index():
            {gene: [{pmid, themes: [{index, name}], annotations: [...]}]}
        asta_api_key: ASTA API key for authentication
        max_genes: Maximum number of genes to query
        max_snippets_per_gene: Maximum snippets per gene

    Returns:
        {gene: [snippet_dicts]}
    """
    if not cross_theme_index:
        return {}

    # Select genes with most cross-theme PMIDs
    sorted_genes = sorted(
        cross_theme_index.items(),
        key=lambda x: len(x[1]),
        reverse=True,
    )[:max_genes]

    results: dict[str, list[dict[str, Any]]] = {}

    try:
        with _open_asta_source(asta_api_key) as source:
            snippet_tool = _find_tool(source.tools, "snippet_search")
            if snippet_tool is None:
                print("  ⚠ snippet_search tool not found in ASTA MCP")
                return {gene: [] for gene, _ in sorted_genes}

            # Build all queries scoped to each gene's cross-theme PMIDs
            query_list: list[dict[str, Any]] = []
            gene_names: list[str] = []

            for gene, entries in sorted_genes:
                pmids = set()
                theme_names = []
                for entry in entries:
                    pmids.add(entry["pmid"])
                    for t in entry.get("themes", []):
                        name = t.get("name", "")
                        if name and name not in theme_names:
                            theme_names.append(name)

                paper_ids = ",".join(f"PMID:{p}" for p in pmids)
                query = f"{gene} {' '.join(theme_names[:2])}".strip()

                print(f"  [{gene}] Cross-theme PMID snippets: {query[:60]}... (scoped to {len(pmids)} PMIDs)")

                query_list.append({
                    "query": query,
                    "paper_ids": paper_ids,
                    "limit": max_snippets_per_gene * 2,  # Fetch more for filtering
                })
                gene_names.append(gene)

            # Execute all in parallel
            raw_results = _parallel_snippet_search(snippet_tool, query_list)

            for i, gene in enumerate(gene_names):
                raw = raw_results[i]
                snippets = _parse_snippet_results(raw or "")
                snippets = _filter_snippets(snippets)
                snippets = _deduplicate_snippets(snippets)[:max_snippets_per_gene]
                results[gene] = snippets
                print(f"    [{gene}] {len(snippets)} snippet(s) found")

    except Exception as e:
        print(f"  ⚠ ASTA MCP session failed: {e}")
        results = {gene: [] for gene, _ in sorted_genes}

    return results
