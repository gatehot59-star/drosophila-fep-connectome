#!/usr/bin/env python3
# guardas_a1_brain.py v2 - BRAIN, 2026-11-03.
# Recalculo independiente de las guardas anatomicas de la enmienda 009-A1 (respuesta 2026-11-02-010)
# y de las 64 guardas originales del sello 009. No importa ni lee medir_guardas_a1.py:
# todo se define desde el texto de 010 (secciones 3, 4 y 8) y se compara contra sus tablas publicadas.
# v2 agrega: identidad exacta de cada D' y de cada poblacion A (huella sha256 de la lista JSON compacta + LF,
# el formato publicado en la evidencia de 010), uniones Q1 conjunto de los hubs, filas QWEAK y peso A->driver,
# comparados contra la salida JSON publicada en docs/agents/evidencia/2026-11-02-010-guardas-enmienda-009-a1.md
# (fijada por su sha256). Ese archivo se usa solo como valor esperado; ningun calculo se toma de el.
# Exit 0 si todo coincide, 1 si alguna fila difiere, 2 si una huella de entrada no coincide.
# Uso: python3 guardas_a1_brain.py [--parquet RUTA] [--units RUTA] [--sello RUTA] [--evid010 RUTA]
# Las cuatro entradas se verifican por sha256 antes de medir. En el repo estan el sello
# (docs/auditorias/evidencia/2026-11-02-02/sello_diseno_16_relevos.json) y la evidencia de 010
# (docs/agents/evidencia/2026-11-02-010-guardas-enmienda-009-a1.md). connectivity.parquet y flywire_units.npz
# no se commitean: son los archivos de brain-env que usaron H_MECANISMO y 010, fijados por las huellas de PIN.
import argparse, hashlib, json, sys, time
import numpy as np, pyarrow.parquet as pq

_ap = argparse.ArgumentParser(description='Recalculo independiente de las guardas anatomicas de 009-A1')
_ap.add_argument('--parquet', default='/workspace/connectivity.parquet')
_ap.add_argument('--units', default='/workspace/mecanismo-2026-11-02/flywire_units.npz')
_ap.add_argument('--sello', default='/workspace/r2026-11-03/sello_diseno_16_relevos.json')
_ap.add_argument('--evid010', default='/workspace/r2026-11-03/evid010.md')
_args = _ap.parse_args()
PARQUET, UNITS, SELLO, EVID010 = _args.parquet, _args.units, _args.sello, _args.evid010
PIN = {'parquet': 'efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347',
       'units': 'fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df',
       'sello': '210b581792d183517d1e4e7771b8435e4a6acb537bc1ad383e5725c500073e93',
       'evid010': 'd5d9b7bad373c13bc240581153fbef8820e2d5587979b263a7908e76daa4eeb8'}

# Valores publicados en 010 (tablas de la seccion 3, cascada y poblaciones de la seccion 4)
ESP_R = {
 'R01': (137, (27, 935), (28, 1170), (137, 2672), (138, 2907)),
 'R02': (25, (6, 135), (7, 315), (25, 271), (26, 451)),
 'R03': (40, (19, 452), (20, 617), (40, 410), (41, 575)),
 'R04': (75, (35, 566), (36, 721), (75, 907), (76, 1062)),
 'R05': (63, (20, 237), (21, 391), (63, 770), (64, 924)),
 'R06': (113, (11, 69), (12, 222), (113, 1318), (114, 1471)),
 'R07': (64, (19, 84), (20, 212), (64, 775), (65, 903)),
 'R08': (70, (27, 1527), (28, 1653), (70, 404), (71, 530)),
 'R09': (56, (17, 307), (18, 427), (56, 608), (57, 728)),
 'R10': (138, (11, 27), (12, 142), (138, 1928), (139, 2043)),
 'R11': (192, (41, 670), (42, 781), (192, 2330), (193, 2441)),
 'R12': (62, (28, 750), (29, 846), (62, 655), (63, 751)),
 'R13': (113, (8, 10), (9, 103), (113, 979), (114, 1072)),
 'R14': (139, (8, 70), (9, 161), (139, 1963), (140, 2054)),
 'R15': (173, (22, 118), (23, 206), (173, 1818), (174, 1906)),
 'R16': (75, (32, 734), (33, 822), (75, 917), (76, 1005))}
