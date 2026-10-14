#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-020 (Topo v0.1 y H_DEBILES corriendo).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-020.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO = q(
    "- **Topo v0.1 y H_DEBILES corriendo (2026-10-14-020, ClickKit @@topo_y_debiles_019@@, 17:53):** H_DEBILES "
    "disparado (@@CORRER@@ en @@84e225c@@, run 38635900391, 64 trabajos, unas 3 h); los reales completos dieron exacto "
    "tambien en brain-env (0,9465 y 0,9135). Topo v0.1 en @@titan/topo-grafo-2026-10-14@@ (@@3d7010a@@): "
    "@@tools/topo/topo_grafo.py@@ dibuja cada programa como grafo (Mermaid) y chequea cada flecha contra FlyWire "
    "(CABLEADA, SIGNO_CONTRARIO, SIN_VIA_DIRECTA); pruebas 5 de 5, reproduce exacto los totales de la 2026-10-12-014. "
    "Descriptivo: en el escape las 10 flechas que suman estan cableadas y las 4 restas del giro no tienen via directa "
    "(a dos saltos, casi todo excitatorio); en el aterrizaje por direccion, la unica flecha nueva (restar LPLC1 en "
    "DNp07) no tiene via directa.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 17:48 (America/Buenos_Aires), con la respuesta 2026-10-14-019.",
     "**Última actualización:** 2026-10-14, 18:10 (America/Buenos_Aires), con la respuesta 2026-10-14-020."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-019) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-020) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_DEBILES"),
    (q("correr H_DEBILES, sellado en la 2026-10-14-016 (su @@CORRER@@); armar Topo v0.1, el grafo chequeado contra el "
       "conectoma (2026-10-14-019); sellar H_TAU_JUSTO"),
     "leer H_DEBILES cuando termine (corre desde las 17:53, run 38635900391, 2026-10-14-020); sellar H_TAU_JUSTO"),
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
