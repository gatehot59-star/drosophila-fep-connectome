#!/usr/bin/env python3
"""sobre_sintetico_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-009).

Sobre SINTETICO de 009-A1 para el ensayo general del verificador independiente (010, seccion 9). Arma los 8.540
recibos del plan con el esquema de runner_a1.py: identidad, D', huellas de mascara y eventos copiados del manifiesto
real, y cuentas de un modelo sembrado con efectos conocidos (tablas BASE y CAMBIOS). Ningun recibo sale de una
simulacion: todos llevan "sintetico": true y code_commit SINTETICO-009, y el generador se niega a escribir en una
ruta que contenga 'corrida_'.

Escenarios:
  limpio  todos los recibos validos; cada rama de 010 tiene al menos una celda sembrada (CAMBIOS).
  sucio   las mismas cuentas mas 13 corrupciones que el control del productor detecta y 6 que no detecta.
  global  las mismas cuentas mas una linea ilegible, que segun D13 invalida las 44 celdas.

Las cuentas solo usan Generator(PCG64).random(): no dependen de como cada version de NumPy muestrea Poisson o
binomiales. La semilla de cada celda no depende del escenario, asi limpio, sucio y global comparten las cuentas.

Uso: python3 sobre_sintetico_a1.py --manifiesto M --sha-manifiesto H --escenario limpio|sucio|global --salida DIR
Escribe DIR/bloques/KK/bloque_KK.jsonl con el reparto de plan_a1.repartir (el de la corrida real), DIR/SHA256SUMS.txt
y DIR/SEMBRADO.json (parametros por celda, corrupciones y el codigo que cada una deberia disparar).
Exit 0 si escribio; 2 si el manifiesto no es el esperado, el escenario no existe o la ruta parece de una corrida real.
"""
import argparse
import copy
import hashlib
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun_a1 as C  # noqa: E402
import plan_a1 as P  # noqa: E402

VERSION = '2026-11-03-009'
CODE_COMMIT = 'SINTETICO-009'
RUNNER = 'SINTETICO-2026-11-03-009'
SEMILLA = 20261103009
N_BLOQUES = 20
ESCENARIOS = ('limpio', 'sucio', 'global')

