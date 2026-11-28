"""The frame every labeling Task page wears: the Task shell and its rail, its steps as views with 🧭 Around the
Work under each, the shared sections, and the signed releases with their delivery."""
from __future__ import annotations

from pathlib import Path
from live import focus_page as F, frame, labeling_theme as T

from live.labeling_focus_read import ASSETS


def base_rail(folder, root) -> list:
    """The right rail exactly as focus_page.render builds it for a Task: (key, name, the words under its name)."""
    inbox = F.interactions(folder, root)
    delivery = F.paper_delivery(folder, root) + F.delivery_html(folder, root) or releases(folder, root)
    rail = [("report", "Report"), ("work", "Work")]
    if F.topic_rows(folder, root):
        rail.append(("studio", "Studio"))
    rail += [("interactions", "Interactions"), ("delivery", "Delivery")]
    if F.related_html(folder, root):
        rail.append(("related", "Related"))
    if F.timeline_events(folder, root):
        rail.append(("timeline", "Timeline"))
    rail.append(("skills", "Skills"))                   # the skills that work on it (JL 261105), as focus_page.render
    rail.append(("files", "Files"))
    from live import labeling_steps as S                 # a meaning or expression Task's Work holds its steps (s58-D02)
    level = frame.level_of(folder)
    work = ("its Jobs" if level == "Block" else "its Tasks" if level == "Job"
            else "its steps" if S.kind(folder) or is_items(folder) else "its Runs")
    words = {"report": "read the results and check the progress", "work": work,
             "studio": "drawings, mind maps, slides",
             "interactions": "🙋 waits on you" if any(r["state"] == "waiting" for r in inbox) else "",
             "delivery": "what it has handed over" if delivery else "",   # no empty-state words
             "related": "what came in: meetings, papers, emails", "timeline": "what happened when",
             "files": "the folder itself", "skills": "the skills that work on it"}
    return [(key, name, words[key]) for key, name in rail]


def task_shell(root, folder, section, views: dict, view: str, body: str, head_extra: str = "", tail_extra: str = "",
               words: dict | None = None, aligned: bool = False):
    """A labeling page's focus page around one view (a Block, a Job, an items, building, meaning or expression Task): the
    base page's path, title with its section, the views of that section, its goal-line, both rails; `head_extra` and `tail_extra` are the view's own
    stylesheet and script; `words` puts each view's state word on its button ({key: (word, ok | you | run)}).
    """
    if aligned:
        from live import work_frame as WF
        rail = [("report", "Report", "")] + [(key, title, "") for key, title in WF.SHARED]
    else:
        rail = base_rail(folder, root)
    level = frame.level_of(folder)
    bar = ('<nav class="section-views" aria-label="Views">' + "".join(
        f'<a href="{frame.esc(F.page_url(folder, root, section, key))}"' + (' aria-current="page"' if key == view else '')
        + f'>{frame.esc(name)}'
        + ('<span class="vw fd-you" title="waits for you">🙋</span>'       # a mark, only where the step waits on you
           if (words or {}).get(key, ("", ""))[1] == "you" else "")
        + '</a>' for key, name in views.items()) + '</nav>')
    goal_html = ""                          # no goal-line under the title: the Goal fold holds it (hai-block A03)
    source = ""                             # no "Open this page's Markdown" line: the face opens from Files (hai-block A02)
    crumbs, cur = [frame._link("/", root.name)], root          # the path, from the SPACE down (focus_page.render)
    for part in folder.relative_to(root).parts[:-1]:
        cur /= part
        crumbs.append(frame._link(F.page_url(cur, root), part))
    crumbs.append(f'<span aria-current="page">{frame.esc(folder.name)}</span>')
    left = []
    siblings = (F.rail_kids(folder.parent, root) if level in ("Job", "Task") else   # a Job's or Task's include its sNN;
                sorted(q for q in folder.parent.iterdir() if q.is_dir() and not q.name.startswith((".", "_"))   # a
                       and F.inside(q, root) and F.page_level(q) == F.page_level(folder)))   # Block's, the Blocks beside it
    for sibling in siblings:                                  # the Job's sNN and Tasks, this Task's own sNN under it
        left.append(F.rail_link(F.rail_url(sibling, root), sibling.name, sibling == folder))
        if sibling == folder:
            left += [F.rail_link(F.rail_url(child, root), child.name, False, "child")
                     for child in F.rail_kids(folder, root) if F.inside(child, root)]
    right = "".join(F.rail_link(F.page_url(folder, root, key), name, key == section, "", words)
                    for key, name, words in rail)
    title_html = frame.esc(folder.name).replace("_", "_<wbr>")   # a phone breaks the name at its words (round 4: "safet/y")
    page = F.page_shell(folder, root, crumbs, title_html, section.title(), dict((k, w) for k, _, w in rail)[section],
                        bar, goal_html, body, source, left, right, [(key, name, "") for key, name, _ in rail], section,
                        identity=F.page_identity_html("labeling", folder, root, F.read_face(folder, root)))   # type line (261109)
    head, tail = page.rsplit("</head>", 1)
    page = head + head_extra + "</head>" + tail
    head, tail = page.rsplit("</body>", 1)
    return head + tail_extra + "</body>" + tail


