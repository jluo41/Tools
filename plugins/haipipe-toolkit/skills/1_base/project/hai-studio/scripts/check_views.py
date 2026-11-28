"""Generate a Studio Check view from its owning type, without claiming execution.

A topic opts in with check_type (SPACE-relative type topic) in studio-views.json.
The type's elements.md is the only criteria source. --check detects stale generated
UI; it does not execute or certify the checks described in that UI.
"""
from __future__ import annotations

import hashlib
import html
import json
import sys
from pathlib import Path
from urllib.parse import urlencode

from type_requirements import SPACE, CSS, words


def owned(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('check_type must be a SPACE-relative type topic')
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('check_type leaves the SPACE')
    if not (path / 'elements.md').is_file() or not (path / 'elements.md').resolve().is_relative_to(root.resolve()):
        raise ValueError('check_type has no contained elements.md')
    return path


def criteria(type_topic: Path) -> list[dict]:
    from host_paths import bootstrap
    bootstrap()
    from live.studio_types import elements_of
    return [e for e in elements_of(type_topic) if e['view'] != 'Check' and (e.get('must') or e.get('check'))]


def groups(elements: list[dict], views: list[dict], layout: str = 'views') -> list[tuple[str, list[dict]]]:
    if layout == 'elements':
        out = []
        for el in elements:
            # Keep top-level criteria too: an element card inherits its view's requirements.
            children = [e for e in elements if e['view'] == el['view'] and e.get('tab')]
            if not el.get('tab') and children:
                continue
            parent = [e for e in elements if e['view'] == el['view'] and not e.get('tab')]
            label = el['view'] + (' › ' + el['tab'] if el.get('tab') else '')
            out.append((label, parent + [el] if el.get('tab') else [el]))
        return out
    if layout != 'views':
        raise ValueError('Unknown Check layout')
    names = list(dict.fromkeys(e['view'] for e in elements))
    out = []
    for name in names:
        rows = [e for e in elements if e['view'] == name]
        if name == '〈skill〉':
            skills = [v['name'] for v in views if v['name'] != 'Check' and any(
                i.get('path', '').endswith('/SKILL.md') for i in v.get('items', []))]
            out.extend((skill, rows) for skill in skills or [name])
        else:
            out.append((name, rows))
    return out


def document(topic: Path, type_topic: Path, entries: list, root: Path) -> str:
    esc = html.escape
    source = type_topic / 'elements.md'
    source_rel = source.relative_to(root).as_posix()
    url = '/_board/workbench?' + urlencode({'view': 'focus-file', 'path': source_rel})
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    definition = topic.resolve() == type_topic.resolve()
    sections = []
    for n, (name, elements) in enumerate(entries):
        cards = []
        for el in elements:
            checks = el.get('must') or [el['check']]
            mark = '◇' if definition else '□'
            hint = 'Check definition' if definition else 'Not verified'
            rows = ''.join(f'<li><span class="mark" title="{hint}" aria-label="{hint}">{mark}</span>'
                           f'<span>{words(line)}</span></li>' for line in checks)
            method = words(el.get('check') or 'Inspect this element against each requirement.')
            cards.append(f'<article><h2>{esc(el["name"])}</h2><ul>{rows}</ul>'
                         f'<details><summary>Verify</summary><p>{method}</p>'
                         f'<a href="{esc(url, quote=True)}" target="_blank" rel="noopener">{esc(type_topic.name)} · {esc(el["view"])} / {esc(el["name"])}</a></details></article>')
        sections.append(f'<section id="check-{n}"'+(' hidden' if n else '')+'>' + ''.join(cards) + '</section>')
    style = CSS + '''body{max-width:none;padding:14px 16px}article{padding:0 0 14px;margin:0 0 16px;border-bottom:1px solid var(--line)}
h2{font-size:15px;margin:0 0 8px}ul{list-style:none;padding:0;margin:0}li{display:flex;gap:9px;margin:8px 0}.mark{color:var(--muted);flex:none}li>span:last-child{min-width:0;overflow-wrap:anywhere}
summary{cursor:pointer;color:var(--muted);font-size:13px}details{margin-top:12px}details p,details a{font-size:13px;overflow-wrap:anywhere}a{color:var(--accent)}[hidden]{display:none!important}'''
    script = "function pick(){const id=location.hash.slice(1)||'check-0';document.querySelectorAll('section').forEach(s=>s.hidden=s.id!==id)}addEventListener('hashchange',pick);pick();"
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>Check · {esc(topic.name)}</title><style>{style}</style></head>'
            f'<body data-requirements-sha256="{digest}" data-target="{esc(topic.relative_to(root).as_posix(),quote=True)}">'
            + ''.join(sections) + f'<script>{script}</script></body></html>\n')


def build(topic: Path, data: dict | None = None, root: Path = SPACE) -> dict[Path, str]:
    topic, root = topic.resolve(), root.resolve()
    if not topic.is_relative_to(root):
        raise ValueError('topic leaves the SPACE')
    manifest = topic / 'studio-views.json'
    data = json.loads(manifest.read_text()) if data is None else json.loads(json.dumps(data))
    type_topic = owned(root, data.get('check_type'))
    views = [v for v in data['views'] if v['name'] != 'Check']
    entries = groups(criteria(type_topic), views, data.get('check_layout', 'views'))
    if not entries:
        raise ValueError('type defines no checkable requirements')
    page = topic / 'delivery/check.html'
    items = [{'name': name, 'path': page.relative_to(root).as_posix(), 'fragment': f'check-{n}'}
             for n, (name, _) in enumerate(entries)]
    data['views'] = views + [{'name': 'Check', 'items': items}]
    return {page: document(topic, type_topic, entries, root),
            manifest: json.dumps(data, ensure_ascii=False, indent=2) + '\n'}


def main(argv: list[str]) -> int:
    check = '--check' in argv
    paths = [a for a in argv if not a.startswith('--')]
    if not paths:
        print(__doc__)
        return 2
    bad = False
    for path in paths:
        try:
            outputs = build(SPACE / path)
            stale = [p for p, text in outputs.items() if not p.is_file() or p.read_text() != text]
            if check:
                for p in stale:
                    print(f'Stale Check view: {p.relative_to(SPACE)}')
                bad |= bool(stale)
            else:
                for p, text in outputs.items():
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(text)
        except (OSError, ValueError, KeyError, TypeError) as error:
            print(f'{path}: {error}')
            bad = True
    return int(bad)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
