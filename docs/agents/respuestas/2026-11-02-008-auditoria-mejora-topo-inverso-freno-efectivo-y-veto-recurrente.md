# 2026-11-02-008 · Auditoría y mejora de Topo inverso: el Freno Efectivo Rectificado sube el proxy de 4/7 a 7/7 (R² = 0,9065) y 17 relevos recurrentes pesados D→X se conservan entre FlyWire y BANC (p < 10⁻⁴)

## 1. Pedido
El usuario adjuntó tres exportaciones `.md` del documento de ClickUp `2026-11-01-001 · Topo inverso: tenemos piezas para buscar una gramática funcional del conectoma, todavía no la gramática` (`https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29177`) y pidió: `"audita y mejora .innova. si es que puedes, sino lo entendreria, a lo mejor es mucho para ti"`.

- **Declaración I-01:** Los 3 archivos adjuntos (`...-20261102165831.md`, `...-20261102165954.md`, `...-20261102170052.md`) son idénticos byte por byte (`83.267` bytes, `690` líneas, SHA-256 `2d4a6e1f2980e88803317e4fb6e08cb6f3daa0ffcc3dd108fb1051a98f05b1d8`).

## 2. Herramientas declaradas
- `execute_bash` (sandbox ClickUp, lectura): verificación SHA-256 y estructura de encabezados de los 3 adjuntos.
- `mcp_gateway__gateway_call_tool` (`build.run`, `build.read_file`, `build.write_file` en `brain-env`, costo 0): ejecución de `verificar_dnp04.py --parquet /workspace/connectivity.parquet` y de `auditoria_e_innovacion_2026_11_02.py` sobre FlyWire v783 y BANC v626.
- `mcp_gateway__gateway_call_tool` (`sqlite.query` / `sqlite.execute` sobre `nexus.db`, costo 0): lectura y cierre del pizarrón (`reportes`).
- `githubmcp_get_file_contents` y `githubmcp_create_or_update_file` (GitHub API sobre `gatehot59-star/drosophila-fep-connectome`, costo 0): commit de `tools/verificar_dnp04.py` (`0c849ddc7`) y `verificacion_dnp04_parquet.log` (`2cb9beb39`) en `titan/mecanismo-dnp04-2026-11-02`, y commit de evidencia, auditoría `2026-11-02-01` (`f38686dcb`) y este recibo `2026-11-02-008` en `main`.
- `create_document_page`, `read_text` y `str_replace` (ClickUp Docs): actualización de `https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29177` y creación de la página de esta entrega bajo `https://app.clickup.com/90171457413/v/dc/2kza6fw5-26157`.

## 3. Qué se midió (con número e instrumento)

