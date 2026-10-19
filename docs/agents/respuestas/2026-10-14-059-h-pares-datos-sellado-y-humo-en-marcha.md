# 2026-10-14-059 · H_PARES_DATOS quedó sellado y el instrumento pasó en brain-env; el humo corre en Actions y la curva todavía no se midió

**Fecha:** 2026-10-18, 23:20 (America/Buenos_Aires)
**Doc:** https://app.clickup.com/90171457413/docs/2kza6fw5-23837

## Pedido

«Sellá H_PARES_DATOS y ejecutá la curva» (Abraham, 18-oct 22:30).

## Veredicto primero

- [HECHO] **Sellado:** `tools/pares/SELLO-PARES-DATOS.md` en `titan/pares-datos-2026-10-18`, commit `0d30190` (22:44), md5 a0737294a570093f236188c638a0c417, antes de escribir código. Verificado desde un clon en brain-env: ese commit trae solo el sello.
- [MEDIDO] **El instrumento pasó en brain-env:**
  - prueba unitaria 6 de 6, VALIDO; L_IGUAL: el lector con guarda da lo mismo que el de H_LECTOR, pliegue por pliegue y predicción por predicción;
  - ruta local de la mosca (c2, tau 20, 600 y 200 ensayos) y del crudo (c2): VALIDO, con todos los pines en True;
  - agregador local, ciego: VALIDO.
- [HECHO] **El humo ciego corre en Actions**, disparado con `fbba63a`.
- [NO MEDIDO] **La curva.** No hay ningún acierto todavía: la corrida completa espera el VALIDO del humo, como dice el sello.
- **Error mío:** el push que disparó el humo (`fbba63a`) no llevaba `agregar_pares.py` ni `prueba_pares.py`. El trabajo «prueba» de ese humo va a fallar; los de la mosca y el crudo usan solo `pares_datos.py` y sí miden. Los dos archivos subieron en `0c6086c`. Antes de CORRER se repite la prueba, sin cambiar código.

## Qué mide (del sello)

- **Brazos**, con el mismo lector L y los mismos ensayos:
  - W, la mosca sin ejemplos de acción, con las taus 20 a 29 que nadie eligió;
  - MOSCA_L, la mosca con lector (240 rasgos);
  - CRUDO, el ridge sobre 22.560 rasgos;
  - PCA_L, 240 componentes ajustadas sin etiquetas;
  - PROY_L, 10 proyecciones aleatorias de 240.
- **Curva:** n = 6, 12, 24, 48, 96, 192, 384, 768 y 2.400 ensayos etiquetados, 20 repeticiones anidadas, celdas c2 y c5, prueba 12.
- **Hipótesis, con margen de 1 punto:**
  - H_DATOS_EMBUDO: el embudo de la mosca les gana a PCA y a la proyección del mismo ancho;
  - H_DATOS_CRUDO: le gana al ridge crudo;
  - H_DATOS_PRIMER_DIA: con 96 ensayos ningún par artificial llega a 1 punto de la mosca sin ejemplos.
- **Controles:** con 2.400 ensayos, MOSCA_L reproduce H_TAU_LIBRE (20 de 20) y CRUDO reproduce H_RIVAL.

## Qué sigue

1. Leer el humo en la rama: REPRO_TAULIBRE y REPRO_CRUDO a tamaño completo en c2 y c5.
2. Si dan VALIDO, repetir la prueba unitaria en Actions con `0c6086c` y pushear `results/pares_datos_2026-10-18/CORRER`. Son 12 trabajos y tardan unos 25 a 30 minutos.
3. Leer `agregado.log` y escribir la respuesta con los tres veredictos, la curva y el parche del CONTEXTO.

## Herramientas y máquina

- **Conector GitHub:** lectura de los sellos e instrumentos de H_RIVAL, H_LECTOR y H_TAU_LIBRE; rama nueva; pushes `0d30190`, `fbba63a` y `0c6086c`.
- **brain-env:** clon de `e7ada46`, composición del entrenamiento, prueba unitaria y ruta local completa. La mosca chica tardó 454 s y el crudo chico 96 s.
- **Sandbox de ClickUp:** redacción y compilación.
- **Actions:** humo en curso. **Kaggle:** nada.

## Archivos

| Archivo | Dónde | md5 (brain-env) |
|---|---|---|
| `tools/pares/SELLO-PARES-DATOS.md` | `titan/pares-datos-2026-10-18`, `0d30190` | a0737294a570093f236188c638a0c417 (verificado en la rama) |
| `tools/pares/pares_datos.py` | ídem, `fbba63a` | e40c3a4f2a9e1aed9431f0bc1f8ecdc8 |
| `tools/pares/agregar_pares.py` | ídem, `0c6086c` | 6ca4306fe0f6c99d00a1007257b34b2b |
| `tools/pares/prueba_pares.py` | ídem, `0c6086c` | ead492f9c4dbe36e916f3dbe8b0ca6fc |
| `.github/workflows/pares-humo.yml` y `pares-datos.yml` | ídem, `fbba63a` | el humo corre; la corrida, todavía no |
| `results/pares_datos_2026-10-18_humo/brain-env/prueba_pares.log` | ídem, `fbba63a` | log verbatim de la prueba |
| este archivo | `main` | este archivo |

## NO MEDIDO

- La curva entera y los tres veredictos.
- Los md5 de los tres scripts tal como quedaron en la rama: falta compararlos desde un clon nuevo contra los de brain-env.
- El resultado del humo.
- El parche del CONTEXTO de la 059: va con la respuesta de los resultados.
- Los logs locales de la mosca, del crudo y del agregador: quedaron en brain-env y no subieron a la rama.

## Antes de firmar

| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| El sello precede al código | historia de la rama: `0d30190` trae solo el sello | Sí | medido |
| L con guarda es el L de H_LECTOR | L_IGUAL contra `rv` y `lm`, en brain-env | Sí: dio rojo una vez por una expectativa mal puesta en la prueba | medido |
| La ruta completa corre | ruta local de mosca, crudo y agregador | Sí | medido (chico, no decide) |
| El humo reproduce H_TAU_LIBRE y H_RIVAL | humo en Actions | Sí | NO MEDIDO |

--- METODO PROMETEO ---
Rol: implementación (grande). Delicado: no.
Máquinas: brain-env (pruebas), Actions (humo en curso), conector GitHub, sandbox de ClickUp. Kaggle: nada.
Archivo: `docs/agents/respuestas/2026-10-14-059-h-pares-datos-sellado-y-humo-en-marcha.md` en `main`.
Doc: https://app.clickup.com/90171457413/docs/2kza6fw5-23837
