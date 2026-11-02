#!/usr/bin/env python3
"""H_MECANISMO, agregado (respuesta 2026-11-02-002). Lee las 17 celdas celda_*.json de intervenir.py y aplica las
reglas del sello SELLO-MECANISMO-2026-11-02.md sin cambiarlas. Lo que mide es causalidad del MODELO de Shiu.

Pruebas principales (4 estimulos x 4 = 16, Holm, alfa 0,05), sobre D = suma de espigas de las neuronas D por ensayo,
pareadas por semilla: P1 C1 > C0, P2 C2 > C0, P3 C3 > C0, P4 C0 > C4. Estadistico: media de la diferencia pareada;
p bilateral por permutacion de signos (B = 99.999, semilla 2026110200 + 4*i + t), p = (1 + #{|T*| >= |T|}) / (B + 1).
Pasa si p_Holm < 0,05 y la media va en la direccion predicha.
Veredicto por estimulo: INVALIDO ante cualquier guarda; REFUTADO si P1 no pasa; SOSTENIDO_EN_MODELO si pasan P1 a P4
y dSX/dX >= 0,5 y dXD/dX >= 0,5; PARCIAL en otro caso.
Uso: python3 agregar_mecanismo.py --dir D [--permitir-sin-pin]
"""
import argparse
import glob
import json
import math
import os

import numpy as np

VERSION = "2026-11-02-002"
ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")
TODAS = ("C0", "C1", "C2", "C3", "C4", "R1", "R2", "R3", "R4", "M5", "K")
BASICAS = ("C0", "C1", "C2", "C3", "C4")
B = 99999
ALFA = 0.05
TECHO_HZ = 400.0
UMBRAL_RATIO = 0.5
PRUEBAS = (("P1", "C1", "C0"), ("P2", "C2", "C0"), ("P3", "C3", "C0"), ("P4", "C0", "C4"))


def pr(s, log):
    print(s, flush=True)
    log.append(s)


def perm_pareada(d, seed, b=B):
    """p bilateral por permutacion de signos de la media de d."""
    d = np.asarray(d, dtype=np.float64)
    if len(d) == 0 or np.all(d == 0):
        return 1.0
    t = abs(d.mean())
    rng = np.random.default_rng(seed)
    cnt = 0
    for k in range(0, b, 10000):
        m = min(10000, b - k)
        s = rng.choice(np.array([-1.0, 1.0]), size=(m, len(d)))
        cnt += int((np.abs((s * d).mean(axis=1)) >= t - 1e-12).sum())
    return (1.0 + cnt) / (b + 1.0)


def holm(ps):
    """p ajustados de Holm, en el orden de entrada."""
    ps = np.asarray(ps, dtype=np.float64)
    m = len(ps)
    orden = np.argsort(ps, kind="stable")
    adj = np.empty(m)
    acc = 0.0
    for r, k in enumerate(orden):
        acc = max(acc, min(1.0, (m - r) * ps[k]))
        adj[k] = acc
    return adj.tolist()


def media(v):
    return float(np.mean(v)) if len(v) else float("nan")


def ratio(a, b):
    return a / b if b not in (0, 0.0) and not math.isnan(b) else None


def veredicto(guardas, pasa, dx, dsx, dxd):
    """guardas: dict nombre -> True si la guarda se dispara. pasa: dict P1..P4 -> bool."""
    if any(guardas.values()):
        return "INVALIDO"
    if not pasa["P1"]:
        return "REFUTADO"
    r1, r2 = ratio(dsx, dx), ratio(dxd, dx)
    if all(pasa[p] for p in ("P1", "P2", "P3", "P4")) and r1 is not None and r2 is not None and \
            r1 >= UMBRAL_RATIO and r2 >= UMBRAL_RATIO:
        return "SOSTENIDO_EN_MODELO"
    return "PARCIAL"


def global_(vs):
    n_inv = sum(v == "INVALIDO" for v in vs)
    if n_inv >= 2:
        return "INVALIDA"
    if sum(v == "SOSTENIDO_EN_MODELO" for v in vs) >= 3 and not any(v == "REFUTADO" for v in vs):
        return "SOSTENIDA_EN_MODELO"
    if sum(v == "REFUTADO" for v in vs) >= 3:
        return "REFUTADA"
    return "MIXTA"


def cargar(d):
    cel = {}
    for r in sorted(glob.glob(os.path.join(d, "celda_*.json"))):
        try:
            c = json.load(open(r))
            cel[c["celda"]] = c
        except Exception as e:  # noqa: BLE001
            cel[os.path.basename(r)] = {"error": str(e)}
    return cel


def completa(c, conds):
    return c is not None and all(k in c.get("conds", {}) and len(c["conds"][k]["D"]) == c["n_run"] for k in conds)


def pin_ok(c, permitir):
    return c is not None and c.get("pines", {}).get("model") and (permitir or (not c.get("sin_pin") and
                                                                    all(c.get("pines", {}).values())))


