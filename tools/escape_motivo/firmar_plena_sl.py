#!/usr/bin/env python3
"""Firma de la 014: la mosca con tau liquida plena entrenada contra mas redes SL y con mas semillas.

Por que existe. En la 014 la mosca (W, LIQ_PLENA, semilla 0) le gano a las 24 SL entrenadas igual con p = 0,04,
el minimo posible con 24 redes. Aca se agregan 45 redes SL nuevas (k = 24..68) y 7 semillas mas de W (1..7), con
el protocolo exacto de la 012 y la 014 (LIQ_PLENA, 40 iteraciones x 8 pares, sigma 0.10, lr 0.05). Las 24 SL de la
014 se leen de su resultados.json (md5 verificado), no se recalculan.

Reutiliza control_plena.py (md5 verificado) y, a traves de el, control_parametros.py, liquida_entrenada.py y
escape_dificil.py: mismo sujeto, tarea, lectura, datos de entrenamiento y prueba, punto de partida y funciones de
shuffle de la 011.

Reglas PRE-REGISTRADAS (antes de la corrida completa; el humo imprime solo controles, guardas y tiempos):
  Validez en PRUEBA y guardas: las de la 014; redes SL nuevas con radio 0.9, distintas de W y distintas entre si.
  REPRODUCE: W semilla 0 de la 014 = 0.9802 (leido); W semillas 1, 2 y 3 recalculadas = 0.9844, 0.9812 y 0.9844
  (los de la 012). Si no, no se firma.
  Q1 (primario)  W semilla 0 contra las 69 SL: p = (1 + #{SL >= W}) / 70; W GANA si p < 0.05.
  Q2 (estricto)  la PEOR de las 8 semillas de W contra las 69 SL, misma regla.
  Q3 (descriptivo) por semilla de W, cuantas SL la igualan; Mann-Whitney unilateral de las 8 W contra las 69 SL.
  VEREDICTO_FIRMA: FIRMADO si Q1 y Q2 dan W GANA; SOLO LA SEMILLA 0 si gana Q1 y no Q2; NO SE SOSTIENE si Q1 no gana.

Uso:
  python3 firmar_plena_sl.py --motivo ../brazo_s/motivo26.json --lados lados26.json \
      --brazo-s ../brazo_s/brazo_s_recurrente.py --escape escape_motivo.py --dificil escape_dificil.py \
      --liquida liquida_entrenada.py --control control_parametros.py --plena control_plena.py \
      --json-014 results/control_plena_2026-10-11/resultados.json \
      --out-dir results/firmar_plena_sl_2026-10-11 [--solo-controles]

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
from scipy.stats import mannwhitneyu

MD5_PLENA = "45bad2a84d625f8826b84876bef87133"
MD5_JSON_014 = "f2792e6ae8d7a93cd972230b9f726242"
K_VIEJAS, K_NUEVAS, SEM_W = 24, 45, 8
REF = {0: "0.9802", 1: "0.9844", 2: "0.9812", 3: "0.9844"}


def cargar(nombre, path):
    """Importa un script del repo como modulo."""
    spec = importlib.util.spec_from_file_location(nombre, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    """Controles, guardas, entrenamiento en dos procesos y reglas pre-registradas."""
    ap = argparse.ArgumentParser(description="Firma de la 014 con mas redes SL y mas semillas")
    for k in ("--motivo", "--lados", "--brazo-s", "--escape", "--dificil", "--liquida", "--control", "--plena",
              "--json-014", "--out-dir"):
        ap.add_argument(k, required=True)
    ap.add_argument("--procesos", type=int, default=2)
    ap.add_argument("--solo-controles", action="store_true")
    a = ap.parse_args()
    T0 = time.time()
    os.makedirs(a.out_dir, exist_ok=True)
    em = cargar("escape_motivo", a.escape)
    meta = {"python": platform.python_version(), "numpy": np.__version__, "maquina": platform.platform(),
            "md5_script": em.md5(os.path.abspath(__file__)), "md5_plena": em.md5(a.plena),
            "md5_control": em.md5(a.control), "md5_liquida": em.md5(a.liquida), "md5_dificil": em.md5(a.dificil),
            "md5_escape": em.md5(a.escape), "md5_brazo_s": em.md5(a.brazo_s), "md5_motivo": em.md5(a.motivo),
            "md5_lados": em.md5(a.lados), "md5_json_014": em.md5(a.json_014), "k_viejas": K_VIEJAS,
            "k_nuevas": K_NUEVAS, "semillas_w": SEM_W, "procesos": a.procesos,
            "fecha_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    print("# " + json.dumps(meta, sort_keys=True), flush=True)
    if meta["md5_plena"] != MD5_PLENA or meta["md5_json_014"] != MD5_JSON_014:
        print("ABORTA: md5 de control_plena.py o del json de la 014 distinto del pin"); return 2
    c14 = cargar("control_plena", a.plena)
    if meta["md5_control"] != c14.MD5_CONTROL:
        print("ABORTA: md5 de control_parametros.py distinto del pin"); return 2
    cp = cargar("control_parametros", a.control)
    if meta["md5_liquida"] != cp.MD5_LIQUIDA:
        print("ABORTA: md5 de liquida_entrenada.py distinto del pin"); return 2
    le = cargar("liquida_entrenada", a.liquida)
    if (meta["md5_dificil"], meta["md5_escape"], meta["md5_brazo_s"], meta["md5_motivo"]) != \
            (le.MD5_DIFICIL, le.MD5_ESCAPE, le.MD5_BRAZO_S, le.MD5_MOTIVO):
        print("ABORTA: md5 de una entrada distinto del pin"); return 2
    ed = cargar("escape_dificil", a.dificil)
    le.instalar_paso(ed)
    cp.instalar(ed, le)
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
    j14 = json.load(open(a.json_014))
    b14 = [r for r in j14["corridas"] if r["parte"] == "B"]
    w0 = [r["comb_prueba"] for r in b14 if r["red"] == "W"]
    sl14 = sorted([(r["k"], r["comb_prueba"]) for r in b14 if r["red"] == "SL"])
    if len(w0) != 1 or [k for k, _ in sl14] != list(range(K_VIEJAS)):
        print("ABORTA: el json de la 014 no tiene lo esperado"); return 2
    print("LEIDO_014 W_semilla0=" + format(w0[0], ".4f") + " SL=" + str(len(sl14)))
    Wn, _ = mod.a_rho(M)
    redes = {("W", 0): Wn}
    for k in range(K_VIEJAS + K_NUEVAS):
        ML, _ = em.shuffle_lado(mod, M, edges, lado, k)
        redes[("SL", k)] = mod.a_rho(ML)[0]
    for (nom, k), Wx in redes.items():
        if abs(mod.radio(Wx) - 0.9) > 1e-6 or (nom != "W" and float(np.max(np.abs(Wx - Wn))) < 1e-9):
            print("ABORTA: guarda de red " + nom + " k=" + str(k)); return 2
    firmas = {Wx.tobytes() for (nom, k), Wx in redes.items() if nom == "SL"}
    if len(firmas) != K_VIEJAS + K_NUEVAS:
        print("ABORTA: hay redes SL repetidas"); return 2
    print("GUARDA redes_nulas_ok=True SL_total=" + str(K_VIEJAS + K_NUEVAS) + " distintas=True")
    t1 = time.time()
    le.evaluar(ed, Wn, tr, "PARAM", "LIQ_PLENA", le.theta0("LIQ_PLENA", tr))
    print("GUARDA seg_por_evaluacion=" + format(time.time() - t1, ".3f"), flush=True)
    if a.solo_controles:
        print("SOLO_CONTROLES: el sujeto no se entreno ni se midio"); print("EXIT_RUN=0"); return 0

    c14.G.update({"ed": ed, "le": le, "redes": redes, "tr": tr, "te": te})
    tareas = [("B", "LIQ_PLENA", "W", 0, s, "C1", 40) for s in range(1, SEM_W)]
    tareas += [("B", "LIQ_PLENA", "SL", k, 0, "C1", 40) for k in range(K_VIEJAS, K_VIEJAS + K_NUEVAS)]
    res = []
    with mp.get_context("fork").Pool(a.procesos) as pool:
        for r in pool.imap_unordered(c14.tarea, tareas):
            res.append(r)
            print("CORRIDA red=" + r["red"] + " k=" + str(r["k"]) + " semilla=" + str(r["semilla"])
                  + " comb_entrenamiento=" + format(r["comb_entrenamiento"], ".4f") + " comb_prueba=" + format(r["comb_prueba"], ".4f")
                  + " supervivencia=" + format(r["supervivencia_prueba"], ".4f") + " rechazo=" + format(r["rechazo_prueba"], ".4f")
                  + " hechas=" + str(len(res)) + "/" + str(len(tareas)) + " seg=" + format(time.time() - T0, ".0f"), flush=True)
    W = {0: w0[0]}
    W.update({r["semilla"]: r["comb_prueba"] for r in res if r["red"] == "W"})
    SL = np.array([c for _, c in sl14] + [r["comb_prueba"] for r in sorted([r for r in res if r["red"] == "SL"], key=lambda r: r["k"])])
    K = len(SL)
    rep = all(format(W[s], ".4f") == v for s, v in REF.items())
    print("REPRODUCE=" + str(rep) + " W_por_semilla=" + ",".join(format(W[s], ".4f") for s in range(SEM_W)))
    print("RESUMEN SL_n=" + str(K) + " SL_media=" + format(SL.mean(), ".4f") + " SL_max=" + format(SL.max(), ".4f")
          + " SL_viejas_media=" + format(SL[:K_VIEJAS].mean(), ".4f") + " SL_nuevas_media=" + format(SL[K_VIEJAS:].mean(), ".4f"))

    def q(et, w):
        n = int((SL >= w - 1e-12).sum()); p = (1 + n) / (K + 1)
        print("CONTRASTE " + et + " W=" + format(w, ".4f") + " n_SL>=W=" + str(n) + "/" + str(K) + " p=" + format(p, ".4f")
              + " -> " + ("W GANA" if p < 0.05 else "W NO GANA"))
        return p < 0.05, n, p

    g1, n1, p1 = q("Q1_semilla0", W[0])
    wmin = min(W.values())
    g2, n2, p2 = q("Q2_peor_semilla", wmin)
    for s in range(SEM_W):
        n = int((SL >= W[s] - 1e-12).sum())
        print("Q3 semilla=" + str(s) + " W=" + format(W[s], ".4f") + " n_SL>=W=" + str(n) + "/" + str(K))
    mw = mannwhitneyu([W[s] for s in range(SEM_W)], SL, alternative="greater")
    print("Q3 mann_whitney_U=" + format(float(mw.statistic), ".1f") + " p_unilateral=" + format(float(mw.pvalue), ".4g"))
    if g1 and g2:
        v = "FIRMADO: CON LA LIQUIDA PLENA LA MOSCA LE GANA A SL"
    elif g1:
        v = "SOLO LA SEMILLA 0: LA PEOR SEMILLA DE W NO LE GANA A SL"
    else:
        v = "NO SE SOSTIENE: CON MAS REDES SL, W SEMILLA 0 NO LE GANA"
    if not rep:
        v += " [NO SE FIRMA: no reproduce]"
    print("VEREDICTO_FIRMA=" + v)
    out = {"meta": meta, "controles": {k: {kk: vv for kk, vv in r.items() if kk != "acierto"} for k, r in ctrl.items()},
           "corridas": [{k: v_ for k, v_ in r.items() if not k.startswith("_")} for r in res],
           "W": W, "SL": SL.tolist(), "Q1": {"n": n1, "p": p1}, "Q2": {"W_min": wmin, "n": n2, "p": p2},
           "mann_whitney": {"U": float(mw.statistic), "p": float(mw.pvalue)}, "reproduce": rep,
           "veredicto": v, "minutos": (time.time() - T0) / 60.0}
    p_out = os.path.join(a.out_dir, "resultados.json")
    json.dump(out, open(p_out, "w"))
    print("escrito resultados.json md5=" + em.md5(p_out))
    print("minutos=" + format(out["minutos"], ".2f"))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
