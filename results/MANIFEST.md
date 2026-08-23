# Evidence manifest

This file records what was measured, where it ran, and the checksum of each artefact,
so that a file arriving in this directory can be verified against the run that produced
it rather than trusted.

## Structural nulls

Ran on a Kaggle CPU worker (no GPU), 180.6 minutes, status complete.

| Artefact | md5 | Bytes | In this repository |
| --- | --- | --- | --- |
| nulls40.json | 38bf1fcadaf37a3b125f83d22b6f4d8e | 191,443 | not yet |
| nulls40.log | a927ece0a08085718815e50c4bfcd08c | 5,850 | not yet |

`nulls40.json` contains, for the real graph and for each of the 40 nulls: the reciprocal
edge count, the unique edge count, per-null in-degree and out-degree mismatch counts,
and three 16x16 group-by-group matrices (edges, excitatory edges, synapses). Every
number in the README and in docs/ERRATUM.md item 2 is recomputable from it with
`src/analyze_nulls40.mjs`, including the numbers that contradict earlier drafts.

## Embedded line

Ran on a Kaggle CPU worker, 98.3 minutes, status complete. Six models at a matched
parameter budget of about 1,400, four tasks, ten seeds each.

| Artefact | md5 | Bytes | In this repository |
| --- | --- | --- | --- |
| dualbrain_bench.json | 1025d60b4e9521d7e4a21ed282935049 | 31,527 | not yet |
| dualbrain_bench.log | e7aac964c9a5c7cc6553308bbce62af7 | 9,895 | not yet |

The gate ablation is positive on all four tasks (21.85x to 108.11x). The frequency
response shows a 31.2x spread in the -3 dB cutoff across the eight dimensions of the
memory state, so the filter bank is not decorative.

**The result that must not be lost when this is written up:** on MultiCue, the two-reference
task, DualBrain loses to GRU (0.42x), LSTM (0.25x) and MinGRU (0.59x), with Cohen's d
from 2.18 to 2.97 against it. That belongs in Limitations with the numbers attached. A
reviewer running two references finds it in an afternoon.

## Why these four files are not in this commit

They were produced on a Kaggle worker and are held in an execution environment that has
network access but no credential permitting a write to this repository. Emitting them
by transcription instead of by transfer would produce files that look like the evidence
without being byte-identical to it, which is worse than an honest gap: the checksums
above would not match and nobody could tell whether the run or the transcription was at
fault.

The checksums are published here first, deliberately. When the files land, they can be
verified against a manifest that predates them.
