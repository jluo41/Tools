#!/usr/bin/env python3
"""space_check.py -- is this SPACE up to date with the haipipe-data migration notes?

Read-only. Run from a SPACE root (the folder holding code/ and examples-*/ or
examples/). Every item is detected from the SPACE itself; nothing is recorded.
Each item prints a status, the evidence, and the next step, with the section of
ref/migration.md that explains it. Stdlib only, no network (git reads only what
the last fetch saw).

    python3 <haipipe-data>/cli/space_check.py [--root .] [--brief]

--brief prints one status line (the dashboard's SPACE status block).
Exit code is always 0; the report is the result.

Status: OK up to date | BEHIND an update is available | RISK something runs
wrong today | INFO nothing to do | N/A the item does not apply to this SPACE.
"""
import argparse
import glob
import os
import re
import subprocess

NOTE = 'ref/migration.md § 2026-09-24 · Fn versions and the external serving bundle'
CODE_COMMIT = '27b1525'          # haipipe-code code-drfirst: fn_dir / fn_version, external_base
LOADERS = ['haipipe/source_base/builder/sourcefn.py', 'haipipe/record_base/builder/record.py',
           'haipipe/record_base/builder/human.py', 'haipipe/case_base/builder/triggerfn.py',
           'haipipe/case_base/builder/casefn.py']
STAGES = ['fn_source', 'fn_record', 'fn_case']
FLAT_SUBDIRS = {'human', 'record', 'fn_trigger', 'case_casefn', '__pycache__'}


def git(cwd, *args):
    try:
        r = subprocess.run(['git', '-C', cwd, *args], capture_output=True, text=True, timeout=20)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def read(path):
    try:
        with open(path) as f:
            return f.read()
    except OSError:
        return None


def task_roots(root):
    return [p for p in glob.glob(os.path.join(root, 'examples*', '*', 'tasks')) if os.path.isdir(p)]


def config_fn_versions(root):
    """{config path: fn_version} for every Task-folder YAML with a top-level fn_version:."""
    found = {}
    for tr in task_roots(root):
        for p in glob.glob(os.path.join(tr, '**', 'scripts', 'config', '*.yaml'), recursive=True):
            m = re.search(r'^fn_version:\s*["\']?([A-Za-z0-9_.-]+)', read(p) or '', re.M)
            if m:
                found[p] = m.group(1)
    return found


