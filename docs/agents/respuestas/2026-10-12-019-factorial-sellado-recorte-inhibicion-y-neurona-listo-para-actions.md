# 019 · Factorial sellado: recorte x inhibicion x neurona, listo para correr en Actions (13-oct, 00:27 a 01:10)

**Veredicto primero.** [MEDIDO] El factorial quedo sellado en la rama `titan/factorial-mosca-2026-10-13`, commit `552942f`, con md5 identicos en un clon limpio: `factorial_mosca.py` 8224fdddc8bf675b0b8b0375bf27f6cb, `agregar_factorial.py` 7931c0884485abd1f74f35fbeb424d87, modulo 015 40d64e074d9163753439307c5be4ac5e, workflow ae5d49bad8f1d47608da88f49cba2d4c. [MEDIDO] La corrida completa de M46_TASA con la v2 reproduce los 12 aciertos de la 015 **exactos** (tolerancia y exacto True x6, VALIDO, 259,9 s en brain-env). [MEDIDO] Humo 2 con la v2: 5 de 9 configuraciones terminadas con rc=0 al cierre (M46_TASA, M46_LIQ, M46_LIF, R1_CON_TASA, R1_CON_LIQ); las otras 4 seguian corriendo y quedan NO MEDIDO aca. [CONCLUSION] No hay resultado del factorial todavia: el sello es el diseno, la corrida completa va a Actions.

## Pedido
ClickKit `sellar_factorial_018`: sellar el experimento combinado propuesto en la 018 (neurona, recorte con inhibicion, o la combinacion).

## Herramientas y maquina
- brain-env (MUDH Gateway, `build`): md5, clon limpio, humo 2, reproduccion completa de M46_TASA. Python 3.12.14, numpy 2.5.3, pandas 3.0.5. Sin GPU.
- GitHub MCP: rama nueva, commit de sello `552942f`, este archivo en main. Nada mergeado.
- `pip download` en brain-env: existen ruedas cp312 x86_64 de numpy 2.5.3, pandas 3.0.5, scipy 1.18.1 y pyarrow 25.0.1 (lo que instala el workflow).

## Diseno sellado (resumen; el docstring del script manda)
- 9 configuraciones: M46_{TASA,LIQ,LIF}, R1_CON_{TASA,LIQ,LIF}, R1_SIN_{TASA,LIQ,LIF}. R1 = las 6 DN de la 015 mas toda neurona con arista >=5 sinapsis sobre alguna (1.504 neuronas, 91.484 aristas, con signo). SIN = sin aristas negativas.
- TASA = la de la 015. LIQ = liquida nativa de SparseLTC, tau_gain 1,0 declarado sin ajuste. LIF = Shiu 2024 con simplificaciones declaradas (dt 1 ms, refractario y retardo 2 pasos, entrada G_IN 14 mV x drive, no Poisson).
- Primaria por configuracion: W contra la regla a mano, McNemar por celda, Holm sobre 6. PIERDE / IGUALA / SUPERA.
- Contrastes de factor (10) y veredicto global en el agregador. **Falsador pre-registrado: NINGUNA CIERRA LA BRECHA.** Ancla: M46_TASA valida.
- Secundaria descriptiva: nulos SL y T en A0,3 sigma0,15 (50+50; 20+20 con LIF).

## Cambio declarado despues del humo 1 y antes del sello
v1 (md5 09e8414d...) -> v2 (8224fddd...): REPRODUCE_015 con tolerancia de 0,001 de acierto (2 ensayos de 2000) porque otra CPU puede redondear distinto; imprime tambien si es exacto. Nada mas cambio.

