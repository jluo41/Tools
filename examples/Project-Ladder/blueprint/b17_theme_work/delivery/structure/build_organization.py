"""Build the content models inside shared Studio views; no independent page framework."""
from html import escape as esc
from pathlib import Path
import re
import json
from urllib.parse import quote, urlencode
from functools import lru_cache
import hashlib
import os
import sys

HERE = Path(__file__).resolve().parent
KINDS = ('work', 'blueprint', 'cowork', 'discovery')
LABELS = ('Folder', 'Job-Task', 'Studio')
# Structure and the live Studio use the same shared band registry.
def _studio_types():
    path = HERE.parent / "page-spec/studio-bands.json"
    rows = json.loads(path.read_text(encoding="utf-8"))["bands"]
    return tuple((f"{row['emoji']} {row['name']}".strip(), row["band"], row.get("holds", "")) for row in rows)


BLUEPRINT_BANDS = _studio_types()


def node(label, *children):
    return (label, children)


ROOT = HERE.parents[5]
SOURCES = {
    'work': 'examples/Project-Ladder/work/b01_example_work',
    'blueprint': 'examples/Project-Ladder/blueprint/b16_theme_paper',
    'cowork': 'examples/Project-Ladder/cowork/b01_example_cowork',
    'discovery': 'examples/Project-Ladder/discovery/b01_example_discovery',
}


def folder_tree(kind):
    """Read actual names and parentage. Organization labels never create folders."""
    source = ROOT / SOURCES[kind]

    def read(path):
        children = []
        if path.is_dir() and not path.is_symlink():
            for child in sorted(path.iterdir(), key=lambda p: p.name):
                if child.name.startswith('.') or child.name == '__pycache__':
                    continue
                children.append(read(child))
        return node(path.name + ('/' if path.is_dir() else ''), *children)

    return read(source)


def folder_rows(kind):
    rows = []
    for path in sorted((ROOT / SOURCES[kind]).iterdir()):
        name = path.name
        if name == 'board.md':
            detail = 'Block purpose, scope, completion condition and authored grouping.'
        elif path.is_dir() and name.startswith('j') and name[1:3].isdigit():
            detail = 'Existing Job: its face and the work records already stored with it.'
        elif path.is_dir() and name.startswith('s') and name[1:3].isdigit():
            detail = 'Existing Studio: its question, decisions, drawings and retained history.'
        elif name == 'trace':
            detail = 'Requests, plans, changes and verification records.'
        elif name == 'delivery':
            detail = 'Selected outputs and their instructions for use.'
        elif name == 'related':
            detail = 'Source material and references used by this Block.'
        else:
            continue
        rows.append((name + ('/' if path.is_dir() else ''), detail))
    return rows


# Design responsibility categories, not new schema values; names bind to real records.
JOB_MODELS = {
    'work': [
        ('Tool implementation', 'j01_first_cli', [('Input handling', 't01_read_csv'),
                                                ('Result reporting', 't02_print_report')]),
        ('Documentation', 'j02_first_docs', [('Usage documentation', 't01_readme')]),
        ('Validation', 'j11_core_checks', [('Data checks', 't01_schema_check'),
                                         ('Data checks', 't02_value_ranges'),
                                         ('Data checks', 't03_missing_values'),
                                         ('Result reporting', 't11_text_report'),
                                         ('Result reporting', 't12_html_report'),
                                         ('Visual display', 't13_range_figure')]),
    ],
    'blueprint': [
        ('UI implementation', 'j01_paper_workbench_pages', [('Block UI', 't01_board_page'),
                                                         ('Job UI', 't02_version_page'),
                                                         ('Task UI', 't03_section_page')]),
        ('Tooling performance', 'j02_word_lane_speed', [('Performance engineering', 't01_word_lane_code')]),
    ],
    'cowork': [
        ('People reference', 'j00_people', []),
        ('Requests and approvals', 'j01_data_access_request', []),
        ('Requests and approvals', 'j02_review_board_amendment', [('Collaborative document', 't01_data_use_plan')]),
        ('Coordination', 'j03_kickoff_meeting', []),
    ],
    'discovery': [
        ('Evidence inquiry', 'j01_policy_effect_inquiry', [('Topic summary', 't01_policy_prior_work')]),
        ('Evidence inquiry', 'j02_subgroup_effect_inquiry', [('Source map', 't01_subgroup_prior_work')]),
    ],
}
BLOCK_NAMES = {'work': 'Work Block', 'blueprint': 'Blueprint Work Block',
               'cowork': 'CoWork Block', 'discovery': 'Discovery Block'}


