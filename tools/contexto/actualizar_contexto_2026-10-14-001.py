#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-14-001 (factorial 4 leido: VALIDO, el cerebro entero da lo mismo que R2).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-14-001.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

LEIDO = (
    "  - **Leído (2026-10-14-001): VÁLIDO.** Los dos kernels terminaron con rc 0 (a 11.755 s, b 13.519 s: unas 7,0 h de "
    "sesión T4) y los 22 trabajos también; todos los chequeos del agregador sellado dan True (recibos, integridad 22/22, "
    "plan 600, REPRO_R2 0,9465 en los 4 carriles, REAL_IGUAL, 50 + 50 nulos, reproduce la primaria del factorial 3, misma "
    "regla y mismas DN que el 3).\n"
    "  - **H_ESCALA REFUTADA: el cerebro entero da lo mismo que R2.** CE menos R2 +0,01 puntos, IC90 [−0,01; +0,04], "
    "EQUIVALENTE en las 6 celdas; la misma predicción en 1.198.955 de 1.200.000 ensayos (99,913 %). En esta tarea, las "
    "105.150 neuronas que están fuera de R2 (33.489) no mueven la lectura de las descendentes.\n"
    "  - **H_SUPERA_CE SIN_DECIDIR:** 0,9355 contra su regla 0,9268, +0,86 puntos, IC90 [+0,11; +1,51], NO_INFERIOR, y "
    "NO_INFERIOR en las 6 celdas: el mismo empate técnico de R2 en el factorial 3.\n"
    "  - **H_CABLEADO_CE SOSTENIDA:** 0,9465 contra 50 SL (media 0,6488, máx 0,7935) y 50 T (media 0,7596, máx 0,8395); "
    "ninguno igual o mejor; p 0,0196 cada uno, Holm 0,0392.\n"
    "  - **Post-hoc, no sellado: lo que decide si la red le gana a su regla es la semilla de tau, no el tamaño.** En 8 de "
    "10 semillas CE le gana en 58 a 60 de las 60 corridas (+1,28 a +1,71 puntos); en la 5 no le gana en ninguna (−2,30) y "
    "en la 7 en 6 de 60 (−0,85); R2 hace lo mismo semilla por semilla. Candidata **H_TAU**, sin sellar: con las constantes "
    "de tiempo elegidas o aprendidas solo con el entrenamiento, ganarle a la regla por más de 1 punto en la prueba. R2 "
    "alcanza y corre en CPU: va a Actions sin gastar GPU.\n"
    "  - En git quedó compacto, en la rama del factorial 4 (`87be763`): `results/factorial4_2026-10-13/` (`agregado.log` "
    "`539733b9`, `corridas.csv` `b58be308`, `nulos.csv` `94811363`, `MD5SUMS.txt` `7f396757` con las 50 salidas de "
    "Kaggle, `relectura_desde_csv.log` `a778e608`) y `tools/factorial4/releer_factorial4_desde_csv.py` (`045caf9e`), que "
    "rehace desde git la primaria, la escala y los nulos con el bootstrap sellado: 18 de 18 líneas iguales al agregado, y "
    "con una sola corrida tocada da 4 distintas y sale con 1. Los json por ensayo (unos 1,6 MB) y los dos recibos quedan "
    "por md5: sin un token para este repo no hay vía directa a git desde brain-env."
)

R = [
    ("**Última actualización:** 2026-10-13, 21:15 (America/Buenos_Aires), con la respuesta 2026-10-13-016.",
     "**Última actualización:** 2026-10-14, 08:25 (America/Buenos_Aires), con la respuesta 2026-10-14-001."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-016) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-14-001) · manda sobre el resto"),
    ("- **Factorial 4 sellado en Kaggle (2026-10-13-015) y disparado (2026-10-13-016): corriendo y sin leer:**",
     "- **Factorial 4 sellado en Kaggle (2026-10-13-015), disparado (2026-10-13-016) y leído (2026-10-14-001): VÁLIDO, "
     "el cerebro entero da lo mismo que R2:**"),
    ("  - La salida grande (unos 1,6 MB de json con la predicción de cada ensayo) no tiene vía directa a git desde "
     "brain-env: irá compacta (agregado, MD5SUMS, recibos, tablas) salvo que haya un token para este repo.",
     LEIDO),
    ("- **Corriendo:** kernels `f4-ce-a-2026-10-13` y `f4-ce-b-2026-10-13` de `abrahammendieta`, rearmados desde un clon "
     "fresco de `431b7bd` con los md5 sellados (`d76dc652`, `09ffa774`), empujados a las 00:13 UTC del 14-oct a pedido de "
     "Abraham (ClickKit `correr_factorial4_015`) y RUNNING a las 00:14 UTC. Fin estimado entre 03:30 y 04:00 UTC. Al "
     "terminar: `kaggle kernels output` de los dos, `agregar_factorial4.py` y commit del agregado, MD5SUMS y recibos.\n",
     ""),
    ("- **Espera decisión de Abraham:** merge del PR #27 (la v2 ya está lista, 2026-10-13-014)",
     "- **Espera decisión de Abraham:** qué sigue tras el factorial 4 (sellar H_TAU, el núcleo conservado, la demo de "
     "aviso de choque o bajar BANC; 2026-10-14-001); merge del PR #27 (la v2 ya está lista, 2026-10-13-014)"),
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
