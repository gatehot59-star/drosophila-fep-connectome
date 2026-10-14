---
title: "[TITULO DE TRABAJO] The connectome as a blueprint: a sealed functional benchmark of the *Drosophila* looming-escape pathway across three scales and two flies"
subtitle: "Paper 2 · SKELETON, not a draft for submission (2026-10-14)"
author:
  - name: Jorge Abraham Mendieta
    affiliation: "Independent Researcher, Salta, Argentina · ORCID 0009-0009-3831-6784"
    email: profeabrahamm@gmail.com
lang: en
---

> **NOTA (para Abraham, se borra antes de publicar).** Esqueleto, no borrador. El texto del paper va en inglés, como la v2 del Paper 1; las notas van en castellano. Cada número lleva entre corchetes la respuesta de git de donde sale. Lo marcado **[PENDIENTE]** espera una corrida; lo marcado **[NO MEDIDO]** todavía no tiene instrumento. Nada de esto se escribe como resultado hasta que su agregado sellado esté en git.

> **Alcance decidido (Abraham, ClickKit `alcance_p3_005`, 14-oct 12:19).** Una sola pregunta: *¿el cableado exacto de la mosca carga la función del reflejo, más allá de su diseño y de sus barajados, y esa parte se conserva en otra mosca?* El control de las salidas (2026-10-10-005 a 009), LC6→GF y sel_post quedan **fuera de este paper y van a un Paper 3 estructural**: son otra pregunta con otros nulos.

## Abstract [ESCRIBIR AL FINAL]

