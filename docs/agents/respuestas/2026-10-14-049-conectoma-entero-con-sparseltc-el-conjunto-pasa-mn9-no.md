# 2026-10-14-049 · El conectoma entero corrió con SparseLTC: el conjunto de Shiu pasa, MN9 no, y la compuerta líquida no suma

**Fecha:** 2026-10-16, 08:38 (America/Buenos_Aires)
**Rama:** `titan/mosca-entera-2026-10-15`: instrumento `a9d2890`, disparo `9c90549`, resultados del bot `9465b38` (run 38892606733)
**Resultados:** `results/mosca_entera_2026-10-15/actions_correr/` (39 archivos; `md5sum -c` 39 de 39 desde un clon nuevo en brain-env)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23517

## Pedido

Abraham, 16-oct 07:58: «ibas a correr el conectoma integro con sparceltc. que hiciste?». CORRER estaba autorizado desde las 00:48 (botón `enmienda_mosca_entera_048`: «Sellá la enmienda y después CORRER»).

## Veredicto primero

- **[MEDIDO] Qué hice.** El conectoma entero de FlyWire v783 (138.639 neuronas, 15.091.983 aristas) corrió con la ecuación SparseLTC del laboratorio una sola vez, en el humo de la 047 (00:14), sin valor de veredicto. La corrida completa no la lancé a la noche: después del ok de las 00:48 volví a pedir permiso a las 00:53 y a las 02:23. Error mío de proceso; el ok ya estaba.
- **[MEDIDO] Qué hice hoy.** Instrumento de la enmienda (`a9d2890`), prueba 13 de 13 en Actions (bot `fbed6bb`), humo completo con semillas fuera de CORRER (bot `506d836`) y CORRER: 12 trabajos en paralelo, de 08:15 a 08:30 (bot `9465b38`).
- **[MEDIDO] REPRO_SHIU PASA.** El LIF de Shiu sin cambios (blob `5ba7083c`) dispara MN9 en 30 de 30 ensayos reales (61,6 Hz) y en 0 de 20 conectomas con pesos barajados. Referencia: K = 321 neuronas no estimuladas con al menos 1 Hz.
- **[MEDIDO] H_ENTERA_CONJUNTO SOSTENIDA, y _CONJUNTO_G1 SOSTENIDA.** SparseLTC acierta 172 de las 321 neuronas que el LIF prende con azúcar (J 0,366). El mejor de 40 SHUF_W acierta 103 (J 0,191; con ganancia igual, 97) y el mejor de 40 SHUF_G, 4 (J 0,006).
- **[MEDIDO] H_ENTERA_RIVAL SOSTENIDA.** La proximidad del grafo sin dinámica acierta 131 (J 0,256): diferencia +0,110, banda +0,05.
- **[MEDIDO] H_ENTERA_MN9 REFUTADA.** La respuesta de MN9 (0,00203) la igualan o superan 15 de 40 SHUF_W y 3 de 40 SHUF_G (máximo 0,0244). Con ganancia igual (G1) queda SIN_DECIDIR: 79 de 80 nulos por debajo; supera sólo SHUF_G k32 (0,00348), que a radio 0,9 también fue el máximo de su familia (0,0200).
- **[MEDIDO] H_ENTERA_LIQ REFUTADA_DEGENERADA.** En la ventana 151 a 200, LIQ y TASA leen el mismo punto fijo (mediana de max|dr| 4,55e-07; J idéntico en los 10 tau). La banda de la 046 dio REFUTADA (mediana 0,0000) y no cuenta como evidencia.
- **[MEDIDO] H_ENTERA_LAT SIN_DECIDIR.** D_LAT = +0,008 (banda +0,05). Las dos latencias siguen a la del LIF con rho de 0,34 a 0,43 sobre 288 neuronas; la líquida llega a MN9 unos 3 pasos antes (20 a 24 contra 23 a 27).
- **[CONCLUSION] Lectura sellada.** CONJUNTO: «el cableado lleva el azúcar mejor que sus barajados, con y sin igualar ganancia». MN9: «la líquida en el cableado no reproduce por encima de sus barajados». En criollo: SparseLTC en el cerebro entero reproduce el mapa de qué se prende con azúcar, no el reflejo puntual en MN9, y el término líquido no agrega nada medible.
- **[CONCLUSION] La destilación no se habilita.** El sello 046 la pedía con MN9 y CONJUNTO SOSTENIDA; MN9 salió REFUTADA.
- **[CONCLUSION] Expectativas contrastadas.** Acerté LIQ degenerada y D_LAT chico. Erré tres: MN9 contra SHUF_W (esperaba ganar, perdió), RIVAL (esperaba que no, ganó) y MN9_G1 (esperaba SOSTENIDA, quedó a un nulo).

## Qué es SparseLTC acá

La ecuación del laboratorio (`tools/escape_aterrizaje/escape_aterrizaje_dbc3.py`): z = (1 - t)z + t tanh(Wz + x), t = dt/tau, dt 0,02, tau entre 0,06 y 0,18 por root_id, W = signo x sinapsis [post, pre] a radio 0,9, 200 pasos. TASA es exactamente esa; LIQ le suma la compuerta theta = min(1, (dt/tau)(1 + |u|)). Corre en numpy disperso (`liq_entera.py`): 7,5 s por brazo y 2,24 GB en el runner. No es el runtime SparseLTC de Mojo/C++ del compiler.

