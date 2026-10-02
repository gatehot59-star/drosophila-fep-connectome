#!/usr/bin/env python3
"""Materialize ROI-preserving, time-aligned H4 features."""
from __future__ import annotations

import argparse
import bisect
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from h4_official_loader import (  # noqa: E402
    build_manifest,
    load_pickle,
    process_camera_line,
    process_frame_counter,
)

ACTIONS = frozenset(
    {"walking", "resting", "head_grooming", "foreleg_grooming", "hind_grooming"}
)


class FeatureAlignmentError(ValueError):
    """Raised when aligned feature construction would extrapolate or lose rows."""


def _finite_axis(name: str, values: Iterable[float]) -> list[float]:
    """Validate and materialize a finite, strictly increasing time axis."""
    axis = [float(value) for value in values]
    if len(axis) < 2:
        raise FeatureAlignmentError(f"{name}: at least two values are required")
    if not all(math.isfinite(value) for value in axis):
        raise FeatureAlignmentError(f"{name}: non-finite value")
    if any(right <= left for left, right in zip(axis, axis[1:])):
        raise FeatureAlignmentError(f"{name}: values must be strictly increasing")
    return axis


def overlap_indices(source_times: Sequence[float], target_times: Sequence[float]) -> list[int]:
    """Return target positions covered by the source axis, without extrapolation."""
    source = _finite_axis("source_times", source_times)
    target = _finite_axis("target_times", target_times)
    return [index for index, value in enumerate(target) if source[0] <= value <= source[-1]]


def interpolate_series(
    source_times: Sequence[float],
    source_values: Sequence[float],
    target_times: Sequence[float],
) -> list[float]:
    """Interpolate one ROI without extrapolation."""
    source = _finite_axis("source_times", source_times)
    target = _finite_axis("target_times", target_times)
    values = [float(value) for value in source_values]
    if len(values) != len(source):
        raise FeatureAlignmentError(
            f"source values length {len(values)} != time length {len(source)}"
        )
    if not all(math.isfinite(value) for value in values):
        raise FeatureAlignmentError("source_values: non-finite value")
    if target[0] < source[0] or target[-1] > source[-1]:
        raise FeatureAlignmentError(
            "target axis falls outside source coverage; extrapolation is forbidden"
        )
    result: list[float] = []
    for timestamp in target:
        right = bisect.bisect_left(source, timestamp)
        if right < len(source) and source[right] == timestamp:
            result.append(values[right])
            continue
        if right == 0 or right == len(source):
            raise FeatureAlignmentError("target timestamp cannot be bracketed")
        left = right - 1
        fraction = (timestamp - source[left]) / (source[right] - source[left])
        result.append(values[left] + fraction * (values[right] - values[left]))
    return result


def derive_bouts(labels: Sequence[str], contexts: Sequence[str]) -> list[dict[str, int]]:
    """Create contiguous bout ids, positions and lengths."""
    if len(labels) != len(contexts):
        raise FeatureAlignmentError("labels and contexts must have equal length")
    if not labels:
        return []
    spans: list[tuple[int, int]] = []
    start = 0
    for index in range(1, len(labels)):
        if labels[index] != labels[index - 1] or contexts[index] != contexts[index - 1]:
            spans.append((start, index))
            start = index
    spans.append((start, len(labels)))
    output: list[dict[str, int]] = []
    for bout_id, (left, right) in enumerate(spans):
        length = right - left
        output.extend(
            {"bout_id": bout_id, "bout_position": position, "bout_length": length}
            for position in range(length)
        )
    return output


def context_by_camera_frame(
    h5_path: Path, capture_path: Path, expected_frames: int
) -> tuple[list[str], dict[str, int]]:
    """Reconstruct CO2 context and sample counts for each camera frame."""
    import h5py
    import numpy as np

    with h5py.File(h5_path, "r") as handle:
        basler = handle["DI/Basler"][:].squeeze()
        counter = handle["CI/Frame Counter"][:].squeeze()
        capture = handle["DI/Capture On"][:].squeeze().astype(bool)
        co2 = handle["DI/CO2_Stim"][:].squeeze().astype(float)
    metadata = json.loads(capture_path.read_text())
    camera = process_camera_line(basler, metadata)
    frame_counter = process_frame_counter(counter, steps_per_frame=3)
    mask = capture & (frame_counter >= 0)
    indices = np.flatnonzero(mask)
    if len(indices) == 0:
        raise FeatureAlignmentError("context: no synchronized samples")
    mask[max(0, int(indices[0]) - 1)] = True
    camera = camera[mask]
    co2 = co2[mask]
    changes = np.flatnonzero(np.diff(camera) > 0) + 1
    starts = np.r_[0, changes]
    stops = np.r_[changes, len(camera)]
    contexts: list[str] = []
    sample_counts = Counter()
    for left, right in zip(starts, stops):
        is_on = bool(float(np.mean(co2[left:right])) > 0.5)
        context = "co2_on" if is_on else "co2_off"
        contexts.append(context)
        sample_counts[context] += int(right - left)
    if len(contexts) != expected_frames:
        raise FeatureAlignmentError(
            f"context frames {len(contexts)} != expected {expected_frames}"
        )
    return contexts, dict(sample_counts)


