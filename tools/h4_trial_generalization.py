#!/usr/bin/env python3
"""Measure within-animal leave-one-trial-out ROI-label generalization.

This is a descriptive instrument, not a causal test. It operates on aligned
ROI-preserving bout features and refuses legacy ``Frame`` joins and mixed
animals. The score is balanced accuracy from a nearest-centroid classifier;
the null shuffles complete bout tokens within each target-context segment,
so consecutive frames are never treated as independent observations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from h4_block_null import BlockNullError, TrialData, _normalized, load_trial

SCHEMA = "h4-trial-generalization/v1"
TARGET_LABELS = ("walking", "resting")


@dataclass(frozen=True)
class Observation:
    """One bout-level ROI observation with its original token metadata."""

    label: str
    vector: tuple[float, ...]
    length: int
    segment: int
    order: int


def _observations(trial: TrialData) -> list[Observation]:
    """Return bout observations for one trial."""
    segments = _normalized(trial)
    output: list[Observation] = []
    for segment_index, segment in enumerate(segments):
        cursor = 0
        for order, token in enumerate(segment.tokens):
            end = cursor + token.length
            left, right = segment.prefix[cursor], segment.prefix[end]
            vector = tuple((right[i] - left[i]) / token.length for i in range(len(left)))
            output.append(Observation(token.label, vector, token.length, segment_index, order))
            cursor = end
    return output


def _centroids(observations: Sequence[Observation], labels: Sequence[str]) -> dict[str, tuple[float, ...]]:
    """Fit equal-weight class centroids from bout observations."""
    groups: dict[str, list[tuple[float, ...]]] = {label: [] for label in labels}
    for observation in observations:
        if observation.label in groups:
            groups[observation.label].append(observation.vector)
    if any(not groups[label] for label in labels):
        missing = [label for label in labels if not groups[label]]
        raise BlockNullError(f"training fold lacks labels: {','.join(missing)}")
    return {label: tuple(sum(vector[i] for vector in groups[label]) / len(groups[label]) for i in range(len(groups[label][0]))) for label in labels}


def _predict(vector: Sequence[float], centroids: Mapping[str, Sequence[float]]) -> str:
    """Predict the nearest centroid using squared Euclidean distance."""
    return min(centroids, key=lambda label: sum((vector[i] - centroids[label][i]) ** 2 for i in range(len(vector))))


def balanced_accuracy(observations: Sequence[Observation], centroids: Mapping[str, Sequence[float]], labels: Sequence[str]) -> float:
    """Compute macro recall over labels present in the evaluated bouts."""
    recalls: list[float] = []
    for label in labels:
        group = [observation for observation in observations if observation.label == label]
        if not group:
            continue
        recalls.append(sum(_predict(observation.vector, centroids) == label for observation in group) / len(group))
    if not recalls:
        raise BlockNullError("test fold has none of the requested labels")
    return sum(recalls) / len(recalls)


def _permuted_test_observations(trial: TrialData, seed: int, labels: Sequence[str]) -> list[Observation]:
    """Shuffle complete bout tokens within each context segment for one test trial."""
    segments = _normalized(trial)
    rng = random.Random(seed)
    output: list[Observation] = []
    for segment_index, segment in enumerate(segments):
        order = list(segment.tokens)
        rng.shuffle(order)
        cursor = 0
        for slot, token in enumerate(order):
            end = cursor + token.length
            left, right = segment.prefix[cursor], segment.prefix[end]
            vector = tuple((right[i] - left[i]) / token.length for i in range(len(left)))
            output.append(Observation(token.label, vector, token.length, segment_index, slot))
            cursor = end
    if not any(observation.label in labels for observation in output):
        raise BlockNullError("permuted test fold has none of the requested labels")
    return output


def _sha256(path: Path) -> str:
    """Hash one JSONL input for the result provenance."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _distribution(observed: float, null_scores: Sequence[float]) -> dict[str, float | int]:
    """Summarize observed balanced accuracy against a one-sided null."""
    mean = sum(null_scores) / len(null_scores)
    sd = math.sqrt(sum((score - mean) ** 2 for score in null_scores) / len(null_scores))
    extreme = sum(score >= observed - 1e-15 for score in null_scores)
    return {"observed": observed, "null_n": len(null_scores), "null_mean": mean, "null_sd": sd, "p_greater_equal": (1 + extreme) / (1 + len(null_scores)), "z": 0.0 if sd == 0.0 else (observed - mean) / sd}


