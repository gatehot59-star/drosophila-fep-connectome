#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con las respuestas 2026-10-14-030, 031 y 032, en un solo parche.

Agrega solo el estado de los sellos (H_REUSO SOSTENIDA, H_DEBILES INVALIDO, H_RIVAL sellado sin script), la regla
de no citar descriptivos de corridas invalidas y la lista de espera al dia. Ningun descriptivo de H_DEBILES.
Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-032.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_030 = q(
    "- **H_REUSO SOSTENIDA en FlyWire y otra vez en BANC (2026-10-14-030, ClickKit @@correr_reuso_029@@, 22:09):** "
    "CORRER @@6bec7cf@@; Actions, bot @@f12c95a@@ (reuso.log 6e12152a); brain-env, @@c74509a@@ (brain-env.log "
    "b008f8e9); 59 de 59 lineas iguales sin tiempos. FlyWire: T1 0,8835 contra nulo media 0,6823 (max 0,7462); T2, "
    "698 inhibitorias que sirven a dos o mas tipos de descendente, contra 128,6 (max 154). BANC: T1 0,8260 contra "
    "0,3472 (max 0,4744); T2 419 contra 11,0 (max 23). p 0,005 en las cuatro (el piso con 200 nulos), Holm 0,0199. "
    "Descriptivo: 203 tipos de X compartidos aparecen en los dos conectomas. Limite: el nulo SL baraja destinos entre "
    "todas las neuronas y no conserva cuanto le manda cada X a las descendentes como clase; el nulo que conserva la "
    "clase del destino es NO MEDIDO y es el falsador siguiente (H_REUSO_ESTRICTO). **H_DEBILES dio INVALIDO por "
    "infraestructura:** Actions perdio 2 de 60 celdas (t3c3, el runner perdio comunicacion; t8c0, el artefacto no "
    "subio) y el agregador freno la lectura como debia (bot @@3bc5432@@, agregado.log 634e762a); falta relanzar esas "
    "2 celdas, y sus descriptivos no se citan.%%"
)

NUEVO_031 = q(
    "- **Regla nueva: los descriptivos de una corrida INVALIDA no se citan como resultado (2026-10-14-031, aprobada "
    "por Abraham el 15-oct a las 00:17):** ni en papers, ni en Docs, ni en el chat; si hace falta nombrarlos, van con "
    "la palabra INVALIDA al lado. La auditoria externa de Fable 5.1 sobre el expediente de las 23:06 y su revision "
    "punto por punto contra el repo estan en la 2026-10-14-031 (commit de documentos @@fb033b2@@); lo que cambia de "
    "wording y el plan de cinco sellos estan ahi.%%"
)

NUEVO_032 = q(
    "- **H_RIVAL y H_TAU_JUSTO sellados, sin script (2026-10-14-032, 15-oct 00:37):** rama @@titan/rival-2026-10-15@@, "
    "sello @@05a574c@@ (solo @@tools/rival/SELLO-RIVAL.md@@, md5 ff79011b), anterior a cualquier script como pidio "
    "Abraham. Pregunta: si W, la red con tau elegida de H_TAU, le gana por mas de 1 punto a tres rivales entrenados con "
    "el mismo presupuesto (10 candidatas, 5 pliegues modulo 5, como tau) y las mismas 564 entradas. Rivales: RIDGE "
    "(10 lambdas, forma dual), el MLP de la 005 (semillas 0 a 9) y REGLA_TAU (la regla con integrador por canal, "
    "semillas 10 a 19; si W no le gana por el margen, H_TAU_JUSTO sale REFUTADA). Metrica: acierto por semilla de "
    "prueba (12 a 21); bootstrap de semillas, IC90 con Bonferroni por 3; margen 0,01. Control positivo: el ridge nuevo "
    "reproduce los 0,9935 de la 015 en las 6 celdas a 0,0010 o menos. Limitaciones declaradas: una red elegida por "
    "celda (el IC no cubre la variacion entre redes) y la secundaria del factorial 3 con 10 semillas de tau (con 30 "
    "seria mas fiable). El instrumento entra en un commit aparte; la corrida, solo con su @@CORRER@@.%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 21:36 (America/Buenos_Aires), con la respuesta 2026-10-14-029.",
     "**Última actualización:** 2026-10-15, 00:41 (America/Buenos_Aires), con las respuestas 2026-10-14-030 a "
     "2026-10-14-032."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-029) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-032) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); ",
     NUEVO_030 + NUEVO_031 + NUEVO_032 + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del "
     "depósito de la v2 (publicar, solo con su sí), y antes de depositar, si Z_CP y la RDI se reproducen o salen del "
     "titulo y del resumen (2026-10-14-031); "),
    ("leer H_DEBILES cuando termine (corre desde las 17:53, run 38635900391, 2026-10-14-020); ",
     "relanzar las 2 celdas de H_DEBILES que perdio Actions (t3c3 y t8c0; el agregado dio INVALIDO, 2026-10-14-030); "),
    (q("correr H_REUSO, sellado en la 2026-10-14-029 (su @@CORRER@@, unos 40 minutos); "),
     q("sellar H_REUSO_ESTRICTO, con el nulo que conserva la clase del destino (2026-10-14-030); escribir el "
       "instrumento de H_RIVAL y su humo ciego, y despues su @@CORRER@@ (2026-10-14-032); ")),
    ("sellar H_TAU_JUSTO y una segunda versión del programa de la barra (2026-10-14-015); ",
     "una segunda versión del programa de la barra (2026-10-14-015; H_TAU_JUSTO ya va sellado dentro de H_RIVAL, "
     "2026-10-14-032); "),
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
