#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-041 (H_TAU_LIBRE medido en Actions).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-041.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_041 = q(
    "- **H_TAU_LIBRE SOSTENIDA en Actions (2026-10-14-041, pedido de Abraham 19:38):** CORRER @@291a2f2@@, bot "
    "@@e7ada46@@ (@@results/taulibre_2026-10-15/@@, agregado.log md5 64f17f1a, MD5SUMS 62 de 62 OK), 20 de 20 json "
    "VALIDO, REPRO_LECTOR exacto en c2 y c5. Con taus que nadie eligio (20 a 29) y cada nulo contra la red real de su "
    "misma tau, el real supera a los 40 nulos en las 4 combinaciones, ninguno lo iguala (p = 1/41): SL c2 +0,0362, "
    "SL c5 +0,1219, T c2 +0,0476, T c5 +0,1127. Descriptivo: con L la tau 10 no fue una ventaja, quedo por debajo de "
    "las 10 frescas en las dos celdas (c2 0,9910 contra 0,9930 a 0,9955; c5 0,9930 contra 0,9940 a 0,9955); el delta "
    "por tau mas chico es +0,0145 (SL c2, tau 26). La asimetria de la 038 queda descartada como explicacion. "
    "REPRO_LECTOR de c2 tambien exacto en brain-env (otra maquina).%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 19:31 (America/Buenos_Aires), con la respuesta 2026-10-14-040.",
     "**Última actualización:** 2026-10-15, 21:33 (America/Buenos_Aires), con la respuesta 2026-10-14-041."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-040) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-041) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_041 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    (q("disparar el @@CORRER@@ de H_TAU_LIBRE, 20 trabajos en Actions, unas 2 horas; H_LECTOR entra al Paper 2 recien "
       "con H_TAU_LIBRE y la replica de la primaria en brain-env (2026-10-14-040); "),
     "reescribir el Paper 2 alrededor de H_LECTOR y H_TAU_LIBRE, con la replica de la primaria de H_LECTOR en "
     "brain-env como condicion para Zenodo (2026-10-14-041); "),
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
