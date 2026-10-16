# 2026-10-14-044 · Paper 3: la pregunta ya la respondió BANC, y lo único propio que queda es el nulo

**Fecha:** 2026-10-15, 22:30 (America/Buenos_Aires) · **Método:** PROMETEO

## Pedido

Abraham, ClickKit `seguir_paper3_044`, 15-oct 22:24: seguir con el Paper 3 en lugar de pasar a DualBrain.

## Veredicto primero

- [CONCLUSIÓN] La revisión de literatura del §1 era el ítem que podía matar al paper y lo hizo como mapa. Tres trabajos ya responden la pregunta o sus cinco resultados firmes:
  1. **Bates et al., Nature 2026** (BANC, «Distributed control circuits across a brain-and-cord connectome», DOI 10.1038/s41586-026-10735-w; preprint bioRxiv 2025.07.31.667571). Su resumen, verbatim: «effector cells (motor neurons, endocrine cells and efferent neurons targeting the viscera) are primarily influenced by local sensory cells in the same body part, forming local feedback loops. These local loops are linked by long-range circuits involving ascending and descending neurons». Es nuestra pregunta, con las mismas tres salidas, en un conectoma de cerebro y cordón, con una métrica de influencia.
  2. **Braun et al., Nature 2024** («Descending networks transform command signals into population motor control», DOI 10.1038/s41586-024-07523-9): redes de descendentes que reclutan otras descendentes, comparadas contra una red barajada. Es nuestro resultado más fuerte, descendentes a descendentes.
  3. **Stürner et al., Nature 2025** («Comparative connectomics of Drosophila descending and ascending neurons», Nature 643, 158 a 172, DOI 10.1038/s41586-025-08925-z): el atlas completo de descendentes y ascendentes en FlyWire, FANC y MANC, incluida la información sensorial que recibe cada descendente.
- [CONCLUSIÓN] Lo que no encontré en esos tres (leí sus resúmenes y la introducción de BANC, no los métodos completos) es cuánto de cada participación sobrevive a nulos que fijan tamaño y región. Eso es lo único propio del Paper 3, igual que en el caso de escape (2026-10-14-043): el aporte es la expectativa, no el conteo.
- [MEDIDO, log de la 008 en la rama del PR #26] Hay una tensión que vale más que el mapa: con el nulo que preserva región, la entrada sensorial directa a las motoras del cerebro sale BAJO el azar (firme en la 007; sobrevive Benjamini-Yekutieli con p 0,01393 y no max-T, p 0,27854; `results/output_control_regioncorr_2026-10-10/run.log`). BANC dice que lo local sensorial domina. No es contradicción directa: BANC mide influencia a varios saltos e incluye el cordón; nosotros medimos la entrada directa en el cerebro solo.
- [RECOMENDACIÓN] Reencuadrar el Paper 3 como prueba con nulo regional de la afirmación de BANC sobre lazos locales, con la réplica en BANC v888 como corrida central. Si la influencia local de BANC sobrevive a un nulo que preserva región, el paper confirma a BANC con un control que no puso; si no sobrevive, es un hallazgo. Las dos salidas son publicables; el mapa solo, no.
- [MEDIDO] Esqueleto actualizado en §1, la nota de relevancia y la checklist; el cotejo corre en Actions en la rama del Paper 3 con esta respuesta como fuente del §1.
- [NO MEDIDO] Métodos completos de los tres trabajos (si alguno usa nulos de tamaño o región); Namiki 2018, Cheong 2024 y Eckstein 2024 sin leer; la réplica en BANC.

## Herramientas y máquina

- Web: tres búsquedas y la lectura de la página de PMC del preprint de BANC (PMC12324551). Nada medido nuevo.
- brain-env (gateway, una llamada por vez): escritura y prueba en copia de los parches.
- GitHub: `push_files` a `main` (esta respuesta y el parche del CONTEXTO) y a `titan/paper3-esqueleto-2026-10-14` (parche del esqueleto y su workflow, que trae esta respuesta desde `main` y verifica su md5).
- ClickUp: Doc público de la 044.
- Delicado: no. Ningún merge, nada a Zenodo ni Kaggle; la réplica de H_LECTOR sigue corriendo en brain-env sin tocarla.

## Archivos

- `docs/agents/respuestas/2026-10-14-044-paper3-la-pregunta-ya-esta-respondida-por-banc.md` (esta).
- `tools/contexto/actualizar_contexto_2026-10-14-044.py` y su workflow en `main`.
- `tools/paper3/editar_esqueleto_2026-10-14-044.py` y `.github/workflows/paper3-fuentes-2026-10-14-044.yml` en la rama del Paper 3. Los md5 del esqueleto resultante y del cotejo quedan en `results/paper3_2026-10-15/MD5SUMS_044` de esa rama.

## NO MEDIDO

1. Métodos completos de Bates 2026, Braun 2024 y Stürner 2025 buscando nulos de tamaño o región.
2. Namiki 2018, Cheong 2024 (descendentes en MANC) y Eckstein 2024 (neurotransmisores), sin leer.
3. La réplica del mapa de salidas en BANC v888 y el nulo regional sobre la influencia de BANC.
4. Si la tensión sensorial directa contra influencia local sobrevive al pasar a varios saltos.

## Antes de firmar

- Las citas de BANC son del resumen verbatim (PMC12324551 y la página de Nature); las de Braun y Stürner, de sus resúmenes. No leí figuras ni métodos: el «no encontré nulos de tamaño o región» vale solo para lo leído y así queda escrito.
- El p 0,27854 y el 0,01393 los copié de la línea `FIRME_007 sensory -> motor BAJO` del log de la 008 en la rama del PR #26, leída hoy.
- La recomendación de reencuadre es opinión, no medición. Lo que la podría tirar: que los métodos de BANC ya traigan un nulo regional.

--- METODO PROMETEO ---
Rol: implementa. Delicado: no.
Máquinas: brain-env (prueba), Actions (aplicación y cotejo), web (lectura).
Artefactos: esta respuesta, el parche del CONTEXTO y su workflow; en la rama del Paper 3, el parche del esqueleto y su workflow; Doc de ClickUp de la 044.
