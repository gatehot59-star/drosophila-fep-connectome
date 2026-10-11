# 2026-10-11-012 · La τ líquida ENTRENADA paga en el escape: 0,98 contra 0,83 de la τ fija entrenada, 4 de 4 semillas

**Doc público:** https://app.clickup.com/90171457413/docs/2kza6fw5-21197

## 1. Pedido

Abraham apretó «Correr la líquida entrenada» (botón ofrecido en la 011). La 011 dejó a la τ líquida perdiendo contra la fija heterogénea, pero esa líquida estaba **congelada con pesos al azar**. Faltaba el brazo que él defiende desde agosto («la neurona líquida es más que necesaria»): la líquida **entrenada** contra la fija **entrenada**, arrancando del mismo punto, en el escape difícil.

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, 2 núcleos, Python 3.12.14, numpy 2.5.3): humo, corrida de 12,50 min, md5 en clon fresco.
- **Sandbox de ClickUp:** escritura del script.
- **GitHub:** pre-registro `95a6d92` (script sellado antes de entrenar) y resultados `f042e6f`, en `titan/escape-motivo-2026-10-11`.
- Acción delicada: NO.

## 3. Veredicto

**Sí: entrenada, la τ líquida paga en esta función.** Las dos líquidas le ganan a la τ fija entrenada en las 4 semillas, y entrenar la τ fija no le agrega nada a la fija sin entrenar. La conclusión de la 011 («paga la τ fija heterogénea, la líquida empeora») valía sólo para la líquida congelada al azar: queda corregida.

**Diseño** (pre-registro `tools/escape_motivo/PREREGISTRO-liquida-entrenada.md`):

- Sujeto, tarea y lectura de `escape_dificil.py` importados tal cual: motivo de 26 (LC4, LPLC2, LC6, GF, DNp09), ρ = 0,9, tanh, disparo por umbral, puntaje comb = (supervivencia + rechazo) / 2.
- Sólo se entrenan los parámetros de τ. Los tres brazos arrancan en la τ fija heterogénea de la 011:
  - FIJA_ENT: τ_i = sigmoid(b_i), 26 parámetros.
  - LIQ_DIAG: τ_i(t) = sigmoid(b_i + vx_i·x_i + vh_i·z_i), 78 parámetros, vx = vh = 0 al inicio.
  - LIQ_PLENA: τ(t) = sigmoid(b + Vx·x + Vh·z), 1.378 parámetros, Vx = Vh = 0 al inicio.
- Estrategia evolutiva antitética, 40 iteraciones × 8 pares, σ 0,1, Adam lr 0,05; 681 evaluaciones por corrida; 4 semillas por brazo.
- Entrenamiento con ruido 20261013 (240 looming + 40 no looming); prueba con ruido 20261014 (480 + 80). Los números de abajo son de **prueba**.
- McNemar exacto sobre aciertos apareados por semilla y ensayo (4 × 560).

**Resultados en prueba:**

| Brazo | Parámetros | comb (media, rango) | Supervivencia | Rechazo |
|---|---|---|---|---|
| FIJA_HET sin entrenar (011) | 0 | 0,8240 | 0,6604 | 0,9875 |
| Líquida congelada al azar (011) | 0 | 0,7854 | 0,5708 | 1,0000 |
| FIJA_ENT | 26 | 0,8263 (0,8135 a 0,8396) | 0,627 a 0,679 | 1,0 |
| LIQ_DIAG | 78 | 0,9216 (0,9073 a 0,9521) | 0,825 a 0,917 | 0,975 a 1,0 |
| LIQ_PLENA | 1.378 | 0,9826 (0,9802 a 0,9844) | 0,960 a 0,975 | 0,9875 a 1,0 |
| Reflejo a mano C+L | 0 | 0,9062 | 0,8125 | 1,0 |

**Contrastes:**

- E1 LIQ_DIAG contra FIJA_ENT: 393 contra 7, p = 2,431e-106 → **MEJOR**.
- E2 LIQ_PLENA contra FIJA_ENT: 608 contra 3, p = 8,947e-177 → **MEJOR**.
- E3 FIJA_ENT contra FIJA_HET: 271 contra 282, p = 0,6707 → **IGUAL**.
- LIQ_DIAG y LIQ_PLENA le ganan a FIJA_ENT en 4/4 semillas.
- Brecha entrenamiento → prueba chica: PLENA 0,9938 a 0,9979 contra 0,9802 a 0,9844; DIAG 0,9563 a 0,9854 contra 0,9073 a 0,9521.
- Las dos líquidas entrenadas superan al reflejo escrito a mano (0,9062), que en la 011 le ganaba a la mosca.

**Log crudo, líneas verbatim** (`results/liquida_entrenada_2026-10-11/run.log`, md5 `4148815889bbd22c60cda15a2f99b233`, 34 líneas):

