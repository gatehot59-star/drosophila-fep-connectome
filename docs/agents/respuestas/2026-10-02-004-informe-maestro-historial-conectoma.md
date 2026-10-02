# Informe maestro del historial del conectoma

## 1. Pedido
Leer el trabajo histórico accesible en Git, brain-env, Kaggle y ClickUp, y producir un informe de todo lo alcanzado: Paper 1, nulls, SparseLTC, DualBrain/DBC3, Kaggle e H4.

## 2. Herramientas y alcance
GitHub API sobre `main` y las ramas `titan/initial-release`, `titan/twohop-nulls`, `titan/auditoria-integra-2026-08-25` y `titan/auditoria-hipotesis-2026-10-01`; lectura de árboles, commits, recibos, logs y runners. MUDH Gateway en `brain-env` para comprobar el árbol persistente, localizar outputs históricos y mapear Kaggle. ClickUp Search/Load para documentos, mensajes y adjuntos relevantes. Se usaron agentes de minería para ampliar cobertura.

**Cobertura honesta:** exhaustivo sobre los hallazgos canónicos identificados, no sobre cada mensaje/adjunto histórico. Las búsquedas devolvieron más de 125 documentos y más de 125 mensajes en varias particiones con solapamiento, 58 adjuntos relevantes y threads truncados. Se procesaron sustantivamente decenas de documentos, commits, logs y mensajes. La colección y el procesamiento global quedan PARCIALES.

## 3. Veredicto

El activo real es la combinación de un grafo FlyWire reproducido, controles contra nulls, dinámica firmada con Dale, un motor líquido compacto y una agenda de hipótesis mejor formulada. No está demostrado que la mosca active y desactive rutas según la acción: **H4 fuerte sigue NO MEDIDA**.

H4 débil queda **REFUTADA en su operacionalización estrecha**. ComplexLTC no tiene ventaja demostrada. DualBrain/DBC3 tiene resultados sintéticos útiles, pero limitaciones claras y ningún benchmark biológico end-to-end.

## 4. Paper 1 y estado del grafo

- `138.639` neuronas, `15.091.983` aristas agregadas, peso total de sinapsis `54.492.922`.
- Identidad del grafo verificada por dimensiones, `nnz`, peso total y comparación arista por arista.
- La densidad `0,0074` publicada fue causada por overflow `int32` en `N*(N-1)`; densidad corregida aproximadamente `0,000785197`.
- El `36x` de reciprocidad queda retirado porque dependía del mismo overflow.
- La reciprocidad reproducida es `26,60%`, `4.014.518` aristas; claim defendible: rank 1 frente a CP, `20,59x` sobre media CP y `47,27x` frente a MS, con `0/40` nulls alcanzando el real.
- Con umbral de cinco sinapsis: `13,98%` frente a `13,8%` de Lin; `12,647` sinapsis/conexión frente a `12,6`.
- “Reciprocidad global excepcional” está refutado frente a cinco conectomas.
- “Lin solo reporta una cifra global” está retirado: Lin descompone por neuropilo.
- El null CP no es innovación absoluta: NPC de Lin es prior art de la misma familia.
- `1,559x` no es un resultado reproducible; la Tabla 5 completa y sus p-valores siguen NO MEDIDOS, en especial AN y la décima clase.

