#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-005 (esqueleto del Paper 2 en la rama titan/paper2-esqueleto-2026-10-14).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-005.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **Esqueleto del Paper 2 (2026-10-14-005, ClickKit @@esqueleto_paper2_004@@):** "
    "@@docs/paper2/paper2-esqueleto.md@@ en @@titan/paper2-esqueleto-2026-10-14@@ (@@753d4d5@@), sin PR.%%"
    "  - Una sola pregunta: si el cableado exacto carga el reflejo mas alla de su diseno y sus barajados, y si esa "
    "parte se conserva en BANC. Resultados 3.1 a 3.5 con numeros medidos (cotejo 73 de 74 en su fuente, el restante en "
    "el log de BANC); 3.6 H_CONSENSO y 3.7 H_TAU como huecos; 3.8 el negativo de lineas etiquetadas.%%"
    "  - Bloquean un borrador: nulo del emparejado BANC, revision de literatura del hueco funcional, ecuacion exacta y "
    "figuras. Recomendacion: el control de salidas, LC6 a GF y sel_post van a un Paper 3, no a este.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 11:45 (America/Buenos_Aires), con la respuesta 2026-10-14-004.",
     "**Última actualización:** 2026-10-14, 12:40 (America/Buenos_Aires), con la respuesta 2026-10-14-005."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-004) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-005) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_TAU y el núcleo cuando terminen (2026-10-14-004); el esqueleto del Paper 2; el nulo "
     "del emparejado BANC; responderle a Tao en su PR.",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_TAU y el núcleo cuando terminen (2026-10-14-004); el alcance del Paper 2 (control de "
     "salidas fuera o dentro, 2026-10-14-005); el nulo del emparejado BANC; responderle a Tao en su PR."),
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
