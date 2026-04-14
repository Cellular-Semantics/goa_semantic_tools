# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_7_themes.csv](Cluster_7_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-regulation-of-anatomical-structure-morphogenesis) | [regulation of anatomical structure morphogenesis](#theme-1-regulation-of-anatomical-structure-morphogenesis) [GO:0022603](http://purl.obolibrary.org/obo/GO_0022603) | BP | 6.96e-07 | 27 | FDR<0.01 |
| [2](#theme-2-nervous-system-development) | [nervous system development](#theme-2-nervous-system-development) [GO:0007399](http://purl.obolibrary.org/obo/GO_0007399) | BP | 1.54e-05 | 23 | FDR<0.01 |
| [3](#theme-3-glutamatergic-synapse) | [glutamatergic synapse](#theme-3-glutamatergic-synapse) [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) | CC | 2.39e-05 | 21 | FDR<0.01 |
| [4](#theme-4-cytoskeleton) | [cytoskeleton](#theme-4-cytoskeleton) [GO:0005856](http://purl.obolibrary.org/obo/GO_0005856) | CC | 1.61e-04 | 27 | FDR<0.01 |
| [5](#theme-5-calcium-mediated-signaling) | [calcium-mediated signaling](#theme-5-calcium-mediated-signaling) [GO:0019722](http://purl.obolibrary.org/obo/GO_0019722) | BP | 7.30e-04 | 10 | FDR<0.01 |
| [6](#theme-6-plasma-membrane-region) | [plasma membrane region](#theme-6-plasma-membrane-region) [GO:0098590](http://purl.obolibrary.org/obo/GO_0098590) | CC | 8.04e-04 | 29 | FDR<0.01 |
| [7](#theme-7-cell-adhesion) | [cell adhesion](#theme-7-cell-adhesion) [GO:0007155](http://purl.obolibrary.org/obo/GO_0007155) | BP | 8.23e-04 | 24 | FDR<0.01 |
| [8](#theme-8-angiogenesis) | [angiogenesis](#theme-8-angiogenesis) [GO:0001525](http://purl.obolibrary.org/obo/GO_0001525) | BP | 2.16e-03 | 12 | FDR<0.01 |
| [9](#theme-9-cell-motility) | [cell motility](#theme-9-cell-motility) [GO:0048870](http://purl.obolibrary.org/obo/GO_0048870) | BP | 3.29e-03 | 39 | FDR<0.01 |
| [10](#theme-10-negative-regulation-of-lens-fiber-cell-differentiation) | [negative regulation of lens fiber cell differentiation](#theme-10-negative-regulation-of-lens-fiber-cell-differentiation) [GO:1902747](http://purl.obolibrary.org/obo/GO_1902747) | BP | 5.39e-03 | 3 | FDR<0.01 |
| [11](#theme-11-axon-guidance) | [axon guidance](#theme-11-axon-guidance) [GO:0007411](http://purl.obolibrary.org/obo/GO_0007411) | BP | 7.98e-03 | 9 | FDR<0.01 |
| [12](#theme-12-regulation-of-cell-projection-organization) | [regulation of cell projection organization](#theme-12-regulation-of-cell-projection-organization) [GO:0031344](http://purl.obolibrary.org/obo/GO_0031344) | BP | 8.42e-03 | 17 | FDR<0.01 |
| [13](#theme-13-protein-phosphorylation) | [protein phosphorylation](#theme-13-protein-phosphorylation) [GO:0006468](http://purl.obolibrary.org/obo/GO_0006468) | BP | 8.42e-03 | 12 | FDR<0.01 |
| [14](#theme-14-regulation-of-epithelial-to-mesenchymal-transition) | [regulation of epithelial to mesenchymal transition](#theme-14-regulation-of-epithelial-to-mesenchymal-transition) [GO:0010717](http://purl.obolibrary.org/obo/GO_0010717) | BP | 9.06e-03 | 7 | FDR<0.01 |
| [15](#theme-15-regulation-of-postsynapse-organization) | [regulation of postsynapse organization](#theme-15-regulation-of-postsynapse-organization) [GO:0099175](http://purl.obolibrary.org/obo/GO_0099175) | BP | 1.20e-02 | 8 | FDR<0.05 |
| [16](#theme-16-dendrite) | [dendrite](#theme-16-dendrite) [GO:0030425](http://purl.obolibrary.org/obo/GO_0030425) | CC | 1.22e-02 | 14 | FDR<0.05 |
| [17](#theme-17-regulation-of-cell-substrate-adhesion) | [regulation of cell-substrate adhesion](#theme-17-regulation-of-cell-substrate-adhesion) [GO:0010810](http://purl.obolibrary.org/obo/GO_0010810) | BP | 1.45e-02 | 9 | FDR<0.05 |
| [18](#theme-18-positive-regulation-of-developmental-process) | [positive regulation of developmental process](#theme-18-positive-regulation-of-developmental-process) [GO:0051094](http://purl.obolibrary.org/obo/GO_0051094) | BP | 1.45e-02 | 24 | FDR<0.05 |
| [19](#theme-19-laminin-trimer) | [laminin trimer](#theme-19-laminin-trimer) [GO:0043256](http://purl.obolibrary.org/obo/GO_0043256) | CC | 1.59e-02 | 3 | FDR<0.05 |
| [20](#theme-20-cell-cell-signaling) | [cell-cell signaling](#theme-20-cell-cell-signaling) [GO:0007267](http://purl.obolibrary.org/obo/GO_0007267) | BP | 1.64e-02 | 16 | FDR<0.05 |
| [21](#theme-21-regulation-of-neuronal-synaptic-plasticity) | [regulation of neuronal synaptic plasticity](#theme-21-regulation-of-neuronal-synaptic-plasticity) [GO:0048168](http://purl.obolibrary.org/obo/GO_0048168) | BP | 1.95e-02 | 5 | FDR<0.05 |
| [22](#theme-22-cell-cell-junction) | [cell-cell junction](#theme-22-cell-cell-junction) [GO:0005911](http://purl.obolibrary.org/obo/GO_0005911) | CC | 1.95e-02 | 14 | FDR<0.05 |
| [23](#theme-23-basement-membrane) | [basement membrane](#theme-23-basement-membrane) [GO:0005604](http://purl.obolibrary.org/obo/GO_0005604) | CC | 1.98e-02 | 6 | FDR<0.05 |
| [24](#theme-24-positive-regulation-of-cell-proliferation-in-bone-marrow) | [positive regulation of cell proliferation in bone marrow](#theme-24-positive-regulation-of-cell-proliferation-in-bone-marrow) [GO:0071864](http://purl.obolibrary.org/obo/GO_0071864) | BP | 2.04e-02 | 2 | FDR<0.05 |
| [25](#theme-25-ligand-gated-calcium-channel-activity) | [ligand-gated calcium channel activity](#theme-25-ligand-gated-calcium-channel-activity) [GO:0099604](http://purl.obolibrary.org/obo/GO_0099604) | MF | 2.12e-02 | 5 | FDR<0.05 |
| [26](#theme-26-cell-surface-receptor-protein-tyrosine-kinase-signaling-pathway) | [cell surface receptor protein tyrosine kinase signaling pathway](#theme-26-cell-surface-receptor-protein-tyrosine-kinase-signaling-pathway) [GO:0007169](http://purl.obolibrary.org/obo/GO_0007169) | BP | 3.45e-02 | 12 | FDR<0.05 |
| [27](#theme-27-protein-serine-kinase-activity) | [protein serine kinase activity](#theme-27-protein-serine-kinase-activity) [GO:0106310](http://purl.obolibrary.org/obo/GO_0106310) | MF | 3.59e-02 | 13 | FDR<0.05 |
| [28](#theme-28-ionotropic-glutamate-receptor-complex) | [ionotropic glutamate receptor complex](#theme-28-ionotropic-glutamate-receptor-complex) [GO:0008328](http://purl.obolibrary.org/obo/GO_0008328) | CC | 3.63e-02 | 4 | FDR<0.05 |
| [29](#theme-29-sarcoplasmic-reticulum-membrane) | [sarcoplasmic reticulum membrane](#theme-29-sarcoplasmic-reticulum-membrane) [GO:0033017](http://purl.obolibrary.org/obo/GO_0033017) | CC | 3.63e-02 | 4 | FDR<0.05 |
| [30](#theme-30-negative-regulation-of-small-gtpase-mediated-signal-transduction) | [negative regulation of small GTPase mediated signal transduction](#theme-30-negative-regulation-of-small-gtpase-mediated-signal-transduction) [GO:0051058](http://purl.obolibrary.org/obo/GO_0051058) | BP | 3.64e-02 | 5 | FDR<0.05 |

---

### Theme 1: regulation of anatomical structure morphogenesis

**Summary:** regulation of anatomical structure morphogenesis ([GO:0022603](http://purl.obolibrary.org/obo/GO_0022603))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Regulation of anatomical structure morphogenesis here reflects coordinated control of guidance cues, cytoskeletal remodeling, and matrix adhesion that sculpt tissue architectures during development.[INFERENCE] SEMA3E delivers repulsive guidance through neuropilin/plexin signaling that remodels actin and microtubules to redirect projections and migrating cells, coupling morphogenetic patterning to local cytoskeletal collapse.[DATA] RUNX1 acts transcriptionally to tune endothelial differentiation and motility programs that shape vascular morphogenesis, aligning with its curated role in developmental patterning [PMID:33894126](https://pubmed.ncbi.nlm.nih.gov/33894126/).[DATA] Angiogenic setpoints within this theme are bidirectionally tuned by protease and integrin pathways, where ADAM12 and ITGB8 promote sprouting while SPRY2 dampens receptor tyrosine kinase signaling to restrain endothelial proliferation and migration [PMID:28637396](https://pubmed.ncbi.nlm.nih.gov/28637396/), [PMID:25801897](https://pubmed.ncbi.nlm.nih.gov/25801897/), [PMID:24177325](https://pubmed.ncbi.nlm.nih.gov/24177325/).[DATA] Endothelial tip behaviors are further refined by RHOJ-dependent actin dynamics that set filopodial protrusion and branch selection, directly linking cytoskeletal control to vessel patterning [PMID:30158707](https://pubmed.ncbi.nlm.nih.gov/30158707/).[INFERENCE] Together these modules channel extracellular cues into cell-shape change and tissue morphogenesis by synchronizing guidance, adhesion, and RTK/MAPK outputs at growth cones and leading edges.

#### Key Insights

- Angiogenic morphogenesis in this set is balanced by positive (ADAM12, ITGB8, RHOJ) and negative (SPRY2) regulators that converge on endothelial cytoskeletal remodeling and sprout selection. ([GO:0045765](http://purl.obolibrary.org/obo/GO_0045765))
- Guidance-cue receptors such as SEMA3E drive localized growth cone collapse to redirect projections, providing a cell-shape based mechanism for tissue patterning. ([GO:0008360](http://purl.obolibrary.org/obo/GO_0008360))

#### Key Genes

- **SEMA3E**: [INFERENCE] Repulsive semaphorin signaling through plexins triggers localized actin collapse to reshape leading edges and growth cones, biasing morphogenetic trajectories. ([GO:0008360](http://purl.obolibrary.org/obo/GO_0008360))
- **RUNX1**: [INFERENCE] Transcriptional regulator that promotes endothelial differentiation and migration programs necessary for vessel patterning during morphogenesis. ([GO:0045765](http://purl.obolibrary.org/obo/GO_0045765))
- **GAS2**: [INFERENCE] Microtubule–actin crosslinker that stabilizes and remodels cytoskeleton to execute cell-shape changes underpinning morphogenesis. ([GO:0022603](http://purl.obolibrary.org/obo/GO_0022603))
- **DNMBP**: [INFERENCE] Rho-family GTPase regulator coordinating actin remodeling to steer dendrite and axon outgrowth during structural patterning. ([GO:0022603](http://purl.obolibrary.org/obo/GO_0022603))
- **ITGA7**: [INFERENCE] ECM-integrin adhesion that transduces matrix forces to cytoskeletal organization, supporting tissue integrity during morphogenesis. ([GO:0022603](http://purl.obolibrary.org/obo/GO_0022603))

#### Statistical Context

[GO:0022603](http://purl.obolibrary.org/obo/GO_0022603) enriched at FDR=6.96e-07 (4.4x) with 27/173 annotated input genes; child terms show regulation of angiogenesis (FDR=8.23e-04) and regulation of cell shape (FDR=2.59e-02).

---

### Theme 2: nervous system development

**Summary:** nervous system development ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Nervous system development in this set is driven by post-transcriptional control, guidance receptors, and cytoskeletal regulation that collectively establish neuronal identity, connectivity, and network architecture.[EXTERNAL] FGF14 modulates neuronal excitability and developmental programs within the FGF homologous factor family, aligning ion channel tuning with axon trajectory decisions [PMID:8790420](https://pubmed.ncbi.nlm.nih.gov/8790420/).[DATA] ENC1 supports neuronal differentiation programs linked to nuclear matrix interactions, connecting nuclear architecture to neurite formation and maturation [PMID:9566959](https://pubmed.ncbi.nlm.nih.gov/9566959/).[DATA] SEMA5A provides axon guidance information within developing brain regions, coupling extracellular semaphorin gradients to growth cone decision-making [PMID:9464278](https://pubmed.ncbi.nlm.nih.gov/9464278/).[DATA] DPYSL5 (CRMP5) participates in semaphorin-driven growth cone collapse and dendrite patterning, directly linking guidance cue decoding to microtubule reorganization [PMID:10851247](https://pubmed.ncbi.nlm.nih.gov/10851247/).[INFERENCE] IGF2BP2/3 likely stabilize and traffic mRNAs encoding growth and cytoskeletal regulators at growth cones to synchronize local translation with guidance and branching cues.

#### Key Insights

- Semaphorin–CRMP signaling converts extracellular gradients into cytoskeletal remodeling for pathfinding and dendritic patterning. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))
- FGF14 and RNA-binding IGF2BPs coordinate intrinsic excitability and local mRNA translation to time neuronal differentiation and projection growth. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))

#### Key Genes

- **IGF2BP3**: [INFERENCE] mRNA-binding regulator anticipated to stabilize transcripts for growth cone navigation and neuronal differentiation. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))
- **DPF3**: [INFERENCE] Chromatin-associated factor implicated in programs that shape neuronal differentiation and connectivity. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))
- **FGF14**: [INFERENCE] FHF that modulates neuronal excitability and development, aligning channel function with axon guidance programs. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))
- **IGF2BP2**: [INFERENCE] Post-transcriptional regulator coordinating local translation of cytoskeletal and guidance effectors during neural development. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))
- **LSAMP**: [INFERENCE] Axon-associated adhesion molecule promoting growth cone interactions that support tract formation. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))

#### Statistical Context

[GO:0007399](http://purl.obolibrary.org/obo/GO_0007399) enriched at FDR=1.54e-05 (4.3x) with 23/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 3: glutamatergic synapse

**Summary:** glutamatergic synapse ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The glutamatergic synapse theme captures scaffolding, receptor composition, and glutamate clearance mechanisms that set synaptic strength and plasticity at excitatory synapses.[DATA] Presynaptic and postsynaptic kainate receptor subunit diversity, including GRIK2, tunes synaptic facilitation and kinetics shaping short-term plasticity [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/), [PMID:21893069](https://pubmed.ncbi.nlm.nih.gov/21893069/).[DATA] Palmitoylated LIMK1 locally stabilizes F-actin in spines to support receptor anchoring and spine morphodynamics during LTP induction and maintenance [PMID:25884247](https://pubmed.ncbi.nlm.nih.gov/25884247/).[EXTERNAL] RhoGEFs such as TRIO position Rho-family signaling at postsynaptic sites to couple NMDAR/Ca2+ influx to structural remodeling required for potentiation [PMID:26858404](https://pubmed.ncbi.nlm.nih.gov/26858404/).[INFERENCE] Glutamate uptake by SLC1A2 and Ca2+-sensing CNKSR2/CPNE4-like adaptors modulate receptor occupancy and nanoscale receptor organization, constraining excitatory drive and plasticity thresholds.

#### Key Insights

- Actin remodeling via LIMK1 anchors AMPAR/KAR nanodomains, stabilizing potentiated states at glutamatergic synapses. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- Kainate receptor subunit composition (GRIK2) dictates presynaptic facilitation and short-term plasticity dynamics. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Key Genes

- **CPNE4**: [INFERENCE] Ca2+-responsive adaptor that can influence receptor positioning and vesicle dynamics to tune synaptic transmission. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **CNKSR2**: [INFERENCE] Scaffold coordinating small GTPase signaling at postsynaptic sites to couple receptor activity to structural plasticity. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **CSMD2**: [INFERENCE] Synaptic organizer implicated in shaping receptor assemblies and spine structure to modulate excitatory throughput. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **PCDH7**: [INFERENCE] Adhesion molecule facilitating synapse formation and receptor clustering to strengthen excitatory synapses. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **SLC1A2**: [INFERENCE] EAAT2 transporter clearing glutamate to prevent excitotoxicity and set synaptic gain control. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Statistical Context

[GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) enriched at FDR=2.39e-05 (4.2x) with 21/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 4: cytoskeleton

**Summary:** cytoskeleton ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The cytoskeleton theme integrates actin, microtubule, and membrane–cytoskeleton coupling systems that drive cell shape, polarity, and motility.[DATA] DENND2A activates specific Rab GTPases to position actin remodeling at trafficking hotspots, linking vesicle flow to protrusion dynamics [PMID:20937701](https://pubmed.ncbi.nlm.nih.gov/20937701/).[DATA] Cortical actin and adherens junction stability are supported by CDH2-associated complexes within flotillin microdomains, coupling cadherin ligation to actin organization [PMID:24046456](https://pubmed.ncbi.nlm.nih.gov/24046456/).[DATA] DLC1 scaffolds RhoGAP activity with EF1A1 to temper RhoA-dependent stress fibers at the cortex, tuning migration and junctional integrity [PMID:19158340](https://pubmed.ncbi.nlm.nih.gov/19158340/).[INFERENCE] Microtubule-stabilizing elements such as EML4 and actin regulators including IQGAP2 coordinate with TRIM9-mediated ubiquitin signaling to align protrusive and adhesive cycles necessary for polarized movement.

#### Key Insights

- Site-specific Rab activation by DENND2A couples membrane traffic to actin assembly at leading edges. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- Cadherin–cortical actin coupling via flotillin microdomains stabilizes junctions while permitting controlled remodeling. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))

#### Key Genes

- **EML4**: [INFERENCE] Microtubule-associated factor organizing non-centrosomal arrays to support polarized architecture. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **DENND2A**: [INFERENCE] Rab GEF that positions actin remodeling through endomembrane trafficking control. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **TRIM9**: [INFERENCE] E3 ligase modulating cytoskeletal effectors to coordinate protrusion and synaptic morphogenesis. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **IQGAP2**: [INFERENCE] Scaffold linking actin filaments to signaling modules to tune cell shape and motility. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))

#### Statistical Context

[GO:0005856](http://purl.obolibrary.org/obo/GO_0005856) enriched at FDR=1.61e-04 (2.9x) with 27/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 5: calcium-mediated signaling

**Summary:** calcium-mediated signaling ([GO:0019722](http://purl.obolibrary.org/obo/GO_0019722))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Calcium-mediated signaling unifies membrane-gated Ca2+ entry with store release and Ca2+/calmodulin decoding to control excitability and contraction.[DATA] The Na+/Ca2+ exchanger SLC8A1 sets cytosolic Ca2+ by electrogenic exchange, directly tuning sarcoplasmic release and cardiac contractility [PMID:23608603](https://pubmed.ncbi.nlm.nih.gov/23608603/), [PMID:23224879](https://pubmed.ncbi.nlm.nih.gov/23224879/).[DATA] CAMK2D phosphorylates Ca2+ handling proteins to potentiate Ca2+-induced Ca2+ release and reshape excitation–contraction coupling dynamics [PMID:17157285](https://pubmed.ncbi.nlm.nih.gov/17157285/), [PMID:12676813](https://pubmed.ncbi.nlm.nih.gov/12676813/).[DATA] Muscarinic receptor CHRM3 engages Ca2+-dependent epithelial transport responses, illustrating GPCR-to-Ca2+ crosstalk [PMID:17478539](https://pubmed.ncbi.nlm.nih.gov/17478539/).[INFERENCE] Parallel glutamatergic receptor subunits (GRIA3, GRIK2, GRIN2B), ryanodine release (RYR3), and IP3-driven ER release (ITPR2) integrate to produce spatial Ca2+ microdomains that drive kinase signaling and gene expression.

#### Key Insights

- SLC8A1 and CAMK2D form a feedback axis where Ca2+ extrusion and phosphorylation of release machinery co-set contraction strength. ([GO:0019722](http://purl.obolibrary.org/obo/GO_0019722))
- Dual-store release via IP3R2 and RyR3 integrates with ionotropic glutamate receptor Ca2+ entry to shape signaling microdomains. ([GO:0019722](http://purl.obolibrary.org/obo/GO_0019722))

#### Key Genes

- **RCAN1**: [INFERENCE] Calcineurin inhibitor that restrains NFAT dephosphorylation to tune Ca2+-dependent transcriptional outputs. ([GO:0019722](http://purl.obolibrary.org/obo/GO_0019722))
- **ITPR2**: [INFERENCE] IP3-gated ER Ca2+ channel generating cytosolic transients that couple receptors to downstream kinases. ([GO:0019722](http://purl.obolibrary.org/obo/GO_0019722))
- **RYR3**: [INFERENCE] RyR family channel amplifying Ca2+-induced Ca2+ release to support excitability and contraction. ([GO:0019722](http://purl.obolibrary.org/obo/GO_0019722))
- **SLC8A1**: [INFERENCE] Electrogenic Na+/Ca2+ exchanger controlling Ca2+ clearance and thereby CaMK activation windows. ([GO:0019722](http://purl.obolibrary.org/obo/GO_0019722))

#### Statistical Context

[GO:0019722](http://purl.obolibrary.org/obo/GO_0019722) enriched at FDR=7.30e-04 (7.6x) with 10/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 6: plasma membrane region

**Summary:** plasma membrane region ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The plasma membrane region theme highlights specialized subdomains that coordinate endocytosis, signaling receptor nanodomains, and synaptic organization.[DATA] Ruffle membranes assemble negative regulators of protrusion including KANK1 to suppress Rac1/IRSp53-driven lamellipodia, constraining motility-associated endocytosis [PMID:19559006](https://pubmed.ncbi.nlm.nih.gov/19559006/).[DATA] Postsynaptic density membranes concentrate ionotropic glutamate receptors such as GRIN2B to potentiate synaptic signaling and plasticity [PMID:24607229](https://pubmed.ncbi.nlm.nih.gov/24607229/).[DATA] Presynaptic and perisynaptic glutamate transport by SLC1A2 sculpts neurotransmitter transients and protects against excitotoxicity [PMID:21258616](https://pubmed.ncbi.nlm.nih.gov/21258616/).[DATA] Membrane transporter localization such as ABCC3 at basal or basolateral faces demonstrates polarized trafficking central to barrier and signaling functions [PMID:35307651](https://pubmed.ncbi.nlm.nih.gov/35307651/), [PMID:28408210](https://pubmed.ncbi.nlm.nih.gov/28408210/).

#### Key Insights

- Ruffle membrane assemblies serve as control points where KANK1 restrains Rac-driven protrusion and macropinocytosis. ([GO:0032587](http://purl.obolibrary.org/obo/GO_0032587))
- Postsynaptic density membranes organize glutamate receptors and adaptors to stabilize transmission hot spots. ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))

#### Key Genes

- **CSMD2**: [INFERENCE] Synaptic organizer influencing postsynaptic receptor clustering within PSD membranes. ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **GPR158**: [INFERENCE] GPCR-like modulator that tunes receptor trafficking and signaling at the cell surface. ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))
- **SYNJ2**: [INFERENCE] Phosphoinositide phosphatase driving endocytic membrane turnover at ruffles and synapses. ([GO:0032587](http://purl.obolibrary.org/obo/GO_0032587))
- **SNTG1**: [INFERENCE] Dystrophin-complex adaptor stabilizing membrane microdomains at synapses and junctions. ([GO:0098590](http://purl.obolibrary.org/obo/GO_0098590))

#### Statistical Context

[GO:0098590](http://purl.obolibrary.org/obo/GO_0098590) enriched at FDR=8.04e-04 (2.5x) with 29/173 annotated input genes; specific terms ruffle membrane FDR=4.28e-03 and postsynaptic density membrane FDR=1.01e-02.

---

### Theme 7: cell adhesion

**Summary:** cell adhesion ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Cell adhesion here spans cadherin-mediated cell–cell contacts, integrin–ECM anchorage, and synaptic adhesion complexes that collectively stabilize tissue architecture and guide migration.[DATA] N-cadherin (CDH2) mediates Ca2+-dependent homophilic adhesion and recruits catenins to reinforce adherens junctions essential for morphogenesis [PMID:31585109](https://pubmed.ncbi.nlm.nih.gov/31585109/).[DATA] ADGRL3 forms trans-synaptic bridges with FLRTs and UNC5 to coordinate cortical cell adhesion and synapse formation [PMID:26235030](https://pubmed.ncbi.nlm.nih.gov/26235030/).[DATA] Integrins such as ITGA3 orchestrate cell–matrix adhesion and signaling across diverse ECM ligands, coupling traction to signaling outputs [PMID:19693543](https://pubmed.ncbi.nlm.nih.gov/19693543/).[DATA] FREM2 supports tissue cohesion, and its disruption underscores adhesion-dependent developmental anomalies [PMID:29688405](https://pubmed.ncbi.nlm.nih.gov/29688405/).[INFERENCE] Adhesion molecules like LSAMP and PCDH7 further refine neuronal pathfinding by tuning growth cone–substrate interactions in developing circuits.

#### Key Insights

- Cadherin–catenin complexes and integrins cooperate to integrate cell–cell and cell–ECM forces for cohesive migration. ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))
- Latrophilin–FLRT–UNC5 assemblies specify synaptic and migratory adhesion codes in the cortex. ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))

#### Key Genes

- **VMP1**: [INFERENCE] Organizer of epithelial junctional complexes that strengthens barrier-forming adhesions. ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))
- **FREM2**: [INFERENCE] Extracellular scaffold supporting intercellular cohesion during tissue morphogenesis. ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))
- **PCDH7**: [INFERENCE] Ca2+-dependent adhesion molecule stabilizing contacts that guide neurite–neurite interactions. ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))
- **SRPX**: [INFERENCE] Secreted adhesion modulator implicated in synaptogenesis and neuronal migration. ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))
- **LSAMP**: [INFERENCE] Axon-associated adhesion factor promoting tract-specific cell–cell interactions. ([GO:0007155](http://purl.obolibrary.org/obo/GO_0007155))

#### Statistical Context

[GO:0007155](http://purl.obolibrary.org/obo/GO_0007155) enriched at FDR=8.23e-04 (3.1x) with 24/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 8: angiogenesis

**Summary:** angiogenesis ([GO:0001525](http://purl.obolibrary.org/obo/GO_0001525))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Angiogenesis is encoded here by endothelial guidance, adhesion to basement membrane, and growth factor–Notch crosstalk that pattern sprouts and stabilize nascent vessels.[DATA] Secretoneurin (SCG2) directly promotes endothelial migration and tube formation, acting as an angiogenic cytokine in vitro and in vivo [PMID:14970115](https://pubmed.ncbi.nlm.nih.gov/14970115/).[DATA] Endothelial programs induce NrCAM during tubulogenesis, linking adhesion cues to lumen formation [PMID:11866539](https://pubmed.ncbi.nlm.nih.gov/11866539/).[DATA] Notch ligand JAG1 modulates endothelial responsiveness to pro-angiogenic stimuli, tuning sprout initiation and maturation [PMID:8955070](https://pubmed.ncbi.nlm.nih.gov/8955070/).[INFERENCE] RHOJ-driven actin remodeling and semaphorin signals (SEMA3E) interface with PDGFA and PTPRJ pathways to balance tip cell protrusion with adhesion stabilization during sprouting.

#### Key Insights

- Neuropeptide-driven angiogenesis via SCG2 couples chemokinetic drive to tube morphogenesis. ([GO:0001525](http://purl.obolibrary.org/obo/GO_0001525))
- Notch–growth factor crosstalk through JAG1 tunes tip/stalk fate and stabilizes emerging vessels. ([GO:0001525](http://purl.obolibrary.org/obo/GO_0001525))

#### Key Genes

- **SCG2**: [INFERENCE] Secretoneurin drives endothelial migration and tube formation as a direct angiogenic cytokine. ([GO:0001525](http://purl.obolibrary.org/obo/GO_0001525))
- **MEIS1**: [INFERENCE] Transcriptional regulator proposed to enhance endothelial proliferation and migration in hypoxic cues. ([GO:0001525](http://purl.obolibrary.org/obo/GO_0001525))
- **RHOJ**: [INFERENCE] Endothelial Rho GTPase controlling actin dynamics for sprouting and branching behaviors. ([GO:0001525](http://purl.obolibrary.org/obo/GO_0001525))
- **TNFRSF12A**: [INFERENCE] Receptor linking neuropeptidergic signals to endothelial motility during angiogenesis. ([GO:0001525](http://purl.obolibrary.org/obo/GO_0001525))

#### Statistical Context

[GO:0001525](http://purl.obolibrary.org/obo/GO_0001525) enriched at FDR=2.16e-03 (5.1x) with 12/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 9: cell motility

**Summary:** cell motility ([GO:0048870](http://purl.obolibrary.org/obo/GO_0048870))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Cell motility emerges from integrated guidance, adhesion turnover, and cytoskeletal force production that drive persistent migration and pathfinding.[DATA] CAMK2B variants perturb neuron migration, underscoring Ca2+-dependent phosphorylation control over actin/spine dynamics during movement [PMID:29100089](https://pubmed.ncbi.nlm.nih.gov/29100089/).[EXTERNAL] SEMA3E controls GnRH neuronal migration by repulsive signaling via plexin/neuropilin receptors that collapse growth cones and redirect trajectories [PMID:25985275](https://pubmed.ncbi.nlm.nih.gov/25985275/).[DATA] Endothelial motility and sprouting are tuned by RHOJ signaling, integrating microRNA-mediated feedback in vascular contexts [PMID:30158707](https://pubmed.ncbi.nlm.nih.gov/30158707/), [PMID:28727754](https://pubmed.ncbi.nlm.nih.gov/28727754/).[INFERENCE] ECM laminins (LAMC1) and RTKs (FGFR1) provide traction and chemotactic gradients, while KANK1 restrains lamellipodia to bias directed migration.

#### Key Insights

- Semaphorin-driven growth cone collapse redirects migrating neurons, coupling cue sensing to cytoskeletal retraction. ([GO:0048870](http://purl.obolibrary.org/obo/GO_0048870))
- RHOJ-dependent actin remodeling and ECM laminin–integrin engagement co-set speed and directionality of motility. ([GO:0048870](http://purl.obolibrary.org/obo/GO_0048870))

#### Key Genes

- **LAMC1**: [INFERENCE] Basement membrane laminin subunit providing integrin ligands that set traction and polarity cues. ([GO:0048870](http://purl.obolibrary.org/obo/GO_0048870))
- **SEMA3A**: [INFERENCE] Repulsive cue activating Rho-family pathways to collapse protrusions and redirect movement. ([GO:0048870](http://purl.obolibrary.org/obo/GO_0048870))
- **FGFR1**: [INFERENCE] RTK that integrates growth factor gradients to modulate adhesion turnover and cytoskeletal dynamics. ([GO:0048870](http://purl.obolibrary.org/obo/GO_0048870))
- **KANK1**: [INFERENCE] Suppresses Rac-dependent lamellipodia to refine protrusion–retraction cycles during migration. ([GO:0048870](http://purl.obolibrary.org/obo/GO_0048870))

#### Statistical Context

[GO:0048870](http://purl.obolibrary.org/obo/GO_0048870) enriched at FDR=3.29e-03 (2.8x) with 23/173 annotated input genes; specific terms include cell migration FDR=4.91e-04 and regulation of cell migration FDR=6.89e-04.

---

### Theme 10: negative regulation of lens fiber cell differentiation

**Summary:** negative regulation of lens fiber cell differentiation ([GO:1902747](http://purl.obolibrary.org/obo/GO_1902747))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Negative regulation of lens fiber cell differentiation reflects MAPK/ERK pathway attenuation to time terminal differentiation and maintain lens transparency.[INFERENCE] SPRED2 and SPRED1 inhibit Ras–Raf signaling to restrain ERK activity, delaying fiber differentiation until proper morphogenetic cues are met.[DATA] SPRY2 similarly antagonizes RTK–RAS–MAPK cascades, curbing proliferative and migratory responses that would otherwise accelerate differentiation programs [PMID:24177325](https://pubmed.ncbi.nlm.nih.gov/24177325/).[INFERENCE] Coordinated suppression of MAPK outputs ensures ordered fiber cell elongation and denucleation without premature commitment.

#### Key Insights

- SPRED–SPRY antagonism of RTK–RAS–ERK signaling times lens fiber differentiation to preserve optical clarity. ([GO:1902747](http://purl.obolibrary.org/obo/GO_1902747))

#### Key Genes

- **SPRED2**: [INFERENCE] Ras/MAPK pathway inhibitor that delays fiber cell differentiation by limiting ERK activation. ([GO:1902747](http://purl.obolibrary.org/obo/GO_1902747))
- **SPRED1**: [INFERENCE] MAPK antagonist cooperating with SPRED2 to restrain premature differentiation. ([GO:1902747](http://purl.obolibrary.org/obo/GO_1902747))
- **SPRY2**: [INFERENCE] Sprouty protein dampening RTK signaling to prevent untimely fiber maturation. ([GO:1902747](http://purl.obolibrary.org/obo/GO_1902747))

#### Statistical Context

[GO:1902747](http://purl.obolibrary.org/obo/GO_1902747) enriched at FDR=5.39e-03 (56.9x) with 3/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 11: axon guidance

**Summary:** axon guidance ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Axon guidance is implemented by extracellular cues decoded into growth cone cytoskeletal remodeling, steering axons to their targets.[DATA] SEMA3A signals via neuropilins to trigger CRMP-dependent growth cone collapse, creating repulsive zones that redirect axons [PMID:19909241](https://pubmed.ncbi.nlm.nih.gov/19909241/).[DATA] DPYSL5 (CRMP5) links semaphorin signaling to microtubule regulation, integrating cue detection with cytoskeletal outputs [PMID:10851247](https://pubmed.ncbi.nlm.nih.gov/10851247/).[INFERENCE] TRIO and KALRN activate Rho-family GTPases to couple receptor activation to lamellipodial and filopodial dynamics, while EPHA3 and NRCAM modulate adhesion polarity along the path.[INFERENCE] SEMA3E and SEMA5A diversify spatial codes, combining repulsion and context-dependent attraction to sculpt tract topography.

#### Key Insights

- Neuropilin–semaphorin signaling uses CRMP effectors to convert repulsive gradients into microtubule destabilization and path correction. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))
- GEF-mediated activation of Rac/Rho by TRIO/KALRN translates guidance receptor engagement into protrusive asymmetry. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))

#### Key Genes

- **TRIO**: [INFERENCE] RhoGEF coupling guidance receptors to Rac/Rho activation for growth cone turning. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))
- **SEMA3A**: [INFERENCE] Repulsive cue via neuropilin–plexin that collapses growth cones to steer axons. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))
- **DPYSL5**: [INFERENCE] CRMP family member transmitting semaphorin signals to microtubule regulation. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))
- **KALRN**: [INFERENCE] RhoGEF shaping actin dynamics for axon pathfinding decisions. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))

#### Statistical Context

[GO:0007411](http://purl.obolibrary.org/obo/GO_0007411) enriched at FDR=7.98e-03 (6.0x) with 9/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 12: regulation of cell projection organization

**Summary:** regulation of cell projection organization ([GO:0031344](http://purl.obolibrary.org/obo/GO_0031344))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Regulation of cell projection organization integrates positive and negative control of neurites, cilia, and lamellipodia to shape cellular protrusions.[DATA] SEMA3A executes negative regulation of neuron projection development via macropinocytosis-coupled growth cone collapse, reducing surface area to retract processes [PMID:21593320](https://pubmed.ncbi.nlm.nih.gov/21593320/).[DATA] KANK1 suppresses lamellipodium and ruffle morphogenesis by disrupting IRSp53–Rac1 coupling, directly limiting protrusive structures [PMID:19171758](https://pubmed.ncbi.nlm.nih.gov/19171758/).[DATA] PRKD1 promotes neuron projection development by supporting Golgi-derived trafficking essential for arbor maintenance [PMID:19211839](https://pubmed.ncbi.nlm.nih.gov/19211839/).[DATA] LPAR1 negatively regulates cilium assembly through a Rab11–Rabin8 switch, illustrating GPCR control over projection biogenesis [PMID:31204173](https://pubmed.ncbi.nlm.nih.gov/31204173/).

#### Key Insights

- Protrusion pruning by SEMA3A and KANK1 counterbalances PRKD1-dependent outgrowth to refine neurite architecture. ([GO:0031344](http://purl.obolibrary.org/obo/GO_0031344))
- LPAR1-driven inhibition of ciliogenesis exemplifies GPCR gating of projection assembly pathways. ([GO:0031345](http://purl.obolibrary.org/obo/GO_0031345))

#### Key Genes

- **PRAG1**: [INFERENCE] Scaffold that interfaces with cytoskeletal regulators to tune neurite structure and guidance responses. ([GO:0031344](http://purl.obolibrary.org/obo/GO_0031344))
- **SEMA3A**: [INFERENCE] Repulsive cue enacting growth cone collapse to downscale projection area. ([GO:0031345](http://purl.obolibrary.org/obo/GO_0031345))
- **DPYSL5**: [INFERENCE] CRMP effector coordinating microtubule dynamics during projection patterning. ([GO:0010975](http://purl.obolibrary.org/obo/GO_0010975))
- **LPAR1**: [INFERENCE] LPA receptor that inhibits ciliogenesis through Rab11–Rabin8 trafficking control. ([GO:0031345](http://purl.obolibrary.org/obo/GO_0031345))
- **KANK1**: [INFERENCE] Actin regulator preventing lamellipodium and ruffle formation to restrain projection expansion. ([GO:0010975](http://purl.obolibrary.org/obo/GO_0010975))

#### Statistical Context

[GO:0031344](http://purl.obolibrary.org/obo/GO_0031344) enriched at FDR=8.42e-03 (3.2x) with 17/173 annotated input genes; specific terms include regulation of neuron projection development FDR=2.16e-03 and negative regulation of cell projection organization FDR=1.84e-02.

---

### Theme 13: protein phosphorylation

**Summary:** protein phosphorylation ([GO:0006468](http://purl.obolibrary.org/obo/GO_0006468))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Protein phosphorylation in this set captures RTKs and downstream serine/threonine kinases that encode extracellular cues into cytoskeletal and transcriptional responses.[DATA] ALK undergoes ligand-triggered peptidyl-tyrosine autophosphorylation to initiate neural developmental signaling cascades [PMID:34646012](https://pubmed.ncbi.nlm.nih.gov/34646012/), [PMID:30061385](https://pubmed.ncbi.nlm.nih.gov/30061385/).[DATA] LIMK1 phosphorylation programs actin dynamics downstream of GPCR/β-arrestin pathways to sculpt cell shape [PMID:23633677](https://pubmed.ncbi.nlm.nih.gov/23633677/).[DATA] PRKD1 autophosphorylation and activity integrate VEGF signals in endothelial cells, coordinating permeability and migration behaviors [PMID:24623306](https://pubmed.ncbi.nlm.nih.gov/24623306/).[INFERENCE] MAP3K1 and NEK6 extend this axis to stress and mitotic control, funneling upstream inputs to cytoskeletal and division machinery to align growth with morphogenetic needs.

#### Key Insights

- Ligand-triggered ALK autophosphorylation seeds RTK cascades that converge on cytoskeleton-remodeling kinases like LIMK1 and PRKD1. ([GO:0006468](http://purl.obolibrary.org/obo/GO_0006468))
- Mitotic and stress-responsive kinases (NEK6, MAP3K1) link cell cycle state to morphogenetic signaling throughput. ([GO:0006468](http://purl.obolibrary.org/obo/GO_0006468))

#### Key Genes

- **NEK6**: [INFERENCE] Mitotic kinase phosphorylating microtubule regulators to ensure accurate division. ([GO:0006468](http://purl.obolibrary.org/obo/GO_0006468))
- **STK17A**: [INFERENCE] Death-associated kinase modulating stress and apoptotic signaling via serine phosphorylation. ([GO:0006468](http://purl.obolibrary.org/obo/GO_0006468))
- **ALK**: [INFERENCE] Receptor tyrosine kinase that autophosphorylates to propagate developmental signals. ([GO:0006468](http://purl.obolibrary.org/obo/GO_0006468))
- **MAP3K1**: [INFERENCE] MAP3K integrating surface cues to ERK/JNK cascades for differentiation and migration control. ([GO:0006468](http://purl.obolibrary.org/obo/GO_0006468))

#### Statistical Context

[GO:0006468](http://purl.obolibrary.org/obo/GO_0006468) enriched at FDR=8.42e-03 (4.3x) with 12/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 14: regulation of epithelial to mesenchymal transition

**Summary:** regulation of epithelial to mesenchymal transition ([GO:0010717](http://purl.obolibrary.org/obo/GO_0010717))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Regulation of epithelial to mesenchymal transition (EMT) reflects transcriptional and Hippo-pathway control over adhesion loss and migratory gain.[DATA] LEF1 positively regulates EMT downstream of collagen I via ILK–NF-κB signaling, activating gene programs that enable motility and invasion [PMID:20018240](https://pubmed.ncbi.nlm.nih.gov/20018240/).[DATA] WWTR1/TAZ promotes EMT when Hippo restraint is relieved, coactivating transcription that downscales junctional adhesion and upscales mesenchymal traits [PMID:18227151](https://pubmed.ncbi.nlm.nih.gov/18227151/).[INFERENCE] SPRED1/2 and SPRY2 restrain RTK–MAPK drive, providing a brake that can oppose EMT onset depending on context, while EPHA3 modulates adhesion polarity to bias collective movement.

#### Key Insights

- ECM-triggered LEF1 and Hippo effector TAZ jointly activate EMT transcriptional programs. ([GO:0010717](http://purl.obolibrary.org/obo/GO_0010717))
- RTK pathway antagonists (SPRED/SPRY) buffer EMT initiation by damping MAPK amplification loops. ([GO:0010717](http://purl.obolibrary.org/obo/GO_0010717))

#### Key Genes

- **WWTR1**: [INFERENCE] Hippo-pathway coactivator driving EMT gene expression when dephosphorylated and nuclear. ([GO:0010717](http://purl.obolibrary.org/obo/GO_0010717))
- **SPRED2**: [INFERENCE] RAS–ERK pathway inhibitor that can oppose EMT-promoting signaling flux. ([GO:0010717](http://purl.obolibrary.org/obo/GO_0010717))
- **LEF1**: [INFERENCE] Wnt/β-catenin transcription factor inducing EMT downstream of collagen–ILK–NF-κB inputs. ([GO:0010717](http://purl.obolibrary.org/obo/GO_0010717))

#### Statistical Context

[GO:0010717](http://purl.obolibrary.org/obo/GO_0010717) enriched at FDR=9.06e-03 (8.1x) with 7/173 annotated input genes; theme confidence FDR<0.01.

---

### Theme 15: regulation of postsynapse organization

**Summary:** regulation of postsynapse organization ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of postsynapse organization links scaffolds and kinases to receptor clustering and spine stabilization that set synaptic efficacy.[INFERENCE] TANC1 coordinates postsynaptic scaffolds to assemble receptor–signaling complexes, stabilizing receptor nanoclusters and PSD architecture.[INFERENCE] SIPA1L1 modulates small GTPase activity to shape spine morphology and maintain postsynaptic compartmentalization.[DATA] N-cadherin (CDH2) strengthens synaptic adhesion, aligning cytoskeleton with receptor fields to preserve synaptic strength [PMID:31585109](https://pubmed.ncbi.nlm.nih.gov/31585109/).[INFERENCE] FGFR1 and GRIN2B signaling tune postsynaptic organization by coupling activity-dependent phosphorylation to receptor trafficking and retention.

#### Key Insights

- Scaffold-driven assembly (TANC1) and cadherin adhesion align receptors with actin to stabilize synapses. ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- Activity-dependent kinase signaling refines receptor trafficking and PSD composition to adjust synaptic strength. ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))

#### Key Genes

- **TANC1**: [INFERENCE] Postsynaptic scaffold coordinating receptor–cytoskeleton assemblies for stable transmission. ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- **IL1RAP**: [INFERENCE] Coreceptor potentially stabilizing cytokine-modulated postsynaptic signaling complexes. ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- **SIPA1L1**: [INFERENCE] RapGAP family regulator shaping spine morphology and postsynaptic organization. ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))

#### Statistical Context

[GO:0099175](http://purl.obolibrary.org/obo/GO_0099175) enriched at FDR=1.20e-02 (6.5x) with 8/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 16: dendrite

**Summary:** dendrite ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] The dendrite theme encompasses ion channel modulators, guidance receptors, and ubiquitin signaling that pattern branching and excitability of dendritic arbors.[INFERENCE] KCNIP1 tunes A-type K+ currents to set dendritic excitability and backpropagation limits that guide plasticity thresholds.[INFERENCE] CHL1-mediated adhesion and EPHA3 signaling shape dendritic filopodia stabilization and pruning to refine input maps.[DATA] TRIM9 acts as a brain-specific E3 ligase expressed in dendrites, suggesting a ubiquitin-based program for dendritic morphogenesis and maintenance [PMID:20085810](https://pubmed.ncbi.nlm.nih.gov/20085810/).[INFERENCE] Lipid transport by OSBP2 and growth-associated protein GAP43 contribute to membrane supply and actin regulation required for branch elaboration.

#### Key Insights

- Voltage-gated K+ current modulation by KCNIP1 constrains dendritic excitability and integration. ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425))
- Adhesion and guidance receptor signaling stabilize or prune dendritic branches to refine connectivity. ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425))

#### Key Genes

- **KCNIP1**: [INFERENCE] KChIP subunit regulating Kv4-mediated A-type currents that set dendritic integration windows. ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425))
- **SAMD4A**: [INFERENCE] RNA-binding regulator proposed to influence microtubule dynamics during dendrite development. ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425))
- **OSBP2**: [INFERENCE] Lipid transporter supporting membrane composition and supply for dendritic growth. ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425))
- **TRIM9**: [INFERENCE] E3 ligase localized to dendrites supporting morphogenesis and synaptic function. ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425))

#### Statistical Context

[GO:0030425](http://purl.obolibrary.org/obo/GO_0030425) enriched at FDR=1.22e-02 (3.2x) with 14/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 17: regulation of cell-substrate adhesion

**Summary:** regulation of cell-substrate adhesion ([GO:0010810](http://purl.obolibrary.org/obo/GO_0010810))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of cell-substrate adhesion captures focal adhesion assembly and negative feedback that calibrate traction and migration on ECM.[DATA] DLC1 suppresses focal adhesion assembly via RhoGAP activity and EF1A1 interaction, reducing stress fibers and motility to tune adhesion turnover [PMID:19158340](https://pubmed.ncbi.nlm.nih.gov/19158340/).[DATA] PTPRJ promotes focal adhesion assembly, enhancing integrin signaling and traction maturation critical for directional movement [PMID:21091576](https://pubmed.ncbi.nlm.nih.gov/21091576/).[DATA] KANK1 diminishes substrate adhesion-dependent spreading by uncoupling IRSp53–Rac1, restraining lamellipodia and adhesion growth [PMID:19171758](https://pubmed.ncbi.nlm.nih.gov/19171758/).[INFERENCE] Notch ligand JAG1 and semaphorin SEMA3E interface with RTK/plexin pathways to reset integrin signaling thresholds during migration and tissue remodeling.

#### Key Insights

- Balanced RhoGAP (DLC1) and phosphatase (PTPRJ) activities set adhesion assembly–disassembly cycles for efficient migration. ([GO:0010810](http://purl.obolibrary.org/obo/GO_0010810))
- KANK1-mediated suppression of Rac-driven spreading prevents excessive adhesion growth, sustaining plastic motility. ([GO:0010812](http://purl.obolibrary.org/obo/GO_0010812))

#### Key Genes

- **DLC1**: [INFERENCE] RhoGAP that curbs stress fibers and focal adhesion maturation to limit substrate adhesion. ([GO:0010812](http://purl.obolibrary.org/obo/GO_0010812))
- **SEMA3E**: [INFERENCE] Guidance cue modulating integrin signaling to reset adhesion during directional movement. ([GO:0001952](http://purl.obolibrary.org/obo/GO_0001952))
- **JAG1**: [INFERENCE] Notch ligand influencing endothelial and stromal adhesion programs during remodeling. ([GO:0001952](http://purl.obolibrary.org/obo/GO_0001952))
- **PTPRJ**: [INFERENCE] Phosphatase that enhances focal adhesion assembly and integrin signaling strength. ([GO:0001952](http://purl.obolibrary.org/obo/GO_0001952))

#### Statistical Context

[GO:0010810](http://purl.obolibrary.org/obo/GO_0010810) enriched at FDR=1.45e-02 (5.4x) with 9/173 annotated input genes; includes regulation of cell-matrix adhesion FDR=1.96e-02 and negative regulation of cell-substrate adhesion FDR=3.45e-02.

---

### Theme 18: positive regulation of developmental process

**Summary:** positive regulation of developmental process ([GO:0051094](http://purl.obolibrary.org/obo/GO_0051094))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Positive regulation of developmental process aggregates ECM, growth factor, and transcriptional programs that accelerate lineage progression and tissue growth.[DATA] Laminin subunits LAMA2 and LAMC1 support muscle cell differentiation, showing ECM–integrin signals that promote myogenic maturation [PMID:26555376](https://pubmed.ncbi.nlm.nih.gov/26555376/).[DATA] WWTR1/TAZ activity promotes osteoblast differentiation, tying mechanotransduction to lineage specification via YAP/TAZ control [PMID:29496737](https://pubmed.ncbi.nlm.nih.gov/29496737/).[DATA] Vascular remodeling inputs include ADAM12 and ITGB8 that enhance angiogenic stabilization during development [PMID:28637396](https://pubmed.ncbi.nlm.nih.gov/28637396/), [PMID:25801897](https://pubmed.ncbi.nlm.nih.gov/25801897/).[INFERENCE] FBN2, RNF157, DPF3, RUNX1, and CPNE8 likely converge on ECM–chromatin–signaling axes to accelerate differentiation in muscle and mesenchymal contexts.

#### Key Insights

- Basement membrane laminins and YAP/TAZ mechanotransduction co-drive myogenic and osteogenic differentiation. ([GO:0051094](http://purl.obolibrary.org/obo/GO_0051094))
- Pro-angiogenic protease/integrin modules facilitate developmental tissue vascularization and maturation. ([GO:0051094](http://purl.obolibrary.org/obo/GO_0051094))

#### Key Genes

- **RNF157**: [INFERENCE] Putative regulator of myogenic differentiation interfacing with ECM-driven satellite cell programs. ([GO:0051094](http://purl.obolibrary.org/obo/GO_0051094))
- **FBN2**: [INFERENCE] ECM organizer promoting myoblast differentiation and stem cell niche cues for regeneration. ([GO:0051094](http://purl.obolibrary.org/obo/GO_0051094))
- **RUNX1**: [INFERENCE] Transcription factor advancing lineage programs across hematopoietic and mesenchymal compartments. ([GO:0051094](http://purl.obolibrary.org/obo/GO_0051094))
- **DPF3**: [INFERENCE] Chromatin remodeler facilitating differentiation gene expression in regenerating tissues. ([GO:0051094](http://purl.obolibrary.org/obo/GO_0051094))
- **CPNE8**: [INFERENCE] Ca2+-dependent adaptor proposed to modulate satellite cell responses to ECM signals. ([GO:0051094](http://purl.obolibrary.org/obo/GO_0051094))

#### Statistical Context

[GO:0051094](http://purl.obolibrary.org/obo/GO_0051094) enriched at FDR=1.45e-02 (2.4x) with 24/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 19: laminin trimer

**Summary:** laminin trimer ([GO:0043256](http://purl.obolibrary.org/obo/GO_0043256))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] The laminin trimer theme reflects assembly of specific αβγ laminin isoforms that nucleate basement membrane scaffolds and signal through integrins and dystroglycan.[DATA] LAMC1 partners with multiple α chains to form diverse laminin trimers (e.g., 211, 221, 511, 521), enabling tissue-specific basement membrane architectures and adhesion signaling [PMID:21421915](https://pubmed.ncbi.nlm.nih.gov/21421915/), [PMID:16236823](https://pubmed.ncbi.nlm.nih.gov/16236823/).[INFERENCE] LAMA4-containing laminins (411/421) specialize vascular basement membranes to regulate endothelial adhesion and sprouting dynamics.[INFERENCE] LAMA2-containing laminins (211/221) support muscle and neural basement membranes, coupling structural integrity to cell fate via receptor engagement.

#### Key Insights

- Gamma1-containing laminin trimers scaffold basement membranes and instruct integrin/dystroglycan signaling. ([GO:0043256](http://purl.obolibrary.org/obo/GO_0043256))
- Isoform-specific assemblies (e.g., laminin-421 and -221) impose vascular versus neuromuscular matrix functions. ([GO:0043256](http://purl.obolibrary.org/obo/GO_0043256))

#### Key Genes

- **LAMC1**: [INFERENCE] Gamma1 chain central to numerous laminin trimer assemblies across tissues. ([GO:0043256](http://purl.obolibrary.org/obo/GO_0043256))
- **LAMA4**: [INFERENCE] Alpha4 chain forming vascular laminin-421 to shape endothelial basement membranes. ([GO:0043258](http://purl.obolibrary.org/obo/GO_0043258))
- **LAMA2**: [INFERENCE] Alpha2 chain forming laminin-221 to support muscle and neural basement membranes. ([GO:0005609](http://purl.obolibrary.org/obo/GO_0005609))

#### Statistical Context

[GO:0043256](http://purl.obolibrary.org/obo/GO_0043256) enriched at FDR=1.59e-02 (26.3x) with 3/173 annotated input genes; child terms laminin-421 trimer and laminin-221 trimer FDR=1.72e-02 each.

---

### Theme 20: cell-cell signaling

**Summary:** cell-cell signaling ([GO:0007267](http://purl.obolibrary.org/obo/GO_0007267))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Cell–cell signaling in this set couples neurotransmission, cytokine co-receptors, and nuclear hormone receptors to coordinate intercellular communication.[EXTERNAL] Estrogen receptor beta (ESR2) regulates transcriptional programs that intersect with Wnt/β-catenin signaling to modulate proliferation and differentiation in target tissues [PMID:19075275](https://pubmed.ncbi.nlm.nih.gov/19075275/), [PMID:17468844](https://pubmed.ncbi.nlm.nih.gov/17468844/).[DATA] GRIN2B-containing NMDARs mediate excitatory chemical synaptic transmission, coupling Ca2+ influx to plasticity pathways [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/).[DATA] KCNIP1 modulates synaptic signaling by tuning Kv4.3 channel function that shapes action potential repolarization and synaptic integration [PMID:21349352](https://pubmed.ncbi.nlm.nih.gov/21349352/).[DATA] The dystrophin-associated complex component SNTG1 stabilizes synaptic signaling architectures at neuromuscular and neuronal synapses [PMID:19899002](https://pubmed.ncbi.nlm.nih.gov/19899002/).

#### Key Insights

- Ionotropic glutamate receptor signaling and K+ channel modulators shape fast synaptic communication and plasticity. ([GO:0007267](http://purl.obolibrary.org/obo/GO_0007267))
- Nuclear receptor ESR2 integrates endocrine cues with developmental signaling for tissue-level coordination. ([GO:0007267](http://purl.obolibrary.org/obo/GO_0007267))

#### Key Genes

- **ESR2**: [INFERENCE] Ligand-activated transcription factor coordinating intercellular hormonal signals with developmental pathways. ([GO:0007267](http://purl.obolibrary.org/obo/GO_0007267))
- **FGF14**: [INFERENCE] Modulator of neuronal excitability that impacts synaptic communication dynamics. ([GO:0007267](http://purl.obolibrary.org/obo/GO_0007267))
- **KCNIP1**: [INFERENCE] K+ channel interacting protein shaping repolarization and synaptic timing. ([GO:0007267](http://purl.obolibrary.org/obo/GO_0007267))
- **SLC1A2**: [INFERENCE] High-affinity glutamate transporter clearing transmitter to terminate signaling. ([GO:0007267](http://purl.obolibrary.org/obo/GO_0007267))

#### Statistical Context

[GO:0007267](http://purl.obolibrary.org/obo/GO_0007267) enriched at FDR=1.64e-02 (3.1x) with 16/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 21: regulation of neuronal synaptic plasticity

**Summary:** regulation of neuronal synaptic plasticity ([GO:0048168](http://purl.obolibrary.org/obo/GO_0048168))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of neuronal synaptic plasticity captures Ca2+/calmodulin decoding, AMPAR trafficking, and kainate receptor-mediated presynaptic modulation that set learning rules.[DATA] CAMK2 family members regulate long-term synaptic plasticity through Ca2+/calmodulin-triggered phosphorylation cascades that stabilize potentiated synapses [PMID:18817731](https://pubmed.ncbi.nlm.nih.gov/18817731/).[DATA] Presynaptic GRIK2-containing kainate receptors modulate short-term facilitation at mossy fiber synapses, shaping information transfer [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/).[DATA] NMDAR signaling is essential for maintenance of remote memories, placing GRIN2 subunits at the core of plasticity regulation [PMID:15003177](https://pubmed.ncbi.nlm.nih.gov/15003177/).[INFERENCE] AMPAR auxiliary protein SHISA9 tunes receptor stability and dwell time at synapses to calibrate plasticity thresholds.

#### Key Insights

- CaMKII-dependent phosphorylation consolidates LTP, while GRIK2 modulates presynaptic facilitation to shape learning dynamics. ([GO:0048168](http://purl.obolibrary.org/obo/GO_0048168))
- Regulated AMPAR/NMDAR trafficking calibrates synaptic strength over short and long timescales. ([GO:0048168](http://purl.obolibrary.org/obo/GO_0048168))

#### Key Genes

- **SHISA9**: [INFERENCE] AMPAR modulator constraining receptor trafficking to tune plasticity setpoints. ([GO:0048168](http://purl.obolibrary.org/obo/GO_0048168))
- **CAMK2D**: [INFERENCE] Ca2+/calmodulin-dependent kinase that phosphorylates substrates to enhance LTP. ([GO:0048168](http://purl.obolibrary.org/obo/GO_0048168))
- **GRIK2**: [INFERENCE] Kainate receptor subunit controlling short-term synaptic facilitation. ([GO:0048168](http://purl.obolibrary.org/obo/GO_0048168))

#### Statistical Context

[GO:0048168](http://purl.obolibrary.org/obo/GO_0048168) enriched at FDR=1.95e-02 (11.6x) with 5/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 22: cell-cell junction

**Summary:** cell-cell junction ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] The cell–cell junction theme integrates tight and adherens junction signaling with phosphatase control to balance barrier function and growth cues.[DATA] Tight junctions couple to MEKK1–JNK via MarvelD3 and MAP3K1, linking junction reassembly to stress signaling that regulates survival and behavior [PMID:24567356](https://pubmed.ncbi.nlm.nih.gov/24567356/).[DATA] PTPRJ localizes to junctions where it modulates tyrosine phosphorylation of junctional proteins, strengthening barrier function [PMID:19332538](https://pubmed.ncbi.nlm.nih.gov/19332538/).[DATA] FRMD5 interacts with p120-catenin at adherens junctions, stabilizing cadherin complexes and restraining tumorigenic behaviors [PMID:22846708](https://pubmed.ncbi.nlm.nih.gov/22846708/).[DATA] Cadherins including CDH2 reside at adherens junctions to connect to cortical actin, providing mechanical continuity across cells [PMID:24046456](https://pubmed.ncbi.nlm.nih.gov/24046456/).

#### Key Insights

- Tight junction transmembrane components signal via MAP3K1 to coordinate barrier assembly with survival pathways. ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- Adherens junction stability depends on phosphatase and p120-catenin scaffolding that tunes cadherin–actin linkages. ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))

#### Key Genes

- **ILDR2**: [INFERENCE] Tight junction-associated Ig-like receptor implicated in barrier organization and signaling. ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **WWTR1**: [INFERENCE] Hippo effector influencing junctional gene programs and cytoskeletal tension. ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **FRMD5**: [INFERENCE] Adherens junction scaffold partnering with p120-catenin to stabilize cadherin complexes. ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **MAP3K1**: [INFERENCE] Kinase linking tight junction cues to JNK signaling during junction remodeling. ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))

#### Statistical Context

[GO:0005911](http://purl.obolibrary.org/obo/GO_0005911) enriched at FDR=1.95e-02 (3.0x) with 14/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 23: basement membrane

**Summary:** basement membrane ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Basement membrane assembly relies on laminin and collagen IV networks cross-linked by nidogen to form a resilient signaling scaffold for epithelia, endothelium, and muscle.[DATA] LAMA2, LAMA4, and LAMC1 are core basement membrane constituents in adrenal cortex and other tissues, underscoring conserved matrix architecture [PMID:14557481](https://pubmed.ncbi.nlm.nih.gov/14557481/).[DATA] Transglutaminase-mediated cross-linking of laminin–nidogen complexes stabilizes the basement membrane and strengthens tissue barriers [PMID:1678389](https://pubmed.ncbi.nlm.nih.gov/1678389/).[DATA] Disrupting nidogen interactions impairs BM assembly, highlighting LAMC1-dependent interfaces as essential for scaffold integrity [PMID:15159456](https://pubmed.ncbi.nlm.nih.gov/15159456/), [PMID:22952693](https://pubmed.ncbi.nlm.nih.gov/22952693/).[INFERENCE] COL22A1 and COL4A2 integrate with laminin networks to provide tensile strength and controlled permeability for morphogenesis.

#### Key Insights

- Laminin–nidogen cross-linking and LAMC1 interfaces are keystones of basement membrane stability. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))
- Collagen IV and XXII enrich mechanical resilience and guide cell adhesion signaling from the BM. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))

#### Key Genes

- **FREM2**: [INFERENCE] Matrix linker stabilizing BM interfaces between epithelia and mesenchyme. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))
- **COL22A1**: [INFERENCE] BM-associated collagen contributing to mechanical stabilization and linkage to laminin networks. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))
- **LAMC1**: [INFERENCE] Gamma1 laminin chain central to BM assembly and signaling to resident cells. ([GO:0005604](http://purl.obolibrary.org/obo/GO_0005604))

#### Statistical Context

[GO:0005604](http://purl.obolibrary.org/obo/GO_0005604) enriched at FDR=1.98e-02 (6.7x) with 6/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 24: positive regulation of cell proliferation in bone marrow

**Summary:** positive regulation of cell proliferation in bone marrow ([GO:0071864](http://purl.obolibrary.org/obo/GO_0071864))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Positive regulation of cell proliferation in bone marrow reflects transcriptional drivers of granulocytic lineage expansion and survival.[DATA] LEF1 is essential for granulocyte progenitor proliferation and differentiation, and its reduction in congenital neutropenia reveals its central role in myelopoiesis [PMID:17063141](https://pubmed.ncbi.nlm.nih.gov/17063141/).[INFERENCE] HMGA2 likely enhances LEF1-driven programs and other developmental genes to sustain progenitor cycling and overcome differentiation blocks within marrow niches.[INFERENCE] Together these factors coordinate Wnt-related and architectural chromatin control to promote effective neutrophil output.

#### Key Insights

- LEF1-dependent transcription drives granulocyte progenitor proliferation and maturation in bone marrow. ([GO:0071864](http://purl.obolibrary.org/obo/GO_0071864))

#### Key Genes

- **HMGA2**: [INFERENCE] Chromatin architectural factor proposed to boost LEF1-centered proliferative programs in progenitors. ([GO:0071864](http://purl.obolibrary.org/obo/GO_0071864))
- **LEF1**: [INFERENCE] Transcription factor required for granulocyte progenitor proliferation and survival in bone marrow. ([GO:0071864](http://purl.obolibrary.org/obo/GO_0071864))

#### Statistical Context

[GO:0071864](http://purl.obolibrary.org/obo/GO_0071864) enriched at FDR=2.04e-02 (113.8x) with 2/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 25: ligand-gated calcium channel activity

**Summary:** ligand-gated calcium channel activity ([GO:0099604](http://purl.obolibrary.org/obo/GO_0099604))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Ligand-gated calcium channel activity aggregates plasma membrane and ER channels that convert chemical signals into Ca2+ flux for excitation and secretion.[DATA] GRIN2B-containing NMDARs conduct Ca2+ upon glutamate binding and depolarization, initiating Ca2+-dependent signaling cascades [PMID:27839871](https://pubmed.ncbi.nlm.nih.gov/27839871/), [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/).[DATA] RYR3 provides ryanodine-sensitive Ca2+ release from intracellular stores, expanding and shaping cytosolic Ca2+ signals [PMID:19095005](https://pubmed.ncbi.nlm.nih.gov/19095005/), [PMID:9395096](https://pubmed.ncbi.nlm.nih.gov/9395096/).[DATA] ITPR2 mediates IP3-gated ER Ca2+ release to support diverse Ca2+-dependent processes including neurotransmission [PMID:8081734](https://pubmed.ncbi.nlm.nih.gov/8081734/).[INFERENCE] AMPAR subunit GRIA3 and KAR subunit GRIK2 complement these pathways to tailor synaptic Ca2+ entry and plasticity rules.

#### Key Insights

- NMDA receptor Ca2+ entry integrates with RyR/IP3R store release to amplify and pattern intracellular Ca2+ signals. ([GO:0099604](http://purl.obolibrary.org/obo/GO_0099604))

#### Key Genes

- **ITPR2**: [INFERENCE] IP3-gated Ca2+ channel releasing ER Ca2+ to shape cytosolic transients. ([GO:0099604](http://purl.obolibrary.org/obo/GO_0099604))
- **RYR3**: [INFERENCE] Ryanodine receptor mediating intracellular Ca2+ release to amplify signals. ([GO:0099604](http://purl.obolibrary.org/obo/GO_0099604))
- **GRIA3**: [INFERENCE] AMPAR subunit supporting fast ligand-gated cation flux including Ca2+ in specific contexts. ([GO:0099604](http://purl.obolibrary.org/obo/GO_0099604))
- **GRIK2**: [INFERENCE] Kainate receptor subunit contributing to synaptic Ca2+ entry and modulation. ([GO:0099604](http://purl.obolibrary.org/obo/GO_0099604))

#### Statistical Context

[GO:0099604](http://purl.obolibrary.org/obo/GO_0099604) enriched at FDR=2.12e-02 (20.3x) with 5/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 26: cell surface receptor protein tyrosine kinase signaling pathway

**Summary:** cell surface receptor protein tyrosine kinase signaling pathway ([GO:0007169](http://purl.obolibrary.org/obo/GO_0007169))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Cell surface receptor protein tyrosine kinase signaling pathway encapsulates ligand-induced RTK activation and downstream cascades controlling proliferation and migration.[DATA] ALK engages ligands to dimerize and autophosphorylate, initiating neural development and oncogenic signaling programs [PMID:34646012](https://pubmed.ncbi.nlm.nih.gov/34646012/), [PMID:30061385](https://pubmed.ncbi.nlm.nih.gov/30061385/), [PMID:25605972](https://pubmed.ncbi.nlm.nih.gov/25605972/).[DATA] FGFR1 signaling calibrates developmental differentiation and endothelial functions, linking growth factors to cytoskeletal reorganization [PMID:22235191](https://pubmed.ncbi.nlm.nih.gov/22235191/), [PMID:21885851](https://pubmed.ncbi.nlm.nih.gov/21885851/).[INFERENCE] ECM components such as COL4A2 and protease–coagulation effectors like PLAT modulate RTK responsiveness through matrix-binding and PAR cross-activation, shaping signal amplitude and duration.[INFERENCE] Negative adaptors UBASH3B and GRB10 likely attenuate RTK output via dephosphorylation and ubiquitin-mediated receptor turnover.

#### Key Insights

- Ligand-bound ALK and FGFR1 autoactivate to drive developmental transcription and cytoskeletal remodeling. ([GO:0007169](http://purl.obolibrary.org/obo/GO_0007169))
- Matrix composition and adaptor-mediated attenuation set RTK signaling gain and kinetic profiles. ([GO:0007169](http://purl.obolibrary.org/obo/GO_0007169))

#### Key Genes

- **GRB10**: [INFERENCE] Adaptor that constrains RTK signaling by promoting receptor downregulation. ([GO:0007169](http://purl.obolibrary.org/obo/GO_0007169))
- **UBASH3B**: [INFERENCE] Phosphatase-associated regulator attenuating RTK phosphorylation to limit downstream flux. ([GO:0007169](http://purl.obolibrary.org/obo/GO_0007169))
- **ALK**: [INFERENCE] RTK undergoing autophosphorylation upon ligand binding to launch signaling cascades. ([GO:0007169](http://purl.obolibrary.org/obo/GO_0007169))
- **FGFR1**: [INFERENCE] FGF receptor controlling differentiation and motility through MAPK/ERK signaling. ([GO:0007169](http://purl.obolibrary.org/obo/GO_0007169))

#### Statistical Context

[GO:0007169](http://purl.obolibrary.org/obo/GO_0007169) enriched at FDR=3.45e-02 (3.6x) with 12/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 27: protein serine kinase activity

**Summary:** protein serine kinase activity ([GO:0106310](http://purl.obolibrary.org/obo/GO_0106310))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Protein serine kinase activity aggregates mitotic, stress, and cytoskeletal kinases that encode signals into phosphorylation to direct cell cycle and morphogenesis.[DATA] PRKD1 is a VEGF-activated serine kinase in endothelium controlling proliferation, migration, and permeability programs [PMID:20497126](https://pubmed.ncbi.nlm.nih.gov/20497126/).[DATA] NEK6 phosphorylates microtubule regulator EML4 during mitosis to lower microtubule affinity and ensure chromosome congression [PMID:31409757](https://pubmed.ncbi.nlm.nih.gov/31409757/).[INFERENCE] STK17A coordinates stress/apoptosis signaling through serine phosphorylation of effectors, while CDK14 and MAP3K1 interface with transcriptional and MAPK modules to align growth with morphogenetic signals.[INFERENCE] TRIO’s GEF-associated kinase domain and CAMK2 family further connect Ca2+ and Rho signaling to serine phosphorylation outputs.

#### Key Insights

- Endothelial PRKD1 integrates growth factor signals into serine phosphorylation programs for angiogenic behaviors. ([GO:0106310](http://purl.obolibrary.org/obo/GO_0106310))
- Mitotic NEK6 modifies microtubule-binding proteins to choreograph spindle function and cell division. ([GO:0106310](http://purl.obolibrary.org/obo/GO_0106310))

#### Key Genes

- **NEK6**: [INFERENCE] Serine/threonine kinase active in mitosis to regulate spindle-associated proteins. ([GO:0106310](http://purl.obolibrary.org/obo/GO_0106310))
- **STK32B**: [INFERENCE] Serine kinase candidate potentially modulating endothelial signaling cascades. ([GO:0106310](http://purl.obolibrary.org/obo/GO_0106310))
- **CDK14**: [INFERENCE] Cyclin-dependent kinase influencing transcriptional programs relevant to growth signaling. ([GO:0106310](http://purl.obolibrary.org/obo/GO_0106310))
- **STK17A**: [INFERENCE] Death-associated protein kinase orchestrating stress-responsive phosphorylation. ([GO:0106310](http://purl.obolibrary.org/obo/GO_0106310))

#### Statistical Context

[GO:0106310](http://purl.obolibrary.org/obo/GO_0106310) enriched at FDR=3.59e-02 (4.1x) with 13/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 28: ionotropic glutamate receptor complex

**Summary:** ionotropic glutamate receptor complex ([GO:0008328](http://purl.obolibrary.org/obo/GO_0008328))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 3.63e-02 · **Genes (4)**: GRIA3, GRIK2, GRIN2B, SHISA9

---

### Theme 29: sarcoplasmic reticulum membrane

**Summary:** sarcoplasmic reticulum membrane ([GO:0033017](http://purl.obolibrary.org/obo/GO_0033017))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Sarcoplasmic reticulum membrane components orchestrate Ca2+ release and kinase tethering to control excitation–contraction and Ca2+ signaling microdomains.[DATA] ITPR2 localizes to sarcoplasmic/endoplasmic reticulum membranes to mediate IP3-evoked Ca2+ release in human platelets [PMID:10828023](https://pubmed.ncbi.nlm.nih.gov/10828023/).[INFERENCE] RYR3 complements this pathway with depolarization-coupled Ca2+-induced Ca2+ release, sustaining cytosolic Ca2+ waves during contraction and excitability.[INFERENCE] CAMK2D enrichment at SR membranes enables rapid decoding of Ca2+ spikes into phosphorylation of local targets that modulate release sensitivity and reuptake.

#### Key Insights

- IP3R2- and RyR3-mediated store release forms the core SR Ca2+ release machinery, with CAMK2D locally decoding signals. ([GO:0033017](http://purl.obolibrary.org/obo/GO_0033017))

#### Key Genes

- **ITPR2**: [INFERENCE] SR/ER Ca2+ release channel generating IP3-driven Ca2+ transients. ([GO:0033017](http://purl.obolibrary.org/obo/GO_0033017))
- **RYR3**: [INFERENCE] RyR channel releasing SR Ca2+ to amplify cytosolic signaling and contraction. ([GO:0033017](http://purl.obolibrary.org/obo/GO_0033017))
- **CAMK2D**: [INFERENCE] Ca2+/calmodulin-dependent kinase tethered near SR to modulate release machinery phosphorylation. ([GO:0033017](http://purl.obolibrary.org/obo/GO_0033017))

#### Statistical Context

[GO:0033017](http://purl.obolibrary.org/obo/GO_0033017) enriched at FDR=3.63e-02 (10.3x) with 4/173 annotated input genes; theme confidence FDR<0.05.

---

### Theme 30: negative regulation of small GTPase mediated signal transduction

**Summary:** negative regulation of small GTPase mediated signal transduction ([GO:0051058](http://purl.obolibrary.org/obo/GO_0051058))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 3.64e-02 · **Genes (5)**: DLC1, ITGA3, KANK1, SPRY2, SPRY4

---

## Hub Genes

- **PRKD1**: [EXTERNAL] [EXTERNAL] PRKD1 is a serine/threonine kinase activated downstream of VEGF and autophosphorylation that maintains dendritic arborization and drives endothelial proliferation, migration, and permeability to coordinate morphogenesis and angiogenesis [PMID:19211839](https://pubmed.ncbi.nlm.nih.gov/19211839/), [PMID:20497126](https://pubmed.ncbi.nlm.nih.gov/20497126/), [PMID:24623306](https://pubmed.ncbi.nlm.nih.gov/24623306/).
- **CAMK2B**: [EXTERNAL] [EXTERNAL] CAMK2B phosphorylates cytoskeletal and synaptic substrates to regulate neuron migration and long-term synaptic plasticity, linking Ca2+ transients to structural remodeling and learning [PMID:29100089](https://pubmed.ncbi.nlm.nih.gov/29100089/), [PMID:18817731](https://pubmed.ncbi.nlm.nih.gov/18817731/).
- **SEMA5A**: [EXTERNAL] [EXTERNAL] SEMA5A guides axons through Plexin signaling to reposition growth cones by reorganizing adhesion and cytoskeleton, integrating morphogenesis with neuronal wiring [PMID:9464278](https://pubmed.ncbi.nlm.nih.gov/9464278/).
- **SPRY2**: [EXTERNAL] [EXTERNAL] SPRY2 inhibits RTK–RAS–MAPK signaling to restrain endothelial proliferation and migration, acting as an anti-angiogenic and anti-EMT brake across developmental contexts [PMID:24177325](https://pubmed.ncbi.nlm.nih.gov/24177325/).
- **GRIN2B**: [EXTERNAL] [EXTERNAL] GRIN2B encodes an NMDA receptor subunit mediating Ca2+ influx that regulates synaptic transmission and plasticity, with Fyn–NR2B phosphorylation controlling receptor cleavage and function across neuronal compartments [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/), [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/).
- **EPHA3**: [INFERENCE] [INFERENCE] EPHA3 activates forward signaling to reprogram adhesion and actin dynamics, directing cell and axon steering and modulating EMT-associated motility.
- **LIMK1**: [EXTERNAL] [EXTERNAL] LIMK1 phosphorylates cofilin to promote actin polymerization, enabling dendritic spine maturation and glutamatergic synapse stability during plasticity [PMID:25884247](https://pubmed.ncbi.nlm.nih.gov/25884247/), [PMID:23633677](https://pubmed.ncbi.nlm.nih.gov/23633677/).
- **KANK1**: [EXTERNAL] [EXTERNAL] KANK1 suppresses Rac/IRSp53-dependent lamellipodia and multiple protrusive structures and reduces substrate adhesion-dependent spreading, integrating membrane ruffles with projection and migration control [PMID:19171758](https://pubmed.ncbi.nlm.nih.gov/19171758/), [PMID:19559006](https://pubmed.ncbi.nlm.nih.gov/19559006/).
- **PDGFA**: [INFERENCE] [INFERENCE] PDGFA activates PDGFR to drive PI3K–AKT/MAPK signaling that promotes cell migration, phosphorylation cascades, and morphogenetic tissue remodeling including angiogenesis.
- **JAG1**: [EXTERNAL] [EXTERNAL] JAG1 engages Notch receptors to steer neural development and endothelial sprout behavior, coordinating fate decisions with angiogenic patterning [PMID:8923452](https://pubmed.ncbi.nlm.nih.gov/8923452/), [PMID:8955070](https://pubmed.ncbi.nlm.nih.gov/8955070/).
- **GRIK2**: [EXTERNAL] [EXTERNAL] GRIK2 assembles kainate receptors that modulate presynaptic facilitation and dendritic signaling, thereby tuning short-term synaptic plasticity and Ca2+ dynamics [PMID:21893069](https://pubmed.ncbi.nlm.nih.gov/21893069/), [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/), [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/).
- **NRCAM**: [EXTERNAL] [EXTERNAL] NRCAM mediates cell adhesion in neural and endothelial contexts to support synaptic connectivity and is induced during endothelial tubulogenesis, linking adhesion to angiogenesis [PMID:11866539](https://pubmed.ncbi.nlm.nih.gov/11866539/).
- **PTPRJ**: [EXTERNAL] [EXTERNAL] PTPRJ promotes focal adhesion assembly and modulates junctional protein phosphorylation to restrain motility and strengthen barrier function across angiogenic and guidance settings [PMID:21091576](https://pubmed.ncbi.nlm.nih.gov/21091576/), [PMID:19332538](https://pubmed.ncbi.nlm.nih.gov/19332538/).
- **SEMA3E**: [EXTERNAL] [EXTERNAL] SEMA3E provides repulsive guidance that regulates GnRH neuron migration and vascular patterning by collapsing growth cones via plexin signaling [PMID:25985275](https://pubmed.ncbi.nlm.nih.gov/25985275/).
- **LPAR1**: [EXTERNAL] [EXTERNAL] LPAR1 signaling switches Rab11–Rabin8 trafficking to inhibit ciliogenesis, coupling GPCR inputs to projection organization and migration behaviors [PMID:31204173](https://pubmed.ncbi.nlm.nih.gov/31204173/).
- **FGFR1**: [EXTERNAL] [EXTERNAL] FGFR1 activation drives ERK-dependent programs for motility and differentiation and modulates postsynaptic organization in neural circuits and angiogenesis [PMID:22235191](https://pubmed.ncbi.nlm.nih.gov/22235191/), [PMID:21885851](https://pubmed.ncbi.nlm.nih.gov/21885851/).
- **DPYSL5**: [EXTERNAL] [EXTERNAL] DPYSL5 (CRMP5) decodes semaphorin signals to regulate dendrite morphogenesis and axon guidance, integrating projection patterning with synaptic development [PMID:33894126](https://pubmed.ncbi.nlm.nih.gov/33894126/), [PMID:10851247](https://pubmed.ncbi.nlm.nih.gov/10851247/).
- **SPRED1**: [INFERENCE] [INFERENCE] SPRED1 antagonizes RAF–MEK–ERK signaling to restrain EMT and angiogenic drive, coordinating plasma membrane RTK signals with morphogenesis limits.
- **KALRN**: [INFERENCE] [INFERENCE] KALRN activates Rac/Rho GTPases to reorganize cytoskeleton for axon guidance and cell motility, interfacing with RTK pathways in neural development.
- **LAMA2**: [EXTERNAL] [EXTERNAL] LAMA2 forms laminin-211/221 trimers that assemble basement membranes, directing cell adhesion, migration, and muscle/neural development through integrin and dystroglycan signaling [PMID:21421915](https://pubmed.ncbi.nlm.nih.gov/21421915/), [PMID:26555376](https://pubmed.ncbi.nlm.nih.gov/26555376/).

## Overall Summary

[DATA] The enrichment landscape is dominated by neurodevelopmental and synaptic themes (glutamatergic synapse, dendrite, postsynaptic organization) together with guidance and motility programs, supported by 173 annotated genes and 107 significant terms at FDR≤0.05.

[INFERENCE] A unifying mechanism is cue-to-cytoskeleton transduction in which semaphorin/EPH/RTK signals converge on Rho GTPases and actin modulators (LIMK1, KANK1, DLC1) to reshape projections and migration during morphogenesis, while Ca2+-coupled kinases (CAMK2, PRKD1) synchronize electrical activity with structural plasticity.

[DATA] Matrix modules (laminin trimers, basement membrane) and adhesion systems (cadherin/integrin/PTPRJ) provide the mechanical and signaling scaffold for coordinated angiogenesis and tissue patterning, with Notch (JAG1) and growth factor (FGFR1, PDGFA) crosstalk modulating sprout selection and stabilization.

[INFERENCE] Hub genes with multi-theme presence (PRKD1, CAMK2B, GRIN2B, SEMA family, FGFR1, KANK1) likely act as biological coordinators linking synaptic signaling, projection dynamics, and vascular remodeling within a shared developmental program.

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

