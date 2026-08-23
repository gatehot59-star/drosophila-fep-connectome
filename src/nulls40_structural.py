# TITAN v5.4 - 40 nulls Maslov-Sneppen sobre el conectoma real de Drosophila
# Preserva grado entrante Y saliente exactos. Sin auto-lazos, sin multi-aristas.
# Mide SOLO la capa estructural: conteos puros. Sin normalizacion, sin tau,
# sin entropia, sin propagacion. Es la capa que sobrevivio a la auditoria.
# Anotaciones PINNEADAS al SHA del commit (V-01): la rama main viva muto.
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

if not os.path.exists(PARQUET):
    lg("descargando parquet")
    urllib.request.urlretrieve(PURL, PARQUET)
if not os.path.exists(ANNOT):
    lg("descargando anotaciones pinneadas al SHA " + ASHA)
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
lg("md5 parquet     = " + MD5P + "  bytes=" + str(os.path.getsize(PARQUET)))
lg("md5 annotations = " + MD5A + "  bytes=" + str(os.path.getsize(ANNOT)))

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
lg("ids unicos en el grafo = " + str(uid.shape[0]))

ann = pd.read_csv(ANNOT, sep=chr(9), low_memory=False)
lg("filas TSV = " + str(ann.shape[0]))
rid = ann["root_id"].values.astype(np.int64)
ccv = ann["cell_class"].astype(str).values
scv = ann["super_class"].astype(str).values
flv = ann["flow"].astype(str).values
ppos = np.minimum(np.searchsorted(uid, rid), uid.shape[0] - 1)
hit = uid[ppos] == rid
ix = uix[ppos]
lg("filas mapeadas al grafo = " + str(int(hit.sum())))

GN = ["other", "visual", "olfactory", "mechano", "gustatory", "hygro", "thermo", "AN", "unk_sens", "MOTOR", "KenyonCell", "MBON", "DAN", "MBIN", "ALPN", "optic_intr"]
G = len(GN)
CMAP = {"visual": 1, "olfactory": 2, "mechanosensory": 3, "gustatory": 4, "hygrosensory": 5, "thermosensory": 6, "AN": 7, "unknown_sensory": 8, "Kenyon_Cell": 10, "MBON": 11, "DAN": 12, "MBIN": 13, "ALPN": 14}
g = np.zeros(N, dtype=np.int64)
ismot = (scv == "descending") | (scv == "motor") | (flv == "efferent")
for k in range(rid.shape[0]):
    if not hit[k]:
        continue
    t = int(ix[k])
    if ismot[k]:
        g[t] = 9
        continue
    c = ccv[k]
    if c in CMAP:
        g[t] = CMAP[c]
    elif scv[k] == "optic":
        g[t] = 15
gc = np.bincount(g, minlength=G)
lg("grupos: " + " ".join([GN[i] + "=" + str(int(gc[i])) for i in range(G)]))
lg("suma grupos = " + str(int(gc.sum())) + "  (N=" + str(N) + ")")

NN = np.int64(N)
def kk(a, b):
    return a * NN + b

def medir(p):
    K = np.sort(kk(pre, p))
    rk = kk(p, pre)
    q = np.minimum(np.searchsorted(K, rk), K.shape[0] - 1)
    rec = int(((K[q] == rk) & (pre != p)).sum())
    cell = g[pre] * G + g[p]
    Ma = np.bincount(cell, minlength=G * G)
    Me = np.bincount(cell[exc], minlength=G * G)
    Ms = np.bincount(cell, weights=syn.astype(np.float64), minlength=G * G)
    return rec, Ma, Me, Ms, K

din0 = np.bincount(post0, minlength=N)
dout0 = np.bincount(pre, minlength=N)
rec0, Ma0, Me0, Ms0, K0 = medir(post0)
dens = float(K0.shape[0]) / (float(N) * float(N - 1))
lg("REAL aristas_unicas=" + str(int(K0.shape[0])) + "  reciprocas=" + str(rec0) + "  densidad=" + format(dens, ".9f"))

