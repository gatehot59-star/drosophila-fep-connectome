# Orden 2026-11-03-009 · Verificador independiente de 009-A1: escribirlo sin el código del productor, ensayarlo contra el productor en un sobre sintético y esperar la autorización para abrir el real

**Emite:** BRAIN, 3-nov-2026, a pedido de Abraham («Dejá 010 tal cual y prepará el verificador independiente», 18:36 ART).

**Estado al emitir:** el sobre real de 009-A1 (8.540 ensayos en `results/a1_2026-11-03/corrida_1/`) sigue cerrado. Nadie calculó un estimando sobre él. 010 queda tal cual, sin enmienda: la regla del BCa degenerado de 010 §7 sigue vigente (ver §9).

## 0. Qué se pide, en una línea

Escribí un verificador propio de 009-A1 que no use código del productor. Probalo con recibos corruptos y contra el productor sobre un sobre sintético con la estructura del manifiesto real. Dejalo commiteado con evidencia cruda y esperá la autorización escrita de Abraham para correrlo sobre el sobre real.

## 1. Quién ejecuta, quién no y quién decide

*   **Ejecuta:** un agente que no sea BRAIN. Puede ser Astra, Argon u otra instancia nueva, por ejemplo con ASTRA-AUDITOR-CORPUS u OPUS-AUDITOR-CORPUS.
*   **No ejecuta: BRAIN.** BRAIN escribió el runner, el control (`validar_a1.py`) y la estadística (`estadistica_a1.py`). El docstring de `validar_a1.py` lo dice desde 005: el verificador distinto del productor que pide 010 §9 lo escribe otro agente. La razón es W-01: un instrumento propio sirve para ejecutar, pero elegir qué medir lo tiene que hacer alguien que no escribió el código.
*   **Decide: Abraham.** El verificador mide y coteja. No lee veredictos científicos, no autoriza la apertura y no mergea.

## 2. Prohibiciones y reglas de parada

1. **No abras el sobre real sin autorización escrita de Abraham en el chat.** Abrir es cualquiera de estas cosas sobre un recibo de `corrida_1`:
    *   leer `cuentas_mirar`, `cuenta_x` o `cuentas_G`;
    *   calcular cualquier estimando;
    *   correr `estadistica_a1.py`.
2. **No importes ni copies código de `tools/a1/`.** Eso incluye `comun_a1`, `plan_a1`, `juntar_a1`, `validar_a1`, `estadistica_a1`, `runner_a1` y `manifiesto_a1`.
    *   Podés ejecutarlos como caja negra (§7) y leer sus docstrings.
    *   No leas el cuerpo de `estadistica_a1.py` antes de commitear tu verificador. Después sí, para diagnosticar diferencias.
3. **No edites** 010, el sello, el manifiesto, la corrida ni la rama del productor. Tu código va en una rama propia; tu bitácora y tu evidencia, a `main`. **Nunca mergees.**
4. **No arregles la trampa del BCa degenerado (§9).** Si tu lectura de 010 difiere de la del productor en algún punto, reportalo como `AMBIGUEDAD_010` con la cita de 010. Decide Abraham.
5. **Paradas:**
    *   Si el manifiesto no da `267ca1d0…`, pará.
    *   Si en el ensayo general queda una diferencia sin clasificar, no pidas la apertura.
    *   En la apertura, si tu fase técnica falla, no calcules estimandos.
    *   Si el cotejo da una diferencia sin explicar, nadie lee veredictos.

## 3. Lecturas, en este orden

| # | Qué | Ruta | Bytes | SHA-256 |
| --- | --- | --- | --- | --- |
| 1 | Enmienda 010: manda en §3 a §9 | `main:docs/agents/respuestas/2026-11-02-010-enmienda-009-a1-sello-original-intacto.md` | 34.776 | `e10b7756ecf5e1bfebdf285e3e37c1af901256327d3e08f0a4abbc8551611127` |
| 2 | Diseño 009 original | `main:docs/agents/respuestas/2026-11-02-009-diseno-corte-causal-16-relevos-recurrentes.md` | 30.215 | `61ab66b7839bc38f1ad6caaee43e60e7f0524fddb3e37ff58ff49acb5c48f1ea` |
| 3 | Sello de 009 | `main:docs/auditorias/evidencia/2026-11-02-02/sello_diseno_16_relevos.json` | 31.673 | `210b581792d183517d1e4e7771b8435e4a6acb537bc1ad383e5725c500073e93` |
| 4 | Esta orden, con los anexos A (D1 a D15), B (cantidades) y C (huellas) | `main:docs/agents/ordenes/2026-11-03-009-verificador-independiente-a1.md` | (este archivo) | (este archivo) |
| 5 | Respuesta 008: cómo se probó la estadística del productor | `main:docs/agents/respuestas/2026-11-03-008-estadistica-a1-escrita-y-probada-sin-abrir-el-sobre.md` | 6.801 | `052442afd4af04b9ca2ac537c4a38579545c860453dd6755b6ca5a8da85ab4e1` |

El repo es público. Cualquier archivo se baja de `https://raw.githubusercontent.com/gatehot59-star/drosophila-fep-connectome/<commit o rama>/<ruta>`.

## 4. Entradas fijadas

**Manifiesto**
*   `results/a1_2026-11-03/prueba_1/manifiesto_a1.json` en la rama `titan/a1-runner-2026-11-03`.
*   640.908 bytes, SHA-256 `267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9`.
*   Hay copia en brain-env: `/workspace/a1/v2/manifiesto_a1.json`.

