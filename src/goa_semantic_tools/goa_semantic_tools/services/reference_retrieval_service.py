"""
Reference Retrieval Service

Extracts claims from provenance-labeled summaries and retrieves
supporting literature references via programmatic lookup and artl-mcp.
"""
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class AtomicAssertion:
    """An atomic assertion extracted from an [INFERENCE] or [EXTERNAL] claim."""

    claim_type: str  # "INFERENCE" or "EXTERNAL"
    original_text: str
    genes: list[str]
    go_term_ids: list[str]  # Mapped GO term IDs
    is_multi_gene: bool
    is_multi_process: bool

    @property
    def complexity(self) -> str:
        """
        Determine complexity level for reference lookup.

        Returns:
            "complex": Needs artl-mcp (multi-gene AND multi-process)
            "multi_gene": Need PMID annotating all genes to same process
            "multi_process": Need PMID annotating gene to multiple processes
            "simple": Single gene, single process
        """
        if self.is_multi_gene and self.is_multi_process:
            return "complex"
        elif self.is_multi_gene:
            return "multi_gene"
        elif self.is_multi_process:
            return "multi_process"
        else:
            return "simple"


@dataclass
class ReferenceMatch:
    """A matched reference for an assertion."""

    pmid: str
    genes_covered: list[str]
    go_terms_covered: list[str]
    match_type: str  # "exact", "descendant", "multi_gene", "multi_process", "partial"


# =============================================================================
# Claim Extraction
# =============================================================================


# Valid provenance tags
PROVENANCE_TAGS = {"DATA", "INFERENCE", "EXTERNAL", "GO-HIERARCHY"}


def extract_claims(summary_text: str) -> dict[str, list[str]]:
    """
    Extract provenance-labeled claims from summary text.

    Parses text for [TAG] markers and extracts the associated claims.

    Args:
        summary_text: Text with provenance tags like [INFERENCE], [EXTERNAL], etc.

    Returns:
        Dictionary mapping tag to list of claims:
        {'INFERENCE': [claim1, claim2, ...], 'EXTERNAL': [claim1, ...]}

    Example:
        >>> text = "[DATA] The gene set shows 5x enrichment. [INFERENCE] This suggests..."
        >>> claims = extract_claims(text)
        >>> print(claims['INFERENCE'])
    """
    claims: dict[str, list[str]] = {tag: [] for tag in PROVENANCE_TAGS}

    # Pattern: [TAG] text until next [TAG] or end
    pattern = r"\[(DATA|INFERENCE|EXTERNAL|GO-HIERARCHY)\]"

    parts = re.split(pattern, summary_text)

    current_tag = None
    for part in parts:
        part = part.strip()
        if part in claims:
            current_tag = part
        elif current_tag and part:
            # Clean up the claim text
            claim = part.strip()
            if claim:
                claims[current_tag].append(claim)

    return claims


def extract_genes_from_text(text: str, known_genes: set[str] | None = None) -> list[str]:
    """
    Extract gene symbols from text.

    Uses a simple heuristic: uppercase words of 2-8 characters that look like
    gene symbols. If known_genes is provided, filters to only those.

    Args:
        text: Text to extract genes from
        known_genes: Optional set of known gene symbols to filter to

    Returns:
        List of extracted gene symbols
    """
    # Simple pattern for gene symbols (uppercase, 2-8 chars, may have numbers)
    pattern = r"\b([A-Z][A-Z0-9]{1,7})\b"
    candidates = re.findall(pattern, text)

    if known_genes:
        return [g for g in candidates if g in known_genes]

    # Filter out common non-gene words
    stopwords = {
        "THE", "AND", "FOR", "WITH", "THIS", "THAT", "FROM", "INTO",
        "THROUGH", "DURING", "BETWEEN", "UNDER", "ABOVE", "DNA", "RNA",
        "ATP", "GTP", "FDR", "LPS", "NF", "IL",
    }
    return [g for g in candidates if g not in stopwords and len(g) >= 2]


# =============================================================================
# Reference Lookup
# =============================================================================