def record(folder):
    face = folder / (folder.name + '.md')
    text = face.read_text()
    heading = next((x[2:].strip() for x in text.splitlines() if x.startswith('# ')), folder.name)
    heading = re.sub(r'^[jt]\d+\s*[·:—-]\s*', '', heading)
    if re.fullmatch(r'Task \d+ name', heading, re.I):
        heading = re.sub(r'^[jt]\d+_', '', folder.name).replace('_', ' ')
        heading = heading[:1].upper() + heading[1:]
        heading = re.sub(r'\b(csv|html|readme)\b', lambda m: m[0].upper(), heading, flags=re.I)
    fields = re.findall(r'(?m)^(task-type|task-kind|job-kind):[ \t]*(.*)$', text)
    manifest = folder / 'discovery.yaml'
    if manifest.is_file():
        fields += re.findall(r'(?m)^(discovery_type):[ \t]*(.*)$', manifest.read_text())
    return heading, face, '; '.join(k + ': ' + (v.strip() or 'not declared') for k, v in fields)


def organization_rows(kind):
    rows = []
    for job_kind, job_name, tasks in JOB_MODELS[kind]:
        job = ROOT / SOURCES[kind] / job_name
        jtitle, jface, jfields = record(job)
        for task_kind, task_name in tasks or [(None, None)]:
            ttitle, tface, tfields = record(job / task_name) if task_name else ('—', None, '')
            rows.append((job_kind, jtitle, task_kind or '—', ttitle, jface, tface, jfields, tfields))
    return rows


def job_tree(kind):
    groups = {}
    for jkind, jname, tkind, tname, *_ in organization_rows(kind):
        groups.setdefault(jkind, {}).setdefault(jname, {}).setdefault(tkind, [])
        if tkind != '—':
            groups[jkind][jname][tkind].append(node(tname))
    return node(BLOCK_NAMES[kind], *[
        node(jkind, *[node(jname, *[node(tkind, *tasks) for tkind, tasks in kinds.items() if tkind != '—'])
                     for jname, kinds in jobs.items()]) for jkind, jobs in groups.items()])


@lru_cache(maxsize=1)
def shared_mindmap():
    """Use the same host-owned skill loader as the live focus-map route."""
    host = str(ROOT / 'plugins/haipipe-toolkit/servers/_host')
    if host not in sys.path:
        sys.path.insert(0, host)
    from live.frame import mindmap_module
    return mindmap_module()


def source_url(face):
    """A Job or Task selection opens inside its owning Block."""
    face = face.resolve()
    if not face.is_relative_to(ROOT):
        return ''
    folder = face.parent
    if re.match(r'^[jt]\d\d[_-]', folder.name):
        job = folder.parent if folder.name.startswith('t') else folder
        block = job.parent
        if (block / 'board.md').is_file():
            query = {'path': str(block.relative_to(ROOT)), 'layout': 'focus',
                     'section': 'jobs', 'group': job.name[:3]}
            if folder != job:
                query['task'] = folder.name[:3]
            return '/_board/workbench?' + urlencode(query)
    return '/_board/page?' + urlencode({'path': str(face.relative_to(ROOT))})


