"""Insight content for the shared Studio; read example metadata, never patient records."""
import argparse
import hashlib
import json
import re
import sys
from html import escape
from pathlib import Path
from urllib.parse import quote, urlencode

import yaml

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'PRINCIPLE.md').is_file())
MAP_SCRIPTS = ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-mindmap/scripts'
sys.path.insert(0, str(MAP_SCRIPTS))
import mmtree as MT
import mmbuild as MB
import mmmap as MM
sys.path.insert(0, str(ROOT / 'plugins/haipipe-toolkit/servers/_host'))
from live.ui_parts import open_dot, PB_CSS
import structure_contracts as SC
BLOCK = HERE.parent.parent
SKILLS = 'plugins/haipipe-toolkit/skills/3_theme/insight/'
CONTRACT = SKILLS + 'hai-insight/ref/'
EXAMPLES = 'examples/Project-Ladder/insight/'
LEVELS = {'D': 'Data', 'I': 'Information', 'K': 'Knowledge', 'W': 'Wisdom', 'X': 'Executive'}
ROLES = {'insight-board': ('Job group', 'Job', 'Task group', 'Task'),
         'question-book': ('Job', 'Task group', 'Task'),
         'data-prep': ('Job', 'Task')}
CONFIG = {
    'insight-board': dict(name='Insight Board', example='Insight-Example', topic='s01-insight-board-structure',
        board_kind='insight-board', job_type='Analysis',
        groups='Jobs group by the question version they pin; Tasks group as Prep, then Data, Information, Knowledge, Wisdom and Executive; each answer Task holds one Run per segment. Groups add no folders.',
        gap='The live Jobs page still groups the prep Task by number; the name Prep is not in its navigation yet.',
        proposal=['Block · Research frame', 'Job · This round of analysis', 'Task · Evidence and reading', 'Block · From insight to design'],
        skills=['hai-insight', 'hai-insight-workflow', 'workbench-insight']),
    'question-book': dict(name='Question Book', example='InsightQuestionBook-Example', topic='s02-question-book-structure',
        board_kind='prototype', job_type='Question-set version',
        groups='Each Job is a question-set version, without a repeated version group; Tasks group by DIKWX.',
        gap='The live Jobs page lists only local Tasks, so it misses questions release.yaml keeps from an earlier version; this structure resolves every member.',
        proposal=['Block · Question map', 'Block · How the questions change', 'Job · Version upgrade', 'Task · Asking and method'],
        skills=['hai-insight', 'hai-insight-question', 'workbench-insight']),
    'data-prep': dict(name='DataPrep', example='InsightDataPrep-Example', topic='s03-dataprep-structure',
        board_kind='insight-dataprep', job_type='Prep-code version',
        groups='Each Job is a prep-code version; steps are ordered directly without a Task group.',
        gap='The live Jobs page still groups by number. experiment, source and prepare are step names, not three Task types.',
        proposal=['Block · Data conventions', 'Block · Prep chain', 'Job · Prep version', 'Task · Step interface'],
        skills=['hai-insight', 'hai-insight-workflow', 'workbench-insight']),
}


def relative(path):
    return str(path.resolve().relative_to(ROOT))


def front(path):
    text = path.read_text(encoding='utf-8')
    if text.startswith('---\n'):
        return yaml.safe_load(text.split('---', 2)[1]) or {}
    return {}


def node(name, role='', children=None, path=''):
    return dict(name=name, role=role, children=children or [], path=path)


def folder(path):
    children = []
    if path.is_dir() and not path.is_symlink():
        for child in sorted(path.iterdir()):
            if child.name.startswith('.') or child.name in {'__pycache__', 'node_modules'}:
                continue
            children.append(folder(child))
    return node(path.name + ('/' if path.is_dir() else ''), 'Folder' if path.is_dir() else 'File', children, relative(path))


