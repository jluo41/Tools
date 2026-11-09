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

from live import decision_report_view as DR, focus_page as F, frame, interaction_section as IX, labeling_theme as T
from live import task_labeling as TL

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
            if T.types_of(t) == ("items",):                # the items Task names its own step, never Preferences
                return (t, *_items_form_next(t, r))
            return t, "runs", f"Answer {r.name} on its Preferences step, then press Copy prompt.", ""
    answered = any("_collect_report_" in r.name and state == "done" for _, r, state in runs)
    for t, r, state in runs:
        if state == "planned" and ("score" not in T.types_of(t) or answered):
            return t, "runs", f"Press {t.name.split('_', 1)[0]} {r.name}: its ticket is ready.", ""
    meaning = next((t for t in ts if "meaning" in T.types_of(t)), None)
    if meaning and not answered:
        return meaning, "goal", "Paste the meaning Task's Report prompt into its chat session.", ""
    return _signs_next(meaning, next((t for t in ts if "expression" in T.types_of(t)), None))


def _items_form_next(task: Path, form: Path) -> tuple:
    """(view, words, note) for a form that waits in an items Task: it asks what the next step's sign rests on, so the
    words name that step (2 · Items: the recipe and its Sign; 3 · Embedding: the build and its Agree), never the
    meaning Task's Preferences step (261106)."""
    card = form / "run.yaml"
    feeds = re.findall(r"(?m)^\s*-\s*(r\d+_\S+)", card.read_text(encoding="utf-8", errors="ignore")) if card.is_file() else []
    embed = any(TL._op(task, task / "runs" / f) == "embed" for f in feeds if (task / "runs" / f).is_dir())
    key, what, verb = ("embedding", "build", "Agree") if embed else ("items", "recipe", "Sign")
    title = TL._form_title(form)
    return key, (f"Answer {title} ({form.name}), then read the {what} in {ITEM_VIEWS[key]} and press {verb}."), ""


def _signs_next(meaning, expression):
    """Past the forms and tickets, what waits is a sign, a round, or nothing (the walkthrough, 261104: a finished Job's
    page said "Prepare an items Task")."""
    from live import labeling_steps as S
    if meaning:
        loops = [lp for lp in S.MV.loops(meaning) if lp.get("map")]
        if loops and not loops[-1].get("approved"):
            return meaning, "runs", f"Sign m{loops[-1]['n']:02d} on the meaning Task's Update step.", ""
    if expression:
        runs = sorted((expression / "runs").glob("r*_release_e*")) if (expression / "runs").is_dir() else []
        if runs and S.MV.state(runs[-1]) == "done":
            round_id = runs[-1].name.rsplit("_", 1)[1]
            if S.MV.release_sign(runs[-1]):
                return expression, "runs", f"Done: {round_id} is released. Its final labels are on the Release step.", ""
            return expression, "runs", f"Sign release {round_id} on the expression Task's Release step.", ""
        return expression, "runs", "Paste the expression Task's Rewrite prompt into its chat session.", ""
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
    if section == "skills":                              # the rail's Skills section, as on every page (261106)
        return F.page_skills(folder, root, "labeling", frame.level_of(folder), False, bool(F.topic_rows(folder, root)),
                             bool(F.interactions(folder, root)), False)
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
             "interactions": ("🙋 waits on you" if any(r["state"] == "waiting" for r in inbox)
                              else "nothing waits on you" if inbox else "nothing asked yet"),
             "delivery": "what it has handed over" if delivery else "nothing handed over yet",
             "related": "what came in: meetings, papers, emails", "timeline": "what happened when",
             "files": "the folder itself", "skills": "the skills that work on it"}
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
    return DR.section(1, BUILD_VIEWS[-1][3], "".join(rows) or DR.line("No Runs yet."),
                      word=f"{len(rows)} Run{'' if len(rows) == 1 else 's'}" if rows else "nothing yet")


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
                       + DR.section(1, first, DR.big("Nothing to show yet") + DR.line(f"This view will show {caption}."),
                                    word="not built yet"))
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
    keys = [key for key, _, _ in base_rail(folder, root)]
    if section in keys and section not in OWN_SECTIONS:
        return F.render(theme, root, folder, section, group)
    section = section if section in OWN_SECTIONS else "work"
    view = group if group in views else ("decide" if DR.waiting_report(folder) else "frame")
    return task_shell(root, folder, section, views, view, building_view(folder, root, section, view),
                      "<style>" + (ASSETS / "decision_report.css").read_text(encoding="utf-8") + "</style>",
                      "<script>" + (ASSETS / "decision_report.js").read_text(encoding="utf-8") + "</script>")


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
    cls = {"ok": " fd-ok", "you": " fd-you"}
    bar = ('<nav class="section-views" aria-label="Views">' + "".join(
        f'<a href="{frame.esc(F.page_url(folder, root, section, key))}"' + (' aria-current="page"' if key == view else '')
        + f'>{frame.esc(name)}'
        + (f'<span class="vw{cls.get((words or {})[key][1], "")}">{frame.esc((words or {})[key][0])}</span>'
           if (words or {}).get(key, ("", ""))[0] else "")
        + '</a>' for key, name in views.items()) + '</nav>')
    data = F.read_face(folder, root)
    goal = data["goal"].split("\n")[0] if data["goal"] else ""
    goal_html = (f'<div class="focus-goal"><span class="goal-word">{F.GOAL_WORD.get(level, "Goal")}</span>'
                 f'{F.markdown(goal, folder, root)}</div>' if goal else '')
    source = (frame.pop(frame.reader(data["face"], root), "Source Markdown", "Open this page's Markdown")
              if data["face"] and F.inside(data["face"], root) else "")
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
# Task kept the older single-section layout; the Block's Work was one Progress view). Report and Work hold the same
# views, drawn by the same code: Report the results, Work ⚙️ Process then 📊 Results; 🙋 Interaction closes every view
# with that view's own forms; the rail is the base page's (Report · Work · Studio · Interactions · Delivery · Skills ·
# Files); every other rail section is focus_page.render's. ──────────────────────────────────────────────────────────
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

