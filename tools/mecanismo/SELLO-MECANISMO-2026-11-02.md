# SELLO-MECANISMO-2026-11-02 · H_MECANISMO: cortar y restaurar el motivo S→D + S→X→D en el LIF de Shiu

Respuesta: 2026-11-02-002. Rama: titan/mecanismo-2026-11-02, sin merge.
Doc: https://app.clickup.com/90171457413/v/dc/2kza6fw5-26157
Sellado antes de CORRER. Lo que se mide es causalidad DEL MODELO de Shiu et al. 2024 (LIF sin actividad de fondo, un solo tau de 5 ms para excitación e inhibición, signo por neurotransmisor predicho), no causalidad en la mosca.

## Pregunta

En el patrón que sostuvo H_REUSO_CIERRE (S visual → D descendente directo, más S → X → D con X inhibitoria compartida), ¿X reclutada por S frena a D en el modelo, y lo hace por el tramo S→X→D y no por un desvío?

## Instrumento (cada trabajo de CORRER exige estos sha256 con sha256sum --check)

85ce6bfc40266c5f7983c21580aea38aa56a9de8652fc7a5b851a2c6cbcdb553  tools/mecanismo/intervenir.py
e0567fd520ed92165ae73ad23efa52d49dba8dd89f91ddc65ddffc4ae67a5c45  tools/mecanismo/agregar_mecanismo.py
e51af3d4e193d8fbb587cf52efb23084d1bbcf78decaa5e1a99e84d329645b4d  tools/mecanismo/conjuntos.py
b604af62e053cacded85979002b34d70ca104d5399cfba1b8135a6626bf784eb  tools/mecanismo/paso12.py
82177a9daa55587519bed359eb6fd8eec6dd21d716173838edd4c5cdb6de1bf9  tools/mecanismo/prueba_mecanismo.py
3650fc74967e35ec7fcd407964049ea91c3483b2a195790736dd2bfe58656f7d  tools/reuso/reuso_mosca.py
fe96c5c0673a3db75cb06d2d864677f070bf87d0cc58390a713e4aabdd5c79db  .github/workflows/mecanismo-correr.yml
e499bfc5dfbc2af9daf944d8005bcfe52df8bad57c7f153b160b35e8f644dac9  .github/workflows/mecanismo-prueba.yml

- Modelo: philshiu/Drosophila_brain_model@91bdd1e7dcf193f3e7ca5a8933497fcef63b7960, model.py blob 5ba7083cf55bf6092967f8d9065e86cd677efed1, sha256 fc45837d7122c6ce2a7f3f2f23c515992e4b232aadb919efabb72337fac88e4e, sin cambios: create_model() y poi() tal cual, default_params salvo r_poi, n_run y t_run.
- Entorno: Actions ubuntu-24.04, Python 3.12.14, brian2 2.10.1, cython 3.1.3, joblib 1.6.0, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, pyarrow 25.0.1.
- Datos: Connectivity_783.parquet md5 3d802fd542b5d18570ba1ba0bb0abed9 (sha256 efeb23fb…); Completeness_783.csv md5 031a4b6eac490bda17c75b65ccaa7906; anotaciones flywire_annotations@17fc5772 sha256 9a4f8b2f…; BANC 888 meta 86ccf5df… y aristas 8c296e94….
- Conjuntos: conjuntos_flywire.json sha256 f3e8602a6bcf3daefc3b83965f7793a2648f59a22bf8df6209d09ed19e0a3c2d, 80.557 bytes. El censo de Actions lo reproduce antes de medir; si no da igual, no se mide.

## Conjuntos (Paso 1, MEDIDO en anatomía)

| Estímulo | S | D (unidades) | X | X glutamatérgicas |
|---|---|---|---|---|
| LC4_right | 50 | 10 (10) | 49 | 8 |
| LC4_left | 54 | 11 (11) | 45 | 7 |
| LPLC2_right | 102 | 14 (14) | 27 | 4 |
| LPLC2_left | 108 | 15 (15) | 25 | 3 |
| LPLC1_right | 72 | 7 (7) | 32 | 3 |
| LPLC1_left | 68 | 7 (7) | 34 | 2 |
| LPLC4_right | 54 | 21 (19) | 83 | 34 |
| LPLC4_left | 56 | 23 (21) | 95 | 31 |

S: las neuronas de la unidad visual. D: las de las unidades descendentes con plantilla (S→D ≥ 20 sinapsis y al menos una X). X: inhibitorias con ≥ 5 sinapsis S→X y ≥ 5 X→D en alguna plantilla.

## Condiciones (ediciones de pesos antes de correr; silenciar con máscara es idéntico a silence() de Shiu, probado)

- C0 intacto. C1 silenciar X. C2 cortar S→X. C3 cortar X→D. C4 cortar S→D.
- R1: X conserva solo X→D. R2: X recibe solo desde S. R3: S conserva solo S→D. R4: S conserva solo S→D y S→X.
- M5: las sinapsis X→D de X glutamatérgicas pasan a excitatorias (contrafáctico del signo).
- K: silenciar inhibición fuera del motivo, reclutada y emparejada. Pool: inhibitorias con ≥ 5 sinapsis sobre D, fuera de S, X y D. Impulso efectivo = espigas medias en C0 × sinapsis sobre D. Se toman en orden descendente (empates por índice) hasta igualar el impulso de X.

## Celdas (17) y muestreo