def runs_of(task):
    """A Board answer Task's Runs: one per segment (rNN_<segment>), plus cross; soft and collect Runs are not shown."""
    runs = task / 'runs'
    return [r.name for r in sorted(runs.iterdir()) if r.is_dir() and re.match(r'^r\d+_', r.name)
            and '_collect' not in r.name] if runs.is_dir() else []


def task_record(task, kind, question=None, kept=False):
    if kind == 'data-prep':
        source = task / 'step.md'
        fields = front(source)
        return dict(name=task.name, type='Prep step', key='step', group='', group_type='', identity_group='Prep step',
                    purpose=fields.get('goal', ''), path=relative(task), source=relative(source), kept=False)
    prep = re.match(r'^t\d+_prep-v\d+', task.name)
    if prep:
        source = task / (task.name + '.md')
        return dict(name=task.name, type='Preparation execution', key='prep', runs=runs_of(task),
                    group='Preparation', group_type='Preparation', identity_group='Prep',
                    purpose=front(source).get('goal', ''), path=relative(task), source=relative(source), kept=False)
    match = re.match(r'^t\d+_([DIKWX])\d+_', task.name)
    if not match:
        raise ValueError(f'Unclassified Task: {task}')
    letter = match.group(1)
    english = LEVELS[letter]
    source = task / ('question.md' if kind == 'question-book' else task.name + '.md')
    fields = front(source)
    if kind == 'question-book' and fields.get('level') != english.lower():
        raise ValueError(f'Folder and question level disagree: {source}')
    if kind == 'question-book' and fields.get('id') != question:
        raise ValueError(f'Release member and source question ID disagree: {source}')
    kind_name = 'Question definition' if kind == 'question-book' else 'Question answer'
    return dict(name=task.name, type=kind_name, key=letter, runs=runs_of(task) if kind == 'insight-board' else [],
                group=english, group_type='Question level',
                identity_group=f'{english} question' if kind == 'question-book' else english,
                purpose=fields.get('ask') or fields.get('goal') or fields.get('question', ''),
                path=relative(task), source=relative(source), kept=kept, question=question or fields.get('question'))


def job_record(job, kind):
    source = job / (job.name + '.md')
    fields = front(source)
    if kind == 'question-book':
        release = yaml.safe_load((job / 'release.yaml').read_text())
        tasks = []
        for qid, member in release['questions'].items():
            task = (job / member['task']).resolve()
            task.relative_to(ROOT)
            tasks.append(task_record(task, kind, qid, task.parent != job))
    else:
        tasks = [task_record(t, kind) for t in sorted(job.iterdir())
                 if t.is_dir() and re.match(r'^t\d+_', t.name)]
    return dict(name=job.name, type=CONFIG[kind]['job_type'], path=relative(job), source=relative(source),
                purpose=fields.get('goal', ''), release=fields.get('release'), prep=fields.get('prep'),
                data=fields.get('data'), tasks=tasks)


def organization(job, kind=''):
    return SC.organization(job, kind, node)


def load_model(kind):
    cfg = CONFIG[kind]
    example = ROOT / EXAMPLES / cfg['example']
    jobs = [job_record(j, kind) for j in sorted(example.iterdir())
            if j.is_dir() and re.match(r'^j\d+_', j.name)]
    catalog = SC.catalog(BLOCK / cfg['topic'], kind)
    if catalog['example'] != relative(example):
        raise ValueError(f'{kind}: catalog and example disagree')
    for job in jobs:
        SC.classified(job, kind, catalog)
    studios = []
    for path in sorted(example.rglob('s[0-9][0-9]-*')):
        source = path / (path.name + '.md')
        if path.is_dir() and source.is_file():
            studios.append(dict(name=path.name, owner=relative(path.parent), source=relative(source),
                                band=SC.actual_studio_band(path.parent, source)))
    studio_tree = node(cfg['name'], 'Block')
    owners = {relative(example): studio_tree}
    for s in studios:
        owner = ROOT / s['owner']
        chain = list(reversed([owner]+list(owner.parents)[:len(owner.relative_to(example).parts)-1])) if owner != example else []
        parent = studio_tree
        for scope in chain:
            key = relative(scope)
            if key not in owners:
                owners[key] = node(scope.name, 'Job' if scope.name.startswith('j') else 'Task')
                parent['children'].append(owners[key])
            parent = owners[key]
        band = next((c for c in parent['children'] if c['role']=='Band' and c['name']==s['band']), None)
        if band is None:
            band = node(s['band'], 'Band')
            parent['children'].append(band)
        band['children'].append(node(s['name'], 'Studio', path=s['source']))
    return dict(kind=kind, **cfg, path=relative(example), jobs=jobs, folder=folder(example),
                studios=studios, studio_tree=studio_tree, catalog=catalog,
                organization=[organization(j, kind) for j in jobs],
                sources=[CONTRACT+'insight-ladder.md', CONTRACT+'dataprep.md',
                         SKILLS+'workbench-insight/ref/block-structure.md'])


