"""Check Paper's three Block Structure instances against the shared type.

Bindings and catalog checks are mandatory even with --bindings-only. Full checks
also verify the active folder trees, type pages, and example inventories.
Missing research execution adapters are tracked separately from Studio conformance.
"""
from __future__ import annotations
import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'PRINCIPLE.md').is_file())
BLOCK = ROOT / 'examples/Project-Ladder/blueprint/b16_theme_paper'
SHARED = ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts'
TYPE = ROOT / 'examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure'
TOPICS = ('s01-idea-block-structure', 's02-grant-block-structure', 's03-paper-block-structure')
sys.path.insert(0, str(SHARED))
import block_types_pages
from block_types_check import LEVELS, read_types


class TreeRows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section, self.parents, self.rows = '', [], {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section':
            self.section = attrs.get('id', '')
        if tag == 'details':
            self.parents.append('open' in attrs)
        if 'data-node' in attrs:
            attrs['opened'] = self.parents[-1] if tag == 'summary' else None
            self.rows[(self.section, attrs['data-node'])] = attrs

    def handle_endtag(self, tag):
        if tag == 'details':
            self.parents.pop()


def check_trees(topic, module):
    import mmtree
    errors, target = [], topic / 'structure/jobs.html'
    if not target.is_file():
        return [f'{topic.name}: folder-tree document missing']
    text = target.read_text()
    if text != module.structure_document(topic):
        errors.append(f'{topic.name}: shared folder-tree output is stale')
    if 'focus-map' in text or 'pm-map' in text or 'Open all' in text:
        errors.append(f'{topic.name}: Structure renders a mind map')
    parsed = TreeRows()
    parsed.feed(text)
    levels = ('', 'job-group', 'job-name', 'task-group', 'task-name')
    for key in ('folder', 'jobs', 'studio'):
        model = mmtree.load(topic / 'structure' / f'{key}.mindmap.md')
        for node, parent, depth, _ in mmtree.walk(model.root):
            row = parsed.rows.get((key + '-rules', node.id), {})
            if not row.get('title') or html.escape(node.text) not in text:
                errors.append(f'{topic.name}: missing tree row/purpose: {key}/{node.text}')
            if row.get('data-parent') != (parent.id if parent else ''):
                errors.append(f'{topic.name}: changed tree parent: {key}/{node.text}')
            if key == 'jobs' and (depth > 4 or row.get('data-level') != levels[depth]):
                errors.append(f'{topic.name}: incorrect Job-Task level: {node.text}')
            if key == 'folder' and (depth == 0 or node.id == 'jobs') and not row.get('opened'):
                errors.append(f'{topic.name}: Folder is not opened to the Job')
    css = ROOT / 'examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/structure.css'
    if '/' + css.relative_to(ROOT).as_posix() not in text:
        errors.append(f'{topic.name}: missing shared S71 level palette')
    palette = css.read_text()
    if 'prefers-color-scheme:dark' not in palette or any(f'data-level={level}' not in palette for level in levels[1:]):
        errors.append(f'{topic.name}: incomplete common level colours')
    return errors


def check_topic(topic, full=True):
    errors = []
    module = load_builder()
    if not (topic / 'types.md').is_file():
        return [f'{topic.name}: missing type catalog']
    example, types = read_types(topic / 'types.md')
    for level in LEVELS:
        if not types.get(level):
            errors.append(f'{topic.name}: missing {level}')
        for kind, about in types.get(level, {}).items():
            if not all(about.get(key) for key in ('for', 'holds')):
                errors.append(f'{topic.name}: {kind} lacks for/holds')
    manifest = json.loads((topic / 'studio-views.json').read_text())
    views = {v['name']: v['items'] for v in manifest['views']}
    expected = [v['name'] for v in json.loads((TYPE / 'studio-views.json').read_text())['views']]
    # The Check UI is opt-in (hai-studio/ref/check-view.md), not a content
    # view declared by elements.md. A type opting in does not opt in instances.
    if not manifest.get('check_type') and 'Check' in expected:
        expected.remove('Check')
    if not example:
        expected.remove('Examples')
    if list(views) != expected:
        errors.append(f'{topic.name}: views differ from the shared type')
    if [i['name'] for i in views.get('Structure', [])] != ['Folder', 'Job-Task', 'Studio']:
        errors.append(f'{topic.name}: Structure needs Folder / Job-Task / Studio')
    structure_path = (topic / 'structure/jobs.html').relative_to(ROOT).as_posix()
    for item, key in zip(views.get('Structure', []), ('folder', 'jobs', 'studio')):
        if item.get('path') != structure_path or item.get('fragment') != key + '-rules':
            errors.append(f'{topic.name}: Structure must bind the S71 folder tree: {key}')
    if len(views.get('Draw', [])) != 1 or not views['Draw'][0].get('path', '').endswith('.excalidraw'):
        errors.append(f'{topic.name}: Draw must open one canvas')
    for view, items in views.items():
        for item in items:
            if 'url' in item:
                url = urlparse(item['url'])
                query = parse_qs(url.query)
                target = (ROOT / query.get('path', [''])[0]).resolve()
                if (url.scheme or url.netloc or url.path != '/_board/workbench'
                        or not target.is_relative_to(ROOT) or not (target / 'board.md').is_file()):
                    errors.append(f'{topic.name}: live view is not a real Block')
                continue
            value = item.get('path', item.get('block', ''))
            target = (ROOT / value).resolve()
            if not value or not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f'{topic.name}: missing source {value}')
            if 'block' in item and not (target / 'board.md').is_file():
                errors.append(f'{topic.name}: example is not a real Block')
            if view == 'Skills' and target.name != 'SKILL.md':
                errors.append(f'{topic.name}: Skills does not open a skill file')
    studio = (topic / 'structure/studio.md').read_text()
    if not re.search(r'\bs[0-9]N\b', studio) or 'Studio type' not in studio:
        errors.append(f'{topic.name}: missing Studio band/type organization')
    if not (topic / 'structure/jobs.mindmap.md').is_file():
        errors.append(f'{topic.name}: authored organization outline missing')
    if example:
        live = {item['name']: item for item in views.get('Examples', [])}
        if any('url' not in live.get(name, {}) for name in ('Folder', 'Job-Task', 'Studio')):
            errors.append(f'{topic.name}: example inventories must open live Block sources')
    for target, text in module.type_outputs(topic).items():
        if not target.is_file() or target.read_text() != text:
            errors.append(f'{topic.name}: stale type page or binding: {target.name}')
        if target.suffix == '.html':
            for href in re.findall(r'href="([^"]+)"', text):
                query = parse_qs(urlparse(html.unescape(href)).query)
                if 'path' in query and not (ROOT / query['path'][0] / 'board.md').is_file():
                    errors.append(f'{topic.name}: a type member leaves its Block')
    if full:
        errors.extend(check_trees(topic, module))
        import mmtree
        drawing = json.loads((topic / 'structure/type.excalidraw').read_text())
        drawn = {(el.get('customData', {}).get('map'), el.get('customData', {}).get('node')): el
                 for el in drawing['elements'] if el.get('type') == 'text' and not el.get('isDeleted')}
        for key in ('folder', 'jobs', 'studio'):
            tree = mmtree.load(topic / 'structure' / f'{key}.mindmap.md')
            if key == 'jobs' and topic.name.startswith('s03-'):
                if [n.text for n in tree.root.children] != ['Story', 'Evidence', 'Display', 'Writing', 'Presentation']:
                    errors.append(f'{topic.name}: Paper needs its five named branches')
            for node, parent, _, _ in mmtree.walk(tree.root):
                el = drawn.get((key, node.id), {})
                if el.get('text') != node.text or el.get('customData', {}).get('parent') != (parent.id if parent else None):
                    errors.append(f'{topic.name}: Draw omits or changes {key}/{node.text}')
        if topic.name.startswith('s01-'):
            names = {n.text for n, *_ in mmtree.walk(mmtree.load(topic / 'structure/folder.mindmap.md').root)}
            for required in ('cards/', 'workflow/', 'ideation.yaml', 'paper-ideation-sync.yaml', 'paper-ideation.yaml'):
                if required not in names:
                    errors.append(f'{topic.name}: Idea Folder lacks {required}')
        for target, text in module.example_maps(topic).items():
            if not target.is_file() or target.read_text() != text:
                errors.append(f'{topic.name}: stale example inventory: {target.name}')
    return errors


def load_builder():
    p = BLOCK / 'delivery/page-spec/build_block_structures.py'
    spec = importlib.util.spec_from_file_location('paper_structure_builder', p)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bindings-only', action='store_true')
    args = ap.parse_args()
    errors = [e for name in TOPICS for e in check_topic(BLOCK / name, not args.bindings_only)]
    from check_examples import problems as example_problems
    errors.extend(example_problems())
    for error in errors:
        print('FAIL:', error)
    print(f'Block Structure: {len(TOPICS)} instances, {len(errors)} problems')
    if not errors:
        print('Live example content is verified; scientific execution and proposed record contracts remain separate.')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
