#!/usr/bin/env python3
"""H_DEBILES: las aristas debiles de R2, ¿pesan por cuales son o por cuantas son? (respuesta 2026-10-14-016).
Sellado antes de correr.

Viene del nucleo (2026-10-14-012 y 015): el nucleo de Schlegel (14,96 % de las aristas) pierde 4,59 puntos contra R2
entero. Las aristas que el nucleo deja afuera (las debiles: menos de 10 sinapsis y no mas del 1 % de la entrada de su
neurona post) ponen esos puntos. Esta prueba separa identidad de cantidad.

MEZCLA_k: R2 con el nucleo intacto (mismas aristas, pesos y signos) y las debiles con sus destinos barajados por
bloque de lados (n3.barajar_sl_np sobre las debiles solas, semilla [17, k]): conserva grados de entrada y salida de
las debiles, lados, pesos y signos; cambia a quien llegan. El radio espectral se vuelve a llevar a 0,9, como en R2 y
en el nucleo. Si dos aristas caen en el mismo par se suman (como en f2.matriz con R2).
Modos:
  grilla   MEZCLA_0 en el banco del factorial 3 (mismas semillas de tau, de prueba y celdas) para parear corrida por
           corrida con R2 (results/factorial3_2026-10-13) y con el nucleo (results/nucleo_2026-10-14).
  mezclas  MEZCLA_k para k0..k0+n-1 en la celda de los nulos (A 0,3, ruido 0,15, tau 0, prueba 2); con --real mide
           tambien R2 real y el nucleo real por el mismo camino (tienen que dar 0,9465 y 0,9135).
La simulacion, el lector, los datos y el nucleo son los de tools/nucleo/nucleo_mosca.py (md5 4697c81d), importado sin
cambios, que a su vez usa factorial2_mosca.py (798a824c) y nulos_r2.py (c4f1c4d3). La regla propia se arma como en
nucleo_mosca.py (lc y regla, copiadas linea por linea).
Controles: pines; R2_tamano; NUCLEO_tamano; por mezcla, NUCLEO_INTACTO, grados y lados de las debiles iguales y
destinos cambiados; en --real (sin humo), REAL_R2_IGUAL y REAL_NUCLEO_IGUAL.
Salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "nucleo"))
import nucleo_mosca as nm  # noqa: E402  sellado (4697c81d), sin cambios

f2, n3, tm, base = nm.f2, nm.n3, nm.tm, nm.base
MD5_NM = "4697c81d994de841f167698562924caa"
SEM_DEB = 17
REAL_R2, REAL_NUCLEO = 0.9465, 0.9135
pr = nm.pr
clave = nm.clave


def mezcla(p, q, w, m, lcod, k, n):
    pw, qw, ww = p[~m], q[~m], w[~m]
    qk = n3.barajar_sl_np(pw, qw, lcod, np.random.default_rng([SEM_DEB, k]))
    P = np.concatenate([p[m], pw])
    Q = np.concatenate([q[m], qk])
    Wt = np.concatenate([w[m], ww])
    nuc = int(m.sum())
    intacto = bool(np.array_equal(P[:nuc], p[m]) and np.array_equal(Q[:nuc], q[m]) and np.array_equal(Wt[:nuc], w[m]))
    grados = bool(np.array_equal(np.bincount(qk, minlength=n), np.bincount(qw, minlength=n)))
    lados_ok = bool(np.array_equal(lcod[qk], lcod[qw]))
    cambiados = int((qk != qw).sum())
    par = P.astype(np.int64) * n + Q.astype(np.int64)
    dup = int(len(par) - len(np.unique(par)))
    info = dict(k=k, debiles=int(len(pw)), destinos_cambiados=cambiados, pares_repetidos=dup,
                nucleo_intacto=intacto, grados_debiles=grados, lados_debiles=lados_ok,
                guarda=bool(intacto and grados and lados_ok and cambiados > 0))
    return (P, Q, Wt), info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--modo", required=True, choices=("grilla", "mezclas"))
    ap.add_argument("--taus", default="0,1,2,3,4,5,6,7,8,9")
    ap.add_argument("--pruebas", default="2,3,4,5,6,7,8,9,10,11")
    ap.add_argument("--celdas", default="todas", help="todas o lista A|ruido separada por coma")
    ap.add_argument("--etiqueta", default="")
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--real", action="store_true")
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(), platform.python_version(),
                                                     np.__version__))
    mi = base.md5(os.path.abspath(__file__))
    mn = base.md5(os.path.abspath(nm.__file__))
    m2, m3, mt = base.md5(os.path.abspath(f2.__file__)), base.md5(os.path.abspath(n3.__file__)), base.md5(
        os.path.abspath(tm.__file__))
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 script = %s | nucleo_mosca = %s | factorial2 = %s | nulos_r2 = %s | modulo015 = %s | conn = %s | annot = %s"
       % (mi, mn, m2, m3, mt, mc, ma))
    if (mn != MD5_NM or m2 != nm.MD5_F2 or m3 != nm.MD5_N3 or mt != f2.MD5_TM or mc != base.MD5_CONN or
            ma != base.MD5_ANNOT):
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    tr = time.time()
    S, m, info = nm.sujeto_nucleo(a.conn, a.annot)
    ids, tipos, lados = S["ids"], S["tipos"], S["lados"]
    n, n_ent, nv46 = len(ids), S["n_ent"], S["nv46"]
    p, q, w = S["aristas"]
    guardas = {"R2_tamano": bool((S["n_U"], S["n_ar_crudo"]) == f2.R2_ESPERADO and S["contiene_m46"] and
                                 S["contiene_r1"]),
               "NUCLEO_tamano": bool((info["aristas"], info["inhibitorias"], info["huella"]) == nm.NUCLEO_ESPERADO)}
    pr("SUJETO R2 neuronas=%d aristas=%d entradas=%d nucleo=%d debiles=%d -> %s %s | %.1f s" % (
        S["n_U"], S["n_ar_crudo"], n_ent, info["aristas"], int((~m).sum()), guardas["R2_tamano"],
        guardas["NUCLEO_tamano"], time.time() - tr))
    lcod = n3.codigos(lados)
    res = dict(modo=a.modo, humo=humo, nucleo=info, n_ent=n_ent, dns_root=[int(r) for r in ids[n - 6:]],
               md5=dict(script=mi, nucleo_mosca=mn, factorial2=m2, nulos_r2=m3, modulo015=mt, conn=mc, annot=ma))
    n_train, n_test = (120, 80) if humo else (tm.N_TRAIN, tm.N_TEST)
    chan = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(n_ent)])
    etr = tm.generar(n_train, f2.SEM_GEN_TR)
    ytr, vtr = etr["y"], etr["vuelo"]
    Ztr = f2.ruido_por_root(ids[:n_ent], n_train, f2.SEM_RUIDO_TR)
    if a.modo == "grilla":
        ar, mi0 = mezcla(p, q, w, m, lcod, 0, n)
        guardas["mezcla_0"] = mi0["guarda"]
        mi0["huella"] = nm.huella(np.asarray(ids, dtype=np.int64)[ar[0]], np.asarray(ids, dtype=np.int64)[ar[1]], ar[2])
        W, radio = f2.matriz(n, ar, densa_ok=False)
        res.update(mezcla=mi0, radio_crudo=radio)
        pr("MEZCLA k=0 debiles=%d destinos_cambiados=%d pares_repetidos=%d intacto=%s grados=%s lados=%s radio=%.4f "
           "huella=%s -> %s" % (mi0["debiles"], mi0["destinos_cambiados"], mi0["pares_repetidos"], mi0["nucleo_intacto"],
                                mi0["grados_debiles"], mi0["lados_debiles"], radio, mi0["huella"], mi0["guarda"]))
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
        ruta = os.path.join(a.out, "debiles_grilla%s.json" % (("_" + a.etiqueta) if a.etiqueta else ""))
    else:
        tau = f2.tau_por_root(ids, nm.TAU_N)
        ete = tm.generar(n_test, nm.PRUEBA_N)
        yte, vte = ete["y"], ete["vuelo"]
        Zte = f2.ruido_por_root(ids[:n_ent], n_test, 1000 + nm.PRUEBA_N)
        A, s = nm.CELDA_N
        dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr)
        dte = dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * Zte)

        def acierto(Wx):
            th = tm.umbrales(tm.lineas(f2.sim_trozos(Wx, tau, n_ent, chan, dtr, False)), ytr, vtr)
            pW = tm.carrera(tm.lineas(f2.sim_trozos(Wx, tau, n_ent, chan, dte, False)), th, vte)
            return float((pW == yte).mean())

        ks = list(range(a.k0, a.k0 + a.n))
        res.update(ks=ks, celda=clave(*nm.CELDA_N), tau=nm.TAU_N, prueba=nm.PRUEBA_N, mezclas=[], real_R2=None,
                   real_nucleo=None)
        pr("# mezclas k=%s celda=%s tau=%d prueba=%d real=%s" % (ks, res["celda"], nm.TAU_N, nm.PRUEBA_N, a.real))
        if a.real:
            tc = time.time()
            res["real_R2"] = acierto(f2.matriz(n, (p, q, w), densa_ok=False)[0])
            res["real_nucleo"] = acierto(f2.matriz(n, (p[m], q[m], w[m]), densa_ok=False)[0])
            pr("REAL R2=%.4f nucleo=%.4f | %.1f s" % (res["real_R2"], res["real_nucleo"], time.time() - tc))
            if not humo:
                guardas["REAL_R2_IGUAL"] = bool(abs(res["real_R2"] - REAL_R2) < 1e-9)
                guardas["REAL_NUCLEO_IGUAL"] = bool(abs(res["real_nucleo"] - REAL_NUCLEO) < 1e-9)
                pr("CHEQUEO REAL_R2_IGUAL esperado=%.4f -> %s | REAL_NUCLEO_IGUAL esperado=%.4f -> %s" % (
                    REAL_R2, guardas["REAL_R2_IGUAL"], REAL_NUCLEO, guardas["REAL_NUCLEO_IGUAL"]))
        ok = True
        for k in ks:
            tc = time.time()
            ar, mk = mezcla(p, q, w, m, lcod, k, n)
            Wk, rk = f2.matriz(n, ar, densa_ok=False)
            mk["acierto"], mk["radio_crudo"] = acierto(Wk), rk
            res["mezclas"].append(mk)
            ok &= mk["guarda"]
            pr("MEZCLA k=%d acierto=%.4f radio=%.4f destinos_cambiados=%d pares_repetidos=%d guarda=%s | %.1f s" % (
                k, mk["acierto"], rk, mk["destinos_cambiados"], mk["pares_repetidos"], mk["guarda"], time.time() - tc))
            del Wk
        guardas["mezclas"] = bool(ok)
        ruta = os.path.join(a.out, "debiles_mezclas_k%03d.json" % a.k0)
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
