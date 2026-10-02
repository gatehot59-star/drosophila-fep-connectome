import json, os, hashlib
import numpy as np
import pandas as pd
from scipy import sparse

ROOT = '/workspace'
OUT = os.path.join(ROOT, 'h4_actions')
os.makedirs(OUT, exist_ok=True)
PARQUET = os.path.join(ROOT, 'connectivity.parquet')
ANNOT = os.path.join(ROOT, 'annotations.tsv')

def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def contains(frame, columns, term):
    mask = np.zeros(len(frame), dtype=bool)
    for col in columns:
        if col in frame:
            mask |= frame[col].fillna('').astype(str).str.contains(term, case=False, regex=False).to_numpy()
    return mask

def exact(frame, columns, values):
    mask = np.zeros(len(frame), dtype=bool)
    for col in columns:
        if col in frame:
            mask |= frame[col].fillna('').astype(str).isin(values).to_numpy()
    return mask

print('loading annotations', flush=True)
ann = pd.read_csv(ANNOT, sep='\t', low_memory=False)
print('loading connectivity', flush=True)
edges = pd.read_parquet(PARQUET, columns=['Presynaptic_ID','Postsynaptic_ID','Excitatory x Connectivity'])
edges.columns = ['pre','post','w']
ids = np.unique(np.concatenate([edges.pre.to_numpy(np.int64), edges.post.to_numpy(np.int64)]))
idx = {int(root): i for i, root in enumerate(ids)}
pre = np.fromiter((idx[int(x)] for x in edges.pre), dtype=np.int32, count=len(edges))
post = np.fromiter((idx[int(x)] for x in edges.post), dtype=np.int32, count=len(edges))
W = sparse.csr_matrix((edges.w.to_numpy(np.float64), (post, pre)), shape=(len(ids), len(ids)))
N = len(ids)
ann_root = ann.root_id.astype('Int64')
valid = ann_root.map(idx).notna().to_numpy()

def population(mask):
    roots = ann_root[mask & valid].astype(np.int64)
    return np.unique(np.array([idx[int(root)] for root in roots], dtype=np.int32))

actions = {
    'escape': population(exact(ann, ['cell_type','hemibrain_type'], {'LC4','LPLC2','LC6'})),
    'grooming': population(contains(ann, ['cell_sub_class','cell_type','hemibrain_type'], 'grooming')),
    'feeding': population(contains(ann, ['cell_sub_class','cell_type','hemibrain_type'], 'taste peg') | contains(ann, ['cell_type','hemibrain_type'], 'GRN')),
}
targets = {
    'GF': population(exact(ann, ['cell_type','hemibrain_type'], {'GF','DNp01'})),
    'descending': population(exact(ann, ['super_class'], {'descending'})),
    'motor': population(exact(ann, ['super_class'], {'motor'})),
    'MBON': population(contains(ann, ['cell_class','cell_type','hemibrain_type'], 'MBON')),
    'KC': population(contains(ann, ['cell_class','cell_type','hemibrain_type'], 'Kenyon')),
}
print('N', N, 'E', len(edges), 'action_sizes', {k:int(v.size) for k,v in actions.items()}, 'target_sizes', {k:int(v.size) for k,v in targets.items()}, flush=True)

def run(source, silence=None, tau=0.119, steps=120, on=20, off=80):
    state = np.zeros(N, dtype=np.float64)
    traces = {key: [] for key in targets}
    source = np.asarray(source, dtype=np.int32)
    amplitude = 1.0 / np.sqrt(max(1, source.size))
    for t in range(steps):
        input_state = np.zeros(N, dtype=np.float64)
        if on <= t < off:
            input_state[source] = amplitude
        state = (1.0 - tau) * state + tau * np.tanh(W.dot(state) + input_state)
        if silence is not None and silence.size:
            state[silence] = 0.0
        for key, members in targets.items():
            traces[key].append(float(np.sqrt(np.mean(state[members] ** 2))) if members.size else float('nan'))
    return traces

def summarize(traces):
    keys = list(targets)
    matrix = np.array([traces[key] for key in keys], dtype=float)
    peak = matrix[:, 80:].max(axis=1)
    profile = peak / peak.sum() if peak.sum() else peak
    return keys, peak, profile

def cosine(left, right):
    denom = np.linalg.norm(left) * np.linalg.norm(right)
    return float(np.dot(left, right) / denom) if denom else 0.0

result = {'meta': {'N': N, 'E': len(edges), 'tau': 0.119, 'steps': 120, 'stim_on': 20, 'stim_off': 80, 'action_definition': 'escape=LC4/LPLC2/LC6; grooming=annotation grooming; feeding=taste peg or GRN', 'parquet_md5': md5(PARQUET), 'annotations_md5': md5(ANNOT)}, 'actions': {}, 'pair_distances': {}, 'silencing': {}}
base = {}
for name, source in actions.items():
    traces = run(source)
    keys, peak, profile = summarize(traces)
    base[name] = {'n_source': int(source.size), 'keys': keys, 'peak': peak.tolist(), 'profile': profile.tolist(), 'traces': traces}
    result['actions'][name] = base[name]
for left_i, left in enumerate(actions):
    for right in list(actions)[left_i + 1:]:
        a = np.array(base[left]['profile']); b = np.array(base[right]['profile'])
        result['pair_distances'][left + '__' + right] = {'cosine': cosine(a,b), 'l1': float(np.abs(a-b).sum())}
for module, members in targets.items():
    result['silencing'][module] = {}
    for name, source in actions.items():
        traces = run(source, members)
        keys, peak, profile = summarize(traces)
        baseline = np.array(base[name]['profile'])
        result['silencing'][module][name] = {'peak': peak.tolist(), 'profile': profile.tolist(), 'delta_l1': float(np.abs(profile-baseline).sum()), 'traces': traces}
with open(os.path.join(OUT, 'h4_actions.json'), 'w') as handle:
    json.dump(result, handle)
print('BASELINE_PROFILES')
for name, data in base.items():
    print(name, 'n=', data['n_source'], 'peak=', [round(x,6) for x in data['peak']], 'profile=', [round(x,4) for x in data['profile']])
print('PAIR_DISTANCES', result['pair_distances'])
print('SILENCING_DELTA_L1')
for module, rows in result['silencing'].items():
    print(module, {name: round(row['delta_l1'],4) for name,row in rows.items()})
print('DONE', os.path.join(OUT, 'h4_actions.json'))
