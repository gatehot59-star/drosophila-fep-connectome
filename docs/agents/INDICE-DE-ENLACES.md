# ÍNDICE DE ENLACES · lo generado en la jornada del 23-ago-2026

**Recopilado:** 2026-08-23 23:04 · **Fuente:** los dos bloques de chat que Abraham pegó, que son el registro de un tercio de 30+ horas de trabajo.

**Por qué existe este archivo:** los enlaces vivían solo dentro del texto de la conversación. Cuando el chat se corta por tamaño, se van con él. Acá quedan.

---

## 1. Docs de auditoría · AGOSTO, estado vigente

A diferencia del corpus de marzo (cerrado en resp 009), estos cuatro son de la jornada de agosto y **sí son estado vivo**.

| # | Doc | De qué es |
|---|---|---|
| 1 | [Auditoría de la jornada completa: 11/11 chequeos de coherencia OK, y el barrido de h_m me REFUTA a mí pero MEJORA tu paper 3,44×](https://app.clickup.com/90171457413/docs/2kza6fw5-4117) | 98/100. DualBrain pasa de perder 4,05× a 1,18× contra LSTM. El veredicto correcto **no** es el que imprime el kernel |
| 2 | [PLAN MAESTRO 10 SEMANAS · 24-ago al 8-nov 2026](https://app.clickup.com/90171457413/docs/2kza6fw5-4137) | 100/100. Producto en 3 capas, 5 papers, inventario de 13 hallazgos con su null, método y **criterio de aborto** por actividad. **Arranca el lunes 24** |
| 3 | [Los tres brazos cerraron: mi predicción está REFUTADA 4/4](https://app.clickup.com/90171457413/docs/2kza6fw5-4157) | Congelar `react` empeora siempre. Pero el brazo más congelado le gana a un modelo entrenado **sin** la estructura por 3,2× a 35×. Error de diseño propio: congeló un `react` **aleatorio**, no cableado |
| 4 | [SparseLTC NO está en los tres brazos: son DOS motores distintos](https://app.clickup.com/90171457413/docs/2kza6fw5-4177) | τ del cuerpo fungiforme 0,0180 vs óptica 0,2689, factor 15×, **y esos números están puestos a mano** |

**Hallazgo al indexar:** el título del #4 ya dice que SparseLTC y los tres brazos son motores distintos. O sea que la distinción que hoy vengo tratando como aporte propio **ya estaba escrita y titulada en agosto**. Mismo patrón que el guard de tautología, que estaba en el §2.4 del Paper 1.

---

## 2. Artefacto interactivo

| Artefacto | Qué tiene |
|---|---|
| [tres-brazos-dashboard.html](https://run.clickup.ai/90171457413/a9077e09-2830-494f-b32c-0652a8f2a0b9/tres-brazos-dashboard.html) | Hipótesis, qué aisló cada brazo, las 4 tareas, resultados **semilla por semilla**, el código por etapas y el flujo lógico |

Y el de hoy, no pedido en ese bloque pero de la misma línea:

| Artefacto | Qué tiene |
|---|---|
| [titan-cronologia-auditoria.html](https://run.clickup.ai/90171457413/500636cd-3ece-4876-ac44-ae95295db4de/titan-cronologia-auditoria.html) | 41 eventos fechados, eje proporcional, 4 carriles. 11 validados, 13 refutados, 8 sin medir |

---

## 3. Kernels de Kaggle citados en esos bloques

| Kernel | Estado |
|---|---|
| [titan-tres-brazos](https://www.kaggle.com/code/abrahammendieta/titan-tres-brazos) | complete. Leído. Refuta 4/4, pero midió el null de la hipótesis |
| [titan-brazo-w](https://www.kaggle.com/code/abrahammendieta/titan-brazo-w) | complete. Leído con ~2 h de retraso. **NO refuta el 96% fijo**: motor denso, 26 nodos, τ sin congelar |
| [titan-motor-ltc-complejo](https://www.kaggle.com/code/abrahammendieta/titan-motor-ltc-complejo) | complete. Log bajado hoy → `results/motor_ltc_complejo.log`. **Test global p = 0,6000** |

---

## 4. Destino de las tareas

| Dónde | Para qué |
|---|---|
| [luz delmis tarraga's List](https://app.clickup.com/90171457413/v/li/901715932722) | Donde irían las **11 tareas** del plan maestro. Siguen **sin crear**: son 11 escrituras y esperan el OK de Abraham |

---

## 5. Código y evidencia ya en este repo

Lo que esos bloques de chat produjeron y hoy vive versionado:

- `src/motor.py` (702 líneas, md5 `480539069ec00f317eec525e6fa81324`) · `results/motor_ltc_complejo.log`
- `src/scriptR.py` (30/30 valores reproducidos) · `src/nulls40_kaggle.py` · `src/cp40.py`
- `src/hm_sweep.py` · `results/hm_sweep.log`
- `docs/agents/CONTEXTO-drosophila-fep.md` · `docs/agents/CONTEXTO-motor.md`
- `docs/agents/respuestas/` · 10 archivos de respuesta del 23-ago

---

## 6. NO MEDIDO

- **De los Docs 1, 3 y 4 se leyó el título, no el contenido interno.** Sus números pueden contener más correcciones que no están en el contexto vivo.
- **No verifiqué si el dashboard sigue accesible.**
- **No sé si en los dos bloques había más enlaces** en la parte que quedó fuera del texto pegado.
