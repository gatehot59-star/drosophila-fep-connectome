# 105 · En qué mejoró v2, medido, y qué cambia de todos los experimentos de v1

**Fecha:** 2026-08-26 · **Modo:** TITAN FULL · **Rúbrica: 43/45 → 95,6/100** (55 pts N/A:
es peritaje, no código de producción nuevo)

**Pregunta de Abraham:** v2 es una versión mejorada de `motor.py`, ¿en qué mejoró?
Contrastá. Y en retrospectiva, ¿todos los experimentos con `motor.py` van a tener
diferencias con v2, aparte de los nulls? Auditá y reevalúa el performance de los dos.

---

## La respuesta en una línea

**v2 no cambió la física. Cambió qué se controla, qué se reporta y qué puede fallar.**

Y eso se mide, no se opina: importé los dos archivos como módulos y los llamé sobre
exactamente el mismo grafo.

| lo que se comparó | diferencia medida |
|---|---|
| `propagate` (la dinámica) | **0,000000e+00** · bit por bit |
| `make_tau` | **0,000000e+00** |
| matriz que devuelve `normalize_spectral` | **0,000000e+00** |
| `region_profile`, `cosine_distance`, `rdi`, `phase_coherence`, `rankdata` | **0,000000e+00** |
| NaN sobre vectores muertos | **igual en las dos** (ya estaba en v1) |
| `build_weights` con `phase_jitter=0` | **8,88e-16** (epsilon del doble) |
| `build_weights` con el jitter por defecto | **difiere**, y es lo único |

**La única diferencia numérica es la realización del ruido de fase.** Signo idéntico,
reparto E/I idéntico (18.134 aristas inhibitorias en las dos), mismas 3.623 multi-aristas
fundidas. Las 3.548 magnitudes que difieren **son** esas multi-aristas: al sumar dos
complejos con fases distintas el módulo depende de la fase.

---

## En qué mejoró, entonces

**19 funciones nuevas, 27 → 45.** Las que cambian el expediente:

1. **El brazo de `W`.** v2 tiene `WEIGHT_COMPLEX` y `WEIGHT_REAL`; **v1 no tiene modos de
   peso**. Es el control que el peritaje 092 señaló como faltante, y el que después
   **refutó la tesis compleja** (p = 0,175).
2. **El guard de potencia.** `validate_statistical_power(9)` → `(0.2, 39, False)` y aborta
   en modo strict. **v1 no puede calcular el piso de su propio p.** Con 9 nulls el mejor p
   posible era 0,20, y v1 corrió sin saberlo.
3. **La verificación espectral cruzada.** v2 mide el radio con iteración de potencia **y**
   con ARPACK, y emite veredicto. v1 devuelve el `rho` de la matriz **original** y un flag
   sobre la iteración, no sobre el resultado: por eso yo leí «14,62» como «quedó en 14,62».
4. **La declaración del dato.** `coalesce_edges` devuelve `edges_in / edges_out /
   merged_multi_edges`. v1 fundía las mismas aristas **en silencio**.
5. **Los tests que pueden dar rojo.** 5 tests nuevos, incluido
   `test_arms_are_different_functions`, que es el que impide un A/B entre dos brazos que
   son la misma función.
6. **Corre fuera de Kaggle**: `synthetic_graph`, `build_config`, `main(argv)`, CLI.

---

## Performance: v2 es MÁS LENTO, y no importa

```
    tarea                v1 min(s)    v2 min(s)    v2/v1
    build_weights        0.0157       0.0251       1.600
    normalize_spectral   0.0422       0.1830       4.339
    propagate 60 pasos   0.0514       0.0509       0.991
    rankdata 5k          0.0100       0.0416       4.174
```

**v2 pierde en 3 de 4.** Pero la que empata es `propagate`, y `propagate` es **el 96,2%
del tiempo** de una corrida real. O sea: v2 paga 4,3× en funciones que corren **una vez
por grafo**, y 0,99× en la que corre 150 veces por estímulo. **El costo de los guards es
ruido en el total.**

Rendimiento normalizado por trabajo (arm-steps = pasos × brazos), **con el confundido de
máquina declarado**:

| corrida | s/null | arm-steps/null | s por arm-step |
|---|---|---|---|
| v1, Kaggle CPU | 155 | 400 | **0,39** |
| v2, container 2 núcleos | ~500 | 600 | **0,83** |
| v2, Kaggle GPU P100 | ~62 | 600 | **0,10** |

v2 hace **1,5× más trabajo por null** que v1 (4 brazos contra 2). Las tres filas son
máquinas distintas: **no** es un A/B limpio.

---

## Retrospectiva: qué cambia de los experimentos de v1

