---
name: explain-enrichment
description: Generate a literature-grounded GO enrichment explanation from an enrichment JSON file. Argument: path to *_enrichment.json
---

> **EXPERIMENTAL — may not reflect current programmatic pipeline**
> This skill is a prototype of the Phase 1b + Phase 2 pipeline implemented in
> `go_markdown_explanation_service.py` + `artl_literature_service.py`. It was
> useful for rapid design iteration but is not actively maintained in sync with
> the Python implementation. Behaviour, output format, and literature search
> strategy may differ from the CLI (`goa-semantic-tools --explain --add-references`).
> For production use, prefer the CLI. Treat output from this skill as indicative only.

# Explain Enrichment Skill

Generate a structured, literature-cited biological explanation for a GO enrichment analysis result. This skill replicates the Python pipeline's Phase 1b + Phase 2 but runs **all Europe PMC searches in parallel** (one response turn), then synthesises into a structured markdown report.

## Input

Enrichment JSON file: **$ARGUMENTS**

---

## Instructions

### Step 1 — Read the enrichment JSON (and optional sidecar files)

Read the file at `$ARGUMENTS`. Extract:
- `metadata` — study parameters (species, gene counts, FDR threshold)
- `themes` — array of theme objects (use up to 15)
- `hub_genes` — dict of `{gene: {theme_count, themes: [...]}}` (use top 20 by `theme_count`)
- `enrichment_leaves` — most specific enriched terms

**Also try to read the GAF PMIDs sidecar file** — derive its path by replacing `_enrichment.json` with `_gaf_pmids.json` in `$ARGUMENTS`. If it exists, load it as `gaf_pmids` (a dict mapping string theme index → list of `{pmid, genes_covered}` dicts). This file is produced automatically by the Python pipeline whenever `--add-references` is used. If it does not exist, `gaf_pmids` is empty and Europe PMC results alone will be used.

For **each theme**, compute ranked candidate key genes to use both as search keywords and as the only valid pool for `key_genes` in the output:
- Collect all genes from `anchor_term.genes` and all `specific_terms[].genes`
- Score each gene: `score = (count_of_specific_terms_containing_gene × 2.0) + (1.0 / theme_count_in_hub_genes_or_1)`
- Sort descending; take top 8 as candidates

---

### Step 2 — Fetch literature evidence (single parallel burst)

Issue **all** searches simultaneously in a single response. If the ASTA (Semantic Scholar) MCP server is available, use snippet_search for richer evidence. Otherwise, fall back to Europe PMC abstracts.

**2a — ASTA snippet search (preferred, if `mcp__Asta__snippet_search` is available):**

Per theme (with GAF PMIDs from sidecar):
```
mcp__Asta__snippet_search(
  query: "{anchor_term.name}"
  paper_ids: "PMID:{pmid1},PMID:{pmid2},PMID:{pmid3}"
  limit: 3
)
```

Per hub gene (top 20 by `theme_count`, unscoped discovery):
```
mcp__Asta__snippet_search(
  query: "{gene_symbol} {gene_data.themes[0]}"
  limit: 3
)
```

All calls in parallel (single response turn). Store snippet results keyed by theme index / gene symbol.

**2b — Europe PMC fallback (if ASTA not available):**

**Per hub gene** (top 20 by `theme_count`):
```
search_europepmc_papers(
  keywords: "{gene_symbol} {gene_data.themes[0]}"
  max_results: 5
  result_type: "core"
)
```
Where `gene_data.themes[0]` is the first theme name listed for that hub gene.

Store the results keyed by gene symbol. You will use them in Step 4 (Hub Genes section) only.

---

### Step 3 — Explain each theme (loop, one theme per iteration)

Repeat the following for **each theme** i = 0 … N−1 in order:

**3a — Fetch this theme's GAF abstracts (parallel within this turn):**

If `gaf_pmids[str(i)]` is non-empty, issue up to **3** `get_europepmc_paper_by_id` calls in parallel (one per PMID, highest-coverage PMIDs first):
```
get_europepmc_paper_by_id(identifier="{pmid}")
```
If `gaf_pmids` is empty or the sidecar was absent, skip — the theme has no GAF literature.

**3b — Generate this theme's explanation:**

