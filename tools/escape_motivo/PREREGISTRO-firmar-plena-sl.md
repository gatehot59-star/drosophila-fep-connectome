# Pre-registro: firma de la 014 con más redes SL y más semillas (firmar_plena_sl.py)

**Sellado antes de entrenar:** `tools/escape_motivo/firmar_plena_sl.py`, md5 `df15f3da3ed27fba262c5733dc92fc6a`. El archivo entero se commitea con los resultados; si su md5 no es este, la corrida no vale.

**Base:** importa `control_plena.py` (md5 `45bad2a8…`, la 014) y su cadena (013, 012, 011). Protocolo exacto de la 012 y la 014: LIQ_PLENA, 40 iteraciones × 8 pares, σ 0,10, lr 0,05.

**Qué se agrega:**

- 45 redes SL nuevas (k = 24 a 68), entrenadas con semilla 0. Las 24 de la 014 se leen de su `resultados.json` (md5 `f2792e6a…`); total 69.
- 7 semillas más de la mosca (1 a 7); la semilla 0 se lee de la 014. Total 8.

**Reglas:**

- Validez y guardas: las de la 014; SL nuevas con radio 0,9, distintas de W y distintas entre sí.
- REPRODUCE: W semilla 0 = 0,9802 (leído); semillas 1, 2 y 3 = 0,9844, 0,9812 y 0,9844 (las de la 012).
- **Q1 (primario):** W semilla 0 contra las 69 SL, p = (1 + #{SL ≥ W}) / 70; W GANA si p < 0,05.
- **Q2 (estricto):** la peor de las 8 semillas de W contra las 69 SL, misma regla.
- **Q3 (descriptivo):** cuántas SL igualan a cada semilla; Mann-Whitney unilateral de las 8 W contra las 69 SL.
- **VEREDICTO_FIRMA:** FIRMADO si Q1 y Q2 dan W GANA; SOLO LA SEMILLA 0 si gana Q1 y no Q2; NO SE SOSTIENE si Q1 no gana.

**Humo** (sólo controles y guardas): C+L 0,8125 / 1,0; C+6 rechazo 0,0; C0 0,0; VALIDO; json de la 014 OK; 69 SL distintas.
