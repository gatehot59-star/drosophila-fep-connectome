#!/usr/bin/env python3
"""Materializa identidades, mascaras, poblaciones y eventos de 009-A1."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np,pyarrow.parquet as pq
from comun_a1 import *
PIN_PARQUET='efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347'; PIN_UNITS='fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df'
def file_sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def load(sello,parquet,units):
 tab=pq.read_table(parquet,columns=['Presynaptic_Index','Postsynaptic_Index','Connectivity','Excitatory x Connectivity']); pre=tab.column(0).to_numpy().astype(np.int64); post=tab.column(1).to_numpy().astype(np.int64); con=tab.column(2).to_numpy().astype(np.int64); w=tab.column(3).to_numpy().astype(np.int64); u=np.load(units); D=u['D']; sl=u['sl']; tipo=u['tipo']; root=u['root']; bypre={i:np.flatnonzero(pre==i) for i in np.unique(pre)}; bypost={i:np.flatnonzero(post==i) for i in np.unique(post)}; elig=D>=0
 def out(i): return bypre.get(int(i),np.empty(0,dtype=np.int64))
 def inp(i): return bypost.get(int(i),np.empty(0,dtype=np.int64))
 def dp(x,G):
  r=out(x); r=r[(w[r]<0)&elig[post[r]]]; return np.array(sorted(set(post[r].tolist())-set(map(int,G))),dtype=np.int64)
 def rows_q1(G,x): return np.concatenate([out(g)[post[out(g)]==x] for g in G])
 def qcol(G,dpv): return np.concatenate([out(g)[(w[out(g)]>0)&np.isin(post[out(g)],dpv)] for g in G])
 def qxd(x,dpv): r=out(x); return r[(w[r]<0)&np.isin(post[r],dpv)]
 seal=json.load(open(sello)); rel=[]; hubs={}
 for z in seal:
  code=z['code'][:3]; d,x=int(z['d_idx']),int(z['x_idx']); dpv=dp(x,[d]); q1=rows_q1([d],x); qc=qcol([d],dpv); qd=qxd(x,dpv); weak=inp(x); weak=weak[(w[weak]>0)&elig[pre[weak]]&(pre[weak]!=d)&(con[weak]>=1)&(con[weak]<=5)]; weakrow=None
  if weak.size:
   mx=con[weak].max(); cand=weak[con[weak]==mx]; wi=int(cand[np.argmin(pre[cand])]); weakrow=[int(pre[wi]),int(post[wi]),int(w[wi])]
  rel.append({'id':code,'driver':d,'hub':x,'driver_root':int(root[d]),'hub_root':int(root[x]),'Dprime':{'indices':dpv.tolist(),'n':int(dpv.size),'sha256':sha_json_indices(dpv)},'masks':{'Q1':np.unique(q1).tolist(),'QCOL':np.unique(qc).tolist(),'Q1_QCOL':unique_union(q1,qc).tolist(),'QXD':np.unique(qd).tolist(),'Q1_QXD':unique_union(q1,qd).tolist()},'weak_row':weakrow,'regimen':'A' if z.get('regimen_visual_S') else 'B'})
 for x,G in [(33912,[41594,104203,19410]),(58129,[58878,71368]),(19257,[111205,130297]),(122969,[27878,20277]),(45293,[129110,53975]),(112031,[84751,69226])]:
  dpv=dp(x,G); q1=rows_q1(G,x); qc=qcol(G,dpv); qd=qxd(x,dpv); hubs[str(x)]={'hub':x,'drivers':G,'Dprime':{'indices':dpv.tolist(),'n':int(dpv.size),'sha256':sha_json_indices(dpv)},'masks':{'Q1':np.unique(q1).tolist(),'QCOL':np.unique(qc).tolist(),'Q1_QCOL':unique_union(q1,qc).tolist(),'QXD':np.unique(qd).tolist(),'Q1_QXD':unique_union(q1,qd).tolist()}}
 events=[]
 for g in ['A_LPLC1_right','B_R01','B_H2','C_H2']:
  for s in SEEDS:
   role='replay' if g.startswith('C_') else 'driver'; idx=19257 if g=='C_H2' else 59804; text,seed=seed_for(g,s,idx,role); ev=replay_ticks(seed) if role=='replay' else bernoulli_events(seed,50); events.append({'group':g,'s':s,'index':idx,'role':role,'seed_text':text,'seed':seed,'events':ev.tolist(),'sha256':sha_array(ev)})
 return {'protocol_id':PROTOCOL,'inputs':{'parquet_sha256':file_sha(parquet),'units_sha256':file_sha(units),'rows':int(pre.size)},'parameters':{'dt_ms':DT_MS,'duration_ms':DURATION_MS,'seeds':20,'poisson_discretization':'Bernoulli N=1','seed_bits':64},'relays':rel,'hubs':hubs,'events':events}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--parquet',required=True); ap.add_argument('--units',required=True); ap.add_argument('--sello',required=True); ap.add_argument('--out',required=True); a=ap.parse_args(); m=load(a.sello,a.parquet,a.units); assert m['inputs']['parquet_sha256']==PIN_PARQUET; assert m['inputs']['units_sha256']==PIN_UNITS; Path(a.out).write_text(json.dumps(m,sort_keys=True,indent=2)+'\n'); print('MANIFEST',a.out,file_sha(a.out)); print('RELAYS',len(m['relays']),'HUBS',len(m['hubs']),'EVENTS',len(m['events']))
if __name__=='__main__': main()
