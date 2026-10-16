# SELLO · H_MOSCA_ENTERA (respuesta 2026-10-14-046)

**Fecha:** 2026-10-15, 23:20 (America/Buenos_Aires). **Pedido:** Abraham, ClickKit `sellar_mosca_entera_046`, 23:15. Sellado antes de escribir una línea de instrumento. Nada corrido. (El primer commit de este sello, `863d2a0`, decía 23:40 por error: estaba adelantado.)

## Pregunta

¿La neurona líquida de nuestro pipeline, corriendo sobre el cerebro entero de FlyWire v783 sin recorte y sin lector entrenado, reproduce lo que el LIF de Shiu et al. 2024 (Nature, DOI 10.1038/s41586-024-07763-9) predijo y validó con optogenética (los sensores de azúcar activan la motora MN9), y lo hace por el cableado y no por la estadística del grafo?

## Datos y pines

- `connectivity.parquet`: md5 `3d802fd542b5d18570ba1ba0bb0abed9`, 100.804.642 bytes, git blob `d386555d1a5f40ebfa1380bcb05b1fab044855fd`. Es byte a byte el `Connectivity_783.parquet` del repo de Shiu (`philshiu/Drosophila_brain_model`, commit `91bdd1e7dcf193f3e7ca5a8933497fcef63b7960`, mismo blob). [MEDIDO 15-oct en brain-env con `git hash-object`; log en `results/mosca_entera_2026-10-15/pines.log`.]
- `annotations.tsv`: md5 `719904abad876c68ace1b5690c9b9b63`.
- `Completeness_783.csv` del mismo commit de Shiu (blob `b5a26b82b69a3c2e7fd99cd6810c36fc8f0e492b`); su md5 lo fija el instrumento.
- Estímulo: los 21 sensores de azúcar del `example.ipynb` de Shiu (ids de v630). 20 existen en v783, en el parquet y en las anotaciones (sensory, gustatory, sugar/water, LB3). Falta `720575940620900446`: se estimulan los 20. [MEDIDO, `tools/mosca_entera/ids_shiu.py` md5 `c82a835586846568cb35e1f1a5e9b14b`.]
- Lectura: MN9 = `720575940660219265` (id del notebook de Shiu). Existe en v783: motor, brain_motor_neuron, ingestion_motor_neuron, cell_type CB0701, side right.
- Declarado y no corregido: el notebook dice «right hemisphere» y las anotaciones v783 marcan side left en los 20.

## Brazos

1. **LIF_SHIU:** `model.py` de Shiu en `91bdd1e7` (blob `5ba7083cf55bf6092967f8d9065e86cd677efed1`), sin cambios. `default_params` salvo `r_poi` = 100 Hz. 30 ensayos de 1000 ms. `Completeness_783.csv` más nuestro parquet.
2. **LIQ:** la celda de `tools/factorial2/factorial2_mosca.py` (md5 `798a824cd47808155fa12adb9e652dac`, rama de H_LECTOR en `8d305e9`) con `liq=True`: z ← (1 − θ) z + θ tanh(u), θ = min(1, (DT/τ)(1 + G_LIQ |u|)), DT 0,02, G_LIQ 1,0. W = `Excitatory x Connectivity` del parquet (W[post, pre]), escalada a radio espectral 0,9 (el RHO de la 003). τ por root_id = 0,06 + 0,12 U con semillas frescas 30 a 39 (las 0 a 9, 10 a 19 y 20 a 29 ya se usaron). Entrada: u += 1,0 en los 20 de azúcar en cada paso. T = 200 pasos, sin ruido, sin lector entrenado. Respuesta r_i = media de z_i en los pasos 151 a 200.
3. **TASA:** igual a LIQ con `liq=False` (θ = DT/τ fijo), mismos τ.
4. **PROX (rival sin dinámica):** s_i = Σ de k = 1 a 4 de 0,5^k (|W|^k e)_i, con |W| el valor absoluto de la W escalada y e el indicador de los 20 estimulados. Sólo cableado: sin signo y sin tiempo.

