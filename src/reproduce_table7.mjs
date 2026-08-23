// Attempt to reproduce Table 7 of Mendieta (2026a) from the published analysis code.
//
// This is a NEGATIVE result and it is committed as one. Five metric variants and two
// floating-point precisions were tested; none reproduces the shape of Table 7's
// trajectory. See results/reproduce_table7.log for the output and docs/ERRATUM.md item 7a
// for what it establishes.
//
// The metric is reimplemented from the published pipeline, not approximated:
//   tau = 0.119, 200 steps, stimulus on steps 10..60 inclusive with amplitude 1.0
//   weights column-normalised by sum of absolute values, then scaled by 0.99
//   update: pre = W_transpose . h + s ; h = clip((1-tau)h + tau*tanh(pre), -2, 2)
//   the saved state is taken AFTER the update, at index t
//   per-region vector: mean of |h| per super_class, over ANNOTATED nodes only
//   metric: mean over modality pairs of (1 - cosine similarity)
//   modalities: cell_class in {visual}, {olfactory, ORN}, {mechanosensory}, each
//               filtered to flow == afferent. The 4-modality variant adds {gustatory}.
//
// float32 is EMULATED rather than approximated: Math.fround is applied to the
// matrix-vector product and to each term of the state update, because the published code
// stores h as np.float32. Running in float64 and calling it equivalent would have been an
// assumption; the two are compared instead and agree to 4.861e-5.
//
// INPUTS. Reads three binary caches of the parquet columns (presynaptic index,
// postsynaptic index, weight) rather than the parquet directly. Those caches were verified
// element-by-element against the file: 0 discrepancies across 15,091,983 rows. They are not
// committed here (60 MB each, and derived). To regenerate them, read the columns of
// 2025_Connectivity_783.parquet in row order into Int32Array, Int32Array and Float32Array.
//
// Also expects, in the working directory:
//   annotations.tsv          flyconnectome release v3.1.0, md5 719904abad876c68ace1b5690c9b9b63
//   idmap.json               map from root_id (string) to graph index
//   exact_bin.i32            per-node super_class bin, -1 for unannotated nodes
//   exact_meta.json          {names: [super_class names, sorted], cnt: [...], pops: [...]}
import fs from "node:fs";

const N = 138639;
const E = 15091983;
const TAU = 0.119;
const NSTEPS = 200;
const TS = 10;
const TE = 60;
const SAVE = [15, 60, 80, 120, 180, 195];

const pre = new Int32Array(fs.readFileSync("pre.i32").buffer.slice(0));
const post = new Int32Array(fs.readFileSync("post.i32").buffer.slice(0));
const w = new Float32Array(fs.readFileSync("w.f32").buffer.slice(0));
const bin = new Int32Array(fs.readFileSync("exact_bin.i32").buffer.slice(0));
const META = JSON.parse(fs.readFileSync("exact_meta.json", "utf8"));
const NS = META.names.length;
const idmap = JSON.parse(fs.readFileSync("idmap.json", "utf8"));

// Stimulated populations, exactly as the published get_sens() defines them.
const NL = String.fromCharCode(10);
const TB = String.fromCharCode(9);
const L = fs.readFileSync("annotations.tsv", "utf8").split(NL);
const H = L[0].split(TB);
const RI = H.indexOf("root_id");
const CI = H.indexOf("cell_class");
const FI = H.indexOf("flow");
const CLS = [
  ["visual", ["visual"]],
  ["olfactory", ["olfactory", "ORN"]],
  ["mechanosensory", ["mechanosensory"]],
  ["gustatory", ["gustatory"]]
];
const midx = [[], [], [], []];
for (let k = 1; k < L.length; k++) {
  const ln = L[k];
  if (!ln) continue;
  const q = ln.split(TB);
  const ix = idmap[q[RI]];
  if (ix === undefined) continue;
  if (q[FI] !== "afferent") continue;
  const c = q[CI] || "";
  for (let m = 0; m < 4; m++) if (CLS[m][1].indexOf(c) >= 0) midx[m].push(ix);
}
console.log("poblaciones afferent: " + CLS.map((c, k) => c[0] + "=" + midx[k].length).join("  "));

// Column-normalised weights in CSR by receiving node, matching normalize_W.
const cs = new Float64Array(N);
for (let e = 0; e < E; e++) cs[post[e]] += Math.abs(w[e]);
const ip = new Int32Array(N + 1);
for (let e = 0; e < E; e++) ip[post[e] + 1]++;
for (let j = 0; j < N; j++) ip[j + 1] += ip[j];
const idx = new Int32Array(E);
const val = new Float32Array(E);
const cur = Int32Array.from(ip.subarray(0, N));
for (let e = 0; e < E; e++) {
  const j = post[e];
  const s = cs[j];
  const k = cur[j]++;
  idx[k] = pre[e];
  val[k] = Math.fround(s > 1e-8 ? (w[e] / s) * 0.99 : w[e]);
}

