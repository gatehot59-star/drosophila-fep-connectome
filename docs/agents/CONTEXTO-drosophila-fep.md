# CONTEXTO VIVO · conectoma / FEP / motor

**Última actualización:** 2026-08-23 20:40 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Leer esto **antes** de responder cualquier cosa de este proyecto. Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`.

---

## 1. Son TRES papers más un motor. No mezclarlos nunca más

| Nombre | Qué es | Estado |
|---|---|---|
| **PAPER 1** | *Signal propagation properties in the Drosophila melanogaster connectome*, Mendieta 2026a | **PUBLICADO** en Zenodo, DOI v1 `10.5281/zenodo.19136948`. Necesita erratum |
| **PAPER 2** | *Topological Retention and Selective Convergence* — FEP, Markov blanket, Script R | Borrador. **No publicable como está** |
| **PATENTE** provisional | Texto congelado **antes** del erratum. Dos series RDI incompatibles (Tabla 6 vs 15) | En pausa |
| **Motor** | SparseLTC / DualBrain, línea C99 + ESP32 | **El activo real.** No publicado |

---

## 2. Los tres motores, que NO son el mismo

| Motor | Dónde | Qué es | ¿Entrena? |
|---|---|---|---|
| **SparseLTC** | `scriptR.py`, `motor.py` | 138.639 neuronas reales, τ por neurona | **NO** |
| **`LiquidCell` denso** | `tres_brazos.py`, brazo W | 8 unidades, Adam, PyTorch | Sí |
| **DualBrain embebido** | `esp32c.py`, C99 | 704 B de RAM, dos vías + gate | Vía lenta sí |

**Consecuencia grave y ya registrada:** el brazo W congela una submatriz de 26 nodos dentro del motor **denso**, no dentro de SparseLTC, y **no congela τ**. Su veredicto "0/4, se retira la analogía del 96% fijo" **no refuta la hipótesis: nunca la testeó.** Estado correcto: **NO MEDIDO**.

---

## 3. VALIDADO (conteos puros o con null que preserva grado y modularidad)

| Hallazgo | Número | Instrumento |
|---|---|---|
| Densidad del grafo | 7,854×10⁻⁴ | igraph + propio |
| Reciprocidad | 26,60% · 4.014.518 aristas · 20,6× vs CP, 0/40 | igraph + 40 nulls |
| Acceso motor corregido | 4 enriquecidas / 4 depletadas (el paper dice 0 y 7) | conteo puro |
| Sensorial → KC directo | **0** en el real, 40/40 nulls dan 1.533–2.640 | nulls CP |
| Fracción plástica | 4,045% de neuronas · 0,41% de conexiones | conteo puro |
| `DAN→KC` vs `DAN→MBON` | 23,5× · 8,71× sobre CP, 0/40 → regla **presináptica** | nulls CP |
| Ley de Dale | **0 de 138.005** neuronas con salidas de los dos signos | conteo puro |
| Script R completo | **30/30 valores** reproducidos, máx. discrepancia 5×10⁻⁵ | 4 instrumentos independientes |
| Circuito de escape | fan-in 314→2+6 · 9,1× LC4→GF · **0/40** · LC6→GF = 0 aristas | 40 nulls CP |
| Escape compilado | ganancia **40×** vs detector vecino no cableado | motor propio |
| Óptimo de reparto | h_m=10/h_r=22 → 1,18× sobre LSTM (publicado: 4,05×, el peor punto) | barrido, p=8,6×10⁻¹⁰ |

---

## 4. REFUTADO (cada uno con el número que lo tumbó)

| Claim | Qué lo tumbó |
|---|---|
| «1.559× de amplificación» | denominador 0,0005 ± 0,0003: va de 1.041× a 4.164× dentro de 1σ |
| «R = 1,31, retención selectiva» | cruza 1 en **las tres** modalidades según normalización (visual 1,878 → 0,811) |
| «0 clases enriquecidas» | con la densidad correcta son 4 y 4 |
| «reciprocidad 36×» | era 338,8×: subreportó su propio hallazgo 9,4× |
| «τ_m = 8,4 ms» | la constante correcta es 7,89 ms. Error 6,47% |
| col-norm «respeta la varianza local» | lleva el CV de 2,402 a **cero**; la global lo preserva entero |
| Tabla 7 reproducible | 5 variantes × 2 precisiones, ninguna reproduce la forma |
| «hace falta una SNN para latencias» | la métrica al 10% del pico da mechano 4 < gust 5 < visual 6 < olf 10 |
| «el control lineal descarta saturación» | clipea: `max|h| = 2,0000` exacto en 2 de 3 modalidades |
| «la topología explica la función» | el escape compilado da selectividad temporal **1,04×**, o sea ninguna |
| «la entropía baja distingue biología» | los nulls bajan **más** (dH −9,79 vs −2,88, z=18,1): signo invertido |
| jerarquía de ruteo 991× | corregido a **283×**; el canal más depletado es olfactory, no visual |
| «sinapsis vs conexiones» explica el bug de densidad | falso: las sinapsis reales son 54.492.922. **Causa desconocida** |

---

## 5. NO MEDIDO / pendiente, declarado

1. `titan-motor-ltc-complejo` (complete 15:06Z): **log nunca bajado**. Es la fuente del `+0,196 vs −0,027, 0/9`.
2. `titan-paper-dualbrain` (complete 00:06Z): log no leído en detalle.
3. `notebookceb82767da` (928 KB): sin leer.
4. La hipótesis del 96% fijo: **sin testear** sobre SparseLTC (el brazo W midió otro motor).
5. Agujero de nulls CP para reciprocidad y KC→MBON.
6. El script original de la Tabla 7: no encontrado.
7. Piso de significancia con 9 nulls = **0,20**. La ventaja de τ compleja es prueba de concepto del instrumento, no el número del paper.

---

## 6. Decisiones esperando a Abraham

1. **Mergear el PR #1**, o decir qué le falta. `main` tenía un README de 206 B hasta este commit.
2. Subir los **17 `.py` y los `.json` de resultado** del container al repo. Hoy viven en un solo disco.
3. El **clip de la config (e)**: subirlo y re-correr. Si diverge, también es resultado.
4. Org `Mendieta-Architect` o aceptar la URL corregida `gatehot59-star` en el erratum.

---

## 7. Correcciones sobre el propio entorno (medidas, no supuestas)

- **El container NO es efímero.** Medido 2026-08-23 20:37: `/workspace` persiste con el parquet (100.804.642 B), el TSV (31.718.505 B), los 17 `.py` y `kaggle.json`. La afirmación previa de que nacía vacío en cada llamada es **falsa**.
- **`nexus.db` no existe** en este container. Todo lo que se declaró "cargado en la base" no está. Este repo es la memoria.
- **`git` no está instalado** en el container: todo lo que va al repo sale por la integración, no por shell. `/workspace/repo` es staging, no un clon.
- **Python 3.12.14 sí está**, con numpy, scipy, pandas, pyarrow, sklearn, igraph, matplotlib. Node 24.18.0. R 4.5.3.
