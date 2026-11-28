"""Optional authored Studio views, using the shared tabs and file reader.

studio-views.json: {"views": [{"name": "Skills", "items":
[{"name": "skill-name", "path": "SPACE-relative/path/SKILL.md"}]}]}.
Items may instead name an existing Block directory with "block". Optional "fragment"
selects a file's drawing. A view whose one item is a Markdown file with two or more `##` sections shows a left tab per section (md_sections). An item may name a folder with "folder": its files show as folds (folder_folds). An item may instead name a live workbench page with "url" (an origin-relative
/_board/workbench? address, a part outlined by its mark=); "old": true reads an item faded. All sources stay inside the SPACE; no external URLs or child pages.
"""
import json
from pathlib import Path
from urllib.parse import urlencode, quote

from live import frame


def read_views(topic: Path, root: Path):
    manifest = topic / 'studio-views.json'
    root = root.resolve()
    if not manifest.is_file() or not manifest.resolve().is_relative_to(root):
        return None
    try:
        data = json.loads(manifest.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get('views'), list):
        return None
    views, parts, seen = [], {}, set()
    for view in data['views']:
        if not isinstance(view, dict):
            continue
        name = view.get('name')
        if not isinstance(name, str) or not name.strip() or name in seen:
            continue
        rows = view.get('items')
        if not isinstance(rows, list):
            continue
        items = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            label, path = row.get('name'), row.get('block', row.get('path'))
            live = row.get('url')       # a live workbench page, a part outlined by mark= (b17 trace 261127/1440)
            if isinstance(label, str) and label.strip() and isinstance(live, str) and live.startswith(frame.ROUTE + '?'):
                items.append((label, live, bool(row.get('old'))))
                continue
            folder = row.get('folder')  # a folder: one fold per file on the right (folder_folds; b17 trace 261127/1405)
            if isinstance(label, str) and label.strip() and isinstance(folder, str):
                from live.folder_folds import folder_item
                skip = [s for s in row.get('skip', []) if isinstance(s, str)] if isinstance(row.get('skip'), list) else []
                held = None if Path(folder).is_absolute() or ':' in folder else folder_item(root / folder, root, skip)
                if held is not None:
                    items.append((label, held, bool(row.get('old'))))
                continue
            if not isinstance(label, str) or not label.strip() or not isinstance(path, str):
                continue
            if Path(path).is_absolute() or ':' in path:
                continue
            target = (root / path).resolve()
            if not target.is_relative_to(root):
                continue
            if 'block' in row:
                board = target / 'board.md'
                if not target.is_dir() or not board.is_file() or not board.resolve().is_relative_to(root):
                    continue
                href = frame.ROUTE + '?' + urlencode({'path': str(target.relative_to(root)),
                                                      'layout': 'focus', 'section': 'work'})
            else:
                if not target.is_file():
                    continue
                if target.name.endswith('.mindmap.md'):
                    href = frame.ROUTE + '?' + urlencode({'view': 'focus-map',
                        'path': str(target.relative_to(root)), 'fit': '1'})
                else:
                    href = (frame._draw_url(target, root) if target.suffix.lower() == '.excalidraw'
                            else frame._file_url(target, root))
                fragment = row.get('fragment')
                if isinstance(fragment, str) and fragment:
                    href += '#' + quote(fragment, safe='')
            items.append((label, href, bool(row.get('old'))))
        if len(items) == 1 and len(rows) == 1 and isinstance(rows[0], dict) and not rows[0].get('fragment'):
            items = _sections(rows[0], items, root)       # one Markdown file: its sections are the left tabs
        if items:
            seen.add(name)
            views.append((name, items[0][1], ''))
            parts[name] = items
    return (views, parts) if views else None


def _sections(row: dict, items: list, root: Path) -> list:
    """One item per `##` section of the view's only Markdown file (md_sections); the item itself otherwise."""
    from live.md_sections import sections_of
    path = row.get('path')
    if 'block' in row or not isinstance(path, str) or not path.lower().endswith('.md'):
        return items
    names = sections_of(root / path)
    _, href, old = items[0]
    return [(title, f'{href}&section={n}', old) for n, title in enumerate(names)] or items
