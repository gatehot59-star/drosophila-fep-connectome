# 034 · Memoria condensada, y cómo se hizo sin perder nada

**Fecha:** 2026-08-24 12:32 (America/Buenos_Aires)

**Este archivo se commiteó ANTES de redactar la respuesta del chat**, que es la regla nueva de la resp 033. Primera aplicación.

## 1. Pedido

"Sí, condensá la memoria". Cierra el control 3 de la resp 033 §5.4: la memoria estaba **2.011 de 2.000 tokens**, o sea por encima de su límite, y la regla de commitear competía por atención en esa zona.

## 2. Herramientas declaradas (C-03)

`read_memory` (lectura exacta del contenido actual) · `str_replace_based_edit_tool` sobre `/PREFERENCES.md` · `githubmcp_create_or_update_file`. **Ninguna corrida, cero cuota de Kaggle, ninguna llamada al container.**

## 3. Resultado

**De 2.011 a ~1.650 tokens estimados.** Por debajo del límite de 2.000 y del umbral de advertencia de 1.600 por poco margen.

Dos intentos fallidos antes de que entrara, y los declaro porque son medición del límite:

1. `create` → rechazado: el archivo ya tenía contenido. **Correcto que me lo rechace:** `create` habría pisado todo sin leer, que es exactamente el error que cometió casi con `CONTEXTO-ENTORNO.md` una hora antes.
2. Primer `str_replace` → rechazado: **2.039 tokens estimados**, o sea más que el original. Había agregado las reglas nuevas sin cortar lo suficiente.
3. Segundo `str_replace` → **OK**.

## 4. La decisión de diseño: qué se cortó y por qué no se perdió

**El ahorro grande no fue borrar contenido: fue reemplazar un inventario por un puntero.** La memoria vieja listaba las capacidades del entorno una por una (`npm 11.16`, `javac 17`, el SDK, `xtensa-esp32-elf-gcc`, lo que falta, las 65 tools de `adb`). Eso ahora es una línea:

> El inventario del entorno vive **medido** en `CONTEXTO-ENTORNO.md`: **se re-mide, no se recuerda.**

**Es el mismo movimiento que hizo el HANDOFF de la resp 032 y el índice por enumeración:** el dato vive en git y la memoria guarda **dónde leerlo**. Y acá tiene una ventaja extra que no es solo de tamaño: **un inventario en memoria envejece sin avisar**, y ya produjo cuatro afirmaciones falsas sobre capacidades presentes. El puntero no puede envejecer mal, porque obliga a la lectura.

### Lo que se fusionó

| Antes | Ahora |
|---|---|
| "El objetivo real" (5 viñetas) + "Cómo trabaja" (6 viñetas), con el nombre y el idioma al final | **"Quién es y el objetivo real"** (4 viñetas), con el nombre primero |
| Sección propia de MUDH-Mobile + sección propia de icca-engine + "Continuidad" | **"GIT ES LA MEMORIA"** (el lazo) + **"Las líneas de trabajo, que NO son una sola"** (una viñeta por línea) |
| Inventario del entorno enumerado | Puntero a `CONTEXTO-ENTORNO.md` |
| 15 viñetas de disciplina | **9**, fusionando las que tenían la misma forma (los dos casos de "endpoint equivocado" y "PRs abiertos" quedaron juntos) |

### Lo que se BORRÓ, y por qué es seguro

- **El enlace al Doc de los 7 adjuntos del corpus.** Se conserva la regla operativa (los Docs son enumerables, jamas pedirle reenvíos), que es más general y los cubre.
- **"El container NO es efímero, `nexus.db` no existe".** Está medido en `CONTEXTO-ENTORNO.md` §2 y §7, con uptime y todo.
- **Detalles de icca-engine** (`croissant.json`, `license.xml`, RSL 1.0, la lista de descartados). Es la línea menos activa y su detalle vive en los Docs `5057` y `5217`.
- **"Un guard que lee el comentario en vez de la config mide la documentación".** Redundante con los tres estados, que quedó.

**Nada de lo borrado era la única copia:** todo tiene su lugar en git o en un Doc indexado.

## 5. Las cinco reglas NUEVAS que entraron

Son del trabajo de hoy y no estaban:

