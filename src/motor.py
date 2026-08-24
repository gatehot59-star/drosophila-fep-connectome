# =====================================================================
# MOTOR LTC COMPLEJO - implementacion de referencia
# Especificacion: Jorge Abraham Mendieta
#
# z_{t+1} = (1 - tau) * z_t + tau * f(W^T z_t + s_t)
#   z   in C^n      amplitud = cuanto, fase = cuando
#   tau in C^n      Re = tasa de integracion, Im = frecuencia intrinseca
#                   POR NEURONA: cada una resuena a su propia frecuencia
#   W   in C^{nxn}  |w| = fuerza sinaptica, arg(w) = signo E/I como fase
#
# Lo que esta implementacion NO hace, y por que:
#  - no inventa priors: los mide del conectoma y los reporta con checksum
#  - no usa una activacion con polos como default
#  - no acepta un rango de tau que diverge sin avisar
#  - no usa un null que rompa el grado entrante
#  - no reporta un ratio cuando el null conserva la cantidad medida
#
# Los tests del bloque TESTS pueden dar ROJO. Un test que no puede fallar
# no mide nada.
# =====================================================================
import os, sys, json, math, time, hashlib, urllib.request
import numpy as np
import pandas as pd
import scipy.sparse as sps

T0 = time.time()
FAILURES = []

def lg(s):
    print("[" + format(time.time() - T0, ".1f") + "s] " + str(s), flush=True)

def check(name, ok, detail):
    """Registra un test. Un fallo no aborta: se acumula y se reporta al final."""
    lg("  " + ("OK  " if ok else "FAIL") + "  " + name + ": " + detail)
    if not ok:
        FAILURES.append(name)
    return ok

# =====================================================================
# 1. ESTABILIDAD - el guard que faltaba
# =====================================================================

def tau_stability_limit(tau_real):
    """Maximo |Im(tau)| que mantiene |1 - tau| < 1.

    El factor que multiplica al estado previo es (1 - tau). Si su modulo
    supera 1, el estado crece sin cota sin importar la activacion. El
    umbral es exacto y derivable: |Im| < sqrt(1 - (1 - Re)^2).
    Con Re = 0.119 vale 0.473116.
    """
    inner = 1.0 - (1.0 - tau_real) ** 2
    return math.sqrt(inner) if inner > 0.0 else 0.0

def validate_tau(tau_real, tau_imag_range):
    """Rechaza configuraciones que divergen por construccion."""
    if not 0.0 < tau_real < 2.0:
        raise ValueError("tau_real fuera de (0,2): " + str(tau_real))
    limit = tau_stability_limit(tau_real)
    worst = max(abs(tau_imag_range[0]), abs(tau_imag_range[1]))
    if worst >= limit:
        raise ValueError(
            "|Im(tau)| maximo " + str(worst) + " alcanza el limite de "
            + "estabilidad " + format(limit, ".6f") + " para Re(tau)="
            + str(tau_real) + ": |1-tau| seria "
            + format(abs(complex(1.0 - tau_real, -worst)), ".6f") + " > 1"
        )
    return limit

# =====================================================================
# 2. ACTIVACION - acotada por defecto, y que avisa en vez de callarse
# =====================================================================

def bounded_complex_tanh(z, clip=2.0):
    """tanh compleja con la MAGNITUD acotada y la FASE preservada.

    tanh es holomorfa y por eso mismo tiene polos en i*pi/2 + i*k*pi:
    medido, |tanh| llega a 1e8 a 1e-8 del polo. Sin cota el estado explota
    a NaN, y np.angle(NaN) devuelve NaN en silencio, o sea que la fase se
    corrompe sin que ninguna metrica lo reporte. Acotar la magnitud y
    dejar la fase intacta es lo correcto cuando la fase es la variable de
    interes.
    """
    with np.errstate(over="ignore", invalid="ignore"):
        out = np.tanh(z)
    bad = ~np.isfinite(out)
    if np.any(bad):
        mag = np.abs(z[bad])
        safe = np.where(mag > 1e-300, mag, 1.0)
        out[bad] = clip * (z[bad] / safe)
    mag = np.abs(out)
    over = mag > clip
    if np.any(over):
        out[over] = clip * out[over] / mag[over]
    return out

