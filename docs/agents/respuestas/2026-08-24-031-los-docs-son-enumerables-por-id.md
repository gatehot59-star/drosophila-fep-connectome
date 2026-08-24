# 031 · **SÍ hay forma**: los Docs son enumerables por ID, sin cosechar del chat

**Fecha:** 2026-08-24 ~12:05 (America/Buenos_Aires)

## 1. Pedido

> "¿no tendrás forma de llegar a todos los enlaces de documentos y no tener que estar haciendo este trabajo? Si descubrís dónde están todos, podrías leer uno por uno y entender el guiso que tenés"

Más: ir al momento en que pasó el paper publicado por primera vez (una sola vez), y distinguir que **DualBrain venía de antes del paper** y que **SparseLTC, aunque es parte del producto, se usa en todos los experimentos del conectoma**.

## 2. Herramientas declaradas (C-03)

`load_assets` con **IDs construidos por mí**, no provistos por el usuario (5 IDs probados) · `search_tools` para verificar si existía un enumerador de Docs · `githubmcp_get_file_contents` (índice actual) · `create_document`. **Cero cuota de Kaggle, ninguna corrida.**

## 3. EL HALLAZGO

**Los IDs de página de Docs son secuenciales con paso 20 bajo el prefijo `2kza6fw5-`, y `load_assets` los acepta directo.** No hace falta que el usuario pegue enlaces.

Evidencia: construí 5 IDs que **nunca fueron provistos** y 4 abrieron con título y contenido:

```
doc:2kza6fw5-3537  -> "[TITAN] MUDH - Hot-Update de Agentes via proot"            16-ago
doc:2kza6fw5-3577  -> "[TITAN] Paquete Plano para OpenCode - OPERIT"              16-ago
doc:2kza6fw5-3597  -> "[TITAN] PAQUETE MAESTRO Unico para OpenCode"               16-ago
doc:2kza6fw5-3617  -> "[TITAN] MUDH-Mobile - Auditoria + D1-D7 para Tachi"        16-ago
doc:2kza6fw5-5177  -> "Tabla 5 - no se puede recalcular, y encontre algo mejor"   21-ago
doc:2kza6fw5-3557  -> (omitido de la respuesta: NO DISTINGUÍ si no existe o si
                       quedó afuera por limite de tamaño)
```

**No existe herramienta de enumeración de Docs en el catálogo** (lo verifiqué). El enumerador es el propio espacio de IDs.

## 4. EL RECLAMO, CONFIRMADO Y PEOR

**`doc:2kza6fw5-5177` NO está en `INDICE-DE-ENLACES.md`.** Es del 21-ago, de la línea del conectoma, **100/100**, y adentro **retiro tres afirmaciones mías** sobre la Tabla 5 del paper publicado:

- "si la densidad cambia 9,42×, cada ratio de la Tabla 5 cambia 9,42×" → **NO VERIFICADO**
- "4 de 9 clases pasan a ENRIQUECIDAS" → **RETIRADO**
- "el hallazgo central se invierte" → **ABIERTO**

con el hallazgo de fondo: **la expectativa de la Tabla 5 no es de densidad** (densidades implicadas 0,016719 y 0,014132, distintas entre sí y distintas de 0,0074; y el cociente `Exp_m/Exp_g ∈ [6,68 , 8,82]` contra `N_m/N_g = 6,52`, incompatible con proporcionalidad a N).

**El índice no tenía 30 de 30: tenía 30 de los que aparecían en los fragmentos pegados.** Construí el índice **desde el chat en vez de desde el workspace**, y un índice armado de citas solo puede contener lo que se citó. Séptimo patrón del Bloque 8, pero el defecto estaba en el **método de construcción**, no en el esfuerzo.

## 5. EL GUISO, con coordenadas

**Tres proyectos distintos conviven en el mismo espacio de IDs, sin separador:**

| Rango | Fecha | Proyecto |
|---|---|---|
| ~1057-1097 | 14-ago | MUDH v1.0, AURA OS (reportes de TITÁN Tao) |
| ~3537-3617 | 16-ago | MUDH-Mobile, OPERIT clean-room, Tachi |
| **~5177-6357** | **21 al 24-ago** | **Conectoma, papers, erratum, motores, DualBrain** |

