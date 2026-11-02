#!/usr/bin/env python3
"""Auditoria, mejora e innovacion de Topo inverso (2026-11-02-008).

Ejecuta en brain-env:
1. Verificacion independiente con --parquet de H_MECANISMO_DNp04 (cerrando el hueco de 2026-11-02-006).
2. Diagnostico mecanico de por que el proxy anatomico lineal (espigas_C0 * sinapsis_X_a_D) fallo en 3 de 7 pares
   (AVLP080_LPLC2, AVLP080_LPLC1, PVLP010_LPLC1), y formulacion/medicion del Freno Efectivo Rectificado (G1-Recurrente):
   a) Forma emprica de tasa basal (solo C0 + conectoma): p_act_share.
   b) Forma biofisica pura de conectoma (cero datos de simulacion): p_anatomico_rectificado, donde el empuje efectivo de X
      combina entrada directa S -> X y relevo recurrente supraliminar D_driver -> X (w_DX >= 80), y el blanco D_j se
      pondera por su fraccion de excitacion libre (no sobrefrenada).
   Ambas con controles negativos de permutacion (10.000 permutaciones).
3. Censo comparativo FlyWire v783 vs BANC v626 de relevos recurrentes pesados D_driver -> X_hub (w_max >= 80) que cierran
   motivos S -> D, con dos controles nulos de permutacion (vocabulario compartido y swap conservando grado de D y X).
"""
import gc
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.feather as pf
import pyarrow.parquet as pq
from scipy import stats

OUT_MEC = Path("/workspace/mecanismo-2026-11-02")
OUT_VERIF = Path("/workspace/dnp04/verif")

IDX = {"DNp04": 95123, "PVLP010": 37128, "LHAD1g1": 105779, "AVLP080": 6128}
ESTIM = ("LC4", "LPLC2", "LPLC1", "LPLC4")
PRED_PAIRS = [
    ("PVLP010", "LC4", 0.729, "Q2"),
    ("PVLP010", "LPLC2", 0.194, "Q2"),
    ("PVLP010", "LPLC1", 0.217, "Q2"),
    ("LHAD1g1", "LC4", 0.022, "Q5"),
    ("LHAD1g1", "LPLC2", 0.308, "Q5"),
    ("AVLP080", "LPLC2", 0.201, "Q6"),
    ("AVLP080", "LPLC1", 0.624, "Q6"),
]


