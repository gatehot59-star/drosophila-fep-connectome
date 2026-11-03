#!/usr/bin/env python3
"""estadistica_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-008).

Estadistica cerrada de 009-A1 segun la enmienda 010 (secciones 5 a 8). Se escribio y se probo con datos sinteticos
ANTES de abrir los recibos de la corrida 1: abrir el sobre exige --abrir-sobre, y 010 pide antes el verificador
distinto del productor. En orden:
  1. control del productor (validar_a1) sobre el plan completo; cada falla deja su celda en INVALIDO_TECNICO, y una
     falla que no se puede ubicar en una celda invalida todas;
  2. por celda (sujeto, regimen) y condicion, vectores por semilla: Y = espigas del D' fijo en 1 s (Hz
     poblacionales), H = espigas de x en 1 s, tasas de los drivers y tasas por neurona del D';
  3. contrastes por semilla: t pareada unilateral (media > 0) y, como sensibilidad, inversion de signos exacta y
     bilateral sobre los 2^20 signos;
  4. familias fijas F_B (46), F_C (6) y F_R01 (3), cada una con Holm < 0,01; lo no evaluable conserva su lugar con
     p_familia = 1;
  5. IC95 BCa con 20.000 remuestreos pareados de semillas, PCG64(2026110209), un solo flujo que se consume en orden
     lexicografico de identificador; cada id consume sus 20.000 x 20 enteros aunque su celda no se pueda calcular;
  6. activacion en B, perfil descriptivo en A, banco C (tabla ON/OFF y F_C), cascada ZA de R01, QWEAK y T3;
  7. veredictos P_T1_B y P_T2_B.
Las decisiones de implementacion donde 010 no fija el detalle estan en DECISIONES y salen en el agregado.
Uso:
  python3 estadistica_a1.py --manifiesto M --sha-manifiesto H --jsonl 'DIR/**/bloque_*.jsonl' --salida OUT --abrir-sobre
Exit 0 si el analisis termino con la validacion OK; 1 si hubo fallas tecnicas; 2 si el manifiesto no es el esperado o
falta --abrir-sobre.
"""
import argparse
import glob
import hashlib
import json
import math
import os
import re
import sys

import numpy as np
from scipy import stats
from scipy.special import ndtr, ndtri

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun_a1 as C  # noqa: E402

VERSION = '2026-11-03-008'
ALFA = 0.01
N_BOOT = 20000
SEMILLA_BOOT = 2026110209
NIVEL = 0.95
DURACION_S = C.NTICKS * C.DT_S
TASA_MIN = 10.0
TASA_OFF = 2.0
DQ2_MIN = 5.0
MARGENES = {'T1_r': 0.35, 'T1_s4': 0.50, 'T2_r': 0.40, 'T2_caida': 0.40}
RELEVOS = tuple('R%02d' % k for k in range(1, 17))
T1 = ('R01', 'R02', 'R03')
T3 = ('R06', 'R08', 'R09', 'R12')
HUBS = ('H1', 'H1b', 'H2', 'H3', 'H4', 'H4b')
TIPOS_T2 = (('CB0580', ('H1', 'H1b')), ('PS100', ('H4', 'H4b')), ('CB0534', ('H2',)), ('CB0172', ('H3',)))
BRAZOS_RELEVO = ('Q1', 'Q2', 'Q3', 'Q4', 'QCOL', 'Q1uQCOL', 'QXD', 'Q1uQXD', 'QWEAK', 'SHAM')
EFECTOS_RELEVO = tuple('D' + b for b in BRAZOS_RELEVO) + ('COL_cortado', 'COL_interaccion', 'XD_q1', 'XD_dif',
                                                           'Q1_menos_Q3')
