#!/usr/bin/env python3
"""Construye la tabla de prerregistro y guardas del diseno de corte causal para los otros 16 relevos
recurrentes conservados (H_MECANISMO_RELEVOS16, 2026-11-02-009) a partir de diseno_corte_16_relevos.json.
"""
import json
from pathlib import Path

with open("/workspace/dnp04/verif/diseno_corte_16_relevos.json") as f:
    relays = json.load(f)

other16 = [r for r in relays if not r["is_reference_006"]]
assert len(other16) == 16

design_16 = []
for idx_16, r in enumerate(other16, 1):
    e0 = r["edges"][0]
    di = e0["d_idx"]
    xi = e0["x_idx"]

    mirror = None
    for ed in r["edges"][1:]:
        if ed["d_side"] != e0["d_side"]:
            mirror = ed
            break

    if e0["w_Q1"] >= 162:
        tier = "T1_SUPRALIMINAR_1ESPIGA"
    elif r["X_type"] in ("CB0580", "CB0172", "CB0534", "PS100"):
        tier = "T2_HUB_CONVERGENTE_MULTI_D"
    else:
        tier = "T3_SUBUMBRAL_ALTO_80_161"

    # Stimulus protocol assignment:
    # - Regimen V (Visual canonico): si tiene entrada visual S directa con w_sd >= 20, se estimula S_canonico a 50 Hz.
    # - Regimen D (Activacion directa controlada de D_driver a 50 Hz Poisson): aisla el eslabon D_driver -> X_hub -| D'
    #   incluso cuando D_driver recibe entradas no visuales (central/LAL/ mecanosensorial).
    top_s = e0["top_S_onto_D_driver"]
    has_strong_vis = len(top_s) > 0 and top_s[0]["w_sd"] >= 20
    s_canon = f"{top_s[0]['s_type']}_{top_s[0]['s_side']}" if has_strong_vis else None

    design_16.append({
        "k": idx_16,
        "rank_17": r["rank"],
        "code": f"R{idx_16:02d}_{r['D_type']}_{r['X_type']}",
        "tier": tier,
        "D_type": r["D_type"],
        "X_type": r["X_type"],
        "x_nt": e0["x_nt"],
        "d_idx": di, "d_root": e0["d_root"], "d_side": e0["d_side"],
        "x_idx": xi, "x_root": e0["x_root"],
        "w_Q1_fw": e0["w_Q1"], "psp_peak_mV": e0["psp_peak_mV"],
        "w_max_banc": r["w_max_banc"],
        "regimen_visual_S": s_canon,
        "w_S_to_D_driver": int(top_s[0]["w_sd"]) if has_strong_vis else 0,
        "top_driver_no_visual": e0["top_any_exc_onto_D_driver"][:2],
        "guardas_filas": {
            "Q1": {"filas": e0["filas_Q1"], "peso_abs": e0["peso_Q1"]},
            "Q2": {"filas": e0["filas_Q2"], "peso_abs": e0["peso_Q2"]},
            "Q3": {"filas": e0["filas_Q3"], "peso_abs": e0["peso_Q3"]},
            "Q4": {"filas": e0["filas_Q4"], "peso_abs": e0["peso_Q4"]},
        },
        "mirror_contralateral": {
            "d_idx": mirror["d_idx"], "d_root": mirror["d_root"],
            "x_idx": mirror["x_idx"], "x_root": mirror["x_root"],
            "d_side": mirror["d_side"], "w_Q1": mirror["w_Q1"],
            "filas_Q1": mirror["filas_Q1"], "peso_Q1": mirror["peso_Q1"],
            "filas_Q2": mirror["filas_Q2"], "filas_Q3": mirror["filas_Q3"], "filas_Q4": mirror["filas_Q4"]
        } if mirror else None,
        "Dp_targets": {
            "n_Dp_total": e0["n_Dp_targets_inhibited"],
            "sum_w_XDp": e0["sum_w_XDp"],
            "max_w_XDp": e0["max_w_XDp"],
            "collateral_w_D_to_Dp": e0["sum_w_D_to_Dp_direct"],
            "top3": e0["top_Dp_targets"][:3]
        }
    })

out_file = Path("/workspace/dnp04/verif/sello_diseno_16_relevos.json")
out_file.write_text(json.dumps(design_16, indent=2, ensure_ascii=False))
print(f"Saved {out_file} ({out_file.stat().st_size} bytes)")
for d in design_16:
    top_dp = ", ".join([f"{x['D_target_type']}_{x['D_target_side']}({x['w_xd']})" for x in d["Dp_targets"]["top3"]])
    vis = f"{d['regimen_visual_S']}({d['w_S_to_D_driver']})" if d["regimen_visual_S"] else "CENTRAL:" + ",".join([f"{x['pre_type']}({x['w_in']})" for x in d["top_driver_no_visual"]])
    mir = f"{d['mirror_contralateral']['d_side']}({d['mirror_contralateral']['d_idx']}->{d['mirror_contralateral']['x_idx']},w={d['mirror_contralateral']['w_Q1']})" if d["mirror_contralateral"] else "SIN_PAR_GE80"
    print(f"R{d['k']:02d} [{d['tier'][:2]}] {d['D_type']:8s}({d['d_idx']:6d})->{d['X_type']:8s}({d['x_idx']:6d}) w={d['w_Q1_fw']:3d}({d['psp_peak_mV']:4.2f}mV)/BANC={d['w_max_banc']:3d} | Q1..Q4={d['guardas_filas']['Q1']['filas']}/{d['guardas_filas']['Q2']['filas']}/{d['guardas_filas']['Q3']['filas']}/{d['guardas_filas']['Q4']['filas']} | Mir:{mir} | In:[{vis}] | D':n={d['Dp_targets']['n_Dp_total']:3d} sum_XD'={d['Dp_targets']['sum_w_XDp']:4d} colat_DD'={d['Dp_targets']['collateral_w_D_to_Dp']:4d} [{top_dp}]")
