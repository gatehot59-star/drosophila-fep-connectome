#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-044 (Paper 3: la pregunta ya la respondio BANC; lo propio es el nulo).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-044.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_044 = q(
    "- **Literatura del Paper 3 (2026-10-14-044, Abraham eligio seguir con el Paper 3, 22:24):** la pregunta ya la "
    "responde BANC (Bates et al., Nature 2026: los efectores dependen sobre todo de sensoriales locales, unidos por "
    "ascendentes y descendentes); las redes de descendentes estan en Braun et al. (Nature 2024) y el atlas en Sturner "
    "et al. (Nature 2025). Leidos solo resumenes y la introduccion de BANC. Lo propio es el nulo de tamano y region. "
    "Tension medida: con el nulo regional la entrada sensorial directa a las motoras del cerebro sale BAJO el azar "
    "(firme en la 007, BY 0,01393, max-T 0,27854). Recomendacion: reencuadrar el Paper 3 como prueba con nulo "
    "regional de los lazos locales de BANC, con la replica en BANC v888 como corrida central. Esqueleto: §1, nota de "
    "relevancia y checklist, cotejo 130 de 130 (md5 dd9aa7c3).%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 22:22 (America/Buenos_Aires), con la respuesta 2026-10-14-043.",
     "**Última actualización:** 2026-10-15, 22:30 (America/Buenos_Aires), con la respuesta 2026-10-14-044."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-043) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-044) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_044 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); si el Paper 3 se reencuadra como prueba con nulo regional de BANC (2026-10-14-044); "),
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
