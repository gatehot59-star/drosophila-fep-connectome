# 2026-10-11-010 · Escape a lazo cerrado: la mosca le gana a su shuffle en su función, pero paga la lateralidad; con τ fija ya escapa 180 de 180

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21157

**Instrumento:** rama `titan/escape-motivo-2026-10-11`. Pre-registro en `445646a` (script, reglas y humo sólo de controles); resultados en `4afb8f9` (`results/escape_motivo_2026-10-11/run.log`, md5 `666b90be13708e7ae0328eef6da05954`).

## 1. Pedido

Abraham apretó el botón «Correr la prueba de escape» que ofrecí en la 009: correr el motivo en su propia función (looming → escape), con el cableado barajado, la τ fija y la líquida en paralelo.

## 2. Herramientas y máquina

- **brain-env** (Celeron N4020, Python 3.12.14, numpy 2.5.3): lados de las 26 desde `annotations.tsv` pinneado; humo de controles; corrida completa desde un clon fresco de la rama (5,18 min); verificación por md5 de lo commiteado.
- **Sandbox de ClickUp:** escritura de `lados26.py` y `escape_motivo.py`.
- **GitHub MCP:** rama, dos commits a la rama y este commit a `main`.
- Actions y Kaggle sin uso; sin cuota ajena.

## 3. Veredicto

1. **En su propia función, la mosca le gana a su shuffle.** Acierto de lado 180/180 contra 0,5102 de media de S (7/200 shuffles en el 100%, p = 0,0398); supervivencia 180/180 contra 0,6605 (6/200, p = 0,0348).
2. **Lo que paga es la lateralidad, no el cableado fino.** Las 88 aristas del motivo son ipsilaterales (0 cruzadas). Un shuffle de grado exacto que conserva el lado (SL) empata: 0,9806 de acierto y 0,9983 de supervivencia, con 149/200 y 161/200 en el 100% (p = 0,7463 y 0,8060). El reflejo escrito a mano (C+) también saca 1,0/1,0.
3. **La neurona líquida no hace falta para esta función.** W saca 180/180 con τ fija heterogénea, τ fija uniforme 0,119, τ líquida, y con el brazo lineal en las tres; McNemar con 0 pares discordantes. Está en el techo: si la líquida ayuda en una versión más difícil, NO MEDIDO.
4. **Contra ruido congelado denso (B):** supervivencia W GANA (8/200, p = 0,0448); acierto W NO GANA (12/200, p = 0,0647).

## 4. Diseño (pre-registrado en el docstring de `escape_motivo.py`)

