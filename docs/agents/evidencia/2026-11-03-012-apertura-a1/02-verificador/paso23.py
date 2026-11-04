
import subprocess, sys, hashlib, os, time
A='/workspace/a1/v2/apertura'
M='/workspace/a1/v2/manifiesto_a1.json'
H='267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9'
VER=A+'/codigo/verificador_a1/verificador_a1.py'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
res=open(A+'/log/paso23.resumen','w')
def R(s): res.write(s+'\n'); res.flush()
R('espera descarga '+time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
while True:
    lg=open(A+'/log/bajar_sobre.log').read()
    if '\nEXIT ' in lg: break
    time.sleep(5)
if '\nEXIT 0' not in lg:
    R('PARADA: la descarga no termino limpia'); sys.exit(3)
R('descarga EXIT 0 '+time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
R('verificador_a1.py sha256 '+sha(VER))
for fases,sal,logf in (('ET',A+'/ver_et',A+'/log/ver_et.log'),('ETS',A+'/ver',A+'/log/ver_ets.log')):
    os.makedirs(sal, exist_ok=True)
    cmd=[sys.executable,VER,'--manifiesto',M,'--sha-manifiesto',H,'--sobre',A+'/corrida_1','--salida',sal,'--fases',fases,'--abrir-sobre']
    R('comando '+' '.join(cmd))
    t=time.time()
    p=subprocess.run(cmd,capture_output=True,text=True,cwd=A)
    open(logf,'w').write(p.stdout+('\n--- stderr ---\n'+p.stderr if p.stderr else ''))
    R('%s rc %d %.1f s inicio %s'%(fases,p.returncode,time.time()-t,time.strftime('%H:%M:%SZ', time.gmtime(t))))
    if p.returncode!=0:
        R('PARADA en '+fases); break
for d in ('ver_et','ver'):
    for f in sorted(os.listdir(A+'/'+d)):
        q=A+'/'+d+'/'+f
        R('%s/%s %d B sha256 %s'%(d,f,os.path.getsize(q),sha(q)))
R('FIN '+time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
