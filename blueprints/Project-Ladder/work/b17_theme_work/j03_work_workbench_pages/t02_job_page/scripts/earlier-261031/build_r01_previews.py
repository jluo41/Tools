"""r01's option previews, for s54 · Job UI: Report (JL 261031: "make detailed interaction ... I will just check in the
interaction section"): one small page per option, drawn in the workbench's own look, with b17's real names read from
disk: the Job faces and their ## Tasks order, each Task's face, each Run's card (run.yaml) and ticket, each sNN's face,
its first slide and its delivery/render.yaml. The MindMap is drawn by haipipe-mindmap's own renderer (mmmap.draw), as
focus_page.parts_mindmap draws a live map; the cards use the Studio row's own classes from focus.css.

Nothing b17 hands over is made yet, so every delivery and every piece shows its planned look, marked planned (s51-D03),
and carries one word, its current version (s51-D05). The part an option changes carries class="diff", which the form
boxes in orange. The form shows a preview at half size in a frame 600 pixels tall, so what differs sits in that height:
no goal-line (no option changes it), compact rows, pieces small.

Writes runs/r01_collect_job_report_views/option-q<N>-<k>.html; question_collection.md links each one under its option.
Rerun after changing anything here, never edit the pages:

    python build_r01_previews.py
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path

import yaml

TASK = Path(__file__).resolve().parents[1]                       # t02_job_page
RUN = TASK / "runs" / "r01_collect_job_report_views"
J03 = TASK.parent                                                # j03_work_workbench_pages
BLOCK = J03.parent                                               # b17_theme_work
J01 = BLOCK / "j01_work_ladder_contract"
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-mindmap/scripts"))
import mmbuild  # noqa: E402  (haipipe-mindmap's own tree builder and renderer, as the live MindMap)
import mmmap  # noqa: E402
import mmtree  # noqa: E402

TAGS = ("Slide", "Draw", "Mind map", "Work", "Delivery")      # the tags below an sNN (s51-D02)
CAPTIONS = {"mindmap": "How it is built, as a map: what it makes, its Tasks, their Runs.",
            "mindmap-tasks": "How it is built, as a map: its Tasks and their Runs.",
            "type": "What this Job hands over."}

# The planned look of each screen at j03's Tasks, as j03/work_ui_cells.py's Design A sketches draw them (page, the
# open view first): what s04's pieces will hold once run-design-*-page writes them.
SCREENS = {"s51": ("b17_theme_work", "Report", ["MindMap", "Skill", "UI"], 1),
           "s52": ("b17_theme_work", "Work", ["Progress"], 0),
           "s53": ("b17_theme_work", "Studio", ["Block UI", "Job UI", "Task UI"], 0),
           "s54": ("j01_work_ladder_contract", "Report", ["MindMap", "Skill"], 1),
           "s55": ("j01_work_ladder_contract", "Work", ["Tasks"], 0),
           "s56": ("j01_work_ladder_contract", "Studio", ["This Job", "Block"], 0),
           "s57": ("t01_skill_section", "Report", ["MindMap", "Result"], 1),
           "s58": ("t01_skill_section", "Work", ["Runs"], 0),
           "s59": ("t01_skill_section", "Studio", ["This Task", "Block"], 0)}

# The planned look of j01's three pieces (nothing is written yet): where each lands, drawn small, in the words of its
# Run's ticket (ask: and close:). `whole` is the same piece at full length, for Q1 C.
PLANNED = {
    # s01's one piece since its rewrite (JL 261031: "you should update this, right?", skills/2_theme/work): the whole
    # SKILL.md, with JL's rule that a Run and a Studio topic get no page
    "haipipe-work/SKILL.md": {
        "file": "haipipe-work · SKILL.md", "head": "The work ladder",
        "lines": ["Five rungs, and which of them gets a page."],
        "pre": ("Block   page: Report · Work · Studio\n"
                "Job     page: Report · Work · Studio\n"
                "Task    page: Report · Work · Studio\n"
                "Run     no page: a row on its Task's Work\n"
                "sNN     no page: a card where it sits"),
        "more": ["A Run opens in the pop-out from its Task's Work.",
                 "A Studio topic is a card, opened by its tags.",
                 "Each request goes to the skill that owns it."]},
    "ladder-section": {
        "file": "haipipe-work · SKILL.md", "head": "The work ladder",
        "lines": ["What a work Block, Job, Task and Run folder hold."],
        "pre": ("work/bNN_&lt;block&gt;/        board.md · sNN\n"
                "└─ jNN_&lt;job&gt;/          goal · close · its Tasks\n"
                "   └─ tNN_&lt;task&gt;/      face · scripts/ · runs/\n"
                "      └─ rNN_&lt;run&gt;/    ticket · run.yaml · result/"),
        "more": ["A Block holds its Jobs and, beside them, its sNN topics.",
                 "A Job makes one sNN's delivery; each of its Tasks builds one piece of it.",
                 "A Task holds its Runs; a Run is one ticket, its card run.yaml and its result/."]},
    "work-scaffold": {
        "file": "haipipe-work · scripts/", "head": "Scaffold a work Block, Job, Task and Run",
        "lines": ["Writes the folders the ladder section names."],
        "pre": ("bNN_&lt;block&gt;/board.md\n"
                "jNN_&lt;job&gt;/jNN_&lt;job&gt;.md\n"
                "tNN_&lt;task&gt;/tNN_&lt;task&gt;.md · scripts/ · runs/\n"
                "rNN_&lt;run&gt;/run.yaml · result/"),
        "more": ["Each level's scaffold writes the agreed folders and faces.",
                 "A new Job's face lists its Tasks in order; a new Task's face names its Runs."]},
    "demo-block": {
        "file": "a demo Block in a temp folder", "head": "Test the scaffold",
        "lines": ["Placeholders only, never real project data."],
        "pre": ("check_task_tree   the demo Block's folders and names\n"
                "workbench         the demo Block's page opens"),
        "more": ["It passes when check_task_tree finds nothing to fix and the page opens."]},
}

PREVIEW_CSS = """
/* preview only: the page without its fixed rails; the right rail is drawn as one line under the path */
.focus-page.pv{max-width:none;padding:14px 22px 30px}.pv h1{margin:6px 0 10px}
.rail-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0 0;font-size:12.5px}
.rail-line .rl-word{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.rail-line span.rl{padding:1px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted)}
.rail-line span.rl.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .section-views{flex-wrap:wrap;margin:0 0 4px}
.pv .focus-card .focus-content{padding:8px 0 0}
.pv .focus-content>.view-caption{margin:0 0 10px}
.pv .focus-content .focus-sub{margin:14px 0 6px}
.pv .studio-row{grid-template-columns:minmax(0,1fr) 190px;gap:14px;padding:11px 14px;margin:0 0 8px}
.pv .row-thumb img,.pv .row-thumb.none{width:190px;height:107px}
.pv .studio-row.small{grid-template-columns:minmax(0,1fr) 120px;padding:8px 12px}
.pv .studio-row.small .row-thumb img{width:120px;height:68px}.pv .studio-row.small .row-name{font-size:14px}
.pv .studio-row.small .row-line{font-size:12px}.pv .studio-row.small .row-verb{font-size:11.5px;padding:1px 8px}
.row-stage.word{border-style:dashed}
.row-verb.wait{border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)}
.piece{display:grid;grid-template-columns:minmax(0,1fr) 290px;gap:14px;align-items:start;border:1px solid var(--line);
 border-radius:10px;padding:10px 14px;margin:0 0 8px;background:var(--paper)}