def find_references_for_assertion(
    assertion: AtomicAssertion,
    ref_index: dict[str, Any],
    descendants_closure: dict[str, set[str]],
    max_refs: int = 3,
) -> list[ReferenceMatch]:
    """
    Find PMIDs that support an atomic assertion.

    Strategy by complexity:
    - Simple (1 gene, 1 process): Find PMIDs annotating gene to process or descendants
    - Multi-gene (N genes, 1 process): Find PMIDs annotating ALL genes to same process
    - Multi-process (1 gene, N processes): Find PMIDs annotating gene to multiple processes
    - Complex: Return empty, flag for artl-mcp

    Args:
        assertion: The assertion to find references for
        ref_index: Reference index from load_gaf_with_pmids
        descendants_closure: Pre-computed descendant closure
        max_refs: Maximum number of references to return

    Returns:
        List of ReferenceMatch objects, sorted by relevance
    """
    if assertion.complexity == "complex":
        return []  # Needs artl-mcp

    gene_go_pmids = ref_index.get("gene_go_pmids", {})

    # Expand GO terms to include descendants
    expanded_go_ids = set(assertion.go_term_ids)
    for go_id in assertion.go_term_ids:
        if go_id in descendants_closure:
            expanded_go_ids.update(descendants_closure[go_id])

    matches: list[ReferenceMatch] = []

    if assertion.complexity == "simple":
        matches = _find_simple_references(
            assertion, gene_go_pmids, expanded_go_ids, max_refs
        )
    elif assertion.complexity == "multi_gene":
        matches = _find_multi_gene_references(
            assertion, gene_go_pmids, expanded_go_ids, max_refs
        )
    elif assertion.complexity == "multi_process":
        matches = _find_multi_process_references(
            assertion, gene_go_pmids, descendants_closure, max_refs
        )

    return matches


def _find_simple_references(
    assertion: AtomicAssertion,
    gene_go_pmids: dict[str, dict[str, set[str]]],
    expanded_go_ids: set[str],
    max_refs: int,
) -> list[ReferenceMatch]:
    """Find references for simple assertions (1 gene, 1 process)."""
    if not assertion.genes:
        return []

    gene = assertion.genes[0]
    if gene not in gene_go_pmids:
        return []

    gene_annotations = gene_go_pmids[gene]
    candidate_pmids: set[str] = set()

    for go_id in expanded_go_ids:
        if go_id in gene_annotations:
            candidate_pmids.update(gene_annotations[go_id])

    if not candidate_pmids:
        return []

    # Rank by recency (higher PMID = newer, roughly)
    ranked = sorted(candidate_pmids, key=lambda x: int(x), reverse=True)

    matches = []
    for pmid in ranked[:max_refs]:
        # Determine match type
        direct_terms = [
            go_id
            for go_id in assertion.go_term_ids
            if go_id in gene_annotations and pmid in gene_annotations[go_id]
        ]

        match_type = "exact" if direct_terms else "descendant"

        matches.append(
            ReferenceMatch(
                pmid=pmid,
                genes_covered=[gene],
                go_terms_covered=direct_terms or assertion.go_term_ids,
                match_type=match_type,
            )
        )

    return matches


def _find_multi_gene_references(
    assertion: AtomicAssertion,
    gene_go_pmids: dict[str, dict[str, set[str]]],
    expanded_go_ids: set[str],
    max_refs: int,
) -> list[ReferenceMatch]:
    """Find references for multi-gene assertions."""
    # Find PMIDs that annotate at least 2 of our genes to relevant GO terms
    pmid_gene_coverage: dict[str, set[str]] = defaultdict(set)

    for gene in assertion.genes:
        if gene not in gene_go_pmids:
            continue
        gene_annotations = gene_go_pmids[gene]
        for go_id in expanded_go_ids:
            if go_id in gene_annotations:
                for pmid in gene_annotations[go_id]:
                    pmid_gene_coverage[pmid].add(gene)

    # Rank by number of genes covered, then by recency
    ranked = sorted(
        pmid_gene_coverage.items(),
        key=lambda x: (len(x[1]), int(x[0])),
        reverse=True,
    )

    matches = []
    for pmid, genes_covered in ranked[:max_refs]:
        if len(genes_covered) >= 2:  # Must cover at least 2 genes
            matches.append(
                ReferenceMatch(
                    pmid=pmid,
                    genes_covered=list(genes_covered),
                    go_terms_covered=assertion.go_term_ids,
                    match_type="multi_gene",
                )
            )

    return matches