def check(root):
    items = []                   # (status, item, evidence, next)
    code = os.path.join(root, 'code')
    base = read(os.path.join(code, 'haipipe', 'base.py'))
    if base is None:
        return [('N/A', 'SPACE root', f'no code/haipipe/base.py under {root}', 'run from the SPACE root')]

    # 1. Tools checkout vs its remote (as of the last fetch)
    tools = os.path.join(root, 'Tools')
    sb = git(tools, 'status', '-sb') if os.path.exists(tools) else None
    if sb is None:
        items.append(('N/A', 'Tools', 'no Tools/ git checkout here', '-'))
    else:
        m = re.search(r'behind (\d+)', sb.splitlines()[0])
        if m:
            items.append(('BEHIND', 'Tools', f'{m.group(1)} commits behind its remote (last fetch)',
                          'git -C Tools pull --ff-only && Tools/install.sh --no-marketplace --project "$(pwd)"'))
        else:
            items.append(('OK', 'Tools', 'not behind its remote as of the last fetch (git -C Tools fetch to refresh)', '-'))

    # 2. code has fn_dir (Fn versions)
    has_fn_dir = 'def fn_dir' in base
    if has_fn_dir:
        items.append(('OK', 'code: fn_dir', 'haipipe.base.fn_dir present', '-'))
    else:
        items.append(('BEHIND', 'code: fn_dir', 'code/ predates Fn versions',
                      f'bring code/ to {CODE_COMMIT} or later (pull code-drfirst, or git -C code cherry-pick {CODE_COMMIT})'))

    # 3. every Fn loader resolves through fn_dir (a partial cherry-pick leaves some flat)
    if has_fn_dir:
        flat = [l for l in LOADERS if 'fn_dir' not in (read(os.path.join(code, l)) or '')]
        if flat:
            items.append(('RISK', 'code: loaders', f'{len(flat)} loader(s) ignore fn_version: ' + ', '.join(flat),
                          f'finish bringing in {CODE_COMMIT}; these load flat Fns even with fn_version: set'))
        else:
            items.append(('OK', 'code: loaders', f'all {len(LOADERS)} Source/Record/Case loaders use fn_dir', '-'))

    # 4. the silent-ignore trap: fn_version: set but the code cannot honour it
    cfgs = config_fn_versions(root)
    if cfgs and not has_fn_dir:
        items.append(('RISK', 'trap: fn_version ignored', f'{len(cfgs)} Run config(s) set fn_version: but code/ lacks fn_dir, '
                      'so they load the FLAT Fns', f'update code/ first ({NOTE})'))
    elif cfgs:
        items.append(('OK', 'trap: fn_version ignored', f'{len(cfgs)} Run config(s) set fn_version: and code/ honours it', '-'))
    else:
        items.append(('N/A', 'trap: fn_version ignored', 'no Run config sets fn_version: (flat folders, unchanged)', '-'))

    # 5. version folders: one version is shared by fn_source, fn_record, fn_case
    haifn = os.path.join(code, 'haifn')
    per_stage = {s: {d for d in os.listdir(os.path.join(haifn, s))
                     if os.path.isdir(os.path.join(haifn, s, d)) and d not in FLAT_SUBDIRS and d.startswith('v')}
                 if os.path.isdir(os.path.join(haifn, s)) else set() for s in STAGES}
    allv = set().union(*per_stage.values())
    if not allv:
        items.append(('N/A', 'haifn: versions', 'no version folders (flat layout)', '-'))
    for v in sorted(allv):
        missing = [s for s in STAGES if v not in per_stage[s]]
        if missing:
            items.append(('RISK', f'haifn: {v}', f'missing in {", ".join(missing)} (one version spans all three)',
                          f'build the {", ".join(missing)} Fns with fn_version: {v}, or retire {v}'))
        else:
            items.append(('OK', f'haifn: {v}', 'present in fn_source, fn_record, fn_case', '-'))
    for p, v in sorted(cfgs.items()):
        if v not in allv:
            items.append(('RISK', 'config -> version', f'{os.path.relpath(p, root)} names {v}, which is not built',
                          f'run the builders with fn_version: {v}'))

    # 6. one dataset Job (j5N, same number in b01-b03) uses ONE fn_version
    by_job = {}
    for p, v in cfgs.items():
        m = re.search(r'/b0[123]_[^/]+/(j5\d)_', p)
        if m:
            by_job.setdefault((p.split('/tasks/')[0], m.group(1)), set()).add(v)
    for (proj, job), vs in sorted(by_job.items()):
        name = f'{os.path.basename(proj)} {job}'
        if len(vs) > 1:
            items.append(('RISK', f'dataset {name}', f'b01-b03 Runs disagree: {", ".join(sorted(vs))}',
                          'give every b01-b03 Run of this dataset one fn_version:'))
        else:
            items.append(('OK', f'dataset {name}', f'fn_version {next(iter(vs))}', '-'))

    # 7. external serving bundle support (only matters if the SPACE uses external_base)
    asset = read(os.path.join(code, 'haipipe', 'external_base', 'asset.py'))
    if asset is None:
        items.append(('N/A', 'code: external bundle', 'no haipipe/external_base (external asset model not in use)', '-'))
    elif 'key_normalized' in asset:
        items.append(('OK', 'code: external bundle', 'pre-keyed versions (key_normalized) load directly', '-'))
    else:
        items.append(('BEHIND', 'code: external bundle', 'external_base predates pre-keyed bundles',
                      f'bring code/ to {CODE_COMMIT} before shipping a trimmed, pre-keyed external/'))

    # 8. the checked-out code/ vs the commit this SPACE pins (a drift explains odd behaviour)
    pinned = (git(root, 'ls-tree', 'HEAD', 'code') or '').split()
    head = git(code, 'rev-parse', 'HEAD')
    if len(pinned) >= 3 and head:
        dirty = bool(git(code, 'status', '--porcelain', '--untracked-files=no'))
        if head != pinned[2]:
            items.append(('INFO', 'code: checkout', f'checked out {head[:7]}, SPACE pins {pinned[2][:7]}'
                          + (', with uncommitted edits' if dirty else ''),
                          'commit or stash local work, then git -C code checkout the pinned commit (or bump the pin)'))
        else:
            items.append(('OK' if not dirty else 'INFO', 'code: checkout', f'at the pinned {head[:7]}'
                          + (', with uncommitted edits' if dirty else ''), '-'))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--brief', action='store_true')
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    items = check(root)
    worst = next((s for s in ('RISK', 'BEHIND') if any(i[0] == s for i in items)), 'OK')
    if a.brief:
        bad = [f'{i[1]} {i[0]}' for i in items if i[0] in ('RISK', 'BEHIND')]
        print(f'SPACE status: {worst}' + (' -- ' + '; '.join(bad) if bad else '')
              + '  (details: /haipipe-data space-check)')
        return
    print(f'SPACE check: {root}')
    print(f'notes: haipipe-data/{NOTE}')
    print()
    w = max(len(i[1]) for i in items)
    for s, item, ev, nxt in items:
        print(f'  {s:6s}  {item:{w}s}  {ev}')
        if nxt != '-':
            print(f'  {"":6s}  {"":{w}s}  next: {nxt}')
    print()
    print(f'overall: {worst}')


if __name__ == '__main__':
    main()
