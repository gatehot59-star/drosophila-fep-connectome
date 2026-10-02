#!/usr/bin/env python3
"""Leave-one-fly-out neural action validation for Aymanns/Brain-only data."""
from __future__ import annotations
import argparse, json, pickle, sys, types
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ACTIONS = ["walking", "resting", "head_grooming", "foreleg_grooming", "hind_grooming"]

def patch_old_pandas() -> None:
    module = types.ModuleType("pandas.core.indexes.numeric")
    module.Int64Index = pd.Index
    module.UInt64Index = pd.Index
    module.Float64Index = pd.Index
    sys.modules["pandas.core.indexes.numeric"] = module

def load(path: Path):
    with path.open("rb") as handle:
        return pickle.load(handle)

def aggregate_features(dff: pd.DataFrame, behaviour: pd.DataFrame, stride: int) -> tuple[np.ndarray, np.ndarray]:
    neural = dff.loc[dff["Source file"] == "denoised", ["dFF", "ROI"]].copy().reset_index()
    neural = neural.sort_values(["Frame", "ROI"])
    frame_stats = neural.groupby("Frame")["dFF"].agg(["mean", "std", "min", "max", "median"]).reset_index()
    quant = neural.groupby("Frame")["dFF"].quantile([0.1, 0.25, 0.75, 0.9]).unstack().reset_index()
    quant.columns = ["Frame", "q10", "q25", "q75", "q90"]
    features = frame_stats.merge(quant, on="Frame", how="inner")
    labels = behaviour.reset_index()[["Frame", "Prediction"]].rename(columns={"Prediction": "label"})
    joined = features.merge(labels, on="Frame", how="inner")
    joined = joined.loc[joined.label.isin(ACTIONS)].iloc[::stride].copy()
    cols = ["mean", "std", "min", "max", "median", "q10", "q25", "q75", "q90"]
    return joined[cols].to_numpy(float), joined.label.to_numpy(str)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--behaviour-dir", type=Path, required=True)
    parser.add_argument("--dff-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--stride", type=int, default=10)
    args = parser.parse_args()
    patch_old_pandas()
    data = {}
    for beh_path in sorted(args.behaviour_dir.glob("*.pkl")):
        name = beh_path.stem
        dff_path = args.dff_dir / f"{name}.pkl"
        x, y = aggregate_features(load(dff_path), load(beh_path), args.stride)
        data[name] = {"x": x, "y": y}
    results = []
    for held_out in sorted(data):
        train_names = [name for name in sorted(data) if name != held_out]
        x_train = np.vstack([data[name]["x"] for name in train_names])
        y_train = np.concatenate([data[name]["y"] for name in train_names])
        x_test, y_test = data[held_out]["x"], data[held_out]["y"]
        model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced"))
        model.fit(x_train, y_train)
        pred = model.predict(x_test)
        labels = sorted(set(ACTIONS) & set(y_test))
        score = float(balanced_accuracy_score(y_test, pred, labels=labels))
        majority = max((np.mean(y_test == label) for label in labels), default=0.0)
        null_scores = []
        for seed in range(10):
            rng = np.random.default_rng(7000 + seed + int(held_out.replace("Fly", "")))
            shuffled = rng.permutation(y_train)
            null_model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced"))
            null_model.fit(x_train, shuffled)
            null_scores.append(float(balanced_accuracy_score(y_test, null_model.predict(x_test), labels=labels)))
        results.append({"held_out": held_out, "n_test": int(len(y_test)), "class_counts": {k: int(v) for k, v in zip(*np.unique(y_test, return_counts=True))}, "balanced_accuracy": score, "majority_accuracy": float(majority), "shuffle_mean": float(np.mean(null_scores)), "shuffle_sd": float(np.std(null_scores, ddof=1)), "shuffle_scores": null_scores})
    output = {"method": "population summary features (9 stats), denoised DFF, every Nth frame, leave-one-fly-out; no frames from held-out fly in training", "stride": args.stride, "n_flies": len(data), "results": results, "mean_balanced_accuracy": float(np.mean([r["balanced_accuracy"] for r in results])), "mean_shuffle": float(np.mean([r["shuffle_mean"] for r in results]))}
    args.out.write_text(json.dumps(output, indent=2))
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
