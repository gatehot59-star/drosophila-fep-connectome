#!/usr/bin/env python3
"""Pruebas de H_MECANISMO_DNp04 (respuesta 2026-11-02-006; sello tools/mecanismo/dnp04/SELLO-DNP04-2026-11-02.md).

1. Mascaras de Q1 a Q6 sobre un grafo sintetico completo, y C0 y C1 identicos a los de intervenir.py.
2. Estadistica: permutacion exacta y Holm contra valores calculados a mano.
3. El agregador con celdas sinteticas que plantan cada veredicto (SOSTENIDA, PARCIAL, REFUTADA), las tres salidas del
   proxy, y cada guarda rota por separado: el caso tiene que dar INVALIDA con esa guarda en falso y las demas en verdadero.
4. Datos reales, si se pasan: los cuatro root_id del sello, sus indices y pertenencias, y las filas que toca cada
   condicion en el parquet de Shiu.
5. Humo, si se pasa --shiu: corre el instrumento sin mirar ninguna condicion de la hipotesis. C0 y C1 de LC4 contra
   la corrida 2, y C0 contra Q2 con LPLC4, donde PVLP010 no dispara.
Uso: python3 prueba_dnp04.py [--conn C --comp K --conjuntos J] [--previa CORRIDA2 --shiu DIR --humo SALIDA]
"""
import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
MECANISMO = os.path.dirname(AQUI)
for _p in (AQUI, MECANISMO):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import intervenir as base  # noqa: E402
import intervenir_dnp04 as inst  # noqa: E402
import agregar_dnp04 as agr  # noqa: E402

RES = []
N_SINT = {"DNp04": 23, "PVLP010": 10, "LHAD1g1": 11, "AVLP080": 12}