# Tasas en Hz por neurona (lD, lx, lG), saltos de desinhibicion por neurona del D' (d2) y fracciones de cada brazo.
BASE = {
    ('relevo', 'B'): {'lD': 12.0, 'lx': 30.0, 'lG': 50.0, 'd2': 6.0, 'r1': 0.75, 'c1': 0.9, 's4': 0.9, 'rw': 0.02,
                      'col': 0.1, 'xd': 0.95},
    ('relevo', 'A'): {'lD': 8.0, 'lx': 30.0, 'lG': 20.0, 'd2': 4.0, 'r1': 0.75, 'c1': 0.9, 's4': 0.9, 'rw': 0.02,
                      'col': 0.1, 'xd': 0.95},
    ('hub', 'B'): {'lD': 12.0, 'lx': 30.0, 'lG': 50.0, 'd2': 6.0, 'rc': 0.75, 'cc': 0.8, 'ri': 0.3, 's4': 0.9},
    ('hub', 'C'): {'lD': 10.0, 'lG': 20.0, 'tipo': 'OR', 'lon': 25.0, 'lfull': 30.0, 'desp': 0.4},
}
CAMBIOS = {
    ('R02', 'B'): ({'trampa': True}, 'Q1 apaga a x en las 20 semillas: Y(Q1) = Y(Q2) por semilla y r_Q1 = 1 exacto'),
    ('R05', 'B'): ({'d2': 0.05}, 'freno chico: DQ2 por debajo de 5 Hz, NO_INFORMATIVO_EN_B'),
    ('R06', 'B'): ({'lG': 4.0}, 'driver a 4 Hz en C0: NO_INFORMATIVO_EN_B'),
    ('R09', 'B'): ({'rw': 0.07}, 'QWEAK intermedio'),
    ('R10', 'B'): ({'rw': 0.20}, 'QWEAK alto'),
    ('R12', 'B'): ({'r1': 0.20}, 'freno de Q1 chico en un relevo T3: el IC de r_Q1 queda debajo de 0,35'),
    ('R05', 'A'): ({'d2': 0.0}, 'sin freno: NO_RECLUTADO_EN_A y r_Q1 nulo'),
    ('R06', 'A'): ({'lx': 0.0}, 'x mudo: H(C0) = 0, c_X y s4 sin estimado'),
    ('R07', 'A'): ({'d2': -3.0}, 'freno negativo: DQ2 < 0 y r_Q1 sin estimado'),
    ('H3', 'B'): ({'trampa': True}, 'Q1conj apaga a x: r_Q1conj y c_Xconj = 1 exactos en todo remuestreo'),
    ('H1b', 'C'): ({'tipo': 'AND'}, 'banco C compatible con AND'),
    ('H2', 'C'): ({'tipo': 'IND'}, 'un subconjunto a 6 Hz: INDETERMINADO'),
    ('H3', 'C'): ({'tipo': 'OTRA'}, 'un parcial OFF y otro ON: OTRA_TRANSFERENCIA'),
    ('H4', 'C'): ({'tipo': 'FC0'}, 'desplazado identico al completo: FC con varianza cero'),
}
# (ensayo, tipo, codigos que deberia dar validar_a1); la celda que queda invalida es la del ensayo
DETECTABLES = [
    ('R04|B|QXD|7', 'falta', ['FALTANTE']),
    ('R05|A|Q2|3', 'duplicado', ['DUPLICADO']),
    ('R06|B|SHAM|11', 'sham_distinto', ['SHAM_DISTINTO_DE_C0']),
    ('R07|A|Q3|5', 'eventos_distintos', ['EVENTOS', 'ENTRADA_DESIGUAL']),
    ('R08|B|QCOL|0', 'mascara', ['MASCARA']),
    ('H3|B|Q2|12', 'estado_tecnico', ['ESTADO_TECNICO', 'LECTURA']),
    ('R09|A|C0|2', 'identidad', ['IDENTIDAD']),
    ('H1|C|C_101|4', 'dprime', ['DPRIME']),
    ('R10|B|Q4|9', 'protocolo', ['PROTOCOLO']),
    ('R11|A|QWEAK|15', 'manifiesto', ['MANIFIESTO']),
    ('R12|B|Q3|19', 'chequeo', ['CHEQUEO_INTERNO']),
    ('R13|A|Q1|8', 'lectura', ['LECTURA']),
    ('R14|B|C0|0', 'fuera_de_seleccion', ['FUERA_DE_SELECCION']),
]
# Corrupciones que el control del productor (validar_a1) no mira: huecos que el verificador tiene que cubrir.
CIEGAS = [
    ('R15|B|Q1|6', 'x_incoherente', 'cuenta_x no coincide con cuentas_mirar en la posicion de x'),
    ('R16|A|Q4|10', 'cuenta_negativa', 'una cuenta del D\' vale -3'),
    ('H4b|B|C0|1', 'runner_version', 'runner_version distinto del resto'),
    ('H2|C|C_11|13', 'input_hashes', 'input_hashes no coincide con las entradas del manifiesto'),
    ('H4|C|C_10|17', 'G_incoherente', 'cuentas_G no coincide con cuentas_mirar en la posicion del driver'),
    ('R12|A|Q4|14', 'total_bajo', 'espigas_total menor que la suma de cuentas_mirar'),
]
CUENTAS = ('cuentas_mirar', 'cuenta_x', 'cuentas_G', 'espigas_total', 'activas', 'espigas_sha256', 'mirar_huella',
           'duracion_sim_s', 'entorno')


def semilla_texto(*partes):
    return int(hashlib.sha256('|'.join(str(p) for p in partes).encode('utf-8')).hexdigest()[:16], 16)


def sha_texto(*partes):
    return hashlib.sha256('|'.join(str(p) for p in partes).encode('utf-8')).hexdigest()


class Azar:
    """Solo Generator(PCG64).random(). cuentas ~ Poisson aproximado por Irwin-Hall; fino = adelgazado con redondeo."""

    def __init__(self, *partes):
        self.g = np.random.Generator(np.random.PCG64(semilla_texto(SEMILLA, *partes)))

    def u(self, forma):
        return self.g.random(forma)

    def cuentas(self, lam):
        lam = np.maximum(np.asarray(lam, dtype=np.float64), 0.0)
        z = (self.u(lam.shape + (4,)).sum(axis=-1) - 2.0) * math.sqrt(3.0)
        return np.maximum(0, np.floor(lam + np.sqrt(lam) * z + 0.5)).astype(np.int64)

    def fino(self, c, p):
        c = np.asarray(c, dtype=np.int64)
        p = min(1.0, max(0.0, float(p)))
        return np.clip(np.floor(c * p + self.u(c.shape)), 0, c).astype(np.int64)


