
import subprocess, sys, hashlib, os, time
A='/workspace/a1/v2/apertura'
M='/workspace/a1/v2/manifiesto_a1.json'
H='267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9'
VER=A+'/codigo/verificador_a1/verificador_a1.py'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
res=open(A+'/log/paso5.resumen','w')
def R(s): res.write(s+'\n'); res.flush()
R('verificador_a1.py sha256 '+sha(VER))
R('ver/verificador_a1.json antes de K sha256 '+sha(A+'/ver/verificador_a1.json'))
R('prod/agregado_a1.json sha256 '+sha(A+'/prod/agregado_a1.json'))
cmd=[sys.executable,VER,'--manifiesto',M,'--sha-manifiesto',H,'--sobre',A+'/corrida_1','--salida',A+'/ver','--fases','ETK','--agregado-productor',A+'/prod/agregado_a1.json','--abrir-sobre']
R('comando '+' '.join(cmd))
t=time.time()
p=subprocess.run(cmd,capture_output=True,text=True,cwd=A)
open(A+'/log/ver_etk.log','w').write(p.stdout+('\n--- stderr ---\n'+p.stderr if p.stderr else ''))
R('ETK rc %d %.1f s inicio %s'%(p.returncode,time.time()-t,time.strftime('%H:%M:%SZ', time.gmtime(t))))
R('ver/verificador_a1.json despues de K sha256 '+sha(A+'/ver/verificador_a1.json'))
for f in sorted(os.listdir(A+'/ver')):
    q=A+'/ver/'+f
    R('ver/%s %d B sha256 %s'%(f,os.path.getsize(q),sha(q)))
R('FIN '+time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
