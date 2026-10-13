#!/usr/bin/env python3
"""Genera los kernels de Kaggle del factorial 4 de la mosca (respuesta 2026-10-13-015) desde un plan json.

Uso: python3 generar_kernels.py <plan.json> <destino> [slug ...]
Cada kernel queda en <destino>/<slug>/ con <slug>.py (CONFIG del plan + cuerpo_kernel.py) y kernel-metadata.json.
El titulo es igual al slug porque Kaggle title-slugifica el ref y un titulo distinto da 403. Privado, GPU, con
internet (trae el repo en el SHA sellado y los insumos por URL, y verifica todos los md5 antes de correr).
"""
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def main():
    plan_p, destino = sys.argv[1], sys.argv[2]
    elegidos = set(sys.argv[3:])
    with open(plan_p) as f:
        plan = json.load(f)
    with open(os.path.join(AQUI, "cuerpo_kernel.py")) as f:
        cuerpo = f.read()
    n = 0
    for k in plan["kernels"]:
        slug = k["slug"]
        if elegidos and slug not in elegidos:
            continue
        cfg = dict(kernel=slug, respuesta=plan["respuesta"], sha=plan["sha_instrumento"], repo=plan["repo"],
                   tarball=plan["tarball"], script=plan["script"], md5=plan["md5"], insumos=plan["insumos"],
                   pip=plan["pip"], corridas=k["corridas"])
        codigo = ("#!/usr/bin/env python3\n# Kernel %s del factorial 4 de la mosca (respuesta %s). Generado por "
                  "tools/factorial4/kaggle/generar_kernels.py\n# desde %s; no editar a mano.\nimport json\n\n"
                  "CONFIG = json.loads(%r)\n\n" % (slug, plan["respuesta"], os.path.basename(plan_p),
                                                  json.dumps(cfg, sort_keys=True)) + cuerpo)
        d = os.path.join(destino, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, slug + ".py"), "w") as f:
            f.write(codigo)
        meta = dict(id="%s/%s" % (plan["cuenta"], slug), title=slug, code_file=slug + ".py", language="python",
                    kernel_type="script", is_private=True, enable_gpu=True, enable_tpu=False, enable_internet=True,
                    dataset_sources=[], competition_sources=[], kernel_sources=[], model_sources=[],
                    machine_shape=k.get("maquina", plan["maquina"]))
        with open(os.path.join(d, "kernel-metadata.json"), "w") as f:
            json.dump(meta, f, indent=1)
        n += 1
        print("kernel %s maquina=%s corridas=%d md5=%s" % (slug, meta["machine_shape"], len(k["corridas"]),
                                                          hashlib.md5(codigo.encode()).hexdigest()))
    print("kernels generados: %d" % n)
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