.piece.text{display:flex;flex-wrap:wrap;align-items:center;gap:4px 12px;padding:7px 14px;margin:0 0 6px}
.piece.text>div{display:contents}.piece.text .piece-by,.piece.text .row-verbs{margin:0}
.piece .row-name{font-size:15px}.piece .row-title{margin:0}
.piece-by{font-size:12.5px;color:var(--muted);margin:3px 0 0}.piece-by code{font-size:11.5px}
.piece .row-verbs{margin:8px 0 0}
.thing .doc{zoom:.72}
.minis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.mini{border:1px solid var(--line);border-radius:6px;padding:5px 6px;background:var(--bg);font-size:10px;min-width:0}
.mini-cap{font-size:9.5px;color:var(--muted)}.mini-h1{font-size:11px;font-weight:700;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.mini-h1 span{font-weight:400;color:var(--muted);margin-left:4px}
.mini-views{display:flex;flex-wrap:wrap;gap:3px;margin:4px 0}.mini-views i{font-style:normal;border:1px solid var(--line);border-radius:4px;padding:0 4px;font-size:9px}
.mini-views i.on{border-color:var(--accent);color:var(--accent)}
.mini-lines span{display:block;height:5px;border-radius:3px;background:var(--wash);margin:4px 0}
.mini-lines span:nth-child(2){width:70%}.mini-lines span:nth-child(3){width:85%}
.doc{border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-size:12.5px;background:var(--bg)}
.doc-file{font:11px ui-monospace,Menlo,monospace;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:4px;margin-bottom:6px}
.doc h4{margin:0 0 4px;font-size:13.5px}.doc p{margin:0 0 4px}
.doc pre{font:11px/1.5 ui-monospace,Menlo,monospace;margin:4px 0;white-space:pre;overflow:hidden}
.whole{margin:0 0 12px}.whole .piece-by{margin:0 0 6px}.whole .doc{font-size:13.5px;padding:12px 14px}
.whole .doc h4{font-size:15px}.whole .doc pre{font-size:12px}
.note-line{font-size:13px;color:var(--muted);border:1px dashed var(--line);border-radius:8px;padding:10px 12px;margin:0}
/* the MindMap as the live page draws it, with its columns narrowed so a half-size frame holds it */
.pv .focus-map .pm{grid-template-columns:170px auto;gap:0 30px}
.pv .focus-map .pm-para{grid-template-columns:205px auto;gap:0 30px}
.pv .focus-map .pm-detail{max-width:330px}
"""


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def diff(on: bool) -> str:
    return " diff" if on else ""


def rel(path: Path) -> str:
    """A file's path from the Run folder, so the form serves it beside the preview."""
    return Path(os.path.relpath(path, RUN)).as_posix()


# ── what the disk says ─────────────────────────────────────────────────────────────────────────────────────────────
def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def field(text: str, key: str) -> str:
    """A face's header line, `goal: …`, or its bold line, `**For:** …`."""
    m = re.search(rf"(?mi)^(?:\*\*{re.escape(key)}:\*\*|{re.escape(key)}:)[^\S\n]*(.+)$", text)
    return m.group(1).strip() if m else ""


def title(face: Path) -> str:
    """A face's own short title: the words after ' · ' on its first line."""
    first = read(face).split("\n", 1)[0]
    return first.split(" · ", 1)[1].strip() if " · " in first else ""


def tasks(job: Path) -> list:
    """A Job's Tasks in its face's ## Tasks order (the plan's order, not the folders')."""
    names = re.findall(r"(?m)^\d+\.\s+(t\d+_[A-Za-z0-9_]+)", read(job / f"{job.name}.md"))
    return [job / n for n in names if (job / n).is_dir()]


def runs(task: Path) -> list:
    out = []
    for card in sorted((task / "runs").glob("*/run.yaml")):
        data = yaml.safe_load(card.read_text(encoding="utf-8")) or {}
        ticket = read(card.parent / f"{card.parent.name}.md")
        out.append({"name": card.parent.name, "status": data.get("status") or "", "ask": field(ticket, "ask"),
                    "collect": data.get("type") == "collect"})
    return out


def address(topic: Path) -> tuple:
    """How the workbench names an sNN (frame.topic_label): b17-s01:theme_work @ work_ladder, or
    b17.j03.t01-s51:theme_work.work_workbench_pages.block_page @ block_ui_report."""
    chain = [topic.parent, *topic.parent.parents]
    chain = chain[:chain.index(BLOCK) + 1][::-1]
    ids = ".".join(p.name.split("_")[0] for p in chain)
    shorts = ".".join(p.name.split("_", 1)[1] for p in chain)
    nn, short = topic.name.split("-", 1)
    return f"{ids}-{nn}:{shorts} @ ", short.replace("-", "_")


def sentence(text: str) -> str:
    """Its first sentence, the (JL …) quote off, as the map's box writes it."""
    first = re.match(r"(.+?[.;])(?:\s|$)", text)
    words = re.sub(r"\s*\(JL [^)]*\)", "", first.group(1) if first else text).strip().rstrip(".;")
    return words[:1].upper() + words[1:] + "."


def topic(folder: Path) -> dict:
    face = read(folder / f"{folder.name}.md")
    line = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", face, re.S)
    gives = re.sub(r"`", "", field(face, "For")).split("; made by")[0]
    record = folder / f"{folder.name}.slides.json"
    first = (json.loads(read(record)).get("slides") or [{}])[0] if record.is_file() else {}
    slide = folder / first["image"] if first.get("image") else None   # a text-only deck has no picture: use the card
    lead, short = address(folder)
    return {"folder": folder, "nn": folder.name.split("-")[0], "lead": lead, "short": short,
            "topic": sentence(" ".join(line.group(1).split())) if line else "", "for": gives,
            "type": field(face, "Delivery type").strip("`"),
            "picture": slide if slide and slide.is_file() else folder / f"{folder.name}.png",
            "tags": [t for t in TAGS if t != "Slide" or (folder / f"{folder.name}.slides.html").is_file()],
            "asks": interactions(folder.parent, folder)}


def interactions(page: Path, about: Path | None = None) -> str:
    """The Interaction button's state from the collection Runs under a page: 'wait' (one waits for you), 'plain', or ''.
    With `about`, only those whose for: line names that sNN."""
    states = []
    for card in sorted(page.glob("**/runs/*_collect_*/run.yaml")):
        text = read(card)
        target = field(text, "target")
        if about is not None and f"-{about.name.split('-')[0]}:" not in target:
            continue
        states.append(field(text, "status"))
    return "wait" if "waiting" in states else "plain" if states else ""


def pieces(folder: Path) -> list:
    """An sNN's pieces in its delivery/render.yaml, each with the Task and Run its by: names."""
    data = yaml.safe_load(read(folder / "delivery" / "render.yaml")) or {}
    out = []
    for p in data.get("pieces") or []:
        name, _, words = str(p.get("code") or p.get("block") or "").partition(":")
        run = folder.parent / str(p.get("by", ""))
        out.append({"name": name.strip(), "words": words.strip(), "run": run.name, "task": run.parent.parent})
    return out


# ── the page ──────────────────────────────────────────────────────────────────────────────────────────────────────
def rail(job: Path) -> str:
    """The right rail as one line: the sections this Job's page has today."""
    names = ["Report", "Work"] + (["Studio"] if list(job.glob("t*/s[0-9]*-*/")) or list(job.glob("s[0-9]*-*/")) else []) \
        + ["Interactions", "Delivery"] + (["Timeline"] if job == J03 else []) + ["Files"]
    spans = "".join(f'<span class="rl{" on" if n == "Report" else ""}">{esc(n)}</span>' for n in names)
    return f'<div class="rail-line"><span class="rl-word">Right rail</span>{spans}</div>'


def views(names: list, on: str) -> str:
    return ('<nav class="section-views" aria-label="Views">'
            + "".join(f'<a{" aria-current=page" if n == on else ""}>{esc(n)}</a>' for n in names) + "</nav>")


def page(name: str, job: Path, bar: str, caption: str, body: str, mark_caption: bool = False) -> str:
    crumb = " / ".join(["Tools-SPACE", *job.relative_to(TOOLS).parts])
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(name)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            f"<body><main class=\"focus-page pv\"><div class=\"focus-crumb\">{esc(crumb)}</div>{rail(job)}"
            f"<h1>{esc(job.name)}<span class=\"h1-section\">Report</span></h1>{bar}"
            f"<section class=\"focus-card\"><div class=\"focus-content\"><p class=\"view-caption{diff(mark_caption)}\">"
            f"{esc(caption)}</p>{body}</div></section></main></body></html>")


