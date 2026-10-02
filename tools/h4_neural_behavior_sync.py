#!/usr/bin/env python3
"""H4 pre-falsifier using the authors' ThorSync alignment procedure."""
from __future__ import annotations
import argparse
import json
import pickle
import sys
import types
from pathlib import Path
import h5py
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def patch_old_pandas() -> None:
    module = types.ModuleType("pandas.core.indexes.numeric")
    module.Int64Index = pd.Index
    module.UInt64Index = pd.Index
    module.Float64Index = pd.Index
    sys.modules["pandas.core.indexes.numeric"] = module


def load(path: Path):
    with path.open("rb") as handle:
        return pickle.load(handle)


def edges(line: np.ndarray) -> np.ndarray:
    return np.flatnonzero(np.diff(line.astype(np.float64)) > 0) + 1


def process_cam_line(line: np.ndarray, metadata: dict) -> np.ndarray:
    rising = edges(line)
    n_frames = max(map(int, metadata["Frame Counts"]["0"].values())) + 1
    if len(rising) < n_frames:
        raise ValueError(f"camera pulses {len(rising)} < metadata frames {n_frames}")
    out = np.ones(line.shape[0], dtype=np.int64) * np.iinfo(np.int64).min
    frame_map = metadata["Frame Counts"]["0"]
    current = 0
    for i, (start, stop) in enumerate(zip(rising[:n_frames], rising[1:n_frames + 1])):
        if int(frame_map[str(current + 1)]) <= i:
            current += 1
        out[start:stop] = current
    out[rising[n_frames - 1]:] = current
    return out


def process_frame_counter(line: np.ndarray, steps_per_frame: int = 3) -> np.ndarray:
    out = np.ones(line.shape[0], dtype=np.int64) * np.iinfo(np.int64).min
    rising = edges(line)
    if len(rising) <= steps_per_frame:
        out[rising[0]:] = 0
        return out
    for i, index in enumerate(range(0, len(rising) - steps_per_frame, steps_per_frame)):
        out[rising[index]:rising[index + steps_per_frame]] = i
    out[rising[-steps_per_frame]:] = out[rising[-steps_per_frame] - 1] + 1
    return out


def get_times(length: int, freq: int = 30000) -> np.ndarray:
    return np.arange(0, length / freq, 1 / freq)


def start_times(line: np.ndarray, times: np.ndarray) -> np.ndarray:
    idx = edges(line)
    if line[0] >= 0:
        idx = np.r_[0, idx]
    return times[idx]


def align_trial(h5_path: Path, capture_path: Path, dff_path: Path, behaviour_path: Path) -> dict:
    with h5py.File(h5_path, "r") as handle:
        basler = handle["DI/Basler"][:].squeeze()
        counter = handle["CI/Frame Counter"][:].squeeze()
        capture = handle["DI/Capture On"][:].squeeze().astype(bool)
    capture_info = json.loads(capture_path.read_text())
    cam = process_cam_line(basler, capture_info)
    fc = process_frame_counter(counter, steps_per_frame=3)
    mask = capture & (fc >= 0)
    indices = np.flatnonzero(mask)
    mask[max(0, int(indices[0]) - 1)] = True
    cam = cam[mask]
    fc = fc[mask]
    times = get_times(len(fc))
    cam_times = start_times(cam, times)
    dff_times = start_times(fc, times)
    behaviour = load(behaviour_path)
    labels = behaviour["Prediction"].astype(str).to_numpy()
    dff = load(dff_path)
    features = []
    for key in sorted(dff):
        values = np.asarray(dff[key], dtype=float)
        if len(values) != len(dff_times):
            values = values[:len(dff_times)]
        features.append(np.interp(cam_times, dff_times[:len(values)], values))
    x = np.column_stack(features)
    n = min(len(labels), len(x))
    labels = labels[:n]
    x = x[:n]
    keep = np.isin(labels, ["walking", "resting", "head_grooming", "foreleg_grooming", "hind_grooming"])
    x, y = x[keep], labels[keep]
    counts = np.unique(y, return_counts=True)[1]
    folds = max(2, min(5, int(np.min(counts))))
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    accuracy = float(np.mean(cross_val_score(model, x, y, cv=folds, scoring="accuracy")))
    shuffled = np.random.default_rng(1007).permutation(y)
    null = float(np.mean(cross_val_score(model, x, shuffled, cv=folds, scoring="accuracy")))
    means = {label: np.mean(x[y == label], axis=0).tolist() for label in sorted(np.unique(y))}
    pairs = []
    for left in sorted(means):
        for right in sorted(means):
            if left < right:
                a, b = np.asarray(means[left]), np.asarray(means[right])
                pairs.append({"left": left, "right": right, "cosine": float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))})
    return {"n_h5_camera_rises": int(len(edges(basler))), "n_camera_frames": int(len(cam_times)), "n_2p_frames": int(len(dff_times)), "n_behavior_frames": int(len(labels)), "classes": {k: int(v) for k, v in zip(*np.unique(y, return_counts=True))}, "accuracy": accuracy, "shuffled_accuracy": null, "accuracy_delta": accuracy - null, "pair_cosines": pairs, "method": "official utils2p-equivalent ThorSync processing: Basler metadata crop, frame counter steps_per_frame=3, 30 kHz times, interpolation to camera frames"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h5", type=Path, required=True)
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--dff", type=Path, required=True)
    parser.add_argument("--behaviour", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    patch_old_pandas()
    result = align_trial(args.h5, args.capture, args.dff, args.behaviour)
    args.out.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
