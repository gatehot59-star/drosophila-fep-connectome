# 046 · Erratum fundido, y el PDF cerró el hueco abriendo dos nuevos

**Fecha:** 2026-08-24 19:05 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** *«[TITAN FULL] ERRATUM FUNDIDO Y COMMITEADO...»* · **Entregable: `docs/ERRATUM.md`, que existe en git por primera vez.**

---

## 1. Pedido

«Fundí el erratum sin el PDF, declarando el hueco.» **Y adjuntó el PDF.** Así que el hueco no se declara: **se cierra**.

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| Lectura del PDF adjunto (7 páginas) | no | no |
| `gateway build.run` × 2 (poblaciones + recomputo de las 9 filas) | `/tmp` | **NO** |
| `create_document` + `push_files` (2 archivos) | sí | no |

**Cero Kaggle, cero cuota, `gradlew` no ejecutado, nada publicado en Zenodo.**

---

## 3. El hueco CERRADO: los cuatro conteos reconciliados

| Fuente | Filas | Verificado en el PDF |
|---|---|---|
| Tabla 5 **publicada** | **9** | ✅ el `5157` E6 tenía razón |
| Methods §2.3, clases canónicas | **10** | ✅ *«For the density analysis, 10 canonical sensory classes with N >= 10»* |
| mi recomputo de la resp 043 | **7** | por usar `super_class=='sensory'`, que **no** es la definición del paper |
| el borrador del container | **8** | **dropeaba `vis. optic` (77.521)**, la clase más grande |

**Y el conteo de depletadas se reconcilia en tres lugares, exactamente como decía el `5157` E6:** la Tabla 5 marca **6** Depleted más 3 ≈Exp., el texto de §3.3 dice **«Seven classes depleted»**, y el Abstract dice **7/10**.

### La definición de población del paper, ahora medida

Es **`cell_class`** (no `super_class`), y `motor_n` sale **exacto**:

```
motor_n=1485 (paper: 1485)  p_exc=0.600272

clase         N_paper   N_mio   obs_exc   r_paper r_MIO_ovf    ratio_OK    veredicto
mechano.         2659    2656     23010     1.300     1.314    12.378  ENRIQUECIDO
unk. sensory      131     131      1179     1.400     1.365    12.858  ENRIQUECIDO
AN                495    2231     27857     0.600     1.894    17.839  ENRIQUECIDO
gustatory         408     408      1280     0.500     0.476     4.482  ENRIQUECIDO
hygrosen.          74      74        13     0.030     0.027     0.251    DEPLETADO
thermosen.         29      29        14     0.070     0.073     0.690    ~ESPERADO
olfactory        2279    2279        80     0.005     0.005     0.050    DEPLETADO
visual          10853   10855       137     0.002     0.002     0.018    DEPLETADO
vis. optic      77521   77530      1679     0.003     0.003     0.031    DEPLETADO
FIN_T5PAPER
```

**8 de 9 filas reproducen el ratio publicado con la densidad overflowed.** La fórmula y las poblaciones quedan **establecidas, no inferidas**. Veredictos corregidos: **4 enriquecidas, 4 depletadas, 1 ≈esperada.** El «4 y 4» del borrador era correcto.

---

## 4. 🚨 DOS defectos del propio borrador, que solo aparecen con el PDF al lado

### 4.1 Su ítem del 1.559× corrige un valor que **el paper nunca publicó**

El borrador dice: *«This value appears **nine times** in the published version, **including the abstract**»*, y además *«The ratios in **Table 1** have the same defect, with denominators of 1.0e-7 and 7.3e-8»*.

**Leí las 7 páginas: el 1.559 no aparece en ninguna.** Y la **Table 1 de este paper es la tabla de poblaciones sensoriales y motoras**, que no tiene un solo ratio. La amplificación en v1.0 está reportada como **diferencia** (RDI de 0,63 a 0,83, Tabla 8), que ya es la forma defendible.

