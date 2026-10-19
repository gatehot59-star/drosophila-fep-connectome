#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 059 (H_PARES_DATOS sellado y humo), la 060 (ARRANQUE), la auditoria 2026-10-19-01 y la 061 (H_PARES_DATOS medido y ARRANQUE corregido).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-061.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO = (
    "- **H_PARES_DATOS (2026-10-14-059 y 2026-10-14-061, pedido de Abraham 18-oct 22:30 «Sellá H_PARES_DATOS y "
    "ejecutá la curva»):** sello 0d30190 en @@titan/pares-datos-2026-10-18@@ antes del código "
    "(@@tools/pares/SELLO-PARES-DATOS.md@@); instrumento probado en brain-env y en el humo 2 de Actions (ccf8d19: "
    "prueba 6/6 VALIDO, mosca idéntica byte a byte al humo 1, crudo VALIDO). CORRER 1f04d2c el 19-oct a las 14:07 "
    "(17:07:45Z; el archivo CORRER dice ~17:15Z y está mal); el bot cerró la medición en e5db870 a las 14:34. "
    "Agregado VALIDO (12/12 json, MISMO_SCRIPT, SUBCONJUNTOS, PLAN_COMPLETO, REPRO_TAULIBRE y REPRO_CRUDO True): "
    "D_CRUDO +0,0401 [+0,0287; +0,0508], D_PCA_L +0,1520 [+0,1425; +0,1616], D_PROY_L +0,0904 [+0,0806; +0,1000]; "
    "E_CRUDO -0,0382 [-0,0599; -0,0170], E_PCA_L -0,2761 [-0,3054; -0,2482], E_PROY_L -0,1198 [-0,1325; -0,1065]: "
    "**H_DATOS_EMBUDO, H_DATOS_CRUDO y H_DATOS_PRIMER_DIA SOSTENIDAS.** Con pocos ensayos etiquetados (6 a 768), los "
    "240 rasgos de la mosca con lector entrenado le ganan a PCA y a la proyección aleatoria del mismo tamaño y al "
    "lector crudo; con 96 etiquetados ningún brazo artificial alcanza a la mosca sin etiquetas (W 0,9276 en c2 y "
    "0,9222 en c5). Para alcanzar a W (promedio de celdas): mosca 96, crudo 192, PCA 384, proyección 2.400. Con "
    "2.400 etiquetados el crudo y PCA empatan o pasan a la mosca en c2 (0,9995 contra 0,9943). Límites del sello: 2 "
    "de 6 celdas, una prueba, W sabe qué ensayos son fondo y PCA ve los 2.400 sin etiqueta. El agregado se repitió "
    "en brain-env sobre los mismos 12 json (MD5SUMS 12 OK) y dio las mismas 52 líneas. Robustez, reservorio y la "
    "réplica de los 12 trabajos en brain-env: NO MEDIDOS.%%"
    "- **ARRANQUE para un chat nuevo (2026-10-14-060, pedido 19-oct 13:23) y su auditoría (2026-10-19-01, pedido "
    "15:13):** la 060 dejó @@docs/agents/ARRANQUE-NUEVO-CHAT.md@@, @@tools/arranque/generar_indice.py@@ y "
    "@@docs/agents/INDICE-COMPLETO-GIT.md@@ (bot 18881ff). La auditoría (misma instancia, no independiente) le "
    "encontró 10 rojos y 11 confirmados: CORRER a las 14:07 y no a las 14:15; la curva ya había terminado; el link "
    "al Doc le llegó a Abraham como «#»; la copia de git iba sin tildes y con otro encabezado; el índice de git deja "
    "sin Doc a 183 de 280 respuestas y su script no es el que se probó; la lista de ClickUp no estaba completa (6 al "
    "30-sep), contaba filas y no Docs y metía títulos de MUDH-Mobile; brain-env no estuvo caído (fallaba el "
    "túnel); el índice nunca se adjuntó al Doc; mojo-absoluto tiene 90 respuestas y no 88.%%"
    "- **ARRANQUE corregido (2026-10-14-061, pedido 19-oct 18:21 «generar el documento sin errores para iniciar en "
    "otra instancia»):** @@docs/agents/ARRANQUE-NUEVO-CHAT.md@@ reescrito con tildes y los 10 rojos corregidos; "
    "mismo texto en la segunda página del Doc 061. Índice de ClickUp v2 adjunto al Doc 061: 472 títulos distintos "
    "del proyecto (sin MUDH-Mobile, REA, Corpus ni ingresos) y las 280 respuestas de git con su Doc (224 con Doc; de "
    "las 56 sin Doc, 34 son la 001 a la 040, anteriores a la regla del Doc espejo). El generador del índice de git "
    "que está en git (a9b6352d) da en el repo de prueba el mismo índice que el que se probó (1c8e36b1), salvo una "
    "línea de redacción. El sandbox de ClickUp se reinició a mitad del turno y se llevó la enumeración fina de "
    "ClickUp; el índice v2 se rehizo a mano sobre el de la 060.%%"
)

R = [
    ("**Última actualización:** 2026-10-17, 19:10 (America/Buenos_Aires), con la respuesta 2026-10-14-058.",
     "**Última actualización:** 2026-10-19, 19:40 (America/Buenos_Aires), con la respuesta 2026-10-14-061."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-058) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-061) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); "
     "si se sella H_PARES y por cual pieza se empieza (datos y embudo, robustez o reservorio; 2026-10-14-058); ",
     NUEVO + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); si se sellan las otras dos piezas de H_PARES, robustez sin reentrenar y reservorio (la de "
     "datos ya está medida y SOSTENIDA, 2026-10-14-061); si H_PARES_DATOS entra al Paper 2; probar el ARRANQUE "
     "pegándolo en un chat nuevo (2026-10-14-061); "),
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
