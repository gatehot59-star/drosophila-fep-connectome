---
title: "[TITULO DE TRABAJO] Who drives the outputs of the fly brain? A null-controlled input map of descending, motor and neurosecretory neurons in FlyWire v783"
subtitle: "Paper 3 · SKELETON, not a draft for submission (2026-10-14)"
author:
  - name: Jorge Abraham Mendieta
    affiliation: "Independent Researcher, Salta, Argentina · ORCID 0009-0009-3831-6784"
    email: profeabrahamm@gmail.com
lang: en
---

> **NOTA (para Abraham, se borra antes de publicar).** Esqueleto, no borrador. El texto va en inglés y las notas en castellano, como el Paper 2. Cada sección con números lleva entre corchetes las respuestas de git de donde salen, y `tools/paper3/cotejar_paper3.py` coteja cada número contra esas fuentes. Lo marcado **[PENDIENTE]** espera una corrida; lo marcado **[NO MEDIDO]** todavía no tiene instrumento.

> **Alcance (Abraham, ClickKit `alcance_p3_005`, 14-oct 12:19; respuesta 2026-10-14-006).** Una sola pregunta: *¿qué clases de neuronas alimentan cada salida del cerebro (descendentes, motoras y neurosecretoras), más allá de lo que explican el tamaño, la ubicación y la cantidad de pruebas?* El escape visual (LC4, LPLC2 y LC6 hacia la fibra gigante, y la fibra gigante sin motoras) entra como caso de la respuesta. sel_post es dinámica, no estructura: recomiendo apéndice o afuera (decide Abraham, §3.6).

> **Relevancia (opinión, 2026-10-14-007):** baja a media. Es un mapa de consulta con nulos serios, no un descubrimiento.

## Abstract [ESCRIBIR AL FINAL]

Slots, in order: (1) the question; (2) the statistic: the share of each output neuron's synaptic input that comes from each class, at one and two hops; (3) three nulls of increasing strength (random destinations, size-matched label permutation, region-preserving permutation) and three corrections (Benjamini-Yekutieli, Holm, max-T); (4) what looks like control at first sight and turns out to be size or location; (5) what survives everything: descending neurons drive motor, neck and antennal outputs and other descending neurons, and the optic lobe is depleted onto descending neurons; (6) the visual escape as a worked case: vision reaches action only through the descending bottleneck.

## 1. Introduction

- The fly brain talks to the body through a few output classes: descending neurons to the nerve cord, motor neurons of the head and neurosecretory cells. [REFERENCIAS POR VERIFICAR]
- A whole-brain connectome lets us count, for every output neuron, where its synaptic input comes from. Counting is easy; deciding which counts are more than size and location is not.
- **[NO MEDIDO]** We did not find a published input map of all output classes against nulls that fix neuron size and brain region. It needs a literature review (descending and ascending connectomics in FlyWire, MANC and BANC) before it is written as a gap.
- Contribution: a measured map with three nulls and three multiple-comparison corrections, with code and logs public.

## 2. Methods

### 2.1 Data [2026-10-10-005]
- FlyWire v783: 138,639 neurons, 15,091,983 edges and 54,492,922 synapses; class labels from the FlyWire annotations (pinned in the code).
- Outputs: descending (1,299 neurons), motor (110, split by cell_sub_class) and endocrine (76, split by cell_type).

### 2.2 Statistic [2026-10-10-005]
- D1(C, O): mean, over the neurons of output set O, of the fraction of their synaptic input that comes from class C. D2: the same through any one intermediate neuron.
- Two thresholds: all edges, and edges with 5 or more synapses.
- Sign: from the neurotransmitter prediction in the parquet, not from physiology.

### 2.3 Nulls [2026-10-10-005, 2026-10-10-006, 2026-10-10-007]
- Random destination sets of the same size (R = 10,000). With permuted labels it flags about 3% false patterns (8/242 and 6/231), so it is only a first screen.
- Label permutation, flat and size-stratified (R = 10,000 each).
- Region-preserving permutation: k-means on neuron positions (k = 40 and k = 120) plus size strata (R = 5,000 per mode and threshold).

