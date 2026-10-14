# 2026-10-13-018 · Dos moscas: lo que se repite entre animales son los reflejos, y ahí está la fábrica de partes

## Veredicto

- **[LITERATURA] No son dos, son tres.**
  - FlyWire: el cerebro de una hembra, el que usa el banco.
  - BANC: cerebro y cordón de otra hembra, unas 160.000 neuronas (Bates et al., Nature 2026).
  - MaleCNS: cerebro y cordón de un macho, 166.691 neuronas (Berg et al., bioRxiv 2025; la versión 1.0 salió el 08-06-2026).
  - Además están hemibrain, parcial, y los cordones MANC y FANC.
- **[LITERATURA] El patrón que intuís existe, y en estructura ya se midió.**
  - Schlegel et al. (Nature 2024) compararon FlyWire con hemibrain, dos moscas distintas. Encontraron estereotipia amplia: las conexiones de más de 10 sinapsis, o de más del 1 % de la entrada de la neurona, se conservan; los pesos finos varían.
  - Berg et al. (2025) compararon macho y hembra: la periferia sensorial y motora es casi igual (7.205 tipos iguales contra 114 dimórficos). Lo distinto está en los centros superiores.
- **[CONCLUSIÓN] Eso te da la razón en lo central.** Lo que se repite entre moscas es justo la capa de reflejos, de sensor a motor: lo que la evolución fijó, y lo que tiene sentido extraer como pieza.
- **[CONCLUSIÓN] Lo que no encontré hecho:** probar en un banco funcional si esa parte conservada carga la función. Es una búsqueda acotada, NO MEDIDO hasta una revisión sistemática.
- **[CONCLUSIÓN, opinión] No reemplaza a los LLM.**
  - En autos y drones el LLM no maneja el lazo rápido: eso lo hacen redes de percepción y controladores. La pieza de mosca compite ahí: reflejos de pocos KB, de milisegundos, sin entrenar. **El LLM piensa, la mosca esquiva.**
  - En prótesis, visión y audición humanas sirve como módulo de procesamiento, por ejemplo un aviso de choque inminente para una persona ciega. No reemplaza la visión humana.
- **[MEDIDO, nuestro] Una advertencia de nuestros propios datos:** la regla a mano rinde casi lo mismo que el cableado y es mucho más barata. La fábrica tiene que exportar lo que gane en el banco, sea el cableado o la regla.
- **[CONCLUSIÓN] El paper.** La v2 del Paper 1 está lista para depositar: no se toca. Las tres moscas son el Paper 2, y es mejor paper.

## Pedido

21:36: «HAY ALGO Q TU NO VES, SI TENEMOS DOS CONECTOMAS DE MOSCA POR MAS QUE SEAN DE MOSCAS DISTINTAS. PODEMOS ENCONTRAR UN PATRON, Y MEJORAR NUESTRO PAPER O GENERAR UNO NUEVO Y DE PASO LOGRA LO Q MI INTUICION DICTA. EMULAR CERBRO DE MOSCAS PARA APLICACIONES DE ROBOTICA O EN DIFERENTES CASOS, TENER UNA FABRICA DE PARTES DE CERBROS DE MOSCAS. PARA DESCARGAR Y QUE SEAN COMPLEMNTOS EN PROCESOS , COMO PROTESIS. LECTURAS DE SENSORES, ETC. EN POCAS PALABRAS REEMPLAZAR A LOS LLM QUE HOY EN DIA SE ENCUNTRAN UTILZADOS EN AUTOS AUTRONOMS , SISTEMAS ESPACIALES. DRONES, ETC. PROTESIS, SISTEMA DE AUDICION Y VISION PARA PERSONAS. ETC»

## Herramientas y máquina

- **Web:** tres búsquedas (Schlegel 2024, MaleCNS 2025, detectores de insecto en robots).
- **Sin máquinas, sin cuota.** No se corrió nada nuevo; el factorial 4 sigue en Kaggle.

## Qué se midió

Nada nuevo: es una síntesis con literatura verificada. Las afirmaciones sobre nuestros datos vienen del CONTEXTO (respuestas 2026-10-13-011 y 2026-10-13-015).

## La fábrica, en limpio

- **Qué es una pieza:**
  - el circuito conservado entre moscas;
  - su regla destilada;
  - las pruebas del banco (contra su diseño y contra sus barajados);
  - tamaño y latencia medidos, y un export a C para un microcontrolador (el taller tiene la cadena del ESP32).
