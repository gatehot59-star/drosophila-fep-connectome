#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
output_control_permutation_correction.py :: correccion por comparaciones multiples del nulo fuerte (006).

Pedido 2026-10-10 (Abraham): "Correct the 006 null for multiple comparisons".

La 006 marco cada test (clase x conjunto de salida, con D1 y con D2) con p <= 0,001 de cada lado, sin
corregir por la cantidad de tests, con dos nulos (perm: permutacion simple; estr: dentro de estratos de
fuerza de salida) y dos umbrales (>=1 y >=5). Sus afirmaciones firmes son del nulo estr con D1: SOBRE
en >=1 y en >=5 en cualquier conjunto, y BAJO en >=1 y en >=5 en los de nivel 1. Aca:

  1. Se regenera el nulo de la 006 con sus mismas semillas y parametros (leidos de su JSON) y se exige
     que estratos, D1, D2, p, flags y la lista de firmes salgan identicos (CRUCE_006).
  2. Las correcciones de la 008, con sus mismas funciones (tools/output_control_region_correction.py):
     max-T step-down (FWER), BH y BY (FDR). Ademas Holm sobre los p de permutacion: con R = 10.000 el
     p bilateral minimo es 0,0002 y Holm ya puede rechazar con hasta 250 tests.
  3. Familia = los tests de un umbral, un nulo y un estadistico (D1 o D2) cuyo nulo varia: ocho
     familias. Las afirmaciones de la 006 son de D1, asi que D2 no les cobra tests.
  4. Firme corregido = la regla de la 006 con ajustado <= alfa en >=1 y en >=5. Se firma con BY, como
     en la 008; el subconjunto FWER es el que aguantan max-T y Holm a la vez (elegir despues el que
     mas deja pasar no controlaria nada).

Controles que pueden dar rojo:
  CRUCE_006         estratos, D1, D2, p, flags y firmes identicos a los de la 006.
  CONSISTENCIA      step-down <= single-step, ajustados monotonos, BY >= BH y Holm >= BH.
  CONTROL_NEGATIVO  etiquetados falsos del mismo nulo, corregidos igual que el real: los que tienen
                    algun rechazo no pasan de max(3, 3 x alfa x n) por metodo, sumando las ocho familias.
  R_PEDIDO_500      con R < 500 en la 006, o una 006 que no dio PASS, el veredicto no puede ser PASS.
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

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import output_control_by_class as oc  # noqa: E402
import output_control_permutation_null as pn  # noqa: E402
import output_control_region_correction as cc  # noqa: E402

ALFA = 0.05
N_FALSOS = 20
R_MINIMO = 500
FACTOR_CONTROL = 3.0
TOL_CRUCE = 1e-12
METODOS = ("maxT", "Holm", "BH", "BY")
ESTADISTICOS = ("D1", "D2")
PIN_JSON_006_MD5 = "ec64172711d7d18040f6f09335d7521b"


def holm(p):
    """p ajustados de Holm (step-down), devueltos en el orden de entrada."""
    p = np.asarray(p, dtype=np.float64)
    m = len(p)
    if m == 0:
        return p.copy()
    o = np.argsort(p, kind="stable")
    a = np.maximum.accumulate(p[o] * (m - np.arange(m)))
    out = np.empty(m)
    out[o] = np.minimum(a, 1.0)
    return out


def corregir(D, nul, E, V, validas, alfa=ALFA):
    """La familia de la 008 (max-T, BH, BY) mas Holm sobre el mismo p bilateral."""
    fam = cc.corregir_familia(D, nul, E, V, validas, alfa)
    K, m = D.shape
    idx = fam["idx"]
    ev = fam["ev"]
    p2 = cc.p_bilateral(ev["ps"], ev["pb"]).ravel()[idx]
    ph = holm(p2)
    sube = ev["ps"].ravel()[idx] < ev["pb"].ravel()[idx]
    pa = np.full(K * m, np.nan)
    pa[idx] = ph
    dec = np.full(K * m, "-", dtype="<U5")
    dec[idx] = np.where(ph <= alfa, np.where(sube, "SOBRE", "BAJO"), "-")
    fam["p_aj"]["Holm"] = pa.reshape(K, m)
    fam["decision"]["Holm"] = dec.reshape(K, m)
    qbh = fam["p_aj"]["BH"].ravel()[idx]
    o = np.argsort(p2, kind="stable")
    fam["consistencia"]["holm_ge_bh"] = bool(np.all(ph >= qbh - 1e-15))
    fam["consistencia"]["holm_monotono"] = bool(np.all(np.diff(ph[o]) >= -1e-15))
    return fam


