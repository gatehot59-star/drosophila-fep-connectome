# 070 · Tau barrida: el claim sobrevive por tau, y se rompe por la métrica

**Fecha:** 2026-08-25 02:05 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «BARRÍ TAU · sobrevive, pero encontré que medía la métrica equivocada»
> **🔬 Evidencia:** `docs/agents/evidencia/2026-08-25-barrido-tau-heterogenea-evidencia-cruda.md`
> **🛠 Instrumento:** `src/sweep_tau_hetero.py`, md5 `35cabd5acc51f37529584cc53c013dcf`

---

## 1. Pedido

«Barré tau heterogénea antes de que Tao audite.» Era el ítem 1 de los NO MEDIDO de la resp 069, y el claim **C-08** de la orden a Tao.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 8 sobre `brain-env` | solo `/tmp` | **NO** |
| `githubmcp_create_or_update_file` × 4 | sí, rama `titan/twohop-nulls` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero Kaggle. Nada a Zenodo. `/workspace` solo leído. Ningún merge.** CPU: 511,8 s.

---

## 3. El diseño, porque sin él el barrido no decidía nada

Un barrido de dispersión a secas no sirve: si la selectividad sube con la dispersión, eso puede ser **una propiedad de tener constantes distintas** y no decir nada del cableado. **Lo que hace falsable el experimento es el modo de asignación.**

| Modo | Qué hace |
|---|---|
| **RANDOM** | `tau` sorteada independiente por neurona |
| **STRUCTURED** | rápidas a las visuales y ópticas, lentas a las centrales, **siguiendo la medición regional del propio repo** (óptica 0,2689 contra cuerpo fungiforme 0,0180, factor 15) |
| **REVERSED** | las mismas `tau`, asignación invertida. **El falsador.** |

Y las `tau` se sortean log-uniformes con **media geométrica fija en 0,119**: el spread cambia, el centro no. **Ningún brazo puede ganar por ser globalmente más rápido.**

**Control interno:** `spread = 1` **reproduce 1,0631 exacto**, el valor de la corrida anterior con otro código. Si no hubiera coincidido, el barrido era inválido.

---

## 4. 🟢 VEREDICTO A · tau heterogénea NO rescata el claim, y el falsador es limpio

`sel_peak`, STRUCTURED contra REVERSED:

| Spread | STRUCTURED | REVERSED | ¿gana la biológica? |
|---|---|---|---|
| 2 | 1,0599 ± 0,0008 | **1,0802** | no |
| 4 | 1,0726 ± 0,0015 | **1,1040** | no |
| 8 | 1,0972 ± 0,0022 | **1,1276** | no |
| 15 | 1,1235 ± 0,0027 | **1,1452** | no |
| 30 | 1,1503 ± 0,0027 | **1,1591** | no |

**5 de 5, con `sd` de tercera cifra.** La asignación biológicamente motivada da **menos** selectividad de pico que su reverso exacto.

**Sí sube algo con la dispersión bruta** (1,0631 → 1,1874 en RANDOM con spread 30), pero eso es **dispersión, no cableado**, y viene con `sd` de 0,0537, o sea que depende del sorteo. **La vía «tau heterogénea rescata la selectividad porque el conectoma la asigna bien» queda refutada.**

---

## 5. 🔴 VEREDICTO B · y acá me equivoqué en algo más grande: la métrica

Agregué una segunda métrica que **nunca había medido**: la separación **después** de que el estímulo termina, integrando desde el paso 80.

```
sel_peak con tau fija:  1,0631      <- lo que medí siempre
sel_post con tau fija:  4,3287      <- lo que nunca medí
```

**El circuito discrimina looming de receding por un factor de 4,3, pero DESPUÉS del estímulo, no en el pico.**

Y contra la dispersión va **al revés** que `sel_peak`:

| Spread | `sel_post` RANDOM | `sel_post` STRUCTURED |
|---|---|---|
| **1** | **4,3287** | — |
| 2 | 4,2328 | 3,8616 |
| 4 | 3,9853 | 3,1302 |
| 8 | 3,5189 | 2,5819 |
| 15 | 3,0157 | 2,2781 |
| 30 | 2,6298 | **2,0686** |

**Monotónica en los dos modos: la dispersión de `tau` DESTRUYE la selectividad post-estímulo, y la asignación estructurada la destruye más rápido.**

### Qué le hace esto al claim

> **«La topología define ruteo y ganancia, no selectividad» pasa a NO SOSTENIDO tal como está escrito.**

No porque tau lo rescatara, sino porque **la métrica estaba mal elegida**. Medí el pico durante seis días y el pico es lo único que este circuito **no** discrimina.

