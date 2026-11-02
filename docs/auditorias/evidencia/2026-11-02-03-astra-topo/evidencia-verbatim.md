# Evidencia de auditoría Astra: Topo inverso, 008 y 009

Fecha: 2026-11-02. Base auditada: c3b718dbdb69c9d0ad25e5a729f1d06cf2ed297a.

Esto es evidencia, no el dictamen. Los programas independientes siguientes se ejecutaron en brain-env sobre datos existentes. No se ejecutó una nueva simulación del cerebro entero. Las poblaciones de cierre X y los mapas de unidades son entradas heredadas, fijadas por hash; no se reconstruyeron desde las anotaciones en esta auditoría. El instrumento de cierre reagrega los nulos archivados, no vuelve a generarlos.

## Ejecuciones

Invocaciones reproducibles:

- python3 /workspace/astra_topo_audit_20261102/audit_core.py
- python3 /workspace/astra_topo_audit_20261102/audit_banc.py
- python3 /workspace/astra_topo_audit_20261102/audit_closure.py

Las tres terminaron con exit 0 y stderr vacío. Python 3.12.14, NumPy 2.5.3, host 6c09d8604b07. No se instaló software ni se usaron Actions o Kaggle.

Fuentes ejecutadas SHA-256:

- audit_core.py: 50928c8ce0c141146b807cae16f7bdd95527bcfaf16f0f13055b120573ab26ff
- audit_banc.py: d1d9d811d1555315b541abebd017f7f59d7c9cd32c556f63571bf5172b1fa9b1
- audit_closure.py: b947699253520ecb352042ca94d15cb194600e48d3b465eaf5ebace9a33c28df

La copia original de stdout de core tiene 14.310 bytes y SHA-256 03c04e0c3d196e109ab16dea76d408c1c90d2f6dbbf1e7e02b6e3fa206ef716c. La de banc tiene 5.401 bytes y SHA-256 ae62ebd50005982ede3bf330c02d9864772d116ede2f8f08221a903b7a22d4b3. A continuación se conservan completas entre sus cercas de texto.

## audit_core.py

```python
import sys,json,hashlib,time,platform,itertools
from pathlib import Path
import numpy as np,pandas as pd,pyarrow.parquet as pq
R=Path('/workspace');M=R/'mecanismo-2026-11-02';V=R/'dnp04/verif';O=R/'astra_topo_audit_20261102'
O.mkdir(exist_ok=True)
out={'environment':{'python':sys.version,'host':platform.node(),'numpy':np.__version__},'inputs':{}}
def fingerprint(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 out['inputs'][str(p)]={'bytes':Path(p).stat().st_size,'sha256':h.hexdigest()}
def read(p):
 fingerprint(p);return json.loads(Path(p).read_text())
def save(k,v):
 out[k]=v;(O/'core.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False));print(k,json.dumps(v,ensure_ascii=False,allow_nan=False),flush=True)
def rates(c,q,idx):
 pos={int(x):i for i,x in enumerate(c['indices']['mirar'])}
 return np.array([[e['cuentas'][pos[int(x)]] for x in idx] for e in c['conds'][q]['ensayos']],float)/(c['t_run_ms']/1000)
def metric(y,p):
 return {'R2':float(1-np.sum((y-p)**2)/np.sum((y-y.mean())**2)),'MAE':float(abs(y-p).mean()),'MaxErr':float(abs(y-p).max()),'hits015':int(np.sum(abs(y-p)<=.15))}
t0=time.monotonic();seal=read(V/'sello_diseno_16_relevos.json');old=read(V/'auditoria_e_innovacion_2026_11_02.json');u=np.load(M/'flywire_units.npz',allow_pickle=False);typ=u['tipo'].astype(str)
for p in [R/'connectivity.parquet',M/'flywire_units.npz',M/'flywire_closing_paths.parquet',M/'banc_closing_paths.parquet']:fingerprint(p)
C={};needed={6128,95123,37128,105779};posts=set()
for r in seal:needed.update([r['d_idx'],r['x_idx']]);posts.add(r['x_idx'])
hubs=[(33912,[41594,104203,19410],[3,278],[1226,6324]),(58129,[58878,71368],[2,180],[1073,5262]),(19257,[111205,130297],[2,282],[402,2348]),(122969,[27878,20277],[2,243],[297,2681]),(45293,[129110,53975],[2,198],[685,7748]),(112031,[84751,69226],[2,165],[575,5662])]
for x,ds,a,b in hubs:needed.update(ds);posts.add(x)
for s in ['LC4','LPLC2','LPLC1','LPLC4']:
 cp=read(M/f'actions_correr2/celda_p_{s}_right_a.json');ca=read(R/f'dnp04/actions_correr/celda_q_{s}_right_a.json');cb=read(R/f'dnp04/actions_correr/celda_q_{s}_right_b.json');C[s]=(cp,ca,cb);needed.update(cp['indices']['X'])
 assert ca['indices']['D']==cb['indices']['D']==cp['indices']['D']
 assert np.array_equal(rates(ca,'C0',ca['indices']['mirar']),rates(cb,'C0',ca['indices']['mirar']))
closing=np.zeros(len(typ),bool);closing[pq.read_table(M/'flywire_closing_paths.parquet',columns=['x'])['x'].to_numpy()]=True
chunks=[];pairs=[];nr=0
for batch in pq.ParquetFile(R/'connectivity.parquet').iter_batches(batch_size=500000,columns=['Presynaptic_Index','Postsynaptic_Index','Connectivity','Excitatory x Connectivity']):
 pre,post,w,sg=[batch.column(i).to_numpy() for i in range(4)];nr+=len(pre);k=np.isin(pre,list(needed))|np.isin(post,list(posts));chunks.append(pd.DataFrame({'pre':pre[k],'post':post[k],'w':w[k],'signed':sg[k]}));k=(u['D'][pre]>=0)&closing[post]&~u['inh'][pre];pairs.append(pd.DataFrame({'D_type':typ[pre[k]],'X_type':typ[post[k]],'w':w[k]}))
ed=pd.concat(chunks,ignore_index=True);fw=pd.concat(pairs,ignore_index=True);fw=fw[~fw.D_type.isin(['None','nan'])&~fw.X_type.isin(['None','nan'])].groupby(['D_type','X_type'],as_index=False).agg(w_max=('w','max'),w_sum=('w','sum'),n_edges=('w','size'));fw.to_csv(O/'fw_typed.csv',index=False);save('scan',{'rows':nr,'typed_fw':len(fw),'retained':len(ed)})
pre,post,sg=[ed[x].to_numpy() for x in ['pre','post','signed']]
def guard(k):return [int(np.sum(k&(sg!=0))),float(abs(sg[k]).sum())]
g=[];col=[]
for r in seal:
 d,x=r['d_idx'],r['x_idx'];m={'Q1':(pre==d)&(post==x),'Q2':pre==x,'Q3':pre==d,'Q4':(post==x)&(pre!=d)}
 for q,k in m.items():
  want=r['guardas_filas'][q];want=[want['filas'],want['peso_abs']];got=guard(k);g.append({'r':r['code'],'q':q,'expected':want,'got':got,'pass':got==want})
 dp=set(post[(pre==x)&(u['D'][post]>=0)&(post!=d)&(sg<0)]);strict=float(sg[(pre==d)&np.isin(post,list(dp))&(sg>0)].sum());all_d=float(sg[(pre==d)&(u['D'][post]>=0)&(post!=d)&(sg>0)].sum());col.append({'r':r['code'],'n_Dprime':len(dp),'strict_D_to_Dprime':strict,'all_other_D':all_d,'published':r['Dp_targets']['collateral_w_D_to_Dp']})
joints=[]
for x,ds,e1,e4 in hubs:
 q1=guard(np.isin(pre,ds)&(post==x));q4=guard(~np.isin(pre,ds)&(post==x));joints.append({'hub':x,'drivers':ds,'q1':q1,'q4':q4,'pass':q1==e1 and q4==e4})
save('guards',{'individual':g,'joint':joints,'n_pass':sum(z['pass'] for z in g),'joint_pass':sum(z['pass'] for z in joints),'cascade_union':guard((pre==6128)|((pre==59804)&(post==30887)))});save('collateral',col)
order=[('PVLP010',37128,'LC4','Q2',.729),('PVLP010',37128,'LPLC2','Q2',.194),('PVLP010',37128,'LPLC1','Q2',.217),('LHAD1g1',105779,'LC4','Q5',.022),('LHAD1g1',105779,'LPLC2','Q5',.308),('AVLP080',6128,'LPLC2','Q6',.201),('AVLP080',6128,'LPLC1','Q6',.624)]
blocks={};rows=[];dnp={}
for s,(cp,ca,cb) in C.items():
 X=cp['indices']['X'];D=[d for d in cp['indices']['D'] if d!=95123];W=ed[ed.pre.isin(X)&ed.post.isin(D)].pivot_table(index='pre',columns='post',values='w',aggfunc='sum',fill_value=0).reindex(index=X,columns=D,fill_value=0).to_numpy(float);rx=rates(ca,'C0',X).mean(axis=0);rd=rates(ca,'C0',D).mean(axis=0);A=rx[:,None]*W;den=A.sum(axis=0);share=np.divide(A,den,out=np.zeros_like(A),where=den>0);p=share@(rd/rd.sum());B=rx*(W@(rd/(rd+10)));delta=(rates(ca,'C1',D)-rates(ca,'C0',D)).sum(axis=1).mean();blocks[s]={'D':D,'X':X,'rd':rd,'share':share}
 if s=='LC4':
  dnp={'delta_global':float(delta),'delta_Q1':float((rates(ca,'Q1',D)-rates(ca,'C0',D)).sum(axis=1).mean()),'delta_Q2':float((rates(ca,'Q2',D)-rates(ca,'C0',D)).sum(axis=1).mean()),'s4':float(rates(cb,'Q4',[37128]).mean()/rates(cb,'C0',[37128]).mean())}
 for name,xi,ss,q,lin in order:
  if ss!=s:continue
  cc=ca if q in ca['conds'] else cb;df=(rates(cc,q,D)-rates(cc,'C0',D)).sum(axis=1);i=X.index(xi);rows.append({'pair':name+'_'+s,'stim':s,'xi':xi,'y':float(df.mean()/delta),'linear':lin,'p008':float(p[i]),'B009_raw':float(B[i]),'B009_norm_exploratory':float(B[i]/B.sum())})
names=[a+'_'+s for a,b,s,c,d in order];rows.sort(key=lambda z:names.index(z['pair']));y=np.array([r['y'] for r in rows]);p=np.array([r['p008'] for r in rows]);obs=abs(y-p).mean();rng=np.random.default_rng(20261102);null=[]
for _ in range(10000):
 sh={s:rng.permutation(b['rd']) for s,b in blocks.items() if s!='LPLC4'};v=[]
 for r in rows:
  b=blocks[r['stim']];v.append(float(b['share'][b['X'].index(r['xi'])]@sh[r['stim']]/b['rd'].sum()))
 null.append(float(np.mean(abs(y-v))))
better=int(np.sum(np.array(null)<=obs+1e-15));ex=np.array([abs(y-np.array(v)).mean() for v in itertools.permutations(p)])
save('dnp04',dnp);save('proxy',{'rows':rows,'metrics008':metric(y,p),'metrics006':metric(y,np.array([r['linear'] for r in rows])),'metrics009_raw':metric(y,np.array([r['B009_raw'] for r in rows])),'metrics009_norm_exploratory':metric(y,np.array([r['B009_norm_exploratory'] for r in rows])),'target_perm_shared_per_stimulus':{'n':10000,'better':better,'p_plus_one':(better+1)/10001,'mean_MAE':float(np.mean(null))},'global_exact':{'n':len(ex),'better':int(np.sum(ex<=obs+1e-15)),'p':float(np.mean(ex<=obs+1e-15))},'published_controls':old['proxy_freno_efectivo']['negative_controls']})
save('blocks',{s:{'D':b['D'],'X':b['X'],'rd':b['rd'].tolist(),'share_rows':{str(r['xi']):b['share'][b['X'].index(r['xi'])].tolist() for r in rows if r['stim']==s}} for s,b in blocks.items() if s!='LPLC4'})
save('seconds',time.monotonic()-t0)
```

