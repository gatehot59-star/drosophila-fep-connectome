# SELLO H_REUSO_CIERRE · 2026-11-01

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157
Rama: `titan/reuso-cierre-2026-11-01`, creada desde `titan/reuso-estricto-2026-11-01` en `6db5d089efa71199f775d1b6619b1cf9f790b7fe`.
Pedido: «AUDITA ESTE TRABSJO Y MEJORA» (Abraham, 1-nov-2026, 13:39 ART).
Motivo: rojos R1 y R2 de la auditoría `docs/auditorias/2026-11-01-02-reuso-estricto-aguanta-flywire-es-proporcion-no-cantidad.md`, en main `d866c2da6de71f404738b059a18014599a9d5c4a`.

## Exposición previa, declarada

Esta variante se eligió **después** de ver el resultado estricto (`0bc09b6`) y los descriptivos de la auditoría. En FlyWire, el real tiene menos pares con plantilla que todos los nulos estrictos, y el nulo estricto no conserva el signo del destino. No es un ensayo ciego: los valores observados de T1 y T2 son los del H_REUSO original y ya se conocen. Lo que no se conoce al sellar es la distribución de este nulo. Ningún sorteo suyo corrió sobre datos reales antes de este commit.

Piloto previo al sello, solo con grafos sintéticos en brain-env. En diez grafos donde la única estructura es que las S prefieren destinos inhibitorios, el nulo estricto dio p en el piso en T1 diez veces y en T2 nueve veces, con 19 nulos. El nulo de este sello dio p en el piso cero veces en cada métrica. En el grafo con motivo plantado dio p en el piso; en el grafo sin motivo, p = 1.

## Pregunta

Con el cableado directo S→D real fijo, y el presupuesto de salida de cada neurona conservado por lado, superclase, signo y rol del destino, ¿las vías S→X→D cierran los pares cableados más de lo esperado, y sus X sirven a más tipos de descendente?

## Lo que no cambia

Poblaciones, umbrales y estadísticos del H_REUSO original, en `reuso_mosca.py` (blob `37b358353ccac46c4b84766f1a63df556dfe531d`):

- S es una unidad tipo/lado de `visual_projection` con tipo y lado válidos; D, lo mismo con `descending`.
- Par cableado: al menos 20 sinapsis S→D agregadas por unidad y mismo lado.
- X tiene signo inhibitorio predicho y queda fuera de los conjuntos S/D elegibles. Cada tramo de la vía necesita al menos 5 sinapsis.
- T1 = pares cableados con plantilla / pares cableados. T2 = X que sirven a al menos dos tipos de descendente.

Cargadores e identidades del estricto, en `reuso_estricto.py` (blob `502b2ee90f90606224a43611bd0c6f4f3b35949c`), importados sin cambios.

## El nulo de cierre

- **Filas fijas:** toda fila con origen en una neurona S elegible y destino en una neurona D elegible. Su destino no se mueve. Por construcción, n_cab de cada nulo es exactamente el real: 996 en FlyWire y 753 en BANC.
- **Filas movibles:** todas las demás. Cada sorteo parte de las filas originales y permuta uniformemente los destinos dentro de cada estrato. El estrato es lado del origen × lado del destino × superclase del destino × signo predicho del destino × rol del destino. El rol puede ser S elegible, D elegible u otro. No es una cadena MCMC.
- **Se conservan:** origen, peso y signo de cada fila; filas y peso saliente de cada origen por lado, superclase, signo y rol del destino; histograma entrante por filas, condicionado al lado del origen; todas las filas S→D.
- **No se conservan:** vecinos únicos tras agregar duplicados, fuerza ponderada entrante, tipo fino del destino, superclase del origen de cada arista entrante ni geometría. Puede haber duplicados y autoaristas.

## Muestras e inferencia

- 200 nulos por conectoma, 400 en total. Semillas 22029 (FlyWire) y 22030 (BANC).
- Humo de validez: dos sorteos por conectoma con semillas 932029 y 932030, sin imprimir T1, T2 ni p. No es un ciego con función de decisión: corre en el mismo job que la serie completa.
- p unilateral por rango: (1 + número de nulos ≥ real) / 201, para T1 y T2 en cada conectoma. Holm sobre las cuatro, alfa 0,05.
- Veredicto por conectoma y final con las reglas originales (`veredicto_conectoma` y `veredicto_final`): H_REUSO_CIERRE_FLYWIRE, H_REUSO_CIERRE_BANC y H_REUSO_CIERRE.
- No se agregan sorteos después de ver resultados.

## Validez

Cualquier falla da INVALIDO:

- Pines de las cuatro entradas; de `reuso_mosca.py`, `prueba_reuso.py` y `reuso_estricto.py`; de este sello; y de `results/reuso_estricto_2026-11-01/estricto.json` (SHA256 `ffce074c422835b426c717902e0510d6bcdd130ecff45d9fccce25e182a89282`).
- Reproducción exacta de los observados históricos y de los controles biológicos del estricto.
- En cada sorteo: índices válidos; filas S→D idénticas; clase, lado, signo y rol del destino idénticos por fila; histograma entrante por lado del origen idéntico; fracción movida mayor que 0,5 en las filas movibles, en S→X y en X→D; n_cab igual al real.
- Presupuestos de salida recomputados por otra vía en el primer y el último sorteo de cada serie.
- 200 huellas de destino distintas por serie. Si los 200 nulos y el real comparten T1 o T2, INVALIDO_NO_IDENTIFICABLE.
- Paridad: una implementación dispersa independiente (scipy.sparse, sin merge ni groupby de pandas) tiene que dar los mismos n_cab, n_pares_ffi, T1, T2 y n_x que `base.estadisticas` en el grafo real y en los sorteos 0 y 199 de cada serie de cierre.

## Controles agregados, informados aparte

No cambian el veredicto de cierre.

- **REPRO_ESTRICTO:** regenerar desde 12029 y 12030 los 200 sorteos estrictos de cada conectoma con `strict_null` y comparar las 400 huellas con `estricto.json`. Recalcular T1 y T2 de los sorteos 0 y 199 con `base.estadisticas` y con la implementación dispersa, y compararlos con el JSON. PASS si todo coincide; si no, FAIL, y el estricto se declara no reproducido.
- **Primer orden, descriptivo:** filas y peso que las S elegibles mandan a X candidatas (inhibitorias, rol otro) en el real, en los sorteos estrictos 0 y 199 y en los de cierre 0 y 199, en total y por superclase del destino; más la misma fracción para todos los orígenes. Mide la dilución que señaló R2. No es inferencial.

## Lectura fijada

- **SOSTENIDA:** con cableado directo real y presupuestos por clase × signo fijos, las inhibitorias cierran los pares cableados y se reusan más que en el azar. El motivo queda como candidato de segundo orden para G1, a comparar contra una G0 por clase × signo. No prueba función ni ahorro.
- **REFUTADA** (FlyWire con las dos p crudas ≥ 0,05): el presupuesto por clase × signo y el cableado directo real alcanzan para la tasa observada. El motivo no tiene que entrar en G1 como regla propia.
- **PARCIAL o NO_SE_REPLICA:** se informa tal cual, sin promover ni descartar el motivo por una sola métrica.
- **INVALIDO:** no hay veredicto; se informa qué guarda falló.

## Fuera de alcance

G1, GPU y Kaggle; inferencia por superclase; S sensoriales; signos desconocidos; geometría; merge. Job en Actions x64 con límite de 60 minutos. Un reintento solo se permite si el intento falló antes de que el instrumento escribiera `cierre.json`, y se declara en la respuesta.
