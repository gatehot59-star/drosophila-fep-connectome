# 2026-11-02-002 · H_MECANISMO, corrida 1 verificada: sin veredicto, porque 8 de 17 celdas murieron por infraestructura · lo medido en el modelo: silenciar X sube D en 20 de 20 ensayos en las 8 celdas de tasas · corrida 2 relanzada con enmienda

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29297
Rama: titan/mecanismo-2026-11-02, sin merge.
Corrida 1: run 41410027436, fuente 394334ed, evidencia en results/mecanismo_2026-11-02/actions_correr (commit f323befc7cc07b86c43ed284188e966ac898711c).
Verificación propia: results/mecanismo_2026-11-02/verificacion_corrida1/ (verificar_corrida1.py y su salida).
Sello: tools/mecanismo/SELLO-MECANISMO-2026-11-02.md (3c47400, sha256 ae904036…). Enmienda: tools/mecanismo/ENMIENDA-MECANISMO-2026-11-02.md (3e34d46, sha256 64578a90…).
Corrida 2: run 41459331354, disparada por results/mecanismo_2026-11-02/CORRER2 (b3b398d), en curso al escribir esto.

## 1. Pedido

«verifica» (2-nov-2026, 10:37 ART), sobre la corrida sellada de H_MECANISMO lanzada a las 05:01 ART para «Reconstruí el mecanismo causal paso a paso» (02:43).

## 2. Herramientas declaradas

- brain-env (MUDH gateway, python): bajé la evidencia del commit f323befc por raw.githubusercontent, la recomputé con un verificador propio que no usa agregar_mecanismo.py, conté filas en el parquet local y corrí la prueba de la enmienda con numpy (54/54).
- API pública de GitHub sin token: estado de jobs, pasos y anotaciones (unas 15 llamadas).
- GitHub MCP: pushes a titan/mecanismo-2026-11-02 (código de la enmienda a550e5a, enmienda y verificador 3e34d46, CORRER2 b3b398d) y a main (este archivo). Sin merge.
- ClickUp: una página nueva en el Doc Topo inverso.
- Cuota ajena: minutos de Actions del repo (prueba 41458071625 y corrida 2 con 21 trabajos).

## 3. Qué se midió

Una línea por afirmación: instrumento, si podía dar rojo, veredicto.

- «La corrida terminó» → API de jobs → sí → ROJO. Terminaron 9 de 17: ctrl_mn9 y las 8 celdas de tasas. Las 4 principales (p_*_right) y las 4 izquierdas (i_*_left) salieron con exit 143 (SIGTERM) a los 42–63 min; el paso de subir artefactos quedó salteado.
- «H_MECANISMO tiene veredicto» → agregado con las reglas del sello → sí → H_MECANISMO INVALIDA, por celdas faltantes. No hay veredicto científico de la hipótesis.
- «Corrió el código sellado sobre los datos fijados» → sha256sum --check en cada log (8 archivos OK) y PINES todos true → sí → medido.
- «El control positivo funciona» → azúcar a 100 Hz sobre MN9 → sí → 10 de 10 ensayos, 59,6 espigas de media.
- «Silenciar X sube D a 20 y 150 Hz» → recomputo propio desde las cuentas por neurona y permutación exacta de signos sobre las 2^20 asignaciones → sí (si X no actuara, C1 = C0) → medido en el modelo: 20 de 20 en las 8 celdas, p = 2/2^20 = 1,9e-6 en cada una.
- «C1 apagó exactamente las salidas de X» → conteo propio en el parquet de Shiu → sí → 31.422, 15.645, 30.861 y 42.200 filas, todas inhibitorias, iguales a las registradas.
- «Los números aleatorios comunes fijan S» → huella de S, C0 contra C1 → sí → a 20 Hz S queda igual (19–20 de 20 ensayos idénticos); a 150 Hz no: en LPLC2 S sube 9,75 %. En el modelo, X también frena a S a tasa alta.
- «El censo es reproducible» → conjuntos y paso12 de Actions contra brain-env → sí → conjuntos byte a byte iguales (sha256 f3e8602a…); paso12 con 168 de 179 líneas iguales y 11 que difieren solo en el orden de empates de listas descriptivas (top_X, top_inhibitory).
- «La causa fue memoria» → RSS máximo por proceso → no podía dar rojo por sí solo → NO MEDIDO. Probable: 3,38 GB con unos 4 ensayos por trabajador, 4,48–5,80 GB con unos 14; una celda principal pedía unos 73.
- «La enmienda no cambia la ciencia» → prueba sintética con procesos nuevos contra los valores de joblib, ensayo por ensayo → sí → medido: mismas espigas en C0, C1, R3 y K, en brain-env (numpy) y en Actions (cython, run 41458071625, 54/54). El control MN9 sobre FlyWire completo dio [55, 56, 57] con procesos nuevos, igual que con joblib.

