"""r02's option previews for s55 · Job UI: Work (b17 j03 t02, JL 261031: "make detailed interaction ... I will just
check in the interaction section"): one small page per option, drawn in the workbench's own look (its focus.css) with
j03's real names, read from disk: its face's ## Tasks, each Task's goal: and state:, each Run's card, each form's title,
and the pieces b17-s04's delivery/render.yaml says a j03 Run makes. The part an option changes carries class="diff",
which the form boxes in orange.

The form shows a preview at half size in a frame 600 pixels tall, so what differs sits in that height: no goal-line (no
option changes it), compact rows, and two places side by side when an option moves something between them.

The sample Job is j03_work_workbench_pages, the Job these forms sit in. Every j03 form is built on 261031, so a form
with no answer file is drawn waiting. j03's face has no ## Deliverables: Q2 B's to-do items are drafted from its close:
line and each sNN's delivery/ui/ path (work_ui_cells.py), marked as drafted on the page.

Writes runs/r02_collect_job_work_views/option-q<N>-<k>.html; question_collection.md links each one under its option.
Rerun after changing anything here, never edit the pages:

    python build_r02_previews.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import yaml

TASK = Path(__file__).resolve().parents[1]                       # t02_job_page
JOB = TASK.parent                                                # j03_work_workbench_pages
BLOCK = JOB.parent                                               # b17_theme_work
RUN = TASK / "runs" / "r02_collect_job_work_views"
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
CRUMB = "Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work / " + JOB.name
RAIL = ["Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Files"]

CAPTIONS = {"Tasks": "Its Tasks in its face's order: where each stands and what waits.",
            "Runs": "Every Run of its Tasks, Task by Task.",
            "Deliverables": "What it must hand over, ticked from the disk. Drafted: j03's face has no "
                            "## Deliverables yet.",
            "TaskRuns": "Its Runs: what waits first.",
            "UI": "What this Job hands over, by type: one word, its current version."}
ORDER = {"wait": 0, "fail": 1, "run": 2, "todo": 3, "done": 4}  # the most urgent Run word becomes the Task's word
TASK_WORD = {"wait": "🙋 waits for you", "fail": "❗ failed", "run": "⏳ running", "todo": "⬜ not run yet",
             "done": "✅ done"}


# ── j03 from disk ─────────────────────────────────────────────────────────────────────────────────────────────────
def field(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", text)
    return m.group(1).strip() if m else ""


def first_clause(text: str) -> str:
    """The goal's first clause, as focus_page.one_line shows it on a row."""
    m = re.match(r"(.+?)(?::\s|;\s|\.\s|$)", " ".join(text.split()))
    return (m.group(1) if m else text).strip().rstrip(".")


def run_facts(run: Path) -> dict:
    """One Run as a line reads it: its card, its word by the proposed rule, and its one verb."""
    card = yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8")) or {}
    kind, rtype, status = str(card.get("kind") or ""), str(card.get("type") or ""), str(card.get("status") or "")
    passes = sorted(p.name for p in (run / "passes").glob("p*")) if (run / "passes").is_dir() else []
    form_title = ""
    if rtype == "collect":
        source = run / "question_collection.md"
        text = source.read_text(encoding="utf-8") if source.is_file() else ""
        form_title = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), run.name)
        if (run / "result" / "answer_collection.md").is_file():
            word, cls, verb = "✅ answered", "done", "Interaction"
        else:                                                   # built on 261031: it waits for JL
            word, cls, verb = "🙋 waiting", "wait", "🙋 Interaction"
    elif kind == "soft":
        if status in ("done", "closed", "complete"):
            word, cls = "✅ done", "done"
        elif passes:
            word, cls = f"⏳ pass {passes[-1].split('-')[0]}", "run"
        else:
            word, cls = f"⬜ {status or 'queued'}", "todo"
        verb = "Pass" if passes else "Ticket"
    else:                                                       # a hard compute Run: its receipt says
        runtime = run / "result" / "runtime.yaml"
        said = field(runtime.read_text(encoding="utf-8"), "status") if runtime.is_file() else ""
        word, cls = {"running": ("⏳ running", "run"), "complete": ("✅ done", "done"),
                     "failed": ("❗ failed", "fail"), "partial": ("partly done", "run")}.get(
            said, (f"⬜ {status or 'planned'}", "todo"))
        verb = "Result" if (run / "result").is_dir() else "Ticket"
    return {"name": run.name, "kind": f"{kind} · {rtype}", "word": word, "cls": cls, "verb": verb, "form": form_title}


