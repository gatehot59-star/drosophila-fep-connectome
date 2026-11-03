#!/usr/bin/env python3
"""prueba_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-005).

Pruebas del runner de 009-A1 antes de cualquier corrida. Cada prueba puede dar rojo: las que comparan dos caminos
traen un control negativo que tiene que salir distinto. Fixture de 30 neuronas en formato Shiu (Completeness csv,
parquet de 7 columnas y units npz); las simulaciones usan create_model() y poi() del model.py real, cada una en un
proceso nuevo.
Uso: python3 prueba_a1.py --shiu DIR --target numpy|cython --trabajo DIR [--manifiesto-real M.json] [--n-proc 2]
Exit 0 solo si pasan todas.
"""
import argparse
import copy
import json
import multiprocessing as mp
import os
import sys
import types
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun_a1 as C  # noqa: E402
import manifiesto_a1 as M  # noqa: E402
import runner_a1 as R  # noqa: E402
import validar_a1 as V  # noqa: E402

N_FX = 30
RAIZ0 = 10 ** 9
INH_FX = (4, 13, 16, 21, 26)
FILAS_FX = (
    (0, 3, 200), (1, 3, 200), (2, 3, 200), (0, 5, 180), (1, 6, 180), (2, 7, 180),
    (3, 4, 250), (8, 4, 200), (3, 5, 40), (3, 6, 15), (3, 15, 20), (8, 7, 25),
    (4, 5, -120), (4, 6, -90), (4, 7, -60), (4, 14, -30), (4, 3, -20), (4, 22, -40),
    (9, 4, 3), (10, 4, 3), (11, 4, 6), (12, 4, 4), (13, 4, -4), (16, 3, -50), (0, 16, 180),
    (3, 17, 10), (8, 17, 10), (8, 3, 200), (0, 19, 180), (1, 20, 180), (2, 21, 180),
    (19, 22, 120), (20, 23, 100), (21, 24, -80), (22, 25, 170), (23, 26, 60), (24, 19, 90),
    (25, 27, 200), (26, 28, -50), (27, 29, 150), (28, 20, 110), (29, 21, 130), (5, 26, 60), (6, 27, 40), (7, 28, 90))
D_FX = {3: 0, 5: 1, 6: 2, 7: 3, 8: 4, 9: 5, 10: 6, 11: 7, 13: 8}
TIPO_FX = {0: 'PA', 1: 'PA', 2: 'PA', 3: 'DND1', 4: 'HX', 5: 'DNT', 6: 'DNT', 7: 'DNT', 8: 'DND2', 9: 'DNW',
           10: 'DNW', 11: 'DNW', 13: 'DNI', 16: 'ZAX', 17: 'SONDA', 19: 'PA', 23: 'PA'}
HUMO_FX = ['F1|B|C0|900', 'F1|B|SHAM|900', 'F1|B|Q1|900', 'F1|B|C0|901', 'F1|B|SHAM|901', 'F1|B|Q1|901',
           'F1|A|C0|900', 'F1|A|ZA|900', 'FH|B|C0|900', 'FH|B|Q1conj|900', 'FH|C|C_11|900', 'FH|C|C_desplazado|900']
RESULTADOS = []


def anotar(nombre, ok, detalle=''):
    RESULTADOS.append((nombre, bool(ok)))
    print('PRUEBA %s %s %s' % (nombre, 'PASS' if ok else 'FAIL', detalle), flush=True)


def fila(p, q):
    for k, (a, b, _) in enumerate(FILAS_FX):
        if (a, b) == (p, q):
            return k
    raise KeyError((p, q))


def filas(*pares):
    return sorted(fila(p, q) for p, q in pares)


