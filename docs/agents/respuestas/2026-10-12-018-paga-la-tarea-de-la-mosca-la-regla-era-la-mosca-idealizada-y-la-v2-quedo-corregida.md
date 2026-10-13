# 018: paga la tarea de la mosca; la «regla a mano» era la mosca idealizada; la v2 quedó corregida (13-oct, 00:45 ART)

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21617

## Veredicto primero (F-01)

- [MEDIDO] `VEREDICTO_GLOBAL -> PAGA LA TAREA DE LA MOSCA`: 6/6 celdas GANA contra SL y contra T (Holm 0,0399 en las 12 pruebas, el mínimo posible con 300 nulos y 12 pruebas); 0 de 300 igualan a W en cada celda. `CHEQUEO INSTRUMENTO ... -> VALIDO`. El falsador sellado (NO PAGA) no se cumplió. Es el primer experimento sellado del 12-oct donde el cableado de la mosca paga.
- [MEDIDO] H3, W contra la regla a mano: PEOR en 4 celdas (p 0,0252; 0,00454; 7,82e-15; 1,08e-09), EMPATE en 2 (p 0,296 y 0,856), nunca MEJOR.
- [MEDIDO, lectura del script sellado] La regla a mano son las mismas etiquetas de la mosca (DNp01 = media de LC4 y LPLC2 del lado; DNp07 = media de LPLC4; DNp06 = media de LPLC1 y LPLC2 con el giro por diferencia), leídas sobre las entradas crudas sin pesos ni dinámica. [CONCLUSIÓN] **Corrige la 017:** no le gana «un sistema clásico» a la mosca; le gana el diseño de la mosca idealizado a nuestra simulación de sus sinapsis.
- [MEDIDO, descriptivo] Con LPLC4 muda, W 0,8030 contra regla 0,7680 (aterrizaje frontal en vuelo 0,515 contra 0,120). Con ruido 0,45, W gira mejor ante el objeto que pasa en 2 de 3 amplitudes (0,705 contra 0,405; 0,765 contra 0,670).
- [MEDIDO] Lo que el modelo deja afuera: las 6 descendentes reciben 40.145 sinapsis; el motivo lleva 875 (2,18%) y ninguna de las 14.576 inhibitorias (36,3%). R1 1.504 neuronas, R2 33.489, cerebro 138.639.
- [MEDIDO] v2 corregida en las tres inconsistencias de la 010, mismo resultado en brain-env y en Actions (md5 iguales), render PASS y verificación del depósito PASS en clon fresco. La Tabla 8 queda para Abraham.
- [CONCLUSIÓN] Abraham tenía razón en lo central: lo que pierde es nuestro modelo de la mosca. No comparto «el control de la mosca es perfecto» como afirmación medible; no hace falta para el argumento.

## 1. Pedido

23:57 ART del 12-oct: «Primero analizá los resultados del último experimento, ya terminó; luego corregí las tres inconsistencias de la v2. Y tu conclusión de que las partes de la mosca son superadas por un sistema clásico de control es inaudita [...] lo único superado somos vos y yo y las herramientas que usamos. Te dije que la neurona debía ser otra, o la topología o el cableado o las formas o una combinación [...]. Ponete pillo.»

## 2. Herramientas y máquina

- brain-env (MUDH Gateway, `build`): lectura del log de la corrida; parche de la v2 (`fix_v2_018.py`), render (`tools/v2/render_v2.py`, pandoc 3.10.2 + typst 0.15.0), `tools/zenodo/depositar_v2.py --verificar`, control de texto de los PDF (`chequeo_pdf_018.py`, md5 `8e30781699750ec2614c1b4ed6e88dd4`, no se commitea), `registro_018.py` (md5 `25a80b8f71fa3c26dc2d0bbc060ffbab`, no se commitea) y la medición `que_falta_al_modelo.py`.
- Actions x64 (repo público, gratis): el workflow `aplicar-fix-v2-018.yml` aplicó el mismo parche con Python 3.12.3, commiteó y se retiró (`ed7c3ac`).
- GitHub MCP: commits en `titan/tarea-mosca-2026-10-12` (`bdf03c2`), `titan/v2-cierre-2026-10-12` (`7f900fe`, `f19a9c7`), `titan/que-falta-al-modelo-2026-10-12` (`3cf6332`), nota en el PR #27 y este archivo. ClickUp: el Doc espejo.
- Acción delicada: no. Nada se mergeó y nada fue a Zenodo.

