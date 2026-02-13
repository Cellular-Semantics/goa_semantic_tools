"""
GO Data Loader Utility

Loads GO ontology and GAF annotations using GOATOOLS.
"""
from pathlib import Path
from typing import Any

from goatools.anno.gaf_reader import GafReader
from goatools.obo_parser import GODag


def load_go_data(go_obo_path: Path) -> GODag:
    """
    Load GO ontology from OBO file.

    Loads with optional_attrs={'relationship'} to support propagate_counts
    in GO enrichment analysis.

    Args:
        go_obo_path: Path to go-basic.obo file

    Returns:
        GODag object with GO ontology

    Raises:
        FileNotFoundError: If OBO file doesn't exist
        Exception: If OBO parsing fails
    """
    if not go_obo_path.exists():
        raise FileNotFoundError(f"GO OBO file not found: {go_obo_path}")

    print(f"Loading GO ontology from: {go_obo_path}")

    # Load with relationship for propagate_counts support
    godag = GODag(str(go_obo_path), optional_attrs={"relationship"})

    print(f"  Loaded {len(godag)} GO terms")

    # Count by namespace
    ns_counts: dict[str, int] = {}
    for term in godag.values():
        ns = term.namespace
        ns_counts[ns] = ns_counts.get(ns, 0) + 1

    for ns, count in sorted(ns_counts.items()):
        print(f"    {ns}: {count} terms")

    return godag


def load_gene_annotations(gaf_path: Path, godag: GODag) -> dict[str, dict[str, set[str]]]:
    """
    Load GAF annotations and build namespace-separated gene-to-GO mappings.

    Builds associations in format required by GOEnrichmentStudyNS:
    ns2assoc[namespace][gene_symbol] = set of GO IDs

    Args:
        gaf_path: Path to GAF file (must be decompressed, not .gz)
        godag: GO DAG object (needed to determine namespace of each GO term)

    Returns:
        Namespace-separated associations:
        {
            'biological_process': {'TP53': {'GO:0008285', ...}, ...},
            'cellular_component': {...},
            'molecular_function': {...}
        }

    Raises:
        FileNotFoundError: If GAF file doesn't exist
        Exception: If GAF parsing fails
    """
    if not gaf_path.exists():
        raise FileNotFoundError(f"GAF file not found: {gaf_path}")

    print(f"Loading GAF annotations from: {gaf_path}")

    # Load GAF file
    gaf_reader = GafReader(str(gaf_path))

    print(f"  Loaded {len(gaf_reader.associations):,} associations")

    # Build namespace-separated associations
    ns2assoc: dict[str, dict[str, set[str]]] = {}

    for assoc in gaf_reader.associations:
        gene = assoc.DB_Symbol
        go_id = assoc.GO_ID

        # Get namespace from GO DAG
        if go_id not in godag:
            continue  # Skip terms not in GO DAG

        ns = godag[go_id].namespace

        # Initialize namespace if needed
        if ns not in ns2assoc:
            ns2assoc[ns] = {}

        # Initialize gene if needed
        if gene not in ns2assoc[ns]:
            ns2assoc[ns][gene] = set()

        # Add annotation
        ns2assoc[ns][gene].add(go_id)

    # Count unique genes per namespace
    print("  Unique genes per namespace:")
    for ns, gene_dict in sorted(ns2assoc.items()):
        print(f"    {ns}: {len(gene_dict):,} genes")

    return ns2assoc


