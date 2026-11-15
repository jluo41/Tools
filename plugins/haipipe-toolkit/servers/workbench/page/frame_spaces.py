"""The vanilla default of each Space, its Disk, and how a theme's Spaces lay over it (spaces_for)."""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path
from urllib.parse import urlencode
from src.common import delivery_dir, delivery_owner, delivery_relative

from live.frame_base import (LEVEL_SKILL, ROUTE, RUN_ANY, SPACE_NAMES, Space, Theme, _PREFIXED, _e, _fields, _link,
                             _reader, _rel, _table, _title, chain, children, face, fill_tag, named, pop, run_type, runs_of, short_name)
from live.frame_tasks import task_layouts, task_type
from live.frame_studio import studio_inventory
from live.frame_groups import studio_cards, studio_sessions
from live.frame_report import report_view
from live.frame_delivery import delivery_view
from live.frame_related import related_view
from live.frame_work import work_tree


# ── the vanilla default of each Space ───────────────────────────────────────────────────────────
def vanilla(level: str, folder: Path, root: Path, sub: str = "", theme: "Theme | None" = None) -> dict:
    """{Space: Space}: what every Space shows when no theme fills it; `theme` lends the Report its fixed and
    starting groups (Theme.report_fixed, report_groups)."""
    out = {}
    tag = (_PREFIXED.match(folder.name).group(0).rstrip("_") if _PREFIXED.match(folder.name)
           else {"Block": "<bNN>", "Job": "<jNN>"}.get(level, "<tNN>"))
    md = face(folder)
    if md:
        rows = [(_e(k), _e(v)) for k, v in _fields(md)]
        out["Description"] = Space(
            f'<h2>{_e(_title(md))}</h2><p class=mut>{_link(_reader(md, root), _rel(md, root))}</p>'
            + (_table(("field", "value"), rows) if rows else ""),
            run_types=(run_type(f"run-face-{tag}", "update the description", "Update the face of {folder}.",
                                LEVEL_SKILL.get(level, LEVEL_SKILL["Task"])),))
    else:
        out["Description"] = Space(f'<p class=mut>No face file: {_e(folder.name)}.md is missing.</p>')

    # Related is the Block's (spaces_for gives a Job or Task its Block's)
    out["Related"] = related_view(folder, root, sub) if level == "Block" else Space()
    out["Idea Studio"] = Space(studio_cards(folder, root), run_types=(
        run_type("run-draw-<sNN>", "add a topic · redraw it · save this session, each a pass",
                 "/haipipe-studio a topic of {folder}: new topic → sNN-<topic>/ and runs/run-draw-<sNN>/; "
                 "redraw or this session → a pass of run-draw-<sNN>.", "haipipe-studio",
                 rows=studio_sessions(folder, root)),))

    # the Report: one card per Question under the Studio's group bar (b10 s05, JL 261011: "if the report card to
    # show, it will be the same as the sNN, we can create and add the tags"); the paper Board's four buttons,
    # once drawn on every theme (AUDIENCE_VIEWS, 261009), stay the paper theme's own
    page_row = ""
    if level == "Task" and md:                                   # a Task's report is its own face (s05-D10)
        runs = " · ".join(_e(r["run"]) for r in runs_of(folder)) or "<span class=mut>no Runs yet</span>"
        page_row = (f'<div class="q-row q-two"><div class=q-l><p class=q-head><b>the Page</b></p></div>'
                    f'<div class=q-r>{pop(_reader(md, root), "the Page", _title(md) + " ↗")}'
                    f'<p class=q-work><span class=mut>Work:</span> {runs}</p></div></div>')
    rows_html = report_view(level, folder, root, theme, empty=page_row)
    out["Audience Report"] = Space(rows_html, run_types=(
        run_type("run-ask-<qNN>", "ask a Question", "Ask a new Question of {folder}: its register row and "
                 "reports/qNN_<topic>/.", "haipipe-report"),
        run_type("run-report-<qNN>", "write the report", "Write or update a report of {folder}.", "haipipe-report"),
        run_type("run-figures-<qNN>", "rebuild the report drawing", "Rebuild a report drawing of {folder} from its "
                 "## Figures list: haipipe-report scripts/build_report_drawing.py <report folder>.", "haipipe-report"),
        run_type("run-check-<qNN>", "check a report", "Check a report of {folder} in a fresh context.",
                 "haipipe-report")))

    if level in ("Block", "Job"):
        kids = children(folder, level)
        rows = []
        for k in kids:
            kmd = face(k)
            count = len(children(k, "Job")) if level == "Block" else len(runs_of(k))
            rows.append((_link(ROUTE + "?" + urlencode({"path": _rel(k, root)}), k.name),
                         _e(_title(kmd) if kmd else "—"), _e(count)))
        # Job → Task → Run → what it found, one tree (b10 s32, JL 261012); the old table when there is none
        out["Work Details"] = Space(work_tree(level, folder, root, theme) or
                                    _table(("Job" if level == "Block" else "Task", "title",
                                            "Tasks" if level == "Block" else "Runs"), rows),
                                    run_types=(run_type("run-add-<jNN>" if level == "Block" else "run-add-<tNN>",
                                                        "add a " + ("Job" if level == "Block" else "Task"),
                                                        "Add a " + ("Job" if level == "Block" else "Task") + " to {folder}.",
                                                        LEVEL_SKILL.get(level, LEVEL_SKILL["Task"])),))
    else:
        rows = [(_e(p.name + "/"), _e(sum(1 for _ in p.rglob("*") if _.is_file())))
                for p in sorted(folder.iterdir()) if p.is_dir() and not p.name.startswith((".", "_"))
                and p.name not in ("runs", "studio", "reports", "delivery")] if folder.is_dir() else []
        out["Work Details"] = Space(work_tree("Task", folder, root, theme) + "<h3>Folders</h3>"
                                    + _table(("folder", "files"), rows),
                                    run_types=(run_type(f"run-build-{tag}", "build the Task", "Build {folder}.",
                                                        "haipipe-task"),))

    runs = runs_of(folder)
    types = sorted({r["type"] for r in runs})
    shown = [r for r in runs if sub in ("", "All") or r["type"] == sub]
    out["Runs"] = Space(
        _table(("Run", "kind", "type", "status"),
               [(_e(r["run"] + ("/" if r["path"].is_dir() else "")), _e(r["kind"]), _e(r["type"]), _e(r["status"]))
                for r in shown]),
        subspaces=("All",) + tuple(types) if runs else (), open=sub or ("All" if runs else ""),
        run_types=(RUN_ANY,))

    deliv = delivery_dir(folder)
    rows = [(_e(p.name + ("/" if p.is_dir() else "")), _e(sum(1 for _ in p.rglob("*") if _.is_file()) if p.is_dir() else ""))
            for p in sorted(deliv.iterdir()) if not p.name.startswith(".")] if deliv.is_dir() else []
    out["Delivery"] = Space(delivery_view(folder, root, theme) or _table(("item", "files"), rows),
                            run_types=(run_type(f"run-delivery-{tag}", "build the delivery", "Build the delivery of {folder}.",
                                                LEVEL_SKILL.get(level, LEVEL_SKILL["Task"])),))
    for name, disk in vanilla_disk(level, md.name if md else folder.name + ".md").items():
        out[name] = replace(out[name], disk=disk)
    if level == "Block":
        old_sources = dict.fromkeys(source for source, _, _ in studio_inventory(folder, root) if source != folder.resolve())
        extra = tuple((source.relative_to(folder.resolve()).as_posix() + "/studio/s*/", "existing topics from " + short_name(source.name))
                      for source in old_sources)
        out["Idea Studio"] = replace(out["Idea Studio"], disk=out["Idea Studio"].disk + extra)
    from live.task_draft import with_page_views       # a Task with a Page face: its Page views (workbench-task-draft/)
    return with_page_views(out, level, folder, root, sub, {"Description": "Face", "Audience Report": "Report",
                                                           "Work Details": "Folders", "Runs": "All",
                                                           "Delivery": "Files"})


