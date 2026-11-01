# Topo inverso: tenemos piezas para buscar una gramática funcional del conectoma, todavía no la gramática

**Mi apuesta: pasar de extraer circuitos a buscar programas cortos que generen circuitos.** El cruce más fuerte no es «conectoma + más neuronas líquidas»: es Topo como lenguaje, H_REUSO como indicio de plantillas y H_PARES_DATOS como prueba funcional que una red generada tendría que conservar.

No encontramos todavía la regla generadora del cerebro. Sí tenemos piezas concretas para formular y falsar esa búsqueda. Esta entrega es una exploración documentada, no un prerregistro ni una corrida nueva.

Ruta del Doc: Space > este Doc, sin carpeta intermedia. Fecha: 1-nov-2026, America/Buenos_Aires.

## 1. Pedido

Cruzar la propuesta de diseño inverso del conectoma con nuestros trabajos y explorar nuevas posibilidades. «Cine toma» se interpreta como conectoma por el contenido del mensaje.

Hay dos productos distintos:

- **Explicar:** una regla compacta que prediga conectividad y respuestas no usadas para ajustarla.
- **Rediseñar:** una regla que genere una red más barata para una tarea, aunque deje de parecerse a la mosca.

El segundo puede funcionar sin que el primero sea verdadero. Ninguno demuestra haber recuperado el programa genético o de desarrollo del animal.

## 2. El cruce con lo que ya hicimos

### Topo ya aporta un lenguaje, pero las reglas las escribimos nosotros

[Topo v0.2](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/a817ad361982b1db92e12fd67bc1da590e0e00f8/docs/topo/TOPO-v0.2-diferencial.md) expresa tipos sensoriales, lateralidad, estados, salidas internas y comparadores. El programa leído separa las DNp06 izquierda/derecha y ubica su diferencia aguas abajo.

Eso es una base mucho mejor que empezar mutando millones de sinapsis. Pero Topo describe y ejecuta una regla manual: no aprende una gramática ni demuestra dónde implementa la mosca el comparador. La equivalencia de sus 800/800 decisiones con el programa anterior es precisamente un ejemplo de que **igual función no identifica igual mecanismo**. H_COMPARADOR sigue siendo la pregunta anatómica independiente.

El paso nuevo sería invertir el recorrido: especificación funcional → búsqueda de programa Topo → generación de familias de grafos → validación. Lo llamo **Topo inverso** como nombre de la propuesta, no de una herramienta ya implementada.

### H_REUSO es el antecedente propio más directo

Leí el [log íntegro de H_REUSO](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/c74509ac461bb1aa129f1a42dc9645d26b22f444/results/reuso_2026-10-14/reuso.log) y el código que construye su nulo.

La plantilla es: un sensor conecta con una descendente y también con una interneurona inhibitoria que conecta con esa descendente. En los pares elegibles aparece en el 88,35 % de FlyWire y el 82,60 % de BANC. Participan en esa plantilla hacia al menos dos tipos de descendente 698 neuronas inhibitorias en FlyWire y 419 en BANC, contra medias de 128,6 y 11,0 en sus nulos. Las cuatro pruebas dan p ajustada por Holm de 0,0199.

Esto sostiene el enriquecimiento anatómico **contra ese nulo**, no una ley generadora ni la función fisiológica de cada motivo. El código baraja destinos dentro de bloques de lateralidad; no mantiene cuánto envía cada interneurona a la clase descendente. Esa especialización de clase puede explicar parte del resultado. H_REUSO_ESTRICTO es el control pendiente que conviene hacer antes de convertir el motivo en «regla del cerebro».

Además, el signo en BANC es una convención basada en neurotransmisor predicho. La próxima prueba debe separar signos desconocidos y analizar sensibilidad, no tratarlos como fisiología confirmada.

### El embudo aporta una función concreta que intentar conservar

El [agregado de H_PARES_DATOS](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/e5db87062e6dfeb1a370e53c11926660f1dc0bc8/results/pares_datos_2026-10-18/agregado.log), leído junto al sello, registra una ventaja media del embudo con lector de +15,20 puntos sobre PCA, +9,04 sobre proyección aleatoria y +4,01 sobre el lector crudo, promediando la curva de 6 a 768 ejemplos y las dos condiciones estudiadas.