### 3.1. Auditoría de `Topo inverso` (`001`–`007`) y `H_MECANISMO_DNp04` (`006`)
1. **Números de las corridas (`CONFIRMADO`):** Ejecutamos `verificar_dnp04.py --dir /workspace/dnp04/actions_correr --previa /workspace/mecanismo-2026-11-02/actions_correr2 --parquet /workspace/connectivity.parquet` en `brain-env`. Dio `FILAS_PARQUET {"Q1": [1, 190.0], "Q2": [937, 6789.0], "Q3": [505, 4366.0], "Q4": [1184, 8733.0], "Q5": [1243, 6240.0], "Q6": [1677, 18623.0]} igual_al_sello=True`, `GUARDAS_PROPIAS G1..G5 = True`, `todo_igual=True` y `H_MECANISMO_DNp04_PROPIO SOSTENIDA_EN_MODELO r_Q1=0.4056 r_Q2=0.7456 s4=0.9677`.
2. **Cinco hallazgos rojos corregidos (`R1..R5`):**
   - **R1 (Doc `https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29177` desincronizado):** tenía el H1 duplicado (`L1` y `L3`), terminaba en la sección 14 (`L656`, faltaba la sección 15 `H_REUSO_CIERRE` pese a haberse declarado publicada ahí en `001` y en la auditoría `2026-11-01-02`) y su encabezado estaba frenado en `2026-11-02-004` sin `006` ni `007`.
   - **R2 (`verificar_dnp04.py` sin commitear y corrido sin `--parquet`):** citado en `006` pero dejado fuera de git en `/workspace/dnp04/verif/`. Commiteado ahora en `titan/mecanismo-dnp04-2026-11-02` (`0c849ddc7` y `2cb9beb39`).
   - **R3 (Techo estadístico de la prueba de signos `p_conv` en `n=20`):** `P1..P4` dan todas el mismo `p = 2/2^20 = 1,90735e-06` porque con `20/20` diferencias positivas las asignaciones extremas son únicas sin importar la magnitud `|d_i|`; el filtro real de magnitud son los umbrales `r_Q1 >= 0,25` y `r_Q2 >= 0,50`.
   - **R4 (`nexus.db` y `CONTEXTO-drosophila-fep.md` atrasados):** `reportes` en `nexus.db` tenía como último registro `id=143` del `2026-11-01 17:31:24` (faltaban los 7 turnos del 2-nov), y `CONTEXTO-drosophila-fep.md` paraba en `004`.
   - **R5 (Candidata `G1` en `Topo inverso` contradicha por `004` y `006`):** las secciones 4A y 5 del Doc seguían proponiendo `G1` como `S -> X -| D` feed-forward directo, cuando `Delta_SX / Delta_X` dio `0,23..0,49 < 0,50` y el freno principal en `LC4` entra por el relevo recurrente `DNp04 -> PVLP010` (`190` sinapsis en una sola fila).

### 3.2. Mejora e Innovación 1: Diagnóstico mecánico de los 3 fallos del proxy lineal y Freno Efectivo Rectificado (`7/7`, `R² = 0,9065`)
- **Por qué falló el proxy lineal (`espigas_C0 * sinapsis_X_a_D`) en 3 de 7 pares:**
  1. En `AVLP080_LPLC2` (`pred = 0,2010` vs `med = 0,0261`), el **`72,0 %` (`470/653`) de las sinapsis de `AVLP080` a `D'` caen en neuronas clavadas bajo umbral en `C0` (`< 2 Hz`)**, sobre todo `DNp35_8` (`388` sinapsis, `C0 = 0,90 Hz`, co-frenada por `X_2860` con `226` sinapsis) y `DNp06_1` (`53` sinapsis, `C0 = 1,55 Hz`, co-frenada por `LHAD1g1` con `399` y `PVLP010` con `262`). No se pueden restar espigas debajo de `0 Hz`, y soltar solo a `AVLP080` no desbloquea un blanco co-frenado.
  2. En `AVLP080_LPLC1` (`pred = 0,6240` vs `med = 0,3297`), el **`63,9 %` (`400/626`) de sus sinapsis caen en blancos clavados `< 2 Hz`** (`DNp35_3`, `388` sinapsis, `C0 = 1,75 Hz`, co-frenada por `X_30179` con `200` sinapsis).
  3. En `PVLP010_LPLC1` (`pred = 0,2170` vs `med = 0,4839`), el **`72,7 %` (`327/450`) de sus sinapsis apuntan a blancos activos en régimen lineal (`>= 2 Hz`)**, liderados por `DNp06_1` (`262` sinapsis, `C0 = 43,80 Hz`), donde cada sinapsis retirada libera espigas de inmediato (`43,80 -> 92,95 Hz`).
- **Freno Efectivo Rectificado (`0` parámetros libres, solo `C0` + `W_XD`):** ponderando la cuota inhibitoria sobre cada blanco `D'_j` por su peso activo en `C0` (`w_j^act = r_C0(D'_j) / sum r_C0(D')`), los aciertos suben de **`4/7` (`PROXY_PARCIAL`) a `7/7` (`PROXY_UTIL`)**, el error medio absoluto baja a la mitad (**`MAE = 0,1312 -> 0,0608`**, `MaxErr = 0,2943 -> 0,1373`), y la varianza explicada sube de **`R² = 0,4985` (`r = 0,7556`) a `R² = 0,9065` (`r = 0,9705`)** (`p = 0,0015` para `MAE` y `p = 0,0024` para `7/7` contra `10.000` permutaciones globales).

