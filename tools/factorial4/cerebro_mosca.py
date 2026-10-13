#!/usr/bin/env python3
"""Factorial 4 de la mosca: el banco con el cerebro entero de FlyWire v783 (138.639 neuronas, 15.091.983 aristas),
en Kaggle con GPU (respuesta 2026-10-13-015). Sellado antes de correr.

Pregunta. En R2 (33.489 neuronas) la red alcanza a la regla con sus mismos sensores (+0,85, IC90 [+0,08; +1,51],
factorial 3) y le gana a sus barajados. Con el cerebro entero: ¿la supera por mas del margen, sigue empatando o
pierde? ¿Agrega algo pasar de R2 al cerebro entero? ¿Le sigue ganando a sus barajados?

Sujeto CE: todas las neuronas del archivo de conectividad, con el mismo armado que factorial2_mosca.sujeto (las
entradas son las 40 visuales del motivo mas toda neurona de los tipos sintonizados con lado; las 6 descendentes van
al final; pesos = sinapsis por signo; radio espectral llevado a 0,9). La red es la de tasa con inhibicion (la
configuracion R2_CON_TASA del factorial 3). La tarea, los datos, el ruido y la tau por root_id, el lector y la
regla son los de factorial2_mosca.py (sellado en 9442fdf, md5 798a824c), importado sin cambios.

Lo unico nuevo es el motor: la misma cuenta de factorial2_mosca.sim escrita en torch (float64) para correr en la
GPU de Kaggle. Por eso los controles comparan torch contra el numpy sellado en la misma maquina:
  SUJETO_IGUAL_F2  el armado generalizado da exactamente el sujeto R1 de factorial2_mosca.sujeto.
  CE_tamano        138.639 neuronas y 15.091.983 aristas; contiene M46 y R1.
  PARIDAD_R1       16 ensayos: torch y numpy dan las mismas trazas de las descendentes (max dif < 1e-9).
  PARIDAD_CE       4 ensayos del cerebro entero: idem.
  REPRO_R2         (con --repro_r2) R2 en tau 0, prueba 2, celda 0,3|0,15 por el motor torch da 0,9465, el
                   numero del factorial 3 en Actions (tolerancia 0,001).
  SL_IGUAL_MODULO  (nulos) el barajado numpy del factorial 3 da lo mismo que base.barajar_sl en R1.
Modos: verificar (controles y tiempos), grilla, nulos (SL o T, en la celda A 0,3 ruido 0,15, tau 0, prueba 2).
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

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "factorial2"))
sys.path.insert(0, os.path.join(AQUI, "..", "factorial3"))
import factorial2_mosca as f2  # noqa: E402  sellado en 9442fdf, sin cambios
import nulos_r2 as n3  # noqa: E402  sellado en 6a7b4cb, sin cambios
import torch  # noqa: E402

tm, base = f2.tm, f2.base
MD5_F2 = "798a824cd47808155fa12adb9e652dac"
MD5_N3 = "c4f1c4d39c99f07cb9ad7977b6f3b01a"
CE_ESPERADO = (138639, 15091983)
R2_REF = 0.9465
CELDA_N, TAU_N, PRUEBA_N = (0.3, 0.15), 0, 2


def pr(s):
    print(s, flush=True)


def sujeto_gen(conn_p, annot_p, alcance):
    """factorial2_mosca.sujeto con inhibicion CON, generalizado: alcance R1, R2 o CE (todo el archivo)."""
    sel, ar46 = tm.construir(conn_p, annot_p)
    nv46 = len(sel) - 6
    m46 = [s[0] for s in sel]
    a = pd.read_csv(annot_p, sep="\t", dtype=str, usecols=["root_id", "cell_type", "side"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(conn_p, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    dns = m46[nv46:]
    c5 = c[c.Connectivity >= 5]
    U1 = set(dns) | set(int(x) for x in c5[c5.Postsynaptic_ID.isin(dns)].Presynaptic_ID.unique())
    if alcance == "R1":
        U = U1
    elif alcance == "R2":
        U = U1 | set(int(x) for x in c5[c5.Postsynaptic_ID.isin(list(U1))].Presynaptic_ID.unique())
    else:
        U = set(int(x) for x in c.Presynaptic_ID.unique()) | set(int(x) for x in c.Postsynaptic_ID.unique())
    del c5
    tipo = {int(r): (t if isinstance(t, str) else "") for r, t in zip(a.root_id, a.cell_type)}
    lado = {int(r): (s if isinstance(s, str) else "") for r, s in zip(a.root_id, a.side)}
    resto = sorted(U - set(m46))
    extra = [r for r in resto if tipo.get(r, "") in tm.TIPOS and lado.get(r, "") in ("left", "right")]
    sx = set(extra)
    otros = [r for r in resto if r not in sx]
    ids = m46[:nv46] + extra + otros + dns
    ix = pd.Series(np.arange(len(ids)), index=np.array(ids, dtype=np.int64))
    Ul = list(U)
    sub = c[c.Presynaptic_ID.isin(Ul) & c.Postsynaptic_ID.isin(Ul)]
    del c
    p = ix[sub.Presynaptic_ID.values].values
    q = ix[sub.Postsynaptic_ID.values].values
    w = (sub.Connectivity.values * sub.Excitatory.values).astype(np.float64)
    n_ar_crudo = len(sub)
    n_inh = int((w < 0).sum())
    cod = {"left": "L", "right": "R"}
    tipos = [tipo.get(r, "") for r in ids]
    lados = [cod.get(lado.get(r, ""), "C") for r in ids]
    pos = {r: i for i, r in enumerate(ids)}
    for s in sel:
        tipos[pos[s[0]]] = s[1]
    return dict(ids=ids, tipos=tipos, lados=lados, aristas=(p, q, w), n_ent=nv46 + len(extra), nv46=nv46,
                n_inh_crudo=n_inh, contiene_m46=set(m46) <= U, contiene_r1=U1 <= U, n_U=len(U),
                n_ar_crudo=n_ar_crudo)


def igual_sujeto(A, B):
    return bool(A["ids"] == B["ids"] and A["tipos"] == B["tipos"] and A["lados"] == B["lados"] and
                A["n_ent"] == B["n_ent"] and all(np.array_equal(x, y) for x, y in zip(A["aristas"], B["aristas"])))


def a_torch(W, dev):
    Wc = W.tocsr()
    return torch.sparse_csr_tensor(torch.from_numpy(Wc.indptr.astype(np.int64)), torch.from_numpy(Wc.indices.astype(np.int64)),
                                   torch.from_numpy(Wc.data.astype(np.float64)), size=Wc.shape, dtype=torch.float64,
                                   device=dev)


def sim_torch(Wt, tau, n_ent, chan, d, idx, dev):
    """La cuenta de factorial2_mosca.sim con neurona de tasa (liq False), en torch float64; estado en columnas."""
    N = Wt.shape[0]
    t0 = torch.as_tensor(base.DT / tau, dtype=torch.float64, device=dev)[:, None]
    ch = torch.as_tensor(chan, dtype=torch.long, device=dev)
    dr = torch.as_tensor(d["drive"][idx], dtype=torch.float64, device=dev)
    ru = torch.as_tensor(d["ruido"][idx], dtype=torch.float64, device=dev)
    z = torch.zeros((N, len(idx)), dtype=torch.float64, device=dev)
    out = torch.zeros((len(idx), tm.T, 6), dtype=torch.float64, device=dev)
    for t in range(tm.T):
        u = torch.sparse.mm(Wt, z)
        u[:n_ent, :] += (dr[:, t, :][:, ch] + ru[:, t, :]).T
        z = (1 - t0) * z + t0 * torch.tanh(u)
        out[:, t, :] = z[N - 6:, :].T
    return out.cpu().numpy()


def sim_torch_trozos(Wt, tau, n_ent, chan, d, dev, trozo):
    n_tr = len(d["y"])
    return np.concatenate([sim_torch(Wt, tau, n_ent, chan, d, np.arange(i, min(n_tr, i + trozo)), dev)
                           for i in range(0, n_tr, trozo)], axis=0)


def chan_de(tipos, lados, n_ent):
    return np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(n_ent)])


def paridad(S, W, dev, k, sem_tau=0):
    ids, n_ent = S["ids"], S["n_ent"]
    chan = chan_de(S["tipos"], S["lados"], n_ent)
    e = tm.generar(k, f2.SEM_GEN_TR)
    Z = f2.ruido_por_root(ids[:n_ent], k, f2.SEM_RUIDO_TR)
    A, s = CELDA_N
    d = dict(y=e["y"], drive=tm.sintonias(e, A), ruido=s * Z)
    tau = f2.tau_por_root(ids, sem_tau)
    t1 = time.time()
    xn = f2.sim(W, tau, n_ent, chan, d, False)
    t2 = time.time()
    xt = sim_torch(a_torch(W, dev), tau, n_ent, chan, d, np.arange(k), dev)
    t3 = time.time()
    return float(np.abs(xn - xt).max()), t2 - t1, t3 - t2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--modo", required=True, choices=("verificar", "grilla", "nulos"))
    ap.add_argument("--taus", default="0")
    ap.add_argument("--pruebas", default="2")
    ap.add_argument("--celdas", default="todas")
    ap.add_argument("--etiqueta", default="")
    ap.add_argument("--tipo", choices=("SL", "T"))
    ap.add_argument("--k0", type=int, default=0)
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--real", action="store_true")
    ap.add_argument("--repro_r2", action="store_true")
    ap.add_argument("--trozo", type=int, default=500)
    ap.add_argument("--dispositivo", default="cuda")
    ap.add_argument("--medir_ensayos", type=int, default=0, help="verificar: ensayos para medir s/ensayo en el CE")
    ap.add_argument("--humo", action="store_true", help="corrida corta de humo: numeros sin valor")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    dev = torch.device(a.dispositivo if (a.dispositivo != "cuda" or torch.cuda.is_available()) else "cpu")
    gpu = torch.cuda.get_device_name(0) if dev.type == "cuda" else "-"
    pr("# maquina: %s | %s | Python %s | numpy %s | pandas %s | torch %s | dispositivo %s %s" % (
        platform.node(), platform.platform(), platform.python_version(), np.__version__, pd.__version__,
        torch.__version__, dev, gpu))
    pr("# md5 script = " + base.md5(os.path.abspath(__file__)))
    m2, m3, mt = base.md5(os.path.abspath(f2.__file__)), base.md5(os.path.abspath(n3.__file__)), base.md5(os.path.abspath(tm.__file__))
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    pr("# md5 factorial2_mosca = %s | nulos_r2 = %s | modulo 015 = %s | conn = %s | annot = %s" % (m2, m3, mt, mc, ma))
    if mc != base.MD5_CONN or ma != base.MD5_ANNOT or mt != f2.MD5_TM or m2 != MD5_F2 or m3 != MD5_N3:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    if a.dispositivo == "cuda" and dev.type != "cuda":
        pr("# AVISO: no hay GPU; corre en CPU")
    humo = a.humo
    if humo:
        pr("# HUMO: corrida corta, estos numeros no valen")
    n_train, n_test = (120, 80) if humo else (tm.N_TRAIN, tm.N_TEST)
    guardas, info = {}, {}

    # control del armado generalizado contra el sellado, en R1
    tc = time.time()
    S1 = f2.sujeto(a.conn, a.annot, "R1", "CON")
    G1 = sujeto_gen(a.conn, a.annot, "R1")
    guardas["SUJETO_IGUAL_F2"] = igual_sujeto(S1, G1)
    pr("CHEQUEO SUJETO_IGUAL_F2 (R1) -> %s | %.1f s" % (guardas["SUJETO_IGUAL_F2"], time.time() - tc))
    W1, _ = f2.matriz(len(S1["ids"]), S1["aristas"], densa_ok=False)
    d1, tn, tt = paridad(S1, W1, dev, 16)
    guardas["PARIDAD_R1"] = bool(d1 < 1e-9)
    pr("CHEQUEO PARIDAD_R1 (16 ensayos) max_dif=%.3g numpy=%.1f s torch=%.1f s -> %s" % (d1, tn, tt, guardas["PARIDAD_R1"]))
    if a.modo == "nulos":
        p1, q1, w1 = S1["aristas"]
        ref = base.barajar_sl(list(zip(p1.tolist(), q1.tolist(), w1.tolist())), S1["lados"], np.random.default_rng([n3.SEM_SL, 0]))
        mio = n3.barajar_sl_np(p1, q1, n3.codigos(S1["lados"]), np.random.default_rng([n3.SEM_SL, 0]))
        guardas["SL_IGUAL_MODULO"] = bool(np.array_equal(np.array([x[1] for x in ref]), mio))
        pr("CHEQUEO SL_IGUAL_MODULO (R1) -> %s" % guardas["SL_IGUAL_MODULO"])
        del ref
    del S1, G1, W1

    if a.repro_r2:
        tc = time.time()
        S2 = f2.sujeto(a.conn, a.annot, "R2", "CON")
        W2, _ = f2.matriz(len(S2["ids"]), S2["aristas"], densa_ok=False)
        ids2, ne2 = S2["ids"], S2["n_ent"]
        ch2 = chan_de(S2["tipos"], S2["lados"], ne2)
        tau2 = f2.tau_por_root(ids2, TAU_N)
        etr = tm.generar(tm.N_TRAIN, f2.SEM_GEN_TR)
        ete = tm.generar(tm.N_TEST, PRUEBA_N)
        A, s = CELDA_N
        dtr = dict(y=etr["y"], drive=tm.sintonias(etr, A), ruido=s * f2.ruido_por_root(ids2[:ne2], tm.N_TRAIN, f2.SEM_RUIDO_TR))
        dte = dict(y=ete["y"], drive=tm.sintonias(ete, A), ruido=s * f2.ruido_por_root(ids2[:ne2], tm.N_TEST, 1000 + PRUEBA_N))
        W2t = a_torch(W2, dev)
        th = tm.umbrales(tm.lineas(sim_torch_trozos(W2t, tau2, ne2, ch2, dtr, dev, a.trozo)), etr["y"], etr["vuelo"])
        pW = tm.carrera(tm.lineas(sim_torch_trozos(W2t, tau2, ne2, ch2, dte, dev, a.trozo)), th, ete["vuelo"])
        r2 = float((pW == ete["y"]).mean())
        guardas["REPRO_R2"] = bool(abs(r2 - R2_REF) <= 0.001 + 1e-9)
        info["repro_r2"] = r2
        pr("CHEQUEO REPRO_R2 torch=%.4f factorial3=%.4f -> %s | %.1f s" % (r2, R2_REF, guardas["REPRO_R2"], time.time() - tc))
        del S2, W2, W2t, dtr, dte

    tc = time.time()
    S = sujeto_gen(a.conn, a.annot, "CE")
    ids, tipos, lados = S["ids"], S["tipos"], S["lados"]
    n, n_ent, nv46 = len(ids), S["n_ent"], S["nv46"]
    guardas["CE_tamano"] = bool((S["n_U"], S["n_ar_crudo"]) == CE_ESPERADO and S["contiene_m46"] and S["contiene_r1"])
    pr("SUJETO CE neuronas=%d aristas=%d inhibitorias=%d entradas=%d contiene_M46=%s contiene_R1=%s -> %s | %.1f s" % (
        S["n_U"], S["n_ar_crudo"], S["n_inh_crudo"], n_ent, S["contiene_m46"], S["contiene_r1"], guardas["CE_tamano"],
        time.time() - tc))
    for t_ in tm.TIPOS:
        pr("SUJETO tipo=%s con_entrada_por_lado=(%d,%d)" % (t_, sum(1 for i in range(n_ent) if tipos[i] == t_ and lados[i] == "L"),
                                                         sum(1 for i in range(n_ent) if tipos[i] == t_ and lados[i] == "R")))
    tc = time.time()
    W, radio = f2.matriz(n, S["aristas"], densa_ok=False)
    info["radio_crudo"], info["t_radio_s"] = radio, time.time() - tc
    pr("RADIO CE crudo=%.6f | %.1f s" % (radio, info["t_radio_s"]))
    d_ce, tn, tt = paridad(S, W, dev, 4)
    guardas["PARIDAD_CE"] = bool(d_ce < 1e-9)
    pr("CHEQUEO PARIDAD_CE (4 ensayos) max_dif=%.3g numpy=%.1f s torch=%.1f s -> %s" % (d_ce, tn, tt, guardas["PARIDAD_CE"]))
    Wt = a_torch(W, dev)
    chan = chan_de(tipos, lados, n_ent)
    res = dict(modo=a.modo, recorte="CE", inhibicion="CON", neurona="TASA", humo=humo, etiqueta=a.etiqueta, n_ent=n_ent,
               dispositivo=str(dev), gpu=gpu, torch=torch.__version__, numpy=np.__version__, trozo=a.trozo,
               dns_root=[int(r) for r in ids[n - 6:]], info=info)

    if a.modo == "verificar":
        if a.medir_ensayos:
            e = tm.generar(a.medir_ensayos, f2.SEM_GEN_TR)
            Z = f2.ruido_por_root(ids[:n_ent], a.medir_ensayos, f2.SEM_RUIDO_TR)
            dm = dict(y=e["y"], drive=tm.sintonias(e, 0.3), ruido=0.15 * Z)
            if dev.type == "cuda":
                torch.cuda.synchronize()
            tc = time.time()
            sim_torch_trozos(Wt, f2.tau_por_root(ids, 0), n_ent, chan, dm, dev, a.trozo)
            if dev.type == "cuda":
                torch.cuda.synchronize()
            info["s_por_ensayo"] = (time.time() - tc) / a.medir_ensayos
            pr("TIEMPO CE torch: %d ensayos, trozo %d -> %.4f s por ensayo" % (a.medir_ensayos, a.trozo, info["s_por_ensayo"]))
            if dev.type == "cuda":
                info["mem_max_gb"] = torch.cuda.max_memory_allocated() / 1e9
                pr("MEMORIA GPU max=%.2f GB" % info["mem_max_gb"])
    elif a.modo == "grilla":
        taus = [int(x) for x in a.taus.split(",")]
        pruebas = [int(x) for x in a.pruebas.split(",")]
        celdas = f2.CELDAS if a.celdas == "todas" else [tuple(float(v) for v in x.split("|")) for x in a.celdas.split(",")]
        etr = tm.generar(n_train, f2.SEM_GEN_TR)
        ytr, vtr = etr["y"], etr["vuelo"]
        Ztr = f2.ruido_por_root(ids[:n_ent], n_train, f2.SEM_RUIDO_TR)
        tau_s = {st: f2.tau_por_root(ids, st) for st in taus}

        def media(X, ld, ts, k):
            m = np.array([lados[i] == ld and tipos[i] in ts for i in range(k)])
            return X[:, :, m].mean(2)

        def lc(d, k):
            X = d["drive"][:, :, chan[:k]] + d["ruido"][:, :, :k]
            return np.stack([media(X, "L", ("LC4", "LPLC2"), k), media(X, "R", ("LC4", "LPLC2"), k),
                             media(X, "L", ("LPLC4",), k), media(X, "R", ("LPLC4",), k),
                             media(X, "L", ("LPLC1", "LPLC2"), k), media(X, "R", ("LPLC1", "LPLC2"), k)], axis=2)

        def regla(dtr, dte, vte, k):
            th = tm.umbrales(tm.lineas(lc(dtr, k)), ytr, vtr)
            return tm.carrera(tm.lineas(lc(dte, k)), th, vte)

        res.update(taus=taus, pruebas=pruebas, celdas=[f2.clave(*c) for c in celdas],
                   tau_DN={str(st): [float(x) for x in tau_s[st][n - 6:]] for st in taus}, corridas=[], reglas=[])
        for A, s in celdas:
            tc = time.time()
            dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * Ztr)
            th = {st: tm.umbrales(tm.lineas(sim_torch_trozos(Wt, tau_s[st], n_ent, chan, dtr, dev, a.trozo)), ytr, vtr)
                  for st in taus}
            for sem in pruebas:
                ete = tm.generar(n_test, sem)
                yte, vte = ete["y"], ete["vuelo"]
                dte = dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * f2.ruido_por_root(ids[:n_ent], n_test, 1000 + sem))
                pP, p40 = regla(dtr, dte, vte, n_ent), regla(dtr, dte, vte, nv46)
                aP, a40 = float((pP == yte).mean()), float((p40 == yte).mean())
                res["reglas"].append(dict(celda=f2.clave(A, s), prueba=sem, regla_propia=aP, regla40=a40,
                                          pred_regla_propia="".join(map(str, pP.tolist()))))
                for st in taus:
                    pW = tm.carrera(tm.lineas(sim_torch_trozos(Wt, tau_s[st], n_ent, chan, dte, dev, a.trozo)), th[st], vte)
                    aW = float((pW == yte).mean())
                    b, c_, pm = base.mcnemar(pW == yte, pP == yte)
                    res["corridas"].append(dict(celda=f2.clave(A, s), tau=st, prueba=sem, W=aW, regla_propia=aP,
                                                regla40=a40, mcnemar_W=b, mcnemar_regla=c_, mcnemar_p=pm,
                                                pred_W="".join(map(str, pW.tolist()))))
                    pr("CORRIDA celda=%s tau=%d prueba=%d W=%.4f regla_propia=%.4f regla40=%.4f dif=%+.4f" % (
                        f2.clave(A, s), st, sem, aW, aP, a40, aW - aP))
            pr("# celda %s lista en %.1f s" % (f2.clave(A, s), time.time() - tc))
    else:
        etr = tm.generar(n_train, f2.SEM_GEN_TR)
        ytr, vtr = etr["y"], etr["vuelo"]
        ete = tm.generar(n_test, PRUEBA_N)
        yte, vte = ete["y"], ete["vuelo"]
        A, s = CELDA_N
        dtr = dict(y=ytr, drive=tm.sintonias(etr, A), ruido=s * f2.ruido_por_root(ids[:n_ent], n_train, f2.SEM_RUIDO_TR))
        dte = dict(y=yte, drive=tm.sintonias(ete, A), ruido=s * f2.ruido_por_root(ids[:n_ent], n_test, 1000 + PRUEBA_N))
        tau = f2.tau_por_root(ids, TAU_N)

        def acierto(Wx, ch):
            th = tm.umbrales(tm.lineas(sim_torch_trozos(Wx, tau, n_ent, ch, dtr, dev, a.trozo)), ytr, vtr)
            pW = tm.carrera(tm.lineas(sim_torch_trozos(Wx, tau, n_ent, ch, dte, dev, a.trozo)), th, vte)
            return float((pW == yte).mean())

        res.update(tipo=a.tipo, ks=list(range(a.k0, a.k0 + a.n)), celda=f2.clave(*CELDA_N), tau=TAU_N, prueba=PRUEBA_N,
                   nulos=[], real=None)
        if a.real:
            tc = time.time()
            res["real"] = acierto(Wt, chan)
            pr("REAL W=%.4f | %.1f s" % (res["real"], time.time() - tc))
        p, q, w = S["aristas"]
        lc_ = n3.codigos(lados)
        gi0, go0 = np.bincount(q, minlength=n), np.bincount(p, minlength=n)
        ok = True
        for k in res["ks"]:
            tc = time.time()
            if a.tipo == "SL":
                qn = n3.barajar_sl_np(p, q, lc_, np.random.default_rng([n3.SEM_SL, k]))
                g = bool(np.array_equal(np.bincount(qn, minlength=n), gi0) and np.array_equal(np.bincount(p, minlength=n), go0)
                         and np.array_equal(lc_[qn], lc_[q]) and int((qn != q).sum()) > 0)
                Wk, rk = f2.matriz(n, (p, qn, w), densa_ok=False)
                ak = acierto(a_torch(Wk, dev), chan)
                res["nulos"].append(dict(k=k, acierto=ak, radio_crudo=rk, destinos_cambiados=int((qn != q).sum()), guarda=g))
                pr("NULO SL k=%d acierto=%.4f radio=%.4f guarda=%s | %.1f s" % (k, ak, rk, g, time.time() - tc))
                del Wk, qn
            else:
                rng = np.random.default_rng([n3.SEM_T, k])
                tp = list(tipos[:n_ent])
                for ld in ("L", "R"):
                    ix_ = [i for i in range(n_ent) if lados[i] == ld]
                    vals = [tp[i] for i in ix_]
                    for i, j in zip(ix_, rng.permutation(len(ix_))):
                        tp[i] = vals[j]
                g = bool(tp != list(tipos[:n_ent]) and all(
                    sorted(tp[i] for i in range(n_ent) if lados[i] == ld) ==
                    sorted(tipos[i] for i in range(n_ent) if lados[i] == ld) for ld in ("L", "R")))
                ak = acierto(Wt, chan_de(tp, lados, n_ent))
                res["nulos"].append(dict(k=k, acierto=ak, tipos_cambiados=sum(1 for i in range(n_ent) if tp[i] != tipos[i]), guarda=g))
                pr("NULO T k=%d acierto=%.4f guarda=%s | %.1f s" % (k, ak, g, time.time() - tc))
            ok &= g
        guardas["nulos_%s" % a.tipo] = bool(ok)

    valido = all(guardas.values())
    res["guardas"], res["valido"] = guardas, valido
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % kv for kv in guardas.items()), "VALIDO" if valido else "INVALIDO"))
    nombre = {"verificar": "verificar_CE%s.json" % ("_" + a.etiqueta if a.etiqueta else ""),
              "grilla": "factorial4_CE_CON_TASA_%s.json" % (a.etiqueta or "todo"),
              "nulos": "nulos_CE_%s_k%03d.json" % (a.tipo, a.k0)}[a.modo]
    ruta = os.path.join(a.out, nombre)
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (nombre, base.md5(ruta)))
    pr("# duracion_s=%.1f" % (time.time() - t_ini))
    rc = 0 if valido else 3
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
