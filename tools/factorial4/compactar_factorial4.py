#!/usr/bin/env python3
"""Compacta la salida del factorial 4 para git y mide, post-hoc, cuanto se parecen CE y R2 ensayo por ensayo
(respuesta 2026-10-14-001). No decide nada: el veredicto es el de agregar_factorial4.py (sellado en 431b7bd).

Uso: python3 compactar_factorial4.py <carpeta del factorial 4> <carpeta del factorial 3> <destino>
Escribe en <destino>:
  corridas.csv  celda, tau, prueba, W_CE, W_R2, regla_propia, regla40 (las 600 corridas pareadas)
  nulos.csv     tipo, k, acierto (los 100 barajados del cerebro entero)
  MD5SUMS.txt   md5 de todo lo bajado de Kaggle (sin el agregado.log, que es nuestro)
Imprime las medias recalculadas con pandas (otro camino que el cubo de numpy del agregador) y la coincidencia ensayo a
ensayo entre las predicciones de CE y de R2.
"""
import glob
import hashlib
import json
import os
import sys

import pandas as pd


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def leer(patron, d, col):
    filas, preds = [], {}
    for p in sorted(glob.glob(os.path.join(d, "**", patron), recursive=True)):
        r = json.load(open(p))
        for x in r["corridas"]:
            k = (x["celda"], x["tau"], x["prueba"])
            filas.append({"celda": x["celda"], "tau": x["tau"], "prueba": x["prueba"], col: x["W"],
                          "regla_" + col: x["regla_propia"], "regla40_" + col: x["regla40"]})
            preds[k] = x["pred_W"]
    return pd.DataFrame(filas), preds


def main():
    d4, d3, dest = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(dest, exist_ok=True)
    c4, p4 = leer("factorial4_CE_CON_TASA_*.json", d4, "W_CE")
    c3, p3 = leer("factorial2_R2_CON_TASA_*.json", d3, "W_R2")
    m = c4.merge(c3, on=["celda", "tau", "prueba"], how="inner").sort_values(["celda", "tau", "prueba"])
    print("CORRIDAS CE=%d R2=%d pareadas=%d" % (len(c4), len(c3), len(m)))
    print("REGLA igual en CE y R2: %d de %d corridas" % (int((m.regla_W_CE == m.regla_W_R2).sum()), len(m)))
    print("MEDIAS (pandas) W_CE=%.4f regla=%.4f W_R2=%.4f | CE-regla=%+.4f | CE-R2=%+.5f" % (
        m.W_CE.mean(), m.regla_W_CE.mean(), m.W_R2.mean(), (m.W_CE - m.regla_W_CE).mean(), (m.W_CE - m.W_R2).mean()))
    d = (m.W_CE - m.W_R2).abs()
    print("DIFERENCIA CE-R2 por corrida: max=%.4f | en ensayos (de 2000): max=%d | corridas con |dif|<=0.001: %d" % (
        d.max(), int(round(d.max() * 2000)), int((d <= 0.001 + 1e-12).sum())))
    tot = igual = ident = 0
    for k, a in p4.items():
        b = p3[k]
        tot += len(a)
        igual += sum(1 for u, v in zip(a, b) if u == v)
        ident += a == b
    print("ENSAYOS con la misma prediccion en CE y R2: %d de %d (%.3f %%)" % (igual, tot, 100.0 * igual / tot))
    print("CORRIDAS con las 2000 predicciones identicas: %d de %d" % (ident, len(p4)))
    out = m.rename(columns={"regla_W_CE": "regla_propia", "regla40_W_CE": "regla40"})
    out[["celda", "tau", "prueba", "W_CE", "W_R2", "regla_propia", "regla40"]].to_csv(
        os.path.join(dest, "corridas.csv"), index=False)
    nl = []
    for p in sorted(glob.glob(os.path.join(d4, "**", "nulos_CE_*.json"), recursive=True)):
        r = json.load(open(p))
        for x in r["nulos"]:
            nl.append({"tipo": r["tipo"], "k": x["k"], "acierto": x["acierto"]})
    n = pd.DataFrame(nl).sort_values(["tipo", "k"])
    n.to_csv(os.path.join(dest, "nulos.csv"), index=False)
    print("NULOS %s" % " ".join("%s n=%d media=%.4f max=%.4f" % (t, len(g), g.acierto.mean(), g.acierto.max())
                                for t, g in n.groupby("tipo")))
    k = 0
    with open(os.path.join(dest, "MD5SUMS.txt"), "w") as f:
        for p in sorted(glob.glob(os.path.join(d4, "**", "*"), recursive=True)):
            if os.path.isfile(p) and os.path.basename(p) != "agregado.log":
                f.write("%s  %s\n" % (md5(p), os.path.relpath(p, d4)))
                k += 1
    print("MD5SUMS archivos=%d" % k)
    for a in ("corridas.csv", "nulos.csv", "MD5SUMS.txt"):
        print("escrito %s md5=%s bytes=%d" % (a, md5(os.path.join(dest, a)), os.path.getsize(os.path.join(dest, a))))


if __name__ == "__main__":
    main()
