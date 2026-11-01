"""r02's option previews: the work Block's Report (s51-block-ui-report), one small page per option, drawn in the
workbench's own look (its focus.css) with b17's real names, read from disk on every build: each sNN face (title,
**For:**, **Topic:**, **Delivery type:**, **Tags:**), each delivery/render.yaml, the Job and Task faces, board.md's
ui-block, ui-job and ui-task lines, each topic's slides, and each collection Run's card (what waits on you). The part
an option changes carries class="diff", which the form boxes in orange.

The form shows a preview at half size in a frame 600 page pixels tall, so each page leaves out what no option
changes (the Purpose, the right rail) and keeps rows compact. Outside the question it asks, every page shows my other
picks (Q1 A, Q2 C, Q3 A, Q4 A, Q5 A, Q6 A), so a page differs from its neighbours only where its question does.

Writes runs/r02_collect_block_report_views/option-q<N>-<k>.html; question_collection.md links each one under its
option. Rerun after changing anything here, never edit the pages:

    python build_r02_previews.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]                       # t01_block_page
RUN = TASK / "runs" / "r02_collect_block_report_views"
JOB = TASK.parent                                                # j03_work_workbench_pages
BLOCK = JOB.parent                                               # b17_theme_work
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
UP = "../../../../"                                              # from the Run folder up to b17_theme_work

TYPE_NAME = {"skill": "Skill", "ui": "UI", "code": "Code", "draft": "Draft", "display": "Display", "data": "Data"}
CAPTION = {"MindMap": "How it is built: its Jobs, what each makes, its Tasks.",
           "Skill": "The skills it hands over, one row each.",
           "UI": "The pages it hands over, one row each; the live pages first.",
           "UI-plain": "The pages it hands over, one row each.",
           "Block UI": "A real Block page of the work theme, live: board.md's ui-block.",
           "Progress": "Its Jobs; what waits on you first."}

# each cell's planned look: the view buttons its Design sketch A draws (../work_ui_cells.py), so a thumb shows the
# screen as proposed until delivery/ui/ holds the agreed one
CELL_LOOK = {"s04": ("b17_theme_work", "Report", ["MindMap", "Skill", "UI"]),
             "s51": ("b17_theme_work", "Report", ["MindMap", "Skill", "UI"]),
             "s52": ("b17_theme_work", "Work", ["Progress"]),
             "s53": ("b17_theme_work", "Studio", ["Interface", "Navigation", "Block UI"]),
             "s54": ("j01_work_ladder_contract", "Report", ["MindMap", "Skill"]),
             "s55": ("j01_work_ladder_contract", "Work", ["Tasks"]),
             "s56": ("j01_work_ladder_contract", "Studio", ["This Job", "Block"]),
             "s57": ("t01_skill_section", "Report", ["MindMap", "Result"]),
             "s58": ("t01_skill_section", "Work", ["Runs"]),
             "s59": ("t01_skill_section", "Studio", ["This Task", "Block"])}


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def diff(on: bool) -> str:
    return " diff" if on else ""


def attr(*classes) -> str:
    names = " ".join(c for c in classes if c)
    return f' class="{names}"' if names else ""


# ── what the page reads from disk ───────────────────────────────────────────────────────────────────────────────────
def first_title(md: Path) -> str:
    first = md.read_text(encoding="utf-8").splitlines()[0] if md.is_file() else ""
    return first.split(" · ", 1)[1].strip() if " · " in first else md.parent.name


def plain(text: str) -> str:
    """A line as the map shows it: no (JL ...) tag, no backticks (focus_page.parts_mindmap does the same)."""
    return re.sub(r"\s*\(JL [^)]*\)", "", text).replace("`", "").strip()


def face(topic: Path) -> dict:
    """An sNN face's facts, as frame._note_facts reads them, plus its For: line, its address and where it sits."""
    text = (topic / f"{topic.name}.md").read_text(encoding="utf-8")
    field = lambda key: (re.search(rf"(?m)^\*\*{key}:\*\*[^\S\n]*(.+)$", text) or [None, ""])[1].strip()
    whole = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    whole = re.sub(r"\s+", " ", whole.group(1)).strip() if whole else ""
    first = re.match(r"(.+?[.;])(?:\s|$)", whole)
    nn, owner = topic.name.split("-", 1)[0], topic.parent
    rung = "" if owner == BLOCK else ".".join(p.name.split("_")[0] for p in (owner.parent, owner))
    short = lambda name: name.split("_", 1)[1] if "_" in name else name
    address = (f"b17.{rung}-{nn}:theme_work.{short(owner.parent.name)}.{short(owner.name)} @ " if rung
               else f"b17-{nn}:theme_work @ ")
    slide = ""
    record = topic / f"{topic.name}.slides.json"
    if record.is_file():
        try:
            image = json.loads(record.read_text(encoding="utf-8"))["slides"][0]["image"]
            slide = image if (topic / image).is_file() else ""
        except (ValueError, KeyError, IndexError, TypeError):
            slide = ""
    render = topic / "delivery" / "render.yaml"
    card = render.read_text(encoding="utf-8") if render.is_file() else ""
    rel = topic.relative_to(BLOCK).as_posix()
    return {"nn": nn, "name": topic.name, "title": first_title(topic / f"{topic.name}.md"), "rung": rung,
            "type": field("Delivery type").strip("`").lower(), "address": address,
            "tags": [t.strip(" `") for t in re.split(r"[·,|]", field("Tags")) if t.strip(" `")],
            "gives": re.sub(r";\s*made by .*$", "", field("For")), "topic": first.group(1) if first else whole,
            "slug": topic.name.split("-", 1)[1].replace("-", "_"),
            "pieces": re.findall(r'(?m)^\s*-\s*code:\s*"([^:"]+):', card),
            "maker": (re.findall(r"(?m)^\s*by:\s*(j\d+_[A-Za-z0-9_]+)/", card) or [""])[0],
            "drawing": f"{UP}{rel}/{topic.name}.png", "slide": f"{UP}{rel}/{slide}" if slide else "",
            "slides": (topic / f"{topic.name}.slides.html").is_file(),
            "mind": (topic / f"{topic.name}.mindmap.md").is_file()}


