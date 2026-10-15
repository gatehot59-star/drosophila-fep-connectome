#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-034 (H_RIVAL completo y el borrador de la v2 en Zenodo).

Agrega el veredicto de H_RIVAL y H_TAU_JUSTO, el estado de la replica, el borrador de la v2 (sin publicar)
y la lista de espera al dia. Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-034.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_034 = q(
    "- **H_RIVAL REFUTADA en Actions y H_TAU_JUSTO SIN_DECIDIR (2026-10-14-034, aprobado por Abraham a las 07:36):** "
    "run 38721794594 desde el @@CORRER@@ @@000d486@@, bot @@576fc4c@@, 9 minutos; @@agregado.log@@ md5 38d473cc. "
    "CHEQUEO VALIDO: los controles de las 6 celdas en verde y CONTROL_RIDGE_015 6/6 exacto. Acierto medio en las "
    "pruebas 12 a 21: la mosca (W elegida) 0,9413 a 0,9467; RIDGE 0,9894 a 0,9988; MLP 0,9879 a 0,9957; REGLA_TAU "
    "0,9308 a 0,9352; la regla propia 0,9234 a 0,9289. Primaria: contra RIDGE D = -0,0503 [-0,0516, -0,0488] y contra "
    "MLP D = -0,0479 [-0,0494, -0,0465], NO_SUPERA (pierde); contra REGLA_TAU D = +0,0119 [+0,0096, +0,0150], "
    "SIN_DECIDIR (el piso queda debajo del margen de 1 punto). Secundaria, descriptiva: contra REGLA_TAU +0,0032 "
    "[-0,0068, +0,0106]. Lectura: con lector entrenado sobre las mismas 564 entradas, un ridge le gana a la mosca por "
    "5 puntos; darle a la regla la τ elegida baja la ventaja de la mosca de 1,78 a 1,19 puntos. La replica en "
    "brain-env se corto (el contenedor se detuvo a las 07:58) y se relanzo a las 08:18; si una etiqueta por rival "
    "difiere entre maquinas, pasa a SIN_DECIDIR (NO_SE_REPLICA).%%"
    "- **Borrador de la v2 del Paper 1 en Zenodo, sin publicar (2026-10-14-034, pedido de Abraham a las 07:50):** "
    "@@tools/zenodo/depositar_v2.py --borrador@@ desde un clon limpio de main (@@fe4a088@@), con @@--verificar@@ PASS "
    "antes. Nueva version del concepto 10.5281/zenodo.19136947: borrador 23393412, DOI reservado "
    "10.5281/zenodo.23393412; los dos PDF con el md5 que calculo Zenodo igual al sellado (6e849bf2 y 05052e6e); "
    "estado @@unsubmitted@@ y el registro publico da 404. Recibo: @@docs/v2/recibo-borrador-v2.0.json@@. El token no "
    "quedo en disco, en git ni en los recibos (medido). El Paper 2 y el Paper 3 no se subieron: son esqueletos "
    "(@@docs/paper2/paper2-esqueleto.md@@ y @@docs/paper3/paper3-esqueleto.md@@, en sus ramas), sin manuscrito, PDF ni "
    "metadatos.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 02:08 (America/Buenos_Aires), con la respuesta 2026-10-14-033.",
     "**Última actualización:** 2026-10-15, 08:19 (America/Buenos_Aires), con la respuesta 2026-10-14-034."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-033) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-034) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, solo con "
     "su sí), y antes de depositar, si Z_CP y la RDI se reproducen o salen del titulo y del resumen (2026-10-14-031); ",
     NUEVO_034 + "- **Espera decisión de Abraham:** publicar o descartar el borrador de la v2 en Zenodo (23393412; "
     "publicar, solo con su sí), y antes de publicar, si Z_CP y la RDI se reproducen o salen del titulo y del resumen "
     "(2026-10-14-031); revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); escribir el Paper 2 "
     "y el Paper 3, con H_RIVAL adentro, antes de depositarlos (2026-10-14-034); "),
    (q("disparar el @@CORRER@@ de H_RIVAL, con el instrumento y el humo ciego listos (2026-10-14-033); "), ""),
    ("(2026-10-14-015; H_TAU_JUSTO ya va sellado dentro de H_RIVAL, 2026-10-14-032); ",
     "(2026-10-14-015; H_TAU_JUSTO dio SIN_DECIDIR, 2026-10-14-034); "),
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
