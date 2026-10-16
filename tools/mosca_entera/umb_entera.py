#!/usr/bin/env python3
"""H_ENTERA_UMBRAL, brazo UMB en el cerebro entero (respuesta 2026-10-14-051).

Sello: tools/mosca_entera/SELLO-UMBRAL-050.md (868ded6, md5 680abca839bd6c80367c9b434af7d800).
Dinamica: z <- (1 - t) z + t tanh(max(0, W z + x - theta)), t = DT / tau. Es la TASA de la 049 (simular() de
liq_entera.py sin liq) con la activacion cortada por un umbral global theta.
Calibracion, la misma para cada grafo (seccion 3 del sello): Activas(theta) = no estimuladas con r > 0 en la
ventana. Si Activas(0) <= N_OBJ, theta = 0 (NO_ALCANZA). Si no, hi = 1 duplicado hasta 8 mientras
Activas(hi) > N_OBJ; biseccion de 24 pasos entre 0 y hi; theta = el mas chico probado con Activas <= N_OBJ.
Estado: OK si |Activas - N_OBJ| <= TOL, FUERA si no, NO_BAJA si ni con 8 baja de N_OBJ.
Real: la matriz de la 049 a radio 0,9, mas el control TASA_049 (TASA con tau 30 contra la S_LIF de la 049).
Nulos: los mismos SHUF_W y SHUF_G de la 049 (nulo() de liq_entera.py) con el factor del real (matriz_g1()),
mas la lectura secundaria con el theta del real fijo.
Humo: el real usa otro estimulo (20 neuronas no sensoriales al azar, semilla 99); los nulos usan el azucar.
Uso:
  real:  python3 umb_entera.py --conn C --comp K --annot A --lif L --out D --modo real [--humo]
  nulos: python3 umb_entera.py --conn C --comp K --annot A --lif L --out D --modo nulos --tipo SHUF_W --k0 0 --n 10
         --real-json R [--humo]
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd
import scipy
import scipy.sparse as sp

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import liq_entera as le  # noqa: E402

N_OBJ, TOL, PASOS, HI_MAX = 321, 32, 24, 8.0
TAU_UMB = 30
MD5_LIF = "f6383d18a0e05efb65696175949df9fa"
SEMILLA_HUMO, N_HUMO = 99, 20
SENSORIALES = ("sensory", "sensory_ascending")


def pr(s):
    print(s, flush=True)


def simular_umb(W, tau, estim, theta, T=le.T_PASOS, A=le.AMPLITUD, ventana=le.VENTANA):
    """TASA de la 049 con tanh(max(0, u - theta)). Devuelve la media de z en la ventana."""
    N = W.shape[0]
    t0 = le.DT / tau
    z = np.zeros(N)
    acum = np.zeros(N)
    for t in range(T):
        u = W @ z
        u[estim] += A
        z = (1 - t0) * z + t0 * np.tanh(np.maximum(0.0, u - theta))
        if ventana[0] <= t < ventana[1]:
            acum += z
    return acum / (ventana[1] - ventana[0])


def activas(r, estim):
    m = r > 0
    m[estim] = False
    return int(m.sum())


def calibrar(W, tau, estim, objetivo=N_OBJ, pasos=PASOS, hi_max=HI_MAX, tol=TOL, sim=None):
    """Seccion 3 del sello. Devuelve dict con theta, activas, estado, r y los probados en orden."""
    sim = sim or simular_umb
    probados = []
    guardado = {}

    def ev(th):
        r = sim(W, tau, estim, th)
        a = activas(r, estim)
        probados.append((float(th), a))
        guardado[float(th)] = r
        return a

    if ev(0.0) <= objetivo:
        estado = "NO_ALCANZA"
    else:
        hi = 1.0
        while ev(hi) > objetivo and hi < hi_max:
            hi *= 2.0
        if probados[-1][1] > objetivo:
            estado = "NO_BAJA"
        else:
            lo = 0.0
            for _ in range(pasos):
                mid = 0.5 * (lo + hi)
                if ev(mid) > objetivo:
                    lo = mid
                else:
                    hi = mid
            estado = None
    validos = [th for th, a in probados if a <= objetivo]
    theta = min(validos) if validos else max(th for th, _ in probados)
    a = dict(probados)[theta]
    if estado is None:
        estado = "OK" if abs(a - objetivo) <= tol else "FUERA"
    return {"theta": theta, "activas": a, "estado": estado, "r": guardado[theta], "probados": probados}


def estimulo_humo(ids, annot, semilla=SEMILLA_HUMO, n=N_HUMO):
    """20 neuronas no sensoriales al azar (super_class fuera de SENSORIALES), sin azucar ni MN9."""
    d = pd.read_csv(annot, sep=chr(9), usecols=["root_id", "super_class"], dtype={"root_id": np.int64},
                    low_memory=False)
    sens = set(d.loc[d["super_class"].astype(str).isin(SENSORIALES), "root_id"].tolist())
    anot = set(d["root_id"].tolist())
    excl = set(le.SUGAR) | {le.MN9}
    cand = np.array([i for i, f in enumerate(ids) if int(f) in anot and int(f) not in sens and int(f) not in excl],
                    dtype=np.int64)
    rng = np.random.default_rng(semilla)
    return np.sort(rng.choice(cand, n, replace=False))


def s_lif(ruta):
    """S_LIF de la 049 (lif_real.json de CORRER), con su pin."""
    m = le.md5(ruta)
    real = json.load(open(ruta))["corridas"]["real"]
    return np.array(real["S_LIF_idx"], dtype=np.int64), m


def jaccard(a, b):
    a, b = set(int(x) for x in a), set(int(x) for x in b)
    return len(a & b) / len(a | b) if (a or b) else float("nan")


def rango(r, i, estim):
    """Puesto de i entre las no estimuladas por r descendente (1 = la mayor); 0 si r_i <= 0."""
    if not r[i] > 0:
        return 0
    m = r > r[i]
    m[estim] = False
    return int(m.sum()) + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--comp", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--lif", required=True, help="lif_real.json de CORRER de la 049")
    ap.add_argument("--out", required=True)
    ap.add_argument("--modo", choices=("real", "nulos"), required=True)
    ap.add_argument("--tipo", choices=tuple(le.CODIGO))
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--real-json", default="")
    ap.add_argument("--humo", action="store_true", help="numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    pr("== umb_entera.py :: H_ENTERA_UMBRAL, brazo UMB (2026-10-14-051)%s ==" % (" HUMO" if a.humo else ""))
    pr("ENTORNO python=%s numpy=%s scipy=%s pandas=%s maquina=%s" % (platform.python_version(), np.__version__,
                                                                    scipy.__version__, pd.__version__,
                                                                    platform.node()))
    m = {"conn": le.md5(a.conn), "annot": le.md5(a.annot), "comp": le.md5(a.comp)}
    slif, m["lif"] = s_lif(a.lif)
    pin = m["conn"] == le.MD5["conn"] and m["annot"] == le.MD5["annot"] and m["lif"] == MD5_LIF
    pr("PIN conn=%s annot=%s comp=%s lif=%s -> %s" % (m["conn"], m["annot"], m["comp"], m["lif"], pin))
    if not pin:
        pr("ABORTA: pin de datos")
        raise SystemExit(3)
    pre, post, w, ids, ok = le.leer_grafo(a.conn, a.comp)
    n = len(ids)
    pr("GRAFO neuronas=%d aristas=%d mapeo_ok=%s | %.1f s" % (n, len(w), ok, time.time() - t_ini))
    if not ok:
        pr("ABORTA: mapeo indice -> id")
        raise SystemExit(3)
    estim = le.indices(ids, le.SUGAR)
    i_mn9 = int(le.indices(ids, [le.MN9])[0])
    tau = le.tau_por_root(ids, TAU_UMB)
    K = len(slif)
    pr("ESTIMULO azucar=%d mn9_indice=%d K=%d N_OBJ=%d" % (len(estim), i_mn9, K, N_OBJ))
    res = {"version": "2026-10-14-051", "humo": a.humo, "modo": a.modo, "md5": m, "n": n, "aristas": len(w),
           "mn9": i_mn9, "K": K, "N_OBJ": N_OBJ, "TOL": TOL, "tau": TAU_UMB}
    tops = {}
    if a.modo == "real":
        t1 = time.time()
        W, radio = le.matriz(n, pre, post, w)
        pr("RADIO crudo=%.6f -> %.2f | %.1f s" % (radio, le.RHO, time.time() - t1))
        e_umb = estimulo_humo(ids, a.annot) if a.humo else estim
        t1 = time.time()
        cal = calibrar(W, tau, e_umb)
        r = cal["r"]
        tops["UMB"] = le.top_positivos(r, e_umb)
        j_umb = jaccard(tops["UMB"][:K], slif)
        pr("CALIB theta=%.9g activas=%d estado=%s probados=%d | %.1f s" % (cal["theta"], cal["activas"], cal["estado"],
                                                                       len(cal["probados"]), time.time() - t1))
        pr("UMB mn9=%.6g rango_mn9=%d J=%.6f" % (r[i_mn9], rango(r, i_mn9, e_umb), j_umb))
        t1 = time.time()
        r_tasa, _ = le.simular(W, tau, estim, False)
        tops["TASA"] = le.top_positivos(r_tasa, estim)
        j_tasa = jaccard(tops["TASA"][:K], slif)
        pr("CONTROL TASA_049 J=%.10f mn9=%.6g | %.1f s" % (j_tasa, r_tasa[i_mn9], time.time() - t1))
        res.update({"radio_crudo": radio, "estim_umb": e_umb.tolist(), "theta": cal["theta"],
                    "activas": cal["activas"], "estado": cal["estado"], "probados": cal["probados"],
                    "mn9_umb": float(r[i_mn9]), "rango_mn9": rango(r, i_mn9, e_umb), "J_umb": j_umb,
                    "J_tasa": j_tasa, "mn9_tasa": float(r_tasa[i_mn9])})
        nombre = "umb_real"
    else:
        real = json.load(open(a.real_json))
        theta_real = float(real["theta"])
        t1 = time.time()
        Wr = sp.coo_matrix((w, (post, pre)), shape=(n, n)).tocsr()
        radio_real = le.radio_crudo(Wr)
        c = le.RHO / radio_real
        del Wr
        pr("G1 radio_crudo_real=%.6f factor=%.6g theta_real=%.9g | %.1f s" % (radio_real, c, theta_real,
                                                                           time.time() - t1))
        res.update({"tipo": a.tipo, "k0": a.k0, "nulos": {}, "radio_crudo_real": radio_real, "factor": c,
                    "theta_real": theta_real, "real_humo": real.get("humo")})
        for k in range(a.k0, a.k0 + a.n):
            t1 = time.time()
            p2, q2, w2 = le.nulo(pre, post, w, a.tipo, k)
            Wn, r_nulo = le.matriz_g1(n, p2, q2, w2, c)
            cal = calibrar(Wn, tau, estim)
            r = cal["r"]
            r_fijo = simular_umb(Wn, tau, estim, theta_real)
            tops["%s_%d" % (a.tipo, k)] = le.top_positivos(r, estim)
            res["nulos"][str(k)] = {"mn9": float(r[i_mn9]), "theta": cal["theta"], "activas": cal["activas"],
                                    "estado": cal["estado"], "probados": len(cal["probados"]),
                                    "radio_crudo": r_nulo, "radio_g1": c * r_nulo,
                                    "mn9_fijo": float(r_fijo[i_mn9]), "activas_fijo": activas(r_fijo, estim)}
            pr("NULO %s k=%d theta=%.9g activas=%d estado=%s mn9=%.6g | fijo: mn9=%.6g activas=%d | %.1f s" % (
                a.tipo, k, cal["theta"], cal["activas"], cal["estado"], r[i_mn9], r_fijo[i_mn9],
                activas(r_fijo, estim), time.time() - t1))
        nombre = "umb_%s_k%03d" % (a.tipo, a.k0)
    np.savez_compressed(os.path.join(a.out, nombre + "_top.npz"), **{k: v.astype(np.int64) for k, v in tops.items()})
    res["segundos"] = time.time() - t_ini
    with open(os.path.join(a.out, nombre + ".json"), "w") as f:
        json.dump(res, f, indent=1)
    pr("JSON %s md5=%s" % (nombre + ".json", le.md5(os.path.join(a.out, nombre + ".json"))))
    pr("FIN segundos=%.1f" % res["segundos"])


if __name__ == "__main__":
    main()
