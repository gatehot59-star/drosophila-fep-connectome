# 2026-10-12-015: la tarea con las etiquetas de la mosca quedó sellada; 46 neuronas con DNp06, cinco etiquetas y el giro por izquierda menos derecha

**Doc espejo:** https://app.clickup.com/90171457413/docs/2kza6fw5-21577
**Rama:** `titan/tarea-mosca-2026-10-12` (desde `titan/lineas-etiquetadas-2026-10-12`, `72b7fa4`). Candidato `3bc1a55` (md5 `4984acd1cb856bd5d3c5169868b904fb`); **sello `57d094a`** (`tools/escape_aterrizaje/tarea_mosca.py`, md5 `40d64e074d9163753439307c5be4ac5e`). Sin PR.

## Veredicto (conclusión)

- [SELLADO] El instrumento quedó en git antes de cualquier corrida completa. Humo 2 sobre el sello: `CHEQUEO INSTRUMENTO ... -> VALIDO`, `EXIT_RUN=0`, 234,8 s.
- [MEDIDO, sujeto] Motivo de **46 neuronas** (40 visuales y 6 descendentes), 187 aristas, 1.149 sinapsis, **0 inhibitorias**, todas del mismo lado. Contiene exacto el motivo de la 003 (`REPRODUCE_003 ... aristas=73 contra 73 -> True`). Las 4 LPLC2 de DNp06 por lado no coinciden con las 4 de DNp01: quedan 8 LPLC2 por lado. Dentro del motivo, DNp06 izquierda recibe 79 sinapsis de LPLC1 y 72 de LPLC2; la derecha, 65 y 78.
- [CAMBIO DECLARADO, antes del sello] En el humo 1 las líneas de giro eran DNp06 izquierda y DNp06 derecha sueltas: con el looming frontal en vuelo cruzaban las dos antes que DNp07 y el aterrizaje frontal salió 0,050 a 0,075 con W y 0,025 con la regla a mano. El giro pasó a ser la diferencia izquierda menos derecha (la mosca gira por diferencia entre lados; Kim 2023 mide L-R WBA). En el humo 2 el aterrizaje frontal dio 0,950 a 0,975 con W y 0,950 con la regla. Mismo cambio para W, SL, T y la regla.
- [HUMO, sin valor] Con 3 nulos el p mínimo es 0,25, así que el «NO PAGA» del humo es mecánico. Dos avisos: con A = 0,6 y ruido 0,15 la regla a mano ya le gana a W (McNemar 11 contra 30, p 0,0043), y posada el punto da despegues falsos (acierto 0,350 a 0,850).
- [NO MEDIDO] La corrida completa. Falsador pre-registrado: con las etiquetas de la mosca, W no le gana a SL ni a T con Holm (global NO PAGA).

## 1. Pedido

21:11: clic en «Diseñar y sellar la tarea con las cinco etiquetas» (respuesta 014).

## 2. Herramientas y máquina

- **GitHub MCP:** lectura de `escape_aterrizaje_dbc3.py` (módulo de la 003) en `72b7fa4`; rama nueva `titan/tarea-mosca-2026-10-12`; commits `3bc1a55` (candidato) y `57d094a` (cambio declarado y sello); este archivo a `main`.
- **Sandbox de ClickUp:** escritura del script, `ast.parse` OK, y prueba unitaria con módulos de relleno: 20 condiciones con las etiquetas esperadas (40 ensayos cada una sobre 400) y la carrera: `carrera [3 1 0]` con líneas sueltas y `[2 3]` con la diferencia (DNp06 simétrica más DNp07 tardía da aterrizar; DNp06 izquierda sola da girar a la derecha).
- **brain-env:** clon fresco de la rama (módulos 003 y 005 con md5 `4d40477d87406c31672acfb6e6e8f5a2` y `e060c4bffb685aa550dadc19eda3dd02`, iguales al pin); humo 1 sobre `3bc1a55` (180,0 s) y humo 2 sobre `57d094a` (234,8 s), los dos `EXIT_RUN=0` y VALIDO.
- **ClickUp:** Doc público nuevo https://app.clickup.com/90171457413/docs/2kza6fw5-21577. Actions y Kaggle sin uso; sin cuota ajena.

## 3. Qué quedó sellado

### 3.1 Tarea

