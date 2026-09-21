from pathlib import Path
import tempfile, subprocess, os, sys, json, importlib.util, hashlib
root=Path(__file__).resolve().parents[3]
base=Path(tempfile.mkdtemp(prefix='haipipe-run-runtime-',dir='/private/tmp'))
workspace=base/'workspace';(workspace/'code').mkdir(parents=True);(workspace/'pyproject.toml').write_text('')
job=workspace/'Proj/tasks/b01_test/j01_demo';task=job/'t01_model'
(task/'runs').mkdir(parents=True);(task/'scripts/config').mkdir(parents=True)
page=task/'t01_model.md';page.write_text('# Model\nfolder-kind: task\ntask: .\n')
(job.parent/'board.md').write_text('# Tasks\nboard-kind: task-block\n')
worker=task/'scripts/worker.py'
worker.write_text('''from pathlib import Path
import os,sys
cfg=Path(os.environ['HAIPIPE_CONFIG']); counter=cfg.with_suffix('.count')
n=int(counter.read_text())+1 if counter.exists() else 1; counter.write_text(str(n))
out=Path(os.environ['RESULT_DIR']);(out/'metrics.json').write_text('{"attempt":'+str(n)+'}')
sys.exit(1 if n==1 else 0)
''')
bin_dir=base/'bin';bin_dir.mkdir();(bin_dir/'python').symlink_to(sys.executable)
env=dict(os.environ,PATH=str(bin_dir)+os.pathsep+os.environ['PATH'],PYTHONDONTWRITEBYTECODE='1')
env.pop('RESULT_STORE',None)
template=(root/'plugins/haipipe-toolkit/skills/task/haipipe-task/ref/run-sh-template.sh').read_text()
log=[]
def make_run(stem):
    ticket=task/'runs'/f'{stem}.sh';ticket.write_text(template)
    cfg=task/'scripts/config'/f'{stem}.yaml';cfg.write_text('notebook: off\nskip_review: true\n')
    result=task/'results'/stem;result.mkdir(parents=True)
    (result/'runtime.yaml').write_text(f'run: {stem}\nstatus: planned\nstarted_at: null\nfinished_at: null\n')
    return ticket,cfg,result

def invoke(ticket):
    proc=subprocess.run(['bash',str(ticket)],env=env,text=True,capture_output=True)
    log.append(dict(ticket=ticket.name,exit=proc.returncode,stdout=proc.stdout,stderr=proc.stderr))
    return proc.returncode

ticket,cfg,result=make_run('r01_execution_fit')
assert invoke(ticket)==1
first=(result/'runtime.yaml').read_bytes()
assert invoke(ticket)==0
second=(result/'runtime.yaml').read_text()
assert 'attempt:    2' in second and 'status:     complete' in second
assert (result/'attempts/000001/runtime.yaml').read_bytes()==first
assert invoke(ticket)==2
assert (result/'runtime.yaml').read_text()==second
changed,cfg2,result2=make_run('r02_execution_fit')
assert invoke(changed)==1
before=(result2/'runtime.yaml').read_bytes();cfg2.write_text(cfg2.read_text()+'changed: true\n')
assert invoke(changed)==2
assert (result2/'runtime.yaml').read_bytes()==before
assert not (result2/'attempts').exists()

# Read-only consumers must count the current Run, not its archived attempt.
sys.path[:0]=[str(root/'plugins/haipipe-toolkit/skills/board/haipipe-board'),str(root/'plugins/haipipe-toolkit/skills/page/haipipe-page')]
from live.runs import local_runs, _status
rows=local_runs(page)
assert len(rows)==2,rows
assert all('attempts' not in str(r['runtime']) for r in rows)
assert sum(r['status']=='Done' for r in rows)==1
assert _status(None,{})=='Held'

