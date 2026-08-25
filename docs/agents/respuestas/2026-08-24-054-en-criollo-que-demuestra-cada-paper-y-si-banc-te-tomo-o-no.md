# 054 · En criollo, qué demuestra cada paper y si BANC te tomó o no

**Fecha:** 2026-08-24 22:14 (America/Buenos_Aires)

## 1. Pedido

«En criollo cada paper qué demuestra y cómo se vinculan entre los tres. Dijiste que este último de junio aplica lo que yo apliqué, pero por casualidad, por ser el único camino o porque tomó mi paper pero no me cita».

## 2. Respuesta corta, fijada

### Lin 2024
Lin **no simula señales**. Hace la radiografía de la red: muestra que el cerebro de la mosca es un grafo muy estructurado, con rich club, small-worldness, caminos cortos y una reciprocidad global que **no es rara entre cerebros**. En criollo: te dice **cómo está armado el cableado** y sugiere que desde ahí se construyan modelos de actividad.

### Tu Paper 1
Tu paper agarra ese cableado y pregunta **qué pasa si una señal entra y se propaga**. Ahí aparecen tres cosas: que algunas vías sensoriales quedan aisladas del centro de aprendizaje, que no todas las modalidades llegan igual al cuello de botella motor, y que el **tiempo** y el **signo excitatorio/inhibitorio** cambian el resultado. En criollo: pasás de la foto del cableado a una **película causal simplificada**.

### BANC 2026
BANC hace algo muy parecido a tu baseline lineal: mete señal en un origen, la deja propagarse por la red, normaliza por la entrada total de cada neurona y mira la influencia multi-salto. Pero le saca dos cosas clave: **el signo** y **el transitorio**. En criollo: hace la versión grande, sobria y Nature-friendly de la misma familia de método, pero se frena antes de donde empieza tu parte más propia.

## 3. Cómo se encadenan de verdad

**Lin prepara el terreno.** Dice: este conectoma tiene estructura no trivial y vale la pena modelar actividad sobre él.

**Tu paper da el primer paso dinámico.** Dice: si propagás señal, aparecen rutas privilegiadas, blindajes y diferencias temporales.

**BANC institucionaliza el paso lineal.** Dice: sí, esta familia de propagación sirve de verdad para mapear influencia a escala cerebro-completa, pero la deja en steady-state y sin signo.

O sea: **no son opuestos**. Son una secuencia bastante clara: **estructura -> propagación lineal -> influencia global consolidada**.

## 4. Entonces: ¿casualidad, único camino, o te tomó?

**Mi veredicto: no te tomó.** La cronología le pega en contra a esa sospecha.

- Tu preprint: **20-mar-2026**.
- Preprint de BANC: **31-jul-2025**.
- Nature de BANC: **8-jun-2026**.

Eso mata la hipótesis de que vieron tu paper de marzo, copiaron el método y salieron en junio. **Temporalmente no cierra.**

### Lo más probable entonces

**No fue casualidad pura tampoco.** Cuando querés medir influencia en un conectoma gigante, con datos incompletos, sin electrofisiología de todo el cerebro y con necesidad de escalar, la ruta lineal normalizada aparece sola como primer instrumento serio. Es el camino natural si querés algo:

- computable,
- interpretable,
- estable,
- y defendible frente a revisores.

Mi lectura es: **convergencia metodológica**. No porque sea el único camino en sentido absoluto, sino porque es el **primer camino razonable** que no se rompe enseguida.

## 5. Lo que te conviene decir, no lo que hiere el ego

La jugada buena no es decir «Nature me copió». Eso hoy queda flojo.

La jugada buena es esta: **«un paper posterior de Nature valida la familia de método lineal de propagación, pero trabaja en régimen estacionario y sin signo; nuestro aporte queda en la dinámica transitoria, la cancelación inhibitoria y la especificidad por circuito».**

Eso te sube, no te baja. Porque te corre del lugar de «preprint aislado que inventó algo raro» al de **alguien que tocó una dirección que después el campo grande también usó**.

## 6. El punto fino, en una línea

**BANC no demuestra que estabas equivocado. Demuestra que ibas por una familia de método real, pero también te obliga a dejar de vender como novedad lo que ya quedó absorbido por el campo.**

## 7. NO MEDIDO, declarado

1. No implementé lado a lado tu modelo lineal y la métrica exacta de BANC para medir equivalencia numérica.
2. No revisé si BANC cita algún preprint menor o discusión informal donde pudiera aparecer una ruta parecida.
3. No leí suplementos completos de BANC para ver si tocan algo parecido a reciprocidad por circuito.
4. El veredicto «convergencia metodológica» sale de cronología + descripción del método, no de prueba documental de independencia.