# ── Disk: the files behind the open Space (JL 261007: "add the disks as well, to show what files are
# associated with the content in the screen ... so we have both disks and runs") ─────────────────
def vanilla_disk(level: str, face_name: str) -> dict:
    """{Space: ((path, what it feeds), ...)}: what each vanilla Space reads, under the open folder."""
    kids = {"Block": ("j[0-9]*_*/", "one row per Job: its face's title, its Tasks"),
            "Job": ("t[0-9]*_*/", "one row per Task: its face's title, its Runs")}.get(level)
    return {
        "Description": ((face_name, "the face: its title and fields"),),
        "Idea Studio": (("studio/s*/", "one row per topic"),
                        ("studio/s*/s*.md", "a row's details: decided · open · feeds"),
                        ("studio/s*/*.excalidraw", "the live drawing an open row shows"),
                        ("studio/s*/passes/", "a topic's rounds: a session or a meeting each")),
        "Audience Report": ((face_name, "## Questions: one row per Question, its group"),
                            ("reports/q*/q*.md", "Report: the title and its answer line"),
                            ("reports/q*/q*.excalidraw", "Report: its drawing, live (click to pan and zoom)"),
                            ("studio/s*/s*.md", "from the Idea Studio: each topic's feeds: line")),
        "Work Details": ((kids,) if kids else (("./", "its own folders, with their file counts"),)),
        "Runs": (("runs/*/", "one row per Run: kind · type · status, grouped by type"),),
        "Delivery": (("delivery/", "one row per item, with its file count"),),
    }


