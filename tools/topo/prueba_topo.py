#!/usr/bin/env python3
"""Prueba de Topo v0 contra el instrumento sellado (respuesta 2026-10-14-011).

PRUEBA 1 EQUIV_REGLA: escape.topo, ejecutado por el backend regla, da exactamente las mismas senales, umbrales y
  decisiones que la regla sellada de los factoriales: las funciones media y lc de factorial2_mosca.py (md5 798a824c,
  extraidas del archivo sin copiarlas a mano) mas lineas, umbrales y carrera de tarea_mosca.py (md5 40d64e07).
  Seis celdas (A x ruido), dos tamanos de entrada (40 y 564), ensayos generados por la tarea sellada.
PRUEBA 2 CONTROL_NEGATIVO: el mismo programa con el aterrizaje leyendo LPLC1 en lugar de LPLC4 tiene que dar
  decisiones distintas; y tres programas mal escritos tienen que ser rechazados.
PRUEBA 3 REPRODUCE_M46: el backend cableado baja las vias a exactamente las mismas neuronas y aristas que
  tarea_mosca.construir (el motivo de 46 neuronas de la 015), con los insumos fijados por md5.
Sale 0 si las tres dan PASA y 1 si alguna falla.
"""
import ast
import hashlib
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.dirname(AQUI)
EA = os.path.join(HERR, "escape_aterrizaje")
F2 = os.path.join(HERR, "factorial2")
sys.path.insert(0, AQUI)
sys.path.insert(0, EA)
import topo  # noqa: E402
import tarea_mosca as tm  # noqa: E402

MD5 = {"escape_aterrizaje/tarea_mosca.py": "40d64e074d9163753439307c5be4ac5e", "factorial2/factorial2_mosca.py": "798a824cd47808155fa12adb9e652dac",
       "escape_aterrizaje/escape_aterrizaje_dbc3.py": "4d40477d87406c31672acfb6e6e8f5a2", "escape_aterrizaje/entrada_por_tipos.py": "e060c4bffb685aa550dadc19eda3dd02"}
CONN_MD5, ANNOT_MD5 = "3d802fd542b5d18570ba1ba0bb0abed9", "719904abad876c68ace1b5690c9b9b63"


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def regla_sellada(lados, tipos, chan):
    """Compila media y lc tal como estan dentro de main() en factorial2_mosca.py."""
    arbol = ast.parse(open(os.path.join(F2, "factorial2_mosca.py"), encoding="utf-8").read())
    main = [f for f in arbol.body if isinstance(f, ast.FunctionDef) and f.name == "main"][0]
    funcs = [f for f in main.body if isinstance(f, ast.FunctionDef) and f.name in ("media", "lc")]
    assert [f.name for f in funcs] == ["media", "lc"], [f.name for f in funcs]
    ns = dict(np=np, lados=lados, tipos=tipos, chan=chan)
    exec(compile(ast.Module(body=funcs, type_ignores=[]), "factorial2_mosca.py", "exec"), ns)
    return ns["lc"]


def entradas(k, rng):
    tipos = [tm.TIPOS[i % tm.NT] for i in range(k)]
    lados = ["L" if (i // tm.NT) % 2 == 0 else "R" for i in range(k)]
    orden = rng.permutation(k)
    return [tipos[i] for i in orden], [lados[i] for i in orden]


def prueba_equivalencia(p):
    ok_total, n_casos = True, 0
    for k in (40, 564):
        rng = np.random.default_rng(k)
        tipos, lados = entradas(k, rng)
        chan = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(k)])
        lc = regla_sellada(lados, tipos, chan)
        etr, ete = tm.generar(600, 11), tm.generar(400, 12)
        Ztr = rng.standard_normal((600, tm.T, k))
        Zte = rng.standard_normal((400, tm.T, k))
        for A in tm.AMPLITUDES:
            for s in tm.RUIDOS:
                dtr = dict(drive=tm.sintonias(etr, A), ruido=s * Ztr)
                dte = dict(drive=tm.sintonias(ete, A), ruido=s * Zte)
                Ltr, Lte = tm.lineas(lc(dtr, k)), tm.lineas(lc(dte, k))
                th_s = tm.umbrales(Ltr, etr["y"], etr["vuelo"])
                pred_s = tm.carrera(Lte, th_s, ete["vuelo"])
                Xtr = dtr["drive"][:, :, chan] + dtr["ruido"]
                Xte = dte["drive"][:, :, chan] + dte["ruido"]
                pred_t, th_t, Ste = topo.ejecutar_regla(p, Xtr, etr["y"], etr["vuelo"].astype(int), Xte,
                                                        ete["vuelo"].astype(int), tipos, lados)
                d_s = float(np.abs(Ste - Lte).max())
                d_th = float(np.abs(th_t - th_s).max())
                igual = int((pred_t == pred_s).sum())
                acierto = float((pred_s == ete["y"]).mean())
                ok = d_s == 0.0 and d_th == 0.0 and igual == len(pred_s)
                ok_total = ok_total and ok
                n_casos += 1
                print("EQUIV entradas=%d A=%.1f ruido=%.2f max_dif_senal=%.3g max_dif_umbral=%.3g decisiones_iguales=%d/%d "
                      "acierto_regla=%.4f -> %s" % (k, A, s, d_s, d_th, igual, len(pred_s), acierto, ok))
    print("PRUEBA EQUIV_REGLA casos=%d -> %s" % (n_casos, "PASA" if ok_total else "FALLA"))
    return ok_total


