# CONTEXTO VIVO · conectoma / FEP / papers

**Última actualización:** 2026-08-23 21:35 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Leer esto **antes** de responder cualquier cosa de este proyecto. Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-motor.md`.

---

## 1. Son TRES papers más un motor. No mezclarlos nunca más

| Nombre | Qué es | Estado |
|---|---|---|
| **PAPER 1** | *Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*, Mendieta 2026a | Depositado en Zenodo 20-mar-2026. **El PDF lleva DOI placeholder `10.5281/zenodo.XXXXXXX`** |
| **PAPER 2** | *Topological Retention and Selective Convergence* — FEP, Markov blanket, Script R | Borrador. **No publicable como está** |
| **PATENTE** provisional | Texto congelado **antes** del erratum. Dos series RDI incompatibles (Tabla 6 vs 15) | En pausa |
| **Motor** | SparseLTC / DualBrain, línea C99 + ESP32 | **El activo real.** Ver `CONTEXTO-motor.md` |

**El título real del Paper 1 termina en «Non-Trivial Temporal Amplification»**, no en «Temporal Amplification Under Dynamics Without Algorithmic Weight Optimization», que es el título que usa el borrador del erratum. Hay que corregirlo ahí.

---

## 2. Lo que dice el PDF publicado, leído verbatim (2026-08-23)

Datos duros del propio archivo, para no volver a suponer:

- **§2.1:** `Density = 0.0074` → **la densidad mal SÍ está en el paper publicado**.
- **Abstract:** `reciprocity (36x over density expectation)` → el 36× también.
- **Table 7 = «Reciprocity by circuit type».** La tabla de RDI es la **Table 8**, con columnas `Real | CP | Z_CP | MS | Z_MS`, **sin columna Ratio**.
- **El 1.559× no aparece** en Abstract, §1.3, §3.4 ni §4.1.
- **§2.4 ya declara el guard de tautología:** *"Net RDI at 1-hop is exactly invariant under CP null (sigma = 0)"*, derivado analíticamente.
- **§1.2 cita a Betzel et al. [2026] correctamente.**
- Nulls declarados: MS `N = 100`, CP `N = 5–10`.

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

---

## 4. REFUTADO (cada uno con el número que lo tumbó)

| Claim | Qué lo tumbó |
|---|---|
| **«el erratum está listo para subir a Zenodo»** | **E3 corrige una «Table 7» con columna Ratio y 1.559× que NO existen en el PDF publicado.** Esos elementos son de otro documento. El erratum no se puede subir así |
| «el Paper 1 evita la densidad contaminada» | falso: §2.1 dice `Density = 0.0074` y el Abstract dice 36× |
| «el Paper 1 cita mal a Barsotti» | §1.2 cita **Betzel** correctamente. Sin confirmar en la bibliografía |
| «el guard de tautología es aporte propio» | §2.4 del paper ya lo declara y lo deriva |
| «1.559× de amplificación» | denominador 0,0005 ± 0,0003: va de 1.041× a 4.164× dentro de 1σ, e indefinido a 2σ |
| «R = 1,31, retención selectiva» | cruza 1 en las tres modalidades según normalización (visual 1,878 → 0,811) |
| «0 clases enriquecidas» | con la densidad correcta son 4 y 4 |
| «reciprocidad 36×» | era 338,8× contra densidad, 47,3× contra grado preservado |
| «τ_m = 8,4 ms» | la constante correcta es 7,89 ms. Error 6,47% |
| col-norm «respeta la varianza local» | lleva el CV de 2,402 a **cero**; la global lo preserva entero |
| Tabla 7 reproducible | 5 variantes × 2 precisiones, ninguna reproduce la forma |
| «hace falta una SNN para latencias» | la métrica al 10% del pico da mechano 4 < gust 5 < visual 6 < olf 10 |
| «el control lineal descarta saturación» | clipea: `max|h| = 2,0000` exacto en 2 de 3 modalidades |
| «la topología explica la función» | el escape compilado da selectividad temporal 1,04× |
| «la entropía baja distingue biología» | los nulls bajan más: dH −9,79 vs −2,88, z = 18,1 |
| jerarquía de ruteo 991× | corregida a **283×**; el más depletado es olfactory, no visual |
| «sinapsis vs conexiones» explica el bug de densidad | falso: las sinapsis reales son 54.492.922. **Causa desconocida** |

---

## 5. NO MEDIDO / pendiente, declarado

1. **Conclusiones, bibliografía y Material Suplementario del PDF del Paper 1:** la extracción se cortó en §5. El 1.559× podría estar en Conclusiones. **Leerlo antes de tocar el erratum.**
2. **De dónde sale el DOI `10.5281/zenodo.19136948`** que se venía citando: no está en el PDF y la web no lo encuentra.
3. Los adjuntos 1, 3 y 7 (patente, Script R, PDF de Gemini de 101 pág.) no se localizaron por nombre en la última pasada. **No se afirma que no estén.**
4. Los HTML de Arena devuelven markup de página, no conversación. Sin verificar si el texto vive en algún payload del bundle.
5. `titan-paper-dualbrain` y `notebookceb82767da`: logs sin leer.
6. La hipótesis del 96% fijo: **sin testear** sobre SparseLTC. Ver `CONTEXTO-motor.md` §4.
7. El script original de la Tabla 7 del Paper 2: no encontrado.
8. Agujero de nulls CP para reciprocidad y KC→MBON.

---

## 6. Decisiones esperando a Abraham

1. **Reescribir el erratum E3** contra el documento que realmente contiene el 1.559×, o borrar E3. Hoy apunta a una tabla inexistente.
2. **Conseguir el DOI real** del depósito de Zenodo. El PDF lleva `XXXXXXX`.
3. **Mergear el PR #1**, o decir qué le falta.
4. Subir los 7 `.py` que quedan del container.
5. El **clip de la config (e)**: subirlo y re-correr. Si diverge, también es resultado.
6. Org `Mendieta-Architect` o aceptar la URL `gatehot59-star` en el erratum.

---

## 7. Correcciones sobre el propio entorno (medidas)

- **El container NO es efímero.** `/workspace` persiste con el parquet (100.804.642 B), el TSV (31.718.505 B), los 17 `.py` y `kaggle.json`.
- **`nexus.db` no existe.** Todo lo que se declaró «cargado en la base» no está. Este repo es la memoria.
- **`git` no está instalado** en el container y no hay token: todo pasa por la integración de GitHub.
- **Python 3.12.14, Node 24.18.0, R 4.5.3** sí están.
- **Los adjuntos PDF del workspace SÍ se leen** (texto extraído). Los HTML de Arena, no. **Y varios están duplicados**: `Arena _ Benchmark & 6.html` 3 veces, `& 2.html` 2 veces, `Análisis de Publicabilidad` 2 veces.
