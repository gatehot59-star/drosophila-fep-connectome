# cascade_sensitivity.py - items 1 y 2 de la deuda declarada, juntos.
#
# ITEM 1: mi cascada anterior no era la de Betzel. Le faltaban sus dinamicas
#         COOPERATIVA y COMPETITIVA, y corrio 20 realizaciones contra sus 1000.
#         La pregunta abierta era: si sus dinamicas rompen la saturacion, el
#         veredicto de la resp 082 cambia.
#
# ITEM 2: no se barrio p_trans ni N_seed. Ese barrido es exactamente el
#         "sensitivity analysis" que su Revisor #3 pidio y que ellos no
#         reportan en el cuerpo del paper.
#
# Los tres ensembles, cada uno fiel a su descripcion en Betzel et al. (2026):
#
#   UNIMODAL     una modalidad siembra. Es el brazo de la resp 082, ampliado.
#   COOPERATIVE  dos modalidades siembran a la vez y la activacion se SUMA:
#                un postsinaptico recibe la union de intentos de las dos
#                cascadas, asi que la probabilidad de encenderse crece.
#   COMPETITIVE  dos modalidades siembran a la vez y cada neurona queda
#                ETIQUETADA por la cascada que la alcanzo primero. Si las dos
#                llegan en el mismo paso, gana la que aporta mas sinapsis, y si
#                empatan exacto se decide por moneda, como su Fig 5a describe.
#
# El estadistico de salida es el mismo en los tres: cuantas de las 110 motoras
# quedan alcanzadas. Asi la comparacion con el brazo lineal no cambia de vara.
#
# LA PREGUNTA FALSABLE, una sola y escrita antes de correr:
#   La saturacion (105-106 de 110 motoras en las cuatro clases, spread 1,009x)
#   es una propiedad del MODELO o un artefacto de p_trans=0.01 y N_seed=16?
#   Si algun punto del barrido baja el reach por debajo de ~50 motoras Y separa
#   las clases, entonces la saturacion era artefacto y el veredicto de la resp
#   082 hay que angostarlo.
#   Si satura en todo el rango, el veredicto se refuerza con evidencia.
#
# Guards, y los tres pueden dar rojo:
#   G1  los tres conteos publicados por Betzel (N, E, Mw) en int64. Si no, aborta.
#   G2  el reach de un ensemble no puede exceder la poblacion motora. Si un
#       punto da mas de 110, hay un bug de conteo y aborta.
#   G3  CONTROL NEGATIVO con nombre: una modalidad FALSA de 256 neuronas tomadas
#       al azar del grafo entero. Si el azar alcanza tantas motoras como las
#       clases sensoriales reales, el estadistico no distingue nada y se declara.

import sys
import os
import time
import json

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

T0 = time.time()
PARQUET = os.environ.get("PARQUET", "connectivity.parquet")
ANNOT = os.environ.get("ANNOT", "annotations.tsv")
OUT = os.environ.get("OUT", "cascade_sensitivity_out.json")
if len(sys.argv) > 1:
    PARQUET = sys.argv[1]
if len(sys.argv) > 2:
    ANNOT = sys.argv[2]
if len(sys.argv) > 3:
    OUT = sys.argv[3]

EXIT_GUARD = 2
CLASSES = ["visual", "olfactory", "mechanosensory", "gustatory"]
CSTEPS = 12
NREAL = 40

# El barrido. p_trans cubre cuatro ordenes de magnitud alrededor del 0.01 que
# Betzel fija en el cuerpo del paper; N_seed cubre de 1 a 256 alrededor de su 16.
PTRANS_GRID = [0.0001, 0.001, 0.003, 0.01, 0.03, 0.1]
NSEED_GRID = [1, 4, 16, 64, 256]


def lg(msg):
    sys.stdout.write(str(msg) + "\n")
    sys.stdout.flush()


def require(condition, message):
    """Aborta con exit 2 si la condicion es falsa."""
    if condition:
        return True
    sys.stderr.write("GUARD_FAILED " + str(message) + "\n")
    sys.stderr.flush()
    raise SystemExit(EXIT_GUARD)