**Sobre real, que no se abre sin autorización**
*   Está en `results/a1_2026-11-03/corrida_1/` de la misma rama. Lo dejó el commit del bot `7d953dc8577ecf1fdbaecc4859b902af8854e79b`.
*   `bloques/00..19/bloque_KK.jsonl`: 8.540 líneas en total.
*   `SHA256SUMS.txt`:
    *   444 líneas, 45.000 bytes, SHA-256 `bf9ebde69cc12f6c1f5b1c85925aebeeb36fd7fe6f23052aef35706a74cc7e38`;
    *   formato: `sha256  ./bloques/KK/bloque_KK.jsonl`.
*   `validacion_corrida.json` es el control del productor:
    *   2.931 bytes, SHA-256 `443976def90ba60ce946fa24b6d96bb26546aa4ff6698e52ff15aa3de22e11af`;
    *   OK, 8.540 de 8.540, 0 fallos.
*   `RESULTADO.txt`: 181 bytes, SHA-256 `f9f9e759e41e5ac2c04afaf1315f3b49da8816ad39926740449a7e07cd2621a0`.

**Código del productor (sólo como caja negra)**
*   Todo está en `tools/a1/`, en el commit `801487cad19747e96bb346d98ffad1c3d508847c` de la rama:

| Archivo | Bytes | SHA-256 |
| --- | --- | --- |
| `estadistica_a1.py` | 36.891 | `37ab63d7dc94913c010cdc51d89a23a0ace0a4e6e511b4c344ffad15b24503e3` |
| `validar_a1.py` | 6.401 | `189eb6477e1f9e3685d273d89aaee4dca8c8c8a63a82a734dae74b2a6ad34e20` |
| `comun_a1.py` | 8.679 | `756e81aba922824f0bf4e6374936b944b7f30c17e88b659adc35b9416c0d93ed` |
| `plan_a1.py` | 5.408 | `d1b26450ecf8e9ca5211ab7a78beadf536ff61c4db659ed79c3dd9e142662e5d` |
| `juntar_a1.py` | 7.757 | `051d0b474a911930db692fed5826839b426df2953eebd39a86ab69538260d414` |

*   `estadistica_a1.py` no cambia desde `5c9492ff`, con huellas en `HUELLAS_ESTADISTICA.sha256`.

**Kit del ensayo general**
*   Todo está en `tools/a1/`, en el mismo commit `801487ca`:

| Archivo | Bytes | SHA-256 |
| --- | --- | --- |
| `sobre_sintetico_a1.py` | 20.188 | `c89ef7f52ddb017c9cca15c56bbadd4fe974962100454aeefb918d99d1848119` |
| `prueba_sobre_sintetico_a1.py` | 14.081 | `975f4b2a3cae55b1804abb59d874100440a396bc9b1e839cf7b2713e47031966` |
| `mutantes_sobre_sintetico_a1.py` | 4.964 | `a31752b643cc253fee958c954f6c0ba2294ab51d4ccf0820bdbfbd448a3c2959` |

## 5. Esquemas que necesitás sin leer código

### 5.1 Recibo: una línea JSON por ensayo

**Identidad y plan**
*   `protocol_id` (`'009-A1'`), `code_commit`, `runner_version`, `manifiesto_sha256`, `input_hashes`.
*   `input_hashes` es una copia de `manifiesto.entradas`.
*   `subject_id`, `regime` (A, B o C), `condition`, `seed` (0 a 19 en el plan) y `grupo`.

**Estado técnico**
*   `estado` (`'OK'` o `'INVALIDO_TECNICO'`), `exit` y `motivo`.
*   `chequeos`: siete booleanos, que son `identidad`, `Dprime`, `mascara`, `eventos`, `fuentes`, `orden_sinapsis` y `signo_pesos`. Fuera de C0 se suman `pesos_fuera_intactos` y `mascara_en_cero`.
*   `filas_cambiadas`, que fuera de C0 vale lo mismo que `mask_n`.

**Huellas**
*   `identidad`: `{x, d, G, roots}`.
*   `Dprime_hash` y `Dprime_n`.
*   `mask_hash`, `mask_n` y `mask_abs`.
*   `input_events_hash` y `n_input_events`.
*   `mirar_huella`.
*   `espigas_sha256`: sha256 del tren completo de la red, no recalculable desde el recibo.

**Cuentas, en 1 s**
*   `cuentas_mirar`: lista alineada con `manifiesto.sujetos[S].mirar`.
*   `cuenta_x` y `cuentas_G` (alineada con `G`).
*   `espigas_total`, `activas`, `duracion_s`, `duracion_sim_s`.
*   `entorno`: `{brian2, numpy, python, target_pedido, codeobj, dt_s, t_run_s}`.
*   En el banco C, además, `replay_aplicado_hash`.

**Formatos de huella que podés recalcular**
*   `huella_lista(v)`: sha256 de `json.dumps(sorted(int(t) for t in v), separators=(',', ':')) + '\n'`.
    *   `Dprime_hash` es `huella_lista(Dp)`.
    *   `mirar_huella` es `huella_lista(mirar)`.
