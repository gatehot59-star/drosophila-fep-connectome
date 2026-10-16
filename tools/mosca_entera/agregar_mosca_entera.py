#!/usr/bin/env python3
"""H_MOSCA_ENTERA, agregado y veredictos contra las bandas del sello (respuesta 2026-10-14-047).

Lee lif_real.json, lif_shufW_k*.json, liq_real.json (+ _top.npz) y liq_SHUF_*_k*.json (+ _top.npz) de --dir.
Bandas del sello (tools/mosca_entera/SELLO-MOSCA-ENTERA.md, md5 55bc4c76657e35f341300d0e082c7ebe):
  REPRO_SHIU  MN9 con espiga en >= 27 de 30 ensayos reales y <= 2 de 20 SHUF_W con espiga en >= 5 de sus 10.
  K_SANO      10 <= K <= 5000.
  MN9         r_MN9 (LIQ, tau 30) > 0 y mayor que los 40 de cada nulo: SOSTENIDA; r <= 0 o >= 5 nulos de algun
              tipo iguales o mayores: REFUTADA; resto SIN_DECIDIR.
  CONJUNTO    J (LIQ, tau 30) contra los 40 de cada nulo, mismas bandas sin la condicion de signo.
  RIVAL       J (LIQ, tau 30) - J (PROX): >= +0,05 SOSTENIDA; <= 0 REFUTADA; resto SIN_DECIDIR.
  LIQ         mediana sobre tau 30 a 39 de J (LIQ) - J (TASA): >= +0,02 SOSTENIDA; <= 0 REFUTADA; resto SIN_DECIDIR.
Si REPRO_SHIU no pasa, las cuatro quedan NO_MEDIDO; si K no es sano, CONJUNTO, RIVAL y LIQ quedan NO_MEDIDO.
Con --humo todo sale marcado HUMO (numeros sin valor) y las bandas que piden 40 nulos dicen INCOMPLETO.
Uso: python3 agregar_mosca_entera.py --dir D [--humo]
"""
import argparse
import glob
import hashlib
import json
import os

import numpy as np

N_NULOS, N_SHUF_LIF, N_REAL, N_ENS_SHUF = 40, 20, 30, 10
TAU_PRIM = 30


def pr(s, f=None):
    print(s, flush=True)
    if f is not None:
        f.write(s + "\n")


def jaccard(a, b):
    a, b = set(int(x) for x in a), set(int(x) for x in b)
    return len(a & b) / len(a | b) if (a or b) else float("nan")


def repro_shiu(real, shufs):
    """real: dict de la corrida real; shufs: lista de dicts de corridas SHUF_W."""
    ok_real = real["n_run"] == N_REAL and real["ensayos_mn9"] >= 27
    activos = sum(1 for s in shufs if s["ensayos_mn9"] >= 5)
    completo = len(shufs) == N_SHUF_LIF and all(s["n_run"] == N_ENS_SHUF for s in shufs)
    if not completo:
        return "INCOMPLETO", activos
    return ("PASA" if ok_real and activos <= 2 else "FALLA"), activos


def banda_nulos(real, nulos_por_tipo, signo):
    """real contra cada lista de 40 nulos: SOSTENIDA, REFUTADA, SIN_DECIDIR o INCOMPLETO."""
    if signo and not real > 0:
        return "REFUTADA", {t: None for t in nulos_por_tipo}
    ge = {t: int(sum(1 for v in vs if v >= real)) for t, vs in nulos_por_tipo.items()}
    if any(n >= 5 for n in ge.values()):
        return "REFUTADA", ge
    if any(len(vs) != N_NULOS for vs in nulos_por_tipo.values()):
        return "INCOMPLETO", ge
    if all(n == 0 for n in ge.values()):
        return "SOSTENIDA", ge
    return "SIN_DECIDIR", ge


def banda_diferencia(d, alto):
    if d >= alto:
        return "SOSTENIDA"
    if d <= 0:
        return "REFUTADA"
    return "SIN_DECIDIR"


def veredictos(repro, k, mn9_real, mn9_nulos, j_real, j_nulos, j_prox, j_liq, j_tasa):
    """Todo lo que decide el sello, en una funcion que la prueba ejercita con numeros plantados."""
    v = {"REPRO_SHIU": repro, "K": k, "K_SANO": 10 <= k <= 5000}
    if repro != "PASA":
        for h in ("MN9", "CONJUNTO", "RIVAL", "LIQ"):
            v[h] = "NO_MEDIDO"
        return v
    v["MN9"], v["MN9_ge"] = banda_nulos(mn9_real, mn9_nulos, True)
    if not v["K_SANO"]:
        for h in ("CONJUNTO", "RIVAL", "LIQ"):
            v[h] = "NO_MEDIDO"
        return v
    v["CONJUNTO"], v["CONJUNTO_ge"] = banda_nulos(j_real, j_nulos, False)
    v["RIVAL_d"] = j_real - j_prox
    v["RIVAL"] = banda_diferencia(v["RIVAL_d"], 0.05)
    difs = [j_liq[s] - j_tasa[s] for s in sorted(j_liq) if s in j_tasa]
    v["LIQ_difs"] = difs
    v["LIQ_mediana"] = float(np.median(difs)) if difs else float("nan")
    v["LIQ"] = banda_diferencia(v["LIQ_mediana"], 0.02) if len(difs) == 10 else "INCOMPLETO"
    return v


