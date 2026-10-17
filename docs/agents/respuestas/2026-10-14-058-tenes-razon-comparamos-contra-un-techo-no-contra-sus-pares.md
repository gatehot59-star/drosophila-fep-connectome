# 2026-10-14-058 · Tenés razón: comparamos la mosca contra un techo, no contra sus pares; cada pieza que queremos tomar tiene su par artificial, y lo que hay que medir es datos, robustez y costo, no sólo acierto

**Fecha:** 2026-10-17, 19:10 (America/Buenos_Aires)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23817

## Pedido

«que es un lector clasico, segun tu contra qien debe ser cmparaod lo hayado en la mosca, donde crees tu que se aplica lo que descubrimos, paper1 2 y 3, creo que no estas comparado lo que queremos tomar de la mosca con sus pares artificiales» (Abraham, 17-oct 18:47), sobre la 057 y con el Doc de la 2026-10-12-011 seleccionado.

Son cuatro cosas:
- qué es un lector clásico;
- contra quién comparar lo hallado;
- dónde se aplica cada paper;
- la crítica de fondo.

Sin corridas nuevas.

## Veredicto primero

- [CONCLUSION] **Tenés razón en lo de fondo.** H_RIVAL comparó la mosca contra un techo, no contra su par.
  - El lector clásico leía los 22.560 números crudos de cada ensayo, se entrenaba con 2.400 ensayos etiquetados y ajustaba unos 135.000 pesos.
  - La mosca leía con 6 umbrales calibrados sólo con ensayos donde no pasa nada, más una τ elegida entre 10.
  - Eso dice cuánto falta para lo mejor posible en esa tarea. No dice si la pieza que queremos tomar de la mosca es mejor que la pieza artificial que haría el mismo trabajo con el mismo presupuesto.
- [MEDIDO] **La asimetría estaba declarada en el sello** (Limitación 3: «el presupuesto de elección es el mismo, la capacidad no»). Pero en la 057 la resumí como «no es un cerebro mejor que lo clásico» y «para un producto conviene lo clásico», y eso fue de más. Lo corrijo acá, en el Doc de la 057 y en el CONTEXTO.
- [CONCLUSION] **Lo que queremos tomar de la mosca no es acierto bruto.** Es funcionar sin datos etiquetados, aguantar cuando algo falla y costar poco, y esas tres cosas casi no las medimos.
- [CONCLUSION] **La literatura que sí comparó contra pares artificiales encuentra justo eso.** El cableado de la mosca rinde parecido a redes artificiales del mismo tamaño y aguanta mejor fuera de lo entrenado (FLYNN, 2026). Además, buena parte de la ventaja desaparece con controles estrictos (Dhiman, 2026).
- **Propuesta (sin sellar): H_PARES, en tres piezas.** Empezaría por la más barata: la curva de datos (cuántos ensayos etiquetados necesita cada uno para alcanzar a la mosca), con el embudo de la mosca contra embudos artificiales del mismo ancho.

## 1. Qué es un lector clásico

- [HECHO] **Un lector** es la parte que convierte lo que hay (los sensores, o la actividad de la red) en una decisión: escapar a la izquierda, escapar a la derecha, aterrizar o nada.
- [HECHO] **«Clásico»** quiere decir aprendizaje automático estándar, entrenado con ejemplos etiquetados y sin nada de la mosca:
  - **ridge:** una regresión lineal con un freno para no sobreajustar; cada número de entrada recibe un peso por acción;
  - **MLP:** una red neuronal chica, con una capa de 32 neuronas.
- [MEDIDO] **Cómo se usaron en H_RIVAL** (sello en `titan/rival-2026-10-15`):
  - los dos leían directo los 22.560 números crudos de cada ensayo (564 sensores por 40 pasos), sin pasar por el cableado;
  - se entrenaban con 2.400 ensayos etiquetados y elegían entre 10 ajustes por validación cruzada;
  - la mosca (W) elegía entre 10 juegos de constantes de tiempo y ajustaba 6 umbrales.