OWN = [face(BLOCK / n) for n in sorted(p.name for p in BLOCK.glob("s[0-9]*-*/") if (p / f"{p.name}.md").is_file())]
CELLS = [face(t) for task in sorted(JOB.glob("t[0-9]*_*/")) for t in sorted(task.glob("s[0-9]*-*/"))
         if (t / f"{t.name}.md").is_file()]
BY_NN = {d["nn"]: d for d in OWN + CELLS}
JOBS = [(j.name, first_title(j / f"{j.name}.md"), [(t.name, first_title(t / f"{t.name}.md"))
                                                  for t in sorted(j.glob("t[0-9]*_*/"))])
        for j in sorted(BLOCK.glob("j[0-9]*_*/"))]
BOARD = (BLOCK / "board.md").read_text(encoding="utf-8")
LIVE = [(key, word, (re.search(rf"(?m)^ui-{key}:\s*(\S+)", BOARD) or [None, ""])[1])
        for key, word in (("block", "Block page"), ("job", "Job page"), ("task", "Task page"))]


def collection_runs() -> list:
    """Each collection Run at b17 or below: (title, the sNN its for: names, its folder name, it waits on you). It
    waits when its card says waiting, or when it is one of this round's j03 forms, built now and read after."""
    out = []
    for card in sorted(BLOCK.glob("**/runs/r*_collect_*/run.yaml")):
        text = card.read_text(encoding="utf-8")
        state = (re.search(r"(?m)^status:\s*(\S+)", text) or [None, ""])[1]
        about = (re.search(r"(?m)^target:.*?-(s\d+):", text) or [None, ""])[1]
        questions = card.parent / "question_collection.md"
        title = questions.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip() if questions.is_file() \
            else card.parent.name
        waits = state == "waiting" or (state == "planned" and JOB in card.parents)
        out.append((title, about, card.parent.name, waits))
    return sorted(out, key=lambda r: not r[3])


