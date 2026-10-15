# 2026-10-14-033 · El instrumento de H_RIVAL está listo y pasó el humo ciego en las dos máquinas: el ridge nuevo reproduce exacto el 0,9935 de la 015 y los rivales ven los mismos ensayos que la mosca

## Pedido
Abraham, 15-oct 01:28, ClickKit `instrumento_rival_034`: «Escribí el instrumento de H_RIVAL».

## Veredicto primero
- [HECHO] **El instrumento está commiteado después del sello y se ejecutó antes de subirlo** (`04d0635`; el sello `05a574c` queda como el commit anterior, con un solo archivo). Son tres scripts y dos workflows: `rival_mosca.py`, `agregar_rival.py`, `prueba_rival.py`, `rival-humo` y `rival-mosca`. Lo que está en git es byte a byte lo que corrió en brain-env (mismo md5).
- [MEDIDO] **El control positivo que pediste pasa exacto.** El ridge nuevo, con el protocolo de la 015, da 0,9935, 0,9595, 0,9935, 0,9575, 0,9940 y 0,9590 en las seis celdas, lo mismo que `completa.log`, y 0 predicciones distintas del ridge original de `ept`, en brain-env y en Actions. El rival no está roto.
- [MEDIDO] **Los rivales van a ver exactamente lo que vio la mosca.** En las 6 celdas, la regla recalculada sobre los ensayos regenerados da las mismas predicciones que la guardada (20 de 20 semillas por celda), y el acierto de W recalculado desde sus predicciones da lo guardado (110 de 110 por celda). La comparación queda pareada ensayo por ensayo.
- [MEDIDO] **Los demás controles pasan en las 6 celdas:**
  - el integrador nulo da la regla sin cambios (2.000 de 2.000);
  - el ridge con etiquetas permutadas cae al azar (0,5000 contra 0,5000);
  - los pines (módulos, conectoma, 6 json de H_TAU, 60 json del factorial 3, `completa.log`);
  - la guarda de fuga;
  - las rutas de los tres rivales con 10 candidatas cada uno, sin imprimir aciertos.
- [MEDIDO] **Prueba 18/18**, con un chequeo hecho para dar rojo a propósito (el ridge con el lambda al doble se nota contra `ept._ridge_fit`).
- [HUMO] **Actions** (run 38684660391, bot `b964058`): 8 de 8 trabajos bien y las 6 celdas VALIDO. **brain-env**: c0 VALIDO y CONTROL_RIDGE_015 6/6, con las mismas líneas de control que Actions.
- [DESVÍO DECLARADO] **El MLP no es `ept.mlp_mux` llamado tal cual.** `ept.mlp_mux` trae fijas las clases de la 005 (en vuelo 0 a 3, posada 0 a 2), que no son las de esta tarea (en vuelo 0, 2, 3 y 4; posada 0 y 1): llamada directa, se rompe. El MLP es su bucle línea por línea, con los mismos hiperparámetros y las clases de `tm.CLASES`. CONTROL_MLP_005 lo compara con `ept.mlp_mux` sobre etiquetas pasadas a las clases de la 005: 480 de 480 predicciones idénticas en las dos máquinas.
- [NO MEDIDO] **Ningún acierto de rival**: el humo es ciego. La corrida completa espera el `CORRER` de Abraham.
- [COSTO] Actions tarda unos 10 minutos por celda (cada MLP de 300 iteraciones, unos 4 s), y las 6 celdas corren en paralelo. La réplica en brain-env tarda unas 9 horas (cada MLP, unos 45 s en un núcleo; c0 del humo, 688 s contra 83 s en Actions).

## Herramientas y máquina
- **brain-env.** Python 3.12.14, numpy 2.5.3, torch 2.14.1, 2 núcleos, 7,8 GB. Clon de `titan/rival-2026-10-15`. Prueba, humo de CONTROL_RIDGE_015 (141 s) y humo de c0 (688 s), con nohup.
- **Actions x64.** Python 3.12.15, numpy 2.5.3, torch 2.14.1+cpu. Humo en 8 trabajos de entre 1 y 2,5 minutos.
- **GitHub.** Push del instrumento y del disparo del humo; md5 verificado desde un clon limpio.
- Acción delicada: ninguna. No hubo corrida completa.

## Archivos
| Archivo | md5 |
|---|---|
| `tools/rival/rival_mosca.py` (`04d0635`) | 774232f5b4a53872a05f6a0f06015f34 |
| `tools/rival/agregar_rival.py` | f66b22508dd44a9394ef0c8dc262e9a8 |
| `tools/rival/prueba_rival.py` | b7b9d4116cd7af8fb49cd364b0b78344 |
| `.github/workflows/rival-humo.yml` | fdbfd7230b1423b78cf864b2da6b8370 |
| `.github/workflows/rival-mosca.yml` | cc1b2bd12f2e9bb67d0fffefa86e9f0a |
| `results/rival_2026-10-15_humo/brainenv/humo_r015.log` (`1d4efcf`) | 3f103a8992200725c2a89db849031796 |
| `results/rival_2026-10-15_humo/brainenv/humo_c0.log` | 980b89ed7114025681e1dab35e0eddb0 |
| `results/rival_2026-10-15_humo/actions/MD5SUMS.txt` (bot `b964058`) | 6d9691092d6efbbd8c44df57a2e2a9aa |
| `tools/contexto/actualizar_contexto_2026-10-14-033.py` (main, este commit) | 6c9fa4e21dbfa75ef00822c13876aebb |
| CONTEXTO antes y después del parche (probado en copia) | d0aad9b066a34d31aa4de921fda14034 y 36480f72e75a1ae412b24ea1818735bd |

Doc de ClickUp: [033](https://app.clickup.com/90171457413/docs/2kza6fw5-22857).

## NO MEDIDO
- Los aciertos de los tres rivales, D, sus IC y los veredictos de H_RIVAL y H_TAU_JUSTO.
- La réplica completa en brain-env y el cotejo entre máquinas.
- La regla con ganancia o umbral por tipo, y W con 30 semillas de τ.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El ridge nuevo es el de la 015 | CONTROL_RIDGE_015 contra `completa.log`, más la comparación con `ept.ridge` | Sí: tolerancia de 2 ensayos por celda; dio 0 |
| Los rivales ven los mismos ensayos que W | REPRO_REGLA y REPRO_W, cadena por cadena | Sí: una semilla o un ruido distinto cambia las predicciones |
| El MLP es el de la 005 | CONTROL_MLP_005 contra `ept.mlp_mux` | Sí: un hiperparámetro o un orden distinto cambia predicciones |
| La prueba puede fallar | ROJO_A_PROPOSITO | Sí, y tiene que dar la diferencia; la dio |
| El humo no miró aciertos | el código no imprime ni guarda aciertos de rivales con `--humo` | Sí: se ve en los logs |
| Lo commiteado es lo probado | md5 desde un clon limpio | Sí |

--- METODO PROMETEO ---
Escribir el instrumento después del sello y ejecutarlo antes de commitear. Controles que pueden dar rojo, uno a propósito. Humo ciego en las dos máquinas. Declarar el desvío del MLP. No disparar la corrida completa sin el sí de Abraham.
Máquina: brain-env y Actions x64. Artefactos: este archivo en main y su Doc en ClickUp.
