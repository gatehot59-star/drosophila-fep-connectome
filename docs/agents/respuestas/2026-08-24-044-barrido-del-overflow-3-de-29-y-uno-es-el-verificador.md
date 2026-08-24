# 044 · Barrido del overflow: **3 de 29**, y uno es el verificador

**Fecha:** 2026-08-24 16:50 (America/Buenos_Aires) · **Modo:** TITAN FULL

> **📄 Doc de ClickUp:** *«[TITAN FULL] BARRIDO CERRADO: el overflow está en 3 de los 29 notebooks, y uno es el VERIFICADOR Script V-K...»*

---

## 1. Pedido

«Sí, grepeá los 28 notebooks buscando el overflow.»

---

## 2. Herramientas declaradas (C-03)

| Llamada | Escribe | Cuota ajena |
|---|---|---|
| `gateway build.run` × 4 (grep + 3 corridas de aritmética) | **solo `/tmp`** | **NO** |
| `create_document` + `create_or_update_file` | sí | no |

**Cero Kaggle, cero runtime de Tachi, `gradlew` no ejecutado, nada publicado en Zenodo. Nada bajo `/workspace` creado, movido ni borrado.**

---

## 3. Qué se midió

### 3.1 El barrido: 3 de 29, y en los tres `N` es `int32`

```
$ grep -n 'N \* (N - 1)\|N*(N-1)' CODE__*.txt      (29 archivos)
CODE__abrahammendieta__notebook2f910c646f.txt:482:density = W.nnz / (N * (N - 1))
CODE__fabiomurillohot__notebook2e0ceb4908.txt:833:    density = W_raw.nnz / (N * (N - 1))
CODE__fabiomurillohot__notebook57386e9dd2.txt:512:density = W.nnz / (N * (N - 1))
```

| Notebook | md5 | `N` |
|---|---|---|
| `2f910c646f` | `77183226dde616cc6b68d988ed76b033` | lín. 105-109, `astype(np.int32)` |
| `57386e9dd2` | `c5cfdc8d339f02ae1da96b171b4ff451` | lín. 105-109, **idéntico** |
| `2e0ceb4908` | `e6b011b7e9c3d92826eda5ad19afaa9f` | lín. 129-132, **idéntico** |

**Los tres calculan `0,007395259`.** No es un desliz de un notebook: es **el bloque de carga «from Script R» copiado tres veces**, arrastrando el bug. **Los otros 26 no calculan densidad**, así que el barrido está cerrado **para este patrón**.

### 3.2 El 36× es el MISMO bug, no un segundo error

`57386e9dd2`, líneas 649-653, verbatim:

```python
# Reciprocidad esperada bajo grafo aleatorio con misma densidad
reciprocity_expected = density
print(f"  Ratio real/esperado: {reciprocity_real/reciprocity_expected:.1f}x")
```

```
reciprocidad real     = 0,2660
ratio con overflow    =  35,97 x   <- el "36x" del Abstract
ratio con densidad OK =  338,8 x   <- el 338,8x del erratum
```

**Una línea produce los dos números publicados** (`Density = 0.0074` de §2.1 y `36x` del Abstract). Para el erratum eso vale mucho: *«corregimos la densidad, y aparte el 36×»* se lee como dos descuidos; *«un overflow de `int32` contaminó la densidad y todo lo normalizado por ella»* **se lee como un diagnóstico**. Misma evidencia, la mitad del daño.

### 3.3 🚨 Uno de los tres es el Script V-K, el verificador que el paper cita

Cabecera de `2e0ceb4908`, verbatim: *«SCRIPT V-K — VERIFICATION & AUDIT TESTS... **Test B: Reproducibility — regenerate Paper 1 table values**»*. Es el verificador de las 14 citas del doc `5637`. Su test B.3:

```python
density = W_raw.nnz / (N * (N - 1))        # <- EL MISMO OVERFLOW
ref = REFERENCE_VALUES.get('density')
match = abs(density - ref) / ref <= RTOL
sym = "PASS" if match else "MISMATCH"
```

**El verificador comparte el bug con lo que verifica, así que no puede detectarlo por construcción.** Es la regla de TESTER literal — *«un test que pasa con el código roto no mide nada»* — y peor que un tautológico común, porque **este se publica como la garantía**.