RUNS = collection_runs()
WAITS = [r for r in RUNS if r[3]]
WAIT_ABOUT = {r[1] for r in WAITS}
ASKED_ABOUT = {r[1] for r in RUNS}


# ── the page's parts ───────────────────────────────────────────────────────────────────────────────────────────────
PREVIEW_CSS = """
/* preview only: the page without its fixed rails and its Purpose (no option changes them) */
.focus-page.pv{max-width:900px;padding:14px 22px 30px}.pv h1{margin:4px 0 8px}
.pv .focus-card{margin-top:4px}.pv .focus-card .focus-content{padding:10px 0 0}
.pv .section-views{flex-wrap:wrap;gap:6px;margin:0 0 6px}.pv .section-views a{font-size:13px;padding:3px 11px}
.pv .focus-content>.view-caption,.screen .view-caption{margin:0 0 8px;font-size:12.5px;color:var(--muted)}
.pv .status-row{padding:9px 0}.pv .studio-row{grid-template-columns:minmax(0,1fr) 176px;gap:14px}
.pv .row-name{font-size:14px}.pv .row-address{font-size:13px}
.pv .row-line{font-size:12.5px;margin:2px 0}.pv .row-meta{font-size:12px;color:var(--muted);margin:2px 0}
.pv .row-verbs{margin:5px 0 0;gap:6px;flex-wrap:wrap}.pv .row-verb{font-size:11.5px;padding:1px 8px}
.pv .row-thumb img,.pv .row-thumb .look{display:block;width:176px;height:99px;object-fit:contain;background:#fff;
 border:1px solid var(--line);border-radius:6px}
.pv .row-where{margin-left:8px;font-size:11.5px;color:var(--muted)}
.pv .focus-sub{margin:10px 0 2px;font-size:13.5px}
.ix-wait{border-color:light-dark(#ffa94d,#b35c00)!important;color:light-dark(#b35c00,#ffc078)!important}
.look{overflow:hidden;padding:6px 8px;font-size:8.5px;line-height:1.35;color:#1c1c1c;background:#fff}
.look .lk-file,.look .lk-crumb,.look .lk-h1,.look b{display:block}
.look .lk-file{font:7.5px ui-monospace,Menlo,monospace;color:#6f6f6b;border-bottom:1px solid #e3e3e6;padding-bottom:2px;margin-bottom:3px}
.look b{font-size:10px;margin:0 0 2px}
.look pre{font:7.5px/1.4 ui-monospace,Menlo,monospace;margin:0;white-space:pre;overflow:hidden}
.look table{border-collapse:collapse;width:100%;font-size:7.5px}.look td{border-bottom:1px solid #e3e3e6;padding:1px 3px}
.look .lk-crumb{font-size:6.5px;color:#6f6f6b}.look .lk-h1{font-size:10px;font-weight:700}
.look .lk-h1 span{font-weight:400;color:#6f6f6b;margin-left:4px}
.look .lk-views{display:flex;gap:3px;margin:3px 0 5px}.look .lk-views i{font-style:normal;border:1px solid #e3e3e6;
 border-radius:3px;padding:0 3px;font-size:7px}.look .lk-views i.on{border-color:#1864ab;color:#1864ab}
.look .lk-bar{display:block;height:6px;border-radius:3px;background:#eef0f2;margin:4px 0}.look .lk-bar.short{width:60%}
.live-frame{border:1px solid var(--line);border-radius:8px;padding:10px 12px;height:330px}
.live-frame .lk-crumb{font-size:10.5px}.live-frame .lk-h1{font-size:16px}.live-frame .lk-views i{font-size:11px;padding:1px 8px}
.live-frame .lk-bar{height:12px;margin:10px 0}
.gone{padding:12px 14px;text-align:center;color:var(--muted);border:1px dashed var(--line);border-radius:8px;font-size:12.5px;
 margin:8px 0 0}
.wait-band{border:1px solid light-dark(#ffa94d,#b35c00);background:light-dark(#fff4e6,#3a2a12);border-radius:8px;
 padding:7px 12px;margin:0 0 10px;font-size:12px;line-height:1.5;color:light-dark(#7a3e00,#ffc078)}
.wait-band b{color:light-dark(#b35c00,#ffc078)}.wait-band .row-verb{margin-left:8px;background:var(--paper)}
.mm{display:grid;grid-template-columns:104px minmax(0,1fr);gap:0 16px;align-items:center;border:1px solid var(--line);
 border-radius:10px;padding:9px;background:var(--paper)}
.mm-root{border:1.5px solid var(--ink);border-radius:10px;padding:8px 9px;font-weight:700;font-size:11.5px;overflow-wrap:anywhere}
.mm-col{display:flex;flex-direction:column;gap:5px;border-left:1.5px solid var(--line);padding-left:11px}
.mm-br{display:grid;grid-template-columns:150px minmax(0,1fr);gap:0 12px;align-items:center}
.mm-node{border:1.5px solid var(--ink);border-radius:9px;padding:4px 8px;font-size:11px;line-height:1.3;background:var(--paper)}
.mm-node small{display:block;font-size:9px;color:var(--muted);overflow-wrap:anywhere}
.mm-leaves{list-style:none;margin:0;padding:0 0 0 9px;border-left:1.5px solid var(--line)}
.mm-leaves li{font-size:10.5px;line-height:1.45;margin:0 0 1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mm-leaves li.sub{padding-left:16px}
.mm-pill{display:inline-block;background:light-dark(#e7f5ff,#253749);color:light-dark(#1864ab,#91caff);font-weight:600;
 font-size:9px;border-radius:9px;padding:0 6px;margin-right:5px;border:1px solid transparent}
.mm-box{display:block;margin:1px 0 2px 10px;padding:2px 7px;background:var(--wash);border:1px solid var(--line);
 border-radius:6px;font-size:9.5px;line-height:1.35;white-space:normal;color:var(--ink)}
.mm-wait .mm-pill{background:light-dark(#fff4e6,#3a2a12);color:light-dark(#b35c00,#ffc078);border-color:light-dark(#ffa94d,#b35c00)}
.mm-said{color:light-dark(#b35c00,#ffc078);font-weight:600;margin-left:5px}
.screens{display:grid;grid-template-columns:1fr;gap:12px;align-items:start}
.screen{border:1px solid var(--line);border-radius:10px;padding:8px 10px;background:var(--paper);min-width:0}
.screen-title{font-size:14px;font-weight:700;margin:0 0 4px}.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:12.5px}
.screen .section-views{margin:0 0 4px}.screen .section-views a{font-size:11px;padding:1px 8px}
.screen .mm{zoom:.8}.screen .status-row{padding:7px 0}.screen .row-name{font-size:13px}
"""


