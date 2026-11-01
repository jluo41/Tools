"""r03's option previews (s56 · Job UI: Studio): one small page per option, drawn in the workbench's own look (its
focus.css) with real names read from disk: b17's Jobs, the topics each one makes or holds, their faces, pictures and
forms. The part an option changes carries class="diff", which the form boxes in orange.

The form shows a preview at half size in a frame 600 pixels tall, so what differs sits in that height: no goal line (no
option changes it), compact cards, and two views side by side when an option moves topics between views.

What it reads (the same rules the proposal names, result/views-proposal.md in s56):
  the topic a Job makes   a Block sNN whose delivery/render.yaml has a `by:` line starting with the Job's folder name
  a Job's own topics      its sNN-* folders;  a Task's: the sNN-* folders in each Task, in the Job face's ## Tasks order
  groups                  each topic face's **Tags:** line, in the Block's _studio_groups.txt order
  forms                   every runs/r*_collect_*/ under the Block: its for: line names the sNN, run.yaml its state

Writes runs/r03_collect_job_studio_views/option-q<N>-<k>.html; question_collection.md links each one under its option.
Rerun after changing anything here, or after a form's state changes; never edit the pages:

    python build_r03_previews.py
"""
from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]                       # t02_job_page
RUN = TASK / "runs" / "r03_collect_job_studio_views"
J03 = TASK.parent                                                # j03_work_workbench_pages
BLOCK = J03.parent                                               # b17_theme_work
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
J01 = BLOCK / "j01_work_ladder_contract"
EMPTY_JOB = TOOLS / "blueprints/Project-Packages/work/b02_haipipe-utils/j02_food"   # a Job with no topic at all
SNN = re.compile(r"^s\d+-")
STAGES = ("explore", "shaping", "agreed", "closed")


# ── what the page reads, as frame.py and focus_page.py read it (re-written here: frame.py needs the server's path) ──
def esc(text) -> str:
    return html.escape(str(text), quote=True)


def rel(path: Path) -> str:
    """A file's path from the Run folder, so the previews work on the host and opened as files."""
    return os.path.relpath(path, RUN)


def short(name: str, words: int = 3) -> str:                    # frame._short
    rest = re.sub(r"^[bjtsr]\d+[_-]?", "", name)
    rest = "_".join(re.split(r"[_.-]+", rest)[:words]) if words else re.sub(r"[.-]+", "_", rest)
    return rest or name


def rungs(folder: Path) -> list:                                 # frame._rungs
    out = []
    while re.fullmatch(r"[bjt]\d+", folder.name.split("_")[0]):
        out.insert(0, folder.name.split("_")[0])
        if out[0].startswith("b"):
            return out
        folder = folder.parent
    return []


def label(topic: Path) -> tuple:
    """frame.topic_label: ('b17.j03.t01-s51:theme_work.work_workbench_pages.block_page @ ', 'block_ui_report')."""
    ladder = rungs(topic.parent)
    address = ".".join(ladder) + "-" + re.match(r"s\d+", topic.name).group(0)
    here = topic.parent
    for _ in ladder[1:]:
        here = here.parent
    names = [short(here.name)]
    for rung in ladder[1:]:
        here = sorted(p for p in here.glob(f"{rung}[_-]*") if p.is_dir())[0]
        names.append(short(here.name))
    return f"{address}:" + ".".join(names) + " @ ", short(topic.name, 0)


def face(topic: Path) -> str:
    md = topic / f"{topic.name}.md"
    return md.read_text(encoding="utf-8", errors="ignore") if md.is_file() else ""


def facts(topic: Path) -> dict:
    """frame._note_facts, the parts a card shows: its one line, groups, stage and delivery type."""
    text = face(topic)
    m = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    line = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    first = re.match(r"(.+?[.;])(?:\s|$)", line)                 # focus_page.studio_html: its first sentence
    tags = [t.strip().strip("`").strip() for line_ in re.findall(r"(?mi)^\*\*(?:Tags|Type):\*\*[^\S\n]*([^\n]*)", text)
            for t in re.split(r"[,·|]", line_) if t.strip().strip("`").strip()]
    stage = re.search(r"(?mi)^\*\*Stage:\*\*[^\S\n]*`?([A-Za-z]+)", text)
    dtype = re.search(r"(?mi)^\*\*Delivery type:\*\*[^\S\n]*`?([A-Za-z]+)", text)
    return {"line": first.group(1) if first else line[:200], "tags": list(dict.fromkeys(tags)),
            "stage": stage.group(1).lower() if stage and stage.group(1).lower() in STAGES else "",
            "dtype": dtype.group(1).lower() if dtype else ""}


