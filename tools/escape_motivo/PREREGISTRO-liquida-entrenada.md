# Pre-registro: τ líquida entrenada (liquida_entrenada.py)

**Sellado antes de entrenar:** `tools/escape_motivo/liquida_entrenada.py`, md5 `0bb3f8f4a9b0fd0f7d74d102d8922d1b`. El archivo entero se commitea con los resultados; si su md5 no es este, la corrida no vale.

**Sujeto, tarea y lectura:** los de `escape_dificil.py` (md5 `2c95e63b…`, importado tal cual): motivo de 26, ρ = 0,9, tanh, disparo por umbral y puntaje comb = (supervivencia + rechazo) / 2. Sólo se entrenan los parámetros de τ.

**Brazos**, todos arrancando en la τ fija heterogénea de la 011:

- FIJA_ENT: τ_i = sigmoid(b_i), 26 parámetros.
- LIQ_DIAG: τ_i(t) = sigmoid(b_i + vx_i·x_i + vh_i·z_i), 78 parámetros, vx = vh = 0 al inicio.
- LIQ_PLENA: τ(t) = sigmoid(b + Vx·x + Vh·z), 1.378 parámetros, Vx = Vh = 0 al inicio.

**Entrenamiento:** estrategia evolutiva antitética, 40 iteraciones × 8 pares, σ 0,1, rangos centrados, Adam lr 0,05; 681 evaluaciones por corrida; 4 semillas por brazo. Entrenamiento con ruido 20261013 (240 + 40 + 40 ensayos); prueba con ruido 20261014 (480 + 80 + 40).

**Reglas:**

- Validez en prueba: C+L supervivencia ≥ 0,60 y rechazo ≥ 0,90; C+6 rechazo ≤ 0,50; C0 supervivencia ≤ 0,05.
- Guarda: los tres brazos arrancan con el mismo puntaje exacto.
- E1 LIQ_DIAG contra FIJA_ENT y E2 LIQ_PLENA contra FIJA_ENT: McNemar exacto sobre los aciertos de prueba apareados por semilla y ensayo (4 × 560), p < 0,05.
- E3 FIJA_ENT contra FIJA_HET sin entrenar, igual.
- VEREDICTO_LIQUIDA_ENTRENADA: PAGA si E1 o E2 da MEJOR y ninguno PEOR; PIERDE si alguno da PEOR y ninguno MEJOR; MIXTO; o NO SE DISTINGUE.

**Humo** (sólo controles y guardas, sin entrenar ni medir al sujeto): C+L 0,8125 / 1,0; C+6 rechazo 0,0; C0 0,0; VALIDO; punto de partida igual en los tres brazos; 0,076 s por evaluación.
