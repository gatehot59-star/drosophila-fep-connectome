# Auditoría independiente del proyecto de este chat: H4

**Fecha:** 2026-10-02 14:xx ART  
**Sujeto auditado:** rama `titan/auditoria-hipotesis-2026-10-01`, HEAD `6112bdd25daf29d68e83d96eecd5f802d0fe8920`  
**Referencia pública:** `main` estaba en `08b3b01bc0a6c678ae09fe6adeabadfe6cd94b63` al auditar.

## Veredicto ejecutivo

**El proyecto tiene una línea científica válida, pero la última cadena H4 no está lista para sostener un claim biológico.** El hallazgo decisivo del propio trabajo es correcto: los análisis cross-animal y temporal quedaron invalidados porque las features unieron relojes distintos por el entero `Frame`. No hay que rescatar esos números; hay que rehacer la medición con el asset sincronizado y con guards que impidan repetir el error.

La H4 débil sobre poblaciones anotadas queda refutada en su alcance estrecho. La H4 fuerte, acción alternativa bajo contexto comparable y rutas activadas/desactivadas, sigue **NO MEDIDA**.

## Hallazgos

### R1 · CONFIRMADO: la auditoría de features encontró el error fatal

El recibo `2026-10-02-075-auditoria-features-H4.md` registra conducta de 54.000 frames frente a `roi_dFF_2p` de 8.767/8.768 frames y DFF de 0 a ~539,65 s. Los runners anteriores hacen `merge` por `Frame` en `h4_cross_animal.py` y `h4_temporal_stability.py`; por tanto, el mismo número entero no representa el mismo instante. La retractación biológica de los resultados cross-animal y temporal es correcta.

Evidencia: [auditoría de features](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f802d0fe8920/docs/agents/respuestas/2026-10-02-075-auditoria-features-H4.md), [cross-animal](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f802d0fe8920/tools/h4_cross_animal.py), [temporal](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f802d0fe8920/tools/h4_temporal_stability.py).

### R2 · CONFIRMADO: los números invalidados no deben reaparecer como biología

Los recibos `073` y `074` sí presentan números y hashes, pero sus instrumentos medían el emparejamiento incorrecto. Por eso `0,1816 vs 0,2019` y los deltas temporales no son resultados biológicos: son diagnósticos históricos del pipeline. El recibo `075` corrige el estado y no intenta salvarlos.

Evidencia: [recibo cross-animal](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f802d0fe8920/docs/agents/respuestas/2026-10-02-073-validacion-cross-animal-H4.md), [recibo temporal](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f802d0fe8920/docs/agents/respuestas/2026-10-02-074-estabilidad-temporal-intra-animal.md).

### R3 · NO MEDIDO: la supuesta equivalencia con el loader oficial no está demostrada

`h4_neural_behavior_all.py` implementa una alineación manual ThorSync-equivalente y usa archivos DFF por trial, pero no hay una comparación de salida contra el loader oficial `roi_dFF.pkl`, ni un test de referencia que fuerce diferencias a rojo. El recibo `072` puede sostener que hubo una corrida reproducible del runner, no que la equivalencia oficial quedó validada.

Evidencia: [runner de ocho trials](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f802d0fe8920/tools/h4_neural_behavior_all.py), [recibo 072](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f8020/does-not-exist).

### R4 · ROJO: el intento de corrección todavía no es una medición válida

`h4_timealigned_features.py` interpola por `Time`, pero sigue usando el asset `roi_dFF_2p` y fija el reloj conductual como `Frame / 100.0`. No produce un resultado concluyente y no demuestra que el archivo neural sea el asset sincronizado oficial. El siguiente resultado no puede publicarse como “corregido” hasta pasar un guard de identidad, trial, animal, rango temporal, monotonía y pérdida de frames.

Evidencia: [runner time-aligned](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f802d0fe8920/tools/h4_timealigned_features.py), [recepción y límites en 075](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f8020/docs/agents/respuestas/2026-10-02-075-auditoria-features-H4.md).

