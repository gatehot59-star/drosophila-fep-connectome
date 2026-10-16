#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-053 (comparacion con Shiu y Lappalainen).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-053.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_053 = q(
    "- **Contra Shiu y Lappalainen (2026-10-14-053, pedido de Abraham 12:08):** con Shiu compartimos archivo, "
    "codigo, estimulo y lectura, y lo reprodujimos (30 de 30 a 100 Hz, 0 de 20 barajados; el reporta 100% contra 1 de "
    "100). Con nuestra tasa sale su mapa (172 de 321) y no su motora. Contra el barajado que uso Shiu (pesos), con "
    "umbral MN9 queda en cero en los 40 SHUF_W; lo que frena es SHUF_G, un nulo que no esta en su texto principal. Lappalainen predice "
    "actividad registrada (64 tipos, 45.669 neuronas, 734 parametros por tipo, 26 estudios); coincidimos en que el "
    "cableado restringe la funcion, no en la vara (nuestro H4 no llego). La liquida no podia pagar en la mosca entera "
    "porque la lectura del azucar es un estado estable; hace falta una tarea temporal. Corrige la 2026-10-13-013: los "
    "parametros de Lappalainen son por tipo, no por neurona. Propuesta sin sellar: el LIF de Shiu sobre los 40 "
    "SHUF_G.%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 11:55 (America/Buenos_Aires), con la respuesta 2026-10-14-052.",
     "**Última actualización:** 2026-10-16, 12:20 (America/Buenos_Aires), con la respuesta 2026-10-14-053."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-052) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-053) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_053 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("H_ENTERA_UMBRAL se escriben como estan en el Paper 2 (2026-10-14-051); ",
     "H_ENTERA_UMBRAL se escriben como estan en el Paper 2 (2026-10-14-051); si se sella correr el LIF de Shiu sobre "
     "los 40 SHUF_G, el nulo que no esta en su texto principal y que freno a MN9 (2026-10-14-053); "),
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
