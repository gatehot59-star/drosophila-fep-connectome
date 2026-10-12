---
title: "Signal Propagation Properties in the *Drosophila melanogaster* Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification"
subtitle: "Version 2.0 · Preprint, not peer reviewed"
author:
  - name: Jorge Abraham Mendieta
    affiliation: "Independent Researcher, Salta, Argentina · ORCID 0009-0009-3831-6784"
    email: profeabrahamm@gmail.com
date: "October 2026"
lang: en
papersize: a4
fontsize: 10pt
abstract: |
  Using the complete FlyWire v783 connectome (*N* = 138,639 neurons; *E* = 15,091,983 directed connections carrying 54,492,922 synapses), three compatible parameter-free neural models and four null-model families, we characterize three signal propagation properties of the *Drosophila melanogaster* brain. **(1) Active intermodal isolation.** The topology separates sensory signals via directed inhibition (contralateral cancellation = 1.37). During stimulus, separation is largely explained by generic modular structure; post-stimulus amplification requires specific wiring (*Z*~CP~ = +14.8σ). **(2) Differential motor access, set by anatomy and restricted within it.** Against degree-preserving controls, somatosensory afferents have privileged access to the motor output population (Δ = +0.365; *p*~perm~ < 0.01), dominated by mechanosensory neurons (95.2%), and canonical gustatory neurons alone are significant (*Z* = +4.5σ). Against uniform density, three of eight reproducible sensory classes are enriched (up to 12.9×) and four are depleted (down to 0.018×). When randomization also preserves the neuropil of each connection, the modality ordering of two-hop access to the 110 brain motor neurons inverts: it is an expression of neuropil co-location. What survives the anatomical control is a restriction: gustatory afferents contact 10 brain motor neurons where co-location predicts 101.6 (*z* = −78.9), consistent with the interneuron-mediated proboscis extension circuit. **(3) Non-trivial temporal amplification.** Under graded dynamics, cosine RDI rises from 0.63 to 0.83 post-stimulus, an effect that survives the community-preserving control (*Z*~CP~ = +14.8σ). Reciprocal connectivity (26.60% of connections; 13.98% under the field-standard five-synapse threshold, matching published values) exceeds a degree- and block-preserving null 20.59-fold (0 of 40 nulls), but its global magnitude is not distinctive across nervous systems; we report it resolved over directed pairs of functional cell classes. The update parameter τ = 0.119 corresponds to an effective time constant of 7.9 ms at 1 ms steps, inside the range over which amplification is robust. Version 2.0 corrects a 32-bit integer overflow that inflated graph density 9.42-fold in v1.0, together with every result normalised by it.
---

**Version 2.0.** Zenodo concept DOI 10.5281/zenodo.19136947, which resolves to the latest version. Version 1.0, deposited on 20 March 2026, has DOI 10.5281/zenodo.19136948 and is not withdrawn. This version applies the corrections of the accompanying erratum and replaces the motor-access interpretation of v1.0 with one tested against an anatomical null (Section 3.4). Numbered changes are listed at the end of the paper. Sections 1 to 3.3 keep the numbering of v1.0; Sections 3.5 to 3.7 correspond to Sections 3.4 to 3.6 of v1.0. Table numbers follow v1.0; Tables 5b and 5c are new.

**Keywords:** *Drosophila* connectome · signal propagation · FlyWire · null models · neuropil · reciprocity · motor access · SparseLTC · bio-inspired computing

# 1 Introduction

## 1.1 The phenomenon

The FlyWire consortium published the first complete connectome of the adult *Drosophila melanogaster* brain [Dorkenwald et al., 2024], and its network statistics were analysed in a companion paper [Lin et al., 2024]. Shiu et al. [2024] demonstrated that a leaky integrate-and-fire model on this connectome, without weight optimization, propagated gustatory signals to specifically activate proboscis extension response (PER) motor neurons. Jin et al. [2026] extended the phenomenon to locomotor control, using the connectome as a graph neural controller for a biomechanical model, and Bates et al. [2026] described distributed control circuits across a combined brain-and-cord connectome.

**Question.** What quantifiable properties of the topology contribute to stimulus-specific propagation without algorithmic weight optimization?

**Note.** The topology was optimized by about 150 million years of evolution. "Without algorithmic optimization" means that no learning algorithm adjusted weights in our models.

## 1.2 Related work

Lin et al. [2024] report the network statistics of this connectome, including connection probability, reciprocity resolved by anatomical neuropil, and random-graph models constrained by inter-neuropil connection probabilities (NPC) and by inter-neuron distance (NND). Betzel et al. [2026] demonstrated convergence of sensory cascades on shared integration nodes. Bates et al. [2026] found, in a brain-and-cord connectome, that effector neurons are primarily influenced by sensory neurons of the same body part. Costi et al. [2025] showed that connectome-based reservoirs are resilient to overfitting in time-series prediction. Yu et al. [2026] reached 98% accuracy on MNIST with a Biological Processing Unit derived from the larval connectome. Hasani et al. [2022] derived closed-form approximations of liquid time-constant networks. Váša & Mišić [2022] review null models in network neuroscience.

## 1.3 Contributions

Three propagation properties, validated with three compatible neural models and four null-model families:

1. **Active intermodal isolation**, with demarcation of what is modular and what is specific.
2. **Differential motor access**: gustatory and mechanosensory decomposition, density analysis, depth profiles and, new in this version, a test of the modality ordering against a neuropil-preserving null.
3. **Non-trivial temporal amplification** that survives the community-preserving control.

Additionally, we report connectome reciprocity as a rank against null ensembles, under two inclusion criteria and resolved over directed pairs of functional cell classes, and we compare the temporal parameter with published electrophysiology.

# 2 Methods

## 2.1 Connectome

FlyWire v783: 15,091,983 directed connections (ordered pairs of connected neurons, carrying 54,492,922 synapses) among 138,639 neurons. Weight: Excitatory × Connectivity (9,059,302 excitatory connections, 60.0%; 6,032,681 inhibitory, 40.0%; E/I = 1.50). Graph density is 15,091,983 / (138,639 × 138,638) = 7.85197 × 10^−4^, computed in arbitrary-precision integers. v1.0 reported 0.0074 because the product *N*(*N* − 1) overflowed a 32-bit integer (Erratum, item 1).

**Pinned inputs.** Connectivity matrix md5 `3d802fd542b5d18570ba1ba0bb0abed9`. Cell annotations [Schlegel et al., 2024] pinned to commit `17fc57722002e1a7d38cdd0c89ac382bf92718da` of the annotation repository, md5 `719904abad876c68ace1b5690c9b9b63`. The string "v783" pins the connectome only, not the annotations, which changed between March and August 2026.

