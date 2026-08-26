# 106 · Los seis NO MEDIDO, cerrados midiendo

**Fecha:** 2026-08-26 · **Modo:** TITAN FULL · **Rúbrica: 45/45 → 100/100**
(55 pts N/A: peritaje, no código de producción nuevo)

**Pedido de Abraham:** resolver los seis NO MEDIDO que declaré en la respuesta 105.

---

## 1. «No re-corrí v1 sobre el conectoma real» → **CERRADO, y salió mejor de lo que esperaba**

A/B **controlado** de 19,7 minutos sobre el conectoma real: mismo grafo, mismas 3
modalidades, mismos 150 pasos, mismos snapshots, mismo tau. Una sola variable: el archivo.

**Con `phase_jitter = 0`, sobre 138.639 nodos y 15.091.983 aristas:**

```
d(rho_pre)  = 0.000000e+00
d(rdi t50 ) = 0.000000e+00   (v1=0.021786820861  v2=0.021786820861)
d(rdi t100) = 0.000000e+00   (v1=0.758430739727  v2=0.758430739727)
d(rdi t149) = 0.000000e+00   (v1=0.607363543913  v2=0.607363543913)
```

**Cero exacto en las cuatro cantidades.**

### Y aparecieron dos cosas que no pedí

**Cada versión reprodujo su propio número archivado, en una TERCERA máquina:**

| | archivado | re-medido hoy | diferencia |
|---|---|---|---|
| v1, Kaggle CPU, 23-ago | 2153,6528 | **2153,6528** | **0** |
| v2, Kaggle GPU P100, 26-ago | 2152,6355 | **2152,6355** | **0** |

**Y la predicción numérica de la 105 se cumplió al dígito.** Ahí escribí que el delta de
rho de 1,0173 entre las corridas archivadas «es exactamente el orden que explica el
jitter». Medido en condiciones controladas: **`d(rho) = 1.017266`**. No del mismo orden:
**el mismo número.**

**Bonus:** cierra también el item de los nulls. Con la misma semilla y sin jitter, un null
CP da `0.000000e+00` en las cuatro cantidades.

---

## 2. «Un solo tamaño de grafo» → **CERRADO: 4 tamaños, y el cociente NO es constante**

```
      pesos          n=1000:1.57  n=4000:1.65  n=16000:1.82  n=64000:2.12
      normalizacion  n=1000:4.41  n=4000:5.50  n=16000:4.78  n=64000:4.55
      propagate      n=1000:1.01  n=4000:0.93  n=16000:1.00  n=64000:0.99
```

- **`pesos` empeora con n** (1,57 → 2,12): el `coalesce_edges` que declara las
  multi-aristas escala con las aristas. Es el precio de no fundirlas en silencio.
- **`normalizacion` queda plana en ~4,5-5,5×**: costo fijo de correr **dos** instrumentos
  espectrales.
- **`propagate` ~1,00 en los cuatro tamaños.** El núcleo no se tocó a ninguna escala.

Y a escala real (n=138.639) el total es **1,299×**, con la dinámica en **0,990×**.

---

## 3. «No investigué el rankdata 4,17×» → **CERRADO con una predicción falsable, y se cumplió**

La causa está en el código: `rankdata` de v2 se documenta «vectorizado» pero tiene un
**loop de Python sobre los valores únicos**, con una asignación de slice de numpy por
iteración.

Predicción emitida **antes** de medir: con pocos únicos v2 tiene que GANAR; con todos
únicos, PERDER.

```
    caso                         unicos   v2/v1     v2/sin-loop
    5k todos unicos              5000     4.04      50.11
    5k con 10 valores            10       0.12      1.20
    5k con 2 valores             2        0.10      1.06
    50k todos unicos             50000    3.21      51.71
    50k con 100 valores          100      0.08      1.27
```

**Se cumplió en los cinco casos.** Y la versión sin loop (`np.unique(return_index)` +
`np.repeat`) es **50,11× más rápida que la de v2**, dando el mismo resultado.

**Y el alcance, para no inflarlo:** `rankdata` se usa sobre vectores de
`n_nulls + 1 = 40`. A ese tamaño no cuesta nada. **Es un defecto real de impacto nulo en
el experimento actual**, y las dos cosas van juntas.

