# 009-A1 · Decisiones fijadas antes de abrir el sobre

Autorización: «Autorizo abrir el sobre de 009-A1» (Abraham, chat, 3-nov-2026 23:48 ART). Llegó sola, así que se aplican las tres recomendaciones de la respuesta 2026-11-03-011. Este commit es anterior a cualquier descarga de los bloques del sobre: al escribirlo, ningún bloque_*.jsonl de corrida_1 se bajó a ninguna máquina.

## Las tres decisiones

1. **D1, «no evaluable» en 010:** sin datos válidos o con varianza cero, como lo implementan el productor y el verificador. La lectura alternativa, más conservadora pero circular, no se aplica.
2. **D12, índice de ablación original:** 010 lo nombra y no lo define; no se calcula y queda NO MEDIDO.
3. **Hueco del control:** si el cotejo K1 marca HUECO_DEL_CONTROL (una celda que invalida el verificador y no el productor), se publican los dos veredictos y vale el propio del verificador, que deja esa celda fuera; el del productor va al lado como descriptivo. Un SIN_CLASIFICAR da DISCORDANTE, y entonces no se lee ningún veredicto.

## Piezas fijadas

| Pieza | Dónde | sha256 |
|---|---|---|
| Sobre | 7d953dc8577ecf1fdbaecc4859b902af8854e79b, results/a1_2026-11-03/corrida_1/ | SHA256SUMS.txt bf9ebde69cc12f6c1f5b1c85925aebeeb36fd7fe6f23052aef35706a74cc7e38 |
| Manifiesto | titan/a1-runner-2026-11-03 (copia en brain-env /workspace/a1/v2/manifiesto_a1.json) | 267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9 (640.908 B) |
| Verificador | 5eaf35d08117a34bb37a325a1e4422ffb316b650, tools/verificador_a1/verificador_a1.py | a7b553f7d456920f76b7f8e9da2459437439c523381908fce923676a1947abd0 |
| Productor | 801487cad19747e96bb346d98ffad1c3d508847c, tools/a1/estadistica_a1.py (sin cambios desde 5c9492ff) | 37ab63d7dc94913c010cdc51d89a23a0ace0a4e6e511b4c344ffad15b24503e3 |
| Módulos del productor | mismo commit, tools/a1/ | comun_a1.py 756e81ab…, plan_a1.py d1b26450…, validar_a1.py 189eb647…, juntar_a1.py 051d0b47…, iguales a tools/a1/HUELLAS.sha256 |

## Orden de corrida (respuesta 010, «Para abrir el sobre»)

Máquina: brain-env. Raíz de trabajo: /workspace/a1/v2/apertura/.

1. Bajar el sobre por raw desde 7d953dc8 y chequear cada archivo contra SHA256SUMS.txt.
2. `verificador_a1.py --manifiesto M --sha-manifiesto 267ca1d0… --sobre corrida_1 --salida V --fases ET --abrir-sobre`. Si sale con algo distinto de 0, se para y se reporta.
3. Lo mismo con `--fases ETS`. Se commitean verificacion_tecnica.json entero y el sha256 de verificador_a1.json antes de correr el productor. verificador_a1.json pesa unos 280 KB: va por sha256, porque la única vía a git es transcribirlo y cualquiera lo recalcula desde git.
4. `estadistica_a1.py --manifiesto M --sha-manifiesto 267ca1d0… --jsonl 'corrida_1/bloques/**/bloque_*.jsonl' --salida P --abrir-sobre`. Se commitea el sha256 de agregado_a1.json (unos 340 KB, por la misma razón).
5. `verificador_a1.py … --salida V --fases ETK --agregado-productor P/agregado_a1.json --abrir-sobre`, que usa el verificador_a1.json ya commiteado. Se commitea cotejo_a1.json entero.
6. Sólo si da CONCORDANTE se leen los veredictos con la tabla de la 007.

Nada de esto cambia 010, el productor ni el verificador.