20 condiciones balanceadas: estado (posada, en vuelo) x estímulo x lado; 40 pasos de 20 ms.

| Estado | Estímulo | Respuesta correcta | Fuente | Línea que la da |
|---|---|---|---|---|
| Posada | LOOM_LATERAL o LOOM_FRONTAL | Despegar (1) | Ache 2019, Nat Neurosci | DNp01 izquierda o derecha |
| Posada | PUNTO, BARRA o NADA | Nada (0) | PUNTO y BARRA: etiqueta de trabajo, sin fuente | Ninguna cruza |
| En vuelo | LOOM_LATERAL o PUNTO | Girar alejándose (3 si viene de la izquierda, 4 si de la derecha) | Kim 2023; Ache 2019, Nat Neurosci | DNp06 izquierda menos derecha, y al revés |
| En vuelo | LOOM_FRONTAL o BARRA | Aterrizar (2) | Ache 2019, Nat Neurosci | DNp07 izquierda o derecha |
| En vuelo | NADA | Nada (0) | | Ninguna cruza |

Looming con l/v de 10 a 80 ms; el frontal es el mismo looming en los dos lados a la vez. Punto oscuro chico de un lado con dirección al azar; barra oscura de adelante hacia atrás.

### 3.2 Sintonías (supuestos declarados)

- **LC4:** velocidad de expansión saturada más 0,1 por punto y barra (como la 005).
- **LPLC2:** gaussiana del tamaño mientras se expande (50 y 20 grados, como la 005) más A por el contraste del punto, entero si va de atrás hacia adelante y 0,5 si va al revés; 0 a la barra. A en {0; 0,3; 0,6}.
- **LPLC1:** el contraste del punto, sin dirección. Descriptiva: SILENCIOSA.
- **LPLC4:** la barra, 0,3 del punto de adelante hacia atrás y la velocidad de expansión (entera frontal, 0,3 lateral). Descriptiva: SILENCIOSA.

### 3.3 Lector, nulos y juez

Líneas sin entrenar: DNp01 compite sólo posada; DNp07 y la diferencia de DNp06 compiten sólo en vuelo. Umbral de cada línea: cuantil 0,95 de su máximo sobre los ensayos de entrenamiento en que compite y cuya respuesta correcta es nada. Gana la primera que cruza. Nulos: 300 SL (destinos barajados dentro de cada bloque de lados, conserva grados) y 300 T (sintonías barajadas entre visuales del mismo lado). Rival: regla a mano con las mismas líneas sobre las entradas crudas. Celdas primarias: A x ruido {0,15; 0,45}. Holm sobre 12 por cola; por amplitud GANA si gana con los dos ruidos; global PAGA LA TAREA DE LA MOSCA, DEPENDE DE LA AMPLITUD DE LPLC2 o NO PAGA. Controles: guardas, reproduce, sub-motivo de la 003, negativo con entrada AGNÓSTICA y positivo de la regla a mano (azar más 0,10).

## 4. Evidencia cruda (verbatim)

Comandos en brain-env:

```text
git clone -q --branch titan/tarea-mosca-2026-10-12 https://github.com/gatehot59-star/drosophila-fep-connectome.git clon
3bc1a5568610943b0ded157a16381581f0e2cc21
4984acd1cb856bd5d3c5169868b904fb  tools/escape_aterrizaje/tarea_mosca.py
nohup python3 tools/escape_aterrizaje/tarea_mosca.py --conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv --out /workspace/tm_2026-10-12/humo --humo > /workspace/tm_2026-10-12/humo.log 2>&1 &

git pull -q
57d094a4abcaae2e5e28a219de8d6701206e8699
40d64e074d9163753439307c5be4ac5e  tools/escape_aterrizaje/tarea_mosca.py
nohup python3 tools/escape_aterrizaje/tarea_mosca.py --conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv --out /workspace/tm_2026-10-12/humo2 --humo > /workspace/tm_2026-10-12/humo2.log 2>&1 &
```

Humo 1 (`humo1.log`, md5 `5c27e41baba0542f43299d5d6efef598`, 97 líneas), las dos celdas que motivaron el cambio (recortadas a 120 caracteres; el séptimo valor de `por_condicion` es el looming frontal en vuelo):

