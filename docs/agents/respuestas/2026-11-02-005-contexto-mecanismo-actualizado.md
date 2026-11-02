# 2026-11-02-005 · CONTEXTO al día con H_MECANISMO: parche anclado por flujo documental, resultado igual al preflight byte por byte

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29337
Rama: titan/contexto-mecanismo-2026-11-02, sin merge.
Run: 41473756266 (completed/success). Commit en main: efa868ca2df8ce1d81c59a0c72287a981752700c, padre 7fecfe1.

## 1. Pedido

Cerrar lo que la 003 dejó dicho («CONTEXTO-drosophila-fep.md sigue sin actualizar; se actualiza con la lectura del veredicto») y que la 004 declaró pendiente, dentro del «sigue» del 2-nov-2026, 12:05 ART.

## 2. Herramientas declaradas

- GitHub MCP: rama titan/contexto-mecanismo-2026-11-02 desde main 7fecfe1; commit dbf495e con el script de parche y el workflow, sin disparar; commit eaf67cf con el CORRER que fija base y resultado; este archivo en main.
- brain-env (MUDH gateway, python): bajé el script publicado y lo corrí en copia (preflight y cuatro negativos); después leí main.
- Actions: el flujo documental (run 41473756266). Además, el workflow existente «H4 integrated regression», que corre en cada push, se disparó solo dos veces (runs 41473679122 y 41473756337).
- Escritura en main: un solo archivo, CONTEXTO, por el bot, con push normal y sin force.

## 3. Qué se midió

- «El parche toca solo lo previsto» → preflight sobre main 7fecfe1 (CONTEXTO sha256 ea44b0ba…, 128.279 bytes) → sí podía dar rojo: cuenta las anclas y fija base y resultado → cuatro anclas con una aparición cada una; 8 líneas de diff (2 reescritas y 4 agregadas); prefijo y cola idénticos; resultado 64b5f6f3…, 131.355 bytes.
- «El script rechaza entradas malas» → cuatro negativos en copia → sí → base distinta, exit 2; resultado distinto, exit 4; ancla repetida, exit 3; ancla ausente, exit 3.
- «main quedó como el preflight» → lectura de main después del run, por la API y por raw → sí → efa868c, padre 7fecfe1, autor github-actions[bot], un solo archivo cambiado; CONTEXTO 64b5f6f3…, igual byte a byte al preflight. La respuesta 004 quedó intacta (ac5bbb46…).

Qué dice ahora el CONTEXTO: la última actualización y el estado canónico nombran la 2026-11-02-004 y la rama titan/mecanismo-2026-11-02, y la sección «1-nov-2026 · Topo inverso corregido» suma cuatro líneas: H_MECANISMO MIXTA en el modelo, qué enciende al freno (post hoc), las corridas 1 y 2, y lo pendiente NO MEDIDO.

## 4. Evidencia cruda

Preflight en brain-env, con el script bajado del commit dbf495e (sha256 a94ce9665b6d5a6e3f57e1e03d9f01d776ade5bbf8db0c9c0f81d53c0958fa9d, 5.330 bytes):

```text
PREFLIGHT 0 BASE_SHA256 ea44b0bae4845bfeccfc9b09793f15465503da2a938c34f0d7a8d259b083b7ed bytes 128279 | ANCLA 0 apariciones 1 | ANCLA 1 apariciones 1 | ANCLA 2 apariciones 1 | ANCLA 3 apariciones 1 | RESULTADO_SHA256 64b5f6f38c3c6e1d9854ac884e1eb5e5f1c5223a6213a03913de4a7d0f85e3f3 bytes 131355
NEG base_distinta 2
NEG resultado_distinto 4
NEG ancla_repetida 3
NEG ancla_ausente 3
lineas_cambiadas 8
solo_prefijo_y_cola True True
```

CORRER (commit eaf67cf):

```text
BASE ea44b0bae4845bfeccfc9b09793f15465503da2a938c34f0d7a8d259b083b7ed
RESULTADO 64b5f6f38c3c6e1d9854ac884e1eb5e5f1c5223a6213a03913de4a7d0f85e3f3
```

Lectura de main después del run:

```text
MAIN efa868ca2df8ce1d81c59a0c72287a981752700c padres ['7fecfe1'] autor github-actions[bot] archivos ['docs/agents/CONTEXTO-drosophila-fep.md'] msg contexto(topo-inverso): H_MECANISMO MIXTA en el modelo, respuesta 2026-11-02-004
CONTEXTO 131355 64b5f6f38c3c6e1d9854ac884e1eb5e5f1c5223a6213a03913de4a7d0f85e3f3 igual_al_preflight True
RUN 41473756266 completed success eaf67cf .github/workflows/contexto-mecanismo-2026-11-02.yml
respuesta_004_intacta ac5bbb46d494a8ce
```

## 5. Archivos generados

- titan/contexto-mecanismo-2026-11-02: tools/contexto/parche_contexto_mecanismo.py (a94ce966…, 5.330 bytes), .github/workflows/contexto-mecanismo-2026-11-02.yml (6ade060b776b380f5046d5a182f74993f809a51a08f7b7c41b8bd08e089c9997, 1.605 bytes) y tools/contexto/CORRER-mecanismo-2026-11-02.
- main: docs/agents/CONTEXTO-drosophila-fep.md, escrito por el bot en efa868c, y este archivo.

## 6. NO MEDIDO

- El log del job documental: no lo leí porque bajarlo pide autenticación. El veredicto sale del estado estructurado del run y de los bytes de main.
- Los dos runs de «H4 integrated regression» que dispararon estos pushes: el de dbf495e dio success; el de eaf67cf estaba en curso cuando cerré.
- El resto del CONTEXTO no se revisó: solo se agregaron las líneas del mecanismo.

--- METODO PROMETEO ---
Accion delicada: SI. Workflow que escribe en main un solo archivo, sin force, con base y resultado fijados por sha256.
Modo aplicado: FULL.
Maquina: brain-env (preflight y lectura), Actions ubuntu-24.04 (parche).
Instrumento con capacidad de dar rojo: script con anclas contadas y dos sha256; cuatro negativos dieron el exit esperado.
NO MEDIDO declarado: log del job y resultado del segundo run de H4.
Review externo: no
