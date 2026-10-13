#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 2026-10-13-004 (factorial 2 sellado) y la 005 (posicionamiento).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13-005.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

NUEVO = (
    "- **Factorial 2 sellado (2026-10-13-004), sin disparar.** Rama `titan/factorial2-mosca-2026-10-13`, sello `9442fdf` "
    "(instrumento `798a824c…`, agregador `150b6f08…`, workflow `b497fe0d…`).\n"
    "  - La regla usa las mismas entradas que la red (40 en M46, 418 en R1, 564 en R2).\n"
    "  - τ y ruido por `root_id`: las DN tienen el mismo τ en los tres recortes.\n"
    "  - Semillas: τ 0..9 × prueba 2..11 (R2: 3 × 5).\n"
    "  - Margen 0,01, con bootstrap de dos vías y Bonferroni sobre 7.\n"
    "  - R2 (33.489 neuronas, 4.031.897 aristas) va a Actions y no a Kaggle: 0,79 s por ensayo en brain-env, techo de 2,7 h por trabajo.\n"
    "  - Humo 8/8 VÁLIDO y ancla exacta.\n"
    "  - Se dispara pusheando `results/factorial2_2026-10-13/CORRER`.\n"
    "- **Posicionamiento (2026-10-13-005): no hay neurona nueva.**\n"
    "  - La líquida nativa de SparseLTC (τ / (1 + g·|drive|)) es de la familia LTC (Hasani et al., AAAI 2021).\n"
    "  - La que ganó entrenada en el escape (t = sigmoid(b + Vx·x + Vh·z), z ← (1 − t)·z + t·tanh(·)) es la actualización "
    "de una GRU sin compuerta de reset (Cho et al., EMNLP 2014); en DualBrain lleva además LayerNorm.\n"
    "  - Antecedentes directos: LTC sobre cableado inspirado en C. elegans (Lechner et al., Nat Mach Intell 2020) y τ "
    "entrenadas por tipo sobre 45.669 neuronas del sistema visual de la mosca (Lappalainen et al., Nature 2024).\n"
    "  - Lo propio:\n"
    "    - dinámica líquida sobre el cableado exacto de FlyWire;\n"
    "    - el banco sellado (nulos SL y T, regla rival, ancla, réplica en Actions);\n"
    "    - el resultado de que la líquida plena entrenada le gana a su control con los mismos parámetros (013 y 014).\n"
    "  - Sin entrenar, la nativa empata con la de tasa en R1 (factorial 1).\n"
    "  - El banco sólo corrió con FlyWire v783; otros conectomas NO MEDIDO (lee columnas de FlyWire).\n"
    "  - Papers: el Paper 1 (v1.0 en Zenodo, v2.0 sin depositar) y el de DualBrain (feb 2026, `dualbrain/docs/01-paper-dualbrain.md`, "
    "depósito NO VERIFICADO; su README marca que faltan `dbc3_motor.h` y el script del benchmark DBC3-v3).\n"
    "  - Aplicaciones medidas fuera de simulación: ninguna.\n"
)

VIEJA_ESPERA = ("- **Espera decisión de Abraham:** sellar el factorial 2 (la regla con los mismos sensores, varias semillas de τ y "
                "de prueba, margen de equivalencia, R2 en Kaggle);")
NUEVA_ESPERA = NUEVO + ("- **Espera decisión de Abraham:** correr el factorial 2 (sellado en `9442fdf`: pushear "
                        "`results/factorial2_2026-10-13/CORRER`);")

R = [
    ("**Última actualización:** 2026-10-13, 08:30 (America/Buenos_Aires), con la respuesta 2026-10-13-003.",
     "**Última actualización:** 2026-10-13, 09:40 (America/Buenos_Aires), con la respuesta 2026-10-13-005."),
    ("## Madrugada y mañana del 13-oct (019 a 2026-10-13-003) · manda sobre el resto",
     "## Madrugada y mañana del 13-oct (019 a 2026-10-13-005) · manda sobre el resto"),
    (VIEJA_ESPERA, NUEVA_ESPERA),
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
