# 2026-10-13-013 · En criollo y en detalle: qué logramos, contra quién nos medimos, si es relevante y cómo escala

## Veredicto

- **[MEDIDO] Lo central.** Construimos un banco que pone a prueba el cableado real de la mosca (FlyWire v783) contra dos rivales:
  - sus barajados, que conservan los mismos grados y lados pero tienen los cables cambiados;
  - el plano de la propia mosca, que es la regla «tipo de sensor → comando» con los mismos sensores.
- **[MEDIDO] El resultado, en tres escalas.**
  - **Contra los barajados, el cableado real gana siempre.** Pasa con 46, con 1.504 y con 33.489 neuronas.
  - **Contra el plano, sólo la escala grande lo alcanza.** R2, con 33.489 neuronas, queda +0,85 puntos arriba (IC90 [+0,08; +1,51]), sin llegar al margen de un punto. Las escalas chicas quedan alrededor de un punto abajo.
- **[CONCLUSIÓN] Es relevante, pero por el método y por una respuesta honesta, no por un titular.**
  - Responde con números una pregunta abierta del campo: cuánto de la función sale sólo del cableado.
  - La respuesta es sobria: el cableado lleva la función y, simulado, reproduce al diseño. No lo mejora.
  - Es un buen preprint de métodos con un resultado limpio. No es un salto como los de Shiu o Lappalainen, porque ellos validaron en moscas reales y nosotros no.
- **[CONCLUSIÓN] Cómo escala.** En cómputo escala bien y gratis: R2 entero en Actions, 81 trabajos en 3 h 38 min, sin costo. En ciencia, el próximo paso natural es el cerebro entero (138.639 neuronas) y un segundo conectoma (BANC, que trae los IDs de FlyWire 783). En robots escala el plano, no el cableado.

## Pedido

Abraham, 13-oct 17:20: «En criollo me puedes explicar detalladamente que logramos. En contrate con otros autores. Es relevante lo nuestro. Como escala ?? Genera un .md bien detallado».

---

## 1. Qué logramos, en criollo

### 1.1 El mapa funciona y se reproduce

- Cargamos el cableado completo de la mosca: 138.639 neuronas y 15.091.983 conexiones (pares de neuronas), con las mismas huellas en las dos máquinas.
  - Dorkenwald et al. (Nature 2024) reportan 139.255 neuronas y 54,5 millones de sinapsis. Nosotros contamos pares conectados, no sinapsis sueltas.
- Todo resultado se sella antes de correr y se corre en una máquina limpia (Actions), con un ancla que tiene que reproducir lo anterior exacto.
  - Hoy las 90 corridas que el factorial 3 comparte con el factorial 2 dieron **números idénticos**.

### 1.2 El cableado lleva el comportamiento

La tarea simulada es la de la mosca: llega un estímulo y hay que elegir entre cinco acciones (escapar, aterrizar, girar, etc.), con ruido y con distintas intensidades. En las tres escalas, el cableado real le gana a la misma red con los cables barajados:

| Escala | Neuronas | Real | Barajados SL | Barajados T | Fuente |
|---|---|---|---|---|---|
| M46 (el motivo) | 46 | gana en 6 de 6 celdas | 300 | 300 | 015, Holm 0,0399 |
| R1 | 1.504 | 0,937 | 0,774 | 0,742 | factorial 1 |
| R2 | 33.489 | 0,9465 | 0,666 (máx. 0,796) | 0,760 (máx. 0,839) | factorial 3, 0 de 100 lo igualan |

En R2, barajar los cables cuesta 28 puntos y mezclar los tipos de sensor cuesta 19. **El cableado no es decorado: es donde está la función.**

### 1.3 El rival que nos ganaba era la mosca misma

- **La regla a mano no es una invención nuestra.** Es el plano de la mosca idealizado: las etiquetas de FlyWire que dicen qué tipo de neurona va a qué neurona descendente, aplicadas directo a los sensores.
- **Las primeras comparaciones eran injustas.** El factorial 1 comparaba la red con una regla con más sensores que ella. Lo corregimos poniendo los mismos sensores en los dos lados.
- **Con los mismos sensores y muchas semillas** (factoriales 2 y 3), la diferencia entre la red y el plano queda así:

