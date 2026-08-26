# 072 · Auditoría íntegra TITAN del proyecto

**Fecha:** 2026-08-25 08:15–09:05 (America/Buenos_Aires) · **Modo:** TITAN FULL

**Repositorio:** `gatehot59-star/drosophila-fep-connectome`

**Sujetos exactos auditados:**

- `main` en `39ce869b004f0db2716b27630e7f2576bc12ec53`.
- PR #2, `titan/twohop-nulls`, en `04bebb58c84f12fe32149ee5d7316efe9845d011`.
- PR #1 abierto y desactualizado respecto de `main`.
- 13 scripts Python/JavaScript de `src/`, los cinco logs de `results/`, `README.md`, `LICENSE`, `docs/METHODS.md`, `docs/ERRATUM.md`, el contexto vivo, el contexto de entorno, las respuestas 062 y 069–071, y el inventario de PRs/issues/commits.

## Veredicto ejecutivo

**62/100 · RECHAZADO como release reproducible.** No encontré una refutación nueva de los headline estructurales: la reciprocidad, KC→MBON y los conteos contra 40 nulls conservan evidencia fuerte. El problema no es que el proyecto no tenga resultados; es que **la rama pública, el ejecutor y el testigo no están alineados**.

El repo es científicamente fértil y documentalmente excepcional, pero hoy un tercero no puede clonar, instalar, correr y recomputar los claims principales sin reconstruir el entorno y buscar evidencia repartida entre una rama abierta, respuestas y archivos externos.

## Lo que sí sobrevive esta auditoría

1. **Los 40 nulls Maslov-Sneppen dejaron un recibo real:** 40/40 con cero mismatches de grado, 15.091.983 aristas únicas y 180,6 min de salida verbatim en `results/nulls40.log`.
2. **La capa estructural está mejor fundada que la dinámica:** conteos puros, datos identificados por checksum y anotaciones pinneadas a SHA.
3. **El erratum corrige errores reales y rastrea su causa:** overflow `int32`, umbral de cinco sinapsis, fila AN no reproducible, referencias y prior art.
4. **El proceso registra refutaciones propias en vez de borrarlas.** Eso es una fortaleza metodológica real.
5. **El resultado `sel_post` del PR #2 es prometedor:** 0/40 en siete configuraciones completas y contraste pareado con `sel_peak`. Sigue siendo prometedor, no cerrado, por los límites del null y de la ventana detallados abajo.

## Hallazgos bloqueantes

### A-01 · CRÍTICO · los guards no gobiernan el proceso

Varios scripts imprimen un estado rojo pero terminan con exit code 0:

- `src/motor.py`: si `FAILURES` no está vacío, imprime el fallo y hace `return` desde `main`; Python termina en 0.
- `src/compile_gf_full.py`, `src/sweep_tau_hetero.py` y `src/signshuffle_selpost.py`: calculan `MISMATCH_FAIL`, pero no abortan ni devuelven un estado distinto.
- `src/cp40.py`: un checksum `DISTINTO` solo se imprime y la corrida continúa.

**Impacto:** un pipeline puede declarar verde una corrida inválida. Es exactamente el patrón que el propio proyecto dice combatir.

**Corrección:** una función única `require(condition, message)` que levante excepción, tests negativos que verifiquen exit distinto de cero, y CI que ejecute esos tests.

### A-02 · CRÍTICO · `guards.py` confunde conservación con saturación

`guarded_ratio()` declara que todo `sd(null) == 0` significa “el null conserva esta cantidad”. Eso es falso cuando el ensemble está saturado en un techo distinto del observado. El propio contexto vivo distingue ambos casos, pero el módulo reusable no.

**Evidencia independiente ejecutada:** `guarded_ratio(15, [110] * 40)` devuelve `NO_MEDIDO` con razón “conserva”, aunque `15 != 110`.

`global_rank_test()` repite la misma clasificación. Esto puede ocultar una dirección válida en estadísticas de reach saturadas.

**Corrección:** si `sd == 0` y `mean == observed`, `CONSERVADO/NO TESTEABLE`; si `sd == 0` y `mean != observed`, `SATURADO`, dirección válida y efecto censurado.

### A-03 · CRÍTICO · no existe un entorno reproducible

