#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-002 (BANC bajado y medido, nucleo aparte, H_TAU y nucleo sellados).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-002.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

NUEVO = (
    "- **BANC bajado y medido; núcleo aparte; H_TAU y núcleo sellados (2026-10-14-002), rama "
    "`titan/htau-nucleo-banc-2026-10-14`:**\n"
    "  - BANC v888 en brain-env (`/workspace/banc_888/`): meta md5 `8c2b93a6`, aristas v3 md5 `08542b07`, iguales al "
    "bucket público. Las aristas usan `root_888`, no `root_id`.\n"
    "  - Las 6 DN tienen pareja del mismo tipo en BANC; entradas con pareja 291/564 (51,6 %) por `fafb_match`, 363 "
    "(64,4 %) por alguna vía.\n"
    "  - De las aristas de R2 evaluables (782.453), el 39,8 % está en BANC: 28,9 % con 1 a 4 sinapsis, 60,0 % con 5 a 9, "
    "77,2 % con 10 a 19 y 92,4 % con 20 o más. Núcleo de Schlegel 77,0 % contra 32,7 % del resto. Sin nulo de parejas "
    "al azar (NO MEDIDO).\n"
    "  - Núcleo de Schlegel de R2 como pieza suelta: 603.219 aristas (14,96 %) con el 56,97 % de las sinapsis, 6/6 DN, "
    "563/564 entradas; huella `69255109`.\n"
    "  - H_TAU sellado (`tools/htau/SELLO-HTAU.md`): candidatas tau 10 a 19, elección por validación cruzada en el "
    "entrenamiento, pruebas nuevas 12 a 21, margen 0,01. 6 trabajos de Actions, unas 2,5 h. Se dispara con "
    "`results/htau_2026-10-14/CORRER`.\n"
    "  - Núcleo sellado (`tools/nucleo/SELLO-NUCLEO.md`): H_CONSENSO (no perder más de 1 punto contra R2 y ganarle a 50 "
    "SL + 50 T). 80 trabajos de Actions, cerca de 1,5 h. Se dispara con `results/nucleo_2026-10-14/CORRER`.\n"
)

R = [
    ("**Última actualización:** 2026-10-14, 08:25 (America/Buenos_Aires), con la respuesta 2026-10-14-001.",
     "**Última actualización:** 2026-10-14, 11:30 (America/Buenos_Aires), con la respuesta 2026-10-14-002."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-14-001) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-002) · manda sobre el resto"),
    ("- **Espera decisión de Abraham:** qué sigue tras el factorial 4 (sellar H_TAU, el núcleo conservado, la demo de "
     "aviso de choque o bajar BANC; 2026-10-14-001); merge",
     NUEVO + "- **Espera decisión de Abraham:** correr H_TAU y el núcleo, sellados en la 2026-10-14-002 (cada uno con su "
     "`CORRER`); el nulo del emparejado BANC; merge"),
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
