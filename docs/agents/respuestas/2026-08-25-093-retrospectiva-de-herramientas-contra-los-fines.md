# 093 · Retrospectiva honesta: ¿elegiría las mismas herramientas, con los mismos fines?

**Fecha:** 2026-08-25 22:50 (America/Buenos_Aires) · **Modo:** TITAN FULL · **Tipo:** peritaje retrospectivo

**La pregunta exacta:** con los fines declarados (dinero, cedible a un aprendiz, innovación y materialización), ¿las herramientas elegidas fueron las correctas, y hay forma objetivamente mejor de resolver lo que ya está hecho?

**Regla que gobierna este documento (B-01):** cuando hay medición externa, gana la medición externa, incluso cuando contradice el trabajo propio. En este turno **el falsador fue la literatura**, y contradijo una decisión estructural.

<hr/>

## 1. 🔴 El hallazgo que duele, verificado en vivo

**Existe un pipeline revisado por pares que hace exactamente el aparato que se construyó a mano.**

```plain
VERIFICADO EN VIVO 2026-08-25
Parkes et al. 2024, Nature Protocols
DOI 10.1038/s41596-024-01023-w  ·  44 citas
"A network control theory pipeline for studying the dynamics of the
 structural connectome"
Autores: incluye Pasqualetti y Bassett (h-index 111)

Karrer et al. 2020, Journal of Neural Engineering
DOI 10.1088/1741-2552/ab6e8b
"A practical guide to methodological considerations in the
 controllability of structural brain networks"
Su abstract, verbatim: "we probe how a selection of modeling choices
 affects four common statistics"
```

**Karrer 2020 es un paper entero sobre cómo las decisiones de modelado afectan las métricas.** Ese es, literalmente, el problema que se peleó de cero durante meses: qué null usar, qué métrica, qué normalización, qué piso.

### Lo que esto NO significa

**No invalida el trabajo.** El conectoma de Drosophila a nivel sináptico no es un conectoma humano por DTI, y ningún pipeline publicado corre sobre 15.091.983 aristas con signo E/I por neurona. La ley de Dale exacta (0 mixtas de 138.005, medido hoy) **no existe en el caso humano**.

### Lo que sí significa, y es lo importante

**Cambia dónde está el activo.** Y esto ya venía apareciendo todo el día por otras vías:

<table><tbody><tr><th width="220" cell-bg-color="grey"><p><strong>lo que se creía el activo</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>quién ya lo tiene</strong></p></th></tr><tr><td width="220"><p>los números de propagación</p></td><td width="220"><p><strong>Betzel: el grafo es idéntico arista por arista</strong> (0 de 15.091.983)</p></td></tr><tr><td width="220"><p>la tabla de ruteo</p></td><td width="220"><p><strong>ya publicada</strong> en el Cell Type Explorer de FAFB</p></td></tr><tr><td width="220"><p>el método de propagación</p></td><td width="220"><p><strong>Parkes 2024</strong>, pipeline con 44 citas</p></td></tr><tr><td width="220"><p>el aparato de decisiones de modelado</p></td><td width="220"><p><strong>Karrer 2020</strong></p></td></tr></tbody></table>

> **Tres veces en el día apareció el mismo patrón: el número converge con el de otro autor que llegó por otra vía.** Eso, leído bien, **no es una derrota: es validación convergente**. Pero obliga a mover el claim de lugar.

<hr/>

## 2. El costo real de las tres vías de ejecución, medido hoy por primera vez

```plain
via                                unidad                    costo medido
container CPU (conectoma real)     1 null del 2x2            764,6 s
container CPU (sintetico)          39 nulls del 2x2           41,6 s
sandbox propio (barrido v1)        30 puntos              15.376,5 s
Kaggle GPU                         push de 4 kernels      HTTP 200 / status 403

factor real vs sintetico, POR NULL:                            ~700x
```

**Nadie había medido eso**, y explica por qué dos corridas de hoy se planificaron mal: el sintético terminaba en 41 segundos y el real necesita **8,07 horas** para los 38 nulls que faltan.

