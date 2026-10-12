# 2026-10-12-009 · Tao no auditó: leyó el pedido, frenó a las 11:39 pidiendo «confirmo» y el depósito lo espera; el token de Zenodo, paso a paso

**Veredicto:** Tao no hizo la auditoría. Su única corrida de hoy (mención 11:36:56, respuesta 11:39:43) leyó el alcance, confirmó el HEAD `47d940e` del conectoma y frenó a pedir «confirmo» para un lote de 7 escrituras, por su regla de cinco o más. No hay rama, archivo, PR ni Doc suyos. Sin auditoría no hay contra qué revisar el PR #27: no toqué nada de la v2 y el borrador de Zenodo espera, como pidió Abraham. La página del token existe (verificada hoy), en brain-env no hay token y los dos PDF del depósito siguen con su md5.

- **Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-21477
- **Tarea de Tao:** https://app.clickup.com/t/86e3p74xa · **su respuesta:** https://app.clickup.com/t/86e3p74xa?comment=90170261436691
- **PR de la v2:** https://github.com/gatehot59-star/drosophila-fep-connectome/pull/27 (sin cambios)

## 1. Pedido

> «taou con sumo ma de 1000 crediros me imagino que ya hiso el trabajo sino en que lo consumio. dame los link y paso a seguir para generA ELTOKEN DE ZENODO ANTES REVISA TODO CON LA AUDITORIA DE TAO» (Abraham, 2026-10-12, 11:48)

Tres partes: (a) si Tao hizo el trabajo y, si no, en qué gastó los créditos; (b) revisar todo con su auditoría antes del token; (c) links y pasos para el token de Zenodo.

## 2. Herramientas y máquina

- **ClickUp, lectura:**
  - la tarea https://app.clickup.com/t/86e3p74xa con el hilo completo;
  - la actividad de TITÁN Tao del 1 al 12-oct en todo el workspace (dos consultas, porque el máximo por consulta es 7 días);
  - todo lo creado en el workspace desde 2026-10-12T14:30Z (documentos, comentarios, tareas y mensajes);
  - la configuración del agente;
  - el Help Center sobre créditos.
- **GitHub, lectura:** ramas del conectoma (36 contando `main`), PRs del conectoma y de `mudh-mobile` ordenados por actualización, y los últimos 5 commits de `main`.
- **brain-env, una llamada de python, sin escribir:** rutas de Zenodo sin seguir redirecciones (con una ruta inventada como control), presencia del token, md5 de los PDF del depósito y HEAD del clon de verificación.
- **Web:** developers.zenodo.org.
- **Escrituras:** este archivo y el CONTEXTO en `main`; el Doc https://app.clickup.com/90171457413/docs/2kza6fw5-21477; el estado de Tao en el Doc de la 007 (https://app.clickup.com/90171457413/docs/2kza6fw5-21437). No le escribí a Tao, no disparé ningún Super Agent y no toqué Zenodo.

## 3. Qué se midió

| Afirmación | Instrumento | ¿Podía dar rojo? | Resultado |
|---|---|---|---|
| Tao corrió con la mención | hilo de la tarea; actividad del workspace | sí: sin respuesta o cero filas | **sí**, una respuesta a las 11:39:43 |
| Tao auditó | ramas y PRs de los dos repos; búsqueda en ClickUp desde 14:30Z | sí: la rama, el PR o el Doc existirían | **no**: ni `titan/auditoria-tao-laboratorio-2026-10-12`, ni PR, ni Doc |
| Por qué frenó | su respuesta y sus instrucciones | sí | pide «confirmo» para 7 escrituras; su regla pregunta todo lote de 5 o más |
| El HEAD que cita era el de ese momento | commits de `main` | sí | **CONFIRMADO**: `47d940e` (14:35:41Z) era HEAD a las 14:39:43Z; `b8eac1c` entró a las 14:42:05Z |
| Cuántos créditos gastó | ninguno accesible a BRAIN | no | **NO MEDIDO** |
| La página del token existe | HTTP sin redirección, con una ruta inventada como control | sí: la inventada dio 404 | **existe**: 302 al login |
| No hay token en brain-env | variable de entorno y archivo | sí | **ausente** en los dos |
| Los PDF del depósito siguen | md5 contra `docs/v2/archivos-deposito-v2.0.json` del PR #27 | sí | **2/2 iguales** |

