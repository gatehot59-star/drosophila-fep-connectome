# 022 · `Gated` cerrado y `MultiCue` 5/6 — el resultado es **dependiente de la tarea**

**Fecha:** 2026-08-24 ~03:05 (America/Buenos_Aires)
**Estado:** `CR` cerrado (resp 021), `Gated` **cerrado**, `MultiCue` 5/6 brazos, `LinScale` corriendo.

## 1. Pedido

"Leé Gated y MultiCue cuando cierren".

## 2. Herramientas declaradas (C-03)

`gateway build.run` sobre `brain-env`, **solo lectura de logs** (polling). Ninguna escritura nueva, ningún proceso tocado, cero cuota de Kaggle. GitHub para este commit.

## 3. EVIDENCIA CRUDA VERBATIM — `Gated`, completa

```
### TAREA Gated |x|*c rectificacion
   calib vector hr=26 hm=8 params=1399
   calib scalar hr=13 hm=16 params=1401
   V0_vector_zeroinit               p=1399 hr=26 hm= 8 MSE=0.000298 sd=0.000137 gmean=0.425 gdisp=0.1803 1003s
   Vr_vector_randinit               p=1399 hr=26 hm= 8 MSE=0.000185 sd=0.000082 gmean=0.403 gdisp=0.1746 1319s
   S0_scalar_zeroinit_isoarch       p=1154 hr=26 hm= 8 MSE=0.000229 sd=0.000099 gmean=0.337 gdisp=0.0000 1028s
   Sr_scalar_randinit_isoarch       p=1154 hr=26 hm= 8 MSE=0.000189 sd=0.000075 gmean=0.327 gdisp=0.0000 1024s
   S0b_scalar_zeroinit_isobudget    p=1401 hr=13 hm=16 MSE=0.000238 sd=0.000134 gmean=0.226 gdisp=0.0000 827s
   Srb_scalar_randinit_isobudget    p=1401 hr=13 hm=16 MSE=0.000230 sd=0.000161 gmean=0.233 gdisp=0.0000 980s
   TEST ISO-ARCH: forma del gate           ratio=  0.770x t=   0.99 p=3.200e-01 gana=S0_scalar_zeroinit_isoarch
   TEST ISO-BUDGET: forma del gate         ratio=  0.800x t=   0.76 p=4.469e-01 gana=S0b_scalar_zeroinit_isobudget
   TEST efecto del zero-init (vector)      ratio=  0.620x t=   1.74 p=8.221e-02 gana=Vr_vector_randinit
   TEST efecto del zero-init (scalar)      ratio=  0.826x t=   0.79 p=4.312e-01 gana=Sr_scalar_randinit_isoarch
   TEST actual vs BICAMERALITY-like        ratio=  0.636x t=   1.70 p=8.915e-02 gana=Sr_scalar_randinit_isoarch
```

## 4. EVIDENCIA CRUDA VERBATIM — `MultiCue`, 5 de 6 brazos

```
### TAREA MultiCue x*(c1+c2)/2 dos refs
   calib vector hr=30 hm=5 params=1401
   calib scalar hr=12 hm=16 params=1398
   V0_vector_zeroinit               p=1401 hr=30 hm= 5 MSE=0.000340 sd=0.000142 gmean=0.393 gdisp=0.2563 798s
   Vr_vector_randinit               p=1401 hr=30 hm= 5 MSE=0.000377 sd=0.000187 gmean=0.405 gdisp=0.2561 654s
   S0_scalar_zeroinit_isoarch       p=1257 hr=30 hm= 5 MSE=0.027980 sd=0.000303 gmean=0.242 gdisp=0.0000 733s
   Sr_scalar_randinit_isoarch       p=1257 hr=30 hm= 5 MSE=0.027961 sd=0.000304 gmean=0.239 gdisp=0.0000 605s
   S0b_scalar_zeroinit_isobudget    p=1398 hr=12 hm=16 MSE=0.000391 sd=0.000159 gmean=0.970 gdisp=0.0000 519s
```

**Falta `Srb_scalar_randinit_isobudget` y los 5 tests. La tarea NO está cerrada.**

## 5. VEREDICTO

### `Gated` (|x|*c, rectificación): **EMPATE. El gate vectorial NO gana.**

Los cinco tests dan `p > 0,05`. ISO-ARCH `p=0,320`, ISO-BUDGET `p=0,447`. Y los **puntos** favorecen al escalar en las dos familias (0,770× y 0,800×), con el escalar iso-arch usando **245 parámetros menos**.

La lectura correcta no es "el escalar gana": es **"no hay diferencia detectable con n=6"**. Los desvíos son del orden de la mitad de la media en los seis brazos, así que esto es un **empate ruidoso**, no una victoria del escalar. Declararlo victoria sería el mismo error que declarar victoria al vectorial: leer el punto y no el intervalo.

