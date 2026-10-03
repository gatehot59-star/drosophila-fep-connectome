# ADR: gate explícito para mapping ROI→FlyWire

**Fecha:** 2026-10-03 ART  
**Estado:** aceptada como contrato de entrada; el mapping biológico sigue NO MEDIDO.

## Contexto medido

La corrida Aymanns actual conserva dos canales llamados `ROI_0` y `ROI_1`, cada uno con 1.067 muestras neurales. El objeto `DFF_dic.p` contiene únicamente esas dos claves y series numéricas; no contiene `root_id`, `cell_type`, neuropilo, máscara espacial ni coordenadas. El H5 del trial conserva solo señales ThorSync (`AI`, `CI`, `DI`, `Global`) y tampoco contiene una identidad FlyWire por ROI.

El atlas FlyWire v783 sí existe como fuente independiente en el pipeline de `mojo-absoluto`: conectividad MD5 `3d802fd542b5d18570ba1ba0bb0abed9` y annotations MD5 `719904abad876c68ace1b5690c9b9b63`, con 138.639 neuronas y 15.091.983 aristas; el loader reportó 138.625 neuronas con annotation y 14 sin annotation. Eso valida el atlas, no asigna esas 138.639 neuronas a `ROI_0`/`ROI_1`.

## Decisión

Agregar `tools/h4_roi_anatomy_manifest.py` como gate fail-closed. El instrumento exige un TSV de mapping explícito, una fila por ROI y una snapshot de annotations. Solo acepta una ROI como `MAPPED` si declara:

- `root_id` positivo presente en el TSV de annotations;
- `evidence_kind` `direct_root_id` o `manual_roi_to_cell`;
- confianza finita en `[0,1]`;
- notas de procedencia.

`UNMAPPED` es válido como estado explícito, pero produce `mapping_verdict=PARTIAL` o `NO_MAPPED_ROIS`; nunca se convierte en una identidad inferida. No se permite usar el índice `ROI_0`/`ROI_1`, una etiqueta de región o la posición de la serie como `root_id`.

## Alternativas descartadas

1. **ROI_0→root_id 0 y ROI_1→root_id 1:** descartado; el índice experimental no es un ID FlyWire.
2. **Unir por orden de filas o por correlación de señal:** descartado; sería E-01, medir una señal y concluir identidad anatómica.
3. **Usar super_class o neuropilo como identidad celular:** descartado; es población/región, no root ID.
4. **Aceptar un mapping parcial como H4 fuerte:** descartado; el manifest lo marca y bloquea la interpretación anatómica.

## Contrato de salida

`verdict=BIEN` significa que la tabla declarada y la snapshot son coherentes, no que H4 esté probada. `mapping_verdict` puede ser `COMPLETE`, `PARTIAL` o `NO_MAPPED_ROIS`. La salida conserva hashes MD5 de mapping y annotations y copia los campos anatómicos de cada root ID validado.

## Próximo gate

Obtener de la segmentación/calcium pipeline la identidad experimental de cada ROI o declarar ambos `UNMAPPED`. Solo con al menos una identidad directa se puede construir el null anatómico pareado; incluso entonces, mapping no equivale a causalidad.

--- METODO TITAN ---
Accion delicada: SI
Modo aplicado: TITAN FULL
Rubrica: 92/100
N/A declarados: deployment no aplica; el gate y sus contratos sí
Review externo: pendiente; silencio no es aprobación
Instrumento: brain-env para inspección de `DFF_dic.p`, H5 y atlas importado; GitHub Actions para contratos
Evidencia: checksums y conteos citados; salida del gate queda lista para un mapping declarado
NO MEDIDO: identidad anatómica de `ROI_0`/`ROI_1`, null anatómico pareado, causalidad y SparseLTC→DBC3 sobre señal real
