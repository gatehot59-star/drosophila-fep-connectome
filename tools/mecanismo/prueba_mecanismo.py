#!/usr/bin/env python3
"""Prueba de H_MECANISMO (respuesta 2026-11-02-002): red sintetica con el model.py de Shiu sin cambios, antes de
sellar. Sale con 0 solo si pasan todas las pruebas; si falla una, sale con 3.
Uso: python3 prueba_mecanismo.py --shiu DIR --tmp T [--target numpy] [--n-proc 2]
"""
import argparse
import copy
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import agregar_mecanismo as ag  # noqa: E402
import intervenir as iv  # noqa: E402

RES = []


def chk(nombre, ok, det=""):
    RES.append((nombre, bool(ok)))
    print("%s %s %s" % ("PASS" if ok else "FAIL", nombre, det), flush=True)


def red(tmp):
    """0-4 S; 5 X gaba; 6 X glutamato; 7-8 D; 9 Y (descendente fuera del objetivo); 10 E relevo excitatorio;
    11 P inhibitoria fuera del motivo (E->P->D); 12 U sin salidas."""
    S, X, D, Y, E, P, U = [0, 1, 2, 3, 4], [5, 6], [7, 8], 9, 10, 11, 12
    filas = []
    for s in S:
        filas += [(s, d, 30, 1) for d in D] + [(s, x, 40, 1) for x in X] + [(s, Y, 30, 1), (s, E, 40, 1)]
    for x in X:
        filas += [(x, d, 20, -1) for d in D] + [(x, Y, 20, -1)]
    filas += [(E, P, 200, 1)] + [(P, d, 10, -1) for d in D]
    n = 13
    ids = np.arange(n, dtype=np.int64) + 1000
    pre = np.array([f[0] for f in filas])
    post = np.array([f[1] for f in filas])
    c = np.array([f[2] for f in filas])
    e = np.array([f[3] for f in filas])
    df = pd.DataFrame({"Presynaptic_ID": ids[pre], "Postsynaptic_ID": ids[post], "Presynaptic_Index": pre,
                       "Postsynaptic_Index": post, "Connectivity": c, "Excitatory": e,
                       "Excitatory x Connectivity": c * e})
    conn = os.path.join(tmp, "conn.parquet")
    comp = os.path.join(tmp, "comp.csv")
    df.to_parquet(conn)
    pd.DataFrame({"Completed": [True] * n}, index=pd.Index(ids, name="")).to_csv(comp)
    conj = {"version": "prueba", "descendentes": {"root": [int(ids[7]), int(ids[8]), int(ids[Y])],
                                                   "tipo": ["DA", "DA", "DY"], "lado": ["right"] * 3},
            "estimulos": {"SYN_right": {"S": [int(ids[s]) for s in S], "D": [int(ids[d]) for d in D],
                                        "D_tipo": ["DA", "DA"], "X": [int(ids[x]) for x in X],
                                        "X_nt": ["gaba", "glutamate"], "X_tipo": ["XG", "XU"],
                                        "unidades_D": 1, "caminos": 2}}}
    rj = os.path.join(tmp, "conj.json")
    json.dump(conj, open(rj, "w"))
    return conn, comp, rj, df, (S, X, D, Y, E, P, U)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shiu", required=True)
    ap.add_argument("--tmp", required=True)
    ap.add_argument("--target", default="")
    ap.add_argument("--n-proc", type=int, default=2)
    ap.add_argument("--n-run", type=int, default=12)
    ap.add_argument("--t-run-ms", type=float, default=200.0)
    a = ap.parse_args()
    os.makedirs(a.tmp, exist_ok=True)
    chk("model_blob", iv.blob(os.path.join(a.shiu, "model.py")) == iv.BLOB_MODEL)
    conn, comp, rj, df, (S, X, D, Y, E, P, U) = red(a.tmp)
    i = df.Presynaptic_Index.to_numpy()
    j = df.Postsynaptic_Index.to_numpy()
    w = df["Excitatory x Connectivity"].to_numpy(dtype=np.float64)
    n = 13
    sys.path.insert(0, a.shiu)
    import brian2
    import model as shiu
    if a.target:
        brian2.prefs.codegen.target = a.target
    # 1. silenciar con mascara == silence() de Shiu, sobre los pesos reales de Brian2
    neu, syn, _ = shiu.create_model(comp, conn, shiu.default_params)
    w_b = np.asarray(syn.w_[:]).copy()
    ib, jb = np.asarray(syn.i[:]), np.asarray(syn.j[:])
    syn = shiu.silence(X + [P], syn)
    w_sh = np.asarray(syn.w_[:]).copy()
    w_mk = iv.editar_pesos(w_b, ib, jb, n, iv.operaciones("C1", S, X + [P], D, [], []))
    chk("silencio_igual_a_shiu", np.array_equal(w_sh, w_mk), "filas_cero=%d" % int((w_sh == 0).sum()))
    chk("orden_sinapsis_igual_parquet", np.array_equal(ib, i) and np.array_equal(jb, j) and
        np.allclose(w_b, w * 0.275e-3))
    # 2. que toca cada condicion
    esper = {"C0": 0, "C1": 6, "C2": 10, "C3": 4, "C4": 10, "R1": 2, "R2": 0, "R3": 20, "R4": 10, "M5": 2}
    for k, v in esper.items():
        t = iv.tocadas(i, j, w, n, iv.operaciones(k, S, X, D, [6], []))
        chk("tocadas_%s" % k, t["filas"] == v, "%d esperado %d" % (t["filas"], v))
    wm5 = iv.editar_pesos(w, i, j, n, iv.operaciones("M5", S, X, D, [6], []))
    chk("M5_invierte_solo_glu_a_D", np.all(wm5[(i == 6) & np.isin(j, D)] > 0) and
        np.all(wm5[(i == 5)] < 0) and np.all(wm5[(i == 6) & (j == Y)] < 0))
    # 3. estadistica y reglas
    p6 = ag.perm_pareada(np.ones(6), 1)
    chk("perm_6_positivos", abs(p6 - 2 / 64) < 0.003, "p=%.5f exacto=%.5f" % (p6, 2 / 64))
    chk("perm_ceros", ag.perm_pareada(np.zeros(5), 1) == 1.0)
    chk("perm_mezcla_alta", ag.perm_pareada(np.array([1.0, -1, 1, -1, 2, -2]), 1) > 0.5)
    h = ag.holm([0.01, 0.04, 0.03, 0.005])
    chk("holm", np.allclose(h, [0.03, 0.06, 0.06, 0.02]), str(h))
    T = {"P1": True, "P2": True, "P3": True, "P4": True}
    chk("veredicto_guarda", ag.veredicto({"x": True}, T, 10, 6, 6) == "INVALIDO")
    chk("veredicto_refutado", ag.veredicto({}, dict(T, P1=False), 10, 6, 6) == "REFUTADO")
    chk("veredicto_sostenido", ag.veredicto({}, T, 10, 6, 6) == "SOSTENIDO_EN_MODELO")
    chk("veredicto_parcial_ratio", ag.veredicto({}, T, 10, 4, 6) == "PARCIAL")
    chk("veredicto_parcial_p4", ag.veredicto({}, dict(T, P4=False), 10, 6, 6) == "PARCIAL")
    chk("k_regla", iv.elegir_k([3, 1, 2], [5, 5, 1], 6) == ([1, 3], 10.0, True))
    chk("k_sin_impulso", iv.elegir_k([3, 1], [5, 5], 0) == ([], 0.0, False))
    chk("global", ag.global_(["SOSTENIDO_EN_MODELO"] * 3 + ["PARCIAL"]) == "SOSTENIDA_EN_MODELO" and
        ag.global_(["REFUTADO"] * 3 + ["PARCIAL"]) == "REFUTADA" and
        ag.global_(["INVALIDO"] * 2 + ["SOSTENIDO_EN_MODELO"] * 2) == "INVALIDA")
    # 4. semilla: mismo ensayo dos veces = mismas cuentas; silenciar U (sin salidas) = nada cambia
    params = dict(shiu.default_params)
    params["r_poi"] = 50 * brian2.Hz
    params["t_run"] = a.t_run_ms * brian2.ms
    mir = list(range(n))
    r1 = iv.ensayo(a.shiu, comp, conn, params, S, 7, [], mir, D, a.target)
    r2 = iv.ensayo(a.shiu, comp, conn, params, S, 7, [], mir, D, a.target)
    r3 = iv.ensayo(a.shiu, comp, conn, params, S, 8, [], mir, D, a.target)
    ru = iv.ensayo(a.shiu, comp, conn, params, S, 7, iv.operaciones("C1", S, [U], D, [], []), mir, D, a.target)
    chk("semilla_reproduce", r1["cuentas"] == r2["cuentas"], str(r1["cuentas"]))
    chk("semilla_distinta_cambia", r1["cuentas"] != r3["cuentas"])
    chk("silenciar_sin_salidas_no_cambia", ru["cuentas"] == r1["cuentas"])
    chk("D_dispara_intacta", sum(r1["cuentas"][d] for d in D) > 0)
    chk("estimulo_sin_refractario", all(r1["cuentas"][s] > 0 for s in S))
    # 5. extremo a extremo: intervenir.py con la celda completa sobre la red sintetica, y agregar
    out = os.path.join(a.tmp, "e2e")
    os.makedirs(out, exist_ok=True)
    cel = {"estimulo": "SYN_right", "hz": 50.0, "conds": list(iv.TODAS), "n_run": a.n_run}
    cmd = [sys.executable, os.path.join(AQUI, "intervenir.py"), "--shiu", a.shiu, "--conn", conn, "--comp", comp,
           "--conjuntos", rj, "--celda", "p_SYN", "--celda-json", json.dumps(cel), "--out", out,
           "--n-proc", str(a.n_proc), "--t-run-ms", str(a.t_run_ms), "--sin-pin"]
    if a.target:
        cmd += ["--target", a.target]
    rc = subprocess.call(cmd)
    chk("intervenir_exit0", rc == 0, "rc=%d" % rc)
    c = json.load(open(os.path.join(out, "celda_p_SYN.json")))
    m = {k: float(np.mean(v["D"])) for k, v in c["conds"].items()}
    mx = {k: float(np.mean(v["X"])) for k, v in c["conds"].items()}
    print("D_media", json.dumps(m), "X_media", json.dumps(mx), "K", json.dumps(c.get("K")), flush=True)
    chk("e2e_C1_mayor", m["C1"] > m["C0"])
    chk("e2e_C2_mayor", m["C2"] > m["C0"])
    chk("e2e_C3_mayor", m["C3"] > m["C0"])
    chk("e2e_C4_menor", m["C4"] < m["C0"])
    chk("e2e_M5_mayor", m["M5"] > m["C0"])
    chk("e2e_X_reclutada_y_silenciada", mx["C0"] > 0 and mx["C2"] < mx["C0"])
    chk("e2e_K_elige_P", c["K"]["indices"] == [P], json.dumps(c["K"]))
    chk("e2e_K_sube_D", m["K"] > m["C0"])
    pos = {x: k for k, x in enumerate(c["indices"]["mirar"])}
    hs = {k: [[r["cuentas"][pos[s]] for s in S] for r in v["ensayos"]] for k, v in c["conds"].items()}
    chk("e2e_crn_S_identico", all(h == hs["C0"] for h in hs.values()))
    # agregado: control positivo y mutantes
    agd = os.path.join(a.tmp, "agr")

    def armar(mut):
        if os.path.isdir(agd):
            for f in os.listdir(agd):
                os.remove(os.path.join(agd, f))
        os.makedirs(agd, exist_ok=True)
        for e in ag.ESTIM:
            for nom in ("p_%s_right", "t20_%s_right", "t150_%s_right", "i_%s_left"):
                cc = copy.deepcopy(c)
                cc["celda"] = nom % e
                mut(cc)
                json.dump(cc, open(os.path.join(agd, "celda_%s.json" % cc["celda"]), "w"))
        ct = copy.deepcopy(c)
        ct["celda"] = "ctrl_mn9"
        ct["n_run"] = 10
        ct["conds"] = {"C0": {"D": [3] * 10, "X": [0] * 10, "tocadas": {"filas": 0}, "ensayos": []}}
        mut(ct)
        json.dump(ct, open(os.path.join(agd, "celda_ctrl_mn9.json"), "w"))
        r = subprocess.call([sys.executable, os.path.join(AQUI, "agregar_mecanismo.py"), "--dir", agd,
                             "--permitir-sin-pin"], stdout=subprocess.DEVNULL)
        return r, json.load(open(os.path.join(agd, "agregado_mecanismo.json")))

    rc, g = armar(lambda cc: None)
    chk("agregar_positivo", rc == 0 and g["global"] == "SOSTENIDA_EN_MODELO",
        "%s %s" % (g["global"], [g["estimulos"][e]["veredicto"] for e in ag.ESTIM]))

    def sin_x(cc):
        if "C1" in cc["conds"]:
            cc["conds"]["C1"]["D"] = list(cc["conds"]["C0"]["D"])
    _, g = armar(sin_x)
    chk("agregar_X_sin_efecto_refuta", g["global"] == "REFUTADA", g["global"])

    def mn9_falla(cc):
        if cc["celda"] == "ctrl_mn9":
            cc["conds"]["C0"]["D"] = [0] * 10
    _, g = armar(mn9_falla)
    chk("agregar_mn9_invalida", g["global"] == "INVALIDA", g["global"])

    def piso(cc):
        if "C1" in cc["conds"]:
            cc["conds"]["C0"]["D"] = [0] * len(cc["conds"]["C0"]["D"])
            cc["conds"]["C1"]["D"] = [0] * len(cc["conds"]["C1"]["D"])
    _, g = armar(piso)
    chk("agregar_piso_invalida", g["global"] == "INVALIDA" and
        all(g["estimulos"][e]["guardas"]["piso"] for e in ag.ESTIM), g["global"])

    def techo(cc):
        if "C1" in cc["conds"]:
            cc["conds"]["C1"]["D"] = [10 ** 6] * len(cc["conds"]["C1"]["D"])
    _, g = armar(techo)
    chk("agregar_techo_invalida", all(g["estimulos"][e]["guardas"]["techo"] for e in ag.ESTIM), g["global"])

    def corte_vacio(cc):
        if "C3" in cc["conds"]:
            cc["conds"]["C3"]["tocadas"]["filas"] = 0
    _, g = armar(corte_vacio)
    chk("agregar_corte_vacio_invalida", g["global"] == "INVALIDA", g["global"])

    armar(lambda cc: None)
    rc = subprocess.call([sys.executable, os.path.join(AQUI, "agregar_mecanismo.py"), "--dir", agd],
                         stdout=subprocess.DEVNULL)
    g = json.load(open(os.path.join(agd, "agregado_mecanismo.json")))
    chk("agregar_sin_pin_invalida", g["global"] == "INVALIDA", g["global"])
    nf = sum(1 for _, ok in RES if not ok)
    print("PRUEBA_MECANISMO %d/%d %s" % (len(RES) - nf, len(RES), "PASS" if nf == 0 else "FAIL"), flush=True)
    raise SystemExit(0 if nf == 0 else 3)


if __name__ == "__main__":
    main()
