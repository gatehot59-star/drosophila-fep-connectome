# Erratum to Mendieta (2026a)

Corrections to *Signal propagation properties in the Drosophila melanogaster
connectome*, Zenodo, March 2026. Seven items. Items 1 and 2 change reported values and one
qualitative conclusion; items 3 to 6 are factual corrections; **item 7 strengthens a
result that is currently under-reported.**

None of these corrections weaken the paper. Item 1 makes the central finding stronger and
more specific, item 2 removes a number that cannot survive scrutiny and replaces it with
one that can, and item 7 is the result that should have been the headline.

## 1. Graph density, and the motor-access table that depends on it

The density used for expected-value calculations was 0.00739526. The correct density of
the directed graph is **0.000785197**: 15,091,983 unique directed edges over
138,639 x 138,638 ordered pairs. The reported figure is 9.42 times too large.

The cause of the incorrect value is **not established** and no explanation is offered
here. A previously considered explanation, that synapse counts were used in place of
connection counts, has been tested and rejected: the synapse total is 54,492,922, which
does not reconcile with the reported density.

Observed counts are unaffected. Expected values, and therefore the enrichment verdicts,
are. The corrected table:

| Class | N | Observed | Published ratio | Corrected ratio | Verdict changes |
| --- | --- | --- | --- | --- | --- |
| visual | 10,855 | 137 | 0.0x | 0.018x | no |
| olfactory | 2,279 | 80 | 0.0x | 0.050x | no |
| hygrosensory | 74 | 13 | 0.0x | 0.251x | no |
| thermosensory | 29 | 14 | 0.1x | 0.690x | no |
| mechanosensory | 2,656 | 23,010 | 1.3x | **12.378x** | **yes** |
| gustatory | 408 | 1,280 | 0.5x depleted | **4.482x enriched** | **yes, sign reversed** |
| ascending (AN) | 2,231 | 27,857 | 0.6x | **17.839x** | **yes** |
| unknown sensory | 131 | 1,179 | 1.4x | **12.858x** | **yes** |

Summary as published: 0 enriched, 7 depleted. Corrected: **4 enriched, 4 depleted**.

Reciprocity is affected in the opposite direction, and here the error understated the
result: reciprocity is 26.60 per cent against a chance expectation of 0.0785 per cent, a
ratio of **338.8x**, not 36x. The reciprocal edge count, 4,014,518, is unchanged and has
since been reproduced by three independent implementations.

## 2. The claim that the topology concentrates rather than proliferates

That claim rested on the count of zero enriched classes. With four enriched classes it
does not hold and is withdrawn.

It is replaced by a stronger and more specific claim: motor access is not uniformly
frugal but **hierarchically routed across two to three orders of magnitude, ordered by
the behavioural urgency of each pathway.** Mechanosensory, gustatory and ascending
pathways, which must reach muscle within milliseconds, are enriched; visual and
olfactory pathways, which must first construct a scene or an odour identity, are
depleted.

This replacement claim has since been tested against a stricter null model that
preserves in-degree and out-degree exactly (40 nulls, this repository). It survives with
the sign preserved in 8 of 8 classes and no null out of 40 reaching the real value in
any class. Under that null the spread between extremes is 283x rather than 991x, and the
ordering within the depleted group shifts: olfactory rather than visual is the most
depleted class. Both figures are reported; the degree-preserving one is the defensible
one, because part of the density-based spread was attributable to the degree sequence.

One limit of this test should be stated with it: those 40 nulls preserve degree but not
modular structure. The routing hierarchy has **not** been tested against a
community-preserving null, so the correct claim is that it exceeds what the degree
sequence explains, with the contribution of modular architecture unmeasured.

## 3. The amplification ratio reported as 1,559x

This value appears nine times in the published version, including the abstract. It is a
quotient whose denominator is 0.0005 with a standard deviation of 0.0003, that is, a
dispersion of 60 per cent of its own mean. Within one standard deviation of that
denominator the quotient ranges from about 1,041x to about 4,164x, so the value is not
determined to better than a factor of four by its own control.

The trajectory confirms the diagnosis: between t = 80 and t = 195 the ratio grows from
6.1x to 1,559x while the numerator moves only from 0.68 to 0.83. The growth is the
control decaying toward zero, not the real system separating further.

The quotient is withdrawn and replaced by the **difference, 0.832 on a [0, 1] range**,
which is a large effect and does not depend on dividing by a quantity near its numerical
floor. Quotients are additionally reported at t = 60 (1.3x) and t = 80 (6.1x), where the
denominator is measurable, with an explicit statement that beyond t = 120 the control is
at the numerical floor and the quotient is not interpretable.

The ratios in Table 1 have the same defect, with denominators of 1.0e-7 and 7.3e-8 and a
single control. The paper already labelled them descriptive and not statistically
tested; they should not have reached the abstract on that basis and are withdrawn from
it.

## 4. Data availability URL and licence

The URL given in Data Availability, github.com/Mendieta-Architect/drosophila-fep-connectome,
returned HTTP 404 at the time of publication and no repository was ever created at that
path. The correct location is:

  https://github.com/gatehot59-star/drosophila-fep-connectome

The account name in the published URL was incorrect, not merely unpopulated. Readers
following the published link found nothing, and no redirect exists.