def pieces() -> dict:
    """{task name: [(sNN address, piece name, the Run that makes it)]}: every render.yaml under b17 whose by: names a
    Run in one of j03's Tasks (b35 s01-D14: an sNN's delivery says which Run makes each piece)."""
    out: dict = {}
    for card in sorted(BLOCK.rglob("delivery/render.yaml")):
        if "result" in card.parts:                              # merged topics kept whole in result/ are history
            continue
        topic = card.parent.parent
        data = yaml.safe_load(card.read_text(encoding="utf-8")) or {}
        for piece in data.get("pieces") or []:
            by = str(piece.get("by") or "")
            parts = by.split("/")
            if len(parts) >= 4 and parts[0] == JOB.name:
                code = str(next((piece[k] for k in piece if k != "by"), ""))
                out.setdefault(parts[1], []).append(("b17-" + topic.name.split("-")[0], code.split(":")[0].strip(),
                                                     parts[-1]))
    return out


def screens_of(task: Path) -> list:
    """The delivery/ui/ paths its sNN hand over (work_ui_cells.py: s54-job-ui-report -> delivery/ui/job-report)."""
    out = []
    for topic in sorted(task.glob("s[0-9]*-*-ui-*")):
        m = re.match(r"s\d+-(block|job|task)-ui-(report|work|studio)$", topic.name)
        if m:
            out.append(f"{topic.name}/delivery/ui/{m.group(1)}-{m.group(2)}")
    return out


def load() -> list:
    face = (JOB / f"{JOB.name}.md").read_text(encoding="utf-8")
    listed = face.split("## Tasks", 1)[1] if "## Tasks" in face else ""
    made = pieces()
    tasks = []
    for name, title in re.findall(r"(?m)^\d+\.\s+(t\d+_\S+)\s+·\s+(.+?)\s*$", listed):
        folder = JOB / name
        text = (folder / f"{name}.md").read_text(encoding="utf-8")
        runs = [run_facts(r) for r in sorted((folder / "runs").iterdir())
                if r.is_dir() and (r / "run.yaml").is_file()] if (folder / "runs").is_dir() else []
        word = min((r["cls"] for r in runs), key=ORDER.get, default="todo")
        tasks.append({"name": name, "title": title, "goal": first_clause(field(text, "goal")),
                      "state": field(text, "state"), "close": field(text, "close"), "runs": runs, "word": word,
                      "makes": made.get(name, []), "screens": screens_of(folder)})
    return tasks


TASKS = load()