def organization_model(kind=None, *, tree=None, sources=None,
                       headings=('Job Type', 'Job Name', 'Task Type', 'Task Name')):
    """Adapt verified content to the existing mind map grammar; no layout code."""
    mm = shared_mindmap()
    if kind is not None:
        if tree is not None or sources is not None:
            raise ValueError('Supply either kind or tree/sources')
        tree, sources = job_tree(kind), {}
        for jk, jname, tk, tname, jface, tface, jf, tf in organization_rows(kind):
            sources[(jk, jname)] = (jface, jf)
            if tface:
                sources[(jk, jname, tk, tname)] = (tface, tf)
    elif tree is None:
        raise ValueError('A Block tree is required')
    sources = sources or {}
    serial = 0

    def convert(entry, ancestry=()):
        nonlocal serial
        label, children = entry
        level, path = len(ancestry), (*ancestry, label)
        if level >= len(headings):
            raise ValueError('Organization exceeds its declared levels below the Block root')
        serial += 1
        key = (3, ancestry[1], label) if level == 3 else (level, label)
        source = sources.get(path, sources.get(key))
        words, notes = label, []
        if source:
            face, fields = source
            face = face.resolve()
            if not face.is_relative_to(ROOT):
                raise ValueError('Source must remain inside SPACE')
            words = '[' + label + '](' + os.path.relpath(face, HERE) + ')'
            notes = [str(face.relative_to(ROOT))] + ([fields] if fields else [])
        result = mm.MT.Node('n' + str(serial), '[' + headings[level] + '] ' + words, note=notes)
        result.children = [convert(child, path) for child in children]
        return result

    root = mm.MT.Node('root', tree[0], children=[convert(c) for c in tree[1]])
    return mm.MT.MindMap({'mindmap': '1', 'written': 'yes'}, root)


def organization_map(kind=None, *, tree=None, sources=None, column_width=240, node_width=190,
                     headings=('Job Type', 'Job Name', 'Task Type', 'Task Name'), fold=True):
    """Compatibility data adapter. Dimensions are retained only for old callers."""
    model = organization_model(kind, tree=tree, sources=sources, headings=headings)
    identity = 'structure-' + hashlib.sha256(repr(model).encode()).hexdigest()[:16]
    return shared_mindmap().draw(model, identity, editable=False, base=HERE,
                                url_of=source_url, fold=fold)



def example_maps(kind):
    """One real Job at a time, preserving the four horizontal mind-map levels."""
    examples, sources = {}, {}
    for jkind, jname, tkind, tname, jface, tface, jf, tf in organization_rows(kind):
        kinds = examples.setdefault((jkind, jname), {})
        sources[(jkind, jname)] = (jface, jf)
        if tface:
            kinds.setdefault(tkind, []).append(node(tname))
            sources[(jkind, jname, tkind, tname)] = (tface, tf)

    options, panels = [], []
    for i, ((jkind, jname), kinds) in enumerate(sorted(examples.items(), key=lambda item: not bool(item[1]))):
        branch = node(jkind, node(jname, *[node(tkind, *tasks) for tkind, tasks in kinds.items()]))
        tree = node(BLOCK_NAMES[kind], branch)
        options.append(f'<option value="{i}">{esc(jname)}</option>')
        panels.append(f'<div class="example-panel" data-example="{i}"' + (' hidden' if i else '') + '>' +
                      organization_map(tree=tree, sources=sources) + '</div>')
    return ('<div class="job-examples"><label class="example-picker">Example '
            '<select aria-label="Example" title="' + esc('; '.join(label + ': ' + text for label, text in ORGANIZATION[kind])) + '">' + ''.join(options) + '</select></label>' + ''.join(panels) + '</div>')

def studio_tree(kind):
    if kind == 'blueprint':
        return node('Blueprint Work Block', *[node(f'{band} · {nn}') for band, nn, _ in BLUEPRINT_BANDS])
    if kind == 'cowork':
        return node('CoWork Block', node('Partner requirements'), node('Collaboration conditions'))
    if kind == 'discovery':
        return node('Discovery Block', node('Research scope'), node('Evidence interpretation'))
    return node('Work Block', node('What the tool checks'), node('HTML report layout'))


PURPOSE = {   # each folder's job, shown as its hover (b17 trace 261127/1225)
    'bNN_〈block〉/': 'the Block: one piece of work and all it holds',
    'board.md': "the Block's face: its goal, Jobs and Studio topics",
    'j00_people/': 'who is involved and how to reach them',
    'jNN_〈job〉/': 'a Job: one goal, done by its Tasks',
    'jNN_〈job〉.md': "the Job's face: its goal, close and Tasks in order",
    'tNN_〈task〉/': 'a Task: one step of its Job',
    'tNN_〈task〉.md': "the Task's face: its goal and state",
    'runs/': "the Task's Runs, each one try with its result",
    'CHECKLIST.md': 'what the request still needs',
    'Timeline.md': 'what happened, in order',
    'sNN-〈topic〉/': 'a Studio topic: a drawing or design to talk through',
    'trace/': 'a record of each change, by day',
    'related/': 'what came in from outside (papers, notes, files); made when first needed',
    'delivery/': 'what the Block hands out (pages, files); made when first needed',
}
NAMING = 'Fixed name · 〈Name for this work〉'


