"""Guard the semantic boundaries the user's real examples exercise."""
import json
import re
from pathlib import Path

import build_structure as build


def walk(tree):
    yield tree
    for child in tree['children']:
        yield from walk(child)


def check_pinned_questions(board):
    """A Board answer belongs to the exact question release its Job pins."""
    for job in board['jobs']:
        fields = build.front(build.ROOT / job['source'])
        release_dir = (build.ROOT / build.EXAMPLES).parent / fields['prototype']
        release = build.yaml.safe_load((release_dir / 'release.yaml').read_text())
        assert release['release'] == job['release'], job['name']
        answers = [task for task in job['tasks'] if task['key'] != 'prep']
        ids = [task['question'] for task in answers]
        assert len(ids) == len(set(ids)), f'Duplicate question: {job["name"]}'
        assert set(ids) == set(release['questions']), f'Release members: {job["name"]}'
        for task in answers:
            qid = task['question']
            question_path = (release_dir / release['questions'][qid]['task'] / 'question.md').resolve()
            question_path.relative_to(build.ROOT)
            question = build.front(question_path)
            assert question['id'] == qid, str(question_path)
            assert question['level'] == build.LEVELS[task['key']].lower(), task['source']


def check_generated_nodes(model, tree):
    """Verify source membership/ownership without treating authored nodes as generated."""
    nodes = list(build.MT.walk(tree.root))
    actual = {n.id: (n, parent) for n, parent, *_ in nodes}
    assert len(actual) == len(nodes), 'Duplicate map identity'
    for entry in build.grouped_organization(model):
        expected = build.map_node(entry, model['kind'])
        for node, parent, depth, _ in build.MT.walk(expected):
            assert node.id in actual, f'Missing source node: {node.id}'
            found, owner = actual[node.id]
            assert owner.id == (parent.id if parent else 'root'), node.id
            # Authored labels/notes are preserved; unchanged nodes retain their role.
            if not found.edited:
                role, _ = build.MM.split_role(found.text)
                assert role == build.ROLES[model['kind']][depth]


def check_authored_changes(model, tree):
    import copy
    old = copy.deepcopy(tree)
    leaf = next(n for n, *_ in build.MT.walk(old.root) if build.MM.split_role(n.text)[0] == 'Task')
    leaf.text += ' — revised by a person'
    leaf.note.append('A person added this note.')
    child = build.MT.Node('n_authored_check', 'A person added this branch',
                          [build.MT.Node('n_authored_detail', 'An explanation')])
    leaf.children.append(child)
    expected = build.MT.flat(old)
    build.MB.refresh(old, copy.deepcopy(tree))
    assert build.MT.flat(old) == expected, 'Authored words, notes or branches lost'
    check_generated_nodes(model, old)
    assert build.MT.flat(build.MT.parse(build.MT.dump(old))) == expected


def check_map_reparenting(models):
    """Removing generated wrappers must preserve identities even if their labels were edited."""
    import copy
    for kind in ('question-book', 'data-prep'):
        fresh = build.organization_mindmap(models[kind])
        old = copy.deepcopy(fresh)
        old.meta.pop('organization-levels', None)
        job = old.root.children[0]
        job.text = 'A person renamed this version'
        task = next(n for n, *_ in build.MT.walk(job) if build.MM.split_role(n.text)[0] == 'Task')
        task.note.append('Keep the evidence link and this note.')
        task.children.append(build.MT.Node('n_authored_leaf', 'A personal branch'))
        if kind == 'data-prep':
            step_wrapper = build.MB.built('step-wrapper', '[Task Type] Prep step', job.children)
            step_wrapper.note.append('An authored explanation on the removed wrapper')
            job.children = [step_wrapper]
        wrapper = build.MB.built('version-wrapper', '[Job Type] Version', old.root.children)
        wrapper.children.append(build.MT.Node('n_authored_root', 'A separate idea'))
        old.root.children = [wrapper]
        build.SC.align_map_levels(old, kind, fresh)
        build.MB.refresh(old, copy.deepcopy(fresh))
        check_generated_nodes(models[kind], old)
        actual = {n.id: n for n, *_ in build.MT.walk(old.root)}
        assert actual[job.id].text == 'A person renamed this version'
        assert actual[task.id].note[-1] == 'Keep the evidence link and this note.'
        assert 'n_authored_leaf' in actual and 'n_authored_root' in actual
        if kind == 'data-prep':
            assert actual[step_wrapper.id].note == step_wrapper.note
        expected = build.MT.flat(old)
        build.SC.align_map_levels(old, kind, fresh)
        build.MB.refresh(old, copy.deepcopy(fresh))
        assert build.MT.flat(old) == expected, 'A repeated refresh moved or duplicated authored content'


