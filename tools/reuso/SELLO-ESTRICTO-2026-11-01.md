# H_REUSO_ESTRICTO: condicionamiento por superclase de destino

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157

## Pedido, alcance y orden

Abraham: «Run H_REUSO_ESTRICTO before designing G1». Fecha: 1-nov-2026; la hora del commit es el sello verificable. Se prueba el control pendiente de H_REUSO, antes de diseñar G1. No se redefine el motivo ni se construye G1. Los dos conectomas y los resultados originales ya fueron vistos; esto no es una réplica en animales vírgenes.

Este documento se commitea antes del instrumento nuevo y antes de observar cualquier estadístico del nulo estricto. La base de la rama es c74509ac461bb1aa129f1a42dc9645d26b22f444, para reutilizar sin cambios el instrumento histórico. No se mergea código a main.

## Pregunta y falsador

¿El exceso de la plantilla S a D, con S a X a D inhibitoria, persiste cuando el azar conserva para cada neurona cuántas filas y cuántas sinapsis envía a cada superclase de destino y lado?

H_REUSO_ESTRICTO queda SOSTENIDA solamente si T1 y T2 superan este nulo en FlyWire y en BANC, con Holm sobre cuatro pruebas. No sobrevivir significa que el exceso no quedó establecido con este condicionamiento, no que no existan circuitos ni que se haya probado causalmente que la clase explica todo. Se conserva el vocabulario operativo original, incluida REFUTADA, con ese límite.

## Población y métricas, sin cambios

Se usa estadisticas(), control(), holm(), veredicto_conectoma() y veredicto_final() de tools/reuso/reuso_mosca.py, blob 37b358353ccac46c4b84766f1a63df556dfe531d, sin editar. Se verifica el blob antes del import.

- S: tipo y lado válido de visual_projection, no neurona sensorial.
- D: tipo y lado válido de descending.
- X: signo inhibitorio predicho, fuera de las poblaciones S y D elegibles. Esta exclusión NO equivale a excluir todas las neuronas de esas superclases si les faltan tipo o lado.
- Par cableado: mismo lado y suma S a D >= 20 sinapsis.
- Plantilla: suma S a X >= 5 y X a D >= 5.
- T1: pares cableados con plantilla / pares cableados. El denominador se recalcula por grafo, como antes.
- T2: X que participan para dos o más tipos distintos de D, no dos unidades del mismo tipo.
- Signos, lados y sustitución fafb_cell_type por cell_type en BANC se mantienen.

Control de regresión exacto contra el JSON histórico fijado: FlyWire n_cab=996, n_pares_ffi=880, T2=698, n_x=1118; BANC 753, 622, 419, 716. T1 debe ser la división exacta correspondiente. Se mantienen los controles LPLC2/DNp06 en ambos lados y LHAD1g1 exigido en FlyWire.

## Nulo estricto único

Cada fila conserva origen, peso y signo. Se permutan uniformemente los IDs de destino dentro de cada estrato (lado_pre, lado_post, super_class_post). Los lados usan la codificación histórica left/right/other. Cada etiqueta de super_class se conserva literalmente; los ausentes forman una categoría separada. No se homogeneizan los nombres de clases de los dos atlas. Cada realización parte del grafo original y es independiente de las anteriores, con el generador NumPy PCG64; no es una cadena MCMC.

Esto conserva exactamente:

1. Cantidad de filas salientes y peso total de cada origen, también desagregados por superclase y lado de destino.
2. Histograma de filas entrantes de cada destino por lado de origen, y por tanto el total entrante por filas.
3. Origen, peso y signo de cada fila, y lateralidad de ambos extremos.

No conserva por construcción: vecinos únicos después de agregar duplicados, fuerza ponderada de entrada, tipo fino de destino, presupuesto hacia X inhibitorias dentro de una clase, clase del origen de cada llegada, geometría ni oportunidad por arborizaciones. Puede generar duplicados y autoaristas, como el nulo original. No se presenta como control de todos los factores anatómicos.

Se retienen root IDs y superclases en la representación para auditar la alineación. Los descriptivos de las X por superclase no añaden pruebas inferenciales ni se usan para cambiar el nulo.

## Plan fijado

- 200 nulos por conectoma; 400 en total. No se agregan sorteos después de ver los resultados.
- Semilla FlyWire 12029; BANC 12030.
- Humo separado: dos nulos por conectoma, semillas 912029 y 912030; no publica T1, T2, p ni listas de X del humo.
- p unilateral = (1 + cantidad de nulos >= observado) / 201.
- Holm sobre [FW_T1, FW_T2, BANC_T1, BANC_T2], alfa 0,05 y desigualdad estricta < 0,05.
- Por conectoma: SOSTENIDA si ambas p ajustadas < 0,05; REFUTADA si ambas p crudas >= 0,05; en otro caso PARCIAL.
- Conjunto: SOSTENIDA si ambos SOSTENIDA; REFUTADA si FlyWire REFUTADA; NO_SE_REPLICA si FlyWire SOSTENIDA y BANC REFUTADA; en otro caso SIN_DECIDIR. INVALIDO si falla una condición de validez.

## Validez y controles que pueden fallar

Antes del full: pruebas sintéticas positivas y negativas, paridad de la métrica con un contador independiente en grafos pequeños, regresión original y humo ciego válidos.

En cada nulo se revisan forma/rango de índices, clase y lado del destino fila por fila y el histograma entrante por lado de origen. La fuente, pesos y signos no se modifican. Se comprueba además el presupuesto ponderado por origen/clase/lado en fixtures y en el primer y último nulo real.

