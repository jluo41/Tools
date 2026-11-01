"""r04's option previews: the work Block's Studio section (b17.j03.t01-s53 @ block_ui_studio), one small page per
option, drawn in the workbench's own look (its focus.css, the real Studio card classes) with b17's real topics: each
card's label, stage, line, Covers and first Open item are read from its face, its picture from its lead slide or its
drawing's preview, as focus_page.studio_html does. The part an option changes carries class="diff", which the form
boxes in orange (haipipe-interaction: "The difference sits in the frame").

The form shows a preview at half size in a frame 600 page pixels tall, about 750 wide: so no Purpose (no option
changes it), compact cards, and for the view list each view drawn as its own small panel.

Two states are the preview's own, not read from disk: the group lists of Q1's three options (each option IS a list),
and in Q4 the nine cells' forms waiting, as JL will find them (each of j03's nine cells asks him one form).

Writes runs/r04_collect_block_studio_views/option-q<N>-<k>.html; question_collection.md links each one under its
option. Rerun after changing anything here, never edit the pages:

    /Users/jluo41/Desktop/Physician-SPACE/.venv/bin/python build_r04_previews.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]                       # t01_block_page
JOB = TASK.parent                                                # j03_work_workbench_pages
BLOCK = JOB.parent                                               # b17_theme_work
RUN = TASK / "runs" / "r04_collect_block_studio_views"
TOOLS = next(p for p in TASK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
UP = "../../../../"                                              # from the Run folder up to b17_theme_work

# b17's twelve sNN, in the order frame.studio_inventory reads them: the Block's own, then each Task's
TOPIC_DIRS = ["s01-work-ladder", "s02-work-skills", "s04-workbench-page-structure",
              "j03_work_workbench_pages/t01_block_page/s51-block-ui-report",
              "j03_work_workbench_pages/t01_block_page/s52-block-ui-work",
              "j03_work_workbench_pages/t01_block_page/s53-block-ui-studio",
              "j03_work_workbench_pages/t02_job_page/s54-job-ui-report",
              "j03_work_workbench_pages/t02_job_page/s55-job-ui-work",
              "j03_work_workbench_pages/t02_job_page/s56-job-ui-studio",
              "j03_work_workbench_pages/t03_task_page/s57-task-ui-report",
              "j03_work_workbench_pages/t03_task_page/s58-task-ui-work",
              "j03_work_workbench_pages/t03_task_page/s59-task-ui-studio"]
WAITING = {f"s{n}" for n in range(51, 60)}                       # Q4: the nine cells' forms, as JL will find them

# Q1's three view lists: each option names its groups, and each group the topics it holds
SKILL, UI_ALL = ["s01", "s02"], ["s04"] + [f"s{n}" for n in range(51, 60)]
LISTS = {
    "a": [("Skill", SKILL), ("UI", UI_ALL)],
    "b": [("Skill", SKILL), ("Interface", ["s04"]), ("Block UI", ["s51", "s52", "s53"]),
          ("Job UI", ["s54", "s55", "s56"]), ("Task UI", ["s57", "s58", "s59"])],
    "c": [("Skill", SKILL), ("Interface", ["s04"]), ("Navigation", ["s04"]), ("Block UI", ["s51", "s52", "s53"]),
          ("Job UI", ["s54", "s55", "s56"]), ("Task UI", ["s57", "s58", "s59"])],
}
CAPTIONS = {"Skill": "The topics that deliver a skill, each with its drawing, slides and mind map.",
            "UI": "The topics that deliver a screen, each with its drawing, slides and mind map."}
RAIL = ["Report", "Work", "Studio", "Interactions", "Delivery", "Timeline", "Files"]
ORANGE = "border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)"   # focus_page.interaction_button

PREVIEW_CSS = """
/* preview only: the page without its fixed rails; the right rail is drawn as one line under the path */
.focus-page.pv{max-width:none;padding:14px 22px 30px}.pv h1{margin:6px 0 8px}
.rail-line{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0 0;font-size:12.5px}
.rail-line .rl-word{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-right:2px}
.rail-line span.rl{padding:1px 9px;border:1px solid var(--line);border-radius:5px;color:var(--muted)}
.rail-line span.rl.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .section-views{flex-wrap:wrap;gap:6px;margin:0 0 10px}.pv .section-views a{padding:3px 12px;font-size:13px}
.pv .section-views a.wait{""" + ORANGE + """}
.pv .section-views a.wait[aria-current]{background:light-dark(#fff4e6,#3a2a12)}
.pv .focus-card .focus-content{padding:0}.pv .focus-content>.view-caption{margin:0 0 10px;font-size:13px}
/* the Studio card, compact: the real .studio-row, smaller */
.pv .studio-row{grid-template-columns:minmax(0,1fr) 128px;gap:12px;padding:8px 12px;margin:0 0 8px}
.pv .row-thumb img,.pv .row-thumb.none{width:128px;height:72px}
.pv .row-name{font-size:14px}.pv .studio-row .row-address{font-size:12px}
.pv .row-stage,.pv .row-type{font-size:11px;padding:0 7px;margin-left:6px}
.pv .focus-content .row-line{font-size:12.5px;margin:3px 0;line-height:1.45}
.pv .row-verbs{gap:5px;margin:4px 0 0;flex-wrap:wrap}.pv .row-verb{font-size:11px;padding:1px 8px;border-radius:6px}
.pv .studio-row.wait{border-color:light-dark(#ffa94d,#b35c00)}
.row-open{color:light-dark(#c92a2a,#ff8787);font-weight:600;margin-right:5px}
/* a view's section: its heading folds it, open by default (haipipe-ui rule 4), as a paper view's .fd-h */
.vsec{margin:0 0 4px}.vsec-h{display:flex;gap:8px;align-items:baseline;font-size:13.5px;font-weight:600;margin:0 0 8px;
 border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:5px 12px}
.vsec-h::before{content:"\\25BE";color:var(--muted);font-size:12px}.vsec-h small{font-weight:400;color:var(--muted)}
/* Q1: each view drawn as its own small panel, as its button opens it */
.screens{display:grid;grid-template-columns:1fr;gap:10px;align-items:start;margin-top:4px}
.screens.two{grid-template-columns:1fr}
.screen{border:1px solid var(--line);border-radius:10px;padding:8px 10px;background:var(--paper);min-width:0}
.screen-title{font-size:13px;font-weight:700;margin:0 0 4px}.screen-title span{font-weight:400;color:var(--muted)}
.mh{font-size:11.5px;font-weight:600;margin:6px 0 2px}.mh::before{content:"\\25BE  ";color:var(--muted)}
.mrow{font-size:12px;padding:3px 0 3px 12px;border-bottom:1px solid var(--line);white-space:nowrap;overflow:hidden;
 text-overflow:ellipsis}.mrow:last-child{border-bottom:0}.mrow b{font-weight:600}.mrow i{font-style:normal;color:var(--muted)}
.mrow.twice{background:light-dark(#fff4e6,#3a2a12)}
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def diff(on: bool) -> str:
    return " diff" if on else ""


# ── the topics, from their faces ───────────────────────────────────────────────────────────────────────────────────
def field(text: str, key: str) -> str:
    m = re.search(rf"(?mi)^\*\*{key}:\*\*[^\S\n]*`?([^`\n]+)", text)
    return m.group(1).strip() if m else ""


def label(rel: str) -> tuple[str, str]:
    """frame.topic_label's words: b17-s01:theme_work @ work_ladder, or for a Task's sNN
    b17.j03.t01-s51:theme_work.work_workbench_pages.block_page @ block_ui_report."""
    parts, short = rel.split("/"), lambda name, k=1: name.split("_", k)[k] if "_" in name else name
    topic = parts[-1]
    num, name = topic.split("-", 1)[0], topic.split("-", 1)[1].replace("-", "_")
    rungs = [p.split("_")[0] for p in parts[:-1]]
    address = "b17" + "".join("." + r for r in rungs) + "-" + num
    names = ["theme_work"] + [short(p) for p in parts[:-1]]
    return f"{address}:{'.'.join(names)} @ ", name


def place(rel: str) -> tuple[str, str]:
    """Where a topic sits: the Block itself, or 'j03 · t01_block_page' with its Task's title."""
    parts = rel.split("/")
    if len(parts) == 1:
        return "b17_theme_work", "this Block"
    task = BLOCK / parts[0] / parts[1]
    title = (task / f"{parts[1]}.md").read_text(encoding="utf-8").splitlines()[0]
    return f"{parts[0].split('_')[0]} · {parts[1]}", re.sub(r"^#\s*t\d+\s*·\s*", "", title).strip()


def asked_about() -> set:
    """The sNN a collection Run is about (its run.yaml target:), so its card carries the Interaction button."""
    out = set()
    for card in BLOCK.rglob("runs/r*_collect_*/run.yaml"):
        m = re.search(r"(?m)^target:.*?-(s\d+)[:\s]", card.read_text(encoding="utf-8"))
        if m:
            out.add(m.group(1))
    return out


def topics() -> dict:
    asked, out = asked_about(), {}
    for rel in TOPIC_DIRS:
        folder = BLOCK / rel
        text = (folder / f"{folder.name}.md").read_text(encoding="utf-8")
        topic_line = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S)
        topic_line = re.sub(r"\s+", " ", topic_line.group(1)).strip() if topic_line else ""
        first = re.match(r"(.+?[.;])(?:\s|$)", topic_line)            # today's line: focus_page.studio_html's cut
        opened = re.search(r"(?ms)^Open\n-+\n(.*?)(?=^\(write|\Z)", text)
        item = re.search(r"(?m)^1\.\s+(.+)$", opened.group(1)) if opened else None
        lead = folder / f"{folder.name}.slides.json"
        picture = f"{folder.name}.png"
        if lead.is_file():
            try:
                picture = json.loads(lead.read_text(encoding="utf-8"))["slides"][0]["image"]
            except (ValueError, KeyError, IndexError):
                pass
        num = folder.name.split("-", 1)[0]
        tags = [t for t in (["Slide"] if (folder / f"{folder.name}.slides.html").is_file() else [])
                + ["Draw", "Mind map", "Work", "Delivery"] + (["Interaction"] if num in asked else [])]
        out[num] = {"num": num, "rel": rel, "label": label(rel), "place": place(rel),
                    "stage": (re.search(r"(?mi)^\*\*Stage:\*\*[^\S\n]*`?([A-Za-z]+)", text) or [None, ""])[1].lower(),
                    "type": field(text, "Delivery type").lower(),
                    "today": first.group(1) if first else topic_line[:200], "covers": field(text, "Covers"),
                    "open": item.group(1).strip() if item else "", "picture": f"{UP}{rel}/{picture}", "tags": tags}
    return out


T = topics()


# ── the page's parts ───────────────────────────────────────────────────────────────────────────────────────────────
def rail() -> str:
    spans = "".join(f'<span class="rl{" on" if n == "Studio" else ""}">{esc(n)}</span>' for n in RAIL)
    return f'<div class="rail-line"><span class="rl-word">Right rail</span>{spans}</div>'


def bar(groups: list, on: str, *, waits: tuple = (), mark: bool = False, mark_one: str = "") -> str:
    """The view-button-list: the Studio's groups, the open one current; a group where a form waits flagged."""
    out = []
    for g in groups:
        cls = " ".join(c for c in ("wait" if g in waits else "", "diff" if g == mark_one else "") if c)
        attrs = ((f' class="{cls}"' if cls else "") + (' aria-current="page"' if g == on else "")
                 + (' title="questions wait for you"' if g in waits else ""))
        out.append(f'<a{attrs}>{"🙋 " if g in waits else ""}{esc(g)}</a>')
    return f'<nav class="section-views studio-groups{diff(mark)}" aria-label="Views">{"".join(out)}</nav>'


def page(title: str, groups_bar: str, body: str, caption: str = "") -> str:
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            "<body><main class=\"focus-page pv\">"
            "<div class=\"focus-crumb\">Tools-SPACE / blueprints / Project-Ladder / work / b17_theme_work</div>"
            f"{rail()}<h1>b17_theme_work<span class=\"h1-section\">Studio</span></h1>{groups_bar}"
            f"<section class=\"focus-card\"><div class=\"focus-content\">{cap}{body}</div></section></main></body></html>")


def words(text: str) -> str:
    """A face's words on the card: escaped, `code` drawn as code (the proposal's line renders it; today's shows ticks)."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", esc(text))


def line_of(t: dict, kind: str) -> str:
    """A card's one line: 'open' its first Open item (else today's), 'today' the Topic's first sentence, 'covers'."""
    if kind == "open" and t["open"]:
        return f'<span class="row-open">Open</span>{words(t["open"])}'
    if kind == "covers" and t["covers"]:
        return words(t["covers"])
    return words(t["today"])


def card(t: dict, *, line: str = "open", group: str = "UI", waits: bool = False, mark_line: bool = False) -> str:
    """One topic as the Studio card draws it: label, stage word (the type word only when it is not the group), one
    line, its tags, its picture; a waiting form edges it and flags its Interaction tag."""
    lead, name = t["label"]
    words = f'<span class="row-stage">{esc(t["stage"])}</span>'
    if t["type"] and t["type"].casefold() != group.casefold():
        words += f'<span class="row-type">{esc(t["type"])}</span>'
    tags = []
    for k, tag in enumerate(t["tags"]):
        if tag == "Interaction" and waits:
            tags.append(f'<a class="row-verb" style="{ORANGE}" title="questions wait for you">🙋 Interaction</a>')
        else:
            tags.append(f'<a class="row-verb{" main" if k == 0 and tag == "Slide" else ""}">{esc(tag)}</a>')
    return (f'<article class="status-row studio-row{" wait" if waits else ""}" id="{esc(t["rel"].split("/")[-1])}"><div>'
            f'<p class="row-title"><span class="row-address">{esc(lead)}</span><a class="row-name">{esc(name)}</a>{words}</p>'
            f'<p class="row-line{diff(mark_line)}">{line_of(t, line)}</p><p class="row-verbs">{"".join(tags)}</p></div>'
            f'<a class="row-thumb"><img src="{esc(t["picture"])}" alt="{esc(t["num"])}"></a></article>')   # eager: a
    # preview sits in a scaled frame, where a lazy picture may never be asked for


def sections(nums: list) -> list:
    """The topics split by where each sits, in reading order: [(heading, title, [nums])]."""
    out = []
    for n in nums:
        head, title = T[n]["place"]
        if not out or out[-1][0] != head:
            out.append((head, title, []))
        out[-1][2].append(n)
    return out


def vsec(head: str, title: str, inner: str, *, mark_head: bool = False, mark_all: bool = False) -> str:
    """One section of a view: its heading (it folds the section) and its cards."""
    return (f'<section class="vsec{diff(mark_all)}"><h3 class="vsec-h{diff(mark_head)}">{esc(head)}'
            f'<small>{esc(title)}</small></h3>{inner}</section>')


def panel(group: str, nums: list, *, mark: bool = False, twice: tuple = ()) -> str:
    """One view drawn small, as its button opens it: its place headings and a line per topic."""
    rows = "".join(f'<div class="mh">{esc(h)}</div>' + "".join(
        f'<div class="mrow{" twice diff" if n in twice else ""}"><b>{esc(n)}</b> <i>@</i> {esc(T[n]["label"][1])}</div>'
        for n in ns) for h, _, ns in sections(nums))
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">Studio <span>› {esc(group)}</span></div>'
            f'{rows}</section>')


# ── the questions ──────────────────────────────────────────────────────────────────────────────────────────────────
def previews() -> dict:
    out = {}
    # Q1 · the view list: each option's buttons, then each view as its own small panel
    for key, groups in LISTS.items():
        names = [g for g, _ in groups]
        changed = {"a": {"UI"}, "b": {"Interface", "Block UI", "Job UI", "Task UI"}, "c": {"Interface", "Navigation"}}[key]
        twice = ("s04",) if key == "c" else ()
        panels = "".join(panel(g, ns, mark=g in changed and key != "c", twice=twice if g in changed else ())
                         for g, ns in groups)
        out[f"q1-{key}"] = page(f"Q1 {key.upper()}", bar(names, "Skill", mark=True),
                                f'<div class="screens{" two" if key == "a" else ""}">{panels}</div>')
    # Q2 · what splits one view (UI, Q1's pick) into sections
    ui = dict(caption=CAPTIONS["UI"])
    by_place = "".join(vsec(h, title, "".join(card(T[n]) for n in ns), mark_head=True) for h, title, ns in sections(UI_ALL))
    out["q2-a"] = page("Q2 A", bar(["Skill", "UI"], "UI"), by_place, **ui)
    out["q2-b"] = page("Q2 B", bar(["Skill", "UI"], "UI"),
                       '<div class="diff">' + "".join(card(T[n]) for n in UI_ALL) + "</div>", **ui)
    by_stage = []
    for stage in ("explore", "shaping", "agreed", "closed"):
        ns = [n for n in UI_ALL if T[n]["stage"] == stage]
        if ns:
            by_stage.append((stage, ns))
    by_stage.sort(key=lambda s: UI_ALL.index(s[1][0]))                    # the stage of the first topic leads
    out["q2-c"] = page("Q2 C", bar(["Skill", "UI"], "UI"),
                       "".join(vsec(stage, "", "".join(card(T[n]) for n in ns), mark_head=True) for stage, ns in by_stage),
                       **ui)
    # Q3 · a card's one line, on the UI view's first two sections
    first = [s for s in sections(UI_ALL)][:2]
    for key, kind in (("a", "open"), ("b", "today"), ("c", "covers")):
        body = "".join(vsec(h, title, "".join(card(T[n], line=kind, mark_line=True) for n in ns)) for h, title, ns in first)
        out[f"q3-{key}"] = page(f"Q3 {key.upper()}", bar(["Skill", "UI"], "UI"), body, **ui)
    # Q4 · a waiting form: flagged on its group's button and opened there (A), only on its card (B, today), or flagged
    # only (C); in A a section that holds a waiting card leads its view, and that card leads its section
    waiting = [s for s in sections(UI_ALL) if any(n in WAITING for n in s[2])]
    rest = [s for s in sections(UI_ALL) if s not in waiting]
    lead = "".join(vsec(h, title, "".join(card(T[n], waits=n in WAITING) for n in
                                           sorted(ns, key=lambda n: (n not in WAITING, ns.index(n)))), mark_all=k == 0)
                   for k, (h, title, ns) in enumerate(waiting + rest))
    skill = "".join(vsec(h, title, "".join(card(T[n], group="Skill") for n in ns), mark_all=True)
                    for h, title, ns in sections(SKILL))
    out["q4-a"] = page("Q4 A", bar(["Skill", "UI"], "UI", waits=("UI",), mark_one="UI"), lead, **ui)
    out["q4-b"] = page("Q4 B", bar(["Skill", "UI"], "Skill", mark_one="UI"), skill, caption=CAPTIONS["Skill"])
    out["q4-c"] = page("Q4 C", bar(["Skill", "UI"], "Skill", waits=("UI",), mark_one="UI"), skill,
                       caption=CAPTIONS["Skill"])
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.name}/")


if __name__ == "__main__":
    main()
