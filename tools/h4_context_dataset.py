#!/usr/bin/env python3
"""Falsador H4 para datos Dallmann: contexto compartido, acción y actividad neural."""
import argparse, json
from pathlib import Path
import pandas as pd

ACTIONS = ['L1_walk', 'L1_groom', 'L1_other', 'L1_rest']
REQUIRED = {'animal_id','trial','frame','time','ball','platform','analyze','calcium',*ACTIONS}

def load(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f'missing columns: {sorted(missing)}')
    return df.loc[df.analyze.astype(bool)].copy()

def summarize(df: pd.DataFrame) -> dict:
    rows = []
    for ctx, g in df.groupby(['ball', 'platform'], dropna=False):
        label = g[ACTIONS].idxmax(axis=1)
        valid = g[ACTIONS].max(axis=1) > 0
        label = label[valid]
        means = {a: float(g.loc[label.index[label == a], 'calcium'].mean()) if (label == a).any() else None for a in ACTIONS}
        rows.append({'ball': int(ctx[0]), 'platform': int(ctx[1]), 'n_frames': int(valid.sum()), 'n_animals': int(g.loc[valid, 'animal_id'].nunique()), 'n_trials': int(g.loc[valid, 'trial'].nunique()), 'action_counts': label.value_counts().to_dict(), 'calcium_mean_by_action': means})
    return {'rows': rows, 'n_rows': int(len(df)), 'n_animals': int(df.animal_id.nunique()), 'n_trials': int(df.trial.nunique()), 'action_columns': ACTIONS}

def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument('parquet', type=Path); ap.add_argument('--out', type=Path, required=True); args = ap.parse_args()
    df = load(args.parquet); result = summarize(df); result['source'] = str(args.parquet); args.out.write_text(json.dumps(result, indent=2)); print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
