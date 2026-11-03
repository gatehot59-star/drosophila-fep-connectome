# 2026-11-03-002 · Seis documentos contrastados: las máscaras de 009-A1 están bien (314 de 314), la sección 15 del Doc maestro no; el runner A1 sigue sin escribir

**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29557 (Space > Topo inverso > 2026-11-03-002)

**Veredicto del pedido.** Lo que BRAIN pudo re-medir sin simular se sostiene. Las guardas anatómicas de la enmienda 009-A1 y las 64 originales del sello 009 dan **314 de 314 iguales** con un instrumento propio, que da rojo (313 de 314, exit 1) cuando se le pone el número colateral viejo de 009. Astra tiene razón en que la **sección 15 del Doc maestro** trae mal las medias del nulo de H_REUSO_CIERRE; el CONTEXTO ya las tenía bien y el veredicto no cambia. El 7/7 de 008 queda como ajuste retrospectivo, no como validación; eso, los 17 relevos frente al nulo de BANC y la reauditoría de los papers son mediciones de Astra que BRAIN no re-midió. El CONTEXTO quedó al día en main (`2beeae0`). Lo que sigue es el **runner A1**, que es entrega de BRAIN y no existe: espera el OK de Abraham, igual que la corrección en el lugar de la sección 15.

## 1. Pedido

El 3-nov a las 03:01 ART, Abraham adjuntó seis documentos sin texto: la auditoría de Astra 2026-11-02-02, las respuestas 2026-11-02-008, 009, 010 y 011, y la reauditoría 2026-11-02-03. Interpretación declarada, por la regla de mayor alcance no irreversible: leerlos contra el repo, re-medir lo que se pueda re-medir sin simulación, poner al día el estado vivo y decir qué sigue. No se pidió correr nada y no se corrió ninguna simulación.

## 2. Herramientas declaradas

- **MUDH Gateway, servicio build (brain-env):** lecturas por raw.githubusercontent, dos instrumentos nuevos y el ensayo en seco del parche del CONTEXTO, todo bajo `/workspace/r2026-11-03/`. La API de GitHub sin autenticar seguía agotada desde el taller (403); las lecturas de API fueron por el conector de GitHub.
- **Conector de GitHub:** lecturas de commits, directorios y archivos; rama nueva `titan/contexto-2026-11-03` desde `c1845fa`; commits `e92f2b5` (parche y workflow, sin disparo) y `d4236b2` (archivo CORRER, que dispara); este commit en main.
- **GitHub Actions x64:** un job del workflow nuevo `contexto-2026-11-03`, que escribió el CONTEXTO en main como bot (`2beeae0`). Los pushes a la rama pueden haber disparado también el workflow preexistente de regresión H4; no lo leí.
- **ClickUp:** lectura de los seis adjuntos y una página nueva en el Doc de Topo inverso.
- **No se tocó:** el sello 009, su JSON y su generador; 010 y su evidencia; el Doc maestro (la sección 15 sigue como estaba); ramas de otros agentes. Sin GPU, Kaggle ni cuota ajena.

## 3. Qué se midió

Una línea por afirmación: afirmación → instrumento → ¿podía dar rojo? → veredicto.

1. Las guardas anatómicas de 009-A1 publicadas en 010 son las del grafo → `guardas_a1_brain.py` v2, de BRAIN, que no importa ni lee `medir_guardas_a1.py`: define D′, QCOL, QXD, sus uniones, ZA, QWEAK y las poblaciones A desde el texto de 010 y compara contra sus tablas y contra la salida JSON de su evidencia, fijada por sha256 → sí: con el colateral viejo de R03 (1.944 en lugar de 452) da 313/314 y exit 1 → **MEDIDO, bien: 314/314, exit 0.**
2. Las 64 guardas originales Q1 a Q4 del sello 009 están bien → mismo instrumento contra `guardas_filas` del sello publicado (sha256 210b5817…) → sí → **MEDIDO, bien: 64/64**, dentro de los 314.
3. Los D′ y las poblaciones A de 010 son exactamente esos conjuntos, no sólo del mismo tamaño → huella sha256 de la lista JSON compacta + LF, el formato que publicó 010 → sí: un índice distinto cambia la huella → **MEDIDO, bien: 22 D′ (16 relevos y 6 hubs) y 16 poblaciones A con huella idéntica.**
4. La sección 15 del Doc maestro tiene mal las medias del nulo → `medias_nulo_cierre.py` sobre `results/reuso_cierre_2026-11-01/cierre.json` en `7f3cbc1` (sha256 a5c689d4…), recalculando desde los 200 registros por mosca y no desde el resumen → sí: si la sección 15 tuviera razón, coincidiría → **MEDIDO: está mal; Astra tiene razón; el CONTEXTO ya tenía los números correctos.**
5. La copia del cierre que usó Astra es la del repo → comparación byte a byte → sí → **MEDIDO, igual.**
6. El CONTEXTO de main quedó con el parche y nada más → campos del commit `2beeae0` por la API (un archivo modificado, +11 −3) y sha256 del archivo en ese commit contra el ensayo en seco → sí → **MEDIDO, bien: 93992ac7…, byte a byte igual al ensayo.**
7. Los 17 relevos sobreviven al nulo de grados de BANC (1/10.001); el 7/7 da p≈0,14 con permutación compartida y una base simple llega a 6/7; BANC es v888 y DNp04→PVLP010 pesa 123; la réplica de H_LECTOR da CERCA y PAGA; la ruta LPi14→H2→CB0705 existe → BRAIN no corrió instrumento → **NO MEDIDO por BRAIN**; se citan como mediciones de Astra.

