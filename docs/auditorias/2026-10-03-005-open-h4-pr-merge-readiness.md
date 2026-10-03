# Audit: merge readiness of all open H4 PRs

**Date:** 2026-10-02 ART / 2026-10-03 UTC  
**Repository:** `gatehot59-star/drosophila-fep-connectome`  
**Current `main`:** `37ebd6d28fddd64ffebff0e9738b3c26787e4b8b`  
**Scope:** open H4 materialization PRs #7 through #12. PR #2 is excluded: it is the older two-hop anatomical-null line, not the H4 alignment/loader/features/null/generalization chain.

## Executive verdict

**None of the six open H4 PRs is TITAN-merge-ready today.** All six report `mergeable_state=clean`, but that only says GitHub sees no textual conflict against each PR's recorded base. The chain is stacked, PR #7 is based on an older `main`, PR #10 has zero individual check runs, and all six have no external review. The code paths were independently executed in `brain-env` in cumulative order and passed, but independent execution is not a substitute for an up-to-date base and review.

## Readiness matrix

| PR | Head | Base | Checks | Reviews | Independent sweep | Readiness | Blocking reason |
|---:|---|---|---:|---|---|---|---|
| [#7](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/7) | `ff48bedc` | `main@1fd25b6` | 2 success | none | 7/7 OK | **HOLD** | base is behind current `main@37ebd6d`; no review |
| [#8](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/8) | `59cf00fa` | #7 head | 1 success | none | 13/13 OK | **HOLD** | stacked on #7; no review |
| [#9](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/9) | `a92e689b` | #8 head | 1 success | none | 20/20 OK | **HOLD** | stacked on #8; no review |
| [#10](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/10) | `5ec2e914` | #9 head | 0 | none | 25/25 OK | **BLOCKED** | no PR check run; no review |
| [#11](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/11) | `7cfa54e5` | #10 head | 1 success | none | 29/29 OK | **HOLD** | stacked on #10; no review |
| [#12](https://github.com/gatehot59-star/drosophila-fep-connectome/pull/12) | `bb5d949f` | #11 head | 1 success | none | 34/34 OK | **HOLD** | top of an unmerged stack; no review |

## Stack topology

```text
main@37ebd6d
  #7  alignment guard
    #8  official loader
      #9  ROI-preserving features
        #10 block-preserving null
          #11 leave-one-trial-out generalization
            #12 temporal halves
```

The merge order is therefore #7 → #8 → #9 → #10 → #11 → #12, unless the branches are rebased/retargeted into a single integration PR. Do not merge a child into its parent branch and assume the result is protected by `main`; the parent still needs to land first.

## Evidence checked

- GitHub PR metadata, head/base SHAs, mergeability and changed-file counts for all six PRs.
- Individual check runs, not only combined status: #7 has 2 successful runs; #8, #9, #11 and #12 have 1 successful run each; #10 has 0.
- Review state: all six return no reviews. Silence is **NO MEDIDO**, not approval.
- Independent `brain-env` execution at each head:
  - #7: alignment guard, 7 tests.
  - #8: alignment + official loader, 13 tests.
  - #9: alignment + loader + features, 20 tests.
  - #10: alignment + loader + features + block null, 25 tests.
  - #11: previous 25 + generalization, 29 tests.
  - #12: previous 29 + temporal halves, 34 tests.
- The H4 scientific claims remain correctly bounded: H4 strong is **NO MEDIDA**; no PR is being treated as causal or anatomical proof.

## Required actions before merge

1. Update #7 against current `main@37ebd6d`, rerun its check, and obtain an independent review.
2. Merge or retarget the chain in order; after each parent lands, refresh the child base and rerun checks.
3. Add a check-producing workflow for #10's block-null contracts, or explicitly attach equivalent CI evidence to that PR. Its local tests pass, but GitHub has no check run for it.
4. Run one full regression check on the final integrated head. The current workflows are incremental: later PR checks do not rerun every earlier suite.
5. Keep the scientific merge boundary explicit: merging the instruments does not merge H4 as a biological finding.

## TITAN scorecard

| Role | Score | Loops | Observation |
|---|---:|---:|---|
| GITHUB | 10/10 | 0 | All six open H4 PRs, exact heads/bases, checks, reviews and stack order read live. |
| QA AUDITOR | 9/10 | 0 | Independent cumulative execution passed; merge remains blocked by stale base, missing check coverage and missing review. |
| **Total** | **95/100** | **0** | Audit passes; no PR is approved for merge yet. |

--- METODO TITAN ---
Accion delicada: NO; audit only, no merge, no branch retarget, no code change.
Modo aplicado: TITAN FULL
Rubrica: 95/100 for the audit deliverable; PR readiness is reported separately per matrix.
N/A declarados: production security, deployment, ABI and product performance do not apply to a merge-readiness audit of scientific Python instruments.
Review externo: no reviews present on the six PRs; state NO MEDIDO, not approval.
Instrument: GitHub PR metadata/check runs/reviews/files plus brain-env independent cumulative test sweep; raw test outputs were observed in the runner.