def falsos(perm, sumar, U, nul, E, V, fams, cortes, n_falsos, semilla, alfa=ALFA):
    """Etiquetados falsos del mismo nulo, corregidos igual que el real en cada familia (D1 y D2)."""
    rng = np.random.default_rng(semilla)
    sd = np.sqrt(np.maximum(V, 0.0))
    con = {st: {mt: 0 for mt in METODOS} for st in fams}
    for _ in range(n_falsos):
        Dall = sumar(perm(rng), U)
        for st, fam in fams.items():
            sl = cortes[st]
            idx = fam["idx"]
            D = Dall[:, sl]
            t = np.abs(D.ravel()[idx] - E[:, sl].ravel()[idx]) / sd[:, sl].ravel()[idx]
            p_sd, _ = cc.maxt_stepdown(t, fam["Z"])
            ev = pn.evaluar_nulo(D, nul[:, :, sl])
            p2 = cc.p_bilateral(ev["ps"], ev["pb"]).ravel()[idx]
            aj = {"maxT": p_sd, "Holm": holm(p2), "BH": cc.bh(p2), "BY": cc.by(p2)}
            for mt in METODOS:
                con[st][mt] += int((aj[mt] <= alfa).any())
    return con


def firmes_regla_006(d1, d5, validas_ambos, es_n1):
    """La regla de la 006: SOBRE en >=1 y en >=5 en cualquier conjunto; BAJO en los dos, solo en nivel 1."""
    sob = (d1 == "SOBRE") & (d5 == "SOBRE") & validas_ambos[None, :]
    baj = (d1 == "BAJO") & (d5 == "BAJO") & (validas_ambos & es_n1)[None, :]
    return np.where(sob, "SOBRE", np.where(baj, "BAJO", "-")).astype("<U5")


