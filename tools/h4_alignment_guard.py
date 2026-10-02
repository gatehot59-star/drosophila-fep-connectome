#!/usr/bin/env python3
"""Fail-closed temporal and identity guards for the H4 neural pipeline."""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


class AlignmentError(ValueError):
    """Raised when an H4 source pair cannot be joined safely."""


@dataclass(frozen=True)
class AxisSummary:
    """Measured properties of one strictly increasing time axis."""

    name: str
    n: int
    start: float
    end: float
    duration: float
    median_step: float
    max_step: float

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable summary."""
        return {
            "name": self.name,
            "n": self.n,
            "start": self.start,
            "end": self.end,
            "duration": self.duration,
            "median_step": self.median_step,
            "max_step": self.max_step,
        }


def _finite_numbers(name: str, values: Iterable[float]) -> list[float]:
    """Materialize and validate a finite numeric sequence."""
    try:
        out = [float(value) for value in values]
    except (TypeError, ValueError) as exc:
        raise AlignmentError(f"{name}: time axis is not numeric") from exc
    if len(out) < 2:
        raise AlignmentError(f"{name}: at least two timestamps are required")
    if not all(math.isfinite(value) for value in out):
        raise AlignmentError(f"{name}: time axis contains NaN or infinity")
    return out


def summarize_time_axis(name: str, values: Sequence[float]) -> AxisSummary:
    """Validate monotonicity and summarize a time axis."""
    axis = _finite_numbers(name, values)
    steps = [right - left for left, right in zip(axis, axis[1:])]
    if any(step <= 0.0 for step in steps):
        raise AlignmentError(f"{name}: timestamps are not strictly increasing")
    ordered = sorted(steps)
    middle = len(ordered) // 2
    median = ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2.0
    return AxisSummary(
        name=name,
        n=len(axis),
        start=axis[0],
        end=axis[-1],
        duration=axis[-1] - axis[0],
        median_step=median,
        max_step=max(steps),
    )


def validate_identity(
    neural_metadata: Mapping[str, Any],
    behavior_metadata: Mapping[str, Any],
    required: Sequence[str] = ("animal", "trial", "timebase"),
) -> dict[str, Any]:
    """Require matching animal, trial and clock identity before joining."""
    missing: list[str] = []
    mismatches: dict[str, dict[str, Any]] = {}
    for key in required:
        left = neural_metadata.get(key)
        right = behavior_metadata.get(key)
        if left is None or right is None:
            missing.append(key)
        elif str(left) != str(right):
            mismatches[key] = {"neural": left, "behavior": right}
    if missing:
        raise AlignmentError("missing identity fields: " + ", ".join(missing))
    if mismatches:
        raise AlignmentError("identity mismatch: " + json.dumps(mismatches, sort_keys=True))
    return {key: neural_metadata[key] for key in required}


def require_time_join(join_key: str) -> None:
    """Reject integer-frame joins; H4 must use an explicit time axis."""
    if join_key.lower() not in {"time", "timestamp", "seconds"}:
        raise AlignmentError(
            f"join key {join_key!r} is unsafe; H4 joins must use Time/seconds, not Frame"
        )


def validate_temporal_alignment(
    neural_times: Sequence[float],
    behavior_times: Sequence[float],
    *,
    neural_metadata: Mapping[str, Any],
    behavior_metadata: Mapping[str, Any],
    join_key: str = "Time",
    max_duration_error: float = 0.05,
    min_overlap_fraction: float = 0.90,
    max_step_factor: float = 20.0,
) -> dict[str, Any]:
    """Validate identity, clocks, coverage and gaps before feature construction."""
    require_time_join(join_key)
    identity = validate_identity(neural_metadata, behavior_metadata)
    neural = summarize_time_axis("neural", neural_times)
    behavior = summarize_time_axis("behavior", behavior_times)
    duration_error = abs(neural.duration - behavior.duration) / max(neural.duration, behavior.duration)
    overlap_start = max(neural.start, behavior.start)
    overlap_end = min(neural.end, behavior.end)
    overlap = max(0.0, overlap_end - overlap_start)
    coverage_neural = overlap / neural.duration
    coverage_behavior = overlap / behavior.duration
    if duration_error > max_duration_error:
        raise AlignmentError(
            f"duration mismatch {duration_error:.6f} exceeds {max_duration_error:.6f}"
        )
    if min(coverage_neural, coverage_behavior) < min_overlap_fraction:
        raise AlignmentError(
            "insufficient temporal overlap: "
            f"neural={coverage_neural:.6f}, behavior={coverage_behavior:.6f}"
        )
    for axis in (neural, behavior):
        if axis.max_step > axis.median_step * max_step_factor:
            raise AlignmentError(
                f"{axis.name}: gap {axis.max_step:.6f}s exceeds "
                f"{max_step_factor:.1f}x its median step"
            )
    return {
        "verdict": "BIEN",
        "join_key": join_key,
        "identity": identity,
        "neural": neural.as_dict(),
        "behavior": behavior.as_dict(),
        "duration_relative_error": duration_error,
        "overlap_start": overlap_start,
        "overlap_end": overlap_end,
        "overlap_duration": overlap,
        "coverage_neural": coverage_neural,
        "coverage_behavior": coverage_behavior,
    }


def validate_manifest(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a manifest with neural/behavior times and metadata."""
    try:
        neural = payload["neural"]
        behavior = payload["behavior"]
    except KeyError as exc:
        raise AlignmentError(f"manifest missing {exc.args[0]!r}") from exc
    if not isinstance(neural, Mapping) or not isinstance(behavior, Mapping):
        raise AlignmentError("manifest neural and behavior entries must be objects")
    return validate_temporal_alignment(
        neural["times"],
        behavior["times"],
        neural_metadata=neural.get("metadata", {}),
        behavior_metadata=behavior.get("metadata", {}),
        join_key=str(payload.get("join_key", "Time")),
        max_duration_error=float(payload.get("max_duration_error", 0.05)),
        min_overlap_fraction=float(payload.get("min_overlap_fraction", 0.90)),
        max_step_factor=float(payload.get("max_step_factor", 20.0)),
    )


def main() -> int:
    """Validate a JSON manifest and print the measured report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = validate_manifest(json.loads(args.manifest.read_text()))
    except (OSError, json.JSONDecodeError, AlignmentError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