**Ese ítem pertenece a otro documento y se retira.** Un erratum que corrige un claim que el paper no hizo **es él mismo un error**, y en un documento con DOI eso es lo primero que un revisor encuentra.

### 4.2 Su ítem de Data Availability cita **la URL equivocada**

```
PDF §7, verbatim:  github.com/Mendieta-Architect/drosophila-connectome-propagation
borrador dice:      github.com/Mendieta-Architect/drosophila-fep-connectome
```

**Son repos distintos.** El borrador corrige la URL citándola mal.

---

## 5. Dos correcciones a decisiones mías de turnos anteriores

**a) Reincorporo el E7 del `5157`, que descarté en la resp 042.** §2.5 del PDF dice verbatim *«tau_m ~= 8.4 ms, **center** of the Drosophila physiological range (5-20 ms)»* y *«3.3 ms, **lower limit** of range»*. El centro de 5-20 es **12,5**, y 3,3 está **debajo** del rango. **Eso es distinto del error de derivación** (7,89 vs 8,4) que trae el container: **son dos defectos sobre el mismo parámetro** y van los dos. Descartar el E7 fue elegir uno de dos.

**b) El E8 es más estrecho de lo que el `5157` planteó.** El «four parameter-free models» está **solo en el Abstract**: §2.5 («Note on LIF-hard») y la Limitación 3 **ya dicen tres**. O sea que el paper se autocorrige y lo único inconsistente es el abstract.

---

## 6. Confirmado verbatim contra el PDF

| Afirmación del contexto | Verificado |
|---|---|
| `Density = 0.0074` en §2.1 | ✅ |
| «36x over density expectation» en el Abstract | ✅ |
| DOI placeholder `10.5281/zenodo.XXXXXXX` literal | ✅ |
| «synapses» en el Abstract vs «connections» en §2.1, mismo 15.091.983 | ✅ **E3 del `5157` confirmado** |
| Tabla 4 suma 90.101 donde 85.821+4.281 = 90.102 | ✅ |
| §2.4 **ya declara** el guard de tautología del CP (`sigma = 0` a 1-hop) | ✅ |
| **Table 7 = reciprocidad por circuito; Table 8 = Cosine RDI con `Real\|CP\|Z_CP\|MS\|Z_MS`, SIN columna Ratio** | ✅ exacto |
| Licencia AGPL v3, más CC BY 4.0 para Zenodo | ✅ |

**Y un dato que corrige al doc `6017`:** lo que ese doc llamaba «Tabla 7» (los valores 0,687 / 0,630 / 0,680 / 0,807 / 0,833) es en realidad la **Tabla 8**. La Tabla 7 es reciprocidad por circuito. **Su hallazgo se sostiene** — esos valores no se reproducen y no están en los notebooks — pero la tabla estaba mal nombrada, y en el erratum va como **Tabla 8**.

---

## 7. Archivos generados

1. **`docs/ERRATUM.md`** — **primera vez en git.** Nueve ítems, cero placeholders, con «What has not changed», «Outstanding verification» (6 ítems) y «How these errors were found».
2. `docs/agents/respuestas/2026-08-24-046-erratum-fundido-con-el-PDF.md` (este archivo).

**No se pisó nada:** `docs/ERRATUM.md` no existía en git. El del container queda intacto y rescatado en `docs/agents/evidencia/`.

---

## 8. NO MEDIDO, declarado

