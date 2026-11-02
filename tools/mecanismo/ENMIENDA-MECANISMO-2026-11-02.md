# ENMIENDA-MECANISMO-2026-11-02 · relanzamiento de H_MECANISMO por falla de infraestructura

Respuesta: 2026-11-02-002. Rama: titan/mecanismo-2026-11-02, sin merge.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-26157
Escrita antes de CORRER2. No cambia la pregunta, las condiciones, las semillas, las pruebas, los umbrales, las guardas, el veredicto ni las apuestas del sello SELLO-MECANISMO-2026-11-02.md, que queda fijado abajo con su sha256.

## Qué pasó en la corrida 1

- Run 41410027436, fuente 394334ed, evidencia conservada en results/mecanismo_2026-11-02/actions_correr (commit f323befc).
- Terminaron 9 de 17 celdas: ctrl_mn9 y las 8 de tasas (C0 y C1 a 20 y 150 Hz).
- Las 4 principales y las 4 de la réplica izquierda murieron con exit 143 (SIGTERM) entre 42 y 63 minutos; el paso de subir artefactos quedó salteado y no hay ni log ni JSON parcial de esas celdas.
- Veredicto de la corrida 1 con las reglas del sello: H_MECANISMO INVALIDA, por celdas faltantes. No hay veredicto científico.
- Causa probable, NO MEDIDA: memoria. El RSS máximo de un proceso subió con los ensayos por trabajador del pool reutilizado de joblib: 3,38 GB en ctrl_mn9 (unos 4 ensayos por trabajador) y de 4,48 a 5,80 GB en las celdas de tasas (unos 14). Una celda principal pide unos 73 por trabajador.

## Qué cambia

1. intervenir.py: cada ensayo corre en un proceso nuevo (multiprocessing spawn, maxtasksperchild=1) en vez del pool reutilizado de joblib. Cada ensayo ya construía su red desde cero y fijaba brian2.seed antes de correr; el cambio solo libera la memoria entre ensayos.
2. Cada celda principal se parte en p_E_right_a (C0, C1, C2, C3, C4, M5) y p_E_right_b (C0, R1, R2, R3, R4, K), para no acercarse al límite de 6 h por trabajo. K se elige con el C0 de _b, igual que antes con el C0 de la celda.
3. unir_celdas.py junta las mitades en celda_p_E_right.json y exige que los dos C0 sean idénticos ensayo por ensayo, con las mismas semillas, índices y pines. Si no, la celda sale con error y el agregado la trata como faltante.
4. Workflow nuevo mecanismo-correr2.yml: se dispara con CORRER2, escribe en actions_correr2 y exige estos sha256. El workflow de la corrida 1 no se toca.
5. prueba_mecanismo.py suma 6 chequeos: regresión contra la prueba previa (con procesos nuevos salen las mismas espigas que con joblib en la red sintética), unión correcta, rechazo de un C0 distinto, mitad _a sola, y agregado partido positivo y con C0 roto.

## Qué no cambia

agregar_mecanismo.py (mismo sha256 que en el sello), conjuntos.py, paso12.py, model.py de Shiu, datos, semillas 20261102 + t, condiciones, umbrales, guardas, Holm sobre 16, veredicto global y apuestas.

## Chequeo de reproducibilidad entre corridas (lo verifico yo al leer)

ctrl_mn9 y las 8 celdas de tasas vuelven a correr con las mismas semillas. Tienen que dar las mismas cuentas, ensayo por ensayo, que en la corrida 1. Si no, la corrida 2 se informa NO REPRODUCIBLE y no se firma veredicto.

## Exposición nueva desde el sello

Vi C0 y C1 a 20 y 150 Hz en los cuatro estímulos derechos. Silenciar X sube D en 20 de 20 ensayos en las 8 celdas (D1/D0 de 1,29 a 7,16; p exacto de signos 2/2^20 en cada una). Con eso, P1 a 50 Hz queda casi descontada y la apuesta 1 ya no informa. Lo informativo que queda: P2, P3, P4, los cocientes ΔSX/ΔX y ΔXD/ΔX, R1 a R4, K, M5, los descendentes fuera del objetivo y la réplica izquierda. La apuesta 5 (lectura SUSTRACTIVA en al menos tres) ya quedó resuelta con celdas completas de la corrida 1: 2 de 4, perdida. Las apuestas 2, 3, 4 y 6 siguen como estaban.

También vi que a 150 Hz los números aleatorios comunes no alcanzan para fijar S: en LPLC2 S dispara 9,75 % más al silenciar X (en el modelo, X también frena a S). A 20 Hz S queda igual.

## Instrumento (cada trabajo de CORRER2 exige estos sha256 con sha256sum --check)

e656d73eac31e4d955b0b78ec2345a65f67097de1c787f4617eb72048b699a2e  tools/mecanismo/intervenir.py
5c55328725e997457a701ff86e43eb38d33bfd0dde7e419165c1b68b4c28106b  tools/mecanismo/unir_celdas.py
e0567fd520ed92165ae73ad23efa52d49dba8dd89f91ddc65ddffc4ae67a5c45  tools/mecanismo/agregar_mecanismo.py
e51af3d4e193d8fbb587cf52efb23084d1bbcf78decaa5e1a99e84d329645b4d  tools/mecanismo/conjuntos.py
b604af62e053cacded85979002b34d70ca104d5399cfba1b8135a6626bf784eb  tools/mecanismo/paso12.py
1eda0695ec3dee0a8131bda29bbd9b02e3f4929ef585aaffb66134c226cb24e1  tools/mecanismo/prueba_mecanismo.py
3650fc74967e35ec7fcd407964049ea91c3483b2a195790736dd2bfe58656f7d  tools/reuso/reuso_mosca.py
ae904036f3862d447bacd0c8b512580cfd17694208e3b289e7c45ae2f337263f  tools/mecanismo/SELLO-MECANISMO-2026-11-02.md
dab498de4b2385541c22c0f4ac2d635afeace0a720193cd6d652fcaa207946ed  .github/workflows/mecanismo-correr2.yml
e499bfc5dfbc2af9daf944d8005bcfe52df8bad57c7f153b160b35e8f644dac9  .github/workflows/mecanismo-prueba.yml

## Reglas ante problemas

Las del sello. La corrida 1 no se borra ni se reescribe. Si la corrida 2 también falla por infraestructura, se informa y se busca otra vía, sin tocar reglas ni apuestas.
