#!/usr/bin/env python3
"""H_LIF_SHUFG, agregado (respuesta 2026-10-14-055; sello SELLO-LIF-SHUFG-054.md, 307db84, md5 9e7e25f7).

Lee lif_shufg_real.json y lif_shufg_G_k*.json de --dir.
Controles: PIN (cada JSON con la version, el blob de model.py, brian2 2.10.1, los md5 de datos, 1000 ms y 100 Hz),
CTRL_REAL (MN9 con espiga en 27 o mas de los 30 ensayos reales; si falla, todo NO_MEDIDO) y NULO_MISMO (el del
instrumento: un nulo que no coincide queda NO_MEDIDO).
Hipotesis con las bandas de H_UMB_MN9 (ninguno: SOSTENIDA; 5 o mas: REFUTADA; de 1 a 4: SIN_DECIDIR):
H_LIF_G_SHIU cuenta los nulos que llegan (E_MN9 >= 5 de 10); H_LIF_G_VARA cuenta los nulos con F_MN9 igual o mayor
que la del real (SOSTENIDA pide ademas F_MN9 real > 0); H_LIF_K32 dice si k32 llega. Un nulo faltante o NO_MEDIDO
cuenta aparte y un veredicto se lee solo si no cambia con ningun valor de los que faltan.
Lectura fijada de k32 (seccion 6 del sello) y descriptivas (activas, K, J contra la S_LIF del real, atajo).
Uso: python3 agregar_lif_shufg.py --dir D [--humo --ks 99 --foco 99] [--sin-pin]
"""
import argparse
import glob
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import lif_shufg as lg  # noqa: E402

NL = chr(10)
LLEGA = 5          # E_MN9 >= 5 de 10: el criterio de los nulos en REPRO_SHIU (sello 046)
N_RUN_NULO = 10
N_RUN_REAL = 30
MIN_REAL = 27      # CTRL_REAL
DESBOCADO = 10     # mas de 10 veces las activas del real
BANDA_REF = 5      # 5 o mas nulos: REFUTADA
KS = list(range(40))
FOCO = 32

TEXTO_K32 = {
    "NO_LLEGA": "el atajo de k32 es de nuestra celda de tasa; el LIF no lo toma. El freno de H_UMB_MN9 es de la "
                "neurona, no del barajado.",
    "LLEGA_DESBOCADO": "llega por actividad global, no por un camino; el freno es del barajado, que vuelve "
                       "epileptico a ese grafo.",
    "LLEGA_IGUAL_O_MAS": "el atajo es del barajado y con nuestra vara frena tambien a Shiu.",
    "LLEGA_MENOS": "el camino esta en el barajado (los dos modelos lo toman), pero el LIF lo separa del real por "
                   "intensidad y nuestra celda no: lo que nos falta es contraste.",
    "NO_MEDIDO": "k32 sin medir: no hay lectura.",
}
TEXTO_SHIU_REF = ("contra SHUF_G el LIF de Shiu es menos especifico que nuestra UMB (1 de 40); SHUF_G no sirve de vara "
                  "para MN9 tal como esta. Cambiar el nulo es otro sello y no rescata la 051.")


def pin(d, humo, sin_pin):
    """Devuelve (ok, motivo) para un JSON del instrumento."""
    if d.get("version") != lg.VERSION:
        return False, "version %s" % d.get("version")
    if bool(d.get("humo")) != bool(humo):
        return False, "humo=%s en un agregado humo=%s" % (d.get("humo"), humo)
    if sin_pin:
        return True, "sin_pin"
    if d.get("sin_pin"):
        return False, "corrida con --sin-pin"
    if d.get("model_blob") != lg.ls.BLOB_MODEL:
        return False, "blob de model.py"
    if d.get("brian2") != lg.BRIAN2:
        return False, "brian2 %s" % d.get("brian2")
    md5 = d.get("md5") or {}
    if md5.get("conn") != lg.le.MD5["conn"] or md5.get("comp") != lg.MD5_COMP:
        return False, "md5 de datos"
    if d.get("t_run_ms") != 1000.0 or d.get("r_poi_hz") != lg.R_POI_HZ:
        return False, "t_run o r_poi"
    if d.get("leer") != lg.le.MN9:
        return False, "lectura distinta de MN9"
    return True, "ok"