# ── the page, drawn small ─────────────────────────────────────────────────────────────────────────────────────────
PREVIEW_CSS = """
/* preview only: the page without its fixed rails; the right rail is drawn as one line under the path */
.focus-page.pv{max-width:900px;padding:14px 22px 30px}.pv h1{margin:6px 0 8px}
.rail-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0 0;font-size:12.5px}
.rail-line .rl-word{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.rail-line span.rli{padding:1px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted)}
.rail-line span.rli.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .section-views{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.pv .section-views span{font-size:13px;border:1px solid var(--line);border-radius:6px;padding:3px 11px;color:var(--muted)}
.pv .section-views span.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .view-caption{margin:0 0 10px;font-size:13px;color:var(--muted)}
.screens{display:grid;grid-template-columns:1fr;gap:12px;align-items:start;margin-top:10px}
.screen{border:1px solid var(--line);border-radius:10px;padding:9px 10px;background:var(--paper);min-width:0;font-size:12px}
.screen-title{font-size:14px;font-weight:700;margin:0 0 6px;overflow-wrap:anywhere}
.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:12px}
.screen .section-views{gap:4px;margin:0 0 6px}.screen .section-views span{font-size:11px;padding:1px 7px}
.screen .view-caption{font-size:11px;margin:0 0 6px}
.trow{border:1px solid var(--line);border-radius:10px;padding:8px 11px;margin:0 0 8px;background:var(--paper)}
.trow-head{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.trow-name{font-weight:700;font-size:14.5px;color:var(--ink)}.trow-title{color:var(--muted);font-size:12.5px}
.word{margin-left:auto;font-size:12.5px;white-space:nowrap}.word.wait{color:light-dark(#b35c00,#ffc078);font-weight:600}
.trow-goal{font-size:12.5px;margin:2px 0 0}
.trow-makes{font-size:12px;margin:5px 0 0}.trow-makes .mut{color:var(--muted)}
.tag{font-size:10.5px;border-radius:9px;padding:0 7px;background:var(--soft);color:var(--accent);margin:0 3px}
.verbs{display:flex;gap:6px;margin:6px 0 0;flex-wrap:wrap}
.btn{font-size:11.5px;border:1px solid var(--line);border-radius:7px;padding:1px 9px;white-space:nowrap;color:var(--ink)}
.btn.wait{border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078);background:light-dark(#fff4e6,#3a2a12)}
.rlines{margin:6px 0 0;border-top:1px solid var(--line)}
.rl{display:flex;flex-wrap:wrap;gap:2px 8px;align-items:center;padding:3px 0;border-bottom:1px dashed var(--line);font-size:11.5px}
.rl-l{min-width:0;overflow-wrap:anywhere}.rl-r{margin-left:auto;display:flex;gap:6px;align-items:center;white-space:nowrap}
.rl-name{font:11.5px ui-monospace,Menlo,monospace;overflow-wrap:anywhere}.rl-kind{color:var(--muted);font-size:10.5px}
.rl-word{white-space:nowrap}.rl-word.wait{color:light-dark(#b35c00,#ffc078);font-weight:600}
.rl-word.done{color:light-dark(#2b8a3e,#8ce99a)}
.screen .rl-name{font-size:10.5px}.screen .rl{font-size:10.5px}
.grp{font-size:11.5px;font-weight:700;margin:8px 0 1px}.grp:first-of-type{margin-top:2px}
.waits{border:1.5px solid light-dark(#ffa94d,#b35c00);background:light-dark(#fff4e6,#3a2a12);border-radius:10px;
       padding:7px 12px;margin:0 0 10px}
.waits header{display:flex;align-items:center;gap:8px;margin:0 0 3px;font-size:13px}
.waits header b{color:light-dark(#b35c00,#ffc078)}.waits header .btn{margin-left:auto}
.wl{display:flex;gap:8px;align-items:center;font-size:12px;padding:2px 0;border-top:1px solid light-dark(#ffd8a8,#7a5520)}
.wl .mut{color:var(--muted);font-size:11px}.wl .btn{margin-left:auto;font-size:11px;padding:0 8px}
.waits-line{display:flex;align-items:center;gap:8px;border:1.5px solid light-dark(#ffa94d,#b35c00);border-radius:10px;
            background:light-dark(#fff4e6,#3a2a12);padding:6px 12px;margin:0 0 10px;font-size:13px}
.waits-line b{color:light-dark(#b35c00,#ffc078)}.waits-line .btn{margin-left:auto}
.dl{border:1px solid var(--line);border-radius:8px;padding:6px 9px;margin:0 0 7px;font-size:11px}
.dl-head{display:flex;gap:6px;align-items:baseline}.dl-head b{font-size:12px}.dl-head .mut{margin-left:auto}
.dl ul{margin:2px 0 2px 14px;padding:0}.dl code{font-size:9.5px;overflow-wrap:anywhere}
.rcard{border:1px solid var(--line);border-radius:8px;padding:7px 9px;font-size:11.5px}
.rcard-head{display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}.rcard-head b{font-size:12.5px}
.rcard-word{margin-left:auto;font-size:11px;border:1px dashed var(--muted);border-radius:9px;padding:0 7px;color:var(--muted)}
.rcard-tags{font-size:10.5px;color:var(--accent);margin:5px 0 0}
.rcard .rl{font-size:11px}
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def diff(on: bool) -> str:
    return " diff" if on else ""


def rail(on: str = "Work") -> str:
    spans = "".join(f'<span class="rli{" on" if n == on else ""}">{esc(n)}</span>' for n in RAIL)
    return f'<div class="rail-line"><span class="rl-word">Right rail</span>{spans}</div>'


def views(names: list, on: str, mark: bool = False) -> str:
    buttons = "".join(f'<span class="{"on" if n == on else ""}">{esc(n)}</span>' for n in names)
    return f'<nav class="section-views{diff(mark)}" aria-label="Views">{buttons}</nav>'


def page(title: str, body: str, *, bar: str = "", caption: str = "", heading: bool = True, on: str = "Work") -> str:
    """One preview page: the path and the right rail, then (heading) the title, its view buttons and the caption."""
    top = (f'<h1>{esc(JOB.name)}<span class="h1-section">{esc(on)}</span></h1>{bar}'
           f'<p class="view-caption">{esc(caption)}</p>') if heading else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            f"<body><main class=\"focus-page pv\"><div class=\"focus-crumb\">{esc(CRUMB)}</div>"
            f"{rail(on)}{top}{body}</main></body></html>")


def screen(name: str, section: str, inner: str, *, bar: str = "", caption: str = "", mark: bool = False) -> str:
    """One place of a page drawn small, so two can sit side by side."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">{esc(name)}<span>{esc(section)}</span>'
            f'</div>{bar}{cap}{inner}</section>')


