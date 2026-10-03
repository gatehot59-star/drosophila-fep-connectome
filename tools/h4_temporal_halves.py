#!/usr/bin/env python3
"""Measure temporal stability between early and late complete bouts.

The instrument uses aligned ROI features, keeps bout units intact, and fits a
nearest-centroid decoder in each temporal half. It is descriptive: it measures
whether a label-to-ROI representation transfers from early to late and back,
not whether any anatomical route causes the behavior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

import h4_block_null
from h4_block_null import BlockNullError, load_trial
_normalized = getattr(h4_block_null, "_normalized", None) or getattr(h4_block_null, "_normalized_segments")

SCHEMA = "h4-temporal-halves/v1"
DEFAULT_LABELS = ("walking", "resting")


class TemporalHalvesError(BlockNullError):
    """Raised when temporal-half contracts cannot be satisfied."""


def _sha256(path: Path) -> str:
    """Hash one input JSONL for provenance."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _observations(segments: Sequence[Any]) -> list[dict[str, Any]]:
    """Convert normalized segments into complete bout observations."""
    output: list[dict[str, Any]] = []
    for segment_index, segment in enumerate(segments):
        cursor = 0
        for order, token in enumerate(segment.tokens):
            end = cursor + token.length
            left, right = segment.prefix[cursor], segment.prefix[end]
            vector = tuple((right[i] - left[i]) / token.length for i in range(len(left)))
            output.append({"label": token.label, "length": token.length, "vector": vector, "segment": segment_index, "order": order})
    return output


