"""The work family's four live views and shared, unnumbered sections.

Reads existing page faces, Question work links, Runs, and Studio records. No UI
state is saved as execution state and viewing a page never creates records.
"""
from pathlib import Path
import re

from live import frame
from live.ui_parts import PB_CSS, PB_JS, _side_tabs, word_span, icon_label


def api():
    from live import focus_page
    return focus_page


def empty(message):
    return '<p class="mut">' + frame.esc(message) + '</p>'


def section(n, title, body, word=''):
    title = (f'{n} · ' if n else '') + title
    return ('<details class=band-sec><summary>' + icon_label(title) + word_span(word)
            + '</summary><div class=band-jobs>' + body + '</div></details>')


def source_link(path, root, label='Open source ↗'):
    f = api()
    if not path or not f.inside(path, root) or not path.exists():
        return ''
    href = f.page_url(path, root) if path.is_dir() else frame.reader(path, root)
    return f'<p><a href="{frame.esc(href)}">{frame.esc(label)}</a></p>'


def topics_for(folder, root, questions):
    """Question groups with explicit work links; otherwise existing bands/children.

    Keep unlinked work reachable, reject references outside this page, and reuse
    the very same groups for Overview's map and Status's navigation.
    """
    f = api()
    groups = {}
    for q in questions:
        paths = [p for p in f.work_paths(q, folder, root) if p == folder or folder in p.parents]
        if not paths:
            continue
        name = str(q.get('group') or q.get('title') or q.get('question') or q.get('id') or 'Work')
        groups.setdefault(name, [])
        groups[name] += [p for p in paths if p not in groups[name]]
    children = [p for p in f.kids(folder) if f.inside(p, root) and f.page_level(p) in ('Job', 'Task')]
    if groups:
        leaves = [p for c in children for p in (f.kids(c) or [c])] if f.page_level(folder) == 'Block' else children
        covered = [p for paths in groups.values() for p in paths]
        remaining = [p for p in leaves if not any(p == c or c in p.parents for c in covered)]
        if remaining:
            groups.setdefault('Other Work', []).extend(p for p in remaining if p not in groups.get('Other Work', []))
    else:
        face = frame.face(folder)
        text = face.read_text(encoding='utf-8') if face and f.inside(face, root) else ''
        bands = dict(re.findall(r'\bj(\d)N\s+([^·\n]+)', (re.search(r'(?m)^bands:\s*(.+)$', text) or [None, ''])[1]))
        for p in children:
            name = bands.get(p.name[1:2], '').strip() or f.page_title(p)
            groups.setdefault(name, []).append(p)
    return list(groups.items()) or [(f.page_title(folder), [folder])]


def tree(folder, paths, root):
    """A pruned real B–J–T–R tree; selecting one Task never includes its siblings."""
    f = api()
    def relevant(p):
        return any(p == t or p in t.parents or t in p.parents for t in paths)
    def node(p):
        level = f.page_level(p)
        d = f.read_face(p, root)
        state = f.state_words(f.state_label(d['state'])) or 'No state recorded'
        label = f'{level} · {f.page_title(p)}'
        link = f'<a data-pop="{frame.esc(label)}" href="{frame.esc(f.page_url(p, root))}">{frame.esc(label)}</a>'
        below = ''
        if level in ('Block', 'Job'):
            below = ''.join(node(c) for c in f.kids(p) if f.inside(c, root) and relevant(c))
        if level in ('Block', 'Task', 'Job'):
            runs = [row for row in f.run_rows(p) if relevant(row[0])]
            if level == 'Task' and any(t == p or t in p.parents for t in paths) and (output := f.output_of(p, root)):
                below += '<li>' + output + '</li>'
            for run, mark, headline in runs:
                if not f.inside(run, root):
                    continue
                below += (f'<li><a data-pop="{frame.esc(run.name)}" href="{frame.esc(f.run_url(run, root))}">{frame.esc(run.name)}</a>'
                          f' <span class="st">{frame.esc(mark)}</span>'
                          + (f'<p>{frame.esc(headline)}</p>' if headline else '') + '</li>')
            if not runs and level == 'Task':
                below = '<li>No Run yet.</li>'
        row = link + f' <span class="st">{frame.esc(state)}</span>'
        return ('<li><details><summary>' + row + '</summary><ul>' + below + '</ul></details></li>') if below else '<li>' + row + '</li>'
    context = frame.chain(folder, root)
    parents = [context.get(k) for k in ('Block', 'Job')]
    heading = ' / '.join(f'<a data-pop="{frame.esc(f.page_title(p))}" href="{frame.esc(f.page_url(p, root))}">{frame.esc(f.page_title(p))}</a>'
                         for p in parents if p and p != folder and f.inside(p, root))
    return (f'<p>{heading}</p>' if heading else '') + '<ul class="work-topic-tree">' + node(folder) + '</ul>'


