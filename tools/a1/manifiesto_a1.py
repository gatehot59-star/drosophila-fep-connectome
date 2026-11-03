#!/usr/bin/env python3
"""manifiesto_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-005).

Manifiesto de H_MECANISMO_RELEVOS16 / 009-A1 (enmienda 2026-11-02-010), escrito antes de generar actividad: indices y
roots, D' y huellas, poblaciones A, fuentes de entrada y huella de sus eventos por grupo y semilla, mascaras con filas
exactas, plan completo, humo fuera del plan, parametros y versiones. Compara todo contra los valores publicados (sello
009, tabla de hubs de 009 y JSON de salida de la evidencia de 010).
Uso: python3 manifiesto_a1.py --parquet P --units U --sello S --evid010 E --salida M.json
Exit 0 si todo coincide; 1 si una guarda difiere o hay colision de semillas; 2 si una huella de entrada difiere.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun_a1 as C  # noqa: E402

VERSION = '2026-11-03-005'
PINES = {'parquet': 'efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347',
         'units_contenido': '3e218ac3e83987b108c645341361897cb42038abdab1ca8af88d80770b24961b',
         'sello': '210b581792d183517d1e4e7771b8435e4a6acb537bc1ad383e5725c500073e93',
         'evid010': 'd5d9b7bad373c13bc240581153fbef8820e2d5587979b263a7908e76daa4eeb8'}
GUARDAS_HUB_009 = {'H1': ([3, 278], [1226, 6324]), 'H1b': ([2, 180], [1073, 5262]), 'H2': ([2, 282], [402, 2348]),
                   'H3': ([2, 243], [297, 2681]), 'H4': ([2, 198], [685, 7748]), 'H4b': ([2, 165], [575, 5662])}
HUMO_REAL = ['R01|B|C0|900', 'R01|B|SHAM|900', 'R01|B|Q1|900', 'R01|B|C0|901', 'R01|B|SHAM|901', 'R01|B|Q1|901',
             'R01|A|C0|900', 'R01|A|SHAM|900', 'H2|C|C_11|900', 'H2|C|C_desplazado|900']
LADO_REF = {'right_indice': 95123, 'left_root': 720575940604954289}


def leer_salida_010(ruta):
    texto = open(ruta, encoding='utf-8').read()
    i = texto.find('{"')
    while i != -1:
        try:
            obj, _ = json.JSONDecoder().raw_decode(texto[i:])
            if isinstance(obj, dict) and 'relay' in obj and 'joint' in obj:
                return obj
        except ValueError:
            pass
        i = texto.find('{"', i + 1)
    raise SystemExit('ABORTA: la evidencia de 010 no trae su JSON de salida')


def espec_real(sello, sal):
    rel = {e['id']: e for e in sal['relay']}
    relevos = []
    for r in sello:
        c = r['code'][:3]
        e = rel[c]
        if (int(e['driver']), int(e['hub'])) != (int(r['d_idx']), int(r['x_idx'])):
            raise SystemExit('ABORTA: sello y 010 no coinciden en %s' % c)
        q = r['guardas_filas']
        wr = e['weak_row']
        relevos.append({
            'id': c, 'codigo': r['code'], 'd': int(r['d_idx']), 'x': int(r['x_idx']), 'A_label': e['A_label'],
            'esperado': {
                'root_d': int(r['d_root']), 'root_x': int(r['x_root']),
                'Q1': [int(q['Q1']['filas']), int(q['Q1']['peso_abs'])], 'Q2': [int(q['Q2']['filas']), int(q['Q2']['peso_abs'])],
                'Q3': [int(q['Q3']['filas']), int(q['Q3']['peso_abs'])], 'Q4': [int(q['Q4']['filas']), int(q['Q4']['peso_abs'])],
                'Dp': [int(e['Dprime']['n']), e['Dprime']['sha256_indices_json_lf']],
                'QCOL': [int(v) for v in e['QCOL']], 'Q1uQCOL': [int(v) for v in e['Q1_union_QCOL']],
                'QXD': [int(v) for v in e['QXD']], 'Q1uQXD': [int(v) for v in e['Q1_union_QXD']],
                'QWEAK': [int(wr['pre']), int(wr['post']), int(wr['weight'])],
                'A': [int(e['A_population']['n']), e['A_population']['sha256_indices_json_lf']],
                'A_indices': sorted(int(v) for v in e['A_indices']) if 'A_indices' in e else None,
                'A_peso_driver': int(e['A_input_weight_to_driver']), 'lado_driver': int(e['driver_side_code'])}})
    hubs = []
    for e in sal['joint']:
        q1, q4 = GUARDAS_HUB_009[e['id']]
        wr = e['weak_row']
        hubs.append({'id': e['id'], 'x': int(e['hub']), 'G': [int(v) for v in e['drivers']],
                     'esperado': {'Dp': [int(e['Dprime']['n']), e['Dprime']['sha256_indices_json_lf']],
                                  'QCOL': [int(v) for v in e['QCOL']], 'QXD': [int(v) for v in e['QXD']],
                                  'Q1conjuQCOL': [int(v) for v in e['Q1_union_QCOL']],
                                  'Q1conjuQXD': [int(v) for v in e['Q1_union_QXD']],
                                  'QWEAK': [int(wr['pre']), int(wr['post']), int(wr['weight'])], 'Q1conj': q1, 'Q4conj': q4}})
    cs = sal['cascade_selective']
    return {'relevos': relevos, 'hubs': hubs, 'lado_codigo': {'right': 1, 'left': 0}, 'lado_ref': LADO_REF,
            'cascada': {'relevo': 'R01', 'ZA': [6128, 59804],
                        'esperado': {'ZA': [int(v) for v in cs['AVLP080_to_DNp35']], 'ZAuQ1': [int(v) for v in cs['union_Q1']]}},
            'humo': list(HUMO_REAL)}


def colisiones(grupos, semillas, fsemilla=None):
    """Toda clave distinta (grupo, s, indice, rol) debe dar una semilla distinta."""
    fs = fsemilla or C.semilla
    vistos, malas, n = {}, [], 0
    for nombre in sorted(grupos):
        for s in semillas:
            for rol, idx, _ in grupos[nombre]['fuentes']:
                k = C.texto_semilla(nombre, s, idx, rol)
                v = fs(nombre, s, idx, rol)
                n += 1
                if v in vistos and vistos[v] != k:
                    malas.append([vistos[v], k])
                vistos.setdefault(v, k)
    return {'n_claves': n, 'n_semillas_distintas': len(vistos), 'n_colisiones': len(malas), 'colisiones': malas[:10],
            'max_semilla': str(max(vistos)) if vistos else '0', 'supera_32_bits': bool(vistos) and max(vistos) >= 2 ** 32}


def construir(espec, g, u, entradas):
    """Arma el manifiesto desde la especificacion y los datos; anota cada guarda contra el valor esperado."""
    D, S, inh, sl, tipo, root = (np.asarray(u[k]) for k in ('D', 'S', 'inh', 'sl', 'tipo', 'root'))
    Dset = D >= 0
    lado = espec['lado_codigo']
    chequeos = []

    def chk(nombre, obt, esp):
        if esp is None:
            return
        chequeos.append({'nombre': nombre, 'obtenido': obt, 'esperado': esp, 'ok': bool(obt == esp)})

    def tupla(f):
        f = np.asarray(f, dtype=np.int64)
        return [int(f.size), int(np.abs(g.w[f].astype(np.int64)).sum())]

    def fila_txt(f):
        return [int(g.pre[f[0]]), int(g.post[f[0]]), int(g.w[f[0]])] if f.size else None

    sujetos, grupos, celdas = {}, {}, []

    def grupo(nombre, regimen, fuentes):
        if nombre in grupos:
            if grupos[nombre]['fuentes'] != fuentes:
                raise SystemExit('ABORTA: el grupo %s se define distinto en dos sujetos' % nombre)
            return
        grupos[nombre] = {'regimen': regimen, 'fuentes': fuentes}

    def cerrar(suj, comp):
        bases = sorted({b for v in comp.values() for b in v})
        cache = {b: C.mascara_base(b, suj, g, Dset) for b in bases}
        suj['composicion'] = comp
        suj['mascaras_base'] = {b: f.tolist() for b, f in cache.items()}
        suj['huellas_condicion'] = {c: C.huella_mascara(g, C.filas_condicion(suj, c, cache)) for c in comp}
        suj['roots'] = {str(i): int(root[i]) for i in [suj['x']] + list(suj['G'])}
        return cache

    lref = espec.get('lado_ref')
    if lref:
        chk('lado_right_indice_%d' % lref['right_indice'], int(sl[lref['right_indice']]), lado['right'])
        izq = np.flatnonzero(root == lref['left_root'])
        chk('lado_left_root_%d' % lref['left_root'], int(sl[izq[0]]) if izq.size else None, lado['left'])
    casc = espec.get('cascada')
    for R in espec['relevos']:
        sid, d, x, E = R['id'], int(R['d']), int(R['x']), R.get('esperado', {})
        Dp = C.dprime(g, Dset, x, [d])
        suj = {'clase': 'relevo', 'codigo': R.get('codigo', sid), 'd': d, 'x': x, 'G': [d], 'Dp': Dp.tolist(),
               'Dp_huella': {'n': int(Dp.size), 'sha256': C.huella_lista(Dp)}}
        comp = {c: list(v) for c, v in C.COMP_RELEVO.items()}
        conds_a = list(C.ORDEN_RELEVO)
        if casc and casc['relevo'] == sid:
            suj['cascada_ZA'] = [int(v) for v in casc['ZA']]
            comp.update({c: list(v) for c, v in C.COMP_CASCADA.items()})
            conds_a += list(C.ORDEN_CASCADA)
        lab = R['A_label']
        if lab.endswith(C.SUF_PRE):
            tipos = lab[:-len(C.SUF_PRE)].split('+')
            r = g.hacia(d)
            r = r[(g.w[r] > 0) & np.isin(tipo[g.pre[r]], tipos)]
            A = np.unique(g.pre[r]).astype(np.int64)
        else:
            t, s = lab.rsplit('_', 1)
            A = np.flatnonzero((tipo == t) & (sl == lado[s]) & (S >= 0) & (~inh)).astype(np.int64)
        suj.update({'A_label': lab, 'A': A.tolist(), 'A_huella': {'n': int(A.size), 'sha256': C.huella_lista(A)}})
        suj['mirar'] = sorted(set(Dp.tolist()) | {x, d} | set(A.tolist()) | set(suj.get('cascada_ZA', [])))
        cache = cerrar(suj, comp)
        chk(sid + ' root_d', int(root[d]), E.get('root_d'))
        chk(sid + ' root_x', int(root[x]), E.get('root_x'))
        for q in ('Q1', 'Q2', 'Q3', 'Q4', 'QCOL', 'QXD'):
            chk(sid + ' ' + q, tupla(cache[q]), E.get(q))
        chk(sid + ' Q1uQCOL', tupla(np.union1d(cache['Q1'], cache['QCOL'])), E.get('Q1uQCOL'))
        chk(sid + ' Q1uQXD', tupla(np.union1d(cache['Q1'], cache['QXD'])), E.get('Q1uQXD'))
        chk(sid + ' QWEAK', fila_txt(cache['QWEAK']), E.get('QWEAK'))
        chk(sid + ' Dp', [suj['Dp_huella']['n'], suj['Dp_huella']['sha256']], E.get('Dp'))
        chk(sid + ' A', [suj['A_huella']['n'], suj['A_huella']['sha256']], E.get('A'))
        chk(sid + ' A_indices', suj['A'], E.get('A_indices'))
        ra = g.hacia(d)
        ra = ra[np.isin(g.pre[ra], A)]
        chk(sid + ' A_peso_driver', int(np.abs(g.w[ra].astype(np.int64)).sum()), E.get('A_peso_driver'))
        chk(sid + ' lado_driver', int(sl[d]), E.get('lado_driver'))
        if 'cascada_ZA' in suj:
            ec = casc.get('esperado', {})
            chk(sid + ' ZA', tupla(cache['ZA']), ec.get('ZA'))
            chk(sid + ' ZAuQ1', tupla(np.union1d(cache['ZA'], cache['Q1'])), ec.get('ZAuQ1'))
        sujetos[sid] = suj
        ga, gb = 'A_' + lab, 'B_' + sid
        grupo(ga, 'A', [['aferente', int(j), C.TASA_A] for j in A.tolist()])
        grupo(gb, 'B', [['driver', d, C.TASA_DRIVER]] + [['blanco', int(j), C.TASA_BLANCO] for j in Dp.tolist()])
        celdas.append({'sujeto': sid, 'regimen': 'A', 'grupo': ga, 'condiciones': conds_a})
        celdas.append({'sujeto': sid, 'regimen': 'B', 'grupo': gb, 'condiciones': list(C.ORDEN_RELEVO)})
    for H in espec['hubs']:
        sid, x, G, E = H['id'], int(H['x']), [int(v) for v in H['G']], H.get('esperado', {})
        Dp = C.dprime(g, Dset, x, G)
        n = len(G)
        suj = {'clase': 'hub', 'codigo': sid, 'd': None, 'x': x, 'G': G, 'Dp': Dp.tolist(),
               'Dp_huella': {'n': int(Dp.size), 'sha256': C.huella_lista(Dp)}}
        cond_b = ['C0', 'Q2', 'Q4conj'] + ['Q1_%d' % v for v in G] + ['Q1conj']
        comp = {'C0': [], 'Q2': ['Q2'], 'Q4conj': ['Q4conj'], 'Q1conj': ['Q1conj']}
        comp.update({'Q1_%d' % v: ['Q1_%d' % v] for v in G})
        base_c = ['Q3_%d' % v for v in G] + ['Q4conj']
        cond_c, replay = [], {}
        for k in range(2 ** n):
            bits = [(k >> i) & 1 for i in range(n)]
            nombre = 'C_' + ''.join(str(b) for b in bits)
            cond_c.append(nombre)
            replay[nombre] = {'encendidos': bits, 'desplaz': [0] * n}
        cond_c.append('C_desplazado')
        replay['C_desplazado'] = {'encendidos': [1] * n, 'desplaz': list(C.DESPLAZAMIENTOS[n])}
        comp.update({c: list(base_c) for c in cond_c})
        suj['replay'] = replay
        suj['mirar'] = sorted(set(Dp.tolist()) | {x} | set(G))
        cache = cerrar(suj, comp)
        qcol = C.mascara_base('QCOL', suj, g, Dset)
        qxd = C.mascara_base('QXD', suj, g, Dset)
        chk(sid + ' Dp', [suj['Dp_huella']['n'], suj['Dp_huella']['sha256']], E.get('Dp'))
        chk(sid + ' QCOL', tupla(qcol), E.get('QCOL'))
        chk(sid + ' QXD', tupla(qxd), E.get('QXD'))
        chk(sid + ' Q1conjuQCOL', tupla(np.union1d(cache['Q1conj'], qcol)), E.get('Q1conjuQCOL'))
        chk(sid + ' Q1conjuQXD', tupla(np.union1d(cache['Q1conj'], qxd)), E.get('Q1conjuQXD'))
        chk(sid + ' QWEAK', fila_txt(C.mascara_base('QWEAK', suj, g, Dset)), E.get('QWEAK'))
        chk(sid + ' Q1conj', tupla(cache['Q1conj']), E.get('Q1conj'))
        chk(sid + ' Q4conj', tupla(cache['Q4conj']), E.get('Q4conj'))
        sujetos[sid] = suj
        gb, gc = 'B_' + sid, 'C_' + sid
        grupo(gb, 'B', [['driver', v, C.TASA_DRIVER] for v in G] + [['blanco', int(j), C.TASA_BLANCO] for j in Dp.tolist()])
        grupo(gc, 'C', [['replay', x, None]])
        celdas.append({'sujeto': sid, 'regimen': 'B', 'grupo': gb, 'condiciones': cond_b})
        celdas.append({'sujeto': sid, 'regimen': 'C', 'grupo': gc, 'condiciones': cond_c})
    semillas = list(C.SEMILLAS_PLAN) + list(C.SEMILLAS_HUMO)
    for nombre, gr in grupos.items():
        gr['eventos'] = {}
        for s in semillas:
            evs = C.eventos_grupo(nombre, s, gr['fuentes'])
            gr['eventos'][str(s)] = {'n_fuentes': len(evs), 'n_eventos': int(sum(int(e[2].size) for e in evs)),
                                     'sha256': C.huella_eventos(evs)}
    col = colisiones(grupos, semillas)
    plan = {(c['sujeto'], c['regimen']): c for c in celdas}
    humo = list(espec.get('humo', []))
    for tid in humo:
        sj, rg, cd, s = tid.split('|')
        if (sj, rg) not in plan or cd not in plan[(sj, rg)]['condiciones'] or int(s) not in C.SEMILLAS_HUMO:
            raise SystemExit('ABORTA: humo fuera del plan o con semilla del plan: %s' % tid)
    n_plan = sum(len(c['condiciones']) for c in celdas) * len(C.SEMILLAS_PLAN)
    return {'protocolo': C.PROTOCOLO, 'version': VERSION, 'entradas': entradas,
            'parametros': {'dt_s': C.DT_S, 'nticks': C.NTICKS, 'tasa_A_Hz': C.TASA_A, 'tasa_driver_Hz': C.TASA_DRIVER,
                           'tasa_blanco_Hz': C.TASA_BLANCO, 'n_replay': C.N_REPLAY,
                           'desplazamientos_ticks': {str(k): list(v) for k, v in C.DESPLAZAMIENTOS.items()},
                           'semillas_plan': list(C.SEMILLAS_PLAN), 'semillas_humo': list(C.SEMILLAS_HUMO),
                           'modelo': 'create_model() y default_params de model.py de Shiu sin cambios',
                           'entrada': 'SpikeGeneratorGroup y Synapses(on_pre v_post += w_syn*f_poi, delay 0) en el turno synapses; rfc=0 en las estimuladas',
                           'replay': 'una fuente por driver con sus filas salientes (post, peso, t_dly); filas originales de G y Q4 conjunto en cero',
                           'runtime_previsto': {'python': '3.12.14', 'numpy': '2.5.3', 'brian2': '2.10.1', 'cython': '3.1.3'}},
            'contrato_semilla': {'texto': '009-A1|grupo|s|indice|rol', 'bits': 64,
                                 'bernoulli': 'evento en el tick k si u_k < tasa_Hz*0,0001; u = Generator(PCG64(semilla)).random(10000)',
                                 'replay': '50 indices menores de argsort estable de Generator(PCG64(semilla)).random(10000), ordenados',
                                 'ejemplo': {'texto': C.texto_semilla('B_R01', 0, 59804, 'driver'),
                                             'semilla': str(C.semilla('B_R01', 0, 59804, 'driver'))},
                                 'colisiones': col},
            'sujetos': sujetos, 'grupos': grupos, 'celdas': celdas, 'n_ensayos_plan': n_plan, 'humo': humo,
            'chequeos': {'n': len(chequeos), 'ok': sum(1 for c in chequeos if c['ok']),
                         'fallas': [c['nombre'] for c in chequeos if not c['ok']], 'detalle': chequeos}}


def escribir(man, ruta):
    txt = json.dumps(man, sort_keys=True, separators=(',', ':')) + '\n'
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(txt)
    return C.sha_archivo(ruta), len(txt.encode('utf-8'))


def main():
    ap = argparse.ArgumentParser(description='Manifiesto de 009-A1')
    for k in ('--parquet', '--units', '--sello', '--evid010', '--salida'):
        ap.add_argument(k, required=True)
    a = ap.parse_args()
    t0 = time.time()
    ent = {'parquet_sha256': C.sha_archivo(a.parquet), 'units_contenido_sha256': C.huella_contenido_npz(a.units),
           'sello_sha256': C.sha_archivo(a.sello), 'evid010_sha256': C.sha_archivo(a.evid010)}
    pin = {'parquet': ent['parquet_sha256'], 'units_contenido': ent['units_contenido_sha256'],
           'sello': ent['sello_sha256'], 'evid010': ent['evid010_sha256']}
    print('== manifiesto_a1.py %s ==' % VERSION, flush=True)
    for k in sorted(pin):
        print('HUELLA %s %s %s' % (k, pin[k], 'OK' if pin[k] == PINES[k] else 'DISTINTA'), flush=True)
    print('UNITS_ARCHIVO_SHA256 %s' % C.sha_archivo(a.units), flush=True)
    if pin != PINES:
        raise SystemExit(2)
    g = C.Grafo.desde_parquet(a.parquet)
    u = {k: v for k, v in np.load(a.units).items()}
    with open(a.sello, encoding='utf-8') as f:
        sello = json.load(f)
    espec = espec_real(sello, leer_salida_010(a.evid010))
    man = construir(espec, g, u, ent)
    ch, col = man['chequeos'], man['contrato_semilla']['colisiones']
    for c in ch['detalle']:
        if not c['ok']:
            print('DIFERENTE %s obtenido=%s esperado=%s' % (c['nombre'], c['obtenido'], c['esperado']), flush=True)
    sha, nbytes = escribir(man, a.salida)
    print('CHEQUEOS %d/%d' % (ch['ok'], ch['n']), flush=True)
    print('COLISIONES %d claves=%d distintas=%d max=%s supera_32_bits=%s' % (
        col['n_colisiones'], col['n_claves'], col['n_semillas_distintas'], col['max_semilla'], col['supera_32_bits']), flush=True)
    print('PLAN sujetos=%d grupos=%d celdas=%d ensayos=%d humo=%d' % (
        len(man['sujetos']), len(man['grupos']), len(man['celdas']), man['n_ensayos_plan'], len(man['humo'])), flush=True)
    print('MANIFIESTO %s bytes=%d sha256=%s segundos=%.1f' % (a.salida, nbytes, sha, time.time() - t0), flush=True)
    raise SystemExit(0 if (ch['ok'] == ch['n'] and col['n_colisiones'] == 0) else 1)


if __name__ == '__main__':
    main()
