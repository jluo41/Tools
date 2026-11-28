"""Knowledge content only; reuse shared folder trees, type pages and the drawing kit."""
from __future__ import annotations

import argparse
import copy
import hashlib
from html import escape
import importlib.util
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
NAME = HERE.name
STUDIO = ROOT / "plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts"
sys.path.insert(0, str(STUDIO))
sys.path.insert(0, str(STUDIO.parent / "gallery/block-structure/scripts"))   # the Block Structure type's own scripts
import quick_draw as Q
import icons
import block_types_check
import block_types_pages as type_pages


def shared():
    source = HERE.parent / "delivery/structure/build_organization.py"
    spec = importlib.util.spec_from_file_location("shared_organization", source)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def type_anchor(level, name):
    key = type_pages.slug(name) or hashlib.sha256(name.encode()).hexdigest()[:8]
    return type_pages.slug(level) + '--' + key


def type_content():
    """Read local uses and resolve shared requirements from their owning file."""
    _, types = block_types_check.read_types(HERE / 'types.md')
    level = name = None
    details = {}
    for line in (HERE / 'types.md').read_text().splitlines():
        if line.startswith('## '):
            level, name = line[3:].strip(), None
        elif line.startswith('### '):
            name = line[4:].strip()
            details[(level, name)] = {}
        elif name and re.match(r'^(ref|use):', line):
            key, value = line.split(':', 1)
            details[(level, name)][key] = value.strip()
    for level, entries in types.items():
        for name, fields in entries.items():
            detail = details[(level, name)]
            source = None
            if 'ref' in detail:
                path, source_level, source_name = [p.strip() for p in detail['ref'].split('|')]
                source = (HERE / path).resolve()
                _, shared_types = block_types_check.read_types(source)
                fields = shared_types[source_level][source_name]
            yield level, name, fields, detail['use'], source


def manifest():
    data = json.loads((HERE / 'studio-views.json').read_text())
    rows = list(type_content())
    path = (HERE / 'delivery/structure.html').relative_to(ROOT).as_posix()
    views = [{'name': view, 'items': [
        {'name': f'{level} · {name}', 'path': path, 'fragment': type_anchor(level, name)}
        for level, name, *_ in rows if level in levels]}
        for view, levels in type_pages.VIEWS.items()]
    kept = [v for v in data['views'] if v['name'] not in type_pages.VIEWS]
    at = next(i + 1 for i, v in enumerate(kept) if v['name'] == 'Structure')
    data['views'] = kept[:at] + views + kept[at:]
    data['check_type'] = 'block-structure'                       # s05 follows the Block Structure type (s71)
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def structure_tree(common, model, key):
    """Adapt authored content to the shared Folder Tree and S71 level palette."""
    mt = common.shared_mindmap().MT
    rows = list(mt.walk(model))
    roles = ('', 'Job group', 'Job name', 'Task group', 'Task name')
    levels = ('', 'job-group', 'job-name', 'task-group', 'task-name')

    def tree(node):
        return common.node(node.text, *(tree(child) for child in node.children))

    rendered = common.tree_html(tree(model), folder=key == 'Folder',
                                roles=roles if key == 'Job-Task' else ())
    nodes = iter(rows)

    def annotate(match):
        node, parent, depth, _ = next(nodes)
        detail = mt.display(' '.join(node.note)) or node.text
        level = levels[depth] if key == 'Job-Task' else ''
        tag = 'summary' if match.group(0) == '<summary>' else 'span'
        cls = 'lvl' if tag == 'summary' else 'leaf lvl'
        return (f'<{tag} class="{cls}" title="{escape(detail, quote=True)}" '
                f'data-node="{escape(node.id)}" data-level="{level}">')

    rendered = re.sub(r'<summary>|<span class="leaf">', annotate, rendered)
    parents = iter((node, depth) for node, _, depth, _ in rows if node.children)

    def opened(_):
        node, depth = next(parents)
        keep = depth == 0 or (key == 'Folder' and node.id == 'jobs') or key == 'Job-Task'
        return '<details open>' if keep else '<details>'

    rendered = re.sub(r'<details open>', opened, rendered)
    return '<div class="drawing"><ul class="tree rule"><li>' + rendered + '</li></ul></div>'


