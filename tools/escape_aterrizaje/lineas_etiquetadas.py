#!/usr/bin/env python3
"""Lineas etiquetadas: cada descendente con su umbral dispara una accion, sin lector entrenado (2026-10-12-012).

Diseno: respuesta 2026-10-12-008. Sujeto, dinamica, entrada, tarea y nulos son los de la 005, importados sin
cambios (escape_aterrizaje_dbc3.py md5 4d40477d..., entrada_por_tipos.py md5 e060c4bf...):
  motivo de 28 neuronas de FlyWire v783 en SparseLTC con tau fija heterogenea (semilla 0), rho 0.9;
  entrada por tipo (LC4, LPLC2, LPLC4 en tres variantes); ruido 0.15 y 0.45; mismo conjunto de prueba
  (semilla 2, ruido semilla 102); 300 SL (rng 7) y 300 T (rng 11), los mismos de la 005.
Lo unico nuevo es el lector (etapa E4 sin entrenar):
  lineas = [DNp01 izq, DNp01 der, DNp07 izq, DNp07 der] -> [escapar de la izq (1), de la der (2),
  aterrizar (3), aterrizar (3)].
  Umbral de cada linea (PRIMARIO, cambio declarado sobre la 008 tras el humo y antes del sellado): cuantil
  1 - FA del maximo temporal de esa linea en los ensayos de ENTRENAMIENTO con el objeto que pasa sin
  acercarse (semilla 1, 800 ensayos, mismo ruido sigma y misma variante), calculado para cada red por
  separado. FA = 0.05 por linea. Motivo: en el humo, con umbral fijado solo con ruido (la 008 literal), el
  objeto que pasa cruzaba siempre (falsa alarma 1,000) y la regla a mano no pasaba el control positivo.
  La 008 literal (umbral con solo ruido, semilla 103, 2000 ensayos) queda como brazo DESCRIPTIVO para W y la
  regla a mano.
  Carrera: gana la primera linea que cruza; en el piso solo compiten las de escape (el estado de vuelo es
  clasico, decision de la 004). Empate en el mismo paso: mayor exceso maximo sobre el umbral. Sin cruce: 0.
Rivales: regla a mano con las mismas lineas sobre las entradas crudas (escape del lado s = media de LC4 y
LPLC2 de ese lado; aterrizaje del lado s = media de LPLC4), mismos umbrales por ruido y misma carrera.
Descriptivo: ridge entrenado sobre las 24 entradas crudas (el rival de la 005) como techo entrenado.
Pruebas: W contra SL y T, p por rango, Holm sobre 12 por cola (3 variantes x 2 ruidos x 2 nulos), con el
mismo criterio de celda de la 005. H3: W contra la regla a mano, McNemar.
Controles: guardas de SL y T; reproduce (W dos veces identico); negativo: con entrada AGNOSTICA, 30 T dan
predicciones identicas a W; positivo: la regla a mano con COMO_LPLC2 y ruido 0.15 supera al azar de la 005
(mayoria por estado) por >= 0.10.
Salida: 0 completo; 2 insumos distintos del pin; 3 instrumento invalido.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import escape_aterrizaje_dbc3 as base  # noqa: E402  modulo de la 003, sin cambios
import entrada_por_tipos as ept  # noqa: E402  modulo de la 005, sin cambios

MD5_BASE = "4d40477d87406c31672acfb6e6e8f5a2"
MD5_EPT = "e060c4bffb685aa550dadc19eda3dd02"
T = base.T
TIPOS = ept.TIPOS
VARIANTES = ept.VARIANTES
RUIDOS = ept.RUIDOS
FA = 0.05
N_CAL = 2000
N_NULO = 300
N_AGN = 30
ALFA = 0.05
MARGEN_POS = 0.10
ACCION = np.array([1, 2, 3, 3])


def pr(s):
    print(s, flush=True)


def umbrales(S_cal, fa):
    return np.quantile(S_cal.max(axis=1), 1.0 - fa, axis=0)


def carrera(S, th, vuelo):
    """S (n, T, 4): [esc_izq, esc_der, aterr_izq, aterr_der]."""
    big = T + 1
    cruza = S > th[None, None, :]
    t_cruce = np.where(cruza.any(axis=1), cruza.argmax(axis=1), big)
    t_cruce[~vuelo, 2:] = big
    exceso = (S - th[None, None, :]).max(axis=1)
    t_min = t_cruce.min(axis=1)
    score = np.where(t_cruce == t_min[:, None], exceso, -np.inf)
    gan = score.argmax(axis=1)
    return np.where(t_min >= big, 0, ACCION[gan])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s" % (platform.node(), platform.platform(),
       platform.python_version(), np.__version__))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    mb, me = base.md5(os.path.abspath(base.__file__)), base.md5(os.path.abspath(ept.__file__))
    pr("# md5 modulo 003 = %s | md5 modulo 005 = %s" % (mb, me))
    pr("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mb != MD5_BASE or me != MD5_EPT:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_nulo = 3 if humo else N_NULO
    n_agn = 3 if humo else N_AGN
    n_cal = 300 if humo else N_CAL
    n_train, n_test = (600, 400) if humo else (ept.N_TRAIN, ept.N_TEST)

    sel, aristas = base.construir_motivo(a.conn, a.annot)
    n = len(sel)
    nv = n - 4
    lados = ["L" if s[2] == "left" else "R" for s in sel]
    tipos = [s[1] for s in sel]
    assert all(t in TIPOS for t in tipos[:nv]) and tipos[nv:] == ["DNp01", "DNp01", "DNp07", "DNp07"]
    assert lados[nv:] == ["L", "R", "L", "R"]
    W, rho0 = base.matriz(n, aristas)
    pr("MOTIVO neuronas=%d visuales=%d aristas=%d inhibitorias=%d rho_crudo=%.4f" % (
        n, nv, len(aristas), sum(w < 0 for _, _, w in aristas), rho0))

    def cod(i, tipo):
        return (0 if lados[i] == "L" else 1) * 3 + TIPOS.index(tipo)
    idx_W = np.array([cod(i, tipos[i]) for i in range(nv)])

    # nulos: copia literal de la 005 (mismas semillas, mismos 300 SL y 300 T)
    rng = np.random.default_rng(7)
    gi0, go0 = base.grados(n, aristas)
    par0 = sorted((p, q) for p, q, _ in aristas)
    sl, guard_sl = [], True
    for k in range(n_nulo):
        ar = base.barajar_sl(aristas, lados, rng)
        gi, go = base.grados(n, ar)
        ok = bool((gi == gi0).all() and (go == go0).all() and sorted((p, q) for p, q, _ in ar) != par0
                  and all(lados[p] == lados[q] for p, q, _ in ar))
        guard_sl &= ok
        sl.append((ar, base.matriz(n, ar)[0]))
    rng_t = np.random.default_rng(11)
    perms, guard_t = [], True
    for k in range(n_nulo):
        tp = list(tipos[:nv])
        for ld in ("L", "R"):
            ix = [i for i in range(nv) if lados[i] == ld]
            vals = [tp[i] for i in ix]
            for i, j in zip(ix, rng_t.permutation(len(ix))):
                tp[i] = vals[j]
        ok = tp != tipos[:nv] and all(
            sorted(tp[i] for i in range(nv) if lados[i] == ld) == sorted(tipos[i] for i in range(nv) if lados[i] == ld)
            for ld in ("L", "R"))
        guard_t &= ok
        perms.append(np.array([cod(i, tp[i]) for i in range(nv)]))
    pr("NULOS SL=%d guarda=%s T=%d guarda=%s" % (len(sl), guard_sl, len(perms), guard_t))

    etr, ete = ept.generar_estimulo(n_train, 1), ept.generar_estimulo(n_test, 2)
    ytr, yte, vte = etr["y"], ete["y"], ete["vuelo"]
    Ztr = np.random.default_rng(101).standard_normal((n_train, T, nv))
    Zte = np.random.default_rng(102).standard_normal((n_test, T, nv))
    Zcal = np.random.default_rng(103).standard_normal((n_cal, T, nv))
    maj = {s: int(np.bincount(ytr[etr["vuelo"] == s]).argmax()) for s in (True, False)}
    azar = float((np.where(vte, maj[True], maj[False]) == yte).mean())
    pr("DATOS prueba=%d calibracion_solo_ruido_descriptiva=%d clases_prueba(nada,esc_izq,esc_der,aterr)=%s azar_mayoria_por_estado=%.4f FA_por_linea=%.2f" % (
        n_test, n_cal, ",".join(str(int((yte == k).sum())) for k in range(4)), azar, FA))
    tau0 = 0.06 + 0.12 * np.random.default_rng(0).random(n)

    m_esc = [np.array([lados[i] == ld and tipos[i] in ("LC4", "LPLC2") for i in range(nv)]) for ld in ("L", "R")]
    m_ate = [np.array([lados[i] == ld and tipos[i] == "LPLC4" for i in range(nv)]) for ld in ("L", "R")]

    def lineas_crudas(X):
        return np.stack([X[:, :, m_esc[0]].mean(2), X[:, :, m_esc[1]].mean(2),
                         X[:, :, m_ate[0]].mean(2), X[:, :, m_ate[1]].mean(2)], axis=2)

    def acc(p):
        return float((p == yte).mean())

    def por_clase(p):
        return [float((p[yte == k] == k).mean()) for k in range(4)]

    def falsa_alarma(p):
        m = ete["est"] == 2
        return float((p[m] != 0).mean())

    res = {"humo": humo, "guarda_SL": guard_sl, "guarda_T": guard_t, "azar": azar, "FA": FA, "celdas": {}}
    prim, pW_c, regla_c = {}, {}, {}
    mpasa = etr["est"] == 2
    pr("CALIBRACION ensayos_pasa_entrenamiento=%d" % int(mpasa.sum()))

    def datos(v, s):
        dr_tr = ept.sintonias(etr, v)
        d_te = dict(y=yte, drive=ept.sintonias(ete, v), ruido=s * Zte)
        d_pasa = dict(y=ytr[mpasa], drive=dr_tr[mpasa], ruido=s * Ztr[mpasa])
        d_ruido = dict(y=np.zeros(n_cal, dtype=int), drive=np.zeros((n_cal, T, 6)), ruido=s * Zcal)
        return dr_tr, d_te, d_pasa, d_ruido

    def pred(Wm, idx, d_te, d_cal):
        th = umbrales(base.simular(Wm, tau0, idx, d_cal), FA)
        return carrera(base.simular(Wm, tau0, idx, d_te), th, vte), th

    def regla(d_te, d_cal):
        th = umbrales(lineas_crudas(d_cal["drive"][:, :, idx_W] + d_cal["ruido"]), FA)
        return carrera(lineas_crudas(d_te["drive"][:, :, idx_W] + d_te["ruido"]), th, vte)

    for v in VARIANTES:
        for s in RUIDOS:
            tc = time.time()
            dr_tr, d_te, d_pasa, d_ruido = datos(v, s)
            pW, thW = pred(W, idx_W, d_te, d_pasa)
            aW = acc(pW)
            a_sl = [acc(pred(Ws, idx_W, d_te, d_pasa)[0]) for _, Ws in sl]
            a_t = [acc(pred(W, ix, d_te, d_pasa)[0]) for ix in perms]
            ps_sl, pi_sl = ept.p_rango(aW, a_sl)
            ps_t, pi_t = ept.p_rango(aW, a_t)
            X_te = d_te["drive"][:, :, idx_W] + d_te["ruido"]
            pR = regla(d_te, d_pasa)
            aR = acc(pR)
            pW8 = pred(W, idx_W, d_te, d_ruido)[0]
            pR8 = regla(d_te, d_ruido)
            b1, c1, p1 = base.mcnemar(pW == yte, pR == yte)
            h3 = "MEJOR" if (b1 > c1 and p1 < ALFA) else ("PEOR" if (c1 > b1 and p1 < ALFA) else "EMPATE")
            Xall = np.concatenate([(dr_tr[:, :, idx_W] + s * Ztr), X_te]).reshape(n_train + n_test, -1)
            pRidge = ept.ridge_mux(Xall[:n_train], ytr, etr["vuelo"], Xall[n_train:], vte)[0]
            del Xall
            c = dict(W=aW, W_por_clase=por_clase(pW), W_falsa_alarma_pasa=falsa_alarma(pW), umbrales_W=thW.tolist(),
                     SL=a_sl, T=a_t, p_sup_SL=ps_sl, p_inf_SL=pi_sl, p_sup_T=ps_t, p_inf_T=pi_t,
                     regla=aR, regla_por_clase=por_clase(pR), regla_falsa_alarma_pasa=falsa_alarma(pR),
                     H3_gana_W=b1, H3_gana_regla=c1, H3_p=p1, H3=h3, ridge_crudo_entrenado=acc(pRidge),
                     d008_W=acc(pW8), d008_W_falsa_alarma_pasa=falsa_alarma(pW8), d008_regla=acc(pR8),
                     d008_regla_falsa_alarma_pasa=falsa_alarma(pR8),
                     dur_s=time.time() - tc)
            prim[(v, s)], pW_c[(v, s)], regla_c[(v, s)] = c, pW, aR
            pr("CELDA variante=%s ruido=%.2f W=%.4f por_clase(nada,esc_izq,esc_der,aterr)=%s falsa_alarma_pasa=%.3f umbrales=%s | "
               "SL media=%.4f max=%.4f igualan=%d/%d p_sup=%.4f p_inf=%.4f | T media=%.4f max=%.4f igualan=%d/%d p_sup=%.4f p_inf=%.4f | %.1f s" % (
                   v, s, aW, ",".join("%.3f" % x for x in c["W_por_clase"]), c["W_falsa_alarma_pasa"],
                   ",".join("%.4f" % x for x in thW), np.mean(a_sl), np.max(a_sl), sum(x >= aW for x in a_sl), len(a_sl),
                   ps_sl, pi_sl, np.mean(a_t), np.max(a_t), sum(x >= aW for x in a_t), len(a_t), ps_t, pi_t, c["dur_s"]))
            pr("RIVAL variante=%s ruido=%.2f regla_a_mano_cruda=%.4f por_clase=%s falsa_alarma_pasa=%.3f | H3 W contra regla %d contra %d p=%.3g -> %s | "
               "ridge_crudo_entrenado(descriptivo)=%.4f" % (
                   v, s, aR, ",".join("%.3f" % x for x in c["regla_por_clase"]), c["regla_falsa_alarma_pasa"], b1, c1, p1, h3,
                   c["ridge_crudo_entrenado"]))
            pr("DESCRIPTIVO_008_LITERAL variante=%s ruido=%.2f umbral_solo_ruido W=%.4f falsa_alarma_pasa=%.3f regla=%.4f falsa_alarma_pasa=%.3f" % (
                v, s, c["d008_W"], c["d008_W_falsa_alarma_pasa"], c["d008_regla"], c["d008_regla_falsa_alarma_pasa"]))

    claves = [(v, s, nul) for v in VARIANTES for s in RUIDOS for nul in ("SL", "T")]
    adj_sup = ept.holm([prim[(v, s)]["p_sup_" + nul] for v, s, nul in claves])
    adj_inf = ept.holm([prim[(v, s)]["p_inf_" + nul] for v, s, nul in claves])
    for (v, s, nul), x, y_ in zip(claves, adj_sup, adj_inf):
        prim[(v, s)]["holm_sup_" + nul] = float(x)
        prim[(v, s)]["holm_inf_" + nul] = float(y_)

    # controles
    s0 = RUIDOS[0]
    _, d_te, d_pasa, _ = datos("COMO_LPLC2", s0)
    repro = bool(np.array_equal(pred(W, idx_W, d_te, d_pasa)[0], pW_c[("COMO_LPLC2", s0)]))
    _, dA, dA_pasa, _ = datos("AGNOSTICA", s0)
    pA = pred(W, idx_W, dA, dA_pasa)[0]
    iguales = [bool(np.array_equal(pred(W, ix, dA, dA_pasa)[0], pA)) for ix in perms[:n_agn]]
    c_neg = all(iguales)
    c_pos = regla_c[("COMO_LPLC2", s0)] >= azar + MARGEN_POS
    pr("CONTROL_NEGATIVO entrada=AGNOSTICA W=%.4f T_identicos=%d/%d -> %s" % (acc(pA), sum(iguales), len(iguales), c_neg))
    pr("CONTROL_POSITIVO regla_a_mano COMO_LPLC2 ruido=%.2f = %.4f contra azar %.4f + %.2f -> %s" % (
        s0, regla_c[("COMO_LPLC2", s0)], azar, MARGEN_POS, c_pos))
    valido = bool(guard_sl and guard_t and repro and c_neg and c_pos)
    pr("CHEQUEO INSTRUMENTO guarda_SL=%s guarda_T=%s reproduce=%s control_negativo=%s control_positivo=%s -> %s" % (
        guard_sl, guard_t, repro, c_neg, c_pos, "VALIDO" if valido else "INVALIDO"))

    ver_v = {}
    for v in VARIANTES:
        vc = []
        for s in RUIDOS:
            c = prim[(v, s)]
            sup_both = c["holm_sup_SL"] < ALFA and c["holm_sup_T"] < ALFA
            sup_any = c["holm_sup_SL"] < ALFA or c["holm_sup_T"] < ALFA
            inf_any = c["holm_inf_SL"] < ALFA or c["holm_inf_T"] < ALFA
            if sup_both and not inf_any:
                x = "GANA"
            elif inf_any and not sup_any:
                x = "PIERDE"
            elif inf_any and sup_any:
                x = "MIXTO"
            else:
                x = "EMPATE"
            c["veredicto"] = x
            vc.append(x)
            pr("VEREDICTO_CELDA variante=%s ruido=%.2f holm_sup(SL,T)=(%.4f,%.4f) holm_inf(SL,T)=(%.4f,%.4f) -> %s" % (
                v, s, c["holm_sup_SL"], c["holm_sup_T"], c["holm_inf_SL"], c["holm_inf_T"], x))
        ver_v[v] = "GANA" if all(x == "GANA" for x in vc) else ("PIERDE" if "PIERDE" in vc else "EMPATE")
        pr("VEREDICTO_VARIANTE %s -> %s" % (v, ver_v[v]))
    ng = sum(x == "GANA" for x in ver_v.values())
    glob = "PAGAN LAS LINEAS ETIQUETADAS" if ng == len(VARIANTES) else ("DEPENDE DE LPLC4" if ng else "NO PAGAN")
    pierde = [v for v in VARIANTES if ver_v[v] == "PIERDE"]
    if pierde:
        glob += " (PIERDE en %s)" % ",".join(pierde)
    pr("VEREDICTO_GLOBAL -> %s" % glob)
    pr("BYTES lector_lineas=4 umbrales (16 B en float32)")
    res["celdas"] = {"%s|%.2f" % k: x for k, x in prim.items()}
    res.update(controles=dict(reproduce=repro, control_negativo=c_neg, control_positivo=c_pos),
               veredicto_variante=ver_v, veredicto_global=glob, valido=valido)
    ruta = os.path.join(a.out, "resultados.json")
    with open(ruta, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True, default=float)
    pr("escrito resultados.json md5=" + base.md5(ruta))
    pr("# duracion_s=%.1f" % (time.time() - t0))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