### Tao, en detalle

- Su respuesta (https://app.clickup.com/t/86e3p74xa?comment=90170261436691) dice: «Leí el alcance y confirmé el conectoma en 47d940e. Todavía no audité los logs ni emití conclusiones.»
- Lista los 7 objetos:
  1. la rama `titan/auditoria-tao-laboratorio-2026-10-12`;
  2. el archivo `docs/auditorias/2026-10-12-tao-auditoria-del-laboratorio.md`;
  3. el PR con review automático;
  4. el Doc en el Space;
  5. una rama en `mudh-mobile`;
  6. su carta `docs/agents/AGENT-TAO.md` (citada en `a898090`);
  7. el PR de esa carta.
- Cierra: «¿Confirmás el lote? Mencioname con «confirmo» y continúo. No modificaré instrumentos, resultados ni archivos del laboratorio.»
- La regla que lo frenó, de sus instrucciones: «preguntás, y no es negociable, cuando [...] (2) el lote es de 5 o más escrituras, porque un pedido detallado es el plan y no la confirmación». El pedido de la 007 pedía exactamente esos 7 objetos, así que cualquier auditoría con entrega en git y Doc le pide una vuelta más.
- Actividad del 1 al 12-oct: dos comentarios en total, el del 3-oct a las 16:39 en «Auditar integralmente la viabilidad de DBC3-live» (https://app.clickup.com/t/86e3jk397) y el de hoy. Los PR #108 y #109 de `mudh-mobile` son del 3-oct.

### En qué se fueron los créditos

- BRAIN no puede leer el contador: **NO MEDIDO**.
- Lo único visible es esa corrida: leer la tarea (el pedido es largo), su conocimiento y su carta, consultar GitHub y escribir la respuesta.
- Help Center, «How are AI Credits consumed?» (https://help.clickup.com/hc/en-us/articles/37837088720151-How-are-AI-Credits-consumed): cada corrida de un Super Agent consume créditos aunque sólo conteste; el estimado es de 100 a 300 por uso y sube con la cantidad de acciones.
- El número exacto está en el perfil de Tao → **Credits** (costo de la última corrida, corridas y costo del mes) y en Settings → AI Usage → Activity, corrida por corrida («Track your Workspace's Brain AI usage», https://help.clickup.com/hc/en-us/articles/34741383911959-Track-your-Workspace-s-Brain-AI-usage).
- Brain no consume créditos de IA («ClickUp Brain AI feature availability and limits», https://help.clickup.com/hc/en-us/articles/20686299081879-ClickUp-Brain-AI-feature-availability-and-limits).

### Zenodo, verbatim de developers.zenodo.org

- «Register for a Zenodo account if you don't already have one. Go to your Applications, to create a new token. Select the OAuth scopes you need (for the quick start tutorial you need `deposit:write` and `deposit:actions`).»
- `deposit:write`: «Grants write access to depositions, but does not allow publishing the upload.»
- `deposit:actions`: «Grants access to publish, edit and discard edits for depositions.»

### La 008

El mensaje «no veo tus respuestas» que cita la 008 existe: es un mensaje de Abraham entre el de las 11:34 y la respuesta 008. El minuto exacto (11:44) no lo medí. No hay nada que corregir en la 008.

## 4. Evidencia cruda

brain-env, `python`, exit=0 (stderr: sólo un DeprecationWarning de `datetime.utcnow`):

```
UTC 2026-10-12T14:56:19.112884
URL https://zenodo.org/account/settings/applications/tokens/new/ STATUS 302 LOC /login/?next=%2Faccount%2Fsettings%2Fapplications%2Ftokens%2Fnew%2F
URL https://zenodo.org/account/settings/applications/ STATUS 302 LOC /login/?next=%2Faccount%2Fsettings%2Fapplications%2F
URL https://zenodo.org/account/settings/zz-no-existe-zz/ STATUS 404 LOC None
URL https://zenodo.org/api/deposit/depositions/19136948 STATUS 403 LOC None
URL https://zenodo.org/api/records/19136948 STATUS 200 LOC None
ENV ZENODO_TOKEN presente: False
ARCHIVO /workspace/.zenodo_token existe: False
PDF Mendieta2026_Paper1_Erratum_v1.0.pdf 189046 28f7a21f97648c12faf90f2190f3ccbc
PDF Mendieta2026_Paper1_Erratum_v1.0.typ 46569 c29a91e7a4cee16790d90bb58d4a9626
PDF Mendieta2026_Paper1_v2.0.pdf 326535 50df4ab9c88add11282e70ef3668c7d0
PDF Mendieta2026_Paper1_v2.0.typ 63324 c0e240fd50f94b131e3a95f64f39ded7
CLON existe: True
554f7d99be81f27da331dc5e736b89c5e704e8c2 evidencia(v2): render determinista PASS y verificacion del deposito PASS, mas el plan de cierre

JSON md5 50a6a3adec0bde1feadc36b0141c24a4
```

Del JSON, verbatim: `"md5": "50df4ab9c88add11282e70ef3668c7d0"` (manuscrito, 326535 B) y `"md5": "28f7a21f97648c12faf90f2190f3ccbc"` (erratum, 189046 B).

GitHub:

- `drosophila-fep-connectome`: 36 ramas contando `main`; `main` en `e322621c36c38b3c789c98fab3f407efe0dacd28`; no figura `titan/auditoria-tao-laboratorio-2026-10-12`. PR más reciente: #27, `titan/v2-cierre-2026-10-12` en `554f7d99be81f27da331dc5e736b89c5e704e8c2`, abierto, creado 2026-10-12T14:28:10Z.
- `mudh-mobile`: PR más reciente #109, `titan/tao-auditoria-dbc3-2026-10-03`, creado 2026-10-03T19:38:51Z.
- Commits de `main`: `47d940e` 2026-10-12T14:35:41Z; `b8eac1c` 14:42:05Z; `e322621` 14:46:15Z.

ClickUp:

- Hilo de la tarea: comentario de Abraham `90170261435881`, timestamp 1791815816086 (14:36:56Z) → respuesta de TITÁN Tao `90170261436691`, timestamp 1791815983433 (14:39:43Z). Tarea en «bandeja», sin asignados y sin adjuntos.
- Actividad de Tao, 2026-10-05T15:00Z a 2026-10-12T15:00Z: «Total Activity Rows Retrieved: 1» (2026-10-12T14:39:43.433Z, comment posted).
- Actividad de Tao, 2026-10-01T03:00Z a 2026-10-05T15:00Z: «Total Activity Rows Retrieved: 1» (2026-10-03T19:39:23.237Z, comment posted).
- Creado desde 2026-10-12T14:30Z: 11 resultados (3 documentos, 2 comentarios, 1 tarea y 5 mensajes); el único de Tao es su respuesta.

## 5. Token de Zenodo, paso a paso

1. Entrar a Zenodo con la cuenta dueña del registro 10.5281/zenodo.19136948: https://zenodo.org/login/
2. Abrir https://zenodo.org/account/settings/applications/tokens/new/ (Applications → Personal access tokens → New token).
3. Nombre `paper1-v2-brain`; tildar **deposit:write** y **deposit:actions**; Create.
4. Copiar el token: Zenodo lo muestra una sola vez.
5. Cuando la auditoría de Tao esté cotejada, Abraham lo pasa en un mensaje. BRAIN lo guarda en brain-env en `/workspace/.zenodo_token` con permisos 600 y no lo imprime.
6. BRAIN corre `tools/zenodo/depositar_v2.py --borrador` desde el clon del PR #27: crea la versión nueva **en borrador**, sube los dos PDF verificando md5 y carga los metadatos. No publica. Devuelve el link del borrador.
7. Abraham revisa el borrador y publica (irreversible: el DOI queda), o da el sí para `--publicar`.
8. Revocar el token en la misma página.

El merge del PR #27 es de Abraham. Conviene antes de publicar, para que `main` tenga la fuente de lo publicado.

## 6. Qué espera la decisión de Abraham

- **El «confirmo» a Tao.** Con el sí, BRAIN publica en el hilo, con la mención: «confirmo el lote de 7. Empezá por el bloque 1 (v2.0, PR #27), que es lo único que frena el depósito en Zenodo, y después seguí con el resto.» Gasta créditos de Tao.
- **La alternativa sin Tao:** una instancia nueva de Brain, sin el contexto de esta conversación, audita el bloque 1 contra el repo.
- Después: cotejar la auditoría contra el repo (no contra su Doc), corregir lo que caiga en el PR #27, y recién ahí el merge, el token, el borrador y la publicación.

## 7. Archivos

- `docs/agents/respuestas/2026-10-12-009-tao-no-audito-pidio-confirmo-y-el-deposito-lo-espera.md` (este archivo).
- `docs/agents/CONTEXTO-drosophila-fep.md`, reescrito: estado de Tao, orden del depósito, la 008 y la 009.

## 8. NO MEDIDO

- Los créditos que gastó Tao, por corrida y en el mes, y si al workspace le quedan para la auditoría completa.
- Corridas de Tao que no dejan rastro en tareas ni comentarios (por ejemplo, DMs con él).
- La auditoría de Tao: no existe, así que la revisión del PR #27 contra ella no se hizo. Nada de la v2 cambió.
- La página del token por dentro: sólo que la ruta existe y pide login.
- El borrador, el depósito y la publicación.
- La hora exacta del mensaje «no veo tus respuestas» que cita la 008.

## Antes de firmar

```
"Tao no auditó"                → ramas, PRs y búsqueda en ClickUp   → SÍ podia dar rojo → medido: no hay rama, PR ni Doc
"Tao corrió una vez hoy"       → actividad del workspace            → SÍ (cero filas)   → medido: 1 fila, 14:39:43Z
"el HEAD que cita era el real" → commits de main                    → SÍ                → medido: 47d940e era HEAD
"la página del token existe"   → HTTP sin redirección + ruta falsa  → SÍ (la falsa 404) → medido: 302 al login
"no hay token en brain-env"    → variable y archivo                 → SÍ                → medido: ausente
"los PDF del depósito siguen"  → md5 contra el JSON del PR #27      → SÍ                → medido: 2/2 iguales
"Tao gastó N créditos en X"    → ninguno accesible                  → NO                → NO MEDIDO
"la v2 resiste la auditoría"   → no hay auditoría                   → NO                → NO MEDIDO
```

## QA

Reporte: aplican Completitud (15), Arquitectura del razonamiento (10), Documentación (10), Innovación (5) y Proceso QA (5). Ejecutabilidad, Seguridad, Testing y DevOps son N/A (55 puntos fuera del denominador): no hay código ni infraestructura nueva.

| Criterio | Puntos | Evidencia |
|---|---|---|
| Completitud | 12/15 | (a) y (c) completas; (b) imposible sin auditoría, declarada en §8 |
| Arquitectura del razonamiento | 9/10 | cada afirmación con un instrumento que podía dar rojo (§3 y Antes de firmar) |
| Documentación | 9/10 | seis campos, evidencia verbatim, Doc con el mismo contenido |
| Innovación | 3/5 | priorizar el bloque 1 para destrabar el depósito; alternativa sin créditos de Super Agent |
| Proceso QA | 5/5 | control negativo de la ruta de Zenodo (404); HEAD citado por Tao cruzado con los commits |
| **Total** | **38/45 = 84/100** | **debajo del umbral de 90**: lo que falta es que Tao corra, no reescribir |

--- METODO PROMETEO ---
Acción delicada: NO (lecturas; bitácora y contexto a main; Doc)
Máquina: brain-env (una llamada de python: rutas de Zenodo, token, md5 de los PDF); ClickUp y GitHub (lecturas); web (developers.zenodo.org)
Artefactos: docs/agents/respuestas/2026-10-12-009-tao-no-audito-pidio-confirmo-y-el-deposito-lo-espera.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21477
