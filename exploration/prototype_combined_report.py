#!/usr/bin/env python3
"""
Prototype: Combined CC/MF/BP reporting for enriched genes.
Shows how we could create integrated gene-centric reports.
"""

import json
from collections import defaultdict
from pathlib import Path

# Load the enrichment results
results_file = Path(__file__).parent.parent / "results/20260115_202817_astrocytoma_c0_enrichment.json"

with open(results_file) as f:
    data = json.load(f)

# Build gene-centric view
gene_annotations = defaultdict(lambda: {'CC': [], 'MF': [], 'BP': []})

for cluster in data['clusters']:
    ns = cluster['root_term']['namespace']
    ns_abbrev = {'cellular_component': 'CC',
                 'molecular_function': 'MF',
                 'biological_process': 'BP'}[ns]

    for gene in cluster['root_term']['study_genes']:
        gene_annotations[gene][ns_abbrev].append({
            'term': cluster['root_term']['name'],
            'go_id': cluster['root_term']['go_id'],
            'fdr': cluster['root_term']['fdr'],
            'p_value': cluster['root_term']['p_value']
        })

# Filter to genes with all three namespaces
complete_genes = {gene: annots for gene, annots in gene_annotations.items()
                  if all(annots[ns] for ns in ['CC', 'MF', 'BP'])}

print("="*80)
print("INTEGRATED GENE ANNOTATION REPORT")
print("Astrocytoma Cluster 0 - Genes with Complete Functional Context")
print("="*80)
print()

for gene in sorted(complete_genes.keys()):
    annots = complete_genes[gene]

    print(f"{'━'*80}")
    print(f"  {gene}")
    print(f"{'━'*80}")

    # Cellular Component - WHERE the gene product is located
    print("\n  📍 LOCATION (Cellular Component):")
    for cc in annots['CC']:
        print(f"     • {cc['term']} (FDR={cc['fdr']:.2e})")

    # Molecular Function - WHAT the gene product does
    print("\n  ⚙️  FUNCTION (Molecular Function):")
    for mf in annots['MF']:
        print(f"     • {mf['term']} (FDR={mf['fdr']:.2e})")

    # Biological Process - WHY - what larger process it participates in
    print("\n  🔄 PROCESSES (Biological Process):")
    for bp in annots['BP']:
        print(f"     • {bp['term']} (FDR={bp['fdr']:.2e})")

    print()

print("="*80)
print(f"Total genes with complete functional context: {len(complete_genes)}")
print("="*80)

# Now create a thematic grouping
print("\n\n")
print("="*80)
print("THEMATIC SUMMARY")
print("="*80)
print()

# Group genes by biological process themes
bp_to_genes = defaultdict(set)
for gene, annots in complete_genes.items():
    for bp in annots['BP']:
        bp_to_genes[bp['term']].add(gene)

# Show thematic groupings
for bp_term, genes in sorted(bp_to_genes.items()):
    print(f"\n🎯 {bp_term.upper()}")
    print(f"   Genes: {', '.join(sorted(genes))}")

    # Show common locations and functions
    cc_counts = defaultdict(int)
    mf_counts = defaultdict(int)

    for gene in genes:
        for cc in complete_genes[gene]['CC']:
            cc_counts[cc['term']] += 1
        for mf in complete_genes[gene]['MF']:
            mf_counts[mf['term']] += 1

    if cc_counts:
        top_cc = max(cc_counts.items(), key=lambda x: x[1])
        print(f"   Common location: {top_cc[0]} ({top_cc[1]}/{len(genes)} genes)")

    if mf_counts:
        top_mf = max(mf_counts.items(), key=lambda x: x[1])
        print(f"   Common function: {top_mf[0]} ({top_mf[1]}/{len(genes)} genes)")

print("\n" + "="*80)
