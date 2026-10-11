#!/usr/bin/env python3
"""Brazo S en la funcion propia del motivo: looming -> escape con lado, a lazo abierto y a lazo cerrado.

Por que existe. La 008 corrio el motivo de escape de 26 neuronas como reservorio en cuatro tareas
genericas y el cableado empato con su shuffle 4/4: eso no mide la funcion del motivo. Aca el motivo
recibe la entrada por sus propias neuronas visuales (LC4, LPLC2 y LC6, cada una por el ojo de su lado)
y se lee SOLO por sus Giant Fiber (DNp01), uno por hemisferio. No se entrena nada: la pregunta es si
el cableado de la mosca, tal cual, saca al robot del camino de la amenaza mejor que su shuffle.

Sustrato, comun a todos los brazos (el de SparseLTC, sin entrada aleatoria U):
  z(t+1) = (1 - tau_t) z(t) + tau_t phi(W z(t) + x(t)),   phi = tanh, o identidad en el brazo LINEAL
  W = matriz del brazo llevada a radio espectral 0.9 con a_rho de brazo_s_recurrente.py (verbatim).
  x(t) entra SOLO en las 20 neuronas visuales; los GF y los DNp09 no reciben entrada externa.

Estimulo y fisica (2D, unidades de largo del robot, un paso por tick):
  Un objeto de radio R=1 sale a d0=10 con azimut az0 (positivo a la derecha; el robot mira a +y) y va
  en linea recta hacia la posicion INICIAL del robot a v por paso; al llegar se queda ahi.
  theta = 2 atan(R / max(dist, R + r)), r = 0.5 (radio del robot); theta_col = theta en el contacto.
  Rasgos: LPLC2 y LC6 = theta / theta_col; LC4 = dtheta / (dtheta + 0.02) (dtheta >= 0).
  Ojo: d_der = (1 + sin az) / 2, d_izq = 1 - d_der, con az el azimut ACTUAL del objeto visto por el robot.
  x_i = rasgo(tipo_i) * d(lado_i) + 0.05 * ruido_i(t); el ruido es UN arreglo fijo (n, T, 26) de
  default_rng(20261011): todos los brazos ven exactamente los mismos ensayos (pareados).
  Condiciones: az0 en {-90, -60, -30, 30, 60, 90} grados, v en {0.2, 0.25, 1/3}, 10 repeticiones = 180.
  T = 60 pasos. Lectura fija: c(t) = z_GF_izq - z_GF_der (amenaza a la derecha -> GF derecho -> c < 0).
  Lazo abierto: el robot no se mueve; D = suma de c(t) hasta la llegada; ACIERTA si |D| > 1e-9 y
    sign(D) = -sign(az0).
  Lazo cerrado: cada paso, si |c| > 1e-3 el robot se corre v_rob = 0.1 en x con signo de c (c < 0 ->
    izquierda, lejos de una amenaza a la derecha); choca si dist < R + r; SOBREVIVE si no choca en T.

Brazos:
  W    motivo real (motivo26.json, 88 aristas).
  S    shuffle de grado in/out exacto, matriz_shuffle de brazo_s_recurrente.py VERBATIM, k = 0..K-1
       (k = 0 es el S del brazo W de agosto). Rompe la lateralidad.
  SL   shuffle de grado exacto DENTRO de cada hemisferio: ms_shuffle verbatim aplicado por separado a las
       aristas izq->izq y der->der, con los pesos permutados dentro de cada lado; las cruzadas, si hubiera,
       quedan fijas. Conserva la lateralidad y rompe el cableado fino (por ejemplo, la exclusion LC6 -> GF).
  B    matriz densa normal, default_rng(9000 + k), llevada a rho 0.9: ruido congelado.
  Controles del instrumento (sin normalizar el radio, son feedforward o nulos):
  C+   reflejo escrito a mano: cada neurona visual -> GF de su lado con peso 1 / (visuales de ese lado).
  C0   W = 0: los GF no reciben nada.
Variantes de tau: FIJA_HET (U[0.06, 0.18], default_rng(119), la de la 008), FIJA_UNI (0.119, la del
  motor y de swarm/), LIQUIDA (tau_t = sigmoid(logit(tau_het) + Vx x + Vh z), Vh = default_rng(120) y
  Vx = default_rng(121), ambas N(0, 1/sqrt(26)), congeladas, como LiquidCell sin entrenar).
No linealidad: TANH (producto) y LINEAL (brazo lineal obligatorio).

Reglas PRE-REGISTRADAS (escritas antes de la corrida completa; la de humo imprime solo los controles):
  Validez del instrumento (TANH + FIJA_HET): C+ acierto >= 0.95 y supervivencia >= 0.90; C0 acierto = 0
    y supervivencia <= 0.05. Si no se cumple: exit 3 y ningun veredicto de sujeto.
  P1  W vs S, acierto a lazo abierto (TANH + FIJA_HET). W GANA si p = (1 + #{S >= W}) / (K + 1) < 0.05.
  P2  W vs SL, acierto, mismo criterio.
  P3  W vs S y W vs SL, supervivencia a lazo cerrado, mismo criterio.
  P4  W vs B, acierto y supervivencia, mismo criterio.
  P5  tau en W: LIQUIDA vs FIJA_HET y FIJA_UNI vs FIJA_HET, por ensayo pareado, McNemar exacto a dos colas,
      p < 0.05; sobre supervivencia y sobre acierto. Para S, SL y B se reportan las medias por variante.
  P6  no linealidad en W: LINEAL vs TANH (FIJA_HET), McNemar exacto, p < 0.05.
  VEREDICTO_FUNCION  sale de P3 contra S;  VEREDICTO_DETALLE de P3 contra SL;
  VEREDICTO_TAU      de P5 (supervivencia, LIQUIDA vs FIJA_HET);  VEREDICTO_LINEAL de P6 (supervivencia).

Uso:
  python3 escape_motivo.py --motivo ../brazo_s/motivo26.json --lados lados26.json \
      --brazo-s ../brazo_s/brazo_s_recurrente.py --k 200 --out-dir results/escape_motivo_2026-10-11
  Humo (solo controles, sin mirar el sujeto): agregar --solo-controles

Codigos de salida: 0 corrida completa con instrumento valido (el veredicto del sujeto va en el log);
2 un guard fallo (md5, lados, shuffle invalido, W == S o SL, radio distinto de 0.9); 3 instrumento invalido.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import platform
import sys
import time

import numpy as np

R_OBJ, R_ROB, D0, V_ROB, T, EPS, RUIDO, K_LC4 = 1.0, 0.5, 10.0, 0.1, 60, 1e-3, 0.05, 0.02
AZ_GRADOS = [-90, -60, -30, 30, 60, 90]
VELOCIDADES = [0.2, 0.25, 1.0 / 3.0]
REPS = 10
SEMILLA_RUIDO = 20261011
B_SEED0 = 9000
SL_SEED_IZQ, SL_SEED_DER = 100000, 200000
TAU_UNI = 0.119
TH_COL = 2.0 * math.atan(R_OBJ / (R_OBJ + R_ROB))
VARIANTES = [("TANH", "FIJA_HET"), ("TANH", "FIJA_UNI"), ("TANH", "LIQUIDA"),
             ("LINEAL", "FIJA_HET"), ("LINEAL", "FIJA_UNI"), ("LINEAL", "LIQUIDA")]
PRINCIPAL = ("TANH", "FIJA_HET")
MD5_MOTIVO = "eb6e53e047c864a46c56bf38b397d289"
MD5_BRAZO_S = "f8b10037e70dfe897ff2d841077419b4"


def md5(path):
    """md5 de un archivo."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def cargar_brazo_s(path):
    """Importa brazo_s_recurrente.py como modulo, para usar su shuffle y su a_rho tal cual."""
    spec = importlib.util.spec_from_file_location("brazo_s_recurrente", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["brazo_s_recurrente"] = mod
    spec.loader.exec_module(mod)
    return mod


def contexto(lados):
    """Ensayos, ruido fijo y mascaras de entrada a partir de los lados de las 26 neuronas."""
    az0, vel = [], []
    for a in AZ_GRADOS:
        for v in VELOCIDADES:
            for _ in range(REPS):
                az0.append(math.radians(a)); vel.append(v)
    n = len(az0)
    tipo = [f["tipo_motivo"] for f in lados["neuronas"]]
    lado = [f["side"] for f in lados["neuronas"]]
    vpn = np.array([t in ("LC4", "LPLC2", "LC6") for t in tipo], dtype=float)
    m_lc4 = np.array([t == "LC4" for t in tipo], dtype=float)
    m_ang = np.array([t in ("LPLC2", "LC6") for t in tipo], dtype=float)
    m_der = np.array([s == "right" for s in lado], dtype=float) * vpn
    m_izq = np.array([s == "left" for s in lado], dtype=float) * vpn
    gf = [i for i, t in enumerate(tipo) if t == "GF"]
    gl = [i for i in gf if lado[i] == "left"]
    gr = [i for i in gf if lado[i] == "right"]
    if len(gl) != 1 or len(gr) != 1:
        raise SystemExit("ABORTA: hace falta un GF por lado; hay izq=" + str(gl) + " der=" + str(gr))
    tau_het = np.random.default_rng(119).uniform(0.06, 0.18, size=26)
    return {"n": n, "az0": np.array(az0), "v": np.array(vel), "tipo": tipo, "lado": lado,
            "ruido": np.random.default_rng(SEMILLA_RUIDO).normal(0.0, 1.0, size=(n, T, 26)),
            "vpn": vpn, "m_lc4": m_lc4, "m_ang": m_ang, "m_der": m_der, "m_izq": m_izq,
            "GL": gl[0], "GR": gr[0], "tau_het": tau_het,
            "logit_het": np.log(tau_het / (1.0 - tau_het)),
            "Vh": np.random.default_rng(120).normal(0.0, 1.0 / math.sqrt(26), size=(26, 26)),
            "Vx": np.random.default_rng(121).normal(0.0, 1.0 / math.sqrt(26), size=(26, 26))}


def simular(Wn, nolin, modo_tau, lazo, ctx, forzar=None):
    """Corre los n ensayos en paralelo. lazo=False: acierto de lado; lazo=True: supervivencia."""
    n, az0, v = ctx["n"], ctx["az0"], ctx["v"]
    P0 = np.stack([D0 * np.sin(az0), D0 * np.cos(az0)], 1)
    u = P0 / D0
    t_arr = np.ceil(D0 / v - 1e-9).astype(int)
    z = np.zeros((n, 26)); px = np.zeros(n)
    vivo = np.ones(n, dtype=bool); t_muerte = np.full(n, -1)
    D = np.zeros(n); lat = np.full(n, -1)
    th_prev = None
    if modo_tau == "FIJA_HET":
        tau = ctx["tau_het"][None, :]
    elif modo_tau == "FIJA_UNI":
        tau = np.full((1, 26), TAU_UNI)
    elif modo_tau != "LIQUIDA":
        raise SystemExit("ABORTA: modo de tau desconocido " + modo_tau)
    for t in range(T):
        Pt = P0 - u * np.minimum(v * t, D0)[:, None]
        rx = Pt[:, 0] - px; ry = Pt[:, 1]
        dist = np.hypot(rx, ry)
        if lazo:
            choca = vivo & (dist < R_OBJ + R_ROB)
            t_muerte[choca] = t
            vivo = vivo & ~choca
        az = np.arctan2(rx, ry)
        th = 2.0 * np.arctan(R_OBJ / np.maximum(dist, R_OBJ + R_ROB))
        dth = np.zeros(n) if th_prev is None else np.maximum(th - th_prev, 0.0)
        th_prev = th
        f_ang = th / TH_COL
        f_vel = dth / (dth + K_LC4)
        d_der = 0.5 * (1.0 + np.sin(az)); d_izq = 1.0 - d_der
        rasgo = f_vel[:, None] * ctx["m_lc4"][None, :] + f_ang[:, None] * ctx["m_ang"][None, :]
        ojo = d_der[:, None] * ctx["m_der"][None, :] + d_izq[:, None] * ctx["m_izq"][None, :]
        x = rasgo * ojo + RUIDO * ctx["ruido"][:, t, :] * ctx["vpn"][None, :]
        pre = z @ Wn.T + x
        f = pre if nolin == "LINEAL" else np.tanh(pre)
        if modo_tau == "LIQUIDA":
            tt = 1.0 / (1.0 + np.exp(-(ctx["logit_het"][None, :] + x @ ctx["Vx"].T + z @ ctx["Vh"].T)))
        else:
            tt = tau
        z = (1.0 - tt) * z + tt * f
        if not np.all(np.isfinite(z)):
            raise SystemExit("ABORTA: estado no finito en t=" + str(t))
        c = z[:, ctx["GL"]] - z[:, ctx["GR"]]
        activo = np.abs(c) > EPS
        lat[activo & (lat < 0)] = t
        if lazo:
            paso = V_ROB * (np.sign(c) * activo if forzar is None else np.full(n, float(forzar)))
            px = px + np.where(vivo, paso, 0.0)
        else:
            D = D + np.where(t < t_arr, c, 0.0)
    if lazo:
        return {"ok": vivo, "lat": lat, "px": px, "t_muerte": t_muerte,
                "lado_ok": np.sign(px) == -np.sign(az0)}
    return {"ok": (np.abs(D) > 1e-9) & (np.sign(D) == -np.sign(az0)), "lat": lat, "D": D}


def medir(Wn, ctx, variantes):
    """Acierto, supervivencia y latencia de una red en cada variante pedida."""
    out = {}
    for (nl, mt) in variantes:
        a = simular(Wn, nl, mt, False, ctx)
        s = simular(Wn, nl, mt, True, ctx)
        lat = s["lat"][s["lat"] >= 0]
        out[nl + "+" + mt] = {"acierto": float(a["ok"].mean()), "supervivencia": float(s["ok"].mean()),
                              "lado_ok_cerrado": float(s["lado_ok"].mean()),
                              "latencia_mediana": float(np.median(lat)) if lat.size else -1.0,
                              "_ok_a": a["ok"], "_ok_s": s["ok"]}
    return out


def mcnemar(a, b):
    """McNemar exacto a dos colas sobre dos vectores booleanos pareados. Devuelve (n01, n10, p)."""
    n10 = int(np.sum(a & ~b)); n01 = int(np.sum(~a & b)); m = n10 + n01
    if m == 0:
        return n01, n10, 1.0
    k = min(n10, n01)
    p = 2.0 * sum(math.comb(m, i) for i in range(k + 1)) / (2.0 ** m)
    return n01, n10, min(1.0, p)


def p_emp(w, nulos):
    """p empirico a una cola: (1 + #{nulo >= W}) / (K + 1). Los empates cuentan contra W."""
    nulos = np.asarray(nulos)
    return (1.0 + float(np.sum(nulos >= w - 1e-12))) / (len(nulos) + 1.0)


def shuffle_lado(mod, M, edges, lado, k):
    """Shuffle de grado exacto dentro de cada hemisferio, con pesos permutados dentro de cada lado."""
    MS = np.zeros_like(M)
    guard = {}
    cruz = [(i, j) for (i, j) in edges if lado[i] != lado[j]]
    for (i, j) in cruz:
        MS[j, i] = M[j, i]
    for nombre, s0, p0 in (("left", SL_SEED_IZQ, SL_SEED_IZQ), ("right", SL_SEED_DER, SL_SEED_DER)):
        E = [(i, j) for (i, j) in edges if lado[i] == nombre and lado[j] == nombre]
        E_sh, n_ok = mod.ms_shuffle(E, mod.SHUFFLE_SEED0 + s0 + k, 30 * len(E))
        di0, do0 = mod.deg_io(E); di1, do1 = mod.deg_io(E_sh)
        g = {"aristas": len(E), "swaps_efectivos": int(n_ok),
             "grado_mal": int(np.sum(di0 != di1) + np.sum(do0 != do1)),
             "unicas": len(set(E_sh)), "autolazos": sum(1 for (i, j) in E_sh if i == j),
             "fuera_de_lado": sum(1 for (i, j) in E_sh if lado[i] != nombre or lado[j] != nombre)}
        if g["grado_mal"] or g["unicas"] != len(E) or g["autolazos"] or g["fuera_de_lado"] or n_ok == 0:
            raise SystemExit("ABORTA: shuffle por lado invalido k=" + str(k) + " " + nombre + " " + json.dumps(g))
        pesos = np.array([M[j, i] for (i, j) in E], dtype=np.float64)
        perm = np.random.default_rng(mod.PERM_SEED0 + p0 + k).permutation(len(pesos))
        for q, (i, j) in enumerate(E_sh):
            MS[j, i] = pesos[perm[q]]
        guard[nombre] = g
    guard["cruzadas_fijas"] = len(cruz)
    return MS, guard


def resumen(m):
    """Saca los vectores por ensayo para el JSON."""
    return {k: {kk: vv for kk, vv in d.items() if not kk.startswith("_")} for k, d in m.items()}


def main():
    """Corre todos los brazos y controles, aplica las reglas pre-registradas y escribe la evidencia."""
    ap = argparse.ArgumentParser(description="Brazo S en la funcion propia del motivo: looming -> escape")
    ap.add_argument("--motivo", required=True)
    ap.add_argument("--lados", required=True)
    ap.add_argument("--brazo-s", required=True)
    ap.add_argument("--k", type=int, default=200)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--solo-controles", action="store_true")
    a = ap.parse_args()
    T0 = time.time()
    os.makedirs(a.out_dir, exist_ok=True)

    meta = {"python": platform.python_version(), "numpy": np.__version__, "maquina": platform.platform(),
            "md5_script": md5(os.path.abspath(__file__)), "md5_motivo": md5(a.motivo),
            "md5_lados": md5(a.lados), "md5_brazo_s": md5(a.brazo_s), "k": a.k,
            "fecha_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "fisica": {"R_obj": R_OBJ, "r_robot": R_ROB, "d0": D0, "v_robot": V_ROB, "T": T, "eps": EPS,
                       "ruido": RUIDO, "k_lc4": K_LC4, "az_grados": AZ_GRADOS, "velocidades": VELOCIDADES,
                       "reps": REPS, "semilla_ruido": SEMILLA_RUIDO}}
    try:
        for line in open("/proc/cpuinfo"):
            if line.startswith("model name"):
                meta["cpu"] = line.split(":", 1)[1].strip(); break
    except OSError:
        pass
    print("# " + json.dumps(meta, sort_keys=True))
    if meta["md5_motivo"] != MD5_MOTIVO or meta["md5_brazo_s"] != MD5_BRAZO_S:
        print("ABORTA: md5 del motivo o de brazo_s_recurrente.py distinto del pin")
        return 2
    lados = json.load(open(a.lados))
    if lados.get("fallas"):
        print("ABORTA: lados con fallas " + str(lados["fallas"]))
        return 2
    mod = cargar_brazo_s(a.brazo_s)
    M, edges, mot = mod.cargar_motivo(a.motivo)
    if [f["root_id"] for f in lados["neuronas"]] != [int(x) for x in mot["orden_root_ids"]]:
        print("ABORTA: el orden de lados26.json no es el del motivo")
        return 2
    ctx = contexto(lados)
    lado = ctx["lado"]
    cruz = sum(1 for (i, j) in edges if lado[i] != lado[j])
    print("LATERALIDAD aristas=" + str(len(edges)) + " ipsilaterales=" + str(len(edges) - cruz) + " cruzadas=" + str(cruz)
          + " GF_izq=" + str(ctx["GL"]) + " GF_der=" + str(ctx["GR"])
          + " visuales_izq=" + str(int(ctx["m_izq"].sum())) + " visuales_der=" + str(int(ctx["m_der"].sum())))
    print("ENSAYOS n=" + str(ctx["n"]) + " (az0 x v x reps) T=" + str(T))

    Cp = np.zeros((26, 26))
    for i in range(26):
        if ctx["vpn"][i]:
            g = ctx["GL"] if lado[i] == "left" else ctx["GR"]
            Cp[g, i] = 1.0 / (ctx["m_izq"].sum() if lado[i] == "left" else ctx["m_der"].sum())
    C0 = np.zeros((26, 26))
    ctrl = {"C+": medir(Cp, ctx, [PRINCIPAL]), "C0": medir(C0, ctx, [PRINCIPAL])}
    clave = PRINCIPAL[0] + "+" + PRINCIPAL[1]
    for nom in ("C+", "C0"):
        r = ctrl[nom][clave]
        print("CONTROL " + nom + " acierto=" + format(r["acierto"], ".4f") + " supervivencia="
              + format(r["supervivencia"], ".4f") + " lado_ok_cerrado=" + format(r["lado_ok_cerrado"], ".4f")
              + " latencia_mediana=" + str(r["latencia_mediana"]))
    ref = {}
    for nom, signo in (("SIEMPRE_IZQ", -1.0), ("SIEMPRE_DER", 1.0)):
        s = simular(C0, "TANH", "FIJA_HET", True, ctx, forzar=signo)
        ref[nom] = float(s["ok"].mean())
        print("REFERENCIA politica=" + nom + " (ciega al lado, desde t=0) supervivencia=" + format(ref[nom], ".4f"))
    valido = (ctrl["C+"][clave]["acierto"] >= 0.95 and ctrl["C+"][clave]["supervivencia"] >= 0.90
              and ctrl["C0"][clave]["acierto"] == 0.0 and ctrl["C0"][clave]["supervivencia"] <= 0.05)
    print("CHEQUEO INSTRUMENTO " + ("VALIDO" if valido else "INVALIDO"))
    res = {"meta": meta, "lateralidad": {"aristas": len(edges), "cruzadas": cruz},
           "controles": {k: resumen(v) for k, v in ctrl.items()}, "referencias": ref, "instrumento_valido": valido}
    if not valido:
        json.dump(res, open(os.path.join(a.out_dir, "resultados.json"), "w"), indent=1)
        print("EXIT_RUN=3")
        return 3
    if a.solo_controles:
        json.dump(res, open(os.path.join(a.out_dir, "resultados_controles.json"), "w"), indent=1)
        print("SOLO_CONTROLES: el sujeto no se corrio")
        print("EXIT_RUN=0")
        return 0

    Wn, r0 = mod.a_rho(M)
    if abs(mod.radio(Wn) - 0.9) > 1e-9:
        print("ABORTA: radio de W"); return 2
    mW = medir(Wn, ctx, VARIANTES)
    for k_, r in mW.items():
        print("SUJETO W variante=" + k_ + " acierto=" + format(r["acierto"], ".4f") + " supervivencia="
              + format(r["supervivencia"], ".4f") + " lado_ok_cerrado=" + format(r["lado_ok_cerrado"], ".4f")
              + " latencia_mediana=" + str(r["latencia_mediana"]))
    nulos = {"S": [], "SL": [], "B": []}
    guardas = {"S": [], "SL": []}
    for k in range(a.k):
        MS, gs = mod.matriz_shuffle(M, edges, k)
        WS, _ = mod.a_rho(MS)
        if float(np.max(np.abs(WS - Wn))) < 1e-9:
            print("ABORTA: S == W en k=" + str(k)); return 2
        gs["cruzadas"] = int(sum(1 for i in range(26) for j in range(26) if MS[j, i] != 0 and lado[i] != lado[j]))
        ML, gl = shuffle_lado(mod, M, edges, lado, k)
        WL, _ = mod.a_rho(ML)
        if float(np.max(np.abs(WL - Wn))) < 1e-9:
            print("ABORTA: SL == W en k=" + str(k)); return 2
        WB, _ = mod.a_rho(np.random.default_rng(B_SEED0 + k).normal(0.0, 1.0, size=(26, 26)))
        for nom, Wx in (("S", WS), ("SL", WL), ("B", WB)):
            if abs(mod.radio(Wx) - 0.9) > 1e-6:
                print("ABORTA: radio de " + nom + " k=" + str(k)); return 2
            nulos[nom].append(resumen(medir(Wx, ctx, VARIANTES)))
        guardas["S"].append(gs); guardas["SL"].append(gl)
        if k % 20 == 0 or k == a.k - 1:
            p = nulos["S"][-1][clave]; q = nulos["SL"][-1][clave]
            print("progreso k=" + str(k) + " S_acierto=" + format(p["acierto"], ".4f") + " S_superv="
                  + format(p["supervivencia"], ".4f") + " SL_acierto=" + format(q["acierto"], ".4f")
                  + " SL_superv=" + format(q["supervivencia"], ".4f") + " cruzadas_S=" + str(gs["cruzadas"])
                  + " seg=" + format(time.time() - T0, ".0f"), flush=True)

    def serie(nom, var, met):
        return np.array([d[var][met] for d in nulos[nom]])

    for nom in ("S", "SL", "B"):
        for (nl, mt) in VARIANTES:
            var = nl + "+" + mt
            a_, s_ = serie(nom, var, "acierto"), serie(nom, var, "supervivencia")
            print("NULO " + nom + " variante=" + var + " acierto_media=" + format(a_.mean(), ".4f")
                  + " acierto_p95=" + format(np.percentile(a_, 95), ".4f") + " superv_media=" + format(s_.mean(), ".4f")
                  + " superv_p95=" + format(np.percentile(s_, 95), ".4f"))
    w = mW[clave]
    con = {}
    for etiqueta, nom, met in (("P1", "S", "acierto"), ("P2", "SL", "acierto"), ("P3_S", "S", "supervivencia"),
                               ("P3_SL", "SL", "supervivencia"), ("P4_acierto", "B", "acierto"),
                               ("P4_superv", "B", "supervivencia")):
        nl = serie(nom, clave, met)
        p = p_emp(w[met], nl)
        con[etiqueta] = {"W": w[met], "nulo": nom, "metrica": met, "nulo_media": float(nl.mean()),
                         "nulo_max": float(nl.max()), "n_nulo_ge_W": int(np.sum(nl >= w[met] - 1e-12)),
                         "p_emp": p, "W_gana": bool(p < 0.05)}
        print("CONTRASTE " + etiqueta + " W_" + met + "=" + format(w[met], ".4f") + " " + nom + "_media="
              + format(nl.mean(), ".4f") + " " + nom + "_max=" + format(nl.max(), ".4f") + " n_" + nom + ">=W="
              + str(con[etiqueta]["n_nulo_ge_W"]) + "/" + str(len(nl)) + " p_emp=" + format(p, ".4f") + " -> "
              + ("W GANA" if p < 0.05 else "W NO GANA"))
    for etiqueta, va, vb in (("P5_liquida", "TANH+LIQUIDA", "TANH+FIJA_HET"), ("P5_uniforme", "TANH+FIJA_UNI", "TANH+FIJA_HET"),
                             ("P6_lineal", "LINEAL+FIJA_HET", "TANH+FIJA_HET")):
        for met, k_ in (("supervivencia", "_ok_s"), ("acierto", "_ok_a")):
            n01, n10, p = mcnemar(mW[va][k_], mW[vb][k_])
            dif = mW[va][met] - mW[vb][met]
            sig = "IGUAL" if p >= 0.05 else ("MEJOR" if dif > 0 else "PEOR")
            con[etiqueta + "_" + met] = {"A": va, "B": vb, "A_val": mW[va][met], "B_val": mW[vb][met],
                                         "solo_A_ok": n10, "solo_B_ok": n01, "p_mcnemar": p, "A_vs_B": sig}
            print("CONTRASTE " + etiqueta + "_" + met + " " + va + "=" + format(mW[va][met], ".4f") + " " + vb + "="
                  + format(mW[vb][met], ".4f") + " solo_A=" + str(n10) + " solo_B=" + str(n01)
                  + " p_mcnemar=" + format(p, ".4f") + " -> " + va + " " + sig)
    v_fun = "LA MOSCA PAGA EN SU FUNCION: W GANA A S" if con["P3_S"]["W_gana"] else "W NO GANA A S EN SU FUNCION"
    v_det = ("PAGA EL CABLEADO FINO, NO SOLO LA LATERALIDAD" if con["P3_SL"]["W_gana"]
             else "EL CABLEADO FINO NO SE DISTINGUE DE SU SHUFFLE POR LADO")
    t_ = con["P5_liquida_supervivencia"]["A_vs_B"]
    v_tau = {"IGUAL": "LA LIQUIDA NO SE DISTINGUE DE LA FIJA", "MEJOR": "LA LIQUIDA PAGA EN LA FUNCION",
             "PEOR": "LA LIQUIDA EMPEORA EN LA FUNCION"}[t_]
    l_ = con["P6_lineal_supervivencia"]["A_vs_B"]
    v_lin = {"IGUAL": "EL LINEAL NO SE DISTINGUE DE TANH", "MEJOR": "EL LINEAL GANA A TANH",
             "PEOR": "TANH GANA AL LINEAL"}[l_]
    print("VEREDICTO_FUNCION=" + v_fun)
    print("VEREDICTO_DETALLE=" + v_det)
    print("VEREDICTO_TAU=" + v_tau)
    print("VEREDICTO_LINEAL=" + v_lin)
    res.update({"W": resumen(mW), "nulos": nulos, "guardas": guardas, "contrastes": con,
                "veredictos": {"funcion": v_fun, "detalle": v_det, "tau": v_tau, "lineal": v_lin},
                "minutos": (time.time() - T0) / 60.0})
    json.dump(res, open(os.path.join(a.out_dir, "resultados.json"), "w"))
    print("escrito resultados.json md5=" + md5(os.path.join(a.out_dir, "resultados.json")))
    print("minutos=" + format(res["minutos"], ".2f"))
    print("EXIT_RUN=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