La oportunidad es preguntar: **¿una gramática puede generar otro embudo que conserve esa ventaja sin guardar el cableado exacto?** Eso sería una prueba funcional mucho más informativa que producir un grafo visualmente parecido.

Límites importantes: son estímulos simulados, dos condiciones y una prueba; el embudo entrega 240 rasgos pero sigue calculando R2, de 33.489 neuronas y 4.031.897 aristas. Igual ancho de salida no es igual costo del extractor. Tampoco gana en cada punto: con 2.400 ejemplos el crudo y PCA lo superan en c2. La ventaja «primer día» del sello es agregada entre condiciones; no una victoria uniforme en cada una.

### Los negativos nos dicen qué no buscar

- **No buscar tamaño por sí mismo.** En el factorial 4, cerebro entero menos R2 dio +0,01 puntos, IC90 de −0,01 a +0,04, equivalente en esa tarea. No significa que las neuronas restantes sean inútiles para otras funciones. Fuente E4.
- **No confundir compresión anatómica con conservación funcional.** El núcleo reducido perdió 4,59 puntos contra R2, IC90 de −5,07 a −4,10, y perdió en las 600 corridas. Retener conexiones fuertes no bastó. Fuente E5.
- **No usar SparseLTC como oráculo de biología.** El historial de MN9 muestra que cambiar la célula neuronal puede cambiar qué nulos pasan. Una topología optimizada contra una sola dinámica puede explotar sus errores. Fuente E6, estado histórico, no reejecutado aquí.
- **No sumar DBC3 por identidad del proyecto.** La evidencia vigente de Mojo registra ventajas selectivas y derrotas frente a rivales ajustados. DBC3 puede competir como memoria/lector, pero no entrar por obligación en cada nodo. Fuente E7.

## 3. Qué corregiría o precisaría del texto que trajiste

### La analogía con Princeton sirve, pero no alcanza

El artículo identificado de Karahan y colaboradores usa un predictor electromagnético para buscar estructuras y las contrasta con simulaciones y circuitos fabricados. Su lección útil es **optimizar con un modelo rápido y verificar por otra vía**. No demuestra un óptimo único. En nuestro caso la incertidumbre del modelo neuronal es una parte central del problema, no sólo un costo de simulación. Fuente P1.

### FlyVis está un paso más cerca de una gramática de lo que sugiere el resumen

Lappalainen y colaboradores no aprendieron libremente la topología, pero tampoco copiaron un cerebro entero neurona por neurona: ensamblaron conectividad local y la repitieron en una retícula hexagonal, suponiendo periodicidad. Su red tiene 45.669 neuronas, 1.513.231 conexiones y 734 parámetros libres compartidos por tipos y pares de tipos. Contrastaron predicciones con 26 estudios. Fuente P2.

La diferencia defendible de nuestra propuesta sería **aprender y comparar las reglas de generación**, no simplemente «generar conexiones por tipos», algo que ya tiene antecedentes.

### La distancia no puede entrar como una palabra genérica

Ya hay modelos generativos de conectomas: modelos jerárquicos por bloques y reglas exponenciales de distancia, entre otros. El trabajo de Péntek y Ercsey-Ravasz explica propiedades del projectome, entre regiones; no demuestra la misma ley entre cada par de neuronas. Betzel y colaboradores muestran que, a escala celular, distancia entre somas y costo por arborizaciones no son intercambiables. Fuentes P3 y P4.

En nuestro `reuso_mosca.py`, el cargador usa identificadores, pesos, signo, tipo, lado y clase. **Ese instrumento no carga geometría ni solapamientos.** No significa que esos datos no existan en FlyWire: significa que no debemos inventar d u O para completar la ecuación. Una primera versión puede trabajar con tipos y lateralidad; una versión morfológica requiere su exportación, unidades, cobertura y control de procedencia.

### Motivos, complejidad y sinapsis necesitan definiciones operativas

