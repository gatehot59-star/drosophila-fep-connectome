#!/usr/bin/env python3
"""Agregador del factorial 4 de la mosca: el cerebro entero (CE) con 10 x 10 semillas y sus barajados, contra su
regla y contra R2 del factorial 3 (respuesta 2026-10-13-015). Sellado antes de correr.

Uso: python3 agregar_factorial4.py <carpeta del factorial 4> <carpeta del factorial 3> [--humo]
La carpeta del factorial 4 tiene una subcarpeta por kernel de Kaggle con lo que bajo `kaggle kernels output`.

Es el diseno de agregar_factorial3.py (sellado en 6a7b4cb) con el sujeto CE (138.639 neuronas, 15.091.983 aristas).
Primaria (CE_CON_TASA, una sola configuracion):
  d = acierto de W menos acierto de la regla propia (las 564 entradas sintonizadas, las mismas de R2), por semilla de
  tau (0..9), prueba (2..11) y celda (6). Media; bootstrap de dos vias (tau y prueba por separado), B = 20.000,
  semilla 2026, percentiles 0,05 y 0,95; margen M = 0,01; los veredictos del factorial 3 (SUPERA, PIERDE,
  EQUIVALENTE, NO_INFERIOR, NO_SUPERIOR, INDETERMINADO). Por celda, descriptivo, con 0,05/6.
Escala (secundaria, pareada con el factorial 3):
  e = acierto de W en CE menos acierto de W en R2 en la misma semilla de tau, prueba y celda (los mismos ensayos y la
  misma regla). Mismo bootstrap con semilla 2027 y mismos veredictos.
Nulos (secundaria confirmatoria): en la celda 0,3|0,15, tau 0, prueba 2, W de la grilla contra 50 SL y 50 T;
  p = (1 + #nulos >= W) / (N + 1); Holm sobre los dos.
Hipotesis pre-registradas:
  H_SUPERA_CE   "el cerebro entero le gana a su regla por mas de un punto": SOSTENIDA si SUPERA; REFUTADA si
                hi < +M (EQUIVALENTE, NO_SUPERIOR o PIERDE); SIN_DECIDIR si no.
  H_ESCALA      "pasar de R2 al cerebro entero suma mas de un punto": SOSTENIDA si SUPERA; REFUTADA si hi < +M
                (si ademas PIERDE, el cerebro entero resta); SIN_DECIDIR si no.
  H_CABLEADO_CE "lo que paga es el cableado real": SOSTENIDA si los dos p de Holm son < 0,05; si no, NO SOSTENIDA.
Controles (VALIDO exige todos): json validos y sin humo; RECIBOS (rc 0, HEAD = SHA sellado, md5 del instrumento OK,
  insumos con el pin); INTEGRIDAD (cada json con el md5 que anoto su recibo, ninguno huerfano); PLAN_GRILLA (600) y
  PLAN_NULOS (50 + 50, k sin repetir); TAU_DN_IGUAL; REPRO_R2 en los 4 carriles (0,9465 +- 0,001); REAL_IGUAL;
  REPRODUCE_PRIMARIA_F3 (este codigo sobre los json del factorial 3 da +0,0085 [+0,0008; +0,0151]).
  Para la escala, ademas: REGLA_IGUAL_F3 (la regla propia de CE da exactamente las mismas predicciones que la de R2 en
  las 60 combinaciones de prueba y celda), TAU_DN_IGUAL_F3 y DN_IGUAL_F3; si alguno falla, H_ESCALA es NO_EVALUABLE.
"""
import glob
import hashlib
import json
import os
import sys

import numpy as np

M, B = 0.01, 20000
TAUS, PRUEBAS = list(range(10)), list(range(2, 12))
CELDAS = ["0.0|0.15", "0.0|0.45", "0.3|0.15", "0.3|0.45", "0.6|0.15", "0.6|0.45"]
CELDA_NULOS, TAU_N, PRUEBA_N, N_NULOS = "0.3|0.15", 0, 2, 50
SHA = "ace8fe78093a9109c20235746d867f2b168290d2"
PIN = {"connectivity.parquet": "3d802fd542b5d18570ba1ba0bb0abed9", "annotations.tsv": "719904abad876c68ace1b5690c9b9b63"}
R2_REF, N_REPRO = 0.9465, 4
F3_PRIMARIA = ("+0.0085", "+0.0008", "+0.0151")


