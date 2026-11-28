"""Guard the authored structure content, destinations and retained history."""
import hashlib
import sys
from html import escape
import json
import re
from pathlib import Path
from build_organization import BLUEPRINT_BANDS, HERE, KINDS, LABELS, job_tree, studio_tree, folder_tree, SOURCES, render, organization_rows, organization_map
from build_organization import node, organization_document, MAP_SCRIPT
from build_organization import example_maps, rule_jobs, rule_folder, rule_sections, organization_model, shared_mindmap, source_url

ROOT = HERE.parents[5]
BLOCK = HERE.parent.parent
TOPICS = ('s01-work-structure', 's02-blueprint-structure', 's03-cowork-structure',
          's04-discovery-structure')
TITLES = ('Work', 'Blueprint', 'CoWork', 'Discovery')   # sNN · Block Structure: <title>


def check():
    # External themes supply their own trees; identical names in distinct type
    # branches must still link to the correct records, without mutable globals.
    tree = node('Block', node('Type A', node('Shared name')),
                node('Type B', node('Shared name', node('Task kind', node('<Draft>')))))
    records = organization_rows('work')
    sources = {('Type A', 'Shared name'): (records[0][4], ''),
               ('Type B', 'Shared name'): (records[-1][4], ''),
               ('Type B', 'Shared name', 'Task kind', '<Draft>'): (records[-1][5], '')}
    diagram = organization_map(tree=tree, sources=sources)
    model = organization_model(tree=tree, sources=sources)
    assert len(list(shared_mindmap().MT.walk(model.root))) == 7
    assert shared_mindmap().MV.CSS in diagram and shared_mindmap().MV.JS.replace(' contenteditable=plaintext-only', '') in diagram
    assert diagram.count('<a ') == 3
    assert 'j01_first_cli' in diagram and 'j11_core_checks' in diagram
    assert '&lt;Draft&gt;' in diagram and '<Draft>' not in diagram
    document = organization_document('<Organization>', tree=tree, sources=sources)
    assert diagram in document and shared_mindmap().MV.JS.replace(' contenteditable=plaintext-only', '') in document
    assert '<title>&lt;Organization&gt;</title>' in document
    for kwargs in ({}, {'kind': 'work', 'tree': tree},
                   {'tree': node('Block', node('A', node('B', node('C', node('D', node('E'))))))}):
        try:
            organization_map(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid organization input was accepted')
    trace = (BLOCK / 'trace/261127/1021_structure_folder_organization.md').read_text()
    hashes = json.loads(re.search(r'```json\n(.*?)\n```', trace, re.S)[1])
    for path, digest in hashes.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    for topic, kind, title in zip(TOPICS, KINDS, TITLES):
        folder = BLOCK / topic
        face = (folder / f'{topic}.md').read_text()
        assert face.splitlines()[0] == f'{topic[:3]} · Block Structure: {title}'
        manifest = json.loads((folder / 'studio-views.json').read_text())
        views = manifest['views']
        sys.path.insert(0, str(ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts'))
        sys.path.insert(0, str(ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/gallery/block-structure/scripts'))
        sys.path.insert(0, str(ROOT / 'plugins/haipipe-toolkit/servers/_host'))
        if manifest.get('check_type'):
            from check_views import build as check_build
            assert all(p.read_text() == text for p, text in check_build(folder).items()), 'stale Check view'
            views = [v for v in views if v['name'] != 'Check']
        typed = [v for v in views if v['name'] in ('Job types', 'Task types')]   # an instance with its types.md pinned
        views = [v for v in views if v not in typed]
        # an instance follows its type (s71): Structure drawn from the topic's own structure.md, no Examples view
        assert [v['name'] for v in views] == ['Structure', 'Draw', 'Skills']
        assert len(typed) in (1, 2) and (folder / 'types.md').is_file()   # Task types only when the type has Tasks
        draw = views[1]['items']                         # Draw is the topic's one Excalidraw drawing, no tabs
        assert len(draw) == 1 and draw[0]['path'].endswith(f'/{topic}/{topic}.excalidraw') and (ROOT / draw[0]['path']).is_file(), draw
        assert tuple(r['name'] for r in views[0]['items']) == LABELS
        for row in views[0]['items']:
            assert (ROOT / row['path']).is_file(), row
            assert row['path'].endswith(f'/{topic}/delivery/structure.html'), row
            assert row['fragment'] in ('folder-rules', 'jobs-rules', 'studio-rules')
        from block_structure_page import build as structure_build
        assert all(p.read_text() == text for p, text in structure_build(folder).items()), 'stale Structure page'
        for row in views[2]['items']:
            assert (ROOT / row['path']).is_file(), row
        assert (folder / 'result/structure-replaced-261127.md').is_file()
        html = (HERE / f'{kind}-organization.html').read_text()
        # Other sessions may add source files while this task preserves Folder verbatim.
        # Reproducibility applies to the organization we changed; Folder has its own
        # preserved-section hash and actual-path checks below.
        without_folder = lambda value: re.sub(r'<section id="folder".*?</section>', '', value, flags=re.S)
        assert without_folder(html) == without_folder(render(kind)), f'{kind}: regenerate stale organization'
        assert all(f'id="{key}"' in html for key in ('folder', 'jobs', 'studio'))
        for key in ('jobs', 'studio'):
            section = re.search(f'<section id="{key}".*?</section>', html, re.S)[0]
            assert '<h1>' not in section and 'class="records"' not in section
            assert 'class="role"' not in section and 'compact-tree' not in section
        assert 'pm-folds' in re.search(r'<section id="studio".*?</section>', html, re.S)[0]
        assert not re.search(r'(?:href|src)=[\"\']https?://', html)
        rules = rule_sections(kind)
        assert 'Fixed name' in rules and '〈Name for this work〉' in rules
        assert all(f'id="{key}-rules"' in rules for key in ('folder', 'jobs', 'studio'))
        assert '<select' not in rules
        assert all(sample not in rules for sample in ('j01_first_cli', 'First command line', 'Read CSV', 'Tool implementation'))
        tree, headings = rule_jobs(kind)
        assert 'Job Type' not in headings, 'An authored group is not a declared type'
        if kind == 'cowork':
            assert 'j00_people' in repr(tree) and '〈Request or coordination job〉' in repr(tree)
            assert all('Task' not in h for h in headings)
            assert 'tNN_' not in repr(rule_folder(kind))
        if kind == 'discovery':
            assert len(headings) == 2 and 'Job / inquiry group' in headings
        if kind == 'blueprint':
            assert all(band in rules for band in ('Block Structure', 'Block Job UI Preview', 'Skills', 'UI Plugin', 'Guide'))
        else:
            assert '<ul class="tree">' in rules and '〈' in rules
    cowork_contract = (ROOT / 'plugins/haipipe-toolkit/skills/2_work/cowork/hai-cowork/SKILL.md').read_text()
    assert '`j00_people` is always first' in cowork_contract and 'There is no `tNN` level' in cowork_contract
    for kind in KINDS:
        source = ROOT / SOURCES[kind]
        tree = folder_tree(kind)
        assert tree[0] == source.name + '/'
        def check_existing(entry, parent):
            label, children = entry
            path = parent / label.rstrip('/')
            assert path.exists(), f'Invented folder or file: {path}'
            assert label.endswith('/') == path.is_dir(), path
            for child in children:
                check_existing(child, path)
        check_existing(tree, source.parent)
        assert all(label not in repr(tree) for label in ('Job topic 1/', 'Task topic 1/', 'sNN-topic/'))
    for kind in KINDS:
        jobs, studios = repr(job_tree(kind)), repr(studio_tree(kind))
        for retired in ('Owning level', 'Job topic 1', 'Task topic 1', 'Studio topic 1', 'Studio group 1'):
            assert retired not in jobs + studios, (kind, retired)
        assert job_tree(kind)[0] == studio_tree(kind)[0], kind
    assert [x[0] for x in studio_tree('blueprint')[1]] == [f'{band} · {nn}' for band, nn, _ in BLUEPRINT_BANDS] and BLUEPRINT_BANDS
    assert [x[0] for x in studio_tree('work')[1]] == ['What the tool checks', 'HTML report layout']
    assert len({repr(job_tree(k)) for k in KINDS}) == 4
    for kind in KINDS:
        diagram = organization_map(kind)
        examples = example_maps(kind)
        jobs = {(row[0], row[1]) for row in organization_rows(kind)}
        assert examples.count('<option ') == len(jobs)
        assert examples.count('class="example-panel"') == len(jobs)
        assert len(re.findall(r'data-example="\d+" hidden', examples)) == len(jobs) - 1
        assert 'data-example="0"><style' in examples
        assert 'pm-folds' in examples and 'data-foldall=1' in examples
        assert 'compact-tree' not in examples
        assert '<table' not in examples
        for _, name in jobs:
            assert escape(name) in examples
        for column in ('Job Type', 'Job Name', 'Task Type', 'Task Name'):
            assert column in diagram
        assert '<table' not in diagram and '<tr' not in diagram
        assert 'pm-wires' in diagram and 'pm-folds' in diagram
        assert 'data-foldall=1' in diagram and 'data-foldall=0' in diagram
        assert 'map-edges' not in diagram and 'contenteditable=plaintext-only' not in diagram
        # Each parent occurs once; connectors equal nodes minus top-level roots.
        expected_nodes = []
        def count_nodes(entry):
            expected_nodes.append(entry)
            for child in entry[1]:
                count_nodes(child)
        for branch in job_tree(kind)[1]:
            count_nodes(branch)
        model = organization_model(kind)
        assert len(list(shared_mindmap().MT.walk(model.root))) - 1 == len(expected_nodes)
        for jkind, jname, tkind, tname, jface, tface, *_ in organization_rows(kind):
            assert jface.is_file()
            assert 'section=jobs' in source_url(jface) and 'layout=focus' in source_url(jface)
            assert 'group=' + jface.parent.name[:3] in source_url(jface)
            assert jface.parent.name not in source_url(jface)
            if tface:
                assert 'task=' + tface.parent.name[:3] in source_url(tface)
            if tface:
                assert tface.is_file()
                assert tface.parent.parent == jface.parent, 'Task must belong to the named Job'
                assert tkind != '—' and tname != '—'
            else:
                assert tkind == tname == '—'
            assert not re.fullmatch(r'(Job|Task|Example) [0-9]+(?: name)?', jname)
            assert not re.fullmatch(r'(Job|Task|Example) [0-9]+(?: name)?', tname)
            assert tname == '—' or tname in repr(job_tree(kind))
            assert jname in repr(job_tree(kind))
        assert 'Example 1' not in repr(job_tree(kind))
    assert 'Read CSV' in repr(job_tree('work'))
    assert 'Board page' in repr(job_tree('blueprint'))
    assert 'Data-use plan' in repr(job_tree('cowork'))
    assert 'Contract mismatch' in (HERE / 'cowork-organization.html').read_text()
    discovery = organization_rows('discovery')
    assert 'discovery_type: topic-summary' in discovery[0][-1]
    assert 'discovery_type: source-map' in discovery[1][-1]
    previous = (BLOCK / 'trace/261127/1048_organization_by_block_type.md').read_text()
    folder_hashes = json.loads(re.search(r'```json\n(.*?)\n```', previous, re.S)[1])
    for kind, digest in folder_hashes.items():
        html = (HERE / f'{kind}-organization.html').read_text()
        folder = re.search(r'<section id="folder".*?</section>', html, re.S)[0]
        assert hashlib.sha256(folder.encode()).hexdigest() == digest, f'{kind}: Folder changed'
    print('PASS: four models, three content views, grouping boundaries, existing folder paths, destinations, retained history and reproducible output.')


if __name__ == '__main__':
    check()
