# Parche del esqueleto del Paper 3 (respuesta 2026-10-14-043): fija los dos nulos de LC6 a GF (060 y 065), la geometria a escala de neuropilo, el prior art (066 y 067) y el vinculo con H_LECTOR (038). Corre desde la raiz del repo; cada reemplazo exige una sola coincidencia, asi que una segunda aplicacion aborta.
NL = chr(10)
P = 'docs/paper3/paper3-esqueleto.md'
t = open(P, encoding='utf-8').read()
R = []

R.append(('before it is written as a gap.' + NL + '- Contribution:', 'before it is written as a gap. For the escape case the review is done and it closed a door: the visual to descending counts are already published from the same dataset (see 3.5).' + NL + '- Contribution:'))

R.append(('### 2.5 Escape case [2026-08-24-060, 2026-10-11-007]' + NL + '- Edge counts from LC4, LPLC2 and LC6 to the giant fiber (GF) and to DNp09, against 40 degree-preserving nulls; gain measured by running the compiled circuit.',
'### 2.5 Escape case [2026-08-24-060, 2026-08-25-065, 2026-10-11-007]' + NL + '- Edge counts from LC4, LPLC2 and LC6 to the giant fiber (GF) and to DNp09, against 40 degree-preserving nulls that shuffle destinations within super-class blocks; gain measured by running the compiled circuit.' + NL + '- Second null, neuropil-preserving: each neuron gets its dominant neuropil and destinations are shuffled within neuropil blocks, 40 realizations. It does not split synapses across neuropils, does not keep the exact in-degree and has no synapse threshold. Instrument `src/escape_neuropil_null.py` (md5 `c04ddd4282ada4f9df462f87d84d85ba`).' + NL + '- Opportunity bound: synaptic sites that source and target have in the same neuropil (`shared_min_sites`). It bounds the chance to connect; it is not contact.'))

R.append(('- Code and logs: branch `titan/tabla7-reconstruida-2026-10-10`, PR #26 (open, not merged, head `95e8d6c`). Each run records the md5 of inputs, code and logs.',
'- Code and logs: branch `titan/tabla7-reconstruida-2026-10-10`, PR #26 (open, not merged, head `95e8d6c`). Each run records the md5 of inputs, code and logs.' + NL + '- Neuropil null of the escape case: branch `titan/twohop-nulls` (`src/escape_neuropil_null.py`). Responses `2026-08-25-065`, `-066` and `-067` are copied verbatim into this branch so the cotejo can read them.'))

R.append(('### 3.5 Case: vision reaches action only through the descending bottleneck [2026-08-24-060, 2026-10-11-007, 2026-10-10-005]', '### 3.5 Case: vision reaches action only through the descending bottleneck [2026-08-24-060, 2026-08-25-065, 2026-08-25-066, 2026-08-25-067, 2026-10-11-007, 2026-10-10-005]'))

VIEJO_D = [l for l in t.split(NL) if l.startswith('- **[DISCREPANCIA, resolver antes de escribir]**')][0]
VIEJO_G = [l for l in t.split(NL) if l.startswith('- **[NO MEDIDO]** Whether the LC6 zero is a decision or geometry')][0]
NUEVO = NL.join([
'- Two nulls, two expected values, both pinned. The degree-preserving null expects 5.8 LC6 to GF edges; the neuropil-preserving null expects 17.2 ± 3.1 (z = −5.61, and the lowest of 40 realizations still gives 12). Confining the shuffle to the neuropil that LC6 and the GF share raises the expectation, so the second null is the harder test and the text leads with it; the first stays as a screen. **[NOTA]** los 5,8 son de la 060 y los 17,2 de la 065: no se contradicen, son dos preguntas distintas.',
'- Geometry at neuropil scale, measured: the dominant output neuropil of LC6 is PVLP (68,082 sites) and so is the dominant input neuropil of the GF (4,085 sites). LC6 shares 5,335 sites with the GF, more than LC4 (4,523), which makes 104 edges. Location does not explain the LC6 zero, whereas it does explain the LPLC1 zero to the GF (its neuropil null expects 0.2).',
'- Under the same null the routing splits by channel: LC9 is excluded from the GF (0 against 11.9, z = −4.0) and enriched 7.6× toward DNp09 (114 edges); LPLC2 enters both. The DNp09 counts of this null use a two-neuron DNp09 and are not comparable with the 170 above until rerun.',
'- The counts are not new. Kind et al. (bioRxiv 2024, eLife Reviewed Preprint 99277) give the looming VPN to DN matrix from FAFB without LC6 to DNp01, which is the GF, and the FAFB Cell Type Explorer lists the same absence. What this paper adds is the expectation: the LC6 zero survives a null that keeps the shared neuropil, and the LPLC1 zero does not.',
'- **[NO MEDIDO]** Distance between arbors (the LC6 glomerulus against the GF dendrites), purity of the neuropil blocks, and the neuropil null with a synapse threshold.'])
R.append((VIEJO_D + NL + VIEJO_G, NUEVO))

R.append(('## 4. Discussion [ESCRIBIR CUANDO ESTÉ LA RÉPLICA EN BANC]', '## 4. Discussion [ESCRIBIR CUANDO ESTÉ LA RÉPLICA EN BANC] [2026-10-14-038]'))
R.append(('- The descending bottleneck as the robust control signal, and the link to Paper 2: its escape bench reads exactly these descending neurons.',
'- The descending bottleneck as the robust control signal, and the link to Paper 2. **[PENDIENTE: cotejo de la réplica de H_LECTOR en brain-env]** Measured on Actions in the compiled network: a ridge reader on the traces of the 6 descending neurons (240 features) stays within 0.3 points of the same ridge on all 22,560 raw features (D1 = −0.0029, CI −0.0038 to −0.0020) and adds 4.7 points over the untrained readout (D2 = +0.0474). Almost all of the task signal a reader can find in the whole state is already in those 6 neurons.'))
R.append(('- Limits: one connectome, class labels as given, sign from a neurotransmitter prediction, no neuropil per synapse.', '- Limits: one connectome, class labels as given, sign from a neurotransmitter prediction, neuropil assigned per neuron (the dominant one), not per synapse.'))

R.append(('- [ ] Resolver la discrepancia del nulo de LC6 a GF (5,8 contra 17,2 esperadas).', '- [x] Discrepancia del nulo de LC6 a GF resuelta: son dos nulos (060 y 065), quedan los dos y manda el que preserva neuropilo (2026-10-14-043).'))
R.append(('- [ ] Solapamiento del glomérulo de LC6 con las dendritas de la GF: hace falta neuropilo, que no está en las anotaciones.', '- [ ] Solapamiento del glomérulo de LC6 con las dendritas de la GF: a escala de neuropilo ya está medido (065: comparten PVLP); falta distancia entre árboles.' + NL + '- [ ] Re-correr el nulo de neuropilo con DNp09 de 4 neuronas y con umbral de 5 sinapsis, para poder poner sus números de DNp09 al lado de los de la 060.' + NL + '- [ ] Leer el cotejo de la réplica de H_LECTOR antes de dejar el vínculo con el Paper 2 en la Discusión.'))

for a, b in R:
    n = t.count(a)
    print('reemplazo', n, a[:50])
    assert n == 1
    t = t.replace(a, b)
open(P, 'w', encoding='utf-8').write(t)
print('OK', len(t.split(NL)))
