#!/usr/bin/env python3
"""Pre-falsador H4: actividad neural Aymanns alineada a acciones por trial.

La alineación lineal es solo una premedición cuando no se dispone del sync H5
correspondiente. El resultado no habilita claims sobre root_id FlyWire.
"""
from __future__ import annotations
import argparse
import glob
import json
import pickle
import sys
import types
from pathlib import Path
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


def align_trace(values: np.ndarray, n_frames: int) -> np.ndarray:
    source = np.linspace(0.0, 1.0, len(values))
    target = np.linspace(0.0, 1.0, n_frames)
    return np.interp(target, source, np.asarray(values, dtype=float))


def trial_number(frame: pd.DataFrame) -> int:
    return int(frame.index.get_level_values("Trial")[0]) - 2


def run(behaviour_dir: Path, dff_dir: Path) -> dict:
    patch_old_pandas()
    records = []
    for beh_path in sorted(behaviour_dir.glob("*.pkl")):
        trial = load(beh_path)
        trial_id = trial_number(trial)
        dff_path = dff_dir / f"{trial_id}.p"
        if not dff_path.exists():
            continue
        dff = load(dff_path)
        labels = trial["Prediction"].astype(str).to_numpy()
        keep = np.isin(labels, ["walking", "resting", "head_grooming", "foreleg_grooming", "hind_grooming"])
        x = np.column_stack([align_trace(dff[key], len(labels)) for key in sorted(dff)])
        x = x[keep]
        y = labels[keep]
        if len(np.unique(y)) < 2:
            continue
        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
        counts = np.unique(y, return_counts=True)[1]
        folds = max(2, min(5, int(np.min(counts))))
        score = float(np.mean(cross_val_score(model, x, y, cv=folds, scoring="accuracy")))
        rng = np.random.default_rng(1000 + trial_id)
        shuffled = rng.permutation(y)
        null = float(np.mean(cross_val_score(model, x, shuffled, cv=folds, scoring="accuracy")))
        means = {label: np.mean(x[y == label], axis=0).tolist() for label in sorted(np.unique(y))}
        rows = []
        for left in sorted(means):
            for right in sorted(means):
                if left < right:
                    a = np.asarray(means[left]); b = np.asarray(means[right])
                    cosine = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))) if np.linalg.norm(a) and np.linalg.norm(b) else 0.0
                    rows.append({"left": left, "right": right, "cosine": cosine})
        records.append({"trial": trial_id, "n_frames": int(len(y)), "classes": {k: int(v) for k, v in zip(*np.unique(y, return_counts=True))}, "accuracy": score, "shuffled_accuracy": null, "accuracy_delta": score - null, "means": means, "pair_cosines": rows})
    return {"method": "linear resampling of 1067-frame DFF to 7440 behavioral frames; trial-block identity preserved", "trials": records, "n_trials": len(records), "no_root_mapping": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--behaviour-dir", type=Path, required=True)
    parser.add_argument("--dff-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.behaviour_dir, args.dff_dir)
    args.out.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
