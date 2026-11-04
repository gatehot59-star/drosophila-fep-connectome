#!/bin/bash
set -u
cd /workspace/a1/v2/evid10
V=codigo/tools/verificador_a1
M=/workspace/a1/v2/manifiesto_a1.json
SHA=267ca1d0820193fff08a79875a1d1bd6a36d8633e203db9e0ee3d7304c5e3dd9
T=/workspace/a1/v2/evid9/ensayo
P=/usr/local/bin/python3
date -u +%FT%TZ > inicio.txt
$P $V/ensayo_verificador_a1.py --verificador $V/verificador_a1.py --manifiesto $M --sha-manifiesto $SHA --trabajo $T --salida ensayo > ensayo.log 2>&1; echo "exit $?" >> ensayo.log
date -u +%FT%TZ > fin_ensayo.txt
$P $V/prueba_verificador_a1.py --verificador $V/verificador_a1.py --manifiesto $M --sha-manifiesto $SHA --sobre-limpio $T/sobre_limpio --agregado-limpio $T/est_limpio/agregado_a1.json --trabajo trab_prueba > prueba.log 2>&1; echo "exit $?" >> prueba.log
date -u +%FT%TZ > fin_prueba.txt
$P $V/mutantes_verificador_a1.py --verificador $V/verificador_a1.py --prueba $V/prueba_verificador_a1.py --manifiesto $M --sha-manifiesto $SHA --sobre-limpio $T/sobre_limpio --agregado-limpio $T/est_limpio/agregado_a1.json --trabajo trab_mut > mutantes.log 2>&1; echo "exit $?" >> mutantes.log
date -u +%FT%TZ > fin.txt
