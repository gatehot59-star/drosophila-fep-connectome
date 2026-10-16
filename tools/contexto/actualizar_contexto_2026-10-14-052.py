#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-052 (sintesis en criollo de la mosca entera y los tres papers).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-052.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_052 = q(
    "- **Sintesis en criollo de la mosca entera y los tres papers (2026-10-14-052, pregunta de Abraham 11:41):** lo "
    "logrado de la 045 a la 051 es el cerebro entero con SparseLTC al lado de una vara externa, el LIF de Shiu "
    "reproducido exacto. El mapa de quien se prende pasa dos veces contra 80 barajados (J 0,366 y 0,332); MN9, motora "
    "de ingestion (nervio faringeo en las anotaciones), queda REFUTADA sin umbral y SIN_DECIDIR con umbral; la "
    "compuerta liquida y el umbral no pagan; destilacion cerrada. Coincide con el modelo validado, no con la mosca "
    "viva. Paper 1: vara externa, ningun numero cambia, nada sobre la amplificacion temporal. Paper 2: capitulo nuevo "
    "(segundo reflejo, cerebro entero, vara validada). Paper 3: de costado (MN9 es una motora de la boca, donde el "
    "central tiene plus propio; el camino por el central NO MEDIDO). Aplicaciones: simulador barato de reclutamiento "
    "(3,7 s por corrida, 2,25 GB) y el banco sellado contra un modelo externo; compresion y reflejos para el borde, "
    "sin cambios.%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 11:35 (America/Buenos_Aires), con la respuesta 2026-10-14-051.",
     "**Última actualización:** 2026-10-16, 11:55 (America/Buenos_Aires), con la respuesta 2026-10-14-052."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-051) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-052) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_052 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
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
