#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-018 (sintesis en criollo: que tenemos, hacia donde vamos, potencial).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-018.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **Sintesis en criollo (2026-10-14-018), reemplaza a la 2026-10-13-011:** tenemos un banco sellado que compara "
    "el cableado real contra sus barajados y contra el plano de la mosca con los mismos sensores. El cableado les gana a "
    "sus barajados en las cuatro escalas (M46, R1, R2 y cerebro entero); contra el plano empata (R2 +0,85, cerebro "
    "entero igual a R2) y lo supera solo con tau elegida por validacion cruzada (+1,78; falta H_TAU_JUSTO). El nucleo "
    "carga la mayor parte de la ventaja sobre los barajados (88 %, post hoc) pero solo pierde 4,59 puntos: falta "
    "H_DEBILES. Potencial: un resultado de nicho publicable por el metodo, Topo para escribir planos de reflejos "
    "baratos y el portero de choque como primera demo fuera de simulacion. Nada medido fuera de simulacion.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 17:27 (America/Buenos_Aires), con la respuesta 2026-10-14-017.",
     "**Última actualización:** 2026-10-14, 17:33 (America/Buenos_Aires), con la respuesta 2026-10-14-018."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-017) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-018) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); correr H_DEBILES"),
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
