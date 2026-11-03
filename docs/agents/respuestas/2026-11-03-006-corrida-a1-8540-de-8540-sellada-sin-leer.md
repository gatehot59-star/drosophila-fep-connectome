# 2026-11-03-006 · Corrida grande de 009-A1: 8.540 de 8.540 ensayos válidos en 20 tandas y 6 tipos de CPU, sellada sin leer estimandos

**Doc:** [Topo inverso](https://app.clickup.com/90171457413/docs/2kza6fw5-26157), página «2026-11-03-006 · Corrida grande de 009-A1».
**Evidencia:** `docs/agents/evidencia/2026-11-03-006-corrida-a1/`.
**Resultados:** rama `titan/a1-runner-2026-11-03`, `results/a1_2026-11-03/corrida_1/`, commit del bot `7d953dc8`. Sin merge.

**Veredicto del pedido:** la corrida grande terminó completa y válida.

- Corrieron los 8.540 ensayos del plan, semillas 0..19, en 20 tandas.
- Los 21 jobs terminaron en success, en 30 minutos de pared.
- La validación técnica del plan completo da OK, 8.540 de 8.540, con 0 fallos, en Actions y rehecha en brain-env.
- En las 20 máquinas, de 6 tipos de CPU, los 10 testigos del humo dieron las mismas espigas que en el intento 1.

**Nadie computo ni leyo un estimando:** como acordamos, el código de la estadística va commiteado antes de mirar.

## 1. Pedido

«Sí, autorizo la corrida grande en 20 tandas» (3-nov 14:16). Responde a la pregunta con la que cerró 005, que tenía la condición de dejar commiteado el código de la estadística antes de leer cualquier resultado.

Alcance: los 8.540 ensayos, en 20 tandas. No incluía calcular efectos ni decidir hipótesis.

## 2. Herramientas declaradas

- **brain-env** (gateway python):
  - pruebas de `plan_a1.py` y `juntar_a1.py`;
  - sintaxis del workflow;
  - el cotejo posterior.

  Solo escribi en `/workspace/a1/v2`.
- **GitHub MCP**:
  - dos pushes a la rama: `a42c9fa5` (código y workflow, sin disparo) y `e7490f59` (huellas y disparo);
  - este commit a `main`;
  - lecturas, y las etiquetas de `actions/upload-artifact` y `actions/download-artifact` para fijarlas por SHA.
- **API pública de Actions desde brain-env**: unos 25 pedidos de estado de jobs y pasos.
- **Actions**: run 41684131931, con 20 jobs de bloque y un job final; repo público, sin cuota.
- **ClickUp**: una página nueva en el Doc Topo inverso.

## 3. Qué se midió

Cada fila va así: afirmación, instrumento, si podía dar rojo, y veredicto.

| # | Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|
| 1 | El reparto cubre el plan exacto sin partir celdas | `plan_a1.py --prueba` en brain-env y en el job final: 8.540 ensayos, 0 duplicados, faltantes, extras o celdas partidas; bloques de 340 a 440 | Sí: con un ensayo movido, uno faltante o uno duplicado da FAIL (4/4 casos) | PASS |
| 2 | Empaquetar y juntar no pierde ni cambia recibos | `juntar_a1.py prueba`: 6/6 | Sí: un testigo adulterado da DISTINTO, una línea rota queda ilegible y un plan incompleto no valida | PASS |
| 3 | Cada job corrió los bytes probados | `sha256sum --check HUELLAS.sha256` en los 21 jobs, con 11 archivos más el manifiesto | Sí: un byte distinto da FAILED | PASS |
| 4 | Cada máquina reconstruye el mismo manifiesto | `cmp` del manifiesto rehecho contra el del intento 1, en 20/20 bloques | Sí: un byte distinto corta el job | PASS |
| 5 | La máquina no cambia las espigas | 10 testigos de humo rehechos en cada bloque: 10/10 IGUAL en 20/20, sobre 6 tipos de CPU (AMD EPYC 7763, 9V45 y 9V74, Intel Xeon 6975P-C y Platinum 8573C; con y sin AVX-512) | Sí: un testigo adulterado da DISTINTO (prueba 2) | PASS: 200 de 200 ensayos iguales |
| 6 | El plan completo es técnicamente válido | `validar-todo` en el job final: OK, 8.540 de 8.540, 0 fallos | Sí: T09 de 005 y la prueba 2 | PASS |
| 7 | La validación se reproduce fuera de Actions | `comparar_corrida_a1.py` en brain-env: K1 a K6, 6/6 IGUAL | Sí: con una `mask_hash` cambiada, K3 y K5 dan DISTINTO (4/6, EXIT=1) | PASS |
| 8 | Los 8.540 recibos vienen del mismo código y del mismo manifiesto | K6: un solo `code_commit` (`e7490f59`), un solo manifiesto (`267ca1d0`), todos OK y `CythonCodeObject` | Sí: dos commits o dos manifiestos lo tumban | PASS |

La corrida empezó a las 17:25:39Z y el job final cerró a las 17:55:44Z. Los bloques tardaron entre 16,8 y 29,1 minutos.

El tiempo dependió de la CPU más que del tamaño del bloque:

- Los EPYC 9V45 corrieron 440 ensayos en unos 15 minutos.
- Los EPYC 7763 tardaron hasta 26,5 minutos.

Yo había estimado 16 minutos por tanda: le pegué a las rápidas y me quedé corto con las lentas. En total fueron 24.887 s de simulación, unos 2,9 s por ensayo con 3 procesos.

## 4. Evidencia cruda (verbatim)

Job final (`results/a1_2026-11-03/corrida_1/juntar.log` en `7d953dc8`):

```
PLAN ensayos=8540 manifiesto=8540 bloques=20 min=340 max=440 duplicados=0 faltantes=0 extra=0 celdas_partidas=0 ok=True
PRUEBA_PLAN limpio PASS
PRUEBA_PLAN movido_parte_una_celda PASS
PRUEBA_PLAN faltante PASS
PRUEBA_PLAN duplicado PASS
bloque=00 run=41684131931 fuente=e7490f59fee2f36c7a266a712415257f61361939 intento=success censo=success plan=success testigos=success ensayos=success validar=success
(las 20 líneas de estado son iguales salvo el número de bloque)
VALIDACION_CORRIDA OK archivos=20 registros=8540 esperados=8540 fallos=0 por_codigo={}
```

`RESULTADO.txt` de la corrida:

```
run=41684131931 dir=results/a1_2026-11-03/corrida_1 fuente=e7490f59fee2f36c7a266a712415257f61361939 bloques=success intento=success juntar=success
UTC_END 2026-11-03T17:55:21+00:00
```

Cotejo en brain-env (`comparar_corrida_a1.log`):

```
CHEQUEO K1_sha256sums IGUAL archivos=444 distintos=[]
CHEQUEO K2_bloques IGUAL bloques=20 con_problemas=[]
MAQUINA AMD EPYC 7763 64-Core Processor | fma avx2 bloques=00,01,02,03,12,13,14,16,17
MAQUINA AMD EPYC 9V45 96-Core Processor | fma avx2 avx512f bloques=05,06,07,10,11,15,18
MAQUINA AMD EPYC 9V74 80-Core Processor | fma avx2 bloques=08
MAQUINA AMD EPYC 9V74 80-Core Processor | fma avx2 avx512f bloques=09
MAQUINA INTEL(R) XEON(R) PLATINUM 8573C | fma avx2 avx512f bloques=19
MAQUINA Intel(R) Xeon(R) 6975P-C | fma avx2 avx512f bloques=04
CHEQUEO K3_jsonl IGUAL archivos=20 lineas=8540 sha_como_anotados=True
CHEQUEO K4_validacion_actions IGUAL estado=OK registros=8540 esperados=8540 fallos=0
CHEQUEO K5_validacion_rehecha IGUAL manifiesto=267ca1d0820193ff estado=OK registros=8540 esperados=8540 fallos=0 por_codigo={}
CHEQUEO K6_recibos IGUAL recibos=8540 commit=['e7490f59fee2f36c7a266a712415257f61361939'] manifiesto=['267ca1d0820193ff'] estados=['OK'] codeobj=['CythonCodeObject']
RESULTADO 6/6 IGUAL
```

Control negativo (`control_negativo_corrida.log`):

```
ADULTERADO bloques/00/bloque_00.jsonl linea 1 mask_hash
CHEQUEO K3_jsonl DISTINTO archivos=20 lineas=8540 sha_como_anotados=False
CHEQUEO K5_validacion_rehecha DISTINTO manifiesto=267ca1d0820193ff estado=INVALIDO_TECNICO registros=8540 esperados=8540 fallos=1 por_codigo={"MASCARA": 1}
RESULTADO 4/6 IGUAL
EXIT=1
```

## 5. Archivos

En este commit, en `main`:

- `docs/agents/respuestas/2026-11-03-006-corrida-a1-8540-de-8540-sellada-sin-leer.md`
- `docs/agents/evidencia/2026-11-03-006-corrida-a1/`, con estos archivos:
  - `README.md`, con la tabla de bloques, CPU y tiempos;
  - `plan_prueba.log`, `juntar_prueba.log`, `testigos_contra_si_mismo.log` y `workflow_sintaxis.log`;
  - `comparar_corrida_a1.py`, con su log y su exit;
  - `control_negativo_corrida.log`.

En la rama `titan/a1-runner-2026-11-03`:

| Commit | Contenido |
|---|---|
| `a42c9fa5` | `tools/a1/plan_a1.py`, `tools/a1/juntar_a1.py` y `.github/workflows/a1-corrida.yml` |
| `e7490f59` | `tools/a1/HUELLAS.sha256` (11 archivos) y `tools/a1/CORRER` con `corrida=1` |
| `7d953dc8` (bot) | `results/a1_2026-11-03/corrida_1/`: 444 archivos |

La corrida del bot contiene los 20 `bloque_KK.jsonl` con los 8.540 recibos. Por cada bloque guarda también sus logs, sus ids, su validación y sus 10 testigos. Arriba quedan `validacion_corrida.json`, `juntar.log`, `RESULTADO.txt` y `SHA256SUMS.txt`.

## 6. NO MEDIDO

- **Estimandos, pruebas, intervalos y veredictos.** No se calcularon a propósito: primero va el código de la estadística de 010 §7, commiteado y probado con datos sintéticos que puedan dar rojo.
- **El verificador independiente** sobre los recibos. Es trabajo de otro agente.
- **La identidad entre máquinas de los ensayos del plan.** Cada ensayo corrió una sola vez. Lo medido son los 10 testigos por máquina, 200 de 200 iguales, no las 8.540 espigas.
- **La reanudación de faltantes que pide 010 §9.** No está implementada; no hizo falta porque hubo 0 faltantes.
- **La cobertura de las pruebas, los CVEs y el pin de pip por hash.**
- **El CONTEXTO**, que sigue sin este estado ni el de 005.
- **La sección 15 de la página maestra**, que sigue esperando que pegues el texto de 003.

## QA (PROMETEO-QA)

| # | Criterio | Puntos | Score | Evidencia |
|---|---|---|---|---|
| 1 | Completitud | 15 | 15 | 8.540/8.540 recibos, 20/20 bloques, validación completa (`juntar.log`, K4, K5) |
| 2 | Ejecutabilidad | 15 | 15 | 21/21 jobs en success sin editar nada (run 41684131931) |
| 3 | Seguridad | 15 | 12 | Actions fijadas por SHA, incluidas `upload-artifact` `ea165f8d` y `download-artifact` `d3f86a10`; permisos mínimos por job (bloque, read; juntar, write); entradas y código por sha256. −2: pip sin hashes. −1: sin revisar CVEs en vivo |
| 4 | Testing | 15 | 14 | `plan_a1 --prueba` 4/4, `juntar_a1 prueba` 6/6, testigos en 20 máquinas y cotejo con control negativo. −1: cobertura no medida |
| 5 | Arquitectura | 10 | 9 | Celdas enteras por bloque, así que el pareado sale de la misma máquina; JSONL por bloque; job final único. −1: cada bloque baja BANC solo para rehacer las units |
| 6 | DevOps | 10 | 9 | Matriz sin fail-fast, artefactos fijados, negativa a repetir y un solo commit final (`7d953dc8`). −1: falta la reanudación de faltantes de 010 §9 |
| 7 | Documentación | 10 | 9 | README con tabla de bloques, este archivo y el Doc. −1: el CONTEXTO sigue atrasado |
| 8 | Innovación | 5 | 5 | Testigos de máquina en cada bloque; manifiesto rehecho y comparado en cada job; celdas enteras por bloque; corrida ciega; cotejo con control negativo |
| 9 | Proceso QA | 5 | 5 | Cada score cita un archivo, un commit o un run |

**Total: 93/100.** Ningún punto quedó marcado N/A.

## Qué sigue

1. **El código de la estadística de 010 §7**, commiteado antes de tocar estos recibos y probado con datos sintéticos que puedan dar rojo. Incluye:
   - la t pareada unilateral;
   - las familias F_B (46 pruebas), F_C (6) y F_R01 (3), con Holm a 0,01;
   - la inversión de signos como sensibilidad;
   - BCa con 20.000 remuestreos y semilla 2026110209;
   - las reglas de activación y los veredictos.
2. **El verificador independiente** sobre los 8.540 recibos, a cargo de otro agente.
3. **Recién después**, correr la estadística y leer los veredictos.
4. **CONTEXTO y sección 15.**

--- METODO PROMETEO ---
Modo: FULL, por el workflow de CI y la corrida autorizada. Roles: implementación y QA.
Máquinas: brain-env (pruebas y cotejo) y Actions (20 jobs ubuntu-24.04 y un job final).
Artefactos: este archivo y la página 2026-11-03-006 del Doc Topo inverso.
QA: 93/100 sobre 100 puntos aplicables, 0 N/A.
