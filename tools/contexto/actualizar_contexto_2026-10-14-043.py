#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-043 (Paper 3 empujado: los dos nulos de LC6 a GF y la tabla ya publicada).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-043.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_043 = q(
    "- **Paper 3 empujado (2026-10-14-043, pedido de Abraham 22:08):** la discrepancia del nulo de LC6 a GF eran dos "
    "nulos: el CP de la 060 (destinos barajados dentro de @@super_class@@) espera 5,8 y el que preserva neuropilo de la "
    "065 (@@src/escape_neuropil_null.py@@, rama @@titan/twohop-nulls@@) espera 17,2 +- 3,1 (z -5,61, minima de 40 = 12); "
    "manda el segundo. A escala de neuropilo LC6 y la GF comparten PVLP (5.335 sitios, mas que LC4 con 104 aristas); "
    "la distancia entre arboles sigue NO MEDIDA. Los conteos ya estan publicados (Kind et al. 2024, eLife RP 99277, y "
    "el Cell Type Explorer de FAFB, respuestas 066 y 067): el aporte es la expectativa, no el conteo. Esqueleto en "
    "@@titan/paper3-esqueleto-2026-10-14@@ (bot @@7f8b331@@, md5 a904026e), cotejo 127 de 127 y control 2 de 2, con "
    "copias verbatim de la 065, 066, 067 y 038. El vinculo con H_LECTOR en la Discusion queda pendiente del cotejo de "
    "la replica.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 21:59 (America/Buenos_Aires), con la respuesta 2026-10-14-042.",
     "**Última actualización:** 2026-10-15, 22:22 (America/Buenos_Aires), con la respuesta 2026-10-14-043."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-042) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-043) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_043 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); decidir el merge del PR #26 (codigo y logs de la 005 a la 009 del Paper 3) y si se sella la "
     "replica del mapa de salidas en BANC v888 en Actions (2026-10-14-043); "),
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