**Inclusion criterion.** Unless stated otherwise all connections are used, without a synapse threshold, as in v1.0. Where the choice matters, results are also reported under the five-synapse threshold adopted by Dorkenwald et al. [2024], Lin et al. [2024] and Bates et al. [2026], which retains 2,700,513 connections (17.9%; Table S2).

## 2.2 Normalization

For temporal propagation: columnar normalization and scaling by 0.99 [Jaeger, 2001]. Static analyses use *W* unnormalized.

## 2.3 Populations

Table 1: Sensory and motor populations.

| Population | Criterion | *N* |
|---|---|---|
| Visual L | `super_class` ∈ {optic, visual_projection}, side = left | 43,056 |
| Olfactory | `super_class` = olfactory ∨ `cell_class` ∈ {ORN, olfactory} | 2,279 |
| Somatosensory | `cell_class` ∈ {gustatory, GRN, mechanosensory} | 3,067 |
| Gustatory | `cell_class` = gustatory | 408 |
| Mechanosensory | `cell_class` = mechanosensory | 2,659 |
| Motor output | `super_class` ∈ {descending, motor} ∨ flow = efferent | 1,485 |
| Brain motor neurons (Section 3.4) | `super_class` = motor | 110 |

The motor output population, labelled "Motor" in v1.0, is mostly descending: with the pinned annotations it comprises 1,299 descending, 110 motor and 76 endocrine neurons. It is called *motor output* here so as not to imply that it consists of motor neurons. For the density analysis v1.0 declared ten canonical sensory classes with *N* ≥ 10 and reported nine; the tenth has not been identified (Erratum, item 6).

## 2.4 Null models

**Maslov–Sneppen (MS).** Preserves the degree distribution; destroys modularity. Swap target 3*E* = 45,275,949; measured acceptance 98.5% (v1.0 stated 100%, which the constraints do not permit). *N* = 100 for static analyses, generated in three parallel batches (34 + 33 + 33) with independent seeds; *N* = 5 for temporal analyses [Maslov & Sneppen, 2002]. The routing comparison of Section 3.3 uses 40 realizations verified to preserve in-degree and out-degree exactly.

**Community-preserving (CP).** For each pair of super-classes (A, B), targets are shuffled within the block A → B. Preserves the number of connections between every pair of communities, the weight distribution and the modular structure; destroys individual neuron identity, reciprocity and motifs. *N* = 10 static; *N* = 5 temporal [Váša & Mišić, 2022]. The reciprocity rank of Section 3.6 uses 40 realizations that additionally preserve in-degree and out-degree. This construction belongs to the same family as the neuropil-connection (NPC) model of Lin et al. [2024], at a different granularity (functional super-classes rather than 78 anatomical neuropils); no novelty is claimed for it, and the two have not been compared side by side.

**Analytical property of the CP null.** Net RDI at 1 hop is exactly invariant under the CP null (σ = 0), because *F*~motor~, the sum of *W*~ij~ over *i* in the stimulated population and *j* in the motor population, depends only on the block weight sum, not on its distribution among individual neurons. Verified empirically: *F*~motor~ is identical for 3 CP realizations. The same reasoning makes the count of connections from a sensory class into the motor output population untestable against this null (Section 3.3). The CP null is informative only for multi-hop and temporal metrics, where the intra-block distribution affects propagation.

**Target-permutation ensembles for multi-hop access**, degree-preserving and neuropil-preserving with 40 realizations each, are described with that analysis in Section 3.4.

## 2.5 Neural models

**SparseLTC** (primary), Equation 1:

$$h_{t+1} = (1-\tau) h_t + \tau \tanh(W_n^{\top} h_t + s_t)$$

with τ = 0.119. **Linear:** without tanh. **LIF-soft:** continuous rate. **LIF-hard:** binary spiking. Stimulus: amplitude 1.0, *t* ∈ [10, 60], 200 steps.

**Physiological plausibility of τ.** For Equation 1 the effective time constant is −1/ln(1 − τ) steps: 7.89 steps for τ = 0.119, that is 7.9 ms at dt = 1 ms. v1.0 gave 8.4 ms from 1/τ and called it the centre of the range; the midpoint of 5–20 ms is 12.5 ms. The value τ = 0.119 is the default LTC setting, not fitted to data. Amplification is robust for τ ∈ [0.05, 0.2] (effective constants from 19.5 to 4.5 ms) and degrades at τ = 0.3 (2.8 ms). The 5–20 ms range for *Drosophila* central neurons is retained from v1.0 with its citation [Gouwens & Wilson, 2009], whose values were not re-read for this version (Section 5).

**Note on LIF-hard.** The LIF-hard model produces binary spike vectors (0 or 1). Because motor-neuron spikes are extremely sparse at any given time step, the activation vectors used for cosine RDI are frequently null (‖*v*‖ = 0), producing a division by zero in the cosine similarity. These cases are reported as "indef.". This limitation is intrinsic to the point-process nature of spiking models evaluated with instantaneous vector metrics: it indicates metric incompatibility, not model failure. Temporal amplification is therefore validated across three compatible models (SparseLTC, Linear, LIF-soft), and LIF-hard is reported as metric-incompatible rather than omitted. The abstract of v1.0 counted four models (Erratum, item 7).

## 2.6 Metrics

Cosine RDI, Net RDI and GABAergic cancellation are defined in the Supplementary Material. For multi-hop access (Section 3.4), **reach** *R*~1~ and *R*~2~ is the number of distinct motor neurons receiving a directed path of length exactly one or two from the class, and **path count** *P*~2~ is the number of two-hop paths into the motor population: the sum over intermediate neurons *v* of (connections from the class into *v*) × (connections from *v* into the motor population).

## 2.7 Statistics

Primary metrics: Δ (real − control), *p*~perm~ (fraction of controls ≥ real) and bootstrap confidence intervals (10,000 iterations). Z-scores are in the Supplementary Material. For Table 5, *p*-values are binomial, with a per-pair probability equal to density × *P*(excitatory), the same quantity that enters the expected count.

**Note on Z-score magnitude.** Some Z-scores exceed 100σ. This reflects the extremely low inter-control variance of the Maslov–Sneppen null, which converges to a narrow distribution as modularity is destroyed, not implausible effect sizes. Δ, *p*~perm~ and bootstrap intervals are the statistics for interpretation; Z-scores are given for completeness and for comparison with the community-preserving null, which has higher variance.

# 3 Results

## 3.1 Active intermodal isolation

Table 2: Contralateral suppression (Visual L → Visual R, 1 hop).

| Component | Ipsilateral | Contralateral |
|---|---|---|
| Excitation | +2,903,970 | +166,770 |
| Inhibition | −613,364 | −228,373 |
| Net flux | +2,290,606 | −61,603 |
| Cancellation | 0.21 | 1.37 |

