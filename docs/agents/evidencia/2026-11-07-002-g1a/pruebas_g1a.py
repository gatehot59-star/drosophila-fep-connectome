# pruebas_g1a.py: pruebas que pueden fallar del instrumento g1a.py, sobre FlyWire 783.
# Nunca cruza la Y real con el M real: G0 usa la Y real (no mira M) y todo lo que mira M usa una Y sintetica.
import sys, os, json, time
import numpy as np
from scipy import sparse
from scipy.special import expit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g1a
OUT = sys.argv[1]
T = time.time()
res = {}
LOG = os.path.join(OUT, 'pruebas_g1a.log')
open(LOG, 'w').close()


def anota(nombre, ok, **d):
    e = dict(prueba=nombre, pasa=bool(ok), s=round(time.time() - T, 1))
    e.update(g1a.py(d))
    res[nombre] = e
    with open(LOG, 'a') as f:
        f.write(json.dumps(e, sort_keys=True) + chr(10))


def ajuste_completo(ix, jd, Z, y, nx, nd):
    # implementacion independiente: diseno disperso entero y Hessiano denso completo, sin eliminar bloques
    n = len(y)
    f = np.arange(n)
    X = sparse.hstack([sparse.csr_matrix((np.ones(n), (f, ix)), shape=(n, nx)),
                       sparse.csr_matrix((np.ones(n), (f, jd)), shape=(n, nd))[:, 1:],
                       sparse.csr_matrix(Z)], format='csr')
    bb = np.zeros(X.shape[1])
    eta = X @ bb
    ll = float(y @ eta - np.logaddexp(0.0, eta).sum())
    it = 0
    for it in range(300):
        p = expit(eta)
        gr_ = X.T @ (y - p)
        if np.abs(gr_).max() < 1e-9:
            break
        H = (X.T @ sparse.diags(p * (1 - p)) @ X).toarray()
        paso = np.linalg.solve(H, gr_)
        t = 1.0
        while True:
            en = X @ (bb + t * paso)
            l2 = float(y @ en - np.logaddexp(0.0, en).sum())
            if l2 >= ll - 1e-9 or t < 1e-8:
                break
            t *= 0.5
        bb, eta, ll = bb + t * paso, en, l2
    p = expit(eta)
    H = (X.T @ sparse.diags(p * (1 - p)) @ X).toarray()
    return dict(eta=eta, ll=ll, b=bb, H=H, X=X, it=it)


def bt_escalar(o, y, idx, keep):
    o1 = o[idx]
    k = float(y[idx].sum())
    nk = int(keep[idx].sum())
    if k == 0:
        return -np.inf
    if k == nk:
        return np.inf
    bb = 0.0
    for _ in range(500):
        p = expit(o1 + bb)
        st = max(-5.0, min(5.0, (p.sum() - k) / (p * (1 - p)).sum()))
        bb -= st
        if abs(st) < 1e-13:
            break
    return bb


g = g1a.cargar('flywire')
b = g1a.base_mosca(g)
cl = g1a.PRIMARIO['flywire']
gr = g1a.grupo(g, b, *cl)
cu = g1a.cuentas(gr, b)
ok = g1a.chequeo_censo('flywire', cl, cu, abortar=False)
anota('T1_censo_' + '_'.join(cl), all(ok.values()), cuentas=cu, chequeo=ok)
for c2 in g1a.SECUNDARIOS['flywire']:
    g2 = g1a.grupo(g, b, *c2)
    cu2 = g1a.cuentas(g2, b)
    ok2 = g1a.chequeo_censo('flywire', c2, cu2, abortar=False)
    anota('T1_censo_' + '_'.join(c2), all(ok2.values()), cuentas=cu2, chequeo=ok2)
    del g2
del g
fuera = int((gr['M'] & (gr['L'] == 0)).sum())
anota('T2_M_contenido_en_L', fuera == 0, M_fuera_de_L=fuera)

yr = gr['y'].astype(np.float64)
kx = np.bincount(gr['px'], yr, gr['nX']) > 0
kd = np.bincount(gr['pdd'], yr, gr['nD']) > 0
keep = kx[gr['px']] & kd[gr['pdd']]
mx, md = np.cumsum(kx) - 1, np.cumsum(kd) - 1
ix, jd = mx[gr['px'][keep]], md[gr['pdd'][keep]]
nxk, ndk = int(kx.sum()), int(kd.sum())
Lk = gr['L'][keep].astype(np.float64)
t1 = time.time()
fb = g1a.ajustar(ix, jd, Lk[:, None], yr[keep], nxk, ndk)
tb = time.time() - t1
t1 = time.time()
fc = ajuste_completo(ix, jd, Lk[:, None], yr[keep], nxk, ndk)
tc = time.time() - t1
de = float(np.abs(fb['eta'] - fc['eta']).max())
anota('T3_G0_bloques_igual_a_completo', de < 1e-5 and abs(fb['ll'] - fc['ll']) < 1e-6 and fb['conv'],
      max_dif_eta=de, dif_ll=abs(fb['ll'] - fc['ll']), it_bloques=fb['it'], it_completo=fc['it'],
      seg_bloques=round(tb, 3), seg_completo=round(tc, 3), gamma=float(fb['c'][0]),
      n_pares_info=int(keep.sum()), n_X_info=nxk, n_D_info=ndk)
