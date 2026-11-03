#!/usr/bin/env python3
"""prueba_estadistica_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-008).

Pruebas de estadistica_a1.py con datos sinteticos armados sobre la estructura del manifiesto real (sujetos, D',
drivers, celdas y condiciones). No abre ningun recibo de la corrida: cada ensayo sintetico sale de un generador con
semilla fija. Cada prueba lleva un control que tiene que dar rojo (un mutante, una variante o el caso opuesto) o lo
tiene en una prueba hermana (E07 frente a E08, E09, E13, E14 y E23); mutantes_estadistica_a1.py mide aparte cuantos
errores plausibles de estadistica_a1.py ve esta suite.
Uso: python3 prueba_estadistica_a1.py --manifiesto M --sha-manifiesto H [--solo E01,E07] [--tmp DIR]
Imprime una linea PRUEBA por prueba y al final PRUEBA_ESTADISTICA k/N PASS o FAIL. Exit 0 si pasan todas, 1 si alguna
falla, 2 si el manifiesto no es el esperado.
"""
import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
import time

import numpy as np
import scipy
from scipy import stats
from scipy.special import ndtr, ndtri

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import estadistica_a1 as E  # noqa: E402

C = E.C
N_ESC = 4000
TOL_BCA = 1e-9
BASE = {
    ('relevo', 'B'): {'lD': 12.0, 'lx': 30.0, 'lG': 50.0, 'd2': 6.0, 'r1': 0.75, 'c1': 1.0, 's4': 0.9, 'rw': 0.02},
    ('relevo', 'A'): {'lD': 8.0, 'lx': 30.0, 'lG': 20.0, 'd2': 4.0, 'r1': 0.75, 'c1': 1.0, 's4': 0.9, 'rw': 0.02},
    ('hub', 'B'): {'lD': 12.0, 'lx': 30.0, 'lG': 50.0, 'd2': 6.0, 'rc': 0.75, 'cc': 0.8, 'ri': 0.3},
    ('hub', 'C'): {'lC': 25.0, 'lCfull': 30.0, 'fc_cero': False, 'modo': 'OR'},
}
RESULTADOS = []


# ---------------------------------------------------------------- generador sintetico


def tabla_sintetica(man, cambios=None, semilla=7):
    """Tabla con la forma de E.tabla_vacia. Efecto de semilla compartido por todos los brazos de una celda (pareado),
    C0 Poisson y cada brazo derivado de C0 con incrementos Poisson en el D' y raleo binomial de x."""
    cambios = cambios or {}
    rng = np.random.Generator(np.random.PCG64(semilla))
    tabla = E.tabla_vacia(man)
    n = len(C.SEMILLAS_PLAN)

    def pois(lam, forma):
        return rng.poisson(lam, size=forma).astype(np.float64)

    def fino(x, f):
        return rng.binomial(x.astype(np.int64), min(max(float(f), 0.0), 1.0)).astype(np.float64)

    for c in man['celdas']:
        sid, reg = c['sujeto'], c['regimen']
        suj = man['sujetos'][sid]
        p = dict(BASE[(suj['clase'], reg)])
        p.update(cambios.get((sid, reg), {}))
        conds = tabla[(sid, reg)]['conds']
        nd, ng = len(suj['Dp']), len(suj['G'])
        u = rng.gamma(100.0, 0.01, size=n)
        uc = u[:, None]
        brazos = {}
        if reg == 'C':
            lleno = 'C_' + '1' * ng
            parciales = sorted(k for k in c['condiciones'] if k not in ('C_desplazado', lleno) and '1' in k[2:])
            for k in c['condiciones']:
                if k == 'C_desplazado':
                    continue
                on = k[2:].count('1')
                if p['modo'] == 'OR':
                    lam = 0.0 if on == 0 else (p['lCfull'] if on == ng else p['lC'])
                elif p['modo'] == 'AND':
                    lam = p['lCfull'] if on == ng else 0.5
                elif p['modo'] == 'IND':
                    lam = 0.0 if on == 0 else (p['lCfull'] if on == ng else (5.0 if k == parciales[0] else p['lC']))
                else:
                    lam = p['lC'] if on < ng else p['lCfull']
                gk = np.array([[50.0 if b == '1' else 0.0 for b in k[2:]]] * n)
                brazos[k] = (pois(1.0, (n, nd)), pois(lam * u, n), gk)
            hl = brazos[lleno][1]
            brazos['C_desplazado'] = (pois(1.0, (n, nd)), hl.copy() if p['fc_cero'] else fino(hl, 0.4),
                                      brazos[lleno][2].copy())
        else:
            D0 = pois(p['lD'] * uc, (n, nd))
            H0 = pois(p['lx'] * u, n)
            G0 = pois(p['lG'] * uc, (n, ng))

            def mas(f):
                return D0 + pois(f * p['d2'] * uc, (n, nd))

            brazos['C0'] = (D0, H0, G0)
            if suj['clase'] == 'relevo':
                hq1 = fino(H0, 1.0 - p['c1'])
                brazos['Q1'] = (mas(p['r1']), hq1, G0)
                brazos['Q2'] = (mas(1.0), H0.copy(), G0)
                brazos['Q3'] = (mas(0.8), np.zeros(n), G0)
                brazos['Q4'] = (mas(0.1), fino(H0, p['s4']), G0)
                brazos['QCOL'] = (mas(0.1), H0.copy(), G0)
                brazos['Q1uQCOL'] = (mas(p['r1'] + 0.12), hq1.copy(), G0)
                brazos['QXD'] = (mas(0.9), H0.copy(), G0)
                brazos['Q1uQXD'] = (mas(0.95), hq1.copy(), G0)
                brazos['QWEAK'] = (mas(p['rw']), H0.copy(), G0)
                brazos['SHAM'] = (D0.copy(), H0.copy(), G0.copy())
                if 'ZA' in c['condiciones']:
                    iz = suj['G'].index(suj['cascada_ZA'][1])
                    gz = G0.copy()
                    gz[:, iz] = gz[:, iz] + pois(0.5 * p['lG'] * u, n)
                    brazos['ZA'] = (fino(D0, 0.9), H0 + pois(0.3 * p['lx'] * u, n), gz)
                    brazos['ZAuQ1'] = (brazos['Q1'][0].copy(), hq1.copy(), gz.copy())
                    dza = (brazos['QCOL'][0] + pois(1.0 * uc, (n, nd)) if p.get('za3_contrario')
                           else fino(brazos['QCOL'][0], 0.9))
                    brazos['ZAuQCOL'] = (dza, H0 + pois(0.3 * p['lx'] * u, n), gz.copy())
                    brazos['ZAuQ1uQCOL'] = (brazos['Q1uQCOL'][0].copy(), hq1.copy(), gz.copy())
            else:
                brazos['Q2'] = (mas(1.0), H0.copy(), G0)
                brazos['Q4conj'] = (mas(0.1), fino(H0, 0.9), G0)
                brazos['Q1conj'] = (mas(p['rc']), fino(H0, 1.0 - p['cc']), G0)
                for i, g in enumerate(suj['G']):
                    brazos['Q1_%d' % g] = (mas(p['ri'] * (1.0 + 0.5 * i)), fino(H0, 0.7), G0)
        faltan, sobran = set(c['condiciones']) - set(brazos), set(brazos) - set(c['condiciones'])
        if faltan or sobran:
            raise SystemExit('ABORTA generador: %s|%s faltan %s sobran %s' % (sid, reg, sorted(faltan), sorted(sobran)))
        for k, (D, H, G) in brazos.items():
            e = conds[k]
            e['D'][:] = D
            e['Y'][:] = D.sum(axis=1)
            e['H'][:] = H
            e['G'][:] = G
    return tabla


def analizar(man, tabla, invalidas=(), motivos=None, n_boot=N_ESC, semilla=E.SEMILLA_BOOT, margenes=None):
    return E.analizar(man, tabla, set(invalidas), motivos or {}, n_boot, semilla, margenes)[0]


