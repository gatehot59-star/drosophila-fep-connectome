# 2026-10-11-014 · La τ líquida plena aguanta el control: gana a su no líquida con optimización ajustada y con ella la mosca le gana a SL

**Doc público:** https://app.clickup.com/90171457413/docs/2kza6fw5-21237

## 1. Pedido

Botón «Correr la plena: otro optimizador y sobre SL» (ofrecido al cerrar la 013). La 013 dejó abierto si la plena ganaba por ser líquida o porque a la no líquida le costaba entrenar, y si con ella seguía pagando el cableado fino.

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, 2 procesos, Python 3.12.14, numpy 2.5.3): humo, corrida de 48,79 min, md5 en clon fresco.
- **Sandbox de ClickUp:** escritura del script.
- **GitHub:** pre-registro y md5 sellado en `be292b0`; script y log en `f0d0c1c`, rama `titan/escape-motivo-2026-10-11`.
- Script `tools/escape_motivo/control_plena.py`, md5 `45bad2a84d625f8826b84876bef87133`; importa `control_parametros.py` de la 013 (md5 verificado).
- Acción delicada: NO.

## 3. Veredicto

**Sí a las dos.**

- **P3, optimización ajustada:** cada semilla de cada brazo se entrenó con C1 (σ 0,10, lr 0,05) y C2 (σ 0,03, lr 0,02), 60 iteraciones, y se eligió por entrenamiento. LIQ_PLENA 0,9854 (desvío 0,0041) contra NOLIQ_PLENA 0,9453 (desvío 0,0506); McNemar 169 contra 15, p = 3,6e-34 → **MEJOR**, 4/4 semillas.
- **Q_SL_PLENA:** con el protocolo de la 012, W 0,9802 contra 24 SL (media 0,9090, máximo 0,9760); 0/24, p = 0,04 → **W GANA**. Con la líquida plena, el cableado fino vuelve a pagar.
- REPRODUCE_012=True.

**Análisis de desempate, hecho después de la corrida y NO pre-registrado:** en NOLIQ_PLENA, las semillas 1, 2 y 3 empataron en entrenamiento (1,0 con C1 y con C2) y `max` eligió C1, el primero en orden. Si a la no líquida se le da el mejor de los dos mirando la prueba (ventaja injusta), saca 0,9510 / 0,9844 / 0,9719 / 0,9844, media 0,9729; la líquida (0,9802 / 0,9875 / 0,9896 / 0,9844) queda arriba en 3 semillas y empata en 1. La diferencia se achica, pero no se da vuelta.

**Descriptivo:** la no líquida llega a 1,0 de entrenamiento en 7 de 8 corridas y cae en prueba; la líquida generaliza mejor.

**Log, líneas verbatim** (`results/control_plena_2026-10-11/run.log`, md5 `dbfb8f124489945526f3899e1e477ff1`, 59 líneas, en `f0d0c1c`):

```
CHEQUEO INSTRUMENTO VALIDO
GUARDA redes_nulas_ok=True SL=24
GUARDA punto_de_partida_igual=True seg_por_evaluacion=0.080
RESUMEN_AJUSTADO brazo=LIQ_PLENA comb_prueba_media=0.9854 desvio=0.0041 min=0.9802 max=0.9896 por_semilla=0.9802,0.9875,0.9896,0.9844 configs=C1,C1,C1,C1
RESUMEN_AJUSTADO brazo=NOLIQ_PLENA comb_prueba_media=0.9453 desvio=0.0506 min=0.8719 max=0.9844 por_semilla=0.8719,0.9844,0.9719,0.9531 configs=C2,C1,C1,C1
CONTRASTE P3_LIQ_PLENA_vs_NOLIQ_PLENA_ajustadas acierto_A=0.9750 acierto_B=0.9062 solo_A=169 solo_B=15 p_mcnemar=3.569e-34 -> MEJOR
SEMILLAS LIQ_PLENA gana_a_NOLIQ_PLENA_ajustada_en=4/4
VEREDICTO_PLENA=LA PLENA GANA POR SER LIQUIDA CON OPTIMIZACION AJUSTADA
REPRODUCE_012=True
CONTRASTE Q_SL_PLENA comb W=0.9802 SL_media=0.9090 SL_max=0.9760 n>=W=0/24 p=0.0400 -> W GANA
VEREDICTO_CABLEADO_CON_PLENA=CON LA LIQUIDA PLENA SIGUE PAGANDO EL CABLEADO FINO
minutos=48.79
EXIT_RUN=0
```

**ANTES DE FIRMAR:**

| Afirmación | ¿Podía dar rojo? | Veredicto |
|---|---|---|
| La plena gana por ser líquida con optimización ajustada | Sí: McNemar; en la 013 la diagonal dio PEOR con el mismo código | PASS; con el desempate más favorable a la no líquida, la diferencia se achica pero se mantiene |
| Con la plena, la mosca le gana a SL | Sí: en la 013 dio W NO GANA con la diagonal | PASS en el borde (p 0,04 es el mínimo con 24) |
| Script sin cambios después de ver datos | Sí | md5 sellado en `be292b0` igual al de `f0d0c1c` |

**Para BEEC v2 L2:** la candidata pasa a ser la τ líquida plena sobre el cableado fijo (1.378 parámetros, unos 5,5 KB en float32; costo en ESP32 NO MEDIDO). Decide Abraham.

## 4. Archivos

- `tools/escape_motivo/PREREGISTRO-control-plena.md` en `be292b0`.
- `tools/escape_motivo/control_plena.py` y `results/control_plena_2026-10-11/run.log` en `f0d0c1c`; md5 2/2 en clon fresco.
- `resultados.json` (md5 `f2792e6ae8d7a93cd972230b9f726242`, con los θ): sólo en brain-env.
- Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-21237. Banner en el Doc de la 013.
- `docs/agents/CONTEXTO-drosophila-fep.md` actualizado en este commit.

## 5. NO MEDIDO

- Más semillas de W y más redes SL (con 24, p no baja de 0,04).
- La plena sobre S; condiciones fuera de las entrenadas; el otro modelo de entrada.
- La plena en Q15 sobre ESP32; segunda máquina; review externo.

## 6. QA

Rúbrica 54/60 → 90/100; N/A 40. −6: desempate sin pre-registrar (declarado y analizado), p en el borde, sin PR ni review externo.

--- METODO PROMETEO ---
Máquina: brain-env (Celeron N4020, 2 procesos); sandbox de ClickUp para escribir el script
Artefactos: `docs/agents/respuestas/2026-10-11-014-la-liquida-plena-aguanta-el-control.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21237
