"""
Exploration 11: artl-mcp literature search via cellsem-llm-client

Minimal test: can an LLM agent use artl-mcp tools (via MCPToolSource)
to find literature references for unresolved assertions from the
reference retrieval pipeline?

Tests:
1. MCPToolSource connects to artl-mcp via stdio
2. LLM agent can call search_europepmc_papers tool
3. LLM agent can call get_europepmc_paper_by_id for validation
4. End-to-end: give agent an assertion, get back supporting PMIDs

Usage:
    uv run python exploration/11_artl_mcp_via_llm.py
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _get_model_and_key() -> tuple[str, str | None]:
    """Pick a cheap model and its API key from environment."""
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if openai_key:
        return "gpt-4o-mini", openai_key
    elif anthropic_key:
        return "claude-haiku-4-5-20251001", anthropic_key
    return "gpt-4o-mini", None


# ---------------------------------------------------------------------------
# Step 1: Verify MCPToolSource can discover artl-mcp tools
# ---------------------------------------------------------------------------


def test_mcp_connection():
    """Verify MCPToolSource connects and discovers artl-mcp tools."""
    from cellsem_llm_client import MCPToolSource

    print("=" * 70)
    print("Step 1: MCPToolSource connection to artl-mcp")
    print("=" * 70)

    with MCPToolSource("uvx artl-mcp") as source:
        tools = source.tools
        print(f"\nDiscovered {len(tools)} tools:")
        for t in tools:
            print(f"  - {t.name}")

        # Verify expected tools are present
        tool_names = {t.name for t in tools}
        expected = {"search_europepmc_papers", "get_europepmc_paper_by_id"}
        missing = expected - tool_names
        if missing:
            print(f"\nERROR: Missing expected tools: {missing}")
            return False

        print("\nAll expected tools found.")
        return True


# ---------------------------------------------------------------------------
# Step 2: Direct tool call — search without LLM
# ---------------------------------------------------------------------------


def test_direct_tool_call():
    """Call artl-mcp search tool directly (no LLM) to verify it works."""
    from cellsem_llm_client import MCPToolSource

    print("\n" + "=" * 70)
    print("Step 2: Direct tool call — search_europepmc_papers")
    print("=" * 70)

    with MCPToolSource("uvx artl-mcp") as source:
        search_tool = next(t for t in source.tools if t.name == "search_europepmc_papers")

        # Search for a well-known topic
        result = search_tool.handler({
            "keywords": "BRCA1 BRCA2 DNA repair homologous recombination",
            "max_results": 3,
        })

        print(f"\nSearch result (first 1000 chars):\n{result[:1000]}")
        return result is not None


# ---------------------------------------------------------------------------
# Step 3: LLM agent with artl-mcp tools — single assertion
# ---------------------------------------------------------------------------


def test_llm_with_artl_mcp():
    """LLM agent uses artl-mcp tools to find references for an assertion."""
    from cellsem_llm_client import LiteLLMAgent, MCPToolSource

    print("\n" + "=" * 70)
    print("Step 3: LLM agent with artl-mcp tools")
    print("=" * 70)

    # Pick a simple assertion to test with
    test_assertion = {
        "assertion": "ATM and BRCA1 cooperate in DNA damage response, "
                     "with ATM phosphorylating BRCA1 to activate homologous recombination repair.",
        "genes": ["ATM", "BRCA1"],
        "complexity": "multi_gene",
    }

    print(f"\nTest assertion: {test_assertion['assertion'][:80]}...")
    print(f"Genes: {test_assertion['genes']}")

    # Check for API key
    model, api_key = _get_model_and_key()
    if not api_key:
        print("\nSKIPPED: No OPENAI_API_KEY or ANTHROPIC_API_KEY set")
        return None

    agent = LiteLLMAgent(model=model, api_key=api_key, max_tokens=2000)

    system_prompt = """\
You are a scientific literature search assistant. Your task is to find
PubMed references that support a specific biological assertion.

Strategy:
1. Use search_europepmc_papers to find candidate papers
2. Use get_europepmc_paper_by_id to check promising results
3. Return a JSON object with your findings

Output format (JSON):
{
    "assertion": "the original assertion",
    "references_found": [
        {
            "pmid": "12345678",
            "title": "Paper title",
            "relevance": "Brief explanation of how this paper supports the assertion"
        }
    ],
    "search_queries_used": ["query1", "query2"],
    "confidence": "high|medium|low"
}
"""

    user_prompt = f"""\
Find 1-3 PubMed references supporting this assertion:

"{test_assertion['assertion']}"

Key genes: {', '.join(test_assertion['genes'])}

Search Europe PMC, check the most promising results, and return your findings as JSON.
Limit yourself to 2-3 tool calls to keep costs down.
"""

    with MCPToolSource("uvx artl-mcp") as source:
        print(f"\nUsing model: {model}")
        print(f"Tools available: {[t.name for t in source.tools]}")
        print("\nRunning agent...")

        result = agent.query_unified(
            message=user_prompt,
            system_message=system_prompt,
            tools=source.tools,
            max_turns=5,
            track_usage=True,
        )

        print(f"\n--- Agent Response ---")
        print(result.text[:2000])

        if result.usage:
            print(f"\n--- Usage ---")
            print(f"  Input tokens: {result.usage.input_tokens}")
            print(f"  Output tokens: {result.usage.output_tokens}")
            if hasattr(result.usage, "estimated_cost_usd"):
                print(f"  Est. cost: ${result.usage.estimated_cost_usd:.4f}")

        return result.text


# ---------------------------------------------------------------------------
# Step 4: Batch test with real artl_queries.json
# ---------------------------------------------------------------------------


def test_batch_from_queries_file():
    """Process first 2 assertions from an existing artl_queries.json file."""
    from cellsem_llm_client import LiteLLMAgent, MCPToolSource

    print("\n" + "=" * 70)
    print("Step 4: Batch test from artl_queries.json (first 2 only)")
    print("=" * 70)

    # Find an existing queries file
    queries_file = Path("results/ref_test_artl_queries.json")
    if not queries_file.exists():
        # Try alternative location
        queries_file = Path("results/reference_retrieval/checkpoint_step8_artl_queries.json")
    if not queries_file.exists():
        print("\nSKIPPED: No artl_queries.json file found")
        return None

    with open(queries_file) as f:
        queries = json.load(f)

    print(f"\nLoaded {len(queries)} assertions from {queries_file.name}")
    print(f"Processing first 2 only (cost control)...")

    model, api_key = _get_model_and_key()
    if not api_key:
        print("\nSKIPPED: No API key set")
        return None

    agent = LiteLLMAgent(model=model, api_key=api_key, max_tokens=2000)

    system_prompt = """\
You are a scientific literature search assistant. Find PubMed references
supporting a biological assertion using the Europe PMC search tools.

Strategy:
1. Search Europe PMC with focused gene + process keywords
2. Check 1-2 promising results for relevance
3. Return findings as JSON

Output JSON format:
{
    "assertion": "original text",
    "references": [{"pmid": "...", "title": "...", "relevance": "..."}],
    "confidence": "high|medium|low"
}

Keep tool calls minimal (2-3 max). Prefer reviews over primary articles.
"""

    results = []

    with MCPToolSource("uvx artl-mcp") as source:
        for i, query in enumerate(queries[:2]):
            print(f"\n--- Assertion {i+1}/2 ---")
            assertion = query["assertion"]
            genes = query.get("genes", [])
            print(f"Genes: {genes}")
            print(f"Text: {assertion[:80]}...")

            user_prompt = f"""\
Find 1-2 PubMed references for:
"{assertion}"
Key genes: {', '.join(genes[:3])}
"""
            result = agent.query_unified(
                message=user_prompt,
                system_message=system_prompt,
                tools=source.tools,
                max_turns=8,
                track_usage=True,
            )

            print(f"Response: {result.text[:500]}")
            if result.usage:
                print(f"Cost: ${result.usage.estimated_cost_usd:.4f}")

            results.append({
                "query": query,
                "response": result.text,
            })

    # Save results
    output_path = Path("results/exploration_11_artl_test.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")

    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    print("Exploration 11: artl-mcp via cellsem-llm-client\n")

    # Step 1: Connection test (no LLM, no API key needed)
    if not test_mcp_connection():
        print("\nFAILED: Cannot connect to artl-mcp")
        sys.exit(1)

    # Step 2: Direct tool call (no LLM, no API key needed)
    if not test_direct_tool_call():
        print("\nFAILED: Direct tool call failed")
        sys.exit(1)

    # Step 3: LLM + tools (needs API key)
    result = test_llm_with_artl_mcp()
    if result is None:
        print("\nSteps 3-4 skipped (no API key). Steps 1-2 passed.")
        sys.exit(0)

    # Step 4: Batch from real queries
    test_batch_from_queries_file()

    print("\n" + "=" * 70)
    print("All steps complete!")
    print("=" * 70)