def picture(topic: Path) -> Path | None:
    """The lead slide (slides.json's first), else the drawing's preview."""
    record = topic / f"{topic.name}.slides.json"
    if record.is_file():
        try:
            first = topic / json.loads(record.read_text(encoding="utf-8"))["slides"][0]["image"]
            if first.is_file():
                return first
        except (ValueError, KeyError, IndexError, TypeError):
            pass
    png = topic / f"{topic.name}.png"
    return png if png.is_file() else None


def builders(topic: Path) -> list:
    """The Jobs a Block sNN's delivery/render.yaml names in its `by:` lines (focus_page.work_root, read the other way)."""
    card = topic / "delivery" / "render.yaml"
    return re.findall(r"(?m)^\s*by:\s*['\"]?(j\d+_[^/\s'\"]+)", card.read_text(encoding="utf-8", errors="ignore")) \
        if card.is_file() else []


def topics_at(folder: Path) -> list:
    return sorted(p for p in folder.iterdir() if p.is_dir() and SNN.match(p.name)) if folder.is_dir() else []


def made_by(job: Path) -> list:
    """The Block's sNN this Job makes."""
    return [t for t in topics_at(job.parent) if job.name in builders(t)]


def tasks(job: Path) -> list:
    """(folder, title) in the Job face's ## Tasks order; the title from each Task face's # line."""
    text = (job / f"{job.name}.md").read_text(encoding="utf-8", errors="ignore")
    names = re.findall(r"(?m)^\d+\.\s+(t\d+_[A-Za-z0-9_]+)", text.split("## Tasks", 1)[-1]) if "## Tasks" in text else []
    folders = [job / n for n in names if (job / n).is_dir()] or sorted(p for p in job.iterdir() if p.is_dir()
                                                                       and re.match(r"t\d+_", p.name))
    out = []
    for t in folders:
        tf = t / f"{t.name}.md"
        head = re.search(r"(?m)^#\s+t\d+\s*·\s*(.+?)\s*$", tf.read_text(encoding="utf-8", errors="ignore")) if tf.is_file() else None
        out.append((t, head.group(1) if head else ""))
    return out


def task_rows(job: Path) -> list:
    """A Job's Work › Progress rows today: each Task's name, its goal line, its state."""
    out = []
    for t, _ in tasks(job):
        text = (t / f"{t.name}.md").read_text(encoding="utf-8", errors="ignore")
        goal = re.search(r"(?m)^goal:\s*(.+)$", text)
        state = re.search(r"(?m)^state:\s*(.+)$", text)
        out.append((t.name, goal.group(1).strip() if goal else "", state.group(1).strip() if state else ""))
    return out


def group_order() -> list:
    f = BLOCK / "_studio_groups.txt"
    return [ln.strip() for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]


def forms() -> list:
    """Every collection Run under the Block: (run folder, title, the sNN folder its for: names, state)."""
    out = []
    for run in sorted(BLOCK.glob("**/runs/r*_collect_*")):
        source = run / "question_collection.md"
        if not run.is_dir() or not source.is_file() or "_old" in run.parts:
            continue
        text = source.read_text(encoding="utf-8", errors="ignore")
        about = re.search(r"(?m)^for:\s*(b\d+(?:\.[jt]\d+)*)-(s\d+)", text)
        title = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), run.name)
        card = (run / "run.yaml").read_text(encoding="utf-8", errors="ignore") if (run / "run.yaml").is_file() else ""
        status = (re.search(r"(?m)^status:\s*(\S+)", card) or [None, "planned"])[1]
        state = "answered" if (run / "result" / "answer_collection.md").is_file() else \
            "waiting" if status == "waiting" or run == RUN else "planned"    # this form waits while it is read
        topic = None
        if about:
            here = BLOCK
            for rung in about.group(1).split(".")[1:]:
                found = sorted(p for p in here.glob(f"{rung}_*") if p.is_dir())
                here = found[0] if found else here
            topic = next((p for p in topics_at(here) if p.name.split("-")[0] == about.group(2)), None)
        out.append({"run": run, "title": title, "topic": topic, "state": state})
    return out


