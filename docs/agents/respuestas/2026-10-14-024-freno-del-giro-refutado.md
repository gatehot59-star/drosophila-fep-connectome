# 2026-10-14-024 · H_FRENO REFUTADA: en el cerebro, a dos saltos, nada frena el giro de DNp06 ante el looming frontal

## Pedido
Abraham, 14-oct 20:10, ClickKit `correr_freno_023`: correr H_FRENO con DNp06, tal como quedó sellado en la 023.

## Veredicto primero
- [HECHO] `CORRER` en `d74eaf3`; el workflow de Actions quedó disparado. El mismo instrumento sellado (`freno_mosca.py` 1318fefb, desde un clon limpio en `d74eaf3`) corrió en brain-env en 19,2 s.
- [MEDIDO] El control positivo PASA: LPLC1 y LPLC2 del mismo lado son el 13,6 % y el 13,0 % de la entrada excitatoria de DNp06, en los percentiles 0,981 y 0,982.
- [MEDIDO] **H_FRENO REFUTADA:** los 7 mecanismos dan DESCARTADO o AUSENTE.
  - Directos: DNp07, DNp01 y la DNp06 opuesta no le mandan ninguna sinapsis inhibitoria a DNp06.
  - Por interneurona, desde LPLC1 y LPLC2 del otro lado, llega el 0,86 % y el 0,40 % de su inhibición (percentiles 0,86 y 0,75).
  - Desde LPLC4, el 4,0 % y el 3,3 % (percentiles 0,69 y 0,67).
  - Desde DNp07 no llega nada.
  - Desde el detector bilateral, el 0,06 % y el 0,03 %.
- [MEDIDO, post hoc] **Las dos primeras inhibitorias de DNp06 son del mismo lado:**
  - LHAD1g1: una neurona GABA por lado, el 13,5 % y el 11,3 % de la inhibición de DNp06. Recibe LPLC2 (796 y 644 sinapsis) y LC4 del **mismo** lado e inhibe solo a la DNp06 de su lado.
  - PVLP010: glutamato, alimentada por LC4 del mismo lado (188 y 209), y también inhibe solo a la DNp06 de su lado.
- [CONCLUSIÓN] Es inhibición de avance: los mismos detectores que excitan a DNp06 la inhiben por una interneurona del mismo lado. Eso puede afinar o acortar la respuesta, pero no distingue un looming de frente de uno de costado.
- [CONCLUSIÓN] El freno que el banco necesita no está cableado en el cerebro a dos saltos. Quedan tres lugares posibles:
  1. El cordón nervioso, aguas abajo.
  2. La dinámica.
  3. Que un looming de frente no excite a DNp06 en la mosca. Esto último es un supuesto de nuestro modelo de entrada: la tarea enciende LPLC1 y LPLC2 de los dos lados ante el looming frontal. Ninguna de las tres está medida.
- [NO MEDIDO] La confirmación en Actions x64.

## Herramientas y máquina
- brain-env (Linux x86_64, Python 3.12.14, numpy 2.5.3, pandas 3.0.5).
- GitHub: `CORRER`, log y post hoc en la rama (`d2240a6`), md5 verificados desde un clon limpio.
- Acción delicada: ninguna.

## Archivos
| Archivo (rama `titan/frena-giro-2026-10-14`) | md5 |
|---|---|
| `results/frena_giro_2026-10-14_brainenv/freno.log` | c474e1f3f360a0cf84d398375aa4c698 |
| `tools/frena_giro/posthoc_lhad1g1.py` (post hoc, escrito después de ver el resultado) | 77b971bd7f9c0523c6965f8046158332 |
| `results/frena_giro_2026-10-14_brainenv/posthoc.log` | c7776bcb40c9520c366e809bb68a85a7 |
| `freno.json` (solo brain-env) | bb6c9c7b223f0754f99b30411771bab1 |
| `tools/contexto/actualizar_contexto_2026-10-14-024.py` (main) | ff6cdcfb90c94fa035864882338797b7 |

## NO MEDIDO
- Actions x64.
- Vías a más de dos saltos y el cordón nervioso.
- Si el looming frontal excita a DNp06 en la mosca: no está medido en lo que leí. El modelo de entrada de la 015 lo supone.
- El signo del glutamato de PVLP010: tomo la convención de Shiu, que es inhibitorio; en la mosca depende del receptor.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| REFUTADA | freno_mosca, sellado | Sí: en el humo, con DNp01, dio CANDIDATO; con DNp06 da todo descartado |
| Ve lo cableado | control positivo | Sí, y PASA |
| LHAD1g1 es del mismo lado | posthoc_lhad1g1.py | Sí: imprime los lados de entrada y de salida |
| Es post hoc | declarado | El script se escribió después de ver el resultado |

--- METODO PROMETEO ---
`CORRER` con el sí de Abraham. La corrida, desde un clon limpio del commit disparado. El veredicto, con la regla sellada. El post hoc, separado del veredicto y con su script commiteado. Las tres explicaciones que quedan están marcadas como NO MEDIDO.