def document():
    common = shared()
    mm = common.shared_mindmap()
    model = mm.MT.load(HERE / f"{NAME}.mindmap.md")
    sections = []
    anchors = {"Folder": "folder-rules", "Job-Task": "jobs-rules", "Studio": "studio-rules"}
    for node in model.root.children:
        anchor = anchors[node.text]
        content = structure_tree(common, node.children[0], node.text)
        sections.append(f'<section class="part" id="{anchor}">{content}</section>')
    for level, name, fields, use, source in type_content():
        anchor = type_anchor(level, name)
        example, _ = block_types_check.read_types(HERE / 'types.md')
        real = type_pages.members(ROOT / example, level, name)
        page = type_pages.page(level, name, fields, real)
        content = page.partition('<body>')[2].partition('</body>')[0]
        content += f'<p>{escape(use)}</p>'
        if source:
            href = '/' + source.relative_to(ROOT).as_posix()
            content += f'<p><a href="{escape(href)}" target="_blank">Work · {escape(level)} · {escape(name)}</a></p>'
        sections.append(f'<section class="part" id="{anchor}">{content}</section>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Knowledge structure</title><style>' + type_pages.CSS + common.STYLE +
            '.part{display:none}.part:target{display:block}'
            'body:not(:has(:target)) #folder-rules{display:block}'
            '</style><link rel="stylesheet" href="/examples/Project-Ladder/blueprint/'
            'b11_theme_insight/delivery/structure/structure.css"></head><body><main>'
            + ''.join(sections) + '</main></body></html>')


def drawing():
    """Resource feeds three knowledge bands; they can share optional practice."""
    random.seed(5)
    els = []

    def words(key, x, y, text, size=25, color=Q.ON):
        added = Q.text(key, x, y, text, size, color)
        for el in added:
            el['fontFamily'] = 6
            el['width'] = max(len(t) for t in text.splitlines()) * size * 0.62
        els.extend(added)

    words('title', 40, 20, 'Knowledge: resources to understanding', 38, Q.TITLE)
    els += icons.document('band-resources', 490, 120, 'off', w=100, h=135)
    words('resources-band', 630, 120, 'Resource · s0N', 32)
    words('resources-topic', 630, 170, 's0N-〈source-selection〉', 25)
    words('resources-detail', 630, 215, 'Link · Version · Precise location', 23)
    words('resources-owner', 630, 255, 'Reference Related / Discovery originals', 23)
    bands = [('methods', 280, 'Method · s2N', 's2N-〈method-question〉'),
             ('application', 880, 'Application · s3N', 's3N-〈application-question〉')]
    for key, x, label, topic in bands:
        els += icons.person('band-' + key, x, 440, 'off', s=0.8)
        words('band-' + key + '-name', x + 105, 440, label, 25)
        words('band-' + key + '-topic', x + 105, 520, topic, 21)
        els += Q.arrow('resource-to-' + key, [(540, 285), (540, 350), (x + 40, 350), (x + 40, 420)])
        els += Q.arrow('band-' + key + '-practice', [(x + 50, 570), (x + 50, 650), (620, 740)], dashed=True)
    els += icons.laptop('optional-practice', 555, 765, 'off')
    words('practice-goal', 750, 780, 'jNN_〈practice-goal〉', 28)
    words('practice-unit', 750, 825, 'tNN_〈execution-unit〉', 24)
    words('practice-optional', 750, 865, 'Create for executable practice', 23)
    els += Q.arrow('practice-feedback', [(550, 850), (360, 850), (360, 570)])
    words('practice-feedback-name', 40, 790, 'Practice informs explanation', 25)
    els += icons.person('band-questions', 1450, 440, 'off', s=0.8)
    words('band-questions-name', 1555, 440, 'Question · s4N', 25)
    words('band-questions-topic', 1555, 520, "s4N-〈learner's question〉", 21)
    words('band-questions-detail', 1555, 560, 'The learner\'s own words;\nanswered from Resource', 21)
    els += Q.arrow('resource-to-questions', [(540, 285), (540, 350), (1490, 350), (1490, 420)])
    words('band-scope', 40, 970, 'Resource comes first, the learner\'s Question last; Bands add no folders.', 27)
    return els


