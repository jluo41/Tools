"""The frame's rows: level row, Spaces row, Delivery source row, links and the old-view redirect."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode
from src.common import delivery_dir

from live.frame_base import (IN_STUDIO, ROUTE, SPACES, SPACE_LABELS, Space, TOP_ROW, Theme, _e, _link, _rel, _table,
                             chain, children, href, short_name)
from live.frame_delivery import _live_pages


# an old theme page's view -> the frame Space it became (cowork-board, work-board, discovery-board)
OLD_VIEW_SPACE = {"scope": "Description", "block": "Description", "people": "Description",
                  "resources": "Description", "work": "Work Details", "jobs": "Work Details",
                  "tasks": "Work Details", "task": "Work Details", "papers": "Work Details",
                  "questions": "Audience Report", "reports": "Audience Report", "check": "Audience Report",
                  "runs": "Runs", "delivery": "Delivery", "related": "Related"}


def frame_redirect(handler, block: Path, root: Path, view: str = "") -> None:
    """Send an old theme page's Block to the shared frame (JL 261011: every workbench has the one
    structure, Studio | Block · Job · Task | Delivery). Its pop-outs, reports and JSON stay where they are;
    an `--only` host serves no frame and keeps its own page."""
    query = {"path": _rel(block.resolve(), root.resolve())}
    space = OLD_VIEW_SPACE.get((view or "").lower(), "")
    if space and space != "Description":
        query["space"] = space
    handler.send_response(302)
    handler.send_header("Location", ROUTE + "?" + urlencode(query))
    handler.send_header("Content-Length", "0")
    handler.end_headers()


def _level_row(theme: Theme, root: Path, folder: Path, level: str, space: str, sub: str = "", *, studio: bool = False) -> str:
    """Guide (mounted first) · Studio | Block · Job ▾ · Task ▾ | Delivery; context stays in the title.
    Studio and Delivery are the Block's shared views (b10 s09-D05, JL 261010: "Studio | Block Job Task |
    Delivery"); Related opens the Studio, where it folds under the topics (b10 s04, JL 261011: "I might
    just want to keep Guide, Studio | Block, Job, Task | Delivery"); a level button goes back to its work view."""
    up = chain(folder, root)
    studio = studio or space in ("Idea Studio", "Studio") or space in IN_STUDIO
    delivery = space == "Delivery" and not studio
    if delivery or space in IN_STUDIO:
        sub = ""
    space = "Description" if space in ("Idea Studio", "Studio", "Delivery") + IN_STUDIO else space
    shared_on = studio or delivery
    current = ' aria-current="page"'
    tab = lambda label, url, on: (f'<a class="tab{" on" if on else ""}" href="{_e(url)}"'
                                  f'{current if on else ""}>{label}</a>')
    parts = [tab("Studio", href(folder, root, theme, space, sub, studio=True), studio),
             '<span class=bar></span>']
    for lv in theme.levels:
        name = theme.level_name(lv)
        here = up.get(lv)
        on = " on" if lv == level and not shared_on else ""
        if lv == "Block":
            if here:
                parts.append(f'<a class="tab{on}" href="{_e(href(here, root, theme, space, sub if here == folder else ""))}" '
                             f'title="{_e(here.name)}">{_e(name)}</a>')
            continue
        parent = up.get({"Job": "Block", "Task": "Job"}[lv])
        options = children(parent, {"Job": "Block", "Task": "Job"}[lv]) if parent else []
        if not options:                          # the tab stays, greyed, so every page has the same row
            if theme.hide_empty_levels:
                continue
            parts.append(f'<select disabled aria-label="{_e(name)}"><option>{_e(name)} ▾</option></select>')
            continue
        if here and (lv != level or shared_on):
            # below this level (a Task under its Job): the open item is a button that goes up to its tab, and a
            # ▾ beside it switches to a sibling; a dropdown alone ignores a click on the item already picked
            # (JL 261008: "I want to click the job button at the top, but it is not react")
            parts.append(f'<span class=lvl><a class=tab href="{_e(href(here, root, theme, space, sub if here == folder else ""))}" title="{_e(here.name)}">'
                         f'{_e(_label(theme, here))}</a><select aria-label="Switch {_e(name)}" '
                         f'onchange="if(this.value)location.href=this.value"><option value="" selected>▾</option>'
                         f'{_options(theme, root, space, options, None)}</select></span>')
            continue
        opts = _options(theme, root, space, options, here, sub if lv == level else "")
        pick = "" if here else f'<option value="" selected>{_e(name)} ▾</option>'
        parts.append(f'<select class="{on.strip()}" aria-label="{_e(name)}" '
                     f'onchange="if(this.value)location.href=this.value">{pick}{opts}</select>')
    parts += ['<span class=bar></span>', tab("Delivery", href(folder, root, theme, "Delivery"), delivery)]
    return '<nav class="row levels">' + "".join(parts) + "</nav>"


