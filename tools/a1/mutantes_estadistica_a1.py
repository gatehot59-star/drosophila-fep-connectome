#!/usr/bin/env python3
"""mutantes_estadistica_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-008).

Analisis de mutantes de estadistica_a1.py: aplica de a uno un cambio chico (un error plausible de implementacion o
de lectura de 010) sobre una copia y corre prueba_estadistica_a1.py contra esa copia. MUERTO = la prueba da exit
distinto de 0; VIVO = pasa igual, o sea que la suite no ve ese error. Antes de los mutantes corre la copia sin tocar,
que tiene que pasar; cada reemplazo tiene que aparecer exactamente una vez en el original.
Uso: python3 mutantes_estadistica_a1.py --manifiesto M --sha-manifiesto H --trabajo DIR [--sin E17,E18] [--solo M01]
Exit 0 si el control pasa y no queda ningun mutante VIVO; 1 si queda alguno; 2 si el control falla o un reemplazo no
se encuentra una sola vez.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
COPIAR = ('estadistica_a1.py', 'prueba_estadistica_a1.py', 'comun_a1.py', 'plan_a1.py', 'juntar_a1.py', 'validar_a1.py')
MUTANTES = [
    ('M01', 't bilateral en vez de unilateral',
     "'p': float(stats.t.sf(t, n - 1))", "'p': float(2 * stats.t.sf(abs(t), n - 1))"),
    ('M02', 'Bonferroni en vez de Holm',
     'acum = max(acum, min(1.0, (m - rango) * p[i]))', 'acum = min(1.0, m * p[i])'),
    ('M03', 'BCa sin aceleracion',
     'acel = float(np.sum((jm - jack) ** 3)) / den', 'acel = 0.0'),
    ('M04', 'margen de T1 fijo en 0,35',
     "q['T1a'] = ('media', dq1 - margenes['T1_r'] * dq2)", "q['T1a'] = ('media', dq1 - 0.35 * dq2)"),
    ('M05', 'activacion de B sin el criterio de Holm',
     "ok['DQ2_F_B_holm_lt_001'] = bool(prueba_dq2['decide'])", "ok['DQ2_F_B_holm_lt_001'] = True"),
    ('M06', 'activacion de B con el p crudo',
     "ok['DQ2_F_B_holm_lt_001'] = bool(prueba_dq2['decide'])",
     "ok['DQ2_F_B_holm_lt_001'] = bool(prueba_dq2['p_observado'] is not None and prueba_dq2['p_observado'] < ALFA)"),
    ('M07', 'T2c contra el maximo de los cortes individuales',
     "q['T2c'] = ('media', dqc - np.mean(ind, axis=0))", "q['T2c'] = ('media', dqc - np.max(ind, axis=0))"),
    ('M08', 'flujo PCG64 que salta los ids invalidos',
     '        idx = rng.integers(0, n, size=(n_boot, n))\n        out[qid] = None if cant[qid] is None else '
     'evaluar(cant[qid], idx)',
     '        if cant[qid] is None:\n            out[qid] = None\n            continue\n        idx = rng.integers(0, n, '
     'size=(n_boot, n))\n        out[qid] = evaluar(cant[qid], idx)'),
    ('M09', 'tipo de hub que pasa con una sola instancia',
     "    if all(e == 'PASA' for e in estados):\n        return 'PASA'",
     "    if any(e == 'PASA' for e in estados):\n        return 'PASA'"),
    ('M10', 'cocientes de A con la regla de B',
     "freno, base = excluye_cero(iv[pre + 'DQ2']), excluye_cero(iv[pre + 'HC0'])", 'freno = base = activo'),
    ('M11', 'media de cocientes por semilla en vez de cociente de medias',
     '    theta = ma / mb\n', '    theta = float(np.mean(a / b))\n'),
    ('M12', 'FC invertido',
     "q['FC'] = ('media', H('C_' + '1' * len(suj['G'])) - H('C_desplazado'))",
     "q['FC'] = ('media', H('C_desplazado') - H('C_' + '1' * len(suj['G'])))"),
    ('M13', 'una falla sin celda no invalida nada',
     '    if globales:\n        for key in tabla:', '    if False:\n        for key in tabla:'),
    ('M14', 'inversion de signos unilateral',
     'return float((int(altos.sum()) + int(bajos.sum())) / 2.0 ** n)', 'return float(int(altos.sum()) / 2.0 ** n)'),
    ('M15', 'banco C sin etiqueta INDETERMINADO',
     "if any(v['etiqueta'] == 'IND' for v in tabla.values()):", 'if False:'),
    ('M16', 'borde de QWEAK con <=',
     "return 'PEQUENO' if a < BANDAS_WEAK[0]", "return 'PEQUENO' if a <= BANDAS_WEAK[0]"),
    ('M17', 'IC que excluye cero solo por arriba',
     "and (q['ic95'][0] > 0 or q['ic95'][1] < 0))", "and (q['ic95'][0] > 0))"),
    ('M18', 'sin control de varianza cero',
     'if not math.isfinite(de) or de <= 1e-12 * max(1.0, abs(m)):', 'if not math.isfinite(de) or de < 0:'),
    ('M19', 'centinela 0 en vez de 1 para lo invalido',
     "'gl': None, 'p_observado': None, 'p_familia': 1.0, 'signos_bilateral': None})",
     "'gl': None, 'p_observado': None, 'p_familia': 0.0, 'signos_bilateral': None})"),
    ('M20', 'ON con > 10 Hz',
     "'etiqueta': 'ON' if h >= TASA_MIN else ('OFF' if h <= TASA_OFF else 'IND')",
     "'etiqueta': 'ON' if h > TASA_MIN else ('OFF' if h <= TASA_OFF else 'IND')"),
    ('M21', 'OFF con < 2 Hz',
     "'etiqueta': 'ON' if h >= TASA_MIN else ('OFF' if h <= TASA_OFF else 'IND')",
     "'etiqueta': 'ON' if h >= TASA_MIN else ('OFF' if h < TASA_OFF else 'IND')"),
    ('M22', 'drivers con > 10 Hz',
     "'drivers_C0_ge_10Hz': bool(np.all(g0 >= TASA_MIN))", "'drivers_C0_ge_10Hz': bool(np.all(g0 > TASA_MIN))"),
    ('M23', 'DQ2 con > 5 Hz', "'DQ2_ge_5Hz': bool(est >= DQ2_MIN)", "'DQ2_ge_5Hz': bool(est > DQ2_MIN)"),
    ('M24', 'Y suma todo mirar y no solo el D',
     "        e['Y'][k] = d.sum()", "        e['Y'][k] = float(np.sum(cm))"),
    ('M25', 'ZA2 con el signo invertido',
     "q['ZA2'] = ('media', (H('ZA') - h0) - (H('ZAuQ1') - H('Q1')))",
     "q['ZA2'] = ('media', (H('ZAuQ1') - H('Q1')) - (H('ZA') - h0))"),
    ('M26', 'interaccion de colaterales invertida',
     "q['COL_interaccion'] = ('media', (Y('Q1uQCOL') - Y('Q1')) - (Y('QCOL') - y0))",
     "q['COL_interaccion'] = ('media', (Y('QCOL') - y0) - (Y('Q1uQCOL') - Y('Q1')))"),
    ('M27', 'P_T1_B con 2 de 3', "'P_T1_B': {'veredicto': combinar(u1, 3)", "'P_T1_B': {'veredicto': combinar(u1, 2)"),
    ('M28', 'firma F_R01 con un solo contraste',
     "firma = 'SOSTENIDA' if all(p['decide'] for p in za.values()) else 'SIN_DECIDIR'",
     "firma = 'SOSTENIDA' if any(p['decide'] for p in za.values()) else 'SIN_DECIDIR'"),
]


def correr(dir_copia, a, sin):
    pruebas = [n for n in ('E%02d' % k for k in range(1, 24)) if n not in sin]
    cmd = [sys.executable, os.path.join(dir_copia, 'prueba_estadistica_a1.py'), '--manifiesto', a.manifiesto,
           '--sha-manifiesto', a.sha_manifiesto, '--solo', ','.join(pruebas), '--tmp', dir_copia]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    caidas = re.findall(r'^PRUEBA (E\d\d) FAIL', p.stdout, flags=re.M)
    final = [ln for ln in p.stdout.splitlines() if ln.startswith('PRUEBA_ESTADISTICA ') and '/' in ln]
    return p.returncode, caidas, (final[-1] if final else (p.stderr.strip().splitlines() or ['sin salida'])[-1]), \
        time.time() - t0


def main():
    ap = argparse.ArgumentParser(description='Mutantes de estadistica_a1.py')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--trabajo', required=True)
    ap.add_argument('--sin', default='E17,E18')
    ap.add_argument('--solo', default='')
    a = ap.parse_args()
    sin = {s.strip() for s in a.sin.split(',') if s.strip()}
    solo = {s.strip() for s in a.solo.split(',') if s.strip()}
    with open(os.path.join(AQUI, 'estadistica_a1.py'), encoding='utf-8') as f:
        original = f.read()
    for mid, _, viejo, _ in MUTANTES:
        if original.count(viejo) != 1:
            print('ABORTA: el reemplazo de %s aparece %d veces' % (mid, original.count(viejo)), flush=True)
            raise SystemExit(2)
    print('MUTANTES inicio n=%d sin=%s' % (len(MUTANTES), ','.join(sorted(sin)) or '-'), flush=True)

    def copia(nombre, texto):
        d = os.path.join(a.trabajo, nombre)
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)
        for archivo in COPIAR:
            shutil.copy2(os.path.join(AQUI, archivo), os.path.join(d, archivo))
        with open(os.path.join(d, 'estadistica_a1.py'), 'w', encoding='utf-8') as f:
            f.write(texto)
        return d

    rc, caidas, final, dt = correr(copia('control', original), a, sin)
    print('CONTROL original exit=%d caidas=%s %s (%.1f s)' % (rc, ','.join(caidas) or '-', final, dt), flush=True)
    if rc != 0:
        print('ABORTA: la copia sin tocar no pasa, los mutantes no se pueden juzgar', flush=True)
        raise SystemExit(2)
    vivos = []
    for mid, desc, viejo, nuevo in MUTANTES:
        if solo and mid not in solo:
            continue
        rc, caidas, final, dt = correr(copia(mid, original.replace(viejo, nuevo)), a, sin)
        estado = 'MUERTO' if rc != 0 else 'VIVO'
        if estado == 'VIVO':
            vivos.append(mid)
        print('MUTANTE %s %s (%s) exit=%d caidas=%s %s (%.1f s)' % (mid, estado, desc, rc, ','.join(caidas) or '-',
                                                                     final, dt), flush=True)
    n = len([m for m in MUTANTES if not solo or m[0] in solo])
    print('MUTANTES muertos %d/%d vivos=%s' % (n - len(vivos), n, ','.join(vivos) or '-'), flush=True)
    raise SystemExit(0 if not vivos else 1)


if __name__ == '__main__':
    main()
