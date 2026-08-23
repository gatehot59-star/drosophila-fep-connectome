// Statistics over results/nulls40.json: reciprocity, motor access per sensory class,
// and the learning-circuit wiring tests, each against the 40 degree-preserving nulls.
//
// CHANGED FROM THE SCRIPT AS RUN: the input and output paths were absolute paths on the
// machine this ran on. They are repository-relative here so that the commands in
// docs/METHODS.md work from a clone. Nothing else was modified.
//
// Note on z-scores: they are printed for direction only. The null distributions here
// have very small variance, so a z in the hundreds reflects a tight null, not an
// extraordinary effect. Report the ratio and the count of nulls exceeding the real value.
import fs from "node:fs";
const d=JSON.parse(fs.readFileSync("results/nulls40.json","utf8"));
const M=d.meta, G=M.G, GN=M.GN, gc=M.gc, NN=M.N, E=M.E;
const nulls=d.nulls;
console.log("meta: N="+NN+" E="+E+" sinapsis="+M.sinapsis+" nulls="+nulls.length);
console.log("md5 parquet="+M.md5_parquet+"  md5 annot="+M.md5_annot+"  SHA="+M.annot_sha);
console.log("densidad="+M.densidad.toPrecision(6));
const st=(a)=>{const n=a.length;const m=a.reduce((x,y)=>x+y,0)/n;const v=a.reduce((s,y)=>s+(y-m)*(y-m),0)/(n-1);return {m:m,sd:Math.sqrt(v),min:Math.min.apply(null,a),max:Math.max.apply(null,a)};};
const fm=(x,p)=>Number(x).toFixed(p===undefined?3:p);
console.log("");console.log("##### 1. RECIPROCIDAD #####");
const rr=d.real.rec, rn=nulls.map(x=>x.rec), s=st(rn);
console.log("real          = "+rr);
console.log("nulls mu      = "+fm(s.m,1)+"   sd = "+fm(s.sd,1)+"   min = "+s.min+"   max = "+s.max);
console.log("ratio real/null = "+fm(rr/s.m,2)+"x");
console.log("z             = "+fm((rr-s.m)/s.sd,1));
console.log("nulls >= real = "+rn.filter(x=>x>=rr).length+"/40    p_perm = "+fm((rn.filter(x=>x>=rr).length+1)/41,4));
const idx=(a,b)=>a*G+b;
const MOT=9;
console.log("");console.log("##### 2. ACCESO MOTOR EXCITATORIO POR CLASE, real vs 40 nulls #####");
console.log("clase".padEnd(14)+"N_src".padStart(7)+"obs".padStart(8)+"null_mu".padStart(10)+"null_sd".padStart(9)+"ratio".padStart(8)+"z".padStart(9)+"n>=obs".padStart(8)+"  p_perm");
const clases=[[1,"visual"],[2,"olfactory"],[3,"mechano"],[4,"gustatory"],[5,"hygro"],[6,"thermo"],[7,"AN"],[8,"unk_sens"],[10,"KenyonCell"],[11,"MBON"],[14,"ALPN"],[15,"optic_intr"]];
const filas=[];
for(const [gi,nm] of clases){
  const obs=d.real.Me[idx(gi,MOT)];
  const arr=nulls.map(x=>x.Me[idx(gi,MOT)]);
  const t=st(arr);
  const ge=arr.filter(x=>x>=obs).length;
  const le=arr.filter(x=>x<=obs).length;
  const z=t.sd>0?(obs-t.m)/t.sd:NaN;
  const p=(Math.min(ge,le)+1)/41;
  filas.push({nm:nm,gi:gi,obs:obs,mu:t.m,sd:t.sd,ratio:obs/t.m,z:z,ge:ge,p:p});
  console.log(nm.padEnd(14)+String(gc[gi]).padStart(7)+String(obs).padStart(8)+fm(t.m,1).padStart(10)+fm(t.sd,1).padStart(9)+(fm(obs/t.m,3)+"x").padStart(8)+fm(z,1).padStart(9)+String(ge).padStart(8)+"  "+fm(p,4));
}
console.log("");console.log("##### 3. KC->MBON: el test que decide si el centro de aprendizaje es cableado #####");
for(const [a,b,nm] of [[10,11,"KC->MBON"],[12,10,"DAN->KC"],[12,11,"DAN->MBON"],[10,10,"KC->KC"],[11,9,"MBON->MOTOR"],[3,10,"mechano->KC"],[2,10,"olfactory->KC"],[1,10,"visual->KC"],[14,10,"ALPN->KC"]]){
  const obs=d.real.Ma[idx(a,b)];
  const arr=nulls.map(x=>x.Ma[idx(a,b)]);
  const t=st(arr);
  const ge=arr.filter(x=>x>=obs).length, le=arr.filter(x=>x<=obs).length;
  const z=t.sd>0?(obs-t.m)/t.sd:NaN;
  console.log(nm.padEnd(16)+"obs="+String(obs).padStart(8)+"  null_mu="+fm(t.m,1).padStart(10)+"  sd="+fm(t.sd,1).padStart(8)+"  ratio="+(fm(obs/t.m,2)+"x").padStart(9)+"  z="+fm(z,1).padStart(8)+"  n>=obs="+ge+"  p="+fm((Math.min(ge,le)+1)/41,4));
}
console.log("");console.log("##### 4. VALIDACION DE INVARIANTES #####");
console.log("indeg_malos: "+nulls.map(x=>x.indeg_malos).join(","));
console.log("outdeg_malos max = "+Math.max.apply(null,nulls.map(x=>x.outdeg_malos)));
console.log("aristas_unicas distintas de E: "+nulls.filter(x=>x.aristas_unicas!==E).length+"/40");
console.log("swaps min="+Math.min.apply(null,nulls.map(x=>x.swaps))+" max="+Math.max.apply(null,nulls.map(x=>x.swaps)));
fs.writeFileSync("results/n40_rows.json",JSON.stringify(filas));
