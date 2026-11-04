# 009-A1 · Compromiso del verificador antes de correr el productor

Este commit fija la salida de la fase S del verificador antes de que corra estadistica_a1.py sobre el sobre real (respuesta 010, paso 3). Hasta acá nadie leyó ningún estimando ni veredicto: con recibos reales el verificador no imprime cuentas, y verificador_a1.json no se abrió.

| Archivo (brain-env, /workspace/a1/v2/apertura/ver/) | Bytes | sha256 |
|---|---|---|
| verificador_a1.json | 283.090 | ad65761bb84ee6632d65f03de88b263a209da5a4242e1055d92bd2f4a8432334 |
| verificacion_tecnica.json | 1.857 | 548198678ec30f6a2060eed81f4498630bb20a0fc49f60be816cb92ee857d0c8 (va entero en esta carpeta) |
| registro_ids.txt | 9.063 | 7c6dadc180b56d1d0c2be39782e948c3b7f73b994294412a345b8d011691c40a (igual al de la 010) |

verificador_a1.json va por sha256 y no entero: pesa 283 KB y la única vía a git es transcribirlo. Se recalcula desde git con el verificador de 5eaf35d0, el manifiesto 267ca1d0 y el sobre de 7d953dc8; la fase S es determinista (en la 010 dio el mismo sha dos veces).

Lo técnico, ya visible en los logs de esta carpeta: el sobre bajó entero (444 de 444 archivos iguales a SHA256SUMS, 22.571.291 B); fase E OK (44 celdas, 427 condiciones, 8.540 ensayos, 722 ids); fase T OK sin ninguna falla (0 celdas inválidas, entorno uniforme, runner 2026-11-03-005 en los 8.540 ensayos, un solo code_commit); fase S en 18,8 s, con 0 celdas inválidas y 0 cantidades no calculables, y el motor marcó 104 intervalos BCa degenerados en 584 llamadas a scipy. Ese 104 es un conteo del motor, no un veredicto: qué criterios toca se ve recién después del cotejo.
