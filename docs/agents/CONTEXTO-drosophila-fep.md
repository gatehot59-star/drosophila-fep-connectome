# CONTEXTO VIVO · conectoma / FEP / papers

**Última actualización:** 2026-08-24 13:45 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Leer esto **antes** de responder cualquier cosa de este proyecto. Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-motor.md`. Índice de Docs: `INDICE-REAL-POR-ENUMERACION.md` (**parcial, 46 de ~65**). Entorno: `CONTEXTO-ENTORNO.md`.

---

## 0. 🚨 EL RELOJ · hay un plan con fechas y la primera vence el 30-ago

**Fuente: doc `6117`, «PLAN MAESTRO 10 SEMANAS · 24-ago al 8-nov 2026», 100/100.** Apareció en el barrido del 24-ago (resp 038) y **no estaba en ningún archivo de contexto**. Hoy es el 24-ago: **la S1 es esta semana.**

| # | El número que decide el éxito | Umbral | Si no llega |
|---|---|---|---|
| 1 | **Erratum en Zenodo** | **antes del 30-ago** | *«todo lo demás se lee con desconfianza»* |
| 2 | Motivos con 0/40 en la biblioteca | ≥ 3 (hoy hay **1**) | P3 se reagenda |
| 3 | Nulls del motor complejo | **40** (piso de `p` 0,20 → 0,0488) | sale de P4 |
| 4 | Papers subidos | ≥ 2 antes del 8-nov | *«el año no produjo publicación»* |

**Deadlines externos** (el `6117` dice haberlos verificado en vivo contra `arcprize.org` el 23-ago — **se re-verifican antes de planificar**): **2-nov** código a Kaggle · **8-nov** papers · resultados 4-dic. Premios 450 mil (Paper Prize) + 850 mil (ARC-AGI-3). **El código no necesita puntuar alto**, y puntean con **RHAE** (eficiencia de acción, no acierto): eso es lo que favorece estructura previa, y es la puerta real. **Ganar ARC no es el objetivo y decirlo distinto sería humo.**

**Las 10 semanas:** S1 cerrar lo público · S2 los nulls que faltan · S3 dos o tres motivos más · S4 mecanismo de aprendizaje · **S5 P1** · **S6 P2** · S7 agente ARC-AGI-3 · S8 P4 · S9 revisión externa · S10 cerrar y subir. Cada actividad tiene **criterio de aborto** escrito.

**Los 5 papers:** **P1** auditoría de connectomíca dinámica (evidencia **completa**, aborto: ninguno) · **P2** el 0,41% blindado (evidencia **completa**) · P3 biblioteca de primitivas (**1 de 3-4 motivos**) · P4 ARC (depende de P1 y P2) · P5 Paper 2 como resultado negativo. **P1 y P2 están en S5-S6 a propósito: si todo lo demás falla, esos dos salen igual, porque solo necesitan escritura.**

**El riesgo real del plan no es técnico:** son cinco entregables en diez semanas de **una persona**, y el taller ya tiene diez ideas sin ejecutar. El orden **es** la protección.

---

## 1. Son TRES papers más un motor. No mezclarlos nunca más

| Nombre | Qué es | Estado |
|---|---|---|
| **PAPER 1** | *Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*, Mendieta 2026a | Depositado en Zenodo 20-mar-2026. **El PDF lleva DOI placeholder `10.5281/zenodo.XXXXXXX`** |
| **PAPER 2** | *Topological Retention and Selective Convergence* — FEP, Markov blanket, Script R | Borrador. **No publicable como está**; va como resultado **negativo** (P5) o no va |
| **PATENTE** provisional | Texto congelado **antes** del erratum. Dos series RDI incompatibles (Tabla 6 vs 15). Doc `5717`: **la patente tiene razón, el FALSIFIED es un artefacto** | En pausa |
| **Motor** | SparseLTC / DualBrain, línea C99 + ESP32 | **El activo real.** Ver `CONTEXTO-motor.md` |

**El título real del Paper 1 termina en «Non-Trivial Temporal Amplification»**, no en «Temporal Amplification Under Dynamics Without Algorithmic Weight Optimization», que es el título que usa el borrador del erratum. Hay que corregirlo ahí.

**El producto en tres capas (doc `6117`):** (1) la **fuente de calibración** = el conectoma medido y sus priors · (2) el **motor** = de 15M aristas a 704 B · (3) **la biblioteca = el activo**, la hoja de datos de los 74xx, hoy con **un** motivo. **No se vende como «derivado del cerebro de la mosca»: se venden microsegundos, miliwatts y BOM.** El conectoma es el currículum, no el pitch.

**El arranque de esta línea es el 21-ago**, cuando llegó el PDF publicado (doc `5077`).

---

## 2. Lo que dice el PDF publicado, leído verbatim (2026-08-23)

- **§2.1:** `Density = 0.0074` → **la densidad mal SÍ está en el paper publicado**.
- **Abstract:** `reciprocity (36x over density expectation)` → el 36× también.
- **Table 7 = «Reciprocity by circuit type».** La tabla de RDI es la **Table 8**, con columnas `Real | CP | Z_CP | MS | Z_MS`, **sin columna Ratio**.
- **El 1.559× no aparece** en Abstract, §1.3, §3.4 ni §4.1. Doc `5757`: es **artefacto de división por casi cero** y aparece **9 veces**.
- **§2.4 ya declara el guard de tautología:** *"Net RDI at 1-hop is exactly invariant under CP null (sigma = 0)"*, derivado analíticamente.
- **§1.2 cita a Betzel et al. [2026] correctamente.**
- Nulls declarados: MS `N = 100`, CP `N = 5–10`.
- **La causa del bug de densidad está identificada (doc `5117`):** el paper usa **«synapses» en el abstract y «connections» en §2.1 para el mismo número**.
- **«RDI» nombra DOS métricas distintas (doc `6017`):** el paper usa 3 modalidades con filtro `flow == afferent` → **3 pares**; la corrida del 19+19 usó 4 modalidades sin filtro → **6 pares**. **Esa era la causa de la discrepancia, no un desfasaje.** Y `ORN` tiene **0 filas** en la v3.1.0: la rama `['olfactory','ORN']` del código es **inerte**.

---

## 3. VALIDADO (conteos puros o con null que preserva grado y modularidad)

| Hallazgo | Número | Instrumento |
|---|---|---|
| Densidad real del grafo | 7,854×10⁻⁴ | igraph + propio |
| **Reciprocidad** | 26,60% · 4.014.518 aristas · **20,59× vs CP, 0/40** ← **el número a publicar**, no 47,3× ni 338,8× | 40 nulls CP (`6057`) |
| Acceso motor corregido | 4 enriquecidas / 4 depletadas (el paper dice 0 y 7) | conteo puro |
| Sensorial → KC directo | **0** en el real, 40/40 nulls MS dan 1.533–2.640 | nulls MS |
| Fracción plástica | 4,045% neuronas · 0,41% conexiones | conteo puro |
| Ley de Dale | **0 mixtas de 138.005** (96.672 excitatorias puras, 41.333 inhibitorias puras) | conteo puro |
| **`KC→MBON`** | 62.261 · **7,81× vs CP, 0/40** ← sobrevive **contra mi predicción** | 40 nulls CP (`6057`) |
| **`DAN→KC`** | 47.404 · **8,71× vs CP, 0/40** → firma presináptica. Es 23,5× `DAN→MBON` | 40 nulls CP |
| **`KC→KC`** | 293.762 · **7,26× vs CP, 0/40** | 40 nulls CP |
| `ALPN→KC` | 27.848 · 1,70× vs CP (débil pero 0/40) | 40 nulls CP |
| Script R completo | **30/30 valores** reproducidos, máx. 5×10⁻⁵ | 4 instrumentos independientes |
| Circuito de escape | 9,1× LC4→GF · LC6→GF = 0 aristas · 0/40 | 40 nulls CP |
| Escape compilado | ganancia **40×** vs detector vecino no cableado | motor propio |
| **Los 40 nulls sobre las 12 clases** | **0/40 en 12/12.** El centro de aprendizaje está **BLINDADO** | doc `5937`, 100/100 |
| **RDI dinámico** | **z = 197.** Es el resultado **más fuerte** del expediente | doc `5977`, 100/100 |
| **Replicación cruzada JS/Python** | 46,88× vs 47,27×; el 0,8% lo explica la convención de swaps. **La evidencia viaja byte-idéntica** | doc `5977` |
| **Priors medidos, listos para exportar** | peso **lognormal(0,7034 , 0,8883)** · `inh_frac` por super_class de **0,068** a **0,513** · grado entrante **CV 1,469** (máx 10.356) · fuerza **CV 2,402** (máx 69.948) · **tabla de 95 pares de bloques** | doc `6057` |

---

## 4. REFUTADO / NO TESTEABLE (cada uno con el número que lo tumbó)

| Claim | Qué lo tumbó |
|---|---|
| **«jerarquía de ruteo: 991× corregido a 283,2×, y listo»** | **🚨 NO TESTEABLE contra el null fuerte (doc `6057`).** Las 8 clases dan `sd = 0,0` **exacto** y `ratio_CP = 1,000×`, 40/40. Es **cantidad conservada** bajo CP: el null baraja destinos dentro de bloques definidos por super_class, y el grupo MOTOR **está definido por la misma super_class**. El conteo no puede cambiar ni en una arista. **El 283,2× es contra grado preservado; contra modularidad es inmedible.** Idem `sensory→KC` y `MBON→motor`. **22,2 min de cuota para medir nada.** Arreglo: null de **tripartición** (sensorial/interno/motor) |
| **«el desfasaje de un paso explica la discrepancia a t=60»** (mío) | **REFUTADO por lectura del código (doc `6017`):** `res[t] = h.copy()` va **después** del update en los dos loops. **No hay desfasaje.** La causa real eran **dos métricas con el mismo nombre** (3 vs 6 pares). **Y la hipótesis refutada sigue escrita en el `docs/ERRATUM.md` público** |
| **«el erratum está listo para subir a Zenodo»** | **E3 corrige una «Table 7» con columna Ratio y 1.559× que NO existen en el PDF publicado.** ⚠️ **Contradicción abierta:** el doc `6117` dice que el erratum está escrito y commiteado con 7 puntos y que **falta un solo dato (los dos DOI)**. Los dos no pueden ser ciertos. **Abrir `docs/ERRATUM.md` y compararlo con el PDF: es lectura, no cómputo** |
| «el Paper 1 evita la densidad contaminada» | falso: §2.1 dice `Density = 0.0074` y el Abstract dice 36× |
| «el Paper 1 cita mal a Barsotti» | §1.2 cita **Betzel** correctamente. Sin confirmar en la bibliografía |
| «el guard de tautología es aporte propio» | §2.4 del paper ya lo declara y lo deriva |
| «1.559× de amplificación» | denominador 0,0005 ± 0,0003: va de 1.041× a 4.164× dentro de 1σ. Doc `5757`: **artefacto, 9 apariciones** |
| «R = 1,31, retención selectiva» | cruza 1 en las tres modalidades según normalización (visual 1,878 → 0,811) |
| «0 clases enriquecidas» | con la densidad correcta son 4 y 4 |
| «**4 de 9 clases pasan a enriquecidas**» (mío) | **RETIRADO (doc `5177`):** la expectativa de la Tabla 5 **no es de densidad** (`Exp_m/Exp_g ∈ [6,68 , 8,82]` vs `N_m/N_g = 6,52`). Medí la densidad y concluí sobre una tabla cuya expectativa no había inspeccionado: **E-01 con una rúbrica de 100/100 puesta** |
| «reciprocidad 36×» | 338,8× vs densidad, 47,3× vs grado, **20,59× vs modularidad**. Y con la densidad de Lin (`0,000161`) el 36× es **1.652×** (doc `5117`) |
| «τ_m = 8,4 ms» | la constante correcta es 7,89 ms. Error 6,47% |
| col-norm «respeta la varianza local» | lleva el CV de 2,402 a **cero**; la global lo preserva entero |
| **Tabla 7 reproducible** | **doc `6017`: 4 particiones con la definición EXACTA del código y ninguna reproduce la FORMA** (la Tabla 7 baja de 0,687 a 0,630 y después sube; A sube monótona, C baja, B y D planas). **Y los 6 valores no existen en ninguno de los 29 notebooks: falta el instrumento, no el esfuerzo.** Además un valor alto a t=15 es **imposible** con esa partición (las 3 modalidades caen en el bin `sensory`) |
| «hace falta una SNN para latencias» | la métrica al 10% del pico da mechano 4 < gust 5 < visual 6 < olf 10 |
| «el control lineal descarta saturación» | clipea: `max|h| = 2,0000` exacto en 2 de 3 modalidades |
| «la topología explica la función» | el escape compilado da selectividad temporal 1,04× |
| «la entropía baja distingue biología» | los nulls bajan más: dH −9,79 vs −2,88, z = 18,1. Doc `5777`: la entropía **no** distingue 12/12; **la FORMA sí, 7/12** |
| «visual es la vía con menos acceso motor» | **no sobrevive**: es **olfactory** (doc `5937`) |
| «sinapsis vs conexiones» explica el bug de densidad | **confirmado como la causa** (doc `5117`). Sinapsis reales: 54.492.922 |
| «Therianos me refuta» (entusiasmo propio) | **retirado:** Lin mide reciprocidad **13,8%** en el adulto y Therianos usa conectoma **larval** → el 26,09% **coincide con el cerebro equivocado** (doc `5117`) |
| «el `temporal RDI` es frágil» (mío) | **error de eje (doc `5977`).** Metí el resultado más fuerte (`z=197`) en la columna de frágil. **El eje no es estático vs dinámico: es CONTRA QUÉ NULL.** Lo que falla contra CP **no está refutado: la modularidad lo explica** |
| «KC→MBON cae contra CP» (predicción mía declarada antes de correr) | **refutada: sobrevive con 7,81×, 0/40.** Acerté la mitad y **por el motivo equivocado** (doc `6057`) |

---

## 5. NO MEDIDO / pendiente, declarado

1. **`docs/ERRATUM.md` no se abrió.** Ahí vive la contradicción de §4 y la hipótesis refutada del desfasaje. **Es la lectura más barata y más urgente que queda.**
2. **Conclusiones, bibliografía y Material Suplementario del PDF del Paper 1:** la extracción se cortó en §5.
3. **De dónde sale el DOI `10.5281/zenodo.19136948`:** no está en el PDF (que lleva `XXXXXXX` literal) y **el repo da 404** (doc `5077`).
4. Los adjuntos 1, 3 y 7 (patente, Script R, PDF de Gemini de 101 pág.) no se localizaron por nombre. **No se afirma que no estén.**
5. Los HTML de Arena devuelven markup de página, no conversación.
6. `titan-paper-dualbrain` y `notebookceb82767da`: logs sin leer.
7. La hipótesis del 96% fijo: **sin testear** sobre SparseLTC. Ver `CONTEXTO-motor.md` §6. **La deuda más vieja del proyecto.**
8. **El script original de la Tabla 7: no está en el corpus.** Cero de 6 valores en 29 notebooks (doc `6017`). Puede estar en Colab, en local o en un notebook borrado.
9. **Null de tripartición: no corrió.** Sin él la jerarquía de ruteo no se publica.
10. **Faltan 21 nulls** para que el test global de los 12 pares llegue a `p<0,05`. Hoy el real sale **1º de 20 (0/19)** pero el piso a dos colas con 19 nulls es **0,10**, y la dirección es post-hoc. **~30 min** (doc `5957`).
11. **El barrido de Docs está al 71%:** 46 de ~65. **9 IDs pendientes en la zona del conectoma** (`6157 6177 6197 6217 6237 6257 6277 6317 6337`), ~15 en icca-engine, ~50 sin barrer entre `3637` y `4717`, MUDH/AURA del 14-ago sin tocar. **22 de los 32 de la zona D están identificados por TÍTULO, no por lectura.** Los docs `6057` y `6077` llegaron **truncados**.
12. **Las fechas de ARC del §0 no las verifiqué yo:** vienen del `6117`. **Un deadline de premio se re-verifica antes de planificar sobre él.**

---

## 6. Decisiones esperando a Abraham

1. **🚨 Subir el erratum a Zenodo antes del 30-ago.** Es el umbral #1 de los cuatro. Falta: los dos DOI (versión y concepto), que son dato tuyo. **Criterio de aborto del propio plan: si el PDF publicado difiere del borrador en más de dos números, PARAR y re-auditar. Un erratum con un error es peor que no tener erratum.**
2. **⭐ El `README.md` público tiene la clasificación equivocada** (doc `5977`): el `temporal RDI` (`z=197`, el más fuerte) figura como **frágil** en un repo que va a citar un preprint con DOI.
3. **⭐ El `docs/ERRATUM.md` público tiene mi hipótesis del desfasaje escrita como explicación probable, y está REFUTADA** (doc `6017`). Decime y la reemplazo por lo medido.
4. **⭐ Los bugs del Script R viven DENTRO del verificador V-K** que el manuscrito cita como garantía de reproducibilidad (doc `5637`, **14 citas con número de línea**). `normalize_global_spectral` cae en silencio a Frobenius con el mismo nombre → el `SR = 0.990000` exacto es **la cota, no el autovalor**. `entropy_kde` devuelve `0.0000` en vez de `nan`. **Se arreglan en el V-K, no en el R.** Parchear antes de publicar, o publicar declarando la limitación.
5. **Los tres corchetes del erratum `5157`:** están sin rellenar **a propósito** y necesitan **una corrida tuya**. Sin ellos la v2 no se publica.
6. **Buscar el script de la Tabla 7 donde sea que esté.** Si aparece, se corre contra los nulls en una hora y el E7 pasa a ser reproducción de verdad. Si no aparece, **es un resultado no reproducible y hay que decirlo en Limitaciones**, porque un revisor con el parquet llega a la misma pared.
7. **Mergear el PR #1**, o decir qué le falta. 13 archivos, y el review automático sin hallazgos es **NO MEDIDO, no aprobación**.
8. **El barrido: ¿sigo con los 9 IDs del conectoma (lotes 2 y 3) o abro las otras zonas?** La pregunta original es de la resp 031, se perdió en un corte de instancia, y el lote 1 ya cerró.
9. Subir los 7 `.py` que quedan del container, y los 4 JSON de evidencia (deuda W-01).
10. El **clip de la config (e)**: subirlo y re-correr. Si diverge, también es resultado.
11. Org `Mendieta-Architect` o aceptar la URL `gatehot59-star` en el erratum.

---

## 7. Correcciones sobre el propio entorno (medidas)

- **El container NO es efímero.** `/workspace` persiste con el parquet (100.804.642 B, md5 `3d802fd542b5d18570ba1ba0bb0abed9`), el TSV (31.718.505 B, md5 `719904abad876c68ace1b5690c9b9b63`), los 17 `.py` y `kaggle.json`.
- **`nexus.db` no existe.** Todo lo que se declaró «cargado en la base» no está. Este repo es la memoria.
- **`git` no está instalado** en el container y no hay token: todo pasa por la integración de GitHub.
- **Python 3.12.14, Node 24.18.0, R 4.5.3** sí están.
- **Los adjuntos PDF del workspace SÍ se leen.** Los HTML de Arena, no. Y varios están **duplicados**.
- **Los Docs del workspace son ENUMERABLES:** IDs de página secuenciales, **paso 20**, prefijo `2kza6fw5-`, cargables por ID sin que Abraham pegue nada. **No existe herramienta de «listar docs»: el enumerador es el propio espacio de IDs.** Límite medido: **5 Docs completos no entran en una ventana** (con uno grande adentro es 4 + 1). → `INDICE-REAL-POR-ENUMERACION.md`.
- **El resto del entorno se re-mide, no se recuerda:** `CONTEXTO-ENTORNO.md`, §12 al 24-ago 12:15.

---

## 8. Modos de falla propios de esta línea, y cada uno ya costó

**1 · Una lista hecha de citas solo contiene lo que alguien citó.** El `INDICE-DE-ENLACES.md` se armó cosechando el chat; creí que tenía 30 de 30 y tenía **30 de los citados**. El doc `5177` — 100/100, que retira tres afirmaciones mías — **no estaba**. Cuando existe un **enumerador**, la lista se arma con el enumerador. Y **un índice parcial se reporta con su fracción**, nunca como cierre (la resp 036 lo reportó como cierre citando el archivo que dice «PARCIAL» en su tercera línea).

**2 · Un null cuyos invariantes incluyen la cantidad medida no es un control, es un espejo.** Antes de reportar cualquier ratio: **si `sd(null) == 0`, reportar NO TESTEABLE**, no `1,000×`. Son cuatro líneas y habrían ahorrado 22,2 minutos de cuota (doc `6057`).

**3 · Una explicación que encaja no es una explicación medida.** Escribí «desfasaje de un paso» en un documento destinado a una publicación con DOI **sin leer el código que estaba explicando**, y el código estaba en el container desde el día anterior: leerlo costó dos llamadas. **Cuando una discrepancia numérica tiene una explicación elegante, buscar el código antes de escribirla** (doc `6017`).

**4 · Un archivo que no abrí en este turno no recibe veredicto de vigencia.** «Sigue vigente» es una medición, no un default. Si no lo leí, el estado es **NO MEDIDO** (resp 037).