# Paper judgment is displayed only as complete with a native human-close journal.
paper=base/'story';paper.mkdir();paper_page=paper/'story.md';paper_page.write_text('# Story\n')
(paper/'runs').mkdir();rid='rclaim-01_support'
(paper/'runs'/f'{rid}.md').write_text(f'---\nrun: {rid}\nfamily: paper\noperation: judgment\ntarget: E5\n---\n')
pr=paper/'results'/rid;pr.mkdir(parents=True)
(pr/'runtime.yaml').write_text(f'run: {rid}\nfamily: paper\noperation: judgment\nstatus: complete\nversion: v001\n')
(pr/'v001.md').write_text('## Step s001\n### Saved result\nConcern recorded\n')
assert local_runs(paper_page)[0]['status']=='Held'
(pr/'v001.md').write_text('## Version closure\n### Human close\nNamed person: record this scoped concern; discussion closed.\n')
assert local_runs(paper_page)[0]['status']=='Done'

# Commission is a valid Design Run; a receiptless Ticket and orphan Result remain visible.
design=base/'design';design.mkdir();dp=design/'design.md';dp.write_text('# Design\n')
(design/'runs').mkdir();d='rd01_commission_item01'
(design/'runs'/f'{d}.yaml').write_text(f'run: {d}\nfamily: design\noperation: commission\n')
dr=design/'results'/d;dr.mkdir(parents=True)
(dr/'runtime.yaml').write_text(f'run: {d}\nfamily: design\noperation: commission\nstatus: complete\n')
(dr/'decision.yaml').write_text('decision: release\n')
assert local_runs(dp)[0]['status']=='Done'
(design/'runs/r02_execution_missing.sh').write_text('#!/bin/sh\n')
(design/'results/r03_execution_orphan').mkdir()
ds=local_runs(dp);assert len(ds)==3 and sum(r['status']=='Held' for r in ds)==2,ds