## Evidencia cruda
```
552942f sello(019): factorial de la mosca (...)
8224fdddc8bf675b0b8b0375bf27f6cb  tools/factorial/factorial_mosca.py
7931c0884485abd1f74f35fbeb424d87  tools/factorial/agregar_factorial.py
40d64e074d9163753439307c5be4ac5e  tools/escape_aterrizaje/tarea_mosca.py
ae5d49bad8f1d47608da88f49cba2d4c  .github/workflows/factorial-mosca.yml
yaml_ok ['correr', 'agregar']
```
Reproduccion completa M46_TASA v2 (log md5 7ff5ae0bf842685240ff2e52fe724fa8, json 7fe16b9af022070311c6aff325e083c2, quedan en brain-env `/workspace/tm_2026-10-12/repro019b/`):
```
CELDA A=0.0 ruido=0.15 W=0.9005 regla=0.9195 H3 W contra regla 118 contra 156 p=0.0252
CELDA A=0.0 ruido=0.45 W=0.8805 regla=0.8705 H3 W contra regla 175 contra 155 p=0.296
CELDA A=0.3 ruido=0.15 W=0.9125 regla=0.9325 H3 W contra regla 75 contra 115 p=0.00454
CELDA A=0.3 ruido=0.45 W=0.8915 regla=0.8935 H3 W contra regla 135 contra 139 p=0.856
CELDA A=0.6 ruido=0.15 W=0.8680 regla=0.9315 H3 W contra regla 73 contra 200 p=7.82e-15
CELDA A=0.6 ruido=0.45 W=0.8580 regla=0.9120 H3 W contra regla 103 contra 211 p=1.08e-09
CHEQUEO REPRODUCE_015 tolerancia=[True, True, True, True, True, True] exacto=[True, True, True, True, True, True] -> True
NULOS_DESCRIPTIVO A=0.3 ruido=0.15 W=0.9125 | SL n=50 media=0.6527 max=0.8015 p_sup=0.0196 | T n=50 media=0.6707 max=0.8395 p_sup=0.0196
CHEQUEO INSTRUMENTO sin_negativas=True REPRODUCE_015=True SL=True T=True -> VALIDO
# duracion_s=259.9
EXIT_RUN=0
```
Humo 2 (`/workspace/tm_2026-10-12/humo_fact2/estado.txt`, UTC):
```
FIN M46_TASA rc=0 04:00:56
FIN M46_LIQ rc=0 04:01:50
FIN M46_LIF rc=0 04:03:16
FIN R1_CON_TASA rc=0 04:05:30
FIN R1_CON_LIQ rc=0 04:06:55
INICIO R1_CON_LIF 04:06:55
```

## Archivos
- Rama `titan/factorial-mosca-2026-10-13` @ 552942f: `tools/factorial/factorial_mosca.py`, `tools/factorial/agregar_factorial.py`, `.github/workflows/factorial-mosca.yml`.
- Este archivo en main.
- Como correr: pushear `results/factorial_2026-10-13/CORRER` a la rama (o disparo manual). El job `agregar` commitea logs, json, `agregado.log` y `MD5SUMS.txt` en `results/factorial_2026-10-13/`.

## NO MEDIDO
- Humo 2 de R1_CON_LIF, R1_SIN_TASA, R1_SIN_LIQ, R1_SIN_LIF y el agregado del humo 2: corriendo al cierre, sin leer.
- El workflow nunca corrio: ni la instalacion pip en el runner ni la descarga publica dentro de Actions (si en brain-env, md5 identico).
- Duracion en Actions de las configuraciones LIF sobre R1 (estimacion gruesa: decenas de minutos por job, bajo el tope de 340).
- Que la reproduccion exacta se mantenga en la CPU del runner (para eso esta la tolerancia, y el ancla lo dice).
- G_IN fijado analiticamente, no ajustado; LIF_RESPONDE es una guarda debil (M46_LIF dispara poco).
- R2 (33.489 neuronas) fuera: va a Kaggle GPU con port verificado contra numpy. Neurona liquida entrenada y formas dendriticas fuera (sin coordenadas de sinapsis).
- M46_TASA completa ya corrio antes del sello solo como reproduccion: sus numeros son los de la 015, no un hallazgo nuevo.

## Antes de firmar
| Afirmacion | Instrumento | Podia dar rojo |
|---|---|---|
| Sello identico en git | md5 en clon limpio | si (un caracter mal copiado) |
| Ancla exacta | REPRODUCE_015 contra 12 numeros fijos | si |
| Humo 5/9 ok | rc por config | si; 4/9 NO MEDIDO |
| Factorial dice algo | nada todavia | NO MEDIDO |

--- METODO PROMETEO ---
Accion delicada: no (rama titan, sin merge; el workflow no se disparo)
Maquina: brain-env (sello, humo, ancla) | Actions x64 (pendiente)
Artefactos: docs/agents/respuestas/2026-10-12-019-factorial-sellado-recorte-inhibicion-y-neurona-listo-para-actions.md + Doc de ClickUp 019
