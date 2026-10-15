# SELLO H_LECTOR (2026-10-14-036)

**Sellado:** 2026-10-15, 10:00 (America/Buenos_Aires), antes de escribir cualquier script de H_LECTOR. Este commit trae solo este archivo. El instrumento (`tools/lector/lector_mosca.py`, su agregador y sus pruebas) entra en un commit posterior; cualquier diferencia con lo que dice aca se declara en la respuesta que lo traiga, y este archivo no se edita.

**Autorizado por:** Abraham, 15-oct 09:52, ClickKit `sellar_lector_mosca` («Sellá la mosca con lector entrenado»).

**Base:** rama `titan/rival-2026-10-15` (`576fc4c`), que trae los modulos sellados, H_TAU, el factorial 3, `tools/factorial3/nulos_r2.py` y la corrida completa de H_RIVAL.

## Por que

En H_RIVAL (2026-10-14-034) la mosca leyo con tres lineas y seis umbrales sin entrenar, y los rivales entrenaron un lector sobre las 564 entradas crudas. La auditoria 2026-10-14-035 (P2-8) dejo abierta la asimetria: la mosca pierde por 5 puntos por su cableado o por su lector? Este sello le da a la mosca el mismo lector entrenado que gano H_RIVAL, sobre sus propias salidas.

## Lo que se vio antes de sellar

- H_RIVAL, pruebas 12 a 21: RIDGE crudo 0,9894 a 0,9988 por celda; W (lineas sin entrenar) 0,9413 a 0,9467. REFUTADA en Actions; la replica en brain-env esta en curso.
- Nadie entreno todavia un lector sobre las descendentes del banco R2: los json de H_TAU y del factorial 3 guardan predicciones de las lineas, no trazas.
- Antecedente en contra, en otra tarea y otro recorte: en la entrada por tipos (`results/entrada_por_tipos_2026-10-12/`), con lector entrenado el cableado no le gano a SL ni a T en ninguna de las celdas leidas (EMPATE o PIERDE).
- Expectativa declarada: H_LECTOR_PAGA puede salir; H_LECTOR_CABLEADO probablemente sale REFUTADA; H_LECTOR_CERCA esta abierta. El sello no esta escrito para que gane la mosca.

## Lector

L es el RIDGE de H_RIVAL sin cambios (`tools/rival/rival_mosca.py`, md5 774232f5b4a53872a05f6a0f06015f34): rasgos estandarizados con media y desvio del conjunto de ajuste (desvio + 1e-6), objetivo one-hot, intercepto sin penalizar, penalidad lambda * n, lambda en {1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 1e2, 1e3, 1e4, 1e5}, un solo lambda para los dos estados, empate al lambda mas grande, un modelo por estado con las clases de `tm.CLASES`, validacion cruzada de 5 pliegues (indice del ensayo modulo 5) sobre los 2.400 ensayos de entrenamiento, reajuste con los 2.400 y recien ahi la prueba.

Lo unico que cambia es la entrada: en lugar de las 564 entradas crudas (22.560 rasgos), L lee las trazas de las 6 descendentes que devuelve `f2.sim_trozos(W, tau, n_ent, chan, d, False)` (40 pasos por 6, **240 rasgos por ensayo**, 94 veces menos). Son las mismas trazas que `tm.lineas` convierte en las tres lineas de W.

## Hipotesis

- **H_LECTOR_CERCA:** con L, la red elegida de H_TAU no pierde mas de 1 punto contra el RIDGE crudo de H_RIVAL.
- **H_LECTOR_PAGA:** con L, la red elegida supera por mas de 1 punto a la misma red leida con las lineas sin entrenar (W_elegida).
- **H_LECTOR_CABLEADO:** con L, el cableado real supera por mas de 1 punto a sus barajados SL y T.

## Datos (los de H_RIVAL, sin cambios)

