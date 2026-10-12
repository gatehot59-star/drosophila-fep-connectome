#!/usr/bin/env python3
"""Catalogo de circuitos candidatos en FlyWire v783 (respuesta 2026-10-12-002).

Para cada circuito de la respuesta 2026-10-12-001 busca los tipos celulares en
las anotaciones pinneadas (flyconnectome/flywire_annotations 17fc577), mide
tamano por lado, cableado interno (aristas >= 5 sinapsis), signo, lateralidad,
costo en bytes en el formato de swarm/ (6 B por arista y 2 B por neurona), las
entradas principales de sus neuronas de salida y sus salidas a descendentes, y
contrasta predicciones de literatura que pueden dar rojo.

Controles del instrumento (si alguno falla: INVALIDO, exit 3):
  C+  LC4 -> DNp01 tiene aristas >= 5 (positivo; ficha GF-01).
  C-  LC6 -> DNp01 no tiene aristas >= 5 (negativo; LC6->GF = 0 de la ficha GF-01).

Salida: 0 corrida completa; 2 md5 de datos distinto del pin; 3 instrumento invalido.
Uso: python3 catalogo_circuitos.py --conn connectivity.parquet --annot annotations.tsv --out DIR
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

MD5_CONN = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5_ANNOT = "719904abad876c68ace1b5690c9b9b63"
UMBRAL = 5
TOP = 5

VS = "|".join("VS%d" % i for i in range(1, 9))
LC10 = "LC10a|LC10b|LC10c-1|LC10c-2|LC10d|LC10e|LC10f"

# Definiciones fijadas antes de la corrida. Los nombres se buscaron antes en las
# anotaciones (oDN1, BDN2 y LPLC3 no estan con ese nombre en v783).
CIRCUITOS = [
    dict(nombre="escape", entrada="LC4|LPLC2|LC6", salida="DNp01|DNp09",
         fuente="medido en este repo (010 a 015) y ficha GF-01"),
    dict(nombre="aterrizaje", entrada="LPLC4|LC4|LPLC2", salida="DNp07|DNp10",
         fuente="Ache 2019 Nat Neurosci: DNp07 y DNp10; dendritas sobre glomerulos de LPLC3 y LPLC4"),
    dict(nombre="giro", entrada="", salida="DNa01|DNa02|DNg13|DNb02",
         fuente="Yang 2024 via Eon (DNa01, DNa02); Simpson 2023 (DNa02, DNg13); Braun 2024 (DNb02)"),
    dict(nombre="marcha", entrada="", salida="DNp09|MDN|oDN1|BDN2",
         fuente="Simpson 2023 (DNp09, MDN, oDN1); Sapkal 2024 (oDN1, BDN2)"),
    dict(nombre="vuelo_flujo", entrada="HSE|HSN|HSS|H1|H2|" + VS, salida="DNp15|DNp06|DNg02*",
         fuente="Simpson 2023 (DNp15 = DNHS1, DNp06 vuelo recto, DNg02 direccion en vuelo); HS/VS de memoria"),
    dict(nombre="rumbo", entrada="EPG|EPGt", salida="PEN_a(PEN1)|PEN_b(PEN2)",
         fuente="anillo E-PG / P-EN del complejo central, de memoria"),
    dict(nombre="objetos_chicos", entrada="LC11|" + LC10, salida="",
         fuente="LC11 y LC10 de memoria"),
    dict(nombre="olfato", entrada="class:olfactory|class:ALPN",
         salida="class:Kenyon_Cell|class:LHLN|class:LHCENT|class:MBON",
         fuente="via olfativa clasica, de memoria"),
]

# (id, pre, post, condicion, fuente). condicion: ">0", ">0exc" o "==0".
PREDICCIONES = [
    ("C+", "LC4", "DNp01", ">0", "control positivo (ficha GF-01)"),
    ("C-", "LC6", "DNp01", "==0", "control negativo (ficha GF-01)"),
    ("E2", "LPLC2", "DNp01", ">0", "LPLC2 -> GF (literatura y GF-01)"),
    ("A1", "LPLC4", "DNp07|DNp10", ">0", "Ache 2019 (solapamiento de dendritas)"),
    ("M1", "DNp09", "DNa02", ">0exc", "Braun 2024 (excitatoria directa)"),
    ("M2", "MDN", "DNa01", ">0", "Braun 2024"),
    ("R1", "EPG|EPGt", "PEN_a(PEN1)|PEN_b(PEN2)", ">0", "anillo de rumbo, de memoria"),
    ("R2", "PEN_a(PEN1)|PEN_b(PEN2)", "EPG|EPGt", ">0", "anillo de rumbo, de memoria"),
    ("F1", "HSE|HSN|HSS", "DNp15", ">0", "nombre DNHS1 (Simpson 2023)"),
    ("O1", "class:olfactory", "class:ALPN", ">0", "via olfativa"),
    ("O2", "class:ALPN", "class:Kenyon_Cell", ">0", "via olfativa"),
    ("O3", "class:ALPN", "class:LHLN|class:LHCENT", ">0", "via olfativa"),
]


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Conectoma:
    def __init__(self, conn, annot):
        a = pd.read_csv(annot, sep="\t", dtype=str,
                        usecols=["root_id", "cell_type", "cell_class", "super_class", "side"])
        a = a.drop_duplicates("root_id")
        rid = a["root_id"].astype(np.int64).to_numpy()
        o = np.argsort(rid)
        self.rid = rid[o]
        def col(n):
            return np.append(a[n].fillna("").to_numpy()[o], "")  # centinela en -1
        self.ct, self.cc, self.sc, self.side = col("cell_type"), col("cell_class"), col("super_class"), col("side")
        c = pd.read_parquet(conn, columns=["Presynaptic_ID", "Postsynaptic_ID", "Connectivity", "Excitatory"])
        self.ipre = self._idx(c["Presynaptic_ID"].to_numpy(np.int64))
        self.ipost = self._idx(c["Postsynaptic_ID"].to_numpy(np.int64))
        self.w = c["Connectivity"].to_numpy(np.int32)
        self.sg = c["Excitatory"].to_numpy(np.int8)
        del c
        self.n_aristas = len(self.w)
        self.sin_anot = int((self.ipre == -1).sum() + (self.ipost == -1).sum())

    def _idx(self, x):
        p = np.searchsorted(self.rid, x)
        p = np.clip(p, 0, len(self.rid) - 1)
        ok = self.rid[p] == x
        p = p.astype(np.int32)
        p[~ok] = -1
        return p

    def sel(self, spec):
        m = np.zeros(len(self.ct), dtype=bool)
        if not spec:
            return m
        for alt in spec.split("|"):
            if alt.startswith("class:"):
                m |= self.cc == alt[6:]
            elif alt.endswith("*"):
                m |= np.char.startswith(self.ct.astype(str), alt[:-1])
            else:
                m |= self.ct == alt
        m[-1] = False
        return m


def lados(cx, m):
    s = cx.side[m]
    return {k: int((s == k).sum()) for k in ("left", "right", "center")}


def flujo(cx, mpre, mpost, umbral):
    e = mpre[cx.ipre] & mpost[cx.ipost] & (cx.w >= umbral)
    w = cx.w[e].astype(np.int64)
    sinap = int(w.sum())
    exc = int(w[cx.sg[e] > 0].sum())
    return e, int(e.sum()), sinap, (exc / sinap if sinap else None)


def frac_ipsi(cx, e):
    sp, so = cx.side[cx.ipre[e]], cx.side[cx.ipost[e]]
    w = cx.w[e].astype(np.int64)
    ok = np.isin(sp, ["left", "right"]) & np.isin(so, ["left", "right"])
    tot = int(w[ok].sum())
    return (int(w[ok & (sp == so)].sum()) / tot) if tot else None


def top_tipos(cx, e, lado, n=TOP):
    idx = cx.ipre[e] if lado == "pre" else cx.ipost[e]
    df = pd.DataFrame({"t": cx.ct[idx], "w": cx.w[e].astype(np.int64)})
    df["t"] = df["t"].replace("", "(sin tipo)")
    g = df.groupby("t")["w"].sum().sort_values(ascending=False)
    tot = int(g.sum())
    return [(k, int(v), (v / tot if tot else 0.0)) for k, v in g.head(n).items()], tot


def f(x):
    return "NA" if x is None else "%.4f" % x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conn", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sin-pin", action="store_true", help="solo para prueba sintetica; queda escrito en el log")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    print("# maquina: %s | %s | Python %s | numpy %s | pandas %s" % (
        platform.node(), platform.platform(), platform.python_version(), np.__version__, pd.__version__))
    print("# md5 script = " + md5(os.path.abspath(__file__)))
    print("# fecha: " + time.strftime("%Y-%m-%d %H:%M:%S %z"))
    mc, ma = md5(a.conn), md5(a.annot)
    print("# md5 conn = %s (pin %s) | md5 annot = %s (pin %s)" % (mc, MD5_CONN, ma, MD5_ANNOT))
    if a.sin_pin:
        print("# PIN OMITIDO (prueba sintetica): estos numeros no valen")
    elif mc != MD5_CONN or ma != MD5_ANNOT:
        print("ABORTA: datos distintos del pin")
        print("EXIT_RUN=2")
        return 2
    cx = Conectoma(a.conn, a.annot)
    print("DATOS aristas=%d neuronas_anotadas=%d extremos_sin_anotacion=%d umbral=%d" % (
        cx.n_aristas, len(cx.rid), cx.sin_anot, UMBRAL))
    desc = (cx.sc == "descending")
    res = {"circuitos": {}, "predicciones": {}, "umbral": UMBRAL}

    for C in CIRCUITOS:
        nom = C["nombre"]
        r = {"fuente": C["fuente"], "tipos": {}}
        print("CIRCUITO %s | fuente: %s" % (nom, C["fuente"]))
        for parte in ("entrada", "salida"):
            for alt in [x for x in C[parte].split("|") if x]:
                m = cx.sel(alt)
                n = int(m.sum())
                lg = lados(cx, m)
                r["tipos"][alt] = {"parte": parte, "n": n, **lg}
                print("TIPO circuito=%s parte=%s tipo=%s n=%d izq=%d der=%d centro=%d%s" % (
                    nom, parte, alt, n, lg["left"], lg["right"], lg["center"],
                    "" if n else " -> NO_ENCONTRADO"))
        me, ms = cx.sel(C["entrada"]), cx.sel(C["salida"])
        mS = me | ms
        e, na, sn, fe = flujo(cx, mS, mS, UMBRAL)
        nn = int(mS.sum())
        fi = frac_ipsi(cx, e)
        r.update(neuronas=nn, aristas5=na, sinapsis5=sn, frac_exc=fe, frac_ipsi=fi, bytes=6 * na + 2 * nn)
        print("INTERNO circuito=%s neuronas=%d aristas5=%d sinapsis5=%d frac_exc=%s frac_ipsi=%s bytes_formato_swarm=%d" % (
            nom, nn, na, sn, f(fe), f(fi), 6 * na + 2 * nn))
        if ms.any():
            todos = np.ones(len(cx.ct), dtype=bool)
            todos[-1] = False
            e2, _, sn2, fe2 = flujo(cx, todos, ms, UMBRAL)
            tp, tot = top_tipos(cx, e2, "pre")
            r["entradas_de_salida"] = {"sinapsis5": sn2, "frac_exc": fe2, "frac_ipsi": frac_ipsi(cx, e2),
                                       "top": tp}
            print("ENTRADA_A_SALIDA circuito=%s sinapsis5=%d frac_exc=%s frac_ipsi=%s" % (
                nom, sn2, f(fe2), f(frac_ipsi(cx, e2))))
            for k, (t, v, fr) in enumerate(tp, 1):
                print("  top%d entrada=%s sinapsis=%d frac=%.4f" % (k, t, v, fr))
        if me.any():
            todos = np.ones(len(cx.ct), dtype=bool)
            todos[-1] = False
            e3, _, sn3, _ = flujo(cx, me, todos, UMBRAL)
            e4, _, sn4, _ = flujo(cx, me, desc, UMBRAL)
            tpd, _ = top_tipos(cx, e4, "post")
            tpa, _ = top_tipos(cx, e3, "post")
            r["salidas_de_entrada"] = {"sinapsis5": sn3, "a_descendentes": sn4,
                                       "frac_a_descendentes": (sn4 / sn3 if sn3 else None),
                                       "top_descendentes": tpd, "top_todos": tpa}
            print("SALIDA_DE_ENTRADA circuito=%s sinapsis5=%d a_descendentes=%d frac=%s" % (
                nom, sn3, sn4, f(sn4 / sn3 if sn3 else None)))
            for k, (t, v, fr) in enumerate(tpd, 1):
                print("  top%d descendente=%s sinapsis=%d frac_de_lo_que_va_a_DN=%.4f" % (k, t, v, fr))
            for k, (t, v, fr) in enumerate(tpa, 1):
                print("  top%d destino=%s sinapsis=%d frac=%.4f" % (k, t, v, fr))
        res["circuitos"][nom] = r

    conf, n_lit = 0, 0
    estado = {}
    for pid, pre, post, cond, fuente in PREDICCIONES:
        mp, mq = cx.sel(pre), cx.sel(post)
        e5, a5, s5, fe5 = flujo(cx, mp, mq, UMBRAL)
        e1, a1, s1, _ = flujo(cx, mp, mq, 1)
        if cond == "==0":
            ok = a5 == 0
        elif cond == ">0exc":
            ok = a5 > 0 and fe5 is not None and fe5 > 0.5
        else:
            ok = a5 > 0
        v = ("PASS" if ok else "FAIL") if pid.startswith("C") else ("CONFIRMA" if ok else "NO_CONFIRMA")
        if not pid.startswith("C"):
            n_lit += 1
            conf += int(ok)
        estado[pid] = ok
        res["predicciones"][pid] = dict(pre=pre, post=post, cond=cond, fuente=fuente, aristas5=a5,
                                        sinapsis5=s5, frac_exc5=fe5, aristas1=a1, sinapsis1=s1, veredicto=v)
        print("PRED %s pre=%s post=%s cond=%s aristas5=%d sinapsis5=%d frac_exc5=%s aristas1=%d sinapsis1=%d -> %s | %s" % (
            pid, pre, post, cond, a5, s5, f(fe5), a1, s1, v, fuente))
    valido = estado["C+"] and estado["C-"]
    print("CHEQUEO INSTRUMENTO C+=%s C-=%s -> %s" % (
        "PASS" if estado["C+"] else "FAIL", "PASS" if estado["C-"] else "FAIL", "VALIDO" if valido else "INVALIDO"))
    print("RESUMEN predicciones_de_literatura confirmadas=%d de %d" % (conf, n_lit))
    res["valido"] = valido
    res["confirmadas"] = [conf, n_lit]
    with open(os.path.join(a.out, "resultados.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True, default=str)
    print("escrito resultados.json md5=" + md5(os.path.join(a.out, "resultados.json")))
    print("# duracion_s=%.1f" % (time.time() - t0))
    rc = 0 if valido else 3
    print("EXIT_RUN=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
