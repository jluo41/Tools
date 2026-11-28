"""The focus page's Plan + Results: Jobs by band, Tasks with their newest Run, the work process."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from live import frame, task_questions
from live.ui_parts import COPY_JS, PB_JS, state_mark, word_span
from live import interaction_section as IX
from live.focus_base import (band_title, face_title, inside, job_short, one_line, page_title, page_url, read_face,
    report_path, state_kind, state_label, state_words, theme_status, topic_home)
from live.focus_styles_bands import BAND_CSS, DC_CSS, FINDINGS_CSS, band_sec, numbered, side_css
from live.focus_runs import (STAGE_WORD, data_card, data_card_html, mark_word, output_run, run_headline, run_rows,
    run_url)
from live.focus_ui import ui_todo
from live.focus_jobs import band_names
from live.state_marks import WORDS
from live.focus_tree import fold_tree, output_of
from live.focus_findings import FOUND_STAGE, answer_state, output_sections
from live.focus_identity import plain_type
from live.ladder_cards import ASSETS as LC_ASSETS, row_cards


def runs_section(task: Path, root: Path, outputs: bool = False) -> tuple | None:
    """(title, word, body): every Run, its state word, its name opening its pop-out, its headline."""
    rows = run_rows(task)
    if not rows:
        return None
    cards = {r: row_cards(r, root, head or r.name) for r, _, head in rows}   # its marks and cards (JL 261116)
    items = "".join(
        f'<li>{"" if "~ask" in cards[r][0] and "wait" in (mark or "").lower() else state_mark(mark)}'
        f'<a href="{frame.esc(run_url(r, root))}" '
        f'data-pop="{frame.esc(task.name + " · " + r.name)}">{frame.esc(r.name)}</a>'
        + (f'<span class=hl>{frame.esc(head)}</span>' if head else '') + cards[r][0]
        + ((f'<details class="dc-fold"><summary>Data out</summary>{data_card_html(dc, compact=True)}</details>')
           if (dc := data_card(r)) else '') + cards[r][1] + '</li>' for r, mark, head in rows)
    words = [mark_word(m) for _, m, _ in rows]
    waiting = sum(w.startswith("waiting") for w in words)   # a waiting form is counted here and asked in 🙋 Interaction
    # a state word, never a tally (AGENTS.md § Page words): each Run's own state is on its row
    word = ("running" if "running" in words else "waits for you" if waiting
            else "done" if words and all(w == "done" for w in words) else "partly")
    css = DC_CSS if 'dc-fold' in items else ''          # a Run's data card, folded under its row (261109)
    return "🧪 Runs", word, f'{css}<ul class="wk-rows wk-runs">{items}</ul>'


def studio_section(topics: list, root: Path) -> tuple | None:
    """(title, word, body): the page's Studio topics, each by its title, its address small (round 2: "lead with the
    title, keep the address small")."""
    rows, stages = [], []
    for topic, _, facts in topics:
        if not topic.is_dir():
            continue
        stage = facts.get("stage", "")
        stages.append(STAGE_WORD.get(stage, stage))
        title = face_title(frame._notes(topic) or topic / "_") or topic.name
        # its title, then its stage in words; no mark beside the word (round 3: "⬜ beside exploring") and no folder
        # name, which its link's hover keeps
        rows.append(f'<li><a href="{frame.esc(topic_home(topic, root))}" title="{frame.esc(topic.name)}">'
                    f'<b>{frame.esc(title)}</b></a><small>{frame.esc(STAGE_WORD.get(stage, stage))}</small></li>')
    if not rows:
        return None
    return "🎨 Studio", ", ".join(f"{stages.count(w)} {w}" for w in dict.fromkeys(stages)), f'<ul class=wk-rows>{"".join(rows)}</ul>'


