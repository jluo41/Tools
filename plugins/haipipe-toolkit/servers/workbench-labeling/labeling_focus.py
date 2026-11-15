"""Labeling's focus pages, backed by the existing presenters and writers.

No parallel workflow state: next actions come from the preparation engine and
the labeling view model. The focus layout changes presentation, never receipts.

Every labeling Block, Job and Task of a known kind has the focus page every level shares (focus_page.page_shell, the
same path, rails and goal-line; task_shell below): a Block or Job holds MindMap · Status · Findings (level_page; b15
review round 2), an items Task Data · Items · Embedding (items_page, task_labeling.items_view), a meaning or an
expression Task its steps (labeling_steps.page), each view ending in 🙋 Interaction with its own forms. A building Task
(its face says `task-type: labeling-building`; b15 j01 t03 s57 and s58): Report and Work each list
Frame · Decide · Changes · Staging · Release · Runs, and open on Decide while a decision report waits for the person,
else on Frame. Decide is decision_report_view.py's; the other four steps show what they will hold, until they are
built; Runs lists the Task's Runs. Studio, Interactions, Delivery, Related, Timeline and Files are the base page's.
Today's one labeling Page (building and scanning at once) keeps the single-section design below.
"""
from __future__ import annotations

import re
from pathlib import Path
from live import focus_page as F, frame
from live import task_labeling as TL

from live.labeling_focus_read import ASSETS, content, link, roster, tasks, title
from live.labeling_focus_frame import (_assets, _jobs_of, delivery_html, is_items, shared_section_page, task_frame,
                                       task_shell)
from live.labeling_focus_building import building_page, is_building


# labeling_focus was split by responsibility into the modules below; an old name still answers from the one that holds it
SPLIT_INTO = ("labeling_focus_building", "labeling_focus_frame", "labeling_focus_read")


def __getattr__(name: str):
    """An old name (`labeling_focus.<name>`, `from live.labeling_focus import <name>`) answers from the sibling that holds it now."""
    import importlib
    for sibling in SPLIT_INTO:
        mod = importlib.import_module(f"live.{sibling}")
        if name in vars(mod):
            return vars(mod)[name]
    raise AttributeError(f"module 'live.labeling_focus' has no attribute {name!r}")

# an older link to a labeling Job (the single-section design's keys) still opens the nearest place
OLD_LEVEL = {"goal": ("report", ""), "tasks": ("work", "standing"), "reports": ("report", "findings"),
             "outputs": ("delivery", ""), "folders": ("files", ""), "progress": ("work", "standing"),
             "overview": ("report", "")}


def findings_html(folder: Path, root: Path) -> str:
    """Findings at a Block or a Job: what each Job has released (its expression Task's newest release: the final
    labels, signed or not) and the rules they follow (its meaning Task's approved guideline). Numbered closed bars,
    each with its state word; nothing made up where nothing is released."""
    from live import labeling_steps as S
    from live.ui_parts import _numbered
    from live.labeling_step_parts import _section
    if S.MV is None:
        return ""
    jobs = _jobs_of(folder, root)
    many = len(jobs) > 1                    # a Block of one Job needs no Job name on its bars (round 4: "j01_…:" stood in
    out = []                                # for a Job tab); with more, each bar names its Job in a few words
    for job in jobs:
        name = f"{F.job_short(job, jobs, root)}: " if many else ""
        tasks_ = [t for t in frame.children(job, "Job") if F.inside(t, root)]
        expression = next((t for t in tasks_ if S.kind(t) == "expression"), None)
        release = (S._xruns(expression)["release"] or [None])[-1] if expression is not None else None
        finals = release / "result" / "final_labels.jsonl" if release is not None else None
        labels = S._final_labels(finals, root, bool(S.MV.release_sign(release))) if finals is not None else ""
        if labels:
            out.append(labels.replace("🏷 Final labels", f"🏷 {name}Final labels, release {S._round(release)}", 1))
        else:
            out.append(_section(f"🏷 {name}Final labels", S._empty("Nothing released yet: an expression Task's signed "
                                                                  "release shows its final labels here."), "nothing yet"))
        got = S.MV.approved_meaning(job)
        if got:
            meaning, version, _ = got
            out.append(_section(f"🧠 {name}The rules they follow", S._maps(meaning, root, on=version, sign=False),
                                f"{version} approved"))
    return _numbered("".join(out))


