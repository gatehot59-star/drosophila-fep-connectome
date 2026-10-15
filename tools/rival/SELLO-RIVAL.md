# SELLO H_RIVAL y H_TAU_JUSTO (2026-10-14-032)

**Sellado:** 2026-10-15, 00:37 (America/Buenos_Aires), antes de escribir cualquier script de H_RIVAL. Este commit trae solo este archivo. El instrumento (`tools/rival/rival_mosca.py`, su agregador y sus pruebas) entra en un commit posterior; cualquier diferencia con lo que dice aca se declara en la respuesta que lo traiga, y este archivo no se edita.

**Autorizado por:** Abraham, 15-oct 00:17 («Sellá H_RIVAL en un commit aparte y anterior a cualquier script»).

**Base:** rama `titan/htau-nucleo-banc-2026-10-14` (2d4dbfb), que trae los modulos sellados y los resultados de H_TAU y del factorial 3.

## Lo que pidio Abraham y donde queda

| Pedido (15-oct 00:17) | Donde queda en este sello |
|---|---|
| Fijar la metrica antes de ver nada | Metrica: acierto por semilla de prueba |
| Presupuesto de CV: 10 candidatas, igual que tau | Rivales y presupuesto: 10 candidatas cada uno, 5 pliegues modulo 5 |
| Ridge reproduce 0,9935 en `tarea_mosca`: control positivo | Controles: CONTROL_RIDGE_015 |
| Declarar el umbral de 1 punto | Comparacion primaria: margen 0,01 |
| La semilla como unidad, o 10 semillas de tau y limitacion declarada | Unidad: la semilla; Limitaciones 1 y 2 |

## Lo que se vio antes de sellar

- Nadie corrio todavia un rival entrenado sobre las 564 entradas por root del banco R2: los factoriales no tienen ridge (0 lineas, verificado en la 2026-10-14-031).
- Lo unico visto de un rival entrenado es el ridge de la 015 sobre las entradas crudas del motivo (`results/tarea_mosca_2026-10-12/completa.log`, md5 ad8c94b47350b5473b13848150047ab4): 0,9935, 0,9595, 0,9935, 0,9575, 0,9940 y 0,9590 en las celdas c0 a c5. Es el control positivo, no un resultado de H_RIVAL.
- De W y de la regla ya esta publicado: H_TAU (W con tau elegida contra su regla, pruebas 12 a 21) y el factorial 3 (tau 0 a 9, pruebas 2 a 11).
- Expectativa declarada: si el ridge repite algo cerca de 0,99 con las 564 entradas, H_RIVAL sale REFUTADA. El sello no esta escrito para que gane W.

## Pregunta

La red de la mosca con tau elegida por validacion (W, la de H_TAU), le gana por mas de 1 punto de acierto a rivales entrenados con el mismo presupuesto de eleccion, las mismas entradas y los mismos ensayos?

- **H_RIVAL:** W supera por mas de 1 punto a los tres rivales.
- **H_TAU_JUSTO:** W supera por mas de 1 punto a la regla con constantes de tiempo elegidas (REGLA_TAU). Si no, la ventaja de W sobre su regla en H_TAU se explica por integrar en el tiempo, no por el cableado.

## Datos (los de H_TAU, sin cambios)

- Sujeto: `f2.sujeto(conn, annot, "R2", "CON")`, 33.489 neuronas, 4.031.897 aristas, 564 entradas.
- Entrenamiento: `tm.generar(2400, 1)`, ruido `f2.ruido_por_root(ids[:564], 2400, 101)`.
- Prueba primaria: semillas 12 a 21, `tm.generar(2000, p)`, ruido de semilla 1000 + p. Secundaria: semillas 2 a 11, igual.
- Celdas: A en {0; 0,3; 0,6} por ruido en {0,15; 0,45}, en el orden de `f2.CELDAS` (c0 a c5).
- Entrada de los rivales entrenados: X = drive[:, :, chan] + s * Z, 40 pasos por 564 entradas, 22.560 rasgos por ensayo: lo mismo que recibe W. El estado (posada o en vuelo) es conocido, como en W y en la regla: un modelo por estado con las clases de `tm.CLASES` (vuelo 0, 2, 3, 4; posada 0, 1).

## Metrica

acc = fraccion de aciertos sobre los 2.000 ensayos de cada semilla de prueba (20 condiciones balanceadas, 100 ensayos cada una), la misma que W en H_TAU. No hay otra metrica primaria.

## Rivales y presupuesto: 10 candidatas cada uno, como tau

Eleccion en los tres: validacion cruzada de 5 pliegues sobre los 2.400 ensayos de entrenamiento, pliegue = indice del ensayo modulo 5, como H_TAU. Lo que se ajusta (umbrales, pesos, estandarizacion) se ajusta en 4 pliegues y el acierto se mide en el quinto; el puntaje de la candidata es el acierto medio de los 5. La elegida se reajusta con los 2.400 ensayos y recien ahi ve la prueba.