TASK_ROWS_CSS = """<style>
.job-row .tn{flex:1 1 auto;min-width:0}
.task-rounds{padding:0 15px 6px 22px}
.task-rr{display:grid;grid-template-columns:22px 1fr auto;gap:10px;align-items:center;padding:5px 0;border-top:1px solid var(--line);font-size:13.5px}
.task-rr:first-child{border-top:0}.task-rr small{color:var(--muted);font-size:12px;white-space:nowrap}
.task-rr.run>span{font-family:var(--mono,ui-monospace,monospace);font-size:12.5px;color:var(--muted)}.task-rr.round{padding-left:18px}
a.task-rr{color:inherit;text-decoration:none;cursor:pointer}a.task-rr:hover>span{text-decoration:underline}
.task-rr a.rr-name{color:inherit;text-decoration:none}.task-rr a.rr-name:hover{text-decoration:underline}
.task-run>summary{list-style:none;position:relative;display:block;cursor:pointer}.task-run>summary::-webkit-details-marker{display:none}
.task-run>summary::before{content:"▸";position:absolute;left:-14px;top:7px;font-size:10px;color:var(--muted)}
.task-run[open]>summary::before{content:"▾"}.task-run+.task-run,.task-run+a.task-rr,a.task-rr+.task-run{border-top:1px solid var(--line)}
</style>"""


def task_name(t: Path) -> str:
    """A Task's name on its row: `t02 · Job and Task views`, its number, then its face's title or its `# ` heading."""
    face = frame.face(t)
    words = face_title(face) if face else ""
    if not words and face and face.is_file():
        words = (re.search(r"(?m)^#\s+(.+)$", face.read_text(encoding="utf-8", errors="ignore")) or [None, ""])[1].strip()
    num = (re.match(r"t\d+", t.name) or [None])[0]
    return " · ".join(x for x in (num, words or t.name) if x)


