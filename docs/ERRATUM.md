# Erratum to Mendieta (2026a)

Corrections to *Signal propagation properties in the Drosophila melanogaster
connectome*, Zenodo, March 2026. Seven items. Items 1 and 2 change reported values and one
qualitative conclusion; items 3 to 6 are factual corrections; item 7 adds a result that
version 1 under-reported, together with a reproducibility limitation found while verifying
it.

**No finding is retracted.** The corrections arise from an independent recomputation that
reproduced the manuscript's observed counts exactly and revealed that two expected-value
calculations used an incorrect baseline. In both cases the corrected result is more
specific than the original, and in one case (reciprocity) the original error understated
the effect.

A table of all corrected values appears at the end.

## 1. Graph density, and the enrichment table that depends on it

The expected-value calculations used a graph density of 0.00739526. The correct density of
the directed graph is:

> **d = 0.000785197**, from 15,091,983 unique directed edges over 138,639 x 138,638
> ordered node pairs.

The published value is 9.42 times too large. **The cause of the incorrect value has not
been established and no explanation is offered here.** One candidate explanation, that
synapse counts were substituted for connection counts, was tested and rejected: the
synapse total is 54,492,922, which does not reconcile with the published density.

Observed counts are unaffected. Expected values, and therefore the enrichment verdicts,
are:

| Sensory class | N | Observed excitatory edges to motor | Published ratio | Corrected ratio | Verdict change |
| --- | --- | --- | --- | --- | --- |
| visual | 10,855 | 137 | 0.0x | 0.018x | none |
| olfactory | 2,279 | 80 | 0.0x | 0.050x | none |
| hygrosensory | 74 | 13 | 0.0x | 0.251x | none |
| thermosensory | 29 | 14 | 0.1x | 0.690x | none |
| mechanosensory | 2,656 | 23,010 | 1.3x | **12.378x** | **yes** |
| gustatory | 408 | 1,280 | 0.5x (depleted) | **4.482x (enriched)** | **yes, sign reversed** |
| ascending (AN) | 2,231 | 27,857 | 0.6x | **17.839x** | **yes** |
| unknown sensory | 131 | 1,179 | 1.4x | **12.858x** | **yes** |

The summary line stating **"enriched = 0, depleted = 7"** is replaced by
**"enriched = 4, depleted = 4"**.

The same error affects reciprocity in the opposite direction, understating the reported
effect. Reciprocity is 26.60% (4,014,518 of 15,091,983 edges have a reciprocal partner).
Against the chance expectation implied by the corrected density this is **338.8x**, not
36x.

That figure should be reported alongside a stricter one. Against 40 degree-preserving
(Maslov-Sneppen) nulls, which hold in-degree and out-degree of all 138,639 nodes exactly,
the null mean is 84,932 +- 401 reciprocal edges and no null of 40 reaches the observed
value, giving **47.3x**. The 47.3x figure is the defensible one, because part of the
338.8x is attributable to the degree sequence rather than to reciprocal wiring. Both are
reported in version 2, with the degree-preserving comparison as the primary claim.

The reciprocal edge count itself, 4,014,518, is unchanged and has been reproduced by three
independent implementations.

## 2. The claim that the topology concentrates rather than proliferates

The qualitative conclusion that the topology "concentrates rather than proliferates" motor
access rested on the count of zero enriched classes. With four enriched classes it does not
hold, and **it is withdrawn.**

It is replaced by a stronger and more specific claim:

> Motor access is not uniformly frugal. It is hierarchically routed across two to three
> orders of magnitude, ordered by the behavioural urgency of each pathway.
> Mechanosensory, gustatory and ascending pathways, which must reach motor output within
> milliseconds, are enriched; visual and olfactory pathways, which must first construct a
> scene or an odour identity, are depleted.

Tested against 40 degree-preserving nulls, this survives with the sign preserved in
**8 of 8** classes and no null of 40 reaching the observed value in any class.

Two quantitative caveats belong with it, neither present in version 1:

1. **The spread between extremes is 283x, not 991x.** The larger figure was computed
   against a uniform-density baseline; part of that spread is attributable to the degree
   sequence.
