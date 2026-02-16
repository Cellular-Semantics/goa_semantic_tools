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
