# 2026-10-11-003 · Nulo por circuito y test de tendencia de la Tabla 7, sobre la base del erratum v2 (EN CURSO)

**Fecha:** 2026-10-11, 01:55 (America/Buenos_Aires).
**Estado:** la corrida sigue en brain-env. Los cruces de entrada dieron PASS. El veredicto de la tendencia es **NO MEDIDO** todavía.

## 1. Pedido

Abraham citó el ítem 1 de «Para dónde vamos» de la 2026-10-11-002: *«Una sola prueba que importa: la del azar por circuito con test de tendencia.»* Cuando yo arrancaba, corrigió:

> *«creo que no estás contemplando que lo visto en marzo ya fue corregido y mejorado con su fe de erratas en esta plataforma, tenemos un git al respecto»*.

Después pidió repetir la última respuesta: el turno anterior se cortó antes de escribir nada, así que no había texto para repetir.

**La corrección es correcta y cambia la base.** Yo iba a usar las anotaciones de marzo (`c03ad46`) para probar la Tabla 7 tal cual se publicó: eso es la v1.0. La base vigente es `docs/ERRATUM.md` (9 ítems) más `docs/PIVOTE-RECIPROCIDAD.md`. Lo que fija, leído hoy en `main`:

- **Ítem 8:** anotaciones pinneadas al commit `17fc577` (md5 `719904ab…`) y parquet md5 `3d802fd5…`.
- **Ítem 3:**
  - la reciprocidad se reporta como **rango contra ensembles**: CP 20,59× con 0/40, y Maslov-Sneppen 47,27×;
  - el claim de la Tabla 7 se acota al **eje** de descomposición.
- **«What has not changed»:** los 8 valores de la Tabla 7 no cambian.
- **Pendiente 9:** la Tabla 7 sin umbral ≥5. La 002 ya lo calculó.
- **Pivote E.3:** **no se corrió un test de tendencia**. No está ni en el erratum ni en la v2, así que la prueba sigue siendo la que falta.

## 2. Herramientas

- brain-env (`build.run`) para los datos y la corrida.
- El sandbox para escribir y probar el código.
- GitHub y ClickUp para los dos artefactos.
- Cero Kaggle.

## 3. Qué se midió hasta ahora

**Instrumento:** `tools/table7_circuit_null.py` (md5 `2796d83678c52888120f5e5566670618`) y `tests/test_table7_circuit_null.py` (md5 `9b2453d9d8af9baeb81bbe99badc5135`).

- Están en brain-env, en `/workspace/dfc-t7`.
- Reusan la 002 sin tocarla (`tools/table7_reciprocity_by_class.py`, md5 `dfbf41ff…`).
- Van a la rama `titan/tabla7-reconstruida-2026-10-10` junto con los logs cuando termine la corrida.

**Diseño, fijado antes de correr (está en el docstring del script):**

- **Nulos, 100 por tipo y por umbral (≥1 y ≥5):**
  - **CP**, el del erratum: destinos barajados dentro de cada bloque (super_class emisor, super_class receptor).
  - **CM**, sólo grado: todos los destinos barajados. **No es el MS del erratum**, porque admite multi-aristas.
- **Tendencia principal**, sobre el eje sensory→central, →descending y →motor:
  - δ = log ρ₁ − log ρ₃, donde ρ es el exceso sobre el nulo;
  - la incertidumbre sale de un bootstrap de dos vías (neuronas emisoras y receptoras) cruzado con los 100 nulos.
- **Tendencia secundaria:** el rango del log-cociente contra el ensemble.
- **Veredictos posibles:** MAS_ALLA_DEL_NULO, INVERTIDO o EXPLICADO_POR_EL_NULO.

**Tests:** 6/6 PASS en el sandbox y en brain-env (`EXIT_TESTS=0`; `tests.log` md5 `d84a2e85d4faa3c97a1c2c7e992147c3`, 285 líneas). Los tres veredictos posibles aparecen con gradientes plantados:

| Caso plantado | Nulo CM | Nulo CP | Veredicto |
|---|---|---|---|
| Gradiente | δ = 1,90 [1,61; 2,23] | δ = 1,91 [1,63; 2,26] | MAS_ALLA |
| Invertido | δ = −2,06 | δ = −1,95 | INVERTIDO |
| Uniforme | δ = −0,05 | δ = −0,03 | EXPLICADO |

El cruce de punta a punta da FAIL si se toca un número.

**Evidencia cruda, `results/table7_circuit_null_2026-10-11/run.log` en brain-env, verbatim:**