```
CHEQUEO INSTRUMENTO VALIDO
GUARDA punto_de_partida_igual=True seg_por_evaluacion=0.076
REFERENCIA_PRUEBA FIJA_HET supervivencia=0.6604 rechazo=0.9875 comb=0.8240
REFERENCIA_PRUEBA LIQUIDA_CONGELADA supervivencia=0.5708 rechazo=1.0000 comb=0.7854
RESUMEN brazo=FIJA_ENT comb_prueba_media=0.8263 min=0.8135 max=0.8396
RESUMEN brazo=LIQ_DIAG comb_prueba_media=0.9216 min=0.9073 max=0.9521
RESUMEN brazo=LIQ_PLENA comb_prueba_media=0.9826 min=0.9802 max=0.9844
CONTRASTE E1_LIQ_DIAG_vs_FIJA_ENT acierto_A=0.8746 acierto_B=0.7022 solo_A=393 solo_B=7 p_mcnemar=2.431e-106 -> MEJOR
CONTRASTE E2_LIQ_PLENA_vs_FIJA_ENT acierto_A=0.9723 acierto_B=0.7022 solo_A=608 solo_B=3 p_mcnemar=8.947e-177 -> MEJOR
CONTRASTE E3_FIJA_ENT_vs_FIJA_HET acierto_A=0.7022 acierto_B=0.7071 solo_A=271 solo_B=282 p_mcnemar=0.6707 -> IGUAL
SEMILLAS LIQ_DIAG gana_a_FIJA_ENT_en=4/4
SEMILLAS LIQ_PLENA gana_a_FIJA_ENT_en=4/4
VEREDICTO_LIQUIDA_ENTRENADA=LA LIQUIDA ENTRENADA PAGA
VEREDICTO_ENTRENAR_TAU=ENTRENAR LA TAU FIJA NO SE DISTINGUE DE NO ENTRENARLA
minutos=12.50
EXIT_RUN=0
```

**ANTES DE FIRMAR: ¿podía dar rojo cada instrumento?**

| Instrumento | ¿Podía dar rojo? | Evidencia |
|---|---|---|
| Puntaje comb | Sí | C+6 rechazo 0,0 (comb 0,3927) y C0 supervivencia 0,0 (comb 0,5000) en el mismo run |
| McNemar apareado | Sí | E3 dio IGUAL (p 0,6707) con el mismo código |
| Ventaja por arrancar distinto | Controlada | guarda punto_de_partida_igual=True; los tres brazos parten de 0,6750 en entrenamiento |
| Sobreajuste al ruido de entrenamiento | Controlado | semillas de ruido distintas para prueba; brecha chica |
| Script cambiado después de ver datos | Controlado | md5 sellado en `95a6d92` igual al de `f042e6f` en clon fresco |

**Mapa de PASS / FAIL / NO MEDIDO de la hipótesis de agosto sobre la neurona líquida:**

- PASS: entrenada, la τ líquida paga en la función propia del motivo (esta respuesta).
- FAIL: congelada al azar, empeora (011); en tareas genéricas sobre el reservorio, empata (008, 3/4).
- NO MEDIDO: si gana por ser líquida o por tener más parámetros (abajo).

**Decisión que se le propone a Abraham:** en BEEC v2 L2, **τ líquida entrenada** (LIQ_DIAG, 78 parámetros, cabe holgado en un ESP32) en vez de la τ fija heterogénea que proponía la 011.

## 4. Archivos

- `tools/escape_motivo/liquida_entrenada.py` (md5 `0bb3f8f4a9b0fd0f7d74d102d8922d1b`) y `tools/escape_motivo/PREREGISTRO-liquida-entrenada.md`, en `95a6d92`.
- `results/liquida_entrenada_2026-10-11/run.log` en `f042e6f`.
- `resultados.json` (138.000 B, md5 `bb49ec3b6c073b707f68e8d715a75b93`): sólo en brain-env, `/workspace/escape/rama/results/liquida_entrenada_2026-10-11/`.
- `docs/agents/CONTEXTO-drosophila-fep.md` actualizado en este commit.
- Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-21197. Banners de corrección en los Docs de la 009 y la 011.

## 5. NO MEDIDO

- **Control de parámetros:** un brazo no líquido con los mismos 78 (o 1.378) parámetros, por ejemplo ganancias de entrada entrenables. Sin esto no se separa «líquida» de «más parámetros». Es el falsador que sigue.
- La líquida entrenada sobre SL y S: ¿sigue importando el cableado de la mosca cuando la τ se entrena?
- Condiciones nuevas (ángulos, velocidades y ruido fuera de los entrenados) y el modelo de entrada alternativo.
- Costo Q15 y latencia de LIQ_DIAG en ESP32.
- Segunda máquina, hardware, review externo. Silencio no es aprobación.

## 6. QA

Rúbrica 55/60 → 92/100; N/A 40 (Seguridad 15, Testing 15, DevOps 10). Pre-registro antes de entrenar, controles en el mismo run, guarda de punto de partida, prueba con ruido separado, md5 verificados en clon fresco. Deuda: sin PR ni review, un solo modelo de entrada, control de parámetros pendiente.

--- METODO PROMETEO ---
Máquina: brain-env (Celeron N4020, Python 3.12.14, numpy 2.5.3); sandbox de ClickUp para escribir el script
Artefactos: `docs/agents/respuestas/2026-10-11-012-la-liquida-entrenada-paga-en-el-escape.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21197