LEVEL_VIEWS = (("mindmap", "MindMap"), ("standing", "Status"), ("findings", "Findings"))
LEVEL_CAPTIONS = {"standing": {"Block": "Where its Jobs and their Tasks stand.", "Job": "Where its Tasks and Runs stand."},
                  "findings": "What it has released: the final labels, and the rules they follow."}
# an older link to a labeling Job (the single-section design's keys) still opens the nearest place
OLD_LEVEL = {"goal": ("report", ""), "tasks": ("work", "standing"), "reports": ("report", "findings"),
             "outputs": ("delivery", ""), "folders": ("files", ""), "progress": ("work", "standing"),
             "overview": ("report", "")}


def _jobs_of(folder: Path, root: Path) -> list:
    return [folder] if frame.level_of(folder) == "Job" else [j for j in frame.children(folder, "Block") if F.inside(j, root)]


def findings_html(folder: Path, root: Path) -> str:
    """Findings at a Block or a Job: what each Job has released (its expression Task's newest release: the final
    labels, signed or not) and the rules they follow (its meaning Task's approved guideline). Numbered closed bars,
    each with its state word; nothing made up where nothing is released."""
    from live import labeling_steps as S
    from live.ui_parts import _numbered, _section
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


def _task_words(task: Path, root: Path, jobs: list) -> str:
    """A Task named for a row: its title ("Example chats as items"), after its Job's few words when a Block has more
    than one Job."""
    words = F.page_title(task)
    return f"{F.job_short(task.parent, jobs, root)} › {words}" if len(jobs) > 1 and task.parent in jobs else words


def next_steps(folder: Path, root: Path, level: str, inbox: list) -> str:
    """Work › Status's Process at a labeling Block or Job: 🚧 Next steps. Every form that waits comes first, each row
    opening the form itself in the pop-out (round 4: the release choices were missing, and the row opened a Run card
    that said only "waiting"); then each Task that is not done and has no form waiting, with its next Run. The first
    waiting row stands under the closed bar (settled 2)."""
    jobs = _jobs_of(folder, root)
    li = lambda name, url, pop, note: (f'<li><a href="{frame.esc(url)}" data-pop="{frame.esc(pop)}">{frame.esc(name)}</a>'
                                       f'<small>{frame.esc(note)}</small></li>')
    rows, waiting, held = [], [], set()
    for r in inbox:
        if r.get("state") != "waiting" or r.get("form") is None or not F.inside(r["form"], root):
            continue
        page = Path(r["page"])
        held.add(page)
        words = (f"{_task_words(page, root, jobs)} › " if frame.level_of(page) == "Task" else "") + r["title"]
        rows.append(li(words, frame._file_url(r["form"], root), r["run"], "waits for you"))
        waiting.append(words)
    for job in jobs:
        for t in (t for t in frame.children(job, "Job") if F.inside(t, root) and t not in held):
            if F.state_kind(F.state_label(F.read_face(t, root)["state"])) == "✅ done":
                continue
            nxt = next(((run, mark) for run, mark, _ in F.run_rows(t) if F.mark_word(mark) != "done"), None)
            if nxt is not None:
                rows.append(li(f"{_task_words(t, root, jobs)} › {nxt[0].name}", F.run_url(nxt[0], root),
                               f"{t.name} · {nxt[0].name}", F.mark_word(nxt[1])))
    if not rows:
        return ""
    word = f"{len(waiting)} wait for you" if waiting else f"{len(rows)} to do"
    return F.band_sec(1, "🚧 Next steps", word, '<ul class=wk-rows>' + "".join(rows) + '</ul>',
                      f"🙋 {waiting[0]}" if waiting else "")