def pr(s):
    print(s, flush=True)


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def bootstrap(D, alfa, rng):
    nt, npb = D.shape
    bs = np.empty(B)
    for b in range(B):
        bs[b] = D[np.ix_(rng.integers(0, nt, nt), rng.integers(0, npb, npb))].mean()
    return float(D.mean()), float(np.quantile(bs, alfa)), float(np.quantile(bs, 1 - alfa))


def veredicto(lo, hi):
    if lo > M:
        return "SUPERA"
    if hi < -M:
        return "PIERDE"
    if lo > -M and hi < M:
        return "EQUIVALENTE"
    if lo > -M:
        return "NO_INFERIOR"
    if hi < M:
        return "NO_SUPERIOR"
    return "INDETERMINADO"


def hipotesis(ver):
    if ver == "SUPERA":
        return "SOSTENIDA"
    if ver in ("EQUIVALENTE", "NO_SUPERIOR", "PIERDE"):
        return "REFUTADA"
    if ver == "NO_EVALUABLE":
        return "NO_EVALUABLE"
    return "SIN_DECIDIR"


def leer(carpeta, patron):
    out = []
    for ruta in sorted(glob.glob(os.path.join(carpeta, "**", patron), recursive=True)):
        with open(ruta) as f:
            out.append((os.path.normpath(ruta), json.load(f)))
    return out


def tablas(grilla):
    W, RP, PRP, taudn, dns = {}, {}, {}, {}, set()
    for n, r in grilla:
        dns.add(tuple(r["dns_root"]))
        for st, v in r["tau_DN"].items():
            taudn.setdefault(st, set()).add(tuple(v))
        for x in r["corridas"]:
            W[(x["tau"], x["prueba"], x["celda"])] = x["W"]
            RP[(x["prueba"], x["celda"])] = x["regla_propia"]
        for x in r.get("reglas", []):
            PRP[(x["prueba"], x["celda"])] = x["pred_regla_propia"]
    return W, RP, PRP, taudn, dns


def cubo(f, taus, pruebas, celdas):
    return np.array([[[f(t, p, c) for c in celdas] for p in pruebas] for t in taus])


