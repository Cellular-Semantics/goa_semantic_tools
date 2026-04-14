# GO Enrichment Analysis Report — human

> **Methods note:** Enrichment themes are built using MRCEA-B (Most Recent Common Enriched Ancestor, all-paths BFS). Each theme is headed by an **anchor** — an enriched GO term selected by maximising information content (IC) × uncovered leaves, chosen bottom-up from all enrichment leaves simultaneously via a greedy algorithm. Anchor confidence (high/medium/low) reflects how tightly the leaf terms cluster under the anchor.

## Theme Index

Full gene listings: [Cluster_9_themes.csv](Cluster_9_themes.csv)

| # | Theme | NS | FDR | Genes | Confidence |
|---|-------|----|-----|-------|------------|
| [1](#theme-1-monoatomic-ion-channel-complex) | [monoatomic ion channel complex](#theme-1-monoatomic-ion-channel-complex) [GO:0034702](http://purl.obolibrary.org/obo/GO_0034702) | CC | 1.25e-13 | 26 | FDR<0.01 |
| [2](#theme-2-glutamatergic-synapse) | [glutamatergic synapse](#theme-2-glutamatergic-synapse) [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978) | CC | 1.86e-12 | 30 | FDR<0.01 |
| [3](#theme-3-regulation-of-membrane-potential) | [regulation of membrane potential](#theme-3-regulation-of-membrane-potential) [GO:0042391](http://purl.obolibrary.org/obo/GO_0042391) | BP | 5.28e-12 | 27 | FDR<0.01 |
| [4](#theme-4-synapse-organization) | [synapse organization](#theme-4-synapse-organization) [GO:0050808](http://purl.obolibrary.org/obo/GO_0050808) | BP | 5.28e-12 | 28 | FDR<0.01 |
| [5](#theme-5-axon) | [axon](#theme-5-axon) [GO:0030424](http://purl.obolibrary.org/obo/GO_0030424) | CC | 2.77e-11 | 25 | FDR<0.01 |
| [6](#theme-6-gaba-ergic-synapse) | [GABA-ergic synapse](#theme-6-gaba-ergic-synapse) [GO:0098982](http://purl.obolibrary.org/obo/GO_0098982) | CC | 4.38e-09 | 13 | FDR<0.01 |
| [7](#theme-7-anterograde-trans-synaptic-signaling) | [anterograde trans-synaptic signaling](#theme-7-anterograde-trans-synaptic-signaling) [GO:0098916](http://purl.obolibrary.org/obo/GO_0098916) | BP | 3.31e-08 | 28 | FDR<0.01 |
| [8](#theme-8-postsynapse) | [postsynapse](#theme-8-postsynapse) [GO:0098794](http://purl.obolibrary.org/obo/GO_0098794) | CC | 1.71e-06 | 28 | FDR<0.01 |
| [9](#theme-9-monoatomic-ion-channel-activity) | [monoatomic ion channel activity](#theme-9-monoatomic-ion-channel-activity) [GO:0005216](http://purl.obolibrary.org/obo/GO_0005216) | MF | 1.34e-05 | 20 | FDR<0.01 |
| [10](#theme-10-brain-development) | [brain development](#theme-10-brain-development) [GO:0007420](http://purl.obolibrary.org/obo/GO_0007420) | BP | 6.31e-05 | 12 | FDR<0.01 |
| [11](#theme-11-neuron-projection-membrane) | [neuron projection membrane](#theme-11-neuron-projection-membrane) [GO:0032589](http://purl.obolibrary.org/obo/GO_0032589) | CC | 1.10e-04 | 7 | FDR<0.01 |
| [12](#theme-12-structural-constituent-of-presynaptic-active-zone) | [structural constituent of presynaptic active zone](#theme-12-structural-constituent-of-presynaptic-active-zone) [GO:0098882](http://purl.obolibrary.org/obo/GO_0098882) | MF | 1.17e-04 | 4 | FDR<0.01 |
| [13](#theme-13-transmembrane-transporter-binding) | [transmembrane transporter binding](#theme-13-transmembrane-transporter-binding) [GO:0044325](http://purl.obolibrary.org/obo/GO_0044325) | MF | 3.28e-04 | 10 | FDR<0.01 |
| [14](#theme-14-regulation-of-monoatomic-ion-transport) | [regulation of monoatomic ion transport](#theme-14-regulation-of-monoatomic-ion-transport) [GO:0043269](http://purl.obolibrary.org/obo/GO_0043269) | BP | 3.72e-04 | 15 | FDR<0.01 |
| [15](#theme-15-presynapse) | [presynapse](#theme-15-presynapse) [GO:0098793](http://purl.obolibrary.org/obo/GO_0098793) | CC | 4.02e-04 | 30 | FDR<0.01 |
| [16](#theme-16-cell-surface) | [cell surface](#theme-16-cell-surface) [GO:0009986](http://purl.obolibrary.org/obo/GO_0009986) | CC | 9.98e-04 | 19 | FDR<0.01 |
| [17](#theme-17-node-of-ranvier) | [node of Ranvier](#theme-17-node-of-ranvier) [GO:0033268](http://purl.obolibrary.org/obo/GO_0033268) | CC | 1.42e-03 | 4 | FDR<0.01 |
| [18](#theme-18-ionotropic-glutamate-receptor-signaling-pathway) | [ionotropic glutamate receptor signaling pathway](#theme-18-ionotropic-glutamate-receptor-signaling-pathway) [GO:0035235](http://purl.obolibrary.org/obo/GO_0035235) | BP | 1.72e-03 | 5 | FDR<0.01 |
| [19](#theme-19-schaffer-collateral---ca1-synapse) | [Schaffer collateral - CA1 synapse](#theme-19-schaffer-collateral---ca1-synapse) [GO:0098685](http://purl.obolibrary.org/obo/GO_0098685) | CC | 1.75e-03 | 7 | FDR<0.01 |
| [20](#theme-20-dendritic-shaft) | [dendritic shaft](#theme-20-dendritic-shaft) [GO:0043198](http://purl.obolibrary.org/obo/GO_0043198) | CC | 1.78e-03 | 5 | FDR<0.01 |
| [21](#theme-21-excitatory-synapse) | [excitatory synapse](#theme-21-excitatory-synapse) [GO:0060076](http://purl.obolibrary.org/obo/GO_0060076) | CC | 2.11e-03 | 6 | FDR<0.01 |
| [22](#theme-22-associative-learning) | [associative learning](#theme-22-associative-learning) [GO:0008306](http://purl.obolibrary.org/obo/GO_0008306) | BP | 2.22e-03 | 6 | FDR<0.01 |
| [23](#theme-23-neuron-development) | [neuron development](#theme-23-neuron-development) [GO:0048666](http://purl.obolibrary.org/obo/GO_0048666) | BP | 2.27e-03 | 21 | FDR<0.01 |
| [24](#theme-24-axon-initial-segment) | [axon initial segment](#theme-24-axon-initial-segment) [GO:0043194](http://purl.obolibrary.org/obo/GO_0043194) | CC | 2.64e-03 | 4 | FDR<0.01 |
| [25](#theme-25-immune-response) | [immune response](#theme-25-immune-response) [GO:0006955](http://purl.obolibrary.org/obo/GO_0006955) | BP | 2.99e-03 | 1 | FDR<0.01 |
| [26](#theme-26-erbb4-erbb4-signaling-pathway) | [ERBB4-ERBB4 signaling pathway](#theme-26-erbb4-erbb4-signaling-pathway) [GO:0038138](http://purl.obolibrary.org/obo/GO_0038138) | BP | 2.99e-03 | 3 | FDR<0.01 |
| [27](#theme-27-neuron-to-neuron-synapse) | [neuron to neuron synapse](#theme-27-neuron-to-neuron-synapse) [GO:0098984](http://purl.obolibrary.org/obo/GO_0098984) | CC | 3.79e-03 | 6 | FDR<0.01 |
| [28](#theme-28-nucleic-acid-metabolic-process) | [nucleic acid metabolic process](#theme-28-nucleic-acid-metabolic-process) [GO:0090304](http://purl.obolibrary.org/obo/GO_0090304) | BP | 3.90e-03 | 15 | FDR<0.01 |
| [29](#theme-29-juxtaparanode-region-of-axon) | [juxtaparanode region of axon](#theme-29-juxtaparanode-region-of-axon) [GO:0044224](http://purl.obolibrary.org/obo/GO_0044224) | CC | 5.94e-03 | 3 | FDR<0.01 |
| [30](#theme-30-sodium-channel-regulator-activity) | [sodium channel regulator activity](#theme-30-sodium-channel-regulator-activity) [GO:0017080](http://purl.obolibrary.org/obo/GO_0017080) | MF | 6.23e-03 | 5 | FDR<0.01 |

---

### Theme 1: monoatomic ion channel complex

**Summary:** monoatomic ion channel complex ([GO:0034702](http://purl.obolibrary.org/obo/GO_0034702))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] This theme centers on assemblies of pore-forming and auxiliary subunits that create selective pathways for ions, with nested enrichment for voltage-gated potassium channels, NMDA receptor complexes, and sodium channel complexes indicating mechanistic subdivision by ion selectivity and gating mode within [GO:0034702](http://purl.obolibrary.org/obo/GO_0034702), [GO:0008076](http://purl.obolibrary.org/obo/GO_0008076), [GO:0017146](http://purl.obolibrary.org/obo/GO_0017146), and [GO:0034706](http://purl.obolibrary.org/obo/GO_0034706) respectively.[DATA] The study captures coordinated overrepresentation of channel complexes from multiple ion classes, consistent with the 7.7-fold enrichment and very low FDR that reflect broad channelome engagement in the input gene set.[EXTERNAL] Biochemical studies demonstrate NMDA receptor complexes contain multiple NR2 with NR1, supporting a pentameric-like assembly logic that explains how glutamatergic inputs couple to Ca2+ entry and downstream plasticity within these complexes [PMID:10480938](https://pubmed.ncbi.nlm.nih.gov/10480938/).[DATA] Curated annotations further link GRIN1/2 subunits to the NMDA selective glutamate receptor complex, reinforcing the structural specificity captured by the NMDA complex subterm [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/), [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/), [PMID:26919761](https://pubmed.ncbi.nlm.nih.gov/26919761/).

#### Key Insights

- [EXTERNAL] NMDA receptor assemblies integrate NR1 and NR2 subunits into Ca2+-permeable complexes, mechanistically explaining synaptic coincidence detection captured by NMDA selective glutamate receptor complex enrichment. ([GO:0017146](http://purl.obolibrary.org/obo/GO_0017146))
- [INFERENCE] Voltage-gated potassium channel complexes shape action potential repolarization and interspike intervals, providing the biophysical counterbalance to excitatory receptor-driven depolarization within this theme. ([GO:0008076](http://purl.obolibrary.org/obo/GO_0008076))
- [INFERENCE] Enrichment of sodium channel complexes indicates recruitment of fast depolarizing conductances that initiate and propagate spikes, coupling receptor input to axonal output. ([GO:0034706](http://purl.obolibrary.org/obo/GO_0034706))

#### Key Genes

- **KCNMB2**: [INFERENCE] [INFERENCE] The BK channel beta subunit tunes voltage and Ca2+ sensitivity of the pore-forming KCNMA1 to accelerate repolarization and curb excitability within voltage-gated potassium channel complexes. ([GO:0008076](http://purl.obolibrary.org/obo/GO_0008076))
- **KCNMA1**: [INFERENCE] [INFERENCE] The BK pore-forming subunit provides large-conductance Ca2+-activated K+ efflux that rapidly terminates bursts and limits Ca2+ loading in postsynaptic membranes. ([GO:0008076](http://purl.obolibrary.org/obo/GO_0008076))
- **KCNB2**: [INFERENCE] [INFERENCE] A delayed-rectifier Kv2 family channel that stabilizes membrane potential after synaptic activation, indirectly constraining NMDA-dependent Ca2+ entry by hastening repolarization. ([GO:0008076](http://purl.obolibrary.org/obo/GO_0008076))
- **DPP10**: [INFERENCE] [INFERENCE] An auxiliary subunit for Kv4 channels that accelerates gating and promotes surface expression, thereby shaping dendritic A-type currents that temper synaptic depolarization. ([GO:0008076](http://purl.obolibrary.org/obo/GO_0008076))
- **SCN2A**: [INFERENCE] [INFERENCE] The Nav1.2 alpha subunit forms sodium channel complexes that drive rapid membrane depolarization and spike initiation in developing axon initial segments. ([GO:0034706](http://purl.obolibrary.org/obo/GO_0034706))

#### Statistical Context

[DATA] 26 genes map to monoatomic ion channel complexes with 7.7-fold enrichment at FDR 1.25e-13 indicating strong selection of channel assemblies in the input list.[GO-HIERARCHY] Significant subterms for potassium channel complexes, NMDA complexes, and sodium channel complexes show layered organization of excitatory and repolarizing conductances within the broader channel complex class.

---

### Theme 2: glutamatergic synapse

**Summary:** glutamatergic synapse ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Enrichment at the glutamatergic synapse cellular component reflects coordinated recruitment of presynaptic release machinery, postsynaptic receptors, and adhesion scaffolds required for fast excitatory transmission within [GO:0098978](http://purl.obolibrary.org/obo/GO_0098978).[EXTERNAL] IL1 family synaptic receptors and partners orchestrate excitatory synapse assembly by linking extracellular adhesion to PSD-95 recruitment, stabilizing AMPA/NMDA receptor nanodomains that tune synaptic gain [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/).[EXTERNAL] Neuregulin–ErbB signaling can depotentiate potentiated CA1 synapses, indicating pathway-specific control of plasticity state at glutamatergic contacts that aligns with this structural synapse enrichment [PMID:16221846](https://pubmed.ncbi.nlm.nih.gov/16221846/).

#### Key Insights

- [EXTERNAL] IL1RAPL family signaling promotes PSD-95 recruitment and excitatory synapse formation, mechanistically linking adhesion to postsynaptic receptor clustering at glutamatergic synapses. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- [EXTERNAL] Neuregulin inputs via ErbB receptors reverse LTP at CA1, showing that trophic signaling pathways dynamically remodel glutamatergic synaptic strength on the enriched structure. ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Key Genes

- **IL1RAPL2**: [EXTERNAL] [DATA] An IL1 receptor family member localized to excitatory synapses that couples to PSD-95 complexes to promote synapse formation and receptor stabilization [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **NSG2**: [EXTERNAL] [DATA] Regulates AMPA receptor localization and stabilization at excitatory postsynapses, supporting synaptic strength and plasticity [PMID:29114105](https://pubmed.ncbi.nlm.nih.gov/29114105/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **SH3GL3**: [EXTERNAL] [EXTERNAL] Endophilin family adaptor that organizes receptor-scaffold complexes to cluster AMPA/NMDA receptors and fine-tune excitatory signaling [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))
- **ANKS1B**: [EXTERNAL] [EXTERNAL] A PSD scaffold interactor that modulates PSD-95 assemblies to stabilize excitatory synapses and shape plasticity states at glutamatergic contacts [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0098978](http://purl.obolibrary.org/obo/GO_0098978))

#### Statistical Context

[DATA] 30 genes at the glutamatergic synapse show 5.7-fold enrichment with FDR 1.86e-12, indicating dense representation of excitatory synaptic structural modules.[GO-HIERARCHY] This cellular component subsumes pre- and postsynaptic subdomains whose coordinated enrichment is reflected by co-occurrence of presynaptic release and postsynaptic receptor genes.

---

### Theme 3: regulation of membrane potential

**Summary:** regulation of membrane potential ([GO:0042391](http://purl.obolibrary.org/obo/GO_0042391))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 5.28e-12 · **Genes (27)**: ANK3, CACNA1C, CACNA1D, FGF13, GABRA2, GABRB1, GABRG2, GRIA1, GRIK4, GRIN1, GRIN2A, GRIN2B, GRM5, KCNB2, KCNC2 … (+12 more)

---

### Theme 4: synapse organization

**Summary:** synapse organization ([GO:0050808](http://purl.obolibrary.org/obo/GO_0050808))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Synapse organization assembles presynaptic active zone scaffolds, trans-synaptic adhesion systems, and postsynaptic density regulators that build and maintain synaptic structure within [GO:0050808](http://purl.obolibrary.org/obo/GO_0050808) and its subterms.[EXTERNAL] GABAA receptor gamma2 is sufficient to initiate inhibitory synapse assembly, indicating receptors can drive postsynaptic scaffold formation that then aligns presynaptic release sites [PMID:23909897](https://pubmed.ncbi.nlm.nih.gov/23909897/), [PMID:25489750](https://pubmed.ncbi.nlm.nih.gov/25489750/).[EXTERNAL] Liprin-alpha and TANC2 recruit dense core vesicles to postsynaptic sites via PPFIA2, linking cargo capture and spine morphogenesis to the organizational program [PMID:30021165](https://pubmed.ncbi.nlm.nih.gov/30021165/).

#### Key Insights

- [EXTERNAL] Presynaptic active zone maintenance depends on RIM, ELKS/ERC, and Piccolo assemblies that align Ca2+ channels with docked vesicles to ensure precise release. ([GO:0048790](http://purl.obolibrary.org/obo/GO_0048790))
- [EXTERNAL] Inhibitory synapse assembly can be initiated by postsynaptic GABAA receptor subunits, demonstrating receptor-driven nucleation of synaptic specializations. ([GO:1904862](http://purl.obolibrary.org/obo/GO_1904862))
- [EXTERNAL] Postsynapse organization is tuned by mGluR5 and NMDA receptor-associated scaffolds that remodel spine shape and receptor content during plasticity. ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))

#### Key Genes

- **PTPRD**: [EXTERNAL] [DATA] A presynaptic phosphatase that promotes presynapse assembly and stabilizes trans-synaptic adhesion, organizing release machinery at excitatory contacts [PMID:21926414](https://pubmed.ncbi.nlm.nih.gov/21926414/). ([GO:0099172](http://purl.obolibrary.org/obo/GO_0099172))
- **PCLO**: [EXTERNAL] [EXTERNAL] Piccolo anchors and organizes active zone components and dense core vesicles to sustain neurotransmitter release and structural integrity of the presynaptic site [PMID:30021165](https://pubmed.ncbi.nlm.nih.gov/30021165/). ([GO:0048790](http://purl.obolibrary.org/obo/GO_0048790))
- **PPFIA2**: [EXTERNAL] [DATA] Liprin-α family member that recruits dense core vesicles to postsynaptic sites and regulates dendritic spine morphogenesis, coupling cargo capture to synapse structure [PMID:30021165](https://pubmed.ncbi.nlm.nih.gov/30021165/). ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- **CAMK2B**: [EXTERNAL] [EXTERNAL] CaMKIIβ phosphorylates synaptic targets to modulate receptor anchoring and spine remodeling, coordinating postsynapse organization with activity-dependent signals [PMID:23909897](https://pubmed.ncbi.nlm.nih.gov/23909897/), [PMID:30021165](https://pubmed.ncbi.nlm.nih.gov/30021165/). ([GO:0099175](http://purl.obolibrary.org/obo/GO_0099175))
- **RIMS1**: [EXTERNAL] [EXTERNAL] A core active zone scaffold that binds Ca2+ channels and synaptotagmin to prime vesicles and preserve active zone architecture [PMID:11438518](https://pubmed.ncbi.nlm.nih.gov/11438518/). ([GO:0048790](http://purl.obolibrary.org/obo/GO_0048790))

#### Statistical Context

[DATA] 22 genes are enriched 10.1-fold for synapse organization at FDR 5.28e-12, capturing both inhibitory and excitatory assembly programs.[GO-HIERARCHY] Child terms highlight presynaptic active zone maintenance, inhibitory synapse assembly, and postsynapse organizational control, indicating multi-compartment remodeling.

---

### Theme 5: axon

**Summary:** axon ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The axon component enrichment captures cytoskeletal scaffolds, ion channel clustering factors, and guidance molecules that establish polarized conduction domains within [GO:0030424](http://purl.obolibrary.org/obo/GO_0030424).[EXTERNAL] Caspr2 enrichment at juxtaparanodes organizes Shaker-type K+ channels, illustrating a cell-adhesion–driven mechanism for lateral membrane domain assembly critical for saltatory conduction [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/).[EXTERNAL] Developmental node of Ranvier formation depends on timely Nav clustering, aligning with the presence of axonal channel and scaffold genes in this component [PMID:16652168](https://pubmed.ncbi.nlm.nih.gov/16652168/).

#### Key Insights

- [EXTERNAL] Axolemmal adhesion molecules such as Caspr2 drive juxtaparanodal K+ channel clustering to reduce internodal excitability and protect spike fidelity. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- [EXTERNAL] Timed Nav accumulation at nodes underlies maturation of conduction velocity, linking axonal protein sorting to electrophysiological output. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))

#### Key Genes

- **NMNAT2**: [INFERENCE] [INFERENCE] An axonal NAD+ biosynthetic enzyme that sustains axon energy homeostasis and integrity, buffering conduction against metabolic stress. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **NCAM2**: [INFERENCE] [INFERENCE] A neural cell adhesion molecule that supports polarized distribution of juxtaparanodal complexes to stabilize K+ channel clusters along axons. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **DGKI**: [INFERENCE] [INFERENCE] Diacylglycerol kinase iota modulates lipid signaling that influences axonal growth and ion channel domain organization during myelination. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **DSCAML1**: [INFERENCE] [INFERENCE] An adhesion receptor guiding axon patterning and fasciculation to establish long-range connectivity and proper axonal targeting. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))
- **PTPRO**: [INFERENCE] [INFERENCE] A receptor phosphatase that modulates axonal guidance and synaptic contact refinement through dephosphorylation of adhesion-cytoskeletal effectors. ([GO:0030424](http://purl.obolibrary.org/obo/GO_0030424))

#### Statistical Context

[DATA] 25 genes localize to axons with 6.3-fold enrichment at FDR 2.77e-11, indicating strong representation of axonal organization machinery.[GO-HIERARCHY] Axonal enrichment coheres with separate node and juxtaparanode subdomain terms elsewhere in the analysis, reflecting compartmental specialization.

---

### Theme 6: GABA-ergic synapse

**Summary:** GABA-ergic synapse ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The GABA-ergic synapse component aggregates inhibitory receptor complexes, presynaptic GABA synthesis and release, and scaffolds that position chloride conductances at synapses within [GO:0098982](http://purl.obolibrary.org/obo/GO_0098982).[EXTERNAL] Postsynaptic GABAA receptors can nucleate inhibitory synapse formation, demonstrating receptor-driven assembly that aligns with the structural enrichment of these receptors and their scaffolds [PMID:23909897](https://pubmed.ncbi.nlm.nih.gov/23909897/).[EXTERNAL] High-resolution receptor structures reinforce how alpha, beta, and gamma subunits create fast Cl− conductances that hyperpolarize neurons and stabilize network rhythms [PMID:29950725](https://pubmed.ncbi.nlm.nih.gov/29950725/).

#### Key Insights

- [EXTERNAL] Postsynaptic GABAA receptor presence is sufficient to initiate inhibitory synapse assembly, coupling receptor insertion to presynaptic partner recruitment. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))
- [INFERENCE] Endocannabinoid CB1 signaling at inhibitory terminals modulates GABA release probability to dynamically regulate inhibitory tone on this structure. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))

#### Key Genes

- **GAD1**: [INFERENCE] [INFERENCE] The GABA-synthesizing enzyme that sets presynaptic transmitter supply and thereby determines inhibitory quantal content and tone. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))
- **CNR1**: [INFERENCE] [INFERENCE] CB1 receptors depress GABA release via Gi/o pathways, tuning inhibitory synaptic strength in an activity-dependent manner. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))
- **GABRB1**: [EXTERNAL] [DATA] A GABAA receptor beta subunit that forms the Cl− channel pore complex for fast inhibitory transmission at GABAergic synapses [PMID:29950725](https://pubmed.ncbi.nlm.nih.gov/29950725/). ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))
- **ERC2**: [INFERENCE] [INFERENCE] An ELKS family active zone scaffold that aligns Ca2+ channels with vesicles to support reliable GABA release. ([GO:0098982](http://purl.obolibrary.org/obo/GO_0098982))

#### Statistical Context

[DATA] 13 genes map to the GABA-ergic synapse with 12.3-fold enrichment at FDR 4.38e-09, indicating robust representation of inhibitory synaptic machinery.[GO-HIERARCHY] This structural component unifies presynaptic synthesis/release modules with postsynaptic receptor complexes to enforce inhibitory control of network excitability.

---

### Theme 7: anterograde trans-synaptic signaling

**Summary:** anterograde trans-synaptic signaling ([GO:0098916](http://purl.obolibrary.org/obo/GO_0098916))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Anterograde trans-synaptic signaling encompasses presynaptic release, cleft transmission, and postsynaptic receptor activation processes that convey information between neurons within [GO:0098916](http://purl.obolibrary.org/obo/GO_0098916).[EXTERNAL] NMDA receptor subunits and GRIA1 potentiate EPSPs and sustain LTP, linking receptor gating to strengthened postsynaptic responses captured by positive regulation of EPSP and LTP subterms [PMID:15003177](https://pubmed.ncbi.nlm.nih.gov/15003177/), [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/).[DATA] GABAA receptor subunits contribute to synaptic transmission GABAergic within this signaling framework, highlighting inhibitory modulation of forward synaptic flow [PMID:29950725](https://pubmed.ncbi.nlm.nih.gov/29950725/).

#### Key Insights

- [EXTERNAL] NMDA-dependent Ca2+ signaling increases excitatory postsynaptic potential amplitude to support LTP-centric information transfer across synapses. ([GO:2000463](http://purl.obolibrary.org/obo/GO_2000463))
- [DATA] GABAergic synaptic transmission operates in parallel to shape the net forward signal by imposing shunting and hyperpolarizing influences [PMID:29950725](https://pubmed.ncbi.nlm.nih.gov/29950725/). ([GO:0051932](http://purl.obolibrary.org/obo/GO_0051932))
- [INFERENCE] Presynaptic Ca2+ sensors and active zone organizers synchronize vesicle fusion timing to maximize information fidelity across the synaptic cleft. ([GO:0048168](http://purl.obolibrary.org/obo/GO_0048168))

#### Key Genes

- **GRIN2A**: [EXTERNAL] [DATA] An NMDA receptor subunit that enhances glutamatergic transmission and plasticity through Ca2+-dependent signaling and EPSP amplification [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/), [PMID:15003177](https://pubmed.ncbi.nlm.nih.gov/15003177/). ([GO:0051966](http://purl.obolibrary.org/obo/GO_0051966))
- **GRIN2B**: [EXTERNAL] [DATA] Drives LTP and synaptic plasticity by tuning NMDA receptor kinetics and Ca2+ signaling that reinforce strengthened synaptic responses [PMID:15003177](https://pubmed.ncbi.nlm.nih.gov/15003177/), [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/). ([GO:0060291](http://purl.obolibrary.org/obo/GO_0060291))
- **GRIN1**: [EXTERNAL] [DATA] The obligatory NMDA subunit enabling excitatory chemical synaptic transmission and positive regulation of EPSPs through Ca2+-permeable receptor activation [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/), [PMID:36959261](https://pubmed.ncbi.nlm.nih.gov/36959261/). ([GO:0098976](http://purl.obolibrary.org/obo/GO_0098976))
- **GRIA1**: [INFERENCE] [INFERENCE] AMPA receptor GluA1 subunit boosts synaptic gain and cooperates with NMDA receptors to consolidate LTP expression at potentiated synapses. ([GO:0060291](http://purl.obolibrary.org/obo/GO_0060291))
- **CAMK2B**: [EXTERNAL] [EXTERNAL] CaMKIIβ phosphorylates synaptic substrates downstream of Ca2+ entry to stabilize potentiated states and augment anterograde signaling [PMID:15003177](https://pubmed.ncbi.nlm.nih.gov/15003177/). ([GO:0048168](http://purl.obolibrary.org/obo/GO_0048168))

#### Statistical Context

[DATA] 19 genes enrich anterograde trans-synaptic signaling 7.0-fold at FDR 3.31e-08 with significant child processes for plasticity and EPSP regulation.[GO-HIERARCHY] The process integrates glutamatergic and GABAergic transmission terms, reflecting excitatory-inhibitory co-regulation of synaptic information flow.

---

### Theme 8: postsynapse

**Summary:** postsynapse ([GO:0098794](http://purl.obolibrary.org/obo/GO_0098794))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The postsynapse component aggregates the PSD membrane, receptors, and spine apparatus that decode and integrate synaptic inputs within [GO:0098794](http://purl.obolibrary.org/obo/GO_0098794) and its spine and PSD-membrane subterms.[EXTERNAL] Activity-dependent exocytosis at dendritic spines inserts AMPA receptors, reorganizing the postsynaptic membrane to express potentiated states aligned with PSD specialization [PMID:20434989](https://pubmed.ncbi.nlm.nih.gov/20434989/).[EXTERNAL] Postsynaptic lipid signaling via PRG-1/PLPPR4 regulates E/I balance by restraining glutamate release and shaping PSD composition, coupling membrane lipids to postsynaptic function [PMID:26671989](https://pubmed.ncbi.nlm.nih.gov/26671989/).

#### Key Insights

- [EXTERNAL] Postsynaptic density membrane enrichment reflects receptor-scaffold nanodomains that control receptor gating, signaling, and plasticity at excitatory synapses. ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- [EXTERNAL] Dendritic spines provide compartmentalized Ca2+ and signaling microdomains, enabling input-specific modulation of synaptic strength and structure. ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))

#### Key Genes

- **GRIN1**: [EXTERNAL] [DATA] An essential NMDA receptor subunit embedded in the PSD membrane that transduces glutamatergic input into Ca2+-dependent postsynaptic signaling [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/). ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))
- **GRIN2A**: [EXTERNAL] [DATA] NMDA subunit that shapes spine Ca2+ signals and plasticity rules within dendritic spines at postsynaptic sites [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/). ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))
- **GRM5**: [INFERENCE] [INFERENCE] mGluR5 couples to G proteins and Ca2+ stores to remodel spine structure and modulate NMDA/AMPA receptor function within PSD microdomains. ([GO:0043197](http://purl.obolibrary.org/obo/GO_0043197))
- **PTPRO**: [EXTERNAL] [EXTERNAL] A receptor phosphatase influencing postsynaptic signaling efficacy by dephosphorylating PSD-associated substrates and coordinating vesicle capture at postsynaptic sites [PMID:30021165](https://pubmed.ncbi.nlm.nih.gov/30021165/). ([GO:0098839](http://purl.obolibrary.org/obo/GO_0098839))

#### Statistical Context

[DATA] 17 genes localize to postsynapses with 5.3-fold enrichment at FDR 1.71e-06, including strong enrichment of the postsynaptic density membrane and dendritic spines.[GO-HIERARCHY] These child components define membrane and actin-rich compartments that encode synaptic input histories.

---

### Theme 9: monoatomic ion channel activity

**Summary:** monoatomic ion channel activity ([GO:0005216](http://purl.obolibrary.org/obo/GO_0005216))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Monoatomic ion channel activity consolidates ligand- and voltage-gated permeation of Na+, K+, and Ca2+ ions, with subterms specifying transmitter-gated control of pre- and postsynaptic potentials and NMDA-specific activities within [GO:0005216](http://purl.obolibrary.org/obo/GO_0005216) and children.[EXTERNAL] NMDA receptor activity and glutamate-gated Ca2+ permeation are substantiated by genetic and structural studies that connect GRIN variants to gating transitions and Ca2+ flux underpinning synaptic plasticity [PMID:38538865](https://pubmed.ncbi.nlm.nih.gov/38538865/), [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/), [PMID:26919761](https://pubmed.ncbi.nlm.nih.gov/26919761/), [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/).[DATA] The term set includes sodium channel activity, capturing Nav-driven depolarization that collaborates with transmitter-gated conductances to shape spike initiation and synaptic integration.

#### Key Insights

- [EXTERNAL] NMDA glutamate receptor activity couples glutamate binding to M3 helix gate opening to permit Ca2+/Na+ influx driving synaptic plasticity. ([GO:0004972](http://purl.obolibrary.org/obo/GO_0004972))
- [EXTERNAL] Transmitter-gated ion channels on the postsynaptic membrane directly set synaptic potential trajectories by controlling fast Cl− or cation fluxes. ([GO:1904315](http://purl.obolibrary.org/obo/GO_1904315))
- [EXTERNAL] Presynaptic ligand-gated channels adjust terminal potential and Ca2+ entry, tuning vesicle fusion probability and short-term plasticity. ([GO:0099507](http://purl.obolibrary.org/obo/GO_0099507))

#### Key Genes

- **GRIN2B**: [EXTERNAL] [DATA] NMDA receptor GluN2B subunit confers distinct gating and deactivation kinetics that regulate Ca2+ entry and synaptic signaling [PMID:26919761](https://pubmed.ncbi.nlm.nih.gov/26919761/), [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/). ([GO:0004972](http://purl.obolibrary.org/obo/GO_0004972))
- **GRIN2A**: [EXTERNAL] [DATA] GluN2A-containing NMDA receptors exhibit PAM-sensitive gating that controls synaptic Ca2+ influx and timing of postsynaptic depolarization [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/), [PMID:26919761](https://pubmed.ncbi.nlm.nih.gov/26919761/). ([GO:0004972](http://purl.obolibrary.org/obo/GO_0004972))
- **GRIN1**: [EXTERNAL] [DATA] The obligatory NMDA subunit is required for glutamate-gated Ca2+ channel activity that underlies Hebbian plasticity [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/), [PMID:38538865](https://pubmed.ncbi.nlm.nih.gov/38538865/). ([GO:0022849](http://purl.obolibrary.org/obo/GO_0022849))
- **GRIK4**: [EXTERNAL] [EXTERNAL] A kainate receptor subunit mediating transmitter-gated cation influx that depolarizes postsynaptic membranes and shapes excitatory signaling [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/). ([GO:1904315](http://purl.obolibrary.org/obo/GO_1904315))
- **GABRB1**: [EXTERNAL] [EXTERNAL] A GABAA beta subunit forming ligand-gated Cl− channels that hyperpolarize postsynaptic neurons to control synaptic potentials [PMID:29950725](https://pubmed.ncbi.nlm.nih.gov/29950725/). ([GO:1904315](http://purl.obolibrary.org/obo/GO_1904315))

#### Statistical Context

[DATA] 20 genes are enriched 4.9-fold for monoatomic ion channel activity at FDR 1.34e-05, spanning transmitter-gated and voltage-gated conductances.[GO-HIERARCHY] Child terms resolve NMDA-specific gating, presynaptic ligand-gated control, and postsynaptic transmitter-gated influence on membrane potential.

---

### Theme 10: brain development

**Summary:** brain development ([GO:0007420](http://purl.obolibrary.org/obo/GO_0007420))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Brain development groups programs for neuronal differentiation, migration, axon guidance, and synaptic maturation within [GO:0007420](http://purl.obolibrary.org/obo/GO_0007420).[EXTERNAL] NMDA receptor subunits are annotated to brain development and regulate activity-dependent maturation of circuits, linking excitatory receptor signaling to developmental plasticity [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/).[EXTERNAL] DSCAML1 exhibits patterned developmental expression guiding axon trajectories, demonstrating adhesion-coded topography essential for circuit assembly [PMID:12051741](https://pubmed.ncbi.nlm.nih.gov/12051741/).

#### Key Insights

- [EXTERNAL] Activity-dependent NMDA receptor signaling steers synaptic and circuit maturation, aligning receptor function with developmental program enrichment. ([GO:0007420](http://purl.obolibrary.org/obo/GO_0007420))
- [EXTERNAL] Adhesion and guidance molecules like CNTNAP2 and ROBO2 pattern axonal growth and target selection to build functional brain networks. ([GO:0007420](http://purl.obolibrary.org/obo/GO_0007420))

#### Key Genes

- **DSCAML1**: [EXTERNAL] [DATA] Guides neuronal and axonal migration via patterned expression in the spinal cord, shaping connectivity during CNS development [PMID:12051741](https://pubmed.ncbi.nlm.nih.gov/12051741/). ([GO:0007420](http://purl.obolibrary.org/obo/GO_0007420))
- **ROBO2**: [EXTERNAL] [DATA] A slit receptor mediating chemorepulsive guidance to position developing axons and neurons appropriately in the forebrain [PMID:10197527](https://pubmed.ncbi.nlm.nih.gov/10197527/). ([GO:0007420](http://purl.obolibrary.org/obo/GO_0007420))
- **CNTNAP2**: [EXTERNAL] [DATA] Caspr2 organizes axonal domains during myelination, supporting rapid conduction and contributing to brain developmental wiring [PMID:10624965](https://pubmed.ncbi.nlm.nih.gov/10624965/). ([GO:0007420](http://purl.obolibrary.org/obo/GO_0007420))
- **GRIN1**: [EXTERNAL] [DATA] NMDA receptor activity supports brain development through experience-dependent synaptic refinement and circuit stabilization [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/). ([GO:0007420](http://purl.obolibrary.org/obo/GO_0007420))

#### Statistical Context

[DATA] 12 genes contribute to a 7.3-fold enrichment for brain development at FDR 6.31e-05, indicating coordinated neurodevelopmental programs.[GO-HIERARCHY] This process integrates transcriptional control, adhesion-guidance, and receptor-mediated activity to assemble mature circuits.

---

### Theme 11: neuron projection membrane

**Summary:** neuron projection membrane ([GO:0032589](http://purl.obolibrary.org/obo/GO_0032589))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The neuron projection membrane component captures dendritic and axonal surface domains, including dendrite membrane and axolemma subregions within [GO:0032589](http://purl.obolibrary.org/obo/GO_0032589), [GO:0032590](http://purl.obolibrary.org/obo/GO_0032590), and [GO:0030673](http://purl.obolibrary.org/obo/GO_0030673).[EXTERNAL] AMPA receptor exocytosis defines an activity-dependent domain on spine membranes, highlighting postsynaptic membrane specialization within dendrites [PMID:20434989](https://pubmed.ncbi.nlm.nih.gov/20434989/).[EXTERNAL] Caspr2 localizes to the axolemma at juxtaparanodes to scaffold K+ channels, demonstrating adhesion-driven compartmentalization of the axonal membrane [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/).

#### Key Insights

- [EXTERNAL] Dendrite membrane enrichment reflects receptor insertion and scaffolding that tune input integration at spines and shafts during plasticity. ([GO:0032590](http://purl.obolibrary.org/obo/GO_0032590))
- [EXTERNAL] Axolemmal specialization at juxtaparanodes organizes K+ channel clusters that shape action potential propagation and reliability. ([GO:0030673](http://purl.obolibrary.org/obo/GO_0030673))

#### Key Genes

- **KCNC2**: [INFERENCE] [INFERENCE] A Kv3 channel concentrated on neuronal projections enabling brief spikes and faithful high-frequency transmission by rapid repolarization. ([GO:0032590](http://purl.obolibrary.org/obo/GO_0032590))
- **ROBO2**: [INFERENCE] [INFERENCE] A guidance receptor contributing to polarized projection membrane architecture by coupling extracellular cues to cytoskeletal remodeling. ([GO:0030673](http://purl.obolibrary.org/obo/GO_0030673))
- **CNTNAP2**: [EXTERNAL] [DATA] An axolemmal adhesion molecule essential for juxtaparanodal K+ channel clustering and axonal domain polarization [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/). ([GO:0030673](http://purl.obolibrary.org/obo/GO_0030673))

#### Statistical Context

[DATA] 7 genes enrich neuron projection membrane 11.9-fold at FDR 1.10e-04 with significant subterms for dendrite membrane and axolemma.[GO-HIERARCHY] These subdomains delineate postsynaptic input zones and axonal conduction zones on neuronal surfaces.

---

### Theme 12: structural constituent of presynaptic active zone

**Summary:** structural constituent of presynaptic active zone ([GO:0098882](http://purl.obolibrary.org/obo/GO_0098882))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Structural constituent of the presynaptic active zone identifies proteins that scaffold release sites and couple Ca2+ channels to vesicles within [GO:0098882](http://purl.obolibrary.org/obo/GO_0098882).[INFERENCE] These structural elements define nanometer alignments that minimize synaptic delay and maximize release probability by positioning SNAREs, sensors, and channels in precise geometries.[EXTERNAL] RIM family proteins and ELKS/ERC interact with Ca2+ channels and synaptotagmin to prime vesicles and stabilize active zone architecture, operationalizing this structural function [PMID:11438518](https://pubmed.ncbi.nlm.nih.gov/11438518/).

#### Key Insights

- [EXTERNAL] RIM–Ca2+ channel–synaptotagmin complexes form the functional core that tethers vesicles at nanodomain Ca2+ microdomains for rapid exocytosis. ([GO:0098882](http://purl.obolibrary.org/obo/GO_0098882))
- [INFERENCE] ELKS/ERC and Piccolo extend the scaffold to recruit additional release machinery and maintain active zone integrity under sustained activity. ([GO:0098882](http://purl.obolibrary.org/obo/GO_0098882))

#### Key Genes

- **RIMS1**: [EXTERNAL] [DATA] A Rab3 effector that binds N-type Ca2+ channels and synaptotagmin, structuring nanodomain coupling for fast release [PMID:11438518](https://pubmed.ncbi.nlm.nih.gov/11438518/). ([GO:0098882](http://purl.obolibrary.org/obo/GO_0098882))
- **RIMS2**: [INFERENCE] [INFERENCE] An active zone scaffold that anchors vesicles near Ca2+ entry sites and promotes calcium-dependent neurotransmitter release. ([GO:0098882](http://purl.obolibrary.org/obo/GO_0098882))
- **PCLO**: [INFERENCE] [INFERENCE] Piccolo integrates cytoskeletal and vesicle-associated factors to maintain active zone structure during high-demand transmission. ([GO:0098882](http://purl.obolibrary.org/obo/GO_0098882))
- **ERC2**: [INFERENCE] [INFERENCE] An ELKS family component that links release machinery to the cytomatrix, preserving vesicle docking geometry. ([GO:0098882](http://purl.obolibrary.org/obo/GO_0098882))

#### Statistical Context

[DATA] Four core active zone scaffold genes yield 62.1-fold enrichment at FDR 1.17e-04, pinpointing the structural nexus of neurotransmitter release.[GO-HIERARCHY] This molecular function denotes constituents that physically build the active zone, distinct from regulators of its activity.

---

### Theme 13: transmembrane transporter binding

**Summary:** transmembrane transporter binding ([GO:0044325](http://purl.obolibrary.org/obo/GO_0044325))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Transmembrane transporter binding aggregates proteins that physically associate with channels and carriers to alter trafficking, gating, or stability within [GO:0044325](http://purl.obolibrary.org/obo/GO_0044325).[EXTERNAL] FGF13 binds Nav channels to modulate activation and conduction, exemplifying auxiliary subunits that tune transporter biophysics in excitable membranes [PMID:21817159](https://pubmed.ncbi.nlm.nih.gov/21817159/).[EXTERNAL] NEGR1 interaction with NPC2 implicates lipid transport machinery at neuronal membranes, linking transporter binding to cholesterol homeostasis that can influence receptor and channel landscapes [PMID:27940359](https://pubmed.ncbi.nlm.nih.gov/27940359/).

#### Key Insights

- [EXTERNAL] Auxiliary subunits and adaptors sculpt transporter availability and gating, converting signaling states into altered ion flux capacity. ([GO:0044325](http://purl.obolibrary.org/obo/GO_0044325))
- [EXTERNAL] Ubiquitin ligases target transporters for turnover, tying membrane excitability to proteostatic control of channel density. ([GO:0044325](http://purl.obolibrary.org/obo/GO_0044325))

#### Key Genes

- **DPP10**: [EXTERNAL] [DATA] An ancillary Kv4 channel subunit that binds and accelerates gating while promoting surface expression to shape dendritic excitability [PMID:27198182](https://pubmed.ncbi.nlm.nih.gov/27198182/). ([GO:0044325](http://purl.obolibrary.org/obo/GO_0044325))
- **NEGR1**: [EXTERNAL] [DATA] Binds NPC2 to influence intracellular cholesterol trafficking, potentially remodeling transporter-rich membrane microdomains [PMID:27940359](https://pubmed.ncbi.nlm.nih.gov/27940359/). ([GO:0044325](http://purl.obolibrary.org/obo/GO_0044325))
- **FGF13**: [EXTERNAL] [DATA] Associates with Nav channels to enhance activation and stabilize channel function, modulating excitability [PMID:21817159](https://pubmed.ncbi.nlm.nih.gov/21817159/). ([GO:0044325](http://purl.obolibrary.org/obo/GO_0044325))
- **NEDD4L**: [EXTERNAL] [EXTERNAL] An E3 ligase that binds channel substrates to drive ubiquitination and regulate membrane abundance of transporters [PMID:21463633](https://pubmed.ncbi.nlm.nih.gov/21463633/). ([GO:0044325](http://purl.obolibrary.org/obo/GO_0044325))

#### Statistical Context

[DATA] 10 genes confer 7.3-fold enrichment for transmembrane transporter binding at FDR 3.28e-04, highlighting auxiliary and regulatory partners of channels.[GO-HIERARCHY] This function complements channel complex enrichment by nominating interactors that set channel numbers and states.

---

### Theme 14: regulation of monoatomic ion transport

**Summary:** regulation of monoatomic ion transport ([GO:0043269](http://purl.obolibrary.org/obo/GO_0043269))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Regulation of monoatomic ion transport consolidates modulators of Na+, K+, and Ca2+ flux through effects on channel activity, trafficking, or localization within [GO:0043269](http://purl.obolibrary.org/obo/GO_0043269) and its sodium/potassium subterms.[EXTERNAL] NEDD4L ubiquitinates K+ channel substrates to downregulate potassium transport, while also impacting sodium channel surface levels, illustrating proteostatic control over ion flux [PMID:21463633](https://pubmed.ncbi.nlm.nih.gov/21463633/).[EXTERNAL] FGF13 enhances Nav1.6 activity, providing a positive regulator of sodium ion transport that boosts excitability in specific neuronal compartments [PMID:36696443](https://pubmed.ncbi.nlm.nih.gov/36696443/).

#### Key Insights

- [EXTERNAL] Negative regulation of potassium transport by ubiquitin ligases reduces repolarizing drive, shifting excitability thresholds. ([GO:1901379](http://purl.obolibrary.org/obo/GO_1901379))
- [EXTERNAL] Positive regulation of sodium ion transport by channel-associated FGFs increases depolarizing current to facilitate spike initiation. ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))

#### Key Genes

- **NEDD4L**: [EXTERNAL] [DATA] E3 ligase that decreases K+ channel surface density to negatively regulate potassium ion transmembrane transport [PMID:21463633](https://pubmed.ncbi.nlm.nih.gov/21463633/). ([GO:1901379](http://purl.obolibrary.org/obo/GO_1901379))
- **FGF13**: [EXTERNAL] [DATA] Enhances Nav1.6 function as a positive regulator of sodium ion transport, elevating depolarizing drive [PMID:36696443](https://pubmed.ncbi.nlm.nih.gov/36696443/). ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))
- **ANK3**: [INFERENCE] [INFERENCE] Ankyrin-G scaffolds Nav and KCNQ channels at AIS/nodes to regulate monoatomic ion flux through stabilized clustering and positioning. ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))
- **SCN3B**: [EXTERNAL] [DATA] A beta subunit that positively regulates sodium ion transport by improving Nav channel gating and trafficking [PMID:21051419](https://pubmed.ncbi.nlm.nih.gov/21051419/). ([GO:0002028](http://purl.obolibrary.org/obo/GO_0002028))

#### Statistical Context

[DATA] 15 genes are enriched 4.6-fold for regulation of monoatomic ion transport at FDR 3.72e-04 with significant sodium and potassium regulatory subterms.[GO-HIERARCHY] This process links structural scaffolding and ubiquitin pathways to quantitative control of ion flux.

---

### Theme 15: presynapse

**Summary:** presynapse ([GO:0098793](http://purl.obolibrary.org/obo/GO_0098793))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The presynapse component assembles vesicle pools, release machinery, and active zone scaffolds on the transmitter-emitting side within [GO:0098793](http://purl.obolibrary.org/obo/GO_0098793) and its membrane/active-zone/vesicle subterms.[EXTERNAL] RIMs bind N-type Ca2+ channels and synaptotagmin at the presynaptic membrane to position vesicles for rapid Ca2+-triggered fusion, epitomizing presynaptic specialization [PMID:11438518](https://pubmed.ncbi.nlm.nih.gov/11438518/).[EXTERNAL] Synaptotagmin’s juxtamembrane domain mediates membrane fusion steps critical for neuroexocytosis, linking Ca2+ sensing to bilayer merger at the presynaptic membrane [PMID:25973365](https://pubmed.ncbi.nlm.nih.gov/25973365/).

#### Key Insights

- [EXTERNAL] Presynaptic active zone cytomatrix proteins create nanodomain alignment of Ca2+ channels and primed vesicles for sub-millisecond release. ([GO:0098831](http://purl.obolibrary.org/obo/GO_0098831))
- [EXTERNAL] Vesicle membrane proteins such as synaptotagmin drive Ca2+-dependent membrane fusion that executes transmitter release. ([GO:0030672](http://purl.obolibrary.org/obo/GO_0030672))

#### Key Genes

- **RIMS1**: [EXTERNAL] [DATA] Localizes to the presynaptic membrane where it links Ca2+ channels and fusion sensors to docked vesicles, expediting release [PMID:11438518](https://pubmed.ncbi.nlm.nih.gov/11438518/). ([GO:0042734](http://purl.obolibrary.org/obo/GO_0042734))
- **ERC2**: [INFERENCE] [INFERENCE] An ELKS family scaffold that reinforces the active zone cytomatrix and sustains coupling between Ca2+ entry and vesicle fusion. ([GO:0098831](http://purl.obolibrary.org/obo/GO_0098831))
- **RIMS2**: [INFERENCE] [INFERENCE] Augments priming and release probability by stabilizing channel–sensor–vesicle interactions at active zones. ([GO:0098831](http://purl.obolibrary.org/obo/GO_0098831))
- **SYT1**: [EXTERNAL] [DATA] A vesicle Ca2+ sensor whose juxtamembrane domain is necessary for exocytosis at the presynaptic membrane [PMID:25973365](https://pubmed.ncbi.nlm.nih.gov/25973365/). ([GO:0042734](http://purl.obolibrary.org/obo/GO_0042734))

#### Statistical Context

[DATA] 13 genes confer 4.5-fold enrichment for the presynapse at FDR 4.02e-04, with strong sub-enrichment of the presynaptic membrane and active zone milieu.[GO-HIERARCHY] Child terms partition release site scaffolds and vesicle membranes that execute exocytosis.

---

### Theme 16: cell surface

**Summary:** cell surface ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The cell surface component aggregates receptors, adhesion molecules, and scaffolds that define extracellular-facing signaling interfaces within [GO:0009986](http://purl.obolibrary.org/obo/GO_0009986).[EXTERNAL] NMDA receptor subunits traffic to the neuronal surface where phosphorylation state governs stability and function, connecting surface residency to synaptic performance [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/).[EXTERNAL] Axonal Caspr2 and Robo receptors at the surface guide neurite outgrowth and domain specification, aligning extracellular interactions with circuit assembly [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/), [PMID:12504588](https://pubmed.ncbi.nlm.nih.gov/12504588/).

#### Key Insights

- [EXTERNAL] Receptor phosphorylation and proteolysis at the surface adjust synaptic receptor availability, tuning excitatory signaling and plasticity. ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- [EXTERNAL] Cell-adhesion–guided neurite outgrowth at the surface patterns connectivity, linking extracellular cues to intracellular cytoskeletal responses. ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Key Genes

- **GRIN1**: [EXTERNAL] [DATA] An NMDA receptor subunit resident at the neuronal cell surface whose phosphorylation regulates receptor stability and signaling [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **GRIN2B**: [EXTERNAL] [DATA] NMDA receptor GluN2B at the surface is subject to tyrosine phosphorylation that modulates receptor cleavage and function [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **CNTNAP2**: [EXTERNAL] [DATA] A surface adhesion protein enriched at juxtaparanodes that orchestrates K+ channel clustering and axonal domain identity [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))
- **ROBO2**: [EXTERNAL] [DATA] A surface guidance receptor mediating homophilic interactions to promote neurite outgrowth in Robo-positive neurons [PMID:12504588](https://pubmed.ncbi.nlm.nih.gov/12504588/). ([GO:0009986](http://purl.obolibrary.org/obo/GO_0009986))

#### Statistical Context

[DATA] 19 genes localize to the cell surface with 3.0-fold enrichment at FDR 9.98e-04, reflecting dense representation of receptors and adhesion molecules.[GO-HIERARCHY] The component interfaces with synaptic subcompartments to transduce extracellular signals into intracellular responses.

---

### Theme 17: node of Ranvier

**Summary:** node of Ranvier ([GO:0033268](http://purl.obolibrary.org/obo/GO_0033268))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Node of Ranvier enrichment pinpoints the excitable axonal gap where Nav and KCNQ channels are anchored to enable saltatory conduction within [GO:0033268](http://purl.obolibrary.org/obo/GO_0033268).[EXTERNAL] Ankyrin-G scaffolding retains KCNQ and Nav channels at nodes to stabilize resting potential and secure rapid spike regeneration between myelin segments [PMID:16525039](https://pubmed.ncbi.nlm.nih.gov/16525039/).[INFERENCE] Spectrin–ankyrin lattices with betaIV-spectrin provide the mechanical framework that preserves channel clustering and nodal integrity under conduction stress.

#### Key Insights

- [EXTERNAL] KCNQ–Nav co-clustering at nodes of Ranvier establishes low-threshold excitability and prevents aberrant firing during high-frequency trains. ([GO:0033268](http://purl.obolibrary.org/obo/GO_0033268))
- [INFERENCE] Spectrin–ankyrin complexes enforce nodal membrane organization, safeguarding conduction reliability in myelinated axons. ([GO:0033268](http://purl.obolibrary.org/obo/GO_0033268))

#### Key Genes

- **KCNQ3**: [EXTERNAL] [DATA] An M-current subunit concentrated at nodes and AIS that stabilizes resting potential and curbs repetitive firing [PMID:16525039](https://pubmed.ncbi.nlm.nih.gov/16525039/). ([GO:0033268](http://purl.obolibrary.org/obo/GO_0033268))
- **SCN2A**: [INFERENCE] [INFERENCE] A nodal Nav channel contributing to the depolarizing upstroke that regenerates action potentials at nodes of Ranvier. ([GO:0033268](http://purl.obolibrary.org/obo/GO_0033268))
- **SPTBN4**: [INFERENCE] [INFERENCE] BetaIV-spectrin maintains nodal cytoskeletal architecture that anchors voltage-gated channels for reliable conduction. ([GO:0033268](http://purl.obolibrary.org/obo/GO_0033268))

#### Statistical Context

[DATA] Four genes yield 21.7-fold enrichment at FDR 1.42e-03 for nodes of Ranvier, highlighting focal conduction machinery.[GO-HIERARCHY] This component complements axolemmal and juxtaparanodal terms that partition myelinated axon domains.

---

### Theme 18: ionotropic glutamate receptor signaling pathway

**Summary:** ionotropic glutamate receptor signaling pathway ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The ionotropic glutamate receptor signaling pathway captures AMPA, kainate, and NMDA receptor-mediated synaptic transmission cascades within [GO:0035235](http://purl.obolibrary.org/obo/GO_0035235).[EXTERNAL] Structural and genetic analyses show NMDA gating transitions in M3 helices and PAM-sensitive GluN2A interfaces that convert glutamate binding into Ca2+-permeable signaling driving plasticity [PMID:38538865](https://pubmed.ncbi.nlm.nih.gov/38538865/), [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/), [PMID:26919761](https://pubmed.ncbi.nlm.nih.gov/26919761/).[EXTERNAL] AMPA receptor GluA1/2 structures with TARP γ8 explain rapid Na+ influx and synaptic scaling mechanisms that implement the fast limb of ionotropic signaling [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/).

#### Key Insights

- [EXTERNAL] NMDA receptor activation requires glutamate plus co-agonist to open a Ca2+-permeable pore that triggers downstream plasticity programs. ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))
- [EXTERNAL] AMPA receptor complexes provide rapid depolarization that recruits NMDA receptors and converts synaptic input into spike output. ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))

#### Key Genes

- **GRIN1**: [EXTERNAL] [DATA] The obligatory NMDA subunit linking ligand binding to pore opening in the ionotropic signaling pathway [PMID:36309015](https://pubmed.ncbi.nlm.nih.gov/36309015/), [PMID:36959261](https://pubmed.ncbi.nlm.nih.gov/36959261/). ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))
- **GRIN2A**: [EXTERNAL] [DATA] GluN2A shapes deactivation kinetics and PAM sensitivity to tune NMDA receptor signaling in synaptic transmission [PMID:26919761](https://pubmed.ncbi.nlm.nih.gov/26919761/), [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/). ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))
- **GRIN2B**: [EXTERNAL] [DATA] GluN2B variants alter channel gating, affecting NMDA-mediated synaptic signaling and plasticity [PMID:38538865](https://pubmed.ncbi.nlm.nih.gov/38538865/), [PMID:26919761](https://pubmed.ncbi.nlm.nih.gov/26919761/). ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))
- **GRIA1**: [EXTERNAL] [DATA] AMPA receptor GluA1 participates in ionotropic signaling that drives fast excitatory transmission at synapses [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/). ([GO:0035235](http://purl.obolibrary.org/obo/GO_0035235))

#### Statistical Context

[DATA] Five genes drive 18.1-fold enrichment for the ionotropic glutamate receptor signaling pathway at FDR 1.72e-03, spanning AMPA and NMDA components.[GO-HIERARCHY] This pathway integrates ligand binding, pore gating, and downstream Ca2+-dependent signaling.

---

### Theme 19: Schaffer collateral - CA1 synapse

**Summary:** Schaffer collateral - CA1 synapse ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The Schaffer collateral–CA1 synapse component focuses on hippocampal glutamatergic connections specialized for LTP/LTD expression within [GO:0098685](http://purl.obolibrary.org/obo/GO_0098685).[EXTERNAL] Structural elucidation of GluA1/2 with TARP γ8 underpins AMPAR gating properties that express LTP at CA1 synapses, aligning with the enrichment of AMPA-centric components here [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/).[INFERENCE] Trans-synaptic organizers and phosphatases modulate receptor trafficking and nanodomain positioning to tune CA1 synaptic efficacy during learning.

#### Key Insights

- [EXTERNAL] AMPAR auxiliary subunits remodel receptor gating and trafficking to support CA1 LTP expression at Schaffer collateral synapses. ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))
- [INFERENCE] Adhesion-phosphatase systems recruit and stabilize AMPAR nanodomains to set synaptic gain during memory encoding. ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))

#### Key Genes

- **GRIA1**: [EXTERNAL] [DATA] An AMPA receptor subunit localized at CA1 synapses whose TARP-dependent architecture supports potentiation mechanisms [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/). ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))
- **LRFN2**: [INFERENCE] [INFERENCE] A synaptic adhesion molecule that promotes AMPA receptor surface stabilization to enhance CA1 synaptic transmission. ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))
- **PTPRD**: [INFERENCE] [INFERENCE] A receptor phosphatase that supports AMPAR complex stability and trafficking to sustain CA1 synaptic strength. ([GO:0098685](http://purl.obolibrary.org/obo/GO_0098685))

#### Statistical Context

[DATA] Seven genes confer 7.6-fold enrichment for the Schaffer collateral–CA1 synapse at FDR 1.75e-03, indicative of targeted hippocampal circuitry representation.[GO-HIERARCHY] This specialized component refines the broader glutamatergic synapse enrichment to a defined anatomical locus.

---

### Theme 20: dendritic shaft

**Summary:** dendritic shaft ([GO:0043198](http://purl.obolibrary.org/obo/GO_0043198))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The dendritic shaft component designates the microtubule-rich dendrite compartment that integrates local synaptic inputs and hosts metabotropic signaling within [GO:0043198](http://purl.obolibrary.org/obo/GO_0043198).[INFERENCE] Adhesion molecules and mGluRs on shafts regulate actin–microtubule coupling and local second messenger cascades to influence spine initiation and input integration.[INFERENCE] AMPARs on shafts contribute extrasynaptic sensing that can modulate local excitability and trigger plastic changes in adjacent spines.

#### Key Insights

- [INFERENCE] Dendritic shaft signaling via mGluRs modulates cAMP and Ca2+ pathways that bias spine formation and synaptic strength. ([GO:0043198](http://purl.obolibrary.org/obo/GO_0043198))
- [INFERENCE] Shaft adhesion proteins stabilize dendritic architecture to support reliable electrotonic propagation between synapses. ([GO:0043198](http://purl.obolibrary.org/obo/GO_0043198))

#### Key Genes

- **KIRREL3**: [INFERENCE] [INFERENCE] Adhesion receptor mediating homophilic interactions that stabilize dendritic shafts and organize nearby synaptic contacts. ([GO:0043198](http://purl.obolibrary.org/obo/GO_0043198))
- **NEGR1**: [INFERENCE] [INFERENCE] A membrane glycoprotein that promotes shaft growth and actin remodeling to support synaptic maturation. ([GO:0043198](http://purl.obolibrary.org/obo/GO_0043198))
- **GRM7**: [INFERENCE] [INFERENCE] A metabotropic glutamate receptor that modulates second messengers on shafts to regulate local excitability and plasticity. ([GO:0043198](http://purl.obolibrary.org/obo/GO_0043198))

#### Statistical Context

[DATA] Five genes provide 12.9-fold enrichment for the dendritic shaft at FDR 1.78e-03, highlighting structural and signaling roles in dendritic compartments.[GO-HIERARCHY] This component complements dendritic spine enrichment by capturing spine-adjacent signaling platforms.

---

### Theme 21: excitatory synapse

**Summary:** excitatory synapse ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The excitatory synapse component assembles presynaptic glutamate release machinery with postsynaptic AMPA/NMDA detectors to drive fast excitation within [GO:0060076](http://purl.obolibrary.org/obo/GO_0060076).[INFERENCE] Ca2+ sensors such as synaptotagmin and presynaptic CaV channels synchronize glutamate output to receptive AMPA/NMDA complexes, determining synaptic gain and timing.[INFERENCE] Kir3 and M-current channels in perisynaptic zones set the excitability context that converts synaptic input into spike output.

#### Key Insights

- [INFERENCE] Cooperative AMPA–NMDA receptor activation transforms glutamate transients into depolarization and Ca2+ signals required for LTP induction. ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))
- [INFERENCE] Presynaptic Ca2+ coupling and vesicle priming dictate quantal content and temporal precision at excitatory contacts. ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))

#### Key Genes

- **SYT1**: [INFERENCE] [INFERENCE] The vesicular Ca2+ sensor that couples presynaptic Ca2+ influx to synchronous glutamate release at excitatory synapses. ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))
- **KCNJ3**: [INFERENCE] [INFERENCE] A GIRK channel that hyperpolarizes neurons to control excitatory synaptic integration and spike threshold near excitatory contacts. ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))
- **CALB2**: [INFERENCE] [INFERENCE] A calcium buffer that shapes postsynaptic Ca2+ transients and thereby modulates plasticity at excitatory synapses. ([GO:0060076](http://purl.obolibrary.org/obo/GO_0060076))

#### Statistical Context

[DATA] Six genes are enriched 9.2-fold for the excitatory synapse at FDR 2.11e-03, reflecting both release and receptor-side determinants.[GO-HIERARCHY] This component sits under broader synapse terms and aligns with glutamatergic synapse enrichment.

---

### Theme 22: associative learning

**Summary:** associative learning ([GO:0008306](http://purl.obolibrary.org/obo/GO_0008306))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Associative learning aggregates molecular mediators of stimulus–stimulus contingency encoding within [GO:0008306](http://purl.obolibrary.org/obo/GO_0008306).[EXTERNAL] NMDA receptor integrity is required for preservation of remote memories, mechanistically tying Ca2+-dependent plasticity to learned associations [PMID:15003177](https://pubmed.ncbi.nlm.nih.gov/15003177/).[INFERENCE] PSD scaffolds and mGluR signaling reshape receptor content and spine structure to store cue–outcome relationships in distributed circuits.

#### Key Insights

- [EXTERNAL] NMDA-dependent synaptic plasticity provides the coincidence detection and consolidation machinery that underlies associative learning. ([GO:0008306](http://purl.obolibrary.org/obo/GO_0008306))
- [INFERENCE] PSD scaffold remodeling stabilizes potentiated synapses to encode learned associations over time. ([GO:0008306](http://purl.obolibrary.org/obo/GO_0008306))

#### Key Genes

- **TAFA2**: [INFERENCE] [INFERENCE] A secreted modulator that may tune neuronal signaling pathways influencing synaptic plasticity states during associative learning. ([GO:0008306](http://purl.obolibrary.org/obo/GO_0008306))
- **SHANK2**: [EXTERNAL] [EXTERNAL] A PSD scaffold that organizes glutamatergic receptors to sustain plasticity mechanisms required for memory encoding [PMID:22699620](https://pubmed.ncbi.nlm.nih.gov/22699620/). ([GO:0008306](http://purl.obolibrary.org/obo/GO_0008306))
- **CLSTN2**: [INFERENCE] [INFERENCE] A postsynaptic adhesion organizer that modulates receptor clustering to strengthen cue–outcome synaptic pathways. ([GO:0008306](http://purl.obolibrary.org/obo/GO_0008306))

#### Statistical Context

[DATA] Six genes contribute to 12.1-fold enrichment for associative learning at FDR 2.22e-03, implicating plasticity machinery in the input gene set.[GO-HIERARCHY] The process term links cellular plasticity modules to behavioral memory formation.

---

### Theme 23: neuron development

**Summary:** neuron development ([GO:0048666](http://purl.obolibrary.org/obo/GO_0048666))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Neuron development integrates lineage specification, neurite outgrowth, and synaptic maturation, with enrichment pointing to guidance and dendrite morphogenesis subprograms within [GO:0048666](http://purl.obolibrary.org/obo/GO_0048666) and children.[INFERENCE] Ubiquitin ligases and guidance receptors coordinate cytoskeletal dynamics and receptor turnover to sculpt maturing neuronal morphology.[EXTERNAL] Guidance cues via semaphorin–plexin or slit–robo pathways steer axons and dendrites, aligning molecular navigation with this developmental term [PMID:10197527](https://pubmed.ncbi.nlm.nih.gov/10197527/).

#### Key Insights

- [INFERENCE] Axon guidance programs translate extracellular gradients into directed growth cone steering to wire neural circuits. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))
- [INFERENCE] Dendrite morphogenesis regulators remodel microtubule–actin networks to establish receptive fields and synaptic capacity. ([GO:0048814](http://purl.obolibrary.org/obo/GO_0048814))

#### Key Genes

- **HECW2**: [INFERENCE] [INFERENCE] A HECT E3 ligase that shapes dendritic architecture through targeted protein turnover during neuronal maturation. ([GO:0048814](http://purl.obolibrary.org/obo/GO_0048814))
- **SEMA3C**: [INFERENCE] [INFERENCE] A secreted semaphorin that signals through plexins to repel or attract growth cones and organize axon trajectories. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))
- **UNC5D**: [INFERENCE] [INFERENCE] A netrin receptor mediating repulsive guidance that positions developing neurites in emerging circuits. ([GO:0007411](http://purl.obolibrary.org/obo/GO_0007411))
- **CAMK2B**: [INFERENCE] [INFERENCE] Activity-dependent kinase that phosphorylates cytoskeletal and synaptic targets to promote dendritic growth and stabilization. ([GO:0048814](http://purl.obolibrary.org/obo/GO_0048814))

#### Statistical Context

[DATA] Eight genes produce 7.6-fold enrichment for neuron development at FDR 2.27e-03, with significant child terms in axon guidance and dendrite morphogenesis.[GO-HIERARCHY] The term bridges extracellular guidance with intracellular remodeling to build functional neurons.

---

### Theme 24: axon initial segment

**Summary:** axon initial segment ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The axon initial segment component identifies the spike initiation zone scaffolded by ankyrin–spectrin complexes that retain Nav and KCNQ channels within [GO:0043194](http://purl.obolibrary.org/obo/GO_0043194).[EXTERNAL] Ankyrin-G-dependent retention of KCNQ and Nav channels at the AIS provides a shared mechanism for stabilizing excitability at electrically active domains [PMID:16525039](https://pubmed.ncbi.nlm.nih.gov/16525039/).[EXTERNAL] AIS cytoskeletal disruption mislocalizes tau and compromises the axo-dendritic barrier, underscoring the structural role of ANK3 in maintaining neuronal polarity [PMID:27356871](https://pubmed.ncbi.nlm.nih.gov/27356871/).

#### Key Insights

- [EXTERNAL] KCNQ channel retention at the AIS sets subthreshold conductances that restrain spontaneous spiking and define spike threshold. ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))
- [EXTERNAL] Ankyrin–spectrin scaffolds preserve AIS polarity and channel clustering, safeguarding initiation zone function under stress. ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))

#### Key Genes

- **LRRC7**: [INFERENCE] [INFERENCE] A scaffold interactor that helps stabilize ankyrin-G-based assemblies to concentrate excitability channels at the AIS. ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))
- **KCNQ3**: [EXTERNAL] [DATA] An M-current subunit concentrated at the AIS that lowers input resistance and raises spike threshold [PMID:16525039](https://pubmed.ncbi.nlm.nih.gov/16525039/). ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))
- **SPTBN4**: [INFERENCE] [INFERENCE] BetaIV-spectrin that supports the AIS cytoskeleton anchoring Nav and KCNQ channels for reliable spike initiation. ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))
- **ANK3**: [EXTERNAL] [DATA] Ankyrin-G maintains AIS polarity and scaffolds ion channels, preventing tau mislocalization under pathological conditions [PMID:27356871](https://pubmed.ncbi.nlm.nih.gov/27356871/). ([GO:0043194](http://purl.obolibrary.org/obo/GO_0043194))

#### Statistical Context

[DATA] Four genes yield 18.1-fold enrichment at FDR 2.64e-03 for the axon initial segment, capturing core scaffolds and channel components.[GO-HIERARCHY] This component specifies the somatic–axonal boundary for spike initiation within the broader axonal architecture.

---

### Theme 25: immune response

**Summary:** immune response ([GO:0006955](http://purl.obolibrary.org/obo/GO_0006955))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Immune response enrichment is driven by a neuro-immune guidance cue embedded in [GO:0006955](http://purl.obolibrary.org/obo/GO_0006955).[EXTERNAL] SEMA3C expression in inflammatory synovium implicates semaphorin signaling in immune cell migration and proliferative responses, suggesting shared chemotropic logic between axon guidance and leukocyte positioning [PMID:9168980](https://pubmed.ncbi.nlm.nih.gov/9168980/).[INFERENCE] Such crosstalk can modulate neuroinflammation impacting synaptic function and plasticity in disease contexts.

#### Key Insights

- [EXTERNAL] Semaphorin-driven guidance signals can be co-opted in immune tissues to direct cell movement and inflammatory tone. ([GO:0006955](http://purl.obolibrary.org/obo/GO_0006955))

#### Key Genes

- **SEMA3C**: [EXTERNAL] [DATA] A secreted guidance molecule implicated in rheumatoid synovial immune responses, indicating semaphorin roles beyond the nervous system [PMID:9168980](https://pubmed.ncbi.nlm.nih.gov/9168980/). ([GO:0006955](http://purl.obolibrary.org/obo/GO_0006955))

#### Statistical Context

[DATA] One gene yields apparent enrichment for immune response at FDR 2.99e-03 despite low fold noted in the study summary, reflecting a focused contribution from a guidance cytokine.[GO-HIERARCHY] This process sits outside the core synaptic axis yet plausibly interfaces with synapse remodeling during inflammation.

---

### Theme 26: ERBB4-ERBB4 signaling pathway

**Summary:** ERBB4-ERBB4 signaling pathway ([GO:0038138](http://purl.obolibrary.org/obo/GO_0038138))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The ERBB4–ERBB4 signaling pathway term aggregates neuregulin–ErbB receptor dimer signaling with downstream kinase cascades within [GO:0038138](http://purl.obolibrary.org/obo/GO_0038138).[EXTERNAL] Neuregulin-1 and -3 activate ERBB4 to regulate differentiation and growth in neural and immune contexts, with defined isoform-specific receptor activation patterns [PMID:12466964](https://pubmed.ncbi.nlm.nih.gov/12466964/), [PMID:9275162](https://pubmed.ncbi.nlm.nih.gov/9275162/).[EXTERNAL] In macrophages, NRG1–ERBB4 signaling dampens fibrotic responses, illustrating context-dependent modulation of cellular state by this pathway [PMID:28822966](https://pubmed.ncbi.nlm.nih.gov/28822966/).

#### Key Insights

- [EXTERNAL] Neuregulin ligands bias ERBB receptor dimer composition to sculpt downstream signaling strength and cell-state transitions. ([GO:0038138](http://purl.obolibrary.org/obo/GO_0038138))
- [EXTERNAL] ERBB4 signaling can impose anti-fibrotic programs in immune cells, highlighting cross-tissue roles for neuregulin pathways. ([GO:0038138](http://purl.obolibrary.org/obo/GO_0038138))

#### Key Genes

- **NRG1**: [EXTERNAL] [DATA] A neuregulin ligand that activates ERBB4 to regulate cellular programs including antifibrotic responses in macrophages [PMID:28822966](https://pubmed.ncbi.nlm.nih.gov/28822966/). ([GO:0038138](http://purl.obolibrary.org/obo/GO_0038138))
- **NRG3**: [EXTERNAL] [DATA] A neural-enriched neuregulin that binds and activates ERBB4, modulating growth and differentiation programs [PMID:9275162](https://pubmed.ncbi.nlm.nih.gov/9275162/). ([GO:0038138](http://purl.obolibrary.org/obo/GO_0038138))
- **ERBB4**: [EXTERNAL] [DATA] A receptor tyrosine kinase preferentially activated by neuregulin isoforms with distinct receptor activation profiles [PMID:12466964](https://pubmed.ncbi.nlm.nih.gov/12466964/). ([GO:0038138](http://purl.obolibrary.org/obo/GO_0038138))

#### Statistical Context

[DATA] Three genes provide 54.4-fold enrichment at FDR 2.99e-03 for ERBB4–ERBB4 signaling, indicating a coherent ligand–receptor module within the dataset.[GO-HIERARCHY] This pathway interfaces with synaptic organization themes where ERBB4 modulates inhibitory and excitatory circuit maturation.

---

### Theme 27: neuron to neuron synapse

**Summary:** neuron to neuron synapse ([GO:0098984](http://purl.obolibrary.org/obo/GO_0098984))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The neuron-to-neuron synapse component emphasizes structural and functional elements at direct neuronal contacts within [GO:0098984](http://purl.obolibrary.org/obo/GO_0098984).[INFERENCE] Presynaptic metabotropic and ionotropic mechanisms set release probability while postsynaptic receptors determine gain and temporal summation, jointly defining efficacy at inter-neuronal synapses.[INFERENCE] Guidance receptors retained at mature synapses continue to influence alignment and stability of trans-synaptic adhesions.

#### Key Insights

- [INFERENCE] mGluR7 presynaptically depresses transmitter release to tune short-term plasticity at neuron-to-neuron contacts. ([GO:0098984](http://purl.obolibrary.org/obo/GO_0098984))
- [INFERENCE] Semaphorin–plexin signaling refines synaptic connectivity by stabilizing appropriate neuron-neuron contacts and pruning mismatches. ([GO:0098984](http://purl.obolibrary.org/obo/GO_0098984))

#### Key Genes

- **GRM7**: [INFERENCE] [INFERENCE] A presynaptic mGluR that inhibits cAMP production to reduce release probability and adjust synaptic filtering. ([GO:0098984](http://purl.obolibrary.org/obo/GO_0098984))
- **PLXNA4**: [INFERENCE] [INFERENCE] A semaphorin receptor that shapes synapse formation and maintenance through activity-dependent guidance signaling. ([GO:0098984](http://purl.obolibrary.org/obo/GO_0098984))
- **PTPRD**: [INFERENCE] [INFERENCE] A synaptic phosphatase that modulates adhesion and receptor phosphorylation to stabilize neuron-neuron synaptic efficacy. ([GO:0098984](http://purl.obolibrary.org/obo/GO_0098984))

#### Statistical Context

[DATA] Six genes are enriched 8.2-fold for the neuron-to-neuron synapse at FDR 3.79e-03, representing pre- and postsynaptic determinants of efficacy.[GO-HIERARCHY] This component overlaps with excitatory and inhibitory synapse specializations captured in parallel themes.

---

### Theme 28: nucleic acid metabolic process

**Summary:** nucleic acid metabolic process ([GO:0090304](http://purl.obolibrary.org/obo/GO_0090304))  · Anchor confidence: **FDR<0.01**

> ⚠ Content validation failed for this theme — showing data only.

**FDR**: 3.90e-03 · **Genes (15)**: CELF4, CHD5, DLX5, ERBB4, ESRRG, HDAC9, HIVEP3, MYT1L, PBX1, RBFOX1, RUNX1T1, SCML4, SRRM4, TENM2, ZNF536

---

### Theme 29: juxtaparanode region of axon

**Summary:** juxtaparanode region of axon ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] The juxtaparanode region of axon component identifies the myelinated axonal domain hosting Shaker-type K+ channels anchored by Caspr2 and cytoskeletal scaffolds within [GO:0044224](http://purl.obolibrary.org/obo/GO_0044224).[INFERENCE] This lateral domain electrically insulates internodes and shapes repolarization between nodes to prevent ectopic excitability.[EXTERNAL] Caspr2 targeting to juxtaparanodes specifies K+ channel clustering, while spectrin scaffolds maintain domain integrity during repetitive conduction [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/).

#### Key Insights

- [EXTERNAL] Caspr2-driven juxtaparanodal assembly concentrates Kv channels to suppress internodal depolarization and stabilize conduction. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))
- [INFERENCE] Spectrin-based scaffolds preserve juxtaparanodal architecture under mechanical and electrical load. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))

#### Key Genes

- **SPTBN4**: [INFERENCE] [INFERENCE] A spectrin that upholds juxtaparanodal cytoskeletal structure and supports K+ channel anchoring in myelinated axons. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))
- **DLG2**: [INFERENCE] [INFERENCE] A MAGUK scaffold that can organize membrane complexes adjacent to nodes to stabilize channel clustering. ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))
- **CNTNAP2**: [EXTERNAL] [DATA] Caspr2 localizes to juxtaparanodes to coordinate Shaker-type K+ channel clustering and axonal domain identity [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/). ([GO:0044224](http://purl.obolibrary.org/obo/GO_0044224))

#### Statistical Context

[DATA] Three genes confer 27.2-fold enrichment for the juxtaparanode at FDR 5.94e-03, emphasizing compartmental specialization of myelinated axons.[GO-HIERARCHY] This component complements node and axolemma terms to complete the domain map of myelinated fibers.

---

### Theme 30: sodium channel regulator activity

**Summary:** sodium channel regulator activity ([GO:0017080](http://purl.obolibrary.org/obo/GO_0017080))  · Anchor confidence: **FDR<0.01**

[GO-HIERARCHY] Sodium channel regulator activity aggregates proteins that modulate Nav channel gating, trafficking, and stability within [GO:0017080](http://purl.obolibrary.org/obo/GO_0017080).[EXTERNAL] FGF13 binds Nav1.6 and augments activation, while SCN3B variants alter channel function and cardiac excitability, exemplifying direct regulatory mechanisms for Nav activity [PMID:36696443](https://pubmed.ncbi.nlm.nih.gov/36696443/), [PMID:21051419](https://pubmed.ncbi.nlm.nih.gov/21051419/), [PMID:20042427](https://pubmed.ncbi.nlm.nih.gov/20042427/).[INFERENCE] Ankyrin scaffolding further regulates functional channel density by retaining Nav at strategic axonal sites to ensure robust excitability.

#### Key Insights

- [EXTERNAL] Intracellular FGFs act as Nav modulators to tune activation kinetics and availability for repetitive firing. ([GO:0017080](http://purl.obolibrary.org/obo/GO_0017080))
- [EXTERNAL] Beta subunits regulate Nav trafficking and gating, shaping tissue-specific excitability and arrhythmia susceptibility. ([GO:0017080](http://purl.obolibrary.org/obo/GO_0017080))

#### Key Genes

- **FGF14**: [EXTERNAL] [EXTERNAL] An intracellular FGF that modulates Nav channel gating and conduction properties to set neuronal firing patterns [PMID:21817159](https://pubmed.ncbi.nlm.nih.gov/21817159/). ([GO:0017080](http://purl.obolibrary.org/obo/GO_0017080))
- **FGF13**: [EXTERNAL] [DATA] A Nav1.6-associated regulator that enhances channel activation, boosting depolarizing drive in excitable cells [PMID:36696443](https://pubmed.ncbi.nlm.nih.gov/36696443/), [PMID:21817159](https://pubmed.ncbi.nlm.nih.gov/21817159/). ([GO:0017080](http://purl.obolibrary.org/obo/GO_0017080))
- **SCN3B**: [EXTERNAL] [DATA] A beta3 subunit whose mutations modify Nav function and are linked to atrial fibrillation and ventricular fibrillation phenotypes [PMID:21051419](https://pubmed.ncbi.nlm.nih.gov/21051419/), [PMID:20042427](https://pubmed.ncbi.nlm.nih.gov/20042427/). ([GO:0017080](http://purl.obolibrary.org/obo/GO_0017080))
- **NEDD4L**: [INFERENCE] [INFERENCE] An E3 ubiquitin ligase that decreases Nav surface density to restrain sodium currents and excitability. ([GO:0017080](http://purl.obolibrary.org/obo/GO_0017080))

#### Statistical Context

[DATA] Five genes provide 13.6-fold enrichment for sodium channel regulator activity at FDR 6.23e-03, highlighting direct modulators of Nav function.[GO-HIERARCHY] This molecular function refines the broader ion transport regulation theme to Nav-targeted mechanisms.

---

## Hub Genes

- **GRIA1**: [EXTERNAL] [EXTERNAL] GRIA1 encodes the AMPA receptor GluA1 that conducts Na+ to rapidly depolarize postsynaptic membranes and expresses LTP at hippocampal CA1 via TARP-dependent gating and trafficking [PMID:30872532](https://pubmed.ncbi.nlm.nih.gov/30872532/).[EXTERNAL] GRIA1 localizes to spine membranes where activity-dependent exocytosis remodels postsynaptic receptor content and plasticity states [PMID:20434989](https://pubmed.ncbi.nlm.nih.gov/20434989/).
- **GRIN1**: [EXTERNAL] [DATA] GRIN1 provides the obligatory NMDA subunit enabling excitatory transmission and positive regulation of EPSPs across diverse receptor assemblies [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/), [PMID:36959261](https://pubmed.ncbi.nlm.nih.gov/36959261/).[EXTERNAL] NR1-containing receptors are modulated by Src-family kinases and MAGUK interactions that tune phosphorylation state, stability, and plasticity coupling [PMID:40602877](https://pubmed.ncbi.nlm.nih.gov/40602877/).
- **GRIN2A**: [EXTERNAL] [DATA] GRIN2A shapes NMDA receptor deactivation and Ca2+ signaling, reinforcing LTP and circuit maturation during development and adult plasticity [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/), [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/).[DATA] PAM sensitivity at the GluN1–GluN2A interface demonstrates allosteric control nodes coordinating multi-theme receptor function [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/).
- **GRIN2B**: [EXTERNAL] [DATA] GRIN2B confers distinct gating kinetics and tyrosine phosphorylation regulation that impact receptor cleavage, synaptic localization, and LTP [PMID:17526495](https://pubmed.ncbi.nlm.nih.gov/17526495/), [PMID:40602877](https://pubmed.ncbi.nlm.nih.gov/40602877/).[DATA] Its Ca2+-permeable signaling underlies memory processes and brain development captured across multiple enriched themes [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/).
- **CACNA1C**: [INFERENCE] [INFERENCE] CACNA1C encodes CaV1.2 L-type channels that support prolonged Ca2+ entry to couple depolarization with transcriptional and release machinery across neuronal and cardiac contexts.[INFERENCE] Localization to dendritic shafts and soma links this channel to excitability set points and synaptic integration across themes.
- **GABRA2**: [EXTERNAL] [DATA] GABRA2 assembles into synaptic GABAA receptors providing fast Cl− currents that hyperpolarize neurons and initiate inhibitory synapse formation [PMID:29950725](https://pubmed.ncbi.nlm.nih.gov/29950725/), [PMID:23909897](https://pubmed.ncbi.nlm.nih.gov/23909897/).[EXTERNAL] Alpha-subunit composition dictates synapse subtype selection and micro-architecture, aligning with organization and membrane potential themes [PMID:25489750](https://pubmed.ncbi.nlm.nih.gov/25489750/).
- **GABRG2**: [EXTERNAL] [DATA] GABRG2 organizes benzodiazepine-sensitive GABAA receptors and can initiate inhibitory synapse assembly, stabilizing inhibitory networks across synaptic themes [PMID:23909897](https://pubmed.ncbi.nlm.nih.gov/23909897/), [PMID:25489750](https://pubmed.ncbi.nlm.nih.gov/25489750/).[INFERENCE] Gamma2-containing receptors cluster at perisomatic synapses to exert strong control over spike initiation.
- **CNTNAP2**: [EXTERNAL] [DATA] CNTNAP2/Caspr2 localizes at the axolemma and juxtaparanodes to cluster Shaker-type K+ channels, coordinating axonal conduction domains across axon-related themes [PMID:19706678](https://pubmed.ncbi.nlm.nih.gov/19706678/).[DATA] As a brain development gene, it contributes to myelinated domain architecture required for high-velocity signaling [PMID:10624965](https://pubmed.ncbi.nlm.nih.gov/10624965/).
- **KCNC2**: [INFERENCE] [INFERENCE] KCNC2 encodes a Kv3 channel that accelerates repolarization to permit high-frequency firing, influencing presynaptic release probability and inhibitory circuitry roles across themes.[INFERENCE] Axonal enrichment supports action potential narrowing and faithful timing in fast-spiking interneurons.
- **SYT1**: [EXTERNAL] [DATA] SYT1 is the vesicular Ca2+ sensor whose juxtamembrane domain is necessary for neuroexocytosis, synchronizing release at presynaptic membranes across synapse themes [PMID:25973365](https://pubmed.ncbi.nlm.nih.gov/25973365/).[INFERENCE] Its Ca2+-binding C2 domains couple AP-triggered Ca2+ influx to ultrafast fusion for precise anterograde signaling.
- **ANK3**: [EXTERNAL] [DATA] ANK3 (ankyrin-G) scaffolds Nav and KCNQ channels at AIS and nodes, preserving polarity and excitability across axonal domain themes [PMID:27356871](https://pubmed.ncbi.nlm.nih.gov/27356871/), [PMID:16525039](https://pubmed.ncbi.nlm.nih.gov/16525039/).[INFERENCE] Its membrane-adaptor role extends to cell surface organization linking cytoskeleton to adhesion complexes.
- **CACNA1D**: [INFERENCE] [INFERENCE] CACNA1D encodes CaV1.3 channels that boost subthreshold depolarizations and pacemaking while coupling to Ca2+-dependent secretion in neurons and endocrine cells across themes.[INFERENCE] Its gating near resting potentials supports modulation of membrane potential and release dynamics.
- **ERBB4**: [EXTERNAL] [DATA] ERBB4 integrates neuregulin signaling to regulate inhibitory and excitatory synapse organization and plasticity, coordinating multiple synaptic themes [PMID:12466964](https://pubmed.ncbi.nlm.nih.gov/12466964/).[INFERENCE] Postsynaptic ERBB4 in interneurons modulates circuit E/I balance and learning-related remodeling.
- **GRM5**: [INFERENCE] [INFERENCE] GRM5 activates Gq/PLC pathways to mobilize Ca2+ and remodel the PSD, coordinating synapse organization and anterograde signaling across postsynaptic themes.[INFERENCE] Its coupling to endocannabinoid production provides feedback control of presynaptic release.
- **GRIK4**: [EXTERNAL] [EXTERNAL] GRIK4 forms kainate receptors that mediate cation influx to depolarize postsynaptic neurons and sculpt synaptic integration and plasticity [PMID:34706237](https://pubmed.ncbi.nlm.nih.gov/34706237/).[INFERENCE] Presynaptic kainate receptors modulate glutamate release to tune information transfer across synapses.
- **GABRB1**: [EXTERNAL] [DATA] GABRB1 contributes to GABAA receptor pore formation enabling Cl− influx for inhibition and can participate in negative regulation of GABAergic transmission via accessory proteins [PMID:29950725](https://pubmed.ncbi.nlm.nih.gov/29950725/), [PMID:33234346](https://pubmed.ncbi.nlm.nih.gov/33234346/).[INFERENCE] Broad synaptic distribution places it at the center of E/I balance across multiple themes.
- **KCNJ3**: [INFERENCE] [INFERENCE] KCNJ3 (GIRK1) produces G protein-gated K+ currents that hyperpolarize neurons and dampen excitatory drive, linking synaptic signaling to membrane potential themes.[INFERENCE] At excitatory synapses, GIRKs set integration thresholds and temporal summation windows.
- **DLG2**: [INFERENCE] [INFERENCE] DLG2/PSD-93 scaffolds receptors and channels at synapses and axonal domains, stabilizing NMDA/AMPA complexes and potassium channels across multiple compartments.[INFERENCE] Its MAGUK interactions coordinate trans-synaptic signaling with cytoskeletal anchoring.
- **SCN3B**: [EXTERNAL] [DATA] SCN3B regulates Nav channel gating and trafficking, positively regulating sodium transport and shaping action potential properties across membrane potential and node themes [PMID:21051419](https://pubmed.ncbi.nlm.nih.gov/21051419/), [PMID:20042427](https://pubmed.ncbi.nlm.nih.gov/20042427/), [PMID:35301303](https://pubmed.ncbi.nlm.nih.gov/35301303/).
- **KCNQ3**: [EXTERNAL] [DATA] KCNQ3 concentrates at AIS and nodes to generate the M-current that stabilizes resting potential and prevents aberrant firing across axonal domain themes [PMID:16525039](https://pubmed.ncbi.nlm.nih.gov/16525039/).[INFERENCE] Its nodal clustering couples with ankyrin-G to maintain excitability homeostasis under high activity loads.

## Overall Summary

[DATA] The enrichment profile is dominated by ion channel complexes and synaptic compartments with exceptionally low FDRs, indicating a coherent modules-of-excitability signature spanning presynaptic release, postsynaptic detection, and axonal conduction.

[GO-HIERARCHY] Concordant enrichment of glutamatergic and GABA-ergic synapse components, postsynaptic density membrane, and presynaptic active zone terms resolves a multi-compartment blueprint for fast neurotransmission and its plasticity control.

[EXTERNAL] Mechanistic anchors include NMDA and AMPA receptor structural–functional studies, GABAA receptor assembly rules, and active zone scaffolding that collectively explain how EPSP/IPSP balance and LTP/LTD emerge in this gene set [PMID:26875626](https://pubmed.ncbi.nlm.nih.gov/26875626/), [PMID:29950725](https://pubmed.ncbi.nlm.nih.gov/29950725/), [PMID:11438518](https://pubmed.ncbi.nlm.nih.gov/11438518/).

[INFERENCE] Axonal domain terms for nodes, axolemma, and juxtaparanodes integrate with sodium/potassium regulatory themes to explain faithful spike initiation and saltatory conduction coupling synaptic input to network output.

[INFERENCE] Upstream RNA and receptor-tyrosine-kinase pathways align with synaptic modules to provide transcriptional, splicing, and trophic levers for circuit maturation and adaptive remodeling.

> **Note:** Statements tagged \[INFERENCE\] without PMID citations are based on the LLM's latent biological knowledge and have not been independently verified against the literature. These should be treated as hypotheses requiring validation.

