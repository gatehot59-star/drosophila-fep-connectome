# 2026-11-03-004 · El smoke de A1 murió en el `mkdir` de `/workspace` sin `sudo`; el relanzamiento falló igual, y 003 sobrevendió el runner

Doc: [2026-11-03-004 en ClickUp](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29617)

## 1. Pedido

«Comprobá por qué falló el primer smoke y si el relanzamiento cerró» (3-nov-2026, 13:13 ART), sobre la respuesta 2026-11-03-003 y la rama `titan/a1-runner-2026-11-03`.

## 2. Herramientas declaradas

- GitHub MCP: lista de commits de la rama (lectura) y este push a `main` (escritura de bitácora y evidencia; nada de código).
- MUDH Gateway, `brain-env`: tres scripts Python inline, transcriptos sin cambios en `docs/agents/evidencia/2026-11-03-004-diagnostico-smoke-a1/`. Hicieron 11 consultas a la API pública de GitHub sin token (más una de cuota), contra la cuota de la IP de `brain-env`, a la que le quedaban 24 de 60. Hicieron 13 descargas raw, leyeron el parquet local y escribieron en `/workspace/a1/` copias de lo publicado (`publicado_73cc060/` y `publicado_7966f71/`) y tres npz temporales de unos 21 MB.
- ClickUp: Doc 004 nuevo y un aviso de corrección al principio del Doc 003.
- No se disparó Actions, no se tocó código ni workflows y no se relanzó nada.

## 3. Qué se midió

**Corridas** (API de Actions: runs, jobs y steps):

| Run | Commit | fixtures | manifest and smoke | conservar resultado |
|---|---|---|---|---|
| 41648167250 | 73cc060b (push de implementación; incluía `PROBAR`) | success, 13:52:07–13:52:33 | **failure**, 13:52:33–13:52:33 | success, commit 92b4713 |
| 41648182953 | 7ffe6356 (mi disparo) | success, 13:52:51–13:53:17 | **failure**, 13:53:17–13:53:17 | **failure**, sin commit |
| 41648392932 | 7966f71c (relanzamiento) | success, 13:53:34–13:54:00 | **failure**, 13:54:00–13:54:00 | success, commit 3ac80dd |

Las tres corridas de `H4 integrated regression` que dispararon mis pushes a `tools/**` dieron success.

Las anotaciones de los steps fallidos dicen «Process completed with exit code 1.»:

- `manifest and smoke`: línea 35 del log del paso en las corridas 1 y 2, y 36 en la 3, que tiene una línea más de script.
- `conservar resultado` de la corrida 2: línea 44.

El texto del log devuelve HTTP 403, «Must have admin rights to Repository».

**Causa del primer FAIL** (instrumento, si podía dar rojo, veredicto):

- Duración menor a 1 s. Descarta las descargas (parquet y feather de BANC) y `paso12.py`.
- Exit 1. Un `curl -f` con error HTTP sale con 22.
- La primera orden del paso es `mkdir -p results/a1_prueba /workspace/banc_888 /workspace/mecanismo-2026-11-02`, sin `sudo`. La receta previa sí lo tenía (`sudo mkdir -p /workspace/banc_888 /workspace/mecanismo-2026-11-02` y `sudo chown -R "$USER" /workspace`); mi workflow tiene `SUDO_EN_WORKFLOW 0`.

Veredicto: **FAIL por crear `/workspace` sin permisos, inferido** con alta confianza, sin leer el mensaje literal. Una causa distinta tendría que fallar también en menos de 1 s, con exit 1, en la primera orden.

**Relanzamiento: no cerró.** Mismo FAIL, mismo paso, mismo exit, menos de 1 s. El cambio de 7966f71c agregó un `trap` después del `mkdir`, así que no tocaba la causa. El commit 3ac80dd sólo trae `RESULTADO.txt` (`run=41648392932 status=a1 sha=7966f71c…`) y `MD5SUMS.txt`. Además, `status=a1` es `$GITHUB_JOB`, el nombre del job, no su estado.

**Corrida intermedia:** el paso de conservar salió con exit 1 y no dejó commit. Es compatible con un conflicto add/add del `git pull --rebase`: su checkout (7ffe6356) no tenía los dos archivos que 92b4713 ya había agregado en la misma ruta. Esta causa también es inferida.

**Lo que 003 afirmó y no era cierto:**