def raw_complex_tanh(z):
    """tanh holomorfa sin cota. Existe SOLO para el test que la refuta."""
    with np.errstate(over="ignore", invalid="ignore"):
        return np.tanh(z)

# =====================================================================
# 3. PESOS COMPLEJOS desde el conectoma medido
# =====================================================================

def build_complex_weights(pre, post, w, n, phase_jitter=0.1, seed=42):
    """Matriz de pesos complejos: |w| del conectoma, arg(w) = signo E/I.

    La fase se asigna por NEURONA PRESINAPTICA, no por arista. Eso es la
    ley de Dale, y en este conectoma es exacto: se midieron 138.005
    neuronas con salidas y CERO tienen salidas de los dos signos.
    96.672 puramente excitatorias, 41.333 puramente inhibitorias.
    El test test_dale_law lo verifica sobre los datos cargados en vez de
    confiar en este comentario.

    Excitatoria -> fase cerca de 0. Inhibitoria -> fase cerca de pi.
    El jitter rompe la simetria exacta sin cambiar el signo.
    """
    rng = np.random.default_rng(seed)
    pos = np.bincount(pre, weights=(w > 0).astype(np.float64), minlength=n)
    neg = np.bincount(pre, weights=(w < 0).astype(np.float64), minlength=n)
    is_inh = neg > pos
    base = np.where(is_inh[pre], np.pi, 0.0)
    phases = base + rng.normal(0.0, phase_jitter, pre.shape[0])
    data = np.abs(w).astype(np.float64) * np.exp(1j * phases)
    W = sps.csr_matrix((data, (pre, post)), shape=(n, n), dtype=np.complex128)
    return W, is_inh

def normalize_spectral(W, target=0.99, n_iter=200, tol=1e-10):
    """Escala W para que su radio espectral sea target.

    Devuelve (W_escalada, rho, convergio). Los TRES, siempre: una funcion
    que devuelve solo un float no permite distinguir convergencia de
    agotamiento de iteraciones, y ese es un estado NO MEDIDO disfrazado de
    medicion. Ademas compara el cambio RELATIVO, no absoluto: con un rho
    de 3e-9 un umbral absoluto de 1e-8 se cumple en la primera iteracion y
    devuelve 0.0, lo que deja la matriz sin normalizar en silencio.
    """
    n = W.shape[0]
    rng = np.random.default_rng(7)
    v = rng.standard_normal(n) + 1j * rng.standard_normal(n)
    v /= np.linalg.norm(v)
    rho = 0.0
    converged = False
    for k in range(n_iter):
        Wv = W.dot(v)
        nrm = float(np.linalg.norm(Wv))
        if nrm < 1e-300:
            return W * 0.0, 0.0, True
        v = Wv / nrm
        if k > 0 and abs(nrm - rho) <= tol * max(nrm, 1e-30):
            rho = nrm
            converged = True
            break
        rho = nrm
    if not converged:
        lg("  AVISO: el radio espectral no convergio en " + str(n_iter)
           + " iteraciones. rho=" + format(rho, ".6e") + " es un limite "
           + "inferior, no una medicion.")
    if rho <= 0.0:
        raise FloatingPointError("radio espectral no positivo: no se puede normalizar")
    return W * (target / rho), rho, converged

# =====================================================================
# 4. NULLS - los dos, con su invariante verificado por corrida
# =====================================================================