- [CUENTA] **El presupuesto de cada uno**, con un modelo por estado (4 acciones en vuelo, 2 posada):
  - el ridge ajusta 22.560 × 6 = 135.360 pesos;
  - el MLP, más de 700.000 por estado;
  - los 6 umbrales de la mosca salen sólo de ensayos sin evento: el cuantil del 95 % de cada línea, en `umbrales()` de `tarea_mosca.py`. No usan ningún ejemplo de acción;
  - la elección de τ (1 de 10) sí usó el acierto sobre ensayos etiquetados, por validación cruzada (H_TAU).
- [MEDIDO] **En H_LECTOR**, el mismo ridge leyendo sólo las 6 descendentes de la mosca usa 240 rasgos (1.440 pesos, por cuenta) y queda a 0,3 puntos del ridge crudo.

## 2. Contra quién comparar: cuatro preguntas, cuatro rivales

| Pregunta | Rival | Qué tiene que ser igual | Estado |
|---|---|---|---|
| ¿Importa el cableado exacto? (ciencia) | sus barajados: SL cambia quién se conecta con quién, con los mismos grados y lados; T deja el cableado y baraja los tipos | el resto: neuronas, cantidad de conexiones, entradas y lector | hecho: gana en las cuatro escalas |
| ¿Conviene tomar esta pieza de la mosca? (ingeniería) | su par artificial: la pieza que diseñaría un ingeniero para el mismo trabajo | entradas, presupuesto (neuronas, conexiones o parámetros), datos de entrenamiento, inicialización y lector | casi sin hacer |
| ¿Cuánto falta para lo mejor posible? (calibración) | el techo: el mejor lector sin límite de capacidad | sólo las entradas y la prueba | hecho (H_RIVAL), pero lo reporté como si fuera la segunda |
| ¿Se parece a la biología? | la mosca viva, o un modelo validado con ella (Shiu) | estímulo y lectura | hecho contra Shiu; contra moscas vivas, NO MEDIDO |

[CONCLUSION] La segunda pregunta es la que vos marcás, y es la que decide qué nos llevamos de la mosca.

## 3. Qué pares artificiales ya medimos (inventario honesto)

- [MEDIDO] **El motivo de 26 neuronas como reservorio** (2026-10-11-008), en 4 tareas genéricas:
  - empata con su barajado (4 de 4);
  - no le gana a un reservorio de ruido (0 de 4): «paga la sparsity, no la mosca»;
  - en su función propia, el escape difícil (011), sí les gana a sus nulos SL, S y B.
- [MEDIDO] **La líquida plena** contra una no líquida con los mismos parámetros (013 y 014): gana la líquida.
- [MEDIDO] **DBC3 contra LSTM** (003 y 004): empatan. En memoria larga ninguna aprende, y una máquina de estados de dos líneas les gana.
- [MEDIDO] **SparseLTC contra su control lineal** en `mojo-absoluto` (HC-2): empate 48 de 48.
- [MEDIDO] **El cerebro entero con SparseLTC** contra una propagación sin dinámica (049, PROX): gana SparseLTC por +0,110.
- [NO MEDIDO] **Falta lo que más importa:**
  - el cableado de R2 contra reservorios artificiales del mismo tamaño;
  - el embudo contra embudos artificiales del mismo ancho;
  - el plano contra una regla aprendida del mismo tamaño;
  - el módulo que se reusa contra módulos compartidos;
  - y, en todos, datos, robustez y costo.

## 4. Pieza por pieza: qué queremos tomar y contra qué par

