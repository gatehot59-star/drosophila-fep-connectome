#!/usr/bin/env python3
"""runner_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-005).

Productor de ensayos de H_MECANISMO_RELEVOS16 / 009-A1 sobre el LIF de Shiu et al. 2024: create_model() y
default_params de model.py (philshiu/Drosophila_brain_model@91bdd1e7, sha256 fc45837d...) sin cambios.
Cada ensayo corre en un proceso nuevo y, antes de simular, rehace desde el parquet y las units lo que fija el
manifiesto: roots, D', filas de cada mascara, eventos externos y coherencia de fuentes. Si algo difiere, el recibo
sale INVALIDO_TECNICO sin simular. Despues comprueba que el orden de sinapsis de create_model sea el del parquet,
edita una copia de los pesos y verifica que fuera de la mascara queden identicos.
Entrada A/B: SpikeGeneratorGroup con los eventos materializados y Synapses(on_pre='v_post += w_syn*f_poi', delay 0),
que actua en el turno 'synapses' del mismo paso, como PoissonInput en poi(); refractario 0 en las estimuladas.
Banco C: filas salientes de los drivers y Q4 conjunto en cero, y una fuente por driver con sus mismas filas (post,
peso y t_dly), asi no se duplican eventos.
Uso: python3 runner_a1.py --manifiesto M --sha-manifiesto H (--humo | --ids a,b) --shiu DIR --comp C --conn P
     --units U --salida DIR [--n-proc 2] [--target cython] [--code-commit SHA]
Exit 0 si todos los recibos salen OK; 1 si alguno es INVALIDO_TECNICO; 2 si el manifiesto o una entrada no coincide.
"""
import argparse
import importlib.util
import json
import multiprocessing as mp
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun_a1 as C  # noqa: E402

VERSION = '2026-11-03-005'
SHA_MODEL = 'fc45837d7122c6ce2a7f3f2f23c515992e4b232aadb919efabb72337fac88e4e'
SHA_COMP = 'bbb847a4cc2caaa7a16349722d220c087317b946d148d4d592d94d250617a311'
SEMILLA_BRIAN2 = 20261103
CAMPOS = ('protocol_id', 'code_commit', 'manifiesto_sha256', 'subject_id', 'regime', 'condition', 'seed', 'grupo')