def look_doc(head: str, body: str) -> str:
    return f'<span class="look"><span class="lk-file">haipipe-work · SKILL.md</span><b>{esc(head)}</b>{body}</span>'


def look_screen(name: str, section: str, buttons: list, live: bool = False) -> str:
    crumb = "examples-2-cms / … / work /" if live else "… / work /"
    marks = "".join(f'<i{attr("on" if k == 0 else "")}>{esc(v)}</i>' for k, v in enumerate(buttons))
    return (f'<span class="lk-crumb">{esc(crumb)} {esc(name)}</span><span class="lk-h1">{esc(name)}<span>{esc(section)}'
            f'</span></span><span class="lk-views">{marks}</span><span class="lk-bar"></span>'
            '<span class="lk-bar short"></span><span class="lk-bar"></span>')


def planned_look(d: dict) -> str:
    """The delivery as planned, small: the thing its drawing's Design sketch A proposes."""
    if d["nn"] == "s01":
        return look_doc("The work ladder", "<pre>work/bNN_&lt;block&gt;/\n└─ jNN_&lt;job&gt;/\n   └─ tNN_&lt;task&gt;/\n"
                                          "      └─ rNN_&lt;run&gt;/</pre>")
    if d["nn"] == "s02":
        return look_doc("Skills of the work theme", "<table><tr><td>haipipe-task</td><td>1_base/task</td></tr>"
                                                    "<tr><td>8_stata</td><td>2_theme/work</td></tr>"
                                                    "<tr><td>9_agent</td><td>2_theme/work</td></tr></table>")
    name, section, buttons = CELL_LOOK.get(d["nn"], ("b17_theme_work", "Report", ["MindMap"]))
    return f'<span class="look">{look_screen(name, section, buttons)}</span>'


