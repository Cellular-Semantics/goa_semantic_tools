# Secondary Theme Membership — Findings and Potential Uses

**From**: exploration/13b_mrcea_all_paths.py secondary membership analysis
**Dataset**: hallmark_inflammatory_response (200 genes, 253 BP leaves, MRCEA-B min_ic=3.0)

---

## What secondary membership is

After the greedy primary assignment (each leaf → one anchor), secondary membership = all other
selected primary anchors that are also ancestors of the leaf. Capped at 3 per leaf, ranked by IC.

---

## Key findings

**Secondary membership is sparse** — only 20/253 leaves have any secondary membership:
- 233 leaves: 0 secondary memberships
- 13 leaves: 1 secondary membership
- 6 leaves: 2 secondary memberships
- 1 leaf: 3 secondary memberships (capped)

**Stranded leaves are not rescued by secondary membership** — this is structural.
A stranded leaf is one whose ancestors were never selected as primary anchors
(they didn't have ≥2 uncovered leaves when the greedy algorithm reached them).
For a stranded leaf to get a secondary membership, its ancestor would have to have
been selected as a primary anchor — but then the leaf itself would have been covered
primarily. Stranded ↔ secondary-member are mutually exclusive under the current scheme.

**Themes with most secondary members:**
| Theme | Secondary | Primary |
|---|---|---|
| cell development | 12 | 2 |
| lymphocyte activation | 10 | 3 |
| cell-cell adhesion | 3 | 6 |
| cellular response to molecule of bacterial origin | 2 | 3 |

"Cell development" and "lymphocyte activation" attract many secondary leaves — these are
broad integrating terms that many specific processes point up to. They're not good primary
anchors (low IC×coverage score) but they represent genuine cross-cutting biology.

**Genes with secondary theme exposure:**
| Gene | Secondary themes | Primary themes | Note |
|---|---|---|---|
| IL12B | 3 | 5 | Interface: inflammasome + adaptive immunity |
| IL18 | 3 | 9 | IL-1 family, appears in multiple signalling contexts |
| NLRP3 | 3 | 3 | Inflammasome — genuine multi-process role |
| ICOSLG | 3 | 3 | T cell co-stimulation — spans activation + adhesion |
| IL6 | 2 | 17 | Despite being biggest hub, low secondary — already primary everywhere |

---

## Potential use for hub gene ranking and explanation

**Current hub gene metric**: count of primary themes a gene appears in. IL6 = 17, IL18 = 9.
This is a proxy for biological centrality but conflates two things:
1. Genes that appear in many themes because they're annotated to many GO terms (annotation breadth)
2. Genes that genuinely operate at the interface of distinct biological processes

**Secondary membership enables a cleaner distinction:**
- `primary_theme_count` — how many distinct biological processes the gene is a primary driver of
- `secondary_theme_count` — how many additional biological contexts the gene participates in

A gene with high primary + high secondary (e.g. IL18: 9 primary, 3 secondary) is a true
cross-pathway hub — its activity touches multiple distinct biological stories.
A gene with high primary + low secondary (e.g. IL6: 17 primary, 2 secondary) is a deeply
embedded hub within one biological area — annotated broadly within immune signalling but not
genuinely operating across distinct process families.

**For explanation**: secondary theme membership could inform the hub gene narrative:
> "IL18 is a cross-pathway hub, driving inflammasome assembly (primary) while also contributing
> to adaptive immune activation and IL-1 signalling (secondary contexts)."
vs.
> "IL6 is a core cytokine hub, deeply embedded across inflammatory signalling."

This is a richer characterisation than just counting themes.

**Practical caveat**: secondary memberships are sparse in this dataset (only 20 leaves affected).
The metric would be more informative with a larger gene set or with min_leaves=1 relaxed
to allow broader anchor selection. Worth revisiting after enrichment algorithm improvements
produce cleaner primary themes.

---

## Decision: defer to post-enrichment-strategy phase

Secondary memberships are currently too sparse to change the explanation pipeline.
Add to the data structure as metadata now; revisit for explanation use once theme
count and quality are improved by the MRCEA-B / IC-based algorithm changes.