```text
CELDA A=0.0 ruido=0.15 W=0.8400 por_condicion=1.000,1.000,0.700,1.000,1.000,0.950,0.075,0.875,1.000,0.800 umbrales=0.304
CELDA A=0.3 ruido=0.15 W=0.8200 por_condicion=1.000,1.000,0.475,1.000,1.000,0.950,0.075,0.900,1.000,0.800 umbrales=0.629
RIVAL A=0.3 ruido=0.15 regla_a_mano=0.8050 por_condicion=1.000,1.000,0.475,1.000,1.000,0.925,0.025,0.975,0.950,0.700 | H3 W contra regla 22 contra 16 p=0.418 -> EMPATE | ridge_crudo_entrenado(descriptivo)=0.9875
CHEQUEO INSTRUMENTO guarda_SL=True guarda_T=True reproduce_003=True reproduce=True control_negativo=True control_positivo=True -> VALIDO
# duracion_s=180.0
EXIT_RUN=0
```

Humo 2 (`humo2.log`, md5 `f7dc968c75f16aa75eee1f1fe7e27d95`, 97 líneas; se omiten las 46 líneas `MOTIVO root_id=...`):

```text
# maquina: 6c09d8604b07 | Linux-4.19.0-27-amd64-x86_64-with-glibc2.41 | Python 3.12.14 | numpy 2.5.3 | pandas 3.0.5
# md5 script = 40d64e074d9163753439307c5be4ac5e
# md5 modulo 003 = 4d40477d87406c31672acfb6e6e8f5a2 | md5 modulo 005 = e060c4bffb685aa550dadc19eda3dd02
# fecha: 2026-10-13 00:26:18 +0000
# md5 conn = 3d802fd542b5d18570ba1ba0bb0abed9 | md5 annot = 719904abad876c68ace1b5690c9b9b63
# HUMO: corrida corta, estos numeros no valen
MOTIVO neuronas=46 visuales=40 aristas=187 sinapsis=1149 inhibitorias=0 ipsilaterales=187 rho_crudo=22.9733
MOTIVO tipo=LC4 por_lado=(4,4)
MOTIVO tipo=LPLC2 por_lado=(8,8)
MOTIVO tipo=LPLC4 por_lado=(4,4)
MOTIVO tipo=LPLC1 por_lado=(4,4)
COMPOSICION dn=DNp01 lado=left sinapsis_desde={'LC4': 54, 'LPLC2': 63, 'LPLC4': 0, 'LPLC1': 0}
COMPOSICION dn=DNp01 lado=right sinapsis_desde={'LC4': 61, 'LPLC2': 74, 'LPLC4': 0, 'LPLC1': 0}
COMPOSICION dn=DNp07 lado=left sinapsis_desde={'LC4': 1, 'LPLC2': 0, 'LPLC4': 169, 'LPLC1': 0}
COMPOSICION dn=DNp07 lado=right sinapsis_desde={'LC4': 0, 'LPLC2': 0, 'LPLC4': 138, 'LPLC1': 0}
COMPOSICION dn=DNp06 lado=left sinapsis_desde={'LC4': 9, 'LPLC2': 72, 'LPLC4': 0, 'LPLC1': 79}
COMPOSICION dn=DNp06 lado=right sinapsis_desde={'LC4': 10, 'LPLC2': 78, 'LPLC4': 0, 'LPLC1': 65}
CHEQUEO REPRODUCE_003 neuronas=True aristas=73 contra 73 -> True
NULOS SL=3 guarda=True T=3 guarda=True
DATOS entrenamiento=600 prueba=400 clases_prueba(nada,despegar,aterrizar,girar_der,girar_izq)=160,80,80,40,40 azar_mayoria_por_estado=0.5000 FA_por_linea=0.05
ORDEN por_condicion = posada(LOOM_LATERAL,LOOM_FRONTAL,PUNTO,BARRA,NADA) | vuelo(LOOM_LATERAL,LOOM_FRONTAL,PUNTO,BARRA,NADA)
CELDA A=0.0 ruido=0.15 W=0.9025 por_condicion=1.000,1.000,0.700,1.000,1.000,0.925,0.950,0.700,0.975,0.775 umbrales=0.304,0.367,0.224,0.294,0.219,0.200 | SL media=0.6833 max=0.6975 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | T media=0.7283 max=0.7375 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | 28.6 s
RIVAL A=0.0 ruido=0.15 regla_a_mano=0.9225 por_condicion=1.000,1.000,0.925,0.875,0.900,0.925,0.950,0.875,0.975,0.800 | H3 W contra regla 22 contra 30 p=0.332 -> EMPATE | ridge_crudo_entrenado(descriptivo)=0.9875
CELDA A=0.0 ruido=0.45 W=0.8950 por_condicion=1.000,1.000,0.850,0.900,0.975,0.900,0.975,0.700,0.925,0.725 umbrales=0.425,0.494,0.505,0.620,0.533,0.465 | SL media=0.6442 max=0.6475 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | T media=0.7267 max=0.7425 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | 55.0 s
RIVAL A=0.0 ruido=0.45 regla_a_mano=0.9000 por_condicion=1.000,1.000,0.975,0.925,0.900,0.875,0.950,0.600,0.975,0.800 | H3 W contra regla 27 contra 29 p=0.894 -> EMPATE | ridge_crudo_entrenado(descriptivo)=0.9475
CELDA A=0.3 ruido=0.15 W=0.8875 por_condicion=1.000,1.000,0.475,1.000,1.000,0.925,0.950,0.775,0.975,0.775 umbrales=0.629,0.715,0.224,0.294,0.219,0.200 | SL media=0.6442 max=0.6775 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | T media=0.6717 max=0.7075 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | 26.3 s
RIVAL A=0.3 ruido=0.15 regla_a_mano=0.9100 por_condicion=1.000,1.000,0.475,1.000,1.000,0.925,0.950,0.975,0.975,0.800 | H3 W contra regla 14 contra 23 p=0.188 -> EMPATE | ridge_crudo_entrenado(descriptivo)=0.9875
CELDA A=0.3 ruido=0.45 W=0.8775 por_condicion=1.000,1.000,0.500,1.000,1.000,0.900,0.975,0.750,0.925,0.725 umbrales=0.576,0.667,0.505,0.620,0.533,0.465 | SL media=0.6267 max=0.6425 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | T media=0.6775 max=0.7075 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | 29.0 s
RIVAL A=0.3 ruido=0.45 regla_a_mano=0.9050 por_condicion=1.000,1.000,0.775,0.975,0.950,0.875,0.950,0.750,0.975,0.800 | H3 W contra regla 22 contra 33 p=0.177 -> EMPATE | ridge_crudo_entrenado(descriptivo)=0.9525
CELDA A=0.6 ruido=0.15 W=0.8600 por_condicion=0.950,0.900,0.350,1.000,1.000,0.925,0.950,0.775,0.975,0.775 umbrales=0.776,0.864,0.224,0.294,0.219,0.200 | SL media=0.6033 max=0.6400 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | T media=0.5900 max=0.6325 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | 26.1 s
RIVAL A=0.6 ruido=0.15 regla_a_mano=0.9075 por_condicion=1.000,1.000,0.450,1.000,1.000,0.925,0.950,0.975,0.975,0.800 | H3 W contra regla 11 contra 30 p=0.00432 -> PEOR | ridge_crudo_entrenado(descriptivo)=0.9900
CELDA A=0.6 ruido=0.45 W=0.8675 por_condicion=0.950,1.000,0.450,1.000,1.000,0.900,0.975,0.750,0.925,0.725 umbrales=0.727,0.808,0.505,0.620,0.533,0.465 | SL media=0.5917 max=0.6325 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | T media=0.6175 max=0.6525 igualan=0/3 p_sup=0.2500 p_inf=1.0000 | 25.9 s
RIVAL A=0.6 ruido=0.45 regla_a_mano=0.9025 por_condicion=1.000,1.000,0.550,1.000,1.000,0.875,0.950,0.875,0.975,0.800 | H3 W contra regla 17 contra 31 p=0.0595 -> EMPATE | ridge_crudo_entrenado(descriptivo)=0.9525
CONTROL_NEGATIVO entrada=AGNOSTICA W=0.5725 T_identicos=3/3 -> True
CONTROL_POSITIVO regla_a_mano A=0.3 ruido=0.15 = 0.9100 contra azar 0.5000 + 0.10 -> True
DESCRIPTIVO LPLC1_SILENCIOSA A=0.3 ruido=0.15 W=0.8625 por_condicion=1.000,1.000,0.425,1.000,1.000,0.925,0.950,0.575,0.975,0.775 | regla=0.8600 por_condicion=1.000,1.000,0.475,1.000,1.000,0.925,0.950,0.475,0.975,0.800
DESCRIPTIVO LPLC4_SILENCIOSA A=0.3 ruido=0.15 W=0.7725 por_condicion=1.000,1.000,0.475,1.000,1.000,0.950,0.525,0.950,0.050,0.775 | regla=0.7425 por_condicion=1.000,1.000,0.475,1.000,1.000,0.925,0.075,0.975,0.175,0.800
CHEQUEO INSTRUMENTO guarda_SL=True guarda_T=True reproduce_003=True reproduce=True control_negativo=True control_positivo=True -> VALIDO
VEREDICTO_GLOBAL -> NO PAGA
escrito resultados.json md5=fa117d9bb9dbbc2ae2152e341b0328e2
# duracion_s=234.8
EXIT_RUN=0
```

