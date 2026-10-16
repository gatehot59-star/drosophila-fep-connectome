#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-046 (sello de H_MOSCA_ENTERA con Shiu como vara).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-046.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_046 = q(
    "- **H_MOSCA_ENTERA sellada (2026-10-14-046, Abraham 23:15):** sello en @@titan/mosca-entera-2026-10-15@@ "
    "(@@500f66d@@, @@tools/mosca_entera/SELLO-MOSCA-ENTERA.md@@ md5 55bc4c76). Medido para el sello: nuestro parquet "
    "es byte a byte el @@Connectivity_783.parquet@@ de Shiu (mismo git blob d386555d); 20 de los 21 sensores de azucar "
    "de Shiu existen en v783 y MN9 tambien. Brazos: LIF de Shiu sin cambios, la liquida de H_LECTOR en las 138.639 "
    "neuronas, la misma sin termino liquido y un rival de proximidad sin dinamica; nulos de pesos y de destinos (40 "
    "cada uno); control REPRO_SHIU; hipotesis H_ENTERA_MN9, _CONJUNTO, _RIVAL y _LIQ con bandas. Maquina: Actions "
    "(brain-env sin brian2 y ocupada). El primer commit del sello decia 23:40 adelantado: corregido y declarado. "
    "Falta instrumento, prueba y humo.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 23:10 (America/Buenos_Aires), con la respuesta 2026-10-14-045.",
     "**Última actualización:** 2026-10-15, 23:30 (America/Buenos_Aires), con la respuesta 2026-10-14-046."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-045) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-046) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_046 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); el instrumento de H_MOSCA_ENTERA en Actions (2026-10-14-046); "),
    ("si se sella la mosca entera con liquidas con Shiu como vara (2026-10-14-045); ", ""),
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
