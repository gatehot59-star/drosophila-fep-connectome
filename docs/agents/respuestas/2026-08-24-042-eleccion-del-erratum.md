# 042 · Elección del erratum: base + trasplantes, y por qué **no se sube hoy**

**Fecha:** 2026-08-24 15:35 (America/Buenos_Aires) · **Modo:** TITAN FULL · peritaje editorial

> **📄 Doc de ClickUp de esta respuesta:** *«[TITAN FULL] ELEGÍ, y no son tres: son DOS textos y una descripción...»*. Segundo Doc del chat, después del hueco de cinco turnos que cerró la resp 041.

---

## 1. Pedido

«Leé los erratums 5157 y 6117 y elegí.»

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `load_assets` · doc `5157` **completo** | no | no |
| doc `6117` · leído completo en la resp 038 | no | no |
| texto del container · `docs/agents/evidencia/2026-08-24-ERRATUM-md-verbatim-del-container.md` | no | no |
| `create_document` · el Doc | **sí, ClickUp** | no |
| `create_or_update_file` · este archivo | **sí, al repo** | no |

**Cero container, cero Kaggle, cero runtime de Tachi, nada publicado en Zenodo, ningún contexto sobrescrito.**

---

## 3. Qué se midió

### 3.1 Corrección a mi propio framing: **no son tres erratums**

Vengó diciendo «tres versiones incompatibles» desde la resp 039. Leídos los tres:

| Candidato | Qué es | Ítems |
|---|---|---|
| doc `5157` (21-ago) | **texto de erratum real**, y trae **tres** entregables: sección del PDF, notas del registro de Zenodo, línea del changelog | **E1-E8** |
| `/workspace/repo/docs/ERRATUM.md` | **texto de erratum real**, prosa de publicación, cero placeholders | **5** + «What is not corrected» |
| doc `6117` (24-ago) | **NO es un erratum: es el PLAN MAESTRO.** En su §2.1 *describe* uno de 7 puntos | — |

**Dos textos y una descripción.** Y la descripción no coincide con ninguno: dice 7 puntos, el container tiene 5, y su punto #7 (*retención temporal, 3,05× vs CP con 0/19*) **no existe en el archivo del container**. Lectura probable, **declarada como inferencia**: el `6117` describió de memoria un archivo que afirmaba estar commiteado y no lo estaba.

### 3.2 🚨 EL BLOQUEO: los dos textos publican un claim que el doc `5177` RETIRÓ

**Container, ítem 1, verbatim:** *«Summary as published: 0 enriched, 7 depleted. **Corrected: 4 enriched, 4 depleted.**»*

**`5157`, E2, verbatim:** *«All observed/expected ratios were computed against the incorrect expectation... That conclusion does not survive recomputation... [AQUI VA EL RESULTADO REAL, una vez recalculado.]»*

**Los dos hacen el mismo movimiento: sustituir la densidad mala por la buena y recalcular la Tabla 5.**

**Doc `5177`, 21-ago, 100/100:** *«la expectativa de la Tabla 5 **NO es de densidad** (densidades implicadas 0,016719 y 0,014132; `Exp_m/Exp_g ∈ [6,68 , 8,82]` vs `N_m/N_g = 6,52`). **Se retira el «4 de 9 enriquecidas».**»*

**Subir cualquiera de los dos tal como está pone en un documento con DOI un número que mi propio expediente retiró.** Y eso dispara el criterio de aborto de la S1: *«un erratum con un error es peor que no tener erratum»*.

**Refuerzo:** la Tabla 5 tiene **tres conteos de filas** — **8** en el container, **9** según `5157` E6, **9** en el `5177` — y los Methods describen **10** clases canónicas. Ninguno de los dos textos lo declara.

### 3.3 Segunda contradicción: la causa del bug de densidad

| Fuente | Afirma |
|---|---|
| container ítem 1 | «sinapsis vs conexiones» *«tested and **rejected**»* (54.492.922 no reconcilia). La causa *«not established»* |
| `5157` E3 | es una **ambigüedad terminológica real**: «synapses» en el abstract y «connections» en §2.1 para el mismo 15.091.983; Lin da 12,6 sinapsis/conexión |
| doc `5117` | **la causa ES esa**, y así quedó en `CONTEXTO-drosophila-fep.md` §2 |

**Reconciliación propuesta:** el container refuta que **el número** se explique por sinapsis; el `5157` afirma que **el texto** usa los dos términos para lo mismo. **Las dos pueden ser ciertas a la vez**, y el erratum tiene que decirlas juntas. Hoy ninguno lo hace.

### 3.4 La elección: **container como base**, con 4 trasplantes y 2 correcciones

