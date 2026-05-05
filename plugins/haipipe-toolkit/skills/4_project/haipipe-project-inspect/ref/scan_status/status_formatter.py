#!/usr/bin/env python3
"""status_formatter.py — read diagram/status.json and write a human-readable txt.

Usage:
    python status_formatter.py <task_dir> [out_txt_path]

If out_txt_path is omitted, writes to <task_dir>/diagram/status.txt.

Table format mirrors the B01 eval task convention:
  Phase 1     : size rows, single status column
  Epoch Sweep : size rows x epoch columns (grid)
  Datasize    : size rows x datasize columns (grid)
  v3          : size rows, single status column
"""
import json
import re
import sys
from pathlib import Path

SIZE_ORDER  = ['1m', '2m', '5m', '10m', '20m', '50m', '100m', '200m',
               '300m', '500m', '750m', '1b']
EPOCH_ORDER = ['ep0.1', 'ep0.25', 'ep0.5', 'ep0.75', 'ep1', 'ep2', 'ep4', 'ep8']
DSIZE_ORDER = ['d1m', 'd5m', 'd10m', 'd50m', 'd100m', 'd500m']

COL1 = 21   # width of the left label column


def size_key(s):
    try:
        return SIZE_ORDER.index(s)
    except ValueError:
        return 99


def classify_setup(setup):
    if setup is None or setup == 'phase1':
        return 'phase1'
    if re.match(r'^ep[\d.]+$', str(setup)):
        return 'epoch'
    if re.match(r'^d\d+[mb]$', str(setup)):
        return 'datasize'
    if setup == 'v3':
        return 'v3'
    return 'other'


def _slot_widths(cols):
    """Column slot widths: non-last = len(col)+2, last = len(col)+1."""
    ws = [len(c) + 2 for c in cols]
    if ws:
        ws[-1] = len(cols[-1]) + 1
    return ws


def fmt_phase1(entries):
    entries_s = sorted(entries, key=lambda e: size_key(e.get('size', '')))
    lines = [
        '--- Phase 1 ---',
        f'{"Setup":<{COL1}}| status',
        '-' * COL1 + '|-------',
    ]
    for e in entries_s:
        label = f'{e.get("size", "?"):<5}/ phase1'
        lines.append(f'{label:<{COL1}}|  {e["status"]}')
    return lines + ['']


def fmt_v3(entries):
    entries_s = sorted(entries, key=lambda e: size_key(e.get('size', '')))
    lines = [
        '--- v3 ---',
        f'{"Setup":<{COL1}}| status',
        '-' * COL1 + '|-------',
    ]
    for e in entries_s:
        label = f'{e.get("size", "?"):<5}/ v3'
        lines.append(f'{label:<{COL1}}|  {e["status"]}')
    return lines + ['']


def fmt_epoch_sweep(entries):
    sizes = sorted(set(e.get('size', '') for e in entries), key=size_key)
    cols  = sorted(set(e.get('setup', '') for e in entries),
                   key=lambda x: EPOCH_ORDER.index(x) if x in EPOCH_ORDER else 99)
    lut   = {(e['size'], e['setup']): e['status'] for e in entries}
    ws    = _slot_widths(cols)

    hdr = f'{"Size":<6}' + ''.join(f'| {c:<{ws[i] - 1}}' for i, c in enumerate(cols))
    sep = '------' + ''.join(f'|{"-" * w}' for w in ws)

    lines = ['--- Epoch Sweep ---', hdr, sep]
    for sz in sizes:
        row = f'{sz:<6}'
        for i, c in enumerate(cols):
            val = lut.get((sz, c), '?')
            row += f'|  {val:<{ws[i] - 2}}' if i < len(cols) - 1 else f'|  {val}'
        lines.append(row)
    return lines + ['']


def fmt_datasize(entries):
    sizes  = sorted(set(e.get('size', '') for e in entries), key=size_key)
    dsizes = sorted(set(e.get('setup', '') for e in entries),
                    key=lambda x: DSIZE_ORDER.index(x) if x in DSIZE_ORDER else 99)
    lut    = {(e['size'], e['setup']): e['status'] for e in entries}
    ws     = _slot_widths(dsizes)

    hdr = f'{"Setup":<{COL1}}' + ''.join(f'| {d:<{ws[i] - 1}}' for i, d in enumerate(dsizes))
    sep = '-' * COL1 + ''.join(f'|{"-" * w}' for w in ws)

    lines = ['--- Datasize ---', hdr, sep]
    for sz in sizes:
        row = f'{sz:<{COL1}}'
        for i, ds in enumerate(dsizes):
            val = lut.get((sz, ds), '?')
            row += f'|  {val:<{ws[i] - 2}}' if i < len(dsizes) - 1 else f'|  {val}'
        lines.append(row)
    return lines + ['']


def fmt_group(group_name, entries):
    phase1   = [e for e in entries if classify_setup(e.get('setup')) == 'phase1']
    epoch    = [e for e in entries if classify_setup(e.get('setup')) == 'epoch']
    datasize = [e for e in entries if classify_setup(e.get('setup')) == 'datasize']
    v3       = [e for e in entries if classify_setup(e.get('setup')) == 'v3']
    other    = [e for e in entries if classify_setup(e.get('setup')) == 'other']

    model_type = entries[0].get('model_type', group_name) if entries else group_name
    lines = [f'=== {model_type} ===', '']

    if phase1:
        lines.extend(fmt_phase1(phase1))
    if epoch:
        lines.extend(fmt_epoch_sweep(epoch))
    if datasize:
        lines.extend(fmt_datasize(datasize))
    if v3:
        lines.extend(fmt_v3(v3))
    if other:
        lines.append('--- Other ---')
        for e in sorted(other, key=lambda e: e.get('run_name', '')):
            lines.append(f'  {e["run_name"]}: {e["status"]}')
        lines.append('')

    return lines


def main():
    task_dir  = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    json_path = task_dir / 'diagram' / 'status.json'

    if not json_path.exists():
        print(f'ERROR: {json_path} not found. Run scan_status.py first.')
        sys.exit(1)

    data    = json.loads(json_path.read_text())
    task    = data.get('task', task_dir.name)
    updated = data.get('updated', '?')

    meta       = {'task', 'updated'}
    group_keys = [k for k in data if k not in meta]

    title = f'Status: {task}'
    lines = [
        title,
        '=' * len(title),
        f'Updated: {updated}',
        '',
        'V = trained + eval done',
        'O = trained, eval not done',
        'X = not trained',
        '? = run not defined in sbatch (not planned)',
        '',
        '',
    ]

    for key in group_keys:
        entries = data[key]
        if entries:
            lines.extend(fmt_group(key, entries))

    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else task_dir / 'diagram' / 'status.txt'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(lines))
    print(f'Written: {out_path}')


if __name__ == '__main__':
    main()
