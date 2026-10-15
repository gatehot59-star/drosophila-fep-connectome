#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-029 (H_REUSO sellado, sin correr).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-029.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **H_REUSO sellado, sin correr (2026-10-14-029, ClickKit @@sellar_reuso_028@@, 21:20):** rama "
    "@@titan/reuso-2026-10-14@@ (A @@613317d@@, sello @@5ef2a63@@, @@tools/reuso/SELLO-REUSO.md@@). Plantilla de "
    "inhibicion de avance: sensor visual a descendente del mismo lado con 20 sinapsis o mas, y una inhibitoria con 5 o "
    "mas desde ese sensor y 5 o mas sobre esa descendente. T1, fraccion de pares con la plantilla; T2, inhibitorias que "
    "la hacen para dos o mas tipos de descendente. 200 nulos SL por conectoma (destinos barajados por bloque de lados), "
    "Holm sobre 4 pruebas; SOSTENIDA si pasa en FlyWire y otra vez en BANC. Prueba 7/7 (dio rojo una vez por un error "
    "de la prueba, corregido antes de datos reales). Humo CIEGO en brain-env: controles y guardas PASAN (FlyWire 996 "
    "pares, BANC 753), sin ver T1 ni T2; de paso, LHAD1g1 tambien esta entre las X de LPLC2 a DNp06 en BANC. La "
    "corrida completa espera su @@CORRER@@ (unos 40 minutos).%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 21:16 (America/Buenos_Aires), con la respuesta 2026-10-14-028.",
     "**Última actualización:** 2026-10-14, 21:36 (America/Buenos_Aires), con la respuesta 2026-10-14-029."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-028) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-029) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    ("decidir si se sella H_REUSO, la misma plantilla en varias acciones en FlyWire y BANC (2026-10-14-028); ",
     q("correr H_REUSO, sellado en la 2026-10-14-029 (su @@CORRER@@, unos 40 minutos); ")),
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