def _label(theme: Theme, folder: Path) -> str:
    """A folder's label in the level row: the theme's, else its short name."""
    got = None
    if theme.option:
        try:
            got = theme.option(folder)
        except Exception:                        # a theme's label must not break the frame
            got = None
    return got[0] if got else short_name(folder.name)


def _options(theme: Theme, root: Path, space: str, options: list, here, sub: str = "") -> str:
    """The dropdown's options: each folder's name, or the theme's label for it; the theme's groups as
    <optgroup>s, in the order they first come."""
    groups: dict = {}
    for o in options:
        got = None
        if theme.option:
            try:
                got = theme.option(o)
            except Exception:                    # a theme's label must not break the frame
                got = None
        label, group = got if got else (short_name(o.name), "")
        groups.setdefault(group or "", []).append(
            f'<option value="{_e(href(o, root, theme, space, sub if o == here else ""))}" title="{_e(o.name)}"'
            f'{" selected" if o == here else ""}>{_e(label)}</option>')
    return "".join("".join(opts) if not g else f'<optgroup label="{_e(g)}">{"".join(opts)}</optgroup>'
                   for g, opts in groups.items())


def _spaces_row(theme, root, folder, space, sub="", views=None) -> str:
    out, last = [], None
    for name, group, optional in SPACES:
        if name in TOP_ROW or name in IN_STUDIO:  # the top row's own, or folded in the Studio (b10 s09-D05, s04)
            continue
        if last is not None and group != last:
            out.append('<span class=bar></span>')
        last = group
        cls = "tab" + (" on" if name == space else "") + (" opt" if optional else "")
        label = SPACE_LABELS.get(name, name)
        shared = (sub if space in ("Audience Report", "Work Details")
                  and name in ("Audience Report", "Work Details")
                  and sub in (views or {}).get(name, Space()).subspaces else "")
        out.append(f'<a class="{cls}" href="{_e(href(folder, root, theme, name, shared))}">{_e(label)}</a>')
    return '<nav class="row spaces">' + "".join(out) + "</nav>"


def delivery_parts(block: Path) -> list:
    """[(source folder, depth)] for each Job, and each Task under it, that has a part in the Block's
    delivery/ (b10 s03-D06): the path is the link, delivery/jNN_<job>/tNN_<task>/ -> jNN_<job>/tNN_<task>/."""
    out, live = [], {i["folder"] for i in _live_pages(block)}
    for job in children(block, "Block"):
        tasks = [t for t in children(job, "Job") if delivery_dir(t).is_dir() or t in live]
        if delivery_dir(job).is_dir() or job in live or tasks:
            out.append((job, 1))
            out += [(t, 2) for t in tasks]
    return out


def _delivery_row(theme, root, block: Path, folder: Path) -> str:
    """Delivery's source row: Block, then each Job with a part (and the open Job or Task even before it has
    one); the open folder is picked. A Task shows beside its Job, `jNN › tNN`."""
    up = chain(folder, root)
    shown = [(f, d) for f, d in delivery_parts(block) if d == 1 or f in (folder, up.get("Task"))]
    for lv, d in (("Job", 1), ("Task", 2)):              # the open one, even with nothing built yet
        f = up.get(lv)
        if f and f not in [x for x, _ in shown]:
            at = next((i + 1 for i, (x, _) in enumerate(shown) if x == up.get("Job")), len(shown))
            shown.insert(at if lv == "Task" else len(shown), (f, d))
    current = ' aria-current="true"'                  # the page's own mark stays on the top row's Delivery
    chip = lambda f, label: (f'<a class="tab{" on" if f == folder else ""}" href="{_e(href(f, root, theme, "Delivery"))}"'
                             f'{current if f == folder else ""}>{_e(label)}</a>')
    parts = [chip(block, theme.level_name("Block"))]
    for f, d in shown:
        parts.append(chip(f, (f.parent.name.split("_", 1)[0] + " › " if d == 2 else "") + _label(theme, f)))
    return '<nav class="row subs delivery-parts">' + "".join(parts) + "</nav>"


def delivery_by_source(theme, block: Path, root: Path) -> str:
    """The Block's Delivery, by source: one row per Job's and Task's part, its files, and links to that part
    and back down to its folder."""
    rows, parts = [], delivery_parts(block)
    task_parts = {delivery_dir(f) for f, d in parts if d == 2}
    for f, d in parts:
        part = delivery_dir(f)                   # a Job's own files: not its Tasks' parts under it
        n = sum(1 for x in part.rglob("*") if x.is_file() and not any(t != part and t in x.parents for t in task_parts)) \
            if part.is_dir() else 0
        n += sum(i["folder"] == f for i in _live_pages(block))     # a live page is what this part hands over, with no file
        rows.append((("└ " if d == 2 else "") + _link(href(f, root, theme, "Delivery"),
                                                                       part.relative_to(block).as_posix() + "/"),
                     _link(ROUTE + "?" + urlencode({"path": _rel(f, root)}), f.name), _e(n)))
    if not rows:
        return ""
    return "<h3>By source</h3>" + _table(("part", "from", "files"), rows)