def fingerprint(el):
    payload = {k: v for k, v in el.items()
               if k not in ('customData', 'version', 'versionNonce', 'updated', 'seed')}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def merge_drawing(old, fresh):
    """Preserve edits, additions and removals against the last generated seed."""
    seed = old.get('knowledgeSeed', {})
    if not seed:
        seed = next(({'owner': NAME, 'ids': e['customData']['seedIds']}
                     for e in old.get('elements', [])
                     if (e.get('customData') or {}).get('owner') == NAME
                     and 'seedIds' in e['customData']), {})
    managed = seed.get('owner') == NAME or any(
        (e.get('customData') or {}).get('owner') == NAME for e in old.get('elements', []))
    keep, edited = [], {}
    removed = set(seed.get('ids', [])) - {e['id'] for e in old.get('elements', [])}
    if managed:
        for el in old['elements']:
            data = el.get('customData') or {}
            if data.get('owner') != NAME:
                keep.append(el)
            elif data.get('baseline') != fingerprint(el):
                edited[el['id']] = el
    elif old:
        raise ValueError('Refuse to replace an unrecognized authored drawing')
    ids = [e['id'] for e in fresh]
    for el in fresh:
        el['customData'] = {'owner': NAME, 'baseline': fingerprint(el), 'seedIds': ids}
    els = [edited.pop(e['id'], e) for e in fresh if e['id'] not in removed]
    return els + list(edited.values()) + keep, {'owner': NAME, 'ids': ids}


def write_drawing():
    target = HERE / f'{NAME}.excalidraw'
    old = json.loads(target.read_text()) if target.exists() else {}
    els, seed = merge_drawing(old, drawing())
    Q.write(target, els)
    data = json.loads(target.read_text())
    data['knowledgeSeed'] = seed
    for key in ('files', 'appState'):
        if key in old:
            data[key] = old[key]
    target.write_text(json.dumps(data, ensure_ascii=False) + '\n')
    subprocess.run([os.environ.get('STUDIO_PREVIEW_PYTHON', 'python3'),
                    str(STUDIO / 'render_png.py'), str(target),
                    str(HERE / f'{NAME}.png'), '1'], check=True)