NAMING = 'Fixed name · 〈Name for this work〉'
PURPOSE = {   # each rule line's hover: what that folder or file is for
    'board.md': "the Block's face: its goal, Jobs and Studio topics",
    'data/': 'optional local data inputs; version locations are declared in board.md',
    'jNN_data-vM_prep-vK_question-vN/': 'a Job: one question version run on one data version, prepared by one prep version',
    'jNN_question-vN_〈slug〉/': 'a Job: one question version of the Book',
    'jNN_prep-vK_〈slug〉/': 'a Job: one version of the prep code',
    'jNN_〈job〉.md': "the Job's face: its versions, goal and Tasks in order",
    'release.yaml': 'the questions this version holds, kept ones pointing to the Task that first asked them',
    'partitions.md': 'the segments every answer is cut by',
    'tNN_prep-vK_〈slug〉/': 'the prep Task: one Run builds the ready folder this Job answers from',
    'tNN_〈L〉NN_〈question〉/': 'a Task: one question at one level (D, I, K, W or X)',
    'tNN_〈step〉/': 'a Task: one step of the prep chain, in order',
    'tNN_〈task〉.md': "the Task's face: its question or goal and state",
    'question.md': 'the question, its level and the method an answer uses',
    'step.md': 'the step: what it reads, what it writes, its checks',
    'scripts/': 'the question script or prep step implementation',
    'runs/': 'operations at this scope; execution evidence belongs to Board Tasks',
    'rNN_〈segment〉/': 'one Run: the question answered on one segment',
    'rNN_cross/': 'the Run that reads across the segments',
    'r01_〈run〉/': 'the one Run that builds the ready folder',
    'sNN-〈topic〉/': 'a Studio topic: a drawing or design to talk through',
    'trace/': 'a record of each change, by day',
    'related/': 'what came in from outside; made when first needed',
    'delivery/': 'what the Block hands out; made when first needed',
}


PURPOSE.update({
    'meta/': 'dataset descriptions and provenance, no individual rows on pages',
    'meta.md': 'metadata for the dataset and its versions',
    'reports/': 'readings and comparisons across the owned work',
    'background/': 'source documents and answers that explain the preparation',
    'proposals/': 'new questions, changes, retirements and segment proposals',
    'thresholds.yaml': 'predeclared floors, thresholds and seeds',
    'src/': 'shared question or preparation code, pinned with its version',
    '〈script〉.py': 'the declared entry script; a prep step exposes run(ctx)',
    'jNN_question-vN-〈slug〉_data-vM/': 'a Job using prepared data directly, without a prep-version pin',
    't01_prep-vK_〈slug〉/': 'present when the Job uses DataPrep; executes the whole chain in one Run',
})


def r(label, *children):
    return (label, children)


