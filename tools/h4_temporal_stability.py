#!/usr/bin/env python3
"""Measure within-animal temporal stability of neural action decoding."""
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

def features(dff: pd.DataFrame, behaviour: pd.DataFrame, stride: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    neural = dff.loc[dff["Source file"] == "denoised", ["dFF", "ROI"]].reset_index()
    stats = neural.groupby("Frame")["dFF"].agg(["mean", "std", "min", "max", "median"]).reset_index()
    quant = neural.groupby("Frame")["dFF"].quantile([0.1, 0.25, 0.75, 0.9]).unstack().reset_index()
    quant.columns = ["Frame", "q10", "q25", "q75", "q90"]
    joined = stats.merge(quant, on="Frame").merge(behaviour.reset_index()[["Frame", "Prediction"]].rename(columns={"Prediction": "label"}), on="Frame")
    joined = joined.loc[joined.label.isin(ACTIONS)].iloc[::stride].copy()
    cols = ["mean", "std", "min", "max", "median", "q10", "q25", "q75", "q90"]
    order = np.arange(len(joined), dtype=int)
    return joined[cols].to_numpy(float), joined.label.to_numpy(str), order

def score(x_train, y_train, x_test, y_test, seed):
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced"))
    model.fit(x_train, y_train)
    real = float(balanced_accuracy_score(y_test, model.predict(x_test)))
    rng = np.random.default_rng(seed)
    shuffled = rng.permutation(y_train)
    null_model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced"))
    null_model.fit(x_train, shuffled)
    null = float(balanced_accuracy_score(y_test, null_model.predict(x_test)))
    return {"balanced_accuracy": real, "shuffle_accuracy": null, "delta": real - null}

def main():
    p = argparse.ArgumentParser(); p.add_argument("--behaviour-dir", type=Path, required=True); p.add_argument("--dff-dir", type=Path, required=True); p.add_argument("--out", type=Path, required=True); p.add_argument("--stride", type=int, default=10); a = p.parse_args(); patch_old_pandas(); results=[]
    for beh_path in sorted(a.behaviour_dir.glob("*.pkl")):
        name=beh_path.stem; x,y,t=features(load(a.dff_dir/f"{name}.pkl"),load(beh_path),a.stride); n=len(y); cut=n//2; early,late=t<cut,t>=cut; row={"animal":name,"n_frames":n,"early_classes":{k:int(v) for k,v in zip(*np.unique(y[early],return_counts=True))},"late_classes":{k:int(v) for k,v in zip(*np.unique(y[late],return_counts=True))},"early_to_late":score(x[early],y[early],x[late],y[late],9000+int(name.replace('Fly',''))),"late_to_early":score(x[late],y[late],x[early],y[early],9100+int(name.replace('Fly','')))}; results.append(row)
    out={"method":"within-animal chronological half split on denoised population summary features; no frames cross the split","stride":a.stride,"n_animals":len(results),"results":results,"mean_early_to_late_delta":float(np.mean([r['early_to_late']['delta'] for r in results]))}
    a.out.write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))

if __name__ == "__main__": main()
