# H_LIF_SHUFG · sello (respuesta 2026-10-14-054)

**Fecha:** 2026-10-16, 12:53 (America/Buenos_Aires)
**Rama:** `titan/mosca-entera-2026-10-15`. Se sella antes de escribir el instrumento: nada de esto corrió.
**Pedido:** Abraham, 16-oct 12:40, «Seal the SHUF_G LIF comparison», sobre la propuesta de la 053.
**No toca:** el sello 046 (`SELLO-MOSCA-ENTERA.md`, md5 55bc4c76), la enmienda 048 (`ENMIENDA-048.md`, md5 022dbbdd) ni el sello 050 (`SELLO-UMBRAL-050.md`, md5 680abca8). Los veredictos de la 049 y la 051 quedan como están: H_ENTERA_MN9_G1 y H_UMB_MN9 siguen SIN_DECIDIR pase lo que pase acá, y no se les agregan nulos.

## 1. Pregunta

En la 049 (G1) y en la 051 (UMB), el único de los 80 nulos que deja a MN9 por encima del real es SHUF_G k32: G1 0,00348 contra 0,00203 del real (el segundo SHUF_G es k39 con 0,0000636); UMB 0,00158 contra 0,000145 (y con el θ del real fijo, 0,00306 con 914 activas, cerca de la mediana de SHUF_G, 924). El LIF de Shiu se midió sólo contra 20 SHUF_W (en ninguno llegó a MN9) y el barajado de destinos no está en el texto principal de su paper. Pregunta: el LIF de Shiu, sin cambios, ¿lleva el azúcar a MN9 en esos mismos 40 SHUF_G, y en particular en k32? Si llega en k32, el freno es del barajado; si no llega, es de nuestra neurona de tasa.

## 2. Brazo y grafos

- **LIF_SHIU**, el mismo de la 049: `model.py` de Shiu en `91bdd1e7` (blob `5ba7083cf55bf6092967f8d9065e86cd677efed1`, md5 5886c9105b7fc9fd4a8ae8baf1b18965) sin cambios; `default_params` salvo `r_poi` = 100 Hz; los 20 sensores de azúcar presentes en v783; lectura MN9 (`720575940660219265`); ensayos de 1000 ms; `Completeness_783.csv` (md5 031a4b6e) y nuestro parquet (md5 3d802fd5), que es byte a byte el `Connectivity_783.parquet` de Shiu.
- **Real:** 30 ensayos (es el control de la sección 4).
- **Nulos:** los 40 SHUF_G de la 049 y la 051 (k 0 a 39), hechos con `nulo()` de `liq_entera.py` (md5 ae3c1a2d), `default_rng([20261015, 2, k])`: la columna postsináptica permutada entre aristas. Cada arista conserva su presináptica y su peso, así que se conservan el grado de entrada y de salida de cada neurona y el signo de cada presináptica. En el modelo de Shiu una multiarista son dos sinapsis con el mismo retardo, que suman como en la tasa; los autolazos quedan. 10 ensayos por nulo, como los SHUF_W de la 049.
- Sin escala: el LIF usa los pesos crudos (sinapsis × signo × `w_syn`), así que acá no existe la elección entre radio propio y G1.

## 3. Lecturas por grafo

- **E_MN9:** ensayos con al menos una espiga de MN9. **Llega** = E_MN9 ≥ 5 de 10, el criterio de los nulos en REPRO_SHIU (sello 046).
- **F_MN9:** tasa media de MN9 en Hz sobre los ensayos del grafo.
- **Desbocado:** un grafo con más de 10 veces las activas (neuronas con alguna espiga) del real de este trabajo.
- Descriptivas, no deciden: activas, espigas, K (no estimuladas a ≥ 1 Hz), J entre ese conjunto y la S_LIF del real de este trabajo, y el atajo en el cableado de cada grafo: n1 (aristas directas de azúcar a MN9), D1+ (su peso excitatorio) y D2+ = (W+ (W+ e)) en MN9, con W+ la parte positiva de W[post, pre] crudo y e el indicador del azúcar.

## 4. Controles

- **PIN:** blob de `model.py`, md5 de parquet y Completeness, brian2 2.10.1. Si no coinciden, aborta.
- **CTRL_REAL:** MN9 con espiga en 27 o más de los 30 ensayos reales (la parte real de REPRO_SHIU). Si falla, todo queda NO_MEDIDO.
- **NULO_MISMO:** el radio espectral crudo del grafo que lee el modelo de Shiu (releído del parquet que se le pasa) es el que registró la 049 para ese k, con tolerancia relativa 1e-6. Fuente: `results/mosca_entera_2026-10-15/actions_correr/liq_SHUF_G_k000.json` (md5 05bedf6f) y `liq_SHUF_G_k020.json` (md5 62982026); k32 = 372,81323741506026. Los 40 radios de la 049 y de la 051 ya coinciden entre sí con diferencia relativa máxima 3,1e-11. Un nulo que no coincide queda NO_MEDIDO.
- Un nulo sin resultado (trabajo caído, tiempo agotado o NULO_MISMO en rojo) es NO_MEDIDO y se cuenta aparte. Un veredicto sobre los 40 se lee sólo si no cambia con ningún valor de los que faltan; si cambiaría, queda NO_MEDIDO.

## 5. Hipótesis y bandas (fijadas antes de ver)

Las bandas son las de H_UMB_MN9: la misma vara que frenó a nuestra celda, aplicada al modelo de Shiu. Con esa vara la UMB de la 051 da 1 de 40 SHUF_G, k32, con los dos criterios de abajo (MN9 > 0 y MN9 ≥ real).