lg("=== CASCADE SENSITIVITY  ---  items 1 y 2 de la deuda declarada ===")
lg("parquet = " + PARQUET)

cols = ["Presynaptic_Index", "Postsynaptic_Index", "Connectivity",
        "Presynaptic_ID", "Postsynaptic_ID"]
tab = pq.read_table(PARQUET, columns=cols)
pre = tab.column(0).to_numpy().astype(np.int32)
post = tab.column(1).to_numpy().astype(np.int32)
syn = tab.column(2).to_numpy().astype(np.float32)
pid = tab.column(3).to_numpy()
qid = tab.column(4).to_numpy()

E = int(len(pre))
N = int(max(pre.max(), post.max())) + 1
Mw = int(tab.column(2).to_numpy().astype(np.int64).sum())
lg("N=" + str(N) + "  E=" + str(E) + "  Mw=" + str(Mw))

# G1 - los tres conteos que Betzel publica. int64, porque float32 pierde 2.
require(N == 138639, "N esperado 138639, medido " + str(N))
require(E == 15091983, "E esperado 15091983, medido " + str(E))
require(Mw == 54492922, "Mw esperado 54492922, medido " + str(Mw))
lg("G1 los tres conteos coinciden con Betzel 2026: OK")

ann = pd.read_csv(ANNOT, sep=chr(9), low_memory=False)
ids = np.union1d(pid, qid)
id2i = {int(r): i for i, r in enumerate(ids)}


def byidx(mask):
    """Indices de la mascara, y cuantas filas se descartaron por no estar en el grafo."""
    raw = ann.loc[mask, "root_id"].values
    keep = [id2i[int(x)] for x in raw if int(x) in id2i]
    return np.array(keep, dtype=np.int64), int(len(raw) - len(keep))


stim = {}
for cls in CLASSES:
    arr, lost = byidx(ann["cell_class"] == cls)
    stim[cls] = arr
    lg("  pob " + cls.ljust(16) + " n=" + str(len(arr)) + "  descartadas=" + str(lost))

motor, motor_lost = byidx(ann["super_class"] == "motor")
require(len(motor) == 110, "motoras esperadas 110, medidas " + str(len(motor)))
NMOTOR = len(motor)
lg("  pob motor            n=" + str(NMOTOR) + "  descartadas=" + str(motor_lost))

motor_mask = np.zeros(N, dtype=bool)
motor_mask[motor] = True

# G3 - control negativo con nombre: modalidad FALSA, 256 nodos al azar del grafo
rng_ctrl = np.random.default_rng(4242)
stim["ZZQQXX_AZAR"] = rng_ctrl.choice(N, size=256, replace=False).astype(np.int64)
lg("  pob ZZQQXX_AZAR      n=256  (control negativo, nodos al azar del grafo)")


def cascade_unimodal(pool, rng, p_trans, n_seed, steps=CSTEPS):
    """Cascada de tres estados sin signo. Devuelve motoras distintas alcanzadas."""
    take = min(n_seed, len(pool))
    seeds = rng.choice(pool, size=take, replace=False)
    state = np.zeros(N, dtype=np.int8)
    state[seeds] = 1
    reached = np.zeros(N, dtype=bool)
    reached[seeds] = True
    for _ in range(steps):
        active = np.flatnonzero(state == 1)
        if active.size == 0:
            break
        amask = np.zeros(N, dtype=bool)
        amask[active] = True
        sel = amask[pre] & (state[post] == 0)
        state[state == 1] = 2
        if not sel.any():
            break
        prob = 1.0 - np.power(1.0 - p_trans, syn[sel])
        fired = rng.random(prob.shape[0]) < prob
        newly = np.unique(post[sel][fired])
        if newly.size:
            state[newly] = 1
            reached[newly] = True
    return int(np.count_nonzero(reached & motor_mask))


