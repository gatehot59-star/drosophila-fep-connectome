# EVIDENCIA CRUDA · A-10 · el mapeo `id2i` contra el índice del parquet

**Fecha:** 2026-08-25 09:15 (America/Buenos_Aires)
**Instrumento:** `gateway build.run` sobre el container `brain-env`. **Solo lectura sobre `/workspace`.**
**Datos:** `/workspace/connectivity.parquet` (100.804.642 B, md5 declarado `3d802fd542b5d18570ba1ba0bb0abed9`) y `/workspace/annotations.tsv` (31.718.505 B, md5 declarado `719904abad876c68ace1b5690c9b9b63`).
**Sujeto auditado:** `src/scriptR.py`, blob SHA `2014cf54755273ee4cdceb652c44597013176bf3`.

---

## 0. El enunciado que se está testeando, verbatim de la resp 073 §5

> **A-10** · 🔴 `scriptR.py` puede reproducir el pipeline equivocado · *«el que más me preocupa de los que no verifiqué. Si `id2i` por orden de `root_id` no coincide con el índice del parquet, **los 30/30 valores reproducidos reproducen un bug**. Su distinción entre fidelidad y corrección es exacta»*

**Las tres líneas de `scriptR.py` que construyen el mapeo:**

```python
pre=df['Presynaptic_Index'].values.astype(np.int32)      # la MATRIZ usa el Index del parquet
post=df['Postsynaptic_Index'].values.astype(np.int32)
N=int(max(pre.max(),post.max()))+1
W_raw=sp.csr_matrix((wts,(pre,post)),shape=(N,N),dtype=np.float32)

ids=np.union1d(pd.read_parquet(...,columns=['Presynaptic_ID'])['Presynaptic_ID'].values,
               pd.read_parquet(...,columns=['Postsynaptic_ID'])['Postsynaptic_ID'].values)
ids.sort()
id2i={int(r):i for i,r in enumerate(ids)}                # las POBLACIONES usan el rank del ID
```

**El defecto sería:** la matriz se indexa por `*_Index` del parquet y las poblaciones por **rank del ID ordenado**. **Si esos dos órdenes no son el mismo, toda `idx_S`, `idx_mu`, `stim` e `idx_motor` apuntan a filas equivocadas de `W_raw`.** Eso es medible exactamente.

---

## 1. Esquema del parquet, verbatim

```
$ cd /workspace && ls -la connectivity.parquet annotations.tsv
-rw-r--r-- 1 root root  31718505 Aug 22 20:46 annotations.tsv
-rw-r--r-- 1 root root 100804642 Aug 22 20:12 connectivity.parquet

ROWS 15091983
COLS ['Presynaptic_ID', 'Postsynaptic_ID', 'Presynaptic_Index', 'Postsynaptic_Index', 'Connectivity', 'Excitatory', 'Excitatory x Connectivity', '__index_level_0__']
Presynaptic_ID: int64
Postsynaptic_ID: int64
Presynaptic_Index: int64
Postsynaptic_Index: int64
Connectivity: int64
Excitatory: int64
Excitatory x Connectivity: int64
__index_level_0__: int64
exit=0
```

---

## 2. 🟢 LA MEDICIÓN PRINCIPAL · salida cruda sin recortar

**Comando (una línea, lanzado con `nohup` porque el timeout del gateway está entre 45 y 75 s):**

```
nohup python3 -c "import numpy as np,pyarrow.parquet as pq; print('=== A-10 VERIFICACION id2i vs INDICE DEL PARQUET ==='); t=pq.read_table('/workspace/connectivity.parquet',columns=['Presynaptic_ID','Postsynaptic_ID','Presynaptic_Index','Postsynaptic_Index']); pre_id=t.column(0).to_numpy(); post_id=t.column(1).to_numpy(); pre_ix=t.column(2).to_numpy(); post_ix=t.column(3).to_numpy(); print('EDGES',len(pre_id)); ids=np.union1d(pre_id,post_id); print('IDS_UNION_len',len(ids)); print('IDS_STRICTLY_SORTED',bool(np.all(np.diff(ids)>0))); N=int(max(pre_ix.max(),post_ix.max()))+1; print('N_from_INDEX',N); print('MIN_INDEX',int(min(pre_ix.min(),post_ix.min()))); print('LEN_ids_EQ_N',len(ids)==N); r_pre=np.searchsorted(ids,pre_id); r_post=np.searchsorted(ids,post_id); mmp=int(np.count_nonzero(r_pre!=pre_ix)); mmq=int(np.count_nonzero(r_post!=post_ix)); print('MISMATCH_PRE_edges',mmp,'de',len(pre_id)); print('MISMATCH_POST_edges',mmq,'de',len(post_id)); ... ; print('DONE')" > a10.log 2>&1 &
```

