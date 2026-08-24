# TITAN v5.4 - 40 nulls COMMUNITY-PRESERVING sobre la capa estructural.
# Cierra el hueco declarado: reciprocidad, KC->MBON y la jerarquia de ruteo
# estaban testeadas solo contra nulls que preservan GRADO (Maslov-Sneppen).
# Este kernel las testea contra nulls que preservan grado Y la matriz de
# conectividad entre super_clases, o sea la arquitectura modular intacta.
#
# El generador CP replica el del analisis de los 12 pares: para cada bloque
# (super_class del emisor, super_class del receptor) se baraja la columna de
# destinos entre las aristas del bloque. Eso preserva el multiconjunto de
# destinos por bloque, y por lo tanto el grado entrante exacto de cada nodo,
# y el grado saliente porque la columna de emisores nunca se toca.
#
# ADVERTENCIA MEDIDA, no supuesta: el CP SI puede crear multi-aristas, a
# diferencia del MS. El kernel las cuenta por null y lo reporta.
import os, json, time, hashlib, urllib.request
import numpy as np
import pandas as pd

T0 = time.time()
def lg(s):
    print("[" + format(time.time() - T0, ".1f") + "s] " + str(s), flush=True)

OUT = "/kaggle/working"
DATA = "/kaggle/working/datos"
os.makedirs(DATA, exist_ok=True)
PARQUET = os.path.join(DATA, "connectivity.parquet")
ANNOT = os.path.join(DATA, "annotations.tsv")
PURL = "https://raw.githubusercontent.com/eonsystemspbc/fly-brain/main/data/2025_Connectivity_783.parquet"
ASHA = "17fc57722002e1a7d38cdd0c89ac382bf92718da"
AURL = "https://raw.githubusercontent.com/flyconnectome/flywire_annotations/" + ASHA + "/supplemental_files/Supplemental_file1_neuron_annotations.tsv"
MD5P_OK = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5A_OK = "719904abad876c68ace1b5690c9b9b63"

if not os.path.exists(PARQUET):
    urllib.request.urlretrieve(PURL, PARQUET)
if not os.path.exists(ANNOT):
    urllib.request.urlretrieve(AURL, ANNOT)

def md5(path):
    h = hashlib.md5()
    f = open(path, "rb")
    while True:
        b = f.read(1048576)
        if not b:
            break
        h.update(b)
    f.close()
    return h.hexdigest()

MD5P = md5(PARQUET)
MD5A = md5(ANNOT)
lg("md5 parquet     = " + MD5P + "   " + ("OK" if MD5P == MD5P_OK else "DISTINTO"))
lg("md5 annotations = " + MD5A + "   " + ("OK" if MD5A == MD5A_OK else "DISTINTO"))

df = pd.read_parquet(PARQUET)
pre = df["Presynaptic_Index"].values.astype(np.int64)
post0 = df["Postsynaptic_Index"].values.astype(np.int64)
exc = df["Excitatory x Connectivity"].values.astype(np.int64) > 0
syn = df["Connectivity"].values.astype(np.int64)
preid = df["Presynaptic_ID"].values.astype(np.int64)
postid = df["Postsynaptic_ID"].values.astype(np.int64)
N = int(max(pre.max(), post0.max())) + 1
E = int(pre.shape[0])
lg("N=" + str(N) + "  E=" + str(E) + "  sinapsis=" + str(int(syn.sum())))

allid = np.concatenate([preid, postid])
allix = np.concatenate([pre, post0])
o = np.argsort(allid, kind="stable")
allid = allid[o]
allix = allix[o]
uid, firstpos = np.unique(allid, return_index=True)
uix = allix[firstpos]
del allid, allix, o, preid, postid, df

ann = pd.read_csv(ANNOT, sep=chr(9), low_memory=False)
rid = ann["root_id"].values.astype(np.int64)
ccv = ann["cell_class"].astype(str).values
scv = ann["super_class"].astype(str).values
flv = ann["flow"].astype(str).values
ppos = np.minimum(np.searchsorted(uid, rid), uid.shape[0] - 1)
hit = uid[ppos] == rid
ix = uix[ppos]
lg("filas TSV = " + str(ann.shape[0]) + "   mapeadas = " + str(int(hit.sum())))

