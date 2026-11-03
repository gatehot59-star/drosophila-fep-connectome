#!/usr/bin/env python3
"""prueba_sobre_sintetico_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-009).

Ensayo general del lado del PRODUCTOR sobre el sobre sintetico de 009-A1. Comprueba que el generador sea
determinista y no escriba en una ruta de corrida; que el control del productor (validar_a1.validar) acepte el
escenario limpio, marque exactamente las 13 corrupciones detectables del sucio y no vea las 6 ciegas (huecos medidos
que el verificador independiente tiene que cubrir); y que estadistica_a1.py --abrir-sobre, corrido SOLO sobre estos
sobres sinteticos, invalide las celdas que corresponde, conserve los intervalos de las celdas sanas (D4) y muestre
cada rama sembrada. Deja en --trabajo los tres agregados, sus logs y registro_ids.txt para el verificador.
No toca la corrida real: aborta si --trabajo contiene 'corrida_' y nunca lee fuera de --trabajo.
Uso: python3 prueba_sobre_sintetico_a1.py --manifiesto M --sha-manifiesto H --trabajo DIR
Exit 0 si las 13 pruebas pasan; 1 si alguna falla; 2 si el manifiesto no es el esperado o la ruta no sirve.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import comun_a1 as C  # noqa: E402
import juntar_a1 as J  # noqa: E402
import plan_a1 as P  # noqa: E402
import sobre_sintetico_a1 as S  # noqa: E402
import validar_a1 as V  # noqa: E402

PATRON = re.compile(r'^([A-Za-z0-9]+)\|([ABC])\|')
CUENTAS_TOCADAS = ('x_incoherente', 'cuenta_negativa')   # ciegas que cambian cuentas que entran a un estimando
RES = []


def prueba(nombre, ok, detalle=''):
    RES.append((nombre, bool(ok)))
    print('PRUEBA %s %s %s' % (nombre, 'PASS' if ok else 'FAIL', detalle), flush=True)


def correr(args):
    t0 = time.time()
    p = subprocess.run([sys.executable] + args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr, time.time() - t0


def generar(man_ruta, sha, esc, salida):
    return correr([os.path.join(AQUI, 'sobre_sintetico_a1.py'), '--manifiesto', man_ruta, '--sha-manifiesto', sha,
                   '--escenario', esc, '--salida', salida])


def estadistica(man_ruta, sha, sobre, dest):
    return correr([os.path.join(AQUI, 'estadistica_a1.py'), '--manifiesto', man_ruta, '--sha-manifiesto', sha,
                   '--jsonl', os.path.join(sobre, 'bloques', '*', 'bloque_*.jsonl'), '--salida', dest,
                   '--abrir-sobre'])


def leer(sobre):
    regs = []
    for ruta in sorted(glob.glob(os.path.join(sobre, 'bloques', '*', 'bloque_*.jsonl'))):
        regs.extend(J.leer_jsonl(ruta))
    return regs


def celda_sr(detalle):
    m = PATRON.match(detalle) if isinstance(detalle, str) else None
    return '%s|%s' % (m.group(1), m.group(2)) if m else None


def rs(celda):
    s, r = celda.split('|')
    return '%s|%s' % (r, s)


def campo(d, *ruta):
    """d[k1][k2]...; None si falta algo: un mutante puede dejar el agregado sin la rama que se mira."""
    for k in ruta:
        if isinstance(d, dict) and k in d:
            d = d[k]
        elif isinstance(d, list) and isinstance(k, int) and -len(d) <= k < len(d):
            d = d[k]
        else:
            return None
    return d


def leer_json(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser(description='Ensayo general del productor sobre el sobre sintetico de 009-A1')
    ap.add_argument('--manifiesto', required=True)
    ap.add_argument('--sha-manifiesto', required=True)
    ap.add_argument('--trabajo', required=True)
    a = ap.parse_args()
    trabajo = os.path.abspath(a.trabajo)
    if 'corrida_' in trabajo.lower():
        print('ABORTA: %s parece una ruta de corrida real' % trabajo, flush=True)
        raise SystemExit(2)
    sha = C.sha_archivo(a.manifiesto)
    if sha != a.sha_manifiesto:
        print('ABORTA: el manifiesto tiene sha256 %s y se esperaba %s' % (sha, a.sha_manifiesto), flush=True)
        raise SystemExit(2)
    man = leer_json(a.manifiesto)
    os.makedirs(trabajo, exist_ok=True)
    t0 = time.time()
    sobres = {e: os.path.join(trabajo, 'sobre_' + e) for e in ('limpio', 'limpio_bis', 'sucio', 'global')}
    for e, ruta in sobres.items():
        rc, out, err, seg = generar(a.manifiesto, sha, e.replace('_bis', ''), ruta)
        print('GENERAR %s exit=%d %.1f s %s %s' % (e, rc, seg, out.strip(), err.strip()[-300:]), flush=True)

    def bytes_de(ruta):
        with open(ruta, 'rb') as f:
            return f.read()

    iguales = all(bytes_de(os.path.join(sobres['limpio'], x)) == bytes_de(os.path.join(sobres['limpio_bis'], x))
                  for x in ['SHA256SUMS.txt', 'SEMBRADO.json']
                  + ['bloques/%02d/bloque_%02d.jsonl' % (k, k) for k in range(S.N_BLOQUES)])
    prueba('S01_generador_determinista', iguales, 'SHA256SUMS=%s' % C.sha_archivo(
        os.path.join(sobres['limpio'], 'SHA256SUMS.txt')))
    falsa = os.path.join(trabajo, 'corrida_falsa')
    rc, out, _, _ = generar(a.manifiesto, sha, 'limpio', falsa)
    prueba('S02_rechaza_ruta_de_corrida', rc == 2 and not os.path.exists(falsa), 'exit=%d' % rc)

    regs = leer(sobres['limpio'])
    v = V.validar(man, sha, regs, P.ids_plan(man))
    sint = all(isinstance(r, dict) and r.get('sintetico') is True and r.get('code_commit') == S.CODE_COMMIT
               for _, r in regs)
    prueba('S03_limpio_pasa_el_control_del_productor',
           v['estado'] == 'OK' and v['n_fallos'] == 0 and v['n_registros'] == len(regs) == man['n_ensayos_plan']
           and sint, 'estado=%s registros=%d fallos=%d todos_sinteticos=%s' % (
               v['estado'], v['n_registros'], v['n_fallos'], sint))

    sem = leer_json(os.path.join(sobres['sucio'], 'SEMBRADO.json'))
    vs = V.validar(man, sha, leer(sobres['sucio']), P.ids_plan(man))
    obtenido = sorted({(f['codigo'], celda_sr(f['detalle'])) for f in vs['fallos']})
    esperado = sorted({(cod, c['celda']) for c in sem['corrupciones'] if c['detecta_el_control_del_productor']
                       for cod in c['codigos_productor']})
    n_det = sum(1 for c in sem['corrupciones'] if c['detecta_el_control_del_productor'])
    prueba('S04_sucio_el_control_marca_las_13_detectables',
           obtenido == esperado and n_det == 13 and len(esperado) == 15,
           'corrupciones=%d pares=%d esperados=%d sobran=%s faltan=%s' % (n_det, len(obtenido), len(esperado),
                                                          sorted(set(obtenido) - set(esperado)),
                                                          sorted(set(esperado) - set(obtenido))))
    ciegas = {c['celda'] for c in sem['corrupciones'] if not c['detecta_el_control_del_productor']}
    vistas = {celda_sr(f['detalle']) for f in vs['fallos']}
    prueba('S05_sucio_el_control_no_ve_las_6_ciegas', len(ciegas) == 6 and not (ciegas & vistas),
           'ciegas=%s' % ','.join(sorted(ciegas)))
    vg = V.validar(man, sha, leer(sobres['global']), P.ids_plan(man))
    il = [f for f in vg['fallos'] if f['codigo'] == 'ILEGIBLE']
    prueba('S06_global_una_linea_ilegible_sin_celda',
           vg['n_fallos'] == 1 and len(il) == 1 and celda_sr(il[0]['detalle']) is None,
           'fallos=%s' % [(f['codigo'], f['detalle']) for f in vg['fallos']])

    corridas = {}
    for nombre, sobre in (('limpio', sobres['limpio']), ('limpio_bis', sobres['limpio']), ('sucio', sobres['sucio']),
                          ('global', sobres['global'])):
        dest = os.path.join(trabajo, 'est_' + nombre)
        rc, out, err, seg = estadistica(a.manifiesto, sha, sobre, dest)
        ag = os.path.join(dest, 'agregado_a1.json')
        corridas[nombre] = (rc, C.sha_archivo(ag) if os.path.exists(ag) else None)
        print('ESTADISTICA %s exit=%d %.1f s agregado_sha256=%s %s' % (nombre, rc, seg, corridas[nombre][1],
                                                                      err.strip()[-300:]), flush=True)
    prueba('S07_estadistica_limpio_exit_0_y_determinista',
           corridas['limpio'][0] == 0 and corridas['limpio_bis'][0] == 0
           and corridas['limpio'][1] is not None and corridas['limpio'][1] == corridas['limpio_bis'][1],
           'sha=%s' % corridas['limpio'][1])
    L = leer_json(os.path.join(trabajo, 'est_limpio', 'agregado_a1.json'))
    Su = leer_json(os.path.join(trabajo, 'est_sucio', 'agregado_a1.json'))
    Gl = leer_json(os.path.join(trabajo, 'est_global', 'agregado_a1.json'))
    inval_esp = sorted({rs(c['celda']) for c in sem['corrupciones'] if c['detecta_el_control_del_productor']})
    ciegas_rs = {rs(c) for c in ciegas}
    prueba('S08_sucio_invalida_las_13_celdas_y_ninguna_ciega',
           corridas['sucio'][0] == 1 and Su['invalidas'] == inval_esp and not (ciegas_rs & set(Su['invalidas']))
           and L['invalidas'] == [], 'invalidas=%s' % ','.join(Su['invalidas']))
    tocadas = {rs(c['celda']) for c in sem['corrupciones'] if c['tipo'] in CUENTAS_TOCADAS}
    sanas, distintas, malos = 0, 0, []
    for qid, iv in sorted(L['intervalos'].items()):
        celda = '|'.join(qid.split('|')[:2])
        if celda in Su['invalidas']:
            continue
        if celda in tocadas:
            distintas += int(iv != Su['intervalos'].get(qid))
        elif iv == Su['intervalos'].get(qid):
            sanas += 1
        else:
            malos.append(qid)
    prueba('S09_D4_celdas_sanas_con_intervalos_identicos_y_las_ciegas_contaminan',
           not malos and sanas > 0 and distintas > 0,
           'identicos=%d distintos_en_ciegas=%d distintos_indebidos=%s' % (sanas, distintas, malos[:5]))
    prueba('S10_global_invalida_las_44',
           corridas['global'][0] == 1 and len(Gl['invalidas']) == len(man['celdas']) == 44
           and campo(Gl, 'veredictos', 'P_T1_B', 'veredicto') == 'INVALIDO_TECNICO'
           and campo(Gl, 'veredictos', 'P_T2_B', 'veredicto') == 'INVALIDO_TECNICO'
           and campo(Gl, 'veredictos', 'F_R01', 'firma') == 'INVALIDO_TECNICO'
           and set((campo(Gl, 'veredictos', 'F_C') or {'x': None}).values()) == {'INVALIDO_TECNICO'},
           'invalidas=%d' % len(Gl['invalidas']))
    trampa = {'B|R02|r_Q1': campo(L, 'intervalos', 'B|R02|r_Q1', 'estado_ic'),
              'B|R02|c_X': campo(L, 'intervalos', 'B|R02|c_X', 'estado_ic'),
              'B|H3|r_Q1conj': campo(L, 'intervalos', 'B|H3|r_Q1conj', 'estado_ic'),
              'B|H3|c_Xconj': campo(L, 'intervalos', 'B|H3|c_Xconj', 'estado_ic'),
              'T1 R02': campo(L, 'casos', 'B|R02', 'T1', 'estado'), 'T2 H3': campo(L, 'casos', 'B|H3', 'T2', 'estado'),
              'P_T1_B': campo(L, 'veredictos', 'P_T1_B', 'veredicto')}
    prueba('S11_trampa_del_bca_degenerado_tal_cual_010',
           trampa == {'B|R02|r_Q1': 'DEGENERADO', 'B|R02|c_X': 'DEGENERADO', 'B|H3|r_Q1conj': 'DEGENERADO',
                      'B|H3|c_Xconj': 'DEGENERADO', 'T1 R02': 'NO_PASA:SIN_DECIDIR', 'T2 H3': 'NO_PASA:SIN_DECIDIR',
                      'P_T1_B': 'SIN_DECIDIR'}, json.dumps(trampa, sort_keys=True))
    hi_r12 = campo(L, 'casos', 'B|R12', 'cocientes', 'r_Q1', 'ic95', 1)
    ramas = {
        'B|R01 T1 PASA': campo(L, 'casos', 'B|R01', 'T1', 'estado') == 'PASA',
        'B|R03 T1 PASA': campo(L, 'casos', 'B|R03', 'T1', 'estado') == 'PASA',
        'B|R05 NO_INFORMATIVO': campo(L, 'casos', 'B|R05', 'estado') == 'NO_INFORMATIVO_EN_B',
        'B|R06 NO_INFORMATIVO': campo(L, 'casos', 'B|R06', 'estado') == 'NO_INFORMATIVO_EN_B',
        'B|R12 IC de r_Q1 bajo 0,35': hi_r12 is not None and hi_r12 < 0.35,
        'A|R04 RECLUTADO': campo(L, 'casos', 'A|R04', 'estado') == 'RECLUTADO',
        'A|R05 NO_RECLUTADO': campo(L, 'casos', 'A|R05', 'estado') == 'NO_RECLUTADO_EN_A',
        'A|R06 c_X SIN_ESTIMADO': campo(L, 'casos', 'A|R06', 'cocientes', 'c_X',
                                        'estado_ic_calculado') == 'SIN_ESTIMADO',
        'A|R07 r_Q1 SIN_ESTIMADO': campo(L, 'casos', 'A|R07', 'cocientes', 'r_Q1',
                                         'estado_ic_calculado') == 'SIN_ESTIMADO',
        'B|R08 QWEAK PEQUENO': campo(L, 'casos', 'B|R08', 'qweak', 'banda') == 'PEQUENO',
        'B|R09 QWEAK INTERMEDIO': campo(L, 'casos', 'B|R09', 'qweak', 'banda') == 'INTERMEDIO',
        'B|R10 QWEAK ALTO': campo(L, 'casos', 'B|R10', 'qweak', 'banda') == 'ALTO',
        'C|H1 OR': campo(L, 'casos', 'C|H1', 'transferencia') == 'OR_COMPATIBLE_EN_C',
        'C|H1b AND': campo(L, 'casos', 'C|H1b', 'transferencia') == 'AND_COMPATIBLE_EN_C',
        'C|H2 INDETERMINADO': campo(L, 'casos', 'C|H2', 'transferencia') == 'INDETERMINADO',
        'C|H3 OTRA': campo(L, 'casos', 'C|H3', 'transferencia') == 'OTRA_TRANSFERENCIA',
        'C|H4 FC VARIANZA_CERO': campo(L, 'casos', 'C|H4', 'FC', 'prueba', 'estado') == 'VARIANZA_CERO',
        'C|H4b FC SOSTENIDA': campo(L, 'casos', 'C|H4b', 'FC', 'estado') == 'SOSTENIDA',
        'B|H1 T2 PASA': campo(L, 'casos', 'B|H1', 'T2', 'estado') == 'PASA',
        'P_T2_B SOSTENIDA': campo(L, 'veredictos', 'P_T2_B', 'veredicto') == 'SOSTENIDA',
        'F_R01 SOSTENIDA': campo(L, 'veredictos', 'F_R01', 'firma') == 'SOSTENIDA',
    }
    prueba('S12_cada_rama_sembrada_aparece_en_el_agregado', all(ramas.values()),
           '%d/%d faltan=%s' % (sum(ramas.values()), len(ramas), [k for k, x in ramas.items() if not x]))
    ids = sorted(L['intervalos'])
    with open(os.path.join(trabajo, 'registro_ids.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(t + '\n' for t in ids))
    prueba('S13_registro_de_722_ids_igual_en_los_tres_escenarios',
           len(ids) == 722 and ids == sorted(Su['intervalos']) == sorted(Gl['intervalos']),
           'n=%d sha256=%s' % (len(ids), C.sha_archivo(os.path.join(trabajo, 'registro_ids.txt'))))
    n_ok = sum(1 for _, x in RES if x)
    print('PRUEBA_SOBRE_SINTETICO %d/%d %s (%.1f s)' % (n_ok, len(RES), 'PASS' if n_ok == len(RES) else 'FAIL',
                                                        time.time() - t0), flush=True)
    raise SystemExit(0 if n_ok == len(RES) else 1)


if __name__ == '__main__':
    main()
