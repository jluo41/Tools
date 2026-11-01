"""r03's option previews (s52 · Block UI: Work): one small page per option, drawn in the workbench's own look (its
focus.css, inlined) with b17's real names, read from disk each run: the Block face's Jobs, each Job face's goal and
## Tasks, each Task face's title and state, every Run card under the Block, every form's title, for: line and
questions, each sNN's delivery/render.yaml (which Job makes it) and its Open list. The part an option changes carries
class="diff", which the form boxes in orange (haipipe-interaction, "The difference sits in the frame").

The form shows a preview at half size in a frame 600 page pixels tall, so: no Purpose line (no option changes it),
compact rows, the parts no option of that question changes left out, and two places side by side (the top of
Progress and further down) when an option changes both ends of the view.

The nine j03 view forms (r02 to r04 in t01_block_page, r01 to r03 in t02_job_page and t03_task_page) are drawn
waiting, as they will be once their agents build them (261031); every other Run is drawn as its card says.

Writes runs/r03_collect_block_work_views/option-q<N>-<k>.html; question_collection.md links each one under its
option. Rerun after changing anything here, never edit the pages:

    python build_r03_previews.py
"""
from __future__ import annotations

import html
import re
from collections import Counter
from datetime import date
from pathlib import Path

import yaml

TASK = Path(__file__).resolve().parents[1]                       # t01_block_page
BLOCK = TASK.parents[1]                                          # b17_theme_work
RUN = TASK / "runs" / "r03_collect_block_work_views"
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
CRUMB = "Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work"
CAPTION = "What waits on you, then each Job and where its Tasks stand."
EXPECTED = {("t01_block_page", "r02_collect_block_report_views"), ("t01_block_page", "r03_collect_block_work_views"),
            ("t01_block_page", "r04_collect_block_studio_views"), ("t02_job_page", "r01_collect_job_report_views"),
            ("t02_job_page", "r02_collect_job_work_views"), ("t02_job_page", "r03_collect_job_studio_views"),
            ("t03_task_page", "r01_collect_task_report_views"), ("t03_task_page", "r02_collect_task_work_views"),
            ("t03_task_page", "r03_collect_task_studio_views")}
ORANGE = "#b35c00"


# ── reading the disk ───────────────────────────────────────────────────────────────────────────────────────────────
def esc(text) -> str:
    return html.escape(str(text), quote=True)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""


def face(folder: Path) -> str:
    return read(folder / ("board.md" if folder == BLOCK else f"{folder.name}.md"))


