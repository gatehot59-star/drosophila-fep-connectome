"""AUDITORIA v1 vs v2, paso 2: POR QUE difieren las matrices de peso.

Mismo nnz (los dos funden multi-aristas) pero |W1-W2| max = 5,28 sobre el grafo de
prueba. Se descompone en MAGNITUD y FASE para ubicar la diferencia, y se re-corre
con phase_jitter=0.0 para aislar si el ruido de fase es TODA la diferencia.

E-01: el sujeto son los dos ARCHIVOS importados como modulos, no una reimplementacion.
W-01: cada comparacion imprime los dos valores crudos, no solo el veredicto.

Corrido en brain-env el 2026-08-26. Salida verbatim en
docs/agents/evidencia/2026-08-26-105-auditoria-v1-vs-v2-evidencia-cruda.md
"""
import importlib.util, sys, numpy as np

def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    sys.modules[n] = m; s.loader.exec_module(m); return m
V1 = load("/workspace/motor.py", "mv1")
V2 = load("/workspace/motor_v2.py", "mv2")

rng = np.random.default_rng(20260826)
n, e = 4000, 60000
per = n // 10
bin_of = np.minimum(np.arange(n) // per, 9).astype(np.int64)
pre = rng.integers(0, n, e).astype(np.int64)
same = rng.random(e) < 0.70
post = np.where(same, bin_of[pre]*per + rng.integers(0, per, e), rng.integers(0, n, e)).astype(np.int64)
keep = pre != post; pre, post = pre[keep], post[keep]
# multi-aristas a proposito: es el caso donde v1 y v2 podrian diferir
dup = rng.choice(pre.shape[0], size=3000, replace=False)
pre = np.concatenate([pre, pre[dup]]); post = np.concatenate([post, post[dup]])
is_inh = rng.random(n) < 0.30
mag = rng.lognormal(0.0, 0.6, pre.shape[0])
w = np.where(is_inh[pre], -mag, mag)

print("=" * 100)
print("PASO 2 \u00b7 POR QUE difieren las matrices de peso")
print("=" * 100)

r1 = V1.build_complex_weights(pre, post, w, n)
r2 = V2.build_weights(pre, post, w, n, mode=V2.WEIGHT_COMPLEX)
W1, W2 = r1[0].tocsr(), r2[0].tocsr()
print("\n  v1 devuelve: %s" % str([type(x).__name__ for x in r1]))
print("  v2 devuelve: %s" % str([type(x).__name__ for x in r2]))
print("  v2 valores 2 y 3: %s | %s" % (str(r2[1])[:150], str(r2[2])[:150]))

W1.sort_indices(); W2.sort_indices()
print("\n  mismos indices? %s" % (np.array_equal(W1.indices, W2.indices) and np.array_equal(W1.indptr, W2.indptr)))
a, b = W1.data, W2.data
print("  nnz %d vs %d" % (a.size, b.size))

print("\n[MAGNITUD]  |w|")
print("    v1: min=%.6f  med=%.6f  max=%.6f  suma=%.4f" % (np.abs(a).min(), np.median(np.abs(a)), np.abs(a).max(), np.abs(a).sum()))
print("    v2: min=%.6f  med=%.6f  max=%.6f  suma=%.4f" % (np.abs(b).min(), np.median(np.abs(b)), np.abs(b).max(), np.abs(b).sum()))
dm = np.abs(np.abs(a) - np.abs(b))
print("    | |w1|-|w2| |  max=%.6e  medio=%.6e  cuantos difieren>1e-12: %d de %d" % (dm.max(), dm.mean(), int((dm > 1e-12).sum()), dm.size))

print("\n[FASE]  angulo")
f1, f2 = np.angle(a), np.angle(b)
df = np.abs(np.angle(np.exp(1j*(f1-f2))))
print("    v1: min=%.6f  max=%.6f  medio|.|=%.6f" % (f1.min(), f1.max(), np.abs(f1).mean()))
print("    v2: min=%.6f  max=%.6f  medio|.|=%.6f" % (f2.min(), f2.max(), np.abs(f2).mean()))
print("    |fase1-fase2|  max=%.6f  medio=%.6f  cuantos difieren>1e-12: %d de %d" % (df.max(), df.mean(), int((df > 1e-12).sum()), df.size))

print("\n[SIGNO / reparto E-I]")
for nm, x in [("v1", a), ("v2", b)]:
    inh = int((x.real < 0).sum())
    print("    %s: parte real negativa en %d de %d aristas (%.2f%%)" % (nm, inh, x.size, 100.0*inh/x.size))

print("\n[LA MISMA MATRIZ SIN JITTER DE FASE?]")
c1 = V1.build_complex_weights(pre, post, w, n, phase_jitter=0.0)[0].tocsr()
c2 = V2.build_weights(pre, post, w, n, mode=V2.WEIGHT_COMPLEX, phase_jitter=0.0)[0].tocsr()
c1.sort_indices(); c2.sort_indices()
d0 = np.abs(c1.data - c2.data)
print("    con phase_jitter=0.0  ->  |W1-W2| max = %.6e   difieren>1e-12: %d de %d" % (d0.max(), int((d0>1e-12).sum()), d0.size))
if d0.max() < 1e-12:
    print("    *** LA DIFERENCIA ES SOLO EL JITTER DE FASE: mismas magnitudes, mismo signo,")
    print("        distinta realizacion del ruido aleatorio. Mismo modelo, otra semilla efectiva.")
else:
    print("    *** La diferencia NO es solo el jitter: hay algo mas.")

print("\n[MODOS DE PESO]")
print("    modos de v2: %s" % [x for x in dir(V2) if x.startswith("WEIGHT_")])
print("    modos de v1: %s" % [x for x in dir(V1) if x.startswith("WEIGHT_")])
