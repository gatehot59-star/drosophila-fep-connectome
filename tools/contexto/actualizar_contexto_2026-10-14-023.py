#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-023 (H_FRENO sellado, sin correr).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-023.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **H_FRENO sellado, sin correr (2026-10-14-023, ClickKit @@sellar_frena_giro_022@@, 19:57):** rama "
    "@@titan/frena-giro-2026-10-14@@ (instrumento @@d59913c@@, sello @@2bad970@@, @@tools/frena_giro/SELLO-FRENO.md@@). "
    "Pregunta: que frena el giro de DNp06 ante el looming frontal, si la resta no tiene via directa. Siete mecanismos "
    "pre-registrados antes de mirar DNp06: directos (DNp07, DNp01, la DNp06 opuesta) y a dos saltos por interneurona "
    "inhibitoria (LPLC1 y LPLC2 del otro lado, LPLC4, DNp07, detector bilateral). Cuota de la entrada inhibitoria y "
    "percentil contra las 927 unidades descendentes; control positivo con LPLC1 y LPLC2 del mismo lado. Prueba 6/6 "
    "(dio rojo una vez y se corrigio antes de datos reales). Humo con DNp01, DNp06 ciega. La corrida con DNp06 "
    "espera su @@CORRER@@ (segundos).%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 18:45 (America/Buenos_Aires), con la respuesta 2026-10-14-022.",
     "**Última actualización:** 2026-10-14, 20:10 (America/Buenos_Aires), con la respuesta 2026-10-14-023."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-022) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-023) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    ("confirmar H_TOPO_FIEL en Actions y decidir si se sella que frena el giro ante el looming frontal "
     "(2026-10-14-022); ",
     q("confirmar H_TOPO_FIEL en Actions (2026-10-14-022); correr H_FRENO, sellado en la 2026-10-14-023 (su "
       "@@CORRER@@, segundos); ")),
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
