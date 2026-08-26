# ab_cascade_vs_linear.py - item 2 de la deuda declarada.
#
# Compara MIDIENDO el modelo de cascada de Betzel et al. (2026) contra el modelo
# lineal con signo del Paper 1, sobre EL MISMO grafo y con EL MISMO estadistico.
#
# Por que existe: las resp 080 y 081 compararon DESCRIPCIONES DE METODO, no
# corridas. Eso alcanza para citar; no alcanza para afirmar que los dos modelos
# llegan a conclusiones distintas. Este script lo mide.
#
# La pregunta falsable, una sola:
#   Los dos modelos ORDENAN igual el acceso motor de las cuatro clases sensoriales?
#   Si el orden coincide, el aporte del signo y del transitorio es MENOR de lo que
#   afirma el parrafo de posicionamiento, y el claim hay que angostarlo.
#   Si difiere, el claim queda sostenido por una MEDICION y no por dos abstracts.
#
# Los dos brazos, cada uno fiel a su fuente:
#   CASCADE  tres estados (inactivo/activo/refractario), probabilidad de
#            transmision por sinapsis, SIN signo, N_seed=16, p_trans=0.01,
#            como declara Betzel en su Fig 1 y su S2 Fig.
#   LINEAR   h <- (1-tau)*h + tau*tanh(W^T h + s), CON signo por neurona
#            presinaptica (Dale) y normalizacion por columna, como el Paper 1.
#
# Guards, y los tres pueden dar rojo:
#   G1  el grafo cargado tiene los conteos publicados (N, E, Mw). Si no, aborta.
#   G2  Dale exacta: 0 neuronas con salidas mixtas. Si no, aborta.
#   G3  CONTROL NEGATIVO: barajar el signo POR ARISTA debe romper G2. Si no lo
#       rompe, el guard no mide nada y el script aborta igual.
#
# Rutas por argumento o variable de entorno (A-05). Sin rutas absolutas fijas.

import sys
import os
import time
import json

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from scipy import sparse as sp
from scipy import stats as st

T0 = time.time()
PARQUET = os.environ.get("PARQUET", "connectivity.parquet")
ANNOT = os.environ.get("ANNOT", "annotations.tsv")
OUT = os.environ.get("OUT", "ab_models_out.json")
if len(sys.argv) > 1:
    PARQUET = sys.argv[1]
if len(sys.argv) > 2:
    ANNOT = sys.argv[2]
if len(sys.argv) > 3:
    OUT = sys.argv[3]

EXIT_GUARD = 2
CLASSES = ["visual", "olfactory", "mechanosensory", "gustatory"]


def lg(msg):
    sys.stdout.write(str(msg) + "\n")
    sys.stdout.flush()


def require(condition, message):
    """Aborta con exit 2 si la condicion es falsa. No imprime y sigue."""
    if condition:
        return True
    sys.stderr.write("GUARD_FAILED " + str(message) + "\n")
    sys.stderr.flush()
    raise SystemExit(EXIT_GUARD)


lg("=== AB CASCADE vs LINEAR  ---  item 2 de la deuda declarada ===")
lg("parquet = " + PARQUET)
lg("annot   = " + ANNOT)

cols = ["Presynaptic_Index", "Postsynaptic_Index", "Connectivity",
        "Excitatory", "Presynaptic_ID", "Postsynaptic_ID"]
tab = pq.read_table(PARQUET, columns=cols)
pre = tab.column(0).to_numpy().astype(np.int32)
post = tab.column(1).to_numpy().astype(np.int32)
conn = tab.column(2).to_numpy().astype(np.float32)
exc = tab.column(3).to_numpy().astype(np.int8)
pid = tab.column(4).to_numpy()
qid = tab.column(5).to_numpy()

E = int(len(pre))
N = int(max(pre.max(), post.max())) + 1
Mw = int(conn.sum())
lg("N=" + str(N) + "  E=" + str(E) + "  Mw=" + str(Mw))

