#!/usr/bin/env python3
"""Pone al dia el CONTEXTO con la 019, la 2026-10-13-001, la 002 y la 003 (respuesta 2026-10-13-003).

Reemplazos exactos, cada ancla tiene que aparecer una sola vez; si no, aborta sin escribir.
Uso: python3 actualizar_contexto_2026-10-13.py docs/agents/CONTEXTO-drosophila-fep.md
"""
import hashlib
import sys

ruta = sys.argv[1]
t = open(ruta, encoding="utf-8").read()
print("md5 antes", hashlib.md5(t.encode("utf-8")).hexdigest())

NUEVA = """## Madrugada y mañana del 13-oct (019 a 2026-10-13-003) · manda sobre el resto

- **Factorial sellado (019) y corrido (2026-10-13-002): VÁLIDO 9/9.** Rama `titan/factorial-mosca-2026-10-13`: sello `552942f`, resultados del bot `5c4fbac`, post-hoc `19a508c`. El ancla reproduce la 015 exacta en brain-env y en Actions.
  - Veredicto sellado: ALGÚN FACTOR CIERRA LA BRECHA (R1_CON_TASA, R1_CON_LIQ, R1_SIN_LIQ). M46 pierde con las tres neuronas, como en la 015.
  - **Post-hoc, no sellado:** la regla con las mismas 418 entradas de R1 sube a 0,926-0,930, y R1_CON_TASA y R1_CON_LIQ la IGUALAN en 6/6. El «supera» sellado era tener más sensores.
  - El cableado paga dentro de R1: 0,937 contra 50 SL (media 0,774) y 50 T (0,742), p por rango 0,0196.
  - Factores: recorte AYUDA; inhibición AYUDA (en TASA y LIQ solo con amplitud 0,6); LIQ empata con TASA en R1; el LIF armado (corriente fija, paso de 1 ms) DAÑA.
  - **Lectura:** la brecha de la 015 era nuestro recorte. Con 1.504 neuronas reales, la mosca simulada alcanza a su diseño idealizado; no lo supera.
  - La primera corrida en Actions murió por falta de torch (el módulo de la 003 lo importa arriba); el workflow ahora lo instala (`7534dd2`).
- **Auditoría de Tao entregada y revisada (2026-10-13-001).** PR #28 (`dd9da1c`, 13-oct 00:17) y Doc en el Space. Leyó main en `51e183c`: no vio la 015 completa, la 018 ni la 019.
  - Siguen abiertos en el texto de la v2 (`f19a9c7`): F01 (el nulo de neurópilo sí preserva el in-degree global; medido en el conectoma entero, rama `titan/revision-auditoria-tao-2026-10-13`), F05 (Z_CP +14,8σ sin Tabla 8 reproducible), F06 (con N = 5 no hay p empírica bajo 1/6), F07 (138.142 y 138.140 son dos corridas del control uniforme; citar la de las tablas).
  - Robótica: `adc_to_q15` y `q15_to_pwm` desbordan int32 con `uint16_t` completos; `test_swarm.c` no puede dar rojo.
  - No se le comentó el PR ni se le escribió: espera el visto bueno de Abraham.
- **Síntesis en criollo (2026-10-13-003):** la mosca da el plano (qué tipo de sensor va a qué comando) y, con cableado real suficiente, su simulación lo alcanza; no es un cerebro mejor que su plano ni que la ingeniería.
- **Espera decisión de Abraham:** sellar el factorial 2 (la regla con los mismos sensores, varias semillas de τ y de prueba, margen de equivalencia, R2 en Kaggle); aplicar F01, F06 y F07 a la v2 y decidir F05 (Tabla 8); merge del PR #27 y token de Zenodo; responderle a Tao en su PR.

## Tarde y noche del 12-oct (010 a 018)"""

R = [
    ("**Última actualización:** 2026-10-13, 00:50 (America/Buenos_Aires), con la respuesta 2026-10-12-018. "
     "**La sección «Tarde y noche del 12-oct (010 a 018)» manda sobre lo que choque en el resto del archivo**",
     "**Última actualización:** 2026-10-13, 08:30 (America/Buenos_Aires), con la respuesta 2026-10-13-003. "
     "**La sección «Madrugada y mañana del 13-oct» manda sobre lo que choque en el resto del archivo; "
     "después, la de «Tarde y noche del 12-oct (010 a 018)»**"),
    ("## Tarde y noche del 12-oct (010 a 018) · manda sobre el resto", NUEVA),
    ("- **Espera decisión de Abraham:** sellar el factorial de la 018",
     "- **Esperaba decisión de Abraham (resuelto en la 019 y la 2026-10-13-002):** sellar el factorial de la 018"),
    ("- **Estado (medido en la 2026-10-12-009, 11:56): parado, esperando el «confirmo» de Abraham.**",
     "- **Entregada (2026-10-13-001):** PR #28 (`dd9da1c`, 13-oct 00:17) y Doc en el Space; la revisión contra el estado vivo "
     "está en la 2026-10-13-001. Lo que sigue en este bloque es el estado del 12 a las 11:56 y quedó superado.\n"
     "- **Estado (medido en la 2026-10-12-009, 11:56): parado, esperando el «confirmo» de Abraham.**"),
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
