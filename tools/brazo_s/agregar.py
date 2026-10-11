#!/usr/bin/env python3
"""Agrega las celdas del brazo S recurrente y emite el veredicto con las reglas escritas ANTES de correr.

Entrada: un directorio con celda_<tarea>_<brazo>.json (salida de brazo_s_recurrente.py) y la referencia
del brazo W (semillas crudas del 2-oct, brain-env). Salida: el log de veredicto por stdout (el workflow
lo guarda como run.log) y un JSON con todos los numeros.

Pruebas por contraste y tarea, las tres siempre impresas:
  p_welch   t de Welch con grados de libertad de Satterthwaite (scipy). Es la que DECIDE.
  p_normal  la aproximacion normal que usaba brazo_w.py (erfc), solo para comparar con agosto.
  p_perm    permutacion exacta de la diferencia de medias (todas las particiones 10 contra 10).
Ademas Holm dentro de cada contraste, sobre las 4 tareas.

Reglas (declaradas antes de ver un solo numero de esta corrida):
  C1 RW contra RB: si RW no le gana a RB (media menor y p_welch <= 0.05) en al menos 3 de 4 tareas,
     la analogia del 96% fijo se retira TAMBIEN en el sustrato recurrente.
  C2 RW contra RS (EL BRAZO S) y C3 LW contra LS:
     gana en >= 3/4  -> LA MOSCA PAGA
     empata en >= 3/4 (p_welch > 0.05) -> PAGA LA SPARSITY, NO LA MOSCA
     pierde en >= 3/4 -> EL CABLEADO REAL RINDE PEOR QUE SU SHUFFLE
     si no -> MIXTO
  C6 A contra F: la neurona liquida es necesaria en la memoria si A le gana a F en >= 3/4;
     si no le gana en >= 3/4 (empata o pierde), NO ES NECESARIA en esta arquitectura y estas tareas.
  C4, C5, C7, C8: informativos, sin regla de decision.

Codigos de salida: 0 siempre que pudo escribir el veredicto (aunque falten celdas: se declaran NO MEDIDO).
"""
import argparse
import glob
import itertools
import json
import math
import os
import sys

import numpy as np
from scipy import stats

TAREAS = ["Gated", "LinScale", "MultiCue", "CR"]
BRAZOS = ["A", "B", "RB", "RW", "RS", "LB", "LW", "LS", "F"]
CONTRASTES = [
    ("C1", "RW", "RB", "conectoma congelado recurrente contra ruido congelado recurrente", "aborto"),
    ("C2", "RW", "RS", "EL BRAZO S: conectoma contra su shuffle de grado exacto, tau fija", "brazo_s"),
    ("C3", "LW", "LS", "el brazo S con tau liquida", "brazo_s"),
    ("C4", "LW", "RW", "tau liquida contra tau fija, sobre el cableado de la mosca", "info"),
    ("C5", "LS", "RS", "tau liquida contra tau fija, sobre el shuffle", "info"),
    ("C6", "A", "F", "memoria liquida contra la misma memoria con tau constante", "liquida"),
    ("C7", "RW", "B", "conectoma recurrente contra el B feedforward del brazo W", "info"),
    ("C8", "RB", "B", "ruido recurrente contra ruido feedforward (efecto de la recurrencia sola)", "info"),
]
_COMB = {}


def p_normal(a, b):
    """Aproximacion normal de brazo_w.py: erfc(|t|/sqrt(2))."""
    va, vb = a.var(ddof=1), b.var(ddof=1)
    if va + vb < 1e-15:
        return 0.0, 1.0
    t = (a.mean() - b.mean()) / max(math.sqrt(va / len(a) + vb / len(b)), 1e-15)
    return float(t), float(math.erfc(abs(t) / math.sqrt(2)))


