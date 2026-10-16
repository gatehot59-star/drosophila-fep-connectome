#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
output_control_permutation_null.py :: nulo por permutacion de etiquetas para la respuesta 005.

Pedido 2026-10-10 (Abraham): "Run the stronger 500+ permutation null".

La 005 comparo cada salida contra destinos al azar. Ese nulo trata a las neuronas de salida
como independientes, y con etiquetas permutadas marco ~3% de falsos. Aca el grafo y las
salidas quedan reales, y lo que se permuta R veces es la etiqueta de clase de las neuronas
de ORIGEN:

  perm  permutacion simple: conserva el tamano de cada clase.
  estr  permutacion dentro de estratos de fuerza de salida (sinapsis hacia neuronas que no
        son salida, en la misma variante): conserva el tamano de cada clase y cuanto pesa
        cada neurona. Es el nulo fuerte: una clase de neuronas grandes no gana por grande.

Con A[i,j] = S[i,j] / entrada_j y t_O = 1/|O| sobre las neuronas de O con entrada:
  u1_O = A t_O,  u2_O = A u1_O      (un valor por neurona presinaptica)
  D1(C,O) = sum_{i en C} u1_O[i]    (el mismo D1 de la 005)
  D2(C,O) = sum_{i en C} u2_O[i]    (el mismo D2 de la 005)
p unilateral con +1 sobre las R permutaciones; flag SOBRE o BAJO si p <= 0.001, como en la 005.

Controles que pueden dar rojo:
  CRUCE_005          D1 y D2 reales iguales (<= 1e-12) a los del JSON de la 005.
  CONTEOS/ESTRATOS   cada permutacion conserva los tamanos de clase (y por estrato en estr).
  MEDIA_NULO         la media de cada nulo coincide con su esperanza exacta, con z sobre la
                     varianza exacta de la permutacion (|z| <= 6). (Primera corrida: z con el
                     desvio empirico daba infinito en eventos raros, p. ej. sin_anotacion -> ITP,
                     donde ninguna de las 10.000 permutaciones toco al unico presinaptico.)
  VARIANZA_NULO      mediana de varianza empirica / varianza exacta entre 0,9 y 1,1.
  CONTROL_NEGATIVO   etiquetados falsos sacados del mismo nulo: flags <= max(3, 3 x esperado).
  R_PEDIDO_500       con R < 500 el veredicto no puede ser PASS.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np
import scipy
import scipy.sparse as sp

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import output_control_by_class as oc  # noqa: E402

SEED = 20261011
R_PERM = 10000
R_MINIMO = 500
N_FALSOS = 20
N_ESTRATOS = 100
P_FLAG = oc.P_FLAG
MODOS = ("perm", "estr")
Z_MAX = 6.0
FACTOR_CONTROL = 3.0
TOL_CRUCE = 1e-12


def vectores_u(pre, post, S, n, umbral, conjuntos):
    """u1 y u2 por neurona presinaptica; columnas = conjuntos (u1) y despues conjuntos (u2)."""
    if umbral > 1:
        m = S >= umbral
        p, q, s = pre[m], post[m], S[m]
        del m
    else:
        p, q, s = pre, post, S
    sw = s.astype(np.float64)
    ent = np.bincount(q, weights=sw, minlength=n)
    con = ent > 0
    A = sp.csr_matrix((sw / ent[q], (p, q)), shape=(n, n))
    del sw
    nombres = list(conjuntos)
    T = np.zeros((n, len(nombres)))
    n_in = {}
    for k, O in enumerate(nombres):
        idx = np.asarray(conjuntos[O], dtype=np.int64)
        idx_in = idx[con[idx]]
        n_in[O] = int(len(idx_in))
        if len(idx_in):
            T[idx_in, k] = 1.0 / len(idx_in)
    U1 = np.asarray(A @ T)
    U2 = np.asarray(A @ U1)
    del A, T
    return {"p": p, "q": q, "s": s, "U": np.ascontiguousarray(np.hstack([U1, U2])),
            "m": len(nombres), "n_in": n_in, "conjuntos": nombres, "con": con}