| Pieza | Qué queremos tomar | Par artificial | A igualdad de | Dónde debería ganar | Estado |
|---|---|---|---|---|---|
| El plano (tipo de sensor → comando) | un reflejo chico que anda sin entrenar | una regla aprendida rala con el mismo número de conexiones; con píxeles, un detector clásico de choque (tasa de expansión o tiempo al contacto) | entradas y conexiones | ensayos etiquetados necesarios, acierto con un sensor muerto, bytes | NO MEDIDO |
| El cableado como reservorio (R2, 33.489 neuronas) | rasgos útiles sin entrenar la red | reservorio aleatorio ralo (Erdős-Rényi), de mundo pequeño (Watts-Strogatz), y una GRU o CfC entrenada con los mismos parámetros | neuronas, aristas, radio espectral, lector L e inicialización | acierto con L; robustez ante ruido fuera de lo entrenado, un sensor apagado o un 10 % de neuronas muertas | parcial: les gana a sus barajados; en el motivo de 26, pierde con el ruido |
| El embudo de 6 descendentes | comprimir 22.560 números a 240 | PCA, proyección aleatoria y un cuello entrenado de 6 canales | ancho (240 rasgos) y lector | acierto con pocos ensayos etiquetados | NO MEDIDO: sólo contra el ridge crudo |
| El módulo de inhibición que se reusa (H_REUSO) | un módulo para varios comandos | un controlador con módulo compartido contra módulos separados | parámetros totales | acierto por comando y parámetros ahorrados | NO MEDIDO: es estructura |
| La jerarquía de salidas (Paper 3) | un bus de comandos chico | control jerárquico (subsunción de Brooks) contra un controlador plano | sensores y motores | robustez y latencia | NO MEDIDO |
| El aislamiento entre modalidades (Paper 1) | fusionar sensores sin que se pisen | fusión temprana contra fusión tardía en una red multimodal | parámetros | interferencia entre sensores | NO MEDIDO: sólo contra nulos de red |
| La τ líquida | integrar en el tiempo con pocos parámetros | LTC o CfC de Hasani, GRU, LSTM | parámetros y cableado | acierto y datos | parcial: le gana a su control no líquido |
| La memoria (DBC3) | memoria selectiva | LSTM, GRU, máquina de estados | parámetros | memoria larga | hecho: empata con LSTM y pierde con la máquina de estados |

## 5. Qué dice la literatura que hizo estas comparaciones

- **FLYNN** (Wang y Chen, arXiv 2607.00025, jul-2026):
  - el conectoma entero de FlyWire v783 como red recurrente, con la misma clase de neurona con fuga que usamos, para navegar un robot en MuJoCo;
  - lo comparan contra redes artificiales con los mismos parámetros (EfficientNet-B0 y MobileNet-v3, unos 5 millones) y una red de mundo pequeño, con las mismas entradas y el mismo entrenamiento;
  - rinde parecido, aguanta mejor fuera de lo entrenado y sin sensores, y sigue andando sin visión;
  - ojo: entrenan todos los pesos del conectoma; nosotros no.
- **Dhiman** (arXiv 2604.04033, abr-2026): con el conectoma visual de la mosca, la ventaja de la topología contra un azar ingenuo «desaparece en gran parte» con la misma inicialización y un nulo que conserva grados. Nuestro SL es ese nulo.
- **Costi et al.** (Biomimetics 2025): el conectoma de la mosca como reservorio para series caóticas, contra reservorios estándar e híbridos. Sobreajusta menos, y aportan tanto la topología como los pesos.
- **McAllister et al.** (bioRxiv 2026): con mucha poda, las redes con cableado de conectoma aguantan mejor que las redes al azar la pérdida de neuronas y los cambios de hiperparámetros.
- [CONCLUSION] **La lección es la tuya.**
  - Contra un par justo, la mosca empata en acierto; donde puede ganar es en robustez, en datos y en costo.
  - Nosotros medimos casi sólo acierto, y dentro de lo entrenado.
  - La única pista propia va en esa dirección: en la 015, con LPLC4 muda, la mosca aguanta más que su regla (0,8030 contra 0,7680, descriptivo).

## 6. Dónde se aplica cada paper, y contra qué par tiene que ganar (opinión)

- **Paper 1 (cómo viaja la señal):**
  - Qué es: la señal de cada sentido se propaga con estructura propia frente a nulos de grado y de ubicación. La reciprocidad queda unas 20 veces sobre el nulo, la vía gustativa a dos saltos está empobrecida (10 contra 101,6 esperadas) y la v2 describe aislamiento entre modalidades.
  - Dónde aplica:
    - análisis de redes con nulos que conservan grado y zona (fraude, energía, logística), como servicio;
    - el diseño de fusión de sensores.
  - Par que tiene que vencer:
    - en ciencia, los grafos al azar con los mismos grados y la misma ubicación (hecho);
    - en ingeniería, la fusión temprana o tardía de una red multimodal (NO MEDIDO).
