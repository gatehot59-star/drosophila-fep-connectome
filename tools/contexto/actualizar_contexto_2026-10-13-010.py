#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-010 (factorial 3 leido).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-010.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

VIEJA = "- **Espera:** que termine el factorial 3 y leerlo (REPRODUCE_F2 y REAL_IGUAL primero, despues la primaria);"
NUEVA = (
    "- **Factorial 3 leído (2026-10-13-010): VÁLIDO, 81 de 81 trabajos.** Resultados del bot en `09ffbc1` (rama titan), "
    "MD5SUMS 163/163 OK.\n"
    "  - Controles: ancla exacta, plan 600/600 y 50 + 50, TAU_DN_IGUAL, REPRODUCE_F2 exacto en las 90 corridas comunes "
    "con el factorial 2, REAL_IGUAL (0,9465).\n"
    "  - Primaria: R2 0,9353 contra la regla con sus mismos sensores 0,9268; dif +0,85 puntos, IC90 [+0,08; +1,51]: "
    "NO_INFERIOR. H_SUPERA_R2 SIN_DECIDIR. Gana en 482 de 600 corridas. El +1,28 del factorial 2 (3 × 5) bajó a +0,85.\n"
    "  - Nulos (A 0,3, ruido 0,15, τ 0, prueba 2): real 0,9465; SL media 0,666 (máx 0,796); T media 0,760 (máx 0,839); "
    "ninguno de los 100 iguala al real; p 0,0196 cada uno (el mínimo posible con 50), Holm 0,039: H_CABLEADO_R2 SOSTENIDA.\n"
    "  - Lectura: el cableado real de R2 pesa mucho (15 a 28 puntos sobre sus barajados) y alcanza a la regla con sus "
    "mismos sensores, con una ventaja chica (menos de un punto) que no pasa el margen.\n"
    "- **Espera decisión de Abraham:** qué sigue tras el factorial 3;"
)
R = [
    ("**Última actualización:** 2026-10-13, 12:20 (America/Buenos_Aires), con la respuesta 2026-10-13-009.",
     "**Última actualización:** 2026-10-13, 16:05 (America/Buenos_Aires), con la respuesta 2026-10-13-010."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-009) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-010) · manda sobre el resto"),
    (VIEJA, NUEVA),
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
