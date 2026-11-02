#!/usr/bin/env python3
"""DESCRIPTIVO POST HOC, NO SELLADO (respuesta 2026-11-02-004). No cambia ningun veredicto.

Espigas por neurona D en C0, C1, C3 y C4 de la corrida 2 (mitad a de cada celda principal), ordenadas por lo que
sube al silenciar X. El tipo de cada D sale de conjuntos_flywire.json mapeado con Completeness_783.csv, y se exige que
coincida con el D_tipo registrado en la celda.
Al final, una cuenta analitica sobre las ecuaciones de Shiu (v' = (v_0 - v + g)/t_mbr, g' = -g/tau, salto g += w):
cuantas sinapsis de una sola neurona hacen falta para que una espiga suya, desde reposo, lleve al blanco al umbral.
Uso: python3 d_por_tipo.py --dir ACTIONS_CORRER2 --comp K
"""
import argparse, json, math
import numpy as np, pandas as pd

ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", required=True); ap.add_argument("--comp", required=True)
    a = ap.parse_args(); D = a.dir.rstrip("/") + "/"
    conj = json.load(open(D + "conjuntos_flywire.json"))
    ids = pd.read_csv(a.comp, index_col=0).index.to_numpy(np.int64); f2i = {int(f): k for k, f in enumerate(ids)}
    for e in ESTIM:
        es = conj["estimulos"][e + "_right"]
        tipo_de = {f2i[r]: t for r, t in zip(es["D"], es["D_tipo"])}
        ca = json.load(open(D + "celda_p_%s_right_a.json" % e))
        pos = {x: k for k, x in enumerate(ca["indices"]["mirar"])}
        Dn = ca["indices"]["D"]; tl = [tipo_de[int(x)] for x in Dn]
        m = {}
        for c in ("C0", "C1", "C3", "C4"):
            M = np.array([r["cuentas"] for r in ca["conds"][c]["ensayos"]], float).mean(axis=0)
            m[c] = np.array([M[pos[x]] for x in Dn])
        sube = m["C1"] - m["C0"]; o = np.argsort(-sube, kind="stable")
        print("D %s tipos_iguales_a_la_celda=%s suma_C0=%.2f suma_C1=%.2f top3_de_la_subida=%.3f" % (
            e, tl == list(ca["D_tipo"]), m["C0"].sum(), m["C1"].sum(), float(sube[o[:3]].sum() / sube.sum())))
        for k in o:
            print("  %s %-8s C0=%.1f C1=%.1f C3=%.1f C4=%.1f" % (e, tl[k], m["C0"][k], m["C1"][k], m["C3"][k], m["C4"][k]))
    t_mbr, tau, w_syn, gap = 20.0, 5.0, 0.275, 7.0
    tp = tau * t_mbr / (t_mbr - tau) * math.log(t_mbr / tau)
    k = tau / (t_mbr - tau) * (math.exp(-tp / t_mbr) - math.exp(-tp / tau))
    print("PSP pico = %.5f x w a los %.2f ms; sinapsis minimas de una sola neurona para cruzar el umbral desde reposo = %d; 190 sinapsis dan %.2f mV (umbral a %.1f mV)" % (
        k, tp, math.ceil(gap / (k * w_syn)), 190 * w_syn * k, gap))


if __name__ == "__main__":
    main()
