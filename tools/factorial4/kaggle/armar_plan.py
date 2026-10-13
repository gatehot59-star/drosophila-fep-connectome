#!/usr/bin/env python3
"""Arma los planes de Kaggle del factorial 4 de la mosca (respuesta 2026-10-13-015) desde el bloque comun del humo
que ya corrio en Kaggle (plan_humo_kaggle.json: cuenta, SHA del instrumento, md5, insumos y pip).

Uso: python3 armar_plan.py <plan_humo_kaggle.json> <destino>
Escribe en <destino>:
  plan_humo_carriles.json  un kernel, dos carriles a la vez (una T4 cada uno), verificar con 1000 ensayos: mide si dos
                           procesos simultaneos mantienen el tiempo por ensayo y si cada GPU reproduce R2.
  plan_factorial4.json     el sellado: dos kernels T4 x2, cuatro carriles, 22 trabajos.
Grilla: 6 celdas x 10 semillas de tau (0..9) x 10 pruebas (2..11), las mismas 600 corridas del factorial 3, en 12
trabajos (una celda y media grilla de tau cada uno). Nulos: 50 SL y 50 T en la celda 0,3|0,15, tau 0, prueba 2, en
10 trabajos de 10; el de SL k0=0 mide tambien el real. El primer trabajo de cada carril pide --repro_r2. En cada
carril va primero la grilla y despues los nulos.
"""
import json
import os
import sys

CELDAS = ["0.0|0.15", "0.0|0.45", "0.3|0.15", "0.3|0.45", "0.6|0.15", "0.6|0.45"]
PRUEBAS = ",".join(str(p) for p in range(2, 12))
MITADES = ("0,1,2,3,4", "5,6,7,8,9")


def grilla(ci, h, repro):
    a = ["--modo", "grilla", "--taus", MITADES[h], "--pruebas", PRUEBAS, "--celdas", CELDAS[ci],
         "--etiqueta", "c%dh%d" % (ci, h)]
    return dict(etiqueta="grilla_c%dh%d" % (ci, h), args=a + (["--repro_r2"] if repro else []))


def nulos(tipo, k0, real):
    a = ["--modo", "nulos", "--tipo", tipo, "--k0", str(k0), "--n", "10"]
    return dict(etiqueta="nulos_%s_k%03d" % (tipo.lower(), k0), args=a + (["--real"] if real else []))


def main():
    with open(sys.argv[1]) as f:
        comun = json.load(f)
    dest = sys.argv[2]
    comun.pop("kernels")
    comun.pop("nota", None)
    carriles = {
        ("a", 0): [grilla(0, 0, True), grilla(1, 0, False), grilla(2, 0, False),
                   nulos("SL", 0, True), nulos("SL", 10, False), nulos("SL", 20, False)],
        ("a", 1): [grilla(3, 0, True), grilla(4, 0, False), grilla(5, 0, False),
                   nulos("T", 0, False), nulos("T", 10, False), nulos("T", 20, False)],
        ("b", 0): [grilla(0, 1, True), grilla(1, 1, False), grilla(2, 1, False),
                   nulos("SL", 30, False), nulos("SL", 40, False)],
        ("b", 1): [grilla(3, 1, True), grilla(4, 1, False), grilla(5, 1, False),
                   nulos("T", 30, False), nulos("T", 40, False)],
    }
    kernels = [dict(slug="f4-ce-%s-2026-10-13" % kn, corridas=[dict(c, gpu=g) for g in (0, 1) for c in carriles[(kn, g)]])
               for kn in ("a", "b")]
    plan = dict(comun, maquina="NvidiaTeslaT4", kernels=kernels,
                nota="factorial 4 sellado: cerebro entero, 600 corridas (6 celdas x 10 tau x 10 pruebas, las del factorial 3) "
                     "y 50 SL + 50 T; dos kernels T4 x2, cuatro carriles, 22 trabajos")
    humo = dict(comun, maquina="NvidiaTeslaT4",
                nota="humo de carriles: dos procesos a la vez, una T4 cada uno; mide s/ensayo con concurrencia y REPRO_R2 por GPU",
                kernels=[dict(slug="f4-ce-humo-carriles-2026-10-13", corridas=[
                    dict(etiqueta="verificar_g0", gpu=0, args=["--modo", "verificar", "--medir_ensayos", "1000", "--repro_r2",
                                                              "--etiqueta", "g0"]),
                    dict(etiqueta="verificar_g1", gpu=1, args=["--modo", "verificar", "--medir_ensayos", "1000", "--repro_r2",
                                                              "--etiqueta", "g1"])])])
    trab = [c for k in kernels for c in k["corridas"]]
    n_g = sum(1 for c in trab if "grilla" in c["args"])
    n_n = sum(1 for c in trab if "nulos" in c["args"])
    ks = sorted((c["args"][c["args"].index("--tipo") + 1], int(c["args"][c["args"].index("--k0") + 1])) for c in trab
                if "nulos" in c["args"])
    combos = sorted((ci, h) for ci in range(6) for h in (0, 1))
    hechos = sorted((CELDAS.index(c["args"][c["args"].index("--celdas") + 1]), MITADES.index(c["args"][c["args"].index("--taus") + 1]))
                    for c in trab if "grilla" in c["args"])
    ok = (n_g == 12 and n_n == 10 and hechos == combos and
          ks == sorted([("SL", k) for k in range(0, 50, 10)] + [("T", k) for k in range(0, 50, 10)]) and
          sum("--real" in c["args"] for c in trab) == 1 and sum("--repro_r2" in c["args"] for c in trab) == 4)
    print("PLAN trabajos=%d grilla=%d nulos=%d corridas_de_grilla=%d nulos_por_tipo=%d -> %s" % (
        len(trab), n_g, n_n, n_g * 5 * 10, n_n * 10 // 2, "OK" if ok else "MAL"))
    for nombre, p in (("plan_factorial4.json", plan), ("plan_humo_carriles.json", humo)):
        with open(os.path.join(dest, nombre), "w") as f:
            json.dump(p, f, indent=1, sort_keys=True)
        print("escrito %s" % nombre)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
