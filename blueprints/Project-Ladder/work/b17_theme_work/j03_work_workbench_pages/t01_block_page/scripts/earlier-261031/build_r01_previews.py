"""r01's option previews (JL 261031, on the r01 form: "I think you should show that what is the expected UI / html
looks like"): one small page per option, drawn in the workbench's own look (its focus.css) with b17's real names and
each topic's real first slide; the part an option changes carries class="diff", which the form boxes in orange.

The form shows a preview at half size in a frame 600 pixels tall, so what differs sits in that height: no Purpose (no
option changes it), compact delivery cards, and two places side by side when an option moves something between them.

Writes runs/r01_collect_report_and_delivery/option-q<N>-<k>.html; question_collection.md links each one under its
option. Rerun after changing anything here, never edit the pages:

    python build_r01_previews.py
"""
from __future__ import annotations

import html
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]                       # t01_block_page
RUN = TASK / "runs" / "r01_collect_report_and_delivery"
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
UP = "../../../../"                                              # from the Run folder up to b17_theme_work

CAPTIONS = {"MindMap": "How it is built, as a map: its parts, and what each must find out.",
            "All": "Everything this Block hands over, one row per delivery.",
            "Skill": "The skill pieces this Block hands over.",
            "Status": "Where its sNN, its Jobs and its Tasks stand.",
            "Progress": "Its parts.",
            "Answers": "What it has found, one answer per thing it must find out.",
            "Findings": "What it has found so far, in the answers' own words.",
            "Questions": "What it must find out."}

# b17's three deliveries (board.md ## Deliveries; each topic's delivery/render.yaml names its pieces)
DELIVERIES = [
    {"id": "s01", "name": "Work ladder", "type": "skill", "topic": "s01-work-ladder", "job": "j01_work_ladder_contract",
     "stage": "⬜ explore", "deck": "slides/idea-01-rungs-one-shape.png",
     "pieces": ["deck/", "ladder-section", "work-scaffold", "demo-block"],
     "goes": "haipipe-work SKILL.md › The work ladder",
     "thing": ('<div class="doc"><div class="doc-file">haipipe-work · SKILL.md</div><h4>The work ladder</h4>'
               '<p>A work Block holds Jobs, a Job holds Tasks, a Task holds Runs.</p><pre>'
               'work/bNN_&lt;block&gt;/        board.md · Questions · sNN\n'
               '└─ jNN_&lt;job&gt;/          goal · close · its Tasks\n'
               '   └─ tNN_&lt;task&gt;/      face · scripts/ · runs/\n'
               '      └─ rNN_&lt;run&gt;/    ticket · run.yaml · result/</pre></div>')},
    {"id": "s02", "name": "Skill homes", "type": "skill", "topic": "s02-work-skills", "job": "j02_work_skill_homes",
     "stage": "⬜ explore", "deck": "slides/idea-01-which-skills-move.png",
     "pieces": ["deck/", "skill-homes-table", "move-list"],
     "goes": "haipipe-work SKILL.md › Skills of the work theme; the move list to b04",
     "thing": ('<div class="doc"><div class="doc-file">haipipe-work · SKILL.md</div><h4>Skills of the work theme</h4>'
               '<table><tr><th>skill folder</th><th>home, proposed</th></tr>'
               '<tr><td>haipipe-task</td><td>1_base/task (Q04)</td></tr><tr><td>8_stata</td><td>2_theme/work</td></tr>'
               '<tr><td>9_agent</td><td>2_theme/work</td></tr><tr><td>1_data</td><td>1_base/task</td></tr></table></div>')},
    {"id": "s04", "name": "Work pages", "type": "ui", "topic": "s04-workbench-page-structure",
     "job": "j03_work_workbench_pages", "stage": "⏳ shaping", "deck": "slides/idea-01-what-is-a-block.png",
     "pieces": ["deck/", "block-page", "job-task-pages", "element-picks"],
     "goes": "servers/workbench/focus_page.py, built by design_b02_workbench",
     "thing": ('<div class="mini"><div class="mini-crumb">… / work / b17_theme_work</div>'
               '<div class="mini-h1">b17_theme_work<span>Report</span></div>'
               '<div class="mini-views"><i class="on">MindMap</i><i>All</i><i>s01</i><i>s02</i><i>s04</i></div>'
               '<div class="mini-map"><b>To find out</b><div><span></span><span></span><span></span></div>'
               '<b>Interface</b><div><span></span><span></span></div></div></div>')},
]
S01 = DELIVERIES[0]
PER_DELIVERY = [f'{d["id"]} {d["name"]}' for d in DELIVERIES]
REPORT_ALL = ["MindMap", "All"] + PER_DELIVERY          # the Report's buttons under my picks (Q2 A, Q5 A, Q6 A)
TODAY = ["MindMap", "Status", "Findings", "Answers", "Questions"]

