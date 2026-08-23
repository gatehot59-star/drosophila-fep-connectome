# drosophila-fep-connectome

Canonical location: https://github.com/gatehot59-star/drosophila-fep-connectome

Analysis code and raw evidence for signal routing and structural specificity in the
*Drosophila melanogaster* connectome (FlyWire v783), and for the embedded DualBrain
inference line derived from it.

Companion code to Mendieta (2026a), *Signal propagation properties in the Drosophila
melanogaster connectome*, Zenodo. **See [docs/ERRATUM.md](docs/ERRATUM.md) before using
any number from the published version.**

## What this repository claims, and what it does not

The measurements here are split into two layers with very different robustness. The
split is not cosmetic: it is the main methodological result.

| Layer | Depends on | Effect of changing the analysis choices |
| --- | --- | --- |
| **Structural** (pure counts on the raw matrix) | nothing: no normalisation, no tau, no entropy estimator, no propagation | none. A count has no free parameters |
| **Dynamic** (lambda_F, retention asymmetry R, entropy, temporal RDI) | five free choices, all defensible | severe. R crosses 1 depending on normalisation; lambda_F varies 3x |

Everything in `results/nulls40.json` is structural. The dynamic results of the companion
papers are reported as a **negative methodological result**, not as a validated model.

## Headline structural results

All tested against **40 Maslov-Sneppen nulls** that preserve in-degree and out-degree
exactly (verified: 0 degree mismatches across 138,639 neurons in all 40 nulls, and no
multi-edges created). `p = 0.0244` is the permutation floor with n = 40, i.e. no null
out of 40 matched or exceeded the real value.

| Measurement | Real | Null mean +- sd | Ratio | p |
| --- | --- | --- | --- | --- |
| Reciprocal edges | 4,014,518 | 84,932 +- 401 | **47.3x** | 0.0244 |
| Kenyon cell -> MBON edges | 62,261 | 2,568 +- 48 | **24.3x** | 0.0244 |
| Dopaminergic -> Kenyon cell | 47,404 | 1,735 +- 39 | **27.3x** | 0.0244 |
| Sensory -> Kenyon cell (direct) | **0** | 1,533 to 2,640 | **0.00x** | 0.0244 |
| MBON -> motor | 364 | 891 +- 34 | 0.41x | 0.0244 |

### Sensory-to-motor routing hierarchy

Excitatory edges from each sensory class to motor neurons, against the degree-preserving
null. Sign is preserved in 8 of 8 classes; the spread between extremes is **283x**.

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
first build a scene or an odour identity are depleted. This is a routing hierarchy
aligned with behavioural urgency, not uniform frugality.

### Plastic fraction of the brain

The canonical plasticity circuit (Kenyon cells, MBONs, DANs, MBINs) is **5,608 of 138,639
neurons = 4.045%**, and the canonical plasticity site (KC -> MBON) is **62,261 of
15,091,983 edges = 0.41%**, carrying **0.47% of the 54,492,922 synapses**.

Two consequences, and they point the same way: the learning centre is small, and it is
also **wired shut**. No sensory neuron connects directly to a Kenyon cell anywhere in
this brain (exactly zero edges, where the degree-preserving null places 1,533 to 2,640),
and MBON output to motor neurons is depleted 0.41x. What the circuit can learn about and
what it can act on are both fixed by structure.

## Layout

```
src/nulls40_structural.py    the 40-null experiment, as run on Kaggle CPU (180.6 min)
src/analyze_nulls40.mjs      statistics over results/nulls40.json
src/routing_hierarchy.mjs    the routing table and its range
results/nulls40.json         raw output: real plus 40 nulls, 16x16 group matrices
results/nulls40.log          verbatim run log with per-null invariant checks
results/dualbrain_bench.*    embedded line: 6 models, 4 tasks, 10 seeds, gate ablation
results/MANIFEST.md          checksums and current push state of the evidence files
docs/METHODS.md              exact data provenance, pinned SHA, checksums
docs/ERRATUM.md              corrections to the published version of Mendieta (2026a)
```

## Reproducing

See [docs/METHODS.md](docs/METHODS.md). The short version: the annotation file is pinned
to a commit SHA, not to a branch. Pinning is not optional here, because the file on the
live branch changed between March and August 2026. Details and the exact drift are in
METHODS.

## Licence

GPLv3 for this analysis code. The embedded inference engine and network topologies are
dual-licensed GPLv3 plus commercial; contact the author for commercial terms. Note that
the published paper states AGPL v3, which is superseded by this repository and recorded
in the erratum.