Contralateral inhibition exceeds excitation by a factor of 1.37. Interhemispheric isolation is an active mechanism of directed inhibition, consistent with the inhibitory commissure between optic lobes.

## 3.2 Differential motor access

Table 3: Net RDI, modality → motor output (*N* = 100 MS controls).

| Population | *N* | Δ | *p*~perm~ | Bootstrap 95% CI of *Z* |
|---|---|---|---|---|
| Somatosensory | 3,067 | +0.365 | < 0.01 | [+147, +318] |
| Mechanosensory | 2,659 | +0.495 | < 0.01 | [+205, +325] |
| Gustatory | 408 | +0.024 | < 0.01 | [+3, +7] |
| Visual L | 43,056 | −0.018 | 1.000 | — |
| Olfactory | 2,279 | −0.046 | 1.000 | — |

None of the 100 controls equals or exceeds the real value for the somatosensory populations; all 100 exceed it for visual and olfactory. Canonical gustatory neurons alone (*N* = 408) produce significant motor privilege at α = 0.01 against MS controls, consistent with direct topological support for the PER [Shiu et al., 2024].

Table 4: Excitatory flux decomposition, somatosensory → motor output.

| Component | *N* | Excitatory flux to motor output | Share | *Z* |
|---|---|---|---|---|
| Mechanosensory | 2,659 | 85,821 | 95.2% | +245σ |
| Gustatory | 408 | 4,281 | 4.8% | +4.4σ |
| Total | 3,067 | 90,102 | | |

v1.0 printed the total as 90,101; the components sum to 90,102.

These comparisons are against the Maslov–Sneppen ensemble, which preserves degree but not anatomy. Section 3.4 shows that, for multi-hop access to the brain motor neurons, the modality ordering found against degree-preserving nulls is explained by neuropil co-location. Net RDI against a neuropil-preserving null was not computed.

## 3.3 Motor access against uniform density and against degree

Table 5 compares, for each sensory class, the observed excitatory connections into the motor output population with the expectation *N*~class~ × *N*~motor~ × density × *P*(excitatory), where *N*~motor~ = 1,485 and *P*(excitatory) = 0.600272 is the fraction of connections that are excitatory. v1.0 described this as a "density expectation" without stating the excitatory factor, and computed it with the overflowed density; the observed counts are unchanged. Verdicts: enriched if ratio > 2 and *p* < 0.001; depleted if ratio < 0.5 and *p* < 0.001; within expectation if 0.5 ≤ ratio ≤ 2.

Table 5: Excitatory connections from each sensory class to the motor output population, against uniform density (v1.0 and v2.0) and against a degree-preserving null (40 realizations).

| Class | *N* | Obs. | Exp. | v1.0 | v2.0 | *p* | Verdict | Degree null |
|---|---|---|---|---|---|---|---|---|
| mechanosensory | 2,656 | 23,010 | 1,859.0 | 1.3× | **12.38×** | < 10^−300^ | enriched | 9.69× |
| unknown sensory | 131 | 1,179 | 91.7 | 1.4× | **12.86×** | < 10^−300^ | enriched | 6.71× |
| gustatory | 408 | 1,280 | 285.6 | 0.5× | **4.48×** | < 10^−300^ | enriched | 2.19× |
| thermosensory | 29 | 14 | 20.3 | 0.07× | **0.69×** | 0.094 | within expectation | 0.236× |
| hygrosensory | 74 | 13 | 51.8 | 0.03× | 0.25× | 1.3 × 10^−10^ | depleted | 0.103× |
| olfactory | 2,279 | 80 | 1,595.1 | 0.005× | 0.050× | < 10^−300^ | depleted | 0.034× |
| visual optic | 77,530 | 1,679 | 54,265 | 0.003× | 0.031× | < 10^−300^ | depleted | not tested |
| visual | 10,855 | 137 | 7,597.7 | 0.002× | 0.018× | < 10^−300^ | depleted | 0.145× |
| ascending (AN), *N* = 495 in v1.0 | | | | 0.6× | not reproducible | | | |

**Corrected summary.** Over the eight reproducible rows, three classes are enriched, one is within expectation and four are depleted. v1.0 reported "zero classes enriched, seven classes depleted"; that statement and the interpretation built on it (v1.0 Section 4.2, "the topology concentrates, not adds") are withdrawn. So is the paradox discussed in v1.0 Section 3.3, in which gustatory neurons were said to have half the expected motor connections and yet to outperform MS controls: with the corrected expectation they have 4.5 times the connections a uniform graph would give them. The v1.0 row for ascending neurons (*N* = 495) matches no filter consistent with the other rows and is declared not reproducible rather than corrected. The full population carrying `cell_class` = AN, 2,231 neurons in the graph, gives 17.84× against uniform density; it is not the population of the published row.

**Against degree.** Against 40 nulls preserving in-degree and out-degree exactly, the sign of every tested class is the same as against uniform density (8 of 8 classes, and no null out of 40 reaching the observed value in any class), and olfactory (0.034×) rather than visual (0.145×) becomes the most depleted class. The eight tested classes are the reproducible rows other than visual optic, plus the full AN population (7.41× against the degree null). Over those eight classes the spread between extremes is 991-fold against uniform density (AN 17.84× over visual 0.018×; 989-fold from unrounded ratios) and 283-fold against the degree-preserving null. Over the eight reproducible rows of Table 5 the uniform-density spread is 713-fold.

**Against modularity, untestable.** Under the CP null this count is conserved by construction, because the motor output group is itself defined by super-class: across 40 realizations the standard deviation is exactly zero and every null equals the observed value. The ordering of Table 5 therefore exceeds what the degree sequence explains, but this quantity cannot decide whether it exceeds what anatomy explains. Section 3.4 addresses that question for the brain motor neurons with a neuropil-preserving null, and there the ordering does not survive.

## 3.4 Multi-hop motor access under an anatomical null (new in v2.0)

**Methods.** Brain motor neurons were defined as `super_class` = motor, yielding 110 neurons, all present in the connectivity graph (109 above the five-synapse threshold). The population is nested: 105 carry `cell_class` = brain_motor_neuron, one is annotated neck_motor_neuron and four carry no `cell_class`; all statistics were computed for both definitions and no conclusion depends on the choice. Nine carry `status` = outlier_seg and were retained. Their efferent nerves are the pharyngeal (40), maxillary-labial (26), cervical connective (20), antennal (14) and occipital (10). Reach and path count (Section 2.6) were computed per sensory class without threshold and under the five-synapse threshold. The threshold is not cosmetic here: without it *R*~2~ is unusable, because every null realization reaches the entire motor population and the ensemble standard deviation is exactly zero; under the threshold it is 1.04 and the statistic becomes estimable.

