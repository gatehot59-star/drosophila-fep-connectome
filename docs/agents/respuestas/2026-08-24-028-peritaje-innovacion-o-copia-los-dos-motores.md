# 028 · Peritaje: ¿innovación o copia? Los dos motores, pieza por pieza

**Fecha:** 2026-08-24 ~11:20 (America/Buenos_Aires)

## 1. Pedido

"EN CRIOLLO QUE ES EL MOTOR SPARSELTC?, PARA QUE SIRVE, DONDE SE APLICA, ES INNOVACION O COPIA DE ALGO EXISTENTE, EXPLICA PARTE POR PARTE Y LO MISMO CON EL MOTOR COMPLEJO. TITAN FULL: EJECUTA".

Router: **auditoría / peritaje**, TITAN FULL por pedido explícito. Aplicables (R-01): Completitud, Arquitectura del razonamiento, Documentación, Innovación, Proceso QA. N/A: Ejecutabilidad, Seguridad, Testing, DevOps (55 pts).

## 2. Herramientas declaradas (C-03)

- `gateway build.run` sobre `brain-env`: lectura de `motor.py` (funciones 73-162, 250-300, 576-700) y del notebook `CODE__fabiomurillohot__notebookc3cbda5fcc.txt`; dos mediciones numéricas propias en `/tmp`.
- **Búsqueda web en vivo (V-01)**, dos consultas: prior art de LTC y prior art de RNN compleja.
- `load_assets` sobre `task:86e2qeakt` (TITAN-COUNCIL v5.4, la tarea que citó).
- `create_document` + este commit.
- **Cero cuota de Kaggle. Ninguna corrida de entrenamiento.** La corrida `LinScale` n=20 sigue viva (`ab_cell20.py`, TAG `n20a` SEED0=0 / `n20b` SEED0=10) y no fue tocada.

## 3. Entregable

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-4397

Seis partes: `SparseLTC` pieza por pieza (7 piezas) · motor complejo pieza por pieza (5 piezas) · innovación vs copia con tabla de prior art de 10 filas · cara a cara · NO MEDIDO · orden de trabajo. Scorecard **44/45 → 98/100**.

## 4. VEREDICTO CENTRAL

**La matemática de los dos motores es prior art. Lo potencialmente novedoso es con qué se llena y que no entrena.**

| Pieza | Veredicto | Fuente verificada hoy |
|---|---|---|
| `h ← (1−τ)h + τ·f(...)` con τ variable | **COPIA** | Liquid Time-Constant Networks, Hasani, Lechner, Amini, Rus, Grosu. arXiv 1811.00321 (2018), arXiv 2006.04439, **AAAI-21 pp. 7657-7666**. Código oficial publicado |
| Forma cerrada | COPIA | Closed-form continuous-time neural networks, **Nature Machine Intelligence 2022**, mismos autores |
| RNN compleja | **COPIA** | Minin, Knoll, Zimmermann (**Siemens**), JSIP 2012. Arjovsky, Shah, **Bengio**, arXiv 1511.06464 (2015), 226 citas |
| Acotar módulo preservando fase | COPIA conceptual | `modReLU`, Arjovsky et al. 2015. La implementación con manejo de polos sí es propia |
| Gate complejo | COPIA | Wolter & Yao, **NeurIPS 2018** |
| Red compleja oscilatoria | COPIA | Frontiers in Comp. Neuroscience 2021 |
| Radio espectral <1 sin entrenar recurrencia | COPIA (reservoir/echo state) | **NO VERIFICADO en vivo**, declarado |
| **Fase = Dale por neurona presináptica desde conectoma medido** | **no encontrado publicado** | candidato |
| **τ compleja heterogénea por neurona, no aprendida, a 138.639** | **no encontrado publicado** | candidato |
| **El motor entero sin entrenar** | **el más fuerte** | encaja con Zador (Nature Comms 2019) y genomic bottleneck (PNAS 2024), que argumentan lo mismo **sin la matriz medida** |

**Y la conclusión que va contra el encuadre actual del proyecto: el pedazo que se trata como la innovación central (la τ compleja) es justo el que ya está medido y NO da (test global p = 0,6000). Lo que sobrevive a nulls con grado preservado es estructural y no necesita aritmética compleja.**

Consecuencia editorial, y es lo primero de la lista de trabajo: **el paper hoy defiende la pieza débil.** El claim correcto es "el cableado medido hace cosas que ningún grafo aleatorio con el mismo grado hace, y funciona sin entrenar", no "inventé un motor complejo".

## 5. MEDICIÓN NUEVA · qué hace `Im(τ)`, con número

Evidencia cruda verbatim (`/tmp/osc.py`, python3 3.12 + numpy):