*   El resto se compara contra el manifiesto:
    *   `mask_*` contra `sujetos[S].huellas_condicion[cond]`, que trae `{n, abs, sha256}`;
    *   `input_events_hash` contra `grupos[grupo].eventos[str(seed)].sha256`.

### 5.2 Manifiesto

**Claves de arriba**
*   `celdas`: 44, cada una con `{sujeto, regimen, grupo, condiciones}`.
*   `sujetos`: 22.
*   `grupos`: 40, cada uno con `{fuentes, eventos, regimen}`.
*   `entradas`: 4 pines.
*   `parametros`, `protocolo` y `n_ensayos_plan` (8.540).
*   `humo`: 10 ids con semillas 900 y 901, fuera del plan.
*   `chequeos` y `contrato_semilla`.

**Cada sujeto**
*   `x`, `d` (el driver en relevos; null en hubs), `G`, `Dp` (D′ ordenado), `Dp_huella {n, sha256}`, `mirar`, `roots`, `huellas_condicion`, `mascaras_base`, `composicion` y `clase` (`relevo` o `hub`).
*   Los relevos traen además `A` y `A_huella`.
*   R01 trae `cascada_ZA = [6128, 59804]`. 59804 es su driver.
*   Los hubs traen `replay`.

**Banco C**
*   `C_<bits>`: el bit k corresponde a `G[k]` (`replay[cond].encendidos`).
*   `C_desplazado` tiene todos encendidos con 0/10 ms (dos drivers) o 0/5/10 ms (tres).

**Lo medido el 3-nov en el manifiesto real**
*   `mirar` contiene D′, x y G en los 22 sujetos.
*   D′ no contiene a x ni a G.

### 5.3 Agregado del productor (`agregado_a1.json`)

**Claves de arriba**
*   `protocolo`, `version`, `parametros`, `decisiones` (D1 a D15, igual al anexo A), `invalidas`, `familias`, `casos`, `veredictos`, `intervalos`, `manifiesto_sha256`, `validacion`, `entradas` y `codigo_sha256`.
*   `invalidas` es una lista ordenada de `'R|S'`, por ejemplo `'B|R04'`.

**`intervalos[id]`**
*   Promedios: `{tipo: 'media', estimado, ic95: [lo, hi] o null, estado_ic}`.
*   Cocientes: `{tipo: 'cociente', numerador, denominador, estimado, ic95, estado_ic[, motivo]}`.
*   `estado_ic` vale `OK`, `DEGENERADO`, `INDEFINIDO` o `SIN_ESTIMADO`.
*   Si la celda es inválida, el id está y vale null.

**`familias[F]`**
*   `{m, alfa, n_deciden, pruebas: [...]}`.
*   Cada prueba trae `{id, estado, n, media, de, t, gl, p_observado, p_familia, signos_bilateral, p_holm, decide}`.
*   `estado` vale `OK`, `VARIANZA_CERO` o `INVALIDO_TECNICO`.

**`casos['R|S']`**
*   **Relevo:**
    *   `estado`, `activacion {estado, medido, criterios, causas}`, `medias`, `fracciones`, `efectos` y `H_C0`;
    *   `cocientes {r_Q1, s4, c_X, r_weak}`: cada uno es un intervalo más `estado_ic_calculado` y, en T1, `margen`, `limite_inferior_supera_margen` e `intervalo_contradice`;
    *   `qweak {banda, DQWEAK_Hz, nota}`;
    *   en B de R01 a R03, `T1 {estado, criterios, pruebas, intervalos}`;
    *   en A de R01, `cascada_ZA`.
*   **Hub B:** `estado`, `activacion`, `medias`, `fracciones`, `efectos`, `cocientes {r_Q1conj, c_Xconj, s4conj}` y `T2 {…}`.
*   **Hub C:** `estado: 'VALIDO'`, `tabla_ON_OFF {cond: {H_Hz, etiqueta}}`, `transferencia`, `H_desplazado_Hz` y `FC {estado, prueba, intervalo, lectura}`.
*   **Celda inválida:** `{estado: 'INVALIDO_TECNICO', motivos: [...]}`.

**`veredictos`**
*   `P_T1_B {veredicto, casos, requiere}`.
*   `P_T2_B {veredicto, tipos, instancias, requiere}`.
*   `F_C {H: estado}`.
*   `F_R01 {firma, contrastes}`.
*   `T3`, `QWEAK` y `P_ESTRATOS`. Este último está retirado.

## 6. Qué tiene que verificar tu instrumento

### Fase E · estructura, sin recibos

*   Calculá el sha256 del manifiesto.
*   **Reconstruí el plan desde las listas de 010, no desde `plan_a1`:**
    *   relevos: 11 condiciones (`C0, Q1, Q2, Q3, Q4, QCOL, Q1uQCOL, QXD, Q1uQXD, QWEAK, SHAM`);
    *   R01 en A suma 4: `ZA, ZAuQ1, ZAuQCOL, ZAuQ1uQCOL`;
    *   hubs en B: `C0, Q2, Q4conj, Q1_<g>` por driver y `Q1conj`;
    *   hubs en C: los 2^k subconjuntos y `C_desplazado`;
    *   semillas 0 a 19.
    *   El total tiene que dar 44 celdas, 427 condiciones y 8.540 ensayos.
*   **Por sujeto:**
    *   D′, x y G están en `mirar`;
    *   D′ no contiene a x ni a G;
    *   `len(Dp)` es igual a `Dp_huella.n`;
    *   `huella_lista(Dp)` es igual a `Dp_huella.sha256`, con tu propia implementación del formato.
