"""Insight source adapters; pages and maps are rendered by the shared Studio skills."""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'PRINCIPLE.md').is_file())
SHARED = ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts'
sys.path.insert(0, str(SHARED))
import block_types_pages as type_pages
from block_types_check import LEVELS, read_types

ABSENT = {'insight-board': set(), 'question-book': {'Job group type'},
          'data-prep': {'Job group type', 'Task group type'}}


def catalog(topic, kind):
    path = topic / 'types.md'
    if not path.is_file():
        raise ValueError(f'Missing type catalog: {path}')
    example, types = read_types(path)
    meta, absent, level, name = {}, {}, '', ''
    for line in path.read_text().splitlines():
        if line.startswith('## '):
            level, name = line[3:].strip(), ''
        elif line.startswith('### '):
            name = line[4:].strip()
        elif line.startswith('absent:') and not name:
            absent[level] = line.split(':', 1)[1].strip()
        elif name and re.match(r'^(source|owner):', line):
            key, value = line.split(':', 1)
            meta.setdefault((level, name), {})[key] = value.strip()
    if set(types) != set(LEVELS) or set(absent) != ABSENT[kind]:
        raise ValueError(f'{path}: four lists and the declared absent levels must match {kind}')
    for level in LEVELS:
        if level in absent:
            if types[level] or not absent[level]:
                raise ValueError(f'{path}: an absent level cannot contain a type')
            continue
        if not types[level]:
            raise ValueError(f'{path}: missing {level}')
        for name, row in types[level].items():
            row.update(meta.get((level, name), {}))
            if not all(row.get(k) for k in ('for', 'holds', 'source', 'owner')):
                raise ValueError(f'{path}: {name} needs for, holds, source and owner')
            for owner in row['owner'].split('; '):
                if not owner.startswith('plugins/') or not (ROOT / owner).is_file():
                    raise ValueError(f'{path}: missing owning skill {owner}')
    if not example or not (ROOT / example / 'board.md').is_file():
        raise ValueError(f'{path}: example must name a real Block')
    return {'example': example, 'types': types, 'absent': absent}


def outputs(topic):
    """Use the shared generator unchanged; it owns the type pages and their two views."""
    return type_pages.build(topic)


def views(topic):
    data = json.loads(outputs(topic)[topic / 'studio-views.json'])
    return [v for v in data['views'] if v['name'] in type_pages.VIEWS]


def classified(job, kind, contract):
    """Check semantic responsibilities against the catalog, not the directory's version number."""
    types = contract['types']
    if job['type'] not in types['Job type']:
        raise ValueError(f'Unlisted Job type: {job["type"]}')
    for task in job['tasks']:
        if task['type'] not in types['Task type']:
            raise ValueError(f'Unlisted Task type: {task["type"]}')
        group = task['group_type']
        if group and group not in types['Task group type']:
            raise ValueError(f'Unlisted Task group type: {group}')
        if not group and 'Task group type' not in ABSENT[kind]:
            raise ValueError(f'Missing Task group for {task["name"]}')


def organization(job, kind, node):
    """At most four levels. Stable source identities survive removal of redundant wrappers."""
    def seed(parent, role, value):
        return parent + '/' + role + '/' + value.split('examples/Project-Ladder/insight/', 1)[-1]

    board = kind == 'insight-board'
    top_seed = seed(kind, 'Question version' if board else 'Job Type', job['release'] if board else job['type'])
    job_seed = seed(top_seed, 'Job' if board else 'Job Name', job['source'])
    children, groups = [], {}
    for task in job['tasks']:
        # Identity roles are kept separate from the displayed roles and type names.
        identity_group = task['identity_group']
        group_seed = seed(job_seed, 'Task kind' if board else 'Task Type', identity_group)
        task_seed = seed(group_seed, 'Task' if board else 'Task Name', task['source'])
        member = node(task['name'], 'Task', path=task['source'])
        member.update(identity=task_seed, kept=task['kept'],
                      notes=['Type: ' + task['type']] + (['Runs: ' + ', '.join(task['runs'])] if task.get('runs') else []))
        if task['group_type']:
            label = task['group']
            if label not in groups:
                group = node(label, 'Task group')
                group.update(identity=group_seed, notes=['Group type: ' + task['group_type']])
                groups[label] = group
                children.append(group)
            groups[label]['children'].append(member)
        else:
            children.append(member)
    named = node(job['name'], 'Job', children, job['source'])
    named.update(identity=job_seed, notes=['Type: ' + job['type']])
    if board:
        top = node(job['release'], 'Job group', [named])
        top.update(identity=top_seed, notes=['Group type: Question version'])
        return top
    return named


