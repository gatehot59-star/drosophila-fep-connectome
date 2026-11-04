
import subprocess, sys, hashlib, os, time
A='/workspace/a1/v2/apertura'
M='/workspace/a1/v2/manifiesto_a1.json'
H='267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9'
PROD=A+'/codigo/a1/estadistica_a1.py'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
res=open(A+'/log/paso4.resumen','w')
def R(s): res.write(s+'\n'); res.flush()
R('estadistica_a1.py sha256 '+sha(PROD))
for f in ('comun_a1.py','plan_a1.py','validar_a1.py','juntar_a1.py'):
    R('%s sha256 %s'%(f,sha(A+'/codigo/a1/'+f)))
os.makedirs(A+'/prod', exist_ok=True)
cmd=[sys.executable,PROD,'--manifiesto',M,'--sha-manifiesto',H,'--jsonl',A+'/corrida_1/bloques/**/bloque_*.jsonl','--salida',A+'/prod','--abrir-sobre']
R('comando '+' '.join(cmd))
t=time.time()
p=subprocess.run(cmd,capture_output=True,text=True,cwd=A+'/codigo/a1')
open(A+'/log/productor.stdout','w').write(p.stdout)
open(A+'/log/productor.stderr','w').write(p.stderr)
R('rc %d %.1f s inicio %s'%(p.returncode,time.time()-t,time.strftime('%H:%M:%SZ', time.gmtime(t))))
R('stdout %d B sha256 %s | stderr %d B'%(len(p.stdout.encode()),hashlib.sha256(p.stdout.encode()).hexdigest(),len(p.stderr.encode())))
for f in sorted(os.listdir(A+'/prod')):
    q=A+'/prod/'+f
    R('prod/%s %d B sha256 %s'%(f,os.path.getsize(q),sha(q)))
R('FIN '+time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