def parametros(suj, reg, sid):
    par = dict(BASE[(suj['clase'], reg)])
    cambio = CAMBIOS.get((sid, reg))
    if cambio:
        par.update(cambio[0])
    return par


def modelo_celda(c, suj, par):
    """Cuentas por condicion: D (semillas x D'), H (semillas) y G (semillas x drivers), en 1 s, o sea en Hz."""
    sid, reg = c['sujeto'], c['regimen']
    az = Azar(sid, reg)
    n, nd, ng = len(C.SEMILLAS_PLAN), len(suj['Dp']), len(suj['G'])
    u = 1.0 + 0.1 * (az.u(n) - 0.5) * math.sqrt(12.0)
    ud, ug = u[:, None] * np.ones((1, nd)), u[:, None] * np.ones((1, ng))
    cero = np.zeros(n, dtype=np.int64)
    D0 = az.cuentas(par['lD'] * ud)
    G0 = az.cuentas(par['lG'] * ug)
    Q = {}
    if reg == 'C':
        vacio, lleno = 'C_' + '0' * ng, 'C_' + '1' * ng
        parciales = sorted(k for k in c['condiciones'] if k not in (vacio, lleno, 'C_desplazado'))
        tipo = par['tipo']
        for k in c['condiciones']:
            if k == 'C_desplazado':
                continue
            if k == lleno:
                tasa = par['lfull']
            elif k == vacio:
                tasa = 0.5 if tipo == 'AND' else 0.0
            elif tipo == 'AND' or (tipo == 'OTRA' and k == parciales[0]):
                tasa = 0.5
            elif tipo == 'IND' and k == parciales[0]:
                tasa = 6.0
            else:
                tasa = par['lon']
            Q[k] = (az.cuentas(par['lD'] * ud), az.cuentas(tasa * u), G0.copy())
        D1, H1, G1 = Q[lleno]
        Q['C_desplazado'] = ((D1.copy(), H1.copy(), G1.copy()) if tipo == 'FC0'
                             else (D1.copy(), az.fino(H1, par['desp']), G0.copy()))
        return Q
    H0 = az.cuentas(par['lx'] * u)

    def mas(f, base=None):
        b = D0 if base is None else base
        delta = f * par['d2']
        if delta >= 0:
            return b + az.cuentas(delta * ud)
        return az.fino(b, 1.0 + delta / par['lD'])

    trampa = bool(par.get('trampa'))
    Q['C0'] = (D0, H0, G0)
    D2 = mas(1.0)
    Q['Q2'] = (D2, H0.copy(), G0.copy())
    if suj['clase'] == 'hub':
        Q['Q4conj'] = (mas(0.1), az.fino(H0, par['s4']), G0.copy())
        Q['Q1conj'] = ((D2.copy(), cero.copy(), G0.copy()) if trampa
                       else (mas(par['rc']), az.fino(H0, 1.0 - par['cc']), G0.copy()))
        for g in suj['G']:
            Q['Q1_%d' % g] = (mas(par['ri']), az.fino(H0, 0.7), G0.copy())
        return Q
    Q['Q1'] = ((D2.copy(), cero.copy(), G0.copy()) if trampa
               else (mas(par['r1']), az.fino(H0, 1.0 - par['c1']), G0.copy()))
    Q['Q3'] = (mas(0.8), cero.copy(), G0.copy())
    Q['Q4'] = (mas(0.1), az.fino(H0, par['s4']), G0.copy())
    Q['QCOL'] = (az.fino(D0, 1.0 - par['col']), H0.copy(), G0.copy())
    Q['Q1uQCOL'] = (az.fino(Q['Q1'][0], 1.0 - par['col']), Q['Q1'][1].copy(), G0.copy())
    Q['QXD'] = (mas(par['xd']), H0.copy(), G0.copy())
    Q['Q1uQXD'] = (Q['QXD'][0] + az.cuentas(0.02 * abs(par['d2']) * ud), Q['Q1'][1].copy(), G0.copy())
    Q['QWEAK'] = (mas(par['rw']), H0.copy(), G0.copy())
    Q['SHAM'] = (D0.copy(), H0.copy(), G0.copy())
    if 'ZA' in c['condiciones']:
        iz = suj['G'].index(suj['cascada_ZA'][1])
        extra = az.cuentas(0.5 * par['lG'] * u)
        hza = az.cuentas(0.3 * par['lx'] * u)

        def gza():
            g = G0.copy()
            g[:, iz] += extra
            return g

        Q['ZA'] = (az.fino(D0, 0.9), H0 + hza, gza())
        Q['ZAuQ1'] = (Q['Q1'][0].copy(), Q['Q1'][1].copy(), gza())
        Q['ZAuQCOL'] = (az.fino(Q['QCOL'][0], 0.9), Q['QCOL'][1] + hza, gza())
        Q['ZAuQ1uQCOL'] = (Q['Q1uQCOL'][0].copy(), Q['Q1uQCOL'][1].copy(), gza())
    return Q