## core.stdout

```text
scan {"rows": 15091983, "typed_fw": 7052, "retained": 98236}
guards {"individual": [{"r": "R01_DNp35_CB0527", "q": "Q1", "expected": [1, 235.0], "got": [1, 235.0], "pass": true}, {"r": "R01_DNp35_CB0527", "q": "Q2", "expected": [551, 4841.0], "got": [551, 4841.0], "pass": true}, {"r": "R01_DNp35_CB0527", "q": "Q3", "expected": [465, 2618.0], "got": [465, 2618.0], "pass": true}, {"r": "R01_DNp35_CB0527", "q": "Q4", "expected": [650, 5164.0], "got": [650, 5164.0], "pass": true}, {"r": "R02_DNpe016_cL22c", "q": "Q1", "expected": [1, 180.0], "got": [1, 180.0], "pass": true}, {"r": "R02_DNpe016_cL22c", "q": "Q2", "expected": [601, 6492.0], "got": [601, 6492.0], "pass": true}, {"r": "R02_DNpe016_cL22c", "q": "Q3", "expected": [186, 1011.0], "got": [186, 1011.0], "pass": true}, {"r": "R02_DNpe016_cL22c", "q": "Q4", "expected": [672, 4497.0], "got": [672, 4497.0], "pass": true}, {"r": "R03_DNa03_PLP060", "q": "Q1", "expected": [1, 165.0], "got": [1, 165.0], "pass": true}, {"r": "R03_DNa03_PLP060", "q": "Q2", "expected": [701, 6472.0], "got": [701, 6472.0], "pass": true}, {"r": "R03_DNa03_PLP060", "q": "Q3", "expected": [385, 4773.0], "got": [385, 4773.0], "pass": true}, {"r": "R03_DNa03_PLP060", "q": "Q4", "expected": [440, 4195.0], "got": [440, 4195.0], "pass": true}, {"r": "R04_DNpe023_CB0172", "q": "Q1", "expected": [1, 155.0], "got": [1, 155.0], "pass": true}, {"r": "R04_DNpe023_CB0172", "q": "Q2", "expected": [267, 2259.0], "got": [267, 2259.0], "pass": true}, {"r": "R04_DNpe023_CB0172", "q": "Q3", "expected": [415, 3270.0], "got": [415, 3270.0], "pass": true}, {"r": "R04_DNpe023_CB0172", "q": "Q4", "expected": [298, 2769.0], "got": [298, 2769.0], "pass": true}, {"r": "R05_DNp71_CB0534", "q": "Q1", "expected": [1, 154.0], "got": [1, 154.0], "pass": true}, {"r": "R05_DNp71_CB0534", "q": "Q2", "expected": [550, 4917.0], "got": [550, 4917.0], "pass": true}, {"r": "R05_DNp71_CB0534", "q": "Q3", "expected": [236, 2128.0], "got": [236, 2128.0], "pass": true}, {"r": "R05_DNp71_CB0534", "q": "Q4", "expected": [403, 2476.0], "got": [403, 2476.0], "pass": true}, {"r": "R06_DNp104_CB0626", "q": "Q1", "expected": [1, 153.0], "got": [1, 153.0], "pass": true}, {"r": "R06_DNp104_CB0626", "q": "Q2", "expected": [1184, 7413.0], "got": [1184, 7413.0], "pass": true}, {"r": "R06_DNp104_CB0626", "q": "Q3", "expected": [364, 1692.0], "got": [364, 1692.0], "pass": true}, {"r": "R06_DNp104_CB0626", "q": "Q4", "expected": [1196, 6951.0], "got": [1196, 6951.0], "pass": true}, {"r": "R07_DNg100_CB0534", "q": "Q1", "expected": [1, 128.0], "got": [1, 128.0], "pass": true}, {"r": "R07_DNg100_CB0534", "q": "Q2", "expected": [550, 4917.0], "got": [550, 4917.0], "pass": true}, {"r": "R07_DNg100_CB0534", "q": "Q3", "expected": [472, 2753.0], "got": [472, 2753.0], "pass": true}, {"r": "R07_DNg100_CB0534", "q": "Q4", "expected": [403, 2502.0], "got": [403, 2502.0], "pass": true}, {"r": "R08_DNa03_VES041", "q": "Q1", "expected": [1, 126.0], "got": [1, 126.0], "pass": true}, {"r": "R08_DNa03_VES041", "q": "Q2", "expected": [1001, 8265.0], "got": [1001, 8265.0], "pass": true}, {"r": "R08_DNa03_VES041", "q": "Q3", "expected": [385, 4773.0], "got": [385, 4773.0], "pass": true}, {"r": "R08_DNa03_VES041", "q": "Q4", "expected": [1487, 11273.0], "got": [1487, 11273.0], "pass": true}, {"r": "R09_DNpe023_cL22b", "q": "Q1", "expected": [1, 120.0], "got": [1, 120.0], "pass": true}, {"r": "R09_DNpe023_cL22b", "q": "Q2", "expected": [1066, 9308.0], "got": [1066, 9308.0], "pass": true}, {"r": "R09_DNpe023_cL22b", "q": "Q3", "expected": [415, 3270.0], "got": [415, 3270.0], "pass": true}, {"r": "R09_DNpe023_cL22b", "q": "Q4", "expected": [918, 6813.0], "got": [918, 6813.0], "pass": true}, {"r": "R10_DNp47_CB0580", "q": "Q1", "expected": [1, 115.0], "got": [1, 115.0], "pass": true}, {"r": "R10_DNp47_CB0580", "q": "Q2", "expected": [1616, 10297.0], "got": [1616, 10297.0], "pass": true}, {"r": "R10_DNp47_CB0580", "q": "Q3", "expected": [423, 2136.0], "got": [423, 2136.0], "pass": true}, {"r": "R10_DNp47_CB0580", "q": "Q4", "expected": [1228, 6487.0], "got": [1228, 6487.0], "pass": true}, {"r": "R11_DNa06_PS100", "q": "Q1", "expected": [1, 111.0], "got": [1, 111.0], "pass": true}, {"r": "R11_DNa06_PS100", "q": "Q2", "expected": [507, 3690.0], "got": [507, 3690.0], "pass": true}, {"r": "R11_DNa06_PS100", "q": "Q3", "expected": [328, 3436.0], "got": [328, 3436.0], "pass": true}, {"r": "R11_DNa06_PS100", "q": "Q4", "expected": [686, 7835.0], "got": [686, 7835.0], "pass": true}, {"r": "R12_DNae007_PS065", "q": "Q1", "expected": [1, 96.0], "got": [1, 96.0], "pass": true}, {"r": "R12_DNae007_PS065", "q": "Q2", "expected": [438, 3479.0], "got": [438, 3479.0], "pass": true}, {"r": "R12_DNae007_PS065", "q": "Q3", "expected": [313, 2380.0], "got": [313, 2380.0], "pass": true}, {"r": "R12_DNae007_PS065", "q": "Q4", "expected": [505, 5383.0], "got": [505, 5383.0], "pass": true}, {"r": "R13_DNp104_CB0580", "q": "Q1", "expected": [1, 93.0], "got": [1, 93.0], "pass": true}, {"r": "R13_DNp104_CB0580", "q": "Q2", "expected": [1140, 5354.0], "got": [1140, 5354.0], "pass": true}, {"r": "R13_DNp104_CB0580", "q": "Q3", "expected": [364, 1692.0], "got": [364, 1692.0], "pass": true}, {"r": "R13_DNp104_CB0580", "q": "Q4", "expected": [1074, 5349.0], "got": [1074, 5349.0], "pass": true}, {"r": "R14_DNp101_CB0580", "q": "Q1", "expected": [1, 91.0], "got": [1, 91.0], "pass": true}, {"r": "R14_DNp101_CB0580", "q": "Q2", "expected": [1616, 10297.0], "got": [1616, 10297.0], "pass": true}, {"r": "R14_DNp101_CB0580", "q": "Q3", "expected": [257, 2489.0], "got": [257, 2489.0], "pass": true}, {"r": "R14_DNp101_CB0580", "q": "Q4", "expected": [1228, 6511.0], "got": [1228, 6511.0], "pass": true}, {"r": "R15_DNge148_PS100", "q": "Q1", "expected": [1, 88.0], "got": [1, 88.0], "pass": true}, {"r": "R15_DNge148_PS100", "q": "Q2", "expected": [439, 2780.0], "got": [439, 2780.0], "pass": true}, {"r": "R15_DNge148_PS100", "q": "Q3", "expected": [324, 1464.0], "got": [324, 1464.0], "pass": true}, {"r": "R15_DNge148_PS100", "q": "Q4", "expected": [576, 5739.0], "got": [576, 5739.0], "pass": true}, {"r": "R16_DNae005_CB0172", "q": "Q1", "expected": [1, 88.0], "got": [1, 88.0], "pass": true}, {"r": "R16_DNae005_CB0172", "q": "Q2", "expected": [267, 2259.0], "got": [267, 2259.0], "pass": true}, {"r": "R16_DNae005_CB0172", "q": "Q3", "expected": [242, 1722.0], "got": [242, 1722.0], "pass": true}, {"r": "R16_DNae005_CB0172", "q": "Q4", "expected": [298, 2836.0], "got": [298, 2836.0], "pass": true}], "joint": [{"hub": 33912, "drivers": [41594, 104203, 19410], "q1": [3, 278.0], "q4": [1226, 6324.0], "pass": true}, {"hub": 58129, "drivers": [58878, 71368], "q1": [2, 180.0], "q4": [1073, 5262.0], "pass": true}, {"hub": 19257, "drivers": [111205, 130297], "q1": [2, 282.0], "q4": [402, 2348.0], "pass": true}, {"hub": 122969, "drivers": [27878, 20277], "q1": [2, 243.0], "q4": [297, 2681.0], "pass": true}, {"hub": 45293, "drivers": [129110, 53975], "q1": [2, 198.0], "q4": [685, 7748.0], "pass": true}, {"hub": 112031, "drivers": [84751, 69226], "q1": [2, 165.0], "q4": [575, 5662.0], "pass": true}], "n_pass": 64, "joint_pass": 6, "cascade_union": [1678, 18858.0]}
collateral [{"r": "R01_DNp35_CB0527", "n_Dprime": 137, "strict_D_to_Dprime": 935.0, "all_other_D": 1192.0, "published": 1192}, {"r": "R02_DNpe016_cL22c", "n_Dprime": 25, "strict_D_to_Dprime": 135.0, "all_other_D": 405.0, "published": 405}, {"r": "R03_DNa03_PLP060", "n_Dprime": 40, "strict_D_to_Dprime": 452.0, "all_other_D": 1944.0, "published": 1944}, {"r": "R04_DNpe023_CB0172", "n_Dprime": 75, "strict_D_to_Dprime": 566.0, "all_other_D": 772.0, "published": 772}, {"r": "R05_DNp71_CB0534", "n_Dprime": 63, "strict_D_to_Dprime": 237.0, "all_other_D": 913.0, "published": 913}, {"r": "R06_DNp104_CB0626", "n_Dprime": 113, "strict_D_to_Dprime": 69.0, "all_other_D": 218.0, "published": 218}, {"r": "R07_DNg100_CB0534", "n_Dprime": 64, "strict_D_to_Dprime": 84.0, "all_other_D": 725.0, "published": 725}, {"r": "R08_DNa03_VES041", "n_Dprime": 70, "strict_D_to_Dprime": 1527.0, "all_other_D": 1944.0, "published": 1944}, {"r": "R09_DNpe023_cL22b", "n_Dprime": 56, "strict_D_to_Dprime": 307.0, "all_other_D": 772.0, "published": 772}, {"r": "R10_DNp47_CB0580", "n_Dprime": 138, "strict_D_to_Dprime": 27.0, "all_other_D": 575.0, "published": 575}, {"r": "R11_DNa06_PS100", "n_Dprime": 192, "strict_D_to_Dprime": 670.0, "all_other_D": 937.0, "published": 937}, {"r": "R12_DNae007_PS065", "n_Dprime": 62, "strict_D_to_Dprime": 750.0, "all_other_D": 1222.0, "published": 1222}, {"r": "R13_DNp104_CB0580", "n_Dprime": 113, "strict_D_to_Dprime": 10.0, "all_other_D": 218.0, "published": 218}, {"r": "R14_DNp101_CB0580", "n_Dprime": 139, "strict_D_to_Dprime": 70.0, "all_other_D": 1135.0, "published": 1135}, {"r": "R15_DNge148_PS100", "n_Dprime": 173, "strict_D_to_Dprime": 118.0, "all_other_D": 237.0, "published": 237}, {"r": "R16_DNae005_CB0172", "n_Dprime": 75, "strict_D_to_Dprime": 734.0, "all_other_D": 1025.0, "published": 1025}]
dnp04 {"delta_global": 252.6, "delta_Q1": 102.45, "delta_Q2": 188.35, "s4": 0.9676663542642924}
proxy {"rows": [{"pair": "PVLP010_LC4", "stim": "LC4", "xi": 37128, "y": 0.7456452889944576, "linear": 0.729, "p008": 0.6082979407880513, "B009_raw": 30310.539302617824, "B009_norm_exploratory": 0.640991313317786}, {"pair": "PVLP010_LPLC2", "stim": "LPLC2", "xi": 37128, "y": 0.24875621890547264, "linear": 0.194, "p008": 0.1974246189501154, "B009_raw": 26488.103991649776, "B009_norm_exploratory": 0.20565824534085825}, {"pair": "PVLP010_LPLC1", "stim": "LPLC1", "xi": 37128, "y": 0.48390446521287644, "linear": 0.217, "p008": 0.4519258014873384, "B009_raw": 14784.216435348197, "B009_norm_exploratory": 0.3556062829060302}, {"pair": "LHAD1g1_LC4", "stim": "LC4", "xi": 105779, "y": 0.011282660332541569, "linear": 0.022, "p008": 0.011896415819459074, "B009_raw": 813.8096821175965, "B009_norm_exploratory": 0.01721001832805513}, {"pair": "LHAD1g1_LPLC2", "stim": "LPLC2", "xi": 105779, "y": 0.20782451379466305, "linear": 0.308, "p008": 0.303481774143236, "B009_raw": 47197.91467710482, "B009_norm_exploratory": 0.366452816679551}, {"pair": "AVLP080_LPLC2", "stim": "LPLC2", "xi": 6128, "y": 0.02608171264887683, "linear": 0.201, "p008": 0.083092510775639, "B009_raw": 18048.30210614574, "B009_norm_exploratory": 0.1401301559259118}, {"pair": "AVLP080_LPLC1", "stim": "LPLC1", "xi": 6128, "y": 0.3296988577362409, "linear": 0.624, "p008": 0.27774241709050995, "B009_raw": 20306.194995865437, "B009_norm_exploratory": 0.4884270028122509}], "metrics008": {"R2": 0.9065287490601567, "MAE": 0.0608422666421836, "MaxErr": 0.13734734820640626, "hits015": 7}, "metrics006": {"R2": 0.4984535123483741, "MAE": 0.1312026040857835, "MaxErr": 0.2943011422637591, "hits015": 4}, "metrics009_raw": {"R2": -11938368982.208784, "MAE": 22563.861142447393, "MaxErr": 47197.70685259102, "hits015": 0}, "metrics009_norm_exploratory": {"R2": 0.7697642901298669, "MAE": 0.10191176868308267, "MaxErr": 0.15872814507600996, "hits015": 5}, "target_perm_shared_per_stimulus": {"n": 10000, "better": 1396, "p_plus_one": 0.1396860313968603, "mean_MAE": 0.09799221385349395}, "global_exact": {"n": 5040, "better": 7, "p": 0.001388888888888889}, "published_controls": {"within_stimulus_target_perm_10000": {"obs_MAE": 0.0608, "null_MAE_mean": 0.098, "null_hits_mean": 5.39, "p_MAE": 0.1043, "p_hits7": 0.104}, "cross_pair_perm_10000": {"obs_MAE": 0.0608, "null_MAE_mean": 0.2461, "null_hits_mean": 2.56, "p_MAE": 0.0015, "p_hits7": 0.0024}}}
blocks {"LC4": {"D": [9313, 11861, 43619, 58111, 59804, 74399, 92174, 95216, 108748], "X": [472, 577, 6009, 19126, 24150, 24642, 25604, 27978, 29262, 30887, 31081, 37128, 37987, 40093, 40752, 42923, 47029, 55703, 70370, 73156, 73727, 74426, 81297, 82815, 84505, 92373, 94792, 94849, 100238, 102923, 103670, 105779, 106025, 106901, 108148, 111561, 115073, 116142, 119162, 119290, 123699, 124304, 125165, 125852, 135309, 136123, 136163, 136180, 138286], "rd": [13.55, 0.0, 70.45, 9.0, 15.95, 45.25, 0.0, 58.2, 53.75], "share_rows": {"37128": [0.5956318470448678, 0.9213980131970126, 0.8317999106744083, 0.8975764817110164, 0.6920315540204226, 0.0, 0.05077567336061673, 0.6545951422648979, 0.7072344707800532], "105779": [0.09048566045635335, 0.025644194830620762, 0.005700596857363271, 0.026565274195169332, 0.020882667913543186, 0.0, 0.0009279527933758446, 0.00580028071871427, 0.011698622581534753]}}, "LPLC2": {"D": [9313, 11861, 14249, 30134, 34615, 37567, 49035, 58111, 59804, 83620, 108641, 108748, 111205], "X": [472, 577, 2860, 6009, 6128, 23023, 24150, 28368, 31081, 37128, 42923, 50971, 65508, 65830, 70370, 77196, 94849, 97308, 98673, 100238, 103670, 105214, 105779, 108148, 112171, 125852, 138286], "rd": [109.15, 1.55, 53.0, 15.45, 84.05, 70.1, 15.15, 52.1, 0.9, 0.0, 0.65, 102.5, 0.95], "share_rows": {"37128": [0.05213467438956074, 0.3009082971330853, 0.04122343884106218, 0.2998025748028703, 0.22034133926470903, 0.13741027152616428, 0.19945637127828253, 0.2643815253989599, 0.05781580041227318, 0.015849128297943615, 0.12203134062527267, 0.4041425800952172, 0.3475330020014842], "105779": [0.43336948086322363, 0.45825347540496586, 0.28856407188743527, 0.018737660925179395, 0.16949333789593002, 0.21985643444186287, 0.0, 0.4281576915753068, 0.09546329835514873, 0.1030193339366335, 0.008135422708351511, 0.36579328417377327, 0.29406638630894816], "6128": [0.3012134263232823, 0.06820597729800625, 0.0, 0.11547600751870808, 0.018991808713133863, 0.06158754378055969, 0.022349180781717964, 0.007864798678572114, 0.5845524800013572, 0.19534925579093151, 0.03646311856159567, 0.0, 0.029954797940045418]}}, "LPLC1": {"D": [9313, 11861, 32330, 59804, 90734, 95216, 113373], "X": [577, 6128, 6181, 14979, 19126, 23287, 29262, 30179, 36085, 37128, 40577, 41973, 42923, 47029, 66171, 70370, 81297, 82815, 84505, 86446, 102923, 103670, 106025, 111561, 113304, 116067, 116953, 123195, 123699, 125852, 128756, 134355], "rd": [6.9, 43.8, 1.3, 1.75, 0.0, 14.8, 12.75], "share_rows": {"37128": [0.0722031752624254, 0.651771424294259, 0.6476386978450253, 0.045099480599519584, 0.0, 0.4577650654914622, 0.0], "6128": [0.7689757971601948, 0.2723280035399866, 0.15049002751031637, 0.840537740997739, 0.22042435308191147, 0.14325873730987837, 0.12233345563184653]}}}
seconds 4.51304755709134
```

