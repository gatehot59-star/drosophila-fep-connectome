#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-016 (factorial 4 disparado en Kaggle a pedido de Abraham).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-016.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

R = [
    ("**Última actualización:** 2026-10-13, 21:05 (America/Buenos_Aires), con la respuesta 2026-10-13-015.",
     "**Última actualización:** 2026-10-13, 21:15 (America/Buenos_Aires), con la respuesta 2026-10-13-016."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-015) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-016) · manda sobre el resto"),
    ("- **Factorial 4 sellado en Kaggle (2026-10-13-015), sin correr:**",
     "- **Factorial 4 sellado en Kaggle (2026-10-13-015) y disparado (2026-10-13-016): corriendo y sin leer:**"),
    ("- **Espera decisión de Abraham:** disparar el factorial 4 (unas 7 h de cuota de GPU de `abrahammendieta`); merge ",
     "- **Corriendo:** kernels `f4-ce-a-2026-10-13` y `f4-ce-b-2026-10-13` de `abrahammendieta`, rearmados desde un clon "
     "fresco de `431b7bd` con los md5 sellados (`d76dc652`, `09ffa774`), empujados a las 00:13 UTC del 14-oct a pedido de "
     "Abraham (ClickKit `correr_factorial4_015`) y RUNNING a las 00:14 UTC. Fin estimado entre 03:30 y 04:00 UTC. Al "
     "terminar: `kaggle kernels output` de los dos, `agregar_factorial4.py` y commit del agregado, MD5SUMS y recibos.\n"
     "- **Espera decisión de Abraham:** merge "),
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
