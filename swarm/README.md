# swarm/ — Cerebro de Enjambre para Micro-Drones (Drosophila)

Primer sustrato neuromórfico generado con el **Substrate Architect Core Engine v3.1**.
Artefacto derivado de la línea embebida (SparseLTC/DualBrain), NO del paper de análisis.

## Qué es

Red líquida dispersa (SparseLTC) de **34 neuronas / 83 sinapsis** en **Q15 puro** para un
micro-drone (ESP32, sin FPU). Topología inspirada en la Drosophila, no entrenada: la
conducta está en el cableado y las constantes de tiempo, no en pesos aprendidos.

Ecuación: `h(t+1) = (1-τ)·h(t) + τ·tanh(Wᵀh(t) + s(t))`, τ uniforme = 0.119.

## Regiones (biología → función del drone)

| Región | Drosophila | Drone |
|---|---|---|
| LAMINA | retina | flujo óptico (4 dir) |
| ANTENNA | antenas | proximidad de vecinos (4 dir) |
| OCELLI / HALTERE | ocelos / halterios | rumbo / altitud |
| GIANT_FIBER | escape | huida rápida (GABA-first, P2) |
| LOBULA_WTA | decisión | maniobra ganadora (P2) |
| LAT_HORN | evasión innata | avoidance |
| FAN_BODY | cohesión | enjambre |
| PB | integración | memoria (P3, capacitor) |
| MOTOR | músculos | ESCs (4) |

## Archivos

- `swarm_drone.substrate.json` — blueprint (regiones + 83 conexiones + metadata + auditoría)
- `swarm_drone.h` — firmware C (Q15, sin float, sin globales, LUT tanh, struct encapsulado)
- `gen_swarm.py` — el generador (reproducible: pesos → radio espectral → Q15)
- `test_swarm.c` — validación (amenaza frontal + vecino izq → pitch atrás + roll der)

## Validación

`gcc -Wall -Wextra test_swarm.c` compila limpio. Estímulo frontal+izquierda →
`motores FL FR BL BR = -11k -9k +16k +17k` (retrocede y rola hacia el vecino). Correcto.

## Estado (honesto)

- **No está** flasheado en ESP32 real ni probado en hardware/drone real.
- La conducta de enjambre es rudimentaria (cohesión; sin alineación/separation ni protocolo inter-drone).
- 34 neuronas es escala de juguete frente a las 138.639 de la mosca.

## Regenerar

```bash
python3 gen_swarm.py   # regenera .json y .h
gcc -o test_swarm test_swarm.c && ./test_swarm
```
