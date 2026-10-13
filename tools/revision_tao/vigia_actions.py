#!/usr/bin/env python3
"""Estado del ultimo run de factorial-mosca en la rama, via API publica (sin credenciales)."""
import json
import sys
import urllib.request

B = "https://api.github.com/repos/gatehot59-star/drosophila-fep-connectome/actions"


def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "brain-env"}), timeout=30) as r:
        return json.load(r)


runs = get(B + "/runs?branch=titan/factorial-mosca-2026-10-13&per_page=4")["workflow_runs"]
runs = [r for r in runs if r["name"] == "factorial-mosca"]
for r in runs[:2]:
    print("RUN", r["id"], r["head_sha"][:7], r["status"], r["conclusion"], r["created_at"], r["updated_at"])
r = runs[0] if len(sys.argv) < 2 else [x for x in runs if str(x["id"]) == sys.argv[1]][0]
for j in get(B + "/runs/%d/jobs?per_page=30" % r["id"])["jobs"]:
    pasos = [(s["number"], s["name"][:22], s["status"], s["conclusion"]) for s in j.get("steps", []) if s["status"] != "queued"]
    print("JOB", j["name"], j["status"], j["conclusion"], j.get("started_at"), j.get("completed_at"), pasos[-1:] if pasos else "")
