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

        if go_id not in godag:
            continue

        if gene not in gene_to_annotations:
            gene_to_annotations[gene] = []

        gene_to_annotations[gene].append(
            {
                "go_id": go_id,
                "go_name": godag[go_id].name,
                "evidence_code": evidence,
                "namespace": godag[go_id].namespace,
            }
        )

    return gene_to_annotations
