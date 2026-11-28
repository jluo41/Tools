"""Resolve examples beside requirements from existing instance view bindings.

examples.json maps ``Top / Left`` (or ``Top``) to topic/view/item selectors.
No UI snapshot or independent copy of an instance manifest is maintained here.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, quote, urlencode, urlsplit


def contained(root: Path, value: str) -> Path:
    path = (root / value).resolve()
    if not value or Path(value).is_absolute() or not path.is_relative_to(root.resolve()):
        raise ValueError('Example source must stay inside the SPACE')
    if not path.exists():
        raise ValueError(f'Missing example source: {value}')
    return path


def block_url(url: str, root: Path) -> str:
    """Normalize existing child-page bindings to the owning Block selection."""
    parts = urlsplit(url)
    if parts.scheme or parts.netloc or parts.path != '/_board/workbench':
        raise ValueError('Example page must use the origin-relative workbench route')
    query = dict(parse_qsl(parts.query))
    target = contained(root, query.get('path', ''))
    if not query.get('view'):
        block = next((p for p in [target, *target.parents]
                      if p.is_relative_to(root.resolve()) and (p / 'board.md').is_file()), None)
        if block is None:
            raise ValueError('Example page has no owning Block')
        children = target.relative_to(block).parts
        jobs = [p for p in children if re.match(r'j\d\d[_-]', p)]
        tasks = [p for p in children if re.match(r't\d\d[_-]', p)]
        if jobs:
            query.update(path=block.relative_to(root).as_posix(), section='jobs', group=jobs[-1][:3])
        if tasks:
            query['task'] = tasks[-1][:3]
    return parts.path + '?' + urlencode(query) + ('#' + parts.fragment if parts.fragment else '')


def resolve(topic: Path, el: dict, root: Path) -> tuple[str, str] | None:
    path = topic / 'examples.json'
    if not path.is_file():
        return None
    key = el['view'] + (' / ' + el['tab'] if el.get('tab') else '')
    bindings = json.loads(path.read_text())
    if key not in bindings:
        raise ValueError(f'Missing example binding: {key}')
    binding = bindings[key]
    source = contained(root, binding['topic'])
    data = json.loads((source / 'studio-views.json').read_text())
    items = [i for v in data['views'] if v['name'] == binding['view']
             for i in v['items'] if i['name'] == binding['item']]
    if len(items) != 1:
        raise ValueError(f'Example selector must identify one item: {key}')
    item = items[0]
    from host_paths import bootstrap
    bootstrap()
    from live import frame
    if item.get('url'):
        url = block_url(item['url'], root)
    elif item.get('block'):
        url = block_url('/_board/workbench?' + urlencode(
            {'path': item['block'], 'layout': 'focus'}), root)
    else:
        target = contained(root, item['path'])
        fragment = item.get('fragment', '')
        if fragment and not re.search(r'\bid=["\x27]' + re.escape(fragment) + r'["\x27]', target.read_text()):
            raise ValueError(f'Missing example fragment: {fragment}')
        if target.suffix == '.excalidraw':
            url = frame._draw_url(target, root)
        else:
            url = frame._file_url(target, root)
        if fragment:
            url += '#' + quote(fragment, safe='')
    return url, f'{source.name} / {binding["view"]} / {binding["item"]}'


def render(topic: Path, el: dict, root: Path) -> str:
    example = resolve(topic, el, root)
    if example is None:
        return ''
    url, label = example
    from live import ui_parts
    esc = html.escape
    # Shared open-dot styling and markup; iframe content retains its own renderer.
    frame = f'<iframe title="{esc(label, quote=True)}" loading="lazy" src="{esc(url, quote=True)}"></iframe>'
    preview = ui_parts.open_dot(frame, url, label, new_tab=True)
    style = '''<style>dd{min-width:0;overflow-wrap:anywhere}.requirement-example{margin-top:22px;min-width:0}.requirement-example>summary{cursor:pointer;font-weight:600;margin-bottom:14px}.requirement-example iframe{display:block;width:100%;height:520px;border:1px solid var(--line);border-radius:8px;box-sizing:border-box;background:var(--bg)}@media(max-width:600px){body{padding:14px 12px}dl{grid-template-columns:64px minmax(0,1fr);gap:8px}dt{font-size:10px}.requirement-example iframe{height:440px}}</style>'''
    return ui_parts.PB_CSS + style + '<details class="requirement-example"><summary>Example</summary>' + preview + '</details>'
