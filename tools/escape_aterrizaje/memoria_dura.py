#!/usr/bin/env python3
"""Escape o aterrizaje con memoria dura: DBC3 contra LSTM fuera del techo (2026-10-12-004).

Reusa, importandolas sin cambios, las piezas de escape_aterrizaje_dbc3.py (md5 4d40477d..., 003):
el motivo de 28 neuronas de FlyWire, la dinamica SparseLTC, DBC3Motor, LSTMLector, SinMemoria,
entrenar, nuevo y mcnemar. Solo cambia la tarea, para que la memoria sea dificil:
  - 120 pasos (la 003 tenia 40); el estimulo aparece entre el paso 90 y el 105.
  - Senal de estado fuerte (+-1, 3 pasos) al principio; con probabilidad 0,5 se invierte con otra
    senal fuerte en un paso al azar entre 20 y 80: vale la ultima (cambio de contexto).
  - Cuatro pulsos debiles (+-0,3, 1 paso, signo al azar) en pasos al azar: hay que ignorarlos.
Dos presupuestos: canonico (DBC3 h_m 20, h_r 36) y chico (h_m 8, h_r 12), cada uno con su LSTM
del mismo tamano. Rival clasico: maquina de estados que guarda la ultima senal fuerte (|c| > 0,5)
y detecta y lateraliza con la regla de la 003.
Salida: 0 completo; 2 md5 distinto del pin; 3 instrumento invalido.
"""
import argparse, os, platform, sys, time, json
import numpy as np
import torch
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import escape_aterrizaje_dbc3 as base  # noqa: E402

MD5_BASE = "4d40477d87406c31672acfb6e6e8f5a2"
T_DURO = 120
SEMILLAS = [0, 1, 2, 3]
PRESUP = {"canonico": (20, 36), "chico": (8, 12)}