def posiciones(suj):
    idx = {int(j): k for k, j in enumerate(suj['mirar'])}
    pd = np.array([idx[int(j)] for j in suj['Dp']], dtype=np.int64)
    pg = np.array([idx[int(j)] for j in suj['G']], dtype=np.int64)
    px = idx[int(suj['x'])]
    usadas = set(pd.tolist()) | set(pg.tolist()) | {px}
    pj = np.array([k for k in range(len(suj['mirar'])) if k not in usadas], dtype=np.int64)
    return pd, pg, px, pj


def recibos_celda(man, sha, c, suj, esc):
    """Los 20 x condiciones recibos de una celda, con las huellas tecnicas del manifiesto."""
    sid, reg = c['sujeto'], c['regimen']
    par = parametros(suj, reg, sid)
    Q = modelo_celda(c, suj, par)
    pd, pg, px, pj = posiciones(suj)
    if set(pd.tolist()) & (set(pg.tolist()) | {px}):
        raise SystemExit('ABORTA: %s tiene x o un driver dentro del D\'' % sid)
    azj = Azar('basura', sid, reg)
    basura = {}
    for k, cond in enumerate(c['condiciones']):
        if cond != 'SHAM':
            basura[cond] = azj.cuentas(np.full((len(C.SEMILLAS_PLAN), pj.size), 3.0 + 2.0 * k))
    basura['SHAM'] = basura.get('C0')
    out = {}
    for cond in c['condiciones']:
        D, H, G = Q[cond]
        hc = suj['huellas_condicion'][cond]
        for i, s in enumerate(C.SEMILLAS_PLAN):
            v = np.zeros(len(suj['mirar']), dtype=np.int64)
            v[pj] = basura[cond][i]
            v[pd] = D[i]
            v[pg] = G[i]
            v[px] = H[i]
            etiqueta = 'C0' if cond == 'SHAM' else cond
            hx = sha_texto('SINTETICO', sid, reg, s, etiqueta)
            ev = man['grupos'][c['grupo']]['eventos'][str(s)]
            r = {'protocol_id': C.PROTOCOLO, 'code_commit': CODE_COMMIT, 'manifiesto_sha256': sha, 'subject_id': sid,
                 'regime': reg, 'condition': cond, 'seed': int(s), 'grupo': c['grupo'], 'runner_version': RUNNER,
                 'input_hashes': dict(man['entradas']), 'estado': 'OK', 'motivo': '', 'exit': 0,
                 'chequeos': {k: True for k in ('identidad', 'Dprime', 'mascara', 'eventos', 'fuentes',
                                                'orden_sinapsis', 'signo_pesos')},
                 'identidad': {'x': int(suj['x']), 'd': suj.get('d'), 'G': [int(g) for g in suj['G']],
                               'roots': dict(suj['roots'])},
                 'Dprime_hash': suj['Dp_huella']['sha256'], 'Dprime_n': suj['Dp_huella']['n'],
                 'mask_hash': hc['sha256'], 'mask_n': hc['n'], 'mask_abs': hc['abs'],
                 'input_events_hash': ev['sha256'], 'n_input_events': ev['n_eventos'], 'duracion_sim_s': 0.0,
                 'mirar_huella': C.huella_lista(suj['mirar']), 'cuentas_mirar': [int(t) for t in v],
                 'cuenta_x': int(v[px]), 'cuentas_G': [int(v[p]) for p in pg],
                 'espigas_total': int(v.sum()) + 1000 + int(hx[:4], 16) % 1000,
                 'activas': int(np.count_nonzero(v)) + 200 + int(hx[4:8], 16) % 100,
                 'espigas_sha256': sha_texto('SINTETICO', sid, reg, s, etiqueta, ','.join(map(str, v.tolist()))),
                 'entorno': {'brian2': 'SINTETICO', 'numpy': 'SINTETICO', 'python': 'SINTETICO',
                             'target_pedido': 'sintetico', 'codeobj': None, 'dt_s': C.DT_S, 't_run_s': 1.0},
                 'duracion_s': 0.0, 'sintetico': True, 'escenario': esc}
            if cond != 'C0':
                r['chequeos'].update(pesos_fuera_intactos=True, mascara_en_cero=True)
                r['filas_cambiadas'] = hc['n']
            if reg == 'C':
                r['replay_aplicado_hash'] = sha_texto('SINTETICO', 'replay', sid, cond, s)
            out[C.id_ensayo(sid, reg, cond, s)] = r
    return out, par


