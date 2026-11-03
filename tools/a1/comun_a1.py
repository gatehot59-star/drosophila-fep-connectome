#!/usr/bin/env python3
"""Primitivas cerradas de H_MECANISMO_RELEVOS16/009-A1."""
import hashlib, json
from pathlib import Path
import numpy as np
PROTOCOL='009-A1'; DT_MS=0.1; DURATION_MS=1000.0; SEEDS=range(20)
def seed_for(group,s,index,role):
 text=f'{PROTOCOL}|{group}|{int(s)}|{int(index)}|{role}'
 return text,int(hashlib.sha256(text.encode()).hexdigest()[:16],16)
def bernoulli_events(seed,rate_hz,ticks=10000):
 if rate_hz<0 or rate_hz>10000: raise ValueError('rate fuera de rango')
 return np.flatnonzero(np.random.Generator(np.random.PCG64(seed)).random(ticks)<rate_hz*0.0001).astype(np.int64)
def replay_ticks(seed,count=50,ticks=10000):
 if count<0 or count>ticks: raise ValueError('count fuera de rango')
 u=np.random.Generator(np.random.PCG64(seed)).random(ticks)
 return np.sort(np.argsort(u,kind='stable')[:count]).astype(np.int64)
def sha_json_indices(values): return hashlib.sha256((json.dumps(sorted(map(int,values)),separators=(',',':'))+'\n').encode()).hexdigest()
def sha_array(a):
 a=np.asarray(a); return hashlib.sha256(a.astype(a.dtype.newbyteorder('<'),copy=False).tobytes()).hexdigest()
def row_key(pre,post): return np.asarray(pre,dtype=np.int64)*1000000+np.asarray(post,dtype=np.int64)
def mask_hash(rows): return hashlib.sha256(np.asarray(sorted(set(map(int,rows))),dtype='<i8').tobytes()).hexdigest()
def unique_union(*rows): return np.unique(np.concatenate([np.asarray(x,dtype=np.int64) for x in rows]))