def disk_markup(entries, folder: Path, root: Path, most: int = 4) -> str:
    """The Disk list: one row per file or folder the open Space reads (JL 261007: "each row is a file
    or folder"), grouped under a short label with its count. A group shows `most` rows and folds the
    rest under "+N more"; a row is the name (a folder ends in /, a .md opens in the reader, the full
    path on hover); what is not there yet is one greyed row."""
    if not entries:
        return ""

    def row(p: Path) -> str:
        rel = Path(os.path.relpath(p, folder)).as_posix() if p != folder else "."
        if p.is_dir():
            n = sum(1 for c in p.iterdir() if not c.name.startswith("."))
            return (f'<li title="{_e(rel)}/"><span class=disk-p>{_e(p.name if p != folder else ".")}/</span>'
                    f'<span class=disk-n>{n}</span></li>')
        name = _link(_reader(p, root), p.name) if p.suffix == ".md" else _e(p.name)
        return f'<li title="{_e(rel)}"><span class=disk-p>{name}</span></li>'

    groups = []
    for path, meaning in entries:
        wants_dir = path.endswith("/")
        if any(ch in path for ch in "*?["):
            found = [m for m in sorted(folder.glob(path.rstrip("/"))) if m.is_dir() or not wants_dir]
        else:
            target = folder if path in ("", "./", ".") else folder / path
            found = [target] if target.exists() else []
        found = [m for m in found if m.resolve().is_relative_to(root.resolve())
                 and (m.resolve().is_relative_to(folder.resolve())
                      or m.resolve().is_relative_to(delivery_dir(folder)))]
        if not found:
            body = f'<li class=miss title="{_e(path)}"><span class=disk-p>{_e(path)}</span><span class=disk-n>not yet</span></li>'
        else:
            body = "".join(row(m) for m in found[:most])
            if len(found) > most:
                body += (f'<li class=disk-more><details><summary>+{len(found) - most} more</summary><ul>'
                         + "".join(row(m) for m in found[most:]) + "</ul></details></li>")
        groups.append(f'<li class=disk-g><p class=disk-gl title="{_e(path)}"><span>{_e(meaning)}</span>'
                      f'<span class=disk-n>{len(found) or ""}</span></p><ul>{body}</ul></li>')
    return (f'<div class=disk-in><p class=disk-head><b>Disk</b> <span class=mut>under {_e(folder.name)}/</span></p>'
            f'<ul class=disk-list>{"".join(groups)}</ul></div>')


DISK_CSS = """
.disk-in{padding:0 0 10px;border-bottom:1px solid var(--line);font:13px/1.45 system-ui,sans-serif;min-width:0}
.disk-head{margin:0 0 6px;overflow-wrap:anywhere}
.disk-list,.disk-list ul{list-style:none;margin:0;padding:0}
.disk-list{max-height:36vh;overflow:auto}
.disk-g+.disk-g{margin-top:8px}
.disk-gl{display:flex;justify-content:space-between;gap:8px;margin:0 0 2px;color:var(--mut);font-size:12px}
.disk-gl span:first-child{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.disk-g li{display:flex;align-items:baseline;gap:8px;padding:1px 0 1px 12px;min-width:0}
.disk-p{flex:1 1 auto;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.disk-p a{color:var(--acc);text-decoration:none}.disk-p a:hover{text-decoration:underline}
.disk-n{flex:none;font-size:11.5px;color:var(--mut)}
.disk-g li.miss .disk-p{color:var(--mut);font-style:italic}
.disk-g li.disk-more{display:block;padding-left:12px}
.disk-more summary{cursor:pointer;color:var(--mut);font-size:12px;list-style:none}
.disk-more summary::-webkit-details-marker{display:none}
.disk-more ul li{padding-left:0}
/* the Runs: one row per run type, its count at the right (JL 261007: "each row to be an item") */
.split>.runs-panel .runs-body{min-width:0}
.split>.runs-panel .runs-types{flex-direction:column;flex-wrap:nowrap;align-items:stretch;gap:4px}
.split>.runs-panel .run-type{justify-content:space-between;text-align:left;padding:4px 10px;min-width:0}
.split>.runs-panel .run-list{flex-direction:column;align-items:stretch;overflow-x:visible}
.split>.runs-panel .run-list button{text-align:left}
.split>.runs-panel .runs-detail,.split>.runs-panel .run-card{min-width:0}
.split>.runs-panel .run-card header>b,.split>.runs-panel .run-card p,.split>.runs-panel .run-results{overflow-wrap:anywhere}
.split>.runs-panel .run-card button,.split>.runs-panel .run-state{flex:none;white-space:nowrap}
.split>.runs-panel .run-results,.split>.runs-panel .run-results code{font-size:12px}
"""


