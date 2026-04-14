# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_8_themes.csv](Cluster_8_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-myelination) | [myelination](#theme-1-myelination) [GO:0042552](http://purl.obolibrary.org/obo/GO_0042552) | BP | 4.49e-08 | 15 | FDR<0.01 |
| [2](#theme-2-structural-constituent-of-myelin-sheath) | [structural constituent of myelin sheath](#theme-2-structural-constituent-of-myelin-sheath) [GO:0019911](http://purl.obolibrary.org/obo/GO_0019911) | MF | 1.16e-04 | 5 | FDR<0.01 |
| [3](#theme-3-synapse) | [synapse](#theme-3-synapse) [GO:0045202](http://purl.obolibrary.org/obo/GO_0045202) | CC | 2.11e-04 | 30 | FDR<0.01 |
| [4](#theme-4-protein-localization-to-axon) | [protein localization to axon](#theme-4-protein-localization-to-axon) [GO:0099612](http://purl.obolibrary.org/obo/GO_0099612) | BP | 3.64e-04 | 4 | FDR<0.01 |
| [5](#theme-5-neuron-projection) | [neuron projection](#theme-5-neuron-projection) [GO:0043005](http://purl.obolibrary.org/obo/GO_0043005) | CC | 5.27e-04 | 26 | FDR<0.01 |
| [6](#theme-6-internode-region-of-axon) | [internode region of axon](#theme-6-internode-region-of-axon) [GO:0033269](http://purl.obolibrary.org/obo/GO_0033269) | CC | 5.27e-04 | 3 | FDR<0.01 |
| [7](#theme-7-compact-myelin) | [compact myelin](#theme-7-compact-myelin) [GO:0043218](http://purl.obolibrary.org/obo/GO_0043218) | CC | 5.27e-04 | 3 | FDR<0.01 |
| [8](#theme-8-apical-plasma-membrane) | [apical plasma membrane](#theme-8-apical-plasma-membrane) [GO:0016324](http://purl.obolibrary.org/obo/GO_0016324) | CC | 5.54e-04 | 15 | FDR<0.01 |
| [9](#theme-9-dna-templated-transcription) | [DNA-templated transcription](#theme-9-dna-templated-transcription) [GO:0006351](http://purl.obolibrary.org/obo/GO_0006351) | BP | 1.01e-03 | 4 | FDR<0.01 |
| [10](#theme-10-perinuclear-region-of-cytoplasm) | [perinuclear region of cytoplasm](#theme-10-perinuclear-region-of-cytoplasm) [GO:0048471](http://purl.obolibrary.org/obo/GO_0048471) | CC | 2.41e-03 | 19 | FDR<0.01 |
| [11](#theme-11-regulation-of-dna-templated-transcription) | [regulation of DNA-templated transcription](#theme-11-regulation-of-dna-templated-transcription) [GO:0006355](http://purl.obolibrary.org/obo/GO_0006355) | BP | 5.26e-03 | 9 | FDR<0.01 |
| [12](#theme-12-cell-cell-adhesion) | [cell-cell adhesion](#theme-12-cell-cell-adhesion) [GO:0098609](http://purl.obolibrary.org/obo/GO_0098609) | BP | 6.89e-03 | 16 | FDR<0.01 |
| [13](#theme-13-membrane-organization) | [membrane organization](#theme-13-membrane-organization) [GO:0061024](http://purl.obolibrary.org/obo/GO_0061024) | BP | 7.35e-03 | 17 | FDR<0.01 |
| [14](#theme-14-nucleoplasm) | [nucleoplasm](#theme-14-nucleoplasm) [GO:0005654](http://purl.obolibrary.org/obo/GO_0005654) | CC | 7.93e-03 | 13 | FDR<0.01 |
| [15](#theme-15-ras-protein-signal-transduction) | [Ras protein signal transduction](#theme-15-ras-protein-signal-transduction) [GO:0007265](http://purl.obolibrary.org/obo/GO_0007265) | BP | 1.15e-02 | 6 | FDR<0.05 |
| [16](#theme-16-transmembrane-transport) | [transmembrane transport](#theme-16-transmembrane-transport) [GO:0055085](http://purl.obolibrary.org/obo/GO_0055085) | BP | 1.21e-02 | 27 | FDR<0.05 |
| [17](#theme-17-transporter-activity) | [transporter activity](#theme-17-transporter-activity) [GO:0005215](http://purl.obolibrary.org/obo/GO_0005215) | MF | 1.23e-02 | 28 | FDR<0.05 |
| [18](#theme-18-cell-surface) | [cell surface](#theme-18-cell-surface) [GO:0009986](http://purl.obolibrary.org/obo/GO_0009986) | CC | 1.32e-02 | 17 | FDR<0.05 |
| [19](#theme-19-juxtaparanode-region-of-axon) | [juxtaparanode region of axon](#theme-19-juxtaparanode-region-of-axon) [GO:0044224](http://purl.obolibrary.org/obo/GO_0044224) | CC | 1.37e-02 | 3 | FDR<0.05 |
| [20](#theme-20-basolateral-plasma-membrane) | [basolateral plasma membrane](#theme-20-basolateral-plasma-membrane) [GO:0016323](http://purl.obolibrary.org/obo/GO_0016323) | CC | 1.62e-02 | 10 | FDR<0.05 |
| [21](#theme-21-monoatomic-ion-transport) | [monoatomic ion transport](#theme-21-monoatomic-ion-transport) [GO:0006811](http://purl.obolibrary.org/obo/GO_0006811) | BP | 2.00e-02 | 22 | FDR<0.05 |
| [22](#theme-22-cytoskeleton) | [cytoskeleton](#theme-22-cytoskeleton) [GO:0005856](http://purl.obolibrary.org/obo/GO_0005856) | CC | 2.12e-02 | 22 | FDR<0.05 |
| [23](#theme-23-sphingolipid-metabolic-process) | [sphingolipid metabolic process](#theme-23-sphingolipid-metabolic-process) [GO:0006665](http://purl.obolibrary.org/obo/GO_0006665) | BP | 2.19e-02 | 8 | FDR<0.05 |
| [24](#theme-24-nuclear-protein-containing-complex) | [nuclear protein-containing complex](#theme-24-nuclear-protein-containing-complex) [GO:0140513](http://purl.obolibrary.org/obo/GO_0140513) | CC | 2.19e-02 | 1 | FDR<0.05 |
| [25](#theme-25-dna-binding) | [DNA binding](#theme-25-dna-binding) [GO:0003677](http://purl.obolibrary.org/obo/GO_0003677) | MF | 2.78e-02 | 6 | FDR<0.05 |
| [26](#theme-26-regulation-of-oligodendrocyte-differentiation) | [regulation of oligodendrocyte differentiation](#theme-26-regulation-of-oligodendrocyte-differentiation) [GO:0048713](http://purl.obolibrary.org/obo/GO_0048713) | BP | 3.02e-02 | 4 | FDR<0.05 |
| [27](#theme-27-neuronal-cell-body) | [neuronal cell body](#theme-27-neuronal-cell-body) [GO:0043025](http://purl.obolibrary.org/obo/GO_0043025) | CC | 3.05e-02 | 11 | FDR<0.05 |

---

### Theme 1: myelination

**Summary:** myelination ([GO:0042552](http://purl.obolibrary.org/obo/GO_0042552))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Myelination ([GO:0042552](http://purl.obolibrary.org/obo/GO_0042552)) organizes glial-axon interactions into sheath initiation, growth, and compaction, with child terms capturing rate control, assembly, and CNS specificity. [DATA] The signal is strong in this set (FDR 4.49e-08, 11 genes, 19.7x enrichment), with leaves enriched for positive regulation of myelination ([GO:0031643](http://purl.obolibrary.org/obo/GO_0031643)), myelin assembly ([GO:0032288](http://purl.obolibrary.org/obo/GO_0032288)), and central nervous system myelination ([GO:0022010](http://purl.obolibrary.org/obo/GO_0022010)). [INFERENCE] Assembly genes coordinate lipid and structural protein trafficking to myelin membranes while positive regulators tune OPC differentiation and wrapping dynamics, linking transcriptional programs to membrane biogenesis. [INFERENCE] Axon–glia adhesion stabilizes paranodal architecture and ensures proper sheath spacing for saltatory conduction, integrating MAG-mediated adhesion with cytoskeletal remodeling in oligodendrocytes.

#### Key Insights

- [GO-HIERARCHY] Positive regulation of myelination ([GO:0031643](http://purl.obolibrary.org/obo/GO_0031643)) feeds into the parent myelination program by accelerating OPC differentiation and promoting sheath growth. ([GO:0031643](http://purl.obolibrary.org/obo/GO_0031643))
- [GO-HIERARCHY] Myelin assembly ([GO:0032288](http://purl.obolibrary.org/obo/GO_0032288)) specifies the structural build of compact membrane stacks within the broader myelination process. ([GO:0032288](http://purl.obolibrary.org/obo/GO_0032288))
- [GO-HIERARCHY] Central nervous system myelination ([GO:0022010](http://purl.obolibrary.org/obo/GO_0022010)) constrains the parent process to brain and spinal cord contexts with lineage-specific transcriptional control. ([GO:0022010](http://purl.obolibrary.org/obo/GO_0022010))

#### Key Genes

- **CDK18**: [EXTERNAL] [DATA] CDK18 promotes OPC differentiation through ERK pathway activation, thereby increasing myelination rate in the CNS [PMID:31028571](https://pubmed.ncbi.nlm.nih.gov/31028571/). ([GO:0031643](http://purl.obolibrary.org/obo/GO_0031643))
- **MAG**: [INFERENCE] [INFERENCE] MAG stabilizes axon–glia adhesion and signals to the oligodendrocyte cytoskeleton to promote membrane wrapping and sheath maintenance during myelin assembly. ([GO:0032288](http://purl.obolibrary.org/obo/GO_0032288))
- **MYRF**: [INFERENCE] [INFERENCE] MYRF drives CNS myelination by binding myelin gene enhancers after autoproteolytic activation, coupling oligodendrocyte differentiation to high-output lipid and protein synthesis for sheath growth. ([GO:0022010](http://purl.obolibrary.org/obo/GO_0022010))
- **SOX10**: [INFERENCE] [INFERENCE] SOX10 orchestrates lineage-specific transcription that primes oligodendrocytes for myelin gene expression and collaborates with MYRF to sustain CNS myelination. ([GO:0022010](http://purl.obolibrary.org/obo/GO_0022010))
- **TPPP**: [INFERENCE] [INFERENCE] TPPP promotes microtubule assembly in differentiating oligodendrocytes, supporting process extension and membrane delivery required for myelin assembly. ([GO:0032288](http://purl.obolibrary.org/obo/GO_0032288))

#### Statistical Context

[DATA] Theme myelination is supported at FDR 4.49e-08 with 11/174 annotated genes at 19.7-fold enrichment relative to the background. [DATA] Specific leaves include positive regulation of myelination (6 genes, FDR 3.28e-05), myelin assembly (5 genes, FDR 8.41e-05), and CNS myelination (4 genes, FDR 7.70e-04).

---

### Theme 2: structural constituent of myelin sheath

**Summary:** structural constituent of myelin sheath ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Structural constituent of myelin sheath ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911)) captures proteins that physically stabilize multilamellar myelin within the broader membrane organization and myelination hierarchy. [INFERENCE] These proteins create liquid-ordered, low-cytoplasm membranes that minimize capacitance and enable high-velocity conduction along axons. [INFERENCE] Coordinated interactions among PLP1, MBP, MAL, and PLLP enforce adhesion and phase behavior that drive compaction and internodal stability.

#### Key Insights

- [GO-HIERARCHY] The molecular function term anchors the physical scaffold that myelination processes assemble and regulate. ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911))
- [INFERENCE] Lipid–protein cooperativity within compact myelin ensures mechanical resilience and low ion permeability critical for saltatory conduction. ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911))

#### Key Genes

- **MOBP**: [EXTERNAL] [EXTERNAL] MOBP helps organize myelin protein assemblies within raft-like domains to stabilize compact myelin architecture [PMID:12153479](https://pubmed.ncbi.nlm.nih.gov/12153479/). ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911))
- **PLP1**: [INFERENCE] [INFERENCE] PLP1 spans myelin bilayers and, together with other proteolipids, generates high-adhesion interfaces that support sheath compaction and long-term stability. ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911))
- **PLLP**: [EXTERNAL] [DATA] PLLP oligomerization promotes liquid-ordered membrane formation that supports compact myelin structure [PMID:26002055](https://pubmed.ncbi.nlm.nih.gov/26002055/). ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911))
- **MAL**: [EXTERNAL] [DATA] MAL is a raft-associated structural component of compact myelin membranes, marking and stabilizing the sheath architecture [PMID:12153479](https://pubmed.ncbi.nlm.nih.gov/12153479/). ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911))
- **MBP**: [EXTERNAL] [EXTERNAL] MBP drives cytoplasmic leaflet apposition by neutralizing negative charges on acidic lipids to compact myelin wraps [PMID:22524708](https://pubmed.ncbi.nlm.nih.gov/22524708/). ([GO:0019911](http://purl.obolibrary.org/obo/GO_0019911))

#### Statistical Context

[DATA] This function is highly enriched (FDR 1.16e-04, 5 genes, 51.4-fold), indicating concentrated structural investment in the sheath among input genes. [DATA] The constituent set includes MAL, MBP, MOBP, PLLP, and PLP1, matching canonical compact myelin architecture.

---

### Theme 3: synapse

**Summary:** synapse ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Synapse ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202)) situates pre- and postsynaptic specializations that coordinate vesicle cycling, receptor clustering, and actin remodeling within the neuronal communication hierarchy. [EXTERNAL] IL1RAPL1 promotes excitatory synapse formation through interactions with PTPδ and RhoGAP2, linking adhesion to Rho-family remodeling at spines [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). [INFERENCE] Endocytic scaffolds and Ras/Rac activators integrate membrane curvature with actin dynamics to tune vesicle retrieval and receptor trafficking essential for synaptic efficacy. [INFERENCE] Adhesion molecules such as protocadherins stabilize spine structure and maintain synaptic specificity during development and plasticity.

#### Key Insights

- [GO-HIERARCHY] The synapse term aggregates presynaptic exocytosis, postsynaptic receptor signaling, and cytoskeletal remodeling into a unified communication unit. ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))
- [EXTERNAL] Synaptogenic adhesion complexes recruit RhoGAPs to regulate actin at excitatory synapses, coupling adhesion to spine morphogenesis [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))

#### Key Genes

- **SH3GL3**: [EXTERNAL] [EXTERNAL] SH3GL3 (endophilin A1 family) couples membrane curvature generation to p140Cap-mediated actin stabilization, coordinating endocytosis and spine morphogenesis [PMID:25771685](https://pubmed.ncbi.nlm.nih.gov/25771685/). ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))
- **RASGRF2**: [EXTERNAL] [EXTERNAL] RASGRF2 activates Ras/Rap at spines to promote structural plasticity by driving actin rearrangements that support excitatory transmission [PMID:25771685](https://pubmed.ncbi.nlm.nih.gov/25771685/). ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))
- **ELMO1**: [EXTERNAL] [EXTERNAL] ELMO1 engages DOCK complexes to activate Rac1, promoting membrane ruffling and spine actin remodeling that supports excitatory synaptic signaling [PMID:25771685](https://pubmed.ncbi.nlm.nih.gov/25771685/). ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))
- **PCDH9**: [INFERENCE] [INFERENCE] PCDH9 mediates homophilic adhesion that stabilizes dendritic spines and organizes postsynaptic receptor fields to maintain synaptic specificity. ([GO:0045202](http://purl.obolibrary.org/obo/GO_0045202))

#### Statistical Context

[DATA] Synapse is enriched at FDR 2.11e-04 with 30 genes at 2.7-fold overrepresentation. [DATA] Theme membership spans presynaptic endocytosis adaptors, adhesion molecules, and small GTPase regulators that align with excitatory synapse formation evidence.

---

### Theme 4: protein localization to axon

**Summary:** protein localization to axon ([GO:0099612](http://purl.obolibrary.org/obo/GO_0099612))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Protein localization to axon ([GO:0099612](http://purl.obolibrary.org/obo/GO_0099612)) refines neuronal polarity within the neuron projection hierarchy by specifying selective delivery and anchorage at the axonal membrane. [INFERENCE] Ankyrin-G scaffolding at the axon initial segment and adhesion cues from contactins cooperate with polarized trafficking to position channels and adhesion complexes. [INFERENCE] Myelin-associated trafficking adaptors shape axonal membrane composition by sorting raft cargoes toward axon-specialized domains.

#### Key Insights

- [GO-HIERARCHY] Axonal protein localization is a child of neuron projection organization, ensuring domain-specific proteome assembly for excitability and conduction. ([GO:0099612](http://purl.obolibrary.org/obo/GO_0099612))
- [INFERENCE] Polarized exocytosis and membrane anchors synergize to retain channels and adhesion molecules at the axon initial segment and nodes. ([GO:0099612](http://purl.obolibrary.org/obo/GO_0099612))

#### Key Genes

- **UGT8**: [INFERENCE] [INFERENCE] UGT8-driven galactosylceramide synthesis supports axonal raft composition that favors targeting and retention of axonal proteins. ([GO:0099612](http://purl.obolibrary.org/obo/GO_0099612))
- **ANK3**: [INFERENCE] [INFERENCE] ANK3 scaffolds membrane proteins to the axon initial segment by linking channel complexes to the spectrin–actin cytoskeleton, reinforcing polarized localization. ([GO:0099612](http://purl.obolibrary.org/obo/GO_0099612))
- **MAL**: [INFERENCE] [INFERENCE] MAL directs raft-associated cargo through apical-like trafficking mechanisms adapted in glia-neuron interfaces to stabilize axonal protein domains. ([GO:0099612](http://purl.obolibrary.org/obo/GO_0099612))
- **CNTN2**: [INFERENCE] [INFERENCE] CNTN2 mediates axonal adhesive contacts that nucleate presynaptic assembly, indirectly reinforcing axonal protein retention near juxtaparanodes. ([GO:0099612](http://purl.obolibrary.org/obo/GO_0099612))

#### Statistical Context

[DATA] The process is sharply enriched (FDR 3.64e-04, 4 genes, 56.6-fold), indicating focused polarity mechanisms among the input set. [DATA] The gene composition points to lipid-driven sorting, scaffolding, and adhesion-based retention in axonal compartments.

---

### Theme 5: neuron projection

**Summary:** neuron projection ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Neuron projection ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005)) encompasses axons and dendrites, with leaves defining axon ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424)) and dendrite ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425)) as specialized subcompartments. [DATA] Axon is strongly enriched (19 genes, FDR 6.55e-06) and dendrite is also enriched (14 genes, FDR 1.32e-02), indicating broad polarity engagement. [DATA] CLDN11 is directly annotated to axon, supporting axonal specialization in this gene set [PMID:30734065](https://pubmed.ncbi.nlm.nih.gov/30734065/). [INFERENCE] Guidance receptors and actin nucleators coordinate extension and branching, while synaptogenic adhesion maintains compartment identity.

#### Key Insights

- [GO-HIERARCHY] Axon ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424)) and dendrite ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425)) specify polarized subdomains within neuron projection that host distinct trafficking and signaling machineries. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- [DATA] Direct axon annotation of tight junction-related components underscores membrane specialization along projecting neurites [PMID:30734065](https://pubmed.ncbi.nlm.nih.gov/30734065/). ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))

#### Key Genes

- **UNC5C**: [INFERENCE] [INFERENCE] UNC5C senses netrin gradients to remodel cytoskeleton via Rho GTPases, steering projection trajectories and stabilizing axon pathfinding. ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- **COBL**: [INFERENCE] [INFERENCE] COBL nucleates actin to drive filopodial protrusion and branching, shaping dendrite and axon arbor architecture. ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- **KIRREL3**: [INFERENCE] [INFERENCE] KIRREL3 mediates adhesive recognition that refines projection targeting and synapse partner choice within developing circuits. ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))
- **IL1RAPL1**: [EXTERNAL] [EXTERNAL] IL1RAPL1 scaffolds excitatory synapse components on projections, linking adhesion to structural maturation of neurites [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0043005](http://purl.obolibrary.org/obo/GO_0043005))

#### Statistical Context

[DATA] Neuron projection is enriched at FDR 5.27e-04 with 26 genes at 2.7-fold, with child terms axon and dendrite significantly overrepresented. [DATA] The breadth across axon and dendrite suggests coordinated polarity and arborization programs.

---

### Theme 6: internode region of axon

**Summary:** internode region of axon ([GO:0033269](http://purl.obolibrary.org/obo/GO_0033269))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The internode region of axon ([GO:0033269](http://purl.obolibrary.org/obo/GO_0033269)) is a specialized subdomain between nodes of Ranvier within the axonal compartment hierarchy. [INFERENCE] Internodal cytoskeleton remodeling and membrane compaction align to minimize capacitance and preserve conduction velocity under myelin. [DATA] Oligodendrocyte-derived cytoskeletal proteins shape sheath geometry and stiffness to withstand repetitive firing.

#### Key Insights

- [GO-HIERARCHY] Internodes represent a child structure of axon that integrates compact myelin and axonal cytoskeleton for efficient saltatory conduction. ([GO:0033269](http://purl.obolibrary.org/obo/GO_0033269))
- [INFERENCE] Microtubule and actin coordination inside the internode ensures stable sheath contact and axonal caliber maintenance. ([GO:0033269](http://purl.obolibrary.org/obo/GO_0033269))

#### Key Genes

- **ERMN**: [EXTERNAL] [DATA] ERMN (ermin) orchestrates oligodendrocyte cytoskeletal rearrangements required for internode formation and maturation [PMID:20934411](https://pubmed.ncbi.nlm.nih.gov/20934411/). ([GO:0033269](http://purl.obolibrary.org/obo/GO_0033269))
- **TUBB4A**: [INFERENCE] [INFERENCE] TUBB4A supports microtubule dynamics in myelinated axons and glia, stabilizing internodal architecture during maturation. ([GO:0033269](http://purl.obolibrary.org/obo/GO_0033269))
- **MBP**: [INFERENCE] [INFERENCE] MBP-driven compaction rigidifies internodal wraps, sustaining low-capacitance cable properties under the sheath. ([GO:0033269](http://purl.obolibrary.org/obo/GO_0033269))

#### Statistical Context

[DATA] This compact subdomain is highly enriched (FDR 5.27e-04, 3 genes, 84.8-fold), indicating a focused internodal specialization among input genes. [DATA] ERMN provides direct curated support for this structure.

---

### Theme 7: compact myelin

**Summary:** compact myelin ([GO:0043218](http://purl.obolibrary.org/obo/GO_0043218))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Compact myelin ([GO:0043218](http://purl.obolibrary.org/obo/GO_0043218)) defines the multilamellar, cytoplasm-extruded membrane stack enveloping internodes within the axon hierarchy. [INFERENCE] Electrostatic compaction and raft-driven adhesion lower membrane capacitance and stabilize the sheath under mechanical stress. [DATA] MAG localization and function within compact myelin link adhesion to sheath integrity.

#### Key Insights

- [GO-HIERARCHY] Compact myelin is a leaf structural compartment whose assembly depends on upstream myelin biogenesis and membrane organization. ([GO:0043218](http://purl.obolibrary.org/obo/GO_0043218))
- [EXTERNAL] MAG localization to compact myelin supports axon–glia adhesion essential for sheath stability [PMID:6200494](https://pubmed.ncbi.nlm.nih.gov/6200494/). ([GO:0043218](http://purl.obolibrary.org/obo/GO_0043218))

#### Key Genes

- **MAG**: [EXTERNAL] [DATA] MAG is resident in compact myelin where it supports structural stabilization of the sheath and axon–glia contact [PMID:6200494](https://pubmed.ncbi.nlm.nih.gov/6200494/). ([GO:0043218](http://purl.obolibrary.org/obo/GO_0043218))
- **PLLP**: [EXTERNAL] [DATA] PLLP oligomerization induces liquid-ordered domains that contribute to the biophysical state of compact myelin membranes [PMID:26002055](https://pubmed.ncbi.nlm.nih.gov/26002055/). ([GO:0043218](http://purl.obolibrary.org/obo/GO_0043218))
- **MBP**: [EXTERNAL] [EXTERNAL] MBP neutralizes membrane charges to drive tight apposition of myelin wraps, reinforcing compact myelin integrity [PMID:22524708](https://pubmed.ncbi.nlm.nih.gov/22524708/). ([GO:0043218](http://purl.obolibrary.org/obo/GO_0043218))

#### Statistical Context

[DATA] Compact myelin is strongly enriched (FDR 5.27e-04, 3 genes, 84.8-fold), matching structural myelin themes observed across the set. [DATA] The gene trio underscores adhesion, compaction, and membrane phase organization.

---

### Theme 8: apical plasma membrane

**Summary:** apical plasma membrane ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The apical plasma membrane ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324)) specifies one pole of polarized epithelial cells within the plasma membrane hierarchy. [DATA] LRP2 is curated at the apical membrane mediating ligand uptake, and MAL and PLD1 contribute to apical trafficking and brush border formation [PMID:23825075](https://pubmed.ncbi.nlm.nih.gov/23825075/); [PMID:22895261](https://pubmed.ncbi.nlm.nih.gov/22895261/); [PMID:22797597](https://pubmed.ncbi.nlm.nih.gov/22797597/). [DATA] ATP1B1 isoform distribution includes apical polarization in specific epithelia, linking ion pumping to domain identity [PMID:11193188](https://pubmed.ncbi.nlm.nih.gov/11193188/). [INFERENCE] Coordinated trafficking and lipid raft partitioning maintain apical microvilli and selective transport.

#### Key Insights

- [GO-HIERARCHY] Apical membrane identity emerges from polarized trafficking and scaffolding that segregate transporters and receptors from basolateral pools. ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))
- [EXTERNAL] Brush border morphogenesis couples cell polarity cues to actin-supported microvilli at the apical surface [PMID:22797597](https://pubmed.ncbi.nlm.nih.gov/22797597/). ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))

#### Key Genes

- **LRP2**: [EXTERNAL] [DATA] LRP2 (megalin) localizes apically to mediate endocytic uptake of ligands in proximal tubule epithelia [PMID:23825075](https://pubmed.ncbi.nlm.nih.gov/23825075/). ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))
- **MAL**: [EXTERNAL] [DATA] MAL (VIP17) directs apical vesicle transport and modulates epithelial cystogenesis and ciliogenesis, shaping apical domain organization [PMID:22895261](https://pubmed.ncbi.nlm.nih.gov/22895261/). ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))
- **PLD1**: [EXTERNAL] [DATA] PLD1 activity links apicobasal polarity to brush border formation by producing phosphatidic acid cues for actin-driven microvilli [PMID:22797597](https://pubmed.ncbi.nlm.nih.gov/22797597/). ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))
- **ATP1B1**: [EXTERNAL] [DATA] ATP1B1 shows apical membrane polarization in human prostate epithelium, coupling Na+/K+-ATPase activity to domain-specific transport [PMID:11193188](https://pubmed.ncbi.nlm.nih.gov/11193188/). ([GO:0016324](http://purl.obolibrary.org/obo/GO_0016324))

#### Statistical Context

[DATA] Apical membrane is enriched at FDR 5.54e-04 with 15 genes at 4.2-fold. [DATA] Multiple curated annotations support apical endocytosis and polarity-coupled cytoskeletal remodeling.

---

### Theme 9: DNA-templated transcription

**Summary:** DNA-templated transcription ([GO:0006351](http://purl.obolibrary.org/obo/GO_0006351))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] DNA-templated transcription ([GO:0006351](http://purl.obolibrary.org/obo/GO_0006351)) represents Pol II–driven gene expression programs upstream of lineage and functional specializations. [INFERENCE] Oligodendrocyte lineage factors integrate enhancer occupancy with chromatin state to drive myelin gene expression and membrane biogenesis. [INFERENCE] Brain-enriched repressors modulate neuronal differentiation timing by antagonizing retinoic acid response elements.

#### Key Insights

- [GO-HIERARCHY] General transcription provides the substrate for downstream regulatory terms that tune lineage specification and activity-dependent programs. ([GO:0006351](http://purl.obolibrary.org/obo/GO_0006351))
- [INFERENCE] Balance between activators and repressors gates transitions from progenitor to differentiated glial or neuronal states. ([GO:0006351](http://purl.obolibrary.org/obo/GO_0006351))

#### Key Genes

- **ST18**: [INFERENCE] [INFERENCE] ST18 functions as a transcriptional regulator modulating Pol II output in stress and developmental contexts to influence cell fate programs. ([GO:0006351](http://purl.obolibrary.org/obo/GO_0006351))
- **ZNF536**: [INFERENCE] [INFERENCE] ZNF536 binds genomic elements to repress RA-driven transcription, tempering neuronal differentiation kinetics. ([GO:0006351](http://purl.obolibrary.org/obo/GO_0006351))
- **SOX10**: [INFERENCE] [INFERENCE] SOX10 recruits co-factors to myelin gene enhancers, coupling DNA binding to transcriptional activation in oligodendrocyte lineage cells. ([GO:0006351](http://purl.obolibrary.org/obo/GO_0006351))
- **MYRF**: [INFERENCE] [INFERENCE] MYRF directly activates myelin gene expression after self-cleavage and nuclear entry, elevating transcriptional throughput for sheath formation. ([GO:0006351](http://purl.obolibrary.org/obo/GO_0006351))

#### Statistical Context

[DATA] The core transcription term is enriched at FDR 1.01e-03 (4 genes), indicating compact yet functionally coherent transcriptional drivers in the set. [DATA] Fold enrichment below 1 reflects a narrow but significant cluster consistent with focused lineage factors.

---

### Theme 10: perinuclear region of cytoplasm

**Summary:** perinuclear region of cytoplasm ([GO:0048471](http://purl.obolibrary.org/obo/GO_0048471))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The perinuclear region of cytoplasm ([GO:0048471](http://purl.obolibrary.org/obo/GO_0048471)) situates trafficking hubs and signaling endosomes adjacent to the nucleus within cellular compartment hierarchy. [DATA] Transferrin receptor pathways and Ebola GP pseudotype entry implicate clathrin-mediated endocytosis operating near the perinuclear space [PMID:20202662](https://pubmed.ncbi.nlm.nih.gov/20202662/); [PMID:15880641](https://pubmed.ncbi.nlm.nih.gov/15880641/). [DATA] APLP1 interactions with adrenergic receptors localize signaling complexes perinuclearly to tune G-protein outputs [PMID:16531006](https://pubmed.ncbi.nlm.nih.gov/16531006/). [INFERENCE] Lipid mediators and cyclic nucleotides processed perinuclearly enable rapid feedback to transcriptional programs.

#### Key Insights

- [GO-HIERARCHY] The perinuclear zone concentrates endosomal sorting and signaling close to chromatin for efficient signal-to-transcription coupling. ([GO:0048471](http://purl.obolibrary.org/obo/GO_0048471))
- [EXTERNAL] Viral and receptor trafficking evidence indicates active clathrin-mediated endocytosis converging perinuclearly [PMID:20202662](https://pubmed.ncbi.nlm.nih.gov/20202662/). ([GO:0048471](http://purl.obolibrary.org/obo/GO_0048471))

#### Key Genes

- **TF**: [EXTERNAL] [DATA] Transferrin receptor pathways localize perinuclearly during clathrin-mediated endocytosis and iron handling in trophoblast and model systems [PMID:20202662](https://pubmed.ncbi.nlm.nih.gov/20202662/); [PMID:15880641](https://pubmed.ncbi.nlm.nih.gov/15880641/). ([GO:0048471](http://purl.obolibrary.org/obo/GO_0048471))
- **APLP1**: [EXTERNAL] [DATA] APLP1 interacts with the α2A-adrenergic receptor to enhance perinuclear signaling that regulates adenylate cyclase inhibition [PMID:16531006](https://pubmed.ncbi.nlm.nih.gov/16531006/). ([GO:0048471](http://purl.obolibrary.org/obo/GO_0048471))
- **TPPP**: [EXTERNAL] [DATA] TPPP (p25alpha) accumulates perinuclearly and can stimulate α-synuclein aggregation, linking local protein quality control to neurodegenerative processes [PMID:15590652](https://pubmed.ncbi.nlm.nih.gov/15590652/). ([GO:0048471](http://purl.obolibrary.org/obo/GO_0048471))
- **APOD**: [EXTERNAL] [DATA] APOD modulates growth factor signaling by preventing ERK1/2 nuclear translocation, consistent with perinuclear signaling control [PMID:14551159](https://pubmed.ncbi.nlm.nih.gov/14551159/). ([GO:0048471](http://purl.obolibrary.org/obo/GO_0048471))

#### Statistical Context

[DATA] The compartment is enriched at FDR 2.41e-03 with 19 genes and 3.0-fold enrichment. [DATA] Curated entries emphasize endocytic routing and GPCR-associated signaling near the nucleus.

---

### Theme 11: regulation of DNA-templated transcription

**Summary:** regulation of DNA-templated transcription ([GO:0006355](http://purl.obolibrary.org/obo/GO_0006355))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 5.26e-03 · **Genes (9)**: FGFR2, MYRF, NKX6-2, RNF220, SEMA4D, SOX10, SPP1, ST18, ZNF536

---

### Theme 12: cell-cell adhesion

**Summary:** cell-cell adhesion ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Cell–cell adhesion ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609)) aggregates cadherin-, IgCAM-, and tight junction–mediated contacts that shape tissue architecture and circuit specificity. [EXTERNAL] Homotypic adhesion programs such as MEGF10-driven retinal mosaics demonstrate spacing logic in neural tissues [PMID:22407321](https://pubmed.ncbi.nlm.nih.gov/22407321/). [DATA] CTNNA3 strengthens adherens junction linkage to actin, while platelet proteome data connect CSRP1 to integrin-dependent adhesive function [PMID:11590244](https://pubmed.ncbi.nlm.nih.gov/11590244/); [PMID:23382103](https://pubmed.ncbi.nlm.nih.gov/23382103/). [INFERENCE] Axoglial adhesion coordinates paranodal alignment to maintain conduction fidelity.

#### Key Insights

- [GO-HIERARCHY] Adhesion underlies higher-order tissue organization and is upstream of synaptogenesis and barrier formation. ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- [EXTERNAL] Homotypic adhesion cascades enforce neuronal spacing and connectivity rules in the retina [PMID:22407321](https://pubmed.ncbi.nlm.nih.gov/22407321/). ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))

#### Key Genes

- **CDH19**: [INFERENCE] [INFERENCE] CDH19 mediates homophilic cadherin binding to stabilize cell–cell junctions important for neural tissue patterning. ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **CTNNA3**: [EXTERNAL] [DATA] CTNNA3 (αT-catenin) links cadherin complexes to actin to enhance strong intercellular adhesion in excitable tissues [PMID:11590244](https://pubmed.ncbi.nlm.nih.gov/11590244/). ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **CSRP1**: [EXTERNAL] [DATA] CSRP1 is implicated in integrin-dependent adhesion and aggregation programs in platelets, highlighting cytoskeletal–adhesion coupling [PMID:23382103](https://pubmed.ncbi.nlm.nih.gov/23382103/). ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))
- **CLDN11**: [INFERENCE] [INFERENCE] CLDN11 forms tight junction strands that reinforce cell–cell adhesion and regulate paracellular ion flow in specialized barriers. ([GO:0098609](http://purl.obolibrary.org/obo/GO_0098609))

#### Statistical Context

[DATA] Adhesion is enriched at FDR 6.89e-03 with 16 genes at 3.5-fold. [DATA] The set spans cadherin linkers, tight junction proteins, and axoglial adhesion organizers.

---

### Theme 13: membrane organization

**Summary:** membrane organization ([GO:0061024](http://purl.obolibrary.org/obo/GO_0061024))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Membrane organization ([GO:0061024](http://purl.obolibrary.org/obo/GO_0061024)) assembles and remodels bilayers, rafts, and curvature to support trafficking and signaling hierarchies. [DATA] Phospholipid flippase ATP8A1 maintains lipid asymmetry captured by curated structural intermediates and functional translocation annotations [PMID:31416931](https://pubmed.ncbi.nlm.nih.gov/31416931/); [PMID:21914794](https://pubmed.ncbi.nlm.nih.gov/21914794/). [DATA] ABCA2 modulates ceramide handling impacting membrane domains, and CNTN2 contributes to presynaptic membrane organization [PMID:24201375](https://pubmed.ncbi.nlm.nih.gov/24201375/); [PMID:23518707](https://pubmed.ncbi.nlm.nih.gov/23518707/). [INFERENCE] Actin–membrane coupling factors coordinate endocytosis and protrusion to tune protein localization and receptor signaling.

#### Key Insights

- [GO-HIERARCHY] Lipid translocation and raft assembly define mesoscale membrane patterning that upstreams vesicle traffic and receptor clustering. ([GO:0061024](http://purl.obolibrary.org/obo/GO_0061024))
- [DATA] Structural and biochemical evidence for ATP8A1 flippase activity anchors asymmetric bilayer maintenance in this theme [PMID:31416931](https://pubmed.ncbi.nlm.nih.gov/31416931/); [PMID:21914794](https://pubmed.ncbi.nlm.nih.gov/21914794/). ([GO:0061024](http://purl.obolibrary.org/obo/GO_0061024))

#### Key Genes

- **ATP8A1**: [EXTERNAL] [DATA] ATP8A1 flips aminophospholipids to the cytoplasmic leaflet, preserving asymmetry that governs trafficking and signaling domain formation [PMID:31416931](https://pubmed.ncbi.nlm.nih.gov/31416931/); [PMID:21914794](https://pubmed.ncbi.nlm.nih.gov/21914794/). ([GO:0061024](http://purl.obolibrary.org/obo/GO_0061024))
- **ABCA2**: [EXTERNAL] [DATA] ABCA2 regulates plasma membrane cholesterol esterification via sphingolipid metabolism, reshaping membrane microdomains and organization [PMID:24201375](https://pubmed.ncbi.nlm.nih.gov/24201375/). ([GO:0061024](http://purl.obolibrary.org/obo/GO_0061024))
- **CNTN2**: [EXTERNAL] [DATA] CNTN2 supports presynaptic membrane organization, stabilizing adhesive scaffolds that pattern release sites [PMID:23518707](https://pubmed.ncbi.nlm.nih.gov/23518707/). ([GO:0061024](http://purl.obolibrary.org/obo/GO_0061024))
- **FA2H**: [INFERENCE] [INFERENCE] FA2H-generated 2-hydroxylated sphingolipids promote ordered membrane packing that supports raft stability in myelin and neurons. ([GO:0061024](http://purl.obolibrary.org/obo/GO_0061024))

#### Statistical Context

[DATA] Membrane organization is enriched at FDR 7.35e-03 with 17 genes at 3.3-fold. [DATA] Multiple curated lipid-handling mechanisms converge on bilayer asymmetry and raft formation.

---

### Theme 14: nucleoplasm

**Summary:** nucleoplasm ([GO:0005654](http://purl.obolibrary.org/obo/GO_0005654))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The nucleoplasm ([GO:0005654](http://purl.obolibrary.org/obo/GO_0005654)) hosts transcriptional and signaling machineries within the nuclear compartment hierarchy. [INFERENCE] Phosphoinositide kinases and calcium sensors in the nucleoplasm modulate chromatin–transcription coupling and stress responses. [INFERENCE] Nuclear shuttling GEFs interface cytoskeletal cues with transcriptional outputs by positioning Ras/Rap signaling near chromatin.

#### Key Insights

- [GO-HIERARCHY] Nucleoplasmic localization integrates signaling with gene regulation proximal to chromatin. ([GO:0005654](http://purl.obolibrary.org/obo/GO_0005654))
- [INFERENCE] Local lipid and ion signaling within the nucleoplasm can gate transcription factor accessibility and activity. ([GO:0005654](http://purl.obolibrary.org/obo/GO_0005654))

#### Key Genes

- **PIP4K2A**: [INFERENCE] [INFERENCE] PIP4K2A shapes nucleoplasmic phosphoinositide pools to tune signal-regulated transcriptional events. ([GO:0005654](http://purl.obolibrary.org/obo/GO_0005654))
- **SGK1**: [INFERENCE] [INFERENCE] SGK1 relays stress and ion transport signals to nuclear targets to modulate survival and transcriptional programs. ([GO:0005654](http://purl.obolibrary.org/obo/GO_0005654))
- **RAPGEF5**: [INFERENCE] [INFERENCE] RAPGEF5 activates Rap near the nucleus to couple membrane and cytoskeletal status to gene regulatory pathways. ([GO:0005654](http://purl.obolibrary.org/obo/GO_0005654))
- **KLK6**: [INFERENCE] [INFERENCE] KLK6 may process nuclear or perinuclear substrates that influence cell cycle and apoptotic signaling impacting transcriptional states. ([GO:0005654](http://purl.obolibrary.org/obo/GO_0005654))

#### Statistical Context

[DATA] Nucleoplasm is enriched at FDR 7.93e-03 with 13 genes at 0.4-fold due to focused but significant nuclear-localized factors. [DATA] The set suggests signaling–transcription coupling hubs.

---

### Theme 15: Ras protein signal transduction

**Summary:** Ras protein signal transduction ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Ras protein signal transduction ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265)) places GEFs, effectors, and lipid enzymes upstream of MAPK and actin remodeling cascades. [INFERENCE] Neuronal GEFs convert synaptic Ca2+/GPCR cues into Ras-GTP to drive spine plasticity and neurite growth. [DATA] PLD1-generated phosphatidic acid supports Ras-dependent chemotaxis signaling, linking lipid metabolism to small GTPase activation [PMID:10848592](https://pubmed.ncbi.nlm.nih.gov/10848592/).

#### Key Insights

- [GO-HIERARCHY] Ras signaling integrates receptor inputs to control transcription and cytoskeletal programs impacting migration and plasticity. ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265))
- [DATA] Lipid second messengers from PLD1 feed into Ras-dependent chemotactic signaling modules [PMID:10848592](https://pubmed.ncbi.nlm.nih.gov/10848592/). ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265))

#### Key Genes

- **RASGRF2**: [INFERENCE] [INFERENCE] RASGRF2 couples Ca2+ influx to Ras activation at synapses, enabling activity-dependent remodeling. ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265))
- **RASGRP3**: [INFERENCE] [INFERENCE] RASGRP3 activates Ras downstream of diacylglycerol and Ca2+, coordinating motility and growth signals. ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265))
- **RASGRF1**: [INFERENCE] [INFERENCE] RASGRF1 integrates receptor signals to activate Ras during neurite outgrowth and learning-related plasticity. ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265))
- **RAPGEF5**: [INFERENCE] [INFERENCE] RAPGEF5 interfaces Rap–Ras crosstalk to fine-tune MAPK outputs during chemotaxis and differentiation. ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265))
- **PLD1**: [EXTERNAL] [DATA] PLD1-derived phosphatidic acid supports Ras-dependent chemotactic responses in myoblasts [PMID:10848592](https://pubmed.ncbi.nlm.nih.gov/10848592/). ([GO:0007265](http://purl.obolibrary.org/obo/GO_0007265))

#### Statistical Context

[DATA] Ras signaling is enriched at FDR 1.15e-02 with 6 genes at 10.1-fold, indicating concentrated GEF and lipid effector involvement. [DATA] Evidence ties lipid synthesis to Ras-module activation.

---

### Theme 16: transmembrane transport

**Summary:** transmembrane transport ([GO:0055085](http://purl.obolibrary.org/obo/GO_0055085))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.21e-02 · **Genes (27)**: ABCA2, ABCA6, ABCA8, ANO4, ATP1B1, ATP8A1, BEST1, BOK, CLCA4, GJB1, KCNK1, KCNMB4, LRP2, PIEZO2, PLCL1 … (+12 more)

---

### Theme 17: transporter activity

**Summary:** transporter activity ([GO:0005215](http://purl.obolibrary.org/obo/GO_0005215))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.23e-02 · **Genes (28)**: ABCA2, ABCA6, ABCA8, ANO4, APOD, ATP1B1, ATP8A1, BEST1, BOK, CLCA4, GJB1, KCNK1, KCNMB4, LRP2, OSBPL1A … (+13 more)

---

### Theme 18: cell surface

**Summary:** cell surface ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Cell surface ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986)) aggregates membrane proteins and ectodomains that sense, adhere, and transport at the extracellular interface. [DATA] Quantitative glycoproteomics links Dab2-dependent endocytosis to surface levels of ITGA2 and CLDND1-associated cargo, and GLDN mutations highlight nodal adhesion at the surface [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/); [PMID:23658023](https://pubmed.ncbi.nlm.nih.gov/23658023/). [INFERENCE] Coordinated receptor–integrin crosstalk tunes migration, survival, and synapse organization by regulating surface residency.

#### Key Insights

- [GO-HIERARCHY] The cell surface is the operational plane for adhesion, signaling, and transport, upstream of endocytic and signaling cascades. ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- [DATA] Surface proteome remodeling via Dab2-integrin modules demonstrates dynamic control of adhesion receptors [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Key Genes

- **CLDND1**: [EXTERNAL] [DATA] CLDND1 participates in Dab2-linked endocytic sorting impacting cell surface cargo composition in polarized cells [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **GLDN**: [EXTERNAL] [DATA] GLDN (gliomedin) functions at the surface to organize nodes of Ranvier; mutations disrupt nodal adhesion and development [PMID:23658023](https://pubmed.ncbi.nlm.nih.gov/23658023/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **ITGA2**: [EXTERNAL] [DATA] ITGA2 surface abundance is regulated by Dab2-dependent endocytosis and is linked to survival programs in epithelial contexts [PMID:19581412](https://pubmed.ncbi.nlm.nih.gov/19581412/); [PMID:23658023](https://pubmed.ncbi.nlm.nih.gov/23658023/); [PMID:23382103](https://pubmed.ncbi.nlm.nih.gov/23382103/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **HHIP**: [INFERENCE] [INFERENCE] HHIP modulates ligand–receptor availability at the cell surface to tune morphogen signaling and adhesion-dependent migration. ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Statistical Context

[DATA] Cell surface is enriched at FDR 1.32e-02 with 17 genes at 2.8-fold. [DATA] Curated entries span adhesion, receptor signaling, and nodal organization.

---

### Theme 19: juxtaparanode region of axon

**Summary:** juxtaparanode region of axon ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] The juxtaparanode region of axon ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224)) defines a myelinated axonal subdomain housing Kv channels adjacent to paranodes. [INFERENCE] Adhesion complexes bridge axon–glia at juxtaparanodes to cluster K+ channels, stabilizing repolarization and preventing ectopic excitation. [INFERENCE] MAGUK scaffolds integrate channel complexes with cytoskeleton to confine conductances to this domain.

#### Key Insights

- [GO-HIERARCHY] Juxtaparanodes are a leaf axonal compartment that refine ionic channel distribution for high-fidelity conduction. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))
- [INFERENCE] Contactin–MAGUK networks help lock Kv channels juxtaparanoidally to shape action potential waveforms. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))

#### Key Genes

- **LGI3**: [INFERENCE] [INFERENCE] LGI3 contributes to K+ channel clustering and stabilization at juxtaparanodes by engaging extracellular scaffolds. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))
- **DLG2**: [INFERENCE] [INFERENCE] DLG2 organizes juxtaparanodal channel complexes via PDZ-mediated scaffolding to the underlying cytoskeleton. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))
- **CNTN2**: [INFERENCE] [INFERENCE] CNTN2 supports axoglial contacts at juxtaparanodes that promote Kv channel enrichment and conduction reliability. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))

#### Statistical Context

[DATA] The juxtaparanodal compartment is enriched at FDR 1.37e-02 with 3 genes at 28.3-fold. [DATA] Gene composition points to adhesion–scaffold coordination of K+ channel domains.

---

### Theme 20: basolateral plasma membrane

**Summary:** basolateral plasma membrane ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] The basolateral plasma membrane ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323)) complements the apical domain to establish epithelial polarity and directional transport. [DATA] BEST1 localizes basolaterally in RPE to conduct Cl−, ANK3 supports basolateral targeting/anchorage, and ERBB3 signals basolaterally via HER2 heterodimers [PMID:26200502](https://pubmed.ncbi.nlm.nih.gov/26200502/); [PMID:21330666](https://pubmed.ncbi.nlm.nih.gov/21330666/); [PMID:15611082](https://pubmed.ncbi.nlm.nih.gov/15611082/); [PMID:12646923](https://pubmed.ncbi.nlm.nih.gov/12646923/). [INFERENCE] Polarized cargo motors and scaffolds enforce domain-selective residence of transporters and receptors.

#### Key Insights

- [GO-HIERARCHY] Basolateral identity specifies receptor and transporter localization for vectorial transport and signaling distinct from apical pools. ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323))
- [DATA] Basolateral BEST1 and ERBB3 highlight ion transport and growth factor signaling specialized to this domain [PMID:26200502](https://pubmed.ncbi.nlm.nih.gov/26200502/); [PMID:12646923](https://pubmed.ncbi.nlm.nih.gov/12646923/). ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323))

#### Key Genes

- **BEST1**: [EXTERNAL] [DATA] BEST1 is a basolateral Cl− channel in RPE; mutations disrupt anion conductance and lead to bestrophinopathies [PMID:26200502](https://pubmed.ncbi.nlm.nih.gov/26200502/); [PMID:21330666](https://pubmed.ncbi.nlm.nih.gov/21330666/); [PMID:19853238](https://pubmed.ncbi.nlm.nih.gov/19853238/). ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323))
- **ANK3**: [EXTERNAL] [DATA] ANK3 (ankyrin-G) anchors and targets basolateral membrane proteins via cytoskeletal linkage in polarized epithelia [PMID:15611082](https://pubmed.ncbi.nlm.nih.gov/15611082/). ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323))
- **ERBB3**: [EXTERNAL] [DATA] ERBB3 is enriched at the basolateral surface where heregulin engagement and HER2 dimerization activate downstream signaling [PMID:12646923](https://pubmed.ncbi.nlm.nih.gov/12646923/). ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323))
- **SLCO1A2**: [INFERENCE] [INFERENCE] SLCO1A2 contributes to basolateral uptake of organic anions to support trans-epithelial flux in polarized cells. ([GO:0016323](http://purl.obolibrary.org/obo/GO_0016323))

#### Statistical Context

[DATA] Basolateral membrane is enriched at FDR 1.62e-02 with 10 genes at 4.1-fold. [DATA] Evidence spans channel localization, scaffolding, and receptor signaling.

---

### Theme 21: monoatomic ion transport

**Summary:** monoatomic ion transport ([GO:0006811](http://purl.obolibrary.org/obo/GO_0006811))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 2.00e-02 · **Genes (22)**: ANO4, ATP1B1, ATP8A1, BEST1, CLCA4, FTH1, KCNK1, KCNMB4, LRP2, PIEZO2, PLCL1, PLLP, SGK1, SLC22A15, SLC24A2 … (+7 more)

---

### Theme 22: cytoskeleton

**Summary:** cytoskeleton ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 2.12e-02 · **Genes (22)**: ANK3, ANLN, COBL, CTNNA3, DLC1, ERMN, FRMD4B, GSN, KIF6, LDB3, MAP7, MTUS1, MYO1D, PLEKHH1, SEPTIN4 … (+7 more)

---

### Theme 23: sphingolipid metabolic process

**Summary:** sphingolipid metabolic process ([GO:0006665](http://purl.obolibrary.org/obo/GO_0006665))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 2.19e-02 · **Genes (8)**: ABCA2, ABCA8, ELOVL7, ENPP2, FA2H, PLPP2, ST6GALNAC3, UGT8

---

### Theme 24: nuclear protein-containing complex

**Summary:** nuclear protein-containing complex ([GO:0140513](http://purl.obolibrary.org/obo/GO_0140513))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Nuclear protein-containing complex ([GO:0140513](http://purl.obolibrary.org/obo/GO_0140513)) specifies multiprotein assemblies operating within the nucleus. [INFERENCE] Cytoskeleton–nucleus coupling factors influence complex positioning and stability, linking mechanical status to gene regulation. [INFERENCE] Assembly dynamics here modulate transcription and chromatin remodeling efficiency.

#### Key Insights

- [GO-HIERARCHY] Nuclear complexes coordinate transcription and genome maintenance within the nuclear compartment hierarchy. ([GO:0140513](http://purl.obolibrary.org/obo/GO_0140513))
- [INFERENCE] Mechanical cues transmitted from cytoskeleton can stabilize nuclear complexes and tune their activity. ([GO:0140513](http://purl.obolibrary.org/obo/GO_0140513))

#### Key Genes

- **CLMN**: [INFERENCE] [INFERENCE] CLMN likely interfaces with actin networks to support nuclear complex positioning and functional stability. ([GO:0140513](http://purl.obolibrary.org/obo/GO_0140513))

#### Statistical Context

[DATA] This compact theme appears with 1 gene at FDR 2.19e-02, reflecting a focused nuclear complex linkage. [DATA] Although few genes, the term anchors nuclear functional assemblies.

---

### Theme 25: DNA binding

**Summary:** DNA binding ([GO:0003677](http://purl.obolibrary.org/obo/GO_0003677))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 2.78e-02 · **Genes (6)**: MYRF, NKX6-2, OTUD7A, SOX10, ST18, ZNF536

---

### Theme 26: regulation of oligodendrocyte differentiation

**Summary:** regulation of oligodendrocyte differentiation ([GO:0048713](http://purl.obolibrary.org/obo/GO_0048713))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of oligodendrocyte differentiation ([GO:0048713](http://purl.obolibrary.org/obo/GO_0048713)) refines the glial lineage hierarchy upstream of myelination. [INFERENCE] Cytoskeletal effectors within Wnt pathways and membrane organizers modulate timing of OPC maturation into myelinating oligodendrocytes. [INFERENCE] Master transcription factors integrate these cues to trigger myelin gene cascades and membrane biogenesis.

#### Key Insights

- [GO-HIERARCHY] Differentiation control sets the stage for downstream myelin assembly and compact sheath formation. ([GO:0048713](http://purl.obolibrary.org/obo/GO_0048713))
- [INFERENCE] Wnt–cytoskeleton coupling and membrane dynamics provide rate control over lineage progression. ([GO:0048713](http://purl.obolibrary.org/obo/GO_0048713))

#### Key Genes

- **DAAM2**: [INFERENCE] [INFERENCE] DAAM2 links Wnt signals to actin remodeling to promote OPC maturation toward myelinating phenotypes. ([GO:0048713](http://purl.obolibrary.org/obo/GO_0048713))
- **OPALIN**: [INFERENCE] [INFERENCE] OPALIN modulates oligodendrocyte membrane organization, supporting the transition to a myelinating state. ([GO:0048713](http://purl.obolibrary.org/obo/GO_0048713))
- **MYRF**: [INFERENCE] [INFERENCE] MYRF activates oligodendrocyte differentiation by turning on myelin gene networks after nuclear activation. ([GO:0048713](http://purl.obolibrary.org/obo/GO_0048713))

#### Statistical Context

[DATA] The differentiation regulator theme is enriched at FDR 3.02e-02 with 4 genes at 16.2-fold. [DATA] Despite small gene count, fold enrichment indicates focused lineage control.

---

### Theme 27: neuronal cell body

**Summary:** neuronal cell body ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Neuronal cell body ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025)) frames soma-localized biosynthesis and signaling hubs within neuronal compartment hierarchy. [INFERENCE] Microtubule and actin regulators maintain somatic organelle distribution and support polarized trafficking to neurites. [INFERENCE] Cyclic nucleotide phosphodiesterases and GPCR signaling modulators in soma tune excitability and plasticity upstream of axodendritic outputs.

#### Key Insights

- [GO-HIERARCHY] Somatic organization supplies proteins and lipids to projections and integrates second-messenger control of neuronal state. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- [INFERENCE] Cytoskeletal stability in soma underpins reliable long-range transport and neuronal health. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))

#### Key Genes

- **TUBB4A**: [INFERENCE] [INFERENCE] TUBB4A supports somatic microtubule networks that organize organelles and enable cargo flow into neurites. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **PDE1A**: [INFERENCE] [INFERENCE] PDE1A degrades cAMP/cGMP in soma to shape kinase signaling that controls excitability and transcriptional responses. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **ERMN**: [INFERENCE] [INFERENCE] ERMN stabilizes somatic cytoskeletal interfaces in oligodendrocyte-lineage neurons, supporting cell body integrity. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **LPAR1**: [INFERENCE] [INFERENCE] LPAR1 signaling in neuron soma engages Rho–PI3K pathways to support survival and readiness for process extension. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))

#### Statistical Context

[DATA] Neuronal cell body is enriched at FDR 3.05e-02 with 11 genes at 3.4-fold. [DATA] The composition highlights cytoskeletal maintenance and second-messenger regulation in soma.

---

## Hub Genes

- **CNTN2**: [EXTERNAL] [EXTERNAL] CNTN2 organizes presynaptic membranes through neuron–neuron adhesion, enhancing synaptic specificity and stability [PMID:23518707](https://pubmed.ncbi.nlm.nih.gov/23518707/). [INFERENCE] By bridging axoglial contacts at juxtaparanodes, CNTN2 helps cluster Kv channels and supports conduction fidelity across projection and synapse themes.
- **MBP**: [EXTERNAL] [EXTERNAL] MBP compacts myelin by neutralizing membrane charge and stabilizing lipid bilayer apposition, sustaining rapid conduction [PMID:22524708](https://pubmed.ncbi.nlm.nih.gov/22524708/). [INFERENCE] Its biophysical role links compact myelin, internodes, and axon-associated synaptic reliability by minimizing capacitive load.
- **ANK3**: [EXTERNAL] [EXTERNAL] ANK3 stabilizes ankyrin-G–dependent complexes at polarized membranes, enabling precise axonal protein localization and domain integrity [PMID:15611082](https://pubmed.ncbi.nlm.nih.gov/15611082/). [INFERENCE] This scaffolding coordinates neuron projection polarity with synaptic and basolateral membrane organization themes.
- **MYRF**: [INFERENCE] [INFERENCE] MYRF activates myelin gene programs after autoproteolysis and nuclear entry, coupling oligodendrocyte differentiation to sheath biogenesis across myelination-related themes. [INFERENCE] Its transcriptional control aligns membrane organization and lipid synthesis to meet myelin production demands.
- **ATP1B1**: [EXTERNAL] [DATA] ATP1B1 supports Na+/K+-ATPase activity that also imports protons, maintaining electrochemical gradients and impacting transport across apical/basolateral domains [PMID:24688018](https://pubmed.ncbi.nlm.nih.gov/24688018/); [PMID:11193188](https://pubmed.ncbi.nlm.nih.gov/11193188/); [PMID:19683723](https://pubmed.ncbi.nlm.nih.gov/19683723/). [INFERENCE] Gradient control connects transporter activity with synaptic excitability and membrane microdomain organization.
- **PLLP**: [EXTERNAL] [EXTERNAL] PLLP oligomerizes to induce liquid-ordered membranes that facilitate compact myelin formation and stability [PMID:26002055](https://pubmed.ncbi.nlm.nih.gov/26002055/). [INFERENCE] By shaping raft composition, PLLP links structural myelin themes with membrane organization and apical trafficking logic in glia.
- **ABCA2**: [EXTERNAL] [DATA] ABCA2 modulates ceramide handling and sphingolipid metabolism, influencing membrane domain organization and myelin-related lipid balance [PMID:24201375](https://pubmed.ncbi.nlm.nih.gov/24201375/); [PMID:26510981](https://pubmed.ncbi.nlm.nih.gov/26510981/). [INFERENCE] Lipid transport roles connect transporter activity and membrane organization with myelination.
- **SOX10**: [EXTERNAL] [DATA] SOX10 binds sequence-specific DNA with methylation-sensitive preferences, enabling myelin gene enhancer selection [PMID:28473536](https://pubmed.ncbi.nlm.nih.gov/28473536/). [INFERENCE] As a lineage TF, SOX10 coordinates transcription themes with myelination and nucleoplasmic regulation.
- **MAL**: [EXTERNAL] [DATA] MAL is a structural myelin component and apical vesicle transport factor that organizes compact membranes and polarity [PMID:12153479](https://pubmed.ncbi.nlm.nih.gov/12153479/); [PMID:22895261](https://pubmed.ncbi.nlm.nih.gov/22895261/). [INFERENCE] MAL links myelin structure with protein localization and epithelial-like trafficking logic in glia.
- **LPAR1**: [INFERENCE] [INFERENCE] LPAR1 activates Rho/PI3K cascades upon LPA binding to promote neuronal survival, myelination support, and synaptic maintenance across neuron projection and synapse themes. [INFERENCE] Its GPCR signaling integrates surface cues with cytoskeletal and transcriptional responses.
- **DLG2**: [INFERENCE] [INFERENCE] DLG2 scaffolds postsynaptic complexes and juxtaparanodal channels, coordinating receptor clustering with cytoskeletal anchorage across synapse and axonal subdomain themes. [INFERENCE] This MAGUK integrates adhesion and signaling with membrane organization.
- **IL1RAPL1**: [EXTERNAL] [EXTERNAL] IL1RAPL1 promotes excitatory synapse formation via PTPδ and RhoGAP2 interactions, coupling adhesion to actin remodeling [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). [INFERENCE] Its synaptogenic role bridges synapse, neuron projection, and cell–cell adhesion themes.
- **ATP8A1**: [EXTERNAL] [DATA] ATP8A1 flips aminophospholipids to the inner leaflet, preserving asymmetry essential for synaptic and trafficking membrane organization [PMID:31416931](https://pubmed.ncbi.nlm.nih.gov/31416931/); [PMID:21914794](https://pubmed.ncbi.nlm.nih.gov/21914794/). [INFERENCE] Lipid flipping couples transporter activity with synapse and membrane organization themes.
- **LRP2**: [EXTERNAL] [DATA] LRP2 mediates apical endocytosis of diverse ligands, supporting polarized uptake in epithelia and impacting neurite-supportive nutrient flux [PMID:23825075](https://pubmed.ncbi.nlm.nih.gov/23825075/). [INFERENCE] Its transport role connects apical membrane, transporter activity, and neuron projection maintenance.
- **KCNK1**: [EXTERNAL] [DATA] KCNK1 sets resting potential via K+ leak and can conduct Na+ in hypokalemia, tuning excitability across projection and synapse contexts [PMID:22282804](https://pubmed.ncbi.nlm.nih.gov/22282804/); [PMID:21653227](https://pubmed.ncbi.nlm.nih.gov/21653227/). [INFERENCE] Channel versatility links monoatomic ion transport with transporter themes and neuronal compartments.
- **SLCO1A2**: [EXTERNAL] [DATA] SLCO1A2 transports amphipathic organic anions in a pH-dependent manner at polarized membranes, impacting extracellular cue uptake [PMID:19129463](https://pubmed.ncbi.nlm.nih.gov/19129463/); [PMID:10873595](https://pubmed.ncbi.nlm.nih.gov/10873595/). [INFERENCE] Its basolateral/apical roles connect transporter activity with epithelial polarity themes.
- **SLCO3A1**: [EXTERNAL] [DATA] SLCO3A1 transports prostaglandins and organic anions, modulating paracrine signaling across polarized membranes [PMID:10873595](https://pubmed.ncbi.nlm.nih.gov/10873595/); [PMID:19129463](https://pubmed.ncbi.nlm.nih.gov/19129463/). [INFERENCE] This positions SLCO3A1 at the interface of transporter activity and cell surface signaling.
- **RNF220**: [EXTERNAL] [DATA] RNF220 monoubiquitylates developmental TFs to enhance Pol II transcription in noradrenergic neuron development, linking transcriptional regulation to neuronal phenotypes [PMID:32094113](https://pubmed.ncbi.nlm.nih.gov/32094113/). [INFERENCE] It bridges nucleoplasmic regulation with myelination and synaptic maturation programs.
- **UNC5C**: [INFERENCE] [INFERENCE] UNC5C guides neuron projections via netrin signaling to remodel cytoskeleton and stabilize synapse formation at cell surfaces. [INFERENCE] Its role spans neuron projection, synapse, and cell surface themes by coupling guidance to adhesion.
- **KCNMB4**: [INFERENCE] [INFERENCE] KCNMB4 modulates BK channel gating in response to Ca2+, shaping neurotransmitter release and excitability under monoatomic ion transport and synapse themes. [INFERENCE] Accessory subunit control links transporter activity with synaptic physiology.

## Overall Summary

[DATA] The analysis of 200 input genes with 174 annotated yielded 77 enriched terms organized into 27 themes, including 31 leaf terms under FDR 0.05.

[GO-HIERARCHY] A dominant axis spans myelination and compact myelin structures, nested within neuron projection and axonal subdomains, indicating coordinated sheath assembly atop polarized neuronal architecture.

[INFERENCE] Lipid handling and membrane organization converge with transporter activity to maintain bilayer asymmetry, electrical gradients, and domain-specific trafficking essential for synaptic and myelin function.

[INFERENCE] Transcriptional controllers (SOX10, MYRF, ZNF536, RNF220) align nucleoplasmic regulation with lineage progression to oligodendrocyte maturation and neuronal plasticity.

[DATA] Hub genes appearing across 3+ themes (n=20 reported here) connect synapse, membrane polarity, ion transport, and myelin structure, highlighting systems-level coordination across cellular compartments and processes.

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

