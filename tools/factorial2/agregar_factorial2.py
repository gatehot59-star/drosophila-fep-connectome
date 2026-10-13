#!/usr/bin/env python3
"""Agregador del factorial 2 de la mosca (respuesta 2026-10-13-004). Sellado antes de correr.

Uso: python3 agregar_factorial2.py <carpeta con los factorial2_*.json> [--humo]

Primaria, por configuracion (7: M46_TASA, M46_LIQ, R1_CON_TASA, R1_CON_LIQ, R1_SIN_TASA, R1_SIN_LIQ, R2_CON_TASA):
  d = acierto de W menos acierto de la regla propia (la regla sobre las mismas entradas que recibe la red), por
  semilla de tau, semilla de prueba y celda. Estimador: la media de d sobre todo. Intervalo: bootstrap de dos vias
  (se remuestrean con reposicion las semillas de tau y, por separado, las de prueba), B = 20.000, semilla 2026,
  percentiles alfa' y 1 - alfa' con alfa' = 0,05 / 7 (TOST con Bonferroni sobre las 7). Margen M = 0,01 (20 de
  2.000 ensayos), declarado antes de correr. Veredicto con el intervalo [lo, hi]:
    SUPERA si lo > +M; PIERDE si hi < -M; EQUIVALENTE si -M < lo y hi < +M;
    NO_INFERIOR si lo > -M y hi >= +M; NO_SUPERIOR si hi < +M y lo <= -M; INDETERMINADO si no.
  Por celda: lo mismo, descriptivo (mismo alfa').
Contrastes (W contra W en las mismas semillas y celdas; familia aparte, alfa' = 0,05 / 9, mismo margen):
  INHIB_R1_TASA, INHIB_R1_LIQ (CON menos SIN), LIQ_M46, LIQ_R1_CON, LIQ_R1_SIN (LIQ menos TASA),
  RECORTE_R1_TASA, RECORTE_R1_LIQ (R1_CON menos M46), RECORTE_R2_TASA (R2_CON menos R1_CON, en las semillas
  comunes) y SENSORES (regla de 418 menos regla de 40, solo semillas de prueba).
  Nombres: AYUDA, DANA, EQUIVALENTE, NO_INFERIOR, NO_SUPERIOR, INDETERMINADO.
Controles: ANCLA_015 valido (reproduce la 015); todos los json validos; el plan completo (semillas y celdas);
  TAU_DN_IGUAL (las 6 descendentes tienen el mismo tau en todas las configuraciones para cada semilla);
  REGLA40_IGUAL (la regla de 40 da lo mismo en todas: mismo sensor, mismo ruido por root_id).
Hipotesis pre-registradas:
  H_ALCANZA "con cableado suficiente la simulacion alcanza al diseno": refutada si R1_CON_TASA y R1_CON_LIQ dan
    PIERDE; sostenida si alguna de las dos da EQUIVALENTE, NO_INFERIOR o SUPERA.
  H_SUPERA "el cableado aporta algo mas que el diseno": sostenida solo si alguna configuracion R da SUPERA.
"""
import glob
import json
import os
import sys

import numpy as np

M, B, ALFA = 0.01, 20000, 0.05
TAUS10, PRUEBAS10 = list(range(10)), list(range(2, 12))
PLAN = {c: (TAUS10, PRUEBAS10) for c in ("M46_TASA", "M46_LIQ", "R1_CON_TASA", "R1_CON_LIQ", "R1_SIN_TASA",
                                         "R1_SIN_LIQ")}
PLAN["R2_CON_TASA"] = ([0, 1, 2], list(range(2, 7)))
PRIMARIAS = list(PLAN)
CELDAS = ["0.0|0.15", "0.0|0.45", "0.3|0.15", "0.3|0.45", "0.6|0.15", "0.6|0.45"]
CONTRASTES = [("INHIB_R1_TASA", "R1_CON_TASA", "R1_SIN_TASA"), ("INHIB_R1_LIQ", "R1_CON_LIQ", "R1_SIN_LIQ"),
              ("LIQ_M46", "M46_LIQ", "M46_TASA"), ("LIQ_R1_CON", "R1_CON_LIQ", "R1_CON_TASA"),
              ("LIQ_R1_SIN", "R1_SIN_LIQ", "R1_SIN_TASA"), ("RECORTE_R1_TASA", "R1_CON_TASA", "M46_TASA"),
              ("RECORTE_R1_LIQ", "R1_CON_LIQ", "M46_LIQ"), ("RECORTE_R2_TASA", "R2_CON_TASA", "R1_CON_TASA")]