| Escala | Sensores | Red menos plano | Veredicto |
|---|---|---|---|
| M46 | 40 | −0,62 (tasa) y −1,83 (líquida) | no lo alcanza |
| R1 | 418 | entre −1,02 y −1,48 | no lo alcanza |
| R2 | 564 | **+0,85**, IC90 [+0,08; +1,51] | lo alcanza, sin superarlo por el margen |

- **En criollo:** con pocas neuronas la simulación le resta al plano. Con 33.489 neuronas lo alcanza y queda un poquito arriba (gana en 482 de 600 corridas), pero no tanto como para decir que lo supera.

### 1.4 Un reflejo chico que anda

- El escape sale de un motivo de 26 neuronas y 88 conexiones sacado de FlyWire, y funciona en simulación desde el día cero.
  - Le gana a sus barajados cuando importa el cableado fino: 0,8177 contra 0,6819 (SL), 0,5973 (S) y 0,4023 (B), en la respuesta 011.
  - **Letra chica:** un reflejo escrito a mano sin LC6 le gana (0,9167).
- **Entrenar sólo las constantes de tiempo (la neurona líquida plena, 1.378 parámetros) lo lleva a 0,98.**
  - Le gana a un control con los mismos parámetros que no es líquido (0,9826 contra 0,9214, en la 013).
  - Contra 69 barajados entrenados igual, la firma vale para la semilla 0 y como tendencia de grupo (88 %, p 0,0002), no para cada entrenamiento (015).

### 1.5 El mapa sirve para encontrar circuitos

El catálogo de circuitos encontró en el cableado las 10 predicciones de literatura que buscamos (12-oct). El control de las salidas mostró que las descendentes son las que mandan sobre las motoras, el cuello y la antena, y eso aguanta la corrección más dura (max-T).

### 1.6 El Paper 1 quedó más honesto que su versión 1.0

- La v1.0 está en Zenodo. La v2.0 ya tiene el render y la verificación en verde (respuesta 012).
- La v2.0 corrige lo que no aguantaba:
  - el 323× era que los sensores terminan cerca de las motoras, no un principio de cableado;
  - la reciprocidad queda como rango (20,59× a 47,27×);
  - cinco referencias de la v1.0 estaban mal citadas.
- Falta decidir F05 (el +14,8σ).

### 1.7 Lo que no anduvo, y está escrito

- **H4:** el registro de una mosca no generaliza (balanced accuracy 0,502, p 0,623).
- **SparseLTC sin entrenar empata con el control lineal** en 48 de 48.
- **El efecto temporal global no sobrevive a 39 nulos** (p 0,25).
- **El enjambre de robots** no sale del conectoma, escapa hacia la amenaza y su test no puede dar rojo.
- **No hay neurona nueva** (005). La líquida es de la familia LTC (Hasani et al., AAAI 2021) y la que ganó entrenada es una GRU sin compuerta de reset (Cho et al., 2014).

---

## 2. Contra otros autores

