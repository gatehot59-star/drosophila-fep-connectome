#!/usr/bin/env python3
"""Segundo control de la 013: la tau liquida plena, contra su control no liquido con optimizacion ajustada, y
sobre el cableado barajado.

Por que existe. En la 013 la liquida plena (1.378 parametros) le gano a la no liquida plena (mismas senales y
parametros en la entrada, tau fija), pero la no liquida salto entre 0,851 y 0,972 segun la semilla: puede ser un
problema del optimizador y no de la liquidez. Y la plena no se probo sobre SL.

Reutiliza control_parametros.py (md5 verificado) y, a traves de el, liquida_entrenada.py y escape_dificil.py:
mismo sujeto, tarea, lectura, datos de entrenamiento y prueba, punto de partida y brazos.

Parte A, optimizacion ajustada, sobre W, 4 semillas por brazo (LIQ_PLENA y NOLIQ_PLENA):
  cada semilla se entrena con dos configuraciones de la estrategia evolutiva, 60 iteraciones x 8 pares:
    C1 sigma 0.10, lr 0.05 (la de la 012 con 50% mas de iteraciones)
    C2 sigma 0.03, lr 0.02 (pasos mas chicos, pensada para el Gh denso)
  y se queda la de MEJOR PUNTAJE DE ENTRENAMIENTO (nunca se mira la prueba para elegir). Mismo trato a los dos.
Parte B, el cableado con la liquida plena: LIQ_PLENA con el protocolo exacto de la 012 (40 iteraciones, C1,
  semilla 0) sobre W y sobre 24 redes SL (k = 0..23, funciones y semillas de la 011).

Reglas PRE-REGISTRADAS (antes de la corrida completa; el humo imprime solo controles, guardas y tiempos):
  Validez en PRUEBA y guardas: las de la 013.
  REPRODUCE_012: W en la parte B debe dar 0.9802 a 4 decimales; si no, la parte B no se firma.
  P3  LIQ_PLENA ajustada vs NOLIQ_PLENA ajustada: McNemar exacto sobre aciertos de prueba apareados por semilla y
      ensayo (4 x 560); p < 0.05 decide MEJOR o PEOR; si no, IGUAL.
  VEREDICTO_PLENA: MEJOR -> LA PLENA GANA POR SER LIQUIDA CON OPTIMIZACION AJUSTADA; IGUAL -> CON OPTIMIZACION
      AJUSTADA LA PLENA NO SE DISTINGUE; PEOR -> CON OPTIMIZACION AJUSTADA GANA LA NO LIQUIDA.
  Descriptivo: desvio entre semillas de cada brazo ajustado y configuracion elegida.
  Q_SL_PLENA  comb de prueba de W contra las 24 SL: p = (1 + #{SL >= W}) / 25; W GANA si p < 0.05.
  VEREDICTO_CABLEADO_CON_PLENA de Q_SL_PLENA.

Uso:
  python3 control_plena.py --motivo ../brazo_s/motivo26.json --lados lados26.json \
      --brazo-s ../brazo_s/brazo_s_recurrente.py --escape escape_motivo.py --dificil escape_dificil.py \
      --liquida liquida_entrenada.py --control control_parametros.py \
      --out-dir results/control_plena_2026-10-11 [--solo-controles]

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

MD5_CONTROL = "342069aa075256e55e6638127f55a05e"
K_SL, SEMILLAS = 24, 4
CONFIGS = {"C1": (0.10, 0.05), "C2": (0.03, 0.02)}
G = {}


def cargar(nombre, path):
    """Importa un script del repo como modulo."""
    spec = importlib.util.spec_from_file_location(nombre, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def tarea(t):
    """Entrena un brazo con una configuracion sobre una red y lo mide en prueba."""
    parte, brazo, red, k, semilla, cfg, iters = t
    ed, le = G["ed"], G["le"]
    le.SIGMA, le.LR = CONFIGS[cfg]
    Wx = G["redes"][(red, k)]
    (f_tr, th, it), hist, n_ev = le.es(ed, Wx, G["tr"], brazo, semilla, iters)
    r = le.evaluar(ed, Wx, G["te"], "PARAM", brazo, th)
    return {"parte": parte, "brazo": brazo, "red": red, "k": k, "semilla": semilla, "config": cfg, "iters": iters,
            "comb_entrenamiento": f_tr, "iter_mejor": it, "comb_prueba": r["comb"],
            "supervivencia_prueba": r["supervivencia"], "rechazo_prueba": r["rechazo"],
            "norma_extra": float(np.linalg.norm(th[26:])), "evaluaciones": n_ev, "_ac": r["acierto"],
            "theta": th.tolist()}


def main():
    """Controles, guardas, entrenamiento en dos procesos y reglas pre-registradas."""
    ap = argparse.ArgumentParser(description="Control de optimizacion y de cableado para la liquida plena")
    for k in ("--motivo", "--lados", "--brazo-s", "--escape", "--dificil", "--liquida", "--control", "--out-dir"):
        ap.add_argument(k, required=True)
    ap.add_argument("--procesos", type=int, default=2)
    ap.add_argument("--solo-controles", action="store_true")
    a = ap.parse_args()
    T0 = time.time()
    os.makedirs(a.out_dir, exist_ok=True)
    em = cargar("escape_motivo", a.escape)
    meta = {"python": platform.python_version(), "numpy": np.__version__, "maquina": platform.platform(),
            "md5_script": em.md5(os.path.abspath(__file__)), "md5_control": em.md5(a.control),
            "md5_liquida": em.md5(a.liquida), "md5_dificil": em.md5(a.dificil), "md5_escape": em.md5(a.escape),
            "md5_brazo_s": em.md5(a.brazo_s), "md5_motivo": em.md5(a.motivo), "md5_lados": em.md5(a.lados),
            "k_sl": K_SL, "semillas": SEMILLAS, "configs": CONFIGS, "procesos": a.procesos,
            "fecha_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    print("# " + json.dumps(meta, sort_keys=True), flush=True)
    if meta["md5_control"] != MD5_CONTROL:
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
    Wn, _ = mod.a_rho(M)
    redes = {("W", 0): Wn}
    for k in range(K_SL):
        ML, _ = em.shuffle_lado(mod, M, edges, lado, k)
        redes[("SL", k)] = mod.a_rho(ML)[0]
    for (nom, k), Wx in redes.items():
        if abs(mod.radio(Wx) - 0.9) > 1e-6 or (nom != "W" and float(np.max(np.abs(Wx - Wn))) < 1e-9):
            print("ABORTA: guarda de red " + nom + " k=" + str(k)); return 2
    print("GUARDA redes_nulas_ok=True SL=" + str(K_SL))
    t1 = time.time()
    f_ini = {k: le.evaluar(ed, Wn, tr, "PARAM", k, le.theta0(k, tr))["comb"] for k in ("LIQ_PLENA", "NOLIQ_PLENA")}
    seg = (time.time() - t1) / 2
    igual = len(set(f_ini.values())) == 1
    print("GUARDA punto_de_partida_igual=" + str(igual) + " seg_por_evaluacion=" + format(seg, ".3f"), flush=True)
    if not igual:
        print("ABORTA: los brazos no arrancan en el mismo punto"); return 2
    if a.solo_controles:
        print("SOLO_CONTROLES: el sujeto no se entreno ni se midio"); print("EXIT_RUN=0"); return 0

    G.update({"ed": ed, "le": le, "redes": redes, "tr": tr, "te": te})
    tareas = [("A", b, "W", 0, s, c, 60) for s in range(SEMILLAS) for b in ("LIQ_PLENA", "NOLIQ_PLENA") for c in CONFIGS]
    tareas += [("B", "LIQ_PLENA", "W", 0, 0, "C1", 40)] + [("B", "LIQ_PLENA", "SL", k, 0, "C1", 40) for k in range(K_SL)]
    res = []
    with mp.get_context("fork").Pool(a.procesos) as pool:
        for r in pool.imap_unordered(tarea, tareas):
            res.append(r)
            print("CORRIDA parte=" + r["parte"] + " brazo=" + r["brazo"] + " red=" + r["red"] + " k=" + str(r["k"])
                  + " semilla=" + str(r["semilla"]) + " config=" + r["config"] + " iters=" + str(r["iters"])
                  + " comb_entrenamiento=" + format(r["comb_entrenamiento"], ".4f") + " comb_prueba=" + format(r["comb_prueba"], ".4f")
                  + " supervivencia=" + format(r["supervivencia_prueba"], ".4f") + " rechazo=" + format(r["rechazo_prueba"], ".4f")
                  + " hechas=" + str(len(res)) + "/" + str(len(tareas)) + " seg=" + format(time.time() - T0, ".0f"), flush=True)

    elegidos = {}
    for b in ("LIQ_PLENA", "NOLIQ_PLENA"):
        elegidos[b] = []
        for s in range(SEMILLAS):
            cand = sorted([r for r in res if r["parte"] == "A" and r["brazo"] == b and r["semilla"] == s],
                          key=lambda r: r["config"])
            mejor = max(cand, key=lambda r: r["comb_entrenamiento"])
            elegidos[b].append(mejor)
        c = np.array([r["comb_prueba"] for r in elegidos[b]])
        print("RESUMEN_AJUSTADO brazo=" + b + " comb_prueba_media=" + format(c.mean(), ".4f") + " desvio="
              + format(c.std(ddof=1), ".4f") + " min=" + format(c.min(), ".4f") + " max=" + format(c.max(), ".4f")
              + " por_semilla=" + ",".join(format(x, ".4f") for x in c)
              + " configs=" + ",".join(r["config"] for r in elegidos[b]))
    A_ = np.concatenate([r["_ac"] for r in elegidos["LIQ_PLENA"]]); B_ = np.concatenate([r["_ac"] for r in elegidos["NOLIQ_PLENA"]])
    n01, n10, p = em.mcnemar(A_, B_)
    v = "IGUAL" if p >= 0.05 else ("MEJOR" if A_.mean() > B_.mean() else "PEOR")
    print("CONTRASTE P3_LIQ_PLENA_vs_NOLIQ_PLENA_ajustadas acierto_A=" + format(A_.mean(), ".4f") + " acierto_B="
          + format(B_.mean(), ".4f") + " solo_A=" + str(n10) + " solo_B=" + str(n01) + " p_mcnemar=" + format(p, ".4g") + " -> " + v)
    gana = sum(1 for x, y in zip(elegidos["LIQ_PLENA"], elegidos["NOLIQ_PLENA"]) if x["comb_prueba"] > y["comb_prueba"])
    print("SEMILLAS LIQ_PLENA gana_a_NOLIQ_PLENA_ajustada_en=" + str(gana) + "/" + str(SEMILLAS))
    vp = {"MEJOR": "LA PLENA GANA POR SER LIQUIDA CON OPTIMIZACION AJUSTADA",
          "IGUAL": "CON OPTIMIZACION AJUSTADA LA PLENA NO SE DISTINGUE",
          "PEOR": "CON OPTIMIZACION AJUSTADA GANA LA NO LIQUIDA"}[v]
    print("VEREDICTO_PLENA=" + vp)
    wB = [r for r in res if r["parte"] == "B" and r["red"] == "W"][0]["comb_prueba"]
    rep = format(wB, ".4f") == "0.9802"
    print("REPRODUCE_012=" + str(rep))
    c = np.array([r["comb_prueba"] for r in sorted([r for r in res if r["parte"] == "B" and r["red"] == "SL"], key=lambda r: r["k"])])
    n0 = int((c >= wB - 1e-12).sum()); p0 = (1 + n0) / (K_SL + 1)
    print("CONTRASTE Q_SL_PLENA comb W=" + format(wB, ".4f") + " SL_media=" + format(c.mean(), ".4f") + " SL_max="
          + format(c.max(), ".4f") + " n>=W=" + str(n0) + "/" + str(K_SL) + " p=" + format(p0, ".4f")
          + " -> " + ("W GANA" if p0 < 0.05 else "W NO GANA"))
    vc = ("CON LA LIQUIDA PLENA SIGUE PAGANDO EL CABLEADO FINO" if p0 < 0.05
          else "CON LA LIQUIDA PLENA EL CABLEADO FINO NO SE DISTINGUE DE SL")
    if not rep:
        vc += " [NO SE FIRMA: no reproduce la 012]"
    print("VEREDICTO_CABLEADO_CON_PLENA=" + vc)
    out = {"meta": meta, "controles": {k: {kk: vv for kk, vv in r.items() if kk != "acierto"} for k, r in ctrl.items()},
           "corridas": [{k: v_ for k, v_ in r.items() if not k.startswith("_")} for r in res],
           "contraste_P3": {"solo_A_ok": n10, "solo_B_ok": n01, "p_mcnemar": p, "veredicto": v},
           "q_sl_plena": {"W": wB, "valores": c.tolist(), "n_ge_W": n0, "p": p0}, "reproduce_012": rep,
           "veredictos": {"plena": vp, "cableado_con_plena": vc}, "minutos": (time.time() - T0) / 60.0}
    p_out = os.path.join(a.out_dir, "resultados.json")
    json.dump(out, open(p_out, "w"))
    print("escrito resultados.json md5=" + em.md5(p_out))
    print("minutos=" + format(out["minutos"], ".2f"))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
