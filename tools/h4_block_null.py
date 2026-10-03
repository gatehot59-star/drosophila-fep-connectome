#!/usr/bin/env python3
"""Run a block-preserving ROI-label null for aligned H4 feature JSONL files.

The instrument is deliberately descriptive. It tests whether named behavioral
labels separate ROI-level activity beyond a null that preserves contiguous bout
lengths, labels, context segments, and trial identity. It does not test route
causality, anatomical identity, or cross-animal generalization.
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

SCHEMA = "h4-aligned-features/v1"
NULL_SCHEMA = "h4-block-null/v1"


class BlockNullError(ValueError):
    """Raised when the aligned-feature contract cannot support this null."""


@dataclass(frozen=True)
class Token:
    """A contiguous labeled bout represented by its label and frame length."""

    label: str
    length: int


@dataclass(frozen=True)
class RawSegment:
    """A contiguous context segment with frame vectors and bout tokens."""

    context: str
    frame_vectors: tuple[tuple[float, ...], ...]
    tokens: tuple[Token, ...]


@dataclass(frozen=True)
class Segment:
    """A normalized context segment with prefix sums for block scoring."""

    context: str
    tokens: tuple[Token, ...]
    prefix: tuple[tuple[float, ...], ...]
    n_frames: int


@dataclass(frozen=True)
class TrialData:
    """Validated aligned features for one trial."""

    path: Path
    metadata: Mapping[str, Any]
    animal: str
    trial: str
    roi_names: tuple[str, ...]
    segments: tuple[RawSegment, ...]


def _finite(value: Any, field: str) -> float:
    """Return a finite float or raise a contract error."""
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise BlockNullError(f"{field}: not numeric") from exc
    if not math.isfinite(number):
        raise BlockNullError(f"{field}: non-finite value")
    return number


def _integer(value: Any, field: str) -> int:
    """Return an integer field without accepting a lossy float."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise BlockNullError(f"{field}: expected integer")
    return value


