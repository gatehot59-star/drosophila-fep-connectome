# 2026-10-13-010 · Factorial 3: R2 alcanza a la regla con sus mismos sensores (+0,85, no pasa el margen) y le gana a los 100 barajados por 15 a 28 puntos

## Veredicto

- **[MEDIDO] VÁLIDO.** El run 38420175126 terminó con success en sus 81 trabajos.
  - Resultados del bot en `09ffbc1` (rama `titan/factorial3-mosca-2026-10-13`); MD5SUMS 163 de 163 OK.
  - Los 81 trabajos corrieron con las mismas versiones (numpy 2.5.3, scipy 1.18.1, torch 2.14.1+cpu) y los mismos insumos (conn `3d802fd5…`, annot `719904ab…`).
- **[MEDIDO] Controles, todos True:**
  - ancla exacta;
  - plan 600/600 y 50 + 50;
  - TAU_DN_IGUAL en 10 semillas;
  - **REPRODUCE_F2 exacto:** las 90 corridas comunes dan los mismos números que el factorial 2;
  - **REAL_IGUAL:** 0,9465 en la grilla y 0,9465 en los dos trabajos de nulos que miden el real.
- **[MEDIDO] Primaria, R2 contra la regla con sus mismos 564 sensores: NO_INFERIOR.**
  - Acierto: R2 0,9353 contra 0,9268 de la regla.
  - Diferencia +0,85 puntos, IC90 [+0,08; +1,51].
  - R2 gana en 482 corridas, empata en 2 y pierde en 116, de 600.
  - Las 6 celdas dan NO_INFERIOR, con diferencias de +0,42 a +1,18.
- **[MEDIDO] H_SUPERA_R2: SIN_DECIDIR.** El intervalo arranca arriba de 0 pero no arriba de +1 punto, que es el margen pre-registrado.
- **[MEDIDO] H_CABLEADO_R2: SOSTENIDA.**
  - El real da 0,9465.
  - 50 SL dan media 0,666 (máximo 0,796); 50 T dan media 0,760 (máximo 0,839).
  - Ninguno de los 100 iguala al real.
  - p = 0,0196 en cada uno, que es el mínimo posible con 50; con Holm queda 0,039.
- **[CONCLUSIÓN] El cableado real de R2 pesa mucho y alcanza al diseño.**
  - Con los mismos grados y lados pero destinos barajados (SL) cae 28 puntos; con los tipos mal asignados (T) cae 19.
  - Contra la regla diseñada con sus mismos sensores queda arriba por menos de un punto: la alcanza, no la supera por el margen.
  - El +1,28 del factorial 2 (3 × 5 semillas) bajó a +0,85 con 10 × 10. Era en parte suerte de pocas semillas.

## Pedido

ClickKit `leer_factorial3_013` (13-oct, 15:41): leer el factorial 3.

## Herramientas y máquina

- **Actions x64:** run 38420175126, 81 trabajos y el agregado, en Linux 6.17 azure.
- **brain-env:**
  - API pública (estado de jobs);
  - clon de `09ffbc1`;
  - `md5sum -c MD5SUMS.txt`;
  - conteo de ganadas y perdidas, guardas y radios de los nulos, versiones;
  - prueba del parche del CONTEXTO.
- **GitHub MCP:** este commit.

## Evidencia cruda

