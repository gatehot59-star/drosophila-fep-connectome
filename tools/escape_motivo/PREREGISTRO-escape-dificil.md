# Pre-registro: escape fuera del techo (escape_dificil.py)

**Sellado antes de la corrida completa:** `tools/escape_motivo/escape_dificil.py`, md5 `2c95e63b6ad3ff590057df80368134d7`. El archivo entero se commitea con los resultados; si su md5 no es este, la corrida no vale.

**Qué cambia contra la 010:** disparo por umbral calibrado en ensayos en blanco (1,1 × el máximo del GF con sólo ruido) y escape balístico; looming a ±90, ±45, ±20 y ±10°, v en {0,25; 1/3; 0,4}, ruido 0,1 y 0,3 (480 ensayos, T = 50); un estímulo que no es looming (objeto girando a distancia fija, 80 ensayos) donde lo correcto es no disparar; LC4 por velocidad de expansión, LPLC2 por tamaño sólo si hay expansión, LC6 por tamaño sin exigirla.

**Puntaje:** comb = (supervivencia + rechazo) / 2.

**Reglas:**

- Validez: C+L supervivencia ≥ 0,60 y rechazo ≥ 0,90; C+6 rechazo ≤ 0,50; C0 supervivencia ≤ 0,05.
- Q1 comb W contra SL (cableado fino); Q2 contra S; Q3 contra B: W gana si (1 + #{nulo ≥ W}) / (K + 1) < 0,05, K = 200.
- Q4 rechazo y Q5 supervivencia contra SL, secundarios.
- Q6 en W, McNemar exacto: líquida contra fija heterogénea, uniforme contra heterogénea, lineal contra tanh.
- Q7 en las poblaciones S y SL: comb(líquida) menos comb(fija) red por red, test del signo exacto.

**Calibración, sólo con controles** (ver `humo_dificil.log`): el primer humo, con v en {1/3; 0,4; 0,5} y T = 40, dio C+L 0,5333 e instrumento INVALIDO. Se bajó v y se subió T. El segundo dio VALIDO. El sujeto no se corrió en ninguno.