def _find_multi_process_references(
    assertion: AtomicAssertion,
    gene_go_pmids: dict[str, dict[str, set[str]]],
    descendants_closure: dict[str, set[str]],
    max_refs: int,
) -> list[ReferenceMatch]:
    """Find references for multi-process assertions."""
    if not assertion.genes:
        return []

    gene = assertion.genes[0]
    if gene not in gene_go_pmids:
        return []

    gene_annotations = gene_go_pmids[gene]

    # Find PMIDs that annotate this gene to multiple of our target processes
    pmid_process_coverage: dict[str, set[str]] = defaultdict(set)

    for go_id in assertion.go_term_ids:
        # Check direct and descendants
        check_ids = {go_id}
        if go_id in descendants_closure:
            check_ids.update(descendants_closure[go_id])

        for check_go in check_ids:
            if check_go in gene_annotations:
                for pmid in gene_annotations[check_go]:
                    pmid_process_coverage[pmid].add(go_id)

    # Rank by process coverage, then recency
    ranked = sorted(
        pmid_process_coverage.items(),
        key=lambda x: (len(x[1]), int(x[0])),
        reverse=True,
    )

    matches = []
    for pmid, processes_covered in ranked[:max_refs]:
        match_type = "multi_process" if len(processes_covered) > 1 else "single_process"

        matches.append(
            ReferenceMatch(
                pmid=pmid,
                genes_covered=[gene],
                go_terms_covered=list(processes_covered),
                match_type=match_type,
            )
        )

    return matches[:max_refs]


# =============================================================================
# Reference Injection
# =============================================================================


def inject_references(
    summary_text: str,
    assertion_refs: list[tuple[AtomicAssertion, list[ReferenceMatch]]],
) -> str:
    """
    Inject references into summary text.

    Appends a references section to the summary with PMIDs for each
    supported assertion.

    Args:
        summary_text: Original summary text
        assertion_refs: List of (assertion, references) tuples

    Returns:
        Summary text with appended references section
    """
    if not assertion_refs:
        return summary_text

    # Check if any assertions have references
    has_refs = any(refs for _, refs in assertion_refs)
    if not has_refs:
        return summary_text

    lines = [summary_text, "", "---", "", "## Supporting References", ""]

    for assertion, refs in assertion_refs:
        if refs:
            pmids = [f"[PMID:{r.pmid}](https://pubmed.ncbi.nlm.nih.gov/{r.pmid}/)" for r in refs]

            # Truncate long claims
            claim_preview = assertion.original_text[:100]
            if len(assertion.original_text) > 100:
                claim_preview += "..."

            lines.append(f"**[{assertion.claim_type}]** \"{claim_preview}\"")
            lines.append(f"- References: {', '.join(pmids)}")
            lines.append(f"- Genes: {', '.join(assertion.genes)}")
            lines.append("")

    return "\n".join(lines)


