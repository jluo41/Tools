"""The focus page's frame: the left and right rails and the page shell around a section."""
from __future__ import annotations

from pathlib import Path

from live import frame
from live.ui_parts import icon_label
from live.focus_base import (document, first_sentence, inside, is_topic, kids, markdown, page_level, page_url,
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
    meta = ((f'<span class="row-stage">{frame.esc(facts["stage"])}</span>' if facts.get("stage") else '')
            + (f'<span class="row-type" title="delivery type">{frame.esc(facts["dtype"])}</span>' if facts.get("dtype") else '')
            + (f'<span class="row-stage">{frame.esc(note)}</span>' if note else ''))
    goal_html = (f'<div class="focus-goal topic-goal"><span class="goal-word">Topic</span>'
                 + (markdown(first_sentence(facts["topic"]), folder, root) if facts.get("topic") else '')
                 + (f'<p class="topic-meta">{meta}</p>' if meta else '') + '</div>')
    crumbs, cur = [frame._link("/", root.name)], root
    for name in folder.relative_to(root).parts[:-1]:
        cur /= name
        crumbs.append(frame._link(page_url(cur, root), name))
    crumbs.append(frame._link(topic_home(folder, root), folder.name))
    left = [rail_link(page_url(owner, root, "studio"), owner.name, False)]
    left += [rail_link(rail_url(other, root), other.name, other == folder, "child") for other in rail_kids(owner, root)]
    title_html = (f'<span class="h1-addr">{frame.esc(lead)}</span>' if lead else '') + frame.esc(shown)
    source = frame.pop(frame.reader(notes, root), "Source Markdown", "Open this topic's Markdown")
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


def page_shell(folder, root, crumbs, title_html, head, sub_line, bar, goal_html, body, source, left, right, rail, section, identity=''):
    """The one page every level shares: path, title with its section, its views, the goal, the card, both rails."""
    card = f'<section class="focus-card"><div class="focus-content">{body}</div></section>'
    section_menu = ('<dialog id="section-drawer" class="rail-drawer" aria-label="Page sections"><header><b>Sections</b>'
        '<button type="button" data-drawer-close aria-label="Close sections">✕</button></header>'
        '<nav aria-label="Page sections">' + "".join(
        f'<a href="{frame.esc(page_url(folder, root, key, view))}"' + (' aria-current="page"' if key == section else '')
        + f'>{icon_label(name)}</a>' for key, name, view in rail) + '</nav></dialog>')
    page_menu = ('<dialog id="page-drawer" class="rail-drawer" aria-label="Pages"><header><b>Pages</b>'
                 '<button type="button" data-drawer-close aria-label="Close pages">✕</button></header>'
                 '<nav aria-label="Pages">' + ''.join(left) + '</nav></dialog>')
    # JL 261029 sketch: "Project-PageParts  Overview" as the title; under it, the views of that section; then the goal
    return document(folder.name, '<main class="focus-page"><div class="focus-crumb">' + ' / '.join(crumbs) + '</div>'
                    '<div class="mobile-rail-controls"><button type="button" data-rail-menu aria-haspopup="dialog" '
                    'aria-controls="page-drawer" aria-expanded="false">☰ Pages</button>'
                    '<button type="button" data-rail-menu aria-haspopup="dialog" '
                    'aria-controls="section-drawer" aria-expanded="false">Sections ☰</button></div>'
                    f'<h1>{title_html}<span class="h1-section" title="{frame.esc(sub_line)}">{icon_label(head)}</span></h1>'
                    + identity + page_menu + section_menu + bar
                    + goal_html
                    + card
                    + f'<footer>{source}</footer><nav class="focus-rail left" aria-label="Pages">{"".join(left)}</nav>'
                    f'<nav class="focus-rail right" aria-label="Page sections">{right}</nav></main>' + wait_items(folder, root))
