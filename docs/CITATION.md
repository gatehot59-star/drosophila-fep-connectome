# Citing the data this analysis depends on

This repository contains no data. It downloads two inputs at run time, and neither is
the author's work. Both must be cited.

## Annotations: what the data authors ask for

The FlyWire annotation repository states the requirement in its own README:

> Version `>=3.0.0`: Please cite Berg _et al._ (2025), Schlegel _et al._ (2024),
> Matsliah _et al._ (2024) and Dorkenwald _et al._ (2024) when using annotations from
> this repository.

Both versions relevant here (v3.0.0, used by the paper; v3.1.0, used by the null
analysis) are `>= 3.0.0`, so all four apply. In particular **Berg et al. cannot be
omitted**: the version matching Schlegel et al. (2024) alone is v2.1.0, which is not the
version either analysis used.

| Work | Reference |
| --- | --- |
| Connectome | Dorkenwald et al. (2024), *Neuronal wiring diagram of an adult brain*, Nature. doi:10.1038/s41586-024-07558-y |
| Annotations | Schlegel et al. (2024), *Whole-brain annotation and multi-connectome cell typing of Drosophila*, Nature. doi:10.1038/s41586-024-07686-5 |
| Optic lobe annotations | Matsliah et al. (2024), *Neuronal parts list and wiring diagram for a visual system*, Nature. https://www.nature.com/articles/s41586-024-07981-1 |
| Annotations v3.x basis | Berg et al. (2025), *Sexual dimorphism in the complete connectome of the Drosophila male central nervous system*, bioRxiv. doi:10.1101/2025.10.09.680999 |

DOIs above are taken from the BibTeX entries published by the annotation authors, not
reconstructed from titles.

Annotation work is maintained by the Drosophila Connectomics group (Department of
Zoology, University of Cambridge) and collaborators. The pinned commit used here was
authored by Philipp Schlegel.

## Connectivity: a longer provenance chain than the paper states

The connectivity matrix is **not** taken from the primary FlyWire release. It is read
from a third-party re-host, `eonsystemspbc/fly-brain`, which derives from:

> Shiu et al., *A leaky integrate-and-fire computational model based on the connectome of
> the entire adult Drosophila brain reveals insights into sensorimotor processing*,
> bioRxiv. doi:10.1101/2023.05.02.539144

This matters for one specific reason and it should not be buried. The
`Excitatory x Connectivity` column, on which **every excitatory count in this
repository depends**, is a construct of that model: it encodes an excitatory/inhibitory
assignment derived from neurotransmitter predictions. It is not a FlyWire measurement.
So the motor-access table inherits that assignment, and a reader who disputes the
neurotransmitter calls disputes the table.

The honest chain is: FlyWire v783 (Dorkenwald et al.) -> LIF model and E/I assignment
(Shiu et al.) -> re-hosted parquet (eonsystemspbc/fly-brain) -> this analysis. Four
links, and the published paper names one.

## Licensing of the inputs

Measured against the GitHub API on 23 August 2026: **neither**
`flyconnectome/flywire_annotations` nor `eonsystemspbc/fly-brain` declares a licence.

Absence of a licence is not permission. That is why this repository redistributes
nothing and the scripts download from source, and why `results/MANIFEST.md` records
checksums rather than shipping copies of third-party data. The GPLv3 in `LICENSE`
covers the analysis code in this repository and nothing else.
