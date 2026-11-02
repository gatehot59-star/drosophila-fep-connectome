#!/usr/bin/env python3
"""Conjuntos S, X y D de las intervenciones de la respuesta 2026-11-02-002, sacados del censo del Paso 1
(tools/mecanismo/paso12.py, con tools/reuso/reuso_mosca.py en el blob 37b35835).

Para cada estimulo (tipo y lado de S, en LC4, LPLC2, LPLC1 y LPLC4): S son las neuronas de la unidad; D, las
neuronas de las unidades descendentes con las que forma plantilla (S->D >= 20 sinapsis directas y al menos una X);
X, las inhibitorias que cierran alguna de esas plantillas (>= 5 sinapsis S->X y >= 5 X->D), con su neurotransmisor
predicho. Ademas, todas las descendentes con su tipo, para la lectura fuera del objetivo.
Uso: python3 conjuntos.py --dir DIR --out conjuntos_flywire.json
"""
import argparse
import hashlib
import json

import numpy as np
import pandas as pd

ESTIMULOS = ("LC4", "LPLC2", "LPLC1", "LPLC4")
LADOS = ("right", "left")


def sha256(ruta):
    """sha256 de un archivo."""
    return hashlib.sha256(open(ruta, "rb").read()).hexdigest()


def main():
    """Lee el censo del Paso 1 y escribe el JSON de conjuntos, con una linea de log por estimulo."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="carpeta con flywire_closing_paths.parquet y flywire_units.*")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rp = a.dir + "/flywire_closing_paths.parquet"
    rz = a.dir + "/flywire_units.npz"
    rj = a.dir + "/flywire_units.json"
    p = pd.read_parquet(rp)
    z = np.load(rz)
    u = json.load(open(rj))
    cs = [tuple(x) for x in u["cs"]]
    cd = [tuple(x) for x in u["cd"]]
    root, S, D, inh, tipo = z["root"], z["S"], z["D"], z["inh"], z["tipo"]
    dn = np.flatnonzero(D >= 0)
    out = {"version": "2026-11-02-002",
           "descendentes": {"root": [int(root[i]) for i in dn], "tipo": [cd[D[i]][0] for i in dn],
                            "lado": [cd[D[i]][1] for i in dn]},
           "estimulos": {}}
    for ty in ESTIMULOS:
        for lado in LADOS:
            s = cs.index((ty, lado))
            q = p[p.s == s]
            du = sorted(set(int(v) for v in q.dd))
            xs = sorted(set(int(v) for v in q.x))
            nt = q.drop_duplicates("x").set_index("x").x_nt
            sn = np.flatnonzero(S == s)
            dneu = np.flatnonzero(np.isin(D, du))
            if not all(bool(inh[x]) for x in xs):
                raise SystemExit("ABORTA: hay X no inhibitoria en %s_%s" % (ty, lado))
            if set(xs) & (set(sn.tolist()) | set(dneu.tolist())):
                raise SystemExit("ABORTA: X se superpone con S o D en %s_%s" % (ty, lado))
            out["estimulos"]["%s_%s" % (ty, lado)] = {
                "S": [int(root[i]) for i in sn], "D": [int(root[i]) for i in dneu],
                "D_tipo": [cd[D[i]][0] for i in dneu], "X": [int(root[x]) for x in xs],
                "X_nt": [str(nt[x]) for x in xs], "X_tipo": [str(tipo[x]) for x in xs],
                "unidades_D": len(du), "caminos": int(len(q))}
            print("ESTIMULO %s_%s S=%d D=%d unidades_D=%d X=%d X_glu=%d caminos=%d" % (
                ty, lado, len(sn), len(dneu), len(du), len(xs), sum(1 for x in xs if nt[x] == "glutamate"), len(q)),
                flush=True)
    txt = json.dumps(out, sort_keys=True)
    with open(a.out, "w") as f:
        f.write(txt)
    print("FUENTES closing=%s npz=%s units=%s" % (sha256(rp), sha256(rz), sha256(rj)), flush=True)
    print("JSON %s bytes=%d sha256=%s" % (a.out, len(txt.encode()), hashlib.sha256(txt.encode()).hexdigest()), flush=True)


if __name__ == "__main__":
    main()
