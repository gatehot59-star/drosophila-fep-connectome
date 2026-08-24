# 024 · `LiquidRealCell` **no es otra celda**: es `LiquidCell` + un vector de bias

**Fecha:** 2026-08-24 ~08:40 (America/Buenos_Aires)
**Estado:** equivalencia **PROBADA**. A/B del bias **CORRIENDO**, `resultado_leido = 0`. Ver §6.

## 1. Pedido

"Corré LiquidRealCell vs LiquidCell ahora". Cierra el último NO MEDIDO que quedó abierto en la resp 023.

## 2. Herramientas declaradas (C-03)

`gateway build.run` sobre `brain-env`: lectura de las dos clases, un script de equivalencia, y **2 procesos de entrenamiento en background** (~40 min de CPU de la PC de Abraham). Cero cuota de Kaggle. GitHub para este commit.

## 3. Las dos clases, verbatim del disco

```python
class LiquidRealCell(nn.Module):            # /workspace/bicam/cell1.py
    """Standard tau cell WITH LayerNorm. For DualBrain."""
    def __init__(self, H):
        super().__init__()
        self.H = H
        self.W_flow = nn.Linear(H * 2, H)
        self.W_tau = nn.Sequential(nn.Linear(H * 2, H), nn.Sigmoid())
        self.norm = nn.LayerNorm(H)
        nn.init.constant_(self.W_tau[0].bias, -2.0)

    def forward(self, x, h):
        cat = torch.cat([x, h], dim=-1)
        target = torch.tanh(self.W_flow(cat))
        tau = self.W_tau(cat)
        h_new = h * (1 - tau) + target * tau
        h_new = self.norm(h_new)
        return h_new, tau
```

```python
class LiquidCell(nn.Module):                # /workspace/tres_brazos.py
    def __init__(self, inp, hid, tau_bias=-2.0):
        super().__init__()
        self.W_in = nn.Linear(inp, hid, bias=False)
        self.W_res = nn.Linear(hid, hid, bias=False)
        self.tau = nn.Linear(inp+hid, hid)
        nn.init.constant_(self.tau.bias, tau_bias)
        self.ln = nn.LayerNorm(hid)
    def forward(self, x, h):
        t = torch.sigmoid(self.tau(torch.cat([x,h],-1)))
        f = torch.tanh(self.W_in(x)+self.W_res(h))
        return self.ln((1-t)*h + t*f), t
```

## 4. EL HALLAZGO — son la MISMA función salvo un bias

**Un `Linear` sobre la concatenación ES la suma de dos `Linear` sobre las partes:**

```
W_flow([x ; h]) = W_flow[:, :H] @ x  +  W_flow[:, H:] @ h  +  b_flow
W_in(x) + W_res(h) = W_in @ x  +  W_res @ h                      (sin bias)
```

O sea que `W_flow` **no es una arquitectura distinta de** `W_in`+`W_res`: es la misma parametrización escrita en una línea en vez de dos. Y el término de `tau` es idéntico en las dos, con el mismo `bias = -2.0`.

**La única diferencia real: `LiquidRealCell` tiene un bias en el término de flujo y `LiquidCell` no.** H parámetros.

### Evidencia cruda — transplante de pesos (`/workspace/ab_cell/equiv.py`)

Copio `W_flow.weight[:, :H] → W_in`, `W_flow.weight[:, H:] → W_res`, `W_tau[0] → tau`, `norm → ln`, y comparo salidas sobre el mismo `x, h` aleatorio (B=64, H=8):

```
params LiquidRealCell: 288
params LiquidCell    : 280
   A W_flow.weight (8, 16)
   A W_flow.bias (8,)
   A W_tau.0.weight (8, 16)
   A W_tau.0.bias (8,)
   A norm.weight (8,)
   A norm.bias (8,)
   B W_in.weight (8, 8)
   B W_res.weight (8, 8)
   B tau.weight (8, 16)
   B tau.bias (8,)
   B ln.weight (8,)
   B ln.bias (8,)

CON el bias de flow que tiene LiquidRealCell (init aleatorio):
   err_max h  = 0.13120055198669434
   err_max tau= 0.0

CON el bias de flow puesto en CERO:
   err_max h  = 3.5762786865234375e-07
   err_max tau= 0.0
```

Tres números y cada uno cierra una pregunta:

1. **288 − 280 = 8 = H.** La diferencia de parámetros es exactamente el bias, ni uno más.
2. **Con el bias en cero, `err_max h = 3,58e−07`.** Eso es ruido de `float32`, no una diferencia de modelo. **Son la misma función.**
3. **`err_max tau = 0.0` exacto, con y sin bias.** El cálculo de `tau` es bit-idéntico. La celda de constante de tiempo — el corazón del argumento del "banco de filtros adaptativo" — **no cambió nunca entre BICAMERALITY y la línea actual.**

## 5. Consecuencias — y me corrijo a mí mismo dos veces

**Corrección 1 (resp 023, cierre):** escribí *"`LiquidRealCell` vs `LiquidCell`: puede ser más grande que la del gate"*. **Falso, y por bastante.** La del gate es una diferencia de forma (escalar vs vectorial) que cambia lo que el modelo puede expresar y midió 8,34×. Ésta es un vector de bias de 5 a 8 parámetros sobre ~1400, o sea **0,4%**, dentro de una función por lo demás idéntica. Lo dije sin medir, y medirlo costaba 20 segundos.

