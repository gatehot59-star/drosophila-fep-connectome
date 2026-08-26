# EVIDENCIA CRUDA · el `.elf`, el arnés corriendo, y la auditoría del ESP32

**Fecha:** 2026-08-25 13:25 (America/Buenos_Aires)
**Instrumentos:** `xtensa-esp-elf-gcc 16.1.0 (crosstool-NG esp-16.1.0_20260609)` en `brain-env` · `gcc 12.2.0 (Debian)` en el sandbox propio
**Sujetos auditados:** el recibo de Tachi (`RECIBO-kaggle-gcc.log`, 9.613 B, blob `a89b1d88e98ee2da39feec70f70878fcaca163de`) y mis resp 084 y 087

---

## 0. 🔥 EL HALLAZGO DEL TURNO: el linkeo con `libm` DIO ROJO

**Este apareció al LINKEAR, y no podía aparecer compilando.** Ni Tachi ni yo lo teníamos.

```
$ xtensa-esp32-elf-gcc -std=c99 -Wall -Wextra -Werror -Os -I. -nostartfiles \
      -o l.elf dualbrain.c db_main.c
  rc = 1
    ld: warning: cannot find entry symbol _start; defaulting to 00400074
    ld: /tmp/ccy4h7d3.o: in function `db_step':
    dualbrain.c:(.text+0x303): undefined reference to `tanhf'
    dualbrain.c:(.text+0x365): undefined reference to `tanhf'
    dualbrain.c:(.text+0x3d2): undefined reference to `tanhf'
    dualbrain.c:(.text+0x3fe): undefined reference to `tanhf'
```

**Y con `-lm` sí linkea. El costo, medido:**

```
  .elf con Pade (sin libm) : 41140 B de text
  .elf con -lm             : 42267 B de text
  costo de traer libm      : 1127 B de flash

  el nucleo solo: Os libm 1336   Os pade 1492  -> la Pade cuesta 156 B mas
  pero AHORRA 1127 B de libm al linkear
  NETO A FAVOR DE PADE: 971 B
```

> ### 🎯 **Esto reclasifica la Pade.** El `CONTEXTO-motor` la trata como una **optimización opcional** que da 1,64× de velocidad. Medida en el **linkeo**, es **la única variante que linkea sin traer la librería matemática entera**, y el balance neto de flash le da **971 B a favor**. **Deja de ser opcional: es la configuración correcta para MCU.**

**Por qué nadie lo había visto:** Tachi compiló en x86, donde `libm` está siempre; y yo compilé con `-c`, o sea **objetos sin linkear**, donde un símbolo indefinido no se queja. **El linkeador es un instrumento distinto del compilador, y mide otra cosa.**

---

## 1. ÍTEM 1 · **HAY `.elf`**

```
  esp32 -Os libm        rc=1  ROJO (ver §0)
  esp32 -Os FAST        rc=0  LINKEO_OK
  esp32s3 -Os FAST      rc=0  LINKEO_OK

-rwxr-xr-x 1 root root 44292 db_esp32f.elf
-rwxr-xr-x 1 root root 44292 db_esp32s3f.elf

73c830776de2382e5d3f63b3532fc33c  db_esp32f.elf
73c830776de2382e5d3f63b3532fc33c  db_esp32s3f.elf     <- md5 IDENTICO
```

**Secciones, medidas con `xtensa-esp-elf-size -A`:**

```
db_esp32f.elf  :
section         size      addr
.text           2144   4194420
.rodata        38996   4196564
.bss             800   4239656
.comment          47         0
.xtensa.info      56   4240456
.xt.lit           16         0
.xt.prop        1452         0
Total          43511
```

### Las dos aritméticas cierran EXACTO, y eso es lo que hace válido el `.elf`

```
  blob TIT4            14420
  secuencia 512x12x4   24576
  suma                 38996
  .rodata medido       38996
  COINCIDE             True
```

> **Los pesos van a `.rodata`, o sea a FLASH, no a RAM.** Eso era el punto del diseño de Tachi (*«los pesos se leen por puntero const: pueden quedarse en flash»*) y ahora está **medido**, no declarado.

```
  db_state              704   (medido por _Static_assert en el turno anterior)
  db_weights: 18 punteros x4 + 5 uint32 x4 = 92
  g_act 1 float           4
  suma                  800
  .bss medido            800
  COINCIDE              True
