#!/usr/bin/env python3
"""Verificador independiente de H_MECANISMO_DNp04 (respuesta 2026-11-02-006, sello SELLO-DNP04-2026-11-02.md).

No importa agregar_dnp04 ni intervenir. Lee las celdas crudas q_<E>_right_a/_b y las previas p_<E>_right_a, recalcula
D' desde las cuentas por neurona (no desde los campos D ni nombres), la prueba exacta de signos por convolucion entera
(otro algoritmo que la enumeracion del agregador), Holm, las guardas G1 a G5, el veredicto y el proxy con las reglas
del sello, y compara todo con agregado_dnp04.json. Con --parquet recuenta las filas que toca cada Q con mascaras
propias. Los indices de las cuatro neuronas salen del sello, no de las celdas.
Uso: python3 verificar_dnp04.py --dir CORRIDA --previa CORRIDA2 [--parquet P] [--nombres JSON]
"""
import argparse
import json
import math
import os

import numpy as np

ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")
FILAS = {"Q1": 1, "Q2": 937, "Q3": 505, "Q4": 1184, "Q5": 1243, "Q6": 1677}
IDX = {"DNp04": 95123, "PVLP010": 37128, "LHAD1g1": 105779, "AVLP080": 6128}
PRED = (("PVLP010", "LC4", 0.729), ("PVLP010", "LPLC2", 0.194), ("PVLP010", "LPLC1", 0.217),
        ("LHAD1g1", "LC4", 0.022), ("LHAD1g1", "LPLC2", 0.308), ("AVLP080", "LPLC2", 0.201),
        ("AVLP080", "LPLC1", 0.624))
QTIPO = {"PVLP010": "Q2", "LHAD1g1": "Q5", "AVLP080": "Q6"}
TEC = (("LPLC1", "Q1"), ("LPLC1", "Q3"), ("LPLC4", "Q1"), ("LPLC4", "Q2"), ("LPLC4", "Q3"), ("LPLC4", "Q4"))
ESC = ("seed", "espigas", "activas", "D_primera_ms", "D_temprano")
A_COND = ("C0", "C1", "Q1", "Q2")
B_COND = ("C0", "Q3", "Q4", "Q5", "Q6")


def p_conv(d):
    """p exacta de dos colas: distribucion de sum(s_i*|d_i|) por convolucion entera de las 2^n asignaciones."""
    d = np.asarray(d, dtype=np.float64)
    if not np.all(d == np.round(d)):
        raise ValueError("diferencias no enteras")
    a = np.abs(d).astype(np.int64)
    tot = int(a.sum())
    cnt = np.zeros(2 * tot + 1, dtype=np.int64)
    cnt[tot] = 1
    for v in a:
        nuevo = np.zeros_like(cnt)
        if v == 0:
            nuevo = 2 * cnt
        else:
            nuevo[v:] += cnt[:-v]
            nuevo[:-v] += cnt[v:]
        cnt = nuevo
    assert int(cnt.sum()) == 2 ** len(a)
    obs = abs(int(np.round(d.sum())))
    s = np.arange(-tot, tot + 1)
    return int(cnt[np.abs(s) >= obs].sum()) / 2 ** len(a)


def holm(p):
    m = len(p)
    orden = sorted(range(m), key=lambda k: (p[k], k))
    adj, run = [0.0] * m, 0.0
    for r, k in enumerate(orden):
        run = max(run, min(1.0, (m - r) * p[k]))
        adj[k] = run
    return adj


def carga(ruta):
    with open(ruta) as f:
        return json.load(f)


def cnt(c, cond, idx):
    pos = {m: k for k, m in enumerate(c["indices"]["mirar"])}
    return np.array([[r["cuentas"][pos[x]] for x in idx] for r in c["conds"][cond]["ensayos"]], dtype=np.int64)