*   **Opcional y valioso:** cotejar tamaños y huellas de D′ con la evidencia de 010, que midió el instrumento de Astra y no el de BRAIN. Está en `main:docs/agents/evidencia/2026-11-02-010-guardas-enmienda-009-a1.md`, con SHA-256 del pin `d5d9b7ba…` en `manifiesto.entradas.evid010_sha256`.

### Fase T · técnica: lee recibos, no calcula estimandos

1. **Integridad:** el sha256 de cada bloque tiene que coincidir con `SHA256SUMS.txt`.
2. **Lectura:** cada línea se parsea como JSON. Una línea que no se lee no tiene celda.
3. **Cobertura por tupla** (sujeto, régimen, condición, semilla): sin faltantes, sin duplicados y nada fuera del plan. Las semillas 900 y 901 están fuera.
4. **Por recibo:**
    *   `protocol_id` y `manifiesto_sha256` coinciden con el pin;
    *   `estado` es OK y `exit` es 0;
    *   todos los `chequeos` son true;
    *   `identidad` es igual al manifiesto;
    *   `Dprime_*`, `mask_*` y `mirar_huella` coinciden con sus huellas;
    *   `grupo` es el de la celda e `input_events_hash` coincide con el del grupo y la semilla;
    *   fuera de C0, `filas_cambiadas` es igual a `mask_n`.
5. **Pareado:** misma `input_events_hash` en todas las condiciones de (sujeto, régimen, semilla). SHAM tiene que ser idéntico a C0 en `espigas_sha256`, `cuentas_mirar`, `espigas_total`, `cuenta_x` y `cuentas_G`.
6. **Unicidad:** un solo `code_commit`, un solo `runner_version` e `input_hashes` igual a `manifiesto.entradas`.
7. **Coherencia interna**, que el control del productor no mira (medido, §7):
    *   `len(cuentas_mirar)` es igual a `len(mirar)`;
    *   toda cuenta es entera y mayor o igual a 0;
    *   `cuenta_x` es igual a `cuentas_mirar[pos(x)]`;
    *   `cuentas_G[k]` es igual a `cuentas_mirar[pos(G[k])]`;
    *   la suma de `cuentas_mirar` no supera `espigas_total`;
    *   las cuentas no nulas no superan `activas`.
    *   Esta fase lee cuentas sólo para comparar. **No imprimas ninguna cuenta.**
8. **Entorno:** informá si `entorno` es uniforme.

Salida: cada falla con código, ensayo y celda, más las celdas que invalidás con tu propia regla. Después compará esa regla con D13.

### Fase S · estadística

Sólo corre sobre el sobre sintético, o sobre el real con autorización.

*   **Magnitudes por ensayo**, con D′ = `Dp`:
    *   Y_s(C) = Σ_{j∈D′} `cuentas_mirar[pos(j)]` / 1 s;
    *   H_s(C) = `cuenta_x` / 1 s;
    *   G_s,k(C) = `cuentas_G[k]` / 1 s.
*   **Cantidades:** el anexo B, con nombres exactos.
*   **Registro:** todas las cantidades de las 44 celdas, salgan o no, con id `'R|S|nombre'`.
    *   Son 722 y van en orden de `sorted()` de Python.
    *   El ensayo general deja la lista en `registro_ids.txt`, con SHA-256 `7c6dadc180b56d1d0c2be39782e948c3b7f73b994294412a345b8d011691c40a`.
*   **Flujo PCG64 (D4):**
    *   Un solo `numpy.random.Generator(PCG64(2026110209))`.
    *   Para cada id del registro, en orden, `integers(0, 20, size=(20000, 20))`.
    *   Esa matriz son los índices de semilla remuestreados de ese id. Se consume aunque la celda sea inválida.
*   **BCa por 010 §7 y D2**, con cocientes por D3.
*   **t pareado unilateral**: H1 es media > 0, con gl 19. La varianza cero sigue D14.
*   **Inversión de signos** exacta y bilateral sobre los 2^20 signos. Los empates siguen D14.
*   **Holm por familia**, con α 0,01, y p_familia 1 donde dice D1. Las familias van en este orden:
    *   F_B, 46 pruebas:
        *   `B|R01|DQ2` a `B|R16|DQ2`;
        *   `B|H1|DQ2, B|H1b|DQ2, B|H2|DQ2, B|H3|DQ2, B|H4|DQ2, B|H4b|DQ2`;
        *   `B|R01|T1a, B|R01|T1b, B|R02|T1a, B|R02|T1b, B|R03|T1a, B|R03|T1b`;
        *   T2a, T2b y T2c de cada hub, en el orden H1, H1b, H2, H3, H4, H4b.
    *   F_C: `C|H1|FC` a `C|H4b|FC`, en ese orden de hubs.
    *   F_R01: `A|R01|ZA1, ZA2, ZA3`.
    *   `decide` exige estado OK y p_holm < 0,01.
*   **Activación, publicación de cocientes, T1/T2, combinación y banco C**, en el anexo B.
*   **Motores independientes sugeridos:**
    *   `scipy.stats.ttest_1samp(alternative='greater')`.
    *   `scipy.stats.bootstrap(method='BCa', paired=True, n_resamples=20000, rng=<el Generator compartido>)`. Con `batch=None`, scipy saca una sola vez `integers(0, n, (n_resamples, n))` por llamada; 008/E04 lo midió: mismo flujo, diferencia de 4,4e-15 del ancho.
    *   Para los ids que no se calculan, consumí el bloque a mano.
    *   Para ver si algún denominador remuestreado es ≤ 0 (INDEFINIDO), cloná el estado del generador antes de llamar a scipy, o calculá desde los mismos índices.