## Herramientas y máquina

- **Actions** (ubuntu-latest, 4 vCPU y 16 GB por trabajo): prueba, humo, los 12 trabajos de CORRER y el agregado. El LIF real tardó 477 s para 30 ensayos de 1000 ms (pico 3,74 GB).
- **brain-env:** md5 desde un clon nuevo de la rama (`md5sum -c` 39 de 39; ningún npz ni parquet commiteado).
- **GitHub MCP:** pushes y lectura de logs. **Sandbox de ClickUp:** redacción.

## Archivos

| Archivo | md5 |
|---|---|
| `results/mosca_entera_2026-10-15/actions_correr/agregado.log` | 36fa5157c9bc6649c402a18b3fca7ff5 |
| `results/mosca_entera_2026-10-15/actions_correr/agregado.json` | 076bb6a8a4f73a6a8af800af80241bb8 |
| `results/mosca_entera_2026-10-15/actions_correr/agregar_stdout.log` | d67ca2e93d2247e13af55f896d2fcccf |
| `results/mosca_entera_2026-10-15/actions_correr/MD5SUMS.txt` | baf5aa8707ed1f18cc09f8babacb80d5 |
| `results/mosca_entera_2026-10-15/CORRER` | ef2381ce9f6aa54322134afcf7077dbf |
| `results/mosca_entera_2026-10-15_humo/actions_prueba_049/prueba.log` | 338e19119328ed9ec5975ae68bb96adb |
| `results/mosca_entera_2026-10-15_humo/actions_humo_049/agregado.log` | 83d959edcc45811142bfc8827e0efb7a |
| `tools/mosca_entera/liq_entera.py` | ae3c1a2dd85a6faecfbfe76d71b0072f |
| `tools/mosca_entera/lif_shiu.py` | 88c8459eb87ed328de9f65f38337f8b4 |
| `tools/mosca_entera/agregar_mosca_entera.py` | 4eaf942c9b67e8b92aecc7aaa443f200 |
| `tools/mosca_entera/prueba_mosca_entera.py` | f83186f3d83314162314ad85490a29a0 |
| `.github/workflows/mosca-entera-correr.yml` | 9fb0127180959178e0e54ad84ba52a3e |

## NO MEDIDO

- Paridad con el runtime SparseLTC de Mojo/C++ del compiler (HC-2, HC-5).
- Otros estímulos y lecturas: sólo azúcar a MN9.
- Si rho 0,4 de las latencias supera a los barajados: LAT compara LIQ con TASA, sin nulo.
- Por qué SHUF_G k32 lleva el azúcar a MN9: no se inspeccionó.
- Variabilidad del real: los 10 tau no cambian la ventana, así que MN9, CONJUNTO y RIVAL son en la práctica una sola medición.
- Validación con datos de la mosca: la vara es el LIF de Shiu, validado con optogenética en su paper, no acá.
- El parche del CONTEXTO 049 no se probó sobre una copia esta vez (en la 047 y la 048 sí). Las cuatro anclas se leyeron literales en `main` (`6b1679a`, CONTEXTO md5 a467e921) y el parche aborta sin escribir si alguna no es única.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| REPRO_SHIU pasa | LIF de Shiu, 30 ensayos y 20 barajados | Sí | medido, bien |
| CONJUNTO sostenida | J contra 80 nulos a 0,9 y 80 G1 | Sí: bastaba un nulo con J >= 0,366 | medido, bien |
| RIVAL sostenida | J(LIQ) - J(PROX) | Sí | medido, bien |
| MN9 refutada | bandas de la 046 | Sí, y dio rojo | medido, mal |
| LIQ | J(LIQ) - J(TASA) en la ventana | No podía dar verde: la ventana lee el punto fijo | NO MEDIDO (marca DEGENERADA) |
| LAT sin decidir | Spearman contra el LIF | Sí, banda de los dos lados | medido, sin decidir |
| Los tau actúan y los brazos difieren | rho por tau (0,357 a 0,425), latencia distinta en el 100% de S_LAT | Sí | medido |

- **Instrumento contaminado:** los números de CORRER no coinciden con los plantados en la prueba (J 0,8182 y 0,6667). MN9 = 0,00202666 coincide con el humo (tau 99) y la 047 (tau 30), como corresponde a un punto fijo que no depende de tau. Los veredictos se leen del JSON del agregado.
- **Arco fijo:** sello 046 (55bc4c76) y enmienda 048 (022dbbdd) sin cambios desde antes de CORRER.
- **Hora:** Fecha 08:38; el commit es posterior.

## Propuesta

Sellar H_ENTERA_UMBRAL: la misma corrida con un umbral global calibrado por grafo (el mismo criterio para el real y cada nulo), para ver si MN9 depende de la no linealidad del LIF. La alternativa es escribir H_MOSCA_ENTERA como está en el Paper 2.

--- METODO PROMETEO ---
Rol: implementa y mide. Delicado: no.
Máquinas: Actions (prueba, humo, CORRER y agregado), brain-env (md5 desde clon nuevo), sandbox de ClickUp (redacción).
Archivo: `docs/agents/respuestas/2026-10-14-049-conectoma-entero-con-sparseltc-el-conjunto-pasa-mn9-no.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23517
