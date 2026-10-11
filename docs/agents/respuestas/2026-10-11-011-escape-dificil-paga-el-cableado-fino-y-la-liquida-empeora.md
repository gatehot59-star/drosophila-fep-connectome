# 2026-10-11-011 · Escape difícil: fuera del techo la mosca le gana también a SL, y la τ líquida congelada empeora; paga la τ fija heterogénea

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21177

**Instrumento:** rama `titan/escape-motivo-2026-10-11`. md5 del script sellado en `e030e19` (`tools/escape_motivo/PREREGISTRO-escape-dificil.md` y `humo_dificil.log`) antes de correr al sujeto; script entero y log en `7163c15`, con el mismo md5 (`2c95e63b6ad3ff590057df80368134d7`).

## 1. Pedido

Abraham apretó «Correr la versión difícil» que ofrecí en la 010: amenazas más rápidas y de frente, más ruido y un estímulo que no se acerque, para ver si el cableado fino de la mosca o la neurona líquida suman algo.

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, Python 3.12.14, numpy 2.5.3): dos humos sólo de controles, la corrida completa (7,16 min) y la verificación por md5 en un clon fresco.
- **Sandbox de ClickUp:** escritura de `escape_dificil.py`.
- **GitHub MCP:** dos commits a la rama y este commit a `main`.
- Actions y Kaggle sin uso; sin cuota ajena.

## 3. Veredicto

1. **Ahora sí paga el cableado fino.** Puntaje (supervivencia + rechazo) / 2: W 0,8177 contra SL 0,6819 (6/200, p = 0,0348), S 0,5973 (1/200, p = 0,0100) y B 0,4023 (0/200, p = 0,0050). Por separado, ni el rechazo (1,0 contra 0,849; p = 0,2139) ni la supervivencia (0,6354 contra 0,5148; p = 0,2239) le ganan a SL: la mosca gana porque hace las dos cosas a la vez.
2. **La τ líquida congelada empeora.** En W, supervivencia 0,5604 contra 0,6354 con τ fija heterogénea: 1 ensayo lo salva sólo la líquida y 37 sólo la fija (McNemar p < 0,0001); el rechazo queda igual (80/80). En las poblaciones, la líquida sale peor en 187 de 199 redes S (p = 1,5e−41) y en 186 de 199 redes SL (p = 2,2e−40).
3. **Paga la heterogeneidad de τ, no la liquidez.** La τ uniforme 0,119 también empeora: 0,5437 (6 contra 50, p < 0,0001). El brazo lineal gana por poco: 0,6500 (7 contra 0, p = 0,0156).
4. **Letra chica.** El reflejo escrito a mano sin LC6 (C+L) le gana a la mosca: 0,9167, con latencia mediana 10 contra 14. Escapar a ciegas desde el primer paso sobrevive 0,8333: la supervivencia es sobre todo velocidad.

## 4. Diseño (en el docstring de `escape_dificil.py` y en el pre-registro)

- **Disparo por umbral y escape balístico.** Umbral de cada red y variante: 1,1 × el máximo de max(GF) en 40 ensayos en blanco (sólo ruido).
- **Looming:** az0 en {±90, ±45, ±20, ±10}°, v en {0,25; 1/3; 0,4}, ruido 0,1 y 0,3, 10 repeticiones: 480 ensayos, T = 50, lazo cerrado.
- **No looming:** objeto girando a distancia 4, az0 en {±60, ±20}°, 0,05 rad por paso, ruido 0,1 y 0,3: 80 ensayos. Correcto es no disparar.
- **Entrada:** LC4 = dθ/(dθ + 0,02); LPLC2 = θ/θ_col sólo si dθ > 0; LC6 = θ/θ_col sin exigir expansión. Elegido para que la exclusión LC6→GF (0 aristas en la mosca) tenga algo que hacer; declarado.
- **Brazos, semillas y funciones** de la 010 (`escape_motivo.py`, md5 `97209982…`, importado tal cual), K = 200.
- **Controles:** C+L (LC4 y LPLC2 al GF de su lado), C+6 (C+L más LC6→GF con peso 1/2), C0.
- **Calibración, sólo con controles:** el primer humo, con v en {1/3; 0,4; 0,5} y T = 40, dio C+L 0,5333 e instrumento INVALIDO; se bajó v y se subió T antes de correr al sujeto.

