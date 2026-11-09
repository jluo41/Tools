"""Design Blocks in the shared Report frame; Job and Task workflows stay specialized.

Supporting records belong to a view only through explicit view or Topic metadata.
The existing design reader remains the authority for results, next Runs and signs.
"""
from pathlib import Path
import re

from live import design_focus as D, design_reader, design_views, design_canvas
from live import focus_page as f, skills_section, work_frame as shared_frame


def applies(folder):
    return D.level_of(folder) == 'Block'


def scope(folder, root, view, topics, every, knows):
    selected = shared_frame.shared_scope(folder, root, view, topics, every, knows)
    if view:
        selected['ui_sources'] = [Path(module.__file__) for module in
                                  (D, design_reader, design_views, design_canvas)] + [Path(__file__)]
    return selected


def skill_rows(folder, root, level, view, selected):
    key = shared_frame.view_key(view) if view else None
    support = {**D.VIEW_SKILLS, 'overview': (('haipipe-mindmap', 'the design ladder'),)}
    if key is None:
        names = [name for k, _ in D.BLOCK_VIEWS for name, _ in support[k]] + ['haipipe-mindmap']
        return skills_section.relevant(folder, 'design', level, names, topics=bool(selected['topics']),
                                       inbox=bool(selected['interactions']), limit=None)
    rows = list(support.get(key, ()))
    rows += [(str(card.get('skill') or ''), 'linked Run') for card in selected['cards'].values()]
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


def report_views(folder, root):
    """Reuse the design content and actions, numbered once under Review Content."""
    def build(key):
        if key == 'mindmap':
            content = f.parts_mindmap(folder, root)
        else:
            _, lead, process, results, after = D.block_view(folder, root, key)
            # The action section owns the pending instruction; keep result state words.
            if process:
                results = re.sub(r'<p class=fd-wait>.*?</p>', '', results, flags=re.S)
            content = lead + D._numbered(results + process) + after
        return ('<h2>📋 Review Content</h2>' + D._head_css() + content
                + D.PB_JS + D.FD.JS + D.PROMPT_JS + D.POST_JS)

    from live.address_links import linked_views, page_linker
    return linked_views({key: (name, lambda k=key: build(k))
                         for key, name in (*D.BLOCK_VIEWS, ('mindmap', 'MindMap'))},
                        page_linker(folder, root))
