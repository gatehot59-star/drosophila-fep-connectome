# 076 · EN CRIOLLO · dónde andamos al 2026-08-25 09:00

**Fecha:** 2026-08-25 09:00 (America/Buenos_Aires) · **Modo:** TITAN LIGERO (explicación, cero mediciones nuevas)

> **📄 Doc de ClickUp:** «EN CRIOLLO · dónde andamos al 25-ago 09:00 · tenés un activo fuerte y un release rechazado»
> **🛠 Instrumento:** ninguno (declarado). Todo número sale de las resp 063-075 y del contexto unificado en el commit anterior, todos commiteados.

---

## 1. Pedido

«EN DONDE ANDAMOS EN CRIOLLO». Estado del proyecto explicado sin jerga. **No pidió una medición.**

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `create_document` × 1 (ClickUp) | sí | no |
| `githubmcp_create_or_update_file` × 1 → **rama `titan/twohop-nulls`** | sí | no |

**Cero lecturas nuevas de repo, cero gateway, cero Kaggle, cero runtime de Tachi. Nada borrado. Ningún merge. `main` intacta.** El estado entero venía cargado del turno anterior (resp 075), donde se leyeron el handoff 074, la resp 063 completa, los dos listados y el log de commits.

## 3. La foto, en cinco frases

1. Hay **un resultado fuerte de verdad**, y no es el que se venía contando hace dos días.
2. **Ocho claims propios murieron** entre el 24 y el 25-ago, y los ocho por la misma razón.
3. Un **auditor externo puntuó el repo 62/100 y lo rechazó como release**, con razón.
4. Lo que se cayó son **claims de interpretación. Las mediciones no fallaron ni una vez.**
5. Lo único con reloj es **el erratum: 30-ago, y depende de Abraham.**

## 4. El activo, explicado

El circuito **no** distingue estímulos por la altura de su respuesta. Los distingue por **cómo se apaga después** de que el estímulo terminó.

`sel_peak` se midió seis días, y el pico es **lo único que este circuito no discrimina**. Con la métrica correcta: `sel_post` = **4,3287** contra **1,1896 ± 0,0173** del null de topología (**z = +181,4**, 0/40), y contra **1,7983 ± 0,401** del null de signo que **preserva Dale** (**z = +6,31**, 0/40). Se repite en **7 de 7** configuraciones. En la misma corrida, `sel_peak` queda **por debajo** de su null en 6 de 7.

**Por qué vale, en criollo:**

- Es **el mismo fenómeno** que el RDI post-estímulo del Paper 1 (z = 197), medido por otro camino. **Dos instrumentos independientes.**
- Es **exactamente lo que BANC declara no cubrir**: ellos toman *steady-state* y magnitud *unsigned*. El campo llegó al método y se detuvo antes del aporte.
- El mecanismo está **medido**: actividad post-estímulo absoluta **2,77 contra 16,09** del null → 5,8× menos actividad total y 3,6× más selectividad. **No resuena más: resuena menos y diferencial.**

**Lo otro en pie:** `LC6→GF = 0` contra el null anatómico (predice 17,2 ± 3,1, hay 0, z = −5,6) → **ese cero sí es prohibición de cableado, no geometría** · 0/40 en 12 de 12 pares del centro de aprendizaje · Dale exacta (0 mixtas de 138.005) · 1.336 B de `.text` en ESP32.

## 5. Lo que se cayó, y la forma común

Los cuatro que más pesan de los ocho:

- El **spread de 323×** de acceso motor a 2 saltos **colapsó a 2,4×** contra el null anatómico, y **tres de cuatro signos se invirtieron**.
- El argumento que lo sostenía (*«las cuatro clases son igual de locales»*) **era falso, y se midió al turno siguiente**: 104 de 110 motoras viven en GNG/PRW, igual que gustativa y mecanosensorial. **Dos clases locales al motor, dos locales a lo sensorial: eso era el efecto entero.**
- La **tabla de ruteo ya está publicada**, y desde el mismo snapshot propio.
- El **«0 inhibitorias» del GF** describía un recorte del 20%. El real es **49,8% inhibitorio y 67,6% central**.

