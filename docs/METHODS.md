# Methods and data provenance

## Why this file exists

The published paper cites FlyWire v783. That version string pins the **connectome**
and does not pin the **annotations**. The annotation table is served from a live branch
and it changed after the March 2026 analysis run. Anyone reproducing the published
numbers from the live branch gets different population sizes and cannot close the
figures to the digit. The drift is small in magnitude and changes no conclusion, but a
reviewer who cannot reproduce the counts will assume the error is the authors.

## Exact inputs

| File | Source | Checksum (md5) | Bytes |
| --- | --- | --- | --- |
| connectivity.parquet | eonsystemspbc/fly-brain, data/2025_Connectivity_783.parquet | 3d802fd542b5d18570ba1ba0bb0abed9 | 100,804,642 |
| annotations.tsv | flyconnectome/flywire_annotations at SHA 17fc57722002e1a7d38cdd0c89ac382bf92718da | 719904abad876c68ace1b5690c9b9b63 | 31,718,505 |

The annotation URL used by the analysis scripts is pinned to that commit SHA, not to
the main branch. Verified twice on independent machines (a local container and a Kaggle
CPU worker), both returning md5 719904abad876c68ace1b5690c9b9b63.

Graph as loaded: N = 138,639 neurons, E = 15,091,983 unique directed edges,
54,492,922 synapses (sum of the Connectivity column), density = 0.000785197.
Annotation rows mapped onto graph nodes: 138,625 of 139,248; 14 graph nodes carry no
annotation.

## The annotation drift, measured

March 2026 run against 23 August 2026, same URL on the live branch:

| Quantity | March 2026 | 23 Aug 2026 | Delta |
| --- | --- | --- | --- |
| total TSV rows | 139,244 | 139,248 | +4 |
| flow: afferent | 19,259 | 19,262 | +3 |
| super_class: sensory | 16,904 | 16,907 | +3 |
| cell_class: visual | 11,385 | 11,391 | +6 |
| cell_class: mechanosensory | 2,671 | 2,668 | -3 |
| visual population stimulated | 10,852 | 10,854 | +2 |

Cause, resolved against the GitHub commit history for the file: three commits landed
after the analysis run, on 28 April 2026 (two) and 4 May 2026 (annotation fixes). The
drift is 0.003 per cent and changes no conclusion in either paper.

## Null model

Maslov-Sneppen double-edge swap, 3E target swaps per null, 40 nulls, seeds
4200 + 17i for i in 0..39. Constraints enforced per swap: no self-loops, no
multi-edges, and no reuse of an edge within a batch.

Preserved by construction and **verified per null**, not assumed:

- in-degree of all 138,639 nodes: 0 mismatches in 40 of 40 nulls
- out-degree of all 138,639 nodes: 0 mismatches in 40 of 40 nulls
- unique edge count exactly 15,091,983: 40 of 40 nulls
- realised swaps per null: 46,288,240 to 46,307,400 against a 45,275,949 target

A swap acceptance rate below 100 per cent is a consequence of the constraints, not a
defect: proposals that would create a self-loop or a duplicate edge must be rejected.
Measured acceptance was 98.5 per cent. A reported rate of exactly 100 per cent is not
attainable under these constraints and indicates either different constraints or a
different counting convention.

## Statistics

Permutation p-values are two-sided and reported as (k + 1) / (n + 1) where k is the
number of nulls at least as extreme as the real value. With n = 40 the attainable
floor is 0.0244. **A reported p of 0.0244 means no null out of 40 reached the real
value; it is not a measurement that p equals 0.0244.**

Multiple comparisons: 40 nulls support a single global test, or a small number of
pre-registered tests. They do **not** support twelve separate tests at a Bonferroni
threshold of 0.00417, which would require n >= 239. Where twelve pairs are of
interest, the correct instrument is one global statistic over the twelve, not twelve
tests with a corrected threshold.

Z-scores are reported for direction and are not interpretable as effect sizes: the
null distributions here have very small variance, so a z of several hundred reflects a
tight null rather than an extraordinary effect. Ratios and the count of nulls exceeding
the real value are the reportable quantities.

## Reproducing

```
# structural nulls: 180.6 min on a Kaggle CPU worker, no GPU
python src/nulls40_structural.py        # writes nulls40.json
node   src/analyze_nulls40.mjs          # the statistics tables
node   src/routing_hierarchy.mjs        # the routing table and its range
```

The script downloads both inputs on first run and prints their md5 before doing any
work. If either checksum differs from the table above, stop: the inputs are not the
ones these results were computed from.