def todo(ctx):
    if 'res_todo' not in ctx:
        ctx['tabla_todo'] = tabla_sintetica(ctx['man'])
        ctx['res_todo'] = analizar(ctx['man'], ctx['tabla_todo'])
    return ctx['tabla_todo'], ctx['res_todo']


def filas(res, fam):
    return {f['id']: f for f in res['familias'][fam]['pruebas']}


def holm_ref(p):
    """Holm escrito aparte, en Python puro: p ajustado = maximo acumulado de (m - rango) * p ordenado, tope 1."""
    m = len(p)
    orden = sorted(range(m), key=lambda i: (p[i], i))
    adj, acum = [0.0] * m, 0.0
    for rango, i in enumerate(orden):
        acum = max(acum, min(1.0, (m - rango) * p[i]))
        adj[i] = acum
    return adj


def rechazos_secuenciales(p, alfa):
    """Regla de Holm como procedimiento: se rechaza en orden mientras p_(k) < alfa / (m - k)."""
    m = len(p)
    orden = sorted(range(m), key=lambda i: (p[i], i))
    out = set()
    for k, i in enumerate(orden):
        if p[i] < alfa / (m - k):
            out.add(i)
        else:
            break
    return out


def enumerar_signos(d, bilateral=True):
    n = d.size
    obs = abs(float(d.sum())) if bilateral else float(d.sum())
    tol = 1e-9 * (1.0 + float(np.abs(d).sum()))
    bits = np.arange(n)
    cuenta, paso = 0, 1 << 16
    for ini in range(0, 1 << n, paso):
        k = np.arange(ini, ini + paso, dtype=np.int64)
        s = ((((k[:, None] >> bits) & 1) * 2 - 1).astype(np.float64)) @ d
        cuenta += int(np.count_nonzero((np.abs(s) if bilateral else s) >= obs - tol))
    return cuenta


def recibos_desde_tabla(man, tabla, pos):
    """Recibos con el esquema del runner (solo los campos que lee la estadistica); las posiciones de mirar que no son
    D' llevan basura que depende de la condicion, para que leer la posicion equivocada cambie los estimandos."""
    regs = []
    for c in man['celdas']:
        sid, reg = c['sujeto'], c['regimen']
        suj = man['sujetos'][sid]
        nm = len(suj['mirar'])
        for ic, k in enumerate(c['condiciones']):
            e = tabla[(sid, reg)]['conds'][k]
            for si, s in enumerate(C.SEMILLAS_PLAN):
                cm = np.full(nm, 1000 + 37 * ic + int(s), dtype=np.int64)
                cm[pos[sid]] = e['D'][si].astype(np.int64)
                regs.append(('sintetico', {'subject_id': sid, 'regime': reg, 'condition': k, 'seed': int(s),
                                           'cuentas_mirar': [int(v) for v in cm],
                                           'cuentas_G': [int(v) for v in e['G'][si]], 'cuenta_x': int(e['H'][si])}))
    return regs


def tablas_iguales(a, b):
    for key, t in a.items():
        for k, e in t['conds'].items():
            f = b[key]['conds'][k]
            for campo in ('D', 'Y', 'H', 'G'):
                if not np.array_equal(e[campo], f[campo]):
                    return False
    return True


# ---------------------------------------------------------------- pruebas


def e01(ctx):
    g = np.random.Generator(np.random.PCG64(101))
    peor = 0.0
    for k in range(300):
        tipo = k % 3
        if tipo == 0:
            d = g.normal(0.3 * (k % 7 - 3), 1.0 + k % 5, 20)
        elif tipo == 1:
            d = g.lognormal(0.0, 1.0, 20) - 1.2
        else:
            d = g.poisson(3.0, 20) - 2.5
        t = E.t_unilateral(d)
        ref = stats.ttest_1samp(d, 0.0, alternative='greater')
        peor = max(peor, abs(t['p'] - float(ref.pvalue)), abs(t['t'] - float(ref.statistic)) / max(1.0, abs(ref.statistic)))
    cte = E.t_unilateral(np.full(20, 2.5))
    d = g.normal(0.4, 1.0, 20)
    uno = E.t_unilateral(d)['p']
    dos = float(stats.ttest_1samp(d, 0.0, alternative='two-sided').pvalue)
    neg = E.t_unilateral(-np.abs(g.normal(1.0, 0.3, 20)))['p']
    ok = peor < 1e-12 and cte['estado'] == 'VARIANZA_CERO' and cte['p'] is None and abs(uno - dos) > 1e-6 and neg > 0.99
    return ok, ('300 vectores, max dif contra scipy ttest_1samp(greater)=%.2e; constante -> %s p=%s; rojo: bilateral '
                'difiere en %.3e; media negativa p=%.6f' % (peor, cte['estado'], cte['p'], abs(uno - dos), neg))


def e02(ctx):
    g = np.random.Generator(np.random.PCG64(202))
    vec = [g.normal(0.2, 1.0, 20), g.normal(0.0, 1.0, 20), np.r_[np.zeros(3), g.normal(0.5, 1.0, 17)],
           g.integers(-3, 4, 20).astype(np.float64), g.lognormal(0.0, 1.0, 20) - 1.0, g.normal(1.0, 0.1, 20)]
    detalles, ok = [], True
    for d in vec:
        cuenta = enumerar_signos(d)
        p = E.signos_bilateral(d)
        bien = p * 2.0 ** 20 == cuenta
        ok &= bien
        detalles.append('%d/%d%s' % (cuenta, int(round(p * 2 ** 20)), '' if bien else '!'))
    piso = E.signos_bilateral(np.abs(g.normal(1.0, 0.2, 20)))
    ceros = E.signos_bilateral(np.zeros(20))
    uni = enumerar_signos(vec[1], bilateral=False)
    ok = ok and piso == 2.0 / 2 ** 20 and ceros == 1.0 and uni != enumerar_signos(vec[1])
    return ok, ('6 vectores contra la enumeracion directa de 2^20 signos (cuenta directa/cuenta implementada): %s; '
                'todos positivos p=%r (piso 2/2^20); todos cero p=%r; rojo: la cuenta unilateral da %d y difiere'
                % (' '.join(detalles), piso, ceros, uni))


def e03(ctx):
    g = np.random.Generator(np.random.PCG64(303))
    peor, malos = 0.0, 0
    for k in range(500):
        p = g.uniform(0, 1, 46) ** (1 + k % 6)
        if k % 5 == 0:
            p[:10] = 1.0
        if k % 7 == 0:
            p[5:9] = p[4]
        adj = E.holm(p)
        ref = holm_ref(list(p))
        peor = max(peor, float(np.max(np.abs(adj - np.array(ref)))))
        for alfa in (0.01, 0.05, float(g.uniform(0.001, 0.2))):
            if set(np.flatnonzero(adj < alfa)) != rechazos_secuenciales(list(p), alfa):
                malos += 1
    p = np.array([0.0001, 0.00022] + [0.9] * 44)
    holm_rech = int(np.sum(E.holm(p) < 0.01))
    bonf_rech = int(np.sum(np.minimum(1, 46 * p) < 0.01))
    ok = peor <= 1e-15 and malos == 0 and holm_rech == 2 and bonf_rech == 1
    return ok, ('500 vectores de 46 con empates y unos: max dif contra Holm aparte=%.1e, decisiones distintas de la regla '
                'secuencial=%d; rojo: en (0.0001, 0.00022, 44 x 0.9) Holm rechaza %d y Bonferroni %d'
                % (peor, malos, holm_rech, bonf_rech))


def bc_sin_aceleracion(theta, estrellas):
    b = estrellas.size
    p0 = (np.count_nonzero(estrellas < theta) + np.count_nonzero(estrellas <= theta)) / (2.0 * b)
    z0 = ndtri(p0)
    zs = ndtri(np.array([0.025, 0.975]))
    return np.quantile(estrellas, ndtr(2 * z0 + zs))