def run_line(r: dict) -> str:
    """One Run, one line: its name and kind on the left, its word and its one verb together on the right."""
    return (f'<div class="rl"><span class="rl-l"><span class="rl-name">{esc(r["name"])}</span> '
            f'<span class="rl-kind">{esc(r["kind"])}</span></span><span class="rl-r">'
            f'<span class="rl-word {r["cls"]}">{esc(r["word"])}</span>'
            f'<span class="btn{" wait" if r["verb"].startswith("🙋") else ""}">{esc(r["verb"])}</span></span></div>')


def life_words(t: dict) -> str:
    """Q4 C: plan · build · run · read · close, each read from disk as haipipe-task ref/lifecycle.md lists it."""
    plan = "✅" if t["goal"] and t["close"] and t["runs"] else "⬜"
    build = "✅" if t["runs"] else "⬜"
    run = {"wait": "🙋", "fail": "❗", "run": "⏳", "todo": "⬜", "done": "✅"}[t["word"]]
    close = "✅" if "closed" in t["state"].lower() else "⬜"
    return f"plan {plan} · build {build} · run {run} · read ⬜ · close {close}"


def word_html(t: dict, how: str = "one", mark: bool = False) -> str:
    if how == "face":
        text, cls = t["state"] or "no state", ""
    elif how == "life":
        text, cls = life_words(t), ""
    else:
        text, cls = TASK_WORD[t["word"]], t["word"]
    return f'<span class="word {cls}{diff(mark)}">{esc(text)}</span>'


