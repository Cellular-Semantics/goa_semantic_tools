# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_2_themes.csv](Cluster_2_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-synapse-organization) | [synapse organization](#theme-1-synapse-organization) [GO:0050808](http://purl.obolibrary.org/obo/GO_0050808) | BP | 1.51e-09 | 29 | FDR<0.01 |
| [2](#theme-2-regulation-of-membrane-potential) | [regulation of membrane potential](#theme-2-regulation-of-membrane-potential) [GO:0042391](http://purl.obolibrary.org/obo/GO_0042391) | BP | 2.26e-08 | 22 | FDR<0.01 |
| [3](#theme-3-postsynapse) | [postsynapse](#theme-3-postsynapse) [GO:0098794](http://purl.obolibrary.org/obo/GO_0098794) | CC | 3.46e-08 | 28 | FDR<0.01 |
| [4](#theme-4-schaffer-collateral---ca1-synapse) | [Schaffer collateral - CA1 synapse](#theme-4-schaffer-collateral---ca1-synapse) [GO:0098685](http://purl.obolibrary.org/obo/GO_0098685) | CC | 1.46e-07 | 11 | FDR<0.01 |
| [5](#theme-5-axon) | [axon](#theme-5-axon) [GO:0030424](http://purl.obolibrary.org/obo/GO_0030424) | CC | 9.83e-07 | 19 | FDR<0.01 |
| [6](#theme-6-monoatomic-ion-channel-complex) | [monoatomic ion channel complex](#theme-6-monoatomic-ion-channel-complex) [GO:0034702](http://purl.obolibrary.org/obo/GO_0034702) | CC | 2.53e-06 | 17 | FDR<0.01 |
| [7](#theme-7-neuronal-cell-body) | [neuronal cell body](#theme-7-neuronal-cell-body) [GO:0043025](http://purl.obolibrary.org/obo/GO_0043025) | CC | 5.76e-05 | 15 | FDR<0.01 |
| [8](#theme-8-behavior) | [behavior](#theme-8-behavior) [GO:0007610](http://purl.obolibrary.org/obo/GO_0007610) | BP | 7.16e-05 | 16 | FDR<0.01 |
| [9](#theme-9-perineuronal-net) | [perineuronal net](#theme-9-perineuronal-net) [GO:0072534](http://purl.obolibrary.org/obo/GO_0072534) | CC | 7.93e-05 | 4 | FDR<0.01 |
| [10](#theme-10-parallel-fiber-to-purkinje-cell-synapse) | [parallel fiber to Purkinje cell synapse](#theme-10-parallel-fiber-to-purkinje-cell-synapse) [GO:0098688](http://purl.obolibrary.org/obo/GO_0098688) | CC | 1.05e-04 | 5 | FDR<0.01 |
| [11](#theme-11-transmembrane-receptor-protein-tyrosine-phosphatase-activity) | [transmembrane receptor protein tyrosine phosphatase activity](#theme-11-transmembrane-receptor-protein-tyrosine-phosphatase-activity) [GO:0005001](http://purl.obolibrary.org/obo/GO_0005001) | MF | 4.95e-04 | 5 | FDR<0.01 |
| [12](#theme-12-nuclear-protein-containing-complex) | [nuclear protein-containing complex](#theme-12-nuclear-protein-containing-complex) [GO:0140513](http://purl.obolibrary.org/obo/GO_0140513) | CC | 7.78e-04 | 0 | FDR<0.01 |
| [13](#theme-13-ion-channel-regulator-activity) | [ion channel regulator activity](#theme-13-ion-channel-regulator-activity) [GO:0099106](http://purl.obolibrary.org/obo/GO_0099106) | MF | 3.82e-03 | 10 | FDR<0.01 |
| [14](#theme-14-immune-response) | [immune response](#theme-14-immune-response) [GO:0006955](http://purl.obolibrary.org/obo/GO_0006955) | BP | 6.38e-03 | 1 | FDR<0.01 |
| [15](#theme-15-neuron-projection-development) | [neuron projection development](#theme-15-neuron-projection-development) [GO:0031175](http://purl.obolibrary.org/obo/GO_0031175) | BP | 7.80e-03 | 21 | FDR<0.01 |
| [16](#theme-16-monoatomic-cation-channel-activity) | [monoatomic cation channel activity](#theme-16-monoatomic-cation-channel-activity) [GO:0005261](http://purl.obolibrary.org/obo/GO_0005261) | MF | 7.98e-03 | 13 | FDR<0.01 |
| [17](#theme-17-neuron-recognition) | [neuron recognition](#theme-17-neuron-recognition) [GO:0008038](http://purl.obolibrary.org/obo/GO_0008038) | BP | 8.22e-03 | 5 | FDR<0.01 |
| [18](#theme-18-ampa-glutamate-receptor-activity) | [AMPA glutamate receptor activity](#theme-18-ampa-glutamate-receptor-activity) [GO:0004971](http://purl.obolibrary.org/obo/GO_0004971) | MF | 8.55e-03 | 3 | FDR<0.01 |
| [19](#theme-19-prepulse-inhibition) | [prepulse inhibition](#theme-19-prepulse-inhibition) [GO:0060134](http://purl.obolibrary.org/obo/GO_0060134) | BP | 8.62e-03 | 3 | FDR<0.01 |
| [20](#theme-20-anterograde-trans-synaptic-signaling) | [anterograde trans-synaptic signaling](#theme-20-anterograde-trans-synaptic-signaling) [GO:0098916](http://purl.obolibrary.org/obo/GO_0098916) | BP | 1.40e-02 | 19 | FDR<0.05 |
| [21](#theme-21-regulation-of-neuronal-action-potential) | [regulation of neuronal action potential](#theme-21-regulation-of-neuronal-action-potential) [GO:0098908](http://purl.obolibrary.org/obo/GO_0098908) | BP | 1.60e-02 | 3 | FDR<0.05 |
| [22](#theme-22-symmetric-gaba-ergic-inhibitory-synapse) | [symmetric, GABA-ergic, inhibitory synapse](#theme-22-symmetric-gaba-ergic-inhibitory-synapse) [GO:0098983](http://purl.obolibrary.org/obo/GO_0098983) | CC | 1.76e-02 | 2 | FDR<0.05 |
| [23](#theme-23-cell-adhesion-mediator-activity) | [cell adhesion mediator activity](#theme-23-cell-adhesion-mediator-activity) [GO:0098631](http://purl.obolibrary.org/obo/GO_0098631) | MF | 1.82e-02 | 7 | FDR<0.05 |
| [24](#theme-24-cytoskeleton) | [cytoskeleton](#theme-24-cytoskeleton) [GO:0005856](http://purl.obolibrary.org/obo/GO_0005856) | CC | 1.94e-02 | 21 | FDR<0.05 |
| [25](#theme-25-presynaptic-active-zone) | [presynaptic active zone](#theme-25-presynaptic-active-zone) [GO:0048786](http://purl.obolibrary.org/obo/GO_0048786) | CC | 2.12e-02 | 10 | FDR<0.05 |
| [26](#theme-26-regulation-of-neural-precursor-cell-proliferation) | [regulation of neural precursor cell proliferation](#theme-26-regulation-of-neural-precursor-cell-proliferation) [GO:2000177](http://purl.obolibrary.org/obo/GO_2000177) | BP | 2.78e-02 | 5 | FDR<0.05 |
| [27](#theme-27-cell-cell-junction) | [cell-cell junction](#theme-27-cell-cell-junction) [GO:0005911](http://purl.obolibrary.org/obo/GO_0005911) | CC | 3.22e-02 | 13 | FDR<0.05 |
| [28](#theme-28-collagen-type-iv-trimer) | [collagen type IV trimer](#theme-28-collagen-type-iv-trimer) [GO:0005587](http://purl.obolibrary.org/obo/GO_0005587) | CC | 3.77e-02 | 2 | FDR<0.05 |
| [29](#theme-29-basal-dendrite) | [basal dendrite](#theme-29-basal-dendrite) [GO:0097441](http://purl.obolibrary.org/obo/GO_0097441) | CC | 3.77e-02 | 2 | FDR<0.05 |
| [30](#theme-30-endocytic-vesicle) | [endocytic vesicle](#theme-30-endocytic-vesicle) [GO:0030139](http://purl.obolibrary.org/obo/GO_0030139) | CC | 3.77e-02 | 7 | FDR<0.05 |

---

### Theme 1: synapse organization

**Summary:** synapse organization ([GO:0050808](http://purl.obolibrary.org/obo/GO_0050808))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] This theme centers on assembling both pre- and postsynaptic specializations, with child terms capturing presynaptic membrane assembly, synaptic membrane adhesion, and the tuning of postsynaptic organization that together drive stable excitatory connectivity. [EXTERNAL] GRID2 integrates into organizer complexes to promote excitatory synapse assembly and strengthen postsynaptic signaling, providing a structural and functional scaffold at glutamatergic synapses [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/). [EXTERNAL] NGL-1 and netrin-G1 cooperate with LAR-family phosphatases to trigger trans-induced cis adhesion that selectively initiates synaptic maturation at adhesion hotspots, mechanistically explaining how adhesion drives local recruitment of synaptic proteins [PMID:23986473](https://pubmed.ncbi.nlm.nih.gov/23986473/). [EXTERNAL] Neuroligin glycosylation state modulates synapse assembly capacity, linking post-translational control to receptor clustering and synaptic abundance in this organizational program [PMID:37865312](https://pubmed.ncbi.nlm.nih.gov/37865312/).

#### Key Insights

- [DATA] Positive regulation of synapse assembly is driven by receptor–organizer complexes that cluster and stabilize receptors at contact sites, elevating synaptic transmission efficiency [GO:0051965](http://purl.obolibrary.org/obo/GO_0051965). ([GO:0051965](http://purl.obolibrary.org/obo/GO_0051965))
- [DATA] Synaptic membrane adhesion positions presynaptic and postsynaptic membranes to nucleate assembly factors that couple adhesion to maturation [GO:0099560](http://purl.obolibrary.org/obo/GO_0099560). ([GO:0099560](http://purl.obolibrary.org/obo/GO_0099560))
- [DATA] Regulation of postsynapse organization tunes receptor and scaffold composition within dendritic spines to shape synaptic gain and plasticity [GO:0099175](http://purl.obolibrary.org/obo/GO_0099175). ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))

#### Key Genes

- **PTPRD**: [EXTERNAL] [EXTERNAL] PTPRD engages in the NGL-1–netrin-G1–LAR complex to couple trans-adhesion to recruitment of postsynaptic assembly machinery, promoting maturation of excitatory synapses [PMID:23986473](https://pubmed.ncbi.nlm.nih.gov/23986473/). ([GO:0099560](http://purl.obolibrary.org/obo/GO_0099560))
- **GRID2**: [EXTERNAL] [EXTERNAL] GRID2 scaffolds postsynaptic organizer complexes to enhance excitatory synapse assembly and stabilize ionotropic signaling at cerebellar synapses [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/). ([GO:1904861](http://purl.obolibrary.org/obo/GO_1904861))
- **LRP4**: [EXTERNAL] [EXTERNAL] LRP4 helps position and stabilize synaptic organizers that recruit glutamate receptor machinery, thereby tuning postsynaptic composition and maturation [PMID:23986473](https://pubmed.ncbi.nlm.nih.gov/23986473/). ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- **DOCK4**: [EXTERNAL] [EXTERNAL] DOCK4 links adhesion cues to local actin remodeling at postsynaptic compartments, facilitating receptor recruitment during postsynapse organization [PMID:23986473](https://pubmed.ncbi.nlm.nih.gov/23986473/). ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- **IGSF21**: [INFERENCE] [INFERENCE] IGSF21 participates in adhesion-governed maturation steps to bolster synaptic protein accumulation and sustain excitatory connectivity. ([GO:0050808](http://purl.obolibrary.org/obo/GO_0050808))

#### Statistical Context

[DATA] Synapse organization is strongly enriched ([GO:0050808](http://purl.obolibrary.org/obo/GO_0050808); FDR 1.51e-09; 9.1-fold; 19 genes), with significant leaves including regulation of postsynapse organization, positive regulation of synapse assembly, presynaptic membrane assembly, and synaptic membrane adhesion.

---

### Theme 2: regulation of membrane potential

**Summary:** regulation of membrane potential ([GO:0042391](http://purl.obolibrary.org/obo/GO_0042391))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Regulation of membrane potential integrates postsynaptic depolarizing currents with voltage-gated repolarizing conductances to sculpt excitability and action potential dynamics. [EXTERNAL] KCND2 and KCND3 supply A-type K+ currents that rapidly repolarize membranes and constrain spike timing, thereby limiting dendritic and axonal excitability [PMID:21349352](https://pubmed.ncbi.nlm.nih.gov/21349352/). [EXTERNAL] NALCN channelosome subunits control tonic Na+ leak to set resting potential and thereby adjust neuronal firing thresholds and network responsiveness [PMID:34929720](https://pubmed.ncbi.nlm.nih.gov/34929720/). [EXTERNAL] SCN3A provides fast Na+ influx to initiate spikes, while auxiliary regulators (KCNMB2, KChIPs) tune channel gating to match synaptic drive and firing probability [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/).

#### Key Insights

- [DATA] Regulation of postsynaptic membrane potential couples ligand-gated conductances with K+ channel feedback to set integration windows [GO:0060078](http://purl.obolibrary.org/obo/GO_0060078). ([GO:0060078](http://purl.obolibrary.org/obo/GO_0060078))
- [DATA] Action potential control emerges from the balance of Na+ inward currents and A-type/BK-mediated repolarization [GO:0001508](http://purl.obolibrary.org/obo/GO_0001508). ([GO:0001508](http://purl.obolibrary.org/obo/GO_0001508))

#### Key Genes

- **KCND2**: [EXTERNAL] [EXTERNAL] KCND2-encoded Kv4 channels drive fast A-type currents that repolarize dendrites and shape EPSP–spike coupling in postsynaptic compartments [PMID:21349352](https://pubmed.ncbi.nlm.nih.gov/21349352/). ([GO:0060078](http://purl.obolibrary.org/obo/GO_0060078))
- **INSYN2A**: [EXTERNAL] [EXTERNAL] INSYN2A engages the NALCN channelosome to sustain Na+ leak currents that depolarize the resting potential and tune neuronal excitability [PMID:34929720](https://pubmed.ncbi.nlm.nih.gov/34929720/). ([GO:0060078](http://purl.obolibrary.org/obo/GO_0060078))
- **RGS7**: [EXTERNAL] [EXTERNAL] RGS7 accelerates GPCR Gα deactivation to restrain channel-modulatory pathways within the NALCN complex, stabilizing leak conductance and resting potential [PMID:34929720](https://pubmed.ncbi.nlm.nih.gov/34929720/). ([GO:0060078](http://purl.obolibrary.org/obo/GO_0060078))
- **SCN3A**: [EXTERNAL] [EXTERNAL] SCN3A mediates rapid Na+ influx during the upstroke of action potentials, setting excitability in developing and adult neurons [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). ([GO:0001508](http://purl.obolibrary.org/obo/GO_0001508))
- **KCNMB2**: [INFERENCE] [INFERENCE] The BK-channel β2 subunit accelerates Ca2+- and voltage-dependent K+ current activation to promote spike repolarization and afterhyperpolarization, stabilizing firing. ([GO:0001508](http://purl.obolibrary.org/obo/GO_0001508))

#### Statistical Context

[DATA] Regulation of membrane potential is enriched ([GO:0042391](http://purl.obolibrary.org/obo/GO_0042391); FDR 2.26e-08; 6.1-fold; 22 genes), including specific enrichment for regulation of postsynaptic membrane potential and action potential.

---

### Theme 3: postsynapse

**Summary:** postsynapse ([GO:0098794](http://purl.obolibrary.org/obo/GO_0098794))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The postsynapse theme captures receptor- and scaffold-rich subdomains in dendritic spines and the postsynaptic density membrane that coordinate fast excitation and plasticity. [EXTERNAL] NLGN4X localizes to the postsynaptic density membrane and modulates excitatory synaptic transmission in human neurons, linking adhesion cues to receptor function [PMID:31257103](https://pubmed.ncbi.nlm.nih.gov/31257103/). [EXTERNAL] GRID2 gating is triggered via mGlu1 signaling, coupling metabotropic activation to delta receptor channel behavior within postsynaptic density assemblies [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). [EXTERNAL] GRIA2 surface abundance is governed by endocytic control, directly tuning AMPA-mediated charge transfer and spine responsiveness [PMID:21221849](https://pubmed.ncbi.nlm.nih.gov/21221849/).

#### Key Insights

- [DATA] Postsynaptic density membrane concentrates receptors and adaptors to align signaling nanodomains with presynaptic release sites [GO:0098839](http://purl.obolibrary.org/obo/GO_0098839). ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- [DATA] Dendritic spines provide compartmentalized calcium and actin signaling to stabilize receptor fields and enable long-term plasticity [GO:0043197](http://purl.obolibrary.org/obo/GO_0043197). ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))

#### Key Genes

- **NLGN4X**: [EXTERNAL] [EXTERNAL] NLGN4X organizes PSD composition at excitatory synapses to enhance receptor recruitment and synaptic efficacy [PMID:31257103](https://pubmed.ncbi.nlm.nih.gov/31257103/). ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **GRIA2**: [EXTERNAL] [EXTERNAL] GRIA2 trafficking via clathrin machinery calibrates synaptic AMPAR content and spine-based integration [PMID:21221849](https://pubmed.ncbi.nlm.nih.gov/21221849/). ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))
- **GRID2**: [EXTERNAL] [EXTERNAL] GRID2 operates within PSD signaling cassettes, transducing mGlu1-triggered gating into postsynaptic current modulation [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **PTPRO**: [INFERENCE] [INFERENCE] PTPRO dephosphorylates postsynaptic substrates to tune scaffold stability and receptor efficacy within excitatory synapses. ([GO:0098794](http://purl.obolibrary.org/obo/GO_0098794))

#### Statistical Context

[DATA] Postsynapse is enriched ([GO:0098794](http://purl.obolibrary.org/obo/GO_0098794); FDR 3.46e-08; 6.2-fold; 19 genes), with strong leaves at the postsynaptic density membrane and dendritic spine.

---

### Theme 4: Schaffer collateral - CA1 synapse

**Summary:** Schaffer collateral - CA1 synapse ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The Schaffer collateral–CA1 synapse theme focuses on hippocampal excitatory contacts where AMPAR trafficking and auxiliary subunits govern LTP/LTD and memory encoding. [EXTERNAL] GSG1L and TARP γ8 co-assemble with GluA1/2 to tune gating and trafficking of AMPARs, directly controlling synaptic potency at SC–CA1 synapses [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/). [INFERENCE] CASK and PTPRD scaffold receptor–organizer complexes to stabilize postsynaptic receptors during plasticity-inducing activity, reinforcing CA1 synaptic weights. [INFERENCE] MYO5C couples actin transport to AMPAR delivery, enabling rapid insertion during potentiation to augment excitatory drive.

#### Key Insights

- [DATA] AMPAR auxiliary subunits orchestrate gating and delivery of GluA1/2 to remodel CA1 synaptic efficacy [GO:0098685](http://purl.obolibrary.org/obo/GO_0098685). ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))
- [INFERENCE] Adhesion phosphatases and MAGUKs consolidate newly inserted receptors to preserve memory traces at potentiated spines [GO:0098685](http://purl.obolibrary.org/obo/GO_0098685). ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))

#### Key Genes

- **GSG1L**: [EXTERNAL] [EXTERNAL] GSG1L promotes assembly and trafficking of GluA1/2–TARP γ8 AMPARs to strengthen CA1 synapses during plasticity [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/). ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))
- **CASK**: [INFERENCE] [INFERENCE] CASK anchors AMPAR–auxiliary complexes within the postsynaptic membrane to stabilize potentiated SC–CA1 synapses. ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))
- **PTPRD**: [INFERENCE] [INFERENCE] PTPRD dephosphorylates synaptic organizers to maintain receptor localization and sustain long-term efficacy in CA1. ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))
- **MYO5C**: [INFERENCE] [INFERENCE] MYO5C drives actin-based vesicular transport of AMPAR cargo to postsynaptic sites during activity-dependent potentiation. ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))

#### Statistical Context

[DATA] Schaffer collateral–CA1 synapse is highly enriched ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685); FDR 1.46e-07; 12.4-fold; 11 genes), consistent with focused hippocampal glutamatergic mechanisms.

---

### Theme 5: axon

**Summary:** axon ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The axon theme captures structural compartments and trafficking pathways that establish polarized conduction and domain-specific channel clustering. [EXTERNAL] CNTNAP2 marks juxtaparanodal domains and orchestrates K+ channel clustering, ensuring saltatory conduction fidelity in myelinated axons [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/). [EXTERNAL] LRRK2 localizes to axonal vesicular structures, consistent with roles in transport and membrane remodeling that support axonal maintenance [PMID:17120249](https://pubmed.ncbi.nlm.nih.gov/17120249/). [INFERENCE] Adhesion molecules and cytoskeletal regulators such as CNTN1 and NAV2 coordinate axon–glia interactions and cargo delivery to sustain conduction velocity and axonal stability.

#### Key Insights

- [DATA] Axonal domain organization depends on adhesion scaffolds that segregate ion channels for efficient propagation [GO:0030424](http://purl.obolibrary.org/obo/GO_0030424). ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- [INFERENCE] Microtubule-based transport and endocytic cycling position membrane proteins to the axon initial segment and nodes [GO:0030424](http://purl.obolibrary.org/obo/GO_0030424). ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))

#### Key Genes

- **CNTNAP2**: [EXTERNAL] [EXTERNAL] CNTNAP2 defines juxtaparanodes and organizes Shaker-type K+ channels critical for rapid axonal conduction [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/). ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **LRRK2**: [EXTERNAL] [EXTERNAL] LRRK2 associates with axonal vesicles, supporting roles in cargo trafficking and axonal maintenance [PMID:17120249](https://pubmed.ncbi.nlm.nih.gov/17120249/). ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **NAV2**: [INFERENCE] [INFERENCE] NAV2 promotes polarized trafficking of axonal cargos to establish domain-specific protein landscapes. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **CNTN1**: [INFERENCE] [INFERENCE] CNTN1 stabilizes paranodal axon–glia junctions to insulate axons and maintain conduction speed. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))

#### Statistical Context

[DATA] Axon is enriched ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424); FDR 9.83e-07; 5.0-fold; 19 genes), consistent with strong axonal polarity and domain-assembly signals.

---

### Theme 6: monoatomic ion channel complex

**Summary:** monoatomic ion channel complex ([GO:0034702](http://purl.obolibrary.org/obo/GO_0034702))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 2.53e-06 · **Genes (17)**: CACNG4, CNTNAP2, DLG2, DPP6, GRIA2, GRIA3, GRID2, KCND2, KCND3, KCNIP1, KCNIP4, KCNMB2, NALCN, PDE4B, SCN1A … (+2 more)

---

### Theme 7: neuronal cell body

**Summary:** neuronal cell body ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The neuronal cell body theme encompasses somatodendritic protein networks that maintain morphology, biosynthesis, and excitability hubs. [EXTERNAL] LRRK2 concentrates in neuronal cell bodies and interacts with small GTPase machinery, linking somatic signaling to cytoskeletal dynamics [PMID:21048939](https://pubmed.ncbi.nlm.nih.gov/21048939/); [PMID:21696411](https://pubmed.ncbi.nlm.nih.gov/21696411/). [EXTERNAL] CNTNAP2 localizes within neuronal compartments that coordinate domain-specific channel clustering and trafficking, supporting soma-to-process polarity [PMID:10624965](https://pubmed.ncbi.nlm.nih.gov/10624965/). [INFERENCE] MAP2 stabilizes somatodendritic microtubules to support biosynthetic load and receptor trafficking required for sustained firing.

#### Key Insights

- [DATA] Somatic compartments host scaffolds and motors that distribute receptors and channels to dendrites and axons [GO:0043025](http://purl.obolibrary.org/obo/GO_0043025). ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- [INFERENCE] Kinase–GTPase hubs in the soma tune cytoskeletal turnover and organelle trafficking to maintain neuronal health [GO:0043025](http://purl.obolibrary.org/obo/GO_0043025). ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))

#### Key Genes

- **LRRK2**: [EXTERNAL] [EXTERNAL] LRRK2 is abundant in neuronal cell bodies and interfaces with ARHGEF7–CDC42 signaling that controls somatic cytoskeletal dynamics [PMID:21048939](https://pubmed.ncbi.nlm.nih.gov/21048939/); [PMID:21696411](https://pubmed.ncbi.nlm.nih.gov/21696411/). ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **CNTNAP2**: [EXTERNAL] [EXTERNAL] CNTNAP2 is present in neuronal compartments coordinating channel clustering and soma–process polarity [PMID:10624965](https://pubmed.ncbi.nlm.nih.gov/10624965/). ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **MAP2**: [INFERENCE] [INFERENCE] MAP2 stabilizes somatic microtubules and organizes trafficking tracks that sustain receptor supply and excitability. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **LRP4**: [INFERENCE] [INFERENCE] LRP4 integrates somatic adhesion–signaling cues to calibrate receptor assembly and downstream neuronal responses. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))

#### Statistical Context

[DATA] Neuronal cell body is enriched ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025); FDR 5.76e-05; 4.7-fold; 15 genes), reflecting somatodendritic specialization.

---

### Theme 8: behavior

**Summary:** behavior ([GO:0007610](http://purl.obolibrary.org/obo/GO_0007610))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The behavior theme links synaptic signaling modules to systems-level outputs including vocalization and learning. [EXTERNAL] CNTNAP2 and NRXN1 influence social communication and learning by controlling synaptic connectivity and presynaptic release properties, with mutations impairing vocalization and cognitive behaviors [PMID:19896112](https://pubmed.ncbi.nlm.nih.gov/19896112/). [EXTERNAL] Human NLGN4X variants disrupt folding and synaptic trafficking, perturbing excitatory–inhibitory balance and leading to social and vocalization deficits [PMID:19726642](https://pubmed.ncbi.nlm.nih.gov/19726642/). [EXTERNAL] NLGN4Y variation associates with alterations in social behavior and vocalization, reinforcing the role of inhibitory synapse organization in behavioral control [PMID:18628683](https://pubmed.ncbi.nlm.nih.gov/18628683/).

#### Key Insights

- [DATA] Vocalization behavior enrichment highlights neuroligin–neurexin adhesion modules that wire communication circuits [GO:0071625](http://purl.obolibrary.org/obo/GO_0071625). ([GO:0071625](http://purl.obolibrary.org/obo/GO_0071625))
- [DATA] Learning enrichment implicates synaptic plasticity regulators whose dosage and trafficking shape memory encoding [GO:0007612](http://purl.obolibrary.org/obo/GO_0007612). ([GO:0007612](http://purl.obolibrary.org/obo/GO_0007612))

#### Key Genes

- **CNTNAP2**: [EXTERNAL] [EXTERNAL] CNTNAP2 modulates circuits underlying speech and social behavior, with genetic disruption impairing vocalization and learning [PMID:19896112](https://pubmed.ncbi.nlm.nih.gov/19896112/). ([GO:0071625](http://purl.obolibrary.org/obo/GO_0071625))
- **NRXN1**: [EXTERNAL] [EXTERNAL] NRXN1 controls presynaptic release and synapse number that support learning and social behaviors [PMID:19896112](https://pubmed.ncbi.nlm.nih.gov/19896112/). ([GO:0007612](http://purl.obolibrary.org/obo/GO_0007612))
- **NLGN4X**: [EXTERNAL] [EXTERNAL] NLGN4X missense mutations hinder ER export and synapse function, producing social and vocalization abnormalities [PMID:19726642](https://pubmed.ncbi.nlm.nih.gov/19726642/). ([GO:0071625](http://purl.obolibrary.org/obo/GO_0071625))
- **NLGN4Y**: [EXTERNAL] [EXTERNAL] NLGN4Y variation correlates with altered social behavior and learning, consistent with perturbed inhibitory synapse maturation [PMID:18628683](https://pubmed.ncbi.nlm.nih.gov/18628683/). ([GO:0007612](http://purl.obolibrary.org/obo/GO_0007612))

#### Statistical Context

[DATA] Behavior is enriched ([GO:0007610](http://purl.obolibrary.org/obo/GO_0007610); FDR 7.16e-05; 5.2-fold; 16 genes) with specific enrichment for vocalization behavior and learning.

---

### Theme 9: perineuronal net

**Summary:** perineuronal net ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The perineuronal net theme captures extracellular matrix lattices that encase neurons to constrain plasticity and stabilize circuitry. [INFERENCE] Versican and brevican proteoglycans assemble chondroitin-sulfate–rich scaffolds that limit receptor mobility and spine remodeling, consolidating network states. [INFERENCE] Tenascin-R and PTPRZ1 interact with ECM components and cell-surface receptors to regulate ion microenvironments and protect synapses from destabilizing proteolysis.

#### Key Insights

- [INFERENCE] ECM proteoglycans in perineuronal nets curb synaptic rewiring to preserve mature circuit function [GO:0072534](http://purl.obolibrary.org/obo/GO_0072534). ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))
- [INFERENCE] Perineuronal nets adjust ionic buffering and diffusion barriers that influence neuronal excitability [GO:0072534](http://purl.obolibrary.org/obo/GO_0072534). ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))

#### Key Genes

- **VCAN**: [INFERENCE] [INFERENCE] VCAN forms ECM backbones of perineuronal nets that restrict receptor diffusion and spine turnover. ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))
- **TNR**: [INFERENCE] [INFERENCE] TNR crosslinks ECM modules and adhesion receptors to stabilize inhibitory microcircuits within nets. ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))
- **BCAN**: [INFERENCE] [INFERENCE] BCAN contributes chondroitin-sulfate proteoglycan content that reinforces synaptic stability and neuroprotection. ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))
- **PTPRZ1**: [INFERENCE] [INFERENCE] PTPRZ1 modulates ECM–receptor signaling that shapes net assembly and activity-dependent plasticity limits. ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))

#### Statistical Context

[DATA] Perineuronal net is strongly enriched ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534); FDR 7.93e-05; 45.2-fold; 4 genes), indicating concentrated ECM modules around neurons.

---

### Theme 10: parallel fiber to Purkinje cell synapse

**Summary:** parallel fiber to Purkinje cell synapse ([GO:0098688](http://purl.obolibrary.org/obo/GO_0098688))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Parallel fiber–Purkinje cell synapses exemplify cerebellar excitatory contacts where AMPAR composition and delta receptor signaling calibrate timing and gain. [INFERENCE] GRID2 and GRIA3 coordinate postsynaptic charge transfer and instructive signaling that underlie cerebellar learning. [INFERENCE] CNTN6 and CTNNA2 provide adhesion and cytoskeletal linkage to stabilize these synapses during development and activity.

#### Key Insights

- [INFERENCE] AMPAR and GRID2-dependent organization sculpts Purkinje cell integration at parallel fiber inputs [GO:0098688](http://purl.obolibrary.org/obo/GO_0098688). ([GO:0098688](http://purl.obolibrary.org/obo/GO_0098688))
- [INFERENCE] Adhesion–cytoskeletal coupling maintains alignment of presynaptic release sites with Purkinje postsynapses [GO:0098688](http://purl.obolibrary.org/obo/GO_0098688). ([GO:0098688](http://purl.obolibrary.org/obo/GO_0098688))

#### Key Genes

- **GRID2**: [INFERENCE] [INFERENCE] GRID2 postsynaptic signaling shapes parallel fiber–Purkinje responses and synapse stability. ([GO:0098688](http://purl.obolibrary.org/obo/GO_0098688))
- **GRIA3**: [INFERENCE] [INFERENCE] GRIA3-containing AMPARs mediate fast excitation essential for cerebellar timing at these synapses. ([GO:0098688](http://purl.obolibrary.org/obo/GO_0098688))
- **CNTN6**: [INFERENCE] [INFERENCE] CNTN6 promotes axon–dendrite adhesion to consolidate cerebellar synaptic architecture. ([GO:0098688](http://purl.obolibrary.org/obo/GO_0098688))

#### Statistical Context

[DATA] Parallel fiber–Purkinje cell synapse is enriched ([GO:0098688](http://purl.obolibrary.org/obo/GO_0098688); FDR 1.05e-04; 23.6-fold; 5 genes), consistent with cerebellar circuit specialization.

---

### Theme 11: transmembrane receptor protein tyrosine phosphatase activity

**Summary:** transmembrane receptor protein tyrosine phosphatase activity ([GO:0005001](http://purl.obolibrary.org/obo/GO_0005001))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Transmembrane receptor protein tyrosine phosphatases couple extracellular recognition to intracellular tyrosine dephosphorylation, rewiring signaling at the membrane. [EXTERNAL] PTPRD displays receptor-like extracellular domains and intracellular phosphatase activity that modulate cell activation and differentiation signals [PMID:7896816](https://pubmed.ncbi.nlm.nih.gov/7896816/). [EXTERNAL] PTPRO and PTPRN2 are bona fide receptor-type phosphatases, with PTPRO (GLEPP1) and PTPRN2 providing transmembrane catalytic hubs that tune cellular responses [PMID:7665166](https://pubmed.ncbi.nlm.nih.gov/7665166/); [PMID:8798755](https://pubmed.ncbi.nlm.nih.gov/8798755/). [EXTERNAL] PTPRZ1 contains a receptor domain homologous to carbonic anhydrases and is highly expressed in the brain, aligning adhesion with phosphatase control in neural tissue [PMID:1323835](https://pubmed.ncbi.nlm.nih.gov/1323835/).

#### Key Insights

- [INFERENCE] RPTPs align adhesion inputs with tyrosine dephosphorylation to reset receptor proximal signaling [GO:0005001](http://purl.obolibrary.org/obo/GO_0005001). ([GO:0005001](http://purl.obolibrary.org/obo/GO_0005001))
- [INFERENCE] Domain diversity across RPTPs enables tissue-specific wiring of growth and guidance pathways [GO:0005001](http://purl.obolibrary.org/obo/GO_0005001). ([GO:0005001](http://purl.obolibrary.org/obo/GO_0005001))

#### Key Genes

- **PTPRN2**: [EXTERNAL] [EXTERNAL] PTPRN2 encodes a receptor-like phosphatase with extracellular adhesive motifs and intracellular catalytic domains that regulate signaling [PMID:8798755](https://pubmed.ncbi.nlm.nih.gov/8798755/). ([GO:0005001](http://purl.obolibrary.org/obo/GO_0005001))
- **PTPRD**: [EXTERNAL] [EXTERNAL] PTPRD provides transmembrane phosphatase activity that shapes cell activation and differentiation pathways [PMID:7896816](https://pubmed.ncbi.nlm.nih.gov/7896816/). ([GO:0005001](http://purl.obolibrary.org/obo/GO_0005001))
- **PTPRO**: [EXTERNAL] [EXTERNAL] PTPRO is a receptor-type phosphatase (GLEPP1) whose activity modulates cell signaling programs [PMID:7665166](https://pubmed.ncbi.nlm.nih.gov/7665166/). ([GO:0005001](http://purl.obolibrary.org/obo/GO_0005001))
- **PTPRZ1**: [EXTERNAL] [EXTERNAL] PTPRZ1 is a brain-enriched receptor PTP with an N-terminal receptor-like domain homologous to carbonic anhydrases [PMID:1323835](https://pubmed.ncbi.nlm.nih.gov/1323835/). ([GO:0005001](http://purl.obolibrary.org/obo/GO_0005001))

#### Statistical Context

[DATA] Transmembrane receptor protein tyrosine phosphatase activity is enriched ([GO:0005001](http://purl.obolibrary.org/obo/GO_0005001); FDR 4.95e-04; 33.3-fold; 5 genes), indicating coordinated receptor-proximal signaling control.

---

### Theme 12: nuclear protein-containing complex

**Summary:** nuclear protein-containing complex ([GO:0140513](http://purl.obolibrary.org/obo/GO_0140513))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Nuclear protein-containing complex appears here without direct gene support in the input set, likely reflecting hierarchical propagation from related nuclear-associated annotations elsewhere. [GO-HIERARCHY] Because no input genes map to this node, the signal may derive from shared ancestors in the ontology rather than specific nuclear complex membership in this gene list.

#### Key Insights

- [DATA] No genes from the input mapped to nuclear protein-containing complex despite statistical enrichment, suggesting contextual or hierarchical carry-over [GO:0140513](http://purl.obolibrary.org/obo/GO_0140513). ([GO:0140513](http://purl.obolibrary.org/obo/GO_0140513))

#### Statistical Context

[DATA] Nuclear protein-containing complex shows enrichment ([GO:0140513](http://purl.obolibrary.org/obo/GO_0140513); FDR 7.78e-04) but with 0 annotated input genes, indicating a non-primary driver in this dataset.

---

### Theme 13: ion channel regulator activity

**Summary:** ion channel regulator activity ([GO:0099106](http://purl.obolibrary.org/obo/GO_0099106))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Ion channel regulator activity unifies auxiliary subunits and signaling enzymes that modulate channel trafficking, gating, and surface expression. [EXTERNAL] DPP6 accelerates Kv4 kinetics and boosts surface density to shape dendritic A-type currents that constrain excitability [PMID:18364354](https://pubmed.ncbi.nlm.nih.gov/18364354/). [EXTERNAL] SGK1 phosphorylates and regulates calcium, potassium, sodium, and chloride channels, coupling hormonal signals to channel availability and conductance [PMID:20530112](https://pubmed.ncbi.nlm.nih.gov/20530112/). [EXTERNAL] CACNG4 modulates Cav1.2 complexes to refine calcium influx, aligning channel function with cellular demand [PMID:21127204](https://pubmed.ncbi.nlm.nih.gov/21127204/).

#### Key Insights

- [INFERENCE] Channel regulators tune recruitment and inactivation kinetics to align excitability with synaptic input patterns [GO:0099106](http://purl.obolibrary.org/obo/GO_0099106). ([GO:0099106](http://purl.obolibrary.org/obo/GO_0099106))
- [INFERENCE] Second-messenger kinases couple extracellular cues to channel density and open probability [GO:0099106](http://purl.obolibrary.org/obo/GO_0099106). ([GO:0099106](http://purl.obolibrary.org/obo/GO_0099106))

#### Key Genes

- **DPP6**: [EXTERNAL] [EXTERNAL] DPP6 remodels Kv4 gating to generate rapid inactivation that sculpts postsynaptic integration windows [PMID:18364354](https://pubmed.ncbi.nlm.nih.gov/18364354/). ([GO:0099106](http://purl.obolibrary.org/obo/GO_0099106))
- **SGK1**: [EXTERNAL] [EXTERNAL] SGK1 adjusts multiple ion channel classes via phosphorylation to modulate excitability under hormonal control [PMID:20530112](https://pubmed.ncbi.nlm.nih.gov/20530112/). ([GO:0099106](http://purl.obolibrary.org/obo/GO_0099106))
- **CACNG4**: [EXTERNAL] [EXTERNAL] CACNG4 influences Cav1.2 channel function and stability to calibrate calcium entry during activity [PMID:21127204](https://pubmed.ncbi.nlm.nih.gov/21127204/). ([GO:0099106](http://purl.obolibrary.org/obo/GO_0099106))
- **KCNIP4**: [INFERENCE] [INFERENCE] KCNIP4 co-assembles with Kv4 to modulate inactivation and surface expression, tuning subthreshold K+ conductance. ([GO:0099106](http://purl.obolibrary.org/obo/GO_0099106))

#### Statistical Context

[DATA] Ion channel regulator activity is enriched ([GO:0099106](http://purl.obolibrary.org/obo/GO_0099106); FDR 3.82e-03; 6.6-fold; 10 genes), consistent with extensive auxiliary-channel control.

---

### Theme 14: immune response

**Summary:** immune response ([GO:0006955](http://purl.obolibrary.org/obo/GO_0006955))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Immune response appears as a focused signal, potentially reflecting synapse–immune interface proteins with roles in recognition and plasticity. [INFERENCE] SUSD4 may influence immune receptor signaling or cell–cell interactions that secondarily modulate neuronal function and synaptic remodeling.

#### Key Insights

- [INFERENCE] Neuronal adhesion proteins can engage immune pathways that reshape synaptic environments [GO:0006955](http://purl.obolibrary.org/obo/GO_0006955). ([GO:0006955](http://purl.obolibrary.org/obo/GO_0006955))

#### Key Genes

- **SUSD4**: [INFERENCE] [INFERENCE] SUSD4 likely participates in receptor-mediated immune signaling that can indirectly impact neural circuit states. ([GO:0006955](http://purl.obolibrary.org/obo/GO_0006955))

#### Statistical Context

[DATA] Immune response is enriched ([GO:0006955](http://purl.obolibrary.org/obo/GO_0006955); FDR 6.38e-03; 1 gene), indicating a pinpointed immunomodulatory component.

---

### Theme 15: neuron projection development

**Summary:** neuron projection development ([GO:0031175](http://purl.obolibrary.org/obo/GO_0031175))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Neuron projection development integrates axon guidance and dendritic morphogenesis to establish synaptic maps. [EXTERNAL] DCC transduces netrin-1 attraction and restrains exuberant collateral sprouting, balancing axon extension with circuit specificity [PMID:19616629](https://pubmed.ncbi.nlm.nih.gov/19616629/). [EXTERNAL] LRRK2 modulates neurite morphology via kinase activity, linking cytoskeletal dynamics to projection growth programs [PMID:17114044](https://pubmed.ncbi.nlm.nih.gov/17114044/). [EXTERNAL] MAP2 stabilizes dendritic microtubules and supports projection development and dendrite morphogenesis in the developing human brain [PMID:26609151](https://pubmed.ncbi.nlm.nih.gov/26609151/); [PMID:20846339](https://pubmed.ncbi.nlm.nih.gov/20846339/).

#### Key Insights

- [DATA] Neuron projection morphogenesis enrichment reflects guidance and cytoskeletal regulators that set arbor complexity [GO:0048812](http://purl.obolibrary.org/obo/GO_0048812). ([GO:0048812](http://purl.obolibrary.org/obo/GO_0048812))
- [DATA] Negative regulation of axonogenesis acts as a brake to prevent mistargeting during circuit assembly [GO:0050771](http://purl.obolibrary.org/obo/GO_0050771). ([GO:0050771](http://purl.obolibrary.org/obo/GO_0050771))

#### Key Genes

- **DCC**: [EXTERNAL] [EXTERNAL] DCC restrains collateral sprouting while guiding netrin-1-mediated outgrowth to refine connectivity [PMID:19616629](https://pubmed.ncbi.nlm.nih.gov/19616629/). ([GO:0050771](http://purl.obolibrary.org/obo/GO_0050771))
- **MAP2**: [EXTERNAL] [EXTERNAL] MAP2 stabilizes dendritic microtubules to drive neuron projection development and dendrite morphogenesis [PMID:26609151](https://pubmed.ncbi.nlm.nih.gov/26609151/); [PMID:20846339](https://pubmed.ncbi.nlm.nih.gov/20846339/). ([GO:0031175](http://purl.obolibrary.org/obo/GO_0031175))
- **LRP4**: [INFERENCE] [INFERENCE] LRP4 couples adhesion and trophic signaling to stabilize projection terminals during maturation. ([GO:0048812](http://purl.obolibrary.org/obo/GO_0048812))
- **DOCK10**: [INFERENCE] [INFERENCE] DOCK10 activates Rac1 to remodel actin for dendritic branching and projection elaboration. ([GO:0048812](http://purl.obolibrary.org/obo/GO_0048812))

#### Statistical Context

[DATA] Neuron projection development is enriched ([GO:0031175](http://purl.obolibrary.org/obo/GO_0031175); FDR 7.80e-03; 3.9-fold; 13 genes), including neuron projection morphogenesis and negative regulation of axonogenesis.

---

### Theme 16: monoatomic cation channel activity

**Summary:** monoatomic cation channel activity ([GO:0005261](http://purl.obolibrary.org/obo/GO_0005261))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Monoatomic cation channel activity aggregates pore-forming Na+, K+, and AMPA channels whose conductance underlies synaptic integration and spike generation. [EXTERNAL] KCND2 and KCND3 provide A-type K+ currents that rapidly inactivate to sculpt EPSP waveforms and interspike intervals [PMID:35597238](https://pubmed.ncbi.nlm.nih.gov/35597238/); [PMID:34997220](https://pubmed.ncbi.nlm.nih.gov/34997220/). [EXTERNAL] SCN3A mediates voltage-gated Na+ currents essential for action potential initiation and propagation in developing and adult neurons [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). [EXTERNAL] NALCN conducts tonic Na+ leak to depolarize resting potential and sustain excitability across behavioral circuits [PMID:32698188](https://pubmed.ncbi.nlm.nih.gov/32698188/).

#### Key Insights

- [INFERENCE] Transient and tonic cation fluxes combine to set thresholds, gain, and temporal filtering in neurons [GO:0005261](http://purl.obolibrary.org/obo/GO_0005261). ([GO:0005261](http://purl.obolibrary.org/obo/GO_0005261))
- [INFERENCE] Auxiliary subunits shift gating equilibria to match channel activity with network state [GO:0005261](http://purl.obolibrary.org/obo/GO_0005261). ([GO:0005261](http://purl.obolibrary.org/obo/GO_0005261))

#### Key Genes

- **KCND2**: [EXTERNAL] [EXTERNAL] KCND2 mediates A-type K+ currents that limit dendritic depolarization and accelerate repolarization [PMID:35597238](https://pubmed.ncbi.nlm.nih.gov/35597238/). ([GO:0005261](http://purl.obolibrary.org/obo/GO_0005261))
- **KCND3**: [EXTERNAL] [EXTERNAL] KCND3-encoded Kv4.3 contributes transient outward K+ conductance shaping spike frequency and width [PMID:34997220](https://pubmed.ncbi.nlm.nih.gov/34997220/). ([GO:0005261](http://purl.obolibrary.org/obo/GO_0005261))
- **SCN3A**: [EXTERNAL] [EXTERNAL] SCN3A carries fast Na+ current essential for action potential upstrokes and signal propagation [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). ([GO:0005261](http://purl.obolibrary.org/obo/GO_0005261))
- **NALCN**: [EXTERNAL] [EXTERNAL] NALCN provides voltage-independent Na+ leak that depolarizes resting potential to promote firing [PMID:32698188](https://pubmed.ncbi.nlm.nih.gov/32698188/). ([GO:0005261](http://purl.obolibrary.org/obo/GO_0005261))

#### Statistical Context

[DATA] Monoatomic cation channel activity is enriched ([GO:0005261](http://purl.obolibrary.org/obo/GO_0005261); FDR 7.98e-03; 4.3-fold; 13 genes), spanning AMPA, Kv4, Nav, and NALCN conductances.

---

### Theme 17: neuron recognition

**Summary:** neuron recognition ([GO:0008038](http://purl.obolibrary.org/obo/GO_0008038))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Neuron recognition captures cell-adhesion codes that ensure specific partner matching during circuit assembly. [EXTERNAL] NTM and OPCML are GPI-anchored adhesion molecules that mediate neuron–neuron recognition, diversifying surface identities to guide precise connections [PMID:7891157](https://pubmed.ncbi.nlm.nih.gov/7891157/). [EXTERNAL] CNTNAP2 participates in recognition at axonal domains, aligning with juxtaparanodal specialization and channel clustering [PMID:10624965](https://pubmed.ncbi.nlm.nih.gov/10624965/). [INFERENCE] SEMA5A provides contact-mediated guidance that influences recognition outcomes and pathway selection.

#### Key Insights

- [INFERENCE] Combinatorial GPI-anchored adhesion codes confer selective recognition and synaptic partner choice [GO:0008038](http://purl.obolibrary.org/obo/GO_0008038). ([GO:0008038](http://purl.obolibrary.org/obo/GO_0008038))
- [DATA] Juxtaparanodal organizers link recognition to ion channel clustering for domain-specific signaling [GO:0008038](http://purl.obolibrary.org/obo/GO_0008038). ([GO:0008038](http://purl.obolibrary.org/obo/GO_0008038))

#### Key Genes

- **NTM**: [EXTERNAL] [EXTERNAL] NTM supports neuron–neuron recognition via GPI-anchored adhesion that specifies synaptic partners [PMID:7891157](https://pubmed.ncbi.nlm.nih.gov/7891157/). ([GO:0008038](http://purl.obolibrary.org/obo/GO_0008038))
- **OPCML**: [EXTERNAL] [EXTERNAL] OPCML contributes to recognition cues that refine circuit assembly through selective adhesion [PMID:7891157](https://pubmed.ncbi.nlm.nih.gov/7891157/). ([GO:0008038](http://purl.obolibrary.org/obo/GO_0008038))
- **CNTNAP2**: [EXTERNAL] [EXTERNAL] CNTNAP2 organizes axonal domains to link recognition with juxtaparanodal channel clustering [PMID:10624965](https://pubmed.ncbi.nlm.nih.gov/10624965/). ([GO:0008038](http://purl.obolibrary.org/obo/GO_0008038))
- **SEMA5A**: [INFERENCE] [INFERENCE] SEMA5A contact-mediated guidance shapes recognition outcomes during pathway selection. ([GO:0008038](http://purl.obolibrary.org/obo/GO_0008038))

#### Statistical Context

[DATA] Neuron recognition is enriched ([GO:0008038](http://purl.obolibrary.org/obo/GO_0008038); FDR 8.22e-03; 13.5-fold; 5 genes), highlighting adhesion code modules.

---

### Theme 18: AMPA glutamate receptor activity

**Summary:** AMPA glutamate receptor activity ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] AMPA glutamate receptor activity unifies pore-forming subunits that mediate fast excitatory transmission and plasticity. [EXTERNAL] GRIA2-dependent AMPAR currents are maintained by calcineurin-sensitive endocytic balance, linking receptor cycling to synaptic stability and resilience to toxic insults [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). [EXTERNAL] GRIA3 gating is controlled by TARPs and cornichons, enabling resensitization and fine-tuning of excitatory charge transfer [PMID:21172611](https://pubmed.ncbi.nlm.nih.gov/21172611/). [INFERENCE] GRID2 integrates delta receptor signaling with AMPAR-driven excitation to calibrate cerebellar circuit output.

#### Key Insights

- [DATA] AMPA receptor-mediated currents provide the principal fast excitatory drive for memory and computation [GO:0004971](http://purl.obolibrary.org/obo/GO_0004971). ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971))
- [INFERENCE] Auxiliary subunits confer kinetic diversity that tailors synapse-specific AMPAR function [GO:0004971](http://purl.obolibrary.org/obo/GO_0004971). ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971))

#### Key Genes

- **GRIA2**: [EXTERNAL] [EXTERNAL] GRIA2 surface abundance determines synaptic AMPAR charge transfer and spine stability via regulated endocytosis [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971))
- **GRIA3**: [EXTERNAL] [EXTERNAL] GRIA3 gating is tuned by TARPs and cornichon proteins to modulate excitatory synaptic strength [PMID:21172611](https://pubmed.ncbi.nlm.nih.gov/21172611/). ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971))
- **GRID2**: [INFERENCE] [INFERENCE] GRID2 cooperates with AMPARs to set postsynaptic gain in cerebellar circuits. ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971))

#### Statistical Context

[DATA] AMPA glutamate receptor activity is highly enriched ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971); FDR 8.55e-03; 56.6-fold; 3 genes), consistent with dominant glutamatergic mechanisms.

---

### Theme 19: prepulse inhibition

**Summary:** prepulse inhibition ([GO:0060134](http://purl.obolibrary.org/obo/GO_0060134))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Prepulse inhibition reflects sensorimotor gating by which forewarning stimuli suppress subsequent responses, relying on cerebello–striatal–cortical synaptic timing. [INFERENCE] GRID2 and GRIA3 tune cerebellar synaptic gain that contributes to the temporal precision required for gating. [INFERENCE] CNTNAP2 and CTNNA2 influence network connectivity and inhibitory balance that modulate PPI strength.

#### Key Insights

- [INFERENCE] Properly timed excitatory drive and inhibitory control across cortico–striato–pallido–pontine loops underlie PPI [GO:0060134](http://purl.obolibrary.org/obo/GO_0060134). ([GO:0060134](http://purl.obolibrary.org/obo/GO_0060134))

#### Key Genes

- **GRID2**: [INFERENCE] [INFERENCE] GRID2-dependent cerebellar signaling shapes timing precision necessary for sensorimotor gating. ([GO:0060134](http://purl.obolibrary.org/obo/GO_0060134))
- **CTNNA2**: [INFERENCE] [INFERENCE] CTNNA2 couples adhesion to cytoskeletal stability to maintain pathways supporting PPI. ([GO:0060134](http://purl.obolibrary.org/obo/GO_0060134))
- **CNTNAP2**: [INFERENCE] [INFERENCE] CNTNAP2-dependent axonal domain integrity modulates long-range synchrony impacting gating. ([GO:0060134](http://purl.obolibrary.org/obo/GO_0060134))

#### Statistical Context

[DATA] Prepulse inhibition is enriched ([GO:0060134](http://purl.obolibrary.org/obo/GO_0060134); FDR 8.62e-03; 42.4-fold; 3 genes), indicating focused behavioral circuitry components.

---

### Theme 20: anterograde trans-synaptic signaling

**Summary:** anterograde trans-synaptic signaling ([GO:0098916](http://purl.obolibrary.org/obo/GO_0098916))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Anterograde trans-synaptic signaling covers presynaptic release programs and postsynaptic potential tuning that transmit information across synapses. [EXTERNAL] RIMS2 and RIMS1 organize active zones to couple Ca2+ channels to docked vesicles, accelerating Ca2+-triggered exocytosis and sustaining neurotransmission [PMID:15217342](https://pubmed.ncbi.nlm.nih.gov/15217342/). [EXTERNAL] LRRK2 phosphorylates Snapin to diminish SNARE complex engagement and reduce release probability, directly regulating synaptic vesicle exocytosis [PMID:23949442](https://pubmed.ncbi.nlm.nih.gov/23949442/). [EXTERNAL] NLGN4X can dampen excitatory postsynaptic potentials, linking adhesion to postsynaptic gain control [PMID:19726642](https://pubmed.ncbi.nlm.nih.gov/19726642/).

#### Key Insights

- [DATA] Regulation of synaptic vesicle exocytosis sets release probability and short-term plasticity that define synaptic throughput [GO:2000300](http://purl.obolibrary.org/obo/GO_2000300). ([GO:2000300](http://purl.obolibrary.org/obo/GO_2000300))
- [DATA] Negative regulation of EPSP provides a postsynaptic brake aligning circuit gain with activity levels [GO:0090394](http://purl.obolibrary.org/obo/GO_0090394). ([GO:0090394](http://purl.obolibrary.org/obo/GO_0090394))

#### Key Genes

- **RIMS2**: [EXTERNAL] [EXTERNAL] RIMS2 scaffolds Ca2+ channels and vesicle tethers at active zones to enhance Ca2+-triggered exocytosis [PMID:15217342](https://pubmed.ncbi.nlm.nih.gov/15217342/). ([GO:2000300](http://purl.obolibrary.org/obo/GO_2000300))
- **LRRK2**: [EXTERNAL] [EXTERNAL] LRRK2 phosphorylation of Snapin weakens SNAP-25 interactions to reduce release-ready pool and exocytosis [PMID:23949442](https://pubmed.ncbi.nlm.nih.gov/23949442/). ([GO:2000300](http://purl.obolibrary.org/obo/GO_2000300))
- **PTPRN2**: [INFERENCE] [INFERENCE] PTPRN2 modulates presynaptic protein phosphorylation states to regulate neurotransmitter secretion efficiency. ([GO:0007269](http://purl.obolibrary.org/obo/GO_0007269))
- **CASK**: [INFERENCE] [INFERENCE] CASK links release machinery to scaffold networks to maintain efficient anterograde signaling. ([GO:0098916](http://purl.obolibrary.org/obo/GO_0098916))

#### Statistical Context

[DATA] Anterograde trans-synaptic signaling is enriched ([GO:0098916](http://purl.obolibrary.org/obo/GO_0098916); FDR 1.40e-02; 4.2-fold; 11 genes), with strong signals for vesicle exocytosis and postsynaptic potential regulation.

---

### Theme 21: regulation of neuronal action potential

**Summary:** regulation of neuronal action potential ([GO:0098908](http://purl.obolibrary.org/obo/GO_0098908))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of neuronal action potential centers on the NALCN channelosome that provides sodium leak to set excitability baselines. [EXTERNAL] NALCN, UNC79, and UNC80 assemble a channelosome that generates depolarizing Na+ leak, modulating firing across circuits controlling respiration, locomotion, and pain [PMID:34929720](https://pubmed.ncbi.nlm.nih.gov/34929720/). [INFERENCE] Structural stabilization by UNC79/UNC80 ensures proper trafficking and gating of NALCN to maintain reliable action potential generation thresholds.

#### Key Insights

- [DATA] Tonic Na+ leak via the NALCN complex tunes resting potential and spike probability [GO:0098908](http://purl.obolibrary.org/obo/GO_0098908). ([GO:0098908](http://purl.obolibrary.org/obo/GO_0098908))

#### Key Genes

- **NALCN**: [EXTERNAL] [EXTERNAL] NALCN conducts persistent Na+ leak that stabilizes resting potential and shapes firing patterns [PMID:34929720](https://pubmed.ncbi.nlm.nih.gov/34929720/). ([GO:0098908](http://purl.obolibrary.org/obo/GO_0098908))
- **UNC79**: [EXTERNAL] [EXTERNAL] UNC79 is essential for NALCN complex integrity and neuronal action potential regulation [PMID:34929720](https://pubmed.ncbi.nlm.nih.gov/34929720/). ([GO:0098908](http://purl.obolibrary.org/obo/GO_0098908))
- **UNC80**: [EXTERNAL] [EXTERNAL] UNC80 scaffolds NALCN to sustain leak current and excitability control [PMID:34929720](https://pubmed.ncbi.nlm.nih.gov/34929720/). ([GO:0098908](http://purl.obolibrary.org/obo/GO_0098908))

#### Statistical Context

[DATA] Regulation of neuronal action potential is enriched ([GO:0098908](http://purl.obolibrary.org/obo/GO_0098908); FDR 1.60e-02; 33.9-fold; 3 genes), highlighting the NALCN channelosome.

---

### Theme 22: symmetric, GABA-ergic, inhibitory synapse

**Summary:** symmetric, GABA-ergic, inhibitory synapse ([GO:0098983](http://purl.obolibrary.org/obo/GO_0098983))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Symmetric GABAergic inhibitory synapses require trans-synaptic adhesion to assemble and maintain inhibitory receptor clusters. [EXTERNAL] NLGN4X and NLGN4Y are linked to inhibitory synapses, aligning adhesion with postsynaptic receptor recruitment and inhibitory tone [PMID:21838267](https://pubmed.ncbi.nlm.nih.gov/21838267/). [INFERENCE] Proper inhibitory synapse formation counterbalances excitation to stabilize network dynamics and behavior.

#### Key Insights

- [DATA] Enrichment for inhibitory synapse components underscores adhesion-driven organization of GABAergic postsynapses [GO:0098983](http://purl.obolibrary.org/obo/GO_0098983). ([GO:0098983](http://purl.obolibrary.org/obo/GO_0098983))

#### Key Genes

- **NLGN4X**: [EXTERNAL] [EXTERNAL] NLGN4X supports assembly of symmetric inhibitory synapses through trans-synaptic adhesion [PMID:21838267](https://pubmed.ncbi.nlm.nih.gov/21838267/). ([GO:0098983](http://purl.obolibrary.org/obo/GO_0098983))
- **NLGN4Y**: [EXTERNAL] [EXTERNAL] NLGN4Y contributes to GABAergic synapse maturation and inhibitory signaling strength [PMID:21838267](https://pubmed.ncbi.nlm.nih.gov/21838267/). ([GO:0098983](http://purl.obolibrary.org/obo/GO_0098983))

#### Statistical Context

[DATA] Symmetric, GABA-ergic, inhibitory synapse is enriched ([GO:0098983](http://purl.obolibrary.org/obo/GO_0098983); FDR 1.76e-02; 56.6-fold; 2 genes), indicating selective inhibitory adhesion modules.

---

### Theme 23: cell adhesion mediator activity

**Summary:** cell adhesion mediator activity ([GO:0098631](http://purl.obolibrary.org/obo/GO_0098631))  · Anchor confidence: **FDR<0.05**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 1.82e-02 · **Genes (7)**: ADGRL3, CNTN1, CNTN6, LRRC4C, NLGN4X, NLGN4Y, NTNG1

---

### Theme 24: cytoskeleton

**Summary:** cytoskeleton ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] The cytoskeleton theme encompasses actin–microtubule systems and motors that position synaptic machinery and shape neuronal morphology. [EXTERNAL] DENND2A activates Rab GTPases that interface with the actin cytoskeleton, coordinating membrane trafficking with cytoskeletal remodeling [PMID:20937701](https://pubmed.ncbi.nlm.nih.gov/20937701/). [EXTERNAL] PEAK1-centered signaling controls actin cytoskeleton dynamics and focal adhesion turnover, illustrating how kinase hubs tune motility and structure [PMID:23105102](https://pubmed.ncbi.nlm.nih.gov/23105102/); [PMID:20534451](https://pubmed.ncbi.nlm.nih.gov/20534451/). [INFERENCE] MYO10 and NAV2 drive cargo transport along actin and microtubules to deliver synaptic components to growing processes.

#### Key Insights

- [INFERENCE] Actin turnover and microtubule stabilization coordinate to target receptors and channels to synaptic domains [GO:0005856](http://purl.obolibrary.org/obo/GO_0005856). ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))

#### Key Genes

- **DENND2A**: [EXTERNAL] [EXTERNAL] DENND2A functions as a Rab GEF to couple membrane traffic with actin cytoskeleton remodeling [PMID:20937701](https://pubmed.ncbi.nlm.nih.gov/20937701/). ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **MYO10**: [INFERENCE] [INFERENCE] MYO10 transports cargos along actin to assemble protrusions and deliver synaptic components. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **NAV2**: [INFERENCE] [INFERENCE] NAV2 coordinates microtubule-based transport and focal adhesion dynamics to support neurite extension. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))
- **CARMIL1**: [INFERENCE] [INFERENCE] CARMIL1 regulates actin capping activities to tune protrusive dynamics and membrane trafficking. ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856))

#### Statistical Context

[DATA] Cytoskeleton is enriched ([GO:0005856](http://purl.obolibrary.org/obo/GO_0005856); FDR 1.94e-02; 2.2-fold; 21 genes), highlighting transport and remodeling systems that support synaptic structure.

---

### Theme 25: presynaptic active zone

**Summary:** presynaptic active zone ([GO:0048786](http://purl.obolibrary.org/obo/GO_0048786))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Presynaptic active zones are nanodomains that dock, prime, and release synaptic vesicles by tightly coupling Ca2+ channels to fusion machinery. [EXTERNAL] RIMS1/2 scaffold Ca2+ channels and SNARE regulators to accelerate Ca2+-triggered exocytosis and sustain high-frequency neurotransmission [PMID:15217342](https://pubmed.ncbi.nlm.nih.gov/15217342/). [INFERENCE] Liprin family member PPFIA2 stabilizes active zone architecture and interfaces with transport machinery to maintain vesicle supply.

#### Key Insights

- [DATA] Presynaptic active zone membranes concentrate Ca2+ channels adjacent to docked vesicles to maximize release efficacy [GO:0048787](http://purl.obolibrary.org/obo/GO_0048787). ([GO:0048787](http://purl.obolibrary.org/obo/GO_0048787))
- [DATA] Cytoplasmic active zone components organize vesicle priming and fusion cycles for reliable transmission [GO:0098831](http://purl.obolibrary.org/obo/GO_0098831). ([GO:0098831](http://purl.obolibrary.org/obo/GO_0098831))

#### Key Genes

- **RIMS2**: [EXTERNAL] [EXTERNAL] RIMS2 positions Ca2+ channels and primes vesicles to boost Ca2+-evoked exocytosis at active zones [PMID:15217342](https://pubmed.ncbi.nlm.nih.gov/15217342/). ([GO:0048786](http://purl.obolibrary.org/obo/GO_0048786))
- **RIMS1**: [EXTERNAL] [EXTERNAL] RIMS1 organizes active zone release sites to maintain synchronous transmitter release [PMID:15217342](https://pubmed.ncbi.nlm.nih.gov/15217342/). ([GO:0048786](http://purl.obolibrary.org/obo/GO_0048786))
- **PPFIA2**: [EXTERNAL] [EXTERNAL] PPFIA2 supports active zone architecture and links to cargo capture at postsynaptic sites [PMID:15217342](https://pubmed.ncbi.nlm.nih.gov/15217342/); [PMID:30021165](https://pubmed.ncbi.nlm.nih.gov/30021165/). ([GO:0048786](http://purl.obolibrary.org/obo/GO_0048786))

#### Statistical Context

[DATA] Presynaptic active zone is enriched ([GO:0048786](http://purl.obolibrary.org/obo/GO_0048786); FDR 2.12e-02; 10.3-fold; 4 genes), with additional leaves at active zone membrane and cytoplasmic components.

---

### Theme 26: regulation of neural precursor cell proliferation

**Summary:** regulation of neural precursor cell proliferation ([GO:2000177](http://purl.obolibrary.org/obo/GO_2000177))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of neural precursor cell proliferation coordinates trophic signaling and intracellular effectors to balance stem cell expansion with differentiation. [EXTERNAL] DISC1 promotes neuroblast proliferation via GSK3β/β-catenin modulation, linking developmental risk genes to progenitor pool maintenance [PMID:19303846](https://pubmed.ncbi.nlm.nih.gov/19303846/). [EXTERNAL] LRRK2 variants impair adult neurogenesis and neuroblast proliferation, indicating kinase control over progenitor dynamics [PMID:21168496](https://pubmed.ncbi.nlm.nih.gov/21168496/). [INFERENCE] NTRK3 trophic signaling engages MAPK/ERK cascades to drive precursor proliferation and survival in developing niches.

#### Key Insights

- [INFERENCE] Kinase and trophic receptor crosstalk tunes progenitor proliferation to match circuit growth demands [GO:2000177](http://purl.obolibrary.org/obo/GO_2000177). ([GO:2000177](http://purl.obolibrary.org/obo/GO_2000177))

#### Key Genes

- **DISC1**: [EXTERNAL] [EXTERNAL] DISC1 enhances neural progenitor proliferation via GSK3β/β-catenin pathway regulation [PMID:19303846](https://pubmed.ncbi.nlm.nih.gov/19303846/). ([GO:2000177](http://purl.obolibrary.org/obo/GO_2000177))
- **LRRK2**: [EXTERNAL] [EXTERNAL] LRRK2 G2019S perturbs adult neurogenesis and neuroblast proliferation in vivo [PMID:21168496](https://pubmed.ncbi.nlm.nih.gov/21168496/). ([GO:2000177](http://purl.obolibrary.org/obo/GO_2000177))
- **NTRK3**: [INFERENCE] [INFERENCE] NTRK3 activation of MAPK/ERK promotes neural precursor proliferation and survival. ([GO:2000177](http://purl.obolibrary.org/obo/GO_2000177))
- **PTPRZ1**: [INFERENCE] [INFERENCE] PTPRZ1 modulates growth factor signaling thresholds that influence precursor proliferation in neurogenic zones. ([GO:2000177](http://purl.obolibrary.org/obo/GO_2000177))

#### Statistical Context

[DATA] Regulation of neural precursor cell proliferation is enriched ([GO:2000177](http://purl.obolibrary.org/obo/GO_2000177); FDR 2.78e-02; 9.9-fold; 5 genes), consistent with neurogenic signaling modules.

---

### Theme 27: cell-cell junction

**Summary:** cell-cell junction ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Cell–cell junctions include adherens and tight junction complexes that integrate adhesion with polarity and signaling. [EXTERNAL] ANK3 is required for epithelial lateral membrane biogenesis and tight junction organization, highlighting ankyrin scaffolding in junctional polarity [PMID:14757759](https://pubmed.ncbi.nlm.nih.gov/14757759/). [EXTERNAL] MarvelD3–MEKK1–JNK coupling demonstrates how tight junction components connect to stress and proliferation signaling through MAP3K1 [PMID:24567356](https://pubmed.ncbi.nlm.nih.gov/24567356/). [EXTERNAL] PDZD2 localizes to junction-associated compartments and undergoes proteolytic processing, implicating PDZ scaffolds in junctional signaling and secretion [PMID:12671685](https://pubmed.ncbi.nlm.nih.gov/12671685/).

#### Key Insights

- [INFERENCE] Adherens and tight junction scaffolds coordinate cytoskeletal linkage with signaling pathways that regulate barrier function [GO:0005911](http://purl.obolibrary.org/obo/GO_0005911). ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))

#### Key Genes

- **MAP3K1**: [EXTERNAL] [EXTERNAL] MAP3K1 links tight junction components to JNK signaling to regulate cell behavior and survival [PMID:24567356](https://pubmed.ncbi.nlm.nih.gov/24567356/). ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **ANK3**: [EXTERNAL] [EXTERNAL] ANK3 is necessary for lateral membrane biogenesis and tight junction integrity in epithelia [PMID:14757759](https://pubmed.ncbi.nlm.nih.gov/14757759/). ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **PDZD2**: [EXTERNAL] [EXTERNAL] PDZD2 is a multi-PDZ scaffold undergoing regulated cleavage, associating with junctional signaling pathways [PMID:12671685](https://pubmed.ncbi.nlm.nih.gov/12671685/). ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))
- **CASK**: [EXTERNAL] [EXTERNAL] CASK influences proliferation and adhesion in keratinocytes, reflecting MAGUK roles at cell–cell junctions [PMID:18664494](https://pubmed.ncbi.nlm.nih.gov/18664494/). ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911))

#### Statistical Context

[DATA] Cell–cell junction is enriched ([GO:0005911](http://purl.obolibrary.org/obo/GO_0005911); FDR 3.22e-02; 2.8-fold; 13 genes), indicating polarity and adhesion scaffolding within the set.

---

### Theme 28: collagen type IV trimer

**Summary:** collagen type IV trimer ([GO:0005587](http://purl.obolibrary.org/obo/GO_0005587))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Collagen type IV trimers compose basement membranes that regulate tissue architecture and signaling microenvironments. [EXTERNAL] COL4A3 encodes a type IV collagen chain that assembles into trimers with anti-angiogenic properties and structural support functions in vascular basement membranes [PMID:10766752](https://pubmed.ncbi.nlm.nih.gov/10766752/). [EXTERNAL] COL4A4 provides an essential chain in collagen IV networks that stabilize basement membranes and modulate endothelial behavior [PMID:7523402](https://pubmed.ncbi.nlm.nih.gov/7523402/).

#### Key Insights

- [INFERENCE] Basement membrane collagen IV regulates diffusion, growth factor presentation, and mechanotransduction at tissue interfaces [GO:0005587](http://purl.obolibrary.org/obo/GO_0005587). ([GO:0005587](http://purl.obolibrary.org/obo/GO_0005587))

#### Key Genes

- **COL4A3**: [EXTERNAL] [EXTERNAL] COL4A3 forms part of collagen IV trimers that stabilize basement membranes and constrain angiogenesis [PMID:10766752](https://pubmed.ncbi.nlm.nih.gov/10766752/). ([GO:0005587](http://purl.obolibrary.org/obo/GO_0005587))
- **COL4A4**: [EXTERNAL] [EXTERNAL] COL4A4 contributes to collagen IV network assembly and vascular basement membrane integrity [PMID:7523402](https://pubmed.ncbi.nlm.nih.gov/7523402/). ([GO:0005587](http://purl.obolibrary.org/obo/GO_0005587))

#### Statistical Context

[DATA] Collagen type IV trimer is enriched ([GO:0005587](http://purl.obolibrary.org/obo/GO_0005587); FDR 3.77e-02; 37.7-fold; 2 genes), indicating basement membrane components in the set.

---

### Theme 29: basal dendrite

**Summary:** basal dendrite ([GO:0097441](http://purl.obolibrary.org/obo/GO_0097441))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Basal dendrite highlights dendritic subdomains specialized for local integration and input segregation. [INFERENCE] MAP2 stabilizes microtubules within basal dendrites to support branching, cargo transport, and receptor positioning that tune input integration. [INFERENCE] SLC4A10 regulates intracellular pH and ionic balance in dendrites, indirectly modulating excitability and plasticity.

#### Key Insights

- [INFERENCE] Dendritic microtubule stabilization and pH regulation sustain basal dendrite structure–function coupling [GO:0097441](http://purl.obolibrary.org/obo/GO_0097441). ([GO:0097441](http://purl.obolibrary.org/obo/GO_0097441))

#### Key Genes

- **MAP2**: [INFERENCE] [INFERENCE] MAP2 maintains basal dendrite architecture and transport routes essential for synaptic reception. ([GO:0097441](http://purl.obolibrary.org/obo/GO_0097441))
- **SLC4A10**: [INFERENCE] [INFERENCE] SLC4A10 supports dendritic pH homeostasis that influences receptor function and excitability. ([GO:0097441](http://purl.obolibrary.org/obo/GO_0097441))

#### Statistical Context

[DATA] Basal dendrite is enriched ([GO:0097441](http://purl.obolibrary.org/obo/GO_0097441); FDR 3.77e-02; 37.7-fold; 2 genes), pointing to compartment-specific dendritic mechanisms.

---

### Theme 30: endocytic vesicle

**Summary:** endocytic vesicle ([GO:0030139](http://purl.obolibrary.org/obo/GO_0030139))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Endocytic vesicles mediate receptor and membrane cargo internalization to balance signaling and supply presynaptic and postsynaptic demands. [EXTERNAL] MTSS1 couples actin remodeling to endocytic vesicle dynamics, supporting curvature generation and cargo internalization [PMID:12570871](https://pubmed.ncbi.nlm.nih.gov/12570871/). [EXTERNAL] RAB31 is recruited to phagocytic/endocytic vesicles to coordinate maturation steps via Rab cascades, exemplifying vesicle identity control [PMID:21255211](https://pubmed.ncbi.nlm.nih.gov/21255211/). [INFERENCE] EGFR and SH3KBP1 cooperate with clathrin adaptors to internalize ligand–receptor complexes and route them for signaling or degradation.

#### Key Insights

- [INFERENCE] Activity-dependent endocytosis regulates receptor abundance and synaptic strength [GO:0030139](http://purl.obolibrary.org/obo/GO_0030139). ([GO:0030139](http://purl.obolibrary.org/obo/GO_0030139))

#### Key Genes

- **MTSS1**: [EXTERNAL] [EXTERNAL] MTSS1 links actin dynamics to endocytic membrane remodeling to drive vesicle formation [PMID:12570871](https://pubmed.ncbi.nlm.nih.gov/12570871/). ([GO:0030139](http://purl.obolibrary.org/obo/GO_0030139))
- **RAB31**: [EXTERNAL] [EXTERNAL] RAB31 participates in endocytic vesicle maturation via Rab recruitment cascades [PMID:21255211](https://pubmed.ncbi.nlm.nih.gov/21255211/). ([GO:0030139](http://purl.obolibrary.org/obo/GO_0030139))
- **EGFR**: [INFERENCE] [INFERENCE] EGFR internalization via clathrin routes channels signaling and downregulation through endocytic vesicles. ([GO:0030139](http://purl.obolibrary.org/obo/GO_0030139))
- **SH3KBP1**: [INFERENCE] [INFERENCE] SH3KBP1 scaffolds endocytic adaptors to coordinate cargo capture and vesicle budding. ([GO:0030139](http://purl.obolibrary.org/obo/GO_0030139))

#### Statistical Context

[DATA] Endocytic vesicle is enriched ([GO:0030139](http://purl.obolibrary.org/obo/GO_0030139); FDR 3.77e-02; 4.4-fold; 7 genes), consistent with active receptor and cargo turnover mechanisms.

---

## Hub Genes

- **LRRK2**: [EXTERNAL] [EXTERNAL] LRRK2 phosphorylates Snapin to reduce SNARE engagement and synaptic vesicle exocytosis, while supporting axonal vesicular trafficking and neuronal cell body maintenance to coordinate excitability and connectivity [PMID:23949442](https://pubmed.ncbi.nlm.nih.gov/23949442/); [PMID:17120249](https://pubmed.ncbi.nlm.nih.gov/17120249/); [PMID:21696411](https://pubmed.ncbi.nlm.nih.gov/21696411/).
- **GRM5**: [INFERENCE] [INFERENCE] GRM5 activates phospholipase C signaling to elevate intracellular Ca2+, modulating postsynaptic integration and plasticity across hippocampal and cortical synapses.
- **ANK3**: [EXTERNAL] [EXTERNAL] ANK3 anchors voltage-gated sodium channels at the axon initial segment and contributes to epithelial tight junction organization, coupling excitability hubs to junctional polarity [PMID:14757759](https://pubmed.ncbi.nlm.nih.gov/14757759/).
- **CNTNAP2**: [EXTERNAL] [EXTERNAL] CNTNAP2 organizes juxtaparanodes for K+ channel clustering and shapes social/vocal behaviors via network wiring effects, linking axonal domain biology to behavior [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/); [PMID:19896112](https://pubmed.ncbi.nlm.nih.gov/19896112/); [PMID:10624965](https://pubmed.ncbi.nlm.nih.gov/10624965/).
- **NRXN1**: [EXTERNAL] [EXTERNAL] NRXN1 acts presynaptically to stabilize release sites and regulate neurotransmission, with dosage effects impacting learning and social communication [PMID:19896112](https://pubmed.ncbi.nlm.nih.gov/19896112/).
- **GRID2**: [EXTERNAL] [EXTERNAL] GRID2 integrates into synaptic organizer complexes and coordinates delta receptor signaling to promote excitatory synapse assembly and cerebellar function [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/); [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/).
- **CTNNA2**: [INFERENCE] [INFERENCE] CTNNA2 links adhesion complexes to actin, stabilizing synapses and long-range projections that contribute to cerebellar and cortical circuit maturation.
- **GRIA2**: [EXTERNAL] [EXTERNAL] GRIA2 controls fast excitatory transmission and is dynamically endocytosed to reset synaptic gain, supporting CA1 plasticity and network computation [PMID:21221849](https://pubmed.ncbi.nlm.nih.gov/21221849/); [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/); [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/).
- **NLGN4X**: [EXTERNAL] [EXTERNAL] NLGN4X mediates trans-synaptic adhesion and can dampen EPSPs, with glycosylation tuning synaptic abundance and variants disrupting social communication [PMID:19726642](https://pubmed.ncbi.nlm.nih.gov/19726642/); [PMID:37865312](https://pubmed.ncbi.nlm.nih.gov/37865312/).
- **CNTN6**: [INFERENCE] [INFERENCE] CNTN6 directs cell–cell adhesion during axon targeting and synapse stabilization, coordinating cerebellar and cortical circuit assembly.
- **KCND2**: [EXTERNAL] [EXTERNAL] KCND2-encoded Kv4.2 generates A-type K+ currents that repolarize dendrites and constrain firing, with scaffolding to actin positioning channels in spines [PMID:24811166](https://pubmed.ncbi.nlm.nih.gov/24811166/); [PMID:11102480](https://pubmed.ncbi.nlm.nih.gov/11102480/); [PMID:35597238](https://pubmed.ncbi.nlm.nih.gov/35597238/).
- **SCN1A**: [EXTERNAL] [EXTERNAL] SCN1A mediates Nav-dependent depolarization essential for spike initiation and propagation, gating excitability across neuronal compartments [PMID:27207958](https://pubmed.ncbi.nlm.nih.gov/27207958/).
- **GRIA3**: [EXTERNAL] [EXTERNAL] GRIA3-containing AMPARs mediate fast Na+/Ca2+ influx and are tuned by TARPs to calibrate synaptic charge transfer and cerebellar signaling [PMID:21172611](https://pubmed.ncbi.nlm.nih.gov/21172611/).
- **PRKCA**: [INFERENCE] [INFERENCE] PRKCA phosphorylates presynaptic and postsynaptic substrates to modulate release probability and receptor function, coupling neuromodulatory inputs to plasticity.
- **KCND3**: [EXTERNAL] [EXTERNAL] KCND3-encoded Kv4.3 contributes transient outward K+ currents that shape action potential repolarization and synaptic integration kinetics [PMID:21349352](https://pubmed.ncbi.nlm.nih.gov/21349352/); [PMID:26016905](https://pubmed.ncbi.nlm.nih.gov/26016905/).
- **PTPRZ1**: [EXTERNAL] [EXTERNAL] PTPRZ1 is a brain-enriched receptor-type phosphatase that supports perineuronal net integrity and modulates growth signaling influencing precursor proliferation [PMID:1323835](https://pubmed.ncbi.nlm.nih.gov/1323835/).
- **NTNG1**: [EXTERNAL] [EXTERNAL] NTNG1 forms an adhesion pair with NGL-1 to trigger synaptic maturation and stabilize excitatory contacts in hippocampal networks [PMID:23986473](https://pubmed.ncbi.nlm.nih.gov/23986473/).
- **RIMS1**: [EXTERNAL] [EXTERNAL] RIMS1 assembles active zones by tethering Ca2+ channels to docked vesicles, ensuring rapid, synchronous neurotransmitter release [PMID:15217342](https://pubmed.ncbi.nlm.nih.gov/15217342/).
- **PPFIA2**: [EXTERNAL] [EXTERNAL] PPFIA2 stabilizes spine morphology and couples cargo capture to postsynaptic sites, coordinating active zone and postsynaptic maturation [PMID:30021165](https://pubmed.ncbi.nlm.nih.gov/30021165/).
- **NLGN4Y**: [EXTERNAL] [EXTERNAL] NLGN4Y supports inhibitory synapse assembly with associations to social and vocal behaviors, indicating roles in E/I balance of behavioral circuits [PMID:18628683](https://pubmed.ncbi.nlm.nih.gov/18628683/); [PMID:21838267](https://pubmed.ncbi.nlm.nih.gov/21838267/).

## Overall Summary

[DATA] The 200-gene input reveals 163 enriched GO terms condensed into 30 themes, with strongest signals in synapse organization, postsynaptic nanodomains, ion channel complexes, and axonal architecture.

[INFERENCE] A unifying mechanism emerges in which adhesion-organizer complexes nucleate synapses, while AMPAR auxiliaries and Kv4 channelosomes calibrate charge transfer and repolarization to set circuit gain.

[INFERENCE] Presynaptic active zone scaffolds and LRRK2-dependent vesicle control couple release probability to postsynaptic responsiveness, integrating with NALCN-driven resting excitability to regulate firing.

[INFERENCE] ECM perineuronal nets, cytoskeletal transport, and progenitor proliferation control provide structural and developmental constraints that stabilize and adapt neural networks across behaviors.

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

