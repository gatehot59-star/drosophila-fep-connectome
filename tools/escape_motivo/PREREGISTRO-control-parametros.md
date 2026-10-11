# Pre-registro: control de parámetros y de cableado para la τ líquida entrenada (control_parametros.py)

**Sellado antes de entrenar:** `tools/escape_motivo/control_parametros.py`, md5 `342069aa075256e55e6638127f55a05e`. El archivo entero se commitea con los resultados; si su md5 no es este, la corrida no vale.

**Base:** importa `liquida_entrenada.py` (md5 `0bb3f8f4…`, la 012) con el mismo sujeto, tarea, lectura, optimizador (40 × 8 pares, σ 0,1, Adam 0,05, 681 evaluaciones), datos de entrenamiento y prueba, y punto de partida.

**Parte A, liquidez contra parámetros** (sobre la mosca, 4 semillas):

- LIQ_DIAG (78) y LIQ_PLENA (1.378): los de la 012, se vuelven a correr.
- NOLIQ_DIAG (78): τ fija entrenable; las mismas señales x_i y z_i entran a la neurona con ganancias entrenables (pre_i = (Wz)_i + x_i + gx_i·x_i + gh_i·z_i).
- NOLIQ_PLENA (1.378): τ fija entrenable; pre = Wz + x + Gx·x + Gh·z, con Gx y Gh densas entrenables.
- Todos arrancan en la τ fija heterogénea de la 011 con lo demás en cero (guarda de puntaje inicial igual).

**Parte B, cableado con la líquida entrenada:** LIQ_DIAG (semilla 0) entrenada sobre 24 redes SL y 8 redes S, generadas con las funciones y semillas de la 011.

**Reglas:**

- Validez en prueba: las de la 012. Guardas: punto de partida igual; redes nulas con radio 0,9 y distintas de W.
- REPRODUCE_012: LIQ_DIAG y LIQ_PLENA deben dar, por semilla y a 4 decimales, los mismos puntajes de prueba que la 012. Si no, la parte A no se firma.
- P1 LIQ_DIAG contra NOLIQ_DIAG y P2 LIQ_PLENA contra NOLIQ_PLENA: McNemar exacto apareado (4 × 560), p < 0,05.
- VEREDICTO_LIQUIDEZ: PAGA POR SER LIQUIDA si P1 y P2 dan MEJOR; LA GANANCIA ERA DE PARAMETROS si ninguno da MEJOR ni PEOR; LOS PARAMETROS NO LIQUIDOS RINDEN MAS si los dos dan PEOR; MIXTO en otro caso.
- Q_SL: W (LIQ_DIAG, semilla 0) contra las 24 SL; p = (1 + #{SL ≥ W}) / 25; W GANA si p < 0,05. Secundario con la peor semilla de W.
- Q_S contra las 8 S: descriptivo (p mínimo 0,111).

**Humo** (sólo controles y guardas): C+L 0,8125 / 1,0; C+6 rechazo 0,0; C0 0,0; VALIDO; redes nulas OK; punto de partida igual; 0,080 s por evaluación.
