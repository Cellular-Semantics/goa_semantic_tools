# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_5_themes.csv](Cluster_5_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-negative-regulation-of-amyloid-beta-formation) | [negative regulation of amyloid-beta formation](#theme-1-negative-regulation-of-amyloid-beta-formation) [GO:1902430](http://purl.obolibrary.org/obo/GO_1902430) | BP | 1.39e-03 | 5 | FDR<0.01 |
| [2](#theme-2-cytoskeleton-organization) | [cytoskeleton organization](#theme-2-cytoskeleton-organization) [GO:0007010](http://purl.obolibrary.org/obo/GO_0007010) | BP | 1.39e-03 | 25 | FDR<0.01 |
| [3](#theme-3-camp-metabolic-process) | [cAMP metabolic process](#theme-3-camp-metabolic-process) [GO:0046058](http://purl.obolibrary.org/obo/GO_0046058) | BP | 4.48e-03 | 5 | FDR<0.01 |
| [4](#theme-4-plasma-membrane-region) | [plasma membrane region](#theme-4-plasma-membrane-region) [GO:0098590](http://purl.obolibrary.org/obo/GO_0098590) | CC | 6.93e-03 | 27 | FDR<0.01 |
| [5](#theme-5-cell-cell-adhesion) | [cell-cell adhesion](#theme-5-cell-cell-adhesion) [GO:0098609](http://purl.obolibrary.org/obo/GO_0098609) | BP | 1.04e-02 | 16 | FDR<0.05 |
| [6](#theme-6-glutamatergic-synapse) | [glutamatergic synapse](#theme-6-glutamatergic-synapse) [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) | CC | 2.35e-02 | 15 | FDR<0.05 |
| [7](#theme-7-membrane-raft) | [membrane raft](#theme-7-membrane-raft) [GO:0045121](http://purl.obolibrary.org/obo/GO_0045121) | CC | 2.70e-02 | 10 | FDR<0.05 |
| [8](#theme-8-cell-surface) | [cell surface](#theme-8-cell-surface) [GO:0009986](http://purl.obolibrary.org/obo/GO_0009986) | CC | 2.70e-02 | 16 | FDR<0.05 |
| [9](#theme-9-cell-substrate-junction) | [cell-substrate junction](#theme-9-cell-substrate-junction) [GO:0030055](http://purl.obolibrary.org/obo/GO_0030055) | CC | 2.70e-02 | 12 | FDR<0.05 |
| [10](#theme-10-adherens-junction) | [adherens junction](#theme-10-adherens-junction) [GO:0005912](http://purl.obolibrary.org/obo/GO_0005912) | CC | 2.91e-02 | 8 | FDR<0.05 |
| [11](#theme-11-negative-regulation-of-cell-motility) | [negative regulation of cell motility](#theme-11-negative-regulation-of-cell-motility) [GO:2000146](http://purl.obolibrary.org/obo/GO_2000146) | BP | 3.32e-02 | 11 | FDR<0.05 |
| [12](#theme-12-actin-cytoskeleton) | [actin cytoskeleton](#theme-12-actin-cytoskeleton) [GO:0015629](http://purl.obolibrary.org/obo/GO_0015629) | CC | 3.68e-02 | 9 | FDR<0.05 |
| [13](#theme-13-neuron-projection) | [neuron projection](#theme-13-neuron-projection) [GO:0043005](http://purl.obolibrary.org/obo/GO_0043005) | CC | 3.68e-02 | 21 | FDR<0.05 |

---

### Theme 1: negative regulation of amyloid-beta formation

**Summary:** negative regulation of amyloid-beta formation ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))  · Anchor confidence: **FDR<0.01**

SORL1 diverts APP from amyloidogenic endosomes to Golgi/lysosomal routes, reducing substrate availability for γ-secretase and thereby lowering Aβ generation [DATA] [PMID:24523320](https://pubmed.ncbi.nlm.nih.gov/24523320/), [PMID:22621900](https://pubmed.ncbi.nlm.nih.gov/22621900/), [PMID:24001769](https://pubmed.ncbi.nlm.nih.gov/24001769/). [INFERENCE] NTRK2 and RTN1 both interface with γ-secretase-associated machinery to bias APP processing away from Aβ production without perturbing Notch, indicating selective modulation of intramembrane proteolysis that spares essential signaling substrates. [DATA] APOE facilitates receptor-mediated uptake and intracellular clearance of Aβ assemblies, decreasing the pool of extracellular Aβ that feeds plaque growth and synaptotoxic spread [PMID:24154541](https://pubmed.ncbi.nlm.nih.gov/24154541/). [GO-HIERARCHY] Together these mechanisms converge on the [GO:1902430](http://purl.obolibrary.org/obo/GO_1902430) node by acting upstream of peptide biogenesis, cargo routing, and extracellular clearance to achieve negative regulation of amyloid-beta formation. [EXTERNAL] LR11/SorLA-dependent trafficking alters APP’s intracellular itinerary such that BACE1 access is limited, providing a mechanistic basis for reduced Aβ levels [PMID:22621900](https://pubmed.ncbi.nlm.nih.gov/22621900/).

#### Key Insights

- Endosomal sorting of APP by SORL1 reduces BACE1 access and curtails Aβ production. [DATA] [PMID:24523320](https://pubmed.ncbi.nlm.nih.gov/24523320/), [PMID:22621900](https://pubmed.ncbi.nlm.nih.gov/22621900/), [PMID:24001769](https://pubmed.ncbi.nlm.nih.gov/24001769/) ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- Selective tuning of γ-secretase-associated steps by NTRK2 and RTN1 can lower Aβ without compromising Notch processing. [DATA] [PMID:26094765](https://pubmed.ncbi.nlm.nih.gov/26094765/) ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- ApoE-mediated binding and uptake of Aβ lowers the effective formation rate by accelerating clearance. [DATA] [PMID:24154541](https://pubmed.ncbi.nlm.nih.gov/24154541/) ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))

#### Key Genes

- **SORL1**: [EXTERNAL] SORL1 sorts APP away from amyloidogenic compartments toward Golgi/lysosomal pathways, reducing Aβ generation ([PMID:24523320](https://pubmed.ncbi.nlm.nih.gov/24523320/); [PMID:22621900](https://pubmed.ncbi.nlm.nih.gov/22621900/); [PMID:24001769](https://pubmed.ncbi.nlm.nih.gov/24001769/)). ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- **NTRK2**: [EXTERNAL] NTRK2 associates with γ-secretase regulatory context to diminish Aβ production while sparing Notch processing ([PMID:26094765](https://pubmed.ncbi.nlm.nih.gov/26094765/)). ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- **RTN1**: [EXTERNAL] RTN1 modulates γ-secretase-dependent cleavage of APP to curb Aβ generation without altering Notch processing ([PMID:26094765](https://pubmed.ncbi.nlm.nih.gov/26094765/)). ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- **APOE**: [EXTERNAL] APOE promotes receptor-mediated uptake and intracellular clearance of Aβ, reducing its accumulation ([PMID:24154541](https://pubmed.ncbi.nlm.nih.gov/24154541/)). ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))

#### Statistical Context

This theme shows strong enrichment with FDR 1.39e-03 and 35.7-fold overrepresentation among 5 genes mapped to the process. [DATA] The signal is high-confidence (FDR<0.01) and reflects a focused APP trafficking and γ-secretase modulation axis captured by [GO:1902430](http://purl.obolibrary.org/obo/GO_1902430). [GO-HIERARCHY]

---

### Theme 2: cytoskeleton organization

**Summary:** cytoskeleton organization ([GO:0007010](http://purl.obolibrary.org/obo/GO_0007010))  · Anchor confidence: **FDR<0.01**

Microtubule–actin coordination nodes steer polarity and spindle orientation while remodeling specialized structures such as axonemes and septin rings to organize the cytoskeleton at multiple scales. [INFERENCE] CFAP43 stabilizes the axonemal microtubule scaffold during flagellogenesis, illustrating how dedicated subassemblies enforce architecture and motility in a lineage-specific cytoskeletal program [PMID:29449551](https://pubmed.ncbi.nlm.nih.gov/29449551/). [EXTERNAL] KANK1-driven capture of cortical microtubules at focal adhesions links adhesome signaling to microtubule stabilization, coupling adhesion turnover to polarity and directed movement [PMID:27410476](https://pubmed.ncbi.nlm.nih.gov/27410476/). [EXTERNAL] DOCK7-dependent septin ring organization and GJA1 control of mitotic spindle orientation show how Rho-family GEF signaling and gap-junction scaffolding tune cytoskeletal patterning in post-mitotic and proliferative contexts [PMID:29467281](https://pubmed.ncbi.nlm.nih.gov/29467281/), [PMID:30992345](https://pubmed.ncbi.nlm.nih.gov/30992345/). [GO-HIERARCHY] Collectively these mechanisms instantiate the parent process [GO:0007010](http://purl.obolibrary.org/obo/GO_0007010) by coordinating filament nucleation, crosslinking, and spatial capture to shape cellular form and mechanics.

#### Key Insights

- Axonemal assembly by CFAP43 exemplifies lineage-specific cytoskeletal organization enforcing stable microtubule arrays. [DATA] [PMID:29449551](https://pubmed.ncbi.nlm.nih.gov/29449551/) ([GO:0007010](http://purl.obolibrary.org/obo/GO_0007010))
- Adhesion-coupled cortical microtubule capture via KANK1 integrates focal adhesion signaling with polarity cues. [DATA] [PMID:27410476](https://pubmed.ncbi.nlm.nih.gov/27410476/) ([GO:0007010](http://purl.obolibrary.org/obo/GO_0007010))
- GEF- and gap junction–mediated control of septins and spindle orientation provides higher-order cytoskeletal patterning. [DATA] [PMID:29467281](https://pubmed.ncbi.nlm.nih.gov/29467281/), [PMID:30992345](https://pubmed.ncbi.nlm.nih.gov/30992345/) ([GO:0007010](http://purl.obolibrary.org/obo/GO_0007010))

#### Key Genes

- **NCKAP5**: [INFERENCE] NCKAP5 is proposed to coordinate actin–microtubule interfaces that stabilize polarity and spindle orientation in epithelial cells. ([GO:0007010](http://purl.obolibrary.org/obo/GO_0007010))
- **CFAP43**: [EXTERNAL] CFAP43 supports sperm axoneme assembly, maintaining ordered microtubule doublets necessary for motility ([PMID:29449551](https://pubmed.ncbi.nlm.nih.gov/29449551/)). ([GO:0007010](http://purl.obolibrary.org/obo/GO_0007010))
- **FIGN**: [INFERENCE] FIGN is implicated in tuning cytoskeletal reorganization through motor–adaptor networks that align microtubule dynamics with cell division and trafficking. ([GO:0007010](http://purl.obolibrary.org/obo/GO_0007010))
- **FMN2**: [INFERENCE] FMN2 promotes actin filament assembly that feeds back on microtubule behavior to stabilize protrusions and adhesion-coupled structures. ([GO:0007010](http://purl.obolibrary.org/obo/GO_0007010))

#### Statistical Context

Cytoskeleton organization is enriched 3.2-fold at FDR 1.39e-03 across 25 annotated genes, indicating a broad but coherent remodeling program. [DATA] The anchor term [GO:0007010](http://purl.obolibrary.org/obo/GO_0007010) aggregates actin, microtubule, and septin regulation consistent with multipathway contributions observed here. [GO-HIERARCHY]

---

### Theme 3: cAMP metabolic process

**Summary:** cAMP metabolic process ([GO:0046058](http://purl.obolibrary.org/obo/GO_0046058))  · Anchor confidence: **FDR<0.01**

Adenylyl cyclases (ADCY2, ADCY8) synthesize cAMP downstream of GPCR activation, while PDE8A and PDE8B create high-affinity degradation sinks that sculpt spatial and temporal second-messenger gradients. [INFERENCE] This push–pull enzymatic architecture gates PKA and Epac activation thresholds, aligning metabolic output with receptor occupancy and synaptic input strength. [INFERENCE] Receptor coupling via ADCYAP1R1 provides feed-forward recruitment of adenylyl cyclase to rapidly elevate cAMP in membrane nanodomains that propagate signaling to downstream effectors. [INFERENCE]

#### Key Insights

- Parallel adenylyl cyclases and PDE8 isoforms implement a producer–degrader circuit that shapes cAMP microdomains and downstream kinase activation. [INFERENCE] ([GO:0046058](http://purl.obolibrary.org/obo/GO_0046058))
- PACAP receptor coupling to adenylyl cyclase accelerates cAMP rise time in response to neuropeptide cues. [INFERENCE] ([GO:0046058](http://purl.obolibrary.org/obo/GO_0046058))

#### Key Genes

- **PDE8A**: [INFERENCE] PDE8A hydrolyzes cAMP with high affinity, restricting second-messenger spread and tuning PKA signaling windows. ([GO:0046058](http://purl.obolibrary.org/obo/GO_0046058))
- **PDE8B**: [INFERENCE] PDE8B degrades cAMP to confine signaling to specific compartments and set responsiveness to hormonal stimulation. ([GO:0046058](http://purl.obolibrary.org/obo/GO_0046058))
- **ADCY2**: [INFERENCE] ADCY2 converts ATP to cAMP upon GPCR–Gαs activation, initiating PKA/Epac cascades that regulate neuronal and metabolic outputs. ([GO:0046058](http://purl.obolibrary.org/obo/GO_0046058))
- **ADCY8**: [INFERENCE] ADCY8 produces cAMP in response to Ca2+/calmodulin and GPCR inputs, supporting synaptic plasticity and cAMP-dependent transcription. ([GO:0046058](http://purl.obolibrary.org/obo/GO_0046058))

#### Statistical Context

The cAMP metabolic process shows 24.3-fold enrichment at FDR 4.48e-03 with 5 genes, indicating a tightly focused second-messenger module. [DATA] [GO:0046058](http://purl.obolibrary.org/obo/GO_0046058) captures both synthesis and degradation arms reflected by the adenylyl cyclase and PDE representation. [GO-HIERARCHY]

---

### Theme 4: plasma membrane region

**Summary:** plasma membrane region ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))  · Anchor confidence: **FDR<0.01**

Signal scaffolds, receptors, and transporters partition into apical, basolateral, and protrusive subregions to spatially organize inputs and cytoskeletal effectors at the plasma membrane. [GO-HIERARCHY] CD44 concentrates at apical and lamellipodial membranes where it couples hyaluronan binding to Rho-family remodeling, positioning adhesion and migration machinery at specific membrane territories [PMID:20962267](https://pubmed.ncbi.nlm.nih.gov/20962267/). [EXTERNAL] Caveolar localization of NOS1AP illustrates how PDZ-scaffolded signaling modules embed within plasma membrane subcompartments to control NO and cAMP cross-talk. [DATA] GABA and glutamate receptor subunits (for example GABRB1 and GRIK1) anchor ion flux to defined membrane nanodomains to tune excitability and synaptic gain. [INFERENCE]

#### Key Insights

- Apical and protrusive membrane partitioning of CD44 coordinates ligand engagement with localized actin remodeling. [DATA] [PMID:20962267](https://pubmed.ncbi.nlm.nih.gov/20962267/) ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))
- Caveola-associated NOS1AP exemplifies scaffolded signaling in plasma membrane microdomains. [DATA] [PMID:19800018](https://pubmed.ncbi.nlm.nih.gov/19800018/) ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))

#### Key Genes

- **AKAP6**: [INFERENCE] AKAP6 anchors cAMP effectors at defined plasma membrane regions to integrate receptor inputs with cytoskeletal responses. ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))
- **GRIK1**: [INFERENCE] GRIK1 assembles into kainate receptors at the plasma membrane to mediate cation influx and excitatory drive in defined synaptic locales. ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))
- **GABRB1**: [INFERENCE] GABRB1 contributes to GABAA receptor complexes at the plasma membrane where Cl− influx dampens neuronal excitability. ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))
- **AHCYL1**: [INFERENCE] AHCYL1 modulates membrane-associated small GTPase signaling impacting polarity and microvillar organization. ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))

#### Statistical Context

This cellular compartment term is enriched 2.5-fold at FDR 6.93e-03 across 27 genes, indicating broad redistribution of signaling complexes to specific plasma membrane regions. [DATA] [GO:0098590](http://purl.obolibrary.org/obo/GO_0098590) subsumes apical, basolateral, and protrusive microdomains, matching the observed diversity of localizations. [GO-HIERARCHY]

---

### Theme 5: cell-cell adhesion

**Summary:** cell-cell adhesion ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))  · Anchor confidence: **FDR<0.05**

Cadherins, integrins, protocadherins, and guidance receptors assemble adhesive interfaces that physically link neighboring cells while coupling force to signaling for tissue patterning. [INFERENCE] PTPRT’s extracellular homophilic binding and intracellular phosphatase activity strengthen adherens contacts by dephosphorylating junctional substrates, directly supporting stable intercellular adhesion [PMID:18644975](https://pubmed.ncbi.nlm.nih.gov/18644975/). [DATA] ROBO2 mediates homophilic interactions that promote neurite outgrowth, illustrating how axon guidance receptors can simultaneously enforce cell–cell apposition and directional growth [PMID:12504588](https://pubmed.ncbi.nlm.nih.gov/12504588/). [EXTERNAL] CD99 and SPARCL1 contribute to adhesion complex maturation and extracellular matrix engagement that reinforce junctional stability and collective behavior. [INFERENCE]

#### Key Insights

- Phosphatase-tuned cadherin complexes via PTPRT stabilize adhesion by reducing inhibitory phosphorylation at junctions. [DATA] [PMID:18644975](https://pubmed.ncbi.nlm.nih.gov/18644975/) ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- Homophilic ROBO2 binding exemplifies guidance-linked intercellular adhesion that promotes coordinated neurite extension. [EXTERNAL] [PMID:12504588](https://pubmed.ncbi.nlm.nih.gov/12504588/) ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))

#### Key Genes

- **SPARCL1**: [INFERENCE] SPARCL1 enhances integrin–ECM coupling that secondarily stabilizes cadherin-based contacts during tissue organization. ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **CD99**: [INFERENCE] CD99 supports adhesion complex maturation and cytoskeletal linkage that strengthen intercellular junctions. ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **PTPRT**: [EXTERNAL] PTPRT promotes homophilic adhesion and dephosphorylates junctional substrates to reinforce cell–cell adhesion ([PMID:18644975](https://pubmed.ncbi.nlm.nih.gov/18644975/)). ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **ROBO2**: [EXTERNAL] ROBO2 engages in homophilic binding that promotes neurite outgrowth while maintaining intercellular apposition ([PMID:12504588](https://pubmed.ncbi.nlm.nih.gov/12504588/)). ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))

#### Statistical Context

Cell–cell adhesion is enriched 3.8-fold at FDR 1.04e-02 with 16 genes, highlighting a coordinated reinforcement of intercellular junctions. [DATA] [GO:0098609](http://purl.obolibrary.org/obo/GO_0098609) captures cadherin and guidance-receptor contributions concordant with the gene set composition. [GO-HIERARCHY]

---

### Theme 6: glutamatergic synapse

**Summary:** glutamatergic synapse ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))  · Anchor confidence: **FDR<0.05**

Postsynaptic scaffolds and receptors coordinate actin remodeling and receptor trafficking to tune excitatory transmission at glutamatergic synapses. [INFERENCE] GRIK1-encoded GluK1 assembles kainate receptors that gate Na+/Ca2+ flux and shape short- and long-term synaptic efficacy, with structural determinants supporting subunit-specific functional diversity [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/), [PMID:21893069](https://pubmed.ncbi.nlm.nih.gov/21893069/). [DATA] NRG3 signaling modulates synaptic plasticity in orbitofrontal circuits, linking growth factor inputs to glutamatergic tuning of cognition [PMID:29114105](https://pubmed.ncbi.nlm.nih.gov/29114105/). [EXTERNAL] NOS1AP-dependent actin remodeling reduces functional glutamate receptor content and mEPSC amplitude, illustrating how cytoskeletal control dictates receptor endocytosis and synaptic strength [PMID:26869880](https://pubmed.ncbi.nlm.nih.gov/26869880/). [EXTERNAL]

#### Key Insights

- GluK1-containing kainate receptors diversify excitatory signaling and plasticity through subunit-specific ion channel properties. [DATA] [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/), [PMID:21893069](https://pubmed.ncbi.nlm.nih.gov/21893069/) ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- Growth factor signaling via NRG3 modulates glutamatergic plasticity at cortical circuits. [DATA] [PMID:29114105](https://pubmed.ncbi.nlm.nih.gov/29114105/) ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Key Genes

- **GRIK1**: [EXTERNAL] GRIK1 forms kainate receptors that mediate excitatory cation flux and regulate synaptic gain ([PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/); [PMID:21893069](https://pubmed.ncbi.nlm.nih.gov/21893069/)). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **NRG3**: [EXTERNAL] NRG3 signaling adjusts glutamatergic plasticity in orbitofrontal cortex, linking trophic cues to synaptic function ([PMID:29114105](https://pubmed.ncbi.nlm.nih.gov/29114105/)). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **CADPS**: [INFERENCE] CADPS promotes Ca2+-regulated vesicle priming and release that sustains glutamatergic neurotransmission. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **DAPK1**: [INFERENCE] DAPK1 influences postsynaptic actin and spine stability, modulating receptor content and excitatory transmission. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Statistical Context

Glutamatergic synapse components are enriched 3.2-fold at FDR 2.35e-02 across 15 genes, indicating remodeling of excitatory postsynaptic architecture. [DATA] [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) aggregates receptors, scaffolds, and signaling proteins consistent with the observed gene set. [GO-HIERARCHY]

---

### Theme 7: membrane raft

**Summary:** membrane raft ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))  · Anchor confidence: **FDR<0.05**

Lipid rafts concentrate signaling enzymes, adhesion receptors, and scaffolds to accelerate reaction kinetics and control endocytosis at the membrane. [INFERENCE] ABCA1 associates with flotillin-rich rafts to couple cholesterol efflux with vesicular trafficking and enhanced phagocytic capacity, illustrating lipid-handling functions embedded in raft microdomains [PMID:15469992](https://pubmed.ncbi.nlm.nih.gov/15469992/). [DATA] CD44 palmitoylation drives raft localization that is required for hyaluronan endocytosis, linking extracellular matrix sensing to compartmentalized uptake and signaling [PMID:16945930](https://pubmed.ncbi.nlm.nih.gov/16945930/). [DATA] NOS1AP occupancy of caveolae places NO and cAMP cross-talk within raft-adjacent nanodomains that influence cardiomyocyte signaling. [DATA]

#### Key Insights

- Raft residency of ABCA1 and CD44 enables coordinated lipid efflux and hyaluronan endocytosis within specialized microdomains. [DATA] [PMID:15469992](https://pubmed.ncbi.nlm.nih.gov/15469992/), [PMID:16945930](https://pubmed.ncbi.nlm.nih.gov/16945930/) ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))
- Caveolar scaffolding of NOS1AP situates nitric oxide signaling within raft-associated compartments for efficient cross-talk. [DATA] [PMID:19800018](https://pubmed.ncbi.nlm.nih.gov/19800018/) ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))

#### Key Genes

- **AKAP6**: [INFERENCE] AKAP6 organizes cAMP effectors within raft-enriched locales to integrate receptor signals with local kinase activity. ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))
- **ABCA1**: [EXTERNAL] ABCA1 associates with flotillin-1–positive rafts to drive cholesterol/phospholipid export and phagocytic vesicle dynamics ([PMID:15469992](https://pubmed.ncbi.nlm.nih.gov/15469992/)). ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))
- **CD44**: [EXTERNAL] CD44 requires raft association for hyaluronan endocytosis and downstream signaling ([PMID:16945930](https://pubmed.ncbi.nlm.nih.gov/16945930/)). ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))
- **NOS1AP**: [EXTERNAL] NOS1AP localizes to caveolae, positioning NO signaling within raft-associated membrane microdomains ([PMID:19800018](https://pubmed.ncbi.nlm.nih.gov/19800018/)). ([GO:0045121](http://purl.obolibrary.org/obo/GO_0045121))

#### Statistical Context

Membrane raft is enriched 4.2-fold at FDR 2.70e-02 with 10 genes, consistent with a reorganization of signaling into lipid microdomains. [DATA] [GO:0045121](http://purl.obolibrary.org/obo/GO_0045121) captures flotillin- and caveola-associated nanocompartments represented in the set. [GO-HIERARCHY]

---

### Theme 8: cell surface

**Summary:** cell surface ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))  · Anchor confidence: **FDR<0.05**

Cell-surface receptors, transporters, and adhesion molecules coordinate environmental sensing with downstream cytoskeletal and metabolic responses. [INFERENCE] The Na+-HCO3− cotransporter SLC4A4 operates at the cell surface to regulate intracellular pH and ion homeostasis, shaping signaling competence across epithelia and neurons [PMID:29500354](https://pubmed.ncbi.nlm.nih.gov/29500354/). [DATA] PTPRT’s extracellular domain confers adhesive recognition while its phosphatase domains tune signaling at the surface to restrain motility and stabilize contacts [PMID:18644975](https://pubmed.ncbi.nlm.nih.gov/18644975/). [EXTERNAL] Integrin β4–containing receptors and lipid transporters such as ABCA1 anchor survival and lipid-efflux programs to the membrane, linking matrix engagement and cholesterol handling to signaling tone. [INFERENCE]

#### Key Insights

- Acid–base transport via SLC4A4 at the cell surface adjusts pH-dependent signaling and excitability. [DATA] [PMID:29500354](https://pubmed.ncbi.nlm.nih.gov/29500354/) ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- Adhesive receptor–phosphatase PTPRT coordinates recognition and signaling at the membrane interface. [EXTERNAL] [PMID:18644975](https://pubmed.ncbi.nlm.nih.gov/18644975/) ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Key Genes

- **SLC4A4**: [EXTERNAL] SLC4A4 (NBCe1) mediates Na+-coupled bicarbonate transport at the plasma membrane to regulate intracellular pH ([PMID:29500354](https://pubmed.ncbi.nlm.nih.gov/29500354/)). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **PTPRT**: [EXTERNAL] PTPRT localizes to the cell surface where it couples adhesive recognition with phosphatase control of downstream signaling ([PMID:18644975](https://pubmed.ncbi.nlm.nih.gov/18644975/)). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **ABCA1**: [INFERENCE] ABCA1 resides at the cell surface to export cholesterol/phospholipids to ApoA-I, maintaining membrane lipid balance. ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **ANOS1**: [INFERENCE] ANOS1 facilitates surface-mediated adhesion and guidance cues that support developmental cell migration and neurite extension. ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Statistical Context

Cell surface proteins are enriched 2.8-fold at FDR 2.70e-02 across 16 genes, consistent with remodeling of interface receptors and transporters. [DATA] [GO:0009986](http://purl.obolibrary.org/obo/GO_0009986) aggregates adhesion receptors and solute carriers matching observed annotations. [GO-HIERARCHY]

---

### Theme 9: cell-substrate junction

**Summary:** cell-substrate junction ([GO:0030055](http://purl.obolibrary.org/obo/GO_0030055))  · Anchor confidence: **FDR<0.05**

Integrin-based adhesions and associated scaffolds couple actomyosin forces to the extracellular matrix, converting mechanical inputs into signaling outputs at cell–substrate junctions. [INFERENCE] Proteomic mapping shows TLN2, TNC, CD99, and DOCK7 populate focal adhesions and undergo myosin II–dependent maturation, placing these factors at the mechanotransduction nexus [PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/). [DATA] Talin–integrin coupling recruits actin linkers and Rho GTPase regulators to stabilize traction and direct migration, while ECM modulators such as tenascin-C tune adhesion lifetime and composition. [INFERENCE]

#### Key Insights

- Focal adhesion maturation requires myosin II–responsive assembly of talin-linked scaffolds and Rho GTPase regulators. [DATA] [PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/) ([GO:0030055](http://purl.obolibrary.org/obo/GO_0030055))
- ECM remodeling by tenascin-C adjusts adhesion composition to balance traction with turnover. [INFERENCE] ([GO:0030055](http://purl.obolibrary.org/obo/GO_0030055))

#### Key Genes

- **TNC**: [INFERENCE] Tenascin-C modulates integrin signaling and focal adhesion composition to regulate traction and migration. ([GO:0030055](http://purl.obolibrary.org/obo/GO_0030055))
- **CD99**: [EXTERNAL] CD99 is recovered in focal adhesion proteomes responsive to myosin II, implicating it in adhesion maturation ([PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/)). ([GO:0030055](http://purl.obolibrary.org/obo/GO_0030055))
- **DOCK7**: [EXTERNAL] DOCK7 localizes to focal adhesions within the myosin II–responsive adhesome, linking Rac signaling to adhesion dynamics ([PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/)). ([GO:0030055](http://purl.obolibrary.org/obo/GO_0030055))
- **TLN2**: [EXTERNAL] Talin-2 couples integrins to actin, nucleating focal adhesion assembly and force transmission ([PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/)). ([GO:0030055](http://purl.obolibrary.org/obo/GO_0030055))

#### Statistical Context

Cell–substrate junctions show 3.5-fold enrichment at FDR 2.70e-02 across 12 genes, consistent with a reinforced adhesome. [DATA] [GO:0030055](http://purl.obolibrary.org/obo/GO_0030055) centers on focal adhesions captured by the proteomic evidence cited. [GO-HIERARCHY]

---

### Theme 10: adherens junction

**Summary:** adherens junction ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))  · Anchor confidence: **FDR<0.05**

Adherens junctions mechanically integrate cells via cadherin–catenin complexes while recruiting polarity and mechanotransduction scaffolds that tune tissue barrier properties. [INFERENCE] FRMD5 binds p120-catenin at adherens junctions to stabilize E-cadherin, aligning cytoskeletal control with junctional retention and suppressing invasive behavior [PMID:22846708](https://pubmed.ncbi.nlm.nih.gov/22846708/). [DATA] SORBS1 (ponsin) localizes to zonula adherens and cell–matrix junctions, connecting afadin and vinculin to transmit tension across actin–cadherin linkages [PMID:10085297](https://pubmed.ncbi.nlm.nih.gov/10085297/). [DATA] Vinculin engagement at adherens junctions reinforces barrier function by coupling actomyosin to cadherins, providing mechanical resilience under stress [PMID:20086044](https://pubmed.ncbi.nlm.nih.gov/20086044/), [PMID:26923917](https://pubmed.ncbi.nlm.nih.gov/26923917/). [EXTERNAL]

#### Key Insights

- p120-catenin–linked FRMD5 stabilizes E-cadherin to maintain adherens junction integrity. [DATA] [PMID:22846708](https://pubmed.ncbi.nlm.nih.gov/22846708/) ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))
- Ponsin/SORBS1 bridges afadin and vinculin at the zonula adherens to transmit force across actin–cadherin assemblies. [DATA] [PMID:10085297](https://pubmed.ncbi.nlm.nih.gov/10085297/) ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))

#### Key Genes

- **PARD3**: [INFERENCE] PARD3 scaffolds polarity complexes at adherens junctions to coordinate actin organization and apicobasal identity. ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))
- **PARD3B**: [INFERENCE] PARD3B contributes to polarity-coupled adherens junction assembly and maintenance through cytoskeletal coordination. ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))
- **FRMD5**: [EXTERNAL] FRMD5 interacts with p120-catenin to stabilize cadherin-based adhesion at adherens junctions ([PMID:22846708](https://pubmed.ncbi.nlm.nih.gov/22846708/)). ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))
- **SORBS1**: [EXTERNAL] SORBS1 (ponsin) localizes to zonula adherens and links afadin/vinculin to actin at cell–cell junctions ([PMID:10085297](https://pubmed.ncbi.nlm.nih.gov/10085297/)). ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))

#### Statistical Context

Adherens junction is enriched 5.0-fold at FDR 2.91e-02 across 8 genes, indicating consolidation of cadherin–catenin–actin connections. [DATA] [GO:0005912](http://purl.obolibrary.org/obo/GO_0005912) captures polarity and mechanotransduction scaffolds observed in the gene set. [GO-HIERARCHY]

---

### Theme 11: negative regulation of cell motility

**Summary:** negative regulation of cell motility ([GO:2000146](http://purl.obolibrary.org/obo/GO_2000146))  · Anchor confidence: **FDR<0.05**

Cell motility is restrained by phosphatases and actin–myosin regulators that dampen protrusion dynamics, focal adhesion turnover, and traction force. [INFERENCE] LIMCH1 suppresses migration by modulating nonmuscle myosin II activity, reducing actomyosin-driven retrograde flow and focal adhesion assembly [PMID:28228547](https://pubmed.ncbi.nlm.nih.gov/28228547/). [DATA] PTPRT dephosphorylates pro-motility substrates and attenuates STAT3-driven programs to curb migration, aligning phosphotyrosine signaling with adhesion stabilization [PMID:24846175](https://pubmed.ncbi.nlm.nih.gov/24846175/). [DATA] FRMD5 binds integrin β5 and ROCK1 to promote adhesion and spreading on vitronectin, thereby antagonizing motile phenotypes [PMID:25448675](https://pubmed.ncbi.nlm.nih.gov/25448675/). [EXTERNAL] Gap junction and cadherin components such as GJA1 and CDH11 enforce contact inhibition and developmental brakes on cell movement in lineage-specific contexts [PMID:30599359](https://pubmed.ncbi.nlm.nih.gov/30599359/), [PMID:33811546](https://pubmed.ncbi.nlm.nih.gov/33811546/). [EXTERNAL]

#### Key Insights

- Actomyosin restraint via LIMCH1 reduces traction forces and limits adhesion turnover to suppress migration. [DATA] [PMID:28228547](https://pubmed.ncbi.nlm.nih.gov/28228547/) ([GO:2000146](http://purl.obolibrary.org/obo/GO_2000146))
- Tyrosine dephosphorylation by PTPRT aligns signaling with adhesion to inhibit cell motility programs. [DATA] [PMID:24846175](https://pubmed.ncbi.nlm.nih.gov/24846175/) ([GO:2000146](http://purl.obolibrary.org/obo/GO_2000146))

#### Key Genes

- **IL33**: [INFERENCE] IL33 modulates leukocyte chemotaxis and inflammatory motility programs via ST2 signaling that can indirectly restrain parenchymal cell migration. ([GO:2000146](http://purl.obolibrary.org/obo/GO_2000146))
- **PTPRT**: [EXTERNAL] PTPRT dephosphorylates pro-migratory substrates and reduces STAT3 activity to inhibit migration ([PMID:24846175](https://pubmed.ncbi.nlm.nih.gov/24846175/)). ([GO:2000146](http://purl.obolibrary.org/obo/GO_2000146))
- **LIMCH1**: [EXTERNAL] LIMCH1 suppresses cell migration by limiting NM-II incorporation into stress fibers and curtailing traction forces ([PMID:28228547](https://pubmed.ncbi.nlm.nih.gov/28228547/)). ([GO:2000146](http://purl.obolibrary.org/obo/GO_2000146))
- **FRMD5**: [EXTERNAL] FRMD5 engages integrin β5 and ROCK1 to promote adhesion and spreading, thereby antagonizing motility ([PMID:25448675](https://pubmed.ncbi.nlm.nih.gov/25448675/)). ([GO:2000146](http://purl.obolibrary.org/obo/GO_2000146))

#### Statistical Context

Negative regulation of cell motility is enriched 4.6-fold at FDR 3.32e-02 across 11 genes, indicating a concerted anti-migratory program. [DATA] [GO:2000146](http://purl.obolibrary.org/obo/GO_2000146) encompasses phosphatases and cytoskeletal brakes reflected by the selected genes. [GO-HIERARCHY]

---

### Theme 12: actin cytoskeleton

**Summary:** actin cytoskeleton ([GO:0015629](http://purl.obolibrary.org/obo/GO_0015629))  · Anchor confidence: **FDR<0.05**

Actin nucleators, crosslinkers, and myosin modulators shape filament architecture to transmit force and signal at the cell cortex. [INFERENCE] DAPK1 and FMN2 respectively tune myosin light-chain phosphorylation and actin nucleation, coupling kinase signaling to filament assembly and apoptotic remodeling [PMID:10629061](https://pubmed.ncbi.nlm.nih.gov/10629061/), [PMID:20082305](https://pubmed.ncbi.nlm.nih.gov/20082305/). [DATA] IQGAP2 scaffolds Rho GTPases with F-actin to integrate small-GTPase cycling with filament stabilization and turnover [PMID:8756646](https://pubmed.ncbi.nlm.nih.gov/8756646/). [DATA] ABLIM1 crosslinks actin bundles to maintain cortical rigidity and coordinate adhesion-dependent signaling, reinforcing load-bearing networks [PMID:9245787](https://pubmed.ncbi.nlm.nih.gov/9245787/), [PMID:10320934](https://pubmed.ncbi.nlm.nih.gov/10320934/). [EXTERNAL]

#### Key Insights

- Kinase-driven tuning of myosin activity and formin-mediated nucleation cooperatively shape actin network architecture. [DATA] [PMID:10629061](https://pubmed.ncbi.nlm.nih.gov/10629061/), [PMID:20082305](https://pubmed.ncbi.nlm.nih.gov/20082305/) ([GO:0015629](http://purl.obolibrary.org/obo/GO_0015629))
- Scaffold-mediated coupling of Rho GTPases to F-actin stabilizes and positions cortical networks for signaling. [DATA] [PMID:8756646](https://pubmed.ncbi.nlm.nih.gov/8756646/) ([GO:0015629](http://purl.obolibrary.org/obo/GO_0015629))

#### Key Genes

- **DAPK1**: [EXTERNAL] DAPK1 regulates actin organization via myosin light chain phosphorylation during stress and apoptotic remodeling ([PMID:10629061](https://pubmed.ncbi.nlm.nih.gov/10629061/)). ([GO:0015629](http://purl.obolibrary.org/obo/GO_0015629))
- **FMN2**: [EXTERNAL] FMN2 nucleates and stabilizes actin filaments to support protrusive structures and adhesion ([PMID:20082305](https://pubmed.ncbi.nlm.nih.gov/20082305/)). ([GO:0015629](http://purl.obolibrary.org/obo/GO_0015629))
- **IQGAP2**: [EXTERNAL] IQGAP2 scaffolds Rho GTPases and binds F-actin to coordinate filament assembly with signaling ([PMID:8756646](https://pubmed.ncbi.nlm.nih.gov/8756646/)). ([GO:0015629](http://purl.obolibrary.org/obo/GO_0015629))
- **ABLIM1**: [EXTERNAL] ABLIM1 crosslinks actin bundles and links them to signaling hubs to maintain cortical mechanics ([PMID:9245787](https://pubmed.ncbi.nlm.nih.gov/9245787/)). ([GO:0015629](http://purl.obolibrary.org/obo/GO_0015629))

#### Statistical Context

Actin cytoskeleton components are enriched 4.2-fold at FDR 3.68e-02 across 9 genes, indicating focal reconfiguration of cortical actin systems. [DATA] [GO:0015629](http://purl.obolibrary.org/obo/GO_0015629) represents the structural network receiving inputs from kinases and small GTPases observed here. [GO-HIERARCHY]

---

### Theme 13: neuron projection

**Summary:** neuron projection ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))  · Anchor confidence: **FDR<0.05**

Neuronal projection morphogenesis integrates ion channel excitability, guidance receptor signaling, and microtubule–actin remodeling to establish polarity and extend axons and dendrites. [INFERENCE] DOCK7-driven Rac signaling locally phosphorylates stathmin to stabilize microtubules in a single neurite, specifying the future axon and initiating polarized growth [PMID:16982419](https://pubmed.ncbi.nlm.nih.gov/16982419/). [DATA] SEMA6A engages Ena/VASP-like effectors to couple guidance cues to actin dynamics, steering axon extension and orientation [PMID:10993894](https://pubmed.ncbi.nlm.nih.gov/10993894/). [EXTERNAL] Calcium-activated K+ conductance via KCNN3 sculpts excitability and Ca2+ dynamics that feedback on cytoskeletal remodeling to support projection stability and growth. [INFERENCE]

#### Key Insights

- Localized Rac signaling and stathmin control downstream of DOCK7 stabilizes microtubules to specify axon identity. [DATA] [PMID:16982419](https://pubmed.ncbi.nlm.nih.gov/16982419/) ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- Semaphorin–Ena/VASP coupling translates external guidance into actin-driven projection steering. [EXTERNAL] [PMID:10993894](https://pubmed.ncbi.nlm.nih.gov/10993894/) ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))

#### Key Genes

- **BMPR1B**: [INFERENCE] BMPR1B signaling influences microtubule organization and axon/dendrite differentiation to promote neuronal polarity. ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- **KCNN3**: [INFERENCE] KCNN3-mediated K+ efflux adjusts membrane excitability and Ca2+ signals that feed back to cytoskeletal remodeling during neurite growth. ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- **STON2**: [INFERENCE] STON2 participates in polarity pathways that regulate microtubule stability and neurite fate specification. ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- **SEMA6A**: [EXTERNAL] SEMA6A links extracellular guidance to Ena/VASP-like effectors to direct axon trajectory ([PMID:10993894](https://pubmed.ncbi.nlm.nih.gov/10993894/)). ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))

#### Statistical Context

Neuron projection is enriched 2.4-fold at FDR 3.68e-02 across 21 genes, indicating coordinated polarization and outgrowth programs. [DATA] [GO:0043005](http://purl.obolibrary.org/obo/GO_0043005) captures axon and dendrite elements aligned with the observed signaling and cytoskeletal factors. [GO-HIERARCHY]

---

## Hub Genes

- **ADCY8**: [INFERENCE] ADCY8 synthesizes cAMP in response to Ca2+/calmodulin and GPCR signals, driving PKA/Epac activation that modulates synaptic plasticity and receptor trafficking at glutamatergic synapses. [INFERENCE] Its localization to plasma membrane regions and rafts positions cAMP microdomains to influence actin-linked adhesion complexes and motility brakes. [INFERENCE]
- **APOE**: [EXTERNAL] APOE binds Aβ and promotes receptor-mediated uptake, reducing intraneuronal Aβ1-42 accumulation and limiting synaptotoxicity. [EXTERNAL] [PMID:24154541](https://pubmed.ncbi.nlm.nih.gov/24154541/). APOE impacts glutamatergic synapse integrity in Alzheimer’s tissue, linking lipid transport to synaptic vulnerability. [EXTERNAL] [PMID:22637583](https://pubmed.ncbi.nlm.nih.gov/22637583/).
- **DMD**: [INFERENCE] Dystrophin bridges the cortical actin cytoskeleton to the extracellular matrix via the dystrophin–glycoprotein complex, stabilizing the plasma membrane during mechanical stress. [INFERENCE] Its presence in rafts and at the cell surface supports adhesion and signaling platforms that affect motility and junctional integrity. [INFERENCE]
- **CNN3**: [EXTERNAL] CNN3 regulates actin filament dynamics at focal adhesions and adherens junctions, reinforcing junctional stability and tuning traction forces. [EXTERNAL] [PMID:25468996](https://pubmed.ncbi.nlm.nih.gov/25468996/). Through actin remodeling it supports cell–cell adhesion and suppresses aberrant motility programs. [EXTERNAL] [PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/).
- **GJA1**: [EXTERNAL] Connexin 43 forms gap junctions that coordinate intercellular signaling and regulate focal adhesion composition, thereby restraining motility. [EXTERNAL] [PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/). GJA1 limits trophoblast migration during early differentiation, linking junctional communication to developmental control of movement. [EXTERNAL] [PMID:30599359](https://pubmed.ncbi.nlm.nih.gov/30599359/).
- **CD44**: [EXTERNAL] CD44 engages hyaluronan to couple extracellular matrix binding with Rho-family signaling from membrane rafts, promoting directional migration and adhesion-site turnover. [EXTERNAL] [PMID:15100360](https://pubmed.ncbi.nlm.nih.gov/15100360/), [PMID:16945930](https://pubmed.ncbi.nlm.nih.gov/16945930/). Its enrichment at apical and lamellipodial membranes integrates surface topology with cytoskeletal remodeling. [EXTERNAL] [PMID:20962267](https://pubmed.ncbi.nlm.nih.gov/20962267/).
- **VCL**: [EXTERNAL] Vinculin links cadherin–catenin and integrin–talin complexes to F-actin, stabilizing adherens and focal adhesions while transmitting force. [EXTERNAL] [PMID:20086044](https://pubmed.ncbi.nlm.nih.gov/20086044/), [PMID:15070891](https://pubmed.ncbi.nlm.nih.gov/15070891/). Its context-dependent tuning of endothelial barrier reflects dual roles in strengthening or releasing junctions under distinct cues. [EXTERNAL] [PMID:26923917](https://pubmed.ncbi.nlm.nih.gov/26923917/).
- **SORBS1**: [EXTERNAL] SORBS1 (ponsin) localizes to the zonula adherens and cell–matrix adhesions where it binds afadin and vinculin to bridge actin to junctional complexes. [EXTERNAL] [PMID:10085297](https://pubmed.ncbi.nlm.nih.gov/10085297/). This scaffolding role supports raft-linked signaling and adhesion mechanics. [INFERENCE]
- **TLN2**: [EXTERNAL] Talin-2 activates integrins and couples them to actin, nucleating and reinforcing focal adhesions that coordinate force transmission and migration. [EXTERNAL] [PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/), [PMID:10320934](https://pubmed.ncbi.nlm.nih.gov/10320934/). Its actin linkage stabilizes adhesion–cytoskeleton crosstalk across multiple themes. [INFERENCE]
- **NOS1AP**: [EXTERNAL] NOS1AP orchestrates postsynaptic actin organization to regulate spine maturation and receptor content at glutamatergic synapses. [EXTERNAL] [PMID:26869880](https://pubmed.ncbi.nlm.nih.gov/26869880/). Its caveolar association situates NO signaling within raft microdomains at the plasma membrane. [EXTERNAL] [PMID:19800018](https://pubmed.ncbi.nlm.nih.gov/19800018/).
- **ADCYAP1R1**: [INFERENCE] PACAP receptor activation recruits adenylyl cyclase to elevate cAMP, modulating raft-localized signaling and surface receptor dynamics. [INFERENCE] This positions neuropeptide cues to influence adhesion and synaptic modules via cAMP effectors. [INFERENCE]
- **ADGRV1**: [INFERENCE] ADGRV1 provides protocadherin-like adhesion at the plasma membrane, stabilizing neuron–neuron contacts and projection architecture. [INFERENCE] Its cell-surface signaling reinforces junctional organization across adhesive themes. [INFERENCE]
- **ITGB4**: [EXTERNAL] Integrin β4 forms high-affinity laminin receptors that sustain cell–matrix adhesion and survival signaling at the surface. [EXTERNAL] [PMID:21310825](https://pubmed.ncbi.nlm.nih.gov/21310825/), [PMID:19933311](https://pubmed.ncbi.nlm.nih.gov/19933311/). Its junctional roles connect plasma membrane architecture to motility restraint. [INFERENCE]
- **CDH11**: [EXTERNAL] Cadherin-11 stabilizes adherens junctions and suppresses migration by reinforcing cadherin–catenin–actin linkages. [EXTERNAL] [PMID:33811546](https://pubmed.ncbi.nlm.nih.gov/33811546/). Its presence at synaptic and adhesive interfaces coordinates structural integrity across tissues. [INFERENCE]
- **CLU**: [EXTERNAL] Clusterin acts as an extracellular chaperone that limits Aβ aggregation and supports neurite integrity at the cell surface and dendrites. [EXTERNAL] [PMID:17567961](https://pubmed.ncbi.nlm.nih.gov/17567961/), [PMID:9560017](https://pubmed.ncbi.nlm.nih.gov/9560017/). These functions connect proteostasis to projection maintenance. [INFERENCE]
- **PARD3B**: [INFERENCE] PARD3B scaffolds polarity complexes at junctions to coordinate cytoskeletal positioning with membrane domain identity. [INFERENCE] This polarity control supports adherens organization and motility restraint. [INFERENCE]
- **KANK1**: [EXTERNAL] KANK1 captures and stabilizes cortical microtubules at focal adhesions through talin interaction, aligning adhesion turnover with microtubule dynamics to suppress aberrant migration. [EXTERNAL] [PMID:27410476](https://pubmed.ncbi.nlm.nih.gov/27410476/), [PMID:19559006](https://pubmed.ncbi.nlm.nih.gov/19559006/). Its membrane recruitment integrates cytoskeletal polarity with surface signaling. [EXTERNAL] [PMID:19559006](https://pubmed.ncbi.nlm.nih.gov/19559006/).
- **DOCK7**: [EXTERNAL] DOCK7 activates Rac1 to organize septin rings and to establish neuronal polarity via localized stathmin phosphorylation that specifies axon identity. [EXTERNAL] [PMID:29467281](https://pubmed.ncbi.nlm.nih.gov/29467281/), [PMID:16982419](https://pubmed.ncbi.nlm.nih.gov/16982419/). Its linkage to focal adhesions connects Rho GTPase signaling to adhesion mechanics. [EXTERNAL] [PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/).
- **TNIK**: [EXTERNAL] TNIK coordinates apical membrane assembly and receptor localization, coupling polarity cues to glutamatergic signaling and cytoskeletal organization. [EXTERNAL] [PMID:22797597](https://pubmed.ncbi.nlm.nih.gov/22797597/). Its placement at membrane domains supports cross-talk between adhesion and synaptic pathways. [INFERENCE]
- **PARD3**: [INFERENCE] PARD3 scaffolds polarity networks at adherens junctions to direct cytoskeletal alignment with apical–basal domains. [INFERENCE] This coordination integrates plasma membrane regionalization with adhesion strength and motility control. [INFERENCE]

## Overall Summary

The enrichment landscape highlights a membrane-centric program where adhesion complexes, lipid rafts, and plasma membrane subregions coordinate cytoskeletal mechanics and second-messenger signaling. [INFERENCE]

Tight cAMP control by adenylyl cyclases and PDE8 isoforms intersects with raft-localized scaffolds to sculpt microdomains that regulate synaptic and motility outputs. [INFERENCE]

Excitatory synapse remodeling is supported by kainate receptor composition and NOS1AP-driven actin changes, aligning with enriched glutamatergic synapse and actin cytoskeleton terms. [DATA] [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/), [PMID:26869880](https://pubmed.ncbi.nlm.nih.gov/26869880/)

Anti-amyloid mechanisms converge on APP sorting and γ-secretase modulation via SORL1, NTRK2, and RTN1, with ApoE-mediated clearance reducing effective Aβ formation. [DATA] [PMID:24523320](https://pubmed.ncbi.nlm.nih.gov/24523320/), [PMID:22621900](https://pubmed.ncbi.nlm.nih.gov/22621900/), [PMID:26094765](https://pubmed.ncbi.nlm.nih.gov/26094765/), [PMID:24154541](https://pubmed.ncbi.nlm.nih.gov/24154541/)

Across themes, hub genes such as VCL, GJA1, CD44, and TLN2 anchor cross-talk between adhesion, cytoskeletal organization, and signaling to collectively restrain aberrant migration while preserving polarized architecture. [INFERENCE]

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