def _bootstrap(datos, f, metodo, semilla, pareado):
    kw = dict(n_resamples=20000, method=metodo, vectorized=True, paired=pareado, confidence_level=0.95)
    try:
        r = stats.bootstrap(datos, f, rng=np.random.Generator(np.random.PCG64(semilla)), **kw)
    except TypeError:
        r = stats.bootstrap(datos, f, random_state=np.random.Generator(np.random.PCG64(semilla)), **kw)
    return [float(r.confidence_interval.low), float(r.confidence_interval.high)]


def e04(ctx):
    g = np.random.Generator(np.random.PCG64(404))
    peor, pct_min, bc_min, n = 0.0, np.inf, np.inf, 0
    for caso in range(6):
        a = g.lognormal(0.0, 1.0, 20) * (1 + caso) + (0 if caso % 2 else g.normal(0, 0.5, 20))
        b = np.abs(a) * 0.5 + g.gamma(5.0, 1.0, 20)
        for tipo in ('media', 'cociente'):
            semilla = 4000 + 10 * caso + (tipo == 'cociente')
            idx = np.random.Generator(np.random.PCG64(semilla)).integers(0, 20, size=(20000, 20))
            if tipo == 'media':
                mio = E.evaluar(('media', a), idx)
                sc = _bootstrap((a,), np.mean, 'BCa', semilla, False)
                pc = _bootstrap((a,), np.mean, 'percentile', semilla, False)
                bc = bc_sin_aceleracion(float(a.mean()), a[idx].mean(axis=1))
            else:
                def f(x, y, axis=-1):
                    return x.mean(axis=axis) / y.mean(axis=axis)
                mio = E.evaluar(('cociente', a, b), idx)
                sc = _bootstrap((a, b), f, 'BCa', semilla, True)
                pc = _bootstrap((a, b), f, 'percentile', semilla, True)
                bc = bc_sin_aceleracion(float(a.mean() / b.mean()), a[idx].mean(axis=1) / b[idx].mean(axis=1))
            w = sc[1] - sc[0]
            peor = max(peor, max(abs(mio['ic95'][0] - sc[0]), abs(mio['ic95'][1] - sc[1])) / w)
            pct_min = min(pct_min, max(abs(mio['ic95'][0] - pc[0]), abs(mio['ic95'][1] - pc[1])) / w)
            bc_min = min(bc_min, max(abs(mio['ic95'][0] - bc[0]), abs(mio['ic95'][1] - bc[1])) / w)
            n += 1
    ok = peor <= TOL_BCA and pct_min > 1e-3 and bc_min > 1e-3
    return ok, ('%d intervalos (media y cociente pareado, 20.000 remuestreos, mismo flujo PCG64): max dif contra '
                'scipy.stats.bootstrap BCa=%.2e del ancho (tolerancia %.0e); rojo: percentil difiere al menos %.3f del '
                'ancho y BCa sin aceleracion al menos %.3f' % (n, peor, TOL_BCA, pct_min, bc_min))


def e05(ctx):
    g = np.random.Generator(np.random.PCG64(505))
    idx = np.random.Generator(np.random.PCG64(5)).integers(0, 20, size=(N_ESC, 20))
    r1 = E.evaluar(('cociente', np.ones(20), np.array([25.0] + [-1.0] * 19)), idx)
    r2 = E.evaluar(('cociente', np.ones(20), -np.ones(20)), idx)
    r3 = E.evaluar(('cociente', np.ones(20), np.zeros(20)), idx)
    r4 = E.evaluar(('media', np.full(20, 3.0)), idx)
    a = g.gamma(4.0, 1.0, 20)
    r5 = E.evaluar(('cociente', a, a.copy()), idx)
    r6 = E.evaluar(('cociente', g.gamma(4.0, 1.0, 20), g.gamma(4.0, 1.0, 20) + 1.0), idx)
    ok = (r1['estado_ic'] == 'INDEFINIDO' and abs(r1['estimado'] - 1 / 0.3) < 1e-12 and r1['ic95'] is None
          and r2['estado_ic'] == 'SIN_ESTIMADO' and r2['estimado'] is None and r3['estado_ic'] == 'SIN_ESTIMADO'
          and r4['estado_ic'] == 'DEGENERADO' and r4['estimado'] == 3.0 and r4['ic95'] is None
          and r5['estado_ic'] == 'DEGENERADO' and r5['estimado'] == 1.0 and r6['estado_ic'] == 'OK')
    return ok, ('denominador con media 0,3 y remuestreos negativos -> %s (estimado %.4f); denominador -1 -> %s; 0 -> %s; '
                'media constante -> %s; cociente a/a -> %s; control: cociente comun -> %s'
                % (r1['estado_ic'], r1['estimado'], r2['estado_ic'], r3['estado_ic'], r4['estado_ic'],
                   r5['estado_ic'], r6['estado_ic']))


def e06(ctx):
    man = ctx['man']
    fam = E.ids_familias()
    fb = fam['F_B']
    tabla = E.tabla_vacia(man)
    todas = {(c['sujeto'], c['regimen']) for c in man['celdas']}
    reg = E.registro(man, tabla_sintetica(man), set(), dict(E.MARGENES))
    nulo = E.registro(man, tabla, todas, dict(E.MARGENES))
    comp = (sum(1 for i in fb if i.endswith('|DQ2') and '|R' in i), sum(1 for i in fb if i.endswith('|DQ2') and '|H' in i),
            sum(1 for i in fb if '|T1' in i), sum(1 for i in fb if '|T2' in i))
    ok = (len(fb) == 46 and len(set(fb)) == 46 and comp == (16, 6, 6, 18) and len(fam['F_C']) == 6
          and len(fam['F_R01']) == 3 and all(i in reg for v in fam.values() for i in v)
          and set(reg) == set(nulo) and all(v is None for v in nulo.values()))
    man2 = copy.deepcopy(man)
    del man2['sujetos']['H3']
    man2['celdas'] = [c for c in man2['celdas'] if c['sujeto'] != 'H3']
    t2 = E.tabla_vacia(man2)
    try:
        E.familias(E.registro(man2, t2, {(c['sujeto'], c['regimen']) for c in man2['celdas']}, dict(E.MARGENES)))
        rojo = 'no aborto'
    except SystemExit as ex:
        rojo = str(ex)
    ok = ok and rojo.startswith('ABORTA')
    return ok, ('F_B=%d (relevos DQ2, hubs DQ2, T1, T2 = %s), F_C=%d, F_R01=%d; registro de %d ids, identico con celdas '
                'validas o invalidas=%s; rojo: sin H3 en el manifiesto -> %s'
                % (len(fb), comp, len(fam['F_C']), len(fam['F_R01']), len(reg), set(reg) == set(nulo), rojo[:60]))


