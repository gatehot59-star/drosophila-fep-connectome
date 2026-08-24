# 019 · Diff literal: `bicam/cell1.py::DualBrain` vs `tres_brazos.py::DualBrain`

**Fecha:** 2026-08-24 00:39 (America/Buenos_Aires)

## 1. Pedido

"Mostrame el diff exacto contra DualBrain" y despues "Show the literal code diff". Se pide el diff **literal** de codigo, no una descripcion.

## 2. Herramientas declaradas (C-03)

- `gateway build.run` (shell dentro del container `brain-env`, en la PC de Abraham). **Solo lectura** de `/workspace` + escritura de un script temporal en `/tmp/d.py`. Ninguna ejecucion de entrenamiento, cero cuota de Kaggle.
- `githubmcp_get_file_contents` (lectura del arbol de respuestas).
- `githubmcp_create_or_update_file` (este commit).

## 3. Que se midio

- `grep -rln "class DualBrain" /workspace` -> **21 archivos** contienen la clase. Los dos sujetos relevantes:
  - BICAMERALITY: `/workspace/bicam/cell1.py`, md5 `9d89a158f809ff5f3765f42848502665`
  - Linea actual: `/workspace/tres_brazos.py`, md5 `73196d78e8d8290fa8feaa0caf883e82`
- Extraccion de la clase por indentacion, no por ojo: 44 lineas (bicam) vs 23 lineas (actual).
- Script del instrumento: `/tmp/d.py`, md5 `80b13362fdb9f2cc48d0520b40095b0f`, `exit=0`.

## 4. Evidencia cruda verbatim

```
9d89a158f809ff5f3765f42848502665  /workspace/bicam/cell1.py
73196d78e8d8290fa8feaa0caf883e82  /workspace/tres_brazos.py
80b13362fdb9f2cc48d0520b40095b0f  /tmp/d.py
BICAM lines= 44
DUAL  lines= 23
---UNIFIED DIFF START---
--- bicam/cell1.py::DualBrain
+++ tres_brazos.py::DualBrain
@@ -1,44 +1,23 @@
 class DualBrain(nn.Module):
-    """v5.6 champion. Reactive cortex + memory hippocampus + gate."""
-    def __init__(self, obs_dim, act_dim, H_react=24, H_mem=8):
+    def __init__(self, ind, outd, h_r=24, h_m=8):
         super().__init__()
-        self.H_mem = H_mem
-        self.react = nn.Sequential(
-            nn.Linear(obs_dim, H_react), nn.Tanh(),
-            nn.Linear(H_react, H_react), nn.Tanh())
-        self.mem_enc = nn.Linear(obs_dim, H_mem)
-        self.mem_cell = LiquidRealCell(H_mem)
-        self.mem_gate = nn.Sequential(
-            nn.Linear(H_react + H_mem, 1), nn.Sigmoid())
-        combined = H_react + H_mem
-        self.actor = nn.Sequential(nn.Linear(combined, act_dim), nn.Tanh())
-        self.log_std = nn.Parameter(torch.full((act_dim,), -0.5))
-        self.critic = nn.Linear(combined, 1)
-
-    def init_states(self, B, device=None):
-        if device is None:
-            device = next(self.parameters()).device
-        return torch.zeros(B, self.H_mem, device=device)
-
-    def forward(self, obs, states=None):
-        B = obs.shape[0]
-        if states is None:
-            states = self.init_states(B)
-        h_r = self.react(obs)
-        x_m = F.gelu(self.mem_enc(obs))
-        h_m, tau = self.mem_cell(x_m, states)
-        gate = self.mem_gate(torch.cat([h_r, h_m], -1))
-        z = torch.cat([h_r, gate * h_m], -1)
-        mean = self.actor(z)
-        lstd = self.log_std.expand(B, -1)
-        lstd = torch.clamp(lstd, -3, 0.5)
-        val = self.critic(z)
-        info = {}
-        if not torch.is_grad_enabled():
-            info = {'tau': tau.mean().item(), 'gate': gate.mean().item(),
-                    'alpha': -1.0}
-        return mean, lstd, val, h_m, info
-
-    @property
-    def is_recurrent(self):
-        return True
+        self.h_m = h_m
+        self.react = nn.Sequential(nn.Linear(ind,h_r),nn.Tanh(),nn.Linear(h_r,h_r),nn.Tanh())
+        self.enc = nn.Sequential(nn.Linear(ind,h_m),nn.GELU())
+        self.cell = LiquidCell(h_m, h_m)
+        self.gate = nn.Linear(h_r+h_m, h_m)
+        nn.init.zeros_(self.gate.weight); nn.init.zeros_(self.gate.bias)
+        self.head = nn.Linear(h_r+h_m, outd)
+    def forward(self, xs, h=None, probe=False):
+        T,B,_ = xs.shape
+        if h is None: h = xs.new_zeros(B, self.h_m)
+        out, hs, ts, gs = [], [], [], []
+        for t in range(T):
+            hr = self.react(xs[t])
+            hm, tau = self.cell(self.enc(xs[t]), h); h = hm
+            g = torch.sigmoid(self.gate(torch.cat([hr,hm],-1)))
+            out.append(self.head(torch.cat([hr, g*hm],-1)))
+            if probe: hs.append(hm); ts.append(tau); gs.append(g)
+        if probe:
+            return torch.stack(out), torch.stack(hs), torch.stack(ts), torch.stack(gs)
+        return torch.stack(out)
---UNIFIED DIFF END---
EXIT=0
```

