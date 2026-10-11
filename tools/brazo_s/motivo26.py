#!/usr/bin/env python3
"""Reconstruye el motivo de escape de 26 neuronas del brazo W desde el parquet pinneado.

Por que existe: el brazo S corregido (brazo_s_recurrente.py) tiene que medir EXACTAMENTE el mismo
sujeto que el brazo W del 23-ago (kernel Kaggle abrahammendieta/titan-brazo-w) y su re-corrida del
2-oct en brain-env (/workspace/wrun/brazo_w.py, md5 ebf757df2d925420faa43082ad9d30c3). Por eso la
seleccion de neuronas y la matriz se copian verbatim de brazo_w.py y el resultado se compara contra
la matriz normalizada que ese run guardo en brazo_w.json (E-01: mismo sujeto, no uno parecido).

Seleccion (verbatim de brazo_w.py): 8 LC4 + 8 LPLC2 + 4 LC6 + 2 GF + 4 DNp09 = 26, dentro de cada
tipo las de mayor grado total en el subgrafo del motivo completo; empate por root_id.
Peso de cada arista: columna 'Excitatory x Connectivity' del parquet (sinapsis con signo de Dale).
Convencion: M[j, i] = peso de la neurona i hacia la neurona j.

Uso:
  python3 motivo26.py --parquet connectivity.parquet --annot annotations.tsv \
      --brazo-w-json brazo_w.json --out motivo26.json

Codigos de salida: 0 todo verificado; 2 un md5 de entrada no coincide con el pin, o la matriz no
coincide con la del brazo W (entonces el sujeto seria otro y el experimento no vale).
"""
import argparse
import hashlib
import json
import sys

import numpy as np
import pandas as pd

MD5P_OK = "3d802fd542b5d18570ba1ba0bb0abed9"
MD5A_OK = "719904abad876c68ace1b5690c9b9b63"
ASHA = "17fc57722002e1a7d38cdd0c89ac382bf92718da"
GRUPOS = [
    ("LC4", ["LC4"], 8),
    ("LPLC2", ["LPLC2"], 8),
    ("LC6", ["LC6"], 4),
    ("GF", ["GF", "DNp01"], 2),
    ("DNp09", ["DNp09"], 4),
]


