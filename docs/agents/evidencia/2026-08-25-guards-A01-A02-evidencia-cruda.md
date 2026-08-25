# EVIDENCIA CRUDA · A-01 y A-02 · `guards.py` reparado y verificado en clon fresco

**Fecha:** 2026-08-25 09:50 (America/Buenos_Aires)
**Instrumento:** `gateway build.run` sobre el container `brain-env`, 4 corridas.
**Sujeto:** `src/guards.py` md5 `954815935545435ced0d1a26865c0859` · `src/test_guards_negativo.py`

---

## 0. El método, y por qué no se corrió donde se escribió

Los dos archivos se escribieron en un container y se **bajaron del raw de GitHub a un directorio vacío de `brain-env`** para correr ahí. Dos razones:

1. **A-05 dice que el clon fresco no corre.** Si estos archivos se testean en el mismo lugar donde se escribieron, el test hereda el entorno y no prueba nada sobre un tercero.
2. **El `$?` de este shell miente**, y eso está medido en el proyecto. Así que el returncode se lee con `subprocess.run().returncode`.

---

## 1. Bajada al directorio vacío, con md5 de los dos lados

```
$ mkdir -p /workspace/a01 && cd /workspace/a01
$ curl -sS -o guards.py 'https://raw.githubusercontent.com/gatehot59-star/drosophila-fep-connectome/titan/twohop-nulls/src/guards.py'
$ curl -sS -o test_guards_negativo.py '.../src/test_guards_negativo.py'
$ ls -la
total 40
drwxr-xr-x  2 root root  4096 Aug 25 13:02 .
drwxr-xr-x 17 root root 12288 Aug 25 13:02 ..
-rw-r--r--  1 root root 13755 Aug 25 13:02 guards.py
-rw-r--r--  1 root root  6543 Aug 25 13:02 test_guards_negativo.py
$ md5sum guards.py test_guards_negativo.py
954815935545435ced0d1a26865c0859  guards.py
cc103bc1c55bcd6ee1bda04b75aa426b  test_guards_negativo.py
exit=0
```

**`954815935545435ced0d1a26865c0859` es el mismo md5 que el archivo local desde donde se escribió.** Los dos lados coinciden.

**Y queda medido de paso:** el repo es **público** (el `curl` sin token funcionó), y estos dos archivos **corren en un directorio vacío sin rutas absolutas**. **A-05 cerrado para ellos, abierto para el resto.**

---

## 2. 🟢 LA CORRIDA · 28 de 28, salida verbatim sin recortar

```
=== CORRIDA DESDE CLON FRESCO, entorno real brain-env ===
Python 3.12.14
=== BATERIA guards.py  A-01 + A-02 ===
python 3.12.14

--- A-02 : los tres estados de sd(null) ---
PASS 1 sd>0 verdict  got='BIEN' want='BIEN'
PASS 1 sd>0 tiene clave ratio  got=True want=True
PASS 2 conservado verdict  got='NO_MEDIDO' want='NO_MEDIDO'
PASS 2 conservado sd_zero_reason  got='NO_MEDIDO_CONSERVADO' want='NO_MEDIDO_CONSERVADO'
PASS 2 conservado NO expone ratio  got=False want=False
PASS 2 conservado NO expone ratio_censored  got=False want=False
PASS 3 TAO verdict es CENSURADO no NO_MEDIDO  got='CENSURADO' want='CENSURADO'
PASS 3 TAO sd_zero_reason  got='CENSURADO' want='CENSURADO'
PASS 3 TAO NO expone ratio  got=False want=False
PASS 3 TAO expone ratio_censored  got=True want=True
PASS 3 TAO direccion  got='real_por_debajo_del_null' want='real_por_debajo_del_null'
PASS 3 TAO lado de la cota  got='techo' want='techo'
PASS 4 piso verdict  got='CENSURADO' want='CENSURADO'
PASS 4 piso direccion  got='real_por_encima_del_null' want='real_por_encima_del_null'
PASS 4 piso lado de la cota  got='piso' want='piso'
PASS 5 vacio verdict  got='NO_MEDIDO' want='NO_MEDIDO'
PASS 5 vacio NO expone ratio  got=False want=False

--- A-02 bis : el guard puede dar rojo (controles negativos) ---
PASS 6 CTRL NEG conservado != censurado  got=False want=False
PASS 7 CTRL NEG conservado sin direccion  got=False want=False

--- reachability ---
PASS 8 cota sqrt(8)  got=2.828427 want=2.828427
PASS 9 umbral 3.0 sobre sqrt(8) explota  got=True want=True
PASS 10 umbral 2.0 sobre sqrt(8) pasa  got=2.0 want=2.0

--- A-01 : require() aborta con exit != 0, medido con subprocess ---
  subprocess returncode = 2
  subprocess stderr     = GUARD_FAILED nulls must be positive, got 0
  subprocess stdout     = ''
PASS 11 require(False) returncode  got=2 want=2
PASS 12 require(False) escribe GUARD_FAILED en stderr  got=True want=True
PASS 13 require(False) NO sigue ejecutando  got=False want=False
  subprocess OK returncode = 0
PASS 14 require(True) returncode  got=0 want=0
PASS 15 require(True) sigue ejecutando  got=True want=True
  ANTIPATRON returncode = 0  (imprime error y sale 0)
PASS 16 CTRL NEG el antipatron da 0 y require da 2  got=(0, 2) want=(0, 2)

=== RESUMEN ===
tests corridos : 28
fallados       : 0
TODOS VERDES, y los controles negativos demuestran que podian dar rojo
EXIT_shell_NO_CONFIABLE=0
--- returncode medido con subprocess ---
EXIT_REAL= 0
ULTIMA_LINEA= TODOS VERDES, y los controles negativos demuestran que podian dar rojo
STDERR= ''
exit=0
```

