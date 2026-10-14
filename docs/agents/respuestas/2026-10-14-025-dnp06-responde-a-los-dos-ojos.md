# 2026-10-14-025 · DNp06 responde a los dos ojos: la entrada del otro lado suma, no resta, y el lado del giro se decidiría aguas abajo

## Pedido
Abraham, 14-oct 20:17, ClickKit `frontal_dnp06_024`: chequear si un looming de frente enciende a DNp06 en la mosca. Es la tercera salida que dejó abierta la 024.

## Veredicto primero
- [MEDIDO en la literatura] **Jang, Goodman, Ausborn y von Reyn 2023**, *J Exp Biol* 226: jeb244790, "Azimuthal invariance to looming stimuli in the Drosophila giant fiber escape circuit":
  - Con un looming a ±45° que excita un solo ojo, "all DNs responded significantly to both stimuli, despite their unilaterally projecting dendrites". Los DN registrados fueron GF, DNp02 y DNp06.
  - DNp06 "showed large depolarizations and spikes".
  - Ojo: lo de DNp06 es **un solo ensayo** ("DNp06 trace is from a single trial", Fig. 1D).
  - El looming **frontal** lo midieron solo en GF.
  - La vía del ojo contrario es "an unidentified pathway".
- [MEDIDO en la literatura] **Kim, Park, Lee y Kim 2023**, *Curr Biol* 33: 321-335: "DNp06 neurons responded to spots moving in the contralateral visual field".
- [MEDIDO en la literatura, mismo laboratorio, no independiente] La tesis de Jang (Drexel), "Circuits for bilateral looming feature integration in Drosophila": "all looming responsive DNs such as DNp01, DNp02, DNp03, and DNp06 respond well to the contralateral looming stimulus".
- [CONCLUSIÓN] La tercera salida de la 024 (que un looming de frente no encienda a DNp06) queda floja. Si DNp06 responde al ojo contrario, con más razón responde al frente, aunque eso no está medido.
- [CONCLUSIÓN] En la mosca, la entrada del otro lado sobre DNp06 es **excitatoria**: suma. El programa hace lo contrario, la resta. Y esa entrada no aparece a dos saltos con sinapsis químicas (la 020 y la 024). FlyWire no tiene sinapsis eléctricas, y los autores hablan de una vía no identificada.
- [CONCLUSIÓN] Entonces DNp06 no lleva limpio el lado del estímulo, y el lado del giro se tiene que decidir aguas abajo: en el cordón nervioso, comparando las dos DNp06 o sumando otras descendentes. La resta del programa sería esa comparación, mal ubicada adentro de DNp06. NO MEDIDO.
- [NO MEDIDO] La respuesta de DNp06 a un looming de frente; la vía contralateral; la comparación en el cordón nervioso.

## Qué cambia para Topo
Un programa fiel a la mosca no tendría que restar adentro de DNp06. Tendría que dejar que las dos DNp06 se enciendan, incluso con el ojo contrario, y decidir el lado en una salida que compare izquierda contra derecha. Eso hoy no se puede escribir en Topo v0: hace falta una salida diferencial en v0.2. Si se sella, el falsador natural es que ese programa no recupere el aterrizaje ante el looming frontal que perdió el fiel en la 022.

## Herramientas y máquina
- Búsqueda web y lectura del artículo de Jang 2023 (texto completo abierto en journals.biologists.com). Kim 2023 y la tesis, por los fragmentos del buscador.
- Sin código nuevo y sin corridas.
- Acción delicada: ninguna.

## Archivos
| Archivo | md5 |
|---|---|
| `tools/contexto/actualizar_contexto_2026-10-14-025.py` | 584d2e19271e2238f36baead7933c23d |

## NO MEDIDO
- DNp06 ante un looming frontal.
- Cuánto responde DNp06 al ojo contrario frente al propio: es un solo ensayo.
- La vía contralateral (¿eléctrica?, ¿más de dos saltos?).
- La lectura en el cordón nervioso: FlyWire v783 es solo el cerebro; haría falta MANC o BANC.

## Antes de firmar
| Afirmación | Fuente | Fuerza |
|---|---|---|
| DNp06 responde al ojo contrario | Jang 2023 Fig. 1D | Débil: un ensayo, una mosca |
| DNp06 responde a puntos del campo contrario | Kim 2023 Fig. 7E | Moderada: otro laboratorio |
| Los DN de looming responden al contralateral | tesis de Jang | No independiente de Jang 2023 |
| Que el lado se decide aguas abajo | inferencia | CONCLUSIÓN, no medida |

--- METODO PROMETEO ---
Ir a la fuente primaria antes de sellar nada. Citar textual. Separar lo medido por otros de lo que deduzco. Declarar cuando una fuente es un solo ensayo.