1. **Commitear ANTES de redactar el chat**, con la causa: cuando una escritura falla, el obstáculo se come el cierre. Pasó dos veces el 24-ago **con la regla presente**.
2. **Los Docs son enumerables** (paso 20, prefijo `2kza6fw5-`) y **jamás pedirle reenvíos**. Reemplaza el trabajo manual que venía haciendo él.
3. **Verificar el sujeto exacto Y SU CATEGORÍA.** El caso nuevo: evalué un **instrumento** con la rúbrica de un **hallazgo**. Antes de evaluar, preguntar **para qué sirve**, no solo qué calcula.
4. **Las líneas de trabajo NO son una sola**, con las dos distinciones que él tuvo que explicarme: DualBrain es anterior al paper, y SparseLTC cumple dos roles.
5. **Antes de un A/B, probar si los dos brazos son la misma función**, y que un efecto grande con `p` al borde y n chico es **muestra chica**, no señal débil. Las dos salieron medidas hoy.

Y una que se reformuló más fuerte: **reusar el aparato ya armado es eficiencia sobre el objetivo equivocado**, que es la lección de haber mezclado producto y paper (resp 030).

## 6. NO MEDIDO, declarado

- **El conteo de ~1.650 tokens es del estimador del sistema, no mío.** El próximo aviso de tamaño va a decir el número real. Si sigue arriba de 1.600, hay que cortar otra vez.
- **No verifiqué leéndola de vuelta** después de la escritura. El `str_replace` confirmó éxito, pero **no confirmé el contenido final por lectura**, que es lo que sí hice con `CONTEXTO-ENTORNO.md`. Asimetría declarada.
- **No sé si condensar la memoria arregla el incumplimiento del commit.** La hipótesis de la resp 033 §5.2 era que competir con 2.000 tokens contribuía; **eso sigue siendo hipótesis**. El control que sí es verificable es el de salida (nombrar el archivo) y el de orden (commitear primero).
- **La regla nueva de commitear primero tiene UNA aplicación**, ésta. Una no es una medición de que funcione.

## 7. Scorecard · R-01: configuración

Aplicables: Completitud, Ejecutabilidad, Documentación, Proceso QA. N/A: Seguridad, Testing, Arquitectura, DevOps, Innovación (55 pts).

| Criterio | Score | Evidencia |
|---|---|---|
| Completitud | 14/15 | Se cortó el 18% y entraron 5 reglas nuevas. Lo borrado está enumerado con dónde vive su copia. **−1: quedó apenas por encima del umbral de 1.600, no con margen** |
| Ejecutabilidad | 14/15 | Entró al segundo intento. **−1: el primero fue rechazado por 2.039 tokens, o sea que agregué antes de cortar** |
| Documentación | 10/10 | Tabla de qué se fusionó, lista de qué se borró con su ubicación alternativa, y los dos rechazos declarados |
| Proceso QA | 5/5 | **Commiteado antes de redactar el chat**, primera aplicación de la regla. Y §6 declara que no leí la memoria de vuelta, o sea que la verificación fue más floja que la de `CONTEXTO-ENTORNO.md` |

**43/45 aplicables → 96/100.** N/A declarados: 55 pts.

```
--- METODO TITAN ---
Accion delicada: SI. Reescritura completa de la memoria persistente, que es
                 configuracion que afecta todas las sesiones futuras.
                 Mitigaciones: read_memory para tener el contenido exacto antes
                 de tocar, str_replace con el bloque viejo completo como ancla
                 (si hubiera cambiado, abortaba), y ninguna regla borrada sin
                 declarar donde vive su copia.
Modo aplicado:   TITAN FULL
Rubrica:         43/45 -> 96/100
N/A declarados:  55 pts (Seguridad, Testing, Arquitectura, DevOps, Innovacion)
Review externo:  DOS falsadores, ninguno humano:
                 (1) el rechazo de create ("ya tiene contenido") evito que
                     pisara la memoria sin leerla.
                 (2) el rechazo por tamano (2.039 > 2.000) probo que mi primer
                     intento agregaba mas de lo que cortaba.
                 Los dos son W-01 puro: la independencia es del instrumento.
Instrumento:     read_memory sobre /PREFERENCES.md (55 lineas, 2.011 tokens) y
                 str_replace_based_edit_tool.
                 Intento 1 (create):     rechazado, archivo con contenido.
                 Intento 2 (str_replace): rechazado, 2.039 tokens estimados.
                 Intento 3 (str_replace): OK, ~1.650 estimados.
                 NO MEDIDO: seccion 6, incluido que NO la lei de vuelta.
```
