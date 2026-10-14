# Cierre de la v2.0 del Paper 1 · estado al 2026-10-12

**Respuesta:** `docs/agents/respuestas/2026-10-12-007-la-v2-del-paper-esta-lista-y-el-erratum-tenia-errores-sobre-la-v1.md` · **Rama:** `titan/v2-cierre-2026-10-12` · **PR a main sin merge** (el merge lo decide Abraham).

**Corrección posterior (12-oct, noche):** `docs/agents/respuestas/2026-10-12-018-paga-la-tarea-de-la-mosca-la-regla-era-la-mosca-idealizada-y-la-v2-quedo-corregida.md` corrige las tres inconsistencias que confirmó la 2026-10-12-010 (§3b). Los PDF del depósito cambiaron: los de la tabla del §2 son los nuevos.

## 1. Qué es la v2.0

- **Manuscrito:** `docs/v2/paper1-v2.0.md`, fuente canónica en Markdown. No había fuente en Zenodo ni en el repo: se reconstruyó desde el texto del PDF v1.0 (185.471 B, md5 `c7cb36a261182f6ce895057ebe26e505`, 7 páginas, extraído con pypdf 6.16.2). Si Abraham tiene el .docx o el LaTeX original, el contenido de la v2.0 se puede portar ahí; no hace falta para depositar.
- **Alcance:** la v1.0 con el erratum aplicado, la reciprocidad como rango contra nulos (`docs/PIVOTE-RECIPROCIDAD.md`) y la sección de dos saltos después del null anatómico (`docs/SECCION-V2-DOS-SALTOS.md`, ahora §3.4 con las Tablas 5b y 5c).
- **Fuera de la v2.0, por recomendación de BRAIN y revocable:** el control de las salidas (2026-10-10-005 a 009), LC6→GF y sel_post. Son otra pregunta, con nulos propios y en ramas sin review; meterlos convierte una corrección urgente en otro paper. Van al Paper 2.
- **Título:** el mismo de la v1.0, para que la versión nueva cuelgue del mismo concepto sin confundir.

## 2. Archivos del depósito

Binarios derivados: no se commitean. Viven en brain-env y se recomputan con `tools/v2/render_v2.py` (pandoc 3.10.2 + typst 0.15.0, determinista).

| Archivo | Bytes | Páginas | md5 | Fuente (md5) |
|---|---|---|---|---|
| `Mendieta2026_Paper1_v2.0.pdf` | 327.479 | 17 | `d353cf0fd05e9e5637be2bccca7bc98e` | `docs/v2/paper1-v2.0.md` (`e5fb86dc…`) |
| `Mendieta2026_Paper1_Erratum_v1.0.pdf` | 191.172 | 15 | `05052e6e7e0dd79cee584c9d285b1b93` | `docs/ERRATUM.md` (`f2ad0507…`) |

Rutas y md5 en `docs/v2/archivos-deposito-v2.0.json` (ahora `/workspace/v2cierre_2026-10-12/deposito_018/`; los PDF anteriores, `50df4ab9…` y `28f7a21f…`, siguen en `deposito/` y ya no son los del depósito). Logs crudos: `docs/v2/render-v2.0.log` (PASS, 19/19 chequeos de texto, dos compilaciones iguales, más el control de texto viejo contra nuevo) y `docs/v2/verificar-v2.0.log` (PASS, 8/8 campos y 2/2 archivos). Metadatos: `docs/v2/zenodo-v2.0-metadata.json`.

## 3. Qué se corrigió en el erratum antes de depositarlo

Cotejado contra el texto del PDF v1.0, no contra la memoria:

1. **Ítem 8, al revés:** la v1.0 dice *«Factor 3×, rate 100%»* y el erratum decía que la v1.0 decía 98,5%. Medido 98,5% (`docs/METHODS.md`); lo que hay que corregir es el 100% de la v1.0.
2. **Ítem 2, conteo inconsistente:** declaraba la fila AN no reproducible y después la contaba como cuarta enriquecida; el 991× usaba la AN completa (2.231) y el texto nombraba 12,9× como extremo. Ahora: 3 enriquecidas, 4 empobrecidas, 1 dentro, AN aparte; 713× sobre las 8 reproducibles.
3. **Tabla 7:** sensory→descending es 8,6 (doble redondeo), como quinto problema de conteo; el pendiente 9 (la tabla con ≥5) queda resuelto.
4. **Referencias:** Betzel verificado; Gouwens & Wilson, Nagel & Wilson, Tuthill & Wilson, Hasani y Schlegel tenían datos mal, y Nagel & Wilson estaba citado para algo que no trata.
5. **Calificación nueva al ítem 2:** con el null anatómico, el orden por modalidad es co-localización; la lectura por urgencia no se sostiene más allá de eso.
6. **Ítem 7, agregado en la 018:** la v1.0 dice que la amplificación temporal está *«validated across three compatible models»* y su propia Tabla 9 muestra que LIF-soft decae (0,253 a 0,002): la amplificación aparece en dos de los tres modelos compatibles.

## 3b. Qué se corrigió en el manuscrito después de la 010 (respuesta 018)