| Trabajo | Qué hicieron | Qué tienen que nosotros no | Qué tenemos que ellos no |
|---|---|---|---|
| **Shiu et al., Nature 2024** (doi 10.1038/s41586-024-07763-9) | Cerebro entero de la mosca como red LIF con el cableado y los neurotransmisores; predicen qué neuronas se activan al comer y al acicalarse | **Validación en moscas reales** (optogenética y conducta) | El rival «plano de la mosca» con los mismos sensores, nulos SL y T sellados y tres escalas. **Usamos su mismo archivo de conectividad** |
| **Lappalainen et al., Nature 2024** (doi 10.1038/s41586-024-07939-3) | 64 tipos del sistema visual; entrenan los parámetros de cada neurona para detectar movimiento y predicen la actividad de 26 estudios | Predicción de actividad medida, entrenamiento a escala | Una tarea de conducta con cinco acciones y la comparación contra el diseño. Ellos muestran que funciona mejor con cableado ralo; nosotros, que con cableado chico la simulación le resta al plano |
| **Costi et al., Biomimetics 2025** (doi 10.3390/biomimetics10050341) | El conectoma de la mosca como reservorio para predecir el problema de tres cuerpos; comparan contra reservorios al azar e híbridos | Prueba con el conectoma entero | La tarea es de la mosca, no una serie caótica genérica, y el rival es el plano de la mosca, no sólo el azar |
| **Suárez et al., Nat Mach Intell 2021** (doi 10.1038/s42256-021-00376-1) | Conectoma humano como reservorio contra nulos recableados; el resultado depende del régimen dinámico | Barrido de regímenes, humano | Conectoma a nivel de sinapsis, conducta y rival de diseño |
| **Lechner et al., Nat Mach Intell 2020** (NCP) | 19 neuronas inspiradas en el gusano manejan un auto | **Un robot real andando** | Cableado exacto, no inspirado |
| **Vaxenburg et al., Nature 2025** y **NeuroMechFly v2, Nat Methods 2024** | Cuerpo de la mosca en física; controladores entrenados por refuerzo; NeuroMechFly usa una red visual con conectoma | **Cuerpo y física** | El banco sellado sobre el cableado del cerebro. Su cuerpo es el próximo paso natural para nuestro lazo cerrado |

**[LITERATURA, búsqueda acotada, NO exhaustiva]** En lo que revisé no vi un trabajo que ponga el cableado simulado contra la regla de diseño del propio animal con los mismos sensores, con nulos sellados y en varias escalas. Antes de afirmarlo en un paper hay que hacer una búsqueda sistemática.

---

## 3. ¿Es relevante?

**Sí, en un nicho, y sobre todo por cómo está hecho.**

1. **Responde la pregunta del campo con un número.** Lappalainen la plantea así: «cuánto puede informar el cableado solo sobre la computación». Nuestra respuesta, en esta tarea:
   - el cableado lleva la función: barajado pierde entre 19 y 28 puntos;
   - simulado, con 33.489 neuronas alcanza al plano de diseño de la mosca, pero no lo supera.
2. **El método vale por sí solo.**
   - Sellos antes de correr; anclas que reproducen exacto en dos máquinas; nulos que pueden dar rojo; un rival justo, con los mismos sensores.
   - Una auditoría externa (Tao) verificada punto por punto.
   - Resultados viejos corregidos cuando hubo más datos: la 002 y la 003 por la 007, y el +1,28 de la 007 por la 010.
   - Es lo que hace falta para que un resultado de conectoma se crea.
3. **El resultado negativo es útil.** Le dice a quien quiera usar conectomas en robots que el plano (qué sensor va a qué comando) rinde casi lo mismo que simular todo: 0,927 contra 0,935. Eso ahorra 4 millones de conexiones.
4. **Lo que le falta para ser fuerte:**
   - validación fuera de simulación;
   - un segundo conectoma;
   - más de una tarea;
   - la búsqueda sistemática de antecedentes.

**Dónde publicarlo:** el banco de tres escalas como preprint de métodos (bioRxiv o arXiv), apuntando a una revista de neurociencia computacional. No da para Nature sin validación in vivo. Es una opinión, no una medición.

---

## 4. ¿Cómo escala?

### 4.1 En neuronas

| Escala | Neuronas | Conexiones | Costo medido | Resultado contra el plano |
|---|---|---|---|---|
| M46 | 46 | pocas | segundos | −0,6 a −1,8 |
| R1 | 1.504 | 91.484 | minutos | −1,0 a −1,5 |
| R2 | 33.489 | 4.031.897 | 0,79 s por ensayo en brain-env; trabajos de 29 a 56 min en Actions | +0,85 |
| Cerebro entero | 138.639 | 15.091.983 | **NO MEDIDO**: si el costo sigue a las conexiones, unas 3,7 veces R2 | NO MEDIDO |

- **[CONCLUSIÓN] Más cableado real acerca al plano.** Ojo: el plano también mejora con más sensores (el de 418 le gana al de 40 por +2,79).
- **La pregunta que sigue es concreta:** con el cerebro entero, ¿pasa el margen o se queda en empate?

