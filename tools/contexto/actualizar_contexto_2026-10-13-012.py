#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-012 (render y verificacion de la v2 desde 1f4a2e0).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-012.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

R = [
    ("**Última actualización:** 2026-10-13, 16:15 (America/Buenos_Aires), con la respuesta 2026-10-13-011.",
     "**Última actualización:** 2026-10-13, 17:30 (America/Buenos_Aires), con la respuesta 2026-10-13-012."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-011) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-012) · manda sobre el resto"),
    ("Falta el render desde `1f4a2e0`, el json de depósito y `--verificar`.",
     "**Cerrado en la 2026-10-13-012:** render desde `1f4a2e0` PASS (manuscrito 18 páginas `a22515e9…`, erratum 15 "
     "páginas `05052e6e…`, en `/workspace/v2cierre_2026-10-13/deposito_013/` de brain-env), json de depósito `55f3ec63…` "
     "y `--verificar` PASS en clon fresco de `e81a903`; con el PDF viejo da FAIL. En el PDF: «Sufficient» 1 → 0, "
     "«138,140» 0 → 1, «1/6» 0 → 2. **F05 sigue abierto:** el resumen y las conclusiones usan +14,8σ como firme (10 apariciones)."),
    ("cerrar el render y la verificación de la v2 (F01, F06 y F07 ya aplicados en `1f4a2e0`); decidir F05 (Tabla 8);",
     "decidir F05 (suavizar el +14,8σ en el resumen y las conclusiones, o intentar reproducir la Tabla 8);"),
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
