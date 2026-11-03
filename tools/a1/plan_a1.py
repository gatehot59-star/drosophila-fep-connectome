#!/usr/bin/env python3
"""plan_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-006).

Reparte el plan de 009-A1 en bloques para correrlo en paralelo sin partir ninguna celda. La unidad es la celda
(sujeto, regimen) entera: sus condiciones por sus 20 semillas van al mismo bloque, asi cada comparacion pareada sale
del mismo binario en la misma maquina. Reparto LPT determinista: celdas de mayor a menor (empate por sujeto y
regimen), cada una al bloque con menos ensayos (empate, el de menor numero).
Uso:
  python3 plan_a1.py --manifiesto M --sha-manifiesto H --bloques 20 --bloque K --salida ids.txt [--resumen]
  python3 plan_a1.py --manifiesto M --sha-manifiesto H --bloques 20 --resumen --prueba
Exit 0 si el reparto cubre el plan exacto sin duplicados ni celdas partidas; 1 si no; 2 si el manifiesto no es el
esperado.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun_a1 as C  # noqa: E402


def ids_celda(c):
    return [C.id_ensayo(c['sujeto'], c['regimen'], cond, s) for cond in c['condiciones'] for s in C.SEMILLAS_PLAN]


def ids_plan(man):
    return [t for c in man['celdas'] for t in ids_celda(c)]


def repartir(celdas, n):
    orden = sorted(celdas, key=lambda c: (-len(c['condiciones']), c['sujeto'], c['regimen']))
    carga, bloques = [0] * n, [[] for _ in range(n)]
    for c in orden:
        k = min(range(n), key=lambda b: (carga[b], b))
        bloques[k].extend(ids_celda(c))
        carga[k] += len(c['condiciones']) * len(C.SEMILLAS_PLAN)
    return bloques


def chequear(man, bloques):
    """Mira solo las listas de ids: el plan exacto, cada ensayo una vez y cada celda en un solo bloque."""
    plan = ids_plan(man)
    visto, celda_bloques = {}, {}
    for k, ids in enumerate(bloques):
        for t in ids:
            visto[t] = visto.get(t, 0) + 1
            sj, rg, _, _ = t.split('|')
            celda_bloques.setdefault((sj, rg), set()).add(k)
    dup = sorted(t for t, v in visto.items() if v > 1)
    falt = sorted(set(plan) - set(visto))
    extra = sorted(set(visto) - set(plan))
    partidas = sorted('%s|%s' % c for c, b in celda_bloques.items() if len(b) > 1)
    ok = (not dup and not falt and not extra and not partidas and len(set(plan)) == len(plan)
          and len(plan) == man['n_ensayos_plan'])
    return {'ok': ok, 'n_plan': len(plan), 'n_manifiesto': man['n_ensayos_plan'], 'n_duplicados': len(dup),
            'n_faltantes': len(falt), 'n_extra': len(extra), 'n_celdas_partidas': len(partidas),
            'cargas': [len(b) for b in bloques]}


def prueba(man, n):
    """El chequeo tiene que dar rojo con un ensayo movido de bloque, uno faltante y uno duplicado."""
    bien = repartir(man['celdas'], n)
    movido = [list(b) for b in bien]
    movido[1].append(movido[0].pop())
    faltante = [list(b) for b in bien]
    faltante[0].pop()
    duplicado = [list(b) for b in bien]
    duplicado[0].append(duplicado[0][0])
    r0, r1, r2, r3 = (chequear(man, b) for b in (bien, movido, faltante, duplicado))
    casos = [('limpio', r0['ok']),
             ('movido_parte_una_celda', not r1['ok'] and r1['n_celdas_partidas'] == 1 and r1['n_faltantes'] == 0),
             ('faltante', not r2['ok'] and r2['n_faltantes'] == 1),
             ('duplicado', not r3['ok'] and r3['n_duplicados'] == 1)]
    for nombre, ok in casos:
        print('PRUEBA_PLAN %s %s' % (nombre, 'PASS' if ok else 'FAIL'), flush=True)
    return all(ok for _, ok in casos)


def main():
    ap = argparse.ArgumentParser(description='Reparto del plan de 009-A1 en bloques')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--bloques', type=int, required=True)
    ap.add_argument('--bloque', type=int, default=-1)
    ap.add_argument('--salida', default='')
    ap.add_argument('--resumen', action='store_true')
    ap.add_argument('--prueba', action='store_true')
    a = ap.parse_args()
    sha = C.sha_archivo(a.manifiesto)
    if sha != a.sha_manifiesto:
        print('ABORTA: el manifiesto tiene sha256 %s y se esperaba %s' % (sha, a.sha_manifiesto), flush=True)
        raise SystemExit(2)
    with open(a.manifiesto, encoding='utf-8') as f:
        man = json.load(f)
    bloques = repartir(man['celdas'], a.bloques)
    ch = chequear(man, bloques)
    print('PLAN ensayos=%d manifiesto=%d bloques=%d min=%d max=%d duplicados=%d faltantes=%d extra=%d '
          'celdas_partidas=%d ok=%s' % (ch['n_plan'], ch['n_manifiesto'], len(bloques), min(ch['cargas']),
                                         max(ch['cargas']), ch['n_duplicados'], ch['n_faltantes'], ch['n_extra'],
                                         ch['n_celdas_partidas'], ch['ok']), flush=True)
    ok = ch['ok']
    if a.prueba:
        ok = prueba(man, a.bloques) and ok
    if a.resumen:
        for k, ids in enumerate(bloques):
            celdas = sorted({'%s|%s' % tuple(t.split('|')[:2]) for t in ids})
            print('BLOQUE %02d ensayos=%d celdas=%s' % (k, len(ids), ','.join(celdas)), flush=True)
    if a.bloque >= 0:
        ids = bloques[a.bloque]
        with open(a.salida, 'w', encoding='utf-8') as f:
            f.write(','.join(ids))
        print('BLOQUE_ELEGIDO %02d ensayos=%d archivo=%s' % (a.bloque, len(ids), a.salida), flush=True)
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
