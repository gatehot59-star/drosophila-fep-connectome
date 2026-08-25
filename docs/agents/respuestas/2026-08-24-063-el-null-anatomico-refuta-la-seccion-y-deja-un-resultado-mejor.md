# 063 · El null anatómico refuta la sección, y deja un resultado mejor

**Fecha:** 2026-08-25 00:40 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «TITAN FULL · el null anatómico refutó mi propia sección»
> **🔬 Evidencia cruda:** `docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md`
> **🛠 Instrumento:** `src/twohop_nulls.py`, md5 `a3d52df61a2bc2ccbb332a01c1353dba`

---

## 1. Pedido

«TITAN FULL, auditá todo lo trabajado este par de horas, generá las tres figuras de la sección, corré el barrido con umbral de 5 sinapsis y buscá la asignación a neuropilos para el null anatómico.»

Cuatro tareas. **Las cuatro se ejecutaron, y la cuarta refuta el producto de la sesión anterior.**

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `search_web` × 2 (buscar la asignación a neuropilos) | no | no |
| `gateway build.run` × ~20 sobre `brain-env` | solo `/tmp` | **NO** |
| `githubmcp_create_branch` + `create_or_update_file` | sí, **rama `titan/twohop-nulls`, nunca `main`** | no |
| `create_document` | sí, ClickUp | no |

**Cero Kaggle. Nada publicado en Zenodo. `/workspace` solo leído. Ningún archivo borrado. Ningún merge.**

---

## 3. 🔍 TAREA 4 PRIMERO, porque cambia todo lo demás: la asignación a neuropilos EXISTE

El ítem 13 de la §5 del contexto decía que el null anatómico **no era testeable** porque `annotations.tsv` tiene 31 columnas y ninguna es neuropilo.

**Eso era un límite de UN archivo, no del entorno.** Está en Zenodo, público, sin login, en el mismo record del release 783:

```
Zenodo 10676866, v783.0
  per_neuron_neuropil_count_pre_783.feather    16.853.770 B
  per_neuron_neuropil_count_post_783.feather  233.843.050 B
  columnas: pre_pt_root_id | neuropil | count
```

Bajado y usado: **79 etiquetas de neuropilo**, y solo **283 neuronas sin neuropilo de salida** y **495 sin neuropilo de entrada** sobre 138.639. La cobertura es prácticamente total.

**Esto es el modo de falla 3 del Bloque 8 de TITAN, cometido por mí durante días:** dar por cerrado un problema porque una herramienta no lo resuelve. El dato estaba a una llamada.

---

## 4. 🔴 LA REFUTACIÓN · el null anatómico borra el efecto y da vuelta tres signos

**El ensemble:** permuta destinos **solo dentro de grupos de aristas que comparten el par (neuropilo de origen, neuropilo de destino)**. Preserva el número de conexiones entre cada par ordenado de neuropilos, además del grado de salida. **Es la familia del NPC model de Lin et al. (2024).** 40 realizaciones, semillas `1000 + 7i`.

### Umbral 1, `P2` (caminos de 2 saltos hasta motoras)

| Clase | Null de GRADO | Null de NEUROPILO | ¿Cambia el signo? |
|---|---|---|---|
| **olfactory** | **0,0228×** (z −51,8, 40/40) | **0,368×** (z −4,44, 40/40) | no, pero el efecto se divide por **16** |
| **visual** | **0,0606×** (z −54,0, 40/40) | **1,531×** (z **+4,10**, **0/40**) | 🔴 **SÍ: pasa a ENRIQUECIDA** |
| **mechanosensory** | **7,365×** (z +342, 0/40) | **0,803×** (z **−20,6**, 40/40) | 🔴 **SÍ: pasa a DEPLETADA** |
| **gustatory** | **6,545×** (z +249, 0/40) | **0,632×** (z **−37,2**, 40/40) | 🔴 **SÍ: pasa a DEPLETADA** |
| **CTRL arbitrario** | **0,652×** | **1,010×** | 🔴 **el piso desaparece** |