# ── the shared shape for a labeling Block, Job and items Task (round 2 of the b15 review: the Job page and the items
# Task kept the older single-section layout). Report holds every view as one numbered list; 🙋 Interaction closes
# every view with that view's own forms; the rail is Report and the eight shared sections, each focus_page.render's.
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def _assets() -> tuple:
    """(head, tail): the shared bars, folds, tabs and prompt box, and the steps' look (labeling_steps.page's)."""
    from live import focus_draft as FD
    from live.runs_panel import PANEL_JS
    from live.ui_parts import GROUP_CSS, PB_CSS, PB_JS
    css = "<style>" + (ASSETS / "steps.css").read_text(encoding="utf-8") + "</style>"
    js = "<script>" + (ASSETS / "steps.js").read_text(encoding="utf-8") + "</script>"
    return PB_CSS + GROUP_CSS + FD.CSS + css + ITEMS_CSS, PB_JS + FD.JS + "<script>" + PANEL_JS + "</script>" + js


# an items step's cards and its Sign, inside the shared bars (task_labeling draws them; their look was labeling.css's);
# its prompt and tables keep the grey wash every other Task's do (round 4: this prompt was blue, its siblings' grey)
ITEMS_CSS = """<style>.lf-items{--tab-wash:var(--soft);--mut:var(--muted);--acc:var(--accent);--fg:var(--ink)}
.lf-items details.topic{border:1px solid var(--line);border-radius:7px;margin:0 0 8px;background:var(--paper)}
.lf-items details.topic>summary{cursor:pointer;padding:7px 12px;font-size:14px}.lf-items details.topic>.work-body{padding:4px 12px 10px}
.lf-items .st{font-size:12.5px;margin-left:8px;color:var(--accent)}.lf-items .st-ok{color:#2b8a3e}.lf-items .st-warn{color:light-dark(#b35c00,#ffc078)}
.lf-items button,.lf-items .chip{display:inline-block;border:1px solid var(--line);padding:4px 11px;border-radius:5px;background:var(--paper);font:inherit;font-size:13px;color:var(--ink);cursor:pointer;text-decoration:none}
.lf-items input{font:inherit;border:1px solid var(--line);border-radius:5px;padding:4px 8px;background:var(--paper);color:var(--ink)}
.lf-items .space-empty{color:var(--muted);margin:4px 0}.lf-items h4{margin:8px 0 4px;font-size:13.5px}
.lf-items code{overflow-wrap:anywhere}.lf-items pre{white-space:pre-wrap;overflow-wrap:anywhere}.lf-items table{max-width:100%}
.lf-items .pb-kv small{color:var(--muted)}
@media(max-width:600px){.lf-items input{font-size:16px}}</style>"""


def _jobs_of(folder: Path, root: Path) -> list:
    return [folder] if frame.level_of(folder) == "Job" else [j for j in frame.children(folder, "Block") if F.inside(j, root)]


def _task_words(task: Path, root: Path, jobs: list) -> str:
    """A Task named for a row: its title ("Example chats as items"), after its Job's few words when a Block has more
    than one Job."""
    words = F.page_title(task)
    return f"{F.job_short(task.parent, jobs, root)} › {words}" if len(jobs) > 1 and task.parent in jobs else words


def releases(folder: Path, root: Path) -> list:
    """[(expression Task, release Run, its sign)] at this page or below: each round a person signed for release, the
    thing a labeling Job hands over (round 4: Delivery said "nothing handed over yet" beside a signed release)."""
    from live import labeling_steps as S
    if S.MV is None:
        return []
    out = []
    for page in F.rollup(folder):
        if frame.level_of(page) == "Task" and S.kind(page) == "expression" and F.inside(page, root):
            for run in S._xruns(page)["release"]:
                signed = S.MV.release_sign(run)
                if signed and S.MV.state(run) == "done":
                    out.append((page, run, signed))
    return out