1. **RIDGE.** Rasgos estandarizados con media y desvio del conjunto de ajuste (desvio + 1e-6), objetivo one-hot, intercepto sin penalizar, penalidad lambda * n como `ept._ridge_fit`, resuelto en forma dual (22.560 rasgos contra unos 1.200 ensayos por estado). Candidatas: lambda en {1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 1e2, 1e3, 1e4, 1e5}; un solo lambda para los dos estados, porque tau tambien es una sola para los dos. Empate: el lambda mas grande.
2. **MLP.** El de la 005 sin cambios (`ept.mlp_mux`): 32 ocultas tanh, Adam lr 1e-2, weight decay 1e-4, lote 256, 300 iteraciones, float32, estandarizacion por estado. Candidatas: semillas 0 a 9 (`torch.manual_seed(semilla)`, lotes de `default_rng(5000 + semilla)`). Empate: la semilla mas chica.
3. **REGLA_TAU.** La regla propia de H_TAU (`lc`, `tm.lineas`, `tm.umbrales`, `tm.carrera`, FA 0,05) con cada uno de los 6 canales de `lc` pasado antes por un integrador con fuga: z(-1) = 0; z(t) = (1 - t_k) z(t-1) + t_k u(t); t_k = 0,02 / tau_k; tau_k = 0,06 + 0,12 u_k; u_k = `default_rng([semilla, k]).random()`, k = 0 a 5 (la ley de `f2.tau_por_root`, con el canal en lugar del root_id). Candidatas: semillas 10 a 19. Empate: la mas chica.

W no se recalcula: se leen `W_elegida` y `pred_elegida` de los json de H_TAU (primaria) y `W` y `pred_W` de los 60 json `factorial2_R2_CON_TASA_t{tau}c{celda}` del factorial 3 (secundaria).

## Comparacion primaria (decide)

- Unidad: la semilla de prueba. d(r, c, p) = W_elegida(c, p) - acc_r(c, p), con p = 12 a 21 y c = c0 a c5.
- Estadistico: D_r = media de d sobre las 6 celdas y las 10 semillas.
- IC: bootstrap de las 10 semillas de prueba (el mismo remuestreo para las 6 celdas y los 3 rivales), B = 20.000, semilla 2031, percentiles, bilateral al 1 - 0,10/3: el 90% con Bonferroni por 3 rivales, percentiles 1,667 y 98,333.
- **Margen declarado: 1 punto (0,01).**
- Etiqueta por rival: SUPERA_POR_MARGEN si el piso del IC es mayor que 0,01; NO_SUPERA si el techo es menor que 0,01; SIN_DECIDIR en otro caso. Descriptivo aparte: PIERDE si el techo es menor que 0.

## Veredictos

- **H_RIVAL:** SOSTENIDA si W sale SUPERA_POR_MARGEN contra los tres; REFUTADA si sale NO_SUPERA contra al menos uno; SIN_DECIDIR en otro caso.
- **H_TAU_JUSTO:** la etiqueta de REGLA_TAU sola: SUPERA_POR_MARGEN da SOSTENIDA, NO_SUPERA da REFUTADA, SIN_DECIDIR da SIN_DECIDIR.
- Si falla cualquier control, las dos son INVALIDO y sus descriptivos no se citan (regla de la 2026-10-14-031).

## Secundaria (declarada, no decide)

W del factorial 3 (tau 0 a 9: redes al azar, sin eleccion) contra los mismos rivales en las pruebas 2 a 11. D2_r = media sobre celdas, semillas de tau y semillas de prueba; bootstrap en dos vias (semillas de tau y semillas de prueba remuestreadas por separado), B = 20.000, semilla 2032, mismo nivel y misma regla de etiquetas, solo descriptiva.

## Limitaciones declaradas antes de correr

1. La primaria tiene una sola red elegida por celda: su IC cubre la variacion entre semillas de prueba, no entre redes. Es la salvedad de H_TAU y sigue en pie.
2. La secundaria cubre la variacion entre redes al azar con 10 semillas de tau. Con 30 el IC seria mas fiable; no se corre ahora por costo: en H_TAU cada red tardo unos 5 minutos en entrenamiento y unos 4,5 por semilla de prueba en Actions (CANDIDATA 317 s; CORRIDA 531 s con dos redes; `htau_c0.log`), asi que 20 semillas mas son unas 16 horas por celda. Si H_TAU_JUSTO sale SIN_DECIDIR, el paso siguiente es sellar la extension a 30 semillas (tau 20 a 39), no leer la estimacion puntual.
3. W elige entre 10 candidatas solo tau y ajusta 6 umbrales; los rivales ajustan miles de pesos. Es la comparacion pedida: el presupuesto de eleccion es el mismo, la capacidad no.
4. Ninguna comparacion por ensayo decide: los McNemar quedan fuera.

## Controles (si falla cualquiera: INVALIDO)