Parche `tools/v2/fix_v2_018.py` (md5 `4c4039d2…`): 15 reemplazos, cada uno exigido una sola vez; aplicado en brain-env y, por separado, en Actions (Python 3.12.3), con los mismos md5 en los cuatro archivos (`docs/v2/fix-v2-018.log`).

1. **El «2.4-fold» (§3.4):** era visual sobre gustatory (1,531 / 0,632 = 2,42), no el cociente entre extremos con que se definía el 323× (mechanosensory sobre olfactory, 7,364619 / 0,022797 = 323,05). Sin umbral el cociente entre extremos cae de 323× a **4,2×** (visual 1,531 sobre olfactory 0,368); con el umbral de cinco sinapsis, de 3.862× a 40×. Valores sin redondear de `docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md` (rama `titan/materializacion-h4-guard-2026-10-02`). Corregido también en `docs/SECCION-V2-DOS-SALTOS.md`.
2. **«Validated across three compatible models» (§2.5, resumen, §1.3, nota de la Tabla 9, §4.1, Limitación 3 y cambio 6):** compatible con la métrica no es replicar. La amplificación aparece con SparseLTC (0,630 a 0,832) y Linear (0,623 a 0,835); con LIF-soft el RDI coseno decae de 0,253 a 0,002. El texto ahora la declara para los dos modelos que la muestran. También en la descripción de Zenodo.
3. **«Not testable» sin precisar umbral (§3.4):** sin umbral el ensemble de neurópilo espera 1,0 ± 0,9 y 0,03 ± 0,16 contactos, así que el cero observado es compatible (z −1,2 y −0,2) y no significativo; sólo con el umbral el ensemble da 0,0 exacto y la prueba no es posible. Corregido también en `docs/SECCION-V2-DOS-SALTOS.md`.

**No tocado en la 018:** la Tabla 8. El resumen y el §4.1 siguen usando *Z*~CP~ = +14,8σ como resultado firme mientras el §3.7 y la Limitación 5 dicen que no se reprodujo. Es la cuarta contradicción de la 010 y la decide Abraham.

## 4. Cómo se deposita

**Opción A, recomendada (token):**

1. Abraham genera un token en Zenodo: Applications → Personal access tokens → New token, con los alcances **`deposit:write`** y **`deposit:actions`** (el segundo hace falta para crear la versión nueva y para publicar; el inventario sólo nombraba el primero).
2. El token va a brain-env como `/workspace/.zenodo_token` (permisos 600). Si lo pasa por el chat, BRAIN lo escribe ahí sin imprimirlo, y conviene revocarlo después.
3. `python3 tools/zenodo/depositar_v2.py --borrador` crea la nueva versión como **borrador** desde la v1.0, le saca el PDF heredado, sube los dos PDF cotejando el md5 que devuelve Zenodo y carga los metadatos. **No publica.** Imprime el link del borrador.
4. Abraham revisa el borrador en Zenodo, en el teléfono si quiere.
5. Publicar es **irreversible** (acuña el DOI): con el botón Publish de Zenodo, o `--publicar ID` con su sí explícito.
6. Revocar el token.

**Opción B (manual):** en el registro de la v1.0, *New version*; borrar el PDF heredado; subir los dos PDF; copiar título, descripción, palabras clave y versión del JSON; publicar. Para eso hay que bajar los PDF de brain-env, que hoy no tiene salida directa a Abraham: la vía A es la práctica.

## 5. Decisiones que esperan a Abraham

1. **Merge del PR** de `titan/v2-cierre-2026-10-12` a main.
2. **Token** de Zenodo (o la vía manual).
3. **Alcance:** la v2.0 sin el control de las salidas, que pasa al Paper 2.
4. **Conflict of interest:** la v2.0 agrega que el motor embebido y las topologías se ofrecen con GPLv3 o licencia comercial. Si no quiere declararlo, se saca antes del render.
5. **Título:** igual al de la v1.0.
6. **Tabla 8 (018):** calificar el +14,8σ en el resumen y el §4.1 como no reproducido, o volver a buscar su productor.

## 6. NO MEDIDO

- **Nadie miró los PDF**: sólo extracción de texto y 19 cadenas de control, más el control de texto viejo contra nuevo de la 018. Maquetación, cortes de tablas y fórmulas se revisan en el borrador de Zenodo.
- **Los metadatos no se probaron contra la API real**: sólo que están los campos que Zenodo exige.
- **El token no existe en brain-env** (medido: sin variables ni archivos `zenodo`).
- **Barrido sistemático de literatura para §3.4**: sólo básico (Gordon & Scott 2009; Shiu et al. 2022).
- **El rango 5–20 ms de Gouwens & Wilson (2009)** no se releyó contra el paper.
- **Tabla 8**: sigue sin reproducirse desde el código archivado.
- **Valores de Lin et al. por neuropilo**: sin cruzar.
- **La fila AN y la décima clase de la Tabla 5**: sin resolver.
- **El informe completo de Tao** sigue sin archivar; lo que dice y la 018 no reprodujo queda sin cotejar.