# b17's Questions as the MindMap draws them today (reports/q01..q04)
QUESTIONS = [("proposed", "How does work climb the ladder?", "The work Theme climbs the shared ladder unchanged."),
             ("no answer yet", "Where do Plan, Build, Execute and Report show?", ""),
             ("no answer yet", "How does a Question read its Runs?", ""),
             ("proposed", "Which skills make the work theme?",
              "The work theme takes the skills only work uses, and base keeps what several themes call.")]

PREVIEW_CSS = """
/* preview only: the page without its fixed rails; the right rail is drawn as one line under the path */
.focus-page.pv{max-width:900px;padding:16px 24px 30px}.pv h1{margin:6px 0 10px}
.rail-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0 0;font-size:12.5px}
.rail-line .rl-word{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.rail-line span.rl{padding:1px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted)}
.rail-line span.rl.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.rail-line span.rl.gone{text-decoration:line-through;border-style:dashed;opacity:.6}
.pv .section-views{flex-wrap:wrap;gap:6px}
.pv .section-views span{font-size:13px;border:1px solid var(--line);border-radius:6px;padding:3px 11px;color:var(--muted)}
.pv .section-views span.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .view-caption{margin:0 0 10px}
.screens{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start;margin-top:12px}
.screen{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--paper);min-width:0}
.screen-title{font-size:15px;font-weight:700;margin:0 0 6px}.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:13px}
.screen .section-views{gap:5px;margin:0 0 6px}.screen .section-views span{font-size:11px;padding:1px 7px}
.screen .view-caption{font-size:11.5px;margin:0 0 8px}
.screen.gone{display:flex;align-items:center;justify-content:center;min-height:220px;color:var(--muted);border-style:dashed;text-align:center}
.dv{border:1px solid var(--line);border-radius:10px;padding:9px 11px;margin:0 0 9px;background:var(--paper)}
.dv-head{display:flex;align-items:baseline;gap:8px;margin:0 0 6px}.dv-head b{font-size:14px}
.dv-type{font-size:11px;padding:0 8px;border-radius:9px;background:var(--soft);color:var(--accent)}
.dv-word{margin-left:auto;font-size:11.5px;border:1px dashed var(--muted);border-radius:9px;padding:0 8px;color:var(--muted)}
.dv-mini{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:start}
.dv-mini img{display:block;width:100%;border:1px solid var(--line);border-radius:5px}
.dv-mini .doc,.dv-mini .mini{zoom:.62}
.dv-goes{font-size:11.5px;color:var(--muted);margin:6px 0 0}.dv-goes code{font-size:10.5px}
.dv-one>*{margin:0 0 12px}.dv-one .doc{max-width:470px}
.dv-part{margin:0}.dv-part figcaption{font-size:11px;color:var(--muted);margin:0 0 3px}
.dv-part img{display:block;width:100%;max-width:330px;border:1px solid var(--line);border-radius:6px}
.dv-line{display:flex;gap:10px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.dv-line .mut{margin-left:auto}
.empty{padding:28px 16px;text-align:center;color:var(--muted);border:1px dashed var(--line);border-radius:10px}
.doc{border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-size:12px;background:var(--bg)}
.doc-file{font:11px ui-monospace,Menlo,monospace;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:4px;margin-bottom:6px}
.doc h4{margin:0 0 4px;font-size:13px}.doc p{margin:0 0 4px}
.doc pre{font:10.5px/1.5 ui-monospace,Menlo,monospace;margin:4px 0 0;white-space:pre;overflow:hidden}
.doc table{font-size:11.5px;border-collapse:collapse;width:100%}
.doc td,.doc th{padding:2px 6px;border-bottom:1px solid var(--line);text-align:left;font-weight:400}.doc th{color:var(--muted)}
.mini{border:1px solid var(--line);border-radius:6px;padding:8px 10px;background:var(--bg);font-size:11px}
.mini-crumb{color:var(--muted);font-size:10px}.mini-h1{font-size:14px;font-weight:700}
.mini-h1 span{font-weight:400;color:var(--muted);margin-left:6px;font-size:12px}
.mini-views{display:flex;gap:4px;margin:6px 0 8px}.mini-views i{font-style:normal;border:1px solid var(--line);border-radius:4px;padding:0 5px;font-size:10px}
.mini-views i.on{border-color:var(--accent);color:var(--accent)}
.mini-map{display:grid;grid-template-columns:76px 1fr;gap:6px 16px;align-items:center}
.mini-map b{border:1px solid var(--ink);border-radius:5px;padding:2px 4px;font-size:10px;text-align:center}
.mini-map span{display:block;height:7px;border-radius:3px;background:var(--wash);margin:4px 0}
.files{font-size:12px;border-collapse:collapse;width:100%}.files td{padding:6px 4px;border-bottom:1px solid var(--line);vertical-align:top}
.map{display:grid;grid-template-columns:96px 1fr;gap:10px 16px;align-items:start}
.map>b{border:1.5px solid var(--ink);border-radius:7px;padding:4px 6px;font-size:12px;text-align:center;margin-top:2px}
.map ul{list-style:none;padding:0!important;margin:0}.map li{margin:0 0 7px;font-size:12px}
.pill{font-size:10.5px;border-radius:9px;padding:0 7px;margin-right:6px;background:var(--soft);color:var(--accent)}
.pill.grey{background:var(--wash);color:var(--muted)}
.map li p{margin:3px 0 0 4px;padding:4px 8px;background:var(--wash);border-radius:6px;font-size:11.5px}
.row{padding:7px 0;border-bottom:1px solid var(--line);font-size:12.5px}.row small{display:block;color:var(--muted);font-size:11px}
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def diff(on: bool) -> str:
    return " diff" if on else ""


def rail(delivery: str = "") -> str:
    """The right rail as one line. delivery: "" (no Delivery item), "there" or "gone"; either is the boxed part."""
    names = ["Report", "Work", "Studio", "Interactions"] + (["Delivery"] if delivery else []) + ["Files"]
    spans = []
    for name in names:
        cls = "rl" + (" on" if name == "Report" else "")
        if name == "Delivery":
            cls += (" gone" if delivery == "gone" else "") + " diff"
        spans.append(f'<span class="{cls}">{esc(name)}</span>')
    return f'<div class="rail-line"><span class="rl-word">Right rail</span>{"".join(spans)}</div>'


def views(names: list, on: str, mark: bool = False) -> str:
    buttons = "".join(f'<span class="{"on" if n == on else ""}">{esc(n)}</span>' for n in names)
    return f'<nav class="section-views{diff(mark)}" aria-label="Views">{buttons}</nav>'


def page(title: str, body: str, *, delivery: str = "", bar: str = "", caption: str = "", heading: bool = True) -> str:
    """One preview page: the path and the right rail, then (heading) the title, its view buttons and the caption."""
    top = (f'<h1>b17_theme_work<span class="h1-section">Report</span></h1>{bar}'
           f'<p class="view-caption">{esc(caption)}</p>') if heading else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            "<body><main class=\"focus-page pv\">"
            "<div class=\"focus-crumb\">Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work</div>"
            f"{rail(delivery)}{top}{body}</main></body></html>")


def screen(section: str, inner: str, *, bar: str = "", caption: str = "", mark: bool = False) -> str:
    """One place of the page drawn small (Report, Delivery, Work), so two can sit side by side."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">b17_theme_work<span>{esc(section)}</span>'
            f'</div>{bar}{cap}{inner}</section>')


