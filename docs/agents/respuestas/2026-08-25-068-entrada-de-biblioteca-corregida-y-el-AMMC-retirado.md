# 068 · Entrada de biblioteca corregida, y el AMMC retirado

**Fecha:** 2026-08-25 01:35 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** «ENTRADA 01 CORREGIDA · el GF no es un circuito visual, y tampoco es lo que dije hace diez minutos»
> **📋 La entrada:** `docs/BIBLIOTECA-01-giant-fiber.md`

---

## 1. Pedido

«Corregí la entrada de biblioteca con lo mecanosensorial.»

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 2 sobre `brain-env` | solo `/tmp` | **NO** |
| `githubmcp_create_or_update_file` × 2 | sí, rama `titan/twohop-nulls` | no |
| `create_document` × 1 | sí, ClickUp | no |

**Cero Kaggle. Nada a Zenodo. `/workspace` solo leído. Ningún merge.**

---

## 3. 🔴 Lo primero: la medición refutó el motivo por el que iba a corregir

El ítem 5 de los NO MEDIDO de la resp 067 decía: *«el hallazgo del AMMC sale de su tabla de ROI, no de medición propia. Hay que re-medirlo antes de escribirlo en ninguna parte.»*

**Lo re-medí antes de escribir, y no se sostiene.**

| Lo que dije en la resp 067 | Lo medido |
|---|---|
| «el GF recibe **más del AMMC (33,5%)** que del PVLP visual (30,7%)» | **la entrada sensorial DIRECTA es 187 sinapsis de 9.474 = 2,0%** |

**El 33,5% del Explorer es dónde están LOCALIZADAS las sinapsis de entrada del GF, no quién se las da.** Leí una columna de **localización anatómica** como si fuera de **origen de señal**.

Medido, cruzando neuropilo de origen del socio contra su clase: de las **2.126** sinapsis que llegan desde AMMC, SAD, GNG y WED, **solo 187 son sensoriales directas**. El resto entra por interneuronas centrales (CB0010 con 223, CB3877 con 80, SAD014 con 74) y por **DNp70** con **587**.

**Es E-01 por séptima vez, y la peor versión hasta ahora:** el turno anterior corrigió un claim mío leyendo prior art, y **al leerlo cometí el mismo tipo de error sobre la fuente nueva**. La regla «verificar el sujeto exacto» estaba escrita, citada en ese mismo archivo, y la incumplí en el párrafo siguiente.

**Lo único que me salvó fue haberlo declarado como NO MEDIDO en vez de escribirlo como hallazgo.** El ítem que puse yo mismo es el que lo atrapó.

---

## 4. 🔥 Pero apareció algo más grande, y ese sí corrige la entrada

Midiendo las **962 aristas de entrada reales** del Giant Fiber:

```
super_class            aristas   sinapsis      %
central                    567      6.403   67,6%
visual_projection          299      1.899   20,0%
descending                  32        831    8,8%
sensory                     39        187    2,0%
ascending                   19        127    1,3%
visual_centrifugal           6         27    0,3%

SIGNO:   +1  595 aristas  4.752 sinapsis  (50,2%)
         -1  367 aristas  4.722 sinapsis  (49,8%)
```

**Dos hechos que rompen la entrada v1:**

1. **La vía visual es el 20,0% del presupuesto de entrada.** Los dos tercios son **control central**.
2. **El 49,8% de las sinapsis de entrada son INHIBITORIAS.** Y las inhibitorias son más pesadas por arista: 12,9 sinapsis contra 8,0.

La entrada v1 decía *«fan-in exclusivo, 314 detectores → 2 actuadores, **0 aristas inhibitorias de 13.026**»*.

> **El «0 inhibitorias» era cierto de un recorte del 20% que presenté como si fuera el circuito.**

### 🟢 Y eso explica el resultado funcional que nunca supe interpretar

El circuito compilado dio **selectividad temporal 1,04×**, o sea ninguna, y lo anoté como «la topología define ruteo y ganancia, no selectividad».

**Se compiló el 20% excitatorio.** Le faltaba el 67,6% central y el 49,8% inhibitorio. **No es que la topología no genere selectividad: es que se compiló un recorte que no puede generarla.**

