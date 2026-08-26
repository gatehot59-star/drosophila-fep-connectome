"""CIERRE EN KAGGLE de los 6 NO MEDIDO que quedaban de la respuesta 106.

Que cierra cada modo:

  MODE=ab      los 39 NULLS del A/B v1-vs-v2 (antes: UN solo null).
               Sharded: cada kernel corre un subconjunto intercalado.
  MODE=extras  1. DISTRIBUCION de la semilla de fase -> intervalo, no un punto
               2. BARRIDO de phase_jitter entre 0 y 0.1 -> no solo los extremos
               3. ESCALA hasta n=138.639, el conectoma REAL completo
               4. RSS REAL por proceso hijo, no tracemalloc
  MODE=smoke   corrida chica sobre grafo sintetico, para probar el arnes antes
               de gastar GPU ajena.

DECISION DE DISENO, declarada porque cambia lo que el A/B mide:
  Los dos motores usan el MISMO propagate de GPU, inyectado en runtime y
  verificado contra la propagate de CADA motor antes de usarse. Es legitimo
  porque la identidad de propagate ya esta medida a escala real con desvio
  0.000000e+00 (respuesta 106, condicion A). Lo que este A/B mide entonces es
  build_weights + normalize_spectral + metricas, que es donde vive la unica
  diferencia conocida (la realizacion del jitter de fase).
  Si la verificacion GPU-vs-CPU falla, cae a CPU y LO DECLARA.

W-01: cada comparacion imprime los dos valores crudos.
"""
import importlib.util, sys, os, time, json, gc, resource, multiprocessing as mp
import numpy as np

MODE = os.environ.get("AB_MODE", "smoke")
SHARD_ID = int(os.environ.get("AB_SHARD", "0"))
SHARD_TOTAL = int(os.environ.get("AB_SHARD_TOTAL", "1"))
N_NULLS = int(os.environ.get("AB_NULLS", "39"))
STEPS = int(os.environ.get("AB_STEPS", "150"))
BASE = os.environ.get("AB_BASE", "/workspace")
OUTDIR = os.environ.get("AB_OUT", os.path.join(BASE, "ab39_out"))

T0 = time.time()
def lg(s):
    print("[%7.1fs] %s" % (time.time() - T0, s), flush=True)

def load(p, nm):
    s = importlib.util.spec_from_file_location(nm, p); m = importlib.util.module_from_spec(s)
    sys.modules[nm] = m; s.loader.exec_module(m); return m

