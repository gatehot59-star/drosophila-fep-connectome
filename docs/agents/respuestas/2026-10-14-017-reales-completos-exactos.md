# 2026-10-14-017 · Los dos reales completos dieron exacto: R2 0,9465 y núcleo 0,9135 por el camino nuevo; H_DEBILES puede correr

**Pedido:** «Chequeá ahora los dos reales completos» (Abraham, 14-oct 17:16).

## Veredicto primero
- [MEDIDO] Actions x64, corrida 38629138935, trabajo «humo (real)», guardado por el bot en `ca8221a` (rama `titan/debiles-2026-10-14`): el camino de las mezclas a tamaño completo (2.400 ensayos de entrenamiento y 2.000 de prueba; tau 0, prueba 2, celda 0,3|0,15) dio **R2 real 0,9465 y núcleo real 0,9135**. Son los valores ya medidos en el factorial 3 y en el núcleo. REAL_R2_IGUAL True, REAL_NUCLEO_IGUAL True, INSTRUMENTO VÁLIDO, EXIT 0, 666,8 s.
- [MEDIDO] MD5SUMS del bot: 10 de 10 OK. Prueba del agregador en Actions: PASA 7/7.
- [MEDIDO] Cruce con brain-env: las 4 líneas de la grilla de humo, iguales; en mezclas, las 3 líneas comunes, iguales (brain-env corrió una mezcla más, k 1).
- [CONCLUSIÓN] Se cumple la condición que puse para el CORRER: el script nuevo arma el mismo sujeto, los mismos ensayos y el mismo lector que las corridas que ya están en git.
- [NO MEDIDO] Los mismos reales a tamaño completo en brain-env: siguen corriendo (largaron 17:03; brain-env va unas 4,5 veces más lento que Actions).
- [NO MEDIDO] H_DEBILES no corrió. Espera el click de Abraham.

## Herramientas y máquina
Actions ubuntu-latest (runnervmmprz5, Linux 6.17 azure, Python 3.12.15, numpy 2.5.3, torch 2.14.1 cpu) para los reales; brain-env (Python 3.12.14, numpy 2.5.3) para el cruce línea por línea. Acción delicada: ninguna.

## Evidencia
- `results/debiles_2026-10-14_humo/debiles_humo_real.log`: «REAL R2=0.9465 nucleo=0.9135 | 658.0 s» y «CHEQUEO REAL_R2_IGUAL esperado=0.9465 -> True | REAL_NUCLEO_IGUAL esperado=0.9135 -> True».
- `debiles_humo_real_k000.json`: real_R2 0.9465, real_nucleo 0.9135, humo False, md5 del script f28404c2, todas las guardas True.

## Qué prueba y qué no
Prueba que el cableado del script nuevo es el correcto: mismo R2, mismo núcleo, mismos ensayos, mismas semillas, mismo lector. No es una medición independiente del simulador: usa las mismas funciones selladas que las corridas de antes. Para esta prueba eso alcanza, porque lo que se quiere es que la mezcla se compare contra R2 y el núcleo por el mismo camino.

## NO MEDIDO
- Los reales en brain-env (en curso).
- La corrida completa de H_DEBILES y sus dos veredictos.

## Antes de firmar
| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| R2 real igual | REAL_R2_IGUAL, igualdad a 1e-9 contra 0,9465 | sí: un ensayo distinto entre 2.000 lo mueve 0,0005 |
| núcleo real igual | REAL_NUCLEO_IGUAL contra 0,9135 | sí, igual |
| el bot guardó lo que corrió | MD5SUMS 10 de 10 | sí |
| no es humo | humo False en el json; el trabajo real corre sin --humo | sí |
| Actions y brain-env dicen lo mismo en el humo | cruce línea por línea | sí; dio iguales |

--- METODO PROMETEO ---
Inventario: Actions y brain-env medidos; la PC de Abraham no se usó. Contexto vivo: CONTEXTO md5 da64da6c (bot 5cc142f, la 016 aplicada). La corrida completa sigue esperando el click de Abraham.