# Declared mirrored Task store must be read by both inventory consumers.
mirror=base/'store';(job/'src').mkdir();(job/'src/config-defaults.yaml').write_text(f'store: {mirror}\n')
remote_stem='r04_execution_remote';(task/'runs'/f'{remote_stem}.sh').write_text('#!/bin/sh\n')
remote=mirror/job.parent.name/job.name/task.name/'results'/remote_stem;remote.mkdir(parents=True)
(remote/'runtime.yaml').write_text(f'run: {remote_stem}\nstatus: planned\n')
assert any(r['runtime']==remote/'runtime.yaml' and r['status']=='Ready' for r in local_runs(page))
path=root/'plugins/haipipe-toolkit/skills/0_utils/table-task/ref/render_task_table.py'
spec=importlib.util.spec_from_file_location('run_task_table',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
findings=[];t=m.scan_task(task,job,'b01j01',findings)
assert any(r['run']==remote_stem and r['status']=='Ready' for r in t['runs']),t['runs']
missing=task/'runs/r05_execution_missing.sh';missing.write_text('#!/bin/sh\n')
findings=[];t=m.scan_task(task,job,'b01j01',findings)
assert next(r for r in t['runs'] if r['run']==missing.stem)['status']=='Held'
assert any('Ticket without runtime' in f for f in findings)
assert m.task_status([{'status':'Waiting'}])['word']=='Waiting'
checks=['retry preserves prior receipt','attempt counter','complete immutable','changed contract blocked','attempts excluded from inventory','Paper judgment closure','Design Commission','missing receipt and orphan visibility','mirrored Task store in both readers','waiting state']

# Current and historical duplicate locations identify one logical Run.
import shutil
duplicate=task/'results'/remote_stem
duplicate.mkdir();shutil.copy2(remote/'runtime.yaml',duplicate/'runtime.yaml')
dups=[r for r in local_runs(page) if r['ticket'] and r['ticket'].stem==remote_stem]
assert len(dups)==1 and dups[0]['status']=='Held' and any('multiple' in a for a in dups[0]['audit'])
findings=[];t=m.scan_task(task,job,'b01j01',findings)
assert sum(r['run']==remote_stem for r in t['runs'])==1
assert next(r for r in t['runs'] if r['run']==remote_stem)['status']=='Held'
checks.append('duplicate receipts stay one Held row in both readers')
orphan='r06_execution_orphan'
for result_root in (task/'results',mirror/job.parent.name/job.name/task.name/'results'):
    d=result_root/orphan;d.mkdir();(d/'runtime.yaml').write_text(f'run: {orphan}\nstatus: failed\n')
orphans=[r for r in local_runs(page) if r['result_path'] and r['result_path'].name==orphan]
assert len(orphans)==1 and any('multiple' in a for a in orphans[0]['audit'])
checks.append('duplicate orphan Results stay one recovery row')

# Resolve relative stores using a SPACE marker, then a checkout, or report a gap.
from live.runs import _task_result_locations
(job/'src/config-defaults.yaml').write_text('store: mirror\n')
loc=_task_result_locations(task,job)
assert loc[0][0]==workspace/'mirror'/job.parent.name/job.name/task.name/'results'
(workspace/'pyproject.toml').unlink();(workspace/'.git').mkdir()
assert _task_result_locations(task,job)[0][0]==loc[0][0]
(workspace/'.git').rmdir()
store_findings=[];loc=_task_result_locations(task,job,store_findings)
assert loc[0][0]==task/'results' and store_findings
findings=[];m.scan_task(task,job,'b01j01',findings)
assert any('cannot resolve relative declared store' in f for f in findings)
checks.append('relative store marker, git fallback and unresolved diagnosis')
(workspace/'pyproject.toml').write_text('');(job/'src/config-defaults.yaml').unlink()

# Frozen inputs must refer to actual bytes, including explicitly pinned hashes.
input_path=job/'input.txt';input_path.write_text('frozen A')
auto,_,ar=make_run('r07_execution_input')
auto.write_text(auto.read_text().replace('RUN_INPUTS=()', 'RUN_INPUTS=("input.txt|auto")'))
assert invoke(auto)==1
old=(ar/'runtime.yaml').read_bytes();input_path.write_text('changed B')
assert invoke(auto)==2 and (ar/'runtime.yaml').read_bytes()==old
assert not (ar/'attempts').exists()
checks.append('changed auto-hashed input blocks retry')
pinned,_,pr=make_run('r08_execution_pinned')
pin=hashlib.sha256(input_path.read_bytes()).hexdigest()
pinned.write_text(pinned.read_text().replace('RUN_INPUTS=()',f'RUN_INPUTS=("input.txt|{pin}")'))
assert invoke(pinned)==1
old=(pr/'runtime.yaml').read_bytes();input_path.write_text('changed C')
assert invoke(pinned)==2 and (pr/'runtime.yaml').read_bytes()==old
assert 'declared input hash changed' in log[-1]['stderr']
checks.append('explicit input hash verified against current bytes')
input_path.unlink()
auto_before=(ar/'runtime.yaml').read_bytes()
assert invoke(auto)==2 and (ar/'runtime.yaml').read_bytes()==auto_before
assert 'declared input is not a readable file' in log[-1]['stderr']
checks.append('missing declared input blocks launch')

# Default reports retain recovery rows even when the rest of the table is shown.
(job/'src/config-defaults.yaml').write_text(f'store: {mirror}\n')
blocks,findings=m.scan(workspace/'Proj/tasks')
report=m.render(workspace/'Proj/tasks',blocks,findings,'all','md')
overview=report.split('## Runs Overview',1)[1].split('## Store Slots',1)[0]
assert missing.stem in overview and 'missing runtime receipt' in overview
assert 'conflicting runtime receipts' in overview
checks.append('default Task report keeps recovery rows visible')

(base/'checks.json').write_text(json.dumps(dict(status='passed',checks=checks,log=log),indent=2))
print(base)
print(f'{len(checks)} runtime behavior checks passed')
