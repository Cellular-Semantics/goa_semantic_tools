"""
Unit tests for Reference Retrieval Service.

Tests claim extraction, reference lookup, and reference injection.
"""
from __future__ import annotations

import pytest

from goa_semantic_tools.services.reference_retrieval_service import (
    AtomicAssertion,
    ReferenceMatch,
    extract_claims,
    extract_genes_from_text,
    find_references_for_assertion,
    format_references_needing_artl_mcp,
    inject_references,
    inject_references_inline,
)


# =============================================================================
# Test AtomicAssertion Dataclass
# =============================================================================


@pytest.mark.unit
class TestAtomicAssertion:
    """Tests for AtomicAssertion dataclass."""

    def test_simple_complexity(self):
        """Test simple complexity (1 gene, 1 process)."""
        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="TP53 is involved in apoptosis",
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )

        assert assertion.complexity == "simple"

    def test_multi_gene_complexity(self):
        """Test multi_gene complexity (N genes, 1 process)."""
        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="TP53 and BRCA1 cooperate in DNA damage response",
            genes=["TP53", "BRCA1"],
            go_term_ids=["GO:0006974"],
            is_multi_gene=True,
            is_multi_process=False,
        )

        assert assertion.complexity == "multi_gene"

    def test_multi_process_complexity(self):
        """Test multi_process complexity (1 gene, N processes)."""
        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="TP53 links apoptosis to cell cycle arrest",
            genes=["TP53"],
            go_term_ids=["GO:0006915", "GO:0007050"],
            is_multi_gene=False,
            is_multi_process=True,
        )

        assert assertion.complexity == "multi_process"

    def test_complex_complexity(self):
        """Test complex complexity (N genes AND N processes)."""
        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="TP53 and BRCA1 coordinate apoptosis and DNA repair",
            genes=["TP53", "BRCA1"],
            go_term_ids=["GO:0006915", "GO:0006281"],
            is_multi_gene=True,
            is_multi_process=True,
        )

        assert assertion.complexity == "complex"


# =============================================================================
# Test ReferenceMatch Dataclass
# =============================================================================


@pytest.mark.unit
class TestReferenceMatch:
    """Tests for ReferenceMatch dataclass."""

    def test_creation(self):
        """Test ReferenceMatch creation."""
        match = ReferenceMatch(
            pmid="12345678",
            genes_covered=["TP53", "BRCA1"],
            go_terms_covered=["GO:0006915"],
            match_type="multi_gene",
        )

        assert match.pmid == "12345678"
        assert match.genes_covered == ["TP53", "BRCA1"]
        assert match.match_type == "multi_gene"


# =============================================================================
# Test extract_claims Function
# =============================================================================


@pytest.mark.unit
class TestExtractClaims:
    """Tests for extract_claims function."""

    def test_single_tag(self):
        """Test extraction with single tag."""
        text = "[DATA] The gene set shows 5x enrichment for inflammatory response."

        claims = extract_claims(text)

        assert len(claims["DATA"]) == 1
        assert "5x enrichment" in claims["DATA"][0]

    def test_multiple_tags(self):
        """Test extraction with multiple different tags."""
        text = """
        [DATA] The gene set contains 50 genes.
        [INFERENCE] This suggests inflammatory signaling.
        [EXTERNAL] IL1B is known to activate NF-kB.
        """

        claims = extract_claims(text)

        assert len(claims["DATA"]) == 1
        assert len(claims["INFERENCE"]) == 1
        assert len(claims["EXTERNAL"]) == 1
        assert "50 genes" in claims["DATA"][0]
        assert "inflammatory" in claims["INFERENCE"][0]
        assert "IL1B" in claims["EXTERNAL"][0]

    def test_multiple_same_tag(self):
        """Test extraction with multiple claims of same tag."""
        text = """
        [INFERENCE] First inference claim.
        [DATA] Some data.
        [INFERENCE] Second inference claim.
        """

        claims = extract_claims(text)

        assert len(claims["INFERENCE"]) == 2
        assert "First" in claims["INFERENCE"][0]
        assert "Second" in claims["INFERENCE"][1]

    def test_go_hierarchy_tag(self):
        """Test extraction of GO-HIERARCHY tag."""
        text = "[GO-HIERARCHY] Apoptosis is a child of cell death."

        claims = extract_claims(text)

        assert len(claims["GO-HIERARCHY"]) == 1
        assert "Apoptosis" in claims["GO-HIERARCHY"][0]

    def test_empty_text(self):
        """Test with empty text."""
        claims = extract_claims("")

        assert claims["DATA"] == []
        assert claims["INFERENCE"] == []
        assert claims["EXTERNAL"] == []

    def test_no_tags(self):
        """Test text with no tags."""
        text = "This is just regular text without any tags."

        claims = extract_claims(text)

        assert all(len(v) == 0 for v in claims.values())