Using only the data in scope (theme i's enrichment fields + the fetched abstracts from 3a), generate the JSON object for this theme:

```json
{
  "theme_index": {i},
  "narrative": "2-3 sentences. EVERY sentence tagged [DATA], [GO-HIERARCHY], [INFERENCE], or [EXTERNAL].",
  "key_insights": [{"insight": "≥20 chars", "go_id": "GO:0000000"}],
  "key_genes": [{"gene": "GENE1", "go_id": "GO:0000000", "description": "≥20 chars ≤200 chars", "claim_type": "EXTERNAL"}],
  "statistical_context": "One sentence with exact FDR, fold enrichment, gene count."
}
```

**Context available for 3b:**
```
## Theme {i+1}: {anchor_term.name}
- theme_index: {i}
- GO ID: {anchor_term.go_id}  Namespace: {anchor_term.namespace}
- FDR: {anchor_term.fdr:.2e}  Fold enrichment: {anchor_term.fold_enrichment:.1f}x
- Genes ({count}): {first 10 sorted}

### Specific Terms ({count})
  - {name} ({go_id}): FDR={fdr:.2e}, {n} genes: {first 8 sorted}

### Candidate Key Genes (select key_genes ONLY from this list):
  1. {gene}  [in {n} specific term(s), {n_themes} theme(s), score: {score:.2f}]
  ...

### Available Evidence Snippets (from ASTA, prefer these for citations):
  [only if ASTA snippet_search returned results for this theme:]
  [PMID:{pmid}] {title} — {authors}
  Evidence: {snippet_text, first 600 chars}...

### Available GAF Literature (cite as PMID:xxxxx):
  [only if gaf_pmids fetched above; include for each fetched paper:]
  [PMID:{pmid}] {title} — {authors} ({year})
  Covers: {genes_covered from gaf_pmids entry, up to 6}
  Abstract: {first 400 chars}...
```

Collect each theme's JSON object as you go. Do **not** keep the fetched abstracts in your working memory after generating that theme's explanation — you only need the JSON output.

---

### Step 4 — Generate the hub genes and overall summary

Using the hub gene abstracts fetched in Step 2, generate:

```json
{
  "hub_genes": [
    {"gene": "GENE1", "narrative": "1-2 sentences ≥30 chars ≤300 chars", "claim_type": "EXTERNAL"}
  ],
  "overall_summary": ["Paragraph 1", "Paragraph 2", "Paragraph 3", "Paragraph 4 — limitations"]
}
```

**Context available:**
```
# Study Overview
- Species / input genes / FDR / theme count / hub gene count

# Hub Genes
## {GENE} ({theme_count} themes)
- Themes: {comma-separated, up to 5}
### Supporting Literature:
[PMID:{pmid}] {title} — {authors} ({year})
Abstract: {first 400 chars}...
```

---

### Step 5 — Assemble and validate the full explanation

Combine all per-theme JSON objects from Step 3 with the hub_genes and overall_summary from Step 4 into:

```json
{
  "themes": [ /* from Step 3 */ ],
  "hub_genes": [ /* from Step 4 */ ],
  "overall_summary": [ /* from Step 4 */ ]
}
```

Apply the CRITICAL RULES below, then render to markdown and write the output file.

---

**CRITICAL RULES — apply throughout Steps 3 and 4:**

1. **Provenance tags**: Tag EVERY sentence in `narrative` and hub gene `narrative` with exactly one:
   - `[DATA]` — derived directly from enrichment statistics
   - `[GO-HIERARCHY]` — about GO parent/child relationships
   - `[INFERENCE]` — mechanistic interpretation beyond raw numbers
   - `[EXTERNAL]` — requires literature or prior biological knowledge

2. **key_genes**: Select ONLY from the "Candidate Key Genes" list for that theme. NEVER introduce gene symbols from training knowledge. 2–5 genes per theme.

3. **key_insights**: Reference only GO IDs present in that theme's `anchor_term.go_id` or `specific_terms[].go_id`. Pattern: `^GO:\d{7}$`. 2–4 per theme.

4. **hub_genes**: Only include genes listed in the input `hub_genes` dict.

5. **Citations**: Only cite PMIDs that appear in the fetched evidence (ASTA snippets, GAF literature, or Europe PMC search results). Prefer citing PMIDs from evidence snippets (body-text passages with specific experimental detail) over abstract-only citations. GAF PMIDs support `[DATA]`/`[EXTERNAL]` claims about specific gene→GO annotations; hub gene PMIDs support broader `[EXTERNAL]` claims about cross-theme coordination. Place inline after the claim: `[EXTERNAL] IL6 coordinates inflammation PMID:20027291.` Do NOT create `[1]`, `[2]` numbered references or a bibliography.

6. **overall_summary**: Array of 3–4 strings (paragraphs). Each paragraph ≥50 chars. Last paragraph must address limitations or caveats. No subheadings — continuous prose.

---

### Step 6 — Render to markdown and write output

Render the structured explanation to markdown following this exact structure:

```markdown
# GO Enrichment Analysis Report — {species}

### Theme 1: {anchor_name}

**Summary:** {anchor_name} ([GO:XXXXXXX](http://purl.obolibrary.org/obo/GO_XXXXXXX))

{narrative}

**Key Insights:**
- {insight} ([GO:XXXXXXX](http://purl.obolibrary.org/obo/GO_XXXXXXX))

**Key Genes:**
- **{GENE}**: [{claim_type}] {description} ([GO:XXXXXXX](http://purl.obolibrary.org/obo/GO_XXXXXXX))

**Statistical Context:** {statistical_context}

---

[... repeat for each theme ...]

## Hub Genes

- **{GENE}**: [{claim_type}] {narrative}

## Overall Summary

{paragraph 1}

{paragraph 2}

{paragraph 3}

{paragraph 4 — limitations}
```

**Hyperlink rules:**
- Convert every GO ID to a link: `[GO:0001234](http://purl.obolibrary.org/obo/GO_0001234)` (replace `:` with `_` in the path)
- Convert every PMID citation to a link: `[PMID:12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/)`

**Output path:** Derive from the input argument by replacing the `_enrichment.json` suffix with `_claude_explanation.md`. If the argument doesn't end in `_enrichment.json`, append `_claude_explanation.md` to the base name.

Write the final markdown to that path.

---

## Output Summary

After writing the file, print a brief summary:
- Output path
- Number of themes explained
- Number of hub genes included
- Total PMID citations used (count unique PMIDs cited)
- Whether GAF PMIDs sidecar was found and used; how many unique PMIDs were fetched
- Any themes where no GAF literature was found (gaf_pmids empty or sidecar absent)
