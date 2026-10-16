#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
output_control_region_null.py :: nulo que conserva region y tamano, para la 005 y la 006.

Pedido 2026-10-10 (Abraham): "Run a region-preserving null".

La 006 barajo las etiquetas de clase entre neuronas del mismo tamano (estr). Quedo abierto si
los BAJO del optico y de la proyeccion visual eran pura geografia: estan lejos de la zona
subesofagica, donde viven casi todas las salidas. Aca la etiqueta se baraja solo entre
neuronas de la misma REGION y del mismo TAMANO:

  region  k-medias sobre la posicion de cada neurona en la anotacion (pos_x, pos_y, pos_z, en
          voxeles de 4 x 4 x 40 nm, pasados a micrometros). La tienen todas las neuronas
          anotadas, tambien las ascendentes y sensoriales, que no tienen soma en el cerebro.
  tamano  estratos de ancho fijo en log(1 + fuerza de salida hacia no salidas), como en la 006
          pero mas gruesos (30 en vez de 100) para que region x tamano no quede vacio.

Dos granularidades: k = 40 (zonas de ~130 um) y k = 120 (~90 um, escala de neuropilo). Un
flag es firme si sale igual con las dos y en los dos umbrales.

Solo D1 (la fraccion directa de la entrada). D2 queda NO MEDIDO con este nulo.

MEZCLA de una clase = fraccion esperada de sus etiquetas que caen en neuronas de otra clase al
barajar. Una clase que no comparte region x tamano con otras no se puede testear: con
MEZCLA < 0,10 su 'azar' se marca NM (no medido), no es evidencia de nada.

Controles que pueden dar rojo:
  CRUCE_006          D1 real igual (<= 1e-12) al de la 006; los flags de la 006 se leen de su JSON.
  CONTEOS/ESTRATOS   cada permutacion conserva los tamanos de clase (y por estrato).
  MEDIA_NULO         media del nulo contra su esperanza exacta, z con la varianza exacta (<= 6).
  VARIANZA_NULO      mediana de varianza empirica / exacta entre 0,9 y 1,1.
  CONTROL_NEGATIVO   etiquetados falsos del mismo nulo: flags <= max(3, 3 x esperado).
  R_PEDIDO_500       con R < 500 el veredicto no puede ser PASS.
