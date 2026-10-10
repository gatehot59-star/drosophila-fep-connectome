#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
output_control_region_correction.py :: correccion por comparaciones multiples del nulo regional (007).

Pedido 2026-10-10 (Abraham): "Apply multiple-comparisons correction to the regional null".

La 007 marco cada test (clase x conjunto de salida) con p <= 0,001 de cada lado, sin corregir por la
cantidad de tests: 242 con >=1 y 231 con >=5, cada uno con dos granularidades de region. Aca:

  1. Se regenera el nulo de la 007 con sus mismas semillas y parametros (leidos de su JSON) y se exige
     que regiones, D1, p y flags de cada test salgan identicos (CRUCE_007).
  2. FWER: Westfall-Young step-down sobre max |z|, con z = (D1 - E) / sd y E, sd exactas del nulo. Usa
     la distribucion conjunta de las permutaciones, asi que vale con cualquier dependencia entre tests
     (y la hay: las 11 clases de un conjunto suman 1).
  3. FDR: Benjamini-Hochberg y Benjamini-Yekutieli (este vale con dependencia arbitraria) sobre el p
     bilateral de permutacion, min(1, 2 x min(p_sobre, p_bajo)).
  4. Familia = los tests de un umbral y una granularidad cuyo nulo varia (sd > 0). Firme corregido = el
     mismo sentido significativo (ajustado <= alfa) en las cuatro familias.

Holm y Bonferroni sobre los p de permutacion no sirven con R = 5.000: el p bilateral minimo es
2 / 5.001 = 0,0004, mayor que 0,05 / m con m > 125 tests. Se informa en RESOLUCION y no se usa.

Controles que pueden dar rojo:
  CRUCE_007         regiones, D1, p y flags de cada test identicos a los de la 007.
  CONSISTENCIA      step-down <= single-step, ajustados monotonos en el orden de |z|, BY >= BH.
  CONTROL_NEGATIVO  etiquetados falsos del mismo nulo con la misma correccion: los que tienen algun
                    rechazo no pasan de max(3, 3 x alfa x n) por metodo, sumando las cuatro familias.
  R_PEDIDO_500      con R < 500 en la 007, o una 007 que no dio PASS, el veredicto no puede ser PASS.
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
import output_control_region_null as rn  # noqa: E402

ALFA = 0.05
N_FALSOS = 20
R_MINIMO = 500
FACTOR_CONTROL = 3.0
SD_MIN = 1e-12
TOL_CRUCE = 1e-12
METODOS = ("maxT", "BH", "BY")
PIN_JSON_007_MD5 = "72427fdc69a583ca796f448f6aaae0a5"


def p_bilateral(ps, pb):
    return np.minimum(1.0, 2.0 * np.minimum(ps, pb))


def holm_puede(R, m, alfa=ALFA):
    """Con R permutaciones el p bilateral minimo es 2 / (R + 1); Holm rechaza algo solo si es <= alfa / m."""
    return bool(2.0 / (R + 1.0) <= alfa / m)


def bh(p):
    """q de Benjamini-Hochberg (step-up), devuelto en el orden de entrada."""
    p = np.asarray(p, dtype=np.float64)
    m = len(p)
    if m == 0:
        return p.copy()
    o = np.argsort(p, kind="stable")
    q = p[o] * m / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(m)
    out[o] = np.minimum(q, 1.0)
    return out


def by(p):
    """Benjamini-Yekutieli: BH por c(m) = sum_i 1/i; vale con dependencia arbitraria."""
    m = len(p)
    c = float(np.sum(1.0 / np.arange(1, m + 1))) if m else 1.0
    return np.minimum(1.0, bh(p) * c)


