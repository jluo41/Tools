"""The focus page's identity line: what type of page this is, its use case."""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from live import frame
from live.focus_base import WORK_SHAPE, inside, page_level, page_module
from live.page_spec import spec_dir


# a Task's use case from the task-type it already declares (b17 delivery/page-spec/task-views.md); an explicit `use-case:` wins
TASK_USE_CASE = {'raw': '📥 Data extraction', 'description': '📖 Data description', 'describe': '📖 Data description',
                 'data': '🔄 Data transformation', 'algo': '🧩 Algorithm development', 'fit': '🧪 Model fitting',
                 'eval': '📏 Evaluation', 'evaluate': '📏 Evaluation', 'stata': '📈 Statistical analysis',
                 'individual': '👤 Individual analysis', 'display': '📊 Display preparation',
                 'endpoint': '📦 Endpoint packaging', 'agent': '🤖 Agent execution', 'evidence': '🧾 Evidence preparation'}


# the five Block types of the work family (skills/2_work/<type>/), by the Project folder a Block sits in
WORK_BLOCK_TYPES = {'work': '🧩 Work Block (Work)', 'tasks': '🧩 Work Block (Work)', 'blueprint': '📐 Work Block (Blueprint)',
                    'cowork': '🤝 Work Block (CoWork)', 'discovery': '🔎 Work Block (Discovery)', 'knowledge': '📚 Work Block (Knowledge)'}
# a Block type's use case when its face writes none and its type has one
BLOCK_USE_CASE = {'📐 Work Block (Blueprint)': '🎨 Theme development'}


# the theme Block whose delivery/page-spec/<level>-views.md names each page type and its use cases (one table, the page reads it)
TYPE_TABLES = {'work': 'b17_theme_work', 'discovery': 'b17_theme_work', 'cowork': 'b17_theme_work',
               'paper': 'b16_theme_paper', 'insight': 'b11_theme_insight', 'design': 'b12_theme_design',
               'labeling': 'b15_theme_labeling'}


@lru_cache(maxsize=32)
def type_use_cases(theme: str, level: str) -> dict:
    """{plain type name: [its use cases]} from the theme's own type table in Tools."""
    block = TYPE_TABLES.get(theme)
    tools = Path(__file__).resolve().parents[6]
    path = spec_dir(tools / 'examples/Project-Ladder/blueprint' / str(block)) / f'{level.lower()}-views.md'
    out = {}
    if not block or not path.is_file():
        return out
    for line in path.read_text(encoding='utf-8', errors='ignore').splitlines()[2:]:
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) > 2 and cells[2] not in ('', '—', '---'):
            out[plain_type(cells[1])] = [u.strip() for u in cells[2].split('<br>') if u.strip()]
    return out


def plain_type(label: str) -> str:
    return re.sub(r'^[^A-Za-z0-9]+', '', str(label)).strip().casefold()