## audit_banc.py

```python
import sys,json,hashlib,time,collections
from pathlib import Path
import numpy as np,pandas as pd,pyarrow as pa,pyarrow.compute as pc,pyarrow.feather as pf,pyarrow.ipc as ipc,pyarrow.parquet as pq
from scipy import stats
R=Path('/workspace');M=R/'mecanismo-2026-11-02';O=R/'astra_topo_audit_20261102';out={'inputs':{},'scope':'BANC 888 typed relays conditional on inherited closing-X membership; no new functional simulation'}
def hashfile(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 out['inputs'][str(p)]={'sha256':h.hexdigest(),'bytes':Path(p).stat().st_size}
def emit(k,v):
 out[k]=v;(O/'banc.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False));print(k,json.dumps(v,ensure_ascii=False),flush=True)
t0=time.monotonic()
for p in [R/'banc_888/banc_888_meta.feather',R/'banc_888/banc_888_edgelist_simple_v3.feather',O/'fw_typed.csv',M/'banc_closing_paths.parquet']:hashfile(p)
m=pf.read_feather(R/'banc_888/banc_888_meta.feather',columns=['root_888','side','super_class','cell_type','fafb_cell_type','neurotransmitter_predicted']).drop_duplicates('root_888').reset_index(drop=True)
v=m.root_888.notna().to_numpy();ids=np.full(len(m),-1,np.int64);ids[v]=m.root_888[v].astype('int64');order=np.flatnonzero(v)[np.argsort(ids[v])];sid=ids[order];t=m.fafb_cell_type.where(m.fafb_cell_type.notna(),m.cell_type);D=((m.super_class=='descending')&m.side.isin(['left','right'])&t.notna()).to_numpy();inh=m.neurotransmitter_predicted.isin(['gaba','glutamate']).to_numpy();t=t.fillna('None').astype(str).to_numpy();X=np.zeros(len(m),bool);X[pq.read_table(M/'banc_closing_paths.parquet',columns=['x'])['x'].to_numpy()]=True
reader=ipc.open_file(pa.memory_map(str(R/'banc_888/banc_888_edgelist_simple_v3.feather'),'r'));parts=[];unmatched=0;total=0
for k in range(reader.num_record_batches):
 b=reader.get_batch(k);a=[]
 for col in ['pre','post']:
  raw=pc.cast(b.column(b.schema.get_field_index(col)),pa.int64()).to_numpy();pos=np.searchsorted(sid,raw);safe=np.minimum(pos,len(sid)-1);ok=(pos<len(sid))&(sid[safe]==raw);unmatched+=int(np.sum(~ok));assert np.all(ok),'Unmapped BANC root';a.append(order[safe])
 pre,post=a;w=b.column(b.schema.get_field_index('count')).to_numpy();total+=len(w);keep=D[pre]&X[post]&~inh[pre];parts.append(pd.DataFrame({'D_type':t[pre[keep]],'X_type':t[post[keep]],'w':w[keep]}))
b=pd.concat(parts,ignore_index=True);b=b[~b.D_type.isin(['None','nan'])&~b.X_type.isin(['None','nan'])].groupby(['D_type','X_type'],as_index=False).agg(w_max=('w','max'),w_sum=('w','sum'),n_edges=('w','size'));b.to_csv(O/'banc_typed.csv',index=False);f=pd.read_csv(O/'fw_typed.csv');ds=set(f.D_type)&set(b.D_type);xs=set(f.X_type)&set(b.X_type);fh=f[f.D_type.isin(ds)&f.X_type.isin(xs)&(f.w_max>=80)];bh=b[b.D_type.isin(ds)&b.X_type.isin(xs)&(b.w_max>=80)];fs=set(zip(fh.D_type,fh.X_type));bs=set(zip(bh.D_type,bh.X_type));both=f.merge(b,on=['D_type','X_type'],suffixes=('_fw','_banc'));heavy=fh.merge(bh,on=['D_type','X_type'],suffixes=('_fw','_banc'));rho=stats.spearmanr(both.w_max_fw,both.w_max_banc);observed=len(fs&bs)
emit('census',{'input_version':888,'banc_rows':total,'unmatched_roots':unmatched,'n_fw':len(f),'n_banc':len(b),'n_shared':len(both),'heavy_fw':len(fs),'heavy_banc':len(bs),'observed':observed,'rho':float(rho.statistic),'p_spearman_descriptive':float(rho.pvalue),'table':heavy.sort_values('w_max_fw',ascending=False).to_dict('records'),'fw_heavy_pairs':sorted(fs),'banc_heavy_pairs':sorted(bs),'threshold_sensitivity_descriptive':{str(c):int(((both.w_max_fw>=c)&(both.w_max_banc>=c)).sum()) for c in [60,80,100,120,162]}})
d,x=bh.D_type.to_numpy(),bh.X_type.to_numpy();rng=np.random.default_rng(20261102);hits=[];sizes=[]
for k in range(10000):
 p=set(zip(d,rng.permutation(x)));hits.append(len(fs&p));sizes.append(len(p))
def report(h):
 c=int(np.sum(np.array(h)>=observed));return {'n':len(h),'mean':float(np.mean(h)),'max':max(h),'exceedances':c,'p_plus_one':(c+1)/(len(h)+1),'hist':{str(a):b for a,b in sorted(collections.Counter(h).items())}}
emit('original_stub_then_set_null',dict(report(hits),original_unique_edges=len(bs),min_unique_edges=min(sizes),max_unique_edges=max(sizes),mean_unique_edges=float(np.mean(sizes)),invalid_unique_degree_draws=int(np.sum(np.array(sizes)!=len(bs))),size_hist={str(a):b for a,b in sorted(collections.Counter(sizes).items())}))
# Rejection sampling, not an MCMC: conditional uniform simple bipartite graphs.
# Each simple graph with the fixed margins has the same stub-label multiplicity.
rng=np.random.default_rng(20261103);hd=collections.Counter(a for a,b in bs);hx=collections.Counter(b for a,b in bs);fixed=[];attempts=0;guard_pass=0
while len(fixed)<10000:
 attempts+=1
 if attempts>1000000:raise RuntimeError('Rejection sampler budget exhausted')
 p=set(zip(d,rng.permutation(x)))
 if len(p)!=len(bs):continue
 assert collections.Counter(a for a,b in p)==hd
 assert collections.Counter(b for a,b in p)==hx
 guard_pass+=1;fixed.append(len(fs&p))
emit('corrected_simple_degree_null',dict(report(fixed),attempts=attempts,rejected_duplicates=attempts-len(fixed),degree_guard_pass=guard_pass,seed=20261103,method='IID stub shuffle rejection conditional on no duplicate typed edge; exact simple in/out degrees'))
# Negative fixture detects that collapsing two identical typed edges loses degree.
fixture=[('d1','x1'),('d1','x2'),('d2','x1')];mutant=[('d1','x1'),('d1','x1'),('d2','x2')]
def margins(seq):return (collections.Counter(a for a,b in set(seq)),collections.Counter(b for a,b in set(seq)))
emit('negative_control',{'same_stub_degrees':collections.Counter(a for a,b in fixture)==collections.Counter(a for a,b in mutant) and collections.Counter(b for a,b in fixture)==collections.Counter(b for a,b in mutant),'collapsed_simple_degrees_detected_wrong':margins(fixture)!=margins(mutant)})
emit('seconds',time.monotonic()-t0)
```

