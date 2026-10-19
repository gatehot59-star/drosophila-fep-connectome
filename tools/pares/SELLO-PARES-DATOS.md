# SELLO H_PARES_DATOS (respuesta 2026-10-14-059)

Rama `titan/pares-datos-2026-10-18`, creada desde `titan/taulibre-2026-10-15` en `e7ada46` (resultados de H_TAU_LIBRE). Sellado antes de escribir ningun script de H_PARES_DATOS: nada de lo que decide se midio. Este commit trae solo este archivo; el instrumento entra en un commit posterior, y cualquier diferencia con lo que dice aca se declara en la respuesta que lo traiga. Este archivo no se edita.

**Pedido:** Abraham, 18-oct 22:30 (America/Buenos_Aires), en el chat: «Sellá H_PARES_DATOS y ejecutá la curva». La propuesta sin sellar esta en la respuesta 2026-10-14-058, seccion 8.

## Por que

En H_RIVAL la mosca se comparo contra un techo: un ridge sobre las 22.560 entradas crudas, entrenado con 2.400 ensayos etiquetados. Lo que queremos tomar de la mosca es otra cosa: que ande con pocos ensayos etiquetados, y que su embudo de 6 descendentes (240 rasgos) comprima mejor que un embudo artificial del mismo ancho. Esta curva lo mide contra sus pares, con el mismo lector y los mismos ensayos.

## Lo que se vio antes de sellar

- H_TAU_LIBRE (Actions): con L y los 2.400 ensayos, la red real con las taus 20 a 29 acierta de 0,9930 a 0,9955 en c2 y de 0,9940 a 0,9955 en c5 (prueba 12). Es el punto n = 2.400 de MOSCA_L, y queda como control.
- H_RIVAL: el RIDGE crudo con los 2.400 ensayos acierta 0,9995 en c2, prueba 12 (log de H_LECTOR), con lambda 10 en c2 y en c5. Es el punto n = 2.400 de CRUDO, y queda como control.
- W con la tau 10 elegida: de 0,9413 a 0,9467 en las 6 celdas (pruebas 12 a 21). Nadie midio W con las taus 20 a 29, ni ningun brazo con menos de 2.400 ensayos etiquetados.
- Composicion del entrenamiento (`tm.generar(2400, 1)`): 1.200 ensayos en vuelo (clase 0: 240; 2: 480; 3: 240; 4: 240) y 1.200 posada (0: 720; 1: 480); 960 sin evento. En la repeticion 0, el subconjunto de 6 tiene 2 en vuelo y 4 posada. Se miro para disenar la guarda de estados vacios; no se miro ningun acierto.

## Brazos

Todos con la red R2 CON TASA (33.489 neuronas, 4.031.897 aristas, 564 entradas), las celdas c2 (A 0,3, ruido 0,15) y c5 (A 0,6, ruido 0,45), el entrenamiento `tm.generar(2400, 1)` con ruido 101 y la prueba 12 (2.000 ensayos, ruido 1012), como H_TAU_LIBRE. Estado conocido, como siempre.

- **W (la mosca sin ejemplos de accion):** las trazas de las 6 descendentes con tau t (`f2.tau_por_root(ids, t)`, t = 20 a 29, las de H_TAU_LIBRE: nadie las eligio), leidas con `tm.lineas`, `tm.umbrales` y `tm.carrera` sin cambios. Los 6 umbrales salen de los 960 ensayos sin evento del entrenamiento (cuantil 95); ningun ejemplo de accion.
- **MOSCA_L (la mosca con lector):** L sobre esas mismas trazas (40 pasos por 6, 240 rasgos), con n ensayos etiquetados.
- **CRUDO:** L sobre las 564 entradas crudas por 40 pasos (22.560 rasgos), con n ensayos etiquetados. Con n = 2.400 es el RIDGE de H_RIVAL.
- **PCA_L:** L sobre las 240 primeras componentes principales de las entradas crudas. La PCA se ajusta en cada celda con los 2.400 ensayos de entrenamiento sin etiquetas (centrada, sin escalar), y la prueba se proyecta con esa misma PCA.
- **PROY_L:** L sobre una proyeccion aleatoria de las entradas crudas a 240 rasgos: matriz gaussiana de 22.560 por 240 con `default_rng([2061, k])`, k = 0 a 9 (10 matrices, tantas como taus de la mosca).

L es el lector de H_LECTOR y H_TAU_LIBRE sin cambios (el RIDGE de H_RIVAL: rasgos estandarizados con el conjunto de ajuste, 10 lambdas, 5 pliegues por indice modulo 5, un lambda para los dos estados, empate al mas grande, un modelo por estado). Una sola guarda nueva: si un estado no tiene ensayos en el conjunto de ajuste de un pliegue o del reajuste, sus ensayos se predicen como clase 0 (nada). Con ensayos de los dos estados, la cuenta es la misma linea por linea (control L_IGUAL).