def rel(c):
    """Fraccion de la salida de D que X suprime: (D1 - D0) / D1."""
    d0, d1 = media(c["conds"]["C0"]["D"]), media(c["conds"]["C1"]["D"])
    return (d1 - d0) / d1 if d1 > 0 else None


def descriptivos(c, i):
    co = c["conds"]
    m = {k: media(v["D"]) for k, v in co.items()}
    d0, d1 = m.get("C0"), m.get("C1")
    out = {"D_media": m, "X_media": {k: media(v["X"]) for k, v in co.items()}}
    den = (d1 - d0) if d0 is not None and d1 is not None else None
    f = {}
    for k in ("R1", "R2"):
        f[k] = ratio(d1 - m[k], den) if k in m and den else None
    for k in ("R3", "R4"):
        f[k] = ratio(m[k], d0) if k in m and d0 else None
    out["restauracion"] = f
    if "K" in m:
        out["K"] = {"delta": m["K"] - d0, "K_sobre_X": ratio(m["K"] - d0, den), "regla": c.get("K")}
    if "M5" in m:
        out["M5_delta"] = m["M5"] - d0
    pos = {x: k for k, x in enumerate(c["indices"]["mirar"])}
    desc = c["indices"]["desc"]
    if desc and "C1" in co:
        a0 = np.array([[r["cuentas"][pos[x]] for x in desc] for r in co["C0"]["ensayos"]], dtype=np.float64)
        a1 = np.array([[r["cuentas"][pos[x]] for x in desc] for r in co["C1"]["ensayos"]], dtype=np.float64)
        dd = a1.sum(1) - a0.sum(1)
        por_tipo = {}
        for k, t in enumerate(c["desc_tipo"]):
            por_tipo[t] = por_tipo.get(t, 0.0) + float((a1[:, k] - a0[:, k]).mean())
        top = sorted(por_tipo.items(), key=lambda kv: (-abs(kv[1]), kv[0]))[:8]
        out["fuera_objetivo"] = {"C0": float(a0.sum(1).mean()), "C1": float(a1.sum(1).mean()),
                                 "p": perm_pareada(dd, 2026110300 + i), "top_tipos": top}
    lat = {}
    for k, v in co.items():
        prim = [r["D_primera_ms"] for r in v["ensayos"] if r["D_primera_ms"] is not None]
        tot = sum(v["D"])
        lat[k] = {"mediana_ms": float(np.median(prim)) if prim else None,
                  "frac_50ms": (sum(r["D_temprano"] for r in v["ensayos"]) / tot) if tot else None}
    out["latencia"] = lat
    S = c["indices"]["S"]
    huellas = {k: [tuple(r["cuentas"][pos[s]] for s in S) for r in v["ensayos"]] for k, v in co.items()}
    base = huellas.get("C0", [])
    out["crn_S_igual"] = {k: (sum(a == b for a, b in zip(h, base)) / len(base)) if base else None
                          for k, h in huellas.items()}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--permitir-sin-pin", action="store_true", help="solo prueba")
    a = ap.parse_args()
    log = []
    cel = cargar(a.dir)
    pr("== agregar_mecanismo.py :: H_MECANISMO (%s) celdas=%d ==" % (VERSION, len(cel)), log)
    ctrl = cel.get("ctrl_mn9")
    mn9_ok = bool(ctrl and completa(ctrl, ["C0"]) and pin_ok(ctrl, a.permitir_sin_pin) and
                  sum(1 for v in ctrl["conds"]["C0"]["D"] if v > 0) >= 9)
    pr("CTRL_MN9 %s ensayos_con_espiga=%s" % ("PASA" if mn9_ok else "FALLA",
                                           sum(1 for v in ctrl["conds"]["C0"]["D"] if v > 0) if ctrl and
                                           "conds" in ctrl and "C0" in ctrl["conds"] else None), log)
    out = {"version": VERSION, "ctrl_mn9": mn9_ok, "estimulos": {}, "tasas": {}, "izquierda": {}}
    ps, info = [], []
    for i, e in enumerate(ESTIM):
        c = cel.get("p_%s_right" % e)
        g = {"pin": not pin_ok(c, a.permitir_sin_pin), "ctrl_mn9": not mn9_ok,
             "celda_faltante": c is None or "error" in c, "C0_C4_incompletas": not completa(c, BASICAS)}
        if not g["celda_faltante"] and not g["C0_C4_incompletas"]:
            co = c["conds"]
            g["corte_vacio"] = any(co[k]["tocadas"]["filas"] == 0 for k in ("C2", "C3", "C4"))
            g["X_no_inhibitoria"] = not c["guardas"].get("X_inhibitoria", False)
            nd, ts = c["conjuntos"]["D"], c["t_run_ms"] / 1000.0
            g["techo"] = any(media(co[k]["D"]) / (nd * ts) >= TECHO_HZ for k in ("C0", "C1"))
            g["piso"] = sum(co["C0"]["D"]) == 0 and sum(co["C1"]["D"]) == 0
        for t, (nom, x, y) in enumerate(PRUEBAS):
            if g["celda_faltante"] or g["C0_C4_incompletas"]:
                ps.append(1.0)
                info.append((e, nom, None))
                continue
            d = np.array(c["conds"][x]["D"], dtype=np.float64) - np.array(c["conds"][y]["D"], dtype=np.float64)
            ps.append(perm_pareada(d, 2026110200 + 4 * i + t))
            info.append((e, nom, float(d.mean())))
        out["estimulos"][e] = {"guardas": g}
    adj = holm(ps)
    for k, (e, nom, dm) in enumerate(info):
        r = out["estimulos"][e]
        r.setdefault("pruebas", {})[nom] = {"media_dif": dm, "p": ps[k], "p_holm": adj[k],
                                            "pasa": bool(dm is not None and dm > 0 and adj[k] < ALFA)}
    vs = []
    for i, e in enumerate(ESTIM):
        r = out["estimulos"][e]
        c = cel.get("p_%s_right" % e)
        pt = r["pruebas"]
        dx, dsx, dxd = pt["P1"]["media_dif"], pt["P2"]["media_dif"], pt["P3"]["media_dif"]
        r["dSX_sobre_dX"] = ratio(dsx, dx) if dx is not None else None
        r["dXD_sobre_dX"] = ratio(dxd, dx) if dx is not None else None
        r["veredicto"] = veredicto(r["guardas"], {p: pt[p]["pasa"] for p in pt}, dx, dsx, dxd)
        vs.append(r["veredicto"])
        if c is not None and "error" not in c and completa(c, BASICAS):
            r["descriptivos"] = descriptivos(c, i)
        pr("ESTIMULO %s veredicto=%s guardas=%s" % (e, r["veredicto"], [k for k, v in r["guardas"].items() if v]),
           log)
        for nom in ("P1", "P2", "P3", "P4"):
            q = pt[nom]
            pr("  %s media_dif=%s p=%.6g p_holm=%.6g pasa=%s" % (nom, q["media_dif"], q["p"], q["p_holm"], q["pasa"]),
               log)
        pr("  dSX/dX=%s dXD/dX=%s" % (r["dSX_sobre_dX"], r["dXD_sobre_dX"]), log)
        if "descriptivos" in r:
            ds = r["descriptivos"]
            pr("  D_media=%s" % json.dumps({k: round(v, 3) for k, v in ds["D_media"].items()}), log)
            pr("  X_media=%s" % json.dumps({k: round(v, 3) for k, v in ds["X_media"].items()}), log)
            pr("  restauracion=%s K=%s M5_delta=%s" % (json.dumps(ds["restauracion"]),
                                                     json.dumps({k: v for k, v in ds.get("K", {}).items()
                                                                 if k != "regla"}), ds.get("M5_delta")), log)
            if "fuera_objetivo" in ds:
                pr("  fuera_objetivo=%s" % json.dumps(ds["fuera_objetivo"]), log)
            pr("  latencia=%s" % json.dumps(ds["latencia"]), log)
            pr("  crn_S_igual=%s" % json.dumps(ds["crn_S_igual"]), log)
        rr = {}
        for hz in ("t20", "t150"):
            ct = cel.get("%s_%s_right" % (hz, e))
            rr[hz] = rel(ct) if ct is not None and completa(ct, ["C0", "C1"]) else None
        rr["t50"] = rel(c) if c is not None and completa(c, ["C0", "C1"]) else None
        lect = None
        if rr["t20"] is not None and rr["t150"] is not None and rr["t20"] > 0:
            if rr["t150"] < 0.5 * rr["t20"]:
                lect = "SUSTRACTIVA"
            elif abs(rr["t150"] - rr["t20"]) <= 0.5 * rr["t20"]:
                lect = "DIVISIVA"
            else:
                lect = "OTRA"
        rr["lectura"] = lect
        out["tasas"][e] = rr
        pr("  TASAS rel20=%s rel50=%s rel150=%s -> %s" % (rr["t20"], rr["t50"], rr["t150"], lect), log)
        cl = cel.get("i_%s_left" % e)
        iz = {"completa": bool(cl is not None and completa(cl, BASICAS))}
        if iz["completa"]:
            for t, (nom, x, y) in enumerate(PRUEBAS):
                d = np.array(cl["conds"][x]["D"], dtype=np.float64) - np.array(cl["conds"][y]["D"], dtype=np.float64)
                iz[nom] = {"media_dif": float(d.mean()), "p_crudo": perm_pareada(d, 2026110250 + 4 * i + t)}
        out["izquierda"][e] = iz
        pr("  IZQUIERDA %s" % json.dumps(iz), log)
    out["global"] = global_(vs)
    pr("H_MECANISMO %s (%s)" % (out["global"], ", ".join("%s=%s" % (e, v) for e, v in zip(ESTIM, vs))), log)
    with open(os.path.join(a.dir, "agregado_mecanismo.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    with open(os.path.join(a.dir, "agregado_mecanismo.log"), "w") as f:
        f.write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