## banc.stdout

```text
census {"input_version": 888, "banc_rows": 13620865, "unmatched_roots": 0, "n_fw": 7052, "n_banc": 5867, "n_shared": 2701, "heavy_fw": 37, "heavy_banc": 31, "observed": 17, "rho": 0.6120192195702387, "p_spearman_descriptive": 2.2118338804821474e-277, "table": [{"D_type": "DNp35", "X_type": "CB0527", "w_max_fw": 235, "w_sum_fw": 642, "n_edges_fw": 4, "w_max_banc": 184, "w_sum_banc": 434, "n_edges_banc": 4}, {"D_type": "DNp04", "X_type": "PVLP010", "w_max_fw": 190, "w_sum_fw": 375, "n_edges_fw": 2, "w_max_banc": 123, "w_sum_banc": 170, "n_edges_banc": 2}, {"D_type": "DNpe016", "X_type": "cL22c", "w_max_fw": 180, "w_sum_fw": 357, "n_edges_fw": 3, "w_max_banc": 138, "w_sum_banc": 255, "n_edges_banc": 3}, {"D_type": "DNa03", "X_type": "PLP060", "w_max_fw": 165, "w_sum_fw": 313, "n_edges_fw": 2, "w_max_banc": 105, "w_sum_banc": 207, "n_edges_banc": 2}, {"D_type": "DNpe023", "X_type": "CB0172", "w_max_fw": 155, "w_sum_fw": 247, "n_edges_fw": 4, "w_max_banc": 188, "w_sum_banc": 357, "n_edges_banc": 4}, {"D_type": "DNp71", "X_type": "CB0534", "w_max_fw": 154, "w_sum_fw": 266, "n_edges_fw": 2, "w_max_banc": 187, "w_sum_banc": 319, "n_edges_banc": 2}, {"D_type": "DNp104", "X_type": "CB0626", "w_max_fw": 153, "w_sum_fw": 173, "n_edges_fw": 2, "w_max_banc": 91, "w_sum_banc": 237, "n_edges_banc": 4}, {"D_type": "DNg100", "X_type": "CB0534", "w_max_fw": 128, "w_sum_fw": 170, "n_edges_fw": 2, "w_max_banc": 82, "w_sum_banc": 137, "n_edges_banc": 3}, {"D_type": "DNa03", "X_type": "VES041", "w_max_fw": 126, "w_sum_fw": 290, "n_edges_fw": 4, "w_max_banc": 106, "w_sum_banc": 204, "n_edges_banc": 4}, {"D_type": "DNpe023", "X_type": "cL22b", "w_max_fw": 120, "w_sum_fw": 177, "n_edges_fw": 4, "w_max_banc": 115, "w_sum_banc": 206, "n_edges_banc": 4}, {"D_type": "DNp47", "X_type": "CB0580", "w_max_fw": 115, "w_sum_fw": 322, "n_edges_fw": 4, "w_max_banc": 98, "w_sum_banc": 144, "n_edges_banc": 2}, {"D_type": "DNa06", "X_type": "PS100", "w_max_fw": 111, "w_sum_fw": 188, "n_edges_fw": 2, "w_max_banc": 94, "w_sum_banc": 94, "n_edges_banc": 1}, {"D_type": "DNae007", "X_type": "PS065", "w_max_fw": 96, "w_sum_fw": 168, "n_edges_fw": 2, "w_max_banc": 159, "w_sum_banc": 259, "n_edges_banc": 2}, {"D_type": "DNp104", "X_type": "CB0580", "w_max_fw": 93, "w_sum_fw": 173, "n_edges_fw": 4, "w_max_banc": 85, "w_sum_banc": 85, "n_edges_banc": 1}, {"D_type": "DNp101", "X_type": "CB0580", "w_max_fw": 91, "w_sum_fw": 317, "n_edges_fw": 4, "w_max_banc": 109, "w_sum_banc": 189, "n_edges_banc": 2}, {"D_type": "DNge148", "X_type": "PS100", "w_max_fw": 88, "w_sum_fw": 242, "n_edges_fw": 4, "w_max_banc": 81, "w_sum_banc": 108, "n_edges_banc": 2}, {"D_type": "DNae005", "X_type": "CB0172", "w_max_fw": 88, "w_sum_fw": 165, "n_edges_fw": 2, "w_max_banc": 82, "w_sum_banc": 147, "n_edges_banc": 2}], "fw_heavy_pairs": [["DNa03", "LAL073"], ["DNa03", "PLP060"], ["DNa03", "PS100"], ["DNa03", "VES041"], ["DNa06", "PS100"], ["DNa11", "PS100"], ["DNae005", "CB0172"], ["DNae007", "PS065"], ["DNde002", "CB0005"], ["DNg100", "CB0534"], ["DNge027", "CB0109"], ["DNge027", "PS100"], ["DNge042", "CB0030"], ["DNge132", "CB0021"], ["DNge148", "PS100"], ["DNp04", "AVLP076"], ["DNp04", "AVLP077"], ["DNp04", "LHAD1g1"], ["DNp04", "PVLP010"], ["DNp09", "CB0397"], ["DNp101", "CB0580"], ["DNp104", "CB0580"], ["DNp104", "CB0626"], ["DNp23", "CB0076"], ["DNp35", "CB0527"], ["DNp47", "CB0580"], ["DNp71", "CB0534"], ["DNpe003", "PS100"], ["DNpe006", "CB0283"], ["DNpe016", "cL22c"], ["DNpe023", "CB0172"], ["DNpe023", "LAL046"], ["DNpe023", "cL22b"], ["DNpe027", "LAL040"], ["DNpe027", "LAL045"], ["DNpe027", "LAL121"], ["DNpe037", "CB0527"]], "banc_heavy_pairs": [["DNa03", "CB0172"], ["DNa03", "PLP060"], ["DNa03", "VES041"], ["DNa06", "PS100"], ["DNa09", "CB0235"], ["DNae003", "CB0235"], ["DNae005", "CB0172"], ["DNae007", "CB0172"], ["DNae007", "PS065"], ["DNde003", "CB0172"], ["DNg100", "CB0534"], ["DNg51", "PS051"], ["DNge053", "CB0580"], ["DNge148", "PS100"], ["DNp04", "PVLP010"], ["DNp09", "CB0527"], ["DNp101", "CB0580"], ["DNp104", "CB0580"], ["DNp104", "CB0626"], ["DNp35", "CB0527"], ["DNp45", "CB0580"], ["DNp47", "CB0580"], ["DNp57", "PS049"], ["DNp71", "CB0534"], ["DNpe005", "PS088"], ["DNpe016", "cL22c"], ["DNpe021", "CB0580"], ["DNpe023", "CB0172"], ["DNpe023", "cL22b"], ["DNpe026", "VES041"], ["DNpe045", "CB0626"]], "threshold_sensitivity_descriptive": {"60": 36, "80": 17, "100": 8, "120": 5, "162": 1}}
original_stub_then_set_null {"n": 10000, "mean": 2.3173, "max": 9, "exceedances": 0, "p_plus_one": 9.999000099990002e-05, "hist": {"0": 680, "1": 2212, "2": 2969, "3": 2329, "4": 1200, "5": 461, "6": 122, "7": 19, "8": 6, "9": 2}, "original_unique_edges": 31, "min_unique_edges": 28, "max_unique_edges": 31, "mean_unique_edges": 30.6089, "invalid_unique_degree_draws": 3403, "size_hist": {"28": 37, "29": 434, "30": 2932, "31": 6597}}
corrected_simple_degree_null {"n": 10000, "mean": 2.4183, "max": 9, "exceedances": 0, "p_plus_one": 9.999000099990002e-05, "hist": {"0": 602, "1": 2047, "2": 2852, "3": 2462, "4": 1363, "5": 498, "6": 139, "7": 28, "8": 7, "9": 2}, "attempts": 15332, "rejected_duplicates": 5332, "degree_guard_pass": 10000, "seed": 20261103, "method": "IID stub shuffle rejection conditional on no duplicate typed edge; exact simple in/out degrees"}
negative_control {"same_stub_degrees": true, "collapsed_simple_degrees_detected_wrong": true}
seconds 8.076529167010449
```

