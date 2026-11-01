#!/usr/bin/env python3
"""docs/auditorias/evidencia/2026-11-01-02/auditoria_estricto.py

Auditoria 2026-11-01-02 de H_REUSO_ESTRICTO. Misma instancia que BRAIN: no es
independiente (W-01); el instrumento y su salida cruda son el testigo.

Lee los recibos crudos que el runner commiteo en 0bc09b6 (estricto.json, run.log)
y los del verificador en 6db5d08 (verificar_estricto.py, verificacion.log), exige
sus SHA256, vuelve a correr el verificador publicado y compara su salida con la
publicada. Despues calcula lo que la respuesta 005 no reporto: conteos absolutos
del motivo, comparabilidad de T1 (denominador variable), T2 por X, correlaciones
dentro del nulo y margen contra el maximo nulo.

No recalcula estadisticos desde los grafos: lee lo que escribio el productor.
Uso: python3 auditoria_estricto.py ESTRICTO_JSON RUN_LOG VERIFICADOR VERIF_LOG
Salida: 0 si todo se leyo y verifico; 2 pin distinto; 3 verificador distinto.
"""
import hashlib
import json
import math
import subprocess
import sys

PINS = {
    "estricto.json": "ffce074c422835b426c717902e0510d6bcdd130ecff45d9fccce25e182a89282",
    "run.log": "00058fbd432f3d298c2d8edc7c5b4485f28ec95208413211fb1256f4d80a60f0",
    "verificar_estricto.py": "41ab582abb40fb707cc3f17d18fccd6e35309561b5116254b51d96b06248a9ef",
    "verificacion.log": "7dc94d7832a52054368774c83e0de4ffaf093bdc4a94c9bcb4e7dbc488e039cc",
}
CAMPOS = ("n_cab", "n_pares_ffi", "t1", "t2", "n_x")


def sha256_bytes(data):
    """SHA256 hexadecimal de un bloque de bytes."""
    return hashlib.sha256(data).hexdigest()


def fmt(v):
    """Enteros tal cual; flotantes con seis decimales."""
    return str(v) if isinstance(v, int) else "%.6f" % v


def resumen(vals):
    """Media, desvio muestral, minimo y maximo de una lista no vacia."""
    n = len(vals)
    media = sum(vals) / n
    var = sum((v - media) ** 2 for v in vals) / (n - 1)
    return media, math.sqrt(var), min(vals), max(vals)


def pearson(xs, ys):
    """Correlacion de Pearson entre dos listas del mismo largo."""
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)


def main(argv):
    """Verifica pines, re-ejecuta el verificador y emite los descriptivos."""
    if len(argv) != 5:
        print("uso: auditoria_estricto.py ESTRICTO_JSON RUN_LOG VERIFICADOR VERIF_LOG")
        return 64
    nombres = ("estricto.json", "run.log", "verificar_estricto.py", "verificacion.log")
    datos = {}
    for nombre, ruta in zip(nombres, argv[1:]):
        with open(ruta, "rb") as fh:
            datos[nombre] = fh.read()
        h = sha256_bytes(datos[nombre])
        estado = "OK" if h == PINS[nombre] else "MISMATCH"
        print("pin", nombre, "bytes=%d" % len(datos[nombre]), "sha256=" + h, estado)
        if estado != "OK":
            return 2
    cmd = [sys.executable, argv[3], "--json", argv[1], "--log", argv[2]]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    publicado = datos["verificacion.log"].decode("utf-8")
    igual = proc.stdout != "" and proc.stdout in publicado
    print("verificador re-ejecutado: exit=%d stdout_bytes=%d stdout_sha256=%s igual_al_bloque_publicado=%s stderr_bytes=%d" % (proc.returncode, len(proc.stdout.encode()), sha256_bytes(proc.stdout.encode()), igual, len(proc.stderr.encode())))
    for linea in proc.stdout.splitlines():
        if linea.startswith(("NEGATIVE_REJECTED", "VERIFY_PASS")):
            print("  " + linea)
    if proc.returncode != 0 or not igual:
        return 3
    j = json.loads(datos["estricto.json"])
    print("status=%s mode=%s veredicto=%s holm=%s" % (j["status"], j["mode"], j["H_REUSO_ESTRICTO"], j["holm"]))
    for c in ("flywire", "banc"):
        C = j["connectomes"][c]
        obs = C["observed"]
        nulls = C["nulls"]
        print("== %s nulos=%d semilla=%d estratos=%d" % (c, len(nulls), C["seed"], C["strata"]))
        malos = sum(1 for d in nulls if d["t1"] != d["n_pares_ffi"] / d["n_cab"])
        print("%s identidad_t1 observado=%s nulos_que_fallan=%d" % (c, obs["t1"] == obs["n_pares_ffi"] / obs["n_cab"], malos))
        for campo in CAMPOS:
            vals = [d[campo] for d in nulls]
            media, sd, mn, mx = resumen(vals)
            ge = sum(1 for v in vals if v >= obs[campo])
            le = sum(1 for v in vals if v <= obs[campo])
            print("%s %s real=%s media=%.4f sd=%.4f min=%s max=%s nulos_ge_real=%d nulos_le_real=%d z=%.2f" % (c, campo, fmt(obs[campo]), media, sd, fmt(mn), fmt(mx), ge, le, (obs[campo] - media) / sd))
        t2x_obs = obs["t2"] / obs["n_x"]
        t2x = [d["t2"] / d["n_x"] for d in nulls]
        media, sd, mn, mx = resumen(t2x)
        print("%s t2_por_x real=%.6f media=%.6f min=%.6f max=%.6f nulos_ge_real=%d" % (c, t2x_obs, media, mn, mx, sum(1 for v in t2x if v >= t2x_obs)))
        nc = [d["n_cab"] for d in nulls]
        nf = [d["n_pares_ffi"] for d in nulls]
        print("%s pares_con_plantilla real_menos_media=%.3f" % (c, obs["n_pares_ffi"] - sum(nf) / len(nf)))
        print("%s pearson n_cab_t1=%.4f n_cab_pares=%.4f n_x_t2=%.4f" % (c, pearson(nc, [d["t1"] for d in nulls]), pearson(nc, nf), pearson([d["n_x"] for d in nulls], [d["t2"] for d in nulls])))
        for campo in ("t1", "t2"):
            mx = max(d[campo] for d in nulls)
            me = sum(d[campo] for d in nulls) / len(nulls)
            print("%s margen_%s real_sobre_max=%.4f real_sobre_media=%.4f" % (c, campo, obs[campo] / mx, obs[campo] / me))
        movs = {}
        for d in nulls:
            for k, v in d["guard"]["moved"].items():
                movs.setdefault(k, []).append(v)
        minimos = " ".join("%s=%.6f" % (k, min(v)) for k, v in sorted(movs.items()))
        print("%s guardas_ok=%s movida_minima %s destinos_distintos=%d" % (c, all(d["guard"]["ok"] for d in nulls), minimos, len({d["targets_sha256"] for d in nulls})))
    print("AUDITORIA_DESCRIPTIVOS_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