**Medias del nulo de H_REUSO_CIERRE, desde los 200 registros por mosca**

| Mosca y prueba | Real | Media del nulo | Mínimo a máximo | Sección 15 dice |
|---|---|---|---|---|
| FlyWire T1 | 88,35 % | 49,66 % | 45,88 a 52,61 % | 80,26 % |
| FlyWire T2 | 698 | 286,04 | 257 a 326 | 539,86 |
| BANC T1 | 82,60 % | 35,01 % | 30,94 a 37,98 % | 74,31 % |
| BANC T2 | 419 | 76,515 | 57 a 95 | 328,99 |

El veredicto de H_REUSO_CIERRE no cambia: p = 1/201 en cada prueba, Holm 0,0199 en las cuatro, SOSTENIDA.

**Desglose de los 314 chequeos**

| Grupo | Chequeos |
|---|---|
| Raíces de driver y hub de los 16 relevos | 32 |
| Guardas originales Q1 a Q4 del sello 009 | 64 |
| Tamaño de D′, QCOL, Q1∪QCOL, QXD y Q1∪QXD de cada relevo | 80 |
| Hubs conjuntos: tamaño de D′, QCOL y QXD (6 × 3) | 18 |
| Cascada R01: ZA, ZA∪Q1, Q6 y Q6∪Q1 | 4 |
| Poblaciones A (9) y presinápticas directas (3) | 12 |
| Por relevo: huella de D′, QWEAK, huella de A, peso A→driver y lado (16 × 5) | 80 |
| Por hub: huella de D′ conjunto, Q1conj∪QCOL, Q1conj∪QXD y QWEAK (6 × 4) | 24 |
| **Total** | **314** |

Los drivers de cada hub conjunto son drivers de los relevos más homólogos contralaterales, con tipo y lado leídos del archivo de unidades: H1 = DNp47 der., DNp101 izq. y DNp104 izq.; H1b = DNp104 der. y DNp101 der.; H2 = DNp71 der. y DNg100 izq.; H3 = DNpe023 izq. y DNae005 der.; H4 = DNa06 der. y DNge148 izq.; H4b = DNge148 der. y DNa06 izq. El instrumento verifica los números de esas listas, no la regla con que 009 eligió los espejos.

### Lectura de los seis documentos

- **008 (Argon).** Dos piezas. Los 17 relevos D→X conservados son coherentes con el caso que midió 006 (D→X⊣D′ por DNp04→PVLP010), y Astra los sostiene con el nulo corregido. El predictor 7/7 queda como ajuste descriptivo: se ajustó sobre las mismas siete combinaciones que predice.
- **Auditoría 2026-11-02-02 (Astra).** Corrige el nulo (el original colapsaba duplicados), retira el 7/7 como validación y lista los errores de 009. De ella, BRAIN re-midió la sección 15 y, a través de 010, las máscaras.
- **009 (Argon).** Diseño con errores de procedencia (BANC v626, peso 138) y de colaterales; su sello queda como registro y para correr manda 009-A1.
- **010 (Astra).** Enmienda prospectiva, completa como especificación; sus tablas anatómicas dan 314/314. Ella misma dice que no hay runner, manifiesto ni corrida autorizada.
- **011 (Astra).** Rectificación: la auditoría de Topo no había leído los Papers 1 a 3. Nada que medir.
- **Reauditoría 2026-11-02-03 (Astra).** Coteja H_LECTOR y H_PARES y refuta una frase del Paper 3 con una ruta visual que no pasa por DN. Es material de paper, no del runner; BRAIN no lo re-midió.
- **2026-11-03-001 (otro agente, no estaba entre los adjuntos).** Síntesis en criollo; coincide en que lo próximo es el runner A1 con casos controlados.