- Si M_ij se calcula mirando las conexiones reales que queremos predecir, filtra la respuesta. Para generar motivos hace falta un modelo conjunto de grafos o un proceso secuencial que sólo consulte el grafo ya generado, no el objetivo reservado.
- Una tabla beta para cada par de miles de tipos puede memorizar tanto como una matriz. Hay que penalizar el programa, sus tablas, etiquetas, excepciones y parámetros; contar «pocas reglas» no alcanza.
- Primero modelaría presencia de conexión, después cantidad de contactos y después dinámica. El conteo de contactos no determina por sí solo eficacia, retardo, plasticidad o neuromodulación.
- Los 139.255 nodos y 54,5 millones de sinapsis del atlas publicado no contradicen nuestros 138.639 nodos y 15.091.983 aristas agregadas: no son el mismo universo ni la misma unidad. La comparación debe fijar versión, filtros y agregación. Fuente P5 y log de H_REUSO.

## 4. Posibilidades nuevas que sí nacen de este cruce

### A. Una gramática anatómica comprobable

Aprender una regla que combine selección por tipo/lado, distribución de grados y una plantilla de inhibición de avance. Generar múltiples redes diferentes, no una réplica determinista escondida detrás de los identificadores.

Una regla candidata, en palabras: «para ciertas familias sensor-descendente del mismo lado, añadir una vía directa y otra por una población inhibitoria compartida, con ganancias y probabilidades aprendidas por familia». Es una hipótesis, no una descripción ya demostrada de cómo se desarrolla el animal.

**Qué la haría valiosa:** predecir conexiones y patrones reservados mejor que un modelo por bloques sin motivos, usando menos descripción total que almacenar el grafo.

**Qué la tumba:** la ganancia desaparece al preservar clase, grado, lateralidad y, cuando estén medidos, oportunidades geométricas; o sólo reconstruye las conexiones que vio.

### B. Un «genoma» funcional pequeño, sin fingir que es ADN

Buscar la descripción mínima suficiente para el embudo de escape/aterrizaje: programa + parámetros + excepciones. El objetivo no sería conservar cada arista de R2, sino su curva de pocos datos y las respuestas a perturbaciones.

Esto conecta Topo con H_PARES_DATOS y evita repetir la poda por fuerza que falló en H_CONSENSO. El resultado puede ser una familia de topologías funcionalmente equivalentes. No hay motivo para exigir una única solución.

**Falsador:** con datos y ajuste pareados, pierde más que el margen fijado frente a R2, o cuesta más que una regla manual/un embudo artificial equivalente. Una descripción corta que al expandirse consume la misma RAM y cómputo sólo comprime almacenamiento, no ejecución.

### C. Usar el diseño inverso para elegir la próxima prueba

Dos reglas pueden acertar las mismas acciones y disentir sobre qué interneurona importa, qué ocurre al apagar un sensor o cuándo cambia una respuesta. Podemos buscar el estímulo o silenciamiento que maximice ese desacuerdo y registrar las predicciones antes de contrastarlas.

Topo v0.2 y H_COMPARADOR son un caso concreto: mover la resta en el programa preservó la salida, pero dejó una predicción distinta sobre dónde debería estar el mecanismo.

**Valor:** convertir una colección de redes que «andan» en hipótesis distinguibles. **Falsador:** las predicciones diferenciales fallan en el dato reservado. Si sólo contrastamos contra otro simulador, es consistencia entre modelos, no causalidad en la mosca.

### D. Diseñar para el dispositivo, no meter el cerebro a la fuerza

Una vez aislada una función útil, el generador podría buscar topologías con fan-in limitado, estado pequeño, conexiones locales y costo de actualización acotado. Ahí se cruzan la línea del compilador, la cámara y la colmena.

Para la cámara: optimizar también cuánto se propaga un cambio y cuántos estados hay que recalcular. No basta con que pocas entradas cambien; nuestro historial de H-RT0b ya mostró la expansión de las dependencias en capas profundas. Para una colmena: generar conexiones entre **módulos**, no equiparar una ESP32 con una neurona biológica; penalizar bytes transmitidos, saltos, demoras y energía. Fuente E7 y E8.

DBC3, GRU con tiempo y una regla sin memoria serían candidatos dentro del mismo presupuesto. La nueva idea no rescata automáticamente al auto-modelo SELF: DBC-RT-AUTO1 quedó ROJO y su cubeta INVÁLIDA en la lectura vigente. Fuente E9.