## 3. Qué se midió

### 3.1 La corrida completa de la 015

Desde un clon fresco del sello `57d094a` (script md5 `40d64e074d9163753439307c5be4ac5e`), 5.628,4 s. Log subido a `results/tarea_mosca_2026-10-12/completa.log` en `bdf03c2`, md5 `ad8c94b47350b5473b13848150047ab4` en el taller y en el clon fresco. `resultados.json` (47.871 B, md5 `08037bd6a6565cbd5207163e39949766`) queda en brain-env. El log termina con dos `EXIT_RUN=0`: el primero es del script (después de `escrito resultados.json` y `# duracion_s`), el segundo es el del envoltorio con `$?` pre-expandido y no vale (016).

| Celda | W | SL media / máx. | T media / máx. | Holm sup (SL, T) | Regla | H3 | Ridge crudo |
|---|---|---|---|---|---|---|---|
| A 0,0, ruido 0,15 | 0,9005 | 0,6967 / 0,8915 | 0,7192 / 0,8730 | 0,0399 / 0,0399 | 0,9195 | PEOR 118 contra 156, p 0,0252 | 0,9935 |
| A 0,0, ruido 0,45 | 0,8805 | 0,6716 / 0,8305 | 0,7033 / 0,8515 | 0,0399 / 0,0399 | 0,8705 | EMPATE 175 contra 155, p 0,296 | 0,9595 |
| A 0,3, ruido 0,15 | 0,9125 | 0,6655 / 0,8880 | 0,6734 / 0,8625 | 0,0399 / 0,0399 | 0,9325 | PEOR 75 contra 115, p 0,00454 | 0,9935 |
| A 0,3, ruido 0,45 | 0,8915 | 0,6530 / 0,8380 | 0,6681 / 0,8390 | 0,0399 / 0,0399 | 0,8935 | EMPATE 135 contra 139, p 0,856 | 0,9575 |
| A 0,6, ruido 0,15 | 0,8680 | 0,6292 / 0,8360 | 0,6246 / 0,8105 | 0,0399 / 0,0399 | 0,9315 | PEOR 73 contra 200, p 7,82e-15 | 0,9940 |
| A 0,6, ruido 0,45 | 0,8580 | 0,6209 / 0,7955 | 0,6252 / 0,7940 | 0,0399 / 0,0399 | 0,9120 | PEOR 103 contra 211, p 1,08e-09 | 0,9590 |

Lectura por condición (orden: posada LOOM_LATERAL, LOOM_FRONTAL, PUNTO, BARRA, NADA | vuelo ídem):

- **Donde pierde W:** con A 0,6 posada ante looming, 0,765 y 0,775 (ruido 0,15) contra 1,000 de la regla: la respuesta de LPLC2 al punto sube los umbrales de DNp01 (0,823 y 0,897 contra 0,306 y 0,355 con A 0,0) y se escapan despegues. En vuelo ante el punto con ruido 0,15, W 0,745 a 0,810 contra regla 0,885 a 0,975.
- **Donde gana W:** con ruido 0,45 ante el punto en vuelo, 0,705 contra 0,405 (A 0,0) y 0,765 contra 0,670 (A 0,3); con A 0,6, 0,770 contra 0,820 (pierde).
- **Brazos descriptivos (A 0,3, ruido 0,15, sin nulos):** LPLC1 muda: W 0,8805, regla 0,8835, y los dos caen en el giro en vuelo (0,485 y 0,475): el giro viaja por LPLC1. LPLC4 muda: W 0,8030, regla 0,7680; aterrizaje frontal en vuelo W 0,515 contra 0,120, barra en vuelo 0,095 contra 0,125.

### 3.2 La regla a mano, leída en el script sellado

```
def lineas_crudas(X):
    return np.stack([media(X, "L", ("LC4", "LPLC2")), media(X, "R", ("LC4", "LPLC2")),
                     media(X, "L", ("LPLC4",)), media(X, "R", ("LPLC4",)),
                     media(X, "L", ("LPLC1", "LPLC2")), media(X, "R", ("LPLC1", "LPLC2"))], axis=2)
```

