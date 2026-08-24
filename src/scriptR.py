import time, json, sys
import numpy as np
import pandas as pd
from scipy import sparse as sp
from scipy.sparse.linalg import eigs
from scipy import stats as spstats
t0=time.time()
N_STEPS=200; TAU=0.119; T_START=10; T_END=60
T_FINE=list(range(0,N_STEPS,5))
print('=== SCRIPT R (python real) ===', flush=True)
df=pd.read_parquet('connectivity.parquet', columns=['Presynaptic_Index','Postsynaptic_Index','Excitatory x Connectivity'])
pre=df['Presynaptic_Index'].values.astype(np.int32)
post=df['Postsynaptic_Index'].values.astype(np.int32)
wts=df['Excitatory x Connectivity'].values.astype(np.float32)
N=int(max(pre.max(),post.max()))+1
W_raw=sp.csr_matrix((wts,(pre,post)),shape=(N,N),dtype=np.float32)
W_raw.eliminate_zeros()
print('N=%d E=%d nnz=%d' % (N, len(pre), W_raw.nnz), flush=True)
del df
ann=pd.read_csv('annotations.tsv', sep=chr(9), low_memory=False)
print('annot rows=%d' % len(ann), flush=True)
ids=np.union1d(pd.read_parquet('connectivity.parquet',columns=['Presynaptic_ID'])['Presynaptic_ID'].values, pd.read_parquet('connectivity.parquet',columns=['Postsynaptic_ID'])['Postsynaptic_ID'].values)
ids.sort()
id2i={int(r):i for i,r in enumerate(ids)}
print('idmap=%d' % len(id2i), flush=True)
def byidx(mask):
    rr=ann.loc[mask,'root_id'].values
    return np.array([id2i[int(x)] for x in rr if int(x) in id2i], dtype=np.int64)
idx_S=byidx(ann['flow']=='afferent')
idx_A=byidx(ann['flow']=='efferent')
idx_mu=byidx(ann['flow']=='intrinsic')
idx_B=np.union1d(idx_S,idx_A)
print('S=%d A=%d mu=%d B=%d' % (len(idx_S),len(idx_A),len(idx_mu),len(idx_B)), flush=True)
sub={}
m_int=ann['flow']=='intrinsic'
for sc in sorted(set(ann.loc[m_int,'super_class'].dropna().astype(str))):
    arr=byidx(m_int & (ann['super_class'].astype(str)==sc))
    if len(arr)>=100: sub['mu_'+sc]=arr
print('submodulos: '+', '.join('%s=%d' % (k,len(v)) for k,v in sub.items()), flush=True)
def sens(classes):
    m=ann['cell_class'].isin(classes) & (ann['flow']=='afferent')
    r=byidx(m)
    if len(r)==0: r=byidx(ann['cell_class'].isin(classes))
    return r
stim={}
for nm,cl in [('visual',['visual']),('olfactory',['olfactory','ORN']),('mechanosensory',['mechanosensory']),('gustatory',['gustatory'])]:
    a=sens(cl)
    if len(a)>0: stim[nm]=a
print('stim: '+', '.join('%s=%d' % (k,len(v)) for k,v in stim.items()), flush=True)
idx_motor=byidx(ann['super_class'].isin(['descending','motor']) | (ann['flow']=='efferent'))
idx_per=byidx(ann['cell_class']=='brain_motor_neuron')
print('motor=%d per=%d' % (len(idx_motor),len(idx_per)), flush=True)
primary={}
for nm,mi in stim.items():
    best=None; bv=-1
    for sn,si in sub.items():
        c=W_raw[mi][:,si].nnz
        if c>bv: bv=c; best=sn
    primary[nm]=best
    print('primary %s -> %s (%d aristas)' % (nm,best,bv), flush=True)
def norm_col(W,s):
    Wc=W.tocsc().astype(np.float32).copy()
    cs=np.asarray(abs(Wc).sum(axis=0)).ravel()
    cs[cs<1e-8]=1.0
    Wc=Wc.dot(sp.diags(1.0/cs))
    return (Wc.tocsr()*s).astype(np.float32)
def norm_row(W,s):
    Wr=W.tocsr().astype(np.float32).copy()
    rs=np.asarray(abs(Wr).sum(axis=1)).ravel()
    rs[rs<1e-8]=1.0
    Wr=sp.diags(1.0/rs).dot(Wr)
    return (Wr.tocsr()*s).astype(np.float32)
def sr_est(W,mi=300):
    try:
        v=eigs(W.astype(np.float64),k=1,which='LM',return_eigenvectors=False,maxiter=mi,tol=1e-4)
        return float(np.abs(v).max())
    except Exception as e:
        return float('nan')
