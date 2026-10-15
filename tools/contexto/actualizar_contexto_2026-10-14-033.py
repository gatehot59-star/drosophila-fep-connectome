#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-033 (instrumento de H_RIVAL y humo ciego).

Agrega solo el estado del sello (instrumento y humo, sin aciertos de rivales) y la lista de espera al dia.
Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-033.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_033 = q(
    "- **Instrumento de H_RIVAL y humo ciego, sin aciertos de rivales (2026-10-14-033, ClickKit "
    "@@instrumento_rival_034@@, 01:28):** rama @@titan/rival-2026-10-15@@, instrumento @@04d0635@@, despues del sello "
    "@@05a574c@@: @@rival_mosca.py@@ (md5 774232f5), @@agregar_rival.py@@ (f66b2250), @@prueba_rival.py@@ (b7b9d411) "
    "y los workflows @@rival-humo@@ y @@rival-mosca@@. Ejecutado en brain-env antes de commitear. Prueba 18/18, con un "
    "rojo a proposito. Control positivo: el ridge nuevo reproduce exactos los seis valores de la 015 (0,9935, 0,9595, "
    "0,9935, 0,9575, 0,9940 y 0,9590), con 0 predicciones distintas del ridge de ept. Humo en Actions (run "
    "38684660391, bot @@b964058@@): las 6 celdas VALIDO, con REPRO_REGLA 20/20 y REPRO_W 110/110 por celda, "
    "CONTROL_MLP_005 480/480 y el negativo en 0,5000 contra un azar de 0,5000; brain-env da lo mismo en c0. Desvio "
    "declarado: @@ept.mlp_mux@@ trae fijas las clases de la 005, asi que el MLP es su bucle linea por linea con las "
    "clases de @@tm.CLASES@@, controlado contra @@ept.mlp_mux@@. Ningun acierto de rival visto. La corrida completa "
    "espera el @@CORRER@@ de Abraham: unos 10 minutos por celda en Actions; la replica en brain-env, unas 9 horas.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 00:41 (America/Buenos_Aires), con las respuestas 2026-10-14-030 a "
     "2026-10-14-032.",
     "**Última actualización:** 2026-10-15, 02:08 (America/Buenos_Aires), con la respuesta 2026-10-14-033."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-032) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-033) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, solo con "
     "su sí), y antes de depositar",
     NUEVO_033 + "- **Espera decisión de Abraham:** el token de Zenodo para el borrador del depósito de la v2 (publicar, "
     "solo con su sí), y antes de depositar"),
    (q("escribir el instrumento de H_RIVAL y su humo ciego, y despues su @@CORRER@@ (2026-10-14-032); "),
     q("disparar el @@CORRER@@ de H_RIVAL, con el instrumento y el humo ciego listos (2026-10-14-033); ")),
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