def md5(path):
    """md5 de un archivo leido en bloques de 1 MiB."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    """Reconstruye, verifica y escribe el motivo. Devuelve el codigo de salida."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--parquet", required=True)
    ap.add_argument("--annot", required=True)
    ap.add_argument("--brazo-w-json", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    falla = []
    m_p, m_a = md5(a.parquet), md5(a.annot)
    print("parquet md5=" + m_p + "  pin=" + MD5P_OK + "  " + ("OK" if m_p == MD5P_OK else "DISTINTO"))
    print("annot   md5=" + m_a + "  pin=" + MD5A_OK + "  " + ("OK" if m_a == MD5A_OK else "DISTINTO"))
    if m_p != MD5P_OK:
        falla.append("md5_parquet")
    if m_a != MD5A_OK:
        falla.append("md5_annot")

    an = pd.read_csv(a.annot, sep="\t", low_memory=False)
    an["cell_type"] = an["cell_type"].astype(str)
    an["hemibrain_type"] = an["hemibrain_type"].astype(str)

    def pick_type(pats):
        m = pd.Series(False, index=an.index)
        for p in pats:
            m = m | an["cell_type"].str.fullmatch(p, na=False)
            m = m | an["hemibrain_type"].str.fullmatch(p, na=False)
        r = pd.to_numeric(an.loc[m, "root_id"], errors="coerce").dropna()
        return set(int(x) for x in r.tolist())

    ids_por_grupo = {}
    for nom, pats, cupo in GRUPOS:
        s = pick_type(pats)
        ids_por_grupo[nom] = s
        print("tipo " + nom.ljust(6) + " halladas=" + str(len(s)) + " cupo=" + str(cupo))
        if len(s) < cupo:
            print("ABORTA: el tipo " + nom + " no llega al cupo")
            return 2

    df = pd.read_parquet(a.parquet, columns=["Presynaptic_ID", "Postsynaptic_ID", "Excitatory x Connectivity"])
    df.columns = ["pre", "post", "w"]
    print("aristas totales=" + str(len(df)))
    todos = set()
    for nom, _, _ in GRUPOS:
        todos |= ids_por_grupo[nom]
    sub = df[df["pre"].isin(todos) & df["post"].isin(todos)]
    print("aristas dentro del motivo completo=" + str(len(sub)))

    gr = {}
    for pre, post in zip(sub["pre"].values, sub["post"].values):
        gr[pre] = gr.get(pre, 0) + 1
        gr[post] = gr.get(post, 0) + 1

    sel, reparto, tipos = [], {}, []
    for nom, _, cupo in GRUPOS:
        cand = sorted(ids_por_grupo[nom], key=lambda r: (-gr.get(r, 0), r))[:cupo]
        reparto[nom] = [int(x) for x in cand]
        sel.extend(cand)
        tipos.extend([nom] * len(cand))
        print(nom.ljust(6) + " elegidas=" + str(len(cand)) + " grados=" + str([gr.get(c, 0) for c in cand]))
    if len(sel) != 26:
        print("ABORTA: seleccionadas " + str(len(sel)))
        return 2
    idx = {int(r): i for i, r in enumerate(sel)}

    M = np.zeros((26, 26), dtype=np.float64)
    sub2 = sub[sub["pre"].isin(list(idx.keys())) & sub["post"].isin(list(idx.keys()))]
    for pre, post, w in zip(sub2["pre"].values, sub2["post"].values, sub2["w"].values):
        i, j = idx[int(pre)], idx[int(post)]
        if i == j:
            continue
        M[j, i] += float(w)
    edges = [(i, j) for i in range(26) for j in range(26) if i != j and M[j, i] != 0.0]
    nE = len(edges)
    recip = sum(1 for (i, j) in edges if M[i, j] != 0.0)
    r = float(np.max(np.abs(np.linalg.eigvals(M))))
    Mn = M * (0.9 / r)
    n_neg = int(sum(1 for (i, j) in edges if M[j, i] < 0))
    print("matriz real: aristas=" + str(nE) + " densidad=" + format(nE / 650.0, ".4f")
          + " reciprocas=" + str(recip) + " inhibitorias=" + str(n_neg) + " radio_crudo=" + format(r, ".4f"))

    ref = json.load(open(a.brazo_w_json))
    Wj = np.array(ref["mascara"]["W"], dtype=np.float64)
    diff = float(np.max(np.abs(Mn - Wj)))
    rep_ok = all(reparto[k] == [int(x) for x in ref["mascara"]["reparto"][k]] for k in reparto)
    print("verificacion contra brazo_w.json: max|W_reconstruida - W_brazo_w|=" + format(diff, ".3e")
          + " reparto_igual=" + str(rep_ok))
    if diff > 1e-12 or not rep_ok:
        falla.append("no_coincide_con_brazo_w")

    out = {
        "fuente": {"md5_parquet": m_p, "md5_annot": m_a, "annot_sha": ASHA,
                   "columna_peso": "Excitatory x Connectivity",
                   "seleccion": "verbatim de brazo_w.py (titan-brazo-w, 23-ago; brain-env 2-oct)",
                   "md5_brazo_w_json": md5(a.brazo_w_json)},
        "orden_root_ids": [int(x) for x in sel],
        "tipos": tipos,
        "reparto": reparto,
        "M_cruda": M.tolist(),
        "aristas": [list(e) for e in edges],
        "n_aristas": nE,
        "densidad": nE / 650.0,
        "reciprocas": recip,
        "inhibitorias": n_neg,
        "radio_crudo": r,
        "verificacion_brazo_w": {"max_abs_diff_W_normalizada": diff, "reparto_igual": rep_ok},
        "fallas": falla,
    }
    with open(a.out, "w") as f:
        json.dump(out, f)
    print("escrito " + a.out + " md5=" + md5(a.out))
    print("VEREDICTO_MOTIVO=" + ("OK" if not falla else "FALLA " + ",".join(falla)))
    return 0 if not falla else 2


if __name__ == "__main__":
    sys.exit(main())
