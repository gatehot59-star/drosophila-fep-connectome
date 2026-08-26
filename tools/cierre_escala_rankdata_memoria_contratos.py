"""Cierra los NO MEDIDO 2, 3, 5 y 6 de la respuesta 105:
  2. barrido de ESCALA del cronometro (la 105 uso un solo n=4000)
  3. DIAGNOSTICO del rankdata 4,17x, con una PREDICCION FALSABLE
  5. MEMORIA de las dos versiones
  6. el IndexError convertido en TABLA DE CONTRATOS

Se corre DESPUES del A/B real y con la maquina libre, para que el cronometro no
este contaminado por otro job. El cronometro usa min() de 3 corridas y
perf_counter, no la media: el minimo es la cota menos contaminada por el scheduler.

Corrido en brain-env el 2026-08-26. Salida verbatim en
docs/agents/evidencia/2026-08-26-106-cierre-no-medidos-evidencia-cruda.md
"""
import importlib.util, sys, time, gc, tracemalloc, re
import numpy as np

def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    sys.modules[n] = m; s.loader.exec_module(m); return m
V1 = load("/workspace/motor.py", "mv1")
V2 = load("/workspace/motor_v2.py", "mv2")

def grafo(n, e, seed=7):
    rng = np.random.default_rng(seed)
    per = max(1, n // 10)
    bin_of = np.minimum(np.arange(n) // per, 9).astype(np.int64)
    pre = rng.integers(0, n, e).astype(np.int64)
    same = rng.random(e) < 0.70
    post = np.where(same, bin_of[pre]*per + rng.integers(0, per, e), rng.integers(0, n, e)).astype(np.int64)
    k = pre != post
    pre, post = pre[k], post[k]
    inh = rng.random(n) < 0.30
    mag = rng.lognormal(0.0, 0.6, pre.shape[0])
    return pre, post, np.where(inh[pre], -mag, mag), bin_of

def crono(f, reps=3):
    ts = []
    for _ in range(reps):
        gc.collect(); t = time.perf_counter(); f(); ts.append(time.perf_counter() - t)
    return min(ts)

print("=" * 104)
print("RESOLUCION DE LOS NO MEDIDO  \u00b7  escala, rankdata, memoria y contratos")
print("=" * 104)

# ============ 2. BARRIDO DE ESCALA ============
print("\n[2] BARRIDO DE ESCALA (min de 3, perf_counter)")
print("    %-9s %-9s | %-11s %-11s %-7s | %-11s %-11s %-7s | %-11s %-11s %-7s"
      % ("n", "aristas", "pesos v1", "pesos v2", "v2/v1", "normal. v1", "normal. v2", "v2/v1",
         "propag. v1", "propag. v2", "v2/v1"))
ESC = []
for n, e in [(1000, 15000), (4000, 60000), (16000, 240000), (64000, 960000)]:
    pre, post, w, bin_of = grafo(n, e)
    W = V2.build_weights(pre, post, w, n, mode=V2.WEIGHT_COMPLEX)[0]
    Wn = V2.normalize_spectral(W)[0]
    tau = V2.make_tau(n); tau = tau[0] if isinstance(tau, tuple) else tau
    stim = np.arange(0, min(400, n // 4), dtype=np.int64)
    b1 = crono(lambda: V1.build_complex_weights(pre, post, w, n))
    b2 = crono(lambda: V2.build_weights(pre, post, w, n, mode=V2.WEIGHT_COMPLEX))
    s1 = crono(lambda: V1.normalize_spectral(W.copy()))
    s2 = crono(lambda: V2.normalize_spectral(W.copy()))
    p1 = crono(lambda: V1.propagate(Wn, tau, stim, n_steps=60))
    p2 = crono(lambda: V2.propagate(Wn, tau, stim, n_steps=60))
    print("    %-9d %-9d | %-11.4f %-11.4f %-7.2f | %-11.4f %-11.4f %-7.2f | %-11.4f %-11.4f %-7.2f"
          % (n, pre.shape[0], b1, b2, b2/b1, s1, s2, s2/s1, p1, p2, p2/p1))
    ESC.append((n, b2/b1, s2/s1, p2/p1))
print("\n    tendencia del cociente v2/v1 al crecer n:")
for lbl, i in [("pesos", 1), ("normalizacion", 2), ("propagate", 3)]:
    print("      %-14s %s" % (lbl, "  ".join("n=%d:%.2f" % (r[0], r[i]) for r in ESC)))

# ============ 3. DIAGNOSTICO DEL rankdata ============
print("\n[3] DIAGNOSTICO del rankdata de v2")
print("    La v2 se documenta 'vectorizado', pero tiene un loop de Python sobre los")
print("    valores UNICOS con una asignacion de slice de numpy por iteracion:")
print("        for u, c in zip(uniq, counts): ranks_sorted[start:start+c] = avg")
print("    Prediccion falsable: si el costo es el loop sobre unicos, entonces con POCOS")
print("    unicos (muchos empates) v2 tiene que GANAR, y con TODOS unicos tiene que PERDER.")
print()
def rankdata_full(v):
    """Referencia SIN loop: np.unique con return_index + np.repeat.

    Es lo que 'vectorizado' deberia costar. Se incluye para que el diagnostico no
    sea 'v2 es lento' sino 'v2 es lento POR ESTO, y sin eso costaria ESTO'.
    """
    a = np.asarray(v, dtype=np.float64)
    n = a.shape[0]
    order = np.argsort(a, kind="stable")
    sa = a[order]
    uniq, idx_start, counts = np.unique(sa, return_index=True, return_counts=True)
    avg = idx_start + (counts - 1) / 2.0 + 1.0
    ranks_sorted = np.repeat(avg, counts)
    out = np.empty(n, dtype=np.float64)
    out[order] = ranks_sorted
    return out

print("    %-28s %-8s %-11s %-11s %-9s %-11s %s" % ("caso", "unicos", "v1 (s)", "v2 (s)", "v2/v1", "sin-loop", "v2/sin-loop"))
for lbl, arr in [
    ("5k todos unicos", np.random.default_rng(1).normal(0, 1, 5000)),
    ("5k con 10 valores", np.random.default_rng(2).integers(0, 10, 5000).astype(np.float64)),
    ("5k con 2 valores", np.random.default_rng(3).integers(0, 2, 5000).astype(np.float64)),
    ("50k todos unicos", np.random.default_rng(4).normal(0, 1, 50000)),
    ("50k con 100 valores", np.random.default_rng(5).integers(0, 100, 50000).astype(np.float64)),
]:
    u = int(np.unique(arr).size)
    t1 = crono(lambda: V1.rankdata(arr))
    t2 = crono(lambda: V2.rankdata(arr))
    t3 = crono(lambda: rankdata_full(arr))
    # la referencia tiene que dar lo MISMO, si no no es comparable
    ok = np.allclose(np.asarray(V2.rankdata(arr)), rankdata_full(arr))
    print("    %-28s %-8d %-11.5f %-11.5f %-9.2f %-11.5f %.2f  %s"
          % (lbl, u, t1, t2, t2/t1, t3, t2/max(t3, 1e-12), "" if ok else "<<< LA REFERENCIA NO COINCIDE"))
print()
print("    Y las tres implementaciones tienen que dar el MISMO resultado:")
v = np.array([3.0, 1.0, 1.0, 2.0, 5.0, 5.0, 5.0])
print("      v1              = %s" % np.asarray(V1.rankdata(v)))
print("      v2 vectorizada  = %s" % np.asarray(V2.rankdata(v)))
print("      v2 naive        = %s" % np.asarray(V2.rankdata_naive(v)))
print("      sin-loop        = %s" % rankdata_full(v))

# ============ 5. MEMORIA ============
print("\n[5] MEMORIA (tracemalloc, pico por llamada)")
pre, post, w, bin_of = grafo(16000, 240000)
def pico(f):
    gc.collect(); tracemalloc.start()
    f()
    cur, pk = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return pk / 1048576.0
W = V2.build_weights(pre, post, w, 16000, mode=V2.WEIGHT_COMPLEX)[0]
Wn = V2.normalize_spectral(W)[0]
tau = V2.make_tau(16000); tau = tau[0] if isinstance(tau, tuple) else tau
stim = np.arange(0, 400, dtype=np.int64)
print("    grafo n=16000  aristas=%d" % pre.shape[0])
print("    %-24s %-14s %-14s %s" % ("etapa", "v1 (MB)", "v2 (MB)", "v2/v1"))
for lbl, f1, f2 in [
    ("build_weights", lambda: V1.build_complex_weights(pre, post, w, 16000),
                      lambda: V2.build_weights(pre, post, w, 16000, mode=V2.WEIGHT_COMPLEX)),
    ("normalize_spectral", lambda: V1.normalize_spectral(W.copy()),
                           lambda: V2.normalize_spectral(W.copy())),
    ("propagate 60 pasos", lambda: V1.propagate(Wn, tau, stim, n_steps=60),
                           lambda: V2.propagate(Wn, tau, stim, n_steps=60)),
]:
    m1, m2 = pico(f1), pico(f2)
    print("    %-24s %-14.2f %-14.2f %.3f" % (lbl, m1, m2, m2/max(m1, 1e-9)))

# ============ 6. TABLA DE CONTRATOS ============
print("\n[6] TABLA DE CONTRATOS: cuantos valores devuelve cada funcion")
print("    (esto es lo que causo el IndexError: propagate de v1 devuelve 2 y la de v2, 3)")
pre4, post4, w4, bin4 = grafo(1000, 8000)
Wq = V2.build_weights(pre4, post4, w4, 1000, mode=V2.WEIGHT_COMPLEX)[0]
Wq = V2.normalize_spectral(Wq)[0]
tq = V2.make_tau(1000); tq = tq[0] if isinstance(tq, tuple) else tq
sq = np.arange(0, 100, dtype=np.int64)
casos = [
    ("build_weights", lambda: V1.build_complex_weights(pre4, post4, w4, 1000),
                      lambda: V2.build_weights(pre4, post4, w4, 1000, mode=V2.WEIGHT_COMPLEX)),
    ("normalize_spectral", lambda: V1.normalize_spectral(Wq.copy()),
                           lambda: V2.normalize_spectral(Wq.copy())),
    ("propagate", lambda: V1.propagate(Wq, tq, sq, n_steps=30),
                  lambda: V2.propagate(Wq, tq, sq, n_steps=30)),
    ("make_tau", lambda: V1.make_tau(1000), lambda: V2.make_tau(1000)),
    ("rdi", lambda: V1.rdi([np.ones(5), np.arange(5.0), np.arange(5.0)[::-1]]),
            lambda: V2.rdi([np.ones(5), np.arange(5.0), np.arange(5.0)[::-1]])),
]
print("    %-24s %-30s %-30s %s" % ("funcion", "v1 devuelve", "v2 devuelve", "compatible?"))
for lbl, f1, f2 in casos:
    r1, r2 = f1(), f2()
    n1 = len(r1) if isinstance(r1, tuple) else 1
    n2 = len(r2) if isinstance(r2, tuple) else 1
    t1 = str([type(x).__name__ for x in r1]) if isinstance(r1, tuple) else type(r1).__name__
    t2 = str([type(x).__name__ for x in r2]) if isinstance(r2, tuple) else type(r2).__name__
    print("    %-24s %-30s %-30s %s"
          % (lbl, ("%d: %s" % (n1, t1))[:29], ("%d: %s" % (n2, t2))[:29],
             "SI" if n1 == n2 else "NO  <<< desempaquetar por posicion ROMPE"))
print()
print("    REGLA que sale de esto: nunca indexar r[2] sobre el retorno de un motor")
print("    sin chequear len(r) primero. Los contratos de v1 y v2 NO son intercambiables")
print("    aunque los nombres coincidan.")
print("\nFIN")
