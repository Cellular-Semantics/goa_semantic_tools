# Bottom-Up GO Enrichment: Existing Methods, Related Tools, and Best Practices

Your leaf-first clustering approach addresses a well-recognized problem in GO enrichment analysis and shares conceptual elements with several established methods, though your particular combination of features—enrichment leaves, gene-set merging, a 20% novelty threshold, and dual FDR thresholds—appears to be a novel synthesis. Below is a detailed landscape of related work.

## Hierarchy-Aware Enrichment Testing (Most Directly Related)

### topGO: elim and weight Algorithms

The **topGO** Bioconductor package (Alexa et al., 2006) is the closest precursor to your bottom-up philosophy. It implements several algorithms that account for GO DAG structure during the enrichment test itself, rather than post-hoc:[^1][^2]

- **`elim`**: Processes GO terms from bottom to top (leaves first), assessing the most specific terms first. When a GO term is found significantly enriched, the algorithm *removes all genes annotated to that term from its ancestor terms* before testing them. This directly parallels your concept of "enrichment leaves"—the elim method inherently prioritizes leaf-level enrichment and penalizes parents whose significance derives from already-enriched children.[^3][^1]

- **`weight`**: Instead of binary gene removal, this method assigns continuous weights to genes based on the significance of neighbouring GO terms, creating a softer decorrelation than elim.[^4][^3]

- **`weight01`** (default in topGO): A hybrid of elim and weight, combining both strategies.[^2][^5]

- **`parentchild`**: Introduced by Grossmann et al. (2007), this method conditions the enrichment test for a term on the annotations of its parent terms, testing whether a term is enriched *given* that its parents are enriched. It comes in "union" and "intersection" variants.[^6][^7]

**Key difference from your approach**: topGO's elim modifies the statistical test by removing genes from ancestors, but doesn't explicitly identify "enrichment leaves" as a defined concept, doesn't merge siblings by gene-set identity, and doesn't use a novelty threshold (like your 20%) to decide whether to include parent terms.

### evoGO

**evoGO** (2025 preprint, Evotec) is a more recent method built on ORA that reduces the impact of differentially expressed genes on a GO term's significance if those genes already contribute to a *higher significance of any descendant term*. In benchmarks against topGO, clusterProfiler, and SetRank, evoGO reduced enriched terms by ~30% on average while recovering 96% of true positives. Critically, evoGO eliminated the fewest enriched GO terms that had *no significantly enriched relatives*—terms that should not be considered redundant. It is available as an R package on GitHub.[^8][^9][^10]

**Relevance**: evoGO's descendant-aware significance attenuation is conceptually similar to your approach of only including parents if they add >20% new genes. Both methods try to prevent parent terms from "stealing" significance from their more specific descendants.

### MGSA (Model-Based Gene Set Analysis)

**MGSA** (Bauer et al., 2010) takes a fundamentally different approach by analyzing all GO categories simultaneously within a Bayesian network. The model assumes that some gene sets are "active" and that genes belonging to active sets are more likely to appear in the observed list. By fitting all categories at once, MGSA naturally handles overlap between GO terms and substantially reduces redundancy compared to single-category testing methods. On simulated data, MGSA achieved up to 95% precision at 20% recall, yielding a 10-fold improvement over standard enrichment methods.[^11][^12]

**Relevance**: MGSA's simultaneous inference over all sets is philosophically different from your sequential leaf-first approach, but it addresses the same core problem of correlated GO terms producing redundant hits.

### SetRank

**SetRank** (Simillion et al., 2017) discards gene sets initially flagged as significant if their significance is attributable entirely to overlap with another gene set. This directly targets the overlap-driven false positive problem. The algorithm evaluates pairwise overlaps and removes sets whose enrichment disappears when shared genes are accounted for.[^13][^14]

**Relevance**: Your step of merging leaves with identical gene sets and requiring >20% new genes from parents is a related but more structured approach to the same problem SetRank addresses.

### Ontologizer (Parent-Child Methods)

The **Ontologizer** (Bauer et al., 2008) implements the parent-child approach in both "union" and "intersection" variants. The parent-child-union method computes enrichment of a GO term by conditioning on the union of genes annotated to its parents, while parent-child-intersection conditions on the intersection. This directly addresses the "inheritance problem" where parent terms are falsely enriched because they inherit annotations from enriched children.[^15][^6]

## Post-Hoc Semantic Similarity and Clustering (Redundancy Reduction)

