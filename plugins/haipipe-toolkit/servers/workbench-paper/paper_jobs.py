"""A paper Board's evidence and submission Jobs on their own pages (JL 261106: "the evidence and submission Jobs use an
old page shape"): their Tasks were meant to show only inside the version's and the Board's views, so each fell back to
the frame's old Progress view. Now each has Report views, the Results alone, and the same views in Work, ⚙️ Process
then 📊 Results, drawn from the Board's own pieces so the pages agree:

    display Job      Plan · Displays · Examples
    value Job        Values · Check
    citation Job     Citations · Check
    submission Job   Cover letter · Portal

focus_page.py asks job_views; the captions go in board_read.PAPER_CAPTIONS. Read-only: nothing here writes."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import (BOARD_CSS, GROUP_CSS, PB_CSS, PB_JS, PROCESS, RESULTS, _band, _cap, _numbered, _open_btn,
                           _plan_html, _section, todo_section)
from live.focus_draft import CSS, JS
from live.board_read import PAPER_CAPTIONS, _field, _num, _section_state, _state_words, _task_url, is_version
from live.address_links import linked_views, page_linker


def job_kind(job: Path) -> str:
    """Which evidence or submission Job this is, by its name (board_read.is_version's words), or "" for a version."""
    name = job.name.lower()
    if is_version(job):
        return ""
    if "submission" in name:
        return "submission"
    if "display" in name:
        return "display"
    if "value" in name:
        return "value"
    if re.search(r"cite|citation", name):
        return "citation"
    return ""


# (key, button, what its Results show) of each kind; Work's keys are `work-<key>`
VIEWS = {"display": (("display-plan", "Plan"), ("display-list", "Displays"), ("display-examples", "Examples")),
         "value": (("value-list", "Values"), ("value-check", "Check")),
         "citation": (("cite-list", "Citations"), ("cite-check", "Check")),
         "submission": (("letter", "Cover letter"), ("portal", "Portal"))}


CAPTIONS = {"display-plan": "How each display is planned against the venue's rules: the display plan's drawing.",
            "display-list": "Each display as the paper prints it, Main then the appendix.",
            "display-examples": "The target venue's published displays on one canvas, to compare with ours.",
            "value-list": "The printed numbers: each raw table and the values the text can quote.",
            "value-check": "Every printed number of the paper checked at once, against its returned Result.",
            "cite-list": "The citations, one Task per claim group, each paper checked.",
            "cite-check": "Every citation of the paper checked at once: its key, its card and its record.",
            "letter": "The cover letter the portal takes, from the writing Job's own letter Section.",
            "portal": "Everything the portal asks beside the manuscript, each field ready to check and paste."}
PAPER_CAPTIONS.update(CAPTIONS)
PAPER_CAPTIONS.update({"work-" + k: v for k, v in {
    "display-plan": "The display plan: its prompt, then its drawing.",
    "display-list": "Where each display stands, then each display.",
    "display-examples": "The venue's published displays, to compare with ours.",
    "value-list": "Where each value Task stands, then the tables and values.",
    "value-check": "The check's Run, then what it found.",
    "cite-list": "Where each citation Task stands, then each one.",
    "cite-check": "The check's Run, then what it found.",
    "letter": "The letter Section's next step, then the letter.",
    "portal": "The portal's walk and fill, then the fill page."}.items()})


def _run_pill(task: Path) -> tuple:
    """(pill, headline) of a Task's newest Run: done, running, waiting for you or not started."""
    runs = sorted(d for d in (task / "runs").glob("r[0-9]*") if d.is_dir()) if (task / "runs").is_dir() else []
    if not runs:
        return "not started", ""
    last = runs[-1]
    text = "".join(f.read_text(encoding="utf-8", errors="ignore") for f in (last / "result" / "runtime.yaml", last / "run.yaml")
                   if f.is_file())
    st = (re.search(r"(?m)^status:\s*(\S+)", text) or [None, ""])[1].lower()
    head = last / "result" / "headline.txt"
    line = head.read_text(encoding="utf-8", errors="ignore").strip().split("\n")[0] if head.is_file() else ""
    pill = ("done" if st in ("done", "complete", "completed", "ok", "succeeded") else "running" if st in ("running", "queued")
            else "waiting for you" if st == "waiting" else "starter, not walked" if st.startswith("starter") else "not started")
    return pill, line.split(": ", 1)[-1]


def _check_task(job: Path) -> Path | None:
    return next((t for t in sorted(job.glob("t99_*")) if t.is_dir()), None)


def _where_rows(tasks: list, root: Path) -> list:
    from live.evidence_read import where_rows
    return where_rows(tasks, root)


def _check(job: Path, root: Path, work: bool) -> tuple:
    """A whole-paper check's (Process, Results): its Run's state; then what it found, each row drawn (no framed page:
    it cut off its last rows), the count line once, what to fix first under the closed bar, its page one Pop out away."""
    from live import evidence_read as er
    from live.board_evidence import check_word, evidence_body
    task = _check_task(job)
    if task is None:
        return "", _section("🔎 Check", '<p class=mut>No check Task yet: a <code>t99_</code> Task runs the whole-paper check '
                                       '(haipipe-paper-evidence).</p>', "nothing yet")
    pill, line = _run_pill(task)
    data = er.value_data(task)
    if data.get("rows"):                         # the value check: what differs, each printed number
        word, waits = er.value_state(data)
        line = er.value_line(data)
        body = er.value_check_html(data, task, root)
    else:                                        # the citation check: each key once
        rows = er.cite_rows(task)
        word, waits = er.cite_state(rows) if rows else (check_word(evidence_body(task, root)[1]), "")
        line = er.cite_line(rows) if rows else line
        body = er.cite_panel(task, root) if rows else evidence_body(task, root)[2]
    # the count line is said once, in the Results (r02: three times in Work · Check); the Process row says what the Run does
    says = (re.search(r"(?m)^says:\s*(.+?)\s*$", "".join(f.read_text(encoding="utf-8", errors="ignore")
                                                           for f in sorted(task.glob("runs/*/run.yaml"))[-1:])) or [None, ""])[1]
    proc = todo_section("⚙️ The check's Run", [("Run the whole-paper check", says, pill, "Open", _task_url(task, root), False)])
    proc += _bind_prompt(job, root) if data.get("rows") else ""
    return proc, _section("🔎 Check", body + f'<p><a class=fd-btn href="{esc(_task_url(task, root))}">Open {esc(task.name)} ↗</a></p>',
                          word, waits)


def _bind_prompt(job: Path, root: Path) -> str:
    """The value Job's proposed bindings as a Copy prompt (r02: a check card's Note held the command "tick, then bind
    --adopt"): the page says a proposal waits for your tick; the command rides the prompt."""
    from live.ui_parts import prompt_box
    props = [t for t in sorted(job.parent.glob("j[0-9]*_*/t[0-9]*_*/evidence/proposals.md"))
             if re.search(r"(?m)^- \[[ xX]\] bind VALUE", t.read_text(encoding="utf-8", errors="ignore"))]
    if not props:
        return ""
    rel = ds._rel(job, root)
    how = (f"Use /haipipe-paper-evidence. The value bindings the search proposed wait in "
           + ", ".join(ds._rel(f, root) for f in props) + ". Read each, tell me which to tick, and after I tick them run "
           f"values_ledger.py bind {rel} --adopt, then rerun the value Runs' tickets. Change no Result by hand.")
    from live.board_process import behind_copy
    return _section("🔗 Bind the proposed values", behind_copy(prompt_box(how, (), step="bind", asks="adopt the ticked proposals",
                                                                          key=f"{rel}#bind")), "waits for your tick")


def _letter_task(job: Path) -> Path | None:
    """The letter Section: the submission Task's `words-in:`, else the version's own letter Task (t3N_*letter*)."""
    text = next((f.read_text(encoding="utf-8", errors="ignore") for f in sorted(job.glob("t[0-9]*_*letter*/t*.md"))), "")
    ref = _field(text, "words-in")
    if ref:
        hit = (next(iter(sorted(job.glob("t[0-9]*_*letter*"))), job) / ref).resolve()
        if hit.is_dir():
            return hit
    version = _field(_face_text(job), "for")
    return next(iter(sorted((job.parent / version).glob("t3[0-9]_*letter*"))), None) if version else None


def _face_text(job: Path) -> str:
    f = job / f"{job.name}.md"
    return f.read_text(encoding="utf-8", errors="ignore") if f.is_file() else ""


def _letter(job: Path, root: Path, work: bool) -> tuple:
    from live.board_results import _section_read, text_word
    task = _letter_task(job)
    if task is None:
        return "", _section("✉️ Cover letter", "<p class=mut>No letter Section yet: the writing Job's "
                                               "<code>t3N_cover-letter</code> holds the letter's words.</p>", "nothing yet")
    say = _state_words(_section_state(task, root))
    step, _, st = say.partition(": ")
    pill = "done" if say == "done" else "waiting for you" if "your" in st else st or "not started"
    proc = todo_section("✍️ The letter Section", [(f"{task.parent.name} · {task.name}", f"next: {step}" if say != "done" else "",
                                                   pill, "Open", _task_url(task, root), False)])
    pdf = next(iter(sorted(job.parent.glob(f"delivery/*/{task.name}/word/{task.name}.pdf"))), None)
    shown = (f'<div class=pb-verbs>{_open_btn("Open the letter PDF", "/" + quote(ds._rel(pdf, root)), pdf.name)}</div>'
             if pdf is not None else "")
    # one word in Report and Work (r01: "1 of 1 written" in Report, "waits for you" in Work): the letter's own step first
    word, waits = ("waits for you", f"🙋 {task.parent.name} · {task.name}: {say}") if "your" in st else (text_word([task]), "")
    return proc, _section("✉️ Cover letter", shown + f'<div class=pb-verbs>{_open_btn("Open the Section", _task_url(task, root), task.name)}</div>'
                          + _section_read(task, root), word, waits)


PORTAL_MARK = {"keep": "✅ in the draft", "paste": "✏️ paste this", "upload": "📎 upload this file", "ask": "🙋 you decide",
               "differ": "❗ disagrees", "missing": "⬜ no file yet"}


def portal_survey(job: Path) -> dict:
    """haipipe-paper's portal_fill.survey of a submission Job (the walk's fields, the values, the build), read only; {}
    when the Job has no walk or no values yet."""
    import importlib
    import sys
    from host_paths import skill_dir
    scripts = str(skill_dir("haipipe-paper") / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    try:
        return importlib.import_module("portal_fill").survey(job)
    except (SystemExit, Exception):
        return {}


def portal_fields_tabs(s: dict, eid: str) -> tuple:
    """(side tabs, the field that disagrees or None) of a portal survey: one tab per portal step, the step holding a
    field that disagrees first and that field first in it; one row per field, its label, what to put there and its
    state, the portal's own words on hover (r02: the fields sat in a framed page with its own look)."""
    steps: dict = {}
    for r in s.get("rows") or []:
        steps.setdefault(re.sub(r"^\d+\s+", "", str(r.get("step", ""))), []).append(r)
    rank = lambda r: {"differ": 0, "missing": 1, "ask": 2, "upload": 3, "paste": 4, "keep": 5}.get(r["state"], 6)
    order = sorted(steps, key=lambda k: (min(rank(r) for r in steps[k]) != 0, list(steps).index(k)))
    items, panels, clash = [], [], None
    for k in order:
        rows = sorted(steps[k], key=rank)
        bad = sum(r["state"] in ("differ", "missing") for r in rows)
        ask = sum(r["state"] == "ask" for r in rows)
        word = (f"{bad} to fix" if bad else f"{ask} for you to decide" if ask else "ready")
        items.append((k, word))
        out = ""
        for r in rows:
            f, v = r["f"], r["v"]
            if r["state"] == "differ" and clash is None:
                clash = r
            what = (r["path"].name if r.get("path") is not None else "") or r.get("text") or r.get("ask") or ""
            hover = " · ".join(x for x in (f.get("says", ""), f"the portal now: {r['now']}" if r.get("now") else "", v.get("note", "")) if x)
            out += (f'<div class=fd-row title="{esc(hover)}"><span class=n>{esc(f.get("label", ""))}'
                    + ("" if f.get("required") else " <small class=mut>optional</small>") + '</span>'
                    f'<span class=d>{esc(what)}' + (f'<br><small class=mut>{esc(v.get("note", ""))}</small>' if r["state"] == "differ" and v.get("note") else "")
                    + f'</span><span class="w {"fd-you" if r["state"] in ("differ", "missing", "ask") else "fd-ok" if r["state"] == "keep" else ""}">'
                    f'{esc(PORTAL_MARK.get(r["state"], r["state"]))}</span></div>')
        panels.append(out)
    from live.ui_parts import _side_tabs
    return (_side_tabs(eid, items, panels) if items else ""), clash


def _portal(job: Path, root: Path, work: bool) -> tuple:
    from live.board_results import _portal as packet, portal_word
    version = _field(_face_text(job), "for")
    vdir = job.parent / "delivery" / version if version else None
    rows = []
    for t in sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir() and "letter" not in x.name), key=_num):
        pill, line = _run_pill(t)
        says = (re.search(r"(?m)^says:\s*['\"]?(.+?)['\"]?\s*$", "".join(f.read_text(encoding="utf-8", errors="ignore")
                                                                     for f in sorted(t.glob("runs/*/run.yaml"))[-1:])) or [None, ""])[1]
        rows.append((_cap(re.sub(r"^t\d+_", "", t.name).replace("-", " ")), says, pill, "Open", _task_url(t, root), False))
    proc = todo_section("🧭 Walk and fill", rows) if rows else ""       # what each Run does; the tally is the Results'
    fill = job.parent / "delivery" / job.name / "portal-fill.html"
    table = job.parent / "delivery" / "delivery.md"
    sent = table.is_file() and any(job.name in ln and "sent" in ln.lower() for ln in table.read_text(encoding="utf-8").splitlines())
    s = portal_survey(job)
    tabs, clash = portal_fields_tabs(s, "jpf")
    body = (packet(vdir, root) if vdir is not None else "") + tabs
    if fill.is_file():                           # the fill page itself, one Pop out away, never framed (r02)
        body = (f'<div class=pb-verbs>{_open_btn("⤢ Pop out the fill page", "/" + quote(ds._rel(fill, root)), fill.name)}</div>'
                + body)
    if not body:
        return proc, _section("📮 Portal", "<p class=mut>No fill page yet: haipipe-paper <code>portal_fill.py</code> builds "
                                           f"<code>delivery/{esc(job.name)}/portal-fill.html</code>.</p>", "nothing yet")
    # a person checks every field and presses Submit themselves (the Job's close): until `sent`, it waits on them
    word = "sent" if sent else "waits for you" if fill.is_file() or tabs else portal_word(vdir)
    n = s.get("tally") or {}
    said = ", ".join(f"{n[k]} {PORTAL_MARK[k].split(' ', 1)[1]}" for k in ("differ", "missing", "ask", "upload", "paste", "keep") if n.get(k))
    decide = n.get("ask", 0)
    # the waiting line names the field that disagrees (r02: it counted one and named none)
    waits = "" if sent else (
        f"🙋 {clash['f'].get('label', '')}: the portal and the manuscript disagree"
        + (f" ({clash['v'].get('note', '').removeprefix('placeholder: ')})" if clash["v"].get("note") else "")
        + (f"; {decide} more for you to decide" if decide else "") if clash else
        f"🙋 {decide} fields for you to decide, then press Submit in the portal yourself" if decide else
        "🙋 Check every field, then press Submit in the portal yourself")
    if said:                                     # the tally, said once
        body = f'<p class=pb-state>{len(s.get("rows") or [])} portal fields: {esc(said)}</p>' + body
    return proc, _section("📮 Portal", body, word, waits)


