# 2026-11-03-010 · Verificador independiente de 009-A1 escrito, probado y ensayado contra el productor en brain-env · limpio y global CONCORDANTE, sucio con las 19 corrupciones vistas · el sobre real sigue cerrado y sólo falta la autorización para abrirlo

**Veredicto del pedido** («no entiendo en qué das vueltas, continuá con nuestro trabajo», 3-nov-2026, 20:47 ART): seguí sin derivar el trabajo a otra instancia. El verificador que 010 §9 exige antes de leer decisiones ya está escrito. En brain-env, con el manifiesto real y los bytes bajados de la rama, pasó todo lo que la orden 009 §7 pide para abrir el sobre:

*   ensayo general **12 de 12**:
    *   limpio CONCORDANTE con 0 diferencias y salida idéntica en dos corridas;
    *   sucio con las 19 corrupciones vistas, ninguna celda de más y las 6 ciegas como `HUECO_DEL_CONTROL`;
    *   global con las 44 celdas invalidadas y cotejo CONCORDANTE;
*   pruebas propias **14 de 14**;
*   mutantes **10 de 10 muertos**, con el control 9 de 9.

Para ver resultados reales falta una sola cosa: la autorización escrita de Abraham para abrir el sobre.

**En criollo:** las 8.540 corridas están hechas y selladas. Ahora hay dos calculadoras escritas por separado, la del productor y este verificador, que en los ensayos dan los mismos números hasta el último decimal. Cuando Abraham escriba «autorizo abrir el sobre de 009-A1», corro las dos sobre los datos reales y comparo. Si coinciden, se leen los veredictos con la tabla de 007.

**Cambio de plan, declarado:** la orden 009 pedía que el verificador lo escribiera otro agente, no BRAIN. Lo escribí yo porque Abraham pidió seguir sin rodeos.
*   **Lo que sí da:** independencia del instrumento (W-01). No importa ni copia nada de `tools/a1/`, y usa otros motores: `scipy.stats.bootstrap` para el BCa, `scipy.stats.ttest_1samp` y una enumeración propia de los 2^20 signos.
*   **Lo que no da:** independencia de selección. Qué medir lo eligió el mismo autor del productor. Queda como deuda, y la orden 009 sigue vigente para una auditoría externa.

## Hallazgos

1. **El cotejo encontró una diferencia real en la primera corrida, y era del verificador.**
    *   **Qué pasó:** en el taller, con el manifiesto de prueba, K2 marcó 2 diferencias en `A|R07`, en `r_Q1` y `r_weak`: el productor publicaba `SIN_ESTIMADO` y el verificador `NULO`.
    *   **Causa:** el verificador aplicaba en A la letra de D8, que pide «denominador positivo y IC95». El productor sigue el anexo B: pone NULO por el IC95 y deja el denominador no positivo a D3, que lo marca SIN_ESTIMADO.
    *   **Efecto:** el mismo, porque el cociente queda sin publicar en los dos casos. Sólo cambia la etiqueta.
    *   **Qué se hizo:** se alineó el verificador al anexo B antes del push. Es `BUG_VERIFICADOR`, ya corregido, y la redacción de D8 queda anotada como imprecisa.
2. **El control del productor no mira la coherencia interna de los recibos, y eso puede mover veredictos.**
    *   **Qué se vio:** en el sucio, el verificador invalida 6 celdas más que el productor.
    *   **Cuáles:** `A|R12`, `A|R16`, `B|R15` y `C|H4` por coherencia, `B|H4b` por `runner_version` y `C|H2` por `input_hashes`.
    *   **Qué mueve:** con esa regla, P_T2_B pasa de `SOSTENIDA` a `INVALIDO_TECNICO`, y F_C de H2 y de H4 pasan a `INVALIDO_TECNICO`.
    *   **En el sobre real:** si aparece un hueco así, el cotejo lo clasifica y no lo esconde. Qué regla manda lo decide Abraham.
3. **La lectura de 010 deja dos puntos para decidir: D1 y D12.**
    *   Está en `lectura_010.md`.
    *   Ninguno cambia el cotejo, porque productor y verificador los aplican igual.
    *   D1 sí puede mover un p ajustado de F_B en el sobre real.

## Para abrir el sobre (orden 009 §8)

