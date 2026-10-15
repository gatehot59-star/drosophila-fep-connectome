# SELLO H_TAU_LIBRE (respuesta 2026-10-14-039)

Rama `titan/taulibre-2026-10-15`, creada desde `titan/lector-2026-10-15` en `8d305e9` (resultados de H_LECTOR). Sellado antes de escribir ningun script: nada de lo que decide H_TAU_LIBRE se midio.

Aprobado por Abraham el 15-oct a las 18:41 (America/Buenos_Aires), ClickKit `sellar_control_tau_039`.

## Por que

H_LECTOR_CABLEADO salio SOSTENIDA en Actions (038): con el lector L, la red real le gano a los 40 nulos SL y T en c2 y c5 (deltas +0,0337 a +0,1194, p = 1/41 en las cuatro). Pero la tau de la red real (semilla 10) la eligio H_TAU entre las semillas 10 a 19 por validacion cruzada sobre la red real, y los nulos la heredaron sin una eleccion propia. Esa eleccion vale: en los json de H_TAU, con las lineas sin entrenar, la elegida le saca a la peor de 2,2 a 4,2 puntos en prueba y a la mediana de validacion de 0,6 a 1,0. El delta mas chico de H_LECTOR (SL c2, +3,4 puntos) es del mismo orden. Nadie midio cuanto pesa la eleccion con L.

## Hipotesis

- **H_TAU_LIBRE:** con tau que nadie eligio, la red real sigue superando a sus nulos SL y T por mas de 1 punto, en c2 y c5, con el mismo lector L.

## Diseno

- Instrumento: el de H_LECTOR (`tools/lector/lector_mosca.py`, md5 5b7fb79e55ab2b695c9751698c8205c4) importado sin cambios; solo cambia la semilla de tau. El script nuevo va en `tools/taulibre/`.
- Tau fresca: semillas 20 a 29 con `f2.tau_por_root(ids, s)`. Revisado en `8d305e9`: los factoriales usaron 0 a 9, H_TAU 10 a 19 y la entrada por tipos 1 y 2. No halle uso de 20 a 29; un control lo vuelve a chequear.
- Celdas c2 (A 0,3, ruido 0,15) y c5 (A 0,6, ruido 0,45), las de los nulos de H_LECTOR. Solo la prueba 12 (2.000 ensayos, ruido 1012). Entrenamiento: los 2.400 ensayos de siempre.
- Real: la red R2 con cada tau s de 20 a 29 en c2 y c5 (20 corridas). En cada una, L se entrena con la misma validacion cruzada de H_LECTOR.
- Nulos: los mismos 40 por familia de H_LECTOR (SL con `default_rng([7, k])`, T con `default_rng([11, k])`, k = 0 a 39). El nulo k usa la tau de semilla 20 + (k mod 10): cada semilla de tau la usan 4 nulos por familia y celda. L se reentrena en cada nulo.
- Nadie elige tau en ningun brazo: ni real ni nulos.

## Estadistica (decide)

- Por familia f y celda c, cada nulo se compara con la red real que tiene su misma tau: r(k) = WL_real(c, 20 + k mod 10).
- p(f, c) = (1 + numero de nulos con WL_nulo(k) >= r(k)) / 41.
- delta(f, c) = media sobre k de [r(k) - WL_nulo(k)].
- SUPERA(f, c) si p(f, c) <= 0,05 y delta(f, c) > 0,01.
- **H_TAU_LIBRE:** SOSTENIDA si hay SUPERA en las 4 combinaciones (interseccion-union, cada una al 5% sin correccion). REFUTADA si en alguna delta(f, c) < 0,01 o p(f, c) > 0,10. SIN_DECIDIR en otro caso.
- Si falla cualquier control: INVALIDO, y los descriptivos no se citan.

## Descriptivos (no deciden)

- Rango de WL_real sobre las 10 taus frescas por celda, y en que lugar caeria la tau 10 de H_LECTOR (0,9910 en c2 y 0,9930 en c5, prueba 12). Si la 10 queda arriba de las 10 frescas, la eleccion pesaba.
- Delta por semilla de tau (real menos la media de sus 4 nulos).

## Controles (si falla cualquiera: INVALIDO)

- **PIN:** md5 de `lector_mosca.py`, `factorial2_mosca.py`, `nulos_r2.py`, del sello de H_LECTOR y de los datos de entrada, iguales a los de H_LECTOR.
- **REPRO_LECTOR:** la red real con tau 10 en c2, prueba 12, reproduce el WL real de H_LECTOR (`nulos_SL_c2_k000.json`) y sus predicciones caracter por caracter.
- **NULOS_IGUAL_LECTOR:** para cada k, los destinos cambiados (SL) y los tipos cambiados (T) son iguales a los de los json de H_LECTOR: el nulo es el mismo grafo, solo cambia la tau.
- **TAU_FRESCA:** ninguna semilla de 20 a 29 aparece como tau en los json de H_TAU, del factorial 3 ni de H_LECTOR.
- **GUARDA_FUGA, CONTROL_NEGATIVO y NULOS_VALIDOS:** los de H_LECTOR, por corrida.
- **PLAN_COMPLETO:** 20 corridas reales y 160 nulos, sin faltantes.

## Limitaciones declaradas antes de correr

1. Una sola prueba (12) y dos celdas, como los nulos de H_LECTOR. Con 40 nulos el p minimo es 1/41.
2. El p apareado no es una permutacion exacta: cada nulo se compara con una sola red real. Es un criterio de conteo, conservador si la tau mueve poco al real.
3. 10 taus frescas: cubren la variacion entre taus al azar, no todas las posibles.
4. La primaria de H_LECTOR (CERCA y PAGA) no se toca: usa la tau 10 y este control no la revisa.

## Expectativa declarada

Con deltas de +11 a +12 puntos, c5 probablemente sobrevive. c2 (+3,4 en SL y +4,5 en T) queda abierta: la eleccion de tau pesaba de 2 a 4 puntos con las lineas sin entrenar. El sello no esta escrito para que gane la mosca.

## Maquina y disparo

- Actions x64 decide: 4 trabajos de reales (5 corridas cada uno), 16 de nulos (10 cada uno) y el agregado; 20 trabajos, justo el tope de simultaneos. Costo estimado desde H_LECTOR: unos 10 minutos por corrida, unas 2 horas en total.
- Humo ciego antes: controles a tamano completo (REPRO_LECTOR, NULOS_IGUAL_LECTOR, TAU_FRESCA) y rutas con 600 y 200 ensayos en la semilla 99, sin imprimir aciertos.
- La corrida completa se dispara solo con el si de Abraham, con `results/taulibre_2026-10-15/CORRER` en esta rama.
