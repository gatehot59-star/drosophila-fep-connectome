#!/usr/bin/env python3
"""Build one fail-closed provenance and alignment manifest from an Aymanns trial."""
from __future__ import annotations

import argparse
import hashlib
import json
import pickle
import sys
import types
from pathlib import Path
from typing import Any, Mapping, Sequence


def patch_old_pandas() -> None:
    """Allow historical pandas pickles to load on current pandas."""
    import pandas as pd
    module = types.ModuleType("pandas.core.indexes.numeric")
    module.Int64Index = pd.Index
    module.UInt64Index = pd.Index
    module.Float64Index = pd.Index
    sys.modules["pandas.core.indexes.numeric"] = module


def load_pickle(path: Path) -> Any:
    """Load one persisted dataset object."""
    with path.open("rb") as handle:
        return pickle.load(handle)


def sha256_file(path: Path) -> str:
    """Return the SHA-256 checksum of a source asset."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rising_edges(line: Sequence[float]) -> Any:
    """Return rising indices from a ThorSync digital line."""
    import numpy as np
    values = np.asarray(line, dtype=np.float64)
    return np.flatnonzero(np.diff(values) > 0) + 1


def process_camera_line(line: Sequence[float], metadata: Mapping[str, Any]) -> Any:
    """Reconstruct camera frame ids from capture metadata."""
    import numpy as np
    rising = rising_edges(line)
    frame_map = metadata["Frame Counts"]["0"]
    n_frames = max(map(int, frame_map.values())) + 1
    if len(rising) < n_frames:
        raise ValueError(f"camera pulses {len(rising)} < metadata frames {n_frames}")
    out = np.full(len(line), np.iinfo(np.int64).min, dtype=np.int64)
    current = 0
    for index, (start, stop) in enumerate(zip(rising[:n_frames], rising[1:n_frames + 1])):
        if int(frame_map[str(current + 1)]) <= index:
            current += 1
        out[start:stop] = current
    out[rising[n_frames - 1]:] = current
    return out


def process_frame_counter(line: Sequence[float], steps_per_frame: int = 3) -> Any:
    """Reconstruct 2P frame ids from the ThorSync frame-counter line."""
    import numpy as np
    rising = rising_edges(line)
    if len(rising) <= steps_per_frame:
        raise ValueError("frame counter has too few pulses")
    out = np.full(len(line), np.iinfo(np.int64).min, dtype=np.int64)
    for frame, index in enumerate(range(0, len(rising) - steps_per_frame, steps_per_frame)):
        out[rising[index]:rising[index + steps_per_frame]] = frame
    out[rising[-steps_per_frame]:] = out[rising[-steps_per_frame] - 1] + 1
    return out


def sync_seconds(length: int, frequency: int = 30000) -> Any:
    """Return the shared ThorSync seconds axis."""
    import numpy as np
    return np.arange(0, length / frequency, 1 / frequency)


def event_times(line: Sequence[int], times: Sequence[float]) -> Any:
    """Return seconds at which reconstructed frame ids start."""
    import numpy as np
    indexes = rising_edges(line)
    if line[0] >= 0:
        indexes = np.r_[0, indexes]
    return np.asarray(times)[indexes]


def validate_dff_lengths(dff: Mapping[str, Sequence[float]], expected: int) -> dict[str, int]:
    """Reject truncated or mixed-length ROI arrays before interpolation."""
    lengths = {str(key): len(values) for key, values in dff.items()}
    if not lengths:
        raise ValueError("DFF dictionary has no ROI arrays")
    wrong = {key: value for key, value in lengths.items() if value != expected}
    if wrong:
        raise ValueError(f"DFF length mismatch: expected {expected}, got {wrong}")
    return lengths


def build_manifest(*, h5_path: Path, capture_path: Path, dff_path: Path, behavior_path: Path, animal: str, trial: str) -> dict[str, Any]:
    """Reconstruct and validate one trial before feature construction."""
    import h5py
    import numpy as np
    patch_old_pandas()
    with h5py.File(h5_path, "r") as handle:
        basler = handle["DI/Basler"][:].squeeze()
        counter = handle["CI/Frame Counter"][:].squeeze()
        capture = handle["DI/Capture On"][:].squeeze().astype(bool)
    capture_metadata = json.loads(capture_path.read_text())
    camera = process_camera_line(basler, capture_metadata)
    frame_counter = process_frame_counter(counter, steps_per_frame=3)
    mask = capture & (frame_counter >= 0)
    indices = np.flatnonzero(mask)
    if len(indices) == 0:
        raise ValueError("capture mask contains no synchronized samples")
    mask[max(0, int(indices[0]) - 1)] = True
    camera, frame_counter = camera[mask], frame_counter[mask]
    thor_times = sync_seconds(len(frame_counter))
    behavior_times = event_times(camera, thor_times)
    neural_times = event_times(frame_counter, thor_times)
    behavior = load_pickle(behavior_path)
    if "Prediction" not in behavior:
        raise ValueError("behavior pickle has no Prediction column")
    labels = behavior["Prediction"].astype(str).to_numpy()
    dff = load_pickle(dff_path)
    roi_lengths = validate_dff_lengths(dff, len(neural_times))
    from h4_alignment_guard import validate_temporal_alignment
    alignment = validate_temporal_alignment(
        neural_times, behavior_times,
        neural_metadata={"animal": animal, "trial": trial, "timebase": "thor_sync_seconds"},
        behavior_metadata={"animal": animal, "trial": trial, "timebase": "thor_sync_seconds"},
        join_key="Time",
    )
    overlap_start = alignment["overlap_start"]
    overlap_end = alignment["overlap_end"]
    source_paths = (("h5", h5_path), ("capture", capture_path), ("dff", dff_path), ("behavior", behavior_path))
    sources = {name: {"name": path.name, "bytes": path.stat().st_size, "sha256": sha256_file(path)} for name, path in source_paths}
    losses = {
        "behavior_labels_unpaired": int(abs(len(labels) - len(behavior_times))),
        "roi_arrays_with_wrong_length": 0,
        "neural_frames_before_overlap": int(np.sum(neural_times < overlap_start)),
        "neural_frames_after_overlap": int(np.sum(neural_times > overlap_end)),
        "behavior_frames_before_overlap": int(np.sum(behavior_times < overlap_start)),
        "behavior_frames_after_overlap": int(np.sum(behavior_times > overlap_end)),
    }
    return {
        "schema": "h4-alignment-manifest/v1", "verdict": "BIEN",
        "method": "ThorSync-equivalent: Basler metadata crop, Frame Counter steps_per_frame=3, 30 kHz seconds, explicit Time join",
        "identity": {"animal": animal, "trial": trial, "timebase": "thor_sync_seconds"},
        "sources": sources,
        "counts": {"basler_rising_edges": int(len(rising_edges(basler))), "camera_frames": int(len(behavior_times)), "neural_frames": int(len(neural_times)), "behavior_labels": int(len(labels)), "roi_count": int(len(roi_lengths))},
        "losses": losses, "roi_lengths": roi_lengths, "alignment": alignment,
        "axes": {"neural_seconds": neural_times.tolist(), "behavior_seconds": behavior_times.tolist()},
    }


def main() -> int:
    """Validate one trial and write its JSON manifest."""
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("h5", "capture", "dff", "behavior"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--animal", required=True); parser.add_argument("--trial", required=True); parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = build_manifest(h5_path=args.h5, capture_path=args.capture, dff_path=args.dff, behavior_path=args.behavior, animal=args.animal, trial=args.trial)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"verdict": "MAL", "error": str(exc)}, sort_keys=True)); return 2
    args.out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"verdict": manifest["verdict"], "counts": manifest["counts"], "losses": manifest["losses"], "alignment": manifest["alignment"]}, indent=2)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