2. **The ordering within the depleted group changes.** Against the degree-preserving null,
   olfactory (0.034x) rather than visual (0.145x) is the most depleted class. Any
   statement that visual has the least motor access is not supported and is removed.

A limit of this test is stated explicitly: these nulls preserve degree but not modular
structure. The routing hierarchy has **not** been tested against a community-preserving
null, so the supported claim is that it exceeds what the degree sequence explains, with
the contribution of modular architecture unmeasured.

## 3. Instability of the reported 1,559x ratio

Version 1 reported a ratio of **1,559x** as the primary quantitative statement of
intra-modal retention, in the Abstract (twice), 1.3, 3.4, 4.1, the Conclusions, and
Table 7. The ratio is numerically unstable because its denominator sits at the numerical
floor of the metric.

At step 195, Table 7 reports:

| | Real | Control mean | Control sd | Difference | Ratio |
| --- | --- | --- | --- | --- | --- |
| Step 195 | 0.8328 | 0.0005 | 0.0003 | 0.832 | 1,559x |

The control's standard deviation is 60% of its own mean. Propagating that variability
through the quotient:

| Denominator | Resulting ratio |
| --- | --- |
| mean - 2sd = -0.0001 | undefined (negative denominator) |
| mean - sd = 0.0002 | 4,164x |
| mean = 0.0005 | 1,666x |
| mean + sd = 0.0008 | 1,041x |

Within one standard deviation the ratio spans a factor of 4.0. At two it is undefined.
**A statistic whose 95 per cent interval includes infinity cannot serve as a primary
quantitative claim.**

The trajectory identifies what the ratio's growth measures:

| Step | Real | Control | Difference | Ratio | Numerator growth | Ratio growth |
| --- | --- | --- | --- | --- | --- | --- |
| 15 | 0.6869 | 0.6530 | 0.034 | 1.1x | 1.00x | 1x |
| 60 | 0.6304 | 0.4691 | 0.161 | 1.3x | 0.92x | 1x |
| 80 | 0.6797 | 0.1109 | 0.569 | 6.1x | 0.99x | 6x |
| 120 | 0.8071 | 0.0041 | 0.803 | 197x | 1.17x | 187x |
| 180 | 0.8318 | 0.0006 | 0.831 | 1,386x | 1.21x | 1,318x |
| 195 | 0.8328 | 0.0005 | 0.832 | 1,666x | 1.21x | 1,583x |

The numerator increases by a factor of 1.21 across the interval. The ratio increases by a
factor of 1,583. **Three orders of magnitude of the ratio's growth are attributable to the
collapse of the denominator, not to any change in the biological measurement.** The ratio
therefore does not quantify how much better the biological connectome separates
modalities; it quantifies how quickly the control loses all modality-specific structure.

**Corrected primary statistic.** Version 2 adopts the difference:

> Post-stimulus, cosine RDI in the biological connectome rises from 0.630 to 0.833 while
> the degree-preserving control falls from 0.469 to 0.0005, giving **a difference of 0.832
> on a metric bounded in [0, 1]**. The biological connectome retains essentially all of
> the modality separation that the control loses entirely.

Ratios are reported only where the denominator is measurably above the floor: **1.3x at
step 60** and **6.1x at step 80**. For steps at or beyond 120 the Ratio column of Table 7
reads "-- (denominator at numerical floor)".

The same defect affects the three intra-modal ratios in Table 1 (1,167x, 3,202x, 3,413x),
whose denominators are 4.15e-7, 7.3e-8 and 1.0e-7 with a single control. Version 1 already
labelled them "descriptive ratios, not statistically tested" in a table footnote. Version 2
removes them from the Abstract and Conclusions and retains them only as descriptive
statistics with that caveat repeated in the body text.

**New limitation added to section 5:**

> **Ratios with denominators at the numerical floor.** When a randomised control loses all
> modal structure, its cosine RDI converges to the numerical floor of the metric with a
> dispersion comparable to its own mean. Any ratio computed against such a denominator is
> unstable by construction and grows as the control decays, independently of the behaviour
> of the biological connectome. Differences are reported as the primary statistic for this
> reason. The same consideration applies to any metric normalised against a control that
> decays toward zero.