def escribir_fixture(d):
    import pandas as pd
    os.makedirs(d, exist_ok=True)
    ids = np.array([RAIZ0 + i for i in range(N_FX)], dtype=np.int64)
    comp = os.path.join(d, 'completeness_fx.csv')
    with open(comp, 'w') as f:
        f.write(',Completed\n')
        for r in ids:
            f.write('%d,True\n' % r)
    pre = np.array([p for p, _, _ in FILAS_FX], dtype=np.int64)
    post = np.array([q for _, q, _ in FILAS_FX], dtype=np.int64)
    w = np.array([v for _, _, v in FILAS_FX], dtype=np.int64)
    df = pd.DataFrame({'Presynaptic_ID': ids[pre], 'Postsynaptic_ID': ids[post], 'Presynaptic_Index': pre,
                       'Postsynaptic_Index': post, 'Connectivity': np.abs(w), 'Excitatory': np.sign(w),
                       'Excitatory x Connectivity': w})
    conn = os.path.join(d, 'connectivity_fx.parquet')
    df.to_parquet(conn, index=False)
    S = np.full(N_FX, -1, dtype=np.int32)
    S[[0, 1, 2, 19]] = 0
    D = np.full(N_FX, -1, dtype=np.int32)
    for k, v in D_FX.items():
        D[k] = v
    inh = np.zeros(N_FX, dtype=bool)
    inh[list(INH_FX)] = True
    tipo = np.array([TIPO_FX.get(i, 'OTRO') for i in range(N_FX)])
    sl = np.ones(N_FX, dtype=np.int8)
    sl[19] = 0
    units = os.path.join(d, 'units_fx.npz')
    np.savez_compressed(units, S=S, D=D, inh=inh, excl=np.zeros(N_FX, dtype=bool), root=ids, tipo=tipo, sl=sl)
    return comp, conn, units


def espec_fx():
    dp, A = [5, 6, 7], [0, 1, 2]
    e1 = {'root_d': RAIZ0 + 3, 'root_x': RAIZ0 + 4, 'Q1': [1, 250], 'Q2': [6, 360], 'Q3': [5, 335], 'Q4': [6, 220],
          'QCOL': [2, 55], 'Q1uQCOL': [3, 305], 'QXD': [3, 270], 'Q1uQXD': [4, 520], 'QWEAK': [9, 4, 3],
          'Dp': [3, C.huella_lista(dp)], 'A': [3, C.huella_lista(A)], 'A_indices': A, 'A_peso_driver': 600,
          'lado_driver': 1}
    eh = {'Dp': [3, C.huella_lista(dp)], 'QCOL': [3, 80], 'QXD': [3, 270], 'Q1conjuQCOL': [5, 530],
          'Q1conjuQXD': [5, 720], 'QWEAK': [9, 4, 3], 'Q1conj': [2, 450], 'Q4conj': [5, 20]}
    return {'relevos': [{'id': 'F1', 'codigo': 'F1_fixture', 'd': 3, 'x': 4, 'A_label': 'PA_right', 'esperado': e1}],
            'hubs': [{'id': 'FH', 'x': 4, 'G': [3, 8], 'esperado': eh}], 'lado_codigo': {'right': 1, 'left': 0},
            'cascada': {'relevo': 'F1', 'ZA': [16, 3], 'esperado': {'ZA': [1, 50], 'ZAuQ1': [2, 300]}},
            'humo': list(HUMO_FX)}


def en_procesos(fn, lista, n_proc):
    with ProcessPoolExecutor(max_workers=max(1, n_proc), mp_context=mp.get_context('spawn'), max_tasks_per_child=1) as ex:
        return list(ex.map(fn, lista))