def check_map(model, html):
    roots = build.grouped_organization(model)
    board = model['kind'] == 'insight-board'
    assert len(roots) == (len({j['release'] for j in model['jobs']}) if board else len(model['jobs']))
    jobs = [c for root in roots for c in root['children']] if board else roots
    order = [j['source'] for j in model['jobs']]
    assert [job['path'] for job in jobs] == (order[::-1] if board else order)
    for root in roots:
        for parent in walk(root):
            assert len(parent['children']) == len({c['name'] for c in parent['children']})
    tree = build.organization_mindmap(model)
    check_generated_nodes(model, tree)
    assert build.MT.flat(build.MT.parse(build.MT.dump(tree))) == build.MT.flat(tree)
    assert 'class=pm-edit' in html and 'class="pm pm-folds"' in html
    assert 'data-foldall=1' in html and 'data-foldall=0' in html
    assert '<table>' not in html and '<select' not in html
    assert 'class="map-node"' not in html and 'data-map-fit' not in html
    # First-level Book/Prep cards show short words, retaining their shared source chips.
    from html import escape
    shown = build.shared_map(tree)
    for branch in tree.root.children:
        _, title = build.MM.split_role(branch.text)
        assert '>'+escape(build.MT.display(title))+'</b>' in shown
        for _, target in build.MM.LINK.findall(title):
            assert 'href="'+escape(target)+'"' in shown
    check_authored_changes(model, tree)


def check_catalog_guards(models):
    import copy
    import tempfile
    with tempfile.TemporaryDirectory(prefix='insight-catalog-') as tmp:
        topic = Path(tmp)
        def rejected(kind):
            try:
                build.SC.catalog(topic, kind)
            except (ValueError, FileNotFoundError):
                return
            raise AssertionError('Invalid or absent type catalog was accepted')
        rejected('insight-board')
        source = (build.BLOCK / build.CONFIG['question-book']['topic'] / 'types.md').read_text()
        (topic / 'types.md').write_text(source.replace('absent:', 'undocumented:', 1))
        rejected('question-book')
        (topic / 'types.md').write_text(source.replace('for:', 'missing:', 1))
        rejected('question-book')
        (topic / 'types.md').write_text(source.replace('owner:', 'missing:', 1))
        rejected('question-book')
    for kind, model in models.items():
        catalog = model['catalog']
        assert set(catalog['absent']) == build.SC.ABSENT[kind]
        assert len(catalog['types']['Job type']) == 1
        for job in model['jobs']:
            build.SC.classified(job, kind, catalog)
        bad = copy.deepcopy(model['jobs'][0])
        bad['tasks'][0]['type'] = 'A version is not a Task type'
        try:
            build.SC.classified(bad, kind, catalog)
        except ValueError:
            pass
        else:
            raise AssertionError('Unlisted semantic type accepted')


def check_studios(model):
    # Every real topic retains its owner and actual configured/tag grouping; no proposal is inserted.
    def lineage(tree, path, parents=()):
        if tree['path'] == path:
            return parents
        for child in tree['children']:
            found = lineage(child, path, parents + (tree,))
            if found is not None:
                return found
        return None
    for studio in model['studios']:
        parents = lineage(model['studio_tree'], studio['source'])
        assert parents[-1]['name'] == studio['band']
        assert parents[-2]['name'] in {Path(studio['owner']).name, model['name']}
        assert build.SC.actual_studio_band(build.ROOT/studio['owner'], build.ROOT/studio['source']) == studio['band']
    tree, notes = build.SC.studio_rule(model['kind'], model['name'], build.r)
    bands = build.SC.ordinary_bands()
    for (key, label), (name, children) in zip(build.SC.STUDIO_BANDS, tree[1]):
        lo, hi = bands[key]
        assert f's{lo:02d}–s{hi:02d}' in name
        assert children[0][0].startswith('〈') and children[0][0].endswith('〉')
        assert notes[name] and notes[children[0][0]]
    assert not any(n['role'].startswith('Propos') for n in walk(model['studio_tree']))
    for node in walk(model['studio_tree']):
        if node['role']=='Job':
            pins = re.findall(r'data-v\d+', node['name'])
            assert all(pin in build.short_name(node) for pin in pins), node['name']