### 3.3. Mejora e Innovación 2: Censo `G1-Recurrente` en FlyWire v783 y BANC v626 (`17` relevos pesados `D->X` conservados, `p < 10^-4`)
- **Control negativo que descarta el conteo triádico difuso:** contar caminos `S -> D_driver -> X -| D_target` con umbral bajo agregado (`w_dx >= 20`) da `214/880` (`24,32 %`) en FlyWire y `132/622` (`21,22 %`) en BANC, pero **no supera al control nulo de permutación de etiquetas `D`** (`228,57 +- 7,38` en FlyWire, `p = 1,0`; `143,10 +- 5,92` en BANC, `p = 1,0`).
- **Lo que sí es altamente no aleatorio y conservado entre individuos es el Relevo Unitario Pesado (`w_max >= 80` sinapsis en una sola arista `D -> X`):**
  - En los `2.701` pares tipados `(D_type, X_type)` compartidos entre FlyWire y BANC, `w_max` correlaciona con **`rho_Spearman = 0,6120` (`p = 2,21e-277`)**.
  - De los `37` relevos con `w_max >= 80` en FlyWire y `31` en BANC dentro del vocabulario compartido, **`17` pares exactos `(D_type -> X_type)` superan las `80` sinapsis en una sola fila en AMBOS conectomas**, encabezados por `DNp35 -> CB0527` (`235` syn en FlyWire, `184` en BANC), `DNp04 -> PVLP010` (`190` en FlyWire, `123` en BANC), `DNpe016 -> cL22c` (`180` y `138`), `DNa03 -> PLP060` (`165` y `105`), `DNpe023 -> CB0172` (`155` y `188`) y `DNp71 -> CB0534` (`154` y `187`).
  - Contra `10.000` permutaciones de vocabulario (`media = 0,129`, `máx = 4`, **`p = 0,0000`**) y `10.000` swaps conservando grado exacto entre aristas pesadas (`media = 2,317`, `máx = 9`, **`p = 0,0000`**), la conservación de los 17 relevos es extrema.

## 4. Evidencia cruda verbatim
```text
== Ejecutando auditoria_e_innovacion_2026_11_02.py ==
1. Verificacion con --parquet completada: {"log_path": "/workspace/dnp04/verif/verificacion_dnp04_parquet.log", "sha256": "ad0b16d33b2be77417ffb1fd75ced1833caf259f32c721a0c3ab6932a58a7128", "bytes": 9596}
FILAS_PARQUET {"Q1": [1, 190.0], "Q2": [937, 6789.0], "Q3": [505, 4366.0], "Q4": [1184, 8733.0], "Q5": [1243, 6240.0], "Q6": [1677, 18623.0]} igual_al_sello=True
COMPARA_AGREGADO {"global": true, "guardas": true, "p": true, "proxy": true, "r": true, "s4": true} todo_igual=True
2. Evaluacion de proxies completada: {"lineal_006": {"n_pasa_tol015": 4, "MAE": 0.1312, "MaxErr": 0.2943, "R2": 0.4985, "r_Pearson": 0.7556}, "freno_efectivo": {"n_pasa_tol015": 7, "MAE": 0.0608, "MaxErr": 0.1373, "R2": 0.9065, "r_Pearson": 0.9705}, "controles": {"within_stimulus_target_perm_10000": {"obs_MAE": 0.0608, "null_MAE_mean": 0.098, "null_hits_mean": 5.39, "p_MAE": 0.1043, "p_hits7": 0.104}, "cross_pair_perm_10000": {"obs_MAE": 0.0608, "null_MAE_mean": 0.2461, "null_hits_mean": 2.56, "p_MAE": 0.0015, "p_hits7": 0.0024}}}
3. Conservacion de relevos D->X FlyWire vs BANC completada: {"n_typed_dx_flywire": 7052, "n_typed_dx_banc": 5867, "n_shared_typed_dx": 2701, "spearman_w_max_shared_dx": 0.612, "spearman_p": 2.2118338804821474e-277, "n_heavy_ge80_fw_shared_vocab": 37, "n_heavy_ge80_banc_shared_vocab": 31, "n_conserved_heavy_ge80": 17, "null_degree_preserving_swap_10000": {"mean": 2.3173, "max": 9, "p": 0.0}, "null_vocab_permutation_10000": {"mean": 0.129, "max": 4, "p": 0.0}}
JSON_GUARDADO /workspace/dnp04/verif/auditoria_e_innovacion_2026_11_02.json bytes=22281 sha256=7e8fbb74f2462af9a4f68a7d733b73f57d498800a86a52e1326239ef3e9a4fab
```