def estratos_por_fuerza(p, q, s, n, es_salida, nb=N_ESTRATOS):
    """Estratos de ancho fijo en log(1 + fuerza), con fuerza = sinapsis hacia neuronas que no son
    salida. Una neurona solo cambia de etiqueta con otras de su mismo tamano (factor exp(ancho)),
    y un hueco de la distribucion nunca queda adentro de un estrato. Los empates quedan juntos.
    (Primera version con cuantiles: un estrato junto fuerza 3 con 25 y el test de tamano dio rojo.)"""
    keep = ~es_salida[q]
    fuerza = np.bincount(p[keep], weights=s[keep].astype(np.float64), minlength=n)
    lf = np.log1p(fuerza)
    ancho = float(lf.max()) / nb if lf.max() > 0 else 1.0
    est = np.floor(lf / ancho).astype(np.int64)
    _, est = np.unique(est, return_inverse=True)
    return fuerza, est.astype(np.int64), ancho


class Permutador:
    """Devuelve una permutacion de las etiquetas: global (perm) o dentro de cada estrato (estr)."""

    def __init__(self, cls, est, modo):
        self.cls = np.asarray(cls)
        if modo == "perm":
            self.bloques = [np.arange(len(self.cls))]
        elif modo == "estr":
            orden = np.argsort(est, kind="stable")
            self.bloques = np.split(orden, np.flatnonzero(np.diff(est[orden])) + 1)
        else:
            raise ValueError(modo)

    def __call__(self, rng):
        out = np.empty_like(self.cls)
        for pos in self.bloques:
            out[pos] = self.cls[pos[rng.permutation(len(pos))]]
        return out


class Sumador:
    """Suma las filas de U por etiqueta: (K x n one-hot) @ U."""

    def __init__(self, n, K):
        self.n = n
        self.K = K
        self.indptr = np.arange(n + 1, dtype=np.int32)
        self.data = np.ones(n)

    def __call__(self, lab, U):
        P = sp.csc_matrix((self.data, np.asarray(lab, dtype=np.int32), self.indptr), shape=(self.K, self.n))
        return np.asarray(P @ U)


def esperanza(cls, est, U, K, modo):
    """Esperanza exacta de la suma por clase bajo el nulo: sum_b n_Cb / n_b * sum_{i en b} U_i."""
    if modo == "perm":
        est = np.zeros(len(cls), dtype=np.int64)
    nb = int(est.max()) + 1
    n_b = np.bincount(est, minlength=nb).astype(np.float64)
    n_cb = np.bincount(np.asarray(cls, dtype=np.int64) * nb + est, minlength=K * nb).reshape(K, nb)
    Ub = Sumador(len(cls), nb)(est, U)
    return (n_cb / n_b[None, :]) @ Ub


def varianza_exacta(cls, est, U, K, modo):
    """Varianza exacta de la suma por clase bajo el nulo: muestreo sin reposicion en cada estrato,
    Var = sum_b n_Cb (n_b - n_Cb) / (n_b - 1) * varianza poblacional de U en b."""
    if modo == "perm":
        est = np.zeros(len(cls), dtype=np.int64)
    nb = int(est.max()) + 1
    n_b = np.bincount(est, minlength=nb).astype(np.float64)
    n_cb = np.bincount(np.asarray(cls, dtype=np.int64) * nb + est, minlength=K * nb).reshape(K, nb)
    n_cb = n_cb.astype(np.float64)
    sumar = Sumador(len(cls), nb)
    s1 = sumar(est, U)
    s2 = sumar(est, U * U)
    media_b = s1 / n_b[:, None]
    var_b = np.maximum(s2 / n_b[:, None] - media_b ** 2, 0.0)
    nbb = n_b[None, :]
    with np.errstate(invalid="ignore", divide="ignore"):
        f = np.where(nbb > 1, n_cb * (nbb - n_cb) / (nbb - 1.0), 0.0)
    return f @ var_b


def chequeo_momentos(media, sd, esp, var, R, cols):
    """z de la media contra la esperanza exacta (con la varianza exacta) y cociente de varianzas."""
    dif = np.abs(media - esp)
    se = np.sqrt(var / R)
    with np.errstate(invalid="ignore", divide="ignore"):
        z = np.where(se > 0, dif / se, np.where(dif <= 1e-12, 0.0, np.inf))
    zc = z[:, cols]
    zmax = float(np.max(zc)) if zc.size else 0.0
    vc = var[:, cols]
    ec = (sd ** 2)[:, cols]
    ok = vc > 0
    ratio = float(np.median(ec[ok] / vc[ok])) if ok.any() else 1.0
    return zmax, ratio