## audit_closure.py

```python
import json, hashlib, statistics, sys, platform
from pathlib import Path
R = Path('/workspace/astra_topo_audit_20261102')
p = R / 'cierre_original.json'
j = json.loads(p.read_text())
claimed = {'flywire': {'t1': 0.8026, 't2': 539.86}, 'banc': {'t1': 0.7431, 't2': 328.99}}
out = {'scope': 'Reaggregation of the archived 200 null results, not rerunning the connectome shuffles', 'source_commit': '7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4', 'source_path': 'results/reuso_cierre_2026-11-01/cierre.json', 'input': {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}, 'environment': {'python': sys.version, 'host': platform.node()}, 'status': j['status'], 'verdict_archived': j['H_REUSO_CIERRE'], 'p': j['p'], 'holm': j['holm'], 'connectomes': {}}
for name, c in j['connectomes'].items():
    rows = c['nulls']
    assert len(rows) == 200
    summary = {key: {'mean': statistics.mean(float(row[key]) for row in rows), 'min': min(row[key] for row in rows), 'max': max(row[key] for row in rows)} for key in ['t1', 't2', 'n_cab', 'n_pares_ffi']}
    checks = {key: abs(summary[key]['mean'] - c['summary'][key]['mean']) < 1e-12 for key in summary}
    assert all(checks.values())
    out['connectomes'][name] = {'observed': c['observed'], 'null_count': len(rows), 'recomputed': summary, 'archived_summary_matches': checks, 'latest_master_claimed': claimed[name], 'latest_master_matches': {key: abs(summary[key]['mean'] - value) < 0.00005 for key, value in claimed[name].items()}}
text = json.dumps(out, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
(R / 'closure.json').write_text(text)
print(text, end='')
```

