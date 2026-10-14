#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-006 (alcance del Paper 2 decidido: el control de salidas va al Paper 3).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-006.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **Alcance del Paper 2 decidido (2026-10-14-006, Abraham, ClickKit @@alcance_p3_005@@, 12:19):** el control de "
    "las salidas (2026-10-10-005 a 009), LC6 a GF y sel_post van a un Paper 3 estructural. El Paper 2 queda con una "
    "sola pregunta. Anotado en el esqueleto (@@4652c81@@).%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 12:40 (America/Buenos_Aires), con la respuesta 2026-10-14-005.",
     "**Última actualización:** 2026-10-14, 12:25 (America/Buenos_Aires), con la respuesta 2026-10-14-006."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-005) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-006) · manda sobre el resto"),
    ("leer H_TAU y el núcleo cuando terminen (2026-10-14-004); el alcance del Paper 2 (control de salidas fuera o "
     "dentro, 2026-10-14-005); el nulo del emparejado BANC; responderle a Tao en su PR.",
     "leer H_TAU y el núcleo cuando terminen (2026-10-14-004); el nulo del emparejado BANC; responderle a Tao en su PR."),
    (q("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, solo "
       "con su sí); leer H_TAU"),
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, solo "
     "con su sí); leer H_TAU"),
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
