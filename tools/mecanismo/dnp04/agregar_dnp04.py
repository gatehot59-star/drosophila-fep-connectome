#!/usr/bin/env python3
"""H_MECANISMO_DNp04, agregador con las reglas del sello (tools/mecanismo/dnp04/SELLO-DNP04-2026-11-02.md, 40969fb).

Lee celda_q_<E>_right_a.json y celda_q_<E>_right_b.json de --dir, y celda_p_<E>_right_a.json de la corrida 2 en
--previa para la guarda de replica. Permutacion exacta de signos (2^20 asignaciones, dos colas), Holm sobre P1 a P4,
guardas G1 a G5, veredicto, prueba del proxy lineal y descriptivos. Escribe agregado_dnp04.json en --dir.
Uso: python3 agregar_dnp04.py --dir RESULTADOS --previa CORRIDA2
"""
import argparse
import json
import os

import numpy as np

VERSION = "2026-11-02-006"
ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")
FILAS = {"Q1": 1, "Q2": 937, "Q3": 505, "Q4": 1184, "Q5": 1243, "Q6": 1677}
PESO_Q1 = 190.0
PRUEBAS = (("P1", "LC4", "Q1"), ("P2", "LPLC2", "Q1"), ("P3", "LC4", "Q2"), ("P4", "LC4", "Q3"))
PRED = {("PVLP010", "LC4"): 0.729, ("PVLP010", "LPLC2"): 0.194, ("PVLP010", "LPLC1"): 0.217,
        ("LHAD1g1", "LC4"): 0.022, ("LHAD1g1", "LPLC2"): 0.308,
        ("AVLP080", "LPLC2"): 0.201, ("AVLP080", "LPLC1"): 0.624}
COND_TIPO = {"PVLP010": "Q2", "LHAD1g1": "Q5", "AVLP080": "Q6"}
TECNICO = {"LPLC1": ("Q1", "Q3"), "LPLC4": ("Q1", "Q2", "Q3", "Q4")}
CAMPOS = ("seed", "espigas", "activas", "D_primera_ms", "D_temprano")
QS = ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6")
TODAS = ("C0", "C1") + QS


def pr(s):
    print(s, flush=True)


def exacto(d):
    """p de dos colas de la permutacion exacta de signos sobre la media de d."""
    d = np.asarray(d, dtype=np.float64)
    n = len(d)
    if n == 0 or np.all(d == 0):
        return 1.0
    t = abs(d.mean())
    bits = np.arange(n, dtype=np.uint64)
    cnt = 0
    for s0 in range(0, 2 ** n, 1 << 16):
        idx = np.arange(s0, min(s0 + (1 << 16), 2 ** n), dtype=np.uint64)
        s = ((idx[:, None] >> bits) & np.uint64(1)).astype(np.float64) * 2.0 - 1.0
        cnt += int((np.abs(s @ d / n) >= t - 1e-12).sum())
    return cnt / 2 ** n


def holm(p):
    p = np.asarray(p, dtype=np.float64)
    o = np.argsort(p, kind="stable")
    m = len(p)
    out = np.empty(m)
    acc = 0.0
    for r, k in enumerate(o):
        acc = max(acc, min(1.0, (m - r) * p[k]))
        out[k] = acc
    return out


def cuentas(c, cond, idx):
    pos = {x: k for k, x in enumerate(c["indices"]["mirar"])}
    return [[int(r["cuentas"][pos[x]]) for x in idx] for r in c["conds"][cond]["ensayos"]]


def iguales(c1, k1, c2, k2, idx):
    """Ensayo por ensayo: los campos escalares y las cuentas de idx."""
    e1, e2 = c1["conds"][k1]["ensayos"], c2["conds"][k2]["ensayos"]
    if len(e1) != len(e2) or not e1:
        return False
    if any(r1.get(f) != r2.get(f) for r1, r2 in zip(e1, e2) for f in CAMPOS):
        return False
    return cuentas(c1, k1, idx) == cuentas(c2, k2, idx)


def suma(c, cond, idx):
    return np.array([sum(v) for v in cuentas(c, cond, idx)], dtype=np.float64)