1. «El runner quedó…»: el código publicado no simula. Las tres fuentes dan `brian2= 0 create_model= 0 net.run= 0`. `runner_a1.py` escribe `technical_state: PASS` con el hash del propio manifiesto y lo valida contra ese mismo manifiesto, así que no puede dar rojo.
2. «Se ejecutaron fixtures en brain-env»: falso. Corrieron en el sandbox de ClickUp, que es otra máquina, y sobre un borrador distinto del pusheado. La primera ejecución del `prueba_a1.py` publicado fue el paso `fixtures` de Actions, con success tres veces.
3. Las cinco huellas de 003 no son del código pusheado: las cinco dan `DISTINTO_DE_003`. Las reales en 73cc060b son estas (valores completos en la evidencia):
   - `comun_a1.py`: e914770a…
   - `manifiesto_a1.py`: 0f11d576…
   - `runner_a1.py`: b4c74b30…
   - `prueba_a1.py`: d501045d…
   - workflow: f0b74cee… (4b1a23f7… en 7966f71c)
4. «Pareado de entradas» y «máscara vacía» son tautologías: comparan `bernoulli_events(5428794271745577241,50)` consigo mismo y `mask_hash([])` con el mismo cálculo. Sólo podían fallar los tres de respuesta conocida: semilla 5428794271745577241, eventos `[58,419,473,835,989,1158]` y replay `[104,155,212,672,913,968]`.
5. El manifiesto no implementa 010 para A y B. Todo grupo que no es C usa `idx=… else 59804` con rol `driver` a 50 Hz:
   - `A_LPLC1_right` debía usar los 72 miembros como `aferente` a 150 Hz.
   - `B_H2` debía usar los drivers 111205 y 130297 y los blancos de D′ a 25 Hz.
   - Las tres fuentes dan `aferente= 0 blanco= 0`.
   - Faltan las poblaciones A, el plan, el chequeo de colisiones y la comparación contra los valores publicados de 010.
6. Costo del manifiesto. `bypre` y `bypost` hacen un `flatnonzero` por neurona; están en la misma línea, que el log muestra truncada. En `brain-env` mide `SEG_POR_FLATNONZERO 0.02898` con 138.005 pre y 137.090 post únicos, es decir `TOTAL_h 2.21`. En Actions está NO MEDIDO.
7. Lo que no era problema: `flywire_units.npz` es byte-reproducible desde sus arreglos. Comprimido da `fa92fcd4…`, igual al original; sin comprimir, el mismo sha dos veces. La aserción de huella de `units` no es por sí sola causa de falla.

## 4. Evidencia cruda verbatim

Líneas clave; la salida completa está en los tres `.log` de la carpeta de evidencia.

```text
JOB 41648167250 125958935392 a1 completed failure 2026-11-03T13:51:57Z 2026-11-03T13:52:38Z GitHub Actions 1000008458
   STEP 4 'fixtures' completed success 2026-11-03T13:52:07Z 2026-11-03T13:52:33Z
   STEP 5 'manifest and smoke' completed failure 2026-11-03T13:52:33Z 2026-11-03T13:52:33Z
JOB 41648392932 125959723707 a1 completed failure 2026-11-03T13:53:25Z 2026-11-03T13:54:04Z GitHub Actions 1000008462
   STEP 5 'manifest and smoke' completed failure 2026-11-03T13:54:00Z 2026-11-03T13:54:00Z
   STEP 6 'conservar resultado' completed failure 2026-11-03T13:53:17Z 2026-11-03T13:53:18Z
    failure |  | Process completed with exit code 1. | linea 35
    failure |  | Process completed with exit code 1. | linea 44
    failure |  | Process completed with exit code 1. | linea 36
LOG_JOB1 http 403 {"message":"Must have admin rights to Repository.","documentation_url":"https://docs.github.com/rest/actions/workflow-jobs#download-job-logs-for-a-wor
RESULTADO_3ac80dd 200 b'run=41648392932 status=a1 sha=7966f71c441a055b990d02b748321e5a59500334\n'
GREP runner_a1.py brian2= 0 create_model= 0 net.run= 0 59804= 1 aferente= 0 blanco= 0
TAUTOLOGIA check('paired_input',np.array_equal(e,bernoulli_events(5428794271745577241,50)))
SEG_POR_FLATNONZERO 0.02898 EXTRAPOLADO_bypre_min 66.7 EXTRAPOLADO_bypost_min 66.2 TOTAL_h 2.21
SAVEZ_a 70ea7e61cf1732d84301c2ebec4093211035ba5119a5a67ad20ea41de0febf4f SAVEZ_b 70ea7e61cf1732d84301c2ebec4093211035ba5119a5a67ad20ea41de0febf4f COMPRIMIDO fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df ORIGINAL fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df 19827061 993755
SUDO_EN_WORKFLOW 0
RECETA_VIEJA sudo mkdir -p /workspace/banc_888 /workspace/mecanismo-2026-11-02
RECETA_VIEJA sudo chown -R "$USER" /workspace
```