### Qué sigue (propuesta, no ejecutada)

El runner A1 es entrega de BRAIN, en una rama `titan/`:

1. Manifiesto con identidades, D′ con huella, máscaras con filas exactas, poblaciones, semillas por fuente con el contrato de 010, plan de condiciones y versiones, commiteado antes de generar actividad. El instrumento de hoy ya reproduce esas identidades y es la base.
2. Implementación sobre el `model.py` de Shiu sin tocar: entrada Bernoulli por tick con PCG64 por fuente, materializada y con hash, y su equivalencia con la semántica de entrada de Shiu probada en un caso chico; máscaras sobre una copia de los pesos; SHAM; banco C con reemplazo de salida sin duplicar eventos.
3. Pruebas con fixtures chicos y recibos corruptos (índice o raíz incorrectos, signo invertido, flujo de entrada distinto, ensayo faltante o duplicado) y humo en Actions.
4. Sin corrida grande hasta que Abraham la autorice. El verificador distinto del productor lo escribe otro agente.

## 4. Evidencia cruda

Instrumento principal, en brain-env (log completo de 361 líneas en la evidencia):

```
$ python3 guardas_a1_brain.py > guardas_a1_brain.log 2> guardas_a1_brain.err; echo $? > guardas_a1_brain.exit
$ cat guardas_a1_brain.exit
0
$ head -7 guardas_a1_brain.log; tail -1 guardas_a1_brain.log
HUELLA parquet efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347 OK
HUELLA units fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df OK
HUELLA sello 210b581792d183517d1e4e7771b8435e4a6acb537bc1ad383e5725c500073e93 OK
HUELLA evid010 d5d9b7bad373c13bc240581153fbef8820e2d5587979b263a7908e76daa4eeb8 OK
FILAS 15091983 abs(w)==con True con>0 True
PARES_UNICOS True
NEURONAS 138639 D_elegibles 1291
GUARDAS_A1_BRAIN 314 / 314 DIFERENTES [] segundos 49.8
```

Control negativo, verbatim (`control_negativo.log`):

```
$ diff guardas_a1_brain.py guardas_a1_brain_negativo.py
35c35
<  'R03': (40, (19, 452), (20, 617), (40, 410), (41, 575)),
---
>  'R03': (40, (19, 1944), (20, 617), (40, 410), (41, 575)),
exit 1
$ python3 guardas_a1_brain_negativo.py > guardas_a1_brain_negativo.log; echo $?
1
$ diff guardas_a1_brain.log guardas_a1_brain_negativo.log
41c41
< CHK R03 QCOL obtenido= (19, 452) esperado= (19, 452) OK
---
> CHK R03 QCOL obtenido= (19, 452) esperado= (19, 1944) DIFERENTE
361c361
< GUARDAS_A1_BRAIN 314 / 314 DIFERENTES [] segundos 49.8
---
> GUARDAS_A1_BRAIN 313 / 314 DIFERENTES ['R03 QCOL'] segundos 56.7
exit 1
```

Medias del nulo, verbatim (`medias_nulo_cierre.log`):

```
ENTRADA results/reuso_cierre_2026-11-01/cierre.json @7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4 371287 a5c689d4153a9f4fcfadc573cac58521f1ade330b82d1d122dfae6f15c41aceb OK
flywire t1 n_nulos 200 media 0.496606 min 0.45883534136546184 max 0.5261044176706827 observado 0.8835341365461847 media_resumen_archivado 0.49660642570281127 igual_al_resumen True seccion15_dice 0.8026 seccion15_coincide False
flywire t2 n_nulos 200 media 286.04 min 257.0 max 326.0 observado 698 media_resumen_archivado 286.04 igual_al_resumen True seccion15_dice 539.86 seccion15_coincide False
flywire p_por_prueba [0.004975124378109453, 0.004975124378109453]
banc t1 n_nulos 200 media 0.350106 min 0.3094289508632138 max 0.3798140770252324 observado 0.8260292164674635 media_resumen_archivado 0.3501062416998672 igual_al_resumen True seccion15_dice 0.7431 seccion15_coincide False
banc t2 n_nulos 200 media 76.515 min 57.0 max 95.0 observado 419 media_resumen_archivado 76.515 igual_al_resumen True seccion15_dice 328.99 seccion15_coincide False
banc p_por_prueba [0.004975124378109453, 0.004975124378109453]
p [0.004975124378109453, 0.004975124378109453, 0.004975124378109453, 0.004975124378109453] holm [0.01990049751243781, 0.01990049751243781, 0.01990049751243781, 0.01990049751243781] H_REUSO_CIERRE SOSTENIDA
EXIT 0
```

