#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-011 (sintesis en criollo, reemplaza a la 003).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-011.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

LECT_V = ("  - Lectura: el cableado real de R2 pesa mucho (15 a 28 puntos sobre sus barajados) y alcanza a la regla con sus "
          "mismos sensores, con una ventaja chica (menos de un punto) que no pasa el margen.")
LECT_N = ("  - Lectura: el cableado real de R2 pesa mucho (19 a 28 puntos sobre el promedio de sus barajados, 11 a 15 sobre el "
          "mejor; el «15 a 28» de la 010 mezclaba las dos cosas, corregido en la 011) y alcanza a la regla con sus mismos "
          "sensores, con una ventaja chica (menos de un punto) que no pasa el margen.")
ESP_V = "- **Espera decisión de Abraham:** qué sigue tras el factorial 3;"
ESP_N = (
    "- **Síntesis en criollo (2026-10-13-011), reemplaza a la 003.**\n"
    "  - El cableado real pesa en las tres escalas: M46, R1 y R2 les ganan a sus barajados.\n"
    "  - Contra el diseño de la mosca con los mismos sensores, M46 y R1 quedan abajo (−0,6 a −1,8 puntos) y sólo R2 "
    "(33.489 neuronas) lo alcanza (+0,85, sin pasar el margen). La 003 decía que alcanzaba con 1.504: lo corrigió la 007.\n"
    "  - Para un robot conviene el plano (la regla tipo de sensor → comando), no el cableado completo: rinde casi lo mismo "
    "y es mucho más barato.\n"
    "  - Posición frente a la literatura: Shiu et al. (Nature 2024, el mismo archivo de conectividad) y Lappalainen et al. "
    "(Nature 2024) predicen actividad y la validan; acá la pregunta es otra (el cableado contra su propio diseño) y no hay "
    "nada medido fuera de simulación.\n"
    "  - Lo más cerca de cerrar es la v2 del Paper 1; las tres escalas son material para el Paper 2.\n"
    "- **Espera decisión de Abraham:** qué sigue tras el factorial 3;"
)
R = [
    ("**Última actualización:** 2026-10-13, 16:05 (America/Buenos_Aires), con la respuesta 2026-10-13-010.",
     "**Última actualización:** 2026-10-13, 16:15 (America/Buenos_Aires), con la respuesta 2026-10-13-011."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-010) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-011) · manda sobre el resto"),
    (LECT_V, LECT_N),
    (ESP_V, ESP_N),
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
