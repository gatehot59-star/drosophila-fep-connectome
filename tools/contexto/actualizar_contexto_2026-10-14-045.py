#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-045 (la mosca entera con liquidas necesita una vara externa).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-045.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

BT = chr(96)
NL = chr(10)


def q(s):
    return s.replace("@@", BT).replace("%%", NL)


ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

NUEVO_045 = q(
    "- **La mosca entera con liquidas (2026-10-14-045, intuicion de Abraham 23:01):** la mitad de la intuicion ya "
    "tiene respaldo medido: el motivo de 28 llevaba el 2,96% de la entrada de sus descendentes y nada de su inhibicion "
    "(2026-10-12-011), y con R2 (33.489 neuronas) el cableado le gano a sus barajados (H_LECTOR_CABLEADO y "
    "H_TAU_LIBRE). La otra mitad pide una vara externa: el conectoma no trae tau, umbrales, neuromodulacion ni "
    "plasticidad, y sin medicion de la mosca las propiedades no se distinguen del lector. Vara propuesta: Shiu et al. "
    "2024 (LIF del cerebro entero, azucar a MN9 validado con optogenetica; con pesos barajados 1 de 100 contra 100%), "
    "codigo publico (@@philshiu/Drosophila_brain_model@@) y nuestro parquet con sus columnas y su signo (md5 contra el "
    "original NO MEDIDO). Plan: Shiu como referencia, la liquida en el cerebro entero con su estimulo y su lectura, "
    "nulos de pesos, grado y region, y recien entonces destilar el subgrafo minimo. Nada corrido.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 22:30 (America/Buenos_Aires), con la respuesta 2026-10-14-044.",
     "**Última actualización:** 2026-10-15, 23:10 (America/Buenos_Aires), con la respuesta 2026-10-14-045."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-044) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-045) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_045 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); si se sella la mosca entera con liquidas con Shiu como vara (2026-10-14-045); "),
]
for a, b in R:
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