# REG = super_class, el mismo orden y el mismo unk=10 del analisis de los 12 pares.
SC = ["central", "visual_projection", "endocrine", "descending", "optic", "motor", "visual_centrifugal", "sensory", "ascending", "sensory_ascending"]
NR = 11
SCIX = {}
for i in range(len(SC)):
    SCIX[SC[i]] = i
reg = np.full(N, 10, dtype=np.int64)

# Grupos funcionales, identicos a los del analisis MS para que las dos
# corridas sean comparables fila por fila.
GN = ["other", "visual", "olfactory", "mechano", "gustatory", "hygro", "thermo", "AN", "unk_sens", "MOTOR", "KenyonCell", "MBON", "DAN", "MBIN", "ALPN", "optic_intr"]
G = len(GN)
CMAP = {"visual": 1, "olfactory": 2, "mechanosensory": 3, "gustatory": 4, "hygrosensory": 5, "thermosensory": 6, "AN": 7, "unknown_sensory": 8, "Kenyon_Cell": 10, "MBON": 11, "DAN": 12, "MBIN": 13, "ALPN": 14}
g = np.zeros(N, dtype=np.int64)
ismot = (scv == "descending") | (scv == "motor") | (flv == "efferent")
for k in range(rid.shape[0]):
    if not hit[k]:
        continue
    t = int(ix[k])
    s = scv[k]
    if s in SCIX:
        reg[t] = SCIX[s]
    if ismot[k]:
        g[t] = 9
        continue
    c = ccv[k]
    if c in CMAP:
        g[t] = CMAP[c]
    elif s == "optic":
        g[t] = 15

regc = np.bincount(reg, minlength=NR).tolist()
gc = np.bincount(g, minlength=G)
REG_OK = [32379, 8038, 76, 1299, 77530, 110, 524, 16352, 1736, 581, 14]
GC_OK = [34668, 10855, 2279, 2656, 408, 74, 29, 2231, 131, 1485, 5177, 96, 331, 4, 685, 77530]
lg("super_class = " + str(regc))
lg("   esperado  = " + str(REG_OK) + "   " + ("OK" if regc == REG_OK else "DISTINTO"))
lg("grupos      = " + str(gc.tolist()))
lg("   esperado  = " + str(GC_OK) + "   " + ("OK" if gc.tolist() == GC_OK else "DISTINTO"))
lg("suma grupos = " + str(int(gc.sum())) + "  (N=" + str(N) + ")")

# Bloques CP: (super_class emisor, super_class receptor).
key = reg[pre] * NR + reg[post0]
srt = np.argsort(key, kind="stable")
ks = key[srt]
uk = np.unique(ks)
st_i = np.searchsorted(ks, uk, side="left")
en_i = np.searchsorted(ks, uk, side="right")
blocks = []
for bi in range(uk.shape[0]):
    blocks.append(srt[st_i[bi]:en_i[bi]])
lg("bloques CP = " + str(len(blocks)) + "   aristas cubiertas = " + str(int(sum([b.size for b in blocks]))))

NN = np.int64(N)
def kk(a, b):
    return a * NN + b

din0 = np.bincount(post0, minlength=N)
dout0 = np.bincount(pre, minlength=N)

def medir(p):
    K = np.sort(kk(pre, p))
    uniq = int(np.unique(K).shape[0])
    rk = kk(p, pre)
    q = np.minimum(np.searchsorted(K, rk), K.shape[0] - 1)
    rec = int(((K[q] == rk) & (pre != p)).sum())
    cell = g[pre] * G + g[p]
    Ma = np.bincount(cell, minlength=G * G)
    Me = np.bincount(cell[exc], minlength=G * G)
    malin = int((np.bincount(p, minlength=N) != din0).sum())
    return rec, Ma, Me, uniq, malin

def gen_cp(seed):
    sd = int(seed)
    p = post0.copy()
    for ei in blocks:
        m = int(ei.size)
        if m < 2:
            continue
        bc = p[ei].tolist()
        for i in range(m - 1, 0, -1):
            sd = (sd * 48271) % 2147483647
            j = int((sd / 2147483647.0) * (i + 1))
            tmp = bc[i]
            bc[i] = bc[j]
            bc[j] = tmp
        p[ei] = bc
    return p

