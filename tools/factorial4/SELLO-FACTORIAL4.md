# Sello del factorial 4 de la mosca: el banco con el cerebro entero, en Kaggle (respuesta 2026-10-13-015)

**Qué es.** El banco de los factoriales 2 y 3 (escape o aterrizaje según vuelo, cuatro tipos visuales sintonizados,
red de tasa con inhibición, lector de umbrales) con el **cerebro entero de FlyWire v783**: 138.639 neuronas,
15.091.983 aristas (6.032.681 inhibitorias) y las mismas 564 entradas sintonizadas de R2. Lo único nuevo es el motor:
la misma cuenta de `factorial2_mosca.sim` en torch float64 para la GPU. Tarea, datos, ruido y tau por `root_id`, lector
y regla son los de `factorial2_mosca.py` (9442fdf), importado sin cambios.

**Respuesta con la evidencia cruda:** `docs/agents/respuestas/2026-10-13-015-cerebro-entero-sellado-en-kaggle-la-t4-reproduce-r2.md` (en `main`).

## Instrumento (lo que traen los kernels: SHA `ace8fe78093a9109c20235746d867f2b168290d2`)

| archivo | md5 |
|---|---|
| `tools/factorial4/cerebro_mosca.py` | `36a9f005cfc87470c74af8f303af56c3` |
| `tools/factorial2/factorial2_mosca.py` | `798a824cd47808155fa12adb9e652dac` |
| `tools/factorial3/nulos_r2.py` | `c4f1c4d39c99f07cb9ad7977b6f3b01a` |
| `tools/escape_aterrizaje/tarea_mosca.py` | `40d64e074d9163753439307c5be4ac5e` |
| `tools/escape_aterrizaje/escape_aterrizaje_dbc3.py` | `4d40477d87406c31672acfb6e6e8f5a2` |
| `tools/escape_aterrizaje/entrada_por_tipos.py` | `e060c4bffb685aa550dadc19eda3dd02` |
| insumo `Connectivity_783.parquet` (philshiu) | `3d802fd542b5d18570ba1ba0bb0abed9` |
| insumo anotaciones FlyWire en `17fc577` | `719904abad876c68ace1b5690c9b9b63` |

## Sello (este commit)

| archivo | md5 |
|---|---|
| `tools/factorial4/agregar_factorial4.py` | `96396793da55400d5a1328e3877c9e2a` |
| `tools/factorial4/prueba_agregar_factorial4.py` | `fab388347f5f6a01a51a757c7d192464` |
| `tools/factorial4/kaggle/cuerpo_kernel.py` (con carriles) | `0ea46695338cda30140c4a497850dd1d` |
| `tools/factorial4/kaggle/cuerpo_kernel_humo1.py` (el del primer humo, sin carriles) | `d9880d8a21dc2b8a4fbcd4849c02cef1` |
| `tools/factorial4/kaggle/armar_plan.py` | `9c79ad85106751fc33e52b2e7eec9a89` |
| `tools/factorial4/kaggle/generar_kernels.py` | `5b23d2edeeac64e170c2049d3909d13f` |
| `tools/factorial4/kaggle/plan_humo_kaggle.json` | `3efe72d1e3f6cfd55f506dfa72966140` |

Generados (se rearman desde lo de arriba; el md5 es el sello):

| archivo | md5 |
|---|---|
| `plan_factorial4.json` (de `armar_plan.py`) | `c3ed538dedd3e82a22e5102452824962` |
| `plan_humo_carriles.json` | `d0f4135c832d7b8bb59e534cfa6a6a75` |
| kernel `f4-ce-a-2026-10-13.py` / `kernel-metadata.json` | `d76dc6522aa773489a3505c73d96f9e5` / `fcc63f904baf3de4bdf874580a2048f1` |
| kernel `f4-ce-b-2026-10-13.py` / `kernel-metadata.json` | `09ffa7743101c614cd5f511e87776917` / `700de6b29e1977f951efba26e69f2413` |
| kernel de humo de carriles (corrió) | `09b876f41da81051452980a673659d1a` |
| kernels del primer humo (corrieron, con `cuerpo_kernel_humo1.py`) | t4 `f5af4366d77fb1982d18b36eab9cbeeb`, p100 `d703187e50172b02520f98ba8950f61e` |

