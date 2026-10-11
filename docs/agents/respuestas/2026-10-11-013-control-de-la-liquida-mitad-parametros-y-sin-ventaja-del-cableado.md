# 2026-10-11-013 · Control de la 012: la ventaja de la líquida era en buena parte de parámetros, y con líquida entrenada el cableado fino ya no se distingue de SL

## 1. Pedido

Botón «Correr el control: mismos parámetros y cableado barajado» (ofrecido en la 012).

## 2. Herramientas y máquina

brain-env (Celeron N4020, 2 procesos, numpy 2.5.3), 43,12 min. Script `tools/escape_motivo/control_parametros.py`, md5 `342069aa075256e55e6638127f55a05e`, sellado con su pre-registro en `d9cbdf9` (rama `titan/escape-motivo-2026-10-11`) antes de entrenar. Importa `liquida_entrenada.py` de la 012 (md5 verificado).

## 3. Veredicto

**Mixto, y corrige a la 012.**

- **Diagonal (78 parámetros): la no líquida le gana a la líquida.** Con las mismas señales metidas en la entrada en vez de en la τ: 0,9443 contra 0,9216; McNemar 149 contra 77, p = 1,9e-06 → PEOR. La ventaja diagonal de la 012 era de parámetros.
- **Plena (1.378): la líquida gana.** 0,9826 contra 0,9214; 252 contra 12, p = 1,3e-59 → MEJOR, 4/4 semillas. Acá la liquidez sí suma, aunque la no líquida plena es inestable entre semillas (0,851 a 0,972) y puede ser un problema de optimización.
- **Cableado con la líquida entrenada: W NO GANA a SL.** W (diagonal, semilla 0) 0,9521; SL media 0,8488, máximo 0,9573; 1 de 24 la iguala, p = 0,08. Con la peor semilla de W, 6 de 24 (p 0,28). S, descriptivo: media 0,7771, 0 de 8 igualan a W.
- La 012 se reproduce exacta (REPRODUCE_012=True).

**Log, líneas verbatim** (`run.log`, md5 `f9af5bd79ef9c618dc59a912ff055dff`, 53 líneas, en brain-env):

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

**Qué cambia:** la propuesta de la 012 para L2 (líquida diagonal) queda sin respaldo: con 78 parámetros rinde más meter las ganancias en la entrada. La líquida plena sigue ganando a su control. Con entrenamiento, la ventaja de la mosca sobre SL (011) ya no se ve: lo que se entrena compensa el cableado fino; la lateralidad sigue pagando contra S.

## 4. Archivos

- Pre-registro y md5 sellado: `tools/escape_motivo/PREREGISTRO-control-parametros.md` en `d9cbdf9`.
- **Deuda:** el script, `run.log` y `resultados.json` (md5 `a3da6f2e9af6e9046224443d9a267983`) están en brain-env, `/workspace/escape/rama/`, sin push a la rama. Falta subirlos y verificar el md5 en clon fresco.
- Este archivo. No hay Doc de ClickUp todavía; `CONTEXTO-drosophila-fep.md` no está actualizado.

## 5. NO MEDIDO

- Verificar en clon fresco el md5 del script commiteado (no subido todavía).
- NOLIQ_PLENA con otro optimizador o más iteraciones (¿la diferencia plena es de liquidez o de optimización?).
- LIQ_PLENA sobre SL; más semillas de W contra SL.
- Condiciones nuevas, otro modelo de entrada, ESP32, segunda máquina, review externo.

## 6. QA

Pre-registro sellado, controles válidos, reproducción exacta de la 012. Deuda: evidencia sin push, sin Doc, sin CONTEXTO. Rúbrica 50/60 → 83/100; N/A 40.

--- METODO PROMETEO ---
Máquina: brain-env
Artefactos: `docs/agents/respuestas/2026-10-11-013-control-de-la-liquida-mitad-parametros-y-sin-ventaja-del-cableado.md`