def _sha256(path: Path) -> str:
    """Hash an input file for the provenance manifest."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_bout(rows: Sequence[Mapping[str, Any]], start: int, stop: int) -> Token:
    """Validate one contiguous bout and return its token."""
    first = rows[start]
    label = str(first["label"])
    context = str(first["context"])
    length = _integer(first["bout_length"], "bout_length")
    if length <= 0 or length != stop - start:
        raise BlockNullError(f"bout {first['bout_id']}: invalid declared length")
    for position, row in enumerate(rows[start:stop]):
        if str(row["label"]) != label or str(row["context"]) != context:
            raise BlockNullError("a bout changes label or context internally")
        if _integer(row["bout_position"], "bout_position") != position:
            raise BlockNullError("bout_position is not contiguous")
        if _integer(row["bout_length"], "bout_length") != length:
            raise BlockNullError("bout_length changes internally")
    return Token(label=label, length=length)


def _segments(rows: Sequence[Mapping[str, Any]], roi_names: Sequence[str], context: str) -> tuple[RawSegment, ...]:
    """Validate rows and construct contiguous target-context segments."""
    if not rows:
        raise BlockNullError("feature file has no frame records")
    for index, row in enumerate(rows):
        if row.get("record_type") != "frame":
            raise BlockNullError(f"row {index}: expected record_type=frame")
        if "Frame" in row:
            raise BlockNullError("legacy Frame joins are forbidden")
        if _integer(row.get("behavior_frame"), "behavior_frame") != index:
            raise BlockNullError("behavior_frame is not sequential")
        time_s = _finite(row.get("time_s"), "time_s")
        if index and time_s <= float(rows[index - 1]["time_s"]):
            raise BlockNullError("time_s must be strictly increasing")
        if not isinstance(row.get("label"), str) or not row["label"]:
            raise BlockNullError("label must be a non-empty string")
        if not isinstance(row.get("context"), str) or not row["context"]:
            raise BlockNullError("context must be a non-empty string")
        roi = row.get("roi")
        if not isinstance(roi, Mapping) or tuple(sorted(roi)) != tuple(sorted(roi_names)):
            raise BlockNullError("ROI names differ between metadata and frame")
        for name in roi_names:
            _finite(roi[name], f"roi.{name}")

    output: list[RawSegment] = []
    position = 0
    while position < len(rows):
        if rows[position]["context"] != context:
            position += 1
            continue
        start = position
        while position < len(rows) and rows[position]["context"] == context:
            position += 1
        chunk = rows[start:position]
        tokens: list[Token] = []
        cursor = 0
        while cursor < len(chunk):
            bout_id = _integer(chunk[cursor]["bout_id"], "bout_id")
            token_start = cursor
            cursor += 1
            while cursor < len(chunk) and _integer(chunk[cursor]["bout_id"], "bout_id") == bout_id:
                cursor += 1
            tokens.append(_validate_bout(rows, start + token_start, start + cursor))
        vectors = tuple(tuple(_finite(row["roi"][name], f"roi.{name}") for name in roi_names) for row in chunk)
        if sum(token.length for token in tokens) != len(vectors):
            raise BlockNullError("bout lengths do not cover the context segment")
        output.append(RawSegment(context=context, frame_vectors=vectors, tokens=tuple(tokens)))
    if not output:
        raise BlockNullError(f"target context {context!r} is absent")
    return tuple(output)


def load_trial(path: Path, target_context: str = "co2_off") -> TrialData:
    """Load and validate one aligned-features JSONL trial."""
    if not path.is_file():
        raise BlockNullError(f"input does not exist: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            documents = [json.loads(line) for line in handle if line.strip()]
    except (OSError, json.JSONDecodeError) as exc:
        raise BlockNullError(f"cannot read {path}: {exc}") from exc
    if len(documents) < 2:
        raise BlockNullError(f"{path}: metadata plus at least one row required")
    metadata, rows = documents[0], documents[1:]
    if metadata.get("record_type") != "metadata" or metadata.get("schema") != SCHEMA:
        raise BlockNullError(f"{path}: unsupported aligned-features schema")
    if metadata.get("verdict") != "BIEN":
        raise BlockNullError(f"{path}: source verdict is not BIEN")
    identity = metadata.get("identity")
    if not isinstance(identity, Mapping):
        raise BlockNullError(f"{path}: identity is missing")
    animal = str(identity.get("animal", ""))
    trial = str(identity.get("trial", ""))
    if not animal or not trial or not identity.get("timebase"):
        raise BlockNullError(f"{path}: incomplete identity")
    roi_names = tuple(str(name) for name in metadata.get("roi_names", []))
    if not roi_names or len(set(roi_names)) != len(roi_names):
        raise BlockNullError(f"{path}: ROI names are missing or duplicated")
    if _integer(metadata.get("n_records"), "n_records") != len(rows):
        raise BlockNullError(f"{path}: n_records does not match JSONL rows")
    return TrialData(path, metadata, animal, trial, roi_names, _segments(rows, roi_names, target_context))


def _normalized(trial: TrialData) -> tuple[Segment, ...]:
    """Standardize ROI dimensions once and build prefix sums."""
    vectors = [vector for segment in trial.segments for vector in segment.frame_vectors]
    dimension = len(trial.roi_names)
    means = [sum(vector[index] for vector in vectors) / len(vectors) for index in range(dimension)]
    scales = []
    for index in range(dimension):
        variance = sum((vector[index] - means[index]) ** 2 for vector in vectors) / len(vectors)
        scales.append(math.sqrt(variance) or 1.0)
    output: list[Segment] = []
    for raw in trial.segments:
        normalized = [tuple((vector[index] - means[index]) / scales[index] for index in range(dimension)) for vector in raw.frame_vectors]
        prefix: list[tuple[float, ...]] = [tuple(0.0 for _ in range(dimension))]
        for vector in normalized:
            previous = prefix[-1]
            prefix.append(tuple(previous[index] + vector[index] for index in range(dimension)))
        output.append(Segment(raw.context, raw.tokens, tuple(prefix), len(normalized)))
    return tuple(output)


def token_observations(segments: Sequence[Segment], orders: Sequence[Sequence[Token]]) -> list[tuple[str, tuple[float, ...]]]:
    """Map a block order onto neural frames and return bout means."""
    if len(segments) != len(orders):
        raise BlockNullError("segment and token-order counts differ")
    observations: list[tuple[str, tuple[float, ...]]] = []
    for segment, order in zip(segments, orders):
        if sum(token.length for token in order) != segment.n_frames:
            raise BlockNullError("permuted bout lengths do not cover segment")
        cursor = 0
        for token in order:
            end = cursor + token.length
            left, right = segment.prefix[cursor], segment.prefix[end]
            mean = tuple((right[index] - left[index]) / token.length for index in range(len(left)))
            observations.append((token.label, mean))
            cursor = end
    return observations


def eta_squared(observations: Sequence[tuple[str, tuple[float, ...]]], labels: Sequence[str], min_bouts: int = 2) -> tuple[float, dict[str, tuple[float, ...]], dict[str, int]]:
    """Compute equal-bout-weighted label separation in normalized ROI space."""
    requested = set(labels)
    counts = Counter(label for label, _ in observations if label in requested)
    eligible = {label for label, count in counts.items() if count >= min_bouts}
    selected = [(label, vector) for label, vector in observations if label in eligible]
    if len(eligible) < 2 or len(selected) < 2:
        return 0.0, {}, dict(counts)
    dimension = len(selected[0][1])
    grand = tuple(sum(vector[index] for _, vector in selected) / len(selected) for index in range(dimension))
    grouped: dict[str, list[tuple[float, ...]]] = {}
    for label, vector in selected:
        grouped.setdefault(label, []).append(vector)
    between = 0.0
    means: dict[str, tuple[float, ...]] = {}
    for label, group in sorted(grouped.items()):
        mean = tuple(sum(vector[index] for vector in group) / len(group) for index in range(dimension))
        means[label] = mean
        between += len(group) * sum((mean[index] - grand[index]) ** 2 for index in range(dimension))
    total = sum(sum((vector[index] - grand[index]) ** 2 for index in range(dimension)) for _, vector in selected)
    score = 0.0 if total <= 0.0 else max(0.0, min(1.0, between / total))
    return score, means, dict(counts)


def _counts(segments: Sequence[Segment], by_frames: bool) -> dict[str, int]:
    """Count source labels by frames or bouts for preservation evidence."""
    counts: Counter[str] = Counter()
    for segment in segments:
        for token in segment.tokens:
            counts[token.label] += token.length if by_frames else 1
    return dict(sorted(counts.items()))


def _summary(observed: float, null: Sequence[float]) -> dict[str, float | int]:
    """Summarize an observed score against a one-sided Monte Carlo null."""
    if not null:
        return {"observed": observed, "null_n": 0, "null_mean": 0.0, "null_sd": 0.0, "p_greater_equal": 1.0, "z": 0.0}
    mean = sum(null) / len(null)
    sd = math.sqrt(sum((score - mean) ** 2 for score in null) / len(null))
    extreme = sum(score >= observed - 1e-15 for score in null)
    return {"observed": observed, "null_n": len(null), "null_mean": mean, "null_sd": sd, "p_greater_equal": (1 + extreme) / (1 + len(null)), "z": 0.0 if sd == 0.0 else (observed - mean) / sd}


def analyze_trial(trial: TrialData, permutations: int, seed: int, labels: Sequence[str] | None, min_bouts: int) -> tuple[dict[str, Any], list[float]]:
    """Analyze one trial and return its report plus null scores."""
    if permutations <= 0 or min_bouts < 1:
        raise BlockNullError("permutations and min_bouts must be positive")
    segments = _normalized(trial)
    requested = tuple(sorted(set(labels))) if labels else tuple(sorted({token.label for segment in segments for token in segment.tokens}))
    observed = token_observations(segments, [segment.tokens for segment in segments])
    observed_score, means, token_counts = eta_squared(observed, requested, min_bouts)
    eligible = tuple(sorted(label for label, count in token_counts.items() if count >= min_bouts))
    rng = random.Random(seed)
    null_scores: list[float] = []
    for _ in range(permutations):
        orders = []
        for segment in segments:
            order = list(segment.tokens)
            rng.shuffle(order)
            orders.append(tuple(order))
        score, _, _ = eta_squared(token_observations(segments, orders), eligible, min_bouts)
        null_scores.append(score)
    return {
        "path": str(trial.path), "animal": trial.animal, "trial": trial.trial, "roi_names": list(trial.roi_names),
        "n_context_segments": len(segments), "n_bouts": sum(len(segment.tokens) for segment in segments),
        "context_frames": sum(segment.n_frames for segment in segments), "labels_requested": list(requested), "labels_used": list(eligible),
        "label_bout_counts": _counts(segments, False), "label_frame_counts": _counts(segments, True),
        "label_means_normalized": {label: list(vector) for label, vector in means.items()},
        "distribution": _summary(observed_score, null_scores),
        "preservation": {"context": segments[0].context, "context_segment_lengths": [segment.n_frames for segment in segments],
                         "bout_lengths_sorted": sorted(token.length for segment in segments for token in segment.tokens),
                         "label_frame_counts": _counts(segments, True), "label_bout_counts": _counts(segments, False)},
        "null_scores": null_scores,
    }, null_scores


def analyze_trials(paths: Sequence[Path], *, target_context: str = "co2_off", permutations: int = 999, seed: int = 20261002, labels: Sequence[str] | None = None, min_bouts: int = 2) -> dict[str, Any]:
    """Run the block-preserving null across trials from one animal."""
    if not paths:
        raise BlockNullError("at least one input is required")
    trials = [load_trial(path, target_context) for path in paths]
    animals = sorted({trial.animal for trial in trials})
    if len(animals) != 1:
        raise BlockNullError("multiple animals supplied; this instrument refuses cross-animal claims")
    reports: list[dict[str, Any]] = []
    nulls: list[list[float]] = []
    for index, trial in enumerate(sorted(trials, key=lambda item: item.trial)):
        report, trial_null = analyze_trial(trial, permutations, seed + index * 1009, labels, min_bouts)
        reports.append(report)
        nulls.append(trial_null)
    observed = sum(report["distribution"]["observed"] for report in reports) / len(reports)
    pooled = [sum(trial_null[index] for trial_null in nulls) / len(nulls) for index in range(permutations)]
    return {
        "schema": NULL_SCHEMA, "verdict": "BIEN",
        "analysis": {"scope": "within_animal_across_trials", "animal": animals[0], "n_trials": len(reports), "context": target_context, "roi_level": True, "cross_animal": False, "causal": False},
        "parameters": {"permutations": permutations, "seed": seed, "min_bouts": min_bouts, "labels_requested": list(labels) if labels else None},
        "null_contract": {"unit": "contiguous bout token", "permuted_within": "each contiguous target-context segment of each trial",
                           "preserved": ["animal and trial identity", "context segment boundaries", "context frame counts", "exact bout-length multiset", "label frame counts", "label bout counts", "ROI values and time order"],
                           "destroyed": ["original label-to-neural-time alignment", "original bout order"], "not_tested": ["anatomical route identity", "causal silencing", "cross-animal generalization"]},
        "inputs": [{"path": str(path), "bytes": path.stat().st_size, "sha256": _sha256(path)} for path in sorted(paths)],
        "trial_results": reports, "pooled": {**_summary(observed, pooled), "null_scores": pooled},
        "limitations": ["All supplied trials belong to one animal; this is not cross-animal evidence.", "Two ROI channels are a descriptive signal, not an anatomical route map.", "The statistic treats bouts as units for the score; it is not a frame-level inferential test.", "A positive separation score would still be decoding, not causal route control."],
    }


def write_result(path: Path, result: Mapping[str, Any]) -> None:
    """Write a deterministic JSON result with the full null distribution."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(result), allow_nan=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_labels(raw: str | None) -> tuple[str, ...] | None:
    """Parse a comma-separated label list, rejecting empty lists."""
    if raw is None:
        return None
    labels = tuple(sorted({part.strip() for part in raw.split(",") if part.strip()}))
    if not labels:
        raise BlockNullError("--labels must contain at least one non-empty label")
    return labels


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI instrument and return a shell exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", dest="inputs", action="append", type=Path, required=True)
    parser.add_argument("--context", default="co2_off")
    parser.add_argument("--labels", default=None)
    parser.add_argument("--min-bouts", type=int, default=2)
    parser.add_argument("--permutations", type=int, default=999)
    parser.add_argument("--seed", type=int, default=20261002)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = analyze_trials(args.inputs, target_context=args.context, permutations=args.permutations, seed=args.seed, labels=_parse_labels(args.labels), min_bouts=args.min_bouts)
        write_result(args.out, result)
        print(json.dumps({"verdict": result["verdict"], "scope": result["analysis"]["scope"], "n_trials": result["analysis"]["n_trials"], "labels_used_by_trial": [item["labels_used"] for item in result["trial_results"]], "pooled": result["pooled"], "out": str(args.out)}, allow_nan=False, sort_keys=True))
        return 0
    except (BlockNullError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
