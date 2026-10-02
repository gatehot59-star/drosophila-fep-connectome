# Comparación H4 vs hallazgos anatómicos que sobrevivieron

## Veredicto corto
H4 y los hallazgos anatómicos no se contradicen. La anatomía demuestra que el conectoma **restringe y sesga** por dónde puede circular la señal; H4 pregunta si, encima de ese armazón fijo, la red **elige dinámicamente** rutas distintas cuando el animal enfrenta el mismo contexto y termina en acciones alternativas. La primera parte está medida; la segunda sigue NO MEDIDA.

## Lo anatómico que sobrevivió
Sobreviven, con el alcance correcto:

- La topología post-estímulo produce selectividad temporal frente a nulls que conservan signo y/o Dale: `sel_post=4,3287` contra `1,1896 ± 0,0173`, `z=181,4`, `0/40`; el efecto no es selectividad de pico.
- `LC6→GF=0` contra null anatómico que predice `17,2 ± 3,1`, `z=-5,6`: este cero sí se comporta como prohibición estructural, no como simple co-localización.
- La arquitectura del centro de aprendizaje está sesgada: `KC→MBON=7,81×`, `DAN→KC=8,71×` y `KC→KC=7,26×` frente a CP, todos `0/40`; DAN→KC es 23,5 veces DAN→MBON.
- El módulo plástico es pequeño en conteo: 4,045% de neuronas, 0,41% de conexiones y 0,47% de sinapsis. Eso describe su enclosure anatómico, no demuestra que el resto no aprenda.
- El cero sensorial→KC y varias asimetrías de acceso sobreviven solo como resultados contra los nulls y definiciones que realmente se midieron. Los resultados de dos saltos contra grado no pueden seguir presentándose como jerarquía biológica: el null anatómico invirtió tres signos y colapsó el spread de 323× a 2,4×.

## Qué sí dice H4 a la anatomía
La anatomía da el **hardware de las rutas**: hay puertas, cuellos de botella, enriquecimientos, depleciones y conexiones prohibidas. Eso vuelve plausible que un sistema fijo pueda ofrecer un repertorio de rutas y que un estado interno pequeño module su uso.

Pero no prueba el **selector contextual**. Un cableado enriquecido puede ser compartido por escape, grooming y feeding. Eso es exactamente lo que ocurrió en el falsador débil: con el grafo real, los perfiles normalizados de las tres poblaciones anotadas tuvieron cosine `0,999786–0,999845`; silenciar descending produjo el mayor cambio, pero casi igual en las tres acciones.

La lectura correcta es: **la anatomía establece capacidad y restricciones; H4 debe demostrar selección dependiente del estado**. H4 no puede rescatarse diciendo que las rutas existen: tiene que mostrar que la misma situación activa una combinación y desactiva otra cuando cambia la acción elegida.

## Qué NO significa la refutación débil
No significa que la mosca no tenga selección de acción ni que la topología sea irrelevante. Significa algo más preciso: las etiquetas anatómicas usadas como sustituto de acción no separaron rutas bajo esa dinámica. El pretest Aymanns con ThorSync exacto dio `accuracy=0,68607` contra `0,66892` del shuffle, pero el trial con CO2 solo tuvo `resting=85` y `walking=140`; no ofreció dos acciones alternativas dentro del mismo contexto.

## Experimento que cierra la brecha
El test decisivo debe combinar:

1. el mismo contexto/estímulo con al menos dos acciones;
2. actividad neural sincronizada y suficiente por trial;
3. ROIs mapeadas a identidades FlyWire o, como mínimo, clases anatómicas explícitas;
4. propagación SparseLTC sobre el subgrafo real;
5. null que preserve la anatomía relevante, no solo grado;
6. ablación cruzada de módulos/rutas;
7. partición por animal y trial, no frames aleatorios.

Predicción: si las rutas reales cambian por acción y el null anatómico no, H4 gana apoyo. Si no cambian, H4 fuerte cae. Si solo cambia la decodificación pero no la causalidad al silenciar rutas, hay representación de acción, no evidencia de control dinámico.

## Fuentes de trabajo
- Auditoría hipótesis: [Auditoría por hipótesis del conectoma](https://app.clickup.com/90171457413/docs/2kza6fw5-17057).
- H4 débil en Brain-env: [H4 en Brain-env: corrida finalizada y veredicto](https://app.clickup.com/90171457413/docs/2kza6fw5-17317).
- H4 con alineamiento ThorSync: [H4 fuerte: validación ThorSync exacta y gate de contexto](https://app.clickup.com/90171457413/docs/2kza6fw5-17497).
- Explicación operativa: [En criollo: qué hicimos con H4 y hacia dónde vamos](https://app.clickup.com/90171457413/docs/2kza6fw5-17517).

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (síntesis científica comparativa)
N/A declarados: deployment/security/CI no aplican; causalidad H4 y mapping FlyWire siguen NO MEDIDOS
Review externo: no pedido
Instrumento: contextos Git vivos, recibos H4 066-069 y resultados anatómicos auditados en CONTEXTO-drosophila-fep
