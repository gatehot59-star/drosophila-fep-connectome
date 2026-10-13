#!/bin/bash
cd /workspace/tm_2026-10-12/rev_tao
M=main; V=titan_v2-cierre-2026-10-12; A=titan_materializacion-h4-guard-2026-10-02; E=titan_escape-motivo-2026-10-11; S=titan_swarm-lazo-cerrado-2026-10-11; T=titan_auditoria-tao-laboratorio-2026-10-12
P=$V/docs/v2/paper1-v2.0.md
echo "== F01 codigo"; grep -n "def neuropil_permutation" -A32 $M/src/twohop_nulls.py | cut -c1-170
echo "== F01 codigo v2 igual?"; md5sum $M/src/twohop_nulls.py $V/src/twohop_nulls.py
echo "== F01 texto"; grep -n -i -E "within blocks|within each block|combined degree|only within" $P | cut -c1-300
echo "== F05 texto"; grep -n -E "14[.,]8" $P | cut -c1-200
echo "== F06 texto"; grep -n -i -E "N ?= ?5|five (CP|null)|sufficient" $P | cut -c1-260
echo "== F07 texto"; grep -rn -E "138[.,]?14[0-9]" $P | cut -c1-220
echo "== F07 log agosto"; grep -rn -E "138[.,]?14[0-9]" $A --include=*.log --include=*.txt --include=*.md --include=*.json 2>/dev/null | cut -c1-220 | head -12
echo "== 015 del 11-oct"; grep -n -i -E "semilla 0|solo la semilla|semillas 0" $M/docs/agents/respuestas/2026-10-11-015-firma-de-la-014-y-en-criollo.md | cut -c1-300
echo "== firma log"; ls $E/results 2>/dev/null | head -30; grep -rln -i "firma" $E/results 2>/dev/null | head
echo "== 004"; grep -n -E "0[.,]743|semilla 2|nadie|0[.,]655" $M/docs/agents/respuestas/2026-10-12-004-memoria-dura-dbc3-contra-lstm.md | cut -c1-300
echo "== swarm"; grep -n -E "adc_to_q15|q15_to_pwm" -A5 $S/swarm/swarm_drone.h | cut -c1-170 | head -30; echo "asserts:"; grep -c -E "assert|abort|exit\(1|return 1" $S/swarm/test_swarm.c
echo "== recompute de Tao en brain-env"; python3 $T/docs/auditorias/2026-10-12-tao-recompute/recompute.py > recompute_brainenv.log 2>&1; echo "exit=$?"; tail -4 recompute_brainenv.log; md5sum recompute_brainenv.log $T/docs/auditorias/2026-10-12-tao-recompute/recompute.py; sha256sum $T/docs/auditorias/2026-10-12-tao-recompute/recompute.py
