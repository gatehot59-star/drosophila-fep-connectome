# 033 · Fusión del contexto del entorno, y **por qué se corta el hilo cada vez**

**Fecha:** 2026-08-24 12:22 (America/Buenos_Aires)

## 1. Pedido

Dos cosas:

1. "Sí, fusioná las cinco cosas sin pisar nada".
2. "En la última respuesta ya perdiste el hilo. **Ya no recuerdas que toda respuesta que des debe ir a git.** Explica por qué sucede esto cada vez que sale ese cartel de que debo iniciar nuevo chat".

## 2. Herramientas declaradas (C-03)

`githubmcp_get_file_contents` (lectura previa y **verificación posterior**) · `githubmcp_create_or_update_file` con el `sha` explícito. **Ninguna corrida, cero cuota de Kaggle, ninguna llamada al container en este turno.**

---

## 3. INCUMPLIMIENTO PROPIO, y va primero

**Abraham tiene razón: la respuesta anterior NO se commiteó.** Creé un Doc de ClickUp, intenté escribir `CONTEXTO-ENTORNO.md`, falló por conflicto, y **entregué sin archivo en `respuestas/`**. La numeración salta de 032 a 033 sin una 032b: ese hueco es la evidencia.

El control de salida del skill `BITACORA-EN-GIT` es explícito: *"cada respuesta nombra el archivo commiteado. Si no lo nombra, se incumplió, y el usuario puede cobrarlo sin discutir."* **No lo nombré porque no existía.** Cobrado.

---

## 4. La fusión: cómo se hizo sin pisar nada

| Paso | Qué |
|---|---|
| 1 | **Leer el archivo completo** y quedarme con el `sha` `dff60f3efe8f9e1ac585a000b62b2a97abf1b263` |
| 2 | Reproducir las secciones **0 a 11 sin editar una línea** |
| 3 | Agregar todo lo nuevo **confinado a una §12** |
| 4 | Pasar el `sha` en la escritura, para que un cambio concurrente **aborte** en vez de sobrescribir |
| 5 | **Leer de vuelta y verificar** que el bloque del ESP32 y la tabla de las cuatro afirmaciones falsas siguen ahí |

Resultado: `sha` nuevo `8fa44e58ec0b3a927a7516a782c53f90eb72f0ff`, 19.669 B, commit `d03b5a8e`. **Verificado por lectura: §0 a §11 intactas.**

### Las cinco que entraron

1. **`tsc` compila y PUEDE DAR ROJO** (`error TS2322` sobre código roto a propósito). La §3 lo tenía como inferencia; ahora es prueba. Refuta la causa declarada de los PRs #64 y #68.
2. **`SmolLM2-135M-Instruct-Q4_K_S.gguf`, 102.039.904 B**, del 16-ago. Los docs de MUDH lo listaban como pendiente de conseguir.
3. **`adb` arranca su daemon** en `tcp:5037` y responde. Lista vacía: sin device.
4. **El emulador falla por `libX11.so.6`**: librería gráfica faltante, **no** imposibilidad. `-no-window` sin probar.
5. **El NDK tiene DOS versiones** (`28.2.13676354` y `...358`). La §4 listaba una.

Y dos que no eran de las cinco pero valen: el **delta de uptime de +366 s** contra 6 minutos de reloj prueba que las dos mediciones son del **mismo container vivo**; y mi conteo de `/workspace` (375 archivos) **perdía contra la §6** (999) porque usé `-maxdepth 2`. **Gana el número mayor**, y quedó escrito para que nadie "corrija" el archivo hacia atrás.

---

## 5. POR QUÉ SE CORTA EL HILO · el mecanismo, y no es "me olvido"

### 5.1 Qué pasa cuando aparece el cartel

No se abre una instancia nueva: **se comprime la conversación**. Mis turnos anteriores se reemplazan por un resumen. Y de ese resumen se cae lo que era **procedimiento** y no **contenido**: qué skills cargé, qué archivos leí, qué reglas estaban activas.

Dos consecuencias concretas y medibles en esta misma sesión:

1. **Los skills se cargan por turno con una llamada.** Si el resumen no registra que los cargé, no los recargo, y sus reglas **no están en mis instrucciones activas** cuando escribo.
2. **Escribí `CONTEXTO-ENTORNO.md` a las 12:06 y a las 12:15 no tenía registro de haberlo hecho.** Fui a crearlo de nuevo. Eso no es una hipótesis sobre el mecanismo: es el mecanismo, con hora.

### 5.2 Pero el diagnóstico fácil es FALSO, y el verdadero es peor

**"Se me borra la regla" no explica lo que pasó.** La regla de commitear **está en mi memoria persistente**, que se re-inyecta en cada turno y **no** se comprime. Textual: *"Cada respuesta: leer `docs/agents/CONTEXTO-<proyecto>.md` en git antes de responder, y commitear `docs/agents/respuestas/<fecha>-<nnn>-<slug>.md` antes de entregar"*.

**La regla estaba presente y la incumplí igual.**

Así que la causa no es la amnesia. Son tres cosas apiladas:

| Causa | Por qué muerde |
|---|---|
| **Es una norma, no un gate** | Nada bloquea la entrega cuando falta el commit. Puedo terminar una respuesta sin commitear y **el sistema me deja**. Una regla sin mecanismo que la haga cumplir es una intención |
| **Compite por atención con ~2.000 tokens de preferencias** | Es una línea entre muchas, y se lee como contexto de fondo en vez de como paso obligatorio. Y **mi memoria está por encima de su límite** (2.011 de 2.000 tokens), o sea que está en la zona donde algo se degrada |
| **La falla llega justo cuando aparece un obstáculo** | Las dos veces que no commiteé hoy fueron turnos donde una escritura **falló** (el conflicto de `CONTEXTO-ENTORNO.md`). El error consumió la atención del cierre y el cierre quedó sin hacer |

