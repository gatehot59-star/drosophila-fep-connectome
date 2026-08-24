# 032 · Handoff para el chat nuevo

**Fecha:** 2026-08-24 12:05 (America/Buenos_Aires)

## 1. Pedido

"Start a new conversation and summarize the issue: mi chat anterior excedió el tamaño, acá va un resumen del problema, ¿me ayudás a seguir desde acá?"

## 2. Herramientas declaradas (C-03)

`create_document` y este commit. **Ninguna corrida, ninguna lectura nueva, cero cuota de Kaggle.** El handoff se arma con lo ya medido y commiteado en esta sesión.

## 3. Decisión de diseño, y es la que importa

**Los handoffs anteriores fallaron por la misma razón que fallaba el índice de enlaces: intentaban meter el estado ENTERO en el mensaje.** El `5677` (HANDOFF del 22-ago) es un muro de texto con bugs, números y tablas, y se cae por tamaño igual que el chat que pretende reemplazar.

**Este es corto a propósito y arranca con una orden de lectura:** los tres archivos de git que contienen el estado vivo. El handoff no ES el estado: es el **puntero** al estado.

Eso solo se puede hacer ahora porque en esta sesión aparecieron las dos piezas que faltaban:

1. **`INDICE-REAL-POR-ENUMERACION.md`** (resp 031 + pasadas 1-3): el mapa de 41 Docs con qué establece cada uno.
2. **El método de enumeración**: IDs secuenciales paso 20 bajo `2kza6fw5-`. El chat nuevo **no necesita que Abraham le pegue enlaces**, y el handoff se lo dice explícitamente.

## 4. Qué lleva el bloque

- **Orden de lectura de git antes de responder** (3 archivos).
- **El método de enumeración**, con la instrucción de no pedir reenvíos.
- **Las cinco líneas de trabajo separadas**, con la aclaración de que DualBrain es anterior al paper y que SparseLTC cumple dos roles. Mezclarlas fue el error más caro de la sesión.
- **Las 5 deudas abiertas** en orden de bloqueo: corchetes del erratum · README público con la clasificación equivocada · reciprocidad y KC→MBON sin probar contra CP · 21 nulls faltantes · los bugs del Script R dentro del verificador.
- **Las 6 cosas cerradas**, para que el chat nuevo no las reabra.
- **El modo de trabajo** (TITAN FULL, C-03, Doc para outputs largos, commit obligatorio).
- **La advertencia B-01 sobre el falsador humano**, con el mecanismo propuesto para reemplazarlo.

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-4477

## 5. NO MEDIDO / lo que el handoff NO cubre

- **14 IDs sin identificar** de la zona del conectoma (`6017` a `6337`).
- **~50 IDs sin barrer** entre `3637` y `4717`.
- **La línea MUDH/AURA del 14-ago** sin tocar.
- **7 de 17 `.py` siguen fuera de git.**
- **No verifiqué que el bloque quepa** en un primer mensaje sin que el entorno lo trunque. Es más corto que el `5677`, pero **no lo medí**.
- **No sé si el chat nuevo va a leer git antes de responder.** El handoff lo ordena en la primera línea y en negrita; **cumplirlo no se puede forzar desde acá.** El control es de salida: si la primera respuesta no nombra los archivos leídos, se incumplió.

```
--- METODO TITAN ---
Accion delicada: NO. Un Doc y un commit. Ninguna corrida, cero cuota ajena.
Modo aplicado:   TITAN LIGERO (redaccion de un handoff sobre estado ya medido
                 y ya auditado con rubrica en las respuestas 019 a 031)
Rubrica:         N/A (modo ligero)
N/A declarados:  N/A (modo ligero)
Review externo:  no aplica. El falsador de este handoff es el proximo chat: si
                 la primera respuesta no nombra los tres archivos de git, el
                 handoff fallo y hay que acortarlo mas.
Instrumento:     ninguno nuevo. Cero mediciones nuevas: el bloque cita las
                 respuestas 019-031 y el INDICE-REAL-POR-ENUMERACION.md.
                 NO MEDIDO: seccion 5, incluido que el bloque quepa.
```
