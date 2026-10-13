# 2026-10-13-014 · F05 suavizado: la v2 del Paper 1 quedó lista para depositar; falta sólo el merge y el token

## Veredicto

- **[MEDIDO] F05 suavizado** con `tools/v2/fix_v2_f05_2026-10-13.py` (`da4ace2d…`).
  - Son 9 reemplazos: resumen (2), lista de contribuciones, §3.7, discusión de las propiedades 1 y 3, conclusiones, cambio 16 nuevo y metadatos de Zenodo.
  - Lo aplicó el bot en Actions en `608bd41`. El manuscrito quedó en `a4d09d2c…`, el mismo md5 que en la prueba en brain-env.
- **[MEDIDO] El número no se tocó.**
  - El +14,8σ sigue en 10 lugares y la Tabla 8 queda igual (la fila de t = 195 la controla el script).
  - Cambian las frases: «survives the community-preserving control» y «requires specific wiring» pasan a «well above the mean of five community-preserving realizations», con «not reproduced» y *N* = 5.
- **[MEDIDO] Render PASS desde `608bd41`:**
  - manuscrito: 18 páginas, `6e849bf2…`, determinista;
  - erratum: igual, `05052e6e…`.
- **[MEDIDO] En el PDF (pypdf, anterior → nuevo):**
  - «survives the community» 2 → 0;
  - «requires specific wiring» 1 → 0;
  - «not reproduced» 0 → 4;
  - el cambio 16 aparece.
- **[MEDIDO] Verificación del depósito PASS** en un clon fresco de `e7fd359`, con el json `0ed096b5…`.
  - **Control negativo:** con el PDF anterior (`a22515e9…`) da `MD5_DISTINTO` y FAIL.
- **[CONCLUSIÓN] La v2 está lista.** Lo que falta es de Abraham: el merge del PR #27 y el token de Zenodo. Después vienen el borrador, la publicación y revocar el token.

## Pedido

Abraham, 13-oct 18:17: «Suaviza f05 y cerra v2».

## Herramientas y máquina

- **brain-env:**
  - prueba del parche sobre una copia de `e81a903`;
  - render de prueba;
  - clon de `608bd41`, render final con `render_v2.py` (pandoc 3.10.2, typst 0.15.0);
  - control de texto con pypdf (`chk2.py`, `825e8b13…`);
  - `depositar_v2.py --verificar` con su control negativo;
  - clon fresco de `e7fd359`;
  - prueba del parche del CONTEXTO.
- **Actions x64:** el workflow `aplicar-fix-v2-f05-2026-10-13.yml` aplicó el parche, commiteó en `608bd41` y se retiró.
- **GitHub MCP:**
  - en la rama del PR #27: el parche y el workflow (`49f8fe0`), y después el json y los logs (`e7fd359`);
  - este commit en main.
- **Lo que no se hizo:** ni Zenodo, ni token, ni merge.

## Evidencia cruda

