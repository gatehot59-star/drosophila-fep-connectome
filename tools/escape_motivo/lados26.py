#!/usr/bin/env python3
"""Lado (hemisferio) de cada una de las 26 neuronas del motivo de escape, desde las anotaciones pinneadas.

Por que existe: escape_motivo.py tiene que darle a cada neurona visual la entrada de SU ojo y leer el
GF de cada lado. El lado sale de la columna 'side' de las anotaciones de FlyWire (commit 17fc577,
md5 719904ab...), que es independiente de las aristas del parquet. Ademas cuenta cuantas aristas del
motivo cruzan de hemisferio: si son cero, el motivo son dos mitades ipsilaterales separadas.

Uso:
  python3 lados26.py --annot annotations.tsv --motivo ../brazo_s/motivo26.json --out lados26.json

Codigos de salida: 0 todo verificado; 2 md5 distinto del pin, una neurona sin anotar o con lado que
no es left/right, o el orden de root_ids no coincide con el del motivo.
"""
import argparse
import hashlib
import json
import sys

import pandas as pd

MD5A_OK = "719904abad876c68ace1b5690c9b9b63"


def md5(path):
    """md5 de un archivo leido en bloques de 1 MiB."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    """Lee las anotaciones, asigna lado a las 26 y escribe el JSON. Devuelve el codigo de salida."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--annot", required=True)
    ap.add_argument("--motivo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    falla = []
    m_a = md5(a.annot)
    print("annot md5=" + m_a + "  pin=" + MD5A_OK + "  " + ("OK" if m_a == MD5A_OK else "DISTINTO"))
    if m_a != MD5A_OK:
        falla.append("md5_annot")
    mot = json.load(open(a.motivo))
    ids = [int(x) for x in mot["orden_root_ids"]]
    tipos = mot["tipos"]
    an = pd.read_csv(a.annot, sep="\t", low_memory=False)
    an["root_id"] = pd.to_numeric(an["root_id"], errors="coerce")
    sub = an[an["root_id"].isin(ids)].drop_duplicates("root_id").set_index("root_id")

    filas = []
    for k, r in enumerate(ids):
        if r not in sub.index:
            falla.append("sin_anotar_" + str(k))
            continue
        s = sub.loc[r]
        fila = {"indice": k, "root_id": int(r), "tipo_motivo": tipos[k], "cell_type": str(s["cell_type"]),
                "hemibrain_type": str(s["hemibrain_type"]), "side": str(s["side"]),
                "super_class": str(s["super_class"]), "top_nt": str(s["top_nt"])}
        if fila["side"] not in ("left", "right"):
            falla.append("lado_raro_" + str(k))
        filas.append(fila)
        print("neurona " + str(k).rjust(2) + " " + tipos[k].ljust(6) + " " + fila["cell_type"].ljust(6)
              + " lado=" + fila["side"].ljust(5) + " nt=" + fila["top_nt"] + " root_id=" + str(r))
    if len(filas) != 26 or [f["root_id"] for f in filas] != ids:
        falla.append("orden_distinto")

    conteo = {}
    for f in filas:
        clave = f["tipo_motivo"] + "_" + f["side"]
        conteo[clave] = conteo.get(clave, 0) + 1
    lado = [f["side"] for f in filas]
    cruzadas = [list(e) for e in mot["aristas"] if len(lado) == 26 and lado[e[0]] != lado[e[1]]]
    print("conteo por tipo y lado=" + json.dumps(conteo, sort_keys=True))
    print("aristas del motivo=" + str(len(mot["aristas"])) + " ipsilaterales="
          + str(len(mot["aristas"]) - len(cruzadas)) + " cruzadas=" + str(len(cruzadas)))

    out = {"fuente": {"md5_annot": m_a, "annot_sha": "17fc57722002e1a7d38cdd0c89ac382bf92718da",
                      "md5_motivo": md5(a.motivo), "columna": "side"},
           "neuronas": filas, "conteo": conteo, "aristas_cruzadas": cruzadas, "fallas": falla}
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    print("escrito " + a.out + " md5=" + md5(a.out))
    print("VEREDICTO_LADOS=" + ("OK" if not falla else "FALLA " + ",".join(falla)))
    return 0 if not falla else 2


if __name__ == "__main__":
    sys.exit(main())
