#!/usr/bin/env python3
"""Prueba del agregador del factorial 4 antes de sellar (respuesta 2026-10-13-015).

Uso: python3 prueba_agregar_factorial4.py <salida del humo T4 de Kaggle> <carpeta del factorial 3> <trabajo>
Casos:
  humo_t4        la salida real del humo en Kaggle, con --humo: tiene que dar VALIDO.
  humo_alterado  la misma salida con un W cambiado en el json de grilla: INTEGRIDAD tiene que dar False (EXIT 3).
  sint_igual     un CE sintetico igual a R2 (los 60 json y los 20 de nulos del factorial 3, con recibo y md5): la
                 primaria tiene que dar la del factorial 3, REGLA_IGUAL_F3 60/60, la escala 0 exacto y EQUIVALENTE.
  sint_mas2      el mismo con W + 0,02 en todas las corridas: primaria SUPERA y escala SUPERA (las dos SOSTENIDA).
  sint_menos2    W - 0,02: primaria NO_SUPERIOR y escala PIERDE (las dos REFUTADA, la escala resta).
Sale 0 si los cinco casos dan lo esperado.
"""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
AG = os.path.join(AQUI, "agregar_factorial4.py")
SHA = "ace8fe78093a9109c20235746d867f2b168290d2"
PIN = {"connectivity.parquet": "3d802fd542b5d18570ba1ba0bb0abed9", "annotations.tsv": "719904abad876c68ace1b5690c9b9b63"}


def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()


def agregar(d4, d3, humo):
    r = subprocess.run([sys.executable, AG, d4, d3] + (["--humo"] if humo else []), stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True)
    return r.returncode, r.stdout


def sintetico(d3, dest, delta):
    shutil.rmtree(dest, ignore_errors=True)
    k = os.path.join(dest, "kern")
    corr = []
    n_rep = 0
    for ruta in sorted(glob.glob(os.path.join(d3, "factorial2_R2_CON_TASA_*.json"))) + sorted(
            glob.glob(os.path.join(d3, "nulos_R2_*.json"))):
        r = json.load(open(ruta))
        r.setdefault("humo", False)
        nom = os.path.basename(ruta).replace("factorial2_R2_", "factorial4_CE_").replace("nulos_R2_", "nulos_CE_")
        if "corridas" in r:
            for x in r["corridas"]:
                x["W"] = x["W"] + delta
            if n_rep < 4:
                r.setdefault("info", {})["repro_r2"] = 0.9465
                n_rep += 1
        elif r.get("real") is not None:
            r["real"] = r["real"] + delta
        et = nom[:-5]
        os.makedirs(os.path.join(k, et))
        p = os.path.join(k, et, nom)
        with open(p, "w") as f:
            json.dump(r, f)
        corr.append(dict(etiqueta=et, rc=0, salidas_md5={nom: md5(p)}))
    et = dict(head=SHA, md5_instrumento="OK", n_gpu=2, **{"md5_" + a: b for a, b in PIN.items()})
    with open(os.path.join(k, "recibo_sint.json"), "w") as f:
        json.dump(dict(kernel="sint", rc=0, etapas=et, corridas=corr, duracion_s=0), f)
    return dest


def tiene(out, *frases):
    return all(f in out for f in frases)


def main():
    humo_dir, d3, trab = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(trab, exist_ok=True)
    casos = []
    rc, out = agregar(humo_dir, d3, True)
    casos.append(("humo_t4", out, rc == 0 and tiene(out, "CHEQUEO INTEGRIDAD archivos_con_md5=4/4 huerfanos=0 -> True",
                                                   "CHEQUEO REPRODUCE_PRIMARIA_F3 dif=+0.0085 IC90=[+0.0008, +0.0151] -> True",
                                                   "VEREDICTO_GLOBAL -> VALIDO")))
    alt = os.path.join(trab, "humo_alterado")
    shutil.rmtree(alt, ignore_errors=True)
    shutil.copytree(humo_dir, alt)
    g = glob.glob(os.path.join(alt, "**", "factorial4_CE_CON_TASA_*.json"), recursive=True)[0]
    r = json.load(open(g))
    r["corridas"][0]["W"] = 0.5
    json.dump(r, open(g, "w"))
    rc, out = agregar(alt, d3, True)
    casos.append(("humo_alterado", out, rc == 3 and tiene(out, "huerfanos=1 -> False", "VEREDICTO_GLOBAL -> INVALIDO")))
    esperado = {
        "sint_igual": (0.0, ["PRIMARIA CE_CON_TASA W=0.9353 regla_propia=0.9268 dif=+0.0085 IC90=[+0.0008, +0.0151] corridas=600 -> NO_INFERIOR",
                             "CHEQUEO REGLA_IGUAL_F3 combinaciones=60 iguales=60 -> True",
                             "dif=+0.0000 IC90=[+0.0000, +0.0000] corridas=600 -> EQUIVALENTE",
                             "HIPOTESIS H_SUPERA_CE -> SIN_DECIDIR", "HIPOTESIS H_ESCALA -> REFUTADA",
                             "NULOS Holm SL=0.0392 T=0.0392", "HIPOTESIS H_CABLEADO_CE -> SOSTENIDA",
                             "VEREDICTO_GLOBAL -> VALIDO"]),
        "sint_mas2": (0.02, ["-> SUPERA", "HIPOTESIS H_SUPERA_CE -> SOSTENIDA", "dif=+0.0200 IC90=[+0.0200, +0.0200] corridas=600 -> SUPERA",
                             "HIPOTESIS H_ESCALA -> SOSTENIDA", "VEREDICTO_GLOBAL -> VALIDO"]),
        "sint_menos2": (-0.02, ["-> NO_SUPERIOR", "HIPOTESIS H_SUPERA_CE -> REFUTADA",
                                "dif=-0.0200 IC90=[-0.0200, -0.0200] corridas=600 -> PIERDE",
                                "HIPOTESIS H_ESCALA -> REFUTADA (el cerebro entero resta)", "VEREDICTO_GLOBAL -> VALIDO"]),
    }
    for nombre, (delta, frases) in esperado.items():
        d = sintetico(d3, os.path.join(trab, nombre), delta)
        rc, out = agregar(d, d3, False)
        casos.append((nombre, out, rc == 0 and tiene(out, *frases)))
    todo = True
    for nombre, out, ok in casos:
        print("==== CASO %s -> %s" % (nombre, "PASA" if ok else "FALLA"))
        print("\n".join(x for x in out.splitlines() if not x.startswith("RECIBO")))
        todo = todo and ok
    print("PRUEBA_AGREGADOR -> %s" % ("PASA 5/5" if todo else "FALLA"))
    return 0 if todo else 1


if __name__ == "__main__":
    sys.exit(main())
