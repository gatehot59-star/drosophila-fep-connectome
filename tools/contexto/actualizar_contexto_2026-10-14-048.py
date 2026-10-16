#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-048 (enmienda sellada de H_MOSCA_ENTERA).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-048.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_048 = q(
    "- **Enmienda de H_MOSCA_ENTERA sellada (2026-10-14-048, Abraham 00:48):** @@tools/mosca_entera/ENMIENDA-048.md@@ "
    "en @@titan/mosca-entera-2026-10-15@@ (@@778dc10@@, md5 022dbbdd), antes de CORRER. No mueve nada de la 046; "
    "agrega la marca REFUTADA_DEGENERADA para H_ENTERA_LIQ, H_ENTERA_LAT (Spearman de latencias contra el LIF, "
    "D_LAT >= +0,05 sostenida, <= 0 refutada) y H_ENTERA_MN9_G1 y _CONJUNTO_G1 contra los mismos 80 nulos con el "
    "factor del real. Lectura conjunta fijada: perder contra los nulos a 0,9 y ganar contra los G1 se lee como "
    "ganancia en lazos, no ruteo. Ningun veredicto medido.%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 00:30 (America/Buenos_Aires), con la respuesta 2026-10-14-047.",
     "**Última actualización:** 2026-10-16, 00:52 (America/Buenos_Aires), con la respuesta 2026-10-14-048."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-047) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-048) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_048 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("sellar la enmienda de H_MOSCA_ENTERA (lectura por latencia y nulos a ganancia igual) antes de CORRER, o "
     "CORRER como esta sellada (2026-10-14-047); ",
     "el instrumento de la enmienda de H_MOSCA_ENTERA con prueba y humo, y despues CORRER (2026-10-14-048); "),
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
