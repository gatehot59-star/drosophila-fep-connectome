// The sensory-to-motor routing table under the degree-preserving null, its range, and a
// side-by-side against the same observations scored under a uniform-density null.
//
// CHANGED FROM THE SCRIPT AS RUN: the input path was an absolute path on the machine
// this ran on. It is repository-relative here. Nothing else was modified.
//
// Run src/analyze_nulls40.mjs first; it writes results/n40_rows.json.
//
// The comparison at the end is the point of this script: the sign of every class is the
// same under both nulls, but the range is 283x under the degree-preserving null and 991x
// under uniform density, and the internal ordering of the depleted group changes. The
// difference is the degree sequence, so the degree-preserving figure is the reportable one.
import fs from "node:fs";
const f=JSON.parse(fs.readFileSync("results/n40_rows.json","utf8"));
const sens=f.filter(x=>[1,2,3,4,5,6,7,8].indexOf(x.gi)>=0);
sens.sort((a,b)=>a.ratio-b.ratio);
console.log("### JERARQUIA DE RUTEO bajo null con grado preservado (8 clases sensoriales)");
for(const x of sens) console.log("  "+x.nm.padEnd(12)+Number(x.ratio).toFixed(3)+"x"+(x.ratio>1?"  ENRIQUECIDO":"  DEPLETADO"));
const mn=sens[0], mx=sens[sens.length-1];
console.log("");
console.log("  minimo: "+mn.nm+" = "+mn.ratio.toFixed(4)+"x");
console.log("  maximo: "+mx.nm+" = "+mx.ratio.toFixed(4)+"x");
console.log("  RANGO  = "+(mx.ratio/mn.ratio).toFixed(1)+"x");
console.log("");
console.log("### comparacion de los dos nulls, mismo obs, distinto esperado");
const dens={visual:0.018,olfactory:0.050,mechano:12.378,gustatory:4.482,hygro:0.251,thermo:0.690,AN:17.839,unk_sens:12.858};
console.log("  clase        ratio_vs_densidad  ratio_vs_grado   cambia_signo");
for(const x of sens){
  const a=dens[x.nm], b=x.ratio;
  const sig=((a>1)!==(b>1))?"SI":"no";
  console.log("  "+x.nm.padEnd(12)+String(a).padStart(10)+"x"+(b.toFixed(3)+"x").padStart(16)+"      "+sig);
}