Two target-permutation ensembles were used, and the comparison between them is the result. The **degree-preserving** ensemble permutes the vector of connection targets while holding sources fixed, preserving every out-degree by construction and every in-degree exactly, since the multiset of targets is conserved; it admits self-loops (317 without threshold, against 0 observed) and repeated connections. The **neuropil-preserving** ensemble permutes targets only within groups of connections sharing the same ordered pair (source neuropil, target neuropil), preserving the number of connections between every ordered pair of neuropils in addition to out-degree. It belongs to the same family as the NPC model of Lin et al. [2024]; it differs in assigning each neuron a single dominant neuropil rather than assigning individual synapses, and it preserves in-degree only within blocks. Neuropil assignments are the per-neuron neuropil synapse counts of the FlyWire 783 release [FlyWire Consortium, 2024], giving 79 labels; 283 of 138,639 neurons lack an output assignment and 495 lack an input assignment, and these fall into an explicit unassigned block rather than being discarded. Forty realizations per family, seeds 1000 + 7*i*.

Degree preservation was verified against a positive and a negative control: the permutation reproduces the observed in-degree vector exactly, whereas drawing targets uniformly breaks it for 138,142 of 138,639 neurons. A quantity conserved by construction was measured inside the same run: 19,860 connections enter the motor population in the observed graph and in all forty realizations, with standard deviation zero, which establishes that the statistics of interest do not behave that way. A size-matched arbitrary control of 10,855 randomly drawn neurons gives the ensemble baseline for each family.

**Results.** Against the degree-preserving ensemble the four sensory classes differ enormously in two-hop access to brain motor neurons (Table 5b): olfactory and visual afferents fall far below expectation, mechanosensory and gustatory far above it, and the ratio between extremes is 323. Direct access shows the same ordering: olfactory and visual reach no motor neuron at all, against 71.3 ± 4.6 and 52.3 ± 5.2 expected.

Table 5b: Two-hop path count *P*~2~ into the 110 brain motor neurons, as observed over null mean, without threshold (40 realizations per ensemble; in parentheses, *z* and the number of realizations at or above the observed value).

| Class | *N* | Observed *P*~2~ | Degree null | Neuropil null | Sign |
|---|---|---|---|---|---|
| Olfactory | 2,279 | 901 | 0.023 (−51.8; 40/40) | 0.368 (−4.4; 40/40) | unchanged, 16-fold weaker |
| Visual | 10,855 | 1,413 | 0.061 (−54.0; 40/40) | **1.531** (+4.1; 0/40) | **inverted** |
| Mechanosensory | 2,656 | 293,022 | 7.36 (+342; 0/40) | **0.803** (−20.6; 40/40) | **inverted** |
| Gustatory | 408 | 67,439 | 6.54 (+249; 0/40) | **0.632** (−37.2; 40/40) | **inverted** |
| Arbitrary control | 10,855 | 312,457 | 0.652 | **1.010** | baseline offset absorbed |

That entire pattern is accounted for by anatomy. Under the neuropil-preserving ensemble the ordering inverts, and the same inversion holds under the five-synapse threshold (olfactory 0.121, visual 4.87, mechanosensory 0.974 and no longer significant at 38 of 40, gustatory 0.376). The 323-fold spread collapses to 2.4-fold, and the 0.652 baseline of the arbitrary control, which under a degree-preserving ensemble looks like a global property of the connectome, becomes 1.010: it was the effect of connections respecting neuropil boundaries.

The mechanism is directly measurable. Taking each neuron's dominant neuropil by presynaptic site count, 104 of the 110 brain motor neurons lie in the gnathal ganglion (GNG) or the prow (PRW), and so do mechanosensory afferents (GNG 1,712; SAD 468) and gustatory afferents (GNG 353; PRW 52). Olfactory afferents lie in the antennal lobes (AL 2,276) and visual afferents in the lamina and medulla (LA 8,086; ME 2,622). Two of the four classes share an address with the motor population and two do not; no further explanation of the degree-null ordering is required. This is the neuropil-scale counterpart of the observation of Bates et al. [2026] that effector neurons are primarily influenced by sensory neurons of the same body part.

Once co-location is controlled for, the informative result is the opposite of the one the degree-preserving ensemble suggests (Table 5c).

Table 5c: Direct motor access *R*~1~ (distinct brain motor neurons contacted) against the neuropil-preserving ensemble, without threshold.

| Class | Observed *R*~1~ | Neuropil null | *z* | Realizations ≥ observed |
|---|---|---|---|---|
| Gustatory | **10** | 101.6 ± 1.2 | **−78.9** | 40/40 |
| Mechanosensory | **64** | 98.6 ± 1.6 | **−21.7** | 40/40 |
| Olfactory | 0 | 1.0 ± 0.9 | −1.2 | 40/40 |
| Visual | 0 | 0.03 ± 0.16 | −0.2 | 40/40 |

Under the five-synapse threshold the contrast sharpens: gustatory afferents contact 2 motor neurons where co-location predicts 91.0, mechanosensory 33 where it predicts 89.2, and the ensemble predicts exactly 0.0 for olfactory and visual.

Two conclusions follow. First, the absence of olfactory and visual connections onto brain motor neurons is predicted by the anatomy and carries no additional information: for these two classes the neuropil-preserving ensemble reproduces the observed value, so the statistic is not testable against it, and an interpretation of the zero as a structural exclusion is not supported. Second, the classes that do share a neuropil with the motor population are strongly depleted relative to that co-location: gustatory afferents make an order of magnitude fewer direct motor contacts than proximity predicts. Access is restricted even where geometry permits it, and that restriction, unlike the modality ordering, survives the strongest control used here. At the circuit level this agrees with prior work: PER motor neurons do not appear to receive direct input from gustatory receptor neurons [Gordon & Scott, 2009], and the sugar PER pathway runs through three intermediate layers [Shiu et al., 2022]. The contribution here is the quantification against an anatomical null across four modalities, not the observation that taste reaches motor neurons through interneurons.

## 3.5 Synaptic depth profiles (*N* = 20 MS controls)

Table 6: GABAergic cancellation by depth.

| Population | 1 hop | 2 hops | 3 hops | Profile |
|---|---|---|---|---|
| Mechanosensory | 0.04% | 135% | 953% | reflex + strong containment |
| Gustatory | 0.05% | 73% | 704% | reflex + gradual containment |
| Olfactory | 0.00% | 8.7% | 10.7% | free propagation |
| Visual L | 12.1% | 40% | 496% | progressive blocking |