def _sim(args):
    """Una simulacion del fixture en un proceso nuevo. modo: poisson, generador, op_synapses u op_start."""
    modo, shiu_dir, comp, conn, target, fuentes, tasa, evs, seed = args
    import brian2 as b2
    b2.prefs.codegen.target = target
    b2.defaultclock.dt = C.DT_S * b2.second
    shiu = R.cargar_shiu(shiu_dir)
    params = dict(shiu.default_params)
    b2.seed(int(seed))
    neu, syn, mon = shiu.create_model(comp, conn, params)
    if modo == 'poisson':
        params['r_poi'] = float(tasa) * b2.Hz
        pois, neu = shiu.poi(neu, list(fuentes), [], params)
        extra = list(pois)
    elif modo == 'generador':
        extra = R.entrada_generador(b2, neu, evs, params)
    else:
        when = modo.split('_', 1)[1]
        w = float(params['w_syn'] * params['f_poi'] / b2.volt)
        por = {}
        for _, idx, t in evs:
            for k in np.asarray(t).tolist():
                por.setdefault(int(k), []).append(int(idx))
        por = {k: np.asarray(v, dtype=np.int64) for k, v in por.items()}
        neu.rfc[np.asarray(sorted({int(e[1]) for e in evs}), dtype=np.int64)] = 0 * b2.ms

        def op(t):
            v = por.get(int(round(float(t / b2.second) / C.DT_S)))
            if v is not None:
                neu.v_[v] = neu.v_[v] + w
        extra = [b2.NetworkOperation(op, when=when, name='a1_ref_op')]
    net = b2.Network(neu, syn, mon, *extra)
    net.run(params['t_run'])
    i = np.asarray(mon.i[:], dtype=np.int64)
    return i.tolist(), np.rint(np.asarray(mon.t_[:]) / C.DT_S).astype(np.int64).tolist()


def _replay(args):
    """Banco C del hub FH con C_11, contando llegadas a la sonda 17 por residuos de g. suprimir=False es el negativo."""
    shiu_dir, comp, conn, target, ruta_man, suprimir = args
    import brian2 as b2
    b2.prefs.codegen.target = target
    b2.defaultclock.dt = C.DT_S * b2.second
    man = json.load(open(ruta_man))
    suj = man['sujetos']['FH']
    g = C.Grafo.desde_parquet(conn)
    shiu = R.cargar_shiu(shiu_dir)
    params = dict(shiu.default_params)
    neu, syn, mon = shiu.create_model(comp, conn, params)
    w0 = np.array(syn.w_[:], dtype=np.float64, copy=True)
    q3 = [np.asarray(suj['mascaras_base']['Q3_%d' % v], dtype=np.int64) for v in suj['G']]
    q4 = np.asarray(suj['mascaras_base']['Q4conj'], dtype=np.int64)
    cero = np.unique(np.concatenate(q3 + [q4])) if suprimir else q4
    w1 = w0.copy()
    w1[cero] = 0.0
    syn.w_[:] = w1
    base = C.eventos_grupo('C_FH', 900, man['grupos']['C_FH']['fuentes'])[0][2]
    objs, _ = R.montar_replay(b2, neu, g, w0, suj['G'], q3, base, [1, 1], [0, 0], params)
    sonda = b2.StateMonitor(neu, 'g', record=[17], when='end', name='a1_sonda')
    net = b2.Network(neu, syn, mon, sonda, *objs)
    net.run(params['t_run'])
    gg = np.asarray(sonda.g_[0], dtype=np.float64)
    dec = np.exp(-C.DT_S / float(params['tau'] / b2.second))
    res = np.concatenate([[gg[0]], gg[1:] - gg[:-1] * dec])
    wq = 10 * float(params['w_syn'] / b2.volt)
    i = np.asarray(mon.i[:], dtype=np.int64)
    return {'llegadas': float(res.sum() / wq), 'esperadas': int(2 * np.sum(base + 18 <= C.NTICKS - 1)),
            'espigas_d1': int(np.sum(i == 3)), 'espigas_sonda': int(np.sum(i == 17))}


