# Erratum to Mendieta (2026a)

Corrections to *Signal propagation properties in the Drosophila melanogaster
connectome*, Zenodo, March 2026. Five items. Items 1 and 2 change reported values and
one qualitative conclusion; items 3 to 5 are factual corrections.

None of these corrections weaken the paper. Item 1 makes the central finding stronger
and more specific, and item 2 removes a number that cannot survive scrutiny and
replaces it with one that can.

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
result: reciprocity is 26.60 per cent against a chance expectation of 0.0785 per cent,
a ratio of **338.8x**, not 36x. The reciprocal edge count, 4,014,518, is unchanged and
has since been reproduced by three independent implementations.

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
preserves in-degree and out-degree exactly (40 nulls, this repository). It survives
with the sign preserved in 8 of 8 classes and no null out of 40 reaching the real value
in any class. Under that null the spread between extremes is 283x rather than 991x, and
the ordering within the depleted group shifts: olfactory rather than visual is the most
depleted class. Both figures are reported; the degree-preserving one is the defensible
one, because part of the density-based spread was attributable to the degree sequence.

## 3. The amplification ratio reported as 1,559x

This value appears nine times in the published version, including the abstract. It is
a quotient whose denominator is 0.0005 with a standard deviation of 0.0003, that is, a
dispersion of 60 per cent of its own mean. Within one standard deviation of that
denominator the quotient ranges from about 1,041x to about 4,164x, so the value is not
determined to better than a factor of four by its own control.

The trajectory confirms the diagnosis: between t = 80 and t = 195 the ratio grows from
6.1x to 1,559x while the numerator moves only from 0.68 to 0.83. The growth is the
control decaying toward zero, not the real system separating further.

The quotient is withdrawn and replaced by the **difference, 0.832 on a [0, 1] range**,
which is a large effect and does not depend on dividing by a quantity near its
numerical floor. Quotients are additionally reported at t = 60 (1.3x) and t = 80 (6.1x),
where the denominator is measurable, with an explicit statement that beyond t = 120 the
control is at the numerical floor and the quotient is not interpretable.

The ratios in Table 1 have the same defect, with denominators of 1.0e-7 and 7.3e-8 and
a single control. The paper already labelled them descriptive and not statistically
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

## 5. Pinned data, and two smaller items

The annotation table was fetched from a live branch and has since changed. Methods
should read: annotations pinned to commit
17fc57722002e1a7d38cdd0c89ac382bf92718da, md5 719904abad876c68ace1b5690c9b9b63.
The v783 version string pins the connectome only. See METHODS.md for the measured
drift.

Two further corrections:

1. The swap acceptance rate is **98.5 per cent**, as stated in this paper. A companion
   document states 100 per cent, which is not attainable under the stated constraints
   and is the value that requires correction. The swap target, 45,275,949, is correct
   and has been reproduced.
2. The reference given as Barsotti et al. (2026), Cascades and convergence, PLOS Complex
   Systems, carries the wrong author list. The same title and journal appear elsewhere
   as Betzel, Puxeddu, Seguin and Misic (2026), 3(3), e0000091. The author list requires
   verification against the published article before the erratum is filed.

## What is not corrected

The effective membrane time constant is reported as 1/tau = 8.4 steps. For the update
used, h <- (1 - tau) h + tau tanh(.), the effective constant is -1 / ln(1 - tau) = 7.89
steps, a 6.5 per cent difference. Both values fall inside the physiological range for
Drosophila and no conclusion depends on the difference, but the derivation is incorrect
and is corrected in this repository for future work.
