# 2026-10-11-016 · Cómo operan las 26 neuronas: ecuación de SparseLTC, sin DualBrain en el escape; la líquida que ganó tiene la forma de la LiquidCell

**Doc público:** https://app.clickup.com/90171457413/docs/2kza6fw5-21277

## 1. Pedido

Verbatim: «PERO ESTAS 26 NURONAS, COMO OPERAN A TRAVES DE DUAL BRAIN O DE SPARECELTC?»

## 2. Herramientas y máquina

- **brain-env** (lectura): `grep` y `sed` sobre `tools/escape_motivo/escape_dificil.py`, `escape_motivo.py`, `liquida_entrenada.py` y `tools/brazo_s/brazo_s_recurrente.py` del clon de `titan/escape-motivo-2026-10-11`; `find` de las copias de `mojo-absoluto` en el taller.
- **GitHub** (lectura): `mojo-absoluto` en `main` (`613bf49`): `include/mojo_abs/connectome_ltc.hpp`, `include/mojo_abs/sparse_ltc_projector.hpp` y `docs/adr/2026-10-01-sparseltc-dbc3-adapter.md`. La búsqueda de código de GitHub devolvió 0 resultados (índice incompleto); por eso se leyó por ruta.
- Escrituras: este archivo, el contexto y el Doc de ClickUp. Ninguna corrida. Acción delicada: NO.

## 3. Respuesta

**En el escape (010 a 015), las 26 corren con la ecuación de SparseLTC y no pasan por DualBrain.** La ecuación está reescrita en numpy dentro de `escape_dificil.py` (no se importa la librería C++), con estado real, la matriz del motivo (26×26, 88 no ceros) llevada a radio espectral 0,9, y la entrada visual directa a las 20 visuales.

- **Equivalencia:** el `step()` de SparseLTC hace z + dt·(−z + tanh acotada(drive))/τ_ef, que es (1 − t)·z + t·tanh(drive) con t = dt/τ_ef: la misma ecuación del escape. Con tau_gain = 0 es la FIJA_HET de la 011.
- **La τ líquida no es la misma:** la nativa de SparseLTC es τ_ef = τ / (1 + tau_gain·|drive|), un parámetro por neurona que acelera con la intensidad. La que ganó en la 012 a la 015 es t = sigmoid(b + Vx·x + Vh·z), **la forma de la LiquidCell de DualBrain** aplicada a cada una de las 26. La nativa nunca se probó en el escape.
- **DualBrain entró sólo en la 008:** las 26 como vía react recurrente adentro de DualBrain (`DualBrainRecurrente`), con cables, entrada U y τ congelados; se entrenaban la memoria líquida de 8 unidades, la compuerta y la cabeza. En tareas genéricas, empate con el barajado 4/4.
- **En el escape no hay DualBrain:** sin memoria, sin compuerta, sin cabeza; la lectura es un umbral fijo sobre las dos fibras gigantes. En la 012 a la 015 sólo se entrena la τ.
- **El diseño del puente** (ADR del 1-oct, «Propuesto»): SparseLTC sobre el conectoma → proyección a features → un solo DBC3 por flujo como lectura y controlador (D1: no por neurona). Según el propio ADR, «Todavía no existe una corrida SparseLTC → DBC3 real».

**Evidencia cruda, verbatim:**

`tools/escape_motivo/escape_dificil.py` (md5 `2c95e63b6ad3ff590057df80368134d7`), líneas 140 a 156:

```
def paso(z, x, Wn, nolin, modo, ctx):
    """Un paso de z <- (1 - tau) z + tau phi(W z + x)."""
    pre = z @ Wn.T + x
    f = pre if nolin == "LINEAL" else np.tanh(pre)
    if modo == "LIQUIDA":
        tt = 1.0 / (1.0 + np.exp(-(ctx["logit_het"][None, :] + x @ ctx["Vx"].T + z @ ctx["Vh"].T)))
    elif modo == "FIJA_HET":
        tt = ctx["tau_het"][None, :]
    elif modo == "FIJA_UNI":
        tt = np.full((1, 26), TAU_UNI)
    else:
        raise SystemExit("ABORTA: modo de tau " + modo)
    z = (1.0 - tt) * z + tt * f
```

`grep` de imports en los cuatro scripts del escape y del brazo S: el escape sólo importa librería estándar y numpy; `brazo_s_recurrente.py` importa torch y define `LiquidCell`, `DualBrain`, `ReactRecurrente` y `DualBrainRecurrente`.

`mojo-absoluto` `include/mojo_abs/connectome_ltc.hpp` (`main`, `613bf49`), `SparseConnectomeComplexLTC::step`:

```
Complex drive=cell.bias+external_drive.at({target});
for(std::size_t edge=topology_.incoming_begin(target);edge<topology_.incoming_end(target);++edge){const Synapse& synapse=topology_.incoming_synapse(edge);drive+=synapse.weight*state_.at({synapse.source});}
const double effective_tau=cell.tau/(1.0+cell.tau_gain*std::abs(drive));
const Complex current=state_.at({target});
next.at({target})=current+dt*((-current+liquid::bounded_complex_tanh(drive))/effective_tau);
```

`tools/brazo_s/brazo_s_recurrente.py`, `LiquidCell` («copiado VERBATIM de brazo_w.py»):

```
t = torch.sigmoid(self.tau(torch.cat([x,h],-1)))
f = torch.tanh(self.W_in(x)+self.W_res(h))
return self.ln((1-t)*h + t*f), t
```

Y `ReactRecurrente`: «Via react como reservorio SparseLTC real y congelado: z = (1 - tau) z + tau tanh(W z + U x)».

ADR `docs/adr/2026-10-01-sparseltc-dbc3-adapter.md`: «D1. DBC3 es readout/controlador, no célula por neurona»; flujo `SparseConnectomeComplexLTC::step() → ISparseLtcProjector::project() → IDbc3Backend::infer()`; «Todavía no existe una corrida SparseLTC → DBC3 real». La proyección de `sparse_ltc_projector.hpp` da 4 features: mean_real, mean_imag, mean_abs, max_abs.

## 4. Archivos

- Este archivo y `docs/agents/CONTEXTO-drosophila-fep.md` (actualizado) en este commit.
- Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-21277.

## 5. NO MEDIDO

- La líquida nativa de SparseLTC (tau_gain, 26 parámetros) en el escape, contra su control.
- Las 26 con estado complejo.
- Las 26 con DBC3 como lectura y controlador; el puente SparseLTC → DBC3 sobre el escape.
- Paridad numérica entre el numpy del escape y el `step()` de C++: sólo está la equivalencia algebraica.

## 6. QA

Respuesta verificada contra el código que corrió y contra `main` de `mojo-absoluto`, no de memoria. Rúbrica N/A (sin ejecución). Deuda: sin review externo.

--- METODO PROMETEO ---
Máquina: brain-env y GitHub (lectura); ninguna corrida
Artefactos: `docs/agents/respuestas/2026-10-11-016-como-operan-las-26-neuronas.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21277
