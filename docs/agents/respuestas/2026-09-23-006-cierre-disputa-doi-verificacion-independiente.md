# Cierre de disputa del DOI · verificación independiente

**Fecha:** 2026-09-23
**Sujeto:** `10.5281/zenodo.19136948`

## Instrumentos independientes usados

Se verificó desde una vía web distinta a la búsqueda indexada:

1. Resolución DOI: `https://doi.org/10.5281/zenodo.19136948`
2. Página pública de Zenodo: `https://zenodo.org/records/19136948`
3. API pública de Zenodo: `https://zenodo.org/api/records/19136948`

## Evidencia devuelta por la API

```text
id:              19136948
recid:           19136948
doi:             10.5281/zenodo.19136948
conceptrecid:    19136947
conceptdoi:      10.5281/zenodo.19136947
publication:     2026-03-20
version:         1.0
access_right:    open
status:          published
state:           done
submitted:       true
resource_type:   Preprint / publication
author:          Mendieta, Jorge Abraham
file:            Paper1_SignalPropagation (1).pdf
file size:       185471 bytes
file md5:        c7cb36a261182f6ce895057ebe26e505
```

La API además devuelve `self_html`, `doi`, `self_doi`, `files` y el enlace directo al PDF. El registro no está en estado draft ni restringido: aparece como `published`, `open`, `done` y `submitted=true`.

## Veredicto

La disputa queda **cerrada a favor de la existencia y accesibilidad pública de la v1.0**. La afirmación externa «el DOI no existe/no es públicamente verificable» es falsa. La formulación correcta es:

> El DOI v1.0 existe, resuelve y es público. Que un buscador no lo haya indexado no prueba inexistencia ni inaccesibilidad. La v2 corregida del erratum todavía no está depositada.

## Precisión importante

La página pública conserva el contenido original de v1.0, incluidos los números que el erratum corrige. Eso no invalida el DOI: es precisamente la versión histórica que debe seguir accesible. La corrección pendiente es publicar una nueva versión, no demostrar que la v1.0 existe.

## Resultado de la vía adicional

`api.crossref.org` no devolvió contenido para este DOI. Eso no contradice Zenodo: Zenodo es el registrador/repositorio del DOI y su propia API devolvió el registro completo. Crossref no es el endpoint autoritativo para cerrar este registro concreto.

## Enlaces verificables

- DOI: https://doi.org/10.5281/zenodo.19136948
- Registro: https://zenodo.org/records/19136948
- API cruda: https://zenodo.org/api/records/19136948
- PDF: https://zenodo.org/api/records/19136948/files/Paper1_SignalPropagation%20(1).pdf/content
- Concept DOI: https://doi.org/10.5281/zenodo.19136947

--- METODO TITAN ---
Accion delicada: NO. Se verificó una fuente pública y se documentó el resultado; no se publicó ni modificó Zenodo.
Modo aplicado: TITAN FULL
Rubrica: N/A (verificación puntual y cierre de disputa)
N/A declarados: código, testing de producto, deployment, seguridad e innovación; no aplican a resolver la existencia del DOI.
Review externo: la búsqueda del auditor queda contradicha por la API pública de Zenodo; no se interpreta el fallo de indexación como evidencia de inexistencia.
Instrumento: fetch web independiente sobre DOI, página Zenodo y API Zenodo; resultado crudo registrado arriba.
