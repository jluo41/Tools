"""Labeling's single-section pages, backed by the existing presenters and writers.

No parallel workflow state: next actions come from the preparation engine and
the labeling view model. The focus layout changes presentation, never receipts.

A building Task (its face says `task-type: labeling-building`) has the focus page every level shares instead
(focus_page.page_shell, the same path, rails and goal-line; b15 j01 t03 s57 and s58): Report and Work each list
Frame · Decide · Changes · Staging · Release · Runs, and open on Decide while a decision report waits for the person,
else on Frame. Decide is decision_report_view.py's; the other four steps show what they will hold, until they are
built; Runs lists the Task's Runs. Studio, Interactions, Delivery, Related, Timeline and Files are the base page's.
Every other labeling page keeps the single-section design below.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import decision_report_view as DR, focus_page as F, frame, labeling_theme as T, task_labeling as TL

ASSETS = Path(__file__).parent / "focus-assets"
ITEM_VIEWS = {"data": "1 · Data", "items": "2 · Items", "embedding": "3 · Embedding"}
ENGINE_VIEWS = {key: (v[0], v[1], v[2]) for key, v in T.VIEW.items()}

# a building Task's views, in button order (s58: building = Frame · Decide · Changes · Staging · Release, then Runs),
# each with the words task_views.py draws it with: its caption, its first section, the step after it in Work
BUILD_VIEWS = (("frame", "Frame", "the task: the label, who decides, its values", "🎯 Frame the task", "decide"),
               ("decide", "Decide", "this round's decision report, card by card", DR.TITLE_1, "changes"),
               ("changes", "Changes", "what your answers changed, and the labels it touches", "🔁 Update and check", "staging"),
               ("staging", "Staging", "this round's run, and where its report sends it", "🔁 Run the round", "decide"),
               ("release", "Release", "what is frozen, and whether it is ready", "🔒 Freeze and check", ""),
               ("runs", "Runs", "every Run of this Task", "⚙️ Runs", ""))
NEXT_WORDS = {"decide": "🙋 Decide", "changes": "🔁 Changes", "staging": "🧪 Staging"}
OWN_SECTIONS = ("report", "work")                     # the building page's own; the rest are the base page's
# an older link to a building Task (the single-section design's keys) still opens the nearest place
OLD_BUILD = {"overview": ("report", ""), "reports": ("report", ""), "goal": ("work", ""), "status": ("work", ""),
             "children": ("work", ""), "runs": ("work", "runs"), "rounds": ("work", "decide"),
             "folders": ("files", ""), "outputs": ("delivery", "")}


def flat_content(html: str) -> str:
    """Flatten rendered disclosures; leave embedded scripts and styles intact."""
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", html, flags=re.S | re.I)
    for i in range(0, len(parts), 2):
        text = re.sub(r"<details\b([^>]*)>", r'<section data-static-content="true"\1>', parts[i])
        text = re.sub(r"</details\s*>", "</section>", text)
        text = re.sub(r"<summary\b([^>]*)>", r'<div role="heading" aria-level="3"\1>', text)
        parts[i] = re.sub(r"</summary\s*>", "</div>", text)
    return "".join(parts)


def link(folder, root, label, section="goal", primary=False):
    return (f'<a class="{"lf-primary" if primary else "lf-link"}" '
            f'href="{frame.esc(F.page_url(folder, root, section))}">{frame.esc(label)}</a>')


def title(folder, root):
    face = frame.face(folder)
    return frame._title(face) if face and F.inside(face, root) else folder.name


def tasks(folder, root):
    job = folder if frame.level_of(folder) == "Job" else folder.parent
    return [t for t in frame.children(job, "Job") if F.inside(t, root)]


def _run_state(run: Path) -> str:
    """A Run's state: its receipt's status once it has run (result/runtime.yaml), else its card's."""
    for path in (run / "result" / "runtime.yaml", run / "run.yaml"):
        if path.is_file():
            m = re.search(r"(?m)^status:\s*(\S+)", path.read_text(encoding="utf-8", errors="ignore"))
            if m:
                return m.group(1)
    return ""