### 3.4 El dígito caído, y la alarma que estaba disponible

```python
REFERENCE_VALUES = { ... "density": 0.00074, ... }   # el paper dice 0.0074
RTOL = 0.02
```

```
computed (con overflow)  = 0,00739526
REFERENCE_VALUES density = 0,00074
densidad VERDADERA       = 0,000785197

desvio computed vs ref  = 899,4 %   -> MISMATCH
desvio VERDADERA vs ref =   6,1 %   -> tambien MISMATCH, pero por poco
```

**La tabla de referencia contiene, por un dígito perdido, un número casi correcto (6,1% de la densidad real), mientras el código calcula uno 9,42× equivocado.** El verificador **sí grita**, con 899% de desvío, **pero por el motivo equivocado**: no detectó el overflow, detectó su propia referencia mal tipeada.

**Y ese `MISMATCH` era una alarma disponible y no leída:** no es «no se midió», es **medido y no leído**. Si el código no hubiera tenido el overflow, el desvío habría sido **6,1%**, que se lee como «diferencia de versión de datos» y se ignora con razón aparente. **El overflow, por grosero, es lo que hizo la alarma imposible de confundir.**

### 3.5 El alcance queda ACOTADO, y eso es buena noticia

| Pregunta | Medido |
|---|---|
| ¿Más de 3 notebooks con `N*(N-1)`? | **No.** 3 de 29 |
| ¿Los otros 26 calculan densidad? | **No la calculan** |
| ¿Qué cuelga de `density`? | **Solo dos cosas:** `p_edge_exc = density * p_exc` → Tabla 5, y `reciprocity_expected = density` → 36× |
| ¿λ_F, R, entropía, RDI? | **No dependen de la densidad**: salen de propagación con normalización columnar |

**El overflow contamina exactamente DOS familias publicadas, y las dos ya están en el erratum.** No hacen falta ítems nuevos: hace falta **la causa** y **reagruparlos bajo ella**, más un ítem sobre el verificador.

**Y confirma con mecanismo lo que el erratum afirmaba sin sostener:** *«the temporal dissociation... the depth profiles and the physiological plausibility of τ are unaffected by E1, because none of them is normalised by graph density»*. **Ahora está medido, no supuesto.**

---

## 4. Evidencia cruda verbatim

```
$ ls -1 CODE__*.txt | wc -l
29

$ md5sum de los tres hits
77183226dde616cc6b68d988ed76b033  CODE__abrahammendieta__notebook2f910c646f.txt
c5cfdc8d339f02ae1da96b171b4ff451  CODE__fabiomurillohot__notebook57386e9dd2.txt
e6b011b7e9c3d92826eda5ad19afaa9f  CODE__fabiomurillohot__notebook2e0ceb4908.txt

$ definicion de N en los tres
57386e9dd2:105  pre_idx  = ...values.astype(np.int32)
57386e9dd2:109  N = max(pre_idx.max(), post_idx.max()) + 1
2e0ceb4908:129  pre = ...values.astype(np.int32)
2e0ceb4908:132  N = max(pre.max(), post.max()) + 1
2f910c646f:105  pre_idx = ...values.astype(np.int32)
2f910c646f:109  N = max(pre_idx.max(), post_idx.max()) + 1

$ sed -n '72,90p' CODE__fabiomurillohot__notebook2e0ceb4908.txt
REFERENCE_VALUES = {
    "contralateral_excitation": 166770,
    "contralateral_inhibition": -228373,
    "contralateral_net": -61603,
    "contralateral_cancellation": 1.37,
    "ipsilateral_excitation": 2903970,
    "ipsilateral_inhibition": -613364,
    "ipsilateral_cancellation": 0.21,
    "reciprocity_global": 0.266,
    "reciprocity_intra_motor": 0.413,
    "density": 0.00074,
    "lambda_F_visual_col099": 0.055142,
    "lambda_F_olfactory_col099": 0.095519,
    "lambda_F_mechanosensory_col099": 0.109976,
    "R_visual_col099": 1.8792,
}
RTOL = 0.02    # 2% relative tolerance

$ python3 /tmp/x36.py
reciprocidad real       = 0.2660
densidad OVERFLOWED     = 0.00739526
densidad correcta       = 0.000785197
ratio con overflow  = 35.97 x   <- el 36x del paper
ratio con densidad OK = 338.8 x   <- el 338,8x del erratum
FIN_36X

$ python3 /tmp/vk.py
computed (con overflow) = 0.00739526
REFERENCE_VALUES density = 0.00074
densidad VERDADERA       = 0.000785197
desvio computed vs ref = 899.4 %  -> RTOL 2% : MISMATCH
desvio VERDADERA vs ref = 6.1 %  -> RTOL 2% : tambien MISMATCH, pero por poco
FIN_VK
```

