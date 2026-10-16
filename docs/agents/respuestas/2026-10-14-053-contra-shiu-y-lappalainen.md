# 2026-10-14-053 · Contra Shiu y Lappalainen: reproducimos a Shiu exacto y, con una neurona de tasa, recuperamos su mapa pero no su motora; de Lappalainen nos separa la validación contra actividad medida, y lo propio son los rivales y los nulos sellados

**Fecha:** 2026-10-16, 12:20 (America/Buenos_Aires)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23637

## Pedido

«Compará estos resultados con Shiu y Lappalainen» (Abraham, 16-oct 12:08), después de la 052. «Estos resultados» son los de la mosca entera (045 a 051) y, para Lappalainen, los del banco del escape con lector (H_RIVAL, H_LECTOR, H_TAU_LIBRE), que es lo que se parece a su método.

## Veredicto primero

- **[MEDIDO] Con Shiu compartimos todo lo que se puede compartir.** Mismo archivo de conectividad (byte a byte), mismo código (`model.py`, blob 5ba7083c), mismo estímulo (20 de sus 21 sensores de azúcar existen en v783) y misma lectura (MN9). Lo reprodujimos: MN9 dispara en 30 de 30 ensayos a 100 Hz y en 0 de 20 con pesos barajados (049). Shiu reporta 100% contra 1 de 100.
- **[MEDIDO] Con nuestra neurona de tasa, el mapa de Shiu sale y su motora no sale firme.** SparseLTC prende 172 de sus 321 neuronas (J 0,366; con umbral, 0,332) y ningún barajado pasa de 103. MN9: REFUTADA sin umbral y SIN_DECIDIR con umbral.
- **[MEDIDO] Contra el barajado que usó Shiu, el umbral sale limpio.** Shiu baraja pesos manteniendo su distribución, como nuestro SHUF_W. Con el umbral de la 051, MN9 queda en cero en los 40 SHUF_W, como su 1 de 100. Lo que nos frena es SHUF_G (destinos barajados con los mismos grados), un nulo que no está en el texto principal de Shiu: uno solo de 40 llega a MN9, el k32.
- **[CONCLUSION] Lo que esto dice del modelo de Shiu.** Lo que no depende de la neurona (mismo cableado, tasa o espigas) es a quién recluta el azúcar. La salida motora fina sí depende de la no linealidad: sin umbral, la tasa la ahoga entre 48.407 neuronas; con el presupuesto de actividad del LIF entra en el puesto 269. En su texto principal no compara modelos de neurona; nosotros sí, sobre su mismo caso.
- **[MEDIDO] Lappalainen hace otra cosa: predice actividad medida, no conducta.** Lóbulo óptico, 64 tipos, 45.669 neuronas, 734 parámetros libres por tipo (τ, potencial de reposo y fuerza sináptica unitaria), entrenados por gradiente para estimar flujo óptico; ensamble de 50 modelos contra 26 estudios; acierta ON/OFF en 32 de 32 tipos (mediana del ensamble).
- **[MEDIDO] Lo nuestro que se parece a su método (cableado más partes entrenadas):** con un lector entrenado sobre las 6 descendentes, el cableado real de R2 le gana a sus 40 barajados en las 4 combinaciones, también con τ que nadie eligió (H_LECTOR_CABLEADO y H_TAU_LIBRE SOSTENIDAS), y queda a 0,29 puntos de un ridge sobre las 564 entradas crudas. Sin ese lector, el ridge le gana por 5 puntos (H_RIVAL REFUTADA).
- **[CONCLUSION] Coincidimos con Lappalainen en el mensaje y no en la vara.** Los dos encontramos que el cableado exacto restringe la función. Ellos lo comprobaron contra registros de neuronas; nosotros, contra barajados, una regla de diseño y rivales entrenados. Nuestra única prueba contra registros (H4) no llegó: 16 de 16 ROI públicos sin mapear a FlyWire.
- **[CONCLUSION] Por qué la neurona líquida no pagó en la mosca entera.** Lappalainen eligió una tarea donde el tiempo importa (el movimiento se calcula comparando instantes) y entrenó τ por tipo. Nuestra lectura del azúcar es un estado estable: ahí τ no puede importar por construcción. Para medir la líquida hace falta una tarea temporal.
- **[CONCLUSION, opinión] Dónde quedamos.** Detrás de los dos en validación (cero datos de moscas vivas o de registros). Adelante en cómo se prueba: bandas selladas antes de ver, dos familias de nulos, rivales justos, réplica en dos máquinas y negativos publicados. Por lo que medimos, estamos más cerca de Shiu; por el método (cableado más partes entrenadas), de Lappalainen.
- **[CORRIGE la 2026-10-13-013]** Allá escribí que Lappalainen «entrena los parámetros de cada neurona». Son parámetros por tipo de célula: 734 en total para 45.669 neuronas.