At 1 hop no profile differs significantly from control (|*Z*| < 2); at 2 and 3 hops all differ significantly (|*Z*| > 3). Gustatory has a profile intermediate between mechanosensory and olfactory: little cancellation at 1 hop, like mechanosensory, but more gradual containment (73% against 135% at 2 hops). This is coherent with the PER: an immediate reflex with contextual modulation (hunger state, gustatory valence). These profiles are against MS controls and were not tested against the neuropil-preserving ensemble.

## 3.6 Connectome reciprocity

Across all 15,091,983 connections, 26.60% participate in reciprocal pairs (4,014,518 reciprocal connections). Against 40 realizations preserving in-degree, out-degree and community block structure, the observed value ranks first of 41 (20.59× the ensemble mean; none of the 40 reaches it); against the Maslov–Sneppen ensemble the ratio is 47.27×. v1.0 reported "36× over density expectation"; that quotient used the overflowed density and is withdrawn. With the corrected density it would be 338.8×; quotients against uniform density are the weakest available comparison and are given for continuity only.

**The global magnitude is threshold-dependent and not distinctive.** Under the five-synapse criterion reciprocity is 13.98% (2,700,513 connections, 377,448 reciprocal), close to the 13.8% reported by Lin et al. [2024] for snapshot v630, and mean synapses per connection is 12.647 against the 12.6 reported by Dorkenwald et al. [2024] (Table S2). Lin et al. [2024] also find reciprocity and clustering comparable across five nervous systems, and describe the over-representation of reciprocal connections in brains as well established. We therefore claim the excess only against randomized controls, not as a property that distinguishes this connectome.

**Resolved over directed pairs of functional cell classes** (Table 7), reciprocity spans more than an order of magnitude under both criteria. Lin et al. [2024] already resolve reciprocity anatomically: within each of 78 neuropils (their Fig. 5c), normalised by connection density per neuropil (their Extended Data Fig. 6c) and as a map of reciprocal pairs between neuropils (their Fig. 5h). We claim no novelty for decomposing reciprocity. The axis used here, functional class pairs along the sensory-to-motor direction, is complementary to theirs, and the two sets of values have not been compared region by region.

Table 7: Reciprocity by circuit type: fraction of connections from class A to class B whose reverse connection exists in the same graph, without threshold and under the five-synapse threshold (pinned annotations; connections, with reciprocal ones in parentheses).

| Circuit | No threshold | Connections | ≥ 5 synapses | Connections |
|---|---|---|---|---|
| Intra-motor | 41.3% | 509 (210) | 35.0% | 80 (28) |
| Intra-visual centrifugal | 36.9% | 7,490 (2,764) | 23.4% | 1,324 (310) |
| Intra-optic | 32.0% | 6,201,390 (1,983,172) | 17.1% | 1,069,721 (183,060) |
| Intra-sensory | 30.7% | 34,107 (10,460) | 37.5% | 1,287 (482) |
| Sensory → central | 24.2% | 159,316 (38,549) | 13.8% | 33,497 (4,609) |
| Sensory → descending | 8.6% | 24,326 (2,104) | 2.8% | 4,786 (136) |
| Sensory → motor | 3.6% | 1,178 (42) | 1.3% | 373 (5) |
| Optic → motor | 0.0% | 6 (0) | undefined | 0 |
| Whole connectome | 26.60% | 15,091,983 (4,014,518) | 13.98% | 2,700,513 (377,448) |

v1.0 printed sensory → descending as 8.7%, a double rounding of 8.649% (to 8.65, then to 8.7); the value is 8.6%. The other seven values of v1.0 reproduce at one decimal with both the March and the pinned annotations. Under the threshold, optic → motor has no connections and its reciprocity is undefined.

Along the rows that originate in sensory neurons, reciprocity declines toward the output under both criteria (without threshold 30.7, 24.2, 8.6 and 3.6%; under the five-synapse threshold 37.5, 13.8, 2.8 and 1.3%). **This ordering is reported descriptively.** A per-circuit comparison against the community-preserving null was run; its preliminary reading is that the null reproduces the decline, but the instrument failed its own negative control and no conclusion is drawn in either direction. The intra-class rows depend on the criterion: intra-motor is highest without a threshold (41.3%) and intra-sensory under it (37.5%), and intra-motor under the threshold rests on 80 connections. The CP null destroys reciprocity by shuffling targets, which is consistent with, but does not isolate, a contribution of reciprocity to the post-stimulus amplification of Section 3.7.

## 3.7 Non-trivial temporal amplification

Table 8: Cosine RDI, Real against CP and MS.

| Step | Phase | Real | CP | *Z*~CP~ | MS | *Z*~MS~ |
|---|---|---|---|---|---|---|
| 15 | During | 0.687 | 0.711 | −24.8 | 0.653 | +40.3 |
| 60 | End of stimulus | 0.630 | 0.663 | −10.6 | 0.469 | +97.1 |
| 80 | Post + 20 | 0.680 | 0.526 | +29.5 | 0.111 | +230 |
| 120 | Post + 60 | 0.807 | 0.368 | +18.4 | 0.004 | +923 |
| 195 | Post + 135 | 0.833 | 0.299 | +14.8 | 0.001 | +2842 |

Quotients derived from Table 8 beyond *t* = 120 approach the numerical floor of the controls and are not interpretable; the series should be quoted side by side. The script that produced Table 8 is not in the archived code, and its values have not been reproduced (Section 5).

Temporal dissociation of two mechanisms. *During stimulus*, separation is modular: CP ≥ Real, so community structure suffices. *Z*~CP~ is negative, indicating that the CP null separates slightly better, likely from a more uniform signal distribution within each community. *Post-stimulus*, amplification requires fine wiring: Real rises from 0.63 to 0.83 (+32%) while CP falls from 0.66 to 0.30 (−55%). The difference (*Z*~CP~ = +14.8σ) shows that generic modularity is insufficient. The CP null destroys reciprocity, recurrent motifs and the placement of individual weights together, so which of these sustains post-stimulus separation was not isolated.

Table 9: Cosine RDI by neural model.

| Step | SparseLTC | Linear | LIF-soft | LIF-hard |
|---|---|---|---|---|
| 60 | 0.630 | 0.623 | 0.253 | indef. |
| 180 | 0.832 | 0.835 | 0.002 | indef. |

LIF-hard: null motor vectors at the sampled time steps produce a division by zero in the cosine similarity (Section 2.5). SparseLTC ≈ Linear: the dynamics are quasi-linear, and in this regime the eigenvalue spectrum of *W* governs the amplification.

Table 10: Amplification by τ. The effective time constant is −1/ln(1 − τ) at dt = 1 ms; v1.0 listed 1/τ.

