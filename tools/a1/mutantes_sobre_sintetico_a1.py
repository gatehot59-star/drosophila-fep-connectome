#!/usr/bin/env python3
"""mutantes_sobre_sintetico_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-009).

Prueba que prueba_sobre_sintetico_a1.py puede dar rojo: copia tools/a1 a un directorio temporal, aplica un cambio
por vez (en el generador, en el control del productor o en su estadistica) y exige que la prueba termine con exit 1.
Antes corre el original, que tiene que dar exit 0. Cada cambio tiene que aparecer exactamente una vez en su archivo.
Uso: python3 mutantes_sobre_sintetico_a1.py --manifiesto M --sha-manifiesto H --trabajo DIR
Exit 0 si el original pasa y todos los mutantes mueren; 1 si no.
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
ARCHIVOS = ('comun_a1.py', 'plan_a1.py', 'juntar_a1.py', 'validar_a1.py', 'estadistica_a1.py',
            'sobre_sintetico_a1.py', 'prueba_sobre_sintetico_a1.py')
MUTANTES = [
    ('M01', 'huella de mascara alterada en todos los recibos', 'sobre_sintetico_a1.py',
     "'mask_hash': hc['sha256'],", "'mask_hash': hc['sha256'][::-1],"),
    ('M02', 'SHAM con la basura de Q1 y no la de C0', 'sobre_sintetico_a1.py',
     "basura['SHAM'] = basura.get('C0')", "basura['SHAM'] = basura.get('Q1')"),
    ('M03', 'semilla que depende del proceso', 'sobre_sintetico_a1.py',
     "'|'.join(str(p) for p in partes).encode('utf-8')).hexdigest()[:16], 16)",
     "'|'.join(str(p) for p in partes + (os.getpid(),)).encode('utf-8')).hexdigest()[:16], 16)"),
    ('M04', 'trampa sembrada ignorada', 'sobre_sintetico_a1.py',
     "trampa = bool(par.get('trampa'))", "trampa = False"),
    ('M05', 'control del productor sin el chequeo SHAM igual a C0', 'validar_a1.py',
     "if 'C0' in conds and 'SHAM' in conds:", "if False:"),
    ('M06', 'flujo PCG64 que saltea los ids invalidos (rompe D4)', 'estadistica_a1.py',
     "    for qid in sorted(cant):\n        idx = rng.integers(0, n, size=(n_boot, n))",
     "    for qid in sorted(k for k in cant if cant[k] is not None):\n"
     "        idx = rng.integers(0, n, size=(n_boot, n))"),
    ('M07', 'falla tecnica que conserva las cuentas', 'sobre_sintetico_a1.py',
     "        for k in CUENTAS:\n            r.pop(k, None)\n", ""),
]


def correr(dir_codigo, man, sha, trabajo):
    t0 = time.time()
    p = subprocess.run([sys.executable, os.path.join(dir_codigo, 'prueba_sobre_sintetico_a1.py'), '--manifiesto', man,
                        '--sha-manifiesto', sha, '--trabajo', trabajo], capture_output=True, text=True)
    caidas = [ln.split()[1] for ln in p.stdout.splitlines() if ln.startswith('PRUEBA ') and ' FAIL' in ln]
    final = [ln for ln in p.stdout.splitlines() if ln.startswith('PRUEBA_SOBRE_SINTETICO')]
    final = final[-1] if final else 'SIN_LINEA_FINAL ' + p.stderr.strip()[-200:]
    return p.returncode, caidas, final, time.time() - t0


def main():
    ap = argparse.ArgumentParser(description='Mutantes del ensayo general del productor')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--trabajo', required=True)
    a = ap.parse_args()
    base = os.path.abspath(a.trabajo)
    os.makedirs(base, exist_ok=True)
    print('MUTANTES inicio n=%d' % len(MUTANTES), flush=True)
    rc, caidas, final, seg = correr(AQUI, a.manifiesto, a.sha_manifiesto, os.path.join(base, 'original'))
    ok = rc == 0
    print('CONTROL original exit=%d caidas=%s %s (%.1f s)' % (rc, ','.join(caidas) or '-', final, seg), flush=True)
    vivos = []
    for mid, que, archivo, viejo, nuevo in MUTANTES:
        d = os.path.join(base, mid, 'codigo')
        shutil.rmtree(os.path.join(base, mid), ignore_errors=True)
        os.makedirs(d)
        for x in ARCHIVOS:
            shutil.copy(os.path.join(AQUI, x), os.path.join(d, x))
        ruta = os.path.join(d, archivo)
        with open(ruta, encoding='utf-8') as f:
            txt = f.read()
        if txt.count(viejo) != 1:
            print('MUTANTE %s INVALIDO (%s): el texto aparece %d veces en %s' % (mid, que, txt.count(viejo), archivo),
                  flush=True)
            ok = False
            continue
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(txt.replace(viejo, nuevo))
        rc, caidas, final, seg = correr(d, a.manifiesto, a.sha_manifiesto, os.path.join(base, mid, 'trabajo'))
        muerto = rc == 1 and bool(caidas) and final.startswith('PRUEBA_SOBRE_SINTETICO') and final.endswith(')') \
            and ' FAIL ' in final
        if not muerto:
            vivos.append(mid)
        print('MUTANTE %s %s (%s) exit=%d caidas=%s %s (%.1f s)' % (
            mid, 'MUERTO' if muerto else 'VIVO', que, rc, ','.join(caidas) or '-', final, seg), flush=True)
    print('MUTANTES muertos %d/%d vivos=%s' % (len(MUTANTES) - len(vivos), len(MUTANTES), ','.join(vivos) or '-'),
          flush=True)
    raise SystemExit(0 if ok and not vivos else 1)


if __name__ == '__main__':
    main()
