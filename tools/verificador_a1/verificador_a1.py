#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificador independiente de 009-A1 (orden 2026-11-03-009, respuesta 2026-11-03-010).

Fases
  E  manifiesto y plan, sin leer recibos.
  T  recibos: integridad, lectura, cobertura, huellas, pareado, unicidad,
     coherencia interna y entorno. No calcula estimandos ni imprime cuentas.
  S  estadistica de 010 seccion 7 con motores de scipy (bootstrap BCa pareado,
     ttest_1samp) y una inversion de signos exacta propia; D1 a D15 del anexo A.
  K  cotejo con agregado_a1.json del productor; cada diferencia con su clase.

Autoria y alcance
  Lo escribio BRAIN el 3-nov-2026, despues de que Abraham pidiera seguir sin
  rodeos (20:47 ART). La orden 009 pedia otro agente: este archivo cambia eso y
  lo declara. La independencia de EJECUCION es del instrumento (W-01): no
  importa ni copia nada de tools/a1 y usa motores distintos. La de SELECCION
  (que medir) no la da: queda como deuda y la orden 009 sigue vigente para una
  auditoria externa.

Seguridad del sobre
  Con una ruta que contenga "corrida_", o con recibos sin "sintetico": true,
  las fases T, S y K exigen --abrir-sobre. Ninguna fase imprime cuentas, y los
  veredictos solo salen por pantalla si todos los recibos son sinteticos.

Uso
  python3 verificador_a1.py --manifiesto M --sha-manifiesto SHA --salida DIR
      [--sobre SOBRE] [--agregado-productor A] [--fases ETSK] [--abrir-sobre]

  Con --fases K (sin S) se usa el verificador_a1.json ya escrito en DIR: es el
  paso 5 de la apertura (orden 009, seccion 8), despues de commitear la fase S.

Salidas en DIR
  verificacion_tecnica.json  fases E y T
  registro_ids.txt           los 722 ids, uno por linea
  verificador_a1.json        fase S con la regla de invalidez propia
  verificador_a1_espejo.json fase S con las celdas invalidas del productor
                             (solo si difieren; aisla el cotejo numerico)
  cotejo_a1.json             fase K

Salida del proceso
  0 todo lo pedido corrio, sin fallas tecnicas y sin diferencias sin clasificar
  1 corrio, pero con fallas tecnicas o cotejo DISCORDANTE
  2 se nego a correr (pin del manifiesto, ruta del sobre, uso)