# G1 - los tres conteos que Betzel et al. (2026) publican en su seccion de metodos
require(N == 138639, "N esperado 138639, medido " + str(N))
require(E == 15091983, "E esperado 15091983, medido " + str(E))
require(Mw == 54492922, "Mw esperado 54492922, medido " + str(Mw))
lg("G1 los tres conteos coinciden con Betzel 2026 y con el Paper 1: OK")

# G2 - ley de Dale sobre el grafo real
sign_edge = np.where(exc > 0, 1.0, -1.0).astype(np.float32)
pos_out = np.zeros(N, dtype=np.int64)
neg_out = np.zeros(N, dtype=np.int64)
np.add.at(pos_out, pre[sign_edge > 0], 1)
np.add.at(neg_out, pre[sign_edge < 0], 1)
mixed = int(np.count_nonzero((pos_out > 0) & (neg_out > 0)))
lg("G2 neuronas con salidas MIXTAS en el grafo real = " + str(mixed))
require(mixed == 0, "Dale roto en el grafo real: " + str(mixed) + " mixtas")

# G3 - control negativo del guard anterior
rng0 = np.random.default_rng(12345)
shuf = sign_edge.copy()
rng0.shuffle(shuf)
p2 = np.zeros(N, dtype=np.int64)
n2 = np.zeros(N, dtype=np.int64)
np.add.at(p2, pre[shuf > 0], 1)
np.add.at(n2, pre[shuf < 0], 1)
mixed_shuf = int(np.count_nonzero((p2 > 0) & (n2 > 0)))
lg("G3 CONTROL NEGATIVO, shuffle por arista -> mixtas = " + str(mixed_shuf))
require(mixed_shuf > 1000,
        "el guard de Dale NO puede dar rojo: el shuffle dio " + str(mixed_shuf))
lg("G3 el guard de Dale PUEDE dar rojo: OK")

# poblaciones, contando lo que se descarta (no en silencio)
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
lg("  pob motor            n=" + str(len(motor)) + "  descartadas=" + str(motor_lost))
require(len(motor) == 110, "motoras esperadas 110, medidas " + str(len(motor)))

motor_mask = np.zeros(N, dtype=bool)
motor_mask[motor] = True

# ------------------ BRAZO LINEAR: el modelo del Paper 1 ------------------
TAU = 0.119
NSTEPS = 200
TSTART = 10
TEND = 60

W = sp.csr_matrix((conn * sign_edge, (pre, post)), shape=(N, N), dtype=np.float32)
colsum = np.asarray(abs(W.tocsc()).sum(axis=0)).ravel()
colsum[colsum < 1e-8] = 1.0
Wn = W.tocsc().dot(sp.diags((0.99 / colsum).astype(np.float32)))
WT = Wn.tocsr().T.tocsr()


def run_linear(seed_idx):
    """Propagacion lineal con signo. Devuelve pico y suma post-estimulo en motoras."""
    h = np.zeros(N, dtype=np.float32)
    peak = 0.0
    post_sum = 0.0
    for step in range(NSTEPS):
        drive = WT.dot(h)
        if TSTART <= step <= TEND:
            drive[seed_idx] += 1.0
        h = (1.0 - TAU) * h + TAU * np.tanh(drive)
        np.clip(h, -2.0, 2.0, out=h)
        m = float(np.abs(h[motor_mask]).sum())
        if TSTART <= step <= TEND:
            peak = max(peak, m)
        if step > TEND:
            post_sum += m
    return peak, post_sum


# ------------------ BRAZO CASCADE: el modelo de Betzel ------------------
PTRANS = 0.01
NSEED = 16
CSTEPS = 12
NREAL = 20
syn = conn.astype(np.float32)