def map_html(folder, root, groups):
    f = api()
    mm = frame.mindmap_module()
    import mmbuild as build
    import mmtree as model
    branches = []
    for i, (name, paths) in enumerate(groups):
        children = [build.built(str(p), f'[{p.name}] {f.page_title(p)}') for p in paths if p != folder]
        branches.append(build.built(f'{folder}/topic/{i}', name, children))
    diagram = model.MindMap({'mindmap': '1', 'title': folder.name, 'built': 'work-topics'},
                           build.built(str(folder), folder.name, branches))
    # Preserve the existing richer map (Questions, Studio and Runs) as well.
    diagram.root.id = 'root'
    return '<style>' + f.FIT_MAP + '</style><div class="focus-map fit-map">' + f.map_html(mm.draw(diagram, '', editable=False), folder, root) + '</div>'


def requirements(folder, root, data, questions):
    f = api()
    content = data['sections'].get('requirements', '')
    body = f.markdown(content, folder, root) if content else ''
    if data['close']:
        body += f.markdown(data['close'], folder, root)
    for q in questions:
        if q.get('acceptance'):
            body += '<p><b>' + frame.esc(str(q.get('title') or q.get('id') or 'Requirement')) + '</b></p>'
            body += f.markdown(str(q['acceptance']), folder, root)
    return body or empty('No requirements recorded yet.')


def overview(folder, root, data, questions, groups):
    f = api()
    # Both maps are live: Topic navigation and the original complete work map.
    maps = _side_tabs('work-overview-map', [('Topics', ''), ('Work Structure', '')],
                     [map_html(folder, root, groups), f.parts_mindmap(folder, root)])
    return (section(1, '🎯 Goal', f.markdown(data['goal'], folder, root) if data['goal'] else empty('No goal recorded yet.'))
            + section(2, '📋 Requirements', requirements(folder, root, data, questions))
            + section(3, '🧠 MindMap', maps))


def status(folder, root, data, groups):
    """Status, topic-based B–J–T–R navigation, and recorded dependencies."""
    f = api()
    level = f.page_level(folder)
    body = f.status_now_html(folder, root, level, []) or f.state_lead(folder, root, level)   # it carries the lead line
    n = f.IX.next_number(body) or 1
    panels = [tree(folder, paths, root) for _, paths in groups]
    body += section(n, '🧩 View BJTR', _side_tabs('work-status-topic', [(name, '') for name, _ in groups], panels))
    n += 1
    dependencies = data['sections'].get('dependencies', '')
    if dependencies:
        body += section(n, '🔗 Dependencies', f.markdown(dependencies, folder, root))
    return body


def delivery(folder, root, data):
    f = api()
    tabs = f.own_delivery_tabs(frame.theme_of(folder, root), folder, root, f.page_level(folder))
    # Keep uncategorized outputs and authored handoff records reachable, without
    # calling delivery_html (which repeats the theme tabs and service previews).
    for directory, where in f.delivery_sources(folder, root):
        record = directory / 'delivery.md'
        if record.is_file() and f.inside(record, root):
            tabs.append((where + ' · Record', '', f.markdown(record.read_text(encoding='utf-8'), directory, root)))
        else:
            entries = [p for p in sorted(directory.iterdir()) if not p.name.startswith('.') and f.inside(p, root)]
            if entries:
                listing = '<ul>' + ''.join(f'<li><a href="{frame.esc(frame._file_url(p, root))}">{frame.esc(p.name)}</a></li>' for p in entries) + '</ul>'
                tabs.append((where + ' · Files', '', listing))
    files = _side_tabs('work-delivery', [(n, w) for n, w, _ in tabs], [b for _, _, b in tabs]) if tabs else ''
    if service := f.service_section(folder, root):
        files += service
    acceptance = data['sections'].get('acceptance', '')
    usage = data['sections'].get('usage', '')
    return (section(1, '📦 Deliverables', files or empty('Nothing handed over yet.'))
            + section(2, '✅ Acceptance', f.markdown(acceptance, folder, root) if acceptance else empty('No acceptance recorded yet.'))
            + section(3, '📖 Usage', f.markdown(usage, folder, root) if usage else empty('No usage notes recorded yet.')))