| τ | Effective constant | v1.0 | RDI~60~ | RDI~180~ | Δ |
|---|---|---|---|---|---|
| 0.05 | 19.5 ms | 20 ms | 0.637 | 0.783 | +0.146 |
| 0.119 | 7.9 ms | 8.4 ms | 0.630 | 0.832 | +0.201 |
| 0.2 | 4.5 ms | 5 ms | 0.632 | 0.825 | +0.193 |
| 0.3 | 2.8 ms | 3.3 ms | 0.632 | 0.644 | +0.011 |

The functional range τ ∈ [0.05, 0.2] corresponds to effective constants from 4.5 to 19.5 ms. Degradation at τ = 0.3 corresponds to 2.8 ms, below the 5–20 ms range.

# 4 Discussion

## 4.1 Three properties with their qualifications

**Property 1, intermodal isolation.** During-stimulus separation is modular (CP ≈ Real). Post-stimulus amplification is non-trivial (*Z*~CP~ = +14.8σ). Contralateral inhibition is active (cancellation 1.37).

**Property 2, differential motor access.** Against degree-preserving controls, canonical gustatory neurons alone give *Z* = +4.5σ, *p* < 0.01 (*N* = 100), and mechanosensory neurons dominate the flux (95.2%). Against uniform density, three classes are enriched and four depleted. Against a neuropil-preserving null the modality ordering of two-hop access inverts: it reflects where afferents terminate relative to the motor neuropil. The property that survives anatomy is restriction: afferents that share a neuropil with the motor neurons contact far fewer of them directly than co-location predicts.

**Property 3, non-trivial amplification.** It requires fine wiring (*Z*~CP~ = +14.8σ) and graded dynamics, in a quasi-linear regime, with a physiologically plausible τ. Reciprocity is elevated against nulls (20.59× against the CP ensemble) and is a candidate substrate for reverberation, not an isolated cause.

## 4.2 Motor access: co-location first, restriction within it

v1.0 read the density analysis as "the topology concentrates existing connections rather than adding them". With the corrected density that reading has no support: three classes have more direct access to the motor output than a uniform graph would give them. The degree-null comparison suggested instead a hierarchy aligned with behavioural urgency, in which pathways that must reach muscle within milliseconds are enriched and pathways that must first build a scene or an odour identity are depleted. The neuropil-preserving null shows that, at least for the brain motor neurons, this ordering is the anatomy: mechanosensory and gustatory afferents terminate in the gnathal ganglion and the prow, where 104 of the 110 brain motor neurons have their dominant output, while olfactory and visual afferents terminate in the antennal lobes and the optic lobes. The urgency reading is therefore not supported as a wiring principle beyond co-location.

What the anatomical control leaves standing is the opposite of privilege: within the shared neuropil, direct sensory-to-motor contacts are an order of magnitude rarer than proximity predicts. This is consistent with sensorimotor transformations being routed through interneurons [Gordon & Scott, 2009; Shiu et al., 2022], and with the observation of Bates et al. [2026] that effector neurons are principally influenced by sensory neurons of the same body part. For the motor output population of Table 5, which is mostly descending, the neuropil-preserving null was not run.

## 4.3 Neurophysiological consistency

- **Mechanosensory** (reflex + strong containment): consistent with the role of mechanosensory feedback in motor control [Tuthill & Wilson, 2016], although direct contacts onto brain motor neurons are fewer than co-location predicts (Section 3.4).
- **Gustatory** (reflex + gradual containment): PER with contextual modulation, through intermediate layers [Shiu et al., 2022].
- **Olfactory** (free propagation): consistent with olfactory signals travelling toward higher centres rather than to motor output.
- **Visual** (progressive blocking): hierarchical medulla and lobula processing.
- **Intra-motor reciprocity** (41.3% without threshold; 35.0% under it, over 80 connections): high, on a small population; its functional role is not addressed here.

## 4.4 Comparison with concurrent work

Table 11: Comparison with concurrent studies. The studies address complementary questions with different models and analytical frameworks.

| | Shiu | Betzel | This work |
|---|---|---|---|
| Null model | No | Community only | MS + CP (*N* = 100), degree and neuropil ensembles (*N* = 40) |
| Gustatory / mechanosensory decomposition | No | No | Yes |
| Density analysis | No | No | Yes |
| Depth profiles | No | No | Yes (*N* = 20) |
| Modular / fine dissociation | No | No | Yes |
| Reciprocity | No | No | Yes, by functional class pair |

Shiu et al. [2024] focused on demonstrating functional sensorimotor propagation with a LIF model. Betzel et al. [2026] used a cooperative spreading model to characterize cascade convergence onto integration hubs. Two further works overlap with this one and are not tabulated, because the comparison would require reading their results row by row. Lin et al. [2024] resolve reciprocity by neuropil and constrain random graphs by neuropil connectivity, so the reciprocity row above establishes no priority. Bates et al. [2026] apply a linear signal-propagation model with input-fraction normalization to the brain-and-cord connectome, validating this class of method at whole-nervous-system scale (*R*^2^ = 0.94 over 94,278 pairs on FAFB v783), with a steady-state, unsigned influence measure. The contributions retained here are those such a measure does not express: signed propagation with per-neuron excitatory or inhibitory identity, transient post-stimulus dynamics, depth-dependent inhibitory cancellation, reciprocity resolved by functional class pair, and multi-hop motor access tested against an anatomical null.

## 4.5 Implications

**The SparseLTC ≈ Linear equivalence** implies that amplification can be analysed spectrally: the dominant eigenvalues of *W* within each module set the reverberation rate. **Depth profiles** encode permeability gradients per modality, information richer than binary modularity. **Co-location with restriction** suggests that motor access is organised in two layers: anatomy decides which afferents can reach the motor neuropil, and wiring within it limits direct contacts.

## 4.6 Implications for bio-inspired AI and edge computing

The following are design hypotheses suggested by the results, not results:

1. **Isolation via directed inhibition** (cancellation > 1.0) as a wiring principle for crosstalk suppression in multi-sensor fusion architectures.
2. **Co-location with restricted direct access** as a template for sparse sensor-to-actuator routing through intermediate layers.
3. **Persistence without trained recurrence.** Recurrent motifs at biologically observed densities sustained post-stimulus separation without trained recurrent weights in these simulations; whether this reduces parameter counts in a deployed system was not measured.
4. **Hardware without nonlinear activations.** The quasi-linear regime (SparseLTC ≈ Linear) suggests that such topologies could run on hardware lacking nonlinear activation support (FPGAs, analog neuromorphic chips); this was not tested on hardware.

# 5 Limitations