La fracción de destinos cambiados debe superar 0,5 en todo el grafo y, separadamente, en las filas originales de S a D, S a X y X a D. Un subconjunto vacío es inválido. Se guardan esas cuatro fracciones para cada realización. Todas las 200 huellas de destinos de un conectoma deben ser distintas.

Se registra la variación de T1 y T2. Si para una métrica los 200 nulos y el observado son todos idénticos, el ensayo se marca INVALIDO_NO_IDENTIFICABLE, no como evidencia positiva. Se prueba en un fixture que el detector rechaza ese caso. Una distribución nula constante pero distinta del observado no queda invalidada por ese motivo.

Se sabotean controles de clase, lado, histograma de destinos, identidad del barajado, pin de fuente y plan completo. Un retorno 0 no es el veredicto científico: también una hipótesis REFUTADA debe terminar correctamente.

## Entradas fijadas

- Connectivity_783.parquet: 100804642 bytes, MD5 3d802fd542b5d18570ba1ba0bb0abed9, SHA256 efeb23fb99098e9c390f6869969b2a121a2ee92c833cfc45ecb2c1d8e1af0347.
- Anotaciones FlyWire, commit 17fc57722002e1a7d38cdd0c89ac382bf92718da: 31718505 bytes, MD5 719904abad876c68ace1b5690c9b9b63, SHA256 9a4f8b2f843196074431ebd7cd883536afa1be86c8a4ce90970441e8be81d1be.
- banc_888_meta.feather: 57503026 bytes, MD5 8c2b93a608c7163ec9d94d68e0756ff4, SHA256 86ccf5df0c67419f8c5f43e93a7ed38d23a080e9f7fde26737290252f3780098.
- banc_888_edgelist_simple_v3.feather: 359161658 bytes, MD5 08542b0771db7418ed474be60dc9886c, SHA256 8c296e946f3c69a8c7222f30ad75fa8a98eeb189124fec6df829c9125f4be64b.

Las cuatro huellas completas se midieron en los archivos presentes en brain-env antes de este sello. Las dos de BANC amplían los prefijos del sello original; no los reemplazan por datos distintos.

## Arquitectura y contratos

Árbol incremental: tools/reuso/reuso_estricto.py contiene CLI, cargadores alineados, estratificación, guardas, pruebas sintéticas y ejecución; el módulo histórico y su prueba no cambian. El workflow de la rama ejecuta pruebas, humo y full secuencialmente y guarda log crudo y JSON. No hay servicio, contenedor de producto ni despliegue.

Flujo: entradas públicas fijadas -> validación de bytes -> lectura de columnas -> armar() histórico + IDs/clases -> observación/control -> permutaciones y guardas -> estadisticas() histórico -> cuatro p/Holm -> veredicto derivado. Salida: JSON con cada nulo, controles, entorno, huellas, plan y resultados; log crudo completo. No se commitean datasets ni grafos derivados.

Interfaces: cargar(nombre, rutas) devuelve el diccionario histórico aumentado con ids y sc; preparar(d) añade estratos y referencias de guardas; nulo_estricto(d,rng) devuelve únicamente un vector de destinos; guarda(d,nuevo) devuelve invariantes y cuatro fracciones de movimiento; ejecutar_conectoma devuelve observación y lista completa de 200 nulos. Errores de entradas, guardas, plan, controles o identificabilidad producen INVALIDO y salida no cero. Las excepciones quedan en el log, no se ocultan.

Máquina elegida: Actions x64 del repo público; brain-env sólo para desarrollo y fixtures pequeños. Sondeo del 1-nov: brain-env tiene dos CPU y aproximadamente 1,9 GiB disponibles, por lo que no se carga allí el ensayo completo junto con los otros trabajos. Es una decisión de reparto, no una afirmación de imposibilidad. El runner mide su entorno al ejecutar. Sin Kaggle, sin GPU ni compra de cómputo. Tope del trabajo: 45 minutos, sin reintento científico automático. Si se agota o falla, se conserva la evidencia y se informa INVALIDO/incompleto.

Riesgos: clases faltantes quedan agrupadas y declaradas; el join de caminos puede crecer y se vigilan tiempo y RSS; una guarda que falla frena el ensayo; duplicados y autoaristas quedan explícitamente fuera de las invariantes. A diez veces las filas se requeriría particionar el cómputo de estadísticas, no multiplicar memoria sin medir.

Alternativa descartada para esta prueba: añadir tipo fino, fuerza de entrada o geometría al mismo tiempo. Cambiarían más de un factor respecto del falsador pendiente. Se prueba exactamente el condicionamiento por clase que faltaba; no se elige el nulo más favorable después.

## NO MEDIDO al sellar

El resultado estricto, su tiempo real y su consumo en runner. No se afirma independencia de selección del mismo agente. Ningún resultado de este control, incluso positivo, demuestra función, causalidad, genes, una gramática aprendida ni ahorro de ejecución. G1 sigue sin diseñar.

--- METODO PROMETEO ---
Accion delicada: NO en este commit de protocolo; ejecución y workflow se verifican aparte.
Modo aplicado: LIGERO para el sello documental; instrumento pendiente.
Maquina: brain-env para huellas y lectura; GitHub para el sello.
Rubrica: N/A para este registro previo, no certifica ejecución.
Review externo: no realizado.
Instrumento: lectura de fuente original y huellas reales de cuatro entradas; no hay nulos estrictos observados.
Artefactos: tools/reuso/SELLO-ESTRICTO-2026-11-01.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157