def _two_loop_next(ts):
    """A Job that runs the two loops (b15 s13-D12): the form that waits for the person first, then the next planned
    Run to press, then the meaning Task's report prompt; the score Task's Runs come only after a report is answered."""
    runs = [(t, r, _run_state(r)) for t in ts if (t / "runs").is_dir()
            for r in sorted((t / "runs").iterdir()) if r.is_dir() and re.match(r"^r\d+_", r.name)]
    for t, r, state in runs:
        if state == "waiting" and "_collect_" in r.name:
            return t, "runs", f"Answer {r.name} in the Block's Interactions; one paste saves it.", ""
    answered = any("_collect_report_" in r.name and state == "done" for _, r, state in runs)
    for t, r, state in runs:
        if state == "planned" and ("score" not in T.types_of(t) or answered):
            return t, "runs", f"Press {t.name.split('_', 1)[0]} {r.name}: its ticket is ready.", ""
    meaning = next((t for t in ts if "meaning" in T.types_of(t)), None)
    if meaning and not answered:
        return meaning, "goal", "Paste the meaning Task's Report prompt into its chat session.", ""
    return None


def next_action(folder, root):
    """Derive the next screen on every request, without settling or starting Runs."""
    ts = tasks(folder, root)
    if any("meaning" in T.types_of(t) for t in ts):
        step = _two_loop_next(ts)
        if step:
            return step
    item = next((t for t in ts if T.types_of(t) == ("items",)), None)
    if item and TL.IT:
        try:
            n = TL.IT.next_step(item, settle_runs=False)
        except (OSError, ValueError, RuntimeError, KeyError) as exc:
            return item, "data", "Inspect corpus preparation", str(exc)
        if n["step"] != "done":
            key = {"describe": "data", "items": "items", "embed": "embedding"}.get(n["step"], "data")
            return item, key, n["do"], n.get("note") or ""
    build = next((t for t in ts if "building" in T.types_of(t)), None)
    if build and T.L:
        vm = T.L._view_model(frame.face(build))
        words, space = T.L._next_step(vm)
        if space == "labeling":
            key = "rounds" if vm["canonical"].get("phase") == "P1" else "definition"
        else:
            key = "contract" if vm.get("preparation", {}).get("linked") else "preparation"
        return build, key, words, ""
    scan = next((t for t in ts if "scanning" in T.types_of(t)), None)
    if scan:
        return scan, "test", "Review the handoff and executor qualification.", ""
    return folder, "tasks", "Prepare an items Task and a labeling Task to continue.", ""


def next_html(folder, root):
    dest, key, words, note = next_action(folder, root)
    step = dict(roster(dest, root)).get(key, key.title())
    badges = [dest.name.split('_', 1)[0].upper(), step]
    if T.types_of(dest) == ("items",) and TL.IT:
        try:
            who = TL.IT.next_step(dest, settle_runs=False).get("who")
            if who in {"person", "agent"}:
                badges.append("Your input needed" if who == "person" else "Agent action")
        except (OSError, ValueError, RuntimeError, KeyError):
            pass
    labels = '<div class="lf-badges" aria-label="Current step">' + ''.join(
        '<span class="lf-badge">' + frame.esc(label) + '</span>' for label in badges) + '</div>'
    return ('<section class="lf-next">' + labels + '<h3>Next action</h3><p>' + frame.esc(words) + '</p>'
            + (f'<div class="lf-note"><span class="lf-note-label">Preparation note</span><p>{frame.esc(note)}</p></div>' if note else "")
            + link(dest, root, "Continue labeling", key, True) + '</section>')


def roster(folder, root):
    level = frame.level_of(folder)
    rows = [("goal", "Goal"), ("tasks", "Tasks")] if level == "Job" else [("goal", "Goal"), ("runs", "Runs")]
    types = T.types_of(folder)
    if types == ("items",):
        rows += [(k, v.split(" · ", 1)[-1]) for k, v in ITEM_VIEWS.items()]
    elif {"building", "scanning"} & set(types):
        keys = (("preparation", "contract", "definition", "rounds", "guideline") if "building" in types else ())
        keys += (("test", "evaluation", "scan", "audit") if "scanning" in types else ())
        keys += ("handoff",) + (("final",) if "scanning" in types else ())
        rows += [(key, ENGINE_VIEWS[key][2]) for key in keys]
    elif types:
        rows += [("context", "Context")]
    rows += [("reports", "Reports")]
    if (folder / "schema.yaml").is_file():
        rows.append(("schema", "Label schema"))
    rows += [("outputs", "Outputs"), ("studio", "Studio-All"), ("timeline", "Timeline"), ("folders", "Folders")]
    return rows


