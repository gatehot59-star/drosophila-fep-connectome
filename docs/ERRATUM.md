# Erratum to Mendieta (2026a)

Corrections to *Signal Propagation Properties in the Drosophila melanogaster Connectome:
Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*,
deposited at Zenodo, 20 March 2026.

**Identifiers.** Concept DOI `10.5281/zenodo.19136947` (always resolves to the latest
version); v1.0 DOI `10.5281/zenodo.19136948`. The v1.0 record remains available and is
**not** withdrawn: it is part of the public record and its DOI continues to resolve.

Nine items. Items 1 to 3 change reported values and one qualitative conclusion; items 4
to 8 are factual corrections; item 9 concerns the verification script this work cites.

None of these corrections weakens the central findings. Item 1 replaces a number that
cannot survive scrutiny with one that can, **and establishes its cause**, which v1.0 could
not. Item 2 makes the motor-access result stronger and more specific.

---

## Reference works cited throughout this erratum

Stated once, in full, because two companion papers published in the same issue of the same
journal are easy to conflate and this erratum corrects figures against both:

- **Dorkenwald, S., Matsliah, A., et al. and the FlyWire Consortium (2024).** *Neuronal
  wiring diagram of an adult brain.* **Nature 634, 124–138.** The data paper: the
  connectome itself, 139,255 proofread neurons, and the source of the figure of **12.6
  synapses per connection**.
- **Lin, A., Yang, R., et al. (2024).** *Network statistics of the whole-brain connectome
  of Drosophila.* **Nature 634, 153–165.** The network-analysis paper: the source of the
  **connection probability 0.000161** and the **connection reciprocity 0.138**, both
  measured on the v630 snapshot under a five-synapse threshold.

**v1.0 cites the first and does not cite the second.** Since Lin et al. is the
network-analysis paper for the same connectome, and this work is a network analysis of
that connectome, the omission is corrected: both are cited in v2.0.

---

## 1. Graph density, its cause, and everything normalised by it

Section 2.1 of v1.0 reports `Density = 0.0074`. This value is incorrect. The correct
density of the directed graph is **0.000785197**: 15,091,983 unique directed edges over
138,639 x 138,638 ordered pairs. The reported figure is **9.42 times too large**.

### The cause is established: a silent 32-bit integer overflow

The node count was held as a 32-bit integer, so the product `N*(N-1)` overflowed:

```
N*(N-1) exact           = 19,220,633,682
N*(N-1) as int32        =  2,040,764,498      (the exact product less 4 x 2^32)
15,091,983 / 2,040,764,498 = 0.007395259
density reported in v1.0   = 0.00739526
```

The two agree to **eight significant figures** (difference 5.2e-10). The expression emits
a runtime warning but **raises no exception**, so nothing in the pipeline failed. This is
a general hazard: any density computation over a graph with more than roughly 46,000
nodes will overflow silently if the node count is held in a 32-bit integer, in any
language with fixed-width integers.

All 40 archived analysis notebooks across both compute accounts were inspected for this
expression. **Three contain it; the remaining thirty-seven do not compute a density.**
One of the three is the verification script (item 9).

### Two published quantities descend from that single line

They are one error with two symptoms, not two oversights:

- **Table 5**, the density analysis of motor access, via
  `expected_edges = N_class x N_motor x density x P(excitatory)`. See item 2.
- **The reciprocity over-representation factor reported as 36x** in the abstract and in
  Section 3.5, via `expected_reciprocity = density`. With reciprocity 26.60 per cent,
  `0.2660 / 0.00739526 = 35.97`, which is the published figure. With the corrected
  density the quotient is 338.8x. See item 3.

**No other reported quantity is normalised by graph density.** The temporal metrics, the
depth profiles, the contralateral cancellation and the estimate of tau derive from
column-normalised propagation or from direct counts, and are unaffected. This was
verified by inspection rather than assumed.

### What was tested and rejected

