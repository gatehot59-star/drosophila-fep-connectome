#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la respuesta 2026-10-14-039 (H_TAU_LIBRE sellado).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-039.py docs/agents/CONTEXTO-drosophila-fep.md
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

NUEVO_039 = q(
    "- **H_TAU_LIBRE sellado, sin script (2026-10-14-039, ClickKit @@sellar_control_tau_039@@, 18:41):** rama "
    "@@titan/taulibre-2026-10-15@@ (desde @@8d305e9@@), sello @@fec8472@@ (@@tools/taulibre/SELLO-TAU-LIBRE.md@@, md5 "
    "3886aa58), solo el documento. Controla la asimetria de la 038: la tau 10 la eligio H_TAU sobre la red real y los "
    "nulos la heredaron. Aca nadie elige: real y nulos con taus frescas 20 a 29, apareadas (nulo k con tau 20 + k mod "
    "10), los mismos 40 nulos SL y T de H_LECTOR en c2 y c5, prueba 12, mismo lector L. SOSTENIDA si el real supera por "
    "mas de 1 punto en las 4 combinaciones (p apareado <= 0,05). Controles nuevos: REPRO_LECTOR, NULOS_IGUAL_LECTOR, "
    "TAU_FRESCA. Expectativa declarada: c5 probablemente sobrevive, c2 abierta.%%"
)

R = [
    ("**Última actualización:** 2026-10-15, 16:50 (America/Buenos_Aires), con la respuesta 2026-10-14-038.",
     "**Última actualización:** 2026-10-15, 18:44 (America/Buenos_Aires), con la respuesta 2026-10-14-039."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-038) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-039) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat (2026-10-14-034); ",
     NUEVO_039 + "- **Espera decisión de Abraham:** revocar el token de Zenodo, que quedo escrito en el chat "
     "(2026-10-14-034); "),
    ("auditar H_LECTOR (sobre todo la tau elegida en la red real) y decidir si entra al Paper 2; la replica de la "
     "primaria corre en brain-env despues de la de H_RIVAL (2026-10-14-038); ",
     q("escribir el instrumento de H_TAU_LIBRE y su humo ciego, y despues su @@CORRER@@; H_LECTOR entra al Paper 2 "
       "recien con H_TAU_LIBRE y la replica de la primaria en brain-env (2026-10-14-039); ")),
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
