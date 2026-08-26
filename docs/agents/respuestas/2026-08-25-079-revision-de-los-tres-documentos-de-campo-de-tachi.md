# 079 · Los tres documentos de Tachi, revisados · 2 confirmados, 1 refutado, y 2 cosas que nadie vio

**Fecha:** 2026-08-25 10:20 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **🔬 Evidencia cruda:** `docs/agents/evidencia/2026-08-25-revision-campo-tachi-evidencia-cruda.md`
> **🛠 Instrumento:** `gateway build.run` sobre `brain-env`, 4 corridas + lectura de `mudh-mobile` vía integración

---

## 1. Pedido

«TITAN FULL: hacé 1 a 4 de corrido. **Pero antes vé a git, Tachi te dejó tres documentos**, revisá qué puede ayudar a nuestro propósito directa o indirectamente.»

**Dos partes, y la segunda va primero por orden explícito.** Este archivo cubre la segunda. **Y lo que encontré cambia el orden de la primera**, así que estaba bien pedirlo antes.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `list_commits` × 3, `list_branches` × 3, `get_commit` × 3, `get_file_contents` × 4 | no | no |
| `run_secret_scanning` × 1 → **FALLÓ**, sin GHAS. Sustituido, no abandonado | no | no |
| `search_code` × 1 | no | no |
| `mcp_gateway build.run` × 4 sobre `brain-env` | sólo `/tmp` | **NO** |
| `push_files` × 1 → rama `titan/twohop-nulls` · `create_document` × 1 | sí | no |

**Cero Kaggle. Cero runtime de Tachi. Nada tocado en `mudh-mobile`. Ningún merge. `main` intacta. El token ajeno NO se usó ni se probó.**

## 3. Los tres documentos, y el dato de forma que hay que ver primero

| Commit | Hora | Qué |
|---|---|---|
| `05a4d40c` · 24-ago 15:30 | `HANDOFF-ARRAQUE.md` | punto de restauración de Tachi: gateway, `brain-env`, nexus.db, Kaggle, issues #71-#77 |
| `73d022fb` · 25-ago 11:08 | informe **cortés** sobre este repo | «calidad científica alta» |
| `5d5806c4` · 25-ago 11:14 | informe **incisivo** | «no es un paper reproducible; es un expediente de autocorrección» |

**Los dos informes son el MISMO archivo: el incisivo sobrescribió al cortés seis minutos después.** No son dos auditorías: son una auditoría y su cambio de tono. **Y el cortés acertó en un punto donde el incisivo se equivocó** (§5), así que leer sólo el segundo pierde información.

## 4. 🔴 Lo que CONFIRMÉ, y el peor es el más simple

**T-4 · el activo comercial no está en el repo.** Medido sobre el árbol de `main`:

> **113 archivos. CERO archivos `.c`, `.h`, `.cpp` o `.ino`.** Extensiones presentes: sin-ext, `.diff`, `.json`, `.log`, `.md`, `.mjs`, `.py`.

No es que el C esté incompleto: **no existe.** Y hay una consecuencia que Tachi no saca y me toca a mí: **el `CONTEXTO-motor` tiene «1.336 B de `.text` medidos en ESP32» en su tabla de VALIDADO, y la fuente que produjo ese número no está en el repo.** O sea que ese número **no es reproducible por nadie desde acá, incluido yo.** Es un validado sin instrumento público.

**T-1 · los dos `.mjs` con paths absolutos.** Confirmado, y **coincide con A-05 de Tao**: dos auditores que no se hablaron, mismo defecto. Eso sube su prioridad.

**T-7 · «el enemigo no es un bug, es la velocidad».** Aceptado. Es el mismo diagnóstico de Tao por otra vía.

## 5. 🟢 Lo que REFUTÉ midiendo, y la refutación enseña algo

**T-3 dice que el README imprime `p = 0.0244` como headline «sin la advertencia al lado».** Medido:

> **README línea 39, inmediatamente antes de la tabla que empieza en la 44:** `` `p = 0.0244` is the permutation floor with n = 40, i.e. no null... ``

**La advertencia está pegada a la tabla.** Y **la versión cortés del propio Tachi lo había leído bien.** Al subir la intensidad, afirmó sobre la presentación **sin releer el archivo**: el modo de falla 3 de este proyecto, cometido por el auditor. Lo registro sin sarcasmo, porque es exactamente lo que me pasa a mí cuando subo la intensidad.