def recorded_sections(folder, root, topics, names, include_page=True):
    """Read explicit sections, including Studio's legacy underlined headings."""
    f = api()
    records = []
    candidates = [(data['face'], data['sections']) for data in [f.read_face(folder, root)] if data['face']] if include_page else []
    for topic, _, _ in topics:
        face = frame._notes(topic)
        if face and f.inside(face, root):
            text = face.read_text(encoding='utf-8')
            candidates.append((face, f.face_parts(text)))
    for face, parts in candidates:
        found = [f.part(parts, name) for name in names]
        text = '\n\n'.join(dict.fromkeys(p for p in found if p))
        if text:
            records.append((face, text))
    return records


DECISION_ID = re.compile(r'(?m)^(?=[a-z]\d{2}-D\d{2} · )')
# A tag is shown only when the entry's own words say it; nothing is inferred from a quote or a date.
DECISION_TAGS = (('Replaced', re.compile(r'Replaced by [a-z]\d{2}-D\d{2}')),
                 ('Waiting', re.compile(r'\bwaits? for\b')),
                 ('Proposed', re.compile(r'\bopen proposals?\b|\bProposed by\b|decided for this round')))


def decision_headline(body, cap=110):
    """The entry's first clause, cut at a colon, semicolon, bracket or full stop; the rest stays in its fold."""
    plain = re.sub(r'`([^`]*)`', r'\1', ' '.join(body.split()))
    cut = re.search(r'.{15,}?(?=: |; | \(|\. )', plain)
    head = cut.group(0) if cut else plain
    return head if len(head) <= cap else head[:cap].rsplit(' ', 1)[0] + '…'


def decision_list(text, base, root):
    """One closed row per `sNN-DNN · …` entry: its number, its headline and a tag its words carry; any other text
    (a heading's lead-in, a list) keeps its Markdown."""
    f = api()
    out, rows = [], []
    for chunk in DECISION_ID.split(text):
        chunk = chunk.strip()
        if not chunk:
            continue
        found = re.match(r'([a-z]\d{2}-D\d{2}) · (.*)', chunk, re.S)
        if not found:
            if rows:
                out.append('<ul class=wk-dec>' + ''.join(rows) + '</ul>')
                rows = []
            out.append(f.markdown(chunk, base, root))
            continue
        did, body = found.groups()
        lead, _, tail = body.partition('\n\n')       # a list or note after the entry is its own block
        tag = next((name for name, rx in DECISION_TAGS if rx.search(lead)), '')   # the first that holds
        tags = f'<span class=wk-dec-tag>{tag}</span>' if tag else ''
        rows.append(f'<li><details><summary><span class=wk-dec-id>{frame.esc(did)}</span>'
                    f'<span class=wk-dec-head>{frame.esc(decision_headline(lead))}</span>{tags}</summary>'
                    f'<div class=wk-dec-body>{f.markdown(lead, base, root)}</div></details></li>')
        if tail.strip():
            out.append('<ul class=wk-dec>' + ''.join(rows) + '</ul>')
            rows = []
            out.append(f.markdown(tail, base, root))
    if rows:
        out.append('<ul class=wk-dec>' + ''.join(rows) + '</ul>')
    return ''.join(out)


def records_html(records, root, eid):
    f = api()
    from live import studio_tabs                     # a topic carries the same name here as in Studio
    return _side_tabs(eid, [(studio_tabs.topic_label(f.face_title(p) or p.stem), '') for p, _ in records],
                      [decision_list(text, p.parent, root) + source_link(p, root) for p, text in records]) if records else ''


