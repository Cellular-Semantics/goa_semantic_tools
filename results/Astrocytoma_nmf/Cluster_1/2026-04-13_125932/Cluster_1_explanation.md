# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_1_themes.csv](Cluster_1_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-response-to-endogenous-stimulus) | [response to endogenous stimulus](#theme-1-response-to-endogenous-stimulus) [GO:0009719](http://purl.obolibrary.org/obo/GO_0009719) | BP | 1.40e-06 | 28 | FDR<0.01 |
| [2](#theme-2-regulation-of-locomotion) | [regulation of locomotion](#theme-2-regulation-of-locomotion) [GO:0040012](http://purl.obolibrary.org/obo/GO_0040012) | BP | 3.40e-06 | 30 | FDR<0.01 |
| [3](#theme-3-transcription-factor-ap-1-complex) | [transcription factor AP-1 complex](#theme-3-transcription-factor-ap-1-complex) [GO:0035976](http://purl.obolibrary.org/obo/GO_0035976) | CC | 1.79e-05 | 4 | FDR<0.01 |
| [4](#theme-4-cellular-response-to-cytokine-stimulus) | [cellular response to cytokine stimulus](#theme-4-cellular-response-to-cytokine-stimulus) [GO:0071345](http://purl.obolibrary.org/obo/GO_0071345) | BP | 2.58e-05 | 15 | FDR<0.01 |
| [5](#theme-5-intracellular-signaling-cassette) | [intracellular signaling cassette](#theme-5-intracellular-signaling-cassette) [GO:0141124](http://purl.obolibrary.org/obo/GO_0141124) | BP | 4.14e-05 | 35 | FDR<0.01 |
| [6](#theme-6-enzyme-linked-receptor-protein-signaling-pathway) | [enzyme-linked receptor protein signaling pathway](#theme-6-enzyme-linked-receptor-protein-signaling-pathway) [GO:0007167](http://purl.obolibrary.org/obo/GO_0007167) | BP | 5.89e-05 | 20 | FDR<0.01 |
| [7](#theme-7-negative-regulation-of-apoptotic-process) | [negative regulation of apoptotic process](#theme-7-negative-regulation-of-apoptotic-process) [GO:0043066](http://purl.obolibrary.org/obo/GO_0043066) | BP | 9.06e-05 | 23 | FDR<0.01 |
| [8](#theme-8-growth-factor-binding) | [growth factor binding](#theme-8-growth-factor-binding) [GO:0019838](http://purl.obolibrary.org/obo/GO_0019838) | MF | 9.90e-05 | 11 | FDR<0.01 |
| [9](#theme-9-dna-binding-transcription-activator-activity-rna-polymerase-ii-specific) | [DNA-binding transcription activator activity, RNA polymerase II-specific](#theme-9-dna-binding-transcription-activator-activity-rna-polymerase-ii-specific) [GO:0001228](http://purl.obolibrary.org/obo/GO_0001228) | MF | 9.90e-05 | 19 | FDR<0.01 |
| [10](#theme-10-positive-regulation-of-monocyte-aggregation) | [positive regulation of monocyte aggregation](#theme-10-positive-regulation-of-monocyte-aggregation) [GO:1900625](http://purl.obolibrary.org/obo/GO_1900625) | BP | 1.54e-04 | 3 | FDR<0.01 |
| [11](#theme-11-positive-regulation-of-mirna-transcription) | [positive regulation of miRNA transcription](#theme-11-positive-regulation-of-mirna-transcription) [GO:1902895](http://purl.obolibrary.org/obo/GO_1902895) | BP | 1.54e-04 | 7 | FDR<0.01 |
| [12](#theme-12-membrane-raft) | [membrane raft](#theme-12-membrane-raft) [GO:0045121](http://purl.obolibrary.org/obo/GO_0045121) | CC | 1.81e-04 | 14 | FDR<0.01 |
| [13](#theme-13-cell-cell-adhesion) | [cell-cell adhesion](#theme-13-cell-cell-adhesion) [GO:0098609](http://purl.obolibrary.org/obo/GO_0098609) | BP | 3.18e-04 | 18 | FDR<0.01 |
| [14](#theme-14-regulation-of-response-to-external-stimulus) | [regulation of response to external stimulus](#theme-14-regulation-of-response-to-external-stimulus) [GO:0032101](http://purl.obolibrary.org/obo/GO_0032101) | BP | 3.82e-04 | 26 | FDR<0.01 |
| [15](#theme-15-glutamatergic-synapse) | [glutamatergic synapse](#theme-15-glutamatergic-synapse) [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) | CC | 4.74e-04 | 19 | FDR<0.01 |
| [16](#theme-16-positive-regulation-of-transcription-by-rna-polymerase-ii) | [positive regulation of transcription by RNA polymerase II](#theme-16-positive-regulation-of-transcription-by-rna-polymerase-ii) [GO:0045944](http://purl.obolibrary.org/obo/GO_0045944) | BP | 4.97e-04 | 28 | FDR<0.01 |
| [17](#theme-17-basement-membrane) | [basement membrane](#theme-17-basement-membrane) [GO:0005604](http://purl.obolibrary.org/obo/GO_0005604) | CC | 6.54e-04 | 8 | FDR<0.01 |
| [18](#theme-18-cell-surface) | [cell surface](#theme-18-cell-surface) [GO:0009986](http://purl.obolibrary.org/obo/GO_0009986) | CC | 7.60e-04 | 20 | FDR<0.01 |
| [19](#theme-19-protease-binding) | [protease binding](#theme-19-protease-binding) [GO:0002020](http://purl.obolibrary.org/obo/GO_0002020) | MF | 8.34e-04 | 10 | FDR<0.01 |
| [20](#theme-20-cytokine-binding) | [cytokine binding](#theme-20-cytokine-binding) [GO:0019955](http://purl.obolibrary.org/obo/GO_0019955) | MF | 8.34e-04 | 10 | FDR<0.01 |
| [21](#theme-21-filopodium-membrane) | [filopodium membrane](#theme-21-filopodium-membrane) [GO:0031527](http://purl.obolibrary.org/obo/GO_0031527) | CC | 1.99e-03 | 4 | FDR<0.01 |
| [22](#theme-22-blood-vessel-morphogenesis) | [blood vessel morphogenesis](#theme-22-blood-vessel-morphogenesis) [GO:0048514](http://purl.obolibrary.org/obo/GO_0048514) | BP | 2.19e-03 | 19 | FDR<0.01 |
| [23](#theme-23-podosome) | [podosome](#theme-23-podosome) [GO:0002102](http://purl.obolibrary.org/obo/GO_0002102) | CC | 3.17e-03 | 5 | FDR<0.01 |
| [24](#theme-24-response-to-oxygen-containing-compound) | [response to oxygen-containing compound](#theme-24-response-to-oxygen-containing-compound) [GO:1901700](http://purl.obolibrary.org/obo/GO_1901700) | BP | 4.04e-03 | 27 | FDR<0.01 |
| [25](#theme-25-regulation-of-epithelial-cell-proliferation) | [regulation of epithelial cell proliferation](#theme-25-regulation-of-epithelial-cell-proliferation) [GO:0050678](http://purl.obolibrary.org/obo/GO_0050678) | BP | 4.45e-03 | 11 | FDR<0.01 |
| [26](#theme-26-cell-matrix-adhesion) | [cell-matrix adhesion](#theme-26-cell-matrix-adhesion) [GO:0007160](http://purl.obolibrary.org/obo/GO_0007160) | BP | 4.74e-03 | 7 | FDR<0.01 |
| [27](#theme-27-positive-regulation-of-intracellular-signal-transduction) | [positive regulation of intracellular signal transduction](#theme-27-positive-regulation-of-intracellular-signal-transduction) [GO:1902533](http://purl.obolibrary.org/obo/GO_1902533) | BP | 4.95e-03 | 24 | FDR<0.01 |
| [28](#theme-28-network-forming-collagen-trimer) | [network-forming collagen trimer](#theme-28-network-forming-collagen-trimer) [GO:0098642](http://purl.obolibrary.org/obo/GO_0098642) | CC | 5.50e-03 | 3 | FDR<0.01 |
| [29](#theme-29-response-to-mechanical-stimulus) | [response to mechanical stimulus](#theme-29-response-to-mechanical-stimulus) [GO:0009612](http://purl.obolibrary.org/obo/GO_0009612) | BP | 5.93e-03 | 9 | FDR<0.01 |
| [30](#theme-30-positive-regulation-of-osteoblast-proliferation) | [positive regulation of osteoblast proliferation](#theme-30-positive-regulation-of-osteoblast-proliferation) [GO:0033690](http://purl.obolibrary.org/obo/GO_0033690) | BP | 6.24e-03 | 3 | FDR<0.01 |

---

### Theme 1: response to endogenous stimulus

**Summary:** response to endogenous stimulus ([GO:0009719](http://purl.obolibrary.org/obo/GO_0009719))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.40e-06 · **Genes (28)**: ARID5A, BTG2, CCL2, CD44, CITED1, COL4A2, DUSP1, EDNRA, EGR1, EGR3, FOS, FOSB, HAS2, IGFBP7, IRS2 … (+13 more)

---

### Theme 2: regulation of locomotion

**Summary:** regulation of locomotion ([GO:0040012](http://purl.obolibrary.org/obo/GO_0040012))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 3.40e-06 · **Genes (30)**: ADAMTS9, ANO6, CCL2, CCN1, CDH11, CLIC4, DUSP1, F3, FN1, FRMD5, GADD45A, GLUL, HAS2, HIF1A, IL6R … (+15 more)

---

### Theme 3: transcription factor AP-1 complex

**Summary:** transcription factor AP-1 complex ([GO:0035976](http://purl.obolibrary.org/obo/GO_0035976))  · Anchor confidence: **FDR<0.01**

[INFERENCE] The AP‑1 complex operates as a dimeric transcriptional hub that integrates stress and receptor signals to reprogram gene expression. [DATA] JUN, JUNB, and FOS localize to the transcription factor AP‑1 complex and drive RNA polymerase II activation at TRE/AP‑1 elements [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/). [EXTERNAL] AP‑1 cooperates with Smad3/4 to potentiate TGF‑beta‑induced transcription, linking enzyme‑linked receptor signaling to immediate gene activation [PMID:9732876](https://pubmed.ncbi.nlm.nih.gov/9732876/). [EXTERNAL] Environmental stressors can selectively modulate AP‑1 subunits, with presenilin‑1 suppressing c‑Jun and JunD but sparing JunB activity, shaping stimulus‑specific outputs [PMID:10117070](https://pubmed.ncbi.nlm.nih.gov/10117070/).

#### Key Insights

- [EXTERNAL] AP‑1 dimers couple MAPK input to Smad‑dependent transcription, aligning stress signals with TGF‑beta gene programs [PMID:9732876](https://pubmed.ncbi.nlm.nih.gov/9732876/). ([GO:0035976](http://purl.obolibrary.org/obo/GO_0035976))
- [DATA] Distinct AP‑1 subunits occupy the transcription factor AP‑1 complex to differentially regulate target promoters in response to stress and cytokines [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/). ([GO:0035976](http://purl.obolibrary.org/obo/GO_0035976))

#### Key Genes

- **JUN**: [EXTERNAL] [DATA] JUN forms AP‑1 dimers and co‑activates TGF‑beta/Smad transcription, integrating MAPK cues with receptor signaling [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/), [PMID:9732876](https://pubmed.ncbi.nlm.nih.gov/9732876/). ([GO:0035976](http://purl.obolibrary.org/obo/GO_0035976))
- **FOS**: [EXTERNAL] [DATA] FOS dimerizes with JUN to activate TRE‑containing promoters as part of the AP‑1 complex in response to diverse stimuli [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/). ([GO:0035976](http://purl.obolibrary.org/obo/GO_0035976))
- **JUNB**: [EXTERNAL] [EXTERNAL] JUNB sustains AP‑1 transactivation even when presenilin‑1 suppresses other AP‑1 members, preserving specific transcriptional outputs [PMID:10117070](https://pubmed.ncbi.nlm.nih.gov/10117070/). ([GO:0035976](http://purl.obolibrary.org/obo/GO_0035976))
- **FOSL2**: [EXTERNAL] [EXTERNAL] FOSL2 partners with JUN family proteins to drive AP‑1‑dependent genes under cytokine and stress signaling [PMID:16327802](https://pubmed.ncbi.nlm.nih.gov/16327802/). ([GO:0035976](http://purl.obolibrary.org/obo/GO_0035976))

#### Statistical Context

[DATA] Theme enrichment: FDR=1.79e-05 with 85.6-fold enrichment across 4 genes. [GO-HIERARCHY] This cellular component anchor pinpoints the AP‑1 complex as a concentrated driver of downstream transcriptional themes.

---

### Theme 4: cellular response to cytokine stimulus

**Summary:** cellular response to cytokine stimulus ([GO:0071345](http://purl.obolibrary.org/obo/GO_0071345))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Cells decode cytokine exposure into antiviral, inflammatory, and matrix‑remodeling programs via interferon‑inducible GTPases, transcription factors, and ECM enzymes. [EXTERNAL] GBP1 and GBP2 are strongly induced by IFN‑gamma and orchestrate downstream responses to TNF and IL‑1, aligning GTPase signaling with pro‑inflammatory gene expression [PMID:17266443](https://pubmed.ncbi.nlm.nih.gov/17266443/), [PMID:21151871](https://pubmed.ncbi.nlm.nih.gov/21151871/). [EXTERNAL] ZFP36 family RNA‑binders are upregulated by cytokines and directly mediate cellular responses to TNF by degrading pro‑inflammatory transcripts, curbing excessive signaling [PMID:20166898](https://pubmed.ncbi.nlm.nih.gov/20166898/). [INFERENCE] HAS2 couples IL‑1 and TNF sensing to hyaluronan synthesis, fostering leukocyte adhesion and tissue remodeling.

#### Key Insights

- [DATA] IFN‑gamma induction of GBP1/GBP2 connects cytokine sensing to GTPase‑controlled effector programs during cellular response to TNF and IL‑1 [PMID:17266443](https://pubmed.ncbi.nlm.nih.gov/17266443/). ([GO:0071356](http://purl.obolibrary.org/obo/GO_0071356))
- [DATA] ZFP36/ZFP36L2 enforce transcript decay under TNF to terminate cytokine signaling within the cellular response to tumor necrosis factor [PMID:20166898](https://pubmed.ncbi.nlm.nih.gov/20166898/). ([GO:0071356](http://purl.obolibrary.org/obo/GO_0071356))

#### Key Genes

- **GBP1**: [EXTERNAL] [EXTERNAL] GBP1 is induced by IFN‑gamma and participates in cellular responses to IL‑1 and TNF, coordinating downstream inflammatory gene control [PMID:17266443](https://pubmed.ncbi.nlm.nih.gov/17266443/), [PMID:21151871](https://pubmed.ncbi.nlm.nih.gov/21151871/). ([GO:0071347](http://purl.obolibrary.org/obo/GO_0071347))
- **GBP2**: [EXTERNAL] [EXTERNAL] GBP2 engages GTPase signaling during cellular responses to TNF and IL‑1 to shape pro‑inflammatory transcription [PMID:17266443](https://pubmed.ncbi.nlm.nih.gov/17266443/). ([GO:0071356](http://purl.obolibrary.org/obo/GO_0071356))
- **ZFP36**: [EXTERNAL] [DATA] ZFP36 binds AU‑rich elements in TNF‑induced transcripts and promotes their decay to limit cytokine signaling [PMID:20166898](https://pubmed.ncbi.nlm.nih.gov/20166898/). ([GO:0071356](http://purl.obolibrary.org/obo/GO_0071356))
- **HAS2**: [INFERENCE] [INFERENCE] HAS2 increases hyaluronan synthesis downstream of TNF/IL‑1 to support leukocyte adhesion and survival signaling in inflamed tissues. ([GO:0071356](http://purl.obolibrary.org/obo/GO_0071356))

#### Statistical Context

[DATA] Theme enrichment: FDR=2.58e-05 with 5.6-fold enrichment across 15 genes. [GO-HIERARCHY] Specific subterms emphasize cellular responses to TNF and IL‑1, indicating convergence of multiple cytokine axes.

---

### Theme 5: intracellular signaling cassette

**Summary:** intracellular signaling cassette ([GO:0141124](http://purl.obolibrary.org/obo/GO_0141124))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 4.14e-05 · **Genes (23)**: ARHGAP29, ARHGEF3, CAMK2D, CEBPD, CHI3L1, CITED1, EDNRA, FOS, ITGAV, ITPR2, JUN, JUNB, MAP3K14, MAPK4, NFATC2 … (+8 more)

---

### Theme 6: enzyme-linked receptor protein signaling pathway

**Summary:** enzyme-linked receptor protein signaling pathway ([GO:0007167](http://purl.obolibrary.org/obo/GO_0007167))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Enzyme‑linked receptor pathways couple ligand binding to kinase cascades and Smad transcriptional control to direct growth and differentiation. [EXTERNAL] TGFBR2 engagement drives receptor complexing and Smad phosphorylation to execute TGF‑beta gene programs controlling proliferation and matrix remodeling [PMID:28131417](https://pubmed.ncbi.nlm.nih.gov/28131417/). [EXTERNAL] STAT3 is recruited downstream of TGF‑beta in vascular smooth muscle, forming an axis with Smad3 that governs pro‑proliferative transcription and FoxO1 control [PMID:28467929](https://pubmed.ncbi.nlm.nih.gov/28467929/). [EXTERNAL] AP‑1 subunits FOS and JUN co‑operate with Smad complexes to amplify TGF‑beta‑induced transcriptional responses [PMID:9732876](https://pubmed.ncbi.nlm.nih.gov/9732876/).

#### Key Insights

- [EXTERNAL] A TGFBR2→Smad2/3→AP‑1 relay defines the transforming growth factor beta receptor signaling pathway controlling growth and adhesion [PMID:28131417](https://pubmed.ncbi.nlm.nih.gov/28131417/), [PMID:9732876](https://pubmed.ncbi.nlm.nih.gov/9732876/). ([GO:0007179](http://purl.obolibrary.org/obo/GO_0007179))
- [EXTERNAL] STAT3 integrates with TGF‑beta receptors to modulate pro‑proliferative transcription within enzyme‑linked receptor protein signaling [PMID:28467929](https://pubmed.ncbi.nlm.nih.gov/28467929/). ([GO:0007167](http://purl.obolibrary.org/obo/GO_0007167))

#### Key Genes

- **STAT3**: [EXTERNAL] [EXTERNAL] STAT3 interfaces with TGF‑beta receptors to drive VSMC transcriptional programs via a TGFβ1–STAT3–FoxO1 axis [PMID:28467929](https://pubmed.ncbi.nlm.nih.gov/28467929/). ([GO:0007179](http://purl.obolibrary.org/obo/GO_0007179))
- **TGFBR2**: [EXTERNAL] [EXTERNAL] TGFBR2 ligand binding initiates heterodimerization and Smad phosphorylation to control diverse cellular outcomes [PMID:28131417](https://pubmed.ncbi.nlm.nih.gov/28131417/). ([GO:0007179](http://purl.obolibrary.org/obo/GO_0007179))
- **ID1**: [INFERENCE] [INFERENCE] ID1 acts downstream of TGF‑beta/Smad as a transcriptional effector modulating proliferation and differentiation. ([GO:0007179](http://purl.obolibrary.org/obo/GO_0007179))
- **DOK5**: [INFERENCE] [INFERENCE] DOK5 functions as an adaptor at activated receptor tyrosine kinases to route signals to downstream effectors that cooperate with Smad programs. ([GO:0007169](http://purl.obolibrary.org/obo/GO_0007169))

#### Statistical Context

[DATA] Theme enrichment: FDR=5.89e-05 with 3.9-fold enrichment across 20 genes. [GO-HIERARCHY] Nested terms highlight transforming growth factor beta receptor signaling and cell surface receptor protein tyrosine kinase signaling as coordinated modules.

---

### Theme 7: negative regulation of apoptotic process

**Summary:** negative regulation of apoptotic process ([GO:0043066](http://purl.obolibrary.org/obo/GO_0043066))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Survival programs counteract intrinsic and neuronal apoptosis by dampening oxidative stress and stabilizing anti‑apoptotic signaling. [EXTERNAL] HIF1A suppresses oxidative stress‑induced neuronal intrinsic apoptosis by modulating the VHL/HIF‑1 axis, preserving mitochondrial integrity under stress [PMID:24899725](https://pubmed.ncbi.nlm.nih.gov/24899725/). [INFERENCE] SOD2 detoxifies superoxide in mitochondria to reduce ROS‑triggered caspase activation and sustain survival signaling. [INFERENCE] CLU acts as an extracellular chaperone that buffers proteotoxic stress and supports pro‑survival receptor signaling. [INFERENCE] STAT3 promotes anti‑apoptotic transcription and mitochondrial functions to restrain intrinsic cell death under cytokine input.

#### Key Insights

- [EXTERNAL] Hypoxic signaling via HIF1A curbs oxidative stress‑driven intrinsic apoptosis in neurons within negative regulation of intrinsic apoptotic signaling pathway [PMID:24899725](https://pubmed.ncbi.nlm.nih.gov/24899725/). ([GO:2001243](http://purl.obolibrary.org/obo/GO_2001243))
- [INFERENCE] Mitochondrial SOD2 reduces ROS burden to attenuate executioner pathways in the negative regulation of apoptotic process. ([GO:0043066](http://purl.obolibrary.org/obo/GO_0043066))

#### Key Genes

- **SOD2**: [INFERENCE] [INFERENCE] SOD2 removes mitochondrial superoxide to blunt ROS‑triggered intrinsic apoptosis signaling and promote cell survival. ([GO:2001243](http://purl.obolibrary.org/obo/GO_2001243))
- **HIF1A**: [EXTERNAL] [EXTERNAL] HIF1A antagonizes oxidative stress‑induced neuronal intrinsic apoptosis by modulating VHL/HIF‑1 signaling [PMID:24899725](https://pubmed.ncbi.nlm.nih.gov/24899725/). ([GO:2001243](http://purl.obolibrary.org/obo/GO_2001243))
- **CLU**: [INFERENCE] [INFERENCE] CLU chaperones extracellular ligands and receptors to sustain pro‑survival signaling and mitigate apoptosis under stress. ([GO:0043066](http://purl.obolibrary.org/obo/GO_0043066))
- **STAT3**: [INFERENCE] [INFERENCE] STAT3 upregulates anti‑apoptotic effectors and supports mitochondrial function to suppress intrinsic apoptosis. ([GO:2001243](http://purl.obolibrary.org/obo/GO_2001243))

#### Statistical Context

[DATA] Theme enrichment: FDR=9.06e-05 with 3.4-fold enrichment across 23 genes. [GO-HIERARCHY] Specific subterms enrich for negative regulation of neuron apoptotic process and intrinsic apoptotic signaling restraint, indicating neuronal vulnerability buffering.

---

### Theme 8: growth factor binding

**Summary:** growth factor binding ([GO:0019838](http://purl.obolibrary.org/obo/GO_0019838))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Growth factor binding at the cell surface organizes co‑receptor ensembles that gate downstream kinase and transcriptional programs controlling proliferation and migration. [EXTERNAL] ITGAV engages FGF1 and IGF‑1 directly via αvβ3 to potentiate signaling independent of matrix ligation, creating integrin–RTK cross‑talk nodes [PMID:18441324](https://pubmed.ncbi.nlm.nih.gov/18441324/), [PMID:19578119](https://pubmed.ncbi.nlm.nih.gov/19578119/). [EXTERNAL] Neuropilin family members serve as growth factor binders that relay VEGF signals to p130Cas and motility circuits [PMID:21245381](https://pubmed.ncbi.nlm.nih.gov/21245381/). [INFERENCE] IL6R and IGFBP7 modulate ligand availability and receptor activation to fine‑tune pathway strength.

#### Key Insights

- [EXTERNAL] Direct integrin αvβ3 binding to FGF1 and IGF‑1 amplifies growth factor signaling outputs that drive migration and survival [PMID:18441324](https://pubmed.ncbi.nlm.nih.gov/18441324/), [PMID:19578119](https://pubmed.ncbi.nlm.nih.gov/19578119/). ([GO:0019838](http://purl.obolibrary.org/obo/GO_0019838))
- [EXTERNAL] Neuropilin‑dependent growth factor binding links VEGF to cytoskeletal signaling for motility and proliferation [PMID:21245381](https://pubmed.ncbi.nlm.nih.gov/21245381/). ([GO:0019838](http://purl.obolibrary.org/obo/GO_0019838))

#### Key Genes

- **ITGAV**: [EXTERNAL] [EXTERNAL] ITGAV (αvβ3) binds FGF1 and IGF‑1 to co‑signal with RTKs, boosting proliferative and migratory pathways [PMID:18441324](https://pubmed.ncbi.nlm.nih.gov/18441324/), [PMID:19578119](https://pubmed.ncbi.nlm.nih.gov/19578119/). ([GO:0019838](http://purl.obolibrary.org/obo/GO_0019838))
- **NRP2**: [EXTERNAL] [EXTERNAL] NRP2 participates in VEGF family ligand binding to organize growth factor signaling complexes that promote motility [PMID:21245381](https://pubmed.ncbi.nlm.nih.gov/21245381/). ([GO:0019838](http://purl.obolibrary.org/obo/GO_0019838))
- **IGFBP7**: [INFERENCE] [INFERENCE] IGFBP7 sequesters IGFs to sculpt receptor occupancy and downstream mitogenic signaling. ([GO:0019838](http://purl.obolibrary.org/obo/GO_0019838))
- **IL6R**: [INFERENCE] [INFERENCE] IL6R engagement of IL‑6 modulates JAK/STAT amplitude as part of growth factor–like cytokine signaling at the surface. ([GO:0019838](http://purl.obolibrary.org/obo/GO_0019838))

#### Statistical Context

[DATA] Theme enrichment: FDR=9.90e-05 with 8.7-fold enrichment across 11 genes. [GO-HIERARCHY] This molecular function anchor consolidates diverse ligand–receptor binding events into a unified amplification layer for downstream pathways.

---

### Theme 9: DNA-binding transcription activator activity, RNA polymerase II-specific

**Summary:** DNA-binding transcription activator activity, RNA polymerase II-specific ([GO:0001228](http://purl.obolibrary.org/obo/GO_0001228))  · Anchor confidence: **FDR<0.01**

[INFERENCE] A cadre of inducible transcription factors activates RNA polymerase II to implement stress, hypoxia, and cytokine‑responsive gene programs. [EXTERNAL] STAT3 directly activates transcription of immune and developmental targets in human PBMCs in response to cytokine axes [PMID:31886314](https://pubmed.ncbi.nlm.nih.gov/31886314/). [EXTERNAL] FOS within AP‑1 induces microRNA circuits that suppress focal adhesion kinase and alter migratory phenotypes, exemplifying transcription–miRNA coupling [PMID:30670568](https://pubmed.ncbi.nlm.nih.gov/30670568/). [EXTERNAL] HIF1A binds hypoxia response elements to drive cardiomyocyte and vascular microRNA expression that modulates apoptosis and metabolism [PMID:24983504](https://pubmed.ncbi.nlm.nih.gov/24983504/). [EXTERNAL] NR4A3 transactivates inflammatory and adhesion genes in vascular cells linking growth factor signaling to motility [PMID:20558821](https://pubmed.ncbi.nlm.nih.gov/20558821/).

#### Key Insights

- [EXTERNAL] Cytokine‑responsive STAT3 and AP‑1 subunits drive RNA polymerase II activation at immune and migration genes [PMID:31886314](https://pubmed.ncbi.nlm.nih.gov/31886314/), [PMID:30670568](https://pubmed.ncbi.nlm.nih.gov/30670568/). ([GO:0001228](http://purl.obolibrary.org/obo/GO_0001228))
- [EXTERNAL] HIF1A couples hypoxia to microRNA transcription to adjust survival and metabolic pathways [PMID:24983504](https://pubmed.ncbi.nlm.nih.gov/24983504/). ([GO:0001228](http://purl.obolibrary.org/obo/GO_0001228))

#### Key Genes

- **STAT3**: [EXTERNAL] [DATA] STAT3 acts as a DNA‑binding transcription activator that stimulates Pol II transcription in cytokine‑activated immune cells [PMID:31886314](https://pubmed.ncbi.nlm.nih.gov/31886314/). ([GO:0001228](http://purl.obolibrary.org/obo/GO_0001228))
- **FOS**: [EXTERNAL] [EXTERNAL] FOS activates Pol II targets and miR‑551a to remodel adhesion signaling and tumorigenesis propensity [PMID:30670568](https://pubmed.ncbi.nlm.nih.gov/30670568/). ([GO:0001228](http://purl.obolibrary.org/obo/GO_0001228))
- **HIF1A**: [EXTERNAL] [EXTERNAL] HIF1A binds HREs to activate transcription and microRNAs during hypoxic stress in cardiomyocytes [PMID:24983504](https://pubmed.ncbi.nlm.nih.gov/24983504/). ([GO:0001228](http://purl.obolibrary.org/obo/GO_0001228))
- **NR4A3**: [EXTERNAL] [EXTERNAL] NR4A3 transactivates vascular and inflammatory genes downstream of growth factor pathways to modulate adhesion and aggregation [PMID:20558821](https://pubmed.ncbi.nlm.nih.gov/20558821/). ([GO:0001228](http://purl.obolibrary.org/obo/GO_0001228))

#### Statistical Context

[DATA] Theme enrichment: FDR=9.90e-05 with 4.5-fold enrichment across 19 genes. [GO-HIERARCHY] This molecular function anchor underpins multiple signaling themes by enabling stimulus‑coupled transcriptional activation.

---

### Theme 10: positive regulation of monocyte aggregation

**Summary:** positive regulation of monocyte aggregation ([GO:1900625](http://purl.obolibrary.org/obo/GO_1900625))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Monocyte aggregation is enforced by a hyaluronan–CD44 adhesive axis transcriptionally reinforced by inflammatory nuclear receptors. [EXTERNAL] HAS2 synthesizes hyaluronan in endothelial cells under pro‑inflammatory cytokines, creating a pericellular matrix that promotes CD44‑dependent monocyte adhesion [PMID:20522558](https://pubmed.ncbi.nlm.nih.gov/20522558/). [EXTERNAL] CD44 ligation to hyaluronan strengthens intercellular contacts that seed aggregates in inflamed endothelium [PMID:20522558](https://pubmed.ncbi.nlm.nih.gov/20522558/). [EXTERNAL] NR4A3 drives pro‑adhesive gene programs that increase monocyte sticking and atherogenic recruitment [PMID:20558821](https://pubmed.ncbi.nlm.nih.gov/20558821/).

#### Key Insights

- [EXTERNAL] Cytokine‑driven HAS2 elevates hyaluronan to promote CD44‑dependent positive regulation of monocyte aggregation [PMID:20522558](https://pubmed.ncbi.nlm.nih.gov/20522558/). ([GO:1900625](http://purl.obolibrary.org/obo/GO_1900625))
- [EXTERNAL] NR4A3 transcriptionally boosts monocyte adhesive behavior to amplify aggregation [PMID:20558821](https://pubmed.ncbi.nlm.nih.gov/20558821/). ([GO:1900625](http://purl.obolibrary.org/obo/GO_1900625))

#### Key Genes

- **HAS2**: [EXTERNAL] [EXTERNAL] HAS2 induction increases endothelial hyaluronan, directly enhancing monocyte aggregation via CD44 binding [PMID:20522558](https://pubmed.ncbi.nlm.nih.gov/20522558/). ([GO:1900625](http://purl.obolibrary.org/obo/GO_1900625))
- **CD44**: [EXTERNAL] [EXTERNAL] CD44 engages hyaluronan to stabilize monocyte–cell contacts and promote aggregation [PMID:20522558](https://pubmed.ncbi.nlm.nih.gov/20522558/). ([GO:1900625](http://purl.obolibrary.org/obo/GO_1900625))
- **NR4A3**: [EXTERNAL] [EXTERNAL] NR4A3 elevates monocyte adhesion/aggregation programs linked to atherogenesis [PMID:20558821](https://pubmed.ncbi.nlm.nih.gov/20558821/). ([GO:1900625](http://purl.obolibrary.org/obo/GO_1900625))

#### Statistical Context

[DATA] Theme enrichment: FDR=1.54e-04 with 107.0-fold enrichment across 3 genes. [GO-HIERARCHY] This focused biological process reflects a specialized leukocyte adhesive program.

---

### Theme 11: positive regulation of miRNA transcription

**Summary:** positive regulation of miRNA transcription ([GO:1902895](http://purl.obolibrary.org/obo/GO_1902895))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Stimulus‑dependent transcription factors elevate microRNA production to rewire signaling and fate decisions. [EXTERNAL] HIF1A upregulates miRNAs such as miR‑21 and miR‑448 under hypoxia, modulating apoptosis and electrical conduction in stressed tissues [PMID:24983504](https://pubmed.ncbi.nlm.nih.gov/24983504/), [PMID:33108349](https://pubmed.ncbi.nlm.nih.gov/33108349/). [EXTERNAL] FOS boosts miR‑551a to suppress FAK and block tumorigenesis, illustrating AP‑1 regulation of miRNA promoters [PMID:30670568](https://pubmed.ncbi.nlm.nih.gov/30670568/). [INFERENCE] JUN and TGFB2 converge on endothelial miRNA clusters to coordinate angiogenic responses.

#### Key Insights

- [EXTERNAL] Hypoxic HIF1A drives positive regulation of miRNA transcription to tune apoptosis and metabolism [PMID:24983504](https://pubmed.ncbi.nlm.nih.gov/24983504/), [PMID:33108349](https://pubmed.ncbi.nlm.nih.gov/33108349/). ([GO:1902895](http://purl.obolibrary.org/obo/GO_1902895))
- [EXTERNAL] AP‑1–FOS activation of miR‑551a links stress transcription to focal adhesion remodeling [PMID:30670568](https://pubmed.ncbi.nlm.nih.gov/30670568/). ([GO:1902895](http://purl.obolibrary.org/obo/GO_1902895))

#### Key Genes

- **HIF1A**: [EXTERNAL] [EXTERNAL] HIF1A induces microRNAs under hypoxia, forming feedback loops that control survival and inflammatory signaling [PMID:24983504](https://pubmed.ncbi.nlm.nih.gov/24983504/), [PMID:33108349](https://pubmed.ncbi.nlm.nih.gov/33108349/). ([GO:1902895](http://purl.obolibrary.org/obo/GO_1902895))
- **FOS**: [EXTERNAL] [EXTERNAL] FOS increases miR‑551a transcription to dampen FAK and tumorigenic signaling [PMID:30670568](https://pubmed.ncbi.nlm.nih.gov/30670568/). ([GO:1902895](http://purl.obolibrary.org/obo/GO_1902895))
- **TGFB2**: [EXTERNAL] [EXTERNAL] TGFB2 regulates endothelial miR‑212/132 to restrain angiogenic morphogenesis [PMID:25217442](https://pubmed.ncbi.nlm.nih.gov/25217442/). ([GO:1902895](http://purl.obolibrary.org/obo/GO_1902895))
- **JUN**: [EXTERNAL] [EXTERNAL] JUN enhances specific miRNA clusters that control vascular and proliferative responses under MAPK input [PMID:24375836](https://pubmed.ncbi.nlm.nih.gov/24375836/). ([GO:1902895](http://purl.obolibrary.org/obo/GO_1902895))

#### Statistical Context

[DATA] Theme enrichment: FDR=1.54e-04 with 13.6-fold enrichment across 7 genes. [GO-HIERARCHY] This process anchors transcriptional control over noncoding regulators of signaling networks.

---

### Theme 12: membrane raft

**Summary:** membrane raft ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Membrane rafts concentrate receptors and adaptors to choreograph cytoskeletal signaling, EMT transitions, and immune synapses. [EXTERNAL] PDPN requires raft association to engage ERM proteins and activate RhoA, promoting EMT and protrusive dynamics [PMID:21376833](https://pubmed.ncbi.nlm.nih.gov/21376833/). [EXTERNAL] RFTN1 localizes to lipid rafts where it scaffolds signaling assemblies in immune cells, enabling efficient receptor coupling [PMID:21955986](https://pubmed.ncbi.nlm.nih.gov/21955986/). [EXTERNAL] NOS1AP targets nitric oxide synthase complexes to caveolar/raft microdomains to tune local signaling in excitable tissues [PMID:19800018](https://pubmed.ncbi.nlm.nih.gov/19800018/). [INFERENCE] CNR1 within rafts modulates GPCR crosstalk with TGF‑beta machinery to bias Smad activation and motility.

#### Key Insights

- [EXTERNAL] Podoplanin’s raft‑dependent ERM engagement links membrane microdomains to EMT and RhoA signaling [PMID:21376833](https://pubmed.ncbi.nlm.nih.gov/21376833/). ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))
- [EXTERNAL] Raft resident adaptors like RFTN1 and NOS1AP organize kinase and NOS signaling nanodomains [PMID:21955986](https://pubmed.ncbi.nlm.nih.gov/21955986/), [PMID:19800018](https://pubmed.ncbi.nlm.nih.gov/19800018/). ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))

#### Key Genes

- **PDPN**: [EXTERNAL] [EXTERNAL] PDPN’s transmembrane domain targets lipid rafts to activate ERM–RhoA signaling and drive EMT‑like protrusions [PMID:21376833](https://pubmed.ncbi.nlm.nih.gov/21376833/). ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))
- **RFTN1**: [EXTERNAL] [EXTERNAL] RFTN1 stabilizes lipid rafts to assemble immune signaling complexes and facilitate receptor coupling [PMID:21955986](https://pubmed.ncbi.nlm.nih.gov/21955986/). ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))
- **NOS1AP**: [EXTERNAL] [EXTERNAL] NOS1AP co‑localizes with NOS1 in caveolar/raft microdomains to regulate localized nitric oxide signaling [PMID:19800018](https://pubmed.ncbi.nlm.nih.gov/19800018/). ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))
- **CNR1**: [INFERENCE] [INFERENCE] CNR1 partitions to rafts to modulate GPCR–kinase crosstalk shaping downstream cytoskeletal responses. ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))

#### Statistical Context

[DATA] Theme enrichment: FDR=1.81e-04 with 5.2-fold enrichment across 14 genes. [GO-HIERARCHY] This cellular component anchor unifies multiple signaling themes via nanoscale receptor organization.

---

### Theme 13: cell-cell adhesion

**Summary:** cell-cell adhesion ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Cell–cell adhesion integrates integrins, cadherin regulators, and cytokine co‑receptors to stabilize contacts and coordinate signaling across tissues. [EXTERNAL] ITGAV mediates heterotypic adhesion with endothelial cells, supporting stromal homing and intercellular communication [PMID:20563599](https://pubmed.ncbi.nlm.nih.gov/20563599/). [INFERENCE] IL1RAP amplifies IL‑1 signaling that secondarily reinforces adhesion molecule expression on immune and stromal cells. [INFERENCE] TGFB2/TGFBR2 signaling contributes to endocardial cushion fusion by regulating adhesion and EMT programs during cardiac morphogenesis.

#### Key Insights

- [EXTERNAL] Integrin αv‑containing receptors foster heterotypic cell–cell adhesion between stromal and endothelial cells [PMID:20563599](https://pubmed.ncbi.nlm.nih.gov/20563599/). ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- [INFERENCE] Cytokine co‑receptors amplify adhesion molecule transcription to strengthen synaptic and tissue contacts. ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))

#### Key Genes

- **ITGA3**: [EXTERNAL] [EXTERNAL] ITGA3‑containing integrins collaborate with endothelial partners to stabilize cell–cell contacts and guide homing [PMID:20563599](https://pubmed.ncbi.nlm.nih.gov/20563599/). ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **TGFBR2**: [INFERENCE] [INFERENCE] TGFBR2 drives EMT‑like adhesion remodeling critical for endocardial cushion fusion during cardiac development. ([GO:0003274](http://purl.obolibrary.org/obo/GO_0003274))
- **TGFB2**: [INFERENCE] [INFERENCE] TGFB2 orchestrates adhesive transitions underlying cushion fusion and septation. ([GO:0003274](http://purl.obolibrary.org/obo/GO_0003274))
- **IL1RAP**: [EXTERNAL] [EXTERNAL] IL1RAP co‑reception heightens IL‑1 signaling to elevate adhesion molecule expression during inflammation [PMID:33482337](https://pubmed.ncbi.nlm.nih.gov/33482337/). ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))

#### Statistical Context

[DATA] Theme enrichment: FDR=3.18e-04 with 3.7-fold enrichment across 18 genes. [GO-HIERARCHY] Synaptic membrane adhesion and endocardial cushion fusion subterms indicate both neural and cardiac adhesion specializations.

---

### Theme 14: regulation of response to external stimulus

**Summary:** regulation of response to external stimulus ([GO:0032101](http://purl.obolibrary.org/obo/GO_0032101))  · Anchor confidence: **FDR<0.01**

[INFERENCE] External cues are filtered by inhibitory and activating circuits to calibrate inflammatory and stress responses. [EXTERNAL] HLA‑E presentation to NKG2A:CD94 restrains NK activation, curbing excessive responses to danger signals [PMID:35705051](https://pubmed.ncbi.nlm.nih.gov/35705051/). [EXTERNAL] IL1RAP potentiates IL‑1 signaling to activate NF‑kB and MAPK cascades that escalate inflammatory outputs when needed [PMID:33482337](https://pubmed.ncbi.nlm.nih.gov/33482337/). [EXTERNAL] SERPINE1 tempers proteolysis and chemokine landscapes after LPS or smoke injury, modulating the overall response to external stimulus [PMID:19916862](https://pubmed.ncbi.nlm.nih.gov/19916862/). [INFERENCE] STAT3 provides a cytokine‑driven rheostat that prevents runaway inflammation by transcriptional feedback.

#### Key Insights

- [EXTERNAL] HLA‑E–mediated NK cell inhibition exemplifies negative regulation of response to external stimulus to avoid bystander damage [PMID:35705051](https://pubmed.ncbi.nlm.nih.gov/35705051/). ([GO:0032102](http://purl.obolibrary.org/obo/GO_0032102))
- [EXTERNAL] IL1RAP enhances positive regulation of inflammatory response through NF‑kB and MAPK activation under IL‑1 signaling [PMID:33482337](https://pubmed.ncbi.nlm.nih.gov/33482337/). ([GO:0050729](http://purl.obolibrary.org/obo/GO_0050729))

#### Key Genes

- **HLA-E**: [EXTERNAL] [EXTERNAL] HLA‑E restrains NK effector functions by presenting VL9‑like ligands to NKG2A:CD94, damping responses to injury signals [PMID:35705051](https://pubmed.ncbi.nlm.nih.gov/35705051/). ([GO:0032102](http://purl.obolibrary.org/obo/GO_0032102))
- **IL1RAP**: [EXTERNAL] [EXTERNAL] IL1RAP boosts IL‑1 signal transduction to intensify inflammatory gene activation via NF‑kB/MAPK [PMID:33482337](https://pubmed.ncbi.nlm.nih.gov/33482337/). ([GO:0050729](http://purl.obolibrary.org/obo/GO_0050729))
- **SERPINE1**: [EXTERNAL] [EXTERNAL] SERPINE1 modulates inflammatory response magnitude by controlling fibrinolysis and cytokine milieu under LPS exposure [PMID:19916862](https://pubmed.ncbi.nlm.nih.gov/19916862/). ([GO:0050729](http://purl.obolibrary.org/obo/GO_0050729))
- **STAT3**: [INFERENCE] [INFERENCE] STAT3 enforces feedback suppression of overzealous cytokine responses to external stimuli via inducible target genes. ([GO:0032102](http://purl.obolibrary.org/obo/GO_0032102))

#### Statistical Context

[DATA] Theme enrichment: FDR=3.82e-04 with 2.8-fold enrichment across 26 genes. [GO-HIERARCHY] The balance of negative regulation of response to external stimulus and positive regulation of inflammatory response reflects bidirectional control.

---

### Theme 15: glutamatergic synapse

**Summary:** glutamatergic synapse ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Glutamatergic synapse organization depends on scaffolded actin networks and Rho GTPase exchange factors that tune receptor anchoring and plasticity. [EXTERNAL] TRIO activates Rac1/RhoA at postsynapses to drive spine morphogenesis and long‑term potentiation, translating CaMKII input into structural plasticity [PMID:26858404](https://pubmed.ncbi.nlm.nih.gov/26858404/). [EXTERNAL] NOS1AP perturbs actin dynamics and NMDA signaling complexes, altering synaptic transmission and spine maturation [PMID:26869880](https://pubmed.ncbi.nlm.nih.gov/26869880/). [EXTERNAL] ACTN1 anchors PSD‑95 to F‑actin, stabilizing AMPAR nanodomains crucial for excitatory transmission [PMID:29429936](https://pubmed.ncbi.nlm.nih.gov/29429936/). [INFERENCE] CNR1 suppresses presynaptic cAMP and calcium influx to reduce glutamate release, shaping short‑term plasticity.

#### Key Insights

- [EXTERNAL] TRIO‑driven Rho GTPase activation remodels dendritic spines to calibrate glutamatergic synapse efficacy [PMID:26858404](https://pubmed.ncbi.nlm.nih.gov/26858404/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- [EXTERNAL] NOS1AP and ACTN1 scaffold receptor complexes and actin to stabilize excitatory postsynaptic machinery [PMID:26869880](https://pubmed.ncbi.nlm.nih.gov/26869880/), [PMID:29429936](https://pubmed.ncbi.nlm.nih.gov/29429936/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Key Genes

- **TRIO**: [EXTERNAL] [EXTERNAL] TRIO activates Rho GTPases at excitatory synapses to drive spine growth and LTP expression [PMID:26858404](https://pubmed.ncbi.nlm.nih.gov/26858404/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **NOS1AP**: [EXTERNAL] [EXTERNAL] NOS1AP overexpression alters actin and NMDA complex coupling, reducing synaptic strength and spine maturity [PMID:26869880](https://pubmed.ncbi.nlm.nih.gov/26869880/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **ACTN1**: [EXTERNAL] [EXTERNAL] ACTN1 binds PSD‑95 to F‑actin to maintain postsynaptic receptor anchoring and transmission [PMID:29429936](https://pubmed.ncbi.nlm.nih.gov/29429936/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **CNR1**: [INFERENCE] [INFERENCE] CNR1 attenuates presynaptic release probability to tune excitatory drive at glutamatergic terminals. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Statistical Context

[DATA] Theme enrichment: FDR=4.74e-04 with 3.5-fold enrichment across 19 genes. [GO-HIERARCHY] This cellular component anchor highlights synaptic nanomachinery for excitatory neurotransmission.

---

### Theme 16: positive regulation of transcription by RNA polymerase II

**Summary:** positive regulation of transcription by RNA polymerase II ([GO:0045944](http://purl.obolibrary.org/obo/GO_0045944))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Signal‑dependent activators amplify RNA polymerase II initiation and elongation to execute growth and stress transcriptional programs. [DATA] AP‑1 subunits JUN/FOS/JUNB positively regulate transcription by RNA polymerase II during G0→G1 transitions and stress responses [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/), [PMID:1406655](https://pubmed.ncbi.nlm.nih.gov/1406655/). [EXTERNAL] HIF1A enhances Pol II transcription under high glucose and hypoxia, fueling inflammatory cytokine output in monocytes [PMID:32697943](https://pubmed.ncbi.nlm.nih.gov/32697943/). [EXTERNAL] STAT3 directly stimulates Pol II at developmental and cytokine targets across diverse tissues [PMID:31886314](https://pubmed.ncbi.nlm.nih.gov/31886314/), [PMID:27050391](https://pubmed.ncbi.nlm.nih.gov/27050391/).

#### Key Insights

- [DATA] AP‑1 complexes drive positive regulation of transcription by RNA polymerase II at early response promoters during regeneration and stress [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/), [PMID:1406655](https://pubmed.ncbi.nlm.nih.gov/1406655/). ([GO:0045944](http://purl.obolibrary.org/obo/GO_0045944))
- [EXTERNAL] HIF1A boosts Pol II activity under metabolic stress to intensify cytokine gene expression [PMID:32697943](https://pubmed.ncbi.nlm.nih.gov/32697943/). ([GO:0045944](http://purl.obolibrary.org/obo/GO_0045944))

#### Key Genes

- **STAT3**: [EXTERNAL] [EXTERNAL] STAT3 activates Pol II at target genes in development and immunity under upstream Rac1 and cytokine control [PMID:31886314](https://pubmed.ncbi.nlm.nih.gov/31886314/), [PMID:27050391](https://pubmed.ncbi.nlm.nih.gov/27050391/). ([GO:0045944](http://purl.obolibrary.org/obo/GO_0045944))
- **JUN**: [EXTERNAL] [DATA] JUN promotes Pol II transcription during G1 and stress, partnering with FOS/JUNB at AP‑1 elements [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/), [PMID:1406655](https://pubmed.ncbi.nlm.nih.gov/1406655/). ([GO:0045944](http://purl.obolibrary.org/obo/GO_0045944))
- **FOS**: [EXTERNAL] [DATA] FOS engages AP‑1 sites to enhance Pol II‑mediated transcription in response to signaling inputs [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/). ([GO:0045944](http://purl.obolibrary.org/obo/GO_0045944))
- **HIF1A**: [EXTERNAL] [EXTERNAL] HIF1A augments transcription of inflammatory genes under hyperglycemia and hypoxia conditions [PMID:32697943](https://pubmed.ncbi.nlm.nih.gov/32697943/). ([GO:0045944](http://purl.obolibrary.org/obo/GO_0045944))

#### Statistical Context

[DATA] Theme enrichment: FDR=4.97e-04 with 2.6-fold enrichment across 28 genes. [GO-HIERARCHY] This process serves as a central actuator for multiple upstream signaling themes.

---

### Theme 17: basement membrane

**Summary:** basement membrane ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))  · Anchor confidence: **FDR<0.01**

[INFERENCE] The basement membrane is a collagen‑rich scaffold whose composition and protease regulation maintain vascular integrity and signaling niches. [EXTERNAL] COL4A1 forms type IV collagen networks essential for basement membrane stability, with haploinsufficiency compromising cerebral small vessels [PMID:23065703](https://pubmed.ncbi.nlm.nih.gov/23065703/). [INFERENCE] TIMP3 restrains matrix metalloproteinases to preserve basement membrane architecture during remodeling. [INFERENCE] FN1 and COL4A2 cooperate to provide adhesive tracks and tensile strength that steer integrin signaling and cell behavior.

#### Key Insights

- [EXTERNAL] Type IV collagen networks assembled by COL4A1 maintain basement membrane integrity critical for vascular stability [PMID:23065703](https://pubmed.ncbi.nlm.nih.gov/23065703/). ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))
- [INFERENCE] TIMP‑controlled proteolysis preserves collagen scaffolding to sustain signaling microenvironments. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))

#### Key Genes

- **COL4A1**: [EXTERNAL] [EXTERNAL] COL4A1 builds type IV collagen networks whose deficiency destabilizes cerebral microvasculature [PMID:23065703](https://pubmed.ncbi.nlm.nih.gov/23065703/). ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))
- **COL4A2**: [INFERENCE] [INFERENCE] COL4A2 partners with COL4A1 to assemble network‑forming collagen IV that supports endothelial adhesion and filtration. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))
- **TIMP3**: [INFERENCE] [INFERENCE] TIMP3 inhibits MMPs to protect basement membrane collagen from excessive degradation. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))
- **FN1**: [INFERENCE] [INFERENCE] FN1 integrates with collagen lattices to regulate integrin engagement and mechanotransduction at the basement membrane. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))

#### Statistical Context

[DATA] Theme enrichment: FDR=6.54e-04 with 8.4-fold enrichment across 8 genes. [GO-HIERARCHY] This cellular component anchor aggregates matrix constituents central to multiple adhesion and signaling themes.

---

### Theme 18: cell surface

**Summary:** cell surface ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))  · Anchor confidence: **FDR<0.01**

[INFERENCE] The cell surface hosts adhesion receptors, complement factors, and ion channels that choreograph attachment, entry signaling, and inflammatory control. [EXTERNAL] Surface αvβ3/α3β1 integrins concentrate in microdomains that mediate KSHV attachment and entry, illustrating spatial control of receptor function [PMID:25063885](https://pubmed.ncbi.nlm.nih.gov/25063885/). [EXTERNAL] Dab2‑dependent endocytic regulation tunes integrin surface levels to control adhesion strength and migration [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/). [INFERENCE] Complement C3 and tissue factor F3 coordinate opsonization and coagulation‑linked signaling at the plasma membrane to shape immune responses.

#### Key Insights

- [EXTERNAL] Integrin placement within specific cell surface microdomains gates pathogen entry and adhesion signaling [PMID:25063885](https://pubmed.ncbi.nlm.nih.gov/25063885/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- [EXTERNAL] Endocytic adaptors set integrin surface abundance to calibrate adhesion and motility [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Key Genes

- **ITGAV**: [EXTERNAL] [EXTERNAL] ITGAV (αvβ3) enriches at microdomains that drive viral attachment and coordinate downstream signaling [PMID:25063885](https://pubmed.ncbi.nlm.nih.gov/25063885/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **ITGA3**: [EXTERNAL] [EXTERNAL] ITGA3 surface localization is controlled by Dab2, tuning adhesion and migration dynamics [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **ANO6**: [EXTERNAL] [DATA] ANO6 is detected at the cell surface where its lipid scrambling influences adhesion and motility [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **F3**: [EXTERNAL] [EXTERNAL] Surface tissue factor integrates coagulation with signaling that impacts endothelial behavior [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Statistical Context

[DATA] Theme enrichment: FDR=7.60e-04 with 3.1-fold enrichment across 20 genes. [GO-HIERARCHY] This cellular component anchor consolidates diverse receptors and effectors functioning at the plasma membrane.

---

### Theme 19: protease binding

**Summary:** protease binding ([GO:0002020](http://purl.obolibrary.org/obo/GO_0002020))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Protease binding at the cell surface and ECM gatekeeps remodeling, lipid processing, and receptor turnover essential for migration and repair. [EXTERNAL] FAM20C binds and is processed by site‑1 protease to activate its secretory kinase function, coupling protease interaction to extracellular phosphoproteome control and biomineralization [PMID:34349020](https://pubmed.ncbi.nlm.nih.gov/34349020/). [EXTERNAL] A2M sequesters metalloproteinases such as ADAMTS‑7/12 to prevent excessive COMP degradation, protecting matrix integrity [PMID:18485748](https://pubmed.ncbi.nlm.nih.gov/18485748/). [EXTERNAL] ANXA2 interacts with proteases including PCSK9 to modulate receptor degradation, linking protease binding to lipid homeostasis and signaling [PMID:22848640](https://pubmed.ncbi.nlm.nih.gov/22848640/). [EXTERNAL] FN1 binds proteases like cathepsin S, which can alter basement membrane linkages and cell migration through nidogen cleavage [PMID:22952693](https://pubmed.ncbi.nlm.nih.gov/22952693/).

#### Key Insights

- [EXTERNAL] Protease sequestration by A2M balances ECM turnover within protease binding to preserve tissue function [PMID:18485748](https://pubmed.ncbi.nlm.nih.gov/18485748/). ([GO:0002020](http://purl.obolibrary.org/obo/GO_0002020))
- [EXTERNAL] Secretory kinase FAM20C requires protease processing to control extracellular phosphorylation networks [PMID:34349020](https://pubmed.ncbi.nlm.nih.gov/34349020/). ([GO:0002020](http://purl.obolibrary.org/obo/GO_0002020))

#### Key Genes

- **FAM20C**: [EXTERNAL] [EXTERNAL] FAM20C interacts with site‑1 protease enabling activation and secretion to govern the secreted phosphoproteome [PMID:34349020](https://pubmed.ncbi.nlm.nih.gov/34349020/). ([GO:0002020](http://purl.obolibrary.org/obo/GO_0002020))
- **A2M**: [EXTERNAL] [EXTERNAL] A2M traps ADAMTS proteases to inhibit cartilage matrix degradation and regulate remodeling [PMID:18485748](https://pubmed.ncbi.nlm.nih.gov/18485748/). ([GO:0002020](http://purl.obolibrary.org/obo/GO_0002020))
- **ANXA2**: [EXTERNAL] [EXTERNAL] ANXA2 binds PCSK9 and other proteases, tuning receptor turnover and signaling outputs [PMID:22848640](https://pubmed.ncbi.nlm.nih.gov/22848640/). ([GO:0002020](http://purl.obolibrary.org/obo/GO_0002020))
- **FN1**: [EXTERNAL] [EXTERNAL] FN1 engages cathepsin S–modified partners, linking protease activity to matrix connectivity and motility [PMID:22952693](https://pubmed.ncbi.nlm.nih.gov/22952693/). ([GO:0002020](http://purl.obolibrary.org/obo/GO_0002020))

#### Statistical Context

[DATA] Theme enrichment: FDR=8.34e-04 with 7.7-fold enrichment across 10 genes. [GO-HIERARCHY] This molecular function anchor highlights protease–substrate networks bridging matrix remodeling and receptor biology.

---

### Theme 20: cytokine binding

**Summary:** cytokine binding ([GO:0019955](http://purl.obolibrary.org/obo/GO_0019955))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Cytokine binding initiates receptor clustering and co‑receptor synergy to launch JAK/STAT, NF‑kB, and chemokine‑integrin programs. [EXTERNAL] GBP1 participates in cytokine binding contexts regulating T cell activation and cytoskeletal coupling, balancing activation thresholds [PMID:24337748](https://pubmed.ncbi.nlm.nih.gov/24337748/). [EXTERNAL] TGFBR2 binds TGF‑beta to initiate canonical Smad signaling that intersects with inflammatory circuits in macrophages [PMID:18453574](https://pubmed.ncbi.nlm.nih.gov/18453574/). [EXTERNAL] Integrin αvβ3 binds fractalkine, acting as a co‑receptor that tunes chemokine signaling and leukocyte adhesion [PMID:23125415](https://pubmed.ncbi.nlm.nih.gov/23125415/). [EXTERNAL] ZFP36 binds chemokine mRNAs such as CCL3 to dampen downstream cytokine excess, aligning ligand availability with signaling demand [PMID:21784977](https://pubmed.ncbi.nlm.nih.gov/21784977/).

#### Key Insights

- [EXTERNAL] TGFBR2’s transforming growth factor beta binding couples cytokine engagement to Smad transcriptional programs in immune contexts [PMID:18453574](https://pubmed.ncbi.nlm.nih.gov/18453574/). ([GO:0019955](http://purl.obolibrary.org/obo/GO_0019955))
- [EXTERNAL] Integrin co‑recognition of chemokines refines cytokine signaling and adhesion cross‑talk [PMID:23125415](https://pubmed.ncbi.nlm.nih.gov/23125415/). ([GO:0019955](http://purl.obolibrary.org/obo/GO_0019955))

#### Key Genes

- **IL6R**: [INFERENCE] [INFERENCE] IL6R binds IL‑6 to activate JAK/STAT signaling and coordinate inflammatory transcription. ([GO:0019955](http://purl.obolibrary.org/obo/GO_0019955))
- **TGFBR2**: [EXTERNAL] [EXTERNAL] TGFBR2 binds TGF‑beta to launch Smad signaling that modulates inflammatory and remodeling responses [PMID:18453574](https://pubmed.ncbi.nlm.nih.gov/18453574/). ([GO:0019955](http://purl.obolibrary.org/obo/GO_0019955))
- **ZFP36**: [EXTERNAL] [EXTERNAL] ZFP36 binds chemokine transcripts like CCL3 to limit cytokine milieu and receptor stimulation [PMID:21784977](https://pubmed.ncbi.nlm.nih.gov/21784977/). ([GO:0019955](http://purl.obolibrary.org/obo/GO_0019955))
- **GBP1**: [EXTERNAL] [EXTERNAL] GBP1 functions within cytokine binding–linked signaling to calibrate T cell activation thresholds [PMID:24337748](https://pubmed.ncbi.nlm.nih.gov/24337748/). ([GO:0019955](http://purl.obolibrary.org/obo/GO_0019955))

#### Statistical Context

[DATA] Theme enrichment: FDR=8.34e-04 with 7.5-fold enrichment across 10 genes. [GO-HIERARCHY] This molecular function anchor sits upstream of multiple immune signaling cassettes.

---

### Theme 21: filopodium membrane

**Summary:** filopodium membrane ([GO:0031527](http://purl.obolibrary.org/obo/GO_0031527))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Filopodial membranes host adhesion and scaffolding proteins that dock proteases and couple Rho GTPase activity to exploratory motility and invasion. [EXTERNAL] PDPN recruits ERM proteins at filopodia to activate RhoA and promote EMT‑like protrusions [PMID:17046996](https://pubmed.ncbi.nlm.nih.gov/17046996/). [EXTERNAL] ITGAV and ITGA3 enrich on actin‑based microdomains that initiate viral attachment and invadopodial protease docking, linking tip adhesions to entry and matrix degradation [PMID:25063885](https://pubmed.ncbi.nlm.nih.gov/25063885/), [PMID:10455171](https://pubmed.ncbi.nlm.nih.gov/10455171/). [EXTERNAL] GAP43 palmitoylation targets it to filopodial membranes to promote actin remodeling and neurite extension [PMID:14978216](https://pubmed.ncbi.nlm.nih.gov/14978216/).

#### Key Insights

- [EXTERNAL] ERM‑coupled PDPN at filopodia triggers RhoA signaling to drive protrusive dynamics [PMID:17046996](https://pubmed.ncbi.nlm.nih.gov/17046996/). ([GO:0031527](http://purl.obolibrary.org/obo/GO_0031527))
- [EXTERNAL] Integrin‑decorated filopodia serve as platforms for pathogen binding and protease docking during invasion [PMID:25063885](https://pubmed.ncbi.nlm.nih.gov/25063885/), [PMID:10455171](https://pubmed.ncbi.nlm.nih.gov/10455171/). ([GO:0031527](http://purl.obolibrary.org/obo/GO_0031527))

#### Key Genes

- **ITGAV**: [EXTERNAL] [EXTERNAL] ITGAV (αvβ3) concentrates on filopodial microdomains crucial for initial pathogen attachment and signaling [PMID:25063885](https://pubmed.ncbi.nlm.nih.gov/25063885/). ([GO:0031527](http://purl.obolibrary.org/obo/GO_0031527))
- **PDPN**: [EXTERNAL] [EXTERNAL] PDPN localizes to filopodia where ERM engagement activates RhoA and motility programs [PMID:17046996](https://pubmed.ncbi.nlm.nih.gov/17046996/). ([GO:0031527](http://purl.obolibrary.org/obo/GO_0031527))
- **ITGA3**: [EXTERNAL] [EXTERNAL] ITGA3 at invadopodial/filopodial sites docks proteases to coordinate adhesion with pericellular proteolysis [PMID:10455171](https://pubmed.ncbi.nlm.nih.gov/10455171/). ([GO:0031527](http://purl.obolibrary.org/obo/GO_0031527))

#### Statistical Context

[DATA] Theme enrichment: FDR=1.99e-03 with 23.8-fold enrichment across 4 genes. [GO-HIERARCHY] This cellular component anchor emphasizes tip‑localized machineries for sensing and invasion.

---

### Theme 22: blood vessel morphogenesis

**Summary:** blood vessel morphogenesis ([GO:0048514](http://purl.obolibrary.org/obo/GO_0048514))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Vascular morphogenesis balances pro‑sprouting cues with vessel stabilization via TGF‑beta, endothelin, integrin, and protease axes. [EXTERNAL] TGFB2 restrains angiogenesis downstream of VEGF–miR circuits, limiting endothelial sprouting and tube formation [PMID:25217442](https://pubmed.ncbi.nlm.nih.gov/25217442/). [INFERENCE] TGFBR2 supports vasculogenesis and branching morphogenesis by directing endothelial/perivascular differentiation through Smad signaling. [INFERENCE] EDNRA signaling tunes arterial identity and remodeling under hemodynamic cues. [EXTERNAL] SERPINE1 modulates perivascular proteolysis to shape both positive and negative angiogenic outputs during inflammation [PMID:19916862](https://pubmed.ncbi.nlm.nih.gov/19916862/).

#### Key Insights

- [EXTERNAL] TGFB2 enforces negative regulation of angiogenesis to prevent exuberant capillary morphogenesis [PMID:25217442](https://pubmed.ncbi.nlm.nih.gov/25217442/). ([GO:0016525](http://purl.obolibrary.org/obo/GO_0016525))
- [INFERENCE] Receptor‑mediated Smad signaling supports vasculogenesis and branching to pattern the vascular tree. ([GO:0001570](http://purl.obolibrary.org/obo/GO_0001570))

#### Key Genes

- **TGFBR2**: [INFERENCE] [INFERENCE] TGFBR2 drives vasculogenic differentiation and branching via Smad‑dependent patterning cues. ([GO:0001570](http://purl.obolibrary.org/obo/GO_0001570))
- **TGFB2**: [EXTERNAL] [EXTERNAL] TGFB2 limits endothelial sprouting and angiogenesis by modulating miRNA programs and anti‑migratory genes [PMID:25217442](https://pubmed.ncbi.nlm.nih.gov/25217442/). ([GO:0016525](http://purl.obolibrary.org/obo/GO_0016525))
- **EDNRA**: [INFERENCE] [INFERENCE] EDNRA signaling promotes arterial morphogenesis and smooth muscle investment to stabilize vessels. ([GO:0048844](http://purl.obolibrary.org/obo/GO_0048844))
- **SERPINE1**: [EXTERNAL] [EXTERNAL] SERPINE1 shapes angiogenesis by controlling fibrinolysis and matrix remodeling during inflammatory stimuli [PMID:19916862](https://pubmed.ncbi.nlm.nih.gov/19916862/). ([GO:0045766](http://purl.obolibrary.org/obo/GO_0045766))

#### Statistical Context

[DATA] Theme enrichment: FDR=2.19e-03 with 10.9-fold enrichment across 6 genes. [GO-HIERARCHY] Subterms span negative and positive regulation of angiogenesis, vasculogenesis, branching, and artery morphogenesis.

---

### Theme 23: podosome

**Summary:** podosome ([GO:0002102](http://purl.obolibrary.org/obo/GO_0002102))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Podosomes are actin‑rich adhesion and degradation organelles that remodel ECM and postsynaptic architecture. [EXTERNAL] LL5β‑associated scaffolds including PHLDB2 localize to podosomes and orchestrate postsynaptic remodeling at neuromuscular junctions [PMID:23525008](https://pubmed.ncbi.nlm.nih.gov/23525008/). [INFERENCE] VCL, PALLD, and TPM4 link integrin adhesions to actin cores, stabilizing podosome belts that drive matrix perforation and shape cell morphogenesis.

#### Key Insights

- [EXTERNAL] PHLDB2‑containing complexes nucleate podosome assembly to enable adhesion‑coupled remodeling [PMID:23525008](https://pubmed.ncbi.nlm.nih.gov/23525008/). ([GO:0002102](http://purl.obolibrary.org/obo/GO_0002102))
- [INFERENCE] Actin crosslinkers and scaffolds stabilize podosome cores to coordinate traction and proteolysis. ([GO:0002102](http://purl.obolibrary.org/obo/GO_0002102))

#### Key Genes

- **PHLDB2**: [EXTERNAL] [EXTERNAL] PHLDB2 partners with LL5β to assemble podosomes that drive postsynaptic differentiation and remodeling [PMID:23525008](https://pubmed.ncbi.nlm.nih.gov/23525008/). ([GO:0002102](http://purl.obolibrary.org/obo/GO_0002102))
- **VCL**: [INFERENCE] [INFERENCE] Vinculin stabilizes actin–adhesion linkages within podosomes to sustain force transmission and matrix remodeling. ([GO:0002102](http://purl.obolibrary.org/obo/GO_0002102))
- **TPM4**: [INFERENCE] [INFERENCE] TPM4 organizes podosome actin filaments to maintain structure and turnover during morphogenesis. ([GO:0002102](http://purl.obolibrary.org/obo/GO_0002102))

#### Statistical Context

[DATA] Theme enrichment: FDR=3.17e-03 with 13.4-fold enrichment across 5 genes. [GO-HIERARCHY] This cellular component anchor focuses on adhesive organelles that integrate degradation and force generation.

---

### Theme 24: response to oxygen-containing compound

**Summary:** response to oxygen-containing compound ([GO:1901700](http://purl.obolibrary.org/obo/GO_1901700))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Oxygen‑containing compounds such as ROS and LPS trigger calcium, MAPK, and transcriptional responses that adapt metabolism and immunity. [INFERENCE] ITPR2 releases ER calcium to couple oxidative signals to NF‑kB/MAPK activation and survival decisions. [EXTERNAL] Vimentin participates in NOD2‑dependent responses to LPS and muramyl dipeptide, linking cytoskeletal remodeling to inflammatory gene induction [PMID:27812135](https://pubmed.ncbi.nlm.nih.gov/27812135/). [EXTERNAL] SERPINE1 is upregulated by LPS in epithelial cells, coordinating inflammatory mediators and barrier responses [PMID:19916862](https://pubmed.ncbi.nlm.nih.gov/19916862/). [INFERENCE] FOS and SOD2 respectively amplify immediate‑early transcription and detoxify ROS to balance adaptation and damage.

#### Key Insights

- [EXTERNAL] Cytoskeletal sensors like vimentin couple LPS detection to NF‑kB/MAPK activation during cellular response to oxygen‑containing compounds [PMID:27812135](https://pubmed.ncbi.nlm.nih.gov/27812135/). ([GO:0032496](http://purl.obolibrary.org/obo/GO_0032496))
- [EXTERNAL] SERPINE1 induction by LPS modulates inflammatory and proteolytic landscapes during stress [PMID:19916862](https://pubmed.ncbi.nlm.nih.gov/19916862/). ([GO:0032496](http://purl.obolibrary.org/obo/GO_0032496))

#### Key Genes

- **FOS**: [INFERENCE] [INFERENCE] FOS orchestrates immediate‑early transcription downstream of ROS and cAMP to recalibrate signaling networks. ([GO:1901701](http://purl.obolibrary.org/obo/GO_1901701))
- **SOD2**: [INFERENCE] [INFERENCE] SOD2 clears mitochondrial superoxide to prevent ROS escalation during LPS‑driven inflammation. ([GO:0032496](http://purl.obolibrary.org/obo/GO_0032496))
- **ITPR2**: [INFERENCE] [INFERENCE] ITPR2‑mediated Ca2+ release links oxidative cues to kinase and transcription factor activation. ([GO:1901701](http://purl.obolibrary.org/obo/GO_1901701))
- **ARID5A**: [INFERENCE] [INFERENCE] ARID5A enhances transcription of stress‑responsive genes under hypoxic and inflammatory metabolite conditions to support adaptation. ([GO:1901701](http://purl.obolibrary.org/obo/GO_1901701))

#### Statistical Context

[DATA] Theme enrichment: FDR=4.04e-03 with 2.3-fold enrichment across 27 genes. [GO-HIERARCHY] Subterms include cellular response to oxygen‑containing compounds, response to lipopolysaccharide, and response to cAMP indicating diverse second‑messenger coupling.

---

### Theme 25: regulation of epithelial cell proliferation

**Summary:** regulation of epithelial cell proliferation ([GO:0050678](http://purl.obolibrary.org/obo/GO_0050678))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Epithelial proliferation is tuned by angiogenic cues and inflammatory circuits that converge on integrin/VEGF signaling and transcriptional regulators. [EXTERNAL] NRP2 relays VEGF signals to p130Cas to promote endothelial proliferation and migration, indirectly supporting epithelial growth through vascular support [PMID:21245381](https://pubmed.ncbi.nlm.nih.gov/21245381/). [EXTERNAL] EGR3 is induced by VEGF to enhance endothelial proliferation and migration, coupling angiogenic signals to tissue expansion [PMID:18059339](https://pubmed.ncbi.nlm.nih.gov/18059339/). [EXTERNAL] Tissue factor F3 promotes endothelial proliferation through coagulation‑linked signaling that interfaces with VEGF pathways [PMID:17898544](https://pubmed.ncbi.nlm.nih.gov/17898544/). [INFERENCE] STAT3 provides a transcriptional engine that sustains epithelial cell cycle entry under cytokine and growth factor stimulation.

#### Key Insights

- [EXTERNAL] VEGF–NRP2–p130Cas signaling drives regulation of endothelial cell proliferation to fuel tissue growth [PMID:21245381](https://pubmed.ncbi.nlm.nih.gov/21245381/). ([GO:0001936](http://purl.obolibrary.org/obo/GO_0001936))
- [EXTERNAL] EGR3 connects VEGF input to endothelial proliferation and migration, scaling angiogenic support for epithelia [PMID:18059339](https://pubmed.ncbi.nlm.nih.gov/18059339/). ([GO:0001936](http://purl.obolibrary.org/obo/GO_0001936))

#### Key Genes

- **NRP2**: [EXTERNAL] [EXTERNAL] NRP2 enhances VEGF‑dependent p130Cas signaling to increase endothelial proliferation and migration [PMID:21245381](https://pubmed.ncbi.nlm.nih.gov/21245381/). ([GO:0001936](http://purl.obolibrary.org/obo/GO_0001936))
- **EGR3**: [EXTERNAL] [EXTERNAL] EGR3 boosts endothelial proliferation downstream of VEGF to promote angiogenic expansion [PMID:18059339](https://pubmed.ncbi.nlm.nih.gov/18059339/). ([GO:0001936](http://purl.obolibrary.org/obo/GO_0001936))
- **F3**: [EXTERNAL] [EXTERNAL] F3 stimulates endothelial proliferation via coagulation‑driven signaling that intersects with angiogenic pathways [PMID:17898544](https://pubmed.ncbi.nlm.nih.gov/17898544/). ([GO:0001936](http://purl.obolibrary.org/obo/GO_0001936))
- **STAT3**: [INFERENCE] [INFERENCE] STAT3 activates epithelial cell cycle genes to positively regulate epithelial proliferation under cytokine input. ([GO:0050679](http://purl.obolibrary.org/obo/GO_0050679))

#### Statistical Context

[DATA] Theme enrichment: FDR=4.45e-03 with 4.4-fold enrichment across 11 genes. [GO-HIERARCHY] Subterms split endothelial versus epithelial proliferation control, reflecting vascular–epithelial coupling.

---

### Theme 26: cell-matrix adhesion

**Summary:** cell-matrix adhesion ([GO:0007160](http://purl.obolibrary.org/obo/GO_0007160))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Cell–matrix adhesion integrates integrins, scaffolds, and matrix proteases to convert mechanical ligation into survival and motility signals. [EXTERNAL] ITGAV/ITGA3 mediate binding to matrix ligands and activate inside‑out and outside‑in signaling that coordinate migration and growth factor activation, including latent TGF‑beta1 [PMID:19693543](https://pubmed.ncbi.nlm.nih.gov/19693543/), [PMID:11970960](https://pubmed.ncbi.nlm.nih.gov/11970960/). [EXTERNAL] Vinculin links integrins to actin and modulates beta‑catenin/E‑cadherin cross‑talk, coupling matrix adhesion with junctional stability [PMID:20086044](https://pubmed.ncbi.nlm.nih.gov/20086044/). [EXTERNAL] High‑affinity fibronectin–αvβ3 interactions illustrate structural mechanisms that tune integrin signaling without partial agonism [PMID:24658351](https://pubmed.ncbi.nlm.nih.gov/24658351/).

#### Key Insights

- [EXTERNAL] Integrin‑dependent cell–matrix adhesion activates signaling that also controls latent TGF‑beta1 activation to coordinate homeostasis [PMID:11970960](https://pubmed.ncbi.nlm.nih.gov/11970960/). ([GO:0007160](http://purl.obolibrary.org/obo/GO_0007160))
- [EXTERNAL] Vinculin fortifies the integrin–actin axis to stabilize adhesion and transduce force into signaling outputs [PMID:20086044](https://pubmed.ncbi.nlm.nih.gov/20086044/). ([GO:0007160](http://purl.obolibrary.org/obo/GO_0007160))

#### Key Genes

- **ITGAV**: [EXTERNAL] [EXTERNAL] ITGAV (αvβ3) binds matrix ligands to drive adhesion‑dependent signaling and TGF‑beta activation [PMID:19693543](https://pubmed.ncbi.nlm.nih.gov/19693543/), [PMID:11970960](https://pubmed.ncbi.nlm.nih.gov/11970960/). ([GO:0007160](http://purl.obolibrary.org/obo/GO_0007160))
- **ITGA3**: [EXTERNAL] [EXTERNAL] ITGA3 pairs with β subunits to anchor cells to laminin‑rich matrices and activate downstream kinases [PMID:19693543](https://pubmed.ncbi.nlm.nih.gov/19693543/). ([GO:0007160](http://purl.obolibrary.org/obo/GO_0007160))
- **VCL**: [EXTERNAL] [EXTERNAL] Vinculin links integrins to actin and modulates E‑cadherin/beta‑catenin to coordinate matrix and cell–cell adhesion [PMID:20086044](https://pubmed.ncbi.nlm.nih.gov/20086044/). ([GO:0007160](http://purl.obolibrary.org/obo/GO_0007160))
- **FN1**: [EXTERNAL] [EXTERNAL] FN1 engages αvβ3 with high affinity to shape signaling without partial agonism, reinforcing adhesion strength [PMID:24658351](https://pubmed.ncbi.nlm.nih.gov/24658351/). ([GO:0007160](http://purl.obolibrary.org/obo/GO_0007160))

#### Statistical Context

[DATA] Theme enrichment: FDR=4.74e-03 with 7.4-fold enrichment across 7 genes. [GO-HIERARCHY] This process underlies multiple motility and signaling themes through integrin–matrix coupling.

---

### Theme 27: positive regulation of intracellular signal transduction

**Summary:** positive regulation of intracellular signal transduction ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Positive regulation of intracellular signaling is achieved by co‑receptor scaffolding, stress‑MAPK activation, and PI3K/Akt potentiation. [EXTERNAL] IL1RAP augments IL‑1 receptor complexes to intensify canonical NF‑kB and MAPK cascades, scaling inflammatory outputs [PMID:10383454](https://pubmed.ncbi.nlm.nih.gov/10383454/), [PMID:33482337](https://pubmed.ncbi.nlm.nih.gov/33482337/). [EXTERNAL] GADD45B and GADD45A activate the MTK1/MEKK4 MAPKKK to drive p38 and JNK signaling under stress, enhancing transcriptional responses [PMID:9827804](https://pubmed.ncbi.nlm.nih.gov/9827804/). [EXTERNAL] MFHAS1 promotes PI3K/Akt and stress MAPKs to mitigate inflammation and shape polarization under metabolic stress [PMID:29168081](https://pubmed.ncbi.nlm.nih.gov/29168081/), [PMID:28471450](https://pubmed.ncbi.nlm.nih.gov/28471450/). [INFERENCE] IRS2 amplifies receptor tyrosine kinase inputs to PI3K signaling, reinforcing survival and metabolic control.

#### Key Insights

- [EXTERNAL] IL1RAP‑driven assembly of IL‑1 signaling complexes elevates NF‑kB/MAPK within positive regulation of intracellular signal transduction [PMID:10383454](https://pubmed.ncbi.nlm.nih.gov/10383454/), [PMID:33482337](https://pubmed.ncbi.nlm.nih.gov/33482337/). ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))
- [EXTERNAL] GADD45 family activation of MTK1/MEKK4 boosts p38/JNK cascades to expand stress‑responsive signaling [PMID:9827804](https://pubmed.ncbi.nlm.nih.gov/9827804/). ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))

#### Key Genes

- **IL1RAP**: [EXTERNAL] [EXTERNAL] IL1RAP intensifies IL‑1 receptor signaling to raise NF‑kB and MAPK activation amplitudes [PMID:10383454](https://pubmed.ncbi.nlm.nih.gov/10383454/), [PMID:33482337](https://pubmed.ncbi.nlm.nih.gov/33482337/). ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))
- **GADD45B**: [EXTERNAL] [EXTERNAL] GADD45B engages MTK1/MEKK4 to activate JNK/p38, enhancing stress signal propagation [PMID:9827804](https://pubmed.ncbi.nlm.nih.gov/9827804/). ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))
- **MFHAS1**: [EXTERNAL] [EXTERNAL] MFHAS1 promotes PI3K/Akt and p38/JNK signaling to shape inflammatory polarization and survival [PMID:29168081](https://pubmed.ncbi.nlm.nih.gov/29168081/), [PMID:28471450](https://pubmed.ncbi.nlm.nih.gov/28471450/). ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))
- **IRS2**: [INFERENCE] [INFERENCE] IRS2 scaffolds RTK inputs to PI3K, elevating downstream Akt signaling and metabolic adaptation. ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))

#### Statistical Context

[DATA] Theme enrichment: FDR=4.95e-03 with 2.4-fold enrichment across 24 genes. [GO-HIERARCHY] This process aggregates multiple amplifier nodes that raise pathway gain across kinase networks.

---

### Theme 28: network-forming collagen trimer

**Summary:** network-forming collagen trimer ([GO:0098642](http://purl.obolibrary.org/obo/GO_0098642))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Network‑forming collagens assemble into trimeric scaffolds that knit basement membranes and specialized matrices for mechanical support and signaling. [EXTERNAL] COL4A1 and COL4A2 co‑assemble as α1/α2(IV) trimers forming type IV networks essential for vascular and epithelial basement membranes, with mutations disrupting cerebral integrity [PMID:16107487](https://pubmed.ncbi.nlm.nih.gov/16107487/), [PMID:3345760](https://pubmed.ncbi.nlm.nih.gov/3345760/). [EXTERNAL] Type VIII collagen trimers from COL8A1 contribute to endothelial and corneal matrix frameworks, supporting tissue repair and architecture [PMID:9438378](https://pubmed.ncbi.nlm.nih.gov/9438378/).

#### Key Insights

- [EXTERNAL] Type IV collagen α1/α2 trimers establish network scaffolds that maintain microvascular integrity [PMID:16107487](https://pubmed.ncbi.nlm.nih.gov/16107487/), [PMID:3345760](https://pubmed.ncbi.nlm.nih.gov/3345760/). ([GO:0098642](http://purl.obolibrary.org/obo/GO_0098642))
- [EXTERNAL] Type VIII collagen trimers augment specialized matrices for endothelial function and repair [PMID:9438378](https://pubmed.ncbi.nlm.nih.gov/9438378/). ([GO:0098642](http://purl.obolibrary.org/obo/GO_0098642))

#### Key Genes

- **COL4A1**: [EXTERNAL] [EXTERNAL] COL4A1 encodes a core subunit of collagen IV trimers that polymerize into basement membrane networks critical for vessel stability [PMID:16107487](https://pubmed.ncbi.nlm.nih.gov/16107487/). ([GO:0098642](http://purl.obolibrary.org/obo/GO_0098642))
- **COL4A2**: [EXTERNAL] [EXTERNAL] COL4A2 pairs with COL4A1 in collagen IV trimers to scaffold basal lamina structure [PMID:3345760](https://pubmed.ncbi.nlm.nih.gov/3345760/). ([GO:0098642](http://purl.obolibrary.org/obo/GO_0098642))
- **COL8A1**: [EXTERNAL] [EXTERNAL] COL8A1 forms collagen VIII trimers present in endothelial and corneal matrices supporting structural integrity [PMID:9438378](https://pubmed.ncbi.nlm.nih.gov/9438378/). ([GO:0098642](http://purl.obolibrary.org/obo/GO_0098642))

#### Statistical Context

[DATA] Theme enrichment: FDR=5.50e-03 with 35.7-fold enrichment across 3 genes. [GO-HIERARCHY] This cellular component anchor isolates trimeric collagen network builders crucial to multiple matrix themes.

---

### Theme 29: response to mechanical stimulus

**Summary:** response to mechanical stimulus ([GO:0009612](http://purl.obolibrary.org/obo/GO_0009612))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Mechanical forces transduce through cytoskeletal sensors and MAPK/NF‑kB modules to adjust transcription, secretion, and barrier function. [EXTERNAL] CHI3L1 is secreted basally by airway epithelium and upregulated by compressive stress via EGFR signaling, linking mechanotransduction to inflammatory remodeling [PMID:20650887](https://pubmed.ncbi.nlm.nih.gov/20650887/). [EXTERNAL] MAP3K14 (NIK) participates in mechanical stress responses by activating NF‑kB, coordinating survival and proliferation signals under strain [PMID:19593445](https://pubmed.ncbi.nlm.nih.gov/19593445/). [INFERENCE] FOSB and GAP43 are rapidly induced or targeted to protrusions to reshape actin and transcription in response to force.

#### Key Insights

- [EXTERNAL] EGFR‑dependent induction of CHI3L1 by compression exemplifies epithelial response to mechanical stimulus [PMID:20650887](https://pubmed.ncbi.nlm.nih.gov/20650887/). ([GO:0009612](http://purl.obolibrary.org/obo/GO_0009612))
- [EXTERNAL] MAP3K14 activation under mechanical stress couples force to NF‑kB‑driven transcriptional programs [PMID:19593445](https://pubmed.ncbi.nlm.nih.gov/19593445/). ([GO:0009612](http://purl.obolibrary.org/obo/GO_0009612))

#### Key Genes

- **CHI3L1**: [EXTERNAL] [EXTERNAL] CHI3L1 secretion increases with compressive stress via EGFR signaling to drive remodeling responses [PMID:20650887](https://pubmed.ncbi.nlm.nih.gov/20650887/). ([GO:0009612](http://purl.obolibrary.org/obo/GO_0009612))
- **MAP3K14**: [EXTERNAL] [EXTERNAL] MAP3K14 links mechanical cues to NF‑kB activation to promote survival/proliferation programs [PMID:19593445](https://pubmed.ncbi.nlm.nih.gov/19593445/). ([GO:0009612](http://purl.obolibrary.org/obo/GO_0009612))
- **GAP43**: [INFERENCE] [INFERENCE] GAP43 targets to filopodia to adjust actin remodeling and growth cone dynamics under mechanical cues. ([GO:0009612](http://purl.obolibrary.org/obo/GO_0009612))

#### Statistical Context

[DATA] Theme enrichment: FDR=5.93e-03 with 5.2-fold enrichment across 9 genes. [GO-HIERARCHY] This process integrates epithelial and neuronal mechanotransduction mechanisms.

---

### Theme 30: positive regulation of osteoblast proliferation

**Summary:** positive regulation of osteoblast proliferation ([GO:0033690](http://purl.obolibrary.org/obo/GO_0033690))  · Anchor confidence: **FDR<0.01**

[INFERENCE] Osteoblast proliferation is amplified by integrin–growth factor co‑signaling that routes BMP and ERK pathways to cell cycle entry. [EXTERNAL] CCN1 engages αvβ3 to activate ILK→ERK, thereby enhancing BMP‑2‑dependent osteoblast differentiation and proliferative expansion [PMID:20675382](https://pubmed.ncbi.nlm.nih.gov/20675382/). [EXTERNAL] Lactoferrin directly stimulates osteoblast growth via receptor engagement, increasing DNA synthesis and local bone formation in vivo [PMID:15166119](https://pubmed.ncbi.nlm.nih.gov/15166119/). [INFERENCE] ITGAV integrates matrix and osteogenic growth factor cues to sustain proliferative signaling in bone microenvironments.

#### Key Insights

- [EXTERNAL] CCN1–αvβ3–ILK–ERK signaling augments BMP‑2 programs to positively regulate osteoblast proliferation [PMID:20675382](https://pubmed.ncbi.nlm.nih.gov/20675382/). ([GO:0033690](http://purl.obolibrary.org/obo/GO_0033690))
- [EXTERNAL] Lactoferrin directly increases osteoblast proliferation, promoting bone anabolism [PMID:15166119](https://pubmed.ncbi.nlm.nih.gov/15166119/). ([GO:0033690](http://purl.obolibrary.org/obo/GO_0033690))

#### Key Genes

- **CCN1**: [EXTERNAL] [EXTERNAL] CCN1 potentiates BMP‑2 osteogenic signaling via αvβ3–ILK–ERK to expand osteoblast populations [PMID:20675382](https://pubmed.ncbi.nlm.nih.gov/20675382/). ([GO:0033690](http://purl.obolibrary.org/obo/GO_0033690))
- **LTF**: [EXTERNAL] [EXTERNAL] LTF stimulates osteoblast proliferation and bone formation through receptor‑mediated signaling [PMID:15166119](https://pubmed.ncbi.nlm.nih.gov/15166119/). ([GO:0033690](http://purl.obolibrary.org/obo/GO_0033690))
- **ITGAV**: [INFERENCE] [INFERENCE] ITGAV integrates osteogenic matrix and growth factor signals to sustain proliferative pathways in osteoblasts. ([GO:0033690](http://purl.obolibrary.org/obo/GO_0033690))

#### Statistical Context

[DATA] Theme enrichment: FDR=6.24e-03 with 35.7-fold enrichment across 3 genes. [GO-HIERARCHY] This narrowly focused process highlights integrin–growth factor synergy in osteogenesis.

---

## Hub Genes

- **STAT3**: [EXTERNAL] [DATA] STAT3 is a DNA‑binding transcription activator and positive regulator of RNA polymerase II transcription that links cytokine and TGF‑beta receptor signals to migratory and survival gene programs [PMID:31886314](https://pubmed.ncbi.nlm.nih.gov/31886314/), [PMID:28467929](https://pubmed.ncbi.nlm.nih.gov/28467929/). [EXTERNAL] Cross‑theme activity includes promotion of cell migration and coordination of inflammatory outputs across enzyme‑linked receptor and transcription themes [PMID:31638206](https://pubmed.ncbi.nlm.nih.gov/31638206/).
- **ITGAV**: [EXTERNAL] [EXTERNAL] ITGAV (αvβ3) binds growth factors including IGF‑1 and FGF1 to co‑signal with RTKs, and localizes to cell surface microdomains and filopodia to organize adhesion, entry, and motility [PMID:19578119](https://pubmed.ncbi.nlm.nih.gov/19578119/), [PMID:18441324](https://pubmed.ncbi.nlm.nih.gov/18441324/), [PMID:25063885](https://pubmed.ncbi.nlm.nih.gov/25063885/). [EXTERNAL] It also participates in cell‑matrix adhesion and cytokine/chemokine co‑reception to integrate mechanical and chemotactic cues [PMID:19693543](https://pubmed.ncbi.nlm.nih.gov/19693543/), [PMID:23125415](https://pubmed.ncbi.nlm.nih.gov/23125415/).
- **FN1**: [EXTERNAL] [EXTERNAL] FN1 strengthens substrate‑dependent migration and binds proteases to shape ECM remodeling, thereby coordinating locomotion with matrix turnover [PMID:25834989](https://pubmed.ncbi.nlm.nih.gov/25834989/), [PMID:22952693](https://pubmed.ncbi.nlm.nih.gov/22952693/). [INFERENCE] Its widespread participation across adhesion and basement membrane themes positions FN1 as a structural and signaling hub.
- **TGFB2**: [EXTERNAL] [EXTERNAL] TGFB2 is progesterone‑responsive and suppresses endothelial sprouting by activating Smad programs and miRNA circuits, linking endocrine signals to angiogenesis control [PMID:18039789](https://pubmed.ncbi.nlm.nih.gov/18039789/), [PMID:25217442](https://pubmed.ncbi.nlm.nih.gov/25217442/). [INFERENCE] It broadly coordinates adhesion and proliferation themes through context‑dependent Smad transcription.
- **TGFBR2**: [EXTERNAL] [EXTERNAL] TGFBR2 binds TGF‑beta and drives Smad activation from membrane rafts, modulating adhesion, EMT, and vascular morphogenesis [PMID:18453574](https://pubmed.ncbi.nlm.nih.gov/18453574/), [PMID:28131417](https://pubmed.ncbi.nlm.nih.gov/28131417/), [PMID:25893292](https://pubmed.ncbi.nlm.nih.gov/25893292/). [INFERENCE] Its appearance across signaling and adhesion themes reflects its role in tuning receptor compartmentalization and gene programs.
- **HIF1A**: [EXTERNAL] [EXTERNAL] HIF1A activates transcription and miRNA production during hypoxia to promote migration, angiogenesis, and anti‑apoptotic programs [PMID:26879375](https://pubmed.ncbi.nlm.nih.gov/26879375/), [PMID:24983504](https://pubmed.ncbi.nlm.nih.gov/24983504/), [PMID:33108349](https://pubmed.ncbi.nlm.nih.gov/33108349/). [EXTERNAL] It also drives inflammatory transcription under metabolic stress, connecting oxygen sensing to immune activation [PMID:32697943](https://pubmed.ncbi.nlm.nih.gov/32697943/).
- **NR4A3**: [EXTERNAL] [EXTERNAL] NR4A3 transactivates genes in PDGF signaling and promotes monocyte aggregation, linking growth factor sensing with inflammatory adhesion [PMID:23554459](https://pubmed.ncbi.nlm.nih.gov/23554459/), [PMID:20558821](https://pubmed.ncbi.nlm.nih.gov/20558821/). [INFERENCE] Its cross‑theme presence reflects broad coupling of locomotion, cytokine, and transcriptional regulation.
- **FOS**: [EXTERNAL] [DATA] FOS in the AP‑1 complex co‑activates Smad transcription and drives Pol II gene programs, including microRNA transcription that remodels focal adhesion signaling [PMID:10508860](https://pubmed.ncbi.nlm.nih.gov/10508860/), [PMID:9732876](https://pubmed.ncbi.nlm.nih.gov/9732876/), [PMID:30670568](https://pubmed.ncbi.nlm.nih.gov/30670568/). [INFERENCE] Its rapid inducibility positions it as a coordinator of multiple responsive themes.
- **CD44**: [EXTERNAL] [EXTERNAL] CD44 binds hyaluronan to promote monocyte aggregation and interface with growth factor signaling, linking membrane rafts to immune adhesion [PMID:20522558](https://pubmed.ncbi.nlm.nih.gov/20522558/). [INFERENCE] Its roles extend across apoptosis resistance and locomotion via matrix engagement.
- **SORBS1**: [INFERENCE] [INFERENCE] SORBS1 scaffolds integrin–actin linkages at adhesion sites and organizes receptors in membrane rafts to potentiate signaling during mechanical and cytokine responses.
- **CCL2**: [EXTERNAL] [EXTERNAL] CCL2 shapes endothelial proliferation and chemotaxis while modulating inflammatory angiogenesis, thereby influencing locomotion and vascular themes [PMID:25466836](https://pubmed.ncbi.nlm.nih.gov/25466836/). [INFERENCE] Its CCR2‑driven axes interconnect cytokine response and migration control.
- **CLU**: [INFERENCE] [INFERENCE] CLU chaperones extracellular ligands and apoptotic cell components to adjust survival signaling and immune modulation across apoptosis and surface themes.
- **ANXA2**: [EXTERNAL] [EXTERNAL] ANXA2 binds proteases such as PCSK9 and organizes membrane‑proximal activities that affect adhesion, transcriptional outputs, and raft signaling [PMID:22848640](https://pubmed.ncbi.nlm.nih.gov/22848640/). [INFERENCE] It links basement membrane remodeling with receptor regulation.
- **C3**: [INFERENCE] [INFERENCE] C3 cleavage products orchestrate opsonization and inflammatory signaling at the cell surface, intersecting with angiogenesis and activation themes.
- **HAS2**: [EXTERNAL] [EXTERNAL] HAS2 synthesizes hyaluronan that engages CD44 to drive monocyte aggregation and regulate locomotion and cytokine responses [PMID:20522558](https://pubmed.ncbi.nlm.nih.gov/20522558/). [INFERENCE] Its matrix outputs influence raft organization and survival pathways.
- **EDNRA**: [EXTERNAL] [EXTERNAL] EDNRA activates cAMP/PKA signaling in response to endothelin‑1 to regulate vascular morphogenesis and wound responses, coupling GPCR inputs to kinase cassettes [PMID:30990108](https://pubmed.ncbi.nlm.nih.gov/30990108/). [INFERENCE] It coordinates locomotion and oxygen‑compound responses via vasomotor control.
- **ZFP36**: [EXTERNAL] [DATA] ZFP36 binds cytokine and chemokine mRNAs including TNF and CCL3 to destabilize them, limiting excessive inflammatory signaling across cytokine and external stimulus themes [PMID:20166898](https://pubmed.ncbi.nlm.nih.gov/20166898/), [PMID:21784977](https://pubmed.ncbi.nlm.nih.gov/21784977/). [INFERENCE] It thereby indirectly tunes migration and survival programs.
- **IRS2**: [INFERENCE] [INFERENCE] IRS2 scaffolds receptor tyrosine kinases to PI3K/Akt, enhancing intracellular signal transduction that intersects with apoptosis restraint and growth factor signaling.
- **SERPINE1**: [EXTERNAL] [EXTERNAL] SERPINE1 restrains fibrinolysis to control matrix remodeling, chemotaxis, and angiogenesis, linking external stimuli to locomotion and vascular themes [PMID:19916862](https://pubmed.ncbi.nlm.nih.gov/19916862/). [INFERENCE] Its actions also impact apoptotic susceptibility through ECM cues.
- **PDPN**: [EXTERNAL] [EXTERNAL] PDPN localizes to membrane rafts and filopodia where it activates RhoA via ERM binding, coordinating motility, raft signaling, and apoptosis resistance [PMID:21376833](https://pubmed.ncbi.nlm.nih.gov/21376833/), [PMID:17046996](https://pubmed.ncbi.nlm.nih.gov/17046996/). [INFERENCE] This positions PDPN at the interface of migration and signaling microdomains.

## Overall Summary

[DATA] The enrichment landscape from 184 annotated human genes reveals 313 significant GO terms distilled into 72 themes, with strongest signals in stimulus‑responsive transcription, adhesion/migration modules, cytokine signaling, and ECM organization.

[GO-HIERARCHY] Anchor components such as transcription factor AP‑1 complex, membrane raft, basement membrane, and collagen trimer terms scaffold numerous process themes spanning locomotion, apoptosis restraint, and vascular morphogenesis.

[INFERENCE] Mechanistically, integrin–growth factor co‑reception and TGF‑beta/Smad–AP‑1 cooperation recur as central motifs that route extracellular cues to RNA polymerase II and microRNA programs controlling movement, proliferation, and survival.

[INFERENCE] Stress‑adaptive signaling cassettes integrating MAPK, PI3K/Akt, and integrated stress response couple oxygen‑compound, cytokine, and mechanical inputs to calibrated inflammatory and anti‑apoptotic outputs.

[DATA] Cross‑theme hub genes including STAT3, ITGAV, HIF1A, TGFB2/TGFBR2, FOS, and HAS2 connect multiple enriched leaves such as transforming growth factor beta receptor signaling pathway, growth factor binding, positive regulation of cell migration, and positive regulation of miRNA transcription, underscoring coordinated network control.

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

