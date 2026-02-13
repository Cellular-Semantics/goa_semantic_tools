#!/usr/bin/env python3
"""
Exploration: Reference retrieval for provenance-labeled summaries.

This script implements the reference injection pipeline:
1. Load hierarchical themes from depth_anchors output
2. Build reference index from GO annotations (GAF)
3. [HUMAN/LLM STEP] Generate provenance-labeled summary
4. Extract [INFERENCE] and [EXTERNAL] claims
5. [HUMAN/LLM STEP] Parse claims into atomic assertions with GO term mapping
6. Programmatic reference lookup for simple assertions
7. Flag complex assertions for artl-mcp
8. Inject references into final output

Run interactively - script has breakpoints where human acts as LLM.
"""

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from goatools.anno.gaf_reader import GafReader
from goatools.obo_parser import GODag


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class GOAnnotation:
    """A GO annotation with reference."""
    gene: str
    go_id: str
    go_name: str
    evidence_code: str
    references: set[str] = field(default_factory=set)  # PMIDs


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
        """Determine complexity level for reference lookup."""
        if self.is_multi_gene and self.is_multi_process:
            return "complex"  # Needs artl-mcp
        elif self.is_multi_gene:
            return "multi_gene"  # Need PMID annotating all genes
        elif self.is_multi_process:
            return "multi_process"  # Need PMID annotating gene to multiple processes
        else:
            return "simple"  # Single gene, single process


@dataclass
class ReferenceMatch:
    """A matched reference for an assertion."""
    pmid: str
    genes_covered: list[str]
    go_terms_covered: list[str]
    match_type: str  # "exact", "descendant", "partial"


# =============================================================================
# Reference Index Building
# =============================================================================

def load_gaf_with_pmids(
    gaf_path: Path,
    godag: GODag,
    genes_of_interest: set[str] = None
) -> dict:
    """
    Load GAF annotations and build reference index.

    Returns:
        dict with structure:
        {
            'gene_go_pmids': {gene: {go_id: set(pmids)}},
            'pmid_gene_gos': {pmid: {gene: set(go_ids)}},
            'go_term_names': {go_id: name}
        }
    """
    print(f"Loading GAF annotations from {gaf_path}...")
    gaf_reader = GafReader(str(gaf_path))

    gene_go_pmids = defaultdict(lambda: defaultdict(set))
    pmid_gene_gos = defaultdict(lambda: defaultdict(set))
    go_term_names = {}

    pmid_pattern = re.compile(r'PMID:(\d+)')

    total = 0
    with_pmid = 0
    filtered = 0

    for assoc in gaf_reader.associations:
        gene = assoc.DB_Symbol
        go_id = assoc.GO_ID
        refs = assoc.DB_Reference

        # Filter to genes of interest if specified
        if genes_of_interest and gene not in genes_of_interest:
            continue
        filtered += 1

        # Store GO term name
        if go_id in godag and go_id not in go_term_names:
            go_term_names[go_id] = godag[go_id].name

        # Extract PMIDs from references
        for ref in refs:
            match = pmid_pattern.match(ref)
            if match:
                pmid = match.group(1)
                gene_go_pmids[gene][go_id].add(pmid)
                pmid_gene_gos[pmid][gene].add(go_id)
                with_pmid += 1

        total += 1

    print(f"  Total annotations: {total}")
    print(f"  Filtered to genes of interest: {filtered}")
    print(f"  Annotations with PMIDs: {with_pmid}")
    print(f"  Unique genes: {len(gene_go_pmids)}")
    print(f"  Unique PMIDs: {len(pmid_gene_gos)}")

    return {
        'gene_go_pmids': dict(gene_go_pmids),
        'pmid_gene_gos': dict(pmid_gene_gos),
        'go_term_names': go_term_names
    }


def get_descendants_closure(go_ids: set[str], godag: GODag) -> dict[str, set[str]]:
    """
    Pre-compute descendant closure for each GO term.

    Returns:
        {go_id: set(all_descendant_ids)}
    """
    closure = {}

    for go_id in go_ids:
        if go_id not in godag:
            closure[go_id] = set()
            continue

        descendants = set()
        to_visit = list(godag[go_id].children)

        while to_visit:
            child = to_visit.pop()
            if child.id not in descendants:
                descendants.add(child.id)
                to_visit.extend(child.children)

        closure[go_id] = descendants

    return closure