def field(text: str, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", text)
    return m.group(1) if m else ""


def title_of(text: str) -> str:
    """A face's own title, the words after ' · ' on its first line (focus_page.face_title)."""
    first = text.splitlines()[0] if text.strip() else ""
    return first.split(" · ", 1)[1].strip() if " · " in first else ""


def short(name: str, words: int = 3) -> str:
    """frame._short: the folder's name without its number, its first words, '-' and '.' as '_'."""
    rest = re.sub(r"^[bjtsr]\d+[_-]?", "", name)
    rest = "_".join(re.split(r"[_.-]+", rest)[:words]) if words else re.sub(r"[.-]+", "_", rest)
    return rest or name


def listed(text: str, heading: str) -> list:
    """The folder names listed under `## <heading>` (`- j01_x` or `1. t01_x · title`), in their order."""
    m = re.search(rf"(?ms)^## {heading}\s*$(.*?)(?=^## |\Z)", text)
    return re.findall(r"(?m)^\s*(?:-|\d+\.)\s+([jt]\d+_[A-Za-z0-9_]+)", m.group(1)) if m else []


def ordered(parent: Path, prefix: str, heading: str) -> list:
    """A Block's Jobs by its face's ## Jobs, a Job's Tasks by its ## Tasks; else folder order (haipipe-job)."""
    folders = sorted(p for p in parent.glob(f"{prefix}[0-9]*_*") if p.is_dir())
    named = [parent / n for n in listed(face(parent), heading) if (parent / n).is_dir()]
    return named + [p for p in folders if p not in named]


STATE_KINDS = (                                                  # focus_page.STATE_KINDS, first match wins
    ("🙋 waiting on you", r"waiting|your call|needs? (a )?(sign-in|decision)"),
    ("⏳ running", r"\brunning\b|in progress"),
    ("partly done", r"\bpartial|partly|carried|\bbuilt\b|drawn|redrawn|results in|unread"),
    ("✅ done", r"\bcomplete|\bclosed\b|\bdone\b|\bran\b|generated|finished"),
    ("⬜ not run yet", r"planned|not run|\bwaits?\b|design build|queued|draft"),
    ("⬜ open", r"\bopen\b"),
)


def state_kind(label: str) -> str:
    text = (label or "").lower()
    head = re.split(r";|:| - | \u2014 |\(", text, maxsplit=1)[0]          # \u2014 is the long dash, as focus_page splits
    for part in (head, text):
        for kind, pattern in STATE_KINDS:
            if re.search(pattern, part):
                return kind
    return "no state" if not text.strip() else "other"


def card(run: Path) -> dict:
    try:
        return yaml.safe_load(read(run / "run.yaml")) or {}
    except yaml.YAMLError:
        return {}


def day(path: Path) -> str:
    return date.fromtimestamp(path.stat().st_mtime).isoformat() if path.exists() else ""


TOPICS = sorted((t for pat in ("s[0-9][0-9]-*", "j*/s[0-9][0-9]-*", "j*/t*/s[0-9][0-9]-*") for t in BLOCK.glob(pat)
                 if t.is_dir() and (t / f"{t.name}.md").is_file()), key=lambda t: int(t.name[1:3]))   # sNN order


def topic_of(about: str):
    m = re.search(r"-(s\d+)\b", about or "")
    return next((t for t in TOPICS if m and t.name.startswith(m.group(1) + "-")), None)


def runs_under(page: Path) -> list:
    """Every Run in one page's runs/: its card, and for a form its title, topic, questions and drawn state."""
    out = []
    for run in sorted(p for p in (page / "runs").glob("*") if p.is_dir() and (p / "run.yaml").is_file()):
        c = card(run)
        r = {"run": run.name, "page": page, "path": run, "kind": c.get("kind") or "", "type": c.get("type") or "",
             "status": str(c.get("status") or ""), "form": "_collect_" in run.name}
        if r["form"]:
            text = read(run / "question_collection.md")
            r["title"] = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), run.name)
            r["topic"] = topic_of(field(text, "for"))
            r["asks"] = re.findall(r"(?ms)^##\s+(Q\d+)\s*·\s*(.+?)\s*$.*?^\*\*(.+?)\*\*\s*$", text)
            answered = (run / "result" / "answer_collection.md").is_file()
            state = "answered" if answered else {"waiting": "waiting"}.get(r["status"], "planned")
            if state == "planned" and (page.name, run.name) in EXPECTED:
                state = "waiting"                                  # built by its agent today (see the docstring)
            r["state"] = state
            form = run / f"{run.name}.html"
            r["date"] = day(run / "result" / "answer_collection.md") if answered else day(form) or day(run / "question_collection.md")
        out.append(r)
    return out


JOBS = ordered(BLOCK, "j", "Jobs")
TASKS = {j: ordered(j, "t", "Tasks") for j in JOBS}
BLOCK_RUNS = runs_under(BLOCK)
RUNS = {t: runs_under(t) for j in JOBS for t in TASKS[j]}
FORMS_BELOW = [r for r in BLOCK_RUNS if r["form"]] + [r for j in JOBS for t in TASKS[j] for r in RUNS[t] if r["form"]]
WAITING = [r for r in FORMS_BELOW if r["state"] == "waiting"]
ORDER = {"waiting": 0, "planned": 1, "answered": 2}


def label(topic: Path) -> str:
    """frame.topic_label: b17-s01:theme_work @ work_ladder; b17.j03.t01-s52:theme_work.work_workbench_pages.block_page @ …"""
    rungs, here = [], topic.parent
    while here != BLOCK.parent:
        rungs.insert(0, here)
        here = here.parent
    address = ".".join(p.name.split("_")[0] for p in rungs) + "-" + topic.name.split("-")[0]
    return f"{address}:" + ".".join(short(p.name) for p in rungs) + " @ " + short(topic.name, 0)


