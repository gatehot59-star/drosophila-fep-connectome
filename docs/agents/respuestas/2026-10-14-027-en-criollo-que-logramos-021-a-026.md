# 2026-10-14-027 · En criollo: la mosca no decide en el cerebro de qué lado girar; manda las dos señales y la resta va más abajo

## Pedido
Abraham, 14-oct 20:56: «en criollo que logramos». Con los Docs del 12-oct (la 011, «No es la neurona») y del 13-oct (la 020, «Donde entramos: de portero») seleccionados.

## Veredicto primero
- [MEDIDO] **El programa que usa solo las conexiones que la mosca tiene pierde 5,4 puntos** contra el que resta el otro lado. Casi todo se pierde con el objeto que viene de frente en vuelo: en vez de aterrizar, gira. Lo confirmaron dos máquinas: brain-env y Actions x64 dieron igual en 38 de 38 líneas (2026-10-14-022).
- [MEDIDO] **En el cerebro, hasta dos saltos, nada frena ese giro.** Revisamos siete frenos posibles, fijados antes de mirar, y los siete dieron vacío. Lo único que inhibe a DNp06 viene de su mismo lado: LHAD1g1, que le da el 11 a 13 % de su inhibición. Lo confirmaron las dos máquinas (2026-10-14-024).
- [MEDIDO en la literatura] **DNp06 responde a los dos ojos** (Jang 2023, Kim 2023). En la mosca, lo del otro lado suma; el programa lo resta (2026-10-14-025).
- [CONCLUSIÓN] **El cerebro de la mosca no decide de qué lado girar: manda las dos DNp06 encendidas, y el lado se decidiría más abajo, en el cordón nervioso.** La resta del programa es esa decisión, puesta en el lugar equivocado.
- [HECHO] **Topo v0.2 lo puede escribir:** las dos DNp06 leen su lado y una comparación «aguas abajo» decide el lado. Contra el conectoma, las 10 flechas del cerebro están cableadas y las 4 de la comparación quedan para el cordón nervioso (2026-10-14-026).
- [NO MEDIDO] Que esa comparación exista en el cordón nervioso. Es H_COMPARADOR en BANC, sin sellar.

## En criollo, qué logramos
1. **Encontramos dónde se equivocaba nuestro programa respecto de la mosca, y por qué igual andaba.** Restaba el otro lado adentro de DNp06, y esa cuenta no está en el cerebro. Sin ella, el programa confunde «de frente» con «de costado».
2. **Descartamos con datos el lugar obvio donde la mosca podría hacer esa cuenta.** No está en el cerebro cerca de DNp06. Y la literatura dice que DNp06 hasta responde al ojo contrario: el otro lado suma.
3. **Llegamos a una hipótesis concreta y falsable para el Paper 3:** el lado del giro se decide en el cordón nervioso, comparando las dos DNp06. Se puede chequear con BANC, que tiene cerebro y cordón y ya está en la máquina.
4. **El lenguaje creció con criterio.** Topo v0.2 dice dónde ocurre cada cuenta, y el chequeo contra el conectoma separa lo que es del cerebro de lo que es de más abajo.
5. **El método se sostuvo.** Dos hipótesis refutadas limpias, cada una con su control que podía dar rojo. Un instrumento que dio rojo en su prueba antes de tocar datos y se corrigió. Y una prueba que no podía dar rojo, la de v0.2 en el banco, no se selló. Te la había ofrecido en la 025, y estuvo mal.

## Con los dos Docs que seleccionaste
- **El del 12-oct («No es la neurona»)** ya había nombrado a LHAD1g1 y a PVLP010 como inhibitorias de las descendentes, y LHAD1g1 con 5,2 % de su entrada desde los detectores visuales. Hoy, con otro script, la izquierda da 5,16 %. Coincide, aunque no es independiente: son los mismos datos. Y hoy sabemos algo más: inhiben a DNp06 solo de su mismo lado.
- **El del 13-oct («Donde entramos»), la demo cámara a vibración:** esto le pega directo. La pieza de mosca sola dice «peligro» por cada lado, pero no decide limpio de qué lado vibrar. Hay que poner después una resta izquierda menos derecha, que en el microcontrolador es una cuenta. Sin esa resta, un objeto de frente haría vibrar del lado equivocado. Con ruido alto, en cambio, la pieza sin resta gira mejor (hasta 22 puntos, 2026-10-14-022), así que la resta tiene un costo y hay que medirlo en la demo. Nada de esto vio todavía un píxel: el puente de píxeles sigue sin hacer.

## Qué no tenemos
- H_COMPARADOR en BANC.
- La dinámica: si la resta la hace el tiempo y no un cable.
- Cómo responde DNp06 a un objeto de frente: no está medido en lo leído.
- El puente de píxeles para la demo.
- H_DEBILES, que sigue corriendo (run 38635900391, desde las 17:53).

## Evidencia de la confirmación en Actions
| Qué | brain-env | Actions x64 (runnervmmprz5, Python 3.12.15) | Cotejo |
|---|---|---|---|
| H_TOPO_FIEL | −0,0541, IC90 [−0,0592; −0,0490], REFUTADA | igual (run 38641915842) | 38/38 líneas iguales salvo máquina y tiempos |
| Prueba fiel | 8/8 | 8/8 | igual |
| H_FRENO | REFUTADA, control PASA | igual (run 38652439698) | 34 de 36 líneas iguales; las 2 distintas son dos tipos empatados en 98 sinapsis que salen en otro orden en el top 10 descriptivo |
| Prueba freno | 6/6 | 6/6 | igual |
| Insumos | 3d802fd5 / 719904ab | 3d802fd5 / 719904ab | igual |

El orden de los empates no es estable entre máquinas: es un defecto chico del instrumento descriptivo, sin efecto en ningún veredicto. Lo dejo declarado y no lo cambio, porque está sellado.

## Herramientas y máquina
- brain-env: clon limpio, `git show` de los resultados del bot y `cotejar_logs.py` (8a8f7f79), que saca máquina, fecha y tiempos y compara línea por línea.
- La API de GitHub para el estado de los runs.
- Los dos Docs seleccionados, leídos completos.
- Acción delicada: ninguna.

## Archivos
| Archivo | md5 |
|---|---|
| `tools/cotejo/cotejar_logs.py` | 8a8f7f79416e0a5a76a4579c743c270d |
| `results/topo_fiel_2026-10-14/banco.log` (rama `titan/topo-fiel-2026-10-14`, bot) | 08c02f530a98c0a4ac5e0759e4f23ac4 |
| `results/frena_giro_2026-10-14/freno.log` (rama `titan/frena-giro-2026-10-14`, bot) | f7102afe62daaaf10532eea281e484f5 |
| `tools/contexto/actualizar_contexto_2026-10-14-027.py` | 3c5b5590d716e38b91039eebd9048c76 |

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| Las dos máquinas dan igual | cotejar_logs.py | Sí: en el freno marcó 2 líneas distintas |
| El freno no está en el cerebro | freno_mosca, sellado | Sí: con DNp01 dio CANDIDATO |
| El lado se decide abajo | inferencia | CONCLUSIÓN; el falsador es H_COMPARADOR |
| Le pega a la demo | inferencia sobre la 2026-10-13-020 | CONCLUSIÓN; la demo no existe todavía |

--- METODO PROMETEO ---
Antes de resumir, confirmar en la segunda máquina. Leer los Docs seleccionados y cruzarlos con lo de hoy. Separar MEDIDO, CONCLUSIÓN y NO MEDIDO. Declarar el defecto que apareció en el cotejo, aunque no cambie nada.