def timeline(folder, root, events, interactions, decisions, pages=None, view=None, runs=None):
    """Dated history with a link to its source; undated facts remain in their own sections."""
    f = api()
    rows = []
    # The legacy reader's origin is a display label, not a file path. Keep its
    # page-wide commits; resolve other records from their actual files below.
    rows += [(day, 'Change', words, folder) for day, kind, words, _ in events if kind == 'commit' and not view]
    selected_runs = [] if runs is None else list(runs)
    for page in (f.rollup(folder) if pages is None else pages):
        if not f.inside(page, root):
            continue
        data = f.read_face(page, root)
        for day, _, words in f.log_events(data['sections'].get('log', '')):
            if data['face']:
                rows.append((day, 'Log', words, data['face']))
        if runs is None:
            selected_runs += [r for r, _, _ in f.run_rows(page) if f.inside(r, root)]
    for run in dict.fromkeys(selected_runs):
        if f.inside(run, root):
            receipt = run / 'result' / 'runtime.yaml'
            if not f.inside(receipt, root) or not receipt.is_file():
                continue
            card = f._yaml(receipt)
            for field, kind in (('started_at', 'Run started'), ('finished_at', 'Run finished')):
                date = re.search(r'\d{4}-\d{2}-\d{2}', str(card.get(field, '')))
                if date:
                    words = run.name + (' · ' + str(card.get('status') or '') if field == 'finished_at' else '')
                    rows.append((date[0], kind, words, receipt))
    for directory, _ in (f.delivery_sources(folder, root) if not view or view == 'delivery' else []):
        record = directory / 'delivery.md'
        if record.is_file() and f.inside(record, root):
            for line in record.read_text(encoding='utf-8').splitlines():
                date = re.search(r'\b(20\d{2}-\d{2}-\d{2})\b', line)
                if date:
                    rows.append((date[1], 'Delivery record', line.strip(), record))
    for item in interactions:
        date = re.search(r'\d{4}-\d{2}-\d{2}', str(item.get('received', '')))
        if date and item.get('answers'):
            rows.append((date[0], 'Feedback', item['title'], item['answers']))
        for q, (state, date, note) in item.get('applied', {}).items():
            rows.append((date, 'Feedback applied' if state == 'applied' else 'Feedback in progress', q + ' · ' + note, item['path'] / 'applied.md'))
    for source, text in decisions:
        for line in text.splitlines():
            date = re.search(r'\b(20\d{2}-\d{2}-\d{2})\b', line)
            if date:
                # Legacy Decided sections mix decisions, proposals and review notes.
                # A heading or a quoted date is not evidence of an approved decision.
                if re.match(r'\s*(?:[-*]\s+)?[\w-]+-D\d+\b', line):
                    rows.append((date[1], 'Decision note', line.strip(), source))
    mod, prefix = f.page_module(frame.theme_of(folder, root), folder, root)
    history = getattr(mod, prefix + 'history', None) if mod else None
    if history and not view:
        rows += [r for r in history(folder, root, f.page_level(folder)) if f.inside(r[3], root)]
    rows = sorted(set(rows), key=lambda x: (x[0], x[1], x[2]), reverse=True)
    if not rows:
        return empty('No dated events linked to this view.' if view else 'No dated events recorded yet.')
    return '<ol class="work-history" aria-label="' + f.page_level(folder) + ' history">' + ''.join(
        f'<li><time>{frame.esc(day)}</time> <b>{frame.esc(kind)}</b><p>{frame.esc(words)}</p>'
        + source_link(source, root, 'Open page ↗' if source.is_dir() else 'Open source ↗')
        + '</li>' for day, kind, words, source in rows[:f.TIMELINE_MAX]) + '</ol>'


SHARED = (
    ('studio', '🎨 Studio'), ('interactions', '🙋 Interactions'),
    ('decisions', '⚖️ Decisions'), ('know', '📚 Things to Know'),
    ('checklist', '📝 Checklist'), ('timeline', '🕒 Timeline'),
    ('skills', '🧰 Skills'), ('files', '📁 Files'),
)


def view_key(value):
    value = str(value or '').strip().casefold().removeprefix('report-').removeprefix('work-')
    return {'mindmap': 'overview', 'status': 'standing', 'block ui': 'ui-block',
            'job ui': 'ui-job', 'task ui': 'ui-task', 'run ui': 'ui-run'}.get(value, value)


def scoped_topics(topics, view, root=None):
    """Only an explicit View or a matching Topic tag belongs in a View."""
    if not view:
        return topics
    selected = []
    for row in topics:
        explicit = api().read_face(row[0], root).get('view') if root else row[2].get('view')
        if (view_key(explicit) == view_key(view) if explicit else
                view_key(view) in {view_key(tag) for tag in row[2].get('tags', [])}):
            selected.append(row)
    return selected