These tools operate *after* enrichment testing to reduce redundancy in the result list. They complement hierarchy-aware testing methods and could be layered on top of your leaf-first approach.

### REVIGO

**REVIGO** (Supek et al., 2011) is the most widely used post-hoc redundancy reduction tool. It summarizes GO term lists using a clustering algorithm based on **semantic similarity** (SimRel measure). For each cluster, REVIGO selects a representative term and removes redundant ones based on a user-defined similarity threshold. Notably, REVIGO includes a special rule: when a parent term is composed almost exclusively of a child term (>75%), the parent is rejected instead. It provides four visualization modes: MDS scatterplots, interactive graphs, treemaps, and tag clouds.[^16][^17][^18]

**Relevance**: REVIGO's >75% parent-rejection rule is conceptually related to your >20% novelty threshold—both attempt to filter parents that add minimal information beyond their children. However, REVIGO operates purely on semantic similarity and p-values, not on gene-set membership directly.

### rrvgo

**rrvgo** (Sayols, 2023) is a Bioconductor package that replicates much of REVIGO's functionality programmatically in R. It computes semantic similarity matrices using **GOSemSim** methods (Resnik, Lin, Jiang, Rel, Wang), then groups similar terms and selects representatives. If scores are not provided, rrvgo defaults to using GO term set size, which favors broader terms.[^19][^20][^21]

### simplifyEnrichment (Binary Cut Method)

**simplifyEnrichment** (Gu et al., 2022) proposes a novel "binary cut" algorithm for clustering GO terms from their semantic similarity matrix. It generates word cloud summaries for each cluster, providing an intuitive visual overview. Unlike REVIGO's greedy approach, binary cut performs a more principled partitioning of the similarity matrix.[^22][^23]

### GO-Figure!

**GO-Figure!** (Reijnders & Waterhouse, 2021) is a Python tool that produces semantic similarity scatterplots of redundancy-reduced GO term lists. It groups terms using quantified information content and semantic similarities, with user control over grouping thresholds. Representatives are then plotted in 2D semantic space where similar terms cluster together.[^24][^25]

### clusterProfiler's `simplify()` Function

The widely-used **clusterProfiler** R package includes a `simplify()` method that uses GOSemSim to calculate semantic similarity between enriched GO terms and removes terms with similarity above a cutoff (default 0.7), keeping the most significant representative. A complementary `dropGO()` function allows removal of specific GO terms or entire GO levels. The `emapplot()` function in the enrichplot package can also visualize overlapping gene sets as networks.[^26][^27][^28]

### GO Trimming

**GO Trimming** (Jantzen et al., 2011) is a simpler method that reduces redundancy in enriched GO lists using an algorithm with variable stringency. It reduced a test list of 90 terms to 54 in the published example.[^29]

## Information Content (IC) Based Approaches

Information content quantifies how specific a GO term is, computed as \(-\log(p(t))\) where \(p(t)\) is the frequency of term \(t\) in a reference annotation corpus. More specific (leaf-like) terms have higher IC because they annotate fewer genes.[^30][^31]

| IC Method | Description | Key Property |
|-----------|-------------|--------------|
| **Resnik** | IC of the most informative common ancestor (MICA) of two terms [^32] | Widely used; does not normalize |
| **Lin** | Normalizes Resnik by the sum of ICs of the two terms [^32] | Bounded between 0 and 1 |
| **Jiang-Conrath** | Distance metric based on IC difference [^32] | Converted to similarity |
| **Rel (Relevance)** | Combines Resnik and Lin approaches [^33] | Balances specificity and normalization |
| **Wang** | Graph-based; does not depend on annotation corpus [^32] | Structural similarity only |

**GOSemSim** (Yu et al., 2010) implements all five methods and is the foundational package used by rrvgo, clusterProfiler's `simplify()`, and simplifyEnrichment for computing GO term similarities.[^33][^32]

**Relevance to your approach**: IC can be used as an alternative or complement to your leaf-detection strategy. Terms with high IC are by definition specific, and IC-based filtering naturally favours leaves over general parent terms.

## GO Slims

An alternative strategy for reducing complexity is to use **GO Slims**—curated, shallow subsets of GO that cover all major branches but lack specific terms. While this approach is simpler than hierarchical methods, it sacrifices substantial specificity. Your dual-threshold approach (0.05 strict, 0.10 relaxed) is a more nuanced solution that preserves annotation-depth-dependent specificity.[^34][^35]

## Comparison to Your Approach

