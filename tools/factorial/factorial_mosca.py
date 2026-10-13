#!/usr/bin/env python3
"""Factorial de la tarea de la mosca: que le cierra la brecha a la mosca simulada (respuesta 2026-10-12-019).

Pregunta. En la 015 el cableado real (W) les gano a 300 SL y 300 T en 6/6 celdas, pero la regla a mano le gano
en 4 y empato en 2. La regla son las mismas etiquetas de la mosca (tipo visual -> descendente) leidas sobre las
entradas sin pesos ni dinamica (018). Este experimento pregunta que factor del modelo cierra esa brecha.

Factores (9 configuraciones; una por corrida, --config):
  RECORTE   M46: el motivo de la 015 (46 neuronas, 0 aristas inhibitorias).
            R1:  las 6 descendentes de la 015 mas todas las neuronas con una arista de 5 sinapsis o mas sobre
                 alguna de ellas, con todas las aristas de FlyWire v783 entre ellas y su signo (018: 1.504
                 neuronas, 91.484 aristas).
  INHIBICION (solo R1) CON: el signo del pipeline (columna Excitatory). SIN: se borran las aristas negativas.
            M46 no tiene aristas inhibitorias: CON y SIN son lo mismo y corre una sola vez.
  NEURONA   TASA: la de la 015, z <- (1 - t) z + t tanh(W z + x), t = dt/tau, tau fija heterogenea (semilla 0),
                 W llevada a radio espectral 0.9.
            LIQ:  la liquida nativa de SparseLTC (mojo-absoluto, connectome_ltc.hpp: tau_ef = tau / (1 +
                 tau_gain |drive|)), sin entrenar, tau_gain = 1.0 (el defecto del codigo es 0, que la apaga;
                 1.0 es eleccion declarada, sin ajuste), t = min(1, dt / tau_ef).
            LIF:  integrar y disparar con signo de Shiu et al. 2024 (v_rest -52 mV, v_th -45, v_reset -52,
                 tau_m 20 ms, tau_syn 5 ms, refractario 2,2 ms, retardo 1,8 ms, w_syn 0,275 mV por sinapsis por
                 signo), sin escalar W. Simplificaciones declaradas: paso de 1 ms (Shiu usa 0,1 ms), refractario y
                 retardo redondeados a 2 pasos, entrada como corriente G_IN x drive (14 mV por unidad; no Poisson).
                 La linea de cada descendente es su cuenta de disparos en cada paso de 20 ms.
Tarea, entradas, lector y umbrales: los de la 015 sin cambios (modulo importado; md5 verificado). En R1 reciben
entrada las neuronas de los 4 tipos sintonizados (LC4, LPLC2, LPLC4, LPLC1) de cada lado; las 40 de la 015 con
el mismo ruido (semillas 101 y 102) y las demas con ruido de semillas 103 y 104. Las otras visuales y las
centrales no reciben entrada externa. La regla a mano es la de la 015 (las mismas 40 entradas), igual en las 9.

Primaria (por configuracion, 6 celdas A x ruido): H3 = W contra la regla, McNemar exacto por celda, Holm sobre
las 6 celdas. Veredicto contra el diseno: PIERDE si alguna celda PEOR tras Holm; SUPERA si ninguna PEOR y alguna
MEJOR; IGUALA si ninguna de las dos.
Secundaria descriptiva (celda A 0.3, ruido 0.15): W contra SL y T (50 y 50; 20 y 20 con LIF), p por rango.
Contrastes y veredicto global: tools/factorial/agregar_factorial.py sobre los 9 json.
Controles: REPRODUCE_015 (M46_TASA y la regla dan los 12 aciertos del log de la 015 con tolerancia de 2 ensayos
de 2000, porque otra CPU puede redondear distinto; tambien se imprime si son exactos); R1 con
1.504 neuronas y 91.484 aristas y conteniendo al M46; SIN sin aristas negativas; guardas SL (grados y lados) y
T (tipos por lado); LIF_RESPONDE (en la celda de nulos, la tasa de DNp01 ante looming posada supera a NADA).
Salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd
import scipy.sparse as sp

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "escape_aterrizaje"))
import tarea_mosca as tm  # noqa: E402  sello de la 015 (57d094a), sin cambios

base, ept = tm.base, tm.ept
MD5_TM = "40d64e074d9163753439307c5be4ac5e"
CONFIGS = ("M46_TASA", "M46_LIQ", "M46_LIF", "R1_CON_TASA", "R1_CON_LIQ", "R1_CON_LIF",
           "R1_SIN_TASA", "R1_SIN_LIQ", "R1_SIN_LIF")
CELDAS = [(A, s) for A in tm.AMPLITUDES for s in tm.RUIDOS]
CELDA_NULOS = (0.3, 0.15)
N_NULO = {"TASA": 50, "LIQ": 50, "LIF": 20}
G_LIQ = 1.0
V_REST, V_RESET, V_TH, TAU_M, TAU_SYN, T_REF, T_DLY, W_SYN = -52.0, -52.0, -45.0, 20.0, 5.0, 2.2, 1.8, 0.275
DT_LIF, G_IN = 1.0, 14.0
SUB = int(round(base.DT * 1000.0 / DT_LIF))
REF_SUB, DLY_SUB = int(round(T_REF / DT_LIF)), int(round(T_DLY / DT_LIF))
REPRO_015 = {(0.0, 0.15): (0.9005, 0.9195), (0.0, 0.45): (0.8805, 0.8705), (0.3, 0.15): (0.9125, 0.9325),
             (0.3, 0.45): (0.8915, 0.8935), (0.6, 0.15): (0.8680, 0.9315), (0.6, 0.45): (0.8580, 0.9120)}
R1_ESPERADO = (1504, 91484)


def pr(s):
    print(s, flush=True)


def sujeto(conn_p, annot_p, recorte, inhib):
    sel, ar46 = tm.construir(conn_p, annot_p)
    n46 = len(sel)
    nv46 = n46 - 6
    m46 = [s[0] for s in sel]
    if recorte == "M46":
        return dict(ids=m46, tipos=[s[1] for s in sel], lados=["L" if s[2] == "left" else "R" for s in sel],
                    aristas=ar46, n_ent=nv46, nv46=nv46, n_inh_crudo=0, contiene_m46=True)
    a = pd.read_csv(annot_p, sep="\t", dtype=str, usecols=["root_id", "cell_type", "side"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(conn_p, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    dns = m46[nv46:]
    pre = c[(c.Connectivity >= 5) & c.Postsynaptic_ID.isin(dns)].Presynaptic_ID.unique()
    U = set(dns) | set(int(x) for x in pre)
    tipo = {int(r): (t if isinstance(t, str) else "") for r, t in zip(a.root_id, a.cell_type)}
    lado = {int(r): (s if isinstance(s, str) else "") for r, s in zip(a.root_id, a.side)}
    resto = sorted(U - set(m46))
    extra = [r for r in resto if tipo.get(r, "") in tm.TIPOS and lado.get(r, "") in ("left", "right")]
    sx = set(extra)
    otros = [r for r in resto if r not in sx]
    ids = m46[:nv46] + extra + otros + dns
    ix = {r: i for i, r in enumerate(ids)}
    sub = c[c.Presynaptic_ID.isin(U) & c.Postsynaptic_ID.isin(U)]
    ar = [(ix[int(p)], ix[int(q)], float(w * e)) for p, q, w, e in sub.itertuples(index=False)]
    n_inh = sum(1 for _, _, w in ar if w < 0)
    if inhib == "SIN":
        ar = [x for x in ar if x[2] > 0]
    cod = {"left": "L", "right": "R"}
    tipos = [tipo.get(r, "") for r in ids]
    lados = [cod.get(lado.get(r, ""), "C") for r in ids]
    for i, s in enumerate(sel):
        tipos[ids.index(s[0])] = s[1]
    return dict(ids=ids, tipos=tipos, lados=lados, aristas=ar, n_ent=nv46 + len(extra), nv46=nv46,
                n_inh_crudo=n_inh, contiene_m46=set(m46) <= U, n_U=len(U), n_ar_crudo=len(sub))


def matriz_tasa(n, ar):
    if n <= 64:
        return base.matriz(n, ar)[0]
    p = np.array([x[0] for x in ar]); q = np.array([x[1] for x in ar]); w = np.array([x[2] for x in ar])
    W = sp.coo_matrix((w, (q, p)), shape=(n, n)).tocsr()
    r = np.abs(np.linalg.eigvals(W.toarray())).max()
    return (W * (base.RHO / r)).tocsr()


def matriz_lif(n, ar):
    p = np.array([x[0] for x in ar]); q = np.array([x[1] for x in ar]); w = np.array([x[2] for x in ar])
    return sp.coo_matrix((W_SYN * w, (q, p)), shape=(n, n)).tocsr()


def sim_tasa(W, tau, n_ent, chan, d, liq):
    n_tr = len(d["y"])
    N = W.shape[0]
    t0 = base.DT / tau
    z = np.zeros((n_tr, N))
    out = np.zeros((n_tr, tm.T, 6))
    for t in range(tm.T):
        x = np.zeros((n_tr, N))
        x[:, :n_ent] = d["drive"][:, t, :][:, chan] + d["ruido"][:, t, :]
        rec = (W @ z.T).T if sp.issparse(W) else z @ W.T
        u = rec + x
        tt = np.minimum(1.0, t0[None, :] * (1.0 + G_LIQ * np.abs(u))) if liq else t0
        z = (1 - tt) * z + tt * np.tanh(u)
        out[:, t, :] = z[:, N - 6:]
    return out


def sim_lif(Wl, n_ent, chan, d):
    n_tr = len(d["y"])
    N = Wl.shape[0]
    WT = Wl.T.tocsr()
    v = np.full((n_tr, N), V_REST)
    g = np.zeros((n_tr, N))
    ref = np.zeros((n_tr, N), dtype=np.int16)
    cola = [None] * DLY_SUB
    out = np.zeros((n_tr, tm.T, 6))
    for t in range(tm.T):
        I = np.zeros((n_tr, N))
        I[:, :n_ent] = G_IN * (d["drive"][:, t, :][:, chan] + d["ruido"][:, t, :])
        for _ in range(SUB):
            llegan = cola.pop(0)
            if llegan is not None and llegan.nnz:
                g += (llegan @ WT).toarray()
            g -= DT_LIF * g / TAU_SYN
            v += DT_LIF * ((g + I) - (v - V_REST)) / TAU_M
            en_ref = ref > 0
            v[en_ref] = V_RESET
            ref[en_ref] -= 1
            disp = v > V_TH
            v[disp] = V_RESET
            ref[disp] = REF_SUB
            out[:, t, :] += disp[:, N - 6:]
            cola.append(sp.csr_matrix(disp.astype(np.float64)) if disp.any() else None)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", required=True, choices=CONFIGS)
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    partes = a.config.split("_")
    recorte, neurona = partes[0], partes[-1]
    inhib = partes[1] if recorte == "R1" else "CON"
    pr("# maquina: %s | %s | Python %s | numpy %s | pandas %s" % (platform.node(), platform.platform(),
       platform.python_version(), np.__version__, pd.__version__))
    pr("# config: %s (recorte %s, inhibicion %s, neurona %s)" % (a.config, recorte, inhib, neurona))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    mt = base.md5(os.path.abspath(tm.__file__))
    pr("# md5 modulo 015 = %s" % mt)
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mt != MD5_TM:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_train, n_test = (60, 40) if humo else (tm.N_TRAIN, tm.N_TEST)
    n_nulo = 2 if humo else N_NULO[neurona]

    S = sujeto(a.conn, a.annot, recorte, inhib)
    ids, tipos, lados, ar = S["ids"], S["tipos"], S["lados"], S["aristas"]
    n, n_ent, nv46 = len(ids), S["n_ent"], S["nv46"]
    guardas = {}
    if recorte == "R1":
        guardas["R1_tamano"] = bool((S["n_U"], S["n_ar_crudo"]) == R1_ESPERADO and S["contiene_m46"])
        pr("SUJETO R1 neuronas=%d aristas_crudas=%d inhibitorias_crudas=%d contiene_M46=%s esperado=%s -> %s" % (
            S["n_U"], S["n_ar_crudo"], S["n_inh_crudo"], S["contiene_m46"], R1_ESPERADO, guardas["R1_tamano"]))
    n_neg = sum(1 for _, _, w in ar if w < 0)
    if inhib == "SIN" or recorte == "M46":
        guardas["sin_negativas"] = n_neg == 0
    pr("SUJETO neuronas=%d con_entrada=%d aristas=%d inhibitorias=%d sinapsis=%d" % (
        n, n_ent, len(ar), n_neg, int(sum(abs(w) for _, _, w in ar))))
    for t in tm.TIPOS:
        pr("SUJETO tipo=%s con_entrada_por_lado=(%d,%d)" % (t, sum(1 for i in range(n_ent) if tipos[i] == t and lados[i] == "L"),
                                                         sum(1 for i in range(n_ent) if tipos[i] == t and lados[i] == "R")))

    def cod_de(i, tipo):
        return (0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipo)
    chan = np.array([cod_de(i, tipos[i]) for i in range(n_ent)])
    chan46 = chan[:nv46]
    tau = 0.06 + 0.12 * np.random.default_rng(0).random(n)

    def red(arx):
        return matriz_lif(n, arx) if neurona == "LIF" else matriz_tasa(n, arx)

    def simular(Wm, ch, d):
        if neurona == "LIF":
            return sim_lif(Wm, n_ent, ch, d)
        if recorte == "M46" and neurona == "TASA":
            return tm.simular(Wm, tau, ch, d, nv46)
        return sim_tasa(Wm, tau, n_ent, ch, d, liq=(neurona == "LIQ"))

    etr, ete = tm.generar(n_train, 1), tm.generar(n_test, 2)
    ytr, yte, vtr, vte = etr["y"], ete["y"], etr["vuelo"], ete["vuelo"]
    Ztr = np.random.default_rng(101).standard_normal((n_train, tm.T, nv46))
    Zte = np.random.default_rng(102).standard_normal((n_test, tm.T, nv46))
    if n_ent > nv46:
        Ztr = np.concatenate([Ztr, np.random.default_rng(103).standard_normal((n_train, tm.T, n_ent - nv46))], axis=2)
        Zte = np.concatenate([Zte, np.random.default_rng(104).standard_normal((n_test, tm.T, n_ent - nv46))], axis=2)
    pr("DATOS entrenamiento=%d prueba=%d nulos_por_tipo=%d celda_nulos=%s" % (n_train, n_test, n_nulo, CELDA_NULOS))

    def datos(A, s):
        return (dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr), dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * Zte))

    def pred(Wm, ch, dtr, dte):
        th = tm.umbrales(tm.lineas(simular(Wm, ch, dtr)), ytr, vtr)
        Ste = simular(Wm, ch, dte)
        return tm.carrera(tm.lineas(Ste), th, vte), Ste

    def media(X, ld, ts):
        m = np.array([lados[i] == ld and tipos[i] in ts for i in range(nv46)])
        return X[:, :, m].mean(2)

    def regla(dtr, dte):
        def lc(d):
            X = d["drive"][:, :, chan46] + d["ruido"][:, :, :nv46]
            return np.stack([media(X, "L", ("LC4", "LPLC2")), media(X, "R", ("LC4", "LPLC2")),
                             media(X, "L", ("LPLC4",)), media(X, "R", ("LPLC4",)),
                             media(X, "L", ("LPLC1", "LPLC2")), media(X, "R", ("LPLC1", "LPLC2"))], axis=2)
        th = tm.umbrales(tm.lineas(lc(dtr)), ytr, vtr)
        return tm.carrera(tm.lineas(lc(dte)), th, vte)

    def acc(p):
        return float((p == yte).mean())

    def por_cond(p):
        return [float((p[(vte == v) & (ete["est"] == k)] == yte[(vte == v) & (ete["est"] == k)]).mean())
                for v in (False, True) for k in range(5)]

    W = red(ar)
    res = dict(config=a.config, recorte=recorte, inhibicion=inhib, neurona=neurona, humo=humo, celdas={})
    pr("ORDEN por_condicion = posada(%s) | vuelo(%s)" % (",".join(tm.ESTIMULOS), ",".join(tm.ESTIMULOS)))
    repro = []
    for A, s in CELDAS:
        tc = time.time()
        dtr, dte = datos(A, s)
        pW, Ste = pred(W, chan, dtr, dte)
        pR = regla(dtr, dte)
        b1, c1, p1 = base.mcnemar(pW == yte, pR == yte)
        aW, aR = acc(pW), acc(pR)
        repro.append((abs(aW - REPRO_015[(A, s)][0]) <= 0.001 + 1e-9 and abs(aR - REPRO_015[(A, s)][1]) <= 0.001 + 1e-9,
                      (round(aW, 4), round(aR, 4)) == REPRO_015[(A, s)]))
        actividad = float(Ste.std())
        res["celdas"]["%.1f|%.2f" % (A, s)] = dict(W=aW, regla=aR, W_por_condicion=por_cond(pW),
                                                   regla_por_condicion=por_cond(pR), H3_W=b1, H3_regla=c1, H3_p=p1,
                                                   pred_W=pW.tolist(), actividad_DN_std=actividad,
                                                   dur_s=time.time() - tc)
        pr("CELDA A=%.1f ruido=%.2f W=%.4f regla=%.4f H3 W contra regla %d contra %d p=%.3g actividad_DN_std=%.4f "
           "por_condicion_W=%s | %.1f s" % (A, s, aW, aR, b1, c1, p1, actividad,
                                            ",".join("%.3f" % x for x in por_cond(pW)), time.time() - tc))
        if (A, s) == CELDA_NULOS and neurona == "LIF":
            loom = (~vte) & (ete["est"] <= 1)
            nada = (~vte) & (ete["est"] == 4)
            r_loom, r_nada = float(Ste[loom][:, :, :2].mean()), float(Ste[nada][:, :, :2].mean())
            guardas["LIF_responde"] = bool(r_loom > r_nada and r_loom > 0)
            pr("CHEQUEO LIF_RESPONDE DNp01 disparos_por_paso looming_posada=%.4f nada_posada=%.4f -> %s" % (
                r_loom, r_nada, guardas["LIF_responde"]))
    if recorte == "M46" and neurona == "TASA":
        guardas["REPRODUCE_015"] = bool(all(r[0] for r in repro)) if not humo else True
        pr("CHEQUEO REPRODUCE_015 tolerancia=%s exacto=%s -> %s" % ("no aplica en humo" if humo else [r[0] for r in repro],
           "no aplica en humo" if humo else [r[1] for r in repro], guardas["REPRODUCE_015"]))

    A0, s0 = CELDA_NULOS
    dtr, dte = datos(A0, s0)
    aW0 = res["celdas"]["%.1f|%.2f" % (A0, s0)]["W"]
    rng = np.random.default_rng(7)
    gi0, go0 = base.grados(n, ar)
    a_sl, guard_sl = [], True
    for k in range(n_nulo):
        arx = base.barajar_sl(ar, lados, rng)
        gi, go = base.grados(n, arx)
        guard_sl &= bool((gi == gi0).all() and (go == go0).all() and
                         all((lados[p], lados[q]) == (lados[p0], lados[q0]) for (p, q, _), (p0, q0, _) in zip(arx, ar)))
        a_sl.append(acc(pred(red(arx), chan, dtr, dte)[0]))
    rng_t = np.random.default_rng(11)
    a_t, guard_t = [], True
    for k in range(n_nulo):
        tp = list(tipos[:n_ent])
        for ld in ("L", "R"):
            ix = [i for i in range(n_ent) if lados[i] == ld]
            vals = [tp[i] for i in ix]
            for i, j in zip(ix, rng_t.permutation(len(ix))):
                tp[i] = vals[j]
        guard_t &= bool(tp != tipos[:n_ent])
        ch = np.array([cod_de(i, tp[i]) for i in range(n_ent)])
        a_t.append(acc(pred(W, ch, dtr, dte)[0]))
    guardas["SL"], guardas["T"] = guard_sl, guard_t
    ps_sl, pi_sl = ept.p_rango(aW0, a_sl)
    ps_t, pi_t = ept.p_rango(aW0, a_t)
    res["nulos"] = dict(celda=list(CELDA_NULOS), W=aW0, SL=a_sl, T=a_t, p_sup_SL=ps_sl, p_sup_T=ps_t, p_inf_SL=pi_sl, p_inf_T=pi_t)
    pr("NULOS_DESCRIPTIVO A=%.1f ruido=%.2f W=%.4f | SL n=%d media=%.4f max=%.4f p_sup=%.4f | T n=%d media=%.4f max=%.4f p_sup=%.4f" % (
        A0, s0, aW0, len(a_sl), np.mean(a_sl), np.max(a_sl), ps_sl, len(a_t), np.mean(a_t), np.max(a_t), ps_t))
    valido = all(guardas.values())
    res["guardas"], res["valido"] = guardas, valido
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % kv for kv in guardas.items()), "VALIDO" if valido else "INVALIDO"))
    ruta = os.path.join(a.out, "factorial_%s.json" % a.config)
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), base.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t_ini))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
