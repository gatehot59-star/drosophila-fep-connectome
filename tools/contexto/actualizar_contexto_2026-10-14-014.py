#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-014 (H_TOPO_NUEVO corriendo en Actions; arreglo de torch declarado).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-014.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **H_TOPO_NUEVO corriendo (2026-10-14-014, ClickKit @@correr_barra_013@@, 13:29):** el humo 1 en Actions fallo "
    "antes de medir por falta de torch (lo importa el modulo sellado de la 003); arreglo declarado en los workflows "
    "(@@6e02d34@@), instrumento sin cambios. Humo 2 en Actions (@@8e89e16@@) igual a brain-env en 15 de 15 lineas. "
    "@@CORRER@@ en @@e416865@@; run 38598860081 desde las 13:31.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 13:20 (America/Buenos_Aires), con la respuesta 2026-10-14-012.",
     "**Última actualización:** 2026-10-14, 13:35 (America/Buenos_Aires), con la respuesta 2026-10-14-014."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-012) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-014) · manda sobre el resto"),
    ("solo con su sí); correr H_TOPO_NUEVO (su " + BT + "CORRER" + BT + ", 2026-10-14-012); la lectura completa",
     "solo con su sí); leer H_TOPO_NUEVO cuando termine (2026-10-14-014); la lectura completa"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_TOPO_NUEVO",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_TOPO_NUEVO"),
]
for i, (a, b) in enumerate(R):
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