FORMS = forms()


def topic(path: Path) -> dict:
    lead, name = label(path)
    asks = [f for f in FORMS if f["topic"] == path]
    verbs = []
    if (path / f"{path.name}.slides.html").is_file():
        verbs.append(("Slide", "main"))
    if (path / f"{path.name}.excalidraw").is_file():
        verbs.append(("Draw", ""))
    if (path / f"{path.name}.mindmap.md").is_file():
        verbs.append(("Mind map", ""))
    if builders(path) or re.match(r"[jt]\d+_", path.parent.name):
        verbs.append(("Work", ""))
    if (path / "delivery").is_dir():
        verbs.append(("Delivery", ""))
    waits = [f for f in asks if f["state"] == "waiting"]
    if asks:
        verbs.append(("🙋 Interaction" if waits else "Interaction", "flag" if waits else ""))
    return {"path": path, "lead": lead, "name": name, **facts(path), "pic": picture(path), "verbs": verbs,
            "waits": waits}


# ── the screen's parts ──────────────────────────────────────────────────────────────────────────────────────
PREVIEW_CSS = """
/* preview only: the page without its fixed rails; the right rail is drawn as one line under the path */
.focus-page.pv{max-width:1040px;padding:14px 22px 30px}.pv h1{margin:6px 0 8px;font-size:23px}.pv .h1-section{font-size:19px}
.rail-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0 0;font-size:12.5px}
.rail-line .rl-word{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.rail-line span.rl{padding:1px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted)}
.rail-line span.rl.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.rail-line span.rl.gone{text-decoration:line-through;border-style:dashed;opacity:.65}
.pv .section-views{flex-wrap:wrap;gap:6px;margin:0 0 10px}.pv .section-views a{font-size:13px;padding:3px 11px}
.pv .focus-card .focus-content{padding:10px 0 0}
.pv .focus-content>.view-caption{margin:0 0 10px;font-size:13px}
.pv .focus-content .focus-sub{margin:16px 0 6px;font-size:12px}.pv .focus-content .focus-sub:first-child{margin-top:0}
.pv .focus-content .focus-sub.wait{color:light-dark(#b35c00,#ffc078)}
.pv .studio-row{grid-template-columns:minmax(0,1fr) 150px;gap:12px;padding:9px 12px;margin:0 0 8px}
.pv .row-thumb img,.pv .row-thumb.none{width:150px;height:84px}
.pv .row-title{font-size:12.5px;line-height:1.4}.pv .row-name{font-size:14.5px}.pv .row-address{overflow-wrap:anywhere}
.pv .row-stage,.pv .row-type{font-size:11px;padding:0 7px}
.pv .focus-content .row-line{font-size:12.5px;margin:3px 0}
.pv .row-verbs{gap:5px;margin:5px 0 0;flex-wrap:wrap}.pv .row-verb{font-size:11.5px;padding:1px 8px}
.pv .row-verb.flag{border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)}
.wait-row{display:flex;align-items:center;gap:12px;border:1px solid light-dark(#ffa94d,#b35c00);border-left-width:5px;
  border-radius:10px;padding:8px 12px;margin:0 0 8px;background:light-dark(#fff4e6,#2b1d0e)}
.wait-row b{font-size:14px}.wait-row p{margin:1px 0 0;font-size:12px;color:var(--muted)}
.wait-row .row-verb{margin-left:auto;border-color:light-dark(#e8590c,#ffa94d);color:light-dark(#b35c00,#ffc078)}
.made-line{border:1px solid var(--line);border-radius:10px;padding:10px 14px;font-size:13.5px}
.made-line a{color:var(--accent)}.made-line .mut{display:block;margin-top:2px}
.note{margin:8px 0 0;padding:8px 12px;border:1px dashed var(--muted);border-radius:8px;font-size:12.5px;color:var(--muted)}
.empty{padding:22px 16px;text-align:center;color:var(--muted);border:1px dashed var(--line);border-radius:10px;font-size:13.5px}
.screens{display:grid;grid-template-columns:1fr;gap:14px;align-items:start;margin-top:12px}
.screen{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--paper);min-width:0}
.screen-title{font-size:15px;font-weight:700;margin:0 0 6px;overflow-wrap:anywhere}
.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:13px}
.screen .section-views{gap:5px;margin:0 0 6px}.screen .section-views a{font-size:11.5px;padding:1px 8px}
.screen .view-caption{font-size:11.5px;margin:0 0 8px;color:var(--muted)}
.screen .studio-row{grid-template-columns:minmax(0,1fr) 92px;gap:8px;padding:7px 9px;margin:0 0 6px}
.screen .row-thumb img,.screen .row-thumb.none{width:92px;height:52px}
.screen .row-title{font-size:11px}.screen .row-name{font-size:12.5px}.screen .row-line{font-size:11px!important}
.screen .row-verb{font-size:10.5px;padding:0 6px}.screen .wait-row b{font-size:12.5px}.screen .wait-row{padding:6px 9px}
.screen .focus-sub{font-size:11px!important;margin:10px 0 5px!important}.screen .focus-sub:first-child{margin-top:0!important}
.wrow{padding:9px 12px}.wrow .row-name{font-size:15px}
"""


