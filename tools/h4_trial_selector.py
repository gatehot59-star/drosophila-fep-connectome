#!/usr/bin/env python3
"""Select Aymanns trials that can test H4 under a shared context."""
from __future__ import annotations
import argparse, json, pickle, types, sys
from pathlib import Path
import numpy as np
import pandas as pd
import h5py

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
    for i, index in enumerate(range(0, len(edges) - steps, steps)):
        out[edges[index]:edges[index + steps]] = i
    out[edges[-steps]:] = out[edges[-steps] - 1] + 1
    return out

def context_labels(h5_path: Path, capture_path: Path, n_frames: int) -> np.ndarray:
    with h5py.File(h5_path, "r") as f:
        basler = f["DI/Basler"][:].squeeze()
        counter = process_counter(f["CI/Frame Counter"][:].squeeze())
        capture = f["DI/Capture On"][:].squeeze().astype(bool)
        co2 = f["DI/CO2_Stim"][:].squeeze() > 0
    cam = process_cam(basler, json.loads(capture_path.read_text()))
    mask = capture & (counter >= 0)
    first = np.flatnonzero(mask)
    mask[max(0, int(first[0]) - 1)] = True
    cam, co2 = cam[mask], co2[mask]
    starts = np.r_[0, np.flatnonzero(np.diff(cam) > 0) + 1]
    stops = np.r_[starts[1:], len(cam)]
    ctx = np.array([bool(np.mean(co2[s:e]) > 0.5) for s, e in zip(starts, stops)])
    return ctx[:n_frames]

def select(beh_dir: Path, h5_dir: Path, capture_dir: Path) -> dict:
    patch_old_pandas()
    trials = []
    for beh_path in sorted(beh_dir.glob("*.pkl")):
        beh = load_pickle(beh_path)
        trial = int(beh.index.get_level_values("Trial")[0]) - 2
        labels = beh["Prediction"].astype(str).to_numpy()
        valid = np.isin(labels, ACTIONS)
        row = {"trial": trial, "behavior_file": beh_path.name, "n_behavior_frames": int(len(labels)), "action_counts": {k: int(v) for k, v in zip(*np.unique(labels[valid], return_counts=True))}}
        h5 = h5_dir / f"trial_{trial}.h5"
        cap = capture_dir / f"trial_{trial}.json"
        if h5.exists() and cap.exists():
            ctx = context_labels(h5, cap, len(labels))
            row["context_available"] = True
            row["contexts"] = {}
            for c in (False, True):
                mask = ctx == c
                vals = labels[mask & valid]
                row["contexts"]["co2_on" if c else "co2_off"] = {k: int(v) for k, v in zip(*np.unique(vals, return_counts=True))}
            eligible = [k for k, vals in row["contexts"].items() if len([a for a in vals if a in ACTIONS]) >= 2 and sum(vals.values()) >= 100]
            row["eligible_contexts"] = eligible
        else:
            row["context_available"] = False
            row["contexts"] = None
            row["eligible_contexts"] = []
        trials.append(row)
    eligible = [r for r in trials if r["eligible_contexts"]]
    return {"criterion": "same CO2 context, at least two action classes and >=100 labeled frames", "trials": trials, "eligible_trials": [r["trial"] for r in eligible], "n_trials": len(trials), "n_eligible": len(eligible)}

def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--behaviour-dir", type=Path, required=True); p.add_argument("--h5-dir", type=Path, required=True); p.add_argument("--capture-dir", type=Path, required=True); p.add_argument("--out", type=Path, required=True); a = p.parse_args(); result = select(a.behaviour_dir, a.h5_dir, a.capture_dir); a.out.write_text(json.dumps(result, indent=2)); print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