```
# prueba en brain-env sobre copia de e81a903
da4ace2dc070ff8c85d1f673a264d0b4  fix_f05.py
ANTES docs/v2/paper1-v2.0.md 2fa575c41926fdc790cecbb5965ba2a1
ANTES docs/v2/zenodo-v2.0-metadata.json 375853474c9148e92aacdd0945b69e42
REEMPLAZO resumen, propiedad 1 apariciones=1
REEMPLAZO resumen, propiedad 3 apariciones=1
REEMPLAZO contribuciones, item 3 apariciones=1
REEMPLAZO seccion 3.7 apariciones=1
REEMPLAZO discusion, propiedad 1 apariciones=1
REEMPLAZO discusion, propiedad 3 apariciones=1
REEMPLAZO conclusiones, item 1 apariciones=1
REEMPLAZO cambio 16 apariciones=1
REEMPLAZO metadatos de Zenodo apariciones=1
DESPUES docs/v2/paper1-v2.0.md a4d09d2c345dca03faca4d9bccf236d7
DESPUES docs/v2/zenodo-v2.0-metadata.json 3c2b0b36f967b691b516a12111db5b70
PARCHE OK: 9 reemplazos (8 en el manuscrito, 1 en los metadatos); la Tabla 8 queda igual
# bot en Actions: 608bd41 docs(v2): suaviza F05 ... (log docs/v2/fix-v2-f05-2026-10-13.log, mismos md5)
# render desde 608bd41
PDF Mendieta2026_Paper1_v2.0.pdf 332607 6e849bf2caffa540165edd826df102ed paginas 18 determinista True
PDF Mendieta2026_Paper1_Erratum_v1.0.pdf 191172 05052e6e7e0dd79cee584c9d285b1b93 paginas 15 determinista True
VEREDICTO_RENDER PASS
# pypdf, anterior (deposito_013) -> nuevo (deposito_f05)
survives the community             viejo=2 nuevo=0
requires specific wiring           viejo=1 nuevo=0
It requires fine wiring            viejo=1 nuevo=0
shows that generic modularity      viejo=1 nuevo=0
not reproduced                     viejo=0 nuevo=4
well above the mean of five        viejo=0 nuevo=3
16. Post-stimulus amplification    viejo=0 nuevo=1
14.8                               viejo=10 nuevo=10
# verificacion, clon fresco de e7fd359
ARCHIVO Mendieta2026_Paper1_v2.0.pdf 332607 6e849bf2caffa540165edd826df102ed OK
ARCHIVO Mendieta2026_Paper1_Erratum_v1.0.pdf 191172 05052e6e7e0dd79cee584c9d285b1b93 OK
VEREDICTO_VERIFICAR PASS
# control negativo (json apuntando a deposito_013)
ARCHIVO Mendieta2026_Paper1_v2.0.pdf 330511 a22515e9e2e7bb02e8d3fd824217dfc7 MD5_DISTINTO
VEREDICTO_VERIFICAR FAIL
# parche del CONTEXTO (copia en brain-env)
e930ac6031caca0a77e3e9b02d80a016  parche.py | md5 antes afc914af… -> despues 9430de7b… PARCHE OK
```

## Archivos

- **Rama del PR #27:**
  - `tools/v2/fix_v2_f05_2026-10-13.py` (`49f8fe0`);
  - `docs/v2/paper1-v2.0.md`, `docs/v2/zenodo-v2.0-metadata.json` y `docs/v2/fix-v2-f05-2026-10-13.log` (bot, `608bd41`);
  - `docs/v2/archivos-deposito-v2.0.json`, `docs/v2/render-v2.0.log` y `docs/v2/verificar-v2.0.log` (`e7fd359`).
- **main:**
  - este archivo;
  - `tools/contexto/actualizar_contexto_2026-10-13-014.py` (`e930ac60…`);
  - `.github/workflows/contexto-2026-10-13-014.yml`.
- **PDF:** están en `/workspace/v2cierre_2026-10-13/deposito_f05/` de brain-env, referenciados por md5.

## NO MEDIDO

- **La Tabla 8 sigue sin reproducirse.** Se cambió cómo se la presenta, no se la midió.
- **El render sólo corrió en brain-env.** El parche sí corrió en Actions, con el mismo md5.
- **Merge, token, borrador y publicación.**
- **La revisión humana del inglés de las frases nuevas.**

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| Las frases firmes ya no están | asserts del parche y conteo pypdf | Sí: el parche aborta si queda una |
| El número y la Tabla 8 no cambiaron | assert de la fila t = 195 y conteo de 14.8 (10 → 10) | Sí |
| El depósito es este PDF | `--verificar` con md5 | Sí: con el anterior dio FAIL |
| Actions y brain-env aplican igual | md5 del manuscrito `a4d09d2c` en los dos | Sí |

```
--- METODO PROMETEO ---
Accion delicada: no (sin merge, token ni deposito)
Maquina: brain-env (prueba, render, verificacion) | Actions x64 (parche)
Artefactos: docs/agents/respuestas/2026-10-13-014-f05-suavizado-v2-lista-para-depositar.md + Doc de ClickUp 2026-10-13-014
```
