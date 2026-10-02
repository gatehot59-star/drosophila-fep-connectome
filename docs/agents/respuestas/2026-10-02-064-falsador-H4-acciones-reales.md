# Falsador H4 sobre acciones reales anotadas

## Pedido

Correr el falsador H4: comprobar si rutas activas y módulos silenciados cambian según acción, usando el conectoma real y anotaciones reales.

## Instrumento

Runner `tools/h4_actions.py`, ejecutado en `brain-env` sobre el parquet FlyWire v783 y `annotations.tsv` pinneado. Grafo dirigido CSR, pesos `Excitatory x Connectivity`, dinámica real LTC discreta con `tau=0.119`, 120 pasos, estímulo de t=20 a t=79. Cada fuente se normalizó por `1/sqrt(n_source)`.

Poblaciones fijadas antes de leer resultados:

- `escape`: `cell_type`/`hemibrain_type` exacto LC4, LPLC2 o LC6.
- `grooming`: anotación `grooming` en subclase, tipo celular o hemibrain type.
- `feeding`: anotación `taste peg` o `GRN` en subclase/tipo.

Módulos de salida fijados antes de medir: GF, descending, motor, MBON y KC.

Datos: N=138.639, E=15.091.983, parquet md5 `3d802fd542b5d18570ba1ba0bb0abed9`, annotations md5 `719904abad876c68ace1b5690c9b9b63`.

## Resultado bruto

Tamaños de fuentes: escape=439, grooming=187, feeding=146.

Perfiles de energía post-estímulo, orden `[GF, descending, motor, MBON, KC]`:

```text
escape   [0.2065, 0.1803, 0.2008, 0.2059, 0.2065]
grooming [0.2080, 0.1817, 0.1938, 0.2086, 0.2079]
feeding  [0.2006, 0.1803, 0.1983, 0.2102, 0.2105]
```

Distancias entre perfiles:

```text
escape vs grooming: cosine=0.99984456, L1=0.01397907
escape vs feeding : cosine=0.99981271, L1=0.01666667
grooming vs feeding: cosine=0.99978593, L1=0.01748113
```

Cambio L1 del perfil al silenciar cada módulo:

```text
module       escape   grooming  feeding
GF           0.4129   0.4159    0.4012
descending   0.7735   0.7793    0.7618
motor        0.4016   0.3876    0.3966
MBON         0.4118   0.4173    0.4205
KC           0.4131   0.4158    0.4211
```

Archivo crudo persistente en brain-env: `/workspace/h4_actions/h4_actions.json`, 166.534 bytes, md5 `9feeb6447bc2e22edd66ad07d0d012d4`. Log: `/workspace/h4_actions.log`.

## Falsación

**La operacionalización H4 no pasó.** Las tres rutas de entrada anotadas como escape, grooming y feeding producen prácticamente el mismo perfil de salida normalizado: cosine > 0,9997. Silenciar GF, descending, motor, MBON o KC cambia la energía, pero el cambio es casi igual para las tres acciones. No aparece una interacción acción×módulo que permita decir que cada acción activa y desactiva rutas distintas.

## Qué queda demostrado y qué no

Demostrado: las tres fuentes reales generan propagación y los módulos fijados son causalmente relevantes para la energía de la red bajo esta dinámica; descending es el módulo cuyo silenciamiento altera más el perfil en las tres condiciones.

Refutado en este test: que esas tres entradas, por sí solas, seleccionen rutas de salida específicas según acción.

NO MEDIDO: esto todavía no es una falsación total de la hipótesis biológica fuerte. Las etiquetas disponibles son poblaciones sensoriales anotadas, no registros de conducta con contexto idéntico y acción elegida. El experimento prueba una versión más débil: “las vías sensoriales asociadas a escape, grooming y feeding producen rutas distintas sin cambiar el modelo”. Esa versión no sobrevivió.

## Próximo falsador correcto

Hace falta un dataset de acción/contexto real o una tarea conductual validada: misma entrada sensorial, dos acciones posibles según contexto, labels de salida y silenciados cruzados. Sin eso, afirmar “la mosca activa y desactiva según acción” sería adelantarse al instrumento.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (medición científica con runner y recibo)
Review externo: no pedido
Instrumento: `tools/h4_actions.py`, `brain-env`, exit del proceso completado; evidencia cruda en `/workspace/h4_actions.log` y `/workspace/h4_actions/h4_actions.json` con md5 arriba
NO MEDIDO: etiquetas conductuales directas, contexto común con acción alternativa, null de rutas y validación de conducta completa.