def status_html(folder: Path, root: Path, level: str, topics: list, outputs: bool = False, html: str | None = None) -> str:
    """Status, focus_page's, with each Job's row on a Block marked by where the Job stands, read from its Tasks
    (🙋 ✅ 🏃 ⬜): a mark, never a state word or a done-of-total count; the Job's own page shows each Task."""
    html = F.status_now_html(folder, root, level, topics, outputs) if html is None else html
    if level != "Block":
        return html
    for job in _jobs_of(folder, root):
        kinds = [F.state_kind(F.state_label(F.read_face(t, root)["state"]))
                 for t in frame.children(job, "Job") if F.inside(t, root)]
        at = html.find(f'data-pop="{frame.esc(job.name)}"')
        end = html.find("</summary>", at) if at >= 0 else -1
        m = re.compile(r"<small>[^<]*</small>").search(html, at, end) if end > at else None
        if m:                                                # its own row's words only, in its closed bar
            html = html[:m.start()] + f"<small>{job_word(kinds)}</small>" + html[m.end():]
    return html


def job_word(kinds: list) -> str:
    """One mark for a Job from its Tasks' kinds of state: what needs the person first, then what runs, then done."""
    if "🙋 waiting on you" in kinds:
        return "🙋"
    if "⏳ running" in kinds:
        return "🏃"
    return "✅" if kinds and all(k == "✅ done" for k in kinds) else "⬜"


def level_page(theme, root, folder, section="", group=""):
    """Shared Work navigation with Labeling-owned findings and signed releases."""
    from live import work_frame as WF
    level = frame.level_of(folder)
    if section in OLD_LEVEL:
        section, group = OLD_LEVEL[section][0], OLD_LEVEL[section][1] or group
    if section == "delivery":
        section, group = "report", "delivery"
    group = WF.view_key(group)
    data = F.read_face(folder, root)
    questions, _ = F.owned_register(data, root, "Questions", "questions")
    topics, every = F.topic_rows(folder, root), F.interactions(folder, root)
    knows, events = F.known(folder, root, every), F.timeline_events(folder, root)
    shared_keys = {key for key, _ in WF.SHARED}
    if section in shared_keys:
        return shared_section_page(theme, root, folder, section, group)
    elif section == "related":
        return F.render(theme, root, folder, section, group)
    else:
        section = "report"  # Old Work links open the combined Report.
        groups = WF.topics_for(folder, root, questions)
        views = {"overview": "Overview", "standing": "Plan + Results", "findings": "Findings", "delivery": "Delivery"}
        view = group if group in views else "overview"
        if view == "overview":
            body = WF.overview(folder, root, data, questions, groups)
        elif view == "standing":
            body = status_html(folder, root, level, topics, html=WF.status(folder, root, data, groups))
        elif view == "findings":
            body = findings_html(folder, root) or WF.empty("No labeling findings recorded yet.")
        else:
            body = delivery_html(folder, root) or WF.empty("No signed labeling release recorded yet.")
        shared = WF.shared(folder, root, theme.name, level, view, topics, every, knows, events, every)
        body = ('<section class="work-section-group"><h2>📋 Review Content</h2>' + body
                + '</section><section class="work-section-group"><h2>🧭 Around the Work</h2>'
                + shared + '</section>')
    head, tail = _assets()
    return task_shell(root, folder, section, views, view, WF.STYLE + F.side_css() + body,
                      head, tail + F.PB_JS, aligned=True)


ITEMS_OLD = {"goal": ("report", ""), "runs": ("report", ""), "reports": ("report", ""), "outputs": ("delivery", ""),
             "folders": ("files", ""), "context": ("report", ""), "studio-all": ("studio", "")}


def items_page(theme, root, folder, section="", group=""):
    """An items Task's focus page: Data · Items · Embedding · Delivery on the shared frame (task_labeling.items_view)."""
    views = {key: name for key, name, _ in TL.ITEM_VIEWS}
    return task_frame(theme, root, folder, section, group, views, lambda: TL.items_default(folder, root),
                      lambda view: TL.items_view(folder, root, "work", view), TL.items_words(folder, root),
                      old=ITEMS_OLD)


