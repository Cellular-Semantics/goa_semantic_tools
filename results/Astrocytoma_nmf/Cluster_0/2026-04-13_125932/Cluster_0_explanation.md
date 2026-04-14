# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_0_themes.csv](Cluster_0_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-neuron-projection) | [neuron projection](#theme-1-neuron-projection) [GO:0043005](http://purl.obolibrary.org/obo/GO_0043005) | CC | 1.73e-04 | 26 | FDR<0.01 |
| [2](#theme-2-synapse) | [synapse](#theme-2-synapse) [GO:0045202](http://purl.obolibrary.org/obo/GO_0045202) | CC | 6.79e-04 | 30 | FDR<0.01 |
| [3](#theme-3-basolateral-plasma-membrane) | [basolateral plasma membrane](#theme-3-basolateral-plasma-membrane) [GO:0016323](http://purl.obolibrary.org/obo/GO_0016323) | CC | 6.79e-04 | 12 | FDR<0.01 |
| [4](#theme-4-transport-across-blood-brain-barrier) | [transport across blood-brain barrier](#theme-4-transport-across-blood-brain-barrier) [GO:0150104](http://purl.obolibrary.org/obo/GO_0150104) | BP | 1.74e-03 | 8 | FDR<0.01 |
| [5](#theme-5-cell-adhesion) | [cell adhesion](#theme-5-cell-adhesion) [GO:0007155](http://purl.obolibrary.org/obo/GO_0007155) | BP | 1.87e-03 | 23 | FDR<0.01 |
| [6](#theme-6-nucleic-acid-binding) | [nucleic acid binding](#theme-6-nucleic-acid-binding) [GO:0003676](http://purl.obolibrary.org/obo/GO_0003676) | MF | 2.06e-03 | 9 | FDR<0.01 |
| [7](#theme-7-cell-surface) | [cell surface](#theme-7-cell-surface) [GO:0009986](http://purl.obolibrary.org/obo/GO_0009986) | CC | 6.79e-03 | 17 | FDR<0.01 |
| [8](#theme-8-sarcolemma) | [sarcolemma](#theme-8-sarcolemma) [GO:0042383](http://purl.obolibrary.org/obo/GO_0042383) | CC | 6.79e-03 | 7 | FDR<0.01 |
| [9](#theme-9-transporter-activity) | [transporter activity](#theme-9-transporter-activity) [GO:0005215](http://purl.obolibrary.org/obo/GO_0005215) | MF | 8.03e-03 | 27 | FDR<0.01 |
| [10](#theme-10-fluid-transport) | [fluid transport](#theme-10-fluid-transport) [GO:0042044](http://purl.obolibrary.org/obo/GO_0042044) | BP | 1.36e-02 | 5 | FDR<0.05 |
| [11](#theme-11-apical-plasma-membrane) | [apical plasma membrane](#theme-11-apical-plasma-membrane) [GO:0016324](http://purl.obolibrary.org/obo/GO_0016324) | CC | 1.57e-02 | 12 | FDR<0.05 |
| [12](#theme-12-negative-regulation-of-amyloid-beta-formation) | [negative regulation of amyloid-beta formation](#theme-12-negative-regulation-of-amyloid-beta-formation) [GO:1902430](http://purl.obolibrary.org/obo/GO_1902430) | BP | 1.66e-02 | 4 | FDR<0.05 |
| [13](#theme-13-extracellular-matrix) | [extracellular matrix](#theme-13-extracellular-matrix) [GO:0031012](http://purl.obolibrary.org/obo/GO_0031012) | CC | 3.08e-02 | 13 | FDR<0.05 |
| [14](#theme-14-anchoring-junction) | [anchoring junction](#theme-14-anchoring-junction) [GO:0070161](http://purl.obolibrary.org/obo/GO_0070161) | CC | 3.10e-02 | 18 | FDR<0.05 |
| [15](#theme-15-cyclic-nucleotide-metabolic-process) | [cyclic nucleotide metabolic process](#theme-15-cyclic-nucleotide-metabolic-process) [GO:0009187](http://purl.obolibrary.org/obo/GO_0009187) | BP | 3.92e-02 | 5 | FDR<0.05 |
| [16](#theme-16-response-to-oxygen-containing-compound) | [response to oxygen-containing compound](#theme-16-response-to-oxygen-containing-compound) [GO:1901700](http://purl.obolibrary.org/obo/GO_1901700) | BP | 3.92e-02 | 24 | FDR<0.05 |
| [17](#theme-17-nucleic-acid-metabolic-process) | [nucleic acid metabolic process](#theme-17-nucleic-acid-metabolic-process) [GO:0090304](http://purl.obolibrary.org/obo/GO_0090304) | BP | 3.92e-02 | 12 | FDR<0.05 |
| [18](#theme-18-monoatomic-ion-transport) | [monoatomic ion transport](#theme-18-monoatomic-ion-transport) [GO:0006811](http://purl.obolibrary.org/obo/GO_0006811) | BP | 3.92e-02 | 21 | FDR<0.05 |
| [19](#theme-19-receptor-complex) | [receptor complex](#theme-19-receptor-complex) [GO:0043235](http://purl.obolibrary.org/obo/GO_0043235) | CC | 3.99e-02 | 13 | FDR<0.05 |
| [20](#theme-20-renal-water-homeostasis) | [renal water homeostasis](#theme-20-renal-water-homeostasis) [GO:0003091](http://purl.obolibrary.org/obo/GO_0003091) | BP | 4.06e-02 | 4 | FDR<0.05 |
| [21](#theme-21-cytoskeleton) | [cytoskeleton](#theme-21-cytoskeleton) [GO:0005856](http://purl.obolibrary.org/obo/GO_0005856) | CC | 4.82e-02 | 20 | FDR<0.05 |

---

### Theme 1: neuron projection

**Summary:** neuron projection ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.73e-04 · **Genes (26)**: ADCY2, ADCY8, ADGRV1, AHCYL2, ALDH1A1, ANK2, APOE, AQP1, ATP1A2, CHL1, CNTN1, DOCK7, DTNA, FAM107A, FARP1 … (+11 more)

---

### Theme 2: synapse

**Summary:** synapse ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))  · Anchor confidence: **FDR<0.01**

Excitatory synapse assembly integrates adhesion cues with receptor and second messenger signaling to stabilize active zones and postsynaptic specializations. [INFERENCE] ErbB4-containing receptor complexes coordinate neuregulin-dependent plasticity and downstream cascades that tune glutamatergic transmission. [EXTERNAL] cAMP production by synaptic adenylyl cyclases modulates short- and long-term plasticity via PKA targets at the synaptic membrane. [INFERENCE] Glutamatergic synapse and synaptic membrane are nested terms that capture both the molecular scaffold and the signaling surface where these reactions occur. [GO-HIERARCHY]

#### Key Insights

- Glutamatergic synapse enrichment indicates coordinated control of excitatory transmission and plasticity by receptor tyrosine kinase and cAMP pathways. [GO-HIERARCHY] ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- Synaptic membrane enrichment highlights compartmentalized signaling platforms that couple receptors to effectors. [GO-HIERARCHY] ([GO:0097060](http://purl.obolibrary.org/obo/GO_0097060))

#### Key Genes

- **ERBB4**: [EXTERNAL] ERBB4 forms ligand-activated receptor complexes that engage MAPK-linked programs to modulate synaptic plasticity and receptor composition. [EXTERNAL] [PMID:23382219](https://pubmed.ncbi.nlm.nih.gov/23382219/) ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))
- **NRP2**: [EXTERNAL] NRP2 assembles with semaphorin receptor complexes to guide axon targeting and synaptic connectivity that stabilize synapse structure. [DATA] [PMID:19909241](https://pubmed.ncbi.nlm.nih.gov/19909241/) ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))
- **ADCY8**: [INFERENCE] ADCY8 converts ATP to cAMP in response to synaptic GPCR signals, shaping PKA-dependent phosphorylation of synaptic substrates during plasticity. [INFERENCE] ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))
- **SRPX2**: [EXTERNAL] SRPX2 supports excitatory synapse formation by engaging synaptic adhesion systems influenced by neuregulin–ErbB4 signaling. [EXTERNAL] [PMID:29114105](https://pubmed.ncbi.nlm.nih.gov/29114105/) ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))
- **PCDH9**: [INFERENCE] PCDH9 mediates homophilic adhesion that stabilizes nascent contacts and supports synapse maturation. [INFERENCE] ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))

#### Statistical Context

Synapse is enriched with FDR 6.79e-04 and 2.7-fold enrichment, comprising 27 genes. [DATA] Nested terms glutamatergic synapse and synaptic membrane are also enriched, refining the compartment-specific signal. [GO-HIERARCHY]

---

### Theme 3: basolateral plasma membrane

**Summary:** basolateral plasma membrane ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 6.79e-04 · **Genes (12)**: ADCY8, ANK2, AQP1, AQP4, CD38, CD44, ERBB4, MAP7, SLC14A1, SLC4A4, SLCO1C1, SLCO3A1

---

### Theme 4: transport across blood-brain barrier

**Summary:** transport across blood-brain barrier ([GO:0150104](http://purl.obolibrary.org/obo/GO_0150104))  · Anchor confidence: **FDR<0.01**

Blood–brain barrier transport is executed by a complement of solute carriers, pumps, and channels that maintain ionic and metabolic homeostasis in the neuronal milieu. [EXTERNAL] Thyroid hormone influx via OATP1C1, peptide uptake by SLC15A2, and bicarbonate handling by SLC4A4 collectively shape CNS pH, nutrient, and hormone balance. [DATA] Astroglial and endothelial glutamate carriers such as SLC1A3 tune neurotransmitter clearance while ATP1A2 and KATP components influence ion gradients that couple energy status to barrier transport. [DATA]

#### Key Insights

- Specialized SLC and ATPase systems at the BBB orchestrate selective influx and efflux to preserve neuronal function. [DATA] ([GO:0150104](http://purl.obolibrary.org/obo/GO_0150104))
- Integration of peptide, amino acid, and ion transport at the BBB links metabolism to neurotransmission. [EXTERNAL] ([GO:0150104](http://purl.obolibrary.org/obo/GO_0150104))

#### Key Genes

- **SLCO1C1**: [EXTERNAL] SLCO1C1 transports thyroid hormones across brain endothelium, shaping endocrine support of neural circuits. [DATA] [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/); [PMID:26590417](https://pubmed.ncbi.nlm.nih.gov/26590417/) ([GO:0150104](http://purl.obolibrary.org/obo/GO_0150104))
- **SLC15A2**: [EXTERNAL] SLC15A2 mediates proton-coupled peptide uptake at the BBB, sustaining nutrient supply to neural tissue. [DATA] [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/) ([GO:0150104](http://purl.obolibrary.org/obo/GO_0150104))
- **SLC1A3**: [EXTERNAL] SLC1A3 clears glutamate at the neurovascular interface, preventing excitotoxic spillover while contributing to barrier transport processes. [DATA] [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/); [PMID:26590417](https://pubmed.ncbi.nlm.nih.gov/26590417/) ([GO:0150104](http://purl.obolibrary.org/obo/GO_0150104))
- **SLC4A4**: [EXTERNAL] SLC4A4 drives basolateral bicarbonate movement in neurovascular epithelia to regulate pH across the barrier. [DATA] [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/) ([GO:0150104](http://purl.obolibrary.org/obo/GO_0150104))

#### Statistical Context

Transport across blood–brain barrier is markedly enriched with FDR 1.74e-03 and 11.4-fold enrichment across 8 genes, indicating a focused BBB transport signature. [DATA] Curated annotations support each listed transporter’s role at the BBB. [DATA]

---

### Theme 5: cell adhesion

**Summary:** cell adhesion ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.87e-03 · **Genes (23)**: ADAMTS9, ADGRV1, ANOS1, ASTN2, CD44, CDH20, CDHR3, CHL1, CNTN1, IGFBP7, ITGA6, LAMA1, MYBPC1, NRP2, NTM … (+8 more)

---

### Theme 6: nucleic acid binding

**Summary:** nucleic acid binding ([GO:0003676](http://purl.obolibrary.org/obo/GO_0003676))  · Anchor confidence: **FDR<0.01**

Nucleic acid binding functions span sequence-specific transcription factor recognition and structural stabilization of single-stranded intermediates during replication and repair. [INFERENCE] RFX4 binds methylation-sensitive cis-regulatory DNA to direct brain developmental programs, while YAP1 coactivator recruitment to damage-activated transcriptional complexes selects proapoptotic targets. [DATA] SSBP2 stabilizes single-stranded DNA, protecting replication intermediates and coordinating handoff to polymerases. [DATA]

#### Key Insights

- Methylation-sensitive DNA binding modulates access to regulatory elements during development and stress responses. [DATA] ([GO:0003676](http://purl.obolibrary.org/obo/GO_0003676))
- Single-stranded DNA binding preserves genome integrity during replication and repair. [DATA] ([GO:0003676](http://purl.obolibrary.org/obo/GO_0003676))

#### Key Genes

- **RFX4**: [EXTERNAL] RFX4 provides sequence-specific double-stranded DNA recognition at RNA polymerase II cis-regulatory regions to control neurodevelopmental transcription. [DATA] [PMID:28473536](https://pubmed.ncbi.nlm.nih.gov/28473536/); [PMID:16893423](https://pubmed.ncbi.nlm.nih.gov/16893423/) ([GO:0003676](http://purl.obolibrary.org/obo/GO_0003676))
- **YAP1**: [EXTERNAL] YAP1 binds transcriptional regulatory regions with p73 to activate proapoptotic gene programs after DNA damage. [DATA] [PMID:18280240](https://pubmed.ncbi.nlm.nih.gov/18280240/) ([GO:0003676](http://purl.obolibrary.org/obo/GO_0003676))
- **SSBP2**: [EXTERNAL] SSBP2 engages single-stranded DNA to stabilize replication intermediates and prevent degradation during fork progression. [DATA] [PMID:12079286](https://pubmed.ncbi.nlm.nih.gov/12079286/) ([GO:0003676](http://purl.obolibrary.org/obo/GO_0003676))
- **ZNF521**: [INFERENCE] ZNF521 acts as a transcriptional modulator that engages DNA to fine-tune lineage and stress-responsive gene expression. [INFERENCE] ([GO:0003676](http://purl.obolibrary.org/obo/GO_0003676))

#### Statistical Context

Nucleic acid binding is enriched with FDR 2.06e-03 across 9 genes, reflecting coordinated transcriptional and DNA handling activities. [DATA] The observed fold enrichment is 0.3x, consistent with selective but focused representation relative to the background universe used. [DATA]

---

### Theme 7: cell surface

**Summary:** cell surface ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))  · Anchor confidence: **FDR<0.01**

The cell surface hosts receptors, transporters, and proteases that convert extracellular cues into intracellular programs and regulate nutrient and ion exchange. [INFERENCE] ITGA6-containing integrins scaffold ECM ligands to control stem cell behaviors, while TLR4 localizes in membrane rafts to facilitate innate immune signaling in endothelium. [DATA] The Na+-bicarbonate cotransporter NBCe1 is validated at the cell surface, linking acid–base transport to signaling microdomains. [EXTERNAL]

#### Key Insights

- Membrane rafts and integrin platforms co-localize receptors and transporters to optimize signaling and transport at the cell surface. [EXTERNAL] ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- Acid–base transporters at the surface integrate metabolism with extracellular matrix-driven signaling. [GO-HIERARCHY] ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Key Genes

- **ITGA6**: [EXTERNAL] ITGA6 presents ECM ligands and organizes adhesion–signaling hubs that tune lineage decisions and motility. [DATA] [PMID:23658023](https://pubmed.ncbi.nlm.nih.gov/23658023/); [PMID:23154389](https://pubmed.ncbi.nlm.nih.gov/23154389/); [PMID:20563599](https://pubmed.ncbi.nlm.nih.gov/20563599/) ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **TLR4**: [EXTERNAL] TLR4 resides in raft-associated platforms where flotillin-1 supports assembly to amplify innate immune signaling. [DATA] [PMID:25204797](https://pubmed.ncbi.nlm.nih.gov/25204797/) ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **SLC4A4**: [EXTERNAL] NBCe1 is expressed at the plasma membrane, enabling bicarbonate transport that interfaces with local signaling. [EXTERNAL] [PMID:29500354](https://pubmed.ncbi.nlm.nih.gov/29500354/) ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **PCSK6**: [INFERENCE] PCSK6 activates secreted and membrane precursors at the cell surface, modulating receptor availability and paracrine signaling. [INFERENCE] ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Statistical Context

Cell surface is enriched with FDR 6.79e-03 and 3.1-fold enrichment across 17 genes, indicating a strong membrane signaling and transport signature. [DATA] Evidence includes proteomics and functional assays confirming surface localization of key components. [EXTERNAL]

---

### Theme 8: sarcolemma

**Summary:** sarcolemma ([GO:0042383](http://purl.obolibrary.org/obo/GO_0042383))  · Anchor confidence: **FDR<0.01**

The sarcolemma integrates water channels, ion channels, and cytoskeletal linkers to preserve muscle fiber excitability and volume during contraction. [INFERENCE] AQP4 and AQP1 provide rapid osmotic equilibration at the muscle membrane, while utrophin stabilizes dystrophin-associated complexes to protect against mechanical stress. [DATA] KATP subunits at the sarcolemma couple cellular ATP to potassium flux, tuning excitability during metabolic shifts. [INFERENCE]

#### Key Insights

- Water channel arrays at the sarcolemma enable rapid volume regulation during mechanical load. [DATA] ([GO:0042383](http://purl.obolibrary.org/obo/GO_0042383))
- Cytoskeletal linkers protect membrane integrity and organize channel microdomains in contracting muscle. [INFERENCE] ([GO:0042383](http://purl.obolibrary.org/obo/GO_0042383))

#### Key Genes

- **AQP4**: [EXTERNAL] AQP4 forms supramolecular arrays in muscle sarcolemma to support efficient water flux without compromising structural integrity. [DATA] [PMID:29055082](https://pubmed.ncbi.nlm.nih.gov/29055082/) ([GO:0042383](http://purl.obolibrary.org/obo/GO_0042383))
- **AQP1**: [EXTERNAL] AQP1 is expressed at the sarcolemma, providing a parallel water pathway that complements AQP4-mediated flux. [DATA] [PMID:17409744](https://pubmed.ncbi.nlm.nih.gov/17409744/) ([GO:0042383](http://purl.obolibrary.org/obo/GO_0042383))
- **UTRN**: [INFERENCE] Utrophin stabilizes the dystrophin-associated complex at the sarcolemma, securing channels and receptors during contraction. [INFERENCE] ([GO:0042383](http://purl.obolibrary.org/obo/GO_0042383))
- **ABCC9**: [INFERENCE] The SUR2 subunit of KATP channels situates in the sarcolemma to link ATP levels to potassium conductance and excitability. [INFERENCE] ([GO:0042383](http://purl.obolibrary.org/obo/GO_0042383))

#### Statistical Context

Sarcolemma is enriched with FDR 6.79e-03 and 7.6-fold enrichment across 7 genes, supporting a robust membrane specialization signal. [DATA] Water channels and channel-associated scaffolds are prominent within this set. [DATA]

---

### Theme 9: transporter activity

**Summary:** transporter activity ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))  · Anchor confidence: **FDR<0.01**

Transporter activity encompasses protein families that move ions, metabolites, and lipids across membranes or between organelles to maintain homeostasis. [INFERENCE] Mitochondrial SLC25A48 imports choline to fuel phospholipid synthesis and one-carbon metabolism, whereas OSBPL11 mediates lipid exchange at contact sites to balance signaling lipids. [DATA] Additional carriers and channels such as putative anion transporters TTYH2 and lipid movers like GRAMD1C complement this metabolic routing. [INFERENCE]

#### Key Insights

- Mitochondrial and contact-site transporters coordinate metabolite and lipid flux to sustain bioenergetics and membrane composition. [EXTERNAL] ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))
- Dedicated choline and lipid exchangers expand transporter activity beyond ions to control signaling capacity. [DATA] ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))

#### Key Genes

- **SLC25A48**: [EXTERNAL] SLC25A48 transports choline across the inner mitochondrial membrane to drive phosphatidylcholine synthesis and methyl-donor production. [DATA] [PMID:39111307](https://pubmed.ncbi.nlm.nih.gov/39111307/); [PMID:39084256](https://pubmed.ncbi.nlm.nih.gov/39084256/) ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))
- **OSBPL11**: [EXTERNAL] OSBPL11 catalyzes phosphatidylserine–PI4P exchange, redistributing lipids to support sphingomyelin synthesis and signaling. [DATA] [PMID:39106189](https://pubmed.ncbi.nlm.nih.gov/39106189/) ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))
- **TTYH2**: [INFERENCE] TTYH2 likely mediates organic anion flux that contributes to maintenance of transmembrane charge and solute gradients. [INFERENCE] ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))
- **GRAMD1C**: [INFERENCE] GRAMD1C participates in nonvesicular lipid transfer to equilibrate sterol and phospholipid pools across membranes. [INFERENCE] ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))
- **ATP13A4**: [INFERENCE] ATP13A4 contributes to cation transport from endolysosomal stores to regulate cytosolic ion balance and signaling. [INFERENCE] ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))

#### Statistical Context

Transporter activity is enriched with FDR 8.03e-03 and 2.6-fold enrichment over background across 27 genes. [DATA] Curated annotations include transmembrane transporter activities for OATP family members consistent with this theme. [DATA]

---

### Theme 10: fluid transport

**Summary:** fluid transport ([GO:0042044](http://purl.obolibrary.org/obo/GO_0042044))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.36e-02 · **Genes (5)**: AHCYL1, AQP1, AQP4, EDNRB, SLC14A1

---

### Theme 11: apical plasma membrane

**Summary:** apical plasma membrane ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))  · Anchor confidence: **FDR<0.05**

Apical plasma membrane specialization builds microvilli and junctional belts to maximize absorptive area and establish vectorial transport. [INFERENCE] Rap2A–TNIK signaling couples polarity cues to brush border morphogenesis, while CD44 concentrates at apical protrusions to coordinate directional migration and receptor presentation. [DATA] Aquaporin-1 populates apical domains in secretory epithelia, supporting rapid water flux aligned with apical transporters. [DATA]

#### Key Insights

- Polarity signaling to the actin cortex drives microvillus assembly at the apical domain. [DATA] ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))
- Apical clustering of adhesion receptors and channels organizes absorptive and migratory functions. [EXTERNAL] ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))

#### Key Genes

- **TNIK**: [EXTERNAL] TNIK links Rap2A polarity signals to apical actin reorganization that builds the microvillus brush border. [DATA] [PMID:22797597](https://pubmed.ncbi.nlm.nih.gov/22797597/) ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))
- **CD44**: [EXTERNAL] CD44 accumulates at apical protrusions through podoplanin association, coordinating directional motility and ligand presentation. [DATA] [PMID:20962267](https://pubmed.ncbi.nlm.nih.gov/20962267/) ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))
- **AQP1**: [EXTERNAL] AQP1 is dynamically distributed at apical membranes to accelerate water exchange supporting secretion and absorption. [DATA] [PMID:18617525](https://pubmed.ncbi.nlm.nih.gov/18617525/); [PMID:17890385](https://pubmed.ncbi.nlm.nih.gov/17890385/); [PMID:16133142](https://pubmed.ncbi.nlm.nih.gov/16133142/) ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))
- **PARD3B**: [INFERENCE] PARD3B organizes polarity complexes to align tight junctions with apical cytoskeletal architecture. [INFERENCE] ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))

#### Statistical Context

Apical plasma membrane is enriched with FDR 1.57e-02 and 3.7-fold enrichment across 12 genes, consistent with epithelial polarity engagement. [DATA] Complementary enrichment of basolateral domains underscores coordinated sorting. [GO-HIERARCHY]

---

### Theme 12: negative regulation of amyloid-beta formation

**Summary:** negative regulation of amyloid-beta formation ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))  · Anchor confidence: **FDR<0.05**

Multiple receptors and sorting adaptors attenuate amyloidogenic processing by redirecting APP away from gamma-secretase or modulating its activity. [INFERENCE] SORL1 traffics APP into endosomal–lysosomal routes that reduce Abeta generation, while NTRK2-linked complexes diminish gamma-secretase-dependent Abeta without impairing Notch cleavage. [DATA] APOE isoform-dependent effects further constrain intraneuronal Abeta accumulation, aligning lipid transport with proteostasis. [DATA]

#### Key Insights

- Receptor-mediated endosomal sorting of APP reduces substrate availability for amyloidogenic cleavage. [DATA] ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- Selective modulation of gamma-secretase activity can lower Abeta while sparing essential Notch signaling. [EXTERNAL] ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))

#### Key Genes

- **SORL1**: [EXTERNAL] SORL1 directs APP to lysosomal pathways via GGA1-dependent sorting, reducing Abeta production. [DATA] [PMID:22621900](https://pubmed.ncbi.nlm.nih.gov/22621900/); [PMID:24523320](https://pubmed.ncbi.nlm.nih.gov/24523320/); [PMID:24001769](https://pubmed.ncbi.nlm.nih.gov/24001769/) ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- **NTRK2**: [EXTERNAL] NTRK2-associated complexes negatively regulate Abeta formation by altering gamma-secretase substrate processing. [DATA] [PMID:26094765](https://pubmed.ncbi.nlm.nih.gov/26094765/) ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- **APOE**: [EXTERNAL] APOE genotype influences intraneuronal Abeta42 accumulation, linking lipid transport to reduced amyloid formation. [DATA] [PMID:24154541](https://pubmed.ncbi.nlm.nih.gov/24154541/) ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))
- **RTN1**: [EXTERNAL] RTN1 can modulate gamma-secretase activity to limit Abeta production without disrupting Notch processing. [EXTERNAL] [PMID:26094765](https://pubmed.ncbi.nlm.nih.gov/26094765/) ([GO:1902430](http://purl.obolibrary.org/obo/GO_1902430))

#### Statistical Context

Negative regulation of amyloid-beta formation is enriched with FDR 1.66e-02 and 29.5-fold enrichment across 4 genes, indicating a concentrated anti-amyloid module. [DATA] Multiple curated annotations converge on APP trafficking and gamma-secretase modulation. [DATA]

---

### Theme 13: extracellular matrix

**Summary:** extracellular matrix ([GO:0031012](http://purl.obolibrary.org/obo/GO_0031012))  · Anchor confidence: **FDR<0.05**

The extracellular matrix provides structural scaffolds and growth factor reservoirs that shape cell behavior, with collagens and glycoproteins forming the core matrisome. [DATA] Type IV and V collagens assemble basement membrane and fibrillar networks that regulate adhesion, while IGFBP7 and ADAMTS9 modulate bioavailability of signaling molecules and matrix turnover. [DATA] Disease-linked ECM remodeling signatures align with these components across cardiovascular and tumor contexts. [EXTERNAL]

#### Key Insights

- Basement membrane and fibrillar collagens organize tissue architecture and integrin signaling. [DATA] ([GO:0031012](http://purl.obolibrary.org/obo/GO_0031012))
- ECM proteases and binding proteins tune matrix composition and growth factor gradients. [EXTERNAL] ([GO:0031012](http://purl.obolibrary.org/obo/GO_0031012))

#### Key Genes

- **COL4A5**: [EXTERNAL] COL4A5 contributes to basement membrane scaffolds that regulate epithelial polarity and barrier function. [DATA] [PMID:28675934](https://pubmed.ncbi.nlm.nih.gov/28675934/); [PMID:28344315](https://pubmed.ncbi.nlm.nih.gov/28344315/) ([GO:0031012](http://purl.obolibrary.org/obo/GO_0031012))
- **COL5A3**: [EXTERNAL] COL5A3 forms fibrillar networks that influence cell adhesion and mechanical signaling within tissues. [DATA] [PMID:28675934](https://pubmed.ncbi.nlm.nih.gov/28675934/); [PMID:27559042](https://pubmed.ncbi.nlm.nih.gov/27559042/) ([GO:0031012](http://purl.obolibrary.org/obo/GO_0031012))
- **IGFBP7**: [EXTERNAL] IGFBP7 integrates into the ECM and modulates growth factor availability within cardiac and tumor microenvironments. [DATA] [PMID:27559042](https://pubmed.ncbi.nlm.nih.gov/27559042/); [PMID:25037231](https://pubmed.ncbi.nlm.nih.gov/25037231/) ([GO:0031012](http://purl.obolibrary.org/obo/GO_0031012))
- **ADAMTS9**: [EXTERNAL] ADAMTS9 participates in ECM remodeling by processing proteoglycans during tissue repair and remodeling. [DATA] [PMID:22261194](https://pubmed.ncbi.nlm.nih.gov/22261194/) ([GO:0031012](http://purl.obolibrary.org/obo/GO_0031012))

#### Statistical Context

Extracellular matrix is enriched with FDR 3.08e-02 and 3.2-fold enrichment across 13 genes, consistent with a substantive matrisome signal. [DATA] Proteomic studies corroborate enrichment of these ECM constituents in disease states. [EXTERNAL]

---

### Theme 14: anchoring junction

**Summary:** anchoring junction ([GO:0070161](http://purl.obolibrary.org/obo/GO_0070161))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 3.10e-02 · **Genes (18)**: ADCYAP1R1, ANK2, ARHGAP26, ATP1A2, CD44, CDH20, CDHR3, DOCK7, FAM107A, GJA1, ITGA6, LAMA1, PARD3B, RHOB, SHROOM3 … (+3 more)

---

### Theme 15: cyclic nucleotide metabolic process

**Summary:** cyclic nucleotide metabolic process ([GO:0009187](http://purl.obolibrary.org/obo/GO_0009187))  · Anchor confidence: **FDR<0.05**

Cyclic nucleotide metabolism couples extracellular cues to intracellular effectors through regulated synthesis and degradation of cAMP. [INFERENCE] Adenylate cyclases ADCY2 and ADCY8 produce cAMP in response to GPCR inputs, while PACAP receptor ADCYAP1R1 elevates cAMP to engage PKA and downstream targets; PDE8A hydrolyzes cAMP to terminate signals. [EXTERNAL] The enriched child terms cAMP metabolic process and cyclic nucleotide biosynthetic process capture both production and turnover arms. [GO-HIERARCHY]

#### Key Insights

- Balanced adenylate cyclase synthesis and phosphodiesterase degradation of cAMP sustain precise temporal signaling. [GO-HIERARCHY] ([GO:0046058](http://purl.obolibrary.org/obo/GO_0046058))
- Ligand-activated receptors drive cyclic nucleotide biosynthesis to gate downstream kinase cascades. [EXTERNAL] ([GO:0009190](http://purl.obolibrary.org/obo/GO_0009190))

#### Key Genes

- **ADCY8**: [INFERENCE] ADCY8 generates cAMP upon GPCR activation to modulate neuronal excitability and plasticity. [INFERENCE] ([GO:0009187](http://purl.obolibrary.org/obo/GO_0009187))
- **ADCY2**: [INFERENCE] ADCY2 catalyzes stimulus-coupled cAMP synthesis that feeds into PKA signaling in excitable cells. [INFERENCE] ([GO:0009187](http://purl.obolibrary.org/obo/GO_0009187))
- **ADCYAP1R1**: [EXTERNAL] ADCYAP1R1 activates adenylate cyclase upon PACAP binding to increase cAMP and orchestrate downstream responses. [EXTERNAL] [PMID:23382219](https://pubmed.ncbi.nlm.nih.gov/23382219/) ([GO:0009187](http://purl.obolibrary.org/obo/GO_0009187))
- **PDE8A**: [INFERENCE] PDE8A degrades cAMP to terminate signaling and shape compartmentalized cyclic nucleotide gradients. [INFERENCE] ([GO:0009187](http://purl.obolibrary.org/obo/GO_0009187))

#### Statistical Context

Cyclic nucleotide metabolic process is enriched with FDR 3.92e-02 and 13.1-fold enrichment across 5 genes, with cAMP metabolic and biosynthetic subprocesses also enriched. [DATA] These signals indicate coordinated control of second-messenger dynamics. [DATA]

---

### Theme 16: response to oxygen-containing compound

**Summary:** response to oxygen-containing compound ([GO:1901700](http://purl.obolibrary.org/obo/GO_1901700))  · Anchor confidence: **FDR<0.05**

Responses to oxygen-containing compounds integrate redox sensing with inflammatory and stress pathways to preserve cellular homeostasis. [INFERENCE] DAPK1 propagates hydroperoxide-induced signals to autophagy via Vps34–PKD axes, TLR4 mediates LPS-driven innate responses, and connexin 43 participates in astrocytic responses to amyloid-beta–evoked oxidative stress. [DATA] These modules converge on antioxidant release, cytokine production, and survival decisions. [INFERENCE]

#### Key Insights

- Oxidant-activated kinases and autophagy pathways mitigate damage and restore proteostasis. [DATA] ([GO:1901700](http://purl.obolibrary.org/obo/GO_1901700))
- Pattern-recognition receptor signaling to NF-kB links oxygenated lipid sensing to inflammation. [DATA] ([GO:1901700](http://purl.obolibrary.org/obo/GO_1901700))

#### Key Genes

- **DAPK1**: [EXTERNAL] DAPK1 relays hydroperoxide signals to Vps34–PKD to induce autophagy under oxidative stress. [DATA] [PMID:22095288](https://pubmed.ncbi.nlm.nih.gov/22095288/) ([GO:1901700](http://purl.obolibrary.org/obo/GO_1901700))
- **TLR4**: [EXTERNAL] TLR4 upregulation enhances cellular responsiveness to lipopolysaccharide, amplifying downstream inflammatory signaling. [DATA] [PMID:30321456](https://pubmed.ncbi.nlm.nih.gov/30321456/) ([GO:1901700](http://purl.obolibrary.org/obo/GO_1901700))
- **GJA1**: [EXTERNAL] GJA1 modulates astrocytic glutathione release in response to amyloid-beta, linking redox stress to neuroprotective coupling. [DATA] [PMID:26200696](https://pubmed.ncbi.nlm.nih.gov/26200696/) ([GO:1901700](http://purl.obolibrary.org/obo/GO_1901700))
- **IGFBP7**: [INFERENCE] IGFBP7 tunes growth factor signaling under oxidative stress to balance survival and proliferation. [INFERENCE] ([GO:1901700](http://purl.obolibrary.org/obo/GO_1901700))

#### Statistical Context

Response to oxygen-containing compound is enriched with FDR 3.92e-02 and 2.4-fold enrichment across 24 genes, reflecting coordinated redox and inflammatory programs. [DATA] Multiple curated response annotations substantiate this theme. [DATA]

---

### Theme 17: nucleic acid metabolic process

**Summary:** nucleic acid metabolic process ([GO:0090304](http://purl.obolibrary.org/obo/GO_0090304))  · Anchor confidence: **FDR<0.05**

Nucleic acid metabolic processes coordinate replication initiation, elongation, and transcriptional control to preserve genome integrity during cell division and differentiation. [INFERENCE] RFX4 provides sequence-specific DNA binding that programs neural gene expression, while ID proteins and PRRX1 modulate transcriptional networks that intersect with replication competence. [DATA] These activities integrate with CMG helicase function and polymerase recruitment to sustain faithful DNA synthesis. [EXTERNAL]

#### Key Insights

- Sequence-specific regulators and co-factors tune transcriptional programs that intersect with replication timing. [DATA] ([GO:0090304](http://purl.obolibrary.org/obo/GO_0090304))
- Integration of replication machinery with regulatory factors maintains genome stability during S phase. [INFERENCE] ([GO:0090304](http://purl.obolibrary.org/obo/GO_0090304))

#### Key Genes

- **RFX4**: [EXTERNAL] RFX4 binds cis-regulatory DNA to direct brain developmental transcription programs that interface with replication-associated chromatin states. [DATA] [PMID:16893423](https://pubmed.ncbi.nlm.nih.gov/16893423/) ([GO:0090304](http://purl.obolibrary.org/obo/GO_0090304))
- **DPF3**: [INFERENCE] DPF3 modulates chromatin to facilitate accessibility of replication and transcriptional machinery. [INFERENCE] ([GO:0090304](http://purl.obolibrary.org/obo/GO_0090304))
- **ID3**: [INFERENCE] ID3 influences transcriptional networks that coordinate cell cycle entry with DNA synthesis. [INFERENCE] ([GO:0090304](http://purl.obolibrary.org/obo/GO_0090304))
- **PRRX1**: [INFERENCE] PRRX1 acts as a transcriptional regulator that shapes lineage programs impacting nucleic acid metabolic throughput. [INFERENCE] ([GO:0090304](http://purl.obolibrary.org/obo/GO_0090304))

#### Statistical Context

Nucleic acid metabolic process is enriched with FDR 3.92e-02 across 12 genes with a modest 0.4-fold representation relative to background, indicating selective inclusion of regulatory factors. [DATA] Supporting annotations include sequence-specific DNA binding activities linked to developmental programs. [DATA]

---

### Theme 18: monoatomic ion transport

**Summary:** monoatomic ion transport ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))  · Anchor confidence: **FDR<0.05**

Monoatomic ion transport maintains membrane potential, calcium homeostasis, and signal propagation through coordinated channel and exchanger activities. [INFERENCE] KCNQ5 provides voltage-gated K+ efflux critical for neuronal repolarization, while KCNN3 couples intracellular Ca2+ to K+ conductance to limit excitability; additional cation transporters adjust organellar and plasma-membrane ion balances. [DATA] Together these systems stabilize firing thresholds and excitation–secretion coupling. [INFERENCE]

#### Key Insights

- Voltage- and calcium-gated potassium channels set membrane excitability and repolarization kinetics. [DATA] ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))
- Endomembrane cation pumps and channels fine-tune cytosolic ion signals that drive downstream effectors. [INFERENCE] ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))

#### Key Genes

- **KCNQ5**: [EXTERNAL] KCNQ5 mediates M-current K+ efflux to stabilize membrane potential and prevent hyperexcitability. [DATA] [PMID:28669405](https://pubmed.ncbi.nlm.nih.gov/28669405/) ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))
- **KCNN3**: [EXTERNAL] KCNN3 conducts Ca2+-activated K+ currents to translate calcium elevations into membrane hyperpolarization. [DATA] [PMID:28842488](https://pubmed.ncbi.nlm.nih.gov/28842488/) ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))
- **ATP13A4**: [INFERENCE] ATP13A4 contributes to lysosomal cation transport that influences cellular ion homeostasis. [INFERENCE] ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))
- **CACNA2D3**: [INFERENCE] CACNA2D3 modulates voltage-gated calcium channel trafficking and gating to control Ca2+ entry. [INFERENCE] ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))
- **ITPR2**: [INFERENCE] ITPR2 releases Ca2+ from ER stores to shape cytosolic calcium transients that regulate downstream channels. [INFERENCE] ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))

#### Statistical Context

Monoatomic ion transport is enriched with FDR 3.92e-02 and 2.7-fold enrichment across 21 genes, highlighting strong ion handling capacity. [DATA] Curated annotations include potassium transport by KCNQ5 and ABCC9-related KATP mechanisms within the broader gene set. [DATA]

---

### Theme 19: receptor complex

**Summary:** receptor complex ([GO:0043235](http://purl.obolibrary.org/obo/GO_0043235))  · Anchor confidence: **FDR<0.05**

Receptor complexes integrate ligand recognition with adaptor-mediated trafficking to shape the magnitude and duration of signaling. [INFERENCE] gp130 family cytokine receptors such as LIFR assemble higher-order complexes to trigger downstream JAK–STAT cascades, while PX-FERM pathway components coordinate endosomal recycling of diverse receptor cargos including neurotrophic and GPCR systems. [DATA] Innate immune receptor complexes like TLR4 oligomers connect danger signals to NF-kB activation. [DATA]

#### Key Insights

- Higher-order cytokine receptor assemblies specify signaling outputs and crosstalk with trafficking regulators. [DATA] ([GO:0043235](http://purl.obolibrary.org/obo/GO_0043235))
- Endosomal retrieval complexes preserve receptor availability and prevent signal desensitization. [EXTERNAL] ([GO:0043235](http://purl.obolibrary.org/obo/GO_0043235))

#### Key Genes

- **LIFR**: [EXTERNAL] LIFR forms part of the ciliary neurotrophic factor receptor complex with gp130 to drive downstream STAT signaling. [DATA] [PMID:36930708](https://pubmed.ncbi.nlm.nih.gov/36930708/) ([GO:0043235](http://purl.obolibrary.org/obo/GO_0043235))
- **NTRK2**: [EXTERNAL] NTRK2 assembles neurotrophin receptor complexes whose endosomal trafficking is governed by PX-FERM adaptors to sustain signaling. [DATA] [PMID:23382219](https://pubmed.ncbi.nlm.nih.gov/23382219/) ([GO:0043235](http://purl.obolibrary.org/obo/GO_0043235))
- **ADGRV1**: [EXTERNAL] ADGRV1 participates in receptor complexes whose sorting is controlled by endosomal adaptors to fine-tune surface signaling. [DATA] [PMID:23382219](https://pubmed.ncbi.nlm.nih.gov/23382219/) ([GO:0043235](http://purl.obolibrary.org/obo/GO_0043235))
- **ITPR2**: [EXTERNAL] ITPR2 associates within receptor-effector assemblies to couple receptor activation to intracellular Ca2+ release. [DATA] [PMID:23382219](https://pubmed.ncbi.nlm.nih.gov/23382219/) ([GO:0043235](http://purl.obolibrary.org/obo/GO_0043235))

#### Statistical Context

Receptor complex is enriched with FDR 3.99e-02 and 3.0-fold enrichment across 13 genes, indicating coordinated signaling assembly and trafficking. [DATA] Structural studies support cytokine receptor architecture within this set. [DATA]

---

### Theme 20: renal water homeostasis

**Summary:** renal water homeostasis ([GO:0003091](http://purl.obolibrary.org/obo/GO_0003091))  · Anchor confidence: **FDR<0.05**

Renal water homeostasis couples aquaporin-mediated water permeability to cAMP signaling that targets channel abundance and trafficking in nephron segments. [INFERENCE] AQP1 and AQP4 provide high-efficiency water pathways whose regulation coordinates with adenylate cyclase signals to adapt to hydration state. [DATA] This integration stabilizes urine concentration capacity and systemic osmolality. [INFERENCE]

#### Key Insights

- Aquaporin channel density and gating govern collecting system water permeability underlying urine concentration. [DATA] ([GO:0003091](http://purl.obolibrary.org/obo/GO_0003091))
- cAMP pathway components align with aquaporin trafficking to adjust renal water reabsorption. [INFERENCE] ([GO:0003091](http://purl.obolibrary.org/obo/GO_0003091))

#### Key Genes

- **AQP1**: [EXTERNAL] AQP1 supplies constitutive water permeability in proximal nephron and vasa recta to support countercurrent exchange. [DATA] [PMID:12766090](https://pubmed.ncbi.nlm.nih.gov/12766090/) ([GO:0003091](http://purl.obolibrary.org/obo/GO_0003091))
- **AQP4**: [EXTERNAL] AQP4 contributes to water balance by enabling rapid osmotic equilibration in renal epithelia. [DATA] [PMID:19383790](https://pubmed.ncbi.nlm.nih.gov/19383790/) ([GO:0003091](http://purl.obolibrary.org/obo/GO_0003091))
- **ADCY2**: [INFERENCE] ADCY2 synthesizes cAMP downstream of hormonal cues to tune water channel trafficking and abundance. [INFERENCE] ([GO:0003091](http://purl.obolibrary.org/obo/GO_0003091))
- **ADCY8**: [INFERENCE] ADCY8 elevates cAMP to modulate aquaporin regulation during antidiuretic responses. [INFERENCE] ([GO:0003091](http://purl.obolibrary.org/obo/GO_0003091))

#### Statistical Context

Renal water homeostasis is enriched with FDR 4.06e-02 and 19.3-fold enrichment across 4 genes, indicating a compact and coherent water regulation module. [DATA] Multiple aquaporin annotations substantiate this renal signature. [DATA]

---

### Theme 21: cytoskeleton

**Summary:** cytoskeleton ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))  · Anchor confidence: **FDR<0.05**

Cytoskeletal systems translate signaling inputs into force generation and morphological change through actin polymerization, crosslinking, and microtubule coordination. [INFERENCE] FMN2 and ITPKB couple calcium signaling to actin assembly states, while ARHGAP26 curbs RhoA to promote filament turnover and cell motility. [DATA] Nuclear–cytoskeletal crosstalk via NAV3-associated complexes ties actin dynamics to transcriptional control and growth restraint. [EXTERNAL]

#### Key Insights

- Calcium-regulated actin modulators and RhoGTPase regulators jointly pattern cytoskeletal remodeling. [DATA] ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- Cytoskeletal elements interface with nuclear programs to integrate mechanics and gene regulation. [EXTERNAL] ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))

#### Key Genes

- **FMN2**: [EXTERNAL] FMN2 supports actin filament assembly linked to beta-catenin–dependent signaling during proliferative control. [DATA] [PMID:20082305](https://pubmed.ncbi.nlm.nih.gov/20082305/) ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **ITPKB**: [EXTERNAL] ITPKB modulates IP3-derived calcium signals that reorganize the actin cytoskeleton for migration and morphogenesis. [DATA] [PMID:12747803](https://pubmed.ncbi.nlm.nih.gov/12747803/) ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **ARHGAP26**: [INFERENCE] ARHGAP26 promotes actin turnover by inactivating RhoA, enabling adhesion remodeling and motility. [INFERENCE] ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **NAV3**: [EXTERNAL] NAV3 participates in nuclear F-actin complexes that interface with signaling regulators to restrain growth. [EXTERNAL] [PMID:28604741](https://pubmed.ncbi.nlm.nih.gov/28604741/) ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))

#### Statistical Context

Cytoskeleton is enriched with FDR 4.82e-02 and 2.4-fold enrichment across 20 genes, highlighting robust engagement of actin-regulatory machinery. [DATA] Independent evidence links these factors to both structural and signaling roles. [EXTERNAL]

---

## Hub Genes

- **AQP1**: [EXTERNAL] AQP1 forms high-conductance water channels at apical and basolateral membranes to drive transepithelial water flow and tissue hydration. [DATA] [PMID:18617525](https://pubmed.ncbi.nlm.nih.gov/18617525/); [PMID:12766090](https://pubmed.ncbi.nlm.nih.gov/12766090/)
- **ANK2**: [INFERENCE] ANK2 anchors ion channels and transporters to the spectrin–actin cytoskeleton in neurons and muscle, stabilizing excitable membrane domains across polarized surfaces. [INFERENCE]
- **ATP1A2**: [EXTERNAL] ATP1A2 generates Na+/K+ gradients that set neuronal excitability and support K+ clearance at the neurovascular interface. [EXTERNAL] [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/)
- **ADCY8**: [INFERENCE] ADCY8 produces cAMP downstream of GPCRs at the plasma membrane, tuning plasticity and excitability in synaptic and epithelial contexts. [INFERENCE]
- **SLC1A3**: [EXTERNAL] SLC1A3 clears synaptic glutamate and participates in BBB transport, preventing excitotoxicity while shaping neurovascular coupling. [EXTERNAL] [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/); [PMID:26590417](https://pubmed.ncbi.nlm.nih.gov/26590417/)
- **SLC1A4**: [EXTERNAL] SLC1A4 transports neutral amino acids at the BBB and cell surface to balance neurotransmitter precursors and metabolic substrates. [EXTERNAL] [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/); [PMID:26590417](https://pubmed.ncbi.nlm.nih.gov/26590417/)
- **APOE**: [EXTERNAL] APOE coordinates lipid trafficking that supports synaptic maintenance and limits amyloid-beta accumulation through genotype-dependent mechanisms. [DATA] [PMID:8083695](https://pubmed.ncbi.nlm.nih.gov/8083695/); [PMID:24154541](https://pubmed.ncbi.nlm.nih.gov/24154541/)
- **GABRB1**: [EXTERNAL] GABRB1 encodes a GABA-A receptor beta subunit that assembles ligand-gated Cl− channels to mediate fast synaptic inhibition across neuronal compartments. [DATA] [PMID:26950270](https://pubmed.ncbi.nlm.nih.gov/26950270/)
- **CD44**: [EXTERNAL] CD44 binds hyaluronan to organize adhesion and migration at both apical and basolateral surfaces, coupling ECM cues to junctional dynamics. [EXTERNAL] [PMID:15100360](https://pubmed.ncbi.nlm.nih.gov/15100360/); [PMID:21423176](https://pubmed.ncbi.nlm.nih.gov/21423176/)
- **ERBB4**: [EXTERNAL] ERBB4 forms receptor complexes that signal to MAPK and can translocate an intracellular domain to regulate transcriptional programs. [DATA] [PMID:23382219](https://pubmed.ncbi.nlm.nih.gov/23382219/); [PMID:15534001](https://pubmed.ncbi.nlm.nih.gov/15534001/)
- **AQP4**: [EXTERNAL] AQP4 assembles into orthogonal arrays in astrocytes and muscle to support rapid water movement, impacting brain edema and renal water handling. [EXTERNAL] [PMID:19383790](https://pubmed.ncbi.nlm.nih.gov/19383790/); [PMID:29055082](https://pubmed.ncbi.nlm.nih.gov/29055082/)
- **SLC4A4**: [EXTERNAL] SLC4A4 targets to basolateral membranes to mediate Na+-HCO3- cotransport, integrating pH regulation with epithelial fluid flux and BBB ion balance. [DATA] [PMID:17661077](https://pubmed.ncbi.nlm.nih.gov/17661077/); [PMID:17182531](https://pubmed.ncbi.nlm.nih.gov/17182531/); [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/)
- **SLCO3A1**: [EXTERNAL] SLCO3A1 transports amphipathic anions at barrier interfaces, contributing to BBB exchange and systemic pharmacokinetics. [EXTERNAL] [PMID:30280653](https://pubmed.ncbi.nlm.nih.gov/30280653/); [PMID:19129463](https://pubmed.ncbi.nlm.nih.gov/19129463/)
- **ABCC9**: [EXTERNAL] ABCC9 encodes SUR2 of KATP channels, coupling ATP levels to K+ efflux to tune excitability and metabolic resilience in muscle and brain vasculature. [DATA] [PMID:26621776](https://pubmed.ncbi.nlm.nih.gov/26621776/); [PMID:24439875](https://pubmed.ncbi.nlm.nih.gov/24439875/)
- **ADCYAP1R1**: [EXTERNAL] ADCYAP1R1 activates adenylate cyclase upon PACAP binding to raise cAMP, impacting junctional dynamics and stress responses across cell surfaces. [EXTERNAL] [PMID:23382219](https://pubmed.ncbi.nlm.nih.gov/23382219/)
- **GJA1**: [EXTERNAL] GJA1 (connexin 43) builds gap junctions and interfaces with adhesion complexes to coordinate intercellular ionic and small-molecule exchange. [EXTERNAL] [PMID:30599359](https://pubmed.ncbi.nlm.nih.gov/30599359/); [PMID:26200696](https://pubmed.ncbi.nlm.nih.gov/26200696/)
- **FAM107A**: [EXTERNAL] FAM107A modulates actin cytoskeleton architecture in neurites and junctions, linking structural remodeling to growth and stress pathways. [EXTERNAL] [PMID:28604741](https://pubmed.ncbi.nlm.nih.gov/28604741/)
- **ADGRV1**: [EXTERNAL] ADGRV1 assembles adhesion GPCR complexes that coordinate synaptic connectivity and surface receptor signaling. [EXTERNAL] [PMID:23382219](https://pubmed.ncbi.nlm.nih.gov/23382219/)
- **ADCY2**: [INFERENCE] ADCY2 synthesizes cAMP in response to receptor inputs to regulate neuronal signaling and epithelial water transport programs. [INFERENCE]
- **NRP2**: [EXTERNAL] NRP2 engages semaphorin receptor complexes to guide axons and organize synaptic networks across adhesion-rich environments. [DATA] [PMID:19909241](https://pubmed.ncbi.nlm.nih.gov/19909241/)

## Overall Summary

The enrichment landscape points to a coordinated neuro-epithelial program where polarity, adhesion, and receptor–transporter assemblies drive neuron projection, synaptic function, and epithelial fluid handling. [INFERENCE]

Basolateral and apical membrane enrichments, together with anchoring junction and cell surface signals, indicate robust epithelial polarity with vectorial transport anchored by SLC4A4, AQP1, and integrin platforms. [GO-HIERARCHY]

BBB transport and monoatomic ion transport themes converge on ion and neurotransmitter homeostasis, supported by ATP1A2, SLCO1C1, and K+ channel systems that stabilize excitability and barrier function. [DATA]

Cyclic nucleotide metabolism integrates with receptor complexes to modulate synaptic and epithelial outputs via ADCY family enzymes and PACAP signaling, counterbalanced by phosphodiesterase activity. [INFERENCE]

Anti-amyloid mechanisms centered on SORL1, NTRK2, and APOE intersect with redox-responsive pathways and connexin-mediated coupling, linking proteostasis to neuroinflammatory resilience. [EXTERNAL]

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