def makes(job: Path) -> list:
    """The Block's sNN whose delivery/render.yaml names a Run under this Job (`by:`), the reverse of work_root."""
    out = []
    for t in TOPICS:
        if t.parent != BLOCK:
            continue
        named = re.findall(r"(?m)^\s*by:\s*['\"]?(j\d+_[^/\s'\"]+)", read(t / "delivery" / "render.yaml"))
        if job.name in named:
            made = [p for p in (t / "delivery").iterdir() if p.name not in ("deck", "render.yaml", ".gitkeep")] \
                if (t / "delivery").is_dir() else []
            out.append((t, "planned" if not made else "made"))
    return out


def newest_result(job: Path):
    files = [f for t in TASKS[job] for f in t.glob("runs/*/result/*") if f.is_file()]
    if not files:
        return None
    f = max(files, key=lambda p: p.stat().st_mtime)
    return f.parents[1].name, f.name, day(f)


def open_points(topic: Path) -> list:
    """The face's Open list: its numbered lines, else its first sentence (an sNN's red questions)."""
    m = re.search(r"(?ms)^Open\n-+\n(.*?)(?=^\(write here|^\S[^\n]*\n-{3,}\n|\Z)", read(topic / f"{topic.name}.md"))
    body = m.group(1).strip().replace("`", "") if m else ""         # Markdown code marks read as plain words here
    numbered = re.findall(r"(?m)^\d+\.\s+(.+)$", body)
    if numbered:
        return [n.strip() for n in numbered]
    first = re.split(r"(?<=[.?!])\s", " ".join(body.split()), maxsplit=1)[0] if body else ""
    return [first] if first and not first.startswith("(") else []


# ── drawing ────────────────────────────────────────────────────────────────────────────────────────────────────────
PREVIEW_CSS = """
/* preview only: the page without its fixed rails; the right rail is drawn as one line under the path */
.focus-page.pv{max-width:980px;padding:14px 22px 30px}.pv h1{margin:6px 0 8px}
.rail-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0 0;font-size:12.5px}
.rail-line .rl-word{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.rail-line span.rl{padding:1px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted)}
.rail-line span.rl.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .section-views{flex-wrap:wrap;gap:6px}
.pv .section-views span{font-size:13px;border:1px solid var(--line);border-radius:6px;padding:3px 11px;color:var(--muted)}
.pv .section-views span.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .view-caption{margin:6px 0 10px}
.cols,.screens{display:grid;grid-template-columns:1fr;gap:14px;align-items:start;margin-top:8px}
.col-word{font-size:10.5px;color:var(--muted);letter-spacing:.05em;text-transform:uppercase;margin:0 0 5px}
.screen{border:1px solid var(--line);border-radius:10px;padding:9px 11px;background:var(--paper);min-width:0}
.screen-title{font-size:14px;font-weight:700;margin:0 0 6px}
.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:12.5px}
.screen .section-views{gap:5px;margin:0 0 5px}.screen .section-views span{font-size:11px;padding:1px 7px}
.screen .view-caption{font-size:11px;margin:0 0 7px}
/* a section of the view, folding by its heading (b16's fd-sec look) */
.wk-sec{margin:0 0 9px}
.wk-h{font-size:13px;font-weight:600;margin:0 0 3px;display:flex;align-items:center;gap:7px;border:1px solid var(--line);
 border-radius:8px;background:var(--paper);padding:4px 10px;overflow-wrap:anywhere}
.wk-h .fold{color:var(--muted);font-size:10px;width:9px;flex:none}.wk-h .btn{margin-left:auto}
.ix-sec>.wk-h{border-left:3px solid #b35c00}
.btn{font-size:10.5px;border:1px solid var(--line);border-radius:5px;padding:0 7px;background:var(--paper);color:var(--ink);
 white-space:nowrap;font-weight:400}
.btn.you{border-color:#ffa94d;color:#b35c00}
.wk-goal{font-size:11px;margin:3px 2px 1px}
.wk-makes,.wk-newest,.wk-more{font-size:11px;margin:2px 2px 3px;color:var(--muted)}
.wk-makes b,.wk-newest b{font-weight:500;color:var(--accent)}
.word{font-size:10px;border:1px dashed var(--muted);border-radius:9px;padding:0 6px;color:var(--muted);margin-left:3px}
.wk-wait{font-size:11px;margin:2px 2px 3px;color:#b45309;font-weight:500}
.wk-task{display:flex;align-items:center;gap:7px;padding:3px 2px;border-bottom:1px solid var(--line);font-size:11px}
.wk-task .w{min-width:88px;white-space:nowrap;color:var(--muted)}.wk-task .w.you{color:#b35c00;font-weight:600}
.wk-task .n{min-width:140px;font-weight:500;overflow-wrap:anywhere}.wk-task .d{flex:1;color:var(--muted);min-width:0}
/* an interaction, folded (b16's focus_draft.ix_item) */
details.ix-fold{border-bottom:1px solid var(--line)}
details.ix-fold>summary{display:flex;align-items:center;gap:7px;padding:3px 2px;list-style:none;font-size:11px}
details.ix-fold>summary::-webkit-details-marker{display:none}
details.ix-fold>summary::before{content:"▸";color:var(--muted);font-size:9px;width:9px}
details.ix-fold>summary b{flex:1;font-weight:600}
.ix-state{font-size:10.5px;color:var(--muted);white-space:nowrap}.ix-state.wait{color:#b35c00;font-weight:600}
.ask{display:flex;gap:8px;padding:3px 8px;border:1px solid var(--line);border-left:3px solid #b35c00;border-radius:6px;
 margin:3px 0;font-size:10.5px}.ask b{font-weight:600;white-space:nowrap}
/* today's rows (focus_page.status_html), drawn small */
.pv .status-row{padding:6px 10px;margin:0 0 6px}.pv .status-row .row-name{font-size:13px}
.pv .focus-content .row-line,.pv .row-line{font-size:11px;margin:2px 0}
.pv .row-meta{font-size:11px;color:var(--muted);margin:2px 0}.pv .row-verb{font-size:10.5px;padding:0 7px;margin-left:8px}
.rl-link{font-size:11px;color:var(--accent);margin:4px 2px}
"""


