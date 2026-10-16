#!/usr/bin/env python3
"""H_MOSCA_ENTERA, brazos LIQ, TASA y PROX en el cerebro entero (respuestas 2026-10-14-047 y 049).

Sello: tools/mosca_entera/SELLO-MOSCA-ENTERA.md (500f66d, md5 55bc4c76657e35f341300d0e082c7ebe).
La celda es la de tools/factorial2/factorial2_mosca.py (md5 798a824cd47808155fa12adb9e652dac, rama
titan/lector-2026-10-15 en 8d305e9): z <- (1 - th) z + th tanh(u), th = min(1, (DT/tau)(1 + G_LIQ |u|)) con liq,
th = DT/tau sin liq; u = W z + entrada. La prueba (prueba_mosca_entera.py) exige que simular() de aca de lo mismo
que sim() de alla, que matriz() y tau_por_root() sean las mismas, y que los nulos conserven lo que dicen conservar.
Uso:
  real:  python3 liq_entera.py --conn C --comp K --annot A --out D --modo real [--taus 30,...,39] [--humo]
  nulos: python3 liq_entera.py --conn C --comp K --annot A --out D --modo nulos --tipo SHUF_W --k0 0 --n 10
  G1:    python3 liq_entera.py --conn C --comp K --annot A --out D --modo nulos_g1 --tipo SHUF_W --k0 0 --n 40
Enmienda 048 (tools/mosca_entera/ENMIENDA-048.md, 778dc10, md5 022dbbdd87ce206e9f33efc62d8e7ee7): el modo real
guarda ademas la latencia de cada neurona (latencias(), primer paso con z >= 0,5 r) y max|r_LIQ - r_TASA| por tau;
el modo nulos_g1 escala cada nulo con el factor del real (RHO / radio crudo del real, medido en el mismo trabajo).
simular() y matriz() no cambian.
"""
import argparse
import hashlib
import json
import os
import platform
import time

import numpy as np
import pandas as pd
import scipy
import scipy.sparse as sp
import scipy.sparse.linalg as sla

DT, RHO, G_LIQ = 0.02, 0.9, 1.0          # los de la 003 y el factorial 2, sin cambios
T_PASOS, VENTANA, AMPLITUD = 200, (150, 200), 1.0   # pasos 151 a 200 (indices 150 a 199)
TAUS = tuple(range(30, 40))              # semillas frescas de tau
TAU_NULOS = 30
SEMILLA_NULOS = 20261015
CODIGO = {"SHUF_W": 1, "SHUF_G": 2}
TOP_GUARDA = 5000                        # K_SANO exige K <= 5000
MD5 = {"conn": "3d802fd542b5d18570ba1ba0bb0abed9", "annot": "719904abad876c68ace1b5690c9b9b63"}
SUGAR = [720575940624963786, 720575940630233916, 720575940637568838, 720575940638202345, 720575940617000768,
         720575940630797113, 720575940632889389, 720575940621754367, 720575940621502051, 720575940640649691,
         720575940639332736, 720575940616885538, 720575940639198653, 720575940620900446, 720575940617937543,
         720575940632425919, 720575940633143833, 720575940612670570, 720575940628853239, 720575940629176663,
         720575940611875570]
FALTA_V783 = 720575940620900446
MN9 = 720575940660219265


def pr(s):
    print(s, flush=True)


def md5(ruta):
    h = hashlib.md5()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def leer_grafo(conn, comp):
    """Indices de Shiu: la posicion en Completeness_783.csv. Devuelve pre, post, w (Excitatory x Connectivity) e ids."""
    ids = pd.read_csv(comp, index_col=0).index.to_numpy(dtype=np.int64)
    df = pd.read_parquet(conn, columns=["Presynaptic_ID", "Postsynaptic_ID", "Presynaptic_Index",
                                        "Postsynaptic_Index", "Excitatory x Connectivity"])
    pre = df["Presynaptic_Index"].to_numpy(dtype=np.int64)
    post = df["Postsynaptic_Index"].to_numpy(dtype=np.int64)
    w = df["Excitatory x Connectivity"].to_numpy(dtype=np.float64)
    ok = bool((ids[pre] == df["Presynaptic_ID"].to_numpy()).all() and (ids[post] == df["Postsynaptic_ID"].to_numpy()).all())
    return pre, post, w, ids, ok


