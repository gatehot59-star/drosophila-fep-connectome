# H_ENTERA_UMBRAL · sello (respuesta 2026-10-14-050)

**Fecha:** 2026-10-16, 10:30 (America/Buenos_Aires)
**Rama:** `titan/mosca-entera-2026-10-15`. Se sella antes de escribir el instrumento: nada de esto corrió.
**Pedido:** botón `sellar_umbral_050` de Abraham (16-oct), sobre la propuesta de la 049.
**No toca:** el sello 046 (`SELLO-MOSCA-ENTERA.md`, md5 55bc4c76) ni la enmienda 048 (`ENMIENDA-048.md`, md5 022dbbdd). Los veredictos de la 049 quedan como están.

## 1. Pregunta

En la 049, SparseLTC sobre el cerebro entero reproduce el conjunto que el LIF de Shiu prende con azúcar (H_ENTERA_CONJUNTO SOSTENIDA, J 0,366) pero no MN9 (H_ENTERA_MN9 REFUTADA a radio 0,9; H_ENTERA_MN9_G1 SIN_DECIDIR, 79 de 80 nulos por debajo). El LIF prende 321 neuronas y lleva el azúcar a MN9 en 30 de 30 ensayos; la tasa con tanh deja 48.407 neuronas positivas. Pregunta: con un umbral que le dé a cada grafo el mismo presupuesto de actividad que tiene el LIF, ¿el cableado real lleva el azúcar a MN9 por encima de sus barajados?

## 2. Brazo UMB

- Dinámica: z ← (1 − t) z + t · tanh(max(0, W z + x − θ_g)), t = dt/τ. Es el brazo TASA de la 049 con la activación cortada por un umbral global θ_g. Sin compuerta líquida (la 049 la dio degenerada).
- dt 0,02; τ por `root_id` con la semilla 30 (`tau_por_root` de `liq_entera.py`); 200 pasos; ventana 151 a 200; entrada A = 1 constante en los 20 sensores de azúcar de Shiu presentes en v783.
- **Real:** la matriz de la 049 (W = signo × sinapsis [post, pre], radio 0,9).
- **Nulos:** los mismos 40 SHUF_W y 40 SHUF_G de la 049 (k 0 a 39, `default_rng([20261015, código, k])`), escalados con el factor del real (G1: 0,9 / radio crudo del real). Se eligen los G1 porque la 049 mostró que normalizar cada nulo a 0,9 le da 6 a 8 veces más ganancia por sinapsis.

## 3. Calibración de θ_g, el mismo criterio para cada grafo

- Objetivo N* = 321: el K del LIF real de la 049 (`results/mosca_entera_2026-10-15/actions_correr/lif_real.json`, md5 f6383d18a0e05efb65696175949df9fa).
- Activas(θ) = neuronas no estimuladas con r > 0 en la ventana.
- Si Activas(0) ≤ N*, θ_g = 0 y el grafo queda marcado `NO_ALCANZA` (es lo más permisivo para ese grafo).
- Si no: hi = 1, duplicado hasta 8 mientras Activas(hi) > N*; bisección de 24 pasos entre 0 y hi; θ_g = el θ más chico probado con Activas ≤ N*.
- **CALIB_REAL:** el real tiene que quedar con |Activas − 321| ≤ 32. Si no, todas las hipótesis quedan NO_MEDIDO (instrumento).
- Los nulos que no calibran dentro de ±32 se comparan igual con su θ_g y se cuentan aparte.

## 4. Lecturas

- r_MN9: r de MN9 en la ventana con el θ_g de su grafo.
- J: Jaccard entre las K = 321 de mayor r positiva (sin estimuladas, empates por índice) y S_LIF de la 049.

## 5. Hipótesis y bandas (fijadas antes de ver)

- **H_UMB_MN9:** r_MN9 real > 0 y mayor que los 40 de cada familia: SOSTENIDA. r_MN9 real ≤ 0, o 5 o más nulos de alguna familia iguales o mayores: REFUTADA. Resto: SIN_DECIDIR.
- **H_UMB_CONJUNTO:** J real contra los 40 de cada familia, mismas bandas sin la condición de signo.
- **H_UMB_GANA:** J(UMB real) − J(TASA real): ≥ +0,05 SOSTENIDA; ≤ 0 REFUTADA; resto SIN_DECIDIR.
- **Controles:** pin de datos (los md5 de la 049); CALIB_REAL; TASA_049: el mismo trabajo vuelve a correr TASA real con τ 30 y tiene que dar J = 0,3659574468 (± 1e-9) contra la misma S_LIF, o todo queda NO_MEDIDO.
- **Secundaria, no decide:** el θ_g del real aplicado fijo a los 80 nulos (como hace el LIF, que usa los mismos parámetros en todos los grafos); se reportan r_MN9 y Activas.

## 6. Lectura conjunta fijada

- **H_UMB_MN9 SOSTENIDA:** con el presupuesto de actividad del LIF, el cableado real lleva el azúcar a MN9 mejor que 80 barajados; la falla de la 049 era la no linealidad, no el cableado. Si además H_UMB_CONJUNTO es SOSTENIDA, se puede sellar la destilación (sello aparte).
- **REFUTADA con r_MN9 real = 0:** MN9 no entra entre las 321 más activas del real; un umbral sobre la tasa no alcanza y el reflejo del LIF depende de algo que la tasa no tiene (espigas, integración en el tiempo).
- **REFUTADA por nulos iguales o mayores:** el umbral lleva el azúcar a MN9 también sin el cableado real; no es específico.
- **SIN_DECIDIR:** 80 nulos no lo resuelven; no se agregan nulos después de ver.

## 7. Expectativa escrita antes de ver

MN9 en TASA vale 0,00203 contra un máximo de 0,769 entre 48.407 positivas, así que mi apuesta es que no entra entre las 321: **H_UMB_MN9 REFUTADA con r = 0 (70%)**. H_UMB_CONJUNTO SOSTENIDA (85%). H_UMB_GANA incierta (50%).

## 8. Humo sin ver la lectura sellada

La lectura de la ventana no depende de τ (es el punto fijo). Por eso el humo de la 049, con τ 99, ya mostró los números del brazo real antes de CORRER; queda declarado en la 050. Para no repetirlo, el humo de UMB corre el real con **otro estímulo** (20 neuronas no sensoriales al azar, semilla 99) y un solo nulo k 99 de cada familia: mide tiempo, memoria y convergencia de la calibración sin mostrar azúcar a MN9.

## 9. Máquina y orden

Actions (no hace falta brian2: S_LIF es la de la 049). Unas 25 simulaciones de 7,5 s por grafo, 81 grafos: unas 4 h de CPU repartidas en 8 trabajos, unos 30 min de pared (estimado, NO MEDIDO). Orden: instrumento, prueba, humo y recién después CORRER.