def cargar(carpeta, humo, sin_pin):
    real, nulos, pines = None, {}, []
    ruta = os.path.join(carpeta, "lif_shufg_real.json")
    if os.path.exists(ruta):
        d = json.load(open(ruta))
        ok, motivo = pin(d, humo, sin_pin)
        pines.append(("lif_shufg_real.json", ok, motivo))
        real = d if ok else None
    for ruta in sorted(glob.glob(os.path.join(carpeta, "lif_shufg_G_k*.json"))):
        d = json.load(open(ruta))
        ok, motivo = pin(d, humo, sin_pin)
        pines.append((os.path.basename(ruta), ok, motivo))
        if not ok:
            continue
        for k, v in d.get("nulos", {}).items():
            nulos[int(k)] = v
    return real, nulos, pines


def estado(v):
    """MEDIDO si NULO_MISMO PASA y hay corrida de 10 ensayos; si no, NO_MEDIDO."""
    if not v:
        return "NO_MEDIDO"
    if (v.get("nulo_mismo") or {}).get("estado") != "PASA":
        return "NO_MEDIDO"
    c = v.get("corrida")
    if not c or c.get("n_run") != N_RUN_NULO:
        return "NO_MEDIDO"
    return "MEDIDO"


def banda(c, sost_ok=True):
    if c >= BANDA_REF:
        return "REFUTADA"
    if c == 0 and sost_ok:
        return "SOSTENIDA"
    return "SIN_DECIDIR"


def robusto(c, faltan, sost_ok=True):
    """El veredicto con los faltantes en un extremo y en el otro; si cambia, NO_MEDIDO."""
    v1, v2 = banda(c, sost_ok), banda(c + faltan, sost_ok)
    return v1 if v1 == v2 else "NO_MEDIDO"


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if (a | b) else float("nan")


def ctrl_real(real, humo):
    if real is None or not real.get("corrida"):
        return "FALLA", "sin real valido", None
    c = real["corrida"]
    n_run = c.get("n_run")
    minimo = MIN_REAL if not humo else int(math.ceil(0.9 * n_run))
    if not humo and n_run != N_RUN_REAL:
        return "FALLA", "n_run=%s, el sello pide %d" % (n_run, N_RUN_REAL), minimo
    ok = c["ensayos_mn9"] >= minimo
    return ("PASA" if ok else "FALLA"), "%d de %d, minimo %d" % (c["ensayos_mn9"], n_run, minimo), minimo


def lectura_k32(fila, F_real):
    if fila is None or fila["estado"] != "MEDIDO":
        return "NO_MEDIDO"
    if not fila["llega"]:
        return "NO_LLEGA"
    if fila["desbocado"]:
        return "LLEGA_DESBOCADO"
    return "LLEGA_IGUAL_O_MAS" if fila["F_MN9"] >= F_real else "LLEGA_MENOS"