def head(d: dict, word: str = "planned", mark_word: bool = False) -> str:
    said = f'<span class="dv-word{diff(mark_word)}">{esc(word)}</span>' if word else ""
    return (f'<header class="dv-head"><b>{esc(d["id"])} · {esc(d["name"])}</b>'
            f'<span class="dv-type">{esc(d["type"])}</span>{said}</header>')


def goes(d: dict) -> str:
    return f'<p class="dv-goes">{" · ".join(esc(p) for p in d["pieces"])} → <code>{esc(d["goes"])}</code> · not sent</p>'


def deck_img(d: dict) -> str:
    return f'<img src="{UP}{d["topic"]}/{d["deck"]}" alt="{esc(d["id"])} deck, first slide">'


def card(d: dict, word: str = "planned", mark_word: bool = False) -> str:
    """One delivery, compact: its name, the thing small, its deck's first slide, the one line of its files."""
    return (f'<article class="dv">{head(d, word, mark_word)}<div class="dv-mini">{d["thing"]}{deck_img(d)}</div>'
            f'{goes(d)}</article>')


def cards(chosen=None, *, mark: bool = False, word: str = "planned", mark_word: bool = False) -> str:
    chosen = DELIVERIES if chosen is None else chosen
    return f'<div class="dv-list{diff(mark)}">' + "".join(card(d, word, mark_word) for d in chosen) + "</div>"


