# 2026-10-10-002 · Tabla 7 reconstruida: reproduce L3 de marzo 16/16; el 8,7% publicado es doble redondeo

**Veredicto del pedido:** el script reconstruido reproduce la salida L3 de marzo **16/16 filas exactas** (aristas, recíprocas y % a 2 decimales) con las anotaciones FlyWire vivas en marzo (`c03ad46`), y la Tabla 7 publicada **8/8** a un decimal. Con el pin de mayo (`17fc577`) da 10/16, por recambio de `root_id`, no por reclasificación. El control negativo dio rojo.

## 1. Pedido

"Reconstruct and run the lost Table 7 script": reconstruir el script perdido de la Tabla 7 del paper v1.0 (reciprocidad por tipo de circuito), correrlo sobre FlyWire v783 y compararlo con la salida L3 de marzo y con la tabla publicada.

## 2. Herramientas declaradas

- **brain-env** (gateway `build.run`): tests, dos corridas completas de ~90 s, descarga pública de la versión de marzo de las anotaciones (raw.githubusercontent.com), diff de anotaciones, commit local `7117e45`. Sin Kaggle ni cuota ajena.
- **GitHub (integración):** historial de `flyconnectome/flywire_annotations` (lectura); rama `titan/tabla7-reconstruida-2026-10-10`; commit `1f66456` con el código; PR hacia `main` sin merge; esta respuesta.
- **ClickUp:** Doc público nuevo y corrección del Doc del corpus.
- brain-env sólo tiene credencial de push para `mojo-absoluto`; no la extendí a este repo. Por eso el código subió por la integración de GitHub.

## 3. Qué se midió

- Tests: `TESTS_OK 4` (fuerza bruta, mapeo no ordenado, comparador ±1, end-to-end con 2 neuronas sin anotación).
- Mapeo: 138.639 IDs, biyección, índice de Eon = rank ordenado. El mapeo del script FEP de marzo y el de `src/cp40.py` dan lo mismo.
- Corrida A, pin `17fc577` (md5 `719904abad876c68ace1b5690c9b9b63`): L3 **10/16**, Tabla 7 8/8, control rojo, 14 neuronas del grafo sin anotación.
- Diff `c03ad46` vs pin: 14 `root_id` sólo en marzo, 18 sólo en el pin, **0** cambios de `super_class` en 139.230 comunes. `c03ad46` (vigente en main de 2025-10-07 a 2026-04-28, 139.244 filas) tiene exacto el conteo por clase que imprimió marzo.
- Corrida B, `c03ad46` (md5 `16ee17446c428bd27cf2bdefb83af4fd`): L3 **16/16**, Tabla 7 **8/8**, control rojo, 22 neuronas del grafo sin anotación.
- Doble redondeo: 2.104 / 24.327 = 8,6488%, que a un decimal es 8,6. El 8,7 publicado (repetido en `docs/ERRATUM.md` y `docs/PIVOTE-RECIPROCIDAD.md`) sale de 8,65 → 8,7.
- Umbral ≥5: 2.700.513 aristas, 377.448 recíprocas, 13,98%, igual al ítem 5 del erratum (otro script, agosto). Tabla 7 bajo umbral: intra-sensory 37,5; intra-motor 35,0 (80 aristas); intra-visual centrifugal 23,4; intra-optic 17,1; sensory→central 13,8; sensory→descending 2,8; sensory→motor 1,3; optic→motor sin aristas (las 6 sin umbral tienen menos de 5 sinapsis).
- Copia a GitHub: `git diff --stat FETCH_HEAD(1f66456) HEAD(7117e45)` sobre los 3 archivos de código = 0 líneas. Lo subido es byte a byte lo que corrió.

## 4. Evidencia cruda (extracto verbatim, líneas sin editar)

Corrida B, `results/table7_anotaciones_marzo_c03ad46_2026-10-10/run.log` (md5 `ee2f3aa4da33d3a3da3c2aefab3d858b`):

