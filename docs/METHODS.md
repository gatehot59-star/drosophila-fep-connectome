# Methods and data provenance

## Why this file exists

The published paper cites FlyWire v783. That version string pins the **connectome** and
does not pin the **annotations**, which are versioned separately and were revised after
the analysis run. Anyone reproducing the published numbers without the right annotation
version gets different population sizes and cannot close the figures to the digit, and a
reviewer who cannot reproduce the counts will reasonably assume the error is the
author's.

The annotation authors anticipated this. Their README says, at the top:

> Annotations in this repository have been updated since the initial FlyWire preprint.
> Please see the tagged release for versions matching specific publications.

The failure was not reading that. The fix is a tag, not a branch.

See [CITATION.md](CITATION.md) for the four references the annotation authors require and
for the full provenance chain of the connectivity matrix, which has more links than the
paper states.

## Which annotation version reproduces what

Row counts and checksums measured directly from each tagged release:

| Release | Date | Rows | md5 | Reproduces |
| --- | --- | --- | --- | --- |
| v2.1.0 | 2024-07-30 | 139,255 | 8527e0a95ed5f112766b13260a91e8e2 | Schlegel et al. (2024). **Not used by either analysis here** |
| **v3.0.0** | 2025-10-09 | **139,244** | 16ee17446c428bd27cf2bdefb83af4fd | **The published paper.** Matches its March 2026 count at the digit |
| **v3.1.0** | 2026-07-21 | **139,248** | 719904abad876c68ace1b5690c9b9b63 | **The 40-null analysis in this repository** |

Two pins, not one, because the two analyses ran on different versions:

- **To reproduce the published paper: pin v3.0.0.** An earlier draft of this file gave a
  commit SHA of `17fc5772` for that purpose. That was wrong: `17fc5772` is
  byte-identical to v3.1.0 (same md5), which is the version the null analysis ran on,
  not the paper's.
- **To reproduce `results/nulls40.json`: pin v3.1.0**, which is what
  `src/nulls40_structural.py` does.

The v3.1.0 checksum was verified independently on two machines, a local container and a
Kaggle CPU worker, both returning `719904abad876c68ace1b5690c9b9b63`.

## What differs between the two versions, and whether it matters here

This needs stating plainly rather than waiting for a reader to find it: the v3.1.0
changelog records a **complete retyping of Johnston's Organ**, which is a
mechanosensory structure, and **mechanosensory carries the strongest claim in this
repository** (9.693x enrichment in motor access).

Measured class by class, v3.0.0 against v3.1.0:

| Class | v3.0.0 | v3.1.0 | Delta | Relative |
| --- | --- | --- | --- | --- |
| mechanosensory | 2,671 | 2,668 | -3 | 0.11% |
| visual | 11,391 minus 6 = 11,385 | 11,391 | +6 | 0.05% |
| olfactory, gustatory, hygrosensory, thermosensory, AN, unknown sensory | unchanged | unchanged | 0 | 0 |
| Kenyon_Cell, MBON, DAN, ALPN | unchanged | unchanged | 0 | 0 |

No cell class was added or removed. The Johnston's Organ retyping operates at
`cell_type` granularity, which is finer than the `cell_class` grouping this analysis
uses, so it moves three neurons at class level. **The class-level results stand, and the
reason they stand is measured rather than asserted.** An analysis keyed on `cell_type`
rather than `cell_class` would not get off this lightly.

## Exact inputs as used by the null analysis

| File | Source | Checksum (md5) | Bytes |
| --- | --- | --- | --- |
| connectivity.parquet | eonsystemspbc/fly-brain, data/2025_Connectivity_783.parquet | 3d802fd542b5d18570ba1ba0bb0abed9 | 100,804,642 |
| annotations.tsv | flyconnectome/flywire_annotations, release v3.1.0 | 719904abad876c68ace1b5690c9b9b63 | 31,718,505 |

Graph as loaded: N = 138,639 neurons, E = 15,091,983 unique directed edges, 54,492,922
synapses (sum of the `Connectivity` column), density = 0.000785197. Annotation rows
mapped onto graph nodes: 138,625 of 139,248; 14 graph nodes carry no annotation.

Neither source repository declares a licence, so no data is redistributed here. See
[CITATION.md](CITATION.md).

## Null model

Maslov-Sneppen double-edge swap, 3E target swaps per null, 40 nulls, seeds 4200 + 17i
for i in 0..39. Constraints enforced per swap: no self-loops, no multi-edges, and no
reuse of an edge within a batch.

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
number of nulls at least as extreme as the real value. With n = 40 the attainable floor
is 0.0244. **A reported p of 0.0244 means no null out of 40 reached the real value; it
is not a measurement that p equals 0.0244.**

Multiple comparisons: 40 nulls support a single global test, or a small number of
pre-registered tests. They do **not** support twelve separate tests at a Bonferroni
threshold of 0.00417, which would require n >= 239. Where twelve pairs are of interest,
the correct instrument is one global statistic over the twelve, not twelve tests with a
corrected threshold.

Z-scores are reported for direction and are not interpretable as effect sizes: the null
distributions here have very small variance, so a z of several hundred reflects a tight
null rather than an extraordinary effect. Ratios and the count of nulls exceeding the
real value are the reportable quantities.

## Reproducing

```
# structural nulls: 180.6 min on a Kaggle CPU worker, no GPU
python src/nulls40_structural.py        # writes nulls40.json
node   src/analyze_nulls40.mjs          # the statistics tables
node   src/routing_hierarchy.mjs        # the routing table and its range
```

The script downloads both inputs on first run and prints their md5 before doing any
work. If either checksum differs from the table above, stop: the inputs are not the ones
these results were computed from.