def render(theme, root, folder, section="", group=""):
    root, folder = Path(root).resolve(), Path(folder).resolve()
    if not F.inside(folder, root):
        raise ValueError("Folder outside root")
    if frame.level_of(folder) in ("Block", "Job"):     # the shared shape (round 2), MindMap · Status · Findings
        return level_page(theme, root, folder, section, group)
    if frame.level_of(folder) not in {"Job", "Task"}:
        return F.render(theme, root, folder, section, group)
    from live import labeling_steps as S                 # a 🧭 meaning or 🛠 expression Task: its steps (b15 s58)
    if S.kind(folder):
        return S.page(theme, root, folder, section, group)
    if is_items(folder):
        return items_page(theme, root, folder, section, group)
    if is_building(folder):
        return building_page(theme, root, folder, section, group)
    data = F.read_face(folder, root)
    sections = roster(folder, root)
    section = section if section in dict(sections) else "goal"
    body = content(folder, root, section, data, group)
    job = folder if frame.level_of(folder) == "Job" else folder.parent
    level = frame.level_of(folder)
    parent_level = "Block" if level == "Job" else "Job"
    pages = [p for p in frame.children(folder.parent, parent_level) if F.inside(p, root)]
    if len(pages) < 2:
        pages = []
    left = ''.join(f'<a href="{frame.esc(F.page_url(p, root))}" aria-label="{frame.esc(title(p, root))}"'
                   + (' aria-current="page"' if p == folder else '') + '><i aria-hidden="true"></i>'
                   + f'<span class="rail-name">{frame.esc(title(p, root))}</span></a>' for p in pages)
    right = ''.join(f'<a href="{frame.esc(F.page_url(folder, root, key))}" aria-label="{frame.esc(label)}"'
                    + (' aria-current="page"' if key == section else '')
                    + '><i aria-hidden="true"></i>'
                    + f'<span class="rail-name">{frame.esc(label)}</span></a>' for key, label in sections)
    child_links = []
    child_kind = "Tasks" if frame.level_of(folder) == "Job" else "Runs"
    if child_kind == "Tasks":
        child_links = [link(p, root, title(p, root)) for p in tasks(folder, root)]
    else:
        seen = set()
        for run in frame.runs_of(folder):
            path = run["path"]
            card = path / "run.yaml" if path.is_dir() else path
            if run["run"] in seen or not card.is_file() or not F.inside(card, root):
                continue
            seen.add(run["run"])
            child_links.append(frame.pop(frame._file_url(card, root), run["run"], run["run"].replace("_", " ")))
    navigation = ('<nav class="lf-children" aria-label="Child ' + child_kind.lower() + '">'
                  + '<span class="lf-children-label">' + child_kind + '</span>'
                  + ''.join(child_links) + '</nav>') if child_links else ''
    crumb = link(job, root, title(job, root)) if folder != job else frame.esc(folder.parent.name)
    html = ('<main class="focus-page labeling-focus"><div class="focus-crumb">' + crumb + '</div>'
            + f'<h1>{frame.esc(title(folder, root))}</h1>' + navigation
            + f'<h2>{frame.esc(dict(sections)[section])}</h2>'
            + '<section class="focus-content">' + body + '</section>'
            + (f'<nav class="focus-rail left" aria-label="Sibling {level.lower()}s">' + left + '</nav>' if left else '')
            + '<nav class="focus-rail right" aria-label="Page sections">' + right + '</nav>'
            + '</main>')
    from live.runs_panel import PANEL_JS
    document = F.document(title(folder, root), html)
    return document.replace('</head>', '<style>' + (ASSETS / 'labeling.css').read_text() + '</style></head>').replace(
        '</body>', '<script>' + PANEL_JS + '</script><script>' + (ASSETS / 'labeling.js').read_text() + '</script></body>')


def focused_engine_document(document):
    """Retain the existing engine's event handlers, identity and guarded actions."""
    return document.replace('</head>', '<style>' + (ASSETS / 'engine.css').read_text() + '</style></head>').replace(
        '</body>', '<script>' + (ASSETS / 'engine.js').read_text() + '</script></body>')