def check_structure_trees(model, manifest, html):
    """Check the content actually selected by Structure, independently of Draw."""
    view = next(v for v in manifest['views'] if v['name']=='Structure')
    assert {i['fragment'] for i in view['items']}=={'folder-rules','jobs-rules','studio-rules'}
    for item in view['items']:
        fragment = item['fragment']
        match = re.search(r'<section id="'+re.escape(fragment)+r'"[^>]*>(.*?)</section>', html, re.S)
        assert match, fragment
        content = match[1]
        assert 'data-structure-shape="folder-tree"' in content, fragment
        assert '<details' in content and '<summary' in content and '<ul' in content, fragment
        assert not re.search(r'pm-node|pm-foldbar|class="shared-map"|<svg', content), 'Structure must use Folder Tree: '+fragment
    # The source-backed example has every Task, including references kept by a release.
    jobs = re.search(r'<section id="jobs-rules"[^>]*>(.*?)</section>',html,re.S)[1]
    from html import escape
    for n, *_ in build.MT.walk(build.organization_mindmap(model).root):
        assert f'data-source-id="{escape(n.id,quote=True)}"' in jobs
    draw = next(v for v in manifest['views'] if v['name']=='Draw')
    assert all(i.get('fragment') not in {'folder-rules','jobs-rules','studio-rules'} for i in draw['items'])


def check_tree_rejection(model, manifest, html):
    import copy
    bad = re.sub(r'(<section id="jobs-rules"[^>]*>).*?(</section>)',
                 lambda m:m[1]+build.rule_map(model,'jobs')+m[2], html, count=1, flags=re.S)
    cases = [(manifest, bad)]
    wrong_view = copy.deepcopy(manifest)
    next(v for v in wrong_view['views'] if v['name']=='Structure')['items'][1]['fragment']='jobs-map'
    cases.append((wrong_view, html))
    for views, content in cases:
        try:
            check_structure_trees(model, views, content)
        except AssertionError:
            continue
        raise AssertionError('Mindmap content or binding was accepted as Structure')


