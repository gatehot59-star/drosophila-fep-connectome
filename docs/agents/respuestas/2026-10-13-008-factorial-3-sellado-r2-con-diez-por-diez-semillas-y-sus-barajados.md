# 2026-10-13-008 · Factorial 3 sellado: R2 con 10 × 10 semillas y contra 50 + 50 barajados, para decidir si de verdad supera a su diseño

## Veredicto

- **[MEDIDO] Sellado y sin disparar.**
  - Rama `titan/factorial3-mosca-2026-10-13`, sello `6a7b4cb`.
  - Verificado en un clon limpio:
    - `nulos_r2.py` `c4f1c4d3…`;
    - `agregar_factorial3.py` `2ec8cd03…`;
    - `factorial2_mosca.py` `798a824c…` (el sellado en el factorial 2, sin cambios);
    - workflow `243a2433…`, cuatro trabajos (ancla, grilla 60, nulos 20 y agregar).
  - No hay CORRER. La única corrida en la rama es un workflow ajeno (H4 integrated regression).
- **[MEDIDO] Humo en brain-env: 3 de 3 VÁLIDO.**
  - **REAL_IGUAL True:** el script de nulos mide el cableado real en 0,9750, igual que la grilla, así que los barajados corren por el mismo camino que lo que comparan.
  - **SL_IGUAL_MODULO True:** el barajado numpy da exactamente lo mismo que `base.barajar_sl` en R1 (91.484 aristas).
  - **Los guardas de un nulo SL y uno T dan True.** El SL cambia 4.030.551 destinos y conserva grados y lados; el T cambia 423 tipos y conserva la cuenta por lado.
  - **Los números no valen:** son 120 ensayos de entrenamiento y 80 de prueba.
- **[CONCLUSIÓN] Listo para Actions:** 81 trabajos, unas 4 h estimadas.

## Pedido

ClickKit `sellar_factorial3_007` (13-oct, 11:45): sellar el factorial 3, con R2 en 10 × 10 semillas y sus barajados.

## Diseño sellado

- **Grilla:** R2_CON_TASA con τ 0..9 × prueba 2..11 × 6 celdas, en 60 trabajos (uno por τ y celda), corrida con `factorial2_mosca.py` sin cambios. Son 600 corridas.
- **Nulos:** 50 SL y 50 T en la celda A 0,3, ruido 0,15, τ 0, prueba 2. Van en 20 trabajos de 5, cada nulo con semilla propia (`[7, k]` y `[11, k]`).
  - El SL permuta destinos dentro de cada bloque (lado pre, lado post), con fuente y peso fijos.
  - El T permuta los tipos sintonizados por lado, con el cableado real.
- **Primaria:** d = W menos la regla con las mismas 564 entradas.
  - Bootstrap de dos vías, B = 20.000, IC al 90 % (TOST al 5 % por lado; hay una sola configuración, así que no se corrige entre configuraciones).
  - Margen 0,01, el mismo del factorial 2.
  - Los mismos seis veredictos que el factorial 2.