def prueba_negativa(texto):
    malo = texto.replace("media(LPLC4@L) en vuelo", "media(LPLC1@L) en vuelo").replace(
        "media(LPLC4@R) en vuelo", "media(LPLC1@R) en vuelo")
    assert malo != texto
    pm, p = topo.parsear(malo), topo.parsear(texto)
    rng = np.random.default_rng(564)
    tipos, lados = entradas(564, rng)
    chan = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(564)])
    etr, ete = tm.generar(600, 11), tm.generar(400, 12)
    Xtr = tm.sintonias(etr, 0.3)[:, :, chan] + 0.15 * rng.standard_normal((600, tm.T, 564))
    Xte = tm.sintonias(ete, 0.3)[:, :, chan] + 0.15 * rng.standard_normal((400, tm.T, 564))
    a = topo.ejecutar_regla(p, Xtr, etr["y"], etr["vuelo"].astype(int), Xte, ete["vuelo"].astype(int), tipos, lados)[0]
    b = topo.ejecutar_regla(pm, Xtr, etr["y"], etr["vuelo"].astype(int), Xte, ete["vuelo"].astype(int), tipos, lados)[0]
    distintas = int((a != b).sum())
    acc_a, acc_b = float((a == ete["y"]).mean()), float((b == ete["y"]).mean())
    print("NEGATIVO aterrizaje con LPLC1: decisiones_distintas=%d/%d acierto %.4f -> %.4f" % (
        distintas, len(a), acc_a, acc_b))
    rechazos = 0
    errores = [texto.replace("media(LC4@L, LPLC2@L)", "media(LC6@L, LPLC2@L)"),
               texto.replace("media(LPLC4@R)", "media(LPLC4)"),
               texto.replace("-> girar_izq", "-> volar_hacia_atras")]
    for e in errores:
        try:
            topo.parsear(e)
            print("NEGATIVO programa mal escrito ACEPTADO")
        except topo.ErrorTopo as x:
            rechazos += 1
            print("NEGATIVO programa mal escrito rechazado: %s" % x)
    ok = distintas > 0 and rechazos == len(errores)
    print("PRUEBA CONTROL_NEGATIVO -> %s" % ("PASA" if ok else "FALLA"))
    return ok


def prueba_cableado(p, conn, annot):
    if md5(conn) != CONN_MD5 or md5(annot) != ANNOT_MD5:
        print("PRUEBA REPRODUCE_M46 -> FALLA (insumos distintos del pin)")
        return False
    sel_t, ar_t = topo.bajar_cableado(p, conn, annot)
    sel_s, ar_s = tm.construir(conn, annot)
    ok = sel_t == sel_s and ar_t == ar_s
    print("CABLEADO topo: neuronas=%d aristas=%d inhibitorias=%d sinapsis=%d | sellado: neuronas=%d aristas=%d" % (
        len(sel_t), len(ar_t), sum(1 for x in ar_t if x[2] < 0), int(sum(abs(x[2]) for x in ar_t)), len(sel_s),
        len(ar_s)))
    print("PRUEBA REPRODUCE_M46 -> %s" % ("PASA" if ok else "FALLA"))
    return ok


def main():
    for f, m in MD5.items():
        got = md5(os.path.join(HERR, f))
        print("SELLADO %s %s -> %s" % (f, got, got == m))
        if got != m:
            return 1
    print("TOPO topo.py %s escape.topo %s" % (md5(os.path.join(AQUI, "topo.py")), md5(os.path.join(AQUI, "escape.topo"))))
    texto = open(os.path.join(AQUI, "escape.topo"), encoding="utf-8").read()
    p = topo.parsear(texto)
    print("PROGRAMA %s renglones_utiles=%d lineas=%d vias=%d" % (
        p["reflejo"], sum(1 for r in texto.split(topo.NL) if r.split("#", 1)[0].strip()), len(p["lineas"]),
        len(p["vias"])))
    r1 = prueba_equivalencia(p)
    r2 = prueba_negativa(texto)
    r3 = prueba_cableado(p, sys.argv[1], sys.argv[2]) if len(sys.argv) == 3 else None
    if r3 is None:
        print("PRUEBA REPRODUCE_M46 -> NO MEDIDO (faltan CONN y ANNOT)")
    ok = r1 and r2 and r3 is not False
    print("VEREDICTO_TOPO -> %s" % ("PASA" if ok else "FALLA"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