# =============================================================================
# Claim Extraction
# =============================================================================

def extract_claims(summary_text: str) -> dict[str, list[str]]:
    """
    Extract [INFERENCE] and [EXTERNAL] claims from provenance-labeled summary.

    Returns:
        {'INFERENCE': [claim1, claim2, ...], 'EXTERNAL': [claim1, ...]}
    """
    claims = {'INFERENCE': [], 'EXTERNAL': [], 'DATA': [], 'GO-HIERARCHY': []}

    # Pattern: [TAG] text until next [TAG] or end
    # We'll split by tags and track which tag each segment belongs to
    pattern = r'\[(DATA|INFERENCE|EXTERNAL|GO-HIERARCHY)\]'

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


# =============================================================================
# Reference Lookup
# =============================================================================

def find_references_for_assertion(
    assertion: AtomicAssertion,
    ref_index: dict,
    descendants_closure: dict[str, set[str]],
    max_refs: int = 3
) -> list[ReferenceMatch]:
    """
    Find PMIDs that support an atomic assertion.

    Strategy:
    - Simple (1 gene, 1 process): Find PMIDs annotating gene to process or descendants
    - Multi-gene (N genes, 1 process): Find PMIDs annotating ALL genes to same process
    - Multi-process (1 gene, N processes): Find PMIDs annotating gene to multiple processes
    - Complex: Return empty, flag for artl-mcp
    """
    if assertion.complexity == "complex":
        return []  # Needs artl-mcp

    gene_go_pmids = ref_index['gene_go_pmids']
    pmid_gene_gos = ref_index['pmid_gene_gos']

    # Expand GO terms to include descendants
    expanded_go_ids = set(assertion.go_term_ids)
    for go_id in assertion.go_term_ids:
        if go_id in descendants_closure:
            expanded_go_ids.update(descendants_closure[go_id])

    matches = []

    if assertion.complexity == "simple":
        # Single gene, single process
        gene = assertion.genes[0]
        if gene not in gene_go_pmids:
            return []

        gene_annotations = gene_go_pmids[gene]
        candidate_pmids = set()

        for go_id in expanded_go_ids:
            if go_id in gene_annotations:
                candidate_pmids.update(gene_annotations[go_id])

        # Rank by recency (higher PMID = newer, roughly)
        ranked = sorted(candidate_pmids, key=lambda x: int(x), reverse=True)

        for pmid in ranked[:max_refs]:
            # Determine match type
            direct_terms = [go_id for go_id in assertion.go_term_ids
                          if go_id in gene_annotations and pmid in gene_annotations[go_id]]

            match_type = "exact" if direct_terms else "descendant"

            matches.append(ReferenceMatch(
                pmid=pmid,
                genes_covered=[gene],
                go_terms_covered=direct_terms or assertion.go_term_ids,
                match_type=match_type
            ))

    elif assertion.complexity == "multi_gene":
        # Multiple genes, single process - find PMIDs annotating ALL genes
        target_go_ids = expanded_go_ids

        # Find PMIDs that annotate at least 2 of our genes to relevant GO terms
        pmid_gene_coverage = defaultdict(set)

        for gene in assertion.genes:
            if gene not in gene_go_pmids:
                continue
            gene_annotations = gene_go_pmids[gene]
            for go_id in target_go_ids:
                if go_id in gene_annotations:
                    for pmid in gene_annotations[go_id]:
                        pmid_gene_coverage[pmid].add(gene)

        # Rank by number of genes covered, then by recency
        ranked = sorted(
            pmid_gene_coverage.items(),
            key=lambda x: (len(x[1]), int(x[0])),
            reverse=True
        )

        for pmid, genes_covered in ranked[:max_refs]:
            if len(genes_covered) >= 2:  # Must cover at least 2 genes
                matches.append(ReferenceMatch(
                    pmid=pmid,
                    genes_covered=list(genes_covered),
                    go_terms_covered=assertion.go_term_ids,
                    match_type="multi_gene"
                ))

    elif assertion.complexity == "multi_process":
        # Single gene, multiple processes
        gene = assertion.genes[0]
        if gene not in gene_go_pmids:
            return []

        gene_annotations = gene_go_pmids[gene]

        # Find PMIDs that annotate this gene to multiple of our target processes
        pmid_process_coverage = defaultdict(set)

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
            reverse=True
        )

        for pmid, processes_covered in ranked[:max_refs]:
            matches.append(ReferenceMatch(
                pmid=pmid,
                genes_covered=[gene],
                go_terms_covered=list(processes_covered),
                match_type="multi_process" if len(processes_covered) > 1 else "single_process"
            ))

    return matches


