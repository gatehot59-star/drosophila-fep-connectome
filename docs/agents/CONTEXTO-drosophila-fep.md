# CONTEXTO VIVO · conectoma / FEP / papers

**Última actualización:** 2026-08-24 19:30 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Leer esto **antes** de responder cualquier cosa de este proyecto. Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-motor.md`. Índice de Docs: `INDICE-REAL-POR-ENUMERACION.md` (**parcial, 46 de ~65**). Entorno: `CONTEXTO-ENTORNO.md` §13. Kaggle: `MANIFIESTO-KAGGLE.md` (**40 kernels, no 29**).

---

## 0. 🚨 EL RELOJ · el erratum vence el 30-ago, y el texto ya está escrito

**Fuente: doc `6117`, «PLAN MAESTRO 10 SEMANAS · 24-ago al 8-nov 2026».** Hoy es el 24-ago: **la S1 es esta semana.**

| # | El número que decide el éxito | Umbral | Estado |
|---|---|---|---|
| 1 | **Erratum en Zenodo** | **antes del 30-ago** | ✅ **texto listo y en git**; falta subirlo, y eso es de Abraham |
| 2 | Motivos con 0/40 en la biblioteca | ≥ 3 (hoy hay **1**) | sin avance |
| 3 | Nulls del motor complejo | **40** (piso de `p` 0,20 → 0,0488) | hoy 9 |
| 4 | Papers subidos | ≥ 2 antes del 8-nov | 0 |

**Deadlines externos** (el `6117` dice haberlos verificado contra `arcprize.org` el 23-ago — **se re-verifican antes de planificar**): **2-nov** código a Kaggle · **8-nov** papers · resultados 4-dic. Premios 450 mil (Paper Prize) + 850 mil (ARC-AGI-3). El código **no necesita puntuar alto** y puntean con **RHAE** (eficiencia de acción), que es lo que favorece estructura previa. **Ganar ARC no es el objetivo.**

**Las 10 semanas:** S1 cerrar lo público · S2 los nulls que faltan · S3 dos o tres motivos más · S4 mecanismo de aprendizaje · **S5 P1** · **S6 P2** · S7 agente ARC · S8 P4 · S9 revisión externa · S10 cerrar y subir. Cada actividad tiene **criterio de aborto** escrito.

**Los 5 papers:** **P1** auditoría de connectomíca dinámica (evidencia **completa**) · **P2** el 0,41% blindado (evidencia **completa**) · P3 biblioteca (**1 de 3-4 motivos**) · P4 ARC (depende de P1 y P2) · P5 Paper 2 como negativo. **P1 y P2 están en S5-S6 a propósito: si todo lo demás falla, esos dos salen igual.**

**El riesgo real no es técnico:** son cinco entregables en diez semanas de **una persona**. El orden **es** la protección.

---

## 1. Son TRES papers más un motor. No mezclarlos nunca más

| Nombre | Qué es | Estado |
|---|---|---|
| **PAPER 1** | *Signal Propagation Properties in the Drosophila melanogaster Connectome: Intermodal Isolation, Differential Motor Access, and Non-Trivial Temporal Amplification*, Mendieta 2026a. **7 páginas, leído completo el 24-ago** | Zenodo 20-mar-2026. **DOI placeholder `XXXXXXX` literal en el header** |
| **PAPER 2** | *Topological Retention and Selective Convergence* — FEP, Markov blanket, Script R | Borrador. Va como resultado **negativo** (P5) o no va |
| **PATENTE** provisional | Congelada antes del erratum. Doc `5717`: **la patente tiene razón, el FALSIFIED es un artefacto** | En pausa |
| **Motor** | SparseLTC / DualBrain, C99 + ESP32 | **El activo real.** Ver `CONTEXTO-motor.md` |

**El título real termina en «Non-Trivial Temporal Amplification»**, confirmado contra el PDF.

**El producto en tres capas:** (1) la **fuente de calibración** = el conectoma medido y sus priors · (2) el **motor** = de 15M aristas a **1.336 B de código medidos en ESP32** y 704 B de RAM todavía solo en x86 · (3) **la biblioteca = el activo**, hoy con **un** motivo. **No se vende como «derivado del cerebro de la mosca»: se venden microsegundos, miliwatts y BOM.**

---

## 2. Lo que dice el PDF publicado, leído verbatim (24-ago, 7 páginas)

- **§2.1:** `Density = 0.0074`. Y `E/I = 1.50`, 9.059.302 excitatorias (60,0%), 6.032.681 inhibitorias.
- **Abstract:** «E = 15,091,983 **synapses**» · «reciprocity (**36×** over density expectation)» · «**four** parameter-free neural models» · «7/10 sensory classes» · «τm ≈ 8.4 ms, **center** of the physiological range».
- **§2.1 dice «connections» para el mismo 15.091.983.** → la ambigüedad **existe** y es defecto de redacción, **pero NO es la causa del número**.
- **La tabla de RDI es la Table 8**, con columnas `Real | CP | Z_CP | MS | Z_MS`, **sin columna Ratio**. **La Table 7 es reciprocidad por circuito** (intra-motor 41,3% … optic→motor 0,0%). ⚠️ **El doc `6017` llamó «Tabla 7» a lo que es la Tabla 8:** su hallazgo se sostiene, el nombre estaba mal.
- **El 1.559× NO EXISTE en el PDF.** Leí las 7 páginas. Y la **Table 1 es la tabla de poblaciones**, sin un solo ratio.
- **§2.4 ya declara y deriva el guard de tautología del CP** («Net RDI at 1-hop is exactly invariant under CP null, sigma = 0»).
- **§2.5 y la Limitación 3 ya dicen TRES modelos compatibles.** El «four» queda **solo en el Abstract**.
- **§2.3:** *«For the density analysis, **10 canonical sensory classes** with N >= 10»*, y la **Tabla 5 muestra 9 filas**. Falta una y **no está establecido cuál**.
- **§7 Data Availability:** URL `github.com/Mendieta-Architect/drosophila-connectome-**propagation**`, licencia **AGPL v3**, resultados en Zenodo CC BY 4.0.
- **Tabla 4 suma 90.101** donde 85.821 + 4.281 = **90.102**.
- **§1.2 cita a Betzel et al. [2026] correctamente** en el texto; la entrada bibliográfica es PLOS Complex Systems 3(3), e0000091, **sin verificar contra el artículo**.
- Nulls declarados: MS `N = 100` estático y `N = 5` temporal; CP `N = 10` estático y `N = 5` temporal. **Tasa de swap 100%**, que no es alcanzable con las restricciones declaradas (la medida es 98,5%).

---

## 3. VALIDADO

| Hallazgo | Número | Instrumento |
|---|---|---|
| Densidad real del grafo | **7,85197×10⁻⁴** · y la publicada, 0,0074, es un **overflow de `int32`** reproducido a 8 cifras | resp 043 |
| **Reciprocidad** | 26,60% · 4.014.518 aristas · **rank 1º de 41, 20,59× vs CP, 0/40** ← **lo publicable** · 47,27× vs MS | 40 nulls CP (`6057`) |
| **Tabla 5 recomputada** | **4 enriquecidas, 4 depletadas, 1 ≈esperada** (el paper dice 0 y 7) | resp 043 + 046 |
| Sensorial → KC directo | **0** en el real, 40/40 nulls MS dan 1.533–2.640 | nulls MS |
| Fracción plástica | 4,045% neuronas · 0,41% conexiones · 0,47% sinapsis | conteo puro |
| Ley de Dale | **0 mixtas de 138.005** (96.672 exc. puras, 41.333 inh. puras) | conteo puro |
| **`KC→MBON`** | 62.261 · **7,81× vs CP, 0/40** ← sobrevive **contra mi predicción** | 40 nulls CP |
| **`DAN→KC`** | 47.404 · **8,71× vs CP, 0/40** → firma presináptica. Es 23,5× `DAN→MBON` | 40 nulls CP |
| **`KC→KC`** | 293.762 · **7,26× vs CP, 0/40** | 40 nulls CP |
| `ALPN→KC` | 27.848 · 1,70× vs CP (débil pero 0/40) | 40 nulls CP |
| Script R completo | **30/30 valores** reproducidos, máx. 5×10⁻⁵ | 4 instrumentos |
| Circuito de escape | 9,1× LC4→GF · LC6→GF = 0 aristas · 0/40 | 40 nulls CP |
| Escape compilado | ganancia **40×** vs detector vecino no cableado | motor propio |
| **Los 40 nulls sobre las 12 clases** | **0/40 en 12/12.** El centro de aprendizaje está **BLINDADO** | doc `5937` |
| **RDI dinámico** | **z = 197.** El resultado **más fuerte** del expediente | doc `5977` |
| **La brecha con Lin, CERRADA** | con umbral ≥5 sinapsis: reciprocidad **13,98%** vs su 13,8% (1,30%) · sinapsis/conexión **12,647** vs su 12,6 (0,37%) · densidad 1,405e-4 vs 1,61e-4 (12,7%, v783 vs v630) | resp 045 |
| Replicación cruzada JS/Python | 46,88× vs 47,27×; el 0,8% lo explica la convención de swaps | doc `5977` |
| **Priors medidos** | peso **lognormal(0,7034 , 0,8883)** · `inh_frac` de **0,068** a **0,513** · grado entrante CV 1,469 · fuerza CV 2,402 · **tabla de 95 pares de bloques** | doc `6057` |
| **C99 embebido en target** | **1.336 B de `.text` a `-Os`** en ESP32/ESP32-S3 | resp 039 |

**La Tabla 5, con las poblaciones REALES del paper** (`cell_class`, `motor_n = 1485` **exacto**, `p_exc = 0,600272`):

```
clase         N_paper   N_mio   obs_exc   r_paper  r_ovf    ratio_OK    veredicto
mechano.         2659    2656     23010     1.300  1.314    12.378  ENRIQUECIDO
unk. sensory      131     131      1179     1.400  1.365    12.858  ENRIQUECIDO
AN                495    2231     27857     0.600  1.894    17.839  NO REPRODUCIBLE
gustatory         408     408      1280     0.500  0.476     4.482  ENRIQUECIDO
hygrosen.          74      74        13     0.030  0.027     0.251    DEPLETADO
thermosen.         29      29        14     0.070  0.073     0.690    ~ESPERADO
olfactory        2279    2279        80     0.005  0.005     0.050    DEPLETADO
visual          10853   10855       137     0.002  0.002     0.018    DEPLETADO
vis. optic      77521   77530      1679     0.003  0.003     0.031    DEPLETADO
```

**8 de 9 filas reproducen el ratio publicado con la densidad overflowed**, así que la fórmula y las poblaciones están **establecidas, no inferidas**.

---

## 4. REFUTADO / NO TESTEABLE / RETIRADO

| Claim | Qué lo tumbó |
|---|---|
| **«1.652× con la densidad de Lin»** (doc `5117`) | **🔴 RETIRADO (resp 045).** Es una **comparación cruzada**: divide nuestra reciprocidad **SIN** umbral (0,266) por la densidad de Lin **CON** umbral (1,61e-4). Pareada dentro de un solo criterio da **995×**, y el publicable sigue siendo **20,59× contra 40 nulls CP** |
| **«jerarquía de ruteo: 283,2× y listo»** | **NO TESTEABLE contra el null fuerte** (doc `6057`): `sd = 0,0` exacto y 40/40. Es **cantidad conservada** bajo CP porque el null baraja destinos dentro de bloques de super_class y el grupo MOTOR está definido por la misma super_class. **El 283,2× es contra grado.** Idem `sensory→KC` y `MBON→motor`. Arreglo: null de **tripartición**, sin correr |
| **«el desfasaje de un paso explica la discrepancia a t=60»** (mío) | **REFUTADO por lectura del código** (doc `6017`): `res[t] = h.copy()` va **después** del update en los dos loops. La causa real eran **dos métricas con el mismo nombre** (3 vs 6 pares) |
| **«el erratum corrige un 1.559× que aparece 9 veces»** (borrador) | **🔴 RETIRADO (resp 046):** el 1.559 **no existe en el PDF**, y la «Table 1 con ratios» de ese ítem es acá **la tabla de poblaciones**. Ese ítem pertenece a otro documento. **Un erratum que corrige un claim que el paper no hizo es él mismo un error** |
| **«el erratum está listo / no está listo / no existe en git»** | **CERRADO: `docs/ERRATUM.md` existe en git desde el commit `cfd1def`, 9 ítems, cero placeholders.** Lo que falta es **subirlo a Zenodo**, y eso es de Abraham |
| «el Paper 1 evita la densidad contaminada» | falso: §2.1 dice `Density = 0.0074` y el Abstract dice 36× |
| «el guard de tautología es aporte propio» | §2.4 del paper ya lo declara y lo deriva |
| «0 clases enriquecidas / 7 depletadas» (el paper) | con la densidad correcta: **4 enriquecidas, 4 depletadas, 1 ≈esperada** |
| «**4 de 9 clases pasan a enriquecidas**», retirado por el `5177` | **🔄 EL RETIRO SE REVIERTE (resp 043).** El `5177` usó el **85.821 de la Tabla 4, que es una SUMA DE PESOS**, como conteo de aristas; el conteo real es **23.010**, y con ése `23010/1859 = 12,378` y `23010/17520 = 1,313 ≈ 1,3` publicado. **La expectativa SÍ es de densidad y el «4 y 4» es correcto** |
| «reciprocidad 36×» | **es el MISMO overflow**: `0,266/0,00739526 = 35,97`. Una línea de código, dos números publicados |
| «τ_m = 8,4 ms, centro del rango» | **dos defectos distintos:** el centro de 5-20 es **12,5** (y 3,3 está **debajo** del rango, no en su límite), **y** la derivación correcta es `-1/ln(1-τ) = 7,89`, error 6,47% |
| «R = 1,31, retención selectiva» | cruza 1 en las tres modalidades según normalización (visual 1,878 → 0,811) |
| col-norm «respeta la varianza local» | lleva el CV de 2,402 a **cero**; la global lo preserva entero |
| **Tabla 8 reproducible** (la que el `6017` llamaba Tabla 7) | **4 particiones con la definición EXACTA del código y ninguna reproduce la FORMA.** Y los 6 valores **no existen en ninguno de los 40 notebooks**: falta el instrumento. Un valor alto a t=15 es **imposible** con esa partición |
| «hace falta una SNN para latencias» | la métrica al 10% del pico da mechano 4 < gust 5 < visual 6 < olf 10 |
| «el control lineal descarta saturación» | clipea: `max h = 2,0000` exacto en 2 de 3 modalidades |
| «la topología explica la función» | el escape compilado da selectividad temporal 1,04× |
| «la entropía baja distingue biología» | los nulls bajan más: dH −9,79 vs −2,88. Doc `5777`: **la FORMA sí, 7/12** |
| «visual es la vía con menos acceso motor» | **no sobrevive**: es **olfactory** (doc `5937`) |
| «sinapsis vs conexiones» explica el bug de densidad | **existe como defecto de redacción pero NO es la causa**: la causa es el overflow (resp 043). Sinapsis reales: 54.492.922, media 3,61 por conexión sin umbral y 12,647 con umbral ≥5 |
| «Therianos me refuta» | **retirado:** Lin mide 13,8% en el adulto y Therianos usa conectoma **larval** (doc `5117`) |
| «el `temporal RDI` es frágil» (mío) | **error de eje** (doc `5977`). **El eje no es estático vs dinámico: es CONTRA QUÉ NULL** |
| «KC→MBON cae contra CP» (predicción mía) | **refutada: sobrevive con 7,81×, 0/40** |

---

## 5. NO MEDIDO / pendiente, declarado

1. **La décima clase de la Tabla 5.** §2.3 declara 10, la tabla muestra 9. **Cuál falta: no establecido.**
2. **La fila AN no es reproducible.** `N=495` no sale de ningún filtro consistente con las otras ocho (`cell_class == 'AN'` da 2.231, y su ratio da 1,894× y no 0,6×). Va declarada así en el erratum, **no corregida**.
3. **Si los `p` de la Tabla 5 usan `p_edge_exc`** o otra probabilidad.
4. **El script de la Tabla 8: no está en el corpus.** Cero de 6 valores en 40 notebooks.
5. **Null de tripartición: no corrió.** Sin él la jerarquía de ruteo no se publica contra modularidad.
6. **Faltan 21 nulls** para que el test global de los 12 pares llegue a `p<0,05`. ~30 min (doc `5957`).
7. **Tres citas externas sin verificar:** los dos **DOI** contra Zenodo, **Lin et al. 2024** contra Nature, y **Betzel** (PLOS Complex Systems 3(3), e0000091) contra el artículo. El erratum lo declara.
8. **Los tres notebooks con overflow se declaran descendientes** de un «pipeline original» que **no está en el corpus**. Que sean los que produjeron el paper está **apoyado** por reproducir 8 de 9 ratios, **no establecido**.
9. **Un solo patrón de overflow barrido** (`N*(N-1)`). No barrí `N**2` ni otros productos de enteros grandes.
10. **El barrido de Docs está al 71%:** 46 de ~65. **9 IDs pendientes** (`6157 6177 6197 6217 6237 6257 6277 6317 6337`), ~15 en icca-engine, ~50 entre `3637` y `4717`, MUDH/AURA sin tocar.
11. **Las fechas de ARC no las verifiqué yo.** Vienen del `6117`.
12. **Los dos `.mjs` del release no corren en un clon ajeno:** leen `/workspace/...` con ruta absoluta, y `routing_hierarchy.mjs` depende de un archivo que escribe `analyze_nulls40.mjs`. **Declarado en el README y en METHODS, no parcheado.** Y mi test de «clon limpio» dio un **falso verde** porque el archivo absoluto existe en esta máquina (resp 047).
13. **Los dos JSON grandes van por md5**, no commiteados: `nulls40.json` (191.443 B, `38bf1fcadaf37a3b125f83d22b6f4d8e`) y `dualbrain_bench.json` (31.527 B, `1025d60b4e9521d7e4a21ed282935049`). Su evidencia verbatim **sí** está en los `.log`.
14. **Los 6 `.py` de deuda siguen fuera de git.** Manifiesto con md5 en `MANIFIESTO-KAGGLE.md`.
15. **El C99 embebido está medido a medias:** hay 1.336 B de `.text` en target, pero **no hay `.elf`, no hay RAM en target** y no corrió en hardware.
16. **No corrí el review automático** sobre los archivos nuevos del repo. **K-02: deuda declarada.**

---

## 6. Decisiones esperando a Abraham

1. **🔴 SUBIR LA v2 A ZENODO antes del 30-ago.** El texto está en **`docs/ERRATUM.md`**, 9 ítems, cero placeholders. **Falta solo tu acción.** El criterio de aborto del plan decía «si el PDF difiere del borrador en más de dos números, parar y re-auditar»: **ya se hizo, se encontraron dos y están corregidos** (el 1.559× inexistente y la URL mal citada).
2. **Re-verificar los dos DOI contra Zenodo** antes de pegarlos. Los tengo del `5157`, que los sacó de su API el 21-ago.
3. **⭐ El `README.md` público clasifica los resultados dinámicos como «negative methodological result»**, y ahí cae el `temporal RDI` con `z=197`. **No lo reclasifiqué: le puse un bloque «Pending revision» que pide no citarlo como veredicto.** La decisión es tuya.
4. **⭐ Los bugs del Script R viven DENTRO del verificador V-K** (doc `5637`, 14 citas con línea). Y el V-K **comparte el overflow** con lo que verifica (resp 044). **Es el ítem 9 del erratum.** Parchear antes de publicar, o publicar declarando la limitación.
5. **Buscar el script de la Tabla 8.** Si aparece, se corre en una hora. Si no, es un resultado no reproducible y va en Limitaciones.
6. **Mergear el PR #1**, o decir qué le falta. El review automático sin hallazgos es **NO MEDIDO, no aprobación**.
7. **¿Arreglo las rutas absolutas de los dos `.mjs`?** Es tocar código que produjo figuras publicadas.
8. **El barrido de Docs: ¿sigo con los 9 IDs del conectoma o abro las otras zonas?** Pregunta de la resp 031, perdida en un corte de instancia.
9. **Subir los 6 `.py` de deuda y los dos JSON grandes.**
10. El **clip de la config (e)**: subirlo y re-correr. Si diverge, también es resultado.
11. Org `Mendieta-Architect` o aceptar la URL `gatehot59-star` en el erratum.

---

## 7. Estado de git y del entorno, medido

**Ya en el repo:** `docs/ERRATUM.md` (**9 ítems, commit `cfd1def`**) · `README.md` · `LICENSE` · `docs/METHODS.md` · `src/` con 8 archivos · `results/` con 5 logs · `docs/agents/` con los cuatro contextos, el índice, el manifiesto de Kaggle, la evidencia y 47 respuestas.

**Verificado por md5 desde los dos lados (resp 045):** cuatro archivos de `src/` son **byte-idénticos** al código que corrió en Kaggle (`motor.py`, `cp40.py`, `nulls40_kaggle.py`, `hm_sweep.py`). **Esos resultados son recomputables por un tercero desde git.**

**Entorno:** el container **no es efímero** (uptime 3,2 días medido), `git` no está instalado y todo pasa por la integración de GitHub, `nexus.db` **no existe**. Python 3.12.14, Node 24.18.0, R 4.5.3. **Los Docs son ENUMERABLES:** IDs de página secuenciales **paso 20**, prefijo `2kza6fw5-`. Límite medido: **5 Docs completos no entran en una ventana**. **El resto se re-mide, no se recuerda:** `CONTEXTO-ENTORNO.md` §13.

---

## 8. Modos de falla propios de esta línea, y cada uno ya costó

**1 · Una lista hecha de lo que está a mano solo contiene lo que está a mano.** Dos veces: el `INDICE-DE-ENLACES.md` cosechado del chat (30 de los citados, no 30 de 30), y el corpus de Kaggle (**29 archivos locales contra 40 kernels reales**, lo que invalidó el denominador de un barrido que había declarado cerrado). **Cuando existe un enumerador, la lista se arma con el enumerador, y el denominador se mide en la fuente, no en la copia.**

**2 · Un null cuyos invariantes incluyen la cantidad medida no es un control, es un espejo.** **Si `sd(null) == 0`, reportar NO TESTEABLE**, no `1,000×`. Cuatro líneas, 22,2 minutos de cuota.

**3 · Una explicación que encaja no es una explicación medida.** El «desfasaje» se escribió en un documento destinado a un DOI **sin leer el código que explicaba**, y el código estaba a dos llamadas. Y la **causa** del overflow apareció solo al **ejecutar**: `numpy` emitió el warning, ninguna relectura lo iba a producir.

**4 · Un archivo que no abrí en este turno no recibe veredicto de vigencia.** «Sigue vigente» es una medición, no un default.

**5 · Comparar dos cantidades medidas con criterios distintos. TRES veces.** El `5177` (suma de pesos como conteo de aristas), el `5117` (reciprocidad sin umbral contra densidad con umbral), y el borrador del erratum (un valor de otro documento). **Antes de dividir dos números, verificar que midan lo mismo.**

**6 · Un test que no puede dar rojo no es un test. TRES en un día.** El `$?` del shell reportando `exit=0` sobre una compilación fallida, un `grep -c` con falso cero por la coma de miles, y un «clon limpio» que corrió leyendo una ruta absoluta.

**7 · Lo que no está commiteado se pierde justo cuando más falta hace.** El entregable del 30-ago vivía en un solo directorio sin versionar y cuatro documentos lo daban por subido. **Hoy está en git.**