def rule_folder(kind):
    """Naming patterns only: never write or migrate the illustrated folders."""
    if kind == 'cowork':
        jobs = [node('j00_people/', node('j00_people.md')),
                node('jNN_〈job〉/', node('jNN_〈job〉.md'), node('CHECKLIST.md'), node('Timeline.md'))]
    else:
        jobs = [node('jNN_〈job〉/', node('jNN_〈job〉.md'),
                     node('tNN_〈task〉/', node('tNN_〈task〉.md'), node('runs/')))]
    return node('bNN_〈block〉/', node('board.md'), *jobs, node('sNN-〈topic〉/'),
                node('trace/'), node('related/'), node('delivery/'))


def rule_jobs(kind):
    """Groups are optional authored organization, never canonical type names."""
    if kind == 'cowork':
        tree = node(BLOCK_NAMES[kind], node('〈Job group〉', node('j00_people'), node('〈Request or coordination job〉')))
        headings = ('Job group · optional', 'Job name')
    elif kind == 'discovery':
        # Discovery's Job is itself the inquiry group; do not invent another level.
        tree = node(BLOCK_NAMES[kind], node('〈Inquiry name〉', node('〈Research question〉')))
        headings = ('Job / inquiry group', 'Task / research topic')
    else:
        tree = node(BLOCK_NAMES[kind], node('〈Job group〉', node('〈Job name〉',
                    node('〈Task group〉', node('〈Task name〉')))))
        headings = ('Job group · optional', 'Job name', 'Task group · optional', 'Task name')
    return tree, headings


def rule_sections(kind):
    tree, headings = rule_jobs(kind)
    # the levels as a folder tree, as Folder is, each level's name small after it (b17 trace 261127/1250)
    diagram = '<div class="drawing"><ul class="tree"><li>' + tree_html(tree, roles=('',) + tuple(headings)) + '</li></ul></div>'
    folders = dict(zip(KINDS, ('s01-work-ladder', 's02-work-skills',
                               's03-q01-work-ladder', 's04-workbench-page-structure')))
    source = HERE.parent.parent / folders[kind] / 'studio-organization.mindmap.md'
    model = shared_mindmap().MT.load(source)
    def as_tree(item):
        return node(item.text, *[as_tree(child) for child in item.children])
    studio = ('<div class="drawing"><ul class="tree"><li>'
              + tree_html(as_tree(model.root)) + '</li></ul></div>')
    folder = '<div class="drawing"><ul class="tree"><li>' + tree_html(rule_folder(kind), True, purpose=True) + '</li></ul></div>'
    return ''.join('<section id="' + key + '-rules" title="' + esc(NAMING) + '" hidden>' + body + '</section>'
                   for key, body in (('folder', folder), ('jobs', diagram), ('studio', studio)))


def tree_html(tree, folder=False, roles=(), depth=0, purpose=False):
    label, children = tree
    icon = '📁' if folder and label.endswith('/') else '◇'
    said = roles[depth] if depth < len(roles) else ''
    base = label.strip('〈〉/').lower()
    if base and said.lower().startswith(base):        # no "〈Job name〉 Job name": keep only what the name lacks
        said = said[len(base):].lstrip(' ·')
    role = f'<small class="role">{esc(said)}</small>' if said else ''
    text = f'<span aria-hidden="true">{icon}</span> {esc(label)}{role}'
    why = PURPOSE.get(label) if purpose else None   # the rule tree only; a real Block's tree stays as read
    if why:
        text = f'<span class="why" title="{esc(why)}">{text}</span>'
    if children:
        inner = ''.join('<li>' + tree_html(c, folder, roles, depth + 1, purpose) + '</li>' for c in children)
        return f'<details open><summary>{text}</summary><ul>{inner}</ul></details>'
    return f'<span class="leaf">{text}</span>'