## Contra Shiu et al., Nature 634: 210-219 (2024), doi 10.1038/s41586-024-07763-9

| | Shiu | Nosotros (045 a 051) |
|---|---|---|
| Modelo de neurona | LIF con espigas en Brian2; un solo parámetro libre (W_syn) | SparseLTC de tasa (tanh), τ sorteada por neurona; variante con umbral calibrado (UMB) |
| Conectoma | FlyWire; el paper reporta 127.400 neuronas modeladas | su archivo público de la versión 783, byte a byte: 138.639 neuronas, 15.091.983 conexiones |
| Estímulo y lectura | sensores de azúcar a MN9 (eleva el rostro de la trompa) | los mismos, 20 de 21 presentes en v783, y MN9 |
| Vara | moscas: optogenética de 106 tipos del SEZ, 10 de 11 predichos positivos aciertan, más del 90%; 10 de 10 tipos conocidos responden al azúcar | su LIF, reproducido: 30 de 30, 0 de 20 barajados, 321 neuronas a 1 Hz o más |
| Barajado | pesos barajados manteniendo la distribución: 1 de 100 activa MN9 | SHUF_W (pesos) y SHUF_G (destinos), 40 de cada uno |
| Mapa | 45 neuronas activas a 10 Hz y 455 a 200 Hz | 172 de 321 (J 0,366); 0,332 con umbral; barajados 103 como mucho |
| Motora | robusta en el LIF | REFUTADA sin umbral (18 de 80 barajados la igualan); SIN_DECIDIR con umbral (0 de 40 SHUF_W, 1 de 40 SHUF_G) |
| Costo en el mismo tipo de runner de Actions | 30 ensayos de 1 s en 480 s | 3,7 s por corrida determinista |
| Lo que tienen y no tenemos | validación en moscas vivas | |
| Lo que tenemos y no tienen | | un segundo modelo de neurona sobre su mismo caso; el nulo de destinos (no está en su texto principal); un rival sin dinámica; bandas selladas |

## Contra Lappalainen et al., Nature 634: 1132-1140 (2024), doi 10.1038/s41586-024-07939-3

| | Lappalainen | Nosotros |
|---|---|---|
| Región | vías de movimiento del lóbulo óptico: 64 tipos, 45.669 neuronas, 1.513.231 conexiones, conectoma consenso teselado | cerebro entero (138.639) y recortes del escape (R2: 33.489) |
| Neurona | sin espigas, lineal con fuga; sinapsis umbral-lineal | tasa tanh; la UMB corta abajo con un umbral global, parecido al umbral-lineal |
| Qué se entrena | 734 parámetros por tipo, por gradiente, con un decodificador, para el flujo óptico | τ elegida por validación cruzada (H_TAU) y un ridge sobre 6 descendentes (H_LECTOR); en la mosca entera, nada |
| Vara | actividad registrada en 26 estudios | conducta simulada contra barajados, la regla de diseño y rivales entrenados; un modelo validado (Shiu) |
| Resultado | conectividad más tarea predicen la actividad; mejor con conectividad rala | el cableado exacto es necesario (les gana a sus barajados en el escape y en el mapa del azúcar) pero no es el mejor lector de sus entradas |
| Lo que tienen y no tenemos | registros de neuronas como vara; τ que importa porque la tarea es temporal | |
| Lo que tenemos y no tienen | | conducta con cinco acciones, rivales con los mismos sensores, nulos sellados, réplica en dos máquinas |

## Qué acortaría la distancia (opinión, sin sellar)

1. **Correr el LIF de Shiu sobre los 40 SHUF_G.** Ese nulo no está en el texto principal de Shiu y es el que frenó a MN9. Si su LIF también llega a MN9 en k32, el nulo abre un atajo y la vara tiene el mismo límite; si no llega, su LIF es más específico que nuestra tasa. Con 10 ensayos por nulo serían unas 2 h de CPU, repartidas en Actions. Hay que sellarlo antes.
2. **Una vara de actividad, como la de Lappalainen:** registros públicos del SEZ con neuronas identificadas en FlyWire. Que existan con mapeo es NO MEDIDO; la búsqueda de H4 se agotó en otra región.

