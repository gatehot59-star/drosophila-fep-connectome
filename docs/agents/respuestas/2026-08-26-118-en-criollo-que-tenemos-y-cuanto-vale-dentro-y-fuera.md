# 118 · En criollo: qué tenemos en manos, dónde estamos, y cuánto vale dentro y fuera de la competencia

**Fecha:** 2026-08-26 · rama `titan/twohop-nulls`

---

## 0. Primero mi propio fallo, porque si no lo nombro se repite

Abraham preguntó **dos veces** lo mismo: qué tenemos objetivamente y cuál es el potencial dentro y fuera de la competencia. Yo contesté con **open source de Kaggle y estado del container**, que es material de hace diez entregas.

No fue falta de datos. Fue **el error del sujeto equivocado (E-01)** en su versión más barata: agarré las últimas herramientas que había usado y contesté con su salida en vez de contestar la pregunta. Reusar el aparato ya armado **sobre el objetivo equivocado** está literalmente escrito en mi propia disciplina, y lo hice igual.

No cobro por confesarlo. Va acá porque el registro sirve, la disculpa no.

---

## 1. Qué tenemos en manos, sin épica

Cuatro cosas distintas que se venían tratando como una sola. Separarlas es la mitad del valor de este documento.

### A. Un instrumento científico serio
`motor_v2.py` sobre el conectoma real. Medido, no declarado:
- v1 y v2 son **la misma física** (desvío exacto 0 en el A/B controlado sobre el conectoma real).
- 39 nulls temporales CP cerrados en GPU, 4 shards, **peor desvío 2,22e-16** contra CPU.
- CPU 390,5 minutos vs GPU 5-7 minutos por shard: el circuito de cómputo quedó probado punta a punta.
- `rankdata` corregido, testeado y mutation-tested en CPU; **no portable a cupy** tal cual, y la versión rápida difiere con NaN, así que no entra al motor.

**Valor real:** es un instrumento con guards, con potencia estadística declarada y con nulls anatómicos y temporales. Eso es raro y es capital.

**Límite honesto:** un instrumento no es un hallazgo. Y el test global del titular dio **p=0,25 con potencia suficiente**: no significativo. Eso no se tapa.

### B. Un paper publicado con una deuda pública
Zenodo sigue en **v1.0**. El erratum existe, está escrito, y **no está depositado**.
- El overflow int32 no es nota al pie: mueve la Tabla 5 y la reciprocidad (**26,6003%** exacto) y la densidad (**0,000785197**).
- El cruce de signo temporal en `t100` replica en tres rejillas distintas: eso sí es sólido.

**Valor real:** credibilidad y antecedente. **Riesgo real:** hoy es un **pasivo**, no un activo. Lo público afirma cosas que lo privado ya retiró. Cualquiera que chequee lo encuentra, y lo encuentra sin que vos lo hayas contado primero.

### C. Un producto embebido que corre en fierro real
DualBrain C99: **1.336 bytes de `.text` medidos en target**. SparseLTC con 138.639 neuronas que no entrena. El brazo `W` **refutado** (no salva la vía rápida cableada). `MultiCue` con contraindicación medida ante referencias simultáneas.

**Valor real:** esta es la pieza más vendible de todo el expediente, y no es el paper. Es control neuromórfico sin entrenamiento, sin LLM, en microcontrolador, con números medidos en hardware.

### D. Un método transferible
117 respuestas commiteadas, bitácora de hipótesis muertas, nulls antes de titulares, W-01 (independencia del instrumento), tres estados bien/mal/NO MEDIDO.

**Valor real:** es exactamente el objetivo de fondo: algo **cedible a un aprendiz**. Y es lo único que no depende de que un experimento salga bien.

---

## 2. Dónde estamos, objetivamente

| dimensión | estado medido |
|---|---|
| aparato científico privado | **fuerte** |
| sincronización pública | **atrasada** (Zenodo v1.0) |
| entrada a ARC | **cero** · `userHasEntered=false` × 3 tracks × 2 cuentas |
| agente ARC en código | **cero** · existe el diseño y el artifact, no el `my_agent.py` |
| score oficial ARC | **cero** |
| infraestructura de cómputo | **probada** · Kaggle + GPU + sharding + 4 slots concurrentes |

**Traducción:** no estamos compitiendo. Estamos en **precompetencia con un muy buen taller**.

---

## 3. Potencial DENTRO de la competencia

### El terreno, medido de fuentes oficiales
- Humanos **100%** en ARC-AGI-3. Frontier **por debajo de 1%** (Gemini 3.1 Pro 0,37%; GPT-5.4 0,26%).
- Milestone **#1 ya se pagó** ($37,5K, corrió hasta el 30 de junio). **Milestone #2 cierra el 30 de septiembre**, $37,5K garantizados.
- Submissions **2-nov**. Paper track **9-nov** por Kaggle (arcprize dice 8; gana Kaggle, que es donde se sube). Resultados **4-dic**.
- Vara real de la tesis "sin pretraining": **CompressARC ~4% cobró $5K**. **TRM con 7M de parámetros ~8% cobró $50K**. El top de Kaggle 2025 fue 24%. El Grand Prize pide 85% **más** eficiencia (~$2,50/tarea en 2025).
- En el leaderboard comunitario hay un **85,1% self-reported (NOOA, $332)** sobre el demo público, **no verificado** por ARC Prize. O sea: no es la vara oficial, es ruido de marketing.

