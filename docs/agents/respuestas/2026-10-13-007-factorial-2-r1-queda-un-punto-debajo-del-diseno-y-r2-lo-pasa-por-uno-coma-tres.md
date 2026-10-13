# 2026-10-13-007 · Factorial 2 leído: con los mismos sensores, R1 queda un punto debajo de su diseño y R2 lo pasa por 1,3

## Veredicto

- **[MEDIDO] VÁLIDO.**
  - 29 de 29 trabajos y el agregado terminaron con éxito (corrida `38396946950`, 55 min).
  - El bot commiteó los resultados en `798ed97`, con `MD5SUMS.txt` 59 de 59 OK.
  - El ancla reproduce la 015 **exacta** (6/6).
  - TAU_DN_IGUAL da True en las 10 semillas y REGLA40_IGUAL da True en 60 claves. El plan quedó completo en las 7 configuraciones.
- **[MEDIDO] La primaria es la diferencia con la regla que usa los mismos sensores.** Margen 0,01, IC al 98,57 %, en puntos:

| Configuración | W | Regla propia | Diferencia | IC | Veredicto sellado |
|---|---|---|---|---|---|
| M46_TASA | 0,8959 | 0,9022 | −0,62 | [−1,38; +0,08] | NO_SUPERIOR |
| M46_LIQ | 0,8838 | 0,9022 | −1,83 | [−2,49; −1,24] | PIERDE |
| R1_CON_TASA | 0,9199 | 0,9301 | −1,02 | [−2,43; +0,17] | NO_SUPERIOR |
| R1_CON_LIQ | 0,9158 | 0,9301 | −1,42 | [−3,02; −0,09] | NO_SUPERIOR |
| R1_SIN_TASA | 0,9153 | 0,9301 | −1,48 | [−3,36; −0,15] | NO_SUPERIOR |
| R1_SIN_LIQ | 0,9196 | 0,9301 | −1,05 | [−3,09; +0,38] | NO_SUPERIOR |
| **R2_CON_TASA** | **0,9412** | 0,9284 | **+1,28** | **[+0,79; +1,77]** | **NO_INFERIOR** |