```
[    0.5s] INPUT parquet md5=3d802fd542b5d18570ba1ba0bb0abed9 OK pin
[    0.5s] INPUT anotaciones md5=719904abad876c68ace1b5690c9b9b63 OK pin 17fc577 (erratum item 8)
[    0.5s] INPUT json_002 md5=6e395935380145ad429924957c09d649 anotaciones_de_la_002=719904abad876c68ace1b5690c9b9b63
[   36.4s] GRAFO N=138,639 aristas=15,091,983 clases=11 sin_anotacion=14
[   60.8s] CRUCE_002 umbral=1 PASS clases_iguales=True misma_base=True aristas_iguales=True reciprocas_iguales=True aristas=15,091,983 reciprocas=4,014,518
[   60.8s] CRUCE_TABLA7 PASS tabla7_publicada=8/8 (L3 de marzo exactas 10/16: informativo, el pin cambia conteos crudos)
[   61.6s] CRUCE_002 umbral=5 PASS clases_iguales=True misma_base=True aristas_iguales=True reciprocas_iguales=True aristas=2,700,513 reciprocas=377,448
[  231.8s]   umbral=1 CM  20/120  rec_global=88,023  dup=57,815  autolazos=291  seg=148.5
[  355.0s]   umbral=1 CM  40/120  rec_global=87,394  dup=57,961  autolazos=290  seg=271.6
[  479.6s]   umbral=1 CM  60/120  rec_global=87,839  dup=58,006  autolazos=309  seg=396.3
[  603.8s]   umbral=1 CM  80/120  rec_global=89,187  dup=57,372  autolazos=331  seg=520.5
[  729.0s]   umbral=1 CM 100/120  rec_global=88,753  dup=57,666  autolazos=304  seg=645.6
[ 1057.7s]   umbral=1 CM 120/120  (falso)  rec_global=87,890  dup=57,825  autolazos=318  seg=974.3
[ 1206.2s]   umbral=1 CP  20/120  rec_global=195,716  dup=150,149  autolazos=672  seg=109.7
[ 1320.4s]   umbral=1 CP  40/120  rec_global=194,835  dup=149,397  autolazos=653  seg=224.0
[ 1430.5s]   umbral=1 CP  60/120  rec_global=195,507  dup=148,697  autolazos=617  seg=334.0
[ 1541.1s]   umbral=1 CP  80/120  rec_global=195,246  dup=150,073  autolazos=644  seg=444.6
[ 1670.8s]   umbral=1 CP 100/120  rec_global=194,708  dup=149,382  autolazos=697  seg=574.3
```

**Lectura parcial:**

- **Con el pin, la Tabla 7 da 8/8.** Lo que el erratum dice de la tabla se sostiene con su propia base.
- **Los nulos CP individuales están cerca del erratum.** Dan entre 194.708 y 195.716 recíprocas contra 194.974 (4.014.518 / 20,59), o sea dentro del 0,4%. El cruce formal (CRUCE_CP40, media de 100) todavía no corrió.
- **El CM da unos 88 mil contra 84.932 del MS:** es otro nulo, y queda como referencia.
- Cada línea muestra un solo nulo, no la media.

### Errores propios

1. **Arranqué con la base de marzo.** Abraham lo corrigió antes de que corriera nada.
2. **Cambié el estadístico antes de correr, y lo declaro.** El plan previo era sólo el rango contra el ensemble. En sensory→motor cada nulo tiene pocas recíprocas y el seudoconteo empuja esa prueba hacia «más allá del nulo». Por eso el bootstrap del exceso pasó a ser la principal.
3. **El control negativo cazó un sesgo mío.** El seudoconteo pesaba distinto de los dos lados y rechazaba 5 de 5 grafos falsos en datos chicos. Lo corregí promediando el nulo por réplica: ahora rechaza 0 de 5. La versión en brain-env es la corregida.
4. Una consulta de seguimiento a brain-env se cortó por tiempo, sin pérdida.

## 4. NO MEDIDO

- **Todo el veredicto:**
  - la tendencia principal y la secundaria, con los dos nulos y los dos umbrales;
  - CRUCE_CP40, CONSERVACION, el control negativo y la tabla por circuito con ρ;
  - el embudo.
- **Maslov-Sneppen por circuito:** unos 270 s por nulo, unas 3 horas para 40.
- **Covariación con el acceso motor** (pivote E.4).
- **Un nulo por neuropilo de cada sinapsis.**
- **El cruce con Lin 2024** valor por valor.

## 5. Próximo paso

Cuando termine la corrida (en brain-env, hacia las 02:00):

1. Leer `results/table7_circuit_null_2026-10-11/run.log` y `table7_circuit_null.json`.
2. Commitear el script, los tests y los logs a la rama.
3. Escribir la respuesta final con el veredicto y actualizar el CONTEXTO, con la base del erratum como vigente.

--- METODO PROMETEO ---
Máquina: brain-env (tests y corrida en curso) y sandbox (tests). Entrega parcial.
Artefactos: `docs/agents/respuestas/2026-10-11-003-nulo-por-circuito-base-erratum-EN-CURSO.md` + Doc de ClickUp.