def _display(key: str, job: Path, root: Path, work: bool) -> tuple:
    from live.board_results import _display_examples, _evidence_kinds, _stage, _topic_canvas
    from live.board_process import _plan_steps, _steps, read_board
    board = job.parent
    if key == "display-plan":
        plan = _topic_canvas(board, root, "paper-displays")
        step = [s for s in _plan_steps(board, root) if s[0].startswith("🖼️")]
        session = _field(read_board(board), "session") if (board / "board.md").is_file() else ""
        from live.board_process import behind_copy
        proc = _section("🧭 Plan the displays", behind_copy(_plan_html(step, session, key=f"plan:{ds._rel(board, root)}")),
                        f"runs in {session}" if session else "1 prompt") if step else ""
        topic = next((t for t in sorted(board.glob("s[0-9]*-paper-displays")) if t.is_dir()), None)
        return proc, _section("📐 Plan", plan or "<p class=mut>No display plan drawn yet: the Board topic "
                              "<code>sNN-paper-displays</code> (haipipe-paper-plan).</p>", (_stage(topic) or "drawn") if plan else "nothing yet")
    if key == "display-list":
        head, rows = _steps(board, "displays", None, "", root, lambda t, b: t)
        proc = todo_section(f"🖼️ {head}", rows) if rows else ""
        res, _ = _evidence_kinds(board, root, ("Displays",))
        res = _not_here(res, job, root)
        return proc, res or _section("🖼️ Displays", "<p class=mut>No display Task yet.</p>", "nothing yet")
    examples = _display_examples(board, root)
    return "", _section("🔍 Examples", examples or "<p class=mut>No examples yet. The target venue's published displays go "
                        "on one canvas, the Board topic <code>sNN-paper-display-examples</code>.</p>",
                        "drawn" if examples else "nothing yet")


