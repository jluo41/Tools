"""Adapt Labeling content to shared folder trees, drawings and Studio readers."""
from html import escape as esc, unescape
from pathlib import Path
import json
import re
import sys
from urllib.parse import urlencode, parse_qs, urlsplit

TOPICS = {'itemization': 's01-labeling-ladder', 'guideline': 's02-labeling-workbench', 'scale': 's03-agent-role'}


def map_module():
    from live import frame
    return frame.mindmap_module()


def entry(key, role, words, note=(), children=()):
    return map_module().MT.Node(key, f'[{role}] {words}', children=list(children), note=list(note))


def proof_notes(proofs):
    return [f'[{p["label"]}]({p["path"]})' for p in proofs]


def organization_tree(model, concrete=False):
    """Content and grouping shared by the folder-tree and drawing adapters."""
    mm = map_module()
    groups = {}
    for task in model['tasks']:
        kind = task['type']
        if kind not in groups:
            note = [task['role'], *proof_notes(task['evidence'])]
            if task['optional']:
                note.insert(0, 'Optional; requires separately authorized external ground truth.')
            groups[kind] = entry('type-' + kind, 'Task Type', kind, note)
        label = task['example_label'] if concrete else task['naming']['label']
        note = ([task['name'], task['name_basis']] if concrete else
                [task['naming']['rule'], task['naming']['basis']])
        note += proof_notes(task['evidence'])
        if not any(n.note == note for n in groups[kind].children):
            groups[kind].children.append(entry('name-' + kind + '-' + str(len(groups[kind].children)),
                                               'Task Name', label, note))
    label = model['example_label'] if concrete else model['job_naming']['label']
    note = [model['job_unit'], *model['gaps'], *proof_notes(model['evidence'])]
    note[:0] = ([model['job_name'], model['name_basis']] if concrete else
                [model['job_naming']['rule'], model['job_naming']['basis']])
    job = entry('job-name', 'Job Name', label, note, groups.values())
    kind = entry('job-type', 'Job Type', model['job_type'] or model['job_type_action'], children=[job])
    root = mm.MT.Node('root', model['name'], children=[kind])
    if concrete and model['name_basis'] == 'Preview model':
        root.note = ['Design example; proposed Jobs and Tasks are not created records.']
    return mm.MT.MindMap({'mindmap': '1', 'written': 'yes'}, root)


def example_tree(model):
    tree = organization_tree(model, concrete=True)
    case = model.get('existing_example')
    if case:
        task = entry('existing-task', 'Task Name', 'Chats as items',
                     [case['task_name'], f'[Task source]({case["task_path"]})'])
        kind = entry('existing-task-type', 'Task Type', case['task_type'], children=[task])
        job = entry('existing-job', 'Job Name', 'Response safety',
                    [case['job_name'], 'Existing synthetic example in the combined labeling Block.',
                     f'[Job source]({case["job_path"]})'], [kind])
        tree.root.children.insert(0, entry('existing', 'Example', 'Existing records', children=[job]))
        tree.root.note = []
        tree.root.children[-1].text = '[Job Type] ' + model['job_type_action']
    return tree


def studio_tree(model):
    mm = map_module()
    owners = {}
    labels = {'block': ('Owner', 'Block'), 'job': ('Owner', 'Job')}
    for studio in model['studio']:
        owner = studio['owner']
        if owner not in owners:
            role, label = labels.get(owner, ('Task Type', owner))
            owners[owner] = entry('owner-' + owner, role, label)
        owners[owner].children.append(entry('studio-' + str(len(owners[owner].children)) + '-' + owner,
            'Studio', studio['name'], [studio['role'], 'Proposed discussion topic; this diagram creates no folder.']))
    band = model['studio_band']
    node = entry('studio-band', 'Band', band['name'],
                 [band['numbers'], band['note'], *[f'[Source]({p})' for p in band['sources']]], owners.values())
    return mm.MT.MindMap({'mindmap': '1', 'written': 'yes'}, mm.MT.Node('root', model['name'], children=[node]))


def draw(tree, root):
    from live import frame
    mm = map_module()
    def source_url(path):
        path = path.resolve()
        return frame._file_url(path, root) if path.is_relative_to(root) and path.is_file() else ''
    return '<div class="sd-map-frame">' + mm.draw(tree, editable=False, base=root, url_of=source_url, fold=True) + '</div>'


