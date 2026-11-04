
import urllib.request, hashlib, os, time, collections
R='gatehot59-star/drosophila-fep-connectome'
SELLO='7d953dc8577ecf1fdbaecc4859b902af8854e79b'
A='/workspace/a1/v2/apertura'
S=A+'/corrida_1'
os.makedirs(S, exist_ok=True)
log=open(A+'/log/bajar_sobre.log','w')
def P(s):
    log.write(s+'\n'); log.flush()
def raw(p, intentos=5):
    url='https://raw.githubusercontent.com/%s/%s/results/a1_2026-11-03/corrida_1/%s'%(R,SELLO,p)
    for k in range(intentos):
        try:
            req=urllib.request.Request(url, headers={'User-Agent':'brain-env-a1'})
            with urllib.request.urlopen(req, timeout=90) as r: return r.read()
        except Exception as e:
            P('reintento %d %s %r'%(k+1,p,e)); time.sleep(2+4*k)
    P('FALLO_DESCARGA '+p); P('EXIT 1'); raise SystemExit(1)
P('inicio '+time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())+' sello '+SELLO)
for f in ['SHA256SUMS.txt','validacion_corrida.json','RESULTADO.txt','juntar.log','juntar_intento.log']:
    b=raw(f); open(S+'/'+f,'wb').write(b)
    P('top %s %d B sha256 %s'%(f,len(b),hashlib.sha256(b).hexdigest()))
sums=open(S+'/SHA256SUMS.txt').read().strip().split('\n')
tipos=collections.Counter()
ok=0; mal=[]; total=0
for i,line in enumerate(sums):
    h,p=line.split(None,1); p=p.strip()
    rel=p[2:] if p.startswith('./') else p
    tipos[os.path.dirname(rel).split('/')[0]+'/*/'+(rel.rsplit('.',1)[-1] if '.' in rel else '')]+=1
    b=raw(rel); total+=len(b)
    dst=S+'/'+rel
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst,'wb').write(b)
    if hashlib.sha256(b).hexdigest()==h: ok+=1
    else: mal.append(rel)
    if i%50==0: P('progreso %d/%d'%(i,len(sums)))
P('tipos de archivo en SHA256SUMS: '+repr(sorted(tipos.items())))
P('archivos en SHA256SUMS %d iguales %d distintos %d bytes %d'%(len(sums),ok,len(mal),total))
for m in mal[:20]: P('DISTINTO '+m)
P('fin '+time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
P('EXIT '+('0' if not mal else '1'))