def check():
    target = HERE / 'delivery/structure.html'
    assert target.read_text() == document(), 'Rebuild the generated structure content'
    html = target.read_text()
    model = shared().shared_mindmap().MT.load(HERE / f'{NAME}.mindmap.md')
    sections = {n.text: n.children[0] for n in model.root.children}
    assert list(sections) == ['Folder', 'Job-Task', 'Studio']
    bands = sections['Studio'].children
    assert [n.id for n in bands] == ['resources', 'methods', 'applications', 'questions']
    assert [n.text for n in bands] == ['📚 Resource · s0N',
                                     '🧭 Method · s2N', '🎯 Application · s3N',
                                     '🤔 Question · s4N']
    mt = shared().shared_mindmap().MT
    job_nodes = list(mt.walk(sections['Job-Task']))
    assert max(depth for _, _, depth, _ in job_nodes) == 4
    assert not any('runs/' in n.text for n, _, _, _ in job_nodes)
    assert html.count('class="tree rule"') == 3 and 'class="pm' not in html
    assert all(f'data-level="{level}"' in html for level in
               ('job-group', 'job-name', 'task-group', 'task-name'))
    assert 'b11_theme_insight/delivery/structure/structure.css' in html
    definitions = (HERE.parent / 'delivery/page-spec/studio-bands-by-block-type.md').read_text()
    assert re.findall(r'^\| Knowledge \| ([^|]+) \|', definitions, re.M) == [
        'Resource', 'Method', 'Application', 'Question']
    example = ROOT / 'examples/Project-Ladder/knowledge/b18_a2ui_learning'
    face = (example / 'board.md').read_text()
    assert 'bands: j0N 🃏 Interactive card · s0N 📚 Resource · s1N 🧭 Method · s2N 🧭 Method · s3N 🎯 Application · s4N 🤔 Question' in face
    expected_topics = ['s01-official-sources', 's11-messages-components-data',
                       's21-tracing-interaction', 's22-chatbot-to-a2ui', 's31-use-cases-boundaries',
                       's41-agent-text-to-a2ui', 's42-who-writes-the-json']
    assert sorted(p.name for p in example.glob('s[0-9][0-9]-*')) == expected_topics
    assert [p.name for p in example.glob('j[0-9][0-9]_*')] == ['j01_interactive_card']  # the one optional practice Job, s15's example
    assert not re.search('[\u4e00-\u9fff]', face)
    assert not block_types_check.problems(HERE / 'types.md')
    resolved = list(type_content())
    assert {row[0] for row in resolved} == set(block_types_check.LEVELS)
    assert all(row[4] for row in resolved if row[0] != 'Job group type')
    assert (HERE / 'studio-views.json').read_text() == manifest(), 'Rebuild type view bindings'
    source = json.loads((HERE / 'studio-views.json').read_text())
    structure = next(v for v in source['views'] if v['name'] == 'Structure')
    assert [i['name'] for i in structure['items']] == ['Folder', 'Job-Task', 'Studio']
    for view in source['views']:
        for row in view['items']:
            if 'path' in row:
                assert (ROOT / row['path']).is_file(), row
            if 'fragment' in row:
                assert f'id="{row["fragment"]}"' in target.read_text(), row
            if 'url' in row:
                assert row['url'].startswith('/_board/workbench?'), row
                if row.get('name') == 'A2UI':
                    assert 'section=studio' in row['url']
    data = json.loads((HERE / f'{NAME}.excalidraw').read_text())
    ids = [e['id'] for e in data['elements']]
    assert len(ids) == len(set(ids)), 'Repeated drawing ids'
    assert any(e['type'] == 'arrow' for e in data['elements'])
    assert (HERE / f'{NAME}.png').is_file()
    # Regression guard for the Studio seed contract; all mutations stay in memory.
    seed_elements, seed = merge_drawing({}, drawing())
    probe = {'elements': copy.deepcopy(seed_elements), 'knowledgeSeed': seed}
    removed = probe['elements'].pop(0)['id']
    edited = probe['elements'][0]
    edited['x'] += 37
    extra = copy.deepcopy(probe['elements'][1])
    extra['id'] = 'human-added'
    extra.pop('customData', None)
    probe['elements'].append(extra)
    probe.pop('knowledgeSeed', None)  # Excalidraw may serialize only element metadata.
    merged, _ = merge_drawing(probe, drawing())
    by_id = {e['id']: e for e in merged}
    assert removed not in by_id
    assert by_id[edited['id']]['x'] == edited['x'] and by_id['human-added'] == extra
    try:
        merge_drawing({'source': 'hai-studio quick_draw', 'elements': []}, drawing())
    except ValueError:
        pass
    else:
        raise AssertionError('An unowned drawing must not be replaced')
    print('Knowledge structure: generated content, bindings and drawing checked')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--content-only', action='store_true', help='Rebuild HTML without touching drawings')
    args = parser.parse_args()
    if args.check:
        check()
    else:
        (HERE / 'delivery').mkdir(exist_ok=True)
        (HERE / 'studio-views.json').write_text(manifest())
        (HERE / 'delivery/structure.html').write_text(document())
        if not args.content_only:
            write_drawing()
