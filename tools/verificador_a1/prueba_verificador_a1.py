#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pruebas del verificador independiente de 009-A1 (respuesta 2026-11-03-010).

V01 huella con el formato de la orden 009 (vector conocido).
V02 inversion de signos: casos con respuesta cerrada y fuerza bruta por bloques.
V03 Holm contra un ejemplo hecho a mano.
V04 BCa: scipy consume un bloque, da la distribucion de los indices propios y el IC de D2 literal.
V05 D2: datos constantes y cociente 1 exacto salen DEGENERADO (la trampa se reproduce, no se arregla).
V06 D3: denominador observado <= 0 da SIN_ESTIMADO; uno remuestreado <= 0 da INDEFINIDO.
V07 D4: invalidar una celda no cambia el intervalo de ningun otro id.
V08 fase E sobre el manifiesto: 44 / 427 / 8.540 y registro de 722 ids.
V09 fase T sobre el sobre limpio: 0 fallas.
V10 recibos corruptos propios, distintos de los del kit: cada uno con su codigo y su celda, y nada mas.
V11 fallas sin celda: code_commit mixto, bloque alterado y linea ilegible invalidan las 44.
V12 negativas: ruta con corrida_ y recibos no sinteticos sin --abrir-sobre.
V13 cotejo: el verificador contra si mismo da 0 diferencias y una perturbacion de 1e-6 se ve.
V14 (si hay agregado del productor) fase S y K sobre el sobre limpio: CONCORDANTE.

Uso
  python3 prueba_verificador_a1.py --verificador tools/verificador_a1/verificador_a1.py \
      --manifiesto M --sha-manifiesto SHA --sobre-limpio DIR --trabajo DIR [--agregado-limpio A]
      [--pruebas V01,V02,...]