Recomputable: `git checkout 57d094a && python3 tools/escape_aterrizaje/tarea_mosca.py --conn <parquet> --annot <tsv> --out <dir>` (con `--humo` para la corrida corta; sale con 2 si los datos o los módulos no son los del pin).

## 5. Propuesta (decide Abraham)

Correr la sellada tal cual, desde un clon fresco de `57d094a`, sin tocar nada. La 012, de tamaño parecido, tardó 36 minutos; esta tiene 46 neuronas en vez de 28, así que la duración queda NO MEDIDA.

## 6. Archivos

- `main`: este archivo.
- Rama `titan/tarea-mosca-2026-10-12`: `tools/escape_aterrizaje/tarea_mosca.py` (sello `57d094a`).
- brain-env, sin commit (derivados de humo): `/workspace/tm_2026-10-12/humo1.log` (md5 `5c27e41baba0542f43299d5d6efef598`), `humo1/resultados.json` (`b2c19a0bb78d97cec7e683be74400a2f`), `humo2.log` (`f7dc968c75f16aa75eee1f1fe7e27d95`), `humo2/resultados.json` (`fa117d9bb9dbbc2ae2152e341b0328e2`).
- ClickUp: Doc público https://app.clickup.com/90171457413/docs/2kza6fw5-21577.