Parche del CONTEXTO (ensayo en seco completo en `preflight_parche_contexto.log`):

```
seco: BASE_SHA256 64b5f6f38c3c6e1d9854ac884e1eb5e5f1c5223a6213a03913de4a7d0f85e3f3 bytes 131355; ANCLA 0 a 4 con 1 aparición;
      RESULTADO_SHA256 93992ac790ee58a7713fa1e9acb42e0c0f1e54f03594183224ed6b92c57934b8 bytes 136411; EXIT 0
negativos: base distinta EXIT 2; resultado distinto EXIT 4; ancla ausente EXIT 3; ancla repetida EXIT 3
DIFF_LINEAS 14 menos 3 mas 11
raw @e92f2b5 tools/contexto/parche_contexto_2026_11_03.py: 7833 bytes, sha256 b717fe8bc0e2933d1458338d2eb388483f48731aa22d93fee7610aa430375fbd, igual al de brain-env
raw @e92f2b5 .github/workflows/contexto-2026-11-03.yml: 2056 bytes, sha256 69dc223babba470f9d713f0a2a5b7d1c3d60036cb3320386d113ab1921e47b04
commit 2beeae0883fab7e2a863cea97ecf3cd6092b21f1: autor github-actions[bot], 2026-11-03T06:24:08Z;
      files: docs/agents/CONTEXTO-drosophila-fep.md modified, additions 11, deletions 3
raw @2beeae0 docs/agents/CONTEXTO-drosophila-fep.md: 136411 bytes, sha256 93992ac790ee58a7713fa1e9acb42e0c0f1e54f03594183224ed6b92c57934b8, igual al ensayo en seco
```

Copia del cierre de Astra: `/workspace/astra_topo_audit_20261102/cierre_original.json`, 371.287 bytes, igual byte a byte al de `7f3cbc1`.

## 5. Archivos generados

En main, bajo `docs/agents/evidencia/2026-11-03-002-contraste/`:

| Archivo | Bytes | sha256 |
|---|---|---|
| `guardas_a1_brain.py` (v2, con rutas por argumento) | 12.333 | c928e2b0fdb02aba9950e3216b1805e3a065f7908bf70c9846cdbc8031c197d3 |
| `guardas_a1_brain.log` | 27.677 | 277f5d156c992a1cd6e3feea64589edde152d480ac99954ec1bb12ccacdad2d2 |
| `guardas_a1_brain.exit` | 2 | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa |
| `control_negativo.log` | 1.025 | ebbbed7d0865c950960bc2872b660c4ecfd8f7522b53439cbe60ef139cce0ff2 |
| `medias_nulo_cierre.py` | 1.871 | 813a751d82adaec3bfd8c8c9bfba024aaf7fb5c7c34127a222d3c04c1f79ef42 |
| `medias_nulo_cierre.log` | 1.295 | 9c13ba4acc79f1d406cf406140c6e337c2232a47abd039733b951d5447502d2f |
| `preflight_parche_contexto.log` | 2.712 | 3f2543bdbac404c62c21036ea06d978c2dc2b2c51a70f74105d8b1c594830739 |

En la rama `titan/contexto-2026-11-03`: `tools/contexto/parche_contexto_2026_11_03.py` (7.833 bytes, b717fe8b…), `.github/workflows/contexto-2026-11-03.yml` (2.056 bytes, 69dc223b…) y `tools/contexto/CORRER-2026-11-03`. En main, por el bot: `docs/agents/CONTEXTO-drosophila-fep.md` (136.411 bytes, 93992ac7…, commit `2beeae0`). Esta respuesta. En ClickUp, la página del Doc enlazada arriba.

No se commitean, por ser binarios grandes: `connectivity.parquet` (100.804.642 bytes, sha256 efeb23fb…) y `flywire_units.npz` (993.755 bytes, sha256 fa92fcd4…), los mismos que usaron H_MECANISMO y 010. El script negativo es el principal con la única línea que muestra el diff (sha256 37d49c19…). Los instrumentos guardan el primer ensayo (v1, 210/210) sólo como antecedente: la v2 lo contiene entero y es la que se commitea; la iteración de QA agregó rutas por argumento y se volvieron a correr los tres.

## 6. NO MEDIDO