def thing(d: dict, mark: bool = False) -> str:
    return f'<figure class="dv-part{diff(mark)}"><figcaption>the thing</figcaption>{d["thing"]}</figure>'


def deck(d: dict, mark: bool = False) -> str:
    return f'<figure class="dv-part{diff(mark)}"><figcaption>its deck, first slide</figcaption>{deck_img(d)}</figure>'


def mindmap(mark: bool = False) -> str:
    items = "".join(f'<li><span class="pill{"" if state == "proposed" else " grey"}">{esc(state)}</span>{esc(ask)}'
                    + (f"<p>{esc(answer)}</p>" if answer else "") + "</li>" for state, ask, answer in QUESTIONS)
    return (f'<div class="map{diff(mark)}"><b>To find out</b><ul>{items}</ul>'
            '<b>Interface</b><ul><li><span class="pill">s04-workbench-page-structure</span>Workbench page structure</li>'
            '</ul></div>')


def rows(kind: str) -> str:
    if kind == "jobs":
        return "".join(f'<div class="row">{esc(d["job"])}<small>build what b17-{esc(d["id"])} hands over</small></div>'
                       for d in DELIVERIES)
    if kind == "status":
        return "".join(f'<div class="row">{esc(d["stage"])} b17-{esc(d["id"])} {esc(d["name"])}<small>'
                       f'{esc(d["job"])} · its Tasks open</small></div>' for d in DELIVERIES)
    if kind == "answers":
        return "".join(f'<div class="row">Q0{i} · {esc(ask)}<small>{esc(answer or "no answer yet")}</small></div>'
                       for i, (_, ask, answer) in enumerate(QUESTIONS, 1))
    return "".join(f'<div class="row">Q0{i} · {esc(ask)}</div>' for i, (_, ask, _a) in enumerate(QUESTIONS, 1))


