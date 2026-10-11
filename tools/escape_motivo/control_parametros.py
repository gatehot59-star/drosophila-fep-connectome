#!/usr/bin/env python3
"""Control de la 012: la tau liquida entrenada, contra un brazo NO liquido con los mismos parametros, y sobre
el cableado barajado.

Por que existe. La 012 mostro que la tau liquida entrenada le gana a la tau fija entrenada en el escape dificil,
pero con 3 a 53 veces mas parametros. Este script separa las dos explicaciones y, de paso, pregunta si con la
liquida entrenada el cableado de la mosca sigue importando.

Reutiliza liquida_entrenada.py (md5 verificado): mismo sujeto, tarea, lectura, optimizador (estrategia evolutiva
40 x 8 pares, sigma 0.1, Adam 0.05, 681 evaluaciones), datos de entrenamiento y prueba, y punto de partida (la tau
fija heterogenea de la 011, con todo lo demas en cero).

Parte A, liquidez contra parametros, sobre W (la mosca), 4 semillas:
  LIQ_DIAG     tau_i = sigmoid(b_i + vx_i x_i + vh_i z_i)                          78 parametros (como la 012)
  NOLIQ_DIAG   tau_i = sigmoid(b_i); pre_i = (W z)_i + x_i + gx_i x_i + gh_i z_i    78 parametros
  LIQ_PLENA    tau = sigmoid(b + Vx x + Vh z)                                     1.378 parametros (como la 012)
  NOLIQ_PLENA  tau = sigmoid(b); pre = W z + x + Gx x + Gh z                       1.378 parametros
  Cada NOLIQ usa las mismas senales que su LIQ y la misma cantidad de parametros, pero las mete en la entrada de
  la neurona (ganancias y conexiones extra entrenables) en vez de en la tau. Tau queda fija en el tiempo.
Parte B, el cableado con la liquida entrenada: LIQ_DIAG entrenada (semilla 0) sobre 24 redes SL (shuffle que
  conserva el lado, k = 0..23) y 8 redes S (k = 0..7), generadas con las mismas funciones y semillas de la 011.

Reglas PRE-REGISTRADAS (antes de la corrida completa; el humo imprime solo controles, guardas y tiempos):
  Validez en PRUEBA: las de la 012 (C+L supervivencia >= 0.60 y rechazo >= 0.90; C+6 rechazo <= 0.50;
  C0 supervivencia <= 0.05). Guardas: los cuatro brazos de la parte A arrancan con el mismo puntaje exacto en W;
  cada red nula tiene radio 0.9 y difiere de W.
  REPRODUCE_012: los puntajes de prueba de LIQ_DIAG y LIQ_PLENA por semilla deben coincidir a 4 decimales con los
  de la 012; si no, se imprime REPRODUCE_012=False y la parte A no se firma.
  P1  LIQ_DIAG vs NOLIQ_DIAG; P2  LIQ_PLENA vs NOLIQ_PLENA: McNemar exacto sobre los aciertos de prueba apareados
      por semilla y ensayo (4 x 560), p < 0.05 decide MEJOR o PEOR; si no, IGUAL.
  VEREDICTO_LIQUIDEZ: PAGA POR SER LIQUIDA si P1 y P2 dan MEJOR; LA GANANCIA ERA DE PARAMETROS si ninguno da
      MEJOR y ninguno PEOR; LOS PARAMETROS NO LIQUIDOS RINDEN MAS si los dos dan PEOR; MIXTO en otro caso.
  Q_SL  comb de prueba de W (LIQ_DIAG, semilla 0) contra las 24 SL entrenadas igual:
        p = (1 + #{SL >= W}) / 25; W GANA si p < 0.05 (hace falta que ninguna SL la iguale).
        Secundario: lo mismo con la peor de las 4 semillas de W.
  Q_S   igual contra las 8 S, DESCRIPTIVO (con 8 redes el p minimo es 0.111).
  VEREDICTO_CABLEADO_CON_LIQUIDA de Q_SL.

Uso:
  python3 control_parametros.py --motivo ../brazo_s/motivo26.json --lados lados26.json \
      --brazo-s ../brazo_s/brazo_s_recurrente.py --escape escape_motivo.py --dificil escape_dificil.py \
      --liquida liquida_entrenada.py --out-dir results/control_parametros_2026-10-11 [--solo-controles]

Corre en 2 procesos (fork). Codigos de salida: 0 completa con instrumento valido; 2 guarda; 3 instrumento invalido.
"""
import argparse
import importlib.util
import json
import multiprocessing as mp
import os
import platform
import sys
import time

import numpy as np