def main():
    d4, d3 = sys.argv[1], sys.argv[2]
    humo = "--humo" in sys.argv
    g4 = leer(d4, "factorial4_CE_CON_TASA_*.json")
    nulos = leer(d4, "nulos_CE_*.json")
    vers = leer(d4, "verificar_CE*.json")
    recibos = leer(d4, "recibo_*.json")
    g3 = leer(d3, "factorial2_R2_CON_TASA_*.json")
    todos = g4 + nulos + vers
    validos = bool(g4) and all(r["valido"] for n, r in todos)
    sin_humo = all(r.get("humo", True) is False for n, r in todos)
    pr("JSON grilla=%d nulos=%d verificar=%d recibos=%d validos=%s sin_humo=%s | factorial 3 grilla=%d" % (
        len(g4), len(nulos), len(vers), len(recibos), validos, sin_humo, len(g3)))
    rec_ok, cubiertos, n_ok, n_tot = bool(recibos), set(), 0, 0
    for ruta, r in recibos:
        e = r["etapas"]
        ins = all(e.get("md5_" + k) == v for k, v in PIN.items())
        bien = r.get("rc") == 0 and e.get("head") == SHA and e.get("md5_instrumento") == "OK" and ins
        rec_ok = rec_ok and bien
        pr("RECIBO %s rc=%s head=%s instrumento=%s insumos=%s n_gpu=%s duracion_s=%s -> %s" % (
            r["kernel"], r.get("rc"), str(e.get("head"))[:7], e.get("md5_instrumento"), ins, e.get("n_gpu"),
            r.get("duracion_s"), bien))
        for c in r["corridas"]:
            for a, m in c.get("salidas_md5", {}).items():
                p = os.path.normpath(os.path.join(os.path.dirname(ruta), c["etiqueta"], a))
                n_tot += 1
                if os.path.exists(p) and md5(p) == m:
                    n_ok += 1
                    cubiertos.add(p)
    huerfanos = [n for n, r in todos if n not in cubiertos]
    integ = n_tot > 0 and n_ok == n_tot and not huerfanos
    pr("CHEQUEO RECIBOS -> %s" % rec_ok)
    pr("CHEQUEO INTEGRIDAD archivos_con_md5=%d/%d huerfanos=%d -> %s" % (n_ok, n_tot, len(huerfanos), integ))
    W4, RP4, PRP4, taudn4, dns4 = tablas(g4)
    W3, RP3, PRP3, taudn3, dns3 = tablas(g3)
    tau_ok = all(len(v) == 1 for v in taudn4.values())
    pr("CHEQUEO TAU_DN_IGUAL semillas=%d -> %s" % (len(taudn4), tau_ok))
    taus, pruebas, celdas = TAUS, PRUEBAS, CELDAS
    if humo:
        taus, pruebas = sorted(set(k[0] for k in W4)), sorted(set(k[1] for k in W4))
        celdas = [c for c in CELDAS if c in set(k[2] for k in W4)]
    falt = [(t, p, c) for t in taus for p in pruebas for c in celdas if (t, p, c) not in W4]
    pr("CHEQUEO PLAN_GRILLA corridas=%d faltan=%d" % (len(W4), len(falt)))
    repros = [r["info"]["repro_r2"] for n, r in g4 + vers if "repro_r2" in r.get("info", {})]
    repro_ok = all(abs(x - R2_REF) <= 0.001 + 1e-9 for x in repros) and len(repros) == N_REPRO
    pr("CHEQUEO REPRO_R2 trabajos=%d valores=%s -> %s" % (len(repros), repros, repro_ok))
    acc, reales, dup = {"SL": {}, "T": {}}, [], 0
    for n, r in nulos:
        for x in r["nulos"]:
            dup += x["k"] in acc[r["tipo"]]
            acc[r["tipo"]][x["k"]] = x["acierto"]
        if r["real"] is not None:
            reales.append(r["real"])
    W0 = W4.get((TAU_N, PRUEBA_N, CELDA_NULOS))
    real_ok = W0 is not None and bool(reales) and all(abs(x - W0) <= 0.001 + 1e-9 for x in reales)
    pr("CHEQUEO REAL_IGUAL grilla=%s script_de_nulos=%s -> %s" % (W0, reales, real_ok))
    n_ok_nulos = (all(len(acc[t]) == N_NULOS for t in acc) and dup == 0) or humo
    pr("CHEQUEO PLAN_NULOS SL=%d T=%d repetidos=%d -> %s" % (len(acc["SL"]), len(acc["T"]), dup, n_ok_nulos))
    falt3 = [(t, p, c) for t in TAUS for p in PRUEBAS for c in CELDAS if (t, p, c) not in W3]
    rep3 = False
    if not falt3:
        D3 = cubo(lambda t, p, c: W3[(t, p, c)] - RP3[(p, c)], TAUS, PRUEBAS, CELDAS)
        e3, l3, h3 = bootstrap(D3.mean(2), 0.05, np.random.default_rng(2026))
        rep3 = ("%+.4f" % e3, "%+.4f" % l3, "%+.4f" % h3) == F3_PRIMARIA
        pr("CHEQUEO REPRODUCE_PRIMARIA_F3 dif=%+.4f IC90=[%+.4f, %+.4f] -> %s" % (e3, l3, h3, rep3))
    else:
        pr("CHEQUEO REPRODUCE_PRIMARIA_F3 faltan=%d -> False" % len(falt3))
    valido = (validos and rec_ok and integ and tau_ok and not falt and n_ok_nulos and rep3 and
              (humo or (sin_humo and repro_ok and real_ok)))
    if humo:
        pr("# HUMO: plan completo, REPRO_R2 en 4 carriles, REAL_IGUAL y sin_humo no se exigen; numeros sin valor")
    rng = np.random.default_rng(2026)
    if falt:
        ver = "NO_EVALUABLE"
        pr("PRIMARIA CE_CON_TASA -> NO_EVALUABLE")
    else:
        D = cubo(lambda t, p, c: W4[(t, p, c)] - RP4[(p, c)], taus, pruebas, celdas)
        mw = float(np.mean(cubo(lambda t, p, c: W4[(t, p, c)], taus, pruebas, celdas)))
        mr = float(np.mean(cubo(lambda t, p, c: RP4[(p, c)], taus, pruebas, celdas)))
        est, lo, hi = bootstrap(D.mean(2), 0.05, rng)
        ver = veredicto(lo, hi)
        pr("PRIMARIA CE_CON_TASA W=%.4f regla_propia=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] corridas=%d -> %s" % (
            mw, mr, est, lo, hi, D.size, ver))
        for j, c in enumerate(celdas):
            e2, l2, h2 = bootstrap(D[:, :, j], 0.05 / 6, rng)
            pr("  CELDA %s dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (c, e2, l2, h2, veredicto(l2, h2)))
    comb = sorted(PRP4)
    iguales = sum(1 for k in comb if k in PRP3 and PRP3[k] == PRP4[k] and RP3.get(k) == RP4.get(k))
    regla_ok = bool(comb) and iguales == len(comb) and (len(comb) == len(PRUEBAS) * len(CELDAS) or humo)
    tau3_ok = bool(taudn4) and all(taudn3.get(st) == v for st, v in taudn4.items())
    dn3_ok = len(dns4) == 1 and dns4 == dns3
    pr("CHEQUEO REGLA_IGUAL_F3 combinaciones=%d iguales=%d -> %s" % (len(comb), iguales, regla_ok))
    pr("CHEQUEO TAU_DN_IGUAL_F3 -> %s" % tau3_ok)
    pr("CHEQUEO DN_IGUAL_F3 -> %s" % dn3_ok)
    falt_e = [(t, p, c) for t in taus for p in pruebas for c in celdas if (t, p, c) not in W3]
    if falt or falt_e or not (regla_ok and tau3_ok and dn3_ok):
        ver_e = "NO_EVALUABLE"
        pr("ESCALA CE_menos_R2 -> NO_EVALUABLE")
    else:
        E = cubo(lambda t, p, c: W4[(t, p, c)] - W3[(t, p, c)], taus, pruebas, celdas)
        m4 = float(np.mean(cubo(lambda t, p, c: W4[(t, p, c)], taus, pruebas, celdas)))
        m3 = float(np.mean(cubo(lambda t, p, c: W3[(t, p, c)], taus, pruebas, celdas)))
        rng_e = np.random.default_rng(2027)
        est_e, lo_e, hi_e = bootstrap(E.mean(2), 0.05, rng_e)
        ver_e = veredicto(lo_e, hi_e)
        pr("ESCALA CE_menos_R2 W_CE=%.4f W_R2=%.4f dif=%+.4f IC90=[%+.4f, %+.4f] corridas=%d -> %s" % (
            m4, m3, est_e, lo_e, hi_e, E.size, ver_e))
        for j, c in enumerate(celdas):
            e2, l2, h2 = bootstrap(E[:, :, j], 0.05 / 6, rng_e)
            pr("  CELDA %s dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (c, e2, l2, h2, veredicto(l2, h2)))
        pr("ESCALA corridas CE>R2=%d iguales=%d CE<R2=%d" % (int((E > 0).sum()), int((E == 0).sum()), int((E < 0).sum())))
    ps = {}
    for t in ("SL", "T"):
        v = np.array(list(acc[t].values()))
        if W0 is None or not len(v):
            ps[t] = 1.0
            pr("NULOS %s -> NO_EVALUABLE" % t)
            continue
        ps[t] = (1 + int((v >= W0).sum())) / (len(v) + 1)
        pr("NULOS %s n=%d media=%.4f max=%.4f W=%.4f iguales_o_mejores=%d p_sup=%.4f" % (
            t, len(v), v.mean(), v.max(), W0, int((v >= W0).sum()), ps[t]))
    orden = sorted(ps, key=ps.get)
    adj, prev = {}, 0.0
    for i, t in enumerate(orden):
        prev = max(prev, min(1.0, ps[t] * (len(orden) - i)))
        adj[t] = prev
    pr("NULOS Holm %s" % " ".join("%s=%.4f" % (t, adj[t]) for t in ("SL", "T")))
    h3 = "SOSTENIDA" if all(adj[t] < 0.05 for t in ("SL", "T")) else "NO SOSTENIDA"
    pr("HIPOTESIS H_SUPERA_CE -> %s" % hipotesis(ver))
    pr("HIPOTESIS H_ESCALA -> %s%s" % (hipotesis(ver_e), " (el cerebro entero resta)" if ver_e == "PIERDE" else ""))
    pr("HIPOTESIS H_CABLEADO_CE -> %s" % h3)
    pr("VEREDICTO_GLOBAL -> %s | primaria=%s | escala=%s" % ("VALIDO" if valido else "INVALIDO", ver, ver_e))
    pr("EXIT_AGREGADO=%d" % (0 if valido else 3))
    return 0 if valido else 3


if __name__ == "__main__":
    sys.exit(main())
