#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-037 (instrumento y humo de H_LECTOR).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-037.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_037 = q(
    "- **Instrumento y humo de H_LECTOR (2026-10-14-037, ClickKit @@instrumento_lector_037@@ y @@cerrar_037@@):** "
    "rama @@titan/lector-2026-10-15@@, sello @@8e65e05@@ sin editar. Instrumento: @@tools/lector/lector_mosca.py@@ "
    "(5b7fb79e), @@agregar_lector.py@@ (8b003a44), @@prueba_lector.py@@ (d697ed32), workflows @@lector-humo.yml@@, "
    "@@lector-mosca.yml@@ (22 trabajos, 612745d3) y @@lector-prueba.yml@@. Humo ciego en Actions (run 38752555880, "
    "bot @@b1cb491@@): las 6 celdas VALIDO con REPRO_W 10/10, REPRO_RIDGE 10/10 y CONTROL_NEGATIVO 0,5000 contra azar "
    "0,5000; en c0 CONTROL_LECTOR_CRUDO 2000/2000 iguales al RIDGE de H_RIVAL (lambda 10); rutas de nulo SL (4.030.551 "
    "destinos cambiados) y T (423 tipos) VALIDO e iguales al factorial 3. La prueba cayo en ese run porque "
    "@@prueba_lector.py@@ no estaba en el commit que disparo (error de orden de push, declarado) y se reintento sola: "
    "13/13 OK en Actions (bot @@c6b1a63@@, log md5 a3b800b5, con los mismos md5 de los tres scripts). Ningun acierto de L se imprimio. Celdas de 50 a 60 min en Actions.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 09:58 (America/Buenos_Aires), con la respuesta 2026-10-14-036.",
     "**Última actualización:** 2026-10-15, 13:46 (America/Buenos_Aires), con la respuesta 2026-10-14-037."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-036) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-037) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_037 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    (q("escribir el instrumento de H_LECTOR y su humo ciego, y despues su @@CORRER@@ (2026-10-14-036); "),
     q("disparar el @@CORRER@@ de H_LECTOR, 22 trabajos en Actions, unas 2 horas (2026-10-14-037); ")),
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