def _not_here(html: str, job: Path, root: Path) -> str:
    """The Board's section without its "Open <this Job>" button: on the Job's own page it only reopened the page (r02)."""
    return html.replace(_open_btn(f"Open {job.name}", _task_url(job, root)), "")


def _items(kind: str, job: Path, root: Path, work: bool) -> tuple:
    """Values or Citations: where each Task stands, then the Board's own section for them (side tabs, the whole-paper
    check once as a verdict line; never a tab of its own: the Check view owns it)."""
    from live.board_results import _evidence_kinds
    from live.evidence_read import item_tasks
    tasks = sorted(item_tasks(job), key=_num)
    proc = todo_section("📋 Where each stands", _where_rows(tasks, root)) if tasks else ""
    res, _ = _evidence_kinds(job.parent, root, (kind,), check=False)   # the Check view beside it owns the whole-paper
    res = _not_here(res, job, root)
    return proc, res or _section(("🔢 " if kind == "Values" else "📚 ") + kind,   # line (r02: it showed in both)
                                 "<p class=mut>No Task yet.</p>", "nothing yet")


def job_views(job: Path, root: Path, work: bool) -> dict:
    """{key: (name, builder)} of an evidence or submission Job: Report's (`work` False) its Results alone, Work's
    `work-<key>` ⚙️ Process then 📊 Results; {} for any other Job."""
    kind = job_kind(job)
    if not kind:
        return {}
    from live.board_views import PAGE_CSS, SIDE_CSS
    from live.paper_version import VERSION_CSS

    def build(key):
        if kind == "display":
            proc, res = _display(key, job, root, work)
        elif key in ("value-list", "cite-list"):
            proc, res = _items("Values" if kind == "value" else "Citations", job, root, work)
        elif key in ("value-check", "cite-check"):
            proc, res = _check(job, root, work)
        elif key == "letter":
            proc, res = _letter(job, root, work)
        else:
            proc, res = _portal(job, root, work)
        body = (_band(PROCESS, _numbered(proc)) + _band(RESULTS, _numbered(res))) if work else _numbered(res)
        return CSS + BOARD_CSS + VERSION_CSS + GROUP_CSS + PB_CSS + SIDE_CSS + PAGE_CSS + body + PB_JS + JS
    pre = "work-" if work else ""
    views = {pre + key: (name, lambda key=key: build(key)) for key, name in VIEWS[kind]}
    if not work:                                 # its own map first: each Task by its title (focus_page keeps it first)
        views = {"mindmap": ("MindMap", lambda: job_mindmap(job, root)), **views}
    return linked_views(views, _linker(job, root))