```

> ### 🆕 **Número nuevo: la RAM del PROGRAMA COMPLETO es 800 B, no 704.** Los 704 son **solo el estado recurrente**. Los 96 restantes son la tabla de punteros y el buffer de salida. **El contexto declara 704 y eso es correcto para lo que mide; 800 es el número que hay que dar si alguien pregunta cuánta RAM ocupa el módulo.**

**⚠️ Limitación del `.elf`, declarada:** se linkó con `-nostartfiles`, así que **no tiene `_start` y no es flasheable**. Es un binario **enteramente linkeado** que demuestra que **todas las referencias resuelven**, que es exactamente lo que el ítem pedía. El startup real lo pone el framework de ESP-IDF.

---

## 2. ÍTEMS 2 y 3 · el arnés corre y la corrección numérica se reprodujo

**El problema:** el blob de Tachi (`dualbrain_weights.bin`, 14.420 B) vive en `/kaggle/working` y **no está en ninguno de los dos repos**.

**La solución, y la elección de qué verificar es lo importante:** no se pueden reproducir los pesos entrenados de marzo. Lo que **sí** se puede, y es una prueba **más fuerte sobre el código C**, es verificar que implementa la especificación: `gen_blob.py` genera pesos deterministas y calcula un **oráculo en numpy escrito DESDE EL HEADER**, sin mirar `dualbrain.c`. **Dos implementaciones independientes de la misma spec.**

**Y el formato se leyó, no se adivinó:**

```
n_floats calculado del header : 3553
n_floats sumando los tensores : 3553
GUARD n_floats OK
weights.bin  14420 bytes
```

**3553 y 14.420 son exactamente los dos números que el recibo de Tachi declara.**

### Salida cruda del arnés, variante `libm`

```
=== ARNES DualBrain (blob sintetico + oraculo numpy) ===
  tanh          : tanhf de libm
  dims          : OBS=12 HR=32 HM=16 ACT=1 Z=48
  DB_N_FLOATS   : 3553
  DB_BLOB_BYTES : 14420
  MACs por paso : 3440
  RAM de estado : 704 bytes
  sizeof(float) : 4

=== BIND ===
  weights.bin   : 14420 bytes
  db_bind       : 0 DB_OK
  header dims   : obs=12 hr=32 hm=16 act=1 n_floats=3553

=== AUTOPRUEBA EMBEBIDA (1 paso desde t_hm_in) ===
  err_max       : 1.1921e-07
  veredicto     : DB_OK
  autoprueba embebida                        OK

=== SECUENCIA CONTRA EL ORACULO numpy ===
  pasos         : 512
  err_max act   : 5.9605e-07  (peor en t=57)
  err_max h_m   : 1.3411e-07
  act[511]      : 1.05153477   oraculo 1.05153430
  secuencia de 512 pasos vs oraculo          OK

=== CASOS NEGATIVOS (deben FALLAR) ===
  magic corrupto          esperado=-1 obtenido=-1 OK
  version 99              esperado=-2 obtenido=-2 OK
  HR declarado 33         esperado=-3 obtenido=-3 OK
  n_floats declarado +1   esperado=-4 obtenido=-4 OK
  buffer truncado        esperado=-5 obtenido=-5 OK
  puntero nulo           esperado=-6 obtenido=-6 OK
  blob desalineado +1    esperado=-8 obtenido=-8 OK

=== RESUMEN ===
  fallas: 0
  TODO VERDE
EXIT=0
```

### Variante Pade, y acá aparece el hallazgo 2

```
  tanh          : PADE [7/8], sin libm
  err_max       : 4.7684e-07   (autoprueba)
  err_max act   : 2.0862e-06   (peor en t=282)
  err_max h_m   : 1.1921e-07
  fallas: 0    TODO VERDE    EXIT=0
```

> ### 🔴 **HALLAZGO 2, y refuta un titular de Tachi.** Su recibo dice: *«La Pade sin libm da el **MISMO** error que tanhf (8.941e-08)»*. Medido con otros pesos: **2,09e-06 contra 5,96e-07, o sea 3,5× PEOR.**
>
> **Y su propia explicación es la correcta.** El punto 3 de su nota dice: *«no es que la aproximación sea perfecta: es que las activaciones de esta red viven en un rango donde su error queda por debajo del epsilon de float32»*. **Mi medición CONFIRMA su explicación y REFUTA su titular.** Con pesos uniformes en `[-0.5, 0.5]` el rango es más ancho y la Pade se degrada.
>
> **El claim correcto es «mismo error PARA ESOS PESOS», no «mismo error».** Y sigue siendo suficiente: 2e-06 está dos órdenes por debajo de cualquier tolerancia útil.

---

## 3. 🔴 HALLAZGO 3 · defecto en el `CONTEXTO-motor` **y en mi propia resp 087**

Emparejando las variantes del recibo de Tachi con las mías, **por variante y no de memoria**:

```
  variante      gcc-x86(Tachi)  xtensa(mio)   factor
  O2_libm           2786         1796  1.551x
  O2_pade           3502         2492  1.405x
  Os_pade           2496         1492  1.673x

  Os_libm: Tachi NO lo midio. El mio da 1336.