## Herramientas y máquina

- **Web:** las páginas de Nature de los dos artículos (acceso abierto), leídas el 16-oct: resumen y secciones principales. No leí sus métodos completos ni los suplementos.
- **brain-env:** el sello 046 y `lif_real.json` de la 049 (clon `x051`): `r_poi` 100 Hz, 30 ensayos de 1000 ms, MN9 a 61,6 Hz, S_LIF de 321 a 1 Hz o más, 480 s; prueba del parche del CONTEXTO en copia.
- **Conector GitHub:** CONTEXTO en `6046da8` y las respuestas 2026-10-13-013, 2026-10-14-034, 038, 041, 049, 051 y 052.

## Evidencia cruda

```
# Shiu et al. 2024, Nature (pagina del articulo, 16-oct)
"modelling using the correct connectome results in robust activation of MN9 in 100% of simulations when sugar-sensing neurons are activated at 100 Hz, only 1 of 100 shuffled simulations did"
"connectivity weights were shuffled randomly (while maintaining the global connectivity weight distribution)"
"Of the 127,400 neurons modelled, we found that 45 are predicted to respond to 10 Hz sugar GRN activation, and 455 to 200 Hz"
"the computational model can predict the activation phenotypes of a non-biased sample of cell types at greater than 90% accuracy"
# Lappalainen et al. 2024, Nature (pagina del articulo, 16-oct)
"the connectome-constrained model comprises 45,669 neurons and 1,513,231 connections, across 64 cell types"
"a marked reduction to just 734 free parameters"
"We found that model predictions agreed with experimental measurements of neural activity across 26 studies"
"this strategy is more likely to be successful when neurons are sparsely connected"
# lif_real.json de la 049 (results/mosca_entera_2026-10-15/actions_correr/)
{'ensayos_mn9': 30, 'n_run': 30, 'tasa_mn9': 61.633, 'activas': 393, 'K': 321, 'segundos': 479.6}
# agregado_umb.log de la 051
NULOS SHUF_W n=40 mn9_max=0
NULOS SHUF_G n=40 mn9_max=0.00158085
VEREDICTO H_UMB_MN9 SIN_DECIDIR nulos_ge={'SHUF_W': 0, 'SHUF_G': 1}
```

## Archivos

| Archivo | md5 |
|---|---|
| `tools/contexto/actualizar_contexto_2026-10-14-053.py` (`main`) | cef61b50a5017edf8304ea94846bc932 |
| CONTEXTO antes y después del parche (copia en brain-env; la segunda pasada aborta) | 84908d5339f30a6116c7ce40c16ec8ea y 5aef709ef3f6cc84d375f61ea09dcf97 |

## NO MEDIDO

- Si el LIF de Shiu llega a MN9 con SHUF_G.
- Nada nuestro contra moscas vivas ni contra registros de neuronas.
- Los métodos completos y los suplementos de los dos artículos.
- Una revisión sistemática de quién más comparó modelos de neurona sobre el mismo conectoma.
- Si existen registros públicos del SEZ mapeados a FlyWire.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Lo que dicen Shiu y Lappalainen | sus páginas en Nature, citadas textual | Sí: la cita podía no estar o decir otra cosa | medido |
| Reproducimos a Shiu con sus parámetros | sello 046 y `lif_real.json` de la 049 | Sí | medido |
| SHUF_W es el barajado de Shiu | su frase textual contra `nulo()` de `liq_entera.py` (permuta pesos entre aristas) | Parcial: no leí su código de barajado | CONCLUSION |
| Shiu no corrió un nulo de destinos | lectura del texto principal, no de los suplementos | Parcial | CONCLUSION |
| Comparación de costo | logs de dos trabajos de Actions del mismo tipo de runner | Sí, pero miden cosas distintas (30 ensayos estocásticos contra una corrida determinista) | descriptivo |
| El parche del CONTEXTO aplica | copia en brain-env; segunda pasada aborta | Sí | medido |

--- METODO PROMETEO ---
Rol: comparación con la literatura. Delicado: no.
Máquinas: web (Nature), brain-env (lectura y parche), conector GitHub.
Archivo: `docs/agents/respuestas/2026-10-14-053-contra-shiu-y-lappalainen.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23637