A previously considered explanation, that synapse counts were used in place of connection
counts, has been **tested and rejected**: the synapse total is 54,492,922, which does not
reconcile with the reported density.

That said, v1.0 does use both terms for the same quantity: the abstract reads
*"E = 15,091,983 synapses"* while Section 2.1 reads *"15,091,983 connections"*. A
connection is an ordered pair of connected neurons; a synapse is an individual contact.
The two counts differ by a factor of 3.61 in this dataset without a synapse threshold,
and by 12.65 with one. **This is a separate defect of exposition**, corrected here, and it
is not the cause of the density error.

---

## 2. Table 5, the density analysis of motor access

Observed counts are unaffected. Expected values, and therefore the enrichment verdicts,
are. The analysis was recomputed from the same data with the corrected density.

**The expectation is stated explicitly here, because v1.0 calls it a "density
expectation" and that is incomplete.** The quantity actually computed is:

```
expected_edges = N_class x N_motor x density x P(excitatory | edge exists)

with  N_motor = 1,485,  P(excitatory | edge exists) = 0.600272
```

The factor `P(excitatory)` is not mentioned in v1.0 and materially changes the
expectation. Populations are defined by `cell_class` (`super_class` for the optic
class), intersected with the connectivity graph.

| Class | N | Observed exc. edges | Published ratio | Corrected ratio | Verdict changes |
| --- | --- | --- | --- | --- | --- |
| mechanosensory | 2,656 | 23,010 | 1.3x | **12.378x** | **yes, now enriched** |
| unknown sensory | 131 | 1,179 | 1.4x | **12.858x** | **yes, now enriched** |
| gustatory | 408 | 1,280 | 0.5x depleted | **4.482x enriched** | **yes, sign reversed** |
| ascending (AN) | see below | see below | 0.6x | **not reproducible** | **see below** |
| hygrosensory | 74 | 13 | 0.03x | 0.251x | no, still depleted |
| thermosensory | 29 | 14 | 0.07x | **0.690x** | **yes, now within expectation** |
| olfactory | 2,279 | 80 | 0.005x | 0.050x | no, still depleted |
| visual | 10,855 | 137 | 0.002x | 0.018x | no, still depleted |
| visual optic | 77,530 | 1,679 | 0.003x | 0.031x | no, still depleted |

**Summary as published (Section 3.3): 0 enriched, 7 depleted. Corrected: 4 enriched,
4 depleted, 1 within expectation.**

### Validation of the recomputation

When the recomputation is run **with the overflowed density**, it reproduces the published
ratio for **eight of the nine rows** (1.314 against 1.3; 1.365 against 1.4; 0.476 against
0.5; 0.027 against 0.03; 0.073 against 0.07; and the three at 0.005x, 0.002x and 0.003x).
The motor population count is reproduced exactly (1,485). The formula and the population
definitions are therefore established, not inferred.

### The ascending (AN) row is not reproducible and is not corrected here

Table 5 of v1.0 gives `N = 495` for the AN class. The annotation table contains 2,276
neurons with `cell_class = AN`, of which 2,231 appear in the connectivity graph. No
filter consistent with the other eight rows yields 495. With `N = 2,231` the ratio under
the overflowed density is 1.894x rather than the published 0.6x, so the discrepancy is
not a rounding effect.

**The AN row is therefore declared not reproducible rather than corrected.** Substituting
a different population and presenting the result as a correction would replace one
unverifiable number with another.

### Consequence for the interpretation in Section 3.3 and 4.2

The statement *"Zero classes enriched. Seven classes depleted. No sensory class has more
direct motor access than expected from graph density"* **does not survive** and is
withdrawn. Four classes exceed expectation, three of them by more than an order of
magnitude.