### 4.2 En cómputo y costo

- **Actions en repo público es gratis.** Corre 20 trabajos en paralelo, con hasta 6 h cada uno.
- **Lo que costó el factorial 3:** 81 trabajos, 600 corridas de grilla y 100 nulos de R2, en 3 h 38 min y a costo cero.
- **[CONCLUSIÓN] El cerebro entero cabe en ese esquema si se reparte en más trabajos.** Es una extrapolación: NO MEDIDO.

### 4.3 En conectomas

- **El banco hoy lee las columnas de FlyWire v783.**
- **BANC** (cerebro más cordón, unas 160.000 a 188.000 neuronas, Bates et al., Nature 2026) trae `fafb_783_match_id`, así que se puede portar el mismo sujeto y la misma regla.
- **MANC** (cordón macho, unas 23.000 neuronas) sirve para la parte motora.
- **[CONCLUSIÓN]** Ese es el «laboratorio para nuevos conectomas» que pediste: hoy está listo para FlyWire y a un puerto de distancia de BANC. Falta portarlo y medir.

### 4.4 En robots

- **Escala el plano, no el cableado.** La regla tipo de sensor → comando entra en un microcontrolador en pocos KB.
- **El reflejo de 26 neuronas también es chico.**
- **Antes de hardware:**
  - arreglar el enjambre: enteros que desbordan y un test que no puede dar rojo;
  - cerrar el lazo en simulación con cuerpo (NeuroMechFly o el modelo de Vaxenburg).

---

## 5. Lo que sigue, en orden

1. **Cerrar la v2 del Paper 1.** Falta F05 (suavizar el +14,8σ), el merge y el token.
2. **Escribir el Paper 2:** el banco y las tres escalas, con la búsqueda sistemática de antecedentes.
3. **Correr el cerebro entero en el mismo banco,** sellado y con margen.
4. **Portar el banco a BANC.**
5. **Arreglar el enjambre y llevar el plano a lazo cerrado.**

---

## Herramientas y máquina

- **brain-env:**
  - clon de main en `9c2cf03`;
  - lectura del CONTEXTO (md5 `ca42f33a…`, secciones del 12 y 13-oct, producto y ciencia, Paper y Tabla 7, H4);
  - prueba del parche del CONTEXTO.
- **Web:** 8 búsquedas para verificar las referencias de la sección 2 y BANC/MANC.
- **GitHub MCP:** este commit.
- No se corrió ninguna medición nueva ni se gastó cuota ajena.

## Evidencia cruda