NNULL = 40
SWF = 3
TARGET = SWF * E
B = 2000000
res = {}
res["meta"] = {"N": N, "E": E, "G": G, "GN": GN, "gc": gc.tolist(), "md5_parquet": MD5P, "md5_annot": MD5A, "annot_sha": ASHA, "swap_factor": SWF, "target_swaps": TARGET, "n_nulls": NNULL, "densidad": dens, "sinapsis": int(syn.sum())}
res["real"] = {"rec": rec0, "aristas_unicas": int(K0.shape[0]), "Ma": Ma0.tolist(), "Me": Me0.tolist(), "Ms": Ms0.tolist()}
res["nulls"] = []
lg("objetivo de swaps por null = " + str(TARGET) + "   nulls = " + str(NNULL))

for it in range(NNULL):
    t1 = time.time()
    rng = np.random.default_rng(4200 + 17 * it)
    p = post0.copy()
    K = np.sort(kk(pre, p))
    hechos = 0
    lotes = 0
    while hechos < TARGET:
        lotes = lotes + 1
        i = rng.integers(0, E, B)
        j = rng.integers(0, E, B)
        a = pre[i]
        b = p[i]
        c = pre[j]
        d = p[j]
        ok = (i != j) & (b != d) & (a != d) & (c != b)
        i = i[ok]
        j = j[ok]
        a = a[ok]
        b = b[ok]
        c = c[ok]
        d = d[ok]
        if i.shape[0] == 0:
            continue
        cnt = np.zeros(E, dtype=np.int8)
        np.add.at(cnt, np.concatenate([i, j]), 1)
        keep = (cnt[i] == 1) & (cnt[j] == 1)
        del cnt
        i = i[keep]
        j = j[keep]
        a = a[keep]
        b = b[keep]
        c = c[keep]
        d = d[keep]
        if i.shape[0] == 0:
            continue
        k1 = kk(a, d)
        k2 = kk(c, b)
        q1 = np.minimum(np.searchsorted(K, k1), K.shape[0] - 1)
        q2 = np.minimum(np.searchsorted(K, k2), K.shape[0] - 1)
        libre = (K[q1] != k1) & (K[q2] != k2) & (k1 != k2)
        i = i[libre]
        j = j[libre]
        b = b[libre]
        d = d[libre]
        k1 = k1[libre]
        k2 = k2[libre]
        if i.shape[0] == 0:
            continue
        u2, c2 = np.unique(np.concatenate([k1, k2]), return_counts=True)
        dups = u2[c2 > 1]
        if dups.shape[0] > 0:
            bien = ~(np.isin(k1, dups) | np.isin(k2, dups))
            i = i[bien]
            j = j[bien]
            b = b[bien]
            d = d[bien]
            k1 = k1[bien]
            k2 = k2[bien]
        if i.shape[0] == 0:
            continue
        vieja = np.concatenate([kk(pre[i], b), kk(pre[j], d)])
        p[i] = d
        p[j] = b
        K = np.setdiff1d(K, vieja, assume_unique=True)
        K = np.sort(np.concatenate([K, k1, k2]))
        hechos = hechos + int(i.shape[0])
    malin = int((np.bincount(p, minlength=N) != din0).sum())
    malout = int((np.bincount(pre, minlength=N) != dout0).sum())
    recN, MaN, MeN, MsN, KN = medir(p)
    res["nulls"].append({"i": it, "swaps": hechos, "lotes": lotes, "aristas_unicas": int(KN.shape[0]), "indeg_malos": malin, "outdeg_malos": malout, "rec": recN, "Ma": MaN.tolist(), "Me": MeN.tolist(), "Ms": MsN.tolist()})
    lg("null " + str(it) + "  swaps=" + str(hechos) + "  lotes=" + str(lotes) + "  aristas=" + str(int(KN.shape[0])) + "  indeg_malos=" + str(malin) + "  outdeg_malos=" + str(malout) + "  rec=" + str(recN) + "  [" + format(time.time() - t1, ".1f") + "s]")
    f = open(os.path.join(OUT, "nulls40.json"), "w")
    json.dump(res, f)
    f.close()

lg("FIN  nulls=" + str(len(res["nulls"])) + "  minutos=" + format((time.time() - T0) / 60.0, ".1f"))
print("FINNULLS40", flush=True)