- **Sujeto:** el motivo de la 008 (`tools/brazo_s/motivo26.json`, md5 `eb6e53e0…`), ρ = 0,9, `z ← (1-τ)·z + τ·φ(W·z + x)`, φ = tanh o identidad.
- **Lados** (`lados26.py`, columna `side` de las anotaciones `17fc577`): izquierda 7 LC4, 2 LPLC2, 2 LC6, GF (DNp01) y 2 DNp09; derecha 1 LC4, 6 LPLC2, 2 LC6, GF y 2 DNp09.
- **Entrada** sólo en las 20 visuales: LC4 = dθ/(dθ + 0,02); LPLC2 y LC6 = θ/θ_col; por el ojo de su lado, d_der = (1 + sin az)/2; ruido 0,05 de un arreglo fijo, el mismo para todos los brazos.
- **Lectura fija:** c = z_GF_izq − z_GF_der. Lazo abierto: el signo de la suma hasta la llegada decide el lado. Lazo cerrado: el robot se corre 0,1 por paso con el signo de c si |c| > 1e-3.
- **Física:** objeto de radio 1 a d0 = 10 hacia la posición inicial del robot (radio 0,5), az0 en {±90, ±60, ±30}°, v en {0,2; 0,25; 1/3}, 10 repeticiones: 180 ensayos, T = 60.
- **Brazos:** W; S (`matriz_shuffle` de `brazo_s_recurrente.py` verbatim, k = 0..199); SL (`ms_shuffle` verbatim dentro de cada lado, pesos permutados por lado); B (normal densa, semilla 9000 + k). Todos a ρ = 0,9.
- **Controles:** C+ (cada visual al GF de su lado, peso 1/n del lado) y C0 (W = 0).
- **Reglas:** p empírico (1 + #{nulo ≥ W})/(K + 1), empates en contra de W, gana si p < 0,05; McNemar exacto para τ y no linealidad. Validez: C+ ≥ 0,95 / 0,90 y C0 = 0 / ≤ 0,05.

## 5. Resultados (verbatim de `run.log`)

```
LATERALIDAD aristas=88 ipsilaterales=88 cruzadas=0 GF_izq=20 GF_der=21 visuales_izq=11 visuales_der=9
CONTROL C+ acierto=1.0000 supervivencia=1.0000 lado_ok_cerrado=1.0000 latencia_mediana=2.0
CONTROL C0 acierto=0.0000 supervivencia=0.0000 lado_ok_cerrado=0.0000 latencia_mediana=-1.0
REFERENCIA politica=SIEMPRE_IZQ (ciega al lado, desde t=0) supervivencia=0.7222
CHEQUEO INSTRUMENTO VALIDO
SUJETO W variante=TANH+FIJA_HET acierto=1.0000 supervivencia=1.0000 lado_ok_cerrado=1.0000 latencia_mediana=1.0
SUJETO W variante=TANH+FIJA_UNI acierto=1.0000 supervivencia=1.0000 lado_ok_cerrado=1.0000 latencia_mediana=1.0
SUJETO W variante=TANH+LIQUIDA acierto=1.0000 supervivencia=1.0000 lado_ok_cerrado=1.0000 latencia_mediana=1.0
SUJETO W variante=LINEAL+FIJA_HET acierto=1.0000 supervivencia=1.0000 lado_ok_cerrado=1.0000 latencia_mediana=1.0
NULO S variante=TANH+FIJA_HET acierto_media=0.5102 acierto_p95=0.9508 superv_media=0.6605 superv_p95=0.9667
NULO S variante=TANH+LIQUIDA acierto_media=0.5020 acierto_p95=0.9444 superv_media=0.6405 superv_p95=0.8681
NULO SL variante=TANH+FIJA_HET acierto_media=0.9806 acierto_p95=1.0000 superv_media=0.9983 superv_p95=1.0000
NULO B variante=TANH+FIJA_HET acierto_media=0.4617 acierto_p95=1.0000 superv_media=0.5976 superv_p95=0.9892
CONTRASTE P1 W_acierto=1.0000 S_media=0.5102 S_max=1.0000 n_S>=W=7/200 p_emp=0.0398 -> W GANA
CONTRASTE P2 W_acierto=1.0000 SL_media=0.9806 SL_max=1.0000 n_SL>=W=149/200 p_emp=0.7463 -> W NO GANA
CONTRASTE P3_S W_supervivencia=1.0000 S_media=0.6605 S_max=1.0000 n_S>=W=6/200 p_emp=0.0348 -> W GANA
CONTRASTE P3_SL W_supervivencia=1.0000 SL_media=0.9983 SL_max=1.0000 n_SL>=W=161/200 p_emp=0.8060 -> W NO GANA
CONTRASTE P4_acierto W_acierto=1.0000 B_media=0.4617 B_max=1.0000 n_B>=W=12/200 p_emp=0.0647 -> W NO GANA
CONTRASTE P4_superv W_supervivencia=1.0000 B_media=0.5976 B_max=1.0000 n_B>=W=8/200 p_emp=0.0448 -> W GANA
CONTRASTE P5_liquida_supervivencia TANH+LIQUIDA=1.0000 TANH+FIJA_HET=1.0000 solo_A=0 solo_B=0 p_mcnemar=1.0000 -> TANH+LIQUIDA IGUAL
CONTRASTE P6_lineal_supervivencia LINEAL+FIJA_HET=1.0000 TANH+FIJA_HET=1.0000 solo_A=0 solo_B=0 p_mcnemar=1.0000 -> LINEAL+FIJA_HET IGUAL
VEREDICTO_FUNCION=LA MOSCA PAGA EN SU FUNCION: W GANA A S
VEREDICTO_DETALLE=EL CABLEADO FINO NO SE DISTINGUE DE SU SHUFFLE POR LADO
VEREDICTO_TAU=LA LIQUIDA NO SE DISTINGUE DE LA FIJA
VEREDICTO_LINEAL=EL LINEAL NO SE DISTINGUE DE TANH
escrito resultados.json md5=e3ce0eb262fae32605c1af4f009976e1
minutos=5.18
EXIT_RUN=0
```

El log completo tiene 63 líneas en la rama. `resultados.json` (533.509 B) queda en brain-env y se regenera con el comando del README.

## 6. Qué cambia en la hipótesis de agosto

| Parte | Antes (008) | Ahora |
|---|---|---|
| «El conocimiento está en el cableado» | sin señal funcional en tareas genéricas | sostenido en su función, acotado a la lateralidad; el detalle fino no se distingue de su shuffle por lado |
| «Funciona el primer día, sin entrenar» | diseño | sostenido en esta tarea: 180/180 sin un peso entrenado |
| «La neurona líquida es necesaria» | sólo en 1 de 4 tareas de memoria | no hace falta para escapar; si ayuda en algo más difícil, NO MEDIDO |

## 7. Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| La mosca le gana a S en su función | p empírico, 200 shuffles, empates en contra | sí: C0 0/0, S media 0,51 | PASS por poco (0,035 y 0,040) |
| Paga la lateralidad, no el cableado fino | W contra SL | sí, si SL caía | medido: SL empata |
| La líquida no hace falta para escapar | W con τ fija | sí, si la fija fallaba | PASS: 180/180 |
| La líquida no ayuda | McNemar líquida contra fija | no: las dos en el techo | NO MEDIDO |
| El lineal vale lo mismo que tanh | McNemar | no: techo | NO MEDIDO fuera de esta tarea |

Las reglas, la física y el modelo de entrada son míos y se fijaron antes de ver al sujeto: el humo corrió sólo los controles. La supervivencia discrimina poco (una política ciega al lado saca 0,7222); el acierto discrimina más.

## 8. Archivos generados

- En `titan/escape-motivo-2026-10-11`: `tools/escape_motivo/escape_motivo.py` (md5 `9720998291e3f08c6082e6c67d142759`), `lados26.py` (`e78241c452041ae6326ef8689b960f10`), `lados26.json` (`e5c19419d586850690ade3e8bbc5b315`), `lados26.log`, `humo_controles.log`, `README.md`, y `results/escape_motivo_2026-10-11/run.log` (`666b90be13708e7ae0328eef6da05954`). Clon fresco: 4/4 md5 idénticos a lo que corrió.
- En `main`: este archivo y `docs/agents/CONTEXTO-drosophila-fep.md`.

## 9. NO MEDIDO

- Una versión fuera del techo: amenazas más rápidas y frontales, más ruido y un estímulo que no sea looming, donde la exclusión LC6→GF podría importar. Es la única forma de separar τ fija de líquida, y W de SL, en esta función.
- La lectura por DNp09 y un readout entrenado sobre las descendentes.
- El GF-01 completo (864 nodos) en lugar del motivo de 26.
- Un S que conserve Dale: este motivo no tiene inhibición.
- El modelo de entrada es una simplificación de literatura, no una respuesta medida.
- Reproducción en una segunda máquina, hardware y review externo.

## 10. QA (TITAN FULL)

| Criterio | Puntaje | Evidencia |
|---|---|---|
| Completitud | 14/15 | Sujeto, tres nulos, dos controles, seis variantes. −1: sin readout entrenado ni segunda máquina |
| Ejecutabilidad | 15/15 | exit 0 desde clon fresco; md5 4/4; 5,18 min |
| Arquitectura del razonamiento | 9/10 | SL separa lateralidad de cableado fino. −1: la tarea quedó en el techo y no discrimina τ |
| Documentación | 9/10 | Docstring con reglas, README, log crudo. −1: `resultados.json` en brain-env |
| Innovación | 5/5 | Pre-registro con humo sólo de controles; nulo que conserva el lado |
| Proceso QA | 4/5 | Cada fila con su línea del log. −1: sin review externo |
| Seguridad, Testing, DevOps | N/A (40) | Sin frontera de confianza ni despliegue; los controles son la prueba |

**56/60 → 93/100 sobre lo aplicable.**
