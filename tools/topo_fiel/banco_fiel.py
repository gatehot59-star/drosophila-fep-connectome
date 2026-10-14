#!/usr/bin/env python3
"""Banco de H_TOPO_FIEL: el programa que usa solo flechas que la mosca tiene, contra el que resta (respuesta
2026-10-14-021, paso B del sello).

Orden del sello: A los programas (escape_fiel.topo y el control escape_cruzado.topo, commit 27fe098, chequeo Topo v0.1
CABLEADA=10) antes de cualquier banco; B este banco, la regla de decision y su prueba; despues el SELLO.

Pregunta: en la mosca, la resta contralateral en DNp06 (giro) no tiene sinapsis directas (2026-10-14-020). Si el
programa que no la hace rinde igual que el que la hace, el programa fiel alcanza y la resta sobra.

Tarea: la de la 012 (tarea_barra_dir.py, sellada d2515357: la 015 mas la barra de atras hacia adelante), 6 celdas
(A x ruido), 2400 de entrenamiento y 2000 de prueba por celda, con SEMILLAS NUEVAS (31 y 32 para los ensayos, 131 y
132 para el ruido) que no corrieron nunca: los numeros de la 014 con las semillas 1, 2, 101 y 102 ya se vieron.
Todos los programas leen la misma entrada (backend regla de Topo) en los mismos ensayos.

Hipotesis pre-registradas (margen 0,01, IC90 por bootstrap estratificado por celda, B = 20.000):
  H_TOPO_FIEL: d = acierto(escape_fiel) - acierto(escape.topo, el que resta) en los 12.000 ensayos de prueba.
    SOSTENIDA si el limite inferior es > -0,01 (el fiel no pierde mas de un punto); REFUTADA si el superior es
    < -0,01; si no, SIN_DECIDIR.
  CONTROL_ROJO: el mismo criterio con escape_cruzado.topo (giro hacia el estimulo) en lugar del fiel. Tiene que salir
    REFUTADA. Si no sale REFUTADA, el veredicto de H_TOPO_FIEL es INVALIDO.
Guardas (salida 3 si fallan): md5 de todo; la tarea pasa sus chequeos; el fiel baja el mismo motivo de 46 neuronas
(REPRODUCE_M46); CABLEADO_FIEL: Topo v0.1 da CABLEADA en las 10 flechas del fiel; CONTROL_GRAFO: el que resta da
SIN_VIA_DIRECTA=4 (lo de la 020).
Descriptivo, sin veredicto: fiel - aterrizaje_dir.topo (resta tambien LPLC1 en el aterrizaje); fiel - W (el cableado
real de la 015, sin entrenar las lineas); por celda; por subconjunto (giro en vuelo, looming frontal en vuelo, barras
AA y AD en vuelo, posada).
Salida: 0 completo; 2 insumos distintos del pin; 3 instrumento invalido. Con --humo: 600/400 y B = 2000; esos numeros
no valen.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
HERR = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(HERR, "escape_aterrizaje"))
sys.path.insert(0, os.path.join(HERR, "topo"))
sys.path.insert(0, os.path.join(HERR, "topo_barra"))
sys.path.insert(0, AQUI)
import escape_aterrizaje_dbc3 as base  # noqa: E402
import tarea_mosca as tm  # noqa: E402
import topo  # noqa: E402
import topo_grafo as tg  # noqa: E402
import tarea_barra_dir as tbd  # noqa: E402
import decidir_fiel as dfl  # noqa: E402

MD5 = {
    "escape_aterrizaje/tarea_mosca.py": "40d64e074d9163753439307c5be4ac5e",
    "escape_aterrizaje/escape_aterrizaje_dbc3.py": "4d40477d87406c31672acfb6e6e8f5a2",
    "escape_aterrizaje/entrada_por_tipos.py": "e060c4bffb685aa550dadc19eda3dd02",
    "topo/topo.py": "9abefe9d620e9f94f4a68ed75108d6be",
    "topo/topo_grafo.py": "0ea687824a45456e0a02b0b197f57a8a",
    "topo/escape.topo": "dae4967da0085f4bedcb4365f87127b0",
    "topo_barra/tarea_barra_dir.py": "d25153570edff8dfc249945c88cd7d4c",
    "topo_barra/aterrizaje_dir.topo": "0122a4ce64884010e8bb741bb57f2e29",
    "topo_fiel/escape_fiel.topo": "8e7f23be70392bde04643a2bf3c1fa65",
    "topo_fiel/escape_cruzado.topo": "9d0bb0f6f4cdc48f138b09f5b268429d",
    "topo_fiel/decidir_fiel.py": "840aeabf15446852cd0122a6fc4e5b7a",
}
CONN_MD5, ANNOT_MD5 = "3d802fd542b5d18570ba1ba0bb0abed9", "719904abad876c68ace1b5690c9b9b63"
N_TRAIN, N_TEST, B = 2400, 2000, 20000
SEM_TR, SEM_TE, SEM_ZTR, SEM_ZTE = 31, 32, 131, 132
SEM_BOOT = dict(fiel_vs_resta=2121, control=2122, fiel_vs_nueva=2123, fiel_vs_W=2124)
CELDAS = [(A, s) for A in tm.AMPLITUDES for s in tm.RUIDOS]


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def pr(s):
    print(s, flush=True)


def leer(ruta):
    return topo.parsear(open(ruta, encoding="utf-8").read())


def cuenta_veredictos(fl):
    c = {}
    for f in fl:
        c[f["veredicto"]] = c.get(f["veredicto"], 0) + 1
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--humo", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(), platform.python_version(),
                                                     np.__version__))
    pr("# md5 banco = " + md5(os.path.abspath(__file__)))
    pr("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    ok_md5 = True
    for f, m in MD5.items():
        got = md5(os.path.join(HERR, f))
        pr("# md5 %s = %s -> %s" % (f, got, got == m))
        ok_md5 = ok_md5 and got == m
    mc, ma = md5(a.conn), md5(a.annot)
    pr("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if not ok_md5 or mc != CONN_MD5 or ma != ANNOT_MD5:
        pr("ABORTA: insumos o modulos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_train, n_test = (600, 400) if humo else (N_TRAIN, N_TEST)
    b_boot = 2000 if humo else B

    if tbd.chequeos() != 0:
        pr("ABORTA: la tarea no pasa sus chequeos")
        pr("EXIT_RUN=3")
        return 3
    Pf = leer(os.path.join(AQUI, "escape_fiel.topo"))
    Px = leer(os.path.join(AQUI, "escape_cruzado.topo"))
    Pv = leer(os.path.join(HERR, "topo", "escape.topo"))
    Pn = leer(os.path.join(HERR, "topo_barra", "aterrizaje_dir.topo"))

    ga, gc = tg.cargar(a.conn, a.annot)
    fl_f = tg.chequear(Pf, ga, gc)[0]
    fl_v = tg.chequear(Pv, ga, gc)[0]
    cf, cv = cuenta_veredictos(fl_f), cuenta_veredictos(fl_v)
    cab_ok = bool(cf == {"CABLEADA": 10})
    ctl_ok = bool(cv.get("SIN_VIA_DIRECTA", 0) == 4)
    pr("CHEQUEO CABLEADO_FIEL %s -> %s" % (" ".join("%s=%d" % kv for kv in sorted(cf.items())), cab_ok))
    pr("CHEQUEO CONTROL_GRAFO escape.topo %s -> %s" % (" ".join("%s=%d" % kv for kv in sorted(cv.items())), ctl_ok))
    del ga, gc
    if not (cab_ok and ctl_ok):
        pr("EXIT_RUN=3")
        return 3

    sel, aristas = topo.bajar_cableado(Pf, a.conn, a.annot)
    sel15, ar15 = tm.construir(a.conn, a.annot)
    rep = bool(sel == sel15 and aristas == ar15)
    pr("CHEQUEO REPRODUCE_M46 neuronas=%d aristas=%d -> %s" % (len(sel), len(aristas), rep))
    if not rep:
        pr("EXIT_RUN=3")
        return 3
    n = len(sel)
    nv = n - 6
    lados = ["L" if s[2] == "left" else "R" for s in sel]
    tipos = [s[1] for s in sel]
    W, rho0 = base.matriz(n, aristas)
    idx_W = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(nv)])

    etr, ete = tbd.generar(n_train, SEM_TR), tbd.generar(n_test, SEM_TE)
    ytr, yte, vtr, vte = etr["y"], ete["y"], etr["vuelo"], ete["vuelo"]
    Ztr = np.random.default_rng(SEM_ZTR).standard_normal((n_train, tm.T, nv))
    Zte = np.random.default_rng(SEM_ZTE).standard_normal((n_test, tm.T, nv))
    tau0 = 0.06 + 0.12 * np.random.default_rng(0).random(n)
    sub = dict(giro_vuelo=vte & ((yte == 3) | (yte == 4)), loom_frontal_vuelo=vte & (ete["est"] == 1),
               barra_AA_vuelo=vte & (ete["est"] == 3), barra_AD_vuelo=vte & (ete["est"] == 5), posada=~vte)
    pr("DATOS entrenamiento=%d prueba=%d clases_prueba=%s %s" % (
        n_train, n_test, ",".join(str(int((yte == k).sum())) for k in range(5)),
        " ".join("%s=%d" % (k, int(v.sum())) for k, v in sub.items())))

    def pred_w(dtr, dte):
        th = tm.umbrales(tm.lineas(tm.simular(W, tau0, idx_W, dtr, nv)), ytr, vtr)
        return tm.carrera(tm.lineas(tm.simular(W, tau0, idx_W, dte, nv)), th, vte)

    def regla(P, dtr, dte):
        Xtr = dtr["drive"][:, :, idx_W] + dtr["ruido"]
        Xte = dte["drive"][:, :, idx_W] + dte["ruido"]
        return topo.ejecutar_regla(P, Xtr, ytr, vtr.astype(int), Xte, vte.astype(int), tipos[:nv], lados[:nv])[0]

    nombres = ("fiel", "resta", "cruzado", "nueva", "W")
    cont = {k: [] for k in SEM_BOOT}
    celdas = []
    for A, s in CELDAS:
        dtr = dict(y=ytr, drive=tbd.sintonias(etr, A), ruido=s * Ztr)
        dte = dict(y=yte, drive=tbd.sintonias(ete, A), ruido=s * Zte)
        pred = dict(fiel=regla(Pf, dtr, dte), resta=regla(Pv, dtr, dte), cruzado=regla(Px, dtr, dte),
                    nueva=regla(Pn, dtr, dte), W=pred_w(dtr, dte))
        ok = {k: (pred[k] == yte) for k in nombres}
        cont["fiel_vs_resta"].append(dfl.contar(ok["fiel"], ok["resta"]))
        cont["control"].append(dfl.contar(ok["cruzado"], ok["resta"]))
        cont["fiel_vs_nueva"].append(dfl.contar(ok["fiel"], ok["nueva"]))
        cont["fiel_vs_W"].append(dfl.contar(ok["fiel"], ok["W"]))
        c = dict(A=A, ruido=s, acierto={k: float(ok[k].mean()) for k in nombres},
                 subconjuntos={sk: {k: float(ok[k][sm].mean()) for k in nombres} for sk, sm in sub.items()})
        celdas.append(c)
        pr("CELDA A=%.1f ruido=%.2f %s | giro_vuelo fiel=%.3f resta=%.3f | loom_frontal_vuelo fiel=%.3f resta=%.3f | "
           "%.1f s" % (A, s, " ".join("%s=%.4f" % (k, c["acierto"][k]) for k in nombres),
                      c["subconjuntos"]["giro_vuelo"]["fiel"], c["subconjuntos"]["giro_vuelo"]["resta"],
                      c["subconjuntos"]["loom_frontal_vuelo"]["fiel"], c["subconjuntos"]["loom_frontal_vuelo"]["resta"],
                      time.time() - t0))

    res_d = {k: dfl.decidir(cont[k], b_boot, SEM_BOOT[k]) for k in SEM_BOOT}
    for k in ("fiel_vs_nueva", "fiel_vs_W"):
        r = res_d[k]
        pr("DESCRIPTIVO %s d=%+.4f IC90=[%+.4f; %+.4f] (sin veredicto)" % (k, r["d"], r["ic90"][0], r["ic90"][1]))
    r = res_d["control"]
    pr("CONTROL_ROJO d(cruzado - resta)=%+.4f IC90=[%+.4f; %+.4f] -> %s (tiene que ser REFUTADA)" % (
        r["d"], r["ic90"][0], r["ic90"][1], r["veredicto"]))
    r = res_d["fiel_vs_resta"]
    h = dfl.final(r["veredicto"], res_d["control"]["veredicto"])
    pr("H_TOPO_FIEL d(fiel - resta)=%+.4f IC90=[%+.4f; %+.4f] margen=-%.2f -> %s%s" % (
        r["d"], r["ic90"][0], r["ic90"][1], dfl.MARGEN, h, " (HUMO, sin valor)" if humo else ""))
    res = dict(humo=humo, n_train=n_train, n_test=n_test, B=b_boot, semillas=[SEM_TR, SEM_TE, SEM_ZTR, SEM_ZTE],
               chequeos=dict(CABLEADO_FIEL=cf, CONTROL_GRAFO=cv, REPRODUCE_M46=rep), celdas=celdas, conteos=cont,
               comparaciones=res_d, H_TOPO_FIEL=h, segundos=time.time() - t0)
    json.dump(res, open(os.path.join(a.out, "topo_fiel.json"), "w"), indent=1)
    pr("EXIT_RUN=0 | %.1f s" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