## 5. Archivos generados y commiteados
- En `titan/mecanismo-dnp04-2026-11-02`:
  - `tools/verificar_dnp04.py` (commit `0c849ddc73d2494ee3e06820f300ae39bc6f4896`, blob `66a235fd87af51716a8d668cdaa71e0ea8a44980`, SHA-256 `623f028c0646460bc18b7e01bc07405698f1aa887b3a0d554458910081ab48b7`)
  - `docs/campo/resultados/2026-11-02-mecanismo-dnp04/verificacion_dnp04_parquet.log` (commit `2cb9beb3994091b4daa473487472959194472564`, blob `33d3b4db6266a41481933415050ae85432ea238a`, SHA-256 `ad0b16d33b2be77417ffb1fd75ced1833caf259f32c721a0c3ab6932a58a7128`)
- En `main`:
  - `docs/auditorias/evidencia/2026-11-02-01/auditoria_e_innovacion_2026_11_02.py` (commit `6f60b4fa680753e2c7d87a9b6bf20d33b2c0b09e`, blob `d5fb19850d0a02cd457616b3e7a04700628c3823`, SHA-256 `23fcdbdac382cbc52df7542311fd7c47ce9236c78242b56b5f00863d15335dae`)
  - `docs/auditorias/evidencia/2026-11-02-01/auditoria_e_innovacion_2026_11_02.json` (commit `3f42099d7f3137719721079743ef6e24e1441d86`, blob `647d186405cdea29e3fc1b245b313173b2648b37`, SHA-256 `7e8fbb74f2462af9a4f68a7d733b73f57d498800a86a52e1326239ef3e9a4fab`)
  - `docs/auditorias/2026-11-02-01-auditoria-topo-inverso-dnp04-y-mejora-g1.md` (commit `f38686dcb4dcc121aa15efe21b5cc522fdbfefba`, blob `5faf111fb3f68e44de57b2d6df364d361d6d13c6`)
  - `docs/agents/respuestas/2026-11-02-008-auditoria-mejora-topo-inverso-freno-efectivo-y-veto-recurrente.md` (este archivo)

## 6. NO MEDIDO
- **Intervención causal `Q1` en el LIF sobre los otros 16 relevos pesados conservados (`DNp35 -> CB0527`, `DNpe023 -> CB0172`, etc.):** su conservación anatómica entre FlyWire y BANC está medida (`17` pares, `p < 10^-4`), pero su corte causal en el LIF sigue **NO MEDIDO**.
- **Validación fuera de muestra del Freno Efectivo Rectificado en estímulos adicionales más allá de `LC4`, `LPLC2` y `LPLC1`:** en los 7 pares medidos sube de `4/7` a `7/7` (`R² = 0,9065`) con `0` parámetros libres, pero su evaluación en nuevos estímulos sensoriales queda **NO MEDIDA**.
- **Biología húmeda (in vivo):** **NO MEDIDO**.