def shared_scope(folder, root, view, topics, every, knows):
    """One selection shared by every supporting section; no child-to-Status fallback, except what waits on the person."""
    f = api()
    within = lambda p: p is not None and f.inside(Path(p), root) and (Path(p) == folder or folder in Path(p).parents)
    all_pages = [p for p in f.rollup(folder) if within(p)]
    # topic_rows already resolves ownership, including legacy Studio topics stored at an ancestor.
    topics = [row for row in topics if f.inside(row[0], root)]
    selected_topics = scoped_topics(topics, view, root)
    topic_paths = {row[0] for row in selected_topics}
    pages = []
    def matches(item):
        if not view:
            return True
        if item.get('view'):
            return view_key(item['view']) == view_key(view)
        if item.get('topic') is not None:
            return Path(item['topic']) in topic_paths
        return item.get('page') in pages
    for page in all_pages:
        data = f.read_face(page, root)
        if not view or matches({'view': data.get('view'),
                                'topic': f.interaction_topic(data.get('topic_ref'), page)}):
            pages.append(page)
    interactions = [r for r in every if within(r.get('page')) and matches(r)]
    if view_key(view) == 'standing':   # Status is where things stand: what still waits on the person shows here too, so its
        interactions += [r for r in every if within(r.get('page')) and r.get('state') == 'waiting'   # rows' 🙋 Interaction
                         and not r.get('view') and r not in interactions]   # and this list agree (261109); a form that names
                                                                            # another view by `view:` stays there
    notes = [r for r in knows if within(r.get('page')) and matches(r)]
    interaction_runs = {r['path']: r for r in every if within(r.get('page'))}
    runs, cards = [], {}
    for page in all_pages:
        for run, _, _ in f.run_rows(page):
            if not within(run):
                continue
            card = f._yaml(run / 'run.yaml')
            item = interaction_runs.get(run, {'page': page, 'view': card.get('view'),
                    'topic': f.interaction_topic(str(card.get('target') or card.get('for') or ''), page)})
            if matches(item):
                runs.append(run)
                cards[run] = card
    return dict(topics=selected_topics, pages=pages, runs=runs, cards=cards,
                interactions=interactions, knows=notes)


def scope_skills(folder, root, theme, level, view, scope):
    from live import skills_section as skills
    f = api()
    if not view:
        names = [n for rows in f.VIEW_SKILLS.values() for n, _ in rows] + f.type_skills(folder, root)
        return skills.relevant(folder, theme, level, names, topics=bool(scope['topics']),
                               inbox=bool(scope['interactions']), limit=None)
    rows = list(f.VIEW_SKILLS.get(view_key(view), ()))
    if view_key(view).startswith('ui-'):
        rows += [('haipipe-ui', 'this view')]
    rows += [(f.TYPE_SKILLS.get(frame.task_type(p), ''), 'linked Task')
             for p in scope['pages'] if f.page_level(p) == 'Task']
    rows += [(str(card.get('skill') or ''), 'linked Run') for card in scope['cards'].values()]
    if scope['topics']:
        rows += [('haipipe-studio', 'linked Topics')]
    if scope['interactions']:
        rows += [('haipipe-interaction', 'linked Interactions')]
    seen = set()
    return [(name, why) for name, why in rows
            if name in skills.catalog() and not (name in seen or seen.add(name))]


