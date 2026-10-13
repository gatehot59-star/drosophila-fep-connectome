#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-014 (F05 suavizado; la v2 queda lista para depositar).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-014.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

R = [
    ("**Última actualización:** 2026-10-13, 17:50 (America/Buenos_Aires), con la respuesta 2026-10-13-013.",
     "**Última actualización:** 2026-10-13, 18:45 (America/Buenos_Aires), con la respuesta 2026-10-13-014."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-013) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-014) · manda sobre el resto"),
    ("**F05 sigue abierto:** el resumen y las conclusiones usan +14,8σ como firme (10 apariciones).",
     "**F05 suavizado en la 2026-10-13-014** (pedido de Abraham, 18:17): `tools/v2/fix_v2_f05_2026-10-13.py` "
     "(`da4ace2d…`, 9 reemplazos: resumen, contribuciones, 3.7, discusión, conclusiones, cambio 16 y metadatos de Zenodo), "
     "aplicado por el bot en `608bd41` (manuscrito `a4d09d2c…`, igual al de la prueba en brain-env); el +14,8σ y la Tabla 8 "
     "se conservan como observación sobre cinco realizaciones, sin reproducir. **La v2 queda lista para depositar:** PDF "
     "`6e849bf2…` (18 páginas), erratum `05052e6e…`, json `0ed096b5…`, `--verificar` PASS en clon fresco de `e7fd359` y "
     "FAIL con el PDF anterior; los PDF están en `/workspace/v2cierre_2026-10-13/deposito_f05/` de brain-env."),
    ("decidir F05 (suavizar el +14,8σ en el resumen y las conclusiones, o intentar reproducir la Tabla 8); merge del PR #27",
     "merge del PR #27 (la v2 ya está lista, 2026-10-13-014)"),
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