def run_cascade(pool, rng):
    """Cascada de tres estados sin signo. Devuelve motoras distintas alcanzadas."""
    take = min(NSEED, len(pool))
    seeds = rng.choice(pool, size=take, replace=False)
    state = np.zeros(N, dtype=np.int8)   # 0 inactivo, 1 activo, 2 refractario
    state[seeds] = 1
    reached = np.zeros(N, dtype=bool)
    reached[seeds] = True
    for _ in range(CSTEPS):
        active = np.flatnonzero(state == 1)
        if active.size == 0:
            break
        amask = np.zeros(N, dtype=bool)
        amask[active] = True
        sel = amask[pre] & (state[post] == 0)
        state[state == 1] = 2
        if not sel.any():
            break
        k = syn[sel]
        prob = 1.0 - np.power(1.0 - PTRANS, k)
        fired = rng.random(prob.shape[0]) < prob
        newly = np.unique(post[sel][fired])
        if newly.size:
            state[newly] = 1
            reached[newly] = True
    return int(np.count_nonzero(reached & motor_mask))


res = {"meta": {"N": N, "E": E, "Mw": Mw, "mixed_real": mixed,
                "mixed_shuffle_ctrl": mixed_shuf, "tau": TAU,
                "nsteps": NSTEPS, "p_trans": PTRANS, "n_seed": NSEED,
                "cascade_steps": CSTEPS, "cascade_realisations": NREAL},
       "linear": {}, "cascade": {}}

lg("")
lg("=== BRAZO LINEAR  (Paper 1: CON signo, CON transitorio) ===")
for cls in CLASSES:
    peak, post_sum = run_linear(stim[cls])
    res["linear"][cls] = {"peak_motor": peak, "post_motor": post_sum}
    lg("  " + cls.ljust(16) + " peak=" + format(peak, ".6f")
       + "  post_sum=" + format(post_sum, ".6f"))

lg("")
lg("=== BRAZO CASCADE  (Betzel: SIN signo, SIN transitorio) ===")
for cls in CLASSES:
    rng = np.random.default_rng(777)
    vals = np.array([run_cascade(stim[cls], rng) for _ in range(NREAL)],
                    dtype=np.float64)
    res["cascade"][cls] = {"mean_motor_reached": float(vals.mean()),
                           "sd": float(vals.std()),
                           "min": float(vals.min()),
                           "max": float(vals.max()), "n": NREAL}
    lg("  " + cls.ljust(16) + " motoras alcanzadas = "
       + format(vals.mean(), ".3f") + " +/- " + format(vals.std(), ".3f")
       + "  [" + str(int(vals.min())) + "," + str(int(vals.max())) + "]")

lg("")
lg("=== EL VEREDICTO: los dos modelos ordenan igual? ===")
lin_rank = sorted(CLASSES, key=lambda c: -res["linear"][c]["post_motor"])
cas_rank = sorted(CLASSES, key=lambda c: -res["cascade"][c]["mean_motor_reached"])
lg("  orden LINEAR  por post-estimulo : " + " > ".join(lin_rank))
lg("  orden CASCADE por motoras       : " + " > ".join(cas_rank))
lg("  ORDEN IDENTICO = " + str(lin_rank == cas_rank))

x = [res["linear"][c]["post_motor"] for c in CLASSES]
y = [res["cascade"][c]["mean_motor_reached"] for c in CLASSES]
rho = st.spearmanr(x, y)
lg("  spearman rho = " + format(float(rho.statistic), ".4f")
   + "   (n=4: el p NO es interpretable y no se usa)")

# el contraste que decide: peak vs post en el brazo lineal
peak_rank = sorted(CLASSES, key=lambda c: -res["linear"][c]["peak_motor"])
lg("  orden LINEAR por PICO           : " + " > ".join(peak_rank))
lg("  pico y post-estimulo coinciden  = " + str(peak_rank == lin_rank))

res["verdict"] = {"linear_rank_post": lin_rank,
                  "linear_rank_peak": peak_rank,
                  "cascade_rank": cas_rank,
                  "identical_post_vs_cascade": lin_rank == cas_rank,
                  "identical_peak_vs_post": peak_rank == lin_rank,
                  "spearman_rho": float(rho.statistic)}

with open(OUT, "w") as fh:
    json.dump(res, fh, indent=1)

lg("")
lg("DONE in " + format(time.time() - T0, ".1f") + " s -> " + OUT)