def page_type(theme: str, level: str, folder: Path, root: Path, data: dict) -> str:
    """The page's type, named by the same branch that draws it (each theme's delivery/page-spec/<level>-views.md and example-types.json):
    every theme, not only work (JL 261109: "this should be used for all the cases ... include the labeling, design and
    insight")."""
    name = folder.name
    if page_module(theme, folder, root)[1] == 'prototype_':
        return {'Block': 'Question Book', 'Job': 'Question Book release'}.get(level, '')
    if theme in WORK_SHAPE:
        if level == 'Block':
            face = data.get('face')
            text = face.read_text(encoding='utf-8', errors='ignore') if face and inside(face, root) else ''
            if theme == 'work' and (re.search(r'(?m)^theme:\s*\S', text) or any(data.get('ui', {}).values())):
                return '📐 Work Block (Blueprint)'
            by_folder = WORK_BLOCK_TYPES.get(folder.parent.name)       # the Project folder the Block sits in
            return by_folder or {'work': '🧩 Work Block (Work)', 'discovery': '🔎 Work Block (Discovery)',
                                 'cowork': '🤝 Work Block (CoWork)'}.get(theme, '')
        if level == 'Job':
            return {'work': '🧩 Job', 'discovery': '🔎 Inquiry Job',
                    'cowork': '👥 People' if name == 'j00_people' else '🤝 Collaboration Job'}.get(theme, '')
        return {'work': '🧩 Task', 'discovery': '🔎 Inquiry Task', 'cowork': '🤝 Collaboration Task'}.get(theme, '')
    if theme == 'paper':
        from live import idea_block, paper_jobs
        if idea_block.idea_block_of(folder) is not None:     # an Idea Block in paper/ (hai-ideation)
            return {'Block': '💡 Idea Block', 'Job': '💡 Idea Job', 'Task': '💡 Assessment Task'}.get(level, '')
        if level == 'Block':
            return '💰 Grant Board' if name.casefold().startswith('grant') else '📄 Paper Board'
        if level == 'Job':
            return paper_jobs.job_type_label(folder)
        job = folder.parent
        if paper_jobs.is_version(job):
            return '📝 Draft Task'
        kind = paper_jobs.job_kind(job)
        if kind == 'display':
            return '🖼️ Display Task'
        if kind == 'value':
            return '🗄️ Value Tables' if 'value-tables' in name else '🔢 Values'
        if kind == 'citation':
            return '📚 Citations'
        if kind == 'submission':
            return ('✉️ Submission Letter' if 'letter' in name else '🚶 Portal Walk' if 'portal-walk' in name
                    else '📮 Portal Fill' if 'portal-fill' in name else '')
        return ''
    if theme == 'insight':
        if level != 'Task':
            return {'Block': 'Insight Board', 'Job': 'Analysis'}[level]
        m = re.match(r't\d+_([DIKWX])\d+_', name)
        return {'D': 'Data question', 'I': 'Information question', 'K': 'Knowledge question', 'W': 'Wisdom question',
                'X': 'Executive question'}.get(m[1], '') if m else ''
    if theme == 'design':
        from live import design_reader as _DR               # a Design Method Book and its method types (JL 261109)
        if level == 'Block' and _DR.is_method_book(folder):
            return '📘 Design Method Book'
        if level == 'Job' and _DR.is_method_book(folder.parent):
            return '📘 Design method'
        if level != 'Task':
            return {'Block': '🎨 Design Board', 'Job': '🧩 Design Job'}[level]
        return ('💡 Reason ideas' if name.startswith('t00_') else '🏆 Review whole' if name.startswith('t99_')
                else '✏️ One design' if re.match(r't\d+_d\d+', name) else '')
    if theme == 'labeling':
        if level != 'Task':
            return {'Block': '🏷️ Labeling', 'Job': '🗃️ Dataset × Label'}[level]
        return ('📦 Items' if re.search(r'_(items|transcripts)$', name) else '🧭 Meaning' if 'meaning' in name
                else '🛠️ Expression' if 'expression' in name else '')
    return ''


def page_identity_html(theme: str, folder: Path, root: Path, data: dict) -> str:
    """The small line under every Block's, Job's and Task's title, in every theme: its type and, when known, its use
    case (JL 261109). A use case is the face's `use-case:`; else a work Task's task-type; else the one use case the
    theme's table gives that type; a type with several and none written shows none (never guessed)."""
    level = page_level(folder)
    if level not in ('Block', 'Job', 'Task'):
        return ''
    face = data.get('face')
    if level == 'Task' and face and inside(face, root) and re.search(
            r'(?m)^task-type:\s*draft\b', face.read_text(encoding='utf-8', errors='ignore')):
        return ''                                 # Draft Lab: the text first, no type line (JL 261115)
    kind = page_type(theme, level, folder, root, data)
    if not kind:
        return ''
    use = data.get('use_case') or ''
    if not use and level == 'Block':
        use = BLOCK_USE_CASE.get(kind, '')
    if not use and theme == 'work' and level == 'Task':
        face = data.get('face')
        text = face.read_text(encoding='utf-8', errors='ignore') if face and inside(face, root) else ''
        use = TASK_USE_CASE.get((re.search(r'(?m)^task-type:\s*([A-Za-z_-]+)', text) or [None, ''])[1].casefold(), '')
    if not use:
        known = type_use_cases(theme, level).get(plain_type(kind), [])
        use = known[0] if len(known) == 1 else ''
    fields = [(level + ' type', kind)] + ([('Use case', use)] if use else [])
    return '<dl class="job-identity">' + ''.join(
        '<div><dt>' + label + '</dt><dd>' + frame.esc(value) + '</dd></div>' for label, value in fields) + '</dl>'


def job_identity_html(theme: str, folder: Path, root: Path, data: dict) -> str:
    """Name the actual Job presentation and its explicitly authored use case."""
    if page_level(folder) != 'Job' or (theme not in WORK_SHAPE and theme != 'paper'):
        return ''
    if page_module(theme, folder, root)[1] == 'prototype_':
        return ''
    kind = {'work': '🧩 Job', 'discovery': '🔎 Inquiry Job',
            'cowork': '👥 People' if folder.name == 'j00_people' else '🤝 Collaboration Job'}.get(theme)
    if theme == 'paper':
        from live import paper_jobs
        kind = paper_jobs.job_type_label(folder)
    if not kind:
        return ''
    fields = [('Job type', kind)]
    if data.get('use_case'):
        fields.append(('Use case', data['use_case']))
    return '<dl class="job-identity">' + ''.join(
        '<div><dt>' + label + '</dt><dd>' + frame.esc(value) + '</dd></div>' for label, value in fields) + '</dl>'