```
Im   |1-tau|   arg(1-tau)  ciclos/paso  pasos/vuelta  vida_media
0.0 0.881 0.0 0.0 0 5.5
0.01 0.881057 -0.01135 0.001806 553.6 5.5
0.05 0.882418 -0.056693 0.009023 110.8 5.5
0.1 0.886657 -0.113024 0.017988 55.6 5.8
0.15 0.893678 -0.168644 0.026841 37.3 6.2
RANGO de frecuencias: 14.858
```

Dos hallazgos que no estaban dichos así en ningún documento del proyecto:

1. **El rango de frecuencias del banco es 14,858×**: de una vuelta cada 553,6 pasos a una cada 37,3. Eso justifica con número la palabra "banco de osciladores" en vez de "oscilador".
2. **`Im(τ)` mueve la frecuencia 1.386% y la vida media solo 12%** (5,5 → 6,2 pasos). **Son dos perillas casi independientes:** frecuencia y duración de memoria se controlan por separado. Es una propiedad vendible del diseño y estaba sin enunciar.
3. Control: con τ real, `arg(1−τ) = 0.0` exacto. Cero rotación. Confirma que el brazo `tau_r` de `motor.py` es el régimen de `SparseLTC` (resp 027).

## 6. Hallazgo colateral que sigue abierto

`ConnectomeDualBrain` (notebook de marzo) es **DualBrain sobre el conectoma real** con gate escalar `sigmoid(mh.mean() - 0.5)`. `motor.py` no lo tiene. Y en la resp 025 se midió que **el gate escalar se satura abierto en 3/4 tareas** del motor denso, o sea que aprende a no gatear. **Nadie miró si sobre el conectoma pasa lo mismo.** Experimento barato, tirado.

## 7. NO MEDIDO, declarado

- **La búsqueda de prior art NO es exhaustiva y NO incluye patentes.** Dos consultas de literatura académica. **Para un claim de patente esto NO alcanza.** Es el hueco más grande del entregable y está en negrita en el Doc.
- **Prior art de reservoir computing / echo state: NO VERIFICADO en vivo.** Marcado como tal en la tabla.
- **No corrí ninguno de los dos motores.** Los números de propagación (p=0,6000, +0,19644, −0,02973) son del log ya leído.
- **El rango de 14,858× es derivación analítica de `arg(1−τ)`, no medición sobre el conectoma.** Que la red *pueda* oscilar a esas frecuencias no prueba que la dinámica real las use.
- **`SparseLTCModel` está definido 9 veces** en el notebook; leí la última y no verifiqué si son idénticas.
- **No leí los resultados de `ConnectomeDualBrain`.**
- **Las 11 τ regionales siguen hardcodeadas** y las regiones suman 139.255 vs 139.244 reales.
- **La hipótesis del 96% fijo sigue sin testear** sobre estos motores.

```
--- METODO TITAN ---
Accion delicada: NO. Lectura de codigo, dos mediciones en /tmp, busqueda web,
                 un Doc, un commit. Cero cuota de Kaggle, ninguna corrida de
                 entrenamiento. La corrida LinScale n=20 sigue viva, sin tocar.
Modo aplicado:   TITAN FULL (pedido explicito)
Rubrica:         44/45 -> 98/100
N/A declarados:  55 pts (Ejecutabilidad, Seguridad, Testing, DevOps: es
                 peritaje, no entrega de codigo)
Review externo:  no pedido, sin PR. DEUDA declarada (K-02).
                 El falsador fue la busqueda en vivo: la ecuacion del motor
                 resulta prior art de Hasani et al. y la aritmetica compleja
                 en RNN es de 2012-2015. Ninguna de las dos era mia ni suya.
Instrumento:     build.run sobre brain-env, python3 3.12 / numpy.
                 /tmp/osc.py -> rango de frecuencias 14.858x (salida cruda
                 verbatim en la seccion 5, sin recortar)
                 fase preservada: bounded=True, clamp=False
                 sigmoid(-2.0) = 0.119203
                 Busqueda web V-01 el 2026-08-24, URLs consultadas:
                   arxiv.org/pdf/1811.00321
                   arxiv.org/pdf/2006.04439
                   ojs.aaai.org/index.php/AAAI/article/download/16936/16743
                   nature.com/articles/s42256-022-00556-7
                   mediatum.ub.tum.de/doc/1287177/785740.pdf (JSIP 2012)
                   arxiv.org/pdf/1511.06464
                   papers.neurips.cc/paper/8253-complex-gated-recurrent-neural-networks.pdf
                   frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2021.551111/full
                 NO MEDIDO: seccion 7, con el hueco de patentes primero.
```
