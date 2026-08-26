# 077 · A-10 verificado · **NO SOSTENIDO**, y apareció otro defecto al lado

**Fecha:** 2026-08-25 09:15 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **🔬 Evidencia cruda:** `docs/agents/evidencia/2026-08-25-A10-idmap-evidencia-cruda.md`
> **🛠 Instrumento:** `gateway build.run` sobre `brain-env`, 3 corridas, solo lectura sobre `/workspace`
> **🔎 Sujeto:** `src/scriptR.py`, blob SHA `2014cf54755273ee4cdceb652c44597013176bf3`

---

## 1. Pedido

«Verificá A-10 ahora.» El hallazgo que la resp 073 dejó como **prioridad técnica máxima** y sin verificar.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `githubmcp_get_file_contents` × 5 (orden a Tao, `src/`, `scriptR.py`, resp 073, dos listados de rama) | no | no |
| `mcp_gateway build.run` × 4 sobre **`brain-env`** (3 mediciones + 1 fallida por el `\n` literal) | solo `/workspace/*.log` | **NO** |
| `githubmcp_push_files` × 1 → **rama `titan/twohop-nulls`** | sí | no |
| `create_document` × 1 (ClickUp) | sí | no |

**Cero Kaggle. Cero runtime de Tachi. `/workspace` solo leído. Nada borrado. Ningún merge. `main` intacta.**

## 3. 🟢 A-10 · NO SOSTENIDO, y el margen no es estrecho

**Lo que decía A-10** (resp 073 §5, verbatim): *«Si `id2i` por orden de `root_id` no coincide con el índice del parquet, los 30/30 valores reproducidos reproducen un bug»*.

**El defecto era plausible leyendo el código:** `W_raw` se indexa con `Presynaptic_Index`/`Postsynaptic_Index` del parquet, mientras que **todas** las poblaciones (`idx_S`, `idx_mu`, `stim`, `idx_motor`) se indexan con el **rank del ID ordenado**. Dos órdenes distintos para la misma matriz.

**Medido: son el mismo orden, exactamente.**

| Medición | Resultado |
|---|---|
| Aristas con `rank(Presynaptic_ID) != Presynaptic_Index` | **0 de 15.091.983** |
| Aristas con `rank(Postsynaptic_ID) != Postsynaptic_Index` | **0 de 15.091.983** |
| Neuronas con `Index` distinto de su rank | **0 de 138.639** |
| `len(ids)` vs `N` de la matriz | **138.639 = 138.639** |
| Biyección ID ↔ Index y slots vacíos | **0 violaciones, 0 slots sin ID** |
| `ids` estrictamente creciente (o sea `enumerate` **es** el rank) | **True** |
| **Control negativo** (dos IDs swapeados en la referencia) | **277 mismatches** en 200.000 aristas → **el test puede dar rojo** |

**Corroboración cruzada que no pedí:** las neuronas presinápticas únicas dan **138.005**, exactamente el denominador de la ley de Dale ya publicado (*«0 mixtas de 138.005»*). **Dos mediciones independientes, mismo número.**

> **Los 30/30 valores del Script R no reproducen un bug de indexado. La fidelidad Y la corrección del mapeo se sostienen.**

**Lo que de A-10 sigue en pie:** su **criterio** — distinguir *reproducir el pipeline* de *que el pipeline esté bien* — es correcto y hay que conservarlo. Lo que no se sostiene es la instancia que señalaba.

## 4. 🔴 Y el eslabón siguiente sí está roto · hallazgo nuevo

No cerré en el primer resultado: medí el paso que viene después del mapeo. `byidx()` hace

```python
return np.array([id2i[int(x)] for x in rr if int(x) in id2i], dtype=np.int64)
```

**y ese `if` descarta filas de `annotations.tsv` sin contarlas ni avisar.** Medido:

| Población | Filas | Mapeadas | **Perdidas en silencio** |
|---|---|---|---|
| `flow == afferent` (S) | 19.262 | 18.664 | **598** (3,1%) |
| `cell_class == visual` | 11.391 | 10.855 | **536** |
| `flow == intrinsic` (μ) | 118.497 | 118.480 | 17 |
| `mechanosensory` | 2.668 | 2.656 | 12 |
| `flow == efferent` (A) | 1.489 | 1.481 | 8 |
| `olfactory` | 2.282 | 2.279 | 3 |
| `super_class == motor` · `brain_motor_neuron` · `gustatory` | 110 · 105 · 408 | 110 · 105 · 408 | **0** |

**Total: 623 filas descartadas**, y **no están repartidas al azar**: se concentran en la población **sensorial**, y dentro de ella en **visual**. Es el **modo de falla 6** del proyecto (un camino que no puede dar rojo) aplicado a una pérdida de población en vez de a un guard.

**🟢 El atenuante, y está medido, no argumentado:** los conteos **post-filtro** son **exactamente** los `N_mio` de la Tabla 5 recomputada que ya está en el contexto — visual **10.855**, mechano **2.656**, olfactory **2.279**, gustatory **408**, motoras **105/110**. **El filtro ya estaba incorporado en todos los números vigentes: no invalida ninguno.** Lo que faltaba era **declararlo**, y ahora está declarado con su tabla.

