# 2026-10-14-015 · El núcleo pierde en todas las semillas y más con ruido; con tau elegida, R2 supera a su regla; Topo pasó su prueba, pero el programa viejo sigue siendo mejor

**Pedido.** 14-oct 16:25: ClickKit `leer_nucleo_014` («Mientras tanto, leé el núcleo completo»). Al leerlo ya habían vuelto H_TAU (bot `2d4dbfb`) y H_TOPO_NUEVO (bot `46929db`).

## Veredicto primero
- **[MEDIDO] Núcleo** (`results/nucleo_2026-10-14/agregado.log`, rama `titan/htau-nucleo-banc-2026-10-14`, bot `a522bc4`; MD5SUMS 241/241 OK):
  - VEREDICTO_GLOBAL VALIDO.
  - H_CONSENSO REFUTADA: −4,59 puntos, IC90 [−5,07; −4,10]; pierde en las 6 celdas y en 600/600 corridas.
  - H_CABLEADO_NUCLEO SOSTENIDA: 0,9135 contra 50 SL (media 0,5913, máximo 0,7570) y 50 T (media 0,6869, máximo 0,7680); Holm 0,0392.
- **[MEDIDO] No es cosa de una semilla.** El núcleo pierde contra R2 en las 10 semillas de tau, de −3,06 (tau 5) a −5,81 (tau 1). Contra la regla, lo peor cae en las semillas 5 y 7 (−5,46 y −6,43), las mismas que en el factorial 4.
- **[MEDIDO, patrón leído después, sin sellar] Pierde más con ruido.** Con ruido 0,45 pierde más que con 0,15 en las 3 amplitudes:
  - A = 0: −5,93 contra −4,28;
  - A = 0,3: −5,61 contra −3,52;
  - A = 0,6: −5,24 contra −2,97;
  - en promedio, −5,59 contra −3,59.
  - Una lectura posible: las conexiones débiles promedian el ruido.
- **[CONCLUSIÓN, cuenta hecha después y cruzando experimentos] Lo poco conserva mucho.** En la celda de los nulos (A 0,3, ruido 0,15, tau 0, prueba 2), el núcleo, con el 14,96 % de las aristas, guarda (0,9135 − 0,666) / (0,9465 − 0,666) = 0,88 de la ventaja de R2 sobre la media de sus barajados SL del factorial 3.
- **[NO MEDIDO] H_DEBILES.** R2 con las fuertes intactas y las débiles barajadas, para saber si las débiles pesan por especificidad o por cantidad.
- **[MEDIDO] H_TAU SOSTENIDA** (`results/htau_2026-10-14/agregado.log`, MD5SUMS 19/19 OK):
  - REPRO_R2 exacto (0,9465 / 0,9375 / 0,9235).
  - La validación cruzada eligió la semilla 10 en las 6 celdas; la peor siempre fue la 14.
  - R2 con tau elegida le gana a su regla por +1,78 puntos, IC90 [+1,45; +2,13]: SUPERA en las 6 celdas (+1,53 a +1,96) y gana en 60/60 corridas.
  - Diagnóstico: elegida menos peor = +3,08.
- **[CONCLUSIÓN] Es la primera vez que el cableado supera a su diseño por el margen pre-registrado.**
  - Letra chica: el cableado eligió entre 10 sorteos de tau y la regla no tuvo ninguna perilla equivalente.
  - La prueba justa es **H_TAU_JUSTO**, sin sellar: darle a la regla una perilla equivalente elegida también por validación cruzada.
- **[MEDIDO] H_TOPO_NUEVO SOSTENIDA** (`results/topo_barra_2026-10-14/banco.log`, MD5SUMS 3/3 OK, Actions x64, 600,3 s):
  - H_TN_CABLEADO: GANA en las 6 celdas; Holm 0,0399 en las 12 pruebas.
  - H_TN_REGLA: regla nueva menos W = +1,68 puntos, IC90 [+0,99; +2,38].
- **[MEDIDO, descriptivo, sin veredicto] El programa nuevo es peor que el viejo.**
  - La regla vieja le gana a la nueva en 5 de 6 celdas en acierto total.
  - La nueva acierta más en la barra que va de atrás hacia adelante (por ejemplo 0,958 contra 0,952 y 0,922 contra 0,873).
  - Pero rompe el aterrizaje ante la barra que va de adelante hacia atrás: 0,315 a 0,917, contra 0,946 a 0,976 de la vieja.
- **[CONCLUSIÓN]** Topo pasó su prueba de fuego como lenguaje, pero la frase nueva fue mala. Una versión 2 del programa se sella sin mirar estos datos, o con una tarea nueva.

## Herramientas y máquina
- brain-env: `git pull` de las tres ramas; lectura de los agregados y de los logs; `md5sum -c` de los MD5SUMS; prueba del parche.
- GitHub (conector): esta respuesta en main.
- Las mediciones son de Actions x64, hechas por los bots.

## Qué cambia en el Paper 2
- §3.6 queda con el desenlace «la estructura se conserva, pero la función necesita también las conexiones débiles».
- §3.7 pasa a resultado positivo, con su letra chica.
- Topo puede ir como método o a un paper aparte.

## NO MEDIDO
- H_DEBILES.
- H_TAU_JUSTO.
- La versión 2 del programa de la barra.
- El nulo BANC.
- El efecto del ruido como hipótesis sellada.

## Antes de firmar
| Afirmación | Instrumento | ¿Podía dar rojo? | Veredicto |
|---|---|---|---|
| Los tres agregados son íntegros | `md5sum -c` de MD5SUMS (241, 19 y 3 archivos) | Sí | PASA |
| H_TAU supera | Agregado sellado, IC90 contra margen 0,01 | Sí: en el factorial 3 dio SIN_DECIDIR | PASA, con la asimetría declarada |
| Topo pasó | Banco sellado | Sí: con 3 nulos dio REFUTADA | PASA; el programa nuevo pierde con el viejo, declarado |
| El efecto del ruido | Lectura de 6 celdas después de los datos | No está sellado | Descriptivo |
| 88 % de la ventaja | Cuenta cruzando el factorial 3 | No está sellado | Descriptivo |

--- METODO PROMETEO ---
Accion delicada: no (lectura de resultados ya commiteados por los bots).
Maquina: brain-env CPU + conector GitHub.
Artefactos: esta respuesta en main; Doc https://app.clickup.com/90171457413/docs/2kza6fw5-22357
