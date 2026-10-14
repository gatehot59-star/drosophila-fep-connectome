#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-015 (lectura completa del nucleo; H_TAU y H_TOPO_NUEVO volvieron).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-015.py docs/agents/CONTEXTO-drosophila-fep.md
Las comillas invertidas y los saltos se arman con chr() para que el archivo no lleve caracteres de escape.
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
    "- **Lectura del nucleo y dos veredictos nuevos (2026-10-14-015):**%%"
    "  - Nucleo: pierde contra R2 en las 10 semillas de tau (-3,06 a -5,81 puntos) y mas con ruido 0,45 que con 0,15 "
    "en las 3 amplitudes (media -5,59 contra -3,59; post hoc). Con el 14,96 % de las aristas conserva cerca del 88 % "
    "de la ventaja de R2 sobre sus barajados SL (post hoc, cruza el factorial 3). Falta H_DEBILES: si las aristas "
    "debiles pesan por especificas o por cantidad.%%"
    "  - H_TAU SOSTENIDA (bot @@2d4dbfb@@): con tau elegida por validacion cruzada (semilla 10 en las 6 celdas), R2 "
    "le gana a su regla por +1,78 puntos, IC90 [+1,45; +2,13], SUPERA en las 6 celdas y en 60 de 60 corridas. "
    "Primera vez que el cableado supera al diseno por el margen. Letra chica: el cableado tuvo 10 sorteos de tau para "
    "elegir y la regla ninguna perilla (H_TAU_JUSTO, sin sellar).%%"
    "  - H_TOPO_NUEVO SOSTENIDA (bot @@46929db@@): el cableado le gana a 300 SL y 300 T en las 6 celdas (Holm "
    "0,0399) y la regla nueva no pierde contra el cableado (+1,68 puntos, IC90 [+0,99; +2,38]). Letra chica "
    "(descriptivo): la regla vieja le gana a la nueva en 5 de 6 celdas; la nueva arregla la barra AD pero rompe el "
    "aterrizaje ante la barra AA.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 13:35 (America/Buenos_Aires), con la respuesta 2026-10-14-014.",
     "**Última actualización:** 2026-10-14, 16:30 (America/Buenos_Aires), con la respuesta 2026-10-14-015."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-014) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-015) · manda sobre el resto"),
    ("solo con su sí); leer H_TOPO_NUEVO cuando termine (2026-10-14-014); la lectura completa del núcleo; leer H_TAU "
     "cuando termine (2026-10-14-004); el nulo",
     "solo con su sí); sellar H_DEBILES y H_TAU_JUSTO, y una segunda versión del programa de la barra (2026-10-14-015); "
     "el nulo"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); sellar H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); sellar H_DEBILES"),
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