# one Task group per question level, each with its own Task name pattern (tNN D01 〈question〉 …)
LEVEL_GROUPS = tuple(r(name, r(f'tNN {letter}NN 〈question〉')) for letter, name in LEVELS.items())
TAIL = (r('sNN-〈topic〉/'), r('trace/'), r('related/'), r('delivery/'))
RULES = {
    'insight-board': dict(
        folder=r('Insight-〈dataset〉/', r('board.md'), r('data/'), r('meta/', r('meta.md')), r('reports/'), r('runs/'),
                 r('jNN_question-vN-〈slug〉_data-vM/', r('jNN_〈job〉.md'), r('reports/'), r('runs/'),
                   r('tNN_〈L〉NN_〈question〉/', r('tNN_〈task〉.md'), r('runs/', r('rNN_〈segment〉/'), r('rNN_cross/')))),
                 r('jNN_data-vM_prep-vK_question-vN/', r('jNN_〈job〉.md'), r('reports/'), r('runs/'),
                   r('t01_prep-vK_〈slug〉/', r('tNN_〈task〉.md'), r('runs/', r('r01_〈run〉/'))),
                   r('tNN_〈L〉NN_〈question〉/', r('tNN_〈task〉.md'), r('runs/', r('rNN_〈segment〉/'), r('rNN_cross/')))),
                 *TAIL),
        headings=('Job group', 'Job name', 'Task group', 'Task name'),
        jobs=r('〈question-vN〉', r('jNN · 〈data-vM〉 · 〈prep-vK〉', r('Preparation', r('t01 〈prep-vK〉')), *LEVEL_GROUPS)),
        notes={**{f'tNN {k}NN 〈question〉': 'Runs: rNN_〈segment〉, one per required segment, plus cross where asked' for k in LEVELS},
               'Preparation': 'Group type: Preparation; present only when the Job pins DataPrep',
               't01 〈prep-vK〉': 'Type: Preparation execution. Runs: r01, the whole chain builds the ready folder'}),
    'question-book': dict(
        folder=r('InsightQuestionBook-〈topic〉/', r('board.md'), r('proposals/'), r('runs/'),
                 r('jNN_question-vN_〈slug〉/', r('jNN_〈job〉.md'), r('release.yaml'), r('partitions.md'),
                   r('thresholds.yaml'), r('src/'), r('runs/'),
                   r('tNN_〈L〉NN_〈question〉/', r('question.md'), r('scripts/', r('〈script〉.py')), r('runs/'))), *TAIL),
        headings=('Job name', 'Task group', 'Task name'),
        jobs=r('〈question-vN〉', *LEVEL_GROUPS),
        notes={f'tNN {k}NN 〈question〉': 'a kept question points to its source Task; membership comes from release.yaml' for k in LEVELS}),
    'data-prep': dict(
        folder=r('InsightDataPrep-〈set〉/', r('board.md'), r('background/'), r('runs/'),
                 r('jNN_prep-vK_〈slug〉/', r('jNN_〈job〉.md'), r('src/'), r('runs/'),
                   r('tNN_〈step〉/', r('step.md'), r('scripts/', r('〈script〉.py')))), *TAIL),
        headings=('Job name', 'Task name'),
        jobs=r('〈prep-vK〉', r('tNN 〈step〉')),
        notes={'tNN 〈step〉': 'ordered code steps; interfaces and checks live in step.md, execution belongs to the Board'}),
}




def rule_model(model, key):
    """One naming model supplies the Folder Tree and the separate Draw view."""
    rule = RULES[model['kind']]
    studio_tree, studio_notes = SC.studio_rule(model['kind'], model['name'], r)
    tree = rule['folder'] if key == 'folder' else r(model['name'], rule['jobs']) if key == 'jobs' else studio_tree

    def item(entry, address='root', depth=0):
        label, children = entry
        role = rule['headings'][depth-1] if key == 'jobs' and depth else ''
        text = f'[{role}] {label}' if role else label
        detail = rule['notes'].get(label, '') if key == 'jobs' else studio_notes.get(label, '') if key == 'studio' else PURPOSE.get(label, model['name']+' folder')
        if key == 'jobs' and role == 'Job name':
            detail = 'Type: ' + model['job_type']
        elif key == 'jobs' and role == 'Task name' and label != 't01 〈prep-vK〉':
            typ = 'Question definition' if model['kind']=='question-book' else 'Prep step' if model['kind']=='data-prep' else 'Question answer'
            detail = 'Type: ' + typ + '. ' + detail
        elif key == 'jobs' and role == 'Task group' and label in LEVELS.values():
            detail = 'Group type: Question level; derived from the source question level'
        ordered = sorted(children, key=lambda c:not c[0].endswith('/')) if key=='folder' else children
        return MT.Node(address, text, [item(c, address+'_'+str(i), depth+1) for i,c in enumerate(ordered)], [detail] if detail else [])
    return MT.MindMap({'mindmap':'1', 'title':model['name']+' '+key}, item(tree))