def diff(on: bool) -> str:
    return " diff" if on else ""


def rail(mark: tuple = ()) -> str:
    names = ["Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Files"]
    return ('<div class="rail-line"><span class="rl-word">Right rail</span>' + "".join(
        f'<span class="rl{" on" if n == "Work" else ""}{diff(n in mark)}">{esc(n)}</span>' for n in names) + "</div>")


def views(names: list, on: str, mark: bool = False) -> str:
    buttons = "".join(f'<span class="{"on" if n == on else ""}">{esc(n)}</span>' for n in names)
    return f'<nav class="section-views{diff(mark)}" aria-label="Views">{buttons}</nav>'


def page(title: str, body: str, *, bar: str = "", heading: bool = True, rail_mark: tuple = ()) -> str:
    top = (f'<h1>b17_theme_work<span class="h1-section">Work</span></h1>{bar}'
           f'<p class="view-caption">{esc(CAPTION)}</p>') if heading else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            f"<body><main class=\"focus-page pv\"><div class=\"focus-crumb\">{esc(CRUMB)}</div>"
            f"{rail(rail_mark)}{top}{body}</main></body></html>")


def screen(view: str, inner: str, *, bar: str = "", caption: str = "", mark: bool = False) -> str:
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">b17_theme_work<span>Work › {esc(view)}</span>'
            f'</div>{bar}{cap}{inner}</section>')


def cols(left: str, right: str, words: tuple = ("the top", "further down")) -> str:
    return (f'<div class="cols"><div><p class="col-word">{esc(words[0])}</p>{left}</div>'
            f'<div><p class="col-word">{esc(words[1])}</p>{right}</div></div>')


UNDER = ("under Interactions", "further down")                   # Q3, Q4: Interactions left out, no option changes it


def sec(title: str, body: str, *, extra: str = "", mark: bool = False, cls: str = "") -> str:
    return (f'<section class="wk-sec{(" " + cls) if cls else ""}{diff(mark)}"><h3 class="wk-h"><span class="fold">▾</span>'
            f'{esc(title)}{extra}</h3>{body}</section>')


def button(rows: list) -> str:
    """The one Interaction button: 🙋 and an orange edge while one of its items waits (b16 r04 Q3, r07)."""
    if not rows:
        return ""
    waits = any(r["state"] == "waiting" for r in rows)
    return f'<span class="btn{" you" if waits else ""}">{"🙋 " if waits else ""}Interaction</span>'


