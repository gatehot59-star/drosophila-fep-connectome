#!/usr/bin/env python3
"""H_RIVAL y H_TAU_JUSTO: instrumento del sello tools/rival/SELLO-RIVAL.md (commit 05a574c). Respuesta 2026-10-14-033.

Por celda se regeneran los ensayos de H_TAU (entrenamiento: tm.generar(2400, 1) con ruido 101; pruebas 2 a 21:
tm.generar(2000, p) con ruido 1000 + p). Cada rival elige entre 10 candidatas por validacion cruzada de 5 pliegues
(indice del ensayo modulo 5) sobre los 2.400 ensayos, se reajusta con los 2.400 y recien ahi ve las pruebas. W no se
recalcula: se lee de los json sellados de H_TAU (primaria) y del factorial 3 (secundaria); REPRO_W prueba el pareo.
  RIDGE      forma dual de ept._ridge_fit (penalidad lambda * n), rasgos estandarizados con el conjunto de ajuste,
             un lambda para los dos estados, empate al lambda mas grande.
  MLP        el bucle de ept.mlp_mux linea por linea (32 tanh, Adam 1e-2, weight decay 1e-4, lote 256, 300
             iteraciones, float32), con las clases de tm.CLASES: ept.mlp_mux trae fijas las clases de la 005, que no
             son las de esta tarea. CONTROL_MLP_005 compara el envoltorio con ept.mlp_mux con etiquetas de la 005.
  REGLA_TAU  lc de H_TAU con un integrador con fuga por canal (t_k = 0,02 / tau_k), tm.lineas, umbrales y carrera.
Modos: --celda A|ruido; --solo_015 (CONTROL_RIDGE_015); --humo (controles a tamano completo y rutas de los rivales
con 600 y 200 ensayos en la semilla 99, sin aciertos). Salida: 0 completo; 2 insumos distintos del pin; 3 control.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools", "htau"))
import htau_mosca as ht  # noqa: E402  sellado (2006cfef), sin cambios
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402
import torch.nn.functional as F  # noqa: E402

f2, tm, base = ht.f2, ht.tm, ht.base
ept = tm.ept
NL = chr(10)

MD5_MOD = {
    "factorial2_mosca.py": "798a824cd47808155fa12adb9e652dac",
    "tarea_mosca.py": "40d64e074d9163753439307c5be4ac5e",
    "entrada_por_tipos.py": "e060c4bffb685aa550dadc19eda3dd02",
    "escape_aterrizaje_dbc3.py": "4d40477d87406c31672acfb6e6e8f5a2",
    "htau_mosca.py": "2006cfef6eaffc023086fd35fbe20f64",
}
MD5_CONN = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_ANNOT = "719904abad876c68ace1b5690c9b9b63"
MD5_HTAU = ("4e796c3f7b4aae9de395dcfdf0a37b31", "0e9f41ab1b28d9ab5a191f3e4907d2b0", "2cbab449f48cb4cd0102d8ba2f4f812b",
            "aca01a833db117cf96c755168ae56834", "7849f2b656097c42b5fe0b714f78e566", "0ef2ee1146f3829cafc985619c992104")
MD5_F3SUMS = "3fb0f772ecf2659760697ab38616a2b3"
MD5_LOG015 = "ad8c94b47350b5473b13848150047ab4"
DIR_HTAU = os.path.join(RAIZ, "results", "htau_2026-10-14")
DIR_F3 = os.path.join(RAIZ, "results", "factorial3_2026-10-13")
LOG015 = os.path.join(RAIZ, "results", "tarea_mosca_2026-10-12", "completa.log")

RIVALES = ("RIDGE", "MLP", "REGLA_TAU")
PRIMARIA = list(range(12, 22))
SECUNDARIA = list(range(2, 12))
TAUS_F3 = list(range(10))
PLIEGUES = 5
LAMBDAS_R = (1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 1e2, 1e3, 1e4, 1e5)
SEM_MLP = list(range(10))
SEM_RT = list(range(10, 20))
MLP_ITERS, MLP_H, MLP_LR, MLP_LOTE, MLP_WD = 300, 32, 1e-2, 256, 1e-4
DT = 0.02
SEM_PERM = 2033
MARGEN_NEG = 0.05
ESPERADO_015 = {(0.0, 0.15): 0.9935, (0.0, 0.45): 0.9595, (0.3, 0.15): 0.9935,
                (0.3, 0.45): 0.9575, (0.6, 0.15): 0.9940, (0.6, 0.45): 0.9590}
TOL_015 = 0.0010
HUMO_TR, HUMO_TE, HUMO_SEM, HUMO_ITERS = 600, 200, 99, 20
GRUPOS = (("L", ("LC4", "LPLC2")), ("R", ("LC4", "LPLC2")), ("L", ("LPLC4",)), ("R", ("LPLC4",)),
          ("L", ("LPLC1", "LPLC2")), ("R", ("LPLC1", "LPLC2")))


def pr(s):
    print(s, flush=True)


def md5(ruta):
    h = hashlib.md5()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def clave(A, s):
    return "%.1f|%.2f" % (A, s)


def a_str(p):
    return "".join(map(str, p.tolist()))


def de_str(s):
    return np.frombuffer(s.encode("ascii"), dtype=np.uint8).astype(np.int64) - 48


def pines(conn, annot):
    ok = {}
    for mod in (f2, tm, ept, base, ht):
        nom = os.path.basename(mod.__file__)
        ok["md5_" + nom] = bool(MD5_MOD.get(nom) == md5(os.path.abspath(mod.__file__)))
    ok["md5_conn"] = bool(md5(conn) == MD5_CONN)
    ok["md5_annot"] = bool(md5(annot) == MD5_ANNOT)
    for c in range(6):
        ok["md5_htau_c%d" % c] = bool(md5(os.path.join(DIR_HTAU, "htau_c%d.json" % c)) == MD5_HTAU[c])
    sums = os.path.join(DIR_F3, "MD5SUMS.txt")
    ok["md5_f3_MD5SUMS"] = bool(md5(sums) == MD5_F3SUMS)
    lista = {}
    for x in open(sums).read().split(NL):
        partes = x.split()
        if len(partes) == 2 and partes[1].startswith("factorial2_R2_CON_TASA_t") and partes[1].endswith(".json"):
            lista[partes[1]] = partes[0]
    ok["f3_60_json"] = bool(len(lista) == 60 and all(md5(os.path.join(DIR_F3, k)) == v for k, v in lista.items()))
    ok["md5_completa_log_015"] = bool(md5(LOG015) == MD5_LOG015)
    return ok


# ---------------- datos (los de H_TAU) ----------------
def sujeto_r2(conn, annot):
    S = f2.sujeto(conn, annot, "R2", "CON")
    n_ent = S["n_ent"]
    tipos, lados = S["tipos"], S["lados"]
    suj = dict(ids=list(S["ids"][:n_ent]), n_ent=n_ent,
               chan=np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(n_ent)]),
               mascaras=[np.array([lados[i] == ld and tipos[i] in ts for i in range(n_ent)]) for ld, ts in GRUPOS],
               ok=bool((S["n_U"], S["n_ar_crudo"]) == f2.R2_ESPERADO and S["contiene_m46"] and S["contiene_r1"]))
    del S
    return suj


def ensayos(suj, A, s, n, sem_gen, sem_ruido):
    e = tm.generar(n, sem_gen)
    Z = f2.ruido_por_root(suj["ids"], n, sem_ruido)
    X = tm.sintonias(e, A)[:, :, suj["chan"]] + s * Z
    return e["y"], e["vuelo"], X


def lc_de(X, suj):
    return np.stack([X[:, :, m].mean(2) for m in suj["mascaras"]], axis=2)


def pliegues(n):
    f = np.arange(n) % PLIEGUES
    return [(np.where(f != j)[0], np.where(f == j)[0]) for j in range(PLIEGUES)]


# ---------------- RIDGE ----------------
def _dual(A, Y, lams):
    """Forma dual de ept._ridge_fit. A es una copia propia: se centra en el lugar."""
    am, ym = A.mean(0), Y.mean(0)
    A -= am
    e, V = np.linalg.eigh(A @ A.T)
    R = V.T @ (Y - ym)
    n = len(A)
    return A, am, ym, [V @ (R / (e + lam * n)[:, None]) for lam in lams]


def ridge_ajustar(X, y, v, idx, lams):
    mods = {}
    for s in (True, False):
        ii = idx[v[idx] == s]
        cl = tm.CLASES[s]
        A = X[ii]
        mu, sd = A.mean(0), A.std(0) + 1e-6
        A -= mu
        A /= sd
        Y = np.eye(len(cl))[np.searchsorted(cl, y[ii])]
        mods[s] = (mu, sd, cl) + tuple(_dual(A, Y, lams))
    return mods


def ridge_predecir(mods, X, v, idx):
    nl = len(mods[True][6])
    P = np.zeros((nl, len(idx)), dtype=np.int64)
    for s, (mu, sd, cl, Ac, am, ym, alfas) in mods.items():
        sel = np.where(v[idx] == s)[0]
        if len(sel) == 0:
            continue
        Bm = X[idx[sel]]
        Bm -= mu
        Bm /= sd
        Bm -= am
        G = Bm @ Ac.T
        for k, al in enumerate(alfas):
            P[k, sel] = cl[(G @ al + ym).argmax(1)]
    return P


def cv_ridge(Fm, y, v, pl, lams):
    acc = np.zeros((len(pl), len(lams)))
    for j, (ia, it) in enumerate(pl):
        mods = ridge_ajustar(Fm, y, v, ia, lams)
        acc[j] = (ridge_predecir(mods, Fm, v, it) == y[it][None, :]).mean(1)
        del mods
    return acc.mean(0), acc


def ridge_015(Xtr, ytr, Xte, clases):
    """El protocolo de ept.ridge (ept.LAMBDAS, 80/20 en orden, empate al mas grande) con el solver dual."""
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    A, Bm = (Xtr - mu) / sd, (Xte - mu) / sd
    yi = np.searchsorted(clases, ytr)
    Y = np.eye(len(clases))[yi]
    nf = int(0.8 * len(A))
    Ac, am, ym, alfas = _dual(A[:nf].copy(), Y[:nf], ept.LAMBDAS)
    G = (A[nf:] - am) @ Ac.T
    accs = [float(((G @ al + ym).argmax(1) == yi[nf:]).mean()) for al in alfas]
    j = max(range(len(ept.LAMBDAS)), key=lambda k: (accs[k], ept.LAMBDAS[k]))
    Ac, am, ym, alfas = _dual(A.copy(), Y, (ept.LAMBDAS[j],))
    return clases[(((Bm - am) @ Ac.T) @ alfas[0] + ym).argmax(1)], ept.LAMBDAS[j]


def ridge_estado_015(Xtr, ytr, vtr, Xte, vte):
    pred = np.zeros(len(Xte), dtype=np.int64)
    lams = {}
    for s in (True, False):
        mtr, mte = vtr == s, vte == s
        pred[mte], lams[str(s)] = ridge_015(Xtr[mtr], ytr[mtr], Xte[mte], tm.CLASES[s])
    return pred, lams


# ---------------- MLP (el bucle de ept.mlp_mux) ----------------
def mlp_ajustar(X, y, v, idx, semilla, clases, iters):
    mods = {}
    for s in (True, False):
        ii = idx[v[idx] == s]
        cl = clases[s]
        Xs = X[ii]
        mu, sd = Xs.mean(0), Xs.std(0) + 1e-6
        A = torch.from_numpy(((Xs - mu) / sd).astype(np.float32))
        del Xs
        Y = torch.from_numpy(np.searchsorted(cl, y[ii]).astype(np.int64))
        torch.manual_seed(semilla)
        net = nn.Sequential(nn.Linear(A.shape[1], MLP_H), nn.Tanh(), nn.Linear(MLP_H, len(cl)))
        opt = torch.optim.Adam(net.parameters(), lr=MLP_LR, weight_decay=MLP_WD)
        rng = np.random.default_rng(5000 + semilla)
        for _ in range(iters):
            b = torch.from_numpy(rng.integers(0, len(Y), MLP_LOTE))
            loss = F.cross_entropy(net(A[b]), Y[b])
            opt.zero_grad()
            loss.backward()
            opt.step()
        mods[s] = (mu, sd, net, cl)
    return mods


def mlp_predecir(mods, X, v, idx):
    pred = np.zeros(len(idx), dtype=np.int64)
    for s, (mu, sd, net, cl) in mods.items():
        sel = np.where(v[idx] == s)[0]
        if len(sel) == 0:
            continue
        Bm = torch.from_numpy(((X[idx[sel]] - mu) / sd).astype(np.float32))
        with torch.no_grad():
            pred[sel] = cl[net(Bm).argmax(1).numpy()]
    return pred


# ---------------- REGLA_TAU ----------------
def t_k(semilla):
    u = np.array([np.random.default_rng([semilla, k]).random() for k in range(6)])
    return DT / (0.06 + 0.12 * u)


def integrar(U, tk):
    Z = np.empty_like(U)
    z = np.zeros((U.shape[0], U.shape[2]))
    for t in range(U.shape[1]):
        z = (1.0 - tk) * z + tk * U[:, t, :]
        Z[:, t, :] = z
    return Z


def regla_carrera(Ltr, ytr, vtr, Lte, vte):
    th = tm.umbrales(tm.lineas(Ltr), ytr, vtr)
    return tm.carrera(tm.lineas(Lte), th, vte)


# ---------------- eleccion y prediccion ----------------
def rivales(Ftr, Ltr, ytr, vtr, m, iters, log):
    idx = np.arange(m)
    pl = pliegues(m)
    M = {}
    tc = time.time()
    cv, acc = cv_ridge(Ftr, ytr, vtr, pl, LAMBDAS_R)
    j = max(range(len(LAMBDAS_R)), key=lambda k: (cv[k], LAMBDAS_R[k]))
    M["RIDGE"] = dict(candidatas=list(LAMBDAS_R), validacion=cv.tolist(), pliegues=acc.tolist(), elegida=LAMBDAS_R[j],
                      modelo=ridge_ajustar(Ftr, ytr, vtr, idx, (LAMBDAS_R[j],)))
    if log:
        for k, lam in enumerate(LAMBDAS_R):
            pr("CANDIDATA rival=RIDGE lambda=%g validacion=%.4f pliegues=%s" % (
                lam, cv[k], " ".join("%.4f" % x for x in acc[:, k])))
        pr("ELECCION rival=RIDGE lambda=%g | %.1f s" % (LAMBDAS_R[j], time.time() - tc))
    tc = time.time()
    acc = np.zeros((len(pl), len(SEM_MLP)))
    for k, sem in enumerate(SEM_MLP):
        for jj, (ia, it) in enumerate(pl):
            mods = mlp_ajustar(Ftr, ytr, vtr, ia, sem, tm.CLASES, iters)
            acc[jj, k] = float((mlp_predecir(mods, Ftr, vtr, it) == ytr[it]).mean())
            del mods
        if log:
            pr("CANDIDATA rival=MLP semilla=%d validacion=%.4f pliegues=%s | %.1f s" % (
                sem, acc[:, k].mean(), " ".join("%.4f" % x for x in acc[:, k]), time.time() - tc))
    cv = acc.mean(0)
    k = max(range(len(SEM_MLP)), key=lambda q: (cv[q], -SEM_MLP[q]))
    M["MLP"] = dict(candidatas=SEM_MLP, validacion=cv.tolist(), pliegues=acc.tolist(), elegida=SEM_MLP[k],
                    iteraciones=iters, modelo=mlp_ajustar(Ftr, ytr, vtr, idx, SEM_MLP[k], tm.CLASES, iters))
    if log:
        pr("ELECCION rival=MLP semilla=%d | %.1f s" % (SEM_MLP[k], time.time() - tc))
    tc = time.time()
    cv, cvp = np.zeros(len(SEM_RT)), []
    for k, sem in enumerate(SEM_RT):
        cv[k], pp = ht.validacion(tm.lineas(integrar(Ltr[idx], t_k(sem))), ytr[idx], vtr[idx], PLIEGUES)
        cvp.append(pp)
        if log:
            pr("CANDIDATA rival=REGLA_TAU semilla=%d validacion=%.4f pliegues=%s tau=%s" % (
                sem, cv[k], " ".join("%.4f" % x for x in pp), " ".join("%.4f" % x for x in DT / t_k(sem))))
    k = max(range(len(SEM_RT)), key=lambda q: (cv[q], -SEM_RT[q]))
    tk = t_k(SEM_RT[k])
    th = tm.umbrales(tm.lineas(integrar(Ltr[idx], tk)), ytr[idx], vtr[idx])
    M["REGLA_TAU"] = dict(candidatas=SEM_RT, validacion=cv.tolist(), pliegues=cvp, elegida=SEM_RT[k],
                          tau=(DT / tk).tolist(), modelo=(tk, th))
    if log:
        pr("ELECCION rival=REGLA_TAU semilla=%d | %.1f s" % (SEM_RT[k], time.time() - tc))
    return M


def predecir_rivales(M, Fte, Lte, vte):
    ar = np.arange(len(vte))
    tk, th = M["REGLA_TAU"]["modelo"]
    return {"RIDGE": ridge_predecir(M["RIDGE"]["modelo"], Fte, vte, ar)[0],
            "MLP": mlp_predecir(M["MLP"]["modelo"], Fte, vte, ar),
            "REGLA_TAU": tm.carrera(tm.lineas(integrar(Lte, tk)), th, vte)}


def repro_w(sp, yte, w):
    p = de_str(sp)
    return bool(len(p) == len(yte) and float((p == yte).mean()) == w)


# ---------------- una celda ----------------
def celda(a, A, s, ci):
    C = {"PIN": True}
    res = dict(experimento="H_RIVAL", celda=clave(A, s), ci=ci, humo=bool(a.humo), primaria=PRIMARIA,
               secundaria=SECUNDARIA, md5_script=md5(os.path.abspath(__file__)))
    tc = time.time()
    suj = sujeto_r2(a.conn, a.annot)
    C["R2_TAMANO"] = suj["ok"]
    pr("SUJETO R2 entradas=%d -> %s | %.1f s" % (suj["n_ent"], suj["ok"], time.time() - tc))
    hj = json.load(open(os.path.join(DIR_HTAU, "htau_c%d.json" % ci)))
    hcor = {r["prueba"]: r for r in hj["corridas"]}
    C["HTAU_CELDA"] = bool(hj["celda"] == clave(A, s) and sorted(hcor) == PRIMARIA)
    f3c, f3r, okf = {}, {}, True
    for t in TAUS_F3:
        j3 = json.load(open(os.path.join(DIR_F3, "factorial2_R2_CON_TASA_t%dc%d.json" % (t, ci))))
        okf = okf and j3["celdas"] == [clave(A, s)] and j3["taus"] == [t]
        f3c[t] = {r["prueba"]: r for r in j3["corridas"]}
        okf = okf and sorted(f3c[t]) == SECUNDARIA
        if t == 0:
            f3r = {r["prueba"]: r for r in j3["reglas"]}
    C["F3_CELDA"] = bool(okf and sorted(f3r) == SECUNDARIA)
    tc = time.time()
    ytr, vtr, Xtr = ensayos(suj, A, s, tm.N_TRAIN, f2.SEM_GEN_TR, f2.SEM_RUIDO_TR)
    ntr = len(ytr)
    Ltr = lc_de(Xtr, suj)
    Ftr = Xtr.reshape(ntr, -1)
    del Xtr
    pl = pliegues(ntr)
    pruebas = SECUNDARIA + PRIMARIA
    C["GUARDA_FUGA"] = bool(f2.SEM_GEN_TR not in pruebas + [HUMO_SEM] and
                            f2.SEM_RUIDO_TR not in [1000 + p for p in pruebas + [HUMO_SEM]] and
                            all(len(np.intersect1d(ia, it)) == 0 and len(ia) + len(it) == ntr for ia, it in pl))
    pr("DATOS entrenamiento=%d rasgos=%d pliegues=%d | %.1f s" % (ntr, Ftr.shape[1], len(pl), time.time() - tc))

    tc = time.time()
    rng = np.random.default_rng(SEM_PERM)
    yperm = ytr.copy()
    for st in (True, False):
        ii = np.where(vtr == st)[0]
        yperm[ii] = ytr[ii][rng.permutation(len(ii))]
    cvn, _ = cv_ridge(Ftr, yperm, vtr, pl, LAMBDAS_R)
    jn = max(range(len(LAMBDAS_R)), key=lambda k: (cvn[k], LAMBDAS_R[k]))
    mod_neg = ridge_ajustar(Ftr, yperm, vtr, np.arange(ntr), (LAMBDAS_R[jn],))
    pr("NEGATIVO etiquetas permutadas dentro de cada estado, lambda elegido=%g | %.1f s" % (
        LAMBDAS_R[jn], time.time() - tc))

    if ci == 0:
        tc = time.time()
        ia, it = pl[0]
        yr = ytr.copy()
        yr[vtr] = np.searchsorted(tm.CLASES[True], ytr[vtr])
        pE = ept.mlp_mux(Ftr[ia], yr[ia], vtr[ia], Ftr[it], vtr[it], 0, MLP_ITERS)
        pM = mlp_predecir(mlp_ajustar(Ftr, yr, vtr, ia, 0, ept.CLASES, MLP_ITERS), Ftr, vtr, it)
        C["CONTROL_MLP_005"] = bool(np.array_equal(pE, pM))
        pr("CONTROL_MLP_005 pliegue=0 semilla=0 iteraciones=%d iguales=%d/%d -> %s | %.1f s" % (
            MLP_ITERS, int((pE == pM).sum()), len(pE), C["CONTROL_MLP_005"], time.time() - tc))

    tc = time.time()
    M = rivales(Ftr, Ltr, ytr, vtr, HUMO_TR if a.humo else ntr, HUMO_ITERS if a.humo else MLP_ITERS, not a.humo)
    pr("RIVALES elegidos | %.1f s" % (time.time() - tc))
    if a.humo:
        y9, v9, X9 = ensayos(suj, A, s, HUMO_TE, HUMO_SEM, 1000 + HUMO_SEM)
        P9 = predecir_rivales(M, X9.reshape(HUMO_TE, -1), lc_de(X9, suj), v9)
        del X9
        for r in RIVALES:
            ok = bool(len(P9[r]) == HUMO_TE and
                      all(np.isin(P9[r][v9 == st], tm.CLASES[st]).all() for st in (True, False)))
            C["RUTA_" + r] = ok
            pr("RUTA rival=%s candidatas=10 ensayos=%d/%d predicciones=%d en_clases=%s (humo: sin aciertos)" % (
                r, HUMO_TR, HUMO_TE, len(P9[r]), ok))

    filas = []
    rp = [0, 0]
    rw = [0, 0]
    for p in pruebas:
        tp = time.time()
        yte, vte, Xte = ensayos(suj, A, s, tm.N_TEST, p, 1000 + p)
        Lte = lc_de(Xte, suj)
        Fte = Xte.reshape(len(yte), -1)
        del Xte
        pP = regla_carrera(Ltr, ytr, vtr, Lte, vte)
        ref = hcor[p]["pred_regla_propia"] if p in PRIMARIA else f3r[p]["pred_regla_propia"]
        rp[0] += int(a_str(pP) == ref)
        rp[1] += 1
        fila = dict(prueba=p, regla_propia=float((pP == yte).mean()))
        if p in PRIMARIA:
            rw[0] += int(repro_w(hcor[p]["pred_elegida"], yte, hcor[p]["W_elegida"]))
            rw[1] += 1
            fila["W_elegida"] = hcor[p]["W_elegida"]
            wtxt = "%.4f" % fila["W_elegida"]
        else:
            fila["W_f3"] = {}
            for t in TAUS_F3:
                r = f3c[t][p]
                rw[0] += int(repro_w(r["pred_W"], yte, r["W"]))
                rw[1] += 1
                fila["W_f3"][str(t)] = r["W"]
            wtxt = "%.4f(media de 10 tau)" % float(np.mean(list(fila["W_f3"].values())))
        if p == PRIMARIA[0]:
            uno = np.ones(6)
            pN = regla_carrera(integrar(Ltr, uno), ytr, vtr, integrar(Lte, uno), vte)
            C["REGLA_TAU_NULA"] = bool(np.array_equal(pN, pP))
            pr("CHEQUEO REGLA_TAU_NULA prueba=%d iguales=%d/%d -> %s" % (
                p, int((pN == pP).sum()), len(pP), C["REGLA_TAU_NULA"]))
            pn = ridge_predecir(mod_neg, Fte, vte, np.arange(len(yte)))[0]
            maj = {st: int(np.bincount(yte[vte == st]).argmax()) for st in (True, False)}
            azar = float((np.where(vte, maj[True], maj[False]) == yte).mean())
            an = float((pn == yte).mean())
            C["CONTROL_NEGATIVO"] = bool(an <= azar + MARGEN_NEG)
            res["control_negativo"] = dict(prueba=p, acierto=an, azar=azar, lam=LAMBDAS_R[jn], validacion=cvn.tolist())
            pr("CONTROL_NEGATIVO prueba=%d acierto=%.4f azar=%.4f tope=%.4f -> %s" % (
                p, an, azar, azar + MARGEN_NEG, C["CONTROL_NEGATIVO"]))
        if a.humo:
            pr("PRUEBA celda=%s prueba=%d regla_igual=%s | %.1f s" % (clave(A, s), p, a_str(pP) == ref,
                                                                    time.time() - tp))
        else:
            P = predecir_rivales(M, Fte, Lte, vte)
            for r in RIVALES:
                fila[r] = float((P[r] == yte).mean())
                fila["pred_" + r] = a_str(P[r])
            pr("PRUEBA celda=%s prueba=%d RIDGE=%.4f MLP=%.4f REGLA_TAU=%.4f regla_propia=%.4f W=%s | %.1f s" % (
                clave(A, s), p, fila["RIDGE"], fila["MLP"], fila["REGLA_TAU"], fila["regla_propia"], wtxt,
                time.time() - tp))
        filas.append(fila)
        del Fte, Lte
    C["REPRO_REGLA"] = bool(rp[0] == rp[1] == len(pruebas))
    C["REPRO_W"] = bool(rw[0] == rw[1] == len(PRIMARIA) + len(SECUNDARIA) * len(TAUS_F3))
    pr("CHEQUEO REPRO_REGLA iguales=%d/%d -> %s | REPRO_W iguales=%d/%d -> %s" % (
        rp[0], rp[1], C["REPRO_REGLA"], rw[0], rw[1], C["REPRO_W"]))
    res["filas"] = filas
    res["rivales"] = None if a.humo else {r: {k: v for k, v in M[r].items() if k != "modelo"} for r in RIVALES}
    res["controles"] = C
    valido = all(C.values())
    res["valido"] = valido
    pr("CHEQUEO INSTRUMENTO %s -> %s" % (" ".join("%s=%s" % kv for kv in C.items()),
                                         "VALIDO" if valido else "INVALIDO"))
    ruta = os.path.join(a.out, ("rival_humo_c%d.json" if a.humo else "rival_c%d.json") % ci)
    with open(ruta, "w") as f:
        json.dump(res, f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), md5(ruta)))
    return 0 if valido else 3


# ---------------- CONTROL_RIDGE_015 ----------------
def control_015(a):
    tc = time.time()
    sel, _ = tm.construir(a.conn, a.annot)
    nv = len(sel) - 6
    lados = ["L" if x[2] == "left" else "R" for x in sel]
    tipos = [x[1] for x in sel]
    idx_W = np.array([(0 if lados[i] == "L" else 1) * tm.NT + tm.TIPOS.index(tipos[i]) for i in range(nv)])
    etr, ete = tm.generar(tm.N_TRAIN, 1), tm.generar(tm.N_TEST, 2)
    ytr, vtr, yte, vte = etr["y"], etr["vuelo"], ete["y"], ete["vuelo"]
    Ztr = np.random.default_rng(101).standard_normal((tm.N_TRAIN, tm.T, nv))
    Zte = np.random.default_rng(102).standard_normal((tm.N_TEST, tm.T, nv))
    pr("MOTIVO_015 visuales=%d rasgos=%d | %.1f s" % (nv, nv * tm.T, time.time() - tc))
    filas = []
    for A, s in f2.CELDAS:
        tc = time.time()
        Xtr = (tm.sintonias(etr, A)[:, :, idx_W] + s * Ztr).reshape(tm.N_TRAIN, -1)
        Xte = (tm.sintonias(ete, A)[:, :, idx_W] + s * Zte).reshape(tm.N_TEST, -1)
        p, lams = ridge_estado_015(Xtr, ytr, vtr, Xte, vte)
        q = tm.ridge_estado(Xtr, ytr, vtr, Xte, vte)
        acc = float((p == yte).mean())
        esp = ESPERADO_015[(A, s)]
        ok = bool(abs(acc - esp) <= TOL_015 + 1e-9)
        filas.append(dict(celda=clave(A, s), acierto=acc, esperado=esp, ok=ok, lambdas=lams,
                          dif_con_ept=int((p != q).sum()), acierto_ept=float((q == yte).mean())))
        pr("CONTROL_RIDGE_015 celda=%s acierto=%.4f esperado=%.4f tolerancia=%.4f dif_con_ept=%d -> %s | %.1f s" % (
            clave(A, s), acc, esp, TOL_015, int((p != q).sum()), ok, time.time() - tc))
    valido = all(f["ok"] for f in filas)
    pr("CHEQUEO CONTROL_RIDGE_015 %d/%d -> %s" % (sum(f["ok"] for f in filas), len(filas),
                                                 "VALIDO" if valido else "INVALIDO"))
    ruta = os.path.join(a.out, "controles_015%s.json" % ("_humo" if a.humo else ""))
    with open(ruta, "w") as f:
        json.dump(dict(experimento="H_RIVAL", control="CONTROL_RIDGE_015", humo=bool(a.humo), nv=nv, filas=filas,
                       valido=valido), f)
    pr("escrito %s md5=%s" % (os.path.basename(ruta), md5(ruta)))
    return 0 if valido else 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--celda", default=None, help="A|ruido, p. ej. 0.3|0.15")
    ap.add_argument("--solo_015", action="store_true", help="solo CONTROL_RIDGE_015")
    ap.add_argument("--humo", action="store_true", help="humo ciego: controles completos, rutas sin aciertos")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t_ini = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s | torch %s hilos=%d" % (
        platform.node(), platform.platform(), platform.python_version(), np.__version__, torch.__version__,
        torch.get_num_threads()))
    pr("# md5 script = " + md5(os.path.abspath(__file__)))
    if a.humo:
        pr("# HUMO: controles a tamano completo; rutas de los rivales con %d y %d ensayos (semilla %d), sin aciertos" % (
            HUMO_TR, HUMO_TE, HUMO_SEM))
    P = pines(a.conn, a.annot)
    pr("PIN " + " ".join("%s=%s" % kv for kv in sorted(P.items())))
    if not all(P.values()):
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    if a.solo_015:
        rc = control_015(a)
    else:
        A, s = (float(x) for x in a.celda.split("|"))
        rc = celda(a, A, s, f2.CELDAS.index((A, s)))
    pr("# duracion_s=%.1f" % (time.time() - t_ini))
    pr("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
