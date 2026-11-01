"""r03's option previews (s59 · Task UI: Studio): one small page per option that is a screen, drawn in the workbench's
own look (its focus.css, and the draft page's view sections and Ask the agent box from focus_draft.py's CSS) with b17's
real names and pictures; the names, stages, pieces and form states are read from disk on every run. The part an
option changes carries class="diff", which the form boxes in orange.

The form shows a preview at half size in a frame 600 page pixels tall, so what differs sits in that height: no Aim (no
option changes it), compact cards, and two places side by side when an option moves something between them (Q4: Studio
and Work; Q5: a card and what its Work tag opens).

Writes runs/r03_collect_task_studio_views/option-q<N>-<k>.html; question_collection.md links each one under its
option. Rerun after changing anything here, never edit the pages:

    python build_r03_previews.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]                       # t03_task_page
RUN = TASK / "runs" / "r03_collect_task_studio_views"
BLOCK = TASK.parents[1]                                          # b17_theme_work
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
SERVER = TOOLS / "plugins/haipipe-toolkit/servers/workbench"
FOCUS_CSS = SERVER / "focus-assets/focus.css"
DRAFT_PY = SERVER / "workbench-task-draft/focus_draft.py"       # its CSS string: a view's sections, Ask the agent
UP_TASK, UP_BLOCK = "../../", "../../../../"                     # from the Run folder up to t03_task_page, to b17
T01 = BLOCK / "j01_work_ladder_contract" / "t01_skill_section"   # a Task that holds no sNN and makes s01's piece
B35_T02 = TOOLS / "blueprints/Project-PageParts/work/b35_studio/j01_studio_delivery_type/t02_new_topic_for_line"

TALK, START, NEW = "Copy prompt: talk and sketch", "Copy prompt: start a topic", "New topic"
MAKES, OWNS = "This Task makes", "Its topics"                     # a view's two topic sections, in this order
WAIT_STYLE = ' style="border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)"'   # interaction_button

PREVIEW_CSS = """
/* preview only: the page without its fixed rails; the right rail drawn as one line under the path */
.focus-page.pv{max-width:860px;padding:14px 22px 26px}.pv h1{margin:6px 0 10px}
.rail-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0 0;font-size:12.5px}
.rail-line .rl-word{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.rail-line span.rl{padding:1px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted)}
.rail-line span.rl.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.rail-line span.rl.gone{text-decoration:line-through;border-style:dashed;opacity:.6}
.pv .section-views{flex-wrap:wrap}.pv .focus-card{margin-top:4px}.pv .focus-card .focus-content{padding:6px 0 0}
.pv .focus-content>.view-caption{margin:0 0 10px}
/* the real Studio row, compact, at every width (the form's frame is narrower than focus.css's 700 px break) */
.focus-page.pv .studio-row{grid-template-columns:minmax(0,1fr) 128px;gap:12px;padding:9px 12px;margin:0 0 7px}
.focus-page.pv .row-thumb img,.focus-page.pv .row-thumb.none{width:128px;height:72px}
.focus-page.pv .row-name{font-size:14px}.focus-page.pv .row-address{font-size:12px}
.focus-page.pv .row-verbs{margin:4px 0 0;flex-wrap:wrap;gap:6px}.focus-page.pv .row-verb{font-size:11.5px;padding:1px 8px}
.focus-page.pv .focus-content .row-line{font-size:12px;margin:2px 0}
.row-piece{margin-left:6px;font-size:12px;padding:1px 8px;border:1px dashed var(--muted);border-radius:9px;color:var(--muted);
 font-weight:400;vertical-align:2px}
.pv .fd-body{margin:8px 0 12px}.pv .fd-sec{margin:0 0 8px}
.empty-line{margin:2px 0 12px;font-size:13.5px;color:var(--muted)}
.made-line{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px;margin:2px 0 4px;font-size:13.5px}
.made-line .row-name{font-size:14px}.made-line .row-verb{font-size:11.5px;padding:1px 8px}
.new-topic{display:flex;gap:8px;align-items:center;margin:8px 0 0;flex-wrap:wrap}
.new-topic input{flex:1;min-width:150px;border:1px solid var(--line);border-radius:5px;padding:4px 8px;font-size:13px;
 background:var(--paper);color:var(--ink)}