### Fase K · cotejo con el agregado del productor

*   **Intervalos:**
    *   `estado_ic` tiene que ser igual;
    *   `estimado`, `ic95` y los numeradores y denominadores, dentro de 1e-9·max(1, |valor|).
*   **Pruebas:**
    *   `estado` y `decide` iguales;
    *   `p_observado`, `p_holm` y `signos_bilateral`, dentro de 1e-12.
*   **Casos y veredictos:** iguales en `invalidas`, en el estado de cada caso y de su activación, en T1/T2, en el `estado_ic` de cada cociente, en `transferencia`, en la banda de QWEAK y en `veredictos`.
*   **Cada diferencia se clasifica** como `BUG_PRODUCTOR`, `BUG_VERIFICADOR`, `AMBIGUEDAD_010` (decide Abraham) o `HUECO_DEL_CONTROL`. Este último es una falla técnica que tu fase T ve y la del productor no.
*   **Resultado:**
    *   `CONCORDANTE` si no queda ninguna diferencia sin explicar;
    *   si no, `DISCORDANTE`.

## 7. Ensayo general: sobre sintético, ahora y sin autorización

El sobre sintético tiene los 8.540 recibos con el esquema real y las huellas del manifiesto real. Las cuentas salen de un modelo sembrado, no de una simulación. Cada recibo lleva `"sintetico": true` y `code_commit: "SINTETICO-009"`, y el generador se niega a escribir en una ruta con `corrida_`.

**Paso 1. Regenerá y corré el productor**
*   Con el manifiesto real:
    *   `python3 prueba_sobre_sintetico_a1.py --manifiesto M --sha-manifiesto 267ca1d0… --trabajo DIR`
*   Eso genera los tres escenarios, corre el control del productor, corre `estadistica_a1.py --abrir-sobre` sobre cada sobre sintético y deja `DIR/est_<escenario>/agregado_a1.json`.
*   En ese comando, `--abrir-sobre` abre sólo el sobre sintético.
*   Las huellas tienen que dar lo del anexo C. En brain-env, con Python 3.12.14, NumPy 2.5.3 y SciPy 1.18.1, salen byte a byte. En otra máquina, cotejá con tolerancia.

**Paso 2. Lo que vas a encontrar**

| Escenario | Qué tiene | Qué vio el productor | Qué tiene que ver tu verificador |
| --- | --- | --- | --- |
| limpio | ninguna falla técnica | control OK, 0 fallos | 0 fallos y cotejo `CONCORDANTE` |
| sucio | 13 corrupciones detectables y 6 ciegas | invalidó las 13 celdas de las detectables y ninguna de las ciegas | las 19; las 6 ciegas son `HUECO_DEL_CONTROL` esperado |
| global | una línea ilegible al final de `bloque_07` | invalidó las 44 celdas por D13 | lo mismo, o tu regla con su justificación |

*   **Las 6 ciegas:**
    *   `R15|B|Q1|6`: `cuenta_x` incoherente con `cuentas_mirar`;
    *   `R16|A|Q4|10`: una cuenta de D′ negativa;
    *   `H4b|B|C0|1`: `runner_version` distinto;
    *   `H2|C|C_11|13`: `input_hashes` alterado;
    *   `H4|C|C_10|17`: `cuentas_G` incoherente;
    *   `R12|A|Q4|14`: `espigas_total` bajo.
*   Dos de las ciegas cambian estimandos del productor sin que nadie lo marque: `B|R15|c_X` (0,8973 a 0,8853) y `A|R16|DQ4` (34,9 a 34,5 Hz).
*   Las ciegas también pueden mover un veredicto. En el sucio, el productor da P_T2_B `SOSTENIDA` con CB0172 `BLOQUEADO`. Si tu verificador invalida `B|H4b` por el `runner_version` distinto, PS100 también queda `BLOQUEADO` y P_T2_B pasa a `INVALIDO_TECNICO`.
*   `SEMBRADO.json` de cada sobre trae:
    *   los parámetros sembrados por celda;
    *   la trampa en `B|R02` y `B|H3`;
    *   la lista de corrupciones con el código que el control del productor debería dar.

**Paso 3. Commiteá**
*   Tu verificador, sus pruebas (incluidos recibos corruptos propios), tus mutantes y la salida cruda del ensayo.

**Criterio para pedir la apertura**
*   limpio `CONCORDANTE`;
*   sucio y global con todas sus diferencias clasificadas;
*   tus pruebas en verde;
*   tus mutantes muertos.

## 8. Apertura del sobre real: sólo con autorización escrita de Abraham

1. Tu verificador queda congelado en un commit y anotás el SHA.
2. Corrés las fases E y T sobre `corrida_1`. Si algo falla, parás y reportás.
3. Corrés la fase S y commiteás tu salida, o al menos su sha256, **antes de leer el agregado del productor**.
4. BRAIN corre `estadistica_a1.py` (5c9492ff, sin cambios) con `--abrir-sobre` sobre `corrida_1` y commitea `agregado_a1.json` con su sha256.
5. Corrés la fase K y commiteás el cotejo.
6. Sólo si da `CONCORDANTE`, Abraham lee los veredictos con la tabla fijada en 007.