def p01_semilla():
    ka = [('B_R01', 0, 59804, 'driver', 5428794271745577241), ('A_LPLC1_right', 0, 333, 'aferente', 16424232594708459014),
          ('C_H2', 0, 19257, 'replay', 17704105924621129695)]
    ok = all(C.semilla(gr, s, i, r) == v for gr, s, i, r, v in ka)
    ok &= C.texto_semilla('B_R01', 0, 59804, 'driver') == '009-A1|B_R01|0|59804|driver'
    e1 = C.eventos_bernoulli(ka[0][4], 50.0)
    e2 = C.eventos_bernoulli(ka[1][4], 150.0)
    rp = C.ticks_replay(ka[2][4])
    ok &= e1.size == 55 and e1[:6].tolist() == [58, 419, 473, 835, 989, 1158]
    ok &= e2.size == 137 and e2[:6].tolist() == [45, 219, 241, 248, 363, 432]
    ok &= rp.size == 50 and np.unique(rp).size == 50 and rp[:6].tolist() == [104, 155, 212, 672, 913, 968]
    ok &= all(v > 2 ** 32 for *_, v in ka)
    anotar('T01_semilla_y_eventos', ok, 'tres respuestas conocidas, 64 bits sin truncar, replay 50 unicos')


def p02_colisiones(man):
    real = man['contrato_semilla']['colisiones']
    plantada = M.colisiones(man['grupos'], [900], fsemilla=lambda *x: 7)
    ok = real['n_colisiones'] == 0 and real['n_claves'] == real['n_semillas_distintas'] and plantada['n_colisiones'] > 0
    anotar('T02_colisiones', ok, 'reales=%d claves=%d; plantada=%d' % (real['n_colisiones'], real['n_claves'], plantada['n_colisiones']))


def p03_manifiesto(man, g, u, ent):
    ch = man['chequeos']
    esp = espec_fx()
    esp['relevos'][0]['esperado']['QCOL'] = [2, 56]
    mal = M.construir(esp, g, u, ent)['chequeos']
    ok = ch['n'] > 0 and ch['ok'] == ch['n'] and mal['fallas'] == ['F1 QCOL']
    anotar('T03_guardas_del_manifiesto', ok, '%d/%d; con un esperado falso: %s' % (ch['ok'], ch['n'], mal['fallas']))


def p04_mascaras(man, g, u):
    f1, fh = man['sujetos']['F1'], man['sujetos']['FH']
    mb = f1['mascaras_base']
    ok = f1['Dp'] == [5, 6, 7] and f1['A'] == [0, 1, 2]
    ok &= mb['QCOL'] == filas((3, 5), (3, 6)) and mb['QXD'] == filas((4, 5), (4, 6), (4, 7))
    ok &= mb['Q4'] == filas((8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4)) and mb['QWEAK'] == filas((9, 4))
    ok &= mb['ZA'] == filas((16, 3)) and mb['Q1'] == filas((3, 4))
    ok &= fh['mascaras_base']['Q1conj'] == filas((3, 4), (8, 4))
    ok &= fh['mascaras_base']['Q4conj'] == filas((9, 4), (10, 4), (11, 4), (12, 4), (13, 4))
    ok &= f1['huellas_condicion']['SHAM']['n'] == 0 and f1['huellas_condicion']['C0']['n'] == 0
    r = g.desde(4)
    invertida = np.unique(r[(g.w[r] > 0) & np.isin(g.post[r], f1['Dp'])]).tolist()
    ok &= invertida != mb['QXD']
    anotar('T04_mascaras_exactas', ok, 'D, A, QCOL, QXD, Q4, QWEAK, ZA y conjuntas por fila; QXD con signo invertido=%s' % invertida)


def p05_poisson(a, comp, conn):
    ref = en_procesos(_sim, [('poisson', a.shiu, comp, conn, a.target, [0, 1, 2], 150.0, None, 12345)], 1)[0]
    i_ref, t_ref = np.asarray(ref[0]), np.asarray(ref[1])
    evs = [('aferente', k, t_ref[i_ref == k] - 1) for k in (0, 1, 2)]
    neg = [(r, k, t + 1) for r, k, t in evs]
    gen, mal = en_procesos(_sim, [('generador', a.shiu, comp, conn, a.target, None, None, e, 0) for e in (evs, neg)], 2)
    igual = gen[0] == ref[0] and gen[1] == ref[1]
    distinto = not (mal[0] == ref[0] and mal[1] == ref[1])
    fuera = int(np.sum(~np.isin(i_ref, [0, 1, 2])))
    n_fuentes = int(np.sum(np.isin(i_ref, [0, 1, 2])))
    ok = igual and distinto and fuera > 0 and n_fuentes > 100
    anotar('T05_equivalencia_con_PoissonInput', ok, 'espigas=%d (fuentes %d, resto %d); identico=%s; negativo distinto=%s' % (
        len(ref[0]), n_fuentes, fuera, igual, distinto))


