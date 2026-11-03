#!/usr/bin/env python3
"""2026-11-03-006: cotejo de la corrida 1 de 009-A1 sin leer estimandos.

Baja de raw, en el commit del bot, los archivos de results/a1_2026-11-03/corrida_1 y comprueba:
  K1 SHA256SUMS.txt coincide con los bytes servidos;
  K2 cada bloque: ESTADO_BLOQUE con success en sus seis pasos, HUELLAS 11/11 OK, manifiesto rehecho igual al del
     intento 1 y TESTIGOS 10/10 IGUAL;
  K3 los 20 JSONL suman 8.540 lineas y sus sha256 son los que anoto validacion_corrida.json;
  K4 validacion_corrida.json dice OK, 8.540 de 8.540 y 0 fallos;
  K5 validar_a1.validar rehecho en esta maquina sobre los mismos JSONL da OK con 0 fallos;
  K6 los 8.540 recibos tienen un solo code_commit, un solo manifiesto, estado OK y CythonCodeObject.
Imprime solo estados, cuentas de archivos, huellas y datos de maquina: ningun conteo de espigas ni estimando.
Con --adulterar cambia en memoria la mask_hash del primer recibo de bloque_00 despues de K1: K3 y K5 tienen que
dar DISTINTO.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

RAIZ = 'https://raw.githubusercontent.com/gatehot59-star/drosophila-fep-connectome/%s/results/a1_2026-11-03/corrida_1/'
MANIFIESTO = '267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9'
PASOS = ('intento', 'censo', 'plan', 'testigos', 'ensayos', 'validar')


def bajar(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return r.read()
        except Exception:
            if k == 3:
                raise


def main():
    ap = argparse.ArgumentParser(description='Cotejo de la corrida 1 de 009-A1 sin estimandos')
    ap.add_argument('--commit', required=True)
    ap.add_argument('--manifiesto-local', required=True)
    ap.add_argument('--tools', required=True)
    ap.add_argument('--adulterar', action='store_true')
    a = ap.parse_args()
    sys.path.insert(0, a.tools)
    import plan_a1 as P
    import validar_a1 as V
    base = RAIZ % a.commit
    fallos = []

    def chequeo(nombre, ok, detalle):
        print('CHEQUEO %s %s %s' % (nombre, 'IGUAL' if ok else 'DISTINTO', detalle), flush=True)
        if not ok:
            fallos.append(nombre)

    sums = bajar(base + 'SHA256SUMS.txt').decode()
    filas = [l.split('  ', 1) for l in sums.splitlines() if l.strip()]
    nombres = [(h, r[2:] if r.startswith('./') else r) for h, r in filas]
    with ThreadPoolExecutor(16) as ex:
        datos = dict(zip([n for _, n in nombres], ex.map(lambda x: bajar(base + x[1]), nombres)))
    malos = [n for h, n in nombres if hashlib.sha256(datos[n]).hexdigest() != h]
    chequeo('K1_sha256sums', bool(nombres) and not malos, 'archivos=%d distintos=%s' % (len(nombres), malos[:5]))

    bloques = sorted({n.split('/')[1] for n in datos if n.startswith('bloques/')})
    ok2, det2, cpus = True, [], {}
    for kk in bloques:
        p = 'bloques/%s/' % kk
        est = datos.get(p + 'ESTADO_BLOQUE.txt', b'').decode()
        pasos_ok = all(('%s=success' % s) in est for s in PASOS)
        intento = datos.get(p + 'intento.log', b'').decode()
        huellas = sum(1 for l in intento.splitlines() if l.endswith(': OK'))
        censo = datos.get(p + 'censo.log', b'').decode()
        rehecho = ('MANIFIESTO_REHECHO_IGUAL_AL_DEL_INTENTO_1 ' + MANIFIESTO) in censo
        testigos = 'TESTIGOS 10/10 IGUAL' in datos.get(p + 'testigos.log', b'').decode()
        bien = pasos_ok and huellas == 12 and rehecho and testigos
        ok2 = ok2 and bien
        if not bien:
            det2.append('%s pasos=%s huellas=%d rehecho=%s testigos=%s' % (kk, pasos_ok, huellas, rehecho, testigos))
        modelo = [l.split(':', 1)[1].strip() for l in intento.splitlines() if l.startswith('Model name')]
        flags = [l[6:].strip() for l in intento.splitlines() if l.startswith('FLAGS ')]
        clave = '%s | %s' % (modelo[0] if modelo else '?', flags[0] if flags else '?')
        cpus.setdefault(clave, []).append(kk)
    chequeo('K2_bloques', len(bloques) == 20 and ok2, 'bloques=%d con_problemas=%s' % (len(bloques), det2[:5]))
    for clave, ks in sorted(cpus.items()):
        print('MAQUINA %s bloques=%s' % (clave, ','.join(ks)), flush=True)

    jsonl = sorted(n for n in datos if n.endswith('.jsonl'))
    if a.adulterar and jsonl:
        lineas = datos[jsonl[0]].decode().split('\n')
        r0 = json.loads(lineas[0])
        r0['mask_hash'] = '0' * 64
        lineas[0] = json.dumps(r0, sort_keys=True)
        datos[jsonl[0]] = '\n'.join(lineas).encode()
        print('ADULTERADO %s linea 1 mask_hash' % jsonl[0], flush=True)
    val = json.loads(datos['validacion_corrida.json'])
    anotados = {x['archivo']: x['sha256'] for x in val.get('archivos', [])}
    n_lineas = sum(datos[n].decode().count('\n') for n in jsonl)
    sha_ok = all(anotados.get(os.path.basename(n)) == hashlib.sha256(datos[n]).hexdigest() for n in jsonl)
    chequeo('K3_jsonl', len(jsonl) == 20 and n_lineas == 8540 and sha_ok,
            'archivos=%d lineas=%d sha_como_anotados=%s' % (len(jsonl), n_lineas, sha_ok))
    chequeo('K4_validacion_actions', val.get('estado') == 'OK' and val.get('n_registros') == 8540
            and val.get('n_esperados') == 8540 and val.get('n_fallos') == 0,
            'estado=%s registros=%s esperados=%s fallos=%s' % (val.get('estado'), val.get('n_registros'),
                                                            val.get('n_esperados'), val.get('n_fallos')))

    with open(a.manifiesto_local, 'rb') as f:
        crudo = f.read()
    man = json.loads(crudo)
    sha_man = hashlib.sha256(crudo).hexdigest()
    regs = []
    for n in jsonl:
        for k, linea in enumerate(datos[n].decode().split('\n'), 1):
            if linea:
                try:
                    regs.append(('%s:%d' % (os.path.basename(n), k), json.loads(linea)))
                except ValueError:
                    regs.append(('%s:%d' % (os.path.basename(n), k), None))
    v = V.validar(man, sha_man, regs, P.ids_plan(man))
    codigos = {}
    for x in v['fallos']:
        codigos[x['codigo']] = codigos.get(x['codigo'], 0) + 1
    chequeo('K5_validacion_rehecha', sha_man == MANIFIESTO and v['estado'] == 'OK' and v['n_fallos'] == 0,
            'manifiesto=%s estado=%s registros=%d esperados=%d fallos=%d por_codigo=%s' % (
                sha_man[:16], v['estado'], v['n_registros'], v['n_esperados'], v['n_fallos'],
                json.dumps(codigos, sort_keys=True)))

    rr = [r for _, r in regs if isinstance(r, dict)]
    commits = sorted({str(r.get('code_commit')) for r in rr})
    mans = sorted({str(r.get('manifiesto_sha256')) for r in rr})
    estados = sorted({str(r.get('estado')) for r in rr})
    codeobj = sorted({str((r.get('entorno') or {}).get('codeobj')) for r in rr})
    chequeo('K6_recibos', len(rr) == 8540 and len(commits) == 1 and mans == [MANIFIESTO] and estados == ['OK']
            and codeobj == ['CythonCodeObject'],
            'recibos=%d commit=%s manifiesto=%s estados=%s codeobj=%s' % (len(rr), commits, [m[:16] for m in mans],
                                                                      estados, codeobj))
    print('RESULTADO %d/6 IGUAL' % (6 - len(fallos)), flush=True)
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