- **H_LIF_G_SHIU** (criterio de Shiu): cuántos de los 40 SHUF_G llegan. Ninguno: SOSTENIDA. 5 o más: REFUTADA. De 1 a 4: SIN_DECIDIR.
- **H_LIF_G_VARA** (nuestra vara): F_MN9 real > 0 y mayor que la de los 40: SOSTENIDA. 5 o más nulos con F_MN9 igual o mayor: REFUTADA. Resto: SIN_DECIDIR. La referencia es el real de este trabajo, no el de la 049.
- **H_LIF_K32:** k32 llega o no llega. Si k32 queda NO_MEDIDO, esta lectura queda NO_MEDIDO.
- No se agregan nulos ni ensayos después de ver.

## 6. Lectura fijada de k32 (atribuye, no cambia veredictos sellados)

- **No llega:** el atajo de k32 es de nuestra celda de tasa; el LIF no lo toma. El freno de H_UMB_MN9 es de la neurona, no del barajado.
- **Llega y está desbocado:** llega por actividad global, no por un camino; el freno es del barajado, que vuelve epiléptico a ese grafo.
- **Llega, no desbocado, con F_MN9 igual o mayor que la del real:** el atajo es del barajado y con nuestra vara frena también a Shiu.
- **Llega, no desbocado, con F_MN9 menor que la del real:** el camino está en el barajado (los dos modelos lo toman), pero el LIF lo separa del real por intensidad y nuestra celda no: lo que nos falta es contraste.
- **H_LIF_G_SHIU REFUTADA:** contra SHUF_G el LIF de Shiu es menos específico que nuestra UMB (1 de 40); SHUF_G no sirve de vara para MN9 tal como está. Cambiar el nulo es otro sello y no rescata la 051.
- Nada de esto convierte el SIN_DECIDIR de la 051 en SOSTENIDA ni habilita la destilación. Una celda con espiga o con integración en el tiempo sería otra hipótesis y otro sello.

## 7. Expectativa escrita antes de ver

En la 049 el LIF casi no se propagó en los 20 SHUF_W (41 a 59 activas contra 393, K de 12 a 33, MN9 en 0 de 10 en los 20). En G1, k32 le saca 55 veces al segundo SHUF_G, y la entrada neta de MN9 en k32 da lo mismo en las tres lecturas: 0,00348 en G1, 0,00158 + θ 0,00190 en UMB y 0,00306 + θ 0,00042 con el θ del real. Con el factor G1 (0,000416) y el azúcar en tanh(1) = 0,76, eso tiene la forma de una entrada directa desde el azúcar de unas 11 sinapsis en total. En la tasa alcanza para superar al real; en el LIF no alcanza para disparar: en el `model.py` de Shiu el azúcar dispara a la tasa de su Poisson (100 Hz, sin refractario) y 11 sinapsis de 0,275 mV con tau 5 ms dan un promedio de 1,5 mV de los 7 que separan el reposo (−52 mV) del umbral (−45 mV). Apuesta: **k32 no llega (80%)**; H_LIF_G_SHIU SOSTENIDA (75%; SIN_DECIDIR 20%, REFUTADA 5%); H_LIF_G_VARA SOSTENIDA (90%); CTRL_REAL PASA (95%); NULO_MISMO PASA (95%). Predicción descriptiva, falsable con n1: k32 tiene al menos una arista directa de azúcar a MN9 (80%) y es el único de los 40 que la tiene (65%). El riesgo contrario: SHUF_G es más excitable que SHUF_W (en la 051, con el θ del real fijo, prendió una mediana de 924 contra 134) y un grafo desbocado puede llevar a MN9 sin atajo.

## 8. Humo sin ver la lectura sellada

El real ya es público (049: 30 de 30, 61,63 Hz), así que no hay nada que ocultar de ese brazo. El humo corre el real con 2 ensayos y un solo nulo SHUF_G k 99 (fuera de 0 a 39) con 10 ensayos, como uno de CORRER, y coteja NULO_MISMO contra el radio que registró el humo de la 051 para ese k (`results/mosca_umbral_2026-10-16_humo/actions_humo/umb_SHUF_G_k099.json`, md5 dddfaeb2, 319,61856064512546). Mide tiempo y memoria de un SHUF_G en el LIF; sus números no valen como resultado. Ninguno de los 40 nulos de CORRER corre antes de CORRER.

## 9. Máquina, costo y orden

- Actions (ubuntu-latest, 4 vCPU, 16 GB). brain-env no tiene brian2 y está ocupada con la réplica de H_LECTOR.
- Versiones fijadas, las que tuvo la 049: Brian2 2.10.1, Cython 3.1.3, joblib 1.6.0, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, pyarrow 25.0.1, Python 3.12.
- Costo: en la 049 cada SHUF_W de 10 ensayos tardó de 92 a 194 s con 3 procesos (2.919 s los 20) y el real de 30, 480 s. Si SHUF_G cuesta lo mismo, los 40 son unas 1,6 h de trabajo, repartidas en 8 trabajos de 5 nulos, unos 15 min de pared (estimado, NO MEDIDO; un SHUF_G desbocado puede costar mucho más). La partición en trabajos es logística y no es parte del sello: se fija con el humo, antes de CORRER.
- Instrumento previsto: archivos nuevos (`lif_shufg.py`, su agregado y su prueba) que importan `lif_shiu.py` (md5 88c8459e) y `liq_entera.py` sin tocarlos. La prueba tiene que mostrar que cada control puede dar rojo.
- Orden: este sello, después instrumento con prueba y humo, y recién después CORRER. Cada paso con su respuesta.

## 10. Lo que este sello no cubre

Los SHUF_W 20 a 39 en el LIF (la 049 corrió 0 a 19), otros estímulos de Shiu, el nulo exacto de sus suplementos (no leídos) y la destilación.