## Curva

- n = 6, 12, 24, 48, 96, 192, 384, 768 y 2.400 ensayos etiquetados; W es el punto de 0 ejemplos de accion.
- Repeticiones r = 0 a 19: perm(r) = `default_rng([2059, r]).permutation(2400)`, y el subconjunto de n es `sort(perm(r)[:n])`. Son anidados (el de 6 esta dentro del de 12, y asi) y son los mismos para todos los brazos, celdas y taus. En n = 2.400 hay un solo subconjunto: todos.
- La validacion cruzada y el reajuste de L ocurren solo dentro del subconjunto.

## Hipotesis

Margen declarado: 1 punto (0,01). Curva baja: n de 6 a 768 (8 puntos); n = 2.400 no entra en las medias.

- **H_DATOS_EMBUDO:** con el mismo L y los mismos ensayos etiquetados, el embudo de la mosca (MOSCA_L) le gana por mas de 1 punto a cada embudo artificial del mismo ancho (PCA_L y PROY_L), en promedio sobre la curva baja y las dos celdas.
- **H_DATOS_CRUDO:** con el mismo L y los mismos ensayos, MOSCA_L le gana por mas de 1 punto a CRUDO, en promedio sobre la curva baja y las dos celdas.
- **H_DATOS_PRIMER_DIA:** con 96 ensayos etiquetados (16 por clase en promedio), ningun par artificial (CRUDO, PCA_L ni PROY_L) llega a menos de 1 punto de W, que no vio ningun ejemplo de accion.

## Estadistica (decide)

- MOSCA_L(c, n) es la media sobre las 10 taus y las 20 repeticiones; PROY_L(c, n), sobre las 10 matrices y las 20 repeticiones; PCA_L y CRUDO, sobre las 20 repeticiones; W(c), sobre las 10 taus.
- D_a = media sobre c en {c2, c5} y n en la curva baja de [MOSCA_L(c, n) - a(c, n)], para a = PCA_L, PROY_L y CRUDO.
- E_a = media sobre c de [a(c, 96) - W(c)], para a = CRUDO, PCA_L y PROY_L.
- IC: bootstrap en tres ejes independientes: las 20 repeticiones (las mismas para todos los brazos y las dos celdas), las 10 taus (las mismas para W y MOSCA_L) y las 10 matrices de PROY_L. B = 20.000, semilla 2063, percentiles 2,5 y 97,5.
- **H_DATOS_EMBUDO:** SOSTENIDA si el piso de D_PCA_L y el de D_PROY_L son mayores que +0,01; REFUTADA si el techo de alguno es menor que +0,01; SIN_DECIDIR en otro caso.
- **H_DATOS_CRUDO:** SOSTENIDA si el piso de D_CRUDO es mayor que +0,01; REFUTADA si el techo es menor que +0,01; SIN_DECIDIR en otro caso.
- **H_DATOS_PRIMER_DIA:** SOSTENIDA si el techo de E_a es menor que -0,01 para los tres; REFUTADA si el piso de alguno es mayor que -0,01; SIN_DECIDIR en otro caso.
- Cada decision es unilateral al 2,5 %; con tres hipotesis, el error de familia queda por debajo del 7,5 %. Las comparaciones por n no deciden.
- Si falla cualquier control, las tres son INVALIDO y sus descriptivos no se citan.

## Descriptivos (no deciden)

- La curva de cada brazo por celda y n: media, minimo y maximo entre repeticiones.
- N_alcanza(a): el n mas chico de la grilla en que la media de a(c, n) llega a W(c) - 0,01, por celda y en la media de las dos; si no llega ni con 2.400, se informa «mas de 2.400». Tambien para MOSCA_L.
- W_n: W con los umbrales calibrados solo con los ensayos sin evento que caen dentro del subconjunto de n, cuando hay al menos uno de cada estado. Dice cuanto fondo necesita la mosca.
- MOSCA_L menos W por n: desde cuantos ensayos le conviene a la mosca entrenar su lector.
- La fraccion de varianza que explican las 240 componentes de la PCA.

## Controles (si falla cualquiera: INVALIDO)