### 2.4 Multiple comparisons [2026-10-10-008, 2026-10-10-009]
- 242 tests with all edges and 231 with 5 or more synapses.
- Benjamini-Yekutieli (false discovery rate under any dependence), Holm, and max-T of Westfall and Young (family-wise error).

### 2.5 Escape case [2026-08-24-060, 2026-10-11-007]
- Edge counts from LC4, LPLC2 and LC6 to the giant fiber (GF) and to DNp09, against 40 degree-preserving nulls; gain measured by running the compiled circuit.

### 2.6 Reproducibility
- Code and logs: branch `titan/tabla7-reconstruida-2026-10-10`, PR #26 (open, not merged, head `95e8d6c`). Each run records the md5 of inputs, code and logs.

## 3. Results

### 3.1 At first sight, the central brain drives every output [2026-10-10-005]
- The central brain provides 60.23% / 62.42% (all edges / 5 or more) of descending input, 64.34% / 65.54% of motor input and 73.03% / 67.88% of neurosecretory input: 2.3 to 2.9 times a random destination set. It is the largest input of 1,051 of 1,299 descending neurons, 90 of 110 motor neurons and 62 of 73 neurosecretory neurons.
- Descending neurons provide 21.48% / 21.89% of motor input (×20.7 / ×26.5): neck 39.96% / 43.07%, antenna 32.06% / 32.26%, proboscis 24.72% / 25.12%.
- Ascending neurons provide 15.93% / 20.31% of neurosecretory input (×8.6 / ×11.7).
- The optic lobe provides 0.45% / 0.33% of descending input and 0.00% of motor and neurosecretory input; at two hops, 3.64% / 2.71%. Direct sensory input is between 3.15% and 6.16% of each output.
- Sign (a prediction, not physiology): central to motor is 43.72% / 43.81% excitatory; sensory to descending, 99.58% / 99.54%.

### 3.2 Against size-matched permutations, the central brain wins by less [2026-10-10-006]
- Central brain over size-matched labels: ×1.63 / ×1.86 / ×2.29 (descending / motor / neurosecretory), against ×2.58 / ×2.75 / ×3.13 with the flat permutation (R = 10,000 each).
- Descending to motor stays at ×20 and ascending to neurosecretory at ×10; the insulin-producing cells (IPC) fall.
- Visual projection neurons reach descending neurons below chance (×0.68 / ×0.64); direct sensory input to descending neurons is chance (×0.96 / ×1.04).

### 3.3 With the brain region fixed, most of the central brain's lead was location [2026-10-10-007]
- With region and size fixed (R = 5,000), descending neurons still drive motor neurons (×3.69 / ×3.21, k = 40 / k = 120) and other descending neurons (×3.29 / ×2.61).
- The central brain's lead over descending (×1.07 / ×1.01) and neurosecretory neurons (×1.09 / ×1.03) was location. Its own surplus is small and goes to motor neurons (×1.31 / ×1.16), mostly those of the mouth.

### 3.4 What survives every correction with both nulls [2026-10-10-008, 2026-10-10-009]
- Region-preserving null: of 33 firm claims, Benjamini-Yekutieli keeps 31 and max-T keeps 5.
- Strong null: of 41 firm claims, Benjamini-Yekutieli keeps 41, Holm 34 and max-T 11. Central to descending and ascending to descending survive max-T there, but §3.3 shows they were location.
- Family-wise with both nulls, five claims survive: descending to descending, to motor, to neck and to antenna, and the optic lobe depleted onto descending neurons.
- The central surplus to mouth motor neurons and to DH44 survives Benjamini-Yekutieli (0.014 to 0.040) but not max-T (0.58 to 0.91).