def verbs(names: list, asks: str = "") -> str:
    tags = "".join(f'<span class="row-verb{" main" if k == 0 and n == "Slide" else ""}">{esc(n)}</span>'
                   for k, n in enumerate(names))
    if asks:                                             # the one Interaction button, orange when a form waits
        tags += f'<span class="row-verb{" wait" if asks == "wait" else ""}">{"🙋 " if asks == "wait" else ""}Interaction</span>'
    return f'<p class="row-verbs">{tags}</p>'


def card(t: dict, word: str = "planned", small: bool = False, mark: bool = False) -> str:
    """An sNN's delivery as the Studio row draws it: its name, its one line, its one word, the tags below, its picture."""
    return (f'<article class="status-row studio-row{" small" if small else ""}{diff(mark)}"><div>'
            f'<p class="row-title"><span class="row-address">{esc(t["lead"])}</span><span class="row-name">'
            f'{esc(t["short"])}</span><span class="row-stage word">{esc(word)}</span></p>'
            f'<p class="row-line">{esc(t["for"])}</p>{verbs(t["tags"], t["asks"])}</div>'
            f'<span class="row-thumb"><img src="{esc(rel(t["picture"]))}" alt="{esc(t["nn"])}, its picture"></span>'
            "</article>")


def doc(look: dict, whole: bool = False) -> str:
    lines = look["lines"] + (look["more"] if whole else [])
    return (f'<div class="doc"><div class="doc-file">{esc(look["file"])}</div><h4>{esc(look["head"])}</h4>'
            + "".join(f"<p>{esc(x)}</p>" for x in lines[:1]) + f'<pre>{look["pre"]}</pre>'
            + "".join(f"<p>{esc(x)}</p>" for x in lines[1:]) + "</div>")