ESP_H = {
 'H1': (33912, [41594, 104203, 19410], 137, (29, 147), (137, 1904)),
 'H1b': (58129, [58878, 71368], 113, (12, 271), (113, 979)),
 'H2': (19257, [111205, 130297], 63, (39, 321), (63, 770)),
 'H3': (122969, [27878, 20277], 74, (67, 1300), (74, 896)),
 'H4': (45293, [129110, 53975], 191, (68, 750), (191, 2329)),
 'H4b': (112031, [84751, 69226], 172, (53, 446), (172, 1784))}
ESP_POB = {'LPLC1_right': 72, 'LTe65_left': 3, 'LPT04_HST_right': 1, 'LC9_right': 92, 'LTe49_right': 14,
           'LPT52_right': [47682], 'LTe42b_right': [71560], 'Nod5_left': [113236], 'LTe42c_right': [138092]}
ESP_PRE = {27878: (('LAL014', 'CB0132'), [61826, 70277]),
           130297: (('PVLP137', 'CB0529'), [29603, 29939, 61559, 116669]),
           104203: (('CL215', 'CL095'), [23917, 48054, 52007, 84088, 113573, 118025])}

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

t0 = time.time()
for k, p in (('parquet', PARQUET), ('units', UNITS), ('sello', SELLO), ('evid010', EVID010)):
    s = sha(p)
    print('HUELLA', k, s, 'OK' if s == PIN[k] else 'DISTINTA', flush=True)
    if s != PIN[k]:
        sys.exit(2)

cols = ['Presynaptic_Index', 'Postsynaptic_Index', 'Connectivity', 'Excitatory x Connectivity']
tab = pq.read_table(PARQUET, columns=cols)
pre = tab.column(cols[0]).to_numpy().astype(np.int64)
post = tab.column(cols[1]).to_numpy().astype(np.int64)
con = tab.column(cols[2]).to_numpy().astype(np.int64)
w = tab.column(cols[3]).to_numpy().astype(np.int64)
del tab
N_ROWS = pre.size
print('FILAS', N_ROWS, 'abs(w)==con', bool(np.all(np.abs(w) == con)), 'con>0', bool(np.all(con > 0)), flush=True)
N = int(max(pre.max(), post.max())) + 1
clave = pre * N + post
print('PARES_UNICOS', int(np.unique(clave).size) == N_ROWS, flush=True)
del clave

u = np.load(UNITS)
Du, root, tipo, sl, Su, inh = u['D'], u['root'], u['tipo'], u['sl'], u['S'], u['inh']
Dset = Du >= 0
print('NEURONAS', Du.size, 'D_elegibles', int(Dset.sum()), flush=True)

o_pre = np.argsort(pre, kind='stable'); ps = pre[o_pre]
o_post = np.argsort(post, kind='stable'); qs = post[o_post]
def desde(i):
    lo, hi = np.searchsorted(ps, [i, i + 1]); return o_pre[lo:hi]
def hacia(i):
    lo, hi = np.searchsorted(qs, [i, i + 1]); return o_post[lo:hi]
def tupla(filas):
    f = np.unique(np.asarray(filas, dtype=np.int64))
    f = f[con[f] != 0]
    return (int(f.size), int(np.abs(w[f]).sum()))
def dprime(x, G):
    r = desde(x); r = r[(w[r] < 0) & Dset[post[r]]]
    t = np.unique(post[r]); return t[~np.isin(t, np.asarray(G))]
def f_q1(G, x):
    return np.concatenate([r[post[r] == x] for r in (desde(g) for g in G)])
def f_qcol(G, Dp):
    return np.concatenate([r[(w[r] > 0) & np.isin(post[r], Dp)] for r in (desde(g) for g in G)])
def f_qxd(x, Dp):
    r = desde(x); return r[(w[r] < 0) & np.isin(post[r], Dp)]
def h_dp(Dp):
    return hashlib.sha256(','.join(str(int(i)) for i in sorted(Dp)).encode()).hexdigest()

