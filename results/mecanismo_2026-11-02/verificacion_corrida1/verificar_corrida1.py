#!/usr/bin/env python3
"""Verificacion independiente de la corrida 1 de H_MECANISMO (run 41410027436, commit f323befc), respuesta 2026-11-02-002.
No usa agregar_mecanismo.py: recomputa D y X desde las cuentas por neurona, usa permutacion EXACTA de signos (2^20)
en vez de Monte Carlo, cuenta las filas tocadas por C1 desde el parquet de Shiu y compara el censo de Actions con el de
brain-env. Uso: python3 verificar_corrida1.py --dir ACTIONS_CORRER --parquet P --comp K --paso12-local L
"""
import argparse, glob, hashlib, json, os, re
import numpy as np, pandas as pd, pyarrow.parquet as pq


def exact_p(d):
    d = np.asarray(d, float); n = len(d); t = abs(d.mean()); cnt = 0; tot = 0
    bits = np.arange(n, dtype=np.uint64)
    for start in range(0, 2 ** n, 1 << 16):
        idx = np.arange(start, min(start + (1 << 16), 2 ** n), dtype=np.uint64)
        s = (((idx[:, None] >> bits) & np.uint64(1)).astype(np.float64) * 2 - 1)
        cnt += int((np.abs(s @ d / n) >= t - 1e-12).sum()); tot += len(idx)
    return cnt / tot, cnt, tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True); ap.add_argument("--parquet", required=True)
    ap.add_argument("--comp", required=True); ap.add_argument("--paso12-local", required=True)
    a = ap.parse_args(); D = a.dir.rstrip("/") + "/"
    lin = [l.split() for l in open(D + "MD5SUMS.txt")]
    bad = [f for h, f in lin if f != "MD5SUMS.txt" and hashlib.md5(open(D + f, "rb").read()).hexdigest() != h]
    print("MD5SUMS archivos=%d discrepan=%s" % (len(lin), bad))
    print("conjuntos_actions_sha256=%s" % hashlib.sha256(open(D + "conjuntos_flywire.json", "rb").read()).hexdigest())
    for f in sorted(glob.glob(D + "celda_t*.json")):
        c = json.load(open(f)); co = c["conds"]; I = c["indices"]; pos = {m: k for k, m in enumerate(I["mirar"])}
        suma = lambda r, g: sum(r["cuentas"][pos[x]] for x in I[g])
        d0 = [suma(r, "D") for r in co["C0"]["ensayos"]]; d1 = [suma(r, "D") for r in co["C1"]["ensayos"]]
        s0 = [suma(r, "S") for r in co["C0"]["ensayos"]]; s1 = [suma(r, "S") for r in co["C1"]["ensayos"]]
        x0 = [suma(r, "X") for r in co["C0"]["ensayos"]]
        semillas = [r["seed"] for r in co["C0"]["ensayos"]] == [r["seed"] for r in co["C1"]["ensayos"]] == list(range(20261102, 20261122))
        crn = sum(1 for p, q in zip(co["C0"]["ensayos"], co["C1"]["ensayos"]) if [p["cuentas"][pos[s]] for s in I["S"]] == [q["cuentas"][pos[s]] for s in I["S"]])
        d = np.array(d1) - np.array(d0); pe, cn, tt = exact_p(d); m0, m1 = np.mean(d0), np.mean(d1); nd = len(I["D"])
        print("%s D0=%.1f D1=%.1f cociente=%.2f rel=%.3f positivos=%d/20 p_exacto=%.3g (%d/%d) recomputo_igual=%s semillas_iguales=%s crn_S=%d/20 S_dif=%.2f%% tasa_D0=%.1fHz tasa_D1=%.1fHz X0=%.0f tocadas_C1=%d pines=%s" % (
            c["celda"], m0, m1, m1 / m0, (m1 - m0) / m1, int((d > 0).sum()), pe, cn, tt, d0 == co["C0"]["D"] and d1 == co["C1"]["D"],
            semillas, crn, 100 * (np.mean(s1) - np.mean(s0)) / np.mean(s0), m0 / nd, m1 / nd, np.mean(x0), co["C1"]["tocadas"]["filas"],
            all(c["pines"].values()) and not c["sin_pin"]))
    c = json.load(open(D + "celda_ctrl_mn9.json"))
    print("ctrl_mn9 ensayos_con_MN9=%d/10 media=%.1f pines=%s" % (sum(1 for v in c["conds"]["C0"]["D"] if v > 0), np.mean(c["conds"]["C0"]["D"]), all(c["pines"].values())))
    conj = json.load(open(D + "conjuntos_flywire.json"))
    ids = pd.read_csv(a.comp, index_col=0).index.to_numpy(np.int64); f2i = {int(f): k for k, f in enumerate(ids)}
    t = pq.read_table(a.parquet, columns=["Presynaptic_Index", "Excitatory x Connectivity"]); pre = t.column(0).to_numpy(); w = t.column(1).to_numpy(); del t
    for e in ("LC4_right", "LPLC2_right", "LPLC1_right", "LPLC4_right"):
        X = np.array([f2i[x] for x in conj["estimulos"][e]["X"]]); m = np.isin(pre, X)
        print("tocadas_independiente %s filas_preX=%d con_peso=%d todas_negativas=%s" % (e, int(m.sum()), int((w[m] != 0).sum()), bool((w[m] < 0).all())))
    tag = lambda s: [re.sub(r'"seconds": [0-9.]+|"maxrss_kib": [0-9]+', "", l) for l in s.splitlines() if re.match(r"^[A-Z_]+ \{", l)]
    A = tag(open(D + "paso12.log").read()); B = tag(open(a.paso12_local).read())
    dif = [(x, y) for x, y in zip(A, B) if x != y]
    claves = sorted(set(k for x, y in dif for k, v in json.loads(x.split(" ", 1)[1]).items() if json.loads(y.split(" ", 1)[1]).get(k) != v))
    print("paso12_lineas_etiquetadas actions=%d brainenv=%d distintas=%d campos_que_difieren=%s" % (len(A), len(B), len(dif), claves))


if __name__ == "__main__":
    main()