def welch(a, b):
    """t de Welch con df de Satterthwaite."""
    r = stats.ttest_ind(a, b, equal_var=False)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    den = (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    df = (va + vb) ** 2 / den if den > 0 else float("nan")
    return float(r.statistic), float(df), float(r.pvalue)


def p_perm(a, b):
    """Permutacion de la diferencia de medias, exacta si n1 + n2 <= 20; si no, 200.000 al azar con semilla fija."""
    x = np.concatenate([a, b])
    n1, n = len(a), len(a) + len(b)
    obs = abs(a.mean() - b.mean())
    if n <= 20:
        key = (n, n1)
        if key not in _COMB:
            _COMB[key] = np.array(list(itertools.combinations(range(n), n1)), dtype=np.int64)
        C = _COMB[key]
        s1 = x[C].sum(1)
    else:
        rng = np.random.default_rng(20261011)
        C = np.array([rng.permutation(n)[:n1] for _ in range(200000)])
        s1 = x[C].sum(1)
    d = np.abs(s1 / n1 - (x.sum() - s1) / (n - n1))
    return float(np.mean(d >= obs - 1e-15))


def holm(ps):
    """Holm-Bonferroni; devuelve los p ajustados en el orden original."""
    m = len(ps)
    orden = sorted(range(m), key=lambda i: ps[i])
    adj = [0.0] * m
    acc = 0.0
    for k, i in enumerate(orden):
        acc = max(acc, min(1.0, (m - k) * ps[i]))
        adj[i] = acc
    return adj


def main():
    """Carga celdas, compara, aplica las reglas declaradas y escribe el JSON."""
    ap = argparse.ArgumentParser(description="Agregador del brazo S recurrente")
    ap.add_argument("--celdas", required=True)
    ap.add_argument("--referencia", required=True)
    ap.add_argument("--json", required=True)
    a = ap.parse_args()

    ref = json.load(open(a.referencia))
    cel = {}
    for path in sorted(glob.glob(os.path.join(a.celdas, "celda_*.json"))):
        d = json.load(open(path))
        cel[(d["tarea"], d["brazo"])] = d
    print("celdas encontradas=" + str(len(cel)) + " de " + str(len(TAREAS) * len(BRAZOS)))
    faltan = [t + "/" + b for t in TAREAS for b in BRAZOS if (t, b) not in cel]
    print("NO MEDIDO (celdas que faltan): " + (", ".join(faltan) if faltan else "ninguna"))
    metas = sorted(set((d["meta"]["torch"], d["meta"]["cpu"], d["meta"]["hilos_torch"]) for d in cel.values()))
    for mt in metas:
        print("maquina: torch=" + str(mt[0]) + " cpu=" + str(mt[1]) + " hilos=" + str(mt[2]))
    shas = sorted(set(d["meta"]["md5_script"] for d in cel.values()))
    print("md5 del script en las celdas: " + ", ".join(shas))
    out = {"celdas": {t + "/" + b: {"mse": cel[(t, b)]["mse"], "mean": cel[(t, b)]["mean"], "sd": cel[(t, b)]["sd"],
                                    "entrenables": cel[(t, b)]["entrenables"]} for (t, b) in cel},
           "faltan": faltan, "contrastes": {}, "veredictos": {}, "reproduccion": {}, "auditoria_brazo_w": {}}

    print("")
    print("=" * 100)
    print("TABLA: MSE medio (sd) por tarea y brazo, 10 semillas")
    print("=" * 100)
    print("tarea     " + "".join(b.rjust(20) for b in BRAZOS))
    for t in TAREAS:
        fila = t.ljust(10)
        for b in BRAZOS:
            if (t, b) in cel:
                fila += (format(cel[(t, b)]["mean"], ".6f") + "(" + format(cel[(t, b)]["sd"], ".6f") + ")").rjust(20)
            else:
                fila += "NO MEDIDO".rjust(20)
        print(fila)

    print("")
    print("=" * 100)
    print("REPRODUCCION de A y B contra el brazo W del 2-oct (mismas semillas, mismo codigo copiado)")
    print("=" * 100)
    for t in TAREAS:
        for b in ("A", "B"):
            if (t, b) not in cel:
                print(t.ljust(9) + " " + b + "  NO MEDIDO")
                continue
            x = np.array(cel[(t, b)]["mse"]); y = np.array(ref["celdas"][t][b]["mse"])
            n = min(len(x), len(y))
            rel = float(np.max(np.abs(x[:n] - y[:n]) / np.abs(y[:n])))
            estado = "REPRODUCE (max rel <= 1e-6)" if rel <= 1e-6 else "NO REPRODUCE EXACTO"
            out["reproduccion"][t + "/" + b] = {"max_rel": rel, "mean_nuevo": float(x.mean()), "mean_ref": float(y.mean())}
            print(t.ljust(9) + " " + b + "  mean_nuevo=" + format(x.mean(), ".6f") + " mean_2oct=" + format(y.mean(), ".6f")
                  + " max_rel_por_semilla=" + format(rel, ".3e") + "  " + estado)

    print("")
    print("=" * 100)
    print("AUDITORIA del brazo W (2-oct) con la t correcta: W contra S y W contra B")
    print("=" * 100)
    for t in TAREAS:
        for p1, p2 in (("W", "S"), ("W", "B")):
            x = np.array(ref["celdas"][t][p1]["mse"]); y = np.array(ref["celdas"][t][p2]["mse"])
            tn, pn = p_normal(x, y); tw, df, pw = welch(x, y); pp = p_perm(x, y)
            out["auditoria_brazo_w"][t + "/" + p1 + "-" + p2] = {"p_normal": pn, "p_welch": pw, "df": df, "p_perm": pp}
            print(t.ljust(9) + " " + p1 + "-" + p2 + "  ratio=" + format(x.mean() / y.mean(), ".3f") + "x  p_normal=" + format(pn, ".4f")
                  + "  p_welch=" + format(pw, ".4f") + " (df " + format(df, ".1f") + ")  p_perm=" + format(pp, ".4f")
                  + "  " + ("indistinguibles" if pw > 0.05 else "difieren"))

    for cid, b1, b2, desc, regla in CONTRASTES:
        print("")
        print("=" * 100)
        print(cid + "  " + b1 + " contra " + b2 + ": " + desc)
        print("=" * 100)
        filas, ps = [], []
        for t in TAREAS:
            if (t, b1) not in cel or (t, b2) not in cel:
                filas.append((t, None)); ps.append(1.0)
                continue
            x = np.array(cel[(t, b1)]["mse"]); y = np.array(cel[(t, b2)]["mse"])
            tn, pn = p_normal(x, y); tw, df, pw = welch(x, y); pp = p_perm(x, y)
            filas.append((t, {"mean1": float(x.mean()), "mean2": float(y.mean()), "ratio": float(x.mean() / y.mean()),
                              "t": tw, "df": df, "p_welch": pw, "p_normal": pn, "p_perm": pp}))
            ps.append(pw)
        adj = holm(ps)
        gana = pierde = empata = medidas = 0
        gana_h = empata_h = pierde_h = 0
        res_c = {}
        for (t, f), ph in zip(filas, adj):
            if f is None:
                print(t.ljust(9) + " NO MEDIDO")
                continue
            medidas += 1
            f["p_holm"] = ph
            sig = f["p_welch"] <= 0.05
            if sig and f["mean1"] < f["mean2"]:
                gana += 1; estado = b1 + " MEJOR"
            elif sig:
                pierde += 1; estado = b1 + " PEOR"
            else:
                empata += 1; estado = "indistinguibles"
            if ph <= 0.05 and f["mean1"] < f["mean2"]:
                gana_h += 1
            elif ph <= 0.05:
                pierde_h += 1
            else:
                empata_h += 1
            res_c[t] = f
            print(t.ljust(9) + " " + b1 + "=" + format(f["mean1"], ".6f") + " " + b2 + "=" + format(f["mean2"], ".6f")
                  + " ratio=" + format(f["ratio"], ".3f") + "x  t=" + format(f["t"], "+.2f") + " df=" + format(f["df"], ".1f")
                  + "  p_welch=" + format(f["p_welch"], ".4f") + "  p_holm=" + format(ph, ".4f")
                  + "  p_perm=" + format(f["p_perm"], ".4f") + "  p_normal=" + format(f["p_normal"], ".4f") + "  -> " + estado)
        out["contrastes"][cid] = {"brazo1": b1, "brazo2": b2, "desc": desc, "tareas": res_c,
                                  "gana": gana, "empata": empata, "pierde": pierde, "medidas": medidas,
                                  "holm": {"gana": gana_h, "empata": empata_h, "pierde": pierde_h}}
        print("conteo (p_welch): " + b1 + " mejor en " + str(gana) + "/" + str(medidas) + ", indistinguibles en "
              + str(empata) + "/" + str(medidas) + ", peor en " + str(pierde) + "/" + str(medidas))
        print("conteo (Holm):    " + b1 + " mejor en " + str(gana_h) + ", indistinguibles en " + str(empata_h)
              + ", peor en " + str(pierde_h))
        if medidas < 4:
            v = "NO MEDIDO: faltan celdas, la regla pide las 4 tareas"
        elif regla == "aborto":
            v = ("SOBREVIVE: el conectoma congelado le gana al ruido congelado en " + str(gana) + "/4"
                 if gana >= 3 else
                 "ABORTO: el conectoma congelado le gana al ruido congelado solo en " + str(gana)
                 + "/4. La analogia del 96% fijo se retira tambien en el sustrato recurrente")
        elif regla == "brazo_s":
            if gana >= 3:
                v = "LA MOSCA PAGA: el cableado real le gana a su shuffle en " + str(gana) + "/4"
            elif empata >= 3:
                v = "PAGA LA SPARSITY, NO LA MOSCA: el cableado real y su shuffle son indistinguibles en " + str(empata) + "/4"
            elif pierde >= 3:
                v = "EL CABLEADO REAL RINDE PEOR QUE SU SHUFFLE en " + str(pierde) + "/4"
            else:
                v = "MIXTO: gana " + str(gana) + ", empata " + str(empata) + ", pierde " + str(pierde)
        elif regla == "liquida":
            v = ("LA NEURONA LIQUIDA PAGA en la memoria: gana en " + str(gana) + "/4"
                 if gana >= 3 else
                 "LA NEURONA LIQUIDA NO ES NECESARIA en esta memoria y estas tareas: gana solo en " + str(gana)
                 + "/4 (empata " + str(empata) + ", pierde " + str(pierde) + ")")
        else:
            v = "informativo: mejor " + str(gana) + ", indistinguible " + str(empata) + ", peor " + str(pierde)
        out["veredictos"][cid] = v
        print("VEREDICTO " + cid + ": " + v)

    print("")
    print("=" * 100)
    print("INTERACCION descriptiva: la ventaja del cableado real sobre su shuffle, con tau fija y con tau liquida")
    print("=" * 100)
    for t in TAREAS:
        if all((t, b) in cel for b in ("RW", "RS", "LW", "LS")):
            r_fija = cel[(t, "RW")]["mean"] / cel[(t, "RS")]["mean"]
            r_liq = cel[(t, "LW")]["mean"] / cel[(t, "LS")]["mean"]
            print(t.ljust(9) + " RW/RS=" + format(r_fija, ".3f") + "x  LW/LS=" + format(r_liq, ".3f")
                  + "x  (menor que 1 = el cableado real rinde mejor)")
        else:
            print(t.ljust(9) + " NO MEDIDO")

    with open(a.json, "w") as f:
        json.dump(out, f)
    print("")
    print("RESUMEN_VEREDICTOS " + json.dumps(out["veredictos"], ensure_ascii=True))
    print("FIN_AGREGADO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
