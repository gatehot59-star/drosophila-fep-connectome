#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-012 (H_TOPO_NUEVO sellado con la barra segun su direccion; el nucleo
volvio: H_CONSENSO REFUTADA y H_CABLEADO_NUCLEO SOSTENIDA).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-012.py docs/agents/CONTEXTO-drosophila-fep.md
Las comillas invertidas y los saltos se arman con chr() para que el archivo no lleve caracteres de escape.
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
    "- **H_TOPO_NUEVO sellado con la barra segun su direccion (2026-10-14-012):** rama "
    "@@titan/topo-barra-dir-2026-10-14@@, orden verificable A tarea (@@42d2f60@@), B programa (@@2deb335@@), "
    "C banco (@@8c7cf1b@@), sello @@afc2585@@ (@@tools/topo_barra/SELLO-BARRA-DIR.md@@).%%"
    "  - La barra de adelante hacia atras ya estaba en la 015 (no era nueva); lo nuevo es la de atras hacia adelante "
    "en vuelo -> girar (fuente indirecta: Ache 2019 Supp Fig 5d, Kim 2023). Programa nuevo: aterrizar = LPLC4 - LPLC1.%%"
    "  - Humo en brain-env VALIDO (numeros sin valor, vistos y declarados); humo en Actions disparado. La corrida "
    "completa espera @@results/topo_barra_2026-10-14/CORRER@@.%%"
    "- **El nucleo volvio (bot @@a522bc4@@, agregado sellado):** VEREDICTO_GLOBAL VALIDO. H_CONSENSO REFUTADA: el "
    "nucleo pierde 4,59 puntos contra R2 (0,8894 contra 0,9353, IC90 [-5,07; -4,10]), pierde en las 600 corridas y "
    "en las 6 celdas. H_CABLEADO_NUCLEO SOSTENIDA: 0,9135 contra 50 SL (max 0,757) y 50 T (max 0,768), Holm 0,0392. "
    "Lectura completa pendiente.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 13:05 (America/Buenos_Aires), con la respuesta 2026-10-14-011.",
     "**Última actualización:** 2026-10-14, 13:20 (America/Buenos_Aires), con la respuesta 2026-10-14-012."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-011) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-012) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, solo con su "
     "sí); qué reflejo nuevo sella H_TOPO_NUEVO (2026-10-14-011); leer H_TAU y el núcleo cuando terminen "
     "(2026-10-14-004); el nulo del emparejado BANC; responderle a Tao en su PR.",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_TOPO_NUEVO (su " + BT + "CORRER" + BT + ", 2026-10-14-012); la lectura completa del "
     "núcleo; leer H_TAU cuando termine (2026-10-14-004); el nulo del emparejado BANC; responderle a Tao en su PR."),
]
for a, b in R:
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
for a, b in R:
    if t.count(a) != 1:
        print("ABORTA: ancla cambiada por un reemplazo previo")
        sys.exit(2)
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
