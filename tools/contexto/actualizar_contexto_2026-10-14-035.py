#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-035 (v2 del Paper 1 publicada y auditoria del Paper 2 y el 3 contra H_RIVAL).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-035.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_035 = q(
    "- **La v2 del Paper 1 esta publicada (2026-10-14-035, ClickKit @@v2_publicar_asi@@, 09:41):** DOI "
    "10.5281/zenodo.23393412, version 2.0 del concepto 10.5281/zenodo.19136947, publicada a las 09:42 con "
    "@@depositar_v2.py --publicar@@ desde main (@@06872d0@@). Chequeo sin token: registro publico 200, los dos PDF con el "
    "md5 sellado (6e849bf2 y 05052e6e), ultima version del concepto. Va con el titulo que incluye la amplificacion "
    "temporal, como eligio Abraham. Recibo: @@docs/v2/recibo-publicacion-v2.0.json@@.%%"
    "- **Auditoria del Paper 2 y el Paper 3 contra H_RIVAL (2026-10-14-035):** el Paper 2 no nombra el ridge entrenado "
    "que su propia fuente ya media (2026-10-12-015, 0,9475 a 0,9875, descriptivo), tiene viejos H_CONSENSO (REFUTADA) "
    "y H_TAU (SOSTENIDA, con H_TAU_JUSTO SIN_DECIDIR), y su titulo y su Discusion (fabrica de piezas, el modelo de "
    "sinapsis como culpable) no sobreviven a H_RIVAL. El Paper 3 es estructural: ningun numero cambia; solo hay que "
    "acotar en 3.5 y 4 que el embudo descendente no es el mejor lugar para leer la vision. Ninguno esta para Zenodo.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 08:19 (America/Buenos_Aires), con la respuesta 2026-10-14-034.",
     "**Última actualización:** 2026-10-15, 09:44 (America/Buenos_Aires), con la respuesta 2026-10-14-035."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-034) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-035) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** publicar o descartar el borrador de la v2 en Zenodo (23393412; publicar, solo con "
     "su sí), y antes de publicar, si Z_CP y la RDI se reproducen o salen del titulo y del resumen (2026-10-14-031); "
     "revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); escribir el Paper 2 y el Paper 3, con "
     "H_RIVAL adentro, antes de depositarlos (2026-10-14-034); ",
     NUEVO_035 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); si una v2.1 del Paper 1 reproduce Z_CP y la RDI o saca la amplificacion del titulo (la v2.0 ya "
     "esta publicada, 2026-10-14-035); la pregunta y el titulo del Paper 2 tras H_RIVAL y H_CONSENSO, y si se mide la "
     "mosca con lector entrenado sobre sus descendentes (2026-10-14-035); "),
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