def check():
    models={k:build.load_model(k) for k in build.CONFIG}
    board,book,prep=(models[k] for k in ('insight-board','question-book','data-prep'))
    check_catalog_guards(models)
    check_map_reparenting(models)
    for model in models.values():
        assert build.front(build.ROOT/model['path']/'board.md')['board-kind']==model['board_kind']
    check_pinned_questions(board)
    assert len({j['type'] for j in board['jobs']})==1
    assert len({m['job_type'] for m in models.values()})==3
    version=next(j for j in book['jobs'] if j['release']=='question-v2')
    assert len(version['tasks'])==9 and sum(t['kept'] for t in version['tasks'])==8
    assert {t['question'] for t in version['tasks']}=={'D01','D02','I01','I02','K01','K02','W01','X01','X02'}
    assert not any(j['release']=='question-v2' for j in board['jobs'])
    steps=prep['jobs'][0]['tasks']
    assert [t['name'] for t in steps]==['t01_experiment','t02_source','t03_prepare']
    assert {t['type'] for t in steps}=={'Prep step'} and not any(t['group_type'] for t in steps)
    assert all(not (build.ROOT/t['path']/'runs').exists() for t in steps)
    prepared=next(j for j in board['jobs'] if j['prep'])
    assert prepared['tasks'][0]['type']=='Preparation execution'
    assert {t['type'] for j in book['jobs'] for t in j['tasks']}=={'Question definition'}
    assert {t['type'] for j in board['jobs'] for t in j['tasks'] if t['key']!='prep'}=={'Question answer'}
    outcome=next(t for t in prepared['tasks'] if t.get('question')=='I01')
    assert outcome['runs']==['r01_full','r02_first','r03_second','r05_third']
    assert len(list((build.ROOT/prepared['tasks'][0]['path']/'runs').glob('r[0-9][0-9]_*')))==1
    for kind,m in models.items():
        for job,tree in zip(m['jobs'],m['organization']):
            nodes=list(walk(tree))
            assert {n['role'] for n in nodes}==set(build.ROLES[kind])
            assert {n['path'] for n in nodes if n['role']=='Task'}=={t['source'] for t in job['tasks']}
            assert not any(n['role']=='Run' for n in nodes), 'Runs belong in Task detail, not another organization level'
            for task in job['tasks']:
                assert (build.ROOT/task['source']).is_file(),task['source']
                if task.get('runs'):
                    node=next(n for n in nodes if n['path']==task['source'])
                    assert all(r in ' '.join(node['notes']) for r in task['runs'])
        assert all((build.ROOT/n['path']).exists() for n in walk(m['folder']))
        check_studios(m)
        manifest=build.manifest(kind)
        type_views=build.SC.views(build.BLOCK/m['topic'])
        assert manifest['views'][1:3]==type_views
        assert [v['name'] for v in manifest['views'] if v['name'] not in build.SC.type_pages.VIEWS]==['Structure','Draw','Skills']
        for view in manifest['views']:
            assert view['items'], 'No empty type view'
            for item in view['items']:
                p=build.ROOT/item.get('block',item.get('path'))
                assert (p/'board.md').is_file() if 'block' in item else p.is_file(),str(p)
        html=(build.HERE/(kind+'.html')).read_text()
        check_map(m,html)
        check_structure_trees(m,manifest,html)
        check_tree_rejection(m,manifest,html)
        rule=build.RULES[kind]
        assert len(rule['headings'])==len(build.ROLES[kind])
        for key in ('folder','jobs','studio'):
            assert f'id="{key}-rules"' in html
            rule_html=build.model_tree(build.rule_model(m,key))
            assert 'examples/Project-Ladder/insight/' not in rule_html
            assert 'data-structure-shape="folder-tree"' in rule_html
            assert (f'data-example="{key}"' in html)==(key!='studio' or bool(m['studios']))
        assert 'class=open-dot' in html and '%2F'+build.CONFIG[kind]['example'] in html
        payload=re.search(r'id="structure-model">(.*?)</script>',html,re.S).group(1)
        assert json.loads(payload)==m
        assert not re.search(r'[\u4e00-\u9fff]',re.sub(r'/\*.*?\*/','',html,flags=re.S))
        assert not re.search(r'(Job topic|Task topic|Studio topic|Example) [1-9]',html)
    assert not prep['studios']
    empty = build.organization({'name':'empty','type':'Prep-code version','source':'test.md','tasks':[]},'data-prep')
    assert empty['role']=='Job' and not empty['children']
    # Folder contracts must not give code steps execution or fictitious faces.
    def rules(tree):
        yield tree
        for child in tree[1]:
            yield from rules(child)
    prep_step=next(n for n in rules(build.RULES['data-prep']['folder']) if n[0]=='tNN_〈step〉/')
    assert {n[0] for n in prep_step[1]}=={'step.md','scripts/'}
    book_question=next(n for n in rules(build.RULES['question-book']['folder']) if n[0]=='tNN_〈L〉NN_〈question〉/')
    assert 'tNN_〈task〉.md' not in {n[0] for n in book_question[1]}
    for path,expected in build.generated_files().items():
        assert path.read_text()==expected,f'Stale: {build.relative(path)}'
    js=(build.HERE/'structure.js').read_text()
    assert 'createElementNS' not in js and 'sizeMap' not in js
    assert 'requestAnimationFrame(window.pmDraw)' in js
    assert not re.search(r'^bands:',(build.BLOCK/'board.md').read_text(),re.M)
    for cfg in build.CONFIG.values():
        topic=build.BLOCK/cfg['topic']
        assert 's71-studio-type-block-structure' in (topic/(topic.name+'.md')).read_text()
    assert 's76-studio-type-theme-guide' in (build.BLOCK/'s99-guide/s99-guide.md').read_text()
    contract_files=['workbench-insight/SKILL.md','workbench-insight/CONSTITUTION.md',
                    'workbench-insight/ref/block-structure.md','hai-insight/SKILL.md',
                    'hai-insight/ref/insight-ladder.md','hai-insight/ref/dataprep.md',
                    'hai-insight-workflow/SKILL.md','folder-kinds/hai-insight-question/SKILL.md']
    for rel in contract_files:
        text=(build.ROOT/build.SKILLS/rel).read_text()
        body=text.split('---',2)[-1] if text.startswith('---\n') else text
        assert not re.search(r'\blegacy\b|six[- ]Spaces|older (?:layout|board)|retired page|\bpreviously\b',body,re.I),rel
        assert len(text.splitlines())<700,rel
    print('PASS: catalogs, ownership, valid absence, Structure Folder Trees, mindmap rejection, separate Draw and generation')


if __name__=='__main__':
    check()
