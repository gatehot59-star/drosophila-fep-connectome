#!/bin/bash
cd /workspace/tm_2026-10-12/rev_tao
V=titan_v2-cierre-2026-10-12; A=titan_materializacion-h4-guard-2026-10-02
echo "== donde esta twohop_nulls"; find . -name "twohop_nulls.py" -exec md5sum {} \; ; find . -name "twohop_nulls.py" -exec git hash-object {} \;
F=$(find . -name "twohop_nulls.py" | head -1)
echo "== funcion ($F)"; grep -n "def neuropil_permutation" -A30 $F | cut -c1-170
echo "== paper 175-177"; sed -n '175p;177p' $V/docs/v2/paper1-v2.0.md | cut -c1-1200
echo "== evidencia cruda 30-60"; sed -n '30,60p' $A/docs/agents/evidencia/2026-08-24-null-anatomico-evidencia-cruda.md | cut -c1-200
echo "== 061 55-80"; sed -n '55,80p' $A/docs/agents/respuestas/2026-08-24-061-null-de-grado-sobre-los-2-saltos.md | cut -c1-220