ORGANIZATION = {
    'work': [('Organization', 'Tool implementation, documentation and validation organize this CSV-tool example. Task categories distinguish input handling, checks and reporting; these are responsibility categories, not new execution task-type values.'),
             ('Source records', 'Names open existing records. Generic Task titles use their meaningful folder names. These records declare code or display; code is an existing example value, not a newly registered skill type.')],
    'blueprint': [('Organization', 'UI implementation divides into Block UI, Job UI and Task UI responsibilities. Tooling performance is a separate Job. Names come from the existing Paper blueprint; legacy page names describe stored work, not standalone Job/Task routes.'),
                  ('Source records', 'The three page Tasks declare task-type: ui; the Word lane Task declares no task-type. UI is an existing example value, not a new canonical execution type. This mapping does not certify the older records against the latest framework.')],
    'cowork': [('Organization', 'People reference, requests and approvals, and coordination have different responsibilities. IRB work may concern an initial application or an amendment; this example is an amendment.'),
               ('Contract mismatch', 'The existing IRB Job contains a Data-use plan Task (task-kind: page); the UI definition calls it a Collaboration Task. hai-cowork says there is no Task level. The contract and example still need reconciliation. A dash means this named Job has no Task in this mapping.')],
    'discovery': [('Organization', 'Each inquiry names the effect it investigates. Its Task names an evidence question and declares topic-summary or source-map. Search, acquire and synthesize are workflow phases, not Task types.'),
                  ('Source records', 'The Task categories come from discovery.yaml. Each admitted paper or source belongs to a Run beneath its Task.')],
}


def studio_rows(kind):
    if kind == 'blueprint':
        return [(f'{band} · {nn}', what) for band, nn, what in BLUEPRINT_BANDS] + [
                ('Skills', 'Related contracts are a view inside the relevant Studio topic, not a separate topic per skill.')]
    if kind == 'cowork':
        return [('Partner requirements', 'Clarify what the receiving office or partner needs before the work can move.'),
                ('Collaboration conditions', 'Discuss data-use, retention and handoff conditions. These examples describe coordination topics, not a new folder taxonomy.')]
    if kind == 'discovery':
        return [('Research scope', 'Set the question, boundaries and relevant settings for the inquiry.'),
                ('Evidence interpretation', 'Discuss what the sources support, disagreements and limits. Reading individual sources remains Run work.')]
    return [('What the tool checks', 'Defines the checks the CSV tool must perform and their order.'),
            ('HTML report layout', 'Designs how that tool presents its check results.')]


STYLE = '''
:root{color-scheme:light dark;--paper:#fff;--ink:#223047;--muted:#59677b;--line:#d9e2ee;--soft:#edf5ff;--accent:#275f9f;--fg:var(--ink);--mut:var(--muted);--card:var(--paper);--acc:var(--accent);--wash:var(--soft)}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:14px/1.65 system-ui,sans-serif}
main{padding:22px;max-width:1080px;margin:auto}h1{font-size:20px;letter-spacing:-.3px;margin:0 0 22px}
.tree,.tree ul{list-style:none}.tree{padding:0;margin:0}.tree ul{margin:8px 0 10px 13px;padding-left:23px;border-left:1px solid var(--line)}
.tree li{position:relative;margin:4px 0}.tree ul>li:before{content:'';position:absolute;left:-23px;top:14px;width:23px;border-top:1px solid var(--line)}
summary,.leaf{display:inline-block;padding:2px 4px;background:none}
summary{cursor:pointer;list-style-position:inside;display:list-item;width:fit-content}summary:hover{color:var(--accent)}
.tree>li>details>summary{color:var(--accent);font-weight:600}
.tree summary span,.leaf span{color:var(--accent);margin-right:5px}.tree span.why{color:inherit;margin:0;cursor:help}.drawing{overflow:auto;padding:5px 4px 18px}
.role{display:inline-block;margin-left:12px;color:var(--muted);font-size:11px;font-weight:400}
.drawing .tree{min-width:0;overflow-wrap:anywhere}.records{margin:24px 0 0;border-top:1px solid var(--line)}
.record{display:grid;grid-template-columns:minmax(130px,1fr) 2fr;gap:20px;padding:15px 0;border-bottom:1px solid var(--line)}
.record dt{font-weight:600;overflow-wrap:anywhere}.record dd{margin:0;color:var(--muted)}

.content>section[hidden]{display:none}body[data-mode=draw] .records{display:none}a{color:var(--accent)}
.job-examples [hidden]{display:none!important}
.example-picker{display:flex;align-items:center;gap:12px;margin-bottom:20px;color:var(--muted)}
.example-picker select{min-width:0;max-width:100%;flex:1;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink);font:16px system-ui}
.studio-topics{list-style:none;padding:0;margin:0;font-size:17px}
.studio-topics li{padding:14px 0;border-bottom:1px solid var(--line)}
@media(prefers-color-scheme:dark){:root{--paper:#19232f;--ink:#e3eaf4;--muted:#abb9cb;--line:#3b4b60;--soft:#243c55;--accent:#9bc9ff}}
@media(max-width:500px){main{padding:14px}.record{grid-template-columns:1fr;gap:5px}}
'''


