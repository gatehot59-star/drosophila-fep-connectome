# 2026-10-14-021 · H_TOPO_FIEL sellado: el programa que usa solo flechas que la mosca tiene, contra el que resta

## Pedido
Abraham, 14-oct 18:20, ClickKit `sellar_topo_fiel_020`: «Sellá el programa fiel a la mosca». Sellar, no correr: la corrida completa espera su `CORRER`.

## Veredicto primero
- [SELLADO] H_TOPO_FIEL en `titan/topo-fiel-2026-10-14`, en tres pasos verificables: A `27fe098` (los programas, antes de cualquier banco), B `b3548c8` (banco, regla de decisión, prueba, workflows), sello `79b8c59` (`tools/topo_fiel/SELLO-TOPO-FIEL.md`).
- [MEDIDO] El programa fiel (`escape_fiel.topo`) es `escape.topo` sin la resta contralateral en el giro. Topo v0.1 lo chequea contra FlyWire v783: **CABLEADA=10**, ninguna flecha sin vía. El que resta da CABLEADA=10 y SIN_VIA_DIRECTA=4 (lo de la 020).
- [MEDIDO] `prueba_fiel.py` 8/8 en brain-env y desde un clon limpio; con el programa equivocado da 6/8 (puede dar rojo).
- [MEDIDO, sin valor] Humo en brain-env (600/400): el fiel pierde unos 5 puntos (−5,37, IC90 [−6,63; −4,21]). Casi todo viene del looming frontal en vuelo: sin la resta, las dos DNp06 se encienden y gana el giro en vez del aterrizaje (fiel 9 a 24 %, el que resta 100 %). En el giro, el fiel acierta igual o más. El control cruzado salió REFUTADA (−27,5 puntos).
- [CONCLUSIÓN] El humo ya anticipa REFUTADA. La corrida completa no es ciega respecto del humo (mismas semillas a menor tamaño); lo que agrega es precisión y el desglose completo. Si se confirma, la resta del programa hace un trabajo real (cancelar el looming frontal en el giro) que en la mosca tiene que hacer otra cosa, sin vía directa.
- [NO MEDIDO] La corrida completa; el humo en Actions (en cola detrás de H_DEBILES).

## Herramientas y máquina
- brain-env (Linux x86_64, Python 3.12.14, numpy 2.5.3, torch del entorno): chequeo Topo v0.1, prueba, humo, prueba del parche en copia.
- GitHub: rama nueva, tres commits, verificación de md5 desde un clon limpio.
- Actions x64: humo disparado (run 38641044331, en cola).
- Acción delicada: ninguna. No se mergea ni se corre nada sellado sin el sí de Abraham.

## Evidencia
| Qué | Valor |
|---|---|
| Chequeo del fiel | `docs/topo/grafo-fiel-2026-10-14.log` 53961f0d, CHEQUEO escape_fiel CABLEADA=10 |
| Prueba | 8/8 (IGUAL, PIERDE5, AMBIGUO, GANA, DETERMINISTA, FINAL_INVALIDO, PAR_MINIMO_FIEL, PAR_MINIMO_CRUZADO) |
| Humo brain-env | `results/topo_fiel_2026-10-14_humo/brain-env-humo.log` eac0b4e7; 64,8 s; EXIT_RUN=0 |
| Humo: fiel menos el que resta | −0,0537, IC90 [−0,0663; −0,0421] (sin valor) |
| Humo: control cruzado | −0,2754, REFUTADA |
| Humo: looming frontal en vuelo | fiel 0,088 a 0,235; el que resta 1,000 en las 6 celdas |
| Humo: giro en vuelo | fiel 0,784 a 0,931; el que resta 0,529 a 0,931 |

## Hipótesis sellada
- **H_TOPO_FIEL:** d = acierto del fiel menos el del que resta, 12.000 ensayos, semillas nuevas (31, 32, 131, 132), IC90 por bootstrap estratificado por celda (B = 20.000). SOSTENIDA si el límite inferior es mayor que −0,01; REFUTADA si el superior es menor que −0,01; si no, SIN_DECIDIR.
- **CONTROL_ROJO:** el cruzado con el mismo criterio tiene que salir REFUTADA; si no, INVALIDO.
- **Descriptivo:** fiel contra `aterrizaje_dir.topo` y contra W; por celda y por subconjunto.

## Archivos
| Archivo | md5 |
|---|---|
| `tools/topo_fiel/escape_fiel.topo` | 8e7f23be70392bde04643a2bf3c1fa65 |
| `tools/topo_fiel/escape_cruzado.topo` | 9d0bb0f6f4cdc48f138b09f5b268429d |
| `tools/topo_fiel/banco_fiel.py` | ff0a7cbf333788634c405da7d09fcae7 |
| `tools/topo_fiel/decidir_fiel.py` | 840aeabf15446852cd0122a6fc4e5b7a |
| `tools/topo_fiel/prueba_fiel.py` | 016a6307ce06f4f70cf74eb753a9cd8d |
| `tools/topo_fiel/SELLO-TOPO-FIEL.md` | 050e8c3e48757d87d58c5389d473b7ea |
| `.github/workflows/topo-fiel-mosca.yml` | 8c18ab3d6ffeed8648905b8e81202ff2 |
| `.github/workflows/topo-fiel-humo.yml` | 63bbfde18d825c4125fbd5d04719cb27 |
| `docs/topo/grafos/escape_fiel.md` | bd4683fcfb5da263c0fb1841531d2b48 |
| `tools/contexto/actualizar_contexto_2026-10-14-021.py` | aef93a88cf0cc4d9747c53983b2f144a |

## NO MEDIDO
- La corrida completa de H_TOPO_FIEL (unos minutos en Actions).
- El humo en Actions (en cola).
- Qué hace la mosca en lugar de la resta: a dos saltos, la 020 vio casi todo excitatorio. Sería la pregunta siguiente si se confirma.
- H_DEBILES sigue corriendo (run 38635900391).

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| El fiel está cableado | topo_grafo.chequear sobre FlyWire v783 | Sí: el que resta da SIN_VIA_DIRECTA=4 con el mismo instrumento |
| Son pares mínimos | prueba_fiel.py | Sí: con escape.topo en lugar del fiel da 6/8 |
| La regla decide bien | escenarios sintéticos | Sí: cubre SOSTENIDA, REFUTADA y SIN_DECIDIR |
| El banco puede dar rojo | control cruzado | Sí: salió REFUTADA en el humo |
| md5 de lo pusheado | clon limpio | Sí: los 10 coinciden |
| Humo independiente de la corrida | no lo es | Declarado: mismas semillas, menor tamaño |

--- METODO PROMETEO ---
Investigar primero: leídos `banco_barra_dir.py`, `SELLO-BARRA-DIR.md`, `escape.topo`, `aterrizaje_dir.topo` y `topo_grafo.py` antes de escribir. Programas sellados antes del banco (paso A). Semillas nuevas. Control negativo con veredicto propio. Humo visto y declarado; nada cambiado después. Corrida completa solo con `CORRER`.
