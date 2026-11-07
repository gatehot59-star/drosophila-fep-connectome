"""g1_memoria_nulo.py · Sonda de memoria y tiempo del nulo de G1-A (recableados de la tabla S->D).
No es el instrumento sellado. La Y es sintetica: la Y real se permuta dentro de cada x con semilla fija y se
borra antes del nulo; M se calcula solo sobre tablas S->D recableadas. Nunca cruza Y con M reales.
Definiciones de S, D, X, signo, tipo y umbrales iguales a g1_censo.py (respuesta 2026-11-04-001)."""
import sys, os, json, time, gc, hashlib, platform, tracemalloc
import numpy as np, pandas as pd, scipy
import pyarrow as pa, pyarrow.parquet as pq, pyarrow.feather as pf, pyarrow.compute as pc
from scipy import sparse
W_DIR, W_X, W_PESADO, W_LIVIANO = 20, 5, 80, 20
LADOS = ('left', 'right')
MOSCA, ALCANCE, GRUPO, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
N_NULO, N_TRAZA, SEMILLA = int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
NOMBRE = '%s_%s_%s' % (MOSCA, ALCANCE, GRUPO)
log = open(os.path.join(OUT, 'mem_%s.log' % NOMBRE), 'w')
t0 = time.time()
etapas = []
def mem():
    d = {}
    for l in open('/proc/self/status'):
        k = l.split(':')[0]
        if k in ('VmRSS', 'VmHWM', 'RssAnon', 'RssFile'):
            d[k + '_MiB'] = round(int(l.split()[1]) / 1024, 1)
    return d
def etapa(nombre, **extra):
    e = dict(etapa=nombre, s=round(time.time() - t0, 2))
    e.update(mem()); e.update(extra)
    etapas.append(e); log.write(json.dumps(e, sort_keys=True) + '\n'); log.flush()
