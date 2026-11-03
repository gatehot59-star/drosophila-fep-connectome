#!/usr/bin/env python3
"""juntar_a1.py - BRAIN, 2026-11-03 (respuesta 2026-11-03-006).

Piezas de la corrida grande de 009-A1 que no leen ningun estimando:
  empaquetar    recibos JSON de un bloque a un JSONL ordenado por ensayo; cada linea es el archivo tal cual.
  testigos      compara las huellas de espigas de los 10 ensayos de humo rehechos en esta maquina con las del
                intento 1 (results/a1_2026-11-03/prueba_1/registros_humo). Solo imprime IGUAL o DISTINTO.
  validar-todo  junta los JSONL de todos los bloques y corre validar_a1.validar sobre el plan completo.
  prueba        ida y vuelta del JSONL y casos rojos sobre recibos de fixture.
Uso:
  python3 juntar_a1.py empaquetar --registros DIR --salida bloque_KK.jsonl
  python3 juntar_a1.py testigos --registros DIR --referencia DIR
  python3 juntar_a1.py validar-todo --manifiesto M --sha-manifiesto H --jsonl 'art/**/bloque_*.jsonl' --salida V.json
  python3 juntar_a1.py prueba --registros DIR --trabajo DIR --manifiesto-fixture M
Exit 0 si todo esta bien; 1 si no.
"""
import argparse
import glob
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun_a1 as C  # noqa: E402
import plan_a1 as P  # noqa: E402
import validar_a1 as V  # noqa: E402


def tid(r):
    return C.id_ensayo(r['subject_id'], r['regime'], r['condition'], r['seed'])


def empaquetar(dir_reg, salida):
    filas = []
    for n in sorted(os.listdir(dir_reg)):
        if not n.endswith('.json'):
            continue
        with open(os.path.join(dir_reg, n), encoding='utf-8') as f:
            txt = f.read().strip()
        if '\n' in txt:
            raise SystemExit('ABORTA: recibo con salto de linea: %s' % n)
        filas.append((tid(json.loads(txt)), txt))
    filas.sort()
    with open(salida, 'w', encoding='utf-8') as f:
        for _, txt in filas:
            f.write(txt + '\n')
    print('EMPAQUETADO %s recibos=%d sha256=%s' % (salida, len(filas), C.sha_archivo(salida)), flush=True)
    return len(filas)


def leer_jsonl(ruta):
    out = []
    with open(ruta, encoding='utf-8') as f:
        for k, linea in enumerate(f, 1):
            linea = linea.rstrip('\n')
            if not linea:
                continue
            etiqueta = '%s:%d' % (os.path.basename(ruta), k)
            try:
                out.append((etiqueta, json.loads(linea)))
            except ValueError:
                out.append((etiqueta, None))
    return out


def testigos(dir_nuevo, dir_ref, esperados=10):
    ref = {tid(r): r for _, r in V.leer_registros(dir_ref) if isinstance(r, dict)}
    nue = {tid(r): r for _, r in V.leer_registros(dir_nuevo) if isinstance(r, dict)}
    claves = sorted(set(ref) | set(nue))
    n_ok = 0
    for t in claves:
        a, b = ref.get(t), nue.get(t)
        igual = (a is not None and b is not None and b.get('estado') == 'OK'
                 and a.get('espigas_sha256') == b.get('espigas_sha256'))
        n_ok += int(igual)
        print('TESTIGO %s %s' % (t, 'IGUAL' if igual else 'DISTINTO'), flush=True)
    print('TESTIGOS %d/%d IGUAL' % (n_ok, len(claves)), flush=True)
    return n_ok == len(claves) == esperados


def validar_todo(ruta_man, sha_esp, patron, salida):
    sha = C.sha_archivo(ruta_man)
    if sha != sha_esp:
        print('ABORTA: el manifiesto tiene sha256 %s y se esperaba %s' % (sha, sha_esp), flush=True)
        return False
    with open(ruta_man, encoding='utf-8') as f:
        man = json.load(f)
    regs, archivos = [], []
    for a in sorted(glob.glob(patron, recursive=True)):
        filas = leer_jsonl(a)
        regs.extend(filas)
        archivos.append({'archivo': os.path.basename(a), 'lineas': len(filas), 'sha256': C.sha_archivo(a)})
        print('JSONL %s lineas=%d sha256=%s' % (os.path.basename(a), len(filas), archivos[-1]['sha256']), flush=True)
    v = V.validar(man, sha, regs, P.ids_plan(man))
    por_codigo = {}
    for x in v['fallos']:
        por_codigo[x['codigo']] = por_codigo.get(x['codigo'], 0) + 1
    v['por_codigo'] = por_codigo
    v['archivos'] = archivos
    with open(salida, 'w', encoding='utf-8') as f:
        json.dump(v, f, sort_keys=True, indent=1)
    for x in v['fallos'][:40]:
        print('FALLA %s %s' % (x['codigo'], x['detalle']), flush=True)
    print('VALIDACION_CORRIDA %s archivos=%d registros=%d esperados=%d fallos=%d por_codigo=%s' % (
        v['estado'], len(archivos), v['n_registros'], v['n_esperados'], v['n_fallos'],
        json.dumps(por_codigo, sort_keys=True)), flush=True)
    return v['estado'] == 'OK'


