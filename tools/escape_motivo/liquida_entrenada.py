#!/usr/bin/env python3
"""Tau liquida ENTRENADA contra tau fija entrenada, sobre el cableado de la mosca, en el escape dificil.

Por que existe. En la 011 la tau liquida perdio, pero era una liquida congelada con pesos al azar. Lo que afirma
una LTC es que la tau que depende de la entrada, ENTRENADA, rinde mas. Aca se entrena y se mide eso, con el
mismo sujeto (motivo de 26, rho 0.9, tanh), la misma tarea y la misma lectura fija por umbral de escape_dificil.py
(importado tal cual; su md5 se verifica). Solo se entrenan los parametros de tau: el cableado W, la entrada y
la regla de disparo quedan fijos.

Brazos (todos arrancan EXACTAMENTE en la tau fija heterogenea de la 011, U[0.06, 0.18] con default_rng(119)):
  FIJA_ENT    tau_i = sigmoid(b_i), b entrenable (26 parametros): tau fija en el tiempo, aprendida.
  LIQ_DIAG    tau_i(t) = sigmoid(b_i + vx_i x_i(t) + vh_i z_i(t)), vx = vh = 0 al inicio (78 parametros).
  LIQ_PLENA   tau(t) = sigmoid(b + Vx x(t) + Vh z(t)), Vx = Vh = 0 al inicio (1.378 parametros), la forma de
              LiquidCell y de la LIQUIDA de la 011, pero entrenada.
Referencias sin entrenar, medidas en el conjunto de prueba: FIJA_HET (la de la 011) y LIQUIDA congelada (la de
la 011, Vx y Vh al azar).

Entrenamiento: estrategia evolutiva con pares antiteticos, misma para los tres brazos: 40 iteraciones x 8 pares,
sigma 0.1, rangos centrados, Adam lr 0.05; 681 evaluaciones por corrida; se queda el centro con mejor puntaje de
entrenamiento. 4 semillas por brazo (default_rng(7000 + semilla)). La funcion objetivo es el puntaje de la 011,
comb = (supervivencia + rechazo) / 2, con el umbral recalculado en cada evaluacion desde los ensayos en blanco.

Datos: ENTRENAMIENTO con ruido default_rng(20261013) y 5 repeticiones (240 looming, 40 no looming, 40 en blanco);
PRUEBA con ruido default_rng(20261014) y 10 repeticiones (480, 80, 40). Las condiciones son las de la 011.

Reglas PRE-REGISTRADAS (antes de la corrida completa; el humo imprime solo controles, tiempos y guardas):
  Validez en PRUEBA: C+L supervivencia >= 0.60 y rechazo >= 0.90; C+6 rechazo <= 0.50; C0 supervivencia <= 0.05.
  Guarda: en el punto de partida, los tres brazos dan el mismo puntaje de entrenamiento (igualdad exacta).
  Por ensayo de prueba, ACIERTO = sobrevivio (looming) o no disparo (no looming); 560 por corrida.
  E1  LIQ_DIAG vs FIJA_ENT: McNemar exacto a dos colas sobre los aciertos apareados por semilla y ensayo
      (4 x 560 pares), p < 0.05 decide MEJOR o PEOR; si no, IGUAL.
  E2  LIQ_PLENA vs FIJA_ENT, igual.
  E3  FIJA_ENT vs FIJA_HET sin entrenar, igual (la FIJA_HET se repite contra cada semilla).
  VEREDICTO_LIQUIDA_ENTRENADA: PAGA si E1 o E2 da MEJOR y ninguno PEOR; PIERDE si alguno da PEOR y ninguno
  MEJOR; MIXTO si uno y uno; NO SE DISTINGUE si los dos IGUAL. VEREDICTO_ENTRENAR_TAU de E3.
  Se reporta ademas, por semilla, el puntaje de prueba de cada brazo y cuantas semillas gana la liquida.

Uso:
  python3 liquida_entrenada.py --motivo ../brazo_s/motivo26.json --lados lados26.json \
      --brazo-s ../brazo_s/brazo_s_recurrente.py --escape escape_motivo.py --dificil escape_dificil.py \
      --out-dir results/liquida_entrenada_2026-10-11   [--solo-controles] [--iters 40] [--semillas 4]

Codigos de salida: 0 completa con instrumento valido; 2 guarda fallida; 3 instrumento invalido.
"""
import argparse
import importlib.util
import json
import math
import os
import platform
import sys
import time