1. **Single modular null with variance.** The CP null is the only control preserving modular structure with variance in temporal metrics. Nulls preserving intra-modular reciprocity (26.6% of connections) would be more restrictive.
2. ***N* = 5 for temporal CP.** Sufficient for *Z* = +14.8σ, but tighter intervals would require *N* ≥ 20.
3. **Model dependence.** Only graded models replicate amplification, and LIF-hard is metric-incompatible. Amplification is not a purely topological property.
4. **Independence in the density analysis.** The binomial test assumes independent connections. Degree correlations could affect *p*-values, though not observed/expected ratios.
5. **Table 8 is not reproducible from the archived code.** Four candidate partitions of the activation vector were tested against the published definition and none reproduces the trajectory; the script that produced Table 8 is not in the archive. Its values are reported as in v1.0.
6. **Two items of Table 5 are unresolved.** The AN row of v1.0 (*N* = 495) matches no consistent filter, and the tenth class declared in Section 2.3 has not been identified.
7. **The neuropil-preserving ensemble approximates the NPC model** of Lin et al. [2024]: one dominant neuropil per neuron rather than per-synapse assignment, in-degree preserved within blocks only, no combined degree-and-neuropil ensemble, no distance-based (NND) ensemble, and block purity not measured.
8. **Statistic-level limits of Section 3.4.** Path counts ignore synaptic sign and weight and do not exclude routes through another motor neuron; paths of length three and above were not examined; the arbitrary control is matched on neuron count, not out-degree; the nine outlier_seg motor neurons are retained without measuring their effect.
9. **The target population is not muscle.** Brain motor neurons innervate head structures; leg, wing, haltere and abdominal motor neurons reside in the ventral nerve cord, absent from this dataset. A brain-and-cord connectome [Bates et al., 2026] is the substrate for extending the analysis to locomotor output.
10. **Results against the Maslov–Sneppen null were not retested against anatomy.** The modality ordering of Sections 3.2 and 3.5 may share the co-location explanation of Section 3.4.
11. **Reciprocity by circuit type is descriptive.** The per-circuit null failed its negative control; the values of Lin et al. [2024] by neuropil were not compared region by region; whether Lin et al. apply the threshold exactly as here was not checked against their Methods.
12. **The physiological range for τ** (5–20 ms) is retained from v1.0 with its citation; the cited paper reports passive properties of antennal-lobe projection neurons, and its values were not re-read for this version.
13. **No synapse threshold by default.** The field standard is five synapses; threshold dependence is reported for reciprocity, Table 7 and Section 3.4 only.

# 6 Conclusions

1. **Intermodal isolation:** during-stimulus separation is modular; post-stimulus amplification requires specific wiring (*Z*~CP~ = +14.8σ).
2. **Differential motor access:** present against degree-preserving controls, but its modality ordering is set by neuropil co-location. What survives the anatomical null is a restriction of direct sensory-to-motor contacts within the shared neuropil (gustatory afferents reach 10 brain motor neurons against 101.6 predicted).
3. **Non-trivial temporal amplification:** quasi-linear regime and an effective time constant of 7.9 ms, with reciprocity elevated against nulls (20.59× against the CP ensemble) as a candidate substrate.

**Central finding.** The temporal dissociation, modular during stimulus and specific post-stimulus, shows two levels of computational information encoded in the topology: modularity produces separation; fine wiring produces persistence. For motor access, anatomy decides which modalities can reach the motor neurons, and wiring restricts how directly they do.

# 7 Data availability