def e07(ctx):
    tabla, res = todo(ctx)
    ver, casos, fam = res['veredictos'], res['casos'], res['familias']
    cb = [k for k in casos if k.startswith('B|')]
    ca = [k for k in casos if k.startswith('A|')]
    cx = [casos['%s|%s' % (g, r)]['cocientes']['c_X'] for r in E.RELEVOS for g in 'AB']
    chequeos = {
        'P_T1_B': ver['P_T1_B']['veredicto'] == 'SOSTENIDA' and all(v == 'PASA' for v in ver['P_T1_B']['casos'].values()),
        'P_T2_B': ver['P_T2_B']['veredicto'] == 'SOSTENIDA' and all(v == 'PASA' for v in ver['P_T2_B']['tipos'].values()),
        'F_C': len(ver['F_C']) == 6 and all(v == 'SOSTENIDA' for v in ver['F_C'].values()),
        'OR_en_C': all(casos['C|' + h]['transferencia'] == 'OR_COMPATIBLE_EN_C' for h in E.HUBS),
        'F_R01': ver['F_R01']['firma'] == 'SOSTENIDA' and all(ver['F_R01']['contrastes'].values()),
        'B_activados': len(cb) == 22 and all(casos[k]['estado'] == 'ACTIVADO' for k in cb),
        'A_reclutados': len(ca) == 16 and all(casos[k]['estado'] == 'RECLUTADO' for k in ca),
        'familias': (fam['F_B']['m'], fam['F_B']['n_deciden'], fam['F_C']['n_deciden'],
                     fam['F_R01']['n_deciden']) == (46, 46, 6, 3),
        'c_X_degenerado': all(q['estado_ic'] == 'DEGENERADO' and q['estimado'] == 1.0 for q in cx),
        'qweak_R11_B': casos['B|R11']['qweak']['banda'] == 'PEQUENO',
        'T3': len(ver['T3']) == 8 and all(v['r_Q1'] is not None for v in ver['T3'].values()),
        'json_estricto': len(json.dumps(res, allow_nan=False, sort_keys=True)) > 0,
        'sin_invalidas': res['invalidas'] == [],
    }
    malos = [k for k, v in chequeos.items() if not v]
    r = casos['B|R01']['cocientes']['r_Q1']
    s4 = casos['B|R01']['cocientes']['s4']
    t2 = casos['B|H1']['cocientes']['r_Q1conj']
    return not malos, ('escenario todo: %d/%d chequeos (fallan %s); B|R01 r_Q1=%.4f IC95=[%.4f; %.4f], s4=%.4f '
                       'IC95=[%.4f; %.4f]; B|H1 r_Q1conj=%.4f IC95=[%.4f; %.4f]'
                       % (len(chequeos) - len(malos), len(chequeos), malos or '-', r['estimado'], r['ic95'][0],
                          r['ic95'][1], s4['estimado'], s4['ic95'][0], s4['ic95'][1], t2['estimado'], t2['ic95'][0],
                          t2['ic95'][1]))


def e08(ctx):
    res = analizar(ctx['man'], tabla_sintetica(ctx['man'], {('R02', 'B'): {'r1': 0.20}}))
    cs = res['casos']['B|R02']
    r = cs['cocientes']['r_Q1']
    v = res['veredictos']['P_T1_B']
    ok = (cs['estado'] == 'ACTIVADO' and cs['T1']['estado'] == 'NO_PASA:SIN_DECIDIR' and r['intervalo_contradice']
          and not cs['T1']['criterios']['T1a_F_B'] and v['veredicto'] == 'SIN_DECIDIR'
          and v['casos']['R01'] == 'PASA' and v['casos']['R03'] == 'PASA')
    return ok, ('R02 con r1=0,20: r_Q1=%.4f IC95=[%.4f; %.4f] contradice el margen 0,35=%s; T1=%s; P_T1_B=%s'
                % (r['estimado'], r['ic95'][0], r['ic95'][1], r['intervalo_contradice'], cs['T1']['estado'],
                   v['veredicto']))


def e09(ctx):
    res = analizar(ctx['man'], tabla_sintetica(ctx['man'], {('R03', 'B'): {'lG': 4.0}}))
    cs = res['casos']['B|R03']
    r = cs['cocientes']['r_Q1']
    f = filas(res, 'F_B')['B|R03|T1a']
    ok = (cs['estado'] == 'NO_INFORMATIVO_EN_B' and cs['activacion']['causas'] == ['drivers_C0_ge_10Hz']
          and r['estimado'] is None and r['estado_ic'] == 'NULO' and r['estado_ic_calculado'] == 'OK'
          and r['numerador'] is not None and r['denominador'] is not None and 'NO_INFORMATIVO_EN_B' in r['motivo']
          and cs['T1']['estado'] == 'NO_PASA:NO_INFORMATIVO_EN_B'
          and res['veredictos']['P_T1_B']['veredicto'] == 'NO_INFORMATIVO_EN_B' and f['p_observado'] is not None)
    return ok, ('R03 con driver a 4 Hz: %s por %s; r_Q1 null (num=%.2f, den=%.2f, motivo "%s"); T1=%s; P_T1_B=%s; '
                'T1a conserva p observado=%s (D1)'
                % (cs['estado'], cs['activacion']['causas'], r['numerador'], r['denominador'], r['motivo'],
                   cs['T1']['estado'], res['veredictos']['P_T1_B']['veredicto'], f['p_observado'] is not None))


def e10(ctx):
    man = ctx['man']
    tabla, rt = todo(ctx)
    inval = {('H2', 'B')}
    res = analizar(man, tabla, inval, {('H2', 'B'): ['PRUEBA invalidada a mano']})
    fb = res['familias']['F_B']
    fl = {f['id']: f for f in fb['pruebas']}
    ids_inv = ['B|H2|DQ2', 'B|H2|T2a', 'B|H2|T2b', 'B|H2|T2c']
    c1 = all(fl[i]['estado'] == 'INVALIDO_TECNICO' and fl[i]['p_familia'] == 1.0 and fl[i]['p_observado'] is None
             for i in ids_inv)
    ref = holm_ref([f['p_familia'] for f in fb['pruebas']])
    c2 = fb['m'] == 46 and len(fb['pruebas']) == 46 and all(abs(f['p_holm'] - h) <= 1e-15
                                                            for f, h in zip(fb['pruebas'], ref))
    v = res['veredictos']['P_T2_B']
    c3 = v['veredicto'] == 'SOSTENIDA' and v['tipos']['CB0534'] == 'BLOQUEADO' and res['casos']['B|H2']['estado'] == \
        'INVALIDO_TECNICO'
    c4 = res['intervalos']['B|R01|DQ2'] == rt['intervalos']['B|R01|DQ2']
    cant = E.registro(man, tabla, inval, dict(E.MARGENES))
    ids = sorted(cant)
    k = ids.index('B|R01|DQ2')
    rng = np.random.Generator(np.random.PCG64(E.SEMILLA_BOOT))
    for _ in range(k):
        rng.integers(0, 20, size=(N_ESC, 20))
    directo = E.evaluar(cant['B|R01|DQ2'], rng.integers(0, 20, size=(N_ESC, 20)))
    c5 = directo['ic95'] == res['intervalos']['B|R01|DQ2']['ic95']
    rng = np.random.Generator(np.random.PCG64(E.SEMILLA_BOOT))
    mut = None
    for qid in ids:
        if cant[qid] is None:
            continue
        idx = rng.integers(0, 20, size=(N_ESC, 20))
        if qid == 'B|R01|DQ2':
            mut = E.evaluar(cant[qid], idx)
            break
    c6 = mut['ic95'] != directo['ic95']
    ok = c1 and c2 and c3 and c4 and c5 and c6
    return ok, ('H2 de B invalida: 4 posiciones con p_familia 1 y m=%d (%s); Holm recalculado igual al Holm aparte=%s; '
                'P_T2_B=%s con CB0534 %s; IC de B|R01|DQ2 igual al escenario todo=%s y al flujo reconstruido a mano=%s; '
                'rojo: un flujo que salta los ids invalidos da [%.4f; %.4f] en vez de [%.4f; %.4f]'
                % (fb['m'], c1, c2, v['veredicto'], v['tipos']['CB0534'], c4, c5, mut['ic95'][0], mut['ic95'][1],
                   directo['ic95'][0], directo['ic95'][1]))


def e11(ctx):
    res = analizar(ctx['man'], tabla_sintetica(ctx['man'], {('H3', 'B'): {'rc': 0.1}}), {('H2', 'B')})
    v = res['veredictos']['P_T2_B']
    ok = (v['tipos']['CB0534'] == 'BLOQUEADO' and v['tipos']['CB0172'] == 'NO_PASA:SIN_DECIDIR'
          and v['veredicto'] == 'INVALIDO_TECNICO')
    return ok, 'H2 invalida y H3 con rc=0,1: tipos=%s -> P_T2_B=%s' % (json.dumps(v['tipos'], sort_keys=True),
                                                                        v['veredicto'])


