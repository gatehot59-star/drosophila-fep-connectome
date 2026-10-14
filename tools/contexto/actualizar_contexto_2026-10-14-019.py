#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-019 (esqueleto del Paper 3 y estado de Topo).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-019.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **Paper 3 con esqueleto y estado de Topo (2026-10-14-019):** esqueleto en @@titan/paper3-esqueleto-2026-10-14@@ "
    "(@@5b2e5ee@@, @@docs/paper3/paper3-esqueleto.md@@, sin PR). Una sola pregunta: que clases alimentan cada salida "
    "(descendentes, motoras, neurosecretoras) mas alla del tamano, la ubicacion y la cantidad de pruebas. Los 106 "
    "numeros estan en sus fuentes de git (@@tools/paper3/cotejar_paper3.py@@ PASA; control negativo PASA). Lo que "
    "aguanta todo: descendentes a descendentes, a motoras, a cuello y a antena, y el optico casi no llega a las "
    "descendentes; el escape visual es el caso (la vista no tiene atajo a las motoras). Pendientes: PR #26 sin review, "
    "la discrepancia del nulo de LC6 a GF (5,8 contra 17,2 esperadas), la replica en BANC. Topo: v0 y H_TOPO_NUEVO "
    "hechos; falta el grafo chequeado contra el conectoma (paso 2 de la 2026-10-14-013) y la v2 del programa de la barra.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 17:33 (America/Buenos_Aires), con la respuesta 2026-10-14-018.",
     "**Última actualización:** 2026-10-14, 17:48 (America/Buenos_Aires), con la respuesta 2026-10-14-019."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-018) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-019) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_DEBILES"),
    (q("correr H_DEBILES, sellado en la 2026-10-14-016 (su @@CORRER@@); sellar H_TAU_JUSTO"),
     q("correr H_DEBILES, sellado en la 2026-10-14-016 (su @@CORRER@@); armar Topo v0.1, el grafo chequeado contra el "
       "conectoma (2026-10-14-019); sellar H_TAU_JUSTO")),
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
