#!/usr/bin/env python3
"""status_formatter.py — read diagram/status.json and write a human-readable txt.

Usage:
    python status_formatter.py <task_dir> [out_txt_path]

If out_txt_path is omitted, writes to <task_dir>/diagram/status.txt.

When status.json contains entries from multiple model_type values (e.g. clm_tkn
and clm_num), a merged format is used: sections are organized by sweep type
(Phase 1 / Epoch Sweep / Datasize / v3) with model types as side-by-side columns.
When only one model_type is present the original per-group format is used instead.

Any unmapped instances stored under the "unmapped" key are appended at the bottom.
"""
import json
import re
import sys
from pathlib import Path

SIZE_ORDER  = ['1m', '2m', '5m', '10m', '20m', '50m', '100m', '200m',
               '300m', '500m', '750m', '1b']
EPOCH_ORDER = ['ep0.1', 'ep0.25', 'ep0.5', 'ep0.75', 'ep1', 'ep2', 'ep4', 'ep8']
DSIZE_ORDER = ['d1m', 'd5m', 'd10m', 'd50m', 'd100m', 'd500m']

MODEL_ABBR_ORDER = ['TKN', 'NUM']  # preferred column order for merged tables

COL1 = 21  # left label column width (per-group format)


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


# ── helpers for merged format ──────────────────────────────────────────────────

def abbreviate_model_type(mt):
    """clm_tkn -> TKN, clm_num -> NUM."""
    if mt and mt.startswith('clm_'):
        return mt[4:].upper()
    return (mt or '').upper()


def abbreviate_epoch_setup(s):
    """ep0.25 -> ep.25, ep0.75 -> ep.75; ep0.1, ep2, etc. unchanged."""
    m = re.match(r'^ep0(\.\d{2,})$', s)
    return 'ep' + m.group(1) if m else s


def sort_model_abbrs(abbrs):
    def key(a):
        try:
            return MODEL_ABBR_ORDER.index(a)
        except ValueError:
            return len(MODEL_ABBR_ORDER) + sum(ord(c) for c in a)
    return sorted(abbrs, key=key)


def _center_val(val, slot_w):
    """Center a single-char value in slot_w chars (left-biased for even slots)."""
    lpad = (slot_w - 1) // 2
    rpad = slot_w - 1 - lpad
    return ' ' * lpad + val + ' ' * rpad


# ── merged: Phase 1 / v3  (no trailing | on rows) ─────────────────────────────

def fmt_simple_merged(entries, model_abbrs):
    """
    Phase 1 or v3 table with model types as columns:
      Size  |  TKN  |  NUM
      ------|-------|------
      1m    |   V   |   V
    Last column has no trailing padding or closing |.
    """
    slot_w = max((len(a) for a in model_abbrs), default=3) + 4

    lut = {}
    all_sizes = set()
    for e in entries:
        abbr = abbreviate_model_type(e.get('model_type', ''))
        sz   = e.get('size', '')
        lut[(abbr, sz)] = e['status']
        all_sizes.add(sz)
    sizes = sorted(all_sizes, key=size_key)

    hdr = 'Size  '
    sep = '------'
    for i, a in enumerate(model_abbrs):
        last = i == len(model_abbrs) - 1
        if last:
            lpad = (slot_w - len(a)) // 2
            hdr += f'|{" " * lpad}{a}'
            sep += f'|{"-" * (slot_w - 1)}'
        else:
            lpad = (slot_w - len(a)) // 2
            rpad = slot_w - len(a) - lpad
            hdr += f'|{" " * lpad}{a}{" " * rpad}'
            sep += f'|{"-" * slot_w}'

    lines = ['', hdr, sep]
    for sz in sizes:
        row = f'{sz:<6}'
        for i, a in enumerate(model_abbrs):
            val  = lut.get((a, sz), '?')
            last = i == len(model_abbrs) - 1
            if last:
                lpad = (slot_w - 1) // 2
                row += f'|{" " * lpad}{val}'
            else:
                row += f'|{_center_val(val, slot_w)}'
        lines.append(row)
    return lines


# ── merged: Epoch Sweep  (trailing | on every row) ────────────────────────────

def fmt_epoch_merged(entries, model_abbrs):
    """
    Epoch Sweep merged table with group-label header:
             |----------- TKN -----------|----------- NUM -----------|
      Size   | ep0.1 | ep.25 | ep.75 | ep2 | ep4 | ep8 | ...        |
    All rows end with |.
    """
    all_epochs_raw = sorted(
        set(e.get('setup', '') for e in entries),
        key=lambda x: EPOCH_ORDER.index(x) if x in EPOCH_ORDER else 99,
    )
    disp    = [abbreviate_epoch_setup(ep) for ep in all_epochs_raw]
    slot_ws = [len(d) + 2 for d in disp]

    lut = {}
    all_sizes = set()
    for e in entries:
        abbr = abbreviate_model_type(e.get('model_type', ''))
        sz   = e.get('size', '')
        ep   = e.get('setup', '')
        lut[(abbr, sz, ep)] = e['status']
        all_sizes.add(sz)
    sizes = sorted(all_sizes, key=size_key)

    SIZE_COL = 9
    N_DASH   = 11  # dashes each side of model-type label in group-header row

    def grp_seg(abbr):
        return f'|{"-" * N_DASH} {abbr} {"-" * N_DASH}'

    grp_row = ' ' * SIZE_COL + ''.join(grp_seg(a) for a in model_abbrs) + '|'
    col_hdr = f'{"Size":<{SIZE_COL}}'
    sep     = '-' * SIZE_COL
    for _a in model_abbrs:
        for d, sw in zip(disp, slot_ws):
            col_hdr += f'| {d} '
            sep     += f'|{"-" * sw}'
    col_hdr += '|'
    sep     += '|'

    lines = ['', grp_row, col_hdr, sep]
    for sz in sizes:
        row = f'{sz:<{SIZE_COL}}'
        for a in model_abbrs:
            for ep_raw, sw in zip(all_epochs_raw, slot_ws):
                val = lut.get((a, sz, ep_raw), '?')
                row += f'|{_center_val(val, sw)}'
        row += '|'
        lines.append(row)
    return lines


