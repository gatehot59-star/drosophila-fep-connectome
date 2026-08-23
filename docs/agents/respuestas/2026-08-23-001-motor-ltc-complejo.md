# resp 001 · ¿Dónde está el motor complejo, qué es y cómo funciona?

**Fecha:** 2026-08-23 20:25–20:37 (America/Buenos_Aires)

## 1. Pedido

> «DIME DONDE ESTA ESTE MOTOR QUE ES Y COMO FUNCIONA», sobre el mensaje que anunciaba *702 líneas, 10 módulos* en el kernel `titan-motor-ltc-complejo`.

Contexto del pedido: en el tramo anterior del chat se había perdido el hilo del motor, hasta el punto de tratarlo como genérico después de haberlo nombrado y especificado al inicio del mismo chat.

## 2. Herramientas declaradas (C-03)

- gateway MUDH → `build.run` sobre el container: **solo lectura** (`ls`, `grep`, `sed`, `wc`, `md5sum`).
- API de Kaggle: **no se llamó** en esta respuesta. Cero cuota consumida, cero escrituras.

## 3. Qué se midió

```
/workspace/motor.py   702 líneas   30.644 B
md5  480539069ec00f317eec525e6fa81324      mtime Aug 23 15:06
kernel: abrahammendieta/titan-motor-ltc-complejo  (complete, log NO bajado)

grep -ci sparseltc  motor.py -> 0
grep -ci liquidcell motor.py -> 0
grep -ci 'torch|adam|backward' motor.py -> 0    <- NO ENTRENA NADA
```

**Es el tercer motor y el único que implementa la especificación de Abraham.** No es el `LiquidCell` denso de 8 unidades entrenado con Adam de `tres_brazos.py` / brazo W.

### Los 10 módulos

1. Estabilidad · 2. Activación · 3. Pesos complejos desde el conectoma · 4. Nulls (MS y CP) · 5. Dinámica · 6. Métricas · 7. Test global con guard de tautología · 8. Datos con checksum · 9. Tests que pueden dar rojo · 10. Experimento falsable.

### Las cinco piezas del mecanismo

**a) Pesos complejos.** `|w|` del conectoma, `arg(w)` = signo E/I asignado **por neurona presináptica, no por arista** (ley de Dale). Medido: 96.672 puramente excitatorias, 41.333 inhibitorias, **0 mixtas de 138.005**. Jitter de fase 0,1 rompe la simetría sin cambiar el signo. Normaliza a radio espectral 0,99.

**b) τ compleja heterogénea.** `Re(τ)=0,119` (valor del paper, sobrevivió la auditoría), `Im(τ) ~ U(0,01 · 0,15)` distinto por neurona. Eso convierte la red en un **banco de osciladores** en vez de un oscilador.

**c) Guard derivado, no tuneado.** El factor del estado previo es `(1−τ)`; si `|1−τ| > 1` divergís por construcción. Límite exacto `|Im| < sqrt(1 − (1−Re)²)` = **0,473116**. `validate_tau` levanta excepción antes de correr.

**d) Dinámica.** `z ← (1−τ)·z + τ·f(Wᵀz + s)`, 200 pasos, estímulo t=10→60, `bounded_complex_tanh` que acota el módulo y **preserva la fase** (la tanh cruda explota a 10¹¹).

**e) Medición diseñada para poder fallar.** Cada grafo corre **dos veces en la misma pasada**, τ compleja y τ real, comparación **pareada dentro del grafo**: `ventaja_compleja = rdi_cplx − rdi_real` en t=60/120/199, más coherencia de fase. RDI devuelve NaN en vez de premiar estados muertos. Contra 9 nulls CP, con test global de rangos y guard de tautología (`sd=0 → NO TESTEABLE`).

`test_uniform_choice_would_fail` verifica que el método uniforme **sí** rompe el grado: es el control del control.

## 4. Evidencia cruda (W-01)

```python
def tau_stability_limit(tau_real):
    inner = 1.0 - (1.0 - tau_real) ** 2
    return math.sqrt(inner) if inner > 0.0 else 0.0

# build_complex_weights
is_inh = neg > pos
base   = np.where(is_inh[pre], np.pi, 0.0)
phases = base + rng.normal(0.0, phase_jitter, pre.shape[0])
data   = np.abs(w).astype(np.float64) * np.exp(1j * phases)

# propagate
for t in range(n_steps):
    drive = WT.dot(z)
    if t_on <= t <= t_off:
        drive = drive + s
    z = one_minus * z + tau * activation(drive)
```

Resultado ya reportado del kernel: **ventaja de τ compleja +0,196 en el real contra −0,027 en los nulls, 0 de 9.** 8 tests en verde.

## 5. Archivos generados por esta respuesta

- `docs/agents/00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`
- `docs/agents/CONTEXTO-drosophila-fep.md`
- este archivo

## 6. NO MEDIDO, declarado

- **El log del kernel no se bajó.** El `+0,196 / −0,027, 0/9` viene de un reporte previo, no de una lectura verificada en esta respuesta.
- **`motor.py` no está en git todavía.** Vive en un solo disco y en un kernel de Kaggle. Es el riesgo abierto más caro de esta respuesta.
- Con 9 nulls el piso de p a dos colas es **0,20**: prueba de concepto del instrumento, no el número del paper.
- No se verificó si las 11 τ regionales de `SparseLTCRegional` salen de una medición: en el andamio anterior estaban hardcodeadas y las regiones sumaban 139.255 contra 139.244 reales.