def diff(on: bool) -> str:
    return " diff" if on else ""


def rail(names: list, on: str, gone: str = "", mark: str = "") -> str:
    """The right rail as one line; `gone` is struck through (not on the rail), `mark` is the boxed item."""
    spans = []
    for name in names:
        cls = "rl" + (" on" if name == on else "") + (" gone" if name == gone else "") + diff(name == mark)
        spans.append(f'<span class="{cls}">{esc(name)}</span>')
    return f'<div class="rail-line"><span class="rl-word">Right rail</span>{"".join(spans)}</div>'


def bar(names: list, on: str, mark: bool = False) -> str:
    links = "".join(f'<a href="#"{" aria-current=page" if n == on else ""}>{esc(n)}</a>' for n in names)
    return f'<nav class="section-views studio-groups{diff(mark)}" aria-label="Views">{links}</nav>'


def card(t: dict, mark_addr: bool = False, mark_ask: bool = False) -> str:
    """One Studio card, as focus_page.studio_html draws it: name (address @ topic), stage, type, its one line, the tags
    that open each part, its picture."""
    verbs = "".join(f'<a class="row-verb{" " + cls if cls else ""}{diff(mark_ask and cls == "flag")}" href="#">'
                    f'{esc(v)}</a>' for v, cls in t["verbs"])
    pic = (f'<a class="row-thumb" href="#"><img src="{esc(rel(t["pic"]))}" alt="{esc(t["path"].name)}"></a>'
           if t["pic"] else '<span class="row-thumb none">no picture yet</span>')
    return (f'<article class="status-row studio-row" id="{esc(t["path"].name)}"><div><p class="row-title">'
            f'<span class="row-address{diff(mark_addr)}">{esc(t["lead"])}</span><a class="row-name" href="#">{esc(t["name"])}</a>'
            + (f'<span class="row-stage">{esc(t["stage"])}</span>' if t["stage"] else "")
            + (f'<span class="row-type">{esc(t["dtype"])}</span>' if t["dtype"] else "")
            + f'</p><p class="row-line"><a href="#">{esc(t["line"])}</a></p><p class="row-verbs">{verbs}</p></div>{pic}</article>')


def heading(words: str, mark: bool = False, wait: bool = False) -> str:
    return f'<h3 class="focus-sub{" wait" if wait else ""}{diff(mark)}">{esc(words)}</h3>'


def waiting(items: list, mark: bool = False) -> str:
    """🙋 Waiting for you: one line per form that waits on a topic in this view, orange and first; Answer opens it."""
    if not items:
        return ""
    rows = "".join(f'<article class="wait-row"><div><b>🙋 {esc(f["title"])}</b><p>about {esc(f["topic"].name)} · '
                   f'{esc(f["run"].name)}</p></div><a class="row-verb" href="#">Answer</a></article>' for f in items)
    return f'<div class="{diff(mark).strip()}">{heading("Waiting for you", wait=True)}{rows}</div>'


def sections(parts: list, *, heads: bool = True, mark_heads: bool = False, mark_addr: bool = False,
             wait: bool = False, mark_wait: bool = False, mark_ask: bool = False) -> str:
    """A view's sections in order: what waits (wait=True), then each place with its topics (parts: (heading, [topic]))."""
    shown = [(h, ts) for h, ts in parts if ts]
    waits = [f for _, ts in shown for t in ts for f in t["waits"]] if wait else []
    body = "".join((heading(h, mark_heads) if heads else "") + "".join(card(t, mark_addr, mark_ask) for t in ts)
                   for h, ts in shown)
    return waiting(waits, mark_wait) + body