def rule_map(model, key):
    return shared_map(rule_model(model, key))


def model_tree(model):
    """Adapt source nodes to the Folder Tree already used for actual folders."""
    def convert(item):
        role, words = MM.split_role(item.text)
        links = MM.LINK.findall(words)
        href = MM.MH.safe_href(links[0][1]) if links else ''
        return dict(name=MT.display(words), role=role, path='', href=href,
                    notes=item.note, source_id=item.id,
                    children=[convert(child) for child in item.children])
    return '<ul class="tree rule" data-structure-shape="folder-tree">'+tree_html(convert(model.root))+'</ul>'


def rule_sections(model):
    example = CONFIG[model['kind']]['example']
    href = '/_board/workbench?' + urlencode({'path':model['path'], 'layout':'focus', 'section':'jobs'})
    examples = {
        'folder': '<ul class="tree" data-structure-shape="folder-tree">'+tree_html(model['folder'])+'</ul>',
        'jobs': model_tree(organization_mindmap(model)),
        'studio': '<ul class="tree" data-structure-shape="folder-tree">'+tree_html(model['studio_tree'])+'</ul>' if model['studios'] else '',
    }
    drawings = {
        'folder': branch_map(model['folder']),
        'jobs': shared_map(organization_mindmap(model), relative(map_source(model))),
        'studio': branch_map(model['studio_tree']) if model['studios'] else '',
    }
    out = []
    for key, content in examples.items():
        body = '<div data-rule="'+key+'">'+model_tree(rule_model(model, key))+'</div>'
        if content:
            body += open_dot(f'<details class="notes" data-example="{key}"><summary>{escape(example)}</summary>'
                             +content+'</details>', href, example, new_tab=True)
        out.append(f'<section id="{key}-rules" title="{escape(NAMING, quote=True)}" hidden>{body}</section>')
        drawing = rule_map(model, key)
        if drawings[key]:
            drawing += open_dot(f'<details class="notes"><summary>{escape(example)}</summary>'
                                +drawings[key]+'</details>', href, example, new_tab=True)
        out.append(f'<section id="{key}-map" hidden>{drawing}</section>')
    return ''.join(out)


def source_link(path, label):
    href = '/_board/page?' + urlencode({'path': '/' + path}) if path.endswith('.md') else '/' + quote(path)
    return f'<a href="{escape(href, quote=True)}" target="_blank" rel="noopener">{escape(label)}</a>'


def tree_html(tree, depth=0):
    text = source_link(tree['path'], tree['name']) if tree['path'] and not tree['children'] else escape(tree['name'])
    if tree.get('href'):
        text = f'<a href="{escape(tree["href"], quote=True)}" target="_blank" rel="noopener">{escape(tree["name"])}</a>'
    role = tree.get('role', '')
    if role in {'Job group','Job name','Job','Task group','Task name','Task'}:
        level = {'Job':'job-name','Task':'task-name'}.get(role,role.lower().replace(' ','-'))
        text = f'<span class="lvl" data-level="{level}" title="{escape(role, quote=True)}">{text}</span>'
    if tree.get('notes'):
        text = f'<span class="why" title="{escape(chr(10).join(tree["notes"]), quote=True)}">{text}</span>'
    identity = f' data-source-id="{escape(tree["source_id"], quote=True)}"' if tree.get('source_id') else ''
    if not tree['children']:
        return f'<li{identity}><span>{text}</span></li>'
    inner = ''.join(tree_html(c, depth+1) for c in tree['children'])
    return f'<li{identity}><details{" open" if depth<2 else ""}><summary>{text}</summary><ul>{inner}</ul></details></li>'