## 5. Resultados (verbatim de `run.log`)

```
MOTIVO aristas=88 LC6->GF=0 cruzadas=0
ENSAYOS looming=480 no_looming=80 blanco=40 T=50
CONTROL C+L umbral=0.0484 supervivencia=0.8333 lado_ok=0.8313 disparo_looming=1.0000 latencia_mediana=10.0 rechazo=1.0000 comb=0.9167
CONTROL C+6 umbral=0.0977 supervivencia=0.7896 lado_ok=0.9229 disparo_looming=1.0000 latencia_mediana=11.0 rechazo=0.0000 comb=0.3948
CONTROL C0 umbral=0.0000 supervivencia=0.0000 lado_ok=0.0000 disparo_looming=0.0000 latencia_mediana=-1.0 rechazo=1.0000 comb=0.5000
REFERENCIA escape inmediato ciego al lado (siempre a la izquierda desde t=0) supervivencia=0.8333
CHEQUEO INSTRUMENTO VALIDO
SUJETO W variante=TANH+FIJA_HET umbral=0.2662 supervivencia=0.6354 lado_ok=0.8708 disparo_looming=1.0000 latencia_mediana=14.0 rechazo=1.0000 comb=0.8177
SUJETO W variante=TANH+FIJA_UNI umbral=0.3516 supervivencia=0.5437 lado_ok=0.9688 disparo_looming=1.0000 latencia_mediana=14.0 rechazo=1.0000 comb=0.7719
SUJETO W variante=TANH+LIQUIDA umbral=0.2722 supervivencia=0.5604 lado_ok=0.8354 disparo_looming=1.0000 latencia_mediana=14.0 rechazo=1.0000 comb=0.7802
SUJETO W variante=LINEAL+FIJA_HET umbral=0.3099 supervivencia=0.6500 lado_ok=0.8917 disparo_looming=1.0000 latencia_mediana=14.0 rechazo=1.0000 comb=0.8250
NULO S variante=TANH+FIJA_HET supervivencia_media=0.3930 rechazo_media=0.8016 comb_media=0.5973 comb_p95=0.7523
NULO SL variante=TANH+FIJA_HET supervivencia_media=0.5148 rechazo_media=0.8490 comb_media=0.6819 comb_p95=0.8073
NULO B variante=TANH+FIJA_HET supervivencia_media=0.0616 rechazo_media=0.7430 comb_media=0.4023 comb_p95=0.5698
CONTRASTE Q1 comb W=0.8177 SL_media=0.6819 n_SL>=W=6/200 p_emp=0.0348 -> W GANA
CONTRASTE Q2 comb W=0.8177 S_media=0.5973 n_S>=W=1/200 p_emp=0.0100 -> W GANA
CONTRASTE Q3 comb W=0.8177 B_media=0.4023 n_B>=W=0/200 p_emp=0.0050 -> W GANA
CONTRASTE Q4 rechazo W=1.0000 SL_media=0.8490 n_SL>=W=42/200 p_emp=0.2139 -> W NO GANA
CONTRASTE Q5 supervivencia W=0.6354 SL_media=0.5148 n_SL>=W=44/200 p_emp=0.2239 -> W NO GANA
CONTRASTE Q6_liquida_supervivencia TANH+LIQUIDA=0.5604 TANH+FIJA_HET=0.6354 solo_A=1 solo_B=37 p_mcnemar=0.0000 -> TANH+LIQUIDA PEOR
CONTRASTE Q6_uniforme_supervivencia TANH+FIJA_UNI=0.5437 TANH+FIJA_HET=0.6354 solo_A=6 solo_B=50 p_mcnemar=0.0000 -> TANH+FIJA_UNI PEOR
CONTRASTE Q6_lineal_supervivencia LINEAL+FIJA_HET=0.6500 TANH+FIJA_HET=0.6354 solo_A=7 solo_B=0 p_mcnemar=0.0156 -> LINEAL+FIJA_HET MEJOR
CONTRASTE Q7_S comb(LIQUIDA)-comb(FIJA_HET) dif_media=-0.0286 liquida_mejor=12 liquida_peor=187 p_signo=1.526e-41 -> LIQUIDA PEOR
CONTRASTE Q7_SL comb(LIQUIDA)-comb(FIJA_HET) dif_media=-0.0303 liquida_mejor=13 liquida_peor=186 p_signo=2.208e-40 -> LIQUIDA PEOR
VEREDICTO_FUNCION=W GANA A S
VEREDICTO_DETALLE=PAGA EL CABLEADO FINO: W GANA A SL
VEREDICTO_TAU_W=LA LIQUIDA EMPEORA EN LA MOSCA
VEREDICTO_TAU_POBLACION=LA LIQUIDA EMPEORA EN LA POBLACION SL
VEREDICTO_LINEAL=EL LINEAL GANA A TANH
escrito resultados.json md5=d57693a44400233ccd4e143c56c18181
minutos=7.16
EXIT_RUN=0
```