## closure.stdout

```text
{
  "scope": "Reaggregation of the archived 200 null results, not rerunning the connectome shuffles",
  "source_commit": "7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4",
  "source_path": "results/reuso_cierre_2026-11-01/cierre.json",
  "input": {
    "bytes": 371287,
    "sha256": "a5c689d4153a9f4fcfadc573cac58521f1ade330b82d1d122dfae6f15c41aceb"
  },
  "environment": {
    "python": "3.12.14 (main, Aug 13 2026, 19:41:13) [GCC 14.2.0]",
    "host": "6c09d8604b07"
  },
  "status": "VALID",
  "verdict_archived": "SOSTENIDA",
  "p": [
    0.004975124378109453,
    0.004975124378109453,
    0.004975124378109453,
    0.004975124378109453
  ],
  "holm": [
    0.01990049751243781,
    0.01990049751243781,
    0.01990049751243781,
    0.01990049751243781
  ],
  "connectomes": {
    "flywire": {
      "observed": {
        "n_cab": 996,
        "n_pares_ffi": 880,
        "t1": 0.8835341365461847,
        "t2": 698,
        "n_x": 1118
      },
      "null_count": 200,
      "recomputed": {
        "t1": {
          "mean": 0.49660642570281127,
          "min": 0.45883534136546184,
          "max": 0.5261044176706827
        },
        "t2": {
          "mean": 286.04,
          "min": 257,
          "max": 326
        },
        "n_cab": {
          "mean": 996.0,
          "min": 996,
          "max": 996
        },
        "n_pares_ffi": {
          "mean": 494.62,
          "min": 457,
          "max": 524
        }
      },
      "archived_summary_matches": {
        "t1": true,
        "t2": true,
        "n_cab": true,
        "n_pares_ffi": true
      },
      "latest_master_claimed": {
        "t1": 0.8026,
        "t2": 539.86
      },
      "latest_master_matches": {
        "t1": false,
        "t2": false
      }
    },
    "banc": {
      "observed": {
        "n_cab": 753,
        "n_pares_ffi": 622,
        "t1": 0.8260292164674635,
        "t2": 419,
        "n_x": 716
      },
      "null_count": 200,
      "recomputed": {
        "t1": {
          "mean": 0.3501062416998672,
          "min": 0.3094289508632138,
          "max": 0.3798140770252324
        },
        "t2": {
          "mean": 76.515,
          "min": 57,
          "max": 95
        },
        "n_cab": {
          "mean": 753.0,
          "min": 753,
          "max": 753
        },
        "n_pares_ffi": {
          "mean": 263.63,
          "min": 233,
          "max": 286
        }
      },
      "archived_summary_matches": {
        "t1": true,
        "t2": true,
        "n_cab": true,
        "n_pares_ffi": true
      },
      "latest_master_claimed": {
        "t1": 0.7431,
        "t2": 328.99
      },
      "latest_master_matches": {
        "t1": false,
        "t2": false
      }
    }
  }
}
```