def _work_views(report: dict, folder: Path, root: Path, level: str, questions: list, inbox: list) -> dict:
    """Work's views, the Report's own drawn by the same code under ⚙️ Process then 📊 Results (focus_page.work_views'
    shape); Status's Process is labeling's Next steps (next_steps above)."""
    def view(key, body):
        def build():
            process = (next_steps(folder, root, level, inbox) if key == "standing"
                       else F.work_process(folder, root, level, key, questions, inbox))
            return (F.BAND_CSS + F.FINDINGS_CSS + (f'<h3 class=wk-band>⚙️ Process</h3>{process}' if process else '')
                    + f'<h3 class=wk-band>📊 Results</h3>{body()}')
        return build
    return {key: (name, view(key, body)) for key, (name, body) in report.items()}


def status_html(folder: Path, root: Path, level: str, topics: list, outputs: bool = False, html: str | None = None) -> str:
    """Status, focus_page's, with each Job's row on a Block saying how many of its Tasks are done, "1 of 3 done", the
    words its own page's Tasks bar says (round 4: the Block said "partly · 3 Tasks · 67%" where the Job said "2 of 3
    done"). focus_page.job_progress words every Block's rows; until it says the same, a labeling Block's are reworded."""
    html = F.status_now_html(folder, root, level, topics, outputs) if html is None else html
    if level != "Block":
        return html
    for job in _jobs_of(folder, root):
        tasks_ = [t for t in frame.children(job, "Job") if F.inside(t, root)]
        done = sum(F.state_kind(F.state_label(F.read_face(t, root)["state"])) == "✅ done" for t in tasks_)
        at = html.find(f'data-pop="{frame.esc(job.name)}"')
        end = html.find("</summary>", at) if at >= 0 else -1
        m = re.compile(r"<small>[^<]*</small>").search(html, at, end) if end > at else None
        if m:                                                # its own row's words only, in its closed bar
            html = html[:m.start()] + f"<small>{done} of {len(tasks_)} done</small>" + html[m.end():]
    return html


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
    from live.ui_parts import _kv, _numbered, _section
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


def delivery_page(theme, root, folder, group=""):
    """A labeling page's Delivery: its releases (delivery_html), in the page's own shell; the base page's when there is
    none to show."""
    body = delivery_html(folder, root)
    if not body:
        return F.render(theme, root, folder, "delivery", group)
    head, tail = _assets()
    return task_shell(root, folder, "delivery", {"overview": "Deliveries"}, "overview",
                      '<p class="view-caption">What it hands over: each signed release and its final labels.</p>'
                      f'<div class=ls-view>{body}</div>', head, tail)


def level_forms(folder: Path, view: str, inbox: list) -> list:
    """A view's own forms (settled 3): the page's own under MindMap, a form about a release (`_collect_release…`)
    under Findings beside the release it is about, every other form below the page under Status."""
    def home(r) -> str:
        if Path(r["page"]) == folder:
            return "mindmap"
        return "findings" if "_collect_release" in r["run"] else "standing"
    return [r for r in inbox if home(r) == view]


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
        items = every
        if section == "interactions" and group in ("waiting", "answered"):
            items = [r for r in every if r.get("state") == group]
        body, _ = WF.shared_bodies(folder, root, theme.name, level, None, topics, items,
                                   knows, events, items, only=section)[section]
        views = ({"all": "All", "waiting": "Needs your input", "answered": "Answered"}
                 if section == "interactions" else {"all": "All"})
        view = group if group in views else "all"
    elif section == "related":
        return F.render(theme, root, folder, section, group)
    else:
        section = "report"  # Old Work links open the combined Report.
        groups = WF.topics_for(folder, root, questions)
        views = {"overview": "Overview", "standing": "Status", "findings": "Findings", "delivery": "Delivery"}
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


ITEMS_OLD = {"goal": ("work", ""), "runs": ("work", ""), "reports": ("report", ""), "outputs": ("delivery", ""),
             "folders": ("files", ""), "context": ("report", ""), "studio-all": ("studio", "")}


def is_items(folder) -> bool:
    return frame.level_of(folder) == "Task" and T.types_of(folder) == ("items",)


def items_page(theme, root, folder, section="", group=""):
    """An items Task's focus page: Data · Items · Embedding in Report and in Work (task_labeling.items_view)."""
    views = {key: name for key, name, _ in TL.ITEM_VIEWS}
    if section in ITEMS_OLD:
        section, group = ITEMS_OLD[section][0], ITEMS_OLD[section][1] or group
    elif section in views:                                   # a step named as a section: that step, in Work
        section, group = "work", section
    rail = base_rail(folder, root)
    if section == "delivery":
        return delivery_page(theme, root, folder, group)
    if section in {k for k, _, _ in rail} - set(OWN_SECTIONS):
        return F.render(theme, root, folder, section, group)
    section = section if section in OWN_SECTIONS else "work"
    view = group if group in views else TL.items_default(folder, root)
    head, tail = _assets()
    return task_shell(root, folder, section, views, view, TL.items_view(folder, root, section, view), head, tail,
                      TL.items_words(folder, root))


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
