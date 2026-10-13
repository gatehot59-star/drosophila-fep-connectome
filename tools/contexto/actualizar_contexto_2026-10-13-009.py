#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-009 (factorial 3 disparado).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-009.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

VIEJA = ("- **Espera decisión de Abraham:** correr el factorial 3 (sellado en `6a7b4cb`: pushear "
         "`results/factorial3_2026-10-13/CORRER`);")
NUEVA = ("- **Factorial 3 disparado (2026-10-13-009).** CORRER `cff2fce` en la rama titan, run 38420175126 de Actions, "
         "81 trabajos (ancla success en 1 min); se estima unas 4 h. El bot commitea logs, json y `agregado.log` en "
         "`results/factorial3_2026-10-13/`.\n"
         "- **Espera:** que termine el factorial 3 y leerlo (REPRODUCE_F2 y REAL_IGUAL primero, despues la primaria);")

R = [
    ("**Última actualización:** 2026-10-13, 12:45 (America/Buenos_Aires), con la respuesta 2026-10-13-008.",
     "**Última actualización:** 2026-10-13, 12:20 (America/Buenos_Aires), con la respuesta 2026-10-13-009."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-008) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-009) · manda sobre el resto"),
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