Fuentes: [`ERRATUM.md`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/ERRATUM.md), [`PIVOTE-RECIPROCIDAD.md`](https://github.com/gatehot59-star/drosophila-fep-connectome/blob/main/docs/PIVOTE-RECIPROCIDAD.md), [comparación con Lin/BANC](https://app.clickup.com/90171457413/docs/2kza6fw5-4697/2kza6fw5-6677).

## 5. Hallazgos estructurales

### Routing

El null de grado produce olfatorio/visual depletados y mecanosensorial/gustativo enriquecidos a dos saltos, spread crudo aproximado `323x`, `0/40` y `40/40`. Pero el null anatómico posterior invierte tres signos y colapsa el spread a `2,4x`: queda **confirmado contra grado, NO MEDIDO como claim anatómicamente robusto**.

### LC6→GF

LC6→GF sobrevive al null por neuropilos; ese cero sí parece una restricción de ruta y no mera co-localización. La tabla de routing visual ya tenía precedentes en Kind/Cell Type Explorer.

### Plasticidad

El circuito plástico representa `5.608/138.639 = 4,045%` de neuronas, KC→MBON `0,41%` de aristas y `0,47%` de sinapsis. Contra CP sobreviven KC→MBON `7,81x`, DAN→KC `8,71x` y KC→KC `7,26x`, todos `0/40`; DAN→KC es `23,5x` DAN→MBON. Esto demuestra topología de modulación, no que el aprendizaje sea mínimo.

## 6. Dinámica

`sel_post` supera el null de topología en las configuraciones completas con `0/40`; `sel_peak` no muestra la misma ventaja. El circuito tiene aproximadamente `5,8x` menos actividad post-estímulo absoluta que el null, pero mayor selectividad diferencial.

La formulación correcta es: **la topología puede suprimir reverberación genérica y conservar selectividad diferencial en el transitorio**, no necesariamente amplificar amplitud. Falta barrer ventana de integración, tau compleja, null anatómico y más circuitos.

La inversión temporal en `t=50/100/149` se replica descriptivamente, pero no autoriza un claim p<0,05 tras corrección múltiple.

Corrección importante: el `z=197` es el valor MS, no el CP. En CP, a t=200, el ratio es aproximadamente `3,496x`, `z≈15,0`, `0/19`; MS da `110,694x`, `z≈197`, `0/19`.

## 7. SparseLTC y ComplexLTC

- SparseLTC opera sobre estructura real, pesos E/I y tau.
- Dale: `0` mixtas entre `138.005` neuronas con salida; `96.672` excitatorias puras y `41.333` inhibitorias puras.
- Tau es sensible; subir `0,0595→0,119` cambia respuesta `8,8–9,0%`; duplicar otra vez agrega `0,6–0,7%`.
- Escala de pesos produce cambios menores en los subgrafos medidos.
- ComplexLTC es LTC-inspired, no LTC canónico.
- Complex tau no tiene ventaja: test global con nueve nulls `p=0,6000`; brazo W real `p=0,175` en t=50/149 y `p=0,80` en t=100.
- Benchmark matched proxy: FlyVis-like `72,22%`, SparseLTC real `66,67%`, SparseLTC complejo `47,22%`. La fase compleja queda refutada como mejora general para esa tarea.

## 8. DualBrain/DBC3

- Ablación iso-run/iso-arquitectura/iso-celda/iso-encoder: gate supera DualNoGate `108,11x`, `21,85x`, `58,97x`, `36,72x`.
- En MultiCue, benchmark publicado: DualBrain pierde frente a GRU/LSTM/MinGRU `0,42x`, `0,25x`, `0,59x`.
- `1,18x` favorable pertenece a otro punto del sweep, no al benchmark fijo.
- El benchmark v3 histórico no es plenamente reproducible: FAST_MODE, una seed y outputs incompletos.
- El puente SparseLTC→DBC3 está diseñado/compilado, pero no existe benchmark biológico end-to-end.
- DualBrain aporta gate/memoria/veto, no planificación/world model/goal acquisition medidos.

## 9. Kaggle y reproducibilidad

- Corpus corregido: `40` kernels, no `29`: `29` febrero-marzo + `11` agosto, sin solapamiento.
- Overflow en `3/40`, todos de marzo; `0/11` de agosto.
- Cuatro fuentes son byte-idénticas a Git: `motor.py`, `cp40.py`, `nulls40_kaggle.py`, `hm_sweep.py`.
- Seis fuentes ejecutadas siguen fuera de Git.
- La comparación umbralizada de cinco sinapsis reproduce los valores de Lin.
- El script original de Tabla 7 sigue perdido; la reimplementación dinámica no es reproducción de esa tabla.

## 10. H4

H4 débil: perfiles de escape/grooming/feeding casi idénticos, cosenos `0,999786–0,999845`; **REFUTADA solo en ese alcance**.

H4 fuerte: **NO MEDIDA**. El pipeline cross-animal/temporal mezcló `54.000` frames de conducta con `8.767/8.768` frames DFF por el entero `Frame`, aunque ambos cubrían aproximadamente `540 s`, generando desfase `6,16x`. Los resultados `0,1816 vs 0,2019` y deltas temporales quedan retirados como biología.

Las nueve estadísticas globales borran identidad ROI, signo, fase y anatomía. Faltan loader oficial `roi_dFF.pkl`, `alignment_guard` negativo, bouts/trials, mapping ROI→FlyWire, null anatómico y silenciamiento causal.

## 11. Hipótesis nuevas

1. La topología selecciona transitorios y suprime reverberación, no necesariamente amplitud.
2. La plasticidad es pequeña en volumen pero estratégicamente ubicada por DAN→KC/KC→KC.
3. La selección contextual depende de módulos anatómicos y contexto compartido, no de etiquetas conductuales gruesas.
4. La jerarquía de rutas exige null que conserve neuropilo, distancia, grado y signo.
5. El gate vectorial sirve para arbitraje/interacción, pero no reemplaza planificación.
6. La fase compleja solo debe volver al producto si una tarea exige fase, interferencia u oscilación.

## 12. Correcciones históricas que son parte del resultado

Se retiraron: excepcionalidad global de reciprocidad, novedad absoluta del null CP, cero visual/olfatorio como refutación de localidad, spread 323x como anatómicamente blindado, `1,652x`, `36x`, `1,559x`, ventaja compleja puntual, tabla visual como novedad, “5/5 wins” de DualBrain y validación v10 sobre conectoma real cuando el fallback había dejado grafo vacío.

## 13. Orden siguiente

1. Mantener H4 fuerte NO MEDIDA.
2. Loader oficial y copia íntegra de `roi_dFF.pkl`.
3. `alignment_guard` con prueba negativa.
4. Features con identidad anatómica y normalización por animal.
5. Rerun por bouts/trials y nulls por bloques.
6. Null anatómico pareado y mapping ROI→FlyWire/cell type.
7. SparseLTC + silenciamientos.
8. Benchmark DBC3 con seeds y outputs persistidos.
9. No incorporar ComplexVectorLTC sin tarea de fase necesaria.
10. Versionar las seis fuentes Kaggle fuera de Git.

## 14. Cobertura y NO MEDIDO

La minería cruzó GitHub, brain-env, Kaggle y ClickUp; procesó decenas de documentos, commits, logs y mensajes canónicos. El corpus bruto sigue mayor: más de 125 documentos/mensajes en particiones con solapamiento, 58 adjuntos y threads truncados. Este informe es exhaustivo sobre los hallazgos canónicos identificados, no una afirmación de que cada mensaje/adjunto fue leído.

Pendientes reales: seis kernels fuera de Git, script Tabla 7 ausente, v2/erratum público no confirmado, loader H4, mapping anatómico, null anatómico H4, causalidad, benchmark SparseLTC→DBC3 y corpus completo Paper 2/FEP.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env + GitHub API + Kaggle API + ClickUp Search/Load
Rubrica: N/A (informe histórico y síntesis científica; no código ni despliegue)
N/A declarados: seguridad, deployment y testing de producto no aplican
Review externo: minería cruzada por dos agentes; no equivale a aprobación independiente del informe
Instrumento: GitHub branches/commits/files/logs; brain-env filesystem; Kaggle list; ClickUp index/load; evidencia enlazada arriba
Artefactos: `docs/agents/respuestas/2026-10-02-004-informe-maestro-historial-conectoma.md` + [Informe maestro del conectoma: Paper 1, nulls, SparseLTC, DualBrain, Kaggle e H4](https://app.clickup.com/90171457413/docs/2kza6fw5-17797)
NO MEDIDO: exhaustividad absoluta de todos los mensajes/adjuntos, loader H4 corregido, null anatómico H4, causalidad y benchmark biológico end-to-end