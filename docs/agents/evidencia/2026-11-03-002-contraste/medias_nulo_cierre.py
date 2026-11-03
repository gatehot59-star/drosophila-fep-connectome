#!/usr/bin/env python3
# medias_nulo_cierre.py - BRAIN, 2026-11-03.
# Recalcula desde los 200 registros nulos por mosca las medias, minimos y maximos de T1 y T2 de H_REUSO_CIERRE,
# y los compara con el resumen archivado en el mismo JSON y con los numeros de la seccion 15 del Doc maestro.
# Exit 0 con la huella fijada; 2 si la entrada no es la del commit 7f3cbc1.
# Uso: python3 medias_nulo_cierre.py [--cierre RUTA]; la entrada es results/reuso_cierre_2026-11-01/cierre.json
# en el commit 7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4 del repo, verificada por sha256.
import argparse, hashlib, json, statistics as st, sys
_ap = argparse.ArgumentParser()
_ap.add_argument('--cierre', default='/workspace/r2026-11-03/cierre_7f3cbc1.json')
P = _ap.parse_args().cierre
PIN = 'a5c689d4153a9f4fcfadc573cac58521f1ade330b82d1d122dfae6f15c41aceb'
b = open(P, 'rb').read(); h = hashlib.sha256(b).hexdigest()
print('ENTRADA results/reuso_cierre_2026-11-01/cierre.json @7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4', len(b), h, 'OK' if h == PIN else 'DISTINTA')
if h != PIN:
    sys.exit(2)
d = json.loads(b)
DOC15 = {'flywire': {'t1': 0.8026, 't2': 539.86}, 'banc': {'t1': 0.7431, 't2': 328.99}}
for k in ('flywire', 'banc'):
    c = d['connectomes'][k]; nl = c['nulls']
    for key in ('t1', 't2'):
        xs = [float(x[key]) for x in nl]
        m = st.fmean(xs)
        print(k, key, 'n_nulos', len(xs), 'media', round(m, 6), 'min', min(xs), 'max', max(xs),
              'observado', c['observed'][key], 'media_resumen_archivado', c['summary'][key]['mean'],
              'igual_al_resumen', abs(m - c['summary'][key]['mean']) < 1e-9,
              'seccion15_dice', DOC15[k][key], 'seccion15_coincide', abs(m - DOC15[k][key]) <= 0.005 * max(1.0, abs(m)))
    print(k, 'p_por_prueba', c['p'])
print('p', d.get('p'), 'holm', d.get('holm'), 'H_REUSO_CIERRE', d.get('H_REUSO_CIERRE'))