def lays_out_page(name: str, subspaces, space=None) -> bool:
    """True when a theme laid the Page out in this Space itself: draft_task_spaces marked it
    (Space.page), or its subspaces start with the base's Page Task views; it may add its own after
    them (paper's Reviews, b16 s13)."""
    if space is not None and getattr(space, "page", False):
        return True
    from live.task_draft import DRAFT_TASK_SUBS
    page = DRAFT_TASK_SUBS.get(name)
    return bool(page) and tuple(subspaces)[:len(page)] == page


def spaces_for(theme: Theme, level: str, folder: Path, root: Path, sub: str = "") -> dict:
    """The theme's Spaces over the vanilla default, field by field."""
    base = vanilla(level, folder, root, sub, theme)
    own = theme.spaces(level, folder, root, sub) if theme.spaces else {}
    layout = task_layouts(theme.name).get(task_type(folder)) if level == "Task" else None
    if layout and not any(getattr(s, "page", False) for s in own.values()):
        # a Task type the base lays out (b32 s03): its layout first, the theme's own Spaces on top
        own = {**layout(folder, root, sub), **own}
    if theme.run_names:                        # the theme's buttons named by their Runs, this folder's tag filled
        names = {k: fill_tag(n, folder) for k, n in theme.run_names.items()}
        own = {k: replace(v, run_types=named(v.run_types, names)) for k, v in own.items()}
    out = {}
    for name in SPACE_NAMES:
        v, t = base.get(name, Space()), own.get(name)
        if t is None:
            out[name] = v
            continue
        merged = replace(v, **{k: getattr(t, k) for k in ("html", "subspaces", "open", "run_types", "note", "disk")
                               if getattr(t, k)})
        if lays_out_page(name, t.subspaces, t):
            # the Page laid out: its runs and its third row as set, even none (Delivery has no third row)
            merged = replace(merged, run_types=t.run_types, subspaces=t.subspaces,
                             open=t.open if t.subspaces else "")
        # the base's Page views stay beside the theme's own subspaces, unless the theme laid the Page
        # out in this Space itself (draft_task_spaces: the Page's exact views, embedded)
        if v.keep and not lays_out_page(name, t.subspaces, t):
            theirs = t.subspaces or v.subspaces           # a view the theme names too keeps its place
            merged = replace(merged, subspaces=theirs + tuple(k for k in v.keep if k not in theirs))
            if sub in v.keep and sub not in (t.subspaces or ()):    # a theme's own view of that name wins
                merged = replace(merged, html=v.html, open=sub, disk=v.disk)
        out[name] = merged
    # Studio and Related are Block-owned views, shared with that Block's Jobs and Tasks (b03 s02-D09,
    # b10 s04-related-workbench-skill)
    if level != "Block":
        block = chain(folder, root).get("Block")
        shared = spaces_for(theme, "Block", block, root) if block else {}
        out["Idea Studio"] = shared.get("Idea Studio") or Space('<p class=mut>Studio needs an owning Block.</p>')
        out["Related"] = shared.get("Related") or Space('<p class=mut>Related needs an owning Block.</p>')
    # Delivery has one physical owner, the Block (b10 s03-D06, JL 261011: "for the section, we will do not
    # have the related studio and delivery"; "also for the Jobs"). A Job's or Task's view is only its part of
    # the Block's Delivery, picked in the source row (render), and links back down to its folder.
    destination = delivery_dir(folder)
    block = delivery_owner(folder)
    address = destination.relative_to(block).as_posix() + "/"
    note = (f'<p class=space-reads>The Block\'s delivery/: <code>delivery/</code>; each Job\'s and Task\'s part '
            'is under its own path, picked in the row above.</p>' if folder.resolve() == block else
            f'<p class=space-reads>Its part of the Block\'s Delivery: <code>{_e(address)}</code> · from '
            f'{_link(ROUTE + "?" + urlencode({"path": _rel(folder, root)}), folder.name)}</p>')
    out["Delivery"] = replace(out["Delivery"], html=note + out["Delivery"].html,
                              disk=((delivery_relative(folder) + "/", "Block-owned delivery files for this source"),))
    return out