The framing of Section 4.2, *"the topology concentrates rather than adds"*, rested on the
count of zero enriched classes and is **withdrawn**. The observed pattern is not uniform
depletion but a **spread of roughly three orders of magnitude between extremes**
(12.9x for unknown sensory down to 0.018x for visual), ordered such that pathways which
must reach muscle within milliseconds are enriched and pathways which must first construct
a scene or an odour identity are depleted.

That replacement claim has since been tested against a null model preserving in-degree
and out-degree exactly (40 nulls, this repository). It survives with the sign preserved in
8 of 8 classes and no null out of 40 reaching the real value. Under that null the spread
between extremes is **283x** rather than 991x, and the ordering within the depleted group
shifts: **olfactory rather than visual is the most depleted class**.

**A limitation is stated here that v1.0 could not have stated.** Against a null that also
preserves modular block structure, this quantity is **conserved by construction**: the
null shuffles targets within blocks defined by super-class, and the motor group is itself
defined by super-class, so the count cannot change. Measured across 40 such nulls the
standard deviation is exactly zero and every null equals the real value. The routing
hierarchy is therefore established against degree but **untestable against modularity**
with this null family. A null with coarser blocks is required, and has not been run.

---

## 3. The reciprocity over-representation factor

The abstract and Section 3.5 report reciprocity of 26.6 per cent as *"36x over density
expectation"*. That factor was computed against the incorrect density (item 1) and is
**withdrawn**. The reciprocal edge count, 4,014,518, is unchanged and has been reproduced
by three independent implementations.

Rather than substitute the corrected quotient, this version reports reciprocity as a
**rank against a control ensemble**, which requires no density estimate and is therefore
immune to this class of error:

- Against 40 nulls preserving in-degree, out-degree and the community block structure,
  the real value ranks **first of 41**, with **0 of 40** nulls reaching it, a ratio of
  **20.59x** over the ensemble mean.
- Against the Maslov-Sneppen ensemble the ratio is 47.27x.

The quotient against a uniform density expectation is reported for continuity only
(338.8x with the corrected density) and is **not** the statistic on which the claim rests.
Quotients against uniform density are the weakest of the three comparisons available and
should not have been the headline figure.

**A further qualification, and it is not a consequence of the density error.** Lin et al.
(2024) report reciprocity and clustering coefficients for five connectomes side by side
(this fly brain, hermaphrodite and male *C. elegans*, larval zebrafish hindbrain and mouse
visual cortex) and conclude that *"the values of reciprocity and clustering coefficient
are comparable across all five datasets"*. Reciprocity in this connectome is therefore
elevated **relative to randomised controls** but **not unusual relative to other measured
nervous systems**, and the over-representation of reciprocal connections in brains is
described there as well established. The comparison against controls reported here stands;
the implication that the magnitude is distinctive of this connectome does not, and any
such wording is withdrawn. What remains specific to this work is the **decomposition of
reciprocity by circuit type** (Table 7: intra-motor 41.3 per cent down to optic-to-motor
0.0 per cent), which the published network analyses report only as a single global figure.

---

## 4. The 1,559x amplification ratio: withdrawn as out of scope

A previous draft of this erratum corrected an amplification ratio of 1,559x reported
"nine times, including the abstract", and also corrected ratios in Table 1 with
denominators of 1.0e-7 and 7.3e-8.

**Neither element exists in this paper.** The value 1,559 does not appear anywhere in
v1.0. Table 1 of v1.0 is the table of sensory and motor populations and contains no
ratios. The amplification result in v1.0 is stated as a **difference** throughout
(RDI rising from 0.63 to 0.83 post-stimulus, Table 8), which is already the defensible
form.

Those corrections belong to a different document in the same line of work and are
**withdrawn from this erratum**. They are recorded here rather than deleted silently,
because a correction addressed to a claim the paper never made is itself an error.

What does require care in v1.0 is the reporting of the amplification quotient in
derivative material: at t >= 120 the community-preserving control falls to 0.368 and
below, and at t = 195 to 0.299, so quotients computed against it beyond t = 120 approach
the numerical floor of the control and are not interpretable. Table 8 correctly reports
the two series side by side; **any quotient derived from it beyond t = 120 should not be
quoted.**