def by_line(p: dict) -> str:
    return (f'<p class="piece-by">made by <code>{esc(p["task"].name)}</code> · <code>{esc(p["run"])}</code></p>')


def piece_row(p: dict, thing: str, asks: str = "", text_only: bool = False) -> str:
    """One piece, one row: its name and its one word, the Task and Run that make it, its tags; the piece itself small."""
    head = (f'<div><p class="row-title"><span class="row-name">{esc(p["name"])}</span>'
            f'<span class="row-stage word">planned</span></p>{by_line(p)}{verbs(["Open", "Task"], asks)}</div>')
    return f'<article class="piece{" text" if text_only else ""}">{head}' + ("" if text_only else f'<div class="thing">{thing}</div>') + "</article>"


def mini(nn: str) -> str:
    name, section, names, on = SCREENS[nn]
    tabs = "".join(f'<i{" class=on" if k == on else ""}>{esc(v)}</i>' for k, v in enumerate(names))
    return (f'<div class="mini"><div class="mini-cap">{esc(nn)} · planned</div><div class="mini-h1">{esc(name)}'
            f'<span>{esc(section)}</span></div><div class="mini-views">{tabs}</div>'
            '<div class="mini-lines"><span></span><span></span><span></span></div></div>')


def job_map(job: Path, makes: dict | None) -> str:
    """The Job's MindMap through the live renderer: (Makes: the sNN it makes,) then its Tasks in the face's order, each
    with its Runs, each Run's box its ticket's ask: line (no point without its sentence, the draft map's rule)."""
    branches = []
    if makes:
        box = f'{makes["topic"]} Delivers {makes["for"]}; planned.'
        point = mmbuild.built(f'{job.name}/makes/{makes["folder"].name}', f'[{makes["folder"].name}] {makes["short"].replace("_", " ")}',
                              [], [box])
        branches.append(mmbuild.built(f"{job.name}/makes", "Makes", [point]))
    for t in tasks(job):
        points = [mmbuild.built(f"{job.name}/{t.name}/{r['name']}", f"[{r['status']}] {r['name']}", [],
                                [r["ask"]] if r["ask"] else []) for r in runs(t)]
        branches.append(mmbuild.built(f"{job.name}/{t.name}", f"[{t.name}] {title(t / f'{t.name}.md')}", points))
    root = mmbuild.built(".", job.name, branches)
    root.id = "root"
    tree = mmtree.MindMap({"mindmap": "1", "title": job.name, "built": "focus-page"}, root)
    drawn = mmmap.draw(tree, "", editable=False)
    # every item shows open, as the live map (focus_page.parts_mindmap; JL 261031: "show the mindmap for all the item")
    drawn = re.sub(r'<div class=pm-detail hidden>(?!<button type=button class=pm-pen)', '<div class=pm-detail>', drawn)
    drawn = drawn.replace('class=pm-more aria-expanded=false title="its detail">▸',
                          'class=pm-more aria-expanded=true title="its detail">▾')
    if makes:                                            # the branch this option adds is the boxed part
        drawn = drawn.replace(f'<div class=pm-para data-p="@{job.name}/makes">',
                              f'<div class="pm-para diff" data-p="@{job.name}/makes">')
    return ('<style>.focus-map .pm-detail,.focus-map .pm-detail *{white-space:normal}</style>'
            f'<div class="focus-map">{drawn}</div>')


