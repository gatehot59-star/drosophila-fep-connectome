# 059 · Erratum corregido y contexto actualizado

**Fecha:** 2026-08-24 23:15 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «ERRATUM CORREGIDO · el claim falso sobre Lin está retirado»

## 1. Pedido

«Corregí el erratum vos y commiteá.»

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_create_or_update_file` × 3 (erratum, contexto, este archivo) | sí, `main` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero mediciones nuevas. Cero Kaggle. Nada publicado en Zenodo: subir la v2 sigue siendo acción de Abraham.** No se tocó el PDF de v1.0 ni ningún resultado.

---

## 3. Qué se cambió en `docs/ERRATUM.md`

**Sigue teniendo 9 ítems.** No se agregó ni se eliminó ninguno: el cambio está **dentro** del ítem 3 más tres actualizaciones de referencias.

### 3.1 · La frase falsa, retirada explícitamente

**Salió** del ítem 3:

> ~~*«What remains specific to this work is the decomposition of reciprocity by circuit type… which the published network analyses report only as a single global figure.»*~~

**Entró** una subsección nueva: *«The claim of a novel decomposition is narrowed, and a false statement about the prior work is retracted»*, que dice verbatim **«That statement is false and is retracted here»** y después lista qué sí hace Lin: **Fig. 5c** (reciprocidad por neuropilo), **ED Fig. 6c** (*«normalised by connection density for all 78 neuropils»*, declarada como *«the region-resolved counterpart of the ratio this work reported as a single whole-brain figure»*), **Fig. 5h** (mapa entre neuropilos) y los NSRNs.

**Se retira, no se borra.** Mismo criterio que el ítem 4, y por la misma razón escrita ahí: un erratum que le atribuye a otro trabajo publicado un defecto que no tiene **es él mismo un error**, y este iba dirigido a autores con nombre y apellido en un documento citable.

### 3.2 · El claim que queda, angostado al EJE

El reclamo pasa de «descomponemos y ellos no» a **«descomponemos sobre otro eje»**: pares **dirigidos de clases funcionales** contra **subredes anatómicas**. Verbatim del texto nuevo:

> *«The two axes answer different questions: theirs, how recurrence varies across brain regions; ours, how it varies along the sensory-to-motor axis. They are complementary, and **no priority is claimed for decomposing reciprocity as such**.»*

Los ocho valores de la Table 7 quedan escritos completos en el ítem 3, así que el lector ve exactamente qué se reclama.

### 3.3 · Dos límites declarados dentro del propio ítem 3

1. **Los valores de la Fig. 5c y la ED Fig. 6c no se leyeron fila por fila**, solo sus definiciones. Si un neuropilo corresponde a un circuito de la Table 7, «complementario» es generoso.
2. **La Table 7 es sin umbral y el 13,98% es con umbral:** no son comparables entre sí. Es el modo de falla 5 de este proyecto, **declarado en vez de cometido**.

### 3.4 · Bates et al. 2026 entra como referencia

El erratum **no lo citaba**. Ahora está en la lista de referencias con DOI, y en el ítem 3 con su frase verbatim (*«nearly all-to-all pattern of reciprocal connectivity»*, cualitativa, sin ratio ni null) y en el ítem 8 como referencia faltante de v1.0.

### 3.5 · El umbral de 5 sinapsis, declarado como estándar del campo

Párrafo nuevo en el ítem 5: **los tres papers de referencia lo usan** (Dorkenwald, Lin, Bates) y el Paper 1 es el único que no, **sin declarar que se aparta de la convención**. Se declara la desviación; adoptarla es decisión para una versión futura, no una corrección.

### 3.6 · Dos ítems nuevos en *Outstanding verification* (ahora 9)

**8:** la reciprocidad por neuropilo de Lin no se leyó valor por valor, y su tabla numérica, si existe como Supplementary Data, no se recuperó.
**9:** Table 7 e ítem 5 usan criterios de inclusión distintos y **no deben dividirse ni compararse entre sí**.

### 3.7 · Y un párrafo en *How these errors were found*

> *«A claim that another paper reports only an aggregate is a claim about that paper's contents, and it has to be verified in that paper, not inferred from what it chose to emphasise.»*

Más la regla reusable al cierre: **«an assertion that a result is novel should be checked against the prior work's own figures before it is filed»**.

Y en *What has not changed*: **los ocho valores de la Table 7 no cambian. Lo que cambia es el claim de prioridad, no los números.**

---

## 4. Qué se cambió en `docs/agents/CONTEXTO-drosophila-fep.md`

Tenía el **mismo defecto** («Lin da un número global; el Paper 1 da la distribución»). Corregido y además:

- **§2.bis:** subsección nueva con la tabla de dónde descompone Lin, la Table 2 de Lin leída fila por fila (**×858 ER, ×43,8 CFG, ×45,9 NND, ×7,22 NPC**), Bates como tercera referencia completa, y el bloque de conteos de BANC con control negativo.
- **§3:** fila nueva, el **acceso motor a 2 saltos** como rescate de la Propiedad 2.
- **§4:** dos filas nuevas de refutación, **las dos contra mí**: el claim del desglose y la degradación del «refuta la localidad de BANC».
- **§5:** ítems 8, 11, 12, 13, 14 nuevos (valores de Lin sin leer · 2 saltos sin null · **105 vs 110 sin resolver** · sin columna de neuropilo · el barrido del cero no exhaustivo).
- **§6:** decisión 16 nueva (¿corro el null de grado sobre los 2 saltos?) y la 7 reforzada (los **tres** papers usan el umbral).
- **§8:** dos modos de falla nuevos, el **10** (*un claim de novedad se verifica contra las FIGURAS del trabajo previo, no contra su abstract*) y el **11** (*verificar la ESCALA a la que la explicación rival es cierta*).

---

## 5. Lo que NO se tocó, y por qué

- **El PDF de v1.0.** No se modifica: es el registro público y su DOI resuelve.
- **`README.md` y `docs/METHODS.md`.** Siguen sin la evidencia de las resp 053b y 057, y sigue pendiente la reclasificación del `temporal RDI`. **Declarado en el §5.23 del contexto.**
- **Zenodo.** Nada subido. **Es tu acción y vence el 30-ago.**

---

## 6. Archivos generados en este commit

| Archivo | Qué |
|---|---|
| `docs/ERRATUM.md` | corregido, 9 ítems, claim falso retirado, Bates citado, 9 outstanding |
| `docs/agents/CONTEXTO-drosophila-fep.md` | estado vivo actualizado |
| `docs/agents/respuestas/2026-08-24-059-...md` | este |

Previos del mismo hilo: `docs/PIVOTE-RECIPROCIDAD.md` (corregido en el commit anterior), resp **057** (la verificación con la evidencia cruda) y resp **058** (la explicación en criollo).

---

## 7. NO MEDIDO, declarado

1. **Este turno no midió nada.** Es redacción sobre las mediciones de la resp 057.
2. **El erratum corregido no lo leyó nadie más que yo.** **W-01: soy el único testigo de que la corrección es correcta.** La evidencia cruda que la sostiene está en la resp 057, verbatim y recomputable, pero **una segunda lectura humana antes de subir a Zenodo sigue siendo lo correcto** — sobre todo porque el error que se corrige nació exactamente de que nadie revisó el borrador anterior.
3. **No verifiqué el erratum entero línea por línea contra el PDF en este turno.** Cambié lo que tenía que cambiar; **el resto conserva el estado de la resp 046 y no recibió veredicto de vigencia nuevo** (modo de falla 4).
4. **Betzel y los dos DOI siguen sin verificar**, y están declarados así dentro del propio erratum.
5. **La discrepancia 105 vs 110 no entró al erratum** porque el cero de motoras de cabeza **no es un resultado de v1.0**: es del 24-ago. Si va a la v2 del paper, el denominador hay que fijarlo antes.