def inject_references_inline(
    summary_text: str,
    assertion_refs: list[tuple[AtomicAssertion, list[ReferenceMatch]]],
) -> str:
    """
    Replace [REF:GENE] markers in summary_text with inline PMID hyperlinks.

    Builds a gene → deduplicated PMIDs mapping (capped at 3 per gene), then
    replaces every ``[REF:GENE]`` marker with the corresponding inline links.
    Markers for genes with no PMIDs are silently removed.

    Args:
        summary_text: Markdown text containing ``[REF:GENE]`` markers placed
            by :func:`render_explanation_to_markdown`.
        assertion_refs: List of ``(AtomicAssertion, [ReferenceMatch])`` tuples
            from the reference lookup pipeline.

    Returns:
        Markdown text with ``[REF:GENE]`` markers replaced by inline PMIDs.
    """
    # Build gene → ordered-deduplicated PMIDs (capped at 3)
    gene_pmids: dict[str, list[str]] = defaultdict(list)
    for assertion, refs in assertion_refs:
        for ref in refs:
            for gene in ref.genes_covered:
                if ref.pmid not in gene_pmids[gene]:
                    gene_pmids[gene].append(ref.pmid)

    def _replace_marker(match: re.Match) -> str:
        gene = match.group(1)
        pmids = gene_pmids.get(gene, [])[:3]  # cap at 3
        if not pmids:
            return ""
        links = ", ".join(
            f"[PMID:{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)" for pmid in pmids
        )
        return f"({links})"

    return re.sub(r"\[REF:([A-Za-z0-9_\-]+)\]", _replace_marker, summary_text)


def format_references_needing_artl_mcp(
    assertions: list[AtomicAssertion],
) -> list[dict[str, Any]]:
    """
    Format assertions needing artl-mcp lookup into query suggestions.

    Args:
        assertions: List of assertions that couldn't be resolved via GAF

    Returns:
        List of dictionaries with suggested artl-mcp queries
    """
    queries = []

    for assertion in assertions:
        # Build search query from genes and claim text
        genes_str = " ".join(assertion.genes[:3])  # Limit to 3 genes
        claim_keywords = assertion.original_text[:50]

        queries.append(
            {
                "assertion": assertion.original_text,
                "suggested_query": f"{genes_str} {claim_keywords}",
                "genes": assertion.genes,
                "go_terms": assertion.go_term_ids,
                "complexity": assertion.complexity,
            }
        )

    return queries


# =============================================================================
# Prompt Loading
# =============================================================================


def get_gaf_pmids_for_themes(
    themes: list[dict[str, Any]],
    ref_index: dict[str, Any],
    top_n: int = 5,
) -> dict[int, list[dict[str, Any]]]:
    """Get curated GAF PMIDs for each theme using the reference index.

    For each theme, collects all genes and GO IDs from the anchor term and
    specific_terms, then calls find_pmids_covering_genes() to get curated
    PMIDs sorted by how many theme genes they annotate.

    Args:
        themes: List of theme dicts from enrichment output (themes key)
        ref_index: Reference index from load_gaf_with_pmids()
        top_n: Maximum number of PMIDs to return per theme

    Returns:
        Dict mapping theme index to list of PMID dicts:
        {theme_index: [{"pmid": str, "genes_covered": list[str]}, ...]}
        Themes with no curated PMIDs get empty lists.
    """
    from ..utils.reference_index import find_pmids_covering_genes

    results: dict[int, list[dict[str, Any]]] = {}

    for i, theme in enumerate(themes):
        anchor = theme.get("anchor_term", {})
        specific_terms = theme.get("specific_terms", [])

        # Collect all genes and GO IDs in this theme
        genes: list[str] = list(anchor.get("genes", []))
        go_ids: list[str] = []
        if anchor.get("go_id"):
            go_ids.append(anchor["go_id"])

        for st in specific_terms:
            genes.extend(st.get("genes", []))
            if st.get("go_id"):
                go_ids.append(st["go_id"])

        # Deduplicate
        genes = list(dict.fromkeys(genes))

        if not genes or not go_ids:
            results[i] = []
            continue

        pmid_records = find_pmids_covering_genes(genes, go_ids, ref_index, min_genes=1)
        results[i] = [
            {"pmid": r["pmid"], "genes_covered": r["genes_covered"]}
            for r in pmid_records[:top_n]
        ]

    return results


def _load_prompt(prompt_file: str) -> dict[str, Any]:
    """
    Load co-located prompt YAML file.

    Args:
        prompt_file: Name of prompt file (e.g., "reference_retrieval.prompt.yaml")

    Returns:
        Dictionary with system_prompt, user_prompt, presets

    Raises:
        FileNotFoundError: If prompt file not found
    """
    prompt_path = Path(__file__).parent / prompt_file
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return yaml.safe_load(prompt_path.read_text())