# =============================================================================
# Hub Gene Analysis
# =============================================================================

def compute_hub_genes(themes: list[dict], min_themes: int = 3) -> dict:
    """
    Find genes appearing in multiple themes.

    Returns:
        {gene: {'theme_count': N, 'themes': [theme_names], 'go_terms': [go_ids]}}
    """
    gene_themes = defaultdict(lambda: {'themes': [], 'go_terms': set()})

    for theme in themes:
        anchor = theme['anchor_term']
        anchor_genes = set(anchor['genes'])

        # Include specific term genes
        all_genes = anchor_genes.copy()
        for specific in theme.get('specific_terms', []):
            all_genes.update(specific['genes'])

        theme_name = anchor['name']
        theme_go_ids = {anchor['go_id']}
        for specific in theme.get('specific_terms', []):
            theme_go_ids.add(specific['go_id'])

        for gene in all_genes:
            gene_themes[gene]['themes'].append(theme_name)
            gene_themes[gene]['go_terms'].update(theme_go_ids)

    # Filter to hub genes
    hub_genes = {}
    for gene, data in gene_themes.items():
        if len(data['themes']) >= min_themes:
            hub_genes[gene] = {
                'theme_count': len(data['themes']),
                'themes': data['themes'][:10],  # Top 10
                'go_terms': list(data['go_terms'])
            }

    # Sort by theme count
    return dict(sorted(hub_genes.items(), key=lambda x: x[1]['theme_count'], reverse=True))


# =============================================================================
# Output Formatting
# =============================================================================

def format_themes_for_llm(themes: list[dict], hub_genes: dict, max_themes: int = 30) -> str:
    """Format themes for LLM summarization prompt."""
    lines = []
    lines.append("=" * 80)
    lines.append("HIERARCHICAL THEMES FOR SUMMARIZATION")
    lines.append("=" * 80)
    lines.append("")

    # Hub genes first
    lines.append("## HUB GENES (appearing in 3+ themes)")
    lines.append("")
    for gene, data in list(hub_genes.items())[:15]:
        lines.append(f"- {gene}: {data['theme_count']} themes")
    lines.append("")

    # Themes
    lines.append("## THEMES (sorted by FDR)")
    lines.append("")

    for i, theme in enumerate(themes[:max_themes], 1):
        anchor = theme['anchor_term']
        conf = theme['anchor_confidence']

        lines.append(f"{i}. [{conf}] {anchor['name']}")
        lines.append(f"   GO:{anchor['go_id']} | FDR: {anchor['fdr']:.2e} | {len(anchor['genes'])} genes")
        lines.append(f"   Genes: {', '.join(sorted(anchor['genes'])[:10])}")
        if len(anchor['genes']) > 10:
            lines.append(f"          ... and {len(anchor['genes']) - 10} more")

        for specific in theme.get('specific_terms', [])[:3]:
            lines.append(f"   └─ {specific['name']} ({len(specific['genes'])} genes, FDR {specific['fdr']:.2e})")

        if len(theme.get('specific_terms', [])) > 3:
            lines.append(f"   └─ ... and {len(theme['specific_terms']) - 3} more specific terms")

        lines.append("")

    if len(themes) > max_themes:
        lines.append(f"... and {len(themes) - max_themes} more themes")

    return "\n".join(lines)


def inject_references(
    summary_text: str,
    assertion_refs: list[tuple[AtomicAssertion, list[ReferenceMatch]]]
) -> str:
    """
    Inject references into summary text after relevant claims.

    This is a simplified version - in practice would need smarter text matching.
    """
    # For now, append a references section
    lines = [summary_text, "", "---", "## References", ""]

    for assertion, refs in assertion_refs:
        if refs:
            pmids = [f"PMID:{r.pmid}" for r in refs]
            lines.append(f"**{assertion.claim_type}**: \"{assertion.original_text[:80]}...\"")
            lines.append(f"  Refs: {', '.join(pmids)}")
            lines.append("")

    return "\n".join(lines)


