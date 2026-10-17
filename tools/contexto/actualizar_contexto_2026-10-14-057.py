#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-057 (en criollo, todo: potencial y alcance).

Ademas corrige el encabezado (decia que Zenodo tenia solo la v1.0; la v2.0 esta publicada desde la 2026-10-14-035)
y anota el sondeo de maquinas del 17-oct.
Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-057.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_057 = (
    "- **Sintesis en criollo de todo, potencial y alcance (2026-10-14-057, pedido de Abraham 17-oct 09:06; en "
    "potencial reemplaza a la 2026-10-14-018):** el cableado exacto de la mosca importa y se mide sin trampa: les gana "
    "a sus barajados en las cuatro escalas y H_REUSO se repite en FlyWire y en BANC. Pero no es un cerebro mejor que lo "
    "clasico: un ridge entrenado sobre las mismas 564 entradas le gana por 5 puntos (H_RIVAL), sus 6 descendentes "
    "comprimen la tarea casi sin perdida (H_LECTOR_CERCA, 240 rasgos contra 22.560) y la motora del azucar solo salio "
    "con la neurona de Shiu (2026-10-14-055). No choca con la 2026-10-12-011: aquella era el recorte del motivo de 28, "
    "que los factoriales confirmaron; sin recorte, en el cerebro entero, queda la neurona. Potencial (opinion): Paper 1 "
    "publicado; Paper 2 reencuadrado (el cableado es necesario y comprime, pero no es el mejor lector; mas la mosca "
    "entera); Paper 3 con nulo regional de BANC; el banco sellado como metodo y servicio; Topo; para un producto "
    "conviene lo clasico (ridge o la regla del plano) y la mosca aporta el plano. Alcance: solo simulacion, un "
    "conectoma con funcion (FlyWire v783), la vara externa es el modelo de Shiu y no la mosca viva, p en el piso de "
    "sus nulos, cero hardware. Sondeo del 17-oct: brain-env con 2 nucleos, 7 GB de RAM (4 disponibles) y 78 GB "
    "libres de 406 en @@/workspace@@; el @@00-ENTORNOS-Y-CAPACIDADES.md@@ de agosto dice 156 GB y gana lo medido "
    "(el archivo no se toco: se actualiza en los cuatro repos a la vez); sandbox de ClickUp con 4 nucleos, gcc y "
    "g++, sin internet. El encabezado de este archivo decia que Zenodo tenia solo la v1.0: corregido.%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 20:40 (America/Buenos_Aires), con la respuesta 2026-10-14-056.",
     "**Última actualización:** 2026-10-17, 09:25 (America/Buenos_Aires), con la respuesta 2026-10-14-057."),
    ("**Base vigente del paper:** en @@main@@, @@docs/ERRATUM.md@@ anterior a la revisión; **la versión para "
     "depositar está en el PR #27** (erratum revisado, 9 ítems y 12 pendientes, anotaciones pinneadas a "
     "@@17fc577@@, y el manuscrito @@docs/v2/paper1-v2.0.md@@). **Zenodo tiene sólo la v1.0** (20-mar).",
     "**Base vigente del paper:** la v2.0 está publicada en Zenodo (DOI 10.5281/zenodo.23393412, 15-oct, "
     "2026-10-14-035), con el erratum revisado adentro; el PR #27 se mergeó en @@main@@ (@@6785316@@, "
     "2026-10-14-004). La v1.0 (20-mar) queda como versión anterior del mismo concepto (10.5281/zenodo.19136947)."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-056) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-057) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_057 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("el nulo del emparejado BANC; responderle a Tao en su PR.",
     "el nulo del emparejado BANC; responderle a Tao en su PR; actualizar a la vez las cuatro copias de "
     "@@00-ENTORNOS-Y-CAPACIDADES.md@@ con el sondeo del 17-oct (2026-10-14-057)."),
]
for a, b in R:
    a, b = q(a), q(b)
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
