"""Suite del fix de `rankdata`, y su prueba de que PUEDE DAR ROJO.

Por que existe: la respuesta 106 midio que `rankdata` de motor_v2 cuesta 50x lo que
deberia, porque se documenta "vectorizado" y tiene un loop de Python sobre los
valores unicos. Ahi declare que aplicar el fix "es otra entrega y necesita su
propio test". Este es ese test, y se corre ANTES de tocar el motor.

Tres cosas que esta suite tiene que hacer, y si falta una no autoriza el cambio:
  1. verificar que el fix da lo MISMO que las tres implementaciones existentes
     (v1, v2 naive, v2 vectorizada) en casos que incluyen los bordes;
  2. probar que la suite PUEDE DAR ROJO, corriendo mutantes a proposito. Un test
     que pasa con el codigo roto no mide nada (Bloque 8, patron 1);
  3. medir la ganancia, para que el cambio tenga un numero y no una intencion.

Uso:  python3 tools/test_rankdata_v3.py
Exit 0 si todo verde y los mutantes fueron detectados; 1 si no.
"""
import sys, time, gc, importlib.util
import numpy as np

BASE = "/workspace"

def load(p, nm):
    s = importlib.util.spec_from_file_location(nm, p); m = importlib.util.module_from_spec(s)
    sys.modules[nm] = m; s.loader.exec_module(m); return m

V1 = load(BASE + "/motor.py", "mv1")
V2 = load(BASE + "/motor_v2.py", "mv2")


# ==================== EL FIX ====================
def rankdata_v3(v):
    """Rangos con promedio en empates. Vectorizado DE VERDAD: sin loop de Python.

    La version de motor_v2 hace `for u, c in zip(uniq, counts)` con una asignacion
    de slice por iteracion, o sea un loop de Python proporcional a la cantidad de
    valores UNICOS. Con datos sin empates eso es un loop de largo n.

    Aca el mismo resultado sale de dos primitivas de numpy:
      - `np.unique(..., return_index=True, return_counts=True)` sobre el array ya
        ordenado da, para cada grupo de empates, su posicion de inicio y su tamano;
      - `np.repeat` expande el rango promedio de cada grupo a sus posiciones.

    El rango promedio de un grupo que arranca en `start` y tiene `c` elementos es
    `start + (c-1)/2 + 1`, con el +1 porque los rangos son 1-based. Es exactamente
    la misma cuenta que hace el loop, escrita sin el loop.
    """
    a = np.asarray(v, dtype=np.float64)
    n = a.shape[0]
    if n == 0:
        return np.empty(0, dtype=np.float64)
    order = np.argsort(a, kind="stable")
    sa = a[order]
    _uniq, idx_start, counts = np.unique(sa, return_index=True, return_counts=True)
    avg = idx_start + (counts - 1) / 2.0 + 1.0
    ranks_sorted = np.repeat(avg, counts)
    out = np.empty(n, dtype=np.float64)
    out[order] = ranks_sorted
    return out


# ==================== MUTANTES: la suite tiene que matarlos ====================
def mut_sin_mas_uno(v):
    """MUTANTE: rangos 0-based. Un off-by-one que no cambia el ORDEN, solo el valor."""
    a = np.asarray(v, dtype=np.float64); n = a.shape[0]
    if n == 0: return np.empty(0)
    o = np.argsort(a, kind="stable"); sa = a[o]
    _u, i0, c = np.unique(sa, return_index=True, return_counts=True)
    r = np.repeat(i0 + (c - 1) / 2.0, c)
    out = np.empty(n); out[o] = r; return out

def mut_sin_promediar(v):
    """MUTANTE: no promedia empates, asigna el rango del primero del grupo."""
    a = np.asarray(v, dtype=np.float64); n = a.shape[0]
    if n == 0: return np.empty(0)
    o = np.argsort(a, kind="stable"); sa = a[o]
    _u, i0, c = np.unique(sa, return_index=True, return_counts=True)
    r = np.repeat(i0 + 1.0, c)
    out = np.empty(n); out[o] = r; return out

def mut_sin_desordenar(v):
    """MUTANTE: devuelve los rangos en orden ORDENADO, sin volver al orden original."""
    a = np.asarray(v, dtype=np.float64); n = a.shape[0]
    if n == 0: return np.empty(0)
    o = np.argsort(a, kind="stable"); sa = a[o]
    _u, i0, c = np.unique(sa, return_index=True, return_counts=True)
    return np.repeat(i0 + (c - 1) / 2.0 + 1.0, c)