# ── merged: Datasize  (trailing | on every row) ───────────────────────────────

def fmt_datasize_merged(entries, model_abbrs):
    """
    Datasize merged table with two-row header:
      Size  |---- TKN ----|---- NUM ----|
            | d10m | d100m | d10m | d100m |
    All rows end with |.
    """
    all_dsizes_raw = sorted(
        set(e.get('setup', '') for e in entries),
        key=lambda x: DSIZE_ORDER.index(x) if x in DSIZE_ORDER else 99,
    )
    slot_ws = [len(d) + 2 for d in all_dsizes_raw]

    lut = {}
    all_sizes = set()
    for e in entries:
        abbr = abbreviate_model_type(e.get('model_type', ''))
        sz   = e.get('size', '')
        ds   = e.get('setup', '')
        lut[(abbr, sz, ds)] = e['status']
        all_sizes.add(sz)
    sizes = sorted(all_sizes, key=size_key)

    SIZE_COL = 6
    N_DASH   = 4

    def grp_seg(abbr):
        return f'|{"-" * N_DASH} {abbr} {"-" * N_DASH}'

    grp_row = f'{"Size":<{SIZE_COL}}' + ''.join(grp_seg(a) for a in model_abbrs) + '|'
    sub_hdr = ' ' * SIZE_COL
    sep     = '-' * SIZE_COL
    for _a in model_abbrs:
        for d, sw in zip(all_dsizes_raw, slot_ws):
            sub_hdr += f'| {d} '
            sep     += f'|{"-" * sw}'
    sub_hdr += '|'
    sep     += '|'

    lines = ['', grp_row, sub_hdr, sep]
    for sz in sizes:
        row = f'{sz:<{SIZE_COL}}'
        for a in model_abbrs:
            for ds, sw in zip(all_dsizes_raw, slot_ws):
                val = lut.get((a, sz, ds), '?')
                row += f'|{_center_val(val, sw)}'
        row += '|'
        lines.append(row)
    return lines


# ── merged top-level ───────────────────────────────────────────────────────────

def fmt_all_merged(all_entries):
    """Format all entries as merged sections (sweep type outer, model type as columns)."""
    model_types = {abbreviate_model_type(e.get('model_type', ''))
                   for e in all_entries if e.get('model_type')}
    model_abbrs = sort_model_abbrs(model_types)

    phase1   = [e for e in all_entries if classify_setup(e.get('setup')) == 'phase1']
    epoch    = [e for e in all_entries if classify_setup(e.get('setup')) == 'epoch']
    datasize = [e for e in all_entries if classify_setup(e.get('setup')) == 'datasize']
    v3       = [e for e in all_entries if classify_setup(e.get('setup')) == 'v3']

    lines = []
    for label, subset, fn in [
        ('Phase 1',     phase1,   fmt_simple_merged),
        ('Epoch Sweep', epoch,    fmt_epoch_merged),
        ('Datasize',    datasize, fmt_datasize_merged),
        ('v3',          v3,       fmt_simple_merged),
    ]:
        if not subset:
            continue
        lines.append(f'=== {label} ===')
        lines.extend(fn(subset, model_abbrs))
        lines.extend(['', ''])

    while lines and lines[-1] == '':
        lines.pop()
    return lines


# ── per-group format (single model type or fallback) ──────────────────────────

def _slot_widths(cols):
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


# ── unmapped instances section ─────────────────────────────────────────────────

def fmt_unmapped(unmapped: dict) -> list:
    """Append an unmapped-instances section if any exist."""
    has_any = any(versions for versions in unmapped.values())
    if not has_any:
        return []

    lines = ['', '', '=== Unmapped Instances ===', '']
    lines.append('Trained versions in store with no matching sbatch run:')
    lines.append('')
    for key in sorted(unmapped):
        versions = unmapped[key]
        if versions:
            lines.append(f'  {key}:')
            for v in sorted(versions):
                lines.append(f'    {v}')
    return lines


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    task_dir  = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    json_path = task_dir / 'diagram' / 'status.json'

    if not json_path.exists():
        print(f'ERROR: {json_path} not found. Run scan_status.py first.')
        sys.exit(1)

    data    = json.loads(json_path.read_text())
    task    = data.get('task', task_dir.name)
    updated = data.get('updated', '?')

    meta       = {'task', 'updated', 'unmapped'}
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

    all_entries = []
    for key in group_keys:
        all_entries.extend(data[key])

    model_types = {e.get('model_type') for e in all_entries if e.get('model_type')}

    if len(model_types) > 1:
        lines.extend(fmt_all_merged(all_entries))
    else:
        for key in group_keys:
            entries = data[key]
            if entries:
                lines.extend(fmt_group(key, entries))

    unmapped = data.get('unmapped', {})
    lines.extend(fmt_unmapped(unmapped))

    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else task_dir / 'diagram' / 'status.txt'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(lines))
    print(f'Written: {out_path}')


if __name__ == '__main__':
    main()