- **Paper 2 (si el cableado sirve):**
  - Qué es: el cableado exacto es necesario para sus reflejos, alcanza a su plano, y sus 6 descendentes comprimen la tarea.
  - Dónde aplica:
    - reflejos chicos para drones, robots y asistencia;
    - redes ralas y robustas para el borde;
    - el método del banco sellado, para evaluar modelos.
  - Par que tiene que vencer: las tres primeras piezas de la tabla, en datos, robustez y costo. Ahí está hoy el hueco.
- **Paper 3 (quién manda las salidas):**
  - Qué es: las descendentes son el bus de comandos (mandan a descendentes, motoras, cuello y antena), y lo óptico casi no llega directo a ellas.
  - Dónde aplica:
    - la arquitectura de control de robots: pocos canales de mando entre la percepción y los motores;
    - el análisis de cuellos de botella de control en otras redes.
  - Par que tiene que vencer: un controlador jerárquico contra uno plano, con los mismos sensores (NO MEDIDO). Es estructural: su ciencia no depende de eso, su aplicación sí.
- **La mosca entera** (capítulo del Paper 2):
  - Aplica a elegir la neurona de un simulador de conectoma: con tasa sale el mapa, y para la decisión motora hacen falta espigas.
  - También sirve como filtro barato de hipótesis.
  - Pares: la propagación sin dinámica (hecho, gana) y el modelo de Shiu (hecho).
- **La línea de producto** (HC-2, HC-3, HC-6): vale la misma regla. Cada hipótesis tiene que ganarle a su par artificial al mismo presupuesto, no sólo a su barajado.

## 7. Corrección a la 057

- [CORRECCION] Donde la 057 dice «no es un cerebro mejor que lo clásico» y «para un producto conviene lo clásico», lo medido es sólo esto: en acierto, dentro de lo entrenado, un lector clásico con 2.400 ensayos etiquetados y unos 135.000 pesos le gana a la mosca por 5 puntos.
- Si conviene para un producto depende de datos, robustez y costo, y eso está NO MEDIDO.
- Lo corregí en el Doc de la 057, con una nota arriba, y en su entrada del CONTEXTO. El archivo de la 057 en git no se edita: es append-only.

## 8. Propuesta: H_PARES, sin sellar

Orden por costo y por lo que decide:

1. **H_PARES_DATOS.** Es la más barata, y la que prueba tu idea de «funciona el primer día».
   - **Curva de datos en R2:** acierto con 0, 6, 12, 24, 48, 96, 192, 384, 768 y 2.400 ensayos etiquetados de entrenamiento.
   - **Brazos:**
     - las líneas de la mosca, con 0 ejemplos de acción: umbrales con ensayos sin evento y una τ fija que nadie eligió, como en H_TAU_LIBRE;
     - la mosca con L (240 rasgos);
     - el ridge crudo (22.560 rasgos);
     - L sobre embudos artificiales de 240 rasgos: PCA de las entradas crudas y una proyección aleatoria.
   - **Falsador:** si el ridge crudo o un embudo artificial alcanza a la mosca con la misma cantidad de ensayos en toda la curva, la mosca no aporta eficiencia de datos y su embudo no es especial.
   - **Costo:** casi todo reusa las trazas de H_LECTOR, y las proyecciones son baratas. Corre en Actions.
2. **H_PARES_ROBUSTO.** Los mismos modelos, sin reentrenar, con un sensor apagado (LPLC4 o un lado), ruido fuera de lo entrenado y un 10 % de interneuronas muertas.
   - **Falsador:** si la mosca no cae menos que el ridge y que los embudos artificiales, no hay ventaja de robustez.
3. **H_PARES_RESERVORIO.** R2 contra reservorios artificiales con las mismas 33.489 neuronas, 4.031.897 aristas y el mismo radio (Erdős-Rényi y mundo pequeño), con el mismo L y la misma τ, en las dos métricas anteriores.
   - **Costo:** es la más cara. Cada reservorio se simula como un nulo de H_LECTOR, unos 10 minutos por red y celda en Actions.