def thumb(d: dict, kind: str = "look", mark: bool = False) -> str:
    """A row's picture: its planned look (my pick, Q2 C), its drawing card (A) or its deck's first slide (B)."""
    if kind == "drawing" or (kind == "slide" and not d["slide"]):
        inner = f'<img src="{esc(d["drawing"])}" alt="{esc(d["name"])}, its drawing">'
    elif kind == "slide":
        inner = f'<img src="{esc(d["slide"])}" alt="{esc(d["name"])}, its first slide">'
    else:
        inner = planned_look(d)
    return f'<span class="row-thumb{diff(mark)}">{inner}</span>'


def tags(d: dict) -> str:
    """The tags below an sNN (s51-D02): each opens its part in the pop-out; Slide only when it has a deck, Interaction
    only when a form is about it, orange with 🙋 while one waits (focus_page.interaction_button)."""
    out = (['<a class="row-verb main">Slide</a>'] if d["slides"] else []) + ['<a class="row-verb">Draw</a>']
    out += (['<a class="row-verb">Mind map</a>'] if d["mind"] else []) + ['<a class="row-verb">Work</a>',
                                                                         '<a class="row-verb">Delivery</a>']
    if d["nn"] in ASKED_ABOUT:
        waits = d["nn"] in WAIT_ABOUT
        out.append(f'<a{attr("row-verb", "ix-wait" if waits else "")}>{"🙋 " if waits else ""}Interaction</a>')
    return f'<p class="row-verbs">{"".join(out)}</p>'


def line_of(d: dict, kind: str) -> str:
    if kind == "pieces":
        return f'{" · ".join(d["pieces"])}, built by {d["maker"]}' if d["pieces"] else "no delivery/render.yaml yet"
    return d["topic"] if kind == "topic" else d["gives"]


def row(d: dict, *, pic: str = "look", line: str = "gives", where: bool = False, mark_pic: bool = False,
        mark_line: bool = False) -> str:
    """One delivery, one row: address and name, its one word, its one line, its tags; its picture on the right."""
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", esc(line_of(d, line)))
    at = f'<span class="row-where">{esc(d["rung"])}</span>' if where and d["rung"] else ""
    return (f'<article class="status-row studio-row"><div><p class="row-title">'
            f'<span class="row-address">{esc(d["address"])}</span><span class="row-name">{esc(d["slug"])}</span>'
            f'<span class="row-stage">planned</span>{at}</p>'
            f'<p class="row-line{diff(mark_line)}">{text}</p>{tags(d)}</div>{thumb(d, pic, mark_pic)}</article>')


def views(names: list, on: str, marked=()) -> str:
    links = "".join(f'<a href="#"{" aria-current=page" if n == on else ""}{attr("diff" if n in marked else "")}>'
                    f'{esc(n)}</a>' for n in names)
    return f'<nav class="section-views" aria-label="Views">{links}</nav>'


