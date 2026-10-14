#!/usr/bin/env python3
"""H_TAU en el banco de la mosca (respuesta 2026-10-14-002). Sellado antes de correr.

Pregunta. En los factoriales 3 y 4 la red le gano a su regla en 8 de 10 semillas de tau (58 a 60 de 60 corridas,
+1,28 a +1,71 puntos) y perdio en la 5 y en la 7; lo vimos despues de los datos (2026-10-14-001). H_TAU lo pone a
prueba sin mirar la prueba: si las constantes de tiempo se eligen con el entrenamiento solo, el cableado de R2 le
gana a su regla por mas de 1 punto en ensayos de prueba que nadie vio.
Diseno (todo nuevo, nada de lo que se miro en la 001):
  candidatas  10 semillas de tau que no se usaron nunca: 10 a 19 (tau_i = 0,06 + 0,12 u por root_id, como el 3).
  eleccion    por celda, la candidata con mas acierto en validacion cruzada de 5 pliegues sobre los 2.400 ensayos de
              entrenamiento (pliegue = indice del ensayo modulo 5; umbrales en 4 pliegues, acierto en el quinto).
              Empate: la semilla mas chica. Tambien se guarda la peor, solo como diagnostico.
  prueba      10 semillas de prueba nuevas: 12 a 21 (2.000 ensayos cada una; ruido 1000 + semilla, como el 3). La
              elegida y la peor usan los umbrales de los 2.400 ensayos, como en el 3; la regla propia, igual.
  repro       en la celda 0,3|0,15 (con --repro) se mide tambien la semilla de tau 0 en la prueba 2: tiene que dar
              exactamente lo del factorial 3 (W 0,9465, regla propia 0,9375, regla de 40 0,9235).
La simulacion, el lector y los datos son los de tools/factorial2/factorial2_mosca.py (md5 798a824c), importado sin
cambios; la regla propia se arma como ahi (lc y regla, copiadas linea por linea; REPRO lo controla).
Primaria (en tools/htau/agregar_htau.py): elegida menos regla propia, bootstrap sobre las semillas de prueba, margen
0,01, el mismo veredicto del factorial 4. Salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "factorial2"))
import factorial2_mosca as f2  # noqa: E402  sellado (798a824c), sin cambios

tm, base = f2.tm, f2.base
MD5_F2 = "798a824cd47808155fa12adb9e652dac"
CANDIDATAS = list(range(10, 20))
PRUEBAS = list(range(12, 22))
PLIEGUES = 5
REPRO_CELDA, REPRO_TAU, REPRO_PRUEBA = (0.3, 0.15), 0, 2
REPRO_ESPERADO = (0.9465, 0.9375, 0.9235)


def pr(s):
    print(s, flush=True)


def clave(A, s):
    return "%.1f|%.2f" % (A, s)


def validacion(L, y, v, k):
    """Acierto medio en k pliegues: umbrales con k-1 pliegues, carrera en el que queda afuera."""
    f = np.arange(len(y)) % k
    acc = []
    for j in range(k):
        te = f == j
        th = tm.umbrales(L[~te], y[~te], v[~te])
        acc.append(float((tm.carrera(L[te], th, v[te]) == y[te]).mean()))
    return float(np.mean(acc)), acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--celda", required=True, help="A|ruido, p. ej. 0.3|0.15")
    ap.add_argument("--candidatas", default=",".join(map(str, CANDIDATAS)))
    ap.add_argument("--pruebas", default=",".join(map(str, PRUEBAS)))
    ap.add_argument("--repro", action="store_true", help="medir tambien tau 0 en la prueba 2 (solo celda 0.3|0.15)")
    ap.add_argument("--solo_repro", action="store_true", help="medir solo el control REPRO y salir")
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(), platform.python_version(),
                                                      np.__version__))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    m2, mt = base.md5(os.path.abspath(f2.__file__)), base.md5(os.path.abspath(tm.__file__))
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 factorial2_mosca = %s | md5 modulo 015 = %s | md5 conn = %s | md5 annot = %s" % (m2, mt, mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mt != f2.MD5_TM or m2 != MD5_F2:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    A, s = (float(x) for x in a.celda.split("|"))
    candidatas = [int(x) for x in a.candidatas.split(",")]
    pruebas = [int(x) for x in a.pruebas.split(",")]
    repro = a.repro or a.solo_repro
    if repro and (A, s) != REPRO_CELDA:
        pr("ABORTA: REPRO solo se mide en la celda 0.3|0.15")
        pr("EXIT_RUN=3")
        return 3
    n_train, n_test = (600, 200) if humo else (tm.N_TRAIN, tm.N_TEST)
    pr("# celda=%s candidatas=%s pruebas=%s pliegues=%d repro=%s solo_repro=%s" % (
        clave(A, s), candidatas, pruebas, PLIEGUES, repro, a.solo_repro))
    tr = time.time()
    S = f2.sujeto(a.conn, a.annot, "R2", "CON")
    ids, tipos, lados = S["ids"], S["tipos"], S["lados"]
    n, n_ent, nv46 = len(ids), S["n_ent"], S["nv46"]
    guardas = {"R2_tamano": bool((S["n_U"], S["n_ar_crudo"]) == f2.R2_ESPERADO and S["contiene_m46"] and
                                 S["contiene_r1"])}
    pr("SUJETO R2 neuronas=%d aristas=%d entradas=%d -> %s | %.1f s" % (S["n_U"], S["n_ar_crudo"], n_ent,
                                                                      guardas["R2_tamano"], time.time() - tr))
    W, radio = f2.matriz(n, S["aristas"], densa_ok=False)
    pr("RADIO crudo=%.6f" % radio)
    chan = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(n_ent)])
    etr = tm.generar(n_train, f2.SEM_GEN_TR)
    ytr, vtr = etr["y"], etr["vuelo"]
    Ztr = f2.ruido_por_root(ids[:n_ent], n_train, f2.SEM_RUIDO_TR)
    dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr)

    def media(X, ld, ts, k):
        mm = np.array([lados[i] == ld and tipos[i] in ts for i in range(k)])
        return X[:, :, mm].mean(2)

    def lc(d, k):
        X = d["drive"][:, :, chan[:k]] + d["ruido"][:, :, :k]
        return np.stack([media(X, "L", ("LC4", "LPLC2"), k), media(X, "R", ("LC4", "LPLC2"), k),
                         media(X, "L", ("LPLC4",), k), media(X, "R", ("LPLC4",), k),
                         media(X, "L", ("LPLC1", "LPLC2"), k), media(X, "R", ("LPLC1", "LPLC2"), k)], axis=2)

    def regla(dte, vte, k):
        th = tm.umbrales(tm.lineas(lc(dtr, k)), ytr, vtr)
        return tm.carrera(tm.lineas(lc(dte, k)), th, vte)

    def prueba(sem):
        e = tm.generar(n_test, sem)
        Z = f2.ruido_por_root(ids[:n_ent], n_test, 1000 + sem)
        return e["y"], e["vuelo"], dict(y=e["y"], drive=tm.sintonias(e, A), ruido=s * Z)

    def lineas(tau, d):
        return tm.lineas(f2.sim_trozos(W, tau, n_ent, chan, d, False))

    res = dict(experimento="H_TAU", celda=clave(A, s), candidatas=candidatas, pruebas=pruebas, pliegues=PLIEGUES,
               humo=humo, n_ent=n_ent, radio_crudo=radio, dns_root=[int(r) for r in ids[n - 6:]], repro=None,
               md5=dict(script=base.md5(os.path.abspath(__file__)), factorial2=m2, modulo015=mt, conn=mc, annot=ma))
    if repro:
        tc = time.time()
        tau0 = f2.tau_por_root(ids, REPRO_TAU)
        th0 = tm.umbrales(lineas(tau0, dtr), ytr, vtr)
        yte, vte, dte = prueba(REPRO_PRUEBA)
        aW = float((tm.carrera(lineas(tau0, dte), th0, vte) == yte).mean())
        aP = float((regla(dte, vte, n_ent) == yte).mean())
        a40 = float((regla(dte, vte, nv46) == yte).mean())
        ok = (round(aW, 4), round(aP, 4), round(a40, 4)) == REPRO_ESPERADO
        if not humo:
            guardas["REPRO_R2"] = bool(ok)
        res["repro"] = dict(W=aW, regla_propia=aP, regla40=a40, esperado=list(REPRO_ESPERADO), igual=bool(ok))
        pr("CHEQUEO REPRO_R2 tau=%d prueba=%d W=%.4f regla_propia=%.4f regla40=%.4f esperado=%s -> %s%s | %.1f s" % (
            REPRO_TAU, REPRO_PRUEBA, aW, aP, a40, REPRO_ESPERADO, ok, " (humo: no aplica)" if humo else "",
            time.time() - tc))
    if not a.solo_repro:
        cv, cvp, ent, th, tau_s = {}, {}, {}, {}, {}
        for st in candidatas:
            tc = time.time()
            tau_s[st] = f2.tau_por_root(ids, st)
            L = lineas(tau_s[st], dtr)
            cv[st], cvp[st] = validacion(L, ytr, vtr, PLIEGUES)
            th[st] = tm.umbrales(L, ytr, vtr)
            ent[st] = float((tm.carrera(L, th[st], vtr) == ytr).mean())
            pr("CANDIDATA tau=%d validacion=%.4f pliegues=%s entrenamiento=%.4f | %.1f s" % (
                st, cv[st], " ".join("%.4f" % x for x in cvp[st]), ent[st], time.time() - tc))
            del L
        orden = sorted(candidatas)
        elegida = max(orden, key=lambda st: (cv[st], -st))
        peor = min(orden, key=lambda st: (cv[st], st))
        pr("ELECCION elegida=%d (validacion %.4f) peor=%d (validacion %.4f)" % (elegida, cv[elegida], peor, cv[peor]))
        res.update(validacion={str(k): v for k, v in cv.items()}, validacion_pliegues={str(k): v for k, v in cvp.items()},
                   entrenamiento={str(k): v for k, v in ent.items()}, elegida=elegida, peor=peor,
                   tau_DN={str(st): [float(x) for x in tau_s[st][n - 6:]] for st in candidatas}, corridas=[])
        for sem in pruebas:
            tc = time.time()
            yte, vte, dte = prueba(sem)
            pP, p40 = regla(dte, vte, n_ent), regla(dte, vte, nv46)
            pE = tm.carrera(lineas(tau_s[elegida], dte), th[elegida], vte)
            pM = tm.carrera(lineas(tau_s[peor], dte), th[peor], vte) if peor != elegida else pE
            fila = dict(prueba=sem, W_elegida=float((pE == yte).mean()), W_peor=float((pM == yte).mean()),
                        regla_propia=float((pP == yte).mean()), regla40=float((p40 == yte).mean()),
                        pred_elegida="".join(map(str, pE.tolist())), pred_peor="".join(map(str, pM.tolist())),
                        pred_regla_propia="".join(map(str, pP.tolist())))
            res["corridas"].append(fila)
            pr("CORRIDA celda=%s prueba=%d W_elegida=%.4f W_peor=%.4f regla_propia=%.4f regla40=%.4f dif=%+.4f | %.1f s" % (
                clave(A, s), sem, fila["W_elegida"], fila["W_peor"], fila["regla_propia"], fila["regla40"],
                fila["W_elegida"] - fila["regla_propia"], time.time() - tc))
    valido = all(guardas.values())
    res["guardas"], res["valido"] = guardas, valido
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % kv for kv in guardas.items()),
                                         "VALIDO" if valido else "INVALIDO"))
    ruta = os.path.join(a.out, "htau_%s%s.json" % ("c%d" % f2.CELDAS.index((A, s)),
                                                   "_repro" if a.solo_repro else ""))
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), base.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t_ini))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