> **Herramienta que faltaba y no es un modelo: un medidor de costo por vía.** Con esa tabla, la decisión "container o Kaggle" se toma en diez segundos en vez de descubrirse a las tres horas.

<hr/>

## 3. 🔴 El patrón que se repitió TRES veces hoy, y es el mismo error

<table><tbody><tr><th width="220" cell-bg-color="grey"><p><strong>dónde</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>el error</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>medido</strong></p></th></tr><tr><td width="220"><p>DBC3, gráfico</p></td><td width="220"><p>una línea de azar única</p></td><td width="220"><p>8,3% para tareas con pisos de <strong>9,9% a 51,4%</strong></p></td></tr><tr><td width="220"><p><code>motor.py</code> v1</p></td><td width="220"><p>9 nulls</p></td><td width="220"><p>piso de <code>p</code> en <strong>0,20</strong>: no podía ganar</p></td></tr><tr><td width="220"><p>DBC3, script</p></td><td width="220"><p><code>ratio = d/max(l, 0.01)</code></p></td><td width="220"><p>denominador que puede morir, hasta <strong>10.000×</strong></p></td></tr></tbody></table>

**Los tres son la misma cosa: comparar contra el denominador equivocado.** Y es el mismo error que `cosine_distance` ya tenía documentado en `motor.py` (devolver 1,0 con vector nulo).

> **Esto es lo más transferible del expediente y no está escrito como regla:** *ningún efecto se reporta como cociente; se reporta como diferencia sobre el piso medido, y el piso se mide por caso.* Cinco líneas de regla que habrían evitado tres errores en un día.

<hr/>

## 4. Las seis decisiones de herramienta, juzgadas contra los fines

<table><tbody><tr><th width="220" cell-bg-color="grey"><p><strong>decisión</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>¿la repetiría?</strong></p></th><th width="220" cell-bg-color="grey"><p><strong>por qué</strong></p></th></tr><tr><td width="220"><p>numpy + scipy sparse en CPU</p></td><td width="220"><p><strong>SÍ</strong></p></td><td width="220"><p>medido: el SpMV es el 96,2% del tiempo y es memoria, no FLOPs. GPU da ~2× por ancho de banda, no 50×</p></td></tr><tr><td width="220"><p>Kaggle para lo pesado</p></td><td width="220"><p><strong>SÍ, con reparo</strong></p></td><td width="220"><p>es cómputo gratis real, pero la credencial <strong>empuja y no lee</strong> (403 <code>kernels.get</code>). Sin monitoreo, es lanzar a ciegas</p></td></tr><tr><td width="220"><p>C99 puro para el ESP32</p></td><td width="220"><p><strong>SÍ, sin duda</strong></p></td><td width="220"><p>800 B de RAM y 1.336 B de código verificados <strong>en target</strong>. Ningún framework llega ahí</p></td></tr><tr><td width="220"><p>PyTorch para el DBC3</p></td><td width="220"><p><strong>SÍ</strong></p></td><td width="220"><p>el presupuesto igualado (1,3% de dispersión) y el <code>assert</code> del conteo son buena ingeniería</p></td></tr><tr><td width="220"><p>construir el aparato de nulls de cero</p></td><td width="220"><p>🔴 <strong>NO</strong></p></td><td width="220"><p>Parkes 2024 existe con 44 citas. Partir de ahí y <strong>extenderlo</strong> daba el mismo resultado siendo citable desde el día uno</p></td></tr><tr><td width="220"><p>ser el único falsador</p></td><td width="220"><p>🔴 <strong>NO</strong></p></td><td width="220"><p>medido hoy: tres claims míos falsos y <strong>el que corrigió el encuadre fuiste vos</strong>, no un instrumento</p></td></tr></tbody></table>

<hr/>

## 5. 🔴 El problema estructural, y es el más caro de todos

**Hoy hice tres afirmaciones falsas y las tres las detectó una medición o vos, no un control automático:**