def makes_html(t: dict, mark: bool = False) -> str:
    if not t["makes"]:
        return f'<p class="trow-makes{diff(mark)}"><span class="mut">makes: not named yet</span></p>'
    by = {r["name"]: r for r in t["runs"]}
    lines = "".join(f'makes <b>{esc(addr)} · {esc(piece)}</b><span class="tag">ui</span>'
                    f'<span class="mut">by {esc(run)} · {esc(by[run]["word"] if run in by else "no card")}</span>'
                    for addr, piece, run in t["makes"])
    return f'<p class="trow-makes{diff(mark)}">{lines}</p>'


def task_row(t: dict, *, word: str = "one", runs: bool = False, makes: bool = False, link_runs: bool = False,
             mark_word: bool = False, mark_runs: bool = False, mark_makes: bool = False, mark_btn: bool = False,
             mark_link: bool = False) -> str:
    """One Task as its row on the Job's Work: name, title and word; its goal; then what the option adds."""
    waits = any(r["cls"] == "wait" for r in t["runs"])
    btn = (f'<span class="btn{" wait" if waits else ""}{diff(mark_btn)}">{"🙋 " if waits else ""}Interaction</span>'
           if any(r["form"] for r in t["runs"]) else "")
    link = f'<span class="btn{diff(mark_link)}">Runs ↗</span>' if link_runs else ""
    lines = (f'<div class="rlines{diff(mark_runs)}">' + "".join(run_line(r) for r in t["runs"]) + "</div>") if runs else ""
    return (f'<article class="trow"><div class="trow-head"><span class="trow-name">{esc(t["name"])}</span>'
            f'<span class="trow-title">{esc(t["title"])}</span>{word_html(t, word, mark_word)}</div>'
            f'<p class="trow-goal">{esc(t["goal"])}</p>' + (makes_html(t, mark_makes) if makes else "")
            + lines + (f'<div class="verbs">{btn}{link}</div>' if btn or link else "") + "</article>")


def rows(**kw) -> str:
    return "".join(task_row(t, **kw) for t in TASKS)


def runs_view() -> str:
    """Q1 B's Runs view: every Run, Task by Task, one line each."""
    return "".join(f'<p class="grp">{esc(t["name"])}</p>' + "".join(run_line(r) for r in t["runs"]) for t in TASKS)


def waits_section(mark: bool = True) -> str:
    """Q3 A: every form, sign or Run waiting on the person at the Job or below, each with its verb; Answer all opens
    the combined page. Named Interactions, as b16's version Work and s52's pick name the same box."""
    lines = "".join(f'<div class="wl"><span>{esc(r["form"])}</span><span class="mut">{esc(t["name"])}</span>'
                    '<span class="btn wait">Answer</span></div>'
                    for t in TASKS for r in t["runs"] if r["cls"] == "wait")
    return (f'<section class="waits{diff(mark)}"><header><b>🙋 Interactions</b>'
            f'<span class="btn wait">Answer all</span></header>{lines}</section>')


def deliverables_view() -> str:
    """Q2 B's Deliverables view, drafted for j03 from its close: line and each sNN's delivery/ui/ path; all ☐."""
    out = []
    for t in TASKS:
        files = "".join(f"<li><code>{esc(t['name'])}/{esc(f)}</code></li>" for f in t["screens"])
        out.append(f'<div class="dl"><div class="dl-head"><b>☐ {esc(t["title"])}: its three screens</b>'
                   f'<span class="mut">{esc(t["name"])}</span></div><ul>{files}</ul></div>')
    return "".join(out)


def report_ui() -> str:
    """Q2 C's other place: the Job's Report by type (s54's cell), the sNN this Job makes and its pieces."""
    made = [(addr, piece, t["name"]) for t in TASKS for addr, piece, _ in t["makes"]]
    addr = made[0][0] if made else "b17-s04"
    lines = "".join(f'<div class="rl"><span class="rl-name">{esc(piece)}</span>'
                    f'<span class="rl-kind">by {esc(task)}</span></div>' for _, piece, task in made)
    return (f'<div class="rcard"><div class="rcard-head"><b>{esc(addr)} · Workbench page structure</b>'
            f'<span class="tag">ui</span><span class="rcard-word">planned</span></div>{lines}'
            '<p class="rcard-tags">Slide · Draw · Mind map · Work · Delivery</p></div>')