def contract_notes(model, root):
    from live import frame
    proofs = [{'label': 'Type catalog', 'path': model['type_catalog']},
              {'label': 'Block Structure definition', 'path': model['studio_type_source']},
              *model['evidence'], *(p for t in model['tasks'] for p in t['evidence'])]
    out = '<details class="sd-notes"><summary>Contract</summary><p>' + esc(model['job_unit']) + '</p>'
    out += '<dl><dt>Job topic</dt><dd>' + esc('〈' + model['job_topic'] + '〉') + '</dd>'
    out += '<dt>Task topic</dt><dd>' + esc(model['task_topic'] or 'No separate grouping defined') + '</dd></dl>'
    out += '<ul>' + ''.join('<li>' + esc(g) + '</li>' for g in model['gaps']) + '</ul></details>'
    out += '<details class="sd-notes"><summary>Sources</summary><ul>'
    for p in proofs:
        href = frame._file_url(root / p['path'], root)
        out += f'<li><a href="{esc(href, quote=True)}" target="_blank" rel="noopener" title="{esc(p["path"], quote=True)}">{esc(p["label"])}</a></li>'
    return out + '</ul></details>'


def tree_module():
    """b17's folder tree (tree_html, node, its CSS): the one tree every Block Structure topic draws; used, never copied."""
    import importlib.util
    path = Path(__file__).resolve().parents[3] / 'b17_theme_work/delivery/structure/build_organization.py'
    spec = importlib.util.spec_from_file_location('b17_build_organization', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tree_css():
    """Only the tree's own rules from b17's STYLE; the page keeps the shared focus look."""
    keep = ('.tree', 'summary', '.leaf', '.role', '.drawing')
    return '\n'.join(line for line in tree_module().STYLE.splitlines() if line.startswith(keep))


def folder_tree(tree, root, sources=True):
    """Adapt the verified hierarchy to Work's folder tree; keep notes and source files."""
    from live import frame
    shared = tree_module()
    files = {}

    def adapt(item):
        match = re.match(r'^\[([^]]+)\]\s*(.*)$', item.text)
        label = f'{match[1]} · {match[2]}' if match else item.text
        notes = []
        for note in item.note:
            links = re.findall(r'\[([^]]+)\]\(([^)]+)\)', note)
            for name, source in links:
                path = (root / source).resolve()
                if path.is_relative_to(root) and path.is_file():
                    files.setdefault(source, name)
            plain = re.sub(r'\[([^]]+)\]\(([^)]+)\)', r'\1', note).strip()
            if plain:
                notes.append(plain)
        if notes:
            shared.PURPOSE[label] = '\n'.join(notes)
        return shared.node(label, *(adapt(child) for child in item.children))

    markup = shared.tree_html(adapt(tree.root), purpose=True).replace('<details open>', '<details>')
    out = '<div class="drawing"><ul class="tree"><li>' + markup + '</li></ul></div>'
    if sources and files:
        out += '<details class="sd-notes"><summary>Sources</summary><ul>'
        for path, name in files.items():
            href = frame._file_url(root / path, root)
            out += (f'<li><a href="{esc(href, quote=True)}" target="_blank" rel="noopener" '
                    f'title="{esc(path, quote=True)}">{esc(name)}</a></li>')
        out += '</ul></details>'
    return out


def folder_rule(model):
    """A naming pattern, through Work's existing folder-tree renderer."""
    t = tree_module()
    node, block = t.node, 'bNN_〈block〉/'
    tasks = [node(task['folder'], node(task['folder'].rstrip('/') + '.md'), node('runs/')) for task in model['tasks']]
    job = node(model['job_folder'], node(model['job_folder'].rstrip('/') + '.md'), *tasks)
    folder = node(block, node('board.md'), job, node('sNN-〈topic〉/'), node('trace/'), node('related/'), node('delivery/'))
    return '<div class="drawing"><ul class="tree"><li>' + t.tree_html(folder, True).replace('<details open>', '<details>') + '</li></ul></div>'


EXAMPLE_FOLDER = {'itemization': 'examples/Project-Ladder/labeling/b02_labeling_walkthrough',
                  'guideline': 'examples/Project-Ladder/labeling/b02_labeling_walkthrough',
                  'scale': 'examples/Project-Ladder/labeling/b05_labeling_at_scale'}


def folder_example(model, root):
    """The example Block's folders as stored, without inventing or truncating paths."""
    node = tree_module().node

    def read(path):
        kids = sorted((p for p in path.iterdir() if not p.name.startswith('.') and p.name != '__pycache__'),
                      key=lambda p: p.name) if path.is_dir() and not path.is_symlink() else []
        return node(path.name + ('/' if path.is_dir() else ''), *(read(p) for p in kids))

    tree = tree_module().tree_html(read(root / EXAMPLE_FOLDER[model['id']]), True).replace('<details open>', '<details>')
    return '<div class="drawing"><ul class="tree"><li>' + tree + '</li></ul></div>'


def case_fold(name, body):
    return f'<details class="sd-example"><summary>{esc(name)}</summary>{body}</details>'


def block_preview(block, section, root):
    """Use the same frame, lazy loader and pop-out as the owning Studio."""
    from live import frame, studio_tabs
    assert (root / block / 'board.md').is_file(), block
    href = frame.ROUTE + '?' + urlencode({'path': block, 'layout': 'focus', 'section': section})
    return '<div class="studio-topic-content">' + studio_tabs.frame_of(Path(block).name, 'Block', href) + '</div>'


def studio_examples(model, root, visual=draw):
    mm = map_module()
    owners = {}
    for example in model['studio_examples']:
        owner = example['owner']
        if owner not in owners:
            owners[owner] = entry('example-owner-' + owner, 'Task Type', owner)
        owners[owner].children.append(entry('example-studio-' + owner + '-' + str(len(owners[owner].children)),
            'Studio', example['name'], [f'[Topic source]({example["path"]})']))
    if not owners:
        return ''
    tree = mm.MT.MindMap({'mindmap': '1', 'written': 'yes'},
                        mm.MT.Node('root', Path(model['record_block']).name, children=list(owners.values())))
    return case_fold('Example topics', visual(tree, root) + block_preview(model['record_block'], 'studio', root))


def contents(model, root):
    folder = folder_rule(model) + case_fold(Path(EXAMPLE_FOLDER[model['id']]).name,
        folder_example(model, root) + block_preview(EXAMPLE_FOLDER[model['id']], 'work', root))

    def examples(visual):
        body = visual(example_tree(model), root)
        if model['record_block']:
            body += case_fold(Path(model['record_block']).name, block_preview(model['record_block'], 'work', root))
        return body + case_fold(model['name'] + ' design', block_preview(model['example_block'], 'work', root))

    jobs = (folder_tree(organization_tree(model), root, sources=False)
            + case_fold('Examples', examples(folder_tree)) + contract_notes(model, root))
    studio = folder_tree(studio_tree(model), root) + studio_examples(model, root, folder_tree)
    draw_jobs = draw(organization_tree(model), root) + case_fold('Examples', examples(draw)) + contract_notes(model, root)
    draw_studio = draw(studio_tree(model), root) + studio_examples(model, root)
    # Existing fragments stay readable; all current bindings use the three combined subjects.
    return {'folder-rules': folder, 'jobs': jobs, 'studio': studio,
            'folder': folder_example(model, root), 'jobs-rules': jobs, 'studio-rules': studio,
            'examples': examples(folder_tree), 'draw-jobs': draw_jobs, 'draw-studio': draw_studio}


def render(model, root, local):
    from live.focus_base import document
    from live import studio_tabs
    from live.ui_parts import PB_CSS
    body = PB_CSS + studio_tabs.STYLE + '<style>' + (local / 'structure.css').read_text() + '\n' + tree_css()
    body += '</style><main id="labeling-structure-design" class="studio-master">'
    body += ''.join('<section class="sd-content" id="' + key + '"' + (' hidden' if key != 'folder-rules' else '') + '>' + html + '</section>'
                    for key, html in contents(model, root).items())
    # Only selects embedded content. Shared components own the trees and drawings.
    body += '''</main><script>(function(){function view(){var key=location.hash.slice(1)||'folder-rules';
document.querySelectorAll('#labeling-structure-design>.sd-content').forEach(function(p){p.hidden=p.id!==key;});
window.dispatchEvent(new Event('resize'));}window.addEventListener('hashchange',view);view();})();</script>'''
    return document(model['name'] + ' structure', body + studio_tabs.SCRIPT)



def type_helpers(root):
    scripts = root / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts'
    sys.path.insert(0, str(scripts))
    import block_types_check
    import block_types_pages
    return block_types_check, block_types_pages


def catalog_check(root, local, model):
    """Presence and evidence are mandatory; declared missing levels remain unresolved contracts."""
    checker, pages = type_helpers(root)
    topic = local.parent.parent / TOPICS[model['id']]
    path = topic / 'types.md'
    assert path.is_file(), f'Missing type catalog: {path}'
    text = path.read_text()
    example, types = checker.read_types(path)
    assert example == model['example_block']
    assert set(types) == set(checker.LEVELS), 'Each of the four levels must be declared'
    assert set(types['Task type']) == {t['type'] for t in model['tasks']}
    for level in checker.LEVELS:
        section = text.split('## ' + level + '\n', 1)[1].split('\n## ', 1)[0]
        if not types[level]:
            assert re.search(r'^absence: \S', section, re.M), level
            assert level != 'Task type', 'An empty catalog is not evidence of coverage'
            for key in ('for', 'holds', 'field', 'owner', 'source'):
                assert re.search(r'^' + key + r': \S', section, re.M), (level, key)
            for key in ('owner', 'source'):
                path = re.search(r'^' + key + r': (\S+)', section, re.M).group(1)
                assert (root / path).is_file(), (level, key, path)
    for task in model['tasks']:
        kind = task['type']
        about = types['Task type'][kind]
        assert about.get('for') and about.get('holds'), kind
        part = text.split('### ' + kind + '\n', 1)[1].split('\n### ', 1)[0]
        assert 'field: `task-type: ' + kind + '`' in part
        owner = task['owner_skill']
        assert (root / owner).is_file() and 'owner: ' + owner + '\n' in part
        assert any(s['path'] == owner for s in model['skills']), owner
        assert 'source: ' + owner + '\n' in part, ('source', kind)
        for proof in task['evidence']:
            assert 'evidence: ' + proof['path'] + ' — `' + proof['needle'] + '`' in part
            assert proof['needle'] in (root / proof['path']).read_text(), proof
    generated = pages.build(topic)
    for path, content in generated.items():
        if path.suffix != '.html':
            continue
        for href in re.findall(r'href="([^"]+)"', content):
            url = urlsplit(unescape(href))
            if url.path == '/_board/workbench':
                address = parse_qs(url.query).get('path', [''])[0]
                assert address and (root / address / 'board.md').is_file(), 'Type member must open its Block'
    return generated


def check(root, local, models):
    from live import studio_tabs, studio_views
    from live.studio_types import studio_types
    mm = map_module()
    assert mm.__file__.endswith('hai-mindmap/scripts/mmmap.py')
    assert mm.MV.__file__.endswith('hai-mindmap/scripts/mapview.py')
    shared_tree = tree_module()
    tree_source = root / 'examples/Project-Ladder/blueprint/b17_theme_work/delivery/structure/build_organization.py'
    assert Path(shared_tree.tree_html.__code__.co_filename).resolve() == tree_source.resolve()
    assert Path(shared_tree.node.__code__.co_filename).resolve() == tree_source.resolve()
    rows = []
    for model in models:
        topic = local.parent.parent / TOPICS[model['id']]
        views, parts = studio_views.read_views(topic, root)
        generated = catalog_check(root, local, model)
        for path, expected in generated.items():
            assert path.is_file() and path.read_text() == expected, f'Stale type content: {path}'
        manifest = json.loads((topic / 'studio-views.json').read_text())
        by_name = {v['name']: v['items'] for v in manifest['views']}
        assert [v[0] for v in views] == [v['name'] for v in manifest['views'] if v['items']]
        assert [(i['name'], i['path']) for i in by_name['Structure']] == [(i['name'], i['path']) for i in by_name['Draw']]
        assert [i.get('fragment') for i in by_name['Structure']] == ['folder-rules', 'jobs', 'studio']
        assert [i.get('fragment') for i in by_name['Draw']] == ['folder-rules', 'draw-jobs', 'draw-studio']
        assert [i['path'] for i in by_name['Skills']] == [s['path'] for s in model['skills']]
        assert [i['name'] for i in by_name['Task types']] == [t['type'] for t in model['tasks']]
        assert not by_name['Job types'], 'No independent Job Type contract is registered'
        for view in manifest['views']:
            assert len(parts.get(view['name'], [])) == len(view['items'])
            for item in view['items']:
                if 'block' in item:
                    assert (root / item['block'] / 'board.md').is_file()
                elif item.get('fragment'):
                    assert 'id="' + item['fragment'] + '"' in (root / item['path']).read_text()
        proofs = [*model['evidence'], *(p for t in model['tasks'] for p in t['evidence'])]
        for proof in proofs:
            assert proof['needle'] in (root / proof['path']).read_text(), proof
        for source in model['sources']:
            assert (root / source).is_file(), source
        assert (root / model['studio_type_source']).is_file()
        assert model['studio_band']['name'].startswith('〈')
        assert model['studio_band']['numbers'].startswith('〈')
        for path in model['studio_band']['sources']:
            assert (root / path).is_file()
        assert model['job_type'] is None, 'A new Job Type needs its own supporting contract'
        placeholders = [model['job_type_action'], model['job_naming']['label'],
                        *(t['naming']['label'] for t in model['tasks']), *(s['name'] for s in model['studio'])]
        assert all(x.startswith('〈') and x.endswith('〉') for x in placeholders)
        for example in model['studio_examples']:
            assert example['name'] in (root / example['path']).read_text()
        if model['id'] == 'guideline':
            assert [t['type'] for t in model['tasks']] == ['labeling-meaning', 'labeling-expression']
            for task in model['tasks']:
                assert task['name'] in (root / task['evidence'][0]['path']).read_text()
        if case := model.get('existing_example'):
            assert case['job_name'] in (root / case['job_path']).read_text()
            assert case['task_name'] in (root / case['task_path']).read_text()
            assert 'task-type: ' + case['task_type'] in (root / case['task_path']).read_text()
        tree = organization_tree(model)
        job = tree.root.children[0].children[0]
        assert len(job.children) == len({t['type'] for t in model['tasks']})
        content = (local / (model['id'] + '.html')).read_text()
        assert content == render(model, root, local), 'Regenerate shared component content'
        assert tree_css() in content, 'Use the shared folder-tree styles'
        sections = contents(model, root)
        for fragment in ('folder-rules', 'jobs', 'studio', 'examples'):
            assert '<ul class="tree">' in sections[fragment], fragment
            assert 'sd-map-frame' not in sections[fragment], 'Structure must use folder trees'
            assert '<details open>' not in sections[fragment], 'Structure trees start folded'
        for fragment in ('draw-jobs', 'draw-studio'):
            assert 'sd-map-frame' in sections[fragment], 'Draw keeps its shared drawing'
        for task in model['tasks']:
            assert task['type'] in sections['jobs'] and task['naming']['label'] in sections['jobs']
        assert mm.MV.CSS in content and mm.MV.FOLD in content
        assert '<details open>' not in content, 'Folder and example folds start closed'
        assert mm.MV.JS.replace(' contenteditable=plaintext-only', '') in content
        assert studio_tabs.SCRIPT in content and 'data-studio-src=' in content
        assert 'path=examples%2FProject-Ladder%2Flabeling%2F' in content
        for href in re.findall(r'data-studio-src="([^"]+)"', content):
            assert not re.search(r'path=[^&]*%2F[jt]\d\d', href), href
        assert 'contenteditable=plaintext-only' not in content
        assert 'sd-mm-' not in content and 'Fit to width' not in content
        assert model['job_name'] in content
        for task in model['tasks']:
            assert task['name'] in unescape(content) and task['type'] in content
        rows.append((topic, [], {}))
    assert not organization_tree(dict(models[0], tasks=[])).root.children[0].children[0].children
    first = models[0]['tasks'][0]
    repeated = dict(models[0], tasks=[first, dict(first, name='Another item construction', example_label='Other items')])
    job = organization_tree(repeated, concrete=True).root.children[0].children[0]
    assert len(job.children) == 1 and len(job.children[0].children) == 2
    blueprint = local.parent.parent
    bands = studio_types(root)
    assert studio_tabs.studio_bands(blueprint, root) == {d: f'{e} {n}'.strip() for d, (e, n, _) in bands.items()}
    rendered = studio_tabs.render(rows, root)
    expected_views = [view[0] for topic, _, _ in rows for view in studio_views.read_views(topic, root)[0]]
    assert re.findall(r'data-studio-view="\d+"[^>]*>([^<]+)</button>', rendered) == expected_views
    assert re.findall(r'<h2 id="studio-band-\d+">([^<]+)</h2>', rendered) == [f'{bands["0"][0]} {bands["0"][1]}']
    for topic in sorted(blueprint.glob('s4[12]-*')):
        rows.append((topic, [], {}))
    rendered = studio_tabs.render(rows, root)
    assert re.findall(r'<h2 id="studio-band-\d+">([^<]+)</h2>', rendered) == [f'{bands[d][0]} {bands[d][1]}' for d in ('0', '4')]
    print('Checked shared folder-tree Structure, separate Draw bindings, catalogs, type pages and source evidence.')
    print('Open contracts: independent Job types, actual Work Studio Bands, eval input adapter and executed split-Block examples.')


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    sys.path.insert(0, str(root / 'plugins/haipipe-toolkit/servers/_host'))
    from host_paths import bootstrap
    bootstrap()
    local = Path(__file__).resolve().parent
    models = json.loads((local / 'model.json').read_text())
    if args.check:
        check(root, local, models)
    else:
        for model in models:
            for path, text in catalog_check(root, local, model).items():
                if not path.is_file() or path.read_text() != text:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text)
            (local / (model['id'] + '.html')).write_text(render(model, root, local))


if __name__ == '__main__':
    main()