# =============================================================================
# Interactive Workflow
# =============================================================================

def save_checkpoint(data: dict, checkpoint_name: str, output_dir: Path):
    """Save intermediate data for inspection."""
    path = output_dir / f"checkpoint_{checkpoint_name}.json"

    # Convert sets to lists for JSON serialization
    def convert_sets(obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, frozenset):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: convert_sets(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_sets(v) for v in obj]
        else:
            return obj

    with open(path, 'w') as f:
        json.dump(convert_sets(data), f, indent=2)
    print(f"Checkpoint saved: {path}")


def main():
    """Interactive reference retrieval workflow."""

    # Paths
    project_root = Path(__file__).parent.parent
    themes_file = project_root / "results/benchmark/hallmark_inflammatory_response_depth_anchors.json"
    gaf_path = project_root / "reference_data/goa_human.gaf"
    go_obo_path = project_root / "reference_data/go-basic.obo"
    output_dir = project_root / "results/reference_retrieval"
    output_dir.mkdir(exist_ok=True)

    print("=" * 80)
    print("REFERENCE RETRIEVAL EXPLORATION")
    print("=" * 80)

    # Step 1: Load themes
    print("\n## Step 1: Load hierarchical themes")
    with open(themes_file) as f:
        themes_data = json.load(f)

    themes = themes_data['themes']
    print(f"  Loaded {len(themes)} themes")
    print(f"  With children: {sum(1 for t in themes if t.get('specific_terms'))}")

    # Extract all genes from themes
    all_genes = set()
    all_go_ids = set()
    for theme in themes:
        all_genes.update(theme['anchor_term']['genes'])
        all_go_ids.add(theme['anchor_term']['go_id'])
        for specific in theme.get('specific_terms', []):
            all_genes.update(specific['genes'])
            all_go_ids.add(specific['go_id'])

    print(f"  Total genes: {len(all_genes)}")
    print(f"  Total GO terms: {len(all_go_ids)}")

    # Step 2: Load GO DAG
    print("\n## Step 2: Load GO ontology")
    godag = GODag(str(go_obo_path), optional_attrs={"relationship"}, prt=None)
    print(f"  Loaded {len(godag)} terms")

    # Pre-compute descendant closure for theme GO terms
    print("  Computing descendant closure...")
    descendants_closure = get_descendants_closure(all_go_ids, godag)
    total_descendants = sum(len(d) for d in descendants_closure.values())
    print(f"  Total descendants across all theme terms: {total_descendants}")

    # Step 3: Build reference index
    print("\n## Step 3: Build reference index from GAF")
    ref_index = load_gaf_with_pmids(gaf_path, godag, genes_of_interest=all_genes)

    # Step 4: Compute hub genes
    print("\n## Step 4: Compute hub genes")
    hub_genes = compute_hub_genes(themes, min_themes=3)
    print(f"  Found {len(hub_genes)} hub genes (appearing in 3+ themes)")
    print("  Top 10:")
    for gene, data in list(hub_genes.items())[:10]:
        print(f"    {gene}: {data['theme_count']} themes")

    # Save checkpoint
    save_checkpoint({
        'hub_genes': hub_genes,
        'all_genes': list(all_genes),
        'all_go_ids': list(all_go_ids),
        'ref_index_stats': {
            'n_genes': len(ref_index['gene_go_pmids']),
            'n_pmids': len(ref_index['pmid_gene_gos']),
            'n_go_terms': len(ref_index['go_term_names'])
        }
    }, 'step4_hub_genes', output_dir)

    # Step 5: Format for LLM
    print("\n## Step 5: Format themes for LLM summarization")
    llm_input = format_themes_for_llm(themes, hub_genes)

    llm_input_file = output_dir / "llm_input_themes.txt"
    with open(llm_input_file, 'w') as f:
        f.write(llm_input)
    print(f"  Saved to: {llm_input_file}")

    print("\n" + "=" * 80)
    print("HUMAN/LLM STEP: Generate provenance-labeled summary")
    print("=" * 80)
    print("""
Instructions:
1. Read the themes from: results/reference_retrieval/llm_input_themes.txt
2. Generate a biological summary using these provenance tags:
   - [DATA]: Direct observations (FDR values, gene counts, co-occurrence)
   - [GO-HIERARCHY]: Facts from GO parent-child structure
   - [INFERENCE]: Logical deductions from co-annotation patterns
   - [EXTERNAL]: Claims requiring training/latent knowledge

3. Save your summary to: results/reference_retrieval/llm_summary.txt

4. Re-run this script with --step2 to continue
""")

    # Also print the prompt template
    prompt_file = output_dir / "summarization_prompt.txt"
    prompt = """Generate a provenance-labeled biological summary of this GO enrichment analysis.

Use these tags to distinguish claim sources:
- [DATA]: Direct observations from enrichment (FDR values, gene counts, co-occurrence facts)
- [GO-HIERARCHY]: Facts derived from GO parent-child structure (subsumption, specialization)
- [INFERENCE]: Logical deductions from co-annotation patterns
- [EXTERNAL]: Claims requiring training/latent knowledge (need literature support)

Guidelines:
- Focus on biology, not ontology structure
- Avoid depth numbers - use "more/less specific" or "specialized" language
- Do not describe GO organization (e.g., "flat categorization under umbrella term")
- Explain biological significance of hierarchical groupings
- Highlight hub genes and their pathway convergence patterns
- For [INFERENCE] claims, mention the specific genes involved
- Be explicit about which processes connect via shared genes

Input themes follow:

""" + llm_input

    with open(prompt_file, 'w') as f:
        f.write(prompt)
    print(f"  Full prompt saved to: {prompt_file}")

    return {
        'themes': themes,
        'hub_genes': hub_genes,
        'ref_index': ref_index,
        'descendants_closure': descendants_closure,
        'godag': godag,
        'output_dir': output_dir
    }


