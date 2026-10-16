#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-047 (instrumento, prueba y humo de H_MOSCA_ENTERA).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-047.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_047 = q(
    "- **H_MOSCA_ENTERA con instrumento, prueba y humo (2026-10-14-047, Abraham 00:01):** en "
    "@@titan/mosca-entera-2026-10-15@@ (instrumento @@194ba1e@@, arreglo de la prueba @@4d14723@@). Prueba 8 de 8 "
    "en Actions (bot @@d0f5385@@) y 7 de 7 en brain-env; la primera cayo por pedir al bit el radio de ARPACK, "
    "declarado. Humo completo (bot @@1603190@@): el LIF de Shiu corre el cerebro entero en el runner (2 ensayos en "
    "65 s, 3,07 GB) y MN9 dispara en 2 de 2 ensayos reales y en 0 de 2 barajados. El humo agarro dos fallas del "
    "sello: en la ventana 151 a 200, LIQ y TASA leen el mismo punto fijo (diferencia 3,2e-10; por construccion, la "
    "compuerta liquida solo cambia la velocidad), asi que H_ENTERA_LIQ no discrimina; y llevar cada grafo a radio "
    "0,9 le da a cada sinapsis de los nulos de 6 a 8 veces la ganancia del real (radio crudo 2164 contra 268 y 340), "
    "mientras el LIF usa pesos crudos. Ningun veredicto medido.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 23:30 (America/Buenos_Aires), con la respuesta 2026-10-14-046.",
     "**Última actualización:** 2026-10-16, 00:30 (America/Buenos_Aires), con la respuesta 2026-10-14-047."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-046) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-047) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_047 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("el instrumento de H_MOSCA_ENTERA en Actions (2026-10-14-046); ",
     "sellar la enmienda de H_MOSCA_ENTERA (lectura por latencia y nulos a ganancia igual) antes de CORRER, o "
     "CORRER como esta sellada (2026-10-14-047); "),
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