Las 8 celdas que terminaron (D = suma de espigas de las neuronas D por ensayo, media de 20):

| Estímulo | Hz | D con X (C0) | D sin X (C1) | C1/C0 | rel = (D1 − D0)/D1 | Tasa media de D, C0 → C1 |
|---|---|---|---|---|---|---|
| LC4 | 20 | 130,6 | 344,4 | 2,64 | 0,621 | 13,1 → 34,4 Hz |
| LPLC2 | 20 | 288,2 | 716,1 | 2,48 | 0,598 | 20,6 → 51,2 Hz |
| LPLC1 | 20 | 23,2 | 166,0 | 7,16 | 0,860 | 3,3 → 23,7 Hz |
| LPLC4 | 20 | 731,5 | 1.082,6 | 1,48 | 0,324 | 34,8 → 51,6 Hz |
| LC4 | 150 | 692,9 | 985,0 | 1,42 | 0,297 | 69,3 → 98,5 Hz |
| LPLC2 | 150 | 1.301,7 | 1.966,5 | 1,51 | 0,338 | 93,0 → 140,5 Hz |
| LPLC1 | 150 | 376,6 | 620,4 | 1,65 | 0,393 | 53,8 → 88,6 Hz |
| LPLC4 | 150 | 2.029,5 | 2.618,2 | 1,29 | 0,225 | 96,6 → 124,7 Hz |

Lectura de tasas (descriptivo del sello): rel baja de 20 a 150 Hz en los cuatro. Con la regla sellada, LC4 y LPLC1 salen SUSTRACTIVA y LPLC2 y LPLC4 DIVISIVA, las cuatro cerca del umbral. La apuesta 5 del sello (SUSTRACTIVA en al menos tres) quedó perdida: 2 de 4.

### La cadena causal, rotulada con lo que hay hoy

1. S → D directo: MEDIDO anatomía (Paso 1). LITERATURA causal para LPLC2 y LC4 sobre la fibra gigante (Ache et al. 2019, Curr Biol; von Reyn et al. 2017).
2. S recluta a X: MEDIDO modelo (X dispara en C0, de 210 a 4.345 espigas de X por ensayo según la celda). Que X reciba directamente de S solo una minoría de su entrada: MEDIDO anatomía (Paso 2).
3. X frena a D: MEDIDO modelo a 20 y 150 Hz (esta corrida). En la mosca, NO MEDIDO. LITERATURA: la fibra gigante recibe una inhibición independiente de LPLC2 y LC4, sin identificar (Ache et al. 2019, Curr Biol: «the hyperpolarizing component derives from inhibitory GF input neurons independent from LPLC2 or LC4»). La cita que dejó el agente de literatura no era literal; esta sí.
4. Por qué tramo actúa X (S→X→D o un desvío): NO MEDIDO; C2, C3 y R1 a R4 murieron.
5. Si X es especial frente a inhibición emparejada (K): NO MEDIDO.
6. Signo del glutamato (M5): NO MEDIDO.
7. Compuerta de estado por AN_multi_11: NO MEDIBLE en este modelo. LITERATURA verificada: AN_multi_11 de FlyWire es AN06B009 de MANC, GABA (83,4 %), hemilinaje 06B. Ache et al. 2019 (Nat Neurosci) muestra que el estado de vuelo apaga las respuestas visuales de DNp07 y DNp10, y que una de ellas probablemente recibe realimentación de los circuitos motores de vuelo.
8. Función (selección entre acciones) y formación: NO MEDIDO.

## 4. Evidencia cruda

Conclusión de cada trabajo del run 41410027436 (API de jobs):

```text
censo success 08:01:10Z-08:02:11Z
medir (ctrl_mn9) success 08:02:13Z-08:06:31Z
medir (t20_LC4_right) success -08:21:29Z | (t150_LC4_right) success -08:22:07Z
medir (t150_LPLC4_right) success -08:28:40Z | (t20_LPLC4_right) success -08:32:10Z
medir (t150_LPLC1_right) success -08:35:44Z | (t20_LPLC1_right) success -08:42:40Z
medir (t20_LPLC2_right) success -08:42:47Z | (t150_LPLC2_right) success -08:57:26Z
medir (p_LPLC1_right) failure -08:44:24Z | (i_LPLC4_left) failure -08:52:35Z
medir (p_LC4_right) failure -08:57:20Z | (p_LPLC2_right) failure -08:58:25Z
medir (i_LPLC1_left) failure -09:00:51Z | (i_LPLC2_left) failure -09:03:29Z
medir (i_LC4_left) failure -09:05:03Z | (p_LPLC4_right) failure -09:05:45Z
agregar success 09:05:47Z-09:06:11Z
anotacion de p_LPLC4_right: "Process completed with exit code 143."; paso upload-artifact: skipped
```