Es la asignación tipo → descendente de FlyWire (COMPOSICION del log: DNp01 recibe de LC4 y LPLC2, DNp07 de LPLC4, DNp06 de LPLC1 y LPLC2), con pesos iguales y sin dinámica, sobre las entradas crudas, con los mismos umbrales y la misma carrera que W.

### 3.3 Qué le falta al modelo

`tools/que_falta/que_falta_al_modelo.py` (md5 `60d0feedb9aa2b1ae6544bb7a57bde79`) y su log `results/que_falta_2026-10-12/que_falta.log` (md5 `956c81e46d369289383a34c36cc66aca`) en `3cf6332`, verificados en clon fresco. Signo: columna `Excitatory` (valores −1 y 1). Descriptivo, sin nulo.

### 3.4 Las tres inconsistencias de la v2

1. **§3.4, «2.4-fold»:** el 323 es mechanosensory sobre olfactory en el nulo de grado (7,364619 / 0,022797 = 323,05); el 2,4 era visual sobre gustatory en el de neurópilo (1,531126 / 0,632312 = 2,42), otro par. Con la misma definición: 4,2× sin umbral (1,531126 / 0,367658 = 4,16) y, con el umbral, 3.862× (5,811884 / 0,001505) a 40× (4,871795 / 0,120950). Valores de `docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md` (rama `titan/materializacion-h4-guard-2026-10-02`, líneas 104 a 143).
2. **«Validated across three compatible models»:** Tabla 9, SparseLTC 0,630 → 0,832, Linear 0,623 → 0,835, LIF-soft 0,253 → 0,002. Corregido en el resumen, §1.3, §2.5, nota de la Tabla 9, §4.1, Limitación 3, cambio 6, erratum ítem 7 (la v1.0 dice lo mismo en su §2.5 y su Limitación 3: leído en `v1.0.txt`, líneas 161 y 455) y descripción de Zenodo.
3. **«Not testable» sin umbral:** Tabla 5c, olfato 0 contra 1,0 ± 0,9 (z −1,2) y visión 0 contra 0,03 ± 0,16 (z −0,2): compatible, no intesteable; con el umbral el ensemble da 0,0 exacto. Corregido en §3.4 y en `docs/SECCION-V2-DOS-SALTOS.md` (dos lugares).

## 4. Evidencia cruda

```
CHEQUEO INSTRUMENTO guarda_SL=True guarda_T=True reproduce_003=True reproduce=True control_negativo=True control_positivo=True -> VALIDO
VEREDICTO_AMPLITUD A=0.0 -> GANA
VEREDICTO_AMPLITUD A=0.3 -> GANA
VEREDICTO_AMPLITUD A=0.6 -> GANA
VEREDICTO_GLOBAL -> PAGA LA TAREA DE LA MOSCA
escrito resultados.json md5=08037bd6a6565cbd5207163e39949766
# duracion_s=5628.4
CONTROL_NEGATIVO entrada=AGNOSTICA W=0.5830 T_identicos=30/30 -> True
CONTROL_POSITIVO regla_a_mano A=0.3 ruido=0.15 = 0.9325 contra azar 0.5000 + 0.10 -> True
DESCRIPTIVO LPLC1_SILENCIOSA A=0.3 ruido=0.15 W=0.8805 por_condicion=1.000,1.000,0.710,1.000,1.000,0.895,0.940,0.485,0.985,0.790 | regla=0.8835 por_condicion=1.000,1.000,0.720,1.000,1.000,0.925,0.950,0.475,0.960,0.805
DESCRIPTIVO LPLC4_SILENCIOSA A=0.3 ruido=0.15 W=0.8030 por_condicion=0.995,0.995,0.730,1.000,1.000,0.950,0.515,0.960,0.095,0.790 | regla=0.7680 por_condicion=1.000,1.000,0.720,1.000,1.000,0.935,0.120,0.975,0.125,0.805
```

