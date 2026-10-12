# 2026-10-11-015 · Firma de la 014 (gana la semilla 0, no todas) y en criollo qué tenemos y su potencial

**Doc público:** https://app.clickup.com/90171457413/docs/2kza6fw5-21257

## 1. Pedido

- Botón «Firmar la 014: más semillas y más redes SL» (ofrecido en la 014, donde p = 0,04 era el mínimo con 24 SL).
- Mientras corría, verbatim: «EN CRIOLLO QUE TENEMOS ENTRE MANOS, CUAL ES SU POTENCIAL,».

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, 2 procesos, Python 3.12.14, numpy 2.5.3, scipy): humo, corrida de 54,79 min, md5 en clon fresco.
- **Sandbox de ClickUp:** escritura del script.
- **GitHub:** pre-registro y md5 sellado en `967fbb2`; script y log en `cc531e7`, rama `titan/escape-motivo-2026-10-11`.
- Script `tools/escape_motivo/firmar_plena_sl.py`, md5 `df15f3da3ed27fba262c5733dc92fc6a`; importa `control_plena.py` de la 014 y lee su `resultados.json` (md5 `f2792e6a…` verificado).
- Acción delicada: NO.

## 3. Veredicto

**VEREDICTO_FIRMA = SOLO LA SEMILLA 0.** No se firma como regla general.

- **Q1:** W semilla 0 (0,9802) contra 69 SL (24 de la 014 + 45 nuevas): 0/69, p = 0,014 → W GANA.
- **Q2:** la peor de 8 semillas de W (0,9469) contra 69 SL: 25/69, p = 0,37 → W NO GANA.
- **Q3 (descriptivo):** semillas 0 a 3 (0,9802 / 0,9844 / 0,9812 / 0,9844): 0/69 cada una; semillas 4 a 7 (0,9615 / 0,9469 / 0,9531 / 0,9729): 14, 25, 20 y 5 de 69. Mann-Whitney unilateral U = 488 de 552 (AUC 0,88), p = 0,0002.
- REPRODUCE=True (las semillas 0 a 3 dan exacto lo de la 012).

**Lectura:** en grupo, la mosca entrenada le gana a SL entrenada el 88% de las veces; un entrenamiento individual no siempre. La 014 («la mosca vuelve a ganarle a SL») queda como tendencia fuerte, no como garantía. Las SL se entrenaron con una semilla cada una: su dispersión mezcla red y entrenamiento.

**Log, líneas verbatim** (`results/firmar_plena_sl_2026-10-11/run.log`, md5 `48b74e4c569d351fafda72667e5dcced`, 77 líneas, en `cc531e7`):

```
CHEQUEO INSTRUMENTO VALIDO
LEIDO_014 W_semilla0=0.9802 SL=24
GUARDA redes_nulas_ok=True SL_total=69 distintas=True
REPRODUCE=True W_por_semilla=0.9802,0.9844,0.9812,0.9844,0.9615,0.9469,0.9531,0.9729
RESUMEN SL_n=69 SL_media=0.9165 SL_max=0.9781 SL_viejas_media=0.9090 SL_nuevas_media=0.9205
CONTRASTE Q1_semilla0 W=0.9802 n_SL>=W=0/69 p=0.0143 -> W GANA
CONTRASTE Q2_peor_semilla W=0.9469 n_SL>=W=25/69 p=0.3714 -> W NO GANA
Q3 mann_whitney_U=488.0 p_unilateral=0.0002068
VEREDICTO_FIRMA=SOLO LA SEMILLA 0: LA PEOR SEMILLA DE W NO LE GANA A SL
minutos=54.79
EXIT_RUN=0
```

## 4. En criollo: qué tenemos y su potencial

**Qué tenemos:** un pedazo real de la mosca (el circuito del escape, 26 neuronas y 88 cables de FlyWire) que en simulación:

- sin entrenar, escapa de lo que se acerca y no se asusta con lo que gira, y le gana a su versión barajada en esa función (010, 011); en tareas genéricas no le gana (008);
- con la τ líquida plena entrenada llega a 0,98, y le gana a un rival no líquido con los mismos parámetros (012 a 014);
- ya entrenado, le gana al barajado que conserva el lado en promedio, no siempre (015).

Además: el diagnóstico del dron de `swarm/` (escapa hacia la amenaza; parche probado en simulación, sin aplicar) y el paper con la Tabla 7 reproducible y el erratum v2 sin depositar.

**Potencial, en mi lectura:**

1. **Producto:** reflejos de mosca compilados a microcontroladores (BEEC v2). 26 neuronas y unos 1.400 parámetros, pocos KB; útil desde el día cero y afinable entrenando sólo la τ. Para drones o robots baratos que tienen que esquivar.
2. **Ciencia:** un resultado honesto y publicable: el cableado paga en su función y no en tareas genéricas; la τ líquida paga entrenada y en forma plena. Con la cadena de pre-registros y md5.
3. **Método:** la receta de motivo certificado contra el nulo se repite con otros circuitos.

**Techo actual:** todo en simulación, un motivo, una tarea, un modelo de entrada propio, una máquina; el reflejo escrito a mano rinde 0,91 sin entrenar, así que falta ganarle a la ingeniería clásica; cero hardware.

**Qué lo destraba, en orden:** parche del dron y este reflejo montado en su simulación; la plena en Q15 sobre un ESP32; un segundo motivo; review externo.

## 5. Archivos

- `tools/escape_motivo/PREREGISTRO-firmar-plena-sl.md` en `967fbb2`.
- `tools/escape_motivo/firmar_plena_sl.py` y `results/firmar_plena_sl_2026-10-11/run.log` en `cc531e7`; md5 2/2 en clon fresco.
- `resultados.json` (md5 `9cecc23384e776aca519a60b342a2650`): sólo en brain-env.
- Doc de ClickUp: https://app.clickup.com/90171457413/docs/2kza6fw5-21257. Banner en el Doc de la 014.
- `docs/agents/CONTEXTO-drosophila-fep.md` actualizado en este commit.

## 6. NO MEDIDO

- SL con varias semillas de entrenamiento cada una.
- La plena sobre S; condiciones fuera de las entrenadas; el otro modelo de entrada.
- Hardware (ESP32, dron real), segunda máquina, review externo.

## 7. QA

Rúbrica 54/60 → 90/100; N/A 40. Se respetó la regla estricta aunque no favorecía. −6: SL con una sola semilla, sin hardware ni review externo.

--- METODO PROMETEO ---
Máquina: brain-env (Celeron N4020, 2 procesos); sandbox de ClickUp para escribir el script
Artefactos: `docs/agents/respuestas/2026-10-11-015-firma-de-la-014-y-en-criollo.md` + https://app.clickup.com/90171457413/docs/2kza6fw5-21257