- **Primera candidata:** el escape por *looming* (LC4 y LPLC2 hacia las descendentes), el motivo que ya medimos.
- **[LITERATURA] No es la primera vez que un reflejo de insecto va a un robot.**
  - Zhao et al. (iScience 2023) hicieron un detector de *looming* inspirado en la mosca para esquivar choques.
  - Fu et al. (Artificial Life 2019) revisan los detectores de movimiento de langosta, mosca y libélula en robots y vehículos.
  - Lo distinto sería que la pieza sale del conectoma, está probada contra su diseño y contra sus barajados, y es la parte que se conserva entre animales.

## Plan del Paper 2, con falsador

- **H_CONSENSO:** el núcleo conservado rinde como el cableado entero (dentro de 1 punto) con una fracción de las aristas. El núcleo son las aristas presentes en las moscas, o la regla de Schlegel como aproximación. **Falsador:** pierde más de 1 punto, o no le gana a sus barajados.
- **H_OTRA_MOSCA:** el banco en BANC y en MaleCNS repite lo de FlyWire y le gana a sus barajados. **Falsador:** en otra mosca no les gana.
- **Pasos:**
  1. Aproximación sin datos nuevos: el núcleo de Schlegel (10 sinapsis o más, o más del 1 % de la entrada) dentro de FlyWire, contra R2 entero. Se sella antes de correr y corre gratis en Actions.
  2. Acceso a los datos de BANC y MaleCNS, y cuántas de nuestras 564 entradas y 6 descendentes tienen pareja.
  3. El sujeto en cada mosca y el consenso.
  4. Compilar la pieza ganadora a C y medir tamaño y latencia en el ESP32.

## Evidencia cruda

- Schlegel et al., «Whole-brain annotation and multi-connectome cell typing of Drosophila», Nature (2024), doi 10.1038/s41586-024-07686-5. Del resumen: «revealed broad stereotypy and occasional variability in neuron count and connectivity». Del preprint (doi 10.1101/2023.06.27.546055): «connections stronger than 10 unitary synapses or providing >1% of the input to a target cell are highly conserved».
- Berg et al., «Sexual dimorphism in the complete connectome of the Drosophila male central nervous system», bioRxiv (2025), doi 10.1101/2025.10.09.680999. Del resumen: «166,691 neurons spanning the brain and nerve cord», «7,205 isomorphic, 114 dimorphic, 262 male-specific and 69 female-specific types» y «the sensory and motor periphery are largely isomorphic». En male-cns.janelia.org: «2026-06-08 - MaleCNS v1.0 released!».
- Bates et al., Nature (2026), doi 10.1038/s41586-026-10735-w (BANC, ver la 2026-10-13-017).
- Zhao et al., «A fly inspired solution to looming detection for collision avoidance», iScience (2023), doi 10.1016/j.isci.2023.106337.
- Fu, Wang, Hu y Yue, «Towards Computational Models and Applications of Insect Visual Systems for Motion Perception», Artificial Life 25(3), 2019.

## Archivos

- Esta respuesta. El CONTEXTO no cambia de estado: el factorial 4 sigue corriendo y sin leer.

## NO MEDIDO

- Que la parte conservada cargue la función en el banco: es la hipótesis.
- El acceso a los datos de BANC y MaleCNS desde nuestras máquinas, y cuántas de nuestras neuronas tienen pareja.
- Que nadie haya probado la parte conservada en un banco funcional: la búsqueda fue acotada.
- Que una pieza de mosca le gane a un controlador o detector clásico en un robot real.
- Tamaño y latencia de una pieza compilada.

## Antes de firmar

| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| hay tres conectomas de moscas distintas | artículos y página de MaleCNS | es literatura, no medición nuestra |
| lo conservado es la periferia sensorial-motora | Berg 2025 (macho contra hembra) y Schlegel 2024 (dos hembras) | sí: si los centros superiores fueran lo conservado |
| no reemplaza a los LLM | opinión sobre dónde trabaja cada uno | no es medición; la pieza contra un controlador real está NO MEDIDA |
| la regla rinde casi como el cableado | factoriales 2 y 3 | ya pudo dar rojo y no lo dio |

```
--- METODO PROMETEO ---
Accion delicada: no (síntesis con referencias; nada corrido)
Maquina: web (3 búsquedas)
Artefactos: docs/agents/respuestas/2026-10-13-018-dos-moscas-lo-conservado-son-los-reflejos-fabrica-de-partes.md + Doc de ClickUp 2026-10-13-018
```