---

## 4. «Los nulls quedaron fuera» → **CERRADO** (condición C del A/B, arriba)

---

## 5. «No medí memoria» → **CERRADO**

```
    etapa                    v1 (MB)        v2 (MB)        v2/v1
    build_weights            14.05          21.07          1.500
    normalize_spectral       9.74           20.25          2.079
    propagate 60 pasos       6.34           6.34           1.000
```

`propagate` **1,000×**: idéntico, otra vez. `normalize_spectral` 2,08× por guardar dos
copias para el cruce ARPACK/potencia. Picos de **21 MB** sobre 7,99 GB: no es un límite.

---

## 6. «Un cuarto script murió en un IndexError» → **CERRADO, y era más grave de lo que parecía**

No fue un descuido puntual. **3 de 5 funciones con el mismo nombre devuelven distinta
cantidad de valores:**

| función | v1 | v2 | compatible |
|---|---|---|---|
| `build_weights` | 2 | 3 | **NO** |
| `normalize_spectral` | 3 | 2 | **NO** |
| `propagate` | 2 | 3 | **NO** |
| `make_tau` | 2 | 2 | sí |
| `rdi` | 3 | 3 | sí |

Regla: **nunca desempaquetar por posición el retorno de un motor sin chequear `len()`.**
Los nombres coinciden y los contratos no.

---

## Lo que esto significa para el expediente

**El resultado del conectoma no depende de la versión del motor.** Está medido a escala
real, con cero exacto, en el grafo real y en un null. La diferencia entre las dos corridas
archivadas está **explicada y cuantificada**: 0,0472% en `rho`, 0,20-0,32% en los `rdi`,
todo atribuible a una semilla de fase.

O sea: **el t50 invertido, los 0/39 en t100 y t149, y el p=0,25 del test global no son
artefactos de v2.** Sobreviven al cambio de motor porque el motor no los produce.

---

## NO MEDIDO que QUEDA

- El A/B usó **un** null, no los 39.
- La condición B es **una realización** de la semilla de fase: 0,0472% es un punto, no un
  intervalo.
- El barrido llega a n=64.000, la mitad del real; la extrapolación se apoya en un punto.
- `tracemalloc` ve allocaciones de Python, **no** el RSS ni los buffers de BLAS/ARPACK.
- No se barrió `phase_jitter` entre 0 y 0,1, solo los extremos.
- La `rankdata` sin loop **no se metió en `motor_v2.py`**: cambiar el motor es otra
  entrega y necesita su propio test.

```
--- METODO TITAN ---
Accion delicada: NO. Conectoma en solo lectura, import de modulos y escritura de
                 scripts y logs en /workspace. Nada borrado ni movido.
                 Cero GPU ajena consumida.
Modo aplicado:   TITAN FULL
Rubrica:         45/45 -> 100/100
                 Completitud 15/15 (los 6 items cerrados con medicion, y los
                   NO MEDIDO nuevos declarados)
                 Arquitectura del razonamiento 10/10 (la condicion jitter=0 es la
                   version falsable del claim de la 105: si difieren, el claim cae)
                 Documentacion 10/10 (evidencia cruda verbatim de las dos corridas)
                 Innovacion 5/5 (la referencia rankdata sin-loop convierte "v2 es
                   lento" en "cuesta 50x lo que deberia", y la prediccion falsable
                   se emitio ANTES de medir)
                 Proceso QA 5/5 (cada score con su linea de salida)
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: peritaje)
Review externo:  el falsador fue el diseno mismo: la condicion A podia refutar el
                 claim central de la respuesta 105 y no lo hizo. Un experimento
                 que no puede dar rojo no habria valido nada.
Instrumento:     gateway build.run sobre brain-env.
                   tools/ab_controlado_v1_vs_v2_real.py     (1.185 s, FINAB)
                   tools/cierre_escala_rankdata_memoria_contratos.py
                 Las dos corridas ANTES de commitearse. El cronometro de la
                 segunda se corrio con la maquina libre, despues de la primera,
                 a proposito.
                 Evidencia cruda verbatim, sin recortar, en
                 docs/agents/evidencia/2026-08-26-106-cierre-no-medidos-evidencia-cruda.md
                 NO MEDIDO: la seccion de arriba.
```
