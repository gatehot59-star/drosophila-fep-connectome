#!/usr/bin/env python3
"""H_FRENO: que frena el giro de DNp06 ante el looming frontal en la mosca (respuesta 2026-10-14-023).

Contexto: H_TOPO_FIEL REFUTADA (2026-10-14-022): sin la resta contralateral, un looming de frente enciende las dos DNp06
y la mosca gira en vez de aterrizar. La resta no tiene via directa en FlyWire v783 (2026-10-14-020). Si la mosca frena
ese giro con algo cableado, tiene que aparecer como entrada INHIBITORIA sobre DNp06 desde alguno de estos mecanismos,
pre-registrados antes de mirar DNp06 (no son excluyentes: una X bilateral cuenta en M3 y en M6):
  Directos (sinapsis inhibitorias de la fuente sobre el objetivo):
    M1_DNP07: DNp07 (el comando de aterrizaje) -> objetivo.
    M1_DNP01: DNp01 (el comando de despegue) -> objetivo.
    M2_OPUESTA: el mismo tipo del otro lado -> objetivo (inhibicion mutua izquierda-derecha).
  A dos saltos (X inhibitoria sobre el objetivo, que recibe >= 5 sinapsis de la fuente):
    M3_CONTRA: fuente LPLC1 y LPLC2 del lado opuesto al objetivo (la resta del programa, por interneurona).
    M4_LPLC4: fuente LPLC4 de los dos lados (el detector de aterrizaje frena el giro).
    M5_DNP07: fuente DNp07 de los dos lados (el comando de aterrizaje frena el giro por interneurona).
    M6_BILATERAL: X recibe >= 5 de LPLC2 o LC4 izquierdas Y >= 5 de LPLC2 o LC4 derechas (un detector de frente).
Metrica: cuota = sinapsis inhibitorias por el mecanismo / sinapsis inhibitorias totales que recibe el objetivo, por lado.
Referencia: todas las unidades descendentes (super_class descending, tipo y lado) con >= 100 sinapsis inhibitorias de
entrada; percentil = fraccion de las otras del mismo lado (sin el objetivo) con cuota estrictamente menor.
Veredictos:
  A dos saltos: CANDIDATO si cuota >= 0,05 y percentil >= 0,90 en los dos lados; DESCARTADO si en los dos lados la
    cuota es < 0,05 o el percentil < 0,50; si no, DUDOSO.
  Directos: PRESENTE si >= 5 sinapsis inhibitorias en los dos lados; AUSENTE si < 5 en los dos; si no, ASIMETRICO.
  H_FRENO: SOSTENIDA si algun mecanismo es CANDIDATO o PRESENTE; REFUTADA si todos son DESCARTADO o AUSENTE; si no,
    SIN_DECIDIR. Son 7 mecanismos sin correccion por multiplicidad: lo declarado como CANDIDATO es candidato, no prueba.
  Control positivo (si falla, INVALIDO): la cuota EXCITATORIA directa desde LPLC1 y LPLC2 del mismo lado tiene que
    dar percentil >= 0,90 en los dos lados (lo que la 020 ya mostro cableado).
Signo: Excitatory del parquet (convencion de Shiu: GABA y glutamato inhibitorios). Descriptivo: GABA y glutamato por
separado segun top_nt de la presinaptica, y los 10 tipos inhibitorios que mas le dan al objetivo, con sus entradas.
Salida: 0 completo; 2 insumos distintos del pin; 3 instrumento invalido o objetivo inexistente.
Con --humo el objetivo es DNp01 (para probar la maquinaria sin mirar DNp06); sus numeros no valen para H_FRENO.
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

CONN_MD5, ANNOT_MD5 = "3d802fd542b5d18570ba1ba0bb0abed9", "719904abad876c68ace1b5690c9b9b63"
OBJETIVO, OBJETIVO_HUMO = "DNp06", "DNp01"
MIN_X, MIN_SIN, MIN_I = 5, 5, 100
CUOTA_MIN, PCT_MIN, PCT_DESCARTE = 0.05, 0.90, 0.50
LADOS = ("left", "right")
OPUESTO = {"left": "right", "right": "left"}
DOS_SALTOS = ("M3_CONTRA", "M4_LPLC4", "M5_DNP07", "M6_BILATERAL")
DIRECTOS = ("M1_DNP07", "M1_DNP01", "M2_OPUESTA")


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def pr(s):
    print(s, flush=True)


def ids(a, tipo, lado=None):
    m = a.cell_type == tipo
    if lado is not None:
        m = m & (a.side == lado)
    return set(a.root_id[m].tolist())


def calificados(c, fuente, minimo=MIN_X):
    e = c[c.Presynaptic_ID.isin(fuente)]
    w = e.groupby("Postsynaptic_ID").Connectivity.sum()
    return set(w[w >= minimo].index.tolist()) - set(fuente)


def percentil(serie, lado_de, u, min_ref, total):
    ref = [k for k in serie.index if k != u and lado_de[k] == lado_de[u] and total.get(k, 0) >= min_ref]
    v = np.array([serie[k] for k in ref])
    return float((v < serie[u]).mean()) if len(v) else float("nan"), len(v)


def calcular(a, c, objetivo, min_i=MIN_I):
    d = a[(a.super_class == "descending") & a.side.isin(LADOS) & a.cell_type.notna()]
    unidad = dict(zip(d.root_id, zip(d.cell_type, d.side)))
    uo = {s: (objetivo, s) for s in LADOS}
    if not all(u in set(unidad.values()) for u in uo.values()):
        return None
    tipo_de = dict(zip(a.root_id, a.cell_type))
    lado_n = dict(zip(a.root_id, a.side))
    e = c[c.Postsynaptic_ID.isin(set(unidad))].copy()
    e["u"] = e.Postsynaptic_ID.map(unidad)
    e["lado"] = e.u.map(lambda t: t[1])
    inh, exc = e[e.Excitatory < 0], e[e.Excitatory > 0]
    I = inh.groupby("u").Connectivity.sum()
    E = exc.groupby("u").Connectivity.sum()
    unidades = sorted(set(unidad.values()))
    lado_de = {u: u[1] for u in unidades}
    I = I.reindex(unidades, fill_value=0)
    E = E.reindex(unidades, fill_value=0)

    f = {}
    for s in LADOS:
        f[("LPLC12", s)] = ids(a, "LPLC1", s) | ids(a, "LPLC2", s)
        f[("FRENTE", s)] = ids(a, "LPLC2", s) | ids(a, "LC4", s)
    lplc4 = ids(a, "LPLC4")
    dnp07, dnp01 = ids(a, "DNp07"), ids(a, "DNp01")
    S = {}
    for s in LADOS:
        S[("M3_CONTRA", s)] = calificados(c, f[("LPLC12", OPUESTO[s])])
    q4, q5 = calificados(c, lplc4), calificados(c, dnp07)
    q6 = calificados(c, f[("FRENTE", "left")]) & calificados(c, f[("FRENTE", "right")])
    for s in LADOS:
        S[("M4_LPLC4", s)], S[("M5_DNP07", s)], S[("M6_BILATERAL", s)] = q4, q5, q6

    def sinapsis_por(tabla, mascara):
        return tabla[mascara].groupby("u").Connectivity.sum().reindex(unidades, fill_value=0)

    sin = {}
    for m in DOS_SALTOS:
        msk = np.zeros(len(inh), dtype=bool)
        for s in LADOS:
            msk |= ((inh.lado == s) & inh.Presynaptic_ID.isin(S[(m, s)])).to_numpy()
        sin[m] = sinapsis_por(inh, msk)
    sin["M1_DNP07"] = sinapsis_por(inh, inh.Presynaptic_ID.isin(dnp07).to_numpy())
    sin["M1_DNP01"] = sinapsis_por(inh, inh.Presynaptic_ID.isin(dnp01).to_numpy())
    pt = inh.Presynaptic_ID.map(tipo_de)
    ps = inh.Presynaptic_ID.map(lado_n)
    post_t = inh.u.map(lambda t: t[0])
    sin["M2_OPUESTA"] = sinapsis_por(inh, ((pt == post_t) & (ps == inh.lado.map(OPUESTO))).to_numpy())
    msk = np.zeros(len(exc), dtype=bool)
    for s in LADOS:
        msk |= ((exc.lado == s) & exc.Presynaptic_ID.isin(f[("LPLC12", s)])).to_numpy()
    pos = sinapsis_por(exc, msk)

    Isafe = I.replace(0, np.nan)
    res = dict(objetivo=objetivo, mecanismos={}, n_unidades=len(unidades),
               tamanos={"%s_%s" % (m, s): len(S[(m, s)]) for m in DOS_SALTOS for s in LADOS})
    for m in DOS_SALTOS + DIRECTOS:
        cuota = (sin[m] / Isafe).fillna(0.0)
        por_lado = {}
        for s in LADOS:
            u = uo[s]
            p, nref = percentil(cuota, lado_de, u, min_i, I)
            por_lado[s] = dict(sinapsis=int(sin[m][u]), inhibitorias_totales=int(I[u]), cuota=float(cuota[u]),
                               percentil=p, n_ref=nref)
        if m in DOS_SALTOS:
            ok = [por_lado[s]["cuota"] >= CUOTA_MIN and por_lado[s]["percentil"] >= PCT_MIN for s in LADOS]
            no = [por_lado[s]["cuota"] < CUOTA_MIN or por_lado[s]["percentil"] < PCT_DESCARTE for s in LADOS]
            v = "CANDIDATO" if all(ok) else ("DESCARTADO" if all(no) else "DUDOSO")
        else:
            n5 = [por_lado[s]["sinapsis"] >= MIN_SIN for s in LADOS]
            v = "PRESENTE" if all(n5) else ("AUSENTE" if not any(n5) else "ASIMETRICO")
        res["mecanismos"][m] = dict(por_lado=por_lado, veredicto=v)
    cpos = (pos / E.replace(0, np.nan)).fillna(0.0)
    pl = {}
    for s in LADOS:
        p, nref = percentil(cpos, lado_de, uo[s], min_i, E)
        pl[s] = dict(sinapsis=int(pos[uo[s]]), excitatorias_totales=int(E[uo[s]]), cuota=float(cpos[uo[s]]),
                     percentil=p, n_ref=nref)
    res["control_positivo"] = dict(por_lado=pl, pasa=bool(all(pl[s]["percentil"] >= PCT_MIN for s in LADOS)))
    vs = [res["mecanismos"][m]["veredicto"] for m in DOS_SALTOS + DIRECTOS]
    if not res["control_positivo"]["pasa"]:
        h = "INVALIDO"
    elif any(v in ("CANDIDATO", "PRESENTE") for v in vs):
        h = "SOSTENIDA"
    elif all(v in ("DESCARTADO", "AUSENTE") for v in vs):
        h = "REFUTADA"
    else:
        h = "SIN_DECIDIR"
    res["H_FRENO"] = h

    nt = dict(zip(a.root_id, a.top_nt)) if "top_nt" in a.columns else {}
    top = {}
    for s in LADOS:
        sub = inh[inh.u.map(lambda t: t == uo[s]).to_numpy(dtype=bool)].copy()
        sub["pt"] = sub.Presynaptic_ID.map(tipo_de).fillna("sin_tipo")
        sub["nt"] = sub.Presynaptic_ID.map(nt).fillna("?")
        res.setdefault("nt_inhibitorio", {})[s] = {k: int(v) for k, v in sub.groupby("nt").Connectivity.sum().items()}
        g = sub.groupby("pt").Connectivity.sum().sort_values(ascending=False).head(10)
        filas = []
        for t, w in g.items():
            xs = set(sub.Presynaptic_ID[sub.pt == t].tolist())
            ent = c[c.Postsynaptic_ID.isin(xs)].copy()
            ent["t"] = ent.Presynaptic_ID.map(tipo_de).fillna("sin_tipo")
            tot = float(ent.Connectivity.sum()) or 1.0
            de = ent.groupby("t").Connectivity.sum().sort_values(ascending=False).head(3)
            filas.append(dict(tipo=t, sinapsis=int(w), neuronas=len(xs),
                              nt=",".join(sorted(set(sub.nt[sub.pt == t].tolist()))),
                              entradas_top3=[[k, round(float(v) / tot, 4)] for k, v in de.items()]))
        top[s] = filas
    res["top_inhibitorias"] = top
    return res


def imprimir(res):
    for m, r in res["mecanismos"].items():
        pr("MECANISMO %s %s -> %s" % (m, " | ".join("%s sin=%d de %d cuota=%.4f pct=%.3f (n=%d)" % (
            s, r["por_lado"][s]["sinapsis"], r["por_lado"][s]["inhibitorias_totales"], r["por_lado"][s]["cuota"],
            r["por_lado"][s]["percentil"], r["por_lado"][s]["n_ref"]) for s in LADOS), r["veredicto"]))
    cp = res["control_positivo"]
    pr("CONTROL_POSITIVO %s -> %s" % (" | ".join("%s sin=%d de %d cuota=%.4f pct=%.3f" % (
        s, cp["por_lado"][s]["sinapsis"], cp["por_lado"][s]["excitatorias_totales"], cp["por_lado"][s]["cuota"],
        cp["por_lado"][s]["percentil"]) for s in LADOS), "PASA" if cp["pasa"] else "FALLA"))
    for s in LADOS:
        pr("NT_INHIBITORIO %s %s" % (s, res.get("nt_inhibitorio", {}).get(s)))
        for f in res["top_inhibitorias"][s]:
            pr("TOP %s %s sin=%d neuronas=%d nt=%s entradas=%s" % (s, f["tipo"], f["sinapsis"], f["neuronas"], f["nt"],
                                                                 f["entradas_top3"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--humo", action="store_true")
    a_ = ap.parse_args()
    os.makedirs(a_.out, exist_ok=True)
    t0 = time.time()
    pr("# maquina: %s | %s | Python %s | numpy %s | pandas %s" % (platform.node(), platform.platform(),
                                                                 platform.python_version(), np.__version__,
                                                                 pd.__version__))
    pr("# md5 instrumento = " + md5(os.path.abspath(__file__)))
    pr("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    mc, ma = md5(a_.conn), md5(a_.annot)
    pr("# md5 conn = %s | md5 annot = %s" % (mc, ma))
    if mc != CONN_MD5 or ma != ANNOT_MD5:
        pr("ABORTA: insumos distintos del pin")
        pr("EXIT_RUN=2")
        return 2
    objetivo = OBJETIVO_HUMO if a_.humo else OBJETIVO
    if a_.humo:
        pr("# HUMO: objetivo %s, no DNp06; estos numeros no valen para H_FRENO" % objetivo)
    a = pd.read_csv(a_.annot, sep=chr(9), dtype=str, usecols=["root_id", "cell_type", "side", "super_class", "top_nt"])
    a["root_id"] = a.root_id.astype(np.int64)
    c = pd.read_parquet(a_.conn, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
    res = calcular(a, c, objetivo)
    if res is None:
        pr("ABORTA: el objetivo %s no tiene unidades descendentes en los dos lados" % objetivo)
        pr("EXIT_RUN=3")
        return 3
    pr("UNIDADES descendentes=%d tamanos_X=%s" % (res["n_unidades"], res["tamanos"]))
    imprimir(res)
    pr("H_FRENO objetivo=%s -> %s%s" % (objetivo, res["H_FRENO"], " (HUMO, sin valor)" if a_.humo else ""))
    res["humo"] = a_.humo
    res["segundos"] = time.time() - t0
    json.dump(res, open(os.path.join(a_.out, "freno.json"), "w"), indent=1, default=str)
    pr("EXIT_RUN=0 | %.1f s" % (time.time() - t0))
    return 0 if res["H_FRENO"] != "INVALIDO" else 3


if __name__ == "__main__":
    sys.exit(main())
