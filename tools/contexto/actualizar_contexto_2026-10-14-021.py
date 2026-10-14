#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-021 (H_TOPO_FIEL sellado, sin correr).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-021.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **H_TOPO_FIEL sellado, sin correr (2026-10-14-021, ClickKit @@sellar_topo_fiel_020@@, 18:20):** rama "
    "@@titan/topo-fiel-2026-10-14@@ (A @@27fe098@@ programas, B @@b3548c8@@ banco, sello @@79b8c59@@, "
    "@@tools/topo_fiel/SELLO-TOPO-FIEL.md@@). El programa fiel (@@escape_fiel.topo@@) es @@escape.topo@@ sin la resta "
    "contralateral en el giro de DNp06; Topo v0.1 da CABLEADA=10. Se compara contra el que resta en la tarea de la 012 "
    "con semillas nuevas (12.000 ensayos, margen 0,01, IC90): SOSTENIDA si el fiel no pierde mas de un punto. Control "
    "cruzado (gira hacia el estimulo) tiene que salir REFUTADA; si no, INVALIDO. Prueba 8/8. Humo en brain-env "
    "(numeros sin valor, vistos y declarados): el fiel pierde unos 5 puntos, casi todo por el looming frontal en vuelo "
    "(sin la resta gira en vez de aterrizar), y gira igual o mejor; el control salio REFUTADA. La corrida completa no "
    "es ciega respecto del humo (mismas semillas, menor tamano). Humo en Actions en cola.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 18:10 (America/Buenos_Aires), con la respuesta 2026-10-14-020.",
     "**Última actualización:** 2026-10-14, 18:35 (America/Buenos_Aires), con la respuesta 2026-10-14-021."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-020) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-021) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    ("leer H_DEBILES cuando termine (corre desde las 17:53, run 38635900391, 2026-10-14-020); sellar H_TAU_JUSTO",
     q("leer H_DEBILES cuando termine (corre desde las 17:53, run 38635900391, 2026-10-14-020); correr H_TOPO_FIEL, "
       "sellado en la 2026-10-14-021 (su @@CORRER@@, unos minutos); sellar H_TAU_JUSTO")),
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