MD5_LIQUIDA = "0bb3f8f4a9b0fd0f7d74d102d8922d1b"
K_SL, K_S, SEMILLAS = 24, 8, 4
BRAZOS_A = ("LIQ_DIAG", "NOLIQ_DIAG", "LIQ_PLENA", "NOLIQ_PLENA")
REF_012 = {"LIQ_DIAG": ["0.9521", "0.9146", "0.9125", "0.9073"],
           "LIQ_PLENA": ["0.9802", "0.9844", "0.9812", "0.9844"]}
G = {}


def cargar(nombre, path):
    """Importa un script del repo como modulo."""
    spec = importlib.util.spec_from_file_location(nombre, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def instalar(ed, le):
    """Agrega los brazos NOLIQ al paso (la 012 ya agrego los LIQ) y su punto de partida."""
    previo = ed.paso
    sig = le.sig

    def paso(z, x, Wn, nolin, modo, ctx):
        if modo != "PARAM" or not ctx["param"][0].startswith("NOLIQ"):
            return previo(z, x, Wn, nolin, modo, ctx)
        kind, th = ctx["param"]
        tt = sig(th[:26])[None, :]
        if kind == "NOLIQ_DIAG":
            extra = th[26:52][None, :] * x + th[52:78][None, :] * z
        elif kind == "NOLIQ_PLENA":
            extra = x @ th[26:702].reshape(26, 26).T + z @ th[702:1378].reshape(26, 26).T
        else:
            raise SystemExit("ABORTA: brazo " + kind)
        pre = z @ Wn.T + x + extra
        z = (1.0 - tt) * z + tt * np.tanh(pre)
        if not np.all(np.isfinite(z)):
            raise SystemExit("ABORTA: estado no finito")
        return z
    ed.paso = paso
    t0_orig = le.theta0

    def theta0(kind, ctx):
        if kind == "NOLIQ_DIAG":
            return np.concatenate([ctx["logit_het"].copy(), np.zeros(52)])
        if kind == "NOLIQ_PLENA":
            return np.concatenate([ctx["logit_het"].copy(), np.zeros(1352)])
        return t0_orig(kind, ctx)
    le.theta0 = theta0


def tarea(t):
    """Entrena un brazo sobre una red y lo mide en prueba."""
    brazo, red, k, semilla = t
    ed, le = G["ed"], G["le"]
    Wx = G["redes"][(red, k)]
    (f_tr, th, it), hist, n_ev = le.es(ed, Wx, G["tr"], brazo, semilla, G["iters"])
    r = le.evaluar(ed, Wx, G["te"], "PARAM", brazo, th)
    return {"brazo": brazo, "red": red, "k": k, "semilla": semilla, "comb_entrenamiento": f_tr, "iter_mejor": it,
            "comb_prueba": r["comb"], "supervivencia_prueba": r["supervivencia"], "rechazo_prueba": r["rechazo"],
            "norma_extra": float(np.linalg.norm(th[26:])), "evaluaciones": n_ev, "_ac": r["acierto"],
            "theta": th.tolist()}


def main():
    """Controles, guardas, entrenamiento en dos procesos y reglas pre-registradas."""
    ap = argparse.ArgumentParser(description="Control de parametros y de cableado para la liquida entrenada")
    for k in ("--motivo", "--lados", "--brazo-s", "--escape", "--dificil", "--liquida", "--out-dir"):
        ap.add_argument(k, required=True)
    ap.add_argument("--iters", type=int, default=40)
    ap.add_argument("--procesos", type=int, default=2)
    ap.add_argument("--solo-controles", action="store_true")
    a = ap.parse_args()
    T0 = time.time()
    os.makedirs(a.out_dir, exist_ok=True)
    em = cargar("escape_motivo", a.escape)
    meta = {"python": platform.python_version(), "numpy": np.__version__, "maquina": platform.platform(),
            "md5_script": em.md5(os.path.abspath(__file__)), "md5_liquida": em.md5(a.liquida),
            "md5_dificil": em.md5(a.dificil), "md5_escape": em.md5(a.escape), "md5_brazo_s": em.md5(a.brazo_s),
            "md5_motivo": em.md5(a.motivo), "md5_lados": em.md5(a.lados), "iters": a.iters, "k_sl": K_SL,
            "k_s": K_S, "semillas": SEMILLAS, "procesos": a.procesos,
            "fecha_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    print("# " + json.dumps(meta, sort_keys=True), flush=True)
    if meta["md5_liquida"] != MD5_LIQUIDA:
        print("ABORTA: md5 de liquida_entrenada.py distinto del pin"); return 2
    le = cargar("liquida_entrenada", a.liquida)
    if (meta["md5_dificil"], meta["md5_escape"], meta["md5_brazo_s"], meta["md5_motivo"]) != \
            (le.MD5_DIFICIL, le.MD5_ESCAPE, le.MD5_BRAZO_S, le.MD5_MOTIVO):
        print("ABORTA: md5 de una entrada distinto del pin"); return 2
    ed = cargar("escape_dificil", a.dificil)
    le.instalar_paso(ed)
    instalar(ed, le)
    mod = cargar("brazo_s_recurrente", a.brazo_s)
    lados = json.load(open(a.lados))
    M, edges, mot = mod.cargar_motivo(a.motivo)
    if [f["root_id"] for f in lados["neuronas"]] != [int(x) for x in mot["orden_root_ids"]]:
        print("ABORTA: orden de lados"); return 2
    tr = le.contexto(ed, lados, le.SEM_TR, 5, 5)
    te = le.contexto(ed, lados, le.SEM_TE, 10, 10)
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

    ctrl = {k: le.evaluar(ed, Cm, te, "FIJA_HET") for k, Cm in
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
    redes = {("W", 0): Wn}
    for k in range(K_SL):
        ML, _ = em.shuffle_lado(mod, M, edges, lado, k)
        redes[("SL", k)] = mod.a_rho(ML)[0]
    for k in range(K_S):
        MS, _ = mod.matriz_shuffle(M, edges, k)
        redes[("S", k)] = mod.a_rho(MS)[0]
    for (nom, k), Wx in redes.items():
        if abs(mod.radio(Wx) - 0.9) > 1e-6 or (nom != "W" and float(np.max(np.abs(Wx - Wn))) < 1e-9):
            print("ABORTA: guarda de red " + nom + " k=" + str(k)); return 2
    print("GUARDA redes_nulas_ok=True SL=" + str(K_SL) + " S=" + str(K_S))
    t1 = time.time()
    f_ini = {k: le.evaluar(ed, Wn, tr, "PARAM", k, le.theta0(k, tr))["comb"] for k in BRAZOS_A}
    seg = (time.time() - t1) / len(BRAZOS_A)
    igual = len(set(f_ini.values())) == 1
    print("GUARDA punto_de_partida_igual=" + str(igual) + " seg_por_evaluacion=" + format(seg, ".3f"), flush=True)
    if not igual:
        print("ABORTA: los brazos no arrancan en el mismo punto"); return 2
    if a.solo_controles:
        print("SOLO_CONTROLES: el sujeto no se entreno ni se midio"); print("EXIT_RUN=0"); return 0

    G.update({"ed": ed, "le": le, "redes": redes, "tr": tr, "te": te, "iters": a.iters})
    tareas = [(b, "W", 0, s) for s in range(SEMILLAS) for b in BRAZOS_A]
    tareas += [("LIQ_DIAG", "SL", k, 0) for k in range(K_SL)] + [("LIQ_DIAG", "S", k, 0) for k in range(K_S)]
    res = []
    with mp.get_context("fork").Pool(a.procesos) as pool:
        for r in pool.imap_unordered(tarea, tareas):
            res.append(r)
            print("CORRIDA brazo=" + r["brazo"] + " red=" + r["red"] + " k=" + str(r["k"]) + " semilla=" + str(r["semilla"])
                  + " comb_entrenamiento=" + format(r["comb_entrenamiento"], ".4f") + " comb_prueba=" + format(r["comb_prueba"], ".4f")
                  + " supervivencia=" + format(r["supervivencia_prueba"], ".4f") + " rechazo=" + format(r["rechazo_prueba"], ".4f")
                  + " norma_extra=" + format(r["norma_extra"], ".3f") + " hechas=" + str(len(res)) + "/" + str(len(tareas))
                  + " seg=" + format(time.time() - T0, ".0f"), flush=True)

    def de(brazo, red):
        return sorted([r for r in res if r["brazo"] == brazo and r["red"] == red], key=lambda r: (r["k"], r["semilla"]))

    W = {b: de(b, "W") for b in BRAZOS_A}
    for b in BRAZOS_A:
        c = np.array([r["comb_prueba"] for r in W[b]])
        print("RESUMEN_W brazo=" + b + " comb_prueba_media=" + format(c.mean(), ".4f") + " min=" + format(c.min(), ".4f")
              + " max=" + format(c.max(), ".4f") + " por_semilla=" + ",".join(format(x, ".4f") for x in c))
    rep = all([format(r["comb_prueba"], ".4f") for r in W[b]] == REF_012[b] for b in REF_012)
    print("REPRODUCE_012=" + str(rep))
    con = {}

    def mc(et, A, B):
        a_ = np.concatenate([x["_ac"] for x in A]); b_ = np.concatenate([x["_ac"] for x in B])
        n01, n10, p = em.mcnemar(a_, b_)
        v = "IGUAL" if p >= 0.05 else ("MEJOR" if a_.mean() > b_.mean() else "PEOR")
        con[et] = {"solo_A_ok": n10, "solo_B_ok": n01, "p_mcnemar": p, "acierto_A": float(a_.mean()),
                   "acierto_B": float(b_.mean()), "veredicto": v}
        print("CONTRASTE " + et + " acierto_A=" + format(a_.mean(), ".4f") + " acierto_B=" + format(b_.mean(), ".4f")
              + " solo_A=" + str(n10) + " solo_B=" + str(n01) + " p_mcnemar=" + format(p, ".4g") + " -> " + v)
        return v

    p1 = mc("P1_LIQ_DIAG_vs_NOLIQ_DIAG", W["LIQ_DIAG"], W["NOLIQ_DIAG"])
    p2 = mc("P2_LIQ_PLENA_vs_NOLIQ_PLENA", W["LIQ_PLENA"], W["NOLIQ_PLENA"])
    for b, nb in (("LIQ_DIAG", "NOLIQ_DIAG"), ("LIQ_PLENA", "NOLIQ_PLENA")):
        gana = sum(1 for x, y in zip(W[b], W[nb]) if x["comb_prueba"] > y["comb_prueba"])
        print("SEMILLAS " + b + " gana_a_" + nb + "_en=" + str(gana) + "/" + str(SEMILLAS))
    s = {p1, p2}
    if s == {"MEJOR"}:
        vl = "PAGA POR SER LIQUIDA"
    elif s == {"PEOR"}:
        vl = "LOS PARAMETROS NO LIQUIDOS RINDEN MAS"
    elif "MEJOR" not in s and "PEOR" not in s:
        vl = "LA GANANCIA ERA DE PARAMETROS"
    else:
        vl = "MIXTO (P1=" + p1 + ", P2=" + p2 + ")"
    if not rep:
        vl += " [NO SE FIRMA: no reproduce la 012]"
    print("VEREDICTO_LIQUIDEZ=" + vl)
    w0 = W["LIQ_DIAG"][0]["comb_prueba"]; wmin = min(r["comb_prueba"] for r in W["LIQ_DIAG"])
    q = {}
    for nom, K in (("SL", K_SL), ("S", K_S)):
        c = np.array([r["comb_prueba"] for r in de("LIQ_DIAG", nom)])
        n0 = int((c >= w0 - 1e-12).sum()); nm = int((c >= wmin - 1e-12).sum())
        p0 = (1 + n0) / (K + 1); pm = (1 + nm) / (K + 1)
        q[nom] = {"W_semilla0": w0, "W_min": wmin, "nulo_media": float(c.mean()), "nulo_max": float(c.max()),
                  "n_ge_W0": n0, "p_W0": p0, "n_ge_Wmin": nm, "p_Wmin": pm, "valores": c.tolist()}
        print("CONTRASTE Q_" + nom + " comb W_semilla0=" + format(w0, ".4f") + " W_min=" + format(wmin, ".4f")
              + " " + nom + "_media=" + format(c.mean(), ".4f") + " " + nom + "_max=" + format(c.max(), ".4f")
              + " n>=W0=" + str(n0) + "/" + str(K) + " p=" + format(p0, ".4f")
              + " n>=Wmin=" + str(nm) + "/" + str(K) + " p_min=" + format(pm, ".4f")
              + (" -> " + ("W GANA" if p0 < 0.05 else "W NO GANA") if nom == "SL" else " (descriptivo)"))
    vc = ("CON LA LIQUIDA ENTRENADA SIGUE PAGANDO EL CABLEADO FINO" if q["SL"]["p_W0"] < 0.05
          else "CON LA LIQUIDA ENTRENADA EL CABLEADO FINO NO SE DISTINGUE DE SL")
    print("VEREDICTO_CABLEADO_CON_LIQUIDA=" + vc)
    out = {"meta": meta, "controles": {k: {kk: vv for kk, vv in r.items() if kk != "acierto"} for k, r in ctrl.items()},
           "corridas": [{k: v for k, v in r.items() if not k.startswith("_")} for r in res],
           "contrastes": con, "nulos": q, "reproduce_012": rep,
           "veredictos": {"liquidez": vl, "cableado_con_liquida": vc}, "minutos": (time.time() - T0) / 60.0}
    p_out = os.path.join(a.out_dir, "resultados.json")
    json.dump(out, open(p_out, "w"))
    print("escrito resultados.json md5=" + em.md5(p_out))
    print("minutos=" + format(out["minutos"], ".2f"))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