## Nulos

- **SHUF_W** (el de Shiu): permutar los valores de `Excitatory x Connectivity` entre las aristas existentes. Conserva topología y distribución de pesos.
- **SHUF_G:** permutar la columna postsináptica entre aristas, cada una con su peso. Conserva el grado de entrada y de salida de cada neurona; puede crear autolazos y multiaristas (se suman).
- En LIF: 20 SHUF_W de 10 ensayos cada uno (semillas 0 a 19).
- En LIQ: 40 SHUF_W y 40 SHUF_G (semillas 0 a 39 por tipo), con τ semilla 30, cada uno re-escalado a radio 0,9.

## Conjunto de referencia

S_LIF = neuronas no estimuladas con tasa media ≥ 1 Hz en los 30 ensayos reales del LIF. K = |S_LIF|. En cada brazo y cada nulo se toman las K neuronas no estimuladas de mayor respuesta (r_i en LIQ y TASA, s_i en PROX) y J = Jaccard con S_LIF.

## Controles del instrumento

- **REPRO_SHIU:** PASA si MN9 dispara al menos una espiga en 27 o más de los 30 ensayos reales, y de los 20 SHUF_W a lo sumo 2 tienen MN9 con espigas en 5 o más de sus 10 ensayos. Si FALLA, la vara no está: las H_ENTERA quedan NO MEDIDO.
- **K_SANO:** si K < 10 o K > 5.000, J no se interpreta.
- **PIN:** md5 de parquet, anotaciones y Completeness al arrancar; si no coinciden, aborta.

## Hipótesis

- **H_ENTERA_MN9:** con el cableado real, r_MN9 (LIQ, τ 30) es mayor que 0 y supera a los 40 SHUF_W y a los 40 SHUF_G. SOSTENIDA: supera a los 40 de cada nulo (p = 1/41 en los dos). REFUTADA: r_MN9 ≤ 0, o 5 o más nulos de algún tipo la igualan o superan. SIN_DECIDIR: el resto.
- **H_ENTERA_CONJUNTO:** J (LIQ, τ 30) supera a los 40 de cada nulo. Mismas bandas que MN9 (sin la condición de signo).
- **H_ENTERA_RIVAL:** J (LIQ, τ 30) − J (PROX). SOSTENIDA ≥ +0,05; REFUTADA ≤ 0; SIN_DECIDIR entre las dos.
- **H_ENTERA_LIQ:** mediana sobre τ 30 a 39 de J (LIQ) − J (TASA). SOSTENIDA ≥ +0,02; REFUTADA ≤ 0; SIN_DECIDIR entre las dos.
- Descriptivo: J (LIQ) y r_MN9 en las 10 semillas de τ.

## Lo que este sello no cubre

- La destilación (subgrafo mínimo): se sella aparte y sólo si H_ENTERA_MN9 y H_ENTERA_CONJUNTO salen SOSTENIDAS.
- Nulo regional, las otras pruebas de Shiu (agua, amargo, aseo), validación contra registros, comparación con Eon.

## Riesgos declarados antes de correr

- La normalización a radio 0,9 sobre 138.639 neuronas puede dejar muy chica la señal en MN9. Si r_MN9 ≤ 0 o se ahoga, es REFUTADA para esta neurona y esta escala; RHO no se re-ajusta después de ver.
- tanh tiene signo y la LIF no: J compara conjuntos por ranking de respuesta positiva, no por tasa.
- S_LIF depende del umbral de 1 Hz, fijado acá.
- Expectativa honesta, no hipótesis: MN9 probablemente SOSTENIDA contra SHUF_W, como en Shiu, y dudosa contra SHUF_G; RIVAL probablemente SIN_DECIDIR o REFUTADA, porque la proximidad en el grafo puede explicar casi todo el conjunto.

## Máquina y orden

- Actions (ubuntu-latest). brain-env no tiene brian2 y está ocupada con la réplica de H_LECTOR. Kaggle no.
- Orden: este sello, después instrumento con prueba y humo, después CORRER y agregado. Cada paso con su respuesta.
