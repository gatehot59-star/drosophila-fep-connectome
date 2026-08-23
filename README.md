# drosophila-fep-connectome

Canonical location: https://github.com/gatehot59-star/drosophila-fep-connectome

Analysis code and raw evidence for signal routing and structural specificity in the
*Drosophila melanogaster* connectome (FlyWire v783), and for the embedded DualBrain
inference line derived from it.

Companion code to Mendieta (2026a), *Signal propagation properties in the Drosophila
melanogaster connectome*, Zenodo. **See [docs/ERRATUM.md](docs/ERRATUM.md) before using
any number from the published version.**

The connectome and its annotations are not this author's work. See
[docs/CITATION.md](docs/CITATION.md) for the four references their authors require and
for the full provenance of the connectivity matrix.

## What matters is which null model a result is tested against

There are two null families in use here, and they answer different questions:

| Null | Preserves | Destroys | Question it answers |
| --- | --- | --- | --- |
| **MS** (Maslov-Sneppen) | in-degree and out-degree, exactly | block structure, modularity | is this more than the degree sequence? |
| **CP** (community-preserving) | degree **and** the super-class connectivity matrix | fine wiring within and between blocks | is this more than the modular architecture? |

CP is the harder test. A result that separates against MS but not against CP is **not
refuted**: it means the modular architecture accounts for it, which is a finding, not a
loss. Those two verdicts are reported separately below and never merged into one.

`p = 0.05` with n = 19 nulls and `p = 0.0244` with n = 40 are permutation **floors**: they
mean no null reached the real value, not that p equals that number.

## Results, one row per measurement

| Measurement | Real | vs CP | vs MS | Verdict |
| --- | --- | --- | --- | --- |
| **Dynamic RDI, t = 80** | 0.65522 | **3.051x**, z 79.9, 0/19 | **5.921x**, z 13.3, 0/19 | survives both |
| **Dynamic RDI, t = 200** | 0.742355 | **3.496x**, z 15.0, 0/19 | **110.694x**, z 197.0, 0/19 | survives both |
| Dynamic RDI, t = 30 / 60 / 100 / 140 | 0.099 / 0.216 / 0.694 / 0.740 | 2.6x to 3.4x, 0/19 | 5.4x to 30.8x, 0/19 (t=30: 1/19) | survives both |
| Spectral radius rho | 0.989886 | 2.186x, **2/19**, p 0.15 | 4.597x, z 21.3, 0/19 | MS only; modularity accounts for it |
| One-hop RDI | 0.40144 | **0.906x**, 19/19, p 1.0 | 3.918x, z 5.6, 0/19 | MS only; CP nulls score *higher* |
| One-hop RDI, >= 5 synapses | 0.753272 | 0.988x, 19/19 | 4.1x, z 6.3, 0/19 | MS only |
| Reciprocal edges | 4,014,518 | *not tested* | **47.3x**, 0/40 | degree only; modularity **unmeasured** |
| Kenyon cell -> MBON | 62,261 | *not tested* | **24.25x**, 0/40 | degree only; modularity **unmeasured** |
| Dopaminergic -> Kenyon cell | 47,404 | *not tested* | **27.33x**, 0/40 | degree only; modularity **unmeasured** |
| Sensory -> Kenyon cell, direct | **0** | *not tested* | 0.00x, 40/40 | degree only; modularity **unmeasured** |
| MBON -> motor | 364 | *not tested* | 0.41x, 40/40 | degree only; modularity **unmeasured** |
| Sensory-to-motor routing, 8 classes | see below | *not tested* | sign preserved 8/8, 0/40 each | degree only; modularity **unmeasured** |
| Distribution **shape** after decay, 12 pairs, global test | S = 67 of 240 | **1st of 20 graphs**, 0/19, p 0.10 two-sided | *not tested* | direction is post-hoc; needs n >= 39 |
| Distribution **scale** after decay, 12 pairs | S = 240 of 240 | worst of 20 in **12/12** pairs | *not tested* | separates perfectly, in the **opposite** direction to the published claim |
| Retention asymmetry R | 1.31 reported | — | — | fails for a different reason: crosses 1 depending on normalisation (1.879 to 0.811) |
| lambda_F | — | — | — | varies 3x across normalisation schemes |

**The rows marked *not tested* are the honest label for a real gap.** The 40 nulls behind
them are MS. Reciprocity in particular is largely intra-block, so a CP null could
reproduce a meaningful share of it. How much is unknown and is not estimated here.

