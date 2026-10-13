#!/bin/bash
set -u
R=/workspace/tm_2026-10-13/f2/repo
H=/workspace/tm_2026-10-13/f2/humo
mkdir -p $H
cd $R
C="--conn /workspace/connectivity.parquet --annot /workspace/annotations.tsv"
python3 tools/factorial2/factorial2_mosca.py $C --out $H/ancla --config ANCLA_015 > $H/ANCLA_015.log 2>&1; echo "ANCLA_015 rc=$?" >> $H/estado.txt
for cfg in M46_TASA M46_LIQ R1_CON_TASA R1_CON_LIQ R1_SIN_TASA R1_SIN_LIQ; do
  python3 tools/factorial2/factorial2_mosca.py $C --out $H/json --config $cfg --taus 0,1 --pruebas 2,3 --humo > $H/$cfg.log 2>&1
  echo "$cfg rc=$?" >> $H/estado.txt
done
python3 tools/factorial2/factorial2_mosca.py $C --out $H/json --config R2_CON_TASA --taus 0 --pruebas 2,3 --celdas "0.3|0.15" --etiqueta t0c3 --humo > $H/R2_CON_TASA.log 2>&1
echo "R2_CON_TASA rc=$?" >> $H/estado.txt
python3 tools/factorial2/agregar_factorial2.py $H/json --humo > $H/agregado.log 2>&1
echo "agregado rc=$?" >> $H/estado.txt
echo FIN >> $H/estado.txt
