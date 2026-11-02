#!/usr/bin/env python3
"""Junta las dos mitades de cada celda principal de H_MECANISMO (enmienda de la respuesta 2026-11-02-002).

celda_p_E_right_a.json trae C0, C1, C2, C3, C4 y M5; celda_p_E_right_b.json trae C0, R1, R2, R3, R4 y K. Las dos
corren C0 con las mismas semillas: se exige que las cuentas de C0 sean identicas ensayo por ensayo (el modelo es
determinista dada la semilla). Si no lo son, o si cambian los conjuntos, la celda unida sale con "error" y el
agregado la trata como faltante. Si falta _b, la celda unida lleva solo lo de _a. Si falta _a, no hay celda.
Uso: python3 unir_celdas.py --dir D
"""
import argparse
import json
import os

ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")
DE_B = ("R1", "R2", "R3", "R4", "K")


def unir(ca, cb):
    """Devuelve (celda unida, informe)."""
    u = json.loads(json.dumps(ca))
    u["celda"] = ca["celda"][:-2]
    inf = {"a": ca["celda"], "b": cb["celda"] if cb else None}
    if cb is None:
        inf["estado"] = "SOLO_A"
        u["union"] = inf
        return u, inf
    c0a, c0b = ca["conds"].get("C0"), cb["conds"].get("C0")
    inf["C0_igual"] = bool(c0a is not None and c0b is not None and
                           [r["cuentas"] for r in c0a["ensayos"]] == [r["cuentas"] for r in c0b["ensayos"]] and
                           [r["seed"] for r in c0a["ensayos"]] == [r["seed"] for r in c0b["ensayos"]])
    inf["indices_igual"] = ca["indices"] == cb["indices"]
    inf["pines_igual"] = ca["pines"] == cb["pines"] and ca.get("sin_pin") == cb.get("sin_pin")
    for k in DE_B:
        if k in cb["conds"]:
            u["conds"][k] = cb["conds"][k]
    if "K" in cb:
        u["K"] = cb["K"]
    u["def"] = dict(ca["def"], conds=list(ca["def"]["conds"]) + [k for k in DE_B if k in cb["conds"]])
    u["segundos"] = ca.get("segundos", 0.0) + cb.get("segundos", 0.0)
    ok = inf["C0_igual"] and inf["indices_igual"] and inf["pines_igual"]
    inf["estado"] = "UNIDA" if ok else "DISCREPA"
    if not ok:
        u["error"] = "las mitades no coinciden: %s" % json.dumps(inf, sort_keys=True)
    u["union"] = inf
    return u, inf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    for e in ESTIM:
        ra = os.path.join(a.dir, "celda_p_%s_right_a.json" % e)
        rb = os.path.join(a.dir, "celda_p_%s_right_b.json" % e)
        if not os.path.exists(ra):
            print("UNION p_%s_right FALTA_A" % e, flush=True)
            continue
        ca = json.load(open(ra))
        cb = json.load(open(rb)) if os.path.exists(rb) else None
        u, inf = unir(ca, cb)
        with open(os.path.join(a.dir, "celda_p_%s_right.json" % e), "w") as f:
            json.dump(u, f)
        print("UNION p_%s_right %s" % (e, json.dumps(inf, sort_keys=True)), flush=True)


if __name__ == "__main__":
    main()