El único experimento de v1 sobre el conectoma real está versionado en
`results/motor_ltc_complejo.log`. Mismo `md5` de parquet, mismo N y E.

| | v1 (23-ago) | v2 (26-ago) |
|---|---|---|
| brazos | **2** (tauC, tauR) | **4** (2×2) |
| modalidades / pares RDI | **3 / 3** | **4 / 6** |
| nulls · piso del p | 9 · **0,20** | 39 · **0,05** |
| pasos / snapshots | 200 / 60,120,199 | 150 / 50,100,149 |
| `rho` del REAL | **2153,6528** | **2152,6355** |
| rdi t temprano | 0,02034 · **9/9 arriba** | 0,4311 · **39/39 arriba** |
| rdi t medio | 0,80747 · **0/9** | 0,7184 · **0/39** |
| rdi t final | 0,35985 · **0/9** | 0,6642 · **0/39** |
| test global | p = **0,60**, no podía ganar | p = **0,25**, podía y no ganó |

**Δrho = 1,0173 = 0,047%**, exactamente el orden del jitter medido. **No es un error: es
el ruido de fase.**

### El hallazgo que ninguna corrida sola podía dar

**La inversión de signo a tiempo temprano REPLICA entre v1 y v2.** v1: 9/9 nulls arriba
del real. v2: 39/39. Dos versiones, dos máquinas, dos semillas de fase, dos rejillas de
tiempo, **tres modalidades contra cuatro**, y el mismo signo invertido.

**Eso no es artefacto de v2, y es lo más sólido del expediente.** Es el cruce entre t
temprano y t medio, el número que sigo diciendo que hay que medir y que sigue sin medirse.

---

## CORRECCIÓN DE UN CLAIM PROPIO, de hace diez minutos

En el chat afirmé que v1 tenía «cero de los cuatro brazos» y que **le faltaba el brazo de
control**. Es engañoso y el archivo lo desmiente:

```python
def measure_graph(..., tau_c, tau_r, label):
    """Mide un grafo con tau COMPLEJA y con tau REAL, en la misma corrida."""
    ...
    res["ventaja_compleja_t" + str(t)] = (a - b)
```

**v1 tenía DOS brazos y calculaba `ventaja_compleja`.** Lo que le faltaba era el brazo de
**`W`**, que es lo que el peritaje dijo con precisión y yo degradé al repetirlo de memoria.
v1 controla tau; **no** controla W.

---

## NO MEDIDO

- **No re-corrí v1 sobre el conectoma real.** La tabla usa el log del 23-ago, y los dos
  experimentos difieren en **cuatro variables a la vez**: no es un A/B controlado.
- El cronómetro usó **un solo tamaño** de grafo (n=4000). No se barrió escala.
- `rankdata` de v2 dio **4,17× más lento** y no investigué por qué.
- Los nulls quedaron fuera por pedido explícito.
- No medí memoria de ninguna de las dos.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura de archivos, import de modulos y escritura en
                 /workspace de scripts de auditoria. Nada borrado ni movido.
Modo aplicado:   TITAN FULL
Rubrica:         43/45 -> 95,6/100
                 Completitud 14/15 (-1: v1 no se re-corrio sobre el conectoma
                   real; la retrospectiva usa el log archivado)
                 Arquitectura del razonamiento 10/10 (la particion "misma fisica
                   / distintos controles" y la replica cruzada de la inversion)
                 Documentacion 10/10 (evidencia cruda verbatim, 3 herramientas)
                 Innovacion 4/5 (el guard de jitter=0 para aislar el ruido es el
                   aporte; el resto es comparacion pedida)
                 Proceso QA 5/5 (cada claim con su salida cruda citada)
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: peritaje)
Review externo:  el falsador fue el propio motor.py: su docstring de measure_graph
                 refuto mi frase de que "v1 no tenia brazo de control". Lo
                 verificado gana y se corrige donde se publico.
Instrumento:     gateway build.run sobre brain-env. Tres herramientas, las tres
                 corridas antes de commitearse:
                   tools/auditoria_v1_vs_v2_inventario.py
                   tools/auditoria_v1_vs_v2_pesos.py
                   tools/auditoria_v1_vs_v2_metricas_y_performance.py
                 Evidencia cruda verbatim, sin recortar, en
                 docs/agents/evidencia/2026-08-26-105-auditoria-v1-vs-v2-evidencia-cruda.md
                 NOTA: un cuarto script murio en un IndexError (s1[2] inexistente
                 porque propagate de v1 devuelve 2 valores y no 3). Se reemplazo
                 por el de metricas y performance. Se declara en vez de taparse.
                 NO MEDIDO: la seccion de arriba.
```