```

**Lo que el `CONTEXTO-motor` afirma:**

```
  dice: 2496 (x86) vs 1336 (xtensa) = factor 1,87x
  PERO 2496 es Os_PADE y 1336 es Os_LIBM -> compara PADE contra LIBM
  factor real libm-a-libm (O2):  1.551x
  factor real pade-a-pade (Os):  1.673x
  el 1,87x declarado:  1.868x  <- cruza variantes
```

> **El 1,87× del contexto compara dos variantes distintas.** Es el **modo de falla 5**, y está en un contexto vivo.

**Y mi propia resp 087 tiene el mismo defecto:** escribí que mi `-O2 FAST` de **2492** estaba *«a 4 bytes del 2.496 que Tachi midió»*. **Falso:** su 2496 es **Os_pade** y mi 2492 es **O2_pade**. **La coincidencia de 4 bytes era casualidad entre dos variantes distintas**, y la usé como evidencia de acuerdo. Es **E-01**: el sujeto equivocado.

**El emparejamiento correcto de mi resp 087 era:** mi `Os_pade` = **1492** contra su `Os_pade` = **2496**, factor **1,673×**.

---

## 4. 🟡 HALLAZGO 4 · el blob NO es reproducible entre entornos

| | sandbox propio | `brain-env` |
|---|---|---|
| tamaño | 14.420 B | 14.420 B |
| md5 | `804b9feb1acba3f1c710c87bfd26adea` | `d0ffa704a5a86e74f067777bdef96a67` |
| `h_m final[0]` | `0.34217095` | `0.34217089` |

**Misma semilla, mismo script, distinto numpy** (el sandbox y el container tienen versiones distintas). La diferencia está en el 7º decimal, o sea **acumulación de `float32`**, no un bug.

> **Por eso el blob NO se commitea: se commitea el GENERADOR.** Cada quien genera el suyo y el arnés verifica el C contra **su propio** oráculo. Un blob commiteado sería un artefacto que **no se puede regenerar idéntico**, y eso es peor que no tenerlo.

---

## 5. Bug propio, encontrado y arreglado antes de commitear

La v1 del arnés imprimía:

```c
printf("  act[0]        : %.8f   oraculo %.8f\n", (double)0.0f, (double)ora_act[0]);
```

**Pasaba `(double)0.0f` en vez del valor medido**, o sea imprimía `0.00000000` donde iba un número. **No afectaba ningún veredicto** (el `check` usaba `worst_act`, que sí estaba bien) **pero un arnés que miente en su salida es exactamente lo que este proyecto persigue.** Corregido a `act[511]` contra su oráculo: **1.05153477** contra **1.05153430**.

---

## 6. ÍTEM 4 · el barrido, a 18 de 30

```
  p=0.0030 seed=256  vis= 91.55  olf= 94.17  mec= 94.85  gus= 94.97  | AZAR= 94.90  no-sat
  p=0.0100 seed=  1  vis= 29.12  olf= 74.05  mec= 47.48  gus= 84.22  | AZAR= 73.65  no-sat
  p=0.0100 seed=  4  vis= 52.62  olf=105.62  mec= 92.00  gus=105.30  | AZAR=105.62  SATURADO
  p=0.0100 seed= 16  vis= 94.62  olf=105.22  mec=105.53  gus=105.88  | AZAR=105.78  SATURADO
```

**El patrón no cambió con los dos puntos nuevos:** el azar sigue ganándole a **visual** (105,78 contra 94,62) y a **mechanosensorial**. **Sin veredicto hasta los 30.**

---

## 7. NO MEDIDO, declarado

1. **El `.elf` NO es flasheable** (`-nostartfiles`, sin `_start`). Demuestra que las referencias resuelven, no que arranque en un chip.
2. **Nada corrió en un ESP32 real.** Sigue sin haber número de hardware, y un `.elf` no lo cambia.
3. **La corrección numérica se verificó contra un oráculo numpy, NO contra PyTorch.** El 8,94e-08 de Tachi con **sus** pesos entrenados **sigue siendo suyo y sin reproducir**: sus pesos no existen en ningún repo.
4. **`db_test.c` de Tachi tampoco se compiló.** Se escribió un arnés **nuevo** que hace lo mismo más el modo MCU. **Su archivo sigue sin ejecutarse por nadie que no sea él.**
5. **El costo de `libm` (1.127 B) se midió sobre ESTE `.elf`**, que incluye el arnés. En un firmware real que ya use `libm` para otra cosa, el costo marginal es **cero**. La comparación vale para un binario que **solo** tenga el motor.
6. **No se midió el tiempo por paso en xtensa.** El de Tachi (5.726 ns libm, 3.488 ns Pade) es de **host x86** y él lo etiqueta así correctamente.
7. **Los defectos de los hallazgos 3 y 4 NO se corrigieron en el `CONTEXTO-motor`.** Se declaran acá y el contexto se corrige en un commit propio, no de memoria.
