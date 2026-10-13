#!/bin/bash
W=/workspace/tm_2026-10-12/rev_tao
rm -rf $W; mkdir -p $W; cd $W
R=https://github.com/gatehot59-star/drosophila-fep-connectome.git
git ls-remote --heads $R > heads.txt 2>&1
for b in main titan/v2-cierre-2026-10-12 titan/materializacion-h4-guard-2026-10-02 titan/escape-motivo-2026-10-11 titan/swarm-lazo-cerrado-2026-10-11 titan/auditoria-tao-laboratorio-2026-10-12; do
  d=$(echo $b | tr '/' '_')
  if git clone -q --depth 1 --branch $b $R $d > /dev/null 2>&1; then
    echo "CLON $b $(git -C $d log -1 --format='%h %cI')" >> estado.txt
  else
    echo "FALLO $b" >> estado.txt
  fi
done
echo TERMINADO >> estado.txt
