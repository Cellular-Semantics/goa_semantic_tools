# Plan: `--exploratory` flag for sub-threshold GO annotation discovery

> Full implementation plan: `~/.claude/plans/lucky-sauteeing-aurora.md`

## Context

Enrichment p-values can give false confidence: enrichment doesn't mean all necessary components are present, and lack of enrichment doesn't mean unimportant (a single rate-limiting gene may suffice). To help researchers explore beyond statistical thresholds, we add an opt-in `--exploratory` flag that surfaces child GO terms beneath significantly enriched anchors that have gene overlap with the input list but didn't reach FDR significance. These are presented as structured leads, not as findings.

## Design Decisions

- **No second p-value cutoff** -- enumerate children with >= 1 input gene
- **Report gene counts and overlap proportion**, not p-values
- **Top 5 children** per enriched parent, ranked by overlap proportion (input genes / total annotated)
- **Clearly separated section** in report, flagged as exploratory
- **Opt-in** via `--exploratory` CLI flag
- **New `[EXPLORATORY]` provenance tag** distinct from the existing four

## Key Insight

`goea_results_all` (all tested GO terms from GOATOOLS) is already computed in `run_go_enrichment()` but only significant results are retained. The sub-threshold terms are available -- we just need to filter them to children of enriched anchors that have gene overlap.

## Files to Modify

| File | Change |
|------|--------|
| `src/.../utils/go_hierarchy.py` | Add `ExploratoryChild` dataclass + `compute_exploratory_children()` |
| `src/.../services/go_enrichment_service.py` | Add `exploratory` param, wire up computation, update `_build_output` |
| `src/.../services/go_markdown_explanation_service.py` | Add exploratory section to LLM context, update citation validation + tag counting |
| `src/.../services/go_explanation.prompt.yaml` | Add `[EXPLORATORY]` tag definition and handling instructions |
| `src/.../cli.py` | Add `--exploratory` flag, pass through, update dry-run + summary |
| `src/.../utils/__init__.py` | Export new symbols |

All paths under `src/goa_semantic_tools/goa_semantic_tools/`.

## Algorithm

For each enriched theme anchor:
1. Get all descendants via existing `get_all_descendants(anchor_id, godag)`
2. Filter to sub-threshold results from `goea_results_all`: `p_fdr_bh >= fdr_threshold` AND `len(study_items) >= 1`
3. Compute `overlap_proportion = len(study_items) / ratio_in_pop[0]`
4. Sort by overlap_proportion descending, take top 5
5. Skip anchors with 0 qualifying children

## Output Structure (JSON)

New top-level key `"exploratory_terms"` in enrichment JSON:
```json
{
  "exploratory_terms": [
    {
      "parent_go_id": "GO:0006954",
      "parent_name": "inflammatory response",
      "children": [
        {
          "go_id": "GO:0071222",
          "name": "cellular response to lipopolysaccharide",
          "namespace": "biological_process",
          "depth": 6,
          "input_genes": ["IL1B", "IL6"],
          "input_gene_count": 2,
          "total_annotated_genes": 153,
          "overlap_proportion": 0.013
        }
      ]
    }
  ]
}
```

## Future Considerations

- Semantic clustering of exploratory terms (reduce redundancy across anchors)
- A child term may appear under multiple enriched parents -- currently allowed (context differs)
- Could eventually fold in other evidence types beyond enrichment to support these leads