def nulo(pre, post, w, tipo, semilla):
    """SHUF_W: permuta los pesos entre aristas. SHUF_G: permuta el destino entre aristas (cada una con su peso)."""
    rng = np.random.default_rng([SEMILLA_NULOS, CODIGO[tipo], int(semilla)])
    if tipo == "SHUF_W":
        return pre, post, w[rng.permutation(len(w))]
    if tipo == "SHUF_G":
        return pre, post[rng.permutation(len(post))], w
    raise ValueError(tipo)


def matriz(n, pre, post, w):
    """La matriz() del factorial 2 con densa_ok=False: W[post, pre], duplicados sumados, radio espectral RHO."""
    W = sp.coo_matrix((w, (post, pre)), shape=(n, n)).tocsr()
    r = float(np.abs(sla.eigs(W, k=1, which="LM", return_eigenvectors=False, tol=1e-10, maxiter=100000)).max())
    return (W * (RHO / r)).tocsr(), r


def tau_por_root(ids, semilla):
    """La de factorial2_mosca.py, sin cambios."""
    return np.array([0.06 + 0.12 * np.random.default_rng([semilla, int(r)]).random() for r in ids])


def simular(W, tau, estim, liq, T=T_PASOS, A=AMPLITUD, ventana=VENTANA, registrar=None):
    """Misma cuenta que sim() del factorial 2 con un solo ensayo, entrada A constante en estim y sin ruido.
    Devuelve la media de z en la ventana y, si se pide, la trayectoria de las neuronas de registrar."""
    N = W.shape[0]
    t0 = DT / tau
    z = np.zeros(N)
    acum = np.zeros(N)
    tray = np.zeros((T, len(registrar))) if registrar is not None else None
    for t in range(T):
        u = W @ z
        u[estim] += A
        tt = np.minimum(1.0, t0 * (1.0 + G_LIQ * np.abs(u))) if liq else t0
        z = (1 - tt) * z + tt * np.tanh(u)
        if ventana[0] <= t < ventana[1]:
            acum += z
        if tray is not None:
            tray[t] = z[registrar]
    return acum / (ventana[1] - ventana[0]), tray


def latencias(W, tau, estim, liq, r, T=T_PASOS, A=AMPLITUD):
    """Enmienda 048, seccion 2: primer paso t (1 a T) en que z_t >= 0,5 r, para las neuronas con r > 0; 0 para las
    demas (sin latencia). Repite la cuenta de simular() paso a paso. Devuelve (lat, pendientes)."""
    N = W.shape[0]
    t0 = DT / tau
    z = np.zeros(N)
    lat = np.zeros(N, dtype=np.int16)
    umbral = 0.5 * r
    pend = r > 0
    for t in range(T):
        u = W @ z
        u[estim] += A
        tt = np.minimum(1.0, t0 * (1.0 + G_LIQ * np.abs(u))) if liq else t0
        z = (1 - tt) * z + tt * np.tanh(u)
        cruza = pend & (z >= umbral)
        lat[cruza] = t + 1
        pend &= ~cruza
    return lat, int(pend.sum())


def radio_crudo(W):
    """El mismo eigs de matriz(), sin escalar."""
    return float(np.abs(sla.eigs(W, k=1, which="LM", return_eigenvectors=False, tol=1e-10, maxiter=100000)).max())


def matriz_g1(n, pre, post, w, c):
    """Enmienda 048, seccion 3: el nulo con el factor c del real en vez del propio. Devuelve (W, radio crudo)."""
    Wc = sp.coo_matrix((w, (post, pre)), shape=(n, n)).tocsr()
    return (Wc * c).tocsr(), radio_crudo(Wc)


def prox(W, estim, kmax=4):
    """Rival sin dinamica: suma de k = 1 a kmax de 0,5^k (|W|^k e)."""
    A = abs(W)
    v = np.zeros(W.shape[0])
    v[estim] = 1.0
    s = np.zeros(W.shape[0])
    for k in range(1, kmax + 1):
        v = A @ v
        s += 0.5 ** k * v
    return s