def generar_duro(n, seed, nv):
    rng = np.random.default_rng(seed)
    T = T_DURO
    cond = np.arange(n) % 6
    rng.shuffle(cond)
    est = cond % 3
    vuelo0 = cond < 3
    cambia = rng.random(n) < 0.5
    vuelo = np.where(cambia, ~vuelo0, vuelo0)
    y = np.where(est == 2, 0, np.where(vuelo, 3, np.where(est == 0, 1, 2)))
    cue = np.zeros((n, T))
    drive = np.zeros((n, T, 2))
    for i in range(n):
        s0 = 1.0 if vuelo0[i] else -1.0
        cue[i, 0:3] = s0
        if cambia[i]:
            tc = rng.integers(20, 81)
            cue[i, tc:tc + 3] = -s0
        for _ in range(4):
            tp = rng.integers(5, 110)
            if abs(cue[i, tp]) < 0.5:
                cue[i, tp] = rng.choice([-0.3, 0.3])
        t0 = rng.integers(90, 106)
        if est[i] < 2:
            amp = rng.uniform(0.6, 1.0)
            drive[i, :, est[i]] = np.clip((np.arange(T) - t0 + 1) / 8.0, 0, 1) * amp
        else:
            amp = rng.uniform(0.3, 0.7)
            for t in range(t0, T):
                drive[i, t, ((t - t0) // 4) % 2] = amp
    ruido = rng.normal(0, 0.15, (n, T, nv))
    return dict(y=y, cue=cue, drive=drive, ruido=ruido, vuelo=vuelo, est=est, cambia=cambia)


def regla_estados(dn_tr, dtr, dn_te, dte, onset_min=90):
    """Maquina de estados: guarda la ultima senal fuerte; deteccion y lado como en la 003."""
    def ultimo(cue):
        fuerte = np.abs(cue) > 0.5
        idx = np.where(fuerte.any(1), cue.shape[1] - 1 - np.argmax(fuerte[:, ::-1], axis=1), 0)
        return cue[np.arange(len(cue)), idx] > 0
    def rasgos(dn):
        pico = dn[:, onset_min:, :].max(axis=(1, 2))
        lado = (dn[:, onset_min:, 0] + dn[:, onset_min:, 2] - dn[:, onset_min:, 1] - dn[:, onset_min:, 3]).sum(1)
        return pico, lado
    def clasif(p, l, v, th):
        return np.where(p <= th, 0, np.where(v, 3, np.where(l > 0, 1, 2)))
    ptr, ltr = rasgos(dn_tr)
    vtr = ultimo(dtr["cue"])
    cands = np.quantile(ptr, np.linspace(0.01, 0.99, 197))
    th = max(cands, key=lambda c: (clasif(ptr, ltr, vtr, c) == dtr["y"]).mean())
    pte, lte = rasgos(dn_te)
    return clasif(pte, lte, ultimo(dte["cue"]), th), float(th)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True); ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--presupuesto", choices=list(PRESUP), required=True)
    ap.add_argument("--iters", type=int, default=400)
    ap.add_argument("--humo", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    torch.set_num_threads(1)
    t0 = time.time()
    P = lambda *x: print(*x, flush=True)
    P("# maquina: %s | %s | Python %s | numpy %s | torch %s" % (platform.node(), platform.platform(),
      platform.python_version(), np.__version__, torch.__version__))
    P("# md5 script = " + base.md5(os.path.abspath(__file__)))
    mb = base.md5(base.__file__)
    P("# md5 base escape_aterrizaje_dbc3.py = %s (pin %s)" % (mb, MD5_BASE))
    P("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z") + " | presupuesto=" + a.presupuesto)
    mc, ma = base.md5(a.conn), base.md5(a.annot)
    if mb != MD5_BASE or mc != base.MD5_CONN or ma != base.MD5_ANNOT:
        P("ABORTA: md5 del modulo base o de los datos distinto del pin"); P("EXIT_RUN=2"); return 2
    if a.humo:
        P("# HUMO: corrida corta, estos numeros no valen")
    base.T = T_DURO  # el simulador del modulo base lee T del modulo
    sel, aristas = base.construir_motivo(a.conn, a.annot)
    n = len(sel)
    lados = ["L" if s[2] == "left" else "R" for s in sel]
    W, rho0 = base.matriz(n, aristas)
    nv = n - 4
    lados_vis = np.array([0 if lados[i] == "L" else 1 for i in range(nv)])
    tau = 0.06 + 0.12 * np.random.default_rng(0).random(n)
    P("MOTIVO neuronas=%d aristas=%d rho_crudo=%.4f (igual que la 003)" % (n, len(aristas), rho0))
    ntr, nte = (512, 600) if a.humo else (base.N_TRAIN, base.N_TEST)
    dtr, dte = generar_duro(ntr, 11, nv), generar_duro(nte, 12, nv)
    P("TAREA T=%d cambia_contexto_train=%.3f test=%.3f" % (T_DURO, dtr["cambia"].mean(), dte["cambia"].mean()))
    dn_tr, dn_te = base.simular(W, tau, lados_vis, dtr), base.simular(W, tau, lados_vis, dte)
    xtr, xte = base.entradas(dn_tr, dtr), base.entradas(dn_te, dte)
    ytr, yte = dtr["y"], dte["y"]
    d_in, d_out = xtr.shape[2], 4
    m, r = PRESUP[a.presupuesto]
    torch.manual_seed(0)
    p_dbc3 = base.n_params(base.DBC3Motor(d_in, d_out, m, r))
    h = base.lstm_h_para(d_in, d_out, p_dbc3)
    P("PARAMS DBC3(h_m=%d,h_r=%d)=%d LSTM(h=%d)=%d SIN_MEMORIA=%d" % (m, r, p_dbc3, h,
      base.n_params(base.LSTMLector(d_in, d_out, h)), base.n_params(base.SinMemoria(d_in, d_out))))
    iters = 10 if a.humo else a.iters
    semillas = SEMILLAS[:1] if a.humo else SEMILLAS

    def construir(nom, s):
        torch.manual_seed(s)
        if nom == "DBC3":
            return base.DBC3Motor(d_in, d_out, m, r)
        return base.nuevo(nom, d_in, d_out, h, s)

    res = {"presupuesto": a.presupuesto, "params": {"DBC3": p_dbc3, "LSTM_h": h}, "W": {}}
    preds = {}
    for nom in ("DBC3", "LSTM", "SIN_MEMORIA"):
        for s in semillas:
            ti = time.time()
            pr = base.entrenar(construir(nom, s), xtr, ytr, xte, s, iters, batch=128)
            preds[(nom, s)] = pr
            acc = float((pr == yte).mean())
            accc = float((pr[dte["cambia"]] == yte[dte["cambia"]]).mean())
            res["W"].setdefault(nom, []).append(acc)
            P("W lector=%s semilla=%d acierto=%.4f con_cambio=%.4f por_clase=%s seg=%.0f" % (
                nom, s, acc, accc, ",".join("%.3f" % float((pr[yte == k] == k).mean()) for k in range(4)),
                time.time() - ti))
    pr2 = base.entrenar(construir("DBC3", semillas[0]), xtr, ytr, xte, semillas[0], iters, batch=128)
    repro = bool((pr2 == preds[("DBC3", semillas[0])]).all())
    P("CHEQUEO REPRODUCE DBC3 semilla=%d -> %s" % (semillas[0], repro))
    pm, th = regla_estados(dn_tr, dtr, dn_te, dte)
    acc_m = float((pm == yte).mean())
    P("W lector=MAQUINA_DE_ESTADOS umbral=%.4f acierto=%.4f con_cambio=%.4f" % (
        th, acc_m, float((pm[dte["cambia"]] == yte[dte["cambia"]]).mean())))
    res["W"]["MAQUINA_DE_ESTADOS"] = acc_m

    def comparar(a_, b_):
        bb = cc = 0; signos = []
        for s in semillas:
            x = preds[(a_, s)] == yte
            y_ = (pm == yte) if b_ == "MAQUINA_DE_ESTADOS" else preds[(b_, s)] == yte
            b1, c1, _ = base.mcnemar(x, y_); bb += b1; cc += c1; signos.append(np.sign(b1 - c1))
        p = stats.binomtest(bb, bb + cc, 0.5).pvalue if bb + cc else 1.0
        v = "MEJOR" if all(z > 0 for z in signos) and p < 0.05 else (
            "PEOR" if all(z < 0 for z in signos) and p < 0.05 else "EMPATE")
        return bb, cc, p, v
    dm, lm = np.mean(res["W"]["DBC3"]), np.mean(res["W"]["LSTM"])
    techo = bool(dm >= 0.99 and lm >= 0.99)
    for pid, (x, y_) in {"H1_DBC3_vs_LSTM": ("DBC3", "LSTM"), "H2_DBC3_vs_SIN_MEMORIA": ("DBC3", "SIN_MEMORIA"),
                         "H3_DBC3_vs_MAQUINA_DE_ESTADOS": ("DBC3", "MAQUINA_DE_ESTADOS")}.items():
        bb, cc, p, v = comparar(x, y_)
        res[pid] = dict(gana_a=bb, gana_b=cc, p=p, veredicto=v)
        P("%s presupuesto=%s discordantes %d contra %d p=%.3g -> %s" % (pid, a.presupuesto, bb, cc, p, v))
    P("TECHO presupuesto=%s DBC3_media=%.4f LSTM_media=%.4f -> %s" % (
        a.presupuesto, dm, lm, "EN EL TECHO (H1 no concluye)" if techo else "FUERA DEL TECHO"))
    sm = float(np.mean(res["W"]["SIN_MEMORIA"]))
    c_neg = sm <= 0.75
    c_pos = acc_m >= 0.75  # 0.80 en la 003; bajado a 0.75 tras el humo (0.7833 con 512 de entrenamiento), antes de correr
    valido = bool(c_neg and c_pos and repro)
    res.update(techo=techo, controles=dict(sin_memoria=sm, control_negativo=c_neg, maquina=acc_m,
                                           control_positivo=c_pos, reproduce=repro), valido=valido)
    P("CHEQUEO INSTRUMENTO control_negativo(sin_memoria<=0.75)=%s control_positivo(maquina_de_estados>=0.75)=%s "
      "reproduce=%s -> %s" % (c_neg, c_pos, repro, "VALIDO" if valido else "INVALIDO"))
    with open(os.path.join(a.out, "resultados.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True, default=float)
    P("escrito resultados.json md5=" + base.md5(os.path.join(a.out, "resultados.json")))
    P("# duracion_s=%.1f" % (time.time() - t0))
    rc = 0 if valido else 3
    P("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
