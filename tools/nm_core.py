"""Cierra los 3 NO MEDIDO que quedaban y que SI necesitan GPU.

Abraham senalo que hay una segunda cuenta de Kaggle. Tenia razon en el principio:
la cuota nunca fue el limite (27,9 h y 29,3 h libres). El limite es de SESIONES
SIMULTANEAS, 2 por cuenta, y los 4 shards del A/B ya ocupaban las 4 disponibles.
Ahora las 4 estan libres, asi que se usan para lo que la corrida anterior dejo
declarado como NO MEDIDO y que si requiere GPU:

  1. LOS DOS BRAZOS que v1 tiene de verdad (tauC y tauR) con las CUATRO
     modalidades y 6 pares de RDI, no uno solo con 3.
     Nota de honestidad: el 2x2 COMPLETO es imposible en v1, porque v1 no tiene
     modo de peso real (WEIGHT_REAL no existe ahi). Lo que se cierra es el 2x1
     que v1 SI puede: la ventaja de tau, con la rejilla completa.
  2. CRUCE ARPACK contra iteracion de potencia sobre cada grafo. v1 no tiene
     ARPACK, asi que el cruce se hace con el instrumento de v2 sobre la matriz
     que produce CADA motor: si los dos rho coinciden con ARPACK, la convergencia
     deja de depender del flag que reporta el propio motor.
  3. rankdata en GPU: la version parcheada contra cupy.argsort/unique, para
     cerrar 'el fix no se probo en GPU'.
"""
import importlib.util, sys, os, time, json, gc
import numpy as np

SHARD = int(os.environ.get("NM_SHARD", "0"))
TOTAL = int(os.environ.get("NM_TOTAL", "4"))
N_NULLS = int(os.environ.get("NM_NULLS", "12"))
STEPS = int(os.environ.get("NM_STEPS", "150"))
BASE = os.environ.get("NM_BASE", "/workspace")
OUTD = os.environ.get("NM_OUT", os.path.join(BASE, "nm_out"))

T0 = time.time()
def lg(s): print("[%7.1fs] %s" % (time.time() - T0, s), flush=True)