def null_maslov_sneppen(pre, post, n, swap_factor=3, batch=2000000, seed=0):
    """Preserva grado entrante Y saliente exactos. Sin auto-lazos ni duplicados.

    Responde: esto es mas que la secuencia de grados?
    """
    rng = np.random.default_rng(seed)
    E = pre.shape[0]
    NN = np.int64(n)
    p = post.copy()
    K = np.sort(pre.astype(np.int64) * NN + p)
    target = swap_factor * E
    done = 0
    while done < target:
        i = rng.integers(0, E, batch)
        j = rng.integers(0, E, batch)
        a, b, c, d = pre[i], p[i], pre[j], p[j]
        ok = (i != j) & (b != d) & (a != d) & (c != b)
        i, j, a, b, c, d = i[ok], j[ok], a[ok], b[ok], c[ok], d[ok]
        if i.shape[0] == 0:
            continue
        cnt = np.zeros(E, dtype=np.int8)
        np.add.at(cnt, np.concatenate([i, j]), 1)
        keep = (cnt[i] == 1) & (cnt[j] == 1)
        del cnt
        i, j, a, b, c, d = i[keep], j[keep], a[keep], b[keep], c[keep], d[keep]
        if i.shape[0] == 0:
            continue
        k1 = a.astype(np.int64) * NN + d
        k2 = c.astype(np.int64) * NN + b
        q1 = np.minimum(np.searchsorted(K, k1), K.shape[0] - 1)
        q2 = np.minimum(np.searchsorted(K, k2), K.shape[0] - 1)
        free = (K[q1] != k1) & (K[q2] != k2) & (k1 != k2)
        i, j, b, d, k1, k2 = i[free], j[free], b[free], d[free], k1[free], k2[free]
        if i.shape[0] == 0:
            continue
        u2, c2 = np.unique(np.concatenate([k1, k2]), return_counts=True)
        dup = u2[c2 > 1]
        if dup.shape[0] > 0:
            good = ~(np.isin(k1, dup) | np.isin(k2, dup))
            i, j, b, d, k1, k2 = i[good], j[good], b[good], d[good], k1[good], k2[good]
        if i.shape[0] == 0:
            continue
        old = np.concatenate([pre[i].astype(np.int64) * NN + b,
                              pre[j].astype(np.int64) * NN + d])
        p[i] = d
        p[j] = b
        K = np.sort(np.concatenate([np.setdiff1d(K, old, assume_unique=True), k1, k2]))
        done += int(i.shape[0])
    return p, done

def null_community_preserving(pre, post, block_of_node, seed=0):
    """Preserva grado entrante, saliente Y la matriz de conectividad entre bloques.

    Responde: esto es mas que la arquitectura modular?

    PERMUTA los destinos existentes dentro de cada bloque. No sortea
    uniformemente: sortear cambia el grado entrante de casi todos los nodos
    (medido: 188 de 200), y entonces cualquier diferencia contra el real
    puede venir del grado en vez de la modularidad, que es justo lo que
    este null aisla. Una linea de diferencia decide si el control sirve.

    ADVERTENCIA declarada: este null SI puede crear multi-aristas, a
    diferencia del Maslov-Sneppen. Se cuentan y se reportan.
    """
    rng = np.random.default_rng(seed)
    p = post.copy()
    key = block_of_node[pre].astype(np.int64) * 1000 + block_of_node[post]
    order = np.argsort(key, kind="stable")
    ks = key[order]
    uk = np.unique(ks)
    lo = np.searchsorted(ks, uk, side="left")
    hi = np.searchsorted(ks, uk, side="right")
    for bi in range(uk.shape[0]):
        idx = order[lo[bi]:hi[bi]]
        if idx.shape[0] < 2:
            continue
        p[idx] = rng.permutation(post[idx])
    return p

# =====================================================================
# 5. DINAMICA
# =====================================================================

def make_tau(n, tau_real=0.119, tau_imag_range=(0.01, 0.15), seed=42):
    """tau compleja HETEROGENEA por neurona. Valida antes de devolver.

    Re(tau) = 0.119 es el valor del paper: sobrevivio la auditoria completa.
    Im(tau) es la frecuencia intrinseca, distinta en cada neurona. Eso es
    lo que hace a la red un banco de osciladores en vez de un oscilador.
    """
    limit = validate_tau(tau_real, tau_imag_range)
    rng = np.random.default_rng(seed)
    im = rng.uniform(tau_imag_range[0], tau_imag_range[1], n)
    return np.full(n, tau_real) + 1j * im, limit

def propagate(W, tau, stim_idx, n_steps=200, t_on=10, t_off=60,
              amp=1.0, activation=bounded_complex_tanh, save_at=None):
    """Corre la dinamica y devuelve el estado en los pasos pedidos.

    z_{t+1} = (1 - tau) * z_t + tau * f(W^T z_t + s_t)
    El estado guardado en el indice t es el POSTERIOR al update de t.
    """
    n = W.shape[0]
    WT = W.T.tocsr()
    z = np.zeros(n, dtype=np.complex128)
    s = np.zeros(n, dtype=np.complex128)
    s[stim_idx] = amp
    keep = set(save_at) if save_at is not None else set()
    out = {}
    one_minus = 1.0 - tau
    for t in range(n_steps):
        drive = WT.dot(z)
        if t_on <= t <= t_off:
            drive = drive + s
        z = one_minus * z + tau * activation(drive)
        if t in keep:
            out[t] = z.copy()
    return out, z