> **La forma común: medir bien y después afirmar la CAUSA o la NOVEDAD sin medir eso. Las mediciones no fallaron nunca.**

**Y el premio de consolación es más grande que lo que murió:** la gustativa **comparte neuropilo con las motoras** y aun así conecta con **10 de 110** cuando su co-localización predice **101,6 ± 1,2** (**z = −78,9**, 40/40). El blindaje interesante no está donde las vías están lejos: está donde están **al lado y aun así no se tocan.** Sobrevive al control más fuerte disponible, y ninguna versión anterior del análisis lo podía ver.

## 6. La auditoría, y por qué conviene

**62/100, RECHAZADO como release. 13 de 13 hallazgos aceptados, 0 rechazados.** Tres verificados independientemente y confirmados; A-06 era **peor** que su texto (862 de 864 neuronas quedaban mixtas).

Verbatim: *«El problema no es que el proyecto no tenga resultados; es que la rama pública, el ejecutor y el testigo no están alineados.»*

**Traducido:** los resultados aguantan; el envase no. Los guards imprimen rojo y salen con 0, no hay entorno reproducible, y un clon fresco **no corre** por rutas absolutas.

**Lo que más vale, y no es un hallazgo:** las ocho autorrefutaciones son **todas científicas**; los cinco bloqueantes son **todos de infraestructura**. **Un instrumento propio no encuentra la clase de error que su dueño no busca.** Eso es W-01 con un número.

**El que más puede doler y sigue sin verificar: A-10.** Si el mapeo `id2i` del Script R está mal, los **30/30 valores reproducidos reproducen un bug.**

## 7. El reloj

| Qué | Cuándo | De quién depende |
|---|---|---|
| **Erratum a Zenodo** | **antes del 30-ago · 5 días** | **de Abraham.** Texto listo, 9 ítems, sin placeholders |
| Papers a ARC Prize | 8-nov | 0 de 2 |

Ninguno de los 13 hallazgos toca los nueve ítems del erratum, y Tao lo confirma explícitamente. **W-01: leerlo una vez antes de subir.**

## 8. Lo que espera decisión, y la recomendación sin hedge

1. **Subir el erratum.** Único ítem con fecha, y no lo puedo hacer yo.
2. **Decidir el cronograma.** La infraestructura son días y no estaba en los cinco entregables del plan. **O se corre el plan, o se mata un entregable. No lo decido yo: priorizar es donde más daño hago.**
3. **¿Abro los 13 issues?** Son 5+ escrituras, por eso se pregunta. Sin issues, los hallazgos son **deuda sin dueño**.

**Recomendación emitida:** el orden de Tao gana al mío. **Primero lo que vuelve confiable al testigo, después lo que amplía el claim.** Y dentro de eso, **A-10 primero**: si ese mapeo está mal, media tabla de validados se cae, y es más barato saberlo hoy que en la revisión externa de la S9.

## 9. Archivos generados en este turno

| Archivo | Qué |
|---|---|
| `docs/agents/respuestas/2026-08-25-076-en-criollo-donde-andamos.md` | este |
| Doc de ClickUp | «EN CRIOLLO · dónde andamos al 25-ago 09:00 · tenés un activo fuerte y un release rechazado» |

## 10. NO MEDIDO, declarado

1. **Cero mediciones nuevas.** Todo número traza a las resp 063-075 y al contexto unificado, ninguno a una corrida de este turno.
2. **`CONTEXTO-motor.md` sigue sin abrirse.** A-12 cerrado a la mitad, y ese archivo **no tiene veredicto de vigencia** (modo de falla 4). **La línea del motor queda fuera de esta foto a propósito**, no por olvido.
3. **`CONTEXTO-ENTORNO.md` no se re-midió** en este turno.
4. **A-10 sin verificar**, y es la prioridad técnica máxima.
5. **Los 13 issues no se abrieron**: esperan el OK.
6. **Ningún guard corrió.** Nada de lo escrito acá se declara verde por medición nueva.
7. **El review automático no emitió hallazgos** sobre este archivo. **K-02: deuda declarada, no aprobación.**
