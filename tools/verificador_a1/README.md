# Verificador independiente de 009-A1

Responde a 010 §9 («datos por semilla → verificador distinto del productor → decisiones por familia») y a la orden `docs/agents/ordenes/2026-11-03-009-verificador-independiente-a1.md`.

## Quién lo escribió y qué independencia da

Lo escribió BRAIN el 3-nov-2026, después de que Abraham pidiera seguir sin derivar el trabajo («continuá con nuestro trabajo», 20:47 ART). La orden 009 pedía otro agente; esto lo cambia y lo declara.

*   **Independencia de ejecución (W-01): sí.** No importa ni copia nada de `tools/a1/`. Usa otros motores: `scipy.stats.bootstrap` para el BCa, `scipy.stats.ttest_1samp` para el t y una enumeración propia de los 2^20 signos. Las listas de condiciones, cantidades y familias salen de 010 y de los anexos A y B de la orden, no de `plan_a1`.
*   **Independencia de selección: no.** Qué medir lo eligió el mismo autor del productor. Queda como deuda, y la orden 009 sigue vigente para que otro agente la ejecute como auditoría.

## Archivos

| Archivo | Qué hace |
| --- | --- |
| `verificador_a1.py` | Fases E (manifiesto y plan), T (recibos, sin estimandos), S (estadística de 010 §7) y K (cotejo con el agregado del productor) |
| `prueba_verificador_a1.py` | 14 pruebas, con 13 recibos corruptos propios, distintos de los del kit |
| `mutantes_verificador_a1.py` | 10 mutantes, cada uno con la prueba que lo tiene que matar |
| `ensayo_verificador_a1.py` | Ensayo general contra el productor en los tres sobres sintéticos (orden 009 §7) |

Sólo stdlib, numpy y scipy. Probado con Python 3.12.14, NumPy 2.5.3 y SciPy 1.18.1 (brain-env).

## Seguridad del sobre real

*   Con una ruta que contenga `corrida_`, las fases T, S y K no corren sin `--abrir-sobre`.
*   Con recibos sin `"sintetico": true`, la fase T se niega antes de leer cuentas.
*   Ninguna fase imprime cuentas. Los veredictos sólo salen por pantalla si todos los recibos son sintéticos.

## Cómo se abre el sobre real (orden 009 §8), sólo con autorización escrita de Abraham

1. Congelar este verificador en un commit y anotar el SHA.
2. `python3 verificador_a1.py --manifiesto M --sha-manifiesto 267ca1d0… --sobre corrida_1 --salida V --fases ETS --abrir-sobre`
3. Commitear `verificacion_tecnica.json`, `verificador_a1.json` y sus sha256 **antes** de correr el productor.
4. Correr `estadistica_a1.py` (5c9492ff) con `--abrir-sobre` y commitear su `agregado_a1.json`.
5. `python3 verificador_a1.py … --salida V --fases ETK --agregado-productor agregado_a1.json --abrir-sobre`. Usa el `verificador_a1.json` ya commiteado.
6. Sólo si el cotejo da `CONCORDANTE`, Abraham lee los veredictos con la tabla de 007.

## Cómo clasifica el cotejo

*   **K1:** celdas inválidas. Las que invalida sólo el verificador son `HUECO_DEL_CONTROL`, con sus códigos. Las que invalida sólo el productor quedan `SIN_CLASIFICAR`.
*   **K2 espejo:** la fase S del verificador con las celdas inválidas del productor. Aísla los motores, y cualquier diferencia queda `SIN_CLASIFICAR`.
*   **K3 propio:** la fase S con la regla propia. Si K2 da 0, sus diferencias son `DERIVADA_DE_INVALIDAS`.
*   **Resultado:** `CONCORDANTE` si nada queda sin clasificar.