- Sujeto: `f2.sujeto(conn, annot, "R2", "CON")`, 33.489 neuronas, 4.031.897 aristas, 564 entradas; red sin liquidez (TASA).
- Red real: tau de `f2.tau_por_root(ids, 10)`, la semilla elegida por H_TAU en las 6 celdas (`elegida` = 10 en los json `htau_c0` a `htau_c5`).
- Entrenamiento: `tm.generar(2400, 1)`, ruido `f2.ruido_por_root(ids[:564], 2400, 101)`. Prueba primaria: semillas 12 a 21, `tm.generar(2000, p)`, ruido de semilla 1000 + p.
- Celdas c0 a c5 en el orden de `f2.CELDAS`. Estado conocido, como en W, la regla y los rivales.

## Metrica

acc = fraccion de aciertos sobre los 2.000 ensayos de cada semilla de prueba. No hay otra metrica primaria.

## Comparacion primaria (decide H_LECTOR_CERCA y H_LECTOR_PAGA)

- WL(c, p): acierto de L sobre la red real, c = c0 a c5, p = 12 a 21.
- d1 = WL - RIDGE(c, p), con RIDGE leido de `results/rival_2026-10-15/rival_c*.json` (campo `RIDGE` de cada fila). d2 = WL - W_elegida(c, p), leido de los json de H_TAU.
- D1 y D2 = media sobre las 6 celdas y las 10 semillas.
- IC: bootstrap de las 10 semillas de prueba (el mismo remuestreo para las 6 celdas y las dos diferencias), B = 20.000, semilla 2041, percentiles 2,5 y 97,5 (el 90% con Bonferroni por 2).
- **Margenes declarados: 1 punto.**
- H_LECTOR_CERCA: SOSTENIDA si el piso de D1 es mayor que -0,01; REFUTADA si el techo es menor que -0,01; SIN_DECIDIR en otro caso. Descriptivo aparte: GANA_AL_RIDGE si el piso de D1 es mayor que 0.
- H_LECTOR_PAGA: SOSTENIDA si el piso de D2 es mayor que +0,01; REFUTADA si el techo es menor que +0,01; SIN_DECIDIR en otro caso.

## Nulos (deciden H_LECTOR_CABLEADO)

- Celdas c2 (A 0,3, ruido 0,15: la de nulos del factorial 3) y c5 (A 0,6, ruido 0,45: la de W mas baja en H_RIVAL). Tau de semilla 10. Solo la prueba 12.
- SL: k = 0 a 39 con `barajar_sl_np` y `default_rng([7, k])`. T: k = 0 a 39 con la permutacion de tipos de `nulos_r2.py` y `default_rng([11, k])`. El modulo se importa sin cambios (md5 c4f1c4d39c99f07cb9ad7977b6f3b01a). Son los primeros 40 nulos de cada familia del factorial 3, ahora en dos celdas y con tau 10.
- Por nulo se simula entrenamiento y prueba y L se reentrena con la misma validacion cruzada.
- Por familia f y celda c: p(f, c) = (1 + numero de nulos con WL_nulo >= WL_real) / 41; delta(f, c) = WL_real - media de los 40 WL_nulo.
- SUPERA(f, c) si p(f, c) <= 0,05 y delta(f, c) > 0,01.
- **H_LECTOR_CABLEADO:** SOSTENIDA si hay SUPERA en las 4 combinaciones (SL y T por c2 y c5); como exige las cuatro, es una prueba de interseccion-union y cada una va al 5% sin correccion. REFUTADA si en alguna delta(f, c) es menor que 0,01 o p(f, c) es mayor que 0,10. SIN_DECIDIR en otro caso.

## Veredictos e invalidez

Si falla cualquier control, las tres hipotesis son INVALIDO y sus descriptivos no se citan (regla de la 2026-10-14-031).

## Limitaciones declaradas antes de correr

1. Una sola red elegida por celda: el IC de la primaria cubre la variacion entre semillas de prueba, no entre redes (como H_TAU y H_RIVAL).
2. Nulos en 2 celdas y una prueba, por costo. Con 40 por familia, el p minimo es 1/41 (0,024).
3. L lee 240 rasgos y el RIDGE crudo 22.560: el presupuesto de eleccion es el mismo (10 lambdas), la capacidad no. Si CERCA sale SOSTENIDA, es con 94 veces menos rasgos.
4. La red no se entrena: solo su lector. Tau sigue siendo la de H_TAU.
5. Ninguna comparacion por ensayo decide.

## Controles (si falla cualquiera: INVALIDO)

