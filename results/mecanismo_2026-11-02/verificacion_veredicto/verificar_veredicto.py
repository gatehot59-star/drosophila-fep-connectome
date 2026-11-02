#!/usr/bin/env python3
"""Verificacion independiente del veredicto de H_MECANISMO, corrida 2 (run 41459331354), respuesta 2026-11-02-004.

No importa nada del instrumento. Lee las mitades crudas p_*_right_a y p_*_right_b (no la celda unida), recomputa D
desde las cuentas por neurona, usa permutacion EXACTA de signos (2^20) en vez de Monte Carlo, aplica Holm y las
reglas del sello, rehace con codigo propio las filas tocadas por cada condicion sobre el parquet de Shiu y la seleccion
de K, y compara todo contra agregado_mecanismo.json.
Uso: python3 verificar_veredicto.py --dir ACTIONS_CORRER2 --parquet P --comp K
"""
import argparse, json, os
import numpy as np, pandas as pd, pyarrow.parquet as pq

ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")
PRU = (("P1", "C1", "C0"), ("P2", "C2", "C0"), ("P3", "C3", "C0"), ("P4", "C0", "C4"))


def exacto(d):
    d = np.asarray(d, float); n = len(d)
    if np.all(d == 0):
        return 1.0
    t = abs(d.mean()); bits = np.arange(n, dtype=np.uint64); cnt = 0
    for s0 in range(0, 2 ** n, 1 << 16):
        idx = np.arange(s0, min(s0 + (1 << 16), 2 ** n), dtype=np.uint64)
        s = (((idx[:, None] >> bits) & np.uint64(1)).astype(np.float64) * 2 - 1)
        cnt += int((np.abs(s @ d / n) >= t - 1e-12).sum())
    return cnt / 2 ** n


def holm(p):
    p = np.asarray(p, float); o = np.argsort(p, kind="stable"); m = len(p); out = np.empty(m); acc = 0.0
    for r, k in enumerate(o):
        acc = max(acc, min(1.0, (m - r) * p[k])); out[k] = acc
    return out