## 7. NO MEDIDO

- La corrida completa (300 SL, 300 T, 2.400 ensayos de entrenamiento y 2.000 de prueba).
- Las sintonías reales de LPLC1 y LPLC4, la razón 0,5 de dirección de LPLC2 y los factores 0,3 de LPLC4: supuestos.
- La inhibición: el motivo sigue con 0 aristas inhibitorias (la 011 midió que el 43,4% de la entrada de DNp01 y DNp07 es inhibitoria).
- Un lector entrenado sobre las 6 descendentes; una segunda máquina.
- CONTEXTO sin reescribir: de la 011 a la 015 vive en sus respuestas.

## Antes de firmar

```text
"el instrumento quedó sellado antes de correr" → commit 57d094a y md5 en el clon         → podía dar rojo: SÍ (md5 distinto)        → bien, 40d64e07 en sandbox, git y brain-env
"el instrumento es VALIDO"                    → controles del propio script en el humo 2 → podía dar rojo: SÍ (humo 1 lo mostró con el frontal) → VALIDO
"contiene exacto el motivo de la 003"         → comparación de ids y aristas con el módulo de la 003 → podía dar rojo: SÍ → True, 73 contra 73
"el cambio no se eligió por el resultado"     → se hizo por un control que fallaba en W y en la regla igual → podía dar rojo: parcial (lo decidí viendo el humo) → declarado
"el cableado paga con la tarea de la mosca"   → nada corrido a escala                    → podía dar rojo: NO                     → NO MEDIDO
```

--- METODO PROMETEO ---
Acción delicada: NO
Máquina: brain-env (clon fresco de la rama; humo 1 180,0 s y humo 2 234,8 s, EXIT_RUN=0, VALIDO) + sandbox de ClickUp + GitHub
Artefactos: docs/agents/respuestas/2026-10-12-015-tarea-de-la-mosca-sellada-con-dnp06-y-giro-bilateral.md + https://app.clickup.com/90171457413/docs/2kza6fw5-21577