**Y ahora el circuito tiene una predicción falsable propia, por primera vez:** compilar las 962 aristas con signo y ver si la selectividad temporal aparece. **Si aparece, «la topología no explica la función» se retira. Si no aparece, se refuerza con evidencia mucho mejor.** Cualquiera de los dos resultados sirve.

---

## 5. Qué quedó en la entrada corregida

`docs/BIBLIOTECA-01-giant-fiber.md`, **versión 2**, nueve secciones. Los cambios de fondo:

| Antes | Ahora |
|---|---|
| «fan-in exclusivo con doble canal» | **«cuello de botella que integra entrada multimodal»**, con el presupuesto de entrada completo |
| «0 inhibitorias de 13.026» | **«49,8% de las sinapsis de entrada son inhibitorias»**, y el 0 se declara como propiedad del recorte |
| la tabla de ruteo como hallazgo | **prior art obligatorio** (Wu, von Reyn, Ache, Morimoto, Kind, FAFB Cell Type Explorer) y el aporte reducido a **las columnas de null** |
| selectividad 1,04× como propiedad del circuito | **1,04× como propiedad del recorte**, con la advertencia de no extrapolar |
| — | **DNp70 → GF con 587 sinapsis**, la mayor entrada individual no visual, sin caracterizar |
| — | §6 entera: la retractación del AMMC con la tabla que la refuta |

**Lo que NO cambió, porque sigue midiendo bien:** los cuatro veredictos del null anatómico (LC6 y LC9 excluidos, LPLC1→GF geometría), la medida de oportunidad de 5.335 contra 4.523, y la ganancia de 40× del recorte compilado.

---

## 6. La ficha final, en una línea

> **El Giant Fiber no es un detector visual de aproximación ni un fan-in exclusivo: es un cuello de botella de 2 salidas dominado por control central (67,6%) e inhibición (49,8%), con la vía visual rápida como un quinto de su presupuesto y un ruteo de entrada verificablemente selectivo.**

---

## 7. Scorecard (QA)

| Criterio | Pts | Evidencia |
|---|---|---|
| **Completitud** | 14/15 | 9 secciones, evidencia cruda verbatim en la §7 de la entrada, prior art completo con citas. **−1**: los 567 socios centrales son 2/3 del circuito y siguen sin caracterizar |
| **Arquitectura del razonamiento** | 9/10 | la corrección distingue **localización** de **origen**, y separa lo que es propiedad del recorte de lo que es propiedad del circuito. **−1**: la fracción inhibitoria se reporta por sinapsis y por arista sin decidir cuál es la métrica correcta |
| **Documentación** | 10/10 | la entrada dice qué hace, qué no hace, qué es de otros y qué no se midió, con 9 ítems de NO MEDIDO |
| **Innovación** | 4/5 | sale una predicción falsable nueva (compilar las 962 con signo). **−1**: no se corrió |
| **Proceso QA** | 5/5 | cada número tiene su línea en la salida cruda commiteada, recomputable, y el error propio queda con su causa nombrada |

**Total 42/45 sobre los aplicables → 93,3/100.** APROBADO (umbral 90).
**N/A: 55 pts** — Ejecutabilidad (15, no hay código entregable nuevo), Seguridad (15), Testing (15), DevOps (10). Tipo de entrega: **hoja de datos / peritaje**.

---

## 8. NO MEDIDO, declarado

1. **Las 962 aristas con signo no se compilaron.** Es el experimento que esta corrección habilita.
2. **Los 567 socios centrales no se caracterizaron.** Dos tercios del circuito, caja negra.
3. **DNp70 → GF (587 sinapsis) sin caracterizar.** Mayor entrada individual no visual.
4. **La fracción inhibitoria se midió con `Excitatory` del parquet**, que es signo por neurona presináptica (ley de Dale). No se verificó contra las predicciones de neurotransmisor del Explorer.
5. **Sin umbral de ≥5 sinapsis** en ninguna cifra de la entrada.
6. **Los pares →DNp09 siguen con `cell_type` (2 neuronas), no `hemibrain_type` (4).**
7. **El `0 inhibitorias de 13.026` de la v1 no se re-verificó sobre su propio subgrafo**: se declaró fuera de alcance, no falso.
8. **La entrada no está en el paper ni en el README**, y los contextos siguen sin actualizar con las resp 065-068.
9. **El motivo sigue contando como 1 en el plan de 10 semanas.** Esta corrección lo mejora, no lo multiplica.
