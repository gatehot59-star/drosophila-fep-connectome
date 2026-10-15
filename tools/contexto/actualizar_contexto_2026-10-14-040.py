#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-040 (instrumento y humo de H_TAU_LIBRE).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-040.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_040 = q(
    "- **Instrumento y humo de H_TAU_LIBRE (2026-10-14-040, ClickKit @@instrumento_taulibre_040@@, 18:47):** rama "
    "@@titan/taulibre-2026-10-15@@, sello @@fec8472@@ sin editar. Instrumento en un solo commit con el disparo "
    "(@@930f0d7@@): @@tools/taulibre/taulibre_mosca.py@@ (c65bebe2, importa @@lector_mosca.py@@ sin cambios), "
    "@@agregar_taulibre.py@@ (340dc41a), @@prueba_taulibre.py@@ (9f74f63d), workflows @@taulibre-humo.yml@@ y "
    "@@taulibre-mosca.yml@@ (20 trabajos). Humo en Actions (run 38816081787, bot @@c3e07cd@@): todo VALIDO; "
    "REPRO_LECTOR reproduce el real de H_LECTOR caracter por caracter en c2 (0,9910, lambda 0,001) y c5 (0,9930, "
    "lambda 0,01); NULOS_IGUAL_LECTOR 40 de 40 grafos SL en c2 y 40 de 40 T en c5; TAU_FRESCA; CONTROL_NEGATIVO en el "
    "azar; prueba 11/11. Ningun acierto nuevo se imprimio.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 18:44 (America/Buenos_Aires), con la respuesta 2026-10-14-039.",
     "**Última actualización:** 2026-10-15, 19:31 (America/Buenos_Aires), con la respuesta 2026-10-14-040."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-039) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-040) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_040 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    (q("escribir el instrumento de H_TAU_LIBRE y su humo ciego, y despues su @@CORRER@@; H_LECTOR entra al Paper 2 "
       "recien con H_TAU_LIBRE y la replica de la primaria en brain-env (2026-10-14-039); "),
     q("disparar el @@CORRER@@ de H_TAU_LIBRE, 20 trabajos en Actions, unas 2 horas; H_LECTOR entra al Paper 2 recien "
       "con H_TAU_LIBRE y la replica de la primaria en brain-env (2026-10-14-040); ")),
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