Connectome: FlyWire v783 [Dorkenwald et al., 2024; FlyWire Consortium, 2024]; annotations from Schlegel et al. [2024], pinned as in Section 2.1. The processed connectivity matrix in .parquet format was obtained from the public repository maintained by Eon Systems PBC (https://github.com/eonsystems). Analysis code, verification scripts, raw logs and the source of this manuscript: https://github.com/gatehot59-star/drosophila-fep-connectome (v1.0 gave an address that never existed; Erratum, item 8). Licences: analysis code under GPLv3; the embedded inference engine and the network topologies under GPLv3 or a commercial licence (see LICENSE in the repository); this text and the numerical results under CC BY 4.0. Zenodo concept DOI: 10.5281/zenodo.19136947.

# 8 Conflict of interest

The author declares no competing interests. The embedded inference engine and network topologies in the companion repository are offered under GPLv3 or a commercial licence.

# 9 Acknowledgments

Parts of the computational implementation were developed with assistance from large language models. All algorithmic design, theoretical framework, experimental design and validation were performed by the author.

# Changes from version 1.0

Item numbers in brackets refer to the accompanying erratum.

1. Graph density corrected from 0.0074 to 7.85197 × 10^−4^; the error was a 32-bit integer overflow [1].
2. Table 5 recomputed with the corrected density and the stated excitatory factor: three classes enriched, four depleted, one within expectation; the AN row is not reproducible; binomial *p*-values recomputed with the same expectation; degree-null column added; Sections 3.3 and 4.2 rewritten; the reading "concentrates, not adds" and the gustatory paradox withdrawn [2, 6].
3. New Section 3.4 with Tables 5b and 5c: multi-hop access to brain motor neurons under degree- and neuropil-preserving ensembles, with prior circuit-level work cited.
4. Reciprocity: "36× over density expectation" withdrawn and replaced by ranks against CP (20.59×, 0 of 40) and MS (47.27×) ensembles; threshold dependence and agreement with Lin et al. (2024) reported; no claim that the global magnitude is distinctive; Table 7 extended with counts and the five-synapse column; sensory → descending corrected from 8.7 to 8.6; the ordering toward the output reported as descriptive [3, 5, 6].
5. Counts: Table 4 total corrected from 90,101 to 90,102; nine density classes reported against ten declared; depleted counts made consistent [6].
6. Models: "four parameter-free neural models" replaced by three compatible models, with LIF-hard reported as metric-incompatible [7].
7. τ: effective constant −1/ln(1 − τ) = 7.89 steps (7.9 ms), not 8.4 ms and not the centre of the range; Table 10 column updated; τ = 0.3 lies below the range, not at its limit [7].
8. The "Motor" population renamed motor output, with its composition stated (1,299 descending, 110 motor, 76 endocrine).
9. Swap acceptance stated as measured, 98.5%; v1.0 stated 100% [8].
10. Community-preserving null: claim of methodological novelty removed; same family as the NPC model of Lin et al. (2024).
11. Data availability: repository address corrected, DOI placeholder replaced, licences updated, inputs pinned by commit and md5 [8].
12. References added: Lin et al. 2024, Bates et al. 2026, FlyWire Consortium 2024, Gordon & Scott 2009, Shiu et al. 2022. References corrected: Gouwens & Wilson 2009, Tuthill & Wilson 2016, Hasani et al. 2022 and Schlegel et al. 2024. Nagel & Wilson 2011 removed, because it does not concern the statement for which it was cited [8].
13. Wording: Section 3.5 "direct access at 1 hop" replaced by "little cancellation at 1 hop"; Section 3.7 no longer attributes the post-stimulus mechanism to reciprocity specifically; Section 4.6 restated as design hypotheses; quotients from Table 8 beyond *t* = 120 flagged [4].
14. Limitations expanded from four to thirteen items.

# Supplementary material

Table S1: Z-scores and bootstrap confidence intervals (*N* = 100 MS).

| Metric | Real | Control mean | *Z* | Bootstrap 95% |
|---|---|---|---|---|
| Net RDI, somatosensory | −0.587 | −0.952 | +183 | [+147, +318] |
| Net RDI, mechanosensory | −0.456 | −0.951 | +248 | [+205, +325] |
| Net RDI, gustatory | −0.929 | −0.953 | +4.5 | [+3, +7] |
| Cosine RDI at *t* = 195 (against CP) | 0.833 | 0.299 | +14.8 | — |

Z-scores reflect low inter-control variance (Section 2.7). Bootstrap intervals confirm effect stability; Δ, *p*~perm~ and ratios are the primary metrics.

Table S2: Reciprocity and connection probability by inclusion criterion, on the matrix used throughout.

| Inclusion criterion | Connections | Reciprocity | Connection probability |
|---|---|---|---|
| No threshold (as in v1.0) | 15,091,983 | 26.60% | 7.85197 × 10^−4^ |
| ≥ 2 synapses | 7,595,967 | 19.21% | 3.95199 × 10^−4^ |
| ≥ 3 synapses | 4,916,231 | 16.45% | 2.55779 × 10^−4^ |
| ≥ 5 synapses (field standard) | 2,700,513 | 13.98% | 1.40501 × 10^−4^ |
| ≥ 10 synapses | 1,066,822 | 11.53% | 5.5504 × 10^−5^ |

Under the five-synapse criterion, reciprocity is 13.98% against the 13.8% reported by Lin et al. [2024] for v630, mean synapses per connection 12.647 against 12.6 [Dorkenwald et al., 2024], and connection probability 1.405 × 10^−4^ against 1.61 × 10^−4^, a difference attributable to the reconstruction version (v783 here, v630 there).

**Metric definitions.**

*Cosine RDI.* Let *v*~A~(*t*) and *v*~B~(*t*) be the motor-neuron activation vectors produced by stimulating populations A and B. Then

$$\mathrm{RDI}_{\cos}(t) = 1 - \frac{v_A(t) \cdot v_B(t)}{\|v_A(t)\| \, \|v_B(t)\|}$$

*Net RDI.* For a population *P* stimulating the motor population *M*:

$$\mathrm{RDI}_{\mathrm{net}} = \frac{\sum_{i \in P, j \in M} W_{ij}}{\sum_{i \in P, j} |W_{ij}|} - 1$$

*GABAergic cancellation.* At depth *d*, *C*~d~ = |Inhibition~d~| / Excitation~d~. Values above 1 indicate net suppression; values below 1 indicate net excitation.

# References

Bates, A.S., Phelps, J.S., Kim, M., Yang, H.H., et al. (2026). Distributed control circuits across a brain-and-cord connectome. *Nature*, 656, 957–970. doi:10.1038/s41586-026-10735-w

Betzel, R.F., Puxeddu, M.G., Seguin, C. & Mišić, B. (2026). Cascades and convergence: Dynamic signal flow in a synapse-level brain network. *PLOS Complex Systems*, 3(3), e0000091. doi:10.1371/journal.pcsy.0000091

Costi, L., Hadjiivanov, A., Dold, D., Hale, Z.F. & Izzo, D. (2025). The *Drosophila* connectome as a computational reservoir for time-series prediction. *Biomimetics*, 10(5), 341. doi:10.3390/biomimetics10050341

Dorkenwald, S., Matsliah, A., et al. (2024). Neuronal wiring diagram of an adult brain. *Nature*, 634, 124–138.

FlyWire Consortium (2024). FlyWire Whole-brain Connectome Connectivity Data, version 783.0. Zenodo. doi:10.5281/zenodo.10676866

Gordon, M.D. & Scott, K. (2009). Motor control in a *Drosophila* taste circuit. *Neuron*, 61(3), 373–384.

Gouwens, N.W. & Wilson, R.I. (2009). Signal propagation in *Drosophila* central neurons. *Journal of Neuroscience*, 29(19), 6239–6249. doi:10.1523/JNEUROSCI.0764-09.2009

Hasani, R., Lechner, M., Amini, A., Liebenwein, L., Ray, A., Tschaikowski, M., Teschl, G. & Rus, D. (2022). Closed-form continuous-time neural networks. *Nature Machine Intelligence*, 4, 992–1003.

Jaeger, H. (2001). The "echo state" approach to analysing and training recurrent neural networks. GMD Report 148.

Jin, Z., Zhu, Y., Zhang, C. & Sui, Y. (2026). Whole-brain connectomic graph model enables whole-body locomotion control in fruit fly. arXiv:2602.17997.

Lin, A., Yang, R., et al. (2024). Network statistics of the whole-brain connectome of *Drosophila*. *Nature*, 634, 153–165.

Maslov, S. & Sneppen, K. (2002). Specificity and stability in topology of protein networks. *Science*, 296, 910–913.

Schlegel, P., et al. (2024). Whole-brain annotation and multi-connectome cell typing of *Drosophila*. *Nature*, 634, 139–152.

Shiu, P.K., et al. (2024). A *Drosophila* computational brain model reveals sensorimotor processing. *Nature*, 634, 210–219.

Shiu, P.K., Sterne, G.R., Engert, S., Dickson, B.J. & Scott, K. (2022). Taste quality and hunger interactions in a feeding sensorimotor circuit. *eLife*, 11, e79887. doi:10.7554/eLife.79887

Tuthill, J.C. & Wilson, R.I. (2016). Mechanosensation and adaptive motor control in insects. *Current Biology*, 26(20), R1022–R1038. doi:10.1016/j.cub.2016.06.070

Váša, F. & Mišić, B. (2022). Null models in network neuroscience. *Nature Reviews Neuroscience*, 23, 493–504.

Yu, S., Qin, Z., Liu, T., Xu, B., Vogelstein, R.J., Brown, J. & Vogelstein, J.T. (2026). Biological processing units: Leveraging an insect connectome to pioneer biofidelic neural architectures. In Iklé, M., Kolonin, A. & Bennett, M. (Eds.), *AGI 2025, Proceedings* (pp. 361–369). LNCS/LNAI 16058. Springer. doi:10.1007/978-3-032-00800-8_32