```
$ md5sum (clon fresco de titan/tarea-mosca-2026-10-12 en bdf03c2)
ad8c94b47350b5473b13848150047ab4  results/tarea_mosca_2026-10-12/completa.log
ad8c94b47350b5473b13848150047ab4  /workspace/tm_2026-10-12/completa.log
40d64e074d9163753439307c5be4ac5e  tools/escape_aterrizaje/tarea_mosca.py
```

```
TOTAL_6DN entrada=40145 en_motivo=875 (2.18%) inhibitorias=14576 (36.3%)
DN DNp06 left entrada_sinapsis=10488 en_motivo=160 (1.53%) inhibitorias=3152 (30.1%) inhibitorias_en_motivo=0 presinapticas=1069 con_5_o_mas=479
DN DNp06 right entrada_sinapsis=11466 en_motivo=154 (1.34%) inhibitorias=3535 (30.8%) inhibitorias_en_motivo=0 presinapticas=1045 con_5_o_mas=484
RECORTE R1 neuronas=1504 aristas_internas=91484 sinapsis_internas=553976 neuronas_inhibitorias=421 (28.0%) contiene_motivo=True clases=central 883; visual_projection 526; ascending 48; descending 27; sensory 14; visual_centrifugal 6
RECORTE R2 neuronas=33489 aristas_internas=4031897 sinapsis_internas=16971919 neuronas_inhibitorias=8460 (25.3%) contiene_motivo=True clases=optic 15969; central 10689; visual_projection 4656; ascending 881; sensory 489; descending 485
```

```
# parche de la v2, en brain-env y en Actions (docs/v2/fix-v2-018.log, Python 3.12.3)
ANTES docs/v2/paper1-v2.0.md ec6dc5d3d599f6c1b6fddc8425fe25d2
ANTES docs/ERRATUM.md f8fbb170e20abaacc5730a102aad5491
REEMPLAZO (15 de 15) apariciones=1
DESPUES docs/v2/paper1-v2.0.md e5fb86dcf79867e77434df33269ad745
DESPUES docs/ERRATUM.md f2ad05072086258a8ce76b9d650ed26d
DESPUES docs/SECCION-V2-DOS-SALTOS.md cbe0245750c4ae1810eda829e391ba7a
DESPUES docs/v2/zenodo-v2.0-metadata.json 375853474c9148e92aacdd0945b69e42
PARCHE OK: 15 reemplazos, sin '2.4-fold' en manuscrito ni seccion, metadatos JSON validos
```

```
PDF Mendieta2026_Paper1_v2.0.pdf 327479 d353cf0fd05e9e5637be2bccca7bc98e paginas 17 determinista True
PDF Mendieta2026_Paper1_Erratum_v1.0.pdf 191172 05052e6e7e0dd79cee584c9d285b1b93 paginas 15 determinista True
VEREDICTO_RENDER PASS
VEREDICTO_VERIFICAR PASS   (clon fresco de f19a9c7)
PDF v2  2.4-fold                                    viejo=1 nuevo=0
PDF v2  validated across three compatible models    viejo=1 nuevo=0
PDF v2  Only graded models replicate amplification  viejo=1 nuevo=0
PDF v2  4.2-fold                                    viejo=0 nuevo=1
PDF err Replication across models                   viejo=0 nuevo=1
```

## 5. Sobre la objeción de Abraham [CONCLUSIÓN]

- **En lo central tiene razón.** Leemos 6 descendentes con el 2,18% de su entrada y 0% de su inhibición, sin neuromodulación (octopamina sobre DNp07 en vuelo, Ache 2019), con sintonías supuestas, neuronas de tasa y sin cuerpo. Que con eso la mosca les gane a 600 barajados habla del diseño; que pierda contra su diseño idealizado habla de la herramienta.
- **Lo que no comparto:** «el control de la mosca es perfecto» no es medible acá y no hace falta. La mosca real optimiza supervivencia con poca energía y tamaño, no esta tarea, y nadie midió una mosca en esta tarea.
- **Neurona, topología, cableado, forma o combinación:** es el espacio de hipótesis correcto, y se prueba por factores. La 011 mostró que en la 004 y la 005 no fallaba la neurona; en el escape la líquida plena sí pagó (013 y 014). La forma necesita la tabla de sinapsis con coordenadas, que el parquet no trae.

