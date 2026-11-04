
"""g1_censo.py · Censo del universo de G1-A en FlyWire 783 y BANC 888.
Solo marginales: cuenta Y y M por separado y nunca los cruza par a par.
En BANC agrega los mismos grupos con X fuera del cordon (region distinta de ventral_nerve_cord);
ahi n_aristas_relevo cuenta pares (x, unidad D) distintos, no filas.
Definiciones de S, D, X, signo y tipo iguales a H_REUSO (reuso_mosca.py, sha 3650fc74)."""
import sys, json, hashlib, time, os, platform
import numpy as np, pandas as pd
import pyarrow as pa, pyarrow.parquet as pq, pyarrow.feather as pf, pyarrow.compute as pc
W_DIR, W_X, W_PESADO, W_LIVIANO = 20, 5, 80, 20
LADOS = ('left', 'right')
OUT = sys.argv[1]
log = open(os.path.join(OUT, 'g1_censo.log'), 'w')
def P(s):
    log.write(s + '\n'); log.flush()
def huella(p):
    h5, h2 = hashlib.md5(), hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h5.update(b); h2.update(b)
    return dict(ruta=p, bytes=os.path.getsize(p), md5=h5.hexdigest(), sha256=h2.hexdigest())
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
    return dict(nombre='FlyWire 783', pre=pre, post=post, w=w, inh=inh, tipo=a.cell_type.to_numpy(dtype=object),
                lado=a.side.to_numpy(dtype=object), sc=a.super_class.to_numpy(dtype=object), n=n,
                huellas=[huella(conn), huella(annot)])
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
    return dict(nombre='BANC 888', pre=pre, post=post, w=w, inh=inh, tipo=tipo, lado=m.side.to_numpy(dtype=object),
                sc=m.super_class.to_numpy(dtype=object), n=len(m), huellas=[huella(meta), huella(ar)],
                cerebro=(m.region.to_numpy(dtype=object) != 'ventral_nerve_cord'))
def unidades(tipo, lado, mask, n):
    claves = sorted(set(zip(tipo[mask], lado[mask])))
    idx = {k: i for i, k in enumerate(claves)}
    u = np.full(n, -1, dtype=np.int32)
    for j in np.nonzero(mask)[0]:
        u[j] = idx[(tipo[j], lado[j])]
    return u, claves
