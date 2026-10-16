# 065 · El LC6→GF sobrevive el null anatómico, y aparece una tabla de ruteo

**Fecha:** 2026-08-25 01:10 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «EL LC6→GF SOBREVIVIÓ · este cero sí es una prohibición»
> **🔬 Evidencia cruda:** `docs/agents/evidencia/2026-08-25-escape-neuropil-null-evidencia-cruda.md`
> **🛠 Instrumento:** `src/escape_neuropil_null.py`, md5 `c04ddd4282ada4f9df462f87d84d85ba`

---

## 1. Pedido

«Testeá el LC6→GF contra neuropilos.» Era el ítem 7 de los NO MEDIDO de la resp 063 y la deuda más barata que quedaba.

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 8 sobre `brain-env` | solo `/tmp` | **NO** |
| `githubmcp_create_or_update_file` × 3 | sí, **rama `titan/twohop-nulls`** | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero Kaggle. Nada a Zenodo. `/workspace` solo leído. Ningún merge.** CPU: 234,6 s.

---

## 3. 🔥 EL VEREDICTO: este cero SÍ es una prohibición

**Y salió al revés del cero de las motoras de cabeza. Ese era geometría; este no.**

```
LC6 -> Giant Fiber
  observado:      0
  null predice:   17,2 ± 3,1
  z:              -5,61
  40/40 realizaciones por encima, y la MÍNIMA de las 40 da 12
```

**Ninguna de las 40 realizaciones bajó de 12.** El null que preserva neuropilos, o sea el único control capaz de matar este hallazgo, **no lo mata**.

### Y hay una prueba que no necesita estadística, y es la más clara

Medí dónde pone sus sinapsis cada población. **El neuropilo dominante de salida de LC6 es PVLP (68.082 sitios). El neuropilo dominante de entrada del Giant Fiber es PVLP (4.085 sitios). Comparten el territorio principal.**

Y la cota de oportunidad, `shared_min_sites`:

| Par | Sitios compartidos | Aristas reales |
|---|---|---|
| **LC6 → GF** | **5.335** | **0** |
| LPLC2 → GF | 5.075 | 189 |
| LC9 → GF | 5.335 | 0 |
| **LC4 → GF** | **4.523** | **104** |
| LPLC1 → GF | 4.478 | 0 |

> **LC6 tiene MÁS oportunidad de conectar que LC4 (5.335 contra 4.523) y conecta CERO donde LC4 conecta 104.**

**Eso no se arregla con ninguna explicación de localidad.** Están en el mismo barrio, LC6 tiene más presencia que LC4 en ese barrio, y no toca la puerta.

**«Exclusión activa» vuelve a ser la palabra correcta**, después de que la resp 060 la bajó a «ausencia de vía» por prudencia. La prudencia era correcta: no se sabía. Ahora se sabe.

---

## 4. 🆕 Y apareció algo que no buscaba: una TABLA DE RUTEO cruzado

Metí LC9 y LPLC1 como controles, esperando que dieran «nada» y demostraran que el null no marca a todos los tipos visuales. **Dieron mucho más que eso.**

| Fuente | → Giant Fiber | → DNp09 |
|---|---|---|
| **LC4** | **104** · null 9,6 · **10,8×** · z +31,6 · 0/40 | **0** · null 5,0 · z −2,4 · 40/40 |
| **LPLC2** | **189** · null 19,4 · **9,8×** · z +39,0 · 0/40 | **32** · null 11,4 · **2,8×** · z +5,9 · 0/40 |
| **LC6** | **0** · null 17,2 · z **−5,6** · 40/40 | **1** · null 8,7 · z −3,0 · 40/40 |
| **LC9** | **0** · null 11,9 · z **−4,0** · 40/40 | **114** · null 15,1 · **7,6×** · z **+28,5** · 0/40 |
| **LPLC1** | 0 · null 0,2 · **NO TESTEABLE** | **0** · null 16,8 · z **−4,9** · 40/40 |

**Cinco tipos visuales que viven todos en el mismo neuropilo, y cada uno tiene un patrón de salida distinto y específico:**

- **LC4** entra al canal rápido y **está excluido del segundo canal**.
- **LPLC2** es el único que entra a **los dos**.
- **LC9 está excluido del Giant Fiber y enriquecido 7,6× en DNp09.** O sea: **no es que LC9 no esté cableado, está cableado al OTRO canal.**
- **LC6** está excluido de los dos.
- **LPLC1** está excluido de DNp09, y su cero hacia el GF **sí es geometría** (el null predice 0,2).

**Eso es exactamente lo que una hoja de datos necesita, y es mucho mejor que «fan-in exclusivo»:** no hay un circuito de escape con un vecino bloqueado, hay una **matriz de ruteo** donde cada detector tiene asignado su canal descendente, y las asignaciones **sobreviven al control anatómico**.

### 🟢 Y predice, desde el cableado, un resultado compilado que ya teníamos

Cuando compilé el circuito con el motor, medí que **LC4 casi no activa DNp09 (0,075) mientras LPLC2 sí (0,658)**, y lo anoté como «algo que no busqué».

