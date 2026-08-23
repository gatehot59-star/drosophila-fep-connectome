# CONTEXTO VIVO · motor / DualBrain / línea embebida

**Última actualización:** 2026-08-23 20:45 (America/Buenos_Aires) · **Se sobreescribe, no se acumula.**

Protocolo: `00-PROTOCOLO-BITACORA-DE-RESPUESTAS.md`. Hermano: `CONTEXTO-drosophila-fep.md`.

**Por qué este archivo existe aparte:** el motor es el activo monetizable y se lo trató como apéndice de los papers durante 24 h. Los papers son el test suite del motor, no al revés.

---

## 1. Los tres motores, y NO son el mismo

| Motor | Archivo | Qué es | ¿Entrena? |
|---|---|---|---|
| **SparseLTC** | `scriptR.py` · `motor.py` (702 líneas, md5 `480539069ec00f317eec525e6fa81324`) | 138.639 neuronas reales, τ por neurona, esparsa | **NO. Cero torch, cero Adam, cero backward** |
| **`LiquidCell` denso** | `tres_brazos.py` · `hm_sweep.py` · brazo W | 8 unidades, densa, Adam | Sí |
| **DualBrain embebido** | `esp32c.py`, C99 | **704 B de RAM**, dos vías + gate multiplicativo | Vía lenta sí, vía rápida no |

**Confundirlos ya costó un veredicto falso.** Ver §4.

---

## 2. La especificación de SparseLTC, verbatim del código

```
z ← (1−τ)·z + τ·f(Wᵗz + s)
```

1. **Pesos complejos:** `|w|` del conectoma, `arg(w)` = signo E/I **por neurona presináptica, no por arista**. Es la ley de Dale y en este conectoma es exacta: **0 de 138.005** neuronas tienen salidas de los dos signos (96.672 excitatorias puras, 41.333 inhibitorias puras). Jitter de fase 0,1. Normaliza a radio espectral 0,99.
2. **τ compleja heterogénea:** `Re(τ)=0,119` fijo, `Im(τ) ~ U(0,01 · 0,15)` distinto por neurona → **banco de osciladores**, no un oscilador.
3. **Guard derivado, no tuneado:** `|Im(τ)| < sqrt(1 − (1−Re)²)` = **0,473116**. `validate_tau` levanta excepción antes de correr.
4. **Activación:** `bounded_complex_tanh` acota el módulo y **preserva la fase**. La tanh cruda explota a 10¹¹.
5. **τ regional:** `SparseLTCRegional` guarda τ como vector por región. Cuerpo fungiforme 0,0180 (56 pasos de memoria) vs óptica 0,2689 (3,7 pasos), **factor 15×**: la zona más lenta es justo el 4% plástico. **PERO las 11 τ están hardcodeadas en `CFG` y las regiones suman 139.255 contra 139.244 reales: es andamio sintético, no medición.**

---

## 3. Medido a favor

| Qué | Número | Instrumento |
|---|---|---|
| Ventaja de τ compleja | **+0,196 en el real vs −0,027 en los nulls, 0 de 9** | `motor.py` en Kaggle. **Log no bajado** |
| Tests del motor complejo | **8 en verde** (τ rechaza 0,48; tanh cruda explota; 0 violan Dale; CP preserva grado en 138.639 nodos) | mismo kernel |
| Spread de τ heterogénea | 31,2× entre la dimensión más lenta y la más rápida | medición propia |
| Gate multiplicativo | ayuda en **4 de 4** tareas | tres brazos |
| Óptimo de reparto react/memoria | h_m=10 / h_r=22 → **1,18× sobre LSTM** (publicado 4,05×, que es el **peor punto** de la curva) | barrido, mejora 3,44×, p=8,6×10⁻¹⁰ |
| Brazo más congelado (42,5% entrenable) | le gana a un modelo 100% entrenado sin estructura por **3,2× a 35×**, 4/4 tareas | tres brazos |
| Escape compilado | ganancia **40×** vs detector vecino no cableado (LC4+LPLC2 = 0,704 · LC6 = 0,017) | motor propio |

---

## 4. Refutado, y el falso refutado

| Claim | Estado |
|---|---|
| «la vía reactiva no necesita entrenarse» (tres brazos) | **REFUTADO pero mal medido**: congeló pesos **aleatorios**, no cableados. Midió el null de la hipótesis, no la hipótesis |
| «el brazo W retira la analogía del 96% fijo» (0/4 vs ruido) | **NO MEDIDO, no refutado.** W congela una submatriz de 26 nodos dentro del motor **denso**, no dentro de SparseLTC, **y no congela τ**: quedan dos efectos mezclados |
| «con más memoria DualBrain gana en MultiCue» | refutado: no gana, y hay **óptimo interior** en h_m=10. Refuta también la explicación del paper |
| «el circuito de escape detecta aproximación» | refutado: selectividad temporal **1,04×**, o sea ninguna. Es un integrador con exclusión. 13.026 aristas y **cero inhibitorias** |
| «la topología explica la función» | refutado para este circuito: la topología define **ruteo y ganancia**, no selectividad |

**El motor nunca falló en ninguna corrida.** Las nueve fallas encontradas fueron de interpretación, normalización, estimador o diseño de métrica.

---

## 5. El producto, en una línea

**Que el motor deje de necesitar entrenamiento para funcionar.** Topología cableada de fábrica: vía rápida por estructura (reflejo, sin memoria), vía lenta con τ heterogénea acumulando contexto, gate decidiendo cuál manda. Funciona **el primer día, sin dataset**, en 704 B.

- **Es cedible:** un motor con pesos entrenados necesita quien sepa entrenarlo; uno cuya vía rápida es estructura necesita un compilador y una tabla de priors. Lo mantiene un aprendiz.
- **Escala por unidades, no por parámetros.** Lo que hay que escalar es **el compilador**.
- **El activo final no es el motor: es la biblioteca** de circuitos con función verificada (la hoja de datos de los 74xx). El motor es el intérprete.
- **Competidor medido:** Liquid AI (Hasani, 293 M USD, unicornio). Su producto más chico es LFM2.5-230M en Raspberry Pi. Ellos **entrenan**; abajo del teléfono no entran. Citar: complex-valued RNN (2016), echo state networks, «When Learning Hurts: Fixed-Pole RNN» (arXiv 2026).

---

## 6. NO MEDIDO / pendiente

1. **`motor.py` NO está en git.** Vive en `/workspace` y en el kernel. Riesgo abierto más caro.
2. Log de `titan-motor-ltc-complejo` (complete 15:06Z): **nunca bajado**. El `+0,196 / 0 de 9` viene de reporte, no de lectura verificada.
3. Log de `titan-paper-dualbrain` (complete 00:06Z) y `notebookceb82767da` (928 KB): sin leer.
4. **La hipótesis del 96% fijo sigue sin testear** sobre SparseLTC. El experimento correcto congela matriz **y** τ.
5. Con 9 nulls el piso de p a dos colas es **0,20**: prueba de concepto del instrumento, no el número del paper.
6. Las 11 τ regionales: hardcodeadas, sin medición que las respalde.
7. Regla de tres factores (KC × MBON × dopamina, mayormente **depresión**) contra descenso de gradiente: diseñada, **no lanzada**. Base medida: `DAN→KC` es 23,5× `DAN→MBON`, 8,71× sobre CP, 0/40 → firma presináptica.
8. Duplicado `paper_db.py` / `dualbrain_src.py`, md5 idéntico `8a42246b5415`: sin resolver.