def align_map_levels(old, kind, fresh):
    """Reparent the same nodes, then let shared refresh preserve authored words and branches."""
    if old.meta.get('organization-levels') == '2' or kind == 'insight-board':
        return

    def lift(parent, member_ids):
        out = []
        for wrapper in parent.children:
            if wrapper.id in member_ids or not wrapper.built:
                out.append(wrapper)
                continue
            promoted = [c for c in wrapper.children if c.id in member_ids]
            wrapper.children = [c for c in wrapper.children if c not in promoted]
            out.extend(promoted)
            if not promoted or wrapper.edited or wrapper.children:
                out.append(wrapper)
        parent.children = out

    jobs = {job.id: job for job in fresh.root.children}
    lift(old.root, set(jobs))
    if kind == 'data-prep':
        for job in old.root.children:
            if job.id in jobs:
                lift(job, {t.id for t in jobs[job.id].children})


def ordinary_bands():
    """Read the ordinary Work writer's numbering, not the Blueprint registry."""
    tree = ast.parse((SHARED / 'new_topic.py').read_text())
    return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == 'BANDS' for t in n.targets))


STUDIO_USES = {
    'insight-board': [('Research frame', 'Block'), ('Evidence by level', 'Task'),
                      ('Findings across Jobs', 'Block / Job'), ('Analysis and review', 'Task'), ('Reading this Board', 'Block')],
    'question-book': [('Question map', 'Block'), ('Question needs and method', 'Task'),
                      ('Version changes', 'Job'), ('Question review and release', 'Job / Task'), ('Maintaining the Book', 'Block')],
    'data-prep': [('Data conventions and chain', 'Block'), ('Step interfaces', 'Task'),
                  ('Preparation limits', 'Job'), ('Step code and review', 'Task'), ('Using this prep version', 'Block')],
}
STUDIO_BANDS = [('concept', '💡 Concept'), ('level', '🧩 Level'), ('report', '📊 Report'),
                ('procedure', '🪜 Task procedure'), ('guide', '🧭 Guide')]


def studio_rule(kind, name, r):
    numbers = ordinary_bands()
    bands, notes = [], {}
    for (key, label), (use, scope) in zip(STUDIO_BANDS, STUDIO_USES[kind]):
        lo, hi = numbers[key]
        title = f'{label} · s{lo:02d}–s{hi:02d}'
        topic = '〈' + use + '〉'
        bands.append(r(title, r(topic)))
        notes[title] = f'Ordinary Work {key} numbering. Create a topic only when the work needs it; keep existing identifiers.'
        notes[topic] = f'{scope} scope. A proposed topic responsibility, not a directory claimed to exist.'
    return r(name, *bands), notes


def actual_studio_band(owner, source):
    """Read the same configured bands, group order and tags as the Workbench."""
    from live import frame
    from live.frame_groups import studio_group_order
    from live.studio_tabs import studio_bands
    named = studio_bands(owner, ROOT)
    tags = frame._note_facts(source).get('tags') or []
    tags = [tags] if isinstance(tags, str) else tags
    decade = re.match(r's(\d)\d', source.parent.name)
    return (named.get(decade[1]) if decade else None) \
        or next((name for name in studio_group_order(owner) if name in tags), None) \
        or next(iter(tags), 'Other')
