import urllib.request, urllib.error, json, hashlib
H={'Accept':'application/vnd.github+json','User-Agent':'brain-env-a1-diagnostico'}
def get(u, js=True):
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=25) as r:
            b=r.read(); return r.status, (json.loads(b.decode()) if js else b)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
for run,job in [(41648167250,125958935392),(41648182953,125959324626),(41648392932,125959723707)]:
    s,a=get('https://api.github.com/repos/gatehot59-star/drosophila-fep-connectome/check-runs/%d/annotations'%job)
    print('ANNOT run',run,'job',job,'http',s)
    if s==200:
        for x in a: print('   ',x.get('annotation_level'),'|',x.get('title'),'|',x.get('message'),'| linea',x.get('start_line'))
    else: print('   ',a)
s,l=get('https://api.github.com/repos/gatehot59-star/drosophila-fep-connectome/actions/jobs/125958935392/logs',js=False)
print('LOG_JOB1 http',s, (l[:150] if isinstance(l,str) else len(l)))
R='https://raw.githubusercontent.com/gatehot59-star/drosophila-fep-connectome/'
s,b=get(R+'3ac80ddecdc9aef6f9514531808b84ca9f1aef04/results/a1_prueba/RESULTADO.txt',js=False); print('RESULTADO_3ac80dd',s,b)
s,b=get(R+'92b47130bb4ac1ae9b7c5a0d2666b0d48c544823/results/a1_prueba/RESULTADO.txt',js=False); print('RESULTADO_92b4713',s,b)
pub={'tools/a1/comun_a1.py':'3dad41c68b900c538cad0ab6deb01a2dea6626c928892232e6b593bc3ed27f23','tools/a1/manifiesto_a1.py':'e323c201c969897ec638c672dea4cd734cfcfb33c7f617d17315135466c4e3b4','tools/a1/runner_a1.py':'be17b25b83881fbdd11ca8ef2d19dc467430f0e9f925072a01882ce7990c796c','tools/a1/prueba_a1.py':'5854ee745a9496b7fe8d8ed2c16d309047509c608a725dca9ac28c0f1c675ed8','.github/workflows/a1-prueba.yml':'c788b4be5556dbf586d311b618d7717bd10cafaa9eeb311e5f42c69a8917c597'}
import os
os.makedirs('/workspace/a1/publicado_73cc060',exist_ok=True); os.makedirs('/workspace/a1/publicado_7966f71',exist_ok=True)
for c,d in [('73cc060b05b7937b08fe14378002adb03b274f2a','/workspace/a1/publicado_73cc060'),('7966f71c441a055b990d02b748321e5a59500334','/workspace/a1/publicado_7966f71')]:
    for p,h in pub.items():
        s,b=get(R+c+'/'+p,js=False)
        if s!=200: print('RAW',c[:7],p,s); continue
        open(os.path.join(d,os.path.basename(p)),'wb').write(b)
        x=hashlib.sha256(b).hexdigest()
        print('SHA',c[:7],p,len(b),x,'IGUAL_A_003' if x==h else 'DISTINTO_DE_003')