- Runner A1, su prueba, el manifiesto, la corrida, el verificador distinto del productor, la potencia con n=20 y la equivalencia de la entrada Bernoulli con PCG64 frente a la de Shiu.
- Lo que dicen Astra y Argon y BRAIN no re-midió: los 17 relevos frente al nulo de BANC (1/10.001), el 7/7 con p≈0,14 y la base de 6/7, BANC v888 y el peso 123, la réplica de H_LECTOR, la ruta LPi14→H2→CB0705 y la lectura de los papers de 011.
- La regla con que 009 eligió los espejos de cada hub.
- El id del run de Actions y el texto de su log: el conector no expone Actions y la API sin autenticar está agotada; el campo estructurado usado fue el commit del bot.
- El workflow de regresión H4 en los pushes de la rama: no se leyó.
- Revisión externa del workflow del CONTEXTO: no pedida, queda como deuda.
- La corrección de la sección 15 del Doc maestro: no se hizo; es texto de otro agente y espera a Abraham.

## QA (PROMETEO-QA)

Aplicables 75: Completitud 15, Ejecutabilidad 15, Seguridad 15, Arquitectura del razonamiento 10, Documentación 10, Innovación 5 y Proceso QA 5. N/A 25: Testing 15 (no hay código de producto; los instrumentos traen su control negativo) y DevOps 10 (sin deployment).

| Criterio | Puntaje | Evidencia |
|---|---|---|
| Completitud | 14/15 | Seis documentos clasificados (sección 3), dos instrumentos con exit code y log completo, CONTEXTO parcheado y leído de vuelta, Doc. −1: lo de Astra y Argon sobre BANC, la permutación y H_LECTOR no se re-midió (sección 6) |
| Ejecutabilidad | 14/15 | `guardas_a1_brain.py` exit 0 (314/314) y su negativo exit 1; `medias_nulo_cierre.py` exit 0; el workflow corrió y el bot escribió `2beeae0`; rutas por argumento y entradas verificadas por sha256. −1: el parquet y el archivo de unidades no están en el repo, sólo sus huellas |
| Seguridad | 13/15 | `.github/workflows/contexto-2026-11-03.yml` (69dc223b…): disparo restringido a rama y archivo, `contents: write` como único permiso, checkout fijado por SHA, sin secretos, corta antes de escribir si base, ancla o resultado no coinciden y exige que sólo cambie el CONTEXTO. −2: el bot escribe en main sin revisión humana intermedia y no se pidió revisión externa |
| Arquitectura del razonamiento | 9/10 | Cada afirmación con instrumento y si podía dar rojo (sección 3); instrumento propio sin importar el ajeno; la evidencia de 010 se usa sólo como valor esperado; negativo con el error real de 009. −1: verifica las listas de drivers de los hubs, no la regla de espejos |
| Documentación | 9/10 | Seis campos, Doc espejo y evidencia cruda commiteada. −1: el log de 361 líneas vive sólo en git; el Doc lleva el resumen |
| Innovación | 4/5 | El negativo usa el número viejo de 009 como prueba de rojo; las huellas de D′ quedan listas para que el manifiesto del runner las afirme. −1: ninguna mejora implementada en el runner, que no existe |
| Proceso QA | 5/5 | Cada puntaje cita archivo, commit o sha256 |

Total **68/75 → 90,7/100**. Iteración 1 de QA: Ejecutabilidad estaba en 13/15 por rutas fijas de brain-env; se agregaron argumentos y se re-corrieron los tres instrumentos, y los logs commiteados son de esa segunda corrida.

```
--- METODO PROMETEO ---
Accion delicada: SI (workflow nuevo con escritura del bot en main; solo el CONTEXTO)
Modo aplicado:   FULL
Maquina:         brain-env (instrumentos y ensayo en seco); Actions x64 ubuntu-24.04 (parche en main)
Rubrica:         68/75 -> 90,7/100
N/A declarados:  25 (Testing 15: sin codigo de producto, los instrumentos traen control negativo; DevOps 10: sin deployment)
Review externo:  no pedido (deuda declarada)
Instrumento:     BRAIN; python3 guardas_a1_brain.py -> exit 0, 314/314; negativo -> exit 1, 313/314;
                 python3 medias_nulo_cierre.py -> exit 0; parche en seco exit 0 y negativos 2/4/3/3;
                 evidencia cruda en docs/agents/evidencia/2026-11-03-002-contraste/; commit del bot 2beeae0
Artefactos:      docs/agents/respuestas/2026-11-03-002-seis-documentos-contrastados-y-guardas-a1-iguales.md
                 + https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29557
```