**Eso ubica la línea del conectoma en el 21-ago**, que es cuando llegó el paper publicado. Los IDs anteriores no son del conectoma.

Y confirma las dos distinciones que el usuario tuvo que explicarme:
- **DualBrain es anterior al paper**: notebooks de marzo, línea neuromórfica de febrero (ya estaba en el índice cronológico y yo lo trataba como una línea sola).
- **SparseLTC es parte del producto Y el instrumento de los experimentos del conectoma.** No son roles excluyentes, y yo los venía como uno.

## 6. Qué cambia el método

| Antes | Ahora |
|---|---|
| El usuario pega fragmentos, yo cosecho enlaces | **Recorro el espacio de IDs y leo directo** |
| El índice tiene lo que el chat citó | El índice puede tener **lo que existe** |
| 18 de 30 leídos solo por título | Se pueden leer todos con contenido |

**Costo real, declarado:** cada Doc viene con contenido completo (algunos 30 KB). **Recorrer ~150 IDs en una pasada no entra en una ventana.** La forma correcta: **barrer por lotes y commitear el índice a medida que avanza**, para que un corte no lo tire. Prometer el barrido completo en una respuesta sería el mismo error de siempre.

## 7. NO MEDIDO, declarado

- **No barrí el espacio completo.** 5 IDs probados, 4 confirmados. **No sé cuántos Docs hay** ni los límites del rango.
- **El paso 20 está confirmado en dos zonas, no en todo el espacio.** Puede haber huecos o cambios de paso.
- **`3557` no devolvió nada y NO distinguí** «no existe» de «omitido por tamaño». Los tres estados.
- **No verifiqué si `2kza6fw5-` cubre todos los Docs** o si hay otro espacio de nombres.
- **No leí el 5177 en profundidad**, solo lo necesario para saber qué es y que faltaba en el índice.
- **No encontré el Doc del primer análisis del paper publicado.** Ubico la línea en el 21-ago **por la fecha del 5177**, no por haber hallado ese Doc. Está entre 3617 y 5177 y **no lo acoté más**.

## 8. O-01 · Propuesta, con criterio

**Criterio: que el usuario deje de tener que pegar fragmentos.**

1. **Barrido por lotes del espacio de IDs**, commiteando en git un índice real (título, fecha, proyecto, veredicto) a medida que avanza. Reemplaza el trabajo manual del usuario de forma permanente.
2. **Separar los tres proyectos en el índice.** Hoy están en el mismo cajón y eso es la causa mecánica del guiso.
3. **Recién después**, lectura en profundidad de la línea del conectoma en orden cronológico desde el paper publicado.

Se preguntó antes de ejecutar porque el barrido consume varias pasadas de contexto y el usuario puede querer acotarlo a la línea del conectoma.

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-4457

```
--- METODO TITAN ---
Accion delicada: NO. Lectura de 5 Docs por ID construido, un Doc nuevo, un
                 commit. Ninguna corrida, cero cuota ajena.
Modo aplicado:   TITAN FULL
Rubrica:         no se emite todavia: esto es el hallazgo del metodo, no el
                 barrido. La rubrica va con el indice completo.
N/A declarados:  pendiente
Review externo:  el falsador fue Abraham, sexta vez en el dia. Y esta vez no
                 corrigio un dato: corrigio el METODO con el que armaba el
                 indice. Ningun instrumento mio iba a encontrarlo, porque el
                 sesgo estaba en de donde saque la lista (W-01: el hueco del
                 sesgo de seleccion).
                 B-01: el unico falsador consistente sigue siendo el usuario.
                 Mecanismo propuesto para reemplazarlo: el indice debe
                 construirse por ENUMERACION del workspace, no por cosecha del
                 chat. Una lista derivada de citas no puede detectar lo que
                 nadie cito; una derivada del espacio de IDs si.
Instrumento:     load_assets con IDs construidos por mi.
                 4 de 5 IDs nuevos abrieron con titulo y contenido.
                 Evidencia verbatim en la seccion 3.
                 NO MEDIDO: seccion 7.
```
