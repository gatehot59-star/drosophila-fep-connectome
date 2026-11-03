import time, hashlib, numpy as np, pyarrow.parquet as pq, re, os, tempfile
t0=time.time()
tab=pq.read_table('/workspace/connectivity.parquet',columns=['Presynaptic_Index','Postsynaptic_Index'])
pre=tab.column(0).to_numpy().astype(np.int64); post=tab.column(1).to_numpy().astype(np.int64); del tab
upre=np.unique(pre); upost=np.unique(post)
print('FILAS',pre.size,'PRE_UNICOS',upre.size,'POST_UNICOS',upost.size,'carga_s',round(time.time()-t0,1))
rng=np.random.default_rng(0); muestra=rng.choice(upre,200,replace=False)
t1=time.time()
for i in muestra: np.flatnonzero(pre==i)
dt=(time.time()-t1)/200
print('SEG_POR_FLATNONZERO',round(dt,5),'EXTRAPOLADO_bypre_min',round(dt*upre.size/60,1),'EXTRAPOLADO_bypost_min',round(dt*upost.size/60,1),'TOTAL_h',round(dt*(upre.size+upost.size)/3600,2))
u=np.load('/workspace/mecanismo-2026-11-02/flywire_units.npz'); print('ORDEN_CLAVES',u.files)
arr={k:u[k] for k in u.files}
def sh(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
d=tempfile.mkdtemp(dir='/workspace/a1')
np.savez(d+'/a.npz',**arr); time.sleep(2); np.savez(d+'/b.npz',**arr); np.savez_compressed(d+'/c.npz',**arr)
print('SAVEZ_a',sh(d+'/a.npz'),'SAVEZ_b',sh(d+'/b.npz'),'COMPRIMIDO',sh(d+'/c.npz'),'ORIGINAL','fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df', os.path.getsize(d+'/a.npz'), os.path.getsize(d+'/c.npz'))
for f in ['runner_a1.py','manifiesto_a1.py','prueba_a1.py']:
    s=open('/workspace/a1/publicado_7966f71/'+f).read()
    print('GREP',f,'brian2=',s.count('brian2'),'create_model=',s.count('create_model'),'net.run=',s.count('.run('),'59804=',s.count('59804'),'aferente=',s.count('aferente'),'blanco=',s.count('blanco'))
s=open('/workspace/a1/publicado_7966f71/prueba_a1.py').read()
for m in re.finditer(r"check\('(empty_mask|paired_input)',[^;]*", s): print('TAUTOLOGIA', m.group(0))
s=open('/workspace/a1/publicado_7966f71/manifiesto_a1.py').read()
for l in s.split('\n'):
    if 'bypre=' in l or "role='replay'" in l or 'units_sha256' in l and 'assert' in l: print('LINEA', l.strip()[:260])
w=open('/workspace/a1/publicado_7966f71/a1-prueba.yml').read()
print('SUDO_EN_WORKFLOW', w.count('sudo'))
import urllib.request
old=urllib.request.urlopen('https://raw.githubusercontent.com/gatehot59-star/drosophila-fep-connectome/titan/mecanismo-dnp04-2026-11-02/.github/workflows/mecanismo-correr2.yml',timeout=20).read().decode()
for l in old.split('\n'):
    if 'sudo' in l: print('RECETA_VIEJA', l.strip())