ok = 0; tot = 0; dif = []
def chk(nombre, obtenido, esperado):
    global ok, tot
    tot += 1; bien = obtenido == esperado; ok += bien
    if not bien: dif.append(nombre)
    print('CHK', nombre, 'obtenido=', obtenido, 'esperado=', esperado, 'OK' if bien else 'DIFERENTE', flush=True)

sello = json.load(open(SELLO))
for r in sello:
    c = r['code'][:3]; d, x = r['d_idx'], r['x_idx']
    chk(c + ' raiz_d', int(root[d]), r['d_root']); chk(c + ' raiz_x', int(root[x]), r['x_root'])
    g = r['guardas_filas']
    q1 = f_q1([d], x)
    chk(c + ' Q1_sello', tupla(q1), (g['Q1']['filas'], int(g['Q1']['peso_abs'])))
    chk(c + ' Q2_sello', tupla(desde(x)), (g['Q2']['filas'], int(g['Q2']['peso_abs'])))
    chk(c + ' Q3_sello', tupla(desde(d)), (g['Q3']['filas'], int(g['Q3']['peso_abs'])))
    rin = hacia(x)
    chk(c + ' Q4_sello', tupla(rin[pre[rin] != d]), (g['Q4']['filas'], int(g['Q4']['peso_abs'])))
    Dp = dprime(x, [d]); e = ESP_R[c]
    qcol = f_qcol([d], Dp); qxd = f_qxd(x, Dp)
    chk(c + ' nDp', int(Dp.size), e[0])
    chk(c + ' QCOL', tupla(qcol), e[1])
    chk(c + ' Q1uQCOL', tupla(np.concatenate([q1, qcol])), e[2])
    chk(c + ' QXD', tupla(qxd), e[3])
    chk(c + ' Q1uQXD', tupla(np.concatenate([q1, qxd])), e[4])
    rin2 = rin[(w[rin] > 0) & Dset[pre[rin]] & (pre[rin] != d) & (con[rin] >= 1) & (con[rin] <= 5)]
    if rin2.size:
        m = con[rin2].max(); cand = rin2[con[rin2] == m]; f = cand[np.argmin(pre[cand])]
        print('QWEAK', c, 'fila', int(pre[f]), '->', int(post[f]), 'peso', int(w[f]), 'tipo_origen', str(tipo[pre[f]]), flush=True)
    else:
        print('QWEAK', c, 'sin_fila_elegible', flush=True)
    print('DPRIME', c, 'n', int(Dp.size), 'sha256', h_dp(Dp), flush=True)

for h, (x, G, nd, eq, ex) in ESP_H.items():
    Dp = dprime(x, G)
    chk(h + ' nDp_conj', int(Dp.size), nd)
    chk(h + ' QCOL_conj', tupla(f_qcol(G, Dp)), eq)
    chk(h + ' QXD_conj', tupla(f_qxd(x, Dp)), ex)
    print('DPRIME', h, 'n', int(Dp.size), 'sha256', h_dp(Dp), 'drivers', [(g, str(tipo[g]), int(sl[g])) for g in G], flush=True)

za = desde(6128); za = za[post[za] == 59804]
q1r01 = desde(59804); q1r01 = q1r01[post[q1r01] == 30887]
chk('ZA', tupla(za), (1, 388))
chk('ZAuQ1_R01', tupla(np.concatenate([za, q1r01])), (2, 623))
chk('Q6', tupla(desde(6128)), (1677, 18623))
chk('Q6uQ1_R01', tupla(np.concatenate([desde(6128), q1r01])), (1678, 18858))

lado = {'right': int(sl[95123])}
idx_izq = np.where(root == 720575940604954289)[0]
lado['left'] = int(sl[idx_izq[0]]) if idx_izq.size else None
print('CODIGO_LADO', lado, flush=True)
for nom, esp in ESP_POB.items():
    t, s = nom.rsplit('_', 1)
    miembros = np.where((tipo == t) & (sl == lado[s]) & (Su >= 0) & (~inh))[0]
    obt = int(miembros.size) if isinstance(esp, int) else [int(i) for i in miembros]
    chk('POB ' + nom, obt, esp)
for d, (tipos, esp) in ESP_PRE.items():
    r = hacia(d); r = r[(w[r] > 0) & np.isin(tipo[pre[r]], list(tipos))]
    chk('PRE_A driver ' + str(d), sorted(int(i) for i in np.unique(pre[r])), sorted(esp))