def correr_nulo(cls, est, modo, U, K, R, semilla, nb_chequeo=50, progreso=None):
    perm = Permutador(cls, est, modo)
    sumar = Sumador(len(cls), K)
    rng = np.random.default_rng(semilla)
    conteo = np.bincount(cls, minlength=K)
    nb = int(est.max()) + 1
    clase_est = np.asarray(cls, dtype=np.int64) * nb + est
    conteo_est = np.bincount(clase_est, minlength=K * nb)
    nul = np.empty((R, K, U.shape[1]))
    ok_conteo = True
    ok_est = True
    t0 = time.time()
    for r in range(R):
        lab = perm(rng)
        ok_conteo = ok_conteo and bool(np.array_equal(np.bincount(lab, minlength=K), conteo))
        if modo == "estr" and r < nb_chequeo:
            le = np.asarray(lab, dtype=np.int64) * nb + est
            ok_est = ok_est and bool(np.array_equal(np.bincount(le, minlength=K * nb), conteo_est))
        nul[r] = sumar(lab, U)
        if progreso is not None and (r + 1) % 1000 == 0:
            progreso("%s r=%d seg=%.1f" % (modo, r + 1, time.time() - t0))
    return nul, ok_conteo, ok_est, time.time() - t0


def evaluar_nulo(real, nul, p_flag=P_FLAG):
    R = nul.shape[0]
    tol = 1e-12 * np.abs(real) + 1e-300
    ge = (nul >= (real - tol)[None]).sum(axis=0)
    le = (nul <= (real + tol)[None]).sum(axis=0)
    ps = (1.0 + ge) / (R + 1.0)
    pb = (1.0 + le) / (R + 1.0)
    media = nul.mean(axis=0)
    sd = nul.std(axis=0, ddof=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        enr = np.where(media > 0, real / media, np.nan)
    fl = np.where(ps <= p_flag, "SOBRE", np.where(pb <= p_flag, "BAJO", "azar")).astype("<U5")
    return {"media": media, "sd": sd, "enr": enr, "ps": ps, "pb": pb, "flag": fl}


def control_negativo(cls, est, modo, U, K, nul, n_falsos, semilla, cols):
    """Etiquetados falsos del mismo nulo, evaluados como si fueran reales (solo columnas D1 validas)."""
    perm = Permutador(cls, est, modo)
    sumar = Sumador(len(cls), K)
    rng = np.random.default_rng(semilla)
    sub = nul[:, :, cols]
    flags = 0
    for _ in range(n_falsos):
        D = sumar(perm(rng), U)[:, cols]
        fl = evaluar_nulo(D, sub)["flag"]
        flags += int(np.isin(fl, ("SOBRE", "BAJO")).sum())
    tests = int(n_falsos * K * len(cols))
    esperado = tests * 2.0 * P_FLAG
    tope = max(3.0, FACTOR_CONTROL * esperado)
    return {"flags": flags, "tests": tests, "esperado": esperado, "tope": tope, "ok": bool(flags <= tope)}


def cruce_005(j005, etq, nombres, conjuntos, D, m, n_in):
    if j005 is None:
        return {"estado": "NO_MEDIDO", "motivo": "sin JSON de la 005"}, {}
    if list(j005.get("clases_orden", [])) != list(nombres):
        return {"estado": "FAIL", "motivo": "clases distintas"}, {}
    var = j005["variantes"][etq]
    maxdif = 0.0
    faltan = 0
    n_dif = 0
    f005 = {}
    for k, O in enumerate(conjuntos):
        bloque = var["nivel1"][O] if O in var["nivel1"] else var["nivel2"].get(O)
        if bloque is None:
            faltan += 1
            continue
        if int(bloque["n_con_entrada"]) != n_in[O]:
            n_dif += 1
        for c, cn in enumerate(nombres):
            pc = bloque["por_clase"][cn]
            for medida, col in (("d1", k), ("d2", m + k)):
                v = pc.get(medida)
                if v is None:
                    if n_in[O] != 0:
                        faltan += 1
                else:
                    maxdif = max(maxdif, abs(float(v) - float(D[c, col])))
            f005[(O, c, "d1")] = pc.get("flag1")
            f005[(O, c, "d2")] = pc.get("flag2")
    ok = maxdif <= TOL_CRUCE and faltan == 0 and n_dif == 0
    return {"estado": "PASS" if ok else "FAIL", "max_dif": maxdif, "faltan": faltan,
            "n_con_entrada_distinto": n_dif}, f005


def _f(v):
    return v if v else "-"


def imprimir_nivel1(etq, O, k, m, n_in, nombres, D, evm, f005):
    ep, ee = evm["perm"], evm["estr"]
    print("-- NIVEL1 %s [%s] | con_entrada=%d" % (O, etq, n_in[O]))
    print("%-19s %7s %-5s %7s %6s %-5s %7s %6s %-5s %7s %-5s %6s %-5s"
          % ("clase", "D1%", "005", "perm%", "enrP", "perm", "estr%", "enrE", "estr",
             "D2%", "005_2", "enrE2", "estr2"))
    for c, cn in enumerate(nombres):
        print("%-19s %s %-5s %s %s %-5s %s %s %-5s %s %-5s %s %-5s"
              % (cn, oc._p(D[c, k]), _f(f005.get((O, c, "d1"))),
                 oc._p(ep["media"][c, k]), oc._x(ep["enr"][c, k]), ep["flag"][c, k],
                 oc._p(ee["media"][c, k]), oc._x(ee["enr"][c, k]), ee["flag"][c, k],
                 oc._p(D[c, m + k]), _f(f005.get((O, c, "d2"))),
                 oc._x(ee["enr"][c, m + k]), ee["flag"][c, m + k]))


def imprimir_finas(etq, conjuntos, n1, n_in, nombres, D, evm, f005, top=3):
    print("-- FINAS [%s] (D1, top %d; flags 005 / perm / estr; x = D1 / media estr) --" % (etq, top))
    for k, O in enumerate(conjuntos):
        if O in n1:
            continue
        orden = np.argsort(-D[:, k], kind="stable")[:top]
        partes = ["%s %s%% 005=%s perm=%s estr=%s x%s"
                  % (nombres[c], oc._p(D[c, k]).strip(), _f(f005.get((O, c, "d1"))),
                     evm["perm"]["flag"][c, k], evm["estr"]["flag"][c, k],
                     oc._x(evm["estr"]["enr"][c, k]).strip()) for c in orden]
        print("FINA [%s] %-40s con_entrada=%4d : %s" % (etq, O, n_in[O], " | ".join(partes)))


def comparar(etq, conjuntos, nombres, D, evm, f005, validas):
    caen, nuevos = [], []
    mantienen = 0
    for k, O in enumerate(conjuntos):
        if not validas[k]:
            continue
        for c, cn in enumerate(nombres):
            a = f005.get((O, c, "d1"))
            b = str(evm["estr"]["flag"][c, k])
            if a in ("SOBRE", "BAJO"):
                if b == a:
                    mantienen += 1
                else:
                    caen.append((O, cn, a, b, float(D[c, k]), float(evm["estr"]["enr"][c, k])))
            elif b in ("SOBRE", "BAJO"):
                nuevos.append((O, cn, a, b, float(D[c, k]), float(evm["estr"]["enr"][c, k])))
    for O, cn, a, b, d, e in caen:
        print("CAE   [%s] %-40s %-19s 005=%-5s -> estr=%-5s D1 %s%% x%s" % (etq, O, cn, a, b, oc._p(d).strip(), oc._x(e).strip()))
    for O, cn, a, b, d, e in nuevos:
        print("NUEVO [%s] %-40s %-19s 005=%-5s -> estr=%-5s D1 %s%% x%s" % (etq, O, cn, _f(a), b, oc._p(d).strip(), oc._x(e).strip()))
    return mantienen, caen, nuevos


def contar(fl):
    return int((fl == "SOBRE").sum()), int((fl == "BAJO").sum())


def main(argv=None):
    ap = argparse.ArgumentParser(description="Nulo por permutacion de etiquetas para la respuesta 005")
    ap.add_argument("--parquet", default="/workspace/connectivity.parquet")
    ap.add_argument("--annotations", default="/workspace/annotations.tsv")
    ap.add_argument("--json-005", default="results/output_control_2026-10-10/output_control_by_class.json")
    ap.add_argument("--out", default="results/output_control_permnull_2026-10-10")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--r", type=int, default=R_PERM)
    ap.add_argument("--n-falsos", type=int, default=N_FALSOS)
    ap.add_argument("--n-estratos", type=int, default=N_ESTRATOS)
    ap.add_argument("--maquina", default="brain-env")
    args = ap.parse_args(argv)
    t0 = time.time()
    os.makedirs(args.out, exist_ok=True)

    def progreso(msg):
        sys.stderr.write("PROGRESO %s t=%.1f\n" % (msg, time.time() - t0))
        sys.stderr.flush()

    print("== output_control_permutation_null.py :: nulo por permutacion de etiquetas para la 005 ==")
    entorno = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
               "maquina": args.maquina}
    print("ENTORNO " + " ".join("%s=%s" % kv for kv in entorno.items()))
    print("PARAMETROS seed=%d r=%d n_falsos=%d n_estratos=%d p_flag=%g z_max=%g factor_control=%g"
          % (args.seed, args.r, args.n_falsos, args.n_estratos, P_FLAG, Z_MAX, FACTOR_CONTROL))
    md5p = oc.md5_archivo(args.parquet)
    md5a = oc.md5_archivo(args.annotations)
    j005 = None
    md5j = None
    if args.json_005 and os.path.exists(args.json_005):
        md5j = oc.md5_archivo(args.json_005)
        with open(args.json_005) as f:
            j005 = json.load(f)
    print("INPUT parquet %s md5=%s pin_ok=%s" % (args.parquet, md5p, md5p == oc.PIN_PARQUET_MD5))
    print("INPUT annotations %s md5=%s pin_ok=%s" % (args.annotations, md5a, md5a == oc.PIN_ANNOT_MD5))
    print("INPUT json_005 %s md5=%s" % (args.json_005, md5j))

    pre, post, S, exc, id_of, ginfo = oc.leer_grafo(args.parquet)
    del exc
    print("GRAFO n_nodos=%d n_aristas=%d mapeo_biyectivo=%s sinapsis_total=%d"
          % (ginfo["n_nodos"], ginfo["n_aristas"], ginfo["mapeo_biyectivo"], ginfo["sinapsis_total"]))
    anot = oc.leer_anotaciones(args.annotations, id_of)
    nombres, cls = oc.codificar_clases(anot["super_class"])
    K = len(nombres)
    n = len(id_of)
    conteos = {cn: int((cls == c).sum()) for c, cn in enumerate(nombres)}
    print("CLASES " + " ".join("%s=%d" % kv for kv in conteos.items()))
    n1, n2 = oc.conjuntos_salida(anot["super_class"], anot["cell_sub_class"], anot["cell_type"])
    conjuntos = dict(n1)
    conjuntos.update({k: v for k, v in n2.items() if k not in n1})
    lista = list(conjuntos)
    es_salida = np.zeros(n, dtype=bool)
    for s_ in oc.SALIDAS:
        es_salida[n1[s_]] = True
    print("CONJUNTOS %d (nivel1 %d + finos %d) neuronas_de_salida=%d"
          % (len(lista), len(n1), len(lista) - len(n1), int(es_salida.sum())))

    resultado = {"schema": "output_control_permutation_null/v1", "entorno": entorno,
                 "parametros": {"seed": args.seed, "r": args.r, "n_falsos": args.n_falsos,
                                "n_estratos": args.n_estratos, "p_flag": P_FLAG, "z_max": Z_MAX,
                                "factor_control": FACTOR_CONTROL},
                 "inputs": {"parquet_md5": md5p, "annotations_md5": md5a, "json_005": args.json_005,
                            "json_005_md5": md5j},
                 "clases": conteos, "clases_orden": nombres, "conjuntos": lista, "variantes": {}}
    oks = {"mapeo": bool(ginfo["mapeo_biyectivo"])}
    estados_cruce = []
    guardado = {}
    for umbral, etq in ((1, ">=1"), (5, ">=5")):
        V = vectores_u(pre, post, S, n, umbral, conjuntos)
        fuerza, est, ancho = estratos_por_fuerza(V["p"], V["q"], V["s"], n, es_salida, args.n_estratos)
        del V["p"], V["q"], V["s"]
        U, m, n_in = V["U"], V["m"], V["n_in"]
        tam = np.bincount(est)
        D = Sumador(n, K)(cls, U)
        cruce, f005 = cruce_005(j005, etq, nombres, lista, D, m, n_in)
        estados_cruce.append(cruce["estado"])
        validas = np.array([n_in[O] > 0 for O in lista])
        cols2 = np.concatenate([validas, validas])
        print("== VARIANTE %s | conjuntos_con_entrada=%d/%d | estratos=%d tam_min=%d tam_max=%d fuerza_max=%.0f"
              " ancho_log=%.4f factor=%.3f =="
              % (etq, int(validas.sum()), len(lista), len(tam), int(tam.min()), int(tam.max()), float(fuerza.max()),
                 ancho, float(np.exp(ancho))))
        evm = {}
        info_modos = {}
        for mi, modo in enumerate(MODOS):
            nul, okc, oke, seg = correr_nulo(cls, est, modo, U, K, args.r, [args.seed, umbral, mi],
                                             progreso=lambda s, e=etq: progreso("%s %s" % (e, s)))
            ev = evaluar_nulo(D, nul)
            ev["flag"][:, ~cols2] = "NA"
            esp = esperanza(cls, est, U, K, modo)
            var = varianza_exacta(cls, est, U, K, modo)
            zmax, vratio = chequeo_momentos(ev["media"], ev["sd"], esp, var, args.r, cols2)
            var_ok = bool(0.9 <= vratio <= 1.1)
            ctrl = control_negativo(cls, est, modo, U, K, nul, args.n_falsos, [args.seed, umbral, mi, 99],
                                    np.flatnonzero(validas))
            del nul
            evm[modo] = ev
            info_modos[modo] = {"segundos": seg, "conteos_ok": okc, "estratos_ok": oke, "media_max_z": zmax,
                                "media_ok": bool(zmax <= Z_MAX), "var_ratio_mediana": vratio,
                                "varianza_ok": var_ok, "control_negativo": ctrl}
            oks["conteos_%s_%s" % (modo, etq)] = okc
            oks["estratos_%s_%s" % (modo, etq)] = oke
            oks["media_%s_%s" % (modo, etq)] = bool(zmax <= Z_MAX)
            oks["varianza_%s_%s" % (modo, etq)] = var_ok
            oks["control_%s_%s" % (modo, etq)] = ctrl["ok"]
            print("NULO [%s] %s R=%d segundos=%.1f conteos_ok=%s estratos_ok=%s media_max_z=%.2f var_ratio_mediana=%.4f"
                  % (etq, modo, args.r, seg, okc, oke, zmax, vratio))
        for k, O in enumerate(lista):
            if O in n1:
                imprimir_nivel1(etq, O, k, m, n_in, nombres, D, evm, f005)
        imprimir_finas(etq, lista, n1, n_in, nombres, D, evm, f005)
        mantienen, caen, nuevos = comparar(etq, lista, nombres, D, evm, f005, validas)
        f1 = np.array([[f005.get((O, c, "d1")) or "-" for k, O in enumerate(lista) if validas[k]]
                       for c in range(K)])
        f2 = np.array([[f005.get((O, c, "d2")) or "-" for k, O in enumerate(lista) if validas[k]]
                       for c in range(K)])
        tests = int(K * validas.sum())
        s005, b005 = contar(f1)
        sp_, bp_ = contar(evm["perm"]["flag"][:, :m][:, validas])
        se_, be_ = contar(evm["estr"]["flag"][:, :m][:, validas])
        print("RESUMEN [%s] D1 tests=%d | 005 SOBRE=%d BAJO=%d | perm SOBRE=%d BAJO=%d | estr SOBRE=%d BAJO=%d"
              " | 005->estr se_mantienen=%d cambian=%d nuevos=%d"
              % (etq, tests, s005, b005, sp_, bp_, se_, be_, mantienen, len(caen), len(nuevos)))
        s005b, b005b = contar(f2)
        sp2, bp2 = contar(evm["perm"]["flag"][:, m:][:, validas])
        se2, be2 = contar(evm["estr"]["flag"][:, m:][:, validas])
        print("RESUMEN [%s] D2 tests=%d | 005 SOBRE=%d BAJO=%d | perm SOBRE=%d BAJO=%d | estr SOBRE=%d BAJO=%d"
              % (etq, tests, s005b, b005b, sp2, bp2, se2, be2))
        print("CRUCE_005 [%s] %s %s" % (etq, cruce["estado"], " ".join("%s=%s" % kv for kv in cruce.items()
                                                                        if kv[0] != "estado")))
        for modo in MODOS:
            c = info_modos[modo]["control_negativo"]
            print("CONTROL_NEGATIVO [%s] %s flags=%d/%d esperado=%.2f tope=%.2f OK=%s"
                  % (etq, modo, c["flags"], c["tests"], c["esperado"], c["tope"], c["ok"]))
        guardado[etq] = {"D": D, "evm": evm, "validas": validas, "m": m}
        por_conj = {}
        for k, O in enumerate(lista):
            pc = {}
            for c, cn in enumerate(nombres):
                d = {"d1": D[c, k], "d2": D[c, m + k], "flag005_d1": f005.get((O, c, "d1")),
                     "flag005_d2": f005.get((O, c, "d2"))}
                for modo in MODOS:
                    ev = evm[modo]
                    d[modo] = {"media1": ev["media"][c, k], "sd1": ev["sd"][c, k], "enr1": ev["enr"][c, k],
                               "ps1": ev["ps"][c, k], "pb1": ev["pb"][c, k], "flag1": ev["flag"][c, k],
                               "media2": ev["media"][c, m + k], "sd2": ev["sd"][c, m + k],
                               "enr2": ev["enr"][c, m + k], "ps2": ev["ps"][c, m + k],
                               "pb2": ev["pb"][c, m + k], "flag2": ev["flag"][c, m + k]}
                pc[cn] = d
            por_conj[O] = {"n_con_entrada": n_in[O], "por_clase": pc}
        resultado["variantes"][etq] = {"estratos": {"n": int(len(tam)), "tam_min": int(tam.min()),
                                                     "tam_max": int(tam.max()), "fuerza_max": float(fuerza.max()),
                                                     "ancho_log": ancho, "tamanos": tam},
                                       "cruce_005": cruce, "modos": info_modos,
                                       "conteo_flags_d1": {"tests": tests, "005": [s005, b005], "perm": [sp_, bp_],
                                                           "estr": [se_, be_], "se_mantienen": mantienen,
                                                           "cambian": [list(x) for x in caen],
                                                           "nuevos": [list(x) for x in nuevos]},
                                       "por_conjunto": por_conj}
        del U, V
    print("-- QUE CONTROLA CADA CLASE CON EL NULO FUERTE (estr, D1, SOBRE en >=1 y en >=5) --")
    firmes = {}
    g1, g5 = guardado[">=1"], guardado[">=5"]
    for c, cn in enumerate(nombres):
        sob = []
        for k, O in enumerate(lista):
            if not (g1["validas"][k] and g5["validas"][k]):
                continue
            if g1["evm"]["estr"]["flag"][c, k] == "SOBRE" and g5["evm"]["estr"]["flag"][c, k] == "SOBRE":
                sob.append("%s x%s/x%s (D1 %s/%s%%)"
                           % (O, oc._x(g1["evm"]["estr"]["enr"][c, k]).strip(),
                              oc._x(g5["evm"]["estr"]["enr"][c, k]).strip(),
                              oc._p(g1["D"][c, k]).strip(), oc._p(g5["D"][c, k]).strip()))
        baj = [O for k, O in enumerate(lista) if O in n1 and g1["evm"]["estr"]["flag"][c, k] == "BAJO"
               and g5["evm"]["estr"]["flag"][c, k] == "BAJO"]
        linea = "QUE_CONTROLA_FIRME %s: SOBRE: %s | BAJO nivel1: %s" % (cn, ", ".join(sob) or "ninguna",
                                                                       ", ".join(baj) or "ninguna")
        print(linea)
        firmes[cn] = linea
    resultado["que_controla_firme"] = firmes
    r_ok = args.r >= R_MINIMO
    print("R_PEDIDO_500 r=%d ok=%s" % (args.r, r_ok))
    resto_ok = all(oks.values())
    print("CHEQUEOS " + " ".join("%s=%s" % kv for kv in oks.items()))
    if resto_ok and r_ok and all(e == "PASS" for e in estados_cruce):
        ver = "PASS"
    elif resto_ok and all(e in ("PASS", "NO_MEDIDO") for e in estados_cruce):
        ver = "INCOMPLETO"
    else:
        ver = "FAIL"
    resultado["veredicto"] = {"nulo": ver, "r_ok": r_ok, "chequeos": oks, "cruce_005": estados_cruce}
    resultado["segundos"] = time.time() - t0
    salida = os.path.join(args.out, "output_control_permutation_null.json")
    with open(salida, "w") as f:
        json.dump(oc.a_py(resultado), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("JSON %s md5=%s" % (salida, oc.md5_archivo(salida)))
    print("VEREDICTO_NULO %s" % ver)
    print("FIN_NULO segundos=%.1f" % (time.time() - t0))
    return 0 if ver in ("PASS", "INCOMPLETO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