def mut_descendente(v):
    """MUTANTE: ordena al reves. Los rangos quedan invertidos."""
    a = np.asarray(v, dtype=np.float64); n = a.shape[0]
    if n == 0: return np.empty(0)
    o = np.argsort(-a, kind="stable"); sa = a[o]
    _u, i0, c = np.unique(sa, return_index=True, return_counts=True)
    r = np.repeat(i0 + (c - 1) / 2.0 + 1.0, c)
    out = np.empty(n); out[o] = r; return out

def mut_promedio_mal(v):
    """MUTANTE: usa c/2 en vez de (c-1)/2. Solo falla cuando HAY empates."""
    a = np.asarray(v, dtype=np.float64); n = a.shape[0]
    if n == 0: return np.empty(0)
    o = np.argsort(a, kind="stable"); sa = a[o]
    _u, i0, c = np.unique(sa, return_index=True, return_counts=True)
    r = np.repeat(i0 + c / 2.0 + 1.0, c)
    out = np.empty(n); out[o] = r; return out


# ==================== LOS CASOS ====================
rng = np.random.default_rng(20260826)
CASOS = [
    ("un solo elemento", np.array([7.0])),
    ("dos iguales", np.array([5.0, 5.0])),
    ("todos iguales", np.full(9, 3.0)),
    ("todos distintos", np.array([3.0, 1.0, 4.0, 1.5, 9.0, 2.6])),
    ("el caso del docstring", np.array([3.0, 1.0, 1.0, 2.0, 5.0, 5.0, 5.0])),
    ("ya ordenado", np.arange(12.0)),
    ("orden inverso", np.arange(12.0)[::-1].copy()),
    ("negativos y cero", np.array([-2.0, 0.0, -2.0, 3.0, 0.0])),
    ("cero negativo", np.array([0.0, -0.0, 1.0])),
    ("muy grandes y muy chicos", np.array([1e300, 1e-300, -1e300, 0.0])),
    ("con infinitos", np.array([np.inf, 1.0, -np.inf, 1.0, np.inf])),
    ("40 elementos, como el test global", rng.normal(0, 1, 40)),
    ("1000 con muchos empates", rng.integers(0, 7, 1000).astype(np.float64)),
    ("1000 sin empates", rng.normal(0, 1, 1000)),
]

IMPLS = [("v1", lambda x: np.asarray(V1.rankdata(x), dtype=np.float64)),
         ("v2_naive", lambda x: np.asarray(V2.rankdata_naive(x), dtype=np.float64)),
         ("v2_vect", lambda x: np.asarray(V2.rankdata(x), dtype=np.float64))]

print("=" * 100)
print("SUITE DEL FIX DE rankdata  \u00b7  %d casos, %d implementaciones de referencia" % (len(CASOS), len(IMPLS)))
print("=" * 100)

fallas = []
print("\n[1] EQUIVALENCIA con las tres implementaciones existentes")
print("    %-38s %-8s %-12s %-12s %-12s" % ("caso", "n", "vs v1", "vs v2_naive", "vs v2_vect"))
for nombre, arr in CASOS:
    got = rankdata_v3(arr)
    fila = []
    for impl_nm, fn in IMPLS:
        try:
            ref = fn(arr)
            ok = got.shape == ref.shape and np.allclose(got, ref, rtol=0, atol=1e-12, equal_nan=True)
        except Exception as e:
            ok = False
            ref = "EXC %s" % type(e).__name__
        fila.append("OK" if ok else "FALLA")
        if not ok:
            fallas.append((nombre, impl_nm, str(got)[:70], str(ref)[:70]))
    print("    %-38s %-8d %-12s %-12s %-12s" % (nombre, arr.shape[0], fila[0], fila[1], fila[2]))