def sumas(c, cond, grupo):
    I = c["indices"]; pos = {x: k for k, x in enumerate(I["mirar"])}
    return np.array([sum(r["cuentas"][pos[x]] for x in I[grupo]) for r in c["conds"][cond]["ensayos"]], float)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True); ap.add_argument("--parquet", required=True); ap.add_argument("--comp", required=True)
    a = ap.parse_args(); D = a.dir.rstrip("/") + "/"
    ag = json.load(open(D + "agregado_mecanismo.json"))
    conj = json.load(open(D + "conjuntos_flywire.json"))
    ids = pd.read_csv(a.comp, index_col=0).index.to_numpy(np.int64); f2i = {int(f): k for k, f in enumerate(ids)}; n = len(ids)
    t = pq.read_table(a.parquet, columns=["Presynaptic_Index", "Postsynaptic_Index", "Connectivity", "Excitatory x Connectivity"])
    pre = t.column(0).to_numpy(); post = t.column(1).to_numpy(); con = t.column(2).to_numpy().astype(float); w = t.column(3).to_numpy().astype(float); del t
    inh = np.zeros(n, bool); inh[pre[w < 0]] = True
    ctrl = json.load(open(D + "celda_ctrl_mn9.json")); mn9 = sum(1 for v in ctrl["conds"]["C0"]["D"] if v > 0) >= 9
    print("CTRL_MN9 ensayos_con_espiga=%d -> %s (agregado %s)" % (sum(1 for v in ctrl["conds"]["C0"]["D"] if v > 0), mn9, ag["ctrl_mn9"]))
    ps, info, filas = [], [], {}
    for i, e in enumerate(ESTIM):
        ca = json.load(open(D + "celda_p_%s_right_a.json" % e)); cb = json.load(open(D + "celda_p_%s_right_b.json" % e))
        es = conj["estimulos"][e + "_right"]
        S = np.array([f2i[x] for x in es["S"]]); X = np.array([f2i[x] for x in es["X"]]); Dn = np.array([f2i[x] for x in es["D"]])
        Xg = np.array([f2i[x] for x, nt in zip(es["X"], es["X_nt"]) if nt == "glutamate"])
        assert sorted(S.tolist()) == sorted(ca["indices"]["S"]) and sorted(X.tolist()) == sorted(ca["indices"]["X"]) and sorted(Dn.tolist()) == sorted(ca["indices"]["D"])
        bS = np.isin(pre, S); bXp = np.isin(pre, X); bXq = np.isin(post, X); bD = np.isin(post, Dn); bXg = np.isin(pre, Xg)
        nz = w != 0
        # pool y K, con codigo propio
        syn_d = np.bincount(pre[bD], weights=con[bD], minlength=n)
        excl = set(S.tolist()) | set(X.tolist()) | set(Dn.tolist())
        pool = [int(p) for p in np.flatnonzero(inh & (syn_d >= 5)) if int(p) not in excl]
        posb = {x: k for k, x in enumerate(cb["indices"]["mirar"])}
        med = np.mean([r["cuentas"] for r in cb["conds"]["C0"]["ensayos"]], axis=0)
        dx = float(sum(med[posb[int(x)]] * syn_d[x] for x in X))
        cand = sorted((-(med[posb[p]] * syn_d[p]), p) for p in pool if med[posb[p]] * syn_d[p] > 0)
        K, acc = [], 0.0
        for nd, p in cand:
            if acc >= dx:
                break
            K.append(p); acc += -nd
        k_ok = K == cb["K"]["indices"] and pool == cb["indices"]["pool"]
        bK = np.isin(pre, np.array(K)) if K else np.zeros(len(pre), bool)
        mask = {"C1": bXp, "C2": bS & bXq, "C3": bXp & bD, "C4": bS & bD, "R1": bXp & ~bD, "R2": ~bS & bXq,
                "R3": bS & ~bD, "R4": bS & ~(bD | bXq), "M5": bXg & bD & (w < 0), "K": bK}
        reg = {k: (ca if k in ca["conds"] else cb)["conds"][k]["tocadas"]["filas"] for k in mask}
        mine = {k: int((m & nz).sum()) for k, m in mask.items()}
        filas[e] = (mine == reg, mine)
        print("FILAS %s propias=%s registradas_iguales=%s K_reconstruido=%s n_K=%d drive_x=%.1f drive_k=%.1f alcanzo=%s X_inhibitorias=%s X_glu=%d" % (
            e, json.dumps(mine), mine == reg, k_ok, len(K), dx, acc, acc >= dx, bool((w[bXp & nz] < 0).all()), len(Xg)))
        dd = {k: sumas(ca, k, "D") for k in ("C0", "C1", "C2", "C3", "C4", "M5")}
        dd.update({k: sumas(cb, k, "D") for k in ("R1", "R2", "R3", "R4", "K")})
        c0b = sumas(cb, "C0", "D")
        guard = {"techo": any(dd[k].mean() / (len(Dn) * ca["t_run_ms"] / 1000) >= 400 for k in ("C0", "C1")),
                 "piso": dd["C0"].sum() == 0 and dd["C1"].sum() == 0, "corte_vacio": any(mine[k] == 0 for k in ("C2", "C3", "C4")),
                 "X_no_inh": not bool((w[bXp & nz] < 0).all()), "mn9": not mn9, "C0_ab_distintos": not np.array_equal(dd["C0"], c0b)}
        for tnom, x, y in PRU:
            d = dd[x] - dd[y]; ps.append(exacto(d)); info.append((e, tnom, d.mean(), int((d > 0).sum())))
        m = {k: v.mean() for k, v in dd.items()}
        print("D_MEDIA %s %s guardas=%s" % (e, json.dumps({k: round(v, 2) for k, v in m.items()}), [k for k, v in guard.items() if v]))
        filas[e] = filas[e] + (guard, m)
    adj = holm(ps)
    vs = []
    for i, e in enumerate(ESTIM):
        guard, m = filas[e][2], filas[e][3]
        rows = [(info[4 * i + t], ps[4 * i + t], adj[4 * i + t]) for t in range(4)]
        pasa = {r[0][1]: bool(r[0][2] > 0 and r[2] < 0.05) for r in rows}
        dX, dSX, dXD = rows[0][0][2], rows[1][0][2], rows[2][0][2]
        r1, r2 = dSX / dX, dXD / dX
        if any(guard.values()):
            v = "INVALIDO"
        elif not pasa["P1"]:
            v = "REFUTADO"
        elif all(pasa.values()) and r1 >= 0.5 and r2 >= 0.5:
            v = "SOSTENIDO_EN_MODELO"
        else:
            v = "PARCIAL"
        vs.append(v)
        A = ag["estimulos"][e]
        igual = (v == A["veredicto"] and all(pasa[k] == A["pruebas"][k]["pasa"] for k in pasa) and
                 abs(r1 - A["dSX_sobre_dX"]) < 1e-9 and abs(r2 - A["dXD_sobre_dX"]) < 1e-9 and
                 all(abs(m[k] - A["descriptivos"]["D_media"][k]) < 1e-9 for k in m))
        for (ee, tnom, md, npos), p, ph in rows:
            print("  %s %s media_dif=%.2f positivos=%d/20 p_exacto=%.3g p_holm=%.3g pasa=%s (agregado p=%.3g pasa=%s)" % (
                e, tnom, md, npos, p, ph, pasa[tnom], A["pruebas"][tnom]["p"], A["pruebas"][tnom]["pasa"]))
        fR1 = (m["C1"] - m["R1"]) / (m["C1"] - m["C0"]); fR2 = (m["C1"] - m["R2"]) / (m["C1"] - m["C0"])
        print("VEREDICTO %s %s dSX/dX=%.4f dXD/dX=%.4f fR1=%.3f fR2=%.3f fR3=%.3f fR4=%.3f K/X=%.3f M5-C0=%.1f M5-C1=%.1f igual_al_agregado=%s" % (
            e, v, r1, r2, fR1, fR2, m["R3"] / m["C0"], m["R4"] / m["C0"], (m["K"] - m["C0"]) / (m["C1"] - m["C0"]), m["M5"] - m["C0"], m["M5"] - m["C1"], igual))
        # fuera del objetivo y replica izquierda. Corregido en v2: recarga la celda del estimulo e (la v1 usaba la ultima celda del primer lazo, LPLC4, para los cuatro)
        ca = json.load(open(D + "celda_p_%s_right_a.json" % e))
        posa = {x: k for k, x in enumerate(ca["indices"]["mirar"])}
        de = ca["indices"]["desc"]
        o0 = np.array([sum(r["cuentas"][posa[x]] for x in de) for r in ca["conds"]["C0"]["ensayos"]], float)
        o1 = np.array([sum(r["cuentas"][posa[x]] for x in de) for r in ca["conds"]["C1"]["ensayos"]], float)
        cl = json.load(open(D + "celda_i_%s_left.json" % e))
        izq = []
        for tnom, x, y in PRU:
            d = sumas(cl, x, "D") - sumas(cl, y, "D"); izq.append("%s %+.1f %d/20 p=%.2g" % (tnom, d.mean(), int((d > 0).sum()), exacto(d)))
        FO = A["descriptivos"]["fuera_objetivo"]
        fo_ig = abs(o0.mean() - FO["C0"]) < 1e-9 and abs(o1.mean() - FO["C1"]) < 1e-9
        IZ = ag.get("izquierda", {}); IZ = IZ.get(e, IZ.get(e + "_left"))
        print("  FUERA %s C0=%.2f C1=%.2f cociente=%.2f positivos=%d/20 p_exacto=%.3g (agregado C0=%.2f C1=%.2f igual=%s) | IZQUIERDA %s | agregado_izq=%s" % (
            e, o0.mean(), o1.mean(), o1.mean() / o0.mean(), int((o1 > o0).sum()), exacto(o1 - o0), FO["C0"], FO["C1"], fo_ig, "; ".join(izq), json.dumps(IZ)[:400]))
    g = "INVALIDA" if sum(v == "INVALIDO" for v in vs) >= 2 else ("SOSTENIDA_EN_MODELO" if sum(v == "SOSTENIDO_EN_MODELO" for v in vs) >= 3 and "REFUTADO" not in vs else ("REFUTADA" if sum(v == "REFUTADO" for v in vs) >= 3 else "MIXTA"))
    print("H_MECANISMO_PROPIO %s (agregado %s) filas_todas_iguales=%s" % (g, ag["global"], all(filas[e][0] for e in ESTIM)))


if __name__ == "__main__":
    main()
