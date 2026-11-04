#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mutantes del verificador independiente de 009-A1 (respuesta 2026-11-03-010).

Cada mutante cambia una linea del verificador y corre las pruebas que lo tienen que matar.
Esta MUERTO si la prueba sale con codigo distinto de 0 y escribe al menos una linea FAIL.
El control corre las mismas pruebas sobre el verificador sin cambios: tienen que pasar.

Uso
  python3 mutantes_verificador_a1.py --verificador V --prueba P --manifiesto M --sha-manifiesto SHA \
      --sobre-limpio DIR --agregado-limpio A --trabajo DIR
"""

import argparse
import os
import subprocess
import sys

MUTANTES = [
    ('M01', 'T7 sin el chequeo de cuenta_x',
     "        if cx != cm[pos[suj['x']]]:\n",
     "        if False:\n", 'V10'),
    ('M02', 'Holm cambiado por Bonferroni',
     "min(1.0, (m - rango) * pruebas[i]['p_familia'])",
     "min(1.0, m * pruebas[i]['p_familia'])", 'V03'),
    ('M03', 'inversion de signos con la tolerancia al reves',
     'np.abs(a[:, None] + b[None, :]) >= obs - tol',
     'np.abs(a[:, None] + b[None, :]) >= obs + tol', 'V02'),
    ('M04', 'D4: no consume el bloque de las celdas invalidas',
     '            gen.integers(0, N, size=(N_BOOT, N))  # D4: el bloque se consume igual\n',
     '            pass\n', 'V07'),
    ('M05', 'D3 sin INDEFINIDO',
     'if np.any(np.mean(den[idx], axis=-1) <= 0) or np.any(np.mean(den[_JK], axis=-1) <= 0):',
     'if False:', 'V06'),
    ('M06', 'una falla sin celda ya no invalida las 44',
     "invalidas = sorted(plan) if globales else sorted({x['celda'] for x in fallas})",
     "invalidas = sorted({x['celda'] for x in fallas if x['celda']})", 'V11'),
    ('M07', 'la trampa del BCa degenerado arreglada en vez de reproducida',
     "    if motivo:\n        motor['degenerados'] += 1\n",
     "    if False:\n        motor['degenerados'] += 1\n", 'V05,V14'),
    ('M08', 'T5 sin el chequeo de SHAM contra C0',
     'if a and b and any(',
     'if False and a and b and any(', 'V10'),
    ('M09', 'activacion con drivers a 1 Hz en vez de 10',
     "crit = {'drivers_C0_ge_10Hz': all(v >= TASA_MIN_HZ for v in drivers),",
     "crit = {'drivers_C0_ge_10Hz': all(v >= 1.0 for v in drivers),", 'V14'),
    ('M10', 'z0 sin la mitad de los empates',
     'frac = (np.count_nonzero(theta_b < theta) + 0.5 * np.count_nonzero(theta_b == theta)) / b',
     'frac = np.count_nonzero(theta_b < theta) / b', 'V04,V14'),
]


def correr(a, verificador, pruebas, destino):
    cmd = [sys.executable, a.prueba, '--verificador', verificador, '--manifiesto', a.manifiesto,
           '--sha-manifiesto', a.sha_manifiesto, '--sobre-limpio', a.sobre_limpio,
           '--agregado-limpio', a.agregado_limpio, '--trabajo', destino, '--pruebas', pruebas]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p.returncode, p.stdout


def main():
    ap = argparse.ArgumentParser()
    for nombre in ('--verificador', '--prueba', '--manifiesto', '--sha-manifiesto', '--sobre-limpio',
                   '--agregado-limpio', '--trabajo'):
        ap.add_argument(nombre, required=True)
    a = ap.parse_args()
    with open(a.verificador, 'r', encoding='utf-8') as f:
        fuente = f.read()
    todas = sorted({p for m in MUTANTES for p in m[4].split(',')})
    rc, out = correr(a, a.verificador, ','.join(todas), os.path.join(a.trabajo, 'control'))
    ultima = [ln for ln in out.splitlines() if ln.startswith('RESUMEN')]
    print('CONTROL rc %d %s' % (rc, ultima[-1] if ultima else 'sin resumen'))
    if rc != 0:
        print(out)
        print('RESUMEN control roto: no se evaluan mutantes')
        return 1
    muertos = 0
    for mid, desc, viejo, nuevo, pruebas in MUTANTES:
        if fuente.count(viejo) != 1:
            print('%s NO_APLICA %s: el texto a mutar aparece %d veces' % (mid, desc, fuente.count(viejo)))
            continue
        d = os.path.join(a.trabajo, mid)
        os.makedirs(d, exist_ok=True)
        ruta = os.path.join(d, 'verificador_a1.py')
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(fuente.replace(viejo, nuevo))
        rc, out = correr(a, ruta, pruebas, os.path.join(d, 'trabajo'))
        fails = [ln for ln in out.splitlines() if ' FAIL ' in ln]
        estado = 'MUERTO' if rc != 0 and fails else 'VIVO'
        muertos += estado == 'MUERTO'
        print('%s %s (%s) %s | %s' % (mid, estado, pruebas, desc, fails[0][:160] if fails else 'sin FAIL'))
    print('RESUMEN %d/%d MUERTOS' % (muertos, len(MUTANTES)))
    return 0 if muertos == len(MUTANTES) else 1


if __name__ == '__main__':
    sys.exit(main())