def top_positivos(r, excluir, k=TOP_GUARDA):
    """Las k de mayor respuesta positiva, sin las excluidas; empates por indice."""
    m = r > 0
    m[excluir] = False
    cand = np.flatnonzero(m)
    orden = cand[np.argsort(-r[cand], kind="stable")]
    return orden[:k]


def indices(ids, lista):
    pos = {int(f): i for i, f in enumerate(ids)}
    return np.array([pos[f] for f in lista if f in pos], dtype=np.int64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--comp", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--modo", choices=("real", "nulos", "nulos_g1"), required=True)
    ap.add_argument("--tipo", choices=tuple(CODIGO))
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--taus", default=",".join(str(t) for t in TAUS))
    ap.add_argument("--humo", action="store_true", help="corrida corta: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    pr("== liq_entera.py :: H_MOSCA_ENTERA, brazos LIQ, TASA y PROX (2026-10-14-047) ==")
    pr("ENTORNO python=%s numpy=%s scipy=%s pandas=%s maquina=%s" % (platform.python_version(), np.__version__,
                                                                    scipy.__version__, pd.__version__,
                                                                    platform.node()))
    m = {"conn": md5(a.conn), "annot": md5(a.annot), "comp": md5(a.comp)}
    pin = m["conn"] == MD5["conn"] and m["annot"] == MD5["annot"]
    pr("PIN conn=%s annot=%s comp=%s -> %s" % (m["conn"], m["annot"], m["comp"], pin))
    if not pin:
        pr("ABORTA: pin de datos")
        raise SystemExit(3)
    pre, post, w, ids, ok = leer_grafo(a.conn, a.comp)
    n = len(ids)
    pr("GRAFO neuronas=%d aristas=%d sinapsis_abs=%d mapeo_ok=%s | %.1f s" % (n, len(w), int(np.abs(w).sum()), ok,
                                                                          time.time() - t_ini))
    if not ok:
        pr("ABORTA: mapeo indice -> id")
        raise SystemExit(3)
    estim = indices(ids, SUGAR)
    i_mn9 = int(indices(ids, [MN9])[0])
    pr("ESTIMULO azucar=%d de %d (falta %d en v783: %s) mn9_indice=%d" % (len(estim), len(SUGAR), FALTA_V783,
                                                                         FALTA_V783 not in set(ids.tolist()), i_mn9))
    res = {"version": "2026-10-14-049", "humo": a.humo, "modo": a.modo, "md5": m, "n": n, "aristas": len(w),
           "estim": estim.tolist(), "mn9": i_mn9, "T": T_PASOS, "ventana": list(VENTANA), "amplitud": AMPLITUD}
    tops = {}
    lats = {}
    if a.modo == "real":
        t1 = time.time()
        W, radio = matriz(n, pre, post, w)
        pr("RADIO crudo=%.6f -> %.2f | %.1f s" % (radio, RHO, time.time() - t1))
        res["radio_crudo"] = radio
        s = prox(W, estim)
        tops["PROX"] = top_positivos(s, estim)
        res["PROX"] = {"mn9": float(s[i_mn9]), "positivos": int((s > 0).sum() - (s[estim] > 0).sum())}
        pr("PROX mn9=%.6g positivos=%d" % (s[i_mn9], res["PROX"]["positivos"]))
        taus = [int(x) for x in a.taus.split(",")]
        res["LIQ"], res["TASA"] = {}, {}
        for st in taus:
            tau = tau_por_root(ids, st)
            rs = {}
            for brazo, liq in (("LIQ", True), ("TASA", False)):
                t1 = time.time()
                r, _ = simular(W, tau, estim, liq)
                rs[brazo] = r
                tops["%s_%d" % (brazo, st)] = top_positivos(r, estim)
                lat, pend = latencias(W, tau, estim, liq, r)
                lats["%s_%d" % (brazo, st)] = lat
                pos = int((r > 0).sum() - (r[estim] > 0).sum())
                res[brazo][str(st)] = {"mn9": float(r[i_mn9]), "positivos": pos, "max": float(r.max()),
                                       "min": float(r.min()), "lat_mn9": int(lat[i_mn9]), "lat_pendientes": pend}
                pr("%s tau=%d mn9=%.6g positivos=%d max=%.4g min=%.4g lat_mn9=%d lat_pendientes=%d | %.1f s" % (
                    brazo, st, r[i_mn9], pos, r.max(), r.min(), lat[i_mn9], pend, time.time() - t1))
            dif = float(np.abs(rs["LIQ"] - rs["TASA"]).max())
            res["LIQ"][str(st)]["dif_max_liq_tasa"] = dif
            pr("DIF tau=%d max|r_LIQ - r_TASA|=%.3g" % (st, dif))
        nombre = "liq_real"
    elif a.modo == "nulos_g1":
        t1 = time.time()
        Wr = sp.coo_matrix((w, (post, pre)), shape=(n, n)).tocsr()
        radio_real = radio_crudo(Wr)
        c = RHO / radio_real
        del Wr
        pr("G1 radio_crudo_real=%.6f factor=%.6g | %.1f s" % (radio_real, c, time.time() - t1))
        tau = tau_por_root(ids, TAU_NULOS)
        res.update({"tipo": a.tipo, "k0": a.k0, "nulos": {}, "radio_crudo_real": radio_real, "factor": c})
        for k in range(a.k0, a.k0 + a.n):
            t1 = time.time()
            p2, q2, w2 = nulo(pre, post, w, a.tipo, k)
            W, r_nulo = matriz_g1(n, p2, q2, w2, c)
            r, _ = simular(W, tau, estim, True)
            tops["G1_%s_%d" % (a.tipo, k)] = top_positivos(r, estim)
            res["nulos"][str(k)] = {"mn9": float(r[i_mn9]), "radio_crudo": r_nulo, "radio_g1": c * r_nulo,
                                    "positivos": int((r > 0).sum() - (r[estim] > 0).sum())}
            pr("NULO_G1 %s k=%d radio_crudo=%.6f radio_g1=%.4f mn9=%.6g positivos=%d | %.1f s" % (
                a.tipo, k, r_nulo, c * r_nulo, r[i_mn9], res["nulos"][str(k)]["positivos"], time.time() - t1))
        nombre = "liq_G1_%s_k%03d" % (a.tipo, a.k0)
    else:
        tau = tau_por_root(ids, TAU_NULOS)
        res.update({"tipo": a.tipo, "k0": a.k0, "nulos": {}})
        for k in range(a.k0, a.k0 + a.n):
            t1 = time.time()
            p2, q2, w2 = nulo(pre, post, w, a.tipo, k)
            W, radio = matriz(n, p2, q2, w2)
            r, _ = simular(W, tau, estim, True)
            tops["%s_%d" % (a.tipo, k)] = top_positivos(r, estim)
            res["nulos"][str(k)] = {"mn9": float(r[i_mn9]), "radio_crudo": radio,
                                    "positivos": int((r > 0).sum() - (r[estim] > 0).sum())}
            pr("NULO %s k=%d radio=%.6f mn9=%.6g positivos=%d | %.1f s" % (a.tipo, k, radio, r[i_mn9],
                                                                         res["nulos"][str(k)]["positivos"],
                                                                         time.time() - t1))
        nombre = "liq_%s_k%03d" % (a.tipo, a.k0)
    np.savez_compressed(os.path.join(a.out, nombre + "_top.npz"), **{k: v.astype(np.int64) for k, v in tops.items()})
    if lats:
        np.savez_compressed(os.path.join(a.out, nombre + "_lat.npz"), **lats)
    res["segundos"] = time.time() - t_ini
    with open(os.path.join(a.out, nombre + ".json"), "w") as f:
        json.dump(res, f, indent=1)
    pr("JSON %s md5=%s" % (nombre + ".json", md5(os.path.join(a.out, nombre + ".json"))))
    pr("FIN segundos=%.1f" % res["segundos"])


if __name__ == "__main__":
    main()