- Después vienen el plano contra una regla aprendida rala y el módulo de reuso contra módulos compartidos, que piden diseño.
- [opinión] Arrancaría por la 1. Es barata, usa lo que ya está medido y contesta directo si lo que querés tomar de la mosca (competencia con pocos datos y un embudo chico) le gana a su par artificial.

## Herramientas y máquina

- **Conector GitHub:** commits de `main` (nada nuevo desde 48dc5f8), y los sellos de H_RIVAL (`titan/rival-2026-10-15`) y H_LECTOR (`titan/lector-2026-10-15`).
- **brain-env:**
  - clon de `main`;
  - grep de las respuestas 2026-10-11-008, 011 y 2026-10-13-013;
  - lectura de `umbrales()` y `lineas()` en `tarea_mosca.py` (md5 40d64e074d9163753439307c5be4ac5e, el pin de H_RIVAL);
  - prueba del parche en una copia.
- **Web:** búsqueda y lectura de FLYNN (arXiv 2607.00025) y Dhiman (arXiv 2604.04033); resúmenes de Costi 2025 y McAllister 2026.
- **ClickUp:** nota de corrección en el Doc de la 057.
- **Actions y Kaggle:** nada.

## Evidencia

- **Sello de H_RIVAL**, Limitación 3, verbatim: «W elige entre 10 candidatas solo tau y ajusta 6 umbrales; los rivales ajustan miles de pesos. Es la comparacion pedida: el presupuesto de eleccion es el mismo, la capacidad no.»
- **Sello de H_RIVAL**, entrada de los rivales: «X = drive[:, :, chan] + s * Z, 40 pasos por 564 entradas, 22.560 rasgos por ensayo: lo mismo que recibe W. El estado (posada o en vuelo) es conocido, como en W y en la regla: un modelo por estado con las clases de `tm.CLASES` (vuelo 0, 2, 3, 4; posada 0, 1).» Entrenamiento: `tm.generar(2400, 1)`.
- **Sello de H_LECTOR**, Limitación 3: «L lee 240 rasgos y el RIDGE crudo 22.560: el presupuesto de eleccion es el mismo (10 lambdas), la capacidad no. Si CERCA sale SOSTENIDA, es con 94 veces menos rasgos.»
- **`tarea_mosca.py`**, líneas 236 a 241 (md5 40d64e074d9163753439307c5be4ac5e): el umbral de cada línea sale sólo de los ensayos con `y == 0`, los que no tienen evento.

```
def umbrales(S, y, vuelo):
    th = np.zeros(6)
    for k in range(6):
        m = (y == 0) & (vuelo == COMPITE_VUELO[k])
        th[k] = np.quantile(S[m].max(axis=1)[:, k], 1.0 - FA)
    return th
```

- **2026-10-11-008**, línea 9: «en el reservorio recurrente el cableado de la mosca empata con su shuffle en 4 de 4 tareas, con τ fija y con τ líquida. Tampoco le gana a un reservorio de ruido (0 de 4). En estas cuatro tareas paga la sparsity, no la mosca.»
- **FLYNN**, resumen: «achieving performance comparable to modern hand-crafted networks of similar parameter counts. Crucially, FLYNN exhibits superior resistance to out-of-distribution (OOD) data and tolerance to sensory loss without further training.»
- **Dhiman**, resumen: «previously reported topology advantages in connectome-constrained neural networks can arise from initialization and null-model confounds, and largely disappear under fair from-scratch initialization and degree-preserving controls.»
- **Cuenta del presupuesto:** 22.560 × (4 + 2) = 135.360 pesos del ridge; MLP de un estado en vuelo, 22.560 × 32 + 32 + 32 × 4 + 4 = 722.084; L, 240 × 6 = 1.440.

- **Parche del CONTEXTO**, probado en una copia del de `main` (48dc5f8) en brain-env, con el mismo md5 del script en los dos lados (fad30bba2127c121a25eedf5d1877bed):
  - primera pasada: `md5 antes 3ebec5a8dad3c2ae537e6d16037e651c`, cinco anclas con `ANCLA apariciones=1`, `md5 despues 1173ec1f5a56b7de7afdd39f879e2ee2`, `PARCHE OK`;
  - segunda pasada: `ANCLA apariciones=0` y `ABORTA: ancla no unica`, con el md5 sin cambios (1173ec1f);
  - incluye las dos correcciones a la entrada de la 057 y el pendiente de H_PARES en la lista de decisiones.