**Dónde correr**
*   En brain-env, por MUDH Gateway/build. El stack está instalado: la estadística del productor tardó 7,6 a 12,8 s por sobre de 8.540 recibos.
*   O en Actions con dependencias fijadas. Actions no trae numpy ni scipy.

## 9. Propiedades conocidas que no son bugs

**La trampa del BCa degenerado**

Se queda tal cual 010 por decisión de Abraham.

*   **Mecanismo:**
    *   Las máscaras ponen pesos en cero.
    *   Si Q1 apaga a x en las 20 semillas, Y(Q1) es igual a Y(Q2) semilla por semilla.
    *   Entonces r_Q1 vale 1 en todo remuestreo, el BCa sale DEGENERADO y el criterio queda SIN_DECIDIR, aunque el efecto sea máximo.
    *   Pasa lo mismo con c_X o c_Xconj si x queda en 0 en todas las semillas, con r_Q1conj, y con s4 si Q4 no mueve a x.
*   **Qué es dato y qué no:**
    *   El humo mostró x de 30 a 0 y de 16 a 0 bajo Q1 en R01 B.
    *   Que pase en el sobre real es una inferencia, NO MEDIDA.
*   **Qué se espera del verificador:** que reproduzca la regla, no que la corrija.

**Otras propiedades**
*   **D1:** Holm usa el p observado también en celdas NO_INFORMATIVO_EN_B, porque la activación depende del Holm.
*   **D12:** el índice de ablación de 009 no se implementa.
*   **QWEAK:** nunca invalida nada.
*   **Banco C:** no tiene criterio de activación.
*   **A:** es descriptivo y no tiene familia propia.
*   **P_ESTRATOS:** retirado (010 §8).

## 10. Entregables del verificador

**Código**
*   En una rama propia que no sea la del productor, por ejemplo `titan/verificador-a1-independiente`, dentro de `tools/verificador_a1/`.
*   Sólo stdlib, numpy y scipy, con versiones declaradas.

**Salidas**
*   `verificacion_tecnica.json`: fases E y T.
*   `verificador_a1.json`: fase S, con los mismos ids que el registro.
*   `cotejo_a1.json`: fase K, con cada diferencia y su clase.

**Lectura de 010**
*   Un archivo `lectura_010.md` que diga, para cada D1 a D15, si sigue a 010, con la cita.
*   Ahí entra el aporte que el instrumento no da: si el productor eligió bien qué medir.

**Bitácora y Doc**
*   La respuesta en `main:docs/agents/respuestas/` con los seis campos y la evidencia cruda en `docs/agents/evidencia/`.
*   El Doc espejo en ClickUp, bajo Topo inverso.

## Anexo A · D1 a D15, tal cual el productor las fijó antes de abrir el sobre

Copia literal de la constante `DECISIONES` de `estadistica_a1.py` (5c9492ff). La misma lista sale en cada `agregado_a1.json`.

*   D1. Holm usa el p observado de toda prueba con datos validos y varianza no nula, tambien en casos NO_INFORMATIVO_EN_B: la activacion de B depende del Holm de F_B, y poner el centinela segun la activacion la volveria circular. El centinela p_familia = 1, con p_observado = null, queda para celdas INVALIDO_TECNICO y pruebas con varianza cero.
*   D2. BCa: z0 con la fraccion de remuestreos menores mas la mitad de los iguales al estimado; aceleracion por jackknife de semillas; cuantiles lineales. DEGENERADO si todos los remuestreos son iguales, si z0 es infinito, si la aceleracion no esta definida o si los niveles ajustados salen de (0, 1).
*   D3. Cociente = media(numerador) / media(denominador). Sin estimado si el denominador observado es <= 0; INDEFINIDO si algun remuestreo o algun jackknife tiene denominador <= 0.
*   D4. El registro de ids sale solo del manifiesto. Cada id consume 20.000 x 20 enteros del flujo PCG64 en orden lexicografico, se pueda calcular o no; asi el intervalo de un id no depende de que otra celda sea invalida.
*   D5. El IC95 de DQ2 excluye cero si su limite inferior es > 0 o su limite superior es < 0.
*   D6. r_weak = DQWEAK / DQ2; la banda usa el |r_weak| puntual.
*   D7. Colaterales: COL_cortado = Y(Q1uQCOL) - Y(Q1); COL_interaccion = COL_cortado - [Y(QCOL) - Y(C0)]. Ruta directa: XD_q1 = Y(Q1uQXD) - Y(QXD); XD_dif = XD_q1 - [Y(Q1) - Y(C0)].
*   D8. En B los cocientes de la celda (r_Q1, s4, c_X, r_weak; en hubs r_Q1conj, c_Xconj, s4conj) se publican como null, con numerador, denominador, estado calculado y motivo, si la celda no queda ACTIVADO: 010 la declara no interpretable. En A cada cociente secundario exige su denominador positivo y el IC95 de ese denominador que excluya cero (DQ2 para r_Q1 y r_weak, H(C0) para c_X y s4); RECLUTADO o NO_RECLUTADO_EN_A se informa aparte y no los bloquea.
*   D9. Veredictos conjuntos: cada unidad PASA, NO_PASA (con motivo) o queda BLOQUEADA por datos invalidos. Con k unidades requeridas: SOSTENIDA si pasan k; INVALIDO_TECNICO si las bloqueadas podrian completar k; NO_INFORMATIVO_EN_B si todas las que no pasan son no informativas; SIN_DECIDIR en el resto. Un tipo de hub PASA si pasan todas sus instancias, NO_PASA si alguna no pasa y queda BLOQUEADO si no hay NO_PASA y alguna esta bloqueada.
*   D10. Banco C: vacio = todos los bits en 0; completo = todos en 1. INDETERMINADO si algun subconjunto queda entre 2 y 10 Hz; OTRA_TRANSFERENCIA si no es OR ni AND compatible y no hay indeterminados.
*   D11. En A, RECLUTADO exige las mismas magnitudes que la activacion de B, sin Holm ni familia A: drivers y x en C0 >= 10 Hz, DQ2 >= 5 Hz e IC95 de DQ2 que excluye cero.
*   D12. El indice original de ablacion de 009 no se implementa: su definicion no esta en 009, ni en 010, ni en el sello 210b5817. Se publican DQ1conj, cada DQ1 individual y T2c.
*   D13. Una falla del control del productor invalida la celda (sujeto, regimen) que nombra su detalle; una falla sin celda (archivo ilegible, code_commit mixto, validacion no OK sin detalle) invalida las 44. Un recibo que falta, se repite o no se puede leer invalida su celda.
*   D14. Tolerancias: varianza cero si la desviacion es <= 1e-12 * max(1, |media|); en la inversion de signos, las sumas a menos de 1e-9 * (1 + suma |d|) del umbral cuentan como extremas.
*   D15. Unidades: cada cuenta es de espigas en NTICKS * DT_S = 1 s, o sea Hz; Y en Hz poblacionales del D fijo y tasas por neurona como media de semillas. El banco C no tiene criterio de activacion: se publican la tabla ON/OFF, H_desplazado y FC. ZA1 usa la tasa del blanco de cascada_ZA, que tiene que ser un driver de R01.

