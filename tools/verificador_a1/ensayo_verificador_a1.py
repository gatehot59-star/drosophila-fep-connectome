#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ensayo general del verificador contra el productor en los tres sobres sinteticos (orden 009, seccion 7).

Corre verificador_a1.py como caja cerrada sobre sobre_limpio, sobre_sucio y sobre_global, cada uno contra
el agregado_a1.json que el productor dejo en est_<escenario>/, y comprueba lo que la orden pide:
  limpio  0 fallas tecnicas y cotejo CONCORDANTE, y la fase S identica en dos corridas;
  sucio   las 19 corrupciones de SEMBRADO.json vistas, las 6 ciegas como HUECO_DEL_CONTROL y el espejo sin
          diferencias;
  global  una falla sin celda que invalida las 44 y cotejo CONCORDANTE.
Tambien coteja las huellas de los sobres y de los agregados con el anexo C de la orden.

Uso
  python3 ensayo_verificador_a1.py --verificador V --manifiesto M --sha-manifiesto SHA --trabajo DIR --salida OUT
  (DIR es el --trabajo del ensayo del productor: tiene sobre_<e>/ y est_<e>/agregado_a1.json)
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

ANEXO_C = {
    'limpio': {'SHA256SUMS': '121045455135271846cb8b45121f40994e10cbae5349fc0ede3f2d64129b82b6',
               'agregado': 'bf8e90b867af195b7c276137f7afce5c257b8bb8dec80b73c69747aefea96219'},
    'sucio': {'SHA256SUMS': '4546466dd7b1d7425da21c4a353396b9166cd80ba6056b9f0be973cf38709fa1',
              'agregado': 'c050a9ebba767b488e7f18ecc38df994651a89579c2d2d208144ac8fea3eef1b'},
    'global': {'SHA256SUMS': '76c6a87a237241f23f3c44a878e9554e1d7c57c2a1b0c0d36de8d496f0a11abd',
               'agregado': 'b873a1cbc95d716e82c993ed0d6905888db2388b303ae61ca7c1b2a158cf81d3'},
}


