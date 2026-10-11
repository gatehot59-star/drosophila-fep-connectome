# Pre-registro: la τ líquida plena con optimización ajustada y sobre SL (control_plena.py)

**Sellado antes de entrenar:** `tools/escape_motivo/control_plena.py`, md5 `45bad2a84d625f8826b84876bef87133`. El archivo entero se commitea con los resultados; si su md5 no es este, la corrida no vale.

**Base:** importa `control_parametros.py` (md5 `342069aa…`, la 013) y, a través de él, la 012 y la 011: mismo sujeto, tarea, lectura, datos, punto de partida y brazos.

**Parte A, optimización ajustada** (LIQ_PLENA y NOLIQ_PLENA sobre la mosca, 4 semillas cada uno). Cada semilla se entrena con dos configuraciones, 60 iteraciones × 8 pares:

- C1: σ 0,10 y lr 0,05.
- C2: σ 0,03 y lr 0,02.

Se elige la de mejor puntaje de **entrenamiento**; la prueba nunca se mira para elegir.

**Parte B, cableado:** LIQ_PLENA con el protocolo exacto de la 012 (40 iteraciones, C1, semilla 0) sobre W y sobre 24 redes SL.

**Reglas:**

- Validez y guardas: las de la 013.
- REPRODUCE_012: W en la parte B debe dar 0,9802.
- P3 LIQ_PLENA ajustada contra NOLIQ_PLENA ajustada: McNemar exacto apareado (4 × 560), p < 0,05. MEJOR: la plena gana por ser líquida; IGUAL: no se distingue; PEOR: gana la no líquida.
- Q_SL_PLENA: p = (1 + #{SL ≥ W}) / 25; W GANA si p < 0,05.

**Humo** (sólo controles y guardas): C+L 0,8125 / 1,0; C+6 rechazo 0,0; C0 0,0; VALIDO; 24 SL OK; punto de partida igual.
