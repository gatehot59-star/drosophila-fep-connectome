#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-026 (Topo v0.2, salida diferencial).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-026.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO = q(
    "- **Topo v0.2, salida diferencial (2026-10-14-026, ClickKit @@topo_v02_diferencial_025@@, 20:22):** rama "
    "@@titan/topo-v02-2026-10-14@@ (@@a817ad3@@, @@docs/topo/TOPO-v0.2-diferencial.md@@). @@topo_v02.py@@ envuelve "
    "topo.py y topo_grafo.py sin cambiarlos y agrega @@linea ... -> interna@@ y @@compara NOMBRE = A - B ... -> ACCION@@. "
    "@@escape_dif.topo@@: las DNp06 leen su lado y el giro sale de comparar izquierda contra derecha; chequeo FlyWire "
    "CABLEADA=10 AGUAS_ABAJO=4 (el que resta daba SIN_VIA_DIRECTA=4). Pruebas 9/9, reproducidas desde un clon limpio: "
    "por linealidad escape_dif da exactamente lo mismo que escape.topo (800 de 800, umbrales bit a bit), asi que no se "
    "sella una prueba de banco (no podria dar rojo). El falsador queda en el cordon nervioso: H_COMPARADOR en BANC "
    "(salidas de DNp06 izquierda y derecha con signo opuesto sobre motoneuronas de vuelo de un lado), sin sellar.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 20:25 (America/Buenos_Aires), con la respuesta 2026-10-14-025.",
     "**Última actualización:** 2026-10-14, 20:30 (America/Buenos_Aires), con la respuesta 2026-10-14-026."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-025) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-026) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    ("confirmar H_FRENO en Actions; decidir si Topo v0.2 lleva una salida que compare las dos DNp06, aguas abajo, "
     "y si se sella contra el programa que resta (2026-10-14-025); ",
     "confirmar H_FRENO en Actions; sellar H_COMPARADOR en BANC, el falsador de Topo v0.2 (2026-10-14-026); "),
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