No hay `requirements.txt`, `pyproject.toml`, lockfile, `package.json`, contenedor ni workflow de CI. Los logs registran ambientes distintos y el código depende de NumPy, pandas, SciPy, PyArrow, PyTorch y Matplotlib sin pins.

Verificación en vivo del 25-ago: PyPI publica NumPy 2.5.2, pandas 3.0.5, SciPy 1.18.1, PyArrow 25.0.1 y Matplotlib 3.11.1. El log del motor corrió con NumPy 2.0.2 y SciPy 1.16.3; el contexto preparado tiene versiones distintas. Sin lockfile, “reproducir” significa “probar suerte”.

**Corrección:** `pyproject.toml` con pins exactos, lockfile con hashes, una imagen o workflow, y matriz mínima de Python. El CI debe correr los instrumentos baratos y validar las salidas esperadas.

### A-04 · ALTO · la evidencia necesaria para recomputar no está en `results/`

`results/` tiene cinco logs, pero no `nulls40.json`, `cp40.json`, `motor_resultados.json`, `twohop_nulls_raw.json` ni los JSON del null de signo. El README afirma que los JSON se omiten por ser “grandes”, pero los tamaños documentados son 191.443 B y 31.527 B: son pequeños para git.

`results/nulls40.log` demuestra invariantes y reciprocidad, pero no contiene las matrices `Ma`/`Me` de 40 realizaciones necesarias para recomputar KC→MBON, DAN→KC o la jerarquía de ruteo. Un tercero tiene que repetir 180,6 minutos para auditar una tabla ya publicada.

**Corrección:** commitear los JSON derivados pequeños, con SHA-256, comando, versiones y esquema. Mantener fuera solo datos fuente grandes.

### A-05 · ALTO · el clon fresco no ejecuta la ruta documentada

- `src/analyze_nulls40.mjs` lee `/workspace/nulls40_kaggle.json`.
- `src/routing_hierarchy.mjs` lee `/workspace/n40_filas.json`.
- `results/` no contiene ninguno de esos archivos.
- README y METHODS dicen que los inputs “existen bajo `results/`”, pero el árbol real no los tiene.

Es un defecto conocido, pero sigue bloqueando la ejecutabilidad. Documentar una rotura no equivale a repararla.

**Corrección:** argumentos CLI, defaults relativos a la raíz y un test desde un directorio temporal vacío.

### A-06 · ALTO · el null de signo viola la ley de Dale

`compile_gf_full.py` y `signshuffle_selpost.py` permutan el signo **por arista**. Eso fabrica neuronas con salidas excitatorias e inhibitorias mezcladas, aunque el propio repo midió cero neuronas mixtas en 138.005 con salidas.

El ensemble responde “qué pasa si el signo por arista no lleva información”, pero no es un null biológicamente plausible. Por eso el salto desde “sobrevive SIGN” a “la combinación específica de signo y topología causa el efecto” es demasiado fuerte.

**Corrección:** null principal que permute identidad E/I a nivel de neurona presináptica preservando Dale, grado y distribución de pesos; dejar el shuffle por arista como control suelto secundario.

### A-07 · ALTO · el baseline de dos saltos no está pareado en grado

`twohop_nulls.py` elige un conjunto arbitrario del tamaño de visual, pero no lo empareja por grado, fuerza, superclase ni neuropilo. Después usa su ratio para normalizar el panel c y sostener ratios “corregidos”. El contexto admite que ese control tiene 1.187.513 aristas frente a 57.764–98.782 en las clases comparadas.

**Impacto:** la normalización puede medir la diferencia de grado del control, no una depresión global del conectoma.

**Corrección:** controles emparejados por distribución de out-degree y, para el null anatómico, por neuropilo/superclase. Reportar sensibilidad a varios pareamientos.

### A-08 · ALTO · el null anatómico no es equivalente al NPC de Lin

`twohop_nulls.py` y `escape_neuropil_null.py` asignan a cada neurona un único neuropilo dominante de salida y otro de entrada. El NPC de Lin conserva probabilidades entre neuropilos a nivel de la red; una neurona multineuropilo queda reducida a una etiqueta.