**Falsador:** no mejora la frontera de precisión, latencia y energía frente al rival simple en la placa; en colmena, anular o permutar los mensajes no empeora la tarea. Esta línea es posterior a la prueba funcional, no el primer gasto.

## 5. El primer experimento que recomiendo

**Prioridad: gramática de inhibición de avance + embudo, no cerebro entero ni lenguaje.** Criterio: es el tramo que comparte una plantilla anatómica medida, un lenguaje existente y una función con comparación pareada. El modelo generador aún debe implementarse; no hay una dependencia de MLIR ni del port embebido para probar primero la hipótesis científica.

1. **Cerrar el control estricto.** Conservar grados y lateralidad, pero también el presupuesto de salida por clase de cada interneurona y las mezclas relevantes entre clases. Verificar que el nulo mezcla realmente y que no conserva por construcción el estadístico investigado. Reportar qué preserva exactamente después de agregar contactos; no confundir grados de filas con grados de vecinos únicos.
2. **Comparar dos gramáticas pequeñas.** G0: tipos/lado con corrección de grado. G1: lo mismo más la plantilla FFI. La comparación G1 contra G0 pregunta si el motivo agrega información; no contra un azar demasiado fácil. Los grados del conjunto reservado no se usan para entrenar. Un control condicionado a grados observados se etiqueta como tal, no como predicción de un individuo nuevo.
3. **Separar los dos objetivos.** Para explicar, ajustar anatomía y congelar la gramática antes de medir función. Para rediseñar, permitir optimización funcional, pero llamarla rediseño y evaluarla en una prueba nueva. No ajustar los pesos de la pérdida mirando el resultado final.
4. **Reservar datos de verdad.** BANC ya fue observado en H_REUSO y otros análisis: no es un test virgen. Hace falta definir qué circuitos, particiones o datos no vistos quedan reservados y documentar exposición previa. Dos hemisferios no cuentan como dos animales independientes. Si los tipos fueron asignados usando conectividad, declarar que la predicción está condicionada a esas etiquetas y evitar filtración adicional.
5. **Congelar interfaces y presupuestos.** Grafo real, G0, G1 y nulos con las mismas entradas/salidas, dinámica, lector, datos y presupuesto de ajuste. Primero igualar tamaño y conexiones para aislar la regla; recién después variar recursos para buscar compresión. No dejar que un lector más grande compense una gramática peor.
6. **Medir tres cosas por separado.** Predicción anatómica reservada y calibración; acierto/curva de pocos datos y perturbaciones; longitud total de descripción y costo de ejecución. Usar conjuntos de grafos y semillas nuevos, no elegir el mejor ejemplar. No tratar millones de aristas correlacionadas como millones de réplicas biológicas.
7. **Poner controles que puedan contradecir la propuesta.** G1 con su término de motivos anulado; etiquetas de acción permutadas; signos o entradas alterados; recuperación de un resultado conocido del banco. Para una afirmación temporal, estímulos temporales: una lectura en punto fijo no puede demostrar que la constante de tiempo aporta.
8. **Sellar antes de correr.** Márgenes, particiones, semillas, multiplicidad y límites de costo se fijan después de calibrar el instrumento, antes de ver la comparación nueva. Este documento no sustituye ese sello ni autoriza consumo de GPU.

La lectura de resultados también debe quedar fijada:

- Anatomía sí, función no: tenemos un modelo anatómico, no un principio funcional.
- Función sí, anatomía no: tenemos un diseño de ingeniería, no una explicación biológica.
- G0 iguala a G1: la regla simple alcanza; el motivo extra no se ganó su lugar.
- G1 conserva función pero no reduce costo: hay regularidad útil, todavía no ventaja para el dispositivo.
- Sólo funciona con una dinámica y falla con una referencia apropiada: posible ajuste al simulador, no validación biológica.

## 6. Herramientas, máquinas y qué se verificó en este turno