### Umbral 5, y el patrón es el mismo

| Clase | GRADO | NEUROPILO |
|---|---|---|
| olfactory | 0,0015× (z −20,3) | **0,121×** (z −2,05) |
| visual | 0,0465× (z −16,7) | **4,872×** (z **+10,9**, 0/40) |
| mechanosensory | 5,812× (z +88,2) | **0,974×** (z −1,59, **38/40 → no significativo**) |
| gustatory | 2,619× (z +20,8) | **0,376×** (z −31,3) |
| CTRL arbitrario | 0,630× | 1,147× |

**Con los dos umbrales, el orden entre clases se invierte.** Y el **spread de 323×** que era el número central de la sección colapsa a **2,4×** (1,531 / 0,632).

### Y el piso de 0,652× era anatomía, no una propiedad del cerebro

El control arbitrario daba **0,652×** contra grado y da **1,010×** contra neuropilos. **La «compresión global» que reporté como hallazgo en la resp 061 es íntegramente el efecto de que las conexiones respetan neuropilos.** Contra el null correcto, no hay compresión: hay 1,0.

---

## 5. 🔥 POR QUÉ pasa, medido: las cuatro clases NO eran «igual de locales»

**El argumento central de la sección que escribí era:** *«la localidad no explica 323× entre cuatro poblaciones que son todas locales y todas craneales»*. Medí dónde vive cada una:

```
SALIDA_DOMINANTE_MOTORAS {'GNG': 89, 'PRW': 15, 'IPS_L': 3, 'IPS_R': 2, 'FLA_R': 1}

SALIDA_DOM olfactory      {'AL_L': 1295, 'AL_R': 981}
SALIDA_DOM visual         {'LA_L': 4250, 'LA_R': 3836, 'ME_R': 1315, 'ME_L': 1307}
SALIDA_DOM mechanosensory {'GNG': 1712, 'SAD': 468, 'AMMC_R': 242, 'AMMC_L': 164}
SALIDA_DOM gustatory      {'GNG': 353, 'PRW': 52, 'SAD': 3}
```

**104 de las 110 motoras tienen su salida dominante en GNG o PRW. Mechanosensorial y gustativa también.** Olfatoria vive en el lóbulo antenal; visual, en lámina y médula.

> **Las cuatro clases no son igual de locales: DOS son locales al neuropilo motor y DOS son locales a neuropilos sensoriales. Eso es el efecto entero.**

**Mi argumento no era débil: era falso, y falso por una razón que podía medir y no medí.** Escribí «todas locales» sin verificar **dónde**, que es exactamente E-01: verificar el sujeto, no uno parecido. Y es el modo de falla 11 del contexto, cometido **en el turno siguiente al que lo escribí**.

Y le da la razón a BANC verbatim: *«effector neurons are primarily influenced by sensory neurons in the **same body part**»*. A granularidad de neuropilo, esa explicación rival **gana**.

---

## 6. 🟢 LO QUE SOBREVIVE, y es mejor que lo que se cayó

**Controlando por neuropilo, el hallazgo se da vuelta y se vuelve más interesante.** El acceso motor directo (`R1`), contra el null anatómico:

| Clase | Socios motores directos, observado | Lo que predice su co-localización | z | nulls ≥ real |
|---|---|---|---|---|
| **gustatory** | **10** | **101,6 ± 1,2** | **−78,9** | **40/40** |
| **mechanosensory** | **64** | **98,6 ± 1,6** | **−21,7** | **40/40** |
| olfactory | 0 | **1,0 ± 0,9** | −1,2 | 40/40 |
| visual | 0 | **0,03 ± 0,16** | −0,2 | 40/40 |

Y a umbral 5 es aún más nítido: **gustativa 2 observados contra 91,0 esperados; mechanosensorial 33 contra 89,2. Olfatoria y visual: el null predice EXACTAMENTE 0,0.**

### El enunciado correcto, que es el inverso del que tenía