rec0, Ma0, Me0, uniq0, malin0 = medir(post0)
lg("REAL  reciprocas=" + str(rec0) + "  aristas_unicas=" + str(uniq0) + "  indeg_malos=" + str(malin0))

NNULL = 40
res = {}
res["meta"] = {"N": N, "E": E, "G": G, "GN": GN, "gc": gc.tolist(), "NR": NR, "n_bloques": len(blocks), "md5_parquet": MD5P, "md5_annot": MD5A, "annot_sha": ASHA, "n_nulls": NNULL, "null": "community-preserving (super_class blocks)"}
res["real"] = {"rec": rec0, "aristas_unicas": uniq0, "Ma": Ma0.tolist(), "Me": Me0.tolist()}
res["nulls"] = []
SEEDS = []
for i in range(NNULL):
    SEEDS.append(42 + i * 2000)
res["seeds"] = SEEDS
lg("arrancan " + str(NNULL) + " nulls CP, semillas " + str(SEEDS[0]) + ".." + str(SEEDS[-1]))

for it in range(NNULL):
    t1 = time.time()
    p = gen_cp(SEEDS[it])
    rec, Ma, Me, uniq, malin = medir(p)
    dup = E - uniq
    res["nulls"].append({"i": it, "seed": SEEDS[it], "rec": rec, "aristas_unicas": uniq, "duplicadas": dup, "indeg_malos": malin, "Ma": Ma.tolist(), "Me": Me.tolist()})
    lg("CP " + str(it + 1).rjust(2) + "/40  seed=" + str(SEEDS[it]).rjust(6) + "  rec=" + str(rec).rjust(9) + "  unicas=" + str(uniq) + "  dup=" + str(dup) + "  indeg_malos=" + str(malin) + "  [" + format(time.time() - t1, ".0f") + "s]")
    f = open(os.path.join(OUT, "cp40.json"), "w")
    json.dump(res, f)
    f.close()

# ================== REPORTE ==================
# Los valores MS vienen de la corrida de 40 nulls Maslov-Sneppen ya hecha
# (results/nulls40.json del repo). Se citan para que las dos familias queden
# lado a lado en la misma tabla.
MS = {}
MS["rec"] = (84932.3, 401.4, 47.27, 0)
MS["KC->MBON"] = (2567.7, 47.5, 24.25, 0)
MS["DAN->KC"] = (1734.7, 38.6, 27.33, 0)
MS["KC->KC"] = (12614.1, 115.8, 23.29, 0)
MS["MBON->MOTOR"] = (890.6, 33.5, 0.41, 40)
MS["mechano->KC"] = (2639.9, 52.1, 0.0, 40)
MS["olfactory->KC"] = (2607.5, 49.1, 0.0, 40)
MS["visual->KC"] = (1532.5, 38.0, 0.0, 40)
MS["ALPN->KC"] = (5184.1, 74.2, 5.37, 0)
MSMOT = {"visual": (946.1, 0.145, 40), "olfactory": (2337.2, 0.034, 40), "mechano": (2374.0, 9.693, 0), "gustatory": (583.7, 2.193, 0), "hygro": (126.5, 0.103, 40), "thermo": (59.3, 0.236, 40), "AN": (3760.7, 7.407, 0), "unk_sens": (175.7, 6.709, 0)}

def stats(arr):
    n = len(arr)
    m = sum(arr) / n
    v = 0.0
    for x in arr:
        v = v + (x - m) * (x - m)
    sd = (v / (n - 1)) ** 0.5
    return m, sd