## Anexo B · Cantidades, criterios y combinaciones

Notación: y0 = Y(C0), h0 = H(C0). Todo es por semilla. «media» es un promedio de semillas con su BCa; «cociente» es media(num)/media(den), por D3.

**Relevo, en A y en B: 20 cantidades por celda**

*   **Efectos:** `D<b>` = media Y(b) − y0, para b en Q1, Q2, Q3, Q4, QCOL, Q1uQCOL, QXD, Q1uQXD, QWEAK y SHAM.
*   **Cocientes:**
    *   `r_Q1` = cociente con numerador Y(Q1) − y0 y denominador Y(Q2) − y0;
    *   `c_X` = cociente con numerador h0 − H(Q1) y denominador h0;
    *   `s4` = cociente con numerador H(Q4) y denominador h0;
    *   `r_weak` = cociente con numerador Y(QWEAK) − y0 y denominador Y(Q2) − y0.
*   **Colaterales y ruta directa (D7):**
    *   `COL_cortado` = media Y(Q1uQCOL) − Y(Q1);
    *   `COL_interaccion` = media [Y(Q1uQCOL) − Y(Q1)] − [Y(QCOL) − y0];
    *   `XD_q1` = media Y(Q1uQXD) − Y(QXD);
    *   `XD_dif` = media [Y(Q1uQXD) − Y(QXD)] − [Y(Q1) − y0].
*   **Resto:**
    *   `Q1_menos_Q3` = media Y(Q1) − Y(Q3);
    *   `HC0` = media h0.

**Extras de algunos relevos**
*   En B, en R01, R02 y R03, se suman 2:
    *   `T1a` = media [Y(Q1) − y0] − 0,35·[Y(Q2) − y0];
    *   `T1b` = media H(Q4) − 0,50·h0.
*   En A de R01 se suman 3, con iz como el índice de `cascada_ZA[1]` en G:
    *   `ZA1` = media G_iz(ZA) − G_iz(C0);
    *   `ZA2` = media [H(ZA) − h0] − [H(ZAuQ1) − H(Q1)];
    *   `ZA3` = media [Y(ZAuQ1uQCOL) − Y(Q1uQCOL)] − [Y(ZAuQCOL) − Y(QCOL)].

**Hub en B: 9 cantidades más una por driver**

Notación: dq2 = Y(Q2) − y0, dqc = Y(Q1conj) − y0.

*   **Efectos:**
    *   `DQ2` = media dq2;
    *   `DQ4conj` = media Y(Q4conj) − y0;
    *   `DQ1conj` = media dqc;
    *   `DQ1_<g>` = media Y(Q1_g) − y0, una por driver.
*   **Cocientes:**
    *   `r_Q1conj` = cociente dqc / dq2;
    *   `c_Xconj` = cociente [h0 − H(Q1conj)] / h0;
    *   `s4conj` = cociente H(Q4conj) / h0.
*   **Contrastes de T2:**
    *   `T2a` = media dqc − 0,40·dq2;
    *   `T2b` = media [h0 − H(Q1conj)] − 0,40·h0;
    *   `T2c` = media dqc − promedio_g[Y(Q1_g) − y0].

**Hub en C: 1 cantidad por celda**
*   `FC` = media H(C_1…1) − H(C_desplazado).

**Total:** 649 cantidades de relevos, 67 de hubs en B y 6 de hubs en C: 722.