MAP_SCRIPT = ''  # Compatibility export: mmmap.draw includes the shared script.



def organization_document(title, *, tree, sources=None):
    """An embeddable Studio content document; it introduces no workbench route."""
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title><style>{STYLE}</style></head><body>'
            f'<main><h1>{esc(title)}</h1>' + organization_map(tree=tree, sources=sources) +
            '</main><script>' + MAP_SCRIPT + '</script></body></html>')


def render(kind):
    trees = [folder_tree(kind), job_tree(kind), studio_tree(kind)]
    records = [folder_rows(kind), ORGANIZATION[kind], studio_rows(kind)]
    sections = []
    for key, title, tree, rows in zip(('folder', 'jobs', 'studio'), LABELS, trees, records):
        if key == 'jobs':
            sections.append('<section id="jobs" hidden>' + example_maps(kind) + '</section>')
            continue
        if key == 'studio':
            sections.append('<section id="studio" hidden>' +
                            organization_map(tree=tree, headings=('Studio topic',)) + '</section>')
            continue
        roles = ('Block', 'Job Type', 'Job Name', 'Task Type', 'Task Name') if key == 'jobs' else (('Block type', 'Studio topic type') if key == 'studio' else ())
        items = ''.join(f'<div class="record"><dt>{esc(name)}</dt><dd>{esc(text)}</dd></div>' for name, text in rows)
        sections.append(f'<section id="{key}"'+(' hidden' if key != 'folder' else '')+f'><h1>{esc(title)}</h1>' + (example_maps(kind) if key == 'jobs' else '') +
                        ('' if key == 'jobs' else '<div class="drawing"'+(f' title="{esc(SOURCES[kind])}"' if key == 'folder' else '')+'><ul class="tree"><li>'+tree_html(tree, key == 'folder', roles)+'</li></ul></div>') +
                        ('' if key == 'jobs' else '<dl class="records">'+items+'</dl>')+'</section>')
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{kind.title()} structure</title><style>{STYLE}</style></head><body><main class="content">'+rule_sections(kind)+''.join(sections)+'''</main>
<script>function pick(){const hash=location.hash.slice(1),draw=hash.endsWith('-draw');
const requested=hash.replace(/-draw$/,'');const section=document.getElementById(requested);
const key=section?requested:'folder-rules';
document.body.dataset.mode=draw?'draw':'structure';document.querySelectorAll('main>section').forEach(s=>s.hidden=s.id!==key);
if(key.startsWith('folder')||key==='studio-rules')document.querySelectorAll('#'+key+' details').forEach((d,i)=>d.open=draw||i===0);}
''' + MAP_SCRIPT + '''document.querySelectorAll('.job-examples').forEach(examples=>{
 const select=examples.querySelector('select');
 select.addEventListener('change',()=>{examples.querySelectorAll('[data-example]').forEach(panel=>panel.hidden=panel.dataset.example!==select.value);if(window.pmDraw)requestAnimationFrame(window.pmDraw)});
});
addEventListener('hashchange',()=>{pick();if(window.pmDraw)requestAnimationFrame(window.pmDraw)});pick();</script></body></html>''')


if __name__ == '__main__':
    for kind in KINDS:
        (HERE / f'{kind}-organization.html').write_text(render(kind))
    print('Built four structure content files.')