def chequeo(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print("%s %s %s" % ("PASS" if ok else "FAIL", nombre, detalle), flush=True)


def prueba_mascaras():
    n = 8
    pares = [(p, q) for p in range(n) for q in range(n) if p != q]
    i = np.array([p for p, _ in pares], dtype=np.int64)
    j = np.array([q for _, q in pares], dtype=np.int64)
    w = np.array([-1.0 if p in (2, 3, 6) else 1.0 for p, _ in pares])
    S, X, D = [0, 1], [2, 3], [4, 5]
    N = {"DNp04": 4, "PVLP010": 2, "LHAD1g1": 3, "AVLP080": 6}
    esperado = {
        "C0": set(),
        "C1": {(p, q) for p, q in pares if p in (2, 3)},
        "Q1": {(4, 2)},
        "Q2": {(p, q) for p, q in pares if p == 2},
        "Q3": {(p, q) for p, q in pares if p == 4},
        "Q4": {(p, q) for p, q in pares if q == 2 and p != 4},
        "Q5": {(p, q) for p, q in pares if p == 3},
        "Q6": {(p, q) for p, q in pares if p == 6},
    }
    for cond, esp in esperado.items():
        ops = inst.operaciones(cond, S, X, D, N)
        w2 = base.editar_pesos(w, i, j, n, ops)
        got = {pares[k] for k in np.flatnonzero(w2 != w)}
        toc = base.tocadas(i, j, w, n, ops)
        chequeo("mascara_%s" % cond, got == esp and toc["filas"] == len(esp),
                "filas=%d esperadas=%d" % (toc["filas"], len(esp)))
    for cond in ("C0", "C1"):
        chequeo("identica_a_intervenir_%s" % cond,
                inst.operaciones(cond, S, X, D, N) == base.operaciones(cond, S, X, D, [], []))


def prueba_estadistica():
    chequeo("exacto_todos_positivos", abs(agr.exacto(np.ones(20)) - 2.0 / 2 ** 20) < 1e-15)
    chequeo("exacto_cero", agr.exacto(np.zeros(20)) == 1.0)
    chequeo("exacto_a_mano", abs(agr.exacto(np.array([1.0, 2.0, 3.0])) - 0.25) < 1e-15)
    h = agr.holm([0.01, 0.04, 0.03, 0.2])
    chequeo("holm_a_mano", bool(np.allclose(h, [0.04, 0.09, 0.09, 0.2])), str(np.round(h, 4).tolist()))


def efectos(e, caso):
    ef = {"C0": {}, "C1": {20: 10, 21: 10, 22: 10}}
    if e == "LC4":
        ef.update({"Q1": {20: 12}, "Q2": {20: 21}, "Q3": {20: 9}, "Q4": {}, "Q5": {21: 1}, "Q6": {}})
        if caso == "refutada":
            ef["Q1"] = {}
        if caso == "parcial":
            ef["Q1"] = {20: 6}
    elif e == "LPLC2":
        ef.update({"Q1": {20: 3}, "Q2": {20: 6}, "Q3": {20: 2}, "Q4": {20: 6}, "Q5": {20: 9}, "Q6": {21: 6}})
        if caso == "proxy_parcial":
            ef["Q5"], ef["Q6"] = {}, {}
    elif e == "LPLC1":
        ef.update({"Q1": {}, "Q2": {20: 6}, "Q3": {}, "Q4": {20: 6}, "Q5": {}, "Q6": {21: 18}})
        if caso == "proxy_parcial":
            ef["Q6"] = {}
    else:
        ef.update({"Q1": {}, "Q2": {}, "Q3": {}, "Q4": {}, "Q5": {21: 1}, "Q6": {22: 1}})
    if caso == "proxy_falla":
        ef["Q2"], ef["Q5"], ef["Q6"] = {}, {}, {}
    return ef


def sinteticas(tmp, caso):
    """Celdas q_* nuevas y p_* de una corrida 2 falsa, con efectos plantados sobre D'."""
    nueva, previa = os.path.join(tmp, "nueva"), os.path.join(tmp, "previa")
    os.makedirs(nueva)
    os.makedirs(previa)
    S, X, Dp = [0, 1, 2, 3], [10, 11, 12, 13], [20, 21, 22]
    for e in agr.ESTIM:
        D = Dp + [23] if e in ("LC4", "LPLC2") else list(Dp)
        mirar = list(dict.fromkeys(S + X + D + [23, 10, 11, 12] + [30, 31]))
        mirar_p = list(dict.fromkeys(S + X + D + [30, 31, 32]))
        ef = efectos(e, caso)

        def condicion(nombre, mir):
            extra = ef[nombre]
            pos = {m: k for k, m in enumerate(mir)}
            ens = []
            for t in range(20):
                c = [0] * len(mir)
                for s in S:
                    c[pos[s]] = 50
                for x in X:
                    c[pos[x]] = 20 + t % 4
                for k, d in enumerate(Dp):
                    c[pos[d]] = 10 + 5 * k + t % 3
                if 23 in pos:
                    c[pos[23]] = 40 if e in ("LC4", "LPLC2") else 0
                if 10 in pos:
                    c[pos[10]] = 0 if e == "LPLC4" else 50
                for m, v in extra.items():
                    if m in pos:
                        c[pos[m]] += v
                if e == "LPLC1" and caso == "invalida_techo":
                    c[pos[20]] += 1500
                if e == "LPLC1" and caso == "invalida_piso":
                    for d in D:
                        c[pos[d]] = 0
                ens.append({"seed": 20261102 + t, "cuentas": c, "D_primera_ms": 5.0, "D_temprano": 3,
                            "espigas": 1000 + 2 * t + (7 if extra else 0), "activas": 300 + t + (1 if extra else 0),
                            "seg_run": 1.0})
            filas = agr.FILAS.get(nombre, 31422 if nombre == "C1" else 0)
            peso = agr.PESO_Q1 if nombre == "Q1" else float(filas)
            return {"tocadas": {"filas": filas, "peso_abs": peso}, "ensayos": ens,
                    "D": [sum(r["cuentas"][pos[d]] for d in D) for r in ens],
                    "X": [sum(r["cuentas"][pos[x]] for x in X) for r in ens],
                    "nombres": {k: [r["cuentas"][pos[v]] for r in ens] for k, v in N_SINT.items() if v in pos},
                    "seg": 1.0}

        nombres = {k: {"root": 0, "indice": v, "en_S": False, "en_X": v in X, "en_D": v in D}
                   for k, v in N_SINT.items()}
        for h, conds in (("a", inst.PARTE_A), ("b", inst.PARTE_B)):
            c = {"t_run_ms": 1000.0, "D_tipo": ["T%d" % k for k in range(len(D))], "nombres": nombres,
                 "indices": {"S": S, "X": X, "D": D, "desc": [30, 31], "mirar": mirar},
                 "conds": {q: condicion(q, mirar) for q in conds}}
            with open(os.path.join(nueva, "celda_q_%s_right_%s.json" % (e, h)), "w") as f:
                json.dump(c, f)
        p = {"t_run_ms": 1000.0, "D_tipo": ["T%d" % k for k in range(len(D))],
             "indices": {"S": S, "X": X, "D": D, "mirar": mirar_p},
             "conds": {q: condicion(q, mirar_p) for q in ("C0", "C1")}}
        with open(os.path.join(previa, "celda_p_%s_right_a.json" % e), "w") as f:
            json.dump(p, f)

    def editar(ruta, fn):
        with open(ruta) as f:
            c = json.load(f)
        fn(c)
        with open(ruta, "w") as f:
            json.dump(c, f)

    def posicion(c, m):
        return c["indices"]["mirar"].index(m)

    if caso == "invalida_replica":
        def fn(c):
            c["conds"]["C0"]["ensayos"][5]["cuentas"][posicion(c, 20)] += 1
        editar(os.path.join(previa, "celda_p_LPLC2_right_a.json"), fn)
    elif caso == "invalida_tecnico":
        def fn(c):
            c["conds"]["Q2"]["ensayos"][0]["cuentas"][posicion(c, 30)] += 1
        editar(os.path.join(nueva, "celda_q_LPLC4_right_a.json"), fn)
    elif caso == "invalida_filas":
        def fn(c):
            c["conds"]["Q1"]["tocadas"]["filas"] = 2
        editar(os.path.join(nueva, "celda_q_LC4_right_a.json"), fn)
    elif caso == "invalida_mitades":
        def fn(c):
            c["conds"]["C0"]["ensayos"][3]["espigas"] += 1
        editar(os.path.join(nueva, "celda_q_LPLC2_right_b.json"), fn)
    elif caso == "invalida_falta":
        os.remove(os.path.join(nueva, "celda_q_LPLC4_right_b.json"))


def prueba_agregador():
    todas = ("G1", "G2", "G3", "G4", "G5")
    casos = (("sostenida", "SOSTENIDA_EN_MODELO", None), ("parcial", "PARCIAL", None), ("refutada", "REFUTADA", None),
             ("proxy_falla", "PARCIAL", None), ("proxy_parcial", "SOSTENIDA_EN_MODELO", None),
             ("invalida_replica", "INVALIDA", "G1"), ("invalida_mitades", "INVALIDA", "G2"),
             ("invalida_filas", "INVALIDA", "G3"), ("invalida_tecnico", "INVALIDA", "G4"),
             ("invalida_techo", "INVALIDA", "G5"), ("invalida_piso", "INVALIDA", "G5"),
             ("invalida_falta", "INVALIDA", "faltan"))
    valores = {"sostenida": ("r_Q1=0.4000 r_Q2=0.7000 s4=1.0000", "PROXY_VEREDICTO PROXY_UTIL 7/7"),
               "parcial": ("r_Q1=0.2000 r_Q2=0.7000 s4=1.0000", "PROXY_VEREDICTO PROXY_UTIL 7/7"),
               "refutada": ("r_Q1=0.0000 r_Q2=0.7000 s4=1.0000",),
               "proxy_falla": ("r_Q1=0.4000 r_Q2=0.0000 s4=1.0000", "PROXY_VEREDICTO PROXY_FALLA 1/7"),
               "proxy_parcial": ("r_Q1=0.4000 r_Q2=0.7000 s4=1.0000", "PROXY_VEREDICTO PROXY_PARCIAL 4/7")}
    for caso, esp, rota in casos:
        with tempfile.TemporaryDirectory() as tmp:
            sinteticas(tmp, caso)
            r = subprocess.run([sys.executable, os.path.join(AQUI, "agregar_dnp04.py"), "--dir",
                                os.path.join(tmp, "nueva"), "--previa", os.path.join(tmp, "previa")],
                               capture_output=True, text=True)
            lineas = r.stdout.splitlines()
            lin = [x for x in lineas if x.startswith("H_MECANISMO_DNp04 ")]
            got = lin[-1].split()[1] if lin else "SIN_LINEA"
            gl = [x for x in lineas if x.startswith("GUARDAS_GLOBALES ")]
            if rota == "faltan":
                gok = not gl and any(x.startswith("FALTAN ") and "celda_q_LPLC4_right_b.json" in x for x in lineas)
                gdet = "faltan"
            else:
                g = json.loads(gl[-1].split(" ", 1)[1]) if gl else {}
                gok = bool(g) and all(g.get(k) is (k != rota) for k in todas)
                gdet = json.dumps(g, sort_keys=True)
            vok = all(v in r.stdout for v in valores.get(caso, ()))
            ok = r.returncode == 0 and got == esp and gok and vok
            chequeo("agregador_%s" % caso, ok, "dio=%s esperado=%s guardas=%s valores=%s exit=%d" % (
                got, esp, gdet, vok, r.returncode))
            if not ok:
                print(r.stdout[-2500:], r.stderr[-2500:], flush=True)


def prueba_reales(conn, comp, conjuntos):
    ids = pd.read_csv(comp, index_col=0).index.to_numpy(dtype=np.int64)
    f2i = {int(f): k for k, f in enumerate(ids)}
    n = len(ids)
    esperado = {"DNp04": 95123, "PVLP010": 37128, "LHAD1g1": 105779, "AVLP080": 6128}
    N = {k: f2i.get(v) for k, v in inst.NOMBRES.items()}
    chequeo("indices_del_sello", N == esperado, json.dumps(N, sort_keys=True))
    with open(conjuntos) as f:
        conj = json.load(f)
    pert = {"DNp04": ("D", ("LC4", "LPLC2")), "PVLP010": ("X", ("LC4", "LPLC2", "LPLC1")),
            "LHAD1g1": ("X", ("LC4", "LPLC2")), "AVLP080": ("X", ("LPLC2", "LPLC1"))}
    for k, (grupo, dentro) in pert.items():
        got = tuple(e for e in agr.ESTIM if inst.NOMBRES[k] in conj["estimulos"][e + "_right"][grupo])
        chequeo("pertenencia_%s" % k, got == dentro, "%s en %s" % (grupo, ",".join(got)))
    df = pd.read_parquet(conn, columns=["Presynaptic_Index", "Postsynaptic_Index", "Excitatory x Connectivity"])
    i = df["Presynaptic_Index"].to_numpy(dtype=np.int64)
    j = df["Postsynaptic_Index"].to_numpy(dtype=np.int64)
    w = df["Excitatory x Connectivity"].to_numpy(dtype=np.float64)
    del df
    e = conj["estimulos"]["LC4_right"]
    S = [f2i[f] for f in e["S"]]
    X = [f2i[f] for f in e["X"]]
    D = [f2i[f] for f in e["D"]]
    for q, filas in agr.FILAS.items():
        toc = base.tocadas(i, j, w, n, inst.operaciones(q, S, X, D, N))
        ok = toc["filas"] == filas and (q != "Q1" or abs(toc["peso_abs"] - agr.PESO_Q1) < 1e-9)
        chequeo("filas_reales_%s" % q, ok, "filas=%d peso_abs=%.1f" % (toc["filas"], toc["peso_abs"]))
    toc = base.tocadas(i, j, w, n, inst.operaciones("C1", S, X, D, N))
    chequeo("filas_reales_C1_LC4_igual_corrida2", toc["filas"] == 31422, "filas=%d" % toc["filas"])


def prueba_humo(shiu, conn, comp, conjuntos, previa, salida):
    os.makedirs(salida, exist_ok=True)
    for nombre, defi in (("humo_LC4", {"estimulo": "LC4_right", "hz": 50.0, "conds": ["C0", "C1"], "n_run": 1}),
                         ("humo_LPLC4", {"estimulo": "LPLC4_right", "hz": 50.0, "conds": ["C0", "Q2"], "n_run": 1})):
        cmd = [sys.executable, os.path.join(AQUI, "intervenir_dnp04.py"), "--shiu", shiu, "--conn", conn, "--comp",
               comp, "--conjuntos", conjuntos, "--celda", nombre, "--celda-json", json.dumps(defi), "--out", salida,
               "--n-proc", "1"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        with open(os.path.join(salida, nombre + ".log"), "w") as f:
            f.write(r.stdout + r.stderr)
        chequeo("humo_corre_%s" % nombre, r.returncode == 0, "exit=%d" % r.returncode)
        if r.returncode != 0:
            print(r.stdout[-3000:], r.stderr[-3000:], flush=True)
            continue
        with open(os.path.join(salida, "celda_%s.json" % nombre)) as f:
            c = json.load(f)
        e = defi["estimulo"].split("_")[0]
        with open(os.path.join(previa, "celda_p_%s_right_a.json" % e)) as f:
            p = json.load(f)
        p1 = copy.deepcopy(p)
        for k in ("C0", "C1"):
            p1["conds"][k]["ensayos"] = p1["conds"][k]["ensayos"][:1]
        nucleo = c["indices"]["S"] + c["indices"]["X"] + c["indices"]["D"]
        chequeo("humo_C0_igual_corrida2_%s" % e, agr.iguales(c, "C0", p1, "C0", nucleo))
        if "C1" in c["conds"]:
            chequeo("humo_C1_igual_corrida2_%s" % e, agr.iguales(c, "C1", p1, "C1", nucleo))
        if "Q2" in c["conds"]:
            chequeo("humo_Q2_igual_C0_%s" % e, agr.iguales(c, "Q2", c, "C0", c["indices"]["mirar"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", default="")
    ap.add_argument("--comp", default="")
    ap.add_argument("--conjuntos", default="")
    ap.add_argument("--previa", default="")
    ap.add_argument("--shiu", default="")
    ap.add_argument("--humo", default="")
    a = ap.parse_args()
    print("== prueba_dnp04.py :: H_MECANISMO_DNp04 ==", flush=True)
    prueba_mascaras()
    prueba_estadistica()
    prueba_agregador()
    if a.conn and a.comp and a.conjuntos:
        prueba_reales(a.conn, a.comp, a.conjuntos)
    else:
        print("NO_MEDIDO datos reales: faltan --conn, --comp o --conjuntos", flush=True)
    if a.shiu and a.previa and a.humo and a.conn and a.comp and a.conjuntos:
        prueba_humo(a.shiu, a.conn, a.comp, a.conjuntos, a.previa, a.humo)
    else:
        print("NO_MEDIDO humo: faltan --shiu, --previa o --humo", flush=True)
    n_ok = sum(1 for _, ok in RES if ok)
    print("PRUEBA %d/%d %s" % (n_ok, len(RES), "PASS" if n_ok == len(RES) else "FAIL"), flush=True)
    raise SystemExit(0 if n_ok == len(RES) else 3)


if __name__ == "__main__":
    main()