**El test 16 deja demostrado A-01 en la misma corrida:** un programa que **imprime error y sale 0** da `returncode 0`, y `require()` da **2**. El antipatrón y el arreglo, medidos lado a lado.

---

## 3. 🔥 LA PRUEBA DE MUTACIÓN · lo que hace valer las 28

**Sin esto, 28 verdes no distinguen un test que funciona de uno que no puede fallar.** Es el **modo de falla 6** del proyecto, que reincidió cuatro veces.

Se revirtió **una sola línea** de `guards.py` al comportamiento viejo de A-02:

```python
-        if abs(mu - r) <= float(atol):
+        if True:  # MUTACION A PROPOSITO: comportamiento viejo de A-02
```

**Salida verbatim:**

```
MUTACION_APLICADA
--- la bateria contra el guards.py MUTADO: DEBE dar rojo ---
EXIT_REAL_MUTADO= 1
LINEAS_FAIL= 10
  FAIL 3 TAO verdict es CENSURADO no NO_MEDIDO  got='NO_MEDIDO' want='CENSURADO'
  FAIL 3 TAO sd_zero_reason  got='NO_MEDIDO_CONSERVADO' want='CENSURADO'
  FAIL 3 TAO expone ratio_censored  got=False want=True
  FAIL 3 TAO direccion  got=None want='real_por_debajo_del_null'
  FAIL 3 TAO lado de la cota  got=None want='techo'
  FAIL 4 piso verdict  got='NO_MEDIDO' want='CENSURADO'
  FAIL 4 piso direccion  got=None want='real_por_encima_del_null'
  FAIL 4 piso lado de la cota  got=None want='piso'
  FAIL 6 CTRL NEG conservado != censurado  got=True want=False
  FAILED: 3 TAO verdict es CENSURADO no NO_MEDIDO, 3 TAO sd_zero_reason, 3 TAO expone ratio_censored, 3 TAO direccion, 3 TAO lado de la cota, 4 piso verdict, 4 piso direccion, 4 piso lado de la cota, 6 CTRL NEG conservado != censurado
RESUMEN= ['fallados       : 9']
954815935545435ced0d1a26865c0859  guards.py
EXIT_REAL_RESTAURADO= 0
exit=0
```

**Los 9 fallos caen exactamente donde tienen que caer:** el **test 3, que es el contraejemplo de Tao** (`guarded_ratio(15, [110]*40)`), el test 4 (la saturación del otro lado) y el **control negativo 6**. Restaurado el archivo, el md5 vuelve a `954815...` y el exit vuelve a **0**.

---

## 4. ⚠️ Un falso positivo que casi se cuela, y va documentado

**Primer intento**, con la URL en una variable de shell que no se expandió:

```
curl: (3) URL rejected: No host part in the URL
EXIT_shell=0
EXIT_REAL_por_subprocess= 2
```

**El archivo no existía** y `subprocess` devolvió **2**, que es exactamente el returncode que se estaba buscando como éxito. **Un returncode correcto por el motivo equivocado.**

Y el `$?` del shell dijo **0** sobre una corrida donde nada se ejecutó, o sea el modo de falla 6 del entorno reincidiendo **dentro del turno en que se lo estaba arreglando**.

**Por eso la corrida definitiva verifica además `md5sum`, tamaño en bytes y la última línea del stdout.** Un returncode solo no alcanza como recibo.

---

## 5. Veredicto

| Hallazgo | Estado |
|---|---|
| **A-02** · `guarded_ratio` confunde conservación con saturación | 🟢 **REPARADO** en el módulo, con test que puede dar rojo |
| **A-01** · los guards imprimen rojo y salen con 0 | 🟡 **REPARADO en `guards.py`** vía `require()` (exit 2 medido). 🔴 **ABIERTO en los llamadores** |
| **A-05** · el clon fresco no corre | 🟢 **cerrado para estos dos archivos** (corren en directorio vacío). 🔴 abierto para los dos `.mjs` y el resto |

---

## 6. NO MEDIDO, declarado

1. **Los llamadores NO fueron migrados.** `motor.py`, `scriptR.py` y los dos `.mjs` siguen con su patrón viejo. **A-01 está cerrado para el módulo, no para el repo**, y el daño que A-01 señalaba vivía en los llamadores.
2. **No se re-corrió ningún resultado científico con el `guards.py` nuevo.** Ningún número del expediente cambia por este commit, y ninguno se re-validó tampoco.
3. **`results/test_guards.log` no se regeneró.** El docstring del módulo lo cita con «16 tests» y esta batería tiene **28**: son archivos distintos y el viejo no se abrió en este turno.
4. **La mutación probó UNA línea.** No es un análisis de mutación completo: no se mutó `require()`, ni `assert_threshold_reachable`, ni la rama `sd > 0`.
5. **No hay CI.** El test existe y corre a mano; **nada lo ejecuta automáticamente**, que es A-03 y sigue abierto.
6. **`atol` por defecto es 0.0**, o sea comparación exacta de flotantes. Para las dos formas medidas en este repo (enteros exactos) alcanza, pero **para un estadístico continuo un `atol` de 0 puede clasificar como CENSURADO algo que es CONSERVADO con ruido de punto flotante.** Declarado, no resuelto.