- **[MEDIDO] Hipótesis selladas:** H_ALCANZA queda SIN_DECIDIR (ningún R1_CON da PIERDE ni EQUIVALENTE) y H_SUPERA NO SOSTENIDA (ninguna R supera por más de 1 punto).
- **[CONCLUSIÓN] R1 no alcanza a su diseño.** Con 100 corridas por configuración queda alrededor de 1 punto abajo, y en dos de las cuatro configuraciones el intervalo excluye el cero. **Esto corrige la 002 y la 003:** el "IGUALA 6/6" del post-hoc salía de una sola semilla.
- **[CONCLUSIÓN] R2 es lo primero que le gana a su diseño con los mismos sensores.** Las 33.489 neuronas sacan +1,28 puntos, con el intervalo entero arriba de cero y positivo en las 6 celdas (de +0,81 a +1,67; SUPERA en amplitud 0 y ruido 0,15). La ventaja es chica: no pasa el margen de 1 punto que sellamos, así que **no se puede decir "supera" según lo pre-registrado**. Además R2 tiene sólo 3 × 5 semillas, un intervalo que declaramos grueso antes de correr.
- **[MEDIDO] Contrastes** (α' = 0,05/9):
  - **SENSORES:** la regla de 418 le gana a la de 40 por +2,79 (AYUDA).
  - **RECORTE R1 menos M46:** +2,39 con TASA (NO_INFERIOR) y +3,20 con LIQ (AYUDA).
  - **RECORTE R2 menos R1:** +1,65 (NO_INFERIOR).
  - **LIQ:** en M46, −1,21 (NO_SUPERIOR); en R1, ±0,4 (EQUIVALENTE con y sin inhibición).
  - **INHIBICIÓN en R1:** +0,46 con TASA y −0,38 con LIQ, sin efecto claro.
- **[CONCLUSIÓN] La tendencia es que más cableado real da más acierto:** M46 0,896, R1 0,920, R2 0,941 (TASA). Recién con R2 el cableado deja de ir detrás de su plano.

## Pedido

ClickKit `leer_factorial2_006` (13-oct, 11:40).

## Herramientas y máquina

- **brain-env:**
  - API pública de Actions (corridas y trabajos);
  - clones de `titan/factorial2-mosca-2026-10-13` (`798ed97`), de main (`48d1f32`) y de `titan/v2-cierre-2026-10-12` (`1f4a2e0`);
  - `md5sum -c`;
  - prueba del parche del CONTEXTO.
- **GitHub MCP:** este commit en main.
- **Actions:** el workflow de este commit aplica el parche del CONTEXTO y se retira. Sin cuota ajena.

## Qué se midió

- **El agregado** (`agregado.log`, md5 `417fb214…`; `MD5SUMS.txt`, md5 `70a9acf7…`).
- **Duración de los trabajos:**
  - el ancla, 6,3 s;
  - el R1 más largo, 1.722,1 s;
  - el R2 más largo, 1.892,3 s (31,5 min), lejos del techo de 2,7 h estimado en la 004.
- **Versiones:** Linux 6.17 en Azure, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, pyarrow 25.0.1 y torch 2.14.1+cpu, las mismas que en el factorial 1.
- **Lo de la 005 y la 006:**
  - el CONTEXTO lo aplicó el bot en `48d1f32` (md5 `13e8469b…`);
  - F01, F06 y F07 los aplicó el bot en `1f4a2e0` (manuscrito `2fa575c4…` y sección de dos saltos `23db9cac…`, iguales a la prueba);
  - los dos workflows se retiraron.

## Evidencia cruda

```
run completed success 2026-10-13T13:18:31Z
Counter({('completed', 'success'): 30})
fix completed success 2026-10-13T12:49:42Z
798ed97 medicion(2026-10-13-004): factorial 2 de la mosca en Actions x64, 29 trabajos y agregado
CHEQUEO ANCLA_015 presente=True valido=True -> True
CHEQUEO TAU_DN_IGUAL semillas=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] -> True
CHEQUEO REGLA40_IGUAL claves=60 -> True
CHEQUEO PLAN M46_TASA=completo M46_LIQ=completo R1_CON_TASA=completo R1_CON_LIQ=completo R1_SIN_TASA=completo R1_SIN_LIQ=completo R2_CON_TASA=completo
PRIMARIA margen=0.010 B=20000 alfa_por_lado=0.00714 (nivel del intervalo 0.9857)
PRIMARIA M46_TASA W=0.8959 regla_propia=0.9022 dif=-0.0062 IC=[-0.0138, +0.0008] corridas=600 -> NO_SUPERIOR
PRIMARIA M46_LIQ W=0.8838 regla_propia=0.9022 dif=-0.0183 IC=[-0.0249, -0.0124] corridas=600 -> PIERDE
PRIMARIA R1_CON_TASA W=0.9199 regla_propia=0.9301 dif=-0.0102 IC=[-0.0243, +0.0017] corridas=600 -> NO_SUPERIOR
PRIMARIA R1_CON_LIQ W=0.9158 regla_propia=0.9301 dif=-0.0142 IC=[-0.0302, -0.0009] corridas=600 -> NO_SUPERIOR
PRIMARIA R1_SIN_TASA W=0.9153 regla_propia=0.9301 dif=-0.0148 IC=[-0.0336, -0.0015] corridas=600 -> NO_SUPERIOR
PRIMARIA R1_SIN_LIQ W=0.9196 regla_propia=0.9301 dif=-0.0105 IC=[-0.0309, +0.0038] corridas=600 -> NO_SUPERIOR
PRIMARIA R2_CON_TASA W=0.9412 regla_propia=0.9284 dif=+0.0128 IC=[+0.0079, +0.0177] corridas=90 -> NO_INFERIOR
  CELDA R2_CON_TASA 0.0|0.15 dif=+0.0167 IC=[+0.0115, +0.0215] -> SUPERA
  CELDA R2_CON_TASA 0.0|0.45 dif=+0.0159 IC=[+0.0091, +0.0226] -> NO_INFERIOR
  CELDA R2_CON_TASA 0.3|0.15 dif=+0.0135 IC=[+0.0079, +0.0197] -> NO_INFERIOR
  CELDA R2_CON_TASA 0.3|0.45 dif=+0.0134 IC=[+0.0090, +0.0179] -> NO_INFERIOR
  CELDA R2_CON_TASA 0.6|0.15 dif=+0.0090 IC=[+0.0025, +0.0165] -> NO_INFERIOR
  CELDA R2_CON_TASA 0.6|0.45 dif=+0.0081 IC=[+0.0036, +0.0142] -> NO_INFERIOR
  CELDA M46_TASA 0.0|0.45 dif=+0.0291 IC=[+0.0204, +0.0381] -> SUPERA
  CELDA M46_TASA 0.6|0.15 dif=-0.0382 IC=[-0.0477, -0.0295] -> PIERDE
  CELDA M46_TASA 0.6|0.45 dif=-0.0363 IC=[-0.0438, -0.0287] -> PIERDE
CONTRASTE INHIB_R1_TASA dif=+0.0046 IC=[-0.0046, +0.0130] -> NO_INFERIOR
CONTRASTE INHIB_R1_LIQ dif=-0.0038 IC=[-0.0150, +0.0072] -> NO_SUPERIOR
CONTRASTE LIQ_M46 dif=-0.0121 IC=[-0.0153, -0.0089] -> NO_SUPERIOR
CONTRASTE LIQ_R1_CON dif=-0.0040 IC=[-0.0072, -0.0011] -> EQUIVALENTE
CONTRASTE LIQ_R1_SIN dif=+0.0043 IC=[+0.0009, +0.0083] -> EQUIVALENTE
CONTRASTE RECORTE_R1_TASA dif=+0.0239 IC=[+0.0097, +0.0356] -> NO_INFERIOR
CONTRASTE RECORTE_R1_LIQ dif=+0.0320 IC=[+0.0174, +0.0453] -> AYUDA
CONTRASTE RECORTE_R2_TASA taus=3 pruebas=5 dif=+0.0165 IC=[+0.0093, +0.0278] -> NO_INFERIOR
CONTRASTE SENSORES (regla 418 menos regla 40) pruebas=10 dif=+0.0279 IC=[+0.0212, +0.0344] -> AYUDA
HIPOTESIS H_ALCANZA -> SIN_DECIDIR
HIPOTESIS H_SUPERA -> NO SOSTENIDA
VEREDICTO_GLOBAL -> VALIDO | M46_TASA=NO_SUPERIOR M46_LIQ=PIERDE R1_CON_TASA=NO_SUPERIOR R1_CON_LIQ=NO_SUPERIOR R1_SIN_TASA=NO_SUPERIOR R1_SIN_LIQ=NO_SUPERIOR R2_CON_TASA=NO_INFERIOR
EXIT_AGREGADO=0
417fb214f13fe874ef31af901b82f4b5  agregado.log
70a9acf73330397927864cc2c979c60c  MD5SUMS.txt
# duracion_s: ANCLA 6.3 | R1 max 1722.1 | R2 max 1892.3
48d1f32 contexto(2026-10-13-005) ... 13e8469b9fc233addba9c093913a5fd4  docs/agents/CONTEXTO-drosophila-fep.md
1f4a2e0 docs(v2): corrige F01, F06 y F07 ... 2fa575c4... paper1-v2.0.md | 23db9cac... SECCION-V2-DOS-SALTOS.md
# parche del CONTEXTO (copia en brain-env)
fa274aec816a578ff74779c2499ae403  parche.py
md5 antes 13e8469b9fc233addba9c093913a5fd4 -> md5 despues e2d4b55b612ce1dc11e053b98b3dad96 PARCHE OK (428 lineas)
```

## Archivos

- **Resultados:** rama `titan/factorial2-mosca-2026-10-13`, `results/factorial2_2026-10-13/` (bot `798ed97`), con 29 logs, 29 json, 29 archivos de versiones, `agregado.log` y `MD5SUMS.txt`.
- **main:**
  - este archivo;
  - `tools/contexto/actualizar_contexto_2026-10-13-007.py` (md5 `fa274aec…`);
  - `.github/workflows/contexto-2026-10-13-007.yml`, que debe dejar el CONTEXTO en md5 `e2d4b55b…`.

## NO MEDIDO

- **Si R2 supera por más de 1 punto.** Hace falta replicarlo con 10 × 10 semillas (un factorial 3, sellado antes de correr).
- **R2 sin inhibición, R2 con LIQ y los nulos SL/T de R2.** Sin los nulos no sabemos si R2 le gana a sus barajados.
- **La varianza del entrenamiento**, porque hay una sola semilla de entrenamiento.
- **Por qué la regla de 564 entradas (0,9284) no supera a la de 418 (0,9301).** Usan semillas de prueba distintas (2..6 contra 2..11) y no son comparables directo.
- **El render de la v2 desde `1f4a2e0`, el json de depósito y `--verificar`.**

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| La corrida es válida | Ancla exacta, TAU_DN_IGUAL, REGLA40_IGUAL, plan completo y MD5SUMS | Sí: cualquiera de los cinco podía fallar |
| R1 queda debajo | IC de dos vías sellado | Sí: podía dar EQUIVALENTE o positivo; en el post-hoc de una semilla daba IGUALA |
| R2 le gana a su regla | IC enteramente arriba de 0 | Sí: con el IC cruzando el 0 sería INDETERMINADO |
| R2 "supera" | **No se afirma**: el límite inferior del IC (+0,79) no pasa el margen (+1) | — |

```
--- METODO PROMETEO ---
Accion delicada: no (lectura y documentacion; el workflow solo edita el CONTEXTO y se retira)
Maquina: Actions x64 (corrida 38396946950) | brain-env (lectura, md5, prueba del parche)
Artefactos: docs/agents/respuestas/2026-10-13-007-factorial-2-r1-queda-un-punto-debajo-del-diseno-y-r2-lo-pasa-por-uno-coma-tres.md + Doc de ClickUp 2026-10-13-007
```
