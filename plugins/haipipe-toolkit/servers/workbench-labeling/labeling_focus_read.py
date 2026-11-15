"""What a labeling Block, Job or Task page reads: its Tasks and their Runs, the one next action, the roster, the
reports, and the engine content each view shows."""
from __future__ import annotations

import re
from pathlib import Path
from live import decision_report_view as DR, focus_page as F, frame, labeling_theme as T
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
# an older link to a building Task (the single-section design's keys) still opens the nearest place
OLD_BUILD = {"overview": ("report", ""), "reports": ("report", ""), "goal": ("report", ""), "status": ("report", ""),
             "children": ("report", ""), "runs": ("report", "runs"), "rounds": ("report", "decide"),
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
