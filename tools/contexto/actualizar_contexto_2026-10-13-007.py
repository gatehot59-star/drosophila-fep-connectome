#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-006 (F01, F06 y F07 aplicados) y la 007 (factorial 2 leido).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-007.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

NUEVO = (
    "- **Factorial 2 corrido (2026-10-13-007): VÁLIDO, 29/29 trabajos, ancla exacta.** Corrida `38396946950`, resultados "
    "del bot `798ed97`, 55 min (R2 hasta 31,5 min por trabajo). Diferencia contra la regla con los mismos sensores, "
    "margen 0,01:\n"
    "  - M46_TASA −0,62 puntos (NO_SUPERIOR); M46_LIQ −1,83 (PIERDE).\n"
    "  - R1, las cuatro configuraciones, entre −1,02 y −1,48 puntos (NO_SUPERIOR); en R1_CON_LIQ y R1_SIN_TASA el "
    "intervalo excluye el cero. **Corrige la 002 y la 003:** con 100 corridas por configuración, R1 no alcanza a su "
    "diseño; queda alrededor de un punto abajo.\n"
    "  - **R2_CON_TASA (33.489 neuronas): +1,28 puntos, IC [+0,79; +1,77], NO_INFERIOR**, positiva en las 6 celdas "
    "(SUPERA en amplitud 0, ruido 0,15). Es la primera vez que el cableado le gana a su diseño con los mismos sensores, "
    "pero por menos del margen: H_SUPERA no sostenida según lo sellado. R2 tiene 3 × 5 semillas.\n"
    "  - Más sensores pagan: la regla de 418 le gana a la de 40 por +2,79 (AYUDA). R2 menos R1: +1,65 (NO_INFERIOR). "
    "LIQ: peor en M46 (−1,21) y equivalente en R1. Inhibición: sin efecto claro.\n"
    "- **F01, F06 y F07 aplicados en el PR #27 (2026-10-13-006):** bot `1f4a2e0`, manuscrito `2fa575c4…`, sección de dos "
    "saltos `23db9cac…`; render de prueba PASS, 18 páginas, `a22515e9…`. Falta el render desde `1f4a2e0`, el json de "
    "depósito y `--verificar`.\n"
)
VIEJA = ("- **Espera decisión de Abraham:** correr el factorial 2 (sellado en `9442fdf`: pushear "
         "`results/factorial2_2026-10-13/CORRER`); aplicar F01, F06 y F07 a la v2 y decidir F05 (Tabla 8);")
NUEVA = NUEVO + ("- **Espera decisión de Abraham:** replicar R2 con 10 × 10 semillas (factorial 3, para decidir si "
                 "SUPERA); cerrar el render y la verificación de la v2 (F01, F06 y F07 ya aplicados en `1f4a2e0`); "
                 "decidir F05 (Tabla 8);")

R = [
    ("**Última actualización:** 2026-10-13, 09:40 (America/Buenos_Aires), con la respuesta 2026-10-13-005.",
     "**Última actualización:** 2026-10-13, 11:55 (America/Buenos_Aires), con la respuesta 2026-10-13-007."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-005) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-007) · manda sobre el resto"),
    ("- **Factorial 2 sellado (2026-10-13-004), sin disparar.**",
     "- **Factorial 2 sellado (2026-10-13-004) y corrido (2026-10-13-007, abajo).**"),
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
