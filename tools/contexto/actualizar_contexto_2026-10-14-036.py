#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-036 (H_LECTOR sellado).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-036.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_036 = q(
    "- **H_LECTOR sellado, sin script (2026-10-14-036, ClickKit @@sellar_lector_mosca@@, 09:52):** rama "
    "@@titan/lector-2026-10-15@@, sello @@8e65e05@@ (@@tools/lector/SELLO-LECTOR.md@@, md5 6e587be6), solo el "
    "documento. Lector: el RIDGE de H_RIVAL sin cambios, sobre las trazas de las 6 descendentes de la red elegida de "
    "H_TAU (240 rasgos contra 22.560 del ridge crudo). H_LECTOR_CERCA: no pierde mas de 1 punto contra el ridge crudo. "
    "H_LECTOR_PAGA: supera por mas de 1 punto a las lineas sin entrenar. H_LECTOR_CABLEADO: con el mismo lector, el "
    "cableado real supera por mas de 1 punto a 40 SL y 40 T en c2 y c5 (prueba 12, interseccion-union). Expectativa "
    "declarada: CABLEADO probablemente REFUTADA (antecedente de la entrada por tipos). El encabezado del sello dice "
    "10:00; el commit es de las 09:57 y manda el commit.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 09:44 (America/Buenos_Aires), con la respuesta 2026-10-14-035.",
     "**Última actualización:** 2026-10-15, 09:58 (America/Buenos_Aires), con la respuesta 2026-10-14-036."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-035) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-036) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_036 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("la pregunta y el titulo del Paper 2 tras H_RIVAL y H_CONSENSO, y si se mide la mosca con lector entrenado sobre "
     "sus descendentes (2026-10-14-035); ",
     q("la pregunta y el titulo del Paper 2 tras H_RIVAL y H_CONSENSO (2026-10-14-035); escribir el instrumento de "
       "H_LECTOR y su humo ciego, y despues su @@CORRER@@ (2026-10-14-036); ")),
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