## 6. Propuesta: factorial con la misma tarea sellada (diseño, sin sellar)

1. Recorte: motivo 46 / R1 1.504 / R2 33.489.
2. Neurona: tasa con τ fija / LIF con signo (Shiu 2024) / líquida plena (013 y 014).
3. Signos: con la inhibición del pipeline / sin ella.
4. Misma tarea, mismos nulos SL y T, la regla idealizada como rival y el ridge como techo. Pregunta: qué factor cierra la brecha entre W y su diseño idealizado.
5. Máquinas: 46 y R1 en Actions; R2 en la GPU de Kaggle con el port a torch verificado contra numpy en R1.
6. Falsador: si con R1, inhibición y la mejor neurona W sigue debajo de la regla idealizada, la brecha no es del recorte.

## 7. Archivos

- Este archivo y el Doc espejo (https://app.clickup.com/90171457413/docs/2kza6fw5-21617).
- `titan/tarea-mosca-2026-10-12` (`bdf03c2`): `results/tarea_mosca_2026-10-12/completa.log`.
- `titan/v2-cierre-2026-10-12` (`7f900fe`, `ed7c3ac`, `f19a9c7`): `tools/v2/fix_v2_018.py`, `docs/v2/paper1-v2.0.md`, `docs/ERRATUM.md`, `docs/SECCION-V2-DOS-SALTOS.md`, `docs/v2/zenodo-v2.0-metadata.json`, `docs/v2/fix-v2-018.log`, `docs/v2/archivos-deposito-v2.0.json`, `docs/v2/render-v2.0.log`, `docs/v2/verificar-v2.0.log`, `docs/V2-CIERRE.md`.
- `titan/que-falta-al-modelo-2026-10-12` (`3cf6332`): `tools/que_falta/que_falta_al_modelo.py`, `results/que_falta_2026-10-12/que_falta.log`.
- En brain-env, sin commitear (binarios y derivados): `/workspace/tm_2026-10-12/completa/resultados.json`, `/workspace/v2cierre_2026-10-12/deposito_018/` (los dos PDF).

## 8. NO MEDIDO

- El factorial: es diseño.
- Una mosca real en esta tarea; cualquier hardware.
- La fisiología de LPLC1 y LPLC4 (sintonías supuestas) y la amplitud de LPLC2 al punto.
- La tabla de sinapsis con coordenadas (forma y dendritas).
- Los PDF nuevos mirados a ojo; la Tabla 8; el informe completo de Tao.
- R1 y R2 son descriptivos, sin nulo; en R2 entran 15.969 neuronas del lóbulo óptico sin modelo de entrada.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| PAGA LA TAREA DE LA MOSCA | Holm sobre 300 SL y 300 T del script sellado | Sí: en la 005 y la 012 el mismo tipo de prueba dio NO PAGA |
| El instrumento es válido | guardas, reproduce, negativo 30/30, positivo | Sí: cada control tiene su FALSO impreso |
| La regla es la mosca idealizada | lectura de `lineas_crudas` en el script sellado | Sí: podría haber usado otros tipos o pesos |
| El log subido es el de la corrida | md5 en el taller y en el clon fresco | Sí: un carácter cambia el md5 |
| El parche es el mismo en dos máquinas | md5 de los cuatro archivos en brain-env y en Actions | Sí: otra versión de Python o un reemplazo distinto cambia el md5 |
| Las frases viejas salieron de los PDF | pypdf sobre PDF viejos y nuevos | Sí: el viejo las tiene (viejo=1) |
| El motivo lleva el 2,18% de la entrada | suma de `Connectivity` por destino | Sí: con otro motivo cambia |
| La crisis es del modelo, no de la mosca | ninguno | No: es conclusión, marcada como tal |

--- METODO PROMETEO ---
Acción delicada: no
Máquina: brain-env (MUDH Gateway, build) para la corrida, el render, la verificación y la medición; Actions x64 para el parche como testigo independiente
Artefactos: docs/agents/respuestas/2026-10-12-018-paga-la-tarea-de-la-mosca-la-regla-era-la-mosca-idealizada-y-la-v2-quedo-corregida.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21617
