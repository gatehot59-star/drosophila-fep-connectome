#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-054 (sello H_LIF_SHUFG, nada corrido).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-054.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_054 = q(
    "- **Sello H_LIF_SHUFG (2026-10-14-054, pedido de Abraham 12:40):** en la rama, "
    "@@tools/mosca_entera/SELLO-LIF-SHUFG-054.md@@ (307db84, md5 9e7e25f7), nada corrido. El LIF de Shiu sin cambios "
    "sobre los mismos 40 SHUF_G de la 049 y la 051 (10 ensayos cada uno) mas el real de 30 como control (27 de 30), con "
    "NULO_MISMO (radio crudo igual al de la 049, tolerancia 1e-6). Bandas de H_UMB_MN9 con dos criterios: el de Shiu "
    "(MN9 en 5 o mas de 10 ensayos, H_LIF_G_SHIU) y el nuestro (tasa de MN9 igual o mayor que la del real, "
    "H_LIF_G_VARA); k32 aparte (H_LIF_K32), con lectura fijada en cuatro casos. No cambia veredictos sellados. "
    "Expectativa escrita: k32 no llega (80%), porque en las tres lecturas de la tasa la entrada de MN9 en k32 es "
    "0,00348, unas 11 sinapsis directas desde el azucar, que en el LIF dan 1,5 mV de los 7 que faltan al umbral.%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 12:20 (America/Buenos_Aires), con la respuesta 2026-10-14-053.",
     "**Última actualización:** 2026-10-16, 13:10 (America/Buenos_Aires), con la respuesta 2026-10-14-054."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-053) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-054) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_054 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("si se sella correr el LIF de Shiu sobre los 40 SHUF_G, el nulo que no esta en su texto principal y que freno a "
     "MN9 (2026-10-14-053); ",
     "el instrumento del sello H_LIF_SHUFG (@@lif_shufg.py@@, agregado y prueba) con prueba y humo, y despues CORRER "
     "(2026-10-14-054); "),
    ("si se mira por que el nulo SHUF_G k32 llega a MN9 (descriptivo, no cambia veredictos) o H_MOSCA_ENTERA y "
     "H_ENTERA_UMBRAL se escriben como estan en el Paper 2 (2026-10-14-051); ",
     "si H_MOSCA_ENTERA y H_ENTERA_UMBRAL se escriben como estan en el Paper 2 (2026-10-14-051; el por que de k32 "
     "entra como descriptivo en el sello 054, con n1, D1+ y D2+); "),
]
for a, b in R:
    b = q(b)
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