Lectura en vivo de GitHub: contextos, últimas respuestas, ramas, PR abiertos del conectoma, programas, sellos y logs. Repos fijados al leer: conectoma `3aa1a17e411e617322cd1994a1a19e931b629116`; Mojo `e4f52fdeb3141b5693edf4edb5e9ac831ffea760`; DualBrain `5a30c61b7497279c47f3cb96540db25eccd23280`. Las ramas experimentales se citan con su commit en los enlaces.

Búsqueda y lectura de ClickUp para el alcance y la última entrega del motor. Búsqueda web y lectura de fuentes primarias para Princeton, FlyVis, modelos generativos y unidades del atlas. Es una revisión focalizada, no sistemática ni exhaustiva.

Se abrió `00-ENTORNOS-Y-CAPACIDADES.md`: su medición general es de agosto y el contexto de Mojo contiene correcciones posteriores. No se usó esa foto para prometer capacidad actual, duración o cuota.

**Mediciones experimentales nuevas: ninguna.** Los números anteriores son relecturas de evidencia histórica, no réplicas realizadas en este turno. No se solicitó ejecución en brain-env, Actions o Kaggle, ni se lanzó un entrenamiento. No se midieron eventuales verificaciones automáticas de CI asociadas al commit documental.

Escrituras de esta entrega: una rama documental, este archivo de respuesta y su Doc público de ClickUp. Sin código nuevo, cambios de firmware, modificaciones de sellos existentes ni merge.

## 7. Evidencia cruda y procedencia

Los logs completos ya están commiteados y se conservan en sus commits originales: no se sustituyen por esta síntesis. Sus enlaces están arriba o en Fuentes. Identidades de los blobs devueltas al leer:

- H_REUSO, `results/reuso_2026-10-14/reuso.log`: `ef631e911155afbc468658c410f552681264d78f`; salida final `EXIT_RUN=0 | 205.2 s`. El mismo log identifica el instrumento con md5 `e9a07a7c58d926c00fec9c64cf4eb253` y conserva los pines de ambos conectomas.
- Su código, `tools/reuso/reuso_mosca.py`: `37b358353ccac46c4b84766f1a63df556dfe531d`. Se leyeron `nulo`, `guarda_nulo`, `estadisticas` y ambos cargadores; la limitación de clase sale de esas operaciones, no sólo del recibo.
- H_PARES_DATOS, `results/pares_datos_2026-10-18/agregado.log`: `66c19d19aacb904b4c45b650c78fb19177999b4b`; `EXIT_RUN=0`. Sello leído: `tools/pares/SELLO-PARES-DATOS.md`, blob `22e2360b06a90d4bbaadcd388b89ed83e28d92d2`.
- Factorial 4, `results/factorial4_2026-10-13/agregado.log`: `77ee1609cc478358f2f7f36d8e11eb9c2120ccbe`; `EXIT_AGREGADO=0`.
- Núcleo, `results/nucleo_2026-10-14/agregado.log`: `86ce1311ea8d7bf8e4a1d99d8846729093543f3f`; `EXIT_AGREGADO=0`.
- Programa leído, `tools/topo_v02/escape_dif.topo`: `5e48c32e2bbc6fef649710aee027a1c4ba304dc0`.

Estos códigos de salida pertenecen a las corridas históricas. No se atribuyen a una ejecución de hoy. Leer un log que declara SOSTENIDA tampoco demuestra que una gramática nueva funcione: esa afirmación permanece NO MEDIDA.

## 8. Archivos generados