> NOTA: este es el resultado del paper. Lo demás es el camino para llegar.

### 3.5 Case: vision reaches action only through the descending bottleneck [2026-08-24-060, 2026-10-11-007, 2026-10-10-005]
- LC4 to GF: 104 edges against a null mean of 11.4 (9.1×, 0/40). LPLC2 to GF: 189 (7.4×, 0/40). LPLC2 to DNp09: 170 (3.6×, 0/40).
- LC6 to GF: 0 edges against a null mean of 5.8 (40/40 nulls above). Other visual projection types to GF: 6 against 256.3 expected.
- Running the compiled circuit, LC4 plus LPLC2 drive the GF 40 times more than LC6 (0.704 against 0.017). Looming against receding gives 1.04× (0.7034 against 0.6772): the circuit does not detect approach by itself, and its subgraph has 0 inhibitory edges of 13,026.
- GF to motor neurons: 0 edges, and the optic lobe gives 0.00% of motor input (§3.1). Vision has no shortcut to the motor neurons: it has to pass through descending neurons.
- **[DISCREPANCIA, resolver antes de escribir]** Another null gave 17.2 ± 3.1 expected LC6 to GF edges (z = −5.61) in the GF-01 sheet (962 input edges, 9,474 synapses, 49.8% inhibitory). Two nulls give two expected values (5.8 and 17.2): pin which one and why.
- **[NO MEDIDO]** Whether the LC6 zero is a decision or geometry (the LC6 glomerulus not overlapping the GF dendrites). The annotations have no neuropil column, so the text says "absence of pathway", not "active exclusion".

### 3.6 [OPCIONAL, decide Abraham] Transient selectivity: sel_post [2026-10-02-004, 2026-10-11-005]
- sel_post beats the topology null in the full configurations (0/40, z = +181) and the sign null (z = +6.31); sel_peak does not.
- The circuit has about 5.8x less absolute post-stimulus activity than the null, with higher differential selectivity: topology can suppress generic reverberation and keep differential selectivity in the transient.
- Not swept: integration window, tau, anatomical null, more circuits.

> NOTA: es dinámica, no estructura, y no tiene el barrido hecho. Recomiendo apéndice o afuera.

## 4. Discussion [ESCRIBIR CUANDO ESTÉ LA RÉPLICA EN BANC]

- What was size, what was location, what is wiring.
- The descending bottleneck as the robust control signal, and the link to Paper 2: its escape bench reads exactly these descending neurons.
- Limits: one connectome, class labels as given, sign from a neurotransmitter prediction, no neuropil per synapse.

## 5. Data and code availability

- FlyWire v783 public files; code and logs in the repository (the PR #26 branch until it is merged).

## Figures and tables (plan)

1. Heat map of D1 (class by output), all edges and 5 or more (§3.1).
2. Enrichment under the three nulls, side by side (§3.2, §3.3).
3. Survival table under Benjamini-Yekutieli, Holm and max-T (§3.4).
4. Escape case diagram: LC4, LPLC2 and LC6 to GF and DNp09 and on to the nerve cord, with counts and null bands (§3.5).

## Lo que falta para un borrador (checklist)

- [ ] Revisar y mergear el PR #26: el código de la 005 a la 009 vive en una rama sin review.
- [ ] Resolver la discrepancia del nulo de LC6 a GF (5,8 contra 17,2 esperadas).
- [ ] Solapamiento del glomérulo de LC6 con las dendritas de la GF: hace falta neuropilo, que no está en las anotaciones.
- [ ] Réplica del mapa de salidas en BANC v888 (ya bajado en brain-env): es lo que más le suma.
- [ ] Revisión de literatura de descendentes y ascendentes (FlyWire, MANC, BANC) para el hueco de §1.
- [ ] Decidir sel_post: adentro, apéndice o afuera.
- [ ] Figuras desde los logs, con script commiteado.
- [ ] Referencias verificadas una por una.