def e12(ctx):
    res = analizar(ctx['man'], tabla_sintetica(ctx['man'], {('H4', 'C'): {'fc_cero': True}}))
    f = filas(res, 'F_C')['C|H4|FC']
    fc = res['veredictos']['F_C']
    ok = (f['estado'] == 'VARIANZA_CERO' and f['p_observado'] is None and f['p_familia'] == 1.0
          and f['signos_bilateral'] == 1.0 and not f['decide'] and res['intervalos']['C|H4|FC']['estado_ic'] == 'DEGENERADO'
          and fc['H4'] == 'SIN_DECIDIR' and sum(1 for h, e in fc.items() if h != 'H4' and e == 'SOSTENIDA') == 5)
    return ok, ('H4 en C con desplazado identico al sincronizado: %s, p_observado=%s, p_familia=%s, signos=%s, IC %s; '
                'F_C=%s' % (f['estado'], f['p_observado'], f['p_familia'], f['signos_bilateral'],
                            res['intervalos']['C|H4|FC']['estado_ic'], json.dumps(fc, sort_keys=True)))


def e13(ctx):
    r1 = analizar(ctx['man'], tabla_sintetica(ctx['man'], {('H1b', 'B'): {'rc': 0.1}}))
    r2 = analizar(ctx['man'], tabla_sintetica(ctx['man'], {('H1b', 'B'): {'rc': 0.1}, ('H4', 'B'): {'rc': 0.1}}))
    v1, v2 = r1['veredictos']['P_T2_B'], r2['veredictos']['P_T2_B']
    ok = (v1['veredicto'] == 'SOSTENIDA' and v1['instancias']['H1'] == 'PASA'
          and v1['instancias']['H1b'] == 'NO_PASA:SIN_DECIDIR' and v1['tipos']['CB0580'] == 'NO_PASA:SIN_DECIDIR'
          and v2['veredicto'] == 'SIN_DECIDIR' and v2['tipos']['PS100'] == 'NO_PASA:SIN_DECIDIR')
    return ok, ('H1b con rc=0,1: CB0580 %s aunque H1 %s, P_T2_B=%s (3 de 4 tipos); H1b y H4 con rc=0,1: P_T2_B=%s'
                % (v1['tipos']['CB0580'], v1['instancias']['H1'], v1['veredicto'], v2['veredicto']))


def e14(ctx):
    tabla, _ = todo(ctx)
    m = dict(E.MARGENES)
    m['T1_r'] = 0.80
    res = analizar(ctx['man'], tabla, margenes=m)
    v = res['veredictos']
    r = res['casos']['B|R01']['cocientes']['r_Q1']
    ok = (v['P_T1_B']['veredicto'] == 'SIN_DECIDIR'
          and all(e == 'NO_PASA:SIN_DECIDIR' for e in v['P_T1_B']['casos'].values())
          and not res['casos']['B|R01']['T1']['criterios']['T1a_F_B'] and r['margen'] == 0.8
          and not r['limite_inferior_supera_margen'] and res['parametros']['margenes']['T1_r'] == 0.8
          and v['P_T2_B']['veredicto'] == 'SOSTENIDA')
    return ok, ('margen T1 de 0,80 sobre r1=0,75: P_T1_B=%s, r_Q1 IC95=[%.4f; %.4f] con margen %s; P_T2_B sigue %s'
                % (v['P_T1_B']['veredicto'], r['ic95'][0], r['ic95'][1], r['margen'], v['P_T2_B']['veredicto']))


def e15(ctx):
    tabla = tabla_sintetica(ctx['man'], {('R05', 'A'): {'d2': 0.0}, ('R06', 'A'): {'lx': 0.0}})
    fijar_freno(tabla, ('R07', 'A'), [-6, -8] * 10)
    res = analizar(ctx['man'], tabla)
    a5, a6, a7 = res['casos']['A|R05'], res['casos']['A|R06'], res['casos']['A|R07']
    q5, q6, q7 = a5['cocientes'], a6['cocientes'], a7['cocientes']
    ok7 = (a7['estado'] == 'NO_RECLUTADO_EN_A' and a7['activacion']['causas'] == ['DQ2_ge_5Hz']
           and a7['activacion']['criterios']['IC95_DQ2_excluye_0'] and q7['r_Q1']['estado_ic'] == 'SIN_ESTIMADO'
           and q7['r_Q1']['estimado'] is None and q7['s4']['estimado'] is not None)
    ok5 = (a5['estado'] == 'NO_RECLUTADO_EN_A' and 'DQ2_ge_5Hz' in a5['activacion']['causas']
           and 'IC95_DQ2_excluye_0' in a5['activacion']['causas'] and q5['r_Q1']['estimado'] is None
           and q5['r_Q1']['estado_ic'] == 'NULO' and q5['r_Q1']['estado_ic_calculado'] == 'SIN_ESTIMADO'
           and q5['r_weak']['estado_ic'] == 'NULO' and q5['s4']['estimado'] is not None and q5['s4']['estado_ic'] == 'OK'
           and q5['c_X']['estimado'] == 1.0)
    ok6 = (a6['estado'] == 'NO_RECLUTADO_EN_A' and 'x_C0_ge_10Hz' in a6['activacion']['causas']
           and q6['r_Q1']['estimado'] is not None and q6['c_X']['estimado'] is None and q6['s4']['estimado'] is None
           and q6['s4']['estado_ic_calculado'] == 'SIN_ESTIMADO' and 'H(C0)' in q6['s4']['motivo'])
    ok = ok5 and ok6 and ok7 and res['casos']['B|R05']['estado'] == 'ACTIVADO'
    return ok, ('A|R05 sin freno: %s, r_Q1 null (calculado %s), s4 publicado=%.4f; A|R06 con x mudo: %s, r_Q1 '
                'publicado=%.4f, s4 null (calculado %s, motivo "%s"); A|R07 con freno negativo de -7 Hz: %s, r_Q1 %s '
                'por denominador negativo y no por el IC; B|R05 sigue %s'
                % (a5['estado'], q5['r_Q1']['estado_ic_calculado'], q5['s4']['estimado'], a6['estado'],
                   q6['r_Q1']['estimado'], q6['s4']['estado_ic_calculado'], q6['s4']['motivo'], a7['estado'],
                   q7['r_Q1']['estado_ic'], res['casos']['B|R05']['estado']))


