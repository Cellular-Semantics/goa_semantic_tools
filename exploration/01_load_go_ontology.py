"""
Test Script 1: Load GO Ontology and Explore Structure

This script tests loading the GO ontology using GOATOOLS and explores its structure.
"""
from pathlib import Path
from goatools.obo_parser import GODag

# Path to downloaded GO ontology
GO_OBO_PATH = Path(__file__).parent.parent / "reference_data" / "go-basic.obo"

def main():
    print("=" * 80)
    print("Test Script 1: Load GO Ontology")
    print("=" * 80)

    # Load GO DAG
    print(f"\n1. Loading GO ontology from: {GO_OBO_PATH}")
    print(f"   File exists: {GO_OBO_PATH.exists()}")
    print(f"   File size: {GO_OBO_PATH.stat().st_size / (1024**2):.2f} MB")

    print("\n   Loading GO DAG...")
    godag = GODag(str(GO_OBO_PATH))

    print(f"\n2. GO DAG loaded successfully!")
    print(f"   Total terms: {len(godag)}")

    # Explore GO namespaces
    print("\n3. GO Namespaces:")
    namespaces = {}
    for term_id, term in godag.items():
        ns = term.namespace
        if ns not in namespaces:
            namespaces[ns] = 0
        namespaces[ns] += 1

    for ns, count in sorted(namespaces.items()):
        print(f"   - {ns}: {count} terms")

    # Explore a sample term
    print("\n4. Sample Term Exploration (GO:0008150 - biological_process root):")
    if "GO:0008150" in godag:
        bp_root = godag["GO:0008150"]
        print(f"   ID: {bp_root.id}")
        print(f"   Name: {bp_root.name}")
        print(f"   Namespace: {bp_root.namespace}")
        print(f"   Definition: {bp_root.defn[:100]}..." if hasattr(bp_root, 'defn') and bp_root.defn else "   No definition")
        print(f"   Level: {bp_root.level}")
        print(f"   Depth: {bp_root.depth}")
        print(f"   Number of children: {len(bp_root.children)}")
        print(f"   Number of parents: {len(bp_root.parents)}")
        print(f"   Is obsolete: {bp_root.is_obsolete}")

    # Test hierarchy navigation - get all parents
    print("\n5. Test Hierarchy Navigation (GO:0006915 - apoptotic process):")
    if "GO:0006915" in godag:
        apoptosis = godag["GO:0006915"]
        print(f"   ID: {apoptosis.id}")
        print(f"   Name: {apoptosis.name}")
        print(f"   Namespace: {apoptosis.namespace}")
        print(f"   Level: {apoptosis.level}")
        print(f"   Depth: {apoptosis.depth}")

        # Get all parents (ancestors)
        all_parents = apoptosis.get_all_parents()
        print(f"\n   All parents (ancestors): {len(all_parents)} terms")
        print(f"   Sample parents:")
        for i, parent_id in enumerate(list(all_parents)[:5]):
            if parent_id in godag:
                parent = godag[parent_id]
                print(f"      - {parent_id}: {parent.name} (level {parent.level})")

        # Get direct parents
        print(f"\n   Direct parents: {len(apoptosis.parents)} terms")
        for parent in apoptosis.parents:
            print(f"      - {parent.id}: {parent.name}")

        # Get direct children
        print(f"\n   Direct children: {len(apoptosis.children)} terms")
        for i, child in enumerate(list(apoptosis.children)[:5]):
            print(f"      - {child.id}: {child.name}")
        if len(apoptosis.children) > 5:
            print(f"      ... and {len(apoptosis.children) - 5} more")

    # Test finding descendants
    print("\n6. Test Finding Descendants:")
    if "GO:0008150" in godag:
        bp_root = godag["GO:0008150"]
        # Get all descendants
        all_descendants = bp_root.get_all_children()
        print(f"   GO:0008150 (biological_process) has {len(all_descendants)} descendants")

    print("\n" + "=" * 80)
    print("Test completed successfully!")
    print("=" * 80)

    # Return godag for potential reuse
    return godag

if __name__ == "__main__":
    godag = main()