def git_new(folder: Path):
    """A test for new work under `folder`: a path no file git tracks sits in (a Task or Run made since the last commit,
    JL 261126: "for the new runs, and new task, you can show it as well"). Outside a git work tree nothing is new."""
    import subprocess
    try:
        out = subprocess.run(["git", "-C", str(folder), "ls-files", "-z", "."], capture_output=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return lambda p: False
    if out.returncode:
        return lambda p: False
    tracked = [x for x in out.stdout.decode("utf-8", "ignore").split("\0") if x]

    def new(p: Path) -> bool:
        try:
            rel = p.relative_to(folder).as_posix() + "/"
        except ValueError:
            return False
        return not any(x.startswith(rel) for x in tracked)
    return new


def row_key(mark: str) -> str:
    """A row's effect key (fx-<key> in focus.css) from its mark."""
    from live.state_marks import state_key
    return state_key(mark) or "plan"


def round_rows(t: Path, new=lambda p: False) -> list:
    """A Task's Runs and their rounds, newest first, as (mark, title, small, hover, kind, folder): a Run with passes is
    a `run` row (its name) over one `round` row per pass (passes/pNN-MMDD/pass.md: its heading, `round N · MM-DD`, its
    Summary's first sentence on hover; the newest takes the Run's mark, an older one ✅); a Run with no pass is one
    row, its headline (JL 261126: "what does the p mean here? for the task, we hsould havethe run, right?")."""
    rows = []
    for r, mark, head in reversed(run_rows(t)):
        passes = sorted((d for d in (r / "passes").glob("*") if d.is_dir()), reverse=True) if (r / "passes").is_dir() else []
        if passes:
            rows.append((mark, r.name, "", head or "", "run", r))
        for i, d in enumerate(passes):
            text = (d / "pass.md").read_text(encoding="utf-8", errors="ignore") if (d / "pass.md").is_file() else ""
            title = (re.search(r"(?m)^#\s+(.+)$", text) or [None, d.name])[1].strip()
            title = re.sub(r"^p\d+-\d+ · ", "", title)
            summ = (re.search(r"(?ms)^## Summary\s*\n(.*?)(?=^## |\Z)", text) or [None, ""])[1]
            summ = re.split(r"(?<=[.!?])\s+", " ".join(summ.split()), maxsplit=1)[0]
            k, _, md = d.name.partition("-")
            when = f"{md[:2]}-{md[2:]}" if len(md) == 4 and md.isdigit() else md
            n = int(k[1:]) if k[1:].isdigit() else k
            rows.append((mark if i == 0 else "✅ done", title,
                         " · ".join(str(x) for x in (f"round {n}", when) if x), summ, "round", d))
        if not passes:
            # a Run git does not track yet and not run yet is new; one that ran shows what it did
            rows.append(("🆕 new" if new(r) and row_key(mark) == "plan" else mark, head or r.name, r.name, head, "run", r))
    return rows


def tasks_section(job: Path, root: Path, outputs: bool = False) -> list:
    """[(title, word, body)]: a Job's Tasks as s07's Topic rows preview draws them (JL 261125: "I want it out of the
    box"), one fold per Task group (JL 261125: "each fold here should be ... the Task group name"): a group is a tNN
    decade, named by the face's `bands:` line (`bands: t0N Page components`), as a Block's Job bands are; a face with
    no `bands:` keeps one fold, Tasks. Under each bar, a row per Task, its name and its newest round's mark; opened,
    its rounds under it."""
    tasks = [t for t in frame.children(job, "Job") if inside(t, root)]
    if not tasks:
        return []
    named = band_names(frame.face(job)) if frame.face(job) else {}
    groups = {}
    for t in tasks:
        d = re.match(r"t(\d)\d", t.name)
        groups.setdefault(d.group(1) if named and d else "", []).append(t)
    new = git_new(job)
    secs = []
    for d, ts in groups.items():
        rows, keys = "", []
        for t in ts:
            rounds = round_rows(t, new)
            # a new Run leaves its Task's own mark; a Task made since the last commit, or with only new Runs, is new
            old = [r for r in rounds if not r[0].startswith("🆕")]
            mark = ("🆕 new" if (rounds and not old) or (new(t) and all(row_key(r[0]) == "plan" for r in old))
                    else old[0][0] if old
                    else state_words(state_label(read_face(t, root)["state"])))
            keys.append(row_key(mark))
            strip, slot = row_cards(t, root, page_title(t))     # its marks and cards, as a sentence's (JL 261116)
            # a row opens in the page's viewer: a round its pass.md, a Run its Run page (JL 261126: "open the preview
            # content for that run or that pass")
            opens = lambda kind, where: (frame._file_url(where / "pass.md", root) if kind == "round" and (where / "pass.md").is_file()
                                         else run_url(where, root) if kind == "run" else "")
            link = lambda mk, title, small, hover, kind, where: (
                f'<a class="task-rr {kind} fx-{row_key(mk)}" data-path="{frame.esc(frame.rel(where, root))}" '
                f'href="{frame.esc(opens(kind, where))}" data-pop="{frame.esc(t.name + " · " + (where.name if kind == "run" else title))}" '
                f'title="{frame.esc(hover)}">{state_mark(mk) or "<span></span>"}'
                f'<span>{frame.esc(title)}</span><small>{frame.esc(small)}</small></a>')
            runs = []                     # each Run a fold of its rounds (JL 261126: "what if I have mutiple runs?")
            def head(mk, title, small, hover, kind, where):    # a Run's bar: its name opens it, the rest folds it
                return (f'<div class="task-rr {kind} fx-{row_key(mk)}" data-path="{frame.esc(frame.rel(where, root))}" '
                        f'title="{frame.esc(hover)}">{state_mark(mk) or "<span></span>"}'
                        f'<span><a class=rr-name href="{frame.esc(opens(kind, where))}" data-pop="{frame.esc(t.name + " · " + where.name)}">'
                        f'{frame.esc(title)}</a></span><small>{frame.esc(small)}</small></div>')
            for r in rounds:
                if r[4] == "run" or not runs:
                    runs.append([link(*r), [], ""])
                    runs[-1].append(head(*r))
                else:
                    runs[-1][1].append(link(*r))
                    runs[-1][2] = max(runs[-1][2], r[5].name.partition("-")[2])    # its newest round's MMDD
            runs.sort(key=lambda g: g[2], reverse=True)          # the Run with the newest round first, and open
            runs = [[g[3] if g[1] else g[0], g[1]] for g in runs]   # a Run with rounds folds; its name alone opens it
            folds = [i for i, (_, kids) in enumerate(runs) if kids]
            inner = "".join(f'<details class=task-run{" open" if folds and i == folds[0] else ""}><summary>{head}</summary>'
                            f'{"".join(kids)}</details>' if kids else head for i, (head, kids) in enumerate(runs))
            rows += (f'<details class="job-row fx-{row_key(mark)}" data-path="{frame.esc(frame.rel(t, root))}"><summary><b class=tn title="{frame.esc(t.name)}">{frame.esc(task_name(t))}</b>'
                     + strip + state_mark(mark) + f'</summary><div class=task-rounds>{inner}</div></details>{slot}')
        states = [state_kind(state_label(read_face(t, root)["state"])) for t in ts]   # job_progress's word, per group
        word = ("done" if all(k == "✅ done" for k in states) else "not run"
                if not any(k in ("✅ done", "partly done") for k in states) else "partly")
        title = named.get(d, "").strip() or "Tasks"
        # work running or waiting inside: the Files pane's pinging folder dot on the group's bar (blue, amber)
        dot = next((f'<i class="live-dot {k}" title="{WORDS[k]} inside"></i>' for k in ("edit", "you") if k in keys), "")
        secs.append((("🧱 " + title if title[:1].isalnum() else title) + dot, word, TASK_ROWS_CSS + rows))   # no progress bar
    return secs


def steps_word(notes: list) -> str:
    """A Next steps bar's word: what its rows are when they agree ("running", "planned"), else "to do". A state word,
    never a count (AGENTS.md § Page words): each row shows its own state."""
    one = set(notes)
    if len(one) == 1 and next(iter(one)) in ("running", "planned", "in progress", "not started", "failed", "blocked"):
        return notes[0]
    return "to do"


def answer_verb(row: dict, path, stage: str, folder: Path, root: Path) -> str:
    """The verb on an answer's row in Work › Findings: Agree when its answer is proposed and waits for the person,
    Write when it has none yet; each a Copy prompt for hai-report, which owns a report's answer-status (round 3:
    "agree it: dead end, no Agree anywhere")."""
    from live.ui_parts import copy_verb
    title = task_questions.words(row.get("title")) or task_questions.words(row.get("question"))
    where = frame.rel(path, root) if path else frame.rel(folder, root)
    if stage == "proposed":
        return copy_verb("Agree", f"/hai-report {where} I agree the proposed answer to \"{title}\": mark it agreed "
                                  "(answer-status: answered) and keep its words.",
                         "Copies a prompt that asks /hai-report to mark this answer agreed")
    return copy_verb("Write", f"/hai-report {where} write the answer to \"{title}\" from the Results of its work, "
                              "as proposed, for me to agree.",
                     "Copies a prompt that asks /hai-report to write this answer")


def work_process(folder: Path, root: Path, level: str, view: str, questions: list, inbox: list, start_number=1) -> str:
    """The Process band of a work page's Work view, as on a paper Board: this view's things to do, then the skills that
    do them. Each is a closed numbered section; a step with nothing in it does not show. What waits on you is the
    view's last section, 🙋 Interaction, so Process does not repeat it (JL 261105: "keep only the bottom")."""
    steps = []
    # every row carries its verb (round 3: "the rows carry no verb"): Open on a next step, Agree or Write on an answer
    li = lambda name, url, pop, note, verb="": (f'<li><a href="{frame.esc(url)}" data-pop="{frame.esc(pop)}">{frame.esc(name)}</a>'
                                                f'<small>{frame.esc(note)}</small>{verb}</li>')
    opener = lambda url, pop: f'<a class=row-verb href="{frame.esc(url)}" data-pop="{frame.esc(pop)}">Open</a>'
    todo, notes = [], []
    # each step's state word says how far it has got (JL 261106: "every closed bar shows a state word on its right")
    # the next step only, never the rows Results already show (round 2, 261106: "Process rows equal to Results' Jobs")
    unfinished = lambda t: state_kind(state_label(read_face(t, root)["state"])) != "✅ done"
    if view == "standing" and level == "Block":
        jobs = [j for j in frame.children(folder, "Block") if inside(j, root)]
        for j in jobs:
            if job_progress(j, root)[1] == "done":
                continue
            nxt = next((t for t in frame.children(j, "Job") if inside(t, root) and unfinished(t)), None)
            if nxt is not None:
                label = state_label(read_face(nxt, root)["state"])
                notes.append(mark_word(state_words(label)) if label else "no state")
                todo.append(li(f"{job_short(j, jobs, root)} › {page_title(nxt)}", page_url(nxt, root), nxt.name,
                               notes[-1], opener(page_url(nxt, root), nxt.name)))
        if todo:
            steps.append(("🚧 Next steps", steps_word(notes), '<ul class=wk-rows>' + "".join(todo) + '</ul>', ""))
    elif view == "standing" and level == "Job":
        # a form's collection Run is the view's 🙋, never a next step (cowork round 1, 261108: "repeats Interaction Q1")
        waiting = lambda page: [(r, m) for r, m, _ in run_rows(page) if mark_word(m) != "done" and "_collect_" not in r.name]
        if not any(inside(t, root) for t in frame.children(folder, "Job")):   # a Job with no Tasks (a cowork Job): its
            for r, m in waiting(folder):                                       # own Runs waiting (an email to send)
                notes.append(mark_word(m))
                todo.append(li(r.name, run_url(r, root), r.name, notes[-1], opener(run_url(r, root), r.name)))
        for t in (t for t in frame.children(folder, "Job") if inside(t, root) and unfinished(t)):
            nxt = next(iter(waiting(t)), None)
            if nxt is not None:
                notes.append(mark_word(nxt[1]))
                todo.append(li(f"{page_title(t)} › {nxt[0].name}", run_url(nxt[0], root), f"{t.name} · {nxt[0].name}",
                               notes[-1], opener(run_url(nxt[0], root), f"{t.name} · {nxt[0].name}")))
            else:
                notes.append("no Run waiting")
                todo.append(li(f"{page_title(t)} › its next Run", page_url(t, root), t.name, notes[-1],
                               opener(page_url(t, root), t.name)))
        if todo:
            steps.append(("🚧 Next steps", steps_word(notes), '<ul class=wk-rows>' + "".join(todo) + '</ul>', ""))
    elif view == "findings" and frame.theme_of(folder, root) in ("discovery", "cowork"):   # a work page has no "✍️ Answers to write
                                                 # or agree" (JL 261109: "I don't think we want them")
        proposed = []
        for r in questions:
            path = report_path(r, folder, root)
            stage = answer_state(path, str(r.get("id") or ""))[0]
            if stage != "agreed":
                title = task_questions.words(r.get("title")) or task_questions.words(r.get("question"))
                todo.append(f'<li>{frame.pop(frame.reader(path, root), title, title) if path else frame.esc(title)}'
                            f'<small>{frame.esc(FOUND_STAGE.get(stage, stage))}</small>{answer_verb(r, path, stage, folder, root)}</li>')
                if stage == "proposed":
                    proposed.append(title)
        if todo:
            word = (f'{len(proposed)} wait{"s" if len(proposed) == 1 else ""} for you' if proposed
                    else "to write")                       # no tally (JL 261113); "N wait for you" is the answer
            steps.append(("✍️ Answers to write or agree", word, '<ul class=wk-rows>' + "".join(todo) + '</ul>' + COPY_JS,
                          f"🙋 {proposed[0]}: its answer waits for your agreement" if proposed else ""))
    elif view.startswith("ui-"):                 # a theme Block's example pages: what is left to do for each kind
        steps += ui_todo(folder, root, view[3:], li)  # (JL 261105: "we should update the work as well for each tab")
    # who does it: the rail's Skills section, once per page, not a step in every view (JL 261105: "a new tab in the
    # right rail, named 'SKILL'"); VIEW_SKILLS feeds it
    if view.startswith("ui-") and steps:          # a UI view's review rounds are its own 🔍 Review band, from 1
        return ('<section class="work-section-group ui-band"><h2>🔍 Review</h2>' + "".join(
            band_sec(n, frame.esc(name), word, body, waits) for n, (name, word, body, waits) in enumerate(steps, 1)) + '</section>')
    return "".join(band_sec(n, frame.esc(name), word, body, waits) for n, (name, word, body, waits) in enumerate(steps, start_number))


def work_views(overview: dict, folder: Path, root: Path, level: str, questions: list, inbox, runs_html, topics: list, live_status=False, results_first=False) -> dict:
    """A work page's Work has the same views as its Report (JL 261104: "why we have the progress? it should have the
    same view to the report"), as on a paper Board: Process first, then Results, the Report's own view drawn by the same
    code. Status alone adds each Task's output in place; a Task's Results are its Runs with their output."""
    def view(key, body):
        def build():
            if key == "standing" and not live_status:
                results = status_now_html(folder, root, level, topics, outputs=True)
            else:
                results = body() if callable(body) else body
            process = ('' if live_status and key == 'standing' else
                       work_process(folder, root, level, key, questions, inbox(),
                                    start_number=max(1, IX.next_number(results)) if results_first else 1))
            # what waits on the person shows once, under the Process bar where its verb is (round 3: "the second 🙋 The
            # main association… line in Work › Findings")
            for line in set(re.findall(r"<p class=band-wait>.*?</p>", process)):
                results = results.replace(line, "")
            process_group = process if results_first else (f'<h3 class=wk-band>⚙️ Process</h3>{process}' if process else '')
            result_title = '📋 Review Content' if results_first else '📊 Results'
            result_group = f'<h3 class=wk-band>{result_title}</h3>{results}'
            return BAND_CSS + FINDINGS_CSS + (result_group + process_group if results_first else process_group + result_group)
        return build
    return {key: (name, view(key, body)) for key, (name, body) in overview.items()}


def job_progress(j: Path, root: Path) -> tuple:
    """(its word, word, Tasks, share, Tasks' worth done): one count for Status and the map; a state word, never a
    Task count or a percent (AGENTS.md § Page words): the bar beside it shows how far."""
    labels = [state_label(read_face(t, root)["state"]) for t in frame.children(j, "Job") if inside(t, root)]
    if not labels:                               # a Job with no Tasks (a cowork Job, one line of work) is known by its own
        kind = state_kind(state_label(read_face(j, root)["state"]))   # face's state (261106), not "not run"
        word = {"✅ done": "done", "⏳ running": "running", "partly done": "partly", "🙋 waiting on you": "waits for you",
                "⬜ open": "open"}.get(kind, "not run")
        share = 100 if word == "done" else 50 if word in ("running", "partly", "waits for you") else 0
        return word, word, 0, share, share / 100
    states = [state_kind(x) for x in labels]
    done, n = sum(k == "✅ done" for k in states), len(states)
    partly = [x for x, k in zip(labels, states) if k == "partly done"]
    # a partly Task fills its share of the bar from its own "N of M" (j61 t03: "652 of 700 complete")
    fill = done + sum(int(a) / int(b) for a, b in (re.search(r"(\d+) of (\d+)", x).groups()
                                                 for x in partly if re.search(r"(\d+) of (\d+)", x)) if int(b))
    share = round(100 * fill / n) if n else 0
    word = "done" if n and done == n else "not run" if not done and not partly else "partly"
    return word, word, n, share, fill


# a Job's type from its Tasks' task-type, in the words of b17 delivery/page-spec/job-views.md (a Job holds one kind of work)
JOB_USE_CASE = {'raw': '🗃️ Data preparation', 'description': '🗃️ Data preparation', 'describe': '🗃️ Data preparation',
                'data': '🗃️ Data preparation', 'algo': '🧪 Model training', 'fit': '🧪 Model training',
                'eval': '📏 Evaluation', 'evaluate': '📏 Evaluation', 'stata': '📈 Statistical analysis',
                'individual': '📈 Statistical analysis', 'display': '📊 Display preparation',
                'endpoint': '💻 Software development', 'agent': '💻 Software development',
                'evidence': '🧾 Evidence preparation'}


def job_type(job: Path, root: Path) -> str:
    """A Job's type: its face's `use-case:` (its emoji added from JOB_USE_CASE when the face wrote the words only), else
    the type most of its Tasks' task-type give, else ""."""
    face = job / f"{job.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    said = (re.search(r"(?m)^use-case:\s*(.+)$", text) or [None, ""])[1].strip()
    if said:
        return next((v for v in JOB_USE_CASE.values() if plain_type(v) == plain_type(said)), said)
    kinds = Counter(JOB_USE_CASE.get(frame.task_type(t) or "", "") for t in frame.children(job, "Job") if inside(t, root))
    kinds.pop("", None)
    return kinds.most_common(1)[0][0] if kinds else ""


JOB_MARK = {"done": "✅", "partly": "🔶", "running": "🏃", "waits for you": "🙋", "open": "⬜", "not run": "⬜"}


def job_row(j: Path, js: list, root: Path, outputs: bool = False) -> tuple:
    """(one Job's closed row, its word, its Tasks, its Tasks' worth done): its emoji and jNN, its name, its mark and a
    bar for how far, never a Task count or a percent; Answer on the row when a form under it waits (round 3);
    opened, its Tasks and Runs. A Block's bands and a Theme's Block sections draw the same row."""
    jf = j / f"{j.name}.md"
    jt = jf.read_text(encoding="utf-8", errors="ignore") if jf.is_file() else ""
    emoji = (re.search(r"(?m)^emoji:\s*(\S+)", jt) or [None, ""])[1]
    said, word, n, share, fill = job_progress(j, root)
    goal = one_line(read_face(j, root)["goal"], 300)
    strip, slot = row_cards(j, root, job_short(j, js, root))   # its marks and cards, as a sentence's (JL 261116)
    row = (f'<details class=job-row><summary><span class=jn>{emoji + " " if emoji else ""}{j.name[:3]}</span>'
           + f'<a href="{frame.esc(page_url(j, root))}" data-pop="{frame.esc(j.name)}" title="{frame.esc(j.name + ": " + goal)}"><b>{frame.esc(job_short(j, js, root))}</b></a>'
           + f'<small title="{frame.esc(word)}">{JOB_MARK.get(word, "⬜")}</small>' + strip +   # a mark, no
           # state word or Task count (AGENTS.md § Page words, JL 261113); the bar beside it shows how far
           f'<span class=bar><i class="{"part" if word == "partly" else ""}" style="width:{share}%"></i></span></summary>'
           f'<div class=job-tree>{fold_tree(j, root, "Job", outputs=outputs)}</div></details>{slot}')
    return row, word, n, fill


def band_board(folder: Path, root: Path, outputs: bool = False) -> str:
    """A Block's Jobs as numbered sections, one per band (j0N, j1N, ...; named by the face's `bands:` line), closed
    (JL 261104: "I prefer to me make it like the sections"): the band's name, a bar of its Tasks done, one state word.
    Opened: one row per Job, and a Job's row opens to its Tasks and Runs (JL 261104: "each job each row, and we can
    collapse them out to see the tasks and runs"; no "Next:" lines, "just delete them")."""
    face = frame.face(folder)
    text = face.read_text(encoding="utf-8", errors="ignore") if face else ""
    named = dict(re.findall(r"\bj(\d)N\s+([^·\n]+)", (re.search(r"(?m)^bands:\s*(.+)$", text) or [None, ""])[1]))
    jobs = [j for j in frame.children(folder, "Block") if inside(j, root) and re.match(r"j\d\d_", j.name)]
    bands = {}
    for j in jobs:                                   # one section per Job type (JL 261109: "here each section will be
        key = j.name[1] if named else (job_type(j, root) or "🧱 Jobs")   # the job type"): the face's `bands:` names
        bands.setdefault(key, []).append(j)          # them by jNN decade (b01: "j0N 🗄️ data · j1N 🏋️ pretraining"),
    secs = []                                        # else each Job's own type
    for number, (b, js) in enumerate(bands.items(), 1):
        cards, filled, total, marks = "", 0, 0, []
        for j in js:
            row, word, n, fill = job_row(j, js, root, outputs)
            filled, total = filled + fill, total + (n or 1)   # a Job with no Tasks counts as one
            marks.append(word)
            cards += row
        title = named.get(b, "").strip() or b                # a named band, else the Jobs' type (job_type)
        first = js[0] / f"{js[0].name}.md"
        emoji = (re.search(r"(?m)^emoji:\s*(\S+)", first.read_text(encoding="utf-8", errors="ignore")) or [None, ""])[1] if first.is_file() else ""
        if not title[:1].isalnum():                   # the face names its own emoji ("j2N 🧠 heads"); else the band's first Job's
            emoji = ""
        word = "done" if all(m == "done" for m in marks) else "not run" if all(m == "not run" for m in marks) else "partly"
        share = round(100 * filled / total) if total else 0
        secs.append(f'<details class=band-sec><summary><span class=bt>{number} ·{" " + emoji if emoji else ""} {frame.esc(band_title(title))}</span>'
                    + word_span(word) +
                    f'<span class=bar><i class="{"part" if word == "partly" else ""}" style="width:{share}%"></i></span></summary>'
                    f'<div class=band-jobs>{cards}</div></details>')
    return BAND_CSS + "".join(secs) if secs else ""


def status_now_html(folder: Path, root: Path, level: str, topics: list, outputs: bool = False) -> str:
    """Status at a Block, Job or Task, the same function in Report and Work (Work adds a Task's figure in a Job's row):
    numbered closed bars, each with its state word, keeping to the work's state (round 2, 261106). A Block: its bands of
    Jobs, then its Studio topics by their titles (261030: "I think this should state the studio and jobs/tasks
    status"). A Job: its Tasks, each one's newest headline on its closed row (the Block's look). A Task: what its newest
    Run returned (its headline, its Values or tables, its map), then its Runs. No row carries an Interaction button:
    what waits on the person is the view's 🙋 Interaction."""
    secs, head = [], ""
    own = theme_status(frame.theme_of(folder, root), folder, root, level)   # a page's own Status bars (page_module)
    if own:
        secs += own
    elif level == "Task":
        secs += output_sections(folder, root)
        runs = runs_section(folder, root, outputs)
        if runs:
            secs.append(runs + ("",))
    elif level == "Job":
        secs += [sec + ("",) for sec in tasks_section(folder, root, outputs)]
    elif level == "Block":
        head = band_board(folder, root, outputs)     # its bands, each Job's row opening to its tree (JL 261104)
        if not head:                                 # a Block whose Jobs carry no jNN_ name: the folding tree
            tree = fold_tree(folder, root, level, outputs=outputs)
            head = f'<h3 class="focus-sub">Jobs and Tasks</h3>{tree}' if tree else ""
    studio = studio_section(topics, root) if level == "Block" else None   # a Job's and a Task's: the rail's Studio
    if studio:
        secs.append(studio + ("",))
    if not head and not secs:
        return ""
    return (side_css() + LC_ASSETS + state_lead(folder, root, level) + head
            + numbered(secs, head.count("<details class=band-sec>") + 1) + PB_JS)


def state_lead(folder: Path, root: Path, level: str) -> str:
    """A Job's Status leads with its face's state line, its main point, in words (round 3: "move the face's state line
    onto Status as its main point"): "⏳ In progress · the main values are handed over; …". A Task's main point is its
    headline bar, so it has none."""
    # JL 261113: a page never says what state a thing is in ("this plan is not signed yet"); the Tasks' marks below
    # show it, so the face's state line stays on the face
    said = ""
    if not said:
        return ""
    label, _, rest = said.partition(" · ")
    m = re.match(r"^([^A-Za-z0-9]*)(.*)$", label.strip())
    words = m.group(2).strip()
    words = words[:1].upper() + words[1:].lower() if words.isupper() else words
    return (f'<p class=st-lead>{frame.esc(m.group(1).strip())} <b>{frame.esc(words)}</b>'
            + (f' · {frame.esc(rest.strip())}' if rest.strip() else "") + '</p>')