**Recomputable y contradecible (W-01):** **si apareciera un cuarto notebook calculando densidad, o si en alguno `N` no fuera `int32`, el §3.1 se cae.**

---

## 5. Archivos generados

1. El Doc de ClickUp con el barrido completo y los dos textos de reemplazo para el erratum.
2. `docs/agents/respuestas/2026-08-24-044-barrido-del-overflow-3-de-29-y-uno-es-el-verificador.md` (este archivo).

**Los contextos vivos siguen sin tocarse**, y ahora sí corresponde actualizarlos: el barrido cerró. Va en el commit siguiente para no mezclar la medición con el cambio de estado.

---

## 6. NO MEDIDO, declarado

1. **No corrí el Script V-K.** Que el `MISMATCH` de 899% «estaba disponible» es **deducción de la aritmética del código**, no lectura de un log. **No hay log de esa corrida en `/workspace`.**
2. **No verifiqué que estos tres sean los notebooks que produjeron el paper.** Los tres se declaran descendientes («from Script R», «construido sobre el pipeline original»). El original puede no estar, igual que el script de la Tabla 7.
3. **Barrí UN patrón.** Un overflow puede tener otra forma (`N**2`, `n_nodes*(n_nodes-1)`, otro producto de conteos grandes). Grepeé `N*(N-1)` y `density`, **no todos los productos de enteros del corpus**.
4. **No verifiqué los otros 13 `REFERENCE_VALUES`** contra el PDF. Si uno tiene un dígito caído, otros pueden tenerlo.
5. **No abrí el PDF publicado.** El «36x» y el `Density = 0.0074` vienen de `CONTEXTO-drosophila-fep.md` §2 (leído verbatim el 23-ago).
6. **La reciprocidad 0,2660 la tomé del `reciprocity_global` del verificador**, no la recomputé hoy. El conteo 4.014.518 sí está medido (doc `6057`).
7. **Los cuatro conteos de filas de la Tabla 5 (7/8/9/10) siguen sin reconciliar.** Paso 2.

---

## 7. La regla que sale

**Un verificador que comparte el bloque de carga con lo verificado no es un control: es la misma medición dos veces.** El aporte de un verificador está en lo que **no comparte** con el original. Acá los dos empiezan con el mismo «DATA LOADING — from Script R», así que cualquier defecto de ese bloque es **invisible por construcción**, y ninguna cantidad de tests posteriores lo encuentra.

**Corolario operativo:** un test de reproducibilidad tiene que **recalcular desde los datos crudos con código independiente**, o declarar explícitamente qué comparte. Si comparte la carga, verifica el análisis pero **no** la carga.

```
--- METODO TITAN ---
Accion delicada: NO. Grep de solo lectura y tres corridas de aritmetica pura.
                 Escrituras en el container: solo /tmp. gradlew NO ejecutado.
                 Nada publicado en Zenodo. Ningun contexto sobrescrito.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100
N/A declarados:  45 pts (Ejecutabilidad, Seguridad, Testing, DevOps)
Review externo:  el falsador fue el corpus contra si mismo: el verificador que
                 el paper cita como garantia contiene el mismo bug que deberia
                 atrapar, y eso solo se ve poniendo su linea 833 al lado de la
                 482 del notebook que produce la tabla. Es el mismo metodo con
                 el que Abraham me falsa: dos cosas propias en la misma
                 pantalla.
Instrumento:     gateway build.run sobre brain-env, 4 llamadas. grep sobre los
                 29 CODE__*.txt con md5 de los tres hits. Python 3.12.14 para
                 la aritmetica (x36.py, vk.py). Evidencia cruda verbatim en la
                 seccion 4, sin recortar.
                 NO MEDIDO: la seccion 6, siete items, incluido que NO corri el
                 V-K y que barri UN SOLO patron de overflow.
```