def corromper(man, recs, tid, tipo):
    """Aplica una corrupcion; devuelve los recibos extra que haya que agregar al bloque de la celda."""
    r = recs[tid]
    suj = man['sujetos'][r['subject_id']]
    malo = sha_texto('ADULTERADO', tid, tipo)
    if tipo == 'falta':
        del recs[tid]
    elif tipo == 'duplicado':
        return [copy.deepcopy(r)]
    elif tipo == 'sham_distinto':
        r['espigas_sha256'] = malo
    elif tipo == 'eventos_distintos':
        r['input_events_hash'] = malo
    elif tipo == 'mascara':
        r['mask_hash'] = malo
    elif tipo == 'estado_tecnico':
        for k in CUENTAS:
            r.pop(k, None)
        r.update(estado='INVALIDO_TECNICO', exit=1, motivo='excepcion RuntimeError: falla sintetica del ensayo general')
    elif tipo == 'identidad':
        r['identidad']['roots'][str(suj['x'])] += 1
    elif tipo == 'dprime':
        r['Dprime_hash'] = malo
    elif tipo == 'protocolo':
        r['protocol_id'] = '009-A0'
    elif tipo == 'manifiesto':
        r['manifiesto_sha256'] = '0' * 64
    elif tipo == 'chequeo':
        r['chequeos']['signo_pesos'] = False
    elif tipo == 'lectura':
        r['cuentas_mirar'] = r['cuentas_mirar'][:-1]
    elif tipo == 'fuera_de_seleccion':
        e = copy.deepcopy(r)
        ev = man['grupos'][e['grupo']]['eventos']['900']
        e.update(seed=900, input_events_hash=ev['sha256'], n_input_events=ev['n_eventos'],
                 espigas_sha256=sha_texto('SINTETICO', 'humo', tid))
        return [e]
    elif tipo == 'x_incoherente':
        r['cuenta_x'] += 7
    elif tipo == 'cuenta_negativa':
        pd = posiciones(suj)[0]
        r['cuentas_mirar'][int(pd[0])] = -3
    elif tipo == 'runner_version':
        r['runner_version'] = 'OTRA-VERSION'
    elif tipo == 'input_hashes':
        r['input_hashes']['parquet_sha256'] = '0' * 64
    elif tipo == 'G_incoherente':
        r['cuentas_G'][0] += 5
    elif tipo == 'total_bajo':
        r['espigas_total'] = int(sum(r['cuentas_mirar'])) - 1
    else:
        raise SystemExit('ABORTA: corrupcion desconocida %s' % tipo)
    return []


