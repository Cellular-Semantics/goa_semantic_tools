"""
artl-mcp Literature Search Service

Resolves unresolved assertions via Europe PMC literature search using
cellsem-llm-client MCPToolSource + LiteLLMAgent.

This service is optional — artl-mcp is only needed when GAF-based
reference lookup fails to find supporting PMIDs.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import yaml

from .reference_retrieval_service import AtomicAssertion, ReferenceMatch

# Lazy imports for MCPToolSource and LiteLLMAgent
# (artl-mcp is optional; import at call time)
MCPToolSource = None
LiteLLMAgent = None


def _ensure_imports():
    """Lazy import cellsem-llm-client components."""
    global MCPToolSource, LiteLLMAgent
    if MCPToolSource is None:
        from cellsem_llm_client import MCPToolSource as _MCP
        from cellsem_llm_client.agents.agent_connection import LiteLLMAgent as _Agent

        MCPToolSource = _MCP
        LiteLLMAgent = _Agent


# =============================================================================
# Public API
# =============================================================================


def resolve_assertions_via_literature(
    assertions: list[AtomicAssertion],
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
    max_turns: int = 5,
    max_refs_per_assertion: int = 3,
) -> list[tuple[AtomicAssertion, list[ReferenceMatch]]]:
    """Resolve assertions via Europe PMC literature search.

    Uses a single MCPToolSource session for the whole batch. Each assertion
    is sent to an LLM agent with artl-mcp tools to search Europe PMC.

    Args:
        assertions: List of AtomicAssertion objects to resolve
        model: LLM model identifier (default: gpt-4o-mini)
        api_key: API key for LLM provider (if None, uses env vars)
        max_turns: Maximum agentic turns per assertion
        max_refs_per_assertion: Maximum references to return per assertion

    Returns:
        List of (assertion, refs) tuples compatible with inject_references().
        Assertions that fail to resolve get empty refs lists.
    """
    if not assertions:
        return []

    _ensure_imports()

    if api_key is None:
        api_key = _get_api_key_for_model(model)

    # Load prompt configuration
    prompt_config = _load_prompt("artl_literature_search.prompt.yaml")
    system_prompt = prompt_config["system_prompt"]

    agent = LiteLLMAgent(model=model, api_key=api_key, max_tokens=2000)

    results: list[tuple[AtomicAssertion, list[ReferenceMatch]]] = []

    try:
        with MCPToolSource("uvx artl-mcp") as source:
            for i, assertion in enumerate(assertions):
                print(f"  [{i + 1}/{len(assertions)}] Searching for: {assertion.original_text[:60]}...")

                user_prompt = _build_user_prompt(
                    assertion, max_refs=max_refs_per_assertion
                )

                try:
                    result = agent.query_unified(
                        message=user_prompt,
                        system_message=system_prompt,
                        tools=source.tools,
                        max_turns=max_turns,
                        track_usage=True,
                    )

                    refs = _parse_literature_response(
                        result.text or "",
                        assertion,
                        max_refs=max_refs_per_assertion,
                    )

                    if result.usage and result.usage.estimated_cost_usd:
                        print(f"    Found {len(refs)} ref(s), cost: ${result.usage.estimated_cost_usd:.4f}")
                    else:
                        print(f"    Found {len(refs)} ref(s)")

                    results.append((assertion, refs))

                except Exception as e:
                    print(f"    ⚠ LLM call failed: {e}")
                    results.append((assertion, []))

    except Exception as e:
        print(f"  ⚠ MCP connection failed: {e}")
        # Return all assertions with empty refs
        results = [(a, []) for a in assertions]

    return results


# =============================================================================
# Internal Helpers
# =============================================================================


def _extract_json(text: str) -> dict | None:
    """Extract JSON object from text, handling code fences.

    Args:
        text: Text that may contain JSON, optionally in markdown code fences

    Returns:
        Parsed dict if JSON found, None otherwise
    """
    # Try code fence extraction first
    fence_pattern = r"```(?:json)?\s*\n?(.*?)\n?```"
    fence_match = re.search(fence_pattern, text, re.DOTALL)
    if fence_match:
        try:
            return json.loads(fence_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try to find a bare JSON object
    # Find the first { and try to parse from there
    brace_start = text.find("{")
    if brace_start == -1:
        return None

    # Find matching closing brace
    depth = 0
    for i in range(brace_start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[brace_start : i + 1])
                except json.JSONDecodeError:
                    return None

    return None


def _parse_literature_response(
    response_text: str,
    assertion: AtomicAssertion,
    max_refs: int = 3,
) -> list[ReferenceMatch]:
    """Parse LLM response into ReferenceMatch objects.

    Args:
        response_text: Raw text response from LLM
        assertion: The assertion being resolved (for gene/GO context)
        max_refs: Maximum number of references to return

    Returns:
        List of ReferenceMatch objects with match_type="literature"
    """
    data = _extract_json(response_text)
    if data is None:
        return []

    refs_data = data.get("references_found", [])
    if not refs_data:
        return []

    matches = []
    for ref in refs_data[:max_refs]:
        pmid = ref.get("pmid")
        if not pmid:
            continue

        # Strip common prefixes
        pmid = str(pmid)
        if pmid.upper().startswith("PMID:"):
            pmid = pmid[5:]
        pmid = pmid.strip()

        if not pmid:
            continue

        matches.append(
            ReferenceMatch(
                pmid=pmid,
                genes_covered=assertion.genes,
                go_terms_covered=assertion.go_term_ids,
                match_type="literature",
            )
        )

    return matches


def _build_user_prompt(
    assertion: AtomicAssertion,
    max_refs: int = 3,
) -> str:
    """Build user prompt for literature search.

    Args:
        assertion: The assertion to find references for
        max_refs: Maximum number of references to request

    Returns:
        Formatted user prompt string
    """
    genes = assertion.genes[:5]  # Limit to 5 genes
    genes_str = ", ".join(genes)
    go_terms_str = ", ".join(assertion.go_term_ids)

    prompt_config = _load_prompt("artl_literature_search.prompt.yaml")
    template = prompt_config["user_prompt"]

    return template.format(
        max_refs=max_refs,
        assertion_text=assertion.original_text,
        genes=genes_str,
        go_terms=go_terms_str,
    )


def _get_api_key_for_model(model: str) -> str:
    """Get appropriate API key for model from environment.

    Args:
        model: Model identifier

    Returns:
        API key string

    Raises:
        ValueError: If required API key not found
    """
    if model.startswith("gpt") or model.startswith("o1"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return api_key
    elif model.startswith("claude"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        return api_key
    else:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable."
            )
        return api_key


def _load_prompt(prompt_file: str) -> dict[str, Any]:
    """Load co-located prompt YAML file.

    Args:
        prompt_file: Name of prompt file

    Returns:
        Dictionary with system_prompt, user_prompt, presets

    Raises:
        FileNotFoundError: If prompt file not found
    """
    prompt_path = Path(__file__).parent / prompt_file
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return yaml.safe_load(prompt_path.read_text())


# =============================================================================
# Hub gene abstract fetch (targeted Europe PMC search for cross-theme genes)
# =============================================================================


def fetch_abstracts_for_hub_genes(
    hub_genes: dict[str, Any],
    max_hub_genes: int = 20,
    mcp_command: str = "uvx artl-mcp",
    max_results_per_gene: int = 5,
) -> dict[str, list[dict[str, Any]]]:
    """Fetch paper abstracts for top hub genes via Europe PMC (artl-mcp).

    Selects the top max_hub_genes by theme_count (hub genes appearing in the
    most themes). For each, searches Europe PMC using the gene symbol + its
    top theme name as keywords. Opens a single MCPToolSource session for all
    hub genes.

    Args:
        hub_genes: hub_genes dict from enrichment output
            {gene: {"theme_count": int, "themes": [str, ...]}}
        max_hub_genes: Maximum number of hub genes to search (top by theme_count)
        mcp_command: Command to start the artl-mcp server
        max_results_per_gene: Maximum papers to retrieve per hub gene

    Returns:
        Dict mapping gene symbol to list of paper dicts. Each paper dict has
        keys: pmid, title, abstract, authors, year.
        Hub genes that fail to retrieve papers get empty lists.
    """
    if not hub_genes:
        return {}

    _ensure_imports()

    # Select top hub genes by theme_count
    sorted_genes = sorted(
        hub_genes.items(), key=lambda x: x[1].get("theme_count", 0), reverse=True
    )[:max_hub_genes]

    results: dict[str, list[dict[str, Any]]] = {}

    try:
        with MCPToolSource(mcp_command) as source:
            search_tool = next(
                (t for t in source.tools if t.name == "search_europepmc_papers"),
                None,
            )
            if search_tool is None:
                print("  ⚠ search_europepmc_papers tool not found in artl-mcp")
                return {gene: [] for gene, _ in sorted_genes}

            for gene, data in sorted_genes:
                try:
                    top_theme = data.get("themes", [""])[0] if data.get("themes") else ""
                    query = f"{gene} {top_theme}".strip()
                    print(f"  [{gene}] Fetching: {query[:70]}...")

                    raw = search_tool.handler({
                        "keywords": query,
                        "max_results": max_results_per_gene,
                        "result_type": "core",
                    })

                    papers = _parse_search_results(raw or "")
                    results[gene] = papers
                    print(f"    {len(papers)} paper(s) found")

                except Exception as e:
                    print(f"    ⚠ Failed for gene {gene}: {e}")
                    results[gene] = []

    except Exception as e:
        print(f"  ⚠ MCP session failed: {e}")
        results = {gene: [] for gene, _ in sorted_genes}

    return results


# =============================================================================
# Literature pre-fetch (lit-first pipeline — kept for reference, not called by default)
# =============================================================================


def fetch_abstracts_for_themes(
    themes: list[dict[str, Any]],
    hub_genes: dict[str, Any],
    mcp_command: str = "uvx artl-mcp",
    max_results_per_theme: int = 10,
) -> dict[int, list[dict[str, Any]]]:
    """Fetch paper abstracts for each theme via Europe PMC (artl-mcp).

    Opens a single MCPToolSource session for all themes. For each theme,
    builds a keyword query from the top-ranked genes and anchor GO term name,
    then calls search_europepmc_papers directly (no LLM involved).

    Args:
        themes: List of theme dicts from enrichment output
        hub_genes: hub_genes dict from enrichment output (used for gene ranking)
        mcp_command: Command to start the artl-mcp server
        max_results_per_theme: Maximum papers to retrieve per theme

    Returns:
        Dict mapping theme index to list of paper dicts. Each paper dict has
        keys: pmid, title, abstract, authors, year.
        Themes that fail to retrieve papers get empty lists.
    """
    if not themes:
        return {}

    _ensure_imports()

    results: dict[int, list[dict[str, Any]]] = {}

    try:
        with MCPToolSource(mcp_command) as source:
            search_tool = next(
                (t for t in source.tools if t.name == "search_europepmc_papers"),
                None,
            )
            if search_tool is None:
                print("  ⚠ search_europepmc_papers tool not found in artl-mcp")
                return {i: [] for i in range(len(themes))}

            for i, theme in enumerate(themes):
                try:
                    query = _build_theme_query(theme, hub_genes)
                    print(f"  [{i + 1}/{len(themes)}] Fetching: {query[:70]}...")

                    raw = search_tool.handler({
                        "keywords": query,
                        "max_results": max_results_per_theme,
                        "result_type": "core",
                    })

                    papers = _parse_search_results(raw or "")
                    results[i] = papers
                    print(f"    {len(papers)} paper(s) found")

                except Exception as e:
                    print(f"    ⚠ Failed for theme {i}: {e}")
                    results[i] = []

    except Exception as e:
        print(f"  ⚠ MCP session failed: {e}")
        results = {i: [] for i in range(len(themes))}

    return results


def _build_theme_query(theme: dict[str, Any], hub_genes: dict[str, Any]) -> str:
    """Build keyword search query for a theme.

    Uses the top 3 ranked genes (by theme-specificity score) plus the anchor
    GO term name as the search keywords.

    Args:
        theme: Single theme dict from enrichment output
        hub_genes: hub_genes dict from enrichment output

    Returns:
        Space-separated keyword string for artl-mcp search
    """
    from .go_markdown_explanation_service import rank_genes_for_theme

    ranked = rank_genes_for_theme(theme, hub_genes, top_n=3)
    gene_names = [r["gene"] for r in ranked]
    anchor_name = theme.get("anchor_term", {}).get("name", "")

    parts = gene_names + ([anchor_name] if anchor_name else [])
    return " ".join(parts)


def _parse_search_results(raw: str) -> list[dict[str, Any]]:
    """Parse raw JSON returned by search_europepmc_papers into paper dicts.

    Handles both a bare list and dict-wrapped formats that artl-mcp may return.

    Args:
        raw: Raw string (JSON) from the MCP tool handler

    Returns:
        List of paper dicts with keys: pmid, title, abstract, authors, year.
        Returns empty list if raw is empty or unparseable.
    """
    if not raw:
        return []

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []

    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        # Europe PMC core API wraps results under resultList.result
        items = (
            data.get("resultList", {}).get("result")
            or data.get("results")
            or data.get("papers")
            or []
        )
    else:
        return []

    papers = []
    for item in items:
        if not isinstance(item, dict):
            continue

        pmid = str(item.get("pmid") or item.get("id") or "").strip()
        title = item.get("title", "")
        abstract = item.get("abstractText", item.get("abstract", ""))

        # Extract author surnames (first 3 authors)
        authors_data = item.get("authorList", {})
        if isinstance(authors_data, dict):
            author_list = authors_data.get("author", [])
        elif isinstance(authors_data, list):
            author_list = authors_data
        else:
            author_list = []

        surnames = [
            a.get("lastName", "")
            for a in author_list[:3]
            if isinstance(a, dict) and a.get("lastName")
        ]
        authors = ", ".join(surnames)
        if len(author_list) > 3:
            authors += " et al."

        year = str(item.get("pubYear", "")).strip()

        if pmid and (title or abstract):
            papers.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "year": year,
            })

    return papers


def _parse_paper_by_id_result(raw: str) -> dict[str, Any] | None:
    """Parse raw JSON returned by get_europepmc_paper_by_id into a paper dict.

    Args:
        raw: Raw string (JSON) from the MCP tool handler

    Returns:
        Paper dict with keys: pmid, title, abstract, authors, year.
        Returns None if raw is empty, unparseable, or missing pmid+content.
    """
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    # Response may be wrapped: {"result": {...}} or bare paper dict
    paper = data.get("result", data)
    if not isinstance(paper, dict):
        return None

    pmid = str(paper.get("pmid") or paper.get("id") or "").strip()
    title = paper.get("title", "")
    abstract = paper.get("abstractText", paper.get("abstract", ""))

    authors_data = paper.get("authorList", {})
    if isinstance(authors_data, dict):
        author_list = authors_data.get("author", [])
    elif isinstance(authors_data, list):
        author_list = authors_data
    else:
        author_list = []

    surnames = [
        a.get("lastName", "")
        for a in author_list[:3]
        if isinstance(a, dict) and a.get("lastName")
    ]
    authors = ", ".join(surnames)
    if len(author_list) > 3:
        authors += " et al."

    year = str(paper.get("pubYear", "")).strip()

    if pmid and (title or abstract):
        return {"pmid": pmid, "title": title, "abstract": abstract, "authors": authors, "year": year}
    return None


def fetch_abstracts_for_gaf_pmids(
    gaf_pmids: dict[int, list[dict[str, Any]]],
    mcp_command: str = "uvx artl-mcp",
) -> dict[int, list[dict[str, Any]]]:
    """Fetch paper abstracts for GAF-curated PMIDs via Europe PMC.

    Deduplicates PMIDs across themes (each PMID fetched once via
    get_europepmc_paper_by_id), then maps results back to theme indices.

    Args:
        gaf_pmids: {theme_index: [{pmid, genes_covered}, ...]} from
            get_gaf_pmids_for_themes()
        mcp_command: artl-mcp server command

    Returns:
        {theme_index: [{pmid, title, abstract, authors, year}, ...]}
        Same shape as paper_abstracts from fetch_abstracts_for_themes().
        Only entries where an abstract was successfully fetched are included.
    """
    if not gaf_pmids:
        return {}

    _ensure_imports()

    # Collect unique PMIDs across all themes
    pmid_to_themes: dict[str, list[int]] = {}
    for theme_idx, entries in gaf_pmids.items():
        for entry in entries:
            pmid = entry.get("pmid", "")
            if pmid:
                pmid_to_themes.setdefault(pmid, []).append(theme_idx)

    unique_pmids = list(pmid_to_themes)
    if not unique_pmids:
        return {i: [] for i in gaf_pmids}

    pmid_to_paper: dict[str, dict[str, Any]] = {}
    try:
        with MCPToolSource(mcp_command) as source:
            fetch_tool = next(
                (t for t in source.tools if t.name == "get_europepmc_paper_by_id"),
                None,
            )
            if fetch_tool is None:
                print("  ⚠ get_europepmc_paper_by_id not found in artl-mcp")
                return {i: [] for i in gaf_pmids}

            print(f"  Fetching {len(unique_pmids)} unique GAF PMIDs from Europe PMC...")
            for pmid in unique_pmids:
                try:
                    raw = fetch_tool.handler({"identifier": pmid})
                    paper = _parse_paper_by_id_result(raw or "")
                    if paper:
                        pmid_to_paper[pmid] = paper
                except Exception as e:
                    print(f"    ⚠ Failed for PMID {pmid}: {e}")

    except Exception as e:
        print(f"  ⚠ MCP session failed: {e}")
        return {i: [] for i in gaf_pmids}

    print(f"  ✓ Fetched {len(pmid_to_paper)}/{len(unique_pmids)} GAF PMID abstracts")

    # Map back to theme indices preserving entry order
    results: dict[int, list[dict[str, Any]]] = {}
    for theme_idx, entries in gaf_pmids.items():
        results[theme_idx] = [
            pmid_to_paper[e["pmid"]]
            for e in entries
            if e.get("pmid") in pmid_to_paper
        ]
    return results