---

## 5. Reciprocity differs from the published value for the same connectome, and the cause is measured

v1.0 reports reciprocity of 26.6 per cent. **Lin et al. (2024, Nature 634:153–165)** report
**0.138** for FlyWire v630 under a **five-synapse threshold**, which v1.0 does not apply.
The same paper reports a connection probability of **0.000161** under that criterion, and
cites **Dorkenwald et al. (2024, Nature 634:124–138)** for a mean of **12.6 synapses per
connection**.

The threshold accounts for the gap. Measured on the same matrix used in v1.0:

| Inclusion criterion | Connections | Reciprocity | Connection probability |
| --- | --- | --- | --- |
| no threshold (as in v1.0) | 15,091,983 | **26.60%** | 0.000785197 |
| >= 2 synapses | 7,595,967 | 19.21% | 0.000395199 |
| >= 3 synapses | 4,916,231 | 16.45% | 0.000255779 |
| **>= 5 synapses (published criterion)** | 2,700,513 | **13.98%** | 0.000140501 |
| >= 10 synapses | 1,066,822 | 11.53% | 0.000055504 |

Under the published criterion this work yields **13.98 per cent against the reported 13.8
per cent**, a relative difference of 1.3 per cent. As an independent check of the criterion,
the mean number of synapses per connection above the threshold is **12.647** against the
reported 12.6, a relative difference of 0.37 per cent. The connection probability is
1.405e-4 against 1.61e-4, a difference of 12.7 per cent attributable to the different
reconstruction version (v783 here, v630 there).

**The two values are therefore consistent and the apparent disagreement is a difference of
inclusion criterion, not of measurement.** This version states the criterion used and
reports both. Agreement on three independently reported quantities, one of which was not
sought, is the basis for that conclusion.

A cross-criterion comparison appearing in earlier working notes, in which the unthresholded
reciprocity of this work was divided by the thresholded connection probability of the
published analysis, yielded a factor of 1,652x. That comparison mixes two inclusion
criteria and is **withdrawn**. Paired within a single criterion the factor is 995x, and
the statistic that should be quoted is the ensemble rank of item 3.

---

## 6. Internal count inconsistencies

Four counting problems are corrected.

- **Table 4 does not sum.** The total is given as 90,101 where the two components,
  85,821 and 4,281, sum to **90,102**.
- **Table 5 has nine rows; Section 2.3 states that the density analysis covers ten
  canonical sensory classes with N >= 10.** One class is absent from the table without
  explanation. **Which class is missing has not been established and is not asserted
  here.**
- **The count of depleted classes is inconsistent across three places.** Table 5 marks
  **six** rows Depleted and three "approximately expected". The text of Section 3.3 states
  **seven** classes depleted. The abstract states **7/10**. Under the corrected
  expectation the counts are four enriched, four depleted and one within expectation, over
  nine reported classes.
- **The thresholds are now defined explicitly.** v1.0 applies the verdicts "enriched",
  "depleted" and "approximately expected" without stating the boundaries. They are:
  enriched if ratio > 2 and p < 0.001; depleted if ratio < 0.5 and p < 0.001;
  approximately expected if 0.5 <= ratio <= 2.

---

## 7. The count of neural models, and the temporal parameter

**Model count.** The abstract of v1.0 states *"four parameter-free neural models"*.
The LIF-hard model yields undefined Cosine RDI at the sampled time steps, as Section 2.5
and Limitation 3 of v1.0 already state. The abstract is therefore inconsistent with the
body of the paper and is corrected to **three compatible models** (SparseLTC, Linear,
LIF-soft), with the fourth reported as metric-incompatible rather than omitted.

