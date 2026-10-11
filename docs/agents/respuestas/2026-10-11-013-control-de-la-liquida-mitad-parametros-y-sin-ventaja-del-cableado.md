# 2026-10-11-013 · Control de la 012: la ventaja de la líquida diagonal era de parámetros, la plena sí gana por ser líquida, y con líquida entrenada el cableado fino ya no se distingue de SL

**Doc público:** https://app.clickup.com/90171457413/docs/2kza6fw5-21217

## 1. Pedido

Botón «Correr el control: mismos parámetros y cableado barajado» (ofrecido en la 012), y después «Cerrar la 013: subir evidencia, Doc y CONTEXTO».

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, 2 procesos, Python 3.12.14, numpy 2.5.3): humo, corrida de 43,12 min y verificación en clon fresco.
- **Sandbox de ClickUp:** escritura del script.
- **GitHub:** pre-registro y md5 sellado en `d9cbdf9`; script y log en `d27edad`, rama `titan/escape-motivo-2026-10-11`.
- Script `tools/escape_motivo/control_parametros.py`, md5 `342069aa075256e55e6638127f55a05e`; importa `liquida_entrenada.py` de la 012 (md5 verificado).
- Acción delicada: NO.

## 3. Veredicto

**Mixto, y corrige a la 012.**

- **Diagonal (78 parámetros): la no líquida le gana a la líquida.** Con las mismas señales metidas en la entrada en vez de en la τ (pre_i = (Wz)_i + x_i + gx_i·x_i + gh_i·z_i, τ fija entrenable): 0,9443 contra 0,9216; McNemar 149 contra 77, p = 1,9e-06 → PEOR. La ventaja diagonal de la 012 era de parámetros.
- **Plena (1.378): la líquida gana.** Contra pre = Wz + x + Gx·x + Gh·z con τ fija: 0,9826 contra 0,9214; 252 contra 12, p = 1,3e-59 → MEJOR, 4/4 semillas. Acá la liquidez sí suma, aunque la no líquida plena es inestable entre semillas (0,851 a 0,972) y puede ser un problema de optimización.
- **Cableado con la líquida entrenada: W NO GANA a SL.** W (diagonal, semilla 0) 0,9521; SL media 0,8488, máximo 0,9573; 1 de 24 la iguala, p = 0,08. Con la peor semilla de W, 6 de 24 (p 0,28). S, descriptivo: media 0,7771, 0 de 8 igualan a W.
- La 012 se reproduce exacta (REPRODUCE_012=True).

**Log, líneas verbatim** (`results/control_parametros_2026-10-11/run.log`, md5 `f9af5bd79ef9c618dc59a912ff055dff`, 53 líneas, en `d27edad`):

```
CHEQUEO INSTRUMENTO VALIDO
GUARDA redes_nulas_ok=True SL=24 S=8
GUARDA punto_de_partida_igual=True seg_por_evaluacion=0.077
RESUMEN_W brazo=LIQ_DIAG comb_prueba_media=0.9216 min=0.9073 max=0.9521 por_semilla=0.9521,0.9146,0.9125,0.9073
RESUMEN_W brazo=NOLIQ_DIAG comb_prueba_media=0.9443 min=0.8917 max=0.9802 por_semilla=0.9313,0.9740,0.8917,0.9802
RESUMEN_W brazo=LIQ_PLENA comb_prueba_media=0.9826 min=0.9802 max=0.9844 por_semilla=0.9802,0.9844,0.9812,0.9844
RESUMEN_W brazo=NOLIQ_PLENA comb_prueba_media=0.9214 min=0.8510 max=0.9719 por_semilla=0.8510,0.9594,0.9719,0.9031
REPRODUCE_012=True
CONTRASTE P1_LIQ_DIAG_vs_NOLIQ_DIAG acierto_A=0.8746 acierto_B=0.9067 solo_A=77 solo_B=149 p_mcnemar=1.923e-06 -> PEOR
CONTRASTE P2_LIQ_PLENA_vs_NOLIQ_PLENA acierto_A=0.9723 acierto_B=0.8652 solo_A=252 solo_B=12 p_mcnemar=1.315e-59 -> MEJOR
SEMILLAS LIQ_DIAG gana_a_NOLIQ_DIAG_en=2/4
SEMILLAS LIQ_PLENA gana_a_NOLIQ_PLENA_en=4/4
VEREDICTO_LIQUIDEZ=MIXTO (P1=PEOR, P2=MEJOR)
CONTRASTE Q_SL comb W_semilla0=0.9521 W_min=0.9073 SL_media=0.8488 SL_max=0.9573 n>=W0=1/24 p=0.0800 n>=Wmin=6/24 p_min=0.2800 -> W NO GANA
CONTRASTE Q_S comb W_semilla0=0.9521 W_min=0.9073 S_media=0.7771 S_max=0.9083 n>=W0=0/8 p=0.1111 n>=Wmin=1/8 p_min=0.2222 (descriptivo)
VEREDICTO_CABLEADO_CON_LIQUIDA=CON LA LIQUIDA ENTRENADA EL CABLEADO FINO NO SE DISTINGUE DE SL
minutos=43.12
EXIT_RUN=0
```