- **PIN:** md5 de conn (3d802fd542b5d18570ba1ba0bb0abed9), annot (719904abad876c68ace1b5690c9b9b63), `factorial2_mosca.py` (798a824cd47808155fa12adb9e652dac), `tarea_mosca.py` (40d64e074d9163753439307c5be4ac5e), `entrada_por_tipos.py` (e060c4bffb685aa550dadc19eda3dd02), `escape_aterrizaje_dbc3.py` (4d40477d87406c31672acfb6e6e8f5a2), `htau_mosca.py` (2006cfef6eaffc023086fd35fbe20f64); json de H_TAU c0 4e796c3f7b4aae9de395dcfdf0a37b31, c1 0e9f41ab1b28d9ab5a191f3e4907d2b0, c2 2cbab449f48cb4cd0102d8ba2f4f812b, c3 aca01a833db117cf96c755168ae56834, c4 7849f2b656097c42b5fe0b714f78e566, c5 0ef2ee1146f3829cafc985619c992104; `MD5SUMS.txt` del factorial 3 (3fb0f772ecf2659760697ab38616a2b3) y cada uno de los 60 json contra esa lista; `completa.log` de la 015 (ad8c94b47350b5473b13848150047ab4).
- **CONTROL_RIDGE_015 (positivo):** el ridge nuevo, con el protocolo de la 015 (`ept.LAMBDAS`, 80/20 en el orden de los ensayos, empate al lambda mas grande, un lambda por estado) sobre las entradas crudas del motivo de la 015 (`tm.construir`; entrenamiento `generar(2400, 1)` con ruido 101; prueba `generar(2000, 2)` con ruido 102), reproduce `ridge_crudo_entrenado` de `completa.log` en las 6 celdas con una diferencia de 0,0010 o menos (2 de 2.000 ensayos): 0,9935, 0,9595, 0,9935, 0,9575, 0,9940 y 0,9590. Si no llega, el rival esta roto y nada de H_RIVAL vale.
- **CONTROL_MLP_005:** en c0, pliegue 0, semilla 0, las predicciones del envoltorio del MLP son identicas a las de `ept.mlp_mux` con los mismos datos.
- **REPRO_REGLA:** la regla propia recalculada sobre los ensayos regenerados da exactamente `pred_regla_propia`: 60 de 60 en H_TAU (6 celdas por pruebas 12 a 21) y 60 de 60 en el factorial 3 (6 celdas por pruebas 2 a 11, json de tau 0).
- **REPRO_W:** el acierto recalculado desde `pred_elegida` y `pred_W` contra las etiquetas regeneradas da exactamente `W_elegida` y `W` (60 y 600 corridas). Es lo que prueba que W y los rivales quedan pareados ensayo por ensayo.
- **REGLA_TAU_NULA:** con t_k = 1 el integrador devuelve la regla sin cambios: predicciones identicas a la regla propia en la prueba 12, en las 6 celdas.
- **CONTROL_NEGATIVO:** ridge con las etiquetas de entrenamiento permutadas dentro de cada estado (semilla 2033), lambda elegido igual, en la prueba 12: acierto de azar + 0,05 o menos en las 6 celdas (azar = clase mayoritaria por estado en la prueba, cerca de 0,50).
- **GUARDA_FUGA:** semillas de prueba (2 a 21) y de ruido de prueba (1002 a 1021) distintas de las de entrenamiento (1 y 101); la estandarizacion, los pesos y los umbrales de cada pliegue salen solo de sus 4 pliegues de ajuste.

## Maquinas

- Actions x64 decide: una tarea por celda (6) y el agregado, que commitea `results/rival_2026-10-15/`.
- brain-env replica las 6 celdas con los mismos comandos; su duracion se mide en el humo, antes de disparar.
- Cotejo: RIDGE y REGLA_TAU (float64) deberian dar las mismas lineas; el MLP (float32, otra CPU) puede diferir en algun ensayo y se reporta la diferencia. Si una etiqueta por rival difiere entre maquinas, esa etiqueta pasa a SIN_DECIDIR (NO_SE_REPLICA) y los veredictos se recalculan con eso.

## Humo y disparo

- Humo ciego: corre los controles a tamano completo y recorre las rutas de los tres rivales con 600 ensayos de entrenamiento y 200 de prueba en una semilla fuera del analisis (99), sin imprimir aciertos de rivales.
- La corrida completa se dispara solo con el si de Abraham, con `results/rival_2026-10-15/CORRER` en esta rama.

## Salidas

`results/rival_2026-10-15/`: `rival_c0` a `rival_c5` (.log y .json: candidatas, puntajes de validacion, elegidas, aciertos y predicciones por semilla), `controles.log`, `agregado.log` y `agregado.json`, `versiones.txt` y `MD5SUMS.txt`. Codigo de salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.

--- METODO PROMETEO ---
Rol: investigacion (pre-registro). Delicado: no, documento solo.
Maquina: brain-env, lectura de los json, logs y modulos sellados en la rama de H_TAU (2d4dbfb); ningun rival corrido.
Artefactos: este sello en `titan/rival-2026-10-15`; respuesta `docs/agents/respuestas/2026-10-14-032-h-rival-sellado.md` en main; Doc de ClickUp con la 032.