def propagate(Wn, stim_idx, save_at, tau=TAU, amp=1.0, use_tanh=True, clip=2.0, nsteps=N_STEPS):
    WT=Wn.T.tocsr()
    h=np.zeros(Wn.shape[0], dtype=np.float32)
    ss=set(save_at); res={}; diverged=False
    for t in range(nsteps):
        pre_act=WT.dot(h)
        if T_START<=t<=T_END: pre_act[stim_idx]+=amp
        upd=np.tanh(pre_act) if use_tanh else pre_act
        h=(1.0-tau)*h + tau*upd
        if clip is not None: np.clip(h,-clip,clip,out=h)
        mx=float(np.abs(h).max())
        if mx>1e6 or not np.isfinite(mx):
            diverged=True; res[t]=h.copy(); break
        if t in ss: res[t]=h.copy()
    return res, diverged
def ent_kde(h, idx):
    v=h[idx]
    if len(v)<20 or float(np.std(v))<1e-15: return float('nan')
    try:
        k=spstats.gaussian_kde(v, bw_method='silverman')
        xg=np.linspace(v.min()-0.1, v.max()+0.1, 500)
        p=k(xg); p=p[p>1e-20]; dx=float(xg[1]-xg[0])
        return float(-np.sum(p*np.log(p)*dx))
    except Exception:
        return float('nan')
def dev_eq(h, idx):
    return float(np.sum(h[idx].astype(np.float64)**2))/max(1,len(idx))
W_mu_S=W_raw[idx_mu][:,idx_S].tocsr()
def fe(h):
    sa=h[idx_S].astype(np.float64); ma=h[idx_mu].astype(np.float64)
    sp_=W_mu_S.T.dot(ma)
    pe=float(np.sum((sa-sp_)**2))/max(1,len(idx_S))
    cx=float(np.sum(ma**2))/max(1,len(idx_mu))
    return pe+cx
def fit_decay(ts, vs):
    ts=np.asarray(ts,dtype=np.float64); vs=np.asarray(vs,dtype=np.float64)
    ok=vs>1e-20
    if ok.sum()<3: return float('nan'), float('nan')
    x=ts[ok]-ts[ok][0]; y=np.log(vs[ok])
    sl,ic,r,pv,se=spstats.linregress(x,y)
    return float(-sl), float(r*r)
print('funciones listas t=%.0fs' % (time.time()-t0), flush=True)
OUT={'meta':{'N':int(N),'E':int(W_raw.nnz),'S':len(idx_S),'A':len(idx_A),'mu':len(idx_mu),'annot_rows':int(len(ann)),'motor':len(idx_motor),'per':len(idx_per),'primary':primary,'sub':{k:len(v) for k,v in sub.items()},'stim':{k:len(v) for k,v in stim.items()}},'test1':{},'test2':{},'test3':{}}
sr_raw=sr_est(W_raw)
print('SR matriz cruda = %.4f' % sr_raw, flush=True)
OUT['meta']['sr_raw']=sr_raw
mods=['visual','olfactory','mechanosensory']
configs=[('a_col099','col x0.99',lambda: norm_col(W_raw,0.99),True,2.0),('b_row099','row x0.99',lambda: norm_row(W_raw,0.99),True,2.0),('c_col101','col x1.01 supercritico',lambda: norm_col(W_raw,1.01),True,5.0),('d_global099','global SR=0.99',lambda: (W_raw.astype(np.float32)*np.float32(0.99/sr_raw)).tocsr(),True,2.0),('e_col099_lin','col x0.99 lineal sin tanh',lambda: norm_col(W_raw,0.99),False,2.0)]
for cid,label,fn,ut,cl in configs:
    tt=time.time(); Wn=fn(); srn=sr_est(Wn)
    entry={'label':label,'sr':srn,'use_tanh':ut,'clip':cl,'mods':{}}
    for m in mods:
        hist,dv=propagate(Wn, stim[m], T_FINE, use_tanh=ut, clip=cl)
        if dv:
            entry['mods'][m]={'diverged':True}; print('  %s %s DIVERGIO' % (cid,m), flush=True); continue
        tp=[t for t in T_FINE if t>T_END and t in hist]
        lamF,r2F=fit_decay(tp,[fe(hist[t]) for t in tp])
        prim=primary[m]; dd={}
        for sn,si in sub.items():
            lamD,r2D=fit_decay(tp,[dev_eq(hist[t],si) for t in tp])
            dd[sn]={'role':('P' if sn==prim else 'S'),'lambda_D':lamD,'r2':r2D}
        lp=[v['lambda_D'] for v in dd.values() if v['role']=='P' and np.isfinite(v['lambda_D'])]
        ls=[v['lambda_D'] for v in dd.values() if v['role']=='S' and np.isfinite(v['lambda_D'])]
        Rasym=float(np.mean(ls)/np.mean(lp)) if lp and ls and np.mean(lp)>1e-12 else float('nan')
        eh={}
        for sn,si in sub.items():
            e60=ent_kde(hist[60],si) if 60 in hist else float('nan')
            e195=ent_kde(hist[195],si) if 195 in hist else float('nan')
            eh[sn]={'H60':e60,'H195':e195,'dH':(e195-e60) if np.isfinite(e60) and np.isfinite(e195) else float('nan')}
        mx=float(np.abs(hist[60]).max()) if 60 in hist else float('nan')
        p09=float(np.mean(np.abs(hist[60][sub[prim]])>0.9)*100.0) if 60 in hist else float('nan')
        entry['mods'][m]={'diverged':False,'lambda_F':lamF,'r2_F':r2F,'R':Rasym,'dev':dd,'ent':eh,'max_abs_h60':mx,'pct_gt09_primary':p09}
        print('  %s %s lamF=%.6f R=%.4f max|h|=%.4f' % (cid,m,lamF,Rasym,mx), flush=True)
    OUT['test1'][cid]=entry
    print('%s listo en %.0fs' % (cid, time.time()-tt), flush=True)
    json.dump(OUT, open('R_out.json','w'), indent=1)
    del Wn
