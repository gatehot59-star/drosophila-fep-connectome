# En criollo: qué hice y hacia dónde vamos

## La pregunta de fondo
Abraham no está intentando demostrar que la mosca sea una red neuronal entrenada como un modelo grande. La hipótesis es otra: el cerebro de la mosca podría hacer gran parte del trabajo con el cableado ya construido, signos excitatorios/inhibitorios, rutas topológicas y dinámicas fijas; un módulo pequeño podría ajustar o aprender lo necesario.

La pregunta H4 es más específica: **¿la red activa y desactiva rutas diferentes según la acción que el animal termina haciendo, incluso cuando el contexto o la situación sensorial es comparable?** No alcanza con ponerle a una población el nombre “escape” o “grooming”. Hay que observar conducta real, contexto real y acción alternativa.

## Qué hice primero
Releí el proyecto por hipótesis, no por archivo. Eso obligó a separar tres cosas que antes se mezclaban:

1. Lo que el conectoma realmente demuestra.
2. Lo que el motor SparseLTC/DualBrain puede hacer como instrumento.
3. Lo que todavía era una intuición biológica sin un experimento capaz de hacerla fallar.

También separé el trabajo propio de los precedentes externos. SparseLTC, DBC3/DualBrain, los nulls y la auditoría son trabajo de Abraham. FlyVis, Shiu, Lin, Bates y otros son referencias externas, no el origen de esos resultados.

## Qué quedó refutado o corregido
El primer falsador H4 usó tres poblaciones anotadas del conectoma: escape, grooming y feeding. El grafo era el real, con 138.639 neuronas y 15.091.983 aristas, y se propagó la dinámica en Brain-env. Las tres entradas produjeron prácticamente el mismo perfil de salida: similitudes cosine entre `0,999786` y `0,999845`. Resultado: **la H4 débil queda refutada**. Esas etiquetas anotadas, por sí solas, no seleccionan rutas funcionales distintas.

Eso no refuta la H4 fuerte. Sería como pintar tres botones con nombres distintos y concluir que el aparato no distingue decisiones: faltaba observar una situación donde el mismo contexto pudiera terminar en dos acciones.

La auditoría también corrigió otros excesos: la analogía del 96% fijo todavía no está medida sobre SparseLTC; algunos ceros del conectoma eran geometría anatómica y no prohibiciones; varios claims de novedad tuvieron que angostarse contra prior art. Esto no destruye el proyecto: limpia qué se puede afirmar y qué no.

## Qué dataset busqué
Busqué datos donde coincidieran cuatro piezas: conducta, contexto, actividad neural y posibilidad de mapear algo a una identidad conectómica.

- **Dallmann**: tiene calcio, walking, grooming, movimiento pasivo/activo, plataforma y treadmill. Está muy bien para contexto y acción, pero el acceso automatizado de Dryad exige permisos adicionales.
- **MC2P**: tiene dos fotones, video, pose 2D/3D y acciones de ocho moscas. El enlace público que figura en el repositorio devuelve 404, así que no lo traté como adquirido.
- **Aymanns**: tiene actividad de neuronas descendentes, conducta y registros sincronizados. Este fue el camino que sí pude abrir y ejecutar.

## Qué medí con Aymanns
Descargué ocho trials del mismo fly/genotipo desde Harvard Dataverse. Cada trial tiene etiquetas de conducta y dos trazas DFF. Primero hice un pretest simple: remuestreé 1.067 frames neurales a 7.440 frames conductuales. La ventaja sobre etiquetas barajadas fue chica, entre `0,0014` y `0,0248` de accuracy. Eso indicó que había señal útil, pero no era todavía una prueba limpia.

Después hice lo correcto: leí el código oficial `utils2p` de los autores y reproduje su idea de sincronización ThorSync. En el trial 007 medí 7.469 pulsos de cámara, 7.440 frames conductuales, 3.201 pasos de frame counter y 1.067 frames de dos fotones. Usé `steps_per_frame=3`, tiempos a 30 kHz e interpolación de DFF sobre los frames exactos de cámara.

Con esa alineación exacta, la accuracy fue `0,68607` contra `0,66892` del shuffle, una diferencia de `0,01716`. Las similitudes entre centroides de acciones quedaron entre `0,97437` y `0,99998`: hay variación entre etiquetas, pero no una separación universal de rutas.

## El descubrimiento metodológico importante
También alineé el contexto CO2. En ese trial hubo 7.215 frames sin CO2 y 225 con CO2. Pero durante CO2 solo aparecieron dos acciones: `resting=85` y `walking=140`. No hubo grooming alternativo dentro del mismo contexto.

Por eso el resultado correcto es: **el instrumento ya funciona mejor, pero H4 fuerte sigue NO MEDIDA**. No se puede decir apoyada ni refutada. El experimento todavía no tiene el contraste que la hipótesis exige.

## Hacia dónde vamos ahora
El siguiente paso no es inventar otra etiqueta ni seguir puliendo la misma corrida. Es buscar entre los trials y contextos un caso que cumpla el gate:

- mismo fly o grupo comparable;
- mismo contexto o estímulo;
- al menos dos acciones alternativas;
- actividad neural sincronizada;
- suficientes frames por acción;
- separación por trial, no por frames mezclados;
- mapping anatómico a FlyWire cuando exista;
- comparación del conectoma real contra un null apropiado;
- silenciamiento de rutas o módulos para probar causalidad.

Si ese gate no se cumple, el veredicto sigue siendo **NO MEDIDA**. Si se cumple y las rutas reales cambian con la acción mientras el null no lo hace, H4 gana apoyo. Si no cambian, H4 fuerte cae. Si el resultado depende solo de la etiqueta o del desbalance de clases, se descarta como instrumento malo.

## En una frase
La primera versión de H4 murió porque usaba nombres de poblaciones como sustituto de decisiones conductuales. Ahora ya tenemos datos reales, sincronización real y un falsador reproducible; falta encontrar la situación experimental correcta donde la mosca pueda elegir dos acciones bajo el mismo contexto.

## Archivos y recibos
- Runner H4 débil: `tools/h4_actions.py`.
- Runner neural: `tools/h4_neural_behavior.py`.
- Runner ThorSync: `tools/h4_neural_behavior_sync.py`, commit `657fcbcbbd876fff560af65bc82a70a93877bece`.
- Recibo H4 Brain-env: [2026-10-02-066-poll-H4-brain-env](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/docs/agents/respuestas/2026-10-02-066-poll-H4-brain-env.md).
- Recibo pretest neural: [2026-10-02-067-pretest-H4-neural-Aymanns](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/docs/agents/respuestas/2026-10-02-067-pretest-H4-neural-Aymanns.md).
- Recibo ThorSync exacto: [2026-10-02-068-H4-ThorSync-exacto](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/titan/auditoria-hipotesis-2026-10-01/docs/agents/respuestas/2026-10-02-068-H4-ThorSync-exacto.md).

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (explicacion y estado cientifico)
N/A declarados: deployment, security, CI no aplican
Review externo: no pedido
Instrumento: Git vivo, Brain-env, APIs públicas y fuente utils2p; recibos citados arriba
NO MEDIDO: H4 fuerte, mapping FlyWire, null topológico sobre actividad observada y causalidad completa