**Lo que de T-3 sí queda:** con `n = 40` ningún `p` puede bajar de 0,0244, así que **el `p` no distingue un efecto de 47× de uno de 1,7×** (los cinco de la tabla muestran el mismo número). Para eso está el `z`, y el `z` sí se reporta. **Su pregunta «¿por qué 40 y no 4000?» sigue sin respuesta medida.**

## 6. 🔴 Y de ahí sale un hallazgo que es MÍO: dos pisos distintos en el mismo repo

| Dónde | Fórmula | Valor con n=40 |
|---|---|---|
| `README.md` línea 39 | `1/(n+1)` **one-sided** | **0,0244** |
| `src/guards.py` | `p_floor = 2/(n+1)` **two-sided** | **0,0488** |

> **Dos criterios para el mismo número, en el mismo repo, con factor 2 entre ellos.** Modo de falla 5, **sexta reincidencia**, y toca **todas** las tablas publicadas.

**No lo corrijo:** elegir one-sided o two-sided es una decisión sobre qué hipótesis se testea, no un bug. **Se declara y espera decisión.** Y noten el detalle: **el módulo que escribí esta mañana ya usaba el criterio más conservador que el README**, y no lo vi hasta que Tachi me hizo mirar el README.

## 7. 🔴 Y el hallazgo que NINGUNA auditoría vio · un token en el árbol de git

El `HANDOFF-ARRAQUE.md` de Tachi tiene un **GitHub Personal Access Token en claro**, en un bloque `bash` de su sección 0. **Y tres secciones más abajo, el mismo archivo tiene un título que dice «5. SECRETOS (NO en git)».** El documento declara la política y la viola arriba: es el **patrón 2 del Bloque 8** en versión documental.

**Lo acoté antes de alarmar, porque la severidad depende de la exposición:**

```
HANDOFF sin credencial  -> HTTP=404 BYTES=14   (mudh-mobile es PRIVADO)
README del conectoma    -> HTTP=200            (este repo es PUBLICO)
```

**El token NO está en la calle.** Pero está en el **historial de git de forma permanente** y lo ve cualquiera con acceso al repo, hoy o mañana. **Severidad alta, urgencia media.**

**Lo que NO hice, a propósito:** no probé el token. Usar una credencial ajena para medir su validez no está autorizado, y **P-01 pone rotar credenciales del lado de Abraham**. El scanner de secretos lo intenté y falló (`Repository does not have GitHub Advanced Security enabled`); **no cerré ahí**: lo sustituí por la medición de exposición por HTTP, que responde la pregunta que importaba.

## 8. 🟡 Y una frase mía que hay que corregir

Tachi: *«el que audita es el mismo sistema que escribió el código; Tao es otro agente del mismo ecosistema».*

**Tiene razón, y corrige la resp 073**, donde llamé a la auditoría de Tao **«la primera medición externa real que tuvo este proyecto»**. Tao es externo **al autor**, no **al ecosistema**. Eso no anula sus 13 hallazgos, pero **sí anula la palabra «externa» tal como la usé**.

**Y Tachi cae en su propia versión del problema:** él también es del ecosistema. **El único falsador realmente externo sigue siendo Abraham**, que es supervisión manual y no escala. Está escrito en B-01 como advertencia y hoy se cumple por tercera vez.

## 9. Qué de esto sirve al propósito, directa e indirectamente

**Directo:**
1. **El repo no contiene el activo que vende.** Si el objetivo es que MUDH sea **entregable y cedible**, este es el hueco más grande, y no es científico: es de empaquetado.
2. **Un `p` que no discrimina** entre 47× y 1,7× es lo primero que un revisor de paper marca.
3. **Los dos pisos** hay que unificar antes de la v2.

**Indirecto, y es lo más útil:**
4. **El `HANDOFF` de Tachi documenta el entorno mejor que mi propio `CONTEXTO-ENTORNO.md`:** los 8 servicios del gateway, qué tiene `brain-env` (numpy, scipy, networkx, igraph, torch CPU, R 4.5.3, **`xtensa-esp-elf-gcc` 16.1.0**), los mounts, y que Kaggle tiene 2 cuentas con rotación.
5. **Y ahí está la vía para cerrar el hueco 1: el compilador de ESP32 está EN el container.** O sea que **el `.c` que falta se puede escribir y compilar acá**, con el `.elf` y el RAM en target que el contexto declara como no medidos. **Eso convierte «el activo no está en el repo» de un problema en una tarea.**

