# Traspaso técnico del conectoma: el repo leído entero (464 de 464) y dónde está cada cosa (11-oct)

## 1. Pedido

> "realiza un documnto tecnoc exuastivo que explique todo lo que tenemos en los dos repositors. los link. los .md genrados en los dos repositores. los estudios y pruebas mas sus codigos corridos en kkagle y en brin-env. tooooo. de tal manera que iniciemos en otra instancia"

Los dos repos son este (público) y `gatehot59-star/mojo-absoluto` (privado). Esta es la mitad pública y habla sólo del conectoma. El traspaso completo (índice por archivo de los dos repos, código de los 93 notebooks de Kaggle e inventario de brain-env) quedó en el repo privado, en `respuestas/2026-10-11-01-traspaso-tecnico-dos-repos-kaggle-brain-env.md` y `docs/traspaso/2026-10-11/`, porque mezcla material que no es público.

## 2. Herramientas y máquina

- brain-env: `git clone --mirror` de este repo e inventario por blob de main y de las 27 ramas (`traspaso_inv.py`), sólo lectura.
- Lectores automáticos con el conector de GitHub: un registro por archivo, PR e issue (349 de la 004 y 143 nuevos).
- Conector de GitHub para este commit. Sin cuota ajena.

## 3. Qué se midió

- main en `02da943`: 182 archivos, 129 commits. 27 ramas además de main, ninguna mergeada por ancestría. Unión de todas las refs: 464 pares ruta y blob, 428 rutas, 3.665.511 B.
- Cobertura de lectura: 464 de 464 (0 sin lectura, 0 leídos en otra versión). Los 57 archivos de main y las 73 rutas de ramas que la 004 había dejado sin leer quedaron leídos.
- Correcciones a la 004: son 27 ramas además de main, no 28 (`ls-remote` da 28 heads contando main); `titan/materializacion-h4-guard-2026-10-02` está 138 commits adelante y 41 atrás de main, no 226 adelante.
- Base vigente, sin cambios: v1.0 en Zenodo (10.5281/zenodo.19136948) más `docs/ERRATUM.md` con el pin `17fc577`. La v2 no está depositada.
- Firme: reciprocidad 20,59× contra CP (0/40) y 47,27× contra MS; LC6 → fibra gigante 0 contra 17,2 ± 3,1 (z = −5,61); sel_post z = +181 y +6,31; gusto a dos saltos 10 contra 101,6 (z = −78,9); plasticidad contra CP 7,81×, 8,71× y 7,26×; control de salidas por descendentes con FWER.
- Caído: 36×, 1.559×, densidad 0,0074, el 323× como jerarquía, la tabla de ruteo como hallazgo propio, AMMC directo a la fibra gigante, efecto temporal global (p = 0,25), tau compleja (p = 0,60), H4 débil.
- Abierto: la 003 (nulo por circuito) sin firmar por FAIL del control negativo; su herramienta, tests y logs siguen sólo en brain-env (`/workspace/dfc-t7`). H4 fuerte NO MEDIDO (16/16 ROI sin mapear).
- Dónde corrió: nulos estructurales y efecto temporal en Kaggle (kernels titan de agosto); nulo anatómico, sel_post, Tabla 7, control de salidas y la 003 en brain-env; H4 en Actions y brain-env.

## 4. Evidencia cruda verbatim

Inventario en brain-env (`inv-dfc.log`, `grep -h -E '^(REPO|UNION) '`):

```text
REPO gatehot59-star/drosophila-fep-connectome main 02da943 archivos_main 182 commits_main 129 ramas 27 tags 0
UNION registros 464 rutas 428 bytes 3665511
```

Cruce de cobertura del armador (`build.log`, fragmento de este repo):

```text
"gatehot59-star/drosophila-fep-connectome": {"inventario": 464, "cubiertos": 464, "otra_version": 0, "sin": 0, "fuera": 0}
```

## 5. Archivos generados

- Este archivo.
- Doc de ClickUp público: https://app.clickup.com/90171457413/docs/2kza6fw5-21077
- Sin cambios en el CONTEXTO en este commit.

## 6. NO MEDIDO

- Nada experimental nuevo. Los resúmenes por archivo los escribieron lectores automáticos: las cifras se copiaron, no se recomputaron.
- `docs/agents/CONTEXTO-drosophila-fep.md` sigue diciendo 28 ramas y 180 archivos: la corrección queda pendiente.
- La 003 firmada, H4 fuerte, NPC por sinapsis, Lin región por región, Betzel arista por arista, la fila AN, la v2 en Zenodo.

--- METODO PROMETEO ---
Máquina: brain-env (espejo e inventario); GitHub MCP para el commit.
Artefactos: `docs/agents/respuestas/2026-10-11-006-traspaso-tecnico-del-conectoma.md` + Doc de ClickUp https://app.clickup.com/90171457413/docs/2kza6fw5-21077