1. Verificador congelado en `titan/verificador-a1-independiente`, commit `5eaf35d08117a34bb37a325a1e4422ffb316b650`.
2. Fases E y T sobre `corrida_1`. Si algo falla, se para y se reporta.
3. Fase S del verificador, y se commitean su salida y su sha256 **antes** de correr el productor.
4. `estadistica_a1.py` (5c9492ff, sin cambios) con `--abrir-sobre`, y se commitea su `agregado_a1.json`.
5. Fase K y se commitea el cotejo.
6. Sólo si da `CONCORDANTE`, se leen los veredictos con la tabla de 007.

**Lo que hace falta de Abraham:** una línea en el chat, «Autorizo abrir el sobre de 009-A1». Sin esa línea no se lee ninguna cuenta del sobre real.

**Lo que ya se sabe que puede pasar:** si en el sobre real Q1 apaga a x en las 20 semillas, la regla del BCa degenerado de 010 §7, que queda tal cual, deja SIN_DECIDIR los criterios de cociente de T1, aunque el efecto sea máximo. Es una inferencia del humo, NO MEDIDA en el sobre.

## 1. Pedido

«no entiendo en que das vueltas, continua con nuestro trabajo» (3-nov-2026, 20:47 ART), después de la respuesta 009, que dejaba el verificador como orden para otra instancia. Se interpretó como: hacer el verificador acá, ensayarlo y dejar todo listo para abrir, sin abrir el sobre, porque abrirlo exige autorización escrita (orden 009 §2 y §8).

## 2. Herramientas

| Dónde | Qué | Para qué |
| --- | --- | --- |
| sandbox, sin red (Python 3.12.15, NumPy 2.4.6, SciPy 1.18.0) | redactar y probar contra un manifiesto de prueba y sus sobres | desarrollo; no es evidencia |
| GitHub | rama `titan/verificador-a1-independiente` desde `main` `d614fea3`; commit `5eaf35d08117a34bb37a325a1e4422ffb316b650` | código |
| brain-env por MUDH Gateway/build (host `6c09d8604b07`, Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1, 4 CPU, 939 MB libres) | bajar los bytes de raw, verificarlos, correr ensayo, pruebas y mutantes | **medición** |

## 3. Qué se midió

Cada afirmación, con el instrumento que la mide, si ese instrumento podía dar rojo y el veredicto.

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
| --- | --- | --- | --- |
| Los bytes que corrieron son los de la rama | sha256 de los 5 archivos bajados de raw en `5eaf35d0` contra el taller | sí, un byte distinto cambia el sha | **PASS**, 5 de 5 iguales |
| El manifiesto es el del pin | sha256 en brain-env | sí | **PASS**, `267ca1d0…` |
| Los sobres sintéticos y los agregados del productor son los del anexo C | sha256 de `SHA256SUMS.txt` y `agregado_a1.json` | sí, el taller con manifiesto de prueba dio DISTINTO en los 3 | **PASS**, 6 de 6 iguales |
| La fase E reconstruye el plan de 010 | conteo y registro propios | sí | **PASS**: 44 celdas, 427 condiciones, 8.540 ensayos y registro `7c6dadc1…`, el mismo del productor |
| limpio: 0 fallas técnicas y cotejo sin diferencias | ensayo, chequeos 2 y 3 | sí, en el taller la primera versión dio 2 diferencias | **PASS**: 0 fallas, K1 0, K2 0 |
| La fase S es determinista | sha de `verificador_a1.json` en dos corridas | sí | **PASS**, `b6561ada…` las dos veces |
| sucio: ve las 19 corrupciones y ninguna de más | ensayo contra `SEMBRADO.json` | sí | **PASS**: 19 celdas, faltan 0, sobran 0 |
| sucio: las 6 ciegas son `HUECO_DEL_CONTROL` | K1 | sí | **PASS**: `A|R12`, `A|R16`, `B|H4b`, `B|R15`, `C|H2`, `C|H4` |
| sucio: los motores coinciden con el productor | K2 espejo, con las celdas inválidas del productor | sí, cualquier intervalo fuera de 1e-9 relativo o p fuera de 1e-12 | **PASS**: 0 diferencias |
| global: una línea ilegible invalida las 44 | fase T y K | sí | **PASS**: `ILEGIBLE` en `bloque_07.jsonl:441`, 44 inválidas, CONCORDANTE |
| Las pruebas propias pasan | `prueba_verificador_a1.py` | sí, cada una afirma un valor exacto | **PASS**, 14 de 14 |
| Las pruebas detectan errores plantados | `mutantes_verificador_a1.py`, con control | sí, un mutante vivo cuenta como rojo | **PASS**, 10 de 10 muertos y control 9 de 9 |
| El verificador no abre el sobre real sin permiso | V12 | sí | **PASS**: con `corrida_` sale con 2 y sin escribir nada; con un recibo no sintético, NEGADO |