| Criterio | container | `5157` |
|---|---|---|
| Placeholders | **CERO** | **TRES corchetes** |
| Mediciones | las de hoy (40 nulls CP, 283×, olfactory, trayectoria del 1.559×, pin con md5, licencia, swap 98,5%) | las del 21-ago |
| Forma | prosa de publicación con tabla armada | texto formal, también publicable |

**Criterio declarado (O-01): cuál está más cerca de poder subirse, con 6 días de reloj.** El container es un documento terminado que necesita correcciones; el `5157` es un documento correcto que necesita **tres corridas**.

**Trasplantes obligatorios del `5157`:**

1. **E4 · la brecha 26,6% vs 13,8% de Lin.** 🔥 **El container no la menciona.** Lin et al. 2024 (*Nature* 634:124-138) publica **13,8%** para el mismo conectoma. Un revisor con Lin pregunta esto primero. **Es el agujero más grande del container.**
2. **E6 · tres inconsistencias aritméticas.** Tabla 4 suma **90.101** donde 85.821+4.281 = **90.102**. Tabla 5: 9 filas vs 10 clases. Depletadas: **6 en la tabla, 7 en el texto, 7/10 en el abstract**. Verificables con el PDF y una calculadora.
3. **E8 · «four parameter-free models» → TRES.** El LIF-hard da RDI indefinido, y ya está en los Methods de la v1.
4. **Los DOI reales:** concept **`10.5281/zenodo.19136947`**, v1 **`10.5281/zenodo.19136948`**. ⚠️ **Cierra el pendiente #3 de `CONTEXTO-drosophila-fep.md`** («no sé de dónde sale el 19136948»): sale del `5157`, verificado contra la API de Zenodo el 21-ago.

**Correcciones sobre el container:**

- **a) El 338,8× sale.** Es el ratio contra densidad uniforme, el null más débil. El defendible es **20,59× vs 40 nulls CP, 0/40** (doc `6057`). **Y el `5157` tenía la solución mejor: reportar la reciprocidad como RANK contra el ensemble**, que *«no depende de ninguna estimación de densidad»* → vuelve el resultado **inmune a esta clase de error**. Su bracket ya no está vacío: **1º de 41**.
- **b) El «4 enriquecidas» sale o se reencuadra** hasta re-auditar la Tabla 5.

**Se descarta el E7 del `5157`** (τm «within» el rango): el container lo trata mejor en «What is not corrected», con la constante correcta **7,89 ms**, error **6,47%**, y que ninguna conclusión depende de la diferencia.

### 3.5 Los tres corchetes, al día de hoy

| Bracket | Estado |
|---|---|
| Ratios reales de la Tabla 5 | 🚨 **no se cierra sustituyendo la densidad** (§3.2). Hace falta re-auditar la tabla contra su propia expectativa: **es una lectura del PDF, no una corrida** |
| Rank de reciprocidad | ✅ **CERRADO.** 1º de 41 · 0/40 vs CP · 20,59× vs CP · 47,27× vs MS |
| ¿El umbral de 5 sinapsis explica 26,6 vs 13,8? | ❌ **ABIERTO.** Corrida corta sobre el parquet ya verificado. **Si no lo explica, el erratum lo dice**, no le invente una causa |

---

## 4. Evidencia cruda verbatim

```
$ load_assets doc:2kza6fw5-5157
  "Erratum v1.0 -> v2.0 - texto formal listo para pegar en Zenodo, con los
   tres numeros que solo podes completar vos"   · fecha 2026-08-21
  E1 densidad · E2 metricas afectadas · E3 sinapsis vs conexiones ·
  E4 brecha con Lin · E5 DOI placeholder · E6 inconsistencias de conteo ·
  E7 caracterizaciones exageradas · E8 conteo de modelos
  Brackets literales: 3
    "[AQUI VA EL RESULTADO REAL, una vez recalculado.]"
    "[AQUI VA EL RANK REAL contra los 100 controles.]"
    "[CONFIRMAR que el umbral explica la brecha antes de afirmarlo...]"
  DOIs: concept 10.5281/zenodo.19136947 · v1 10.5281/zenodo.19136948

$ grep -n '^## ' /workspace/repo/docs/ERRATUM.md     (md5 2ae28606c28c...)
  11: ## 1. Graph density, and the motor-access table that depends on it
  43: ## 2. The claim that the topology concentrates rather than proliferates
  63: ## 3. The amplification ratio reported as 1,559x
  86: ## 4. Data availability URL and licence
  100: ## 5. Pinned data, and two smaller items
  119: ## What is not corrected
  -> CINCO. El 6117 dice SIETE, y su punto 7 no esta aca.

El conflicto, los dos verbatim:
  container: "Summary as published: 0 enriched, 7 depleted.
              Corrected: 4 enriched, 4 depleted."
  doc 5177:  "La expectativa de la Tabla 5 NO es de densidad ... Se retira el
              '4 de 9 enriquecidas'."

Conteos de filas de la Tabla 5: container 8 · 5157 E6 "nine" · 5177 "4 de 9"
  · Methods: 10 clases canonicas.  CUATRO numeros para una tabla.
```