Dependencias: Python 3.12, numpy y scipy. Las versiones salen en cada archivo.
"""

import argparse
import glob
import hashlib
import json
import math
import os
import platform
import sys
import time
import warnings
from collections import Counter, defaultdict

import numpy as np
import scipy
from scipy import special, stats

VERSION = '2026-11-03-010'
PROTOCOLO = '009-A1'
N = 20
SEMILLAS = tuple(range(N))
DURACION_S = 1.0
N_BOOT = 20000
SEMILLA_BOOT = 2026110209
NIVEL = 0.95
ALFA = 0.01
TASA_MIN_HZ = 10.0
TASA_OFF_HZ = 2.0
DQ2_MIN_HZ = 5.0
MARGEN_T1_R = 0.35
MARGEN_T1_S4 = 0.50
MARGEN_T2_R = 0.40
MARGEN_T2_CAIDA = 0.40
BANDAS_WEAK = (0.05, 0.10)
TOL_VARIANZA = 1e-12
TOL_SIGNOS = 1e-9
TOL_K_INTERVALO = 1e-9
TOL_K_PRUEBA = 1e-12
MAX_DIFERENCIAS_ESCRITAS = 2000

# Listas de 010 y del anexo B de la orden 009, no de plan_a1.
RELEVOS = tuple('R%02d' % i for i in range(1, 17))
HUBS = ('H1', 'H1b', 'H2', 'H3', 'H4', 'H4b')
REGIMENES = {'relevo': ('A', 'B'), 'hub': ('B', 'C')}
T1_RELEVOS = ('R01', 'R02', 'R03')
T3_RELEVOS = ('R06', 'R08', 'R09', 'R12')  # estrato T3 del diseno 009 (seccion de estratos)
TIPOS_HUB = (('CB0580', ('H1', 'H1b')), ('PS100', ('H4', 'H4b')), ('CB0534', ('H2',)), ('CB0172', ('H3',)))
COND_RELEVO = ('C0', 'Q1', 'Q2', 'Q3', 'Q4', 'QCOL', 'Q1uQCOL', 'QXD', 'Q1uQXD', 'QWEAK', 'SHAM')
COND_ZA = ('ZA', 'ZAuQ1', 'ZAuQCOL', 'ZAuQ1uQCOL')
CHEQUEOS_BASE = ('identidad', 'Dprime', 'mascara', 'eventos', 'fuentes', 'orden_sinapsis', 'signo_pesos')
CHEQUEOS_FUERA_C0 = ('pesos_fuera_intactos', 'mascara_en_cero')
CAMPOS_SHAM = ('espigas_sha256', 'cuentas_mirar', 'espigas_total', 'cuenta_x', 'cuentas_G')
COCIENTES_RELEVO = ('r_Q1', 'c_X', 's4', 'r_weak')
COCIENTES_HUB = ('r_Q1conj', 'c_Xconj', 's4conj')
EFECTOS_EXTRA = ('COL_cortado', 'COL_interaccion', 'XD_q1', 'XD_dif', 'Q1_menos_Q3')

# ----------------------------------------------------------------------------
# Utilidades


def sha256_archivo(ruta):
    h = hashlib.sha256()
    with open(ruta, 'rb') as f:
        for trozo in iter(lambda: f.read(1 << 20), b''):
            h.update(trozo)
    return h.hexdigest()


def sha256_texto(texto):
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()


def huella(valores):
    """Formato de la orden 009, seccion 5.1, con implementacion propia."""
    return sha256_texto(json.dumps(sorted(int(v) for v in valores), separators=(',', ':')) + '\n')


def canonico(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def es_entero(v):
    return isinstance(v, int) and not isinstance(v, bool)


def escribir_json(ruta, obj):
    texto = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1, allow_nan=False) + '\n'
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(texto)
    return sha256_texto(texto)


def condiciones_de(sujeto_id, regimen, sujeto):
    """Condiciones de una celda segun las listas de 010 (orden 009, fase E)."""
    if sujeto_id in RELEVOS:
        conds = list(COND_RELEVO)
        if sujeto_id == 'R01' and regimen == 'A':
            conds += list(COND_ZA)
        return conds
    if regimen == 'B':
        return ['C0', 'Q2', 'Q4conj'] + ['Q1_%d' % g for g in sujeto['G']] + ['Q1conj']
    k = len(sujeto['G'])
    subconj = ['C_' + ''.join('1' if (m >> j) & 1 else '0' for j in range(k)) for m in range(2 ** k)]
    return subconj + ['C_desplazado']


def nombres_de(sujeto_id, regimen, sujeto):
    """Cantidades de una celda segun el anexo B de la orden 009."""
    if sujeto_id in RELEVOS:
        nombres = ['D' + b for b in COND_RELEVO[1:]] + list(COCIENTES_RELEVO) + list(EFECTOS_EXTRA) + ['HC0']
        if regimen == 'B' and sujeto_id in T1_RELEVOS:
            nombres += ['T1a', 'T1b']
        if regimen == 'A' and sujeto_id == 'R01':
            nombres += ['ZA1', 'ZA2', 'ZA3']
        return nombres
    if regimen == 'B':
        return (['DQ2', 'DQ4conj', 'DQ1conj'] + ['DQ1_%d' % g for g in sujeto['G']]
                + list(COCIENTES_HUB) + ['T2a', 'T2b', 'T2c'])
    return ['FC']


def ids_familia(nombre):
    if nombre == 'F_B':
        ids = ['B|%s|DQ2' % s for s in RELEVOS] + ['B|%s|DQ2' % h for h in HUBS]
        ids += ['B|%s|%s' % (s, t) for s in T1_RELEVOS for t in ('T1a', 'T1b')]
        ids += ['B|%s|%s' % (h, t) for h in HUBS for t in ('T2a', 'T2b', 'T2c')]
        return ids
    if nombre == 'F_C':
        return ['C|%s|FC' % h for h in HUBS]
    return ['A|R01|ZA1', 'A|R01|ZA2', 'A|R01|ZA3']


FAMILIAS = ('F_B', 'F_C', 'F_R01')

# ----------------------------------------------------------------------------
# Fase E


def fase_E(ruta_man, sha_pin):
    sha = sha256_archivo(ruta_man)
    res = {'manifiesto': os.path.basename(ruta_man), 'sha256': sha, 'sha_pin': sha_pin,
           'fallas': [], 'notas': []}
    if sha != sha_pin:
        res['fallas'].append({'codigo': 'PIN_MANIFIESTO', 'detalle': 'el sha256 no es el del pin'})
        res['estado'] = 'PARADA'
        return res, None, None, None
    with open(ruta_man, 'rb') as f:
        man = json.loads(f.read().decode('utf-8'))
    fallas = res['fallas']

    def falla(codigo, detalle):
        fallas.append({'codigo': codigo, 'detalle': detalle})

    if man.get('protocolo') != PROTOCOLO:
        falla('PROTOCOLO', 'protocolo del manifiesto distinto de 009-A1')
    sujetos = man.get('sujetos', {})
    esperados = set(RELEVOS) | set(HUBS)
    if set(sujetos) != esperados:
        falla('SUJETOS', 'sobran o faltan: %s' % sorted(set(sujetos) ^ esperados))
    plan = {}
    vistas = Counter()
    grupos = man.get('grupos', {})
    for c in man.get('celdas', []):
        s_id, reg = c.get('sujeto'), c.get('regimen')
        clave = '%s|%s' % (reg, s_id)
        vistas[clave] += 1
        if s_id not in sujetos:
            falla('CELDA', '%s: sujeto ausente' % clave)
            continue
        suj = sujetos[s_id]
        clase = 'relevo' if s_id in RELEVOS else 'hub'
        if suj.get('clase') != clase:
            falla('CLASE', '%s: clase %r, 010 dice %s' % (s_id, suj.get('clase'), clase))
        if reg not in REGIMENES[clase]:
            falla('CELDA', '%s: regimen fuera de 010' % clave)
            continue
        esperadas = condiciones_de(s_id, reg, suj)
        dadas = c.get('condiciones', [])
        if sorted(dadas) != sorted(esperadas) or len(set(dadas)) != len(dadas):
            falla('CONDICIONES', '%s: no coinciden con las listas de 010' % clave)
        g = c.get('grupo')
        grp = grupos.get(g)
        if grp is None:
            falla('GRUPO', '%s: grupo %s ausente' % (clave, g))
        else:
            if grp.get('regimen') != reg:
                falla('GRUPO', '%s: el grupo %s es de otro regimen' % (clave, g))
            ev = grp.get('eventos', {})
            for s in SEMILLAS:
                e = ev.get(str(s))
                if not isinstance(e, dict) or not isinstance(e.get('sha256'), str) or len(e['sha256']) != 64:
                    falla('EVENTOS', '%s: semilla %d sin huella de eventos' % (clave, s))
        plan[clave] = {'sujeto': s_id, 'regimen': reg, 'grupo': g, 'condiciones': esperadas}
    celdas_010 = ({'%s|%s' % (r, s) for s in RELEVOS for r in ('A', 'B')}
                  | {'%s|%s' % (r, h) for h in HUBS for r in ('B', 'C')})
    if set(vistas) != celdas_010 or any(v != 1 for v in vistas.values()):
        falla('CELDAS', 'las celdas del manifiesto no son las 44 de 010')
    n_cond = sum(len(p['condiciones']) for p in plan.values())
    res['conteo'] = {'celdas': len(plan), 'condiciones': n_cond, 'ensayos': n_cond * N,
                     'n_ensayos_plan': man.get('n_ensayos_plan')}
    if (len(plan), n_cond, n_cond * N) != (44, 427, 8540) or man.get('n_ensayos_plan') != 8540:
        falla('CONTEO', 'no da 44 celdas, 427 condiciones y 8.540 ensayos')
    for s_id in sorted(sujetos):
        suj = sujetos[s_id]
        mirar, dp, x, g_ = suj.get('mirar', []), suj.get('Dp', []), suj.get('x'), suj.get('G', [])
        pm = set(mirar)
        if len(pm) != len(mirar):
            falla('MIRAR', '%s: mirar tiene repetidos' % s_id)
        if not set(dp) <= pm or x not in pm or not set(g_) <= pm:
            falla('MIRAR', '%s: D\', x o G fuera de mirar' % s_id)
        if set(dp) & ({x} | set(g_)):
            falla('DPRIME', '%s: D\' contiene a x o a un driver' % s_id)
        hu = suj.get('Dp_huella', {})
        if len(dp) != hu.get('n') or huella(dp) != hu.get('sha256'):
            falla('DPRIME', '%s: Dp_huella no coincide con Dp' % s_id)
        if list(dp) != sorted(dp):
            res['notas'].append('%s: Dp no viene ordenado (no cambia Y)' % s_id)
        hc = suj.get('huellas_condicion', {})
        for clave, p in plan.items():
            if p['sujeto'] == s_id:
                faltan = [cc for cc in p['condiciones'] if not isinstance(hc.get(cc), dict)]
                if faltan:
                    falla('MASCARA', '%s: %d condiciones sin huella de mascara' % (clave, len(faltan)))
        if s_id == 'R01':
            za = suj.get('cascada_ZA')
            if not (isinstance(za, list) and len(za) == 2 and za[1] in g_):
                falla('CASCADA_ZA', 'R01: cascada_ZA[1] no es un driver de R01 (D15)')
    registro = sorted('%s|%s|%s' % (p['regimen'], p['sujeto'], n)
                      for p in plan.values() for n in nombres_de(p['sujeto'], p['regimen'], sujetos[p['sujeto']]))
    res['registro'] = {'n': len(registro), 'sha256': sha256_texto('\n'.join(registro) + '\n')}
    if len(registro) != 722 or len(set(registro)) != 722:
        falla('REGISTRO', 'el registro no tiene 722 ids distintos')
    res['estado'] = 'OK' if not fallas else 'FALLA'
    return res, man, plan, registro

# ----------------------------------------------------------------------------
# Fase T


def leer_sumas(ruta):
    listados = {}
    with open(ruta, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.rstrip('\n')
            if not linea.strip():
                continue
            partes = linea.split(None, 1)
            if len(partes) != 2:
                listados.setdefault('__mal__', []).append(linea)
                continue
            sha, ruta_rel = partes[0], partes[1].strip()
            if ruta_rel.startswith('*'):
                ruta_rel = ruta_rel[1:]
            if ruta_rel.startswith('./'):
                ruta_rel = ruta_rel[2:]
            listados[ruta_rel] = sha
    return listados


def fase_T(man, sha_pin, sobre, plan, abrir_sobre):
    fallas = []

    def falla(codigo, ensayo=None, celda=None, donde=None, detalle=''):
        fallas.append({'codigo': codigo, 'ensayo': ensayo, 'celda': celda, 'donde': donde, 'detalle': detalle})

    res = {'sobre': os.path.basename(os.path.normpath(sobre))}
    # T1 integridad
    ruta_sumas = os.path.join(sobre, 'SHA256SUMS.txt')
    bloques = sorted(glob.glob(os.path.join(sobre, 'bloques', '*', 'bloque_*.jsonl')))
    res['n_bloques'] = len(bloques)
    if not os.path.exists(ruta_sumas):
        falla('INTEGRIDAD', detalle='falta SHA256SUMS.txt')
        listados = {}
    else:
        res['sha256_SHA256SUMS'] = sha256_archivo(ruta_sumas)
        listados = leer_sumas(ruta_sumas)
        for linea in listados.pop('__mal__', []):
            falla('INTEGRIDAD', detalle='linea de SHA256SUMS sin formato: %r' % linea[:80])
        for rel, sha in sorted(listados.items()):
            ruta = os.path.join(sobre, rel)
            if not os.path.exists(ruta):
                falla('INTEGRIDAD', donde=rel, detalle='listado en SHA256SUMS y ausente')
            elif sha256_archivo(ruta) != sha:
                falla('INTEGRIDAD', donde=rel, detalle='sha256 distinto del listado')
    for b in bloques:
        rel = os.path.relpath(b, sobre).replace(os.sep, '/')
        if rel not in listados:
            falla('INTEGRIDAD', donde=rel, detalle='bloque sin linea en SHA256SUMS')
    res['n_listados'] = len(listados)
    # T2 lectura
    registros = []
    for b in bloques:
        with open(b, 'rb') as f:
            crudo = f.read()
        lineas = crudo.split(b'\n')
        if lineas and lineas[-1] == b'':
            lineas.pop()
        for i, ln in enumerate(lineas, 1):
            donde = '%s:%d' % (os.path.basename(b), i)
            try:
                r = json.loads(ln.decode('utf-8'))
            except (UnicodeDecodeError, ValueError):
                falla('ILEGIBLE', donde=donde, detalle='la linea no se lee como JSON')
                continue
            if not isinstance(r, dict):
                falla('ILEGIBLE', donde=donde, detalle='la linea no es un objeto JSON')
                continue
            registros.append((donde, r))
    res['n_lineas_leidas'] = len(registros)
    res['todos_sinteticos'] = bool(registros) and all(r.get('sintetico') is True for _, r in registros)
    if not res['todos_sinteticos'] and not abrir_sobre:
        res['estado'] = 'NEGADO'
        res['detalle'] = 'recibos no sinteticos: hace falta --abrir-sobre con autorizacion escrita'
        return res, None
    # T3 cobertura
    por_tupla = defaultdict(list)
    for donde, r in registros:
        s_id, reg, cond, sem = r.get('subject_id'), r.get('regime'), r.get('condition'), r.get('seed')
        if not (isinstance(s_id, str) and isinstance(reg, str) and isinstance(cond, str) and es_entero(sem)):
            falla('ESQUEMA', donde=donde, detalle='identidad del ensayo ausente o de tipo invalido')
            continue
        celda = '%s|%s' % (reg, s_id)
        ensayo = '%s|%s|%s|%d' % (s_id, reg, cond, sem)
        if celda not in plan:
            falla('FUERA_DEL_PLAN', ensayo=ensayo, donde=donde, detalle='celda que no existe en 010')
        elif cond not in plan[celda]['condiciones'] or sem not in SEMILLAS:
            falla('FUERA_DEL_PLAN', ensayo=ensayo, celda=celda, donde=donde, detalle='condicion o semilla fuera')
        else:
            por_tupla[(s_id, reg, cond, sem)].append((donde, r))
    for celda, p in sorted(plan.items()):
        for cond in p['condiciones']:
            for sem in SEMILLAS:
                t = (p['sujeto'], p['regimen'], cond, sem)
                ensayo = '%s|%s|%s|%d' % t
                n = len(por_tupla.get(t, []))
                if n == 0:
                    falla('FALTANTE', ensayo=ensayo, celda=celda)
                elif n > 1:
                    falla('DUPLICADO', ensayo=ensayo, celda=celda,
                          donde=','.join(d for d, _ in por_tupla[t]))
    unicos = {t: v[0] for t, v in por_tupla.items() if len(v) == 1}
    # T4 por recibo, T7 coherencia interna (sin imprimir cuentas)
    huellas_dp = {s: huella(man['sujetos'][s]['Dp']) for s in man['sujetos']}
    huellas_mirar = {s: huella(man['sujetos'][s]['mirar']) for s in man['sujetos']}
    posiciones = {s: {j: i for i, j in enumerate(man['sujetos'][s]['mirar'])} for s in man['sujetos']}
    entradas = canonico(man.get('entradas'))
    for t in sorted(unicos):
        donde, r = unicos[t]
        s_id, reg, cond, sem = t
        celda = '%s|%s' % (reg, s_id)
        ensayo = '%s|%s|%s|%d' % t
        suj = man['sujetos'][s_id]

        def f(codigo, detalle=''):
            falla(codigo, ensayo=ensayo, celda=celda, donde=donde, detalle=detalle)

        if r.get('protocol_id') != PROTOCOLO:
            f('PROTOCOLO')
        if r.get('manifiesto_sha256') != sha_pin:
            f('MANIFIESTO')
        if r.get('estado') != 'OK' or r.get('exit') != 0:
            f('ESTADO_TECNICO', 'estado o exit no son OK y 0')
        ch = r.get('chequeos')
        pedidos = CHEQUEOS_BASE + (CHEQUEOS_FUERA_C0 if cond != 'C0' else ())
        if (not isinstance(ch, dict) or any(k not in ch for k in pedidos)
                or any(v is not True for v in ch.values())):
            f('CHEQUEO_INTERNO', 'algun chequeo falta o no es true')
        ident = {'x': suj.get('x'), 'd': suj.get('d'), 'G': suj.get('G'), 'roots': suj.get('roots')}
        if canonico(r.get('identidad')) != canonico(ident):
            f('IDENTIDAD')
        if r.get('Dprime_hash') != huellas_dp[s_id] or r.get('Dprime_n') != len(suj['Dp']):
            f('DPRIME')
        hc = suj.get('huellas_condicion', {}).get(cond)
        if (not isinstance(hc, dict) or r.get('mask_hash') != hc.get('sha256')
                or r.get('mask_n') != hc.get('n') or r.get('mask_abs') != hc.get('abs')):
            f('MASCARA')
        if r.get('mirar_huella') != huellas_mirar[s_id]:
            f('MIRAR')
        grupo = plan[celda]['grupo']
        if r.get('grupo') != grupo:
            f('GRUPO')
        ev = man['grupos'].get(grupo, {}).get('eventos', {}).get(str(sem))
        if not isinstance(ev, dict) or r.get('input_events_hash') != ev.get('sha256'):
            f('EVENTOS')
        if cond != 'C0' and (not es_entero(r.get('filas_cambiadas')) or r.get('filas_cambiadas') != r.get('mask_n')):
            f('FILAS', 'filas_cambiadas distinto de mask_n')
        if canonico(r.get('input_hashes')) != entradas:
            f('ENTRADAS', 'input_hashes distinto de manifiesto.entradas')
        cm, cx, cg = r.get('cuentas_mirar'), r.get('cuenta_x'), r.get('cuentas_G')
        et, ac = r.get('espigas_total'), r.get('activas')
        if not (isinstance(cm, list) and isinstance(cg, list) and es_entero(cx) and es_entero(et) and es_entero(ac)):
            f('LECTURA', 'cuentas ausentes o de tipo invalido')
            continue
        mirar = suj['mirar']
        if len(cm) != len(mirar):
            f('COHERENCIA', 'len(cuentas_mirar) distinto de len(mirar)')
            continue
        if any(not es_entero(v) or v < 0 for v in cm) or any(not es_entero(v) or v < 0 for v in cg) \
                or cx < 0 or et < 0 or ac < 0:
            f('COHERENCIA', 'hay una cuenta no entera o negativa')
            continue
        pos = posiciones[s_id]
        if cx != cm[pos[suj['x']]]:
            f('COHERENCIA', 'cuenta_x distinto de cuentas_mirar[pos(x)]')
        if len(cg) != len(suj['G']) or any(cg[k] != cm[pos[g]] for k, g in enumerate(suj['G'])):
            f('COHERENCIA', 'cuentas_G distinto de cuentas_mirar[pos(G)]')
        if sum(cm) > et:
            f('COHERENCIA', 'la suma de cuentas_mirar supera espigas_total')
        if sum(1 for v in cm if v != 0) > ac:
            f('COHERENCIA', 'las cuentas no nulas superan activas')
    # T5 pareado
    for celda, p in sorted(plan.items()):
        s_id, reg = p['sujeto'], p['regimen']
        for sem in SEMILLAS:
            hashes = {unicos[(s_id, reg, c, sem)][1].get('input_events_hash')
                      for c in p['condiciones'] if (s_id, reg, c, sem) in unicos}
            if len(hashes) > 1:
                falla('ENTRADA_DESIGUAL', ensayo='%s|%s|*|%d' % (s_id, reg, sem), celda=celda,
                      detalle='input_events_hash distinto entre condiciones')
            if s_id in RELEVOS:
                a, b = unicos.get((s_id, reg, 'C0', sem)), unicos.get((s_id, reg, 'SHAM', sem))
                if a and b and any(canonico(a[1].get(k)) != canonico(b[1].get(k)) for k in CAMPOS_SHAM):
                    falla('SHAM_DISTINTO_DE_C0', ensayo='%s|%s|SHAM|%d' % (s_id, reg, sem), celda=celda)
    # T6 unicidad
    commits = Counter(r.get('code_commit') for _, r in registros)
    res['code_commit'] = sorted(map(str, commits))
    if len(commits) > 1:
        falla('CODE_COMMIT_MIXTO', detalle='%d code_commit distintos' % len(commits))
    versiones = Counter(unicos[t][1].get('runner_version') for t in unicos)
    res['runner_version'] = {str(k): v for k, v in sorted(versiones.items(), key=lambda kv: str(kv[0]))}
    if len(versiones) > 1:
        modal, n_modal = versiones.most_common(1)[0]
        if 2 * n_modal <= sum(versiones.values()):
            falla('RUNNER_VERSION_MIXTO', detalle='sin version mayoritaria')
        else:
            for t in sorted(unicos):
                if unicos[t][1].get('runner_version') != modal:
                    falla('RUNNER_VERSION', ensayo='%s|%s|%s|%d' % t, celda='%s|%s' % (t[1], t[0]),
                          donde=unicos[t][0], detalle='runner_version distinto del mayoritario')
    # T8 entorno
    entornos = Counter(canonico(unicos[t][1].get('entorno')) for t in unicos)
    res['entorno'] = {'uniforme': len(entornos) == 1, 'variantes': len(entornos),
                      'mayoritario': json.loads(entornos.most_common(1)[0][0]) if entornos else None}
    # Regla propia de invalidez: una falla con celda invalida esa celda; sin celda, las 44.
    globales = [x for x in fallas if x['celda'] is None]
    invalidas = sorted(plan) if globales else sorted({x['celda'] for x in fallas})
    res['fallas'] = fallas
    res['n_fallas'] = len(fallas)
    res['por_codigo'] = dict(sorted(Counter(x['codigo'] for x in fallas).items()))
    res['fallas_globales'] = len(globales)
    res['celdas_invalidas'] = invalidas
    res['regla'] = ('una falla con celda invalida su celda (sujeto, regimen); una falla sin celda '
                    '(integridad, linea ilegible, esquema, celda inexistente, code_commit mixto) invalida las 44')
    res['comparacion_D13'] = ('igual a D13 en lo que D13 nombra; agrega como fallas de celda MIRAR, GRUPO, FILAS, '
                              'ENTRADAS, RUNNER_VERSION y COHERENCIA, que D13 no menciona porque el control '
                              'del productor no las mira')
    res['estado'] = 'OK' if not fallas else 'FALLAS'
    return res, unicos

# ----------------------------------------------------------------------------
# Fase S: datos


class ErrorDatos(Exception):
    pass


def extraer_celda(man, p, unicos):
    s_id, reg = p['sujeto'], p['regimen']
    suj = man['sujetos'][s_id]
    pos = {j: i for i, j in enumerate(suj['mirar'])}
    idx_dp = np.array([pos[j] for j in suj['Dp']], dtype=np.int64)
    k = len(suj['G'])
    por_cond = {}
    for cond in p['condiciones']:
        y = np.empty(N)
        h = np.empty(N)
        g = np.empty((N, k))
        for sem in SEMILLAS:
            par = unicos.get((s_id, reg, cond, sem))
            if par is None:
                raise ErrorDatos('falta o se repite %s|%s|%s|%d' % (s_id, reg, cond, sem))
            r = par[1]
            try:
                cm = np.asarray(r['cuentas_mirar'], dtype=np.int64)
                if cm.shape != (len(suj['mirar']),):
                    raise ErrorDatos('cuentas_mirar con largo distinto de mirar')
                y[sem] = float(cm[idx_dp].sum()) / DURACION_S
                h[sem] = float(r['cuenta_x']) / DURACION_S
                cg = np.asarray(r['cuentas_G'], dtype=np.int64)
                if cg.shape != (k,):
                    raise ErrorDatos('cuentas_G con largo distinto de G')
                g[sem] = cg / DURACION_S
            except (KeyError, TypeError, ValueError) as e:
                raise ErrorDatos('recibo ilegible para la estadistica: %s' % type(e).__name__)
        por_cond[cond] = {'Y': y, 'H': h, 'G': g}
    return por_cond


def cantidades(s_id, reg, suj, pc):
    """Anexo B. Devuelve nombre -> ('media', d) o ('cociente', num, den), todo por semilla."""
    def y(c):
        return pc[c]['Y']

    def h(c):
        return pc[c]['H']

    q = {}
    if s_id in RELEVOS:
        y0, h0 = y('C0'), h('C0')
        for b in COND_RELEVO[1:]:
            q['D' + b] = ('media', y(b) - y0)
        q['r_Q1'] = ('cociente', y('Q1') - y0, y('Q2') - y0)
        q['c_X'] = ('cociente', h0 - h('Q1'), h0)
        q['s4'] = ('cociente', h('Q4'), h0)
        q['r_weak'] = ('cociente', y('QWEAK') - y0, y('Q2') - y0)
        q['COL_cortado'] = ('media', y('Q1uQCOL') - y('Q1'))
        q['COL_interaccion'] = ('media', (y('Q1uQCOL') - y('Q1')) - (y('QCOL') - y0))
        q['XD_q1'] = ('media', y('Q1uQXD') - y('QXD'))
        q['XD_dif'] = ('media', (y('Q1uQXD') - y('QXD')) - (y('Q1') - y0))
        q['Q1_menos_Q3'] = ('media', y('Q1') - y('Q3'))
        q['HC0'] = ('media', h0)
        if reg == 'B' and s_id in T1_RELEVOS:
            q['T1a'] = ('media', (y('Q1') - y0) - MARGEN_T1_R * (y('Q2') - y0))
            q['T1b'] = ('media', h('Q4') - MARGEN_T1_S4 * h0)
        if reg == 'A' and s_id == 'R01':
            iz = suj['G'].index(suj['cascada_ZA'][1])

            def g(c):
                return pc[c]['G'][:, iz]

            q['ZA1'] = ('media', g('ZA') - g('C0'))
            q['ZA2'] = ('media', (h('ZA') - h0) - (h('ZAuQ1') - h('Q1')))
            q['ZA3'] = ('media', (y('ZAuQ1uQCOL') - y('Q1uQCOL')) - (y('ZAuQCOL') - y('QCOL')))
        return q
    if reg == 'B':
        y0, h0 = y('C0'), h('C0')
        dq2 = y('Q2') - y0
        dqc = y('Q1conj') - y0
        q['DQ2'] = ('media', dq2)
        q['DQ4conj'] = ('media', y('Q4conj') - y0)
        q['DQ1conj'] = ('media', dqc)
        dq1 = []
        for gg in suj['G']:
            d1 = y('Q1_%d' % gg) - y0
            q['DQ1_%d' % gg] = ('media', d1)
            dq1.append(d1)
        q['r_Q1conj'] = ('cociente', dqc, dq2)
        q['c_Xconj'] = ('cociente', h0 - h('Q1conj'), h0)
        q['s4conj'] = ('cociente', h('Q4conj'), h0)
        q['T2a'] = ('media', dqc - MARGEN_T2_R * dq2)
        q['T2b'] = ('media', (h0 - h('Q1conj')) - MARGEN_T2_CAIDA * h0)
        q['T2c'] = ('media', dqc - np.mean(np.vstack(dq1), axis=0))
        return q
    completo = 'C_' + '1' * len(suj['G'])
    q['FC'] = ('media', h(completo) - h('C_desplazado'))
    return q

# ----------------------------------------------------------------------------
# Fase S: motores


_JK = np.array([[j for j in range(N) if j != i] for i in range(N)], dtype=np.int64)
_SIGNOS10 = 1.0 - 2.0 * ((np.arange(1024)[:, None] >> np.arange(10)[None, :]) & 1)


def _media(x, axis=-1):
    return np.mean(x, axis=axis)


def _cociente(num, den, axis=-1):
    return np.mean(num, axis=axis) / np.mean(den, axis=axis)


def niveles_bca(theta, theta_b, stat, datos):
    """D2 literal: z0 con menores mas la mitad de los iguales, aceleracion por jackknife de semillas."""
    b = theta_b.size
    frac = (np.count_nonzero(theta_b < theta) + 0.5 * np.count_nonzero(theta_b == theta)) / b
    z0 = float(special.ndtri(frac))
    theta_j = stat(*[x[_JK] for x in datos])
    u = np.mean(theta_j) - theta_j
    s2 = float(np.sum(u ** 2))
    s3 = float(np.sum(u ** 3))
    a = s3 / (6.0 * s2 ** 1.5) if s2 > 0 else float('nan')
    zl = float(special.ndtri((1.0 - NIVEL) / 2.0))
    zh = -zl
    with np.errstate(all='ignore'):
        a1 = float(special.ndtr(z0 + (z0 + zl) / (1.0 - a * (z0 + zl))))
        a2 = float(special.ndtr(z0 + (z0 + zh) / (1.0 - a * (z0 + zh))))
    return z0, a, a1, a2


def degenerado(theta, theta_b, stat, datos):
    if np.all(theta_b == theta_b[0]):
        return 'D2: todos los remuestreos iguales'
    z0, a, a1, a2 = niveles_bca(theta, theta_b, stat, datos)
    if not math.isfinite(z0):
        return 'D2: z0 infinito'
    if not math.isfinite(a):
        return 'D2: aceleracion no definida'
    if not (0.0 < a1 < 1.0 and 0.0 < a2 < 1.0):
        return 'D2: niveles ajustados fuera de (0, 1)'
    return None


def intervalo(gen, cant, motor):
    """Un id del registro: consume exactamente un bloque del flujo (D4) y aplica D2 y D3."""
    estado0 = gen.bit_generator.state
    idx = gen.integers(0, N, size=(N_BOOT, N))
    if cant[0] == 'media':
        datos = (np.asarray(cant[1], dtype=float),)
        stat = _media
        out = {'tipo': 'media', 'estimado': float(np.mean(datos[0])), 'ic95': None, 'estado_ic': None}
    else:
        num, den = np.asarray(cant[1], dtype=float), np.asarray(cant[2], dtype=float)
        datos = (num, den)
        stat = _cociente
        mn, md = float(np.mean(num)), float(np.mean(den))
        out = {'tipo': 'cociente', 'numerador': mn, 'denominador': md, 'estimado': None, 'ic95': None,
               'estado_ic': None}
        if not md > 0:
            out['estado_ic'] = 'SIN_ESTIMADO'
            out['motivo'] = 'D3: denominador observado <= 0'
            return out
        out['estimado'] = mn / md
        if np.any(np.mean(den[idx], axis=-1) <= 0) or np.any(np.mean(den[_JK], axis=-1) <= 0):
            out['estado_ic'] = 'INDEFINIDO'
            out['motivo'] = 'D3: algun remuestreo o jackknife con denominador <= 0'
            return out
    theta = float(stat(*datos))
    theta_b = stat(*[x[idx] for x in datos])
    motivo = degenerado(theta, theta_b, stat, datos)
    if motivo:
        motor['degenerados'] += 1
        out['estado_ic'] = 'DEGENERADO'
        out['motivo'] = motivo
        return out
    clon = np.random.Generator(np.random.PCG64())
    clon.bit_generator.state = estado0
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            res = stats.bootstrap(datos, stat, n_resamples=N_BOOT, batch=None, vectorized=True, paired=True,
                                  axis=-1, confidence_level=NIVEL, alternative='two-sided', method='BCa', rng=clon)
    except Exception as e:  # el motor no deberia fallar si D2 no marco degenerado
        motor['scipy_excepcion'] += 1
        out['estado_ic'] = 'MOTOR_INCONSISTENTE'
        out['motivo'] = 'scipy.stats.bootstrap: %s' % type(e).__name__
        return out
    motor['scipy_llamadas'] += 1
    if clon.bit_generator.state != gen.bit_generator.state:
        motor['flujo_desalineado'] += 1
    if not np.array_equal(np.asarray(res.bootstrap_distribution), theta_b):
        motor['distribucion_distinta'] += 1
    lo, hi = float(res.confidence_interval.low), float(res.confidence_interval.high)
    if not (math.isfinite(lo) and math.isfinite(hi)):
        motor['scipy_no_finito'] += 1
        out['estado_ic'] = 'MOTOR_INCONSISTENTE'
        out['motivo'] = 'scipy devolvio un limite no finito'
        return out
    _, _, a1, a2 = niveles_bca(theta, theta_b, stat, datos)
    lo2, hi2 = (float(v) for v in np.percentile(theta_b, [100.0 * a1, 100.0 * a2]))
    if abs(lo - lo2) > 1e-12 * max(1.0, abs(lo)) or abs(hi - hi2) > 1e-12 * max(1.0, abs(hi)):
        motor['bca_literal_distinto'] += 1
    out['estado_ic'] = 'OK'
    out['ic95'] = [lo, hi]
    return out


def signos_bilateral(d):
    """Inversion de signos exacta sobre los 2^20 signos, con la tolerancia de D14."""
    d = np.asarray(d, dtype=float)
    if d.shape != (N,):
        raise ValueError('la inversion de signos espera 20 semillas')
    obs = abs(float(np.sum(d)))
    tol = TOL_SIGNOS * (1.0 + float(np.sum(np.abs(d))))
    a = _SIGNOS10 @ d[:10]
    b = _SIGNOS10 @ d[10:]
    extremos = np.count_nonzero(np.abs(a[:, None] + b[None, :]) >= obs - tol)
    return float(extremos) / float(2 ** N)


def prueba(id_, d):
    p = {'id': id_, 'estado': None, 'n': None, 'media': None, 'de': None, 't': None, 'gl': None,
         'p_observado': None, 'p_familia': 1.0, 'signos_bilateral': None, 'p_holm': None, 'decide': False}
    if d is None:
        p['estado'] = 'INVALIDO_TECNICO'
        return p
    d = np.asarray(d, dtype=float)
    media = float(np.mean(d))
    de = float(np.std(d, ddof=1))
    p.update(n=int(d.size), media=media, de=de, gl=int(d.size) - 1, signos_bilateral=signos_bilateral(d))
    if de <= TOL_VARIANZA * max(1.0, abs(media)):
        p['estado'] = 'VARIANZA_CERO'
        return p
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        r = stats.ttest_1samp(d, 0.0, alternative='greater')
    p.update(estado='OK', t=float(r.statistic), p_observado=float(r.pvalue), p_familia=float(r.pvalue))
    return p


def holm(pruebas):
    m = len(pruebas)
    orden = sorted(range(m), key=lambda i: (pruebas[i]['p_familia'], i))
    acumulado = 0.0
    for rango, i in enumerate(orden):
        acumulado = max(acumulado, min(1.0, (m - rango) * pruebas[i]['p_familia']))
        pruebas[i]['p_holm'] = acumulado
    for p in pruebas:
        p['decide'] = bool(p['estado'] == 'OK' and p['p_holm'] < ALFA)
    return pruebas

# ----------------------------------------------------------------------------
# Fase S: casos y veredictos


def excluye_cero(iv):
    return bool(iv is not None and iv.get('estado_ic') == 'OK' and iv.get('ic95') is not None
                and (iv['ic95'][0] > 0 or iv['ic95'][1] < 0))


def lim_inf_supera(iv, margen):
    return bool(iv is not None and iv.get('estado_ic') == 'OK' and iv.get('ic95') is not None
                and iv['ic95'][0] > margen)


def activacion(reg, s_id, suj, pc, iv, decide):
    pre = '%s|%s|' % (reg, s_id)
    dq2 = iv[pre + 'DQ2']
    drivers = [float(np.mean(pc['C0']['G'][:, k])) for k in range(len(suj['G']))]
    x0 = float(np.mean(pc['C0']['H']))
    crit = {'drivers_C0_ge_10Hz': all(v >= TASA_MIN_HZ for v in drivers),
            'x_C0_ge_10Hz': x0 >= TASA_MIN_HZ,
            'DQ2_ge_5Hz': dq2['estimado'] >= DQ2_MIN_HZ,
            'IC95_DQ2_excluye_0': excluye_cero(dq2)}
    if reg == 'B':
        crit['DQ2_F_B_holm_lt_001'] = bool(decide[pre + 'DQ2'])
    ok = all(crit.values())
    if reg == 'B':
        estado = 'ACTIVADO' if ok else 'NO_INFORMATIVO_EN_B'
    else:
        estado = 'RECLUTADO' if ok else 'NO_RECLUTADO_EN_A'
    return {'estado': estado, 'criterios': crit, 'causas': sorted(k for k, v in crit.items() if not v),
            'medido': {'drivers_C0_Hz': drivers, 'x_C0_Hz': x0, 'DQ2_Hz': dq2['estimado'],
                       'IC95_DQ2': dq2['ic95'], 'IC95_DQ2_estado': dq2['estado_ic']}}


def publicar(reg, calc, estado_act, iv_base):
    """D8 segun el anexo B: en B solo con la celda ACTIVADO; en A con el IC95 del denominador que excluye cero.

    El denominador no positivo ya deja al cociente SIN_ESTIMADO por D3, y esa etiqueta se conserva.
    (Primera version: tambien pedia aca el denominador positivo y ponia NULO; el cotejo K2 del ensayo lo
    marco en A|R07 y se alineo al anexo B. Ver respuesta 2026-11-03-010.)
    """
    pub = dict(calc)
    pub['estado_ic_calculado'] = calc['estado_ic']
    motivo = None
    if reg == 'B':
        if estado_act != 'ACTIVADO':
            motivo = 'B %s' % estado_act
    elif not excluye_cero(iv_base):
        motivo = 'A: el IC95 del denominador no excluye cero'
    if motivo:
        pub.update(estimado=None, ic95=None, estado_ic='NULO', motivo=motivo)
    return pub


def estado_prueba_T(activado, crit):
    if not activado:
        return 'NO_PASA:NO_INFORMATIVO_EN_B'
    return 'PASA' if all(crit.values()) else 'NO_PASA:SIN_DECIDIR'


def caso_relevo(reg, s_id, suj, pc, iv, decide):
    pre = '%s|%s|' % (reg, s_id)
    act = activacion(reg, s_id, suj, pc, iv, decide)
    caso = {'estado': act['estado'], 'activacion': act, 'H_C0': iv[pre + 'HC0'],
            'efectos': {n: iv[pre + n] for n in ['D' + b for b in COND_RELEVO[1:]] + list(EFECTOS_EXTRA)}}
    bases = {'r_Q1': iv[pre + 'DQ2'], 'r_weak': iv[pre + 'DQ2'], 'c_X': iv[pre + 'HC0'], 's4': iv[pre + 'HC0']}
    caso['cocientes'] = {n: publicar(reg, iv[pre + n], act['estado'], bases[n]) for n in COCIENTES_RELEVO}
    rw = caso['cocientes']['r_weak']
    banda = None
    if rw['estimado'] is not None:
        a = abs(rw['estimado'])
        banda = 'PEQUENO' if a < BANDAS_WEAK[0] else ('INTERMEDIO' if a < BANDAS_WEAK[1] else 'ALTO')
    caso['qweak'] = {'banda': banda, 'DQWEAK_Hz': iv[pre + 'DQWEAK']['estimado']}
    if reg == 'B' and s_id in T1_RELEVOS:
        crit = {'activado': act['estado'] == 'ACTIVADO',
                'T1a_F_B': bool(decide[pre + 'T1a']), 'T1b_F_B': bool(decide[pre + 'T1b']),
                'r_Q1_ic_sobre_margen': lim_inf_supera(caso['cocientes']['r_Q1'], MARGEN_T1_R),
                's4_ic_sobre_margen': lim_inf_supera(caso['cocientes']['s4'], MARGEN_T1_S4)}
        caso['T1'] = {'estado': estado_prueba_T(crit['activado'], crit), 'criterios': crit}
    if reg == 'A' and s_id == 'R01':
        caso['cascada_ZA'] = {z: iv[pre + z] for z in ('ZA1', 'ZA2', 'ZA3')}
    return caso


def caso_hub_B(s_id, suj, pc, iv, decide):
    pre = 'B|%s|' % s_id
    act = activacion('B', s_id, suj, pc, iv, decide)
    nombres = ['DQ2', 'DQ4conj', 'DQ1conj'] + ['DQ1_%d' % g for g in suj['G']] + ['T2a', 'T2b', 'T2c']
    caso = {'estado': act['estado'], 'activacion': act, 'efectos': {n: iv[pre + n] for n in nombres}}
    caso['cocientes'] = {n: publicar('B', iv[pre + n], act['estado'], None) for n in COCIENTES_HUB}
    crit = {'activado': act['estado'] == 'ACTIVADO',
            'T2a_F_B': bool(decide[pre + 'T2a']), 'T2b_F_B': bool(decide[pre + 'T2b']),
            'T2c_F_B': bool(decide[pre + 'T2c']),
            'r_Q1conj_ic_sobre_margen': lim_inf_supera(caso['cocientes']['r_Q1conj'], MARGEN_T2_R),
            'c_Xconj_ic_sobre_margen': lim_inf_supera(caso['cocientes']['c_Xconj'], MARGEN_T2_CAIDA),
            'c_ic_sobre_0': lim_inf_supera(iv[pre + 'T2c'], 0.0)}
    caso['T2'] = {'estado': estado_prueba_T(crit['activado'], crit), 'criterios': crit}
    return caso


def caso_hub_C(s_id, suj, pc, iv, decide):
    k = len(suj['G'])
    subconj = condiciones_de(s_id, 'C', suj)[:-1]
    tabla = {}
    for c in subconj:
        hz = float(np.mean(pc[c]['H']))
        etq = 'ON' if hz >= TASA_MIN_HZ else ('OFF' if hz <= TASA_OFF_HZ else 'IND')
        tabla[c] = {'H_Hz': hz, 'etiqueta': etq}
    vacio, completo = 'C_' + '0' * k, 'C_' + '1' * k
    if any(t['etiqueta'] == 'IND' for t in tabla.values()):
        transf = 'INDETERMINADO'
    elif tabla[vacio]['etiqueta'] == 'OFF' and all(tabla[c]['etiqueta'] == 'ON' for c in subconj if c != vacio):
        transf = 'OR_COMPATIBLE_EN_C'
    elif tabla[completo]['etiqueta'] == 'ON' and all(tabla[c]['etiqueta'] == 'OFF'
                                                     for c in subconj if c != completo):
        transf = 'AND_COMPATIBLE_EN_C'
    else:
        transf = 'OTRA_TRANSFERENCIA'
    fc = 'C|%s|FC' % s_id
    return {'estado': 'VALIDO', 'tabla_ON_OFF': tabla, 'H_desplazado_Hz': float(np.mean(pc['C_desplazado']['H'])),
            'transferencia': transf,
            'FC': {'estado': 'SOSTENIDA' if decide[fc] else 'SIN_DECIDIR', 'intervalo': iv[fc]}}


def combinar(estados, k):
    """D9."""
    pasa = sum(1 for e in estados if e == 'PASA')
    bloq = sum(1 for e in estados if e == 'BLOQUEADO')
    if pasa >= k:
        return 'SOSTENIDA'
    if pasa + bloq >= k:
        return 'INVALIDO_TECNICO'
    no_pasan = [e for e in estados if e != 'PASA']
    if no_pasan and all(e == 'NO_PASA:NO_INFORMATIVO_EN_B' for e in no_pasan):
        return 'NO_INFORMATIVO_EN_B'
    return 'SIN_DECIDIR'


def estado_tipo(instancias):
    """D9: un tipo pasa si pasan todas sus instancias."""
    if all(e == 'PASA' for e in instancias):
        return 'PASA'
    no_pasan = [e for e in instancias if e.startswith('NO_PASA')]
    if no_pasan:
        if all(e == 'NO_PASA:NO_INFORMATIVO_EN_B' for e in no_pasan):
            return 'NO_PASA:NO_INFORMATIVO_EN_B'
        return 'NO_PASA:SIN_DECIDIR'
    return 'BLOQUEADO'


def veredictos(casos, decide, inval, iv):
    t1 = {s: ('BLOQUEADO' if 'B|%s' % s in inval else casos['B|%s' % s]['T1']['estado']) for s in T1_RELEVOS}
    inst = {h: ('BLOQUEADO' if 'B|%s' % h in inval else casos['B|%s' % h]['T2']['estado']) for h in HUBS}
    tipos = {t: estado_tipo([inst[h] for h in hs]) for t, hs in TIPOS_HUB}
    f_c = {h: ('INVALIDO_TECNICO' if 'C|%s' % h in inval else casos['C|%s' % h]['FC']['estado']) for h in HUBS}
    if 'A|R01' in inval:
        f_r01 = {'firma': 'INVALIDO_TECNICO', 'contrastes': None}
    else:
        con = {z: bool(decide['A|R01|%s' % z]) for z in ('ZA1', 'ZA2', 'ZA3')}
        f_r01 = {'firma': 'SOSTENIDA' if all(con.values()) else 'SIN_DECIDIR', 'contrastes': con}
    qweak = {}
    for s in RELEVOS:
        for r in ('A', 'B'):
            c = '%s|%s' % (r, s)
            qweak[c] = None if c in inval else casos[c]['qweak']
    t3 = {}
    for s in T3_RELEVOS:
        for r in ('A', 'B'):
            c = '%s|%s' % (r, s)
            if c in inval:
                t3[c] = {'estado': 'INVALIDO_TECNICO'}
            else:
                co = casos[c]['cocientes']
                t3[c] = {'estado': casos[c]['estado'], 'DQ2_Hz': iv['%s|DQ2' % c]['estimado'],
                         'r_Q1': co['r_Q1']['estimado'], 'c_X': co['c_X']['estimado'], 's4': co['s4']['estimado']}
    return {'P_T1_B': {'casos': t1, 'veredicto': combinar(list(t1.values()), 3), 'requiere': 'R01, R02 y R03'},
            'P_T2_B': {'instancias': inst, 'tipos': tipos, 'veredicto': combinar(list(tipos.values()), 3),
                       'requiere': '3 de 4 tipos'},
            'F_C': f_c, 'F_R01': f_r01, 'QWEAK': qweak, 'T3': t3,
            'P_ESTRATOS': 'retirada (010 seccion 8): no se evalua'}


def fase_S(man, plan, registro, unicos, invalidas, modo):
    no_calculables = []
    datos = {}
    for c in sorted(plan):
        if c in invalidas:
            continue
        try:
            datos[c] = extraer_celda(man, plan[c], unicos)
        except ErrorDatos as e:
            no_calculables.append({'celda': c, 'detalle': str(e)})
    inval = set(invalidas) | {x['celda'] for x in no_calculables}
    cants = {}
    for c, pc in datos.items():
        if c in inval:
            continue
        reg, s_id = c.split('|')
        for nombre, q in cantidades(s_id, reg, man['sujetos'][s_id], pc).items():
            cants['%s|%s|%s' % (reg, s_id, nombre)] = q
    faltan = [i for i in registro if '|'.join(i.split('|')[:2]) not in inval and i not in cants]
    if faltan or len(cants) != sum(1 for i in registro if '|'.join(i.split('|')[:2]) not in inval):
        raise RuntimeError('el registro y las cantidades no coinciden: %s' % faltan[:5])
    gen = np.random.Generator(np.random.PCG64(SEMILLA_BOOT))
    motor = Counter()
    iv = {}
    for id_ in registro:
        celda = '|'.join(id_.split('|')[:2])
        if celda in inval:
            gen.integers(0, N, size=(N_BOOT, N))  # D4: el bloque se consume igual
            iv[id_] = None
            continue
        iv[id_] = intervalo(gen, cants[id_], motor)
    familias = {}
    for nombre in FAMILIAS:
        pr = []
        for i in ids_familia(nombre):
            celda = '|'.join(i.split('|')[:2])
            pr.append(prueba(i, None if celda in inval else cants[i][1]))
        holm(pr)
        familias[nombre] = {'m': len(pr), 'alfa': ALFA, 'n_deciden': sum(1 for p in pr if p['decide']),
                            'pruebas': pr}
    decide = {p['id']: p['decide'] for f in familias.values() for p in f['pruebas']}
    casos = {}
    for c in sorted(plan):
        if c in inval:
            casos[c] = {'estado': 'INVALIDO_TECNICO'}
            continue
        reg, s_id = c.split('|')
        suj = man['sujetos'][s_id]
        if s_id in RELEVOS:
            casos[c] = caso_relevo(reg, s_id, suj, datos[c], iv, decide)
        elif reg == 'B':
            casos[c] = caso_hub_B(s_id, suj, datos[c], iv, decide)
        else:
            casos[c] = caso_hub_C(s_id, suj, datos[c], iv, decide)
    return {'protocolo': PROTOCOLO, 'version_verificador': VERSION, 'modo': modo,
            'parametros': {'n': N, 'n_boot': N_BOOT, 'semilla_boot': SEMILLA_BOOT, 'nivel': NIVEL, 'alfa': ALFA,
                           'tasa_min_Hz': TASA_MIN_HZ, 'tasa_off_Hz': TASA_OFF_HZ, 'dq2_min_Hz': DQ2_MIN_HZ,
                           'margenes': {'T1_r': MARGEN_T1_R, 'T1_s4': MARGEN_T1_S4, 'T2_r': MARGEN_T2_R,
                                        'T2_caida': MARGEN_T2_CAIDA},
                           'bandas_weak': list(BANDAS_WEAK)},
            'motores': {'bca': 'scipy.stats.bootstrap(method=BCa, paired=True, batch=None)',
                        't': 'scipy.stats.ttest_1samp(alternative=greater)',
                        'signos': 'enumeracion exacta propia (2^10 x 2^10)', 'holm': 'propio',
                        'chequeos': dict(sorted(motor.items()))},
            'invalidas': sorted(inval), 'no_calculables': no_calculables,
            'registro_sha256': sha256_texto('\n'.join(registro) + '\n'),
            'intervalos': iv, 'familias': familias, 'casos': casos,
            'veredictos': veredictos(casos, decide, inval, iv)}

# ----------------------------------------------------------------------------
# Fase K


class Diferencias:
    def __init__(self):
        self.lista = []

    def anotar(self, donde, campo, prod, ver, regla):
        self.lista.append({'donde': donde, 'campo': campo, 'productor': prod, 'verificador': ver, 'regla': regla})


def _es_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def cmp_valor(dif, donde, campo, p, v, tol=None, relativa=True):
    if p is None or v is None:
        if not (p is None and v is None):
            dif.anotar(donde, campo, p, v, 'uno es nulo')
        return
    if isinstance(p, list) or isinstance(v, list):
        if not (isinstance(p, list) and isinstance(v, list) and len(p) == len(v)):
            dif.anotar(donde, campo, p, v, 'forma distinta')
            return
        for i, (a, b) in enumerate(zip(p, v)):
            cmp_valor(dif, donde, '%s[%d]' % (campo, i), a, b, tol, relativa)
        return
    if tol is None:
        if p != v:
            dif.anotar(donde, campo, p, v, 'distinto')
        return
    if not (_es_num(p) and _es_num(v)):
        dif.anotar(donde, campo, p, v, 'tipo distinto')
        return
    lim = tol * max(1.0, abs(p)) if relativa else tol
    if not abs(p - v) <= lim:
        dif.anotar(donde, campo, p, v, '|dif| > %.3g' % lim)


def cmp_intervalo(dif, donde, p, v):
    if p is None or v is None:
        cmp_valor(dif, donde, 'intervalo', None if p is None else 'presente', None if v is None else 'presente')
        return
    for campo in ('tipo', 'estado_ic'):
        cmp_valor(dif, donde, campo, p.get(campo), v.get(campo))
    for campo in ('estimado', 'ic95', 'numerador', 'denominador'):
        if campo in p or campo in v:
            cmp_valor(dif, donde, campo, p.get(campo), v.get(campo), TOL_K_INTERVALO)


def comparar(agr, mio, registro):
    dif = Diferencias()
    cmp_valor(dif, 'invalidas', 'lista', sorted(agr.get('invalidas', [])), sorted(mio['invalidas']))
    ip = agr.get('intervalos', {})
    if sorted(ip) != list(registro):
        dif.anotar('intervalos', 'ids', len(ip), len(registro), 'el registro del productor no es el propio')
    for i in registro:
        cmp_intervalo(dif, 'intervalos/' + i, ip.get(i), mio['intervalos'].get(i))
    for nombre in FAMILIAS:
        fp, fv = agr.get('familias', {}).get(nombre, {}), mio['familias'][nombre]
        for campo in ('m', 'n_deciden'):
            cmp_valor(dif, 'familias/' + nombre, campo, fp.get(campo), fv.get(campo))
        lp = fp.get('pruebas', [])
        if [p.get('id') for p in lp] != [p['id'] for p in fv['pruebas']]:
            dif.anotar('familias/' + nombre, 'orden', None, None, 'otras pruebas u otro orden')
        pp = {p.get('id'): p for p in lp}
        for b in fv['pruebas']:
            a = pp.get(b['id'])
            donde = 'familias/%s/%s' % (nombre, b['id'])
            if a is None:
                dif.anotar(donde, 'prueba', None, 'presente', 'falta en el productor')
                continue
            for campo in ('estado', 'decide', 'n', 'gl'):
                cmp_valor(dif, donde, campo, a.get(campo), b.get(campo))
            for campo in ('p_observado', 'p_familia', 'p_holm', 'signos_bilateral'):
                cmp_valor(dif, donde, campo, a.get(campo), b.get(campo), TOL_K_PRUEBA, relativa=False)
            for campo in ('media', 'de', 't'):
                cmp_valor(dif, donde, campo, a.get(campo), b.get(campo), TOL_K_INTERVALO)
    cp = agr.get('casos', {})
    for c in sorted(mio['casos']):
        a, b = cp.get(c), mio['casos'][c]
        donde = 'casos/' + c
        if a is None:
            dif.anotar(donde, 'caso', None, 'presente', 'falta en el productor')
            continue
        cmp_valor(dif, donde, 'estado', a.get('estado'), b.get('estado'))
        if a.get('estado') == 'INVALIDO_TECNICO' or b.get('estado') == 'INVALIDO_TECNICO':
            continue
        if 'activacion' in b:
            aa, ab = a.get('activacion', {}), b['activacion']
            cmp_valor(dif, donde, 'activacion.estado', aa.get('estado'), ab['estado'])
            cmp_valor(dif, donde, 'activacion.criterios', canonico(aa.get('criterios')), canonico(ab['criterios']))
            ma, mb = aa.get('medido', {}), ab['medido']
            for campo in ('drivers_C0_Hz', 'x_C0_Hz', 'DQ2_Hz', 'IC95_DQ2'):
                cmp_valor(dif, donde, 'activacion.medido.' + campo, ma.get(campo), mb[campo], TOL_K_INTERVALO)
            cmp_valor(dif, donde, 'activacion.medido.IC95_DQ2_estado', ma.get('IC95_DQ2_estado'),
                      mb['IC95_DQ2_estado'])
        for n, ivb in b.get('cocientes', {}).items():
            iva = a.get('cocientes', {}).get(n) or {}
            for campo in ('estado_ic', 'estado_ic_calculado'):
                cmp_valor(dif, donde, 'cocientes.%s.%s' % (n, campo), iva.get(campo), ivb.get(campo))
            for campo in ('estimado', 'ic95', 'numerador', 'denominador'):
                cmp_valor(dif, donde, 'cocientes.%s.%s' % (n, campo), iva.get(campo), ivb.get(campo), TOL_K_INTERVALO)
        for t in ('T1', 'T2'):
            if t in a or t in b:
                ta, tb = a.get(t) or {}, b.get(t) or {}
                cmp_valor(dif, donde, t + '.estado', ta.get('estado'), tb.get('estado'))
                cmp_valor(dif, donde, t + '.criterios', canonico(ta.get('criterios')), canonico(tb.get('criterios')))
        if 'qweak' in b:
            qa = a.get('qweak') or {}
            cmp_valor(dif, donde, 'qweak.banda', qa.get('banda'), b['qweak']['banda'])
            cmp_valor(dif, donde, 'qweak.DQWEAK_Hz', qa.get('DQWEAK_Hz'), b['qweak']['DQWEAK_Hz'], TOL_K_INTERVALO)
        if 'transferencia' in b:
            cmp_valor(dif, donde, 'transferencia', a.get('transferencia'), b['transferencia'])
            ta = a.get('tabla_ON_OFF') or {}
            for cond, fila in b['tabla_ON_OFF'].items():
                fa = ta.get(cond) or {}
                cmp_valor(dif, donde, 'tabla_ON_OFF.%s.etiqueta' % cond, fa.get('etiqueta'), fila['etiqueta'])
                cmp_valor(dif, donde, 'tabla_ON_OFF.%s.H_Hz' % cond, fa.get('H_Hz'), fila['H_Hz'], TOL_K_INTERVALO)
            if sorted(ta) != sorted(b['tabla_ON_OFF']):
                dif.anotar(donde, 'tabla_ON_OFF', sorted(ta), sorted(b['tabla_ON_OFF']), 'otras subcondiciones')
            cmp_valor(dif, donde, 'H_desplazado_Hz', a.get('H_desplazado_Hz'), b['H_desplazado_Hz'], TOL_K_INTERVALO)
            cmp_valor(dif, donde, 'FC.estado', (a.get('FC') or {}).get('estado'), b['FC']['estado'])
    vp, vv = agr.get('veredictos', {}), mio['veredictos']
    for clave in ('P_T1_B', 'P_T2_B'):
        for campo in ('veredicto', 'casos', 'tipos', 'instancias'):
            if campo in vv[clave]:
                cmp_valor(dif, 'veredictos/' + clave, campo, canonico((vp.get(clave) or {}).get(campo)),
                          canonico(vv[clave][campo]))
    cmp_valor(dif, 'veredictos/F_C', 'estados', canonico(vp.get('F_C')), canonico(vv['F_C']))
    fr_p, fr_v = vp.get('F_R01') or {}, vv['F_R01']
    cmp_valor(dif, 'veredictos/F_R01', 'firma', fr_p.get('firma'), fr_v['firma'])
    if fr_v['firma'] != 'INVALIDO_TECNICO':
        cmp_valor(dif, 'veredictos/F_R01', 'contrastes', canonico(fr_p.get('contrastes')), canonico(fr_v['contrastes']))
    qp = vp.get('QWEAK') or {}
    for c, qv in sorted(vv['QWEAK'].items()):
        qa = qp.get(c)
        if qa is None or qv is None:
            cmp_valor(dif, 'veredictos/QWEAK/' + c, 'presencia', None if qa is None else 'presente',
                      None if qv is None else 'presente')
            continue
        cmp_valor(dif, 'veredictos/QWEAK/' + c, 'banda', qa.get('banda'), qv['banda'])
        cmp_valor(dif, 'veredictos/QWEAK/' + c, 'DQWEAK_Hz', qa.get('DQWEAK_Hz'), qv['DQWEAK_Hz'], TOL_K_INTERVALO)
    tp = vp.get('T3') or {}
    if sorted(tp) != sorted(vv['T3']):
        dif.anotar('veredictos/T3', 'celdas', sorted(tp), sorted(vv['T3']), 'otras celdas')
    for c, tv in sorted(vv['T3'].items()):
        ta = tp.get(c) or {}
        cmp_valor(dif, 'veredictos/T3/' + c, 'estado', ta.get('estado'), tv['estado'])
        for campo in ('DQ2_Hz', 'r_Q1', 'c_X', 's4'):
            if campo in tv or campo in ta:
                cmp_valor(dif, 'veredictos/T3/' + c, campo, ta.get(campo), tv.get(campo), TOL_K_INTERVALO)
    return dif.lista


def veredictos_resumidos(v):
    return {'P_T1_B': v['P_T1_B']['veredicto'], 'P_T2_B': v['P_T2_B']['veredicto'], 'F_C': v['F_C'],
            'F_R01': v['F_R01']['firma']}


def fase_K(agr, espejo, propio, registro, tecnica_T):
    inv_p, inv_v = set(agr.get('invalidas', [])), set(propio['invalidas'])
    k1 = []
    for c in sorted(inv_v - inv_p):
        codigos = sorted({x['codigo'] for x in tecnica_T['fallas'] if x['celda'] == c})
        globales = sorted({x['codigo'] for x in tecnica_T['fallas'] if x['celda'] is None})
        k1.append({'celda': c, 'lado': 'solo_verificador', 'codigos_verificador': codigos or globales,
                   'clase': 'HUECO_DEL_CONTROL',
                   'por_que': 'la fase T ve una falla tecnica en la celda y el control del productor no'})
    for c in sorted(inv_p - inv_v):
        k1.append({'celda': c, 'lado': 'solo_productor',
                   'motivos_productor': (agr.get('casos', {}).get(c) or {}).get('motivos'),
                   'clase': 'SIN_CLASIFICAR', 'por_que': 'el productor invalida y la fase T no ve falla'})
    k2 = comparar(agr, espejo, registro)
    for d in k2:
        d['clase'] = 'SIN_CLASIFICAR'
    if propio is espejo:
        k3 = []
    else:
        k3 = comparar(agr, propio, registro)
        clase = 'DERIVADA_DE_INVALIDAS' if not k2 else 'SIN_CLASIFICAR'
        for d in k3:
            d['clase'] = clase
    sin_clasificar = (sum(1 for x in k1 if x['clase'] == 'SIN_CLASIFICAR') + len(k2)
                      + sum(1 for d in k3 if d['clase'] == 'SIN_CLASIFICAR'))
    return {'resultado': 'CONCORDANTE' if sin_clasificar == 0 else 'DISCORDANTE',
            'sin_clasificar': sin_clasificar,
            'tolerancias': {'intervalos': 'abs <= 1e-9 * max(1, |productor|)', 'pruebas': 'abs <= 1e-12'},
            'K1_celdas_invalidas': {'productor': sorted(inv_p), 'verificador': sorted(inv_v), 'diferencias': k1},
            'K2_espejo': {'que_es': 'fase S propia con las celdas invalidas del productor: aisla los motores',
                          'n_diferencias': len(k2), 'diferencias': k2[:MAX_DIFERENCIAS_ESCRITAS]},
            'K3_propio': {'que_es': 'fase S propia con la regla de invalidez propia',
                          'n_diferencias': len(k3), 'diferencias': k3[:MAX_DIFERENCIAS_ESCRITAS],
                          'veredictos_productor': veredictos_resumidos_agr(agr),
                          'veredictos_verificador': veredictos_resumidos(propio['veredictos'])}}


def veredictos_resumidos_agr(agr):
    v = agr.get('veredictos', {})
    return {'P_T1_B': (v.get('P_T1_B') or {}).get('veredicto'), 'P_T2_B': (v.get('P_T2_B') or {}).get('veredicto'),
            'F_C': v.get('F_C'), 'F_R01': (v.get('F_R01') or {}).get('firma')}

# ----------------------------------------------------------------------------
# Principal


def main(argv=None):
    ap = argparse.ArgumentParser(description='Verificador independiente de 009-A1 (orden 2026-11-03-009).')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--salida', required=True)
    ap.add_argument('--sobre')
    ap.add_argument('--agregado-productor')
    ap.add_argument('--fases', default='ETSK')
    ap.add_argument('--abrir-sobre', action='store_true')
    a = ap.parse_args(argv)
    t0 = time.time()
    fases = set(a.fases.upper())
    if not fases <= set('ETSK') or 'E' not in fases:
        print('USO: --fases tiene que incluir E y solo letras de ETSK')
        return 2
    if fases & set('TSK') and not a.sobre:
        print('USO: las fases T, S y K necesitan --sobre')
        return 2
    if 'K' in fases and not a.agregado_productor:
        print('USO: la fase K necesita --agregado-productor')
        return 2
    if a.sobre and 'corrida_' in os.path.abspath(a.sobre) and not a.abrir_sobre:
        print('NEGADO: el sobre esta en una ruta con "corrida_" y falta --abrir-sobre '
              '(hace falta la autorizacion escrita de Abraham, orden 009 seccion 8)')
        return 2
    os.makedirs(a.salida, exist_ok=True)
    entorno = {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__,
               'verificador_version': VERSION, 'verificador_sha256': sha256_archivo(os.path.abspath(__file__))}
    print('verificador_a1 %s | python %s | numpy %s | scipy %s' % (VERSION, entorno['python'], entorno['numpy'],
                                                                  entorno['scipy']))
    print('verificador_sha256 %s' % entorno['verificador_sha256'])
    e_res, man, plan, registro = fase_E(a.manifiesto, a.sha_manifiesto)
    tecnica = {'version': VERSION, 'entorno': entorno, 'fase_E': e_res}
    print('E: %s | manifiesto %s | fallas %d' % (e_res['estado'], e_res['sha256'], len(e_res['fallas'])))
    if e_res['estado'] == 'PARADA':
        escribir_json(os.path.join(a.salida, 'verificacion_tecnica.json'), tecnica)
        print('PARADA: el manifiesto no es el del pin')
        return 2
    print('E: conteo %s | registro %d ids sha256 %s' % (e_res['conteo'], e_res['registro']['n'],
                                                         e_res['registro']['sha256']))
    for x in e_res['fallas']:
        print('E FALLA %s: %s' % (x['codigo'], x['detalle']))
    with open(os.path.join(a.salida, 'registro_ids.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(registro) + '\n')
    codigo_salida = 0 if e_res['estado'] == 'OK' else 1
    if not fases & set('TSK'):
        sha = escribir_json(os.path.join(a.salida, 'verificacion_tecnica.json'), tecnica)
        print('verificacion_tecnica.json sha256 %s' % sha)
        return codigo_salida
    t_res, unicos = fase_T(man, a.sha_manifiesto, os.path.abspath(a.sobre), plan, a.abrir_sobre)
    tecnica['fase_T'] = t_res
    if t_res['estado'] == 'NEGADO':
        escribir_json(os.path.join(a.salida, 'verificacion_tecnica.json'), tecnica)
        print('NEGADO: %s' % t_res['detalle'])
        return 2
    sha_t = escribir_json(os.path.join(a.salida, 'verificacion_tecnica.json'), tecnica)
    print('T: %s | lineas %d | fallas %d (globales %d) | celdas invalidas %d | entorno uniforme %s'
          % (t_res['estado'], t_res['n_lineas_leidas'], t_res['n_fallas'], t_res['fallas_globales'],
             len(t_res['celdas_invalidas']), t_res['entorno']['uniforme']))
    print('T: por codigo %s' % json.dumps(t_res['por_codigo'], sort_keys=True))
    for x in t_res['fallas'][:60]:
        print('T FALLA %s | %s | %s | %s | %s' % (x['codigo'], x['ensayo'], x['celda'], x['donde'], x['detalle']))
    print('verificacion_tecnica.json sha256 %s' % sha_t)
    if t_res['estado'] != 'OK':
        codigo_salida = 1
    if not fases & set('SK'):
        return codigo_salida
    if e_res['estado'] != 'OK':
        print('S: no se calcula porque la fase E fallo')
        return 1
    ruta_propio = os.path.join(a.salida, 'verificador_a1.json')
    inv_propias = set(t_res['celdas_invalidas'])
    if 'S' in fases:
        t1 = time.time()
        propio = fase_S(man, plan, registro, unicos, inv_propias, 'propio')
        sha_s = escribir_json(ruta_propio, propio)
        print('S: %.1f s | invalidas %d | no calculables %d | motores %s'
              % (time.time() - t1, len(propio['invalidas']), len(propio['no_calculables']),
                 json.dumps(propio['motores']['chequeos'], sort_keys=True)))
        print('verificador_a1.json sha256 %s' % sha_s)
    else:
        with open(ruta_propio, 'rb') as f:
            crudo = f.read()
        propio = json.loads(crudo.decode('utf-8'))
        print('S: leido verificador_a1.json ya escrito, sha256 %s' % hashlib.sha256(crudo).hexdigest())
        if sorted(propio['invalidas']) != sorted(inv_propias | {x['celda'] for x in propio['no_calculables']}):
            print('K: el verificador_a1.json escrito no corresponde a esta fase T')
            return 1
    malos = {k: v for k, v in propio['motores']['chequeos'].items()
             if k not in ('degenerados', 'scipy_llamadas') and v}
    if malos:
        print('S: chequeos del motor con problemas: %s' % malos)
        codigo_salida = 1
    if t_res['todos_sinteticos']:
        print('S (sintetico): veredictos %s' % json.dumps(veredictos_resumidos(propio['veredictos']), sort_keys=True))
    if 'K' not in fases:
        print('tiempo total %.1f s' % (time.time() - t0))
        return codigo_salida
    with open(a.agregado_productor, 'rb') as f:
        crudo = f.read()
    agr = json.loads(crudo.decode('utf-8'))
    print('K: agregado del productor sha256 %s' % hashlib.sha256(crudo).hexdigest())
    inv_p = set(agr.get('invalidas', []))
    if inv_p == set(propio['invalidas']):
        espejo = propio
    else:
        t1 = time.time()
        espejo = fase_S(man, plan, registro, unicos, inv_p, 'espejo')
        sha_e = escribir_json(os.path.join(a.salida, 'verificador_a1_espejo.json'), espejo)
        print('S espejo: %.1f s | verificador_a1_espejo.json sha256 %s' % (time.time() - t1, sha_e))
    cot = fase_K(agr, espejo, propio, registro, t_res)
    cot['agregado_productor_sha256'] = hashlib.sha256(crudo).hexdigest()
    cot['verificador_a1_sha256'] = sha256_archivo(ruta_propio)
    sha_k = escribir_json(os.path.join(a.salida, 'cotejo_a1.json'), cot)
    print('K: %s | sin clasificar %d | K1 %d celdas | K2 espejo %d diferencias | K3 propio %d diferencias'
          % (cot['resultado'], cot['sin_clasificar'], len(cot['K1_celdas_invalidas']['diferencias']),
             cot['K2_espejo']['n_diferencias'], cot['K3_propio']['n_diferencias']))
    for x in cot['K1_celdas_invalidas']['diferencias']:
        print('K1 %s %s %s %s' % (x['celda'], x['lado'], x['clase'], x.get('codigos_verificador',
                                                                           x.get('motivos_productor'))))
    for x in cot['K2_espejo']['diferencias'][:40]:
        print('K2 %s | %s | productor %s | verificador %s | %s' % (x['donde'], x['campo'], x['productor'],
                                                                   x['verificador'], x['regla']))
    if t_res['todos_sinteticos'] and cot['K3_propio']['n_diferencias']:
        print('K3 (sintetico) veredictos productor %s' % json.dumps(cot['K3_propio']['veredictos_productor'],
                                                                     sort_keys=True))
        print('K3 (sintetico) veredictos verificador %s' % json.dumps(cot['K3_propio']['veredictos_verificador'],
                                                                       sort_keys=True))
    print('cotejo_a1.json sha256 %s' % sha_k)
    print('tiempo total %.1f s' % (time.time() - t0))
    if cot['resultado'] != 'CONCORDANTE':
        codigo_salida = 1
    return codigo_salida


if __name__ == '__main__':
    sys.exit(main())
