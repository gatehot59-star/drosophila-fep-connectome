# 2026-11-02-009 · Diseño y sello del corte causal para los otros 16 relevos recurrentes pesados D→X (H_MECANISMO_RELEVOS16)

## 1. Pedido

«Diseñá el corte causal para los otros 16 relevos».

En la entrega `2026-11-02-008` se identificaron en el universo de cierre `(S, X, D)` **17 pares de tipos `(D_driver, X_hub)`** con al menos **80 sinapsis en una sola fila** (`w_max >= 80`) conservados entre **FlyWire v783** y **BANC v626** (0 de 10.000 permutaciones nulas alcanzan 17 pares conservados, `p < 10^-4`). Uno de esos 17 pares es `DNp04 -> PVLP010` (#2 del ranking en FlyWire, `w = 190`, `BANC = 138`), ya medido y verificado en `H_MECANISMO_DNp04` (`2026-11-02-006`). Este documento fija el diseño experimental completo, las guardas exactas de filas y pesos en `connectivity.parquet`, los dos regímenes de activación, los cortes conjuntos en hubs convergentes y los criterios de falsación para los **otros 16 relevos** (`R01` a `R16`).

---

## 2. Herramientas declaradas

* **`MUDH Gateway` → `build.write_file`, `build.run`, `build.python`, `build.read_file`** (ejecución en `brain-env`, sin cuota externa):
  * `/workspace/dnp04/verif/disenar_16_relevos.py` (SHA-256 `882d367197d9b0723c6e12abccaf27e92a88c46098ef7f5fb5de90723d8cc260`) -> generó `/workspace/dnp04/verif/diseno_corte_16_relevos.json` (`171.824` bytes, SHA-256 `045d7823e2e939551c6b11d467d3ee22cf59579d7937fee82ba267b6d27a1527`) y `/workspace/dnp04/verif/diseno_corte_16_relevos.log` (SHA-256 `39eaed3429337c5545d00a05406a5feb3ce6464145a475cbc0d2ae4761709170`).
  * `/workspace/dnp04/verif/chequear_16_en_4estimulos.py` -> verificó las tasas de disparo `C0`, `C1` y `Q1..Q6` de los 16 relevos en las corridas existentes de `LC4`, `LPLC2`, `LPLC1` y `LPLC4`.
  * `/workspace/dnp04/verif/armar_sello_16_relevos.py` (SHA-256 `f60624380e6344f21be5cc8608ba6ea913bf1971687c2d683eb91b3f845b2f62`) -> generó `/workspace/dnp04/verif/sello_diseno_16_relevos.json` (`31.672` bytes, SHA-256 `00bf832c3697d76c70d6d5594b44b550217e5bb4540e1c898b4b6d950341f8bb`) y `/workspace/dnp04/verif/sello_diseno_16_relevos.log` (SHA-256 `92cb401930ac43033c7e382d1a0f7d9f507a0779f5b84a7cf6337ba487a136c2`).
* **`GitHub MCP`** (`githubmcp_create_or_update_file`, `githubmcp_get_file_contents`): commit de la evidencia y de este diseño en `main` de `gatehot59-star/drosophila-fep-connectome`.
* **`ClickUp`** (`create_document_page`, `str_replace`): publicación de la subpágina `2026-11-02-009` bajo `https://app.clickup.com/90171457413/v/dc/2kza6fw5-26157` y actualización de `https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29177`.
* **`MUDH Gateway` → `sqlite.execute`**: registro de cierre del turno en `nexus.db` (`reportes`).

---

## 3. Qué se midió para diseñar el experimento (3 trampas dinámicas detectadas antes de correr)

Antes de fijar las condiciones de corte, medimos los 16 relevos contra `connectivity.parquet` (`15.091.983` filas) y contra los JSON crudos de los 4 estímulos visuales ya corridos (`LC4`, `LPLC2`, `LPLC1`, `LPLC4`). Ese cruce reveló **tres hechos estructurales y dinámicos** que harían fracasar un diseño ingenuo si se repitiera a ciegas el protocolo de `LC4`:

### 3.1. Trampa 1 · Cascada desinhibitoria jerárquica en `R01 (DNp35 -> CB0527)`

* `R01` (`DNp35_right` `idx=59804` -> `CB0527` `idx=30887`, `235` sinapsis en una sola fila, `10,18 mV` de PSP pico, `184` sinapsis en BANC, y espejo contralateral `88284 -> 60863` con `221` sinapsis) es el relevo unitario más pesado de todo el universo `D -> X`, por encima incluso de `DNp04 -> PVLP010` (`190` sinapsis).
* Anatómica y visualmente, `LPLC1_right` entrega **904 sinapsis excitatorias directas** a `DNp35_right` (y `LC11_right` entrega `584`). Sin embargo, en las corridas medidas de `LPLC1_right`:
  * En `C0` (red intacta), `DNp35_right` está **clampeada en `1,75 Hz`** (`0,90 Hz` en `LPLC2_right`) porque `AVLP080` (`idx=6128`) le descarga **388 sinapsis inhibitorias** (y `X_30179` otras `200`).
  * Al quitar toda la población `X` (`C1`), `DNp35_right` salta de `1,75 Hz` a **`71,85 Hz`** en `LPLC1` (y de `0,90 Hz` a **`83,15 Hz`** en `LPLC2`).
  * Más aún: en la condición `Q6` ya corrida de `LPLC1_right` (donde **sólo** se silencia `AVLP080`), `DNp35_right` se desinhibe y salta de `1,75 Hz` a **`32,35 Hz`** (`+30,60 Hz`, 18,5×).
  * En cambio, bajo `LC4_right`, `DNp35_right` sí está activa en `C0` (`15,95 Hz`) y `CB0527` dispara `23,60 Hz` en `C0` (cayendo a `16,85 Hz` en `Q3` y subiendo a `30,25 Hz` cuando se silencia `AVLP080` en `Q6`).
* **Consecuencia de diseño:** En `LPLC1`, `DNp35 -> CB0527` opera como un **relevo de segunda etapa gobernado por desinhibición (`AVLP080 -| DNp35 -> CB0527 -| D'`)**. Por eso, además de medir `R01` en `LC4_right` y `LC11_right`, el diseño incluye la condición específica **`Q1_desinhibido`** en `LPLC1_right`: comparar `Q6(AVLP080=0)` (donde `DNp35` queda liberada a `32,35 Hz`) contra `Q6(AVLP080=0) ∪ Q1(DNp35->CB0527=0)` (`1.678` filas, `18.858,0` sinapsis).

### 3.2. Trampa 2 · Convergencia multi-descendente (`T2`) sobre 4 hubs compartidos (`CB0580`, `CB0534`, `CB0172`, `PS100`)

Los 16 relevos nuevos no apuntan a 16 interneuronas independientes, sino a **11 tipos `X_hub` únicos**, distribuidos en tres estratos biofísicos según el umbral de disparo de una espiga aislada en el modelo de Shiu (`w_crit = 162` sinapsis, `7,0 mV`):

1. **Estrato `T1` (Relevos unitarios supraliminares, `w >= 162`, `PSP >= 7,0 mV`, 3 pares):**
   * `R01`: `DNp35 (59804) -> CB0527 (30887)` (`w = 235`, `10,18 mV`, `BANC = 184`).
   * `R02`: `DNpe016 (61465) -> cL22c (80081)` (`w = 180`, `7,80 mV`, `BANC = 138`).
   * `R03`: `DNa03 (96843) -> PLP060 (116067)` (`w = 165`, `7,15 mV`, `BANC = 105`).
2. **Estrato `T2` (Hubs convergentes multi-descendente, `88 <= w <= 155`, `3,81..6,71 mV`, 9 pares sobre 4 tipos `X_hub`):**
   * **`Hub H1 (CB0580)`**: en el nodo `x_idx=33912` convergen `R10` (`DNp47_right`, `115` sin), `R14` (`DNp101_left`, `91` sin) y el espejo contralateral de `R13` (`DNp104_left`, `idx=19410`, `72` sin), sumando **`278` sinapsis (`12,04 mV`) en 3 filas**. En el nodo espejo `x_idx=58129` convergen `R13` (`DNp104_right`, `93` sin) y el espejo de `R14` (`DNp101_right`, `idx=71368`, `87` sin), sumando **`180` sinapsis (`7,80 mV`) en 2 filas**.
   * **`Hub H2 (CB0534, x_idx=19257)`**: convergen `R05` (`DNp71_right`, `154` sin) y `R07` (`DNg100_left`, `128` sin), sumando **`282` sinapsis (`12,21 mV`) en 2 filas**.
   * **`Hub H3 (CB0172, x_idx=122969)`**: convergen `R04` (`DNpe023_left`, `155` sin) y `R16` (`DNae005_right`, `88` sin), sumando **`243` sinapsis (`10,52 mV`) en 2 filas**.
   * **`Hub H4 (PS100)`**: en `x_idx=45293` convergen `R11` (`DNa06_right`, `111` sin) y el espejo de `R15` (`DNge148_left`, `idx=53975`, `87` sin), sumando **`198` sinapsis (`8,57 mV`) en 2 filas**. En el nodo espejo `x_idx=112031` convergen `R15` (`DNge148_right`, `88` sin) y el espejo de `R11` (`DNa06_left`, `idx=69226`, `77` sin), sumando **`165` sinapsis (`7,15 mV`) en 2 filas**.
   * **Consecuencia de diseño:** Cada arista individual de `T2` está por debajo de `162` sinapsis (`3,81..6,71 mV`), pero la suma de sus `D_driver` convergentes supera holgadamente el umbral (`165..282` sinapsis, `7,15..12,21 mV`). Por eso en `T2` el corte individual `Q1_k` debe acompañarse del **corte conjunto `Q1_conj(H_m)`** (cortar las 2 o 3 filas `D_driver -> X_hub` a la vez), que decide si el hub opera como **compuerta OR** (redundancia: cortar una sola arista casi no baja `X_hub`, pero cortar todas lo apaga) o como **detector de coincidencia AND / suma integradora** (cortar una sola arista ya derrumba el freno).
3. **Estrato `T3` (Relevos subumbrales altos en hubs simples, `96 <= w <= 153`, `4,16..6,63 mV`, 4 pares):**
   * `R06`: `DNp104 (58878) -> CB0626 (676)` (`w = 153`, `6,63 mV`, `BANC = 91`).
   * `R08`: `DNa03 (96843) -> VES041 (117221)` (`w = 126`, `5,46 mV`, `BANC = 106`).
   * `R09`: `DNpe023 (27878) -> cL22b (86580)` (`w = 120`, `5,20 mV`, `BANC = 115`).
   * `R12`: `DNae007 (22415) -> PS065 (83980)` (`w = 96`, `4,16 mV`, `BANC = 159`).

### 3.3. Trampa 3 · Entradas sensoriales no visuales y blancos `D'` silentes (Freno Efectivo Rectificado)

* Doce de los 16 relevos tienen entrada directa desde `visual_projection` (`S_k` con `w >= 20`: `LPLC1_right`, `LTe65_left`, `LPT04_HST_right`, `LC9_right`, `LTe49_right`, `LPT52_right`, `LTe42b_right`, `Nod5_left`, `LTe42c_right`), pero **cuatro relevos (`R04`, `R07`, `R09`, `R14`) tienen `0` sinapsis directas desde `visual_projection`**: sus excitadores primarios son neuronas centrales/premotores del LAL y del complejo central (`LAL014`, `CB0132`, `PVLP137`, `CB0529`, `CL215`, `CL095`). Incluso en `R02` y `R03`, la entrada principal proviene del complejo central de navegación (`PFL3` con `336` sinapsis hacia `DNpe016`; `PFL2` con `599` sinapsis hacia `DNa03`).
* Además, como demostró la auditoría `2026-11-02-008`, el freno sobre `D'_k` es invisible si las neuronas blanco `D'_k` están en `0 Hz` en `C0` (no se pueden restar espigas a una neurona silente).
* **Consecuencia de diseño (Protocolo de Doble Régimen):**
  1. **Régimen A (Estímulo aferente nativo `E_nat(k)` a `150 Hz` Poisson, `n = 20` semillas):** estimula la población aferente principal de cada relevo (`S_k` visual cuando `w_SD >= 20`, o el par excitatorio presináptico principal `E_drv(k)` cuando `w_SD = 0`). Mide cuánto del freno se recluta en la red completa ante su entrada aferente natural.
  2. **Régimen B (Clamp causal estandarizado: `50 Hz` Poisson directo en `D_driver` + excitación tónica basal `25 Hz` Poisson sobre el conjunto blanco `D'_k`, `n = 20` semillas):** garantiza por construcción que `D_driver` dispare en todos los 16 relevos y que todas las neuronas blanco `D'_k` estén por encima del umbral en `C0` (`r_d(C0) > 10 Hz`), aislando la transmisión biofísica pura del motivo `D_driver -> X_hub -| D'_k` en igualdad de condiciones para los 16 pares.

---

## 4. Tabla maestra de sujetos y guardas exactas en `connectivity.parquet` (`R01` a `R16`)

Cada fila fue verificada contra `/workspace/connectivity.parquet` (`15.091.983` aristas). Para cada relevo `R_k`:
* **`Q1_k`**: anular únicamente la fila `pre == d_idx` y `post == x_idx` (**exactamente `1` fila** en los 16 casos).
* **`Q2_k`**: anular todas las salidas de `X_hub` (`pre == x_idx`).
* **`Q3_k`**: anular todas las salidas de `D_driver` (`pre == d_idx`).
* **`Q4_k`**: anular todas las entradas a `X_hub` salvo `D_driver` (`post == x_idx` y `pre != d_idx`).
* **`D'_k`**: conjunto de neuronas descendentes (`D \ {d_idx}`) que reciben inhibición directa desde `x_idx` (`w_{x_idx -> d} > 0`).

| ID | Estrato | `D_driver` (`d_idx` / `root_id` / lado) | `X_hub` (`x_idx` / `root_id` / NT) | `w_Q1` FW (`PSP`) / BANC | Guarda `Q1` `(filas, peso)` | Guarda `Q2` `(filas, peso)` | Guarda `Q3` `(filas, peso)` | Guarda `Q4` `(filas, peso)` | Espejo contralateral `(d_idx->x_idx, w)` | Entrada aferente `E_nat(k)` (`w_in`) | Blancos `D'_k`: `n` (`sum w_{XD'}` / colat `w_{DD'}`) y Top-2 `D'` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`R01`** | `T1` | `DNp35` (`59804` / `720575940623276168` / R) | `CB0527` (`30887` / `720575940617444130` / gaba) | `235` (`10,18 mV`) / `184` | `(1, 235.0)` | `(551, 4841.0)` | `(465, 2618.0)` | `(650, 5164.0)` | L: `88284->60863` (`w=221`) | `LPLC1_right` (`904`), `LC11_right` (`584`) | `137` (`2672` / `1192`): `DNa16_R(274)`, `DNa15_R(200)` |
| **`R02`** | `T1` | `DNpe016` (`61465` / `720575940623556755` / L) | `cL22c` (`80081` / `720575940627068772` / gaba) | `180` (`7,80 mV`) / `138` | `(1, 180.0)` | `(601, 6492.0)` | `(186, 1011.0)` | `(672, 4497.0)` | R: `19718->132221` (`w=174`) | `LTe65_left` (`136`) / `PFL3` (`336`) | `25` (`271` / `405`): `DNp18_R(96)`, `DNae007_R(79)` |
| **`R03`** | `T1` | `DNa03` (`96843` / `720575940630085583` / R) | `PLP060` (`116067` / `720575940634790648` / gaba) | `165` (`7,15 mV`) / `105` | `(1, 165.0)` | `(701, 6472.0)` | `(385, 4773.0)` | `(440, 4195.0)` | L: `46248->51555` (`w=148`) | `LPT04_HST_right` (`21`) / `PFL2` (`599`) | `40` (`410` / `1944`): `DNp05_R(72)`, `DNb05_R(60)` |
| **`R04`** | `T2 (H3)` | `DNpe023` (`27878` / `720575940616604817` / L) | `CB0172` (`122969` / `720575940637635305` / gaba) | `155` (`6,71 mV`) / `188` | `(1, 155.0)` | `(267, 2259.0)` | `(415, 3270.0)` | `(298, 2769.0)` | R: `110931->44709` (`w=68`) | `CENTRAL: LAL014(123), CB0132(87)` | `75` (`907` / `772`): `DNa02_R(112)`, `DNde003_R(105)` |
| **`R05`** | `T2 (H2)` | `DNp71` (`111205` / `720575940633095137` / R) | `CB0534` (`19257` / `720575940614087219` / gaba) | `154` (`6,67 mV`) / `187` | `(1, 154.0)` | `(550, 4917.0)` | `(236, 2128.0)` | `(403, 2476.0)` | L: `72597->11774` (`w=112`) | `LC9_right` (`231`), `LPLC2_right` (`180`) | `63` (`770` / `913`): `DNg74_a_L(202)`, `DNg74_a_R(193)` |
| **`R06`** | `T3` | `DNp104` (`58878` / `720575940623122125` / R) | `CB0626` (`676` / `720575940604470240` / gaba) | `153` (`6,63 mV`) / `91` | `(1, 153.0)` | `(1184, 7413.0)` | `(364, 1692.0)` | `(1196, 6951.0)` | L: `19410->117257` (`w=109`) | `LTe49_right` (`47`) / `CL086_e` (`155`) | `113` (`1318` / `218`): `DNp69_R(192)`, `DNpe043_R(69)` |
| **`R07`** | `T2 (H2)` | `DNg100` (`130297` / `720575940640978048` / L) | `CB0534` (`19257` / `720575940614087219` / gaba) | `128` (`5,54 mV`) / `82` | `(1, 128.0)` | `(550, 4917.0)` | `(472, 2753.0)` | `(403, 2502.0)` | R: `135733->11774` (`w=42`) | `CENTRAL: PVLP137(381), CB0529(296)` | `64` (`775` / `725`): `DNg74_a_L(202)`, `DNg74_a_R(193)` |
| **`R08`** | `T3` | `DNa03` (`96843` / `720575940630085583` / R) | `VES041` (`117221` / `720575940635202204` / gaba) | `126` (`5,46 mV`) / `106` | `(1, 126.0)` | `(1001, 8265.0)` | `(385, 4773.0)` | `(1487, 11273.0)` | L: `46248->81321` (`w=105`) | `LPT04_HST_right` (`21`) / `PFL2` (`599`) | `70` (`404` / `1944`): `DNa03_L(170)`, `DNpe023_L(13)` |
| **`R09`** | `T3` | `DNpe023` (`27878` / `720575940616604817` / L) | `cL22b` (`86580` / `720575940628154364` / gaba) | `120` (`5,20 mV`) / `115` | `(1, 120.0)` | `(1066, 9308.0)` | `(415, 3270.0)` | `(918, 6813.0)` | R: `110931->97451` (`w=51`) | `CENTRAL: LAL014(123), CB0132(87)` | `56` (`608` / `772`): `DNpe016_L(310)`, `DNp05_R(48)` |
| **`R10`** | `T2 (H1)` | `DNp47` (`41594` / `720575940620038779` / R) | `CB0580` (`33912` / `720575940618165393` / gaba) | `115` (`4,98 mV`) / `98` | `(1, 115.0)` | `(1616, 10297.0)` | `(423, 2136.0)` | `(1228, 6487.0)` | L: `23197->33912` (`w=88`) | `LPT52_right` (`62`) / `CB3111` (`127`) | `138` (`1928` / `575`): `DNp09_R(212)`, `DNp71_R(154)` |
| **`R11`** | `T2 (H4)` | `DNa06` (`129110` / `720575940640325429` / R) | `PS100` (`45293` / `720575940620746478` / gaba) | `111` (`4,81 mV`) / `94` | `(1, 111.0)` | `(507, 3690.0)` | `(328, 3436.0)` | `(686, 7835.0)` | L: `69226->112031` (`w=77`) | `LPT04_HST_right` (`31`) / `CB0581` (`290`) | `192` (`2330` / `937`): `DNa16_R(272)`, `DNa15_R(149)` |
| **`R12`** | `T3` | `DNae007` (`22415` / `720575940615043222` / R) | `PS065` (`83980` / `720575940627715870` / gaba) | `96` (`4,16 mV`) / `159` | `(1, 96.0)` | `(438, 3479.0)` | `(313, 2380.0)` | `(505, 5383.0)` | L: `99517->111648` (`w=72`) | `LTe42b_right` (`55`) / `CB0755` (`157`) | `62` (`655` / `1222`): `DNpe022_R(152)`, `DNp57_R(80)` |
| **`R13`** | `T2 (H1b)` | `DNp104` (`58878` / `720575940623122125` / R) | `CB0580` (`58129` / `720575940622998627` / gaba) | `93` (`4,03 mV`) / `85` | `(1, 93.0)` | `(1140, 5354.0)` | `(364, 1692.0)` | `(1074, 5349.0)` | L: `19410->33912` (`w=72`) | `LTe49_right` (`47`) / `CL086_e` (`155`) | `113` (`979` / `218`): `DNp09_R(134)`, `DNp71_R(129)` |
| **`R14`** | `T2 (H1)` | `DNp101` (`104203` / `720575940631483695` / L) | `CB0580` (`33912` / `720575940618165393` / gaba) | `91` (`3,94 mV`) / `109` | `(1, 91.0)` | `(1616, 10297.0)` | `(257, 2489.0)` | `(1228, 6511.0)` | R: `71368->58129` (`w=87`) | `CENTRAL: CL215(143), CL095(113)` | `139` (`1963` / `1135`): `DNp09_R(212)`, `DNp71_R(154)` |
| **`R15`** | `T2 (H4b)` | `DNge148` (`84751` / `720575940627845704` / R) | `PS100` (`112031` / `720575940633308371` / glut) | `88` (`3,81 mV`) / `81` | `(1, 88.0)` | `(439, 2780.0)` | `(324, 1464.0)` | `(576, 5739.0)` | L: `53975->45293` (`w=87`) | `Nod5_left` (`20`) / `DNpe028` (`37`) | `173` (`1818` / `237`): `DNa16_L(211)`, `DNg75_L(113)` |
| **`R16`** | `T2 (H3)` | `DNae005` (`20277` / `720575940614403178` / R) | `CB0172` (`122969` / `720575940637635305` / gaba) | `88` (`3,81 mV`) / `82` | `(1, 88.0)` | `(267, 2259.0)` | `(242, 1722.0)` | `(298, 2836.0)` | L: `6882->44709` (`w=77`) | `LTe42c_right` (`212`) / `CB0316` (`230`) | `75` (`917` / `1025`): `DNa02_R(112)`, `DNde003_R(105)` |

---

## 5. Guardas exactas de los cortes conjuntos en hubs convergentes (`Q1_conj` y `Q4_conj`) y de la cascada desinhibitoria (`R01_desinhibido`)

Medidas directamente sobre `/workspace/connectivity.parquet`:

| ID Hub / Cascada | Nodo `X_hub` (`x_idx`) | Drivers `D_driver` convergentes (`d_idx`) | Guarda `Q1_conj` `(filas, peso_abs)` | Guarda `Q4_conj` `(filas, peso_abs)` | Suma `PSP` conjunta | Hipótesis que decide |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`H1_CB0580_33912`** | `CB0580` (`33912`) | `DNp47_R (41594)`, `DNp101_L (104203)`, `DNp104_L (19410)` | `(3, 278.0)` | `(1226, 6324.0)` | `12,04 mV` | Sinergia / compuerta entre `R10`, `R14` y espejo de `R13` sobre `CB0580` (`33912`) |
| **`H1b_CB0580_58129`** | `CB0580` (`58129`) | `DNp104_R (58878)`, `DNp101_R (71368)` | `(2, 180.0)` | `(1073, 5262.0)` | `7,80 mV` | Sinergia / compuerta entre `R13` y espejo de `R14` sobre `CB0580` (`58129`) |
| **`H2_CB0534_19257`** | `CB0534` (`19257`) | `DNp71_R (111205)`, `DNg100_L (130297)` | `(2, 282.0)` | `(402, 2348.0)` | `12,21 mV` | Sinergia / compuerta entre `R05` (visual `LC9`) y `R07` (central `PVLP137`) sobre `CB0534` |
| **`H3_CB0172_122969`** | `CB0172` (`122969`) | `DNpe023_L (27878)`, `DNae005_R (20277)` | `(2, 243.0)` | `(297, 2681.0)` | `10,52 mV` | Sinergia / compuerta entre `R04` (central `LAL014`) y `R16` (visual `LTe42c`) sobre `CB0172` |
| **`H4_PS100_45293`** | `PS100` (`45293`) | `DNa06_R (129110)`, `DNge148_L (53975)` | `(2, 198.0)` | `(685, 7748.0)` | `8,57 mV` | Sinergia / compuerta entre `R11` y espejo de `R15` sobre `PS100` (`45293`) |
| **`H4b_PS100_112031`** | `PS100` (`112031`) | `DNge148_R (84751)`, `DNa06_L (69226)` | `(2, 165.0)` | `(575, 5662.0)` | `7,15 mV` | Sinergia / compuerta entre `R15` y espejo de `R11` sobre `PS100` (`112031`) |
| **`R01_desinhibido`** | `CB0527` (`30887`) + `AVLP080` (`6128`) | `Q6(AVLP080=0) ∪ Q1(DNp35->CB0527=0)` | `(1678, 18858.0)` vs `Q6=(1677, 18623.0)` | — | `10,18 mV` (una vez liberada `DNp35`) | Prueba de cascada desinhibitoria `AVLP080 -| DNp35 -> CB0527 -| D'` bajo `LPLC1_right` |

---

## 6. Condiciones causales, métricas y corrección de las dos trampas metodológicas de `006`

El diseño incorpora dos correcciones obligatorias respecto de `SELLO-DNP04-2026-11-02.md` (detectadas en el hallazgo `R3` de la auditoría `2026-11-02-01`):

1. **Estadístico sensible a la magnitud (no sólo al signo):** Además del test exacto de permutación de signos sobre `n = 20` semillas pareadas (`p_signo`, cuyo piso es `2 / 2^20 = 1,907e-6` cada vez que los 20 ensayos comparten signo), toda afirmación primaria exige **intervalo de confianza bootstrap BCa al 95 % sobre la magnitud media (`IC95_inf(r_Q1)`)** y **estadístico de Wilcoxon / t pareado sobre las diferencias continuas**.
2. **Exclusión del auto-disparo de neuronas silenciadas por `peso_saliente = 0`:** Cuando una condición silencia `D_driver` (`Q3_k`) o `X_hub` (`Q2_k`) anulando sus filas salientes (`pre == idx`), la neurona silenciada sigue integrando sus propias entradas y disparando espigas que no salen a la red. Por tanto:
   * El conjunto blanco `D'_k` excluye siempre a `d_idx` (y en `Q1_conj`, excluye a todos los `d_idx` del hub).
   * La lectura funcional de `Q2_k` se mide sobre `D'_k`, nunca sobre el conteo interno de `x_idx`.

### Métricas por relevo `R_k` (en cada régimen A y B, `n = 20` ensayos pareados `s = 0..19` de `1000 ms`):

Sea `F_k(C) = sum_{d in D'_k} espigas_d(C)` sobre las descendentes blanco de `x_idx`, y `F_hub(C) = espigas_{x_idx}(C)`:

1. **Fracción del freno de `X_hub` gobernada por la única fila `D_driver -> X_hub`:**
   `r_Q1(k) = (F_k(Q1_k) - F_k(C0)) / max(F_k(Q2_k) - F_k(C0), 1e-9)`
   *(Nota: se normaliza contra `F_k(Q2_k) - F_k(C0)`, es decir el freno total que ejerce ese `X_hub` sobre sus blancos `D'_k`, además de reportar `r_Q1_global(k) = (F_k(Q1_k) - F_k(C0)) / (F_k(C1) - F_k(C0))` respecto de toda la población `X`).*
2. **Caída de actividad de `X_hub` al cortar la única fila `D_driver -> X_hub`:**
   `c_X(k) = (F_hub(C0) - F_hub(Q1_k)) / max(F_hub(C0), 1e-9)`
3. **Suficiencia de `D_driver` sola para sostener a `X_hub` (`Q4_k`):**
   `s4(k) = F_hub(Q4_k) / max(F_hub(C0), 1e-9)`
4. **Índice de sinergia en los 4 hubs convergentes (`T2`, `H_m`):**
   `I_sinergia(H_m) = (F_hub(C0) - F_hub(Q1_conj(H_m))) / max(sum_{k in H_m} (F_hub(C0) - F_hub(Q1_k)), 1e-9)`
   * Si `I_sinergia(H_m) > 1,25`: **compuerta OR / saturación** (los drivers individuales son redundantes; hace falta cortar el conjunto para apagar el hub).
   * Si `I_sinergia(H_m) < 0,80`: **compuerta AND / facilitación supralineal** (cortar un solo driver ya desarma la coincidencia subumbral).
   * Si `0,80 <= I_sinergia(H_m) <= 1,25`: **suma cuasi-lineal**.
5. **Balance colateral neto de `D_driver` (`Q3_k` vs `Q1_k`):**
   Como varios `D_driver` tienen excitación colateral directa `D_driver -> D'_k` fuerte (p. ej. `R03 DNa03` tiene `1.944` sinapsis excitatorias directas a `D'` contra `410` inhibitorias vía `PLP060`), se mide `Delta_colat(k) = F_k(Q1_k) - F_k(Q3_k)`, separando el freno disináptico `D_driver -> X_hub -| D'_k` de la excitación monosináptica `D_driver -> D'_k`.

---

## 7. Criterios de decisión preregistrados y controles negativos (`H_MECANISMO_RELEVOS16`)

* **Guarda de activación previa (`G_ACT`):** Un relevo `R_k` está en régimen dinámicamente informativo sólo si en `C0` el driver dispara `F_{d_idx}(C0) >= 10,0 Hz`, el hub dispara `F_hub(C0) >= 10,0 Hz` y el freno del hub es positivo (`F_k(Q2_k) - F_k(C0) >= 5,0 Hz` con `p_Holm < 0,05`). Si en el Régimen A (sensorial nativo) no pasa `G_ACT` (como ocurre con `R01` en `LPLC1` antes de desinhibir `AVLP080`), el Régimen A se etiqueta `BLOQUEADO_AGUAS_ARRIBA` y el veredicto del eslabón se evalúa en `Q1_desinhibido` y en el Régimen B.
* **Predicción por estrato biofísico (`P_ESTRATOS`):**
  1. **En `T1` (`R01`, `R02`, `R03`, `w >= 162` sinapsis, `PSP >= 7,0 mV`):** la única fila `Q1_k` captura por sí sola `r_Q1(k) >= 0,35` y `s4(k) >= 0,50` con `p_Holm < 0,01` en los 3 pares (réplica de `DNp04 -> PVLP010` en otros tres circuitos independientes).
  2. **En `T2` (`R04, R05, R07, R10, R11, R13, R14, R15, R16`, hubs convergentes `CB0580`, `CB0534`, `CB0172`, `PS100`):** el corte conjunto `Q1_conj(H_m)` supera `r_Q1_conj(H_m) >= 0,40` y reduce `F_hub` en `>= 40 %` (`p_Holm < 0,01`) en al menos 3 de los 4 hubs convergentes, superando al promedio de los cortes individuales `Q1_k`.
  3. **En `T1 ∪ T2 ∪ T3` (los 16 relevos):** el **Freno Efectivo Rectificado** `B_eff(X_k, E) = r_{X_k}(C0) * sum_{d in D'_k} w_{X_k -> d} * min(1, r_d(C0) / (r_d(C0) + 10))` predice la fracción de liberación de cada hub con `R^2 >= 0,75` y `p < 0,005` contra el control negativo de permutación de blancos `D'`.
* **Controles negativos obligatorios:**
  1. **`CN1` (Corte de fila débil apareada `w <= 5`):** Para cada `R_k`, cortar una fila excitatoria `D_weak -> X_hub` de peso `1 <= w <= 5` sinapsis (`1` fila). Debe dar `|r_Q1_weak(k)| < 0,05`. Si da `>= 0,10`, el protocolo queda `INVALIDO`.
  2. **`CN2` (Permutación de tasas `r_d(C0)` en `B_eff`):** Barajar 10.000 veces la identidad de las tasas basales `r_d(C0)` entre los blancos `D'_k`. El `R^2` real debe superar al percentil 99 del nulo.
  3. **`CN3` (Verificador independiente con `--parquet` obligatorio):** Todo recibo de corrida de `H_MECANISMO_RELEVOS16` debe commitear el log de verificación corriendo contra `/workspace/connectivity.parquet` y contrastando las tuplas exactas `(filas, peso_abs)` de las Secciones 4 y 5.

---

## 8. Evidencia cruda verbatim (`sello_diseno_16_relevos.log`)

Comando ejecutado en `brain-env`:
`python3 /workspace/dnp04/verif/armar_sello_16_relevos.py`

Hashes SHA-256:
* `f60624380e6344f21be5cc8608ba6ea913bf1971687c2d683eb91b3f845b2f62  /workspace/dnp04/verif/armar_sello_16_relevos.py`
* `00bf832c3697d76c70d6d5594b44b550217e5bb4540e1c898b4b6d950341f8bb  /workspace/dnp04/verif/sello_diseno_16_relevos.json`
* `92cb401930ac43033c7e382d1a0f7d9f507a0779f5b84a7cf6337ba487a136c2  /workspace/dnp04/verif/sello_diseno_16_relevos.log`

Salida literal:
* `Saved /workspace/dnp04/verif/sello_diseno_16_relevos.json (31672 bytes)`
* `R01 [T1] DNp35   ( 59804)->CB0527  ( 30887) w=235(10.18mV)/BANC=184 | Q1..Q4=1/551/465/650 | Mir:left(88284->60863,w=221) | In:[LPLC1_right(904)] | D':n=137 sum_XD'=2672 colat_DD'=1192 [DNa16_right(274), DNa15_right(200), DNa16_left(194)]`
* `R02 [T1] DNpe016 ( 61465)->cL22c   ( 80081) w=180(7.80mV)/BANC=138 | Q1..Q4=1/601/186/672 | Mir:right(19718->132221,w=174) | In:[LTe65_left(136)] | D':n= 25 sum_XD'= 271 colat_DD'= 405 [DNp18_right(96), DNae007_right(79), DNpe017_right(28)]`
* `R03 [T1] DNa03   ( 96843)->PLP060  (116067) w=165(7.15mV)/BANC=105 | Q1..Q4=1/701/385/440 | Mir:left(46248->51555,w=148) | In:[LPT04_HST_right(21)] | D':n= 40 sum_XD'= 410 colat_DD'=1944 [DNp05_right(72), DNb05_right(60), DNpe037_right(53)]`
* `R04 [T2] DNpe023 ( 27878)->CB0172  (122969) w=155(6.71mV)/BANC=188 | Q1..Q4=1/267/415/298 | Mir:right(110931->44709,w=68) | In:[CENTRAL:LAL014(123),CB0132(87)] | D':n= 75 sum_XD'= 907 colat_DD'= 772 [DNa02_right(112), DNde003_right(105), DNa13_right(82)]`
* `R05 [T2] DNp71   (111205)->CB0534  ( 19257) w=154(6.67mV)/BANC=187 | Q1..Q4=1/550/236/403 | Mir:left(72597->11774,w=112) | In:[LC9_right(231)] | D':n= 63 sum_XD'= 770 colat_DD'= 913 [DNg74_a_left(202), DNg74_a_right(193), DNge144_right(55)]`
* `R06 [T3] DNp104  ( 58878)->CB0626  (   676) w=153(6.63mV)/BANC= 91 | Q1..Q4=1/1184/364/1196 | Mir:left(19410->117257,w=109) | In:[LTe49_right(47)] | D':n=113 sum_XD'=1318 colat_DD'= 218 [DNp69_right(192), DNpe043_right(69), DNp69_left(69)]`
* `R07 [T2] DNg100  (130297)->CB0534  ( 19257) w=128(5.54mV)/BANC= 82 | Q1..Q4=1/550/472/403 | Mir:right(135733->11774,w=42) | In:[CENTRAL:PVLP137(381),CB0529(296)] | D':n= 64 sum_XD'= 775 colat_DD'= 725 [DNg74_a_left(202), DNg74_a_right(193), DNge144_right(55)]`
* `R08 [T3] DNa03   ( 96843)->VES041  (117221) w=126(5.46mV)/BANC=106 | Q1..Q4=1/1001/385/1487 | Mir:left(46248->81321,w=105) | In:[LPT04_HST_right(21)] | D':n= 70 sum_XD'= 404 colat_DD'=1944 [DNa03_left(170), DNpe023_left(13), DNa16_left(12)]`
* `R09 [T3] DNpe023 ( 27878)->cL22b   ( 86580) w=120(5.20mV)/BANC=115 | Q1..Q4=1/1066/415/918 | Mir:right(110931->97451,w=51) | In:[CENTRAL:LAL014(123),CB0132(87)] | D':n= 56 sum_XD'= 608 colat_DD'= 772 [DNpe016_left(310), DNp05_right(48), DNp102_left(43)]`
* `R10 [T2] DNp47   ( 41594)->CB0580  ( 33912) w=115(4.98mV)/BANC= 98 | Q1..Q4=1/1616/423/1228 | Mir:left(23197->33912,w=88) | In:[LPT52_right(62)] | D':n=138 sum_XD'=1928 colat_DD'= 575 [DNp09_right(212), DNp71_right(154), DNp71_left(131)]`
* `R11 [T2] DNa06   (129110)->PS100   ( 45293) w=111(4.81mV)/BANC= 94 | Q1..Q4=1/507/328/686 | Mir:left(69226->112031,w=77) | In:[LPT04_HST_right(31)] | D':n=192 sum_XD'=2330 colat_DD'= 937 [DNa16_right(272), DNa15_right(149), DNa04_right(148)]`
* `R12 [T3] DNae007 ( 22415)->PS065   ( 83980) w= 96(4.16mV)/BANC=159 | Q1..Q4=1/438/313/505 | Mir:left(99517->111648,w=72) | In:[LTe42b_right(55)] | D':n= 62 sum_XD'= 655 colat_DD'=1222 [DNpe022_right(152), DNp57_right(80), DNp05_right(78)]`
* `R13 [T2] DNp104  ( 58878)->CB0580  ( 58129) w= 93(4.03mV)/BANC= 85 | Q1..Q4=1/1140/364/1074 | Mir:left(19410->33912,w=72) | In:[LTe49_right(47)] | D':n=113 sum_XD'= 979 colat_DD'= 218 [DNp09_right(134), DNp71_right(129), DNpe024_right(52)]`
* `R14 [T2] DNp101  (104203)->CB0580  ( 33912) w= 91(3.94mV)/BANC=109 | Q1..Q4=1/1616/257/1228 | Mir:right(71368->58129,w=87) | In:[CENTRAL:CL215(143),CL095(113)] | D':n=139 sum_XD'=1963 colat_DD'=1135 [DNp09_right(212), DNp71_right(154), DNp71_left(131)]`
* `R15 [T2] DNge148 ( 84751)->PS100   (112031) w= 88(3.81mV)/BANC= 81 | Q1..Q4=1/439/324/576 | Mir:left(53975->45293,w=87) | In:[Nod5_left(20)] | D':n=173 sum_XD'=1818 colat_DD'= 237 [DNa16_left(211), DNg75_left(113), DNa15_left(110)]`
* `R16 [T2] DNae005 ( 20277)->CB0172  (122969) w= 88(3.81mV)/BANC= 82 | Q1..Q4=1/267/242/298 | Mir:left(6882->44709,w=77) | In:[LTe42c_right(212)] | D':n= 75 sum_XD'= 917 colat_DD'=1025 [DNa02_right(112), DNde003_right(105), DNa13_right(82)]`

---

## 9. Archivos generados

* `docs/auditorias/evidencia/2026-11-02-02/armar_sello_16_relevos.py` (commit `bef3cd2b7fda41ace25b50e87d660c6033eaa05b`, blob `ee7ce82e5fb2251a0c24286fcb252323f14505ab`).
* `docs/auditorias/evidencia/2026-11-02-02/sello_diseno_16_relevos.json` (commit `ddb62475470c863a7d2389a2612052f3e425e8a9`, blob `4fe9ac1e5ba418dbb39470ae703797b311f59a4a`).
* `docs/agents/respuestas/2026-11-02-009-diseno-corte-causal-16-relevos-recurrentes.md` (este documento, en `main`).

---

## 10. NO MEDIDO

* **Ejecución de las corridas Brian2 de `H_MECANISMO_RELEVOS16` (Régimen A y Régimen B):** **NO MEDIDO**. Este documento entrega el diseño experimental sellado y las guardas exactas verificadas sobre `connectivity.parquet` antes de lanzar las simulaciones LIF en Actions/Kaggle.
* **Causalidad biológica en vivo en *Drosophila* para `R01..R16`:** **NO MEDIDO**.

--- METODO PROMETEO ---
Maquina: brain-env (contenedor persistente)
Instrumentos: /workspace/dnp04/verif/disenar_16_relevos.py, /workspace/dnp04/verif/chequear_16_en_4estimulos.py, /workspace/dnp04/verif/armar_sello_16_relevos.py
Doc principal: https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29177
--- FIN METODO PROMETEO ---
