# 2026-11-03-003 · Runner 009-A1 arrancado y corrección de sección 15

## Pedido
Arrancar el runner de 009-A1 y corregir la sección 15 del Doc maestro de Topo inverso.

## Herramientas declaradas
Se leyó el estado vivo de `main`, la rama base de H_MECANISMO_DNp04, el sello 009, la enmienda 009-A1, `model.py` de Shiu y los workflows previos. Se creó la rama `titan/a1-runner-2026-11-03`, se ejecutaron fixtures en brain-env y se disparó un humo controlado en GitHub Actions. No se inició la corrida grande de 16 relevos.

## Qué se midió
El runner quedó separado en primitivas de semilla/eventos, constructor de manifiesto, productor de recibos y fixtures. Los fixtures dieron **5/5 PASS**: semilla de 64 bits sin truncamiento, eventos Bernoulli conocidos, replay de 50 ticks únicos, máscara vacía y pareado de entradas. La semilla B_R01/0/59804/driver fue `5428794271745577241`; sus primeros eventos fueron `[58,419,473,835,989,1158]`. El smoke de Actions debe producir el manifiesto antes de generar actividad y guardar su huella.

## Evidencia cruda verbatim
```text
PASS seed_64bit
PASS events_known_answer
PASS replay_unique
PASS empty_mask
PASS paired_input
A1_FIXTURES PASS
```

Huellas locales de la implementación: `comun_a1.py` `3dad41c68b900c538cad0ab6deb01a2dea6626c928892232e6b593bc3ed27f23`; `manifiesto_a1.py` `e323c201c969897ec638c672dea4cd734cfcfb33c7f617d17315135466c4e3b4`; `runner_a1.py` `be17b25b83881fbdd11ca8ef2d19dc467430f0e9f925072a01882ce7990c796c`; `prueba_a1.py` `5854ee745a9496b7fe8d8ed2c16d309047509c608a725dca9ac28c0f1c675ed8`; workflow `c788b4be5556dbf586d311b618d7717bd10cafaa9eeb311e5f42c69a8917c597`.

## Archivos generados
Código y workflow en la rama [titan/a1-runner-2026-11-03](https://github.com/gatehot59-star/drosophila-fep-connectome/tree/titan/a1-runner-2026-11-03). El commit de implementación es `73cc060b05b7937b08fe14378002adb03b274f2a`; el disparo del humo es `7ffe6356bb0199f30d33522cf9c04c6ddac6e353`.

## Corrección exacta para sección 15
La edición directa del page de ClickUp fue rechazada por una protección de contenido: escribirlo eliminaría contenido existente. Por eso no voy a fingir que quedó corregida. Reemplazá el párrafo de la sección 15 por:

> H_REUSO_CIERRE quedó **SOSTENIDA** en ambos conectomas: en FlyWire, T1 fue `88,35 %` frente a una media nula de `49,66 %` (rango `45,88–52,61`) y T2 fue `698` frente a `286,04` (rango `257–326`); en BANC, T1 fue `82,60 %` frente a `35,01 %` (rango `30,94–37,98`) y T2 fue `419` frente a `76,515` (rango `57–95`). Los cuatro contrastes conservaron `p=1/201` y `p_Holm=0,0199005`. El recibo es `cierre.json` en `7f3cbc1b1ff2243149ba45d10c18abb4ce5311e4`; la transcripción anterior (`80,26 %`, `74,31 %`, `539,86`, `328,99`) era incorrecta.

El cambio corresponde a una corrección documental, no a una nueva corrida ni a la regeneración de los nulos.

## NO MEDIDO
No están medidos todavía: manifiesto producido por Actions, resultado del smoke de Actions, replay neuronal C completo, recibos corruptos contra un verificador independiente, nueva simulación A/B/C de los 16 relevos, estadística por familias, corrida grande ni causalidad biológica. El runner implementado en esta entrega es un arranque técnico, no habilita por sí solo la corrida confirmatoria.

--- METODO PROMETEO ---
Acción delicada: SI, nuevo workflow con escritura de resultados por bot; NO se hizo merge ni corrida grande.
Modo aplicado: FULL.
Máquinas: brain-env para fixtures y lectura; GitHub Actions x64 para el smoke disparado.
Instrumento: `tools/a1/prueba_a1.py`, exit 0, 5/5 PASS; el manifiesto queda sellado por el workflow antes del recibo smoke.
Independencia: el verificador independiente y la corrida funcional completa quedan NO MEDIDOS.
Artefactos: rama `titan/a1-runner-2026-11-03` + Doc `2026-11-03-003`.
--- FIN METODO PROMETEO ---
