#!/usr/bin/env python3
"""scan_status.py — scan a B01 eval task and write/update diagram/status.json

Shared across B01 subtasks. Group naming conventions are defined in
scan_groups.json at the B01 level. Results accumulate under first-level
keys = storage_key in diagram/status.json.

Usage:
    python scan_status.py <task_dir>                   # all groups
    python scan_status.py <task_dir> <storage_key>     # one group, merge into existing JSON

scan_groups.json format:
    {
      "<storage_key>": {
        "run_filter":    "<substring to match run names>",
        "parse_pattern": "<regex with capture groups>",
        "parse_fields":  ["field1", "field2", ...]
      },
      ...
    }
"""
import re
import json
import sys
from pathlib import Path
from datetime import date


# ── resolve paths ─────────────────────────────────────────────────────────────

TASK_DIR    = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
STORAGE_KEY = sys.argv[2] if len(sys.argv) > 2 else None
B01_DIR     = TASK_DIR.parent


def find_project_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / '_WorkSpace').exists():
            return p
    raise RuntimeError(f'Cannot find project root (no _WorkSpace) from {start}')


PROJECT_ROOT = find_project_root(TASK_DIR)
MODEL_STORE  = PROJECT_ROOT / '_WorkSpace' / '5-ModelInstanceStore'


# ── load group config ─────────────────────────────────────────────────────────

config_path = B01_DIR / 'scan_groups.json'
if not config_path.exists():
    raise FileNotFoundError(f'scan_groups.json not found at {config_path}')

with open(config_path) as f:
    ALL_GROUPS = json.load(f)

if STORAGE_KEY and STORAGE_KEY not in ALL_GROUPS:
    raise KeyError(f'storage_key "{STORAGE_KEY}" not in scan_groups.json. '
                   f'Available: {list(ALL_GROUPS)}')


# ── helpers ───────────────────────────────────────────────────────────────────

def get_version(run_script: Path):
    if not run_script.exists():
        return None
    m = re.search(r'VERSIONS_STR="([^"]+)"', run_script.read_text())
    return m.group(1) if m else None


def check_trained(version: str, storage_key: str) -> bool:
    if not version:
        return False
    d = MODEL_STORE / storage_key / version
    return d.exists() and any(d.iterdir())


def check_eval_b1(version: str, storage_key: str) -> bool:
    if not version:
        return False
    return (MODEL_STORE / storage_key / version / 'eval_results.json').exists()


def check_eval_b2(run_name: str) -> bool:
    return (TASK_DIR / 'results' / run_name / 'forecast.json').exists()


# ── detect task type ──────────────────────────────────────────────────────────

is_b1 = 'loss' in TASK_DIR.name


# ── collect run names from sbatch scripts ─────────────────────────────────────

SKIP_SCRIPTS = {'run_all_nb.sh', 'rerun_force_nb.sh'}


def collect_runs(run_filter: str):
    seen, runs = set(), []
    for sh in sorted((TASK_DIR / 'sbatch').glob('*.sh')):
        if sh.name in SKIP_SCRIPTS:
            continue
        for line in sh.read_text().splitlines():
            m = re.search(r'\b(eval_[a-z0-9_.]+_nb)\b', line)
            if m and run_filter in m.group(1):
                name = m.group(1)
                if name not in seen:
                    seen.add(name)
                    runs.append((name, sh.name))
    return runs


# ── scan one group ────────────────────────────────────────────────────────────

def scan_group(storage_key: str, cfg: dict) -> list:
    parse_re     = re.compile(cfg['parse_pattern'])
    parse_fields = cfg['parse_fields']
    entries = []

    for run_name, _ in collect_runs(cfg['run_filter']):
        pm = parse_re.match(run_name)
        parsed = {}
        if pm:
            for i, field in enumerate(parse_fields, start=1):
                val = pm.group(i) if pm.lastindex and i <= pm.lastindex else None
                parsed[field] = val or ('phase1' if field == 'setup' else None)

        version   = get_version(TASK_DIR / 'runs' / f'{run_name}.sh')
        trained   = check_trained(version, storage_key)
        eval_done = check_eval_b1(version, storage_key) if is_b1 else check_eval_b2(run_name)
        status    = 'V' if (trained and eval_done) else ('O' if trained else 'X')

        entries.append({
            'run_name':  run_name,
            **parsed,
            'version':   version,
            'trained':   trained,
            'eval_done': eval_done,
            'status':    status,
        })

    return entries


# ── load / update / write status.json ─────────────────────────────────────────

out_path = TASK_DIR / 'diagram' / 'status.json'
out_path.parent.mkdir(parents=True, exist_ok=True)

data = json.loads(out_path.read_text()) if out_path.exists() else {}
data['task']    = TASK_DIR.name
data['updated'] = str(date.today())

groups_to_run = {STORAGE_KEY: ALL_GROUPS[STORAGE_KEY]} if STORAGE_KEY else ALL_GROUPS

# On full scan, drop keys that are no longer in scan_groups.json
if not STORAGE_KEY:
    meta = {'task', 'updated'}
    for stale in [k for k in data if k not in meta and k not in ALL_GROUPS]:
        del data[stale]

for key, cfg in groups_to_run.items():
    entries = scan_group(key, cfg)
    data[key] = entries
    print(f'  {key}: {len(entries)} entries')

out_path.write_text(json.dumps(data, indent=2))
print(f'Written: {out_path}')