### Qué de lo nuestro entra de verdad
Entra: **priors estructurales**, el `gate` medido como árbitro reflejo/memoria, **τ heterogénea** como memoria multi-horizonte, y la tesis de **no entrenar todo**, que ya tiene análogo premiado.

No entra todavía: **planificación, goal-setting, world model explícito**. Y eso es la mitad de lo que ARC-AGI-3 mide.

### Veredicto
- **ARC-AGI-2: no.** Otra cancha, stacks hiperoptimizados. No gastar ahí.
- **ARC-AGI-3 Milestone #2 (30-sep): improbable como podio**, faltan 35 días y no hay agente en código. Sí vale entrar: la entrada no cuesta y da existencia oficial.
- **Paper Prize: acá está el valor esperado real.** $75K de Top Paper garantizados, más un pool de $375K para papers >4,5. La rúbrica premia Theory, Progress, Completeness, Universality y Novelty, y ahí el expediente es fuerte de verdad.

**La trampa aritmética, y es dura:** el paper tiene que estar ligado a una submission real, y **Accuracy pesa igual que las otras cinco**. Con score 0, el pool >4,5 es matemáticamente casi imposible. **Un agente random alcanza para existir, no para cobrar el pool.**

---

## 4. Potencial FUERA de la competencia

Acá está la mayor parte del valor, y creo que se estuvo mirando para el lado equivocado.

1. **DualBrain embebido.** Un controlador que decide sin entrenar, con 1.336 bytes de `.text` medidos en target, en un mercado donde todo se resuelve tirando GPU. Es la única línea plausiblemente **patentable** del expediente (los hallazgos del conectoma no lo son: son descubrimientos).
2. **El instrumento como servicio.** Motor + nulls + guards es un aparato de peritaje reusable. Sirve para cualquier grafo biológico, no solo para *Drosophila*.
3. **El método como producto cedible.** La bitácora de hipótesis muertas es lo que hace transferible el resto. Es el fin declarado, no un subproducto.
4. **icca-engine.com** como canal: el cómputo se regala, el precio es leer el corpus.
5. **La tercera línea ("ingeniería inversa de cerebros no escaneados")** tiene la mejor idea nueva del lote, pero está **calibrada sobre densidad y reciprocidad ya retiradas**. Recalibrar o no vale nada.

**Mi take sin diplomacia:** afuera vale más que adentro. La competencia no es el negocio, es **el forzador de plazo** que vuelve legible lo de afuera. Un paper de ARC con submission real es la mejor carta de presentación que este expediente puede tener, y sirve igual si no gana un peso.

---

## 5. El riesgo número uno, y no es técnico

**Abrir un frente más.** Hay cuatro líneas vivas, dos papers inconclusos, un erratum sin depositar, tres tracks sin entrar y un agente sin escribir. El expediente no tiene un problema de capacidad: tiene un problema de **cierre**.

Priorizar es donde más daño puedo hacer. Así que priorizo:

1. **Depositar el erratum en Zenodo.** Cheap, un día, y saca el único pasivo reputacional. **Nada de cómputo nuevo antes de esto.**
2. **Tres clicks tuyos** en los tres tracks de Kaggle. Sin eso no existís oficialmente.
3. **`my_agent.py` mínimo que puntúe > 0.** No elegante: que puntúe. Sin score, el pool grande se cierra solo.
4. **Paper del producto para ARC**, no el del conectoma reciclado.
5. Recién ahí decidir cuál de los dos papers inconclusos se termina.

Nada más. Todo lo demás que aparezca hasta el 9 de noviembre es distracción, incluida cualquier medición nueva del conectoma.

---

## 6. NO MEDIDO

- **No leí las reglas oficiales renderizadas de Kaggle** de los tres tracks (son JS). Hay vía: el navegador del gateway. No la lancé en este turno.
- **No verifiqué en este turno el estado de `main`** contra `titan/twohop-nulls`.
- **No pude confirmar procesos vivos en `brain-env`**: el container no tiene `ps` ni `pgrep`, y las lecturas de `/proc` por script fallaron por el shell del gateway. Lo único medido fue **load 3,56**. O sea: **NO MEDIDO**, no "no hay nada corriendo".
- **No estimé el costo en horas** de un agente mínimo que puntúe > 0. Sin eso, mi "improbable para el 30-sep" es juicio, no medición.
- **No revisé el reparto exacto del Milestone #2** ni la fórmula del pool >4,5: no la publican.