| Feature | Your Method | topGO (elim) | evoGO | REVIGO | MGSA | SetRank |
|---------|------------|--------------|-------|--------|------|---------|
| Direction of traversal | Bottom-up (leaf-first) | Bottom-up | Descendant-aware | N/A (post-hoc) | Simultaneous | Pairwise overlap |
| Enrichment leaf identification | Explicit | Implicit | Implicit | No | No | No |
| Sibling merging by gene set | Yes (identical sets) | No | No | Semantic similarity | No | Overlap-based |
| Parent inclusion threshold | >20% new genes | Gene removal | Significance attenuation | >75% overlap rejection [^16] | Bayesian inference | Overlap test |
| Dual FDR thresholds | Yes (0.05/0.10) | No | No | No | No | No |
| Specific vs. category enrichment labels | Yes | No | No | No | No | No |
| Annotation depth sensitivity | Yes (by design) | Partial | Partial | No | No | No |

## Novel Aspects of Your Approach

Several elements of your method appear to be genuinely novel in combination:

- **Explicit "enrichment leaf" identification** as a defined intermediate step, rather than implicitly prioritizing leaves through gene elimination or weighting. While topGO's elim traverses bottom-up, it doesn't formalize the concept of an enrichment leaf.[^1]

- **Gene-set identity merging of siblings** is distinct from semantic similarity clustering (REVIGO/rrvgo) and from overlap-based discounting (SetRank). Testing for *identical* gene sets is a stricter, more interpretable criterion.

- **The 20% novelty threshold for parent inclusion** sits between topGO's binary gene removal and REVIGO's 75% overlap rejection rule. This middle ground could better capture biologically meaningful category-level enrichment.

- **Dual FDR thresholds (0.05/0.10)** to handle variation in annotation depth across branches is a practical innovation not found in current tools. Well-annotated branches naturally produce more specific significant terms at strict thresholds, while sparsely annotated branches may need relaxed thresholds to capture real biology.

- **Classification into "specific enrichment" vs. "category enrichment"** provides users with explicit information about the nature of each result, which existing tools do not systematically offer.

## Practical Recommendations

1. **Benchmark against topGO weight01 and evoGO**: These are the closest algorithmic relatives. Use synthetic datasets with known true positive GO terms (as evoGO did ) and tissue-specific gene sets to compare sensitivity and specificity.[^9]

2. **Layer semantic similarity post-hoc**: Even after your leaf-first procedure, applying rrvgo or REVIGO on the output could further reduce redundancy among unrelated branches.[^19]

3. **Use GOSemSim for the merging step**: Instead of requiring strictly identical gene sets for sibling merging, consider a Jaccard index threshold (e.g., >0.9) or semantic similarity threshold, which would be more robust to minor annotation differences.[^32]

4. **Validate the 20% threshold empirically**: Test a range of thresholds (10%, 20%, 30%) on datasets with known biology to find the optimal balance. REVIGO's 75% threshold for parent rejection serves a different purpose (near-complete redundancy), whereas your 20% targets meaningful parental contribution.

5. **Consider IC as a complementary filter**: Terms with very low IC (highly general terms like "membrane") could be automatically flagged or deprioritized, providing an additional layer to your hierarchy-based filtering.[^30]

6. **Compare with MGSA's Bayesian approach**: MGSA's simultaneous inference over all categories is a fundamentally different paradigm and may serve as a useful upper bound for performance comparison.[^12]

## Key References

- Alexa A, Rahnenführer J, Lengauer T (2006). "Improved scoring of functional groups from gene expression data by decorrelating GO graph structure." *Bioinformatics* 22(13):1600-7 — topGO elim/weight algorithms.[^36]
- Supek F et al. (2011). "REVIGO Summarizes and Visualizes Long Lists of Gene Ontology Terms." *PLoS ONE* 6(7):e21800 — REVIGO semantic clustering.[^18]
- Bauer S et al. (2010). "GOing Bayesian: model-based gene set analysis of genome-scale data." *Nucleic Acids Research* 38(11):3523-32 — MGSA.[^12]
- Grossmann S et al. (2007). "Improved detection of overrepresentation of Gene-Ontology annotations with parent child analysis." *Bioinformatics* — Parent-child methods.[^6]
- Gu Z et al. (2022). "simplifyEnrichment: an R/Bioconductor package for Clustering and Visualizing Functional Enrichment Results." *Genomics, Proteomics & Bioinformatics* — Binary cut clustering.[^22]
- Simillion C et al. (2017). "Avoiding the pitfalls of gene set enrichment analysis with SetRank." *BMC Bioinformatics* — Overlap-aware enrichment.[^13]
- Koopmans F (2024). "GOAT: efficient and robust identification of gene set enrichment." *Communications Biology* 7:744 — Modern preranked enrichment.[^37]
- evoGO (2025 preprint). "Cutting through the clutter: minimizing redundancy in GO enrichment analysis with evoGO." — Descendant-aware ORA.[^10]
- Sayols S (2023). "rrvgo: a Bioconductor package for interpreting lists of Gene Ontology terms." *microPublication Biology* — Programmatic REVIGO alternative.[^19]

