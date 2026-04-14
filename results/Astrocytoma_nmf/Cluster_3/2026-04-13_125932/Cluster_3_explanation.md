# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_3_themes.csv](Cluster_3_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-neuron-projection) | [neuron projection](#theme-1-neuron-projection) [GO:0043005](http://purl.obolibrary.org/obo/GO_0043005) | CC | 1.32e-05 | 29 | FDR<0.01 |
| [2](#theme-2-postsynaptic-density-membrane) | [postsynaptic density membrane](#theme-2-postsynaptic-density-membrane) [GO:0098839](http://purl.obolibrary.org/obo/GO_0098839) | CC | 1.80e-05 | 10 | FDR<0.01 |
| [3](#theme-3-glutamatergic-synapse) | [glutamatergic synapse](#theme-3-glutamatergic-synapse) [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) | CC | 2.58e-05 | 20 | FDR<0.01 |
| [4](#theme-4-cell-cell-junction) | [cell-cell junction](#theme-4-cell-cell-junction) [GO:0005911](http://purl.obolibrary.org/obo/GO_0005911) | CC | 6.87e-04 | 17 | FDR<0.01 |
| [5](#theme-5-platelet-derived-growth-factor-receptor-signaling-pathway) | [platelet-derived growth factor receptor signaling pathway](#theme-5-platelet-derived-growth-factor-receptor-signaling-pathway) [GO:0048008](http://purl.obolibrary.org/obo/GO_0048008) | BP | 9.89e-04 | 5 | FDR<0.01 |
| [6](#theme-6-cell-cell-adhesion) | [cell-cell adhesion](#theme-6-cell-cell-adhesion) [GO:0098609](http://purl.obolibrary.org/obo/GO_0098609) | BP | 2.13e-03 | 17 | FDR<0.01 |
| [7](#theme-7-cell-adhesion-molecule-binding) | [cell adhesion molecule binding](#theme-7-cell-adhesion-molecule-binding) [GO:0050839](http://purl.obolibrary.org/obo/GO_0050839) | MF | 2.25e-03 | 20 | FDR<0.01 |
| [8](#theme-8-positive-regulation-of-intracellular-signal-transduction) | [positive regulation of intracellular signal transduction](#theme-8-positive-regulation-of-intracellular-signal-transduction) [GO:1902533](http://purl.obolibrary.org/obo/GO_1902533) | BP | 3.32e-03 | 25 | FDR<0.01 |
| [9](#theme-9-positive-regulation-of-locomotion) | [positive regulation of locomotion](#theme-9-positive-regulation-of-locomotion) [GO:0040017](http://purl.obolibrary.org/obo/GO_0040017) | BP | 4.58e-03 | 17 | FDR<0.01 |
| [10](#theme-10-regulation-of-synapse-organization) | [regulation of synapse organization](#theme-10-regulation-of-synapse-organization) [GO:0050807](http://purl.obolibrary.org/obo/GO_0050807) | BP | 7.06e-03 | 12 | FDR<0.01 |
| [11](#theme-11-regulation-of-cell-junction-assembly) | [regulation of cell junction assembly](#theme-11-regulation-of-cell-junction-assembly) [GO:1901888](http://purl.obolibrary.org/obo/GO_1901888) | BP | 8.48e-03 | 11 | FDR<0.01 |
| [12](#theme-12-cell-projection-organization) | [cell projection organization](#theme-12-cell-projection-organization) [GO:0030030](http://purl.obolibrary.org/obo/GO_0030030) | BP | 9.48e-03 | 33 | FDR<0.01 |
| [13](#theme-13-phosphate-containing-compound-metabolic-process) | [phosphate-containing compound metabolic process](#theme-13-phosphate-containing-compound-metabolic-process) [GO:0006796](http://purl.obolibrary.org/obo/GO_0006796) | BP | 9.48e-03 | 28 | FDR<0.01 |
| [14](#theme-14-learning-or-memory) | [learning or memory](#theme-14-learning-or-memory) [GO:0007611](http://purl.obolibrary.org/obo/GO_0007611) | BP | 9.48e-03 | 9 | FDR<0.01 |
| [15](#theme-15-phosphatidylinositol-mediated-signaling) | [phosphatidylinositol-mediated signaling](#theme-15-phosphatidylinositol-mediated-signaling) [GO:0048015](http://purl.obolibrary.org/obo/GO_0048015) | BP | 1.42e-02 | 4 | FDR<0.05 |
| [16](#theme-16-regulation-of-cell-adhesion) | [regulation of cell adhesion](#theme-16-regulation-of-cell-adhesion) [GO:0030155](http://purl.obolibrary.org/obo/GO_0030155) | BP | 1.61e-02 | 18 | FDR<0.05 |
| [17](#theme-17-modulation-of-excitatory-postsynaptic-potential) | [modulation of excitatory postsynaptic potential](#theme-17-modulation-of-excitatory-postsynaptic-potential) [GO:0098815](http://purl.obolibrary.org/obo/GO_0098815) | BP | 1.83e-02 | 5 | FDR<0.05 |
| [18](#theme-18-system-development) | [system development](#theme-18-system-development) [GO:0048731](http://purl.obolibrary.org/obo/GO_0048731) | BP | 1.95e-02 | 21 | FDR<0.05 |
| [19](#theme-19-cell-migration) | [cell migration](#theme-19-cell-migration) [GO:0016477](http://purl.obolibrary.org/obo/GO_0016477) | BP | 1.95e-02 | 18 | FDR<0.05 |
| [20](#theme-20-negative-regulation-of-relaxation-of-cardiac-muscle) | [negative regulation of relaxation of cardiac muscle](#theme-20-negative-regulation-of-relaxation-of-cardiac-muscle) [GO:1901898](http://purl.obolibrary.org/obo/GO_1901898) | BP | 1.96e-02 | 2 | FDR<0.05 |
| [21](#theme-21-phosphoric-diester-hydrolase-activity) | [phosphoric diester hydrolase activity](#theme-21-phosphoric-diester-hydrolase-activity) [GO:0008081](http://purl.obolibrary.org/obo/GO_0008081) | MF | 2.06e-02 | 7 | FDR<0.05 |
| [22](#theme-22-negative-regulation-of-camppka-signal-transduction) | [negative regulation of cAMP/PKA signal transduction](#theme-22-negative-regulation-of-camppka-signal-transduction) [GO:0141162](http://purl.obolibrary.org/obo/GO_0141162) | BP | 2.42e-02 | 4 | FDR<0.05 |
| [23](#theme-23-regulation-of-presynaptic-membrane-potential) | [regulation of presynaptic membrane potential](#theme-23-regulation-of-presynaptic-membrane-potential) [GO:0099505](http://purl.obolibrary.org/obo/GO_0099505) | BP | 2.69e-02 | 4 | FDR<0.05 |
| [24](#theme-24-cell-cortex) | [cell cortex](#theme-24-cell-cortex) [GO:0005938](http://purl.obolibrary.org/obo/GO_0005938) | CC | 4.15e-02 | 8 | FDR<0.05 |
| [25](#theme-25-microvillus) | [microvillus](#theme-25-microvillus) [GO:0005902](http://purl.obolibrary.org/obo/GO_0005902) | CC | 4.15e-02 | 5 | FDR<0.05 |
| [26](#theme-26-synaptic-signaling) | [synaptic signaling](#theme-26-synaptic-signaling) [GO:0099536](http://purl.obolibrary.org/obo/GO_0099536) | BP | 4.16e-02 | 11 | FDR<0.05 |
| [27](#theme-27-synapse-assembly) | [synapse assembly](#theme-27-synapse-assembly) [GO:0007416](http://purl.obolibrary.org/obo/GO_0007416) | BP | 4.58e-02 | 6 | FDR<0.05 |

---

### Theme 1: neuron projection

**Summary:** neuron projection ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))  · Anchor confidence: **FDR<0.01**

Neuron projection enrichment indicates coordinated control of axon and dendrite growth, spine formation, and receptor-scaffold coupling that tunes signal propagation and circuit wiring. [GO-HIERARCHY] Evidence within this set links postsynaptic adhesion systems and ion channel excitability to structural remodeling of projections, aligning with the nested terms dendritic spine and axon under the neuron projection anchor. [GO-HIERARCHY] NLGN4X glycosylation controls its surface delivery and synapse parameters in neurons, placing postsynaptic adhesion upstream of projection maturation and synaptic stability. [EXTERNAL] PTEN limits AKT signaling to restrain neurite arborization and synaptic plasticity, providing a brake on overgrowth of projections and activity-dependent remodeling. [EXTERNAL] NRCAM and related Ig-superfamily CAMs support fasciculation and axon guidance, stabilizing projection tracts and synaptic contacts. [DATA]

#### Key Insights

- PTEN-mediated PIP3 dephosphorylation suppresses AKT to restrict dendrite and axon elaboration, preventing hyper-arborization during activity-dependent growth. ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- Neuroligin glycosylation state tunes its postsynaptic surface abundance, coupling adhesion strength to spine maturation and excitatory synapse density within projections. ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))

#### Key Genes

- **PTCHD1**: [INFERENCE] PTCHD1 localizes to dendritic spines and modulates spine dynamics to stabilize excitatory contacts, linking membrane trafficking to projection maturation and synaptic efficacy. [DATA] ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))
- **PRICKLE2**: [INFERENCE] PRICKLE2 interfaces with planar cell polarity and Wnt effectors to bias cytoskeletal remodeling in neurites, coordinating axon–dendrite patterning and synapse alignment. [EXTERNAL] ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- **DTNA**: [INFERENCE] DTNA integrates the dystrophin-associated complex with postsynaptic adhesion networks to secure projection–synapse mechanical coupling, supporting stable signal transmission along neurites. [EXTERNAL] ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- **NCAM2**: [INFERENCE] NCAM2 promotes neurite adhesion and guidance by engaging synaptic partners to consolidate axon trajectories and dendritic architecture, strengthening projection integrity. [INFERENCE] ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **KCND3**: [INFERENCE] KCND3-mediated A-type K+ currents set firing patterns that feedback onto activity-dependent neurite growth and spine refinement, linking excitability to projection morphology. [INFERENCE] ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))

#### Statistical Context

This theme is significantly enriched for neuron projection genes with FDR 1.32e-05 and 3.1x fold enrichment across 29 annotated genes, indicating robust over-representation among input genes. [DATA] The anchor [GO:0043005](http://purl.obolibrary.org/obo/GO_0043005) (cellular_component) contains nested specific terms dendritic spine ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197)) and axon ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424)), showing hierarchical concentration at both projections and their spine substructures. [GO-HIERARCHY]

---

### Theme 2: postsynaptic density membrane

**Summary:** postsynaptic density membrane ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))  · Anchor confidence: **FDR<0.01**

Postsynaptic density membrane enrichment highlights scaffolding hubs where adhesion molecules, glutamate receptors, and auxiliary subunits co-assemble to set synaptic gain. [GO-HIERARCHY] Neuroligin-4 localizes to human cortical excitatory synapses and organizes PSD nanodomains, placing adhesion upstream of receptor clustering and excitatory drive. [DATA] NETO2 and kainate receptor subunits shape receptor assembly and kinetics, refining synaptic current waveforms that define postsynaptic responsiveness. [EXTERNAL] LRRTM3 binds neurexins and interfaces with PSD-95, enhancing synapse density without requiring PSD-95 binding for its synaptogenic output, thereby decoupling adhesion from specific scaffold dependency. [EXTERNAL]

#### Key Insights

- Human NLGN4X concentrates at PSDs to potentiate excitatory transmission, mechanistically linking adhesion to receptor clustering and synaptic strength. ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- KAR auxiliaries such as NETO2 tune receptor gating and assembly, adjusting postsynaptic depolarization dynamics at the PSD. ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))

#### Key Genes

- **NETO2**: [INFERENCE] NETO2 cooperates with postsynaptic adhesion programs to stabilize kainate receptor complexes at the PSD, sharpening excitatory current kinetics and plasticity thresholds. [EXTERNAL] ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **LRRTM3**: [INFERENCE] LRRTM3 promotes excitatory synapse formation via neurexin binding and PSD-95–connected scaffolding, increasing synapse number while functionally separating PSD-95 binding from its synaptogenic efficacy. [EXTERNAL] ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **GRIK3**: [INFERENCE] GRIK3 supplies ionotropic glutamate receptor subunits to PSDs, where subunit composition modulates Na+/Ca2+ flux and excitatory drive. [DATA] ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **NTM**: [INFERENCE] NTM engages neuroligin-based adhesion to consolidate excitatory PSD architecture, promoting receptor clustering and stable synaptic transmission. [EXTERNAL] ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))

#### Statistical Context

This theme shows strong enrichment for postsynaptic density membrane with FDR 1.80e-05 and 9.5x fold enrichment across 10 genes, indicating a concentrated PSD module. [DATA] The anchor [GO:0098839](http://purl.obolibrary.org/obo/GO_0098839) (cellular_component) captures PSD-resident adhesion and receptor complexes that hierarchically integrate synaptic structure and signaling. [GO-HIERARCHY]

---

### Theme 3: glutamatergic synapse

**Summary:** glutamatergic synapse ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))  · Anchor confidence: **FDR<0.01**

Glutamatergic synapse enrichment denotes coordinated assembly of presynaptic release machinery, trans-synaptic adhesion, and postsynaptic receptor modules that define excitatory neurotransmission. [GO-HIERARCHY] Human NLGN4X drives excitatory synapse formation and transmission, placing adhesion as a proximal regulator of synaptic number and function at glutamatergic contacts. [DATA] LRRTM3 enhances presynaptic assembly via neurexin binding and increases excitatory synapse density, mechanistically coupling postsynaptic adhesion to presynaptic organization. [DATA] Kainate receptor subunit GRIK3 and its auxiliary NETO2 tailor receptor composition and gating to sculpt postsynaptic depolarization dynamics. [DATA]

#### Key Insights

- Postsynaptic adhesion proteins (NLGN4X, LRRTM3) recruit and align presynaptic release sites via neurexin interactions, directly tuning excitatory synapse number and efficacy. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- Kainate receptor composition controlled by GRIK3 and NETO2 modifies synaptic current kinetics, influencing integration and plasticity at glutamatergic synapses. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Key Genes

- **NETO2**: [INFERENCE] NETO2 stabilizes and modulates kainate receptors at excitatory postsynapses, refining receptor assembly to adjust synaptic gain and kinetics. [EXTERNAL] ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **LRRTM3**: [INFERENCE] LRRTM3 connects neurexins to PSD scaffolds to promote presynaptic assembly and elevate excitatory synapse density, coupling adhesion to transmitter release alignment. [DATA] ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **ELMOD1**: [INFERENCE] ELMOD1 is proposed to regulate AMPA receptor trafficking into spines, tuning receptor availability during activity-dependent potentiation at excitatory synapses. [INFERENCE] ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **SIPA1L2**: [INFERENCE] SIPA1L2 likely coordinates postsynaptic complex assembly to support plasticity signaling, integrating adhesion inputs with receptor clustering at excitatory synapses. [EXTERNAL] ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Statistical Context

Glutamatergic synapse is enriched with FDR 2.58e-05 and 4.0x fold enrichment across 20 genes, supporting a pronounced excitatory synaptic signature. [DATA] The anchor [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) (cellular_component) aggregates pre- and postsynaptic modules that hierarchically define chemical excitatory transmission. [GO-HIERARCHY]

---

### Theme 4: cell-cell junction

**Summary:** cell-cell junction ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))  · Anchor confidence: **FDR<0.01**

Cell–cell junction enrichment implicates adherens and tight junction machineries that couple cadherins, polarity proteins, and the actomyosin belt to maintain cohesive tissues and regulate barrier function. [GO-HIERARCHY] E-cadherin complex interactors stabilize cadherins at junctions, and loss of junctional phosphatase–kinase balance perturbs barrier assembly and turnover. [DATA] PARD3 scaffolds polarity cues at epithelial junctions to coordinate apicobasal organization and lumen formation. [DATA] Stabilization of cadherin complexes by flotillin microdomains strengthens adhesion and limits junctional fragility. [DATA]

#### Key Insights

- Polarity scaffolds such as PARD3 spatially organize junctional complexes and actomyosin tension, aligning adhesion with epithelial morphogenesis and lumenization. ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- Tyrosine phosphatase control of junction protein phosphorylation calibrates assembly and disassembly cycles that determine barrier robustness and cell motility. ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))

#### Key Genes

- **NHS**: [INFERENCE] NHS supports adherens junction integrity by coordinating cadherin-associated cytoskeletal linkages, preserving cohesive epithelial contacts under mechanical stress. [INFERENCE] ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **PARD3B**: [INFERENCE] PARD3B organizes cortical polarity cues at junctions to bias microtubule anchoring and cadherin localization, sustaining junctional stability during remodeling. [INFERENCE] ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **MYO1E**: [INFERENCE] MYO1E links junctional cadherins to cortical actin, enhancing adhesive strength and enabling contractility-driven junction maturation. [INFERENCE] ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **ILDR2**: [INFERENCE] ILDR2 promotes assembly of adherens junctions through cooperative interactions with cadherin complexes, reinforcing epithelial cohesion. [INFERENCE] ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))

#### Statistical Context

Cell–cell junction ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911), cellular_component) is enriched with FDR 6.87e-04 and 3.6x fold enrichment across 17 genes, indicating a substantive adhesion module. [DATA] Hierarchically related junction subtypes, including adherens and tight junction components, are represented through polarity scaffolds and phosphatase regulators. [GO-HIERARCHY]

---

### Theme 5: platelet-derived growth factor receptor signaling pathway

**Summary:** platelet-derived growth factor receptor signaling pathway ([GO:0048008](http://purl.obolibrary.org/obo/GO_0048008))  · Anchor confidence: **FDR<0.01**

PDGFR signaling enrichment captures growth factor–driven activation of PI3K–AKT and MAPK cascades that promote mesenchymal proliferation, survival, and motility. [GO-HIERARCHY] PDGF-C is a protease-activated ligand for PDGFRA that triggers fibroblast proliferation and downstream kinase signaling. [DATA] NR4A3 integrates PDGF cues at the transcriptional level to potentiate VSMC migration and proliferation programs. [DATA] PTPRJ modulates PDGFR pathway outputs by dephosphorylating junctional and signaling substrates, tuning adhesion–migration balance. [DATA]

#### Key Insights

- Ligand processing of PDGF-C enables selective engagement of PDGFRA to amplify PI3K–AKT and MAPK outputs in mesenchymal contexts. ([GO:0048008](http://purl.obolibrary.org/obo/GO_0048008))
- Transcription factor NR4A3 couples receptor-proximal PDGFR signals to downstream gene programs driving cell cycle entry and motility. ([GO:0048008](http://purl.obolibrary.org/obo/GO_0048008))

#### Key Genes

- **PDGFRL**: [INFERENCE] PDGFRL attenuates PDGFR signaling, restraining excessive mitogenic and motility responses to preserve tissue homeostasis. [INFERENCE] ([GO:0048008](http://purl.obolibrary.org/obo/GO_0048008))
- **PDGFC**: [INFERENCE] PDGFC engages PDGFRA after proteolytic activation to initiate proliferative and survival signaling cascades in mesenchymal cells. [DATA] ([GO:0048008](http://purl.obolibrary.org/obo/GO_0048008))
- **NR4A3**: [INFERENCE] NR4A3 amplifies PDGFR pathway transcriptional responses that promote migration and proliferation of vascular smooth muscle cells. [DATA] ([GO:0048008](http://purl.obolibrary.org/obo/GO_0048008))

#### Statistical Context

Platelet-derived growth factor receptor signaling pathway ([GO:0048008](http://purl.obolibrary.org/obo/GO_0048008), biological_process) is highly enriched with FDR 9.89e-04 and 27.2x fold enrichment across 5 genes, reflecting a focused growth factor module. [DATA] The hierarchy situates ligand processing, receptor activation, and transcriptional effectors within a single signaling axis. [GO-HIERARCHY]

---

### Theme 6: cell-cell adhesion

**Summary:** cell-cell adhesion ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))  · Anchor confidence: **FDR<0.01**

Cell–cell adhesion enrichment highlights homophilic and heterophilic CAM interactions that assemble synapses and maintain tissue architecture through cadherin–catenin linkages and neurexin–neuroligin complexes. [GO-HIERARCHY] NLGN4X and neurexins mediate neuron cell–cell adhesion that aligns pre- and postsynaptic specializations. [DATA] N-cadherin (CDH2) supports calcium-dependent adhesion essential for development and synapse stabilization. [DATA] ADGRL3 engages FLRT and UNC5 to couple adhesion with synapse formation and neuronal migration. [DATA]

#### Key Insights

- Cadherin–catenin coupling transduces mechanical cohesion into intracellular signaling that stabilizes synaptic and epithelial contacts. ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- Neurexin–neuroligin and latrophilin–FLRT axes bridge pre- and postsynaptic membranes to coordinate synapse specification and maturation. ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))

#### Key Genes

- **NCAM2**: [INFERENCE] NCAM2 promotes neuron–neuron adhesion to stabilize synaptic contacts and guide network assembly during development. [INFERENCE] ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **CADM1**: [INFERENCE] CADM1 forms trans-synaptic adhesions that reinforce synaptic stability and align signaling nanodomains across the cleft. [EXTERNAL] ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **CTNNA3**: [INFERENCE] CTNNA3 links cadherins to actin to convert adhesive bonds into load-bearing junctions that endure mechanical stress. [EXTERNAL] ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **PTPRT**: [INFERENCE] PTPRT dephosphorylates adhesion substrates to fine-tune cadherin-based synaptic and epithelial adhesion strength. [EXTERNAL] ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))

#### Statistical Context

Cell–cell adhesion ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609), biological_process) is enriched with FDR 2.13e-03 and 3.8x fold enrichment across 17 genes, indicating robust adhesion circuitry among inputs. [DATA] The hierarchy encompasses diverse neuronal and epithelial CAM systems that converge on cytoskeletal coupling. [GO-HIERARCHY]

---

### Theme 7: cell adhesion molecule binding

**Summary:** cell adhesion molecule binding ([GO:0050839](http://purl.obolibrary.org/obo/GO_0050839))  · Anchor confidence: **FDR<0.01**

Cell adhesion molecule binding enrichment indicates effectors that recognize cadherins, integrins, and synaptic CAMs to modulate adhesion complex stability and signaling. [GO-HIERARCHY] NLGN4X and NRXN3 provide bidirectional synaptic CAM interfaces that shape synapse formation and function. [DATA] R3-type phosphatases such as PTPRJ bind cadherins to adjust phosphorylation states and adhesion strength, integrating motility cues with junctional stability. [DATA] PDLIM5 connects cadherin complexes to actin-regulatory modules to reinforce junctional resilience. [DATA]

#### Key Insights

- Cadherin-binding adaptors and phosphatases tune adhesion site phosphorylation to balance stability versus turnover during migration and synaptogenesis. ([GO:0050839](http://purl.obolibrary.org/obo/GO_0050839))
- Synaptic CAM ligand–receptor pairs (neuroligins–neurexins) are core binding interactions that instruct synapse identity and efficacy. ([GO:0050839](http://purl.obolibrary.org/obo/GO_0050839))

#### Key Genes

- **ADAM23**: [INFERENCE] ADAM23 stabilizes CAM interactions at excitatory synapses, organizing adhesive microdomains that favor efficient neurotransmission. [EXTERNAL] ([GO:0050839](http://purl.obolibrary.org/obo/GO_0050839))
- **CTNNA3**: [INFERENCE] CTNNA3 promotes high-affinity cadherin engagement by coupling extracellular binding to cytoskeletal anchoring. [EXTERNAL] ([GO:0050839](http://purl.obolibrary.org/obo/GO_0050839))
- **NRXN3**: [INFERENCE] NRXN3 presents synaptic ligands for neuroligins to drive selective adhesion and signaling across the synaptic cleft. [EXTERNAL] ([GO:0050839](http://purl.obolibrary.org/obo/GO_0050839))
- **NPNT**: [INFERENCE] NPNT serves as an extracellular matrix linker facilitating integrin–CAM binding that consolidates adhesion sites. [INFERENCE] ([GO:0050839](http://purl.obolibrary.org/obo/GO_0050839))

#### Statistical Context

Cell adhesion molecule binding ([GO:0050839](http://purl.obolibrary.org/obo/GO_0050839), molecular_function) is enriched with FDR 2.25e-03 and 3.6x fold enrichment across 20 genes, supporting a strong CAM-interaction layer. [DATA] The hierarchy situates ligand-binding activities that control cadherin, integrin, and synaptic CAM engagement. [GO-HIERARCHY]

---

### Theme 8: positive regulation of intracellular signal transduction

**Summary:** positive regulation of intracellular signal transduction ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))  · Anchor confidence: **FDR<0.01**

Positive regulation of intracellular signal transduction enrichment reflects coordinated activation of MAPK and PI3K–AKT cascades by growth factors and guidance cues to drive adaptive responses. [GO-HIERARCHY] PDGF ligands engaging PDGFRA elevate MAPK and PI3K–AKT activities to promote proliferation and survival. [DATA] NTRK3 signaling enhances motility and chemotaxis upon NT-3 stimulation, aligning trophic signaling with migration programs. [DATA] SEMA3E boosts PI3K–AKT signaling to support neuronal migration during development, linking guidance to intracellular amplification. [DATA]

#### Key Insights

- Activation of PDGFRA by PDGF-C converges on MAPK and PI3K–AKT branches to integrate mitogenic and survival outputs. ([GO:1902533](http://purl.obolibrary.org/obo/GO_1902533))
- G protein–coupled receptor pathways, exemplified by NPSR1, co-activate ERK and cAMP axes to diversify signal amplification modes. ([GO:0043410](http://purl.obolibrary.org/obo/GO_0043410))

#### Key Genes

- **NOX4**: [INFERENCE] NOX4-derived ROS act as second messengers to potentiate kinase cascades such as p38 MAPK, sensitizing cells to pro-apoptotic or inflammatory signals. [EXTERNAL] ([GO:0043410](http://purl.obolibrary.org/obo/GO_0043410))
- **PDGFC**: [INFERENCE] PDGFC engagement of PDGFRA promotes PI3K–AKT activation to drive anabolic and survival signaling in mesenchymal cells. [DATA] ([GO:0051897](http://purl.obolibrary.org/obo/GO_0051897))
- **PDGFRA**: [INFERENCE] PDGFRA transduces ligand inputs into MAPK activation, sustaining proliferative signaling upon PDGF stimulation. [DATA] ([GO:0043410](http://purl.obolibrary.org/obo/GO_0043410))
- **NTRK3**: [INFERENCE] NTRK3 propagates neurotrophin cues into MAPK and PI3K pathways that augment migration and chemotaxis. [DATA] ([GO:0043410](http://purl.obolibrary.org/obo/GO_0043410))

#### Statistical Context

This theme is enriched with FDR 3.32e-03 and 2.7x fold enrichment across 25 genes, with nested terms highlighting MAPK cascade and PI3K–AKT upregulation. [DATA] The anchor [GO:1902533](http://purl.obolibrary.org/obo/GO_1902533) (biological_process) organizes upstream receptors and intracellular amplifiers that hierarchically coordinate signal gain. [GO-HIERARCHY]

---

### Theme 9: positive regulation of locomotion

**Summary:** positive regulation of locomotion ([GO:0040017](http://purl.obolibrary.org/obo/GO_0040017))  · Anchor confidence: **FDR<0.01**

Positive regulation of locomotion enrichment links adhesion remodeling, cytoskeletal dynamics, and chemotactic signaling to enhanced cell migration. [GO-HIERARCHY] PRKD1 downstream of VEGF promotes endothelial chemotaxis by coordinating cytoskeletal reorganization and focal adhesion turnover. [DATA] NTRK3 activation by NT-3 stimulates migratory and chemotactic programs in carcinoma models, demonstrating trophic control over locomotion. [DATA] PDGFRA signaling enhances mesenchymal migration, integrating growth cues with motility. [DATA]

#### Key Insights

- Kinase pathways (PKD, TrkC) couple receptor activation to Rho–actin remodeling that boosts protrusion–adhesion cycles during motility. ([GO:0040017](http://purl.obolibrary.org/obo/GO_0040017))
- Pro-migratory cues also elevate chemotaxis, indicating shared upstream effectors governing directional sensing and speed. ([GO:0050921](http://purl.obolibrary.org/obo/GO_0050921))

#### Key Genes

- **F3**: [INFERENCE] Tissue factor initiates thrombin generation and downstream PAR signaling that potentiates motility programs in vascular and tumor contexts. [INFERENCE] ([GO:0030335](http://purl.obolibrary.org/obo/GO_0030335))
- **NEDD9**: [INFERENCE] NEDD9 scaffolds focal adhesion and Src-family signaling to intensify lamellipodial dynamics and cell migration. [INFERENCE] ([GO:0030335](http://purl.obolibrary.org/obo/GO_0030335))
- **PRKD1**: [INFERENCE] PRKD1 amplifies endothelial cell chemotaxis by integrating VEGF signals with actin remodeling and adhesion turnover. [DATA] ([GO:0050921](http://purl.obolibrary.org/obo/GO_0050921))
- **PDGFRA**: [INFERENCE] PDGFRA activation stimulates downstream migration pathways that coordinate protrusive activity and adhesion cycling. [DATA] ([GO:0030335](http://purl.obolibrary.org/obo/GO_0030335))

#### Statistical Context

Positive regulation of locomotion ([GO:0040017](http://purl.obolibrary.org/obo/GO_0040017), biological_process) is enriched with FDR 4.58e-03 and 3.5x fold enrichment across 17 genes, including nested terms for positive regulation of cell migration and chemotaxis. [DATA] The hierarchy captures both speed and directional control modules of motility. [GO-HIERARCHY]

---

### Theme 10: regulation of synapse organization

**Summary:** regulation of synapse organization ([GO:0050807](http://purl.obolibrary.org/obo/GO_0050807))  · Anchor confidence: **FDR<0.01**

Regulation of synapse organization enrichment pinpoints adhesion–scaffold effectors that govern presynaptic assembly, postsynaptic clustering, and synapse maturation. [GO-HIERARCHY] LRRTM3 drives presynaptic assembly through neurexin binding while increasing synapse density independent of PSD-95 binding, uncoupling scaffold affinity from synaptogenic potency. [DATA] NLGN4X regulates human excitatory synapse assembly, linking postsynaptic adhesion to synapse number and efficacy. [DATA] NTM likely stabilizes PSD complexes to maintain synapse architecture and transmission fidelity. [EXTERNAL]

#### Key Insights

- Trans-synaptic adhesion molecules orchestrate presynaptic active zone recruitment and postsynaptic receptor clustering to refine synapse topology. ([GO:0050807](http://purl.obolibrary.org/obo/GO_0050807))
- Scaffold-independent synaptogenic programs ensure robustness of synapse assembly when specific adaptor interactions are perturbed. ([GO:0050807](http://purl.obolibrary.org/obo/GO_0050807))

#### Key Genes

- **SIPA1L1**: [INFERENCE] SIPA1L1 modulates clustering of postsynaptic proteins and may couple adhesion signals to structural maturation of excitatory synapses. [EXTERNAL] ([GO:0050807](http://purl.obolibrary.org/obo/GO_0050807))
- **LRRTM3**: [INFERENCE] LRRTM3 coordinates presynaptic assembly through neurexin binding to upscale synapse number and transmitter release sites. [DATA] ([GO:0050807](http://purl.obolibrary.org/obo/GO_0050807))
- **NTM**: [INFERENCE] NTM enhances stabilization of synaptic adhesion and PSD scaffolds to preserve synapse structure and throughput. [EXTERNAL] ([GO:0050807](http://purl.obolibrary.org/obo/GO_0050807))

#### Statistical Context

Regulation of synapse organization ([GO:0050807](http://purl.obolibrary.org/obo/GO_0050807), biological_process) is enriched with FDR 7.06e-03 and 4.5x fold enrichment across 12 genes, indicating a pronounced synaptogenic regulatory module. [DATA] The hierarchy integrates presynaptic assembly and postsynaptic clustering under a common organizational process. [GO-HIERARCHY]

---

### Theme 11: regulation of cell junction assembly

**Summary:** regulation of cell junction assembly ([GO:1901888](http://purl.obolibrary.org/obo/GO_1901888))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 8.48e-03 · **Genes (11)**: EPHA3, LRRTM3, LZTS1, NLGN4X, NTM, NTRK3, PDLIM5, PHLDB2, PRKCA, PTEN, PTPRJ

---

### Theme 12: cell projection organization

**Summary:** cell projection organization ([GO:0030030](http://purl.obolibrary.org/obo/GO_0030030))  · Anchor confidence: **FDR<0.01**

Cell projection organization enrichment reflects regulators of neurite morphogenesis and protrusion dynamics that align signaling with actin–microtubule remodeling. [GO-HIERARCHY] PTEN constrains neuron projection development by dampening PI3K–AKT signaling, ensuring controlled arborization. [DATA] SEMA3A directs basal dendrite arborization via RhoA-dependent cytoskeletal reorganization, linking guidance cues to projection shape. [DATA] PRKD1 promotes migration-associated protrusion remodeling, aligning kinase signaling with projection dynamics. [DATA]

#### Key Insights

- Balancing PI3K–AKT activity via PTEN prevents unchecked neurite outgrowth, coupling metabolic status to morphogenesis. ([GO:0030030](http://purl.obolibrary.org/obo/GO_0030030))
- Semaphorin–plexin signaling converts extracellular positional information into Rho GTPase programs that sculpt dendrites and axons. ([GO:0048812](http://purl.obolibrary.org/obo/GO_0048812))

#### Key Genes

- **PTN**: [INFERENCE] PTN engages integrins to strengthen adhesion–protrusion coupling, supporting extension and stabilization of cellular projections. [EXTERNAL] ([GO:0031346](http://purl.obolibrary.org/obo/GO_0031346))
- **EPHA3**: [INFERENCE] EPHA3 signaling reshapes focal adhesion–cytoskeleton linkage to direct protrusion assembly during neurite pathfinding. [DATA] ([GO:0010975](http://purl.obolibrary.org/obo/GO_0010975))
- **PRKD1**: [INFERENCE] PRKD1 coordinates protrusive dynamics and chemotaxis, facilitating projection extension during directed migration. [DATA] ([GO:0031346](http://purl.obolibrary.org/obo/GO_0031346))
- **SEMA3A**: [INFERENCE] SEMA3A triggers cytoskeletal remodeling programs to define dendritic architecture and projection polarity. [DATA] ([GO:0048812](http://purl.obolibrary.org/obo/GO_0048812))

#### Statistical Context

Cell projection organization ([GO:0030030](http://purl.obolibrary.org/obo/GO_0030030), biological_process) is enriched with FDR 9.48e-03 and 2.7x fold enrichment across 22 genes, with nested terms for regulation of neuron projection development, morphogenesis, and positive regulation of projection organization. [DATA] The hierarchy captures upstream guidance and downstream cytoskeletal executors that shape projections. [GO-HIERARCHY]

---

### Theme 13: phosphate-containing compound metabolic process

**Summary:** phosphate-containing compound metabolic process ([GO:0006796](http://purl.obolibrary.org/obo/GO_0006796))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 9.48e-03 · **Genes (28)**: ACSBG1, ADCY2, EPHA3, FHIT, NAMPT, NEK6, NUAK1, PDE4B, PDE4D, PDGFRA, PITPNC1, PLCB4, PLCE1, PLCG2, PLCH1 … (+13 more)

---

### Theme 14: learning or memory

**Summary:** learning or memory ([GO:0007611](http://purl.obolibrary.org/obo/GO_0007611))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 9.48e-03 · **Genes (9)**: GRIA1, GRIN2B, NEDD9, NLGN4X, NRXN3, PRKCA, PTEN, PTN, PTPRZ1

---

### Theme 15: phosphatidylinositol-mediated signaling

**Summary:** phosphatidylinositol-mediated signaling ([GO:0048015](http://purl.obolibrary.org/obo/GO_0048015))  · Anchor confidence: **FDR<0.05**

Phosphatidylinositol-mediated signaling enrichment captures PLC-driven PIP2 hydrolysis to generate IP3 and DAG, initiating Ca2+ release and PKC activation downstream of receptors. [GO-HIERARCHY] PLCH1 and PLCB4 catalyze PIP2 cleavage to mobilize Ca2+ and activate PKC, linking surface receptors to intracellular effectors. [DATA] PLCG2 provides immune and microglial PI signaling competence central to inflammatory responses. [DATA] PLCE1 supports PI signaling dynamics in excitable and secretory cells. [DATA]

#### Key Insights

- Diversified PLC isozymes partition across receptor classes to translate PIP2 into IP3–DAG signals with cell type–specific kinetics. ([GO:0048015](http://purl.obolibrary.org/obo/GO_0048015))
- IP3-driven Ca2+ mobilization and DAG–PKC activation form a bifurcated signaling core that couples receptor engagement to rapid effector responses. ([GO:0048015](http://purl.obolibrary.org/obo/GO_0048015))

#### Key Genes

- **PLCH1**: [INFERENCE] PLCH1 hydrolyzes PIP2 to IP3 and DAG, actuating Ca2+ mobilization and PKC signaling after receptor activation. [DATA] ([GO:0048015](http://purl.obolibrary.org/obo/GO_0048015))
- **PLCB4**: [INFERENCE] PLCB4 links Gq-coupled receptors to PIP2 hydrolysis, converting ligand binding into Ca2+ and PKC activation. [EXTERNAL] ([GO:0048015](http://purl.obolibrary.org/obo/GO_0048015))
- **PLCE1**: [INFERENCE] PLCE1 sustains PI signaling by producing IP3/DAG second messengers to drive Ca2+ release and PKC activation. [EXTERNAL] ([GO:0048015](http://purl.obolibrary.org/obo/GO_0048015))
- **PLCG2**: [INFERENCE] PLCG2 delivers PI hydrolytic activity essential for immune receptor signaling and microglial inflammatory responses. [DATA] ([GO:0048015](http://purl.obolibrary.org/obo/GO_0048015))

#### Statistical Context

Phosphatidylinositol-mediated signaling ([GO:0048015](http://purl.obolibrary.org/obo/GO_0048015), biological_process) is enriched with FDR 1.42e-02 and 19.9x fold enrichment across 4 genes, indicating a tightly focused PI signaling node. [DATA] The hierarchy situates PLC isozymes as proximal transducers of receptor inputs. [GO-HIERARCHY]

---

### Theme 16: regulation of cell adhesion

**Summary:** regulation of cell adhesion ([GO:0030155](http://purl.obolibrary.org/obo/GO_0030155))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.61e-02 · **Genes (18)**: ADAM9, CARMIL1, EPHA3, GLI3, ILDR2, NEDD9, NPNT, NR4A3, NUAK1, PAG1, PHLDB2, PODXL, PRKCA, PTEN, PTPRG … (+3 more)

---

### Theme 17: modulation of excitatory postsynaptic potential

**Summary:** modulation of excitatory postsynaptic potential ([GO:0098815](http://purl.obolibrary.org/obo/GO_0098815))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.83e-02 · **Genes (5)**: GRIA1, GRIN2B, NLGN4X, PTEN, TMEM108

---

### Theme 18: system development

**Summary:** system development ([GO:0048731](http://purl.obolibrary.org/obo/GO_0048731))  · Anchor confidence: **FDR<0.05**

System development enrichment aggregates neuronal adhesion molecules, growth factors, and transcriptional regulators that drive tissue patterning and organogenesis. [GO-HIERARCHY] PDGF-C contributes to central nervous system development through PDGFR signaling that supports proliferation and differentiation. [DATA] NRCAM mediates CNS development by guiding axonal growth and synapse formation. [DATA] Semaphorin–neuropilin signaling orchestrates sympathetic and sensory system development, integrating guidance with growth pathways. [DATA]

#### Key Insights

- Adhesion molecule networks (NRCAM, ADAM family) and growth factors (PDGFC) converge to coordinate axon guidance with tissue morphogenesis. ([GO:0048731](http://purl.obolibrary.org/obo/GO_0048731))
- Heparan sulfate remodeling and semaphorin signaling shape gradients and receptor availability to position developing circuits. ([GO:0048731](http://purl.obolibrary.org/obo/GO_0048731))

#### Key Genes

- **CNTNAP3B**: [INFERENCE] CNTNAP3B promotes neuronal adhesion and axon guidance necessary for assembling functional neural circuits. [INFERENCE] ([GO:0048731](http://purl.obolibrary.org/obo/GO_0048731))
- **DPF3**: [INFERENCE] DPF3 modulates chromatin at neurodevelopmental genes to support differentiation and axon growth programs. [EXTERNAL] ([GO:0048731](http://purl.obolibrary.org/obo/GO_0048731))
- **GAS7**: [INFERENCE] GAS7 facilitates adhesion-coupled neurite outgrowth to align migration and axon extension during development. [EXTERNAL] ([GO:0048731](http://purl.obolibrary.org/obo/GO_0048731))
- **DCLK2**: [INFERENCE] DCLK2 supports neuronal differentiation and migration to refine layer-specific connectivity. [EXTERNAL] ([GO:0048731](http://purl.obolibrary.org/obo/GO_0048731))

#### Statistical Context

System development ([GO:0048731](http://purl.obolibrary.org/obo/GO_0048731), biological_process) is enriched with FDR 1.95e-02 and 2.6x fold enrichment across 21 genes, representing coordinated morphogenetic programs. [DATA] The hierarchy spans nervous system and sensory system development under shared patterning mechanisms. [GO-HIERARCHY]

---

### Theme 19: cell migration

**Summary:** cell migration ([GO:0016477](http://purl.obolibrary.org/obo/GO_0016477))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.95e-02 · **Genes (18)**: ADAM9, ADGRL3, CARMIL1, CDH2, CTNNA3, EPHA3, FMN2, NEDD9, NRCAM, NTRK3, PDE4B, PDGFRA, PHLDB2, PODXL, PTEN … (+3 more)

---

### Theme 20: negative regulation of relaxation of cardiac muscle

**Summary:** negative regulation of relaxation of cardiac muscle ([GO:1901898](http://purl.obolibrary.org/obo/GO_1901898))  · Anchor confidence: **FDR<0.05**

Negative regulation of relaxation of cardiac muscle enrichment pinpoints cAMP phosphodiesterases that limit PKA signaling to reduce lusitropy. [GO-HIERARCHY] PDE4D and PDE4B hydrolyze cAMP, lowering PKA activity and thereby constraining relaxation signaling downstream of β-adrenergic input. [DATA] By shaping spatiotemporal cAMP pools, PDE4 isoforms set contractility–relaxation balance in cardiomyocytes. [INFERENCE]

#### Key Insights

- Targeted degradation of cAMP by PDE4 isoforms curtails PKA-driven phosphorylation of Ca2+-handling proteins, reducing relaxation. ([GO:1901898](http://purl.obolibrary.org/obo/GO_1901898))
- Compartmentalized phosphodiesterase activity creates microdomains that tune β-adrenergic responses in the heart. ([GO:1901898](http://purl.obolibrary.org/obo/GO_1901898))

#### Key Genes

- **PDE4D**: [INFERENCE] PDE4D limits cAMP availability to restrain PKA-dependent lusitropic signaling in cardiac muscle. [INFERENCE] ([GO:1901898](http://purl.obolibrary.org/obo/GO_1901898))
- **PDE4B**: [INFERENCE] PDE4B contributes to cAMP degradation, complementing PDE4D to dampen relaxation pathways under adrenergic stimulation. [DATA] ([GO:1901898](http://purl.obolibrary.org/obo/GO_1901898))

#### Statistical Context

Negative regulation of relaxation of cardiac muscle ([GO:1901898](http://purl.obolibrary.org/obo/GO_1901898), biological_process) is enriched with FDR 1.96e-02 and 114.4x fold enrichment across 2 genes, consistent with a narrowly specialized regulatory axis. [DATA] The hierarchy situates PDE-mediated control within cardiac relaxation processes. [GO-HIERARCHY]

---

### Theme 21: phosphoric diester hydrolase activity

**Summary:** phosphoric diester hydrolase activity ([GO:0008081](http://purl.obolibrary.org/obo/GO_0008081))  · Anchor confidence: **FDR<0.05**

Phosphoric diester hydrolase activity enrichment unites PLCs and PDEs that cleave phosphodiester bonds to generate or terminate second messengers. [GO-HIERARCHY] PLCG2 hydrolyzes PIP2 to IP3 and DAG to elicit Ca2+ mobilization and PKC activation, positioning it as a central inflammatory signaling node. [DATA] PDE1C and PDE4 isoforms degrade cyclic nucleotides to sculpt cAMP/cGMP signaling dynamics. [DATA]

#### Key Insights

- Balanced PLC production of IP3/DAG and PDE degradation of cyclic nucleotides ensures precise timing and amplitude of intracellular signals. ([GO:0008081](http://purl.obolibrary.org/obo/GO_0008081))
- Isozyme diversity enables spatial compartmentalization of hydrolase activities across receptor microdomains. ([GO:0008081](http://purl.obolibrary.org/obo/GO_0008081))

#### Key Genes

- **PDE1C**: [INFERENCE] PDE1C hydrolyzes cAMP and cGMP to constrain cyclic nucleotide signaling and downstream kinase activation. [DATA] ([GO:0008081](http://purl.obolibrary.org/obo/GO_0008081))
- **PLCB4**: [INFERENCE] PLCB4 generates IP3 and DAG from PIP2, coupling receptor activation to Ca2+ release and PKC signaling. [EXTERNAL] ([GO:0008081](http://purl.obolibrary.org/obo/GO_0008081))
- **PLCE1**: [INFERENCE] PLCE1 supports PI signaling by producing IP3/DAG second messengers to drive rapid effector responses. [EXTERNAL] ([GO:0008081](http://purl.obolibrary.org/obo/GO_0008081))

#### Statistical Context

Phosphoric diester hydrolase activity ([GO:0008081](http://purl.obolibrary.org/obo/GO_0008081), molecular_function) is enriched with FDR 2.06e-02 and 9.1x fold enrichment across 7 genes, capturing key signal-generating and -terminating enzymes. [DATA] The hierarchy integrates lipid and cyclic nucleotide hydrolases under a common catalytic function. [GO-HIERARCHY]

---

### Theme 22: negative regulation of cAMP/PKA signal transduction

**Summary:** negative regulation of cAMP/PKA signal transduction ([GO:0141162](http://purl.obolibrary.org/obo/GO_0141162))  · Anchor confidence: **FDR<0.05**

Negative regulation of cAMP/PKA signal transduction enrichment reflects degradation and sequestration mechanisms that restrain PKA activity. [GO-HIERARCHY] PRKAR2B regulatory subunits bind catalytic PKA to prevent activity until cAMP rises, enforcing basal inhibition. [DATA] PDE4D and PDE1C hydrolyze cAMP to lower PKA activation probability, coordinating temporal shutoff of signaling. [DATA]

#### Key Insights

- Regulatory subunits and phosphodiesterases operate in tandem to limit PKA activity, shaping stimulus thresholds and recovery kinetics. ([GO:0141162](http://purl.obolibrary.org/obo/GO_0141162))
- Compartmentalized cAMP degradation by PDEs enforces local PKA inhibition in distinct subcellular domains. ([GO:0141162](http://purl.obolibrary.org/obo/GO_0141162))

#### Key Genes

- **PDE1C**: [INFERENCE] PDE1C lowers cAMP in Ca2+/calmodulin-regulated fashion to restrain PKA activity in excitable cells. [INFERENCE] ([GO:0141162](http://purl.obolibrary.org/obo/GO_0141162))
- **PDE4D**: [INFERENCE] PDE4D degrades cAMP to reduce PKA signaling, dominating cAMP control in T cell receptor contexts and beyond. [DATA] ([GO:0141162](http://purl.obolibrary.org/obo/GO_0141162))
- **PRKAR2B**: [INFERENCE] PRKAR2B sequesters PKA catalytic subunits to enforce inactivity until cAMP binding releases them. [DATA] ([GO:0141162](http://purl.obolibrary.org/obo/GO_0141162))

#### Statistical Context

Negative regulation of cAMP/PKA signal transduction ([GO:0141162](http://purl.obolibrary.org/obo/GO_0141162), biological_process) is enriched with FDR 2.42e-02 and 16.3x fold enrichment across 4 genes, indicating a defined inhibitory module. [DATA] The hierarchy emphasizes enzymatic degradation and regulatory sequestration as convergent brakes on PKA. [GO-HIERARCHY]

---

### Theme 23: regulation of presynaptic membrane potential

**Summary:** regulation of presynaptic membrane potential ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505))  · Anchor confidence: **FDR<0.05**

Regulation of presynaptic membrane potential enrichment focuses on ionotropic glutamate receptors and voltage-gated sodium channels that shape presynaptic excitability and release probability. [GO-HIERARCHY] SCN1A governs action potential initiation and propagation to set presynaptic depolarization waveforms and Ca2+ entry. [INFERENCE] Kainate and NMDA receptor subunits modulate tonic conductances and presynaptic excitability, tuning neurotransmitter output. [INFERENCE]

#### Key Insights

- Voltage-gated Na+ channels set the timing and amplitude of presynaptic spikes that drive Ca2+ influx and vesicle fusion. ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505))
- Presynaptic glutamate receptors adjust terminal excitability and release probability through modulatory conductances. ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505))

#### Key Genes

- **SCN1A**: [INFERENCE] SCN1A determines spike threshold and waveform in axons, controlling presynaptic depolarization and transmitter release triggering. [INFERENCE] ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505))
- **GRIK3**: [INFERENCE] GRIK3-containing kainate receptors contribute modulatory currents that influence presynaptic membrane potential and glutamate release. [INFERENCE] ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505))

#### Statistical Context

Regulation of presynaptic membrane potential ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505), biological_process) is enriched with FDR 2.69e-02 and 15.8x fold enrichment across 4 genes, indicating a discrete excitability control set. [DATA] The hierarchy centers on channels and receptors that shape presynaptic depolarization. [GO-HIERARCHY]

---

### Theme 24: cell cortex

**Summary:** cell cortex ([GO:0005938](http://purl.obolibrary.org/obo/GO_0005938))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 4.15e-02 · **Genes (8)**: FMN2, MYO5B, NEDD9, PARD3, PARD3B, PHLDB2, PRKD1, STOX1

---

### Theme 25: microvillus

**Summary:** microvillus ([GO:0005902](http://purl.obolibrary.org/obo/GO_0005902))  · Anchor confidence: **FDR<0.05**

Microvillus enrichment identifies actin–membrane coupling and motor systems that build and maintain apical protrusions for surface area expansion and signaling. [GO-HIERARCHY] MYO1E links actin to membrane cargo to stabilize microvillar architecture and trafficking. [INFERENCE] PROM1 regulates apical membrane organization to support microvillus formation and receptor distribution. [INFERENCE] FMN2 fosters actin filament elongation to sustain microvillus core bundles. [INFERENCE]

#### Key Insights

- Actin polymerization and myosin-based membrane trafficking cooperate to construct durable, absorptive microvilli. ([GO:0005902](http://purl.obolibrary.org/obo/GO_0005902))
- Apical membrane organizers such as PROM1 pattern lipid–protein domains to stabilize microvillus arrays. ([GO:0005902](http://purl.obolibrary.org/obo/GO_0005902))

#### Key Genes

- **MYO1E**: [INFERENCE] MYO1E couples cortical actin to apical membranes, supporting vesicle movement and microvillus stability. [INFERENCE] ([GO:0005902](http://purl.obolibrary.org/obo/GO_0005902))
- **PROM1**: [INFERENCE] PROM1 organizes apical membrane microdomains to promote microvillus biogenesis and maintenance. [INFERENCE] ([GO:0005902](http://purl.obolibrary.org/obo/GO_0005902))
- **FMN2**: [INFERENCE] FMN2 elongates actin filaments to reinforce microvillus core bundles and apical surface architecture. [INFERENCE] ([GO:0005902](http://purl.obolibrary.org/obo/GO_0005902))

#### Statistical Context

Microvillus ([GO:0005902](http://purl.obolibrary.org/obo/GO_0005902), cellular_component) is enriched with FDR 4.15e-02 and 7.8x fold enrichment across 5 genes, indicating a compact apical morphogenesis module. [DATA] The hierarchy situates actin–membrane coupling components within specialized apical structures. [GO-HIERARCHY]

---

### Theme 26: synaptic signaling

**Summary:** synaptic signaling ([GO:0099536](http://purl.obolibrary.org/obo/GO_0099536))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 4.16e-02 · **Genes (11)**: DTNA, GRIA1, GRIK3, GRIN2B, KCND3, PMP22, PRKAR2B, PTCHD1, PTEN, SLC1A2, SNTG1

---

### Theme 27: synapse assembly

**Summary:** synapse assembly ([GO:0007416](http://purl.obolibrary.org/obo/GO_0007416))  · Anchor confidence: **FDR<0.05**

Synapse assembly enrichment emphasizes trans-synaptic adhesion systems and lipid phosphatase brakes that together set synapse number and stability. [GO-HIERARCHY] NLGN4X promotes synapse assembly at human excitatory synapses, linking adhesion to postsynaptic receptor clustering. [DATA] NRCAM drives synapse assembly via Ig-superfamily interactions that stabilize contacts. [DATA] PTEN tempers synaptogenesis by limiting AKT-driven structural consolidation, balancing assembly with pruning. [EXTERNAL]

#### Key Insights

- Trans-synaptic adhesion pairs nucleate synaptic specializations and align release sites with receptor nanodomains. ([GO:0007416](http://purl.obolibrary.org/obo/GO_0007416))
- PI3K–AKT pathway restraint by PTEN prevents exuberant synapse accumulation and supports circuit refinement. ([GO:0007416](http://purl.obolibrary.org/obo/GO_0007416))

#### Key Genes

- **NLGN4X**: [INFERENCE] NLGN4X organizes excitatory synapse assembly by bridging neurexins to PSD scaffolds and clustering receptors. [DATA] ([GO:0007416](http://purl.obolibrary.org/obo/GO_0007416))
- **NRCAM**: [INFERENCE] NRCAM mediates synaptic adhesion to stabilize nascent contacts and promote assembly. [DATA] ([GO:0007416](http://purl.obolibrary.org/obo/GO_0007416))
- **CDH2**: [INFERENCE] CDH2 supports adherens-like synaptic junctions that reinforce assembly and stabilize maturing synapses. [INFERENCE] ([GO:0007416](http://purl.obolibrary.org/obo/GO_0007416))

#### Statistical Context

Synapse assembly ([GO:0007416](http://purl.obolibrary.org/obo/GO_0007416), biological_process) is enriched with FDR 4.58e-02 and 7.1x fold enrichment across 6 genes, reflecting a concentrated synaptogenic adhesion module. [DATA] The hierarchy positions adhesion-driven nucleation as a proximal event in synaptogenesis. [GO-HIERARCHY]

---

## Hub Genes

- **PTEN**: [INFERENCE] PTEN dephosphorylates PIP3 to restrain AKT signaling, thereby limiting neurite arborization, synaptogenesis, and plasticity across projection, synapse assembly, and learning themes. [EXTERNAL]
- **NLGN4X**: [INFERENCE] NLGN4X localizes to human excitatory PSDs and promotes synapse assembly, with glycosylation controlling surface abundance and synaptic strength across postsynaptic membrane, glutamatergic synapse, adhesion, and EPSP modulation themes. [DATA]
- **NRCAM**: [INFERENCE] NRCAM, an Ig-superfamily CAM, supports axon guidance and synapse assembly, stabilizing projection tracts and nascent synaptic contacts across neuron projection and synaptogenesis themes. [DATA]
- **GRIA1**: [INFERENCE] GRIA1 mediates fast AMPA currents to drive depolarization and activity-dependent behaviors, coordinating with junction and projection modules to influence locomotion and synaptic signaling. [INFERENCE]
- **NTRK3**: [INFERENCE] NTRK3 activates PI3K–AKT and MAPK pathways upon NT-3 binding to enhance migration, chemotaxis, and synapse organization across signaling and locomotion themes. [DATA]
- **PTPRJ**: [INFERENCE] PTPRJ promotes focal adhesion assembly and modulates PDGFR signaling, integrating adhesion dynamics with motility and intracellular signal amplification across junction and migration themes. [DATA]
- **PRKCA**: [INFERENCE] PRKCA phosphorylates cytoskeletal and adhesion regulators to enhance motility and synaptic organization, bridging MAPK and Rho GTPase outputs across migration and junction themes. [EXTERNAL]
- **PDGFRA**: [INFERENCE] PDGFRA transduces PDGF-C signals to activate PI3K–AKT and MAPK, coordinating proliferation, migration, and projection remodeling across growth factor and locomotion themes. [DATA]
- **CDH2**: [INFERENCE] CDH2 forms adherens junctions linking to the actin cytoskeleton, stabilizing synaptic and epithelial adhesion across junction, adhesion, and synapse organization themes. [DATA]
- **GRIN2B**: [INFERENCE] GRIN2B confers NMDA receptor Ca2+ permeability that supports LTP, EPSP enhancement, and memory, coordinating with PSD organization and synaptic signaling themes. [DATA]
- **ADGRL3**: [INFERENCE] ADGRL3 (latrophilin-3) binds FLRT/UNC5 to couple adhesion with synapse formation and neuronal migration across adhesion and synaptogenesis themes. [DATA]
- **SEMA3A**: [INFERENCE] SEMA3A guides basal dendrite arborization via RhoA signaling, aligning projection morphogenesis with system development and locomotor circuitry themes. [DATA]
- **PRKD1**: [INFERENCE] PRKD1 promotes endothelial migration and chemotaxis through autophosphorylation-driven signaling, coordinating projection dynamics and adhesion turnover across migration themes. [DATA]
- **NEDD9**: [INFERENCE] NEDD9 scaffolds Src and focal adhesion components to drive adhesion turnover and synapse-associated structural plasticity across locomotion and synapse organization themes. [INFERENCE]
- **PDE4B**: [INFERENCE] PDE4B hydrolyzes cAMP to restrain PKA signaling, impacting cardiac relaxation, synaptic signaling, and neuron projection plasticity across cyclic nucleotide themes. [DATA]
- **EPHA3**: [INFERENCE] EPHA3 modulates focal adhesion assembly via CrkII–Rho signaling, coordinating de-adhesion with projection guidance across junction assembly and projection organization themes. [DATA]
- **PDLIM5**: [INFERENCE] PDLIM5 binds cadherin complexes at adherens junctions, linking adhesion to cytoskeletal modules across cell–cell junction and synapse organization themes. [DATA]
- **ADAM9**: [INFERENCE] ADAM9 enhances cell migration by proteolytic remodeling of the pericellular matrix, coupling adhesion modulation to intracellular signaling across locomotion and adhesion themes. [EXTERNAL]
- **PTN**: [INFERENCE] PTN binds integrins to promote adhesion and locomotion and may influence learning via synaptic plasticity, coordinating projection organization with system development themes. [EXTERNAL]
- **SEMA3E**: [INFERENCE] SEMA3E augments PI3K–AKT signaling to guide neuronal migration, bridging intracellular signal amplification with system development and locomotion themes. [DATA]

## Overall Summary

The enrichment landscape is dominated by neuronal adhesion and excitatory synapse modules that couple postsynaptic scaffolding with receptor composition to drive synapse assembly, signaling, and plasticity. [INFERENCE]

Growth factor and guidance receptor pathways converge on MAPK and PI3K–AKT signaling to coordinate migration, projection morphogenesis, and junction assembly across tissues. [INFERENCE]

Cyclic nucleotide and phosphoinositide metabolism modules shape intracellular signal amplitude and timing, impacting EPSP modulation, cardiac relaxation, and immune signaling. [INFERENCE]

Adhesion regulators and phosphatases integrate mechanical stability with motility by tuning focal adhesion and adherens junction dynamics, thereby aligning tissue architecture with cell movement. [INFERENCE]

Hub genes such as PTEN, NLGN4X, PDGFRA, and PTPRJ connect multiple themes, acting as control points that synchronize adhesion, signaling, and structural remodeling across neuronal and mesenchymal contexts. [INFERENCE]

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

