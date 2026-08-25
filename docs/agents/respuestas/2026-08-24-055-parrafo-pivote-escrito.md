# 055 · El párrafo pivote, escrito

**Fecha:** 2026-08-24 22:20 (America/Buenos_Aires)

> **📄 Doc de ClickUp:** «EL PÁRRAFO PIVOTE · de “es enorme” a “está distribuida”»

## 1. Pedido

«Armá el párrafo pivote para el paper».

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_get_file_contents` × 4 | no | no |
| `githubmcp_create_or_update_file` × 2 | sí, en `main` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero mediciones nuevas en este turno. Cero Kaggle. Nada publicado en Zenodo. El PDF y el erratum no se tocaron.** Es un turno de **redacción**, y los números son todos preexistentes y trazables.

## 3. Qué se entregó

**`docs/PIVOTE-RECIPROCIDAD.md`**, con cinco partes:

- **A** · versión corta para el **Abstract**, que reemplaza la frase del 36×.
- **B** · versión larga para **Results / Discussion**, en tres párrafos: el global no es distintivo → la distribución por circuito sí → relación con Lin y BANC.
- **C** · **qué hay que borrar** cuando se pega: el 36×, el `Density = 0.0074`, el claim de novedad del CP, y la palabra «motor» sin calificar.
- **D** · las **tres referencias** que el párrafo obliga a agregar, completas y con páginas.
- **E** · **seis NO MEDIDO** que el párrafo asume.

## 4. La lógica del pivote, en una línea

**No se corrige un número: se cambia el sujeto del claim.** De «la reciprocidad es enorme» (que es falso como novedad, porque Lin la encuentra comparable en cinco cerebros) a **«la reciprocidad está distribuida de forma no uniforme, decrece hacia la salida motora, y se anula exactamente en la vía que la propagación identifica como más depletada»**. Lo primero es un récord discutible. Lo segundo es un **resultado estructural** que nadie publicó, y que ata la Tabla 7 con la Propiedad 2.

## 5. Números usados y de dónde salen

| Número | Fuente |
|---|---|
| 26,60% · 4.014.518 aristas · 20,59× · 0/40 | 40 nulls CP, doc `6057` |
| 13,98% con umbral ≥5 · 12,647 sinapsis/conexión | resp 045 |
| 13,8% de Lin · 12,6 de Dorkenwald | §2.bis del contexto, verificado el 24-ago |
| los 8 valores por circuito | **Table 7 del PDF publicado** |
| R² = 0,94 en 94.278 pares | BANC, leído en PMC |
| 1.303 descendentes + 110 motoras | resp 053b |
| cero visual/olfatorio → motoras de cabeza · 14 del nervio antenal | resp 053b, medido |
| densidad real 7,85197×10⁻⁴ | resp 043 |

## 6. Archivos generados

- `docs/PIVOTE-RECIPROCIDAD.md` (nuevo)
- `docs/agents/respuestas/2026-08-24-055-parrafo-pivote-escrito.md` (este)

## 7. NO MEDIDO, declarado

1. **Los seis ítems de la parte E del propio archivo**, que son los agujeros del texto.
2. **El párrafo no está integrado**: ni en el PDF, ni en `docs/ERRATUM.md`, ni en el `README`. Es texto suelto listo para pegar, **y pegarlo es decisión de Abraham**.
3. **No se recomputó la Table 7 con umbral ≥5**, así que la tabla y el 13,98% conviven en el mismo párrafo con criterios distintos. **Es el modo de falla número 5 de este proyecto y esta vez está declarado en vez de cometido.**
4. **No se verificó si Lin o BANC reportan reciprocidad por circuito.** Si alguno lo hace, la parte B pierde su reclamo central.