## 4. Evidencia cruda

Todo está verbatim en `docs/agents/evidencia/2026-11-03-010-verificador-a1/`. Los logs son copia byte a byte de brain-env y sus sha256 están en el README de esa carpeta. Lo central:

```plain
verificador codigo/tools/verificador_a1/verificador_a1.py sha256 a7b553f7d456920f76b7f8e9da2459437439c523381908fce923676a1947abd0
PASS limpio: huellas del anexo C | SHA256SUMS 1210454551352718 IGUAL | agregado bf8e90b867af195b IGUAL
PASS limpio: 0 fallas tecnicas | fallas 0
PASS limpio: cotejo CONCORDANTE sin diferencias | CONCORDANTE | K1 0 | K2 0
PASS limpio: fase S identica en dos corridas | b6561ada6611f414 / b6561ada6611f414
PASS sucio: huellas del anexo C | SHA256SUMS 4546466dd7b1d742 IGUAL | agregado c050a9ebba767b48 IGUAL
PASS sucio: las 19 corrupciones vistas | faltan []
PASS sucio: ninguna celda invalidada de mas | sobran []
PASS sucio: las 6 ciegas como HUECO_DEL_CONTROL | K1 ['A|R12', 'A|R16', 'B|H4b', 'B|R15', 'C|H2', 'C|H4']
PASS sucio: espejo sin diferencias y cotejo CONCORDANTE | CONCORDANTE | K2 0 | K3 167 derivadas de invalidas
PASS global: huellas del anexo C | SHA256SUMS 76c6a87a237241f2 IGUAL | agregado b873a1cbc95d716e IGUAL
PASS global: falla sin celda que invalida las 44 | [('ILEGIBLE', 'bloque_07.jsonl:441')] | invalidas 44
PASS global: cotejo CONCORDANTE | CONCORDANTE | K1 0 | K2 0
RESUMEN 12/12 PASS
exit 0
```

```plain
verificador bajo prueba codigo/tools/verificador_a1/verificador_a1.py sha256 a7b553f7d456920f76b7f8e9da2459437439c523381908fce923676a1947abd0
V01 PASS (0.0 s) huella([3,1,2]) = sha256("[1,2,3]\n")
V02 PASS (2.4 s) cerrados 3/3 y fuerza bruta 3/3
V03 PASS (0.0 s) ejemplo a mano y centinela p_familia = 1
V04 PASS (0.4 s) 6 intervalos con empates: flujo, distribucion e IC literal iguales a scipy
V05 PASS (0.0 s) constante y r = 1 exacto: DEGENERADO, sin IC
V06 PASS (0.0 s) SIN_ESTIMADO e INDEFINIDO
V07 PASS (41.5 s) 702 ids sin cambio con B|R07 invalida
V08 PASS (0.0 s) registro 7c6dadc180b56d1d0c2be39782e948c3b7f73b994294412a345b8d011691c40a
V09 PASS (0.0 s) 8.540 recibos, 0 fallas
V10 PASS (3.5 s) 13 recibos corruptos: 15 pares exactos en 13 celdas
V11 PASS (9.8 s) invalidan las 44: CODE_COMMIT_MIXTO, INTEGRIDAD, ILEGIBLE
V12 PASS (1.8 s) corrida_ sin --abrir-sobre: rc 2 sin salida; recibo no sintetico: NEGADO
V13 PASS (0.1 s) auto-cotejo 0 y una perturbacion de 1e-6 detectada en A|R01|COL_cortado
V14 PASS (0.0 s) CONCORDANTE contra el agregado del productor
RESUMEN 14/14 PASS
exit 0
```

