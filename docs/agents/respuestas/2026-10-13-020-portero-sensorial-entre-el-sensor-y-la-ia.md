# 2026-10-13-020 · Dónde entramos: de portero entre el sensor y la IA, no de voz de la IA

## Veredicto

- **[CONCLUSIÓN] La parte buena de la idea es el portero.** Una pieza chica entre el sensor y la IA grande:
  - mira o escucha todo el tiempo, gasta casi nada y reacciona en milisegundos;
  - decide cuándo despertar a la IA y qué mandarle;
  - dispara el reflejo de seguridad sin esperarla.
  - Ahí encajan la pieza de mosca (choques y movimiento) y DBC3 o SparseLTC (memoria corta y señales en el tiempo).
- **[CONCLUSIÓN] La voz de la IA, no.** Generar habla natural pide un modelo entrenado con muchas horas de grabación. La mosca no habla, y DBC3 no tiene nada de eso. Ahí no entramos, por ahora.
- **[CONCLUSIÓN] Audio y visión no son lo mismo para nosotros.**
  - En visión la mosca es una experta en choques y movimiento, y esos circuitos son justo los que tenemos medidos.
  - En audio la mosca oye cerca y poco: sobre todo el canto de cortejo. Para voz humana el portero sería DBC3 o SparseLTC entrenado, no una pieza de mosca.
- **[MEDIDO, nuestro] Lo que hay hoy es menos que eso.**
  - El banco usa entradas sintéticas ya sintonizadas por tipo de neurona, no píxeles ni micrófono.
  - DBC3 y SparseLTC empataron con una LSTM en las tareas del 12-oct.
  - Que el lector de DBC3 entre en un microcontrolador es la hipótesis HC-6, sin cerrar.
- **[CONCLUSIÓN] Prótesis:** el camino realista es la sustitución sensorial, por ejemplo cámara a vibración para una persona ciega. Es un módulo de procesamiento, no un reemplazo de la vista ni del oído, y como aparato médico está lejos.

## Pedido

21:51: «justamnete, nosotros, entramos con dual brain o dbc3 o partes de la mozca, en por ejemplo captar audio, o imagen, y llevarlos directos a ia. protesis, el habla de las ia, tambien puede ser genradas por nuestros sistemas»

## Herramientas y máquina

- Ninguna. Es una síntesis sobre el CONTEXTO y las respuestas 2026-10-13-015 a 2026-10-13-019. Sin cuota gastada.

## Qué se midió

Nada nuevo. Lo marcado [MEDIDO, nuestro] sale del CONTEXTO, de los Docs del 12-oct y de la memoria del proyecto (HC-6).

## Primera demo propuesta, con falsador

- **Aviso de choque.**
  - **Cadena:** cámara, después un puente que pasa de píxeles a los canales de la mosca (*looming* por lado), después la pieza de mosca (LC4 y LPLC2 hacia las descendentes) y al final una vibración izquierda o derecha.
  - **Se compara** contra un detector clásico de expansión (el tiempo al choque) y contra la regla a mano, en videos grabados con choques marcados.
  - **Se mide:** aviso anticipado, falsas alarmas por minuto, tamaño y consumo en el ESP32.
  - **Falsador:** si la pieza no le gana al detector clásico, o no lo empata siendo más chica, no entra a la fábrica.
- **Portero de audio**, la alternativa: DBC3 o SparseLTC chico detectando voz presente o una palabra clave, contra una LSTM o un detector clásico del mismo tamaño. **Falsador:** si no gana en tamaño, latencia o energía a igual acierto, no sirve.
- **Lo que falta para la de choque:** el puente de píxeles a canales. El banco hoy le da a la mosca la señal ya armada. La literatura tiene un modelo de la óptica de la mosca restringido por el conectoma (Lappalainen et al., Nature 2024). Si llega hasta LC4 y LPLC2 está NO MEDIDO.

## Archivos

- Esta respuesta. El CONTEXTO no cambia de estado: el factorial 4 sigue corriendo y sin leer.

## NO MEDIDO

- Cualquier cosa con cámara o micrófono reales: el banco nunca vio un píxel ni un sonido.
- El puente de píxeles a los canales de entrada de la mosca.
- Tamaño, latencia y consumo de una pieza en el ESP32.
- Que una pieza nuestra le gane a un detector clásico en un caso real.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| el banco no ve píxeles | el diseño del banco (sintonias de tarea_mosca) | sí: si el banco leyera imágenes |
| DBC3 empató con LSTM | Docs del 12-oct | ya pudo dar rojo y no lo dio |
| la voz no es para nosotros | opinión | no es medición |

```
--- METODO PROMETEO ---
Accion delicada: no (propuesta; nada corrido)
Maquina: ninguna
Artefactos: docs/agents/respuestas/2026-10-13-020-portero-sensorial-entre-el-sensor-y-la-ia.md + Doc de ClickUp 2026-10-13-020
```