```
run 38420175126: completed success | 81/81 trabajos success (ancla 1, nulos 20, grilla 60) + agregar
09ffbc1 medicion(2026-10-13-008): factorial 3 de la mosca en Actions x64, 81 trabajos y agregado
MD5SUMS: 163 OK, 0 FAILED | agregado.log ba3aecfd… | MD5SUMS.txt 3fb0f772…
JSON grilla=60 nulos=20 ancla=1 validos=True
CHEQUEO ANCLA_015 -> True
CHEQUEO TAU_DN_IGUAL semillas=10 -> True
CHEQUEO PLAN_GRILLA corridas=600 faltan=0
CHEQUEO REPRODUCE_F2 corridas_comparadas=90 tolerancia=True exacto=True -> True
CHEQUEO REAL_IGUAL grilla=0.9465 script_de_nulos=[0.9465, 0.9465] -> True
CHEQUEO PLAN_NULOS SL=50 T=50 -> True
PRIMARIA R2_CON_TASA W=0.9353 regla_propia=0.9268 dif=+0.0085 IC90=[+0.0008, +0.0151] corridas=600 -> NO_INFERIOR
  CELDA 0.0|0.15 dif=+0.0107 IC=[-0.0032, +0.0203] -> NO_INFERIOR
  CELDA 0.0|0.45 dif=+0.0118 IC=[+0.0008, +0.0203] -> NO_INFERIOR
  CELDA 0.3|0.15 dif=+0.0092 IC=[-0.0038, +0.0184] -> NO_INFERIOR
  CELDA 0.3|0.45 dif=+0.0102 IC=[-0.0003, +0.0179] -> NO_INFERIOR
  CELDA 0.6|0.15 dif=+0.0042 IC=[-0.0085, +0.0131] -> NO_INFERIOR
  CELDA 0.6|0.45 dif=+0.0049 IC=[-0.0054, +0.0127] -> NO_INFERIOR
NULOS SL n=50 media=0.6659 max=0.7955 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
NULOS T n=50 media=0.7598 max=0.8390 W=0.9465 iguales_o_mejores=0 p_sup=0.0196
NULOS Holm SL=0.0392 T=0.0392
HIPOTESIS H_SUPERA_R2 -> SIN_DECIDIR
HIPOTESIS H_CABLEADO_R2 -> SOSTENIDA
VEREDICTO_GLOBAL -> VALIDO | primaria=NO_INFERIOR
# conteo propio (brain-env)
corridas 600 gana 482 empata 2 pierde 116 min -0.0425 max 0.0295
nulos validos True 20 | radio SL crudo 347.3 a 735.5 (real 2032.3) | tipos T cambiados 390 a 432
versiones: 81 iguales, Linux-6.17.0-1022-azure-x86_64 numpy 2.5.3 pandas 3.0.5 scipy 1.18.1 pyarrow 25.0.1 torch 2.14.1+cpu
```

## Qué cambia respecto de lo anterior

- **Se corrige el +1,28 del factorial 2 (007).** Con 10 × 10 semillas queda +0,85; el factorial 2 sobreestimó con 3 × 5.
- **Antes R2 nunca se había medido contra barajados.** La ventaja grande del cableado real ahora está medida en R2, no sólo en M46 (factorial 1).

## Archivos

- **Rama titan:** `results/factorial3_2026-10-13/` (246 archivos: logs, json, versiones, `agregado.log`, `MD5SUMS.txt`), commit del bot `09ffbc1`.
- **main:**
  - este archivo;
  - `tools/contexto/actualizar_contexto_2026-10-13-010.py` (`5106b052…`);
  - `.github/workflows/contexto-2026-10-13-010.yml`.

## NO MEDIDO

- **Nulos en una sola celda y con una sola semilla de τ y de prueba.** No se sabe si la ventaja sobre los barajados se sostiene igual en las 6 celdas.
- **Los nulos se escalan al mismo radio espectral que el real.** El radio crudo de los SL (347 a 735) es mucho menor que el real (2032), así que la comparación es a radio normalizado, no a radio crudo.
- **El p de los nulos está en su piso** (1/51). Con más nulos bajaría; el tamaño del efecto (15 a 28 puntos) es lo informativo.
- **Variantes de R2 que no se midieron:** sin inhibición y con LIQ.
- **Lo de afuera de la simulación:** ninguna prueba fuera de simulación, ni otro conectoma que no sea FlyWire v783.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| Es el instrumento sellado | REPRODUCE_F2 exacto en 90 corridas y md5 de los scripts | Sí: cualquier cambio rompe la reproducción |
| Los nulos se comparan con lo mismo | REAL_IGUAL 0,9465 en los dos caminos | Sí |
| R2 no supera por el margen | IC90 hi +1,51 > +1 y lo +0,08 < +1 | Sí: con lo > +1 daba SUPERA |
| El cableado le gana a sus barajados | 0 de 100 nulos ≥ real, Holm 0,039 | Sí: con 2 o más nulos ≥ real por tipo, Holm pasaba 0,05 |

```
--- METODO PROMETEO ---
Accion delicada: no (lectura)
Maquina: Actions x64 (run 38420175126) | brain-env (verificacion y conteo)
Artefactos: docs/agents/respuestas/2026-10-13-010-factorial-3-r2-alcanza-a-su-regla-y-le-gana-a-sus-barajados.md + Doc de ClickUp 2026-10-13-010
```