def generar(man, sha, esc, salida):
    if 'corrida_' in os.path.abspath(salida).lower():
        print('ABORTA: %s parece la ruta de una corrida real; el sobre sintetico no va ahi' % salida, flush=True)
        raise SystemExit(2)
    recs, pars = {}, {}
    for c in man['celdas']:
        r, par = recibos_celda(man, sha, c, man['sujetos'][c['sujeto']], esc)
        recs.update(r)
        pars['%s|%s' % (c['sujeto'], c['regimen'])] = par
    extras = {}
    corr = []
    if esc == 'sucio':
        for tid, tipo, codigos in DETECTABLES:
            extras.setdefault(tid, []).extend(corromper(man, recs, tid, tipo))
            corr.append({'ensayo': tid, 'tipo': tipo, 'celda': '|'.join(tid.split('|')[:2]),
                         'codigos_productor': codigos, 'detecta_el_control_del_productor': True})
        for tid, tipo, nota in CIEGAS:
            extras.setdefault(tid, []).extend(corromper(man, recs, tid, tipo))
            corr.append({'ensayo': tid, 'tipo': tipo, 'celda': '|'.join(tid.split('|')[:2]), 'codigos_productor': [],
                         'detecta_el_control_del_productor': False, 'nota': nota})
    bloques = P.repartir(man['celdas'], N_BLOQUES)
    sumas, lineas = [], 0
    for k, ids in enumerate(bloques):
        filas = []
        for t in ids:
            for r in ([recs[t]] if t in recs else []) + extras.get(t, []):
                filas.append((C.id_ensayo(r['subject_id'], r['regime'], r['condition'], r['seed']),
                              json.dumps(r, sort_keys=True)))
        filas.sort()
        texto = ''.join(f + '\n' for _, f in filas)
        if esc == 'global' and k == 7:
            texto += '{"subject_id": "R01", "linea": "rota a proposito\n'
            corr.append({'ensayo': None, 'tipo': 'ilegible', 'celda': None, 'codigos_productor': ['ILEGIBLE'],
                         'detecta_el_control_del_productor': True, 'nota': 'linea final de bloque_07 sin cerrar'})
        rel = 'bloques/%02d/bloque_%02d.jsonl' % (k, k)
        ruta = os.path.join(salida, rel)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
            f.write(texto)
        sumas.append((C.sha_archivo(ruta), rel))
        lineas += texto.count('\n')
    with open(os.path.join(salida, 'SHA256SUMS.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join('%s  %s\n' % s for s in sumas))
    sembrado = {'protocolo': C.PROTOCOLO, 'version': VERSION, 'escenario': esc, 'sintetico': True,
                'manifiesto_sha256': sha, 'n_lineas': lineas, 'code_commit': CODE_COMMIT, 'semilla': SEMILLA,
                'base': {'%s|%s' % k: v for k, v in BASE.items()},
                'cambios': {'%s|%s' % k: {'parametros': v[0], 'por_que': v[1]} for k, v in CAMBIOS.items()},
                'parametros_por_celda': pars, 'corrupciones': corr,
                'bloques': [{'archivo': rel, 'sha256': h} for h, rel in sumas]}
    with open(os.path.join(salida, 'SEMBRADO.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(sembrado, f, sort_keys=True, indent=1)
        f.write('\n')
    print('SOBRE_SINTETICO escenario=%s lineas=%d bloques=%d corrupciones=%d sha256sums=%s' % (
        esc, lineas, len(sumas), len(corr), C.sha_archivo(os.path.join(salida, 'SHA256SUMS.txt'))), flush=True)
    return sembrado


def main():
    ap = argparse.ArgumentParser(description='Sobre sintetico de 009-A1 para el ensayo general del verificador')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--escenario', required=True)
    ap.add_argument('--salida', required=True)
    a = ap.parse_args()
    if a.escenario not in ESCENARIOS:
        print('ABORTA: escenario %s; los validos son %s' % (a.escenario, ', '.join(ESCENARIOS)), flush=True)
        raise SystemExit(2)
    sha = C.sha_archivo(a.manifiesto)
    if sha != a.sha_manifiesto:
        print('ABORTA: el manifiesto tiene sha256 %s y se esperaba %s' % (sha, a.sha_manifiesto), flush=True)
        raise SystemExit(2)
    with open(a.manifiesto, encoding='utf-8') as f:
        man = json.load(f)
    generar(man, sha, a.escenario, a.salida)
    raise SystemExit(0)


if __name__ == '__main__':
    main()