def previews() -> dict:
    out = {}
    tasks_bar, tasks_cap = views(["Tasks"], "Tasks"), CAPTIONS["Tasks"]
    # Q1 · where a Task's Runs show: under its row, a Runs view, or only on the Task's own page
    out["q1-a"] = page("Q1 A", rows(runs=True, mark_runs=True), bar=tasks_bar, caption=tasks_cap)
    out["q1-b"] = page("Q1 B", '<div class="screens">'
                       + screen(JOB.name, "Work", rows(), bar=views(["Tasks", "Runs"], "Tasks", mark=True),
                                caption=CAPTIONS["Tasks"])
                       + screen(JOB.name, "Work", runs_view(), bar=views(["Tasks", "Runs"], "Runs"),
                                caption=CAPTIONS["Runs"], mark=True) + "</div>", heading=False)
    first = TASKS[0]
    task_page = "".join(run_line(r) for r in sorted(first["runs"], key=lambda r: ORDER[r["cls"]]))
    out["q1-c"] = page("Q1 C", '<div class="screens">'
                       + screen(JOB.name, "Work", rows(link_runs=True, mark_link=True), bar=tasks_bar,
                                caption=CAPTIONS["Tasks"])
                       + screen(first["name"], "Work", task_page, bar=views(["Runs"], "Runs"),
                                caption=CAPTIONS["TaskRuns"], mark=True) + "</div>", heading=False)
    # Q2 · where what each Task hands over shows: on its row, a Deliverables view, or the Report by type
    out["q2-a"] = page("Q2 A", rows(makes=True, mark_makes=True), bar=tasks_bar, caption=tasks_cap)
    out["q2-b"] = page("Q2 B", '<div class="screens">'
                       + screen(JOB.name, "Work", rows(), bar=views(["Tasks", "Deliverables"], "Tasks", mark=True),
                                caption=CAPTIONS["Tasks"])
                       + screen(JOB.name, "Work", deliverables_view(), bar=views(["Tasks", "Deliverables"], "Deliverables"),
                                caption=CAPTIONS["Deliverables"], mark=True) + "</div>", heading=False)
    out["q2-c"] = page("Q2 C", '<div class="screens">'
                       + screen(JOB.name, "Work", rows(), bar=tasks_bar, caption=CAPTIONS["Tasks"])
                       + screen(JOB.name, "Report", report_ui(), bar=views(["MindMap", "UI"], "UI"),
                                caption=CAPTIONS["UI"], mark=True) + "</div>", heading=False)
    # Q3 · what sits first: every waiting form in one place, nothing extra, or one line
    out["q3-a"] = page("Q3 A", waits_section() + rows(), bar=tasks_bar, caption=tasks_cap)
    out["q3-b"] = page("Q3 B", rows(mark_btn=True), bar=tasks_bar, caption=tasks_cap)
    out["q3-c"] = page("Q3 C", '<div class="waits-line diff"><b>🙋 Forms wait for you below</b>'
                       '<span class="btn wait">Answer all</span></div>' + rows(), bar=tasks_bar, caption=tasks_cap)
    # Q4 · the word that says where a Task stands
    for key, how in (("a", "one"), ("b", "face"), ("c", "life")):
        out[f"q4-{key}"] = page(f"Q4 {key.upper()}", rows(word=how, mark_word=True), bar=tasks_bar, caption=tasks_cap)
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/ from {len(TASKS)} Tasks: "
          + ", ".join(f'{t["name"]} ({len(t["runs"])} Runs, word {t["word"]}, makes {len(t["makes"])})' for t in TASKS))


if __name__ == "__main__":
    main()