## 4. Data availability URL and licence

The repository URL given in Data Availability,
`github.com/Mendieta-Architect/drosophila-fep-connectome`, returned HTTP 404 at the time
of publication, and no repository existed at that path. The account name was incorrect
rather than the repository merely unpopulated, and no redirect exists. The correct location
is:

> **https://github.com/gatehot59-star/drosophila-fep-connectome**

The licence stated as AGPL v3 is superseded: **GPLv3** for the analysis code, and GPLv3
plus a separate commercial licence for the embedded inference engine and network
topologies.

## 5. Data provenance and required citations

**Annotation version.** The manuscript cites FlyWire v783. That identifier pins the
**connectome** and not the **annotations**, which are versioned separately in a public
repository and have been revised since the analysis was run. Methods should state the
annotation release explicitly:

> Annotations: `flyconnectome/flywire_annotations` release **v3.0.0** (2025-10-09),
> 139,244 rows, md5 `16ee17446c428bd27cf2bdefb83af4fd`.

That release matches the analysis run's row count exactly and is the pin required to
reproduce the published figures. A later release (v3.1.0, 2026-07-21, 139,248 rows) differs
by four rows and by a retyping of Johnston's Organ; the class-level populations used here
differ by three neurons in mechanosensory (0.11%) and six in visual (0.05%).

**Citations required by the data authors.** For any annotation release at or above v3.0.0
the authors require that four works be cited. Version 1 does not cite all four:

- Dorkenwald et al. (2024), *Neuronal wiring diagram of an adult brain*, Nature.
  doi:10.1038/s41586-024-07558-y
- Schlegel et al. (2024), *Whole-brain annotation and multi-connectome cell typing of
  Drosophila*, Nature. doi:10.1038/s41586-024-07686-5
- Matsliah et al. (2024), *Neuronal parts list and wiring diagram for a visual system*,
  Nature.
- Berg et al. (2025), *Sexual dimorphism in the complete connectome of the Drosophila male
  central nervous system*, bioRxiv. doi:10.1101/2025.10.09.680999

The release corresponding to Schlegel et al. alone is v2.1.0, which is not the version
analysed. Citing the connectome and the Schlegel annotations while omitting Berg et al.
misattributes the annotation version actually used.

**Provenance of the connectivity matrix, and of one column the results depend on.** The
connectivity matrix was not read from the primary FlyWire release but from a third-party
re-host derived from the leaky integrate-and-fire model of Shiu et al.
(doi:10.1101/2023.05.02.539144). The `Excitatory x Connectivity` column, on which every
excitatory count in the manuscript depends, is that model's excitatory/inhibitory
assignment derived from neurotransmitter predictions. **It is not a FlyWire measurement.**
The manuscript should state this, because a reader who disputes those neurotransmitter
assignments disputes the motor-access table. The full chain is: FlyWire v783 -> LIF model
and E/I assignment (Shiu et al.) -> re-hosted parquet -> this analysis.

## 6. Two factual corrections

1. **Swap acceptance rate.** The rate of 98.5% reported in this manuscript is correct. A
   companion document states 100%, which is not attainable under the stated constraints,
   since proposals that would create a self-loop or a duplicate edge must be rejected. The
   swap target, 45,275,949, is correct and has been reproduced.
2. **Reference with incorrect authorship.** The reference given as "Barsotti, F., et al.
   (2026). Cascades and convergence... PLOS Complex Systems" carries the wrong author
   list. The correct reference, verified against the publisher's citation export, is:

> Betzel RF, Puxeddu MG, Seguin C, Misic B (2026) *Cascades and convergence: Dynamic signal
> flow in a synapse-level brain network.* PLOS Complex Systems 3(3): e0000091.
> doi:10.1371/journal.pcsy.0000091

## 7. Temporal separation against two null families, and a reproducibility limitation

This item reports a result that version 1 under-reported. It also documents a
reproducibility limitation found while verifying it, which is stated first because it
determines how the result may be read.

### 7a. Table 7 is not reproducible from the archived code

The temporal retention measurement was reimplemented from the published analysis code and
run on the same connectome. **It does not reproduce Table 7**, and the cause is not an
implementation difference. Five variants were tested:

| Variant | 15 | 60 | 80 | 120 | 180 | 195 |
| --- | --- | --- | --- | --- | --- | --- |
| **Table 7 as published** | **0.6869** | **0.6304** | **0.6797** | **0.8071** | **0.8318** | **0.8328** |
| all annotated nodes, 3 modalities (literal to the code) | 0.0043 | 0.0818 | 0.5998 | 0.7636 | 0.7830 | 0.7842 |
| same, in float32 as the code uses | 0.0043 | 0.0818 | 0.5998 | 0.7636 | 0.7830 | 0.7842 |
| intrinsic nodes only | 0.7070 | 0.9248 | 0.9623 | 0.9700 | 0.9508 | 0.9476 |
| annotated minus stimulated | 0.9468 | 0.9001 | 0.8711 | 0.8178 | 0.8048 | 0.8051 |
| all annotated, 4 modalities (adding gustatory) | 0.4225 | 0.4452 | **0.6876** | 0.7410 | 0.7439 | 0.7435 |

What this establishes, and what it does not:

- **Floating-point precision is not the cause.** float32, as the published code uses, and
  float64 agree to four decimal places at all six timepoints, worst absolute difference
  4.9e-5.
- **The number of modalities is not the cause.** Adding gustatory matches step 80 to within
  1.2 per cent, the closest agreement obtained by any variant at any point, but inverts the
  shape of the trajectory.
- **The node partition is not the cause.** Four partitions were tested and the one literal
  to the published code fits worst at early timepoints.
- **A high value at step 15 is not attainable under this metric.** The afferents of all
  three modalities occupy the same `super_class` bin, so their vectors are near-parallel
  before activity propagates outward, and the cosine distance is near zero by construction.
- **The shape of the trajectory is not reproduced by any variant.** Table 7 falls from
  0.687 to 0.630 between steps 15 and 60 before rising. No variant reproduces that fall,
  and the shape rather than the endpoint values is what carries the claim.

**None of Table 7's six values, and no occurrence of "1559", appears in any of the 29
archived analysis notebooks.** The script that produced Table 7 is not in the archive.
This is a reproducibility limitation of version 1 and is recorded as one. A reader working
from the published code and data will reach the same point.

An earlier draft of this erratum attributed the discrepancy to a one-step offset in when
the state is sampled relative to the stimulus. **That hypothesis is false and is
withdrawn.** The published code assigns the saved state after the update, which is what the
reimplementation also does. It was written before the relevant code had been read.

### 7b. The result, as a metric defined here

The following is reported as a property of the reimplemented metric, defined in this
erratum, and **not** as a reproduction of Table 7. The metric is the mean pairwise cosine
distance between per-region activation profiles across four stimulated sensory modalities,
under the propagation dynamics of the published model.

It was tested against two null families over 200 steps: 19 community-preserving nulls,
which preserve degree **and** the super-class connectivity matrix, and 19 degree-preserving
nulls.

| Step | Real | vs community-preserving (n = 19) | vs degree-preserving (n = 19) |
| --- | --- | --- | --- |
| 30 | 0.099155 | 2.613x, 0/19 nulls reach it | 5.375x, 1/19 |
| 60 | 0.216050 | 3.387x, 0/19 | 7.414x, 0/19 |
| 80 | 0.655220 | 3.051x, 0/19 | 5.921x, 0/19 |
| 100 | 0.694287 | 3.041x, 0/19 | 6.756x, 0/19 |
| 140 | 0.739882 | 3.271x, 0/19 | 30.753x, 0/19 |
| 200 | 0.742355 | 3.496x, 0/19 | 110.694x, 0/19 |

The community-preserving column is the informative one: those nulls leave the modular
architecture intact and randomise only the finer wiring. A three-fold separation against
them, with no null of 19 reaching the observed value at any step at or beyond 60, supports
a claim about specific connectivity rather than about modular organisation.

**Two neighbouring quantities do not have the same standing**, and version 2 reports them
separately:

| Measurement | Real | vs community-preserving | vs degree-preserving |
| --- | --- | --- | --- |
| Spectral radius | 0.989886 | 2.186x, **2 of 19 nulls reach it**, p = 0.15 | 4.597x, 0/19 |
| One-hop RDI | 0.401440 | **0.906x, all 19 nulls score higher** | 3.918x, 0/19 |
| One-hop RDI, at least 5 synapses | 0.753272 | 0.988x, all 19 higher | 4.100x, 0/19 |

Both exceed what the degree sequence explains and neither exceeds what the modular
architecture explains. **This is a positive finding and version 2 states it as one:** these
two quantities are properties of how the modules are arranged, while temporal retention is
a property of the wiring within and between them.

**A caveat on reported statistics.** Z-scores in these comparisons reach the hundreds
because the null distributions have very small variance (sd 0.0055 at step 80), not because
effect sizes are extraordinary. Ratios and the count of nulls reaching the observed value
are the reportable quantities. Version 1's own section on reported statistics already argues
this; the argument applies here too.

## 8. What this erratum does not change

Unaffected by the above:

- The direction and magnitude of the principal effect: the biological connectome retains
  modality separation post-stimulus while randomised controls do not.
- All static analyses reported on unnormalised weights that do not involve ratios against
  near-zero denominators.
- The contralateral cancellation result (1.37), a ratio of two large quantities
  (228,373 / 166,770), not subject to the item 3 defect.
- The SparseLTC and linear equivalence, and the time-constant sensitivity analysis.
- The synaptic depth profiles.
- The conclusion that amplification requires graded dynamics and is not purely topological.
- The declared limitation that Maslov-Sneppen is the weakest available control, which the
  additional null families here partially address.

## Table of corrected values

| Quantity | Version 1 | Version 2 |
| --- | --- | --- |
| Graph density | 0.00739526 | **0.000785197** |
| Motor-access summary | 0 enriched, 7 depleted | **4 enriched, 4 depleted** |
| mechanosensory to motor | 1.3x | **12.378x** |
| gustatory to motor | 0.5x depleted | **4.482x enriched** |
| ascending to motor | 0.6x | **17.839x** |
| unknown sensory to motor | 1.4x | **12.858x** |
| Reciprocity vs chance | 36x | **338.8x** (uniform density); **47.3x** (degree-preserving, primary) |
| Routing spread | not reported | **283x** (degree-preserving) |
| Most depleted sensory class | visual | **olfactory** |
| Primary retention statistic | ratio 1,559x | **difference 0.832 on [0, 1]** |
| Retention ratio, step 60 | -- | 1.3x |
| Retention ratio, step 80 | -- | 6.1x |
| Retention ratio, steps 120 and beyond | 197x to 1,559x | **not reported (denominator at floor)** |
| Table 7 reproducibility | not addressed | **not reproducible from archived code; limitation declared** |
| Annotation version | implied by "v783" | **v3.0.0, md5 16ee1744...** |
| Data availability URL | 404 | **github.com/gatehot59-star/...** |
| Licence | AGPL v3 | **GPLv3 (plus commercial for the engine)** |
| "Barsotti et al. (2026)" | incorrect authorship | **Betzel, Puxeddu, Seguin and Misic (2026)** |

## Acknowledgement of method

The corrections in items 1 and 2 were identified by recomputing the connectome
measurements with an implementation that shares no code with the original analysis
pipeline. That recomputation reproduced the manuscript's observed counts exactly, including
the reciprocal edge count (4,014,518), the motor neuron count (1,485), the excitatory
fraction of edges (0.6003) and the observed excitatory edge counts of all eight sensory
classes, which is what isolated the expected-value baseline as the sole point of
divergence. The additional null families were computed on the same connectome with per-null
verification that in-degree and out-degree were preserved exactly for all 138,639 nodes.

Item 7a required seven complete propagation runs across five metric variants and two
floating-point precisions. Code, raw run logs and checksums are available at the repository
given in item 4.

## What remains unresolved

One item, stated so that it is not mistaken for settled:

**Table 7 has not been reproduced, and the script that produced it has not been located.**
Every implementation hypothesis available for testing has been tested and eliminated
(item 7a). If the original script is recovered it can be run against the null families
directly, and item 7b would then become a reproduction rather than an independent metric.
Until then, Table 7's values stand as published but unverified, and the limitation is
recorded above.
