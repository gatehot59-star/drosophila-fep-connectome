#!/usr/bin/env python3
"""validar_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-005).

Control del PRODUCTOR sobre recibos de 009-A1. El verificador distinto del productor que pide 010 (seccion 9) lo
escribe otro agente. Revisa identidad, D', huella de mascara, eventos por grupo y semilla, pareado entre brazos, plan
completo sin faltantes ni duplicados, SHAM identico a C0 espiga por espiga, estado tecnico y un solo code_commit.
Uso: python3 validar_a1.py --manifiesto M --sha-manifiesto H --registros DIR (--humo | --ids a,b) [--salida V.json]
Exit 0 si el conjunto es valido; 1 si no.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun_a1 as C  # noqa: E402

OBLIGATORIOS = ('identidad', 'Dprime', 'mascara', 'eventos', 'fuentes', 'orden_sinapsis', 'signo_pesos')


def leer_registros(d):
    out = []
    for n in sorted(os.listdir(d)):
        if n.endswith('.json'):
            with open(os.path.join(d, n), encoding='utf-8') as f:
                try:
                    out.append((n, json.load(f)))
                except ValueError:
                    out.append((n, None))
    return out


def validar(man, sha_man, registros, seleccion):
    fallos = []

    def falla(cod, det):
        fallos.append({'codigo': cod, 'detalle': det})

    celdas = {(c['sujeto'], c['regimen']): c for c in man['celdas']}
    vistos = {}
    for nombre, r in registros:
        if not isinstance(r, dict):
            falla('ILEGIBLE', nombre)
            continue
        try:
            tid = C.id_ensayo(r['subject_id'], r['regime'], r['condition'], r['seed'])
        except (KeyError, TypeError, ValueError):
            falla('ILEGIBLE', nombre)
            continue
        vistos.setdefault(tid, []).append((nombre, r))
    for tid, lst in sorted(vistos.items()):
        if len(lst) > 1:
            falla('DUPLICADO', '%s en %s' % (tid, [n for n, _ in lst]))
    esperados = set(seleccion)
    for tid in sorted(esperados - set(vistos)):
        falla('FALTANTE', tid)
    for tid in sorted(set(vistos) - esperados):
        falla('FUERA_DE_SELECCION', tid)
    commits, por_semilla = set(), {}
    for tid, lst in sorted(vistos.items()):
        for nombre, r in lst:
            suj = man['sujetos'].get(r['subject_id'])
            c = celdas.get((r['subject_id'], r['regime']))
            if suj is None or c is None or r['condition'] not in c['condiciones']:
                falla('FUERA_DEL_PLAN', tid)
                continue
            if r.get('protocol_id') != C.PROTOCOLO:
                falla('PROTOCOLO', tid)
            if r.get('manifiesto_sha256') != sha_man:
                falla('MANIFIESTO', tid)
            if r.get('estado') != 'OK' or r.get('exit') != 0:
                falla('ESTADO_TECNICO', '%s: %s' % (tid, r.get('motivo')))
            chq = r.get('chequeos') or {}
            req = list(OBLIGATORIOS) + ([] if r['condition'] == 'C0' else ['pesos_fuera_intactos', 'mascara_en_cero'])
            if any(chq.get(k) is not True for k in req):
                falla('CHEQUEO_INTERNO', tid)
            idn = r.get('identidad') or {}
            if (idn.get('x') != suj['x'] or idn.get('G') != suj['G'] or idn.get('d') != suj.get('d')
                    or idn.get('roots') != suj['roots']):
                falla('IDENTIDAD', tid)
            if r.get('Dprime_hash') != suj['Dp_huella']['sha256'] or r.get('Dprime_n') != suj['Dp_huella']['n']:
                falla('DPRIME', tid)
            hc = suj['huellas_condicion'].get(r['condition'], {})
            if [r.get('mask_hash'), r.get('mask_n'), r.get('mask_abs')] != [hc.get('sha256'), hc.get('n'), hc.get('abs')]:
                falla('MASCARA', tid)
            ev = man['grupos'].get(c['grupo'], {}).get('eventos', {}).get(str(r['seed']))
            if r.get('grupo') != c['grupo'] or ev is None or r.get('input_events_hash') != ev['sha256']:
                falla('EVENTOS', tid)
            if r.get('mirar_huella') != C.huella_lista(suj['mirar']) or len(r.get('cuentas_mirar') or []) != len(suj['mirar']):
                falla('LECTURA', tid)
            commits.add(str(r.get('code_commit')))
            por_semilla.setdefault((r['subject_id'], r['regime'], int(r['seed'])), {})[r['condition']] = r
    if len(commits) > 1:
        falla('CODE_COMMIT_MIXTO', sorted(commits))
    for (sid, reg, s), conds in sorted(por_semilla.items()):
        k = '%s|%s|%d' % (sid, reg, s)
        if len({r.get('input_events_hash') for r in conds.values()}) > 1:
            falla('ENTRADA_DESIGUAL', k)
        if 'C0' in conds and 'SHAM' in conds:
            a, b = conds['C0'], conds['SHAM']
            if (a.get('espigas_sha256') != b.get('espigas_sha256') or a.get('cuentas_mirar') != b.get('cuentas_mirar')
                    or a.get('espigas_total') != b.get('espigas_total')):
                falla('SHAM_DISTINTO_DE_C0', k)
    return {'estado': 'OK' if not fallos else 'INVALIDO_TECNICO', 'n_registros': sum(len(v) for v in vistos.values()),
            'n_esperados': len(esperados), 'n_fallos': len(fallos), 'fallos': fallos}


def main():
    ap = argparse.ArgumentParser(description='Control del productor sobre recibos de 009-A1')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--registros', required=True)
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--ids', default='')
    ap.add_argument('--salida', default='')
    a = ap.parse_args()
    sha = C.sha_archivo(a.manifiesto)
    if sha != a.sha_manifiesto:
        print('ABORTA: el manifiesto no es el esperado (%s)' % sha, flush=True)
        raise SystemExit(1)
    with open(a.manifiesto, encoding='utf-8') as f:
        man = json.load(f)
    sel = list(man['humo']) if a.humo else [x for x in a.ids.split(',') if x]
    v = validar(man, sha, leer_registros(a.registros), sel)
    for x in v['fallos']:
        print('FALLA %s %s' % (x['codigo'], x['detalle']), flush=True)
    print('VALIDACION %s registros=%d esperados=%d fallos=%d' % (v['estado'], v['n_registros'], v['n_esperados'], v['n_fallos']), flush=True)
    if a.salida:
        with open(a.salida, 'w', encoding='utf-8') as f:
            json.dump(v, f, sort_keys=True, indent=1)
    raise SystemExit(0 if v['estado'] == 'OK' else 1)


if __name__ == '__main__':
    main()