import numpy as np

MD5_DIFICIL = "2c95e63b6ad3ff590057df80368134d7"
MD5_ESCAPE = "9720998291e3f08c6082e6c67d142759"
MD5_BRAZO_S = "f8b10037e70dfe897ff2d841077419b4"
MD5_MOTIVO = "eb6e53e047c864a46c56bf38b397d289"
SEM_TR, SEM_TE = 20261013, 20261014
PARES, SIGMA, LR = 8, 0.1, 0.05
BRAZOS = ("FIJA_ENT", "LIQ_DIAG", "LIQ_PLENA")


def cargar(nombre, path):
    """Importa un script del repo como modulo."""
    spec = importlib.util.spec_from_file_location(nombre, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def sig(a):
    """Sigmoide."""
    return 1.0 / (1.0 + np.exp(-a))


def instalar_paso(ed):
    """Agrega el modo PARAM al paso de escape_dificil.py; los modos de la 011 quedan intactos."""
    original = ed.paso

    def paso(z, x, Wn, nolin, modo, ctx):
        if modo != "PARAM":
            return original(z, x, Wn, nolin, modo, ctx)
        kind, th = ctx["param"]
        if kind == "FIJA_ENT":
            tt = sig(th)[None, :]
        elif kind == "LIQ_DIAG":
            tt = sig(th[:26][None, :] + th[26:52][None, :] * x + th[52:78][None, :] * z)
        elif kind == "LIQ_PLENA":
            Vx = th[26:702].reshape(26, 26); Vh = th[702:1378].reshape(26, 26)
            tt = sig(th[:26][None, :] + x @ Vx.T + z @ Vh.T)
        else:
            raise SystemExit("ABORTA: brazo " + kind)
        pre = z @ Wn.T + x
        z = (1.0 - tt) * z + tt * np.tanh(pre)
        if not np.all(np.isfinite(z)):
            raise SystemExit("ABORTA: estado no finito")
        return z
    ed.paso = paso


def theta0(kind, ctx):
    """Punto de partida comun: la tau fija heterogenea de la 011."""
    b = ctx["logit_het"].copy()
    if kind == "FIJA_ENT":
        return b
    if kind == "LIQ_DIAG":
        return np.concatenate([b, np.zeros(52)])
    return np.concatenate([b, np.zeros(1352)])


def evaluar(ed, Wn, ctx, modo, kind=None, th=None):
    """Puntaje y vectores de acierto con la regla de disparo de la 011."""
    if modo == "PARAM":
        ctx["param"] = (kind, th)
    umb = ed.FACTOR_UMBRAL * ed.blanco(Wn, "TANH", modo, ctx)
    L = ed.looming(Wn, "TANH", modo, ctx, umb); N = ed.no_looming(Wn, "TANH", modo, ctx, umb)
    sv, rj = float(L["sv"].mean()), float(N["rj"].mean())
    return {"comb": 0.5 * (sv + rj), "supervivencia": sv, "rechazo": rj, "umbral": umb,
            "acierto": np.concatenate([L["sv"], N["rj"]])}


def es(ed, Wn, ctx, kind, semilla, iters):
    """Estrategia evolutiva antitetica con rangos centrados y Adam. Devuelve el mejor centro."""
    rng = np.random.default_rng(7000 + semilla)
    th = theta0(kind, ctx); d = th.size
    m = np.zeros(d); v = np.zeros(d)
    f0 = evaluar(ed, Wn, ctx, "PARAM", kind, th)["comb"]
    mejor = (f0, th.copy(), 0); hist = [f0]; n_eval = 1
    for it in range(1, iters + 1):
        eps = rng.normal(size=(PARES, d))
        f = np.array([evaluar(ed, Wn, ctx, "PARAM", kind, th + s * SIGMA * e)["comb"]
                      for s in (1.0, -1.0) for e in eps])
        n_eval += 2 * PARES
        r = np.empty(2 * PARES); r[np.argsort(f, kind="stable")] = np.arange(2 * PARES)
        r = r / (2 * PARES - 1) - 0.5
        g = ((r[:PARES] - r[PARES:])[:, None] * eps).sum(0) / (PARES * SIGMA)
        m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g * g
        th = th + LR * (m / (1 - 0.9 ** it)) / (np.sqrt(v / (1 - 0.999 ** it)) + 1e-8)
        fc = evaluar(ed, Wn, ctx, "PARAM", kind, th)["comb"]; n_eval += 1
        hist.append(fc)
        if fc > mejor[0]:
            mejor = (fc, th.copy(), it)
    return mejor, hist, n_eval


def contexto(ed, lados, semilla, reps, reps_nl):
    """Construye el contexto de escape_dificil.py con otra semilla de ruido y otra cantidad de repeticiones."""
    viejo = (ed.SEMILLA_RUIDO, ed.REPS, ed.REPS_NL)
    ed.SEMILLA_RUIDO, ed.REPS, ed.REPS_NL = semilla, reps, reps_nl
    try:
        return ed.construir_ctx(lados)
    finally:
        ed.SEMILLA_RUIDO, ed.REPS, ed.REPS_NL = viejo


def main():
    """Controles, entrenamiento, prueba y reglas pre-registradas."""
    ap = argparse.ArgumentParser(description="Tau liquida entrenada contra tau fija entrenada")
    for k in ("--motivo", "--lados", "--brazo-s", "--escape", "--dificil", "--out-dir"):
        ap.add_argument(k, required=True)
    ap.add_argument("--iters", type=int, default=40)
    ap.add_argument("--semillas", type=int, default=4)
    ap.add_argument("--solo-controles", action="store_true")
    a = ap.parse_args()
    T0 = time.time()
    os.makedirs(a.out_dir, exist_ok=True)
    em = cargar("escape_motivo", a.escape)
    meta = {"python": platform.python_version(), "numpy": np.__version__, "maquina": platform.platform(),
            "md5_script": em.md5(os.path.abspath(__file__)), "md5_dificil": em.md5(a.dificil),
            "md5_escape": em.md5(a.escape), "md5_brazo_s": em.md5(a.brazo_s), "md5_motivo": em.md5(a.motivo),
            "md5_lados": em.md5(a.lados), "iters": a.iters, "semillas": a.semillas, "pares": PARES,
            "sigma": SIGMA, "lr": LR, "semilla_ruido_entrenamiento": SEM_TR, "semilla_ruido_prueba": SEM_TE,
            "fecha_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        for line in open("/proc/cpuinfo"):
            if line.startswith("model name"):
                meta["cpu"] = line.split(":", 1)[1].strip(); break
    except OSError:
        pass
    print("# " + json.dumps(meta, sort_keys=True))
    if (meta["md5_dificil"], meta["md5_escape"], meta["md5_brazo_s"], meta["md5_motivo"]) != \
            (MD5_DIFICIL, MD5_ESCAPE, MD5_BRAZO_S, MD5_MOTIVO):
        print("ABORTA: md5 de una entrada distinto del pin"); return 2
    ed = cargar("escape_dificil", a.dificil)
    instalar_paso(ed)
    mod = cargar("brazo_s_recurrente", a.brazo_s)
    lados = json.load(open(a.lados))
    M, edges, mot = mod.cargar_motivo(a.motivo)
    if [f["root_id"] for f in lados["neuronas"]] != [int(x) for x in mot["orden_root_ids"]]:
        print("ABORTA: orden de lados"); return 2
    tr = contexto(ed, lados, SEM_TR, 5, 5)
    te = contexto(ed, lados, SEM_TE, 10, 10)
    print("ENSAYOS entrenamiento looming=" + str(len(tr["loom_az"])) + " no_looming=" + str(len(tr["nl_az"]))
          + " | prueba looming=" + str(len(te["loom_az"])) + " no_looming=" + str(len(te["nl_az"])))
    lado, tipo = te["lado"], te["tipo"]

    def reflejo(con_lc6):
        C = np.zeros((26, 26))
        for side, g in (("left", te["GL"]), ("right", te["GR"])):
            base = [i for i in range(26) if lado[i] == side and tipo[i] in ("LC4", "LPLC2")]
            for i in base:
                C[g, i] = 1.0 / len(base)
            if con_lc6:
                for i in range(26):
                    if lado[i] == side and tipo[i] == "LC6":
                        C[g, i] = 0.5
        return C

    ctrl = {k: evaluar(ed, Cm, te, "FIJA_HET") for k, Cm in
            (("C+L", reflejo(False)), ("C+6", reflejo(True)), ("C0", np.zeros((26, 26))))}
    for k, r in ctrl.items():
        print("CONTROL_PRUEBA " + k + " supervivencia=" + format(r["supervivencia"], ".4f") + " rechazo="
              + format(r["rechazo"], ".4f") + " comb=" + format(r["comb"], ".4f"))
    valido = (ctrl["C+L"]["supervivencia"] >= 0.60 and ctrl["C+L"]["rechazo"] >= 0.90
              and ctrl["C+6"]["rechazo"] <= 0.50 and ctrl["C0"]["supervivencia"] <= 0.05)
    print("CHEQUEO INSTRUMENTO " + ("VALIDO" if valido else "INVALIDO"))
    if not valido:
        print("EXIT_RUN=3"); return 3
    Wn, _ = mod.a_rho(M)
    t1 = time.time()
    f_ini = {k: evaluar(ed, Wn, tr, "PARAM", k, theta0(k, tr))["comb"] for k in BRAZOS}
    seg_eval = (time.time() - t1) / 3.0
    igual = len(set(f_ini.values())) == 1
    print("GUARDA punto_de_partida_igual=" + str(igual) + " seg_por_evaluacion=" + format(seg_eval, ".3f"))
    if not igual:
        print("ABORTA: los brazos no arrancan en el mismo punto"); return 2
    if a.solo_controles:
        print("SOLO_CONTROLES: el sujeto no se entreno ni se midio"); print("EXIT_RUN=0"); return 0

    ref = {"FIJA_HET": evaluar(ed, Wn, te, "FIJA_HET"), "LIQUIDA_CONGELADA": evaluar(ed, Wn, te, "LIQUIDA")}
    for k, r in ref.items():
        print("REFERENCIA_PRUEBA " + k + " supervivencia=" + format(r["supervivencia"], ".4f") + " rechazo="
              + format(r["rechazo"], ".4f") + " comb=" + format(r["comb"], ".4f"))
    corr = {k: [] for k in BRAZOS}
    for s in range(a.semillas):
        for k in BRAZOS:
            (f_tr, th, it), hist, n_ev = es(ed, Wn, tr, k, s, a.iters)
            r = evaluar(ed, Wn, te, "PARAM", k, th)
            tau_med = float(np.median(sig(th[:26])))
            corr[k].append({"semilla": s, "comb_entrenamiento": f_tr, "iter_mejor": it, "evaluaciones": n_ev,
                            "comb_prueba": r["comb"], "supervivencia_prueba": r["supervivencia"],
                            "rechazo_prueba": r["rechazo"], "tau_mediana_b": tau_med,
                            "norma_v": float(np.linalg.norm(th[26:])) if th.size > 26 else 0.0,
                            "historia": hist, "theta": th.tolist(), "_ac": r["acierto"]})
            print("CORRIDA brazo=" + k + " semilla=" + str(s) + " comb_entrenamiento=" + format(f_tr, ".4f")
                  + " (inicio " + format(hist[0], ".4f") + ", iter " + str(it) + ") comb_prueba=" + format(r["comb"], ".4f")
                  + " supervivencia=" + format(r["supervivencia"], ".4f") + " rechazo=" + format(r["rechazo"], ".4f")
                  + " norma_v=" + format(corr[k][-1]["norma_v"], ".3f") + " evaluaciones=" + str(n_ev)
                  + " seg=" + format(time.time() - T0, ".0f"), flush=True)
    for k in BRAZOS:
        c = np.array([x["comb_prueba"] for x in corr[k]])
        print("RESUMEN brazo=" + k + " comb_prueba_media=" + format(c.mean(), ".4f") + " min=" + format(c.min(), ".4f")
              + " max=" + format(c.max(), ".4f"))
    con = {}

    def mc(et, A, B):
        a_ = np.concatenate([x["_ac"] for x in A]); b_ = np.concatenate([x["_ac"] for x in B])
        n01, n10, p = em.mcnemar(a_, b_)
        dif = float(a_.mean() - b_.mean())
        v = "IGUAL" if p >= 0.05 else ("MEJOR" if dif > 0 else "PEOR")
        con[et] = {"solo_A_ok": n10, "solo_B_ok": n01, "p_mcnemar": p, "dif_acierto": dif, "veredicto": v}
        print("CONTRASTE " + et + " acierto_A=" + format(a_.mean(), ".4f") + " acierto_B=" + format(b_.mean(), ".4f")
              + " solo_A=" + str(n10) + " solo_B=" + str(n01) + " p_mcnemar=" + format(p, ".4g") + " -> " + v)
        return v

    e1 = mc("E1_LIQ_DIAG_vs_FIJA_ENT", corr["LIQ_DIAG"], corr["FIJA_ENT"])
    e2 = mc("E2_LIQ_PLENA_vs_FIJA_ENT", corr["LIQ_PLENA"], corr["FIJA_ENT"])
    base = [{"_ac": ref["FIJA_HET"]["acierto"]} for _ in range(a.semillas)]
    e3 = mc("E3_FIJA_ENT_vs_FIJA_HET", corr["FIJA_ENT"], base)
    for k in ("LIQ_DIAG", "LIQ_PLENA"):
        gana = sum(1 for x, y in zip(corr[k], corr["FIJA_ENT"]) if x["comb_prueba"] > y["comb_prueba"])
        print("SEMILLAS " + k + " gana_a_FIJA_ENT_en=" + str(gana) + "/" + str(a.semillas))
    s = {e1, e2}
    if s == {"IGUAL"}:
        vl = "LA LIQUIDA ENTRENADA NO SE DISTINGUE DE LA TAU FIJA ENTRENADA"
    elif "MEJOR" in s and "PEOR" in s:
        vl = "MIXTO"
    elif "MEJOR" in s:
        vl = "LA LIQUIDA ENTRENADA PAGA"
    else:
        vl = "LA LIQUIDA ENTRENADA PIERDE CONTRA LA TAU FIJA ENTRENADA"
    ve = {"IGUAL": "ENTRENAR LA TAU FIJA NO SE DISTINGUE DE NO ENTRENARLA", "MEJOR": "ENTRENAR LA TAU FIJA PAGA",
          "PEOR": "ENTRENAR LA TAU FIJA EMPEORA EN PRUEBA"}[e3]
    print("VEREDICTO_LIQUIDA_ENTRENADA=" + vl)
    print("VEREDICTO_ENTRENAR_TAU=" + ve)
    out = {"meta": meta, "controles": {k: {kk: vv for kk, vv in r.items() if kk != "acierto"} for k, r in ctrl.items()},
           "referencias": {k: {kk: vv for kk, vv in r.items() if kk != "acierto"} for k, r in ref.items()},
           "corridas": {k: [{kk: vv for kk, vv in x.items() if not kk.startswith("_")} for x in v_] for k, v_ in corr.items()},
           "contrastes": con, "veredictos": {"liquida_entrenada": vl, "entrenar_tau": ve},
           "minutos": (time.time() - T0) / 60.0}
    p_out = os.path.join(a.out_dir, "resultados.json")
    json.dump(out, open(p_out, "w"))
    print("escrito resultados.json md5=" + em.md5(p_out))
    print("minutos=" + format(out["minutos"], ".2f"))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