def previews() -> dict:
    out = {}
    # Q1 · where a delivery shows: the Report and the right rail's Delivery, side by side
    report_all = dict(bar=views(REPORT_ALL, "All"), caption=CAPTIONS["All"])
    files = "".join(f'<tr><td><b>{esc(d["id"])}</b> {esc(d["name"])}</td><td>{"<br>".join(esc(p) for p in d["pieces"])}'
                    '</td><td>☐ sent</td></tr>' for d in DELIVERIES)
    out["q1-a"] = page("Q1 A", heading=False, delivery="gone", body='<div class="screens">'
                       + screen("Report", cards(mark=True), **report_all)
                       + '<section class="screen gone diff">No Delivery in the right rail:<br>Report › All shows each '
                         'delivery.</section></div>')
    out["q1-b"] = page("Q1 B", heading=False, delivery="there", body='<div class="screens">'
                       + screen("Report", cards(mark=True), **report_all)
                       + screen("Delivery", f'<table class="files">{files}</table>', mark=True,
                                caption="Its files, and whether each was sent.") + "</div>")
    out["q1-c"] = page("Q1 C", heading=False, delivery="there", body='<div class="screens">'
                       + screen("Report", mindmap(mark=True), bar=views(TODAY, "MindMap"), caption=CAPTIONS["MindMap"])
                       + screen("Delivery", cards(), mark=True, caption=CAPTIONS["All"]) + "</div>")
    # Q2 · the buttons after MindMap, each with the view it opens
    out["q2-a"] = page("Q2 A", cards(), bar=views(REPORT_ALL, "All", mark=True), caption=CAPTIONS["All"])
    out["q2-b"] = page("Q2 B", f'<div class="dv-one">{head(S01)}{thing(S01)}{deck(S01)}{goes(S01)}</div>',
                       bar=views(["MindMap"] + PER_DELIVERY, PER_DELIVERY[0], mark=True),
                       caption=f"What s01 hands over: {S01['goes']}.")
    out["q2-c"] = page("Q2 C", cards([d for d in DELIVERIES if d["type"] == "skill"]),
                       bar=views(["MindMap", "Skill", "UI"], "Skill", mark=True), caption=CAPTIONS["Skill"])
    # Q3 · the order inside one delivery's view; the deck is the part that moves
    one = dict(bar=views(REPORT_ALL, PER_DELIVERY[0]), caption=f"What s01 hands over: {S01['goes']}.")
    out["q3-a"] = page("Q3 A", f'<div class="dv-one">{head(S01)}{thing(S01)}{deck(S01, mark=True)}{goes(S01)}</div>',
                       **one)
    out["q3-b"] = page("Q3 B", f'<div class="dv-one">{head(S01)}{deck(S01, mark=True)}{thing(S01)}{goes(S01)}</div>',
                       **one)
    out["q3-c"] = page("Q3 C", f'<div class="dv-one">{head(S01)}{thing(S01)}{goes(S01)}'
                               '<p class="dv-goes diff">its deck: Studio › s01-work-ladder</p></div>', **one)
    # Q4 · before a delivery is made (none of b17's is)
    lines = "".join(f'<div class="dv-line"><b>{esc(d["id"])} · {esc(d["name"])}</b><span class="dv-type">'
                    f'{esc(d["type"])}</span><span class="mut">not made yet · {esc(d["job"])}</span></div>'
                    for d in DELIVERIES)
    out["q4-a"] = page("Q4 A", cards(mark=True), **report_all)
    out["q4-b"] = page("Q4 B", f'<div class="diff">{lines}</div>', **report_all)
    out["q4-c"] = page("Q4 C", '<div class="empty diff">Nothing yet: a delivery shows here once it is made.</div>',
                       **report_all)
    # Q5 · where Questions and their answers show; the MindMap shows them in every option
    out["q5-a"] = page("Q5 A", mindmap(), bar=views(REPORT_ALL, "MindMap", mark=True), caption=CAPTIONS["MindMap"])
    out["q5-b"] = page("Q5 B", '<div class="screens">' + screen("Report", mindmap(), caption="MindMap")
                       + screen("Report", rows("answers"), mark=True, caption="Answers: " + CAPTIONS["Answers"])
                       + "</div>", bar=views(REPORT_ALL + ["Answers"], "MindMap", mark=True), caption=CAPTIONS["MindMap"])
    out["q5-c"] = page("Q5 C", '<div class="screens">' + screen("Report", mindmap(), caption="MindMap")
                       + '<div class="diff">'
                       + "".join(screen("Report", rows("answers" if v != "Questions" else "questions"),
                                        caption=f"{v}: {CAPTIONS[v]}") for v in ("Findings", "Answers", "Questions"))
                       + "</div></div>", bar=views(REPORT_ALL + ["Findings", "Answers", "Questions"], "MindMap", mark=True),
                       caption=CAPTIONS["MindMap"])
    # Q6 · where Status goes: one word on each delivery, a second Work view, or a Report view
    out["q6-a"] = page("Q6 A", '<div class="screens">' + screen("Report", cards(mark_word=True), **report_all)
                       + screen("Work", rows("jobs"), bar=views(["Progress"], "Progress"), caption=CAPTIONS["Progress"])
                       + "</div>", heading=False)
    out["q6-b"] = page("Q6 B", '<div class="screens">' + screen("Report", cards(word=""), **report_all)
                       + screen("Work", rows("status"), bar=views(["Progress", "Status"], "Status", mark=True),
                                caption=CAPTIONS["Status"], mark=True) + "</div>", heading=False)
    out["q6-c"] = page("Q6 C", '<div class="screens">'
                       + screen("Report", cards(word=""), bar=views(REPORT_ALL + ["Status"], "All", mark=True),
                                caption=CAPTIONS["All"])
                       + screen("Report", rows("status"), bar=views(REPORT_ALL + ["Status"], "Status"),
                                caption=CAPTIONS["Status"], mark=True) + "</div>", heading=False)
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/")


if __name__ == "__main__":
    main()