def p06_recurrente(a, comp, conn, man):
    evs = C.eventos_grupo('B_F1', 900, man['grupos']['B_F1']['fuentes'])
    sims = en_procesos(_sim, [(m, a.shiu, comp, conn, a.target, None, None, evs, 0) for m in ('generador', 'op_synapses', 'op_start')], 3)
    igual = sims[0] == sims[1]
    distinto = sims[0] != sims[2]
    ok = igual and distinto and len(sims[0][0]) > 0
    anotar('T06_entrada_en_turno_synapses', ok, 'espigas=%d; igual a v+=w en synapses=%s; distinto en start=%s' % (len(sims[0][0]), igual, distinto))


def p07_runner(a, comp, conn, units, man, sha_man, salida):
    args = types.SimpleNamespace(code_commit='PRUEBA_FIXTURE', shiu=a.shiu, comp=comp, conn=conn, units=units, target=a.target)
    res = R.ejecutar(R.tareas_de(man, sha_man, HUMO_FX, args), a.n_proc, salida)
    regs = V.leer_registros(salida)
    v = V.validar(man, sha_man, regs, HUMO_FX)
    por = {C.id_ensayo(r['subject_id'], r['regime'], r['condition'], r['seed']): r for _, r in regs}
    ok_estado = all(r['estado'] == 'OK' for r in res) and len(res) == len(HUMO_FX)
    sham = all(por['F1|B|SHAM|%d' % s]['espigas_sha256'] == por['F1|B|C0|%d' % s]['espigas_sha256'] for s in (900, 901))
    q1 = any(por['F1|B|Q1|%d' % s]['espigas_sha256'] != por['F1|B|C0|%d' % s]['espigas_sha256'] for s in (900, 901))
    par = len({por[t]['input_events_hash'] for t in ('F1|B|C0|900', 'F1|B|SHAM|900', 'F1|B|Q1|900')}) == 1
    c11, cd = por['FH|C|C_11|900'], por['FH|C|C_desplazado|900']
    banco = c11['input_events_hash'] == cd['input_events_hash'] and c11['replay_aplicado_hash'] != cd['replay_aplicado_hash']
    ok = ok_estado and v['estado'] == 'OK' and sham and q1 and par and banco
    anotar('T07_runner_sobre_fixture', ok, 'recibos=%d OK=%s validacion=%s SHAM=C0=%s Q1!=C0=%s pareado=%s banco=%s x(C0,Q1)=%s,%s' % (
        len(res), ok_estado, v['estado'], sham, q1, par, banco, por['F1|B|C0|900'].get('cuenta_x'), por['F1|B|Q1|900'].get('cuenta_x')))
    return regs


def p08_replay(a, comp, conn, ruta_man):
    bien, mal = en_procesos(_replay, [(a.shiu, comp, conn, a.target, ruta_man, s) for s in (True, False)], 2)
    ok = (abs(bien['llegadas'] - bien['esperadas']) < 1e-6 and bien['espigas_d1'] > 0
          and mal['llegadas'] > mal['esperadas'] + 0.5 and bien['espigas_sonda'] == 0)
    anotar('T08_replay_sin_duplicar', ok, 'con supresion %.6f llegadas de %d esperadas, d1 endogena=%d; sin supresion %.6f' % (
        bien['llegadas'], bien['esperadas'], bien['espigas_d1'], mal['llegadas']))


