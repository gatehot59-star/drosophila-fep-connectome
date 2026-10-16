#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-050 (sello de H_ENTERA_UMBRAL).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-050.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_050 = q(
    "- **H_ENTERA_UMBRAL sellada (2026-10-14-050, Abraham eligio sellar):** @@tools/mosca_entera/SELLO-UMBRAL-050.md@@ "
    "en @@titan/mosca-entera-2026-10-15@@, antes del instrumento. Brazo UMB: TASA de la 049 con activacion "
    "tanh(max(0, Wz + x - theta)) y un umbral global calibrado por grafo para que queden 321 neuronas activas (el K "
    "del LIF), en el real a radio 0,9 y en los mismos 80 nulos con el factor del real (G1). H_UMB_MN9, _CONJUNTO "
    "(bandas de la 046) y _GANA (J(UMB) - J(TASA) >= +0,05). Expectativa escrita: H_UMB_MN9 REFUTADA con r = 0. "
    "Declarado: la lectura de la ventana no depende de tau, asi que el humo de la 049 (tau 99) ya habia mostrado el "
    "brazo real antes de CORRER; el humo de UMB usa otro estimulo. Ningun numero nuevo.%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 08:38 (America/Buenos_Aires), con la respuesta 2026-10-14-049.",
     "**Última actualización:** 2026-10-16, 10:30 (America/Buenos_Aires), con la respuesta 2026-10-14-050."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-049) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-050) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_050 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("si se sella H_ENTERA_UMBRAL (la misma corrida con un umbral global calibrado por grafo, para ver si MN9 depende "
     "de la no linealidad del LIF) o H_MOSCA_ENTERA se escribe como esta en el Paper 2 (2026-10-14-049); ",
     "el instrumento de H_ENTERA_UMBRAL con prueba y humo, y despues CORRER (2026-10-14-050); "),
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
