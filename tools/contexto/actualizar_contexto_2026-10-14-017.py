#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-017 (los dos reales completos de H_DEBILES dieron exacto).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-017.py docs/agents/CONTEXTO-drosophila-fep.md
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

R = [
    ("**Última actualización:** 2026-10-14, 17:15 (America/Buenos_Aires), con la respuesta 2026-10-14-016.",
     "**Última actualización:** 2026-10-14, 17:27 (America/Buenos_Aires), con la respuesta 2026-10-14-017."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-016) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-017) · manda sobre el resto"),
    ("Antes del CORRER, los reales a tamano completo del humo tienen que dar 0,9465 y 0,9135.",
     q("Los reales a tamano completo dieron exacto en Actions (bot @@ca8221a@@, 2026-10-14-017): R2 0,9465 y nucleo "
       "0,9135, REAL_R2_IGUAL y REAL_NUCLEO_IGUAL True; la condicion del CORRER esta cumplida.")),
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
