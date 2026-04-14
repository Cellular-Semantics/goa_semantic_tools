# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_6_themes.csv](Cluster_6_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-neuron-projection-development) | [neuron projection development](#theme-1-neuron-projection-development) [GO:0031175](http://purl.obolibrary.org/obo/GO_0031175) | BP | 1.51e-07 | 27 | FDR<0.01 |
| [2](#theme-2-axon) | [axon](#theme-2-axon) [GO:0030424](http://purl.obolibrary.org/obo/GO_0030424) | CC | 1.96e-07 | 20 | FDR<0.01 |
| [3](#theme-3-nervous-system-development) | [nervous system development](#theme-3-nervous-system-development) [GO:0007399](http://purl.obolibrary.org/obo/GO_0007399) | BP | 1.44e-05 | 44 | FDR<0.01 |
| [4](#theme-4-glutamatergic-synapse) | [glutamatergic synapse](#theme-4-glutamatergic-synapse) [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) | CC | 8.07e-05 | 19 | FDR<0.01 |
| [5](#theme-5-postsynaptic-density-membrane) | [postsynaptic density membrane](#theme-5-postsynaptic-density-membrane) [GO:0098839](http://purl.obolibrary.org/obo/GO_0098839) | CC | 1.12e-04 | 9 | FDR<0.01 |
| [6](#theme-6-dendrite) | [dendrite](#theme-6-dendrite) [GO:0030425](http://purl.obolibrary.org/obo/GO_0030425) | CC | 5.79e-04 | 23 | FDR<0.01 |
| [7](#theme-7-glial-cell-projection) | [glial cell projection](#theme-7-glial-cell-projection) [GO:0097386](http://purl.obolibrary.org/obo/GO_0097386) | CC | 1.37e-03 | 5 | FDR<0.01 |
| [8](#theme-8-neuronal-cell-body) | [neuronal cell body](#theme-8-neuronal-cell-body) [GO:0043025](http://purl.obolibrary.org/obo/GO_0043025) | CC | 1.40e-03 | 13 | FDR<0.01 |
| [9](#theme-9-modulation-of-chemical-synaptic-transmission) | [modulation of chemical synaptic transmission](#theme-9-modulation-of-chemical-synaptic-transmission) [GO:0050804](http://purl.obolibrary.org/obo/GO_0050804) | BP | 1.40e-03 | 16 | FDR<0.01 |
| [10](#theme-10-ionotropic-glutamate-receptor-signaling-pathway) | [ionotropic glutamate receptor signaling pathway](#theme-10-ionotropic-glutamate-receptor-signaling-pathway) [GO:0035235](http://purl.obolibrary.org/obo/GO_0035235) | BP | 2.29e-03 | 5 | FDR<0.01 |
| [11](#theme-11-specialized-extracellular-matrix) | [specialized extracellular matrix](#theme-11-specialized-extracellular-matrix) [GO:0140047](http://purl.obolibrary.org/obo/GO_0140047) | CC | 2.54e-03 | 4 | FDR<0.01 |
| [12](#theme-12-positive-regulation-of-cell-matrix-adhesion) | [positive regulation of cell-matrix adhesion](#theme-12-positive-regulation-of-cell-matrix-adhesion) [GO:0001954](http://purl.obolibrary.org/obo/GO_0001954) | BP | 2.64e-03 | 6 | FDR<0.01 |
| [13](#theme-13-adherens-junction) | [adherens junction](#theme-13-adherens-junction) [GO:0005912](http://purl.obolibrary.org/obo/GO_0005912) | CC | 3.12e-03 | 9 | FDR<0.01 |
| [14](#theme-14-regulation-of-membrane-potential) | [regulation of membrane potential](#theme-14-regulation-of-membrane-potential) [GO:0042391](http://purl.obolibrary.org/obo/GO_0042391) | BP | 3.37e-03 | 14 | FDR<0.01 |
| [15](#theme-15-cell-junction-organization) | [cell junction organization](#theme-15-cell-junction-organization) [GO:0034330](http://purl.obolibrary.org/obo/GO_0034330) | BP | 3.62e-03 | 27 | FDR<0.01 |
| [16](#theme-16-ampa-glutamate-receptor-complex) | [AMPA glutamate receptor complex](#theme-16-ampa-glutamate-receptor-complex) [GO:0032281](http://purl.obolibrary.org/obo/GO_0032281) | CC | 5.77e-03 | 4 | FDR<0.01 |
| [17](#theme-17-neural-crest-cell-migration) | [neural crest cell migration](#theme-17-neural-crest-cell-migration) [GO:0001755](http://purl.obolibrary.org/obo/GO_0001755) | BP | 6.68e-03 | 5 | FDR<0.01 |
| [18](#theme-18-anatomical-structure-formation-involved-in-morphogenesis) | [anatomical structure formation involved in morphogenesis](#theme-18-anatomical-structure-formation-involved-in-morphogenesis) [GO:0048646](http://purl.obolibrary.org/obo/GO_0048646) | BP | 1.03e-02 | 16 | FDR<0.05 |
| [19](#theme-19-transmitter-gated-channel-activity) | [transmitter-gated channel activity](#theme-19-transmitter-gated-channel-activity) [GO:0022835](http://purl.obolibrary.org/obo/GO_0022835) | MF | 1.14e-02 | 6 | FDR<0.05 |
| [20](#theme-20-heterophilic-cell-cell-adhesion) | [heterophilic cell-cell adhesion](#theme-20-heterophilic-cell-cell-adhesion) [GO:0007157](http://purl.obolibrary.org/obo/GO_0007157) | BP | 1.48e-02 | 5 | FDR<0.05 |
| [21](#theme-21-excitatory-synapse) | [excitatory synapse](#theme-21-excitatory-synapse) [GO:0060076](http://purl.obolibrary.org/obo/GO_0060076) | CC | 1.49e-02 | 5 | FDR<0.05 |
| [22](#theme-22-plasma-membrane-phospholipid-scrambling) | [plasma membrane phospholipid scrambling](#theme-22-plasma-membrane-phospholipid-scrambling) [GO:0017121](http://purl.obolibrary.org/obo/GO_0017121) | BP | 1.55e-02 | 4 | FDR<0.05 |
| [23](#theme-23-gaba-ergic-synapse) | [GABA-ergic synapse](#theme-23-gaba-ergic-synapse) [GO:0098982](http://purl.obolibrary.org/obo/GO_0098982) | CC | 1.86e-02 | 6 | FDR<0.05 |
| [24](#theme-24-regulation-of-mesenchymal-stem-cell-differentiation) | [regulation of mesenchymal stem cell differentiation](#theme-24-regulation-of-mesenchymal-stem-cell-differentiation) [GO:2000739](http://purl.obolibrary.org/obo/GO_2000739) | BP | 1.89e-02 | 3 | FDR<0.05 |
| [25](#theme-25-regulation-of-axon-extension) | [regulation of axon extension](#theme-25-regulation-of-axon-extension) [GO:0030516](http://purl.obolibrary.org/obo/GO_0030516) | BP | 2.85e-02 | 5 | FDR<0.05 |
| [26](#theme-26-side-of-membrane) | [side of membrane](#theme-26-side-of-membrane) [GO:0098552](http://purl.obolibrary.org/obo/GO_0098552) | CC | 3.27e-02 | 15 | FDR<0.05 |
| [27](#theme-27-regulation-of-sodium-ion-transport) | [regulation of sodium ion transport](#theme-27-regulation-of-sodium-ion-transport) [GO:0002028](http://purl.obolibrary.org/obo/GO_0002028) | BP | 3.41e-02 | 5 | FDR<0.05 |
| [28](#theme-28-axon-initial-segment) | [axon initial segment](#theme-28-axon-initial-segment) [GO:0043194](http://purl.obolibrary.org/obo/GO_0043194) | CC | 3.92e-02 | 3 | FDR<0.05 |
| [29](#theme-29-sodium-channel-complex) | [sodium channel complex](#theme-29-sodium-channel-complex) [GO:0034706](http://purl.obolibrary.org/obo/GO_0034706) | CC | 3.92e-02 | 3 | FDR<0.05 |
| [30](#theme-30-sodium-channel-activity) | [sodium channel activity](#theme-30-sodium-channel-activity) [GO:0005272](http://purl.obolibrary.org/obo/GO_0005272) | MF | 3.99e-02 | 5 | FDR<0.05 |

---

### Theme 1: neuron projection development

**Summary:** neuron projection development ([GO:0031175](http://purl.obolibrary.org/obo/GO_0031175))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Neuron projection development integrates axon guidance cues with intrinsic cytoskeletal remodeling to extend, branch, and stabilize axons and dendrites in defined trajectories and target fields. [EXTERNAL] Rho-ROCK pathway modulation shapes growth cone actomyosin contractility and promotes neurite extension, aligning with positive regulation of neuron projection development and downstream synaptic maturation [PMID:27160703](https://pubmed.ncbi.nlm.nih.gov/27160703/). [GO-HIERARCHY] The enriched child term axon guidance refines the anchor by specifying ligand–receptor signaling that biases growth cone turning decisions, while positive regulation of neuron projection development captures transcriptional and epigenetic programs that lift brakes on outgrowth. [INFERENCE] Coordinated engagement of guidance ligands with Rho family GTPase effectors and microtubule assembly machinery produces rapid filopodial sampling and polarized advance needed for long-range wiring.

#### Key Insights

- [GO-HIERARCHY] Axon guidance signals steer growth cones via Rho-GTPase control of actin and microtubules to realize neuron projection development. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))
- [EXTERNAL] Reducing ROCK activity lowers contractility and facilitates neurite extension, mechanistically explaining positive regulation of neuron projection development in this context [PMID:27160703](https://pubmed.ncbi.nlm.nih.gov/27160703/). ([GO:0010976](http://purl.obolibrary.org/obo/GO_0010976))
- [GO-HIERARCHY] Positive regulation of neuron projection development encompasses chromatin and transcriptional mechanisms that increase expression of cytoskeletal and adhesion modules enabling stable projection growth. ([GO:0010976](http://purl.obolibrary.org/obo/GO_0010976))

#### Key Genes

- **NTN4**: [INFERENCE] [INFERENCE] NTN4 presents a laminin-related guidance cue that biases growth cone advance by engaging receptors to locally tune RhoA/Rac1 signaling, stabilizing microtubule invasion into leading filopodia and promoting axon extension. ([GO:0031175](http://purl.obolibrary.org/obo/GO_0031175))
- **DPYSL3**: [INFERENCE] [INFERENCE] DPYSL3 couples guidance receptor inputs to microtubule capture and actin–microtubule crosslinking in growth cones, thereby accelerating neurite elongation and stabilizing newly formed projections. ([GO:0031175](http://purl.obolibrary.org/obo/GO_0031175))
- **KAT2B**: [INFERENCE] [INFERENCE] KAT2B acetylates histones at neurodevelopmental loci to increase expression of cytoskeletal and adhesion effectors that lift intrinsic brakes on projection growth and branching. ([GO:0010976](http://purl.obolibrary.org/obo/GO_0010976))
- **SEMA6D**: [INFERENCE] [INFERENCE] SEMA6D delivers direction-selective guidance through Plexin-A signaling that elevates RhoA-driven actomyosin remodeling to bias growth cone turning and constrain or promote axon advance depending on context. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))

#### Statistical Context

[DATA] The theme neuron projection development ([GO:0031175](http://purl.obolibrary.org/obo/GO_0031175)) shows strong enrichment at FDR 1.51e-07 with 6.3-fold overrepresentation among 167 annotated input genes. [DATA] Child terms axon guidance ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411)) and positive regulation of neuron projection development ([GO:0010976](http://purl.obolibrary.org/obo/GO_0010976)) are also enriched, supporting both cue interpretation and intrinsic growth programs.

---

### Theme 2: axon

**Summary:** axon ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The axon compartment concentrates cargo trafficking, cytoskeletal scaffolds, and membrane proteins that support fast conduction and precise synaptic delivery. [INFERENCE] Long-range transport complexes and adhesion molecules cooperate to stabilize axonal shafts while positioning presynaptic sites along collaterals. [GO-HIERARCHY] Enrichment at the cellular component level indicates concerted localization of multiple cargos to the axonal domain, consistent with polarized neuronal biology.

#### Key Insights

- [GO-HIERARCHY] Axonal enrichment reflects polarized trafficking of ion channels, vesicles, and adhesion modules that enable long-range conduction and synapse formation. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- [INFERENCE] Microtubule-based motors and adaptors couple signaling endosomes and SV precursors to maintain axonal supply and synaptogenesis. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))

#### Key Genes

- **UNC80**: [INFERENCE] [INFERENCE] UNC80 scaffolds the NALCN channelosome and links it to cytoskeletal transport machinery, promoting axonal localization of cargoes that sustain excitability and presynaptic function. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **NCAM2**: [INFERENCE] [INFERENCE] NCAM2 mediates axon–axon and axon–target adhesion that stabilizes growth cones and supports fasciculation and correct pathway selection during outgrowth. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **CADM2**: [INFERENCE] [INFERENCE] CADM2 forms trans-synaptic adhesion that seeds axonal presynaptic assembly and aligns vesicle release sites with postsynaptic receptors. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **IGSF9B**: [INFERENCE] [INFERENCE] IGSF9B participates in axonal adhesion complexes that stabilize maturing axons and help specify inhibitory versus excitatory presynaptic identity. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))

#### Statistical Context

[DATA] The axon compartment ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424)) is enriched at FDR 1.96e-07 with 5.5-fold overrepresentation, consistent with broad axonal polarization of the submitted gene set. [DATA] Twenty genes map to this structure, indicating coordinated localization to the axonal domain.

---

### Theme 3: nervous system development

**Summary:** nervous system development ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Nervous system development integrates neurogenesis, cell-type specification, axon pathfinding, and synaptogenesis into a coherent program across central and peripheral compartments. [EXTERNAL] FGF homologous factors contribute to neural development programs, highlighting ligand–receptor and intracellular modulators that tune excitability during maturation [PMID:8790420](https://pubmed.ncbi.nlm.nih.gov/8790420/). [EXTERNAL] Rho-ROCK pathway suppression promotes neuronal differentiation and synaptogenesis, linking cytoskeletal dynamics to developmental timing and circuit assembly [PMID:27160703](https://pubmed.ncbi.nlm.nih.gov/27160703/). [GO-HIERARCHY] The enriched specific terms including oligodendrocyte differentiation, brain development, and peripheral nervous system development indicate coordinated patterning across neurons and glia.

#### Key Insights

- [GO-HIERARCHY] Enrichment for oligodendrocyte differentiation and brain development indicates concurrent maturation of neuronal circuits and myelinating glia. ([GO:0048709](http://purl.obolibrary.org/obo/GO_0048709))
- [EXTERNAL] Reduced ROCK activity facilitates neuronal differentiation and spine formation, aligning cytoskeletal remodeling with developmental progression [PMID:27160703](https://pubmed.ncbi.nlm.nih.gov/27160703/). ([GO:0050767](http://purl.obolibrary.org/obo/GO_0050767))
- [GO-HIERARCHY] Positive regulation of nervous system development captures transcriptional and signaling programs that accelerate synapse assembly and circuit refinement. ([GO:0051962](http://purl.obolibrary.org/obo/GO_0051962))

#### Key Genes

- **SOX10**: [INFERENCE] [INFERENCE] SOX10 drives neural crest and glial lineage programs by activating myelin and peripheral neuron gene networks, coordinating neuronal–glial co-development within the nervous system. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))
- **SOX8**: [INFERENCE] [INFERENCE] SOX8 modulates neurogenesis–gliogenesis decisions and cooperates with SOX partners to balance lineage commitment during brain development. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))
- **PTPRZ1**: [INFERENCE] [INFERENCE] PTPRZ1 dephosphorylates axon growth and progenitor signaling substrates, tuning responsiveness to extracellular cues during neuronal differentiation and pathfinding. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))
- **ERBB3**: [INFERENCE] [INFERENCE] ERBB3 engages neuregulin signaling in peripheral glia and neurons to promote survival and differentiation, supporting peripheral nervous system development. ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399))

#### Statistical Context

[DATA] Nervous system development ([GO:0007399](http://purl.obolibrary.org/obo/GO_0007399)) is enriched at FDR 1.44e-05 with 4.2-fold overrepresentation and 22 genes annotated, spanning neuron and glial maturation processes. [DATA] Multiple specific children including oligodendrocyte differentiation ([GO:0048709](http://purl.obolibrary.org/obo/GO_0048709)) and brain development ([GO:0007420](http://purl.obolibrary.org/obo/GO_0007420)) are significantly enriched, indicating multi-compartment developmental engagement.

---

### Theme 4: glutamatergic synapse

**Summary:** glutamatergic synapse ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Glutamatergic synapse enrichment reflects assembly of presynaptic release machinery, trans-synaptic organizers, and postsynaptic receptor–scaffold complexes enabling fast excitation. [DATA] IL1RAPL1 and ARHGAP22 are curated to glutamatergic synapses where IL1RAPL1 couples to PSD-95 and presynaptic organizers, and ARHGAP22 restrains RhoA to stabilize spine structure [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). [DATA] Kainate receptor subunits such as GRIK2 are integral to synaptic transmission and plasticity at excitatory synapses, linking ionotropic receptor diversity to circuit computation [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/). [GO-HIERARCHY] The cellular component focus specifies synaptic microdomain localization underpinning functional modulation captured in related biological process themes.

#### Key Insights

- [DATA] Synapse organizers at excitatory synapses scaffold PSD-95 and align presynaptic release sites with AMPAR/KAR nanodomains, enhancing transmission efficacy [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- [DATA] Kainate receptor diversity at glutamatergic synapses shapes short- and long-term plasticity, modulating presynaptic release and postsynaptic integration [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- [GO-HIERARCHY] Localization to the glutamatergic synapse underscores coordinated trafficking of adhesion molecules, Rho GTPase regulators, and receptor subunits within the excitatory synaptic cleft. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Key Genes

- **DLGAP1**: [INFERENCE] [INFERENCE] DLGAP1 binds PSD-95 and Shank to nucleate postsynaptic nanodomains, positioning AMPARs and signaling enzymes to tune quantal responses and plasticity. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **ARHGAP22**: [EXTERNAL] [DATA] ARHGAP22 attenuates RhoA signaling at excitatory synapses to stabilize actin-rich spines, supporting synapse maintenance and function [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **NXPH1**: [INFERENCE] [INFERENCE] NXPH1 engages presynaptic organizers to influence vesicle release probability and coordinate alignment with postsynaptic receptor fields at excitatory contacts. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Statistical Context

[DATA] Glutamatergic synapse ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978)) is enriched at FDR 8.07e-05 with 3.9-fold overrepresentation across 19 genes, indicating coordinated localization of presynaptic and postsynaptic organizers. [DATA] Curated gene–synapse annotations within this theme include IL1RAPL1 and ARHGAP22 with experimental support.

---

### Theme 5: postsynaptic density membrane

**Summary:** postsynaptic density membrane ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The postsynaptic density membrane concentrates ligand-gated receptors, tyrosine kinases, and adhesion molecules within a nanometer-scale scaffold that couples neurotransmitter binding to electrical and biochemical signaling. [DATA] GRID2 is localized to the postsynaptic density membrane and can be gated via mGlu1 signaling, demonstrating cross-talk between metabotropic and ionotropic pathways at the PSD membrane [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). [INFERENCE] Assembly of AMPAR and kainate receptor subunits alongside receptor tyrosine kinases such as ERBB4 enables rapid depolarization and activity-dependent plasticity coupling to intracellular cascades. [GO-HIERARCHY] The cellular component focus highlights the membrane plane of the PSD where conductance changes and receptor trafficking are orchestrated.

#### Key Insights

- [DATA] mGlu1-triggered gating of GRID2 at the PSD membrane exemplifies metabotropic–ionotropic coupling embedded in the postsynaptic density architecture [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- [GO-HIERARCHY] Receptor clustering within the PSD membrane elevates local receptor density and kinase access, amplifying synaptic signals into downstream plasticity. ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))

#### Key Genes

- **GPR158**: [EXTERNAL] [EXTERNAL] GPR158 modulates postsynaptic signaling in complexes that influence GluD2 gating downstream of mGlu1, tuning PSD membrane excitability [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **GRID2**: [EXTERNAL] [DATA] GRID2 resides at the postsynaptic density membrane and is gated by mGlu1 signaling, integrating organizer complexes with ion conduction at the PSD membrane [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **GRIA2**: [INFERENCE] [INFERENCE] GRIA2-containing AMPARs populate the PSD membrane where RNA editing and auxiliary subunits set Na+ permeability and trafficking kinetics to control EPSC amplitude and plasticity. ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))

#### Statistical Context

[DATA] Postsynaptic density membrane ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839)) is enriched at FDR 1.12e-04 with 8.8-fold overrepresentation across 9 genes, indicating strong concentration of receptor complexes at the PSD membrane. [DATA] Curated localization for GRID2 to this compartment supports the specificity of the signal.

---

### Theme 6: dendrite

**Summary:** dendrite ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Dendritic enrichment reflects specialization for synaptic input integration via spines, distal branches, and growth cones that house receptor nanodomains and local translation hubs. [EXTERNAL] ZNF804A localizes to MAP2-positive dendrites and dendritic spines, co-localizing with PSD-95 and GluN1, supporting a role in spine structure and postsynaptic organization [PMID:4438586](https://pubmed.ncbi.nlm.nih.gov/4438586/). [DATA] GRIA2 participates in dendritic spine biology where activity-dependent endocytosis remodels AMPAR content and synaptic efficacy [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). [GO-HIERARCHY] Child terms highlight spines for synaptic input, dendritic growth cones for pathfinding, and distal dendrites for compartmentalized signaling.

#### Key Insights

- [DATA] Dendritic spines concentrate glutamate receptors and scaffolds, enabling input-specific plasticity through regulated AMPAR trafficking [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))
- [GO-HIERARCHY] Dendritic growth cones interpret local cues to refine arborization, while distal dendrites support compartmentalized synaptic integration. ([GO:0044294](http://purl.obolibrary.org/obo/GO_0044294))

#### Key Genes

- **MAP2**: [EXTERNAL] [EXTERNAL] MAP2 stabilizes dendritic microtubules and shapes arborization, linking cytoskeletal organization to dendritic growth cone dynamics and branch maturation [PMID:20846339](https://pubmed.ncbi.nlm.nih.gov/20846339/). ([GO:0044294](http://purl.obolibrary.org/obo/GO_0044294))
- **SLC1A1**: [INFERENCE] [INFERENCE] SLC1A1 clears glutamate along dendritic shafts and distal dendrites, constraining spillover and protecting spines from excitotoxicity while preserving signal fidelity. ([GO:0150002](http://purl.obolibrary.org/obo/GO_0150002))
- **PDE4B**: [INFERENCE] [INFERENCE] PDE4B sculpts spine cAMP microdomains to control PKA-dependent phosphorylation of synaptic substrates, thereby tuning dendritic spine morphology and synaptic gain. ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))

#### Statistical Context

[DATA] Dendrite ([GO:0030425](http://purl.obolibrary.org/obo/GO_0030425)) is enriched at FDR 5.79e-04 with 3.8-fold overrepresentation across 16 genes, including strong enrichment for dendritic spine ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197)) and growth cone ([GO:0044294](http://purl.obolibrary.org/obo/GO_0044294)). [DATA] This pattern supports broad postsynaptic and arborization specialization in the input set.

---

### Theme 7: glial cell projection

**Summary:** glial cell projection ([GO:0097386](http://purl.obolibrary.org/obo/GO_0097386))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Glial cell projection enrichment highlights astrocytic and other glial processes that contact synapses and vasculature to regulate ionic milieu, neurotransmitter clearance, and metabolic support. [DATA] The H(+)-myo-inositol symporter SLC2A13 localizes to astrocyte end-feet, supplying inositol for osmotic balance and vesicle cycling in glial processes [PMID:11500374](https://pubmed.ncbi.nlm.nih.gov/11500374/). [INFERENCE] Coordinated cytoskeletal remodeling and transporter localization within glial projections underpins neuron–glia signaling and synaptic homeostasis.

#### Key Insights

- [DATA] Astrocyte end-foot inositol transport supports glial projection signaling and osmotic regulation critical for neurovascular and synaptic functions [PMID:11500374](https://pubmed.ncbi.nlm.nih.gov/11500374/). ([GO:0097386](http://purl.obolibrary.org/obo/GO_0097386))
- [GO-HIERARCHY] Enrichment of glial projections indicates coordinated placement of kinases and transporters that modulate perisynaptic ion and transmitter dynamics. ([GO:0097386](http://purl.obolibrary.org/obo/GO_0097386))

#### Key Genes

- **SLC2A13**: [EXTERNAL] [DATA] SLC2A13 transports myo-inositol into glial projections, fueling phosphoinositide signaling and osmoregulation at astrocyte end-feet [PMID:11500374](https://pubmed.ncbi.nlm.nih.gov/11500374/). ([GO:0097386](http://purl.obolibrary.org/obo/GO_0097386))
- **SIRT2**: [INFERENCE] [INFERENCE] SIRT2 deacetylates cytoskeletal regulators in glial processes, stabilizing projection morphology and positioning of transporters at perisynaptic sites. ([GO:0097386](http://purl.obolibrary.org/obo/GO_0097386))

#### Statistical Context

[DATA] Glial cell projection ([GO:0097386](http://purl.obolibrary.org/obo/GO_0097386)) is enriched at FDR 1.37e-03 with 16.4-fold overrepresentation across 5 genes, consistent with strong glial process localization in the dataset. [DATA] Presence of SLC2A13 with astrocyte end-foot annotation strengthens interpretability.

---

### Theme 8: neuronal cell body

**Summary:** neuronal cell body ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Neuronal cell body enrichment reflects concentration of biosynthetic machinery, ion channel pools, and transport hubs that feed axonal and dendritic compartments. [DATA] ZNF804A is localized to the neuronal soma in addition to dendrites, consistent with dual roles in transcriptional regulation and synaptic organization [PMID:27837918](https://pubmed.ncbi.nlm.nih.gov/27837918/). [DATA] SLC1A1 enriches in neuronal cell bodies to maintain glutamate homeostasis and protect against excitotoxicity by high-affinity reuptake [PMID:9409715](https://pubmed.ncbi.nlm.nih.gov/9409715/). [GO-HIERARCHY] The cell body focus complements axonal and dendritic enrichments, indicating whole-neuron polarization of the gene set.

#### Key Insights

- [DATA] Neuronal soma localization of ZNF804A suggests coupling of nuclear transcriptional programs with synapse-directed trafficking [PMID:27837918](https://pubmed.ncbi.nlm.nih.gov/27837918/). ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- [DATA] Cell body glutamate transport by SLC1A1 limits excitotoxic stress and shapes transmitter availability for local and distal synapses [PMID:9409715](https://pubmed.ncbi.nlm.nih.gov/9409715/). ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))

#### Key Genes

- **BRINP3**: [INFERENCE] [INFERENCE] BRINP3 supports soma–neurite structural integrity by organizing cytoskeletal regulators and synaptic protein trafficking hubs within the neuronal cell body. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **BRINP2**: [INFERENCE] [INFERENCE] BRINP2 modulates actin dynamics in the soma to influence spine precursor formation and delivery of components to dendrites. ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **ZNF804A**: [EXTERNAL] [DATA] ZNF804A localizes to neuronal cell bodies and dendrites, linking transcriptional control with synaptic structural regulation [PMID:27837918](https://pubmed.ncbi.nlm.nih.gov/27837918/). ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))
- **SLC1A1**: [EXTERNAL] [DATA] SLC1A1 concentrates in neuronal somata to clear extracellular glutamate and maintain synaptic homeostasis across neuronal territories [PMID:9409715](https://pubmed.ncbi.nlm.nih.gov/9409715/). ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025))

#### Statistical Context

[DATA] Neuronal cell body ([GO:0043025](http://purl.obolibrary.org/obo/GO_0043025)) is enriched at FDR 1.40e-03 with 4.2-fold overrepresentation across 13 genes, supporting soma-focused biosynthetic and homeostatic roles in the set. [DATA] Multiple soma-localized transporters and regulators underpin the signal.

---

### Theme 9: modulation of chemical synaptic transmission

**Summary:** modulation of chemical synaptic transmission ([GO:0050804](http://purl.obolibrary.org/obo/GO_0050804))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Modulation of chemical synaptic transmission encompasses presynaptic release probability, postsynaptic receptor gating, and perisynaptic regulation that tune synaptic strength. [DATA] Presynaptic kainate receptors containing GRIK2 modulate short-term plasticity and can positively regulate synaptic transmission at mossy fiber synapses, illustrating transmitter-gated control over release dynamics [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/). [DATA] Structural synapse organizers such as GRID2 participate in long-term synaptic depression, aligning structural complexes with enduring transmission changes [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/). [GO-HIERARCHY] This process theme interfaces with cellular component enrichments at excitatory synapses and PSD membranes to mechanistically explain functional outputs.

#### Key Insights

- [DATA] Presynaptic kainate receptors regulate short-term facilitation and influence release probability, directly modulating chemical synaptic transmission [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/). ([GO:0050804](http://purl.obolibrary.org/obo/GO_0050804))
- [DATA] Postsynaptic organizer GRID2 supports long-term synaptic depression, providing a structural route to lasting transmission changes [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/). ([GO:0050804](http://purl.obolibrary.org/obo/GO_0050804))

#### Key Genes

- **DLGAP1**: [INFERENCE] [INFERENCE] DLGAP1 organizes PSD signaling hubs that gate AMPAR trafficking and receptor phosphorylation, thereby modulating synaptic strength and plasticity. ([GO:0050804](http://purl.obolibrary.org/obo/GO_0050804))
- **GPR158**: [INFERENCE] [INFERENCE] GPR158 integrates metabotropic inputs to tune ionotropic receptor responsiveness, shaping postsynaptic gain during ongoing transmission. ([GO:0050804](http://purl.obolibrary.org/obo/GO_0050804))
- **GLRA3**: [INFERENCE] [INFERENCE] GLRA3-mediated chloride currents dampen local excitatory drive and rebalance network excitation–inhibition to modulate synaptic throughput. ([GO:0050804](http://purl.obolibrary.org/obo/GO_0050804))
- **C1QL1**: [INFERENCE] [INFERENCE] C1QL1 stabilizes synaptic contacts and promotes AMPAR clustering, elevating quantal content and reliability of excitatory transmission. ([GO:0050804](http://purl.obolibrary.org/obo/GO_0050804))

#### Statistical Context

[DATA] Modulation of chemical synaptic transmission ([GO:0050804](http://purl.obolibrary.org/obo/GO_0050804)) is enriched at FDR 1.40e-03 with 4.0-fold overrepresentation across 16 genes, capturing both presynaptic and postsynaptic regulators. [DATA] Curated roles for GRIK2 and GRID2 substantiate functional modulation within the set.

---

### Theme 10: ionotropic glutamate receptor signaling pathway

**Summary:** ionotropic glutamate receptor signaling pathway ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The ionotropic glutamate receptor signaling pathway conveys millisecond-scale excitation via AMPA, kainate, and delta receptor assemblies that convert glutamate binding into cation influx and downstream plasticity signaling. [DATA] GRIA2 participates in this pathway with structural and pharmacologic evidence supporting its central role in synaptic transmission and plasticity [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/); [PMID:20614889](https://pubmed.ncbi.nlm.nih.gov/20614889/). [GO-HIERARCHY] Co-enrichment of receptor subunits across AMPA, kainate, and delta classes indicates coordinated assembly and gating mechanisms shared within the ionotropic family.

#### Key Insights

- [DATA] AMPARs containing GRIA2 mediate fast EPSCs and are central to plasticity through regulated trafficking and auxiliary subunit modulation [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/). ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))
- [GO-HIERARCHY] Inclusion of kainate and delta subunits points to broader ionotropic diversity shaping kinetics and plasticity rules in the pathway. ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))

#### Key Genes

- **GRIA2**: [EXTERNAL] [DATA] GRIA2 drives ionotropic glutamate signaling with defined structures showing how auxiliary subunits shape gating and pharmacology [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/); [PMID:20614889](https://pubmed.ncbi.nlm.nih.gov/20614889/). ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))
- **GRIA3**: [INFERENCE] [INFERENCE] GRIA3 confers distinct AMPAR gating and trafficking properties that tune synaptic kinetics and Hebbian plasticity. ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))
- **GRIK2**: [INFERENCE] [INFERENCE] GRIK2-containing kainate receptors contribute to slower, modulatory ionotropic currents and presynaptic control of glutamate release within the same pathway. ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))

#### Statistical Context

[DATA] Ionotropic glutamate receptor signaling pathway ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235)) is enriched at FDR 2.29e-03 with 19.6-fold overrepresentation across 5 genes, dominated by AMPAR and KAR subunits. [DATA] Multiple independent lines of evidence for GRIA2 strengthen the pathway-level signal.

---

### Theme 11: specialized extracellular matrix

**Summary:** specialized extracellular matrix ([GO:0140047](http://purl.obolibrary.org/obo/GO_0140047))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Specialized extracellular matrix structures organize pericellular signaling and biophysics, with perineuronal nets stabilizing synapses and the interphotoreceptor matrix supporting photoreceptor homeostasis. [INFERENCE] Versican-rich perineuronal nets bind hyaluronan and link proteins to restrict synaptic remodeling and buffer ions around fast-spiking neurons. [INFERENCE] PTPRZ1 and Tenascin-R coordinate matrix assembly and receptor signaling at neuronal surfaces to balance plasticity with stability.

#### Key Insights

- [GO-HIERARCHY] Perineuronal nets constrain spine turnover and diffusion, maintaining circuit stability while modulating plasticity thresholds. ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))
- [GO-HIERARCHY] The interphotoreceptor matrix scaffolds photoreceptor outer segments and nutrient exchange to sustain vision. ([GO:0033165](http://purl.obolibrary.org/obo/GO_0033165))

#### Key Genes

- **VCAN**: [INFERENCE] [INFERENCE] VCAN assembles hyaluronan-based lattices that encase neurons, regulating ion buffering and receptor mobility to stabilize synaptic output. ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534))
- **EYS**: [INFERENCE] [INFERENCE] EYS contributes structural elements to the interphotoreceptor matrix, supporting photoreceptor alignment and outer segment maintenance. ([GO:0033165](http://purl.obolibrary.org/obo/GO_0033165))
- **PTPRZ1**: [INFERENCE] [INFERENCE] PTPRZ1 modulates cell–matrix signaling by dephosphorylating adhesion and growth regulators embedded in specialized neural ECM. ([GO:0140047](http://purl.obolibrary.org/obo/GO_0140047))

#### Statistical Context

[DATA] Specialized extracellular matrix ([GO:0140047](http://purl.obolibrary.org/obo/GO_0140047)) is enriched at FDR 2.54e-03 with 21.4-fold overrepresentation across 4 genes, with significant child enrichment for perineuronal net ([GO:0072534](http://purl.obolibrary.org/obo/GO_0072534)). [DATA] This indicates focal concentration of matrix organizers within the input set.

---

### Theme 12: positive regulation of cell-matrix adhesion

**Summary:** positive regulation of cell-matrix adhesion ([GO:0001954](http://purl.obolibrary.org/obo/GO_0001954))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Positive regulation of cell–matrix adhesion captures mechanisms that increase integrin activation, focal adhesion assembly, and matrix engagement to stabilize cell shape and signaling. [DATA] RIN2 promotes endothelial cell–matrix adhesion by coordinating integrin endocytosis and Rac signaling, enhancing adhesion maturation during morphogenesis [PMID:22825554](https://pubmed.ncbi.nlm.nih.gov/22825554/). [DATA] PTPRJ supports focal adhesion assembly by dephosphorylating targets that maintain integrin-driven adhesion and restrain motility [PMID:21091576](https://pubmed.ncbi.nlm.nih.gov/21091576/). [DATA] CDH13 elevates surface β1 integrin levels to enhance matrix adhesiveness, linking cadherin signaling to ECM engagement [PMID:17573778](https://pubmed.ncbi.nlm.nih.gov/17573778/).

#### Key Insights

- [DATA] Endocytic recycling of integrins via RIN2 amplifies adhesive strength and promotes matrix engagement during morphogenesis [PMID:22825554](https://pubmed.ncbi.nlm.nih.gov/22825554/). ([GO:0001954](http://purl.obolibrary.org/obo/GO_0001954))
- [DATA] Phosphatase PTPRJ sustains focal adhesion assembly to stabilize ECM attachment and suppress migratory escape [PMID:21091576](https://pubmed.ncbi.nlm.nih.gov/21091576/). ([GO:0001954](http://purl.obolibrary.org/obo/GO_0001954))

#### Key Genes

- **FERMT1**: [INFERENCE] [INFERENCE] FERMT1 binds integrin β tails to promote high-affinity conformations and recruit adhesion machinery, boosting cell–matrix adhesion. ([GO:0001954](http://purl.obolibrary.org/obo/GO_0001954))
- **RIN2**: [EXTERNAL] [DATA] RIN2 enhances endothelial cell–matrix adhesion through active integrin endocytosis and Rac signaling during angiogenic morphogenesis [PMID:22825554](https://pubmed.ncbi.nlm.nih.gov/22825554/). ([GO:0001954](http://purl.obolibrary.org/obo/GO_0001954))
- **CDH13**: [EXTERNAL] [DATA] CDH13 increases β1 integrin surface levels to strengthen cell–matrix adhesiveness and support tissue remodeling [PMID:17573778](https://pubmed.ncbi.nlm.nih.gov/17573778/). ([GO:0001954](http://purl.obolibrary.org/obo/GO_0001954))
- **PTPRJ**: [EXTERNAL] [DATA] PTPRJ promotes focal adhesion assembly and limits motility by dephosphorylating key adhesion regulators [PMID:21091576](https://pubmed.ncbi.nlm.nih.gov/21091576/). ([GO:0001954](http://purl.obolibrary.org/obo/GO_0001954))

#### Statistical Context

[DATA] Positive regulation of cell–matrix adhesion ([GO:0001954](http://purl.obolibrary.org/obo/GO_0001954)) is enriched at FDR 2.64e-03 with 12.9-fold overrepresentation across 6 genes, indicating a focused adhesion-enhancing module. [DATA] Multiple curated effectors converge on integrin activation and adhesion complex stabilization.

---

### Theme 13: adherens junction

**Summary:** adherens junction ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Adherens junction enrichment reflects cadherin–catenin complexes linking membranes to actin, integrating mechanical cues with growth and polarity pathways. [DATA] LIMD1 localizes to adherens junctions where Ajuba family adaptors negatively regulate Hippo signaling to connect adhesion with proliferation control [PMID:20303269](https://pubmed.ncbi.nlm.nih.gov/20303269/). [DATA] AJAP1 targets cadherin-mediated junctions and modulates junction dynamics as a membrane adaptor [PMID:14595118](https://pubmed.ncbi.nlm.nih.gov/14595118/). [DATA] CRB1 participates in photoreceptor junctional scaffolds, reinforcing epithelial polarity at adherens junctions [PMID:15914641](https://pubmed.ncbi.nlm.nih.gov/15914641/).

#### Key Insights

- [DATA] Adherens junction adaptors can tune Hippo signaling to translate mechanical adhesion into growth control [PMID:20303269](https://pubmed.ncbi.nlm.nih.gov/20303269/). ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))
- [DATA] Membrane adaptors at cadherin junctions stabilize linkage to actin and coordinate polarity complexes [PMID:14595118](https://pubmed.ncbi.nlm.nih.gov/14595118/); [PMID:15914641](https://pubmed.ncbi.nlm.nih.gov/15914641/). ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))

#### Key Genes

- **CTNNA3**: [INFERENCE] [INFERENCE] CTNNA3 bridges cadherins to actin, stabilizing adherens junctions and transmitting tension to downstream signaling pathways. ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))
- **LIMD1**: [EXTERNAL] [DATA] LIMD1 at adherens junctions couples adhesion to Hippo pathway repression, coordinating epithelial remodeling with growth restraint [PMID:20303269](https://pubmed.ncbi.nlm.nih.gov/20303269/). ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))
- **AJAP1**: [EXTERNAL] [DATA] AJAP1 targets cadherin-mediated junctions to regulate junctional stability and epithelial polarity [PMID:14595118](https://pubmed.ncbi.nlm.nih.gov/14595118/). ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))
- **CRB1**: [EXTERNAL] [DATA] CRB1 supports adherens junction scaffolding in photoreceptors to maintain polarity and tissue integrity [PMID:15914641](https://pubmed.ncbi.nlm.nih.gov/15914641/). ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912))

#### Statistical Context

[DATA] Adherens junction ([GO:0005912](http://purl.obolibrary.org/obo/GO_0005912)) is enriched at FDR 3.12e-03 with 5.4-fold overrepresentation across 9 genes, indicating robust engagement of junctional scaffolds and adaptors. [DATA] Multiple curated junction components substantiate this cellular component signal.

---

### Theme 14: regulation of membrane potential

**Summary:** regulation of membrane potential ([GO:0042391](http://purl.obolibrary.org/obo/GO_0042391))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Regulation of membrane potential integrates synaptic receptor currents with voltage-gated channel gating to set neuronal excitability in pre- and postsynaptic compartments. [DATA] SCN1A encodes a voltage-gated sodium channel critical for action potential initiation, directly shaping presynaptic membrane potential dynamics and excitability [PMID:27207958](https://pubmed.ncbi.nlm.nih.gov/27207958/). [INFERENCE] AMPAR and kainate receptor subunits regulate postsynaptic membrane potential through Na+-permeant currents whose amplitude and kinetics dictate depolarization and spike coupling. [GO-HIERARCHY] Child terms highlight both postsynaptic and presynaptic membrane potential control, indicating compartmental breadth.

#### Key Insights

- [DATA] Voltage-gated sodium channel activity via SCN1A sets the threshold and waveform of spikes that regulate presynaptic membrane potential and release [PMID:27207958](https://pubmed.ncbi.nlm.nih.gov/27207958/). ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505))
- [GO-HIERARCHY] Postsynaptic receptor-mediated cation influx determines EPSP size and temporal summation, regulating postsynaptic membrane potential. ([GO:0060078](http://purl.obolibrary.org/obo/GO_0060078))

#### Key Genes

- **GRIA3**: [INFERENCE] [INFERENCE] GRIA3-containing AMPARs drive rapid postsynaptic depolarization and shape summation by gating Na+ influx in response to glutamate. ([GO:0060078](http://purl.obolibrary.org/obo/GO_0060078))
- **GRIK2**: [INFERENCE] [INFERENCE] Presynaptic GRIK2-containing KARs modulate terminal excitability to tune membrane potential and transmitter release probability. ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505))
- **SCN1A**: [EXTERNAL] [EXTERNAL] SCN1A-mediated Na+ currents govern spike initiation and axonal conduction, directly controlling presynaptic membrane potential dynamics [PMID:27207958](https://pubmed.ncbi.nlm.nih.gov/27207958/). ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505))
- **P2RX7**: [INFERENCE] [INFERENCE] ATP-gated P2RX7 channels conduct Na+ and Ca2+, depolarizing membranes and adjusting excitability and downstream signaling in neural and glial cells. ([GO:0060078](http://purl.obolibrary.org/obo/GO_0060078))

#### Statistical Context

[DATA] Regulation of membrane potential ([GO:0042391](http://purl.obolibrary.org/obo/GO_0042391)) is enriched at FDR 3.37e-03 with 4.1-fold overrepresentation across 14 genes, including specific enrichment for postsynaptic ([GO:0060078](http://purl.obolibrary.org/obo/GO_0060078)) and presynaptic ([GO:0099505](http://purl.obolibrary.org/obo/GO_0099505)) control. [DATA] This distribution indicates coordinated tuning of excitability across compartments.

---

### Theme 15: cell junction organization

**Summary:** cell junction organization ([GO:0034330](http://purl.obolibrary.org/obo/GO_0034330))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Cell junction organization captures assembly, remodeling, and stabilization of synaptic and non-synaptic junctions through coordinated adhesion, cytoskeletal regulation, and signaling. [DATA] IL1RAPL1 regulates presynapse assembly and postsynapse organization by engaging PTPδ and RhoGAP2, linking adhesion with actin remodeling and functional maturation [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). [DATA] GRID2 contributes to excitatory synapse assembly via organizer complexes that stabilize postsynaptic architecture and align trans-synaptic partners [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/). [GO-HIERARCHY] Enriched children include regulation of synapse assembly and regulation of postsynapse organization, pinpointing synaptic junction control as a dominant signal.

#### Key Insights

- [DATA] IL1RAPL1 drives coordinated pre- and postsynaptic assembly, increasing active presynaptic compartments and mEPSC frequency [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- [DATA] GRID2-containing organizer complexes promote excitatory synapse assembly and structural stabilization [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/). ([GO:0051963](http://purl.obolibrary.org/obo/GO_0051963))

#### Key Genes

- **IL1RAPL1**: [EXTERNAL] [DATA] IL1RAPL1 orchestrates presynapse assembly and postsynapse organization via PTPδ and RhoGAP2 interactions, enhancing synaptic connectivity [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- **GRID2**: [EXTERNAL] [DATA] GRID2 integrates into synaptic organizer complexes to promote excitatory synapse assembly and alignment of trans-synaptic partners [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/). ([GO:0051963](http://purl.obolibrary.org/obo/GO_0051963))
- **DOCK10**: [INFERENCE] [INFERENCE] DOCK10 activates Rac1 to remodel actin at nascent junctions, stabilizing spine structure and supporting synapse assembly. ([GO:0051963](http://purl.obolibrary.org/obo/GO_0051963))
- **PRICKLE1**: [INFERENCE] [INFERENCE] PRICKLE1 interfaces with PSD scaffolds to position adhesion complexes and maintain postsynaptic density organization. ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))

#### Statistical Context

[DATA] Cell junction organization ([GO:0034330](http://purl.obolibrary.org/obo/GO_0034330)) is enriched at FDR 3.62e-03 with 4.0-fold overrepresentation across 14 genes, with significant children for postsynapse organization ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175)) and synapse assembly ([GO:0051963](http://purl.obolibrary.org/obo/GO_0051963)). [DATA] Multiple curated synaptic organizers substantiate the junctional focus.

---

### Theme 16: AMPA glutamate receptor complex

**Summary:** AMPA glutamate receptor complex ([GO:0032281](http://purl.obolibrary.org/obo/GO_0032281))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The AMPA glutamate receptor complex defines tetrameric assemblies that mediate fast synaptic excitation and are tuned by auxiliary subunits and scaffolds. [INFERENCE] Co-enrichment of GRIA2/3/4 and GRID2 indicates coordinated biogenesis and trafficking of AMPA-like assemblies into synapses where subunit composition sets Ca2+ permeability and kinetics. [GO-HIERARCHY] This cellular component theme links directly to ionotropic signaling and postsynaptic density membrane enrichment to explain functional excitation.

#### Key Insights

- [GO-HIERARCHY] AMPAR complex composition determines conductance, desensitization, and plasticity rules at excitatory synapses. ([GO:0032281](http://purl.obolibrary.org/obo/GO_0032281))
- [GO-HIERARCHY] Assembly with auxiliary proteins controls surface delivery and synaptic anchoring of AMPARs. ([GO:0032281](http://purl.obolibrary.org/obo/GO_0032281))

#### Key Genes

- **GRIA2**: [INFERENCE] [INFERENCE] GRIA2 sets AMPAR ion selectivity and trafficking behavior, governing EPSC amplitude and plasticity sensitivity. ([GO:0032281](http://purl.obolibrary.org/obo/GO_0032281))
- **GRIA3**: [INFERENCE] [INFERENCE] GRIA3 contributes distinct gating to AMPAR complexes that shape temporal integration and LTP/LTD induction thresholds. ([GO:0032281](http://purl.obolibrary.org/obo/GO_0032281))

#### Statistical Context

[DATA] AMPA glutamate receptor complex ([GO:0032281](http://purl.obolibrary.org/obo/GO_0032281)) is enriched at FDR 5.77e-03 with 15.7-fold overrepresentation across 4 genes, indicating concentrated representation of AMPAR subunits. [DATA] This enrichment mechanistically bridges receptor composition with synaptic function in the dataset.

---

### Theme 17: neural crest cell migration

**Summary:** neural crest cell migration ([GO:0001755](http://purl.obolibrary.org/obo/GO_0001755))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Neural crest cell migration requires epithelial–mesenchymal transition, contact guidance, and chemotaxis to reach diverse targets and generate multiple lineages. [INFERENCE] SOX10 and SOX8 activate adhesion and motility programs that enable delamination and directional movement from the neural tube. [INFERENCE] Semaphorin cues such as SEMA6D and SEMA5B deliver repulsive guidance via plexin signaling to sculpt migratory streams and prevent ectopic invasion.

#### Key Insights

- [GO-HIERARCHY] Transcriptional control and semaphorin–plexin guidance jointly drive neural crest delamination and directed migration. ([GO:0001755](http://purl.obolibrary.org/obo/GO_0001755))
- [GO-HIERARCHY] Integration of repulsion with substrate adhesion ensures proper routing of neural crest streams to target niches. ([GO:0001755](http://purl.obolibrary.org/obo/GO_0001755))

#### Key Genes

- **SOX10**: [INFERENCE] [INFERENCE] SOX10 programs EMT and motility by inducing adhesion modulators and cytoskeletal effectors that empower neural crest migration. ([GO:0001755](http://purl.obolibrary.org/obo/GO_0001755))
- **SEMA6D**: [INFERENCE] [INFERENCE] SEMA6D–plexin signaling imposes repulsive corridors that channel migrating neural crest cells along permissive paths. ([GO:0001755](http://purl.obolibrary.org/obo/GO_0001755))

#### Statistical Context

[DATA] Neural crest cell migration ([GO:0001755](http://purl.obolibrary.org/obo/GO_0001755)) is enriched at FDR 6.68e-03 with 14.4-fold overrepresentation across 5 genes, reflecting a focused migratory guidance module. [DATA] Representation of SOX and semaphorin families supports combined transcriptional and guidance control.

---

### Theme 18: anatomical structure formation involved in morphogenesis

**Summary:** anatomical structure formation involved in morphogenesis ([GO:0048646](http://purl.obolibrary.org/obo/GO_0048646))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Anatomical structure formation involved in morphogenesis encompasses cellular rearrangements, ECM remodeling, and growth factor signaling that sculpt tissues. [DATA] CALCRL mediates intermedin-driven pro-angiogenic signaling through VEGF pathways, coupling GPCR activity to vascular morphogenesis during tissue formation [PMID:20596610](https://pubmed.ncbi.nlm.nih.gov/20596610/). [INFERENCE] Rho GTPase regulators and planar cell polarity effectors orchestrate convergent extension and epithelial remodeling to shape organ architecture. [GO-HIERARCHY] Enrichment reflects both vascular and neural morphogenetic programs that integrate with adhesion and synapse assembly themes.

#### Key Insights

- [DATA] Intermedin–CALCRL signaling promotes endothelial proliferation and survival through VEGF pathways to drive angiogenic morphogenesis [PMID:20596610](https://pubmed.ncbi.nlm.nih.gov/20596610/). ([GO:0048646](http://purl.obolibrary.org/obo/GO_0048646))
- [GO-HIERARCHY] Cytoskeletal control via Rho GAPs enables cell shape change and rearrangements essential for tissue morphogenesis. ([GO:0048646](http://purl.obolibrary.org/obo/GO_0048646))

#### Key Genes

- **RBPJ**: [INFERENCE] [INFERENCE] RBPJ transduces Notch signals to coordinate differentiation and boundary formation, guiding tissue patterning during morphogenesis. ([GO:0048646](http://purl.obolibrary.org/obo/GO_0048646))
- **CALCRL**: [EXTERNAL] [DATA] CALCRL activation by intermedin engages VEGF-dependent pathways to promote angiogenesis integral to organ morphogenesis [PMID:20596610](https://pubmed.ncbi.nlm.nih.gov/20596610/). ([GO:0048646](http://purl.obolibrary.org/obo/GO_0048646))
- **ARHGAP24**: [INFERENCE] [INFERENCE] ARHGAP24 attenuates RhoA to permit actin reorganization and cell intercalation movements required for tissue shaping. ([GO:0048646](http://purl.obolibrary.org/obo/GO_0048646))
- **PDGFRA**: [INFERENCE] [INFERENCE] PDGFRA signaling drives mesenchymal proliferation and migration that populate and pattern developing structures during morphogenesis. ([GO:0048646](http://purl.obolibrary.org/obo/GO_0048646))

#### Statistical Context

[DATA] Anatomical structure formation involved in morphogenesis ([GO:0048646](http://purl.obolibrary.org/obo/GO_0048646)) is enriched at FDR 1.03e-02 with 3.2-fold overrepresentation across 16 genes, consistent with combined vascular and neural tissue-shaping programs. [DATA] Angiogenic and cytoskeletal regulators co-occur within this theme.

---

### Theme 19: transmitter-gated channel activity

**Summary:** transmitter-gated channel activity ([GO:0022835](http://purl.obolibrary.org/obo/GO_0022835))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Transmitter-gated channel activity captures ligand-gated ion channels that convert neurotransmitter binding into ion fluxes controlling postsynaptic potentials and excitability. [DATA] GRIA2 mediates AMPA receptor activity central to fast synaptic transmission and is dynamically regulated by endocytosis during plasticity [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). [DATA] GRID2 exhibits transmitter-gated monoatomic ion channel activity that is triggered via mGlu1 signaling, expanding the repertoire of glutamate-driven currents at synapses [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). [DATA] AMPAR subunits GRIA3 and GRIA4 are curated for AMPA glutamate receptor activity, underscoring multi-subunit contribution to gating diversity [PMID:21172611](https://pubmed.ncbi.nlm.nih.gov/21172611/).

#### Key Insights

- [DATA] AMPA receptor activity by GRIA2/3/4 underlies rapid EPSCs and is tuned by auxiliary proteins and phosphorylation [PMID:21172611](https://pubmed.ncbi.nlm.nih.gov/21172611/); [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971))
- [DATA] GRID2 participates in mGlu1-triggered ion channel gating contributing to regulation of postsynaptic membrane potential [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). ([GO:1904315](http://purl.obolibrary.org/obo/GO_1904315))

#### Key Genes

- **GRIA2**: [EXTERNAL] [DATA] GRIA2 confers AMPA glutamate receptor activity that drives Na+ influx for fast excitation and plasticity remodeling [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971))
- **GRID2**: [EXTERNAL] [DATA] GRID2 operates as a transmitter-gated ion channel regulated by mGlu1 to modulate postsynaptic membrane potential [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). ([GO:1904315](http://purl.obolibrary.org/obo/GO_1904315))

#### Statistical Context

[DATA] Transmitter-gated channel activity ([GO:0022835](http://purl.obolibrary.org/obo/GO_0022835)) is enriched at FDR 1.14e-02 with 11.2-fold overrepresentation across 6 genes, including significant AMPA receptor activity ([GO:0004971](http://purl.obolibrary.org/obo/GO_0004971)). [DATA] Together these annotations indicate robust representation of ligand-gated cation channels.

---

### Theme 20: heterophilic cell-cell adhesion

**Summary:** heterophilic cell-cell adhesion ([GO:0007157](http://purl.obolibrary.org/obo/GO_0007157))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Heterophilic cell–cell adhesion relies on distinct ligand–receptor pairs to establish specific intercellular contacts that pattern circuits and immune synapses. [DATA] ALCAM engages CD6 to form stable contacts and promote sustained signaling, exemplifying long-term heterophilic adhesion essential for functional responses [PMID:16352806](https://pubmed.ncbi.nlm.nih.gov/16352806/). [INFERENCE] LSAMP and OPCML mediate selective neuronal adhesion to specify synaptic partner choice and compartmental organization.

#### Key Insights

- [DATA] Prolonged ALCAM–CD6 engagement stabilizes conjugates and sustains signaling, illustrating durable heterophilic adhesion [PMID:16352806](https://pubmed.ncbi.nlm.nih.gov/16352806/). ([GO:0007157](http://purl.obolibrary.org/obo/GO_0007157))
- [GO-HIERARCHY] Neuronal Ig superfamily members provide target-selective adhesion that shapes synaptic maps. ([GO:0007157](http://purl.obolibrary.org/obo/GO_0007157))

#### Key Genes

- **ALCAM**: [EXTERNAL] [DATA] ALCAM mediates heterophilic adhesion with CD6 to stabilize contacts and sustain downstream signaling [PMID:16352806](https://pubmed.ncbi.nlm.nih.gov/16352806/). ([GO:0007157](http://purl.obolibrary.org/obo/GO_0007157))
- **LSAMP**: [INFERENCE] [INFERENCE] LSAMP supports selective neurite adhesion that partitions axonal pathways and refines synaptic partner selection. ([GO:0007157](http://purl.obolibrary.org/obo/GO_0007157))
- **OPCML**: [INFERENCE] [INFERENCE] OPCML forms heterophilic interactions that contribute to neuronal surface organization and circuit specificity. ([GO:0007157](http://purl.obolibrary.org/obo/GO_0007157))

#### Statistical Context

[DATA] Heterophilic cell–cell adhesion ([GO:0007157](http://purl.obolibrary.org/obo/GO_0007157)) is enriched at FDR 1.48e-02 with 11.6-fold overrepresentation across 5 genes, reflecting a focused adhesion code. [DATA] The presence of ALCAM with curated heterophilic function anchors this theme.

---

### Theme 21: excitatory synapse

**Summary:** excitatory synapse ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Excitatory synapse enrichment denotes loci of glutamatergic transmission where receptor composition and cAMP signaling coordinate plasticity. [INFERENCE] PDE4B constrains synaptic cAMP to regulate AMPAR phosphorylation and trafficking, linking second messenger dynamics to long-term changes. [INFERENCE] C1QL1 promotes receptor clustering and synapse stabilization to enhance excitatory throughput and reliability.

#### Key Insights

- [GO-HIERARCHY] Coupling of receptor nanodomains with cAMP modulators enables input-specific tuning of excitatory synaptic strength. ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))
- [DATA] GRIA2 localizes to excitatory synapses where Aβ-induced AMPAR endocytosis disrupts transmission, highlighting sensitivity of these compartments [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))

#### Key Genes

- **PDE4B**: [INFERENCE] [INFERENCE] PDE4B sculpts synaptic cAMP microdomains to control AMPAR phosphorylation cycles and stabilize potentiated states at excitatory synapses. ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))
- **C1QL1**: [INFERENCE] [INFERENCE] C1QL1 organizes postsynaptic receptor clusters and strengthens synaptic apposition to elevate excitatory synapse efficacy. ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))

#### Statistical Context

[DATA] Excitatory synapse ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076)) is enriched at FDR 1.49e-02 with 8.3-fold overrepresentation across 5 genes, consistent with concentrated excitatory postsynaptic specialization. [DATA] Co-occurrence with AMPAR pathway themes supports mechanistic coherence.

---

### Theme 22: plasma membrane phospholipid scrambling

**Summary:** plasma membrane phospholipid scrambling ([GO:0017121](http://purl.obolibrary.org/obo/GO_0017121))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Plasma membrane phospholipid scrambling collapses lipid asymmetry to expose phosphatidylserine and facilitate signaling, vesiculation, and cell clearance. [DATA] P2RX7 activation triggers macrophage phospholipid scrambling and membrane blebbing, supporting innate immune responses via downstream scramblases [PMID:25651887](https://pubmed.ncbi.nlm.nih.gov/25651887/). [DATA] SERINC5 promotes phospholipid scrambling that disrupts viral envelope asymmetry, restricting HIV-1 infectivity when incorporated into virions [PMID:37474505](https://pubmed.ncbi.nlm.nih.gov/37474505/). [GO-HIERARCHY] This process intersects apoptosis, immunity, and membrane repair pathways relevant to neuronal–glial interactions under stress.

#### Key Insights

- [DATA] ATP-gated P2RX7 initiates scramblase activation leading to PS exposure and membrane remodeling in innate immunity [PMID:25651887](https://pubmed.ncbi.nlm.nih.gov/25651887/). ([GO:0017121](http://purl.obolibrary.org/obo/GO_0017121))
- [DATA] SERINC5-driven scrambling disrupts viral envelope architecture to limit infectivity, illustrating the functional output of asymmetry collapse [PMID:37474505](https://pubmed.ncbi.nlm.nih.gov/37474505/). ([GO:0017121](http://purl.obolibrary.org/obo/GO_0017121))

#### Key Genes

- **XKR4**: [INFERENCE] [INFERENCE] XKR4 functions as a scramblase that collapses lipid asymmetry downstream of receptor signaling to promote PS exposure. ([GO:0017121](http://purl.obolibrary.org/obo/GO_0017121))
- **SERINC5**: [EXTERNAL] [DATA] SERINC5 induces lipid scrambling that perturbs HIV-1 membrane asymmetry and reduces infectivity when incorporated into virions [PMID:37474505](https://pubmed.ncbi.nlm.nih.gov/37474505/). ([GO:0017121](http://purl.obolibrary.org/obo/GO_0017121))
- **P2RX7**: [EXTERNAL] [DATA] P2RX7 activation triggers phospholipid scrambling with membrane blebbing and apoptosis that augment phagocytic clearance [PMID:25651887](https://pubmed.ncbi.nlm.nih.gov/25651887/). ([GO:0017121](http://purl.obolibrary.org/obo/GO_0017121))

#### Statistical Context

[DATA] Plasma membrane phospholipid scrambling ([GO:0017121](http://purl.obolibrary.org/obo/GO_0017121)) is enriched at FDR 1.55e-02 with 17.5-fold overrepresentation across 4 genes, highlighting a focused membrane remodeling module. [DATA] Multiple curated actors substantiate functional scrambling within the set.

---

### Theme 23: GABA-ergic synapse

**Summary:** GABA-ergic synapse ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] GABA-ergic synapse enrichment captures inhibitory junctions where GABA receptors and adhesion complexes organize release and reception to balance excitation. [INFERENCE] IGSF9B contributes to trans-synaptic alignment of presynaptic neurexins with postsynaptic scaffolds to stabilize inhibitory synapses. [INFERENCE] NXPH1 and ERBB4 influence inhibitory circuit maturation and synaptic efficacy by modulating adhesion and receptor signaling at GABAergic contacts.

#### Key Insights

- [GO-HIERARCHY] Inhibitory synapse assembly relies on adhesion codes that align GABA release sites with receptor clusters to ensure precise shunting inhibition. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))
- [DATA] DISC1 localizes to GABA-ergic synapses in human cortex, illustrating shared scaffolding principles across inhibitory contacts [PMID:16736468](https://pubmed.ncbi.nlm.nih.gov/16736468/). ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))

#### Key Genes

- **IGSF9B**: [INFERENCE] [INFERENCE] IGSF9B stabilizes inhibitory junctions by bridging presynaptic and postsynaptic partners to maintain release–receptor alignment. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))
- **NXPH1**: [INFERENCE] [INFERENCE] NXPH1 modulates presynaptic properties to regulate GABA release probability and inhibitory tone. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))
- **ERBB4**: [INFERENCE] [INFERENCE] ERBB4 signaling in interneurons tunes inhibitory synapse development and GABAergic transmission strength. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))

#### Statistical Context

[DATA] GABA-ergic synapse ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982)) is enriched at FDR 1.86e-02 with 6.1-fold overrepresentation across 6 genes, indicating representation of inhibitory junction regulators. [DATA] Cross-referenced presence of DISC1 in curated annotations supports the theme’s biological plausibility.

---

### Theme 24: regulation of mesenchymal stem cell differentiation

**Summary:** regulation of mesenchymal stem cell differentiation ([GO:2000739](http://purl.obolibrary.org/obo/GO_2000739))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of mesenchymal stem cell differentiation highlights transcriptional and receptor tyrosine kinase programs that bias lineage commitment. [DATA] SOX5 and SOX6 co-operatively enhance chondrogenic differentiation from MSCs, elevating cartilage marker expression and promoting lineage entry [PMID:21401405](https://pubmed.ncbi.nlm.nih.gov/21401405/). [DATA] PDGFRA signaling modulates MSC differentiation through downstream ERK/PI3K pathways, with altered receptor ubiquitination influencing osteogenic commitment [PMID:21596750](https://pubmed.ncbi.nlm.nih.gov/21596750/). [GO-HIERARCHY] This process interfaces with morphogenesis and adhesion themes by controlling progenitor fate and matrix interactions.

#### Key Insights

- [DATA] SOX trio activity drives chondrogenic MSC differentiation by elevating cartilage gene programs [PMID:21401405](https://pubmed.ncbi.nlm.nih.gov/21401405/). ([GO:2000739](http://purl.obolibrary.org/obo/GO_2000739))
- [DATA] PDGFRA signaling biases MSC fate via ERK/PI3K cascades and ubiquitination-dependent receptor control [PMID:21596750](https://pubmed.ncbi.nlm.nih.gov/21596750/). ([GO:2000739](http://purl.obolibrary.org/obo/GO_2000739))

#### Key Genes

- **SOX5**: [EXTERNAL] [DATA] SOX5 potentiates chondrogenic programs in MSCs, especially with SOX6/9, to promote lineage commitment [PMID:21401405](https://pubmed.ncbi.nlm.nih.gov/21401405/). ([GO:2000739](http://purl.obolibrary.org/obo/GO_2000739))
- **SOX6**: [EXTERNAL] [DATA] SOX6 activates chondrogenic markers and cooperates within the SOX trio to reinforce MSC differentiation toward cartilage [PMID:21401405](https://pubmed.ncbi.nlm.nih.gov/21401405/). ([GO:2000739](http://purl.obolibrary.org/obo/GO_2000739))
- **PDGFRA**: [EXTERNAL] [DATA] PDGFRA regulates MSC differentiation via ERK/PI3K signaling, with reduced Cbl-mediated ubiquitination enhancing osteogenic output [PMID:21596750](https://pubmed.ncbi.nlm.nih.gov/21596750/). ([GO:2000739](http://purl.obolibrary.org/obo/GO_2000739))

#### Statistical Context

[DATA] Regulation of mesenchymal stem cell differentiation ([GO:2000739](http://purl.obolibrary.org/obo/GO_2000739)) is enriched at FDR 1.89e-02 with 32.1-fold overrepresentation across 3 genes, indicating a compact, high-specificity differentiation module. [DATA] The presence of both transcriptional and RTK controllers strengthens interpretability.

---

### Theme 25: regulation of axon extension

**Summary:** regulation of axon extension ([GO:0030516](http://purl.obolibrary.org/obo/GO_0030516))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of axon extension integrates repulsive and attractive cues with cytoskeletal effectors to set growth cone advance rates and trajectory persistence. [DATA] NRCAM contributes to regulation of axon extension as a cell adhesion molecule that coordinates interactions at the external side of the plasma membrane to guide outgrowth [PMID:8812479](https://pubmed.ncbi.nlm.nih.gov/8812479/). [INFERENCE] SLIT–ROBO repulsion and netrin receptor complexes tune Rho GTPase activity and microtubule advance to throttle extension in space and time. [GO-HIERARCHY] This process theme complements neuron projection development by emphasizing rate control and directionality mechanisms.

#### Key Insights

- [DATA] Adhesion receptor NRCAM modulates axon extension by stabilizing growth cone–substrate contacts and signaling through its cytoplasmic domain [PMID:8812479](https://pubmed.ncbi.nlm.nih.gov/8812479/). ([GO:0030516](http://purl.obolibrary.org/obo/GO_0030516))
- [GO-HIERARCHY] Repulsive and attractive gradients converge on Rho GTPase and microtubule targeting to regulate extension speed and turning. ([GO:0030516](http://purl.obolibrary.org/obo/GO_0030516))

#### Key Genes

- **SLIT1**: [INFERENCE] [INFERENCE] SLIT1 provides midline-derived repulsion via ROBO receptors to restrict axon advance and sculpt trajectories. ([GO:0030516](http://purl.obolibrary.org/obo/GO_0030516))
- **NRCAM**: [EXTERNAL] [DATA] NRCAM regulates axon extension by mediating cell–cell and cell–matrix adhesion that coordinates growth cone advance [PMID:8812479](https://pubmed.ncbi.nlm.nih.gov/8812479/). ([GO:0030516](http://purl.obolibrary.org/obo/GO_0030516))

#### Statistical Context

[DATA] Regulation of axon extension ([GO:0030516](http://purl.obolibrary.org/obo/GO_0030516)) is enriched at FDR 2.85e-02 with 9.8-fold overrepresentation across 5 genes, underscoring targeted control of growth dynamics. [DATA] Curated adhesion input from NRCAM anchors this regulatory signal.

---

### Theme 26: side of membrane

**Summary:** side of membrane ([GO:0098552](http://purl.obolibrary.org/obo/GO_0098552))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Side of membrane enrichment highlights asymmetric placement of proteins on the external or cytoplasmic leaflet that dictates trafficking, signaling, and adhesion. [DATA] AJAP1 localizes to the cytoplasmic side of the plasma membrane where it interfaces with endocytic machinery to regulate receptor abundance and junctional dynamics [PMID:14595118](https://pubmed.ncbi.nlm.nih.gov/14595118/). [DATA] PKP4 is enriched at the cytoplasmic side during cytokinesis to regulate Rho signaling and membrane remodeling, exemplifying leaflet-specific function [PMID:17115030](https://pubmed.ncbi.nlm.nih.gov/17115030/). [GO-HIERARCHY] External side enrichments for adhesion molecules complement internal adaptors to establish directional signaling across the bilayer.

#### Key Insights

- [DATA] Cytoplasmic leaflet adaptors such as PKP4 gate Rho signaling and endocytosis to remodel membrane composition and mechanics [PMID:17115030](https://pubmed.ncbi.nlm.nih.gov/17115030/). ([GO:0098552](http://purl.obolibrary.org/obo/GO_0098552))
- [DATA] Membrane-sided localization of AJAP1 links cadherin junctions to internalization pathways, tuning cell–cell adhesion [PMID:14595118](https://pubmed.ncbi.nlm.nih.gov/14595118/). ([GO:0098552](http://purl.obolibrary.org/obo/GO_0098552))

#### Key Genes

- **AJAP1**: [EXTERNAL] [DATA] AJAP1 resides on the cytoplasmic side of the membrane to regulate endocytosis and cadherin-junction dynamics [PMID:14595118](https://pubmed.ncbi.nlm.nih.gov/14595118/). ([GO:0098552](http://purl.obolibrary.org/obo/GO_0098552))
- **PKP4**: [EXTERNAL] [DATA] PKP4 targets the cytoplasmic membrane side to control Rho-dependent cytokinesis and membrane remodeling [PMID:17115030](https://pubmed.ncbi.nlm.nih.gov/17115030/). ([GO:0098552](http://purl.obolibrary.org/obo/GO_0098552))
- **OPCML**: [INFERENCE] [INFERENCE] OPCML is positioned on the external side to mediate heterophilic adhesion and receptor organization at the cell surface. ([GO:0098552](http://purl.obolibrary.org/obo/GO_0098552))

#### Statistical Context

[DATA] Side of membrane ([GO:0098552](http://purl.obolibrary.org/obo/GO_0098552)) is enriched at FDR 3.27e-02 with 2.6-fold overrepresentation across 15 genes, indicating systematic leaflet-specific localization. [DATA] Both cytoplasmic and external sided proteins contribute to the signal.

---

### Theme 27: regulation of sodium ion transport

**Summary:** regulation of sodium ion transport ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Regulation of sodium ion transport comprises modulators of Na+ channels and pumps that set excitability, cardiac rhythm, and ionic homeostasis. [DATA] FGF12 regulates voltage-gated sodium channel activity, tuning Nav gating and thereby influencing Na+ influx during excitability disorders [PMID:27164707](https://pubmed.ncbi.nlm.nih.gov/27164707/). [DATA] DMD stabilizes membrane microdomains that support sodium channel function, and its loss perturbs Na+ handling in dystrophic cardiomyocytes [PMID:21677768](https://pubmed.ncbi.nlm.nih.gov/21677768/). [DATA] PRKCE inhibits the Na+/K+ pump via PKC–NADPH oxidase signaling to reduce Na+ extrusion and modulate intracellular Na+ load [PMID:19193863](https://pubmed.ncbi.nlm.nih.gov/19193863/). [DATA] P2RX7 impacts sodium ion transport through ATP-gated cation channel activity relevant to neuronal–immune signaling [PMID:17785580](https://pubmed.ncbi.nlm.nih.gov/17785580/).

#### Key Insights

- [DATA] FGF12-dependent modulation of Nav channels alters sodium influx and excitability, directly regulating sodium ion transport [PMID:27164707](https://pubmed.ncbi.nlm.nih.gov/27164707/). ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))
- [DATA] PKCε signaling can depress Na+/K+ pump activity to tune cellular Na+ homeostasis in stress states [PMID:19193863](https://pubmed.ncbi.nlm.nih.gov/19193863/). ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))

#### Key Genes

- **FGF12**: [EXTERNAL] [DATA] FGF12 modulates voltage-gated sodium channel gating to regulate Na+ entry and neuronal excitability [PMID:27164707](https://pubmed.ncbi.nlm.nih.gov/27164707/). ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))
- **DMD**: [EXTERNAL] [DATA] Dystrophin deficiency disrupts sodium channel function and Na+ handling in cardiomyocytes, evidencing regulation of sodium ion transport [PMID:21677768](https://pubmed.ncbi.nlm.nih.gov/21677768/). ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))
- **PRKCE**: [EXTERNAL] [DATA] PRKCE activation inhibits the Na+/K+ pump via NADPH oxidase, reducing Na+ extrusion and altering Na+ balance [PMID:19193863](https://pubmed.ncbi.nlm.nih.gov/19193863/). ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))
- **P2RX7**: [EXTERNAL] [DATA] P2RX7 contributes to regulation of sodium ion transport through ATP-gated cation fluxes that adjust cellular Na+ levels [PMID:17785580](https://pubmed.ncbi.nlm.nih.gov/17785580/). ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))

#### Statistical Context

[DATA] Regulation of sodium ion transport ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028)) is enriched at FDR 3.41e-02 with 9.4-fold overrepresentation across 5 genes, spanning channel modulation and pump regulation. [DATA] Multiple curated mechanisms link to excitability and homeostatic control.

---

### Theme 28: axon initial segment

**Summary:** axon initial segment ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] The axon initial segment concentrates voltage-gated sodium channels and adhesion scaffolds to initiate action potentials and maintain neuronal polarity. [INFERENCE] SCN1A-rich channel clusters at the AIS set spike threshold and reliability, while ankyrin–adhesion networks anchor channels and segregate axonal identity. [INFERENCE] NRCAM contributes to AIS organization and axon guidance interfaces, linking membrane adhesion with excitability localization.

#### Key Insights

- [GO-HIERARCHY] High-density Nav channel clustering at the AIS establishes a privileged site for spike initiation and polarity maintenance. ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))
- [GO-HIERARCHY] Adhesion scaffolds at the AIS stabilize channel nanoclusters and segregate axonal from somatodendritic membranes. ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))

#### Key Genes

- **SCN1A**: [INFERENCE] [INFERENCE] SCN1A provides AIS-localized Na+ currents essential for spike initiation and reliable axonal propagation. ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))
- **NRCAM**: [INFERENCE] [INFERENCE] NRCAM helps organize AIS adhesion and cytoskeletal anchoring to maintain channel clustering and axonal identity. ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))

#### Statistical Context

[DATA] Axon initial segment ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194)) is enriched at FDR 3.92e-02 with 14.7-fold overrepresentation across 3 genes, indicating strong AIS specialization within the set. [DATA] This compact enrichment highlights excitability and polarity hubs.

---

### Theme 29: sodium channel complex

**Summary:** sodium channel complex ([GO:0034706](http://purl.obolibrary.org/obo/GO_0034706))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] The sodium channel complex comprises pore-forming Nav α subunits and auxiliary β subunits that mediate rapid depolarizing Na+ currents. [DATA] SCN3A forms the Nav1.3 sodium channel complex with defined structures that inform drug and antagonist modulation, central to developmental excitability and pain pathways [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). [INFERENCE] SCN1A-containing complexes contribute to mature neuronal firing and network stability, complementing Nav1.3 roles across development.

#### Key Insights

- [DATA] Structural definition of Nav1.3 complexes reveals drug-binding sites and gating determinants critical for excitability control [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). ([GO:0034706](http://purl.obolibrary.org/obo/GO_0034706))
- [GO-HIERARCHY] Co-enrichment of multiple Nav subunits indicates coordinated assembly of sodium channel complexes in excitable cells. ([GO:0034706](http://purl.obolibrary.org/obo/GO_0034706))

#### Key Genes

- **SCN3A**: [EXTERNAL] [DATA] SCN3A assembles the Nav1.3 sodium channel complex essential for action potential initiation with defined drug-binding architecture [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). ([GO:0034706](http://purl.obolibrary.org/obo/GO_0034706))
- **SCN1A**: [INFERENCE] [INFERENCE] SCN1A contributes to sodium channel complexes that set spike threshold and firing fidelity in mature neurons. ([GO:0034706](http://purl.obolibrary.org/obo/GO_0034706))

#### Statistical Context

[DATA] Sodium channel complex ([GO:0034706](http://purl.obolibrary.org/obo/GO_0034706)) is enriched at FDR 3.92e-02 with 14.7-fold overrepresentation across 3 genes, highlighting concentrated Nav assemblies. [DATA] Structural evidence for SCN3A anchors complex-level interpretation.

---

### Theme 30: sodium channel activity

**Summary:** sodium channel activity ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272))  · Anchor confidence: **FDR<0.05**

[GO-HIERARCHY] Sodium channel activity encompasses ligand- and voltage-gated Na+ permeation that drives depolarization, spike initiation, and non-neuronal signaling. [DATA] SCN1A and SCN3A mediate voltage-gated sodium channel activity essential for action potentials, with disease-associated variants altering gating and excitability [PMID:14672992](https://pubmed.ncbi.nlm.nih.gov/14672992/); [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). [DATA] P2RX7 conducts Na+ in ATP-gated channels, and kainate-selective GRIK2 subunits contribute Na+ currents upon glutamate binding, adding transmitter-gated Na+ entry routes [PMID:17483156](https://pubmed.ncbi.nlm.nih.gov/17483156/); [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/). [GO-HIERARCHY] The functional enrichment bridges voltage-gated and transmitter-gated Na+ pathways that converge on membrane potential control.

#### Key Insights

- [DATA] Voltage-gated sodium channels SCN1A/SCN3A are core depolarizing effectors whose gating defects underlie excitability disorders [PMID:14672992](https://pubmed.ncbi.nlm.nih.gov/14672992/); [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272))
- [DATA] Transmitter-gated channels including P2RX7 and GRIK2 provide ligand-driven Na+ influx that modulates excitability and signaling [PMID:17483156](https://pubmed.ncbi.nlm.nih.gov/17483156/); [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/). ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272))

#### Key Genes

- **ASIC4**: [INFERENCE] [INFERENCE] ASIC4 contributes proton-gated Na+ conductance to adjust excitability in acidified microenvironments such as inflammation or ischemia. ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272))
- **SCN3A**: [EXTERNAL] [DATA] SCN3A encodes Nav1.3 voltage-gated sodium channel activity central to depolarization and spike initiation [PMID:35277491](https://pubmed.ncbi.nlm.nih.gov/35277491/). ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272))
- **SCN1A**: [EXTERNAL] [DATA] SCN1A provides Nav1.1 channel activity with pathogenic variants perturbing gating and neuronal excitability [PMID:14672992](https://pubmed.ncbi.nlm.nih.gov/14672992/). ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272))
- **P2RX7**: [EXTERNAL] [DATA] P2RX7 forms ATP-gated cation channels with Na+ permeation that modulates membrane potential and downstream signaling [PMID:17483156](https://pubmed.ncbi.nlm.nih.gov/17483156/). ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272))
- **GRIK2**: [EXTERNAL] [DATA] GRIK2 confers kainate-selective glutamate receptor activity permitting Na+ influx that contributes to synaptic depolarization [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/). ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272))

#### Statistical Context

[DATA] Sodium channel activity ([GO:0005272](http://purl.obolibrary.org/obo/GO_0005272)) is enriched at FDR 3.99e-02 with 11.1-fold overrepresentation across 5 genes, spanning voltage- and transmitter-gated Na+ entry routes. [DATA] The combined presence of Nav and ligand-gated channels explains broad excitability control in the set.

---

## Hub Genes

- **GRIK2**: [EXTERNAL] [DATA] GRIK2 is annotated to modulation of chemical synaptic transmission and positive regulation of synaptic transmission, and provides kainate-selective glutamate receptor activity that conducts Na+ and Ca2+ to modulate pre- and postsynaptic signaling [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/). [EXTERNAL] Structural and pharmacologic studies establish GRIK2 as a core kainate receptor subunit coordinating excitatory synaptic diversity and plasticity [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/); [PMID:21893069](https://pubmed.ncbi.nlm.nih.gov/21893069/). [INFERENCE] By shaping presynaptic facilitation and postsynaptic depolarization across multiple synapse-related themes, GRIK2 acts as a cross-theme driver of excitability and plasticity.
- **GRID2**: [EXTERNAL] [DATA] GRID2 promotes excitatory synapse assembly and positive regulation of synapse assembly and localizes to the postsynaptic density membrane, integrating organizer complexes with ion channel gating [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/); [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). [EXTERNAL] mGlu1-triggered gating of GRID2 provides a metabotropic-to-ionotropic coupling mechanism that tunes postsynaptic potentials across dendritic and synaptic themes [PMID:24357660](https://pubmed.ncbi.nlm.nih.gov/24357660/). [INFERENCE] Through stabilizing synaptic architecture and controlling postsynaptic excitability, GRID2 coordinates junction organization and transmission modulation.
- **NRCAM**: [EXTERNAL] [DATA] NRCAM is annotated to regulation of axon extension and the external side of the plasma membrane, supporting adhesion-guided axon growth and pathway stabilization [PMID:8812479](https://pubmed.ncbi.nlm.nih.gov/8812479/). [INFERENCE] Its repeated presence across axon, neuron projection development, and junction organization themes reflects a unifying role in linking membrane adhesion to circuit wiring.
- **GRIA2**: [EXTERNAL] [DATA] GRIA2 participates in ionotropic glutamate receptor signaling, AMPA receptor activity, dendritic spine biology, and excitatory synapses, defining fast EPSC generation and plasticity [PMID:20614889](https://pubmed.ncbi.nlm.nih.gov/20614889/); [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/); [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). [EXTERNAL] Aβ-driven AMPAR endocytosis targeting GRIA2-positive spines disrupts synaptic transmission, connecting disease perturbations across PSD and dendritic themes [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/). [INFERENCE] By setting ion selectivity and trafficking, GRIA2 coordinates multiple synaptic component and process themes.
- **EPHB1**: [INFERENCE] [INFERENCE] EPHB1 transduces ephrin guidance to shape axon and dendrite morphology and align excitatory synapses, bridging neuron projection development with synapse organization across themes. [INFERENCE] Its bidirectional signaling integrates cell–cell contact with cytoskeletal remodeling to coordinate circuit assembly.
- **DSCAM**: [EXTERNAL] [EXTERNAL] DSCAM promotes axon extension and collaborates with DCC in netrin-1 responses to guide commissural trajectories, linking projection development with axon guidance themes [PMID:18585357](https://pubmed.ncbi.nlm.nih.gov/18585357/). [INFERENCE] Its adhesion and receptor functions also influence dendritic patterning and somatodendritic organization, connecting multiple neuronal compartment themes.
- **DISC1**: [EXTERNAL] [DATA] DISC1 localizes to glutamatergic and GABA-ergic synapses, indicating a scaffolding role that bridges excitatory–inhibitory balance across synaptic themes [PMID:16736468](https://pubmed.ncbi.nlm.nih.gov/16736468/). [INFERENCE] DISC1’s interactions with cytoskeletal and adhesion regulators tie neuron projection development to synapse formation and junction organization.
- **GRIA3**: [EXTERNAL] [EXTERNAL] GRIA3 provides AMPA receptor activity and contributes to fast depolarization and plasticity at excitatory synapses, coordinating signaling across dendritic spine and membrane potential themes [PMID:21172611](https://pubmed.ncbi.nlm.nih.gov/21172611/). [INFERENCE] By tuning AMPAR kinetics, GRIA3 participates in transmitter-gated channel and ionotropic signaling pathways across multiple compartments.
- **GRIA4**: [EXTERNAL] [EXTERNAL] GRIA4 encodes an AMPAR subunit with defined gating control by TARPs and cornichon proteins, supporting transmitter-gated channel activity and synaptic plasticity across excitatory synapse and PSD themes [PMID:21172611](https://pubmed.ncbi.nlm.nih.gov/21172611/). [INFERENCE] Its co-assembly with GRIA2/3 diversifies AMPAR signaling across dendritic and membrane potential themes.
- **OPHN1**: [EXTERNAL] [DATA] OPHN1 regulates neuron projection development and glutamatergic synapse function via inhibition of hyperactive Rho-ROCK signaling, aligning cytoskeletal control with synaptic plasticity [PMID:27160703](https://pubmed.ncbi.nlm.nih.gov/27160703/); [PMID:24966368](https://pubmed.ncbi.nlm.nih.gov/24966368/). [INFERENCE] This coupling enables coherent effects across projection development, dendritic spine organization, and synaptic transmission themes.
- **SLC1A1**: [EXTERNAL] [EXTERNAL] SLC1A1 maintains glutamate homeostasis in neuronal cell bodies and dendrites, preventing excitotoxicity and stabilizing synaptic signaling across dendrite and soma themes [PMID:9409715](https://pubmed.ncbi.nlm.nih.gov/9409715/). [INFERENCE] By shaping extracellular glutamate, it indirectly modulates synaptic transmission and membrane potential regulation themes.
- **MAP2**: [EXTERNAL] [EXTERNAL] MAP2 stabilizes dendritic microtubules to drive arborization and supports neuron projection development, linking cytoskeletal architecture to synaptic organization across dendrite-related themes [PMID:20846339](https://pubmed.ncbi.nlm.nih.gov/20846339/). [EXTERNAL] MAP2-associated PSD scaffolding influences receptor positioning and plasticity, coordinating dendritic spine and PSD membrane themes [PMID:26609151](https://pubmed.ncbi.nlm.nih.gov/26609151/).
- **IL1RAPL1**: [EXTERNAL] [DATA] IL1RAPL1 regulates presynaptic assembly and postsynaptic organization at excitatory synapses, increasing active presynaptic compartments and mEPSC frequency [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). [INFERENCE] This organizer bridges cell junction organization with glutamatergic synapse function across multiple themes.
- **ALCAM**: [EXTERNAL] [EXTERNAL] ALCAM mediates heterophilic adhesion with CD6 to stabilize intercellular contacts, intersecting axon, dendrite, and junction organization themes through adhesion control [PMID:16352806](https://pubmed.ncbi.nlm.nih.gov/16352806/). [INFERENCE] Its neuronal expression supports projection development and compartment organization across cellular component themes.
- **FYN**: [EXTERNAL] [EXTERNAL] Fyn kinase is activated at dendritic PSDs downstream of PrPC–Aβo–mGlu5 and disrupts synapses, implicating FYN as a dendritic signaling hub across PSD and dendritic themes [PMID:24012003](https://pubmed.ncbi.nlm.nih.gov/24012003/). [INFERENCE] FYN also phosphorylates cytoskeletal and receptor targets to coordinate synapse formation and membrane potential regulation.
- **SCN1A**: [EXTERNAL] [EXTERNAL] SCN1A encodes Nav1.1 critical for action potential initiation and propagation, coordinating axon initial segment, membrane potential regulation, and sodium channel activity themes [PMID:27207958](https://pubmed.ncbi.nlm.nih.gov/27207958/). [INFERENCE] Its distribution across axonal and somatic compartments integrates excitability with synaptic output control.
- **ERBB4**: [INFERENCE] [INFERENCE] ERBB4 signaling shapes nervous system development and synapse formation, coordinating interneuron maturation across GABA-ergic synapse and junction organization themes. [INFERENCE] Postsynaptic roles at excitatory synapses extend its influence to PSD membrane organization.
- **P2RX7**: [EXTERNAL] [EXTERNAL] P2RX7 mediates ATP-gated Na+/Ca2+ influx and drives phospholipid scrambling, linking ion flux, membrane remodeling, and inflammatory signaling across membrane potential and scrambling themes [PMID:17785580](https://pubmed.ncbi.nlm.nih.gov/17785580/); [PMID:25651887](https://pubmed.ncbi.nlm.nih.gov/25651887/). [INFERENCE] Its presence in soma and membrane themes highlights cross-compartment signaling roles.
- **CDH13**: [EXTERNAL] [DATA] CDH13 enhances cell–matrix adhesion by elevating β1 integrin on the surface and promotes angiogenic morphogenesis, integrating adhesion with morphogenesis themes [PMID:17573778](https://pubmed.ncbi.nlm.nih.gov/17573778/); [PMID:16873731](https://pubmed.ncbi.nlm.nih.gov/16873731/). [INFERENCE] Junctional and synaptic impacts position CDH13 as a coordinator of cell–cell and cell–matrix interfaces.
- **ZNF804A**: [EXTERNAL] [DATA] ZNF804A localizes to neuronal soma and dendrites and regulates neurite formation and dendritic spines, connecting neuron projection development with dendritic spine and soma themes [PMID:27837918](https://pubmed.ncbi.nlm.nih.gov/27837918/); [PMID:4438586](https://pubmed.ncbi.nlm.nih.gov/4438586/). [INFERENCE] Its dual nuclear and synaptic presence coordinates transcriptional and structural programs across development and synaptic function.

## Overall Summary

[DATA] The 200-gene human input yields 154 enriched GO terms with 46 leaves and 31 high-level themes distilled here, with 167 genes annotated and multiple terms surpassing FDR<0.01 indicating robust signal concentration across neuronal systems.

[GO-HIERARCHY] Dominant cellular component themes span axon, dendrite, postsynaptic density membrane, excitatory and GABA-ergic synapses, and axon initial segment, while process and function themes include neuron projection development, axon guidance, synapse assembly, ionotropic glutamate signaling, and regulation of membrane potential.

[EXTERNAL] Mechanistic anchors include GRIA2-driven AMPAR signaling and plasticity, GRIK2-mediated kainate receptor modulation of release, GRID2 organizer functions at excitatory synapses, and SCN1A-dependent action potential initiation linking compartmental structure to excitability [PMID:20032460](https://pubmed.ncbi.nlm.nih.gov/20032460/); [PMID:15537878](https://pubmed.ncbi.nlm.nih.gov/15537878/); [PMID:27418511](https://pubmed.ncbi.nlm.nih.gov/27418511/); [PMID:27207958](https://pubmed.ncbi.nlm.nih.gov/27207958/).

[INFERENCE] Cross-theme hub genes such as GRIK2, GRID2, GRIA2/3/4, NRCAM, IL1RAPL1, OPHN1, and ZNF804A coordinate adhesion, cytoskeletal remodeling, receptor gating, and transcriptional control to integrate wiring with synaptic function.

[DATA] The statistical context across themes shows fold enrichments up to ~21-fold with FDR values frequently below 0.01, supporting coherent biological narratives that jointly explain developmental wiring and mature synaptic signaling in the dataset.

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