def maxt_stepdown(t_obs, Z):
    """Westfall-Young sobre max |z|. t_obs (m,) observados; Z (R, m) del nulo. El observado cuenta como
    una permutacion mas. Devuelve (p step-down, p single-step)."""
    t_obs = np.asarray(t_obs, dtype=np.float64)
    R, m = Z.shape
    if m == 0:
        return np.empty(0), np.empty(0)
    o = np.argsort(-t_obs, kind="stable")
    cola = np.maximum.accumulate(Z[:, o][:, ::-1], axis=1)[:, ::-1]
    p_sd = np.maximum.accumulate((1.0 + (cola >= t_obs[o][None, :]).sum(axis=0)) / (R + 1.0))
    out = np.empty(m)
    out[o] = p_sd
    mx = Z.max(axis=1)
    p_ss = (1.0 + (mx[:, None] >= t_obs[None, :]).sum(axis=0)) / (R + 1.0)
    return out, p_ss


def corregir_familia(D1, nul, E, V, validas, alfa=ALFA):
    """Una familia (umbral x granularidad). D1, E, V: (K, m); nul: (R, K, m); validas: (m,)."""
    K, m = D1.shape
    R = nul.shape[0]
    ev = pn.evaluar_nulo(D1, nul)
    sd = np.sqrt(np.maximum(V, 0.0))
    varia = nul.max(axis=0) > nul.min(axis=0)
    test = (sd > SD_MIN) & varia & np.asarray(validas, dtype=bool)[None, :]
    idx = np.flatnonzero(test.ravel())
    e = E.ravel()[idx]
    s = sd.ravel()[idx]
    z = np.full(K * m, np.nan)
    z[idx] = (D1.ravel()[idx] - e) / s
    Z = np.abs(nul.reshape(R, K * m)[:, idx] - e[None, :]) / s[None, :]
    p_sd, p_ss = maxt_stepdown(np.abs(z[idx]), Z)
    p2 = p_bilateral(ev["ps"], ev["pb"]).ravel()[idx]
    aj = {"maxT": p_sd, "BH": bh(p2), "BY": by(p2)}
    sube = ev["ps"].ravel()[idx] < ev["pb"].ravel()[idx]
    sentido = {"maxT": np.where(z[idx] > 0, "SOBRE", "BAJO"), "BH": np.where(sube, "SOBRE", "BAJO"),
               "BY": np.where(sube, "SOBRE", "BAJO")}
    out = {"ev": ev, "testeable": test, "m": int(len(idx)), "idx": idx, "Z": Z, "z": z.reshape(K, m),
           "z_crit": float(np.quantile(Z.max(axis=1), 1.0 - alfa)) if len(idx) else float("nan"),
           "p_aj": {}, "decision": {}}
    pss = np.full(K * m, np.nan)
    pss[idx] = p_ss
    out["p_ss"] = pss.reshape(K, m)
    for mt in METODOS:
        pa = np.full(K * m, np.nan)
        pa[idx] = aj[mt]
        dec = np.full(K * m, "-", dtype="<U5")
        dec[idx] = np.where(aj[mt] <= alfa, sentido[mt], "-")
        out["p_aj"][mt] = pa.reshape(K, m)
        out["decision"][mt] = dec.reshape(K, m)
    o = np.argsort(-np.abs(z[idx]), kind="stable")
    out["consistencia"] = {"stepdown_le_singlestep": bool(np.all(p_sd <= p_ss + 1e-15)),
                           "monotono": bool(np.all(np.diff(p_sd[o]) >= -1e-15)),
                           "by_ge_bh": bool(np.all(aj["BY"] >= aj["BH"] - 1e-15))}
    return out


def falsos(cls, est, U, K, nul, E, V, fam, n_falsos, semilla, alfa=ALFA):
    """Etiquetados falsos del mismo nulo, corregidos igual que el real: cuantos tienen algun rechazo."""
    perm = rn.PermutadorRapido(cls, est)
    sumar = pn.Sumador(len(cls), K)
    rng = np.random.default_rng(semilla)
    idx = fam["idx"]
    e = E.ravel()[idx]
    s = np.sqrt(np.maximum(V, 0.0)).ravel()[idx]
    con = {mt: 0 for mt in METODOS}
    for _ in range(n_falsos):
        D = sumar(perm(rng), U)
        p_sd, _ = maxt_stepdown(np.abs(D.ravel()[idx] - e) / s, fam["Z"])
        ev = pn.evaluar_nulo(D, nul)
        p2 = p_bilateral(ev["ps"], ev["pb"]).ravel()[idx]
        aj = {"maxT": p_sd, "BH": bh(p2), "BY": by(p2)}
        for mt in METODOS:
            con[mt] += int((aj[mt] <= alfa).any())
    return con