def cargar_shiu(dir_shiu):
    spec = importlib.util.spec_from_file_location('shiu_model_a1', os.path.join(dir_shiu, 'model.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def entrada_generador(b2, neu, evs, params, nombre='a1_entrada'):
    """Fuentes materializadas con la semantica de poi(): v += w_syn*f_poi en el turno 'synapses' del paso del evento."""
    if not evs:
        return []
    blancos = np.array([int(e[1]) for e in evs], dtype=np.int64)
    if np.unique(blancos).size != blancos.size:
        raise ValueError('dos fuentes sobre la misma neurona')
    ii = np.concatenate([np.full(len(e[2]), k, dtype=np.int64) for k, e in enumerate(evs)])
    tt = np.concatenate([np.asarray(e[2], dtype=np.int64) for e in evs])
    gen = b2.SpikeGeneratorGroup(len(evs), ii, tt * C.DT_S * b2.second, name=nombre)
    syn = b2.Synapses(gen, neu, on_pre='v_post += w_entrada', delay=0 * b2.ms,
                      namespace={'w_entrada': params['w_syn'] * params['f_poi']}, name=nombre + '_syn')
    syn.connect(i=np.arange(len(evs)), j=blancos)
    neu.rfc[blancos] = 0 * b2.ms
    return [gen, syn]


def montar_replay(b2, neu, g, w0, G, filas_q3, ticks_base, encendidos, desplaz, params, nombre='a1_replay'):
    """Una fuente por driver de G con sus mismas filas salientes: mismos post, mismos pesos en volt y retardo t_dly."""
    trenes, ii, tt = [], [], []
    base = np.asarray(ticks_base, dtype=np.int64)
    for k, gi in enumerate(G):
        if int(encendidos[k]):
            t = np.sort((base + int(desplaz[k])) % C.NTICKS)
            trenes.append(('replay', int(gi), t))
            ii.append(np.full(t.size, k, dtype=np.int64))
            tt.append(t)
    ii = np.concatenate(ii) if ii else np.zeros(0, dtype=np.int64)
    tt = np.concatenate(tt) if tt else np.zeros(0, dtype=np.int64)
    gen = b2.SpikeGeneratorGroup(len(G), ii, tt * C.DT_S * b2.second, name=nombre)
    pre_k = np.concatenate([np.full(len(f), k, dtype=np.int64) for k, f in enumerate(filas_q3)])
    filas = np.concatenate([np.asarray(f, dtype=np.int64) for f in filas_q3])
    post = g.post[filas].astype(np.int64)
    syn = b2.Synapses(gen, neu, 'w : volt', on_pre='g_post += w', delay=params['t_dly'], name=nombre + '_syn')
    syn.connect(i=pre_k, j=post)
    if not (np.array_equal(np.asarray(syn.i[:]), pre_k) and np.array_equal(np.asarray(syn.j[:]), post)):
        raise ValueError('orden de las sinapsis de replay distinto del pedido')
    syn.w_[:] = np.asarray(w0, dtype=np.float64)[filas]
    return [gen, syn], C.huella_eventos(trenes)


def _invalido(rec, t0, motivo):
    rec.update({'estado': 'INVALIDO_TECNICO', 'motivo': motivo, 'exit': 1, 'duracion_s': round(time.time() - t0, 3)})
    return rec


def ensayo(tarea):
    """Un ensayo en su proceso: verificaciones, red nueva de Shiu, edicion de pesos, entrada, 1 s y recibo."""
    t0 = time.time()
    rec = {k: tarea[k] for k in CAMPOS}
    rec.update({'runner_version': VERSION, 'input_hashes': tarea['entradas'], 'estado': 'OK', 'motivo': '', 'exit': 0})
    chq = rec['chequeos'] = {}
    try:
        suj, cond, reg = tarea['sujeto'], tarea['condition'], tarea['regime']
        g = C.Grafo.desde_parquet(tarea['conn'])
        u = np.load(tarea['units'])
        Dset = np.asarray(u['D']) >= 0
        root = np.asarray(u['root'])
        roots = {str(i): int(root[i]) for i in [int(suj['x'])] + [int(v) for v in suj['G']]}
        rec['identidad'] = {'x': int(suj['x']), 'd': suj.get('d'), 'G': [int(v) for v in suj['G']], 'roots': roots}
        chq['identidad'] = roots == suj['roots']
        if not chq['identidad']:
            return _invalido(rec, t0, 'identidad: roots distintos del manifiesto')
        Dp = C.dprime(g, Dset, suj['x'], suj['G'])
        rec['Dprime_hash'], rec['Dprime_n'] = C.huella_lista(Dp), int(Dp.size)
        chq['Dprime'] = Dp.tolist() == suj['Dp'] and rec['Dprime_hash'] == suj['Dp_huella']['sha256']
        if not chq['Dprime']:
            return _invalido(rec, t0, "D' distinto del manifiesto")
        cache = {}
        for b in suj['composicion'][cond]:
            f = C.mascara_base(b, suj, g, Dset)
            if f.tolist() != suj['mascaras_base'][b]:
                return _invalido(rec, t0, 'mascara %s distinta del manifiesto' % b)
            cache[b] = f
        filas = C.filas_condicion(suj, cond, cache)
        hm = C.huella_mascara(g, filas)
        rec['mask_hash'], rec['mask_n'], rec['mask_abs'] = hm['sha256'], hm['n'], hm['abs']
        chq['mascara'] = hm == suj['huellas_condicion'][cond]
        if not chq['mascara']:
            return _invalido(rec, t0, 'huella de mascara distinta del manifiesto')
        evs = C.eventos_grupo(tarea['grupo'], tarea['seed'], tarea['fuentes'])
        rec['input_events_hash'] = C.huella_eventos(evs)
        rec['n_input_events'] = int(sum(int(e[2].size) for e in evs))
        chq['eventos'] = rec['input_events_hash'] == tarea['eventos_esperado']
        if not chq['eventos']:
            return _invalido(rec, t0, 'eventos distintos del manifiesto')
        roles = {}
        for rol, idx, _ in evs:
            roles.setdefault(rol, []).append(int(idx))
        if reg == 'A':
            chq['fuentes'] = set(roles) == {'aferente'} and sorted(roles['aferente']) == suj['A']
        elif reg == 'B':
            chq['fuentes'] = (set(roles) == {'driver', 'blanco'} and sorted(roles['driver']) == sorted(suj['G'])
                              and sorted(roles['blanco']) == suj['Dp'])
        else:
            chq['fuentes'] = roles == {'replay': [int(suj['x'])]}
        if not chq['fuentes']:
            return _invalido(rec, t0, 'fuentes incoherentes con el sujeto')
        import brian2 as b2
        b2.prefs.codegen.target = tarea['target']
        b2.defaultclock.dt = C.DT_S * b2.second
        b2.seed(SEMILLA_BRIAN2)
        shiu = cargar_shiu(tarea['shiu'])
        params = dict(shiu.default_params)
        neu, syn, mon = shiu.create_model(tarea['comp'], tarea['conn'], params)
        si, sj = np.asarray(syn.i[:]), np.asarray(syn.j[:])
        chq['orden_sinapsis'] = bool(si.size == g.pre.size and np.array_equal(si, g.pre) and np.array_equal(sj, g.post))
        del si, sj
        if not chq['orden_sinapsis']:
            return _invalido(rec, t0, 'orden de sinapsis distinto del parquet')
        w0 = np.array(syn.w_[:], dtype=np.float64, copy=True)
        chq['signo_pesos'] = bool(np.array_equal(np.sign(w0), np.sign(g.w)))
        if not chq['signo_pesos']:
            return _invalido(rec, t0, 'signo de pesos distinto del parquet')
        if cond != 'C0':
            w1 = w0.copy()
            w1[filas] = 0.0
            syn.w_[:] = w1
            leido = np.asarray(syn.w_[:])
            fuera = np.ones(w0.size, dtype=bool)
            fuera[filas] = False
            chq['pesos_fuera_intactos'] = bool(np.array_equal(leido[fuera], w0[fuera]))
            chq['mascara_en_cero'] = bool(np.all(leido[filas] == 0.0))
            rec['filas_cambiadas'] = int(np.count_nonzero(leido != w0))
            if not (chq['pesos_fuera_intactos'] and chq['mascara_en_cero'] and rec['filas_cambiadas'] == hm['n']):
                return _invalido(rec, t0, 'edicion de pesos no exacta')
            del w1, leido, fuera
        if reg in ('A', 'B'):
            extra = entrada_generador(b2, neu, evs, params)
        else:
            rp = tarea['replay']
            filas_q3 = [np.asarray(suj['mascaras_base']['Q3_%d' % v], dtype=np.int64) for v in suj['G']]
            extra, rec['replay_aplicado_hash'] = montar_replay(b2, neu, g, w0, suj['G'], filas_q3, evs[0][2],
                                                               rp['encendidos'], rp['desplaz'], params)
        net = b2.Network(neu, syn, mon, *extra)
        t1 = time.time()
        net.run(params['t_run'])
        rec['duracion_sim_s'] = round(time.time() - t1, 3)
        i = np.asarray(mon.i[:], dtype=np.int64)
        tk = np.rint(np.asarray(mon.t_[:], dtype=np.float64) / C.DT_S).astype(np.int64)
        cnt = np.bincount(i, minlength=len(neu))
        mirar = np.asarray(suj['mirar'], dtype=np.int64)
        rec['mirar_huella'] = C.huella_lista(mirar)
        rec['cuentas_mirar'] = cnt[mirar].tolist()
        rec['cuenta_x'] = int(cnt[int(suj['x'])])
        rec['cuentas_G'] = [int(cnt[int(v)]) for v in suj['G']]
        rec['espigas_total'] = int(i.size)
        rec['activas'] = int(np.count_nonzero(cnt))
        rec['espigas_sha256'] = C.huella_espigas(i, tk)
        co = getattr(getattr(neu, 'state_updater', None), 'codeobj', None)
        rec['entorno'] = {'brian2': b2.__version__, 'numpy': np.__version__, 'python': sys.version.split()[0],
                          'target_pedido': tarea['target'], 'codeobj': type(co).__name__ if co is not None else None,
                          'dt_s': float(b2.defaultclock.dt_), 't_run_s': float(params['t_run'] / b2.second)}
        rec['duracion_s'] = round(time.time() - t0, 3)
        return rec
    except Exception as e:  # el recibo dice que fallo; no se rellena nada
        return _invalido(rec, t0, 'excepcion %s: %s' % (type(e).__name__, str(e)[:400]))


def cargar_manifiesto(ruta, sha_esperado=''):
    sha = C.sha_archivo(ruta)
    if sha_esperado and sha != sha_esperado:
        print('ABORTA: el manifiesto %s tiene sha256 %s y se esperaba %s' % (ruta, sha, sha_esperado), flush=True)
        raise SystemExit(2)
    with open(ruta, encoding='utf-8') as f:
        return json.load(f), sha


def tareas_de(man, sha, ids, a):
    celdas = {(c['sujeto'], c['regimen']): c for c in man['celdas']}
    out = []
    for tid in ids:
        sid, reg, cond, s = tid.split('|')
        s = int(s)
        c = celdas.get((sid, reg))
        if c is None or cond not in c['condiciones']:
            raise SystemExit('ABORTA: %s no esta en el plan del manifiesto' % tid)
        if s not in C.SEMILLAS_PLAN and s not in C.SEMILLAS_HUMO:
            raise SystemExit('ABORTA: semilla %d fuera del contrato' % s)
        gr = man['grupos'][c['grupo']]
        suj = man['sujetos'][sid]
        t = {'protocol_id': C.PROTOCOLO, 'code_commit': a.code_commit, 'manifiesto_sha256': sha, 'subject_id': sid,
             'regime': reg, 'condition': cond, 'seed': s, 'grupo': c['grupo'], 'entradas': man['entradas'],
             'sujeto': suj, 'fuentes': gr['fuentes'], 'eventos_esperado': gr['eventos'][str(s)]['sha256'],
             'shiu': a.shiu, 'comp': a.comp, 'conn': a.conn, 'units': a.units, 'target': a.target}
        if reg == 'C':
            t['replay'] = suj['replay'][cond]
        out.append(t)
    return out


def nombre_registro(r):
    return '%s__%s__%s__s%03d.json' % (r['subject_id'], r['regime'], r['condition'], int(r['seed']))


def ejecutar(tareas, n_proc, salida):
    """Cada ensayo en un proceso nuevo; si un proceso muere, su recibo dice INVALIDO_TECNICO."""
    os.makedirs(salida, exist_ok=True)
    res = []
    with ProcessPoolExecutor(max_workers=max(1, int(n_proc)), mp_context=mp.get_context('spawn'),
                             max_tasks_per_child=1) as ex:
        futs = {ex.submit(ensayo, t): t for t in tareas}
        for fu in as_completed(futs):
            t = futs[fu]
            try:
                r = fu.result()
            except Exception as e:
                r = {k: t[k] for k in CAMPOS}
                r.update({'runner_version': VERSION, 'estado': 'INVALIDO_TECNICO', 'exit': 1,
                          'motivo': 'proceso caido %s: %s' % (type(e).__name__, str(e)[:300])})
            with open(os.path.join(salida, nombre_registro(r)), 'w', encoding='utf-8') as f:
                json.dump(r, f, sort_keys=True)
            print('ENSAYO %s estado=%s x=%s G=%s total=%s sha=%s seg=%s motivo=%s' % (
                C.id_ensayo(r['subject_id'], r['regime'], r['condition'], r['seed']), r['estado'], r.get('cuenta_x'),
                r.get('cuentas_G'), r.get('espigas_total'), str(r.get('espigas_sha256'))[:16], r.get('duracion_s'),
                r.get('motivo')), flush=True)
            res.append(r)
    return res


def main():
    ap = argparse.ArgumentParser(description='Productor de ensayos de 009-A1')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--ids', default='')
    for k in ('--shiu', '--comp', '--conn', '--units', '--salida'):
        ap.add_argument(k, required=True)
    ap.add_argument('--n-proc', type=int, default=2)
    ap.add_argument('--target', default='cython')
    ap.add_argument('--code-commit', default='SIN_COMMIT')
    a = ap.parse_args()
    man, sha = cargar_manifiesto(a.manifiesto, a.sha_manifiesto)
    ent = man['entradas']
    pines = {'model.py': (C.sha_archivo(os.path.join(a.shiu, 'model.py')), SHA_MODEL),
             'completeness': (C.sha_archivo(a.comp), SHA_COMP),
             'parquet': (C.sha_archivo(a.conn), ent['parquet_sha256']),
             'units_contenido': (C.huella_contenido_npz(a.units), ent['units_contenido_sha256'])}
    print('== runner_a1.py %s, manifiesto %s ==' % (VERSION, sha), flush=True)
    for k, (v, e) in pines.items():
        print('HUELLA %s %s %s' % (k, v, 'OK' if v == e else 'DISTINTA'), flush=True)
    if any(v != e for v, e in pines.values()):
        raise SystemExit(2)
    ids = list(man['humo']) if a.humo else [x for x in a.ids.split(',') if x]
    if not ids:
        raise SystemExit('ABORTA: sin ensayos')
    t0 = time.time()
    res = ejecutar(tareas_de(man, sha, ids, a), a.n_proc, a.salida)
    malos = [r for r in res if r['estado'] != 'OK']
    print('RUNNER %d/%d OK, %d INVALIDO_TECNICO, target=%s, %.1f s' % (
        len(res) - len(malos), len(res), len(malos), a.target, time.time() - t0), flush=True)
    raise SystemExit(1 if malos else 0)


if __name__ == '__main__':
    main()
