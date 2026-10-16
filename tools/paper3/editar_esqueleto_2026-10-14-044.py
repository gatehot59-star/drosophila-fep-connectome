# Parche del esqueleto del Paper 3 (respuesta 2026-10-14-044): el §1 pasa de hueco sin revisar a prior art (Bates 2026 BANC, Braun 2024, Stürner 2025), nota de relevancia y checklist con el reencuadre. Corre desde la raiz del repo; cada reemplazo exige una sola coincidencia y escribe al final, asi que una segunda aplicacion aborta sin tocar nada.
NL = chr(10)
P = 'docs/paper3/paper3-esqueleto.md'
t = open(P, encoding='utf-8').read()
R = []

VIEJA_REL = [l for l in t.split(NL) if l.startswith('> **Relevancia (opinión, 2026-10-14-007):**')][0]
R.append((VIEJA_REL, VIEJA_REL + NL + NL + '> **Relevancia, revisada (2026-10-14-044):** baja como mapa. BANC (Bates et al., Nature 2026) ya responde qué alimenta cada salida, Braun et al. (Nature 2024) ya tiene las redes de descendentes y Stürner et al. (Nature 2025) el atlas de descendentes y ascendentes. Lo único propio es el nulo de tamaño y región. Reencuadre recomendado: usar ese nulo para poner a prueba la afirmación de BANC sobre lazos locales, con la réplica en BANC v888 como corrida central (decide Abraham).'))

R.append(('## 1. Introduction' + NL, '## 1. Introduction [2026-10-14-044]' + NL))

VIEJO_HUECO = [l for l in t.split(NL) if l.startswith('- **[NO MEDIDO]** We did not find a published input map of all output classes')][0]
NUEVO_HUECO = NL.join([
    '- **[REVISADO]** The question is not open. Bates et al. (Nature 2026, the BANC brain-and-cord connectome) ask what influences each effector (motor neurons, endocrine cells and visceral efferents) and answer with an influence metric: local sensory cells in the same body part, linked by ascending and descending neurons. Braun et al. (Nature 2024) show networks of descending neurons that recruit other descending neurons, against a shuffled network. Stürner et al. (Nature 2025) give the complete atlas of descending and ascending neurons in FlyWire, FANC and MANC, including the sensory input of each descending neuron.',
    '- What is left for this paper is the expectation: how much of each input share survives nulls that fix size and brain region. **[NO MEDIDO]** Only the abstracts of the three papers and the introduction of BANC were read; their methods still have to be checked for size- or region-matched nulls. For the escape case the review is done and it closed the same door: the visual to descending counts are already published from the same dataset (see the escape case).',
])
R.append((VIEJO_HUECO, NUEVO_HUECO))

R.append(('- [ ] Revisión de literatura de descendentes y ascendentes (FlyWire, MANC, BANC) para el hueco de §1.', '- [x] Revisión de literatura del §1 (2026-10-14-044): BANC, Braun 2024 y Stürner 2025 ya responden la pregunta como mapa; falta leer sus métodos completos buscando nulos de tamaño o región.' + NL + '- [ ] Reencuadre (decide Abraham): el Paper 3 como prueba con nulo regional de la afirmación de BANC sobre lazos locales, con la réplica en BANC v888 como corrida central.'))

for a, b in R:
    n = t.count(a)
    print('reemplazo', n, a[:50])
    assert n == 1
    t = t.replace(a, b)
open(P, 'w', encoding='utf-8').write(t)
print('OK', len(t.split(NL)))
