#!/usr/bin/env python3
"""Segundo cierre de la 2026-10-14-061: en el ARRANQUE, «auditar el laboratorio» y «pedido a Tao» eran dos links a la misma tarea; queda uno solo. Agrega a la 061 la segunda vuelta de la prueba del arranque.

Cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir nada.
Uso (desde la raiz del repo): python3 tools/arranque/cierre2_2026-10-14-061.py
"""
import hashlib
import sys

NL = chr(10)
ARR = "docs/agents/ARRANQUE-NUEVO-CHAT.md"
R061 = "docs/agents/respuestas/2026-10-14-061-arranque-corregido-y-h-pares-datos-medido.md"


def unica(t, a, ruta):
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s :: %s" % (n, ruta, a[:50]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)


arr = open(ARR, encoding="utf-8").read()
a1 = "Tareas: [auditar el laboratorio]("
a2 = "), [pedido a Tao]("
a3 = "), [auditoría de DBC3-live]("
for a in (a1, a2, a3):
    unica(arr, a, ARR)
i = arr.find(a1)
j = arr.find(a2, i)
if j < i:
    print("ABORTA: orden inesperado")
    sys.exit(2)
arr = arr[:i] + "Tareas: [pedido a Tao: auditar el laboratorio](" + arr[j + len(a2):]
arr = arr.replace(a3, ") y [auditoría de DBC3-live](")

r = open(R061, encoding="utf-8").read()
ancla = NL + NL + "--- METODO PROMETEO ---"
unica(r, ancla, R061)
if "Segunda vuelta del agente" in r:
    print("ABORTA: la segunda vuelta ya esta")
    sys.exit(2)
linea = (NL + "- Segunda vuelta del agente, después del push: los cinco problemas quedaron resueltos (la 061 en main, "
         "el blob 00a1a343, el CONTEXTO en la 061 y el Doc con sus dos páginas). Encontró uno nuevo y menor: «auditar el "
         "laboratorio» y «pedido a Tao» eran dos links a la misma tarea; queda uno solo "
         "(tools/arranque/cierre2_2026-10-14-061.py); el ARRANQUE final queda en md5 de659ba5 y blob d2beec25, y lo "
         "confirma el commit del bot del segundo cierre. Su veredicto: arrancaría sin preguntar.")
r = r.replace(ancla, linea + ancla)

open(ARR, "w", encoding="utf-8").write(arr)
open(R061, "w", encoding="utf-8").write(r)
print("md5", hashlib.md5(arr.encode("utf-8")).hexdigest(), ARR)
print("md5", hashlib.md5(r.encode("utf-8")).hexdigest(), R061)
print("CIERRE2 OK")