def analyze_trials(paths: Sequence[Path], *, labels: Sequence[str] = TARGET_LABELS, context: str = "co2_off", permutations: int = 999, seed: int = 20261002) -> dict[str, Any]:
    """Run leave-one-trial-out generalization for one animal."""
    if len(paths) < 3:
        raise BlockNullError("at least three trials are required for leave-one-trial-out generalization")
    if permutations <= 0:
        raise BlockNullError("permutations must be positive")
    trials = [load_trial(path, target_context=context) for path in paths]
    animals = sorted({trial.animal for trial in trials})
    if len(animals) != 1:
        raise BlockNullError("multiple animals supplied; cross-animal claims are forbidden")
    label_tuple = tuple(sorted(set(labels)))
    prepared = {trial.trial: _observations(trial) for trial in trials}
    fold_results: list[dict[str, Any]] = []
    null_matrix: list[list[float]] = []
    ordered = sorted(trials, key=lambda trial: trial.trial)
    for fold_index, test_trial in enumerate(ordered):
        test_observations = prepared[test_trial.trial]
        train_observations = [observation for trial in ordered if trial.trial != test_trial.trial for observation in prepared[trial.trial]]
        centroids = _centroids(train_observations, label_tuple)
        observed = balanced_accuracy(test_observations, centroids, label_tuple)
        null_scores: list[float] = []
        for permutation in range(permutations):
            shuffled = _permuted_test_observations(test_trial, seed + fold_index * 1009 + permutation, label_tuple)
            null_scores.append(balanced_accuracy(shuffled, centroids, label_tuple))
        distribution = _distribution(observed, null_scores)
        fold_results.append({"trial": test_trial.trial, "animal": test_trial.animal, "train_trials": [trial.trial for trial in ordered if trial.trial != test_trial.trial], "train_bouts": len(train_observations), "test_bouts": len(test_observations), "test_label_bouts": dict(sorted(Counter(observation.label for observation in test_observations if observation.label in label_tuple).items())), "distribution": distribution, "null_scores": null_scores})
        null_matrix.append(null_scores)
    pooled_observed = sum(result["distribution"]["observed"] for result in fold_results) / len(fold_results)
    pooled_null = [sum(row[index] for row in null_matrix) / len(null_matrix) for index in range(permutations)]
    return {"schema": SCHEMA, "verdict": "BIEN", "analysis": {"scope": "within_animal_leave_one_trial_out", "animal": animals[0], "context": context, "n_trials": len(ordered), "cross_animal": False, "causal": False, "unit": "bout", "feature_level": "ROI"}, "parameters": {"labels": list(label_tuple), "permutations": permutations, "seed": seed}, "inputs": [{"path": str(path), "bytes": path.stat().st_size, "sha256": _sha256(path)} for path in sorted(paths)], "null_contract": {"permuted_within": "each target-context segment of the held-out trial", "preserved": ["animal and trial identity", "context segments", "complete bout token lengths", "label bout counts", "ROI time order"], "destroyed": ["held-out label-to-neural-time alignment"], "not_tested": ["anatomical route identity", "causal silencing", "cross-animal generalization"]}, "folds": fold_results, "pooled": {**_distribution(pooled_observed, pooled_null), "null_scores": pooled_null}, "limitations": ["All trials belong to one animal; this is not cross-animal evidence.", "The nearest-centroid score is descriptive decoding, not route selection or causality.", "ROI channels are preserved but not mapped to cell type or neuropil.", "Labels are DAART predictions, not manual independent annotations."]}


def write_result(path: Path, result: Mapping[str, Any]) -> None:
    """Write deterministic JSON evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(result), allow_nan=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a shell exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", dest="inputs", action="append", type=Path, required=True)
    parser.add_argument("--labels", default=",".join(TARGET_LABELS))
    parser.add_argument("--context", default="co2_off")
    parser.add_argument("--permutations", type=int, default=999)
    parser.add_argument("--seed", type=int, default=20261002)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        labels = tuple(sorted({part.strip() for part in args.labels.split(",") if part.strip()}))
        result = analyze_trials(args.inputs, labels=labels, context=args.context, permutations=args.permutations, seed=args.seed)
        write_result(args.out, result)
        pooled = result["pooled"]
        print(json.dumps({"verdict": result["verdict"], "scope": result["analysis"]["scope"], "n_trials": result["analysis"]["n_trials"], "pooled": {key: value for key, value in pooled.items() if key != "null_scores"}, "out": str(args.out)}, sort_keys=True))
        return 0
    except (BlockNullError, OSError, KeyError, ValueError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
