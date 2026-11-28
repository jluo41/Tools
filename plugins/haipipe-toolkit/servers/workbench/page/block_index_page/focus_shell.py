"""The focus page's frame: the left and right rails and the page shell around a section."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

from live import frame
from live.ui_parts import FOLDER_ICON, icon_label
from live.section_icons import section_label
from live.focus_base import (document, inside, is_topic, kids, page_level, page_url,
    topic_home)
from live.focus_delivery import delivery_views, views_bar


def rail_url(page: Path, root: Path) -> str:
    """A left-rail link: an sNN's card in its level's Studio, any other folder its page."""
    return topic_home(page, root) if is_topic(page) else page_url(page, root)


def static_page(folder: Path, root: Path, view: str, body: str, note: str = "") -> str:
    """A page an sNN's builder writes into delivery/ (its preview, contract, slides): the workbench frame, its path and
    left rail ending at the topic's card in its level's Studio (JL 261031: the sNN has no page of its own), its
    Delivery views under the title. `view` is preview, contract or slides; `note` a tag beside its stage."""
    notes = frame._notes(folder)
    facts = frame._note_facts(notes)
    lead, shown = frame.topic_label(folder, facts.get("at", ""))
    owner = frame.topic_owner(folder)
    goal_html = ""                                   # no goal line under the title (hai-block CONSTITUTION A03);
                                                     # the topic's sentence lives on its card in its level's Studio
    crumbs, cur = [frame._link("/", root.name)], root
    for name in folder.relative_to(root).parts[:-1]:
        cur /= name
        crumbs.append(frame._link(page_url(cur, root), name))
    crumbs.append(frame._link(topic_home(folder, root), folder.name))
    left = [rail_link(page_url(owner, root, "studio"), owner.name, False)]
    left += [rail_link(rail_url(other, root), other.name, other == folder, "child") for other in rail_kids(owner, root)]
    title_html = (f'<span class="h1-addr">{frame.esc(lead)}</span>' if lead else '') + frame.esc(shown)
    source = ""                                      # no Markdown link under a page: the face opens from Files
    return page_shell(folder, root, crumbs, title_html, "Delivery", "what it hands over, and where it goes",
                      views_bar(delivery_views(folder, root), view), goal_html, body, source, left, "", [], "delivery")


def rail_kids(folder: Path, root: Path) -> list:
    """The pages one level down in the left rail: a Block's or a Job's sNN first, then its Jobs or Tasks, since an sNN
    sits beside them at the same level (JL 261030: "you should show the sNN as well, they are in the same level now");
    any other level, its kids()."""
    topics = [t for t, _ in frame._studio_topics(folder) if is_topic(t) and inside(t, root)] \
        if page_level(folder) in ("Block", "Job", "Task") else []
    return topics + [k for k in kids(folder) if inside(k, root)]


def rail_link(href, name, current, cls="", desc=""):
    return (f'<a href="{frame.esc(href)}" aria-label="{frame.esc(name)}"' + (' aria-current="page"' if current else '')
            + (f' class="{cls}"' if cls else '') + f'><i aria-hidden="true"></i><span class="rail-name">{icon_label(name)}'
            + (f'<small>{frame.esc(desc)}</small>' if desc else '') + '</span></a>')


def wait_items(folder, root) -> str:
    """The questions waiting for the person at this page or below, as rows focus.js adds to the page's 🙋 tray (JL 261114:
    "if there are things for me to make decision, could they just pop out?"); each opens its page's Interactions view."""
    try:
        from live.focus_interactions import interactions
        from live.focus_base import page_level
        if page_level(folder) in ("SPACE", "Folder"):     # a SPACE's own rollup is itself only: walk its Projects,
            from live.space_home import waiting_rows       # once, shared with its Home's 🙋 Waiting section
            rows = waiting_rows(folder, root)
        else:
            rows = [r for r in interactions(folder, root) if r.get("state") == "waiting"]
    except Exception:                                   # the tray is a help; a bad record never breaks the page
        return ""
    items = "".join(
        f'<li><span>{frame.esc(r.get("title") or r.get("run") or "")}'
        + (f'<small>{frame.esc(r["page"].name)}</small>' if r.get("page") and r["page"] != folder else "")
        + f'</span><a href="{frame.esc(page_url(r["page"] if r.get("page") else folder, root, "interactions"))}">Open</a></li>'
        for r in rows)
    return f'<template id="wait-items">{items}</template>' if items else ""


