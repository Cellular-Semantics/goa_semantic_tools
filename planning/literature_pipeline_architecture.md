# Literature Pipeline Architecture

**Last updated**: 2026-03-16 (enrichment_strategy branch)

## Pipeline Overview

```
Phase 1:   genes → enrichment                    → _enrichment.json
Phase 1b:  enrichment → literature evidence      → _literature.json
Phase 2:   enrichment + literature → LLM         → _explanation.md
```

CLI runs full pipeline by default. `--stop-after {enrichment,literature}` exits early.
`--enrichment-json` / `--literature-json` resume from intermediates.

---

## Phase 1b: Literature Evidence Gathering

### 1. GAF PMID Selection

**Function**: `get_gaf_pmids_for_themes()` in `reference_retrieval_service.py`

**How it works**:
- For each theme, collects all genes + GO IDs (anchor + specific terms)
- Queries the GAF reference index: finds PMIDs where gene is annotated to a theme GO ID
- **With descendant expansion** (added 2026-03-16): annotations to child GO terms also match
  - Himes dataset: 43 → 197 PMIDs, 11/22 → 20/22 themes covered
- Ranked by: gene coverage count (desc), then PMID recency (desc)
- Top 5 per theme (default)

**Output per PMID**:
```json
{
  "pmid": "18458160",
  "genes_covered": ["KANK1"],
  "go_terms": ["GO:0030336"],
  "gene_go_map": {"KANK1": ["GO:0030336"]},
  "gene_go_named": {"KANK1": ["negative regulation of cell migration [GO:0030336]"]}
}
```

The `gene_go_named` field (resolved in cli.py using godag) lets the LLM see the
actual annotated term, not just a gene name.

### 2. ASTA Snippet Search (Semantic Scholar)

**Requires**: `ASTA_API_KEY` environment variable

**Per-theme** (`fetch_snippets_for_gaf_pmids`):
- Query: anchor term name (e.g. "negative regulation of cell migration")
- **Scoped to GAF PMIDs** via `paper_ids` — only searches within curated papers
- Returns body-text passages (~500 words), filtered by score >= 0.2
- Themes with 0 GAF PMIDs get 0 snippets

**Per hub gene** (`fetch_snippets_for_hub_genes`):
- Query: `"{gene} {top_theme_name}"` (e.g. "FOXO3 negative regulation of cell migration")
- **Unscoped** — searches all of Semantic Scholar
- Top 20 hub genes by theme_count, up to 3 snippets each
- 15s timeout per call

### 3. Europe PMC Abstract Fetch

**For GAF PMIDs** (`fetch_abstracts_for_gaf_pmids`):
- Per-PMID lookup via `get_europepmc_paper_by_id`
- Returns title, abstract, authors, year
- Deduplicates across themes

**For hub genes** (`fetch_abstracts_for_hub_genes`):
- Keyword search: `"{gene} {top_theme_name}"`
- Up to 5 papers per gene, `result_type=core` (includes abstracts)
- Top 20 hub genes

---

## Phase 2: LLM Context & Synthesis

### What the LLM sees per theme

In priority order (additive — theme can have both):

1. **ASTA snippets** ("Available Evidence Snippets"):
   ```
   [PMID:18458160] Paper Title — Authors
   Evidence: <first 600 chars of body text passage>
   ```
   Self-describing — the text contains the biology.

2. **GAF citations** ("Available GAF Citations"):
   ```
   [PMID:18458160] Paper Title — Authors (Year)
   Annotates: KANK1→negative regulation of cell migration [GO:0030336]
   Abstract: <first 400 chars>
   ```
   Shows the specific gene→GO annotation the paper supports.

### What the LLM sees per hub gene

ASTA snippets (preferred) OR Europe PMC abstracts, showing cross-theme evidence.

### Prompt instructions (go_explanation.prompt.yaml)

- "Only cite PMIDs that appear in the provided citations"
- "Do NOT generate numbered references or bibliography"
- "Place citations directly inside the tagged sentence"
- Provenance tags: [DATA], [GO-HIERARCHY], [INFERENCE], [EXTERNAL]