# ---- v2: identidad exacta contra la salida JSON publicada de 010 ----
texto = open(EVID010, encoding='utf-8').read()
sal = None; i = texto.find('{"')
while i != -1:
    try:
        obj, _ = json.JSONDecoder().raw_decode(texto[i:])
        if isinstance(obj, dict) and 'relay' in obj and 'joint' in obj:
            sal = obj; break
    except ValueError:
        pass
    i = texto.find('{"', i + 1)
if sal is None:
    print('EVID010 sin JSON de salida'); sys.exit(2)
def huella(pop):
    v = sorted(int(t) for t in pop)
    return hashlib.sha256((json.dumps(v, separators=(',', ':')) + '\n').encode()).hexdigest()
POB_DE = {}
for r in sello:
    POB_DE[r['code'][:3]] = r['regimen_visual_S']
PRE_DE = {'R04': 27878, 'R09': 27878, 'R07': 130297, 'R14': 104203}
for e in sal['relay']:
    c = e['id']; d, x = e['driver'], e['hub']
    Dp = dprime(x, [d])
    chk(c + ' huella_Dp', (int(Dp.size), huella(Dp)), (e['Dprime']['n'], e['Dprime']['sha256_indices_json_lf']))
    rin = hacia(x)
    rin2 = rin[(w[rin] > 0) & Dset[pre[rin]] & (pre[rin] != d) & (con[rin] >= 1) & (con[rin] <= 5)]
    m = con[rin2].max(); cand = rin2[con[rin2] == m]; f = cand[np.argmin(pre[cand])]
    chk(c + ' QWEAK', (int(pre[f]), int(post[f]), int(w[f])), (e['weak_row']['pre'], e['weak_row']['post'], e['weak_row']['weight']))
    if c in PRE_DE:
        tipos = ESP_PRE[PRE_DE[c]][0]
        rr = hacia(d); rr = rr[(w[rr] > 0) & np.isin(tipo[pre[rr]], list(tipos))]
        A = np.unique(pre[rr])
    else:
        t, sd = POB_DE[c].rsplit('_', 1)
        A = np.where((tipo == t) & (sl == lado[sd]) & (Su >= 0) & (~inh))[0]
    chk(c + ' huella_A', (int(A.size), huella(A)), (e['A_population']['n'], e['A_population']['sha256_indices_json_lf']))
    ra = hacia(d); ra = ra[np.isin(pre[ra], A)]
    chk(c + ' peso_A_a_driver', int(np.abs(w[ra]).sum()), e['A_input_weight_to_driver'])
    chk(c + ' lado_driver', int(sl[d]), e['driver_side_code'])
for e in sal['joint']:
    h = e['id']; x = e['hub']; G = e['drivers']
    Dp = dprime(x, G)
    q1 = f_q1(G, x); qcol = f_qcol(G, Dp); qxd = f_qxd(x, Dp)
    chk(h + ' huella_Dp_conj', (int(Dp.size), huella(Dp)), (e['Dprime']['n'], e['Dprime']['sha256_indices_json_lf']))
    chk(h + ' Q1conjuQCOL', list(tupla(np.concatenate([q1, qcol]))), e['Q1_union_QCOL'])
    chk(h + ' Q1conjuQXD', list(tupla(np.concatenate([q1, qxd]))), e['Q1_union_QXD'])
    rin = hacia(x)
    rin2 = rin[(w[rin] > 0) & Dset[pre[rin]] & ~np.isin(pre[rin], G) & (con[rin] >= 1) & (con[rin] <= 5)]
    m = con[rin2].max(); cand = rin2[con[rin2] == m]; f = cand[np.argmin(pre[cand])]
    chk(h + ' QWEAK_conj', (int(pre[f]), int(post[f]), int(w[f])), (e['weak_row']['pre'], e['weak_row']['post'], e['weak_row']['weight']))

print('GUARDAS_A1_BRAIN', ok, '/', tot, 'DIFERENTES', dif, 'segundos', round(time.time() - t0, 1), flush=True)
sys.exit(0 if ok == tot else 1)
