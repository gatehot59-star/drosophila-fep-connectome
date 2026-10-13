#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-015 (factorial 4 sellado en Kaggle: el banco con el cerebro entero).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-015.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

R = [
    ("**Última actualización:** 2026-10-13, 18:45 (America/Buenos_Aires), con la respuesta 2026-10-13-014.",
     "**Última actualización:** 2026-10-13, 21:05 (America/Buenos_Aires), con la respuesta 2026-10-13-015."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-014) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-015) · manda sobre el resto"),
    ("costaría unas 3,7 veces R2 si el costo sigue a las conexiones (NO MEDIDO); BANC trae",
     "costaría unas 3,7 veces R2 si el costo sigue a las conexiones (estimación; el costo absoluto quedó medido en la "
     "2026-10-13-015: 0,026 s por ensayo en una T4 de Kaggle y 3,2 s en brain-env); BANC trae"),
    ("- **Espera decisión de Abraham:** qué sigue tras el factorial 3; merge del PR #27 (la v2 ya está lista, "
     "2026-10-13-014) y token de Zenodo; responderle a Tao en su PR.",
     "- **Factorial 4 sellado en Kaggle (2026-10-13-015), sin correr:** el banco con el cerebro entero de FlyWire v783 "
     "(138.639 neuronas, 15.091.983 aristas, 6.032.681 inhibitorias, las mismas 564 entradas de R2). Rama "
     "`titan/factorial4-cerebro-entero-2026-10-13`: instrumento `ace8fe7` (`cerebro_mosca.py` `36a9f005…`, motor torch "
     "float64) y sello `431b7bd` (`tools/factorial4/SELLO-FACTORIAL4.md`).\n"
     "  - Humo medido, todo VÁLIDO, en brain-env (CPU) y en tres sesiones T4 de Kaggle: paridad torch contra numpy de "
     "4e-16 o menos en R1 y en el cerebro entero, y **REPRO_R2: la T4 reproduce exacto el 0,9465 de R2 del factorial 3**, "
     "en cada una de las dos GPU. 0,026 s por ensayo por T4, igual con dos procesos a la vez; 3,1 GB de GPU.\n"
     "  - Plan: las 600 corridas del factorial 3 + 50 SL + 50 T; 2 kernels T4 x2 de `abrahammendieta`, 4 carriles, 22 "
     "trabajos; unas 3,6 h de reloj y 7 h de cuota de GPU (cuánta queda: NO MEDIDO).\n"
     "  - Hipótesis pre-registradas: H_SUPERA_CE (contra su regla, margen 1 punto), H_ESCALA (CE contra R2 en los mismos "
     "ensayos) y H_CABLEADO_CE (50 SL y 50 T, Holm). Agregador probado 5/5 en clon fresco del sello.\n"
     "  - La salida grande (unos 1,6 MB de json con la predicción de cada ensayo) no tiene vía directa a git desde "
     "brain-env: irá compacta (agregado, MD5SUMS, recibos, tablas) salvo que haya un token para este repo.\n"
     "- **Espera decisión de Abraham:** disparar el factorial 4 (unas 7 h de cuota de GPU de `abrahammendieta`); merge "
     "del PR #27 (la v2 ya está lista, 2026-10-13-014) y token de Zenodo; responderle a Tao en su PR."),
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
