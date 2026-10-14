#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-016 (H_DEBILES sellado, sin correr).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-016.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **H_DEBILES sellado, sin correr (2026-10-14-016):** rama @@titan/debiles-2026-10-14@@. La mezcla es R2 con el "
    "nucleo intacto y las 3.428.678 aristas debiles con destinos barajados por lado (mismos grados, pesos y signos). "
    "E1 = mezcla menos R2 decide H_DEBILES_ESPECIFICAS (importa cuales son) y E2 = mezcla menos nucleo decide "
    "H_DEBILES_SUMAN (importa cuantas son), pareadas corrida por corrida con el factorial 3 y con el nucleo, M 0,01. "
    "Instrumento @@f28404c2@@, agregador @@c60fbbc6@@, prueba del agregador 7 de 7. Antes del CORRER, los reales a "
    "tamano completo del humo tienen que dar 0,9465 y 0,9135. Corre solo con @@results/debiles_2026-10-14/CORRER@@.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 16:30 (America/Buenos_Aires), con la respuesta 2026-10-14-015.",
     "**Última actualización:** 2026-10-14, 17:15 (America/Buenos_Aires), con la respuesta 2026-10-14-016."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-015) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-016) · manda sobre el resto"),
    ("solo con su sí); sellar H_DEBILES y H_TAU_JUSTO, y una segunda versión del programa de la barra (2026-10-14-015); "
     "el nulo",
     q("solo con su sí); correr H_DEBILES, sellado en la 2026-10-14-016 (su @@CORRER@@); sellar H_TAU_JUSTO y una "
       "segunda versión del programa de la barra (2026-10-14-015); el nulo")),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_DEBILES"),
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