- Repo: `gatehot59-star/drosophila-fep-connectome`.
- Rama documental: `titan/docs-gramatica-conectoma-2026-11-01`, desde el main leído, sin merge.
- Archivo: `docs/agents/respuestas/2026-11-01-01-topo-inverso-gramatica-funcional-por-medir.md`.
- [Doc público: 2026-11-01 · Topo inverso: tenemos piezas para buscar una gramática funcional del conectoma, todavía no la gramática](https://app.clickup.com/90171457413/docs/2kza6fw5-26157), en Space.

No se modificó el contexto canónico: no cambió ningún resultado experimental ni se abrió una corrida. Las prioridades de la sección 5 son una recomendación para esta exploración, no una orden a otro ejecutor.

## 9. NO MEDIDO

- Aprendizaje de una gramática generadora y su compresión real.
- H_REUSO_ESTRICTO y el valor adicional del motivo sobre un modelo por tipos/grados adecuado.
- Preservación de H_PARES_DATOS por grafos generados; generalización a tareas nuevas y robustez fuera de lo entrenado.
- Geometría y solapamientos incorporados al instrumento propuesto.
- Identificación del mecanismo biológico, desarrollo genético, plasticidad y validación con actividad o perturbación del animal.
- Ventaja de DBC3 dentro de esta nueva cadena, rendimiento físico de cámara/colmena, energía y causalidad de la comunicación.
- Novedad global de la propuesta: se verificaron antecedentes concretos, no se hizo una revisión sistemática.
- Tiempo, RAM y cuota de la futura búsqueda. No doy una estimación sin piloto.

## Fuentes complementarias

<details>
<summary>Repositorios y literatura primaria</summary>

- E3. [Código de H_REUSO y su nulo](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/c74509ac461bb1aa129f1a42dc9645d26b22f444/tools/reuso/reuso_mosca.py).
- E4. [Factorial 4: cerebro entero frente a R2](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/87be7634649026d317b8f775654379ab92e2857f/results/factorial4_2026-10-13/agregado.log).
- E5. [Núcleo reducido: pérdida funcional](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/2d4dbfb973c70745a312d5cb4c1c935baa6c0e3b/results/nucleo_2026-10-14/agregado.log).
- E6. [Contexto del conectoma, con MN9, H_COMPARADOR y límites de los modelos](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/3aa1a17e411e617322cd1994a1a19e931b629116/docs/agents/CONTEXTO-drosophila-fep.md). Secciones de las respuestas 049 a 055 y 026.
- E7. [Contexto vigente de Mojo, DBC3 y la cámara](https://github.com/gatehot59-star/mojo-absoluto/blob/e4f52fdeb3141b5693edf4edb5e9ac831ffea760/docs/agents/CONTEXTO-mojo-absoluto.md). Reemplaza cifras antiguas del motor cuando chocan con mediciones posteriores.
- E8. [Colmena DualBrain: propuesta, no cerebro demostrado](https://github.com/gatehot59-star/dualbrain/blob/5a30c61b7497279c47f3cb96540db25eccd23280/docs/agents/respuestas/2026-10-31-01-arquitectura-colmena-dualbrain-esp.md).
- E9. [DBC-RT-AUTO1: ROJO e INVÁLIDO, según hipótesis](https://app.clickup.com/90171457413/docs/2kza6fw5-26137/2kza6fw5-29157).
- P1. [Karahan et al., diseño inverso de circuitos RF, Nature Communications 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11685664/).
- P2. [Lappalainen et al., redes restringidas por el conectoma, Nature 2024](https://www.nature.com/articles/s41586-024-07939-3).
- P3. [Péntek y Ercsey-Ravasz, regla de distancia en el projectome, Network Neuroscience 2025](https://direct.mit.edu/netn/article/9/3/869/128460/The-exponential-distance-rule-based-network-model).
- P4. [Betzel et al., modelos jerárquicos por bloques y geometría celular, PNAS 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11420166/).
- P5. [Dorkenwald et al., atlas del cerebro adulto, Nature 2024](https://www.nature.com/articles/s41586-024-07558-y).

</details>

--- METODO TITAN ---

Acción delicada: NO; lectura y documentación nueva, sin alterar producto, sellos ni resultados.  
Modo aplicado: TITAN LIGERO, consulta técnica y exploración de hipótesis, sin implementación.  
Rúbrica: N/A (modo ligero); autocheck de sujeto, unidades, alcance, exposición previa y separación entre evidencia y propuesta.  
Review externo: no realizado; no se presenta la síntesis como auditoría independiente.  
Instrumento: archivos y metadatos de GitHub, logs históricos completos, Docs de ClickUp y fuentes primarias web; ninguna medición experimental nueva.  
Máquina: servicios de lectura/publicación; brain-env, Actions y Kaggle no utilizados como ejecutores experimentales en este turno.  
Artefactos: `docs/agents/respuestas/2026-11-01-01-topo-inverso-gramatica-funcional-por-medir.md`, en la rama documental, y Doc público de ClickUp enlazado en la sección 8.