- Principales: lado derecho a 50 Hz, LC4, LPLC2, LPLC1 y LPLC4, las 11 condiciones, 20 ensayos.
- Tasas: 20 y 150 Hz, C0 y C1, 20 ensayos (8 celdas).
- Réplica izquierda: 50 Hz, C0 a C4, 20 ensayos (4 celdas).
- ctrl_mn9: azúcar a 100 Hz, 10 ensayos; pasa si MN9 dispara en ≥ 9.
- T = 1000 ms. Semilla brian2.seed(20261102 + t) en el ensayo t, igual en todas las condiciones (números aleatorios comunes).

## Pruebas y veredicto (reglas fijas)

- Lectura: D = suma de espigas de las neuronas D por ensayo.
- P1 C1 > C0; P2 C2 > C0; P3 C3 > C0; P4 C0 > C4. Diferencia pareada por semilla; p bilateral por permutación de signos, B = 99.999, semilla 2026110200 + 4i + t; Holm sobre las 16; pasa si p_Holm < 0,05 y la media va en la dirección predicha.
- INVALIDO ante cualquier guarda: pin, control MN9 fallido, celda faltante, C0 a C4 incompletas, corte vacío en C2, C3 o C4, X no inhibitoria, techo (tasa media de D ≥ 400 Hz en C0 o C1) o piso (C0 y C1 suman 0).
- REFUTADO si P1 no pasa. SOSTENIDO_EN_MODELO si pasan P1 a P4 y ΔSX/ΔX ≥ 0,5 y ΔXD/ΔX ≥ 0,5. PARCIAL en otro caso.
- Global: INVALIDA con ≥ 2 INVALIDO; SOSTENIDA_EN_MODELO con ≥ 3 SOSTENIDO y ningún REFUTADO; REFUTADA con ≥ 3 REFUTADO; MIXTA en otro caso.

## Descriptivos (sin veredicto)

Restauración f_R1 y f_R2 = (D1 − DR)/(D1 − D0), f_R3 y f_R4 = DR/D0; efecto de K y K/X; delta de M5; descendentes fuera del objetivo en C0 contra C1 (permutación, semilla 2026110300 + i) y los tipos que más cambian; latencia y fracción de espigas de D en los primeros 50 ms; huella de S para los números comunes; lectura de tasas con rel = (D1 − D0)/D1: SUSTRACTIVA si rel150 < 0,5·rel20, DIVISIVA si |rel150 − rel20| ≤ 0,5·rel20, OTRA en el resto; réplica izquierda con p crudos (semilla 2026110250 + 4i + t).

## Mecanismos rivales y qué predice cada uno aquí

- M0 subproducto estructural: X no frena a D (P1 falla).
- M1 control de ganancia por inhibición de avance: P1 a P4 pasan y R4 reproduce C0 (f_R4 cerca de 1).
- M2 ventana temporal: necesita taus distintos; con un solo tau queda poco testeable, solo latencia y fracción temprana como pista.
- M3 selección entre acciones vía X compartidas: silenciar X sube también descendentes fuera del objetivo; K emparejado hace menos que X (K/X < 1).
- Compuerta de contexto: X impulsada sobre todo por el cerebro central; en el modelo, ΔSX/ΔX < 0,5 y f_R2 bajo.
- M4 compuerta de estado por la ascendente AN_multi_11: NO MEDIBLE acá (truncada en FlyWire, sin fondo).
- M5 glutamato excitatorio: si fuera cierto, la inhibición del motivo se achica; acá solo contrafáctico.

## Apuestas (antes de ver)

1. P1 pasa en los cuatro estímulos (confianza 0,7).
2. Global SOSTENIDA_EN_MODELO (0,5); la alternativa más probable es MIXTA por ΔSX/ΔX < 0,5 en LPLC4, donde las X son muchas y reciben poco de S directo.
3. K/X ≥ 0,5 en al menos tres estímulos: la inhibición emparejada fuera del motivo hace algo parecido; en el modelo la identidad de X pesa menos que su impulso sobre D (0,6).
4. Silenciar X sube los descendentes fuera del objetivo con p < 0,05 en al menos tres estímulos (0,6).
5. Lectura de tasas SUSTRACTIVA en al menos tres (0,55): el modelo suma corrientes, no conductancias.
6. M5 en LPLC4_right supera a C1 (34 de 83 X son glutamatérgicas) (0,55).

## Exposición previa

Solo anatomía (Pasos 1 y 2, en brain-env y reproducidos en Actions, run 41408632528), la red sintética de la prueba (48/48 PASS en brain-env con numpy y en Actions con cython) y el cronómetro: ctrl_mn9 con 3 ensayos (azúcar → MN9, 55 a 57 espigas, 33,4 s por tanda de 3, RSS máximo 2,97 GB). Ningún ensayo con S del motivo ni lectura de D del motivo se corrió antes de este sello.

## NO MEDIDO (esto no lo mide)

Causalidad en la mosca; el signo real del glutamato; la compuerta por AN_multi_11; la ventana temporal; la formación del cableado (linaje, geometría); BANC en simulación; actividad de fondo; plasticidad.

## Reglas ante problemas

Una celda que falla o se corta queda faltante y el agregado aplica las guardas. No se relanza para mejorar un resultado. Un relanzamiento por falla de infraestructura se declara y conserva el run fallido. El workflow se niega a correr si ya hay resultados.