BANDAS_WEAK = (0.05, 0.10)
PATRON_CELDA = re.compile(r'^([A-Za-z0-9]+)\|([ABC])\|')
DECISIONES = [
    'D1. Holm usa el p observado de toda prueba con datos validos y varianza no nula, tambien en casos '
    'NO_INFORMATIVO_EN_B: la activacion de B depende del Holm de F_B, y poner el centinela segun la activacion la '
    'volveria circular. El centinela p_familia = 1, con p_observado = null, queda para celdas INVALIDO_TECNICO y '
    'pruebas con varianza cero.',
    'D2. BCa: z0 con la fraccion de remuestreos menores mas la mitad de los iguales al estimado; aceleracion por '
    'jackknife de semillas; cuantiles lineales. DEGENERADO si todos los remuestreos son iguales, si z0 es infinito, '
    'si la aceleracion no esta definida o si los niveles ajustados salen de (0, 1).',
    'D3. Cociente = media(numerador) / media(denominador). Sin estimado si el denominador observado es <= 0; '
    'INDEFINIDO si algun remuestreo o algun jackknife tiene denominador <= 0.',
    'D4. El registro de ids sale solo del manifiesto. Cada id consume 20.000 x 20 enteros del flujo PCG64 en orden '
    'lexicografico, se pueda calcular o no; asi el intervalo de un id no depende de que otra celda sea invalida.',
    'D5. El IC95 de DQ2 excluye cero si su limite inferior es > 0 o su limite superior es < 0.',
    'D6. r_weak = DQWEAK / DQ2; la banda usa el |r_weak| puntual.',
    'D7. Colaterales: COL_cortado = Y(Q1uQCOL) - Y(Q1); COL_interaccion = COL_cortado - [Y(QCOL) - Y(C0)]. Ruta '
    'directa: XD_q1 = Y(Q1uQXD) - Y(QXD); XD_dif = XD_q1 - [Y(Q1) - Y(C0)].',
    'D8. En B los cocientes de la celda (r_Q1, s4, c_X, r_weak; en hubs r_Q1conj, c_Xconj, s4conj) se publican como '
    'null, con numerador, denominador, estado calculado y motivo, si la celda no queda ACTIVADO: 010 la declara no '
    'interpretable. En A cada cociente secundario exige su denominador positivo y el IC95 de ese denominador que '
    'excluya cero (DQ2 para r_Q1 y r_weak, H(C0) para c_X y s4); RECLUTADO o NO_RECLUTADO_EN_A se informa aparte y '
    'no los bloquea.',
    'D9. Veredictos conjuntos: cada unidad PASA, NO_PASA (con motivo) o queda BLOQUEADA por datos invalidos. Con k '
    'unidades requeridas: SOSTENIDA si pasan k; INVALIDO_TECNICO si las bloqueadas podrian completar k; '
    'NO_INFORMATIVO_EN_B si todas las que no pasan son no informativas; SIN_DECIDIR en el resto. Un tipo de hub PASA '
    'si pasan todas sus instancias, NO_PASA si alguna no pasa y queda BLOQUEADO si no hay NO_PASA y alguna esta '
    'bloqueada.',
    'D10. Banco C: vacio = todos los bits en 0; completo = todos en 1. INDETERMINADO si algun subconjunto queda entre '
    '2 y 10 Hz; OTRA_TRANSFERENCIA si no es OR ni AND compatible y no hay indeterminados.',
    'D11. En A, RECLUTADO exige las mismas magnitudes que la activacion de B, sin Holm ni familia A: drivers y x en '
    'C0 >= 10 Hz, DQ2 >= 5 Hz e IC95 de DQ2 que excluye cero.',
    'D12. El indice original de ablacion de 009 no se implementa: su definicion no esta en 009, ni en 010, ni en el '
    'sello 210b5817. Se publican DQ1conj, cada DQ1 individual y T2c.',
    'D13. Una falla del control del productor invalida la celda (sujeto, regimen) que nombra su detalle; una falla '
    'sin celda (archivo ilegible, code_commit mixto, validacion no OK sin detalle) invalida las 44. Un recibo que '
    'falta, se repite o no se puede leer invalida su celda.',
    'D14. Tolerancias: varianza cero si la desviacion es <= 1e-12 * max(1, |media|); en la inversion de signos, las '
    'sumas a menos de 1e-9 * (1 + suma |d|) del umbral cuentan como extremas.',
    'D15. Unidades: cada cuenta es de espigas en NTICKS * DT_S = 1 s, o sea Hz; Y en Hz poblacionales del D fijo y '
    'tasas por neurona como media de semillas. El banco C no tiene criterio de activacion: se publican la tabla '
    'ON/OFF, H_desplazado y FC. ZA1 usa la tasa del blanco de cascada_ZA, que tiene que ser un driver de R01.',
]


def _f(v):
    return None if v is None else float(v)