### R5 · ROJO DE DISEÑO: las features no pueden probar rutas anatómicas

Las nueve estadísticas por frame eliminan identidad ROI, signo individual, fase, posición y módulo. Son válidas como control de señal global, no como proxy de rutas SparseLTC ni como base de silenciamiento causal. Aun con el reloj arreglado, una clasificación positiva solo demostraría señal decodificable, no activación/desactivación de una ruta.

### R6 · CONFIRMADO: la H4 fuerte sigue abierta, no refutada

Los ocho trials Aymanns aportan actividad y acciones alternativas descriptivas. Pero no se midió todavía el mismo estímulo/contexto con acciones alternativas, mapping ROI→FlyWire o cell type, propagación SparseLTC sobre el subgrafo real, null anatómico pareado ni silenciamiento cruzado. El estado correcto es **NO MEDIDA**.

### R7 · ROJO DE ESTADO: el contexto vivo quedó vencido

`CONTEXTO-drosophila-fep.md` declara última actualización del 25-ago, rama `titan/twohop-nulls` y estado hasta la resp 075, mientras el trabajo H4 vive en otra rama y llega a la resp 075 con commits de octubre. El protocolo exige actualizar el contexto cuando cambia el estado. Hoy no es una fuente confiable para decidir qué está medido.

Evidencia: [contexto vivo](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/6112bdd25daf29d68e83d96eecd5f802d0fe8920/docs/agents/CONTEXTO-drosophila-fep.md), [HEAD H4](https://github.com/gatehot59-star/drosophila-fep-connectome/commits/titan/auditoria-hipotesis-2026-10-01).

### R8 · ROJO DE ENTREGA: el trabajo H4 no está en main ni tiene PR abierto

La rama H4 existe, pero `main` quedó en `08b3b01` y los PR abiertos enumerados son #1, #2 y #3, sin la rama H4 actual. Los resultados pueden ser auditados por SHA, pero no forman parte de la rama pública principal ni de un release reproducible.

## Qué no se midió y era decisivo

1. Equivalencia bit a bit o tolerancia explícita entre loader oficial y runner manual.
2. Guard que rechace merges de relojes incompatibles.
3. Mapping anatómico común de ROIs y correspondencia con FlyWire v783.
4. H4 fuerte con contexto/estímulo compartido y acción alternativa.
5. Causalidad por silenciamiento de rutas reales.
6. Revisión externa del conjunto de runners H4.

## Orden obligatorio

Primero: loader oficial y `alignment_guard`, con prueba negativa que falle. Segundo: repetir cross-animal y temporal por bouts/trials, con nulls por bloques. Tercero: preservar identidad anatómica y mapear ROIs. Recién después: SparseLTC sobre subgrafo real, null anatómico y silenciamientos. No correr más clasificadores sobre el reloj viejo.

## Scorecard de esta auditoría

| Criterio | Resultado | Evidencia |
|---|---:|---|
| Completitud | 11/15 | Se auditó la cadena H4 completa y el estado de ramas; falta inspección de los datos oficiales íntegros |
| Razonamiento | 10/10 | Se separan ejecución, validez temporal, decodificación y causalidad |
| Documentación | 9/10 | Cada rojo apunta a código/recibo; el contexto vivo está vencido |
| Proceso QA | 4/5 | Auditoría contra repo y máquina; no hubo review externo del pipeline |
| **Total** | **34/40 = 85/100** | **NO APROBADA** |

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: 34/40 -> 85/100
N/A declarados: seguridad, deployment y producto no aplican a una auditoría científica del pipeline; no se puntúan como cero
Review externo: no pedido; queda deuda K-02, no aprobación
Instrumento: GitHub API para rama, commits, archivos y PRs; gateway build.run para estado del checkout, buzón SQLite y disponibilidad del taller; lectura directa de runners y recibos
Evidencia cruda: SHAs, URLs y salidas registradas en este archivo
NO MEDIDO: loader oficial completo, rerun corregido, mapping anatómico, causalidad, review externo y equivalencia manual-oficial
