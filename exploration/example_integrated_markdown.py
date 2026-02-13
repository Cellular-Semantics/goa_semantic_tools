#!/usr/bin/env python3
"""
Generate example integrated markdown report combining CC/MF/BP.
This shows what the actual report output could look like.
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

# Filter to genes with multiple namespaces
multi_ns_genes = {gene: annots for gene, annots in gene_annotations.items()
                  if sum(1 for ns in ['CC', 'MF', 'BP'] if annots[ns]) >= 2}

# Generate markdown
output = []

output.append("# Integrated Functional Analysis")
output.append("")
output.append("## Summary")
output.append("")
output.append(f"This analysis identified {len(multi_ns_genes)} genes with enriched annotations across multiple Gene Ontology aspects.")
output.append("")
output.append("### Enrichment Overview")
output.append("")

# Count by namespace
ns_counts = defaultdict(int)
for cluster in data['clusters']:
    ns = cluster['root_term']['namespace']
    ns_counts[ns] += 1

output.append(f"- **Cellular Component**: {ns_counts['cellular_component']} enriched terms")
output.append(f"- **Molecular Function**: {ns_counts['molecular_function']} enriched terms")
output.append(f"- **Biological Process**: {ns_counts['biological_process']} enriched terms")
output.append("")

# Identify the strongest functional theme
output.append("## Functional Themes")
output.append("")

# Build theme from BP terms
bp_themes = defaultdict(list)
for gene, annots in multi_ns_genes.items():
    if annots['BP']:
        # Group by most significant BP term
        top_bp = min(annots['BP'], key=lambda x: x['fdr'])
        bp_themes[top_bp['term']].append(gene)

# Show top themes
for theme, genes in sorted(bp_themes.items(), key=lambda x: len(x[1]), reverse=True):
    if len(genes) < 3:  # Only show themes with 3+ genes
        continue

    output.append(f"### {theme.title()}")
    output.append("")
    output.append(f"**{len(genes)} genes identified**")
    output.append("")

    # Get common features
    cc_common = defaultdict(int)
    mf_common = defaultdict(int)

    for gene in genes:
        for cc in gene_annotations[gene]['CC']:
            cc_common[cc['term']] += 1
        for mf in gene_annotations[gene]['MF']:
            mf_common[mf['term']] += 1

    # Report common patterns
    if cc_common:
        top_cc, count = max(cc_common.items(), key=lambda x: x[1])
        output.append(f"**Primary Location**: {top_cc} ({count}/{len(genes)} genes)")
        output.append("")

    if mf_common:
        top_mf, count = max(mf_common.items(), key=lambda x: x[1])
        output.append(f"**Primary Function**: {top_mf} ({count}/{len(genes)} genes)")
        output.append("")

    # List genes with integrated annotations
    output.append("**Gene Details:**")
    output.append("")

    for gene in sorted(genes):
        annots = gene_annotations[gene]

        # Build integrated description
        parts = [f"**{gene}**"]

        # Location
        if annots['CC']:
            cc_list = [cc['term'] for cc in sorted(annots['CC'], key=lambda x: x['fdr'])]
            parts.append(f"Located in {cc_list[0]}")

        # Function
        if annots['MF']:
            mf_list = [mf['term'] for mf in sorted(annots['MF'], key=lambda x: x['fdr'])]
            parts.append(f"with {mf_list[0]} activity")

        # Process
        if annots['BP']:
            bp_list = [bp['term'] for bp in sorted(annots['BP'], key=lambda x: x['fdr'])[:2]]
            parts.append(f"involved in {' and '.join(bp_list)}")

        # Combine with proper punctuation
        output.append(f"- {parts[0]}: {', '.join(parts[1:]) if len(parts) > 1 else 'Enriched in this analysis'}.")

    output.append("")

# Add detailed term lists at end
output.append("---")
output.append("")
output.append("## Detailed Enrichment Terms")
output.append("")

for ns_full in ['cellular_component', 'molecular_function', 'biological_process']:
    ns_display = {'cellular_component': 'Cellular Component',
                  'molecular_function': 'Molecular Function',
                  'biological_process': 'Biological Process'}[ns_full]

    output.append(f"### {ns_display}")
    output.append("")

    ns_clusters = [c for c in data['clusters'] if c['root_term']['namespace'] == ns_full]

    if not ns_clusters:
        output.append("*No significant enrichment*")
        output.append("")
        continue

    for cluster in sorted(ns_clusters, key=lambda x: x['root_term']['fdr']):
        rt = cluster['root_term']
        output.append(f"**{rt['name']}** ({rt['go_id']})")
        output.append(f"- FDR: {rt['fdr']:.2e}")
        output.append(f"- Fold Enrichment: {rt['fold_enrichment']:.2f}")
        output.append(f"- Genes ({rt['study_count']}): {', '.join(sorted(rt['study_genes']))}")
        output.append("")

# Write to file
output_file = Path(__file__).parent.parent / "results/example_integrated_report.md"
output_file.write_text('\n'.join(output))

print(f"Generated integrated report: {output_file}")
print("\nFirst 50 lines preview:")
print("="*80)
print('\n'.join(output[:50]))
