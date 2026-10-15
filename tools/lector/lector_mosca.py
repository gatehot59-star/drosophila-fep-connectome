#!/usr/bin/env python3
"""H_LECTOR: instrumento del sello tools/lector/SELLO-LECTOR.md (commit 8e65e05). Respuesta 2026-10-14-037.

El lector L es el RIDGE de H_RIVAL sin cambios (rival_mosca.cv_ridge, ridge_ajustar y ridge_predecir: 10 lambdas,
5 pliegues modulo 5, un lambda para los dos estados, empate al mas grande, un modelo por estado), pero lee las trazas
de las 6 descendentes que devuelve f2.sim_trozos (40 pasos por 6, 240 rasgos) en lugar de las 564 entradas crudas.
Red: R2 CON, TASA, tau de f2.tau_por_root(ids, 10), la elegida por H_TAU en las 6 celdas.
Modos:
  --celda A|ruido                  primaria: WL en las pruebas 12 a 21, con REPRO_W, REPRO_RIDGE,
                                   CONTROL_NEGATIVO y, en c0, CONTROL_LECTOR_CRUDO.
  --nulos SL|T --celda --k0 --n    nulos de la celda (c2 o c5), prueba 12; --real mide tambien la red real.
  --humo                           ciego: controles a tamano completo en --celda; en --nulos, rutas con 600 y 200
                                   ensayos en la semilla 99. No imprime ni guarda aciertos de L.
  --local                          solo para probar el codigo en una maquina chica: 600 y 200 ensayos en la semilla
                                   99, controles de pareo marcados NO_APLICA; nunca decide nada.
Desvio declarado: la permutacion de tipos de nulos_r2.py vive dentro de su main(), asi que se copia linea por
linea; NULOS_IGUAL_F3 la controla contra los json del factorial 3 (tipos y destinos cambiados por nulo).
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
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "rival"))
sys.path.insert(0, os.path.join(RAIZ, "tools", "factorial3"))
import rival_mosca as rv  # noqa: E402  sellado en 04d0635 (774232f5), sin cambios
import nulos_r2 as nr  # noqa: E402  sellado en el factorial 3 (c4f1c4d3), sin cambios

f2, tm, ht = rv.f2, rv.tm, rv.ht
NL = chr(10)
MD5_RIVAL = "774232f5b4a53872a05f6a0f06015f34"
MD5_NULOS = "c4f1c4d39c99f07cb9ad7977b6f3b01a"
MD5_RSUMS = "78477d7a099e3399333309126a42ee6d"
DIR_RIVAL = os.path.join(RAIZ, "results", "rival_2026-10-15")
TAU_SEM = 10
PRIMARIA = list(range(12, 22))
PRUEBA_NULOS = 12
CELDAS_NULOS = (2, 5)
N_NULOS = 40
SEM_PERM = 2043
MARGEN_NEG = 0.05
CHICO_TR, CHICO_TE, CHICO_SEM = 600, 200, 99


def pr(s):
    print(s, flush=True)


def pines(conn, annot):
    ok = rv.pines(conn, annot)
    ok["md5_rival_mosca.py"] = bool(rv.md5(os.path.abspath(rv.__file__)) == MD5_RIVAL)
    ok["md5_nulos_r2.py"] = bool(rv.md5(os.path.abspath(nr.__file__)) == MD5_NULOS)
    sums = os.path.join(DIR_RIVAL, "MD5SUMS.txt")
    ok["md5_rival_MD5SUMS"] = bool(rv.md5(sums) == MD5_RSUMS)
    lista = {}
    for x in open(sums).read().split(NL):
        partes = x.split()
        if len(partes) == 2 and partes[1].startswith("rival_c") and partes[1].endswith(".json"):
            lista[partes[1]] = partes[0]
    ok["rival_6_json"] = bool(len(lista) == 6 and all(rv.md5(os.path.join(DIR_RIVAL, k)) == v for k, v in lista.items()))
    return ok


def f3_nulos(tipo):
    """Los nulos del factorial 3, verificados contra su MD5SUMS (pineado por rv.pines)."""
    lista = {}
    for x in open(os.path.join(rv.DIR_F3, "MD5SUMS.txt")).read().split(NL):
        partes = x.split()
        if len(partes) == 2 and partes[1].startswith("nulos_R2_%s_k" % tipo) and partes[1].endswith(".json"):
            lista[partes[1]] = partes[0]
    ok = len(lista) > 0
    por_k = {}
    for nom, m in lista.items():
        ruta = os.path.join(rv.DIR_F3, nom)
        ok = ok and rv.md5(ruta) == m
        for e in json.load(open(ruta))["nulos"]:
            por_k[int(e["k"])] = e
    return bool(ok), por_k


# ---------------- lector ----------------
def lector(F, y, v):
    """El RIDGE de H_RIVAL tal cual: eleccion por validacion y reajuste con todos los ensayos."""
    n = len(y)
    cv, acc = rv.cv_ridge(F, y, v, rv.pliegues(n), rv.LAMBDAS_R)
    j = max(range(len(rv.LAMBDAS_R)), key=lambda k: (cv[k], rv.LAMBDAS_R[k]))
    lam = rv.LAMBDAS_R[j]
    mod = rv.ridge_ajustar(F, y, v, np.arange(n), (lam,))
    return dict(candidatas=list(rv.LAMBDAS_R), validacion=cv.tolist(), pliegues=acc.tolist(), elegida=lam), mod


def leer(mod, F, v):
    return rv.ridge_predecir(mod, F, v, np.arange(len(v)))[0]


def en_clases(p, v):
    return bool(all(np.isin(p[v == st], tm.CLASES[st]).all() for st in (True, False)))


# ---------------- red y datos (los de H_TAU) ----------------
def red(conn, annot):
    S = f2.sujeto(conn, annot, "R2", "CON")
    ok = bool((S["n_U"], S["n_ar_crudo"]) == f2.R2_ESPERADO and S["contiene_m46"] and S["contiene_r1"])
    return dict(ids=S["ids"], tipos=S["tipos"], lados=S["lados"], n=len(S["ids"]), n_ent=S["n_ent"],
                aristas=S["aristas"], ok=ok)


def chan_de(R, tp):
    return np.array([(0 if R["lados"][i] == "L" else 1) * tm.NT + tm.TIPOS.index(tp[i]) for i in range(R["n_ent"])])


def datos(R, A, s, n, sem_gen, sem_ruido):
    e = tm.generar(n, sem_gen)
    Z = f2.ruido_por_root(R["ids"][:R["n_ent"]], n, sem_ruido)
    return e["y"], e["vuelo"], dict(y=e["y"], drive=tm.sintonias(e, A), ruido=s * Z)


def trazas(W, tau, R, ch, d):
    return f2.sim_trozos(W, tau, R["n_ent"], ch, d, False)


def crudas(d, ch):
    X = d["drive"][:, :, ch] + d["ruido"]
    return X.reshape(len(X), -1)


def celda_de(A, s):
    return f2.CELDAS.index((A, s))


# ---------------- primaria ----------------
def celda(a, A, s, ci, R):
    chico = a.local
    C = {}
    res = dict(experimento="H_LECTOR", modo="celda", celda=rv.clave(A, s), ci=ci, humo=bool(a.humo), local=chico,
               tau_semilla=TAU_SEM, md5_script=rv.md5(os.path.abspath(__file__)))
    C["R2_TAMANO"] = R["ok"]
    tc = time.time()
    W, radio = f2.matriz(R["n"], R["aristas"], densa_ok=False)
    chan = chan_de(R, R["tipos"][:R["n_ent"]])
    tau = f2.tau_por_root(R["ids"], TAU_SEM)
    pr("RED radio_crudo=%.6f tau_semilla=%d | %.1f s" % (radio, TAU_SEM, time.time() - tc))
    hj = json.load(open(os.path.join(rv.DIR_HTAU, "htau_c%d.json" % ci)))
    hcor = {r["prueba"]: r for r in hj["corridas"]}
    C["HTAU_CELDA"] = bool(hj["celda"] == rv.clave(A, s) and hj["elegida"] == TAU_SEM and sorted(hcor) == PRIMARIA)
    rj = json.load(open(os.path.join(DIR_RIVAL, "rival_c%d.json" % ci)))
    rf = {f["prueba"]: f for f in rj["filas"]}
    C["RIVAL_CELDA"] = bool(rj["celda"] == rv.clave(A, s) and rj["valido"] is True and rj["humo"] is False and
                            all(p in rf and "pred_RIDGE" in rf[p] for p in PRIMARIA))
    ntr, nte = (CHICO_TR, CHICO_TE) if chico else (tm.N_TRAIN, tm.N_TEST)
    pruebas = [CHICO_SEM] if chico else [int(x) for x in a.pruebas.split(",")]
    if not chico and not a.humo:
        C["PLAN_PRUEBAS"] = bool(pruebas == PRIMARIA)
    res["pruebas"] = pruebas
    tc = time.time()
    ytr, vtr, dtr = datos(R, A, s, ntr, f2.SEM_GEN_TR, f2.SEM_RUIDO_TR)
    Ttr = trazas(W, tau, R, chan, dtr)
    Ftr = Ttr.reshape(ntr, -1)
    th = tm.umbrales(tm.lineas(Ttr), ytr, vtr)
    pl = rv.pliegues(ntr)
    C["GUARDA_FUGA"] = bool(f2.SEM_GEN_TR not in PRIMARIA + [CHICO_SEM] and
                            f2.SEM_RUIDO_TR not in [1000 + p for p in PRIMARIA + [CHICO_SEM]] and
                            all(len(np.intersect1d(ia, it)) == 0 and len(ia) + len(it) == ntr for ia, it in pl))
    pr("TRAZAS entrenamiento=%d rasgos=%d | %.1f s" % (ntr, Ftr.shape[1], time.time() - tc))
    tc = time.time()
    info, mod = lector(Ftr, ytr, vtr)
    if not a.humo and not chico:
        for k, lam in enumerate(info["candidatas"]):
            pr("CANDIDATA lector lambda=%g validacion=%.4f" % (lam, info["validacion"][k]))
    pr("ELECCION lector lambda=%s | %.1f s" % ("(humo: no se imprime)" if a.humo else "%g" % info["elegida"],
                                             time.time() - tc))
    rng = np.random.default_rng(SEM_PERM)
    yperm = ytr.copy()
    for st in (True, False):
        ii = np.where(vtr == st)[0]
        yperm[ii] = ytr[ii][rng.permutation(len(ii))]
    infoN, modN = lector(Ftr, yperm, vtr)
    del Ftr
    if ci == 0:
        tc = time.time()
        p0 = CHICO_SEM if chico else PRIMARIA[0]
        infoX, modX = lector(crudas(dtr, chan), ytr, vtr)
        y0, v0, d0 = datos(R, A, s, nte, p0, 1000 + p0)
        pX = leer(modX, crudas(d0, chan), v0)
        if chico:
            C["CONTROL_LECTOR_CRUDO"] = None
            pr("CONTROL_LECTOR_CRUDO local: ruta en_clases=%s (NO_APLICA) | %.1f s" % (en_clases(pX, v0), time.time() - tc))
        else:
            igual = int((pX == rv.de_str(rf[p0]["pred_RIDGE"])).sum())
            C["CONTROL_LECTOR_CRUDO"] = bool(rv.a_str(pX) == rf[p0]["pred_RIDGE"] and
                                             infoX["elegida"] == rj["rivales"]["RIDGE"]["elegida"])
            pr("CONTROL_LECTOR_CRUDO prueba=%d lambda=%g (H_RIVAL %g) iguales=%d/%d -> %s | %.1f s" % (
                p0, infoX["elegida"], rj["rivales"]["RIDGE"]["elegida"], igual, len(pX), C["CONTROL_LECTOR_CRUDO"],
                time.time() - tc))
        del d0
    filas, rw, rr = [], [0, 0], [0, 0]
    for p in pruebas:
        tp = time.time()
        yte, vte, dte = datos(R, A, s, nte, p, 1000 + p)
        Tte = trazas(W, tau, R, chan, dte)
        del dte
        Fte = Tte.reshape(len(yte), -1)
        pW = tm.carrera(tm.lineas(Tte), th, vte)
        if not chico:
            rw[0] += int(rv.a_str(pW) == hcor[p]["pred_elegida"] and rv.repro_w(hcor[p]["pred_elegida"], yte, hcor[p]["W_elegida"]))
            rw[1] += 1
            rr[0] += int(rv.repro_w(rf[p]["pred_RIDGE"], yte, rf[p]["RIDGE"]))
            rr[1] += 1
        if p == pruebas[0]:
            pn = leer(modN, Fte, vte)
            maj = {st: int(np.bincount(yte[vte == st]).argmax()) for st in (True, False)}
            azar = float((np.where(vte, maj[True], maj[False]) == yte).mean())
            an = float((pn == yte).mean())
            C["CONTROL_NEGATIVO"] = bool(an <= azar + MARGEN_NEG)
            res["control_negativo"] = dict(prueba=p, acierto=an, azar=azar, lam=infoN["elegida"])
            pr("CONTROL_NEGATIVO prueba=%d acierto=%.4f azar=%.4f tope=%.4f -> %s" % (
                p, an, azar, azar + MARGEN_NEG, C["CONTROL_NEGATIVO"]))
        pL = leer(mod, Fte, vte)
        if a.humo or chico:
            if p == pruebas[0]:
                C["RUTA_LECTOR"] = en_clases(pL, vte) and len(pL) == len(yte)
                pr("RUTA lector prueba=%d predicciones=%d en_clases=%s (sin aciertos)" % (p, len(pL), C["RUTA_LECTOR"]))
            pr("PRUEBA celda=%s prueba=%d W_igual=%s | %.1f s" % (
                rv.clave(A, s), p, "NO_APLICA" if chico else rv.a_str(pW) == hcor[p]["pred_elegida"], time.time() - tp))
        else:
            fila = dict(prueba=p, WL=float((pL == yte).mean()), pred_WL=rv.a_str(pL), RIDGE=rf[p]["RIDGE"],
                        W_elegida=hcor[p]["W_elegida"])
            filas.append(fila)
            pr("PRUEBA celda=%s prueba=%d WL=%.4f RIDGE=%.4f W_elegida=%.4f | %.1f s" % (
                rv.clave(A, s), p, fila["WL"], fila["RIDGE"], fila["W_elegida"], time.time() - tp))
        del Tte, Fte
    if chico:
        C["REPRO_W"], C["REPRO_RIDGE"] = None, None
        pr("CHEQUEO REPRO_W y REPRO_RIDGE: NO_APLICA (local)")
    else:
        C["REPRO_W"] = bool(rw[0] == rw[1] == len(pruebas))
        C["REPRO_RIDGE"] = bool(rr[0] == rr[1] == len(pruebas))
        pr("CHEQUEO REPRO_W iguales=%d/%d -> %s | REPRO_RIDGE iguales=%d/%d -> %s" % (
            rw[0], rw[1], C["REPRO_W"], rr[0], rr[1], C["REPRO_RIDGE"]))
    res["filas"] = filas
    res["lector"] = None if (a.humo or chico) else info
    return res, C


# ---------------- nulos ----------------
def nulos(a, A, s, ci, R):
    chico = a.humo or a.local
    C = {}
    ks = list(range(a.k0, a.k0 + a.n))
    res = dict(experimento="H_LECTOR", modo="nulos", tipo=a.nulos, celda=rv.clave(A, s), ci=ci, ks=ks,
               humo=bool(a.humo), local=bool(a.local), tau_semilla=TAU_SEM, nulos=[], real=None,
               md5_script=rv.md5(os.path.abspath(__file__)))
    C["R2_TAMANO"] = R["ok"]
    if not chico:
        C["PLAN_NULOS"] = bool(ci in CELDAS_NULOS and ks[0] >= 0 and ks[-1] < N_NULOS)
    okf3, f3 = f3_nulos(a.nulos)
    n, n_ent = R["n"], R["n_ent"]
    p_, q_, w_ = R["aristas"]
    lc = nr.codigos(R["lados"])
    tau = f2.tau_por_root(R["ids"], TAU_SEM)
    ntr, nte, prueba = (CHICO_TR, CHICO_TE, CHICO_SEM) if chico else (tm.N_TRAIN, tm.N_TEST, PRUEBA_NULOS)
    res["prueba"] = prueba
    ytr, vtr, dtr = datos(R, A, s, ntr, f2.SEM_GEN_TR, f2.SEM_RUIDO_TR)
    yte, vte, dte = datos(R, A, s, nte, prueba, 1000 + prueba)
    tipos = R["tipos"]
    chan_real = chan_de(R, tipos[:n_ent])

    def medir(W, ch):
        Ftr = trazas(W, tau, R, ch, dtr).reshape(ntr, -1)
        info, mod = lector(Ftr, ytr, vtr)
        del Ftr
        pL = leer(mod, trazas(W, tau, R, ch, dte).reshape(nte, -1), vte)
        return info, pL

    W_real = None
    if a.real or a.nulos == "T":
        W_real, r_real = f2.matriz(n, (p_, q_, w_), densa_ok=False)
        pr("RADIO real crudo=%.6f" % r_real)
    rutas = True
    if a.real:
        tc = time.time()
        info, pL = medir(W_real, chan_real)
        rutas &= en_clases(pL, vte)
        res["real"] = None if chico else dict(WL=float((pL == yte).mean()), pred_WL=rv.a_str(pL), lam=info["elegida"])
        pr("REAL %s | %.1f s" % ("(humo: sin aciertos)" if chico else "WL=%.4f" % res["real"]["WL"], time.time() - tc))
    gi0, go0 = np.bincount(q_, minlength=n), np.bincount(p_, minlength=n)
    ok_nulos, ok_f3 = True, okf3
    for k in ks:
        tc = time.time()
        if a.nulos == "SL":
            qn = nr.barajar_sl_np(p_, q_, lc, np.random.default_rng([nr.SEM_SL, k]))
            cambiados = int((qn != q_).sum())
            g = bool(np.array_equal(np.bincount(qn, minlength=n), gi0) and
                     np.array_equal(np.bincount(p_, minlength=n), go0) and
                     np.array_equal(lc[qn], lc[q_]) and cambiados > 0)
            Wk, rk = f2.matriz(n, (p_, qn, w_), densa_ok=False)
            del qn
            info, pL = medir(Wk, chan_real)
            del Wk
            e3 = f3.get(k)
            igual3 = bool(e3 is not None and e3.get("destinos_cambiados") == cambiados and
                          abs(e3.get("radio_crudo", -1.0) - rk) < 1e-6)
            ent = dict(k=k, destinos_cambiados=cambiados, radio_crudo=rk, guarda=g, igual_f3=igual3)
        else:
            rng = np.random.default_rng([nr.SEM_T, k])
            tp = list(tipos[:n_ent])
            for ld in ("L", "R"):
                ix = [i for i in range(n_ent) if R["lados"][i] == ld]
                vals = [tp[i] for i in ix]
                for i, j in zip(ix, rng.permutation(len(ix))):
                    tp[i] = vals[j]
            g = bool(tp != list(tipos[:n_ent]) and all(
                sorted(tp[i] for i in range(n_ent) if R["lados"][i] == ld) ==
                sorted(tipos[i] for i in range(n_ent) if R["lados"][i] == ld) for ld in ("L", "R")))
            cambiados = sum(1 for i in range(n_ent) if tp[i] != tipos[i])
            info, pL = medir(W_real, chan_de(R, tp))
            e3 = f3.get(k)
            igual3 = bool(e3 is not None and e3.get("tipos_cambiados") == cambiados)
            ent = dict(k=k, tipos_cambiados=cambiados, guarda=g, igual_f3=igual3)
        rutas &= en_clases(pL, vte)
        if not chico:
            ent.update(WL=float((pL == yte).mean()), lam=info["elegida"])
        res["nulos"].append(ent)
        pr("NULO %s k=%d %s cambiados=%d guarda=%s igual_f3=%s | %.1f s" % (
            a.nulos, k, "(humo: sin aciertos)" if chico else "WL=%.4f" % ent["WL"], cambiados, g, igual3,
            time.time() - tc))
        ok_nulos &= g
        ok_f3 &= igual3
    C["NULOS_VALIDOS"] = bool(ok_nulos)
    C["NULOS_IGUAL_F3"] = bool(ok_f3)
    C["RUTAS_EN_CLASES"] = bool(rutas)
    return res, C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--celda", required=True, help="A|ruido, p. ej. 0.3|0.15")
    ap.add_argument("--pruebas", default=",".join(map(str, PRIMARIA)))
    ap.add_argument("--nulos", choices=("SL", "T"), default=None)
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--real", action="store_true")
    ap.add_argument("--humo", action="store_true")
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(), platform.python_version(),
                                                      np.__version__))
    pr("# md5 script = " + rv.md5(os.path.abspath(__file__)))
    if a.humo:
        pr("# HUMO: ciego, sin aciertos de L")
    if a.local:
        pr("# LOCAL: prueba de codigo con 600 y 200 ensayos, no decide nada")
    A, s = (float(x) for x in a.celda.split("|"))
    ci = celda_de(A, s)
    pin = pines(a.conn, a.annot)
    pr("PIN " + " ".join("%s=%s" % kv for kv in sorted(pin.items())))
    if not all(pin.values()):
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    tc = time.time()
    R = red(a.conn, a.annot)
    pr("SUJETO R2 neuronas=%d entradas=%d -> %s | %.1f s" % (R["n"], R["n_ent"], R["ok"], time.time() - tc))
    if a.nulos:
        res, C = nulos(a, A, s, ci, R)
        etiqueta = "nulos_%s_c%d_k%03d" % (a.nulos, ci, a.k0)
    else:
        res, C = celda(a, A, s, ci, R)
        etiqueta = "lector_c%d" % ci
    C["PIN"] = True
    if a.humo:
        etiqueta = "humo_" + etiqueta
    if a.local:
        etiqueta = "local_" + etiqueta
    res["controles"] = C
    valido = all(v is not False for v in C.values())
    res["valido"] = bool(valido and not a.local)
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % (k, "NO_APLICA" if v is None else v) for k, v in C.items()),
                                         "VALIDO" if valido else "INVALIDO"))
    ruta = os.path.join(a.out, etiqueta + ".json")
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), rv.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t0))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