def build_gene_to_go_mapping(
    gaf_path: Path, godag: GODag
) -> dict[str, list[dict[str, Any]]]:
    """
    Build detailed gene-to-GO mapping with evidence codes.

    This is used for drill-down to show which genes have which annotations.

    Args:
        gaf_path: Path to GAF file
        godag: GO DAG object

    Returns:
        Mapping of gene symbol to list of annotations:
        {
            'TP53': [
                {
                    'go_id': 'GO:0008285',
                    'go_name': 'negative regulation of cell population proliferation',
                    'evidence_code': 'IDA',
                    'namespace': 'biological_process'
                },
                ...
            ],
            ...
        }
    """
    if not gaf_path.exists():
        raise FileNotFoundError(f"GAF file not found: {gaf_path}")

    # Load GAF file
    gaf_reader = GafReader(str(gaf_path))

    # Build detailed mapping
    gene_to_annotations: dict[str, list[dict[str, Any]]] = {}

    for assoc in gaf_reader.associations:
        gene = assoc.DB_Symbol
        go_id = assoc.GO_ID
        evidence = assoc.Evidence_Code
        # GAF column 6: references (e.g., "PMID:12345|PMID:67890")
        references_raw = getattr(assoc, "DB_Reference", "")

        if go_id not in godag:
            continue

        if gene not in gene_to_annotations:
            gene_to_annotations[gene] = []

        # Parse references - handle both string and set formats
        references = []
        if references_raw:
            if isinstance(references_raw, set):
                # GOATOOLS returns DB_Reference as a set
                references = [ref.strip() for ref in references_raw if ref and ref.strip()]
            elif isinstance(references_raw, str):
                # Handle pipe-separated string format
                references = [ref.strip() for ref in references_raw.split("|") if ref.strip()]

        gene_to_annotations[gene].append(
            {
                "go_id": go_id,
                "go_name": godag[go_id].name,
                "evidence_code": evidence,
                "namespace": godag[go_id].namespace,
                "references": references,
            }
        )

    # Collapse annotations by GO term to eliminate redundancy
    return _collapse_annotations_by_go_term(gene_to_annotations)


def _collapse_annotations_by_go_term(
    gene_to_annotations: dict[str, list[dict[str, Any]]]
) -> dict[str, list[dict[str, Any]]]:
    """
    Collapse redundant annotations by grouping evidence codes for each GO term.

    Converts:
      [{go_id: "GO:123", evidence_code: "IDA", references: ["PMID:1"]},
       {go_id: "GO:123", evidence_code: "IMP", references: ["PMID:2"]},
       {go_id: "GO:123", evidence_code: "IMP", references: ["PMID:3"]}]

    To:
      [{go_id: "GO:123",
        go_name: "...",
        namespace: "...",
        evidence: [
          {code: "IDA", references: ["PMID:1"]},
          {code: "IMP", references: ["PMID:2", "PMID:3"]}
        ]}]

    Args:
        gene_to_annotations: Raw annotations with duplicates

    Returns:
        Collapsed annotations grouped by GO term
    """
    collapsed = {}

    for gene, annotations in gene_to_annotations.items():
        # Group by GO term
        go_term_map: dict[str, dict[str, Any]] = {}

        for annot in annotations:
            go_id = annot["go_id"]

            if go_id not in go_term_map:
                go_term_map[go_id] = {
                    "go_id": go_id,
                    "go_name": annot["go_name"],
                    "namespace": annot["namespace"],
                    "evidence": {},  # Will map evidence_code -> set of references
                }

            # Add this evidence code and references
            evidence_code = annot["evidence_code"]
            if evidence_code not in go_term_map[go_id]["evidence"]:
                go_term_map[go_id]["evidence"][evidence_code] = set()

            # Add references to this evidence code
            for ref in annot["references"]:
                go_term_map[go_id]["evidence"][evidence_code].add(ref)

        # Convert to final format
        collapsed_annotations = []
        for go_data in go_term_map.values():
            # Convert evidence dict to list format
            evidence_list = [
                {"code": code, "references": sorted(refs)}
                for code, refs in sorted(go_data["evidence"].items())
            ]

            collapsed_annotations.append(
                {
                    "go_id": go_data["go_id"],
                    "go_name": go_data["go_name"],
                    "namespace": go_data["namespace"],
                    "evidence": evidence_list,
                }
            )

        collapsed[gene] = collapsed_annotations

    return collapsed