1. "`normalize_spectral` no normaliza" → **falso**, medido: 0,990000000 con error 4,35e-10
2. "`gelu_c` no es GELU" → **falso**, medido: 0,0188 contra GELU exacta
3. "el fix del candidato se lleva a `motor.py`" → **falso**, `motor.py` ya lo hacía

**Las tres se cerraron con una medición.** Ese es el sistema funcionando. Pero **quién eligió qué medir fuiste vos**, y eso es exactamente el hueco que W-01 dice que ningún instrumento propio cubre.

> **Con el fin de "cedible a un aprendiz", esto es el bloqueante real.** Un método que necesita que Abraham revise cada encuadre no es cedible: es Abraham.

<hr/>

## 6. 🟢 Y el A/B de la v4 cerró, con veredicto PARTIDO

```plain
VENTAJA SOBRE EL PISO MEDIDO, en puntos. Sin cocientes que puedan morir
  tarea                    v3           v4         LSTM | v4 vs v3 (pareado)
  XORMemory             +0.5       +16.4        -0.4 | +16.0 pts, t=0.97, n=3
  DelayedClass         +89.2       +78.5        -2.3 | -10.8 pts, t=-1.63, n=3

  la v4 gana en 1 de 2 tareas
```

**Y la lectura es limpia, justamente porque perdió una:**

- **XORMemory: +16,0 puntos.** La v3 estaba **en el piso** (+0,5) y la v4 la resuelve. El gate simétrico sirve donde hace falta **interacción**.
- **DelayedClass: −10,8 puntos.** Ahí hacía falta **ancho de memoria**, y la v4 pagó el gate nuevo bajando `h_m` de 20 a 13. **El costo se cobró donde se esperaba.**

> **Eso no es un fracaso del fix: es el fix funcionando y su precio apareciendo.** Y con `n=3` ningún `t` es concluyente, así que **no se declara significancia**.

<hr/>

## 7. Lo que haría distinto, en orden, con el criterio declarado

**Criterio: qué acerca los fines (dinero, cedible, innovación), no qué es más lindo de correr.**

1. **Escribir la regla del denominador y meterla en el skill.** Cinco líneas que habrían evitado tres errores hoy. Cuesta nada y es lo más transferible del expediente.
2. **Posicionar el activo donde de verdad está: el MÉTODO, no los números.** Los ocho guards de `motor.py` son ocho hipótesis muertas convertidas en código. **Eso** es lo que nadie más tiene y lo que se puede ceder.
3. **Anclar el paper a Parkes 2024 en vez de competir con él.** "Extendemos el pipeline de control de redes al caso sináptico con signo E/I exacto" es más fuerte y más citable que "construimos un método".
4. **Cerrar el `p` del conectoma real** con los 38 nulls que faltan. Sin eso, el mejor resultado del expediente no tiene su número.
5. **Meter un falsador que no seas vos.** Concretamente: los tests de `motor.py` corriendo en CI sobre cada commit. Hoy existe el arnés local y **no está en el CI**.

<hr/>

## 8. NO MEDIDO, declarado

1. **No se descargó ni se corrió el pipeline de Parkes 2024.** Su existencia y sus 44 citas están verificadas; **su aplicabilidad al caso sináptico es una conjetura mía**.
2. **No se verificó si existe un paquete instalable** de ese pipeline. Se leyó el paper, no el software.
3. **El A/B de la v4 corrió sobre 2 tareas de 5**, y ContextSwitch quedó afuera por costo. Declarado, no escondido.
4. **`n=3` semillas.** El `+16,0` tiene `t=0,97`: **efecto grande, muestra chica**. No es un resultado cerrado.
5. **Los 38 nulls del conectoma real siguen sin correr.** Van 2 de 39.
6. **La comparación de costos no incluye Kaggle GPU medido**, porque el `403` impidió leer el log. Es **no medido**, no cero.
7. **Buena parte de la sección 4 y toda la 7 son JUICIO, no medición.** Están marcadas como tales y son contradecibles.