Escribe todo en --trabajo (brain-env no deja escribir en /tmp). Sale con 0 si todas pasan.
"""

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import time
import traceback

import numpy as np


def cargar(ruta):
    spec = importlib.util.spec_from_file_location('verificador_a1_bajo_prueba', ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(ruta):
    with open(ruta, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def copiar_sobre(origen, destino):
    shutil.copytree(os.path.join(origen, 'bloques'), os.path.join(destino, 'bloques'))
    shutil.copy2(os.path.join(origen, 'SHA256SUMS.txt'), os.path.join(destino, 'SHA256SUMS.txt'))


def reescribir_sumas(sobre):
    lineas = []
    for d in sorted(os.listdir(os.path.join(sobre, 'bloques'))):
        for f in sorted(os.listdir(os.path.join(sobre, 'bloques', d))):
            if f.endswith('.jsonl'):
                rel = 'bloques/%s/%s' % (d, f)
                lineas.append('%s  %s' % (sha(os.path.join(sobre, rel)), rel))
    with open(os.path.join(sobre, 'SHA256SUMS.txt'), 'w') as f:
        f.write('\n'.join(lineas) + '\n')


def editar(sobre, cambios):
    """cambios: tupla (S, R, C, seed) -> funcion(recibo) que lo modifica en el lugar."""
    hechos = set()
    for d in sorted(os.listdir(os.path.join(sobre, 'bloques'))):
        ruta = os.path.join(sobre, 'bloques', d, 'bloque_%s.jsonl' % d)
        if not os.path.exists(ruta):
            continue
        with open(ruta, 'r', encoding='utf-8') as f:
            lineas = f.read().split('\n')
        tocado = False
        for i, ln in enumerate(lineas):
            if not ln:
                continue
            r = json.loads(ln)
            t = (r['subject_id'], r['regime'], r['condition'], r['seed'])
            if t in cambios:
                cambios[t](r)
                lineas[i] = json.dumps(r, sort_keys=True, separators=(',', ':'))
                hechos.add(t)
                tocado = True
        if tocado:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lineas))
    faltan = set(cambios) - hechos
    if faltan:
        raise RuntimeError('no encontre los recibos %s' % sorted(faltan))


class Corrida:
    def __init__(self, a):
        self.a = a
        self.v = cargar(a.verificador)
        self.res = []
        self.cache = {}

    def base(self):
        if 'base' not in self.cache:
            v, a = self.v, self.a
            e, man, plan, reg = v.fase_E(a.manifiesto, a.sha_manifiesto)
            self.cache['base'] = (e, man, plan, reg)
        return self.cache['base']

    def tecnica_limpia(self):
        if 'T' not in self.cache:
            e, man, plan, reg = self.base()
            self.cache['T'] = self.v.fase_T(man, self.a.sha_manifiesto, self.a.sobre_limpio, plan, False)
        return self.cache['T']

    def s_limpio(self):
        if 'S' not in self.cache:
            e, man, plan, reg = self.base()
            t, unicos = self.tecnica_limpia()
            self.cache['S'] = self.v.fase_S(man, plan, reg, unicos, set(), 'propio')
        return self.cache['S']

    def tmp(self, nombre):
        return tempfile.mkdtemp(prefix=nombre + '_', dir=self.a.trabajo)

# ----------------------------------------------------------------------------


def v01(c):
    h = c.v.huella([3, 1, 2])
    esperado = hashlib.sha256(b'[1,2,3]\n').hexdigest()
    assert h == esperado, 'huella %s, esperada %s' % (h, esperado)
    assert c.v.huella([]) == hashlib.sha256(b'[]\n').hexdigest()
    return 'huella([3,1,2]) = sha256("[1,2,3]\\n")'


def fuerza_bruta(d):
    d = np.asarray(d, float)
    obs = abs(d.sum())
    tol = 1e-9 * (1 + np.abs(d).sum())
    total = 0
    for trozo in range(16):
        filas = np.arange(trozo * 65536, (trozo + 1) * 65536, dtype=np.int64)[:, None]
        signos = 1 - 2 * ((filas >> np.arange(20)[None, :]) & 1)
        total += int(np.count_nonzero(np.abs(signos @ d) >= obs - tol))
    return total / 2 ** 20


def v02(c):
    s = c.v.signos_bilateral
    assert s(np.ones(20)) == 2 / 2 ** 20, 'unos: %r' % s(np.ones(20))
    assert s(np.zeros(20)) == 1.0, 'ceros: %r' % s(np.zeros(20))
    mitad = np.array([1.0] * 10 + [0.0] * 10)
    assert s(mitad) == 2 ** 11 / 2 ** 20, 'mitad: %r' % s(mitad)
    rng = np.random.default_rng(7)
    for i in range(3):
        d = np.round(rng.normal(0.4, 1.0, 20), 2)
        a, b = s(d), fuerza_bruta(d)
        assert a == b, 'aleatorio %d: %r contra %r' % (i, a, b)
    return 'cerrados 3/3 y fuerza bruta 3/3'


def v03(c):
    pr = [{'estado': 'OK', 'p_familia': p} for p in (0.01, 0.04, 0.03, 0.005)]
    c.v.holm(pr)
    obtenido = [round(p['p_holm'], 12) for p in pr]
    esperado = [0.03, 0.06, 0.06, 0.02]
    assert obtenido == esperado, 'holm %s, esperado %s' % (obtenido, esperado)
    assert [p['decide'] for p in pr] == [False, False, False, False]
    pr = [{'estado': 'OK', 'p_familia': 0.001}, {'estado': 'VARIANZA_CERO', 'p_familia': 1.0},
          {'estado': 'OK', 'p_familia': 0.004}]
    c.v.holm(pr)
    assert [round(p['p_holm'], 12) for p in pr] == [0.003, 1.0, 0.008], [p['p_holm'] for p in pr]
    assert [p['decide'] for p in pr] == [True, False, True]
    return 'ejemplo a mano y centinela p_familia = 1'


def v04(c):
    v = c.v
    rng = np.random.default_rng(11)
    gen = np.random.Generator(np.random.PCG64(v.SEMILLA_BOOT))
    ref = np.random.Generator(np.random.PCG64(v.SEMILLA_BOOT))
    motor = __import__('collections').Counter()
    for i in range(6):
        if i % 2 == 0:
            cant = ('media', rng.integers(0, 12, 20).astype(float))
        else:
            cant = ('cociente', rng.integers(5, 30, 20).astype(float), rng.integers(20, 60, 20).astype(float))
        out = v.intervalo(gen, cant, motor)
        ref.integers(0, 20, size=(20000, 20))
        assert gen.bit_generator.state == ref.bit_generator.state, 'el flujo no avanzo un bloque en %d' % i
        assert out['estado_ic'] == 'OK', 'estado %s en %d' % (out['estado_ic'], i)
    malos = {k: n for k, n in motor.items() if k not in ('scipy_llamadas', 'degenerados') and n}
    assert not malos, 'chequeos del motor: %s' % malos
    assert motor['scipy_llamadas'] == 6
    return '6 intervalos con empates: flujo, distribucion e IC literal iguales a scipy'


def v05(c):
    v = c.v
    gen = np.random.Generator(np.random.PCG64(1))
    m = __import__('collections').Counter()
    a = v.intervalo(gen, ('media', np.full(20, 3.0)), m)
    assert a['estado_ic'] == 'DEGENERADO' and a['ic95'] is None and a['estimado'] == 3.0, a
    num = np.arange(20, 40, dtype=float)
    b = v.intervalo(gen, ('cociente', num, num.copy()), m)
    assert b['estado_ic'] == 'DEGENERADO' and b['estimado'] == 1.0, b
    return 'constante y r = 1 exacto: DEGENERADO, sin IC'


def v06(c):
    v = c.v
    gen = np.random.Generator(np.random.PCG64(2))
    m = __import__('collections').Counter()
    a = v.intervalo(gen, ('cociente', np.ones(20), np.array([-1.0] * 10 + [0.5] * 10)), m)
    assert a['estado_ic'] == 'SIN_ESTIMADO' and a['estimado'] is None, a
    den = np.array([20.0] + [-0.5] * 19)
    b = v.intervalo(gen, ('cociente', np.ones(20), den), m)
    assert b['estado_ic'] == 'INDEFINIDO' and b['ic95'] is None, b
    return 'SIN_ESTIMADO e INDEFINIDO'


def v07(c):
    e, man, plan, reg = c.base()
    t, unicos = c.tecnica_limpia()
    s0 = c.s_limpio()
    s1 = c.v.fase_S(man, plan, reg, unicos, {'B|R07'}, 'propio')
    distintos = [i for i in reg if not i.startswith('B|R07|') and s0['intervalos'][i] != s1['intervalos'][i]]
    assert not distintos, 'cambian %d ids, por ejemplo %s' % (len(distintos), distintos[:3])
    assert all(s1['intervalos'][i] is None for i in reg if i.startswith('B|R07|'))
    otros = sum(1 for i in reg if not i.startswith('B|R07|'))
    return '%d ids sin cambio con B|R07 invalida' % otros


def v08(c):
    e, man, plan, reg = c.base()
    assert e['estado'] == 'OK', e['fallas'][:5]
    assert e['conteo']['celdas'] == 44 and e['conteo']['condiciones'] == 427 and e['conteo']['ensayos'] == 8540
    assert len(reg) == 722 and reg == sorted(reg)
    return 'registro %s' % e['registro']['sha256']


def v09(c):
    t, unicos = c.tecnica_limpia()
    assert t['estado'] == 'OK' and t['n_fallas'] == 0, t['fallas'][:5]
    assert len(unicos) == 8540
    return '8.540 recibos, 0 fallas'


def corrupciones_propias(man):
    def pos(s, j):
        return man['sujetos'][s]['mirar'].index(j)

    def flotante(r):
        r['cuentas_mirar'][pos('R03', man['sujetos']['R03']['Dp'][0])] = 2.5

    def g_corto(r):
        r['cuentas_G'] = r['cuentas_G'][:-1]

    def activas(r):
        r['activas'] = sum(1 for v in r['cuentas_mirar'] if v != 0) - 1

    def mirar(r):
        r['mirar_huella'] = '0' * 64

    def filas(r):
        r['filas_cambiadas'] = r['filas_cambiadas'] + 1

    def chequeo(r):
        r['chequeos']['signo_pesos'] = False

    def grupo(r):
        r['grupo'] = 'g_otro'

    def exit1(r):
        r['exit'] = 1

    def sham(r):
        r['espigas_sha256'] = 'f' * 64

    def renombrar(r):
        r['condition'] = 'Q9'

    def eventos(r):
        r['input_events_hash'] = 'e' * 64

    def identidad(r):
        r['identidad']['x'] = r['identidad']['x'] + 1

    def cuenta_x(r):
        r['cuenta_x'] = r['cuenta_x'] + 3

    cambios = {('R03', 'A', 'Q2', 4): flotante, ('H2', 'B', 'Q4conj', 7): g_corto, ('R10', 'A', 'C0', 11): activas,
               ('R05', 'B', 'QXD', 2): mirar, ('R11', 'B', 'Q3', 16): filas, ('H1b', 'C', 'C_10', 9): chequeo,
               ('R14', 'A', 'QCOL', 3): grupo, ('R16', 'B', 'Q1', 18): exit1, ('R08', 'A', 'SHAM', 5): sham,
               ('H4', 'B', 'Q2', 0): renombrar, ('R02', 'A', 'Q3', 10): eventos, ('R09', 'B', 'C0', 12): identidad,
               ('R07', 'B', 'Q4', 8): cuenta_x}
    esperado = {('COHERENCIA', 'A|R03'), ('COHERENCIA', 'B|H2'), ('COHERENCIA', 'A|R10'), ('MIRAR', 'B|R05'),
                ('FILAS', 'B|R11'), ('CHEQUEO_INTERNO', 'C|H1b'), ('GRUPO', 'A|R14'), ('ESTADO_TECNICO', 'B|R16'),
                ('SHAM_DISTINTO_DE_C0', 'A|R08'), ('FUERA_DEL_PLAN', 'B|H4'), ('FALTANTE', 'B|H4'),
                ('EVENTOS', 'A|R02'), ('ENTRADA_DESIGUAL', 'A|R02'), ('IDENTIDAD', 'B|R09'),
                ('COHERENCIA', 'B|R07')}
    return cambios, esperado


def v10(c):
    e, man, plan, reg = c.base()
    d = c.tmp('v10')
    copiar_sobre(c.a.sobre_limpio, d)
    cambios, esperado = corrupciones_propias(man)
    editar(d, cambios)
    reescribir_sumas(d)
    t, _ = c.v.fase_T(man, c.a.sha_manifiesto, d, plan, False)
    vistos = {(x['codigo'], x['celda']) for x in t['fallas']}
    assert vistos == esperado, 'sobran %s; faltan %s' % (sorted(vistos - esperado), sorted(esperado - vistos))
    celdas = sorted({cc for _, cc in esperado})
    assert t['celdas_invalidas'] == celdas, t['celdas_invalidas']
    shutil.rmtree(d)
    return '13 recibos corruptos: %d pares exactos en %d celdas' % (len(esperado), len(celdas))


def v11(c):
    e, man, plan, reg = c.base()
    salidas = []
    for caso in ('commit', 'bloque', 'ilegible'):
        d = c.tmp('v11_' + caso)
        copiar_sobre(c.a.sobre_limpio, d)
        if caso == 'commit':
            def mover(r):
                r['code_commit'] = 'OTRO'
            editar(d, {('R01', 'B', 'C0', 0): mover})
            reescribir_sumas(d)
            codigo = 'CODE_COMMIT_MIXTO'
        elif caso == 'bloque':
            def leve(r):
                r['duracion_s'] = 123.0
            editar(d, {('R01', 'B', 'C0', 0): leve})
            codigo = 'INTEGRIDAD'
        else:
            ruta = os.path.join(d, 'bloques', '03', 'bloque_03.jsonl')
            with open(ruta, 'a', encoding='utf-8') as f:
                f.write('\n{esto no es json')
            reescribir_sumas(d)
            codigo = 'ILEGIBLE'
        t, _ = c.v.fase_T(man, c.a.sha_manifiesto, d, plan, False)
        assert any(x['codigo'] == codigo and x['celda'] is None for x in t['fallas']), (caso, t['por_codigo'])
        assert t['celdas_invalidas'] == sorted(plan), (caso, len(t['celdas_invalidas']))
        salidas.append(codigo)
        shutil.rmtree(d)
    return 'invalidan las 44: %s' % ', '.join(salidas)


def v12(c):
    a = c.a
    d = os.path.join(c.tmp('v12'), 'corrida_x')
    copiar_sobre(a.sobre_limpio, d)
    sal = os.path.join(a.trabajo, 'v12_salida_no_debe_existir')
    with contextlib.redirect_stdout(io.StringIO()):
        rc = c.v.main(['--manifiesto', a.manifiesto, '--sha-manifiesto', a.sha_manifiesto, '--sobre', d,
                       '--salida', sal, '--fases', 'ET'])
    assert rc == 2 and not os.path.exists(sal), 'corrida_: rc %r, salida %r' % (rc, os.path.exists(sal))
    d2 = c.tmp('v12_real')
    copiar_sobre(a.sobre_limpio, d2)
    e, man, plan, reg = c.base()

    def real(r):
        r.pop('sintetico', None)
    editar(d2, {('R01', 'A', 'C0', 0): real})
    reescribir_sumas(d2)
    t, unicos = c.v.fase_T(man, a.sha_manifiesto, d2, plan, False)
    assert t['estado'] == 'NEGADO' and unicos is None, t.get('estado')
    shutil.rmtree(os.path.dirname(d))
    shutil.rmtree(d2)
    return 'corrida_ sin --abrir-sobre: rc 2 sin salida; recibo no sintetico: NEGADO'


def v13(c):
    e, man, plan, reg = c.base()
    s = c.s_limpio()
    espejo = json.loads(json.dumps(s))
    assert c.v.comparar(espejo, s, reg) == [], 'contra si mismo hay diferencias'
    i = next(k for k in reg if s['intervalos'][k] and s['intervalos'][k]['estado_ic'] == 'OK')
    espejo['intervalos'][i]['estimado'] *= 1 + 1e-6
    dif = c.v.comparar(espejo, s, reg)
    assert len(dif) == 1 and dif[0]['donde'] == 'intervalos/' + i, dif[:3]
    return 'auto-cotejo 0 y una perturbacion de 1e-6 detectada en %s' % i


def v14(c):
    if not c.a.agregado_limpio:
        return 'SALTEADA: sin --agregado-limpio'
    e, man, plan, reg = c.base()
    t, unicos = c.tecnica_limpia()
    s = c.s_limpio()
    with open(c.a.agregado_limpio, 'rb') as f:
        agr = json.loads(f.read().decode('utf-8'))
    cot = c.v.fase_K(agr, s, s, reg, t)
    assert cot['resultado'] == 'CONCORDANTE', (cot['sin_clasificar'], cot['K2_espejo']['diferencias'][:3])
    return 'CONCORDANTE contra el agregado del productor'


PRUEBAS = [('V01', v01), ('V02', v02), ('V03', v03), ('V04', v04), ('V05', v05), ('V06', v06), ('V07', v07),
           ('V08', v08), ('V09', v09), ('V10', v10), ('V11', v11), ('V12', v12), ('V13', v13), ('V14', v14)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verificador', required=True)
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--sobre-limpio', required=True)
    ap.add_argument('--trabajo', required=True)
    ap.add_argument('--agregado-limpio')
    ap.add_argument('--pruebas')
    a = ap.parse_args()
    os.makedirs(a.trabajo, exist_ok=True)
    elegidas = set(a.pruebas.split(',')) if a.pruebas else None
    c = Corrida(a)
    print('verificador bajo prueba %s sha256 %s' % (a.verificador, sha(a.verificador)))
    pasan = fallan = 0
    for nombre, fn in PRUEBAS:
        if elegidas and nombre not in elegidas:
            continue
        t0 = time.time()
        try:
            detalle = fn(c)
            print('%s PASS (%.1f s) %s' % (nombre, time.time() - t0, detalle))
            pasan += 1
        except Exception as e:
            print('%s FAIL (%.1f s) %s: %s' % (nombre, time.time() - t0, type(e).__name__, e))
            traceback.print_exc(limit=2, file=sys.stdout)
            fallan += 1
    print('RESUMEN %d/%d PASS' % (pasan, pasan + fallan))
    return 0 if fallan == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