1. **No establecí cuál es la décima clase** que los Methods declaran y la Tabla 5 no muestra. Va como «Outstanding verification» ítem 1.
2. **La fila AN sigue sin reproducirse.** `N=495` no sale de ningún filtro consistente con las otras ocho. Va declarada **no reproducible**, no corregida.
3. **No verifiqué si los `p` de la Tabla 5 usan `p_edge_exc`.**
4. **No verifiqué Betzel** (PLOS Complex Systems 3(3), e0000091) contra el artículo. El erratum dice explícitamente que hay que hacerlo antes de presentarlo.
5. **No re-verifiqué los DOI contra Zenodo hoy.** Vienen del `5157`. **Antes de subir se re-verifican.**
6. **El 1.559×:** afirmo que no está en el PDF sobre la base del **texto extraído de las 7 páginas**. El Material Suplementario está parcialmente incluido (Tabla S1 y las definiciones de métricas); si hay un suplementario aparte, no lo vi.
7. **No leí `repo/docs/METHODS.md`, `repo/README.md` ni `repo/LICENSE`**, y el ítem 8 toca la licencia. Siguen sin versionar.
8. **Los 6 `.py` de deuda y los 10 archivos del release siguen fuera de git.** Su manifiesto con md5 sí está commiteado.
9. **Los contextos vivos no se tocaron en este commit.** El `1.652×` sigue escrito en `CONTEXTO-drosophila-fep.md` §4 y hay que retirarlo; va en el commit siguiente para no mezclar el entregable con el cambio de estado.

---

## 9. Scorecard (R-01)

**Tipo:** documento para publicar. **Aplicables:** Completitud, Arquitectura del razonamiento, Documentación, Innovación, Proceso QA. **N/A: 45 pts.**

| Criterio | Pts | Evidencia |
|---|---|---|
| Completitud | 15/15 | Nueve ítems, la tabla de 9 filas con su validación a 8/9, «What has not changed», seis ítems de «Outstanding verification», y **cero placeholders** contra los tres corchetes del `5157` |
| Arquitectura del razonamiento | 10/10 | La validación va **antes** de la corrección: se reproduce el ratio publicado con la densidad rota (8/9) y solo entonces se corrige. Y la fila que **no** reproduce se declara no reproducible en vez de sustituirle una población |
| Documentación | 10/10 | Cada cifra con su instrumento; el mecanismo del overflow escrito para que otro grupo lo busque en su código; las citas del PDF verbatim |
| Innovación | 5/5 | No pedido: que el ítem del 1.559× **corrija un valor inexistente** · que la URL esté mal citada · que el borrador dropeara la clase más grande · el ítem 9 sobre el verificador · y `thermosensory` reclasificado a ≈esperado |
| Proceso QA | 5/5 | Se retira un ítem del propio borrador y se **deja constancia** en vez de borrarlo. Se corrigen dos decisiones mías de turnos anteriores (E7 descartado, y la Tabla 7 vs 8). Nueve NO MEDIDO |

**45/45 aplicables → 100/100.** N/A declarados: 45 pts.

```
--- METODO TITAN ---
Accion delicada: SI. Se crea docs/ERRATUM.md en main, texto destinado a una
                 publicacion con DOI. Mitigacion: el archivo NO existia en git
                 (nada pisado), cada cifra viene de una medicion commiteada con
                 evidencia cruda, los seis huecos van declarados DENTRO del
                 documento en una seccion propia, y SUBIR A ZENODO sigue siendo
                 decision de Abraham. Cero cuota, gradlew no ejecutado.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100
N/A declarados:  45 pts (Ejecutabilidad, Seguridad, Testing, DevOps)
Review externo:  el falsador fue EL PDF, o sea el documento publicado, y es el
                 unico testigo que no podia contradecirme hasta hoy. Encontro
                 dos defectos del borrador que ninguna medicion propia iba a
                 encontrar, porque para verlos hacia falta el original al lado.
                 K-02: sin review automatico sobre este texto, va como DEUDA.
Instrumento:     lectura del PDF adjunto (7 paginas) + gateway build.run x 2
                 sobre brain-env. Python 3.12.14, pandas/numpy/scipy.
                 Entradas: connectivity.parquet md5 3d802fd542b5d18570ba1ba0bb0abed9
                           annotations.tsv md5 719904abad876c68ace1b5690c9b9b63
                 Recomputo de las 9 filas con las poblaciones del paper:
                 motor_n = 1485 EXACTO, y 8 de 9 ratios reproducidos con la
                 densidad overflowed. Evidencia cruda verbatim en la seccion 3.
                 NO MEDIDO: la seccion 8, nueve items.
```
