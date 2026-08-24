# 026 · Explicación en criollo de las entregas 022 a 025

**Fecha:** 2026-08-24 ~10:45 (America/Buenos_Aires)

## 1. Pedido

"EN CRIOLLO QUE HICISTE EN ESTAS ULTIMAS 4 OUTPUT, EXPLICA DETALLADAMENTE".

O sea: sin jerga, detallado, las 4 entregas de la auditoría arquitectónica.

## 2. Herramientas declaradas (C-03)

`create_document` (un Doc nuevo en el workspace, visibilidad pública) y GitHub para este commit. **Ninguna corrida nueva, cero CPU, cero cuota de Kaggle.** Ninguna medición nueva: esto es exposición de lo ya medido en 022-025.

## 3. Qué se entregó

Doc: **EN CRIOLLO · Qué hice en las últimas 4 entregas: la auditoría BICAMERALITY ↔ tu DualBrain, de punta a punta (y los 5 errores míos que aparecieron en el camino)**

URL: https://app.clickup.com/90171457413/docs/2kza6fw5-4357

Ocho secciones: de dónde venía la pregunta · las 4 entregas una por una en orden · la tabla única de veredictos · los 5 errores propios sin maquillaje · lo NO medido · el orden de trabajo con criterio · trazabilidad con md5 · y la contabilidad de máquina en un toggle.

**Por qué va a Doc y no al chat:** el pedido es explicitamente "detalladamente", o sea &gt;20 líneas. Una explicación larga en el chat es una explicación que el entorno puede descartar, y ya pasó varias veces en este proyecto (el usuario reenvió el mismo mensaje tres veces por eso). Regla del Bloque 0.

## 4. Decisiones de exposición, y por qué

1. **Los errores propios tienen sección propia y numerada (5 + 1 operativo)**, no repartidos como notas al pie. Si el registro se diluye, no sirve.
2. **La distinción "empate" ≠ "son iguales"** se explica con banner en la primera entrega y se repite en la cuarta, porque es la que más fácil se pierde al leer rápido y la que cambia el veredicto del bias.
3. **El estado del bias se presenta como SUBPOTENCIADO, no como nulo**, con los tres números que lo sostienen (3/4 en punto, p=0,0571, d=1,10, potencia ~45%).
4. **La regla de la tabla 2×2 se marca como HIPÓTESIS** en el mismo párrafo donde se presenta, con las 2 casillas vacías señaladas y el experimento que la falsaría.
5. **La contabilidad de CPU va en toggle**: 284 min (gate) + 98 min (bias) + ~30 min desperdiciados por mi job duplicado, cero cuota de Kaggle. Cada llamada cae en la máquina de Abraham y él la loguea, así que el gasto es auditable sin preguntármelo.

## 5. Evidencia

Ninguna nueva. Todos los números del Doc son citas de:

- `respuestas/2026-08-24-022-ab-gate-Gated-cerrado-MultiCue-5de6.md`
- `respuestas/2026-08-24-023-ab-gate-CERRADO-veredicto-final-4-tareas.md`
- `respuestas/2026-08-24-024-LiquidRealCell-es-LiquidCell-mas-un-bias.md`
- `respuestas/2026-08-24-025-ab-bias-de-flujo-CERRADO.md`
- `CONTEXTO-motor.md` §0

La salida cruda verbatim de los instrumentos vive en esos cuatro archivos, no acá. **El Doc no introduce ni un número que no esté respaldado ahí.**

## 6. NO MEDIDO, declarado

- **No verifiqué los números del Doc contra los JSON de nuevo.** Son transcripciones de las respuestas 022-025, que a su vez transcriben logs verbatim. Si hay un error de copia en el Doc, está acá y no en la medición.
- **El cálculo de potencia (~45% para d=1,1 con n=6, α=0,05) es una estimación de tabla, no una simulación.** El orden de magnitud es el que importa para el argumento (está lejos del 80%), pero el número exacto no lo computé.
- Todo el resto de lo no medido sigue igual y está en §7 del Doc y §6 de `CONTEXTO-motor.md`.

```
--- METODO TITAN ---
Accion delicada: NO. Un Doc nuevo, un commit. Ninguna corrida, cero CPU,
                 cero cuota ajena, nada sobreescrito salvo este archivo nuevo.
Modo aplicado:   TITAN LIGERO (exposicion de resultados ya medidos y ya
                 auditados con rubrica en 023 y 025; no hay entrega tecnica
                 nueva que puntuar)
Rubrica:         N/A (modo ligero). Las rubricas de lo expuesto: 98/100 en la
                 023 y 98/100 en la 025.
N/A declarados:  N/A (modo ligero)
Review externo:  no aplica
Instrumento:     ninguno nuevo. Cero mediciones nuevas: el Doc cita 022-025.
                 Verificable contra ab_gate_A/B.json y ab_cell_A/B.json, con
                 md5 listados en la seccion de trazabilidad del Doc.
                 NO MEDIDO: seccion 6.
```
