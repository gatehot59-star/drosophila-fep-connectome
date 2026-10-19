#!/usr/bin/env python3
"""Cierre de la 2026-10-14-061: pone la tilde que se perdio al pushear («rehizo» por «rehízo») en el ARRANQUE y en el CONTEXTO, y agrega a la 061 la verificacion despues del push.

Reemplazos exactos; cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir nada.
Uso (desde la raiz del repo): python3 tools/arranque/cierre_2026-10-14-061.py
"""
import hashlib
import sys

BT = chr(96)
NL = chr(10)


def q(s):
    return s.replace("@@", BT).replace("%%", NL)


ARR = "docs/agents/ARRANQUE-NUEVO-CHAT.md"
CTX = "docs/agents/CONTEXTO-drosophila-fep.md"
R061 = "docs/agents/respuestas/2026-10-14-061-arranque-corregido-y-h-pares-datos-medido.md"

SECCION_7 = (
    "## 7. Verificación después del push (agregado en el cierre)%%%%"
    "- Commit 82a745d (22:24:48Z). La 061 llegó igual byte a byte: blob 550b9783 en git y en el sandbox. El ARRANQUE "
    "y el parche llegaron con una tilde de menos, «rehizo» por «rehízo» (una línea de diff en cada uno; blob d682cc4a "
    "contra 00a1a343 y a488a09b contra 179ef6fc).%%"
    "- Bot ff2d2fb (22:24:55Z): parche aplicado, tres anclas con una aparición cada una, md5 del CONTEXTO de 1173ec1f "
    "a a07976bd. El parche de git (md5 b6bc1207), corrido en el sandbox sobre la copia real, da el mismo a07976bd.%%"
    "- Cierre (@@tools/arranque/cierre_2026-10-14-061.py@@, aplicado por Actions): pone la tilde en el ARRANQUE y en "
    "el CONTEXTO. Esperado y probado en el sandbox: ARRANQUE md5 3dcfb259 y blob 00a1a343, iguales a la copia del "
    "sandbox y del Doc; CONTEXTO md5 de0f8711, igual a la prueba del parche en el sandbox. Lo confirma el commit del "
    "bot «cierre(2026-10-14-061)». El parche que quedó en git conserva «rehizo»: es el que corrió.%%%%"
    "--- METODO PROMETEO ---"
)

R = [
    (ARR, "y se rehizo a mano sobre el de la 060 porque", "y se rehízo a mano sobre el de la 060 porque"),
    (CTX, "el índice v2 se rehizo a mano sobre el de la 060.", "el índice v2 se rehízo a mano sobre el de la 060."),
    (R061, "--- METODO PROMETEO ---", q(SECCION_7)),
]
nuevos = {}
for ruta, a, b in R:
    t = nuevos.get(ruta) or open(ruta, encoding="utf-8").read()
    n = t.count(a)
    print("ANCLA apariciones=%d :: %s :: %s" % (n, ruta, a[:50]))
    if n != 1:
        print("ABORTA: ancla no unica")
        sys.exit(2)
    if ruta == R061 and "## 7. Verificación después del push" in t:
        print("ABORTA: la seccion 7 ya esta")
        sys.exit(2)
    nuevos[ruta] = t.replace(a, b)
for ruta, t in nuevos.items():
    open(ruta, "w", encoding="utf-8").write(t)
    print("md5", hashlib.md5(t.encode("utf-8")).hexdigest(), ruta)
print("CIERRE OK")