def huella(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return dict(ruta=p, bytes=os.path.getsize(p), md5=h.hexdigest())
def col(path, c, dt):
    return pq.read_table(path, columns=[c]).column(c).to_numpy().astype(dt)
def flywire():
    conn, annot = '/workspace/connectivity.parquet', '/workspace/annotations.tsv'
    pre = col(conn, 'Presynaptic_Index', np.int32); post = col(conn, 'Postsynaptic_Index', np.int32)
    n = int(max(pre.max(), post.max())) + 1
    rid = np.zeros(n, dtype=np.int64)
    rid[pre] = col(conn, 'Presynaptic_ID', np.int64); rid[post] = col(conn, 'Postsynaptic_ID', np.int64)
    w = col(conn, 'Connectivity', np.int32)
    exc = col(conn, 'Excitatory', np.int8)
    inh = np.zeros(n, dtype=bool); inh[pre[exc < 0]] = True
    del exc
    a = pd.read_csv(annot, sep=chr(9), dtype=str, usecols=['root_id', 'cell_type', 'side', 'super_class'])
    a['root_id'] = a.root_id.astype(np.int64)
    a = a.drop_duplicates('root_id').set_index('root_id').reindex(rid)
    return dict(pre=pre, post=post, w=w, inh=inh, tipo=a.cell_type.to_numpy(dtype=object),
                lado=a.side.to_numpy(dtype=object), sc=a.super_class.to_numpy(dtype=object), n=n,
                entradas=[conn, annot])
def banc():
    meta = '/workspace/banc_888/banc_888_meta.feather'; ar = '/workspace/banc_888/banc_888_edgelist_simple_v3.feather'
    m = pd.read_feather(meta, columns=['root_888', 'side', 'super_class', 'cell_type', 'fafb_cell_type', 'neurotransmitter_predicted', 'region'])
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
    return dict(pre=pre, post=post, w=w, inh=inh, tipo=tipo, lado=m.side.to_numpy(dtype=object),
                sc=m.super_class.to_numpy(dtype=object), n=len(m), entradas=[meta, ar],
                cerebro=(m.region.to_numpy(dtype=object) != 'ventral_nerve_cord'))
def unidades(tipo, lado, mask, n):
    claves = sorted(set(zip(tipo[mask], lado[mask])))
    idx = {k: i for i, k in enumerate(claves)}
    u = np.full(n, -1, dtype=np.int32)
    for j in np.nonzero(mask)[0]:
        u[j] = idx[(tipo[j], lado[j])]
    return u, claves
def estructuras(g):
    pre, post, w, inh, tipo, lado, sc, n = (g[k] for k in ('pre', 'post', 'w', 'inh', 'tipo', 'lado', 'sc', 'n'))
    ok = pd.notna(tipo) & np.isin(lado, LADOS)
    S, cs = unidades(tipo, lado, (sc == 'visual_projection') & ok, n)
    D, cd = unidades(tipo, lado, (sc == 'descending') & ok, n)
    nS, nD = len(cs), len(cd)
    excl = (S >= 0) | (D >= 0)
    xinh = inh & ~excl
    if ALCANCE == 'cerebro':
        xinh = xinh & g['cerebro']
    m = (S[pre] >= 0) & (D[post] >= 0)
    agg = np.bincount(S[pre[m]].astype(np.int64) * nD + D[post[m]], weights=w[m], minlength=nS * nD).reshape(nS, nD)
    ls = np.array([k[1] for k in cs], dtype=object); ld = np.array([k[1] for k in cd], dtype=object)
    cab = (agg >= W_DIR) & (ls[:, None] == ld[None, :])
    base = (D[pre] >= 0) & xinh[post]
    pesadas = np.unique(post[base & (w >= W_PESADO)])
    if GRUPO == 'pesado':
        sel = base & (w >= W_PESADO)
    else:
        sel = base & (w >= W_LIVIANO) & (w < W_PESADO) & ~np.isin(post, pesadas)
    drv = pd.DataFrame(dict(x=post[sel], d=D[pre[sel]])).drop_duplicates()
    xs = np.unique(drv.x.to_numpy())
    xset = np.zeros(n, dtype=bool); xset[xs] = True
    s2 = xset[pre] & (D[post] >= 0)
    k = pre[s2].astype(np.int64) * nD + D[post[s2]]
    u, inv = np.unique(k, return_inverse=True)
    sw = np.bincount(inv, weights=w[s2])
    ypos = set(u[sw >= W_X].tolist())
    dd = drv.groupby('x').d.apply(lambda v: sorted(set(int(a) for a in v))).to_dict()
    px, pdd, y, L, drivers = [], [], [], [], []
    for i, x in enumerate(xs.tolist()):
        ds = dd[x]; drivers.append(ds)
        lados = set(ld[d] for d in ds); sd = set(ds)
        for d2 in range(nD):
            if d2 in sd:
                continue
            px.append(i); pdd.append(d2)
            y.append(1 if x * nD + d2 in ypos else 0); L.append(1 if ld[d2] in lados else 0)
    return dict(cab=cab, ls=ls, nS=nS, nD=nD, nX=len(xs), drivers=drivers,
                px=np.array(px, dtype=np.int32), pdd=np.array(pdd, dtype=np.int32),
                y=np.array(y, dtype=np.int8), L=np.array(L, dtype=np.int8))
def y_sintetica(px, y, nX, rng):
    ys = np.zeros_like(y)
    cortes = np.searchsorted(px, np.arange(nX + 1))
    for i in range(nX):
        idx = np.arange(cortes[i], cortes[i + 1])
        kx = int(y[idx].sum())
        if kx:
            ys[rng.choice(idx, size=kx, replace=False)] = 1
    return ys
def ajustar_g0(ix, jd, L, y):
    n = len(y); nx = int(ix.max()) + 1; nd = int(jd.max()) + 1
    f = np.arange(n)
    X = sparse.hstack([sparse.csr_matrix((np.ones(n), (f, ix)), shape=(n, nx)),
                       sparse.csr_matrix((np.ones(n), (f, jd)), shape=(n, nd)),
                       sparse.csr_matrix(L.astype(np.float64).reshape(-1, 1))], format='csr')
    b = np.zeros(X.shape[1]); ll_prev = -np.inf; ll = ll_prev
    for it in range(1, 101):
        eta = X @ b
        p = 1.0 / (1.0 + np.exp(-eta))
        g = X.T @ (y - p)
        H = (X.T @ sparse.diags(p * (1.0 - p)) @ X).toarray()
        H[np.diag_indices_from(H)] += 1e-6
        paso = np.linalg.solve(H, g)
        t = 1.0
        for _ in range(30):
            eta_n = X @ (b + t * paso)
            ll = float(y @ eta_n - np.logaddexp(0.0, eta_n).sum())
            if ll >= ll_prev - 1e-9:
                break
            t *= 0.5
        b = b + t * paso; ll_prev = ll
        if np.abs(t * paso).max() < 1e-7:
            break
    return X @ b, it, ll, int(X.shape[1])
def beta_tilde(o, y, M):
    o1 = o[M]; k = float(y[M].sum()); n1 = len(o1)
    if n1 == 0 or k == 0 or k == n1:
        return float('nan')
    b = 0.0
    for _ in range(100):
        p = 1.0 / (1.0 + np.exp(-(o1 + b)))
        paso = (p.sum() - k) / (p * (1.0 - p)).sum()
        b -= paso
        if abs(paso) < 1e-10:
            break
    return b
etapa('inicio')
g = flywire() if MOSCA == 'flywire' else banc()
entradas = g['entradas']
etapa('mosca_cargada', n_neuronas=int(g['n']), n_aristas=int(len(g['pre'])))
est = estructuras(g)
del g
gc.collect()
nS, nD, nX = est['nS'], est['nD'], est['nX']
cuentas = dict(n_X=nX, n_pares=int(len(est['px'])), n_Y1=int(est['y'].sum()), n_L1=int(est['L'].sum()),
               n_aristas_cab=int(est['cab'].sum()))
etapa('estructuras_y_mosca_liberada', **cuentas)
rng = np.random.default_rng(SEMILLA)
ys = y_sintetica(est['px'], est['y'], nX, rng)
est['y'] = None
gc.collect()
kx = np.bincount(est['px'], weights=ys, minlength=nX) > 0
kd = np.bincount(est['pdd'], weights=ys, minlength=nD) > 0
keep = kx[est['px']] & kd[est['pdd']]
pxk, pddk, Lk, ysk = est['px'][keep], est['pdd'][keep], est['L'][keep], ys[keep].astype(np.float64)
ix = np.unique(pxk, return_inverse=True)[1]; jd = np.unique(pddk, return_inverse=True)[1]
etapa('y_sintetica', n_pares_con_info=int(keep.sum()), n_X_con_info=int(kx.sum()), n_D_con_info=int(kd.sum()))
o, it_g0, ll_g0, n_param = ajustar_g0(ix, jd, Lk, ysk)
gc.collect()
etapa('g0_ajustado', iteraciones=int(it_g0), n_parametros=n_param)
cab, ls = est['cab'], est['ls']
E = np.argwhere(cab)
lado_e = ls[E[:, 0]]
idx_lado = [np.nonzero(lado_e == l)[0] for l in LADOS]
drv = est['drivers']
Dr = sparse.csr_matrix((np.ones(sum(len(d) for d in drv)), (np.repeat(np.arange(nX), [len(d) for d in drv]),
                        np.array([d for ds in drv for d in ds]))), shape=(nX, nD))
def recablear(rng):
    es = E[:, 0].tolist(); ed = E[:, 1].tolist()
    claves = set(s * nD + d for s, d in zip(es, ed))
    hechos = 0; intentos = 0
    for idx in idx_lado:
        m = len(idx)
        if m < 2:
            continue
        ii = idx[rng.integers(0, m, size=10 * m)].tolist(); jj = idx[rng.integers(0, m, size=10 * m)].tolist()
        intentos += 10 * m
        for i, j in zip(ii, jj):
            s1, d1, s2, d2 = es[i], ed[i], es[j], ed[j]
            if s1 == s2 or d1 == d2:
                continue
            k1 = s1 * nD + d2; k2 = s2 * nD + d1
            if k1 in claves or k2 in claves:
                continue
            claves.discard(s1 * nD + d1); claves.discard(s2 * nD + d2); claves.add(k1); claves.add(k2)
            ed[i] = d2; ed[j] = d1; hechos += 1
    return np.array(es), np.array(ed), hechos, intentos
def M_de(es, ed):
    C = sparse.csr_matrix((np.ones(len(es)), (es, ed)), shape=(nS, nD))
    co = (C.T @ C).tocsr(); co.setdiag(0); co.eliminate_zeros()
    A = (Dr @ co).toarray()
    return A[pxk, pddk] > 0
def grados(es, ed):
    return np.bincount(es, minlength=nS), np.bincount(ed, minlength=nD)
gs0, gd0 = grados(E[:, 0], E[:, 1])
gc.collect()
etapa('antes_del_nulo', n_aristas_por_lado=[int(len(i)) for i in idx_lado])
betas = np.full(N_NULO, np.nan); hechos = np.zeros(N_NULO, dtype=np.int64); nm = np.zeros(N_NULO, dtype=np.int64)
grados_ok = 0; muestras = []
t1 = time.time()
for r in range(N_NULO):
    es, ed, h, intentos = recablear(rng)
    a1, a2 = grados(es, ed)
    grados_ok += int(np.array_equal(a1, gs0) and np.array_equal(a2, gd0))
    Mv = M_de(es, ed)
    nm[r] = int(Mv.sum()); hechos[r] = h
    betas[r] = beta_tilde(o, ysk, Mv)
    if r in (0, 9) or (r + 1) % 100 == 0:
        q = dict(r=r + 1); q.update(mem()); muestras.append(q)
seg_nulo = time.time() - t1
etapa('despues_del_nulo', recableados=N_NULO, segundos_nulo=round(seg_nulo, 2))
tracemalloc.start()
for r in range(N_TRAZA):
    es, ed, h, intentos = recablear(rng); Mv = M_de(es, ed); beta_tilde(o, ysk, Mv)
cur, pico = tracemalloc.get_traced_memory(); tracemalloc.stop()
etapa('traza', recableados=N_TRAZA, tracemalloc_pico_MiB=round(pico / 2**20, 3), tracemalloc_actual_MiB=round(cur / 2**20, 3))
censo = json.load(open('/workspace/a1/v2/g1/censo/g1_censo.json'))
clave = {'flywire_entero_pesado': ('flywire', 'pesado_inh'), 'banc_cerebro_pesado': ('banc', 'pesado_inh_cerebro'),
         'banc_entero_pesado': ('banc', 'pesado_inh'), 'banc_entero_liviano': ('banc', 'liviano_inh_sin_pesado'),
         'flywire_entero_liviano': ('flywire', 'liviano_inh_sin_pesado'), 'banc_cerebro_liviano': ('banc', 'liviano_inh_sin_pesado_cerebro')}[NOMBRE]
c = censo[clave[0]][clave[1]]
cuadra = dict(n_X=c['n_X'] == cuentas['n_X'], n_pares=c['n_pares'] == cuentas['n_pares'],
              n_Y1=c['n_Y1_marginal'] == cuentas['n_Y1'], n_L1=c['n_L1_marginal'] == cuentas['n_L1'],
              n_aristas_cab=censo[clave[0]]['n_pares_S_D_cableados'] == cuentas['n_aristas_cab'])
fin = np.isfinite(betas)
res = dict(version='g1_memoria_nulo 2026-11-07-001', configuracion=dict(mosca=MOSCA, alcance=ALCANCE, grupo=GRUPO,
           n_nulo=N_NULO, n_traza=N_TRAZA, semilla=SEMILLA, intentos_por_lado='10 x aristas del lado'),
           cuentas=cuentas, cuadra_con_censo=cuadra, etapas=etapas, muestras_rss=muestras,
           nulo=dict(segundos=round(seg_nulo, 2), segundos_por_recableado=round(seg_nulo / N_NULO, 4),
                     grados_conservados=int(grados_ok), intercambios_efectivos_media=round(float(hechos.mean()), 1),
                     M1_media=round(float(nm.mean()), 1), M1_min=int(nm.min()), M1_max=int(nm.max()),
                     beta_finitos=int(fin.sum()),
                     beta_sintetica_media=round(float(np.nanmean(betas)), 4), beta_sintetica_de=round(float(np.nanstd(betas)), 4)),
           guardado_bytes=dict(betas_float64=int(N_NULO * 8), tablas_int16_si_se_guardan=int(N_NULO * len(E) * 2 * 2)),
           entradas=[huella(p) for p in entradas],
           entorno=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, pandas=pd.__version__,
                        pyarrow=pa.__version__, host=platform.node()),
           segundos_total=round(time.time() - t0, 1))
json.dump(res, open(os.path.join(OUT, 'mem_%s.json' % NOMBRE), 'w'), indent=1, sort_keys=True)
etapa('FIN')
