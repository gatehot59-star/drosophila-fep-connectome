import urllib.request, urllib.error, json
H={'Accept':'application/vnd.github+json','User-Agent':'brain-env-a1-diagnostico'}
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=25) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]
s,rl=get('https://api.github.com/rate_limit'); print('RATE',s, rl['resources']['core'] if s==200 else rl)
s,runs=get('https://api.github.com/repos/gatehot59-star/drosophila-fep-connectome/actions/runs?branch=titan%2Fa1-runner-2026-11-03&per_page=20')
print('RUNS',s)
if s==200:
    rr=runs['workflow_runs']
    for r in rr:
        print('RUN',r['id'],r['name'],r['event'],r['head_sha'],r['status'],r['conclusion'],'created',r['created_at'],'started',r.get('run_started_at'),'updated',r['updated_at'],'attempt',r.get('run_attempt'))
    for r in rr:
        s2,jobs=get(r['jobs_url'])
        if s2!=200: print('JOBS',r['id'],s2,jobs); continue
        for j in jobs['jobs']:
            print('JOB',r['id'],j['id'],j['name'],j['status'],j['conclusion'],j['started_at'],j['completed_at'],j.get('runner_name'))
            for st in j['steps']:
                print('   STEP',st['number'],repr(st['name']),st['status'],st['conclusion'],st['started_at'],st['completed_at'])
else:
    print(runs)