def linea_firme_006(cn, c, lista, n1, g):
    """Rearma la linea QUE_CONTROLA_FIRME de la 006 con el nulo regenerado."""
    sob = []
    for k, O in enumerate(lista):
        if not (g[">=1"]["validas"][k] and g[">=5"]["validas"][k]):
            continue
        if g[">=1"]["flag"][c, k] == "SOBRE" and g[">=5"]["flag"][c, k] == "SOBRE":
            sob.append("%s x%s/x%s (D1 %s/%s%%)"
                       % (O, oc._x(g[">=1"]["enr"][c, k]).strip(), oc._x(g[">=5"]["enr"][c, k]).strip(),
                          oc._p(g[">=1"]["D1"][c, k]).strip(), oc._p(g[">=5"]["D1"][c, k]).strip()))
    baj = [O for k, O in enumerate(lista) if O in n1 and g[">=1"]["flag"][c, k] == "BAJO"
           and g[">=5"]["flag"][c, k] == "BAJO"]
    return "QUE_CONTROLA_FIRME %s: SOBRE: %s | BAJO nivel1: %s" % (cn, ", ".join(sob) or "ninguna",
                                                                   ", ".join(baj) or "ninguna")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Correccion por comparaciones multiples del nulo fuerte (006)")
    ap.add_argument("--parquet", default="/workspace/connectivity.parquet")
    ap.add_argument("--annotations", default="/workspace/annotations.tsv")
    ap.add_argument("--json-006", default="results/output_control_permnull_2026-10-10/output_control_permutation_null.json")
    ap.add_argument("--out", default="results/output_control_permcorr_2026-10-10")
    ap.add_argument("--alfa", type=float, default=ALFA)
    ap.add_argument("--n-falsos", type=int, default=N_FALSOS)
    ap.add_argument("--maquina", default="brain-env")
    args = ap.parse_args(argv)
    t0 = time.time()
    os.makedirs(args.out, exist_ok=True)
    alfa = args.alfa

    def progreso(msg):
        sys.stderr.write("PROGRESO %s t=%.1f\n" % (msg, time.time() - t0))
        sys.stderr.flush()

    with open(args.json_006) as f:
        j6 = json.load(f)
    md5j = oc.md5_archivo(args.json_006)
    par = j6["parametros"]
    seed, R, n_est = int(par["seed"]), int(par["r"]), int(par["n_estratos"])
    ver6 = j6["veredicto"]["nulo"]
    print("== output_control_permutation_correction.py :: correccion por comparaciones multiples del nulo fuerte (006) ==")
    entorno = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
               "pandas": pd.__version__, "maquina": args.maquina}
    print("ENTORNO " + " ".join("%s=%s" % kv for kv in entorno.items()))
    print("PARAMETROS_006 seed=%d r=%d n_estratos=%d veredicto_006=%s | alfa=%g n_falsos=%d factor_control=%g"
          % (seed, R, n_est, ver6, alfa, args.n_falsos, FACTOR_CONTROL))
    md5p = oc.md5_archivo(args.parquet)
    md5a = oc.md5_archivo(args.annotations)
    print("INPUT parquet %s md5=%s pin_ok=%s" % (args.parquet, md5p, md5p == oc.PIN_PARQUET_MD5))
    print("INPUT annotations %s md5=%s pin_ok=%s" % (args.annotations, md5a, md5a == oc.PIN_ANNOT_MD5))
    print("INPUT json_006 %s md5=%s pin_ok=%s" % (args.json_006, md5j, md5j == PIN_JSON_006_MD5))

    pre, post, S, exc, id_of, ginfo = oc.leer_grafo(args.parquet)
    del exc
    print("GRAFO n_nodos=%d n_aristas=%d mapeo_biyectivo=%s"
          % (ginfo["n_nodos"], ginfo["n_aristas"], ginfo["mapeo_biyectivo"]))
    anot = oc.leer_anotaciones(args.annotations, id_of)
    nombres, cls = oc.codificar_clases(anot["super_class"])
    K = len(nombres)
    n = len(id_of)
    n1, n2 = oc.conjuntos_salida(anot["super_class"], anot["cell_sub_class"], anot["cell_type"])
    conjuntos = dict(n1)
    conjuntos.update({k: v for k, v in n2.items() if k not in n1})
    lista = list(conjuntos)
    es_salida = np.zeros(n, dtype=bool)
    for s_ in oc.SALIDAS:
        es_salida[n1[s_]] = True
    es_n1 = np.array([O in n1 for O in lista])
    m_ref = K * len(lista)
    print("RESOLUCION r=%d p_min_bilateral=%.6f tests_por_familia=%d bonferroni=%.6f holm_puede_rechazar=%s"
          % (R, 2.0 / (R + 1.0), m_ref, alfa / m_ref, cc.holm_puede(R, m_ref, alfa)))

    claves = [(e, md, st) for e in (">=1", ">=5") for md in pn.MODOS for st in ESTADISTICOS]
    fams = {}
    cruce = {"clases": list(j6.get("clases_orden", [])) == list(nombres) and list(j6.get("conjuntos", [])) == lista,
             "estratos": True, "d": True, "p": True, "flags": True, "conservacion": True, "firmes": True}
    max_dif = {"d": 0.0, "p": 0.0}
    validas_u = {}
    g006 = {}
    falsos_tot = {mt: 0 for mt in METODOS}
    n_falsos_tot = 0
    for umbral, etq in ((1, ">=1"), (5, ">=5")):
        V_ = pn.vectores_u(pre, post, S, n, umbral, conjuntos)
        _, est, _ = pn.estratos_por_fuerza(V_["p"], V_["q"], V_["s"], n, es_salida, n_est)
        del V_["p"], V_["q"], V_["s"]
        U, m, n_in = V_["U"], V_["m"], V_["n_in"]
        del V_
        tam = np.bincount(est)
        est_ok = tam.tolist() == list(j6["variantes"][etq]["estratos"]["tamanos"])
        cruce["estratos"] = cruce["estratos"] and est_ok
        print("ESTRATOS [%s] n=%d iguales_006=%s" % (etq, len(tam), est_ok))
        D = pn.Sumador(n, K)(cls, U)
        validas = np.array([n_in[O] > 0 for O in lista])
        validas_u[etq] = validas
        pc6 = j6["variantes"][etq]["por_conjunto"]
        d6 = np.array([[pc6[O]["por_clase"][cn][x] for x in ("d1", "d2") for O in lista] for cn in nombres],
                      dtype=np.float64)
        dd = float(np.max(np.abs(d6 - D)))
        max_dif["d"] = max(max_dif["d"], dd)
        cruce["d"] = cruce["d"] and dd <= TOL_CRUCE
        cortes = {"D1": slice(0, m), "D2": slice(m, 2 * m)}
        for mi, md in enumerate(pn.MODOS):
            nul, okc, oke, seg = pn.correr_nulo(cls, est, md, U, K, R, [seed, umbral, mi],
                                                progreso=lambda s, e=etq: progreso("%s %s" % (e, s)))
            E = pn.esperanza(cls, est, U, K, md)
            Vx = pn.varianza_exacta(cls, est, U, K, md)
            cruce["conservacion"] = cruce["conservacion"] and bool(okc and oke)
            fm = {}
            dp = 0.0
            fl_igual = True
            for st in ESTADISTICOS:
                sl = cortes[st]
                fam = corregir(D[:, sl], nul[:, :, sl], E[:, sl], Vx[:, sl], validas, alfa)
                ev = fam["ev"]
                fl = ev["flag"].copy()
                fl[:, ~validas] = "NA"
                suf = st[1]
                ps6 = np.array([[pc6[O]["por_clase"][cn][md]["ps" + suf] for O in lista] for cn in nombres],
                               dtype=np.float64)
                pb6 = np.array([[pc6[O]["por_clase"][cn][md]["pb" + suf] for O in lista] for cn in nombres],
                               dtype=np.float64)
                fl6 = np.array([[pc6[O]["por_clase"][cn][md]["flag" + suf] for O in lista] for cn in nombres])
                dp = max(dp, float(max(np.max(np.abs(ps6 - ev["ps"])), np.max(np.abs(pb6 - ev["pb"])))))
                fl_igual = fl_igual and bool(np.array_equal(fl6, fl))
                fam["flag006"] = fl
                fm[st] = fam
            max_dif["p"] = max(max_dif["p"], dp)
            cruce["p"] = cruce["p"] and dp <= TOL_CRUCE
            cruce["flags"] = cruce["flags"] and fl_igual
            con = falsos(pn.Permutador(cls, est, md), pn.Sumador(n, K), U, nul, E, Vx, fm, cortes, args.n_falsos,
                         [seed, umbral, mi, 98], alfa)
            del nul
            print("NULO [%s] %s R=%d segundos=%.1f d_igual_006=%s p_iguales_006=%s flags_iguales_006=%s"
                  % (etq, md, R, seg, dd <= TOL_CRUCE, dp <= TOL_CRUCE, fl_igual))
            for st in ESTADISTICOS:
                fam = fm[st]
                fam["Z"] = None
                fam["falsos"] = con[st]
                for mt in METODOS:
                    falsos_tot[mt] += con[st][mt]
                n_falsos_tot += args.n_falsos
                fams[(etq, md, st)] = fam
                s6, b6 = cc.contar_sb(fam["flag006"])
                partes = " | ".join("%s SOBRE=%d BAJO=%d" % ((mt,) + cc.contar_sb(fam["decision"][mt]))
                                    for mt in METODOS)
                print("FAMILIA [%s] %s %s m=%d z_crit=%.2f | 006 SOBRE=%d BAJO=%d | %s"
                      % (etq, md, st, fam["m"], fam["z_crit"], s6, b6, partes))
            print("FALSOS [%s] %s n=%d con_rechazo %s"
                  % (etq, md, args.n_falsos, " | ".join("%s %s" % (st, " ".join("%s=%d" % (mt, con[st][mt])
                                                                                   for mt in METODOS))
                                                        for st in ESTADISTICOS)))
        e_ = (etq, "estr", "D1")
        g006[etq] = {"flag": fams[e_]["flag006"], "enr": fams[e_]["ev"]["enr"], "D1": D[:, :m].copy(),
                     "validas": validas}
        del U, D

    e1, e5 = (">=1", "estr", "D1"), (">=5", "estr", "D1")
    va = validas_u[">=1"] & validas_u[">=5"]
    base = firmes_regla_006(fams[e1]["flag006"], fams[e5]["flag006"], va, es_n1)
    f006 = base != "-"
    lineas6 = j6.get("que_controla_firme", {})
    cruce["firmes"] = all(linea_firme_006(cn, c, lista, n1, g006) == lineas6.get(cn) for c, cn in enumerate(nombres))

    print("-- NIVEL1 corregido (nulo estr, D1; orden: >=1, >=5) --")
    for k, O in enumerate(lista):
        if O not in n1:
            continue
        for c, cn in enumerate(nombres):
            zs = "/".join(cc._fz(fams[cl]["z"][c, k]) for cl in (e1, e5))
            pj = {mt: "/".join(cc._fp(fams[cl]["p_aj"][mt][c, k]) for cl in (e1, e5)) for mt in METODOS}
            print("NIVEL1 %-10s %-19s z=%s maxT=%s Holm=%s BH=%s BY=%s"
                  % (O, cn, zs, pj["maxT"], pj["Holm"], pj["BH"], pj["BY"]))

    corr = {mt: firmes_regla_006(fams[e1]["decision"][mt], fams[e5]["decision"][mt], va, es_n1) for mt in METODOS}
    pmax = {}
    for mt in METODOS:
        pila = [np.where(np.isfinite(fams[cl]["p_aj"][mt]), fams[cl]["p_aj"][mt], 1.0) for cl in (e1, e5)]
        pmax[mt] = np.maximum(pila[0], pila[1])
    queda = {mt: f006 & (corr[mt] == base) for mt in METODOS}
    print("-- FIRMES DE LA 006 CON CORRECCION (nulo estr, D1, regla de la 006; p ajustado maximo entre >=1 y >=5;"
          " queda = <= %g en los dos) --" % alfa)
    for c, cn in enumerate(nombres):
        for k, O in enumerate(lista):
            if not f006[c, k]:
                continue
            print("FIRME_006 %-19s -> %-40s %-5s | p_max maxT=%.5f Holm=%.5f BH=%.5f BY=%.5f | queda maxT=%s Holm=%s"
                  " BH=%s BY=%s"
                  % (cn, O, base[c, k], pmax["maxT"][c, k], pmax["Holm"][c, k], pmax["BH"][c, k], pmax["BY"][c, k],
                     *("SI" if queda[mt][c, k] else "NO" for mt in METODOS)))
    for mt in METODOS:
        for c, cn in enumerate(nombres):
            for k, O in enumerate(lista):
                if corr[mt][c, k] != "-" and not f006[c, k]:
                    print("NUEVO_CORREGIDO %-4s %-19s -> %-40s %-5s | p_max=%.5f"
                          % (mt, cn, O, corr[mt][c, k], pmax[mt][c, k]))
    n6 = int(f006.sum())
    s6 = int((base == "SOBRE").sum())
    quedan = {mt: int(queda[mt].sum()) for mt in METODOS}
    nuevos = {mt: int(((corr[mt] != "-") & ~f006).sum()) for mt in METODOS}
    fwer = queda["maxT"] & queda["Holm"]
    fwer2 = fwer & (pmax["maxT"] <= alfa / 2.0) & (pmax["Holm"] <= alfa / 2.0)
    print("RESUMEN firmes_006=%d (SOBRE=%d BAJO=%d) | %s | FWER (maxT y Holm) quedan=%d, con alfa/2=%g quedan=%d"
          % (n6, s6, n6 - s6, " | ".join("%s quedan=%d nuevos=%d" % (mt, quedan[mt], nuevos[mt]) for mt in METODOS),
             int(fwer.sum()), alfa / 2.0, int(fwer2.sum())))

    claves_cons = ("stepdown_le_singlestep", "monotono", "by_ge_bh", "holm_ge_bh", "holm_monotono")
    cons = {k: all(fams[cl]["consistencia"][k] for cl in claves) for k in claves_cons}
    cruce_ok = all(cruce.values())
    cons_ok = all(cons.values())
    esperado = alfa * n_falsos_tot
    tope = max(3.0, FACTOR_CONTROL * esperado)
    ctrl_ok = all(falsos_tot[mt] <= tope for mt in METODOS)
    r_ok = bool(R >= R_MINIMO and ver6 == "PASS")
    print("CRUCE_006 %s %s max_dif_d=%.3g max_dif_p=%.3g"
          % ("PASS" if cruce_ok else "FAIL", " ".join("%s=%s" % kv for kv in cruce.items()), max_dif["d"],
             max_dif["p"]))
    print("CONSISTENCIA %s %s" % ("PASS" if cons_ok else "FAIL", " ".join("%s=%s" % (k, cons[k]) for k in claves_cons)))
    print("CONTROL_NEGATIVO %s esperado=%.1f tope=%.1f OK=%s"
          % (" ".join("%s=%d/%d" % (mt, falsos_tot[mt], n_falsos_tot) for mt in METODOS), esperado, tope, ctrl_ok))
    print("R_PEDIDO_500 r=%d veredicto_006=%s ok=%s" % (R, ver6, r_ok))
    if cruce_ok and cons_ok and ctrl_ok and r_ok:
        ver = "PASS"
    elif cruce_ok and cons_ok and ctrl_ok:
        ver = "INCOMPLETO"
    else:
        ver = "FAIL"

    def celdas(mask, sentido):
        return [[nombres[c], lista[k], str(sentido[c, k])] for c, k in zip(*np.nonzero(mask))]

    res = {"schema": "output_control_permutation_correction/v1", "entorno": entorno, "parametros_006": par,
           "alfa": alfa, "n_falsos": args.n_falsos, "metodos": list(METODOS),
           "inputs": {"parquet_md5": md5p, "annotations_md5": md5a, "json_006": args.json_006, "json_006_md5": md5j},
           "clases_orden": nombres, "conjuntos": lista, "familias": {},
           "firmes": {"006": celdas(f006, base)}, "quedan": quedan, "nuevos": nuevos,
           "fwer_maxT_y_Holm": celdas(fwer, base), "fwer_alfa2": celdas(fwer2, base),
           "cruce_006": cruce, "max_dif": max_dif, "consistencia": cons,
           "control_negativo": {"con_rechazo": falsos_tot, "n": n_falsos_tot, "esperado": esperado, "tope": tope,
                                "ok": ctrl_ok},
           "veredicto": ver}
    for mt in METODOS:
        res["firmes"][mt] = celdas(corr[mt] != "-", corr[mt])
    for cl in claves:
        fam = fams[cl]
        res["familias"]["%s %s %s" % cl] = {"m": fam["m"], "z_crit": fam["z_crit"], "falsos": fam["falsos"],
                                            "consistencia": fam["consistencia"], "z": fam["z"], "p_ss": fam["p_ss"],
                                            "p_aj": fam["p_aj"], "decision": fam["decision"],
                                            "flag006": fam["flag006"], "testeable": fam["testeable"]}
    res["segundos"] = time.time() - t0
    salida = os.path.join(args.out, "output_control_permutation_correction.json")
    with open(salida, "w") as f:
        json.dump(oc.a_py(res), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("JSON %s md5=%s" % (salida, oc.md5_archivo(salida)))
    print("VEREDICTO_CORRECCION %s" % ver)
    print("FIN_CORRECCION segundos=%.1f" % (time.time() - t0))
    return 0 if ver in ("PASS", "INCOMPLETO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
