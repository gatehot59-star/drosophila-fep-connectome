# 2026-10-14-023 · H_FRENO sellado: qué frena el giro de DNp06 ante el looming frontal, con DNp06 todavía ciega

## Pedido
Abraham, 14-oct 19:57, ClickKit `sellar_frena_giro_022`: «Sellá qué frena el giro en la mosca».

## Veredicto primero
- [SELLADO] H_FRENO en `titan/frena-giro-2026-10-14`. El instrumento, la prueba y los workflows están en `d59913c`, antes de mirar DNp06. El sello, el humo y su disparo están en `2bad970` (`tools/frena_giro/SELLO-FRENO.md`).
- [SELLADO] **Siete mecanismos pre-registrados:**
  - Directos: DNp07 inhibe a DNp06, DNp01 inhibe a DNp06, y la DNp06 opuesta inhibe a la otra.
  - A dos saltos, por una interneurona inhibitoria alimentada por: LPLC1 y LPLC2 del otro lado, LPLC4, DNp07, o un detector de frente bilateral (LPLC2 o LC4 de los dos lados).
- [SELLADO] **Cómo se mide:** cuota de la entrada inhibitoria de DNp06 y su percentil contra las otras unidades descendentes del mismo lado.
  - A dos saltos es CANDIDATO con cuota de al menos 5 % y percentil de al menos 0,90, en los dos lados.
  - Un directo es PRESENTE con al menos 5 sinapsis en los dos lados.
  - Control positivo: LPLC1 y LPLC2 del mismo lado sobre DNp06, excitatorio. Si falla, el resultado es INVALIDO.
- [MEDIDO] `prueba_freno.py` da 6/6 con grafos de juguete. **Dio rojo una vez:** el objetivo entraba en su propia referencia y el percentil daba 0,957 en vez de 1,0. Lo corregí antes de cualquier dato real.
- [MEDIDO, sin valor] El humo corrió con **DNp01** como objetivo, así que DNp06 sigue sin mirar. Corre en 17,6 s, toma 927 unidades descendentes de referencia y el control positivo PASA (percentil 0,993 y 0,995).
- [NO MEDIDO] DNp06. La corrida espera el `CORRER` y tarda segundos.

## Herramientas y máquina
- brain-env (Linux x86_64, Python 3.12.14, numpy 2.5.3, pandas 3.0.5).
- GitHub: rama nueva desde main `b311b3c` y md5 verificados desde un clon limpio.
- Actions: humo disparado con DNp01.
- Acción delicada: ninguna.

## Archivos
| Archivo | md5 |
|---|---|
| `tools/frena_giro/freno_mosca.py` | 1318fefb8dbac3ce56bc56c9a439ea26 |
| `tools/frena_giro/prueba_freno.py` | 9b095a1534f9a3ef6f4906e75d570a1d |
| `tools/frena_giro/SELLO-FRENO.md` | e3d828dda910e26fea49239115b68878 |
| `.github/workflows/freno-mosca.yml` | 45f988be173857944875a84e929c90e0 |
| `.github/workflows/freno-humo.yml` | 341b9e421c2faaeca13f694be3bd913d |
| `results/frena_giro_2026-10-14_humo/brain-env-humo.log` | f8aa6f3b4de134c84e2d143ff5eb3d2a |
| `tools/contexto/actualizar_contexto_2026-10-14-023.py` | ed0ccedea1aa2f7f248f67627b51aeb8 |

## NO MEDIDO
- DNp06, que es la pregunta.
- Vías a más de dos saltos, el freno aguas abajo (en el cordón nervioso) y la dinámica.
- Si un CANDIDATO frena de verdad. Eso pide el paso funcional siguiente: agregar ese freno al banco y ver si recupera el aterrizaje ante el looming frontal.
- H_TOPO_FIEL en Actions y H_DEBILES siguen en cola o corriendo.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? |
|---|---|---|
| La regla clasifica bien | prueba_freno.py | Sí, y dio rojo una vez (percentil) |
| El instrumento ve lo cableado | control positivo | Sí: E3 da INVALIDO sin LPLC1 directo |
| DNp06 sigue ciega | humo con DNp01 | El log no nombra a DNp06 como objetivo |
| md5 de lo pusheado | clon limpio | Sí: todos coinciden |
| Multiplicidad | ninguna corrección | Declarado: un CANDIDATO no es una prueba |

--- METODO PROMETEO ---
Leídas la 020 y la 022 antes de diseñar. Mecanismos y umbrales fijados antes de mirar DNp06. Prueba con juguetes que cubren cada veredicto. Humo sobre otro objetivo para no ver el real. Corrida solo con `CORRER`.