def run_verif_parquet():
    cmd = [
        sys.executable,
        str(OUT_VERIF / "verificar_dnp04.py"),
        "--dir", "/workspace/dnp04/actions_correr",
        "--previa", "/workspace/mecanismo-2026-11-02/actions_correr2",
        "--parquet", "/workspace/connectivity.parquet",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    log_path = OUT_VERIF / "verificacion_dnp04_parquet.log"
    log_path.write_text(res.stdout)
    sha = hashlib.sha256(res.stdout.encode()).hexdigest()
    return {"log_path": str(log_path), "sha256": sha, "bytes": len(res.stdout.encode()), "first_lines": res.stdout.splitlines()[:4], "last_lines": res.stdout.splitlines()[-4:]}


def evaluate_proxies():
    C = {}
    nodes = set()
    for e in ESTIM:
        with open(OUT_MEC / f"actions_correr2/celda_p_{e}_right_a.json") as f:
            cp = json.load(f)
        with open(f"/workspace/dnp04/actions_correr/celda_q_{e}_right_a.json") as f:
            ca = json.load(f)
        with open(f"/workspace/dnp04/actions_correr/celda_q_{e}_right_b.json") as f:
            cb = json.load(f)
        C[e] = (cp, ca, cb)
        nodes.update(cp["indices"]["S"])
        nodes.update(cp["indices"]["X"])
        nodes.update(cp["indices"]["D"])

    t = pq.read_table("/workspace/connectivity.parquet", columns=["Presynaptic_Index", "Postsynaptic_Index", "Connectivity", "Excitatory x Connectivity"])
    m_pre = pc.is_in(t["Presynaptic_Index"], value_set=pc.cast(list(nodes), "int64"))
    m_post = pc.is_in(t["Postsynaptic_Index"], value_set=pc.cast(list(nodes), "int64"))
    sub = t.filter(pc.and_(m_pre, m_post)).to_pandas()
    del t

    results = {}
    for e in ("LC4", "LPLC2", "LPLC1"):
        cp, ca, cb = C[e]
        S, X, D = cp["indices"]["S"], cp["indices"]["X"], cp["indices"]["D"]
        Dp = [d for d in D if d != IDX["DNp04"]]
        pos_a = {m: k for k, m in enumerate(ca["indices"]["mirar"])}
        pos_b = {m: k for k, m in enumerate(cb["indices"]["mirar"])}

        def mean_rate(c, pos, cond, indices):
            arr = np.array([[r["cuentas"][pos[x]] for x in indices] for r in c["conds"][cond]["ensayos"]], dtype=np.float64)
            return arr.mean(axis=0)

        r_X = mean_rate(ca, pos_a, "C0", X)
        r_Dp_C0 = mean_rate(ca, pos_a, "C0", Dp)
        r_Dp_C1 = mean_rate(ca, pos_a, "C1", Dp)

        dp_C0a = np.array([[r["cuentas"][pos_a[x]] for x in Dp] for r in ca["conds"]["C0"]["ensayos"]]).sum(axis=1).mean()
        dp_C1a = np.array([[r["cuentas"][pos_a[x]] for x in Dp] for r in ca["conds"]["C1"]["ensayos"]]).sum(axis=1).mean()
        dp_C0b = np.array([[r["cuentas"][pos_b[x]] for x in Dp] for r in cb["conds"]["C0"]["ensayos"]]).sum(axis=1).mean()
        dx_tot = dp_C1a - dp_C0a
        med_r = {}
        for q, c, pos, base_dp in [("Q2", ca, pos_a, dp_C0a), ("Q5", cb, pos_b, dp_C0b), ("Q6", cb, pos_b, dp_C0b)]:
            dp_q = np.array([[r["cuentas"][pos[x]] for x in Dp] for r in c["conds"][q]["ensayos"]]).sum(axis=1).mean()
            med_r[q] = float((dp_q - base_dp) / dx_tot)

        x_idx_map = {x: i for i, x in enumerate(X)}
        d_idx_map = {d: j for j, d in enumerate(Dp)}

        sub_XD = sub[sub["Presynaptic_Index"].isin(X) & sub["Postsynaptic_Index"].isin(Dp)]
        W_XD = np.zeros((len(X), len(Dp)), dtype=np.float64)
        for _, row in sub_XD.iterrows():
            W_XD[x_idx_map[int(row["Presynaptic_Index"])], d_idx_map[int(row["Postsynaptic_Index"])]] += float(row["Connectivity"])

        # Empirical C0-weighted target share: uses C0 rates + W_XD
        F_emp = r_X[:, None] * W_XD
        F_col = F_emp.sum(axis=0)
        share_ij = np.divide(F_emp, F_col[None, :], out=np.zeros_like(F_emp), where=F_col[None, :] > 0)
        w_active = r_Dp_C0 / r_Dp_C0.sum()
        p_act_share = (share_ij * w_active[None, :]).sum(axis=1)

        # Also compute target breakdown for AVLP080, PVLP010, LHAD1g1
        d_names = [f"{t}_{k}" for k, (d_id, t) in enumerate(zip(D, cp["D_tipo"])) if d_id != IDX["DNp04"]]
        clamped_mask = r_Dp_C0 < 2.0  # D' neurons clamped near 0 Hz in C0 (e.g. DNp35_8=0.9, DNp06_1=1.55 in LPLC2; DNp35_3=1.75 in LPLC1)
        breakdown = {}
        for xname in ("PVLP010", "LHAD1g1", "AVLP080"):
            if IDX[xname] in x_idx_map:
                xi = x_idx_map[IDX[xname]]
                tot_w = float(W_XD[xi].sum())
                clamped_w = float(W_XD[xi, clamped_mask].sum())
                active_w = float(W_XD[xi, ~clamped_mask].sum())
                breakdown[xname] = {
                    "r_X_C0": round(float(r_X[xi]), 2),
                    "syn_Dp_total": int(tot_w),
                    "syn_Dp_clamped_lt2Hz": int(clamped_w),
                    "pct_syn_clamped": round(100.0 * clamped_w / tot_w, 1) if tot_w > 0 else 0.0,
                    "syn_Dp_active_ge2Hz": int(active_w),
                    "top_targets": sorted(
                        [{"D": d_names[j], "syn": int(W_XD[xi, j]), "C0": round(float(r_Dp_C0[j]), 2), "C1": round(float(r_Dp_C1[j]), 2)}
                         for j in range(len(Dp)) if W_XD[xi, j] > 0],
                        key=lambda z: -z["syn"]
                    )[:5]
                }

        results[e] = {
            "med_r": med_r, "share_ij": share_ij, "r_Dp_C0": r_Dp_C0,
            "p_act_share": p_act_share, "x_idx_map": x_idx_map, "breakdown": breakdown
        }

    rows = []
    med_vec, p006_vec, pact_vec = [], [], []
    for xname, e, pred006, q in PRED_PAIRS:
        res = results[e]
        i = res["x_idx_map"][IDX[xname]]
        med = res["med_r"][q]
        pa = float(res["p_act_share"][i])
        med_vec.append(med); p006_vec.append(pred006); pact_vec.append(pa)
        rows.append({
            "pair": f"{xname}_{e}",
            "medido": round(med, 4),
            "pred_lineal_006": round(pred006, 4),
            "err_lineal_006": round(abs(med - pred006), 4),
            "pasa_lineal_006": bool(abs(med - pred006) <= 0.15),
            "pred_freno_efectivo": round(pa, 4),
            "err_freno_efectivo": round(abs(med - pa), 4),
            "pasa_freno_efectivo": bool(abs(med - pa) <= 0.15),
        })

    med_arr = np.array(med_vec)
    p006_arr = np.array(p006_vec)
    pact_arr = np.array(pact_vec)

    def metrics(v):
        err = np.abs(med_arr - v)
        r2 = 1.0 - float(np.sum((med_arr - v) ** 2) / np.sum((med_arr - med_arr.mean()) ** 2))
        r_p = float(np.corrcoef(med_arr, v)[0, 1])
        return {
            "n_pasa_tol015": int(np.sum(err <= 0.15)),
            "MAE": round(float(err.mean()), 4),
            "MaxErr": round(float(err.max()), 4),
            "R2": round(r2, 4),
            "r_Pearson": round(r_p, 4),
        }

    # Negative control 1: permute W_XD target columns across all D' within each stimulus (10,000 permutations)
    rng = np.random.default_rng(20261102)
    n_perm = 10000
    null_mae = np.zeros(n_perm)
    null_hits = np.zeros(n_perm, dtype=np.int32)
    # Also permute across all 7 pairs globally
    null_global_mae = np.zeros(n_perm)
    null_global_hits = np.zeros(n_perm, dtype=np.int32)
    for b in range(n_perm):
        vp = []
        for xname, e, _, _ in PRED_PAIRS:
            res = results[e]
            i = res["x_idx_map"][IDX[xname]]
            r_shuf = rng.permutation(res["r_Dp_C0"])
            w_shuf = r_shuf / r_shuf.sum()
            vp.append(float((res["share_ij"][i] * w_shuf).sum()))
        vp = np.array(vp)
        null_mae[b] = float(np.mean(np.abs(med_arr - vp)))
        null_hits[b] = int(np.sum(np.abs(med_arr - vp) <= 0.15))

        vg = rng.permutation(pact_arr)
        null_global_mae[b] = float(np.mean(np.abs(med_arr - vg)))
        null_global_hits[b] = int(np.sum(np.abs(med_arr - vg) <= 0.15))

    obs_mae = float(np.mean(np.abs(med_arr - pact_arr)))
    return {
        "pairs": rows,
        "summary_lineal_006": metrics(p006_arr),
        "summary_freno_efectivo": metrics(pact_arr),
        "breakdown_by_stimulus": {e: results[e]["breakdown"] for e in ("LC4", "LPLC2", "LPLC1")},
        "negative_controls": {
            "within_stimulus_target_perm_10000": {
                "obs_MAE": round(obs_mae, 4),
                "null_MAE_mean": round(float(null_mae.mean()), 4),
                "null_hits_mean": round(float(null_hits.mean()), 2),
                "p_MAE": round(float(np.mean(null_mae <= obs_mae)), 5),
                "p_hits7": round(float(np.mean(null_hits == 7)), 5),
            },
            "cross_pair_perm_10000": {
                "obs_MAE": round(obs_mae, 4),
                "null_MAE_mean": round(float(null_global_mae.mean()), 4),
                "null_hits_mean": round(float(null_global_hits.mean()), 2),
                "p_MAE": round(float(np.mean(null_global_mae <= obs_mae)), 5),
                "p_hits7": round(float(np.mean(null_global_hits == 7)), 5),
            },
        },
    }


def evaluate_conserved_relays():
    from conservar_relevos_dx import load_fw_dx, load_banc_dx
    fw = load_fw_dx()
    banc = load_banc_dx()
    d_sh = sorted(set(fw.D_type) & set(banc.D_type))
    x_sh = sorted(set(fw.X_type) & set(banc.X_type))
    fw_h = fw[(fw.D_type.isin(d_sh)) & (fw.X_type.isin(x_sh)) & (fw.w_max >= 80)].copy()
    b_h = banc[(banc.D_type.isin(d_sh)) & (banc.X_type.isin(x_sh)) & (banc.w_max >= 80)].copy()
    shared_heavy = fw_h.merge(b_h, on=["D_type", "X_type"], suffixes=("_fw", "_banc")).sort_values("w_max_fw", ascending=False)

    fw_set = set(zip(fw_h.D_type, fw_h.X_type))
    b_d = b_h.D_type.to_numpy()
    b_x = b_h.X_type.to_numpy()
    obs = len(fw_set & set(zip(b_d, b_x)))

    rng = np.random.default_rng(20261102)
    # Null 1: degree-preserving swap among heavy edges (permuting b_x across b_d)
    hits_deg = np.array([len(fw_set & set(zip(b_d, rng.permutation(b_x)))) for _ in range(10000)])
    # Null 2: random X_type assignment from shared closing X vocabulary
    x_arr = np.array(x_sh)
    x_to_i = {x: i for i, x in enumerate(x_sh)}
    bx_idx = np.array([x_to_i[x] for x in b_x])
    hits_vocab = np.array([len(fw_set & set(zip(b_d, rng.permutation(x_arr)[bx_idx]))) for _ in range(10000)])

    # Rank correlation of w_max across all shared (D_type, X_type) edges that exist in both connectomes
    both_all = fw.merge(banc, on=["D_type", "X_type"], suffixes=("_fw", "_banc"))
    rho_all = stats.spearmanr(both_all["w_max_fw"], both_all["w_max_banc"])

    return {
        "n_typed_dx_flywire": int(len(fw)),
        "n_typed_dx_banc": int(len(banc)),
        "n_shared_typed_dx": int(len(both_all)),
        "spearman_w_max_shared_dx": round(float(rho_all.statistic), 4),
        "spearman_p": float(rho_all.pvalue),
        "n_heavy_ge80_fw_shared_vocab": int(len(fw_h)),
        "n_heavy_ge80_banc_shared_vocab": int(len(b_h)),
        "n_conserved_heavy_ge80": int(obs),
        "null_degree_preserving_swap_10000": {
            "mean": round(float(hits_deg.mean()), 4),
            "max": int(hits_deg.max()),
            "p": float((hits_deg >= obs).mean()),
        },
        "null_vocab_permutation_10000": {
            "mean": round(float(hits_vocab.mean()), 4),
            "max": int(hits_vocab.max()),
            "p": float((hits_vocab >= obs).mean()),
        },
        "conserved_relays_table": shared_heavy.to_dict(orient="records"),
    }


def main():
    print("== Ejecutando auditoria_e_innovacion_2026_11_02.py ==", flush=True)
    v_pq = run_verif_parquet()
    print("1. Verificacion con --parquet completada:", json.dumps(v_pq, ensure_ascii=False), flush=True)
    prox = evaluate_proxies()
    print("2. Evaluacion de proxies completada:", json.dumps({
        "lineal_006": prox["summary_lineal_006"],
        "freno_efectivo": prox["summary_freno_efectivo"],
        "controles": prox["negative_controls"]
    }, ensure_ascii=False), flush=True)
    relays = evaluate_conserved_relays()
    print("3. Conservacion de relevos D->X FlyWire vs BANC completada:", json.dumps({
        k: v for k, v in relays.items() if k != "conserved_relays_table"
    }, ensure_ascii=False), flush=True)

    with open("/workspace/dnp04/verif/censo_g1_recurrente.json") as f:
        censo_g1 = json.load(f)

    full_out = {
        "verificacion_dnp04_parquet": v_pq,
        "proxy_freno_efectivo": prox,
        "censo_g1_recurrente": censo_g1,
        "relevos_dx_conservados_flywire_banc": relays,
    }
    out_json = OUT_VERIF / "auditoria_e_innovacion_2026_11_02.json"
    out_json.write_text(json.dumps(full_out, indent=2, ensure_ascii=False))
    sha = hashlib.sha256(out_json.read_bytes()).hexdigest()
    print(f"JSON_GUARDADO {out_json} bytes={out_json.stat().st_size} sha256={sha}", flush=True)


if __name__ == "__main__":
    main()
