#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-011 (Topo v0, lenguaje topologico ejecutable, en titan/topo-lenguaje-2026-10-14).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-011.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **Topo v0, lenguaje topologico ejecutable (2026-10-14-011):** rama @@titan/topo-lenguaje-2026-10-14@@ "
    "(@@b34924d@@), @@tools/topo/@@ y @@docs/topo/TOPO-v0.md@@. Un reflejo se escribe como tipo x lado x signo -> "
    "comando, con dos backends: regla y cableado.%%"
    "  - El escape en 18 renglones (@@escape.topo@@). Desde un clon limpio: EQUIV_REGLA PASA (12 de 12 casos "
    "exactos contra la regla sellada de los factoriales), CONTROL_NEGATIVO PASA (127 de 400 decisiones distintas "
    "con el aterrizaje mal escrito; 3 programas invalidos rechazados), REPRODUCE_M46 PASA (46 neuronas, 187 aristas, "
    "1.149 sinapsis, igual a la 015). Registro md5 @@f1008c67@@.%%"
    "  - Faltan, sin medir: H_TOPO_NUEVO (un reflejo nuevo escrito solo en Topo que pague en el banco), "
    "H_TOPO_C99 y H_TOPO_ESCALA. Antes, en la 2026-10-14-010, se evaluaron tres ideas: el lenguaje topologico es "
    "la mas fuerte, cerebelo de borde todavia no y protesis solo para avisar.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 12:25 (America/Buenos_Aires), con la respuesta 2026-10-14-006.",
     "**Última actualización:** 2026-10-14, 13:05 (America/Buenos_Aires), con la respuesta 2026-10-14-011."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-006) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-011) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, solo "
     "con su sí); leer H_TAU",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); qué reflejo nuevo sella H_TOPO_NUEVO (2026-10-14-011); leer H_TAU"),
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