def ix_line(r: dict, mark: bool = False) -> str:
    """One interaction folded, as b16's ix_item: its title, its state and date, its one button."""
    word = {"waiting": "waiting for you", "answered": "answered", "planned": "not sent yet"}[r["state"]]
    act = {"waiting": "Answer", "answered": "See answers"}.get(r["state"], "")
    where = (f'asked by {esc(r["page"].name)}' + (f' · about {esc(r["topic"].name)}' if r["topic"] else "")
             + f' · <code>{esc(r["run"])}</code>')
    asks = "".join(f"<li><b>{esc(q)}</b> {esc(ask)}</li>" for q, _, ask in r["asks"])
    return (f'<details class="ix-fold{diff(mark)}"><summary><b>{esc(r["title"])}</b><span class="ix-state'
            f'{" wait" if r["state"] == "waiting" else ""}">{esc(word)}{(" · " + esc(r["date"])) if r["date"] else ""}'
            f'</span>{f"<span class=btn>{act}</span>" if act else ""}</summary><div class="ix-body"><p class="mut">{where}'
            f'</p><ol>{asks}</ol></div></details>')


def interactions(items: list, *, mark: bool = False, lead: str = "", tail: str = "") -> str:
    extra = '<span class="btn">Answer all</span>' if len(items) > 1 else ""
    return sec("Interactions", lead + "".join(ix_line(r) for r in sorted(items, key=lambda r: ORDER[r["state"]])) + tail,
               extra=extra, mark=mark, cls="ix-sec")


def task_state(task: Path) -> tuple:
    forms = [r for r in RUNS[task] if r["form"]]
    if any(r["state"] == "waiting" for r in forms):
        return "🙋 waits on you", True
    if any(r["status"] == "running" for r in RUNS[task]):
        return "⏳ running", False
    return state_kind(field(face(task), "state")), False


def task_line(task: Path, mark: bool = False) -> str:
    word, you = task_state(task)
    title = title_of(face(task)) or field(face(task), "goal")
    return (f'<div class="wk-task{diff(mark)}"><span class="w{" you" if you else ""}">{esc(word)}</span>'
            f'<span class="n">{esc(task.name)}</span><span class="d">{esc(title)}</span>'
            f'{button([r for r in RUNS[task] if r["form"]])}</div>')


def job_sec(job: Path, *, tasks: str = "all", head: str = "makes", open_flag: bool = False, mark_tasks: bool = False,
            mark_head: bool = False, mark_flag: bool = False, folded: bool = False) -> str:
    """One Job's section: its heading, its goal, the sNN it makes, then its Tasks (all, the next one, or none)."""
    if folded:
        return (f'<section class="wk-sec"><h3 class="wk-h"><span class="fold">▸</span>{esc(job.name)}</h3></section>')
    goal = field(face(job), "goal")
    made = "".join(f'<p class="wk-makes{diff(mark_head and head != "goal")}">makes <b>{esc(label(t))}</b>'
                   f'<span class="word">{esc(w)}</span></p>' for t, w in makes(job)) if head != "goal" else ""
    newest = ""
    if head == "newest":
        got = newest_result(job)
        newest = (f'<p class="wk-newest diff">newest result: <b>{esc(got[0])}</b> · result/{esc(got[1])} · {esc(got[2])}</p>'
                  if got else '<p class="wk-newest diff">newest result: none yet</p>')
    below = [r for t in TASKS[job] for r in RUNS[t] if r["form"]]
    flag = f'<p class="wk-wait{diff(mark_flag)}">🙋 open points wait on you</p>' if open_flag else ""
    lines = TASKS[job]
    if tasks == "all":
        body = "".join(task_line(t) for t in lines) or '<p class="wk-more">No Tasks yet.</p>'
        body = f'<div class="{diff(mark_tasks).strip()}">{body}</div>' if mark_tasks else body
        extra = ""
    elif tasks == "next":
        nxt = next((t for t in lines if task_state(t)[1]), None) or next(
            (t for t in lines if task_state(t)[0] not in ("✅ done",)), None)
        body = (f'<div class="diff">{task_line(nxt) if nxt else ""}'
                f'<p class="wk-more">its other Tasks: on its page ↗</p></div>')
        extra = ""
    else:                                    # today's words: the Task faces' states only (focus_page.task_tally)
        kinds = " · ".join(k for k, _ in Counter(state_kind(field(face(t), "state")) for t in lines).most_common())
        body = f'<p class="wk-more diff">{esc(kinds or "no Tasks yet")}</p>'
        extra = button(below)
    goal_html = f'<p class="wk-goal{diff(mark_head and head == "goal")}">{esc(goal)}</p>'
    return sec(job.name, goal_html + made + newest + flag + body, extra=extra)