def step2_extract_claims(output_dir: Path = None):
    """Step 2: Extract claims from LLM summary."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "results/reference_retrieval"

    summary_file = output_dir / "llm_summary.txt"

    if not summary_file.exists():
        print(f"ERROR: Summary file not found: {summary_file}")
        print("Please complete the LLM step first.")
        return None

    print("\n## Step 6: Extract claims from summary")
    with open(summary_file) as f:
        summary_text = f.read()

    claims = extract_claims(summary_text)

    print(f"  [DATA] claims: {len(claims['DATA'])}")
    print(f"  [GO-HIERARCHY] claims: {len(claims['GO-HIERARCHY'])}")
    print(f"  [INFERENCE] claims: {len(claims['INFERENCE'])}")
    print(f"  [EXTERNAL] claims: {len(claims['EXTERNAL'])}")

    # Save claims for inspection
    save_checkpoint(claims, 'step6_claims', output_dir)

    print("\n## [INFERENCE] Claims:")
    for i, claim in enumerate(claims['INFERENCE'], 1):
        print(f"  {i}. {claim[:100]}...")

    print("\n## [EXTERNAL] Claims:")
    for i, claim in enumerate(claims['EXTERNAL'], 1):
        print(f"  {i}. {claim[:100]}...")

    print("\n" + "=" * 80)
    print("HUMAN/LLM STEP: Parse claims into atomic assertions")
    print("=" * 80)
    print("""
Instructions:
1. For each [INFERENCE] and [EXTERNAL] claim, extract:
   - genes: List of gene symbols mentioned
   - go_term_ids: Map process names to GO IDs from the theme list

2. Create a JSON file: results/reference_retrieval/atomic_assertions.json
   Format:
   [
     {
       "claim_type": "INFERENCE",
       "original_text": "The claim text...",
       "genes": ["RELA", "IL1B"],
       "go_term_ids": ["GO:0006954", "GO:0071222"],
       "is_multi_gene": true,
       "is_multi_process": false
     },
     ...
   ]

