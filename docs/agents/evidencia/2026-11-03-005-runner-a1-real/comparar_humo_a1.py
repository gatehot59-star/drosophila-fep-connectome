#!/usr/bin/env python3
"""2026-11-03-005: cruza el intento 1 del humo 009-A1 (Actions, run 41679588168) con lo medido en brain-env.

Lee los archivos del intento desde raw en el commit del bot y los logs locales de brain-env, y comprueba:
  C1 el manifiesto de Actions es byte a byte el de brain-env;
  C2 las 12 huellas de espigas del fixture son iguales entre numpy (brain-env) y cython (Actions);
  C3 los 10 recibos del humo: estado OK, CythonCodeObject, un solo manifiesto y un solo code_commit;
  C4 SHAM igual a C0 en espigas para cada (sujeto, regimen, semilla) del humo, y Q1 distinto de C0;
  C5 la huella de entrada es una sola entre los brazos de un mismo (sujeto, regimen, semilla);
  C6 los SHA256SUMS del intento coinciden con los bytes servidos.
Sale con 0 si todo da igual y 1 si algo difiere. Cada chequeo puede dar rojo: un byte distinto en el manifiesto,
una espiga distinta en el fixture, un recibo con otro estado o un SHAM con otra huella lo tumban.
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.request

BASE = 'https://raw.githubusercontent.com/gatehot59-star/drosophila-fep-connectome/%s/results/a1_2026-11-03/prueba_1/'


def bajar(base, nombre):
    with urllib.request.urlopen(base + nombre, timeout=60) as r:
        return r.read()


def huellas_fixture(texto):
    out = {}
    for linea in texto.splitlines():
        m = re.match(r'ENSAYO (\S+) estado=OK .* sha=([0-9a-f]{16}) ', linea)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def main():
    ap = argparse.ArgumentParser(description='Cotejo del humo 009-A1 contra brain-env')
    ap.add_argument('--commit', required=True)
    ap.add_argument('--manifiesto-local', required=True)
    ap.add_argument('--prueba-numpy', required=True)
    a = ap.parse_args()
    base = BASE % a.commit
    fallos = []

    def chequeo(nombre, ok, detalle):
        print('CHEQUEO %s %s %s' % (nombre, 'IGUAL' if ok else 'DISTINTO', detalle), flush=True)
        if not ok:
            fallos.append(nombre)

    sums = bajar(base, 'SHA256SUMS.txt').decode()
    filas = [l.split('  ', 1) for l in sums.splitlines() if l.strip()]
    cache, malos = {}, []
    for h, ruta in filas:
        nombre = ruta[2:] if ruta.startswith('./') else ruta
        b = bajar(base, nombre)
        cache[nombre] = b
        if hashlib.sha256(b).hexdigest() != h:
            malos.append(nombre)
    chequeo('C6_sha256sums', bool(filas) and not malos, 'archivos=%d distintos=%s' % (len(filas), malos))

    man_a = cache['manifiesto_a1.json']
    with open(a.manifiesto_local, 'rb') as f:
        man_l = f.read()
    chequeo('C1_manifiesto', man_a == man_l, 'actions=%s/%d brain_env=%s/%d' % (
        hashlib.sha256(man_a).hexdigest(), len(man_a), hashlib.sha256(man_l).hexdigest(), len(man_l)))

    with open(a.prueba_numpy, encoding='utf-8') as f:
        fx_np = huellas_fixture(f.read())
    fx_cy = huellas_fixture(cache['prueba_cython.log'].decode())
    dif = sorted(k for k in set(fx_np) | set(fx_cy) if fx_np.get(k) != fx_cy.get(k))
    chequeo('C2_fixture_numpy_vs_cython', len(fx_np) == 12 and not dif,
            'ensayos numpy=%d cython=%d distintos=%s' % (len(fx_np), len(fx_cy), dif))

    regs = {n: json.loads(b) for n, b in cache.items() if n.startswith('registros_humo/')}
    estados = sorted(set(r['estado'] for r in regs.values()))
    codeobj = sorted(set(r['entorno']['codeobj'] for r in regs.values()))
    mans = sorted(set(r['manifiesto_sha256'] for r in regs.values()))
    commits = sorted(set(r['code_commit'] for r in regs.values()))
    chequeo('C3_recibos', len(regs) == 10 and estados == ['OK'] and codeobj == ['CythonCodeObject']
            and len(mans) == 1 and len(commits) == 1,
            'n=%d estados=%s codeobj=%s manifiesto=%s commit=%s' % (len(regs), estados, codeobj, mans, commits))

    por = {}
    for r in regs.values():
        por.setdefault((r['subject_id'], r['regime'], int(r['seed'])), {})[r['condition']] = r
    lineas, ok4 = [], True
    for k in sorted(por):
        c = por[k]
        if 'SHAM' in c:
            igual = c['SHAM']['espigas_sha256'] == c['C0']['espigas_sha256']
            ok4 = ok4 and igual
            lineas.append('%s|%s|%d SHAM==C0 %s' % (k[0], k[1], k[2], igual))
        if 'Q1' in c:
            dist = c['Q1']['espigas_sha256'] != c['C0']['espigas_sha256']
            ok4 = ok4 and dist
            lineas.append('%s|%s|%d Q1!=C0 %s x_C0=%s x_Q1=%s' % (k[0], k[1], k[2], dist, c['C0']['cuenta_x'],
                                                                  c['Q1']['cuenta_x']))
    chequeo('C4_sham_y_q1', ok4 and len(lineas) == 5, '; '.join(lineas))

    ok5, det5 = True, []
    for k in sorted(por):
        hs = sorted(set(r['input_events_hash'] for r in por[k].values()))
        ok5 = ok5 and len(hs) == 1
        det5.append('%s|%s|%d brazos=%d huellas_entrada=%d' % (k[0], k[1], k[2], len(por[k]), len(hs)))
    chequeo('C5_entrada_pareada', ok5, '; '.join(det5))

    for n in sorted(regs):
        r = regs[n]
        print('RECIBO %s x=%s G=%s total=%s sim_s=%s seg=%s Dprime_n=%s eventos=%s mask_n=%s' % (
            n.split('/')[-1], r['cuenta_x'], r['cuentas_G'], r['espigas_total'], r.get('duracion_sim_s'),
            r['duracion_s'], r['Dprime_n'], r['n_input_events'], r['mask_n']), flush=True)
    print('RESULTADO %d/6 IGUAL' % (6 - len(fallos)), flush=True)
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