def page(title: str, crumb: str, rail_html: str, body: str, *, name: str = "", section: str = "",
         bar_html: str = "", caption: str = "") -> str:
    """One preview page: the path and the right rail, then (name) the title-&-section, its view buttons and the open
    view (its caption, then its content)."""
    top = (f'<h1>{esc(name)}<span class="h1-section">{esc(section)}</span></h1>{bar_html}'
           f'<section class="focus-card"><div class="focus-content">'
           + (f'<p class="view-caption">{esc(caption)}</p>' if caption else "") + f'{body}</div></section>') if name else body
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            f"<body><main class=\"focus-page pv\"><div class=\"focus-crumb\">{esc(crumb)}</div>{rail_html}{top}"
            "</main></body></html>")


def screen(name: str, bar_html: str, body: str, caption: str = "") -> str:
    """One view of the page drawn small, so two views sit side by side."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return (f'<section class="screen"><div class="screen-title">{esc(name)}<span>Studio</span></div>{bar_html}'
            f'<div class="focus-content">{cap}{body}</div></section>')


def crumb(folder: Path) -> str:
    return " / ".join(("Tools-SPACE",) + folder.relative_to(TOOLS).parts)


# ── the options ─────────────────────────────────────────────────────────────────────────────────────────────
def previews() -> dict:
    out = {}
    groups = group_order()
    j03_made = [topic(t) for t in made_by(J03)]                                       # s04
    j03_tasks = [(f"{t.name} · {title}", [topic(s) for s in topics_at(t)]) for t, title in tasks(J03)]
    j03_own = [topic(s) for s in topics_at(J03)]                                      # none today
    j03_head = f"{J03.name} · " + re.search(r"(?m)^#\s+j\d+\s*·\s*(.+)$", (J03 / f"{J03.name}.md").read_text()).group(1)
    every = j03_made + j03_own + [t for _, ts in j03_tasks for t in ts]
    j03_groups = [g for g in groups if any(g in t["tags"] for t in every)]            # Interface … Task UI

    def in_group(g):
        """A group view's places: what this Job makes, its own, then each Task."""
        return ([("This Job makes", [t for t in j03_made if g in t["tags"]]),
                 (j03_head, [t for t in j03_own if g in t["tags"]])]
                + [(h, [t for t in ts if g in t["tags"]]) for h, ts in j03_tasks])

    cap = "The topics tagged {}."
    j03_rail = rail(["Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Files"], "Studio")
    first, second = j03_groups[0], next(g for g in j03_groups if any(g in t["tags"] for _, ts in j03_tasks for t in ts))

    # Q1 · the red question, on j01: it makes b17-s01, which sits at the Block
    s01 = [topic(t) for t in made_by(J01)]
    j01_names = ["Report", "Work", "Studio", "Interactions", "Delivery", "Files"]
    j01_groups = [g for g in groups if any(g in t["tags"] for t in s01)] or ["Topics"]
    out["q1-a"] = page("Q1 A", crumb(J01), rail(j01_names, "Studio", mark="Studio"),
                       f'<div class="diff">{sections([("This Job makes", s01)])}</div>', name=J01.name, section="Studio",
                       bar_html=bar(j01_groups, j01_groups[0]), caption=cap.format(j01_groups[0]))
    lead, name = s01[0]["lead"], s01[0]["name"]
    out["q1-b"] = page("Q1 B", crumb(J01), rail(j01_names, "Studio", mark="Studio"),
                       f'<p class="made-line diff">This Job makes <a href="#">{esc(lead)}{esc(name)}</a> ↗'
                       '<span class="mut">its card sits in b17_theme_work › Studio</span></p>', name=J01.name,
                       section="Studio", bar_html=bar(["Topics"], "Topics"), caption="The topics this Job makes or holds.")
    rows = "".join(f'<article class="status-row wrow"><a class="row-name" href="#">{esc(n)}</a><p class="row-line">{esc(g)}</p>'
                   f'<p class="row-meta">{esc(s)}</p></article>' for n, g, s in task_rows(J01))
    out["q1-c"] = page("Q1 C", crumb(J01), rail(j01_names, "Work", gone="Studio", mark="Studio")
                       + '<p class="note diff">No Studio on j01: it holds no sNN, so s01 shows only on b17_theme_work › Studio.</p>',
                       rows, name=J01.name, section="Work", bar_html=bar(["Progress"], "Progress"), caption="Its parts.")

    # Q2 · the view buttons, on j03: the view that opens, beside the next one
    a_bar = lambda on: bar(j03_groups, on, mark=True)
    out["q2-a"] = page("Q2 A", crumb(J03), j03_rail, '<div class="screens">'
                       + screen(J03.name, a_bar(first), sections(in_group(first)), cap.format(first))
                       + screen(J03.name, a_bar(second), sections(in_group(second)), cap.format(second)) + "</div>")
    b_names = ["This Job", "Block"]
    block_rest = [topic(t) for t in topics_at(BLOCK) if t not in made_by(J03)]
    this_job = [("This Job makes", j03_made), (j03_head, j03_own)] + j03_tasks
    out["q2-b"] = page("Q2 B", crumb(J03), j03_rail, '<div class="screens">'
                       + screen(J03.name, bar(b_names, "This Job", mark=True), sections(this_job),
                                "What this Job makes, its own topics, then each Task's.")
                       + screen(J03.name, bar(b_names, "Block", mark=True), sections([("", block_rest)], heads=False),
                                "The Block's other topics.") + "</div>")
    c_names = ["This Job makes"] + [t.name for t, _ in tasks(J03)]
    t01 = tasks(J03)[0][0]
    out["q2-c"] = page("Q2 C", crumb(J03), j03_rail, '<div class="screens">'
                       + screen(J03.name, bar(c_names, "This Job makes", mark=True), sections([("", j03_made)], heads=False),
                                "The topic this Job makes, from the Block.")
                       + screen(J03.name, bar(c_names, t01.name, mark=True),
                                sections([("", [topic(s) for s in topics_at(t01)])], heads=False),
                                f"The topics in {t01.name}.") + "</div>")

    # Q3 · inside one view: headings by where each topic sits, or one list
    for key, heads in (("a", True), ("b", False)):
        out[f"q3-{key}"] = page(f"Q3 {key.upper()}", crumb(J03), j03_rail, '<div class="screens">'
                                + "".join(screen(J03.name, bar(j03_groups, g),
                                                 sections(in_group(g), heads=heads, mark_heads=heads, mark_addr=not heads),
                                                 cap.format(g)) for g in (first, second)) + "</div>")

    # Q4 · a form that waits: a line on top of the view, or only the card's button; the second view is s56's own
    # group (Job UI), where this form waits while it is read
    waits_in = facts(TASK / "s56-job-ui-studio")["tags"][0]
    for key, top in (("a", True), ("b", False)):
        out[f"q4-{key}"] = page(f"Q4 {key.upper()}", crumb(J03), j03_rail, '<div class="screens">'
                                + "".join(screen(J03.name, bar(j03_groups, g),
                                                 sections(in_group(g), wait=top, mark_wait=top, mark_ask=not top),
                                                 cap.format(g)) for g in (first, waits_in)) + "</div>")

    # Q5 · a Job with no topic at all
    food_names = ["Report", "Work", "Studio", "Interactions", "Delivery", "Files"]
    out["q5-a"] = page("Q5 A", crumb(EMPTY_JOB), rail(food_names, "Studio", mark="Studio"),
                       f'<p class="empty diff">No topic yet: none is made by {esc(EMPTY_JOB.name)}, sits in it or in its '
                       'Tasks.</p>', name=EMPTY_JOB.name, section="Studio", bar_html=bar(["Topics"], "Topics"),
                       caption="The topics this Job makes or holds.")
    out["q5-b"] = page("Q5 B", crumb(EMPTY_JOB), rail(food_names, "Work", gone="Studio", mark="Studio")
                       + '<p class="note diff">No Studio on its rail: Studio shows only when it holds a topic.</p>',
                       '<p class="mut">No Tasks yet.</p>', name=EMPTY_JOB.name, section="Work",
                       bar_html=bar(["Progress"], "Progress"), caption="Its parts.")
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/")


if __name__ == "__main__":
    main()