def p09_corruptos(man, sha_man, regs, g, u):
    def buscar(lst, tid):
        for k, (_, r) in enumerate(lst):
            if C.id_ensayo(r['subject_id'], r['regime'], r['condition'], r['seed']) == tid:
                return k
        raise KeyError(tid)

    Dset = np.asarray(u['D']) >= 0
    r4 = g.desde(4)
    dp_inv = np.unique(g.post[r4[(g.w[r4] > 0) & Dset[g.post[r4]]]])
    casos = []

    def caso(nombre, codigo, fn):
        lst = copy.deepcopy(regs)
        fn(lst)
        v = V.validar(man, sha_man, lst, HUMO_FX)
        casos.append((nombre, v['estado'] == 'INVALIDO_TECNICO' and codigo in {x['codigo'] for x in v['fallos']}))

    def root_mal(lst):
        lst[buscar(lst, 'F1|B|Q1|900')][1]['identidad']['roots']['4'] += 1

    def indice_mal(lst):
        lst[buscar(lst, 'F1|B|Q1|900')][1]['identidad']['x'] = 5

    def signo_mal(lst):
        lst[buscar(lst, 'F1|B|C0|901')][1]['Dprime_hash'] = C.huella_lista(dp_inv)

    def entrada_mal(lst):
        lst[buscar(lst, 'F1|B|SHAM|900')][1]['input_events_hash'] = '0' * 64

    def faltante(lst):
        del lst[buscar(lst, 'F1|B|Q1|901')]

    def duplicado(lst):
        k = buscar(lst, 'F1|B|C0|900')
        lst.append(('copia_' + lst[k][0], copy.deepcopy(lst[k][1])))

    def sham_mal(lst):
        lst[buscar(lst, 'F1|B|SHAM|901')][1]['espigas_sha256'] = 'f' * 64

    def estado_mal(lst):
        lst[buscar(lst, 'FH|B|C0|900')][1].update({'estado': 'INVALIDO_TECNICO', 'exit': 1})

    def mascara_mal(lst):
        lst[buscar(lst, 'F1|B|Q1|901')][1]['mask_hash'] = man['sujetos']['F1']['huellas_condicion']['C0']['sha256']

    caso('root', 'IDENTIDAD', root_mal)
    caso('indice', 'IDENTIDAD', indice_mal)
    caso('signo_invertido', 'DPRIME', signo_mal)
    caso('entrada_desigual', 'ENTRADA_DESIGUAL', entrada_mal)
    caso('faltante', 'FALTANTE', faltante)
    caso('duplicado', 'DUPLICADO', duplicado)
    caso('sham_distinto', 'SHAM_DISTINTO_DE_C0', sham_mal)
    caso('estado', 'ESTADO_TECNICO', estado_mal)
    caso('mascara_ajena', 'MASCARA', mascara_mal)
    limpio = V.validar(man, sha_man, regs, HUMO_FX)['estado'] == 'OK'
    ok = limpio and all(x for _, x in casos)
    anotar('T09_recibos_corruptos', ok, 'limpio=%s; rechazados %d/%d: %s' % (limpio, sum(x for _, x in casos), len(casos), casos))


def p10_adulterado(a, comp, conn, units, man, trabajo):
    args = types.SimpleNamespace(code_commit='PRUEBA_FIXTURE', shiu=a.shiu, comp=comp, conn=conn, units=units, target=a.target)
    m1 = copy.deepcopy(man)
    m1['sujetos']['F1']['mascaras_base']['Q1'] = filas((8, 4))
    m2 = copy.deepcopy(man)
    m2['grupos']['B_F1']['eventos']['900']['sha256'] = '0' * 64
    tareas = R.tareas_de(m1, 'ADULTERADO_1', ['F1|B|Q1|900'], args) + R.tareas_de(m2, 'ADULTERADO_2', ['F1|B|C0|900'], args)
    res = R.ejecutar(tareas, 2, os.path.join(trabajo, 'adulterado'))
    mot = sorted(r['motivo'] for r in res)
    ok = all(r['estado'] == 'INVALIDO_TECNICO' for r in res) and any('mascara Q1' in m for m in mot) and any('eventos' in m for m in mot)
    ruta = os.path.join(trabajo, 'manifiesto_fx.json')
    try:
        R.cargar_manifiesto(ruta, 'f' * 64)
        rechaza = False
    except SystemExit as e:
        rechaza = e.code == 2
    ok &= rechaza
    anotar('T10_runner_rechaza_manifiesto_adulterado', ok, 'motivos=%s; sha ajeno rechazado=%s' % (mot, rechaza))


