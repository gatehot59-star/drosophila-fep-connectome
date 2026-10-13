#!/bin/bash
set -u
R=/workspace/tm_2026-10-13/f3/repo
H=/workspace/tm_2026-10-13/f3/humo
mkdir -p $H/res
cd $R
C="--conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv"
python3 tools/factorial2/factorial2_mosca.py $C --out $H/res --config R2_CON_TASA --taus 0 --pruebas 2 --celdas "0.3|0.15" --etiqueta t0c2 --humo > $H/grilla.log 2>&1; echo "grilla rc=$?" >> $H/estado.txt
python3 tools/factorial3/nulos_r2.py $C --out $H/res --tipo SL --k0 0 --n 1 --real --humo > $H/nulos_SL.log 2>&1; echo "nulos_SL rc=$?" >> $H/estado.txt
python3 tools/factorial3/nulos_r2.py $C --out $H/res --tipo T --k0 0 --n 1 --humo > $H/nulos_T.log 2>&1; echo "nulos_T rc=$?" >> $H/estado.txt
python3 tools/factorial3/agregar_factorial3.py $H/res results/factorial2_2026-10-13 --humo > $H/agregado.log 2>&1; echo "agregado rc=$?" >> $H/estado.txt
echo FIN >> $H/estado.txt
