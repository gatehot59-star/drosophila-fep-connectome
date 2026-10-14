#!/usr/bin/env python3
"""Nucleo conservado de R2 en el banco de la mosca (respuesta 2026-10-14-002). Sellado antes de correr.

Pregunta (H_CONSENSO, 2026-10-13-018). Si las conexiones que se repiten entre moscas son las que cargan el reflejo,
el nucleo conservado de R2 tiene que rendir como R2 entero (sin perder mas de 1 punto) con una fraccion de las
aristas, y ganarle a sus barajados.
Nucleo (regla de Schlegel et al., Nature 2024, como aproximacion dentro de FlyWire): de las aristas de R2 quedan las
de 10 sinapsis o mas, o las que pesan mas del 1 % de la entrada total de su neurona post, contada sobre todo
FlyWire 783. Mismas 33.489 neuronas, mismas 564 entradas, mismas 6 descendentes, mismo signo y peso por arista; el
radio espectral se vuelve a llevar a 0,9 sobre el nucleo, como en R2 y en el cerebro entero.
Modos:
  construir  arma el nucleo, imprime su tamano y lo guarda aparte (parquet con root_id pre, root_id post y peso con
             signo), sin simular: es la pieza suelta. La huella es el md5 de las tres columnas en int64.
  grilla     el banco del factorial 3 con el nucleo en lugar de R2 (mismas semillas de tau, de prueba y celdas), para
             parear corrida por corrida con R2 en results/factorial3_2026-10-13.
  nulos      SL y T del nucleo, como tools/factorial3/nulos_r2.py pero sobre las aristas del nucleo, en A 0,3,
             ruido 0,15, tau 0 y prueba 2; con --real mide tambien el nucleo real por el mismo camino.
La simulacion, el lector y los datos son los de tools/factorial2/factorial2_mosca.py (md5 798a824c) y el barajado
SL el de tools/factorial3/nulos_r2.py (md5 c4f1c4d3), importados sin cambios; la regla propia se arma como en
factorial2_mosca.py (lc y regla, copiadas linea por linea).
Nucleo sellado (medido con --modo construir en brain-env, 2026-10-14): 603.219 de las 4.031.897 aristas de R2
(14,96 %), 260.173 inhibitorias, 9.668.248 de 16.971.919 sinapsis (56,97 %), las 6 descendentes con entrada y 563 de
las 564 entradas con salida; huella 69255109562f8a93270c435acdde2239.
Controles: pin de md5 (insumos y modulos); R2_tamano; NUCLEO_tamano (aristas, inhibitorias y huella iguales a las
selladas; sin sello solo corre construir); por nulo, las guardas de nulos_r2.py.
Salida: 0 completo; 2 insumos distintos del pin; 3 control fallido o nucleo sin sellar.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "factorial2"))
sys.path.insert(0, os.path.join(AQUI, "..", "factorial3"))
import factorial2_mosca as f2  # noqa: E402  sellado (798a824c), sin cambios
import nulos_r2 as n3  # noqa: E402  sellado (c4f1c4d3), sin cambios

tm, base = f2.tm, f2.base
MD5_F2 = "798a824cd47808155fa12adb9e652dac"
MD5_N3 = "c4f1c4d39c99f07cb9ad7977b6f3b01a"
SIN_MIN, FRAC_MIN = 10, 0.01
NUCLEO_ESPERADO = (603219, 260173, "69255109562f8a93270c435acdde2239")
CELDA_N, TAU_N, PRUEBA_N = (0.3, 0.15), 0, 2


def pr(s):
    print(s, flush=True)


def clave(A, s):
    return "%.1f|%.2f" % (A, s)


def entrada_total(conn_p):
    c = pd.read_parquet(conn_p, columns=["Postsynaptic_ID", "Connectivity"])
    return c.groupby("Postsynaptic_ID").Connectivity.sum()


def nucleo_schlegel(sin, total_post):
    """Aristas con 10 sinapsis o mas, o con mas del 1 % de la entrada total de su neurona post."""
    return (sin >= SIN_MIN) | (sin > FRAC_MIN * total_post)


def huella(pre, post, peso):
    x = np.ascontiguousarray(np.stack([pre, post, peso]).astype(np.int64))
    return hashlib.md5(x.tobytes()).hexdigest()


def sujeto_nucleo(conn_p, annot_p):
    S = f2.sujeto(conn_p, annot_p, "R2", "CON")
    ids = np.array(S["ids"], dtype=np.int64)
    p, q, w = S["aristas"]
    tpost = entrada_total(conn_p).reindex(ids[q]).to_numpy(dtype=np.float64)
    sin = np.abs(w)
    m = nucleo_schlegel(sin, tpost)
    n, n_ent = len(ids), S["n_ent"]
    info = dict(neuronas=int(n), entradas=int(n_ent), aristas_R2=int(len(w)), aristas=int(m.sum()),
                inhibitorias=int((w[m] < 0).sum()), inhibitorias_R2=int((w < 0).sum()),
                por_10_sinapsis=int((sin >= SIN_MIN).sum()), por_1pc_entrada=int((sin > FRAC_MIN * tpost).sum()),
                sinapsis_R2=int(sin.sum()), sinapsis=int(sin[m].sum()),
                dn_con_entrada=int(len(set(q[m].tolist()) & set(range(n - 6, n)))),
                entradas_con_salida=int(len(set(p[m].tolist()) & set(range(n_ent)))),
                post_sin_total=int(np.isnan(tpost).sum()),
                huella=huella(ids[p[m]], ids[q[m]], w[m]))
    return S, m, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--modo", required=True, choices=("construir", "grilla", "nulos"))
    ap.add_argument("--taus", default="0,1,2,3,4,5,6,7,8,9")
    ap.add_argument("--pruebas", default="2,3,4,5,6,7,8,9,10,11")
    ap.add_argument("--celdas", default="todas", help="todas o lista A|ruido separada por coma")
    ap.add_argument("--etiqueta", default="")
    ap.add_argument("--tipo", choices=("SL", "T"))
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--real", action="store_true")
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s | pandas %s" % (platform.node(), platform.platform(),
       platform.python_version(), np.__version__, pd.__version__))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    m2, m3, mt = base.md5(os.path.abspath(f2.__file__)), base.md5(os.path.abspath(n3.__file__)), base.md5(
        os.path.abspath(tm.__file__))
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 factorial2_mosca = %s | md5 nulos_r2 = %s | md5 modulo 015 = %s | md5 conn = %s | md5 annot = %s" % (
        m2, m3, mt, mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mt != f2.MD5_TM or m2 != MD5_F2 or m3 != MD5_N3:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    tr = time.time()
    S, m, info = sujeto_nucleo(a.conn, a.annot)
    ids, tipos, lados = S["ids"], S["tipos"], S["lados"]
    n, n_ent, nv46 = len(ids), S["n_ent"], S["nv46"]
    p, q, w = S["aristas"]
    guardas = {"R2_tamano": bool((S["n_U"], S["n_ar_crudo"]) == f2.R2_ESPERADO and S["contiene_m46"] and
                                 S["contiene_r1"])}
    pr("SUJETO R2 neuronas=%d aristas=%d entradas=%d -> %s | %.1f s" % (S["n_U"], S["n_ar_crudo"], n_ent,
                                                                      guardas["R2_tamano"], time.time() - tr))
    pr("NUCLEO aristas=%d de %d (%.2f %%) inhibitorias=%d de %d | por_10_sinapsis=%d por_1pc_entrada=%d | sinapsis=%d "
       "de %d (%.2f %%) | DN_con_entrada=%d/6 entradas_con_salida=%d/%d | post_sin_total=%d | huella=%s" % (
           info["aristas"], info["aristas_R2"], 100.0 * info["aristas"] / info["aristas_R2"], info["inhibitorias"],
           info["inhibitorias_R2"], info["por_10_sinapsis"], info["por_1pc_entrada"], info["sinapsis"],
           info["sinapsis_R2"], 100.0 * info["sinapsis"] / info["sinapsis_R2"], info["dn_con_entrada"],
           info["entradas_con_salida"], n_ent, info["post_sin_total"], info["huella"]))
    if NUCLEO_ESPERADO is None:
        if a.modo != "construir":
            pr("ABORTA: el nucleo no esta sellado; solo corre --modo construir")
            pr("EXIT_RUN=3")
            return 3
        pr("# NUCLEO_ESPERADO sin fijar: este construir es el que lo fija")
    else:
        guardas["NUCLEO_tamano"] = bool((info["aristas"], info["inhibitorias"], info["huella"]) == NUCLEO_ESPERADO)
        pr("CHEQUEO NUCLEO_tamano esperado=%s -> %s" % (NUCLEO_ESPERADO, guardas["NUCLEO_tamano"]))
    res = dict(modo=a.modo, humo=humo, nucleo=info, regla_nucleo="sinapsis >= %d o sinapsis > %.2f * entrada_total_post"
               % (SIN_MIN, FRAC_MIN), n_ent=n_ent, dns_root=[int(r) for r in ids[n - 6:]],
               md5=dict(script=base.md5(os.path.abspath(__file__)), factorial2=m2, nulos_r2=m3, modulo015=mt, conn=mc,
                        annot=ma))
    if a.modo == "construir":
        ruta_pq = os.path.join(a.out, "nucleo_R2_schlegel.parquet")
        pd.DataFrame({"pre_root_id": np.array(ids, dtype=np.int64)[p[m]], "post_root_id": np.array(ids, dtype=np.int64)[q[m]],
                      "peso": w[m].astype(np.int64)}).to_parquet(ruta_pq, index=False)
        res["parquet_md5"] = base.md5(ruta_pq)
        pr("escrito %s md5=%s (la identidad del nucleo es la huella, no el md5 del parquet)" % (
            os.path.basename(ruta_pq), res["parquet_md5"]))
        ruta = os.path.join(a.out, "nucleo_R2_resumen.json")
    else:
        W, radio = f2.matriz(n, (p[m], q[m], w[m]), densa_ok=False)
        res["radio_crudo"] = radio
        pr("RADIO nucleo crudo=%.6f" % radio)
        n_train, n_test = (120, 80) if humo else (tm.N_TRAIN, tm.N_TEST)
        chan = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(n_ent)])
        etr = tm.generar(n_train, f2.SEM_GEN_TR)
        ytr, vtr = etr["y"], etr["vuelo"]
        Ztr = f2.ruido_por_root(ids[:n_ent], n_train, f2.SEM_RUIDO_TR)
        if a.modo == "grilla":
            taus = [int(x) for x in a.taus.split(",")]
            pruebas = [int(x) for x in a.pruebas.split(",")]
            celdas = f2.CELDAS if a.celdas == "todas" else [tuple(float(v) for v in x.split("|"))
                                                            for x in a.celdas.split(",")]

            def media(X, ld, ts, k):
                mm = np.array([lados[i] == ld and tipos[i] in ts for i in range(k)])
                return X[:, :, mm].mean(2)

            def lc(d, k):
                X = d["drive"][:, :, chan[:k]] + d["ruido"][:, :, :k]
                return np.stack([media(X, "L", ("LC4", "LPLC2"), k), media(X, "R", ("LC4", "LPLC2"), k),
                                 media(X, "L", ("LPLC4",), k), media(X, "R", ("LPLC4",), k),
                                 media(X, "L", ("LPLC1", "LPLC2"), k), media(X, "R", ("LPLC1", "LPLC2"), k)], axis=2)

            def regla(dtr, dte, vte, k):
                th = tm.umbrales(tm.lineas(lc(dtr, k)), ytr, vtr)
                return tm.carrera(tm.lineas(lc(dte, k)), th, vte)

            tau_s = {st: f2.tau_por_root(ids, st) for st in taus}
            res.update(taus=taus, pruebas=pruebas, celdas=[clave(*c) for c in celdas], etiqueta=a.etiqueta,
                       tau_DN={str(st): [float(x) for x in tau_s[st][n - 6:]] for st in taus}, corridas=[], reglas=[])
            pr("# grilla taus=%s pruebas=%s celdas=%s etiqueta=%s" % (taus, pruebas, res["celdas"], a.etiqueta or "-"))
            for A, s in celdas:
                tc = time.time()
                dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr)
                th = {st: tm.umbrales(tm.lineas(f2.sim_trozos(W, tau_s[st], n_ent, chan, dtr, False)), ytr, vtr)
                      for st in taus}
                for sem in pruebas:
                    ete = tm.generar(n_test, sem)
                    yte, vte = ete["y"], ete["vuelo"]
                    Zte = f2.ruido_por_root(ids[:n_ent], n_test, 1000 + sem)
                    dte = dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * Zte)
                    pP, p40 = regla(dtr, dte, vte, n_ent), regla(dtr, dte, vte, nv46)
                    aP, a40 = float((pP == yte).mean()), float((p40 == yte).mean())
                    res["reglas"].append(dict(celda=clave(A, s), prueba=sem, regla_propia=aP, regla40=a40,
                                              pred_regla_propia="".join(map(str, pP.tolist()))))
                    for st in taus:
                        pW = tm.carrera(tm.lineas(f2.sim_trozos(W, tau_s[st], n_ent, chan, dte, False)), th[st], vte)
                        aW = float((pW == yte).mean())
                        res["corridas"].append(dict(celda=clave(A, s), tau=st, prueba=sem, W=aW, regla_propia=aP,
                                                    regla40=a40, pred_W="".join(map(str, pW.tolist()))))
                        pr("CORRIDA celda=%s tau=%d prueba=%d W=%.4f regla_propia=%.4f dif=%+.4f" % (
                            clave(A, s), st, sem, aW, aP, aW - aP))
                pr("CELDA %s lista | %.1f s" % (clave(A, s), time.time() - tc))
            ruta = os.path.join(a.out, "nucleo_grilla%s.json" % (("_" + a.etiqueta) if a.etiqueta else ""))
        else:
            if a.tipo is None:
                pr("ABORTA: --modo nulos pide --tipo")
                pr("EXIT_RUN=3")
                return 3
            pn, qn_r, wn = p[m], q[m], w[m]
            lcod = n3.codigos(lados)
            tau = f2.tau_por_root(ids, TAU_N)
            ete = tm.generar(n_test, PRUEBA_N)
            yte, vte = ete["y"], ete["vuelo"]
            Zte = f2.ruido_por_root(ids[:n_ent], n_test, 1000 + PRUEBA_N)
            A, s = CELDA_N
            dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr)
            dte = dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * Zte)

            def chan_de(tp):
                return np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tp[i]) for i in range(n_ent)])

            def acierto(Wx, ch):
                th = tm.umbrales(tm.lineas(f2.sim_trozos(Wx, tau, n_ent, ch, dtr, False)), ytr, vtr)
                pW = tm.carrera(tm.lineas(f2.sim_trozos(Wx, tau, n_ent, ch, dte, False)), th, vte)
                return float((pW == yte).mean())

            ks = list(range(a.k0, a.k0 + a.n))
            chan_real = chan_de(tipos[:n_ent])
            res.update(tipo=a.tipo, ks=ks, celda=clave(*CELDA_N), tau=TAU_N, prueba=PRUEBA_N, nulos=[], real=None)
            pr("# nulos del nucleo tipo=%s k=%s celda=%s tau=%d prueba=%d real=%s" % (
                a.tipo, ks, clave(*CELDA_N), TAU_N, PRUEBA_N, a.real))
            if a.real:
                tc = time.time()
                res["real"] = acierto(W, chan_real)
                pr("REAL nucleo W=%.4f | %.1f s" % (res["real"], time.time() - tc))
            gi0, go0 = np.bincount(qn_r, minlength=n), np.bincount(pn, minlength=n)
            ok_nulos = True
            for k in ks:
                tc = time.time()
                if a.tipo == "SL":
                    qk = n3.barajar_sl_np(pn, qn_r, lcod, np.random.default_rng([n3.SEM_SL, k]))
                    g = bool(np.array_equal(np.bincount(qk, minlength=n), gi0) and
                             np.array_equal(np.bincount(pn, minlength=n), go0) and
                             np.array_equal(lcod[qk], lcod[qn_r]) and int((qk != qn_r).sum()) > 0)
                    Wk, rk = f2.matriz(n, (pn, qk, wn), densa_ok=False)
                    ak = acierto(Wk, chan_real)
                    res["nulos"].append(dict(k=k, acierto=ak, radio_crudo=rk, destinos_cambiados=int((qk != qn_r).sum()),
                                             guarda=g))
                    pr("NULO SL k=%d acierto=%.4f radio=%.4f destinos_cambiados=%d guarda=%s | %.1f s" % (
                        k, ak, rk, int((qk != qn_r).sum()), g, time.time() - tc))
                    del Wk
                else:
                    rng = np.random.default_rng([n3.SEM_T, k])
                    tp = list(tipos[:n_ent])
                    for ld in ("L", "R"):
                        ix = [i for i in range(n_ent) if lados[i] == ld]
                        vals = [tp[i] for i in ix]
                        for i, j in zip(ix, rng.permutation(len(ix))):
                            tp[i] = vals[j]
                    g = bool(tp != list(tipos[:n_ent]) and all(
                        sorted(tp[i] for i in range(n_ent) if lados[i] == ld) ==
                        sorted(tipos[i] for i in range(n_ent) if lados[i] == ld) for ld in ("L", "R")))
                    ak = acierto(W, chan_de(tp))
                    cambiados = sum(1 for i in range(n_ent) if tp[i] != tipos[i])
                    res["nulos"].append(dict(k=k, acierto=ak, tipos_cambiados=cambiados, guarda=g))
                    pr("NULO T k=%d acierto=%.4f tipos_cambiados=%d guarda=%s | %.1f s" % (
                        k, ak, cambiados, g, time.time() - tc))
                ok_nulos &= g
            guardas["nulos_%s" % a.tipo] = bool(ok_nulos)
            ruta = os.path.join(a.out, "nulos_nucleo_%s_k%03d.json" % (a.tipo, a.k0))
    valido = all(guardas.values())
    res["guardas"], res["valido"] = guardas, valido
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % kv for kv in guardas.items()),
                                         "VALIDO" if valido else "INVALIDO"))
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), base.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t_ini))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
