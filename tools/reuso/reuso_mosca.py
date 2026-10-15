#!/usr/bin/env python3
"""H_REUSO: la misma plantilla de circuito sirve a distintas acciones, en FlyWire v783 y otra vez en BANC 888
(respuesta 2026-10-14-029).

Idea de Abraham (2026-10-14-028): mucho de la mosca seria lo mismo aplicado de distintas formas para distintas acciones.
Primer indicio, descriptivo y post hoc: LHAD1g1 y PVLP010 inhiben a DNp01 (despegue) y a DNp06 (giro).

Plantilla, escrita antes de mirar (inhibicion de avance, FFI):
  un sensor S (unidad = tipo y lado, super_class visual_projection) y una descendente D (unidad = tipo y lado,
  super_class descending) del MISMO lado forman un par cableado si S le da a D >= 20 sinapsis directas;
  el par tiene la plantilla si existe una neurona inhibitoria X (que no es sensor ni descendente) con >= 5 sinapsis
  desde S y >= 5 sinapsis sobre D.
Estadisticos:
  T1 = fraccion de pares cableados que tienen la plantilla.
  T2 = cuantas X hacen la plantilla para dos o mas TIPOS de descendente distintos (la misma pieza para varias acciones).
Nulo SL: los destinos de todas las aristas se barajan dentro de cada bloque (lado pre, lado post); conserva cuantas
aristas salen de cada neurona y cuantas llegan, el peso y el signo (que van con la presinaptica). Puede crear aristas
repetidas; se suman. p = (1 + #nulos >= observado) / (N + 1).
Signo: FlyWire, columna Excitatory (convencion de Shiu). BANC, neurotransmitter_predicted: gaba o glutamate es
inhibitoria; el resto, incluso sin prediccion, no. Tipos en BANC: fafb_cell_type y, si falta, cell_type.
Hipotesis (alfa 0,05, Holm sobre las 4 pruebas: T1 y T2 en FlyWire y en BANC):
  por conectoma: SOSTENIDA si T1 y T2 pasan Holm; REFUTADA si ninguna tiene p crudo < 0,05; si no, PARCIAL.
  H_REUSO: SOSTENIDA si las dos son SOSTENIDA; REFUTADA si FlyWire es REFUTADA; NO_SE_REPLICA si FlyWire es
  SOSTENIDA y BANC REFUTADA; si no, SIN_DECIDIR. INVALIDO si falla un control.
Controles (INVALIDO si fallan): FlyWire, (LPLC2, DNp06) es par cableado en los dos lados y LHAD1g1 esta entre sus X
(lo de la 024); BANC, (LPLC2, DNp06) es par cableado en los dos lados. Guarda del nulo: conserva grados y bloques.
Descriptivo (sin veredicto): los tipos de X compartidos y a que descendentes sirven; cuantos se repiten entre conectomas.
Con --humo: 2 nulos y CIEGO (no imprime T1, T2, p ni listas; solo tamanos, tiempos y controles).
Salida: 0 completo; 2 insumos distintos del pin; 3 control o guarda fallida.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time

import numpy as np
import pandas as pd

PIN = dict(conn="3d802fd542b5d18570ba1ba0bb0abed9", annot="719904abad876c68ace1b5690c9b9b63",
           banc_meta="8c2b93a6", banc_aristas="08542b07")
W_DIR, W_X = 20, 5
N_NULO, ALFA = 200, 0.05
LADOS = ("left", "right")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def pr(s):
    print(s, flush=True)


def armar(pre, post, w, inh, tipo, lado, sc):
    """pre, post: indices de neurona (int32); inh, tipo, lado, sc: por neurona."""
    n = len(tipo)
    lado = np.asarray(lado, dtype=object)
    tipo = np.asarray(tipo, dtype=object)
    sc = np.asarray(sc, dtype=object)
    ok_l = np.isin(lado, LADOS)
    ok_t = pd.notna(tipo)

    def unidades(mask):
        claves = sorted(set(zip(tipo[mask], lado[mask])))
        idx = {k: i for i, k in enumerate(claves)}
        u = np.full(n, -1, dtype=np.int32)
        for j in np.nonzero(mask)[0]:
            u[j] = idx[(tipo[j], lado[j])]
        return u, claves
    S, cs = unidades((sc == "visual_projection") & ok_l & ok_t)
    D, cd = unidades((sc == "descending") & ok_l & ok_t)
    sl = np.array([0 if x == "left" else 1 if x == "right" else 2 for x in lado], dtype=np.int8)
    bloque = (sl[pre].astype(np.int16) * 3 + sl[post]).astype(np.int8)
    orden = np.argsort(bloque, kind="stable")
    cortes = np.searchsorted(bloque[orden], np.arange(10))
    tipos_d = sorted(set(k[0] for k in cd))
    d_tipo = np.array([tipos_d.index(k[0]) for k in cd], dtype=np.int32)
    mismo = np.array([[a[1] == b[1] for b in cd] for a in cs], dtype=bool)
    excl = (S >= 0) | (D >= 0)
    return dict(pre=pre, post=post, w=w.astype(np.int32), inh=np.asarray(inh, dtype=bool), S=S, D=D, cs=cs, cd=cd,
                tipo=tipo, sl=sl, orden=orden, cortes=cortes, d_tipo=d_tipo, mismo=mismo, excl=excl, n=n)


def _agrupar(k, w, minimo):
    if len(k) == 0:
        return np.zeros(0, dtype=np.int64)
    u, inv = np.unique(k, return_inverse=True)
    s = np.bincount(inv, weights=w)
    return u[s >= minimo]


def estadisticas(d, post, detalle=False):
    pre, w, S, D, inh, n = d["pre"], d["w"], d["S"], d["D"], d["inh"], d["n"]
    nS, nD = len(d["cs"]), len(d["cd"])
    sS, dD = S[pre], D[post]
    m = (sS >= 0) & (dD >= 0)
    agg = np.bincount(sS[m].astype(np.int64) * nD + dD[m], weights=w[m], minlength=nS * nD)
    cab = (agg >= W_DIR) & d["mismo"].ravel()
    xs = inh & ~d["excl"]
    m1 = (sS >= 0) & xs[post]
    b1 = _agrupar(sS[m1].astype(np.int64) * n + post[m1], w[m1], W_X)
    m2 = xs[pre] & (dD >= 0)
    b2 = _agrupar(pre[m2].astype(np.int64) * nD + dD[m2], w[m2], W_X)
    f1 = pd.DataFrame(dict(s=b1 // n, x=b1 % n))
    f2 = pd.DataFrame(dict(x=b2 // nD, dd=b2 % nD))
    j = f1.merge(f2, on="x")
    j = j[cab[j.s.to_numpy() * nD + j.dd.to_numpy()]]
    pares = j[["s", "dd"]].drop_duplicates()
    n_cab = int(cab.sum())
    t1 = len(pares) / n_cab if n_cab else 0.0
    j = j.assign(dt=d["d_tipo"][j.dd.to_numpy()])
    por_x = j.groupby("x").dt.nunique()
    t2 = int((por_x >= 2).sum())
    out = dict(n_cab=n_cab, t1=float(t1), t2=t2, n_pares_ffi=int(len(pares)), n_x=int(len(por_x)))
    if detalle:
        out["j"], out["cab"] = j, cab
    return out


def nulo(d, rng):
    post, orden, cortes = d["post"], d["orden"], d["cortes"]
    nuevo = post.copy()
    for b in range(9):
        ix = orden[cortes[b]:cortes[b + 1]]
        if len(ix) > 1:
            nuevo[ix] = post[ix][rng.permutation(len(ix))]
    return nuevo


def guarda_nulo(d, nuevo):
    n = d["n"]
    ok = bool((np.bincount(d["post"], minlength=n) == np.bincount(nuevo, minlength=n)).all())
    lado_ok = bool((d["sl"][nuevo] == d["sl"][d["post"]]).all())
    cambia = bool((nuevo != d["post"]).mean() > 0.5)
    return ok and lado_ok and cambia


def control(d, j, cab, exige_x):
    cs, cd, nD = d["cs"], d["cd"], len(d["cd"])
    res = {}
    for s in LADOS:
        if ("LPLC2", s) not in cs or ("DNp06", s) not in cd:
            res[s] = dict(cableado=False, x_lhad1g1=False)
            continue
        a, b = cs.index(("LPLC2", s)), cd.index(("DNp06", s))
        xs = j[(j.s == a) & (j.dd == b)].x.to_numpy()
        tipos = set(d["tipo"][xs].tolist())
        res[s] = dict(cableado=bool(cab[a * nD + b]), x_lhad1g1=bool("LHAD1g1" in tipos))
    pasa = all(res[s]["cableado"] and (res[s]["x_lhad1g1"] or not exige_x) for s in LADOS)
    return pasa, res


def correr(nombre, d, n_nulo, semilla, humo, exige_x):
    t0 = time.time()
    obs = estadisticas(d, d["post"], detalle=True)
    pasa, ctl = control(d, obs["j"], obs["cab"], exige_x)
    pr("%s UNIDADES sensores=%d descendentes=%d pares_cableados=%d | %.1f s" % (
        nombre, len(d["cs"]), len(d["cd"]), obs["n_cab"], time.time() - t0))
    pr("%s CONTROL %s -> %s" % (nombre, ctl, "PASA" if pasa else "FALLA"))
    rng = np.random.default_rng(semilla)
    n1, n2, guarda = [], [], True
    for k in range(n_nulo):
        nuevo = nulo(d, rng)
        if k < 3:
            guarda &= guarda_nulo(d, nuevo)
        e = estadisticas(d, nuevo)
        n1.append(e["t1"])
        n2.append(e["t2"])
        if k in (0, 9, 49, 99, 199):
            pr("%s NULO %d de %d | %.1f s" % (nombre, k + 1, n_nulo, time.time() - t0))
    n1, n2 = np.array(n1), np.array(n2)
    p1 = (1 + int((n1 >= obs["t1"]).sum())) / (n_nulo + 1.0)
    p2 = (1 + int((n2 >= obs["t2"]).sum())) / (n_nulo + 1.0)
    pr("%s GUARDA_NULO -> %s" % (nombre, guarda))
    res = dict(n_cab=obs["n_cab"], control=ctl, control_pasa=pasa, guarda=guarda, segundos=time.time() - t0)
    if not humo:
        res.update(t1=obs["t1"], t2=obs["t2"], n_pares_ffi=obs["n_pares_ffi"], n_x=obs["n_x"],
                   nulo_t1=[float(np.mean(n1)), float(np.max(n1))], nulo_t2=[float(np.mean(n2)), float(np.max(n2))],
                   p1=p1, p2=p2)
        pr("%s T1 fraccion_con_plantilla=%.4f nulo media=%.4f max=%.4f p=%.4f" % (nombre, obs["t1"], np.mean(n1),
                                                                              np.max(n1), p1))
        pr("%s T2 X_compartidas=%d nulo media=%.1f max=%d p=%.4f" % (nombre, obs["t2"], np.mean(n2), np.max(n2), p2))
        j = obs["j"]
        j = j.assign(xt=d["tipo"][j.x.to_numpy()])
        g = j.groupby("xt").dt.nunique().sort_values(ascending=False, kind="stable")
        tipos_d = sorted(set(k[0] for k in d["cd"]))
        top = []
        for xt, k in g.head(15).items():
            sirve = sorted(set(tipos_d[i] for i in j[j.xt == xt].dt))
            top.append([str(xt), int(k), sirve[:12]])
            pr("%s COMPARTIDA %s tipos_de_descendente=%d %s" % (nombre, xt, k, ",".join(sirve[:12])))
        res["compartidas_top"] = top
        res["tipos_compartidos"] = sorted(str(x) for x, k in g.items() if k >= 2)
    else:
        pr("%s HUMO CIEGO: no se imprimen T1, T2, p ni listas" % nombre)
    return res


def cargar_flywire(conn, annot):
    a = pd.read_csv(annot, sep=chr(9), dtype=str, usecols=["root_id", "cell_type", "side", "super_class"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(conn, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    ids, inv = np.unique(np.concatenate([c.Presynaptic_ID.to_numpy(), c.Postsynaptic_ID.to_numpy()]),
                         return_inverse=True)
    ne = len(c)
    pre, post = inv[:ne].astype(np.int32), inv[ne:].astype(np.int32)
    inh = np.zeros(len(ids), dtype=bool)
    inh[pre[c.Excitatory.to_numpy() < 0]] = True
    w = c.Connectivity.to_numpy()
    del c, inv
    a = a.drop_duplicates("root_id").set_index("root_id").reindex(ids)
    return armar(pre, post, w, inh, a.cell_type.to_numpy(), a.side.to_numpy(), a.super_class.to_numpy())


def cargar_banc(meta, aristas):
    m = pd.read_feather(meta, columns=["root_888", "side", "super_class", "cell_type", "fafb_cell_type",
                                       "neurotransmitter_predicted"])
    m = m.drop_duplicates("root_888").reset_index(drop=True)
    e = pd.read_feather(aristas, columns=["pre", "post", "count"])
    ix = pd.Index(m.root_888.astype(str))
    pre = ix.get_indexer(e.pre.astype(str)).astype(np.int32)
    post = ix.get_indexer(e.post.astype(str)).astype(np.int32)
    w = e["count"].to_numpy()
    del e
    if (pre < 0).any() or (post < 0).any():
        raise ValueError("aristas de BANC con ids fuera del meta")
    inh = m.neurotransmitter_predicted.isin(["gaba", "glutamate"]).to_numpy()
    tipo = m.fafb_cell_type.where(m.fafb_cell_type.notna(), m.cell_type).to_numpy()
    return armar(pre, post, w, inh, tipo, m.side.to_numpy(), m.super_class.to_numpy())


def holm(ps):
    ps = np.asarray(ps, dtype=float)
    orden = np.argsort(ps)
    adj, acc = np.zeros(len(ps)), 0.0
    for r, i in enumerate(orden):
        acc = max(acc, min(1.0, (len(ps) - r) * ps[i]))
        adj[i] = acc
    return adj


def veredicto_conectoma(p_crudo, p_holm):
    if all(p < ALFA for p in p_holm):
        return "SOSTENIDA"
    if all(p >= ALFA for p in p_crudo):
        return "REFUTADA"
    return "PARCIAL"


def veredicto_final(fw, banc, controles_ok):
    if not controles_ok:
        return "INVALIDO"
    if fw == "SOSTENIDA" and banc == "SOSTENIDA":
        return "SOSTENIDA"
    if fw == "REFUTADA":
        return "REFUTADA"
    if fw == "SOSTENIDA" and banc == "REFUTADA":
        return "NO_SE_REPLICA"
    return "SIN_DECIDIR"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--banc-meta", required=True)
    ap.add_argument("--banc-aristas", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--humo", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s | pandas %s" % (platform.node(), platform.platform(),
                                                                 platform.python_version(), np.__version__,
                                                                 pd.__version__))
    pr("# md5 instrumento = " + md5(os.path.abspath(__file__)))
    pr("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    got = dict(conn=md5(a.conn), annot=md5(a.annot), banc_meta=md5(a.banc_meta), banc_aristas=md5(a.banc_aristas))
    ok = all(got[k].startswith(PIN[k]) for k in PIN)
    pr("# md5 insumos = %s -> %s" % (got, ok))
    if not ok:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    n_nulo = 2 if a.humo else N_NULO
    if a.humo:
        pr("# HUMO CIEGO: 2 nulos, sin T1, T2 ni p")
    res = {}
    d = cargar_flywire(a.conn, a.annot)
    pr("FLYWIRE cargado: neuronas=%d aristas=%d inhibitorias=%d | %.1f s" % (d["n"], len(d["pre"]), int(d["inh"].sum()),
                                                                         time.time() - t0))
    res["flywire"] = correr("FLYWIRE", d, n_nulo, 2029, a.humo, True)
    del d
    d = cargar_banc(a.banc_meta, a.banc_aristas)
    pr("BANC cargado: neuronas=%d aristas=%d inhibitorias=%d | %.1f s" % (d["n"], len(d["pre"]), int(d["inh"].sum()),
                                                                      time.time() - t0))
    res["banc"] = correr("BANC", d, n_nulo, 2030, a.humo, False)
    del d
    ok_ctl = all(res[k]["control_pasa"] and res[k]["guarda"] for k in res)
    if not a.humo:
        ps = [res["flywire"]["p1"], res["flywire"]["p2"], res["banc"]["p1"], res["banc"]["p2"]]
        adj = holm(ps)
        vf = veredicto_conectoma(ps[:2], adj[:2])
        vb = veredicto_conectoma(ps[2:], adj[2:])
        h = veredicto_final(vf, vb, ok_ctl)
        res.update(holm=[float(x) for x in adj], H_REUSO_FLYWIRE=vf, H_REUSO_BANC=vb, H_REUSO=h)
        comun = sorted(set(res["flywire"]["tipos_compartidos"]) & set(res["banc"]["tipos_compartidos"]))
        res["compartidas_en_los_dos"] = comun
        pr("DESCRIPTIVO tipos_X_compartidos flywire=%d banc=%d en_los_dos=%d %s" % (
            len(res["flywire"]["tipos_compartidos"]), len(res["banc"]["tipos_compartidos"]), len(comun),
            ",".join(comun[:30])))
        pr("HOLM %s" % " ".join("%.4f" % x for x in adj))
        pr("H_REUSO_FLYWIRE -> %s | H_REUSO_BANC -> %s | H_REUSO -> %s" % (vf, vb, h))
    else:
        pr("CONTROLES_Y_GUARDAS -> %s (HUMO)" % ok_ctl)
    res["humo"], res["segundos"] = a.humo, time.time() - t0
    json.dump(res, open(os.path.join(a.out, "reuso.json"), "w"), indent=1, default=str)
    pr("EXIT_RUN=%d | %.1f s" % (0 if ok_ctl else 3, time.time() - t0))
    return 0 if ok_ctl else 3


if __name__ == "__main__":
    sys.exit(main())