import hashlib
def md5f(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def load(p, nm):
    s = importlib.util.spec_from_file_location(nm, p); m = importlib.util.module_from_spec(s)
    sys.modules[nm] = m; s.loader.exec_module(m); return m

P1 = os.path.join(BASE, "motor.py"); P2 = os.path.join(BASE, "motor_v2.py")
lg("motor.py md5=%s   motor_v2.py md5=%s" % (md5f(P1), md5f(P2)))
V1 = load(P1, "mv1"); V2 = load(P2, "mv2")

HAS_GPU = False; GPU_NAME = ""; WHY = ""
try:
    import cupy as cp
    import cupyx.scipy.sparse as csp
    GPU_NAME = cp.cuda.runtime.getDeviceProperties(0)["name"].decode(); HAS_GPU = True
except Exception as e:
    WHY = "%s: %s" % (type(e).__name__, str(e)[:110])
lg("GPU: %s" % (GPU_NAME if HAS_GPU else "NO -> " + WHY))

def propagate_gpu(W, tau, stim_idx, n_steps=200, t_on=10, t_off=60, amp=1.0,
                  activation=None, save_at=None, clip=2.0):
    n = W.shape[0]
    WT = csp.csr_matrix(W.T.tocsr())
    tg = cp.asarray(tau); om = cp.asarray(1.0 - tau)
    z = cp.zeros(n, dtype=cp.complex128); s = cp.zeros(n, dtype=cp.complex128)
    s[cp.asarray(stim_idx)] = amp
    keep = set(save_at) if save_at is not None else set()
    out = {}
    for t in range(n_steps):
        drive = WT.dot(z)
        if t_on <= t <= t_off: drive = drive + s
        a = cp.tanh(drive)
        bad = ~cp.isfinite(a)
        if bool(cp.any(bad)):
            mi = cp.abs(drive); safe = cp.where(mi > 1e-300, mi, cp.complex128(1.0))
            a = cp.where(bad, clip * (drive / safe), a)
        mg = cp.abs(a); ov = mg > clip
        if bool(cp.any(ov)):
            a = cp.where(ov, clip * a / cp.where(mg > 0, mg, cp.complex128(1.0)), a)
        z = om * z + tg * a
        if t in keep: out[t] = cp.asnumpy(z)
    zc = cp.asnumpy(z); m = np.abs(zc)
    return out, zc, {"max_abs": float(np.max(m)),
                     "frac_at_clip": float(np.mean(m >= clip * 0.999)),
                     "frac_dead": float(np.mean(m <= 1e-12))}

D = V2.load_connectome(BASE, download=True)
pre, post, w = D["pre"], D["post"], D["w"]
n = int(D["n"]); bin_of = D["bin_of"]; n_bins = len(D["bin_names"])
STIM = D["stim"]                       # LAS CUATRO, no 3
SNAP = sorted(set([max(1, STEPS//3), max(2, (2*STEPS)//3), STEPS-1]))
PARES = len(STIM) * (len(STIM) - 1) // 2
lg("grafo n=%d e=%d md5=%s" % (n, pre.shape[0], D["md5"]["parquet"]))
lg("modalidades=%s (%d pares de RDI)  pasos=%d  snapshots=%s"
   % (D["mod_names"], PARES, STEPS, SNAP))

tau_c = V2.make_tau(n)
tau_c = tau_c[0] if isinstance(tau_c, tuple) else tau_c
tau_r = np.asarray(tau_c.real, dtype=np.complex128)   # el brazo de control de v1
lg("tau compleja: Re=%.6f |Im| medio=%.6f   tau REAL: |Im|=%.1e"
   % (tau_c.real.mean(), np.abs(tau_c.imag).mean(), float(np.abs(tau_r.imag).max())))

BACKEND = "CPU"; PROP = None
if HAS_GPU:
    lg("")
    lg("########## VERIFICACION GPU contra la CPU de CADA motor ##########")
    Wv = V2.normalize_spectral(V2.build_weights(pre, post, w, n, mode=V2.WEIGHT_COMPLEX, phase_jitter=0.0)[0])[0]
    sv = STIM[0][:200]
    zg = propagate_gpu(Wv, tau_c, sv, n_steps=20)[1]
    ok = True
    for nm, M in [("mv1", V1), ("mv2", V2)]:
        zc = M.propagate(Wv, tau_c, sv, n_steps=20)[1]
        rel = float(np.max(np.abs(zg - zc))) / (float(np.max(np.abs(zc))) or 1.0)
        ok &= rel < 1e-9
        lg("  %s desvio relativo = %.3e  %s" % (nm, rel, "OK" if rel < 1e-9 else "FALLA"))
    if ok:
        BACKEND = "GPU"; PROP = propagate_gpu
        lg("  BACKEND EFECTIVO: GPU")
    else:
        lg("  BACKEND EFECTIVO: CPU_FALLBACK, declarado")
    del Wv; gc.collect()

os.makedirs(OUTD, exist_ok=True)
OUT = {"shard": SHARD, "total": TOTAL, "backend": BACKEND, "gpu": GPU_NAME,
       "md5_motor": md5f(P1), "md5_motor_v2": md5f(P2),
       "meta": {"n": n, "e": int(pre.shape[0]), "md5": D["md5"],
                "mods": D["mod_names"], "pares_rdi": PARES,
                "steps": STEPS, "snap": SNAP, "n_nulls": N_NULLS},
       "grafos": {}}
def guardar():
    json.dump(OUT, open(os.path.join(OUTD, "nm_%d.json" % SHARD), "w"), default=str, indent=1)

def medir(nm, M, p_post, etiqueta):
    """Los DOS brazos de tau que v1 tiene, con las 4 modalidades. Y el cruce ARPACK."""
    if nm == "mv1":
        Wc = M.build_complex_weights(pre, p_post, w, n, phase_jitter=0.0)[0]
        o = M.normalize_spectral(Wc); Wn = o[0]; rho = float(o[1]); conv = bool(o[2])
    else:
        Wc = M.build_weights(pre, p_post, w, n, mode=M.WEIGHT_COMPLEX, phase_jitter=0.0)[0]
        o = M.normalize_spectral(Wc); Wn = o[0]
        rho = float(o[1].get("rho_pre")); conv = bool(o[1].get("pre_converged", True))
    # NO MEDIDO 3: el cruce ARPACK sobre la matriz de ESTE motor, con el
    # instrumento de v2. v1 no tiene ARPACK, asi que su convergencia venia
    # solo de su propio flag. Aca se mide con un segundo instrumento.
    rho_ark = float("nan"); brecha = float("nan")
    try:
        rho_ark = float(V2.spectral_radius_arpack(Wn)[0])
        brecha = abs(rho_ark - 0.99) / 0.99
    except Exception as e:
        rho_ark = float("nan")
    res = {"rho_pre": rho, "convergio_flag": conv, "rho_post_arpack": rho_ark,
           "brecha_rel_post": brecha, "nnz": int(Wn.nnz)}
    for tag, tau in (("tauC", tau_c), ("tauR", tau_r)):
        pr = {s: [] for s in SNAP}
        f = PROP if PROP is not None else M.propagate
        for mi in STIM:
            out = f(Wn, tau, mi, n_steps=STEPS, save_at=SNAP)[0]
            for s in SNAP:
                pr[s].append(M.region_profile(out[s], bin_of, n_bins))
        for s in SNAP:
            v, nv, nx = M.rdi(pr[s])
            res["rdi_%s_t%d" % (tag, s)] = float(v)
            res["pares_%s_t%d" % (tag, s)] = int(nv)
    for s in SNAP:
        res["ventaja_tau_t%d" % s] = res["rdi_tauC_t%d" % s] - res["rdi_tauR_t%d" % s]
    del Wn, Wc; gc.collect()
    lg("  %-24s rho=%10.4f conv=%-5s arpack_post=%.9f  %s"
       % (etiqueta, rho, conv, rho_ark,
          " ".join("vent_t%d=%+.6f" % (s, res["ventaja_tau_t%d" % s]) for s in SNAP)))
    return res

idxs = list(range(SHARD, N_NULLS, TOTAL))
lg("")
lg("########## LOS DOS BRAZOS DE TAU, 4 modalidades, %d pares ##########" % PARES)
lg("  este shard: REAL=%s  nulls=%s" % (SHARD == 0, idxs))
if SHARD == 0:
    OUT["grafos"]["REAL"] = {"v1": medir("mv1", V1, post, "v1 REAL"),
                             "v2": medir("mv2", V2, post, "v2 REAL")}
    guardar()
for gi in idxs:
    p = V2.make_null("cp", pre, post, n, bin_of, seed=1000 + 7 * gi)
    OUT["grafos"]["null_%d" % gi] = {"v1": medir("mv1", V1, p, "v1 null g%d" % gi),
                                     "v2": medir("mv2", V2, p, "v2 null g%d" % gi),
                                     "_seed": 1000 + 7 * gi}
    del p; gc.collect()
    guardar()

# ---- NO MEDIDO 3: rankdata en GPU ----
if SHARD == 0 and HAS_GPU:
    lg("")
    lg("########## rankdata: la version parcheada contra cupy ##########")
    def rankdata_gpu(v):
        a = cp.asarray(v, dtype=cp.float64); nn = a.shape[0]
        order = cp.argsort(a, kind="stable"); sa = a[order]
        uniq, i0, cnt = cp.unique(sa, return_index=True, return_counts=True)
        rs = cp.repeat(i0 + (cnt - 1) / 2.0 + 1.0, cnt)
        out = cp.empty(nn, dtype=cp.float64); out[order] = rs
        return cp.asnumpy(out)
    rk = []
    for lbl, arr in [("40 (el uso real)", np.random.default_rng(1).normal(0, 1, 40)),
                     ("5k sin empates", np.random.default_rng(2).normal(0, 1, 5000)),
                     ("200k sin empates", np.random.default_rng(3).normal(0, 1, 200000)),
                     ("200k con 100 valores", np.random.default_rng(4).integers(0, 100, 200000).astype(np.float64))]:
        rc = np.asarray(V2.rankdata(arr), dtype=np.float64)
        rg = rankdata_gpu(arr)
        d = float(np.max(np.abs(rc - rg)))
        def cr(f, reps=3):
            ts = []
            for _ in range(reps):
                t = time.perf_counter(); f(); ts.append(time.perf_counter() - t)
            return min(ts)
        tc = cr(lambda: V2.rankdata(arr)); tg = cr(lambda: rankdata_gpu(arr))
        rk.append({"caso": lbl, "n": int(arr.shape[0]), "unicos": int(np.unique(arr).size),
                   "desvio_cpu_gpu": d, "t_cpu": tc, "t_gpu": tg})
        lg("  %-22s n=%-8d unicos=%-8d |cpu-gpu|=%.3e   cpu %.6f s  gpu %.6f s  (%.2fx)"
           % (lbl, arr.shape[0], np.unique(arr).size, d, tc, tg, tc / max(tg, 1e-12)))
    lg("")
    lg("  el caso NO ESPECIFICADO por el motor: entrada con NaN")
    vn = np.array([3.0, np.nan, 1.0, np.nan, 2.0])
    try:
        a = np.asarray(V2.rankdata(vn)); lg("    cpu -> %s" % a)
    except Exception as e:
        lg("    cpu -> EXCEPCION %s" % type(e).__name__)
    try:
        b = rankdata_gpu(vn); lg("    gpu -> %s" % b)
    except Exception as e:
        lg("    gpu -> EXCEPCION %s" % type(e).__name__)
    lg("    NOTA: el motor no especifica el comportamiento con NaN. Se reporta lo")
    lg("          que hace, no se declara correcto.")
    OUT["rankdata_gpu"] = rk
    guardar()

guardar()
lg("")
lg("FIN shard=%d backend=%s" % (SHARD, BACKEND))
print("FINNM", flush=True)
