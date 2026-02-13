#!/usr/bin/env python3
"""
Explore how CC, MF, and BP annotations overlap in enrichment results.
This will help design better summary reports that combine these aspects.
"""

import json
from collections import defaultdict
from pathlib import Path

# Load the enrichment results
results_file = Path(__file__).parent.parent / "results/20260115_202817_astrocytoma_c0_enrichment.json"

with open(results_file) as f:
    data = json.load(f)

print(f"Total clusters: {len(data['clusters'])}\n")

# Analyze namespace distribution
namespace_counts = defaultdict(int)
clusters_by_namespace = defaultdict(list)

for cluster in data['clusters']:
    ns = cluster['root_term']['namespace']
    namespace_counts[ns] += 1
    clusters_by_namespace[ns].append(cluster)

print("Clusters by namespace:")
for ns, count in namespace_counts.items():
    print(f"  {ns}: {count}")

print("\n" + "="*80 + "\n")

# Analyze gene overlap across namespaces
gene_to_namespaces = defaultdict(set)
gene_to_clusters = defaultdict(list)

for cluster in data['clusters']:
    ns = cluster['root_term']['namespace']
    root_genes = set(cluster['root_term']['study_genes'])

    for gene in root_genes:
        gene_to_namespaces[gene].add(ns)
        gene_to_clusters[gene].append({
            'namespace': ns,
            'go_id': cluster['root_term']['go_id'],
            'name': cluster['root_term']['name'],
            'p_value': cluster['root_term']['p_value'],
            'fdr': cluster['root_term']['fdr']
        })

# Count genes with multiple namespace annotations
multi_namespace_genes = {gene: namespaces for gene, namespaces in gene_to_namespaces.items()
                         if len(namespaces) > 1}

print(f"Total unique genes across all clusters: {len(gene_to_namespaces)}")
print(f"Genes with annotations in multiple namespaces: {len(multi_namespace_genes)}")

# Breakdown by namespace combinations
namespace_combos = defaultdict(int)
for gene, namespaces in multi_namespace_genes.items():
    combo = tuple(sorted(namespaces))
    namespace_combos[combo] += 1

print("\nGenes by namespace combinations:")
for combo, count in sorted(namespace_combos.items(), key=lambda x: x[1], reverse=True):
    print(f"  {' + '.join(combo)}: {count} genes")

print("\n" + "="*80 + "\n")

# Show example genes with all three namespaces
all_three = [gene for gene, ns in multi_namespace_genes.items() if len(ns) == 3]

if all_three:
    print(f"Example genes with CC + MF + BP annotations ({len(all_three)} total):\n")

    # Show first 5 examples with their annotations
    for gene in all_three[:5]:
        print(f"\n{gene}:")
        for cluster_info in gene_to_clusters[gene]:
            print(f"  [{cluster_info['namespace'][:2].upper()}] {cluster_info['name']} "
                  f"(GO:{cluster_info['go_id'][3:]}, FDR={cluster_info['fdr']:.2e})")

print("\n" + "="*80 + "\n")

# Analyze cluster sizes and see if there are similar gene sets across namespaces
print("Looking for similar gene sets across different namespaces...\n")

# Group clusters by their gene sets
gene_set_to_clusters = defaultdict(list)
for cluster in data['clusters']:
    gene_set = frozenset(cluster['root_term']['study_genes'])
    gene_set_to_clusters[gene_set].append(cluster)

# Find gene sets that appear in multiple namespaces
multi_namespace_sets = {genes: clusters for genes, clusters in gene_set_to_clusters.items()
                        if len(set(c['root_term']['namespace'] for c in clusters)) > 1}

print(f"Gene sets appearing in multiple namespaces: {len(multi_namespace_sets)}")

if multi_namespace_sets:
    print("\nExample multi-namespace gene sets:\n")
    for i, (genes, clusters) in enumerate(list(multi_namespace_sets.items())[:3]):
        print(f"Gene set {i+1} ({len(genes)} genes):")
        for cluster in clusters:
            ns = cluster['root_term']['namespace']
            name = cluster['root_term']['name']
            fdr = cluster['root_term']['fdr']
            print(f"  [{ns[:2].upper()}] {name} (FDR={fdr:.2e})")
        print()

print("="*80 + "\n")

# Summary statistics for potential combined reporting
print("SUMMARY: Potential for combined reporting")
print(f"  - {len(multi_namespace_genes)} genes have annotations across 2+ namespaces")
print(f"  - This represents {len(multi_namespace_genes)/len(gene_to_namespaces)*100:.1f}% of all annotated genes")
print(f"  - {len(all_three)} genes have all three aspects (CC + MF + BP)")
print(f"  - Could create integrated gene-centric reports showing WHERE + WHAT + WHY")
