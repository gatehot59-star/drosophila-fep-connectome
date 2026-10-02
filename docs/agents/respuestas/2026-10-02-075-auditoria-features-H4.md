# Auditoría de las features H4: el problema principal estaba antes del modelo

## Veredicto
Sí: encontramos un problema grave en la etapa de construcción de features. El cross-animal y la estabilidad temporal anteriores **no pueden interpretarse como evidencia biológica** porque el runner usó `roi_dFF_2p.pkl` y lo cruzó con conducta por número de `Frame`, sin convertir el frame 2P a tiempo/frame conductual.

La discrepancia está medida:

```text
conducta: 54.000 frames, Frame 0..53.999
DFF roi_dFF_2p: 8.767/8.768 frames, Frame 0..8.766/8.767
DFF Time: 0..539,65 s
```

Al hacer `merge` por `Frame`, el runner emparejó DFF frame 0..8.766 con conducta frame 0..8.766. Eso toma aproximadamente los primeros 87,7 segundos de conducta, mientras asigna a esos mismos números los 540 segundos completos de DFF. Es un desfase temporal de aproximadamente 6,16×. El resultado anterior mide un emparejamiento incorrecto, no H4.

## Cómo se concibieron las features
La idea original era razonable como parche de comparabilidad: cada animal tiene un número y orden de ROIs distinto, por eso se colapsó la población neural por frame a nueve números:

- media
- desviación estándar
- mínimo y máximo
- mediana
- cuantiles 10%, 25%, 75% y 90%

Después se entrenó un clasificador con esas estadísticas. La intención era evitar comparar `ROI_17` de una mosca con `ROI_17` de otra sin saber si eran la misma neurona.

El problema es que ese parche borra justo la información que H4 necesita: qué neurona o ruta cambia, qué signo tiene, dónde está anatómicamente y qué módulo causal se puede silenciar. Sirve como sanity check de señal global, no como instrumento de rutas del conectoma.

## Auditoría por etapas

### 1. Elección de datos
Los cinco animales son útiles, pero se usó un trial por animal y no un conjunto equilibrado de sesiones. Los ROIs observados varían: 75, 79, 81, 86 y 95. Eso impide asumir identidad ROI común.

**Estado:** correcto para explorar; insuficiente para una afirmación de especie.

### 2. Elección del archivo neural
El runner usó `roi_dFF_2p.pkl`. El loader oficial de los autores, leído en vivo en `DN_population_analysis/utils.py`, carga `roi_dFF.pkl` para combinarlo con conducta; el loader R65D11 usa además interpolación explícita entre tiempos 2P y frames de cámara. Hay que repetir usando el asset oficial sincronizado, no el archivo 2P crudo.

**Estado:** elección del asset equivocada para el cruce directo.

### 3. Sincronización
Este fue el error fatal. Se unieron tablas por el entero `Frame`, aunque ambos relojes tienen distinta frecuencia. La conducta tiene 54.000 frames y el DFF 8.767 frames, pero ambos cubren aproximadamente 540 segundos. El cruce correcto debe usar `Time` del DFF y el tiempo de cámara/conducta, o `roi_dFF.pkl` ya sincronizado por el pipeline oficial.

**Estado:** rojo. Las conclusiones de cross-animal y estabilidad temporal quedan invalidadas como mediciones biológicas.

### 4. Construcción de features
Los nueve estadísticos de población son invariantes a la identidad ROI, pero no a:

- cantidad de ROIs, que varió 75–95;
- escala de fluorescencia entre animales;
- pérdida de un subgrupo funcional;
- signo o fase de la señal;
- distribución espacial/anatómica;
- dinámica temporal y latencia;
- conectividad y rutas.

`min` y `max` son especialmente sensibles a número de ROIs y outliers. La media puede cancelar subpoblaciones con signos opuestos. La feature no puede alimentar un silenciamiento anatómico porque ya destruyó la identidad de la ruta.

**Estado:** útil como control global después de corregir tiempo; inválida como proxy de SparseLTC/rutas.

### 5. Etiquetas
Las labels son predicciones DAART (`Prediction`), no una anotación manual independiente en este análisis. Hay fuerte desbalance entre walking, resting y grooming. `co2_off` también es un contexto amplio, no un estímulo único.

**Estado:** usable para screening, no suficiente para H4 fuerte sin bouts, contexto y controles.

### 6. Partición temporal
El split primera/segunda mitad evita mezclar frames entre mitades, pero se hizo después de filtrar labels y tomar stride 10. No es todavía un split por bout ni por trial. Los frames consecutivos tampoco son muestras independientes: la autocorrelación puede inflar o deformar accuracy.

**Estado:** control preliminar, no validación temporal definitiva.

### 7. Null y modelo
El shuffle de etiquetas se hizo en el entrenamiento, pero no preserva estructura temporal, bout length ni transiciones conductuales. Para datos de video/neural hay que usar shuffles por bloques/bouts y respetar el balance de clases. Balanced accuracy fue una buena elección; el null temporal necesita mejorar.

**Estado:** instrumento de screening, no falsador final.

## Qué queda invalidado
Quedan invalidados como evidencia biológica, aunque siguen siendo diagnósticos de código:

- cross-animal `0,1816` contra shuffle `0,2019`;
- estabilidad temporal `early_to_late` y `late_to_early`;
- la conclusión de que la feature no generaliza o no es estable.

No invalida el hallazgo H4 débil del conectoma real: ese fue otro instrumento, con perfiles cosine `0,999786–0,999845`, y sí respondió a su pregunta limitada.

## Corrección obligatoria

1. Rehacer el cruce con `roi_dFF.pkl` o la función oficial de carga, que ya trabaja en el reloj conductual.
2. Verificar explícitamente: número de frames, rango temporal, trial, animal, pérdidas y `Time` antes del merge.
3. Mapear ROIs/cell types a identidades comunes; si no existe mapping, declarar el resultado como señal global, no ruta.
4. Repetir cross-animal y temporal por bouts/trials, no por frames independientes.
5. Usar nulls por bloques temporales y balanceados.
6. Solo después probar SparseLTC real vs null anatómico y silenciamiento cruzado.

## Conclusión en criollo
No descubrimos que la biología sea inestable. Descubrimos que **le dimos al modelo dos relojes distintos y le pedimos que creyera que eran el mismo**. El camino conceptual sigue bien; esta corrida no sirve para interpretar H4. Primero se corrige el tiempo, después se diseñan features que conserven identidad anatómica.

## Fuentes
- Loader oficial Aymanns: https://github.com/NeLy-EPFL/DN_population_analysis/blob/main/DN_population_analysis/utils.py
- Recibo cross-animal anterior: `docs/agents/respuestas/2026-10-02-073-validacion-cross-animal-H4.md`.
- Recibo temporal anterior: `docs/agents/respuestas/2026-10-02-074-estabilidad-temporal-intra-animal.md`.

--- METODO TITAN ---
Accion delicada: NO
Modo aplicado: TITAN FULL
Rubrica: N/A (auditoría científica)
N/A declarados: deployment/security/CI no aplican; rerun corregido y mapping anatómico quedan pendientes
Review externo: no pedido
Instrumento: Git vivo, build.run sobre 5 behavior + 5 roi_dFF_2p, fuente oficial utils2p/loader leída en vivo
NO MEDIDO: asset roi_dFF sincronizado completo, rerun corregido, mapping ROI→FlyWire y falsación causal H4
