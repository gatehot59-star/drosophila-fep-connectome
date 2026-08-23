# Evidence manifest

This file records what was measured, where it ran, and the checksum of each artefact, so
that a file arriving in this directory can be verified against the run that produced it
rather than trusted.

## Structural nulls, degree-preserving (Maslov-Sneppen)

Ran on a Kaggle CPU worker (no GPU), 180.6 minutes, status complete. 40 nulls, 3E swaps
each, in-degree and out-degree verified against the original for all 138,639 nodes on
every null: 0 mismatches, 0 multi-edges, unique edge count exactly 15,091,983 throughout.

| Artefact | md5 | Bytes | In this repository |
| --- | --- | --- | --- |
| nulls40.json | 38bf1fcadaf37a3b125f83d22b6f4d8e | 191,443 | not yet |
| nulls40.log | a927ece0a08085718815e50c4bfcd08c | 5,850 | not yet |
| nulls40_local_js.log | 2f56f1bbf11fd5c46eb8ab09c1ac68e6 | 3,358 | **yes** |

The JavaScript log is an independent replication: different language, different machine,
different seeds, different swap-accounting convention. Null means differ by 0.8 per cent
and the verdict is identical, 0 of 40 nulls reaching the observed value in both.

## Structural nulls, community-preserving

Ran on a Kaggle CPU worker, 22.2 minutes, status complete. 40 nulls. These preserve
degree **and** the super-class connectivity matrix, so they ask whether a result exceeds
what modular architecture explains. In-degree verified per null: 0 mismatches.

This family admits multi-edges by construction, unlike Maslov-Sneppen: 149,120 to 150,406
per null, counted and reported.

| Artefact | md5 | Bytes | In this repository |
| --- | --- | --- | --- |
| cp40.json | not recorded at run time | ~190,000 | not yet |

One finding from this run is a correction to the repository's own method, recorded here
because it cost compute to learn: the sensory-to-motor routing statistic is **conserved**
under this null (standard deviation exactly zero, ratio exactly 1.000). The null shuffles
targets within super-class blocks and the motor group is defined by super-class, so the
quantity cannot move. A test whose null has zero variance is a tautology, not a
measurement, and it is reported as NOT TESTABLE rather than as a ratio of 1.000.

## Twelve-pair global test

Ran on a Kaggle CPU worker, 9.8 minutes, status complete. 21 additional
community-preserving nulls bringing the total to 40, which moves the two-sided
permutation floor from 0.10 to 0.0488.

| Artefact | md5 | Bytes | In this repository |
| --- | --- | --- | --- |
| nulls21_global12.log | d4340415c5e5438a7ebfff9709bbefaa | 8,027 | **yes** |
| nulls21_global12.json | f0d9bf252f02c1432416a61b5dfe333e | 52,765 | not yet |

The log includes the port validation: the original 19 nulls were produced by a JavaScript
engine and this run is Python, so seeds 42 and 2042 were reproduced first and all 24
metrics compared against the original values. Worst absolute difference 1.055e-14, which
is double-precision rounding.

## Dual null families on the same connectome

Ran on a Kaggle CPU worker, 136.9 minutes, status complete. 19 community-preserving plus
19 degree-preserving nulls, with the dynamic and static measurements of the companion
paper computed against both.

| Artefact | md5 | Bytes | In this repository |
| --- | --- | --- | --- |
| nulls19_cp_ms.txt | 8d678da04954b4ab8fc8a4760de6c7e8 | 8,060 | **yes** |

## Embedded line: architecture benchmark

Ran on a Kaggle CPU worker, 98.3 minutes, status complete. Six models at a matched
parameter budget of about 1,400, four tasks, ten seeds each.

| Artefact | md5 | Bytes | In this repository |
| --- | --- | --- | --- |
| dualbrain_bench.json | 1025d60b4e9521d7e4a21ed282935049 | 31,527 | not yet |
| dualbrain_bench.log | e7aac964c9a5c7cc6553308bbce62af7 | 9,895 | not yet |

The gate ablation is positive on all four tasks (21.85x to 108.11x). The frequency
response shows a 31.2x spread in the -3 dB cutoff across the eight dimensions of the
memory state, so the filter bank is not decorative.

## Embedded line: the two-reference task, re-measured

Ran on a Kaggle CPU worker, 51.6 minutes, status complete. Nine configurations at ten
seeds each: six values of h_m with h_r rebalanced to hold the parameter budget, plus
LSTM, GRU and MinGRU as fixed references at the same budget.

| Artefact | md5 | Bytes | In this repository |
| --- | --- | --- | --- |
| multicue_hm_sweep.log | e9717a3fec8f720904653548005919de | 1,520 | **yes** |
| hm_sweep.json | 8c18930f204f0a48db9b3f6dd34fcf92 | 3,601 | not yet |

**This run corrects a figure in the architecture benchmark above.** That benchmark
reported MSE 0.000326 on the two-reference task, 4.05x worse than LSTM. The sweep shows
that value is the worst point of a curve with a 3.44x spread and an interior optimum at
h_m=10, where the figure is 0.000095 and 1.18x. Welch between the two: t=6.13,
p=8.59e-10.

Both available explanations are refuted by the same curve. It is not monotonic, so
"insufficient memory" is wrong. It varies by 3.44x, so "the architecture is indifferent
here" is wrong. The mechanism is visible in the h_r column: the budget is fixed, so
raising h_m starves the reactive pathway, and at h_m=16 h_r falls to 6. The trade is
memory against reflex, and the optimum is a property of that split rather than of either
pathway alone.

**The number that should be reported** is the optimum with its qualification, not a single
blind-search point: performance on two simultaneous references depends strongly on the
reactive-to-memory split, and at the optimum the model remains 1.18x above an LSTM at
matched parameters.

## Why some artefacts are not in this repository

The JSON files marked "not yet" were produced on Kaggle workers and are held in an
execution environment that has network access but no credential permitting a write here.
Emitting them by transcription rather than by transfer would produce files that resemble
the evidence without being byte-identical to it, which is worse than an honest gap: the
checksums above would not match and nobody could tell whether the run or the
transcription was at fault.

The checksums are published first, deliberately. When the files land, they can be verified
against a manifest that predates them. Every log file marked **yes** has been verified
byte-identical to its run output after committing.