def shared_bodies(folder, root, theme, level, view, topics, own, knows, events, every, only=None, *, scope=None, skill_rows=None):
    """One renderer for view context and the unfiltered right-rail destination."""
    f = api()
    view = view_key(view) if view else None
    scope = shared_scope(folder, root, view, topics, every, knows) if scope is None else scope
    topics, pages = scope['topics'], scope['pages']
    skill_rows = scope_skills(folder, root, theme, level, view, scope) if skill_rows is None else skill_rows
    from live import skills_section, work_files
    file_options = dict(scope=scope, skill_rows=skill_rows)
    if only == 'files':
        return {'files': (work_files.render(folder, root, view, topics, pages, **file_options), '')}
    def records(names):
        rows = [row for page in pages for row in recorded_sections(page, root, [], names)]
        rows += recorded_sections(folder, root, topics, names, include_page=False)
        return list(dict.fromkeys(rows))
    decisions = records(('decisions', 'decision', 'decided'))
    checklist = records(('checklist',))
    checklist_html = records_html(checklist, root, 'work-checklist')
    if not view or view.startswith('ui-'):
        checklist_html += f.ui_walk_checklist(folder, root, view)
    know_records = records(('things to know',))
    visible_knows = scope['knows']
    know = f.standard_interactions(visible_knows, folder, root, title='Notes') if visible_knows else ''
    know += records_html(know_records, root, 'work-notes')
    asks = [r for r in scope['interactions'] if r.get('state') != 'to know']
    studio = f.studio_html(topics, root, '', asks, tabs=True) if topics else (empty('No Topics linked to this view.') if view else f.studio_none(folder, root))
    interaction = f.IX.interaction_section(asks, root, 0, lambda r: f.interaction_where(r, folder, root), plain=False, body_only=True)
    rest = [r for r in asks if r.get('form') is None or not r.get('asks')]
    if rest:
        interaction += _side_tabs('work-interaction-record-', [(r['title'], '') for r in rest],
                                  [f.interaction_item(r, folder, root) + (source_link(r['path'] / 'question_collection.md', root, 'Open questions ↗')
                                   if not r.get('form') and not r.get('answers') else '') for r in rest])
    interaction = interaction or (empty('No Interactions linked to this view.') if view else f.IX.NONE_YET)
    word, _ = f.IX.state_word(asks) if asks else ('', '')
    notes = records_html(decisions, root, 'work-decisions') or empty('No Decisions linked to this view.' if view else 'No decision records yet.')
    history = timeline(folder, root, events, asks, decisions, pages=pages, view=view, runs=scope['runs'])
    return {
        'studio': (studio, ''), 'interactions': (interaction, word),
        'decisions': (notes, ''), 'know': (know or empty('No notes linked to this view.' if view else 'No notes recorded yet.'), ''),
        'checklist': (checklist_html or empty('No Checklist linked to this view.' if view else 'No checklist recorded yet.'), ''),
        'timeline': (history, ''),
        'skills': ((skills_section.skills_html(folder, root, theme, level, rows=skill_rows) if skill_rows else empty('No Skills linked to this view.' if view else 'No Skills recorded yet.')), ''),
        'files': (work_files.render(folder, root, view, topics, pages, **file_options) if not only else '', ''),
    }


def shared(folder, root, theme, level, view, topics, own, knows, events, every, **options):
    bodies = shared_bodies(folder, root, theme, level, view, topics, own, knows, events, every, **options)
    return ''.join(section(0, title, *bodies[key]) for key, title in SHARED)


STYLE = '''<style>
.work-section-group+.work-section-group{margin-top:28px}
.work-section-group>h2{display:flex;align-items:center;gap:12px;font-size:17px;font-weight:600;color:var(--ink);margin:22px 0 10px}
.work-section-group>h2::after{content:"";flex:1;border-top:1px solid var(--line)}
.work-topic-tree,.work-topic-tree ul{list-style:none;padding-left:16px;margin:8px 0}
.work-topic-tree{padding-left:0}.work-topic-tree li{margin:8px 0;overflow-wrap:anywhere}
.work-topic-tree summary{cursor:pointer}.work-topic-tree .st{font-size:12px;color:var(--muted);margin-left:8px}
.work-history{list-style:none;padding:0}.work-history li{border-left:2px solid var(--line);padding:0 14px 16px;margin:0}
.work-history time{font-size:13px;margin-right:8px}.work-history p{margin:4px 0}
.wk-dec{list-style:none;margin:0;padding:0}.wk-dec li{border-bottom:1px solid var(--line)}.wk-dec li:last-child{border-bottom:0}
.wk-dec summary{cursor:pointer;display:flex;align-items:baseline;gap:10px;padding:9px 2px;line-height:1.45}
.wk-dec-id{flex:none;font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;min-width:62px}
.wk-dec-head{flex:1;min-width:0}.wk-dec-tag{flex:none;font-size:11.5px;padding:1px 8px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.wk-dec-body{margin:0 0 10px 72px;font-size:14px;color:var(--muted);overflow-wrap:anywhere}.wk-dec-body p{margin:4px 0}
@media(max-width:600px){.wk-dec-body{margin-left:0}.wk-dec summary{flex-wrap:wrap}}
</style>'''