def side_launcher(folder, root, rail, section):
    """The right rail's sections behind one round button on the right edge: a pick opens that section in the side pane,
    a right split on a wide screen and a drawer on a phone. The pane has no header: the same button switches it, and
    its menu's last row closes it."""
    def src(key, view):
        url = page_url(folder, root, key, view)
        return url + ('&' if '?' in url else '?') + urlencode({'panel': key})
    items = ''.join(
        f'<button type="button" role="menuitem" data-side-key="{frame.esc(key)}" data-side-src="{frame.esc(src(key, view))}"'
        + (' aria-current="page"' if key == section else '') + f'>{icon_label(section_label(key, name))}</button>'
        for key, name, view in rail)                                    # every section's emoji, one table (hai-ui A12)
    return ('<button type="button" class="files-ball" aria-label="Sections" title="Sections" aria-haspopup="menu" '
            f'aria-controls="side-menu" aria-expanded="false">{FOLDER_ICON}</button>'
            f'<div id="side-menu" class="side-menu" role="menu" aria-label="Sections" hidden>{items}'
            '<button type="button" role="menuitem" class="side-close" data-side-close hidden>✕ Close</button></div>'
            '<dialog id="files-drawer" class="rail-drawer files-drawer" aria-label="Side pane">'
            '<div class="files-grip" aria-hidden="true"></div><iframe title="Side pane"></iframe></dialog>')


def page_shell(folder, root, crumbs, title_html, head, sub_line, bar, goal_html, body, source, left, right, rail, section, identity=''):
    """The one page every level shares: path, title with its section, its views, the goal, the card, both rails."""
    card = f'<section class="focus-card"><div class="focus-content">{body}</div></section>'
    page_menu = ('<dialog id="page-drawer" class="rail-drawer" aria-label="Pages"><header><b>Pages</b>'
                 '<button type="button" data-drawer-close aria-label="Close pages">✕</button></header>'
                 '<nav aria-label="Pages">' + ''.join(left) + '</nav></dialog>')
    edge_tabs = ''.join(
        f'<button type="button" class="rail-tab {side}" data-rail-menu aria-haspopup="dialog" '
        f'aria-label="{name}" aria-controls="{drawer}-drawer" aria-expanded="false">'
        f'<span class="rail-tab-label" aria-hidden="true">{name}</span></button>'
        for enabled, drawer, side, name in ((left, 'page', 'left', 'Pages'),)   # no right rail: sections are the
        if enabled)                                                       # title's ▾ menu (JL 261126)
    files = side_launcher(folder, root, rail, section) if rail else ''
    # JL 261029 sketch: "Project-PageParts  Overview" as the title; under it, the views of that section; then the goal
    return document(folder.name, '<main class="focus-page"><div class="focus-crumb">' + ' / '.join(crumbs) + '</div>'
                    + edge_tabs
                    + f'<h1>{title_html}<button type="button" class="h1-section h1-pick" aria-haspopup="menu" aria-controls="side-menu" '
                    f'aria-expanded="false" title="{frame.esc(sub_line)}">{icon_label(head)}</button></h1>'
                    + identity + page_menu + files + bar
                    + goal_html
                    + card
                    + f'<footer>{source}</footer><nav class="focus-rail left" aria-label="Pages">{"".join(left)}</nav>'
                    f'<nav class="focus-rail right" aria-label="Page sections">{right}</nav></main>' + wait_items(folder, root))