def md5(ruta):
    return hashlib.md5(open(ruta, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--humo", action="store_true")
    a = ap.parse_args()
    log = open(os.path.join(a.dir, "agregado.log"), "w")
    pr("== agregar_mosca_entera.py :: H_MOSCA_ENTERA (2026-10-14-047)%s ==" % (" HUMO, NUMEROS SIN VALOR" if a.humo
                                                                            else ""), log)
    lif = json.load(open(os.path.join(a.dir, "lif_real.json")))
    real = lif["corridas"]["real"]
    shufs = []
    for p in sorted(glob.glob(os.path.join(a.dir, "lif_shufW_k*.json"))):
        shufs.extend(json.load(open(p))["corridas"].values())
    repro, activos = repro_shiu(real, shufs)
    if a.humo and repro == "INCOMPLETO":
        repro_ef = "PASA"
        pr("HUMO: REPRO_SHIU INCOMPLETO (%d SHUF_W); se sigue como si pasara para ejercitar el agregado" % len(shufs), log)
    else:
        repro_ef = repro
    pr("LIF real ensayos_mn9=%d de %d tasa_mn9=%.2f Hz K=%d | SHUF_W corridas=%d con_mn9>=5=%d -> REPRO_SHIU %s" % (
        real["ensayos_mn9"], real["n_run"], real["tasa_mn9"], real["K"], len(shufs), activos, repro), log)
    s_lif = real["S_LIF_idx"]
    k = len(s_lif)
    liq = json.load(open(os.path.join(a.dir, "liq_real.json")))
    tops = np.load(os.path.join(a.dir, "liq_real_top.npz"))
    taus = sorted(int(t) for t in liq["LIQ"])
    j_liq = {t: jaccard(tops["LIQ_%d" % t][:k], s_lif) for t in taus}
    j_tasa = {t: jaccard(tops["TASA_%d" % t][:k], s_lif) for t in taus}
    j_prox = jaccard(tops["PROX"][:k], s_lif)
    for t in taus:
        pr("TAU %d LIQ mn9=%.6g J=%.4f | TASA mn9=%.6g J=%.4f" % (t, liq["LIQ"][str(t)]["mn9"], j_liq[t],
                                                                liq["TASA"][str(t)]["mn9"], j_tasa[t]), log)
    pr("PROX J=%.4f mn9=%.6g" % (j_prox, liq["PROX"]["mn9"]), log)
    mn9_nulos, j_nulos = {"SHUF_W": [], "SHUF_G": []}, {"SHUF_W": [], "SHUF_G": []}
    for p in sorted(glob.glob(os.path.join(a.dir, "liq_SHUF_*_k*.json"))):
        d = json.load(open(p))
        tn = np.load(p.replace(".json", "_top.npz"))
        for kk, v in sorted(d["nulos"].items(), key=lambda x: int(x[0])):
            mn9_nulos[d["tipo"]].append(v["mn9"])
            j_nulos[d["tipo"]].append(jaccard(tn["%s_%s" % (d["tipo"], kk)][:k], s_lif))
    for tipo in mn9_nulos:
        pr("NULOS %s n=%d mn9_max=%s J_max=%s" % (tipo, len(mn9_nulos[tipo]),
                                                  "%.6g" % max(mn9_nulos[tipo]) if mn9_nulos[tipo] else "-",
                                                  "%.4f" % max(j_nulos[tipo]) if j_nulos[tipo] else "-"), log)
    t0 = TAU_PRIM if TAU_PRIM in j_liq else taus[0]
    v = veredictos(repro_ef, k, liq["LIQ"][str(t0)]["mn9"], mn9_nulos, j_liq[t0], j_nulos, j_prox, j_liq, j_tasa)
    v["REPRO_SHIU_medido"] = repro
    for h in ("REPRO_SHIU", "K_SANO", "MN9", "CONJUNTO", "RIVAL", "LIQ"):
        extra = ""
        if h == "MN9" and "MN9_ge" in v:
            extra = " nulos_ge=%s" % v["MN9_ge"]
        if h == "CONJUNTO" and "CONJUNTO_ge" in v:
            extra = " nulos_ge=%s" % v["CONJUNTO_ge"]
        if h == "RIVAL" and "RIVAL_d" in v:
            extra = " d=%+.4f" % v["RIVAL_d"]
        if h == "LIQ" and "LIQ_mediana" in v:
            extra = " mediana=%+.4f" % v["LIQ_mediana"]
        pr("VEREDICTO%s %s %s%s" % ("_HUMO" if a.humo else "", h, v[h] if h != "REPRO_SHIU" else repro, extra), log)
    out = {"humo": a.humo, "K": k, "j_liq": j_liq, "j_tasa": j_tasa, "j_prox": j_prox, "mn9_nulos": mn9_nulos,
           "j_nulos": j_nulos, "veredictos": v, "lif_real": {x: real[x] for x in ("ensayos_mn9", "n_run", "tasa_mn9",
                                                                                  "K")}}
    with open(os.path.join(a.dir, "agregado.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    log.close()
    print("MD5 agregado.json=%s agregado.log=%s" % (md5(os.path.join(a.dir, "agregado.json")),
                                                    md5(os.path.join(a.dir, "agregado.log"))))


if __name__ == "__main__":
    main()