def json_seguro(o):
    if isinstance(o, dict):
        return {str(k): json_seguro(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [json_seguro(v) for v in o]
    if isinstance(o, np.ndarray):
        return [json_seguro(v) for v in o.tolist()]
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        x = float(o)
        return x if math.isfinite(x) else None
    return o


# ---------------------------------------------------------------- lectura de recibos


def posiciones(man):
    pos = {}
    for sid, suj in man['sujetos'].items():
        idx = {j: k for k, j in enumerate(suj['mirar'])}
        pos[sid] = np.array([idx[j] for j in suj['Dp']], dtype=np.int64)
    return pos


def tabla_vacia(man):
    n = len(C.SEMILLAS_PLAN)
    tabla = {}
    for c in man['celdas']:
        suj = man['sujetos'][c['sujeto']]
        ng, nd = len(suj['G']), len(suj['Dp'])
        tabla[(c['sujeto'], c['regimen'])] = {
            'conds': {k: {'Y': np.full(n, np.nan), 'H': np.full(n, np.nan), 'G': np.full((n, ng), np.nan),
                          'D': np.full((n, nd), np.nan)} for k in c['condiciones']},
            'problemas': []}
    return tabla


def extraer(man, regs):
    """regs: lista de (etiqueta, recibo). Arma la tabla por celda, condicion y semilla."""
    pos = posiciones(man)
    tabla = tabla_vacia(man)
    semillas = {s: k for k, s in enumerate(C.SEMILLAS_PLAN)}
    for _, r in regs:
        if not isinstance(r, dict):
            continue
        key = (r.get('subject_id'), r.get('regime'))
        t = tabla.get(key)
        if t is None or r.get('condition') not in t['conds'] or r.get('seed') not in semillas:
            continue
        suj = man['sujetos'][key[0]]
        tid = C.id_ensayo(key[0], key[1], r['condition'], r['seed'])
        cm, cg, cx = r.get('cuentas_mirar'), r.get('cuentas_G'), r.get('cuenta_x')
        if (not isinstance(cm, list) or len(cm) != len(suj['mirar']) or not isinstance(cg, list)
                or len(cg) != len(suj['G']) or not isinstance(cx, int)):
            t['problemas'].append('LECTURA ' + tid)
            continue
        e = t['conds'][r['condition']]
        k = semillas[r['seed']]
        if not np.isnan(e['Y'][k]):
            t['problemas'].append('REPETIDO ' + tid)
            continue
        d = np.asarray(cm, dtype=np.float64)[pos[key[0]]]
        e['D'][k] = d
        e['Y'][k] = d.sum()
        e['H'][k] = float(cx)
        e['G'][k] = np.asarray(cg, dtype=np.float64)
    for key, t in tabla.items():
        for cond, e in t['conds'].items():
            if np.isnan(e['Y']).any():
                t['problemas'].append('INCOMPLETO %s|%s|%s' % (key[0], key[1], cond))
    return tabla


def celdas_invalidas(validacion, tabla):
    """Ubica cada falla del control del productor en su celda; lo que no se ubica invalida todas."""
    inval, motivos, globales = set(), {}, []
    for f in validacion.get('fallos') or []:
        det = f.get('detalle')
        m = PATRON_CELDA.match(det) if isinstance(det, str) else None
        key = (m.group(1), m.group(2)) if m else None
        if key in tabla:
            inval.add(key)
            motivos.setdefault(key, []).append('%s %s' % (f.get('codigo'), det))
        else:
            globales.append('%s %s' % (f.get('codigo'), det))
    if validacion.get('estado') != 'OK' and not validacion.get('fallos'):
        globales.append('VALIDACION %s sin fallas detalladas' % validacion.get('estado'))
    if globales:
        for key in tabla:
            inval.add(key)
            motivos.setdefault(key, []).extend('GLOBAL ' + g for g in globales)
    for key, t in tabla.items():
        if t['problemas']:
            inval.add(key)
            motivos.setdefault(key, []).extend(t['problemas'])
    return inval, motivos


# ---------------------------------------------------------------- pruebas e intervalos


def t_unilateral(d):
    d = np.asarray(d, dtype=np.float64)
    n = int(d.size)
    m = float(d.mean())
    de = float(d.std(ddof=1)) if n > 1 else 0.0
    if not math.isfinite(de) or de <= 1e-12 * max(1.0, abs(m)):
        return {'n': n, 'media': m, 'de': de, 't': None, 'gl': n - 1, 'p': None, 'estado': 'VARIANZA_CERO'}
    t = m / (de / math.sqrt(n))
    return {'n': n, 'media': m, 'de': de, 't': t, 'gl': n - 1, 'p': float(stats.t.sf(t, n - 1)), 'estado': 'OK'}


def _sumas_signos(v):
    k = v.size
    if k == 0:
        return np.zeros(1)
    signos = ((np.arange(2 ** k, dtype=np.int64)[:, None] >> np.arange(k)) & 1) * 2 - 1
    return signos @ v


def signos_bilateral(d):
    """Inversion de signos exacta y bilateral: fraccion de los 2^n signos con |suma| >= |suma observada|."""
    d = np.asarray(d, dtype=np.float64)
    n = d.size
    umbral = abs(float(d.sum())) - 1e-9 * (1.0 + float(np.abs(d).sum()))
    if umbral <= 0:
        return 1.0
    h = n // 2
    a = _sumas_signos(d[:h])
    b = np.sort(_sumas_signos(d[h:]))
    altos = b.size - np.searchsorted(b, umbral - a, side='left')
    bajos = np.searchsorted(b, -umbral - a, side='right')
    return float((int(altos.sum()) + int(bajos.sum())) / 2.0 ** n)


def holm(p):
    p = np.asarray(p, dtype=np.float64)
    m = p.size
    orden = np.argsort(p, kind='stable')
    adj = np.empty(m)
    acum = 0.0
    for rango, i in enumerate(orden):
        acum = max(acum, min(1.0, (m - rango) * p[i]))
        adj[i] = acum
    return adj


def _bca(theta, estrellas, jack, nivel=NIVEL):
    if not (np.all(np.isfinite(estrellas)) and np.all(np.isfinite(jack))):
        return None, 'DEGENERADO'
    if np.all(estrellas == estrellas[0]):
        return None, 'DEGENERADO'
    b = estrellas.size
    p0 = (np.count_nonzero(estrellas < theta) + np.count_nonzero(estrellas <= theta)) / (2.0 * b)
    if p0 <= 0.0 or p0 >= 1.0:
        return None, 'DEGENERADO'
    z0 = float(ndtri(p0))
    jm = float(jack.mean())
    den = 6.0 * float(np.sum((jm - jack) ** 2)) ** 1.5
    if not den > 0:
        return None, 'DEGENERADO'
    acel = float(np.sum((jm - jack) ** 3)) / den
    zs = ndtri(np.array([(1.0 - nivel) / 2.0, 1.0 - (1.0 - nivel) / 2.0]))
    base = 1.0 - acel * (z0 + zs)
    if np.any(base <= 0):
        return None, 'DEGENERADO'
    niveles = ndtr(z0 + (z0 + zs) / base)
    if not (np.all(np.isfinite(niveles)) and 0.0 < niveles[0] < niveles[1] < 1.0):
        return None, 'DEGENERADO'
    lo, hi = np.quantile(estrellas, niveles)
    return [float(lo), float(hi)], 'OK'


def evaluar(cant, idx):
    """cant: ('media', a) o ('cociente', a, b), vectores por semilla. idx: (B, n) indices de semillas."""
    n = cant[1].size
    if cant[0] == 'media':
        a = cant[1]
        theta = float(a.mean())
        ic, estado = _bca(theta, a[idx].mean(axis=1), (a.sum() - a) / (n - 1))
        return {'tipo': 'media', 'estimado': theta, 'ic95': ic, 'estado_ic': estado}
    a, b = cant[1], cant[2]
    ma, mb = float(a.mean()), float(b.mean())
    out = {'tipo': 'cociente', 'numerador': ma, 'denominador': mb}
    if not mb > 0:
        out.update(estimado=None, ic95=None, estado_ic='SIN_ESTIMADO', motivo='denominador no positivo (%.6g)' % mb)
        return out
    theta = ma / mb
    out['estimado'] = theta
    mbs = b[idx].mean(axis=1)
    jb = (b.sum() - b) / (n - 1)
    if np.any(mbs <= 0) or np.any(jb <= 0):
        out.update(ic95=None, estado_ic='INDEFINIDO', motivo='hay remuestreos con denominador no positivo')
        return out
    ic, estado = _bca(theta, a[idx].mean(axis=1) / mbs, ((a.sum() - a) / (n - 1)) / jb)
    out.update(ic95=ic, estado_ic=estado)
    return out


# ---------------------------------------------------------------- registro de cantidades


def cantidades_celda(c, suj, conds, margenes):
    """Cantidades de una celda. Con conds=None devuelve los mismos nombres con valor None."""
    n = len(C.SEMILLAS_PLAN)
    nulo = conds is None

    def Y(k):
        return np.zeros(n) if nulo else conds[k]['Y'] / DURACION_S

    def H(k):
        return np.zeros(n) if nulo else conds[k]['H'] / DURACION_S

    def G(k, i):
        return np.zeros(n) if nulo else conds[k]['G'][:, i] / DURACION_S

    sid, reg = c['sujeto'], c['regimen']
    q = {}
    if suj['clase'] == 'relevo':
        y0, h0 = Y('C0'), H('C0')
        for b in BRAZOS_RELEVO:
            q['D' + b] = ('media', Y(b) - y0)
        dq1, dq2 = Y('Q1') - y0, Y('Q2') - y0
        q['r_Q1'] = ('cociente', dq1, dq2)
        q['c_X'] = ('cociente', h0 - H('Q1'), h0)
        q['s4'] = ('cociente', H('Q4'), h0)
        q['r_weak'] = ('cociente', Y('QWEAK') - y0, dq2)
        q['COL_cortado'] = ('media', Y('Q1uQCOL') - Y('Q1'))
        q['COL_interaccion'] = ('media', (Y('Q1uQCOL') - Y('Q1')) - (Y('QCOL') - y0))
        q['XD_q1'] = ('media', Y('Q1uQXD') - Y('QXD'))
        q['XD_dif'] = ('media', (Y('Q1uQXD') - Y('QXD')) - dq1)
        q['Q1_menos_Q3'] = ('media', Y('Q1') - Y('Q3'))
        q['HC0'] = ('media', h0)
        if reg == 'B' and sid in T1:
            q['T1a'] = ('media', dq1 - margenes['T1_r'] * dq2)
            q['T1b'] = ('media', H('Q4') - margenes['T1_s4'] * h0)
        if reg == 'A' and 'ZA' in c['condiciones']:
            za = suj.get('cascada_ZA')
            if not za or za[1] not in suj['G']:
                raise SystemExit('ABORTA: %s no tiene cascada_ZA con su blanco entre los drivers' % sid)
            iz = suj['G'].index(za[1])
            q['ZA1'] = ('media', G('ZA', iz) - G('C0', iz))
            q['ZA2'] = ('media', (H('ZA') - h0) - (H('ZAuQ1') - H('Q1')))
            q['ZA3'] = ('media', (Y('ZAuQ1uQCOL') - Y('Q1uQCOL')) - (Y('ZAuQCOL') - Y('QCOL')))
    elif reg == 'B':
        y0, h0 = Y('C0'), H('C0')
        dq2, dqc = Y('Q2') - y0, Y('Q1conj') - y0
        q['DQ2'] = ('media', dq2)
        q['DQ4conj'] = ('media', Y('Q4conj') - y0)
        q['DQ1conj'] = ('media', dqc)
        ind = []
        for g in suj['G']:
            v = Y('Q1_%d' % g) - y0
            q['DQ1_%d' % g] = ('media', v)
            ind.append(v)
        q['r_Q1conj'] = ('cociente', dqc, dq2)
        q['c_Xconj'] = ('cociente', h0 - H('Q1conj'), h0)
        q['s4conj'] = ('cociente', H('Q4conj'), h0)
        q['T2a'] = ('media', dqc - margenes['T2_r'] * dq2)
        q['T2b'] = ('media', (h0 - H('Q1conj')) - margenes['T2_caida'] * h0)
        q['T2c'] = ('media', dqc - np.mean(ind, axis=0))
    else:
        q['FC'] = ('media', H('C_' + '1' * len(suj['G'])) - H('C_desplazado'))
    if nulo:
        return {k: None for k in q}
    return q


def registro(man, tabla, invalidas, margenes):
    cant = {}
    for c in man['celdas']:
        key = (c['sujeto'], c['regimen'])
        conds = None if key in invalidas else tabla[key]['conds']
        for k, v in cantidades_celda(c, man['sujetos'][c['sujeto']], conds, margenes).items():
            cant['%s|%s|%s' % (c['regimen'], c['sujeto'], k)] = v
    return cant


def intervalos(cant, n_boot=N_BOOT, semilla=SEMILLA_BOOT):
    rng = np.random.Generator(np.random.PCG64(semilla))
    n = len(C.SEMILLAS_PLAN)
    out = {}
    for qid in sorted(cant):
        idx = rng.integers(0, n, size=(n_boot, n))
        out[qid] = None if cant[qid] is None else evaluar(cant[qid], idx)
    return out


def ids_familias():
    fb = (['B|%s|DQ2' % r for r in RELEVOS] + ['B|%s|DQ2' % h for h in HUBS]
          + ['B|%s|T1%s' % (r, x) for r in T1 for x in 'ab'] + ['B|%s|T2%s' % (h, x) for h in HUBS for x in 'abc'])
    return {'F_B': fb, 'F_C': ['C|%s|FC' % h for h in HUBS], 'F_R01': ['A|R01|ZA%d' % k for k in (1, 2, 3)]}


def familias(cant):
    out = {}
    for nombre, ids in ids_familias().items():
        filas = []
        for pid in ids:
            if pid not in cant:
                raise SystemExit('ABORTA: la prueba %s no esta en el registro' % pid)
            q = cant[pid]
            if q is None:
                filas.append({'id': pid, 'estado': 'INVALIDO_TECNICO', 'n': None, 'media': None, 'de': None, 't': None,
                              'gl': None, 'p_observado': None, 'p_familia': 1.0, 'signos_bilateral': None})
                continue
            t = t_unilateral(q[1])
            filas.append({'id': pid, 'estado': t['estado'], 'n': t['n'], 'media': t['media'], 'de': t['de'],
                          't': t['t'], 'gl': t['gl'], 'p_observado': t['p'],
                          'p_familia': 1.0 if t['p'] is None else t['p'], 'signos_bilateral': signos_bilateral(q[1])})
        adj = holm([f['p_familia'] for f in filas])
        for f, a in zip(filas, adj):
            f['p_holm'] = float(a)
            f['decide'] = bool(f['estado'] == 'OK' and a < ALFA)
        out[nombre] = {'m': len(ids), 'alfa': ALFA, 'n_deciden': int(sum(f['decide'] for f in filas)), 'pruebas': filas}
    return out


# ---------------------------------------------------------------- lectura por celda


def medias_celda(conds):
    out = {}
    for k, e in conds.items():
        out[k] = {'Y_Hz': float(np.mean(e['Y'])) / DURACION_S, 'H_Hz': float(np.mean(e['H'])) / DURACION_S,
                  'G_Hz': [float(v) / DURACION_S for v in np.mean(e['G'], axis=0)]}
    return out


def fracciones_c0(conds):
    if 'C0' not in conds:
        return None
    tn = np.mean(conds['C0']['D'], axis=0) / DURACION_S
    return {'n_Dp': int(tn.size), 'frac_C0_le_2Hz': float(np.mean(tn <= TASA_OFF)),
            'frac_C0_gt_10Hz': float(np.mean(tn > TASA_MIN))}


def excluye_cero(q):
    """D5: un IC95 calculado (estado OK) excluye cero si su limite inferior es > 0 o el superior es < 0."""
    return bool(q is not None and q.get('estado_ic') == 'OK' and q.get('ic95') is not None
                and (q['ic95'][0] > 0 or q['ic95'][1] < 0))


def activacion(reg, conds, iv_dq2, prueba_dq2):
    g0 = np.mean(conds['C0']['G'], axis=0) / DURACION_S
    x0 = float(np.mean(conds['C0']['H'])) / DURACION_S
    est, ic = iv_dq2['estimado'], iv_dq2['ic95']
    medido = {'drivers_C0_Hz': [float(v) for v in g0], 'x_C0_Hz': x0, 'DQ2_Hz': est, 'IC95_DQ2': ic,
              'IC95_DQ2_estado': iv_dq2['estado_ic']}
    ok = {'drivers_C0_ge_10Hz': bool(np.all(g0 >= TASA_MIN)), 'x_C0_ge_10Hz': bool(x0 >= TASA_MIN),
          'DQ2_ge_5Hz': bool(est >= DQ2_MIN), 'IC95_DQ2_excluye_0': excluye_cero(iv_dq2)}
    if reg == 'B':
        medido['DQ2_p_holm_F_B'] = prueba_dq2['p_holm']
        ok['DQ2_F_B_holm_lt_001'] = bool(prueba_dq2['decide'])
    causas = [k for k, v in ok.items() if not v]
    if reg == 'B':
        estado = 'ACTIVADO' if not causas else 'NO_INFORMATIVO_EN_B'
    else:
        estado = 'RECLUTADO' if not causas else 'NO_RECLUTADO_EN_A'
    return {'estado': estado, 'medido': medido, 'criterios': ok, 'causas': causas}


def cociente(iv, publicar, motivo, margen=None):
    out = dict(iv)
    out['estado_ic_calculado'] = iv.get('estado_ic')
    if not publicar:
        out.update(estimado=None, ic95=None, estado_ic='NULO', motivo=motivo)
    if margen is not None:
        ok = out.get('estado_ic') == 'OK'
        out['margen'] = margen
        out['limite_inferior_supera_margen'] = bool(ok and out['ic95'][0] > margen)
        out['intervalo_contradice'] = bool(ok and out['ic95'][1] < margen)
    return out


def banda_weak(r):
    a = abs(r)
    return 'PEQUENO' if a < BANDAS_WEAK[0] else ('INTERMEDIO' if a < BANDAS_WEAK[1] else 'ALTO')


def resumen_relevo(c, conds, iv, fam, margenes):
    sid, reg = c['sujeto'], c['regimen']
    pre = '%s|%s|' % (reg, sid)
    act = activacion(reg, conds, iv[pre + 'DQ2'], fam.get(pre + 'DQ2'))
    activo = act['estado'] in ('ACTIVADO', 'RECLUTADO')
    es_t1 = reg == 'B' and sid in T1
    if reg == 'B':
        motivo = '' if activo else 'B %s: %s' % (act['estado'], ', '.join(act['causas']))
        pub = {k: (activo, motivo) for k in ('r_Q1', 's4', 'c_X', 'r_weak')}
    else:
        freno, base = excluye_cero(iv[pre + 'DQ2']), excluye_cero(iv[pre + 'HC0'])
        mf = '' if freno else 'A: el IC95 de DQ2, su denominador, no excluye cero'
        mb = '' if base else 'A: el IC95 de H(C0), su denominador, no excluye cero'
        pub = {'r_Q1': (freno, mf), 'r_weak': (freno, mf), 'c_X': (base, mb), 's4': (base, mb)}
    r = {'estado': act['estado'], 'activacion': act, 'medias': medias_celda(conds), 'fracciones': fracciones_c0(conds),
         'efectos': {k: iv[pre + k] for k in EFECTOS_RELEVO}, 'H_C0': iv[pre + 'HC0'],
         'cocientes': {'r_Q1': cociente(iv[pre + 'r_Q1'], *pub['r_Q1'], margen=margenes['T1_r'] if es_t1 else None),
                       's4': cociente(iv[pre + 's4'], *pub['s4'], margen=margenes['T1_s4'] if es_t1 else None),
                       'c_X': cociente(iv[pre + 'c_X'], *pub['c_X']),
                       'r_weak': cociente(iv[pre + 'r_weak'], *pub['r_weak'])}}
    rw = r['cocientes']['r_weak']['estimado']
    r['qweak'] = {'banda': None if rw is None else banda_weak(rw), 'DQWEAK_Hz': iv[pre + 'DQWEAK']['estimado'],
                  'nota': '' if rw is not None else 'denominador no informativo: se reporta solo DQWEAK'}
    if es_t1:
        crit = {'activado': activo, 'T1a_F_B': bool(fam[pre + 'T1a']['decide']),
                'T1b_F_B': bool(fam[pre + 'T1b']['decide']),
                'r_Q1_ic_sobre_margen': r['cocientes']['r_Q1']['limite_inferior_supera_margen'],
                's4_ic_sobre_margen': r['cocientes']['s4']['limite_inferior_supera_margen']}
        if all(crit.values()):
            est = 'PASA'
        else:
            est = 'NO_PASA:NO_INFORMATIVO_EN_B' if not activo else 'NO_PASA:SIN_DECIDIR'
        r['T1'] = {'estado': est, 'criterios': crit, 'pruebas': {k: fam[pre + k] for k in ('T1a', 'T1b')},
                   'intervalos': {k: iv[pre + k] for k in ('T1a', 'T1b')}}
    if reg == 'A' and 'ZA' in c['condiciones']:
        r['cascada_ZA'] = {k: iv[pre + k] for k in ('ZA1', 'ZA2', 'ZA3')}
    return r


def resumen_hub_b(c, suj, conds, iv, fam, margenes):
    pre = 'B|%s|' % c['sujeto']
    act = activacion('B', conds, iv[pre + 'DQ2'], fam[pre + 'DQ2'])
    activo = act['estado'] == 'ACTIVADO'
    motivo = '' if activo else '%s: %s' % (act['estado'], ', '.join(act['causas']))
    nombres = ['DQ2', 'DQ4conj', 'DQ1conj'] + ['DQ1_%d' % g for g in suj['G']] + ['T2c']
    r = {'estado': act['estado'], 'activacion': act, 'medias': medias_celda(conds), 'fracciones': fracciones_c0(conds),
         'efectos': {k: iv[pre + k] for k in nombres},
         'cocientes': {'r_Q1conj': cociente(iv[pre + 'r_Q1conj'], activo, motivo, margenes['T2_r']),
                       'c_Xconj': cociente(iv[pre + 'c_Xconj'], activo, motivo, margenes['T2_caida']),
                       's4conj': cociente(iv[pre + 's4conj'], activo, motivo)}}
    ic_c = iv[pre + 'T2c']
    crit = {'activado': activo, 'T2a_F_B': bool(fam[pre + 'T2a']['decide']),
            'T2b_F_B': bool(fam[pre + 'T2b']['decide']), 'T2c_F_B': bool(fam[pre + 'T2c']['decide']),
            'r_Q1conj_ic_sobre_margen': r['cocientes']['r_Q1conj']['limite_inferior_supera_margen'],
            'c_Xconj_ic_sobre_margen': r['cocientes']['c_Xconj']['limite_inferior_supera_margen'],
            'c_ic_sobre_0': bool(ic_c['estado_ic'] == 'OK' and ic_c['ic95'][0] > 0)}
    if all(crit.values()):
        est = 'PASA'
    else:
        est = 'NO_PASA:NO_INFORMATIVO_EN_B' if not activo else 'NO_PASA:SIN_DECIDIR'
    r['T2'] = {'estado': est, 'criterios': crit, 'pruebas': {k: fam[pre + k] for k in ('T2a', 'T2b', 'T2c')},
               'intervalos': {k: iv[pre + k] for k in ('T2a', 'T2b', 'T2c')}}
    return r


def resumen_hub_c(c, suj, conds, iv, fam):
    pre = 'C|%s|' % c['sujeto']
    ng = len(suj['G'])
    tabla = {}
    for k in c['condiciones']:
        if k == 'C_desplazado':
            continue
        h = float(np.mean(conds[k]['H'])) / DURACION_S
        tabla[k] = {'H_Hz': h, 'etiqueta': 'ON' if h >= TASA_MIN else ('OFF' if h <= TASA_OFF else 'IND')}
    vacio, lleno = 'C_' + '0' * ng, 'C_' + '1' * ng
    if any(v['etiqueta'] == 'IND' for v in tabla.values()):
        transf = 'INDETERMINADO'
    elif tabla[vacio]['etiqueta'] == 'OFF' and all(v['etiqueta'] == 'ON' for k, v in tabla.items() if k != vacio):
        transf = 'OR_COMPATIBLE_EN_C'
    elif tabla[lleno]['etiqueta'] == 'ON' and all(v['etiqueta'] == 'OFF' for k, v in tabla.items() if k != lleno):
        transf = 'AND_COMPATIBLE_EN_C'
    else:
        transf = 'OTRA_TRANSFERENCIA'
    p = fam[pre + 'FC']
    return {'estado': 'VALIDO', 'tabla_ON_OFF': tabla, 'transferencia': transf,
            'H_desplazado_Hz': float(np.mean(conds['C_desplazado']['H'])) / DURACION_S,
            'FC': {'estado': 'SOSTENIDA' if p['decide'] else 'SIN_DECIDIR', 'prueba': p, 'intervalo': iv[pre + 'FC'],
                   'lectura': 'sensibilidad temporal en C' if p['decide'] else ''}}


def combinar(unidades, k):
    estados = list(unidades.values())
    n_pasa = sum(1 for e in estados if e == 'PASA')
    n_bloq = sum(1 for e in estados if e == 'BLOQUEADO')
    if n_pasa >= k:
        return 'SOSTENIDA'
    if n_pasa + n_bloq >= k:
        return 'INVALIDO_TECNICO'
    no = [e for e in estados if e.startswith('NO_PASA')]
    if no and all(e == 'NO_PASA:NO_INFORMATIVO_EN_B' for e in no):
        return 'NO_INFORMATIVO_EN_B'
    return 'SIN_DECIDIR'


def estado_tipo(estados):
    if all(e == 'PASA' for e in estados):
        return 'PASA'
    no = [e for e in estados if e.startswith('NO_PASA')]
    if no:
        return 'NO_PASA:NO_INFORMATIVO_EN_B' if all(e == 'NO_PASA:NO_INFORMATIVO_EN_B' for e in no) else \
            'NO_PASA:SIN_DECIDIR'
    return 'BLOQUEADO'


def analizar(man, tabla, invalidas, motivos, n_boot=N_BOOT, semilla=SEMILLA_BOOT, margenes=None):
    margenes = dict(MARGENES if margenes is None else margenes)
    cant = registro(man, tabla, invalidas, margenes)
    iv = intervalos(cant, n_boot, semilla)
    fams = familias(cant)
    fam = {f['id']: f for v in fams.values() for f in v['pruebas']}
    casos, tasas = {}, []
    for c in man['celdas']:
        key = (c['sujeto'], c['regimen'])
        nombre = '%s|%s' % (c['regimen'], c['sujeto'])
        suj = man['sujetos'][c['sujeto']]
        if key in invalidas:
            casos[nombre] = {'estado': 'INVALIDO_TECNICO', 'motivos': list(motivos.get(key, []))}
            continue
        conds = tabla[key]['conds']
        if suj['clase'] == 'relevo':
            casos[nombre] = resumen_relevo(c, conds, iv, fam, margenes)
        elif c['regimen'] == 'B':
            casos[nombre] = resumen_hub_b(c, suj, conds, iv, fam, margenes)
        else:
            casos[nombre] = resumen_hub_c(c, suj, conds, iv, fam)
        for k in c['condiciones']:
            tn = np.mean(conds[k]['D'], axis=0) / DURACION_S
            tasas.extend((c['regimen'], c['sujeto'], k, int(j), float(v)) for j, v in zip(suj['Dp'], tn))
    u1 = {r: ('BLOQUEADO' if casos['B|' + r]['estado'] == 'INVALIDO_TECNICO' else casos['B|' + r]['T1']['estado'])
          for r in T1}
    inst = {h: ('BLOQUEADO' if casos['B|' + h]['estado'] == 'INVALIDO_TECNICO' else casos['B|' + h]['T2']['estado'])
            for h in HUBS}
    tipos = {t: estado_tipo([inst[h] for h in hs]) for t, hs in TIPOS_T2}
    fc = {h: ('INVALIDO_TECNICO' if casos['C|' + h]['estado'] == 'INVALIDO_TECNICO' else casos['C|' + h]['FC']['estado'])
          for h in HUBS}
    za = {k: fam['A|R01|ZA%d' % k] for k in (1, 2, 3)}
    if casos['A|R01']['estado'] == 'INVALIDO_TECNICO':
        firma = 'INVALIDO_TECNICO'
    else:
        firma = 'SOSTENIDA' if all(p['decide'] for p in za.values()) else 'SIN_DECIDIR'
    t3 = {}
    for r in T3:
        for reg in ('B', 'A'):
            cs = casos['%s|%s' % (reg, r)]
            t3['%s|%s' % (reg, r)] = {'estado': cs['estado']} if cs['estado'] == 'INVALIDO_TECNICO' else {
                'estado': cs['estado'], 'r_Q1': cs['cocientes']['r_Q1']['estimado'],
                's4': cs['cocientes']['s4']['estimado'], 'c_X': cs['cocientes']['c_X']['estimado'],
                'DQ2_Hz': cs['efectos']['DQ2']['estimado']}
    qweak = {}
    for r in RELEVOS:
        for reg in ('B', 'A'):
            cs = casos['%s|%s' % (reg, r)]
            qweak['%s|%s' % (reg, r)] = None if cs['estado'] == 'INVALIDO_TECNICO' else cs['qweak']
    veredictos = {
        'P_T1_B': {'veredicto': combinar(u1, 3), 'casos': u1, 'requiere': 'R01, R02 y R03'},
        'P_T2_B': {'veredicto': combinar(tipos, 3), 'tipos': tipos, 'instancias': inst, 'requiere': '3 de 4 tipos'},
        'F_C': fc,
        'F_R01': {'firma': firma, 'contrastes': {('ZA%d' % k): bool(p['decide']) for k, p in za.items()}},
        'T3': t3, 'QWEAK': qweak,
        'P_ESTRATOS': 'RETIRADA_COMO_PRIMARIA_EN_A1 (010, seccion 8): no se evalua'}
    res = {'protocolo': C.PROTOCOLO, 'version': VERSION,
           'parametros': {'alfa': ALFA, 'n_boot': n_boot, 'semilla_boot': semilla, 'nivel': NIVEL,
                          'duracion_s': DURACION_S, 'tasa_min_Hz': TASA_MIN, 'tasa_off_Hz': TASA_OFF,
                          'dq2_min_Hz': DQ2_MIN, 'margenes': margenes, 'bandas_weak': list(BANDAS_WEAK)},
           'decisiones': DECISIONES, 'invalidas': sorted('%s|%s' % (k[1], k[0]) for k in invalidas),
           'familias': fams, 'casos': casos, 'veredictos': veredictos, 'intervalos': iv}
    return json_seguro(res), tasas


def correr(man, sha_man, regs, validacion, n_boot=N_BOOT, semilla=SEMILLA_BOOT, margenes=None):
    tabla = extraer(man, regs)
    inval, motivos = celdas_invalidas(validacion, tabla)
    res, tasas = analizar(man, tabla, inval, motivos, n_boot, semilla, margenes)
    por_codigo = {}
    for f in validacion.get('fallos') or []:
        por_codigo[f.get('codigo')] = por_codigo.get(f.get('codigo'), 0) + 1
    res['manifiesto_sha256'] = sha_man
    res['validacion'] = json_seguro({'estado': validacion.get('estado'), 'n_registros': validacion.get('n_registros'),
                                     'n_esperados': validacion.get('n_esperados'),
                                     'n_fallos': validacion.get('n_fallos'), 'por_codigo': por_codigo})
    return res, tasas


def lineas_resumen(res):
    out = []
    v = res.get('validacion') or {}
    out.append('ESTADISTICA_A1 version=%s n_boot=%s semilla=%s alfa=%s' % (
        res['version'], res['parametros']['n_boot'], res['parametros']['semilla_boot'], res['parametros']['alfa']))
    out.append('VALIDACION %s registros=%s esperados=%s fallos=%s invalidas=%d' % (
        v.get('estado'), v.get('n_registros'), v.get('n_esperados'), v.get('n_fallos'), len(res['invalidas'])))
    for nombre, f in res['familias'].items():
        out.append('FAMILIA %s m=%d deciden=%d alfa=%s' % (nombre, f['m'], f['n_deciden'], f['alfa']))
        for p in f['pruebas']:
            out.append('PRUEBA %s %s estado=%s media=%s t=%s p=%s holm=%s decide=%s signos=%s' % (
                nombre, p['id'], p['estado'], p['media'], p['t'], p['p_observado'], p['p_holm'],
                'SI' if p['decide'] else 'NO', p['signos_bilateral']))
    for nombre, cs in sorted(res['casos'].items()):
        out.append('CASO %s %s' % (nombre, cs['estado']))
    ver = res['veredictos']
    out.append('VEREDICTO P_T1_B %s casos=%s' % (ver['P_T1_B']['veredicto'], json.dumps(ver['P_T1_B']['casos'],
                                                                                         sort_keys=True)))
    out.append('VEREDICTO P_T2_B %s tipos=%s' % (ver['P_T2_B']['veredicto'], json.dumps(ver['P_T2_B']['tipos'],
                                                                                       sort_keys=True)))
    for h, e in ver['F_C'].items():
        out.append('VEREDICTO F_C %s %s' % (h, e))
    out.append('VEREDICTO F_R01 firma=%s contrastes=%s' % (ver['F_R01']['firma'],
                                                          json.dumps(ver['F_R01']['contrastes'], sort_keys=True)))
    return out


def main():
    ap = argparse.ArgumentParser(description='Estadistica cerrada de 009-A1 (010, secciones 5 a 8)')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--jsonl', required=True)
    ap.add_argument('--salida', required=True)
    ap.add_argument('--abrir-sobre', action='store_true')
    a = ap.parse_args()
    if not a.abrir_sobre:
        print('ABORTA: abrir el sobre es un acto explicito (--abrir-sobre); 010 pide antes el verificador', flush=True)
        raise SystemExit(2)
    sha = C.sha_archivo(a.manifiesto)
    if sha != a.sha_manifiesto:
        print('ABORTA: el manifiesto tiene sha256 %s y se esperaba %s' % (sha, a.sha_manifiesto), flush=True)
        raise SystemExit(2)
    with open(a.manifiesto, encoding='utf-8') as f:
        man = json.load(f)
    import juntar_a1 as J
    import plan_a1 as P
    import validar_a1 as V
    regs, entradas = [], []
    for ruta in sorted(glob.glob(a.jsonl, recursive=True)):
        filas = J.leer_jsonl(ruta)
        regs.extend(filas)
        entradas.append({'archivo': os.path.basename(ruta), 'lineas': len(filas), 'sha256': C.sha_archivo(ruta)})
    v = V.validar(man, sha, regs, P.ids_plan(man))
    res, tasas = correr(man, sha, regs, v)
    res['entradas'] = entradas
    with open(os.path.abspath(__file__), 'rb') as f:
        res['codigo_sha256'] = hashlib.sha256(f.read()).hexdigest()
    os.makedirs(a.salida, exist_ok=True)
    with open(os.path.join(a.salida, 'agregado_a1.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, sort_keys=True, indent=1, allow_nan=False)
    with open(os.path.join(a.salida, 'tasas_por_neurona.csv'), 'w', encoding='utf-8') as f:
        f.write('regimen,sujeto,condicion,neurona,tasa_media_Hz\n')
        for fila in tasas:
            f.write('%s,%s,%s,%d,%.6f\n' % fila)
    lineas = lineas_resumen(res)
    with open(os.path.join(a.salida, 'estadistica_a1.log'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas) + '\n')
    for linea in lineas:
        print(linea, flush=True)
    raise SystemExit(0 if v['estado'] == 'OK' else 1)


if __name__ == '__main__':
    main()