**ANTES DE FIRMAR: ¿podía dar rojo cada instrumento?**

| Afirmación | ¿Podía dar rojo? | Veredicto |
|---|---|---|
| La diagonal ganaba por parámetros | Sí: McNemar con mismo punto de partida y presupuesto (P2 dio lo contrario con el mismo código) | PASS |
| La plena gana por ser líquida | Sí | PASS, con la letra chica de optimización |
| Entrenada, la mosca no le gana a SL | Sí: con 0 de 24 daba p = 0,04 | PASS para W semilla 0; poder bajo con 24 redes |
| Script sin cambios después de ver datos | Sí | md5 sellado en `d9cbdf9` igual al de `d27edad` en clon fresco |

**Qué cambia:** la propuesta de la 012 para L2 (líquida diagonal) queda sin respaldo: con 78 parámetros rinde más meter las ganancias en la entrada. La líquida plena sigue ganando a su control. Con entrenamiento, la ventaja de la mosca sobre SL (011) ya no se ve: lo que se entrena compensa el cableado fino; la lateralidad sigue adelante contra S (descriptivo).

## 4. Archivos

- `tools/escape_motivo/PREREGISTRO-control-parametros.md` en `d9cbdf9`.
- `tools/escape_motivo/control_parametros.py` y `results/control_parametros_2026-10-11/run.log` en `d27edad`; md5 2/2 idénticos en clon fresco.
- `resultados.json` (313.682 B, md5 `a3da6f2e9af6e9046224443d9a267983`, con los θ): sólo en brain-env, `/workspace/escape/rama/results/control_parametros_2026-10-11/`.
- Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-21217. Banner de corrección en el Doc de la 012.
- `docs/agents/CONTEXTO-drosophila-fep.md` actualizado en este commit.

## 5. NO MEDIDO

- NOLIQ_PLENA con otro optimizador o más iteraciones (¿la diferencia plena es de liquidez o de optimización?).
- LIQ_PLENA sobre SL; más semillas de W y más redes SL.
- Condiciones nuevas, otro modelo de entrada, ESP32, segunda máquina, review externo.

## 6. QA

Rúbrica 53/60 → 88/100; N/A 40 (Seguridad 15, Testing 15, DevOps 10). Pre-registro sellado, controles válidos, reproducción exacta de la 012, md5 en clon fresco. −7: sin la plena sobre SL, poder bajo con 24 redes, sin PR ni review externo.

--- METODO PROMETEO ---
Máquina: brain-env (Celeron N4020, 2 procesos); sandbox de ClickUp para escribir el script
Artefactos: `docs/agents/respuestas/2026-10-11-013-control-de-la-liquida-mitad-parametros-y-sin-ventaja-del-cableado.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21217
