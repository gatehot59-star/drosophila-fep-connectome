# correr_g1a.py: lanza g1a.py o sus pruebas en segundo plano y deja el exit code de cada proceso en corrida.log
import sys, os, json, time, subprocess
OUT, modo = sys.argv[1], sys.argv[2]
AQUI = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')


def lanzar(args, nombre):
    fo = open(os.path.join(OUT, nombre + '.out'), 'w')
    fe = open(os.path.join(OUT, nombre + '.err'), 'w')
    return nombre, subprocess.Popen([sys.executable] + args, stdout=fo, stderr=fe, env=ENV, cwd=AQUI), time.time(), args


def registrar(nombre, p, t0, args):
    rc = p.wait()
    with open(os.path.join(OUT, 'corrida.log'), 'a') as f:
        f.write(json.dumps(dict(nombre=nombre, args=args, rc=rc, segundos=round(time.time() - t0, 1),
                                fin=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())), sort_keys=True) + chr(10))
    return rc


g1a = os.path.join(AQUI, 'g1a.py')
if modo == 'pruebas':
    registrar(*lanzar([os.path.join(AQUI, 'pruebas_g1a.py'), OUT], 'pruebas'))
elif modo == 'calibrar':
    ps = [lanzar([g1a, 'calibrar', m, OUT], 'cal_' + m) for m in ('flywire', 'banc')]
    for p in ps:
        registrar(*p)
elif modo == 'cruzar':
    sha, sello = sys.argv[3], sys.argv[4]
    if registrar(*lanzar([g1a, 'cruzar', 'flywire', OUT, sha, sello], 'cruce_flywire')) == 0:
        if registrar(*lanzar([g1a, 'cruzar', 'banc', OUT, sha, sello, os.path.join(OUT, 'cruce_flywire.json')],
                             'cruce_banc')) == 0:
            registrar(*lanzar([g1a, 'leer', OUT], 'lectura'))
else:
    raise SystemExit('modo desconocido: ' + modo)