# =====================================================================
# 6. METRICAS - la que no premia cadaveres
# =====================================================================

def region_profile(z, bin_of_node, n_bins):
    """Perfil de amplitud media por region, sobre nodos anotados."""
    m = bin_of_node >= 0
    v = np.bincount(bin_of_node[m], weights=np.abs(z[m]), minlength=n_bins)
    c = np.bincount(bin_of_node[m], minlength=n_bins).astype(np.float64)
    nz = c > 0
    v[nz] /= c[nz]
    return v

def cosine_distance(a, b):
    """1 - cos(theta). Devuelve NaN si alguno colapso.

    La distancia angular a un vector nulo no esta definida. Elegir 1.0 hace
    que un control apagado puntue como MAXIMAMENTE diferenciado y le gane
    al conectoma real: medido, 1.0000 contra 0.7424, o sea 1.347x. Es la
    misma clase de error que un cociente cuyo denominador muere.
    Quien agregue DEBE excluir los NaN y decir cuantos excluyo.
    """
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na < 1e-15 or nb < 1e-15:
        return float("nan")
    return 1.0 - float(np.dot(a, b)) / (na * nb)

def rdi(profiles):
    """Media de (1 - cos) sobre pares validos.

    Devuelve (valor, n_validos, n_excluidos). Los tres: un RDI sobre 3
    pares y uno sobre 1 par no son el mismo numero, y reportar solo el
    primero esconde cuanta evidencia lo sostiene.
    """
    ds = []
    k = len(profiles)
    for i in range(k):
        for j in range(i + 1, k):
            ds.append(cosine_distance(profiles[i], profiles[j]))
    ok = [d for d in ds if not math.isnan(d)]
    if len(ok) == 0:
        return float("nan"), 0, len(ds)
    return float(np.mean(ok)), len(ok), len(ds) - len(ok)

def phase_coherence(z):
    """Parametro de orden de Kuramoto sobre las neuronas activas.

    Se filtra por AMPLITUD, no por fase: una neurona con z=0 tiene fase 0,
    que es un valor legitimo, asi que filtrar por fase distinta de cero
    descarta neuronas activas y cuenta neuronas muertas.
    """
    m = np.abs(z) > 1e-12
    if not np.any(m):
        return float("nan")
    return float(np.abs(np.mean(np.exp(1j * np.angle(z[m])))))

# =====================================================================
# 7. TEST GLOBAL con guard de tautologia
# =====================================================================

