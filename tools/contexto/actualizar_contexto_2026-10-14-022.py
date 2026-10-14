#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-022 (H_TOPO_FIEL REFUTADA en brain-env). Va despues del parche 021.

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-022.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **H_TOPO_FIEL REFUTADA en brain-env (2026-10-14-022, ClickKit @@correr_topo_fiel_021@@, 18:38):** @@CORRER@@ en "
    "@@0f83872@@; Actions en cola detras de H_DEBILES, asi que el mismo instrumento sellado corrio completo en brain-env "
    "(81 s, log md5 5db97477). Todas las guardas en verde. El fiel pierde 5,41 puntos contra el que resta (IC90 "
    "[-5,92; -4,90]); el control cruzado REFUTADA (-27,97). Por subconjunto (descriptivo): ante el looming frontal en "
    "vuelo el fiel pierde 85 a 88 puntos (aterriza 6,5 a 7,1 por ciento contra 92 a 94), en el giro gana hasta 22 puntos con "
    "ruido alto. Lectura: la resta del programa cancela el looming frontal en el giro; en la mosca eso no pasa por "
    "via directa, asi que lo hace otro circuito (NO MEDIDO). Falta la confirmacion en Actions x64.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 18:35 (America/Buenos_Aires), con la respuesta 2026-10-14-021.",
     "**Última actualización:** 2026-10-14, 18:45 (America/Buenos_Aires), con la respuesta 2026-10-14-022."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-021) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-022) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    (q("correr H_TOPO_FIEL, sellado en la 2026-10-14-021 (su @@CORRER@@, unos minutos); "),
     "confirmar H_TOPO_FIEL en Actions y decidir si se sella que frena el giro ante el looming frontal "
     "(2026-10-14-022); "),
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