**El cableado lo predecía:** `LC4 → DNp09 = 0` contra 5,0 esperadas, y `LPLC2 → DNp09 = 32` contra 11,4, o sea **2,8× enriquecido**. La estructura y la simulación coinciden, y se midieron por separado y con meses de diferencia. **Eso es una validación cruzada que no se pidió.**

---

## 5. La entrada corregida para la biblioteca

> **Ruteo visual→descendente por canal, con exclusión verificada.**
> Cinco tipos de proyección visual co-localizados en PVLP, dos canales descendentes de 2 neuronas cada uno.
> **Asignaciones que sobreviven a un null que preserva neuropilos (40 realizaciones):** LC4→GF **10,8×** · LPLC2→GF **9,8×** · LPLC2→DNp09 **2,8×** · LC9→DNp09 **7,6×**.
> **Exclusiones que sobreviven al mismo null:** LC6→GF (z −5,6) · LC9→GF (z −4,0) · LPLC1→DNp09 (z −4,9) · LC4→DNp09 (z −2,4).
> **Ganancia funcional medida compilando:** 40× entre una entrada cableada y una excluida.
> **Selectividad temporal: 1,04×**, o sea ninguna. Es un integrador. **0 aristas inhibitorias de 13.026.**
> **Límites:** el cero de LPLC1→GF **es** geometría (null ≈ 0) y va marcado como tal. La co-localización se mide a nivel de neuropilo, **no de distancia entre árboles**. Sin umbral de sinapsis.

**Esta entrada dice qué hace, qué no hace, y cómo se verificó cada línea.** Es la primera de la biblioteca con exclusiones medidas contra el control fuerte, y sube de 1 a 1 el conteo de motivos (**sigue siendo un motivo, ahora mucho mejor caracterizado**, no dos).

---

## 6. 🔴 Una discrepancia histórica encontrada y resuelta

| Cantidad | Medición vieja | Esta corrida |
|---|---|---|
| LC4→GF, LPLC2→GF, LC6→GF | 104 / 189 / 0 | **104 / 189 / 0** ✅ exacto |
| LPLC2 → DNp09 | **170** | **32** 🔴 |
| población DNp09 | **4** | **2** 🔴 |

Medido:

```
cell_type == 'DNp09'      -> N=2, LPLC2->DNp09 = 32 aristas
hemibrain_type == 'DNp09' -> N=4, LPLC2->DNp09 = 170 aristas
hemibrain_type con DNp01  -> []   (el GF solo existe como cell_type)
```

**Las dos son correctas: son poblaciones distintas y nunca se declaró cuál se usaba.** Es el modo de falla 5 de este proyecto (comparar cantidades con criterios distintos), sexta aparición.

**El resultado central no se afecta**, porque el Giant Fiber tiene una sola definición posible y los tres números históricos se reproducen exactos. **Pero los ratios →DNp09 de este turno valen para la población de 2 y NO son comparables con el 3,6× histórico.**

---

## 7. Lo que esto le hace al expediente

**Ahora hay dos ceros medidos contra el control fuerte, y dan resultados opuestos:**

| Cero | Contra el null anatómico | Veredicto |
|---|---|---|
| visual/olfatorio → motoras de cabeza | el null predice ≈ **0** | 🔴 **geometría.** NO TESTEABLE |
| **LC6 → Giant Fiber** | el null predice **17,2 ± 3,1** | 🟢 **prohibición real** |

**Y esa comparación es el aporte metodológico del expediente, más que cualquiera de los dos ceros por separado:** un cero en un conectoma **no significa nada por sí mismo**. Significa una cosa si las poblaciones no se tocan y la opuesta si comparten territorio. **La forma de distinguirlo es medir la oportunidad y después correr el null que la preserva.** Los dos casos están ahora medidos con el mismo instrumento y dan lados opuestos, lo que es la mejor demostración posible de que el método discrimina.

---

## 8. NO MEDIDO, declarado

1. **`shared_min_sites` es una cota de oportunidad, no contacto.** Dos neuronas con sitios en el mismo neuropilo pueden estar a decenas de micrones. **No se midió distancia entre árboles**, y ese es el control que sigue.
2. **El null asigna un neuropilo dominante por neurona**, no reparte sinapsis: misma familia que el NPC de Lin, no idéntico.
3. **No preserva el grado entrante exacto**, solo dentro de bloque.
4. **Sin umbral de ≥5 sinapsis.** No comparable con Lin ni Bates hasta re-correrlo.
5. **Los pares →DNp09 no se re-corrieron con la definición de 4 neuronas.**
6. **No se barrió la literatura.** El circuito LC4/LPLC2→GF es conocido; **lo que sería propio es esta tabla de exclusiones contra null, y no verifiqué si ya está publicada.** Es exactamente el error que las últimas cuatro respuestas corrigieron, así que **queda como el pendiente más importante de este hallazgo.**
7. **No se compiló la tabla nueva.** La ganancia de 40× es de la corrida vieja y con la topología vieja; **LC9→DNp09 nunca se compiló.**
8. **No se midió la pureza de los bloques**, o sea cuánto margen real de movimiento le queda al null en el bloque PVLP→PVLP.
9. **Los contextos y la entrada de la biblioteca no están actualizados en este archivo.** Es el commit que sigue.
