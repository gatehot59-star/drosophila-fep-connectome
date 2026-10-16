#!/usr/bin/env python3
"""H_ENTERA_UMBRAL, agregado y veredictos contra las bandas del sello (respuesta 2026-10-14-051).

Sello: tools/mosca_entera/SELLO-UMBRAL-050.md (868ded6, md5 680abca839bd6c80367c9b434af7d800).
Lee umb_real.json (+ _top.npz) y umb_SHUF_*_k*.json (+ _top.npz) de --dir, y la S_LIF de la 049 (--lif).
  Controles   PIN (md5 de cada trabajo), CALIB_REAL (|Activas - 321| <= 32), TASA_049 (J = 0,3659574468 +- 1e-9).
              Si alguno falla, las tres hipotesis quedan NO_MEDIDO.
  H_UMB_MN9       r_MN9 real > 0 y mayor que los 40 de cada familia: SOSTENIDA; r <= 0 o >= 5 nulos de alguna
                  familia iguales o mayores: REFUTADA; resto SIN_DECIDIR (banda_nulos de la 046).
  H_UMB_CONJUNTO  J real contra los 40 de cada familia, mismas bandas sin signo.
  H_UMB_GANA      J(UMB) - J(TASA) >= +0,05 SOSTENIDA; <= 0 REFUTADA; resto SIN_DECIDIR.
  Secundaria      theta del real fijo en los 80 nulos: no decide.
Con --humo todo sale marcado HUMO (numeros sin valor).
Uso: python3 agregar_umb.py --dir D --lif L [--humo]
"""
import argparse
import glob
import hashlib
import json
import os
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import agregar_mosca_entera as ag  # noqa: E402

N_OBJ, TOL = 321, 32
J_TASA_049, TOL_TASA = 0.3659574468085106, 1e-9
MD5 = {"conn": "3d802fd542b5d18570ba1ba0bb0abed9", "annot": "719904abad876c68ace1b5690c9b9b63",
       "lif": "f6383d18a0e05efb65696175949df9fa"}


def pr(s, f=None):
    print(s, flush=True)
    if f is not None:
        f.write(s + chr(10))


def md5(ruta):
    return hashlib.md5(open(ruta, "rb").read()).hexdigest()


def controles(real, nulos_json):
    """PIN, CALIB_REAL y TASA_049. Devuelve dict con cada uno y ok."""
    pins = [real["md5"]] + [d["md5"] for d in nulos_json]
    c = {"PIN": all(p.get(k) == v for p in pins for k, v in MD5.items()),
         "CALIB_REAL": abs(int(real["activas"]) - N_OBJ) <= TOL,
         "TASA_049": abs(float(real["J_tasa"]) - J_TASA_049) <= TOL_TASA}
    c["ok"] = c["PIN"] and c["CALIB_REAL"] and c["TASA_049"]
    return c


def veredictos(ok, mn9_real, mn9_nulos, j_real, j_nulos, j_tasa):
    v = {}
    if not ok:
        v["MN9"] = v["CONJUNTO"] = v["GANA"] = "NO_MEDIDO"
        return v
    v["MN9"], v["MN9_ge"] = ag.banda_nulos(mn9_real, mn9_nulos, True)
    v["CONJUNTO"], v["CONJUNTO_ge"] = ag.banda_nulos(j_real, j_nulos, False)
    v["GANA_d"] = j_real - j_tasa
    v["GANA"] = ag.banda_diferencia(v["GANA_d"], 0.05)
    return v