---

## References

1. [Using TopGO to test for GO-term enrichment - avrilomics](http://avrilomics.blogspot.com/2015/07/using-topgo-to-test-for-go-term.html) - If you use the weight01 (default), elim or parentchild algorithm, TopGO may report a GO term as sign...

2. [1 Introduction](http://bioconductor.posit.co/packages/release/bioc/vignettes/topGO/inst/doc/topGO_manual.html)

3. [topGO - Bioinformatics DBbioinformaticshome.com › tool › topGO](https://bioinformaticshome.com/db/tool/topGO) - topGO is a software package for enrichment analysis of Gene Ontology (GO) terms using gene expressio...

4. [From a gene list to biological function](https://topgo.bioinf.mpi-inf.mpg.de/docs/stat_comp_2006.pdf)

5. [Gene set enrichment analysis with topGO](https://bioconductor.org/packages/release/bioc/vignettes/topGO/inst/doc/topGO.pdf)

6. [Ontologizer 2.0—a multifunctional tool for GO term enrichment ...](https://academic.oup.com/bioinformatics/article/24/14/1650/182451) - Here, we describe an application that implements not only the standard approach to GO analysis, but ...

7. [Ontologizer](https://cyverse.atlassian.net/wiki/spaces/DEapps/pages/241882173/Ontologizer) - To do a GO enrichment analysis, you need a list of differentially expressed genes, the population (o...

8. [Cutting Through the Clutter: Minimizing Redundancy in GO Enrichment Analysis with evoGO - Evotec](https://www.evotec.com/en/sciencepool/cutting-through-the-clutter-minimizing-redundancy-in-go-enrichment-analysis-with-evogo) - Our findings demonstrate that among tested ORA-based approaches, evoGO stands out as an effective an...

9. [Minimizing Redundancy in GO Enrichment Analysis with evoGO](https://www.evotec.com/sciencepool/cutting-through-the-clutter-minimizing-redundancy-in-go-enrichment-analysis-with-evogo) - We developed evoGO, a novel method that aims to improve the specificity and relevance of enrichment ...

10. [Cutting through the clutter: minimizing redundancy in GO enrichment analysis with evoGO](https://labs.sciety.org/articles/by?article_doi=10.1101%2F2025.02.24.639258) - Gene Ontology (GO) enrichment analysis is a powerful tool for elucidating underlying biological proc...

11. [The mgsa package](https://www.bioconductor.org/packages/devel/bioc/vignettes/mgsa/inst/doc/mgsa.pdf)

12. [GOing Bayesian: model-based gene set analysis of genome-scale ...](https://academic.oup.com/nar/article/38/11/3523/3100635) - Here we present model-based gene set analysis (MGSA) that analyzes all categories at once by embeddi...

13. [Avoiding the pitfalls of gene set enrichment analysis with SetRank.](https://sonar.ch/global/documents/278700) - The SONAR project aims to create a scholarly archive that collects, promotes and preserves the publi...

14. [Gene Set Overlap: An Impediment to Achieving High Specificity in ...](https://www.biorxiv.org/content/10.1101/319145v2.full-text) - In this paper, we propose a systematic approach to investigate the hypothesis that gene set overlap ...

15. [Ontologizer 2.0--a multifunctional tool for GO term ... - PubMed](https://pubmed.ncbi.nlm.nih.gov/18511468/) - The Ontologizer allows users to visualize data as a graph including all significantly overrepresente...

16. [REVIGO Summarizes and Visualizes Long Lists of Gene ...](https://journals.plos.org/plosone/article/figures?id=10.1371%2Fjournal.pone.0021800) - Outcomes of high-throughput biological experiments are typically interpreted by statistical testing ...

17. [REVIGO Summarizes and Visualizes Long Lists of Gene Ontology ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC3138752/) - REVIGO is a Web server that summarizes long, unintelligible lists of GO terms by finding a represent...

18. [REVIGO Summarizes and Visualizes Long Lists of Gene Ontology Terms](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0021800&rut=4c230d4807411a7ffe3937fdfcbc17689fb969759766cfe521adae02ffe1c842) - Outcomes of high-throughput biological experiments are typically interpreted by statistical testing ...

19. [Reduce + Visualize GO • rrvgo - ssayols.github.io](https://ssayols.github.io/rrvgo/) - rrvgo aims at simplifying the redundance of GO sets by grouping similar terms in terms of semantic s...

20. [Using the rrvgo package - Bioconductor](https://bioconductor.org/packages/release/bioc/vignettes/rrvgo/inst/doc/rrvgo.html)

21. [Contents](https://www.bioconductor.org/packages/devel/bioc/vignettes/rrvgo/inst/doc/rrvgo.html)

22. [Simplify Functional Enrichment Results - Zuguang Gu](https://jokergoo.github.io/simplifyEnrichment/) - A new clustering algorithm, "binary cut", for clustering similarity matrices of functional terms is ...

23. [GitHub - jokergoo/simplifyEnrichment: Simplify functional enrichment results](https://github.com/jokergoo/simplifyEnrichment) - Simplify functional enrichment results. Contribute to jokergoo/simplifyEnrichment development by cre...

24. [Frontiers | Summary Visualizations of Gene Ontology Terms With GO-Figure!](https://www.frontiersin.org/journals/bioinformatics/articles/10.3389/fbinf.2021.638255/full) - The Gene Ontology (GO) is a cornerstone of functional genomics research that drives discoveries thro...

25. [Summary Visualizations of Gene Ontology Terms With GO-Figure!](https://pmc.ncbi.nlm.nih.gov/articles/PMC9581009/) - Amongst current visualization tools and resources there is a lack of standalone open-source software...

26. [use simplify to remove redundancy of enriched GO terms](https://guangchuangyu.github.io/2015/10/use-simplify-to-remove-redundancy-of-enriched-go-terms/) - To simplify enriched GO result, we can use slim version of GO and use enricher function to analyze. ...

27. [reduce redundancy of enriched GO terms · Issue #28 · YuLab-SMU/clusterProfiler](https://github.com/YuLab-SMU/clusterProfiler/issues/28) - To simplify the enriched result, we can use slim version of GO and use enricher() function to analyz...

28. [13 Visualization of functional enrichment result - YuLab@SMU](https://yulab-smu.top/biomedical-knowledge-mining-book/enrichplot.html) - Enrichment map organizes enriched terms into a network with edges connecting overlapping gene sets. ...

29. [GO Trimming: Systematically reducing redundancy in large Gene ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC3160396/) - Here we present a simple yet novel method called GO Trimming that utilizes an algorithm designed to ...

30. [Information Content-Based Gene Ontology Semantic ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC3775452/) - Several approaches have been proposed for computing term information content (IC) and semantic simil...

31. [Information Content (IC) of GO terms - Biostars](https://www.biostars.org/p/172279/) - I have downloaded all GO terms of UniProt genes (file). I would like to calculate the Information Co...

32. [GOSemSim](https://www.bioconductor.org/packages/release/bioc/html/GOSemSim.html) - The semantic comparisons of Gene Ontology (GO) annotations provide quantitative ways to compute simi...

33. [1 GO semantic similarity analysis - YuLab@SMU](https://yulab-smu.top/biomedical-knowledge-mining-book/011-GOSemSim.html) - On the basis of semantic similarity between GO terms, GOSemSim can also compute semantic similarity ...

34. [GO Enrichment Analysis - Galaxy Training!](https://training.galaxyproject.org/training-material/topics/transcriptomics/tutorials/goenrichment/tutorial.html) - What are GO annotations? Genes are associated to GO terms via GO annotations. Each gene can have mul...

35. [Automatic, context-specific generation of Gene Ontology slims - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3098080/) - Here we introduce such a method that can generate customised GO slims for specific annotated dataset...

36. [Improved scoring of functional groups from gene expression data by ...](https://academic.oup.com/bioinformatics/article/22/13/1600/193669) - In this article we present two novel methods that improve the enrichment analysis of GO terms by int...

37. [GOAT: efficient and robust identification of gene set enrichment - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11187187/) - We here present GOAT, a novel algorithm for gene set enrichment testing in preranked gene lists that...