def frame_records(
    *,
    animal: str,
    trial: str,
    times: Sequence[float],
    labels: Sequence[str],
    contexts: Sequence[str],
    roi_features: Mapping[str, Sequence[float]],
) -> list[dict[str, Any]]:
    """Build one record per aligned behavior frame while retaining ROI names."""
    if len(times) != len(labels) or len(labels) != len(contexts):
        raise FeatureAlignmentError("times, labels and contexts must have equal length")
    names = sorted(roi_features)
    if not names:
        raise FeatureAlignmentError("no ROI features supplied")
    for name in names:
        if len(roi_features[name]) != len(times):
            raise FeatureAlignmentError(f"ROI {name} has a row-count mismatch")
    bouts = derive_bouts(labels, contexts)
    records: list[dict[str, Any]] = []
    for index, (timestamp, label, context, bout) in enumerate(
        zip(times, labels, contexts, bouts)
    ):
        records.append(
            {
                "record_type": "frame",
                "animal": animal,
                "trial": trial,
                "behavior_frame": index,
                "time_s": float(timestamp),
                "label": str(label),
                "context": str(context),
                "is_action": str(label) in ACTIONS,
                **bout,
                "roi": {name: float(roi_features[name][index]) for name in names},
            }
        )
    return records


def write_jsonl(path: Path, metadata: Mapping[str, Any], records: Sequence[Mapping[str, Any]]) -> None:
    """Write metadata followed by frame records as strict JSON Lines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(metadata), allow_nan=False, sort_keys=True) + "\n")
        for record in records:
            handle.write(json.dumps(dict(record), allow_nan=False, sort_keys=True) + "\n")


def build_aligned_features(
    *,
    h5_path: Path,
    capture_path: Path,
    dff_path: Path,
    behavior_path: Path,
    animal: str,
    trial: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Build ROI-preserving features from a manifest-validated trial."""
    manifest = build_manifest(
        h5_path=h5_path,
        capture_path=capture_path,
        dff_path=dff_path,
        behavior_path=behavior_path,
        animal=animal,
        trial=trial,
    )
    neural_times = manifest["axes"]["neural_seconds"]
    behavior_times_all = manifest["axes"]["behavior_seconds"]
    valid_indices = overlap_indices(neural_times, behavior_times_all)
    if not valid_indices:
        raise FeatureAlignmentError("no behavior frames overlap neural coverage")
    behavior_times = [behavior_times_all[index] for index in valid_indices]
    behavior = load_pickle(behavior_path)
    labels_all = behavior["Prediction"].astype(str).to_numpy().tolist()
    labels = [labels_all[index] for index in valid_indices]
    dff = load_pickle(dff_path)
    roi_features = {
        str(name): interpolate_series(neural_times, values, behavior_times)
        for name, values in sorted(dff.items())
    }
    contexts_all, context_samples = context_by_camera_frame(
        h5_path, capture_path, expected_frames=len(behavior_times_all)
    )
    contexts = [contexts_all[index] for index in valid_indices]
    records = frame_records(
        animal=animal,
        trial=trial,
        times=behavior_times,
        labels=labels,
        contexts=contexts,
        roi_features=roi_features,
    )
    summary = Counter(record["label"] for record in records)
    metadata = {
        "record_type": "metadata",
        "schema": "h4-aligned-features/v1",
        "verdict": "BIEN",
        "identity": manifest["identity"],
        "source_manifest": {
            "schema": manifest["schema"],
            "counts": manifest["counts"],
            "losses": manifest["losses"],
            "alignment": manifest["alignment"],
            "sources": manifest["sources"],
        },
        "feature_losses": {
            "behavior_frames_dropped_outside_neural_coverage": len(behavior_times_all) - len(valid_indices),
            "behavior_frames_materialized": len(valid_indices),
        },
        "roi_names": sorted(roi_features),
        "n_records": len(records),
        "n_bouts": (records[-1]["bout_id"] + 1) if records else 0,
        "label_counts": dict(summary),
        "context_sample_counts": context_samples,
        "innovation": [
            "[TITAN-INNOVATOR] ROI identity is retained instead of collapsing to nine global statistics",
            "[TITAN-INNOVATOR] contiguous label/context bouts are materialized for block-aware nulls",
            "[TITAN-INNOVATOR] CO2 context is reconstructed from the same ThorSync camera clock",
        ],
    }
    return metadata, records


def main() -> int:
    """Run the aligned feature materializer and write JSONL plus summary."""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("h5", "capture", "dff", "behavior"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--animal", required=True)
    parser.add_argument("--trial", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    args = parser.parse_args()
    try:
        metadata, records = build_aligned_features(
            h5_path=args.h5,
            capture_path=args.capture,
            dff_path=args.dff,
            behavior_path=args.behavior,
            animal=args.animal,
            trial=args.trial,
        )
        write_jsonl(args.out, metadata, records)
        args.summary_out.parent.mkdir(parents=True, exist_ok=True)
        args.summary_out.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    except (OSError, KeyError, TypeError, ValueError, FeatureAlignmentError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps({"verdict": "BIEN", "n_records": len(records), "n_bouts": metadata["n_bouts"], "roi_names": metadata["roi_names"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
