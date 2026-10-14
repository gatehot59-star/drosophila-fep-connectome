# 2026-10-13-019 · Liquid AI: hacen modelos tipo LLM, pero salen de entrenar con billones de palabras, no de copiar un gusano

## Veredicto

- **[LITERATURA] Sí, existe: Liquid AI.**
  - Salió del MIT CSAIL en 2023; la fundaron Ramin Hasani, Mathias Lechner, Alexander Amini y Daniela Rus, los inventores de las redes líquidas.
  - La idea original salió de *C. elegans*, el gusano de 302 neuronas.
  - Sus modelos LFM2 (2025) son modelos de lenguaje chicos, de 350 millones a 8.300 millones de parámetros, con pesos abiertos y hechos para correr en el dispositivo. El de 2.600 millones saca 82,41 % en GSM8K, problemas de matemática.
- **[LITERATURA] Ojo con lo que prueba.** Lo «loí quido» de LFM2 es un operador eficiente: convoluciones cortas con compuertas, sistemas lineales de primer orden. Va mezclado con bloques de atención como los de cualquier LLM: 10 de convolución y 6 de atención. **La inteligencia sale de entrenar con 10 a 12 billones de tokens**, con destilación y ajuste fino. Adentro no hay ningún cableado de gusano.
- **[CONCLUSIÓN] Entonces no dice que un cableado de mosca dé un LLM.** Dice dos cosas útiles:
  1. Hay mercado para modelos chicos y rápidos en el dispositivo: autos, drones, teléfonos.
  2. El primo directo de nuestras piezas es su trabajo de 2020: 19 neuronas inspiradas en el gusano manteniendo un auto en su carril (Lechner et al., Nature Machine Intelligence 2020). Eso es nivel reflejo, como lo nuestro.
- **[MEDIDO, nuestro] En nuestro banco la neurona líquida no agregó por sí sola.**
  - En el factorial 2, R1 con neurona líquida y R1 con neurona de tasa igualan las dos a la regla en 6 de 6 celdas.
  - En las pruebas del 12-oct, el acople SparseLTC a DBC3 empató con una LSTM: lo que pagó fue tener memoria, no el tipo de neurona.
- **[CONCLUSIÓN, opinión] La jugada buena es la combinación, no el reemplazo.** Un modelo chico tipo LFM para entender y planear, más piezas de mosca probadas para los reflejos de seguridad. Es la idea de DualBrain con dos piezas reales.

## Pedido

21:47: «HAY TRABJSO DE EMPRESAS CON NURONAS LIQUIDAS QUE LOGRARON REPRODUCIR INTLIGENCa artificial similar a los llm»

## Herramientas y máquina

- **Web:** dos búsquedas (informe técnico de LFM2, blog de Liquid AI, página de la empresa, TechCrunch y Wired).
- **Sin máquinas, sin cuota.** No se corrió nada; el factorial 4 sigue en Kaggle.

## Qué se midió

- Nada nuevo. Lo de nuestro banco sale del CONTEXTO (factorial 2, respuesta 2026-10-13-002) y de los Docs del 12-oct (acople SparseLTC a DBC3 contra LSTM).

## Evidencia cruda

- Amini, Hasani, Lechner, Rus y otros, «LFM2 Technical Report», arXiv 2511.23404 (2025). Del resumen:
  - «combines gated short convolutions with a small number of grouped query attention blocks»;
  - «The LFM2 family covers 350M-8.3B parameters»;
  - «Pre-trained on 10-12T tokens»;
  - «LFM2-2.6B reaches 79.56% on IFEval and 82.41% on GSM8K».
- Blog de Liquid AI (10-07-2025): «LFM2 is a hybrid Liquid model with multiplicative gates and short convolutions. It consists of 16 blocks: 10 double-gated short-range convolution blocks and 6 blocks of grouped query attention». También: «linear first-order systems converging to zero after a finite time».
- liquid.ai/company: «Spun out of MIT CSAIL, four founders — Ramin Hasani (CEO), Mathias Lechner (CTO), Alexander Amini (CSO), and Daniela Rus»; «Est. 2023».
- Wired (23-10-2024): «Hasani's research drew inspiration from the C. elegans». También mencionan modelos «for controlling self-driving cars».
- Lechner et al., «Neural circuit policies enabling auditable autonomy», Nature Machine Intelligence (2020), ya en nuestra lista verificada de la 2026-10-13-013.
- Nuestro, del CONTEXTO: «R1_CON_TASA y R1_CON_LIQ la IGUALAN en 6/6».

## Archivos

- Esta respuesta. El CONTEXTO no cambia de estado.

## NO MEDIDO

- Cómo rinde un LFM2 en nuestras tareas, o como planificador encima de una pieza de mosca.
- Si sus modelos para manejar autos usan redes líquidas de verdad o la arquitectura de LFM2: Wired los menciona sin detalle.
- El rendimiento de LFM2 fuera de lo que publica la empresa: no se verificó de forma independiente.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| LFM2 no lleva cableado de gusano | su informe técnico y su blog (convoluciones con compuertas y atención) | sí: si el informe describiera un circuito biológico |
| la inteligencia sale del entrenamiento | «Pre-trained on 10-12T tokens», más destilación y ajuste fino | es literatura de la empresa |
| en nuestro banco lo líquido no agregó | factorial 2: líquida y tasa igualan a la regla en 6/6 | ya pudo dar rojo y no lo dio |

```
--- METODO PROMETEO ---
Accion delicada: no (síntesis con referencias)
Maquina: web (2 búsquedas)
Artefactos: docs/agents/respuestas/2026-10-13-019-liquid-ai-es-un-llm-entrenado-no-un-gusano-copiado.md + Doc de ClickUp 2026-10-13-019
```