# =============================================================================
# Test extract_genes_from_text Function
# =============================================================================


@pytest.mark.unit
class TestExtractGenesFromText:
    """Tests for extract_genes_from_text function."""

    def test_simple_extraction(self):
        """Test extracting gene symbols from text."""
        text = "The interaction between TP53 and BRCA1 affects DNA repair."

        genes = extract_genes_from_text(text)

        assert "TP53" in genes
        assert "BRCA1" in genes
        assert "DNA" not in genes  # Common word filtered

    def test_with_known_genes(self):
        """Test filtering to known genes."""
        text = "TP53, BRCA1, UNKNOWN, and ATM are involved."
        known = {"TP53", "BRCA1", "ATM"}

        genes = extract_genes_from_text(text, known_genes=known)

        assert set(genes) == {"TP53", "BRCA1", "ATM"}

    def test_gene_with_numbers(self):
        """Test extracting genes with numbers."""
        text = "IL1B and IL6 are cytokines."

        genes = extract_genes_from_text(text)

        assert "IL1B" in genes
        assert "IL6" in genes

    def test_stopword_filtering(self):
        """Test that common stopwords are filtered."""
        text = "THE GENE IS IN THE DNA AND RNA COMPLEX"

        genes = extract_genes_from_text(text)

        assert "THE" not in genes
        assert "AND" not in genes
        assert "DNA" not in genes
        assert "RNA" not in genes


# =============================================================================
# Test find_references_for_assertion Function
# =============================================================================


@pytest.mark.unit
class TestFindReferencesForAssertion:
    """Tests for find_references_for_assertion function."""

    def test_simple_reference_lookup(self):
        """Test simple reference lookup (1 gene, 1 process)."""
        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="TP53 is involved in apoptosis",
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )

        ref_index = {
            "gene_go_pmids": {
                "TP53": {
                    "GO:0006915": {"12345678", "23456789"},
                },
            },
        }

        descendants_closure = {"GO:0006915": set()}

        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure, max_refs=3
        )

        assert len(refs) >= 1
        assert any(r.pmid in {"12345678", "23456789"} for r in refs)
        assert all(r.match_type in {"exact", "descendant"} for r in refs)

    def test_multi_gene_reference_lookup(self):
        """Test multi-gene reference lookup."""
        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="TP53 and BRCA1 cooperate",
            genes=["TP53", "BRCA1"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=True,
            is_multi_process=False,
        )

        ref_index = {
            "gene_go_pmids": {
                "TP53": {"GO:0006915": {"12345678"}},
                "BRCA1": {"GO:0006915": {"12345678"}},  # Same PMID
            },
        }

        descendants_closure = {"GO:0006915": set()}

        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure, max_refs=3
        )

        assert len(refs) >= 1
        assert refs[0].pmid == "12345678"
        assert set(refs[0].genes_covered) == {"TP53", "BRCA1"}
        assert refs[0].match_type == "multi_gene"

    def test_complex_returns_empty(self):
        """Test that complex assertions return empty list."""
        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="Complex claim",
            genes=["TP53", "BRCA1"],
            go_term_ids=["GO:0006915", "GO:0006281"],
            is_multi_gene=True,
            is_multi_process=True,
        )

        ref_index = {"gene_go_pmids": {"TP53": {"GO:0006915": {"12345678"}}}}
        descendants_closure = {}

        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure
        )

        assert refs == []

    def test_descendant_matching(self):
        """Test that descendants are included in lookup."""
        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="TP53 in apoptosis",
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )

        ref_index = {
            "gene_go_pmids": {
                "TP53": {
                    "GO:0097193": {"12345678"},  # Descendant of GO:0006915
                },
            },
        }

        descendants_closure = {"GO:0006915": {"GO:0097193", "GO:0097194"}}

        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure
        )

        assert len(refs) >= 1
        assert refs[0].pmid == "12345678"
        assert refs[0].match_type == "descendant"

    def test_no_references_found(self):
        """Test when no references are found."""
        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="Unknown gene in apoptosis",
            genes=["UNKNOWN"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )

        ref_index = {"gene_go_pmids": {}}
        descendants_closure = {}

        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure
        )

        assert refs == []

    def test_multi_process_reference_lookup(self):
        """Test multi-process reference lookup (1 gene, N processes)."""
        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="TP53 links apoptosis to DNA repair",
            genes=["TP53"],
            go_term_ids=["GO:0006915", "GO:0006281"],
            is_multi_gene=False,
            is_multi_process=True,
        )

        ref_index = {
            "gene_go_pmids": {
                "TP53": {
                    "GO:0006915": {"12345678", "99999999"},
                    "GO:0006281": {"12345678"},  # Same PMID covers both
                },
            },
        }

        descendants_closure = {"GO:0006915": set(), "GO:0006281": set()}

        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure, max_refs=3
        )

        assert len(refs) >= 1
        # The PMID covering both processes should be ranked first
        assert refs[0].pmid == "12345678"
        assert "multi_process" in refs[0].match_type

    def test_multi_process_with_empty_genes(self):
        """Test multi-process with empty genes list."""
        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="Some process",
            genes=[],
            go_term_ids=["GO:0006915", "GO:0006281"],
            is_multi_gene=False,
            is_multi_process=True,
        )

        ref_index = {"gene_go_pmids": {}}
        descendants_closure = {}

        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure
        )

        assert refs == []

    def test_multi_process_gene_not_found(self):
        """Test multi-process when gene not in index."""
        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="Unknown gene in multiple processes",
            genes=["UNKNOWN"],
            go_term_ids=["GO:0006915", "GO:0006281"],
            is_multi_gene=False,
            is_multi_process=True,
        )

        ref_index = {
            "gene_go_pmids": {
                "TP53": {"GO:0006915": {"12345678"}},
            },
        }
        descendants_closure = {}

        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure
        )

        assert refs == []