## Huellas de entradas, registradas durante las ejecuciones

```json
{"core": {"/workspace/dnp04/verif/sello_diseno_16_relevos.json": {"bytes": 31672, "sha256": "00bf832c3697d76c70d6d5594b44b550217e5bb4540e1c898b4b6d950341f8bb"}, "/workspace/dnp04/verif/auditoria_e_innovacion_2026_11_02.json": {"bytes": 22281, "sha256": "7e8fbb74f2462af9a4f68a7d733b73f57d498800a86a52e1326239ef3e9a4fab"}, "/workspace/connectivity.parquet": {"bytes": 100804642, "sha256": "efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347"}, "/workspace/mecanismo-2026-11-02/flywire_units.npz": {"bytes": 993755, "sha256": "fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df"}, "/workspace/mecanismo-2026-11-02/flywire_closing_paths.parquet": {"bytes": 128393, "sha256": "6efe0494b043d5084b5151f1f290ade048e87d88bf9431bd2f1b08e09ad9e6ab"}, "/workspace/mecanismo-2026-11-02/banc_closing_paths.parquet": {"bytes": 73144, "sha256": "8e5ecbbf0c52cf5226fb418ec2a66d0d98af727405004e9db0ffc26cf618831f"}, "/workspace/mecanismo-2026-11-02/actions_correr2/celda_p_LC4_right_a.json": {"bytes": 320877, "sha256": "22df0528b060e79fe3cd371055bd1248fecc667925e5caf18a837f6e2be8fb06"}, "/workspace/dnp04/actions_correr/celda_q_LC4_right_a.json": {"bytes": 376533, "sha256": "46d9eb39ae751ca6f350e48912a38ffa0e5f3bb0544eea92e4914d5009bfa760"}, "/workspace/dnp04/actions_correr/celda_q_LC4_right_b.json": {"bytes": 464599, "sha256": "94b31d08ee8906a11ae35761521d28ff176ef1b6ca25aa62ff4e86ae6ba3d07f"}, "/workspace/mecanismo-2026-11-02/actions_correr2/celda_p_LPLC2_right_a.json": {"bytes": 372608, "sha256": "d1dd6b62132088bb7d43f925ab0cbba441f394199c572c62d966e3ee43be14cd"}, "/workspace/dnp04/actions_correr/celda_q_LPLC2_right_a.json": {"bytes": 390615, "sha256": "4dbf1bc1d9a3bf5b3c214cfa412f6fbf1a4a3400dc3095228bbd4ac7d1fc9cc7"}, "/workspace/dnp04/actions_correr/celda_q_LPLC2_right_b.json": {"bytes": 481558, "sha256": "6a234c301a752a0076c22569d604c723a91cc2059506123f247183210db8130d"}, "/workspace/mecanismo-2026-11-02/actions_correr2/celda_p_LPLC1_right_a.json": {"bytes": 319193, "sha256": "934c552738478e25022b476333aee31dabe852dfc15707237849d1654be2bd36"}, "/workspace/dnp04/actions_correr/celda_q_LPLC1_right_a.json": {"bytes": 385161, "sha256": "531b892caa7e066150bd6aca053fd2fc95411c6c1de09e213d8ced95e395564e"}, "/workspace/dnp04/actions_correr/celda_q_LPLC1_right_b.json": {"bytes": 475543, "sha256": "c2ad5910d9ca7d6f5bf97f266630848d9c2edadadd0de3caf45a3d4a052ce8f9"}, "/workspace/mecanismo-2026-11-02/actions_correr2/celda_p_LPLC4_right_a.json": {"bytes": 393169, "sha256": "d23ab2856191f320a6b0e3176ca4e9643e4f8f6bd0addea86cce8cdd87adb6d7"}, "/workspace/dnp04/actions_correr/celda_q_LPLC4_right_a.json": {"bytes": 393988, "sha256": "ae284482441407af2405cf58601a720d80c4937c7ae05a2a151f6aefaf2b95fd"}, "/workspace/dnp04/actions_correr/celda_q_LPLC4_right_b.json": {"bytes": 485309, "sha256": "b1d4b5159e58c37ddabd460cd011316966006a0370f078a9f4129a78d92d0eca"}}, "banc": {"/workspace/banc_888/banc_888_meta.feather": {"sha256": "86ccf5df0c67419f8c5f43e93a7ed38d23a080e9f7fde26737290252f3780098", "bytes": 57503026}, "/workspace/banc_888/banc_888_edgelist_simple_v3.feather": {"sha256": "8c296e946f3c69a8c7222f30ad75fa8a98eeb189124fec6df829c9125f4be64b", "bytes": 359161658}, "/workspace/astra_topo_audit_20261102/fw_typed.csv": {"sha256": "e992fb732ba775a428ad69e2518defd73df4e7e739ecfcd65568db402b8e0cbb", "bytes": 143626}, "/workspace/mecanismo-2026-11-02/banc_closing_paths.parquet": {"sha256": "8e5ecbbf0c52cf5226fb418ec2a66d0d98af727405004e9db0ffc26cf618831f", "bytes": 73144}}}
```

