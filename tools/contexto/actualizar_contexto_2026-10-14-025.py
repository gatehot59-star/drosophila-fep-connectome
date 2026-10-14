#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-025 (la literatura: DNp06 responde tambien al ojo contrario). Va despues
del parche 024.

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-025.py docs/agents/CONTEXTO-drosophila-fep.md
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
    "- **DNp06 responde a los dos ojos; el frente no esta medido (2026-10-14-025, ClickKit @@frontal_dnp06_024@@, "
    "20:17, literatura):** Jang et al. 2023, J Exp Biol 226: jeb244790: con looming a +-45 grados, GF, DNp02 y DNp06 "
    "responden a los dos ojos aunque sus dendritas son de un solo lado; DNp06 con grandes despolarizaciones y espigas "
    "(un solo ensayo mostrado). La via contralateral es unidentified segun los autores. Kim et al. 2023, Curr Biol 33: 321: DNp06 "
    "responde a puntos que se mueven en el campo contralateral. El looming frontal sobre DNp06 no esta medido en lo "
    "leido. Lectura: la tercera salida de la 024 (el frente no enciende a DNp06) queda floja; la entrada contralateral "
    "de DNp06 en la mosca es EXCITATORIA, al reves que la resta del programa, y no aparece a dos saltos con sinapsis "
    "quimicas (FlyWire no tiene las electricas). Entonces el lado del giro se decide aguas abajo, comparando las dos "
    "DNp06 (u otras descendentes) en el cordon nervioso: la resta del programa seria esa comparacion, no una cuenta "
    "dentro de DNp06. NO MEDIDO.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 20:15 (America/Buenos_Aires), con la respuesta 2026-10-14-024.",
     "**Última actualización:** 2026-10-14, 20:25 (America/Buenos_Aires), con la respuesta 2026-10-14-025."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-024) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-025) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES",
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_DEBILES"),
    ("confirmar H_FRENO en Actions; decidir si se prueba que el looming frontal no excita a DNp06 en la mosca "
     "(2026-10-14-024); ",
     "confirmar H_FRENO en Actions; decidir si Topo v0.2 lleva una salida que compare las dos DNp06, aguas abajo, "
     "y si se sella contra el programa que resta (2026-10-14-025); "),
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