3. Re-run this script with --step3 to continue
""")

    return claims


def step3_lookup_references(output_dir: Path = None):
    """Step 3: Lookup references for atomic assertions."""
    project_root = Path(__file__).parent.parent
    if output_dir is None:
        output_dir = project_root / "results/reference_retrieval"

    assertions_file = output_dir / "atomic_assertions.json"

    if not assertions_file.exists():
        print(f"ERROR: Assertions file not found: {assertions_file}")
        print("Please complete the atomic assertions step first.")
        return None

    # Reload required data
    print("\n## Step 7: Loading data for reference lookup...")

    themes_file = project_root / "results/benchmark/hallmark_inflammatory_response_depth_anchors.json"
    gaf_path = project_root / "reference_data/goa_human.gaf"
    go_obo_path = project_root / "reference_data/go-basic.obo"

    with open(themes_file) as f:
        themes_data = json.load(f)
    themes = themes_data['themes']

    # Extract all genes and GO IDs
    all_genes = set()
    all_go_ids = set()
    for theme in themes:
        all_genes.update(theme['anchor_term']['genes'])
        all_go_ids.add(theme['anchor_term']['go_id'])
        for specific in theme.get('specific_terms', []):
            all_genes.update(specific['genes'])
            all_go_ids.add(specific['go_id'])

    godag = GODag(str(go_obo_path), optional_attrs={"relationship"}, prt=None)
    descendants_closure = get_descendants_closure(all_go_ids, godag)
    ref_index = load_gaf_with_pmids(gaf_path, godag, genes_of_interest=all_genes)

    # Load assertions
    print("\n## Step 8: Lookup references for assertions")
    with open(assertions_file) as f:
        assertions_raw = json.load(f)

    assertions = [
        AtomicAssertion(
            claim_type=a['claim_type'],
            original_text=a['original_text'],
            genes=a['genes'],
            go_term_ids=a['go_term_ids'],
            is_multi_gene=a['is_multi_gene'],
            is_multi_process=a['is_multi_process']
        )
        for a in assertions_raw
    ]

    print(f"  Loaded {len(assertions)} assertions")

    # Lookup references
    results = []
    needs_artl_mcp = []

    for assertion in assertions:
        refs = find_references_for_assertion(
            assertion, ref_index, descendants_closure, max_refs=3
        )

        results.append((assertion, refs))

        if assertion.complexity == "complex" or not refs:
            needs_artl_mcp.append(assertion)

        print(f"\n  [{assertion.claim_type}] {assertion.original_text[:60]}...")
        print(f"    Complexity: {assertion.complexity}")
        print(f"    Genes: {assertion.genes}")
        print(f"    GO terms: {assertion.go_term_ids}")
        if refs:
            for ref in refs:
                print(f"    → PMID:{ref.pmid} ({ref.match_type}, covers {ref.genes_covered})")
        else:
            print(f"    → No GO annotation refs found - needs artl-mcp")

    # Save results
    results_data = []
    for assertion, refs in results:
        results_data.append({
            'claim_type': assertion.claim_type,
            'original_text': assertion.original_text,
            'genes': assertion.genes,
            'go_term_ids': assertion.go_term_ids,
            'complexity': assertion.complexity,
            'references': [
                {
                    'pmid': r.pmid,
                    'genes_covered': r.genes_covered,
                    'go_terms_covered': r.go_terms_covered,
                    'match_type': r.match_type
                }
                for r in refs
            ]
        })

    save_checkpoint(results_data, 'step8_references', output_dir)

    # Report on artl-mcp needs
    print("\n" + "=" * 80)
    print(f"ASSERTIONS NEEDING artl-mcp: {len(needs_artl_mcp)}")
    print("=" * 80)

    for assertion in needs_artl_mcp:
        print(f"\n[{assertion.claim_type}] {assertion.original_text}")
        print(f"  Genes: {assertion.genes}")

    # Save artl-mcp queries
    artl_queries = []
    for assertion in needs_artl_mcp:
        # Build search query from genes and claim text
        genes_str = " ".join(assertion.genes[:3])  # Limit to 3 genes
        query = f"{genes_str} {assertion.original_text[:50]}"
        artl_queries.append({
            'assertion': assertion.original_text,
            'suggested_query': query,
            'genes': assertion.genes
        })

    save_checkpoint(artl_queries, 'step8_artl_queries', output_dir)

    return results, needs_artl_mcp


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--step2":
            step2_extract_claims()
        elif sys.argv[1] == "--step3":
            step3_lookup_references()
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Usage: python 10_reference_retrieval.py [--step2|--step3]")
    else:
        main()