> **El cero de olfatorio y visual no es un blindaje: es geometría, y el null anatómico lo predice exactamente. El blindaje real está en las clases que SÍ comparten neuropilo con las motoras: gustativa entra al mismo neuropilo que las motoras y conecta con 10 de 110 donde su co-localización predice 102.**

**Eso sí sobrevive al null más fuerte disponible**, tiene z de −79, y no lo podía ver ninguna de las dos versiones anteriores del análisis. **Es la Propiedad 2 dada vuelta, y es publicable donde la otra no lo era.**

### ⚠️ La salvedad honesta, que NO rescata el claim viejo

Para `R1` de olfatorio y visual, **el null anatómico predice ≈ 0**, o sea que **conserva la cantidad medida** y el estado correcto para esas dos filas es **NO TESTEABLE**, no «refutado». Pero la razón por la que la conserva es que **la anatomía ya explica el cero**, así que la salvedad no devuelve el hallazgo: lo confirma como geometría.

Para `P2` el null sí se mueve (`sd` 349 sobre media 2.451), así que ahí el test es válido y el veredicto también.

---

## 7. ✅ TAREA 3 · el barrido con umbral 5, y arregla un artefacto

**Retención: 2.700.513 de 15.091.983 aristas (17,89%), 134.181 nodos, 109 de las 110 motoras.** Los valores están en la §2 de la evidencia.

**Y resuelve el censurado.** Sin umbral, `R2` daba `sd = 0,0` porque los 40 nulls llegaban al techo de 110. **A umbral 5 el `sd` es 1,04**, o sea que el censurado **era un artefacto de no aplicar umbral**, y con el criterio del campo el reach sí es estimable: olfatorio alcanza **1 de 109** contra 107,3 ± 1,0 (**z = −102**), visual **8** contra 107,3 (**z = −96**).

**Consecuencia para la decisión 7 del contexto:** adoptar el umbral de 5 no es solo alinearse con los tres papers de Nature, **es técnicamente mejor**, porque destapa un estadístico que sin umbral no se podía usar.

---

## 8. ✅ TAREA 2 · las tres figuras

Generadas por el instrumento commiteado, con los dos ensembles y los dos umbrales en cada panel:

```
8a1806e9b16db8c4d3210523d51622ef  fig_twohop_a_pathcount.svg   168.751 B
c420213caa112be0db40bb7049fc81a9  fig_twohop_b_reach.svg        31.788 B
6ffc18be441974d6fbe7239c6daef572  fig_twohop_c_normalised.svg   24.186 B
```

- **a** · `P2` observado (guion) contra las 40 realizaciones (puntos), grado a la izquierda y neuropilos a la derecha de cada clase, eje log.
- **b** · reach a 1 y 2 saltos, barras del null con su `sd` y puntos del observado, con la línea de la población motora completa.
- **c** · ratios normalizados por el control arbitrario, círculo umbral 1 y cuadrado umbral 5, borde negro grado y borde rojo neuropilos. **En este panel se ve el cruce de signo.**

**No commiteadas**, por la política del propio repo: nada de binarios derivados, van por md5 y el CI compila desde fuente. **El generador sí está commiteado y es determinista**, así que un tercero las reproduce.

---

## 9. ✅ TAREA 1 · la auditoría de estas dos horas