- **PIN:** los de H_TAU_LIBRE (`lector_mosca.py` 5b7fb79e55ab2b695c9751698c8205c4, `rival_mosca.py` 774232f5b4a53872a05f6a0f06015f34, modulos, conectoma, anotaciones y los MD5SUMS de H_RIVAL y H_LECTOR), mas `taulibre_mosca.py` (c65bebe270da1e0526a212cff29830fd), `results/taulibre_2026-10-15/MD5SUMS.txt` (89ebc30bdf307e9c071168fb3584379f) y cada `reales_c*.json` contra esa lista.
- **REPRO_TAULIBRE:** MOSCA_L con n = 2.400 reproduce, para cada celda y tau, el WL, el lambda y las predicciones caracter por caracter de los `reales_c*_t*.json` de H_TAU_LIBRE (20 de 20).
- **REPRO_CRUDO:** CRUDO con n = 2.400 reproduce el RIDGE de H_RIVAL en c2 y c5, prueba 12: acierto, lambda y `pred_RIDGE` caracter por caracter (`rival_c2.json` y `rival_c5.json`).
- **L_IGUAL:** en la prueba unitaria, el L con guarda da lo mismo que `rv.cv_ridge`, `rv.ridge_ajustar` y `rv.ridge_predecir` cuando hay ensayos de los dos estados, y la guarda predice 0 cuando falta un estado.
- **CONTROL_NEGATIVO:** con las etiquetas permutadas dentro de cada estado (semilla 2043, la de H_LECTOR) y n = 2.400, MOSCA_L (primera tau de cada trabajo) y CRUDO aciertan como mucho el azar mas 0,05.
- **SUBCONJUNTOS:** cada json guarda el md5 de los 20 subconjuntos de cada n; el agregador exige que sean iguales en todos los trabajos. El instrumento chequea que sean anidados y caigan dentro de los 2.400.
- **PCA_ORTONORMAL:** las 240 componentes son ortonormales (error maximo menor que 1e-8).
- **GUARDA_FUGA:** semillas de prueba y de ruido de prueba distintas de las de entrenamiento; la PCA, la estandarizacion y los pesos de cada pliegue salen solo de su conjunto de ajuste (la PCA, de los 2.400 de entrenamiento sin etiquetas).
- **PLAN_COMPLETO:** las 20 combinaciones de celda y tau de la mosca y las 2 celdas del crudo, con los 9 n y las 20 repeticiones, sin faltantes, y el mismo md5 de script en todos los json.

## Limitaciones declaradas antes de correr

1. Dos celdas de seis y una sola prueba (12), como H_TAU_LIBRE: el IC cubre subconjuntos, taus y matrices, no pruebas.
2. W calibra sus umbrales con los 960 ensayos sin evento del entrenamiento: no ve ningun ejemplo de accion, pero sabe cuales ensayos son fondo. W_n mide cuanto de ese fondo necesita.
3. La PCA usa los 2.400 ensayos de entrenamiento sin etiquetas, y la mosca no. Es una ventaja a favor del par artificial, declarada.
4. El cuello entrenado de 6 canales, la robustez y el costo en placa no entran: son H_PARES_ROBUSTO y lo que sigue.
5. Los 96 ensayos de H_DATOS_PRIMER_DIA son una eleccion (16 por clase en promedio, un lote chico de etiquetado). N_alcanza da la curva completa.
6. Ninguna comparacion por ensayo decide.

## Expectativa declarada

H_DATOS_CRUDO probablemente sale SOSTENIDA: con pocos ensayos, 240 rasgos le ganan a 22.560. H_DATOS_EMBUDO esta abierta, y la PCA es el rival mas duro porque ve los 2.400 ensayos sin etiqueta. H_DATOS_PRIMER_DIA esta abierta. El sello no esta escrito para que gane la mosca.

## Maquina y disparo

- Actions x64 decide: 10 trabajos de la mosca (c2 y c5, 2 taus cada uno), 2 del crudo (uno por celda) y el agregado, que commitea `results/pares_datos_2026-10-18/`. Costo estimado desde H_TAU_LIBRE: unos 11 minutos por tau, unos 25 minutos por trabajo.
- Humo ciego antes, con `results/pares_datos_2026-10-18_humo/HUMO`: REPRO_TAULIBRE (tau 20) y REPRO_CRUDO a tamano completo en c2 y c5, que reproducen resultados ya publicados; la prueba unitaria; y las rutas de la curva con 600 y 200 ensayos en la semilla 99, sin aciertos nuevos.
- La corrida completa la autorizo Abraham en el mismo pedido («ejecutá la curva»). Se dispara con `results/pares_datos_2026-10-18/CORRER` solo si el humo da VALIDO.
- brain-env corre la prueba unitaria y la ruta local antes de commitear el instrumento. La replica completa en brain-env queda NO MEDIDA.

## Salidas

`results/pares_datos_2026-10-18/`: `mosca_c*_t*.json` y `crudo_c*.json` con sus .log, `versiones_*.txt`, `agregado.log`, `agregado.json` y `MD5SUMS.txt`. Codigo de salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.

--- METODO PROMETEO ---
Rol: investigacion (pre-registro). Delicado: no, documento solo.
Maquina: brain-env, lectura de `lector_mosca.py`, `taulibre_mosca.py`, `rival_mosca.py`, los json de H_TAU_LIBRE y de H_RIVAL en `e7ada46`, y la composicion de `tm.generar(2400, 1)`; ningun brazo corrido.
Artefactos: este sello en `titan/pares-datos-2026-10-18`; respuesta `docs/agents/respuestas/2026-10-14-059-*.md` en main; Doc de ClickUp de la 059.
