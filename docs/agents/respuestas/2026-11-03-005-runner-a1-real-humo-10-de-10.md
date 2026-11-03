# 2026-11-03-005 · Runner 009-A1 real: 11/11 pruebas en numpy y en cython, el mismo manifiesto en las dos máquinas y humo 10/10 sobre la red completa

**Doc:** [Topo inverso](https://app.clickup.com/90171457413/docs/2kza6fw5-26157), página «2026-11-03-005 · Runner 009-A1 real».
**Evidencia:** `docs/agents/evidencia/2026-11-03-005-runner-a1-real/`.
**Código:** rama `titan/a1-runner-2026-11-03`, sin merge.

**Veredicto del pedido:** el runner quedó rehecho de verdad y probado.

- Corre Brian2 sobre la red completa de Shiu, con un proceso nuevo por ensayo.
- El manifiesto da 308/308 contra 009 y 010, y sale byte a byte igual en brain-env y en Actions.
- Las 11 pruebas pueden dar rojo, y pasan con numpy y con cython.
- El humo dio 10/10 ensayos OK, con SHAM igual a C0 en los tres pares.

**La corrida grande, de 8.540 ensayos, no se tocó y espera tu autorización.** La sección 15 sigue esperando que pegues el texto de 003.

## 1. Pedido

«ok» (3-nov 13:28) a la pregunta con la que cerró 004: «¿Rehago el runner de verdad antes de volver a disparar? Sería Brian2 por ensayo, el manifiesto comparado contra 010 y pruebas que puedan dar rojo.»

Lo leí así: rehacer el runner, probarlo en brain-env y volver a disparar solo el humo. La corrida grande no estaba en el pedido.

## 2. Herramientas declaradas

- **brain-env** (gateway python):
  - descargas de raw;
  - pruebas con Brian2 numpy en el venv;
  - el manifiesto real y el cotejo.

  Solo escribí en `/workspace/a1/v2`. La máquina tenía unos 1.048 MB libres, por otra carga que no es mía.
- **GitHub MCP**: este commit a `main`, lecturas de archivos y commits, y tres pushes a `titan/a1-runner-2026-11-03`:
  - `4c499296`, el runner;
  - `3faf0ac`, el workflow, que no dispara;
  - `dee4d670`, las huellas y el disparo.
- **API pública de Actions desde brain-env**: unos 4 pedidos para ver el estado del run y de sus pasos.
- **Actions**: run 41679588168, unos 2 minutos, en repo público y sin cuota.
- **ClickUp**: una página nueva en el Doc Topo inverso.

## 3. Qué se midió

Cada fila va así: afirmación, instrumento, si podía dar rojo, y veredicto.

| # | Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|---|
| 1 | Actions corrió exactamente los bytes probados en brain-env | `sha256sum --check tools/a1/HUELLAS.sha256` en el paso «intento»: 8/8 OK | Sí: un byte distinto da FAILED y el paso se cae | PASS |
| 2 | Las pruebas del runner pasan con los dos backends | `prueba_a1.py`: 11/11 PASS en brain-env con numpy y 11/11 PASS en Actions con cython | Sí, cada prueba tiene su caso rojo:<br>• T03, con un esperado falso, devuelve `['F1 QCOL']`.<br>• T04, con el signo invertido, da `[]`.<br>• T05, con un tick corrido, da distinto.<br>• T06, en el turno `start`, da distinto.<br>• T08, sin supresión, da 135 llegadas contra 100.<br>• T09 rechaza 9/9 recibos corruptos.<br>• T10 rechaza el manifiesto adulterado y el sha ajeno. | PASS |
| 3 | El manifiesto reproduce los valores publicados de 009 y 010 | `manifiesto_a1.py`:<br>• CHEQUEOS 308/308.<br>• 0 colisiones en 55.396 claves; la semilla máxima, 18446679777526156732, pasa de 32 bits.<br>• 22 sujetos, 40 grupos, 44 celdas y 8.540 ensayos. | Sí: T03 lo prueba con un esperado falso | PASS |
| 4 | El manifiesto se reproduce igual en otra máquina | sha256 `267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9` y 640.908 bytes en brain-env y en Actions, byte a byte (C1 del cotejo) | Sí: el control negativo con un dígito cambiado da DISTINTO | PASS |
| 5 | El fixture da las mismas espigas con numpy y con cython | 12/12 huellas iguales, numpy en brain-env y cython en Actions (C2) | Sí: el control negativo da DISTINTO en `F1\|B\|SHAM\|900` | PASS |
| 6 | El runner simula la red completa | Los recibos muestran:<br>• `CythonCodeObject`.<br>• 1,0 s simulado a dt 0,1 ms, con entre 2,1 y 4,4 s de reloj por simulación.<br>• RSS máximo de 3.252.900 kB por proceso (`/usr/bin/time -v`).<br>• Entre 428 y 33.992 espigas por ensayo. | Sí: un runner que no simula no da espigas ni ocupa memoria de red completa, y Q1 cambia la huella | PASS |
| 7 | SHAM es igual a C0 | Huellas de espigas iguales en 3/3 pares: R01 B s900, R01 B s901 y R01 A s900 (`validar_a1.py` y C4) | Sí: T09 rechaza `sham_distinto` | PASS |
| 8 | La entrada es la misma entre brazos | Una sola huella de entrada por (sujeto, régimen, semilla), en 4/4 grupos (C5 y validar) | Sí: T09 rechaza `entrada_desigual` | PASS |
| 9 | El productor valida sus recibos | `VALIDACION OK registros=10 esperados=10 fallos=0` | Sí: T09 | PASS; no reemplaza al verificador independiente |
| 10 | El manifiesto quedó commiteado antes de cualquier ensayo | Commit del bot `72835a5f` a las 16:59:16Z; el paso del humo arrancó a las 17:00:05Z (API de pasos) | Sí: con otro orden, el commit habría llegado después del humo | PASS |

### Lo que muestra el humo

No son decisiones: son dos semillas fuera del contrato, y no hay estimando.

| Ensayo | Espigas de x | Espigas de G | Espigas totales |
|---|---|---|---|
| R01 B C0 s900 | 30 | 54 | 5.154 |
| R01 B SHAM s900 | 30 | 54 | 5.154 |
| R01 B Q1 s900 | 0 | 54 | 5.274 |
| R01 B C0 s901 | 16 | 41 | 5.804 |
| R01 B SHAM s901 | 16 | 41 | 5.804 |
| R01 B Q1 s901 | 0 | 41 | 5.837 |
| R01 A C0 s900 | 87 | 95 | 33.992 |
| R01 A SHAM s900 | 87 | 95 | 33.992 |
| H2 C C_11 s900 | 41 | 0 y 0 | 436 |
| H2 C C_desplazado s900 | 43 | 0 y 0 | 428 |

Cortar la única fila 59804→30887 (Q1) apaga a x en las dos semillas, y las espigas totales suben un poco.

**Costo**: los 10 ensayos tardaron 22,66 s de pared con 3 procesos, entre 4,0 y 6,6 s cada uno. Extrapolando en línea recta, los 8.540 ensayos tardarían unas 5,4 h en un solo runner, cerca del tope de 6 h. Por eso la corrida grande conviene en matriz: 20 jobs de 427 ensayos, unos 16 minutos cada uno. Esto es una extrapolación, NO MEDIDO.

## 4. Evidencia cruda (verbatim)

Manifiesto en brain-env (`manifiesto_brainenv.log`):

```
CHEQUEOS 308/308
COLISIONES 0 claves=55396 distintas=55396 max=18446679777526156732 supera_32_bits=True
PLAN sujetos=22 grupos=40 celdas=44 ensayos=8540 humo=10
MANIFIESTO /workspace/a1/v2/manifiesto_a1.json bytes=640908 sha256=267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9 segundos=24.3
EXIT=0
```

Manifiesto en Actions (`results/a1_2026-11-03/prueba_1/manifiesto.log` en `737aafec`):

```
CHEQUEOS 308/308
COLISIONES 0 claves=55396 distintas=55396 max=18446679777526156732 supera_32_bits=True
PLAN sujetos=22 grupos=40 celdas=44 ensayos=8540 humo=10
MANIFIESTO results/a1_2026-11-03/prueba_1/manifiesto_a1.json bytes=640908 sha256=267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9 segundos=2.4
MANIFIESTO_IGUAL_A_BRAIN_ENV 267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9
```

Censo en Actions (`censo.log`):

```
PARITY {"connectome": "flywire", "equal": true, "expected": {"n_cab": 996, "n_pares_ffi": 880, "n_x": 1118, "t2": 698}, "values": {"n_cab": 996, "n_pares_ffi": 880, "n_x": 1118, "t2": 698}}
PARITY {"connectome": "banc", "equal": true, "expected": {"n_cab": 753, "n_pares_ffi": 622, "n_x": 716, "t2": 419}, "values": {"n_cab": 753, "n_pares_ffi": 622, "n_x": 716, "t2": 419}}
fa92fcd493162db96b7d185af4231c701bb30ec6a413ab913b401829d3a1e2df  /workspace/mecanismo-2026-11-02/flywire_units.npz
```

Últimas líneas de las pruebas: igual en `prueba_brainenv_numpy_2.log` (numpy) y en `prueba_cython.log` (Actions).

```
PRUEBA T11_manifiesto_real PASS chequeos 308/308, sujetos=22, grupos=40, ensayos=8540, colisiones=0, claves=55396
PRUEBA_A1 11/11 PASS
```

Humo en Actions (`humo.log`):

```
ENSAYO R01|B|Q1|900 estado=OK x=0 G=[54] total=5274 sha=d484fba46c4e48da seg=4.789 motivo=
ENSAYO R01|B|C0|900 estado=OK x=30 G=[54] total=5154 sha=fe00b8c895f58703 seg=5.787 motivo=
ENSAYO R01|B|SHAM|900 estado=OK x=30 G=[54] total=5154 sha=fe00b8c895f58703 seg=6.606 motivo=
ENSAYO R01|B|C0|901 estado=OK x=16 G=[41] total=5804 sha=ee2fa9806a0de8e0 seg=5.788 motivo=
ENSAYO R01|B|Q1|901 estado=OK x=0 G=[41] total=5837 sha=2779007df600df94 seg=4.419 motivo=
ENSAYO R01|B|SHAM|901 estado=OK x=16 G=[41] total=5804 sha=ee2fa9806a0de8e0 seg=6.578 motivo=
ENSAYO H2|C|C_11|900 estado=OK x=41 G=[0, 0] total=436 sha=39e101b93767e026 seg=4.133 motivo=
ENSAYO R01|A|C0|900 estado=OK x=87 G=[95] total=33992 sha=90e67662af09d758 seg=6.592 motivo=
ENSAYO R01|A|SHAM|900 estado=OK x=87 G=[95] total=33992 sha=90e67662af09d758 seg=6.422 motivo=
ENSAYO H2|C|C_desplazado|900 estado=OK x=43 G=[0, 0] total=428 sha=b6dd01ccadbf2dcd seg=3.971 motivo=
RUNNER 10/10 OK, 0 INVALIDO_TECNICO, target=cython, 22.5 s
	Percent of CPU this job got: 267%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:22.66
	Maximum resident set size (kbytes): 3252900
	Exit status: 0
```

Validación y estado en Actions:

```
VALIDACION OK registros=10 esperados=10 fallos=0
run=41679588168 dir=results/a1_2026-11-03/prueba_1 fuente=dee4d670557b3c5e6c6a5b4ab7d2f352b2a07754 job=success intento=success censo=success manifiesto=success fixtures=success humo=success validar=success
```

Cotejo en brain-env (`comparar_humo_a1.log`):

```
CHEQUEO C6_sha256sums IGUAL archivos=39 distintos=[]
CHEQUEO C1_manifiesto IGUAL actions=267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9/640908 brain_env=267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9/640908
CHEQUEO C2_fixture_numpy_vs_cython IGUAL ensayos numpy=12 cython=12 distintos=[]
CHEQUEO C3_recibos IGUAL n=10 estados=['OK'] codeobj=['CythonCodeObject'] manifiesto=['267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9'] commit=['dee4d670557b3c5e6c6a5b4ab7d2f352b2a07754']
CHEQUEO C4_sham_y_q1 IGUAL R01|A|900 SHAM==C0 True; R01|B|900 SHAM==C0 True; R01|B|900 Q1!=C0 True x_C0=30 x_Q1=0; R01|B|901 SHAM==C0 True; R01|B|901 Q1!=C0 True x_C0=16 x_Q1=0
CHEQUEO C5_entrada_pareada IGUAL H2|C|900 brazos=2 huellas_entrada=1; R01|A|900 brazos=2 huellas_entrada=1; R01|B|900 brazos=3 huellas_entrada=1; R01|B|901 brazos=3 huellas_entrada=1
RESULTADO 6/6 IGUAL
```

El control negativo, con las dos copias adulteradas, da `C1_manifiesto DISTINTO`, `C2_fixture_numpy_vs_cython DISTINTO ... distintos=['F1|B|SHAM|900']`, `RESULTADO 4/6 IGUAL` y `EXIT=1`.

## 5. Archivos

En este commit, en `main`:

- `docs/agents/respuestas/2026-11-03-005-runner-a1-real-humo-10-de-10.md`
- `docs/agents/evidencia/2026-11-03-005-runner-a1-real/`, con estos archivos:
  - `README.md`
  - `prueba_brainenv_numpy_1.log`
  - `prueba_brainenv_numpy_2.log`
  - `manifiesto_brainenv.log`
  - `comparar_humo_a1.py`
  - `comparar_humo_a1.log`
  - `comparar_humo_a1.exit`
  - `control_negativo_comparar.log`

En la rama `titan/a1-runner-2026-11-03`:

| Commit | Contenido |
|---|---|
| `4c499296` | `tools/a1/comun_a1.py`, `manifiesto_a1.py`, `runner_a1.py`, `validar_a1.py` y `prueba_a1.py` |
| `3faf0ac` | `.github/workflows/a1-prueba.yml` |
| `dee4d670` | `tools/a1/HUELLAS.sha256` y `tools/a1/PROBAR` |
| `72835a5f` y `737aafec` (bot) | `results/a1_2026-11-03/prueba_1/`: 39 archivos, entre ellos el manifiesto, los 10 recibos, el fixture en cython sin binarios y los logs |

No se commitean el manifiesto de brain-env, que es idéntico por sha256 al de la rama, ni los `.npz` y `.parquet` del fixture.

## 6. NO MEDIDO

- **La corrida grande**, 8.540 ensayos con semillas 0..19. No está autorizada y no corrió ningún ensayo del plan.
- **El verificador independiente del productor.** Es trabajo de otro agente (W-01). `validar_a1.py` es mi propio control.
- **Los estimandos y la estadística por familia** (t pareada unilateral, Holm, BCa). Ese código todavía no existe.
- **La equivalencia de mi rutina de entrada con PoissonInput sobre la red real.** Solo se probó en el fixture (T05).
- **La cobertura de las pruebas.** No hay herramienta de cobertura instalada.
- **Los CVEs de las dependencias fijadas, y el pin por hash de pip.**
- **Los núcleos reales del runner.** `nproc` dio 1 por `OMP_NUM_THREADS`; el 267 % de CPU muestra que usó al menos 3.
- **La duración de la corrida grande.** Es una extrapolación.
- **El aviso de Brian2 en T06** (`w` en el namespace). No cambia el resultado, porque Brian2 usa la variable interna, pero queda sin limpiar.
- **La sección 15 de la página maestra.** Sigue con las medias equivocadas hasta que pegues el texto de [2026-11-03-003](https://app.clickup.com/90171457413/docs/2kza6fw5-26157/2kza6fw5-29597). Las herramientas no pueden reescribir esa página.
- **El CONTEXTO**, que todavía no tiene este estado. Va en el próximo turno por el flujo del bot.

## QA (PROMETEO-QA)

| # | Criterio | Puntos | Score | Evidencia |
|---|---|---|---|---|
| 1 | Completitud | 15 | 14 | 5 módulos, workflow y huellas, sin placeholders (HUELLAS 8/8, prueba 11/11). −1: falta el código de estimandos y estadística de 010 |
| 2 | Ejecutabilidad | 15 | 15 | Corrió sin editar en las dos máquinas: brain-env, con los comandos del README, y el run 41679588168, con success en todos los pasos |
| 3 | Seguridad | 15 | 12 | `permissions: contents: write`; actions fijadas por SHA (checkout `11d5960a`, setup-python `a26af69b`); 9 entradas fijadas por sha256 y 8 archivos por HUELLAS; sin secretos. −2: pip fija versiones pero no hashes. −1: no revisé CVEs en vivo |
| 4 | Testing | 15 | 13 | 11 pruebas con su negativo propio, más el cotejo con control negativo (4/6, EXIT=1). −1: cobertura no medida. −1: la equivalencia con PoissonInput solo se probó en el fixture |
| 5 | Arquitectura | 10 | 9 | comun, manifiesto, runner, validar y prueba separados; el runner re-deriva el manifiesto antes de simular; un proceso por ensayo. −1: cada proceso lee el parquet dos veces, 3,25 GB por proceso |
| 6 | DevOps | 10 | 9 | Intento numerado con negativa a repetir; manifiesto commiteado a mitad del job; RESULTADO con el resultado real de cada paso (`737aafec`). −1: `nproc` sin `--all` |
| 7 | Documentación | 10 | 9 | README con comandos y máquinas, este archivo y el Doc. −1: el aviso de T06 sigue en el código |
| 8 | Innovación | 5 | 5 | Manifiesto comparado byte a byte entre máquinas dentro del workflow; huellas numpy contra cython; manifiesto commiteado antes de ensayar; humo fuera del contrato; cotejo con control negativo |
| 9 | Proceso QA | 5 | 5 | Cada score cita un archivo, un commit o un run |

**Total: 91/100.** Ningún punto quedó marcado N/A: hay workflow, así que DevOps y Seguridad aplican.

## Qué sigue

1. **Tu decisión**: autorizar la corrida grande, los 8.540 ensayos con semillas 0..19, como matriz de Actions y con el mismo manifiesto `267ca1d0…`. La escribiría como un workflow aparte que se niega a correr si el manifiesto difiere y que commitea los recibos de cada bloque.
2. **Antes de leer cualquier estimando**: commitear el código de la estadística de 010.
3. **Después**: que otro agente pase el verificador independiente sobre los recibos.
4. **Sección 15**: pegar el texto de 003.

--- METODO PROMETEO ---
Modo: FULL, porque toca un workflow de CI. Roles: implementación y QA.
Máquinas: brain-env (pruebas numpy, manifiesto y cotejo) y Actions ubuntu-24.04 (run 41679588168, cython).
Artefactos: este archivo y la página 2026-11-03-005 del Doc Topo inverso.
QA: 91/100 sobre 100 puntos aplicables, 0 N/A.
