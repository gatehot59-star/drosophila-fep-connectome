"""Cierra 'el fix de rankdata no se probo en GPU', y documenta el HALLAZGO del intento anterior.

El primer intento (dentro de nm_core.py, shard 0) fallo con:
    ValueError: cupy.ndaray cannot be specified as `repeats` argument.

o sea: `cupy.repeat` NO acepta un array de device como `repeats`, mientras
`numpy.repeat` si. La version parcheada del motor usa exactamente eso, asi que
**NO es portable a cupy tal cual**. Eso es una respuesta medida a la pregunta, y es
mas util que un "anda igual".

Aca se prueban DOS reescrituras que evitan repeat con array de device:
  A) cumsum + searchsorted, todo en device, cero sincronizaciones
  B) repeat con los counts traidos a host (cp.asnumpy), la traduccion minima,
     que paga una sincronizacion device->host
y las dos se verifican contra la version de CPU del motor.

Y se incluye `rk_roto`, que es la version del intento fallido, para que el test
PUEDA DAR ROJO: si esa funcion dejara de fallar, el hallazgo no se reproduce y
habria que revisarlo.
"""
import importlib.util, sys, os, time, json
import numpy as np

BASE = os.environ.get("RK_BASE", "/workspace")
T0 = time.time()
def lg(s): print("[%6.1fs] %s" % (time.time() - T0, s), flush=True)

import hashlib
def md5f(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

sp = importlib.util.spec_from_file_location("mv2", os.path.join(BASE, "motor_v2.py"))
V2 = importlib.util.module_from_spec(sp); sys.modules["mv2"] = V2; sp.loader.exec_module(V2)
lg("motor_v2.py md5=%s" % md5f(os.path.join(BASE, "motor_v2.py")))

import cupy as cp
lg("GPU: %s   cupy %s" % (cp.cuda.runtime.getDeviceProperties(0)["name"].decode(), cp.__version__))

def rk_A(v):
    """cumsum + searchsorted: todo en device, cero sincronizaciones."""
    a = cp.asarray(v, dtype=cp.float64); n = a.shape[0]
    order = cp.argsort(a, kind="stable"); sa = a[order]
    nuevo = cp.empty(n, dtype=cp.bool_)
    nuevo[0] = True
    nuevo[1:] = sa[1:] != sa[:-1]
    i0 = cp.flatnonzero(nuevo)
    fin = cp.concatenate([i0[1:], cp.asarray([n])])
    cnt = fin - i0
    avg = i0 + (cnt - 1) / 2.0 + 1.0
    grupo = cp.cumsum(nuevo) - 1
    rs = avg[grupo]
    out = cp.empty(n, dtype=cp.float64); out[order] = rs
    return cp.asnumpy(out)

def rk_B(v):
    """repeat con los counts en HOST: la traduccion minima, paga una sincronizacion."""
    a = cp.asarray(v, dtype=cp.float64); n = a.shape[0]
    order = cp.argsort(a, kind="stable"); sa = a[order]
    uniq, i0, cnt = cp.unique(sa, return_index=True, return_counts=True)
    avg = i0 + (cnt - 1) / 2.0 + 1.0
    rs = cp.repeat(avg, cp.asnumpy(cnt).tolist())
    out = cp.empty(n, dtype=cp.float64); out[order] = rs
    return cp.asnumpy(out)

def rk_roto(v):
    """El del intento anterior, tal cual: tiene que FALLAR. Es el control."""
    a = cp.asarray(v, dtype=cp.float64); n = a.shape[0]
    order = cp.argsort(a, kind="stable"); sa = a[order]
    uniq, i0, cnt = cp.unique(sa, return_index=True, return_counts=True)
    rs = cp.repeat(i0 + (cnt - 1) / 2.0 + 1.0, cnt)
    out = cp.empty(n, dtype=cp.float64); out[order] = rs
    return cp.asnumpy(out)

CASOS = [("40 (el uso real)", np.random.default_rng(1).normal(0, 1, 40)),
         ("5k sin empates", np.random.default_rng(2).normal(0, 1, 5000)),
         ("200k sin empates", np.random.default_rng(3).normal(0, 1, 200000)),
         ("2M sin empates", np.random.default_rng(4).normal(0, 1, 2000000)),
         ("200k con 100 valores", np.random.default_rng(5).integers(0, 100, 200000).astype(np.float64)),
         ("todos iguales, 10k", np.full(10000, 3.0)),
         ("con infinitos", np.array([np.inf, 1.0, -np.inf, 1.0, np.inf]))]

lg("")
lg("########## CONTROL: la version del intento anterior TIENE que fallar ##########")
try:
    rk_roto(CASOS[0][1])
    lg("  NO FALLO. El hallazgo anterior no se reproduce -> revisar.")
except Exception as e:
    lg("  FALLA como se esperaba: %s: %s" % (type(e).__name__, str(e)[:110]))

def crono(f, reps=3):
    ts = []
    for _ in range(reps):
        cp.cuda.Stream.null.synchronize()
        t = time.perf_counter(); f(); cp.cuda.Stream.null.synchronize()
        ts.append(time.perf_counter() - t)
    return min(ts)

lg("")
lg("########## LAS DOS REESCRITURAS contra la CPU del motor ##########")
lg("  %-22s %-8s %-13s %-13s %-11s %-11s %-11s %s"
   % ("caso", "n", "|A-cpu|", "|B-cpu|", "cpu (s)", "A gpu (s)", "B gpu (s)", "A vs cpu"))
res = []
for lbl, arr in CASOS:
    rc = np.asarray(V2.rankdata(arr), dtype=np.float64)
    ra, rb = rk_A(arr), rk_B(arr)
    da = float(np.max(np.abs(rc - ra))); db = float(np.max(np.abs(rc - rb)))
    tc = crono(lambda: V2.rankdata(arr)); ta = crono(lambda: rk_A(arr)); tb = crono(lambda: rk_B(arr))
    res.append({"caso": lbl, "n": int(arr.shape[0]), "d_A": da, "d_B": db,
                "t_cpu": tc, "t_A": ta, "t_B": tb})
    lg("  %-22s %-8d %-13.3e %-13.3e %-11.6f %-11.6f %-11.6f %.2fx"
       % (lbl, arr.shape[0], da, db, tc, ta, tb, tc / max(ta, 1e-12)))

lg("")
lg("########## el caso que el motor NO ESPECIFICA: NaN ##########")
vn = np.array([3.0, np.nan, 1.0, np.nan, 2.0])
for nm, f in [("cpu del motor", lambda: np.asarray(V2.rankdata(vn))), ("gpu A", lambda: rk_A(vn)), ("gpu B", lambda: rk_B(vn))]:
    try:
        lg("  %-14s -> %s" % (nm, f()))
    except Exception as e:
        lg("  %-14s -> EXCEPCION %s" % (nm, type(e).__name__))
lg("  NOTA: el motor no especifica el comportamiento con NaN. Se reporta lo que hace,")
lg("        no se declara correcto. Y CPU y GPU pueden diferir ahi sin que nadie lo note.")

os.makedirs(os.path.join(BASE, "rk_out"), exist_ok=True)
json.dump({"gpu": cp.cuda.runtime.getDeviceProperties(0)["name"].decode(),
           "cupy": cp.__version__, "md5_motor_v2": md5f(os.path.join(BASE, "motor_v2.py")),
           "casos": res},
          open(os.path.join(BASE, "rk_out", "rk_gpu.json"), "w"), indent=1)
lg("")
lg("FIN")
print("FINRK", flush=True)