import hashlib
def md5f(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

P1 = os.path.join(BASE, "motor.py")
P2 = os.path.join(BASE, "motor_v2.py")
lg("motor.py     md5=%s  %d B" % (md5f(P1), os.path.getsize(P1)))
lg("motor_v2.py  md5=%s  %d B" % (md5f(P2), os.path.getsize(P2)))
V1 = load(P1, "mv1")
V2 = load(P2, "mv2")
lg("los dos motores importados como modulos")

# ---------------- GPU ----------------
HAS_GPU = False
GPU_NAME = ""
GPU_WHY = ""
try:
    import cupy as cp
    import cupyx.scipy.sparse as csp
    d = cp.cuda.Device(0)
    GPU_NAME = cp.cuda.runtime.getDeviceProperties(0)["name"].decode()
    HAS_GPU = True
except Exception as e:
    GPU_WHY = "%s: %s" % (type(e).__name__, str(e)[:120])
lg("GPU: %s" % (GPU_NAME if HAS_GPU else ("NO -> " + GPU_WHY)))

def propagate_gpu(W, tau, stim_idx, n_steps=200, t_on=10, t_off=60, amp=1.0,
                  activation=None, save_at=None, clip=2.0):
    """Misma especificacion que propagate() del motor, con SpMV y activacion en GPU.

    La activacion se reimplementa en cupy porque mover el vector a CPU en cada
    paso anularia la ganancia: el costo del bucle es ancho de banda.
    Acepta y descarta `activation` para tener la MISMA firma que la de CPU.
    """
    n = W.shape[0]
    WT = csp.csr_matrix(W.T.tocsr())
    tau_g = cp.asarray(tau)
    one_minus = cp.asarray(1.0 - tau)
    z = cp.zeros(n, dtype=cp.complex128)
    s = cp.zeros(n, dtype=cp.complex128)
    s[cp.asarray(stim_idx)] = amp
    keep = set(save_at) if save_at is not None else set()
    out = {}
    for t in range(n_steps):
        drive = WT.dot(z)
        if t_on <= t <= t_off:
            drive = drive + s
        a = cp.tanh(drive)
        bad = ~cp.isfinite(a)
        if bool(cp.any(bad)):
            mag_in = cp.abs(drive)
            safe = cp.where(mag_in > 1e-300, mag_in, cp.complex128(1.0))
            a = cp.where(bad, clip * (drive / safe), a)
        mag = cp.abs(a)
        over = mag > clip
        if bool(cp.any(over)):
            a = cp.where(over, clip * a / cp.where(mag > 0, mag, cp.complex128(1.0)), a)
        z = one_minus * z + tau_g * a
        if t in keep:
            out[t] = cp.asnumpy(z)
    zc = cp.asnumpy(z)
    mg = np.abs(zc)
    return out, zc, {"max_abs": float(np.max(mg)),
                     "frac_at_clip": float(np.mean(mg >= clip * 0.999)),
                     "frac_dead": float(np.mean(mg <= 1e-12))}

# ---------------- el dato ----------------
if MODE == "smoke":
    D = V2.synthetic_graph(n=3000, e=45000, n_mods=3, stim_size=200, seed=11)
    STEPS = 30
else:
    D = V2.load_connectome(BASE, download=True)
pre, post, w = D["pre"], D["post"], D["w"]
n = int(D["n"]); bin_of = D["bin_of"]; n_bins = len(D["bin_names"])
STIM = D["stim"][:3]
MODS = D["mod_names"][:3]
SNAP = sorted(set([max(1, STEPS // 3), max(2, (2 * STEPS) // 3), STEPS - 1]))
lg("grafo: n=%d  e=%d  md5=%s" % (n, pre.shape[0], D["md5"]["parquet"]))
lg("modalidades=%s  pasos=%d  snapshots=%s" % (MODS, STEPS, SNAP))

tau = V2.make_tau(n)
tau = tau[0] if isinstance(tau, tuple) else tau

# ---------------- verificacion GPU contra la CPU de CADA motor ----------------
BACKEND = "CPU"
PROP = {"mv1": V1.propagate, "mv2": V2.propagate}
if HAS_GPU:
    lg("")
    lg("########## VERIFICACION GPU contra la CPU de CADA motor ##########")
    Wv = V2.build_weights(pre, post, w, n, mode=V2.WEIGHT_COMPLEX, phase_jitter=0.0)[0]
    Wv = V2.normalize_spectral(Wv)[0]
    sv = STIM[0][:min(200, STIM[0].shape[0])]
    ok_all = True
    zg = propagate_gpu(Wv, tau, sv, n_steps=20)[1]
    for nm, M in [("mv1", V1), ("mv2", V2)]:
        zc = M.propagate(Wv, tau, sv, n_steps=20)[1]
        den = float(np.max(np.abs(zc))) or 1.0
        rel = float(np.max(np.abs(zg - zc))) / den
        ok = rel < 1e-9
        ok_all &= ok
        lg("  %s  desvio relativo maximo = %.3e   %s" % (nm, rel, "OK" if ok else "FALLA"))
    if ok_all:
        BACKEND = "GPU"
        PROP = {"mv1": propagate_gpu, "mv2": propagate_gpu}
        lg("  BACKEND EFECTIVO: GPU (misma propagate inyectada en los dos)")
    else:
        lg("  BACKEND EFECTIVO: CPU_FALLBACK -> la verificacion no paso, se declara")
    del Wv
    gc.collect()
lg("backend=%s" % BACKEND)

def medir(nm, M, p_post, jitter, seed_fase, etiqueta):
    """Cadena completa de UN motor: pesos -> normalizacion -> dinamica -> rdi."""
    t = time.time()
    if nm == "mv1":
        r = M.build_complex_weights(pre, p_post, w, n, phase_jitter=jitter, seed=seed_fase)
        o = M.normalize_spectral(r[0]); Wn = o[0]; rho = float(o[1])
    else:
        r = M.build_weights(pre, p_post, w, n, mode=M.WEIGHT_COMPLEX,
                            phase_jitter=jitter, seed=seed_fase)
        o = M.normalize_spectral(r[0]); Wn = o[0]
        rho = float(o[1].get("rho_pre") if isinstance(o[1], dict) else o[1])
    tw = time.time() - t
    profs = {s: [] for s in SNAP}
    t = time.time()
    for mi in STIM:
        out = PROP[nm](Wn, tau, mi, n_steps=STEPS, save_at=SNAP)[0]
        for s in SNAP:
            profs[s].append(M.region_profile(out[s], bin_of, n_bins))
    tp = time.time() - t
    res = {"rho_pre": rho, "nnz": int(Wn.nnz), "t_pesos_s": tw, "t_dinamica_s": tp}
    for s in SNAP:
        v, nv, nx = M.rdi(profs[s])
        res["rdi_t%d" % s] = float(v)
    del Wn
    gc.collect()
    lg("  %-30s rho=%12.4f  %s  (%.1f s)"
       % (etiqueta, rho, " ".join("t%d=%.9f" % (s, res["rdi_t%d" % s]) for s in SNAP), tw + tp))
    return res

os.makedirs(OUTDIR, exist_ok=True)
OUT = {"mode": MODE, "shard": SHARD_ID, "shard_total": SHARD_TOTAL,
       "backend": BACKEND, "gpu": GPU_NAME, "gpu_why": GPU_WHY,
       "md5_motor": md5f(P1), "md5_motor_v2": md5f(P2),
       "meta": {"n": n, "e": int(pre.shape[0]), "md5": D["md5"], "mods": MODS,
                "steps": STEPS, "snap": SNAP, "n_nulls": N_NULLS}}
def guardar():
    with open(os.path.join(OUTDIR, "%s_%d.json" % (MODE, SHARD_ID)), "w") as f:
        json.dump(OUT, f, default=str, indent=1)

# ==================== MODO ab / smoke : LOS 39 NULLS ====================
if MODE in ("ab", "smoke"):
    idxs = list(range(SHARD_ID, N_NULLS, SHARD_TOTAL))
    lg("")
    lg("########## A/B v1 vs v2 sobre %d NULLS (jitter=0) ##########" % len(idxs))
    lg("  indices globales de este shard: %s" % idxs)
    OUT["null_indices"] = idxs
    OUT["pares"] = {}
    if SHARD_ID == 0:
        lg("  -- el grafo REAL, como referencia --")
        a1 = medir("mv1", V1, post, 0.0, 42, "v1 REAL j=0")
        a2 = medir("mv2", V2, post, 0.0, 42, "v2 REAL j=0")
        OUT["real"] = {"v1": a1, "v2": a2}
        guardar()
    peor = 0.0
    for gi in idxs:
        seed = 1000 + 7 * gi
        p = V2.make_null("cp", pre, post, n, bin_of, seed=seed)
        r1 = medir("mv1", V1, p, 0.0, 42, "v1 NULL g%d" % gi)
        r2 = medir("mv2", V2, p, 0.0, 42, "v2 NULL g%d" % gi)
        d = {"d_rho": abs(r1["rho_pre"] - r2["rho_pre"])}
        for s in SNAP:
            d["d_rdi_t%d" % s] = abs(r1["rdi_t%d" % s] - r2["rdi_t%d" % s])
        peor = max([peor, d["d_rho"]] + [d["d_rdi_t%d" % s] for s in SNAP])
        OUT["pares"][str(gi)] = {"v1": r1, "v2": r2, "delta": d, "_seed_null": seed}
        lg("     null g%-3d  d_rho=%.3e  %s   -> peor acumulado %.3e"
           % (gi, d["d_rho"], " ".join("d_t%d=%.3e" % (s, d["d_rdi_t%d" % s]) for s in SNAP), peor))
        del p
        gc.collect()
        guardar()
    OUT["peor_desvio"] = peor
    OUT["identicos"] = bool(peor < 1e-9)
    lg("")
    lg("  VEREDICTO shard %d: peor desvio sobre %d nulls = %.6e  -> %s"
       % (SHARD_ID, len(idxs), peor,
          "IDENTICOS" if peor < 1e-9 else "DIFIEREN, revisar"))
    guardar()

# ==================== MODO extras ====================
if MODE == "extras":
    # ---- 1. DISTRIBUCION de la semilla de fase: intervalo, no un punto ----
    SEEDS = [42, 101, 202, 303, 404, 505, 606, 707, 808, 909, 1111, 1313]
    lg("")
    lg("########## 1. DISTRIBUCION de la semilla de fase (jitter=0.1, %d realizaciones) ##########" % len(SEEDS))
    lg("  Antes: 0,0472%% era UN punto. Aca sale la dispersion de esa cantidad.")
    dist = []
    for sd in SEEDS:
        r = medir("mv2", V2, post, 0.1, sd, "REAL j=0.1 seed=%d" % sd)
        r["_seed_fase"] = sd
        dist.append(r)
        OUT["dist_semilla"] = dist
        guardar()
    import statistics as st
    lg("")
    lg("  %-14s %-14s %-12s %-12s %-12s %s" % ("cantidad", "media", "sd", "min", "max", "rango/media %"))
    for k in ["rho_pre"] + ["rdi_t%d" % s for s in SNAP]:
        v = [x[k] for x in dist]
        rng = max(v) - min(v)
        lg("  %-14s %-14.6f %-12.6f %-12.6f %-12.6f %.4f%%"
           % (k, st.mean(v), st.stdev(v), min(v), max(v), 100.0 * rng / max(abs(st.mean(v)), 1e-30)))
    OUT["dist_resumen"] = {k: {"mean": st.mean([x[k] for x in dist]),
                              "sd": st.stdev([x[k] for x in dist]),
                              "min": min([x[k] for x in dist]),
                              "max": max([x[k] for x in dist])}
                           for k in ["rho_pre"] + ["rdi_t%d" % s for s in SNAP]}
    guardar()

    # ---- 2. BARRIDO de phase_jitter ----
    JIT = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.20]
    lg("")
    lg("########## 2. BARRIDO de phase_jitter (antes: solo los extremos) ##########")
    sweep = []
    for j in JIT:
        r = medir("mv2", V2, post, j, 42, "REAL jitter=%.2f" % j)
        r["_jitter"] = j
        sweep.append(r)
        OUT["barrido_jitter"] = sweep
        guardar()
    lg("")
    lg("  %-9s %-14s %s" % ("jitter", "rho_pre", " ".join("rdi_t%d" % s for s in SNAP)))
    for r in sweep:
        lg("  %-9.2f %-14.6f %s" % (r["_jitter"], r["rho_pre"],
                                    " ".join("%.6f" % r["rdi_t%d" % s] for s in SNAP)))
    guardar()

    # ---- 3. ESCALA hasta el n REAL ----
    lg("")
    lg("########## 3. ESCALA hasta n=%d, el conectoma REAL completo ##########" % n)
    lg("  Antes el barrido llegaba a n=64.000. Aca se sub-muestrea el grafo REAL.")
    def crono(f, reps=2):
        ts = []
        for _ in range(reps):
            gc.collect(); t = time.perf_counter(); f(); ts.append(time.perf_counter() - t)
        return min(ts)
    esc = []
    for frac in [0.125, 0.25, 0.5, 1.0]:
        nn = int(n * frac)
        keep = (pre < nn) & (post < nn)
        pr, po, ww = pre[keep], post[keep], w[keep]
        bo = bin_of[:nn]
        Wq = V2.build_weights(pr, po, ww, nn, mode=V2.WEIGHT_COMPLEX)[0]
        Wq = V2.normalize_spectral(Wq)[0]
        tq = V2.make_tau(nn); tq = tq[0] if isinstance(tq, tuple) else tq
        sq = np.arange(0, min(400, max(4, nn // 8)), dtype=np.int64)
        b1 = crono(lambda: V1.build_complex_weights(pr, po, ww, nn))
        b2 = crono(lambda: V2.build_weights(pr, po, ww, nn, mode=V2.WEIGHT_COMPLEX))
        s1 = crono(lambda: V1.normalize_spectral(Wq.copy()))
        s2 = crono(lambda: V2.normalize_spectral(Wq.copy()))
        p1 = crono(lambda: V1.propagate(Wq, tq, sq, n_steps=30))
        p2 = crono(lambda: V2.propagate(Wq, tq, sq, n_steps=30))
        row = {"n": nn, "e": int(pr.shape[0]), "pesos_v1": b1, "pesos_v2": b2,
               "norm_v1": s1, "norm_v2": s2, "prop_v1": p1, "prop_v2": p2}
        esc.append(row)
        lg("  n=%-8d e=%-9d | pesos %.4f/%.4f =%.2f | norm %.4f/%.4f =%.2f | prop %.4f/%.4f =%.2f"
           % (nn, pr.shape[0], b1, b2, b2/b1, s1, s2, s2/s1, p1, p2, p2/p1))
        OUT["escala"] = esc
        guardar()
        del Wq, pr, po, ww
        gc.collect()

    # ---- 4. RSS REAL, en proceso hijo ----
    lg("")
    lg("########## 4. RSS REAL por proceso hijo (antes: solo tracemalloc) ##########")
    lg("  tracemalloc ve allocaciones de Python. Aca se mide ru_maxrss del HIJO,")
    lg("  que incluye los buffers de BLAS/ARPACK y el heap de numpy.")
    def hijo(q, motor_path, nombre, etapa, nn, e_):
        import importlib.util as iu, sys as sy, numpy as npx, resource as rs, os as osx
        sp = iu.spec_from_file_location("m", motor_path); mm = iu.module_from_spec(sp)
        sy.modules["m"] = mm; sp.loader.exec_module(mm)
        rng = npx.random.default_rng(7)
        per = max(1, nn // 10)
        bo = npx.minimum(npx.arange(nn) // per, 9).astype(npx.int64)
        pr = rng.integers(0, nn, e_).astype(npx.int64)
        sm = rng.random(e_) < 0.70
        po = npx.where(sm, bo[pr]*per + rng.integers(0, per, e_), rng.integers(0, nn, e_)).astype(npx.int64)
        k = pr != po; pr, po = pr[k], po[k]
        inh = rng.random(nn) < 0.30
        mg = rng.lognormal(0.0, 0.6, pr.shape[0])
        ww = npx.where(inh[pr], -mg, mg)
        base = rs.getrusage(rs.RUSAGE_SELF).ru_maxrss
        if etapa == "pesos":
            if nombre == "v1": mm.build_complex_weights(pr, po, ww, nn)
            else: mm.build_weights(pr, po, ww, nn, mode=mm.WEIGHT_COMPLEX)
        else:
            if nombre == "v1":
                W0 = mm.build_complex_weights(pr, po, ww, nn)[0]
                base = rs.getrusage(rs.RUSAGE_SELF).ru_maxrss
                mm.normalize_spectral(W0)
            else:
                W0 = mm.build_weights(pr, po, ww, nn, mode=mm.WEIGHT_COMPLEX)[0]
                base = rs.getrusage(rs.RUSAGE_SELF).ru_maxrss
                mm.normalize_spectral(W0)
        pk = rs.getrusage(rs.RUSAGE_SELF).ru_maxrss
        q.put({"base_kb": base, "peak_kb": pk, "delta_mb": (pk - base) / 1024.0,
               "total_mb": pk / 1024.0})
    rss = []
    for nn, e_ in [(64000, 960000), (138639, 3000000)]:
        for etapa in ["pesos", "norm"]:
            fila = {"n": nn, "e": e_, "etapa": etapa}
            for nombre, path in [("v1", P1), ("v2", P2)]:
                q = mp.Queue()
                pr_ = mp.Process(target=hijo, args=(q, path, nombre, etapa, nn, e_))
                pr_.start(); pr_.join()
                try: r = q.get_nowait()
                except Exception: r = {"total_mb": float("nan"), "delta_mb": float("nan")}
                fila[nombre] = r
            rss.append(fila)
            lg("  n=%-8d %-6s | v1 pico %8.1f MB (delta %7.1f) | v2 pico %8.1f MB (delta %7.1f) | v2/v1 pico %.3f"
               % (nn, etapa, fila["v1"]["total_mb"], fila["v1"]["delta_mb"],
                  fila["v2"]["total_mb"], fila["v2"]["delta_mb"],
                  fila["v2"]["total_mb"] / max(fila["v1"]["total_mb"], 1e-9)))
            OUT["rss"] = rss
            guardar()

guardar()
lg("")
lg("FIN modo=%s shard=%d  backend=%s  salida=%s" % (MODE, SHARD_ID, BACKEND, OUTDIR))
print("FINAB39", flush=True)