The licence stated as AGPL v3 is superseded: GPLv3 for the analysis code, and GPLv3 plus
commercial for the embedded inference engine and network topologies. See LICENSE.

## 5. Data provenance: the annotation version, and citations that were missing

The paper cites FlyWire v783. That string pins the connectome and **not** the
annotations, which are versioned separately in a public repository and have been revised
since. Methods should state the annotation release explicitly.

Measured against the tagged releases, the analysis used **v3.0.0** (2025-10-09,
139,244 rows, md5 16ee17446c428bd27cf2bdefb83af4fd), which matches the March 2026 run
at the digit. That is the pin required to reproduce the published figures.

This has a consequence for the reference list that is easy to miss. The annotation
authors require, for any version at or above 3.0.0, that **four** works be cited: Berg
et al. (2025), Schlegel et al. (2024), Matsliah et al. (2024) and Dorkenwald et al.
(2024). The release matching Schlegel et al. alone is v2.1.0, which is **not** the
version used. Citing the connectome and the Schlegel annotations while omitting Berg et
al. misattributes the annotation version actually analysed.

A second provenance gap, and it touches a column the results depend on. The connectivity
matrix was not read from the primary FlyWire release but from a third-party re-host
derived from the Shiu et al. leaky integrate-and-fire model
(doi:10.1101/2023.05.02.539144). The `Excitatory x Connectivity` column, which every
excitatory count in the paper uses, is that model's excitatory/inhibitory assignment
derived from neurotransmitter predictions, not a FlyWire measurement. The paper should
say so, because a reader who disputes those calls disputes the motor-access table. Full
chain in docs/CITATION.md.

## 6. Two smaller items

1. The swap acceptance rate is **98.5 per cent**, as stated in this paper. A companion
   document states 100 per cent, which is not attainable under the stated constraints
   and is the value that requires correction. The swap target, 45,275,949, is correct and
   has been reproduced.
2. The reference given as Barsotti et al. (2026), Cascades and convergence, PLOS Complex
   Systems, carries the wrong author list. The same title and journal appear elsewhere as
   Betzel, Puxeddu, Seguin and Misic (2026), 3(3), e0000091. The author list requires
   verification against the published article before the erratum is filed.

## 7. Under-reported: the result that survives both null families

This item adds rather than corrects, and it exists because the strongest result in the
study was at risk of being buried under the six items above.

**Temporal RDI separates the real connectome from both null families at the permutation
floor.** Tested against 19 community-preserving nulls and 19 degree-preserving nulls:

| t | Real | vs CP (19) | vs MS (19) |
| --- | --- | --- | --- |
| 30 | 0.099155 | 2.613x, z 36.1, 0/19 | 5.375x, z 2.8, 1/19 |
| 60 | 0.216050 | 3.387x, z 49.2, 0/19 | 7.414x, z 5.6, 0/19 |
| 80 | 0.655220 | **3.051x, z 79.9, 0/19** | 5.921x, z 13.3, 0/19 |
| 100 | 0.694287 | 3.041x, z 65.0, 0/19 | 6.756x, z 18.4, 0/19 |
| 140 | 0.739882 | 3.271x, z 32.2, 0/19 | 30.753x, z 55.9, 0/19 |
| 200 | 0.742355 | 3.496x, z 15.0, 0/19 | **110.694x, z 197.0, 0/19** |

The CP column is what matters. Those nulls preserve degree **and** the super-class
connectivity matrix, so they leave the modular architecture of the brain intact and only
randomise the fine wiring. A three-fold separation against that null, with no null out of
19 reaching the real value at any t >= 60, is a statement about specific wiring and not
about modular organisation.

A caveat that belongs with it rather than in a footnote: z-scores in the hundreds here
reflect very small null variance (sd 0.0055 at t = 80), not extraordinary effect sizes.
Report the ratio and the count of nulls exceeding the real value. The paper's own section
on reported statistics already argues this, and the argument applies to these numbers too.

### Two neighbouring claims that do not have the same standing

These should be reported next to the above, not merged with it:

| Measurement | Real | vs CP | vs MS |
| --- | --- | --- | --- |
| Spectral radius rho | 0.989886 | 2.186x, **2 of 19 nulls reached it**, p 0.15 | 4.597x, z 21.3, 0/19 |
| One-hop RDI | 0.401440 | **0.906x, all 19 nulls scored higher**, p 1.0 | 3.918x, z 5.6, 0/19 |
| One-hop RDI, >= 5 synapses | 0.753272 | 0.988x, all 19 higher | 4.100x, z 6.3, 0/19 |

Both exceed what the degree sequence explains and neither exceeds what the modular
architecture explains. **That is a positive finding and should be written as one:** these
two quantities are properties of how the brain's modules are arranged, while temporal RDI
is a property of the wiring within and between them. Presenting all three as equally
supported would not survive review; presenting the distinction is a stronger paper than
omitting it.

## What is not corrected

The effective membrane time constant is reported as 1/tau = 8.4 steps. For the update
used, h <- (1 - tau) h + tau tanh(.), the effective constant is -1 / ln(1 - tau) = 7.89
steps, a 6.5 per cent difference. Both values fall inside the physiological range for
Drosophila and no conclusion depends on the difference, but the derivation is incorrect
and is corrected in this repository for future work.
