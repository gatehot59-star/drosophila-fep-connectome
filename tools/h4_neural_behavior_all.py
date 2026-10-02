#!/usr/bin/env python3
"""Run the ThorSync-aligned neural H4 falsifier across all Aymanns trials."""
from __future__ import annotations
import argparse, json, pickle, sys, types
from pathlib import Path
import h5py
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ACTIONS = ["walking", "resting", "head_grooming", "foreleg_grooming", "hind_grooming"]


def patch_old_pandas() -> None:
    module = types.ModuleType("pandas.core.indexes.numeric")
    module.Int64Index = pd.Index
    module.UInt64Index = pd.Index
    module.Float64Index = pd.Index
    sys.modules["pandas.core.indexes.numeric"] = module


def load_pickle(path: Path):
    with path.open("rb") as handle:
        return pickle.load(handle)


def rising(line: np.ndarray) -> np.ndarray:
    return np.flatnonzero(np.diff(line.astype(np.float64)) > 0) + 1


def process_cam(line: np.ndarray, metadata: dict) -> np.ndarray:
    edges = rising(line)
    n = max(map(int, metadata["Frame Counts"]["0"].values())) + 1
    if len(edges) < n:
        raise ValueError(f"camera pulses {len(edges)} < metadata frames {n}")
    out = np.ones(len(line), dtype=np.int64) * np.iinfo(np.int64).min
    mapping = metadata["Frame Counts"]["0"]
    cur = 0
    for i, (start, stop) in enumerate(zip(edges[:n], edges[1:n + 1])):
        if int(mapping[str(cur + 1)]) <= i:
            cur += 1
        out[start:stop] = cur
    out[edges[n - 1]:] = cur
    return out


def process_counter(line: np.ndarray, steps: int = 3) -> np.ndarray:
    out = np.ones(len(line), dtype=np.int64) * np.iinfo(np.int64).min
    edges = rising(line)
    if len(edges) <= steps:
        out[edges[0]:] = 0
        return out
    for i, index in enumerate(range(0, len(edges) - steps, steps)):
        out[edges[index]:edges[index + steps]] = i
    out[edges[-steps]:] = out[edges[-steps] - 1] + 1
    return out


def align_trial(h5_path: Path, capture_path: Path, dff_path: Path, behaviour_path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    with h5py.File(h5_path, "r") as handle:
        basler = handle["DI/Basler"][:].squeeze()
        counter = process_counter(handle["CI/Frame Counter"][:].squeeze())
        capture = handle["DI/Capture On"][:].squeeze().astype(bool)
        co2_raw = handle["DI/CO2_Stim"][:].squeeze() > 0
    cam = process_cam(basler, json.loads(capture_path.read_text()))
    mask = capture & (counter >= 0)
    first = np.flatnonzero(mask)
    mask[max(0, int(first[0]) - 1)] = True
    cam, co2_raw = cam[mask], co2_raw[mask]
    starts = np.r_[0, np.flatnonzero(np.diff(cam) > 0) + 1]
    stops = np.r_[starts[1:], len(cam)]
    co2 = np.array([bool(np.mean(co2_raw[s:e]) > 0.5) for s, e in zip(starts, stops)])
    times = np.arange(len(counter[mask])) / 30000.0
    cam_times = times[starts]
    counter_times = times[rising(counter[mask])]
    dff = load_pickle(dff_path)
    features = []
    for key in sorted(dff):
        values = np.asarray(dff[key], dtype=float)
        n = min(len(values), len(counter_times))
        features.append(np.interp(cam_times, counter_times[:n], values[:n]))
    x = np.column_stack(features)
    behaviour = load_pickle(behaviour_path)
    y = behaviour["Prediction"].astype(str).to_numpy()
    n = min(len(y), len(x), len(co2))
    return x[:n], y[:n], co2[:n]


def score(x: np.ndarray, y: np.ndarray, seed: int) -> dict:
    keep = np.isin(y, ACTIONS)
    x, y = x[keep], y[keep]
    labels, counts = np.unique(y, return_counts=True)
    if len(labels) < 2:
        return {"n_frames": int(len(y)), "classes": {}, "accuracy": None, "shuffled_accuracy": None, "accuracy_delta": None, "pair_cosines": []}
    folds = max(2, min(5, int(np.min(counts))))
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    accuracy = float(np.mean(cross_val_score(model, x, y, cv=folds, scoring="accuracy")))
    shuffled = np.random.default_rng(seed).permutation(y)
    null = float(np.mean(cross_val_score(model, x, shuffled, cv=folds, scoring="accuracy")))
    means = {label: np.mean(x[y == label], axis=0) for label in labels}
    pairs = []
    for left in sorted(means):
        for right in sorted(means):
            if left < right:
                a, b = means[left], means[right]
                den = np.linalg.norm(a) * np.linalg.norm(b)
                pairs.append({"left": left, "right": right, "cosine": float(np.dot(a, b) / den) if den else 0.0})
    return {"n_frames": int(len(y)), "classes": {k: int(v) for k, v in zip(labels, counts)}, "accuracy": accuracy, "shuffled_accuracy": null, "accuracy_delta": accuracy - null, "pair_cosines": pairs}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h5-dir", type=Path, required=True)
    parser.add_argument("--capture-dir", type=Path, required=True)
    parser.add_argument("--dff-dir", type=Path, required=True)
    parser.add_argument("--behaviour-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    patch_old_pandas()
    trials = []
    for beh_path in sorted(args.behaviour_dir.glob("*.pkl")):
        trial = int(load_pickle(beh_path).index.get_level_values("Trial")[0]) - 2
        paths = (args.h5_dir / f"trial_{trial}.h5", args.capture_dir / f"trial_{trial}.json", args.dff_dir / f"{trial}.p")
        if not all(path.exists() for path in paths):
            raise FileNotFoundError(f"missing files for trial {trial}: {paths}")
        x, y, co2 = align_trial(paths[0], paths[1], paths[2], beh_path)
        rows = {"trial": trial, "all": score(x, y, 1000 + trial)}
        for context, value in [("co2_off", False), ("co2_on", True)]:
            rows[context] = score(x[co2 == value], y[co2 == value], 2000 + trial)
            rows[context]["n_context_frames"] = int(np.sum(co2 == value))
        trials.append(rows)
    result = {"method": "official utils2p-equivalent ThorSync alignment; steps_per_frame=3; 30 kHz; per-trial and CO2-context scores", "trials": trials, "n_trials": len(trials)}
    args.out.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