# =============================================================================
# Test inject_references Function
# =============================================================================


@pytest.mark.unit
class TestInjectReferences:
    """Tests for inject_references function."""

    def test_basic_injection(self):
        """Test basic reference injection."""
        summary = "This is the summary text."

        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="TP53 is involved in apoptosis",
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )

        refs = [
            ReferenceMatch(
                pmid="12345678",
                genes_covered=["TP53"],
                go_terms_covered=["GO:0006915"],
                match_type="exact",
            ),
        ]

        result = inject_references(summary, [(assertion, refs)])

        assert "This is the summary text." in result
        assert "Supporting References" in result
        assert "PMID:12345678" in result
        assert "pubmed.ncbi.nlm.nih.gov/12345678" in result

    def test_no_references(self):
        """Test injection with no references."""
        summary = "This is the summary text."

        result = inject_references(summary, [])

        assert result == summary

    def test_empty_refs_list(self):
        """Test when assertions have empty reference lists."""
        summary = "This is the summary text."

        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="Some claim",
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )

        result = inject_references(summary, [(assertion, [])])

        # No references section should be added
        assert result == summary

    def test_truncates_long_claims(self):
        """Test that long claims are truncated in output."""
        summary = "Summary."

        long_claim = "A" * 150  # 150 character claim

        assertion = AtomicAssertion(
            claim_type="INFERENCE",
            original_text=long_claim,
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )

        refs = [
            ReferenceMatch(
                pmid="12345678",
                genes_covered=["TP53"],
                go_terms_covered=["GO:0006915"],
                match_type="exact",
            ),
        ]

        result = inject_references(summary, [(assertion, refs)])

        # Should be truncated with ellipsis
        assert "..." in result
        # Full claim should not appear
        assert long_claim not in result


# =============================================================================
# Test format_references_needing_artl_mcp Function
# =============================================================================


@pytest.mark.unit
class TestFormatReferencesNeedingArtlMcp:
    """Tests for format_references_needing_artl_mcp function."""

    def test_basic_formatting(self):
        """Test basic formatting of artl-mcp queries."""
        assertions = [
            AtomicAssertion(
                claim_type="EXTERNAL",
                original_text="TP53 and BRCA1 coordinate multiple processes",
                genes=["TP53", "BRCA1"],
                go_term_ids=["GO:0006915", "GO:0006281"],
                is_multi_gene=True,
                is_multi_process=True,
            ),
        ]

        queries = format_references_needing_artl_mcp(assertions)

        assert len(queries) == 1
        assert "TP53" in queries[0]["suggested_query"]
        assert "BRCA1" in queries[0]["suggested_query"]
        assert queries[0]["complexity"] == "complex"

    def test_limits_genes_in_query(self):
        """Test that query limits genes to 3."""
        assertions = [
            AtomicAssertion(
                claim_type="EXTERNAL",
                original_text="Many genes involved",
                genes=["GENE1", "GENE2", "GENE3", "GENE4", "GENE5"],
                go_term_ids=["GO:0006915"],
                is_multi_gene=True,
                is_multi_process=True,
            ),
        ]

        queries = format_references_needing_artl_mcp(assertions)

        # Only first 3 genes in query
        query = queries[0]["suggested_query"]
        assert "GENE1" in query
        assert "GENE2" in query
        assert "GENE3" in query
        # But all genes in the genes list
        assert len(queries[0]["genes"]) == 5


