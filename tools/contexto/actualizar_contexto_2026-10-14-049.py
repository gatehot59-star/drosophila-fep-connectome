#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-049 (CORRER de H_MOSCA_ENTERA con la enmienda 048).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-049.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_049 = q(
    "- **H_MOSCA_ENTERA corrida (2026-10-14-049, pregunta de Abraham 07:58):** CORRER en Actions en "
    "@@titan/mosca-entera-2026-10-15@@ (disparo @@9c90549@@, run 38892606733, bot @@9465b38@@, de 08:15 a 08:30), "
    "despues de la prueba 13 de 13 (@@fbed6bb@@) y el humo (@@506d836@@). Es el conectoma entero (138.639 neuronas) "
    "con la ecuacion SparseLTC del laboratorio en numpy disperso, no el runtime de Mojo/C++. REPRO_SHIU PASA: MN9 "
    "dispara en 30 de 30 ensayos reales del LIF de Shiu y en 0 de 20 barajados (K = 321). H_ENTERA_CONJUNTO y "
    "_CONJUNTO_G1 SOSTENIDA: SparseLTC acierta 172 de las 321 neuronas que el LIF prende con azucar (J 0,366); el "
    "mejor de 80 barajados, 103 (G1: 97). H_ENTERA_RIVAL SOSTENIDA (+0,110; la proximidad sin dinamica acierta 131). "
    "H_ENTERA_MN9 REFUTADA (15 de 40 SHUF_W y 3 de 40 SHUF_G iguales o mayores) y _MN9_G1 SIN_DECIDIR (79 de 80 por "
    "debajo; supera SHUF_G k32). H_ENTERA_LIQ REFUTADA_DEGENERADA (mismo punto fijo, max|dr| 4,55e-07) y "
    "H_ENTERA_LAT SIN_DECIDIR (D_LAT +0,008). La destilacion no se habilita. Error de proceso declarado: CORRER "
    "estaba autorizado desde las 00:48 y se volvio a pedir permiso dos veces.%%"
)

R = [
    ("**Última actualización:** 2026-10-16, 00:52 (America/Buenos_Aires), con la respuesta 2026-10-14-048.",
     "**Última actualización:** 2026-10-16, 08:38 (America/Buenos_Aires), con la respuesta 2026-10-14-049."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-048) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-049) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_049 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("el instrumento de la enmienda de H_MOSCA_ENTERA con prueba y humo, y despues CORRER (2026-10-14-048); ",
     "si se sella H_ENTERA_UMBRAL (la misma corrida con un umbral global calibrado por grafo, para ver si MN9 depende "
     "de la no linealidad del LIF) o H_MOSCA_ENTERA se escribe como esta en el Paper 2 (2026-10-14-049); "),
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
