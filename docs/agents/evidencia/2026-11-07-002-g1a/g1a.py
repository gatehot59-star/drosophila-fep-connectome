# g1a.py: instrumento de G1-A (H_G1_VETO), respuesta 2026-11-07-002 del repo drosophila-fep-connectome.
# Diseno fijado en docs/agents/respuestas/2026-11-04-001-g1-arrancado-diseno-g1a-y-censo.md (commit c89a3388).
# Enmiendas fijadas antes de calibrar: docs/agents/evidencia/2026-11-07-002-g1a/00-enmienda-antes-de-calibrar.md
# Modos:
#   calibrar <mosca> <OUT> [n_rep]: Y sintetica desde el G0 ajustado a la Y real (G0 no mira M), con beta
#       plantado 0; 0,4; 0,7 y 1,1 sobre el M real, 200 replicas por beta. Nunca estima beta con la Y real.
#   cruzar <mosca> <OUT> <sha256 de este archivo> <commit del sello> [cruce_flywire.json]: la prueba real.
#       Se niega a correr si este archivo no es el sellado, si la calibracion no paso o si el banco de
#       recableados no es el mismo que se calibro.
#   leer <OUT>: Holm sobre las dos moscas y la tabla de lectura fijada en 2026-11-04-001.
# Definiciones de S, D, X, signo, tipo y umbrales iguales a g1_censo.py (2026-11-04-001).
import sys, os, json, time, hashlib, platform, warnings
import numpy as np, pandas as pd, scipy
import pyarrow as pa, pyarrow.parquet as pq, pyarrow.feather as pf, pyarrow.compute as pc
from scipy import sparse
from scipy.special import expit
from scipy.stats import binom
warnings.filterwarnings('ignore', category=sparse.SparseEfficiencyWarning)

VERSION = 'g1a 2026-11-07-002'
W_DIR, W_X, W_PESADO, W_LIVIANO = 20, 5, 80, 20
LADOS = ('left', 'right')
N_BANCO, N_REP, BETAS = 1000, 200, (0.0, 0.4, 0.7, 1.1)
SEMILLA_BANCO = {'flywire': 7830711, 'banc': 8880711}
SEMILLA_CAL = {'flywire': 7830712, 'banc': 8880712}
O_FUERA, ALFA, MARGEN_OR, Z95, SESGO_MAX = -50.0, 0.01, 1.5, 1.959963984540054, 0.1
TOL_GRAD, MAX_IT = 1e-6, 100
MD5 = {'/workspace/connectivity.parquet': '3d802fd542b5d18570ba1ba0bb0abed9',
       '/workspace/annotations.tsv': '719904abad876c68ace1b5690c9b9b63',
       '/workspace/banc_888/banc_888_meta.feather': '8c2b93a608c7163ec9d94d68e0756ff4',
       '/workspace/banc_888/banc_888_edgelist_simple_v3.feather': '08542b0771db7418ed474be60dc9886c'}
CENSO = '/workspace/a1/v2/g1/censo/g1_censo.json'
PRIMARIO = {'flywire': ('inh', 'entero', 'pesado'), 'banc': ('inh', 'cerebro', 'pesado')}
SECUNDARIOS = {'flywire': [('exc', 'entero', 'pesado'), ('inh', 'entero', 'liviano')],
               'banc': [('exc', 'cerebro', 'pesado'), ('inh', 'cerebro', 'liviano'), ('inh', 'entero', 'pesado')]}
CLAVE_CENSO = {('inh', 'entero', 'pesado'): 'pesado_inh', ('exc', 'entero', 'pesado'): 'pesado_exc',
               ('inh', 'entero', 'liviano'): 'liviano_inh_sin_pesado',
               ('inh', 'cerebro', 'pesado'): 'pesado_inh_cerebro', ('exc', 'cerebro', 'pesado'): 'pesado_exc_cerebro',
               ('inh', 'cerebro', 'liviano'): 'liviano_inh_sin_pesado_cerebro'}
COLS = ['beta', 'rep', 'n_pares_info', 'n_X_info', 'n_D_info', 'n_Y1', 'n_M1_info', 'n_Y1_en_M', 'esperado_G0_en_M',
        'beta_tilde', 'k_nulo', 'p_nulo', 'beta_hat', 'se_robusto', 'se_modelo', 'regla_se', 'ic_lo', 'ic_hi',
        'll0', 'll1', 'it0', 'it1', 'conv0', 'conv1', 'gmax0', 'gmax1', 'seg_g0', 'seg_nulo', 'seg_g1']
T0 = time.time()


def criterios(n_rep):
    return dict(SESGO_MAX=SESGO_MAX, COB_MIN=int(binom.ppf(0.005, n_rep, 0.95)),
                FP01_MAX=int(binom.ppf(0.995, n_rep, 0.01)), FP05_MAX=int(binom.ppf(0.995, n_rep, 0.05)))


