# Anatomía R65D11 medida a escala física

**Doc público asociado:** [Anatomía R65D11 medida: stacks confocales calibrados, mapping ROI todavía bloqueado](https://app.clickup.com/90171457413/docs/2kza6fw5-18837)

## 1. Pedido

Medir la anatomía disponible del experimento R65D11, sin convertir la petición en una inferencia de identidad para `ROI_0` o `ROI_1`.

## 2. Fuente y herramientas

Se usó el dataset público [Confocal images, DOI 10.7910/DVN/KTQT27](https://doi.org/10.7910/DVN/KTQT27), licencia CC0 1.0. La metadata LSM se leyó en `brain-env` con `tifffile`; la herramienta reproducible quedó en `tools/h4_anatomy_measure.py` y sus tres tests pasaron.

## 3. Medición obtenida

- **Brain 40x:** `352×2×1024×1024` (`ZCYX`), voxel `0.142084×0.142084×0.330 µm`, campo físico `145.494×145.494×116.160 µm`.
- **VNC 40x:** `353×2×1024×1024` (`ZCYX`), voxel `0.312585×0.312585×0.330 µm`, campo físico `320.087×320.087×116.490 µm`.
- Objetivo en ambos: `Plan-Apochromat 40x/1.3 Oil DIC M27`.
- Adquisiciones: `20201130-1-R65D11-FlpPEST-MCFO-40x-brain` y `20201130-1-R65D11-FlpPEST-MCFO-40x-VNC`.

Esto es anatomía cuantificada de la muestra de la línea R65D11, con escala espacial calibrada. No es todavía el mapping de la señal funcional.

## 4. Evidencia cruda verbatim

```text
brain40: pages=704
brain40: series=[((352, 2, 1024, 1024), 'ZCYX'), ((352, 3, 128, 128), 'ZSYX')]
brain40: VoxelSizeX=1.4208402876414194e-07 m
brain40: VoxelSizeY=1.4208402876414194e-07 m
brain40: VoxelSizeZ=3.3e-07 m

vnc40: pages=706
vnc40: series=[((353, 2, 1024, 1024), 'ZCYX'), ((353, 3, 128, 128), 'ZSYX')]
vnc40: VoxelSizeX=3.1258486328111226e-07 m
vnc40: VoxelSizeY=3.125848632811123e-07 m
vnc40: VoxelSizeZ=3.3e-07 m

Ran 3 tests in 0.001s
OK
```

MD5 publicados por Dataverse: brain 40x `fbc4635cbddfe512057ca1bfe8044348`; VNC 40x `88d30a04b95768918cbabf510a77d8be`. Tamaños exactos: `755716276` y `757912760` bytes.

## 5. Archivos commiteados

- `tools/h4_anatomy_measure.py`.
- `tests/test_h4_anatomy_measure.py`.
- `docs/agents/evidencia/2026-10-03-006-r65d11-confocal-anatomy-geometry.json`.
- Este archivo de respuesta.
- [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18837).

## 6. Veredicto honesto

**BIEN:** la anatomía confocal pública está medida a escala física, separando cerebro y VNC. **NO MEDIDO:** segmentación volumétrica completa por canal, bounding box de fluorescencia, transformación confocal→2P, correspondencia funcional de `ROI_0`/`ROI_1`, región real, `root_id`, causalidad y null anatómico biológico.

La anatomía existe y ya está cuantificada. Lo que sigue bloqueado es la identidad de las dos trazas funcionales, porque el confocal corresponde a otra adquisición y no trae la transformación necesaria.

--- METODO PROMETEO ---
Accion delicada: NO
Modo aplicado: ANDROMEDA + BITACORA-EN-GIT
Rubrica: N/A (medición de geometría anatómica, sin inferir mapping funcional)
N/A declarados: deployment, producto, causalidad y merge no aplican
Review externo: no solicitado; silencio no es aprobación
Instrumento: `tifffile` sobre headers LSM en `brain-env`; tests 3/3; evidencia cruda commiteada
Maquina: brain-env + GitHub API + navegador público
Artefactos: `tools/h4_anatomy_measure.py` + `tests/test_h4_anatomy_measure.py` + `docs/agents/evidencia/2026-10-03-006-r65d11-confocal-anatomy-geometry.json` + este archivo + [Doc público](https://app.clickup.com/90171457413/docs/2kza6fw5-18837)
NO MEDIDO: segmentación completa, mapping ROI→anatomía, root IDs, causalidad y null anatómico