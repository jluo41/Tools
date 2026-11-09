"""Curated, source-backed use-case examples; private SPACE mappings stay local.

Public blueprint entries use the served root. Cross-SPACE entries are accepted
only from .server_config/workbench-examples.json and use each SPACE's DOMAIN.
No request parameter grants filesystem access and no source file is served here.
"""
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlencode, urlsplit


def _json(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _relative(base, value):
    if not isinstance(value, str) or not value:
        return None
    part = Path(value)
    if part.is_absolute() or '..' in part.parts or any(p.startswith('.') for p in part.parts):
        return None
    path = (base / part).resolve()
    return path if path.is_relative_to(base) and path.is_dir() else None


def _origin(root):
    from server_config import load_server_config
    value = load_server_config(root).get('DOMAIN', '').rstrip('/')
    try:
        u = urlsplit(value)
        if u.scheme in ('http', 'https') and u.netloc and not u.username and not u.password and u.path in ('', '/') and not u.query and not u.fragment:
            return value
    except ValueError:
        pass
    return ''


def _entries(mapping, level, kind, case):
    try:
        rows = mapping[level][kind][case]
        return rows if isinstance(rows, list) else []
    except (KeyError, TypeError):
        return []


def examples(source, root, guide, level, kind, case):
    root = root.resolve()
    private = _json(root / '.server_config' / 'workbench-examples.json')
    key = source.resolve().relative_to(root).as_posix()
    public = _entries(guide.get('use_cases', {}), level, kind, case)
    matrices = private.get('matrices', {})
    local = _entries(matrices.get(key, {}) if isinstance(matrices, dict) else {}, level, kind, case)
    spaces = private.get('spaces', {})
    found, seen = [], set()
    for row, trusted in [(r, True) for r in local] + [(r, False) for r in public]:
        if not isinstance(row, dict):
            continue
        space = row.get('space', '')
        base = root
        if space:
            if not trusted or not isinstance(spaces, dict) or not isinstance(space, str):
                continue
            setting = spaces.get(space, {})
            if not isinstance(setting, dict) or not isinstance(setting.get('root'), str):
                continue
            configured = Path(setting['root']).expanduser()
            if not configured.is_absolute():
                continue
            base = configured.resolve()
        page = _relative(base, row.get('path'))
        if page is None or page in seen:
            continue
        face = page / ('board.md' if (page / 'board.md').is_file() else page.name + '.md')
        if not face.is_file() or not face.resolve().is_relative_to(base):
            continue
        seen.add(page)
        origin = '' if base == root else _origin(base)
        block = next((p for p in [page, *page.parents] if p.is_relative_to(base) and (p / 'board.md').is_file()), None)
        job = next((p for p in [page, *page.parents] if p.is_relative_to(base) and re.match(r'^j\d+_', p.name)), None)
        task = page if re.match(r'^t\d+_', page.name) else None
        # Only immediate actual Tasks of the linked Job, never a semantic guess.
        tasks = [task] if task else sorted(p for p in page.glob('t[0-9]*_*')
                    if p.is_dir() and p.resolve().is_relative_to(base) and (p / (p.name + '.md')).is_file()
                    and (p / (p.name + '.md')).resolve().is_relative_to(base)) if job == page else []
        found.append(dict(space=base.name, label=row.get('label', ''), base=base, origin=origin, page=page,
                          block=block, job=job, tasks=tasks, can_open=(base == root or bool(origin)) and not (trusted and row.get('preview_available') is False)))
    return found


def _link(row, page, level):
    label = html.escape(f'{level} · {page.name}')
    if not row['can_open']:
        return label
    url = row['origin'] + '/_board/workbench?' + urlencode({'path':page.relative_to(row['base']).as_posix(), 'layout':'focus'})
    return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener">{label} ↗</a>'


def button(label, kind, source, root, guide, level):
    from live import matrix_help
    case = matrix_help.plain(label)
    rows = examples(source, root, guide, level, matrix_help.plain(kind), case)
    token = hashlib.sha256(f'{source}:{level}:{kind}:{case}'.encode()).hexdigest()[:16]
    ident = 'use-case-' + token
    panels = []
    for row in rows:
        links = ''.join('<li>' + _link(row, row[k], k.title()) + '</li>' for k in ('block','job') if row[k])
        if row['tasks']:
            links += '<li><details><summary>Tasks</summary><ul>' + ''.join('<li>' + _link(row, t, 'Task') + '</li>' for t in row['tasks']) + '</ul></details></li>'
        if not links:
            links = '<li>' + _link(row, row['page'], 'Page') + '</li>'
        note = ('<p>Preview unavailable. Source folder verified.</p>' if row['origin']
                else '<p>Workbench address not configured.</p>') if not row['can_open'] else ''
        heading = row['space'] + (' · ' + str(row['label']) if row['label'] else '')
        path = html.escape(row['page'].relative_to(row['base']).as_posix())
        panels.append('<article class="use-case-example"><h3>' + html.escape(heading) + '</h3><ul>' + links + '</ul>'
                      + '<details class="use-case-path"><summary>Path</summary><code>' + path + '</code></details>' + note + '</article>')
    notes = guide.get('use_case_notes', {})
    try:
        note = notes[level][matrix_help.plain(kind)][case]
    except (KeyError, TypeError):
        note = ''
    note = '<p>' + html.escape(note) + '</p>' if isinstance(note, str) and note.strip() else ''
    body = note + ''.join(panels) if note or panels else '<p>No linked examples yet.</p>'
    return (f'<button type="button" class="matrix-section" aria-haspopup="dialog" data-template="{ident}" '
            f'data-title="{html.escape(matrix_help.words(label), quote=True)}" data-context="{html.escape(level.title()+" · "+matrix_help.plain(kind)+" · Use Cases", quote=True)}">'
            + html.escape(matrix_help.words(label)) + f'</button><template id="{ident}">' + body + '</template>')
