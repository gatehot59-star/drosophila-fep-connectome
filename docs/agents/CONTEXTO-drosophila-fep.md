# CONTEXTO VIVO · conectoma / FEP / papers

**Última actualización:** 2026-08-24 12:55 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Leer esto **antes** de responder cualquier cosa de este proyecto. Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-motor.md`. Índice de Docs: `INDICE-REAL-POR-ENUMERACION.md` (**parcial, 41 de ~65**). Entorno: `CONTEXTO-ENTORNO.md`.

> **Nota de la resp 037:** este archivo estuvo fechado **23-ago 21:35** hasta las 12:55 del 24-ago, y en la resp 036 lo declaré «vigente» **sin abrirlo**. Era falso: le faltaba todo lo que destapó el barrido por enumeración de Docs. Un archivo que no se abrió en el turno no recibe veredicto de vigencia.

---

## 1. Son TRES papers más un motor. No mezclarlos nunca más

| Nombre | Qué es | Estado |
|---|---|---|
| **PAPER 1** | *Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*, Mendieta 2026a | Depositado en Zenodo 20-mar-2026. **El PDF lleva DOI placeholder `10.5281/zenodo.XXXXXXX`** |
| **PAPER 2** | *Topological Retention and Selective Convergence* — FEP, Markov blanket, Script R | Borrador. **No publicable como está** |
| **PATENTE** provisional | Texto congelado **antes** del erratum. Dos series RDI incompatibles (Tabla 6 vs 15). Doc `5717`: **la patente tiene razón, el FALSIFIED es un artefacto** | En pausa |
| **Motor** | SparseLTC / DualBrain, línea C99 + ESP32 | **El activo real.** Ver `CONTEXTO-motor.md` |

**El título real del Paper 1 termina en «Non-Trivial Temporal Amplification»**, no en «Temporal Amplification Under Dynamics Without Algorithmic Weight Optimization», que es el título que usa el borrador del erratum. Hay que corregirlo ahí.

**El arranque de esta línea es el 21-ago**, cuando llegó el PDF publicado (doc `5077`). Todo lo anterior del workspace es MUDH / MUDH-Mobile / infraestructura, y son **otras líneas**.

---

## 2. Lo que dice el PDF publicado, leído verbatim (2026-08-23)

Datos duros del propio archivo, para no volver a suponer:

- **§2.1:** `Density = 0.0074` → **la densidad mal SÍ está en el paper publicado**.
- **Abstract:** `reciprocity (36x over density expectation)` → el 36× también.
- **Table 7 = «Reciprocity by circuit type».** La tabla de RDI es la **Table 8**, con columnas `Real | CP | Z_CP | MS | Z_MS`, **sin columna Ratio**.
- **El 1.559× no aparece** en Abstract, §1.3, §3.4 ni §4.1. Doc `5757`: es **artefacto de división por casi cero** y aparece **9 veces**.
- **§2.4 ya declara el guard de tautología:** *"Net RDI at 1-hop is exactly invariant under CP null (sigma = 0)"*, derivado analíticamente.
- **§1.2 cita a Betzel et al. [2026] correctamente.**
- Nulls declarados: MS `N = 100`, CP `N = 5–10`.
- **La causa del bug de densidad está identificada (doc `5117`):** el paper usa **«synapses» en el abstract y «connections» en §2.1 para el mismo número**.

---

## 3. VALIDADO (conteos puros o con null que preserva grado y modularidad)

| Hallazgo | Número | Instrumento |
|---|---|---|
| Densidad real del grafo | 7,854×10⁻⁴ | igraph + propio |
| Reciprocidad | 26,60% · 4.014.518 aristas · 20,6× vs CP | 40 nulls, 0/40 |
| Acceso motor corregido | 4 enriquecidas / 4 depletadas (el paper dice 0 y 7) | conteo puro |
| Sensorial → KC directo | **0** en el real, 40/40 nulls dan 1.533–2.640 | nulls CP |
| Fracción plástica | 4,045% neuronas · 0,41% conexiones | conteo puro |
| Ley de Dale | 0 mixtas de 138.005 | conteo puro |
| `DAN→KC` vs `DAN→MBON` | 23,5× · 8,71× sobre CP, 0/40 → firma presináptica | nulls CP |
| Script R completo | **30/30 valores** reproducidos, máx. 5×10⁻⁵ | 4 instrumentos independientes |
| Circuito de escape | 9,1× LC4→GF · LC6→GF = 0 aristas · 0/40 | 40 nulls CP |
| Escape compilado | ganancia **40×** vs detector vecino no cableado | motor propio |
| **Los 40 nulls sobre las 12 clases** | **0/40 en 12/12.** El centro de aprendizaje está **BLINDADO** | doc `5937`, 100/100 |
| **RDI dinámico** | **z = 197.** Es el resultado **más fuerte** del expediente | doc `5977`, 100/100 |
| **Replicación cruzada JS/Python** | 46,88× vs 47,27×; el 0,8% lo explica la convención de swaps. **La evidencia viaja byte-idéntica** | doc `5977` |

---

## 4. REFUTADO (cada uno con el número que lo tumbó)

| Claim | Qué lo tumbó |
|---|---|
| **«el erratum está listo para subir a Zenodo»** | **E3 corrige una «Table 7» con columna Ratio y 1.559× que NO existen en el PDF publicado.** Esos elementos son de otro documento. El erratum no se puede subir así |
| «el Paper 1 evita la densidad contaminada» | falso: §2.1 dice `Density = 0.0074` y el Abstract dice 36× |
| «el Paper 1 cita mal a Barsotti» | §1.2 cita **Betzel** correctamente. Sin confirmar en la bibliografía |
| «el guard de tautología es aporte propio» | §2.4 del paper ya lo declara y lo deriva |
| «1.559× de amplificación» | denominador 0,0005 ± 0,0003: va de 1.041× a 4.164× dentro de 1σ, e indefinido a 2σ. Doc `5757`: **artefacto, 9 apariciones** |
| «R = 1,31, retención selectiva» | cruza 1 en las tres modalidades según normalización (visual 1,878 → 0,811) |
| «0 clases enriquecidas» | con la densidad correcta son 4 y 4 |
| «**4 de 9 clases pasan a enriquecidas**» (mío) | **RETIRADO en el doc `5177`:** la expectativa de la Tabla 5 **no es de densidad** (`Exp_m/Exp_g ∈ [6,68 , 8,82]` vs `N_m/N_g = 6,52`). Medí la densidad y concluí sobre una tabla cuya expectativa no había inspeccionado: **E-01 con una rúbrica de 100/100 puesta** |
| «reciprocidad 36×» | era 338,8× contra densidad, 47,3× contra grado preservado. **Y con la densidad de Lin (Nature 2024, `0,000161`) es `1.652×`: el 36× no sobrevive** (doc `5117`) |
| «τ_m = 8,4 ms» | la constante correcta es 7,89 ms. Error 6,47% |
| col-norm «respeta la varianza local» | lleva el CV de 2,402 a **cero**; la global lo preserva entero |
| Tabla 7 reproducible | 5 variantes × 2 precisiones, ninguna reproduce la forma. Doc `6037`: **no es reproducible con el código archivado** |
| «hace falta una SNN para latencias» | la métrica al 10% del pico da mechano 4 < gust 5 < visual 6 < olf 10 |
| «el control lineal descarta saturación» | clipea: `max|h| = 2,0000` exacto en 2 de 3 modalidades |
| «la topología explica la función» | el escape compilado da selectividad temporal 1,04× |
| «la entropía baja distingue biología» | los nulls bajan más: dH −9,79 vs −2,88, z = 18,1. Doc `5777`: la entropía **no** distingue 12/12; **la FORMA sí, 7/12** |
| jerarquía de ruteo 991× | corregida a **283,2×**; el más depletado es **olfactory**, no visual (doc `5937`) |
| «sinapsis vs conexiones» explica el bug de densidad | **YA NO: el doc `5117` lo confirma como la causa.** El paper usa los dos términos para el mismo número. Sinapsis reales: 54.492.922 |
| «Therianos me refuta» (entusiasmo propio) | **retirado:** Lin mide reciprocidad **13,8%** en el adulto. Therianos usa conectoma **larval**, o sea que el 26,09% **coincide con el cerebro equivocado** (doc `5117`) |
| «el `temporal RDI` es frágil» (mío) | **error de eje, doc `5977`.** Metí el resultado más fuerte (`z=197`) en la columna de frágil. **El eje no es estático vs dinámico: es CONTRA QUÉ NULL.** Lo que falla contra CP **no está refutado: la modularidad lo explica** |

---

## 5. NO MEDIDO / pendiente, declarado

1. **Conclusiones, bibliografía y Material Suplementario del PDF del Paper 1:** la extracción se cortó en §5. **Leerlo antes de tocar el erratum.**
2. **De dónde sale el DOI `10.5281/zenodo.19136948`:** no está en el PDF (que lleva `XXXXXXX` literal) y **el repo da 404** (doc `5077`).
3. Los adjuntos 1, 3 y 7 (patente, Script R, PDF de Gemini de 101 pág.) no se localizaron por nombre en la última pasada. **No se afirma que no estén.**
4. Los HTML de Arena devuelven markup de página, no conversación. Sin verificar si el texto vive en algún payload del bundle.
5. `titan-paper-dualbrain` y `notebookceb82767da`: logs sin leer.
6. La hipótesis del 96% fijo: **sin testear** sobre SparseLTC. Ver `CONTEXTO-motor.md` §6.2. **Es la deuda más vieja del proyecto.**
7. El script original de la Tabla 7 del Paper 2: no encontrado.
8. **Reciprocidad y KC→MBON nunca probados contra CP:** los 40 nulls son **MS** (docs `5937`, `5977`).
9. **Faltan 21 nulls** para que el test global de los 12 pares llegue a `p<0,05`. Hoy el real sale **1º de 20 (0/19)** pero el piso a dos colas con 19 nulls es **0,10**, y la dirección es post-hoc. **~30 min de máquina** (doc `5957`).
10. **El barrido de Docs está al ~63%:** 41 de ~65. **14 IDs pendientes en la zona del conectoma** (`6017 6057 6077 6117 6137 6157 6177 6197 6217 6237 6257 6277 6317 6337`), ~15 en icca-engine, ~50 sin barrer entre `3637` y `4717`, MUDH/AURA del 14-ago sin tocar. **22 de los 27 de la zona D están identificados por TÍTULO, no por lectura.**

---

## 6. Decisiones esperando a Abraham

1. **⭐ El `README.md` público tiene la clasificación equivocada** (doc `5977`): el `temporal RDI`, que es el resultado **más fuerte** (`z=197`), figura como **frágil** en un repo que va a citar un preprint con DOI. **Es lo único público y equivocado del expediente.**
2. **⭐ Los bugs del Script R viven DENTRO del verificador V-K** que el manuscrito cita como garantía de reproducibilidad (doc `5637`, **14 citas con número de línea**). `normalize_global_spectral` cae en silencio a Frobenius con el mismo nombre → el `SR = 0.990000` exacto es **la cota, no el autovalor**. `entropy_kde` devuelve `0.0000` en vez de `nan`. **Se arreglan en el V-K, no en el R.** Decisión: parchear antes de publicar, o publicar declarando la limitación.
3. **Los tres corchetes del erratum `5157`:** están sin rellenar **a propósito** y necesitan **una corrida del código de Abraham**. Sin ellos la v2 no se publica.
4. **Reescribir el erratum E3** contra el documento que realmente contiene el 1.559×, o borrar E3. Hoy apunta a una tabla inexistente.
5. **Conseguir el DOI real** del depósito de Zenodo.
6. **Mergear el PR #1**, o decir qué le falta.
7. **El barrido de Docs: ¿acotado a la línea del conectoma (los 14 IDs pendientes) o el espacio completo incluyendo MUDH y AURA?** Esta pregunta se hizo en la resp 031 y **se perdió en el corte de instancia**; la resp 036 la archivó mal como «cerrada».
8. Subir los 7 `.py` que quedan del container.
9. El **clip de la config (e)**: subirlo y re-correr. Si diverge, también es resultado.
10. Org `Mendieta-Architect` o aceptar la URL `gatehot59-star` en el erratum.

---

## 7. Correcciones sobre el propio entorno (medidas)

- **El container NO es efímero.** `/workspace` persiste con el parquet (100.804.642 B), el TSV (31.718.505 B), los 17 `.py` y `kaggle.json`.
- **`nexus.db` no existe.** Todo lo que se declaró «cargado en la base» no está. Este repo es la memoria.
- **`git` no está instalado** en el container y no hay token: todo pasa por la integración de GitHub.
- **Python 3.12.14, Node 24.18.0, R 4.5.3** sí están.
- **Los adjuntos PDF del workspace SÍ se leen** (texto extraído). Los HTML de Arena, no. **Y varios están duplicados**: `Arena _ Benchmark & 6.html` 3 veces, `& 2.html` 2 veces, `Análisis de Publicabilidad` 2 veces.
- **Los Docs del workspace son ENUMERABLES:** IDs de página secuenciales, **paso 20**, prefijo `2kza6fw5-`, cargables por ID sin que Abraham pegue nada. **No existe herramienta de «listar docs»: el enumerador es el propio espacio de IDs.** → `INDICE-REAL-POR-ENUMERACION.md`.
- **El resto del entorno se re-mide, no se recuerda:** `CONTEXTO-ENTORNO.md`, §12 al 24-ago 12:15. Ahí vive medido que `xtensa-esp32-elf-gcc 16.1.0` compila, `javac` 17 compila, hay NDK 28.2 y red completa.

---

## 8. Modo de falla propio de esta línea, y ya costó dos veces

**El índice viejo (`INDICE-DE-ENLACES.md`) se armó cosechando el chat**, o sea que solo podía contener lo que algún mensaje de Abraham había citado. Creí que tenía 30 de 30 y tenía **30 de los citados**. El doc `5177` — 100/100, que retira tres afirmaciones mías — **no estaba**.

**La generalización, y aplica fuera de los Docs:** una lista hecha de citas solo contiene lo que alguien citó. Cuando existe un **enumerador** (un espacio de IDs, un `ls`, un endpoint), la lista se arma con el enumerador. Y **un índice parcial se reporta con su fracción**, nunca como cierre.