# =============================================================================
# Test inject_references_inline Function
# =============================================================================


def _make_ref(pmid: str, genes: list[str]) -> tuple[AtomicAssertion, list[ReferenceMatch]]:
    """Helper: build a (AtomicAssertion, [ReferenceMatch]) tuple."""
    assertion = AtomicAssertion(
        claim_type="EXTERNAL",
        original_text=f"{genes[0]} is involved in a biological process.",
        genes=genes,
        go_term_ids=["GO:0006915"],
        is_multi_gene=False,
        is_multi_process=False,
    )
    ref = ReferenceMatch(
        pmid=pmid,
        genes_covered=genes,
        go_terms_covered=["GO:0006915"],
        match_type="exact",
    )
    return assertion, [ref]


@pytest.mark.unit
class TestInjectReferencesInline:
    """Tests for inject_references_inline function."""

    def test_replaces_marker_with_pmid_link(self):
        """[REF:GENE] marker is replaced by an inline PMID hyperlink."""
        text = "**TP53**: Important tumour suppressor. [REF:TP53]"
        assertion, refs = _make_ref("12345678", ["TP53"])

        result = inject_references_inline(text, [(assertion, refs)])

        assert "[REF:TP53]" not in result
        assert "PMID:12345678" in result
        assert "pubmed.ncbi.nlm.nih.gov/12345678" in result

    def test_removes_marker_when_no_pmids_for_gene(self):
        """If no PMIDs are found for a gene, the [REF:GENE] marker is silently removed."""
        text = "**UNKNOWN**: Some gene. [REF:UNKNOWN]"

        result = inject_references_inline(text, [])

        assert "[REF:UNKNOWN]" not in result
        # Original description text should still be present
        assert "Some gene." in result

    def test_caps_at_three_pmids(self):
        """At most 3 PMIDs are injected for any single gene marker."""
        text = "**TP53**: Important gene. [REF:TP53]"

        assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="TP53 in apoptosis",
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )
        refs = [
            ReferenceMatch(pmid=str(i), genes_covered=["TP53"], go_terms_covered=["GO:0006915"], match_type="exact")
            for i in range(1, 6)  # 5 PMIDs
        ]

        result = inject_references_inline(text, [(assertion, refs)])

        # Count how many PMID: occurrences appear
        pmid_count = result.count("PMID:")
        assert pmid_count <= 3

    def test_empty_assertion_refs_removes_all_markers(self):
        """With empty assertion_refs, all [REF:*] markers are stripped."""
        text = "**BRCA1**: [REF:BRCA1] **IL6**: Something else. [REF:IL6]"

        result = inject_references_inline(text, [])

        assert "[REF:" not in result
        assert "BRCA1" in result
        assert "IL6" in result

    def test_multiple_genes_each_get_own_pmids(self):
        """Two different [REF:GENE] markers each resolve to their own PMIDs."""
        text = "**TP53**: desc1. [REF:TP53] **BRCA1**: desc2. [REF:BRCA1]"

        _, tp53_refs = _make_ref("11111111", ["TP53"])
        _, brca1_refs = _make_ref("22222222", ["BRCA1"])

        tp53_assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="TP53 in apoptosis",
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )
        brca1_assertion = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="BRCA1 in DNA repair",
            genes=["BRCA1"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )

        result = inject_references_inline(
            text, [(tp53_assertion, tp53_refs), (brca1_assertion, brca1_refs)]
        )

        assert "PMID:11111111" in result
        assert "PMID:22222222" in result
        assert "[REF:" not in result

    def test_deduplicates_pmids_for_same_gene(self):
        """If the same PMID appears in multiple assertions for the same gene, it appears once."""
        text = "**TP53**: desc. [REF:TP53]"

        assertion1 = AtomicAssertion(
            claim_type="EXTERNAL",
            original_text="TP53 in apoptosis",
            genes=["TP53"],
            go_term_ids=["GO:0006915"],
            is_multi_gene=False,
            is_multi_process=False,
        )
        assertion2 = AtomicAssertion(
            claim_type="INFERENCE",
            original_text="TP53 in cell cycle",
            genes=["TP53"],
            go_term_ids=["GO:0007050"],
            is_multi_gene=False,
            is_multi_process=False,
        )
        dup_ref = ReferenceMatch(
            pmid="99999999",
            genes_covered=["TP53"],
            go_terms_covered=["GO:0006915"],
            match_type="exact",
        )

        result = inject_references_inline(text, [(assertion1, [dup_ref]), (assertion2, [dup_ref])])

        # PMID should appear exactly once
        assert result.count("PMID:99999999") == 1