## Fuentes

- Sellos: `tools/rival/SELLO-RIVAL.md` (`titan/rival-2026-10-15`) y `tools/lector/SELLO-LECTOR.md` (`titan/lector-2026-10-15`).
- Respuestas:
  - 2026-10-11-008 (el reservorio), 011 (el escape difícil), 013 y 014 (la líquida);
  - 2026-10-12-003 y 004 (DBC3 contra LSTM), 015 (la tarea de la mosca);
  - 2026-10-13-013 (Costi, Suárez y Lechner);
  - 2026-10-14-009 (aplicaciones por paper), 034 (H_RIVAL), 038 (H_LECTOR), 049 (PROX) y 057 (la que se corrige).
- Literatura:
  - Wang y Chen, «FLYNN: Robust Neural Network for Robot Navigation using Fly Brain Topology», arXiv 2607.00025;
  - Dhiman, «Topological Sensitivity in Connectome-Constrained Neural Networks», arXiv 2604.04033;
  - Costi et al., Biomimetics 10(5):341, 2025, doi 10.3390/biomimetics10050341;
  - McAllister, Houghton, Wade y O'Donnell, bioRxiv 2026.03.30.715411.

## Archivos

| Archivo | Dónde | md5 |
|---|---|---|
| `docs/agents/respuestas/2026-10-14-058-tenes-razon-comparamos-contra-un-techo-no-contra-sus-pares.md` | `main` | este archivo |
| `tools/contexto/actualizar_contexto_2026-10-14-058.py` | `main` | fad30bba2127c121a25eedf5d1877bed |
| `.github/workflows/contexto-2026-10-14-058.yml` | `main`, se borra solo al aplicar | 2b87a33ff0c23e3e5b6a0bd9af541795 |

## NO MEDIDO

- Todas las comparaciones de la sección 4 marcadas NO MEDIDO, y H_PARES entero.
- FLYNN, Dhiman, Costi y McAllister: leídos en resumen (de FLYNN, también la introducción y los métodos). Sus resultados no se reprodujeron.
- El 135.360 es una cuenta sobre lo que dice el sello, no un conteo sobre el código corrido.
- El costo de cualquier pieza en placa: bytes, energía y latencia.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| H_RIVAL comparó contra un techo, no contra un par | sello de H_RIVAL: entradas, entrenamiento y Limitación 3 | Sí: si el ridge hubiera tenido el presupuesto de la mosca, la frase caía | medido (lectura del sello) |
| Los umbrales de la mosca no usan ejemplos de acción | `umbrales()` de `tarea_mosca.py`, con el pin de H_RIVAL | Sí: si usara ensayos con `y` distinto de 0, caía | medido (lectura de código) |
| La τ de W sí usó etiquetas | CONTEXTO: H_TAU elige τ por validación cruzada en el entrenamiento | Sí | medido (copia) |
| 135.360 pesos del ridge | cuenta: 22.560 × (4 + 2) | Sí, si el modelo no fuera por estado | cuenta |
| Inventario de pares ya medidos | CONTEXTO y respuestas 008, 011, 003, 004, 013, 014 y 049 | Sí | medido (copia) |
| Lo que dice la literatura | resúmenes, y métodos de FLYNN | Sí, contra el texto | leído, no reproducido |
| Dónde se aplica cada paper | ninguno | No | opinión |
| El parche del CONTEXTO aplica | copia del de `main` en brain-env; la segunda pasada aborta | Sí | medido |

--- METODO PROMETEO ---
Rol: análisis y diseño (chica). Delicado: no.
Máquinas: conector GitHub y brain-env (lectura y parche), web (literatura), ClickUp (Doc de la 057), sandbox de ClickUp (redacción). Actions y Kaggle: nada.
Archivo: `docs/agents/respuestas/2026-10-14-058-tenes-razon-comparamos-contra-un-techo-no-contra-sus-pares.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23817