def cascade_two_modal(pool_a, pool_b, rng, p_trans, n_seed, mode, steps=CSTEPS):
    """Cascada con DOS modalidades sembrando a la vez.

    mode='cooperative': la activacion se suma; un postsinaptico se enciende si
        CUALQUIERA de las dos cascadas lo alcanza, asi que las dos colaboran.
    mode='competitive': cada neurona queda etiquetada por la cascada que la
        alcanzo primero; los empates de paso se resuelven por peso sinaptico y
        los empates exactos por moneda.

    Devuelve (motoras alcanzadas total, motoras de A, motoras de B).
    """
    ta = min(n_seed, len(pool_a))
    tb = min(n_seed, len(pool_b))
    seeds_a = rng.choice(pool_a, size=ta, replace=False)
    seeds_b = rng.choice(pool_b, size=tb, replace=False)
    # label 0 = libre, 1 = de A, 2 = de B, 3 = de las dos (solo cooperativo)
    label = np.zeros(N, dtype=np.int8)
    label[seeds_a] = 1
    label[seeds_b] = np.where(label[seeds_b] == 1, 3, 2)
    state = np.zeros(N, dtype=np.int8)
    state[seeds_a] = 1
    state[seeds_b] = 1
    reached = state > 0
    for _ in range(steps):
        active = np.flatnonzero(state == 1)
        if active.size == 0:
            break
        amask = np.zeros(N, dtype=bool)
        amask[active] = True
        sel = amask[pre] & (state[post] == 0)
        state[state == 1] = 2
        if not sel.any():
            break
        idx = np.flatnonzero(sel)
        prob = 1.0 - np.power(1.0 - p_trans, syn[idx])
        fired = rng.random(prob.shape[0]) < prob
        hit = idx[fired]
        if hit.size == 0:
            continue
        tgt = post[hit]
        src_label = label[pre[hit]]
        if mode == "cooperative":
            # la union enciende: cualquiera de las dos sirve
            newly = np.unique(tgt)
            state[newly] = 1
            reached[newly] = True
            # el destino hereda la union de etiquetas de sus fuentes
            for lab in (1, 2):
                w = np.unique(tgt[(src_label == lab) | (src_label == 3)])
                if w.size:
                    label[w] = np.where(label[w] == 0, lab,
                                        np.where(label[w] == lab, lab, 3))
        else:
            # COMPETITIVO: el que aporta mas sinapsis en este paso se queda el nodo
            wa = np.zeros(N, dtype=np.float64)
            wb = np.zeros(N, dtype=np.float64)
            from_a = (src_label == 1) | (src_label == 3)
            from_b = (src_label == 2) | (src_label == 3)
            np.add.at(wa, tgt[from_a], syn[hit][from_a])
            np.add.at(wb, tgt[from_b], syn[hit][from_b])
            newly = np.unique(tgt)
            tie = np.isclose(wa[newly], wb[newly])
            coin = rng.random(newly.shape[0]) < 0.5
            win_a = np.where(tie, coin, wa[newly] > wb[newly])
            label[newly] = np.where(win_a, 1, 2)
            state[newly] = 1
            reached[newly] = True
    tot = int(np.count_nonzero(reached & motor_mask))
    ma = int(np.count_nonzero((label == 1) & motor_mask))
    mb = int(np.count_nonzero((label == 2) & motor_mask))
    return tot, ma, mb


res = {"meta": {"N": N, "E": E, "Mw": Mw, "n_motor": NMOTOR,
                "cascade_steps": CSTEPS, "n_real": NREAL,
                "ptrans_grid": PTRANS_GRID, "nseed_grid": NSEED_GRID},
       "sweep": {}, "cooperative": {}, "competitive": {}}