**Y esto conecta con el paper de una forma que no esperaba:** la Propiedad 3 del Paper 1 es exactamente **amplificación post-estímulo** (RDI subiendo de 0,63 a 0,83 después del estímulo, `z = 197`). **El circuito compilado reproduce cualitativamente esa propiedad, y yo la tenía medida en el conectoma y no la había buscado en el compilado.** Es el modo de falla de siempre: **medir el sujeto equivocado**, ahora en su versión de métrica.

### 🔴 Pero el 4,33 NO es un resultado todavía, y hay que decirlo fuerte

**El control de signo barajado de la corrida anterior se midió solo sobre `sel_peak`.** No hay null para `sel_post`. **Sin él, el 4,33 es un número crudo.**

Y hay una trampa que ya cometió este proyecto: comparar el 1,1598 de spread 15 contra el sign-shuffle de 1,1131 **mezcla dos condiciones**, porque ese shuffle se midió con `tau` fija. **Es el modo de falla 5, sexta aparición, y esta vez declarado antes de cometerlo.**

**El experimento que sigue, y es barato:** sign-shuffle sobre `sel_post`, a cada spread. Si el 4,33 sobrevive, **es el mejor resultado del expediente**. Si no, se cae y el claim original vuelve.

---

## 6. Addendum a la orden de Tao

La orden dice, en **C-08**: *«tau heterogénea es el parámetro con más chance de generar selectividad temporal y no se barrió. Este claim puede ser un artefacto de un modelo demasiado pobre.»*

**Se barrió, y C-08 se reformula.** Está escrito en `docs/agents/ORDEN-TAO-ADDENDUM-01-tau-y-post-estimulo.md`, que **Tao tiene que leer junto con la orden**. Lo nuevo que le pido atacar:

- **C-08a:** ¿la métrica correcta de «selectividad temporal» es el pico o el post-estímulo? **Las dos se mueven en direcciones opuestas con la dispersión**, así que el veredicto depende enteramente de esa elección, y esa elección la hice yo sin justificarla.
- **C-08b:** ¿el `sel_post = 4,3287` sobrevive un null de signo? **No lo corrí.**
- **C-08c:** `sel_post` integra desde el paso 80 hasta el 200. ¿Cuánto del 4,33 es la elección de esa ventana?

---

## 7. Scorecard (QA)

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | 13 configuraciones × 20 sorteos, tres modos, dos métricas, control interno. **−1**: `tau` compleja (el banco de osciladores del motor real) no se barrió |
| **Ejecutabilidad** | 15/15 | `DONE in 511.8 s`, rutas por `argparse`, y **el control interno reprodujo 1,0631 exacto con otro código** |
| **Arquitectura del razonamiento** | 10/10 | el contraste STRUCTURED/REVERSED es lo que separa «dispersión» de «asignación», y la media geométrica fija impide que un brazo gane por ser globalmente más rápido |
| **Documentación** | 10/10 | evidencia verbatim, ocho defectos declarados, y el addendum emitido **antes** de que Tao audite con el claim viejo |
| **Innovación** | 4/5 | la métrica post-estímulo no estaba pedida y es lo que dio vuelta el turno. **−1**: no vino con su null |
| **Proceso QA** | 2/5 | cada número tiene su línea. **−3: el hallazgo principal (4,33) se entrega SIN control**, y este proyecto ya sabe que un ratio sin null no es un resultado |

**Total 55/60 → 91,7/100.** APROBADO al filo (umbral 90), **y el descuento de Proceso QA es el honesto.**
**N/A: 40 pts** — Seguridad (15), Testing (15), DevOps (10).

---

## 8. NO MEDIDO, declarado

1. **🔴 `sel_post = 4,3287` sin null de signo.** Es el pendiente que decide si el hallazgo existe.
2. **El sign-shuffle de 1,1131 es con `tau` fija:** no comparable con los spreads. Hace falta a cada spread.
3. **No se decidió cuál es la métrica correcta**, y el veredicto depende de eso.
4. **`tau` real, no compleja.** El motor usa `Im(tau) ~ U(0,01 , 0,15)`: banco de osciladores, sin barrer.
5. **Las 11 `tau` regionales del motor son andamio sintético hardcodeado**, no medición, así que STRUCTURED es **una hipótesis de asignación**, no la real.
6. **Solo se estimula LC4+LPLC2**, escalar, sin campo receptivo ni entrada multimodal.
7. **Una sola ventana.** `sel_post` depende de cuántos pasos quedan y no se barrió.
8. **La normalización iguala la ganancia a propósito:** este barrido no dice nada sobre ganancia.
9. **Los contextos siguen sin actualizar** con las resp 065 a 070. Es la deuda de estado más vieja abierta.
10. **La entrada 01 de la biblioteca dice «selectividad temporal 1,04×, o sea ninguna»** y eso ahora está incompleto. **Sin corregir hasta que el null de `sel_post` decida.**