**Salida (`cat a10.log`), verbatim:**

```
exit=0
lanzado
=== A-10 VERIFICACION id2i vs INDICE DEL PARQUET ===
EDGES 15091983
IDS_UNION_len 138639
IDS_STRICTLY_SORTED True
N_from_INDEX 138639
MIN_INDEX 0
LEN_ids_EQ_N True
MISMATCH_PRE_edges 0 de 15091983
MISMATCH_POST_edges 0 de 15091983
FRAC_PRE 0.0 FRAC_POST 0.0
NEURONAS_pre_unicas 138005 post_unicas 137090
GUARD_INDEX_ID_1a1_violaciones 0
SLOTS_SIN_ID 0
NEURONAS_CON_INDEX_DISTINTO_DE_SU_RANK 0 de 138639
EJEMPLOS_index_id_rank
CONTROL_NEGATIVO_ids_con_2_swapeados_debe_dar_mismatch>0 277
DONE
```

### Qué mide cada línea, y por qué está ahí

| Línea | Qué prueba |
|---|---|
| `IDS_STRICTLY_SORTED True` | `np.union1d` devuelve estrictamente creciente y sin duplicados → `enumerate(ids)` **es** el rank, y `searchsorted` lo reproduce exacto |
| `LEN_ids_EQ_N True` (138.639 = 138.639) | el dominio del mapeo tiene el tamaño de la matriz. Si esto fallaba, había desbordes o huecos |
| `MISMATCH_PRE_edges 0` / `MISMATCH_POST_edges 0` | **el núcleo de A-10.** Sobre las 15.091.983 aristas y en las **dos** columnas, `rank(ID) == Index` siempre |
| `NEURONAS_CON_INDEX_DISTINTO_DE_SU_RANK 0 de 138639` | el test por **neurona**, no por arista: ninguna de las 138.639 |
| `GUARD_INDEX_ID_1a1_violaciones 0` + `SLOTS_SIN_ID 0` | la relación ID ↔ Index del parquet es **biyectiva y sin slots vacíos**. Sin esto, «coincide» no querría decir nada |
| `EJEMPLOS_index_id_rank` **vacío** | se pidieron los primeros 8 contraejemplos y **no hay ninguno** |
| `CONTROL_NEGATIVO ... 277` | **el test puede dar rojo.** Con solo **dos** IDs intercambiados en el array de referencia, el comparador detecta 277 mismatches en las primeras 200.000 aristas |

**Corroboración cruzada no pedida:** `NEURONAS_pre_unicas 138005` coincide **exacto** con el denominador de la ley de Dale ya publicado en el contexto (*«0 mixtas de 138.005»*). Dos mediciones independientes, mismo número.

---

## 3. 🔴 EL SEGUNDO ESLABÓN, que A-10 no nombra, y acá sí hay un defecto

`byidx()` mapea `ann['root_id']` → `id2i` **y descarta lo que no encuentra, en silencio:**

```python
def byidx(mask):
    rr=ann.loc[mask,'root_id'].values
    return np.array([id2i[int(x)] for x in rr if int(x) in id2i], dtype=np.int64)
```

**El `if int(x) in id2i` no cuenta ni reporta lo que tira.** Medido:

```
exit=0
IDS_EN_GRAFO 138639
ANNOT_ROWS 139248
ANNOT_ROOT_ID_EN_GRAFO 138625 FUERA_descartados_en_silencio 623
ROOT_ID_DUPLICADOS_en_annot 0
IDS_DEL_GRAFO_SIN_FILA_EN_ANNOT 14
  POB flow_afferent_S filas 19262 mapeadas 18664 PERDIDAS 598
  POB flow_efferent_A filas 1489 mapeadas 1481 PERDIDAS 8
  POB flow_intrinsic_mu filas 118497 mapeadas 118480 PERDIDAS 17
  POB super_class_motor filas 110 mapeadas 110 PERDIDAS 0
  POB cell_class_brain_motor_neuron filas 105 mapeadas 105 PERDIDAS 0
  POB cell_class_visual filas 11391 mapeadas 10855 PERDIDAS 536
  POB cell_class_olfactory filas 2282 mapeadas 2279 PERDIDAS 3
  POB cell_class_mechanosensory filas 2668 mapeadas 2656 PERDIDAS 12
  POB cell_class_gustatory filas 408 mapeadas 408 PERDIDAS 0
CONTROL_NEGATIVO_isin_contra_ids_desplazados_debe_caer_fuerte 559
DONE
```

**Control negativo:** contra `ids+1` (IDs que no existen) el `isin` cae de **138.625 a 559** → el instrumento discrimina, no dice sí a todo.

### Lectura, con los tres estados separados

- 🔴 **MAL:** la pérdida es **real y silenciosa**. **623 filas**, y **no está uniformemente repartida**: se concentra en `afferent` (**598**, o sea el **3,1%** de la población sensorial) y dentro de eso en `visual` (**536**). Es el **modo de falla 6** del proyecto — un camino que no puede dar rojo — aplicado a una pérdida de población en vez de a un guard.
- 🟢 **ATENUANTE, y está medido:** los conteos **post-filtro** son **exactamente** los `N_mio` de la Tabla 5 recomputada que ya está en el contexto: visual **10.855**, mechanosensory **2.656**, olfactory **2.279**, gustatory **408**, `brain_motor_neuron` **105**, `super_class == motor` **110**. **O sea que el filtro ya estaba incorporado en todos los números vigentes: no invalida ninguno.** Lo que faltaba era **declararlo**.
- ⚪ **NO MEDIDO:** si esas 623 filas son segmentos descartados del release v783 o neuronas reales sin aristas. `annotations.tsv` tiene **139.248** filas contra **138.639** IDs en el grafo, y **14 IDs del grafo no tienen fila en annotations**.

---

## 4. Veredicto

| Claim | Veredicto | Evidencia |
|---|---|---|
| **A-10 · `id2i` no coincide con el índice del parquet** | 🟢 **NO SOSTENIDO** | 0 mismatches en 15.091.983 aristas × 2 columnas; 0 de 138.639 neuronas; control negativo en 277 |
| **A-10 · «los 30/30 valores reproducen un bug»** | 🟢 **NO SOSTENIDO por esta vía.** La fidelidad **y** la corrección del indexado se sostienen | misma corrida |
| 🆕 **`byidx()` descarta población en silencio** | 🔴 **DEFECTO CONFIRMADO**, no bloqueante para los números vigentes | 623 filas, 598 aferentes, 536 visuales |

**Lo que A-10 sí acierta y sigue en pie:** su distinción entre **fidelidad** (reproducir el pipeline) y **corrección** (que el pipeline esté bien) es válida como criterio. Lo que no se sostiene es la instancia concreta que señalaba.

---

## 5. NO MEDIDO en esta corrida, declarado

1. **No se recomputó el md5 de los dos archivos de datos en esta corrida.** Se citan los declarados en el contexto: **coincidencia de tamaño en bytes, no de hash**.
2. **No se re-corrió `scriptR.py` entero** (son minutos). Se verificó **el mapeo**, que es el sujeto exacto de A-10, no los 30 valores uno por uno.
3. **Los pesos y el signo no se tocaron.** Esta corrida no dice nada sobre `Excitatory x Connectivity`, ni sobre la normalización, ni sobre `τ`.
4. **Las 623 filas descartadas no se caracterizaron** (¿segmentos del release, o neuronas sin aristas?).
5. **A-11 y A-13 siguen sin verificar.**
6. **El informe de Tao (`2026-08-25-072-auditoria-integra-titan.md`) no se abrió verbatim en este turno.** El enunciado de A-10 se tomó de la **resp 073 §5**, que es la paráfrasis de BRAIN. **Si Tao le dio a A-10 un alcance más amplio que el mapeo `id2i`, este veredicto cubre solo la parte citada.**