def grouped_organization(model):
    """Only Board Jobs need a group; versions in Book and Prep are Jobs themselves."""
    if model['kind'] != 'insight-board':
        return model['organization']
    groups = {}
    for tree in model['organization']:
        if tree['name'] not in groups:
            groups[tree['name']] = {**tree, 'children': []}
        groups[tree['name']]['children'].extend(tree['children'])
    for group in groups.values():
        group['children'].reverse()
    return list(groups.values())


def map_source(model):
    topic = BLOCK / model['topic']
    return topic / (model['topic']+'.mindmap.md')


def short_name(entry):
    name = entry['name']
    if entry['role']=='Job Name':
        pins = list(dict.fromkeys(re.findall(r'(?:data|prep|question)-v\d+',name)))
        return name.split('_',1)[0]+' · '+' × '.join(pins) if pins else name.replace('_',' ')
    if entry['role']=='Job':   # its own versions; the question version is its group
        pattern = r'(?:data|prep)-v\d+' if re.search(r'data-v\d+',name) else r'(?:question|prep)-v\d+'
        pins = list(dict.fromkeys(re.findall(pattern,name)))
        return ' · '.join([name.split('_',1)[0]]+pins)
    if entry['role'] in ('Task Name','Task'):
        return name.replace('_',' ').replace('-',' ')
    return name.split(' · ',1)[0]


def map_node(entry, key, depth=0):
    # A content adapter only: grammar, layout, folds and wires belong to hai-mindmap.
    label = short_name(entry)
    # the id reads the path inside the example Block, so moving the examples folder keeps every id
    inside = entry['path'].split(EXAMPLES, 1)[-1] if entry['path'] else entry['name']
    identity = entry.get('identity') or key+'/'+entry['role']+'/'+inside
    node_id = hashlib.sha256(identity.encode()).hexdigest()[:20]
    notes = list(entry.get('notes', []))
    if entry['path']:
        target = '/_board/page?'+urlencode({'path':entry['path']}) if entry['path'].endswith('.md') else '/'+quote(entry['path'])
        label = f'[{label}]({target})'
        notes.append(entry['path'])
    if entry.get('kept'):
        notes.insert(0,'↗ kept from the source question')
    return MB.built(node_id, f'[{entry["role"]}] {label}',
                    [map_node(child,identity,depth+1) for child in entry['children']], notes)


def organization_mindmap(model):
    roots = grouped_organization(model)
    root = MB.built(model['kind'], model['name'],
                    [map_node(entry,model['kind']) for entry in roots])
    root.id = 'root'
    fresh = MT.MindMap({'mindmap':'1','title':model['name']+' organization','built':'insight-structure', 'organization-levels':'2'},root)
    path = map_source(model)
    if path.is_file():
        old = MT.load(path)
        if old.meta.get('mindmap')=='1':
            SC.align_map_levels(old, model['kind'], fresh)
            MB.refresh(old,fresh)  # The shared merge preserves a person's words and added branches.
            return old
        # Preserve the earlier generated outline, including any notes, during grammar migration.
        fresh.tail = '## Previous structure source\n\n'+path.read_text()
    return fresh


def shared_map(tree, source=''):
    rendered = MM.draw(tree,source,editable=False,fold=True)
    # Shared cards escape their title, whereas leaf labels already strip Markdown links.
    # Normalize only visible title content; retain the shared source chip and original data-raw.
    for branch in tree.root.children:
        _, title = MM.split_role(branch.text)
        rendered = rendered.replace('>'+escape(title)+'</b>', '>'+escape(MT.display(title))+'</b>')
    return '<div class="shared-map">'+rendered+'</div>'


def branch_map(entry):
    root = map_node(entry,entry['path'] or entry['name'],-1)
    root.id = 'root'
    root.text = entry['name']
    return shared_map(MT.MindMap({'mindmap':'1','title':entry['name']},root))