def contar_sb(a):
    return int((a == "SOBRE").sum()), int((a == "BAJO").sum())


def _fz(x):
    return "-" if not np.isfinite(x) else "%+.1f" % x


def _fp(x):
    return "-" if not np.isfinite(x) else "%.4f" % x


def main(argv=None):
    ap = argparse.ArgumentParser(description="Correccion por comparaciones multiples del nulo regional (007)")
    ap.add_argument("--parquet", default="/workspace/connectivity.parquet")
    ap.add_argument("--annotations", default="/workspace/annotations.tsv")
    ap.add_argument("--json-007", default="results/output_control_regionnull_2026-10-10/output_control_region_null.json")
    ap.add_argument("--out", default="results/output_control_regioncorr_2026-10-10")
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

    with open(args.json_007) as f:
        j7 = json.load(f)
    md5j = oc.md5_archivo(args.json_007)
    par = j7["parametros"]
    seed, R, n_tam = int(par["seed"]), int(par["r"]), int(par["n_tam"])
    ks = [int(k) for k in par["k_regiones"]]
    modos = ["reg%d" % k for k in ks]
    ver7 = j7["veredicto"]["nulo"]
    print("== output_control_region_correction.py :: correccion por comparaciones multiples del nulo regional (007) ==")
    entorno = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
               "pandas": pd.__version__, "maquina": args.maquina}
    print("ENTORNO " + " ".join("%s=%s" % kv for kv in entorno.items()))
    print("PARAMETROS_007 seed=%d r=%d k_regiones=%s n_tam=%d veredicto_007=%s | alfa=%g n_falsos=%d factor_control=%g"
          % (seed, R, ",".join(str(k) for k in ks), n_tam, ver7, alfa, args.n_falsos, FACTOR_CONTROL))
    md5p = oc.md5_archivo(args.parquet)
    md5a = oc.md5_archivo(args.annotations)
    print("INPUT parquet %s md5=%s pin_ok=%s" % (args.parquet, md5p, md5p == oc.PIN_PARQUET_MD5))
    print("INPUT annotations %s md5=%s pin_ok=%s" % (args.annotations, md5a, md5a == oc.PIN_ANNOT_MD5))
    print("INPUT json_007 %s md5=%s pin_ok=%s" % (args.json_007, md5j, md5j == PIN_JSON_007_MD5))

    pre, post, S, exc, id_of, ginfo = oc.leer_grafo(args.parquet)
    del exc
    print("GRAFO n_nodos=%d n_aristas=%d mapeo_biyectivo=%s"
          % (ginfo["n_nodos"], ginfo["n_aristas"], ginfo["mapeo_biyectivo"]))
    anot = oc.leer_anotaciones(args.annotations, id_of)
    nombres, cls = oc.codificar_clases(anot["super_class"])
    K = len(nombres)
    n = len(id_of)
    X, tiene = rn.leer_posiciones(args.annotations, id_of)
    regs = {}
    reg_ok = list(j7.get("clases_orden", [])) == list(nombres)
    for k, md in zip(ks, modos):
        reg, info = rn.regiones(X, tiene, k, [seed, k])
        regs[md] = reg
        igual = np.asarray(info["tamanos"]).tolist() == list(j7["regiones"][md]["tamanos"])
        reg_ok = reg_ok and igual
        print("REGIONES k=%d iteraciones=%d iguales_007=%s" % (k, info["iteraciones"], igual))
    n1, n2 = oc.conjuntos_salida(anot["super_class"], anot["cell_sub_class"], anot["cell_type"])
    conjuntos = dict(n1)
    conjuntos.update({k: v for k, v in n2.items() if k not in n1})
    lista = list(conjuntos)
    reg_ok = reg_ok and list(j7.get("conjuntos", [])) == lista
    es_salida = np.zeros(n, dtype=bool)
    for s_ in oc.SALIDAS:
        es_salida[n1[s_]] = True
    m_ref = K * len(lista)
    print("RESOLUCION r=%d p_min_bilateral=%.6f tests_por_familia=%d bonferroni=%.6f holm_puede_rechazar=%s"
          % (R, 2.0 / (R + 1.0), m_ref, alfa / m_ref, holm_puede(R, m_ref, alfa)))

    claves = [(e, md) for e in (">=1", ">=5") for md in modos]
    fams = {}
    cruce = {"regiones": bool(reg_ok), "d1": True, "p": True, "flags": True, "conservacion": True}
    max_dif = {"d1": 0.0, "p": 0.0}
    validas_u = {}
    falsos_tot = {mt: 0 for mt in METODOS}
    n_falsos_tot = 0
    for umbral, etq in ((1, ">=1"), (5, ">=5")):
        V_ = pn.vectores_u(pre, post, S, n, umbral, conjuntos)
        _, tam, _ = pn.estratos_por_fuerza(V_["p"], V_["q"], V_["s"], n, es_salida, n_tam)
        del V_["p"], V_["q"], V_["s"]
        m, n_in = V_["m"], V_["n_in"]
        U1 = np.ascontiguousarray(V_["U"][:, :m])
        del V_
        D1 = pn.Sumador(n, K)(cls, U1)
        validas = np.array([n_in[O] > 0 for O in lista])
        validas_u[etq] = validas
        pc7 = j7["variantes"][etq]["por_conjunto"]
        d17 = np.array([[pc7[O]["por_clase"][cn]["d1"] for O in lista] for cn in nombres], dtype=np.float64)
        dd = float(np.max(np.abs(d17 - D1)))
        max_dif["d1"] = max(max_dif["d1"], dd)
        cruce["d1"] = cruce["d1"] and dd <= TOL_CRUCE
        for mi, md in enumerate(modos):
            est = rn.combinar(regs[md], tam)
            nul, okc, oke, seg = rn.correr_nulo_rapido(cls, est, U1, K, R, [seed, umbral, mi], progreso=progreso,
                                                       etiqueta="%s %s" % (etq, md))
            E = pn.esperanza(cls, est, U1, K, "estr")
            Vx = pn.varianza_exacta(cls, est, U1, K, "estr")
            fam = corregir_familia(D1, nul, E, Vx, validas, alfa)
            ev = fam["ev"]
            fl = ev["flag"].copy()
            fl[:, ~validas] = "NA"
            ps7 = np.array([[pc7[O]["por_clase"][cn][md]["ps"] for O in lista] for cn in nombres], dtype=np.float64)
            pb7 = np.array([[pc7[O]["por_clase"][cn][md]["pb"] for O in lista] for cn in nombres], dtype=np.float64)
            fl7 = np.array([[pc7[O]["por_clase"][cn][md]["flag"] for O in lista] for cn in nombres])
            dp = float(max(np.max(np.abs(ps7 - ev["ps"])), np.max(np.abs(pb7 - ev["pb"]))))
            fl_igual = bool(np.array_equal(fl7, fl))
            max_dif["p"] = max(max_dif["p"], dp)
            cruce["p"] = cruce["p"] and dp <= TOL_CRUCE
            cruce["flags"] = cruce["flags"] and fl_igual
            cruce["conservacion"] = cruce["conservacion"] and bool(okc and oke)
            con = falsos(cls, est, U1, K, nul, E, Vx, fam, args.n_falsos, [seed, umbral, mi, 98], alfa)
            for mt in METODOS:
                falsos_tot[mt] += con[mt]
            n_falsos_tot += args.n_falsos
            del nul
            fam["Z"] = None
            fam["flag007"] = fl
            fam["falsos"] = con
            fams[(etq, md)] = fam
            s7, b7 = contar_sb(fl)
            partes = " | ".join("%s SOBRE=%d BAJO=%d" % ((mt,) + contar_sb(fam["decision"][mt])) for mt in METODOS)
            print("NULO [%s] %s R=%d segundos=%.1f d1_igual_007=%s p_iguales_007=%s flags_iguales_007=%s"
                  % (etq, md, R, seg, dd <= TOL_CRUCE, dp <= TOL_CRUCE, fl_igual))
            print("FAMILIA [%s] %s m=%d z_crit=%.2f | 007 SOBRE=%d BAJO=%d | %s"
                  % (etq, md, fam["m"], fam["z_crit"], s7, b7, partes))
            print("FALSOS [%s] %s n=%d con_rechazo %s"
                  % (etq, md, args.n_falsos, " ".join("%s=%d" % (mt, con[mt]) for mt in METODOS)))

    print("-- NIVEL1 corregido (orden: %s) --" % ", ".join("%s %s" % cl for cl in claves))
    for k, O in enumerate(lista):
        if O not in n1:
            continue
        for c, cn in enumerate(nombres):
            zs = "/".join(_fz(fams[cl]["z"][c, k]) for cl in claves)
            pj = {mt: "/".join(_fp(fams[cl]["p_aj"][mt][c, k]) for cl in claves) for mt in METODOS}
            print("NIVEL1 %-10s %-19s z=%s maxT=%s BH=%s BY=%s" % (O, cn, zs, pj["maxT"], pj["BH"], pj["BY"]))

    validas_ambos = validas_u[">=1"] & validas_u[">=5"]

    def firme(decs):
        base = decs[0]
        igual = np.ones(base.shape, dtype=bool)
        for d in decs[1:]:
            igual &= d == base
        return igual & np.isin(base, ("SOBRE", "BAJO")) & validas_ambos[None, :]

    f007 = firme([fams[cl]["flag007"] for cl in claves])
    sent7 = fams[claves[0]]["flag007"]
    fM = {mt: firme([fams[cl]["decision"][mt] for cl in claves]) for mt in METODOS}
    pmax = {}
    for mt in METODOS:
        pila = [np.where(np.isfinite(fams[cl]["p_aj"][mt]), fams[cl]["p_aj"][mt], 1.0) for cl in claves]
        pmax[mt] = np.max(np.stack(pila), axis=0)
    queda = {mt: f007 & fM[mt] & (fams[claves[0]]["decision"][mt] == sent7) for mt in METODOS}
    print("-- FIRMES DE LA 007 CON CORRECCION (p ajustado maximo entre las cuatro familias; queda = <= %g en las cuatro) --"
          % alfa)
    for c, cn in enumerate(nombres):
        for k, O in enumerate(lista):
            if not f007[c, k]:
                continue
            print("FIRME_007 %-19s -> %-40s %-5s | p_max maxT=%.5f BH=%.5f BY=%.5f | queda maxT=%s BH=%s BY=%s"
                  % (cn, O, sent7[c, k], pmax["maxT"][c, k], pmax["BH"][c, k], pmax["BY"][c, k],
                     *("SI" if queda[mt][c, k] else "NO" for mt in METODOS)))
    for mt in METODOS:
        for c, cn in enumerate(nombres):
            for k, O in enumerate(lista):
                if fM[mt][c, k] and not f007[c, k]:
                    print("NUEVO_CORREGIDO %-4s %-19s -> %-40s %-5s | p_max=%.5f"
                          % (mt, cn, O, fams[claves[0]]["decision"][mt][c, k], pmax[mt][c, k]))
    n7 = int(f007.sum())
    s7 = int((f007 & (sent7 == "SOBRE")).sum())
    quedan = {mt: int(queda[mt].sum()) for mt in METODOS}
    nuevos = {mt: int((fM[mt] & ~f007).sum()) for mt in METODOS}
    q4 = int((queda["maxT"] & (pmax["maxT"] <= alfa / 4.0)).sum())
    print("RESUMEN firmes_007=%d (SOBRE=%d BAJO=%d) | %s | maxT con alfa/4=%g quedan=%d"
          % (n7, s7, n7 - s7, " | ".join("%s quedan=%d nuevos=%d" % (mt, quedan[mt], nuevos[mt]) for mt in METODOS),
             alfa / 4.0, q4))

    cons = {k: all(fams[cl]["consistencia"][k] for cl in claves)
            for k in ("stepdown_le_singlestep", "monotono", "by_ge_bh")}
    cruce_ok = all(cruce.values())
    cons_ok = all(cons.values())
    esperado = alfa * n_falsos_tot
    tope = max(3.0, FACTOR_CONTROL * esperado)
    ctrl_ok = all(falsos_tot[mt] <= tope for mt in METODOS)
    r_ok = bool(R >= R_MINIMO and ver7 == "PASS")
    print("CRUCE_007 %s regiones=%s d1=%s p=%s flags=%s conservacion=%s max_dif_d1=%.3g max_dif_p=%.3g"
          % ("PASS" if cruce_ok else "FAIL", cruce["regiones"], cruce["d1"], cruce["p"], cruce["flags"],
             cruce["conservacion"], max_dif["d1"], max_dif["p"]))
    print("CONSISTENCIA %s stepdown_le_singlestep=%s monotono=%s by_ge_bh=%s"
          % ("PASS" if cons_ok else "FAIL", cons["stepdown_le_singlestep"], cons["monotono"], cons["by_ge_bh"]))
    print("CONTROL_NEGATIVO %s esperado=%.1f tope=%.1f OK=%s"
          % (" ".join("%s=%d/%d" % (mt, falsos_tot[mt], n_falsos_tot) for mt in METODOS), esperado, tope, ctrl_ok))
    print("R_PEDIDO_500 r=%d veredicto_007=%s ok=%s" % (R, ver7, r_ok))
    if cruce_ok and cons_ok and ctrl_ok and r_ok:
        ver = "PASS"
    elif cruce_ok and cons_ok and ctrl_ok:
        ver = "INCOMPLETO"
    else:
        ver = "FAIL"

    def celdas(mask, sentido):
        return [[nombres[c], lista[k], str(sentido[c, k])] for c, k in zip(*np.nonzero(mask))]

    res = {"schema": "output_control_region_correction/v1", "entorno": entorno, "parametros_007": par,
           "alfa": alfa, "n_falsos": args.n_falsos, "metodos": list(METODOS),
           "inputs": {"parquet_md5": md5p, "annotations_md5": md5a, "json_007": args.json_007, "json_007_md5": md5j},
           "clases_orden": nombres, "conjuntos": lista, "familias": {},
           "firmes": {"007": celdas(f007, sent7)}, "quedan": quedan, "nuevos": nuevos, "quedan_maxT_alfa4": q4,
           "cruce_007": cruce, "max_dif": max_dif, "consistencia": cons,
           "control_negativo": {"con_rechazo": falsos_tot, "n": n_falsos_tot, "esperado": esperado, "tope": tope,
                                "ok": ctrl_ok},
           "veredicto": ver}
    for mt in METODOS:
        res["firmes"][mt] = celdas(fM[mt], fams[claves[0]]["decision"][mt])
    for cl in claves:
        fam = fams[cl]
        res["familias"]["%s %s" % cl] = {"m": fam["m"], "z_crit": fam["z_crit"], "falsos": fam["falsos"],
                                         "consistencia": fam["consistencia"], "z": fam["z"], "p_ss": fam["p_ss"],
                                         "p_aj": fam["p_aj"], "decision": fam["decision"],
                                         "flag007": fam["flag007"], "testeable": fam["testeable"]}
    res["segundos"] = time.time() - t0
    salida = os.path.join(args.out, "output_control_region_correction.json")
    with open(salida, "w") as f:
        json.dump(oc.a_py(res), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("JSON %s md5=%s" % (salida, oc.md5_archivo(salida)))
    print("VEREDICTO_CORRECCION %s" % ver)
    print("FIN_CORRECCION segundos=%.1f" % (time.time() - t0))
    return 0 if ver in ("PASS", "INCOMPLETO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