def sha(ruta):
    with open(ruta, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def leer(ruta):
    with open(ruta, 'rb') as f:
        return json.loads(f.read().decode('utf-8'))


def correr(a, escenario, salida):
    cmd = [sys.executable, a.verificador, '--manifiesto', a.manifiesto, '--sha-manifiesto', a.sha_manifiesto,
           '--sobre', os.path.join(a.trabajo, 'sobre_' + escenario),
           '--agregado-productor', os.path.join(a.trabajo, 'est_' + escenario, 'agregado_a1.json'),
           '--salida', salida]
    t0 = time.time()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    with open(salida + '.log', 'w', encoding='utf-8') as f:
        f.write('$ %s\n' % ' '.join(cmd))
        f.write(p.stdout)
        f.write('exit %d | %.1f s\n' % (p.returncode, time.time() - t0))
    return p.returncode, time.time() - t0


def celda_de(sembrado_celda):
    s, r = sembrado_celda.split('|')
    return '%s|%s' % (r, s)


def main():
    ap = argparse.ArgumentParser()
    for nombre in ('--verificador', '--manifiesto', '--sha-manifiesto', '--trabajo', '--salida'):
        ap.add_argument(nombre, required=True)
    a = ap.parse_args()
    os.makedirs(a.salida, exist_ok=True)
    chequeos = []

    def chequeo(nombre, ok, detalle):
        chequeos.append({'chequeo': nombre, 'ok': bool(ok), 'detalle': detalle})
        print('%s %s | %s' % ('PASS' if ok else 'FAIL', nombre, detalle))

    print('verificador %s sha256 %s' % (a.verificador, sha(a.verificador)))
    resumen = {'verificador_sha256': sha(a.verificador), 'escenarios': {}}
    for e in ('limpio', 'sucio', 'global'):
        sumas = sha(os.path.join(a.trabajo, 'sobre_' + e, 'SHA256SUMS.txt'))
        agr = sha(os.path.join(a.trabajo, 'est_' + e, 'agregado_a1.json'))
        chequeo('%s: huellas del anexo C' % e, sumas == ANEXO_C[e]['SHA256SUMS'] and agr == ANEXO_C[e]['agregado'],
                'SHA256SUMS %s %s | agregado %s %s' % (sumas[:16], 'IGUAL' if sumas == ANEXO_C[e]['SHA256SUMS']
                                                       else 'DISTINTO', agr[:16],
                                                       'IGUAL' if agr == ANEXO_C[e]['agregado'] else 'DISTINTO'))
        salida = os.path.join(a.salida, e)
        rc, seg = correr(a, e, salida)
        tec = leer(os.path.join(salida, 'verificacion_tecnica.json'))
        cot = leer(os.path.join(salida, 'cotejo_a1.json'))
        t = tec['fase_T']
        k1 = cot['K1_celdas_invalidas']['diferencias']
        resumen['escenarios'][e] = {
            'exit': rc, 'segundos': round(seg, 1), 'fallas_T': t['n_fallas'], 'por_codigo': t['por_codigo'],
            'celdas_invalidas': t['celdas_invalidas'], 'resultado_K': cot['resultado'],
            'sin_clasificar': cot['sin_clasificar'], 'K1': [(x['celda'], x['clase']) for x in k1],
            'K2': cot['K2_espejo']['n_diferencias'], 'K3': cot['K3_propio']['n_diferencias'],
            'veredictos_productor': cot['K3_propio']['veredictos_productor'],
            'veredictos_verificador': cot['K3_propio']['veredictos_verificador'],
            'sha_verificador_a1': sha(os.path.join(salida, 'verificador_a1.json')),
            'sha_cotejo_a1': sha(os.path.join(salida, 'cotejo_a1.json'))}
        sembrado = leer(os.path.join(a.trabajo, 'sobre_' + e, 'SEMBRADO.json'))
        if e == 'limpio':
            chequeo('limpio: 0 fallas tecnicas', t['n_fallas'] == 0, 'fallas %d' % t['n_fallas'])
            chequeo('limpio: cotejo CONCORDANTE sin diferencias',
                    cot['resultado'] == 'CONCORDANTE' and not k1 and cot['K2_espejo']['n_diferencias'] == 0,
                    '%s | K1 %d | K2 %d' % (cot['resultado'], len(k1), cot['K2_espejo']['n_diferencias']))
            salida2 = os.path.join(a.salida, 'limpio_bis')
            correr(a, e, salida2)
            s1, s2 = sha(os.path.join(salida, 'verificador_a1.json')), sha(os.path.join(salida2, 'verificador_a1.json'))
            chequeo('limpio: fase S identica en dos corridas', s1 == s2, '%s / %s' % (s1[:16], s2[:16]))
        elif e == 'sucio':
            corr = sembrado['corrupciones']
            todas = {celda_de(x['celda']) for x in corr}
            ciegas = {celda_de(x['celda']) for x in corr if not x['detecta_el_control_del_productor']}
            vistas = set(t['celdas_invalidas'])
            chequeo('sucio: las %d corrupciones vistas' % len(corr), todas <= vistas,
                    'faltan %s' % sorted(todas - vistas))
            chequeo('sucio: ninguna celda invalidada de mas', vistas <= todas, 'sobran %s' % sorted(vistas - todas))
            huecos = {x['celda'] for x in k1 if x['clase'] == 'HUECO_DEL_CONTROL'}
            chequeo('sucio: las %d ciegas como HUECO_DEL_CONTROL' % len(ciegas), huecos == ciegas,
                    'K1 %s' % sorted(huecos))
            chequeo('sucio: espejo sin diferencias y cotejo CONCORDANTE',
                    cot['K2_espejo']['n_diferencias'] == 0 and cot['resultado'] == 'CONCORDANTE',
                    '%s | K2 %d | K3 %d derivadas de invalidas' % (cot['resultado'], cot['K2_espejo']['n_diferencias'],
                                                                   cot['K3_propio']['n_diferencias']))
        else:
            globales = [x for x in t['fallas'] if x['celda'] is None]
            chequeo('global: falla sin celda que invalida las 44',
                    bool(globales) and len(t['celdas_invalidas']) == 44,
                    '%s | invalidas %d' % ([(x['codigo'], x['donde']) for x in globales], len(t['celdas_invalidas'])))
            chequeo('global: cotejo CONCORDANTE', cot['resultado'] == 'CONCORDANTE',
                    '%s | K1 %d | K2 %d' % (cot['resultado'], len(k1), cot['K2_espejo']['n_diferencias']))
    resumen['chequeos'] = chequeos
    with open(os.path.join(a.salida, 'ensayo_resumen.json'), 'w', encoding='utf-8') as f:
        json.dump(resumen, f, ensure_ascii=False, sort_keys=True, indent=1)
        f.write('\n')
    n_ok = sum(1 for c in chequeos if c['ok'])
    print('RESUMEN %d/%d PASS' % (n_ok, len(chequeos)))
    return 0 if n_ok == len(chequeos) else 1


if __name__ == '__main__':
    sys.exit(main())
