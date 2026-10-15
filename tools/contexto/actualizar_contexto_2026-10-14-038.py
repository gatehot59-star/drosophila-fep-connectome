#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-038 (H_LECTOR medido en Actions).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-038.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_038 = q(
    "- **H_LECTOR medido en Actions (2026-10-14-038, ClickKit @@correr_lector_038@@, 13:50):** CORRER @@2df0961@@, "
    "bot @@8d305e9@@ (@@results/lector_2026-10-15/@@, agregado.log md5 8f2f4392, MD5SUMS 68 de 68 OK). Todos los "
    "controles VALIDO. H_LECTOR_CERCA SOSTENIDA: D1 = WL - RIDGE = -0,0029 [-0,0038, -0,0020], con 240 rasgos contra "
    "22.560. H_LECTOR_PAGA SOSTENIDA: D2 = WL - W = +0,0474 [+0,0454, +0,0493]. H_LECTOR_CABLEADO SOSTENIDA: el real "
    "le gana a los 40 nulos en las 4 combinaciones (p = 1/41 = 0,0244 en todas): SL c2 +0,0337, SL c5 +0,1194, T c2 "
    "+0,0450, T c5 +0,1111. Contra la expectativa declarada en el sello. Falta la replica de la primaria en brain-env "
    "(si difiere, NO_SE_REPLICA). Abierto para auditoria: la tau de semilla 10 se eligio en H_TAU sobre la red real y "
    "los nulos la heredan sin eleccion propia.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 13:46 (America/Buenos_Aires), con la respuesta 2026-10-14-037.",
     "**Última actualización:** 2026-10-15, 16:50 (America/Buenos_Aires), con la respuesta 2026-10-14-038."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-037) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-038) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_038 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    (q("disparar el @@CORRER@@ de H_LECTOR, 22 trabajos en Actions, unas 2 horas (2026-10-14-037); "),
     q("auditar H_LECTOR (sobre todo la tau elegida en la red real) y decidir si entra al Paper 2; la replica de la "
       "primaria corre en brain-env despues de la de H_RIVAL (2026-10-14-038); ")),
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