**Recomendación (no aplicada, porque tocar `scriptR.py` cambia el instrumento de un resultado publicado):** que `byidx` **cuente y reporte** los descartes, y que aborte si superan un umbral. Es el mismo `require()` que piden A-01 y A-02, en otro archivo.

## 5. 🔴 Novena autorrefutación, y es de mi turno anterior

La **resp 075** declaró, verbatim: *«Existencia de una resp 072: **NO EXISTE.** Correlativo faltante, no pérdida · instrumento: listado del directorio»*.

**Existe.** Es `docs/agents/respuestas/2026-08-25-072-auditoria-integra-titan.md`, **en la rama `titan/auditoria-integra-2026-08-25`**: es el informe de auditoría de Tao. La resp 073 lo linkea en su encabezado, y yo leí ese encabezado en este turno.

**El error:** verifiqué en el listado de **una** rama y lo reporté como hecho del repo. Es el **modo de falla 1** — *el denominador se mide en la fuente, no en la copia* — y lo cometí **en el turno en que unificaba el contexto para arreglar A-12**. Igual que el `grado_check_in` del 24-ago: el modo de falla estaba escrito y presente.

**Y hay un agravante de forma:** lo escribí con la etiqueta **«verificado en el listado, no inferido»**, que es precisamente el sello que este proyecto usa para decir *«esto lo podés cobrar»*. **Un sello de verificación sobre un alcance mal declarado es peor que no ponerlo.**

## 6. Archivos generados en este turno

| Archivo | Qué |
|---|---|
| `docs/agents/evidencia/2026-08-25-A10-idmap-evidencia-cruda.md` | comandos y salidas verbatim de las tres corridas, con qué prueba cada línea |
| `docs/agents/respuestas/2026-08-25-077-A10-verificado-no-sostenido.md` | este |
| Doc de ClickUp | «A-10 NO SOSTENIDO · el mapeo está bien, pero encontré otro agujero al lado» |

## 7. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | el sujeto exacto de A-10 medido en las dos columnas y por arista **y** por neurona, más el eslabón siguiente. **−1:** no se re-corrió `scriptR.py` entero |
| **Ejecutabilidad** | 14/15 | tres corridas con salida cruda. **−1:** una cuarta falló por el `\n` literal del shell, modo de falla ya documentado del entorno |
| **Arquitectura del razonamiento** | 10/10 | el veredicto no descansa en «no hay mismatches»: se probó antes que el mapeo es **biyectivo**, que `ids` es estrictamente creciente y que el comparador **puede dar rojo** (277 con dos IDs swapeados; 138.625 → 559 en el `isin`) |
| **Documentación** | 10/10 | evidencia verbatim, tres estados separados (mal / atenuante medido / no medido), y la autorrefutación de mi propio turno anterior en su propia sección |
| **Innovación** | 3/5 | la corroboración cruzada con el 138.005 de Dale salió gratis del mismo instrumento. **−2:** es una verificación, no un aporte |
| **Proceso QA** | 4/5 | veredicto con evidencia citada y hallazgo nuevo declarado como tal. **−1:** el hallazgo del `byidx` **no tiene review externo** (K-02) |

**Total 55/60 → 91,7/100.** **N/A: 40 pts** (Seguridad 15, Testing 15, DevOps 10).

**W-01:** soy el único testigo de este veredicto, y es un veredicto que **me favorece** (dice que mi código estaba bien). Por eso la evidencia va cruda y verbatim, con el control negativo incluido: **el criterio es que cualquiera pueda recomputarlo y contradecirme.**

## 8. NO MEDIDO, declarado

1. **El informe de Tao (`072`) no se abrió verbatim.** El enunciado de A-10 se tomó de la **resp 073 §5**, que es mi propia paráfrasis. **Si Tao le dio a A-10 un alcance más amplio que el mapeo `id2i`, este veredicto cubre solo la parte citada.** Es el riesgo E-01 residual de este turno.
2. **No se recomputaron los md5** de `connectivity.parquet` ni `annotations.tsv` en esta corrida: se citan los declarados, con **coincidencia de tamaño en bytes, no de hash**.
3. **No se re-corrió `scriptR.py` entero.** Se verificó el mapeo, no los 30 valores uno por uno.
4. **Las 623 filas descartadas no se caracterizaron:** ¿segmentos del release v783 o neuronas sin aristas? `annotations.tsv` tiene 139.248 filas contra 138.639 IDs, y **14 IDs del grafo no tienen fila en annotations**.
5. **Nada de pesos, signo, normalización ni `τ`** entra en esta medición.
6. **A-11 y A-13 siguen sin verificar.** Los 13 issues siguen sin abrir (esperan el OK de Abraham).
7. **El contexto vivo queda con dos líneas desactualizadas y las nombro** en vez de reescribirlo de memoria, porque reemitir 40 KB desde memoria de modelo arriesga degradar un archivo bueno: (a) la línea *«no existe una 072»*, refutada en la §5; (b) A-10 figura como **NO MEDIDO** y ahora es **NO SOSTENIDO**. **Se corrigen en el próximo commit de contexto, junto con `CONTEXTO-motor.md`, que es el otro medio A-12.**
8. **`CONTEXTO-motor.md` sigue sin abrirse**, tercer turno consecutivo. **Sin veredicto de vigencia.**