- **PIN:** los pines de H_RIVAL (conn, annot, modulos, json de H_TAU, factorial 3, `completa.log`), mas `rival_mosca.py` (774232f5b4a53872a05f6a0f06015f34), `nulos_r2.py` (c4f1c4d39c99f07cb9ad7977b6f3b01a), `results/rival_2026-10-15/MD5SUMS.txt` (78477d7a099e3399333309126a42ee6d) y cada `rival_c*.json` contra esa lista.
- **REPRO_W:** con las trazas simuladas, `tm.lineas`, `tm.umbrales` y `tm.carrera` reproducen exactamente `pred_elegida` de H_TAU en las 60 corridas (6 celdas por pruebas 12 a 21). Prueba que L lee la misma red que W.
- **REPRO_RIDGE:** el acierto recalculado desde `pred_RIDGE` contra las etiquetas regeneradas da exactamente `RIDGE` en las 60 corridas. Prueba que WL y RIDGE quedan pareados ensayo por ensayo.
- **CONTROL_LECTOR_CRUDO (positivo):** el codigo de L, aplicado a las entradas crudas (22.560 rasgos) en la celda c0 y la prueba 12, da exactamente las predicciones de `pred_RIDGE` de H_RIVAL en esa celda y prueba. Prueba que L es el RIDGE de H_RIVAL.
- **CONTROL_NEGATIVO:** L con las etiquetas de entrenamiento permutadas dentro de cada estado (semilla 2043) sobre las trazas reales, en la prueba 12: acierto de azar + 0,05 o menos en las 6 celdas.
- **NULOS_VALIDOS:** las guardas de `nulos_r2.py` por nulo (SL: grados de entrada y salida y lado de cada arista iguales, al menos un destino cambiado; T: cuenta de tipos por lado igual, al menos un tipo cambiado).
- **REAL_EN_NULOS:** cada trabajo de nulos corre tambien la red real por el mismo camino y da el mismo WL que la primaria en (c2, 12) y (c5, 12).
- **GUARDA_FUGA:** semillas de prueba y de ruido de prueba distintas de las de entrenamiento; la estandarizacion y los pesos de cada pliegue salen solo de sus 4 pliegues de ajuste.

## Maquinas

- Actions x64 decide: 6 trabajos de primaria (uno por celda), los nulos repartidos en trabajos por k (cada nulo tiene su semilla, repartir no cambia numeros) y el agregado, que commitea `results/lector_2026-10-15/`.
- Costo estimado desde H_TAU en Actions (unos 5 minutos de entrenamiento y 4,5 por semilla de prueba): unos 50 minutos por celda en la primaria y unos 10 minutos por red y celda en los nulos (160 en total). El humo lo mide antes de disparar.
- brain-env replica la primaria con los mismos comandos cuando termine la replica de H_RIVAL. Los nulos no se replican (limitacion). Si una etiqueta difiere entre maquinas, pasa a SIN_DECIDIR (NO_SE_REPLICA).

## Humo y disparo

- Humo ciego: corre los controles a tamano completo y recorre las rutas de 2 nulos (uno SL y uno T) con 600 ensayos de entrenamiento y 200 de prueba en una semilla fuera del analisis (99), sin imprimir aciertos de L.
- La corrida completa se dispara solo con el si de Abraham, con `results/lector_2026-10-15/CORRER` en esta rama.

## Salidas

`results/lector_2026-10-15/`: `lector_c0` a `lector_c5` (.log y .json: candidatas, validacion, lambda elegido, aciertos y predicciones por semilla), `nulos_*` (.log y .json), `agregado.log` y `agregado.json`, `versiones_*.txt` y `MD5SUMS.txt`. Codigo de salida: 0 completo; 2 insumos distintos del pin; 3 control fallido.

--- METODO PROMETEO ---
Rol: investigacion (pre-registro). Delicado: no, documento solo.
Maquina: brain-env, lectura de `factorial2_mosca.py`, `nulos_r2.py`, los json de H_TAU y de H_RIVAL en `576fc4c`; ningun lector corrido.
Artefactos: este sello en `titan/lector-2026-10-15`; respuesta `docs/agents/respuestas/2026-10-14-036-h-lector-sellado.md` en main; Doc de ClickUp de la 036.
