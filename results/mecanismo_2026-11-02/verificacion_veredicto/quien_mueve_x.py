#!/usr/bin/env python3
"""DESCRIPTIVO POST HOC, NO SELLADO (respuesta 2026-11-02-004). No cambia ningun veredicto.

Pregunta: en el modelo, quien mueve a X y que neuronas X llevan el freno sobre D, en la corrida 2 (run 41459331354).
Lee las mitades crudas celda_p_*_right_a/_b.json, conjuntos_flywire.json, el parquet de conectividad de Shiu y
Completeness_783.csv. No importa nada del instrumento.

Freno lineal de una X sobre D = espigas medias en 1 s x sinapsis X->D. Es un proxy lineal de la carga inhibitoria que
llega a D; no es un efecto causal por tipo (eso pide silenciar cada tipo: NO MEDIDO).
En el modelo de Shiu solo S recibe Poisson y nadie dispara solo (v_0 -52 < v_th -45), asi que toda actividad nace en S:
en R3 (S conserva solo S->D) lo que dispare X tiene que venir de D.
Uso: python3 quien_mueve_x.py --dir ACTIONS_CORRER2 --parquet P --comp K
"""
import argparse, json
from collections import defaultdict
import numpy as np, pandas as pd, pyarrow.parquet as pq

ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")