def e16(ctx):
    man, sha = ctx['man'], ctx['sha']
    tabla, rt = todo(ctx)
    pos = E.posiciones(man)
    extras = sum(1 for s in man['sujetos'].values() if len(s['mirar']) > len(s['Dp']))
    regs = recibos_desde_tabla(man, tabla, pos)
    ok_val = {'estado': 'OK', 'n_registros': len(regs), 'n_esperados': len(regs), 'n_fallos': 0, 'fallos': []}
    t_ext = E.extraer(man, regs)
    c1 = tablas_iguales(tabla, t_ext) and all(not t['problemas'] for t in t_ext.values())
    rc, _ = E.correr(man, sha, regs, ok_val, n_boot=N_ESC)
    claves = ('casos', 'familias', 'veredictos', 'intervalos', 'invalidas', 'parametros')
    c2 = all(json.dumps(rc[k], sort_keys=True) == json.dumps(rt[k], sort_keys=True) for k in claves)
    original = E.posiciones
    E.posiciones = lambda m: {s: (v + 1) % len(m['sujetos'][s]['mirar']) for s, v in original(m).items()}
    try:
        t_mut = E.extraer(man, regs)
    finally:
        E.posiciones = original
    cambian = sum(1 for key, t in t_mut.items()
                  if any(not np.array_equal(e['Y'], tabla[key]['conds'][k]['Y']) for k, e in t['conds'].items()))
    d_ok = float(np.mean(tabla[('R05', 'B')]['conds']['Q2']['Y'] - tabla[('R05', 'B')]['conds']['C0']['Y']))
    d_mut = float(np.mean(t_mut[('R05', 'B')]['conds']['Q2']['Y'] - t_mut[('R05', 'B')]['conds']['C0']['Y']))
    c3 = cambian == len(tabla) and abs(d_mut - d_ok) > 1.0
    inv_m, _ = E.celdas_invalidas({'estado': 'FALLA', 'fallos': [{'codigo': 'MASCARA', 'detalle': 'R05|A|Q2|3'}]}, t_ext)
    inv_s, _ = E.celdas_invalidas({'estado': 'FALLA', 'fallos': [{'codigo': 'SHAM_DISTINTO_DE_C0',
                                                                 'detalle': 'R09|B|7'}]}, t_ext)
    inv_i, mot_i = E.celdas_invalidas({'estado': 'FALLA', 'fallos': [{'codigo': 'ILEGIBLE',
                                                                     'detalle': 'bloque_03.jsonl:17'}]}, t_ext)
    inv_c, _ = E.celdas_invalidas({'estado': 'FALLA', 'fallos': [{'codigo': 'CODE_COMMIT_MIXTO',
                                                                 'detalle': ['a', 'b']}]}, t_ext)
    inv_v, _ = E.celdas_invalidas({'estado': 'FALLA', 'fallos': []}, t_ext)
    c4 = (inv_m == {('R05', 'A')} and inv_s == {('R09', 'B')} and len(inv_i) == len(tabla) == len(inv_c) == len(inv_v))
    quitar = ('R07', 'B', 'QCOL', 5)
    sin_uno = [r for r in regs if (r[1]['subject_id'], r[1]['regime'], r[1]['condition'], r[1]['seed']) != quitar]
    t_falta = E.extraer(man, sin_uno)
    inv_f, mot_f = E.celdas_invalidas(ok_val, t_falta)
    t_dup = E.extraer(man, regs + [regs[123]])
    inv_d, mot_d = E.celdas_invalidas(ok_val, t_dup)
    k_lect = next(i for i, r in enumerate(regs) if r[1]['subject_id'] == 'H4' and r[1]['regime'] == 'B')
    malo = dict(regs[k_lect][1])
    malo['cuentas_mirar'] = malo['cuentas_mirar'][:-1]
    lect = list(regs)
    lect[k_lect] = ('sintetico', malo)
    inv_l, mot_l = E.celdas_invalidas(ok_val, E.extraer(man, lect))
    humo = dict(regs[0][1])
    humo['seed'] = 900
    t_humo = E.extraer(man, regs + [('humo', humo)])
    c5 = (inv_f == {('R07', 'B')} and any(m.startswith('INCOMPLETO R07|B|QCOL') for m in mot_f[('R07', 'B')])
          and len(inv_d) == 1 and any(m.startswith('REPETIDO') for v in mot_d.values() for m in v)
          and inv_l == {('H4', 'B')} and any(m.startswith('LECTURA') for m in mot_l[('H4', 'B')])
          and tablas_iguales(tabla, t_humo) and all(not t['problemas'] for t in t_humo.values()))
    ri = analizar(man, tabla, inv_i, mot_i)
    vi = ri['veredictos']
    c6 = (vi['P_T1_B']['veredicto'] == 'INVALIDO_TECNICO' and vi['P_T2_B']['veredicto'] == 'INVALIDO_TECNICO'
          and all(e == 'INVALIDO_TECNICO' for e in vi['F_C'].values()) and vi['F_R01']['firma'] == 'INVALIDO_TECNICO'
          and all(f['estado'] == 'INVALIDO_TECNICO' and f['p_familia'] == 1.0 and not f['decide']
                  for fam in ri['familias'].values() for f in fam['pruebas']))
    ok = c1 and c2 and c3 and c4 and c5 and c6 and extras == len(man['sujetos'])
    return ok, ('%d recibos sinteticos con basura fuera del D en los %d sujetos: tabla reconstruida identica=%s; agregado '
                'por recibos identico al directo=%s; rojo: leer las posiciones corridas en uno cambia %d/%d celdas y '
                'DQ2 de B|R05 pasa de %.2f a %.2f Hz; mapeo de fallas (celda, SHAM, ilegible, commit mixto, validacion '
                'sin detalle)=%s; faltante, repetido, ilegible y semilla de humo=%s; todo invalido bloquea los cuatro '
                'veredictos=%s' % (len(regs), extras, c1, c2, cambian, len(tabla), d_ok, d_mut, c4, c5, c6))


def e17(ctx):
    man = ctx['man']
    tabla, _ = todo(ctx)
    t0 = time.time()
    ra = analizar(man, tabla, n_boot=E.N_BOOT)
    ta = time.time() - t0
    rb = analizar(man, tabla, n_boot=E.N_BOOT)
    rc = analizar(man, tabla, n_boot=E.N_BOOT, semilla=E.SEMILLA_BOOT + 1)
    sa, sb = json.dumps(ra, sort_keys=True), json.dumps(rb, sort_keys=True)
    distintos = sum(1 for k, v in ra['intervalos'].items() if v is not None and v.get('ic95') != rc['intervalos'][k].get('ic95'))
    consts = (E.N_BOOT, E.SEMILLA_BOOT, E.ALFA, E.NIVEL, E.MARGENES)
    ok = (sa == sb and distintos > 0 and consts == (20000, 2026110209, 0.01, 0.95,
                                                    {'T1_r': 0.35, 'T1_s4': 0.50, 'T2_r': 0.40, 'T2_caida': 0.40})
          and ra['parametros']['n_boot'] == 20000 and ra['veredictos'] == rb['veredictos'])
    import hashlib
    return ok, ('20.000 remuestreos dos veces: agregado identico=%s (sha256 %s, %.1f s por corrida); con semilla '
                '2026110210 cambian %d intervalos; constantes %s'
                % (sa == sb, hashlib.sha256(sa.encode()).hexdigest()[:16], ta, distintos, consts))


def e18(ctx):
    est = os.path.abspath(E.__file__)
    base = tempfile.mkdtemp(prefix='prueba_cli_', dir=ctx['tmp'])
    vacio = os.path.join(base, 'nada', '*.jsonl')

    def correr(args, salida):
        cmd = [sys.executable, est, '--manifiesto', ctx['manifiesto'], '--jsonl', vacio, '--salida', salida] + args
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        return p.returncode, (p.stdout + p.stderr).strip().splitlines()

    sa, sb, sc = (os.path.join(base, x) for x in ('sin_sobre', 'sha_mala', 'vacio'))
    ra, la = correr(['--sha-manifiesto', ctx['sha']], sa)
    rb, lb = correr(['--sha-manifiesto', 'f' * 64, '--abrir-sobre'], sb)
    rc, lc = correr(['--sha-manifiesto', ctx['sha'], '--abrir-sobre'], sc)
    agregado = os.path.join(sc, 'agregado_a1.json')
    okc = False
    det_c = 'sin agregado'
    if os.path.exists(agregado):
        with open(agregado, encoding='utf-8') as f:
            res = json.load(f)
        with open(os.path.join(sc, 'tasas_por_neurona.csv'), encoding='utf-8') as f:
            csv = f.read().splitlines()
        with open(os.path.join(sc, 'estadistica_a1.log'), encoding='utf-8') as f:
            log = f.read().splitlines()
        okc = (rc == 1 and len(res['invalidas']) == len(ctx['man']['celdas']) and res['validacion']['estado'] != 'OK'
               and log[0].startswith('ESTADISTICA_A1') and len(csv) == 1 and res['manifiesto_sha256'] == ctx['sha']
               and len(res['codigo_sha256']) == 64)
        det_c = 'exit %d, %d celdas invalidas, validacion %s, %d lineas de log, csv %d linea' % (
            rc, len(res['invalidas']), res['validacion']['estado'], len(log), len(csv))
    ok = ra == 2 and not os.path.exists(sa) and rb == 2 and not os.path.exists(sb) and okc
    return ok, ('sin --abrir-sobre: exit %d, salida creada=%s ("%s"); sha equivocado: exit %d, salida creada=%s; sin '
                'recibos y con el sobre abierto: %s' % (ra, os.path.exists(sa), (la or [''])[-1][:70], rb,
                                                        os.path.exists(sb), det_c))