print("\n[2] PROPIEDADES que tienen que valer por definicion")
props = []
for nombre, arr in CASOS:
    r = rankdata_v3(arr)
    n = arr.shape[0]
    finito = np.all(np.isfinite(arr))
    # la suma de rangos de 1..n es n(n+1)/2, y promediar empates la preserva
    suma_ok = abs(float(np.sum(r)) - n * (n + 1) / 2.0) < 1e-6
    # valores iguales -> rangos iguales
    emp_ok = True
    for u in np.unique(arr):
        m = (arr == u)
        if m.sum() > 1 and not np.allclose(r[m], r[m][0]):
            emp_ok = False
    # monotonia: si a<b entonces rango(a)<rango(b)
    o = np.argsort(arr, kind="stable")
    mono_ok = bool(np.all(np.diff(r[o]) >= -1e-12))
    rango_ok = bool(n == 0 or (r.min() >= 1.0 - 1e-12 and r.max() <= n + 1e-12))
    props.append((nombre, suma_ok, emp_ok, mono_ok, rango_ok))
    if not (suma_ok and emp_ok and mono_ok and rango_ok):
        fallas.append((nombre, "propiedades",
                       "suma=%s empates=%s monotonia=%s rango=%s" % (suma_ok, emp_ok, mono_ok, rango_ok), ""))
print("    %-38s %-10s %-10s %-12s %-10s" % ("caso", "suma", "empates", "monotonia", "rango 1..n"))
for nombre, a, b, c, d in props:
    print("    %-38s %-10s %-10s %-12s %-10s" % (nombre, "OK" if a else "FALLA", "OK" if b else "FALLA",
                                                 "OK" if c else "FALLA", "OK" if d else "FALLA"))

print("\n[3] LOS MUTANTES: la suite tiene que DETECTARLOS a todos")
print("    Un test que pasa con el codigo roto no mide nada.")
MUTANTES = [("sin el +1 (0-based)", mut_sin_mas_uno),
            ("no promedia empates", mut_sin_promediar),
            ("no vuelve al orden original", mut_sin_desordenar),
            ("ordena descendente", mut_descendente),
            ("c/2 en vez de (c-1)/2", mut_promedio_mal)]
print("    %-34s %-12s %s" % ("mutante", "detectado", "primer caso que lo mata"))
escapes = []
for mn, mf in MUTANTES:
    matado_por = None
    for nombre, arr in CASOS:
        ref = np.asarray(V2.rankdata_naive(arr), dtype=np.float64)
        try:
            got = mf(arr)
            igual = got.shape == ref.shape and np.allclose(got, ref, rtol=0, atol=1e-12, equal_nan=True)
        except Exception:
            igual = False
        if not igual:
            matado_por = nombre
            break
    if matado_por is None:
        escapes.append(mn)
    print("    %-34s %-12s %s" % (mn, "SI" if matado_por else "NO  <<< ESCAPO",
                                  matado_por or "ninguno"))

print("\n[4] LA GANANCIA, medida")
def crono(f, reps=3):
    ts = []
    for _ in range(reps):
        gc.collect(); t = time.perf_counter(); f(); ts.append(time.perf_counter() - t)
    return min(ts)
print("    %-26s %-9s %-12s %-12s %-12s %s" % ("caso", "unicos", "v2_vect", "v3", "v3/v2", "ganancia"))
for lbl, arr in [("5k sin empates", rng.normal(0, 1, 5000)),
                 ("50k sin empates", rng.normal(0, 1, 50000)),
                 ("50k con 100 valores", rng.integers(0, 100, 50000).astype(np.float64)),
                 ("40 (el uso real)", rng.normal(0, 1, 40))]:
    u = int(np.unique(arr).size)
    t2 = crono(lambda: V2.rankdata(arr))
    t3 = crono(lambda: rankdata_v3(arr))
    print("    %-26s %-9d %-12.6f %-12.6f %-12.4f %.1fx"
          % (lbl, u, t2, t3, t3 / max(t2, 1e-12), t2 / max(t3, 1e-12)))

print("\n" + "=" * 100)
if fallas:
    print("ROJO: %d fallas" % len(fallas))
    for f in fallas[:10]:
        print("   %s | %s | got=%s | ref=%s" % f)
if escapes:
    print("ROJO: %d mutantes ESCAPARON -> la suite no autoriza el cambio: %s" % (len(escapes), escapes))
if not fallas and not escapes:
    print("VERDE: %d casos x %d referencias equivalentes, 4 propiedades por caso,"
          % (len(CASOS), len(IMPLS)))
    print("       y %d de %d mutantes DETECTADOS. La suite puede dar rojo, o sea que mide."
          % (len(MUTANTES), len(MUTANTES)))
    print("       El cambio del motor queda AUTORIZADO por esta suite.")
print("=" * 100)
sys.exit(1 if (fallas or escapes) else 0)