def p11_real(ruta):
    man = json.load(open(ruta))
    ch, col = man['chequeos'], man['contrato_semilla']['colisiones']
    plan = {(c['sujeto'], c['regimen']): c for c in man['celdas']}
    humo = all(t.split('|')[2] in plan[tuple(t.split('|')[:2])]['condiciones'] for t in man['humo'])
    ok = (ch['ok'] == ch['n'] == 308 and len(man['sujetos']) == 22 and len(man['grupos']) == 40
          and man['n_ensayos_plan'] == 8540 and col['n_colisiones'] == 0 and col['supera_32_bits']
          and man['humo'] == M.HUMO_REAL and humo)
    anotar('T11_manifiesto_real', ok, 'chequeos %d/%d, sujetos=%d, grupos=%d, ensayos=%d, colisiones=%d, claves=%d' % (
        ch['ok'], ch['n'], len(man['sujetos']), len(man['grupos']), man['n_ensayos_plan'], col['n_colisiones'], col['n_claves']))


def main():
    ap = argparse.ArgumentParser(description='Pruebas del runner de 009-A1')
    ap.add_argument('--shiu', required=True)
    ap.add_argument('--target', default='numpy')
    ap.add_argument('--trabajo', required=True)
    ap.add_argument('--manifiesto-real', default='')
    ap.add_argument('--n-proc', type=int, default=2)
    a = ap.parse_args()
    os.makedirs(a.trabajo, exist_ok=True)
    comp, conn, units = escribir_fixture(a.trabajo)
    g = C.Grafo.desde_parquet(conn)
    u = {k: v for k, v in np.load(units).items()}
    ent = {'parquet_sha256': C.sha_archivo(conn), 'units_contenido_sha256': C.huella_contenido_npz(units),
           'sello_sha256': 'FIXTURE', 'evid010_sha256': 'FIXTURE'}
    ruta_man = os.path.join(a.trabajo, 'manifiesto_fx.json')
    sha_man, nbytes = M.escribir(M.construir(espec_fx(), g, u, ent), ruta_man)
    man = json.load(open(ruta_man))
    print('== prueba_a1.py %s target=%s; manifiesto del fixture %s, %d bytes ==' % (R.VERSION, a.target, sha_man, nbytes), flush=True)
    p01_semilla()
    p02_colisiones(man)
    p03_manifiesto(man, g, u, ent)
    p04_mascaras(man, g, u)
    p05_poisson(a, comp, conn)
    p06_recurrente(a, comp, conn, man)
    regs = p07_runner(a, comp, conn, units, man, sha_man, os.path.join(a.trabajo, 'recibos'))
    p08_replay(a, comp, conn, ruta_man)
    p09_corruptos(man, sha_man, regs, g, u)
    p10_adulterado(a, comp, conn, units, man, a.trabajo)
    if a.manifiesto_real:
        p11_real(a.manifiesto_real)
    n_ok = sum(1 for _, ok in RESULTADOS if ok)
    print('PRUEBA_A1 %d/%d %s' % (n_ok, len(RESULTADOS), 'PASS' if n_ok == len(RESULTADOS) else 'FAIL'), flush=True)
    return 0 if n_ok == len(RESULTADOS) else 1


if __name__ == '__main__':
    sys.exit(main())
