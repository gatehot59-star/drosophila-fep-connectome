
import hashlib, json, time, gc, importlib.util, resource
from pathlib import Path
import numpy as np, pandas as pd, pyarrow as pa, pyarrow.compute as pc, pyarrow.parquet as pq, pyarrow.feather as pf
from scipy import stats
OUT = Path("/workspace/mecanismo-2026-11-02")
T0 = time.time()
def emit(tag, obj):
    print(tag, json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str), flush=True)
src = (OUT / "reuso_mosca.py").read_bytes()
assert hashlib.sha1(b"blob " + str(len(src)).encode() + b"\0" + src).hexdigest() == "37b358353ccac46c4b84766f1a63df556dfe531d"
spec = importlib.util.spec_from_file_location("reuso_mosca", OUT / "reuso_mosca.py")
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
BASE = {"flywire": dict(n_cab=996, n_pares_ffi=880, t2=698, n_x=1118), "banc": dict(n_cab=753, n_pares_ffi=622, t2=419, n_x=716)}
S_FOCUS = ["LC4", "LPLC1", "LPLC2", "LPLC4"]
D_FOCUS = ["DNp01", "DNp02", "DNp03", "DNp04", "DNp06", "DNp07", "DNp10", "DNp11"]
X_NAMED = ["AN_multi_11", "LHAD1g1", "PVLP010"]
def mode(s):
    v = pd.Series(s).value_counts(dropna=False)
    return None if len(v) == 0 else (None if pd.isna(v.index[0]) else str(v.index[0]))
def load_flywire():
    path = "/workspace/connectivity.parquet"
    t = pq.read_table(path, columns=["Presynaptic_Index", "Postsynaptic_Index", "Connectivity", "Excitatory"])
    pre = t["Presynaptic_Index"].to_numpy().astype(np.int32); post = t["Postsynaptic_Index"].to_numpy().astype(np.int32)
    w = t["Connectivity"].to_numpy().astype(np.int32); exc = t["Excitatory"].to_numpy().astype(np.int8)
    del t; gc.collect()
    n = int(max(pre.max(), post.max())) + 1
    root = np.zeros(n, dtype=np.int64)
    for a, b in (("Presynaptic_ID", "Presynaptic_Index"), ("Postsynaptic_ID", "Postsynaptic_Index")):
        t = pq.read_table(path, columns=[a, b]); ids = t[a].to_numpy(); ix = t[b].to_numpy(); del t
        root[ix] = ids
        assert np.array_equal(root[ix], ids)
        del ids, ix; gc.collect()
    inh = np.zeros(n, dtype=bool); inh[pre[exc < 0]] = True
    a = pd.read_csv("/workspace/annotations.tsv", sep=chr(9), dtype=str, usecols=["root_id", "cell_type", "side", "super_class", "cell_class", "top_nt", "top_nt_conf", "ito_lee_hemilineage"])
    a["root_id"] = a.root_id.astype(np.int64)
    a = a.drop_duplicates("root_id").set_index("root_id").reindex(root)
    d = base.armar(pre, post, w, inh, a.cell_type.to_numpy(dtype=object), a.side.to_numpy(dtype=object), a.super_class.to_numpy(dtype=object))
    meta = dict(sc=a.super_class.to_numpy(dtype=object), nt=a.top_nt.to_numpy(dtype=object), ntc=pd.to_numeric(a.top_nt_conf, errors="coerce").to_numpy(), lin=a.ito_lee_hemilineage.to_numpy(dtype=object), region=None, root=root)
    return d, meta
def load_banc():
    m = pd.read_feather("/workspace/banc_888/banc_888_meta.feather", columns=["root_888", "side", "super_class", "cell_type", "fafb_cell_type", "neurotransmitter_predicted", "neurotransmitter_score", "region", "hemilineage"])
    m = m.drop_duplicates("root_888").reset_index(drop=True)
    valid = m.root_888.notna().to_numpy()
    ids = np.full(len(m), -1, dtype=np.int64); ids[valid] = m.root_888[valid].astype("int64").to_numpy()
    vi = np.flatnonzero(valid); order = vi[np.argsort(ids[vi])]; sid = ids[order]
    t = pf.read_table("/workspace/banc_888/banc_888_edgelist_simple_v3.feather", columns=["pre", "post", "count"])
    out = []
    for col in ("pre", "post"):
        v = pc.cast(t[col], pa.int64()).to_numpy()
        pos = np.searchsorted(sid, v); pos[pos >= len(sid)] = 0
        if not (sid[pos] == v).all():
            raise ValueError("BANC ids outside meta")
        out.append(order[pos].astype(np.int32)); del v, pos; gc.collect()
    w = t["count"].to_numpy().astype(np.int32); del t; gc.collect()
    pre, post = out
    inh = m.neurotransmitter_predicted.isin(["gaba", "glutamate"]).to_numpy()
    tipo = m.fafb_cell_type.where(m.fafb_cell_type.notna(), m.cell_type).to_numpy(dtype=object)
    d = base.armar(pre, post, w, inh, tipo, m.side.to_numpy(dtype=object), m.super_class.to_numpy(dtype=object))
    meta = dict(sc=m.super_class.to_numpy(dtype=object), nt=m.neurotransmitter_predicted.to_numpy(dtype=object), ntc=pd.to_numeric(m.neurotransmitter_score, errors="coerce").to_numpy(), lin=m.hemilineage.to_numpy(dtype=object), region=m.region.to_numpy(dtype=object), root=ids)
    return d, meta