**The temporal parameter, two separate defects.** Section 2.5 states that tau = 0.119
corresponds to tau_m ~= 8.4 ms, *"center of the Drosophila physiological range (5-20 ms)"*,
and that tau = 0.3 corresponds to *"3.3 ms, lower limit of range"*.

- **The characterisations are overstated.** The midpoint of 5-20 ms is 12.5 ms, so 8.4 ms
  is **within** the range rather than at its centre; and 3.3 ms is **below** the cited
  range rather than at its lower limit.
- **The derivation is incorrect.** For the update used, `h <- (1 - tau) h + tau tanh(.)`,
  the effective constant is `-1 / ln(1 - tau) = 7.89` steps, not 8.4. The difference is
  6.5 per cent.

Both values fall inside the physiological range and no conclusion depends on the
difference, but both statements require correction and the corrected derivation is used
in this repository for future work.

---

## 8. Data availability, licence, pinned data and references

**The repository URL in Data Availability is wrong, not merely unpopulated.** v1.0 gives
`github.com/Mendieta-Architect/drosophila-connectome-propagation`. No repository was ever
created at that path and the account name is incorrect. The correct location is:

```
https://github.com/gatehot59-star/drosophila-fep-connectome
```

Readers following the published link found nothing, and no redirect exists.

**The DOI placeholder.** The v1.0 header carries the literal string
`10.5281/zenodo.XXXXXXX`. The assigned identifiers are given at the top of this erratum.

**The licence.** v1.0 states AGPL v3 for the analysis code and CC BY 4.0 for the archived
numerical results. This is superseded: **GPLv3** for the analysis code, and **GPLv3 plus a
commercial option** for the embedded inference engine and the network topologies. See
LICENSE.

**Pinned data.** The annotation table was fetched from a live branch and has since
changed. Methods should read: annotations pinned to commit
`17fc57722002e1a7d38cdd0c89ac382bf92718da`, md5 `719904abad876c68ace1b5690c9b9b63`. The
connectivity matrix used throughout has md5 `3d802fd542b5d18570ba1ba0bb0abed9`. The
string "v783" pins the connectome only, not the annotations.

**A missing reference.** v1.0 cites the connectome data paper (Dorkenwald et al. 2024) but
does not cite **Lin et al. (2024), Nature 634:153–165**, the network-analysis paper for the
same connectome, against whose figures items 3 and 5 of this erratum are stated. It is
added to the bibliography of v2.0.

**One further correction.** The swap acceptance rate is **98.5 per cent**, as stated in
Section 2.4 of v1.0. A companion document states 100 per cent, which is not attainable
under the stated constraints and is the value requiring correction. The swap target,
45,275,949, is correct and has been reproduced.

**One reference requires verification before this erratum is filed.** Section 1.2 and the
bibliography of v1.0 cite Betzel, Puxeddu, Seguin and Misic (2026), *Cascades and
convergence*, PLOS Complex Systems 3(3), e0000091. The author list has not been checked
against the published article by the present analysis and must be before filing.

---

## 9. The verification script shares the defect it was written to catch

The reproducibility script associated with this work computes graph density with the same
overflowed expression described in item 1. **It therefore cannot detect that error by
construction:** the pipeline produces 0.0074 and the verifier recomputes 0.0074, so the
comparison confirms the value instead of challenging it.

Its reference table additionally carries `density = 0.00074` where `0.0074` was intended,
one digit short. The consequence is that the density check does report a mismatch, of
899 per cent against a 2 per cent tolerance, **but for the wrong reason**: it is comparing
an overflowed computation against a mistyped reference. Had the computation been correct,
the reported deviation would have been 6.1 per cent, which reads as a data-version
difference and would plausibly have been dismissed.

Both are corrected. The reference table now records recomputed values with their
provenance, and the density expression is computed in arbitrary-precision integers.

**The general point is stated because it is the more useful finding.** The verification
script and the analysis pipeline share their data-loading block. Any defect in that block
is invisible to the verifier no matter how many tests follow it. A reproducibility check
recomputes from raw data with independent code, or it states explicitly which stages it
shares with the pipeline it verifies.

