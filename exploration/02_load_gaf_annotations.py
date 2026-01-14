"""
Test Script 2: Load GAF Annotations

This script tests loading GAF (Gene Association File) annotations and exploring gene-to-GO mappings.
"""
from pathlib import Path
from goatools.obo_parser import GODag
from goatools.anno.gaf_reader import GafReader

# Paths
GO_OBO_PATH = Path(__file__).parent.parent / "reference_data" / "go-basic.obo"
GAF_PATH = Path(__file__).parent.parent / "reference_data" / "goa_human.gaf"

def main():
    print("=" * 80)
    print("Test Script 2: Load GAF Annotations")
    print("=" * 80)

    # Load GO DAG first
    print(f"\n1. Loading GO ontology from: {GO_OBO_PATH}")
    godag = GODag(str(GO_OBO_PATH))
    print(f"   GO DAG loaded: {len(godag)} terms")

    # Load GAF annotations
    print(f"\n2. Loading GAF annotations from: {GAF_PATH}")
    print(f"   File exists: {GAF_PATH.exists()}")
    print(f"   File size: {GAF_PATH.stat().st_size / (1024**2):.2f} MB (compressed)")

    print("\n   Reading GAF file...")
    gaf_reader = GafReader(str(GAF_PATH))

    # Get associations
    print("\n3. GAF Associations Loaded:")
    print(f"   Total associations: {len(gaf_reader.associations)}")

    # Explore a few associations
    print("\n4. Sample Associations (first 5):")
    for i, assoc in enumerate(gaf_reader.associations[:5]):
        print(f"\n   Association {i+1}:")
        print(f"      DB: {assoc.DB}")
        print(f"      DB_ID: {assoc.DB_ID}")
        print(f"      DB_Symbol: {assoc.DB_Symbol}")
        print(f"      GO_ID: {assoc.GO_ID}")
        print(f"      Evidence: {assoc.Evidence_Code}")
        print(f"      Taxon: {assoc.Taxon}")
        print(f"      Qualifier: {assoc.Qualifier}")
        print(f"      Date: {assoc.Date}")

    # Build gene to GO mapping
    print("\n5. Building Gene to GO Mapping...")
    gene_to_gos = {}
    for assoc in gaf_reader.associations:
        gene = assoc.DB_Symbol
        go_id = assoc.GO_ID
        evidence = assoc.Evidence_Code

        if gene not in gene_to_gos:
            gene_to_gos[gene] = []

        gene_to_gos[gene].append({
            'go_id': go_id,
            'evidence': evidence,
            'go_name': godag[go_id].name if go_id in godag else 'Unknown',
            'namespace': godag[go_id].namespace if go_id in godag else 'Unknown'
        })

    print(f"   Total unique genes: {len(gene_to_gos)}")

    # Test with specific genes (tumor suppressors)
    test_genes = ['TP53', 'BRCA1', 'BRCA2', 'PTEN', 'RB1']
    print(f"\n6. Test with Tumor Suppressor Genes:")
    for gene in test_genes:
        if gene in gene_to_gos:
            annotations = gene_to_gos[gene]
            print(f"\n   {gene}: {len(annotations)} GO annotations")

            # Count by namespace
            ns_counts = {}
            for annot in annotations:
                ns = annot['namespace']
                ns_counts[ns] = ns_counts.get(ns, 0) + 1

            for ns, count in sorted(ns_counts.items()):
                print(f"      - {ns}: {count} annotations")

            # Show sample annotations
            print(f"      Sample annotations:")
            for annot in annotations[:3]:
                print(f"         {annot['go_id']}: {annot['go_name']} ({annot['evidence']})")

        else:
            print(f"\n   {gene}: NOT FOUND in annotations")

    # Test evidence codes
    print("\n7. Evidence Code Distribution:")
    evidence_counts = {}
    for assoc in gaf_reader.associations:
        evidence = assoc.Evidence_Code
        evidence_counts[evidence] = evidence_counts.get(evidence, 0) + 1

    # Show top 10 evidence codes
    sorted_evidence = sorted(evidence_counts.items(), key=lambda x: x[1], reverse=True)
    for evidence, count in sorted_evidence[:10]:
        print(f"   {evidence}: {count:,} annotations")

    # Test namespace distribution
    print("\n8. Namespace Distribution:")
    namespace_counts = {}
    for assoc in gaf_reader.associations:
        go_id = assoc.GO_ID
        if go_id in godag:
            ns = godag[go_id].namespace
            namespace_counts[ns] = namespace_counts.get(ns, 0) + 1

    for ns, count in sorted(namespace_counts.items()):
        print(f"   {ns}: {count:,} annotations")

    print("\n" + "=" * 80)
    print("Test completed successfully!")
    print("=" * 80)

    return godag, gaf_reader, gene_to_gos

if __name__ == "__main__":
    godag, gaf_reader, gene_to_gos = main()