**Corrección 2 (resp 019, el diff):** puse `LiquidRealCell(H)` → `LiquidCell(h_m, h_m)` en la columna "**SI**, es diferencia real (clase distinta, firma distinta)". La firma sí cambió; **la función no**. Un cambio de firma no es un cambio de arquitectura, y presentarlo como tal es el mismo error de leer la declaración en vez del cálculo por el que ya me comí el `GELU` en esa misma respuesta.

**Consecuencia buena, y es la que importa para el paper:** el linaje de BICAMERALITY a la línea actual es **más limpio** de lo que parecía. **Un solo cambio funcional en toda la celda de memoria: ninguno.** El único cambio arquitectónico real entre las dos versiones de `DualBrain` es el gate escalar→vectorial, y ése ya está medido con `p<1e-9` (resp 023). No hay una segunda variable escondida.

**Consecuencia metodológica:** el A/B baja de 6 brazos a **2**, porque no hay presupuesto que igualar (0,4%) ni init que aislar. La pregunta bien planteada es una sola: **¿sirve el bias en el término de flujo?**

## 6. TRABAJO VIVO — `resultado_leido = 0`

| Campo | Valor |
|---|---|
| Dónde | container `brain-env`, `/workspace/ab_cell/` |
| Qué | 2 brazos (`flow_bias` off/on) × 4 tareas × 6 semillas × 2000 steps |
| Proceso A | `TAG=A`, tareas `CR,Gated` → `cellA.log` |
| Proceso B | `TAG=B`, tareas `MultiCue,LinScale` → `cellB.log` |
| Lanzado | 2026-08-24 ~08:38, `loadavg 2.55` sobre 2 núcleos (los dos quemando CPU) |
| ETA | ~40 min |
| Cómo se lee | `tail -30 /workspace/ab_cell/cellA.log` y `cellB.log`, o los JSON |
| Estado | **CORRIENDO, SIN LEER** |

Dos precauciones aplicadas por los errores anteriores: **rutas absolutas** en el lanzamiento (resp 021: `cd X && ... &` backgroundea la cadena y el segundo proceso muere), y **TAG distinto por proceso** verificado en los logs antes de seguir (resp 021: dos procesos con el mismo TAG se pisan el archivo).

### Predicción declarada ANTES de leer el resultado

**Espero empate en las 4 tareas.** Un bias sobre un término que ya entra a un `tanh` y después a un `LayerNorm` — que **resta la media** — es el parámetro con menos chance de importar de todo el modelo: el `LayerNorm` posterior debería absorber buena parte de un corrimiento constante. Si el bias gana en alguna tarea con `p<0,05`, mi razonamiento sobre el `LayerNorm` está mal y quiero saberlo.

Queda escrito antes del dato para no poder acomodar la narrativa después, igual que en la resp 020 (donde el smoke me engañó y estaba declarado).

## 7. Archivos generados

- `/workspace/ab_cell/equiv.py` — la prueba de equivalencia
- `/workspace/ab_cell/ab_cell.py` — 221 líneas, `ast.parse` OK, celda **única parametrizada** por `flow_bias` (así el A/B no puede diferir en nada más por accidente)
- `/workspace/ab_cell/ab_cell_smoke.json`, `cellA.log`, `cellB.log`, `ab_cell_A.json`, `ab_cell_B.json` (guardado incremental por brazo)
- Este archivo.

## 8. NO MEDIDO, declarado

- **El resultado del A/B no existe todavía.** El smoke (2 semillas, 40 steps) dio `ratio=0,997× p=0,925`, o sea nada, y con 40 steps **no mide**. No citar.
- **La equivalencia se probó con `H=8`, `B=64`, una sola semilla de inicialización.** El argumento algebraico es general, pero la verificación numérica es de un caso.
- **`LiquidRealCell` exige `inp == hid`** (hace `Linear(H*2, H)`), `LiquidCell` no. En `DualBrain` se cumple siempre (`enc` sale a `h_m`), así que no cambia nada acá, pero **no es intercambiable en general**.
- **No comparé el resto de `cell1.py`** contra la línea actual: esto es la celda, no el archivo.
- **n=6 semillas.** Para detectar el efecto de 0,4% de los parámetros esto es poco: si sale empate, el enunciado correcto es "no detectable con n=6", no "no existe".

```
--- METODO TITAN ---
Accion delicada: NO en cuanto a datos (nada se borra ni se mergea, cero cuota
                 ajena). SI en cuanto a recurso: ~40 min de CPU en la PC de
                 Abraham, 2 procesos. Declarado al lanzar.
Modo aplicado:   TITAN FULL
Rubrica:         se emite con el resultado del A/B. La equivalencia de la
                 seccion 4 ya esta medida y es independiente de ese resultado.
N/A declarados:  pendiente
Review externo:  no pedido, sin PR asociado. El falsador fue el propio
                 instrumento: retira mi prediccion de la resp 023 de que esta
                 diferencia podia ser mayor que la del gate, y corrige la
                 tabla del diff de la resp 019.
Instrumento:     build.run sobre brain-env, python3 3.12 / torch 2.13.0+cpu,
                 nproc=2, THREADS=1.
                 equiv.py: transplante de pesos, err_max h = 3.5762786865234375e-07
                 con bias en cero, err_max tau = 0.0 exacto. Salida cruda
                 verbatim y sin recortar en la seccion 4.
                 A/B: NO MEDIDO TODAVIA (seccion 6).
```