def prueba(dir_reg, trabajo, ruta_man_fx):
    os.makedirs(trabajo, exist_ok=True)
    j = os.path.join(trabajo, 'bloque_prueba.jsonl')
    n = empaquetar(dir_reg, j)
    por_dir = {tid(r): r for _, r in V.leer_registros(dir_reg)}
    por_j = {tid(r): r for _, r in leer_jsonl(j)}
    ida_vuelta = n == len(por_dir) > 0 and por_j == por_dir
    with open(j, encoding='utf-8') as f:
        lineas = f.read().split('\n')[:-1]
    originales = []
    for x in os.listdir(dir_reg):
        if x.endswith('.json'):
            with open(os.path.join(dir_reg, x), encoding='utf-8') as f:
                originales.append(f.read().strip())
    textual = sorted(lineas) == sorted(originales)
    copia = os.path.join(trabajo, 'copia')
    shutil.rmtree(copia, ignore_errors=True)
    shutil.copytree(dir_reg, copia)
    iguales = testigos(copia, dir_reg, esperados=n)
    x0 = sorted(x for x in os.listdir(copia) if x.endswith('.json'))[0]
    with open(os.path.join(copia, x0), encoding='utf-8') as f:
        r = json.load(f)
    r['espigas_sha256'] = '0' * 64
    with open(os.path.join(copia, x0), 'w', encoding='utf-8') as f:
        json.dump(r, f, sort_keys=True)
    adulterado = not testigos(copia, dir_reg, esperados=n)
    roto = os.path.join(trabajo, 'roto.jsonl')
    with open(roto, 'w', encoding='utf-8') as f:
        f.write(lineas[0] + '\n{roto\n')
    rr = leer_jsonl(roto)
    linea_rota = len(rr) == 2 and isinstance(rr[0][1], dict) and rr[1][1] is None
    incompleto = not validar_todo(ruta_man_fx, C.sha_archivo(ruta_man_fx), j, os.path.join(trabajo, 'v_fx.json'))
    casos = [('ida_y_vuelta', ida_vuelta), ('lineas_textuales', textual), ('testigos_iguales', iguales),
             ('testigo_adulterado_da_distinto', adulterado), ('linea_rota_queda_ilegible', linea_rota),
             ('plan_incompleto_no_valida', incompleto)]
    for nombre, ok in casos:
        print('PRUEBA_JUNTAR %s %s' % (nombre, 'PASS' if ok else 'FAIL'), flush=True)
    ok = all(x for _, x in casos)
    print('PRUEBA_JUNTAR %d/%d %s' % (sum(1 for _, x in casos if x), len(casos), 'PASS' if ok else 'FAIL'), flush=True)
    return ok


def main():
    ap = argparse.ArgumentParser(description='Juntar la corrida grande de 009-A1 sin leer estimandos')
    ap.add_argument('accion', choices=['empaquetar', 'testigos', 'validar-todo', 'prueba'])
    ap.add_argument('--registros', default='')
    ap.add_argument('--salida', default='')
    ap.add_argument('--referencia', default='')
    ap.add_argument('--manifiesto', default='')
    ap.add_argument('--sha-manifiesto', default='')
    ap.add_argument('--jsonl', default='')
    ap.add_argument('--trabajo', default='')
    ap.add_argument('--manifiesto-fixture', default='')
    a = ap.parse_args()
    if a.accion == 'empaquetar':
        ok = empaquetar(a.registros, a.salida) >= 0
    elif a.accion == 'testigos':
        ok = testigos(a.registros, a.referencia)
    elif a.accion == 'validar-todo':
        ok = validar_todo(a.manifiesto, a.sha_manifiesto, a.jsonl, a.salida)
    else:
        ok = prueba(a.registros, a.trabajo, a.manifiesto_fixture)
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