def report_files(task, root):
    """Only the Task's human-readable Run results; never enumerate a labeling lane."""
    found = []
    for row in frame.runs_of(task):
        run = row["path"]
        if not F.inside(run, root):
            continue
        dirs = [run / "result", task / "results" / row["run"]] if run.is_dir() else [task / "results" / row["run"]]
        for directory in dirs:
            if not directory.is_dir() or not F.inside(directory, root):
                continue
            # Direct result files only. Nested raw data and protected lanes stay private.
            files = sorted(p for p in directory.iterdir() if p.is_file() and F.inside(p, root)
                           and p.suffix.lower() in {".md", ".pdf", ".html", ".txt"}
                           and p.name not in {"stderr.txt", "stdout.txt"})
            found += [(row, p) for p in files]
    return found


def reports(folder, root, group=""):
    if frame.level_of(folder) == "Job":
        out = []
        for task in tasks(folder, root):
            n = len(report_files(task, root))
            out.append('<article class="lf-row"><h3>' + frame.esc(title(task, root)) + '</h3><p>'
                       + (f'{n} saved report files' if n else 'No saved report file yet') + '</p>'
                       + link(task, root, 'Review Task reports', 'reports') + '</article>')
        return "".join(out)
    out = []
    for row, path in report_files(folder, root):
        status = TL._status(row["path"]) if row["path"].is_dir() else row["status"]
        out.append('<article class="lf-row"><h3>' + frame.esc(path.name) + '</h3><p>'
                   + frame.esc(row["run"] + ' · ' + status) + '</p>'
                   + frame.pop(frame._file_url(path, root), path.name, 'Read report') + '</article>')
    if T.types_of(folder) == ("items",):
        selected = group if group in ITEM_VIEWS else "items"
        controls = ''.join('<a href="' + frame.esc(F.page_url(folder, root, "reports", key))
                           + '"' + (' aria-current="page"' if key == selected else '') + '>'
                           + frame.esc(value.split(' · ', 1)[-1]) + '</a>' for key, value in ITEM_VIEWS.items())
        result = TL.spaces(folder, root, ITEM_VIEWS[selected]).get("Audience Report")
        out.insert(0, '<nav class="focus-actions lf-report-nav" aria-label="Preparation reports">'
                   + controls + '</nav>' + (flat_content(result.html) if result else '<p>No preparation report yet.</p>'))
    elif {"building", "scanning"} & set(T.types_of(folder)):
        job = T._engine_job(folder, root)
        if job and T.L:
            vm = T.L._view_model(frame.face(folder))
            out.insert(0, flat_content(T.L._run_table(vm)))
            out.insert(0, '<p>Labeling records are read from the existing Run tickets and results.</p>')
    return "".join(out) or '<p>No report has been saved for this Task yet.</p>'


def engine_embed(folder, root, key):
    job = T._engine_job(folder, root)
    if not job:
        return '<p>No labeling workspace is attached yet.</p>'
    url = T._view_url(job, T.VIEW[key])
    if not url:
        return '<p>No labeling workspace is attached yet.</p>'
    # Exact existing view and write-door identity; focus only changes its presentation.
    url += '&focus=1'
    return (f'<iframe class="lf-engine" title="{frame.esc(ENGINE_VIEWS[key][2])}" '
            f'src="{frame.esc(url)}"></iframe><p class="mut">'
            f'<a href="{frame.esc(url)}" target="_blank" rel="noopener">Open this workspace separately</a></p>')