```plain
CONTROL rc 0 RESUMEN 9/9 PASS
M01 MUERTO (V10) T7 sin el chequeo de cuenta_x | V10 FAIL (3.3 s) AssertionError: sobran []; faltan [('COHERENCIA', 'B|R07')]
M02 MUERTO (V03) Holm cambiado por Bonferroni | V03 FAIL (0.0 s) AssertionError: holm [0.04, 0.16, 0.12, 0.02], esperado [0.03, 0.06, 0.06, 0.02]
M03 MUERTO (V02) inversion de signos con la tolerancia al reves | V02 FAIL (0.0 s) AssertionError: unos: 0.0
M04 MUERTO (V07) D4: no consume el bloque de las celdas invalidas | V07 FAIL (44.2 s) AssertionError: cambian 167 ids, por ejemplo ['B|R08|COL_interaccion', 'B|R08|DQ1', 'B|R08|DQ1uQCOL']
M05 MUERTO (V06) D3 sin INDEFINIDO | V06 FAIL (0.0 s) AssertionError: {'tipo': 'cociente', 'numerador': 1.0, 'denominador': 0.525, 'estimado': 1.9047619047619047, 'ic95': [0.6451612903225806, 1.904
M06 MUERTO (V11) una falla sin celda ya no invalida las 44 | V11 FAIL (4.2 s) AssertionError: ('commit', 0)
M07 MUERTO (V05,V14) la trampa del BCa degenerado arreglada en vez de reproducida | V05 FAIL (0.0 s) AssertionError: {'tipo': 'media', 'estimado': 3.0, 'ic95': None, 'estado_ic': 'MOTOR_INCONSISTENTE', 'motivo': 'scipy devolvio un limite no fin
M08 MUERTO (V10) T5 sin el chequeo de SHAM contra C0 | V10 FAIL (3.7 s) AssertionError: sobran []; faltan [('SHAM_DISTINTO_DE_C0', 'A|R08')]
M09 MUERTO (V14) activacion con drivers a 1 Hz en vez de 10 | V14 FAIL (30.8 s) AssertionError: (21, [{'donde': 'casos/B|R06', 'campo': 'estado', 'productor': 'NO_INFORMATIVO_EN_B', 'verificador': 'ACTIVADO', 'regla': 'dis
M10 MUERTO (V04,V14) z0 sin la mitad de los empates | V04 FAIL (0.2 s) AssertionError: chequeos del motor: {'bca_literal_distinto': 6}
RESUMEN 10/10 MUERTOS
exit 0
```

## 5. Archivos

**Código**, en la rama `titan/verificador-a1-independiente`, commit `5eaf35d08117a34bb37a325a1e4422ffb316b650`, carpeta `tools/verificador_a1/`:

| Archivo | Bytes | SHA-256 |
| --- | --- | --- |
| `verificador_a1.py` | 65.252 | `a7b553f7d456920f76b7f8e9da2459437439c523381908fce923676a1947abd0` |
| `prueba_verificador_a1.py` | 17.291 | `5a569c04e06dd56f3a2c3ba562aae0254fbce03583cb14cb17538f658efbb10c` |
| `mutantes_verificador_a1.py` | 4.621 | `bdef3f8b19105a221bd9e7f79a74bd996427a50bbe5758c7896999f10fb354b5` |
| `ensayo_verificador_a1.py` | 7.844 | `8bb8be83d9e8616bf8b2e07b897868bbedb369eb84a38d9b9f39fe3478afe9f6` |
| `README.md` | 3.212 | `bb89869e09c22110b6c5ec5cb68cd57b5bd4110aa6cf16fbfa7665eb4e12799c` |

**Bitácora y evidencia**, en `main`:
*   esta respuesta: `docs/agents/respuestas/2026-11-03-010-verificador-independiente-escrito-y-ensayado.md`;
*   `docs/agents/evidencia/2026-11-03-010-verificador-a1/`: logs de descarga, ensayo (los cuatro escenarios), pruebas y mutantes, más `ensayo_resumen.json`, `lectura_010.md` y un README con sha256.

**Salidas que quedan en brain-env** (`/workspace/a1/v2/evid10/ensayo/`), con sus sha256:

| Escenario | `verificacion_tecnica.json` | `verificador_a1.json` | `cotejo_a1.json` |
| --- | --- | --- | --- |
| limpio | `f4767078cf62d4abfba2282e240c942022567b24cf1135b4be5a3bef11814aa7` | `b6561ada6611f4144c6896c7710e83e019125cd56444884aed5a4aced8120484` | `91bbaeacd012a47568b302a5eb2243f0e468a38aaaff70c899ffab93f37b261f` |
| sucio | `ee7781a08fef24e43dbf656b88a76077a17a7d66ea78b0c24ffa4e7933b8a577` | `83abee6f4b508b7a8d118de0066cad7982c05fd1b44018bb55a613cd0f494140` | `88e8d3a718c561bc9071dd07669026dd07acbb0b351a6ed60bb3765e6f80bf1f` |
| global | `c027c00da2e39ba2ae4c77e583a0077faa7cefbfbd7ba953fa0a0f2bc0f83ae7` | `5a6fe4bc6d61c967235b771dcc1dd5615fb4be7d0bcaa51662b8895207dd0b95` | `710de1338e722ced0c5095aeaba33d79fca5d2bc2609dc345dadaafb51b9ae88` |

En el sucio también queda `verificador_a1_espejo.json`, con sha256 `c1939943632514e32a89c6746f13157f54f5e74dced84184ee80646bdd6e2f08`.

## 6. NO MEDIDO

*   **El sobre real:** nada de `corrida_1` se leyó. No hay ningún estimando real.
*   **Independencia de selección:** el verificador y el productor los eligió el mismo autor. Un error de lectura de 010 que los dos compartan no lo ve este cotejo. Para eso sigue la orden 009.
*   **El cotejo opcional con la evidencia de 010** (`d5d9b7ba…`, instrumento de Astra) sobre tamaños y huellas de D′ no se hizo.
*   **Revisión automática del diff** (K-01): no se pidió. Queda como deuda, y no es una aprobación.
*   **Los tiempos de brain-env no son comparables con otra máquina:** la fase S tardó 22 a 24 s en limpio, con 939 MB libres y 10 GB de swap ocupados por otros procesos.
*   **`entorno uniforme False` en el sucio:** es informativo. Lo causa algún recibo corrupto, no se buscó cuál y no invalida nada.
*   **Que la trampa del BCa degenerado aparezca en el sobre real:** sigue siendo una inferencia.

## QA (PROMETEO-QA, tipo «script o instrumento»)

| Criterio | Puntaje | Evidencia |
| --- | --- | --- |
| Completitud | 14/15 | Fases E, T, S y K, pruebas, mutantes, ensayo y `lectura_010.md`. Falta el cotejo opcional con la evidencia de 010 (−1). |
| Ejecutabilidad | 15/15 | Corrió en brain-env sobre los bytes de la rama, con exit codes en los logs. |
| Documentación | 9/10 | README, docstrings, esta respuesta y su Doc. La redacción de D8 quedó imprecisa en la orden y no se corrigió allá (−1). |
| Proceso QA | 5/5 | Pruebas 14/14, mutantes 10/10, ensayo 12/12 y sha de los bytes verificado. |
| **Total** | **43/45 → 96/100** | N/A: Seguridad, Testing como criterio aparte, Arquitectura, DevOps e Innovación (55 puntos), por tipo de entrega. |

Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29737

```plain
--- METODO PROMETEO ---
Accion delicada: NO (codigo en rama titan sin merge; bitacora y evidencia en main)
Modo aplicado:   FULL
Maquina:         brain-env (medicion); sandbox solo para redactar
Rubrica:         43/45 -> 96/100
N/A declarados:  55 (Seguridad, Testing aparte, Arquitectura, DevOps, Innovacion: no aplican a un instrumento)
Review externo:  no pedido (deuda K-01); independencia de seleccion: deuda W-01, orden 009 vigente
Instrumento:     BRAIN en brain-env: ensayo_verificador_a1.py (exit 0, 12/12),
                 prueba_verificador_a1.py (exit 0, 14/14), mutantes_verificador_a1.py (exit 0, 10/10);
                 evidencia cruda en docs/agents/evidencia/2026-11-03-010-verificador-a1/
Artefactos:      docs/agents/respuestas/2026-11-03-010-verificador-independiente-escrito-y-ensayado.md + https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29737
```
