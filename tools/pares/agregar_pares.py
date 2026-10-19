#!/usr/bin/env python3
"""H_PARES_DATOS: agregador del sello tools/pares/SELLO-PARES-DATOS.md (commit 0d30190). Respuesta 2026-10-14-059.

Lee los mosca_c*_t*.json y crudo_c*.json de --dir, chequea controles y plan, arma las curvas y decide H_DATOS_EMBUDO,
H_DATOS_CRUDO y H_DATOS_PRIMER_DIA con el bootstrap de tres ejes del sello: repeticiones (las mismas para todos los
brazos y las dos celdas), taus (las mismas para W y MOSCA_L) y matrices de PROY_L; B = 20.000, semilla 2063,
percentiles 2,5 y 97,5. Por cada muestra se sortean, en este orden, repeticiones, taus y matrices.
--local lee los local_*.json de una prueba de codigo: plan chico, nunca decide (los veredictos salen como LOCAL), y
es ciego: calcula curvas, descriptivos y estadisticos pero no los imprime.
Salida: 0 completo y valido; 3 control o plan fallido.
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

CELDAS = (2, 5)
TAUS = list(range(20, 30))
NS = (6, 12, 24, 48, 96, 192, 384, 768, 2400)
N_DIA = 96
REPS = 20
N_PROY = 10
B = 20000
SEM_BOOT = 2063
MARGEN = 0.01
ARTIFICIALES = ("CRUDO", "PCA_L", "PROY_L")


CIEGO = [False]


def pr(s):
    if CIEGO[0] and s.startswith(("CURVA", "DESCRIPTIVO", "ESTADISTICO")):
        return
    print(s, flush=True)


def cargar(d, local):
    pre = "local_" if local else ""
    mos = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(d, pre + "mosca_c*_t*.json")))]
    cru = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(d, pre + "crudo_c*.json")))]
    return mos, cru


def matriz(cur, ns, reps):
    """cur: n -> {acc: [...]}; devuelve (len(ns), reps); el n completo (una sola corrida) se repite."""
    M = np.zeros((len(ns), reps))
    for i, n in enumerate(ns):
        ac = cur[str(n)]["acc"]
        M[i] = ac if len(ac) == reps else ac[0]
    return M


def armar(mos, cru, celdas, ns, reps):
    X = {}
    for c in celdas:
        filas = sorted([f for m in mos if m["ci"] == c for f in m["filas"]], key=lambda f: f["tau"])
        cj = [j for j in cru if j["ci"] == c][0]
        X[c] = dict(
            taus=[f["tau"] for f in filas],
            FLY=np.stack([matriz(f["MOSCA_L"], ns, reps) for f in filas]),
            W=np.array([f["W"] for f in filas]),
            CRUDO=matriz(cj["brazos"]["CRUDO"], ns, reps),
            PCA_L=matriz(cj["brazos"]["PCA_L"], ns, reps),
            PROY_L=np.stack([matriz(b, ns, reps) for b in cj["brazos"]["PROY_L"]]),
            WN={str(n): [x for f in filas for x in f["W_n"].get(str(n), [])] for n in ns},
            pca=cj.get("pca"))
    return X


def medias(x, rr=None, tt=None, kk=None):
    """Curvas medias de cada brazo (por n) y W, con los indices sorteados o todos."""
    F, P = x["FLY"], x["PROY_L"]
    if tt is not None:
        F = F[tt]
    if kk is not None:
        P = P[kk]
    cr, pc = x["CRUDO"], x["PCA_L"]
    if rr is not None:
        F, P, cr, pc = F[:, :, rr], P[:, :, rr], cr[:, rr], pc[:, rr]
    w = x["W"] if tt is None else x["W"][tt]
    return dict(MOSCA_L=F.mean(axis=(0, 2)), PROY_L=P.mean(axis=(0, 2)), CRUDO=cr.mean(1), PCA_L=pc.mean(1)), float(w.mean())


def estadisticos(X, celdas, ib, nb, rr=None, tt=None, kk=None):
    """D_a sobre la curva baja (los primeros nb puntos) y E_a en el indice ib, promediados sobre las celdas."""
    d = {}
    for a in ARTIFICIALES:
        d["D_" + a] = 0.0
        d["E_" + a] = 0.0
    for c in celdas:
        m, w = medias(X[c], rr, tt, kk)
        for a in ARTIFICIALES:
            d["D_" + a] += float((m["MOSCA_L"][:nb] - m[a][:nb]).mean()) / len(celdas)
            d["E_" + a] += float(m[a][ib] - w) / len(celdas)
    return d


def bootstrap(X, celdas, ib, nb, b_total, semilla):
    rng = np.random.default_rng(semilla)
    x0 = X[celdas[0]]
    T, K, R = x0["FLY"].shape[0], x0["PROY_L"].shape[0], x0["CRUDO"].shape[1]
    out = None
    for b in range(b_total):
        rr = rng.integers(0, R, R)
        tt = rng.integers(0, T, T)
        kk = rng.integers(0, K, K)
        d = estadisticos(X, celdas, ib, nb, rr, tt, kk)
        if out is None:
            out = {k: np.zeros(b_total) for k in d}
        for k, v in d.items():
            out[k][b] = v
    return {k: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) for k, v in out.items()}


def decidir(ic):
    def piso(k):
        return ic[k][0]

    def techo(k):
        return ic[k][1]
    if piso("D_PCA_L") > MARGEN and piso("D_PROY_L") > MARGEN:
        emb = "SOSTENIDA"
    elif techo("D_PCA_L") < MARGEN or techo("D_PROY_L") < MARGEN:
        emb = "REFUTADA"
    else:
        emb = "SIN_DECIDIR"
    if piso("D_CRUDO") > MARGEN:
        cru = "SOSTENIDA"
    elif techo("D_CRUDO") < MARGEN:
        cru = "REFUTADA"
    else:
        cru = "SIN_DECIDIR"
    if all(techo("E_" + a) < -MARGEN for a in ARTIFICIALES):
        dia = "SOSTENIDA"
    elif any(piso("E_" + a) > -MARGEN for a in ARTIFICIALES):
        dia = "REFUTADA"
    else:
        dia = "SIN_DECIDIR"
    return dict(H_DATOS_EMBUDO=emb, H_DATOS_CRUDO=cru, H_DATOS_PRIMER_DIA=dia)


def n_alcanza(curva_media, w, ns):
    for n, v in zip(ns, curva_media):
        if v >= w - MARGEN:
            return int(n)
    return None


def chequeos(mos, cru, local):
    C = {}
    todos = mos + cru
    for j in todos:
        nom = "%s_c%d%s" % (j["modo"], j["ci"], ("_t%d" % j["taus"][0]) if j["modo"] == "mosca" else "")
        ok = all(v is not False and (local or v is not None) for v in j["controles"].values())
        pr("CONTROLES %s valido=%s %s" % (nom, j["valido"], " ".join(
            "%s=%s" % (k, "NO_APLICA" if v is None else v) for k, v in sorted(j["controles"].items()))))
        C["json_" + nom] = bool(ok and (local or j["valido"] is True) and j["humo"] is False)
    C["MISMO_SCRIPT"] = bool(len(set(j["md5_script"] for j in todos)) == 1)
    C["SUBCONJUNTOS"] = bool(len(set(json.dumps(j["subconjuntos_md5"], sort_keys=True) for j in todos)) == 1)
    if local:
        C["PLAN_COMPLETO"] = None
        C["REPRO_TAULIBRE"] = None
        C["REPRO_CRUDO"] = None
        return C
    plan = True
    for c in CELDAS:
        taus = sorted(f["tau"] for m in mos if m["ci"] == c for f in m["filas"])
        plan = plan and taus == TAUS and len([j for j in cru if j["ci"] == c]) == 1
    for j in todos:
        plan = plan and list(j["ns"]) == list(NS) and j["reps"] == REPS and j["ntr"] == 2400 and j["prueba"] == 12
        curvas = [f["MOSCA_L"] for f in j.get("filas", [])]
        if j["modo"] == "crudo":
            curvas = [j["brazos"]["CRUDO"], j["brazos"]["PCA_L"]] + list(j["brazos"]["PROY_L"])
            plan = plan and len(j["brazos"]["PROY_L"]) == N_PROY
        for cur in curvas:
            plan = plan and sorted(int(n) for n in cur) == list(NS)
            plan = plan and all(len(cur[str(n)]["acc"]) == (1 if n == 2400 else REPS) for n in NS)
    C["PLAN_COMPLETO"] = bool(plan and len(mos) == 10 and len(cru) == 2)
    rep = [f.get("repro_taulibre") is True for m in mos for f in m["filas"]]
    C["REPRO_TAULIBRE"] = bool(len(rep) == 20 and all(rep))
    C["REPRO_CRUDO"] = bool(len(cru) == 2 and all(j["controles"].get("REPRO_CRUDO") is True for j in cru))
    return C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--b", type=int, default=B)
    a = ap.parse_args()
    CIEGO[0] = bool(a.local)
    mos, cru = cargar(a.dir, a.local)
    pr("# H_PARES_DATOS agregado | json mosca=%d crudo=%d | local=%s" % (len(mos), len(cru), a.local))
    if not mos or not cru:
        pr("ABORTA: faltan json")
        pr("EXIT_RUN=3")
        return 3
    C = chequeos(mos, cru, a.local)
    valido = all(v is not False for v in C.values())
    pr("CHEQUEO %s -> %s" % (" ".join("%s=%s" % (k, "NO_APLICA" if v is None else v) for k, v in C.items()
                                       if not k.startswith("json_")) + " json_validos=%d/%d" % (
        sum(1 for k, v in C.items() if k.startswith("json_") and v), sum(1 for k in C if k.startswith("json_"))),
        "VALIDO" if valido else "INVALIDO"))
    ns = [int(n) for n in mos[0]["ns"]]
    reps = int(mos[0]["reps"])
    celdas = sorted(set(m["ci"] for m in mos) & set(j["ci"] for j in cru))
    baja = [n for n in ns if n < max(ns)]
    nb = len(baja)
    ib = baja.index(N_DIA) if N_DIA in baja else nb - 1
    X = armar(mos, cru, celdas, ns, reps)
    est = estadisticos(X, celdas, ib, nb)
    ic = bootstrap(X, celdas, ib, nb, a.b, SEM_BOOT)
    ver = decidir(ic)
    salida = dict(experimento="H_PARES_DATOS", local=bool(a.local), controles=C, valido=bool(valido), ns=ns,
                  reps=reps, celdas=celdas, curva_baja=baja, n_dia=ns[ib], estadisticos=est, ic=ic, celda={})
    for c in celdas:
        m, w = medias(X[c])
        x = X[c]
        filas = {}
        for i, n in enumerate(ns):
            fl = x["FLY"][:, i, :].mean(0)
            py = x["PROY_L"][:, i, :].mean(0)
            wn = [v for v in x["WN"].get(str(n), []) if v is not None]
            filas[str(n)] = dict(
                MOSCA_L=[float(fl.mean()), float(fl.min()), float(fl.max())],
                CRUDO=[float(x["CRUDO"][i].mean()), float(x["CRUDO"][i].min()), float(x["CRUDO"][i].max())],
                PCA_L=[float(x["PCA_L"][i].mean()), float(x["PCA_L"][i].min()), float(x["PCA_L"][i].max())],
                PROY_L=[float(py.mean()), float(py.min()), float(py.max())],
                W_n=[float(np.mean(wn)) if wn else None, len(wn), len(x["WN"].get(str(n), []))])
            pr("CURVA c%d n=%d MOSCA_L=%.4f [%.4f, %.4f] CRUDO=%.4f [%.4f, %.4f] PCA_L=%.4f [%.4f, %.4f] PROY_L=%.4f "
               "[%.4f, %.4f] W_n=%s (%d de %d) | W=%.4f" % (
                   c, n, *filas[str(n)]["MOSCA_L"], *filas[str(n)]["CRUDO"], *filas[str(n)]["PCA_L"],
                   *filas[str(n)]["PROY_L"], ("%.4f" % filas[str(n)]["W_n"][0]) if wn else "-", len(wn),
                   len(x["WN"].get(str(n), [])), w))
        alc = {k: n_alcanza(m[k], w, ns) for k in ("MOSCA_L",) + ARTIFICIALES}
        salida["celda"][str(c)] = dict(taus=x["taus"], W=[float(v) for v in x["W"]], W_media=w, filas=filas,
                                       n_alcanza=alc, pca=x["pca"])
        pr("DESCRIPTIVO c%d W por tau %s | media=%.4f" % (c, " ".join(
            "%d:%.4f" % (t, v) for t, v in zip(x["taus"], x["W"])), w))
        pr("DESCRIPTIVO c%d N_alcanza (media >= W - 0,01): %s" % (c, " ".join(
            "%s=%s" % (k, v if v is not None else "mas_de_%d" % max(ns)) for k, v in alc.items())))
        pr("DESCRIPTIVO c%d MOSCA_L menos W por n: %s" % (c, " ".join(
            "%d:%+.4f" % (n, m["MOSCA_L"][i] - w) for i, n in enumerate(ns))))
        if x["pca"]:
            pr("DESCRIPTIVO c%d PCA varianza de las %d componentes=%.4f" % (c, x["pca"]["componentes"],
                                                                         x["pca"]["varianza"]))
    if len(celdas) > 1:
        mm = [medias(X[c]) for c in celdas]
        wm = float(np.mean([w for _, w in mm]))
        alc = {k: n_alcanza(np.mean([m[k] for m, _ in mm], axis=0), wm, ns) for k in ("MOSCA_L",) + ARTIFICIALES}
        salida["n_alcanza_media"] = alc
        pr("DESCRIPTIVO media de celdas N_alcanza: %s | W=%.4f" % (" ".join(
            "%s=%s" % (k, v if v is not None else "mas_de_%d" % max(ns)) for k, v in alc.items()), wm))
    for k in sorted(est):
        pr("ESTADISTICO %s=%+.4f IC95=[%+.4f, %+.4f]" % (k, est[k], ic[k][0], ic[k][1]))
    if a.local:
        pr("LOCAL: curvas, descriptivos y estadisticos calculados para %d celda(s); no se imprimen" % len(celdas))
    if not valido:
        ver = {k: "INVALIDO" for k in ver}
    if a.local:
        ver = {k: "LOCAL" for k in ver}
    salida["veredictos"] = ver
    for k, v in ver.items():
        pr("VEREDICTO %s=%s" % (k, v))
    with open(os.path.join(a.dir, "agregado.json"), "w") as f:
        json.dump(salida, f)
    pr("escrito agregado.json")
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