```
[    0.5s] md5 parquet     = 3d802fd542b5d18570ba1ba0bb0abed9  OK pin
[    0.5s] md5 anotaciones = 16ee17446c428bd27cf2bdefb83af4fd  DISTINTO del pin
[    7.3s] N=138,639  filas=15,091,983  sinapsis=54,492,922
[   44.0s] mapeo root_id->indice: {"ids": 138639, "ids_con_varios_indices": 0, "indices_con_varios_ids": 0, "indice_eon_igual_rank_ordenado": true}
[   46.0s] anotacion: {"filas_tsv": 139244, "filas_mapeadas": 138617, "filas_mapeadas_duplicadas": 0, "neuronas_sin_anotacion": 22}
[   55.1s] global: aristas=15,091,983  unicas=15,091,983  autolazos=0  con_reciproca=4,014,518  (26.60%)
[   55.7s]   EXACTA   global                         ref=[15091983, 4014518, '26.60']  obs=[15091983, 4014518, '26.60']
[   55.7s]   EXACTA   sensory->descending            ref=[24327, 2104, '8.65']  obs=[24327, 2104, '8.65']
[   55.7s]   EXACTA   sensory->motor                 ref=[1178, 42, '3.57']  obs=[1178, 42, '3.57']
[   55.7s]   EXACTA   sensory->central               ref=[159360, 38554, '24.19']  obs=[159360, 38554, '24.19']
[   55.7s]   EXACTA   optic->descending              ref=[3069, 285, '9.29']  obs=[3069, 285, '9.29']
[   55.7s]   EXACTA   optic->motor                   ref=[6, 0, '0.00']  obs=[6, 0, '0.00']
[   55.7s]   EXACTA   optic->central                 ref=[5345, 269, '5.03']  obs=[5345, 269, '5.03']
[   55.7s]   EXACTA   intra ascending                ref=[14627, None, '21.43']  obs=[14627, 3134, '21.43']
[   55.7s]   EXACTA   intra central                  ref=[4586059, None, '26.00']  obs=[4586059, 1192460, '26.00']
[   55.7s]   EXACTA   intra descending               ref=[38742, None, '22.40']  obs=[38742, 8680, '22.40']
[   55.7s]   EXACTA   intra motor                    ref=[509, None, '41.26']  obs=[509, 210, '41.26']
[   55.7s]   EXACTA   intra optic                    ref=[6201151, None, '31.98']  obs=[6201151, 1983114, '31.98']
[   55.7s]   EXACTA   intra sensory                  ref=[34111, None, '30.66']  obs=[34111, 10460, '30.66']
[   55.7s]   EXACTA   intra sensory_ascending        ref=[1315, None, '32.09']  obs=[1315, 422, '32.09']
[   55.7s]   EXACTA   intra visual_centrifugal       ref=[7490, None, '36.90']  obs=[7490, 2764, '36.90']
[   55.7s]   EXACTA   intra visual_projection        ref=[346021, None, '29.73']  obs=[346021, 102888, '29.73']
[   55.7s]   COINCIDE  T7 sensory->descending                      publicado=8.7%  obs_1d=8.6%  obs_2d=8.65%  <- solo por doble redondeo (8.65 -> 8.7; exacto a 1 decimal: 8.6)
[   55.7s] intra endocrine (no figura en L3): aristas=68  pct=17.65
[   58.1s] global >=5: aristas=2,700,513  con_reciproca=377,448  (13.98%)  [erratum item 5: 2,700,513 y 13.98%]
[   58.1s]   T7 >=5  motor->motor                             aristas=        80  reciprocas=       28  pct=35.0%  (sin umbral 41.3%)
[   58.1s]   T7 >=5  optic->optic                             aristas= 1,069,677  reciprocas=  183,056  pct=17.1%  (sin umbral 32.0%)
[   58.1s]   T7 >=5  sensory->sensory                         aristas=     1,287  reciprocas=      482  pct=37.5%  (sin umbral 30.7%)
[   58.1s]   T7 >=5  optic->motor                             aristas=         0  reciprocas=        0  pct=nan%  (sin umbral 0.0%)
[   58.1s] VEREDICTO_L3_EXACTA=SI (16/16 filas exactas)
[   58.1s] VEREDICTO_TABLA7_PUBLICADA=SI (8/8)  solo_por_doble_redondeo=["sensory->descending"]
[   58.1s] CONTROL_NEGATIVO_DIO_ROJO=SI (1/16 exactas, 0/8 T7)
[   58.1s] FIN_TABLA7
```

Corrida A, `results/table7_reconstruida_2026-10-10/run.log` (md5 `775647d87d519816f083e346bffa37da`), filas que difieren y veredicto:

```
[   74.0s] anotacion: {"filas_tsv": 139248, "filas_mapeadas": 138625, "filas_mapeadas_duplicadas": 0, "neuronas_sin_anotacion": 14}
[   85.8s]   DIFIERE  sensory->descending            ref=[24327, 2104, '8.65']  obs=[24326, 2104, '8.65']
[   85.8s]   DIFIERE  sensory->central               ref=[159360, 38554, '24.19']  obs=[159316, 38549, '24.20']
[   85.8s]   DIFIERE  intra central                  ref=[4586059, None, '26.00']  obs=[4585828, 1192352, '26.00']
[   85.8s]   DIFIERE  intra optic                    ref=[6201151, None, '31.98']  obs=[6201390, 1983172, '31.98']
[   85.8s]   DIFIERE  intra sensory                  ref=[34111, None, '30.66']  obs=[34107, 10460, '30.67']
[   85.8s]   DIFIERE  intra visual_projection        ref=[346021, None, '29.73']  obs=[346090, 102908, '29.73']
[   88.2s] VEREDICTO_L3_EXACTA=NO (10/16 filas exactas)
[   88.2s] VEREDICTO_TABLA7_PUBLICADA=SI (8/8)  solo_por_doble_redondeo=["sensory->descending"]
[   88.2s] CONTROL_NEGATIVO_DIO_ROJO=SI (1/16 exactas, 0/8 T7)
```

Diff, `diff_annotations_c03ad46_vs_17fc577.log` (md5 `9ff52fdc2b020f56caaae9321b8ede60`), sin las listas de IDs:

```
A /workspace/annot_hist/annot_c03ad46.tsv md5 16ee17446c428bd27cf2bdefb83af4fd filas_unicas 139244 duplicados 0
B /workspace/annotations.tsv md5 719904abad876c68ace1b5690c9b9b63 filas_unicas 139248 duplicados 0
A super_class {'ascending': 1750, 'central': 32384, 'descending': 1303, 'endocrine': 80, 'motor': 110, 'optic': 77539, 'sensory': 16904, 'sensory_ascending': 612, 'visual_centrifugal': 524, 'visual_projection': 8038}
B super_class {'ascending': 1750, 'central': 32383, 'descending': 1303, 'endocrine': 80, 'motor': 110, 'optic': 77541, 'sensory': 16907, 'sensory_ascending': 612, 'visual_centrifugal': 524, 'visual_projection': 8038}
comunes 139230 cambios_super_class 0
FIN_DIFF
```

## 5. Archivos generados

- GitHub, rama `titan/tabla7-reconstruida-2026-10-10`, commit `1f66456`: `tools/table7_reciprocity_by_class.py` (md5 `dfbf41ff089a6dd2a89fe7036e6b426f`), `tests/test_table7_reciprocity.py` (md5 `9db7530a90ed439c723d0cde85f21de6`), `tools/diff_annotations_super_class.py` (md5 `39c3fa932c0b6fd22b29777c5d1ef1ab`).
- brain-env, commit local `7117e45` en `/workspace/dfc-t7`, todavía sin subir: `results/table7_reconstruida_2026-10-10/` (run.log `775647d8…`, tests.log `8e772e3989937b415221d611e1a1cadb`, json `6e395935380145ad429924957c09d649`) y `results/table7_anotaciones_marzo_c03ad46_2026-10-10/` (run.log `ee2f3aa4…`, diff `9ff52fdc…`, json `9317a1d2ee3a2f2b387ca400a086478d`, INPUT_ANOTACIONES.txt `a32fd4e56188c6b2219e4b5b0e2f6063`).
- Esta respuesta.
- Doc ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-20817

## 6. NO MEDIDO

1. Que el código sea el mismo de marzo: da los mismos 16 números; el original sigue perdido.
2. Si marzo usó exactamente `c03ad46` o una versión de octubre de 2025 con la misma asignación de clases.
3. Por qué endocrine no figura en L3: compatible con un filtro de 100 neuronas (endocrine 80, motor 110), no verificable sin el código.
4. Nulo por circuito: la Tabla 7 sigue siendo descriptiva, sin significancia por fila.
5. Editar `docs/ERRATUM.md` (ítem 9 y el 8,7) y el párrafo pivote: decisión de Abraham.
6. Las carpetas `results/` no están en GitHub: sólo en el commit local `7117e45`. La evidencia que decide el veredicto está copiada arriba, verbatim.
7. **Corrección a 001:** sus líneas 41 y 86 dicen que el script L1-L6 estaba en el corpus con la indentación rota. Es falso: sólo estaba la salida L3. Esta respuesta lo corrige (bitácora append-only) y el Doc del corpus quedó corregido en ClickUp. `CONTEXTO-drosophila-fep.md` no se actualizó en este turno.

--- METODO PROMETEO ---
Máquina: brain-env. Rama de código sin merge. Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-20817
