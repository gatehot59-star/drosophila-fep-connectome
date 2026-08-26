# 101 · Los 39 nulls cerraron en GPU hace 4 horas, y el 403 era mío

**Fecha:** 2026-08-26 · **Modo:** medición directa, sin invocación de TITAN.
**Pregunta de Abraham:** ¿dejé la evidencia del bloqueo de Kaggle y lo que Tachi tenía que intentar?

---

## 1. La respuesta corta

**Tachi no tiene que intentar nada. El bloqueo no existía.**

El `403 Permission 'kernels.get' was denied` que reporté ayer no era un permiso faltante:
era que yo monitoreaba **un kernel que no existe**. Kaggle no usa el `slug` que mando en
el push, genera el `ref` slugificando el **título**. Detalle y vía correcta en
[`docs/agents/KAGGLE-REGLA-DEL-SLUG.md`](../KAGGLE-REGLA-DEL-SLUG.md).

Y la consecuencia importante: **los 4 shards ya estaban `complete`** desde
2026-08-26 00:16 UTC (21:16 ART del 25). Estuvieron listos toda la noche y yo dije que
no los podía ver.

## 2. El resultado: los 39 nulls, en GPU, con partición exacta

| control | medición |
|---|---|
| partición 0..38 | 39 índices, 39 únicos, cero duplicados, cero faltantes |
| el dato | md5 del parquet y de annotations **idéntico en los 4 shards** |
| grafo | n=138.639, e=15.091.983, 623 filas de anotación sin match |
| control espectral | `rho_post = 0,990000` **39/39 en los 4 brazos**, y en el real |
| backend | GPU Tesla P100-PCIE-16GB, `cupy=True`, en los 4 |
| costo | brazo real 220,1 s |

### El test

| métrica | REAL | media null | nulls ≥ real | p (1 cola) | lectura |
|---|---|---|---|---|---|
| `rdi_Wc_tauC_t50` | 0,4311 | 0,4411 | **39/39** | 1,0000 | **refutado, y con el signo invertido** |
| `rdi_Wc_tauC_t100` | 0,7184 | 0,4163 | **0/39** | 0,0250 (piso) | spread 1,73× |
| `rdi_Wc_tauC_t149` | 0,6642 | 0,1340 | **0/39** | 0,0250 (piso) | spread **4,96×** |
| `ventaja_tau_t50` | +0,0020 | -0,0014 | 0/39 | 0,0250 | el real es el único positivo |
| `ventaja_tau_t100` | -0,0228 | -0,0115 | 39/39 | 1,0000 | **invertido** |
| `ventaja_tau_t149` | +0,0060 | -0,0564 | 0/39 | 0,0250 | el real es el único positivo |
| `ventaja_W_t50` / `t149` | ~0 | ~0 | 6/39 | 0,1750 | **el brazo W sigue sin ser un resultado** |
| `interaccion_*` | ~0 | ~0 | 19-37/39 | 0,50-0,95 | nada |

## 3. Lo que esto refuta de lo que yo mismo dije

1. **«El efecto está»** sin más: **falso en t=50.** Ahí el real queda **por debajo** de
   los 39 nulls (z = -4,49). El efecto **no es una propiedad del grafo, es una propiedad
   del grafo A PARTIR DE CIERTO TIEMPO.** Eso es un hallazgo distinto y más chico que
   «el conectoma real separa modalidades».
2. **«La ventaja de tau sobrevive»**: **falso en t=100**, donde se invierte. Sobrevive en
   t=50 y t=149. Una cantidad que cambia de signo con el snapshot no es un mecanismo
   todavía: es una curva que hay que medir entera.
3. **El brazo W sigue NO MEDIDO como efecto**: p = 0,175. No es negativo, es que no
   alcanza. Y era el brazo que sostenía la tesis del peritaje 092.

## 4. Lo que hay que hacer con esto (y qué NO)

- **Barrer el tiempo completo**, no 3 snapshots. El cruce entre t=50 y t=100 es el
  resultado real: hay un tiempo en el que el conectoma empieza a separar. Ese número
  es publicable; «0/39 en t149» solo, no.
- **Corrección por múltiples comparaciones**: 12 métricas, y el piso del p con 39 nulls
  es 1/40. Con Bonferroni no sobrevive nada. Hacen falve más nulls **si** se va a
  reclamar significancia corregida. Con GPU eso ahora cuesta minutos, no horas.
- **NO tocar el paper con esto todavía.** El t50 invertido cambia la afirmación.

## 5. NO MEDIDO

- El cruce **CPU contra GPU** no está hecho: la corrida del container iba en 33/39.
  Es el control de instrumento y es lo único que falta para cerrar W-01 en serio.
- No se leyó el log completo de los 4 kernels.
- No se barrió el tiempo entre 50 y 100.
- No se midió cuota restante de las dos cuentas.

```
--- METODO ---
Accion delicada: NO. API de Kaggle en solo lectura, cero kernels lanzados.
Instrumento:     gateway build.run sobre brain-env. kernels/list + status +
                 output + pull con Bearer. Sondas kprobe.mjs, kreal.mjs,
                 kdown.mjs y tools/consolida_39_nulls.py, esta ultima corrida
                 antes de commitearse.
Falsador:        el propio baseline. list?user daba 200 mientras status daba 403
                 con el mismo token: eso ya decia que el problema era el sujeto,
                 no el permiso. Tarde un dia en mirarlo.
Evidencia:       docs/agents/evidencia/2026-08-26-101-kaggle-slug-403-y-39-nulls.md
```