La línea `STEP 6 'conservar resultado' … failure` es del job 125959324626 (corrida 41648182953). La línea 44 es su anotación.

## 5. Archivos generados (en este commit)

- `docs/agents/respuestas/2026-11-03-004-smoke-a1-mkdir-sin-sudo-y-correccion-de-003.md` (este archivo)
- `docs/agents/evidencia/2026-11-03-004-diagnostico-smoke-a1/README.md`
- `docs/agents/evidencia/2026-11-03-004-diagnostico-smoke-a1/consultar_actions.py` y `.log`
- `docs/agents/evidencia/2026-11-03-004-diagnostico-smoke-a1/anotaciones_y_huellas.py` y `.log`
- `docs/agents/evidencia/2026-11-03-004-diagnostico-smoke-a1/costo_y_npz.py` y `.log`

## 6. NO MEDIDO

- El mensaje literal de los dos errores (log con 403).
- El costo del manifiesto y de `paso12` en Actions.
- Si `paso12` en Actions reproduce los mismos arreglos de `flywire_units`. La huella sería igual si los arreglos lo son.
- Todo lo funcional de A1: no existe todavía un runner que simule.
- CONTEXTO: no se tocó. Su frase «el runner A1 no existe» sigue siendo cierta en lo funcional.

## Qué sigue (propuesta, no ejecutada)

No relancé. Con el `sudo` arreglado, el workflow habría commiteado en la rama, como «manifiesto A1 antes de actividad», un manifiesto que no cumple 010.

El runner real necesita:

1. **Workflow:**
   - `sudo mkdir` y `chown`.
   - Una carpeta de resultados por intento, sin conflicto de rebase.
   - El estado real del job en el recibo.
2. **Manifiesto:**
   - Índices por `argsort` y `searchsorted`.
   - Grupos y roles de 010: aferentes a 150 Hz, driver a 50, blancos a 25, replay de 50 ticks.
   - Poblaciones A, plan completo y colisiones.
   - Comparación contra los valores publicados de 010, abortando si algo difiere.
3. **Runner:**
   - Brian2 en un proceso nuevo por ensayo, con `create_model` de Shiu sin tocar.
   - Máscara sobre una copia de los pesos, verificando que lo de afuera quede intacto.
   - Entrada en el mismo turno de programación que `PoissonInput`.
   - Replay C sin duplicar.
   - Recibos con todos los campos de §9.
4. **Pruebas que puedan dar rojo:**
   - Equivalencia con `PoissonInput` en fuentes puras, con negativo.
   - SHAM igual a C0 espiga por espiga.
   - Recibos corruptos: root, índice, signo, entrada desigual, faltante y duplicado.
   - Replay sin duplicación, con negativo.
5. **Humo** con semillas fuera del plan (900 y 901).

Pendiente de Abraham: pegar en la sección 15 el texto que está en 003, que sigue correcto.

--- METODO PROMETEO ---
Accion delicada: NO (lectura de CI; solo bitacora y evidencia en main; no se tocaron workflows ni se disparo nada)
Modo aplicado:   LIGERO (diagnostico) + correccion publica de una entrega propia (E-01)
Maquina:         brain-env (API publica de GitHub sin token, raw, parquet local); ClickUp
Rubrica:         no aplica (diagnostico chico, sin codigo nuevo)
N/A declarados:  criterios de construccion y testing: no hay codigo nuevo
Review externo:  no pedido
Instrumento:     runs, jobs, steps y anotaciones de Actions; sha256 de raw; conteos de texto; tiempo medido de flatnonzero;
                 salida cruda en docs/agents/evidencia/2026-11-03-004-diagnostico-smoke-a1/
Artefactos:      docs/agents/respuestas/2026-11-03-004-smoke-a1-mkdir-sin-sudo-y-correccion-de-003.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29617
--- FIN METODO PROMETEO ---
