"""Draft Task views use the common supporting sections without copying records."""
from pathlib import Path

from live import focus_draft, draft_steps, focus_page as f, skills_section
from live import work_frame as shared_frame


VIEW_SKILLS = {
    'plan': 'hai-draft-logic', 'write': 'hai-draft-writing',
    'evidence': 'hai-evidence', 'display': 'hai-display',
    'revise': 'hai-draft-review', 'draft': 'hai-draft-writing', 'text': 'hai-draft',
    'overview': 'hai-draft', 'standing': 'hai-draft-workflow',
    'runs': 'hai-run',
}


def scope(folder, root, view, topics, every, knows):
    view = shared_frame.view_key(view) if view else None
    selected = shared_frame.shared_scope(folder, root, view, topics, every, knows)
    if not view:
        return selected
    # Native Draft Run families predate view metadata. Explicit view/topic
    # ownership always wins; unknown and unassigned records remain on the rail.
    title = dict(focus_draft.WORK).get(view) or dict(zip(('write', 'revise'), focus_draft.DRAFT)).get(view)
    prefixes = focus_draft.RUN_PREFIX.get(title, ())
    all_scope = shared_frame.shared_scope(folder, root, None, topics, every, knows)
    records = {row['path']: row for row in every if row.get('page') == folder}
    for run, card in all_scope['cards'].items():
        record = records.get(run, {})
        target_topic = f.interaction_topic(str(card.get('target') or card.get('for') or ''), folder)
        if card.get('view') or target_topic or record.get('view') or record.get('topic'):
            continue
        if run.parent != folder / 'runs':
            continue
        if view == 'runs' or run.name.startswith(prefixes):
            if run not in selected['runs']:
                selected['runs'].append(run)
                selected['cards'][run] = card
            for key in ('interactions', 'knows'):
                for row in all_scope[key]:
                    if row.get('path') == run and row not in selected[key]:
                        selected[key].append(row)
    # Sources displayed by the step itself, separate from scoped context records.
    sources = [f.frame.face(folder)]
    if view in ('plan', 'write', 'draft', 'evidence', 'display', 'revise', 'text', 'overview'):
        sources += list((folder / 'draft').glob('*.md'))
    if view in ('plan', 'revise', 'draft'):
        sources += [folder / 'draft' / 'records']
    if view in ('evidence', 'text'):
        sources += [folder / 'evidence']
    if view == 'display':
        sources += [folder / 'display']
    selected['source_paths'] = [p for p in sources if p and p.exists() and f.inside(p, root)]
    selected['ui_sources'] = [Path(__file__), Path(focus_draft.__file__), Path(draft_steps.__file__)]
    return selected


def skill_rows(folder, root, level, view, selected):
    if not view:
        return skills_section.relevant(folder, 'paper', level, list(VIEW_SKILLS.values()),
                                       topics=bool(selected['topics']),
                                       inbox=bool(selected['interactions']), limit=None)
    rows = [(VIEW_SKILLS.get(shared_frame.view_key(view), 'hai-draft'), 'this view')]
    rows += [(str(card.get('skill') or ''), 'linked Run') for card in selected['cards'].values()]
    if selected['topics']:
        rows.append(('hai-studio', 'linked Topics'))
    if selected['interactions']:
        rows.append(('hai-interaction', 'linked Interactions'))
    seen = set()
    return [(name, why) for name, why in rows
            if name in skills_section.catalog() and not (name in seen or seen.add(name))]


def shared_bodies(folder, root, theme, level, view, topics, own, knows, events, every, only=None):
    selected = scope(folder, root, view, topics, every, knows)
    bodies = shared_frame.shared_bodies(folder, root, theme, level, view, topics, own, knows, events, every,
                                       only=only, scope=selected,
                                       skill_rows=skill_rows(folder, root, level, view, selected))
    if not view and 'studio' in bodies:
        body, word = bodies['studio']
        bodies['studio'] = (focus_draft.studio_top(folder, root) + body, word)
    return bodies


def shared(folder, root, theme, level, view, topics, own, knows, events, every):
    bodies = shared_bodies(folder, root, theme, level, view, topics, own, knows, events, every)
    return ''.join(shared_frame.section(0, title, *bodies[key]) for key, title in shared_frame.SHARED
                   if not shared_frame.blank(bodies[key][0]))   # an empty section is hidden (JL 261113)