El propio PR lo declara, pero el texto de salida aún usa “neuropil-preserving” sin que el lector vea la pérdida. El colapso de 323× a 2,4× puede ser biología o puede ser esta discretización.

**Corrección:** null por sinapsis/edge con sus neuropilos reales, y comparación directa entre dominante, fraccional y NPC.

### A-09 · MEDIO-ALTO · `hm_sweep.welch()` no calcula Welch

La función usa `erfc(|t|/sqrt(2))`, una aproximación normal, y no calcula grados de libertad de Welch ni la cola t de Student. Con `t = 2`, `df = 18`, el código da `p = 0,04550026`; Welch exacto da `p = 0,06082147`, diferencia relativa de 25,19%.

**Impacto:** puede convertir un borde no significativo en significativo con n pequeño. Los efectos gigantes no dependen de esto, pero los bordes sí.

**Corrección:** `scipy.stats.ttest_ind(..., equal_var=False)` o implementación completa de Welch, y preferir análisis pareado por semilla cuando corresponde.

### A-10 · MEDIO-ALTO · `scriptR.py` puede reproducir el pipeline equivocado

`scriptR.py` construye `id2i` enumerando IDs raíz ordenados. Los otros scripts usan el par real `root_id → Presynaptic_Index/Postsynaptic_Index`. La igualdad entre “orden de root_id” e “índice interno” no está verificada en ese archivo.

Reproducir 30/30 valores del notebook demuestra fidelidad al pipeline histórico, no corrección del mapeo. Si el notebook original compartía el supuesto, la reproducción conserva el bug.

**Corrección:** construir el mapa desde las dos columnas ID/index del parquet y afirmar con un guard si coincide o no con el orden.

### A-11 · MEDIO · normalización espectral fail-open

`motor.normalize_spectral()` continúa y escala con un estimador que el propio código llama “límite inferior” cuando la iteración no converge. La salida lleva `rho_convergio`, pero el experimento no aborta.

**Corrección:** convergencia obligatoria o método robusto alternativo, comparación contra `scipy.sparse.linalg.eigs` en una muestra y fallo ruidoso.

### A-12 · MEDIO · la rama pública y el estado vivo divergen

`main` termina en la respuesta 062. El PR #2 contiene las respuestas 063–071 y cinco scripts nuevos. Sin embargo, `CONTEXTO-drosophila-fep.md` del PR #2 es byte-idéntico al de `main` y termina antes del null anatómico, la tabla publicada y `sel_post`.

Hay dos PRs abiertos: #1 es el initial release antiguo y #2 acumula la ciencia nueva. Un lector de `main` recibe un estado viejo; uno del PR #2 recibe código nuevo con contexto viejo.

**Corrección:** actualizar contexto en la misma unidad de cambio, cerrar/retargetear PR #1, y dividir #2 en unidades revisables o declarar que es la release candidate.

### A-13 · MEDIO · licencia no reconocible y alcance ambiguo

El archivo `LICENSE` es un aviso de 1.105 B que enlaza el texto GPL, no el texto completo. GitHub lo clasifica como “Other”. Además, “network topologies” está dentro del doble licenciamiento sin definir qué archivos abarca.

La guía GNU/SPDX recomienda incluir el texto íntegro y un identificador claro (`GPL-3.0-only` o `GPL-3.0-or-later`).

**Corrección:** texto GPL completo en `LICENSE`/`COPYING`, archivo `COMMERCIAL-LICENSE.md`, SPDX por archivo y mapa explícito de qué paths son duales.

## Hallazgos no bloqueantes

- Los nuevos scripts no validan checksum de sus cuatro inputs; el riesgo de drift volvió a entrar después de haber sido corregido en la línea estructural.
- Los argumentos aceptan `--nulls 0`, spreads inválidos y ventanas incoherentes sin validación uniforme.
- Los nombres “motor” siguen mezclando motoras de cabeza con descendentes en artefactos históricos; los scripts nuevos mejoran esto, pero el README no está al día.
- No hay escaneo de secretos del árbol completo ni política de contribución/CLA materializada, aunque el LICENSE la exige.
- Seguridad de runtime es de bajo riesgo porque son scripts batch locales, pero las descargas remotas y parsers de parquet/feather justifican checksums fail-closed.

