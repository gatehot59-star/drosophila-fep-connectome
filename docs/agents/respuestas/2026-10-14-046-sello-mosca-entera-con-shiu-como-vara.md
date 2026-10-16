# 2026-10-14-046 · Sello de H_MOSCA_ENTERA: la líquida en el cerebro entero, con Shiu 2024 como vara

**Fecha:** 2026-10-15, 23:30 (America/Buenos_Aires) · **Método:** PROMETEO

## Pedido

Abraham, ClickKit `sellar_mosca_entera_046`, 15-oct 23:15: «Sellá la mosca entera con líquidas, con Shiu como vara».

## Veredicto primero

- [MEDIDO] Nuestro parquet es byte a byte el `Connectivity_783.parquet` de Shiu: mismo tamaño (100.804.642 bytes) y mismo git blob (`d386555d1a5f40ebfa1380bcb05b1fab044855fd`) que el archivo de su repo en el commit `91bdd1e7`. Esto cierra el NO MEDIDO de la 045.
- [MEDIDO] De los 21 sensores de azúcar del notebook de Shiu (ids de v630), 20 existen en v783 (LB3, sugar/water); falta `720575940620900446`. MN9 (`720575940660219265`) existe en v783 (ingestion_motor_neuron, CB0701).
- [SELLADO] `tools/mosca_entera/SELLO-MOSCA-ENTERA.md` en `titan/mosca-entera-2026-10-15` (`500f66d`, md5 `55bc4c76657e35f341300d0e082c7ebe`). Cuatro brazos: el LIF de Shiu sin cambios, nuestra líquida (la celda de H_LECTOR) en las 138.639 neuronas, la misma sin término líquido, y un rival de proximidad en el grafo sin dinámica. Dos nulos de 40: pesos barajados (el de Shiu) y destinos barajados con grados conservados. Un control que tiene que pasar antes de interpretar nada (REPRO_SHIU) y cuatro hipótesis con bandas fijadas: MN9, CONJUNTO, RIVAL y LIQ.
- [DECLARADO] El primer commit del sello (`863d2a0`) decía 23:40 y se escribió a las 23:20: corregido en `500f66d`, sin tocar brazos, nulos, controles ni hipótesis.
- [NO MEDIDO] Todo: no hay instrumento todavía. La destilación se sella aparte y sólo si MN9 y CONJUNTO salen SOSTENIDAS.

## Herramientas y máquina

- Web: `model.py` y `example.ipynb` de Shiu en su commit `91bdd1e7`, listado del repo por la API de GitHub.
- brain-env (una llamada por vez): `git hash-object` del parquet, md5 de datos y `ids_shiu.py` (lee anotaciones y dos columnas del parquet). Se confirmó que brain-env no tiene brian2 y tiene 2 núcleos y 7 GB, ocupada con la réplica de H_LECTOR (sin tocarla).
- GitHub: `create_branch` de `titan/mosca-entera-2026-10-15` desde `main` en `7d121d6`; dos `push_files` a esa rama; uno a `main` (esta respuesta y el parche del CONTEXTO).
- ClickUp: Doc público de la 046.
- Delicado: no. Ningún merge, nada a Zenodo ni Kaggle.

## Archivos

Rama `titan/mosca-entera-2026-10-15`, head `500f66d`, verificados desde un clon fresco:

| Archivo | md5 |
|---|---|
| `tools/mosca_entera/SELLO-MOSCA-ENTERA.md` | `55bc4c76657e35f341300d0e082c7ebe` |
| `tools/mosca_entera/ids_shiu.py` | `c82a835586846568cb35e1f1a5e9b14b` |
| `results/mosca_entera_2026-10-15/pines.log` | `6144a4bf14a4bcde44da211749bf5249` |

En `main`: esta respuesta, `tools/contexto/actualizar_contexto_2026-10-14-046.py` y su workflow.

## Lo que sigue

1. Instrumento en Actions: LIF de Shiu con brian2, la líquida entera con sus nulos, prueba con grafos chicos y humo corto.
2. CORRER y agregado, con el veredicto de cada hipótesis contra sus bandas.

## NO MEDIDO

1. REPRO_SHIU y las cuatro H_ENTERA.
2. El md5 de `Completeness_783.csv` (lo fija el instrumento).
3. Tiempo y memoria del cerebro entero en Actions.

## Antes de firmar

- «Byte a byte el de Shiu»: mismo blob de git, medido con `git hash-object` en brain-env contra el sha que da la API de GitHub para su archivo. Podía dar distinto.
- Los 20 de 21 salen de `ids_shiu.py` corrido hoy; su log está en la rama con md5 verificado.
- Las bandas del sello se fijaron antes de escribir instrumento y sin haber corrido ninguna neurona sobre el cerebro entero con este estímulo.
- La expectativa honesta del sello (MN9 probable contra pesos barajados, dudosa contra destinos barajados, RIVAL probablemente no) quedó escrita para que se pueda contrastar.

--- METODO PROMETEO ---
Rol: implementa (sello). Delicado: no.
Máquinas: brain-env (pines), web (lectura).
Artefactos: el sello y sus pines en la rama, esta respuesta, el parche del CONTEXTO y su workflow; Doc de ClickUp de la 046.
