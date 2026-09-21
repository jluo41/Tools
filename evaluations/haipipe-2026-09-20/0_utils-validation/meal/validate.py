import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path('/tmp/mealcam-fresh-20260920')
SKILL = Path('/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/0_utils/meal-cam-logger')
text = (SKILL / 'SKILL.md').read_text()
blocks = re.findall(r'```bash\n(.*?)```', text, re.S)
assert len(blocks) == 3, len(blocks)
for name, body in zip(('start', 'identity', 'stop'), blocks):
    (ROOT / (name + '.sh')).write_text(body)
ENV = dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin', PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT), MEAL_CAM_PYTHON=sys.executable, MEAL_CAM_SKILL_DIR=str(SKILL.resolve()), MEAL_CAM_OUTPUT_DIR=str(ROOT / 'receipts'))
sessions = []
checks = []
commands = []
source_hashes = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SKILL/'SKILL.md', SKILL/'scripts/meal_cam_loop.py', SKILL/'scripts/episode_tracker.py']}

def record(name, condition, detail):
    checks.append(dict(check=name, passed=bool(condition), detail=detail))
    print(('PASS ' if condition else 'FAIL ') + name + ': ' + str(detail), flush=True)
    if not condition:
        raise AssertionError(name)

def shell(code, env, title, timeout=18):
    path = ROOT / ('command-%02d-%s.sh' % (len(commands)+1, title))
    path.write_text(code)
    result = subprocess.run(['/bin/bash', str(path)], env=env, text=True, capture_output=True, timeout=timeout)
    commands.append(dict(title=title, command='/bin/bash ' + str(path), exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr))
    (path.with_suffix('.stdout.txt')).write_text(result.stdout)
    (path.with_suffix('.stderr.txt')).write_text(result.stderr)
    if result.returncode:
        raise RuntimeError('%s failed: %s %s' % (title, result.stdout, result.stderr))
    return result

def wait_for(predicate, timeout=8):
    end = time.monotonic()+timeout
    while time.monotonic() < end:
        if predicate():
            return
        time.sleep(.1)
    raise AssertionError('timed out waiting for expected local event')

def events(s):
    return [json.loads(line) for line in s['audit'].read_text().splitlines()]

def command(s, code, title):
    env = dict(s['env'], MEAL_CAM_CONTROL_DIR=str(s['control']))
    return shell(blocks[1]+'\n'+code, env, s['name']+'-'+title)

def start(name, label, bites='1,31'):
    audit = ROOT / (name+'.audit.jsonl')
    env = dict(ENV, MEAL_TEST_LABEL=label, MEAL_TEST_BITES=bites, MEAL_TEST_AUDIT=str(audit))
    result = shell(blocks[0], env, name+'-start')
    pid = int(re.search(r'^PID=(\d+)$', result.stdout, re.M)[1])
    control = Path(re.search(r'^PID_FILE=(.+)$', result.stdout, re.M)[1]).parent
    log = control / 'run.log'
    receipt = Path(re.search(r'session_file=([^\n]+)', log.read_text())[1])
    s = dict(name=name, env=env, pid=pid, control=control, log=log, receipt=receipt, audit=audit)
    sessions.append(s)
    verify = command(s, 'check_meal_cam_process', 'verify-start')
    record(name+' started', 'started.' in log.read_text() and receipt.exists() and 'Verified meal-cam PID' in verify.stdout, str(receipt))
    return s

def stop(s):
    command(s, blocks[2], 'stop')
    final = s['receipt'].read_text()
    record(s['name']+' final receipt', '**Status:**   stopped' in final and 'In progress' not in final and '[meal-cam] stopped.' in s['log'].read_text(), final)
    record(s['name']+' resources closed', sum(e['kind']=='capture_release' for e in events(s))==1 and sum(e['kind']=='detector_close' for e in events(s))==1, 'one capture release and one detector close')
    rejected = command(s, 'if check_meal_cam_process; then exit 9; fi', 'reject-stopped-pid')
    record(s['name']+' stale PID rejected', 'No matching live' in rejected.stdout, rejected.stdout.strip())