## Prueba independiente ejecutada

```text
CASO 1: sd=0 por saturacion, real != null
{'verdict': 'NO_MEDIDO', 'reason': 'el null conserva esta cantidad (sd=0)', 'real': 15.0, 'null_mean': 110.0}
CLASIFICACION_ES_FALSA= True

CASO 2: implementacion llamada Welch usa normal, no t de Student
t=2.0 df=18 p_codigo=0.04550026 p_welch=0.06082147 diferencia_relativa=25.19%
NO_ES_WELCH= True

CASO 3: piso bilateral correcto con n=40
piso_unilateral=0.024390243902439025
piso_bilateral=0.04878048780487805
```

Instrumento: Python 3.12 + SciPy, exit code 0. La prueba no usa los datos del proyecto y puede ser contradicha recomputando las tres líneas.

## Orden recomendado, por dependencia real

1. **Hacer que un rojo sea rojo:** exit codes, checksum fail-closed y corrección conservación/saturación.
2. **Congelar el entorno:** pins, lockfile y CI mínimo.
3. **Commitear la evidencia derivada pequeña:** JSON crudo y manifiestos.
4. **Arreglar rutas y ejecutar desde clon fresco.** Recién ahí existe una release reproducible.
5. **Rehacer los nulls que sostienen claims nuevos:** Dale a nivel de neurona, baseline degree-matched y neuropilo por sinapsis.
6. **Actualizar/partir el PR #2 y el contexto vivo.** No mezclar reparación de infraestructura con decisión editorial del paper.
7. **Después** integrar `sel_post` a un paper: primero barrer ventana y tau compleja.

El criterio de orden es simple: primero lo que vuelve confiable al testigo; después lo que amplía el claim.

## TITAN SCORECARD DEL PROYECTO

| Criterio | Pts | Evidencia |
|---|---:|---|
| Completitud | 10/15 | resultados y erratum sólidos; faltan outputs crudos, entorno y estado unificado |
| Ejecutabilidad | 6/15 | scripts reales y logs, pero clon fresco roto, sin pins/CI y rojos con exit 0 |
| Seguridad | 10/15 | superficie baja; checksums no son fail-closed y faltan controles de supply chain |
| Testing | 7/15 | muchos guards y controles, pero no automatizados y uno clasifica mal saturación |
| Arquitectura | 7/10 | separación estructural/dinámica buena; loaders/nulls duplicados y ramas divergentes |
| DevOps | N/A | no es servicio desplegable; sí necesita CI reproducible, puntuado en Ejecutabilidad |
| Documentación | 8/10 | excepcional en refutaciones; README y contexto no reflejan el árbol actual |
| Innovación | 5/5 | nulls, controles y `sel_post` son aportes fuertes y falsables |
| Proceso QA | 3/5 | evidencia y errores propios registrados; review externo y gates siguen incompletos |

**Total aplicable: 56/90 → 62,2/100. RECHAZADO.**

**N/A declarado:** 10 puntos de DevOps porque el artefacto es un repositorio de investigación, no un servicio. El CI requerido se descuenta en Ejecutabilidad y Testing, no se perdona.

## Scorecard de esta auditoría

Completitud 14/15, Arquitectura del razonamiento 10/10, Documentación 10/10, Innovación 5/5, Proceso QA 4/5. **43/45 → 95,6/100.** N/A: 55 puntos por tipo de entrega.

## NO MEDIDO

1. No repetí los 180,6 min de los nulls ni las 511,8 s del barrido de tau; audité código y evidencia commiteada.
2. No leí los 72 archivos de respuesta completos; leí contexto vivo, entorno, la última de `main` y las tres últimas del PR #2.
3. No ejecuté el análisis sobre los datasets de 100,8 MB y 31,7 MB; no usé runtime ajeno.
4. No verifiqué fila por fila las tablas de Lin/Bates ni el PDF completo en este turno.
5. No corrí un secret scan del repositorio completo.
6. No abrí issues por los 13 hallazgos: hacerlo sería un lote de 5+ escrituras y requiere confirmación humana.
7. El review automático se solicita sobre el PR de esta auditoría; “sin hallazgos emitidos” no contará como aprobación.