def celda_de(ca, cb, q):
    return ca if q in ca["conds"] else cb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--previa", required=True)
    a = ap.parse_args()
    pr("== agregar_dnp04.py :: H_MECANISMO_DNp04 (%s) ==" % VERSION)
    out = {"version": VERSION, "guardas": {}, "estimulos": {}, "pruebas": {}, "proxy": {}}
    ruta_out = os.path.join(a.dir, "agregado_dnp04.json")
    cel, falta = {}, []
    for e in ESTIM:
        for h, ruta in (("a", os.path.join(a.dir, "celda_q_%s_right_a.json" % e)),
                        ("b", os.path.join(a.dir, "celda_q_%s_right_b.json" % e)),
                        ("previa", os.path.join(a.previa, "celda_p_%s_right_a.json" % e))):
            if os.path.exists(ruta):
                with open(ruta) as f:
                    cel[(e, h)] = json.load(f)
            else:
                falta.append(os.path.basename(ruta))
    if falta:
        out["guardas"]["faltan"] = falta
        out["global"] = "INVALIDA"
        with open(ruta_out, "w") as f:
            json.dump(out, f, indent=1, sort_keys=True)
        pr("FALTAN %s" % json.dumps(falta))
        pr("H_MECANISMO_DNp04 INVALIDA (faltan celdas)")
        return
    G = {"G1": {}, "G2": {}, "G3": {}, "G4": {}, "G5": {}}
    dat = {}
    for e in ESTIM:
        ca, cb, cp = cel[(e, "a")], cel[(e, "b")], cel[(e, "previa")]
        S, X, D = ca["indices"]["S"], ca["indices"]["X"], ca["indices"]["D"]
        N = {k: v["indice"] for k, v in ca["nombres"].items()}
        nucleo = S + X + D
        G["G1"][e] = {"C0": iguales(ca, "C0", cp, "C0", nucleo), "C1": iguales(ca, "C1", cp, "C1", nucleo)}
        G["G2"][e] = bool(ca["indices"]["mirar"] == cb["indices"]["mirar"] and
                          iguales(ca, "C0", cb, "C0", ca["indices"]["mirar"]))
        fil = {}
        for c in (ca, cb):
            for q, v in c["conds"].items():
                if q in FILAS:
                    ok = v["tocadas"]["filas"] == FILAS[q]
                    if q == "Q1":
                        ok = ok and abs(v["tocadas"]["peso_abs"] - PESO_Q1) < 1e-9
                    fil[q] = bool(ok)
        G["G3"][e] = bool(len(fil) == len(FILAS) and all(fil.values()))
        tec = {}
        for q in TECNICO.get(e, ()):
            c = celda_de(ca, cb, q)
            tec[q] = iguales(c, q, c, "C0", c["indices"]["mirar"])
        G["G4"][e] = tec
        t_run = ca["t_run_ms"] / 1000.0
        dC0 = np.array(ca["conds"]["C0"]["D"], dtype=np.float64)
        dC1 = np.array(ca["conds"]["C1"]["D"], dtype=np.float64)
        G["G5"][e] = {"techo": bool(max(dC0.mean(), dC1.mean()) / (len(D) * t_run) < 400.0),
                      "piso": bool(dC0.sum() + dC1.sum() > 0)}
        dp = [d for d in D if d != N["DNp04"]]
        dd = {q: suma(celda_de(ca, cb, q), q, dp) for q in TODAS}
        c0a, c0b = dd["C0"], suma(cb, "C0", dp)
        dx = float((dd["C1"] - c0a).mean())
        dif = {q: dd[q] - (c0a if q in ca["conds"] else c0b) for q in QS}
        r = {q: (float(dif[q].mean()) / dx if dx != 0 else float("nan")) for q in QS}
        nom = {k: {q: float(np.mean(celda_de(ca, cb, q)["conds"][q]["nombres"][k])) for q in TODAS} for k in N}
        pv0 = float(np.mean(cb["conds"]["C0"]["nombres"]["PVLP010"]))
        s4 = float(np.mean(cb["conds"]["Q4"]["nombres"]["PVLP010"])) / pv0 if pv0 > 0 else float("nan")
        q4c0 = float(dd["Q4"].mean() / c0b.mean()) if c0b.mean() > 0 else float("nan")
        dtipo = {}
        for q in TODAS:
            m = np.mean(cuentas(celda_de(ca, cb, q), q, D), axis=0)
            dtipo[q] = {"%s_%d" % (t, k): float(v) for k, (t, v) in enumerate(zip(ca["D_tipo"], m))}
        dat[e] = {"dif": dif, "r": r, "dx": dx, "dprima": {q: float(v.mean()) for q, v in dd.items()},
                  "nombres": nom, "s4": s4, "q4_sobre_c0": q4c0, "D_tipo_media": dtipo}
    ps, info = [], []
    for nom_p, e, q in PRUEBAS:
        d = dat[e]["dif"][q]
        ps.append(exacto(d))
        info.append((nom_p, e, q, float(d.mean()), int((d > 0).sum()), int((d < 0).sum()), len(d)))
    adj = holm(ps)
    P = {}
    for (nom_p, e, q, md, npos, nneg, nt), p, ph in zip(info, ps, adj):
        P[nom_p] = {"estimulo": e, "cond": q, "media_dif": md, "positivos": npos, "negativos": nneg, "n": nt,
                    "p": float(p), "p_holm": float(ph), "pasa": bool(md > 0 and ph < 0.05)}
    ok = {"G1": all(all(v.values()) for v in G["G1"].values()),
          "G2": all(G["G2"].values()),
          "G3": all(G["G3"].values()),
          "G4": all(all(v.values()) for v in G["G4"].values()) and sum(len(v) for v in G["G4"].values()) == 6,
          "G5": all(all(v.values()) for v in G["G5"].values())}
    L = dat["LC4"]
    r1, r2, s4 = L["r"]["Q1"], L["r"]["Q2"], L["s4"]
    if not all(ok.values()):
        ver = "INVALIDA"
    elif not P["P1"]["pasa"] or not (r1 >= 0.10):
        ver = "REFUTADA"
    elif r1 >= 0.25 and s4 >= 0.8 and P["P3"]["pasa"] and r2 >= 0.5:
        ver = "SOSTENIDA_EN_MODELO"
    else:
        ver = "PARCIAL"
    prox = {}
    for (t, e), pred in PRED.items():
        med = dat[e]["r"][COND_TIPO[t]]
        prox["%s_%s" % (t, e)] = {"pred": pred, "medido": med, "pasa": bool(abs(med - pred) <= 0.15)}
    npasa = sum(1 for v in prox.values() if v["pasa"])
    pver = "PROXY_UTIL" if npasa >= 5 else ("PROXY_FALLA" if npasa <= 2 else "PROXY_PARCIAL")
    fuera = {"%s_%s" % (t, e): dat[e]["r"][COND_TIPO[t]] for t in COND_TIPO for e in ESTIM if (t, e) not in PRED}
    for e in ESTIM:
        x = dat[e]
        pr("ESTIMULO %s dXprima=%.2f Dprima=%s r=%s s4=%.4f DprimaQ4/DprimaC0=%.4f" % (
            e, x["dx"], json.dumps({q: round(v, 2) for q, v in x["dprima"].items()}),
            json.dumps({q: round(v, 4) for q, v in x["r"].items()}), x["s4"], x["q4_sobre_c0"]))
        pr("  NOMBRES %s %s" % (e, json.dumps({k: {q: round(v, 2) for q, v in d.items()} for k, d in x["nombres"].items()})))
        pr("  GUARDAS %s G1=%s G2=%s G3=%s G4=%s G5=%s" % (
            e, json.dumps(G["G1"][e]), G["G2"][e], G["G3"][e], json.dumps(G["G4"][e]), json.dumps(G["G5"][e])))
    for k, v in P.items():
        pr("PRUEBA %s %s %s media_dif=%.2f positivos=%d/%d negativos=%d p=%.3g p_holm=%.3g pasa=%s" % (
            k, v["estimulo"], v["cond"], v["media_dif"], v["positivos"], v["n"], v["negativos"], v["p"], v["p_holm"],
            v["pasa"]))
    for k, v in prox.items():
        pr("PROXY %s predicho=%.3f medido=%.4f pasa=%s" % (k, v["pred"], v["medido"], v["pasa"]))
    pr("PROXY_FUERA_DE_X %s" % json.dumps({k: round(v, 4) for k, v in fuera.items()}))
    pr("PROXY_VEREDICTO %s %d/7" % (pver, npasa))
    pr("DESCRIPTIVOS LC4 r_Q3-r_Q1=%.4f DprimaQ4/DprimaC0=%.4f" % (L["r"]["Q3"] - r1, L["q4_sobre_c0"]))
    pr("GUARDAS_GLOBALES %s" % json.dumps(ok, sort_keys=True))
    out["guardas"] = {"por_estimulo": G, "globales": ok}
    out["pruebas"] = P
    out["proxy"] = {"pares": prox, "n_pasa": npasa, "veredicto": pver, "fuera_de_x": fuera}
    for e in ESTIM:
        x = dict(dat[e])
        x["dif"] = {q: v.tolist() for q, v in x["dif"].items()}
        out["estimulos"][e] = x
    out["global"] = ver
    with open(ruta_out, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    pr("H_MECANISMO_DNp04 %s r_Q1=%.4f r_Q2=%.4f s4=%.4f" % (ver, r1, r2, s4))


if __name__ == "__main__":
    main()
