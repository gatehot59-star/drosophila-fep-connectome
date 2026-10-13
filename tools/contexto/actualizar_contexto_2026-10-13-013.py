#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-013 (informe detallado: logros, otros autores, relevancia y escala).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-013.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

ESP = "- **Espera decisión de Abraham:** qué sigue tras el factorial 3;"
NUEVO = (
    "- **Informe detallado (2026-10-13-013):** logros, contraste con Shiu, Lappalainen, Costi, Suárez, Lechner, "
    "Vaxenburg y NeuroMechFly (doi en la respuesta), relevancia y escala.\n"
    "  - Relevante en un nicho y por el método; para publicar: preprint de métodos (opinión, no medición).\n"
    "  - Escala: el cerebro entero (138.639 neuronas, 15.091.983 conexiones) costaría unas 3,7 veces R2 si el costo sigue a "
    "las conexiones (NO MEDIDO); BANC trae `fafb_783_match_id` y es el segundo conectoma natural (NO MEDIDO).\n"
    "  - La novedad («nadie comparó el cableado contra el plano del animal con los mismos sensores») es de búsqueda acotada: "
    "NO MEDIDO hasta una revisión sistemática.\n"
)
R = [
    ("**Última actualización:** 2026-10-13, 17:30 (America/Buenos_Aires), con la respuesta 2026-10-13-012.",
     "**Última actualización:** 2026-10-13, 17:50 (America/Buenos_Aires), con la respuesta 2026-10-13-013."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-012) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-013) · manda sobre el resto"),
    (ESP, NUEVO + ESP),
]
for a, b in R:
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
for a, b in R:
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
