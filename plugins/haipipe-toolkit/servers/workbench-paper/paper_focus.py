"""Paper Board content in the common Report and supporting-section frame.

The paper keeps its seven views. View ownership comes from explicit metadata or
the existing paper Topic roles, never from an unassigned record's folder name.
Versions and draft Sections retain their specialist workflows.
"""
from pathlib import Path
import re

from live import board_read, board_results, board_views, board_process
from live import focus_page as f, skills_section, work_frame as shared_frame


def context_topics(board, root, topics):
    """Adapt existing paper Topic roles without editing their source records."""
    roles = {topic: key for key, _, _ in board_read.BOARD_VIEWS
             for _, _, topic in board_read.view_topics(board, key)}
    related = board_read.board_topic(board, 'related', board_read.RELATED)
    if related:
        roles.setdefault(related, 'story')
    for topic, _, _ in topics:
        if re.search(r'-paper-displays?\b|-display-examples', topic.name):
            roles.setdefault(topic, 'displays')
    names = {'writing': 'draft', 'support blocks': 'explore', 'data + paper plan': 'plan'}
    out = []
    for topic, drawings, facts in topics:
        tags = [names.get(shared_frame.view_key(tag), shared_frame.view_key(tag))
                for tag in facts.get('tags', [])]
        if topic in roles and not any(tag in board_process.VIEW_SKILLS for tag in tags):
            tags.append(roles[topic])
        out.append((topic, drawings, {**facts, 'tags': tags}))
    return out


def scope(board, root, view, topics, every, knows):
    view = shared_frame.view_key(view) if view else None
    result = shared_frame.shared_scope(board, root, view, context_topics(board, root, topics), every, knows)
    selected = {row[0] for row in result['topics']}
    result['topics'] = [row for row in topics if row[0] in selected]
    if view:
        sources = [Path(__file__), Path(board_views.__file__), Path(board_results.__file__),
                   Path(board_read.__file__), Path(board_process.__file__)]
        if view == 'evidence':
            sources += [Path(__file__).with_name(name) for name in ('board_evidence.py', 'evidence_read.py')]
        elif view == 'draft':
            sources.append(Path(__file__).with_name('paper_version.py'))
        result['ui_sources'] = sources
    return result


def skill_rows(board, root, level, view, selected):
    if not view:
        names = [name for rows in board_process.VIEW_SKILLS.values() for name, _ in rows]
        return skills_section.relevant(board, 'paper', level, names, topics=bool(selected['topics']),
                                       inbox=bool(selected['interactions']), limit=None)
    rows = list(board_process.VIEW_SKILLS.get(shared_frame.view_key(view), ()))
    rows += [(str(card.get('skill') or ''), 'linked Run') for card in selected['cards'].values()]
    rows += [(f.TYPE_SKILLS.get(f.frame.task_type(page), ''), 'linked Task')
             for page in selected['pages'] if f.page_level(page) == 'Task']
    if selected['topics']:
        rows.append(('haipipe-studio', 'linked Topics'))
    if selected['interactions']:
        rows.append(('haipipe-interaction', 'linked Interactions'))
    seen = set()
    return [(name, why) for name, why in rows
            if name in skills_section.catalog() and not (name in seen or seen.add(name))]


def shared_bodies(folder, root, theme, level, view, topics, own, knows, events, every, only=None):
    selected = scope(folder, root, view, topics, every, knows)
    return shared_frame.shared_bodies(folder, root, theme, level, view, topics, own, knows, events, every,
                                     only=only, scope=selected,
                                     skill_rows=skill_rows(folder, root, level, view, selected))


def shared(folder, root, theme, level, view, topics, own, knows, events, every):
    bodies = shared_bodies(folder, root, theme, level, view, topics, own, knows, events, every)
    return ''.join(shared_frame.section(0, title, *bodies[key]) for key, title in shared_frame.SHARED)


def report_views(board, root):
    """Keep content and authorized actions together; Studio is rendered once below."""
    md = lambda text, base: f.markdown(text, base, root)
    items = f.interactions(board, root)
    views = board_views.board_report_views(board, root, md, items)
    views.setdefault('draft', ('Writing', None))

    def build(key):
        if key in ('idea', 'story'):
            result = getattr(board_results, key + '_view')(board, root, md, items, studio=False)
        else:
            result = board_views._results(board, key, root, md, items)
        # Plan's auxiliary drawings now live in the shared Studio section.
        result = result.partition('<hr class=pb-rule>')[0]
        process = board_process.process_html(board, key, root, md, items, True)
        offset = max(0, f.IX.next_number(result) - 1)
        process = re.sub(r'(<h3 class=fd-h>)(\d+) · ',
                         lambda m: m[1] + str(int(m[2]) + offset) + ' · ', process)
        body = (board_views.CSS + board_views.BOARD_CSS + board_views.VERSION_CSS + board_views.PB_CSS
                + board_views.SIDE_CSS + board_views.PAGE_CSS + result + process + board_views.PB_JS + board_views.JS)
        return '<h2>📋 Review Content</h2>' + body

    from live.address_links import linked_views, page_linker
    return linked_views({key: (name, lambda k=key: build(k)) for key, (name, _) in views.items()},
                        page_linker(board, root))
