#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-008 (factorial 3 sellado).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-008.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

NUEVO = (
    "- **Factorial 3 sellado (2026-10-13-008), sin disparar.** Rama `titan/factorial3-mosca-2026-10-13`, sello `6a7b4cb`.\n"
    "  - Grilla: R2_CON_TASA con τ 0..9 × prueba 2..11 × 6 celdas, con `factorial2_mosca.py` sin cambios (`798a824c…`).\n"
    "  - Nulos: 50 SL y 50 T de R2 (`tools/factorial3/nulos_r2.py`, `c4f1c4d3…`) en A 0,3, ruido 0,15, τ 0, prueba 2.\n"
    "  - Agregador `agregar_factorial3.py` (`2ec8cd03…`): margen 0,01, IC al 90 % (TOST); Holm sobre los dos nulos.\n"
    "  - Hipótesis: H_SUPERA_R2 (gana por más de un punto) y H_CABLEADO_R2 (le gana a sus barajados).\n"
    "  - Controles nuevos: REPRODUCE_F2 (las 90 corridas comunes con el factorial 2), REAL_IGUAL (el script de nulos "
    "reproduce la grilla) y SL_IGUAL_MODULO (el barajado numpy da lo mismo que `base.barajar_sl`).\n"
    "  - Humo en brain-env: 3/3 VÁLIDO; REAL_IGUAL y SL_IGUAL_MODULO True. 81 trabajos; se estima unas 4 h en Actions.\n"
)
VIEJA = ("- **Espera decisión de Abraham:** replicar R2 con 10 × 10 semillas (factorial 3, para decidir si "
         "SUPERA);")
NUEVA = NUEVO + ("- **Espera decisión de Abraham:** correr el factorial 3 (sellado en `6a7b4cb`: pushear "
                 "`results/factorial3_2026-10-13/CORRER`);")

R = [
    ("**Última actualización:** 2026-10-13, 11:55 (America/Buenos_Aires), con la respuesta 2026-10-13-007.",
     "**Última actualización:** 2026-10-13, 12:45 (America/Buenos_Aires), con la respuesta 2026-10-13-008."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-007) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-008) · manda sobre el resto"),
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