def linea(nombre, obs, arr, msk):
    m, sd = stats(arr)
    ge = len([x for x in arr if x >= obs])
    le = len([x for x in arr if x <= obs])
    ratio = obs / m if m > 0 else float("inf")
    z = (obs - m) / sd if sd > 0 else float("nan")
    p = (min(ge, le) + 1.0) / (len(arr) + 1.0)
    msinfo = ""
    if msk is not None and msk in MS:
        msinfo = "   MS: " + format(MS[msk][2], ".2f") + "x  n_ge=" + str(MS[msk][3])
    lg("  " + nombre.ljust(16) + "obs=" + str(obs).rjust(8) + "  CP_mu=" + format(m, ".1f").rjust(10) + "  sd=" + format(sd, ".1f").rjust(8) + "  ratio=" + (format(ratio, ".2f") + "x").rjust(9) + "  z=" + format(z, ".1f").rjust(8) + "  n_ge=" + str(ge).rjust(2) + "/40  p=" + format(p, ".4f") + msinfo)
    return {"obs": obs, "cp_mu": m, "cp_sd": sd, "ratio": ratio, "z": z, "n_ge": ge, "n_le": le, "p": p}

lg("")
lg("########## RECIPROCIDAD contra 40 nulls CP ##########")
R = {}
R["reciprocidad"] = linea("reciprocas", rec0, [x["rec"] for x in res["nulls"]], "rec")

lg("")
lg("########## CIRCUITO DE APRENDIZAJE contra 40 nulls CP ##########")
PARES = [(10, 11, "KC->MBON"), (12, 10, "DAN->KC"), (12, 11, "DAN->MBON"), (10, 10, "KC->KC"), (11, 9, "MBON->MOTOR"), (3, 10, "mechano->KC"), (2, 10, "olfactory->KC"), (1, 10, "visual->KC"), (14, 10, "ALPN->KC")]
for a, b, nm in PARES:
    obs = int(Ma0[a * G + b])
    arr = [int(x["Ma"][a * G + b]) for x in res["nulls"]]
    R[nm] = linea(nm, obs, arr, nm)

lg("")
lg("########## ACCESO MOTOR EXCITATORIO contra 40 nulls CP ##########")
MOT = 9
CLASES = [(1, "visual"), (2, "olfactory"), (3, "mechano"), (4, "gustatory"), (5, "hygro"), (6, "thermo"), (7, "AN"), (8, "unk_sens")]
filas = []
for gi, nm in CLASES:
    obs = int(Me0[gi * G + MOT])
    arr = [int(x["Me"][gi * G + MOT]) for x in res["nulls"]]
    m, sd = stats(arr)
    ge = len([x for x in arr if x >= obs])
    le = len([x for x in arr if x <= obs])
    ratio = obs / m if m > 0 else float("inf")
    msr = MSMOT[nm][1]
    cambia = "SI" if ((ratio > 1.0) != (msr > 1.0)) else "no"
    lg("  " + nm.ljust(11) + "obs=" + str(obs).rjust(7) + "  CP_mu=" + format(m, ".1f").rjust(10) + "  ratio_CP=" + (format(ratio, ".3f") + "x").rjust(9) + "  ratio_MS=" + (format(msr, ".3f") + "x").rjust(9) + "  n_ge=" + str(ge).rjust(2) + "/40  p=" + format((min(ge, le) + 1.0) / 41.0, ".4f") + "  cambia_signo=" + cambia)
    filas.append({"clase": nm, "obs": obs, "cp_mu": m, "ratio_cp": ratio, "ratio_ms": msr, "n_ge": ge, "cambia_signo": cambia})
R["acceso_motor"] = filas
rr = [f["ratio_cp"] for f in filas]
lg("")
lg("  rango CP = " + format(max(rr) / min(rr), ".1f") + "x   (contra grado preservado fue 283.2x, contra densidad uniforme 991x)")
nsigno = len([f for f in filas if f["cambia_signo"] == "SI"])
lg("  clases que cambian de signo respecto al null MS: " + str(nsigno) + "/8")

lg("")
lg("########## VALIDACION DEL NULL ##########")
lg("  indeg_malos por null: " + str(sorted(set([x["indeg_malos"] for x in res["nulls"]]))))
lg("  duplicadas: min=" + str(min([x["duplicadas"] for x in res["nulls"]])) + "  max=" + str(max([x["duplicadas"] for x in res["nulls"]])) + "   (el CP admite multi-aristas por diseno; el MS no)")
res["analisis"] = R
f = open(os.path.join(OUT, "cp40.json"), "w")
json.dump(res, f)
f.close()
lg("")
lg("FIN  minutos=" + format((time.time() - T0) / 60.0, ".1f"))
print("FINCP40", flush=True)