RSS máximo (/usr/bin/time -v) de las celdas que terminaron: ctrl_mn9 3.376.680 kB; t150_LC4 4.484.412; t150_LPLC1 5.079.668; t150_LPLC2 5.438.156; t150_LPLC4 4.544.036; t20_LC4 4.634.576; t20_LPLC1 5.323.272; t20_LPLC2 5.795.476; t20_LPLC4 4.742.284.

Agregado de la corrida 1 (agregado_mecanismo.log, extracto):

```text
CTRL_MN9 PASA ensayos_con_espiga=10
ESTIMULO LC4 veredicto=INVALIDO guardas=['pin', 'celda_faltante', 'C0_C4_incompletas']
  TASAS rel20=0.620879918687382 rel50=None rel150=0.2965839297497589 -> SUSTRACTIVA
ESTIMULO LPLC2 veredicto=INVALIDO guardas=['pin', 'celda_faltante', 'C0_C4_incompletas']
  TASAS rel20=0.5975703414089227 rel50=None rel150=0.338079377590196 -> DIVISIVA
ESTIMULO LPLC1 veredicto=INVALIDO guardas=['pin', 'celda_faltante', 'C0_C4_incompletas']
  TASAS rel20=0.8602409638554217 rel50=None rel150=0.3930039493834126 -> SUSTRACTIVA
ESTIMULO LPLC4 veredicto=INVALIDO guardas=['pin', 'celda_faltante', 'C0_C4_incompletas']
  TASAS rel20=0.3243118418621836 rel50=None rel150=0.22488303255991596 -> DIVISIVA
H_MECANISMO INVALIDA (LC4=INVALIDO, LPLC2=INVALIDO, LPLC1=INVALIDO, LPLC4=INVALIDO)
```

La guarda «pin» aparece porque la celda falta (pin_ok de una celda ausente da falso), no porque un pin haya fallado.

Salida completa del verificador propio (results/mecanismo_2026-11-02/verificacion_corrida1/verificacion_corrida1.log, md5 de MD5SUMS sin discrepancias):

```text
MD5SUMS archivos=34 discrepan=[]
conjuntos_actions_sha256=f3e8602a6bcf3daefc3b83965f7793a2648f59a22bf8df6209d09ed19e0a3c2d
t150_LC4_right D0=692.9 D1=985.0 cociente=1.42 rel=0.297 positivos=20/20 p_exacto=1.91e-06 (2/1048576) recomputo_igual=True semillas_iguales=True crn_S=20/20 S_dif=0.00% tasa_D0=69.3Hz tasa_D1=98.5Hz X0=1406 tocadas_C1=31422 pines=True
t150_LPLC1_right D0=376.6 D1=620.4 cociente=1.65 rel=0.393 positivos=20/20 p_exacto=1.91e-06 (2/1048576) recomputo_igual=True semillas_iguales=True crn_S=2/20 S_dif=0.02% tasa_D0=53.8Hz tasa_D1=88.6Hz X0=1272 tocadas_C1=30861 pines=True
t150_LPLC2_right D0=1301.7 D1=1966.5 cociente=1.51 rel=0.338 positivos=20/20 p_exacto=1.91e-06 (2/1048576) recomputo_igual=True semillas_iguales=True crn_S=0/20 S_dif=9.75% tasa_D0=93.0Hz tasa_D1=140.5Hz X0=1433 tocadas_C1=15645 pines=True
t150_LPLC4_right D0=2029.5 D1=2618.2 cociente=1.29 rel=0.225 positivos=20/20 p_exacto=1.91e-06 (2/1048576) recomputo_igual=True semillas_iguales=True crn_S=0/20 S_dif=0.20% tasa_D0=96.6Hz tasa_D1=124.7Hz X0=4345 tocadas_C1=42200 pines=True
t20_LC4_right D0=130.6 D1=344.4 cociente=2.64 rel=0.621 positivos=20/20 p_exacto=1.91e-06 (2/1048576) recomputo_igual=True semillas_iguales=True crn_S=20/20 S_dif=0.00% tasa_D0=13.1Hz tasa_D1=34.4Hz X0=210 tocadas_C1=31422 pines=True
t20_LPLC1_right D0=23.2 D1=166.0 cociente=7.16 rel=0.860 positivos=20/20 p_exacto=1.91e-06 (2/1048576) recomputo_igual=True semillas_iguales=True crn_S=20/20 S_dif=0.00% tasa_D0=3.3Hz tasa_D1=23.7Hz X0=264 tocadas_C1=30861 pines=True
t20_LPLC2_right D0=288.2 D1=716.1 cociente=2.48 rel=0.598 positivos=20/20 p_exacto=1.91e-06 (2/1048576) recomputo_igual=True semillas_iguales=True crn_S=19/20 S_dif=0.00% tasa_D0=20.6Hz tasa_D1=51.2Hz X0=403 tocadas_C1=15645 pines=True
t20_LPLC4_right D0=731.5 D1=1082.6 cociente=1.48 rel=0.324 positivos=20/20 p_exacto=1.91e-06 (2/1048576) recomputo_igual=True semillas_iguales=True crn_S=20/20 S_dif=0.00% tasa_D0=34.8Hz tasa_D1=51.6Hz X0=878 tocadas_C1=42200 pines=True
ctrl_mn9 ensayos_con_MN9=10/10 media=59.6 pines=True
tocadas_independiente LC4_right filas_preX=31422 con_peso=31422 todas_negativas=True
tocadas_independiente LPLC2_right filas_preX=15645 con_peso=15645 todas_negativas=True
tocadas_independiente LPLC1_right filas_preX=30861 con_peso=30861 todas_negativas=True
tocadas_independiente LPLC4_right filas_preX=42200 con_peso=42200 todas_negativas=True
paso12_lineas_etiquetadas actions=179 brainenv=179 distintas=11 campos_que_difieren=['top_X', 'top_inhibitory']
```

