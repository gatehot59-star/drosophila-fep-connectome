#!/usr/bin/env python3
"""Replica de la corrida 1 por la corrida 2 de H_MECANISMO (respuesta 2026-11-02-003).

Compara, celda por celda y ensayo por ensayo, las 9 celdas que terminaron en las dos corridas (ctrl_mn9 y las 8 de
tasas): semillas, cuentas de todas las neuronas observadas, espigas totales de la red entera, neuronas activas, primera
espiga de D y espigas tempranas, ademas de conjuntos, pines y filas tocadas. Ignora solo los tiempos de reloj. Antes
prueba que el comparador detecta una espiga de diferencia. Despues rechequea, sin usar unir_celdas.py, que los dos C0
de cada celda principal partida de la corrida 2 sean identicos, y que cada log de la corrida 2 haya pasado los pines.
Uso: python3 verificar_replica.py --c1 DIR_CORRIDA1 --c2 DIR_CORRIDA2
"""
import argparse, copy, glob, json, os, re

RELOJ = {"seg_run", "seg", "segundos"}
CELDAS = ["ctrl_mn9"] + ["t%d_%s_right" % (h, e) for h in (20, 150) for e in ("LC4", "LPLC2", "LPLC1", "LPLC4")]


def sin_reloj(x):
    if isinstance(x, dict):
        return {k: sin_reloj(v) for k, v in x.items() if k not in RELOJ}
    if isinstance(x, list):
        return [sin_reloj(v) for v in x]
    return x


def primera_dif(a, b, ruta=""):
    if type(a) != type(b):
        return ruta + " tipo"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return ruta + "/" + k + " falta"
            d = primera_dif(a[k], b[k], ruta + "/" + k)
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return ruta + " largo %d!=%d" % (len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = primera_dif(x, y, ruta + "[%d]" % i)
            if d:
                return d
        return None
    return None if a == b else ruta + " %r!=%r" % (a, b)


def contar(c):
    n_cuentas = sum(len(r["cuentas"]) for v in c["conds"].values() for r in v["ensayos"])
    n_ens = sum(len(v["ensayos"]) for v in c["conds"].values())
    espigas = sum(r["espigas"] for v in c["conds"].values() for r in v["ensayos"])
    return n_ens, n_cuentas, espigas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--c1", required=True); ap.add_argument("--c2", required=True)
    a = ap.parse_args()
    # el comparador puede dar rojo
    c = sin_reloj(json.load(open(os.path.join(a.c2, "celda_t20_LC4_right.json"))))
    m1 = copy.deepcopy(c); m1["conds"]["C1"]["ensayos"][7]["cuentas"][3] += 1
    m2 = copy.deepcopy(c); m2["conds"]["C0"]["ensayos"][19]["espigas"] -= 1
    m3 = copy.deepcopy(c); m3["conds"]["C0"]["ensayos"][0]["seed"] += 1
    neg = [primera_dif(c, m) is not None for m in (m1, m2, m3)]
    print("CONTROL_NEGATIVO detecta_1_espiga=%s detecta_espigas_red=%s detecta_semilla=%s identico_consigo=%s" % (
        neg[0], neg[1], neg[2], primera_dif(c, copy.deepcopy(c)) is None))
    ok_all = all(neg)
    tot = [0, 0, 0]
    for nom in CELDAS:
        x = sin_reloj(json.load(open(os.path.join(a.c1, "celda_%s.json" % nom))))
        y = sin_reloj(json.load(open(os.path.join(a.c2, "celda_%s.json" % nom))))
        d = primera_dif(x, y)
        n_ens, n_c, esp = contar(y)
        tot = [tot[0] + n_ens, tot[1] + n_c, tot[2] + esp]
        ok_all &= d is None
        print("REPLICA %s %s ensayos=%d cuentas=%d espigas_red=%d pines=%s target=%s/%s" % (
            nom, "IDENTICA" if d is None else "DIFIERE en " + d, n_ens, n_c, esp,
            all(y["pines"].values()) and not y["sin_pin"], x["target"], y["target"]))
    print("TOTAL ensayos=%d cuentas=%d espigas_red=%d" % tuple(tot))
    for e in ("LC4", "LPLC2", "LPLC1", "LPLC4"):
        pa = json.load(open(os.path.join(a.c2, "celda_p_%s_right_a.json" % e)))
        pb = json.load(open(os.path.join(a.c2, "celda_p_%s_right_b.json" % e)))
        d = primera_dif(sin_reloj(pa["conds"]["C0"]), sin_reloj(pb["conds"]["C0"]))
        ok_all &= d is None
        print("C0_A_B p_%s_right %s ensayos=%d" % (e, "IDENTICO" if d is None else "DIFIERE en " + d, len(pa["conds"]["C0"]["ensayos"])))
    for f in sorted(glob.glob(os.path.join(a.c2, "medir_*.log"))):
        s = open(f).read()
        oks = len(re.findall(r": OK$", s, re.M))
        pin = '"comp": true, "conjuntos": true, "conn": true, "model": true} sin_pin=False' in s
        fuente = re.search(r"^SOURCE_COMMIT (\w+)", s, re.M)
        fin = "FIN celda=" in s
        ok_all &= oks == 14 and pin and fin
        print("LOG %s ok_lines=%d pines=%s fuente=%s fin=%s" % (os.path.basename(f), oks, pin, fuente.group(1)[:7] if fuente else None, fin))
    print("REPLICA_CORRIDA2 %s" % ("PASS" if ok_all else "FAIL"))


if __name__ == "__main__":
    main()
