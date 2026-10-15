#!/usr/bin/env python3
"""H_TAU_LIBRE: instrumento del sello tools/taulibre/SELLO-TAU-LIBRE.md (commit fec8472). Respuesta 2026-10-14-040.

Reusa tools/lector/lector_mosca.py de H_LECTOR sin cambios (md5 5b7fb79e): red R2, datos, trazas, el lector L y la
construccion de los nulos SL y T con las mismas semillas. Lo unico nuevo es la tau: semillas frescas 20 a 29 con
f2.tau_por_root; nadie elige tau en ningun brazo. El nulo k usa la tau 20 + (k mod 10).
Modos:
  --reales --celda A|ruido --taus 20,21,...  la red real con cada tau, prueba 12; --repro agrega la tau 10 a tamano
                                             completo y la compara con H_LECTOR (REPRO_LECTOR).
  --nulos SL|T --celda --k0 --n              nulos k0 a k0+n-1 con su tau fresca, prueba 12.
  --humo    ciego: REPRO_LECTOR a tamano completo (es un resultado ya publicado), NULOS_IGUAL_LECTOR sobre todos los
            grafos pedidos y TAU_FRESCA; las rutas nuevas con 600 y 200 ensayos en la semilla 99, sin aciertos.
  --local   prueba de codigo en una maquina chica: todo con 600 y 200; REPRO_LECTOR NO_APLICA; nunca decide.
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
sys.path.insert(0, os.path.join(RAIZ, "tools", "lector"))
import lector_mosca as lm  # noqa: E402  instrumento de H_LECTOR (5b7fb79e), sin cambios

rv, nr, f2, tm = lm.rv, lm.nr, lm.f2, lm.tm
NL = chr(10)
MD5_LECTOR = "5b7fb79e55ab2b695c9751698c8205c4"
MD5_SELLO_LECTOR = "6e587be69bbffcdc25b98b4899579edd"
MD5_LSUMS = "22f65b263669ddc8ba611e5b3632eb4a"
N_LJSON = 23
DIR_LECTOR = os.path.join(RAIZ, "results", "lector_2026-10-15")
TAUS_LIBRES = list(range(20, 30))
TAU_LECTOR = 10
PRUEBA = 12
CELDAS = (2, 5)
N_NULOS = 40
CHICO_TR, CHICO_TE, CHICO_SEM = 600, 200, 99


def pr(s):
    print(s, flush=True)


def tau_de_k(k):
    return TAUS_LIBRES[0] + (k % 10)


def pines(conn, annot):
    ok = lm.pines(conn, annot)
    ok["md5_lector_mosca.py"] = bool(rv.md5(os.path.abspath(lm.__file__)) == MD5_LECTOR)
    ok["md5_SELLO_LECTOR"] = bool(rv.md5(os.path.join(RAIZ, "tools", "lector", "SELLO-LECTOR.md")) == MD5_SELLO_LECTOR)
    sums = os.path.join(DIR_LECTOR, "MD5SUMS.txt")
    ok["md5_lector_MD5SUMS"] = bool(rv.md5(sums) == MD5_LSUMS)
    lista = {}
    for x in open(sums).read().split(NL):
        partes = x.split()
        if len(partes) == 2 and partes[1].endswith(".json"):
            lista[partes[1]] = partes[0]
    ok["lector_json"] = bool(len(lista) == N_LJSON and
                             all(rv.md5(os.path.join(DIR_LECTOR, k)) == v for k, v in lista.items()))
    return ok


def tau_fresca():
    """Semillas de tau ya usadas: factoriales 0 a 9, entrada por tipos 1 y 2, candidatas de H_TAU y la de H_LECTOR."""
    usadas = set(range(10)) | {1, 2}
    for c in range(6):
        hj = json.load(open(os.path.join(rv.DIR_HTAU, "htau_c%d.json" % c)))
        usadas |= set(int(x) for x in hj["candidatas"])
    for nom in sorted(os.listdir(DIR_LECTOR)):
        if nom.endswith(".json") and nom != "agregado.json":
            usadas.add(int(json.load(open(os.path.join(DIR_LECTOR, nom)))["tau_semilla"]))
    return bool(not (usadas & set(TAUS_LIBRES))), sorted(usadas)


def lector_nulos(tipo, ci):
    """Los nulos y el real de H_LECTOR en esa celda (json pineados por MD5SUMS)."""
    por_k, real = {}, None
    for k0 in (0, 10, 20, 30):
        d = json.load(open(os.path.join(DIR_LECTOR, "nulos_%s_c%d_k%03d.json" % (tipo, ci, k0))))
        for e in d["nulos"]:
            por_k[int(e["k"])] = e
        if d.get("real"):
            real = d["real"]
    return por_k, real


def guarda_fuga(ntr):
    pl = rv.pliegues(ntr)
    return bool(f2.SEM_GEN_TR not in (PRUEBA, CHICO_SEM) and f2.SEM_RUIDO_TR not in (1000 + PRUEBA, 1000 + CHICO_SEM) and
                all(len(np.intersect1d(ia, it)) == 0 and len(ia) + len(it) == ntr for ia, it in pl))


def juego(R, A, s, chico):
    ntr, nte, prueba = (CHICO_TR, CHICO_TE, CHICO_SEM) if chico else (tm.N_TRAIN, tm.N_TEST, PRUEBA)
    ytr, vtr, dtr = lm.datos(R, A, s, ntr, f2.SEM_GEN_TR, f2.SEM_RUIDO_TR)
    yte, vte, dte = lm.datos(R, A, s, nte, prueba, 1000 + prueba)
    return dict(ntr=ntr, nte=nte, prueba=prueba, ytr=ytr, vtr=vtr, dtr=dtr, yte=yte, vte=vte, dte=dte)


def medir(W, tau, R, ch, D, negativo=False):
    Ftr = lm.trazas(W, tau, R, ch, D["dtr"]).reshape(D["ntr"], -1)
    info, mod = lm.lector(Ftr, D["ytr"], D["vtr"])
    neg = None
    if negativo:
        rng = np.random.default_rng(lm.SEM_PERM)
        yperm = D["ytr"].copy()
        for st in (True, False):
            ii = np.where(D["vtr"] == st)[0]
            yperm[ii] = D["ytr"][ii][rng.permutation(len(ii))]
        infoN, modN = lm.lector(Ftr, yperm, D["vtr"])
    del Ftr
    Fte = lm.trazas(W, tau, R, ch, D["dte"]).reshape(D["nte"], -1)
    pL = lm.leer(mod, Fte, D["vte"])
    if negativo:
        yte, vte = D["yte"], D["vte"]
        pn = lm.leer(modN, Fte, vte)
        maj = {st: int(np.bincount(yte[vte == st]).argmax()) for st in (True, False)}
        azar = float((np.where(vte, maj[True], maj[False]) == yte).mean())
        an = float((pn == yte).mean())
        neg = dict(acierto=an, azar=azar, ok=bool(an <= azar + lm.MARGEN_NEG))
    del Fte
    return info, pL, neg


# ---------------- reales ----------------
def reales(a, A, s, ci, R):
    chico = a.humo or a.local
    C = {}
    taus = [int(x) for x in a.taus.split(",")]
    res = dict(experimento="H_TAU_LIBRE", modo="reales", celda=rv.clave(A, s), ci=ci, taus=taus, humo=bool(a.humo),
               local=bool(a.local), reales=[], repro=None, md5_script=rv.md5(os.path.abspath(__file__)))
    C["R2_TAMANO"] = R["ok"]
    C["PLAN_REALES"] = bool(ci in CELDAS and len(taus) > 0 and all(t in TAUS_LIBRES for t in taus))
    C["TAU_FRESCA"], usadas = tau_fresca()
    pr("TAU_FRESCA usadas=%s libres=%s -> %s" % (usadas, TAUS_LIBRES, C["TAU_FRESCA"]))
    W, radio = f2.matriz(R["n"], R["aristas"], densa_ok=False)
    chan = lm.chan_de(R, R["tipos"][:R["n_ent"]])
    pr("RED radio_crudo=%.6f | taus=%s" % (radio, taus))
    D = juego(R, A, s, chico)
    C["GUARDA_FUGA"] = guarda_fuga(D["ntr"])
    rutas, neg_ok = True, None
    if a.repro or a.humo:
        if a.local:
            C["REPRO_LECTOR"] = None
            pr("REPRO_LECTOR: NO_APLICA (local)")
        else:
            tc = time.time()
            Dg = D if not chico else juego(R, A, s, False)
            _, real_l = lector_nulos("SL", ci)
            info, pL, _ = medir(W, f2.tau_por_root(R["ids"], TAU_LECTOR), R, chan, Dg)
            wl = float((pL == Dg["yte"]).mean())
            C["REPRO_LECTOR"] = bool(real_l is not None and rv.a_str(pL) == real_l["pred_WL"] and wl == real_l["WL"] and
                                     info["elegida"] == real_l["lam"])
            res["repro"] = dict(tau=TAU_LECTOR, WL=wl, lam=info["elegida"])
            pr("REPRO_LECTOR tau=%d WL=%.4f (H_LECTOR %.4f) lambda=%g -> %s | %.1f s" % (
                TAU_LECTOR, wl, real_l["WL"] if real_l else -1.0, info["elegida"], C["REPRO_LECTOR"], time.time() - tc))
            del Dg
    for j, t in enumerate(taus):
        tc = time.time()
        info, pL, neg = medir(W, f2.tau_por_root(R["ids"], t), R, chan, D, negativo=(j == 0))
        rutas &= lm.en_clases(pL, D["vte"]) and len(pL) == D["nte"]
        if neg is not None:
            neg_ok = neg["ok"]
            res["control_negativo"] = dict(tau=t, **neg)
            pr("CONTROL_NEGATIVO tau=%d acierto=%.4f azar=%.4f tope=%.4f -> %s" % (
                t, neg["acierto"], neg["azar"], neg["azar"] + lm.MARGEN_NEG, neg["ok"]))
        if chico:
            pr("REAL tau=%d (sin aciertos) en_clases=%s | %.1f s" % (t, rutas, time.time() - tc))
        else:
            res["reales"].append(dict(tau=t, WL=float((pL == D["yte"]).mean()), pred_WL=rv.a_str(pL),
                                      lam=info["elegida"]))
            pr("REAL tau=%d WL=%.4f lambda=%g | %.1f s" % (t, res["reales"][-1]["WL"], info["elegida"], time.time() - tc))
    C["CONTROL_NEGATIVO"] = bool(neg_ok)
    C["RUTAS_EN_CLASES"] = bool(rutas)
    return res, C


# ---------------- nulos ----------------
def grafo_sl(R, k, p_, q_, lc):
    n = R["n"]
    qn = nr.barajar_sl_np(p_, q_, lc, np.random.default_rng([nr.SEM_SL, k]))
    cambiados = int((qn != q_).sum())
    g = bool(np.array_equal(np.bincount(qn, minlength=n), np.bincount(q_, minlength=n)) and
             np.array_equal(lc[qn], lc[q_]) and cambiados > 0)
    return qn, cambiados, g


def tipos_t(R, k):
    n_ent, tipos = R["n_ent"], R["tipos"]
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
    return tp, cambiados, g


def nulos(a, A, s, ci, R):
    chico = a.humo or a.local
    C = {}
    ks = list(range(a.k0, a.k0 + a.n))
    res = dict(experimento="H_TAU_LIBRE", modo="nulos", tipo=a.nulos, celda=rv.clave(A, s), ci=ci, ks=ks,
               humo=bool(a.humo), local=bool(a.local), nulos=[], md5_script=rv.md5(os.path.abspath(__file__)))
    C["R2_TAMANO"] = R["ok"]
    C["PLAN_NULOS"] = bool(ci in CELDAS and ks[0] >= 0 and ks[-1] < N_NULOS)
    C["TAU_FRESCA"], usadas = tau_fresca()
    pr("TAU_FRESCA usadas=%s libres=%s -> %s" % (usadas, TAUS_LIBRES, C["TAU_FRESCA"]))
    porl, _ = lector_nulos(a.nulos, ci)
    n = R["n"]
    p_, q_, w_ = R["aristas"]
    lc = nr.codigos(R["lados"])
    D = juego(R, A, s, chico)
    C["GUARDA_FUGA"] = guarda_fuga(D["ntr"])
    chan_real = lm.chan_de(R, R["tipos"][:R["n_ent"]])
    W_real = None
    if a.nulos == "T":
        W_real, r_real = f2.matriz(n, (p_, q_, w_), densa_ok=False)
        pr("RADIO real crudo=%.6f" % r_real)
    rutas, ok_g, ok_l = True, True, True
    for j, k in enumerate(ks):
        tc = time.time()
        t = tau_de_k(k)
        simular = (not a.humo) or j == 0
        el = porl.get(k)
        if a.nulos == "SL":
            qn, cambiados, g = grafo_sl(R, k, p_, q_, lc)
            Wk, rk = f2.matriz(n, (p_, qn, w_), densa_ok=False)
            del qn
            igual = bool(el is not None and el.get("destinos_cambiados") == cambiados and
                         abs(el.get("radio_crudo", -1.0) - rk) < 1e-6)
            ent = dict(k=k, tau=t, destinos_cambiados=cambiados, radio_crudo=rk, guarda=g, igual_lector=igual)
            pL = None
            if simular:
                info, pL, _ = medir(Wk, f2.tau_por_root(R["ids"], t), R, chan_real, D)
            del Wk
        else:
            tp, cambiados, g = tipos_t(R, k)
            igual = bool(el is not None and el.get("tipos_cambiados") == cambiados)
            ent = dict(k=k, tau=t, tipos_cambiados=cambiados, guarda=g, igual_lector=igual)
            pL = None
            if simular:
                info, pL, _ = medir(W_real, f2.tau_por_root(R["ids"], t), R, lm.chan_de(R, tp), D)
        if pL is not None:
            rutas &= lm.en_clases(pL, D["vte"]) and len(pL) == D["nte"]
            if not chico:
                ent.update(WL=float((pL == D["yte"]).mean()), lam=info["elegida"])
        res["nulos"].append(ent)
        pr("NULO %s k=%d tau=%d %s cambiados=%d guarda=%s igual_lector=%s | %.1f s" % (
            a.nulos, k, t, ("WL=%.4f" % ent["WL"]) if "WL" in ent else ("(ruta, sin aciertos)" if pL is not None
                                                                        else "(solo grafo)"),
            cambiados, g, igual, time.time() - tc))
        ok_g &= g
        ok_l &= igual
    C["NULOS_VALIDOS"] = bool(ok_g)
    C["NULOS_IGUAL_LECTOR"] = bool(ok_l)
    C["RUTAS_EN_CLASES"] = bool(rutas)
    return res, C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--celda", required=True, help="A|ruido, p. ej. 0.3|0.15")
    ap.add_argument("--reales", action="store_true")
    ap.add_argument("--taus", default=",".join(map(str, TAUS_LIBRES)))
    ap.add_argument("--repro", action="store_true")
    ap.add_argument("--nulos", choices=("SL", "T"), default=None)
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--humo", action="store_true")
    ap.add_argument("--local", action="store_true")
    a = ap.parse_args()
    if bool(a.reales) == bool(a.nulos):
        pr("ABORTA: pedir --reales o --nulos, uno solo")
        return 2
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(), platform.python_version(),
                                                      np.__version__))
    pr("# md5 script = " + rv.md5(os.path.abspath(__file__)))
    if a.humo:
        pr("# HUMO: ciego, sin aciertos nuevos")
    if a.local:
        pr("# LOCAL: prueba de codigo con 600 y 200 ensayos, no decide nada")
    A, s = (float(x) for x in a.celda.split("|"))
    ci = lm.celda_de(A, s)
    pin = pines(a.conn, a.annot)
    pr("PIN " + " ".join("%s=%s" % kv for kv in sorted(pin.items())))
    if not all(pin.values()):
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    tc = time.time()
    R = lm.red(a.conn, a.annot)
    pr("SUJETO R2 neuronas=%d entradas=%d -> %s | %.1f s" % (R["n"], R["n_ent"], R["ok"], time.time() - tc))
    if a.nulos:
        res, C = nulos(a, A, s, ci, R)
        etiqueta = "nulos_%s_c%d_k%03d" % (a.nulos, ci, a.k0)
    else:
        res, C = reales(a, A, s, ci, R)
        etiqueta = "reales_c%d_t%d" % (ci, res["taus"][0])
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