**Recomputable y contradecible (W-01):** se abre el `5157` y el archivo rescatado en `docs/agents/evidencia/` y se comparan ítem por ítem. **Si el «4 enriquecidas» del container no es el mismo claim que el `5177` retiró, el bloqueo del §3.2 es falso.**

---

## 5. Archivos generados

1. El Doc de ClickUp con el peritaje completo.
2. `docs/agents/respuestas/2026-08-24-042-eleccion-del-erratum.md` (este archivo).

**Ningún contexto se toca en este commit**, a propósito: la elección es una recomendación, y el estado vivo cambia cuando Abraham la acepta o la rechaza.

---

## 6. El plan de subida, con el bloqueante de cada paso

| # | Paso | Quién |
|---|---|---|
| 1 | **Re-auditar la Tabla 5** contra su expectativa real (lectura del PDF) | yo |
| 2 | Recalcular reciprocidad **con y sin umbral de 5 sinapsis** | yo, corrida corta |
| 3 | Fundir: container + 4 trasplantes + 2 correcciones | yo |
| 4 | **Commitear `docs/ERRATUM.md` a git** por primera vez, con los 10 archivos del release | yo |
| 5 | Arreglar el `README.md` público (`temporal RDI` marcado frágil) | vos decidís, yo aplico |
| 6 | **Subir la v2 a Zenodo** | 🔴 **SOLO VOS** |

**Advertencia del `5157` que sigue vigente:** *«no publiques la v2 solo con el erratum. Un erratum que corrige un número y deja los resultados iguales invita a la pregunta obvia: si la densidad cambia 46×, por qué no cambió ningún resultado?»*

**Dato de Zenodo:** al subir la v2, el concept DOI resuelve a la nueva y el DOI de la v1 **sigue funcionando con el archivo viejo**. **No pedir el retiro de la v1:** un erratum vale porque la versión anterior sigue visible.

---

## 7. NO MEDIDO, declarado

1. **No abrí el PDF publicado en este turno.** El bloqueo del §3.2 se apoya en la medición del `5177` del 21-ago, no en una re-lectura de hoy.
2. **No recalculé nada.** Cero corridas.
3. **No puedo reconciliar el conteo del `6117`** sin saber qué archivo describía. La explicación de §3.1 es **inferencia declarada**.
4. **No leí `repo/docs/METHODS.md`, `repo/README.md` ni `repo/LICENSE`**, y el ítem 4 del container **cambia la licencia**.
5. **No re-verifiqué los DOI contra Zenodo hoy.** Vienen del `5157` (API, 21-ago). **Antes de pegarlos en un documento público se re-verifican.**
6. **No verifiqué la cita de Lin** (*Nature* 634:124-138, 1,61×10⁻⁴, 12,6 sinapsis/conexión, 0,138). **Un número ajeno que va a un erratum se verifica contra la fuente.**
7. **Los cuatro conteos de la Tabla 5 (8, 9, 9, 10) sin reconciliar.**

---

## 8. La regla que sale

**Antes de elegir entre N candidatos, verificar que los N sean del mismo tipo.** Uno de los tres no era un erratum: era un plan que describía uno. Comparé dos textos contra una descripción y de ahí salió el framing de «tres versiones incompatibles» que arrastré tres turnos. **Es E-01 aplicado a un conjunto en vez de a un archivo: verificar el sujeto exacto Y su categoría.**

```
--- METODO TITAN ---
Accion delicada: NO. Lectura de Docs y dos escrituras de documentacion. Nada
                 publicado en Zenodo, ningun contexto sobrescrito, cero cuota.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100
N/A declarados:  45 pts (Ejecutabilidad, Seguridad, Testing, DevOps)
Review externo:  el falsador fue el doc 5177, que es un documento MIO del
                 21-ago: retiro el "4 de 9 enriquecidas" y ninguno de los dos
                 erratums lo incorporo. El corpus ya contenia la refutacion del
                 entregable, y hacian falta los tres textos en la misma pantalla
                 para verla. Es el mismo metodo con el que Abraham me falsa:
                 poner dos cosas mias juntas.
Instrumento:     load_assets sobre el doc 5157 completo (3 brackets literales
                 localizados), el archivo del container rescatado por la resp
                 039 (md5 2ae28606c28c140dc76cd3b8e6b3ab85, 125 lineas), y el
                 doc 6117 leido completo en la resp 038. Evidencia cruda
                 verbatim en la seccion 4.
                 NO MEDIDO: la seccion 7, siete items, incluido que el bloqueo
                 se apoya en una medicion del 21-ago y no en una lectura de hoy.
```