def own_runs(rows: list, mark: bool = False) -> str:
    word = lambda r: ({"planned": "not sent yet", "answered": "answered"}.get(r.get("state"), "")
                      if r["form"] else state_kind(r["status"]))
    lines = "".join(f'<div class="wk-task"><span class="w">{esc(word(r))}</span><span class="n">{esc(r["run"])}</span>'
                    f'<span class="d">{esc(r["type"])}{(" · " + esc(r["title"])) if r["form"] else ""}</span>'
                    f'{button([r]) if r["form"] else ""}</div>' for r in rows)
    return sec("Its own Runs", lines, mark=mark)


def today_rows(rows: list, mark: bool = False) -> str:
    """The Block's own forms as focus_page.status_html draws them today: a row each, any state, before the Jobs."""
    out = "".join(f'<article class="status-row ix-row"><span class="row-name">{esc(r["title"])}</span>'
                  + (f'<p class="row-line">about <a>{esc(r["topic"].name)}</a></p>' if r["topic"] else "")
                  + f'<p class="row-meta">{esc(r["run"])}{button([r])}</p></article>'
                  for r in sorted(rows, key=lambda r: ORDER[r["state"]]))       # waiting first, as interactions()
    return f'<div class="{diff(mark).strip()}">{out}</div>'


def runs_view(mark: bool = False) -> str:
    """Q1 C's second view: every Run below the Block, one line each, a waiting or running one first."""
    rows = [(r, "b17_theme_work") for r in BLOCK_RUNS] + [(r, t.name) for j in JOBS for t in TASKS[j] for r in RUNS[t]]

    def word(r):
        if r["form"]:
            return {"waiting": "🙋 waiting for you", "answered": "✅ answered", "planned": "⬜ not sent yet"}[r["state"]]
        return {"running": "⏳ running", "queued": "⬜ queued", "done": "✅ done"}.get(r["status"], r["status"] or "⬜ planned")
    rank = lambda r: 0 if word(r).startswith("🙋") else 1 if word(r).startswith("⏳") else 2 if "queued" in word(r) else 3
    lines = "".join(f'<div class="wk-task"><span class="w{" you" if word(r).startswith("🙋") else ""}">{esc(word(r))}'
                    f'</span><span class="n">{esc(r["run"])}</span><span class="d">{esc(where)}</span></div>'
                    for r, where in sorted(rows, key=lambda x: rank(x[0])))
    return f'<div class="{diff(mark).strip()}">{lines}</div>'


def by_type(kind: str) -> tuple:
    """Q1 B: the Block's sNN of one delivery type, the Jobs that make them, and the forms about them."""
    typed = [t for t in TOPICS if re.search(rf"(?m)^\*\*Delivery type:\*\*\s*{kind}\b", read(t / f"{t.name}.md"))]
    jobs = [j for j in JOBS if any(t in typed for t, _ in makes(j))]
    return typed, jobs, [r for r in WAITING if r["topic"] in typed]


def type_view(kind: str, name: str) -> str:
    typed, jobs, waits = by_type(kind)
    asks = "".join(f'<div class="ask"><b>{esc(t.name.split("-")[0])}</b><span>{esc(p)}</span></div>'
                   for t in typed for p in open_points(t))
    body = (interactions(waits) if waits else "") + (sec("Open", asks) if asks else "")
    body += "".join(job_sec(j) for j in jobs)
    return body + f'<p class="rl-link">Its result: Report › {esc(name)} ↗</p>'