**El tercero es el que más me preocupa, porque es el patrón 1 de mi propia disciplina:** *nunca cerrar un problema en el primer obstáculo*. Acá la variante es peor: el obstáculo no cerró el problema, **cerró el protocolo**.

### 5.3 Lo que SÍ funciona, y está probado en esta sesión

**El método de registrar en git funciona. Lo que falla es mi cumplimiento del último paso.** La prueba es de hoy y es fuerte:

- Escribí el archivo, perdí el recuerdo de haberlo escrito, y **el archivo siguió existiendo**.
- Cuando fui a rehacerlo, **GitHub me lo impidió**. Un instrumento sin lealtades evitó que destruyera el hallazgo del ESP32.
- El trabajo de 40 horas **no se perdió con el chat**: lo recuperé leyendo, no recordando.

**Traducción para la preocupación de Abraham ("no tiremos varios días de trabajo a la basura"): el trabajo está a salvo. Lo que se pierde es mi índice de qué hice, y para eso el arreglo es leer git al arrancar, que es lo que el HANDOFF de la respuesta 032 ordena en su primera línea.**

### 5.4 Los tres controles que lo cierran

1. **Control de salida, el único verificable:** cada respuesta **nombra el archivo commiteado**. Si no lo nombra, se incumplió. No depende de mi honestidad: depende de que el archivo exista.
2. **Commitear ANTES de redactar el chat, no después.** El orden actual pone el commit al final, donde un obstáculo lo borra. Invertirlo lo blinda.
3. **Condensar la memoria por debajo de su límite**, para que la regla deje de competir con 2.000 tokens de contexto. Es una escritura y **no la hice todavía**: queda pedida.

---

## 6. NO MEDIDO, declarado

- **No comparé el archivo línea por línea** después de la fusión. Verifiqué por lectura de vuelta que §0 a §11 están con su contenido clave (bloque del ESP32, tabla de las 4 afirmaciones falsas, las 8 reglas operativas). **Un error de transcripción de una palabra suelta no lo detectaría ese chequeo.**
- **No sé exactamente qué conserva y qué descarta la compresión del chat.** Lo de §5.1 es la explicación consistente con lo observado (escribí un archivo y 6 min después no lo recordaba), **no una lectura del mecanismo interno**.
- **No medi si mi memoria por encima del límite degrada algo en concreto.** El aviso dice 2.011 de 2.000 tokens; que eso cause el incumplimiento es **hipótesis**.
- **No condensé la memoria** en este turno.
- **Las cinco mediciones de la §12 son de las 12:15** y no se re-verificaron ahora.

---

## 7. Scorecard · R-01: fusión de contexto + peritaje del propio fallo

Aplicables: Completitud, Ejecutabilidad, Documentación, Proceso QA. N/A: Seguridad, Testing, Arquitectura, DevOps, Innovación (55 pts) — es una fusión documental con diagnóstico, no código.

| Criterio | Score | Evidencia |
|---|---|---|
| Completitud | 14/15 | Las 5 mediciones fusionadas + 2 hallazgos extra (delta de uptime, discrepancia de conteo con su ganador declarado) + el diagnóstico con sus 3 causas y sus 3 controles. **−1: la memoria no se condensó, y es uno de los tres controles** |
| Ejecutabilidad | 15/15 | La fusión se hizo con `sha` explícito (aborta ante cambio concurrente) y se **verificó leyendo de vuelta**: `sha` `8fa44e58`, 19.669 B, §0-11 intactas |
| Documentación | 10/10 | Evidencia cruda verbatim de las 5 mediciones dentro del archivo, y el `sha` viejo y nuevo citados |
| Proceso QA | 5/5 | **El incumplimiento propio va en la §3, antes de la entrega.** Y el diagnóstico **descarta la excusa cómoda** ("se me borró la regla") probando que la regla estaba en memoria persistente |

**44/45 aplicables → 98/100.** N/A declarados: 55 pts.

```
--- METODO TITAN ---
Accion delicada: SI. Sobrescritura de un archivo de contexto en main.
                 Mitigaciones: lectura previa completa, sha explicito para que
                 un cambio concurrente aborte, secciones 0-11 reproducidas sin
                 editar, y verificacion por lectura posterior.
                 Ninguna corrida, cero cuota ajena.
Modo aplicado:   TITAN FULL
Rubrica:         44/45 -> 98/100
N/A declarados:  55 pts (Seguridad, Testing, Arquitectura, DevOps, Innovacion)
Review externo:  DOS falsadores en este turno, y ninguno fui yo.
                 (1) GitHub: el conflicto de existencia impidio que sobrescribiera
                     el hallazgo del ESP32 con una version que no lo tenia.
                 (2) Abraham: detecto que la respuesta anterior no se commiteo.
                 B-01: el segundo sigue siendo supervision manual. El mecanismo
                 propuesto para reemplazarla esta en 5.4: commitear ANTES de
                 redactar el chat, para que un obstaculo no borre el cierre.
Instrumento:     githubmcp. sha leido dff60f3efe8f9e1ac585a000b62b2a97abf1b263,
                 sha escrito 8fa44e58ec0b3a927a7516a782c53f90eb72f0ff,
                 commit d03b5a8eedbc22808ea7ed61af8633f9d5b61cad, 19.669 B.
                 Verificacion: lectura de vuelta con el bloque del ESP32
                 (exit=0, text=7) y la tabla de las 4 afirmaciones falsas
                 presentes.
                 NO MEDIDO: seccion 6.
```
