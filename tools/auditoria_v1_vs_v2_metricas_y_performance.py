"""AUDITORIA v1 vs v2, paso 3: metricas, test global y PERFORMANCE.

Las metricas se evaluan sobre EXACTAMENTE los mismos vectores, para que la unica
variable sea el codigo. El cronometro usa min() de 3 corridas, no la media, porque
el minimo es la cota menos contaminada por el ruido del scheduler.

Corrido en brain-env el 2026-08-26. Salida verbatim en
docs/agents/evidencia/2026-08-26-105-auditoria-v1-vs-v2-evidencia-cruda.md
"""
import importlib.util, sys, numpy as np, time

def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    sys.modules[n] = m; s.loader.exec_module(m); return m
V1 = load("/workspace/motor.py", "mv1")
V2 = load("/workspace/motor_v2.py", "mv2")

rng = np.random.default_rng(20260826)
n, e = 4000, 60000
per = n // 10
bin_of = np.minimum(np.arange(n)//per, 9).astype(np.int64)
pre = rng.integers(0, n, e).astype(np.int64)
same = rng.random(e) < 0.70
post = np.where(same, bin_of[pre]*per + rng.integers(0, per, e), rng.integers(0, n, e)).astype(np.int64)
keep = pre != post; pre, post = pre[keep], post[keep]
is_inh = rng.random(n) < 0.30
mag = rng.lognormal(0.0, 0.6, pre.shape[0])
w = np.where(is_inh[pre], -mag, mag)

print("=" * 100)
print("PASO 3 \u00b7 metricas, test global y PERFORMANCE")
print("=" * 100)

W = V2.build_weights(pre, post, w, n, mode=V2.WEIGHT_COMPLEX)[0]
Wn = V2.normalize_spectral(W)[0]
tau = V2.make_tau(n)
tau = tau[0] if isinstance(tau, tuple) else tau
stim = np.arange(0, 400, dtype=np.int64)
z = V2.propagate(Wn, tau, stim, n_steps=60)[1]

print("\n[METRICAS] sobre EXACTAMENTE los mismos vectores")
p1 = V1.region_profile(z, bin_of, 10); p2 = V2.region_profile(z, bin_of, 10)
print("    region_profile   |dif| max = %.6e" % float(np.max(np.abs(p1-p2))))
q = V2.region_profile(np.roll(z, 7), bin_of, 10)
d1, d2 = V1.cosine_distance(p1, q), V2.cosine_distance(p1, q)
print("    cosine_distance  v1=%.12f  v2=%.12f  dif=%.3e" % (d1, d2, abs(d1-d2)))
prof = [p1, q, V2.region_profile(np.roll(z, 31), bin_of, 10)]
print("    rdi              v1=%s" % str(V1.rdi(prof)))
print("                     v2=%s" % str(V2.rdi(prof)))
print("    phase_coherence  v1=%.12f  v2=%.12f" % (V1.phase_coherence(z), V2.phase_coherence(z)))
v = np.array([3.0, 1.0, 1.0, 2.0, 5.0, 5.0, 5.0])
print("    rankdata empates v1=%s" % V1.rankdata(v))
print("                     v2=%s" % V2.rankdata(v))
print("\n    -- el caso que separaria a los dos: un vector MUERTO --")
dead = np.zeros(10, dtype=np.complex128)
for nm, M in [("v1", V1), ("v2", V2)]:
    try:  cd = M.cosine_distance(dead, p1)
    except Exception as ex: cd = "EXCEPCION %s" % type(ex).__name__
    try:  pc = M.phase_coherence(dead)
    except Exception as ex: pc = "EXCEPCION %s" % type(ex).__name__
    print("      %s  cosine(muerto,vivo)=%s   phase_coherence(muerto)=%s" % (nm, cd, pc))

print("\n[TEST GLOBAL] mismos datos de entrada")
names = ["m%d" % i for i in range(9)]
rt = np.random.default_rng(5)
real = {k: float(x) for k, x in zip(names, rt.normal(1.0, 0.2, 9))}
nulls = [{k: float(x) for k, x in zip(names, rt.normal(0.0, 0.2, 9))} for _ in range(9)]
g1 = V1.global_rank_test(real, nulls, names)
g2 = V2.global_rank_test(real, nulls, names)
print("    v1 claves: %s" % list(g1.keys()))
print("    v2 claves: %s" % list(g2.keys()))
def dig(g, ks):
    for k in ks:
        if k in g: return g[k]
    for vv in g.values():
        if isinstance(vv, dict):
            for k in ks:
                if k in vv: return vv[k]
    return None
for lbl, ks in [("p dos colas", ["p_two_sided","p_two","p"]), ("S_real", ["S_real"]),
                ("piso", ["floor","p_floor"]), ("piso alcanzable", ["p_floor_reachable"]),
                ("significativo", ["significant"])]:
    print("    %-16s v1=%-22s v2=%s" % (lbl, str(dig(g1, ks)), str(dig(g2, ks))))

print("\n[PERFORMANCE] mismo trabajo, min de 3 corridas")
def crono(f, reps=3):
    ts = []
    for _ in range(reps):
        t = time.time(); f(); ts.append(time.time() - t)
    return min(ts), sum(ts)/len(ts)
tareas = [
    ("build_weights   ", lambda: V1.build_complex_weights(pre, post, w, n),
                         lambda: V2.build_weights(pre, post, w, n, mode=V2.WEIGHT_COMPLEX)),
    ("normalize_spectral", lambda: V1.normalize_spectral(W.copy()),
                           lambda: V2.normalize_spectral(W.copy())),
    ("propagate 60 pasos", lambda: V1.propagate(Wn, tau, stim, n_steps=60),
                           lambda: V2.propagate(Wn, tau, stim, n_steps=60)),
    ("rankdata 5k       ", lambda: V1.rankdata(np.random.default_rng(1).normal(0,1,5000)),
                           lambda: V2.rankdata(np.random.default_rng(1).normal(0,1,5000))),
]
print("    %-20s %-12s %-12s %-10s" % ("tarea", "v1 min(s)", "v2 min(s)", "v2/v1"))
for nm, f1, f2 in tareas:
    m1, _ = crono(f1); m2, _ = crono(f2)
    print("    %-20s %-12.4f %-12.4f %-10.3f" % (nm, m1, m2, m2/m1 if m1 > 0 else float("nan")))

print("\n[LO QUE v2 AGREGA Y v1 NO PUEDE HACER] llamadas reales")
for nm, fn, args in [("validate_statistical_power(9)", "validate_statistical_power", (9,)),
                     ("validate_statistical_power(39)", "validate_statistical_power", (39,)),
                     ("p_floor_two_sided(9)", "p_floor_two_sided", (9,)),
                     ("p_floor_two_sided(39)", "p_floor_two_sided", (39,)),
                     ("nulls_needed_for(0.05)", "nulls_needed_for", (0.05,))]:
    a = getattr(V1, fn, None); b = getattr(V2, fn, None)
    ra = "NO EXISTE en v1" if a is None else str(a(*args))[:90]
    rb = "NO EXISTE en v2" if b is None else str(b(*args))[:90]
    print("    %-32s v1: %-18s v2: %s" % (nm, ra, rb))