def task_title(task: Path) -> str:
    """What a page calls an evidence or submission Task: a display's printed number and name ("Table 1 · <Patients> at
    baseline"), else its label, else its face's title, never only its folder name (r02: MindMap cards read
    "figure1-example")."""
    text = _face_text(task)
    first = text.split("\n", 1)[0]
    num, name, label = _field(text, "number"), _field(text, "name"), _field(text, "label")
    if num:
        return f"{num} · {name or label}" if (name or label) else num
    if label and label.lower() not in ("values", "citations"):
        return _cap(label)
    return first.split(" · ", 1)[1].strip() if " · " in first else _cap(re.sub(r"^t\d+_", "", task.name).replace("-", " "))


def job_mindmap(job: Path, root: Path) -> str:
    """An evidence or submission Job's map (r02: folder names, leaves cut at the frame's edge): one branch per Task, its
    title and state; under it what it must find out (a display's caption, a value group's goal, a claim group's
    question) and its page."""
    try:
        from live import frame
        from live.paper_version import paper_map
        from live.evidence_read import task_state
        from live.address_links import href
        frame.mindmap_module()
        import mmbuild
        kids = []
        for t in sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir()), key=_num):
            text = _face_text(t)
            finds = _field(text, "caption") or _field(text, "goal") or _field(text, "answers")
            line, pill = task_state(t, _field(text, "status"))
            line = re.sub(r"\s*\(.*\)$", "", line or "")      # "drawn 2026-11-06 (placeholder …)" -> "drawn 2026-11-06"
            state = line if line and len(line) < 40 else pill
            leaves = ([mmbuild.built(f"{job.name}/{t.name}/finds", f"[finds out] {finds}")] if finds else []) + \
                     [mmbuild.built(f"{job.name}/{t.name}/page", f"[page] [{t.name}]({href(t, root)})")]
            kids.append(mmbuild.built(f"{job.name}/{t.name}", f"{task_title(t)} · {state}" if state else task_title(t), leaves))
        goal = _field(_face_text(job), "goal")
        return paper_map(job.name, kids, [goal] if goal else [], key=job.name)
    except Exception:                            # a map that does not draw never takes the page down
        import traceback
        traceback.print_exc()
        return '<p class=mut>The map does not draw yet.</p>'


def _linker(job: Path, root: Path):
    """The page's address links; a submission Job's Section names resolve in the version it is for first (r01: its
    t31_cover-letter link opened the newest version's letter, j12, not this send's j11)."""
    version = _field(_face_text(job), "for")
    if not version or not (job.parent / version).is_dir():
        return page_linker(job, root)
    from live.address_links import linkify, paper_board_of, project_of, writing_jobs
    sections = [job.parent / version] + [j for j in writing_jobs(paper_board_of(job)) if j.name != version]
    project = project_of(job, root)

    def link(text):
        try:
            return linkify(text, project, root, sections, "_top", here=job)
        except Exception:
            return text
    return link