## Plan: dos kernels T4 x2 de `abrahammendieta`, cuatro carriles, 22 trabajos

| carril | trabajos en serie |
|---|---|
| a, GPU 0 | grilla c0h0 (+REPRO_R2), c1h0, c2h0; nulos SL k0 (+real), k10, k20 |
| a, GPU 1 | grilla c3h0 (+REPRO_R2), c4h0, c5h0; nulos T k0, k10, k20 |
| b, GPU 0 | grilla c0h1 (+REPRO_R2), c1h1, c2h1; nulos SL k30, k40 |
| b, GPU 1 | grilla c3h1 (+REPRO_R2), c4h1, c5h1; nulos T k30, k40 |

Celdas c0..c5 = 0.0|0.15, 0.0|0.45, 0.3|0.15, 0.3|0.45, 0.6|0.15, 0.6|0.45; h0 = tau 0..4, h1 = tau 5..9; pruebas 2..11.
Total: 600 corridas (las mismas del factorial 3) y 50 SL + 50 T de a 10 en la celda 0,3|0,15, tau 0, prueba 2.

**Costo, con lo medido (0,0260 s por ensayo por T4, también con dos procesos a la vez):** 1.344.000 ensayos de
grilla y 440.000 de nulos, unas 12,9 h de GPU repartidas en cuatro carriles: ≈ 3,6 h de reloj el kernel a y ≈ 3,2 h
el b, corriendo a la vez (dos sesiones simultáneas medidas el 13-oct). **≈ 7 h de sesión de la cuota semanal de GPU**
(NO MEDIDO cuánta queda). Memoria: 3,1 GB por GPU de 15 GB.

## Hipótesis pre-registradas (`agregar_factorial4.py`)

- **H_SUPERA_CE** (primaria): CE menos su regla con los mismos 564 sensores, bootstrap de dos vías (tau y prueba),
  IC90, margen 1 punto. SOSTENIDA si el IC90 queda entero arriba de +1; REFUTADA si queda abajo de +1.
- **H_ESCALA**: CE menos R2 en las mismas 600 corridas (mismos ensayos, misma regla). Misma regla de decisión.
- **H_CABLEADO_CE**: el real contra 50 SL y 50 T, p por rango y Holm; SOSTENIDA si los dos quedan bajo 0,05.
- Si el VEREDICTO_GLOBAL da INVALIDO no se lee ninguna. Nada del humo vale como número.

## Cómo se dispara (solo cuando Abraham lo pide)

1. Clon fresco de este commit; md5 de las fuentes iguales a la tabla.
2. `python3 tools/factorial4/kaggle/armar_plan.py tools/factorial4/kaggle/plan_humo_kaggle.json <dir>` y
   `python3 tools/factorial4/kaggle/generar_kernels.py <dir>/plan_factorial4.json <kernels>`: los md5 tienen que dar
   los de la tabla; si no, no se empuja nada.
3. `kaggle kernels push -p <kernels>/f4-ce-a-2026-10-13` y lo mismo con `f4-ce-b-2026-10-13` (cuenta `abrahammendieta`).
4. Al terminar: `kaggle kernels output` de los dos en `results/factorial4_2026-10-13/<kernel>/` y
   `python3 tools/factorial4/agregar_factorial4.py results/factorial4_2026-10-13 results/factorial3_2026-10-13`.
5. A git van el `agregado.log`, el MD5SUMS de todo lo bajado, los recibos y las tablas compactas. Los json con la
   predicción de cada ensayo (≈ 1,6 MB) no tienen vía directa a git desde brain-env: quedan por md5 salvo que haya un
   token para este repo.

## Prueba del agregador antes de sellar

`python3 tools/factorial4/prueba_agregar_factorial4.py results/factorial4_2026-10-13_humo/t4 results/factorial3_2026-10-13 <trabajo>`
tiene que dar `PRUEBA_AGREGADOR -> PASA 5/5`: el humo real de Kaggle da VALIDO; el mismo con un W tocado da INVALIDO por
integridad; y tres sintéticos hechos con los json del factorial 3 dan la primaria del factorial 3 exacta, la escala en
cero (EQUIVALENTE), y con W ± 0,02 dan SUPERA o NO_SUPERIOR y PIERDE: el instrumento puede dar cada color.