def mismo(c1, k1, c2, k2, idx):
    e1, e2 = c1["conds"][k1]["ensayos"], c2["conds"][k2]["ensayos"]
    if len(e1) != len(e2) or len(e1) == 0:
        return False, "n %d %d" % (len(e1), len(e2))
    for t, (r1, r2) in enumerate(zip(e1, e2)):
        for f in ESC:
            if f not in r1 or f not in r2 or r1[f] != r2[f]:
                return False, "ensayo %d campo %s" % (t, f)
    a, b = cnt(c1, k1, idx), cnt(c2, k2, idx)
    if not np.array_equal(a, b):
        t, k = np.argwhere(a != b)[0]
        return False, "ensayo %d neurona %d: %d contra %d" % (t, idx[k], a[t, k], b[t, k])
    return True, ""


def filas_parquet(ruta, N):
    import pandas as pd
    df = pd.read_parquet(ruta, columns=["Presynaptic_Index", "Postsynaptic_Index", "Excitatory x Connectivity"])
    i = df["Presynaptic_Index"].to_numpy(dtype=np.int64)
    j = df["Postsynaptic_Index"].to_numpy(dtype=np.int64)
    w = df["Excitatory x Connectivity"].to_numpy(dtype=np.float64)
    dn, pv, lh, av = N["DNp04"], N["PVLP010"], N["LHAD1g1"], N["AVLP080"]
    m = {"Q1": (i == dn) & (j == pv), "Q2": i == pv, "Q3": i == dn, "Q4": (j == pv) & (i != dn), "Q5": i == lh,
         "Q6": i == av}
    return {q: (int((v & (w != 0)).sum()), float(np.abs(w[v]).sum())) for q, v in m.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--previa", required=True)
    ap.add_argument("--parquet", default="")
    ap.add_argument("--nombres", default="", help="solo prueba: indices propios de las cuatro neuronas")
    a = ap.parse_args()
    N = json.loads(a.nombres) if a.nombres else dict(IDX)
    print("== verificar_dnp04.py :: verificacion independiente de H_MECANISMO_DNp04 ==", flush=True)
    C = {}
    for e in ESTIM:
        C[e] = (carga(os.path.join(a.dir, "celda_q_%s_right_a.json" % e)),
                carga(os.path.join(a.dir, "celda_q_%s_right_b.json" % e)),
                carga(os.path.join(a.previa, "celda_p_%s_right_a.json" % e)))
    ok = {"G1": True, "G2": True, "G3": True, "G4": True, "G5": True}
    est, estructura = {}, {}
    pq = filas_parquet(a.parquet, N) if a.parquet else None
    if pq:
        bien = all(pq[q][0] == FILAS[q] for q in FILAS) and abs(pq["Q1"][1] - 190.0) < 1e-9
        print("FILAS_PARQUET %s igual_al_sello=%s" % (json.dumps(pq, sort_keys=True), bien), flush=True)
        ok["G3"] = ok["G3"] and bien
    for e in ESTIM:
        ca, cb, cp = C[e]
        S, X, D = cp["indices"]["S"], cp["indices"]["X"], cp["indices"]["D"]
        mismos_conj = all(ca["indices"][k] == cp["indices"][k] == cb["indices"][k] for k in ("S", "X", "D"))
        conds_ok = sorted(ca["conds"]) == sorted(A_COND) and sorted(cb["conds"]) == sorted(B_COND)
        n_ok = all(len(c["conds"][q]["ensayos"]) == 20 for c in (ca, cb) for q in c["conds"])
        semillas = all([r["seed"] for r in c["conds"][q]["ensayos"]] == [20261102 + t for t in range(20)]
                       for c in (ca, cb) for q in c["conds"])
        nom_ok = a.nombres != "" or all(ca["nombres"][k]["indice"] == N[k] == cb["nombres"][k]["indice"] for k in N)
        g1 = [mismo(ca, k, cp, k, S + X + D) for k in ("C0", "C1")]
        g1_ok = all(x[0] for x in g1) and mismos_conj
        g2 = mismo(ca, "C0", cb, "C0", ca["indices"]["mirar"])
        g2_ok = g2[0] and ca["indices"]["mirar"] == cb["indices"]["mirar"]
        toc = {q: c["conds"][q]["tocadas"] for c in (ca, cb) for q in c["conds"] if q in FILAS}
        g3_ok = (sorted(toc) == sorted(FILAS) and all(toc[q]["filas"] == FILAS[q] for q in FILAS) and
                 abs(toc["Q1"]["peso_abs"] - 190.0) < 1e-9)
        g4 = {}
        for ee, q in TEC:
            if ee == e:
                c = ca if q in ca["conds"] else cb
                g4[q] = mismo(c, q, c, "C0", c["indices"]["mirar"])
        t_s = ca["t_run_ms"] / 1000.0
        tot = {k: cnt(ca, k, D).sum(axis=1) for k in ("C0", "C1")}
        techo = max(tot["C0"].mean(), tot["C1"].mean()) / (len(D) * t_s) < 400.0
        piso = (tot["C0"].sum() + tot["C1"].sum()) > 0
        ok["G1"] &= g1_ok
        ok["G2"] &= g2_ok
        ok["G3"] &= g3_ok
        ok["G4"] &= all(v[0] for v in g4.values())
        ok["G5"] &= bool(techo and piso)
        Dp = [d for d in D if d != N["DNp04"]]
        dp = {}
        for c in (ca, cb):
            for q in c["conds"]:
                if not (c is cb and q == "C0"):
                    dp[q] = cnt(c, q, Dp).sum(axis=1)
        dp["C0b"] = cnt(cb, "C0", Dp).sum(axis=1)
        base = {q: ("C0" if q in A_COND else "C0b") for q in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6")}
        dx = float((dp["C1"] - dp["C0"]).mean())
        dif = {q: dp[q] - dp[base[q]] for q in base}
        r = {q: (float(v.mean()) / dx if dx != 0 else float("nan")) for q, v in dif.items()}
        nom = {}
        for k in N:
            nom[k] = {}
            for c in (ca, cb):
                for q in c["conds"]:
                    key = q if not (c is cb and q == "C0") else "C0b"
                    nom[k][key] = float(cnt(c, q, [N[k]]).mean())
        s4 = nom["PVLP010"]["Q4"] / nom["PVLP010"]["C0b"] if nom["PVLP010"]["C0b"] > 0 else float("nan")
        tipo = {}
        for c in (ca, cb):
            for q in c["conds"]:
                key = q if not (c is cb and q == "C0") else "C0b"
                m = cnt(c, q, D).mean(axis=0)
                tipo[key] = {"%s_%d" % (t, k): round(float(v), 2) for k, (t, v) in enumerate(zip(cp["D_tipo"], m))}
        est[e] = {"dx": dx, "dif": dif, "r": r, "s4": s4, "nom": nom, "dp": {q: float(v.mean()) for q, v in dp.items()},
                  "tipo": tipo}
        print("CELDAS %s conjuntos_iguales=%s conds=%s n20=%s semillas=%s indices_sello=%s" % (
            e, mismos_conj, conds_ok, n_ok, semillas, nom_ok), flush=True)
        print("  G1 %s C0=%s C1=%s | G2 %s %s | G3 %s %s | G4 %s | G5 techo=%s piso=%s" % (
            e, g1[0], g1[1], g2_ok, g2[1], g3_ok, json.dumps({q: toc[q]["filas"] for q in sorted(toc)}),
            json.dumps({q: v[0] for q, v in g4.items()}), techo, piso), flush=True)
        estructura[e] = bool(conds_ok and n_ok and semillas and nom_ok)
        print("  DPRIMA %s %s dX'=%.2f" % (e, json.dumps({q: round(v, 2) for q, v in est[e]["dp"].items()}), dx),
              flush=True)
        print("  R %s %s s4=%.4f" % (e, json.dumps({q: round(v, 4) for q, v in r.items()}), s4), flush=True)
        print("  NOMBRES %s %s" % (e, json.dumps({k: {q: round(v, 2) for q, v in d.items()} for k, d in nom.items()})),
              flush=True)
    pruebas = (("P1", "LC4", "Q1"), ("P2", "LPLC2", "Q1"), ("P3", "LC4", "Q2"), ("P4", "LC4", "Q3"))
    ps = [p_conv(est[e]["dif"][q]) for _, e, q in pruebas]
    ph = holm(ps)
    P = {}
    for (k, e, q), p, h in zip(pruebas, ps, ph):
        d = est[e]["dif"][q]
        P[k] = {"p": p, "p_holm": h, "media": float(d.mean()), "pos": int((d > 0).sum()), "neg": int((d < 0).sum()),
                "pasa": bool(h < 0.05 and d.mean() > 0)}
        print("PRUEBA %s %s %s media=%.2f pos=%d neg=%d p=%.6g p_holm=%.6g pasa=%s" % (
            k, e, q, P[k]["media"], P[k]["pos"], P[k]["neg"], p, h, P[k]["pasa"]), flush=True)
    L = est["LC4"]
    r1, r2, s4 = L["r"]["Q1"], L["r"]["Q2"], L["s4"]
    print("ESTRUCTURA %s" % json.dumps(estructura, sort_keys=True), flush=True)
    if not all(ok.values()) or not all(estructura.values()):
        ver = "INVALIDA"
    elif (not P["P1"]["pasa"]) or math.isnan(r1) or r1 < 0.10:
        ver = "REFUTADA"
    elif r1 >= 0.25 and s4 >= 0.8 and P["P3"]["pasa"] and r2 >= 0.5:
        ver = "SOSTENIDA_EN_MODELO"
    else:
        ver = "PARCIAL"
    pas = []
    for t, e, pred in PRED:
        med = est[e]["r"][QTIPO[t]]
        pas.append(abs(med - pred) <= 0.15)
        print("PROXY %s_%s predicho=%.3f medido=%.4f pasa=%s" % (t, e, pred, med, pas[-1]), flush=True)
    npasa = sum(pas)
    pver = "PROXY_UTIL" if npasa >= 5 else ("PROXY_FALLA" if npasa <= 2 else "PROXY_PARCIAL")
    print("DESCRIPTIVOS LC4 r_Q3-r_Q1=%.4f DprimaQ4/DprimaC0=%.4f" % (
        L["r"]["Q3"] - r1, L["dp"]["Q4"] / L["dp"]["C0b"]), flush=True)
    for e in ("LC4", "LPLC2"):
        print("  D_TIPO %s %s" % (e, json.dumps(est[e]["tipo"])), flush=True)
    print("GUARDAS_PROPIAS %s" % json.dumps(ok, sort_keys=True), flush=True)
    ag_ruta = os.path.join(a.dir, "agregado_dnp04.json")
    if os.path.exists(ag_ruta):
        g = carga(ag_ruta)
        cmp = {"global": g.get("global") == ver,
               "guardas": g["guardas"]["globales"] == ok,
               "p": all(abs(g["pruebas"][k]["p"] - P[k]["p"]) < 1e-12 and
                        abs(g["pruebas"][k]["p_holm"] - P[k]["p_holm"]) < 1e-12 and
                        g["pruebas"][k]["pasa"] == P[k]["pasa"] for k in P),
               "r": all(abs(g["estimulos"][e]["r"][q] - est[e]["r"][q]) < 1e-9 or
                        (math.isnan(g["estimulos"][e]["r"][q]) and math.isnan(est[e]["r"][q]))
                        for e in ESTIM for q in est[e]["r"]),
               "s4": abs(g["estimulos"]["LC4"]["s4"] - s4) < 1e-9,
               "proxy": g["proxy"]["veredicto"] == pver and g["proxy"]["n_pasa"] == npasa}
        print("COMPARA_AGREGADO %s todo_igual=%s" % (json.dumps(cmp, sort_keys=True), all(cmp.values())), flush=True)
    else:
        print("COMPARA_AGREGADO NO_MEDIDO: no hay agregado_dnp04.json", flush=True)
    print("PROXY_PROPIO %s %d/7" % (pver, npasa), flush=True)
    print("H_MECANISMO_DNp04_PROPIO %s r_Q1=%.4f r_Q2=%.4f s4=%.4f" % (ver, r1, r2, s4), flush=True)


if __name__ == "__main__":
    main()
