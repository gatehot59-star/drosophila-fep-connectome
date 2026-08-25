# 062 · La sección de 2 saltos, redactada

**Fecha:** 2026-08-24 23:55 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «SECCIÓN DE 2 SALTOS · lista para pegar en la v2»

## 1. Pedido

«Redactá la sección de 2 saltos para la v2». Era la decisión 16 de la §6 del contexto.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_create_or_update_file` × 2 | sí, `main` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero mediciones nuevas.** Turno de redacción sobre la resp 061. **Nada de Kaggle, nada a Zenodo, el erratum NO se tocó** (y no debe tocarse: esto es material nuevo, no una corrección de v1.0).

---

## 3. Qué se entregó: `docs/SECCION-V2-DOS-SALTOS.md`

Seis partes, en inglés de paper y listas para pegar:

| Parte | Qué |
|---|---|
| **A · Methods** | definición de la población motora con **los dos denominadores declarados**, los dos estadísticos (`R_k` y `P_2`) con la fórmula explícita, el null, y **los tres controles** |
| **B · Results** | el cero de 1 salto con su expectativa, la tabla de `P_2`, el baseline de 0,652, el reach como **censurado**, y la Interpretation |
| **C · Limitations** | el null anatómico ausente, el argumento que no lo necesita, los límites del estadístico, y que **el blanco no es músculo** |
| **D** | qué figura y qué tabla faltan: **tres paneles, ninguno generado** |
| **E** | las tres referencias que la sección obliga a citar, con páginas |
| **F** | **nueve NO MEDIDO** |

---

## 4. Las tres decisiones de redacción, y por qué

### 4.1 · El estadístico principal es `P_2`, no el reach, y se dice por qué

El reach (motoras distintas alcanzadas) **se satura**: los 40 nulls dan 110 de 110, `sd = 0`. La sección lo reporta como **censurado por techo** y aclara verbatim que *«the direction of the effect is unambiguous… but the magnitude is not estimable from this statistic, which is why path count is used for quantification»*.

**Por qué importa:** un `sd = 0` por saturación **no** es el mismo defecto que un `sd = 0` por conservación. En el segundo el null **iguala** al real y el test no puede fallar; acá el null da 110 y el real 15, o sea que el real cae fuera del ensemble entero. **Distinguir los dos casos por escrito es lo que evita que un revisor lea «sd cero» y tire la sección.**

### 4.2 · El baseline de 0,652 va en Results, no escondido en el suplementario

El control arbitrario dio **0,652×**, o sea que el grafo real tiene menos caminos de 2 saltos que un grafo de configuración **en general**. La sección reporta **los ratios crudos Y los normalizados** (olfatorio 28,6× y no 43,9×; visual 10,8× y no 16,5×), y aclara que el spread de 323× **es invariante** a la normalización porque es un cociente de dos cantidades normalizadas.

**Es el número menos favorable de la sección y va arriba a propósito.** Un revisor que corra su propio control lo encuentra en diez minutos.

### 4.3 · La Limitation principal se escribe con el número de cuánto puede costar

En vez de «faltan controles espaciales», la sección dice **cuánto se lleva un control espacial cuando existe**: en Lin, pasar de grado (43,8×) a neuropilo (7,22×) **absorbe el 84% del efecto**, y después dice *«No comparable reduction can be excluded here»*.

**Y a continuación el párrafo que salva el resultado sin ese null:** la explicación espacial tiene que explicar **el orden entre cuatro poblaciones que son todas locales y todas craneales**. El caso decisivo es gustatory: es la **más chica** (`N = 408`) y sale **enriquecida 10×**, mientras visual es la **más grande** (`N = 10.855`), **alcanza más cerebro que ninguna** y sale depletada. **La localidad no produce 323× entre poblaciones igual de locales.** Y el texto cierra concediendo: *«The absolute ratios should be regarded as upper bounds; the ordering and the spread should not.»*

---

## 5. Lo que la sección conecta, y no existía como enunciado

Tres mediciones que estaban sueltas quedan en un solo argumento:

1. **Tabla 5 de v1.0:** visual y olfatorio depletados a 1 salto.
2. **El circuito de escape:** `GF → MOTOR = 0`, o sea que la vía visual más rápida del animal **no toca motoras** y sale por descendentes.
3. **Los 2 saltos:** la asimetría persiste cuando el confinamiento ya no aplica.

**El enunciado que sale:** *la variable que ordena no es cuán lejos proyecta una modalidad, sino sobre qué blancos se le permite influir.* Y en la parte F queda declarado que **«permitted» es interpretación, no medición**: no hay mecanismo de desarrollo ni funcional detrás de esa palabra.

---

## 6. Archivos generados

- `docs/SECCION-V2-DOS-SALTOS.md` (nuevo)
- `docs/agents/respuestas/2026-08-24-062-seccion-de-2-saltos-redactada.md` (este)

---

## 7. NO MEDIDO, declarado

1. **Este turno no midió nada.** Todo número viene de la resp 061 y es recomputable desde ahí.
2. **Las tres figuras no existen.** La sección las especifica panel por panel y ninguna está generada.
3. **La sección no está integrada al PDF.** Es texto suelto listo para pegar, y pegarlo es de Abraham.
4. **No re-leí v1.0 en este turno** para verificar que la numeración de secciones y el estilo de citas encajen. **Modo de falla 4: no le doy veredicto de vigencia a un archivo que no abrí hoy.**
5. **Los nueve ítems de la parte F del propio archivo**, empezando por el null anatómico.
6. **No verifiqué si este análisis multi-salto por modalidad ya está publicado.** Cinco búsquedas no lo encontraron: **apoyado, no establecido.**