Lp = np.random.default_rng(1).permutation(Lk)
fp = g1a.ajustar(ix, jd, Lp[:, None], yr[keep], nxk, ndk)
dp = float(np.abs(fp['eta'] - fc['eta']).max())
anota('T4_control_del_comparador_con_L_permutada_debe_diferir', dp > 1e-3, max_dif_eta=dp)
o0 = np.full(len(gr['px']), g1a.O_FUERA)
o0[keep] = fb['eta']
del yr

ys = (np.random.default_rng(20261107).random(len(o0)) < expit(o0 + 0.7 * gr['M'])).astype(np.int8)
bk = g1a.banco(b, 'flywire', n=20, semilla=11)
ln = g1a.lote_de_banco(gr, b, bk)
lr = g1a.lote([np.nonzero(gr['M'])[0]])
t1 = time.time()
fin, aux = g1a.analizar(ys, gr, lr, ln)
ta = time.time() - t1
Z1 = np.column_stack([aux['Lk'], aux['Mk']])
fc1 = ajuste_completo(aux['ix'], aux['jd'], Z1, aux['yk'], aux['nxk'], aux['ndk'])
Hi = np.linalg.inv(fc1['H'])
h = Hi[:, -1]
r = aux['yk'] - expit(fc1['eta'])
Xr = sparse.csr_matrix(fc1['X'].multiply(r[:, None]))
nn = len(r)
Ix = sparse.csr_matrix((np.ones(nn), (aux['ix'], np.arange(nn))), shape=(aux['nxk'], nn))
Id = sparse.csr_matrix((np.ones(nn), (aux['jd'], np.arange(nn))), shape=(aux['ndk'], nn))
psi = Xr @ h
Vx, Vd, V0 = float(((Ix @ psi) ** 2).sum()), float(((Id @ psi) ** 2).sum()), float((psi ** 2).sum())
smf, bf = float(np.sqrt(Hi[-1, -1])), float(fc1['b'][-1])


def rel(a, c):
    return abs(a / c - 1.0)


ok5 = (abs(fin['beta_hat'] - bf) < 1e-5 and rel(fin['se_modelo'], smf) < 1e-4 and rel(fin['V_x'], Vx) < 1e-4
       and rel(fin['V_d'], Vd) < 1e-4 and rel(fin['V_0'], V0) < 1e-4 and fin['conv1'])
anota('T5_G1_y_errores_bloques_igual_a_completo', ok5, beta_plantado=0.7, beta_hat_bloques=fin['beta_hat'],
      beta_hat_completo=bf, se_modelo_bloques=fin['se_modelo'], se_modelo_completo=smf, V_x=[fin['V_x'], Vx],
      V_d=[fin['V_d'], Vd], V_0=[fin['V_0'], V0], se_robusto=fin['se_robusto'], regla=fin['regla_se'],
      seg_analizar_con_20_nulos=round(ta, 3), seg_g0=fin['seg_g0'], seg_g1=fin['seg_g1'], seg_nulo_20=fin['seg_nulo'])
ysf = ys.astype(np.float64)
vec = np.concatenate([g1a.beta_tilde_lote(aux['o'], ysf, aux['keep'], lr)[0],
                      g1a.beta_tilde_lote(aux['o'], ysf, aux['keep'], ln)[0]])
listas = [np.nonzero(gr['M'])[0]] + [np.nonzero(g1a.M_de(es, ed, b['nS'], b['nD'], gr['Drs'], gr['px'], gr['pdd']))[0]
                                     for es, ed in bk['tablas']]
esc = np.array([bt_escalar(aux['o'], ysf, a, aux['keep']) for a in listas])
anota('T6_beta_tilde_vectorizado_igual_a_escalar', bool(np.allclose(vec, esc, atol=1e-8, rtol=0)),
      max_dif=float(np.max(np.abs(vec - esc))), n_listas=len(listas))
ba = g1a.banco(b, 'flywire', n=5, semilla=99)
bb2 = g1a.banco(b, 'flywire', n=5, semilla=99)
bc = g1a.banco(b, 'flywire', n=5, semilla=100)
anota('T7_banco_determinista_y_valido', ba['sha256'] == bb2['sha256'] and ba['sha256'] != bc['sha256']
      and ba['chequeos_ok'] == 5 and bk['chequeos_ok'] == 20, sha_a=ba['sha256'], sha_b=bb2['sha256'],
      sha_otra_semilla=bc['sha256'], intercambios_media=ba['intercambios_media'],
      fraccion_aristas_reales_media=ba['fraccion_aristas_reales_media'], n_aristas=ba['n_aristas'])
anota('T8_recupera_el_beta_plantado_en_una_replica', abs(fin['beta_hat'] - 0.7) < 4 * fin['se_robusto'],
      beta_hat=fin['beta_hat'], se_robusto=fin['se_robusto'], p_con_20_nulos=fin['p_nulo'])
todas = all(v['pasa'] for v in res.values())
with open(os.path.join(OUT, 'pruebas_g1a.json'), 'w') as f:
    json.dump(g1a.py(dict(version=g1a.VERSION, sha256_g1a=g1a.sha_archivo(os.path.abspath(g1a.__file__)),
                          sha256_pruebas=g1a.sha_archivo(os.path.abspath(__file__)), todas_pasan=todas, pruebas=res,
                          entorno=g1a.entorno(), segundos=round(time.time() - T, 1))), f, indent=1, sort_keys=True)
with open(LOG, 'a') as f:
    f.write('FIN todas_pasan=%s s=%.1f' % (todas, time.time() - T) + chr(10))