N_CONTR = len(CONTRASTES) + 1


def pr(s):
    print(s, flush=True)


def bootstrap(D, alfa, rng):
    """D: (n_tau, n_prueba). Media remuestreando filas y columnas por separado."""
    nt, npb = D.shape
    est = float(D.mean())
    bs = np.empty(B)
    for b in range(B):
        ti = rng.integers(0, nt, nt)
        pj = rng.integers(0, npb, npb)
        bs[b] = D[np.ix_(ti, pj)].mean()
    return est, float(np.quantile(bs, alfa)), float(np.quantile(bs, 1 - alfa))


def veredicto(lo, hi, nombres):
    sup, pie = nombres
    if lo > M:
        return sup
    if hi < -M:
        return pie
    if lo > -M and hi < M:
        return "EQUIVALENTE"
    if lo > -M:
        return "NO_INFERIOR"
    if hi < M:
        return "NO_SUPERIOR"
    return "INDETERMINADO"


def main():
    carpeta = sys.argv[1]
    humo = "--humo" in sys.argv
    J = {}
    validos, ancla = {}, None
    for ruta in sorted(glob.glob(os.path.join(carpeta, "**", "factorial2_*.json"), recursive=True)):
        with open(ruta) as f:
            r = json.load(f)
        validos[os.path.basename(ruta)] = r["valido"]
        if r["config"] == "ANCLA_015":
            ancla = r
            continue
        J.setdefault(r["config"], []).append(r)
    pr("JSON leidos=%d validos=%s" % (len(validos), ",".join("%s:%s" % kv for kv in validos.items())))
    ok_ancla = ancla is not None and ancla["valido"] and not ancla["humo"]
    pr("CHEQUEO ANCLA_015 presente=%s valido=%s -> %s" % (ancla is not None, ancla and ancla["valido"], ok_ancla))
    todos_validos = all(validos.values())
    # tablas por configuracion
    W, RP, R40, faltan = {}, {}, {}, {}
    tau_dn = {}
    for c, lst in J.items():
        for r in lst:
            for st, v in r["tau_DN"].items():
                tau_dn.setdefault(int(st), []).append((c, tuple(v), tuple(r["dns_root"])))
            for x in r["corridas"]:
                W.setdefault(c, {})[(x["tau"], x["prueba"], x["celda"])] = x["W"]
                RP.setdefault(c, {})[(x["prueba"], x["celda"])] = x["regla_propia"]
                R40.setdefault(c, {})[(x["prueba"], x["celda"])] = x["regla40"]
    tau_ok = all(len(set((v, d) for _, v, d in L)) == 1 for L in tau_dn.values())
    pr("CHEQUEO TAU_DN_IGUAL semillas=%s -> %s" % (sorted(tau_dn), tau_ok))
    claves40 = {}
    for c, dd in R40.items():
        for k, v in dd.items():
            claves40.setdefault(k, set()).add(v)
    r40_ok = all(len(v) == 1 for v in claves40.values())
    pr("CHEQUEO REGLA40_IGUAL claves=%d -> %s" % (len(claves40), r40_ok))
    plan = {}
    for c in PRIMARIAS:
        taus, pruebas = PLAN[c]
        if humo and c in J:
            taus = sorted(set(k[0] for k in W.get(c, {})))
            pruebas = sorted(set(k[1] for k in W.get(c, {})))
        need = [(t, p, k) for t in taus for p in pruebas for k in CELDAS]
        falt = [x for x in need if x not in W.get(c, {})]
        plan[c] = (taus, pruebas, not falt)
        faltan[c] = len(falt)
    pr("CHEQUEO PLAN %s" % " ".join("%s=%s" % (c, "completo" if plan[c][2] else "faltan_%d" % faltan[c]) for c in PRIMARIAS))
    valido = ok_ancla and todos_validos and tau_ok and r40_ok
    if humo:
        valido = todos_validos and tau_ok and r40_ok
        pr("# HUMO: el ancla no se exige y el plan se toma de lo que hay; numeros sin valor")
    rng = np.random.default_rng(2026)
    a1 = ALFA / len(PRIMARIAS)
    pr("PRIMARIA margen=%.3f B=%d alfa_por_lado=%.5f (nivel del intervalo %.4f)" % (M, B, a1, 1 - 2 * a1))
    ver = {}
    for c in PRIMARIAS:
        taus, pruebas, completo = plan[c]
        if c not in W or not completo:
            ver[c] = "NO_EVALUABLE"
            pr("PRIMARIA %s -> NO_EVALUABLE (faltan %d corridas)" % (c, faltan[c]))
            continue
        D = np.array([[[W[c][(t, p, k)] - RP[c][(p, k)] for k in CELDAS] for p in pruebas] for t in taus])
        mw = np.mean([[[W[c][(t, p, k)] for k in CELDAS] for p in pruebas] for t in taus])
        mr = np.mean([[RP[c][(p, k)] for k in CELDAS] for p in pruebas])
        est, lo, hi = bootstrap(D.mean(2), a1, rng)
        ver[c] = veredicto(lo, hi, ("SUPERA", "PIERDE"))
        pr("PRIMARIA %s W=%.4f regla_propia=%.4f dif=%+.4f IC=[%+.4f, %+.4f] corridas=%d -> %s" % (
            c, mw, mr, est, lo, hi, D.size, ver[c]))
        for j, k in enumerate(CELDAS):
            e2, l2, h2 = bootstrap(D[:, :, j], a1, rng)
            pr("  CELDA %s %s dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (c, k, e2, l2, h2, veredicto(l2, h2, ("SUPERA", "PIERDE"))))
    a2 = ALFA / N_CONTR
    pr("CONTRASTES margen=%.3f alfa_por_lado=%.5f" % (M, a2))
    vc = {}
    for nom, c1, c2 in CONTRASTES:
        if ver.get(c1) == "NO_EVALUABLE" or ver.get(c2) == "NO_EVALUABLE" or c1 not in W or c2 not in W:
            vc[nom] = "NO_EVALUABLE"
            pr("CONTRASTE %s (%s menos %s) -> NO_EVALUABLE" % (nom, c1, c2))
            continue
        taus = [t for t in plan[c1][0] if t in plan[c2][0]]
        pruebas = [p for p in plan[c1][1] if p in plan[c2][1]]
        D = np.array([[np.mean([W[c1][(t, p, k)] - W[c2][(t, p, k)] for k in CELDAS]) for p in pruebas] for t in taus])
        est, lo, hi = bootstrap(D, a2, rng)
        vc[nom] = veredicto(lo, hi, ("AYUDA", "DANA"))
        pr("CONTRASTE %s (%s menos %s) taus=%d pruebas=%d dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (
            nom, c1, c2, len(taus), len(pruebas), est, lo, hi, vc[nom]))
    if "R1_CON_TASA" in RP and plan["R1_CON_TASA"][2]:
        pruebas = plan["R1_CON_TASA"][1]
        D = np.array([[np.mean([RP["R1_CON_TASA"][(p, k)] - R40["R1_CON_TASA"][(p, k)] for k in CELDAS]) for p in pruebas]])
        est, lo, hi = bootstrap(D, a2, rng)
        vc["SENSORES"] = veredicto(lo, hi, ("AYUDA", "DANA"))
        pr("CONTRASTE SENSORES (regla 418 menos regla 40) pruebas=%d dif=%+.4f IC=[%+.4f, %+.4f] -> %s" % (
            len(pruebas), est, lo, hi, vc["SENSORES"]))
    else:
        vc["SENSORES"] = "NO_EVALUABLE"
        pr("CONTRASTE SENSORES -> NO_EVALUABLE")
    r1 = [ver.get("R1_CON_TASA"), ver.get("R1_CON_LIQ")]
    if "NO_EVALUABLE" in r1:
        h_alc = "NO_EVALUABLE"
    elif all(v == "PIERDE" for v in r1):
        h_alc = "REFUTADA"
    elif any(v in ("EQUIVALENTE", "NO_INFERIOR", "SUPERA") for v in r1):
        h_alc = "SOSTENIDA"
    else:
        h_alc = "SIN_DECIDIR"
    sup = [c for c in PRIMARIAS if c.startswith("R") and ver.get(c) == "SUPERA"]
    h_sup = "SOSTENIDA (%s)" % ",".join(sup) if sup else "NO SOSTENIDA"
    pr("HIPOTESIS H_ALCANZA -> %s" % h_alc)
    pr("HIPOTESIS H_SUPERA -> %s" % h_sup)
    pr("VEREDICTO_GLOBAL -> %s | %s" % ("VALIDO" if valido else "INVALIDO",
                                        " ".join("%s=%s" % (c, ver[c]) for c in PRIMARIAS)))
    pr("EXIT_AGREGADO=%d" % (0 if valido else 3))
    return 0 if valido else 3


if __name__ == "__main__":
    sys.exit(main())