const SS = new Set(SAVE);

/**
 * Propagate one modality for NSTEPS and return the per-region vector at each saved step.
 * State is float32, emulated with Math.fround on the product and on each update term.
 * @param {number[]} stim graph indices of the stimulated population
 * @returns {Float64Array[]} one vector of length NS per entry of SAVE, in SAVE order
 */
function propagate(stim) {
  const h = new Float32Array(N);
  const y = new Float32Array(N);
  const st = new Uint8Array(N);
  for (const q of stim) st[q] = 1;
  const rows = [];
  for (let t = 0; t < NSTEPS; t++) {
    for (let j = 0; j < N; j++) {
      let s = 0;
      for (let k = ip[j]; k < ip[j + 1]; k++) s += val[k] * h[idx[k]];
      y[j] = Math.fround(s);
    }
    for (let i = 0; i < N; i++) {
      const v = y[i] + ((t >= TS && t <= TE && st[i]) ? 1 : 0);
      const x = Math.fround(Math.fround((1 - TAU) * h[i]) + Math.fround(TAU * Math.tanh(v)));
      h[i] = x > 2 ? 2 : (x < -2 ? -2 : x);
    }
    if (SS.has(t)) {
      const vv = new Float64Array(NS);
      const cc = new Float64Array(NS);
      for (let i = 0; i < N; i++) {
        const b = bin[i];
        if (b < 0) continue;
        vv[b] += Math.abs(h[i]);
        cc[b]++;
      }
      for (let b = 0; b < NS; b++) if (cc[b] > 0) vv[b] /= cc[b];
      rows.push(vv);
    }
  }
  return rows;
}

/**
 * Mean pairwise cosine distance across modality vectors, matching rdi_cosine.
 * @param {Float64Array[]} vs one per-region vector per modality
 * @returns {number} mean of (1 - cosine similarity) over all pairs, 0 if no valid pair
 */
function cosrdi(vs) {
  const d = [];
  for (let i = 0; i < vs.length; i++) {
    for (let j = i + 1; j < vs.length; j++) {
      const a = vs[i];
      const b = vs[j];
      let na = 0;
      let nb = 0;
      let dp = 0;
      for (let k = 0; k < NS; k++) {
        na += a[k] * a[k];
        nb += b[k] * b[k];
        dp += a[k] * b[k];
      }
      na = Math.sqrt(na);
      nb = Math.sqrt(nb);
      if (na > 1e-15 && nb > 1e-15) d.push(1.0 - dp / (na * nb + 1e-15));
    }
  }
  return d.length ? d.reduce((x, y2) => x + y2, 0) / d.length : 0;
}

const V = [];
for (let m = 0; m < 4; m++) {
  const a = Date.now();
  V.push(propagate(midx[m]));
  console.log("  " + CLS[m][0] + " listo (" + ((Date.now() - a) / 1000).toFixed(0) + "s)");
}

const T7 = { 15: 0.6869, 60: 0.6304, 80: 0.6797, 120: 0.8071, 180: 0.8318, 195: 0.8328 };
const F64 = { 15: 0.0043, 60: 0.0818, 80: 0.5998, 120: 0.7636, 180: 0.7830, 195: 0.7842 };

const r3 = [];
const r4 = [];
for (let ti = 0; ti < SAVE.length; ti++) {
  r3.push(cosrdi([V[0][ti], V[1][ti], V[2][ti]]));
  r4.push(cosrdi([V[0][ti], V[1][ti], V[2][ti], V[3][ti]]));
}

console.log("");
console.log("variante".padEnd(40) + SAVE.map((t) => String(t).padStart(8)).join(""));
console.log("Tabla 7 del paper".padEnd(40) + SAVE.map((t) => T7[t].toFixed(4).padStart(8)).join(""));
console.log("float32, 3 modalidades (3 pares)".padEnd(40) + r3.map((x) => x.toFixed(4).padStart(8)).join(""));
console.log("float32, 4 modalidades (6 pares)".padEnd(40) + r4.map((x) => x.toFixed(4).padStart(8)).join(""));
console.log("float64, 3 modalidades (medido antes)".padEnd(40) + SAVE.map((t) => F64[t].toFixed(4).padStart(8)).join(""));
console.log("");
console.log("float32 vs float64, 3 modalidades: peor difabs = " +
  Math.max.apply(null, SAVE.map((t, i) => Math.abs(r3[i] - F64[t]))).toExponential(3));

fs.writeFileSync("reproduce_table7.json", JSON.stringify({ save: SAVE, r3: r3, r4: r4, pops: midx.map((x) => x.length) }));