Wn_a=norm_col(W_raw,0.99)
for amp in [0.1,0.5,1.0,2.0,5.0]:
    e={'amp':amp,'mods':{}}
    for m in mods:
        hist,dv=propagate(Wn_a, stim[m], T_FINE, amp=amp)
        if dv: e['mods'][m]={'diverged':True}; continue
        tp=[t for t in T_FINE if t>T_END and t in hist]
        lamF,r2F=fit_decay(tp,[fe(hist[t]) for t in tp])
        prim=primary[m]; lp=[]; ls=[]
        for sn,si in sub.items():
            lamD,_=fit_decay(tp,[dev_eq(hist[t],si) for t in tp])
            if np.isfinite(lamD):
                (lp if sn==prim else ls).append(lamD)
        Rasym=float(np.mean(ls)/np.mean(lp)) if lp and ls else float('nan')
        mx=float(np.abs(hist[60]).max())
        e['mods'][m]={'diverged':False,'lambda_F':lamF,'R':Rasym,'max_abs_h60':mx}
        print('  amp=%s %s lamF=%.6f R=%.4f max|h|=%.4f' % (amp,m,lamF,Rasym,mx), flush=True)
    OUT['test2'][str(amp)]=e
    json.dump(OUT, open('R_out.json','w'), indent=1)
print('TEST2 listo t=%.0fs' % (time.time()-t0), flush=True)
t3={'motor_act':{},'per_act':{},'latency_peak':{},'latency_10pct':{},'onehop':{}}
KEY=[5,30,60,80,100,140,180,195]
for m in ['gustatory','visual','olfactory','mechanosensory']:
    if m not in stim: continue
    hist,_=propagate(Wn_a, stim[m], sorted(set(KEY+list(range(T_START,T_START+60)))))
    t3['motor_act'][m]={str(t):float(np.abs(hist[t][idx_motor]).sum()) for t in KEY if t in hist}
    t3['per_act'][m]={str(t):float(np.abs(hist[t][idx_per]).sum()) for t in KEY if t in hist}
    tr=sorted(t for t in hist if T_START<=t<T_START+60)
    series=[(t,float(np.abs(hist[t][idx_motor]).sum())) for t in tr]
    pk=max(series,key=lambda z:z[1])
    t3['latency_peak'][m]={'t':pk[0],'lat_ms':pk[0]-T_START,'val':pk[1]}
    thr=0.10*pk[1]
    hit=[t for t,v in series if v>=thr]
    t3['latency_10pct'][m]={'t':(hit[0] if hit else None),'lat_ms':((hit[0]-T_START) if hit else None),'thr':thr}
    print('  T3 %s pico t=%d (%.2f) | 10pct t=%s' % (m,pk[0],pk[1],str(hit[0] if hit else None)), flush=True)
for m,mi in stim.items():
    blk=W_raw[mi][:,idx_motor]
    d=blk.data
    t3['onehop'][m]={'edges':int(blk.nnz),'exc':float(d[d>0].sum()) if d.size else 0.0,'inh':float(d[d<0].sum()) if d.size else 0.0}
    print('  1hop %s aristas=%d exc=%.0f inh=%.0f' % (m,blk.nnz,t3['onehop'][m]['exc'],t3['onehop'][m]['inh']), flush=True)
t3['tau']={'tau':TAU,'inv_tau':1.0/TAU,'minus_1_over_ln1mtau':float(-1.0/np.log(1.0-TAU))}
OUT['test3']=t3
json.dump(OUT, open('R_out.json','w'), indent=1)
print('SCRIPT R COMPLETO en %.1f min' % ((time.time()-t0)/60.0), flush=True)