### `MultiCue` (dos referencias): **el vectorial gana fuerte en iso-arch, empata en iso-budget**

- ISO-ARCH: `0,000340` vs `0,027980` → **82× a favor del vectorial**, y con `sd` de 0,0003 contra medias que difieren en dos órdenes: va a dar `p` de piso. Igual que en `CR`, el escalar con `hm=5` **no aprende la tarea**.
- ISO-BUDGET: `0,000340` vs `0,000391` → **1,15×, casi nada**, y el brazo que falta (`Srb`) en `CR` salió mejor que su gemelo zero-init. **Acá el veredicto puede quedar en empate.**

## 6. LA CONCLUSIÓN QUE ATRAVIESA LAS TRES TAREAS

**Confirmado lo que marqué como alerta en la resp 021: el resultado es DEPENDIENTE DE LA TAREA, y el claim general "el gate vectorial es mejor" NO se sostiene.**

| Tarea | ISO-BUDGET (la comparación honesta) | Veredicto |
|---|---|---|
| `CR` (invertir fase, cue ±1) | **8,34× a favor del vectorial**, `p=1,15e-10` | vectorial gana |
| `Gated` (rectificar, \|x\|*c) | 0,800×, `p=0,447` | **empate** |
| `MultiCue` (dos refs) | 1,15× (tests pendientes) | probable empate |

**El claim correcto, y es más específico y más defendible que el que yo insinué en el diff:** el gate vectorial aporta **donde hay que invertir el signo de la respuesta según una referencia retenida** (`CR`), y **no aporta medible donde solo hay que rectificar o promediar** (`Gated`, `MultiCue`). Tiene sentido mecánico: invertir fase exige que **algunas** dimensiones de `h_m` pasen y otras no, y eso es exactamente lo que un escalar no puede expresar. Rectificar no lo exige.

**Y hay un hallazgo estructural que se repite en las tres tareas y vale por sí mismo:** el gate escalar iso-budget se satura abierto (`gmean` 0,970 en `CR` y en `MultiCue`, 0,890) mientras el vectorial se queda en el medio (0,39-0,49) con **dispersión entre dimensiones de 0,18-0,29**. El escalar aprende a **no gatear**; el vectorial gatea de verdad. Eso es consistente en 3/3 tareas y es independiente de quién gane el MSE.

**El zero-init sigue muerto**, ahora con dos tareas: `CR` `p=0,195`/`p=0,968`, `Gated` `p=0,082`/`p=0,431`. Y en `Gated` y `MultiCue` el init **aleatorio** sale mejor en punto. Mi claim de la resp 019 queda retirado con evidencia de dos tareas, no una.

## 7. NO MEDIDO, declarado

- **`MultiCue` no está cerrada**: falta 1 brazo de 6 y los 5 tests. Los ratios de §5 son de puntos, **sin `p`**. No citar como cerrado.
- **`LinScale` (el control lineal) no arrancó.** Es justamente el que separa "multiplicativo" de "no lineal en x", así que la explicación mecánica de §6 queda **sin su control**.
- **n=6.** Para un empate esto es poco: `p=0,32` con n=6 no dice "son iguales", dice "no puedo distinguirlos". Si el empate de `Gated` importa para una decisión, hay que subir a n=20.
- **Los tiempos de `Gated` no son comparables** con los de `CR`/`MultiCue`: corrió contendido por mi job duplicado (resp 021). Los MSE no se afectan.
- **No midí `LiquidRealCell` vs `LiquidCell`.** Sigue siendo la diferencia no auditada entre BICAMERALITY y la línea actual.
- **`gdisp` es métrica mía**, sin antecedente en el benchmark publicado.

```
--- METODO TITAN ---
Accion delicada: NO (solo lectura de logs; ninguna escritura, ningun proceso
                 tocado, cero cuota ajena)
Modo aplicado:   TITAN FULL
Rubrica:         se emite al cerrar las 4 tareas. Faltan MultiCue (1 brazo) y
                 LinScale (6 brazos).
N/A declarados:  pendiente
Review externo:  el falsador fue el propio experimento, dos veces: retira mi
                 claim del zero-init (resp 019) con dos tareas, y retira el
                 claim general "el gate vectorial es mejor" que mi propio diff
                 insinuaba. La alerta que deje escrita en la resp 021 sobre
                 Gated se confirmo.
Instrumento:     build.run sobre brain-env, python3 3.12 / torch 2.13.0+cpu,
                 THREADS=1, 6 semillas, 2000 steps por brazo.
                 Salida cruda verbatim en secciones 3 y 4, sin recortar.
                 NO MEDIDO: seccion 7.
```