def _split_observations(observations: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split chronological bouts at the closest complete-bout midpoint."""
    if len(observations) < 2:
        raise TemporalHalvesError("at least two complete bouts are required")
    total_frames = sum(int(item["length"]) for item in observations)
    target = total_frames / 2.0
    cumulative = 0
    candidates: list[tuple[float, int]] = []
    for index, item in enumerate(observations[:-1], start=1):
        cumulative += int(item["length"])
        candidates.append((abs(cumulative - target), index))
    _, split_index = min(candidates)
    early = [dict(item, half="early", half_order=index) for index, item in enumerate(observations[:split_index])]
    late = [dict(item, half="late", half_order=index) for index, item in enumerate(observations[split_index:])]
    if not early or not late:
        raise TemporalHalvesError("midpoint produced an empty half")
    return early, late


def _centroids(observations: Sequence[Mapping[str, Any]], labels: Sequence[str]) -> dict[str, tuple[float, ...]]:
    """Fit one equal-bout-weighted centroid per requested label."""
    groups: dict[str, list[tuple[float, ...]]] = {label: [] for label in labels}
    for item in observations:
        if item["label"] in groups:
            groups[item["label"]].append(tuple(item["vector"]))
    missing = [label for label in labels if not groups[label]]
    if missing:
        raise TemporalHalvesError(f"half lacks labels: {','.join(missing)}")
    return {label: tuple(sum(vector[index] for vector in groups[label]) / len(groups[label]) for index in range(len(groups[label][0]))) for label in labels}


def _predict(vector: Sequence[float], centroids: Mapping[str, Sequence[float]]) -> str:
    """Return the closest centroid label."""
    return min(centroids, key=lambda label: sum((vector[index] - centroids[label][index]) ** 2 for index in range(len(vector))))


def balanced_accuracy(observations: Sequence[Mapping[str, Any]], centroids: Mapping[str, Sequence[float]], labels: Sequence[str]) -> float:
    """Compute macro recall over labels present in a half."""
    recalls: list[float] = []
    for label in labels:
        group = [item for item in observations if item["label"] == label]
        if not group:
            continue
        recalls.append(sum(_predict(item["vector"], centroids) == label for item in group) / len(group))
    if not recalls:
        raise TemporalHalvesError("half has none of the requested labels")
    return sum(recalls) / len(recalls)


def _shuffle_labels(observations: Sequence[Mapping[str, Any]], seed: int) -> list[dict[str, Any]]:
    """Permute complete bout tokens within each half-segment.

    The aligned inputs contain seven disjoint ``co2_off`` segments per trial.
    Shuffling across those boundaries would make the null too permissive and
    would silently change the experimental context. Keep every segment's
    label/length multiset fixed and only destroy its label-to-ROI assignment.
    """
    rng = random.Random(seed)
    output = [dict(item) for item in observations]
    slots_by_segment: dict[Any, list[int]] = {}
    for slot, item in enumerate(observations):
        slots_by_segment.setdefault(item["segment"], []).append(slot)
    for slots in slots_by_segment.values():
        tokens = [(observations[slot]["label"], observations[slot]["length"]) for slot in slots]
        rng.shuffle(tokens)
        for slot, (label, length) in zip(slots, tokens):
            output[slot]["label"] = label
            output[slot]["length"] = length
            output[slot]["half_order"] = slot
    return output


def _centroid_cosines(early: Mapping[str, Sequence[float]], late: Mapping[str, Sequence[float]], labels: Sequence[str]) -> dict[str, float]:
    """Compute cosine similarity between early and late label centroids."""
    output: dict[str, float] = {}
    for label in labels:
        left, right = early[label], late[label]
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        output[label] = 0.0 if left_norm == 0.0 or right_norm == 0.0 else sum(left[i] * right[i] for i in range(len(left))) / (left_norm * right_norm)
    return output


def _summary(observed: float, null_scores: Sequence[float]) -> dict[str, float | int]:
    """Compare a stability score with a one-sided null."""
    mean = sum(null_scores) / len(null_scores)
    sd = math.sqrt(sum((value - mean) ** 2 for value in null_scores) / len(null_scores))
    extreme = sum(value >= observed - 1e-15 for value in null_scores)
    return {"observed": observed, "null_n": len(null_scores), "null_mean": mean, "null_sd": sd, "p_greater_equal": (1 + extreme) / (1 + len(null_scores)), "z": 0.0 if sd == 0.0 else (observed - mean) / sd}


def analyze_trial(trial: Any, labels: Sequence[str], permutations: int, seed: int, context: str) -> tuple[dict[str, Any], list[float]]:
    """Measure bidirectional cross-half transfer for one trial."""
    normalized = _normalized(trial)
    all_observations = _observations(normalized)
    early, late = _split_observations(all_observations)
    early_centroids = _centroids(early, labels)
    late_centroids = _centroids(late, labels)
    early_to_late = balanced_accuracy(late, early_centroids, labels)
    late_to_early = balanced_accuracy(early, late_centroids, labels)
    observed = (early_to_late + late_to_early) / 2.0
    null_scores: list[float] = []
    for permutation in range(permutations):
        null_early = _shuffle_labels(early, seed + permutation * 2)
        null_late = _shuffle_labels(late, seed + permutation * 2 + 1)
        null_early_centroids = _centroids(null_early, labels)
        null_late_centroids = _centroids(null_late, labels)
        null_scores.append((balanced_accuracy(null_late, null_early_centroids, labels) + balanced_accuracy(null_early, null_late_centroids, labels)) / 2.0)
    return {
        "trial": trial.trial,
        "animal": trial.animal,
        "context": context,
        "early_bouts": len(early),
        "late_bouts": len(late),
        "early_frames": sum(item["length"] for item in early),
        "late_frames": sum(item["length"] for item in late),
        "early_label_bouts": dict(sorted(Counter(item["label"] for item in early if item["label"] in labels).items())),
        "late_label_bouts": dict(sorted(Counter(item["label"] for item in late if item["label"] in labels).items())),
        "early_to_late": early_to_late,
        "late_to_early": late_to_early,
        "centroid_cosine": _centroid_cosines(early_centroids, late_centroids, labels),
        "distribution": _summary(observed, null_scores),
        "null_scores": null_scores,
    }, null_scores


def analyze_trials(paths: Sequence[Path], *, labels: Sequence[str] = DEFAULT_LABELS, context: str = "co2_off", permutations: int = 999, seed: int = 20261002) -> dict[str, Any]:
    """Run temporal-half stability across aligned trials from one animal."""
    if len(paths) < 3:
        raise TemporalHalvesError("at least three trials are required")
    if permutations <= 0:
        raise TemporalHalvesError("permutations must be positive")
    try:
        trials = [load_trial(path, target_context=context) for path in paths]
    except BlockNullError as exc:
        raise TemporalHalvesError(str(exc)) from exc
    animals = sorted({trial.animal for trial in trials})
    if len(animals) != 1:
        raise TemporalHalvesError("multiple animals supplied; cross-animal claims are forbidden")
    label_tuple = tuple(sorted(set(labels)))
    results: list[dict[str, Any]] = []
    nulls: list[list[float]] = []
    for index, trial in enumerate(sorted(trials, key=lambda item: item.trial)):
        result, scores = analyze_trial(trial, label_tuple, permutations, seed + index * 1009, context)
        results.append(result)
        nulls.append(scores)
    observed = sum(item["distribution"]["observed"] for item in results) / len(results)
    pooled = [sum(scores[index] for scores in nulls) / len(nulls) for index in range(permutations)]
    return {
        "schema": SCHEMA,
        "verdict": "BIEN",
        "analysis": {"scope": "within_animal_temporal_halves", "animal": animals[0], "context": context, "n_trials": len(results), "cross_animal": False, "causal": False, "unit": "bout", "feature_level": "ROI"},
        "parameters": {"labels": list(label_tuple), "permutations": permutations, "seed": seed, "split": "nearest complete-bout midpoint by target-context frames"},
        "inputs": [{"path": str(path), "bytes": path.stat().st_size, "sha256": _sha256(path)} for path in sorted(paths)],
        "null_contract": {"permuted_within": "each half of each target-context segment", "preserved": ["animal/trial identity", "target-context segment boundaries", "complete bout lengths", "label and length counts per half-segment", "ROI temporal order within slots"], "destroyed": ["label-to-neural alignment within each half-segment"], "not_tested": ["anatomical route identity", "causal silencing", "cross-animal generalization"]},
        "trials": results,
        "pooled": {**_summary(observed, pooled), "null_scores": pooled},
        "limitations": ["All trials belong to one animal; this is not cross-animal evidence.", "Cross-half decoding is descriptive and not causal.", "The temporal split is constrained to complete bouts, so halves are not exactly equal in frames.", "ROI channels are not mapped to cell type or neuropil.", "Labels are DAART predictions, not manual independent annotations."],
    }


def write_result(path: Path, result: Mapping[str, Any]) -> None:
    """Write deterministic JSON evidence."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(result), allow_nan=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a shell exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", dest="inputs", action="append", type=Path, required=True)
    parser.add_argument("--labels", default=",".join(DEFAULT_LABELS))
    parser.add_argument("--context", default="co2_off")
    parser.add_argument("--permutations", type=int, default=999)
    parser.add_argument("--seed", type=int, default=20261002)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        labels = tuple(sorted({part.strip() for part in args.labels.split(",") if part.strip()}))
        result = analyze_trials(args.inputs, labels=labels, context=args.context, permutations=args.permutations, seed=args.seed)
        write_result(args.out, result)
        print(json.dumps({"verdict": result["verdict"], "scope": result["analysis"]["scope"], "n_trials": result["analysis"]["n_trials"], "pooled": {key: value for key, value in result["pooled"].items() if key != "null_scores"}, "out": str(args.out)}, sort_keys=True))
        return 0
    except (TemporalHalvesError, OSError, KeyError, ValueError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
