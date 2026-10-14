#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-004 (v2 mergeada en main, H_TAU y nucleo corriendo en Actions).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-004.py docs/agents/CONTEXTO-drosophila-fep.md
Las comillas invertidas y los saltos se arman con chr() para que el archivo no lleve caracteres de escape.
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
    "- **v2 en main y los dos sellos corriendo (2026-10-14-004, ClickKit @@merge_y_correr_004@@, 11:28):**%%"
    "  - PR #27 mergeado en main (@@6785316@@); la prueba de mezcla contra @@7eec778@@ dio limpia. "
    "@@tools/zenodo/depositar_v2.py --verificar@@ sobre main da PASS (PDF v2.0 @@6e849bf2@@, erratum v1.0 @@05052e6e@@).%%"
    "  - @@results/htau_2026-10-14/CORRER@@ y @@results/nucleo_2026-10-14/CORRER@@ pusheados en @@9545af4@@ "
    "(rama @@titan/htau-nucleo-banc-2026-10-14@@, nada sellado cambio). @@htau-mosca@@ y @@nucleo-mosca@@ arrancaron "
    "14:30 UTC; estimado: nucleo hacia las 13:30 y H_TAU hacia las 14:30 de Buenos Aires (NO MEDIDO).%%"
    "  - El deposito en Zenodo sigue esperando el token (borrador primero; publicar solo con el si de Abraham).%%"
)

R = [
    ("**Última actualización:** 2026-10-14, 11:30 (America/Buenos_Aires), con la respuesta 2026-10-14-002.",
     "**Última actualización:** 2026-10-14, 11:45 (America/Buenos_Aires), con la respuesta 2026-10-14-004."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-002) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-004) · manda sobre el resto"),
    (q("- **Espera decisión de Abraham:** correr H_TAU y el núcleo, sellados en la 2026-10-14-002 (cada uno con su "
       "@@CORRER@@); el nulo del emparejado BANC; merge del PR #27 (la v2 ya está lista, 2026-10-13-014) y token de "
       "Zenodo; responderle a Tao en su PR."),
     NUEVO + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí); leer H_TAU y el núcleo cuando terminen (2026-10-14-004); el esqueleto del Paper 2; el nulo "
     "del emparejado BANC; responderle a Tao en su PR."),
]
for a, b in R:
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s" % (n, a[:60]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
for a, b in R:
    t = t.replace(a, b)
open(ruta, "w", encoding="utf-8").write(t)
print("md5 despues", hashlib.md5(t.encode("utf-8")).hexdigest())
print("PARCHE OK")
