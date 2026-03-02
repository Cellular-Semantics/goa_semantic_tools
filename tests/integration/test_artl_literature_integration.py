"""
Integration tests for artl-mcp Literature Search Service.

Requires:
- OPENAI_API_KEY or ANTHROPIC_API_KEY in environment
- artl-mcp available via uvx (npm package)

These tests make real API calls and cost ~$0.003-0.006 per assertion.
"""
from __future__ import annotations

import os

import pytest

from goa_semantic_tools.services.reference_retrieval_service import AtomicAssertion


@pytest.mark.integration
def test_real_assertion_resolution():
    """Test resolving a well-known assertion via real artl-mcp + real LLM.

    Uses ATM + BRCA1 DNA damage response as a well-studied topic
    that should reliably return PubMed references.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.fail("OPENAI_API_KEY or ANTHROPIC_API_KEY required for integration tests")

    from goa_semantic_tools.services.artl_literature_service import (
        resolve_assertions_via_literature,
    )

    assertion = AtomicAssertion(
        claim_type="EXTERNAL",
        original_text=(
            "ATM and BRCA1 cooperate in DNA damage response, "
            "with ATM phosphorylating BRCA1 to activate homologous recombination repair."
        ),
        genes=["ATM", "BRCA1"],
        go_term_ids=["GO:0006974"],  # DNA damage response
        is_multi_gene=True,
        is_multi_process=False,
    )

    # Determine model based on available key
    model = "gpt-4o-mini" if os.getenv("OPENAI_API_KEY") else "claude-haiku-4-5-20251001"

    results = resolve_assertions_via_literature(
        [assertion],
        model=model,
        max_refs_per_assertion=3,
    )

    assert len(results) == 1
    resolved_assertion, refs = results[0]

    # Should find at least 1 reference for this well-known topic
    assert len(refs) >= 1, f"Expected >=1 reference for ATM+BRCA1 DDR, got {len(refs)}"

    # Validate reference structure
    for ref in refs:
        assert ref.pmid, "PMID should not be empty"
        assert ref.pmid.isdigit(), f"PMID should be numeric, got: {ref.pmid}"
        assert ref.match_type == "literature"
        assert ref.genes_covered == ["ATM", "BRCA1"]