def agregar(real, nulos, pines, ks, foco, humo):
    out = {"version": lg.VERSION, "humo": humo, "ks": ks, "foco": foco,
           "pin": [{"archivo": a, "ok": o, "motivo": m} for a, o, m in pines]}
    lineas = ["== agregar_lif_shufg.py :: H_LIF_SHUFG (2026-10-14-055), sello SELLO-LIF-SHUFG-054.md =="]
    if humo:
        lineas.append("HUMO: numeros sin valor")
    pin_ok = bool(pines) and all(o for _, o, _ in pines)
    out["PIN"] = "PASA" if pin_ok else "FALLA"
    lineas.append("CONTROL PIN %s %s" % (out["PIN"], "; ".join("%s: %s" % (a, m) for a, o, m in pines if not o)))
    cr, motivo, minimo = ctrl_real(real, humo)
    out["CTRL_REAL"] = cr
    out["CTRL_REAL_motivo"] = motivo
    lineas.append("CONTROL CTRL_REAL %s (%s)" % (cr, motivo))
    F_real = real["corrida"]["tasa_mn9"] if real and real.get("corrida") else float("nan")
    act_real = real["corrida"]["activas"] if real and real.get("corrida") else None
    s_real = real["corrida"]["S_LIF_idx"] if real and real.get("corrida") else []
    if real and real.get("corrida"):
        c = real["corrida"]
        at = real.get("atajo", {})
        out["real"] = {"E_MN9": c["ensayos_mn9"], "n_run": c["n_run"], "F_MN9": c["tasa_mn9"],
                       "activas": c["activas"], "espigas": c["espigas"], "K": c["K"], "atajo": at}
        lineas.append("REAL E_MN9=%d de %d F_MN9=%.4f Hz activas=%d espigas=%d K=%d atajo n1=%s D1+=%s D2+=%s" % (
            c["ensayos_mn9"], c["n_run"], c["tasa_mn9"], c["activas"], c["espigas"], c["K"], at.get("n1"),
            at.get("D1+"), at.get("D2+")))
    filas = {}
    nm_pasa = nm_otro = 0
    for k in ks:
        v = nulos.get(k)
        st = estado(v)
        if v and (v.get("nulo_mismo") or {}).get("estado") == "PASA":
            nm_pasa += 1
        elif v:
            nm_otro += 1
        f = {"k": k, "estado": st}
        if v:
            nm = v.get("nulo_mismo") or {}
            f.update({"nulo_mismo": nm.get("estado"), "radio_crudo": nm.get("radio_crudo"),
                      "dif_rel": nm.get("dif_rel"), "atajo": v.get("atajo")})
        if st == "MEDIDO":
            c = v["corrida"]
            f.update({"E_MN9": c["ensayos_mn9"], "F_MN9": c["tasa_mn9"], "activas": c["activas"],
                      "espigas": c["espigas"], "K": c["K"], "J": jaccard(c["S_LIF_idx"], s_real),
                      "llega": c["ensayos_mn9"] >= LLEGA,
                      "ge_real": c["tasa_mn9"] >= F_real,
                      "desbocado": (act_real is not None and c["activas"] > DESBOCADO * act_real),
                      "segundos": c.get("segundos")})
            at = v.get("atajo") or {}
            lineas.append("NULO k=%d E_MN9=%d F_MN9=%.4f activas=%d K=%d J=%.4f n1=%s D1+=%s D2+=%s radio=%.6f "
                          "desbocado=%s | %.0f s" % (k, f["E_MN9"], f["F_MN9"], f["activas"], f["K"], f["J"],
                                                     at.get("n1"), at.get("D1+"), at.get("D2+"),
                                                     f["radio_crudo"], f["desbocado"], f["segundos"] or 0))
        else:
            if not v:
                por = "falta"
            elif f.get("nulo_mismo") != "PASA":
                por = "NULO_MISMO %s" % f.get("nulo_mismo")
            else:
                por = "corrida incompleta"
            lineas.append("NULO k=%d NO_MEDIDO (%s)" % (k, por))
        filas[k] = f
    out["nulos"] = {str(k): f for k, f in filas.items()}
    med = [k for k in ks if filas[k]["estado"] == "MEDIDO"]
    faltan = len(ks) - len(med)
    llegan = [k for k in med if filas[k]["llega"]]
    ge = [k for k in med if filas[k]["ge_real"]]
    desb = [k for k in med if filas[k]["desbocado"]]
    out.update({"medidos": len(med), "faltan": faltan, "llegan": llegan, "ge_real": ge, "desbocados": desb})
    lineas.append("CONTROL NULO_MISMO PASA en %d de %d (otros estados %d, sin archivo %d)" % (
        nm_pasa, len(ks), nm_otro, len(ks) - nm_pasa - nm_otro))
    lineas.append("NULOS medidos=%d faltan=%d llegan=%s ge_real=%s desbocados=%s" % (len(med), faltan, llegan, ge,
                                                                                     desb))
    if cr == "PASA" and pin_ok:
        h_shiu = robusto(len(llegan), faltan)
        h_vara = robusto(len(ge), faltan, sost_ok=F_real > 0)
        fk = filas.get(foco)
        h_k = "NO_MEDIDO" if (fk is None or fk["estado"] != "MEDIDO") else ("LLEGA" if fk["llega"] else "NO_LLEGA")
        lk = lectura_k32(fk, F_real)
    else:
        h_shiu = h_vara = h_k = lk = "NO_MEDIDO"
    out.update({"H_LIF_G_SHIU": h_shiu, "H_LIF_G_VARA": h_vara, "H_LIF_K32": h_k, "LECTURA_K32": lk})
    lineas.append("VEREDICTO H_LIF_G_SHIU %s (llegan=%d, faltan=%d)" % (h_shiu, len(llegan), faltan))
    lineas.append("VEREDICTO H_LIF_G_VARA %s (con F_MN9 >= real=%d, faltan=%d, F_real=%.4f Hz)" % (
        h_vara, len(ge), faltan, F_real))
    lineas.append("VEREDICTO H_LIF_K32 %s (foco k=%d)" % (h_k, foco))
    lineas.append("LECTURA K32 %s: %s" % (lk, TEXTO_K32[lk]))
    if h_shiu == "REFUTADA":
        lineas.append("LECTURA H_LIF_G_SHIU_REFUTADA: " + TEXTO_SHIU_REF)
    con_n1 = [k for k in ks if filas[k].get("nulo_mismo") == "PASA" and (filas[k].get("atajo") or {}).get("n1", 0) >= 1]
    fk = filas.get(foco) or {}
    out["descriptivo"] = {"nulos_con_n1": con_n1, "foco_atajo": fk.get("atajo"),
                          "foco_n1_ge_1": bool((fk.get("atajo") or {}).get("n1", 0) >= 1),
                          "foco_unico_con_n1": con_n1 == [foco]}
    lineas.append("DESCRIPTIVO nulos con n1>=1: %s | foco n1=%s D1+=%s D2+=%s | foco unico con n1>=1: %s" % (
        con_n1, (fk.get("atajo") or {}).get("n1"), (fk.get("atajo") or {}).get("D1+"),
        (fk.get("atajo") or {}).get("D2+"), con_n1 == [foco]))
    if med:
        acts = sorted(filas[k]["activas"] for k in med)
        js = sorted(filas[k]["J"] for k in med)
        fs = sorted(filas[k]["F_MN9"] for k in med)
        out["descriptivo"].update({"activas_mediana": acts[len(acts) // 2], "activas_max": acts[-1],
                                   "J_mediana": js[len(js) // 2], "J_max": js[-1], "F_MN9_max": fs[-1]})
        lineas.append("DESCRIPTIVO activas mediana=%d max=%d | J mediana=%.4f max=%.4f | F_MN9 max=%.4f Hz" % (
            acts[len(acts) // 2], acts[-1], js[len(js) // 2], js[-1], fs[-1]))
    return out, lineas


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--humo", action="store_true")
    ap.add_argument("--ks", default="", help="por defecto 0 a 39")
    ap.add_argument("--foco", type=int, default=FOCO)
    ap.add_argument("--sin-pin", action="store_true", help="solo para la prueba")
    a = ap.parse_args(argv)
    ks = [int(x) for x in a.ks.split(",")] if a.ks else list(KS)
    real, nulos, pines = cargar(a.dir, a.humo, a.sin_pin)
    out, lineas = agregar(real, nulos, pines, ks, a.foco, a.humo)
    for s in lineas:
        print(s, flush=True)
    with open(os.path.join(a.dir, "agregado_lif_shufg.json"), "w") as f:
        json.dump(out, f, indent=1)
    with open(os.path.join(a.dir, "agregado_lif_shufg.log"), "w") as f:
        f.write(NL.join(lineas) + NL)
    return out


if __name__ == "__main__":
    main()