try:
    main = start('meal', 'test salad')
    wait_for(lambda:'(2 bites)' in main['receipt'].read_text())
    progress = main['receipt'].read_text()
    (ROOT/'meal-progress.md').write_text(progress)
    record('meal progress', '**Status:**   running' in progress and '(2 bites)  test salad' in progress, progress)
    record('one identification for repeated bites', sum(e['kind']=='fake_identify' for e in events(main))==1, '2 injected bites grouped in one actual EpisodeTracker episode')
    command(main, 'if check_meal_cam_process; then kill -STOP "$MEAL_CAM_PID"; else exit 1; fi\nps -p "$MEAL_CAM_PID" -o stat=', 'pause')
    time.sleep(.2)
    paused_audit = main['audit'].read_bytes()
    paused_receipt = main['receipt'].read_bytes()
    time.sleep(1.4)
    state = subprocess.check_output(['/bin/ps', '-p', str(main['pid']), '-o', 'stat='], text=True).strip()
    record('pause suspends capture and receipt', 'T' in state and main['audit'].read_bytes()==paused_audit and main['receipt'].read_bytes()==paused_receipt, 'process stat='+state+'; unchanged for 1.4 sec')
    stop(main)
    duration = re.search(r'Duration:\*\* (\d+) min (\d+) sec', main['receipt'].read_text())
    record('duration includes pause', int(duration[1])*60+int(duration[2]) >= 4, duration[0])

    empty = start('empty', 'unused', bites='')
    record('empty startup receipt', 'No bite episodes detected.' in empty['receipt'].read_text(), str(empty['receipt']))
    command(empty, 'if check_meal_cam_process; then kill -USR1 "$MEAL_CAM_PID"; else exit 1; fi', 'skip-empty')
    wait_for(lambda:'no episode to remove' in empty['log'].read_text())
    stop(empty)
    record('empty finalized without identification', 'No bite episodes detected.' in empty['receipt'].read_text() and not any(e['kind']=='fake_identify' for e in events(empty)), empty['receipt'].read_text())

    first = start('independent-a', 'test apple')
    second = start('independent-b', 'test soup')
    wait_for(lambda:'(2 bites)' in second['receipt'].read_text())
    record('independent controls and receipts', first['pid']!=second['pid'] and first['control']!=second['control'] and first['receipt']!=second['receipt'], {'a':str(first['receipt']), 'b':str(second['receipt'])})
    other_before = second['receipt'].read_bytes()
    command(first, 'if check_meal_cam_process; then kill -USR1 "$MEAL_CAM_PID"; else exit 1; fi', 'skip-last')
    wait_for(lambda:'removed episode #1' in first['log'].read_text())
    record('skip affects only selected session', 'No bite episodes detected.' in first['receipt'].read_text() and second['receipt'].read_bytes()==other_before, 'A whole episode removed; B still has 2 bites of test soup')
    stop(first)
    live = command(second, 'check_meal_cam_process', 'verify-after-other-stop')
    record('other session remains running', 'Verified' in live.stdout and '**Status:**   running' in second['receipt'].read_text(), live.stdout.strip())
    stop(second)
    record('final outputs remain independent', 'test salad' in main['receipt'].read_text() and 'No bite episodes' in first['receipt'].read_text() and 'test soup' in second['receipt'].read_text(), 'read each exact startup session_file; all four files exist')
    record('sources unchanged', all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==digest for p,digest in source_hashes.items()), 'SKILL.md, meal_cam_loop.py, episode_tracker.py')
finally:
    for s in sessions:
        try:
            args = subprocess.check_output(['/bin/ps', '-p', str(s['pid']), '-o', 'args='], text=True)
            if str(SKILL/'scripts/meal_cam_loop.py') in args:
                command(s, blocks[2], 'cleanup-stop')
        except subprocess.CalledProcessError:
            pass
    result = dict(checks=checks, commands=commands, source_sha256=source_hashes, sessions=[{key:str(s[key]) for key in ('name','pid','control','log','receipt','audit')} for s in sessions])
    (ROOT/'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    summary = ['# Meal-cam fresh-context validation', '', 'Executed production meal_cam_loop.py and EpisodeTracker with deterministic dependency substitutes. No repository source changes.', '', '## Result', '', '%s / %s assertions passed.' % (sum(c['passed'] for c in checks),len(checks)), '', '## Scope', '', 'Real: bash launch/identity/pause/stop commands copied verbatim from current SKILL; OS signals; production capture loop, grouping, render, finalization, cleanup dispatch. Start paths restored in separate shell invocations.', '', 'Substituted: cv2 capture/color/JPEG (no actual image), BiteDetector event outputs (frames 1 and 31, or none), Anthropic client label response. Socket connections disabled; clean child environment omitted credentials. No camera, model downloads, network, API, or package installation.', '', 'Unverified: real camera opening/permissions/backend behavior; MediaPipe initialization/model downloads/detection accuracy/cooldown; genuine JPEG encoding; actual Anthropic authentication, network, responses, error behavior, latency and billing. Linux/Windows were not run.', '', '## Checks', '']
    summary += ['- '+('PASS' if c['passed'] else 'FAIL')+' '+c['check'] for c in checks]
    summary += ['', '## Commands and artifacts', '', 'Run: `python3 /tmp/mealcam-fresh-20260920/validate.py` (requires process inspection allowed by sandbox).', '', 'All exact shell commands, stdout/stderr, audit events and JSON results are alongside this receipt. Skill bash blocks saved as start.sh, identity.sh, stop.sh.', '', '## Friction', '', 'Environment: sandbox denied ps before execution. Documented process identity checks at SKILL.md:153-160 and start timestamp capture at SKILL.md:84 need process inspection; run used an auto-reviewed escalation. This is an environment limit, not a demonstrated script defect.', '', 'No functional friction in the exercised lifecycle paths.', '', '## Session files', '']
    summary += ['- '+s['name']+': '+str(s['receipt'])+'; log '+str(s['log']) for s in sessions]
    (ROOT/'validation-receipt.md').write_text('\n'.join(summary)+'\n')
    print('Receipt: '+str(ROOT/'validation-receipt.md'), flush=True)