### Sensory-to-motor routing hierarchy

Excitatory edges from each sensory class to motor neurons, against 40 degree-preserving
nulls. Sign preserved in 8 of 8 classes, no null of 40 reaching the real value in any
class, spread between extremes **283x**.

| Class | N | Ratio vs null | Verdict |
| --- | --- | --- | --- |
| olfactory | 2,279 | 0.034x | depleted |
| hygrosensory | 74 | 0.103x | depleted |
| visual | 10,855 | 0.145x | depleted |
| thermosensory | 29 | 0.236x | depleted |
| gustatory | 408 | 2.193x | enriched |
| unknown sensory | 131 | 6.709x | enriched |
| ascending (AN) | 2,231 | 7.407x | enriched |
| mechanosensory | 2,656 | 9.693x | enriched |

Pathways that must reach muscle within milliseconds are enriched; pathways that must
first build a scene or an odour identity are depleted. A routing hierarchy aligned with
behavioural urgency, not uniform frugality.

### Plastic fraction of the brain

The canonical plasticity circuit (Kenyon cells, MBONs, DANs, MBINs) is **5,608 of 138,639
neurons = 4.045%**, and the canonical plasticity site (KC -> MBON) is **62,261 of
15,091,983 edges = 0.41%**, carrying **0.47% of the 54,492,922 synapses**.

The learning centre is also wired shut at both ends: no sensory neuron connects directly
to a Kenyon cell anywhere in this brain (exactly zero edges, where the degree-preserving
null places 1,533 to 2,640), and MBON output to motor neurons is depleted 0.41x. Subject
to the *not tested* caveat above.

## Two dependencies that no null model addresses

Both of these sit upstream of every table here and are not fixed by adding nulls.

1. **Excitatory counts inherit an assumption.** They rest on the
   `Excitatory x Connectivity` column, which is an excitatory/inhibitory assignment from
   the Shiu et al. model derived from neurotransmitter predictions, not a FlyWire
   measurement. A count has no analysis parameters; it is not free of its input's
   assumptions. See [docs/CITATION.md](docs/CITATION.md).
2. **Entropy results depend on the estimator.** Histogram and KDE estimators over the
   same activations invert the conclusion in this dataset. The estimator used here is a
   50-bin histogram, which is a choice and is stated as one in
   [docs/METHODS.md](docs/METHODS.md).

## Layout

```
src/nulls40_structural.py       the 40-null MS experiment, as run on Kaggle CPU (180.6 min)
src/analyze_nulls40.mjs         statistics over results/nulls40.json
src/routing_hierarchy.mjs       the routing table and its range
results/nulls40.json            raw output: real plus 40 MS nulls, 16x16 group matrices
results/nulls40.log             verbatim run log with per-null invariant checks
results/nulls40_local_js.log    independent replication in JavaScript, different seeds
results/dualbrain_bench.*       embedded line: 6 models, 4 tasks, 10 seeds, gate ablation
results/MANIFEST.md             checksums and current push state of the evidence files
docs/METHODS.md                 provenance, the two annotation pins, and the null models
docs/CITATION.md                the four required data citations and the full input chain
docs/ERRATUM.md                 corrections to the published version of Mendieta (2026a)
```

## Reproducing

See [docs/METHODS.md](docs/METHODS.md). Pin the annotations to a **tagged release**, not
a branch, and note that there are two pins depending on what you want to reproduce.
Release **v3.0.0** reproduces the published paper (139,244 rows); release **v3.1.0**
reproduces the null analysis here (139,248 rows).

The MS experiment has been run twice independently, in Python on a Kaggle worker and in
JavaScript on a different machine with different seeds and a different swap-accounting
convention. Null means differ by 0.8 per cent (84,932 against 85,626 reciprocal edges),
the cause is visible in the logs, and the verdict is identical in both: 0 of 40 nulls
reach the real value. Both logs are in `results/`.

## Licence

GPLv3 for this analysis code. The embedded inference engine and network topologies are
dual-licensed GPLv3 plus commercial; contact the author for commercial terms. Note that
the published paper states AGPL v3, which is superseded by this repository and recorded
in the erratum.

The input data is third-party, carries no declared licence, and is not redistributed
here. See [docs/CITATION.md](docs/CITATION.md).
