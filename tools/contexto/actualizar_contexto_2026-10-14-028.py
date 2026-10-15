#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-028 (la idea de Abraham: comparar conectomas para encontrar la misma
plantilla aplicada a distintas acciones).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-028.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **Idea de Abraham: la misma plantilla en distintas acciones, comparando conectomas (2026-10-14-028, 21:14):** "
    "comparar BANC con los otros conectomas para separar lo que es de la mosca de lo que es de un individuo, y buscar "
    "circuitos que se repiten para acciones distintas. Primer indicio medido (descriptivo, de los logs de la 023 y la "
    "024): LHAD1g1 (GABA) y PVLP010 (glutamato) estan entre las inhibitorias mayores de DNp01 (despegue; 10,9 y 10,5 "
    "por ciento de su inhibicion) y de DNp06 (giro; 20,1 y 18,7): el mismo modulo de inhibicion de avance sirve a dos "
    "comandos. BANC 888 trae pareja de tipo con FlyWire para 64.789 neuronas, con MANC para 24.277 y con hemibrain "
    "para 6.768; MANC y hemibrain no estan bajados. Propuesta H_REUSO, sin sellar: una plantilla escrita antes de mirar "
    "(sensor a descendente del mismo lado, mas el mismo sensor a una inhibitoria que vuelve a esa descendente) aparece en "
    "mas pares sensor-descendente que en los nulos SL, en FlyWire y otra vez en BANC; falsador, no supera al nulo o no "
    "se replica. Topo v0.3 tendria plantillas: si el repertorio se escribe con pocas plantillas, la compresion es la "
    "medida del reuso.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 21:00 (America/Buenos_Aires), con la respuesta 2026-10-14-027.",
     "**Última actualización:** 2026-10-14, 21:16 (America/Buenos_Aires), con la respuesta 2026-10-14-028."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-027) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-028) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    ("sellar H_COMPARADOR en BANC, el falsador de Topo v0.2 (2026-10-14-026; H_TOPO_FIEL y H_FRENO ya confirmadas en "
     "Actions, 2026-10-14-027); ",
     "sellar H_COMPARADOR en BANC, el falsador de Topo v0.2 (2026-10-14-026; H_TOPO_FIEL y H_FRENO ya confirmadas en "
     "Actions, 2026-10-14-027); decidir si se sella H_REUSO, la misma plantilla en varias acciones en FlyWire y BANC "
     "(2026-10-14-028); "),
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