def delivery_html(folder: Path, root: Path) -> str:
    """Delivery at a labeling page: each signed release, its final labels and where they came from, then whatever the
    Block's delivery/ holds (focus_page.delivery_html). Numbered closed bars, each with its state word."""
    from live import labeling_steps as S
    from live.ui_parts import _kv, _numbered
    from live.labeling_step_parts import _section
    jobs = _jobs_of(folder, root) if frame.level_of(folder) in ("Block", "Job") else []
    out = []
    for task, run, signed in releases(folder, root):
        finals = run / "result" / "final_labels.jsonl"
        rows = []
        if finals.is_file():
            import json
            rows = [json.loads(ln) for ln in finals.read_text(encoding="utf-8").splitlines() if ln.strip()]
        tally = " · ".join(f"{sum(r.get('label') == w for r in rows)} {w}" for w in sorted({str(r.get("label")) for r in rows}))
        got = S.MV.approved_meaning(task.parent)
        where = f"{_task_words(task, root, jobs)} › " if len(jobs) > 1 else ""
        body = _kv([("labels", frame.esc(f"{len(rows)} final labels" + (f": {tally}" if tally else ""))),
                    ("the file", S._open(run / "result" / "final_labels.md", root, "Open the final labels")),
                    ("rules", frame.esc(f"{got[1]}, approved {got[2]['at']}") if got else "—"),
                    ("signed", frame.esc(signed.get("at", "") or "yes")),
                    ("made by", f'<a data-pop="{frame.esc(run.name)}" href="{frame.esc(F.run_url(run, root))}">'
                                f'<code>{frame.esc(run.name)}</code></a>')])
        out.append(_section(f"🏷 {where}Final labels, release {S._round(run)}", body, "released"))
    base = F.delivery_html(folder, root)
    if base:
        out.append(_section("📁 The Block's delivery/", base, "handed over"))
    if not out:
        return ""
    from live.ui_parts import PB_CSS
    return PB_CSS + _numbered("".join(out))


def shared_section_page(theme, root, folder, section, group=""):
    """One of the 8 shared sections (Studio · Interactions · ... · Files) opened from the right rail, unfiltered:
    the same page for a labeling Block, Job and Task (work_frame.shared_bodies)."""
    from live import work_frame as WF
    level = frame.level_of(folder)
    topics, every = F.topic_rows(folder, root), F.interactions(folder, root)
    knows, events = F.known(folder, root, every), F.timeline_events(folder, root)
    items = every
    if section == "interactions" and group in ("waiting", "answered"):
        items = [r for r in every if r.get("state") == group]
    body, _ = WF.shared_bodies(folder, root, theme.name, level, None, topics, items,
                               knows, events, items, only=section)[section]
    views = ({"all": "All", "waiting": "Needs your input", "answered": "Answered"}
             if section == "interactions" else {"all": "All"})
    view = group if group in views else "all"
    head, tail = _assets()
    return task_shell(root, folder, section, views, view, WF.STYLE + F.side_css() + body,
                      head, tail + F.PB_JS, aligned=True)


def task_frame(theme, root, folder, section, group, views: dict, default, body, words=None,
               head_extra="", tail_extra="", old=None):
    """A labeling Task on the shared frame (the Paper Section Task's shape): one Report section, the Task's steps as
    its views and Delivery last, each view 📋 Review Content (`body(view)`: the whole step) then its 🙋 Interactions (the side pane holds the rest)
    (the 8 shared sections scoped to that step); the right rail is Report plus the 8 shared sections. Older links
    (section=work, a step named as a section, the Task's own `old` keys, section=delivery) open the nearest view.
    `default()` names the view that opens; `words` puts each step's state word on its button."""
    from live import work_frame as WF
    if old and section in old:
        section, group = old[section][0], old[section][1] or group
    if section in views:                                       # a step named as a section: that step
        section, group = "report", section
    if section == "work":                                      # Work is retired: its steps live in Report
        section = "report"
    if section == "delivery":
        section, group = "report", "delivery"
    if section in {key for key, _ in WF.SHARED}:
        return shared_section_page(theme, root, folder, section, group)
    if section not in ("", "report"):
        return F.render(theme, root, folder, section, group)
    views = {**views, "delivery": "Delivery"}
    view = group if group in views else default()
    if view == "delivery":
        content = (delivery_html(folder, root) or WF.empty("No signed labeling release recorded yet."))
    else:
        content = body(view)
    topics, every = F.topic_rows(folder, root), F.interactions(folder, root)
    knows, events = F.known(folder, root, every), F.timeline_events(folder, root)
    content = ('<section class="work-section-group"><h2>📋 Review Content</h2>' + content   # the side pane holds the
               + WF.view_asks(folder, root, theme.name, "Task", view, topics, every, knows, events, every) + '</section>')
    head, tail = _assets()
    return task_shell(root, folder, "report", views, view, WF.STYLE + F.side_css() + content,
                      head + head_extra, tail + F.PB_JS + tail_extra, words, aligned=True)


def is_items(folder) -> bool:
    return frame.level_of(folder) == "Task" and T.types_of(folder) == ("items",)