def censo(g):
    pre, post, w, inh, tipo, lado, sc, n = g['pre'], g['post'], g['w'], g['inh'], g['tipo'], g['lado'], g['sc'], g['n']
    ok = pd.notna(tipo) & np.isin(lado, LADOS)
    S, cs = unidades(tipo, lado, (sc == 'visual_projection') & ok, n)
    D, cd = unidades(tipo, lado, (sc == 'descending') & ok, n)
    nS, nD = len(cs), len(cd)
    excl = (S >= 0) | (D >= 0)
    xinh = inh & ~excl; xexc = ~inh & ~excl
    m = (S[pre] >= 0) & (D[post] >= 0)
    agg = np.bincount(S[pre[m]].astype(np.int64) * nD + D[post[m]], weights=w[m], minlength=nS * nD).reshape(nS, nD)
    ls = np.array([k[1] for k in cs], dtype=object); ld = np.array([k[1] for k in cd], dtype=object)
    cab = (agg >= W_DIR) & (ls[:, None] == ld[None, :])
    co = (cab.T.astype(np.int32) @ cab.astype(np.int32)) > 0
    np.fill_diagonal(co, False)
    r = dict(conectoma=g['nombre'], n_neuronas=int(n), n_aristas=int(len(pre)), n_unidades_S=nS, n_unidades_D=nD,
             n_neuronas_DN=int((D >= 0).sum()), n_X_inhibitorias_candidatas=int(xinh.sum()),
             n_X_excitatorias_candidatas=int(xexc.sum()), n_pares_S_D_cableados=int(cab.sum()),
             n_pares_D_D_coimpulsados=int(co.sum() // 2))
    mdx = (D[pre] >= 0) & ~excl[post]
    epre, epost, ew = pre[mdx], post[mdx], w[mdx]
    def grupo(nombre, xmask, wmin, wmax):
        sel = xmask[epost] & (ew >= wmin) & (ew < wmax)
        xs = np.unique(epost[sel])
        drv = pd.DataFrame(dict(x=epost[sel], d=D[epre[sel]])).drop_duplicates()
        return nombre, xs, drv, int(sel.sum())
    grupos = [grupo('pesado_inh', xinh, W_PESADO, 1 << 30), grupo('pesado_exc', xexc, W_PESADO, 1 << 30)]
    nombre, xs_l, drv_l, nl = grupo('liviano_inh', xinh, W_LIVIANO, W_PESADO)
    pes = set(grupos[0][1].tolist())
    keep = np.array([x not in pes for x in xs_l], dtype=bool)
    xs_l = xs_l[keep]; drv_l = drv_l[drv_l.x.isin(set(xs_l.tolist()))]
    grupos.append(('liviano_inh_sin_pesado', xs_l, drv_l, nl))
    if 'cerebro' in g:
        cb = g['cerebro']
        r['n_X_inhibitorias_candidatas_cerebro'] = int((xinh & cb).sum())
        extra = []
        for nombre, xs, drv, n_ar in grupos:
            xs2 = xs[cb[xs]]
            drv2 = drv[drv.x.isin(set(xs2.tolist()))]
            extra.append((nombre + '_cerebro', xs2, drv2, int(len(drv2))))
        grupos += extra
    for nombre, xs, drv, n_ar in grupos:
        xset = np.zeros(n, dtype=bool); xset[xs] = True
        sel = xset[pre] & (D[post] >= 0)
        k = pre[sel].astype(np.int64) * nD + D[post[sel]]
        u, inv = np.unique(k, return_inverse=True)
        s = np.bincount(inv, weights=w[sel])
        ypos = pd.DataFrame(dict(x=u[s >= W_X] // nD, d=u[s >= W_X] % nD))
        dd = drv.groupby('x').d.apply(lambda v: sorted(set(int(a) for a in v))).to_dict()
        n_pares = int(sum(nD - len(dd[x]) for x in xs.tolist()))
        ypos = ypos[[d not in dd[x] for x, d in zip(ypos.x.tolist(), ypos.d.tolist())]]
        n_y = int(len(ypos))
        n_m = 0; n_l = 0
        for x in xs.tolist():
            ds = dd[x]
            mm = np.zeros(nD, dtype=bool)
            for d in ds: mm |= co[d]
            mm[ds] = False
            n_m += int(mm.sum())
            lados = set(ld[d] for d in ds)
            ll = np.isin(ld, list(lados)); ll[ds] = False
            n_l += int(ll.sum())
        r[nombre] = dict(n_aristas_relevo=n_ar, n_X=int(len(xs)), n_pares=n_pares, n_Y1_marginal=n_y,
                         n_M1_marginal=int(n_m), n_L1_marginal=int(n_l))
    return r, dict(D=D, cd=cd, excl=excl)
def semilla_g1f(g, manifiesto, agregado):
    pre, post, w, inh = g['pre'], g['post'], g['w'], g['inh']
    suj = json.load(open(manifiesto))['sujetos']
    ag = json.load(open(agregado))['casos']
    filas = []
    for k in sorted(suj):
        x = int(suj[k]['x']); G = [int(v) for v in suj[k]['G']]
        sel = post == x
        p, ww = pre[sel], w[sel]
        exc_in = int(ww[~inh[p]].sum()); inh_in = int(ww[inh[p]].sum())
        de_G = int(ww[np.isin(p, G)].sum())
        c = ag.get('B|' + k, {})
        est = c.get('activacion', {}).get('estado')
        cq = c.get('cocientes', {})
        cx = (cq.get('c_X') or cq.get('c_Xconj') or {}).get('estimado')
        rq = (cq.get('r_Q1') or cq.get('r_Q1conj') or {}).get('estimado')
        filas.append(dict(sujeto=k, x=x, drivers=G, sinapsis_de_drivers=de_G, entrada_exc=exc_in, entrada_inh=inh_in,
                          fraccion_exc_de_drivers=round(de_G / exc_in, 4) if exc_in else None,
                          estado_B=est, c_X_B=cx, r_Q1_B=rq))
    from scipy.stats import spearmanr
    act = [f for f in filas if f['estado_B'] == 'ACTIVADO' and f['c_X_B'] is not None]
    rc = spearmanr([f['fraccion_exc_de_drivers'] for f in act], [f['c_X_B'] for f in act])
    rr = spearmanr([f['fraccion_exc_de_drivers'] for f in act], [f['r_Q1_B'] for f in act])
    return dict(filas=filas, n_activados=len(act), spearman_fraccion_vs_cX=[float(rc[0]), float(rc[1])],
                spearman_fraccion_vs_rQ1=[float(rr[0]), float(rr[1])])
t0 = time.time()
res = dict(version='g1_censo 2026-11-04-001', umbrales=dict(W_DIR=W_DIR, W_X=W_X, W_PESADO=W_PESADO, W_LIVIANO=W_LIVIANO),
           entorno=dict(python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__, pyarrow=pa.__version__, host=platform.node()))
fw = flywire(); P('FlyWire cargado %.1f s' % (time.time() - t0))
res['flywire'], _ = censo(fw); res['huellas_flywire'] = fw['huellas']
P('FlyWire censo ' + json.dumps(res['flywire'], sort_keys=True))
res['semilla_g1f'] = semilla_g1f(fw, '/workspace/a1/v2/manifiesto_a1.json', '/workspace/a1/v2/apertura/prod/agregado_a1.json')
P('semilla G1-F ' + json.dumps({k: v for k, v in res['semilla_g1f'].items() if k != 'filas'}, sort_keys=True))
del fw
b = banc(); P('BANC cargado %.1f s' % (time.time() - t0))
res['banc'], _ = censo(b); res['huellas_banc'] = b['huellas']
P('BANC censo ' + json.dumps(res['banc'], sort_keys=True))
res['segundos'] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(OUT, 'g1_censo.json'), 'w'), indent=1, sort_keys=True)
P('FIN %.1f s' % (time.time() - t0))
