# ADR: loader oficial H4 con manifest de alineación

## Estado
Aceptado para la rama de materialización. No autoriza interpretar H4 fuerte.

## Contexto
El pipeline anterior unió conducta y DFF por el entero `Frame`, aunque conducta tenía 54.000 frames y DFF 8.767/8.768 frames. Ese error retiró como evidencia biológica los resultados cross-animal y temporales. El procedimiento válido disponible reconstruye cámara y 2P desde ThorSync a 30 kHz.

## Decisión
`tools/h4_official_loader.py` es el punto de entrada para el primer manifest por trial. El loader:

1. reconstruye Basler y Frame Counter con el procedimiento ThorSync-equivalente;
2. genera segundos explícitos para cámara y 2P;
3. exige identidad coincidente de animal, trial y timebase;
4. rechaza cualquier join por `Frame`;
5. rechaza ROI truncadas o con longitudes mezcladas;
6. delega monotonicidad, duración, cobertura y gaps al alignment guard;
7. escribe provenance, conteos, ejes y veredicto `BIEN`/`MAL`.

## Alternativas descartadas

- Reusar `roi_dFF_2p.pkl` con `Frame`: fue el instrumento que produjo el error fatal.
- Interpolar con `behavior Frame / 100`: inventa la frecuencia conductual y no prueba equivalencia con ThorSync.
- Aceptar ROI cortas y truncar: esconder pérdidas convierte un dato incompleto en falso alineamiento.
- Usar nueve estadísticas globales como instrumento principal: borra identidad ROI, signo y anatomía; queda solo como control descriptivo.

## Evidencia real inicial

Trial 7, identidad `R65D11-tdTomGC6fopt-fly1`, dataset Aymanns:

- 7.469 pulsos Basler;
- 7.440 frames de cámara;
- 1.067 frames 2P/ROI;
- 7.440 etiquetas conductuales;
- duración neural 248,6562 s y conductual 247,9128 s;
- error relativo de duración 0,0029898;
- cobertura neural 0,9970102 y conductual 1,0;
- join `Time`, timebase `thor_sync_seconds`;
- 2 ROI, ambas de 1.067 muestras;
- manifest SHA-256 `8025aa0b966d4d358c8b108c23009f8b6501c6997dce36802d6310bfca542f36`.

## Consecuencia
El manifest de un trial es un artefacto verificable antes de construir features. `BIEN` demuestra alineación del instrumento, no selección contextual, causalidad ni generalización entre animales. Esos claims requieren nulls por bloques, mapping anatómico y silenciamiento.

## Criterio de éxito
Un trial real produce un manifest con `verdict=BIEN`, identidad completa, ejes monotónicos, cobertura suficiente, conteos y longitudes ROI. Un trial incompatible termina con `verdict=MAL` y exit code 2; no produce una corrida interpretable.

## Estado actual
Tests locales: 7 alignment + 6 loader, verdes. Mutación que desactiva el rechazo de DFF vacío: detectada; restauración: verde. CI del workflow queda como verificador limpio del PR.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: FULL
Maquina: brain-env para trial real; Actions x64 para contratos
Rubrica: N/A (ADR + instrumento + tests, sin deployment)
N/A declarados: seguridad de producto y deployment no aplican
Review externo: pendiente; silencio no es aprobación
Instrumento: loader ThorSync-equivalente, manifest, unittest y workflow; evidencia cruda en respuesta versionada
Artefactos: `tools/h4_official_loader.py` + `tests/test_h4_official_loader.py` + `.github/workflows/h4-official-loader.yml` + este ADR