def lectura(v, mn9_real):
    """Seccion 6 del sello."""
    h = v.get("MN9")
    if h == "SOSTENIDA":
        s = ("con el presupuesto de actividad del LIF el cableado real lleva el azucar a MN9 mejor que 80 barajados: "
             "la falla de la 049 era la no linealidad, no el cableado")
        if v.get("CONJUNTO") == "SOSTENIDA":
            s += "; con CONJUNTO SOSTENIDA se puede sellar la destilacion"
        return s
    if h == "REFUTADA" and not mn9_real > 0:
        return "MN9 no entra entre las activas del real: un umbral sobre la tasa no alcanza"
    if h == "REFUTADA":
        return "el umbral lleva el azucar a MN9 tambien sin el cableado real: no es especifico"
    if h == "SIN_DECIDIR":
        return "80 nulos no lo resuelven; no se agregan nulos despues de ver"
    return "sin lectura (%s)" % h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--lif", required=True)
    ap.add_argument("--humo", action="store_true")
    a = ap.parse_args()
    log = open(os.path.join(a.dir, "agregado_umb.log"), "w")
    tag = "_HUMO" if a.humo else ""
    pr("== agregar_umb.py :: H_ENTERA_UMBRAL (2026-10-14-051)%s ==" % (" HUMO, NUMEROS SIN VALOR" if a.humo else ""), log)
    m_lif = md5(a.lif)
    s_lif = json.load(open(a.lif))["corridas"]["real"]["S_LIF_idx"]
    K = len(s_lif)
    pr("LIF %s md5=%s K=%d" % (a.lif, m_lif, K), log)
    real = json.load(open(os.path.join(a.dir, "umb_real.json")))
    tr = np.load(os.path.join(a.dir, "umb_real_top.npz"))
    j_umb = ag.jaccard(tr["UMB"][:K], s_lif)
    j_tasa = ag.jaccard(tr["TASA"][:K], s_lif)
    real["J_tasa"] = j_tasa
    pr("REAL theta=%.9g activas=%d estado=%s mn9=%.6g rango_mn9=%d J_umb=%.6f J_tasa=%.10f" % (
        real["theta"], real["activas"], real["estado"], real["mn9_umb"], real["rango_mn9"], j_umb, j_tasa), log)
    mn9_n, j_n, est, mn9_f, act_f, th = ({"SHUF_W": [], "SHUF_G": []} for _ in range(6))
    nulos_json = []
    for p in sorted(glob.glob(os.path.join(a.dir, "umb_SHUF_*_k*.json"))):
        d = json.load(open(p))
        nulos_json.append(d)
        tn = np.load(p.replace(".json", "_top.npz"))
        for kk, vv in sorted(d["nulos"].items(), key=lambda x: int(x[0])):
            t = d["tipo"]
            mn9_n[t].append(vv["mn9"])
            j_n[t].append(ag.jaccard(tn["%s_%s" % (t, kk)][:K], s_lif))
            est[t].append(vv["estado"])
            mn9_f[t].append(vv["mn9_fijo"])
            act_f[t].append(vv["activas_fijo"])
            th[t].append(vv["theta"])
    for t in ("SHUF_W", "SHUF_G"):
        cuenta = {e: est[t].count(e) for e in sorted(set(est[t]))}
        pr("NULOS %s n=%d mn9_max=%s J_max=%s theta_mediana=%s estados=%s" % (
            t, len(mn9_n[t]), "%.6g" % max(mn9_n[t]) if mn9_n[t] else "-", "%.4f" % max(j_n[t]) if j_n[t] else "-",
            "%.6g" % float(np.median(th[t])) if th[t] else "-", cuenta), log)
        pr("SECUNDARIA %s theta_real fijo: nulos con mn9 >= real=%d activas_mediana=%s" % (
            t, sum(1 for x in mn9_f[t] if x >= real["mn9_umb"]),
            "%.0f" % float(np.median(act_f[t])) if act_f[t] else "-"), log)
    c = controles(real, nulos_json)
    for k in ("PIN", "CALIB_REAL", "TASA_049"):
        pr("CONTROL%s %s %s" % (tag, k, "PASA" if c[k] else "FALLA"), log)
    v = veredictos(c["ok"], real["mn9_umb"], mn9_n, j_umb, j_n, j_tasa)
    pr("VEREDICTO%s H_UMB_MN9 %s%s" % (tag, v["MN9"], " nulos_ge=%s" % v["MN9_ge"] if "MN9_ge" in v else ""), log)
    pr("VEREDICTO%s H_UMB_CONJUNTO %s%s" % (tag, v["CONJUNTO"],
                                           " nulos_ge=%s" % v["CONJUNTO_ge"] if "CONJUNTO_ge" in v else ""), log)
    pr("VEREDICTO%s H_UMB_GANA %s%s" % (tag, v["GANA"], " d=%+.4f" % v["GANA_d"] if "GANA_d" in v else ""), log)
    lect = lectura(v, real["mn9_umb"])
    pr("LECTURA%s %s" % (tag, lect), log)
    out = {"humo": a.humo, "K": K, "lif_md5": m_lif, "real": {k: real[k] for k in ("theta", "activas", "estado",
                                                                                  "mn9_umb", "rango_mn9")},
           "J_umb": j_umb, "J_tasa": j_tasa, "mn9_nulos": mn9_n, "j_nulos": j_n, "estados": est, "theta_nulos": th,
           "mn9_fijo": mn9_f, "activas_fijo": act_f, "controles": c, "veredictos": v, "lectura": lect}
    with open(os.path.join(a.dir, "agregado_umb.json"), "w") as f:
        json.dump(out, f, indent=1, default=float)
    log.close()
    print("MD5 agregado_umb.json=%s agregado_umb.log=%s" % (md5(os.path.join(a.dir, "agregado_umb.json")),
                                                            md5(os.path.join(a.dir, "agregado_umb.log"))))


if __name__ == "__main__":
    main()