**Activación** (D5 y D11)
*   Exige todo esto:
    *   cada driver, en promedio de semillas en C0, a 10 Hz o más;
    *   x en C0 a 10 Hz o más;
    *   el estimado de DQ2 en 5 Hz o más;
    *   el IC95 de DQ2 en estado OK y que excluya cero.
*   En B se suma que `B|S|DQ2` decida en F_B.
*   Estados posibles:
    *   en B, `ACTIVADO` o `NO_INFORMATIVO_EN_B`;
    *   en A, `RECLUTADO` o `NO_RECLUTADO_EN_A`.

**Publicación de cocientes** (D8)
*   En B, si la celda no queda ACTIVADO, los cocientes salen con estimado e ic95 null y `estado_ic` `NULO`. El estado calculado queda en `estado_ic_calculado`.
*   En A, r_Q1 y r_weak exigen que el IC95 de DQ2 excluya cero; c_X y s4 exigen lo mismo del IC95 de HC0.

**T1**, en B de R01, R02 y R03
*   `PASA` si se cumple todo esto:
    *   la celda está activada;
    *   T1a y T1b deciden;
    *   el límite inferior de r_Q1 supera 0,35 con estado OK;
    *   el límite inferior de s4 supera 0,50 con estado OK.
*   Si no está activada, `NO_PASA:NO_INFORMATIVO_EN_B`.
*   Si está activada pero falla otra cosa, `NO_PASA:SIN_DECIDIR`.
*   Si la celda es inválida, `BLOQUEADO`.

**T2**, por hub
*   `PASA` si se cumple todo esto:
    *   la celda está activada;
    *   T2a, T2b y T2c deciden;
    *   el límite inferior de r_Q1conj supera 0,40;
    *   el límite inferior de c_Xconj supera 0,40;
    *   el límite inferior del IC de T2c supera 0.
*   Si no, los mismos estados que en T1.

**Combinación** (D9)
*   P_T1_B combina R01, R02 y R03 con k = 3.
*   P_T2_B combina tipos con k = 3. Los tipos son CB0580 (H1 y H1b), PS100 (H4 y H4b), CB0534 (H2) y CB0172 (H3).

**Banco C** (D10)
*   La etiqueta de cada subcondición sale de la media de H:
    *   10 Hz o más, ON;
    *   2 Hz o menos, OFF;
    *   en el medio, IND.
*   Compatible con OR: vacío OFF y todo lo demás ON.
*   Compatible con AND: completo ON y todo lo demás OFF.
*   F_C de cada hub:
    *   `SOSTENIDA` si FC decide;
    *   `SIN_DECIDIR` si no;
    *   `INVALIDO_TECNICO` si la celda es inválida.

**F_R01**
*   `firma` es `SOSTENIDA` si deciden ZA1, ZA2 y ZA3.
*   Si A|R01 es inválida, `INVALIDO_TECNICO`.
*   Si no, `SIN_DECIDIR`.

**QWEAK** (D6)
*   La banda depende de |r_weak|:
    *   menos de 0,05, `PEQUENO`;
    *   menos de 0,10, `INTERMEDIO`;
    *   el resto, `ALTO`.
*   Sólo hay banda si r_weak se publica.

## Anexo C · Huellas del ensayo general

Medidas en brain-env el 3-nov-2026 sobre el manifiesto real y el código de `801487ca`. Las salidas crudas están en `main:docs/agents/evidencia/2026-11-03-009-verificador-a1/`.

| Escenario | Líneas | `SHA256SUMS.txt` | Control del productor | `agregado_a1.json` (exit) |
| --- | --- | --- | --- | --- |
| limpio | 8.540 | `121045455135271846cb8b45121f40994e10cbae5349fc0ede3f2d64129b82b6` | OK, 0 fallos | `bf8e90b867af195b7c276137f7afce5c257b8bb8dec80b73c69747aefea96219` (0), igual en dos corridas |
| sucio | 8.541 | `4546466dd7b1d7425da21c4a353396b9166cd80ba6056b9f0be973cf38709fa1` | 15 pares (código, celda) en 13 celdas | `c050a9ebba767b488e7f18ecc38df994651a89579c2d2d208144ac8fea3eef1b` (1) |
| global | 8.541 | `76c6a87a237241f23f3c44a878e9554e1d7c57c2a1b0c0d36de8d496f0a11abd` | 1 falla, ILEGIBLE en `bloque_07.jsonl:441` | `b873a1cbc95d716e82c993ed0d6905888db2388b303ae61ca7c1b2a158cf81d3` (1) |

`registro_ids.txt`: 722 ids, SHA-256 `7c6dadc180b56d1d0c2be39782e948c3b7f73b994294412a345b8d011691c40a`.

--- METODO PROMETEO ---
Accion delicada: SI (emite una orden dirigida a otro ejecutor)
Modo aplicado:   FULL
Maquina:         brain-env para el ensayo general; sandbox sólo para redactar
Rubrica:         en la respuesta 2026-11-03-009
Instrumento:     prueba_sobre_sintetico_a1.py y mutantes_sobre_sintetico_a1.py en brain-env (evidencia en docs/agents/evidencia/2026-11-03-009-verificador-a1/)
Artefactos:      docs/agents/respuestas/2026-11-03-009-verificador-independiente-orden-y-ensayo-general.md + Doc de ClickUp (ver la respuesta)