def previews() -> dict:
    out = {}
    progress = dict(bar=views(["Progress"], "Progress"))
    top = interactions(WAITING)
    ends = own_runs([r for r in BLOCK_RUNS if not (r["form"] and r["state"] == "waiting")])

    # Q1 · the view list: the whole Progress in two columns, Report's type list, or Progress then Runs
    out["q1-a"] = page("Q1 A", heading=False, body='<div class="screens">'
                       + screen("Progress", top + job_sec(JOBS[0]), bar=views(["Progress"], "Progress", mark=True),
                                caption=CAPTION)
                       + screen("Progress, further down", "".join(job_sec(j) for j in JOBS[1:]) + ends,
                                bar=views(["Progress"], "Progress", mark=True)) + "</div>")
    out["q1-b"] = page("Q1 B", heading=False, body='<div class="screens">'
                       + screen("Skill", type_view("skill", "Skill"), bar=views(["Skill", "UI"], "Skill", mark=True),
                                caption="What waits, what is open, and the Jobs that make the Skill deliveries.")
                       + screen("UI", type_view("ui", "UI"), bar=views(["Skill", "UI"], "UI", mark=True),
                                caption="What waits, what is open, and the Jobs that make the UI deliveries.") + "</div>")
    out["q1-c"] = page("Q1 C", heading=False, body='<div class="screens">'
                       + screen("Progress", top + job_sec(JOBS[0]), bar=views(["Progress", "Runs"], "Progress", mark=True),
                                caption=CAPTION)
                       + screen("Runs", runs_view(), bar=views(["Progress", "Runs"], "Runs", mark=True),
                                caption="Every Run below the Block, a waiting or running one first.", mark=True)
                       + "</div>")

    # Q2 · what shows first: Interactions, today's own-form rows and open-points line, or Interactions plus open points
    j03 = JOBS[-1]
    others = [j for j in JOBS if j != j03]
    points = "".join(f'<div class="ask"><b>{esc(t.name.split("-")[0])}</b><span>{esc(p)}</span></div>'
                     for t in TOPICS for p in open_points(t))
    out["q2-a"] = page("Q2 A", cols(interactions(WAITING, mark=True) + job_sec(others[0]), job_sec(j03)), **progress)
    out["q2-b"] = page("Q2 B", cols(today_rows([r for r in BLOCK_RUNS if r["form"]], mark=True) + job_sec(others[0]),
                                    job_sec(j03, open_flag=True, mark_flag=True)), **progress)
    out["q2-c"] = page("Q2 C", cols(interactions(WAITING, tail=f'<div class="diff">{points}</div>'), job_sec(j03)),
                       **progress)

    # Q3 · a Job's Tasks: every one, only the next, or none (the Job's state words); Interactions above, unchanged
    for key, mode in (("a", "all"), ("b", "next"), ("c", "none")):
        sections = [job_sec(j, tasks=mode, mark_tasks=mode == "all") for j in JOBS]
        out[f"q3-{key}"] = page(f"Q3 {key.upper()}", cols("".join(sections[:-1]), sections[-1], UNDER), **progress)

    # Q4 · a Job's head: its goal and the sNN it makes; plus its newest result; or its goal only
    for key, mode in (("a", "makes"), ("b", "newest"), ("c", "goal")):
        sections = [job_sec(j, head=mode, mark_head=mode != "newest") for j in JOBS]
        out[f"q4-{key}"] = page(f"Q4 {key.upper()}", cols("".join(sections[:-1]), sections[-1], UNDER), **progress)

    # Q5 · the Block's own Runs: a last section, its forms first whatever their state, or nowhere in Work
    planned = [r for r in BLOCK_RUNS if r["form"] and r["state"] != "waiting"]
    out["q5-a"] = page("Q5 A", cols(top, job_sec(j03) + own_runs(planned + [r for r in BLOCK_RUNS if not r["form"]],
                                                                     mark=True)), **progress)
    out["q5-b"] = page("Q5 B", cols(interactions(WAITING, lead="".join(ix_line(r, mark=True) for r in planned)),
                                    job_sec(j03)), **progress)
    out["q5-c"] = page("Q5 C", cols(top, job_sec(j03)), rail_mark=("Interactions", "Timeline"), **progress)
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/ · {len(WAITING)} forms drawn waiting · Jobs: "
          + ", ".join(j.name for j in JOBS))


if __name__ == "__main__":
    main()