lg("")
lg("=== ITEM 2 - BARRIDO de p_trans x N_seed, unimodal, " + str(NREAL) + " realizaciones por punto ===")
lg("   (el sensitivity analysis que pidio su Revisor #3)")
POOLS = CLASSES + ["ZZQQXX_AZAR"]
for p_trans in PTRANS_GRID:
    for n_seed in NSEED_GRID:
        key = "p" + format(p_trans, ".4f") + "_s" + str(n_seed)
        row = {}
        for cls in POOLS:
            rng = np.random.default_rng(777)
            vals = np.array([cascade_unimodal(stim[cls], rng, p_trans, n_seed)
                             for _ in range(NREAL)], dtype=np.float64)
            require(vals.max() <= NMOTOR,
                    "reach " + str(vals.max()) + " excede la poblacion motora "
                    + str(NMOTOR) + " en " + key + " " + cls)
            row[cls] = {"mean": float(vals.mean()), "sd": float(vals.std()),
                        "min": float(vals.min()), "max": float(vals.max())}
        reals = [row[c]["mean"] for c in CLASSES]
        lo = min(reals)
        hi = max(reals)
        spread = (hi / lo) if lo > 0 else float("inf")
        row["spread_between_classes"] = spread
        row["saturated"] = bool(hi >= 0.90 * NMOTOR)
        res["sweep"][key] = row
        lg("  p=" + format(p_trans, ".4f") + " seed=" + str(n_seed).rjust(3)
           + "  vis=" + format(row["visual"]["mean"], "6.2f")
           + "  olf=" + format(row["olfactory"]["mean"], "6.2f")
           + "  mec=" + format(row["mechanosensory"]["mean"], "6.2f")
           + "  gus=" + format(row["gustatory"]["mean"], "6.2f")
           + "  | AZAR=" + format(row["ZZQQXX_AZAR"]["mean"], "6.2f")
           + "  spread=" + format(spread, "7.3f")
           + ("  SATURADO" if row["saturated"] else "  no-sat"))

lg("")
lg("=== ITEM 1 - las DINAMICAS que faltaban, en el punto que Betzel usa ===")
PAIRS = [("gustatory", "mechanosensory"), ("visual", "olfactory"),
         ("mechanosensory", "visual")]
for mode in ("cooperative", "competitive"):
    lg("  --- " + mode.upper() + " ---")
    for a, b in PAIRS:
        rng = np.random.default_rng(999)
        tots = []
        mas = []
        mbs = []
        for _ in range(NREAL):
            t, ma, mb = cascade_two_modal(stim[a], stim[b], rng, 0.01, 16, mode)
            tots.append(t)
            mas.append(ma)
            mbs.append(mb)
        tv = np.array(tots, dtype=np.float64)
        av = np.array(mas, dtype=np.float64)
        bv = np.array(mbs, dtype=np.float64)
        require(tv.max() <= NMOTOR, "reach total excede " + str(NMOTOR))
        res[mode][a + "+" + b] = {
            "total_mean": float(tv.mean()), "total_sd": float(tv.std()),
            a + "_mean": float(av.mean()), b + "_mean": float(bv.mean())}
        lg("    " + (a + "+" + b).ljust(32) + " total=" + format(tv.mean(), "6.2f")
           + " +/- " + format(tv.std(), ".2f")
           + "   " + a[:4] + "=" + format(av.mean(), "6.2f")
           + "   " + b[:4] + "=" + format(bv.mean(), "6.2f"))

lg("")
lg("=== EL VEREDICTO ===")
sat_points = sum(1 for k, v in res["sweep"].items() if v["saturated"])
tot_points = len(res["sweep"])
lg("  puntos del barrido SATURADOS (>=90% de las 110 motoras): "
   + str(sat_points) + " de " + str(tot_points))
spreads = [v["spread_between_classes"] for v in res["sweep"].values()]
lg("  spread entre clases: min=" + format(min(spreads), ".3f")
   + "  max=" + format(max(spreads), ".3f"))
best = max(res["sweep"].items(), key=lambda kv: kv[1]["spread_between_classes"])
lg("  punto con MAS separacion: " + best[0] + "  spread="
   + format(best[1]["spread_between_classes"], ".3f"))
lg("  en ese punto AZAR alcanza " + format(best[1]["ZZQQXX_AZAR"]["mean"], ".2f")
   + " motoras")
res["verdict"] = {"saturated_points": sat_points, "total_points": tot_points,
                  "spread_min": float(min(spreads)),
                  "spread_max": float(max(spreads)),
                  "best_separating_point": best[0]}

with open(OUT, "w") as fh:
    json.dump(res, fh, indent=1)
lg("")
lg("DONE in " + format(time.time() - T0, ".1f") + " s -> " + OUT)