El log completo tiene 64 líneas en la rama. `resultados.json` (735.358 B) queda en brain-env y se regenera con el mismo comando.

## 6. Qué cambia en la hipótesis de agosto

| Parte | Después de la 010 | Ahora |
|---|---|---|
| «El conocimiento está en el cableado» | sólo como lateralidad | también como cableado fino: la mosca le gana a SL cuando hay que escapar y no asustarse a la vez. El reflejo escrito a mano sigue siendo mejor |
| «Funciona el primer día, sin entrenar» | 180/180 en la tarea fácil | 80/80 sin falsas alarmas y 63,5% de escapes, sin entrenar un peso |
| «La neurona líquida es necesaria» | no hace falta para escapar | congelada, empeora; paga la τ fija heterogénea. Entrenada, NO MEDIDA |

**Para BEEC v2:** la capa L2 decía «SparseLTC con τ uniforme»; esto apunta a τ fija heterogénea. Decide Abraham.

## 7. Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| La mosca le gana a SL en su función | p empírico, 200 shuffles, empates en contra | sí: C+6 muestra que LC6→GF hunde el puntaje | PASS (0,035; contraste primario único) |
| La líquida congelada empeora | McNemar en W y test del signo en 399 redes | sí | PASS, fuerte |
| La τ heterogénea gana a la uniforme | McNemar | sí | PASS (50 contra 6) |
| La neurona líquida no sirve | ninguno: sólo se probó congelada | no | NO MEDIDO |
| La ventaja sobre SL no depende del modelo de entrada | ninguno | no | NO MEDIDO |

## 8. Archivos generados

- En `titan/escape-motivo-2026-10-11`: `tools/escape_motivo/escape_dificil.py` (md5 `2c95e63b6ad3ff590057df80368134d7`), `PREREGISTRO-escape-dificil.md`, `humo_dificil.log` y `results/escape_dificil_2026-10-11/run.log` (`4615f051cd86201cff965d9ca5838d67`). Clon fresco: 2/2 md5 idénticos.
- En `main`: este archivo y `docs/agents/CONTEXTO-drosophila-fep.md`.

## 9. NO MEDIDO

- τ líquida entrenada (Vx y Vh aprendidos) en esta tarea.
- Otro modelo de entrada: LC6 que también exija expansión.
- Lectura por DNp09; GF-01 completo (864 nodos); un S que conserve Dale.
- Segunda máquina, hardware y review externo.

## 10. QA (TITAN FULL)

| Criterio | Puntaje | Evidencia |
|---|---|---|
| Completitud | 14/15 | Tres nulos, tres controles, seis variantes y poblaciones. −1: falta la líquida entrenada |
| Ejecutabilidad | 15/15 | exit 0; md5 sellado igual al commiteado; 7,16 min |
| Arquitectura del razonamiento | 9/10 | Puntaje combinado y umbral por piso de ruido. −1: el modelo de entrada favorece la exclusión (declarado) |
| Documentación | 9/10 | Docstring, pre-registro, humos y log. −1: `resultados.json` en brain-env |
| Innovación | 5/5 | Pre-registro por md5 sellado; C+6 hace visible la exclusión |
| Proceso QA | 4/5 | Calibración declarada y sólo con controles. −1: sin review externo |
| Seguridad, Testing, DevOps | N/A (40) | Sin frontera de confianza ni despliegue |

**56/60 → 93/100 sobre lo aplicable.**