El JSON original de cierre se obtuvo de [cierre.json fijado al commit de resultados](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4/results/reuso_cierre_2026-11-01/cierre.json). SHA-256 a5c689d4153a9f4fcfadc573cac58521f1ade330b82d1d122dfae6f15c41aceb, 371.287 bytes.

## Procedencia de los adjuntos

- Las exportaciones 165831, 165954 y 170052 son idénticas: 83.267 bytes cada una; SHA-256 2d4a6e1f2980e88803317e4fb6e08cb6f3daa0ffcc3dd108fb1051a98f05b1d8.
- La exportación 185950 tiene 91.183 bytes; SHA-256 ea155fbd886c3ea59b51617bd53a39825867fe38e0ded0d7538dbe35ec82dbd1.
- El adjunto 008 tiene 8.328 bytes; SHA-256 f0a1294e8171b9a723fa3266feee0efad0b5340e43a64aafed66d39a2a0f0151.
- El adjunto 009 tiene 12.983 bytes; SHA-256 d61afd8fe16367f745b219d2c2099682bb5cb238bff8df78fa60db799c0bdfad.

El árbol recursivo de main fijado al SHA auditado devolvió truncated=false. Ninguna ruta terminó en conservar_relevos_dx.py, disenar_16_relevos.py, diseno_corte_16_relevos.json, censo_g1_recurrente.py, censo_g1_recurrente.json o chequear_16_en_4estimulos.py. Es una afirmación sobre ese main, no sobre todas las ramas. Copias locales leídas: conservar_relevos_dx.py SHA-256 8f5d95d164a7a1e25c6d9f4b2b854280908c15047d9c1b9d9a5f1cb770fde891; disenar_16_relevos.py SHA-256 882d367197d9b0723c6e12abccaf27e92a88c46098ef7f5fb5de90723d8cc260.

## Incidencias propias

Un primer intento de publicar mediante git nativo terminó exit 128 por falta de credencial en ese transporte, sin escritura remota. Se usó después la integración autenticada de GitHub. No se cambió la rama de trabajo regression-h4-34 ni su archivo no rastreado tools/__pycache__/. Un primer agregado de cierre consultó una clave real inexistente; el instrumento definitivo usa observed, comprueba el agregado archivado y conserva su salida completa arriba. No se presenta ninguna de esas fallas como fallo del experimento auditado.
