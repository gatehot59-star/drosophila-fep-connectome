#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-042 (replica de H_LECTOR lanzada y H_RIVAL cotejado).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-042.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_042 = q(
    "- **H_RIVAL replicado en brain-env y replica de H_LECTOR lanzada (2026-10-14-042, pedido de Abraham 21:51):** la "
    "replica de H_RIVAL (6 celdas, de 4210 a 4365 s cada una, termino el 15-oct 15:56) coteja con Actions: H_RIVAL "
    "REFUTADA y H_TAU_JUSTO SIN_DECIDIR en las dos maquinas; RIDGE y REGLA_TAU con 120 de 120 aciertos iguales; MLP con "
    "40 de 120 iguales y diferencia maxima 0,0045 (torch entre maquinas), misma etiqueta (agregado.log de brain-env md5 "
    "17168360). La replica de la primaria de H_LECTOR corre en brain-env desde el 15-oct 21:55 desde el clon de "
    "@@8d305e9@@ (@@lector_mosca.py@@ 5b7fb79e), dos celdas a la vez, en @@/workspace/fable/rl041/out_brain@@; al "
    "terminar, @@agregar_lector.py --cotejar@@ contra el agregado de Actions (los nulos no se replican, limitacion del "
    "sello).%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 21:33 (America/Buenos_Aires), con la respuesta 2026-10-14-041.",
     "**Última actualización:** 2026-10-15, 21:59 (America/Buenos_Aires), con la respuesta 2026-10-14-042."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-041) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-042) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_042 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("reescribir el Paper 2 alrededor de H_LECTOR y H_TAU_LIBRE, con la replica de la primaria de H_LECTOR en "
     "brain-env como condicion para Zenodo (2026-10-14-041); ",
     "reescribir el Paper 2 alrededor de H_LECTOR y H_TAU_LIBRE; leer el cotejo de la replica de H_LECTOR en "
     "brain-env cuando termine (unas 12 h, sin medir), que es condicion para Zenodo (2026-10-14-042); "),
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
