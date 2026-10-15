#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-027 (confirmacion en Actions y sintesis en criollo de la 021 a la 026).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-027.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **Confirmado en Actions y sintesis en criollo (2026-10-14-027, 20:56):** H_TOPO_FIEL REFUTADA en Actions x64 "
    "igual que en brain-env (run 38641915842; 38 de 38 lineas iguales salvo maquina y tiempos). H_FRENO REFUTADA en "
    "Actions igual (run 38652439698; mecanismos, control y veredicto identicos); unica diferencia, descriptiva: dos tipos "
    "empatados en 98 sinapsis salen en otro orden en el top 10 (el orden de los empates no es estable). Cruce con la "
    "2026-10-12-011: LHAD1g1 izquierda recibe 5,16 por ciento de su entrada desde LC4 y LPLC2, como el 5,2 de entonces. "
    "Sintesis: el cerebro de la mosca no decide de que lado girar ante un looming; manda las dos DNp06 encendidas "
    "(responden a los dos ojos) y la resta que el programa necesita no esta en el cerebro a dos saltos; Topo v0.2 la "
    "pone aguas abajo y el falsador es H_COMPARADOR en BANC. Para la demo camara a vibracion (2026-10-13-020): la "
    "pieza de mosca da peligro por lado y el lado lo decide una resta despues, que en el microcontrolador es una cuenta.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 20:30 (America/Buenos_Aires), con la respuesta 2026-10-14-026.",
     "**Última actualización:** 2026-10-14, 21:00 (America/Buenos_Aires), con la respuesta 2026-10-14-027."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-026) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-027) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    ("confirmar H_TOPO_FIEL en Actions (2026-10-14-022); ", ""),
    ("confirmar H_FRENO en Actions; sellar H_COMPARADOR en BANC, el falsador de Topo v0.2 (2026-10-14-026); ",
     "sellar H_COMPARADOR en BANC, el falsador de Topo v0.2 (2026-10-14-026; H_TOPO_FIEL y H_FRENO ya confirmadas en "
     "Actions, 2026-10-14-027); "),
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