def render(model):
    cfg = CONFIG[model['kind']]
    studios = '<ul>'+''.join(f'<li>{source_link(s["source"],s["name"])}<code>{escape(s["owner"])}</code></li>'
                            for s in model['studios'])+'</ul>' if model['studios'] else ''
    sources = ''.join('<li>'+source_link(p,p)+'</li>' for p in model['sources'])
    payload = json.dumps(model,ensure_ascii=False).replace('<','\\u003c')
    return f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{cfg['name']} Structure</title><style>{PB_CSS}</style><link rel="stylesheet" href="structure.css">
<main>
{rule_sections(model)}
<section id="folder" hidden><h1>Folder</h1><code>{escape(model['path'])}/</code>
<div class="structure-content"><ul class="tree">{tree_html(model['folder'])}</ul></div>
<div class="diagram">{branch_map(model['folder'])}</div></section>
<section id="jobs" hidden><h1>Job-Task</h1>
{shared_map(organization_mindmap(model),relative(map_source(model)))}
<div class="structure-content">
<details class="notes"><summary>Why these groups and types</summary>
<p>{escape(cfg['groups'])}</p><p>A type names a responsibility from the contract; the files carry no job-type or task-type field.</p>
<p>{escape(cfg['gap'])}</p><ul>{sources}</ul></details></div>
</section>
<section id="studio" hidden><h1>Studio</h1>
<div class="structure-content">{studios}</div>
<div class="diagram">{branch_map(model['studio_tree'])}</div></section>
</main><script type="application/json" id="structure-model">{payload}</script>
<script src="structure.js"></script></html>
'''


def manifest(kind):
    cfg=CONFIG[kind]
    content=relative(HERE / (kind+'.html'))
    entries=[('Folder','folder'),('Job-Task','jobs'),('Studio','studio')]
    views=[dict(name=view,items=[dict(name=name,path=content,fragment=key+suffix) for name,key in entries])
           for view,suffix in [('Structure','-rules'),('Draw','-map')]]
    def skill_path(name):
        paths=list((ROOT/SKILLS).rglob(name+'/SKILL.md'))
        if len(paths)!=1:
            raise ValueError(f'Expected one skill {name}, got {paths}')
        return relative(paths[0])
    views.append(dict(name='Skills',items=[dict(name=name,path=skill_path(name)) for name in cfg['skills']]))
    return dict(views=views[:1]+SC.views(BLOCK/cfg['topic'])+views[1:])


def mindmap(model):
    return MT.dump(organization_mindmap(model))


def generated_files():
    out={}
    inventory=dict(block={},job={},task={})
    for kind,cfg in CONFIG.items():
        model=load_model(kind)
        topic=BLOCK/cfg['topic']
        out.update({p:t for p,t in SC.outputs(topic).items() if p.name!='studio-views.json'})
        out[HERE/(kind+'.html')]=render(model)
        out[topic/'studio-views.json']=json.dumps(manifest(kind),ensure_ascii=False,indent=2)+'\n'
        out[topic/(cfg['topic']+'.mindmap.md')]=mindmap(model)
        inventory['block'][model['path']]=cfg['name']
        for job in model['jobs']:
            inventory['job'][job['path']]=job['type']
            for task in job['tasks']:inventory['task'][task['path']]=task['type']
    out[BLOCK/'delivery/page-spec/example-types.json']=json.dumps(inventory,ensure_ascii=False,indent=2)+'\n'
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    mismatches=[]
    for path,text in generated_files().items():
        if args.check:
            if not path.is_file() or path.read_text()!=text:mismatches.append(relative(path))
        else:
            if not path.is_file() or path.read_text()!=text:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text(text,encoding='utf-8')
    if mismatches:raise SystemExit('Regenerate: '+', '.join(mismatches))
    print('Generated content is current' if args.check else 'Built three Insight structure Studios')


if __name__=='__main__':
    main()
