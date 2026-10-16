#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-051 (medicion de H_ENTERA_UMBRAL).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-051.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_051 = q(
    "- **H_ENTERA_UMBRAL medida (2026-10-14-051, Abraham pidio implementar el instrumento UMB):** instrumento "
    "@@1f40beb@@, prueba 7 de 7 y humo limpio en Actions, CORRER en el run 38912718970 (bot @@c5f2960@@, unos 20 min). "
    "Controles PIN, CALIB_REAL (321 activas justas, theta 0,000417) y TASA_049 en PASA. **H_UMB_MN9 SIN_DECIDIR:** MN9 "
    "entra entre las 321 activas del real (r 0,000145, puesto 269) y queda en cero en los 40 SHUF_W y en 39 de 40 "
    "SHUF_G; el unico nulo que llega es SHUF_G k32 (0,00158), el mismo que dejo SIN_DECIDIR a H_ENTERA_MN9_G1 en la "
    "049. **H_UMB_CONJUNTO SOSTENIDA** (J 0,332 contra maximos 0,182 y 0,006). **H_UMB_GANA REFUTADA** (d -0,034). "
    "La expectativa escrita (MN9 REFUTADA con r = 0) fallo. Destilacion no habilitada; no se agregan nulos despues de "
    "ver. Medicion en @@results/mosca_umbral_2026-10-16/actions_correr/@@ (30 archivos, md5 verificados desde un clon "
    "nuevo).%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 10:30 (America/Buenos_Aires), con la respuesta 2026-10-14-050.",
     "**Última actualización:** 2026-10-16, 11:35 (America/Buenos_Aires), con la respuesta 2026-10-14-051."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-050) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-051) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_051 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("el instrumento de H_ENTERA_UMBRAL con prueba y humo, y despues CORRER (2026-10-14-050); ",
     "si se mira por que el nulo SHUF_G k32 llega a MN9 (descriptivo, no cambia veredictos) o H_MOSCA_ENTERA y "
     "H_ENTERA_UMBRAL se escriben como estan en el Paper 2 (2026-10-14-051); "),
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