def medias(c, cond, idx):
    pos = {x: k for k, x in enumerate(c["indices"]["mirar"])}
    M = np.array([r["cuentas"] for r in c["conds"][cond]["ensayos"]], float).mean(axis=0)
    return np.array([M[pos[int(i)]] for i in idx])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True); ap.add_argument("--parquet", required=True); ap.add_argument("--comp", required=True)
    a = ap.parse_args(); D = a.dir.rstrip("/") + "/"
    conj = json.load(open(D + "conjuntos_flywire.json")); ag = json.load(open(D + "agregado_mecanismo.json"))
    ids = pd.read_csv(a.comp, index_col=0).index.to_numpy(np.int64); f2i = {int(f): k for k, f in enumerate(ids)}; n = len(ids)
    t = pq.read_table(a.parquet, columns=["Presynaptic_Index", "Postsynaptic_Index", "Connectivity"])
    pre = t.column(0).to_numpy(); post = t.column(1).to_numpy(); con = t.column(2).to_numpy().astype(float); del t
    ent_all = np.bincount(post, weights=con, minlength=n)
    for e in ESTIM:
        es = conj["estimulos"][e + "_right"]
        ca = json.load(open(D + "celda_p_%s_right_a.json" % e)); cb = json.load(open(D + "celda_p_%s_right_b.json" % e))
        S = np.array([f2i[x] for x in es["S"]]); X = np.array([f2i[x] for x in es["X"]]); Dn = np.array([f2i[x] for x in es["D"]])
        assert sorted(X.tolist()) == sorted(ca["indices"]["X"])
        tipo = [str(z) for z in es["X_tipo"]]; nt = list(es["X_nt"])
        bD = np.isin(post, Dn); bSp = np.isin(pre, S); bDp = np.isin(pre, Dn)
        syn_xd = np.bincount(pre[bD], weights=con[bD], minlength=n)[X]
        ent = ent_all[X]
        ent_S = np.bincount(post[bSp], weights=con[bSp], minlength=n)[X]
        ent_D = np.bincount(post[bDp], weights=con[bDp], minlength=n)[X]
        esp = {k: medias(ca, k, X) for k in ("C0", "C2", "C4")}
        esp.update({k: medias(cb, k, X) for k in ("R2", "R3")})
        c0b = medias(cb, "C0", X)
        A = ag["estimulos"][e]["descriptivos"]
        f0 = float((esp["C0"] * syn_xd).sum())
        fe = {k: round(float(v.sum() / esp["C0"].sum()), 3) for k, v in esp.items()}
        fr = {k: round(float((v * syn_xd).sum() / f0), 3) for k, v in esp.items()}
        glu = np.array([z == "glutamate" for z in nt])
        print("X %s suma_C0=%.2f (agregado %.2f) C0_a_igual_b=%s espigas_rel=%s freno_rel=%s 1-dSX/dX=%.3f" % (
            e, esp["C0"].sum(), A["X_media"]["C0"], bool(np.array_equal(esp["C0"], c0b)), json.dumps(fe), json.dumps(fr), 1 - ag["estimulos"][e]["dSX_sobre_dX"]))
        print("  ANAT %s sinapsis_S_a_X=%d (%.3f de la entrada de X) sinapsis_D_a_X=%d (%.4f) sinapsis_X_a_D=%d freno_C0_glutamato=%.3f" % (
            e, ent_S.sum(), ent_S.sum() / ent.sum(), ent_D.sum(), ent_D.sum() / ent.sum(), syn_xd.sum(), float((esp["C0"] * syn_xd)[glu].sum() / f0)))
        g = defaultdict(list)
        for k, ty in enumerate(tipo):
            g[ty].append(k)
        filas = []
        for ty, ks in g.items():
            ks = np.array(ks); fz = float((esp["C0"][ks] * syn_xd[ks]).sum()); c0 = float(esp["C0"][ks].sum())
            filas.append((fz / f0, ty, len(ks), nt[ks[0]], int(syn_xd[ks].sum()), c0,
                          (esp["C2"][ks].sum() / c0) if c0 > 0 else float("nan"),
                          (esp["C4"][ks].sum() / c0) if c0 > 0 else float("nan"),
                          (esp["R3"][ks].sum() / c0) if c0 > 0 else float("nan"),
                          ent_S[ks].sum() / ent[ks].sum(), ent_D[ks].sum() / ent[ks].sum()))
        filas.sort(reverse=True)
        acum = 0.0
        for fz, ty, nk, ntk, sd, c0, r2, r4, r3, fs, fd in filas[:8]:
            acum += fz
            print("  TIPO %s %-10s n=%d nt=%s sin_X_a_D=%d espigas_C0=%.1f freno=%.3f acum=%.3f C2/C0=%.2f C4/C0=%.2f R3/C0=%.2f entrada_desde_S=%.3f desde_D=%.3f" % (
                e, ty, nk, ntk, sd, c0, fz, acum, r2, r4, r3, fs, fd))
        print("  TIPOS %s n_tipos=%d top3=%.3f" % (e, len(filas), sum(f[0] for f in filas[:3])))
        # anatomia: que D mandan sinapsis a los tres tipos X que mas frenan
        dtip = dict(zip([f2i[x] for x in es["D"]], es["D_tipo"]))
        for f in filas[:3]:
            ks = np.array([X[k] for k, z in enumerate(tipo) if z == f[1]])
            bq = np.isin(post, ks) & bDp
            cnt = defaultdict(float)
            for p_, c_ in zip(pre[bq], con[bq]):
                cnt[dtip[int(p_)]] += c_
            print("  D_A_X %s %s %s" % (e, f[1], json.dumps({k: int(v) for k, v in sorted(cnt.items(), key=lambda kv: -kv[1])})))
        # S por condicion: donde se rompen los numeros aleatorios comunes
        mir = set(int(z) for z in ca["indices"]["mirar"])
        if all(int(z) in mir for z in S):
            sS = {k: float(medias(ca, k, S).sum()) for k in ("C0", "C1", "C2", "C3", "C4", "M5")}
            sS.update({k: float(medias(cb, k, S).sum()) for k in ("R1", "R2", "R3", "R4", "K")})
            print("  S %s C0=%.2f rel=%s" % (e, sS["C0"], json.dumps({k: round(v / sS["C0"], 4) for k, v in sS.items()})))
        else:
            print("  S %s no_esta_en_mirar" % e)


if __name__ == "__main__":
    main()