# ── the previews ──────────────────────────────────────────────────────────────────────────────────────────────────
def previews() -> dict:
    out = {}
    s01, s04 = topic(BLOCK / "s01-work-ladder"), topic(BLOCK / "s04-workbench-page-structure")
    j01_views = ["MindMap", s01["type"].capitalize()]                  # MindMap · Skill
    j03_views = ["MindMap", s04["type"].upper() if s04["type"] == "ui" else s04["type"].capitalize()]   # MindMap · UI
    skill = dict(job=J01, bar=views(j01_views, j01_views[1]), caption=CAPTIONS["type"])

    # Q1 · each Task's result in j01's Skill view: none, small (one row per piece), or whole
    s01_pieces = pieces(s01["folder"])
    head = '<h3 class="focus-sub">The delivery</h3>' + card(s01)
    out["q1-a"] = page("Q1 A", body=head + '<h3 class="focus-sub">Its pieces</h3><p class="note-line diff">Each Task\'s '
                       'result stays on its own page: ' + " · ".join(esc(p["task"].name) for p in s01_pieces) + ".</p>",
                       **skill)
    rows = "".join(piece_row(p, doc(PLANNED[p["name"]])) for p in s01_pieces)
    out["q1-b"] = page("Q1 B", body=head + f'<h3 class="focus-sub">Its pieces, by Task</h3><div class="diff">{rows}</div>',
                       **skill)
    whole = "".join(f'<section class="whole">{by_line(p).replace("made by", esc(p["name"]) + " · made by", 1)}'
                    f'{doc(PLANNED[p["name"]], whole=True)}</section>' for p in s01_pieces)
    out["q1-c"] = page("Q1 C", body=head + f'<h3 class="focus-sub">Each Task\'s result</h3><div class="diff">{whole}</div>',
                       **skill)

    # Q2 · which deliveries j03's UI view lists: only s04 (its Tasks' screens inside its pieces), or s04 and s51 to s59
    ui = dict(job=J03, bar=views(j03_views, j03_views[1]), caption=CAPTIONS["type"])
    head = '<h3 class="focus-sub">The delivery</h3>' + card(s04)
    s04_pieces = pieces(s04["folder"])
    screens = {p["task"]: sorted(q.name.split("-")[0] for q in p["task"].glob("s[0-9]*-*") if q.is_dir())
               for p in s04_pieces}
    rows = "".join(piece_row(p, f'<div class="minis diff">{"".join(mini(nn) for nn in screens[p["task"]])}</div>',
                             interactions(p["task"])) for p in s04_pieces)
    out["q2-a"] = page("Q2 A", body=head + f'<h3 class="focus-sub">Its pieces, by Task</h3>{rows}', **ui)
    rows = "".join(piece_row(p, "", interactions(p["task"]), text_only=True) for p in s04_pieces)
    own = "".join(card(topic(q), small=True) for p in s04_pieces
                  for q in sorted(x for x in p["task"].glob("s[0-9]*-*") if x.is_dir()))
    out["q2-b"] = page("Q2 B", body=head + f'<h3 class="focus-sub">Its pieces, by Task</h3>{rows}'
                       f'<div class="diff"><h3 class="focus-sub">At its Tasks</h3>{own}</div>', **ui)

    # Q3 · what j01's MindMap shows first: Makes (s01), then its Tasks; or its Tasks only
    mind = dict(job=J01, bar=views(j01_views, "MindMap"), mark_caption=True)   # its caption says what the map holds
    out["q3-a"] = page("Q3 A", body=job_map(J01, s01), caption=CAPTIONS["mindmap"], **mind)
    out["q3-b"] = page("Q3 B", body=job_map(J01, None), caption=CAPTIONS["mindmap-tasks"], **mind)
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/")


if __name__ == "__main__":
    main()