def content(folder, root, section, data, group=""):
    level, types = frame.level_of(folder), T.types_of(folder)
    if section == "goal":
        text = data["goal"] or data["sections"].get("opening") or data["sections"].get("topic") or ""
        body = F.markdown(text, folder, root) if text else '<p>No goal recorded in this page.</p>'
        if level == "Job" or {"items", "building", "scanning"} & set(types):
            body += next_html(folder, root)
        if data["close"]:
            body += '<section class="lf-row"><h3>Completion criteria</h3>' + F.markdown(data["close"], folder, root) + '</section>'
        return body
    if section == "tasks":
        return "".join('<article class="lf-row"><h3>' + link(t, root, title(t, root)) + '</h3><p>'
                       + T.work_meta(t, root) + '</p></article>' for t in tasks(folder, root))
    if section == "runs":
        rows = []
        for row in frame.runs_of(folder):
            p = row["path"]
            if not F.inside(p, root):
                continue
            card = p / 'run.yaml' if p.is_dir() else p
            status = TL._status(p) if p.is_dir() else row["status"]
            rows.append('<article class="lf-row"><h3>' + frame.esc(row["run"]) + '</h3><p>'
                        + frame.esc(status) + '</p>' + (frame.pop(frame._file_url(card, root), row["run"], 'Run record')
                                                     if card.is_file() else '') + '</article>')
        return "".join(rows) or '<p>No Run tickets yet.</p>'
    if types == ("items",) and section in ITEM_VIEWS:
        space = TL.spaces(folder, root, ITEM_VIEWS[section]).get("Work Details")
        return flat_content(space.html) if space else '<p>Preparation presenter unavailable.</p>'
    if section in ENGINE_VIEWS and {"building", "scanning"} & set(types):
        return engine_embed(folder, root, section)
    if section == "reports":
        return reports(folder, root, group)
    if section == "schema":
        schema = folder / "schema.yaml"
        return '<pre>' + frame.esc(schema.read_text()) + '</pre>' if F.inside(schema, root) else '<p>Unavailable.</p>'
    if section == "context":
        return F.markdown(data["sections"].get("topic") or data["sections"].get("opening") or '', folder, root)
    if section == "outputs":
        if level == "Job":
            return '<p>Each Task keeps its own outputs and versions.</p>' + ''.join(
                '<article class="lf-row">' + link(t, root, title(t, root), 'outputs') + '</article>' for t in tasks(folder, root))
        if types == ("items",):
            f = TL._items_facts(folder, root)
            if not f["run"]:
                return '<p>No completed items output yet.</p>'
            return '<h3>Prepared items</h3>' + TL._kv([
                ('Run', frame.esc(f['run'].name)), ('Items', frame.esc(f['manifest'].get('items', 'Not recorded'))),
                ('Item unit', frame.esc(f['manifest'].get('item') or 'Not recorded'))]) + link(folder, root, 'Inspect items', 'items')
        if {"building", "scanning"} & set(types):
            return '<p>Review the recorded guideline and delivery status.</p><div class="focus-actions">' + ''.join(
                link(folder, root, label, key) for key, label in roster(folder, root) if key in {'guideline', 'handoff', 'final'}) + '</div>'
        return reports(folder, root)
    if section == "studio":
        return F.studio_html(F.topic_rows(folder, root), root, '')
    if section == "timeline":
        events = F.log_events(data['sections'].get('log', ''))
        return '<ol class="focus-timeline">' + ''.join(
            f'<li><time>{frame.esc(day)}</time><div>{F.markdown(text, folder, root)}</div></li>'
            for day, _, text in events) + '</ol>' if events else '<p>No dated entries in this page’s Log.</p>'
    return F.folder_html(folder, root)


def is_building(folder) -> bool:
    """A building Task: its face says `task-type: labeling-building` (one type, not today's labeling Page)."""
    return frame.level_of(folder) == "Task" and T.types_of(folder) == ("building",)


def base_rail(folder, root) -> list:
    """The right rail exactly as focus_page.render builds it for a Task: (key, name, the words under its name)."""
    inbox = F.interactions(folder, root)
    delivery = F.paper_delivery(folder, root) + F.delivery_html(folder, root)
    rail = [("report", "Report"), ("work", "Work")]
    if F.topic_rows(folder, root):
        rail.append(("studio", "Studio"))
    rail += [("interactions", "Interactions"), ("delivery", "Delivery")]
    if F.related_html(folder, root):
        rail.append(("related", "Related"))
    if F.timeline_events(folder, root):
        rail.append(("timeline", "Timeline"))
    rail.append(("files", "Files"))
    words = {"report": "read the results and check the progress", "work": "its Runs",
             "studio": "drawings, mind maps, slides",
             "interactions": ("🙋 waits on you" if any(r["state"] == "waiting" for r in inbox)
                              else "nothing waits on you" if inbox else "nothing asked yet"),
             "delivery": "what it has handed over" if delivery else "nothing handed over yet",
             "related": "what came in: meetings, papers, emails", "timeline": "what happened when",
             "files": "the folder itself"}
    return [(key, name, words[key]) for key, name in rail]


def building_runs(folder, root) -> str:
    """Runs: the Task's Runs, newest first, each its type, its state and its record; no Run's output."""
    rows = []
    for row in reversed(frame.runs_of(folder)):
        p = row["path"]
        if not F.inside(p, root):
            continue
        card = p / "run.yaml" if p.is_dir() else p
        state = TL._status(p) if p.is_dir() else row["status"]
        rows.append(f'<div class="dec-run"><span class="n">{frame.esc(row["run"])}</span>'
                    f'<span class="d">{frame.esc(row["type"])}</span><span class="w">{frame.esc(state)}</span>'
                    + (frame.pop(frame._file_url(card, root), row["run"], "Open").replace("<a ", '<a class="dec-btn" ', 1)
                       if card.is_file() and F.inside(card, root) else "") + "</div>")
    return DR.section(1, BUILD_VIEWS[-1][3], "".join(rows) or DR.line("No Runs yet."))