def page(title: str, body: str, *, bar: str = "", caption: str = "", section: str = "Report") -> str:
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            "<body><main class=\"focus-page pv\">"
            "<div class=\"focus-crumb\">Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work</div>"
            f"<h1>b17_theme_work<span class=\"h1-section\">{esc(section)}</span></h1>{bar}"
            f"<section class=\"focus-card\"><div class=\"focus-content\">{cap}{body}</div></section>"
            "</main></body></html>")


def screen(section: str, inner: str, *, bar: str = "", caption: str = "", mark: bool = False) -> str:
    """One section drawn small, so two can sit side by side."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">b17_theme_work<span>{esc(section)}</span>'
            f'</div>{bar}{cap}<div class="focus-content">{inner}</div></section>')


def of_type(dtype: str, pool=None) -> list:
    """The deliveries of one type: what waits first, then in the order of the Jobs that make them."""
    chosen = [d for d in (OWN if pool is None else pool) if d["type"] == dtype]
    return sorted(chosen, key=lambda d: (d["nn"] not in WAIT_ABOUT, d["maker"] or "~", d["nn"]))


TYPES = list(dict.fromkeys(d["type"] for d in sorted(OWN, key=lambda d: (d["maker"] or "~", d["nn"])) if d["type"]))
BAR = ["MindMap"] + [TYPE_NAME[t] for t in TYPES]                 # MindMap · Skill · UI


# ── the live pages (board.md ui-block, ui-job, ui-task) ───────────────────────────────────────────────────────────
def live_name(key: str, url: str) -> str:
    target = url.rstrip("/").rsplit("/", 1)[-1]
    return target if key == "block" else "_".join(target.split("_")[:3]) + "_…"


def live_rows(mark: bool) -> str:
    rows = []
    for key, word, url in LIVE:
        if not url:
            continue
        name = live_name(key, url)
        look = look_screen(name, "Report" if key == "block" else "Work",
                           ["MindMap", "Status"] if key == "block" else ["Progress"], live=True)
        rows.append(f'<article class="status-row studio-row"><div><p class="row-title"><span class="row-name">{word}'
                    f'</span><span class="row-stage">live</span></p><p class="row-line"><code>ui-{key}:</code> '
                    f'{esc(name)}, a real page of the work theme</p><p class="row-verbs"><a class="row-verb main">Open'
                    f'</a></p></div><span class="row-thumb"><span class="look">{look}</span></span></article>')
    return f'<div{attr("diff" if mark else "")}><h3 class="focus-sub">Live pages</h3>{"".join(rows)}</div>'


def live_frame() -> str:
    name = live_name("block", LIVE[0][2])
    return (f'<div class="live-frame look diff">{look_screen(name, "Report", ["MindMap", "Status"], live=True)}'
            '<span class="lk-bar short"></span><span class="lk-bar"></span><span class="lk-bar short"></span></div>')


# ── the MindMap, drawn like the draft map: a pill, a short title, one plain paragraph box ─────────────────────────────
def sbox(d: dict) -> str:
    said = plain(d["topic"])
    return f'<span class="mm-box">{esc(TYPE_NAME.get(d["type"], d["type"]))}, planned. {esc(said[:1].upper() + said[1:])}</span>'


def leaf(d: dict, *, box: bool = True, sub: bool = False, flag: bool = False, mark: bool = False) -> str:
    waits = flag and d["nn"] in WAIT_ABOUT
    said = '<span class="mm-said">🙋 waits on you</span>' if waits else ""
    return (f'<li{attr("sub" if sub else "", "mm-wait" if waits else "", "diff" if waits and mark else "")}>'
            f'<span class="mm-pill">{esc(d["name"])}</span>{esc(d["title"])}{said}{sbox(d) if box else ""}</li>')


def task_leaf(name: str, title: str, *, sub: bool = False) -> str:
    return f'<li{attr("sub" if sub else "")}><span class="mm-pill">{esc(name)}</span>{esc(title)}</li>'


def branch(node: str, leaves: str, mark: bool) -> str:
    return f'<div class="mm-br"><div class="mm-node{diff(mark)}">{node}</div><ul class="mm-leaves">{leaves}</ul></div>'


def job_node(name: str, title: str) -> str:
    return f'<small>{esc(name)}</small>{esc(title)}'


def cells_of(job: str, task: str) -> list:
    rung = f'{job.split("_")[0]}.{task.split("_")[0]}'
    return [d for d in CELLS if d["rung"] == rung]


def mindmap(branches: list) -> str:
    return f'<div class="mm"><div class="mm-root">b17_theme_work</div><div class="mm-col">{"".join(branches)}</div></div>'


def map_by_job(mark: bool = False, flag: bool = False, mark_flags: bool = False) -> str:
    out = []
    for name, title, tasks in JOBS:
        leaves = "".join(leaf(d, flag=flag, mark=mark_flags) for d in OWN if d["maker"] == name)
        for tname, ttitle in tasks:
            leaves += task_leaf(tname, ttitle)
            leaves += "".join(leaf(c, box=False, sub=True, flag=flag, mark=mark_flags) for c in cells_of(name, tname))
        out.append(branch(job_node(name, title), leaves, mark))
    return mindmap(out)


def map_by_type(mark: bool = False) -> str:
    out = []
    for dtype in TYPES:
        leaves = ""
        for d in of_type(dtype):
            job = next((j for j in JOBS if j[0] == d["maker"]), None)
            leaves += leaf(d)
            if job:
                leaves += task_leaf(job[0], job[1], sub=True)
                leaves += "".join(task_leaf(t, tt, sub=True) for t, tt in job[2][:1]) + (
                    '<li class="sub">…</li>' if len(job[2]) > 1 else "")
        out.append(branch(f'<small>delivery type</small>{esc(TYPE_NAME[dtype])}', leaves, mark))
    return mindmap(out)


def map_today(mark: bool = False) -> str:
    groups = list(dict.fromkeys(d["tags"][0] for d in OWN if d["tags"]))
    out = [branch(f'<small>Studio group</small>{esc(g)}', "".join(leaf(d) for d in OWN if d["tags"][:1] == [g]), mark)
           for g in groups]
    for name, title, tasks in JOBS:
        leaves = "".join(task_leaf(t, tt) + "".join(leaf(c, box=False, sub=True) for c in cells_of(name, t))
                         for t, tt in tasks)
        out.append(branch(job_node(name, title), leaves, mark))
    return mindmap(out)


# ── what waits on you ───────────────────────────────────────────────────────────────────────────────────────────────
def band() -> str:
    titles = " · ".join(esc(t) for t, _, _, _ in WAITS)
    verb = "Answer all" if len(WAITS) > 1 else "Answer"
    return (f'<div class="wait-band diff"><b>🙋 Waits on you:</b> {titles}<a class="row-verb ix-wait">{verb}</a></div>'
            if WAITS else "")


def work_rows() -> str:
    """Work › Progress as it reads today (focus_page.status_html): the Block's own forms first, what waits orange,
    then one row per Job with its goal and its Interaction button."""
    own = [r for r in RUNS if (BLOCK / "runs" / r[2]).is_dir()]
    rows = []
    for title, about, run, waits in own:
        topic = BY_NN[about]["name"] if about in BY_NN else about
        rows.append(f'<article class="status-row"><span class="row-name">{esc(title)}</span>'
                    f'<p class="row-line">about {esc(topic)}</p><p class="row-meta">{esc(run)} '
                    f'<a{attr("row-verb", "ix-wait" if waits else "")}>{"🙋 " if waits else ""}Interaction</a></p></article>')
    for name, title, tasks in JOBS:
        below = any(r[3] and any((BLOCK / name).glob(f"**/runs/{r[2]}")) for r in RUNS)   # a form waits in this Job
        rows.append(f'<article class="status-row"><span class="row-name">{esc(name)}</span>'
                    f'<p class="row-line">{esc(title)}</p><p class="row-meta">its Tasks open'
                    + (' <a class="row-verb ix-wait">🙋 Interaction</a>' if below else '') + '</p></article>')
    return "".join(rows)


# ── the seventeen pages ─────────────────────────────────────────────────────────────────────────────────────────────
def previews() -> dict:
    out = {}
    skill, ui = of_type("skill"), of_type("ui")
    bar_ui, bar_skill, bar_map = views(BAR, "UI"), views(BAR, "Skill"), views(BAR, "MindMap")
    # Q1 · the view list: where the live Block, Job and Task pages (board.md ui-block, ui-job, ui-task) go
    out["q1-a"] = page("Q1 A", live_rows(True) + '<h3 class="focus-sub">Deliveries</h3>' + "".join(row(d) for d in ui),
                       bar=bar_ui, caption=CAPTION["UI"])
    out["q1-b"] = page("Q1 B", live_frame(), bar=views(BAR + ["Block UI", "Job UI", "Task UI"], "Block UI",
                                                        marked=("Block UI", "Job UI", "Task UI")),
                       caption=CAPTION["Block UI"])
    out["q1-c"] = page("Q1 C", "".join(row(d) for d in ui)
                       + '<p class="gone diff">No live pages: the Block UI, Job UI and Task UI views go, and nothing '
                         'shows board.md\'s ui-block, ui-job and ui-task.</p>', bar=bar_ui, caption=CAPTION["UI-plain"])
    # Q2 · the row's picture (s51's open question), on the Skill view
    for key, kind in (("a", "drawing"), ("b", "slide"), ("c", "look")):
        out[f"q2-{key}"] = page(f"Q2 {key.upper()}", "".join(row(d, pic=kind, mark_pic=True) for d in skill),
                                bar=bar_skill, caption=CAPTION["Skill"])
    # Q3 · which sNN the type views list: the Block's own, or with every one below, marked where it lives
    out["q3-a"] = page("Q3 A", '<div class="diff">' + "".join(row(d) for d in ui) + "</div>",
                       bar=bar_ui, caption=CAPTION["UI-plain"])
    out["q3-b"] = page("Q3 B", '<div class="diff">' + "".join(row(d, where=True) for d in of_type("ui", OWN + CELLS))
                       + "</div>", bar=bar_ui, caption=CAPTION["UI-plain"])
    # Q4 · the MindMap's first level
    out["q4-a"] = page("Q4 A", map_by_job(mark=True), bar=bar_map, caption=CAPTION["MindMap"])
    out["q4-b"] = page("Q4 B", map_by_type(mark=True), bar=bar_map, caption="How it is built, by what it hands over.")
    out["q4-c"] = page("Q4 C", map_today(mark=True), bar=bar_map, caption="Its topics by Studio group, then its Jobs.")
    # Q5 · what waits on you, on the view the Block opens on; C moves it to Work, so two places sit side by side
    out["q5-a"] = page("Q5 A", map_by_job(flag=True, mark_flags=True), bar=bar_map, caption=CAPTION["MindMap"])
    out["q5-b"] = page("Q5 B", band() + map_by_job(flag=True), bar=bar_map, caption=CAPTION["MindMap"])
    out["q5-c"] = page("Q5 C", '<div class="screens">'
                       + screen("Report", map_by_job(), bar=views(BAR, "MindMap"), caption=CAPTION["MindMap"])
                       + screen("Work", work_rows(), bar=views(["Progress"], "Progress"), caption=CAPTION["Progress"],
                                mark=True) + "</div>")
    # Q6 · the row's one line, on the Skill view
    for key, kind in (("a", "gives"), ("b", "pieces"), ("c", "topic")):
        out[f"q6-{key}"] = page(f"Q6 {key.upper()}", "".join(row(d, line=kind, mark_line=True) for d in skill),
                                bar=bar_skill, caption=CAPTION["Skill"])
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/ · views {' · '.join(BAR)} · "
          f"waiting: {', '.join(t for t, _, _, _ in WAITS)}")


if __name__ == "__main__":
    main()
