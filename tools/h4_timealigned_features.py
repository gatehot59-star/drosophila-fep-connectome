#!/usr/bin/env python3
"""Time-align Brain-only DFF population features to behavior frames."""
from __future__ import annotations
import argparse, json, pickle, sys, types
from pathlib import Path
import numpy as np
import pandas as pd

ACTIONS = ["walking", "resting", "head_grooming", "foreleg_grooming", "hind_grooming"]

def patch_old_pandas():
    m = types.ModuleType("pandas.core.indexes.numeric"); m.Int64Index = pd.Index; m.UInt64Index = pd.Index; m.Float64Index = pd.Index; sys.modules["pandas.core.indexes.numeric"] = m

def load(p):
    with open(p, "rb") as h: return pickle.load(h)

def feature_matrix(dff, beh, stride):
    n = dff.loc[dff["Source file"] == "denoised"].reset_index()
    per = n.groupby("Frame").agg(time=("Time", "mean"), mean=("dFF", "mean"), std=("dFF", "std"), min=("dFF", "min"), max=("dFF", "max"), median=("dFF", "median"), q10=("dFF", lambda x: x.quantile(.1)), q25=("dFF", lambda x: x.quantile(.25)), q75=("dFF", lambda x: x.quantile(.75)), q90=("dFF", lambda x: x.quantile(.9))).sort_values("time")
    y = beh.reset_index()[["Frame", "Prediction"]].copy(); y["time"] = y["Frame"] / 100.0; y = y.loc[y["Prediction"].isin(ACTIONS)].iloc[::stride]
    cols = ["mean", "std", "min", "max", "median", "q10", "q25", "q75", "q90"]
    x = np.column_stack([np.interp(y.time.to_numpy(), per.time.to_numpy(), per[c].to_numpy()) for c in cols])
    return x, y["Prediction"].to_numpy(str)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--behaviour-dir',type=Path,required=True); p.add_argument('--dff-dir',type=Path,required=True); p.add_argument('--out',type=Path,required=True); p.add_argument('--stride',type=int,default=10); a=p.parse_args(); patch_old_pandas(); data={}
    for b in sorted(a.behaviour_dir.glob('*.pkl')):
        name=b.stem; x,y=feature_matrix(load(a.dff_dir/f'{name}.pkl'),load(b),a.stride); data[name]=(x,y)
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import balanced_accuracy_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    cross=[]; temporal=[]
    for held in sorted(data):
        train=[k for k in data if k!=held]; xt=np.vstack([data[k][0] for k in train]); yt=np.concatenate([data[k][1] for k in train]); xe,ye=data[held]; model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,class_weight='balanced')); model.fit(xt,yt); real=balanced_accuracy_score(ye,model.predict(xe)); null=[]
        for s in range(10):
            nm=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,class_weight='balanced')); nm.fit(xt,np.random.default_rng(7000+s).permutation(yt)); null.append(balanced_accuracy_score(ye,nm.predict(xe)))
        cross.append({'held_out':held,'n':len(ye),'balanced_accuracy':float(real),'shuffle_mean':float(np.mean(null))})
        x,y= data[held]; cut=len(y)//2; em=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,class_weight='balanced')); em.fit(x[:cut],y[:cut]); lm=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,class_weight='balanced')); lm.fit(x[cut:],y[cut:]); temporal.append({'animal':held,'early_to_late':float(balanced_accuracy_score(y[cut:],em.predict(x[cut:]))),'late_to_early':float(balanced_accuracy_score(y[:cut],lm.predict(x[:cut]))),'n':len(y)})
    out={'method':'DFF population summaries aggregated at 2P Time then linearly interpolated to behavior time=Frame/100 s','stride':a.stride,'n_animals':len(data),'cross_animal':cross,'cross_mean':float(np.mean([r['balanced_accuracy'] for r in cross])),'cross_shuffle_mean':float(np.mean([r['shuffle_mean'] for r in cross])),'temporal':temporal}; a.out.write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
