# 2026-10-14-022 · H_TOPO_FIEL REFUTADA en brain-env: sin la resta, el giro le gana al aterrizaje ante el looming frontal

## Pedido
Abraham, 14-oct 18:38, ClickKit `correr_topo_fiel_021`: correr H_TOPO_FIEL tal como quedó sellado en la 021.

## Veredicto primero
- [HECHO] `CORRER` en `0f83872` (rama `titan/topo-fiel-2026-10-14`). Actions quedó en cola detrás de H_DEBILES.
- [MEDIDO] El mismo instrumento sellado corrió completo en brain-env, desde un clon limpio en `0f83872` (`banco_fiel.py` ff0a7cbf), en 81 s. Todas las guardas en verde: md5, tarea VALIDA, CABLEADO_FIEL=10, CONTROL_GRAFO SIN_VIA_DIRECTA=4, REPRODUCE_M46.
- [MEDIDO] **H_TOPO_FIEL REFUTADA:** el fiel menos el que resta da −5,41 puntos, IC90 [−5,92; −4,90], en 12.000 ensayos con semillas nuevas. Pierde en las 6 celdas, de −1,55 a −7,40.
- [MEDIDO] CONTROL_ROJO REFUTADA (−27,97, IC90 [−28,68; −27,27]): el banco puede dar rojo y el veredicto vale.
- [MEDIDO, descriptivo] **Dónde pierde:** ante el looming frontal en vuelo pierde de 85 a 88 puntos. Aterriza el 6,5 a 7,1 % de las veces; el que resta, el 92 a 94 %.
- [MEDIDO, descriptivo] **Dónde gana:**
  - En el giro en vuelo gana hasta 22,5 puntos con ruido alto. Con ruido bajo empata (−0,2 a +7,4).
  - Ante la barra AD gana hasta 34,9 puntos con ruido alto.
  - En posada da exactamente igual.
- [MEDIDO, descriptivo] **Contra los otros dos:**
  - Contra `aterrizaje_dir.topo`, el fiel pierde 1,71 puntos (IC90 [−2,32; −1,09]).
  - Contra W (el cableado de la 015 sin entrenar), el fiel empata: +0,45, IC90 [−0,28; +1,19].
- [CONCLUSIÓN] La resta contralateral del programa hace un trabajo real: un looming de frente enciende las dos DNp06 por igual, y la resta las cancela para que gane el aterrizaje. La mosca no tiene esa vía directa, así que ese trabajo lo hace otra cosa. Esto lo deduzco del resultado, no lo medí.
- [CONCLUSIÓN] El fiel empata con W, que es el cableado real con la dinámica de la 015. Que el cableado sin resta empate con la regla sin resta es coherente con que el motivo de 46 neuronas tampoco tenga esa cancelación.
- [NO MEDIDO] La confirmación en Actions x64, que es una máquina distinta.

## Herramientas y máquina
- brain-env (Linux x86_64, Python 3.12.14, numpy 2.5.3).
- GitHub: `CORRER`, el log en la rama (`1930ed3`).
- Actions: en cola.
- Acción delicada: ninguna.

## Evidencia
| Celda (A, ruido) | fiel | el que resta | d | looming frontal en vuelo, fiel / resta | giro en vuelo, fiel / resta |
|---|---|---|---|---|---|
| 0,0 · 0,15 | 0,8560 | 0,9110 | −5,50 | 0,065 / 0,940 | 0,934 / 0,861 |
| 0,0 · 0,45 | 0,8205 | 0,8360 | −1,55 | 0,071 / 0,923 | 0,783 / 0,558 |
| 0,3 · 0,15 | 0,8605 | 0,9320 | −7,15 | 0,065 / 0,940 | 0,956 / 0,948 |
| 0,3 · 0,45 | 0,8445 | 0,8875 | −4,30 | 0,071 / 0,923 | 0,914 / 0,783 |
| 0,6 · 0,15 | 0,8605 | 0,9345 | −7,40 | 0,065 / 0,940 | 0,956 / 0,958 |
| 0,6 · 0,45 | 0,8485 | 0,9140 | −6,55 | 0,071 / 0,923 | 0,936 / 0,886 |

## Archivos
| Archivo | md5 |
|---|---|
| `results/topo_fiel_2026-10-14_brainenv/banco.log` (rama) | 5db974776ef76b7e680201ebcee23f1e |
| `topo_fiel.json` (solo brain-env) | d421e72cb34170e673ac24b98e41ab1a |
| `tools/contexto/actualizar_contexto_2026-10-14-022.py` | 1b7a94bf35efcdaaa9e3127603eedbde |

## NO MEDIDO
- La corrida en Actions x64.
- Qué circuito de la mosca frena el giro ante el looming frontal. Son candidatos a probar, no hallazgos: una inhibición de DNp07 sobre DNp06, una prioridad del aterrizaje, o una vía a más de dos saltos.
- H_DEBILES sigue corriendo.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| REFUTADA | decidir_fiel, sellado y probado | Sí: los escenarios de la prueba incluyen SOSTENIDA |
| El banco discrimina | control cruzado | Sí, y salió REFUTADA como debía |
| Es el instrumento sellado | md5 en el log | Sí: aborta con salida 2 si difiere |
| Independencia de máquina | falta | Declarado: Actions en cola |
| Corrida ciega | no lo es | Declarado en la 021: el humo usó las mismas semillas |

--- METODO PROMETEO ---
`CORRER` con el sí de Abraham. Corrida completa desde un clon limpio del commit disparado, en otra máquina mientras Actions espera. Veredicto con la regla sellada. Lo descriptivo, separado del veredicto. La explicación mecánica figura como CONCLUSIÓN y no como medida.