## 5. Lectura del diff — que cambia de verdad

| Aspecto | BICAMERALITY (v5.6) | Linea actual | Es diferencia real? |
|---|---|---|---|
| Gate | `Sequential(Linear(H_r+H_m, 1), Sigmoid())` — **escalar** | `Linear(h_r+h_m, h_m)` **cero-inicializado**, sigmoid en el forward — **vectorial** | **SI, y es LA diferencia** |
| Cabezas | `actor` + `log_std` + `critic` (politica gaussiana de RL) | una sola `head` lineal | **SI**: RL vs regresion supervisada |
| Celda | `LiquidRealCell(H_mem)` | `LiquidCell(h_m, h_m)` | **SI** (clase distinta, firma distinta) |
| Forward | **un paso** por llamada, el estado lo lleva el que llama | **loop interno sobre T**, devuelve la secuencia apilada | **SI** |
| Instrumentacion | `info` solo cuando `torch.is_grad_enabled()` es False, y solo promedios | flag `probe` que devuelve `hm`, `tau`, `gate` completos por paso | **SI, y el nuevo mide mejor** |
| Encoder de memoria | `mem_enc = Linear`, y `F.gelu(...)` **aplicado en el forward** | `enc = Sequential(Linear, GELU)` | **NO. Es el mismo calculo, movido de lugar** |
| Defaults | `H_react=24`, `H_mem=8` | `h_r=24`, `h_m=8` | **NO. Identicos** |
| Composicion de `react` | `Linear->Tanh->Linear->Tanh` | `Linear->Tanh->Linear->Tanh` | **NO. Identica** |

### El punto no obvio del gate cero-inicializado

`nn.init.zeros_` sobre peso **y** bias hace que en el paso 0 valga `sigmoid(0) = 0.5` **exacto en todas las dimensiones**. O sea: arranca en mezcla neutra y aprende a abrir o cerrar cada dimension de `h_m` por separado. El viejo arrancaba en un escalar aleatorio y solo podia subir o bajar el volumen de **toda** la memoria a la vez.

## 6. Correccion de un error propio (E-01)

En la respuesta anterior del chat afirme, entre las diferencias: *"enc: Linear vs Linear+GELU"*. **Es falso y el diff lo prueba**: la linea `x_m = F.gelu(self.mem_enc(obs))` del viejo aplica exactamente el mismo GELU, solo que en el `forward` en vez de en el `Sequential`. Concluí sobre el `__init__` sin leer el `forward` del mismo archivo. Es el patron 4 del Bloque 8 (sujeto equivocado), y esta vez el sujeto equivocado fue **medio archivo**.

Lo que **si** se sostiene de esa respuesta: gate escalar -> vectorial, cabezas RL -> `head`, defaults 24/8 identicos, ancestro estructural.

## 7. Archivos generados

- Este archivo.
- `/tmp/d.py` en el container (efimero, md5 arriba; su salida esta transcripta verbatim en §4, asi que el veredicto es recomputable sin el).

## 8. NO MEDIDO, declarado

- **No compare `LiquidRealCell` contra `LiquidCell`.** El diff es de la clase `DualBrain` unicamente. La diferencia de las celdas puede ser mas grande que la del gate y no lo se.
- **No conte parametros de las dos versiones al mismo `obs_dim`.** El 1822 del viejo viene de una medicion anterior; el del nuevo no esta medido en esta pasada.
- **No corri ninguna de las dos.** Este es un diff estatico. Que el gate vectorial ayude sigue estando medido solo en el benchmark del proyecto (gate 4/4), no en un A/B escalar-vs-vectorial al mismo presupuesto. **Ese experimento no existe.**
- **`cell1_fixed.py` no entro en el diff.** Es el archivo parcheado por mi en la auditoria, no la version original de BICAMERALITY.

```
--- METODO TITAN ---
Accion delicada: NO (lectura + un script temporal en /tmp del container propio;
                 ninguna corrida de entrenamiento, cero cuota ajena nueva)
Modo aplicado:   TITAN LIGERO (pedido puntual: mostrar un diff de un archivo)
Rubrica:         N/A (modo ligero)
N/A declarados:  N/A (modo ligero)
Review externo:  no pedido, sin PR asociado
Instrumento:     build.run sobre brain-env, python3 + difflib, exit=0.
                 /tmp/d.py md5 80b13362fdb9f2cc48d0520b40095b0f
                 Sujetos: bicam/cell1.py md5 9d89a158f809ff5f3765f42848502665
                          tres_brazos.py md5 73196d78e8d8290fa8feaa0caf883e82
                 Salida cruda verbatim en la seccion 4.
                 NO MEDIDO: seccion 8.
```