Slots, in order: (1) the question; (2) the sealed bench (task with the fly's own labels, three descending lines, 564 sensory entries, untrained readout); (3) wiring beats degree-preserving and type-shuffled nulls at every scale tested [2026-10-12-018, 2026-10-13-010, 2026-10-14-001]; (4) the simulated wiring reaches but does not exceed, by the pre-registered margin, an idealised hand rule built on the same sensors [2026-10-13-010]; (5) function saturates at a 33,489-neuron cut: the whole brain makes the same prediction in 99.913% of trials [2026-10-14-001]; (6) strong connections are conserved in a second fly (BANC) [2026-10-14-002]; (7) **[PENDIENTE] whether the conserved core alone carries the reflex (H_CONSENSO)**; (8) **[PENDIENTE] whether choosing tau by cross-validation removes the seed dependence (H_TAU)**.

## 1. Introduction

- Whole-brain connectomes now exist for more than one fly: FlyWire (female brain; Dorkenwald et al., 2024; Schlegel et al., 2024), BANC (female brain and nerve cord; Bates et al., 2026) and MaleCNS (Berg et al., 2025).
- Connectome-constrained models predict activity and behaviour (Shiu et al., 2024; Lappalainen et al., 2024), but they are rarely tested against the two controls that decide whether the *exact* wiring matters: (a) shuffled wiring with the same degrees, and (b) a hand-designed rule that uses the same sensors.
- Structural stereotypy across flies is documented: connections above about 10 synapses are conserved, and fine weights vary (Schlegel et al., 2024). **[NO MEDIDO]** We did not find a functional test of whether the conserved part carries the function. This needs a systematic search before it is written as a gap.
- Contribution: a pre-registered bench (sealed code with md5, triggers, smoke tests and frozen aggregators) applied to the looming-escape pathway at four scales and against a second connectome.

> NOTA: la frase de los LLM ("el LLM piensa, la mosca esquiva", 2026-10-13-018) va como una línea de motivación en la Discusión, no en la Introducción.

## 2. Methods

### 2.1 Task with the fly's own labels [2026-10-12-015]
- 20 balanced conditions: state (resting, flying) × stimulus (LOOM_LATERAL, LOOM_FRONTAL, SPOT, BAR, NONE) × side; 40 steps of 20 ms.
- Five responses: none, take off, land, turn right, turn left.
- Looming gives take-off at rest and landing in flight (Ache et al., 2019). LPLC2 and DNp06 drive evasive turns to lateral or approaching objects (Kim et al., 2023).
- Readout lines, untrained:
  - DNp01 (take-off) competes only at rest.
  - DNp07 (landing) and the DNp06 left-minus-right difference (turn) compete only in flight.
  - Each line's threshold is the 0.95 quantile of its maximum over the training trials where the correct answer is none. The first line to cross wins.
- Six cells: amplitude A ∈ {0, 0.3, 0.6} × input noise ∈ {0.15, 0.45}.
- SPOT and BAR labels at rest are working labels without a source; declare this.

### 2.2 Model
- Leaky rate units on the FlyWire v783 graph with signed synapse weights; tau drawn by seed (10 tau seeds × 10 test seeds in factorials 3 and 4).
- **[ESCRIBIR]** The exact equation and the input model, from `tools/factorial2/factorial2_mosca.py` (md5 798a824c).
- **[DECLARAR]** The LPLC2 response to a translating spot is qualitatively supported (Kim et al., 2023), but its amplitude is a modelling assumption that no source we read fixes as a number [2026-10-12-013].

### 2.3 Scales
| Cut | Neurons | Source |
|---|---|---|
| M46 (motif) | 46 (40 visual + 6 DN), 187 edges, 0 inhibitory | 2026-10-12-015 |
| R1 | 1,504 | 2026-10-12-018 |
| R2 | 33,489; 4,031,897 edges | 2026-10-13-008 |
| Whole brain (CE) | 138,639 | 2026-10-14-001 |

### 2.4 Rivals and nulls
- **Hand rule with the same 564 entries:** the fly's labels read on raw inputs, without weights or dynamics (for example, DNp01 = mean of LC4 and LPLC2 on its side) [2026-10-12-018].
- **SL:** destinations permuted within each (pre side, post side) block, with source and weight fixed; this preserves degrees and sides.
- **T:** tuned visual types permuted by side, with the real wiring.
- 50 + 50 nulls at R2 and CE [2026-10-13-008]; 300 + 300 at M46 [2026-10-12-018].

### 2.5 Statistics (sealed before running)
- Primary contrast: d = W minus the rule with the same sensors. Two-way bootstrap, B = 20,000, 90% CI (TOST at 5% per side), margin 0.01. Verdicts: SUPERA, NO_INFERIOR, EQUIVALENTE, NO_SUPERIOR, PIERDE, SIN_DECIDIR.
- Nulls: p = (1 + #nulls ≥ W)/(N + 1), with Holm correction across SL and T.

### 2.6 Pre-registration and reproducibility
- Each experiment had a SELLO file with the md5 of its code, a smoke test on Actions and a `CORRER` trigger pushed only with the author's go-ahead.
- Controls inside each aggregator: an exact anchor, a complete plan, TAU_DN_IGUAL, REPRODUCE (overlapping runs match the previous factorial exactly) and REAL_IGUAL.
- Factorial 4 can be recomputed from the CSVs: 18 of 18 lines match, and a single altered run makes it fail [2026-10-14-001].

### 2.7 Second fly (BANC v888) [2026-10-14-002]
- Downloaded files match the public bucket md5 (meta 8c2b93a6, edges v3 08542b07).
- Edges are indexed by `root_888`; a first pass with `root_id` was invalid (20.8%) and is reported as such.
- Only unique `fafb_match` pairs are used (25,492), because 13,173 FlyWire IDs map to more than one BANC neuron.

## 3. Results

### 3.1 At the motif scale, wiring beats its shuffles but loses to its own design [2026-10-12-018]
- W wins against SL and T in 6/6 cells (Holm 0.0399, the minimum possible); 0 of 300 nulls equal W in any cell.
- Against the hand rule: worse in 4 cells and tied in 2, never better.
- The motif carries 875 of the 40,145 synapses onto the six DNs (2.18%) and none of the 14,576 inhibitory ones.

### 3.2 More real wiring, more accuracy [2026-10-13-007]
| Config | W | Own rule | d (points) | Verdict |
|---|---|---|---|---|
| M46_TASA | 0.8959 | 0.9022 | −0.62 | NO_SUPERIOR |
| R1_CON_TASA | 0.9199 | 0.9301 | −1.02 | NO_SUPERIOR |
| R2_CON_TASA | 0.9412 | 0.9284 | +1.28 | NO_INFERIOR |

Sensors matter: the 418-entry rule beats the 40-entry rule by +2.79. Liquid (trained) tau gives no gain at R1 (EQUIVALENTE). R2 had only 3 × 5 seeds here, which is why factorial 3 exists.

### 3.3 At R2, the wiring reaches its design and its shuffles collapse [2026-10-13-010]
- R2 0.9353 vs rule 0.9268: d = +0.85 points, 90% CI [+0.08; +1.51], NO_INFERIOR in all 6 cells. H_SUPERA_R2 is SIN_DECIDIR. The +1.28 of factorial 2 was partly seed luck.
- Nulls: real 0.9465; SL mean 0.666 (max 0.796); T mean 0.760 (max 0.839); none of 100 reach the real wiring; Holm 0.039. Destinations shuffled cost 28 points; types shuffled cost 19.

### 3.4 The whole brain adds nothing over R2 [2026-10-14-001]
- CE − R2 = +0.01 points, 90% CI [−0.01; +0.04], EQUIVALENTE in six cells. Identical prediction in 1,198,955 of 1,200,000 trials (99.913%).
- CE vs rule: +0.86, 90% CI [+0.11; +1.51], NO_INFERIOR. Nulls: SL mean 0.6488, T mean 0.7596, Holm 0.0392.
- Post hoc, not sealed: the margin against the rule depends on the tau seed (seed 5: −2.30; seed 7: −0.85; the other 8: +1.28 to +1.71). This motivates H_TAU (§3.7).

### 3.5 Strong connections are conserved in a second fly [2026-10-14-002]
| FlyWire strength (synapses) | Present in BANC (≥1) | Present in BANC (≥5) |
|---|---|---|
| 1–4 | 28.9% | 4.0% |
| 5–9 | 60.0% | 20.6% |
| 10–19 | 77.2% | 43.3% |
| ≥20 | 92.4% | 79.0% |
| Schlegel core | 77.0% | 51.1% |
| Rest | 32.7% | 6.1% |

- 782,453 evaluable R2 edges; 6/6 DNs paired. Entries paired: 291/564 by `fafb_match`, 363/564 by either method.
- **[NO MEDIDO] Null for this table:** random pairs with matched degree. Without it, the gradient could partly be a matching artefact. This blocks writing §3.5 as a result.

### 3.6 Does the conserved core carry the reflex? [PENDIENTE: H_CONSENSO, sealed 2026-10-14-002, running since 2026-10-14 11:30]
- Core: 603,219 of 4,031,897 R2 edges (14.96%) carrying 56.97% of synapses; 6/6 DNs, 563/564 entries.
- Pre-registered: the core loses no more than 1 point against R2 and beats 50 SL + 50 T of the core.
- Write both outcomes in advance: if it holds, the conserved part is the functional part; if it fails, structure is conserved but function needs the weak edges.

### 3.7 Tau chosen by cross-validation [PENDIENTE: H_TAU, sealed 2026-10-14-002, running since 2026-10-14 11:30]
- Candidates tau 10 to 19, chosen by 5-fold CV on training, tested on new seeds 12 to 21, margin 0.01; REPRO_R2 guard.

### 3.8 A negative result that shaped the task [2026-10-12-012, 2026-10-12-013]
- With a labelled-line task that labelled "spot in flight → nothing" and read flight threat through DNp01, the wiring did NOT pay (loses or ties against nulls; the hand rule wins 6/6).
- Literature showed both labels contradict the fly (Kim et al., 2023; Ache et al., 2019). Correcting the task (§2.1) is what made the wiring pay (§3.1).
- Report it: a bench result is a result about the task.

## 4. Discussion [ESCRIBIR CUANDO ESTÉN 3.6 Y 3.7]
- The exact wiring is necessary (shuffles lose 19 to 28 points) but, in our simulation, it is not better than the fly's design idealised as a rule on the same sensors. Our model of the synapses is what falls short, not the fly.
- Function saturates by R2: what matters is a separable piece, not brain size.
- If H_CONSENSO holds, this supports a "parts factory": conserved reflex modules that can be exported. The cheapest export may be the hand rule; the bench decides which.
- Limitations:
  - one task;
  - simulated inputs, with the LPLC2 amplitude assumed;
  - rate units, not spiking;
  - one connectome for function, the second only for structure;
  - no BANC null yet;
  - tau seed dependence.

## 5. Data and code availability
- Repository: `gatehot59-star/drosophila-fep-connectome`. Branches `titan/tarea-mosca-2026-10-12`, `titan/factorial2-mosca-2026-10-13`, `titan/factorial3-mosca-2026-10-13`, the factorial 4 Kaggle kernels, and `titan/htau-nucleo-banc-2026-10-14`.
- Inputs: FlyWire v783 connectivity (Shiu et al.) and annotations at a fixed commit; BANC v888 from the public bucket.

## Figures and tables (plan)
1. Task and readout schematic (§2.1).
2. Accuracy vs scale, with rule and null bands (§3.1 to 3.4).
3. Null distributions at R2 and CE.
4. BANC conservation vs strength, with the null when it exists (§3.5).
5. Core vs R2 (§3.6).
6. Tau per seed, before and after CV (§3.4, §3.7).

## Lo que falta para un borrador (checklist)
- [ ] H_CONSENSO y H_CABLEADO_NUCLEO: leer el agregado sellado.
- [ ] H_TAU: leer el agregado sellado.
- [ ] Nulo del emparejado BANC: diseño, sello y corrida.
- [ ] Revisión de literatura para el hueco de §1 (¿alguien probó función de la parte conservada?).
- [ ] Ecuación y modelo de entrada exactos (§2.2) desde el código sellado.
- [ ] Figuras desde los CSV de git, con script commiteado.
- [x] Alcance: el control de salidas, LC6→GF y sel_post van al Paper 3 (Abraham, 14-oct 12:19).
- [ ] Referencias verificadas una por una (la v1.0 tenía cinco mal).