| Entrega | Veredicto |
|---|---|
| **resp 057** · Lin sí descompone reciprocidad | ✅ **se sostiene.** Verificado contra sus pies de figura |
| **resp 057** · el cero es anatomía de manual | ✅ **se sostiene, y ahora está MEDIDO, no inferido de literatura** |
| **resp 059** · erratum corregido | ✅ **se sostiene.** Y ahora el ítem 3 queda **mejor** apoyado: el 84% de Lin era optimista, acá el null anatómico se comió el 100% y cambió el signo |
| **resp 060** · la biblioteca, el escape, el aprendizaje | 🟡 **una parte cae: el `LC6 → GF = 0` que dejé como «ausencia de vía» ahora es testeable con neuropilos y NO se corrió.** El resto se sostiene |
| **resp 060** · «la localidad no explica 323× entre poblaciones igual de locales» | 🔴 **FALSO. Refutado en la §5** |
| **resp 061** · los 40 nulls de grado | ✅ **los números se reproducen exactamente** con código independiente · 🔴 **la interpretación cae** |
| **resp 061** · el piso de 0,652× como propiedad del conectoma | 🔴 **era anatomía.** Contra neuropilos da 1,010× |
| **resp 061** · el `grado_check_in` que no podía fallar | 🔴 confirmado como error, **corregido en el instrumento** |
| **resp 062** · la sección de la v2 | 🔴 **NO SE PUBLICA COMO ESTÁ.** Su Results y su Interpretation quedan refutados por su propia Limitation, que era correcta |
| **resp 062** · haber puesto el 0,652 y el 84% de Lin en el texto | ✅ **fue lo que salvó el turno.** El texto declaraba dónde estaba el agujero, y el agujero era real |

**El saldo, sin adornos:** de las dos horas anteriores sobreviven **todas las mediciones** y se cae **la interpretación principal**, que era mía. Es el quinto claim de causa o novedad mío que muere hoy, y los cinco tienen la misma forma: **medir bien y después afirmar por qué, sin medir el por qué.**

---

## 10. Archivos generados en este turno

| Archivo | Qué |
|---|---|
| `src/twohop_nulls.py` | el instrumento único, 469 líneas, rutas por argumento, dos ensembles, guards con control negativo |
| `docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md` | la salida cruda verbatim, los dos ensembles, los dos umbrales, los guards y el diagnóstico |
| `docs/agents/respuestas/2026-08-24-063-...md` | este |
| `docs/SECCION-V2-DOS-SALTOS.md` | **a reescribir con el veredicto invertido** |
| `docs/agents/CONTEXTO-drosophila-fep.md` | **a actualizar** |

**Todo en la rama `titan/twohop-nulls`. Nada en `main`. El merge es decisión de Abraham.**

---

## 11. NO MEDIDO, declarado

1. **El neuropilo dominante es una aproximación.** Una neurona con sinapsis repartidas entre varios neuropilos queda asignada a uno solo. **El NPC de Lin asigna por sinapsis, no por neurona**, así que este ensemble es de la **misma familia, no idéntico**, y no se comparó contra el suyo midiendo.
2. **No se corrió el NND** (probabilidad por distancia física). Las posiciones están en `annotations.tsv` (`pos_x/y/z`, `soma_x/y/z`) y **no se usó**: es la vuelta que falta.
3. **El ensemble de neuropilos no preserva el grado entrante exacto**, solo dentro de bloque. Un efecto residual puede ser de grado y no de anatomía, y **los dos nulls no se combinaron** en uno que preserve las dos cosas.
4. **Para `R1` de olfatorio y visual el null anatómico conserva la cantidad medida** (media ≈ 0). Esas dos filas son **NO TESTEABLES**, no refutadas.
5. **El hallazgo nuevo de la §6 (gustativa 10 contra 102) no tiene control de tripartición ni de distancia**, y **no se verificó si ya está publicado**. Es el mismo error que acabo de cometer si lo doy por propio sin barrer literatura.
6. **No se midió la pureza de los bloques**: qué fracción de las aristas de cada bloque pertenece a la clase medida. Sin eso no sé **cuánto** margen de movimiento le queda al null para cada clase.
7. **El `LC6 → GF = 0` del circuito de escape sigue sin testear contra neuropilos**, y ahora es testeable con estos mismos datos. **Es la deuda más barata que queda.**
8. **Las figuras no están commiteadas** (política del repo), solo por md5 y con su generador.
9. **El review automático del PR todavía no emitió hallazgos** al momento de escribir esto. **K-02: eso es deuda declarada, no aprobación.**
10. **La sección de la v2 y los contextos todavía no están corregidos en este archivo.** Son los commits que siguen.
