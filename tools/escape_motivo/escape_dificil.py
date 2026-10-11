#!/usr/bin/env python3
"""Escape fuera del techo: amenazas rapidas y frontales, mas ruido, disparo por umbral y un estimulo que no es looming.

Por que existe. En la 010 el motivo de 26 neuronas escapo 180/180 con cualquier tau y con el brazo lineal, y
el shuffle que conserva el lado (SL) tambien: todo en el techo. Aca la tarea se endurece para que el cableado
fino (por ejemplo la exclusion LC6 -> GF de la mosca) y la tau liquida tengan algo que hacer.

Lo que cambia respecto de escape_motivo.py (todo lo demas se importa de ahi o de brazo_s_recurrente.py):
  1. Disparo por umbral, como la espiga del Giant Fiber: el robot no escapa con |c| > 1e-3 sino cuando
     max(z_GF_izq, z_GF_der) supera un umbral; en ese paso elige el lado con sign(z_GF_izq - z_GF_der) y desde
     ahi se corre balisticamente v_rob = 0.1 por paso hacia ese lado. El umbral de cada red y variante es
     1.1 x el maximo de max(GF) en 40 ensayos EN BLANCO (solo ruido, sin objeto): cada red se calibra contra
     su propio piso de ruido, sin ver ningun estimulo.
  2. Looming mas dificil: az0 en {-90, -45, -20, -10, 10, 20, 45, 90} grados, v en {0.25, 1/3, 0.4} (llega en
     40, 31 y 25 pasos), ruido sigma en {0.1, 0.3}, 10 repeticiones = 480 ensayos, T = 50, lazo cerrado.
     Calibracion, solo con controles: el primer humo (v en {1/3, 0.4, 0.5}, T = 40) dio C+L supervivencia
     0.5333 (instrumento INVALIDO); se bajo v y se subio T antes de correr al sujeto.
  3. Un estimulo que NO es looming: el mismo objeto girando alrededor del robot a distancia fija 4 (theta
     constante, dtheta = 0), az0 en {-60, -20, 20, 60}, 0.05 rad por paso alternando el sentido, sigma en
     {0.1, 0.3}, 10 repeticiones = 80 ensayos. Correcto = NO disparar en T pasos (rechazo).
  4. Modelo de entrada (simplificacion de literatura, declarada): LC4 = dtheta / (dtheta + 0.02) (velocidad de
     expansion); LPLC2 = theta / theta_col SOLO si dtheta > 0 (tamano durante la expansion); LC6 = theta /
     theta_col sin exigir expansion. Se eligio para que la exclusion LC6 -> GF tenga algo que hacer: si con
     esto la mosca no le gana a SL, el cableado fino no paga ni en el caso que lo favorece.

Puntaje de cada red y variante: comb = (supervivencia en looming + rechazo en no-looming) / 2.

Brazos y variantes: W, S, SL y B como en escape_motivo.py (las mismas funciones y semillas, K = 200), con
TANH/LINEAL x FIJA_HET/FIJA_UNI/LIQUIDA. Ruido: default_rng(20261012), un arreglo fijo por tipo de ensayo.

Controles del instrumento (sin normalizar el radio):
  C+L  reflejo escrito a mano SIN LC6: cada LC4 y LPLC2 -> GF de su lado, peso 1 / (LC4 + LPLC2 de ese lado).
  C+6  el mismo reflejo MAS LC6 -> GF de su lado con peso 1/2 por LC6: debe tener falsas alarmas.
  C0   W = 0.

Reglas PRE-REGISTRADAS (escritas antes de la corrida completa; el humo imprime solo los controles):
  Validez (TANH + FIJA_HET): C+L supervivencia >= 0.60 y rechazo >= 0.90; C+6 rechazo <= 0.50; C0
    supervivencia <= 0.05. Si no se cumple: exit 3 y ningun veredicto de sujeto.
  Q1  comb, W vs SL (cableado fino). W GANA si p = (1 + #{SL >= W}) / (K + 1) < 0.05.
  Q2  comb, W vs S.   Q3  comb, W vs B.   Mismo criterio.
  Q4  rechazo, W vs SL.   Q5  supervivencia, W vs SL.   Mismo criterio (secundarios).
  Q6  en W, por ensayo pareado y McNemar exacto a dos colas, p < 0.05, sobre supervivencia y sobre rechazo:
      LIQUIDA vs FIJA_HET, FIJA_UNI vs FIJA_HET, LINEAL vs TANH (FIJA_HET).
  Q7  en la poblacion de redes S y SL: diferencia comb(TANH+LIQUIDA) - comb(TANH+FIJA_HET) red por red, test
      del signo exacto a dos colas, p < 0.05.
  VEREDICTO_DETALLE de Q1; VEREDICTO_FUNCION de Q2; VEREDICTO_TAU_W de Q6 liquida (MEJOR si alguna metrica
  mejora y ninguna empeora, PEOR al reves, MIXTO si una y una, IGUAL si ninguna); VEREDICTO_TAU_POBLACION de
  Q7 sobre SL; VEREDICTO_LINEAL de Q6 lineal (misma regla). Si W saca comb = 1 se imprime W_EN_EL_TECHO.

Uso:
  python3 escape_dificil.py --motivo ../brazo_s/motivo26.json --lados lados26.json \
      --brazo-s ../brazo_s/brazo_s_recurrente.py --escape escape_motivo.py --k 200 \
      --out-dir results/escape_dificil_2026-10-11      [--solo-controles para el humo]

Codigos de salida: 0 corrida completa con instrumento valido; 2 un guard fallo; 3 instrumento invalido.
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

R_OBJ, R_ROB, D0, V_ROB, T, K_LC4 = 1.0, 0.5, 10.0, 0.1, 50, 0.02
AZ_LOOM = [-90, -45, -20, -10, 10, 20, 45, 90]
V_LOOM = [0.25, 1.0 / 3.0, 0.4]
SIGMAS = [0.1, 0.3]
REPS = 10
R_CIRC, W_CIRC = 4.0, 0.05
AZ_CIRC = [-60, -20, 20, 60]
REPS_NL = 10
REPS_BLANCO = 20
FACTOR_UMBRAL = 1.1
SEMILLA_RUIDO = 20261012
TAU_UNI = 0.119
TH_COL = 2.0 * math.atan(R_OBJ / (R_OBJ + R_ROB))
VARIANTES = [("TANH", "FIJA_HET"), ("TANH", "FIJA_UNI"), ("TANH", "LIQUIDA"),
             ("LINEAL", "FIJA_HET"), ("LINEAL", "FIJA_UNI"), ("LINEAL", "LIQUIDA")]
PRINCIPAL = "TANH+FIJA_HET"
MD5_MOTIVO = "eb6e53e047c864a46c56bf38b397d289"
MD5_BRAZO_S = "f8b10037e70dfe897ff2d841077419b4"
MD5_ESCAPE = "9720998291e3f08c6082e6c67d142759"


def cargar(nombre, path):
    """Importa un script del repo como modulo, para usar sus funciones tal cual."""
    spec = importlib.util.spec_from_file_location(nombre, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


def construir_ctx(lados):
    """Ensayos, ruido fijo y mascaras."""
    tipo = [f["tipo_motivo"] for f in lados["neuronas"]]
    lado = [f["side"] for f in lados["neuronas"]]
    vpn = np.array([t in ("LC4", "LPLC2", "LC6") for t in tipo], dtype=float)
    mk = {k: np.array([t == k for t in tipo], dtype=float) for k in ("LC4", "LPLC2", "LC6")}
    m_der = np.array([s == "right" for s in lado], dtype=float) * vpn
    m_izq = np.array([s == "left" for s in lado], dtype=float) * vpn
    gl = [i for i, t in enumerate(tipo) if t == "GF" and lado[i] == "left"]
    gr = [i for i, t in enumerate(tipo) if t == "GF" and lado[i] == "right"]
    if len(gl) != 1 or len(gr) != 1:
        raise SystemExit("ABORTA: hace falta un GF por lado")
    loom = [(math.radians(a), v, s) for a in AZ_LOOM for v in V_LOOM for s in SIGMAS for _ in range(REPS)]
    nl = [(math.radians(a), s, 1.0 if r % 2 == 0 else -1.0) for a in AZ_CIRC for s in SIGMAS for r in range(REPS_NL)]
    bl = [s for s in SIGMAS for _ in range(REPS_BLANCO)]
    rng = np.random.default_rng(SEMILLA_RUIDO)
    tau_het = np.random.default_rng(119).uniform(0.06, 0.18, size=26)
    return {"tipo": tipo, "lado": lado, "vpn": vpn, "mk": mk, "m_der": m_der, "m_izq": m_izq,
            "GL": gl[0], "GR": gr[0],
            "loom_az": np.array([e[0] for e in loom]), "loom_v": np.array([e[1] for e in loom]),
            "loom_s": np.array([e[2] for e in loom]),
            "nl_az": np.array([e[0] for e in nl]), "nl_s": np.array([e[1] for e in nl]),
            "nl_dir": np.array([e[2] for e in nl]), "bl_s": np.array(bl),
            "r_loom": rng.normal(size=(len(loom), T, 26)), "r_nl": rng.normal(size=(len(nl), T, 26)),
            "r_bl": rng.normal(size=(len(bl), T, 26)),
            "tau_het": tau_het, "logit_het": np.log(tau_het / (1.0 - tau_het)),
            "Vh": np.random.default_rng(120).normal(0.0, 1.0 / math.sqrt(26), size=(26, 26)),
            "Vx": np.random.default_rng(121).normal(0.0, 1.0 / math.sqrt(26), size=(26, 26))}


def entrada(th, dth, az, sig, r_t, ctx):
    """Entrada de las 20 visuales segun el modelo declarado en el docstring."""
    f4 = dth / (dth + K_LC4)
    f2 = (th / TH_COL) * (dth > 0)
    f6 = th / TH_COL
    mk = ctx["mk"]
    rasgo = f4[:, None] * mk["LC4"][None, :] + f2[:, None] * mk["LPLC2"][None, :] + f6[:, None] * mk["LC6"][None, :]
    d_der = 0.5 * (1.0 + np.sin(az)); d_izq = 1.0 - d_der
    ojo = d_der[:, None] * ctx["m_der"][None, :] + d_izq[:, None] * ctx["m_izq"][None, :]
    return rasgo * ojo + sig[:, None] * r_t * ctx["vpn"][None, :]


def paso(z, x, Wn, nolin, modo, ctx):
    """Un paso de z <- (1 - tau) z + tau phi(W z + x)."""
    pre = z @ Wn.T + x
    f = pre if nolin == "LINEAL" else np.tanh(pre)
    if modo == "LIQUIDA":
        tt = 1.0 / (1.0 + np.exp(-(ctx["logit_het"][None, :] + x @ ctx["Vx"].T + z @ ctx["Vh"].T)))
    elif modo == "FIJA_HET":
        tt = ctx["tau_het"][None, :]
    elif modo == "FIJA_UNI":
        tt = np.full((1, 26), TAU_UNI)
    else:
        raise SystemExit("ABORTA: modo de tau " + modo)
    z = (1.0 - tt) * z + tt * f
    if not np.all(np.isfinite(z)):
        raise SystemExit("ABORTA: estado no finito")
    return z


def blanco(Wn, nolin, modo, ctx):
    """Maximo de max(GF) en los ensayos en blanco (solo ruido)."""
    n = len(ctx["bl_s"]); z = np.zeros((n, 26)); pico = np.full(n, -np.inf); cero = np.zeros(n)
    for t in range(T):
        z = paso(z, entrada(cero, cero, cero, ctx["bl_s"], ctx["r_bl"][:, t, :], ctx), Wn, nolin, modo, ctx)
        pico = np.maximum(pico, np.maximum(z[:, ctx["GL"]], z[:, ctx["GR"]]))
    return float(pico.max())


def looming(Wn, nolin, modo, ctx, umbral, forzar=None):
    """Lazo cerrado con disparo por umbral y escape balistico."""
    az0, v, sg = ctx["loom_az"], ctx["loom_v"], ctx["loom_s"]
    n = len(az0)
    P0 = np.stack([D0 * np.sin(az0), D0 * np.cos(az0)], 1); u = P0 / D0
    z = np.zeros((n, 26)); px = np.zeros(n); vivo = np.ones(n, dtype=bool)
    disp = np.zeros(n, dtype=bool); dirr = np.zeros(n); lat = np.full(n, -1)
    if forzar is not None:
        disp[:] = True; dirr[:] = float(forzar); lat[:] = 0
    th_prev = None
    for t in range(T):
        Pt = P0 - u * np.minimum(v * t, D0)[:, None]
        rx = Pt[:, 0] - px; ry = Pt[:, 1]; dist = np.hypot(rx, ry)
        vivo = vivo & ~(dist < R_OBJ + R_ROB)
        az = np.arctan2(rx, ry)
        th = 2.0 * np.arctan(R_OBJ / np.maximum(dist, R_OBJ + R_ROB))
        dth = np.zeros(n) if th_prev is None else np.maximum(th - th_prev, 0.0)
        th_prev = th
        z = paso(z, entrada(th, dth, az, sg, ctx["r_loom"][:, t, :], ctx), Wn, nolin, modo, ctx)
        g = np.maximum(z[:, ctx["GL"]], z[:, ctx["GR"]]); c = z[:, ctx["GL"]] - z[:, ctx["GR"]]
        nuevo = (~disp) & (g > umbral)
        dirr[nuevo] = np.sign(c[nuevo]); lat[nuevo] = t; disp = disp | nuevo
        px = px + np.where(vivo & disp, V_ROB * dirr, 0.0)
    return {"sv": vivo, "lado_ok": disp & (dirr == -np.sign(az0)), "lat": lat}


def no_looming(Wn, nolin, modo, ctx, umbral):
    """Objeto girando a distancia fija: correcto es no disparar."""
    n = len(ctx["nl_az"]); z = np.zeros((n, 26)); disp = np.zeros(n, dtype=bool)
    th = np.full(n, 2.0 * math.atan(R_OBJ / R_CIRC)); cero = np.zeros(n)
    for t in range(T):
        az = ctx["nl_az"] + ctx["nl_dir"] * W_CIRC * t
        z = paso(z, entrada(th, cero, az, ctx["nl_s"], ctx["r_nl"][:, t, :], ctx), Wn, nolin, modo, ctx)
        disp = disp | (np.maximum(z[:, ctx["GL"]], z[:, ctx["GR"]]) > umbral)
    return {"rj": ~disp}


def medir(Wn, ctx, variantes):
    """Umbral, supervivencia, lado, latencia, rechazo y comb por variante."""
    out = {}
    for (nl, mt) in variantes:
        umb = FACTOR_UMBRAL * blanco(Wn, nl, mt, ctx)
        L = looming(Wn, nl, mt, ctx, umb); N = no_looming(Wn, nl, mt, ctx, umb)
        lat = L["lat"][L["lat"] >= 0]
        sv, rj = float(L["sv"].mean()), float(N["rj"].mean())
        out[nl + "+" + mt] = {"umbral": umb, "supervivencia": sv, "lado_ok": float(L["lado_ok"].mean()),
                              "disparo_looming": float((L["lat"] >= 0).mean()),
                              "latencia_mediana": float(np.median(lat)) if lat.size else -1.0,
                              "rechazo": rj, "comb": 0.5 * (sv + rj), "_sv": L["sv"], "_rj": N["rj"]}
    return out


def signo(d):
    """Test del signo exacto a dos colas. Devuelve (positivos, negativos, p)."""
    pos = int(np.sum(d > 1e-12)); neg = int(np.sum(d < -1e-12)); m = pos + neg
    if m == 0:
        return pos, neg, 1.0
    k = min(pos, neg)
    return pos, neg, min(1.0, 2.0 * sum(math.comb(m, i) for i in range(k + 1)) / (2.0 ** m))


def linea(nom, r):
    """Linea de log de una red en una variante."""
    return (nom + " umbral=" + format(r["umbral"], ".4f") + " supervivencia=" + format(r["supervivencia"], ".4f")
            + " lado_ok=" + format(r["lado_ok"], ".4f") + " disparo_looming=" + format(r["disparo_looming"], ".4f")
            + " latencia_mediana=" + str(r["latencia_mediana"]) + " rechazo=" + format(r["rechazo"], ".4f")
            + " comb=" + format(r["comb"], ".4f"))


def regla(sv, rj):
    """Combina dos veredictos McNemar (IGUAL/MEJOR/PEOR) en uno."""
    s = {sv, rj}
    if s == {"IGUAL"}:
        return "IGUAL"
    if "MEJOR" in s and "PEOR" in s:
        return "MIXTO"
    return "MEJOR" if "MEJOR" in s else "PEOR"


def main():
    """Corre controles, sujeto y nulos; aplica las reglas pre-registradas."""
    ap = argparse.ArgumentParser(description="Escape fuera del techo")
    for k in ("--motivo", "--lados", "--brazo-s", "--escape", "--out-dir"):
        ap.add_argument(k, required=True)
    ap.add_argument("--k", type=int, default=200)
    ap.add_argument("--solo-controles", action="store_true")
    a = ap.parse_args()
    T0 = time.time()
    os.makedirs(a.out_dir, exist_ok=True)
    em = cargar("escape_motivo", a.escape)
    meta = {"python": platform.python_version(), "numpy": np.__version__, "maquina": platform.platform(),
            "md5_script": em.md5(os.path.abspath(__file__)), "md5_motivo": em.md5(a.motivo),
            "md5_lados": em.md5(a.lados), "md5_brazo_s": em.md5(a.brazo_s), "md5_escape": em.md5(a.escape),
            "k": a.k, "fecha_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "fisica": {"R_obj": R_OBJ, "r_robot": R_ROB, "d0": D0, "v_robot": V_ROB, "T": T, "k_lc4": K_LC4,
                       "az_loom": AZ_LOOM, "v_loom": V_LOOM, "sigmas": SIGMAS, "reps": REPS, "r_circ": R_CIRC,
                       "w_circ": W_CIRC, "az_circ": AZ_CIRC, "reps_nl": REPS_NL, "reps_blanco": REPS_BLANCO,
                       "factor_umbral": FACTOR_UMBRAL, "semilla_ruido": SEMILLA_RUIDO}}
    try:
        for line in open("/proc/cpuinfo"):
            if line.startswith("model name"):
                meta["cpu"] = line.split(":", 1)[1].strip(); break
    except OSError:
        pass
    print("# " + json.dumps(meta, sort_keys=True))
    if (meta["md5_motivo"], meta["md5_brazo_s"], meta["md5_escape"]) != (MD5_MOTIVO, MD5_BRAZO_S, MD5_ESCAPE):
        print("ABORTA: md5 de una entrada distinto del pin"); return 2
    lados = json.load(open(a.lados))
    if lados.get("fallas"):
        print("ABORTA: lados con fallas"); return 2
    mod = cargar("brazo_s_recurrente", a.brazo_s)
    M, edges, mot = mod.cargar_motivo(a.motivo)
    if [f["root_id"] for f in lados["neuronas"]] != [int(x) for x in mot["orden_root_ids"]]:
        print("ABORTA: orden de lados distinto del motivo"); return 2
    ctx = construir_ctx(lados)
    lado, tipo = ctx["lado"], ctx["tipo"]
    lc6_gf = sum(1 for (i, j) in edges if tipo[i] == "LC6" and tipo[j] == "GF")
    print("MOTIVO aristas=" + str(len(edges)) + " LC6->GF=" + str(lc6_gf) + " cruzadas="
          + str(sum(1 for (i, j) in edges if lado[i] != lado[j])))
    print("ENSAYOS looming=" + str(len(ctx["loom_az"])) + " no_looming=" + str(len(ctx["nl_az"]))
          + " blanco=" + str(len(ctx["bl_s"])) + " T=" + str(T))

    def reflejo(con_lc6):
        C = np.zeros((26, 26))
        for side, g in (("left", ctx["GL"]), ("right", ctx["GR"])):
            base = [i for i in range(26) if lado[i] == side and tipo[i] in ("LC4", "LPLC2")]
            for i in base:
                C[g, i] = 1.0 / len(base)
            if con_lc6:
                for i in range(26):
                    if lado[i] == side and tipo[i] == "LC6":
                        C[g, i] = 0.5
        return C

    clave = PRINCIPAL
    ctrl = {"C+L": medir(reflejo(False), ctx, [("TANH", "FIJA_HET")]),
            "C+6": medir(reflejo(True), ctx, [("TANH", "FIJA_HET")]),
            "C0": medir(np.zeros((26, 26)), ctx, [("TANH", "FIJA_HET")])}
    for nom in ("C+L", "C+6", "C0"):
        print(linea("CONTROL " + nom, ctrl[nom][clave]))
    ref = float(looming(np.zeros((26, 26)), "TANH", "FIJA_HET", ctx, 0.0, forzar=-1.0)["sv"].mean())
    print("REFERENCIA escape inmediato ciego al lado (siempre a la izquierda desde t=0) supervivencia=" + format(ref, ".4f"))
    valido = (ctrl["C+L"][clave]["supervivencia"] >= 0.60 and ctrl["C+L"][clave]["rechazo"] >= 0.90
              and ctrl["C+6"][clave]["rechazo"] <= 0.50 and ctrl["C0"][clave]["supervivencia"] <= 0.05)
    print("CHEQUEO INSTRUMENTO " + ("VALIDO" if valido else "INVALIDO"))
    res = {"meta": meta, "controles": {k: em.resumen(v) for k, v in ctrl.items()}, "referencia": ref,
           "instrumento_valido": valido}
    if not valido:
        json.dump(res, open(os.path.join(a.out_dir, "resultados.json"), "w"), indent=1)
        print("EXIT_RUN=3"); return 3
    if a.solo_controles:
        json.dump(res, open(os.path.join(a.out_dir, "resultados_controles.json"), "w"), indent=1)
        print("SOLO_CONTROLES: el sujeto no se corrio"); print("EXIT_RUN=0"); return 0

    Wn, _ = mod.a_rho(M)
    mW = medir(Wn, ctx, VARIANTES)
    for k_, r in mW.items():
        print(linea("SUJETO W variante=" + k_, r))
    if mW[clave]["comb"] >= 1.0 - 1e-12:
        print("W_EN_EL_TECHO")
    nulos = {"S": [], "SL": [], "B": []}
    vec = {"S": [], "SL": [], "B": []}
    for k in range(a.k):
        MS, _ = mod.matriz_shuffle(M, edges, k)
        ML, _ = em.shuffle_lado(mod, M, edges, lado, k)
        MB = np.random.default_rng(em.B_SEED0 + k).normal(0.0, 1.0, size=(26, 26))
        for nom, Mx in (("S", MS), ("SL", ML), ("B", MB)):
            Wx, _ = mod.a_rho(Mx)
            if abs(mod.radio(Wx) - 0.9) > 1e-6 or (nom != "B" and float(np.max(np.abs(Wx - Wn))) < 1e-9):
                print("ABORTA: guard de " + nom + " k=" + str(k)); return 2
            m = medir(Wx, ctx, VARIANTES)
            nulos[nom].append(em.resumen(m))
        if k % 20 == 0 or k == a.k - 1:
            print("progreso k=" + str(k) + " " + " ".join(nom + "_comb=" + format(nulos[nom][-1][clave]["comb"], ".4f")
                                                       for nom in ("S", "SL", "B"))
                  + " seg=" + format(time.time() - T0, ".0f"), flush=True)

    def serie(nom, var, met):
        return np.array([d[var][met] for d in nulos[nom]])

    for nom in ("S", "SL", "B"):
        for (nl, mt) in VARIANTES:
            var = nl + "+" + mt
            print("NULO " + nom + " variante=" + var + " " + " ".join(
                met + "_media=" + format(serie(nom, var, met).mean(), ".4f") for met in ("supervivencia", "rechazo", "comb"))
                + " comb_p95=" + format(np.percentile(serie(nom, var, "comb"), 95), ".4f"))
    w = mW[clave]; con = {}
    for et, nom, met in (("Q1", "SL", "comb"), ("Q2", "S", "comb"), ("Q3", "B", "comb"),
                         ("Q4", "SL", "rechazo"), ("Q5", "SL", "supervivencia")):
        nl = serie(nom, clave, met); p = em.p_emp(w[met], nl)
        con[et] = {"nulo": nom, "metrica": met, "W": w[met], "nulo_media": float(nl.mean()),
                   "n_nulo_ge_W": int(np.sum(nl >= w[met] - 1e-12)), "p_emp": p, "W_gana": bool(p < 0.05)}
        print("CONTRASTE " + et + " " + met + " W=" + format(w[met], ".4f") + " " + nom + "_media=" + format(nl.mean(), ".4f")
              + " n_" + nom + ">=W=" + str(con[et]["n_nulo_ge_W"]) + "/" + str(len(nl)) + " p_emp=" + format(p, ".4f")
              + " -> " + ("W GANA" if p < 0.05 else "W NO GANA"))
    q6 = {}
    for et, va, vb in (("Q6_liquida", "TANH+LIQUIDA", "TANH+FIJA_HET"), ("Q6_uniforme", "TANH+FIJA_UNI", "TANH+FIJA_HET"),
                       ("Q6_lineal", "LINEAL+FIJA_HET", "TANH+FIJA_HET")):
        sig = {}
        for met, kk in (("supervivencia", "_sv"), ("rechazo", "_rj")):
            n01, n10, p = em.mcnemar(mW[va][kk], mW[vb][kk])
            dif = mW[va][met] - mW[vb][met]
            sig[met] = "IGUAL" if p >= 0.05 else ("MEJOR" if dif > 0 else "PEOR")
            con[et + "_" + met] = {"A": va, "B": vb, "A_val": mW[va][met], "B_val": mW[vb][met], "solo_A_ok": n10,
                                   "solo_B_ok": n01, "p_mcnemar": p, "A_vs_B": sig[met]}
            print("CONTRASTE " + et + "_" + met + " " + va + "=" + format(mW[va][met], ".4f") + " " + vb + "="
                  + format(mW[vb][met], ".4f") + " solo_A=" + str(n10) + " solo_B=" + str(n01) + " p_mcnemar="
                  + format(p, ".4f") + " -> " + va + " " + sig[met])
        q6[et] = regla(sig["supervivencia"], sig["rechazo"])
    for nom in ("S", "SL"):
        d = serie(nom, "TANH+LIQUIDA", "comb") - serie(nom, clave, "comb")
        pos, neg, p = signo(d)
        con["Q7_" + nom] = {"liquida_mejor": pos, "liquida_peor": neg, "p_signo": p, "dif_media": float(d.mean())}
        print("CONTRASTE Q7_" + nom + " comb(LIQUIDA)-comb(FIJA_HET) dif_media=" + format(d.mean(), "+.4f")
              + " liquida_mejor=" + str(pos) + " liquida_peor=" + str(neg) + " p_signo=" + format(p, ".4g")
              + " -> " + ("IGUAL" if p >= 0.05 else ("LIQUIDA MEJOR" if pos > neg else "LIQUIDA PEOR")))
    q7 = con["Q7_SL"]
    v = {"detalle": "PAGA EL CABLEADO FINO: W GANA A SL" if con["Q1"]["W_gana"] else "EL CABLEADO FINO NO SE DISTINGUE DE SL",
         "funcion": "W GANA A S" if con["Q2"]["W_gana"] else "W NO GANA A S",
         "tau_w": {"IGUAL": "LA LIQUIDA NO SE DISTINGUE DE LA FIJA EN LA MOSCA", "MEJOR": "LA LIQUIDA PAGA EN LA MOSCA",
                   "PEOR": "LA LIQUIDA EMPEORA EN LA MOSCA", "MIXTO": "LA LIQUIDA ES MIXTA EN LA MOSCA"}[q6["Q6_liquida"]],
         "tau_poblacion": ("LA LIQUIDA NO SE DISTINGUE EN LA POBLACION SL" if q7["p_signo"] >= 0.05 else
                           ("LA LIQUIDA PAGA EN LA POBLACION SL" if q7["liquida_mejor"] > q7["liquida_peor"]
                            else "LA LIQUIDA EMPEORA EN LA POBLACION SL")),
         "lineal": {"IGUAL": "EL LINEAL NO SE DISTINGUE DE TANH", "MEJOR": "EL LINEAL GANA A TANH",
                    "PEOR": "TANH GANA AL LINEAL", "MIXTO": "LINEAL Y TANH MIXTOS"}[q6["Q6_lineal"]]}
    for k_ in ("funcion", "detalle", "tau_w", "tau_poblacion", "lineal"):
        print("VEREDICTO_" + k_.upper() + "=" + v[k_])
    res.update({"W": em.resumen(mW), "nulos": nulos, "contrastes": con, "veredictos": v,
                "minutos": (time.time() - T0) / 60.0})
    p_out = os.path.join(a.out_dir, "resultados.json")
    json.dump(res, open(p_out, "w"))
    print("escrito resultados.json md5=" + em.md5(p_out))
    print("minutos=" + format(res["minutos"], ".2f"))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