```
# CONTEXTO leido (brain-env)
9c2cf03 contexto(2026-10-13-012): CONTEXTO al dia con la v2 cerrada salvo F05
ca42f33af0cdf239f667a0874b6faab6  docs/agents/CONTEXTO-drosophila-fep.md
# factorial 3, agregado.log del bot (09ffbc1, run 38420175126, 15:13:21Z a 18:51:57Z)
PRIMARIA R2_CON_TASA W=0.9353 regla_propia=0.9268 dif=+0.0085 IC90=[+0.0008, +0.0151] corridas=600 -> NO_INFERIOR
NULOS SL n=50 media=0.6659 max=0.7955 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
NULOS T n=50 media=0.7598 max=0.8390 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
CHEQUEO REPRODUCE_F2 corridas_comparadas=90 tolerancia=True exacto=True -> True
corridas 600 gana 482 empata 2 pierde 116
grilla (3, 5) 15:13:24Z a 15:42:19Z (29 min) | grilla (1, 4) 15:13:24Z a 16:09:18Z (56 min)
# CONTEXTO, lineas citadas
"W les gana a 300 SL y 300 T en 6/6 celdas (Holm 0,0399)"
"El cableado paga dentro de R1: 0,937 contra 50 SL (media 0,774) y 50 T (0,742), p por rango 0,0196."
"M46_TASA −0,62 puntos (NO_SUPERIOR); M46_LIQ −1,83 (PIERDE)."
"R1, las cuatro configuraciones, entre −1,02 y −1,48 puntos (NO_SUPERIOR)"
"Más sensores pagan: la regla de 418 le gana a la de 40 por +2,79 (AYUDA)."
"R2 (33.489 neuronas, 4.031.897 aristas) ... 0,79 s por ensayo en brain-env"
"W 0,8177 contra SL 0,6819 (6/200, p = 0,0348), S 0,5973 (p = 0,0100) y B 0,4023 (p = 0,0050)"
"el reflejo escrito a mano sin LC6 le gana a la mosca (0,9167"
"Plena (1.378): líquida 0,9826 contra no líquida 0,9214"
"Mann-Whitney 8 W contra 69 SL: U 488 de 552 (88%), p 0,0002"
"HC-2: SparseLTC empata 48/48 con el control lineal sobre FlyWire real"
"balanced accuracy=0.5018855395873556, p=0.623"
"el efecto temporal global no sobrevive (39 nulos, p = 0,25)"
"FWER con los dos nulos: descendentes → descendentes, → motoras, → cuello y → antena"
# cuenta de escala
15.091.983 / 4.031.897 = 3,74
# literatura (busqueda web, abstracts)
Shiu et al., Nature 2024, doi 10.1038/s41586-024-07763-9: LIF del cerebro entero, validado con optogenetica y conducta
Lappalainen et al., Nature 2024, doi 10.1038/s41586-024-07939-3: 64 tipos, 26 estudios, mejor con conectividad rala
Costi et al., Biomimetics 2025, doi 10.3390/biomimetics10050341: conectoma de la mosca como reservorio, contra azar e hibridos
Suarez et al., Nat Mach Intell 2021, doi 10.1038/s42256-021-00376-1: conectoma humano como reservorio contra nulos
Lechner et al., Nat Mach Intell 2020, doi 10.1038/s42256-020-00237-3: 19 neuronas, 253 sinapsis, manejo
Vaxenburg et al., Nature 2025, doi 10.1038/s41586-025-09029-4; Wang-Chen et al., Nat Methods 2024, doi 10.1038/s41592-024-02497-y
Dorkenwald et al., Nature 2024, doi 10.1038/s41586-024-07558-y: 139.255 neuronas, 54,5 millones de sinapsis
BANC (bancr): ~160.000 neuronas, columna fafb_783_match_id; Bates et al., Nature 2026 (preprint bioRxiv 2025.07.31.667571). htem/BANC-project: ~188.000 neuronas
MANC (Janelia): ~23.000 neuronas
```

## Archivos

- **main:**
  - este archivo;
  - `tools/contexto/actualizar_contexto_2026-10-13-013.py`;
  - `.github/workflows/contexto-2026-10-13-013.yml`.

## NO MEDIDO

- **El cerebro entero en el banco:** ni el costo ni el resultado. El «3,7 veces» es una cuenta, no una medición.
- **Otro conectoma** (BANC, MANC): no se portó nada.
- **Nada fuera de simulación.**
- **Que el plano gane en hardware.**
- **La novedad frente a la literatura.** La búsqueda fue acotada, sin revisión sistemática.
- **El lugar de publicación.** Es una opinión.
- **Los números de BANC.** Las fuentes dan entre 160.000 y 188.000 neuronas; no se verificó en sus datos.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El cableado gana a sus barajados en tres escalas | nulos sellados en 015, factorial 1 y factorial 3 | Sí, en las tres |
| Sólo R2 alcanza al plano | factoriales 2 y 3 con los mismos sensores | Sí: R1 podía dar NO_INFERIOR |
| Las referencias existen y dicen eso | abstracts por búsqueda web | Sí: una cita podía no existir o no decirlo |
| «Nadie lo hizo» | búsqueda acotada | Débil: se declara NO MEDIDO |

```
--- METODO PROMETEO ---
Accion delicada: no (sintesis con referencias)
Maquina: brain-env (lectura del CONTEXTO y prueba del parche) | web
Artefactos: docs/agents/respuestas/2026-10-13-013-en-criollo-detallado-que-logramos-frente-a-otros-autores-y-como-escala.md + Doc de ClickUp 2026-10-13-013
```
