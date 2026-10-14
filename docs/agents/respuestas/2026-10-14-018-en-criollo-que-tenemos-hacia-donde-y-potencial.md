# 2026-10-14-018 · En criollo: qué tenemos, hacia dónde vamos y cuál es el potencial

**Pedido:** «En criollo qué tenemos entre manos, hacia dónde vamos, cuál es su potencial» (Abraham, 14-oct 17:32). Reemplaza a la síntesis 2026-10-13-011 con lo medido hoy.

## Veredicto primero
- [CONCLUSIÓN] **Tenemos un banco de pruebas, no un cerebro.** Le pregunta al cableado real de la mosca si sirve para un reflejo (escapar o aterrizar según lo que ve), contra dos rivales: sus barajados (las mismas piezas, conectadas al azar) y el plano de la mosca (la regla a mano: qué tipo de sensor va a qué comando), con los mismos sensores. Las reglas se escriben antes de mirar y todo se repite en dos máquinas.
- [MEDIDO] **El cableado real pesa, en las cuatro escalas.** M46, R1 (1.504 neuronas), R2 (33.489) y el cerebro entero (138.639) les ganan a sus barajados. En R2, por 19 a 28 puntos sobre su promedio; ninguno de 100 barajados lo iguala.
- [MEDIDO] **Contra el plano, empata.** R2 +0,85 puntos, sin pasar el margen de 1; el cerebro entero da lo mismo que R2 (la misma decisión en el 99,913 % de los ensayos). M46 y R1 quedan alrededor de un punto abajo.
- [MEDIDO, con letra chica] **Hoy lo superó por primera vez:** con las constantes de tiempo elegidas solo con el entrenamiento, +1,78 puntos, IC90 [+1,45; +2,13], en las 6 condiciones. El cableado tuvo una perilla y la regla ninguna: falta la prueba justa (H_TAU_JUSTO).
- [MEDIDO] **Lo que carga es el núcleo más las débiles.** Las conexiones fuertes (15 % de las aristas, el 57 % de las sinapsis) le ganan solas a sus barajados, pero pierden 4,59 puntos contra R2 entero. Las débiles ponen esa diferencia; si por cuáles son o por cuántas son lo decide H_DEBILES, listo para correr.
- [MEDIDO] **Salieron dos herramientas:** el banco sellado (nulos, regla rival, ancla, réplica) y Topo, donde el escape se escribe en 18 renglones y da exacto lo mismo que la regla (12 de 12).
- [NO MEDIDO] **Nada fuera de simulación.** El banco nunca vio un píxel: usa entradas sintéticas por tipo de neurona.

## Hacia dónde vamos
1. **Cerrar la ciencia del Paper 2:** H_DEBILES (64 trabajos, unas 3 h, espera el click), H_TAU_JUSTO (la regla con su propia perilla) y el nulo de BANC (la segunda mosca: el núcleo se conserva 77,0 % contra 32,7 % del resto, sin nulo todavía).
2. **Depositar el Paper 1 v2:** `--verificar` PASS en main; falta el token de Zenodo.
3. **Salir de la simulación:** cámara, puente de píxeles a los canales de la mosca, la pieza de choque (LC4 y LPLC2 a las descendentes) y vibración izquierda o derecha, contra un detector clásico de expansión (2026-10-13-020). Falta el puente de píxeles.

## Potencial, sin adornos
- **Ciencia (lo más firme):** un resultado de nicho y publicable por el método. La pregunta «el cableado contra el plano del animal con los mismos sensores» no la vimos hecha (búsqueda acotada, NO MEDIDO como revisión sistemática). Si el cableado sobrevive a la prueba justa, el titular es que supera a su plano; si no, que lo alcanza y que el plano es lo que se lleva a un robot. Las dos salidas son publicables.
- **Ingeniería:** para un robot conviene el plano, que rinde casi lo mismo y cuesta casi nada. Topo es la forma de escribir, probar y compilar esos planos: el producto barato que Abraham marcó («lo hecho a mano es una buena opción y barata»).
- **Aplicación:** el portero sensorial: una pieza chica entre el sensor y la IA que mira siempre, gasta casi nada y dispara el aviso de choque sin esperar a la IA. Prótesis solo como sustitución sensorial (cámara a vibración). Consumo y tamaño en un ESP32: NO MEDIDO.
- **Profesional:** te posiciona como ingeniero de evaluación de modelos y reproducibilidad (pre-registro, nulos, réplica entre máquinas). Los papers no pagan a corto plazo (2026-10-14-008).
- **Lo que no es:** no es un cerebro de mosca que aprende, ni una IA nueva, ni una neurona nueva (2026-10-13-005).

## Herramientas y máquina
Lectura del CONTEXTO vivo (md5 a41faa3d, bot 78d80bc) y de las respuestas 2026-10-12-011, 2026-10-13-005, 007, 010, 011, 013, 020 y 2026-10-14-001 a 017. Sin corridas nuevas. Acción delicada: ninguna.

## Evidencia (dónde está cada número)
| afirmación | fuente |
|---|---|
| cuatro escalas les ganan a sus barajados | 2026-10-13-002 (R1), 010 (R2), 2026-10-14-001 (cerebro entero), 015 de la tarea (M46) |
| R2 +0,85 contra la regla | factorial 3, bot `09ffbc1` |
| cerebro entero igual a R2, 99,913 % | factorial 4, 2026-10-14-001 |
| +1,78 con tau elegida | H_TAU, bot `2d4dbfb` |
| núcleo pierde 4,59; 88 % de la ventaja | núcleo, bot `a522bc4`; post hoc en 2026-10-14-015 |
| Topo 12 de 12 | 2026-10-14-011, `b34924d` |
| BANC 77,0 % contra 32,7 % | 2026-10-14-002 |
| v2 `--verificar` PASS | 2026-10-14-004 |

## NO MEDIDO
- H_DEBILES, H_TAU_JUSTO y el nulo de BANC.
- Cualquier cosa con píxeles, cámara, ESP32 o personas.
- La novedad frente a la literatura, como revisión sistemática.

## Antes de firmar
| afirmación | instrumento | ¿podía dar rojo? |
|---|---|---|
| el cableado les gana a sus barajados | 50 SL y 50 T por escala, Holm | sí; dio verde en las cuatro |
| empata con el plano | IC90 contra margen 1 punto, sellado | sí; dio NO_INFERIOR, no SUPERA |
| lo supera con tau elegida | H_TAU sellado | sí; dio SUPERA, con la letra chica de la perilla |
| el potencial | ninguno | no: es opinión, marcada como tal |

--- METODO PROMETEO ---
Inventario: lectura, sin corridas nuevas; brain-env sigue con los reales de H_DEBILES (en Actions ya dieron exacto, 2026-10-14-017). Contexto vivo: CONTEXTO md5 a41faa3d.