def rankdata(v):
    """Rangos con promedio en los empates. Sin dependencias externas."""
    n = len(v)
    idx = sorted(range(n), key=lambda i: v[i])
    r = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and v[idx[j + 1]] == v[idx[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[idx[k]] = avg
        i = j + 1
    return r

def global_rank_test(real, nulls, names):
    """Suma de rangos sobre k estadisticos a la vez. UN test, no k.

    Los n+1 grafos son intercambiables bajo la hipotesis nula, asi que la
    distribucion del estadistico sale de los nulls sin supuestos y no hace
    falta correccion multiple. Con n nulls el piso de p a dos colas es
    2/(n+1).

    GUARD DE TAUTOLOGIA, y esta aca por un error propio medido: si la
    desviacion estandar de un estadistico bajo el null es exactamente
    cero, ese null CONSERVA la cantidad y el test no puede fallar. Se
    reporta NO_TESTEABLE en vez de un ratio de 1.000x que parece un
    resultado. Sin este guard se gastan 22 minutos de computo ajeno para
    medir nada.
    """
    per = {}
    usable = []
    for nm in names:
        col = [x[nm] for x in nulls]
        sd = float(np.std(col))
        if sd == 0.0:
            per[nm] = {"verdict": "NO_TESTEABLE",
                       "reason": "el null conserva esta cantidad (sd=0)",
                       "real": real[nm], "null_mean": float(np.mean(col))}
            continue
        usable.append(nm)
        mu = float(np.mean(col))
        ge = int(np.sum(np.array(col) >= real[nm]))
        le = int(np.sum(np.array(col) <= real[nm]))
        per[nm] = {"verdict": "TESTEABLE", "real": real[nm],
                   "null_mean": mu, "null_sd": sd,
                   "ratio": (real[nm] / mu) if mu != 0 else float("inf"),
                   "n_ge": ge, "n_le": le,
                   "p_two": min(1.0, 2.0 * min((ge + 1.0), (le + 1.0)) / (len(nulls) + 1.0))}
    if len(usable) == 0:
        return {"global": None, "per_statistic": per,
                "error": "ningun estadistico es testeable con este null"}
    S = np.zeros(len(nulls) + 1)
    for nm in usable:
        vals = [real[nm]] + [x[nm] for x in nulls]
        S += np.array(rankdata(vals))
    n = len(nulls)
    below = int(np.sum(S[1:] <= S[0]))
    above = int(np.sum(S[1:] >= S[0]))
    p_two = min(1.0, 2.0 * min((below + 1.0) / (n + 1.0), (above + 1.0) / (n + 1.0)))
    return {"global": {"S_real": float(S[0]), "S_null_mean": float(np.mean(S[1:])),
                       "S_null_sd": float(np.std(S[1:], ddof=1)),
                       "S_null_min": float(np.min(S[1:])),
                       "n_below": below, "n_above": above,
                       "p_two_sided": p_two, "floor": 2.0 / (n + 1.0),
                       "k_usable": len(usable), "k_total": len(names)},
            "per_statistic": per}

# =====================================================================
# 8. DATOS - medidos, con checksum verificado
# =====================================================================

PARQUET_URL = "https://raw.githubusercontent.com/eonsystemspbc/fly-brain/main/data/2025_Connectivity_783.parquet"
ANNOT_SHA = "17fc57722002e1a7d38cdd0c89ac382bf92718da"
ANNOT_URL = ("https://raw.githubusercontent.com/flyconnectome/flywire_annotations/"
             + ANNOT_SHA + "/supplemental_files/Supplemental_file1_neuron_annotations.tsv")
MD5_PARQUET = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_ANNOT = "719904abad876c68ace1b5690c9b9b63"

def md5_of(path):
    h = hashlib.md5()
    f = open(path, "rb")
    while True:
        b = f.read(1048576)
        if not b:
            break
        h.update(b)
    f.close()
    return h.hexdigest()

def load_connectome(data_dir):
    """Descarga si falta, verifica checksums, y devuelve el grafo con etiquetas.

    Los checksums no son decorativos: la tabla de anotaciones se sirve de una
    rama viva y cambio entre marzo y agosto de 2026. Si un md5 no coincide,
    esto NO es el grafo sobre el que se midieron los priors, y el llamador
    tiene que saberlo antes de interpretar cualquier numero.
    """
    os.makedirs(data_dir, exist_ok=True)
    pq = os.path.join(data_dir, "connectivity.parquet")
    an = os.path.join(data_dir, "annotations.tsv")
    if not os.path.exists(pq):
        urllib.request.urlretrieve(PARQUET_URL, pq)
    if not os.path.exists(an):
        urllib.request.urlretrieve(ANNOT_URL, an)
    m1, m2 = md5_of(pq), md5_of(an)
    check("md5_parquet", m1 == MD5_PARQUET, m1)
    check("md5_annotations", m2 == MD5_ANNOT, m2 + "  (SHA " + ANNOT_SHA[:8] + ")")
    df = pd.read_parquet(pq)
    pre = df["Presynaptic_Index"].values.astype(np.int64)
    post = df["Postsynaptic_Index"].values.astype(np.int64)
    w = df["Excitatory x Connectivity"].values.astype(np.float64)
    preid = df["Presynaptic_ID"].values.astype(np.int64)
    postid = df["Postsynaptic_ID"].values.astype(np.int64)
    n = int(max(pre.max(), post.max())) + 1
    allid = np.concatenate([preid, postid])
    allix = np.concatenate([pre, post])
    o = np.argsort(allid, kind="stable")
    uid, first = np.unique(allid[o], return_index=True)
    uix = allix[o][first]
    del df, allid, allix, o, preid, postid
    ann = pd.read_csv(an, sep=chr(9), low_memory=False)
    rid = ann["root_id"].values.astype(np.int64)
    scv = ann["super_class"].astype(str).values
    ccv = ann["cell_class"].astype(str).values
    flv = ann["flow"].astype(str).values
    pos = np.minimum(np.searchsorted(uid, rid), uid.shape[0] - 1)
    hit = uid[pos] == rid
    ix = uix[pos]
    names = sorted(set(scv[hit]))
    bin_of = np.full(n, -1, dtype=np.int64)
    for k in range(rid.shape[0]):
        if hit[k]:
            bin_of[int(ix[k])] = names.index(scv[k])
    mods = [("visual", ["visual"]), ("olfactory", ["olfactory", "ORN"]),
            ("mechanosensory", ["mechanosensory"])]
    stim = []
    for _, classes in mods:
        sel = []
        for k in range(rid.shape[0]):
            if hit[k] and flv[k] == "afferent" and ccv[k] in classes:
                sel.append(int(ix[k]))
        stim.append(np.array(sorted(set(sel)), dtype=np.int64))
    return {"pre": pre, "post": post, "w": w, "n": n, "bin_of": bin_of,
            "bin_names": names, "stim": stim,
            "mod_names": [m[0] for m in mods],
            "md5": {"parquet": m1, "annotations": m2, "annot_sha": ANNOT_SHA}}

# =====================================================================
# 9. TESTS - cada uno puede dar ROJO
# =====================================================================

def test_tau_guard():
    """El guard de estabilidad rechaza lo que diverge y acepta lo que no."""
    lim = tau_stability_limit(0.119)
    check("tau_limit_es_0.473116", abs(lim - 0.473116) < 1e-6, format(lim, ".6f"))
    ok_default = True
    try:
        validate_tau(0.119, (0.01, 0.15))
    except ValueError:
        ok_default = False
    check("tau_acepta_el_default", ok_default, "(0.01, 0.15) con Re=0.119")
    rejected = False
    try:
        validate_tau(0.119, (0.01, 0.48))
    except ValueError:
        rejected = True
    check("tau_rechaza_0.48", rejected,
          "|1-tau| seria " + format(abs(complex(0.881, -0.48)), ".6f") + " > 1")

def test_activation_bounded():
    """La activacion acotada sobrevive el polo. La cruda, no."""
    z = np.array([1j * (math.pi / 2 - 1e-8), 1j * (math.pi / 2 - 1e-12)],
                 dtype=np.complex128)
    raw = raw_complex_tanh(z)
    bnd = bounded_complex_tanh(z, clip=2.0)
    check("tanh_cruda_explota", float(np.max(np.abs(raw))) > 1e6,
          "|tanh| max = " + format(float(np.max(np.abs(raw))), ".3e"))
    check("tanh_acotada_respeta_el_clip", float(np.max(np.abs(bnd))) <= 2.0 + 1e-12,
          "|f| max = " + format(float(np.max(np.abs(bnd))), ".6f"))
    ang_raw = np.angle(raw)
    ang_bnd = np.angle(bnd)
    d = float(np.max(np.abs(ang_raw - ang_bnd)))
    check("el_clip_preserva_la_fase", d < 1e-9, "desvio maximo de fase = " + format(d, ".3e"))

def test_dale_law(pre, w, n):
    """La fase por neurona es valida solo si ninguna neurona mezcla signos."""
    pos = np.bincount(pre, weights=(w > 0).astype(np.float64), minlength=n)
    neg = np.bincount(pre, weights=(w < 0).astype(np.float64), minlength=n)
    has_out = (pos + neg) > 0
    mixed = int(np.sum((pos > 0) & (neg > 0)))
    check("ley_de_Dale_sin_neuronas_mixtas", mixed == 0,
          str(mixed) + " mixtas de " + str(int(np.sum(has_out))) + " con salidas"
          + "  (E puras " + str(int(np.sum(has_out & (neg == 0))))
          + ", I puras " + str(int(np.sum(has_out & (pos == 0)))) + ")")

def test_null_preserves_degree(pre, post, n, bin_of):
    """Los dos nulls preservan el grado entrante. Si no, no son controles."""
    din0 = np.bincount(post, minlength=n)
    dout0 = np.bincount(pre, minlength=n)
    p_cp = null_community_preserving(pre, post, bin_of, seed=1)
    bad_cp = int(np.sum(np.bincount(p_cp, minlength=n) != din0))
    check("CP_preserva_grado_entrante", bad_cp == 0, str(bad_cp) + " nodos alterados de " + str(n))
    uniq_cp = int(np.unique(pre.astype(np.int64) * np.int64(n) + p_cp).shape[0])
    lg("       CP crea " + str(pre.shape[0] - uniq_cp) + " multi-aristas (esperado: el CP las admite)")
    bad_out = int(np.sum(np.bincount(pre, minlength=n) != dout0))
    check("CP_preserva_grado_saliente", bad_out == 0, str(bad_out) + " nodos alterados")
    return p_cp

def test_uniform_choice_would_fail(pre, post, n, bin_of, seed=1):
    """Control del control: el metodo uniforme SI rompe el grado entrante.

    Si este test no diera FAIL en el metodo uniforme, el test anterior no
    estaria midiendo nada.
    """
    rng = np.random.default_rng(seed)
    din0 = np.bincount(post, minlength=n)
    idx = np.where(bin_of[pre] == bin_of[post])[0][:200000]
    if idx.shape[0] < 100:
        lg("       sin bloque suficiente para el control; se omite")
        return
    targets = np.where(bin_of >= 0)[0]
    p = post.copy()
    p[idx] = rng.choice(targets, idx.shape[0])
    bad = int(np.sum(np.bincount(p, minlength=n) != din0))
    check("el_metodo_uniforme_ROMPE_el_grado", bad > 0,
          str(bad) + " nodos alterados -> el test anterior puede fallar, o sea que mide")

# =====================================================================
# 10. EXPERIMENTO - la pregunta falsable
# =====================================================================

N_NULLS = int(os.environ.get("N_NULLS", "9"))
N_STEPS = int(os.environ.get("N_STEPS", "200"))
SNAP = [60, 120, N_STEPS - 1]

def measure_graph(pre, p, w, n, bin_of, n_bins, stim, tau_c, tau_r, label):
    """Mide un grafo con tau COMPLEJA y con tau REAL, en la misma corrida.

    La comparacion pareada dentro del mismo grafo es lo que aisla el aporte
    de la aritmetica compleja: si la ventaja de tau compleja fuera un
    artefacto del grafo, apareceria igual en los nulls.
    """
    W, is_inh = build_complex_weights(pre, p, w, n)
    W, rho, conv = normalize_spectral(W)
    res = {"rho": rho, "rho_convergio": bool(conv),
           "frac_inhibitoria": float(np.mean(is_inh))}
    for tag, tau in (("cplx", tau_c), ("real", tau_r)):
        profs = {t: [] for t in SNAP}
        coh = {t: [] for t in SNAP}
        for mi in stim:
            out, _ = propagate(W, tau, mi, n_steps=N_STEPS, save_at=SNAP)
            for t in SNAP:
                profs[t].append(region_profile(out[t], bin_of, n_bins))
                coh[t].append(phase_coherence(out[t]))
        for t in SNAP:
            val, nv, nx = rdi(profs[t])
            res["rdi_" + tag + "_t" + str(t)] = val
            res["pares_validos_" + tag + "_t" + str(t)] = nv
            res["pares_excluidos_" + tag + "_t" + str(t)] = nx
            res["coh_" + tag + "_t" + str(t)] = float(np.nanmean(coh[t]))
    for t in SNAP:
        a = res["rdi_cplx_t" + str(t)]
        b = res["rdi_real_t" + str(t)]
        res["ventaja_compleja_t" + str(t)] = (a - b) if (not math.isnan(a) and not math.isnan(b)) else float("nan")
    lg("  " + label.ljust(14)
       + "  rho=" + format(rho, ".4f") + ("" if conv else " (NO CONVERGIO)")
       + "  rdi_cplx=" + format(res["rdi_cplx_t" + str(SNAP[-1])], ".4f")
       + "  rdi_real=" + format(res["rdi_real_t" + str(SNAP[-1])], ".4f")
       + "  ventaja=" + format(res["ventaja_compleja_t" + str(SNAP[-1])], "+.4f"))
    return res

def main():
    lg("python " + sys.version.split()[0] + "  numpy " + np.__version__
       + "  scipy " + __import__("scipy").__version__)
    lg("")
    lg("########## TESTS DE UNIDAD ##########")
    test_tau_guard()
    test_activation_bounded()
    lg("")
    lg("########## CARGA Y VERIFICACION DE DATOS ##########")
    D = load_connectome("/kaggle/working/datos")
    pre, post, w, n = D["pre"], D["post"], D["w"], D["n"]
    bin_of, n_bins = D["bin_of"], len(D["bin_names"])
    lg("  N=" + str(n) + "  E=" + str(pre.shape[0]) + "  regiones=" + str(n_bins))
    lg("  poblaciones estimuladas: " + str([(D["mod_names"][i], int(D["stim"][i].shape[0])) for i in range(3)]))
    lg("")
    lg("########## TESTS SOBRE LOS DATOS REALES ##########")
    test_dale_law(pre, w, n)
    test_null_preserves_degree(pre, post, n, bin_of)
    test_uniform_choice_would_fail(pre, post, n, bin_of)
    lg("")
    if FAILURES:
        lg("HAY " + str(len(FAILURES)) + " TESTS EN ROJO: " + ", ".join(FAILURES))
        lg("El experimento NO se corre con invariantes roto.")
        print("FINMOTOR", flush=True)
        return
    lg("########## EXPERIMENTO ##########")
    tau_c, lim = make_tau(n, 0.119, (0.01, 0.15))
    tau_r = np.full(n, 0.119) + 0j
    lg("  tau compleja: Re=0.119  Im en (0.01,0.15)  limite de estabilidad=" + format(lim, ".6f"))
    lg("  tau real: 0.119 + 0j  (el control de la aritmetica compleja)")
    lg("  nulls=" + str(N_NULLS) + "  pasos=" + str(N_STEPS) + "  snapshots=" + str(SNAP))
    lg("")
    real = measure_graph(pre, post, w, n, bin_of, n_bins, D["stim"], tau_c, tau_r, "REAL")
    nulls = []
    for i in range(N_NULLS):
        p = null_community_preserving(pre, post, bin_of, seed=1000 + 7 * i)
        nulls.append(measure_graph(pre, p, w, n, bin_of, n_bins, D["stim"], tau_c, tau_r,
                                   "CP " + str(i + 1) + "/" + str(N_NULLS)))
    names = (["rdi_cplx_t" + str(t) for t in SNAP]
             + ["ventaja_compleja_t" + str(t) for t in SNAP])
    out = global_rank_test(real, nulls, names)
    lg("")
    lg("########## RESULTADO ##########")
    for nm in names:
        d = out["per_statistic"][nm]
        if d["verdict"] == "NO_TESTEABLE":
            lg("  " + nm.ljust(26) + "NO_TESTEABLE  " + d["reason"])
        else:
            lg("  " + nm.ljust(26) + "real=" + format(d["real"], "+.5f")
               + "  null_mu=" + format(d["null_mean"], "+.5f")
               + "  sd=" + format(d["null_sd"], ".5f")
               + "  n_ge=" + str(d["n_ge"]) + "/" + str(N_NULLS)
               + "  p2=" + format(d["p_two"], ".4f"))
    g = out["global"]
    lg("")
    if g is None:
        lg("  TEST GLOBAL: " + out["error"])
    else:
        lg("  TEST GLOBAL sobre " + str(g["k_usable"]) + " de " + str(g["k_total"]) + " estadisticos")
        lg("    S_real=" + format(g["S_real"], ".1f")
           + "  S_null_mu=" + format(g["S_null_mean"], ".1f")
           + "  sd=" + format(g["S_null_sd"], ".1f")
           + "  min=" + format(g["S_null_min"], ".1f"))
        lg("    nulls por debajo=" + str(g["n_below"]) + "/" + str(N_NULLS)
           + "   p dos colas=" + format(g["p_two_sided"], ".4f")
           + "   piso alcanzable=" + format(g["floor"], ".4f"))
    payload = {"meta": {"n": n, "e": int(pre.shape[0]), "md5": D["md5"],
                        "n_nulls": N_NULLS, "n_steps": N_STEPS, "snap": SNAP,
                        "tau_real": 0.119, "tau_imag_range": [0.01, 0.15],
                        "tau_limit": lim, "bin_names": D["bin_names"],
                        "mod_names": D["mod_names"],
                        "stim_sizes": [int(x.shape[0]) for x in D["stim"]]},
               "tests_en_rojo": FAILURES, "real": real, "nulls": nulls,
               "test_global": out}
    f = open("/kaggle/working/motor_resultados.json", "w")
    json.dump(payload, f)
    f.close()
    lg("")
    lg("FIN  tests en rojo=" + str(len(FAILURES)) + "  minutos=" + format((time.time() - T0) / 60.0, ".1f"))
    print("FINMOTOR", flush=True)

if __name__ == "__main__":
    main()