def py(v):
    if isinstance(v, dict):
        return {str(k): py(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [py(x) for x in v]
    if isinstance(v, np.ndarray):
        return [py(x) for x in v.tolist()]
    if isinstance(v, np.bool_):
        return bool(v)
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        return float(v)
    return v


def fmt(v):
    if isinstance(v, (float, np.floating)):
        return '%.10g' % float(v)
    return str(py(v))


def mem():
    d = {}
    for l in open('/proc/self/status'):
        k = l.split(':')[0]
        if k in ('VmRSS', 'VmHWM'):
            d[k + '_MiB'] = round(int(l.split()[1]) / 1024, 1)
    return d


class Bitacora:
    def __init__(self, ruta):
        self.f = open(ruta, 'w')

    def __call__(self, etapa, **extra):
        e = dict(etapa=etapa, s=round(time.time() - T0, 2))
        e.update(mem())
        e.update(py(extra))
        self.f.write(json.dumps(e, sort_keys=True) + chr(10))
        self.f.flush()


def huella(p):
    h5, h2 = hashlib.md5(), hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h5.update(b)
            h2.update(b)
    return dict(ruta=p, bytes=os.path.getsize(p), md5=h5.hexdigest(), sha256=h2.hexdigest())


def sha_archivo(p):
    with open(p, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def entorno():
    return dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                pandas=pd.__version__, pyarrow=pa.__version__, host=platform.node(),
                OMP_NUM_THREADS=os.environ.get('OMP_NUM_THREADS'))


def col(path, c, dt):
    return pq.read_table(path, columns=[c]).column(c).to_numpy().astype(dt)


def cargar(mosca):
    if mosca == 'flywire':
        entradas = ['/workspace/connectivity.parquet', '/workspace/annotations.tsv']
    else:
        entradas = ['/workspace/banc_888/banc_888_meta.feather', '/workspace/banc_888/banc_888_edgelist_simple_v3.feather']
    hs = [huella(p) for p in entradas]
    for h in hs:
        if h['md5'] != MD5[h['ruta']]:
            raise SystemExit('md5 distinto del fijado: ' + h['ruta'])
    if mosca == 'flywire':
        conn, annot = entradas
        pre = col(conn, 'Presynaptic_Index', np.int32)
        post = col(conn, 'Postsynaptic_Index', np.int32)
        n = int(max(pre.max(), post.max())) + 1
        rid = np.zeros(n, dtype=np.int64)
        rid[pre] = col(conn, 'Presynaptic_ID', np.int64)
        rid[post] = col(conn, 'Postsynaptic_ID', np.int64)
        w = col(conn, 'Connectivity', np.int32)
        exc = col(conn, 'Excitatory', np.int8)
        inh = np.zeros(n, dtype=bool)
        inh[pre[exc < 0]] = True
        del exc
        a = pd.read_csv(annot, sep=chr(9), dtype=str, usecols=['root_id', 'cell_type', 'side', 'super_class'])
        a['root_id'] = a.root_id.astype(np.int64)
        a = a.drop_duplicates('root_id').set_index('root_id').reindex(rid)
        g = dict(pre=pre, post=post, w=w, inh=inh, tipo=a.cell_type.to_numpy(dtype=object),
                 lado=a.side.to_numpy(dtype=object), sc=a.super_class.to_numpy(dtype=object), n=n)
    else:
        meta, ar = entradas
        m = pd.read_feather(meta, columns=['root_888', 'side', 'super_class', 'cell_type', 'fafb_cell_type',
                                           'neurotransmitter_predicted', 'region'])
        m = m.drop_duplicates('root_888').reset_index(drop=True)
        vs = pa.array(m.root_888.astype(str).to_numpy())
        t = pf.read_table(ar, columns=['pre', 'post', 'count'], memory_map=True)
        pre = pc.index_in(t.column('pre'), value_set=vs).fill_null(-1).to_numpy().astype(np.int32)
        post = pc.index_in(t.column('post'), value_set=vs).fill_null(-1).to_numpy().astype(np.int32)
        w = t.column('count').to_numpy().astype(np.int32)
        del t
        if (pre < 0).any() or (post < 0).any():
            raise SystemExit('aristas de BANC con ids fuera del meta')
        inh = m.neurotransmitter_predicted.isin(['gaba', 'glutamate']).to_numpy()
        tipo = m.fafb_cell_type.where(m.fafb_cell_type.notna(), m.cell_type).to_numpy(dtype=object)
        g = dict(pre=pre, post=post, w=w, inh=inh, tipo=tipo, lado=m.side.to_numpy(dtype=object),
                 sc=m.super_class.to_numpy(dtype=object), n=len(m),
                 cerebro=(m.region.to_numpy(dtype=object) != 'ventral_nerve_cord'))
    g['huellas'] = hs
    return g


def unidades(tipo, lado, mask, n):
    claves = sorted(set(zip(tipo[mask], lado[mask])))
    idx = {k: i for i, k in enumerate(claves)}
    u = np.full(n, -1, dtype=np.int32)
    for j in np.nonzero(mask)[0]:
        u[j] = idx[(tipo[j], lado[j])]
    return u, claves


def base_mosca(g):
    pre, post, w, tipo, lado, sc, n = (g[k] for k in ('pre', 'post', 'w', 'tipo', 'lado', 'sc', 'n'))
    ok = pd.notna(tipo) & np.isin(lado, LADOS)
    S, cs = unidades(tipo, lado, (sc == 'visual_projection') & ok, n)
    D, cd = unidades(tipo, lado, (sc == 'descending') & ok, n)
    nS, nD = len(cs), len(cd)
    m = (S[pre] >= 0) & (D[post] >= 0)
    agg = np.bincount(S[pre[m]].astype(np.int64) * nD + D[post[m]], weights=w[m], minlength=nS * nD).reshape(nS, nD)
    ls = np.array([k[1] for k in cs], dtype=object)
    ld = np.array([k[1] for k in cd], dtype=object)
    cab = (agg >= W_DIR) & (ls[:, None] == ld[None, :])
    return dict(S=S, D=D, nS=nS, nD=nD, excl=(S >= 0) | (D >= 0), ls=ls, ld=ld, cab=cab, E=np.argwhere(cab),
                lado_d=np.array([LADOS.index(s) for s in ld], dtype=np.int64))


def M_de(es, ed, nS, nD, Drs, px, pdd):
    C = sparse.csr_matrix((np.ones(len(es)), (es, ed)), shape=(nS, nD))
    co = (C.T @ C).tocsr()
    co.setdiag(0)
    co.eliminate_zeros()
    A = (Drs @ co).toarray()
    return A[px, pdd] > 0


def grupo(g, b, signo, alcance, clase):
    pre, post, w, inh, n = g['pre'], g['post'], g['w'], g['inh'], g['n']
    D, nD, excl = b['D'], b['nD'], b['excl']
    xinh = inh & ~excl
    xsig = xinh if signo == 'inh' else (~inh & ~excl)
    dx = D[pre] >= 0
    if clase == 'pesado':
        sel = dx & xsig[post] & (w >= W_PESADO)
    else:
        pes = np.zeros(n, dtype=bool)
        pes[post[dx & xinh[post] & (w >= W_PESADO)]] = True
        sel = dx & xsig[post] & (w >= W_LIVIANO) & (w < W_PESADO) & ~pes[post]
    if alcance == 'cerebro':
        sel = sel & g['cerebro'][post]
    dr = np.unique(post[sel].astype(np.int64) * nD + D[pre[sel]])
    xs = np.unique(dr // nD)
    nX = len(xs)
    Dr = np.zeros((nX, nD), dtype=bool)
    Dr[np.searchsorted(xs, dr // nD), dr % nD] = True
    xset = np.zeros(n, dtype=bool)
    xset[xs] = True
    s2 = xset[pre] & (D[post] >= 0)
    k = pre[s2].astype(np.int64) * nD + D[post[s2]]
    u, inv = np.unique(k, return_inverse=True)
    sw = np.bincount(inv, weights=w[s2])
    yk = u[sw >= W_X]
    Ym = np.zeros((nX, nD), dtype=bool)
    Ym[np.searchsorted(xs, yk // nD), yk % nD] = True
    libre = ~Dr.reshape(-1)
    px = np.repeat(np.arange(nX, dtype=np.int64), nD)[libre]
    pdd = np.tile(np.arange(nD, dtype=np.int64), nX)[libre]
    Lx = np.zeros((nX, len(LADOS)), dtype=bool)
    xi, di = np.nonzero(Dr)
    Lx[xi, b['lado_d'][di]] = True
    Drs = sparse.csr_matrix(Dr.astype(np.float64))
    M = M_de(b['E'][:, 0], b['E'][:, 1], b['nS'], nD, Drs, px, pdd)
    return dict(clave=(signo, alcance, clase), xs=xs, nX=nX, nD=nD, px=px, pdd=pdd,
                y=Ym[px, pdd].astype(np.int8), L=Lx[px, b['lado_d'][pdd]].astype(np.int8), M=M, Drs=Drs)


def cuentas(gr, b):
    return dict(n_X=int(gr['nX']), n_pares=int(len(gr['px'])), n_Y1=int(gr['y'].sum()), n_M1=int(gr['M'].sum()),
                n_L1=int(gr['L'].sum()), n_cab=int(b['cab'].sum()))


def chequeo_censo(mosca, clave, cu, abortar=True):
    c = json.load(open(CENSO))
    cm = c[mosca][CLAVE_CENSO[tuple(clave)]]
    ok = dict(n_X=cm['n_X'] == cu['n_X'], n_pares=cm['n_pares'] == cu['n_pares'], n_Y1=cm['n_Y1_marginal'] == cu['n_Y1'],
              n_M1=cm['n_M1_marginal'] == cu['n_M1'], n_L1=cm['n_L1_marginal'] == cu['n_L1'],
              n_cab=c[mosca]['n_pares_S_D_cableados'] == cu['n_cab'])
    if abortar and not all(ok.values()):
        raise SystemExit('no cuadra con el censo: ' + json.dumps(py(dict(clave=list(clave), cuentas=cu, ok=ok))))
    return ok


def recablear(E, lado_e, nD, rng):
    es = E[:, 0].tolist()
    ed = E[:, 1].tolist()
    claves = set(s * nD + d for s, d in zip(es, ed))
    hechos = 0
    for l in range(len(LADOS)):
        idx = np.nonzero(lado_e == l)[0]
        m = len(idx)
        if m < 2:
            continue
        ii = idx[rng.integers(0, m, size=10 * m)].tolist()
        jj = idx[rng.integers(0, m, size=10 * m)].tolist()
        for i, j in zip(ii, jj):
            s1, d1, s2, d2 = es[i], ed[i], es[j], ed[j]
            if s1 == s2 or d1 == d2:
                continue
            k1 = s1 * nD + d2
            k2 = s2 * nD + d1
            if k1 in claves or k2 in claves:
                continue
            claves.discard(s1 * nD + d1)
            claves.discard(s2 * nD + d2)
            claves.add(k1)
            claves.add(k2)
            ed[i] = d2
            ed[j] = d1
            hechos += 1
    return np.array(es, dtype=np.int32), np.array(ed, dtype=np.int32), hechos


def banco(b, mosca, n=N_BANCO, semilla=None):
    rng = np.random.default_rng(SEMILLA_BANCO[mosca] if semilla is None else semilla)
    E, nS, nD = b['E'], b['nS'], b['nD']
    lado_e = np.array([LADOS.index(s) for s in b['ls'][E[:, 0]]], dtype=np.int64)
    gs0, gd0 = np.bincount(E[:, 0], minlength=nS), np.bincount(E[:, 1], minlength=nD)
    real = set((E[:, 0].astype(np.int64) * nD + E[:, 1]).tolist())
    h = hashlib.sha256()
    tablas, hechos, comun, ok = [], [], [], 0
    for r in range(n):
        es, ed, hh = recablear(E, lado_e, nD, rng)
        tablas.append((es, ed))
        hechos.append(hh)
        h.update(es.tobytes())
        h.update(ed.tobytes())
        k = (es.astype(np.int64) * nD + ed).tolist()
        ok += int(np.array_equal(np.bincount(es, minlength=nS), gs0) and np.array_equal(np.bincount(ed, minlength=nD), gd0)
                  and len(set(k)) == len(k) and bool((b['ls'][es] == b['ld'][ed]).all()))
        comun.append(len(real.intersection(k)) / len(k))
    return dict(tablas=tablas, sha256=h.hexdigest(), n=n, semilla=SEMILLA_BANCO[mosca] if semilla is None else semilla,
                chequeos_ok=ok, n_aristas=int(len(E)), intercambios_media=round(float(np.mean(hechos)), 1),
                fraccion_aristas_reales_media=round(float(np.mean(comun)), 4))


def lote(listas):
    lens = np.array([len(a) for a in listas], dtype=np.int64)
    return dict(seg=np.repeat(np.arange(len(listas), dtype=np.int32), lens),
                idx=np.concatenate([np.asarray(a, dtype=np.int32) for a in listas]), R=len(listas), lens=lens)


def lote_de_banco(gr, b, bk):
    return lote([np.nonzero(M_de(es, ed, b['nS'], b['nD'], gr['Drs'], gr['px'], gr['pdd']))[0] for es, ed in bk['tablas']])


def beta_tilde_lote(o, y, keep, lt):
    # beta con theta, phi y gamma fijos en el ajuste de G0 (o), uno por lista de pares M=1
    seg, idx, R = lt['seg'], lt['idx'], lt['R']
    oo = o[idx]
    k = np.bincount(seg, y[idx], R)
    nk = np.bincount(seg, keep[idx].astype(np.float64), R)
    act = (k > 0) & (k < nk)
    b = np.zeros(R)
    paso = np.zeros(R)
    it = 0
    for it in range(1, 201):
        p = expit(oo + b[seg])
        s1 = np.bincount(seg, p, R)
        s2 = np.bincount(seg, p * (1.0 - p), R)
        paso = np.where(act, np.clip((s1 - k) / np.maximum(s2, 1e-300), -5.0, 5.0), 0.0)
        b = b - paso
        if np.abs(paso).max() < 1e-10:
            break
    b = np.where(act, b, np.where(k == 0, -np.inf, np.inf))
    return b, it, float(np.abs(paso).max())


def bloques(ix, jd, Z, w, nx, nd):
    # Hessiano por bloques: a = (theta, columnas de Z); phi sin su primer D (gauge) queda diagonal
    k = Z.shape[1]
    Wz = Z * w[:, None]
    A = np.zeros((nx + k, nx + k))
    A[np.arange(nx), np.arange(nx)] = np.bincount(ix, w, nx)
    Bxc = np.stack([np.bincount(ix, Wz[:, j], nx) for j in range(k)], axis=1)
    A[:nx, nx:] = Bxc
    A[nx:, :nx] = Bxc.T
    A[nx:, nx:] = Z.T @ Wz
    Bxp = np.bincount(ix * nd + jd, w, nx * nd).reshape(nx, nd)
    Bcp = np.stack([np.bincount(jd, Wz[:, j], nd) for j in range(k)], axis=0)
    return A, np.vstack([Bxp[:, 1:], Bcp[:, 1:]]), np.bincount(jd, w, nd)[1:]


def ajustar(ix, jd, Z, y, nx, nd, off=None, ini=None):
    # logit P(Y=1) = off + theta_x + phi_D + Z c, con phi del primer D fijo en 0; Newton por bloques con busqueda lineal
    k = Z.shape[1]
    off = np.zeros(len(y)) if off is None else off
    if ini is None:
        th, ph, c = np.zeros(nx), np.zeros(nd), np.zeros(k)
    else:
        th, ph, c = (np.array(v, dtype=np.float64) for v in ini)
        th, ph = th + ph[0], ph - ph[0]
    eta = off + th[ix] + ph[jd] + Z @ c
    ll = float(y @ eta - np.logaddexp(0.0, eta).sum())
    conv, gmax, it = False, float('inf'), 0
    for it in range(1, MAX_IT + 1):
        p = expit(eta)
        w = p * (1.0 - p)
        r = y - p
        ga = np.concatenate([np.bincount(ix, r, nx), Z.T @ r])
        gp = np.bincount(jd, r, nd)[1:]
        gmax = float(max(np.abs(ga).max(), np.abs(gp).max() if len(gp) else 0.0))
        if gmax < TOL_GRAD:
            conv = True
            break
        A, B, Dg = bloques(ix, jd, Z, w, nx, nd)
        BD = B / Dg
        da = np.linalg.solve(A - BD @ B.T, ga - BD @ gp)
        dph = np.concatenate([[0.0], (gp - B.T @ da) / Dg])
        dth, dc = da[:nx], da[nx:]
        t = 1.0
        while True:
            eta_n = off + (th + t * dth)[ix] + (ph + t * dph)[jd] + Z @ (c + t * dc)
            ll_n = float(y @ eta_n - np.logaddexp(0.0, eta_n).sum())
            if ll_n >= ll - 1e-10 * abs(ll) - 1e-9 or t < 1e-8:
                break
            t *= 0.5
        th, ph, c, eta, ll = th + t * dth, ph + t * dph, c + t * dc, eta_n, ll_n
    return dict(th=th, ph=ph, c=c, eta=eta, ll=ll, it=it, conv=conv, gmax=gmax)


def se_beta(ix, jd, Z, y, eta, nx, nd, j):
    # error estandar de la columna j de Z: modelo (inversa del Hessiano) y robusto a dos vias (x y D)
    p = expit(eta)
    w = p * (1.0 - p)
    r = y - p
    A, B, Dg = bloques(ix, jd, Z, w, nx, nd)
    BD = B / Dg
    e = np.zeros(nx + Z.shape[1])
    e[nx + j] = 1.0
    ha = np.linalg.solve(A - BD @ B.T, e)
    hp = np.concatenate([[0.0], -(B.T @ ha) / Dg])
    psi = r * (ha[:nx][ix] + hp[jd] + Z @ ha[nx:])
    Vx = float((np.bincount(ix, psi, nx) ** 2).sum())
    Vd = float((np.bincount(jd, psi, nd) ** 2).sum())
    V0 = float((psi ** 2).sum())
    cx, cd = nx / (nx - 1.0), nd / (nd - 1.0)
    V, regla = cx * Vx + cd * Vd - V0, 'dos_vias'
    if V <= 0:
        V, regla = max(cx * Vx, cd * Vd), 'max_una_via'
    return dict(se_robusto=float(np.sqrt(V)), se_modelo=float(np.sqrt(ha[nx + j])), V_x=Vx, V_d=Vd, V_0=V0, regla=regla)


def analizar(y, gr, lr, ln, ini=None):
    px, pdd, nX, nD = gr['px'], gr['pdd'], gr['nX'], gr['nD']
    yf = y.astype(np.float64)
    kx = np.bincount(px, yf, nX) > 0
    kd = np.bincount(pdd, yf, nD) > 0
    keep = kx[px] & kd[pdd]
    mx, md = np.cumsum(kx) - 1, np.cumsum(kd) - 1
    ix, jd = mx[px[keep]], md[pdd[keep]]
    nxk, ndk = int(kx.sum()), int(kd.sum())
    yk = yf[keep]
    Lk = gr['L'][keep].astype(np.float64)
    Mk = gr['M'][keep].astype(np.float64)
    ini0 = None if ini is None else (ini[0][kx], ini[1][kd], np.asarray(ini[2])[:1])
    t0 = time.time()
    f0 = ajustar(ix, jd, Lk[:, None], yk, nxk, ndk, ini=ini0)
    t_g0 = time.time() - t0
    o = np.full(len(px), O_FUERA)
    o[keep] = f0['eta']
    bt = float(beta_tilde_lote(o, yf, keep, lr)[0][0])
    t1 = time.time()
    bn, it_n, res_n = beta_tilde_lote(o, yf, keep, ln)
    t_nulo = time.time() - t1
    k_nulo = int((bn >= bt).sum())
    p = (k_nulo + 1.0) / (ln['R'] + 1.0)
    m1, y1m = int(Mk.sum()), int(yk[Mk > 0].sum())
    n_info = int(keep.sum())
    nan = float('nan')
    fn = np.isfinite(bn)
    fin = dict(n_pares_info=n_info, n_X_info=nxk, n_D_info=ndk, n_X_fuera=int(nX - nxk), n_D_fuera=int(nD - ndk),
               n_Y1=int(yk.sum()), n_M1_info=m1, n_Y1_en_M=y1m, esperado_G0_en_M=float(expit(f0['eta'])[Mk > 0].sum()),
               beta_tilde=bt, k_nulo=k_nulo, p_nulo=p, it0=f0['it'], conv0=f0['conv'], gmax0=f0['gmax'], ll0=f0['ll'],
               gamma_G0=float(f0['c'][0]), seg_g0=round(t_g0, 4), seg_nulo=round(t_nulo, 4), it_nulo=it_n,
               residuo_nulo=res_n,
               nulo=dict(n=int(ln['R']), n_no_finitos=int((~fn).sum()),
                         media=float(bn[fn].mean()) if fn.any() else nan, de=float(bn[fn].std()) if fn.any() else nan,
                         q50=float(np.quantile(bn[fn], 0.5)) if fn.any() else nan,
                         q95=float(np.quantile(bn[fn], 0.95)) if fn.any() else nan,
                         q99=float(np.quantile(bn[fn], 0.99)) if fn.any() else nan))
    aux = dict(ix=ix, jd=jd, Lk=Lk, Mk=Mk, yk=yk, nxk=nxk, ndk=ndk, keep=keep, o=o, f0=f0, f1=None)
    if m1 == 0 or y1m == 0 or y1m == m1:
        fin.update(beta_hat=nan, se_robusto=nan, se_modelo=nan, regla_se='no_estimable', ic_lo=nan, ic_hi=nan,
                   OR=nan, OR_lo=nan, OR_hi=nan, ll1=nan, it1=0, conv1=False, gmax1=nan, gamma_G1=nan, seg_g1=0.0,
                   bits_G1_menos_G0=nan)
        return fin, aux
    t2 = time.time()
    Z1 = np.column_stack([Lk, Mk])
    f1 = ajustar(ix, jd, Z1, yk, nxk, ndk, ini=(f0['th'], f0['ph'], np.array([f0['c'][0], bt if np.isfinite(bt) else 0.0])))
    se = se_beta(ix, jd, Z1, yk, f1['eta'], nxk, ndk, 1)
    t_g1 = time.time() - t2
    b1, s = float(f1['c'][1]), se['se_robusto']
    lo, hi = b1 - Z95 * s, b1 + Z95 * s
    fin.update(beta_hat=b1, se_robusto=s, se_modelo=se['se_modelo'], regla_se=se['regla'], V_x=se['V_x'], V_d=se['V_d'],
               V_0=se['V_0'], ic_lo=lo, ic_hi=hi, OR=float(np.exp(b1)), OR_lo=float(np.exp(lo)), OR_hi=float(np.exp(hi)),
               ll1=f1['ll'], it1=f1['it'], conv1=f1['conv'], gmax1=f1['gmax'], gamma_G1=float(f1['c'][0]),
               seg_g1=round(t_g1, 4), bits_G1_menos_G0=float((f1['ll'] - f0['ll']) / np.log(2) - 0.5 * np.log2(n_info)))
    aux['f1'] = f1
    return fin, aux


def resumir(filas, n_rep):
    cr = criterios(n_rep)
    out = {}
    nan = float('nan')
    for beta in BETAS:
        F = [f for f in filas if f['beta'] == beta]
        v = {c: np.array([f[c] for f in F], dtype=np.float64)
             for c in ('beta_hat', 'ic_lo', 'ic_hi', 'p_nulo', 'beta_tilde', 'se_robusto', 'se_modelo')}
        bh, lo, hi, p, bt = v['beta_hat'], v['ic_lo'], v['ic_hi'], v['p_nulo'], v['beta_tilde']
        fin = np.isfinite(bh) & np.isfinite(lo) & np.isfinite(hi)
        conv = bool(all(f['conv0'] and f['conv1'] for f in F))
        sesgo = float(bh[fin].mean() - beta) if fin.all() else nan
        cob = int(((lo <= beta) & (beta <= hi) & fin).sum())
        n01, n05, n005 = int((p < 0.01).sum()), int((p < 0.05).sum()), int((p < 0.005).sum())
        comp = int(((p < 0.005) & fin & (np.exp(bh) >= MARGEN_OR) & (np.exp(lo) > 1.0)).sum())
        fb = np.isfinite(bt)
        d = dict(n=len(F), n_finitos=int(fin.sum()), todos_convergen=conv,
                 media_beta_hat=float(bh[fin].mean()) if fin.any() else nan, sesgo=sesgo,
                 de_beta_hat=float(bh[fin].std()) if fin.any() else nan,
                 media_se_robusto=float(v['se_robusto'][fin].mean()) if fin.any() else nan,
                 media_se_modelo=float(v['se_modelo'][fin].mean()) if fin.any() else nan,
                 cobertura=cob, n_p_menor_001=n01, n_p_menor_005=n05, n_p_menor_0005=n005,
                 potencia_p=n005 / len(F), potencia_completa=comp / len(F),
                 media_beta_tilde=float(bt[fb].mean()) if fb.any() else nan,
                 de_beta_tilde=float(bt[fb].std()) if fb.any() else nan, n_beta_tilde_no_finito=int((~fb).sum()),
                 pasa_sesgo=bool(fin.all() and abs(sesgo) < cr['SESGO_MAX']), pasa_cobertura=bool(cob >= cr['COB_MIN']),
                 pasa_convergencia=conv)
        if beta == 0.0:
            d['pasa_falsos_positivos'] = bool(n01 <= cr['FP01_MAX'] and n05 <= cr['FP05_MAX'])
        out['%.1f' % beta] = d
    pasa = bool(all(x for d in out.values() for kk, x in d.items() if kk.startswith('pasa_')))
    return out, pasa


def calibrar(mosca, OUT, n_rep=N_REP):
    propio = sha_archivo(os.path.abspath(__file__))
    bit = Bitacora(os.path.join(OUT, 'cal_%s.log' % mosca))
    bit('inicio', version=VERSION, mosca=mosca, sha256_instrumento=propio, n_rep=n_rep)
    g = cargar(mosca)
    bit('mosca_cargada', n_neuronas=int(g['n']), n_aristas=int(len(g['pre'])))
    b = base_mosca(g)
    cl = PRIMARIO[mosca]
    gr = grupo(g, b, *cl)
    cu = cuentas(gr, b)
    chequeo_censo(mosca, cl, cu)
    hs = g['huellas']
    del g
    bit('grupo', clave='_'.join(cl), **cu)
    bk = banco(b, mosca)
    bit('banco', sha256=bk['sha256'], chequeos_ok=bk['chequeos_ok'], intercambios_media=bk['intercambios_media'],
        fraccion_aristas_reales_media=bk['fraccion_aristas_reales_media'])
    ln = lote_de_banco(gr, b, bk)
    lr = lote([np.nonzero(gr['M'])[0]])
    bit('banco_M', M1_media=float(ln['lens'].mean()), M1_min=int(ln['lens'].min()), M1_max=int(ln['lens'].max()))
    # G0 con la Y real, que no mira M; la Y real se borra del grupo antes de simular
    yr = gr['y'].astype(np.float64)
    gr['y'] = None
    nX, nD, px, pdd = gr['nX'], gr['nD'], gr['px'], gr['pdd']
    kx = np.bincount(px, yr, nX) > 0
    kd = np.bincount(pdd, yr, nD) > 0
    keep = kx[px] & kd[pdd]
    mx, md = np.cumsum(kx) - 1, np.cumsum(kd) - 1
    f0 = ajustar(mx[px[keep]], md[pdd[keep]], gr['L'][keep].astype(np.float64)[:, None], yr[keep],
                 int(kx.sum()), int(kd.sum()))
    o0 = np.full(len(px), O_FUERA)
    o0[keep] = f0['eta']
    thf = np.zeros(nX)
    thf[kx] = f0['th']
    phf = np.zeros(nD)
    phf[kd] = f0['ph']
    ini = (thf, phf, f0['c'])
    g0 = dict(n_pares_info=int(keep.sum()), n_X_info=int(kx.sum()), n_D_info=int(kd.sum()), it=f0['it'],
              conv=f0['conv'], gmax=f0['gmax'], ll=f0['ll'], gamma=float(f0['c'][0]))
    del yr
    bit('g0_con_y_real', **g0)
    M = gr['M'].astype(np.float64)
    filas = []
    ruta_csv = os.path.join(OUT, 'cal_%s_replicas.csv' % mosca)
    with open(ruta_csv, 'w') as fc:
        fc.write(','.join(COLS) + chr(10))
        for beta in BETAS:
            rng = np.random.default_rng([SEMILLA_CAL[mosca], int(round(beta * 10))])
            pr = expit(o0 + beta * M)
            for r in range(n_rep):
                ys = (rng.random(len(pr)) < pr).astype(np.int8)
                fila = dict(beta=beta, rep=r)
                fila.update(analizar(ys, gr, lr, ln, ini)[0])
                fc.write(','.join(fmt(fila[c]) for c in COLS) + chr(10))
                fc.flush()
                filas.append(fila)
            bit('beta_hecho', beta=beta)
    resumen, pasa = resumir(filas, n_rep)
    out = dict(version=VERSION, mosca=mosca, grupo='_'.join(cl), sha256_instrumento=propio, n_rep=n_rep,
               betas=list(BETAS), semilla_cal=SEMILLA_CAL[mosca], criterios=criterios(n_rep), cuentas=cu,
               g0_con_y_real=g0, banco={k: v for k, v in bk.items() if k != 'tablas'},
               banco_M=dict(M1_media=float(ln['lens'].mean()), M1_min=int(ln['lens'].min()), M1_max=int(ln['lens'].max())),
               resumen=resumen, pasa=pasa, sha256_replicas=sha_archivo(ruta_csv), huellas=hs, entorno=entorno(),
               segundos_total=round(time.time() - T0, 1))
    with open(os.path.join(OUT, 'cal_%s.json' % mosca), 'w') as f:
        json.dump(py(out), f, indent=1, sort_keys=True)
    bit('FIN', pasa=pasa)


def cruzar(mosca, OUT, sha_esperado, commit_sello, json_fw=None):
    propio = sha_archivo(os.path.abspath(__file__))
    if propio != sha_esperado:
        raise SystemExit('este g1a.py no es el sellado: ' + propio)
    cal = json.load(open(os.path.join(OUT, 'cal_%s.json' % mosca)))
    if cal['sha256_instrumento'] != propio or not cal['pasa'] or cal['n_rep'] != N_REP:
        raise SystemExit('la calibracion no habilita el cruce')
    bit = Bitacora(os.path.join(OUT, 'cruce_%s.log' % mosca))
    bit('inicio', version=VERSION, mosca=mosca, sha256_instrumento=propio, commit_sello=commit_sello)
    g = cargar(mosca)
    bit('mosca_cargada', n_neuronas=int(g['n']), n_aristas=int(len(g['pre'])))
    b = base_mosca(g)
    grupos = []
    for cl in [PRIMARIO[mosca]] + SECUNDARIOS[mosca]:
        gr = grupo(g, b, *cl)
        cu = cuentas(gr, b)
        chequeo_censo(mosca, cl, cu)
        grupos.append((cl, gr, cu))
        bit('grupo', clave='_'.join(cl), **cu)
    hs = g['huellas']
    del g
    bk = banco(b, mosca)
    if bk['sha256'] != cal['banco']['sha256']:
        raise SystemExit('banco distinto del calibrado')
    bit('banco', sha256=bk['sha256'], chequeos_ok=bk['chequeos_ok'])
    res, costo = {}, {}
    for cl, gr, cu in grupos:
        t0 = time.time()
        nombre = '_'.join(cl)
        ln = lote_de_banco(gr, b, bk)
        lr = lote([np.nonzero(gr['M'])[0]])
        fin, aux = analizar(gr['y'], gr, lr, ln)
        res[nombre] = dict(cuentas=cu, **fin)
        if mosca == 'banc' and cl == PRIMARIO['banc'] and json_fw:
            fw = json.load(open(json_fw))
            bfw = fw['grupos']['_'.join(PRIMARIO['flywire'])]['beta_hat']
            tr = dict(beta_flywire=bfw)
            if np.isfinite(bfw):
                f0 = aux['f0']
                ft = ajustar(aux['ix'], aux['jd'], aux['Lk'][:, None], aux['yk'], aux['nxk'], aux['ndk'],
                             off=bfw * aux['Mk'], ini=(f0['th'], f0['ph'], f0['c']))
                n1 = float(aux['yk'].sum())
                tr.update(ll_G0=f0['ll'], ll_con_beta_flywire=ft['ll'], conv=ft['conv'], it=ft['it'],
                          bits=float((ft['ll'] - f0['ll']) / np.log(2)),
                          bits_por_positivo=float((ft['ll'] - f0['ll']) / np.log(2) / n1))
                if aux['f1'] is not None:
                    tr['bits_G1_propio_por_positivo'] = float((aux['f1']['ll'] - f0['ll']) / np.log(2) / n1)
            res[nombre]['transferencia'] = tr
        costo[nombre] = dict(segundos=round(time.time() - t0, 2), **mem())
        bit('grupo_cruzado', clave=nombre)
    out = dict(version=VERSION, mosca=mosca, sha256_instrumento=propio, commit_sello=commit_sello, grupos=res,
               costo=costo, banco={k: v for k, v in bk.items() if k != 'tablas'}, huellas=hs, entorno=entorno(),
               segundos_total=round(time.time() - T0, 1))
    with open(os.path.join(OUT, 'cruce_%s.json' % mosca), 'w') as f:
        json.dump(py(out), f, indent=1, sort_keys=True)
    bit('FIN')


def holm(pv):
    orden = sorted(pv, key=lambda m: pv[m])
    adj, prev = {}, 0.0
    for i, m in enumerate(orden):
        prev = max(prev, min(1.0, (len(pv) - i) * pv[m]))
        adj[m] = prev
    return adj


def diferencia(a, b):
    d = a['beta_hat'] - b['beta_hat']
    s = (a['se_robusto'] ** 2 + b['se_robusto'] ** 2) ** 0.5
    lo, hi = d - Z95 * s, d + Z95 * s
    if not (np.isfinite(lo) and np.isfinite(hi)):
        lec = 'no_estimable'
    elif lo > 0:
        lec = 'otro_menor'
    elif hi < 0:
        lec = 'otro_mayor'
    else:
        lec = 'no_distinguible'
    return dict(beta_primario=a['beta_hat'], beta_otro=b['beta_hat'], delta=d, se=s, ic_lo=lo, ic_hi=hi, lectura=lec)


def leer(OUT):
    moscas = ('flywire', 'banc')
    cal = {m: json.load(open(os.path.join(OUT, 'cal_%s.json' % m))) for m in moscas}
    cru = {m: json.load(open(os.path.join(OUT, 'cruce_%s.json' % m))) for m in moscas}
    shas = set([cal[m]['sha256_instrumento'] for m in moscas] + [cru[m]['sha256_instrumento'] for m in moscas])
    sellos = set(cru[m]['commit_sello'] for m in moscas)
    cal_ok = all(cal[m]['pasa'] and cal[m]['n_rep'] == N_REP for m in moscas)
    prim = {m: cru[m]['grupos']['_'.join(PRIMARIO[m])] for m in moscas}
    pv = {m: prim[m]['p_nulo'] for m in moscas}
    ph = holm(pv)
    est = {}
    for m in moscas:
        r = prim[m]
        est[m] = dict(p=pv[m], p_holm=ph[m], beta_hat=r['beta_hat'], se_robusto=r['se_robusto'], OR=r['OR'],
                      OR_lo=r['OR_lo'], OR_hi=r['OR_hi'], n_Y1_en_M=r['n_Y1_en_M'], esperado_G0_en_M=r['esperado_G0_en_M'],
                      pasa=bool(ph[m] < ALFA and r['OR'] >= MARGEN_OR and r['OR_lo'] > 1.0),
                      ic_debajo=bool(r['OR_hi'] < MARGEN_OR), ic_incluye=bool(r['OR_lo'] <= MARGEN_OR <= r['OR_hi']))
    if len(shas) != 1 or len(sellos) != 1 or not cal_ok:
        V = 'INVALIDO'
    elif est['flywire']['pasa'] and est['banc']['pasa']:
        V = 'SOSTENIDA'
    elif est['flywire']['pasa'] and est['banc']['ic_incluye']:
        V = 'SOSTENIDA_EN_FLYWIRE'
    elif est['flywire']['pasa'] and est['banc']['ic_debajo']:
        V = 'NO_REPLICA'
    elif est['flywire']['ic_debajo'] and est['banc']['ic_debajo']:
        V = 'REFUTADA'
    else:
        V = 'SIN_DECIDIR'
    sec = {}
    for m in moscas:
        G = cru[m]['grupos']
        al = 'entero' if m == 'flywire' else 'cerebro'
        base = G['_'.join(PRIMARIO[m])]
        sec[m] = dict(dosis=diferencia(base, G['inh_%s_liviano' % al]), especificidad=diferencia(base, G['exc_%s_pesado' % al]),
                      descripcion_bits=base['bits_G1_menos_G0'])
    be = cru['banc']['grupos']['inh_entero_pesado']
    sec['banc']['banc_entero'] = {k: be[k] for k in ('beta_hat', 'se_robusto', 'OR', 'OR_lo', 'OR_hi', 'p_nulo',
                                                     'n_Y1_en_M', 'esperado_G0_en_M')}
    sec['banc']['transferencia'] = prim['banc'].get('transferencia')
    out = dict(version=VERSION, veredicto=V, instrumento_unico=len(shas) == 1, sello_unico=len(sellos) == 1,
               calibracion_ok=cal_ok, sha256_instrumento=sorted(shas), commit_sello=sorted(sellos), primario=est,
               secundarias=sec, costo={m: cru[m]['costo'] for m in moscas})
    with open(os.path.join(OUT, 'lectura_g1a.json'), 'w') as f:
        json.dump(py(out), f, indent=1, sort_keys=True)
    lin = ['VEREDICTO H_G1_VETO: ' + V]
    for m in moscas:
        e = est[m]
        lin.append('%s: beta %.4f, OR %.3f [%.3f; %.3f], p %.4g, p Holm %.4g, Y1 en M %d (G0 espera %.1f), pasa %s'
                   % (m, e['beta_hat'], e['OR'], e['OR_lo'], e['OR_hi'], e['p'], e['p_holm'], e['n_Y1_en_M'],
                      e['esperado_G0_en_M'], e['pasa']))
    for m in moscas:
        for nombre in ('dosis', 'especificidad'):
            d = sec[m][nombre]
            lin.append('%s %s: delta %.4f [%.4f; %.4f] %s' % (m, nombre, d['delta'], d['ic_lo'], d['ic_hi'], d['lectura']))
        lin.append('%s descripcion: %.2f bits' % (m, sec[m]['descripcion_bits']))
    lin.append('banc entero: ' + json.dumps(py(sec['banc']['banc_entero']), sort_keys=True))
    lin.append('transferencia: ' + json.dumps(py(sec['banc']['transferencia']), sort_keys=True))
    with open(os.path.join(OUT, 'lectura_g1a.txt'), 'w') as f:
        f.write(chr(10).join(lin) + chr(10))


def main():
    modo = sys.argv[1]
    if modo == 'calibrar':
        calibrar(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else N_REP)
    elif modo == 'cruzar':
        cruzar(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6] if len(sys.argv) > 6 else None)
    elif modo == 'leer':
        leer(sys.argv[2])
    else:
        raise SystemExit('modo desconocido: ' + modo)


if __name__ == '__main__':
    main()