- **Nulos:** p = (1 + #nulos ≥ W)/(N + 1), con Holm sobre SL y T.
- **Hipótesis pre-registradas:**
  - **H_SUPERA_R2:** se sostiene si da SUPERA (lo > +1 punto). Queda refutada si hi < +1 (EQUIVALENTE, NO_SUPERIOR o PIERDE). En cualquier otro caso, SIN_DECIDIR.
  - **H_CABLEADO_R2:** se sostiene si los dos p de Holm son < 0,05.
- **Controles del agregador:**
  - ancla exacta;
  - todos los json válidos;
  - plan completo (600 corridas y 50 + 50 nulos);
  - TAU_DN_IGUAL;
  - **REPRODUCE_F2:** las 90 corridas que comparte con el factorial 2 deben dar lo mismo, con tolerancia 0,001 y una bandera de exacto;
  - **REAL_IGUAL.**

## Herramientas y máquina

- **GitHub MCP:** `create_branch` y dos `push_files` en la rama titan, más este commit en main.
- **brain-env:**
  - humo de 3 corridas (grilla 1 celda, un nulo SL con `--real` y un nulo T), con R2 completo y n chico;
  - clon de verificación;
  - `yaml.safe_load`;
  - API pública de Actions;
  - prueba del parche del CONTEXTO.
- **Actions:** nada del factorial. Sin cuota ajena.

## Qué se midió y evidencia cruda

```
# humo (brain-env)
grilla rc=0 nulos_SL rc=0 nulos_T rc=0 agregado rc=0 FIN
CORRIDA celda=0.3|0.15 tau=0 prueba=2 W=0.9750 regla_propia=0.9500 regla40=0.9250 dif=+0.0250
CHEQUEO SL_IGUAL_MODULO (R1, 91484 aristas, semilla [7, 0]) -> True
SUJETO R2 neuronas=33489 aristas=4031897 entradas=564 -> True
RADIO real crudo=2032.307097
REAL W=0.9750 | 160.7 s
NULO SL k=0 acierto=0.7250 radio=559.0970 destinos_cambiados=4030551 guarda=True | 149.6 s
NULO T k=0 acierto=0.7500 tipos_cambiados=423 guarda=True | 156.3 s
CHEQUEO REAL_IGUAL grilla=0.975 script_de_nulos=[0.975] -> True
CHEQUEO REPRODUCE_F2 corridas_comparadas=1 tolerancia=False exacto=False -> False   (esperado en humo: n distinto)
VEREDICTO_GLOBAL -> VALIDO | primaria=SUPERA   (humo, sin valor)
md5: agregado.log 13c53f11… | grilla.log c8bf9254… | nulos_SL.log 2322e894… | nulos_T.log 90e8f20b…
md5: factorial2_R2_CON_TASA_t0c2.json e1b9d153… | nulos_R2_SL_k000.json 30b64d40… | nulos_R2_T_k000.json 06aa60a2…
# clon limpio de 6a7b4cb
c4f1c4d39c99f07cb9ad7977b6f3b01a  tools/factorial3/nulos_r2.py
2ec8cd03073e4e729e1c3872f29390b3  tools/factorial3/agregar_factorial3.py
798a824cd47808155fa12adb9e652dac  tools/factorial2/factorial2_mosca.py
243a24330fcf0efe0af8d225f707fb2e  .github/workflows/factorial3-mosca.yml
sin_CORRER | 18 json R2 del factorial 2 presentes | yaml_ok ['ancla', 'grilla', 'nulos', 'agregar'] 60 20
runs 1 [('H4 integrated regression', 'completed', '373e8ac')]
# parche del CONTEXTO (copia en brain-env)
171cab59e2bb11368fe2d14a08ab9a97  parche.py | md5 antes e2d4b55b… -> despues 20f6eb51… PARCHE OK (435 lineas)
```

**Costo:** en brain-env, un nulo SL de R2 con 200 ensayos tarda 150 s. En Actions, el factorial 2 midió unos 0,135 s por ensayo, así que se estiman unos 55 min por trabajo de grilla y unos 60 min por trabajo de nulos. Con el límite de 20 simultáneos, son unas 4 h.

## Archivos

- **Rama `titan/factorial3-mosca-2026-10-13`:**
  - `tools/factorial3/nulos_r2.py`, `tools/factorial3/agregar_factorial3.py` y `tools/factorial3/humo_f3.sh` (`373e8ac`);
  - `.github/workflows/factorial3-mosca.yml` (`6a7b4cb`).
- **main:**
  - este archivo;
  - `tools/contexto/actualizar_contexto_2026-10-13-008.py` (`171cab59…`);
  - `.github/workflows/contexto-2026-10-13-008.yml`.
- Los logs del humo quedan en brain-env (`/workspace/tm_2026-10-13/f3/humo/`), referenciados por md5.

## NO MEDIDO

- **Ningún resultado.** Todavía no corrió.
- **Que GitHub arme bien la grilla.** Que el `include` le agregue `celda` a cada combinación de la matriz está documentado, pero no se probó en Actions. Si falla, el trabajo aborta con `--celdas` vacío y se ve.
- **Los nulos usan una sola semilla de τ y una de prueba,** igual que en el factorial 1.
- **El entrenamiento es uno solo.**
- **Lo que queda fuera:** R2 sin inhibición y R2 con LIQ.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| Los nulos corren por el mismo camino que la grilla | REAL_IGUAL en el humo | Sí: con otro ruido o con otro τ daba distinto |
| El barajado es el del módulo | SL_IGUAL_MODULO contra `base.barajar_sl` | Sí: con otro orden de bloques no coincide |
| La grilla es el instrumento del factorial 2 | md5 `798a824c…` y REPRODUCE_F2 sobre 90 corridas | Sí: cualquier cambio rompe el md5 o la reproducción |
| Está sellado sin disparar | API de runs y ausencia de CORRER | Sí |

```
--- METODO PROMETEO ---
Accion delicada: no (rama titan, nada disparado)
Maquina: brain-env (humo, verificacion) | Actions x64 (cuando se dispare)
Artefactos: docs/agents/respuestas/2026-10-13-008-factorial-3-sellado-r2-con-diez-por-diez-semillas-y-sus-barajados.md + Doc de ClickUp 2026-10-13-008
```
