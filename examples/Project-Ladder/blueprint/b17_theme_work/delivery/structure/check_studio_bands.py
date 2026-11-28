"""Read-only checks for the Block types' native Studio organization maps.

Compare content bands with the contract and Blueprint bands with the registry;
verify Structure binds to a Folder Tree and keeps the existing drawing.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'PRINCIPLE.md').is_file())
BLOCK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-mindmap/scripts'))
import mmtree as MT

TOPICS = {
    'Work': 's01-work-structure',
    'Blueprint': 's02-blueprint-structure',
    'CoWork': 's03-cowork-structure',
    'Discovery': 's04-discovery-structure',
}


def expected_bands(block: Path) -> dict[str, list[str]]:
    contract = (block / 'delivery/page-spec/studio-bands-by-block-type.md').read_text()
    out: dict[str, list[str]] = {}
    for line in contract.splitlines():
        if line.startswith('| '):
            cells = [s.strip() for s in line.strip('|').split('|')]
            if len(cells) == 4 and cells[0] in (*TOPICS, 'Knowledge'):
                out.setdefault(cells[0], []).append(cells[1])
    registry = json.loads((block / 'delivery/page-spec/studio-bands.json').read_text())['bands']
    out['Blueprint'] = list(dict.fromkeys(row['name'] for row in registry))
    return out


def map_errors(mm, kind: str, expected: list[str]) -> list[str]:
    errors = []
    if [n.text for n in mm.root.children] != expected:
        errors.append(f'{kind}: Band names/order differ from the content contract')
    if mm.meta.get('block-type') != kind:
        errors.append(f'{kind}: wrong Block type metadata')
    ids = [n.id for n, _, _, _ in MT.walk(mm.root)]
    if len(ids) != len(set(ids)) or any(not key for key in ids):
        errors.append(f'{kind}: missing or duplicate node id')
    for band in mm.root.children:
        if not band.note or not band.children:
            errors.append(f'{kind}/{band.text}: needs a purpose and illustrative topic')
        for topic in band.children:
            if not (topic.text.startswith('〈') and topic.text.endswith('〉')):
                errors.append(f'{kind}/{band.text}: example topic must be bracketed')
    return errors


def check(block=BLOCK, root=ROOT) -> list[str]:
    expected = expected_bands(block)
    errors = []
    for kind, folder in TOPICS.items():
        topic = block / folder
        source = topic / 'studio-organization.mindmap.md'
        try:
            mm = MT.load(source)
            errors.extend(map_errors(mm, kind, expected[kind]))
            manifest = json.loads((topic / 'studio-views.json').read_text())
            views = {view['name']: view for view in manifest['views']}
            items = [i for i in views['Structure']['items'] if i['name'] == 'Studio']
            page = block / 'delivery/structure' / (kind.lower() + '-organization.html')
            if len(items) != 1 or items[0].get('fragment') != 'studio-rules' or (root / items[0].get('path', '')).resolve() != page.resolve():
                errors.append(f'{folder}: Structure Studio must bind to the Folder Tree')
            text = page.read_text()
            section = re.search(r'<section id="studio-rules".*?</section>', text, re.S)
            if not section or '<ul class="tree">' not in section[0] or '<details' not in section[0] or 'pm-folds' in section[0] or '<svg' in section[0]:
                errors.append(f'{folder}: Studio rules must render a collapsible Folder Tree')
            if section and any(band not in section[0] for band in expected[kind]):
                errors.append(f'{folder}: displayed tree omits a Band')
            if any(i.get('path', '').endswith('studio-organization.mindmap.md') for i in views['Draw']['items']):
                errors.append(f'{folder}: injected Studio map must not replace the drawing')
            if not any(item.get('path', '').endswith('.excalidraw') for item in views['Draw']['items']):
                errors.append(f'{folder}: original drawing entry missing')
            if 'organization.html#studio-rules' not in (topic / f'{folder}.md').read_text():
                errors.append(f'{folder}: face does not link its organization map')
        except (OSError, ValueError, KeyError, MT.GrammarError) as exc:
            errors.append(f'{folder}: {exc}')
    return errors


if __name__ == '__main__':
    problems = check()
    print('\n'.join(problems) if problems else 'Studio Band contract, maps and bindings agree.')
    raise SystemExit(bool(problems))