---

## What has not changed

The three propagation properties reported in v1.0 are retained.

Tables 2, 3, 6, 8, 9, 10 and S1 required no correction: their internal arithmetic was
verified and is consistent. The temporal dissociation between during-stimulus and
post-stimulus separation, the gustatory and mechanosensory decomposition, the synaptic
depth profiles and the physiological plausibility of tau are unaffected by item 1, because
none of them is normalised by graph density. This was verified by inspecting every
archived notebook rather than assumed.

Section 2.4 of v1.0 already derives and declares the analytical invariance of net RDI at
1-hop under the community-preserving null. That declaration is correct and is retained; it
is noted here because item 2 extends the same reasoning to the routing hierarchy, where
v1.0 did not apply it.

---

## Outstanding verification

Stated as open rather than resolved, so that no reader takes a conclusion this analysis
did not reach.

1. **The missing tenth class of Table 5.** Section 2.3 declares ten canonical sensory
   classes with N >= 10; the table reports nine. Which class is absent has not been
   established.
2. **The AN population.** N = 495 in Table 5 does not correspond to any filter consistent
   with the other eight rows. See item 2.
3. **Whether the p-values of Table 5 use the same expectation as the ratios.** The
   binomial test requires a per-pair probability, and whether it is the same quantity that
   enters the expected count has not been confirmed from the archived code.
4. **Table 8 is not reproducible from the archived code.** Four candidate partitions of
   the activation vector were tested against the published definition and none reproduces
   the shape of the trajectory, which falls between t = 15 and t = 60 and then rises. The
   six published values do not appear in any of the 40 archived notebooks. The script that
   produced Table 8 is not in the archive, and this is recorded as a limitation of
   reproducibility rather than as a corrected value.
5. **The three notebooks carrying the overflow declare themselves derived from an earlier
   pipeline** which is not among the archived notebooks. That they are the code that
   produced the published tables is supported by their reproducing eight of nine ratios of
   Table 5, but is not established.
6. **Whether Lin et al. apply the synapse threshold as applied here** (`synapse count >= 5`)
   has not been confirmed against their Methods; the agreement of three independently
   reported quantities is consistent with it.
7. **Prior art for the community-preserving null.** Section 2.4 of v1.0 presents the
   community-preserving null as a methodological contribution. Lin et al. (2024) describe a
   **neuropil connection (NPC) model** that constrains a degree-preserving random network
   by enforcing the measured connection probabilities between 78 anatomically defined
   neuropils, and a **neuron-neuron distance (NND) model** with spatially varying
   connection probability. The NPC model belongs to the same family as the null used here,
   at a different granularity (78 anatomical neuropils against 10 functional super-classes).
   **The two have not been implemented side by side and compared**, so whether they yield
   equivalent ensembles is not established. The prior work is cited in v2.0 regardless, and
   the claim of novelty for the null model is narrowed accordingly.

---

## How these errors were found

By recomputing the reported figures against each other and against published values for
the same dataset, and by re-running the archived analysis code rather than reading it.

The density error was identified by checking the paper's own N and E. Its **cause** was
found only when the recomputation was executed: the arithmetic library emitted an overflow
warning on the same expression, which no amount of reading the code would have produced.
The scope of the damage was bounded by inspecting all 40 archived notebooks across both
compute accounts rather than the subset available locally.

The qualifications in items 3 and 5, and the prior art in Outstanding verification 7, were
found by reading the companion network-analysis paper for the same connectome. They are
not arithmetic errors and no recomputation would have surfaced them: a figure can be
correct and still not be notable, and a method can be sound and still not be new.

This is recorded because it is reusable: a numerical discrepancy with an elegant
explanation should be executed before the explanation is written down, and a figure
intended for an abstract should be compared against whoever measured the same quantity in
another system before it is called distinctive.