def building_view(folder, root, section, key) -> str:
    """One view of a building Task: Decide (decision_report_view), Runs, or a step not built yet, said so; in Work
    the step after it last (Report is read only, its Results only)."""
    _, name, caption, first, after = next(v for v in BUILD_VIEWS if v[0] == key)
    report = section == "report"
    if key == "decide":
        body = DR.decide_view(folder, root, read_only=report)
    elif key == "runs":
        body = DR.wrap(building_runs(folder, root))
    else:                                         # honest: what the view will show, no number made up
        body = DR.wrap(DR.group(DR.RESULTS if report else DR.PROCESS)
                       + DR.section(1, first, DR.big("Nothing to show yet") + DR.line(f"This view will show {caption}.")))
    if after and not report:
        body += DR.wrap(DR.next_link(F.page_url(folder, root, "work", after), NEXT_WORDS[after]))
    return f'<p class="view-caption">{frame.esc(caption[:1].upper() + caption[1:])}.</p>' + body


def building_page(theme, root, folder, section="", group=""):
    """A building Task's focus page: the base page's shell and rails; Report and Work hold the building views."""
    views = {key: name for key, name, *_ in BUILD_VIEWS}
    if section in OLD_BUILD:
        section, group = OLD_BUILD[section][0], OLD_BUILD[section][1] or group
    elif section in views:                             # a view named as a section: that view, in Work
        section, group = "work", section
    rail = base_rail(folder, root)
    keys = [key for key, _, _ in rail]
    if section in keys and section not in OWN_SECTIONS:
        return F.render(theme, root, folder, section, group)
    section = section if section in OWN_SECTIONS else "work"
    view = group if group in views else ("decide" if DR.waiting_report(folder) else "frame")
    bar = ('<nav class="section-views" aria-label="Views">' + "".join(
        f'<a href="{frame.esc(F.page_url(folder, root, section, key))}"' + (' aria-current="page"' if key == view else '')
        + f'>{frame.esc(name)}</a>' for key, name in views.items()) + '</nav>')
    data = F.read_face(folder, root)
    goal = data["goal"].split("\n")[0] if data["goal"] else ""
    goal_html = (f'<div class="focus-goal"><span class="goal-word">{F.GOAL_WORD["Task"]}</span>'
                 f'{F.markdown(goal, folder, root)}</div>' if goal else '')
    source = (frame.pop(frame.reader(data["face"], root), "Source Markdown", "Open this page's Markdown")
              if data["face"] and F.inside(data["face"], root) else "")
    crumbs, cur = [frame._link("/", root.name)], root          # the path, from the SPACE down (focus_page.render)
    for part in folder.relative_to(root).parts[:-1]:
        cur /= part
        crumbs.append(frame._link(F.page_url(cur, root), part))
    crumbs.append(f'<span aria-current="page">{frame.esc(folder.name)}</span>')
    left = []
    for sibling in F.rail_kids(folder.parent, root):          # the Job's sNN and Tasks, this Task's own sNN under it
        left.append(F.rail_link(F.rail_url(sibling, root), sibling.name, sibling == folder))
        if sibling == folder:
            left += [F.rail_link(F.rail_url(child, root), child.name, False, "child")
                     for child in F.rail_kids(folder, root) if F.inside(child, root)]
    right = "".join(F.rail_link(F.page_url(folder, root, key), name, key == section, "", words)
                    for key, name, words in rail)
    page = F.page_shell(folder, root, crumbs, frame.esc(folder.name), section.title(), dict((k, w) for k, _, w in rail)[section],
                        bar, goal_html, building_view(folder, root, section, view), source, left, right,
                        [(key, name) for key, name, _ in rail], section)
    head, tail = page.rsplit("</head>", 1)
    page = head + "<style>" + (ASSETS / "decision_report.css").read_text(encoding="utf-8") + "</style></head>" + tail
    head, tail = page.rsplit("</body>", 1)
    return head + "<script>" + (ASSETS / "decision_report.js").read_text(encoding="utf-8") + "</script></body>" + tail


def render(theme, root, folder, section="", group=""):
    root, folder = Path(root).resolve(), Path(folder).resolve()
    if not F.inside(folder, root):
        raise ValueError("Folder outside root")
    if frame.level_of(folder) not in {"Job", "Task"}:
        return F.render(theme, root, folder, section, group)
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