def e19(ctx):
    cambios = {('H2', 'C'): {'modo': 'AND'}, ('H3', 'C'): {'modo': 'IND'}, ('H4b', 'C'): {'modo': 'OTRA'},
               ('R11', 'B'): {'rw': 0.07}, ('R12', 'B'): {'rw': 0.3}}
    res = analizar(ctx['man'], tabla_sintetica(ctx['man'], cambios))
    tr = {h: res['casos']['C|' + h]['transferencia'] for h in E.HUBS}
    esperado = {'H1': 'OR_COMPATIBLE_EN_C', 'H1b': 'OR_COMPATIBLE_EN_C', 'H2': 'AND_COMPATIBLE_EN_C',
                'H3': 'INDETERMINADO', 'H4': 'OR_COMPATIBLE_EN_C', 'H4b': 'OTRA_TRANSFERENCIA'}
    bandas = [(0.0, 'PEQUENO'), (0.0499, 'PEQUENO'), (-0.0499, 'PEQUENO'), (0.05, 'INTERMEDIO'), (0.0999, 'INTERMEDIO'),
              (-0.07, 'INTERMEDIO'), (0.10, 'ALTO'), (-0.2, 'ALTO')]
    ok_b = all(E.banda_weak(x) == e for x, e in bandas)
    q11, q12 = res['casos']['B|R11']['qweak']['banda'], res['casos']['B|R12']['qweak']['banda']
    ind = [k for k, v in res['casos']['C|H3']['tabla_ON_OFF'].items() if v['etiqueta'] == 'IND']
    ok = tr == esperado and ok_b and q11 == 'INTERMEDIO' and q12 == 'ALTO' and len(ind) == 1
    return ok, ('transferencias en C=%s; bandas QWEAK en los bordes=%s; R11 con rw=0,07 -> %s; R12 con rw=0,3 -> %s; H3 '
                'con %s indeterminado' % (json.dumps(tr, sort_keys=True), ok_b, q11, q12, ind))


FRENO_CHICO = [-13, -11, -7, -5, -3, -1, 2, 3, 5, 6, 8, 9, 11, 12, 15, 17, 19, 21, 25, 27]


def fijar_freno(tabla, key, delta):
    """Q2 copia el D' de C0; la neurona 0 queda en 30 espigas en todas las condiciones y en Q2 suma delta, asi que
    DQ2 por semilla es exactamente delta."""
    conds = tabla[key]['conds']
    conds['Q2']['D'][:] = conds['C0']['D']
    for k, e in conds.items():
        e['D'][:, 0] = 30.0 + (np.asarray(delta, dtype=np.float64) if k == 'Q2' else 0.0)
        e['Y'][:] = e['D'].sum(axis=1)


def e20(ctx):
    man = ctx['man']
    p_crudo = float(stats.ttest_1samp(FRENO_CHICO, 0.0, alternative='greater').pvalue)
    uno = tabla_sintetica(man)
    fijar_freno(uno, ('R04', 'B'), FRENO_CHICO)
    ra = analizar(man, uno)
    dos = tabla_sintetica(man)
    fijar_freno(dos, ('R04', 'B'), FRENO_CHICO)
    fijar_freno(dos, ('R10', 'B'), FRENO_CHICO)
    rb = analizar(man, dos)
    fa, fb = filas(ra, 'F_B'), filas(rb, 'F_B')
    ok_a = ra['casos']['B|R04']['estado'] == 'ACTIVADO' and fa['B|R04|DQ2']['p_holm'] < 0.01
    ok_b = all(rb['casos']['B|' + r]['estado'] == 'NO_INFORMATIVO_EN_B'
               and rb['casos']['B|' + r]['activacion']['causas'] == ['DQ2_F_B_holm_lt_001']
               and fb['B|%s|DQ2' % r]['p_observado'] < 0.01 <= fb['B|%s|DQ2' % r]['p_holm'] for r in ('R04', 'R10'))
    ok = 0.005 < p_crudo < 0.01 and ok_a and ok_b
    ic = rb['casos']['B|R04']['activacion']['medido']['IC95_DQ2']
    return ok, ('freno chico de media 7 Hz con p crudo %.5f: solo en R04 -> %s (Holm %.5f); en R04 y R10 -> %s y %s, '
                'causa unica %s, IC95 de DQ2=[%.2f; %.2f], Holm %.5f' % (
                    p_crudo, ra['casos']['B|R04']['estado'], fa['B|R04|DQ2']['p_holm'],
                    rb['casos']['B|R04']['estado'], rb['casos']['B|R10']['estado'],
                    rb['casos']['B|R04']['activacion']['causas'], ic[0], ic[1], fb['B|R04|DQ2']['p_holm']))


def e21(ctx):
    """Estimandos escritos aparte desde el texto de 010 secciones 5 a 7, sin usar las funciones de estadistica_a1."""
    man = ctx['man']
    tabla, rt = todo(ctx)
    dur = C.NTICKS * C.DT_S
    iv = rt['intervalos']

    def Y(key, k):
        return tabla[key]['conds'][k]['Y'] / dur

    def H(key, k):
        return tabla[key]['conds'][k]['H'] / dur

    b, a, h, c = ('R01', 'B'), ('R01', 'A'), ('H1', 'B'), ('H1', 'C')
    iz = man['sujetos']['R01']['G'].index(man['sujetos']['R01']['cascada_ZA'][1])
    q1i = [Y(h, 'Q1_%d' % g) for g in man['sujetos']['H1']['G']]
    esperado = {
        'B|R01|DQ1': np.mean(Y(b, 'Q1') - Y(b, 'C0')),
        'B|R01|r_Q1': np.mean(Y(b, 'Q1') - Y(b, 'C0')) / np.mean(Y(b, 'Q2') - Y(b, 'C0')),
        'B|R01|c_X': (np.mean(H(b, 'C0')) - np.mean(H(b, 'Q1'))) / np.mean(H(b, 'C0')),
        'B|R01|s4': np.mean(H(b, 'Q4')) / np.mean(H(b, 'C0')),
        'B|R01|r_weak': np.mean(Y(b, 'QWEAK') - Y(b, 'C0')) / np.mean(Y(b, 'Q2') - Y(b, 'C0')),
        'B|R01|COL_cortado': np.mean(Y(b, 'Q1uQCOL') - Y(b, 'Q1')),
        'B|R01|COL_interaccion': np.mean(Y(b, 'Q1uQCOL') - Y(b, 'Q1')) - np.mean(Y(b, 'QCOL') - Y(b, 'C0')),
        'B|R01|XD_q1': np.mean(Y(b, 'Q1uQXD') - Y(b, 'QXD')),
        'B|R01|XD_dif': np.mean(Y(b, 'Q1uQXD') - Y(b, 'QXD')) - np.mean(Y(b, 'Q1') - Y(b, 'C0')),
        'B|R01|Q1_menos_Q3': np.mean(Y(b, 'Q1') - Y(b, 'Q3')),
        'B|R01|T1a': np.mean((Y(b, 'Q1') - Y(b, 'C0')) - 0.35 * (Y(b, 'Q2') - Y(b, 'C0'))),
        'B|R01|T1b': np.mean(H(b, 'Q4') - 0.50 * H(b, 'C0')),
        'A|R01|ZA1': np.mean(tabla[a]['conds']['ZA']['G'][:, iz] - tabla[a]['conds']['C0']['G'][:, iz]) / dur,
        'A|R01|ZA2': np.mean((H(a, 'ZA') - H(a, 'C0')) - (H(a, 'ZAuQ1') - H(a, 'Q1'))),
        'A|R01|ZA3': np.mean((Y(a, 'ZAuQ1uQCOL') - Y(a, 'Q1uQCOL')) - (Y(a, 'ZAuQCOL') - Y(a, 'QCOL'))),
        'B|H1|DQ1conj': np.mean(Y(h, 'Q1conj') - Y(h, 'C0')),
        'B|H1|r_Q1conj': np.mean(Y(h, 'Q1conj') - Y(h, 'C0')) / np.mean(Y(h, 'Q2') - Y(h, 'C0')),
        'B|H1|c_Xconj': (np.mean(H(h, 'C0')) - np.mean(H(h, 'Q1conj'))) / np.mean(H(h, 'C0')),
        'B|H1|s4conj': np.mean(H(h, 'Q4conj')) / np.mean(H(h, 'C0')),
        'B|H1|T2a': np.mean((Y(h, 'Q1conj') - Y(h, 'C0')) - 0.40 * (Y(h, 'Q2') - Y(h, 'C0'))),
        'B|H1|T2b': np.mean((H(h, 'C0') - H(h, 'Q1conj')) - 0.40 * H(h, 'C0')),
        'B|H1|T2c': np.mean(Y(h, 'Q1conj') - np.mean(q1i, axis=0)),
        'C|H1|FC': np.mean(H(c, 'C_111') - H(c, 'C_desplazado')),
    }
    peor, malos = 0.0, []
    for k, v in esperado.items():
        got = iv[k]['estimado']
        dif = abs(got - float(v)) / max(1.0, abs(float(v)))
        peor = max(peor, dif)
        if dif > 1e-12:
            malos.append(k)
    _, tasas = E.analizar(man, tabla, set(), {}, 200, E.SEMILLA_BOOT, None)
    j0 = man['sujetos']['R01']['Dp'][0]
    tasa = [t for t in tasas if t[:4] == ('B', 'R01', 'C0', j0)]
    tasa_ok = len(tasa) == 1 and abs(tasa[0][4] - float(np.mean(tabla[b]['conds']['C0']['D'][:, 0])) / dur) < 1e-12
    tn = np.mean(tabla[b]['conds']['C0']['D'], axis=0) / dur
    fr = rt['casos']['B|R01']['fracciones']
    fr_ok = fr['frac_C0_le_2Hz'] == float(np.mean(tn <= 2.0)) and fr['frac_C0_gt_10Hz'] == float(np.mean(tn > 10.0))
    t2c_max = float(np.mean(Y(h, 'Q1conj') - np.max(q1i, axis=0)))
    rojo = abs(t2c_max - iv['B|H1|T2c']['estimado']) > 1.0
    ok = not malos and tasa_ok and fr_ok and rojo and len(tasas) == sum(
        len(c_['condiciones']) * len(man['sujetos'][c_['sujeto']]['Dp']) for c_ in man['celdas'])
    return ok, ('%d estimandos recalculados aparte desde 010: max dif relativa=%.1e (fallan %s); tasa por neurona y '
                'fracciones C0 iguales=%s; rojo: T2c con el maximo de los cortes individuales daria %.2f y no %.2f'
                % (len(esperado), peor, malos or '-', tasa_ok and fr_ok, t2c_max, iv['B|H1|T2c']['estimado']))