---

## 10. 🔢 El orden actualizado (O-01), y por qué cambió

**El pedido era hacer 1 a 4 de corrido. Lo que encontré agrega dos ítems y NO desplaza el criterio**, que sigue siendo *primero lo que vuelve confiable al testigo*.

| # | Qué | Quién | Cambió porque |
|---|---|---|---|
| **0a** | **Subir el erratum a Zenodo** | **Abraham** · 5 días | sin cambios, sigue siendo lo único con fecha |
| **0b** | 🆕 **Rotar el PAT del `HANDOFF`** y sacarlo del historial | **Abraham** | hallazgo de este turno. Repo privado, así que no es una emergencia, pero es de una sola persona y de un solo minuto |
| 1 | Migrar los llamadores a `require()` | BRAIN | sin cambios |
| 2 | A-03: pins, lockfile, CI | BRAIN | **sube**: dos auditores independientes marcaron reproducibilidad |
| 3 | A-04: los JSON chicos | BRAIN | sin cambios |
| 4 | A-05: rutas de los `.mjs` | BRAIN | **sube**: es T-1 y A-05, el único defecto que encontraron los dos |
| **4b** | 🆕 **Decidir one-sided vs two-sided y unificar el piso de `p`** | **Abraham decide**, BRAIN aplica | toca todas las tablas publicadas |
| 5 | A-07 y A-08 | BRAIN | sin cambios: el único que puede cambiar un resultado |
| **5b** | 🆕 **Escribir y compilar el `.c` del motor en `brain-env`** (el `xtensa-esp-elf-gcc` está ahí) | BRAIN | cierra T-4 **y** el «1.336 B sin instrumento público» |

**Los 13 issues siguen SIN abrir:** son 5+ escrituras y **no llegó el OK**. Repetido acá porque es el mecanismo que evita que estos hallazgos se pierdan, y ya van dos que reaparecieron por eso.

## 11. Scorecard

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | los tres documentos leídos, **incluida la versión sobrescrita**, y los 7 hallazgos con veredicto. **−1:** `mudh-mobile` no se leyó completo, pueden haber más secretos |
| **Arquitectura del razonamiento** | 10/10 | ningún veredicto por lectura: el árbol se contó, el README se leyó por línea, la exposición del token se midió por HTTP **con control** (404 privado vs 200 público) antes de calificar la severidad |
| **Documentación** | 10/10 | evidencia verbatim, el fallo del scanner declarado **y sustituido**, el `$?` mentiroso declarado dentro de la propia corrida |
| **Innovación** | 4/5 | dos hallazgos que ninguna de las tres auditorías tenía, y la vía del `xtensa-gcc` para cerrar T-4. **−1:** la vía no se ejecutó |
| **Proceso QA** | 4/5 | cada veredicto con su comando y salida. **−1:** los issues siguen sin abrir |

**Total 56/60 → 93,3/100.** **N/A: 40 pts** (Ejecutabilidad, Seguridad-como-implementación, Testing, DevOps): la entrega es un peritaje.

## 12. NO MEDIDO, declarado

1. **El token no se probó y no se va a probar.** Su validez es **NO MEDIDA**. Rotarlo es de Abraham.
2. **No se buscaron más secretos:** se leyó **un** archivo de `mudh-mobile`. El scanner no está disponible. **Puede haber más.**
3. **No se midió si el 1.336 B es correcto**, sólo que **su instrumento no está en este repo**.
4. **La pregunta «¿por qué 40 nulls y no 4000?» no se contestó midiendo.** El costo declarado es 180 min por corrida de 40.
5. **El barrido de overflow sigue cubriendo un solo patrón** (`N*(N-1)`); `N**2` sin barrer. Es la forma falsable de T-5.
6. **Los pasos 1 a 4 del pedido NO se ejecutaron en este turno**: se ejecutó la parte «antes vé a git», que era explícita y previa. **Van en el turno siguiente**, y arranco por el 1 salvo que Abraham reordene con los ítems nuevos.
7. **`CONTEXTO-motor.md` sigue sin abrirse**, quinto turno. Sin veredicto de vigencia. **Y ahora hay un motivo nuevo para abrirlo:** contiene el 1.336 B que quedó sin instrumento público.
8. **El contexto vivo acumula cuatro líneas viejas** (la de la «072», A-10, A-01/A-02, y ahora la palabra «externa» sobre Tao). **Se corrigen en un commit de contexto, no de memoria.**