.new-topic small{color:var(--muted);font-size:12px}
.screens{display:grid;grid-template-columns:1fr;gap:12px;align-items:start;margin-top:6px}
.screen{border:1px solid var(--line);border-radius:10px;padding:8px 10px;background:var(--paper);min-width:0}
.screen-title{font-size:14px;font-weight:700;margin:0 0 6px}.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:12.5px}
.pv .screen .section-views{gap:5px;margin:0 0 6px}.pv .screen .section-views a{font-size:11px;padding:1px 8px}
.focus-page.pv .screen .studio-row{grid-template-columns:minmax(0,1fr) 64px;gap:8px;padding:6px 8px;margin:0 0 6px}
.focus-page.pv .screen .row-thumb img{width:64px;height:36px}
.focus-page.pv .screen .row-name{font-size:11.5px}.focus-page.pv .screen .row-address{font-size:10px}
.focus-page.pv .screen .row-stage,.focus-page.pv .screen .row-type,.pv .screen .row-piece{font-size:9.5px;padding:0 5px;margin-left:4px}
.focus-page.pv .screen .row-verbs{gap:4px;margin-top:3px}.focus-page.pv .screen .row-verb{font-size:9.5px;padding:0 5px}
.focus-page.pv .screen .focus-content .row-line,.focus-page.pv .screen .row-line{font-size:10.5px;margin:2px 0}
.pv .screen .fd-h{font-size:12px;padding:4px 10px}.pv .screen .fd-body{margin:5px 0 7px}
.pv .screen .fd-run textarea{min-height:24px;font-size:10.5px;padding:3px 8px}.pv .screen .fd-btn{font-size:10px;padding:2px 7px}
.pv .screen .fd-run .fd-bar{flex-wrap:wrap;gap:5px}
.run-row{display:flex;gap:8px;align-items:baseline;padding:5px 0;border-bottom:1px solid var(--line);font-size:11.5px}
.run-row b{font-weight:600;overflow-wrap:anywhere}.run-row .w{margin-left:auto;white-space:nowrap;color:var(--muted)}
.run-row.waits{border-left:3px solid #b35c00;padding-left:7px}.run-row.waits .w{color:#b35c00;font-weight:600}
.pop{border:1px solid var(--line);border-radius:10px;box-shadow:0 6px 18px rgba(0,0,0,.12);background:var(--paper);padding:8px 10px}
.pop-head{display:flex;justify-content:space-between;font-size:11.5px;color:var(--muted);border-bottom:1px solid var(--line);
 padding:0 0 5px;margin:0 0 6px}
.pop p{margin:3px 0;font-size:11.5px}.pop .mut{font-size:11px}
.tree{font:10.5px/1.6 ui-monospace,Menlo,monospace;margin:0;white-space:pre-wrap}
.none-box{border:1px dashed var(--line);border-radius:10px;padding:26px 12px;text-align:center;color:var(--muted);font-size:12.5px}
"""


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def diff(on) -> str:
    return " diff" if on else ""


def card_field(path: Path, key: str) -> str:
    m = re.search(rf"(?m)^{key}:\s*(.+)$", path.read_text(encoding="utf-8")) if path.is_file() else None
    return m.group(1).strip() if m else ""


def interaction_state(address: str) -> str:
    """'waiting', 'quiet' or '' for the collection Runs about one topic (their target: starts with its address); this
    Run counts as waiting, as it is once collect.py build writes its form."""
    states = []
    for card in sorted(BLOCK.rglob("runs/r*_collect_*/run.yaml")):
        if "_old" in card.parts or not card_field(card, "target").startswith(address):
            continue
        states.append("waiting" if card.parent == RUN else card_field(card, "status"))
    return "waiting" if "waiting" in states else ("quiet" if states else "")


def picture(folder: Path, up: str) -> str:
    """What studio_html shows: the lead idea slide (the slides record's first image), else the drawing's preview."""
    record = folder / f"{folder.name}.slides.json"
    try:
        first = json.loads(record.read_text(encoding="utf-8"))["slides"][0]["image"]
        if (folder / first).is_file():
            return f"{up}{folder.name}/{first}"
    except (OSError, ValueError, KeyError, IndexError, TypeError):
        pass
    return f"{up}{folder.name}/{folder.name}.png"


def piece_made_by(folder: Path, task: Path) -> str:
    """The piece of a topic's delivery a Task makes: the delivery/render.yaml entry whose by: is a Run of that Task."""
    card = folder / "delivery" / "render.yaml"
    rel = task.relative_to(BLOCK).as_posix() + "/"
    text = card.read_text(encoding="utf-8") if card.is_file() else ""
    for code, by in re.findall(r'(?m)^\s*-\s*code:\s*"([^"]*)"\s*\n\s*by:\s*(\S+)', text):
        if by.startswith(rel):
            return code.split(":")[0].strip()
    return ""


def topic(folder: Path, lead: str, name: str, up: str, task: Path | None = None) -> dict:
    """One topic as its card reads it: the face's Stage, Delivery type and Topic's first sentence, its picture, its tags
    (Slide when a deck is built, Delivery when delivery/ exists, Interaction when a form is about it)."""
    face = (folder / f"{folder.name}.md").read_text(encoding="utf-8")
    tags = re.search(r"(?mi)^\*\*Tags:\*\*[^\S\n]*([^\n]*)", face)
    tags = [v.strip().strip("`").strip() for v in re.split(r"[,·|]", tags.group(1) if tags else "") if v.strip()]
    stage = re.search(r"(?mi)^\*\*Stage:\*\*[^\S\n]*`?([A-Za-z]+)", face).group(1).lower()
    dtype = re.search(r"(?mi)^\*\*Delivery type:\*\*[^\S\n]*`?([A-Za-z]+)", face).group(1).lower()
    said = re.sub(r"\s+", " ", re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", face, re.S).group(1)).strip()
    first = re.match(r"(.+?[.;])(?:\s|$)", said)
    state = interaction_state(lead.split(":")[0] + ":")
    verbs = (["Slide"] if (folder / f"{folder.name}.slides.html").is_file() else []) + ["Draw", "Mind map", "Work"] \
        + (["Delivery"] if (folder / "delivery").is_dir() else []) + (["Interaction"] if state else [])
    return {"folder": folder.name, "id": folder.name.split("-")[0], "lead": lead, "name": name, "stage": stage,
            "type": dtype, "line": first.group(1) if first else said[:200], "img": picture(folder, up),
            "piece": piece_made_by(folder, task) if task else "", "verbs": verbs, "waits": state == "waiting",
            "tags": tags}


def group_buttons(shown: list) -> list:
    """The Studio's view buttons: one per group the shown topics' Tags name, in the Block's _studio_groups.txt order,
    Other last when a topic has none, Topics when none has a group."""
    order = [ln.strip() for ln in (BLOCK / "_studio_groups.txt").read_text(encoding="utf-8").splitlines()
             if ln.strip() and not ln.startswith("#")]
    named = {g for t in shown for g in t["tags"]}
    out = [g for g in order if g in named] + sorted(named - set(order))
    out += ["Other"] if out and any(not t["tags"] for t in shown) else []
    return out or ["Topics"]


def caption(group: str) -> str:
    return ("What this Task makes, then its own topics." if group == "Topics"
            else f"Topics tagged {group}: what this Task makes, then its own.")


OWN = [topic(TASK / f, f"b17.j03.t03-{f[:3]}:theme_work.work_workbench_pages.task_page @ ", n, UP_TASK)
       for f, n in (("s57-task-ui-report", "task_ui_report"), ("s58-task-ui-work", "task_ui_work"),
                    ("s59-task-ui-studio", "task_ui_studio"))]
OWN = sorted(OWN, key=lambda t: not t["waits"])              # a card whose form waits on you comes first (stable)
S59 = next(t for t in OWN if t["id"] == "s59")
S01 = topic(BLOCK / "s01-work-ladder", "b17-s01:theme_work @ ", "work_ladder", UP_BLOCK, T01)
S02 = topic(BLOCK / "s02-work-skills", "b17-s02:theme_work @ ", "work_skills", UP_BLOCK)
S04 = topic(BLOCK / "s04-workbench-page-structure", "b17-s04:theme_work @ ", "workbench_page_structure", UP_BLOCK, TASK)

WHERE = {"t03": "Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work / j03_work_workbench_pages / t03_task_page",
         "t01": "Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work / j01_work_ladder_contract / t01_skill_section",
         "b35": "Tools-SPACE / blueprints / Project-PageParts / work / b35_studio / j01_studio_delivery_type / "
                "t02_new_topic_for_line"}
RAIL = ["Report", "Work", "Studio", "Interactions", "Delivery", "Files"]          # b17's Task pages, Studio proposed
RAIL_B35 = ["Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Files"]


def prompt_talk(task: Path, ids: list) -> str:
    rel = task.relative_to(TOOLS).as_posix()
    return (f"/haipipe-studio {rel} {' '.join(ids)}: talk with me about {task.name}'s aim and sketch it on the topic's "
            "drawing; write no text yet; what we settle goes into the topic's Decided.")


def prompt_start(task: Path) -> str:
    return (f"/haipipe-studio {task.relative_to(TOOLS).as_posix()}: start a new topic here with new_topic.py (a Task holds "
            "three at most), then talk with me and sketch it.")


def rail(names: list, on: str = "Studio", gone: tuple = (), mark: tuple = ()) -> str:
    spans = "".join(f'<span class="rl{" on" if n == on else ""}{" gone" if n in gone else ""}{diff(n in mark)}">'
                    f'{esc(n)}</span>' for n in names)
    return f'<div class="rail-line"><span class="rl-word">Right rail</span>{spans}</div>'


def views(names: list, on: str, *, mark: bool = False, studio: bool = True) -> str:
    links = "".join('<a href="#"' + (' aria-current="page"' if n == on else "") + f">{esc(n)}</a>" for n in names)
    return f'<nav class="section-views{" studio-groups" if studio else ""}{diff(mark)}" aria-label="Views">{links}</nav>'


def page(title: str, where: str, task: str, section: str, body: str, *, top: str = "", bar: str = "",
         caption: str = "", head: bool = True) -> str:
    """One preview page: the path (and the right rail as a line), the title-&-section, its view buttons, the content;
    head=False leaves out the title when the screens side by side carry it."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    h1 = f'<h1>{esc(task)}<span class="h1-section">{esc(section)}</span></h1>' if head else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{CSS}</style></head><body><main class=\"focus-page pv\">"
            f'<div class="focus-crumb">{esc(where)}</div>{top}{h1}{bar}'
            f'<section class="focus-card"><div class="focus-content">{cap}{body}</div></section></main></body></html>')


def screen(name: str, section: str, inner: str, *, bar: str = "", mark: bool = False) -> str:
    """One place of the page drawn small, so two sit side by side."""
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">{esc(name)}<span>{esc(section)}</span></div>'
            f'{bar}<div class="focus-content">{inner}</div></section>')


def card(t: dict, *, made: bool = False, mark: bool = False, work: str = "plain", line: bool = True,
         tagged: bool = True) -> str:
    """One topic as studio_html draws it: address and name, stage, delivery type (This Task makes: the piece it
    makes), its one line, its tags, its picture. work: 'plain', 'mark' (the Work tag boxed) or 'none' (no Work tag,
    the tags boxed); line and tagged False leave out what no option of a question changes."""
    tags = []
    for v in t["verbs"]:
        if v == "Work" and work == "none":
            continue
        cls = "row-verb" + (" main" if v == "Slide" else "") + diff(v == "Work" and work == "mark")
        if v == "Interaction" and t["waits"]:
            tags.append(f'<a class="{cls}"{WAIT_STYLE} href="#">🙋 Interaction</a>')
        else:
            tags.append(f'<a class="{cls}" href="#">{esc(v)}</a>')
    pill = f'<span class="row-piece">piece: {esc(t["piece"])}</span>' if made and t["piece"] else ""
    said = f'<p class="row-line"><a href="#">{esc(t["line"])}</a></p>' if line else ""
    return (f'<article class="status-row studio-row{diff(mark)}" id="{esc(t["folder"])}"><div><p class="row-title">'
            f'<span class="row-address">{esc(t["lead"])}</span><a class="row-name" href="#">{esc(t["name"])}</a>'
            f'<span class="row-stage">{esc(t["stage"])}</span><span class="row-type">{esc(t["type"])}</span>{pill}</p>'
            + said + (f'<p class="row-verbs{diff(work == "none")}">{"".join(tags)}</p>' if tagged else "") + '</div>'
            f'<a class="row-thumb" href="#"><img src="{esc(t["img"])}" alt="{esc(t["folder"])}"></a></article>')


def sec(title: str, inner: str, mark: bool = False) -> str:
    """One section of a view: its heading bar (folds, open by default), its content unboxed below (focus_draft)."""
    return (f'<section class="fd-sec{diff(mark)}"><h3 class="fd-h" data-fold="1" aria-expanded="true">{esc(title)}</h3>'
            f'<div class="fd-body">{inner}</div></section>')


def ask(buttons: list, *, mark: bool = False, extra: str = "") -> str:
    """Ask the agent: one notes box, then a button per prompt (the prompt shows on hover), as the draft page's."""
    bs = "".join(f'<button type="button" class="fd-btn fd-copy{diff(m)}" title="{esc(p)}">{esc(b)}</button>'
                 for b, p, m in buttons)
    return sec("Ask the agent", '<div class="fd-run"><textarea rows="1" placeholder="your notes, copied with the prompt">'
               f'</textarea><div class="fd-bar">{bs}</div></div>{extra}', mark)


def runs(task: Path) -> list:
    """(name, kind, type, status) of a Task's Runs, from their run.yaml; this Run is waiting once built."""
    out = []
    for folder in sorted((task / "runs").iterdir()):
        card_ = folder / "run.yaml"
        if card_.is_file():
            status = "waiting" if folder == RUN else card_field(card_, "status")
            out.append((folder.name, card_field(card_, "kind"), card_field(card_, "type"), status))
    return out


def work_screen(extra: list = (), mark: bool = False) -> str:
    """Work drawn small: its Runs, a waiting form first, then its own Ask the agent (s58 owns this screen)."""
    rows = sorted(runs(TASK), key=lambda r: r[3] != "waiting")
    lines = "".join(f'<div class="run-row{" waits" if s == "waiting" else ""}"><b>{esc(n)}</b>'
                    f'<span class="w">{"🙋 " if s == "waiting" else ""}{esc(s)}</span></div>' for n, k, ty, s in rows)
    buttons = [("Copy prompt", "the Work prompt (s58)", False)] + list(extra)
    return screen("t03_task_page", "Work", lines + ask(buttons, mark=mark),
                  bar=views(["Progress"], "Progress", studio=False))     # today's name; s58 owns any rename


def previews() -> dict:
    out = {}
    talk01, start01 = prompt_talk(T01, ["s01"]), prompt_start(T01)
    t01_page = dict(where=WHERE["t01"], task="t01_skill_section", section="Studio", top=rail(RAIL))
    skill = group_buttons([S01])                                  # s01's Tags: Skill

    # Q1 · does a Task's Studio show the Block topic it makes? t01_skill_section holds no sNN and makes s01's piece
    out["q1-a"] = page("Q1 A", body=sec(MAKES, card(S01, made=True), mark=True)
                       + ask([(TALK, talk01, 0), (START, start01, 0)]),
                       bar=views(skill, skill[0]), caption=caption(skill[0]), **t01_page)
    line = (f'<p class="made-line"><b>{esc(S01["piece"])}</b> of <span class="row-address">{esc(S01["lead"])}</span>'
            f'<a class="row-name" href="#">{esc(S01["name"])}</a> <a class="row-verb" href="#">Open ↗</a></p>')
    out["q1-b"] = page("Q1 B", body=sec(MAKES, line, mark=True) + ask([(TALK, talk01, 0), (START, start01, 0)]),
                       bar=views(["Topics"], "Topics"), caption=caption("Topics"), **t01_page)
    out["q1-c"] = page("Q1 C", body='<p class="empty-line diff">No topic sits at t01_skill_section yet.</p>'
                       + ask([(START, start01, 0)]), bar=views(["Topics"], "Topics"), caption="Its own topics.",
                       **t01_page)

    # Q2 · a Task that holds no topic and makes none: Studio stays on the rail with one line, or leaves it as today
    start35 = prompt_start(B35_T02)
    run35 = runs(B35_T02)[0]
    out["q2-a"] = page("Q2 A", where=WHERE["b35"], task="t02_new_topic_for_line", section="Studio",
                       top=rail(RAIL_B35, mark=("Studio",)), bar=views(["Topics"], "Topics"), caption=caption("Topics"),
                       body='<div class="diff"><p class="empty-line">No topic sits at t02_new_topic_for_line yet.</p>'
                       + ask([(START, start35, 0)]) + "</div>")
    out["q2-b"] = page("Q2 B", where=WHERE["b35"], task="t02_new_topic_for_line", section="Work",
                       top=rail(RAIL_B35, on="Work", gone=("Studio",), mark=("Studio",)),
                       bar=views(["Progress"], "Progress", studio=False), caption="Its parts.",
                       body=f'<article class="status-row"><span class="row-name">{esc(run35[0])}</span>'
                       f'<p class="row-meta">{esc(run35[3])}</p></article>'
                       '<p class="empty-line diff">No Studio on the rail: section=studio opens Work.</p>')

    # Q3 · s59's open question: start an sNN here with one click, or by the prompt (t01_skill_section, my other picks)
    made01 = sec(MAKES, card(S01, made=True))
    out["q3-a"] = page("Q3 A", body=made01 + ask([(TALK, talk01, 0), (START, start01, 1)]),
                       bar=views(skill, skill[0]), caption=caption(skill[0]), **t01_page)
    new = ('<div class="new-topic diff"><input type="text" placeholder="a title for the new topic" aria-label="title">'
           f'<button type="button" class="fd-btn">{NEW}</button>'
           '<small>writes sNN-&lt;slug&gt;/ in t01_skill_section</small></div>')
    out["q3-b"] = page("Q3 B", body=made01 + ask([(TALK, talk01, 0)], extra=new),
                       bar=views(skill, skill[0]), caption=caption(skill[0]), **t01_page)

    # Q4 · where Ask the agent sits: t03_task_page's Task UI view and its Work side by side (C moves both prompts)
    groups = group_buttons([S04] + OWN)                           # s04: Interface · Navigation; s57 to s59: Task UI
    talk03, start03 = prompt_talk(TASK, sorted(t["id"] for t in OWN)), prompt_start(TASK)
    cards = sec(OWNS, "".join(card(t, line=False, tagged=False) for t in OWN))   # no Q4 option changes a card
    studio_bar = views(groups, "Task UI")
    t03 = dict(where=WHERE["t03"], task="t03_task_page", section="Studio", head=False)   # each screen names the page
    asked = ask([(TALK, talk03, 0), (START, start03, 0)], mark=True)
    a_studio = screen("t03_task_page", "Studio", cards + asked, bar=studio_bar)
    b_studio = screen("t03_task_page", "Studio", asked + cards, bar=studio_bar)
    c_studio = screen("t03_task_page", "Studio", cards, bar=studio_bar)
    out["q4-a"] = page("Q4 A", body=f'<div class="screens">{a_studio}{work_screen()}</div>', **t03)
    out["q4-b"] = page("Q4 B", body=f'<div class="screens">{b_studio}{work_screen()}</div>', **t03)
    out["q4-c"] = page("Q4 C", body='<div class="screens">' + c_studio
                       + work_screen([(TALK, talk03, True), (START, start03, True)]) + "</div>", **t03)

    # Q5 · what a card's Work tag opens on a Task page: s59's card, and the pop-out beside it
    design = TASK / "runs" / "run-design-task-page" / "run.yaml"
    writes = re.findall(r"(?m)^-\s*\S*/(s\d+)-[^/]+/delivery/(\S+)", design.read_text(encoding="utf-8"))
    head = '<div class="pop-head"><span>s59-task-ui-studio · work</span><span>Close</span></div>'
    one_run = (f'<div class="pop diff">{head}<div class="run-row"><b>run-design-task-page</b>'
               f'<span class="w">{esc(card_field(design, "status"))}</span></div>'
               f'<p>{esc(card_field(design, "kind"))} · {esc(card_field(design, "type"))} · '
               f'target: {esc(card_field(design, "target"))}</p>'
               f'<p class="mut">writes {esc(" · ".join(s for s, _ in writes))} delivery/{esc(writes[0][1] if writes else "")}'
               '</p></div>')
    job = TASK.parent
    tree = [f"{job.name.split('_')[0]} · {card_field(job / (job.name + '.md'), 'goal')[:58]}…"]
    for task in sorted(p for p in job.iterdir() if p.is_dir() and re.match(r"t\d\d_", p.name)):
        tree.append(task.name)
        tree += [f"  {n} · {s}" for n, k, ty, s in runs(task)]
    whole = f'<div class="pop diff">{head}<pre class="tree">{esc(chr(10).join(tree))}</pre></div>'
    left = lambda work: screen("t03_task_page", "Studio", sec(OWNS, card(S59, work=work)), bar=studio_bar)
    out["q5-a"] = page("Q5 A", body=f'<div class="screens">{left("mark")}{one_run}</div>', **t03)
    out["q5-b"] = page("Q5 B", body=f'<div class="screens">{left("mark")}{whole}</div>', **t03)
    out["q5-c"] = page("Q5 C", body=f'<div class="screens">{left("none")}<div class="none-box diff">No Work tag on a '
                       'Task page: its Runs are one rail click away, in Work.</div></div>', **t03)
    return out


def draft_css() -> str:
    """The draft page's CSS string (focus_draft.CSS): the view's section headings and the Ask the agent box."""
    m = re.search(r'(?ms)^CSS = """<style>(.*?)</style>"""', DRAFT_PY.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


CSS = FOCUS_CSS.read_text(encoding="utf-8") + draft_css() + PREVIEW_CSS


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/")


if __name__ == "__main__":
    main()