"""
import argparse
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd
import scipy

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import output_control_by_class as oc  # noqa: E402
import output_control_permutation_null as pn  # noqa: E402

SEED = 20261012
R_PERM = 5000
R_MINIMO = 500
N_FALSOS = 20
K_REGIONES = (40, 120)
N_TAM = 30
MEZCLA_MIN = 0.10
UM_POR_VOXEL = np.array([0.004, 0.004, 0.040])
P_FLAG = oc.P_FLAG
Z_MAX = pn.Z_MAX
FACTOR_CONTROL = pn.FACTOR_CONTROL
TOL_CRUCE = 1e-12


def _xn(v):
    """oc._x que acepta None."""
    return oc._x(np.nan if v is None else float(v))


def leer_posiciones(path, id_of):
    """pos_x, pos_y, pos_z de la anotacion (voxeles de 4 x 4 x 40 nm) en micrometros, alineadas a id_of."""
    a = pd.read_csv(path, sep="\t", dtype=str, usecols=["root_id", "pos_x", "pos_y", "pos_z"], low_memory=False)
    rid = a["root_id"].astype("int64").to_numpy()
    dup = pd.Index(rid).duplicated(keep="first")
    a = a[~dup]
    rid = rid[~dup]
    xyz = np.column_stack([pd.to_numeric(a[c], errors="coerce").to_numpy(dtype=np.float64)
                           for c in ("pos_x", "pos_y", "pos_z")]) * UM_POR_VOXEL[None, :]
    pos = pd.Index(rid).get_indexer(id_of)
    X = np.full((len(id_of), 3), np.nan)
    m = pos >= 0
    X[m] = xyz[pos[m]]
    return X, np.isfinite(X).all(axis=1)


def _asignar(X, C, bloque=20000):
    out = np.empty(len(X), dtype=np.int64)
    cc = (C ** 2).sum(axis=1)
    for i in range(0, len(X), bloque):
        x = X[i:i + bloque]
        d = (x ** 2).sum(axis=1)[:, None] - 2.0 * (x @ C.T) + cc[None, :]
        out[i:i + bloque] = np.argmin(d, axis=1)
    return out


def kmedias(X, k, semilla, iters=100):
    """Lloyd con arranque k-means++; determinista dada la semilla."""
    rng = np.random.default_rng(semilla)
    n = len(X)
    C = np.empty((k, X.shape[1]))
    C[0] = X[rng.integers(n)]
    d2 = ((X - C[0]) ** 2).sum(axis=1)
    for j in range(1, k):
        C[j] = X[rng.choice(n, p=d2 / d2.sum())]
        d2 = np.minimum(d2, ((X - C[j]) ** 2).sum(axis=1))
    lab = np.full(n, -1, dtype=np.int64)
    convergio = False
    it = 0
    for it in range(1, iters + 1):
        nuevo = _asignar(X, C)
        if np.array_equal(nuevo, lab):
            convergio = True
            break
        lab = nuevo
        cnt = np.bincount(lab, minlength=k)
        for d in range(X.shape[1]):
            C[:, d] = np.bincount(lab, weights=X[:, d], minlength=k) / np.maximum(cnt, 1)
        for j in np.flatnonzero(cnt == 0):
            C[j] = X[int(np.argmax(((X - C[lab]) ** 2).sum(axis=1)))]
    inercia = float(((X - C[lab]) ** 2).sum())
    return lab, {"k": int(k), "iteraciones": int(it), "convergio": bool(convergio), "inercia_um2": inercia,
                 "tamanos": np.bincount(lab, minlength=k)}


def regiones(X, tiene, k, semilla):
    """Region por k-medias para las neuronas con posicion; las que no tienen van a una region aparte (k)."""
    reg = np.full(len(X), k, dtype=np.int64)
    lab, info = kmedias(X[tiene], k, semilla)
    reg[tiene] = lab
    info["sin_posicion"] = int((~tiene).sum())
    return reg, info


def combinar(reg, tam):
    """Estrato = region x tamano, renumerado 0..B-1."""
    clave = np.asarray(reg, dtype=np.int64) * (int(np.max(tam)) + 1) + np.asarray(tam, dtype=np.int64)
    _, est = np.unique(clave, return_inverse=True)
    return est.astype(np.int64)


def mezcla(cls, est, K):
    """Fraccion esperada de las etiquetas de cada clase que caen en neuronas de otra clase al barajar."""
    est = np.asarray(est, dtype=np.int64)
    nb = int(est.max()) + 1
    n_b = np.bincount(est, minlength=nb).astype(np.float64)
    n_cb = np.bincount(np.asarray(cls, dtype=np.int64) * nb + est, minlength=K * nb).reshape(K, nb)
    n_cb = n_cb.astype(np.float64)
    n_c = n_cb.sum(axis=1)
    m = (n_cb * (1.0 - n_cb / np.maximum(n_b, 1.0)[None, :])).sum(axis=1)
    return np.where(n_c > 0, m / np.maximum(n_c, 1.0), 0.0)


def flag_efectivo(flag, mez, minimo=MEZCLA_MIN):
    """El 'azar' de una clase que casi no se mezcla (mezcla < minimo) es NM: el nulo no la puede mover."""
    flag = np.asarray(flag).astype("<U5")
    mez = np.asarray(mez, dtype=np.float64)
    if flag.ndim == 2:
        mez = mez[:, None]
    return np.where((flag == "azar") & (mez < minimo), "NM", flag).astype("<U5")


class PermutadorRapido:
    """Permutacion uniforme dentro de cada estrato con un solo argsort: clave = estrato + U(0,1)."""

    def __init__(self, cls, est):
        self.cls = np.asarray(cls)
        self.estf = np.asarray(est, dtype=np.float64)
        self.base = np.argsort(np.asarray(est), kind="stable")

    def __call__(self, rng):
        orden = np.argsort(self.estf + rng.random(len(self.cls)))
        out = np.empty_like(self.cls)
        out[self.base] = self.cls[orden]
        return out


def correr_nulo_rapido(cls, est, U, K, R, semilla, nb_chequeo=50, progreso=None, etiqueta=""):
    perm = PermutadorRapido(cls, est)
    sumar = pn.Sumador(len(cls), K)
    rng = np.random.default_rng(semilla)
    est = np.asarray(est, dtype=np.int64)
    conteo = np.bincount(cls, minlength=K)
    nb = int(est.max()) + 1
    conteo_est = np.bincount(np.asarray(cls, dtype=np.int64) * nb + est, minlength=K * nb)
    nul = np.empty((R, K, U.shape[1]))
    ok_conteo = True
    ok_est = True
    t0 = time.time()
    for r in range(R):
        lab = perm(rng)
        ok_conteo = ok_conteo and bool(np.array_equal(np.bincount(lab, minlength=K), conteo))
        if r < nb_chequeo:
            le = np.asarray(lab, dtype=np.int64) * nb + est
            ok_est = ok_est and bool(np.array_equal(np.bincount(le, minlength=K * nb), conteo_est))
        nul[r] = sumar(lab, U)
        if progreso is not None and (r + 1) % 1000 == 0:
            progreso("%s r=%d seg=%.1f" % (etiqueta, r + 1, time.time() - t0))
    return nul, ok_conteo, ok_est, time.time() - t0


def cruce_006(j006, etq, nombres, conjuntos, D1, n_in):
    if j006 is None:
        return {"estado": "NO_MEDIDO", "motivo": "sin JSON de la 006"}, {}
    if list(j006.get("clases_orden", [])) != list(nombres):
        return {"estado": "FAIL", "motivo": "clases distintas"}, {}
    var = j006["variantes"][etq]["por_conjunto"]
    maxdif = 0.0
    faltan = 0
    n_dif = 0
    f006 = {}
    for k, O in enumerate(conjuntos):
        b = var.get(O)
        if b is None:
            faltan += 1
            continue
        if int(b["n_con_entrada"]) != n_in[O]:
            n_dif += 1
        for c, cn in enumerate(nombres):
            pc = b["por_clase"][cn]
            v = pc.get("d1")
            if v is None:
                if n_in[O] != 0:
                    faltan += 1
            else:
                maxdif = max(maxdif, abs(float(v) - float(D1[c, k])))
            f006[(O, c)] = {"estr": pc["estr"]["flag1"], "enr_estr": pc["estr"]["enr1"], "perm": pc["perm"]["flag1"]}
    ok = maxdif <= TOL_CRUCE and faltan == 0 and n_dif == 0
    return {"estado": "PASS" if ok else "FAIL", "max_dif": maxdif, "faltan": faltan,
            "n_con_entrada_distinto": n_dif}, f006


def imprimir_nivel1(etq, O, k, n_in, nombres, D1, evs, fes, f006, modos):
    print("-- NIVEL1 %s [%s] | con_entrada=%d" % (O, etq, n_in[O]))
    cab = "%-19s %7s %-6s %6s" % ("clase", "D1%", "estr06", "enrE")
    for md in modos:
        cab += " %7s %6s %-5s" % (md + "%", "x" + md[3:], "f" + md[3:])
    print(cab)
    for c, cn in enumerate(nombres):
        f = f006.get((O, c), {})
        fila = "%-19s %s %-6s %s" % (cn, oc._p(D1[c, k]), f.get("estr") or "-", _xn(f.get("enr_estr")))
        for md in modos:
            fila += " %s %s %-5s" % (oc._p(evs[md]["media"][c, k]), oc._x(evs[md]["enr"][c, k]), fes[md][c, k])
        print(fila)


def imprimir_finas(etq, lista, n1, n_in, nombres, D1, fes, f006, modos, top=3):
    print("-- FINAS [%s] (D1, top %d; flags estr06 / %s) --" % (etq, top, " / ".join(modos)))
    for k, O in enumerate(lista):
        if O in n1:
            continue
        orden = np.argsort(-D1[:, k], kind="stable")[:top]
        partes = []
        for c in orden:
            f = f006.get((O, c), {})
            partes.append("%s %s%% estr=%s %s" % (nombres[c], oc._p(D1[c, k]).strip(), f.get("estr") or "-",
                                                 " ".join("%s=%s" % (md, fes[md][c, k]) for md in modos)))
        print("FINA [%s] %-40s con_entrada=%4d : %s" % (etq, O, n_in[O], " | ".join(partes)))


def comparar(etq, lista, nombres, D1, evs, fes, f006, modos, validas):
    a_md, b_md = modos
    mant = camb = nuev = inest = 0
    lineas = []
    for k, O in enumerate(lista):
        if not validas[k]:
            continue
        for c, cn in enumerate(nombres):
            e = (f006.get((O, c)) or {}).get("estr") or "-"
            a = str(fes[a_md][c, k])
            b = str(fes[b_md][c, k])
            xs = "D1 %s%% x%s/x%s" % (oc._p(D1[c, k]).strip(), oc._x(evs[a_md]["enr"][c, k]).strip(),
                                      oc._x(evs[b_md]["enr"][c, k]).strip())
            if a != b:
                inest += 1
                lineas.append("INESTABLE [%s] %-40s %-19s estr06=%-5s %s=%-5s %s=%-5s %s"
                              % (etq, O, cn, e, a_md, a, b_md, b, xs))
            elif e in ("SOBRE", "BAJO"):
                if a == e:
                    mant += 1
                else:
                    camb += 1
                    lineas.append("CAMBIA    [%s] %-40s %-19s estr06=%-5s -> region=%-5s %s" % (etq, O, cn, e, a, xs))
            elif a in ("SOBRE", "BAJO"):
                nuev += 1
                lineas.append("NUEVO     [%s] %-40s %-19s estr06=%-5s -> region=%-5s %s" % (etq, O, cn, e, a, xs))
    for linea in lineas:
        print(linea)
    return mant, camb, nuev, inest


def contar(fl):
    return int((fl == "SOBRE").sum()), int((fl == "BAJO").sum()), int((fl == "NM").sum())


def main(argv=None):
    ap = argparse.ArgumentParser(description="Nulo que conserva region y tamano para la 005 y la 006")
    ap.add_argument("--parquet", default="/workspace/connectivity.parquet")
    ap.add_argument("--annotations", default="/workspace/annotations.tsv")
    ap.add_argument("--json-006", default="results/output_control_permnull_2026-10-10/output_control_permutation_null.json")
    ap.add_argument("--out", default="results/output_control_regionnull_2026-10-10")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--r", type=int, default=R_PERM)
    ap.add_argument("--n-falsos", type=int, default=N_FALSOS)
    ap.add_argument("--k-regiones", default=",".join(str(k) for k in K_REGIONES))
    ap.add_argument("--n-tam", type=int, default=N_TAM)
    ap.add_argument("--maquina", default="brain-env")
    args = ap.parse_args(argv)
    t0 = time.time()
    os.makedirs(args.out, exist_ok=True)
    ks = [int(x) for x in args.k_regiones.split(",")]
    if len(ks) != 2:
        raise SystemExit("ERROR --k-regiones necesita dos granularidades")
    modos = ["reg%d" % k for k in ks]

    def progreso(msg):
        sys.stderr.write("PROGRESO %s t=%.1f\n" % (msg, time.time() - t0))
        sys.stderr.flush()

    print("== output_control_region_null.py :: nulo que conserva region y tamano para la 005 y la 006 ==")
    entorno = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
               "pandas": pd.__version__, "maquina": args.maquina}
    print("ENTORNO " + " ".join("%s=%s" % kv for kv in entorno.items()))
    print("PARAMETROS seed=%d r=%d n_falsos=%d k_regiones=%s n_tam=%d p_flag=%g mezcla_min=%g z_max=%g"
          " factor_control=%g" % (args.seed, args.r, args.n_falsos, args.k_regiones, args.n_tam, P_FLAG,
                                  MEZCLA_MIN, Z_MAX, FACTOR_CONTROL))
    md5p = oc.md5_archivo(args.parquet)
    md5a = oc.md5_archivo(args.annotations)
    j006 = None
    md5j = None
    if args.json_006 and os.path.exists(args.json_006):
        md5j = oc.md5_archivo(args.json_006)
        with open(args.json_006) as f:
            j006 = json.load(f)
    print("INPUT parquet %s md5=%s pin_ok=%s" % (args.parquet, md5p, md5p == oc.PIN_PARQUET_MD5))
    print("INPUT annotations %s md5=%s pin_ok=%s" % (args.annotations, md5a, md5a == oc.PIN_ANNOT_MD5))
    print("INPUT json_006 %s md5=%s" % (args.json_006, md5j))

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
    X, tiene = leer_posiciones(args.annotations, id_of)
    rx = [(float(np.nanmin(X[:, d])), float(np.nanmax(X[:, d]))) for d in range(3)]
    print("POSICIONES con_pos=%d sin_pos=%d rango_um x=%.1f-%.1f y=%.1f-%.1f z=%.1f-%.1f"
          % (int(tiene.sum()), int((~tiene).sum()), rx[0][0], rx[0][1], rx[1][0], rx[1][1], rx[2][0], rx[2][1]))
    regs = {}
    info_reg = {}
    for k, md in zip(ks, modos):
        reg, info = regiones(X, tiene, k, [args.seed, k])
        regs[md] = reg
        info_reg[md] = info
        t = info["tamanos"]
        print("REGIONES k=%d iteraciones=%d convergio=%s inercia_um2=%.4g tam_min=%d tam_mediana=%d tam_max=%d"
              " sin_posicion=%d" % (k, info["iteraciones"], info["convergio"], info["inercia_um2"], int(t.min()),
                                   int(np.median(t)), int(t.max()), info["sin_posicion"]))
    n1, n2 = oc.conjuntos_salida(anot["super_class"], anot["cell_sub_class"], anot["cell_type"])
    conjuntos = dict(n1)
    conjuntos.update({k: v for k, v in n2.items() if k not in n1})
    lista = list(conjuntos)
    es_salida = np.zeros(n, dtype=bool)
    for s_ in oc.SALIDAS:
        es_salida[n1[s_]] = True
    print("CONJUNTOS %d (nivel1 %d + finos %d) neuronas_de_salida=%d"
          % (len(lista), len(n1), len(lista) - len(n1), int(es_salida.sum())))

    resultado = {"schema": "output_control_region_null/v1", "entorno": entorno,
                 "parametros": {"seed": args.seed, "r": args.r, "n_falsos": args.n_falsos, "k_regiones": ks,
                                "n_tam": args.n_tam, "p_flag": P_FLAG, "mezcla_min": MEZCLA_MIN, "z_max": Z_MAX,
                                "factor_control": FACTOR_CONTROL},
                 "inputs": {"parquet_md5": md5p, "annotations_md5": md5a, "json_006": args.json_006,
                            "json_006_md5": md5j},
                 "clases": conteos, "clases_orden": nombres, "conjuntos": lista, "regiones": info_reg,
                 "variantes": {}}
    oks = {"mapeo": bool(ginfo["mapeo_biyectivo"])}
    estados_cruce = []
    g = {}
    for umbral, etq in ((1, ">=1"), (5, ">=5")):
        V = pn.vectores_u(pre, post, S, n, umbral, conjuntos)
        _, tam, ancho = pn.estratos_por_fuerza(V["p"], V["q"], V["s"], n, es_salida, args.n_tam)
        _, est06, _ = pn.estratos_por_fuerza(V["p"], V["q"], V["s"], n, es_salida, pn.N_ESTRATOS)
        del V["p"], V["q"], V["s"]
        m, n_in = V["m"], V["n_in"]
        U1 = np.ascontiguousarray(V["U"][:, :m])
        del V
        D1 = pn.Sumador(n, K)(cls, U1)
        cruce, f006 = cruce_006(j006, etq, nombres, lista, D1, n_in)
        estados_cruce.append(cruce["estado"])
        validas = np.array([n_in[O] > 0 for O in lista])
        print("== VARIANTE %s | conjuntos_con_entrada=%d/%d | tamano: estratos=%d ancho_log=%.4f factor=%.3f =="
              % (etq, int(validas.sum()), len(lista), int(tam.max()) + 1, ancho, float(np.exp(ancho))))
        estratos = {md: combinar(regs[md], tam) for md in modos}
        info_est = {}
        for md in modos:
            tb = np.bincount(estratos[md])
            info_est[md] = {"n": int(len(tb)), "unitarios": int((tb == 1).sum()), "tam_max": int(tb.max())}
            print("ESTRATOS [%s] %s n=%d unitarios=%d tam_max=%d"
                  % (etq, md, len(tb), int((tb == 1).sum()), int(tb.max())))
        mez = {"perm": 1.0 - np.bincount(cls, minlength=K) / float(n), "estr06": mezcla(cls, est06, K)}
        for md in modos:
            mez[md] = mezcla(cls, estratos[md], K)
        print("MEZCLA [%s] %-19s %6s %6s %6s %s" % (etq, "clase", "n", "perm", "estr06",
                                                  " ".join("%6s" % md for md in modos)))
        for c, cn in enumerate(nombres):
            print("MEZCLA [%s] %-19s %6d %6.3f %6.3f %s" % (etq, cn, conteos[cn], mez["perm"][c], mez["estr06"][c],
                                                          " ".join("%6.3f" % mez[md][c] for md in modos)))
        evs, fes, info_modos = {}, {}, {}
        for mi, md in enumerate(modos):
            est = estratos[md]
            nul, okc, oke, seg = correr_nulo_rapido(cls, est, U1, K, args.r, [args.seed, umbral, mi],
                                                    progreso=progreso, etiqueta="%s %s" % (etq, md))
            ev = pn.evaluar_nulo(D1, nul)
            ev["flag"][:, ~validas] = "NA"
            esp = pn.esperanza(cls, est, U1, K, "estr")
            var = pn.varianza_exacta(cls, est, U1, K, "estr")
            zmax, vratio = pn.chequeo_momentos(ev["media"], ev["sd"], esp, var, args.r, validas)
            var_ok = bool(0.9 <= vratio <= 1.1)
            ctrl = pn.control_negativo(cls, est, "estr", U1, K, nul, args.n_falsos, [args.seed, umbral, mi, 99],
                                       np.flatnonzero(validas))
            del nul
            evs[md] = ev
            fes[md] = flag_efectivo(ev["flag"], mez[md])
            info_modos[md] = {"segundos": seg, "conteos_ok": okc, "estratos_ok": oke, "media_max_z": zmax,
                              "media_ok": bool(zmax <= Z_MAX), "var_ratio_mediana": vratio, "varianza_ok": var_ok,
                              "control_negativo": ctrl}
            oks["conteos_%s_%s" % (md, etq)] = okc
            oks["estratos_%s_%s" % (md, etq)] = oke
            oks["media_%s_%s" % (md, etq)] = bool(zmax <= Z_MAX)
            oks["varianza_%s_%s" % (md, etq)] = var_ok
            oks["control_%s_%s" % (md, etq)] = ctrl["ok"]
            print("NULO [%s] %s R=%d segundos=%.1f conteos_ok=%s estratos_ok=%s media_max_z=%.2f"
                  " var_ratio_mediana=%.4f" % (etq, md, args.r, seg, okc, oke, zmax, vratio))
        for k, O in enumerate(lista):
            if O in n1:
                imprimir_nivel1(etq, O, k, n_in, nombres, D1, evs, fes, f006, modos)
        imprimir_finas(etq, lista, n1, n_in, nombres, D1, fes, f006, modos)
        mant, camb, nuev, inest = comparar(etq, lista, nombres, D1, evs, fes, f006, modos, validas)
        tests = int(K * validas.sum())
        e06 = np.array([[(f006.get((O, c)) or {}).get("estr") or "-" for k, O in enumerate(lista) if validas[k]]
                        for c in range(K)])
        s06, b06, _ = contar(e06)
        partes = []
        for md in modos:
            s_, b_, nm_ = contar(fes[md][:, validas])
            partes.append("%s SOBRE=%d BAJO=%d NM=%d" % (md, s_, b_, nm_))
        acuerdo = int((fes[modos[0]][:, validas] == fes[modos[1]][:, validas]).sum())
        print("RESUMEN [%s] D1 tests=%d | estr06 SOBRE=%d BAJO=%d | %s | acuerdo_%s_%s=%d/%d"
              " | estr06->region se_mantienen=%d cambian=%d nuevos=%d inestables=%d"
              % (etq, tests, s06, b06, " | ".join(partes), modos[0], modos[1], acuerdo, tests, mant, camb, nuev,
                 inest))
        print("CRUCE_006 [%s] %s %s" % (etq, cruce["estado"], " ".join("%s=%s" % kv for kv in cruce.items()
                                                                        if kv[0] != "estado")))
        for md in modos:
            c_ = info_modos[md]["control_negativo"]
            print("CONTROL_NEGATIVO [%s] %s flags=%d/%d esperado=%.2f tope=%.2f OK=%s"
                  % (etq, md, c_["flags"], c_["tests"], c_["esperado"], c_["tope"], c_["ok"]))
        g[etq] = {"D1": D1, "evs": evs, "fes": fes, "validas": validas, "mez": mez}
        por_conj = {}
        for k, O in enumerate(lista):
            pc = {}
            for c, cn in enumerate(nombres):
                f = f006.get((O, c)) or {}
                d = {"d1": D1[c, k], "estr006": f.get("estr"), "enr006": f.get("enr_estr"), "perm006": f.get("perm")}
                for md in modos:
                    ev = evs[md]
                    d[md] = {"media": ev["media"][c, k], "sd": ev["sd"][c, k], "enr": ev["enr"][c, k],
                             "ps": ev["ps"][c, k], "pb": ev["pb"][c, k], "flag": ev["flag"][c, k],
                             "flag_ef": fes[md][c, k]}
                pc[cn] = d
            por_conj[O] = {"n_con_entrada": n_in[O], "por_clase": pc}
        resultado["variantes"][etq] = {"tamano": {"n": int(tam.max()) + 1, "ancho_log": ancho},
                                       "estratos": info_est,
                                       "mezcla": {md: {cn: float(mez[md][c]) for c, cn in enumerate(nombres)}
                                                  for md in mez},
                                       "cruce_006": cruce, "modos": info_modos,
                                       "conteo": {"tests": tests, "estr06": [s06, b06], "se_mantienen": mant,
                                                  "cambian": camb, "nuevos": nuev, "inestables": inest},
                                       "por_conjunto": por_conj}
    print("-- QUE CONTROLA CADA CLASE CON REGION Y TAMANO (D1; firme = igual en %s, %s, >=1 y >=5) --"
          % (modos[0], modos[1]))
    firmes = {}
    for c, cn in enumerate(nombres):
        sob, baj_n1, baj_finos = [], [], 0
        for k, O in enumerate(lista):
            if not (g[">=1"]["validas"][k] and g[">=5"]["validas"][k]):
                continue
            fl = [str(g[e]["fes"][md][c, k]) for e in (">=1", ">=5") for md in modos]
            if all(f == "SOBRE" for f in fl):
                sob.append("%s x%s/x%s" % (O, oc._x(g[">=1"]["evs"][modos[0]]["enr"][c, k]).strip(),
                                           oc._x(g[">=1"]["evs"][modos[1]]["enr"][c, k]).strip()))
            elif all(f == "BAJO" for f in fl):
                if O in n1:
                    baj_n1.append(O)
                else:
                    baj_finos += 1
        mz = min(float(g[e]["mez"][md][c]) for e in (">=1", ">=5") for md in modos)
        linea = ("QUE_CONTROLA_REGION %s: mezcla_min=%.3f %s | SOBRE: %s | BAJO: %s + %d finos"
                 % (cn, mz, "sin_poder" if mz < MEZCLA_MIN else "con_poder", ", ".join(sob) or "ninguna",
                    ", ".join(baj_n1) or "ninguna de nivel1", baj_finos))
        print(linea)
        firmes[cn] = linea
    resultado["que_controla_region"] = firmes
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
    resultado["veredicto"] = {"nulo": ver, "r_ok": r_ok, "chequeos": oks, "cruce_006": estados_cruce}
    resultado["segundos"] = time.time() - t0
    salida = os.path.join(args.out, "output_control_region_null.json")
    with open(salida, "w") as f:
        json.dump(oc.a_py(resultado), f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("JSON %s md5=%s" % (salida, oc.md5_archivo(salida)))
    print("VEREDICTO_NULO %s" % ver)
    print("FIN_NULO segundos=%.1f" % (time.time() - t0))
    return 0 if ver in ("PASS", "INCOMPLETO") else 1


if __name__ == "__main__":
    raise SystemExit(main())