---

## Co-annotation Patterns (discovered 2026-03-16)

### Within-theme: same gene → 2+ GO terms

A paper annotating VEGFA to both "pos reg sprouting angiogenesis migration" and
"pos reg trophoblast migration" under the same theme tells a story about how a
gene participates in multiple sub-processes.

- Himes dataset: 14 such gene×PMID pairs (uncapped)
- Already visible via `Annotates:` format (shows both terms)
- Could highlight with explicit tag

### Cross-theme: same PMID spanning multiple themes

A paper appearing under 2+ themes links those themes mechanistically.
E.g. PMID:16814735 spans 5 themes (fatty acid oxidation, oxygen response,
nitrogen response, chemical homeostasis, glucose transport).

- Himes dataset: 28 cross-theme PMIDs
- Especially valuable for hub genes section (evidence for coordination)
- **Not yet surfaced** — plan to add to hub gene context

---

## Known Issues & Gaps

### PMID Hallucination (critical)

The LLM generates fake PMIDs (9+ digit numbers) when no real citation is available.
**No validation exists** — `_add_pmid_hyperlinks` just linkifies any `PMID:\d+`.

Potential fixes (cheapest first):
1. **Format check**: Real PMIDs are 1-8 digits. Flag/strip 9+ digit PMIDs.
2. **Grounding check**: Collect all PMIDs from literature context; any output PMID
   not in that set is ungrounded → strip or warn.
3. **Schema-level field**: Add `pmids_cited: list[str]` per theme — easier to validate
   than mining free text.
4. **LLM correction loop**: Send failing themes back with "you cited PMID:X but it
   was not in your context."
5. **PubMed existence check**: Verify via Europe PMC API (adds latency).

### Validator gaps

`validate_explanation_json` only checks:
- Gene names in `key_genes` against theme gene lists
- GO IDs in `key_genes`/`key_insights` against theme GO IDs

Does NOT check:
- PMIDs (anywhere)
- Hub genes section
- Overall summary
- Narrative free text
- Provenance tag correctness
- `_validate_citations` exists but is **dead code** (never called)

### ASTA per-theme scoping limitation

Per-theme ASTA snippets are scoped to GAF PMIDs. This means:
- Themes with 0 GAF PMIDs get 0 snippets
- Even with descendant expansion, 2/22 Himes themes have no GAF PMIDs
- Hub gene ASTA search is unscoped and partially compensates

### Snippet coverage concern

When querying for co-annotation (gene annotated to two GO terms), a single
snippet may not cover both processes. Options:
- Query for each GO term independently, rely on LLM synthesis to stitch
- Query with both terms, accept that some stories fall between snippets
- Accept this limitation — abstracts still provide the link even if no
  single snippet covers both

---

## Planned Improvements

### Near-term (this branch)

- [ ] **Cross-theme PMID surfacing for hub genes**: When a GAF PMID appears in
  2+ themes for the same gene, surface it in the hub gene section with the
  theme-linking context. Use as ASTA snippet query too.

- [ ] **PMID hallucination check**: At minimum, format check (≤8 digits) +
  grounding check (PMID must be in provided literature context).

### Medium-term

- [ ] **Co-annotation ASTA queries**: For within-theme multi-GO annotations,
  query ASTA with both GO term names to find linking passages.

- [ ] **LLM correction loop**: Re-call LLM with validation failures for
  1-2 retry rounds (bounded cost). Especially useful for cheaper models
  (gpt-4o-mini) that hallucinate more.

- [ ] **Raise GAF top_n for cross-theme PMIDs**: Currently top_n=5 per theme.
  Cross-theme PMIDs are high-value; could preferentially include them even
  if they rank lower within a single theme.

### Longer-term

- [ ] **Activate `_validate_citations`**: Dead code that cross-checks GO IDs
  in narrative text. Wire it up.

- [ ] **Hub gene validation**: Extend `validate_explanation_json` to check
  hub_genes entries.

- [ ] **Structured PMID field in schema**: Add `pmids_cited` to the JSON schema
  so PMIDs are machine-parseable, not buried in free text.