def census(name, d, meta):
    obs = base.estadisticas(d, d["post"], detalle=True)
    vals = {k: obs[k] for k in ("n_cab", "n_pares_ffi", "t2", "n_x")}
    emit("PARITY", dict(connectome=name, values=vals, expected=BASE[name], equal=vals == BASE[name]))
    assert vals == BASE[name]
    j, cab = obs["j"].copy(), obs["cab"]
    pre, post, w, S, D, inh, n = d["pre"], d["post"], d["w"], d["S"], d["D"], d["inh"], d["n"]
    cs, cd, tipo = d["cs"], d["cd"], d["tipo"]; nS, nD = len(cs), len(cd)
    xs = inh & ~d["excl"]; sS, dD = S[pre], D[post]
    m = (sS >= 0) & (dD >= 0)
    direct = np.bincount(sS[m].astype(np.int64) * nD + dD[m], weights=w[m], minlength=nS * nD)
    m1 = (sS >= 0) & xs[post]; k1 = sS[m1].astype(np.int64) * n + post[m1]
    u1, i1 = np.unique(k1, return_inverse=True); sx = pd.Series(np.bincount(i1, weights=w[m1]), index=u1)
    m2 = xs[pre] & (dD >= 0); k2 = pre[m2].astype(np.int64) * nD + dD[m2]
    u2, i2 = np.unique(k2, return_inverse=True); xd = pd.Series(np.bincount(i2, weights=w[m2]), index=u2)
    js, jx, jd = j.s.to_numpy().astype(np.int64), j.x.to_numpy().astype(np.int64), j.dd.to_numpy().astype(np.int64)
    j["w_sx"] = sx.reindex(js * n + jx).to_numpy(); j["w_xd"] = xd.reindex(jx * nD + jd).to_numpy(); j["w_sd"] = direct[js * nD + jd]
    j["s_type"] = [cs[s][0] for s in js]; j["s_side"] = [cs[s][1] for s in js]; j["d_type"] = [cd[x][0] for x in jd]; j["d_side"] = [cd[x][1] for x in jd]
    j["x_type"] = tipo[jx]; j["x_sc"] = meta["sc"][jx]; j["x_nt"] = meta["nt"][jx]; j["x_lin"] = meta["lin"][jx]; j["bottleneck"] = np.minimum(j.w_sx, j.w_xd)
    j.to_parquet(OUT / (name + "_closing_paths.parquet"))
    emit("CLOSING_ROWS", dict(connectome=name, rows=int(len(j)), pairs=int(len(j[["s", "dd"]].drop_duplicates())), x_neurons=int(j.x.nunique())))
    ex = j[j.s_type.isin(S_FOCUS) & j.d_type.isin(D_FOCUS)]
    for (st, ss, dt_, ds), g in ex.groupby(["s_type", "s_side", "d_type", "d_side"]):
        top = g.sort_values("bottleneck", ascending=False).drop_duplicates("x").head(4)
        emit("EXEMPLAR", dict(connectome=name, S=st, S_side=ss, D=dt_, D_side=ds, direct_syn=int(g.w_sd.iloc[0]), closing_X=int(g.x.nunique()), top_X=[dict(type=r.x_type, sc=r.x_sc, nt=r.x_nt, w_sx=int(r.w_sx), w_xd=int(r.w_xd)) for r in top.itertuples()]))
    for si, sk in enumerate(cs):
        if sk[0] not in S_FOCUS: continue
        for di, dk in enumerate(cd):
            if dk[0] in D_FOCUS and cab[si * nD + di] and not ((js == si) & (jd == di)).any():
                emit("EXEMPLAR_NO_X", dict(connectome=name, S=sk[0], S_side=sk[1], D=dk[0], D_side=dk[1], direct_syn=int(direct[si * nD + di])))
    hub = []
    for xt, g in j.groupby("x_type", dropna=False):
        u_sx = g.drop_duplicates(["s", "x"]); u_xd = g.drop_duplicates(["x", "dd"])
        hub.append(dict(type=None if pd.isna(xt) else str(xt), neurons=int(g.x.nunique()), d_types=int(g.dt.nunique()), s_types=int(g.s_type.nunique()), pairs=int(len(g[["s", "dd"]].drop_duplicates())), sc=mode(g.drop_duplicates("x").x_sc), nt=mode(g.drop_duplicates("x").x_nt), lin=mode(g.drop_duplicates("x").x_lin), syn_sx=int(u_sx.w_sx.sum()), syn_xd=int(u_xd.w_xd.sum())))
    hub = sorted(hub, key=lambda r: (-r["d_types"], -r["pairs"]))
    for r in hub[:20]: emit("HUB", dict(connectome=name, **r))
    for r in hub:
        if r["type"] in X_NAMED: emit("NAMED_X", dict(connectome=name, **r))
    xtot = j.drop_duplicates(["x", "dd"]); by = xtot.groupby("x_type").w_xd.sum().sort_values(ascending=False)
    emit("XD_CONCENTRATION", dict(connectome=name, x_types=int(len(by)), top10_share=float(by.head(10).sum() / by.sum()), top1=str(by.index[0]), top1_share=float(by.iloc[0] / by.sum())))
    sc_pre = meta["sc"]
    for di, dk in enumerate(cd):
        if dk[0] not in D_FOCUS: continue
        mu = dD == di
        if not mu.any(): continue
        tot = int(w[mu].sum()); mi = mu & inh[pre]; inh_syn = int(w[mi].sum())
        motif = np.unique(jx[jd == di]); mm = mi & np.isin(pre, motif); mot = int(w[mm].sum())
        tp = pd.Series(w[mi], index=pd.Index(tipo[pre[mi]].astype(str))).groupby(level=0).sum().sort_values(ascending=False).head(5)
        mot_types = set(str(x) for x in tipo[motif])
        emit("D_BUDGET", dict(connectome=name, D=dk[0], side=dk[1], neurons=int((D == di).sum()), input_syn=tot, inhibitory_syn=inh_syn, inhibitory_share=round(inh_syn / tot, 4) if tot else None, motif_X=int(len(motif)), motif_share_of_inhibitory=round(mot / inh_syn, 4) if inh_syn else None, top_inhibitory=[dict(type=k, share=round(v / inh_syn, 4), motif=k in mot_types) for k, v in tp.items()]))
    hubs = [r["type"] for r in hub[:15]] + [x for x in X_NAMED if x not in [r["type"] for r in hub[:15]]]
    reg = meta["region"]
    for xt in hubs:
        xn = np.flatnonzero(tipo.astype(str) == str(xt)) if xt is not None else np.array([], dtype=np.int64)
        xn = np.intersect1d(xn, np.unique(jx))
        if len(xn) == 0: emit("X_DRIVE_MISSING", dict(connectome=name, type=xt)); continue
        isx = np.zeros(n, dtype=bool); isx[xn] = True
        mi = isx[post]; tin = int(w[mi].sum())
        by_sc = pd.Series(w[mi], index=pd.Index(pd.Series(sc_pre[pre[mi]]).fillna("NA").astype(str))).groupby(level=0).sum().sort_values(ascending=False)
        from_S = int(w[mi & (S[pre] >= 0)].sum())
        res = dict(connectome=name, type=xt, neurons=int(len(xn)), input_syn=tin, from_eligible_S=round(from_S / tin, 4) if tin else None, input_by_superclass={k: round(v / tin, 4) for k, v in by_sc.head(6).items()})
        if reg is not None:
            by_reg = pd.Series(w[mi], index=pd.Index(pd.Series(reg[pre[mi]]).fillna("NA").astype(str))).groupby(level=0).sum().sort_values(ascending=False)
            res["input_by_region_of_presynaptic"] = {k: round(v / tin, 4) for k, v in by_reg.head(6).items()}
            res["X_region"] = mode(reg[xn])
        mo = isx[pre]; tout = int(w[mo].sum())
        res["output_syn"] = tout; res["output_to_D"] = round(int(w[mo & (D[post] >= 0)].sum()) / tout, 4) if tout else None
        res["nt"] = mode(meta["nt"][xn]); res["sc"] = mode(meta["sc"][xn])
        emit("X_DRIVE", res)
    if name == "flywire":
        np.savez_compressed(OUT / "flywire_units.npz", S=d["S"], D=d["D"], inh=d["inh"], excl=d["excl"], root=meta["root"], tipo=tipo.astype(str), sl=d["sl"])
        (OUT / "flywire_units.json").write_text(json.dumps(dict(cs=[list(x) for x in cs], cd=[list(x) for x in cd])))
    return {r["type"]: r["d_types"] for r in hub}
res = {}
for name, loader in (("flywire", load_flywire), ("banc", load_banc)):
    t = time.time(); d, meta = loader(); emit("LOADED", dict(connectome=name, neurons=int(d["n"]), rows=int(len(d["pre"])), S_units=len(d["cs"]), D_units=len(d["cd"]), seconds=round(time.time() - t, 1)))
    res[name] = census(name, d, meta)
    del d, meta; gc.collect()
shared = sorted(set(k for k in res["flywire"] if k) & set(k for k in res["banc"] if k))
if len(shared) > 2:
    rho = stats.spearmanr([res["flywire"][k] for k in shared], [res["banc"][k] for k in shared])
    topf = [k for k, _ in sorted(res["flywire"].items(), key=lambda x: -x[1])[:20]]; topb = [k for k, _ in sorted(res["banc"].items(), key=lambda x: -x[1])[:20]]
    emit("CROSS", dict(shared_x_types=len(shared), spearman_d_types=round(float(rho.statistic), 4), spearman_p=float(rho.pvalue), top20_overlap=sorted(set(topf) & set(topb))))
emit("DONE", dict(seconds=round(time.time() - T0, 1), maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