def e22(ctx):
    """Bordes de 010: drivers y x >= 10 Hz, DQ2 >= 5 Hz, ON >= 10 Hz y OFF <= 2 Hz, justo en el umbral."""
    man = ctx['man']
    tabla = tabla_sintetica(man)
    c0 = tabla[('R13', 'B')]['conds']['C0']
    c0['G'][:] = 10.0
    c0['H'][:] = 10.0
    fijar_freno(tabla, ('R14', 'B'), [4, 6] * 10)
    cc = tabla[('H1b', 'C')]['conds']
    cc['C_10']['H'][:] = 10.0
    cc['C_01']['H'][:] = 2.0
    res = analizar(man, tabla)
    r13, r14 = res['casos']['B|R13'], res['casos']['B|R14']
    t = res['casos']['C|H1b']['tabla_ON_OFF']
    ok = (r13['estado'] == 'ACTIVADO' and r13['activacion']['medido']['drivers_C0_Hz'] == [10.0]
          and r13['activacion']['medido']['x_C0_Hz'] == 10.0 and r14['estado'] == 'ACTIVADO'
          and r14['activacion']['medido']['DQ2_Hz'] == 5.0 and t['C_10']['etiqueta'] == 'ON'
          and t['C_01']['etiqueta'] == 'OFF' and res['casos']['C|H1b']['transferencia'] == 'OTRA_TRANSFERENCIA')
    return ok, ('driver y x en 10,0 Hz -> %s; DQ2 en 5,0 Hz -> %s; C_10 en 10,0 Hz -> %s y C_01 en 2,0 Hz -> %s, '
                'transferencia %s' % (r13['estado'], r14['estado'], t['C_10']['etiqueta'], t['C_01']['etiqueta'],
                                      res['casos']['C|H1b']['transferencia']))


def e23(ctx):
    res = analizar(ctx['man'], tabla_sintetica(ctx['man'], {('R01', 'A'): {'za3_contrario': True}}))
    v = res['veredictos']['F_R01']
    f = filas(res, 'F_R01')
    ok = (v['firma'] == 'SIN_DECIDIR' and v['contrastes'] == {'ZA1': True, 'ZA2': True, 'ZA3': False}
          and f['A|R01|ZA3']['media'] < 0 and res['veredictos']['P_T1_B']['veredicto'] == 'SOSTENIDA')
    return ok, ('ZA3 en contra (QCOL con ZA sube el D): contrastes=%s, ZA3 media=%.2f -> firma %s; P_T1_B sigue %s'
                % (json.dumps(v['contrastes'], sort_keys=True), f['A|R01|ZA3']['media'], v['firma'],
                   res['veredictos']['P_T1_B']['veredicto']))


PRUEBAS = [('E01', e01), ('E02', e02), ('E03', e03), ('E04', e04), ('E05', e05), ('E06', e06), ('E07', e07),
           ('E08', e08), ('E09', e09), ('E10', e10), ('E11', e11), ('E12', e12), ('E13', e13), ('E14', e14),
           ('E15', e15), ('E16', e16), ('E17', e17), ('E18', e18), ('E19', e19), ('E20', e20), ('E21', e21),
           ('E22', e22), ('E23', e23)]


def main():
    ap = argparse.ArgumentParser(description='Pruebas sinteticas de estadistica_a1.py')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--solo', default='')
    ap.add_argument('--tmp', default=None)
    a = ap.parse_args()
    sha = C.sha_archivo(a.manifiesto)
    if sha != a.sha_manifiesto:
        print('ABORTA: el manifiesto tiene sha256 %s y se esperaba %s' % (sha, a.sha_manifiesto), flush=True)
        raise SystemExit(2)
    with open(a.manifiesto, encoding='utf-8') as f:
        man = json.load(f)
    print('PRUEBA_ESTADISTICA inicio manifiesto=%s estadistica_sha256=%s prueba_sha256=%s python=%s numpy=%s scipy=%s'
          % (sha, C.sha_archivo(os.path.abspath(E.__file__)), C.sha_archivo(os.path.abspath(__file__)),
             sys.version.split()[0], np.__version__, scipy.__version__), flush=True)
    ctx = {'man': man, 'sha': sha, 'manifiesto': os.path.abspath(a.manifiesto),
           'tmp': a.tmp or tempfile.gettempdir()}
    solo = {s.strip() for s in a.solo.split(',') if s.strip()}
    for nombre, f in PRUEBAS:
        if solo and nombre not in solo:
            continue
        t0 = time.time()
        try:
            ok, det = f(ctx)
        except BaseException as ex:  # noqa: B902 - una prueba que revienta es una prueba que falla
            ok, det = False, 'EXCEPCION %s: %s' % (type(ex).__name__, ex)
        RESULTADOS.append((nombre, bool(ok)))
        print('PRUEBA %s %s %s (%.1f s)' % (nombre, 'PASS' if ok else 'FAIL', det, time.time() - t0), flush=True)
    k = sum(1 for _, ok in RESULTADOS if ok)
    print('PRUEBA_ESTADISTICA %d/%d %s' % (k, len(RESULTADOS), 'PASS' if k == len(RESULTADOS) else 'FAIL'), flush=True)
    raise SystemExit(0 if k == len(RESULTADOS) else 1)


if __name__ == '__main__':
    main()