Comando: `python3 verificar_corrida1.py --dir actions_correr --parquet /workspace/connectivity.parquet --comp Completeness_783.csv --paso12-local paso12.log` (brain-env, Python 3.12).

Prueba de la enmienda en Actions (run 41458071625, extracto de prueba.log):

```text
PASS e2e_igual_a_prueba_previa {"C0": [2, 4, 6, 4, 6, 6, 6, 8, 6, 6, 6, 6], "C1": [6, 6, 6, 8, 6, 8, 8, 12, 10, 10, 10, 6], "R3": [6, 8, 8, 10, 6, 10, 8, 12, 10, 12, 10, 6], "K": [4, 4, 6, 6, 4, 6, 6, 8, 6, 8, 8, 6]}
PASS unir_reconstruye {"a": "p_SYN_a", "b": "p_SYN_b", "C0_igual": true, "indices_igual": true, "pines_igual": true, "estado": "UNIDA"}
PASS unir_rechaza_C0_distinto {"a": "p_SYN_a", "b": "p_SYN_b", "C0_igual": false, "indices_igual": true, "pines_igual": true, "estado": "DISCREPA"}
PASS partido_positivo SOSTENIDA_EN_MODELO
PASS partido_C0_distinto_invalida INVALIDA
PRUEBA_MECANISMO 54/54 PASS
PINES {"comp": true, "conjuntos": true, "conn": true, "model": true} sin_pin=False
COND C0 tocadas=0 D=[55, 56, 57] X=[0, 0, 0] | 50.4 s
	Maximum resident set size (kbytes): 2973456
```

## 5. Archivos generados

En titan/mecanismo-2026-11-02:

- results/mecanismo_2026-11-02/actions_correr/ (corrida 1, escrita por el bot; se conserva sin tocar).
- results/mecanismo_2026-11-02/verificacion_corrida1/verificar_corrida1.py y verificacion_corrida1.log.
- tools/mecanismo/intervenir.py (e656d73e…), unir_celdas.py (5c553287…), prueba_mecanismo.py (1eda0695…), .github/workflows/mecanismo-correr2.yml (dab498de…).
- tools/mecanismo/ENMIENDA-MECANISMO-2026-11-02.md (64578a90…) y results/mecanismo_2026-11-02/CORRER2.
- results/mecanismo_2026-11-02/actions_prueba_41458071625/ (escrita por el bot).

En main: este archivo.

## 6. NO MEDIDO

- El veredicto de H_MECANISMO: P1 a P4 a 50 Hz, los cocientes ΔSX/ΔX y ΔXD/ΔX, R1 a R4, K, M5, los descendentes fuera del objetivo y la réplica izquierda. Todo eso está en la corrida 2.
- La causa exacta del SIGTERM.
- Que la corrida 2 reproduzca a la corrida 1: se chequea al leerla.
- Todo lo que es mosca y no modelo: causalidad, signo del glutamato, compuerta de estado, formación.
- CONTEXTO-drosophila-fep.md no se actualizó en esta entrega; se actualiza con la lectura de la corrida 2.

--- METODO PROMETEO ---
Accion delicada: NO. Relanzamiento previsto por el propio sello; enmienda escrita, probada y fijada antes de CORRER2; corrida 1 conservada.
Modo aplicado: FULL.
Maquina: brain-env (2 CPU, numpy) para verificar y probar; Actions x64 (cython) para la prueba 41458071625 y las corridas 41410027436 y 41459331354.
Instrumentos con capacidad de dar rojo: API de jobs, permutacion exacta, conteo sobre el parquet, regresion de la prueba, sha256sum --check.
NO MEDIDO declarado: causa del SIGTERM y veredicto de la hipotesis.
Review externo: no
