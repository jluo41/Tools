"""r01_collect_theme_alignment's option previews (JL 261031: "I want you compare to others, like the theme_paper to
update the theme_work as well"): one small page per option, drawn in the workbench's own look (its focus.css,
inlined) with b17's and b16's real topic names, stages, delivery types and pictures, read from their faces on every
build; a topic the proposal adds is typed here and marked proposed. The part an option changes carries
class="diff", which the form boxes in orange.

The form shows a preview at half size in a frame 600 page pixels tall, so what differs sits in that height: no
Purpose and no rails (no option changes them), compact rows, the groups no option changes on one line, and two places
side by side when an option moves something between them (Studio and Work; b16 and b17).

Writes runs/r01_collect_theme_alignment/option-q<N>-<k>.html; question_collection.md links each one under its
option. The proposal they illustrate: s01-work-ladder/result/theme-alignment-proposal.md. Rerun after changing
anything here, never edit the pages:

    python src/build_r01_theme_alignment_previews.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

BLOCK = Path(__file__).resolve().parents[1]                       # b17_theme_work
RUN = BLOCK / "runs" / "r01_collect_theme_alignment"
B16 = BLOCK.parent / "b16_theme_paper"
TOOLS = next(p for p in BLOCK.parents if (p / "plugins" / "haipipe-toolkit").is_dir())
FOCUS_CSS = TOOLS / "plugins/haipipe-toolkit/servers/workbench/focus-assets/focus.css"
J03 = BLOCK / "j03_work_workbench_pages"
CRUMB = "Tools-SPACE / blueprints / Project-Ladder / work / "
WAITING = 'border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)'   # the live 🙋 Interaction look

PREVIEW_CSS = """
/* preview only: the page without its rails or Purpose; compact rows so what differs sits in the top 600 pixels */
.focus-page.pv{max-width:900px;padding:14px 22px 26px}.pv h1{margin:6px 0 8px}
.pv .section-views{flex-wrap:wrap;gap:6px;margin:0 0 8px}
.pv .section-views span{font-size:13px;border:1px solid var(--line);border-radius:8px;padding:3px 11px;color:var(--ink);background:var(--paper)}
.pv .section-views span.on{color:var(--accent);border-color:var(--accent);background:var(--soft)}
.pv .focus-card{margin-top:6px}.pv .focus-content{padding:12px 14px}
.pv .view-caption{margin:0 0 8px;font-size:12.5px}
.pv-ref{font-size:12px;color:var(--muted);margin:0 0 6px}.pv-ref b{font-weight:600;color:var(--ink)}
.pv .focus-content .focus-sub{margin:12px 0 5px;font-size:11.5px}
.pv .studio-row{grid-template-columns:minmax(0,1fr) 104px;gap:10px;padding:8px 10px;margin:0 0 6px}
.pv .row-thumb img,.pv .row-thumb.none{width:104px;height:58px;font-size:10.5px}
.pv .row-title{margin:0}.pv .row-name{font-size:13.5px}.pv .row-address{font-size:12px}
.pv .row-stage,.pv .row-type{font-size:10.5px;padding:0 6px}
.pv .focus-content .row-line{font-size:12px;margin:3px 0 0}
.pv .row-verbs{margin:5px 0 0;gap:5px}.pv .row-verb{font-size:11px;padding:1px 7px}
.crow{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px;padding:5px 10px;margin:0 0 5px;border:1px solid var(--line);border-radius:8px;font-size:12.5px;background:var(--paper)}
.crow .row-address{color:var(--muted)}.crow b{font-weight:700}
.pv-new{margin-left:6px;font-size:10.5px;padding:0 7px;border:1px dashed var(--accent);border-radius:9px;color:var(--accent);vertical-align:1px}
.pv-same{font-size:12px;color:var(--muted);padding:6px 10px;border:1px dashed var(--line);border-radius:8px;margin:10px 0 0}
.pv-note{font-size:12px;color:var(--muted);padding:6px 10px;border:1px dashed var(--muted);border-radius:8px;margin:6px 0}
.screens{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start;margin-top:8px}
.screen{border:1px solid var(--line);border-radius:10px;padding:9px 10px;background:var(--paper);min-width:0}
.screen-title{font-size:14.5px;font-weight:700;margin:0 0 6px;overflow-wrap:anywhere}
.screen-title span{font-weight:400;color:var(--muted);margin-left:6px;font-size:12.5px}
.screen .section-views{gap:4px;margin:0 0 6px}.screen .section-views span{font-size:10.5px;padding:1px 6px}
.screen .view-caption{font-size:11px;margin:0 0 6px}
.screen .studio-row{grid-template-columns:minmax(0,1fr) 78px;padding:6px 8px}
.screen .row-thumb img,.screen .row-thumb.none{width:78px;height:44px;font-size:9.5px}
.screen .row-name{font-size:12.5px}.screen .row-address{font-size:10.5px}
.jrow{padding:7px 9px;margin:0 0 6px;border:1px solid var(--line);border-radius:8px;font-size:12px;background:var(--paper)}
.jrow b{font-size:12.5px}.jrow p{margin:2px 0 0;color:var(--ink)}.jrow small{display:block;color:var(--muted);font-size:11px;margin-top:2px}
"""


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def diff(on: bool) -> str:
    return " diff" if on else ""


# ── the topics, read from their faces ───────────────────────────────────────────────────────────────────
def face_facts(folder: Path) -> dict:
    """What a topic's face says, with frame._note_facts's own patterns: its Topic's first sentence, stage, type."""
    text = (folder / f"{folder.name}.md").read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"\*\*Topic:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    topic = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    first = re.match(r"(.+?[.;])(?:\s|$)", topic)
    stage = re.search(r"(?mi)^\*\*Stage:\*\*[^\S\n]*`?([A-Za-z]+)", text)
    dtype = re.search(r"(?mi)^\*\*Delivery type:\*\*[^\S\n]*`?([A-Za-z]+)", text)
    return {"line": first.group(1) if first else topic[:160], "stage": stage.group(1).lower() if stage else "",
            "type": dtype.group(1).lower() if dtype else ""}


def picture(folder: Path) -> str:
    """The card's picture as the Studio picks it (its lead slide, else its preview), as a path from the Run folder."""
    record = folder / f"{folder.name}.slides.json"
    found = None
    if record.is_file():
        try:
            lead = folder / json.loads(record.read_text(encoding="utf-8"))["slides"][0]["image"]
            found = lead if lead.is_file() else None
        except (ValueError, KeyError, IndexError, TypeError):
            found = None
    if found is None and (folder / f"{folder.name}.png").is_file():
        found = folder / f"{folder.name}.png"
    if found is None:
        return ""
    rel = Path(*[".."] * len(RUN.relative_to(BLOCK.parent).parts)) / found.relative_to(BLOCK.parent)
    return rel.as_posix()


def short(name: str) -> str:
    """A rung's short name as frame.topic_label writes it: no jNN_/tNN_/sNN- prefix, dashes as underscores."""
    return re.sub(r"^[bjts]\d+[-_]", "", name).replace("-", "_")


def existing(folder: Path, address: str, **more) -> dict:
    return {"address": address, "name": short(folder.name), "pic": picture(folder), **face_facts(folder), **more}


def cell_address(block: str, block_short: str, job: Path, task: Path, nn: str) -> str:
    return f"{block}.{job.name[:3]}.{task.name[:3]}-{nn}:{block_short}.{short(job.name)}.{short(task.name)} @ "


T = {
    "s01": existing(BLOCK / "s01-work-ladder", "b17-s01:theme_work @ "),
    "s02": existing(BLOCK / "s02-work-skills", "b17-s02:theme_work @ "),
    "s04": existing(BLOCK / "s04-workbench-page-structure", "b17-s04:theme_work @ "),
    # proposed (theme-alignment-proposal.md § 4.2, 4.3); no face yet, so typed here
    "s21": {"address": "b17-s21:theme_work @ ", "name": "work_run_skill", "stage": "explore", "type": "skill", "pic": "",
            "line": "every work Run type and the skill behind it, and which skills make the work theme (b16's s21 shape)."},
    "s31": {"address": "b17-s31:theme_work @ ", "name": "work_guide", "stage": "explore", "type": "ui", "pic": "",
            "line": "the work Guide, rewritten for the focus page one level at a time; today it still teaches Questions."},
    "s11": {"address": "b17-s11:theme_work @ ", "name": "work_block", "stage": "explore", "type": "ui", "pic": "",
            "line": "the work Block's page as a whole, with what is on disk under each section."},
    "s12": {"address": "b17-s12:theme_work @ ", "name": "work_job", "stage": "explore", "type": "ui", "pic": "",
            "line": "a work Job's page as a whole, with what is on disk under each section."},
    "s13": {"address": "b17-s13:theme_work @ ", "name": "work_task", "stage": "explore", "type": "ui", "pic": "",
            "line": "a work Task's page as a whole, with what is on disk under each section."},
    "s61": {"address": "b17-s61:theme_work @ ", "name": "work_slides", "stage": "explore", "type": "display", "pic": "",
            "line": "the slides that explain the work theme on the ladder, for people new to the toolkit."},
}
CELLS = {}                                                          # s51..s59, from j03's three Tasks
for task in sorted(J03.glob("t0[1-3]_*")):
    for topic in sorted(task.glob("s5[1-9]-*")):
        nn = topic.name[:3]
        CELLS[nn] = existing(topic, cell_address("b17", "theme_work", J03, task, nn), task=task.name)
B16_J01 = B16 / "j01_paper_workbench_pages"
B16_CELLS = [existing(t, cell_address("b16", "theme_paper", B16_J01, t.parent, t.name[:3]))
             for t in sorted((B16_J01 / "t01_board_page").glob("s3[2-4]-*"))]

# the group bars (theme-alignment-proposal.md § 2.3, § 4.1)
B16_BAR = ["Structure", "Levels", "Run and Skill", "Guide", "Block UI", "Job UI", "Task UI"]
UI_BARS = ["Block UI", "Job UI", "Task UI"]
BAR = {"a": ["Skill", "Levels", "Guide"] + UI_BARS, "b": ["Skill", "UI"] + UI_BARS,
       "c": ["Skill", "Interface", "Navigation"] + UI_BARS + ["Other"]}


# ── the page parts ──────────────────────────────────────────────────────────────────────────────────────
def bar(names: list, on: str = "", mark: bool = False, studio: bool = True) -> str:
    buttons = "".join(f'<span class="{"on" if n == on else ""}">{esc(n)}</span>' for n in names)
    return f'<nav class="section-views{" studio-groups" if studio else ""}{diff(mark)}" aria-label="Views">{buttons}</nav>'


def addr(t: dict) -> str:
    """The address with its sNN in bold, so a renumbering reads at a glance."""
    return re.sub(r"(s\d\d)(?=:)", r"<b>\1</b>", esc(t["address"]), count=1)


def badge(word: str) -> str:
    return f'<span class="pv-new">{esc(word)}</span>' if word else ""


def row(t: dict, *, mark: bool = False, new: str = "", line: str = "", verbs: str = "") -> str:
    """One Studio card as studio_html draws it: address @ name, stage, type; its one line; its picture."""
    title = (f'<p class="row-title"><span class="row-address">{addr(t)}</span><span class="row-name">'
             f'{esc(t["name"])}</span><span class="row-stage">{esc(t["stage"])}</span>'
             f'<span class="row-type">{esc(t["type"])}</span>{badge(new)}</p>')
    pic = (f'<span class="row-thumb"><img src="{esc(t["pic"])}" alt="{esc(t["name"])}"></span>' if t["pic"]
           else '<span class="row-thumb none">no picture yet</span>')
    return (f'<article class="status-row studio-row{diff(mark)}"><div>{title}<p class="row-line">{esc(line or t["line"])}'
            f'</p>{verbs}</div>{pic}</article>')


def crow(t: dict, *, mark: bool = False, new: str = "") -> str:
    """One card on one line, for the whole-Studio view of Q1."""
    return (f'<div class="crow{diff(mark)}"><span class="row-address">{addr(t)}</span><b>{esc(t["name"])}</b>'
            f'<span class="row-stage">{esc(t["stage"])}</span><span class="row-type">{esc(t["type"])}</span>'
            f'{badge(new)}</div>')


def group(name: str, inner: str, mark: bool = False) -> str:
    return f'<section class="pv-group{diff(mark)}"><h3 class="focus-sub">{esc(name)}</h3>{inner}</section>'


def jrow(job: str, goal: str, tasks: str, *, mark: bool = False, new: str = "") -> str:
    """One Job on Work › Progress: its folder, its goal, its Tasks."""
    return (f'<article class="jrow{diff(mark)}"><b>{esc(job)}</b>{badge(new)}<p>{esc(goal)}</p>'
            f'<small>{tasks}</small></article>')


def interaction(waiting: bool = True, dashed: bool = False) -> str:
    style = WAITING + (";border-style:dashed" if dashed else "") if waiting else ""
    return (f'<p class="row-verbs"><span class="row-verb">Draw</span><span class="row-verb">Mind map</span>'
            f'<span class="row-verb" style="{style}">🙋 Interaction</span></p>')


def page(title: str, body: str, *, block: str = "b17_theme_work", section: str = "Studio", top: str = "",
         caption: str = "") -> str:
    """One preview page: the path, the title-&-section, the view-button-list (top), then the card with its caption."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    head = f'<h1>{esc(block)}<span class="h1-section">{esc(section)}</span></h1>{top}' if top else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{esc(title)}</title><style>{FOCUS_CSS.read_text(encoding='utf-8')}{PREVIEW_CSS}</style></head>"
            f'<body><main class="focus-page pv"><div class="focus-crumb">{esc(CRUMB + block if block else CRUMB[:-3])}</div>{head}'
            f'<section class="focus-card"><div class="focus-content">{cap}{body}</div></section></main></body></html>')


def screen(block: str, section: str, inner: str, *, top: str = "", caption: str = "", mark: bool = False) -> str:
    """One page drawn small, so two can sit side by side."""
    cap = f'<p class="view-caption">{esc(caption)}</p>' if caption else ""
    return (f'<section class="screen{diff(mark)}"><div class="screen-title">{esc(block)}<span>{esc(section)}</span>'
            f'</div>{top}{cap}{inner}</section>')


# ── Q1 · the group bar ──────────────────────────────────────────────────────────────────────────────────
def q1(key: str) -> str:
    skill = group("Skill", crow(T["s01"]) + crow(T["s21"], new="was s02"))
    same = ('<p class="pv-same">Block UI · Job UI · Task UI: s51 to s59, the nine cells, three each; the same in '
            'every option.</p>')
    if key == "a":
        middle = (group("Levels", crow(T["s04"]), mark=True)
                  + group("Guide", crow(T["s31"], new="proposed"), mark=True))
        tail = ""
    elif key == "b":
        middle = group("UI", crow(T["s04"]) + crow(T["s31"], new="proposed"), mark=True)
        tail = ""
    else:
        middle = (group("Interface", crow(T["s04"]), mark=True) + group("Navigation", crow(T["s04"]), mark=True))
        tail = group("Other", crow(T["s31"], new="proposed, no tag"), mark=True)
    top = (bar(BAR[key], "Skill", mark=True)
           + f'<p class="pv-ref"><b>b16_theme_paper</b>: {esc(" · ".join(B16_BAR))}</p>')
    return page(f"Q1 {key.upper()} · Studio groups", skill + middle + same + tail, top=top,
                caption="Every group opened, one under another; the page opens one group at a time.")


# ── Q2 · skills and Runs ────────────────────────────────────────────────────────────────────────────────
JOB_GOALS = {
    "j01": ("j01_work_ladder_contract", "build what b17-s01 hands over: haipipe-work's ladder section and the work "
            "scaffold", "t01_skill_section · t02_scaffold · t03_demo_fixture"),
    "j03": ("j03_work_workbench_pages", "the work theme's three pages on the focus page, each in its three sections",
            "t01_block_page · t02_job_page · t03_task_page"),
}


def j(key: str, **more) -> str:
    folder, goal, tasks = JOB_GOALS[key]
    return jrow(folder, goal, esc(tasks), **more)


def q2(key: str) -> str:
    if key == "a":
        studio = (row(T["s01"]) + row(T["s21"], mark=True, new="was s02",
                  line="every work Run type, the skill behind it, each skill's home, the update plan; s02 retired."))
        j02 = jrow("j02_work_skill_homes", "build what b17-s21 hands over: the skills-and-Runs table, the move list "
                   "for b04", 't01_skill_homes_table · t02_move_list_b04 · <b>t03_run_types_table</b> (new)', mark=True)
        work = j("j01") + j02 + j("j03")
    elif key == "b":
        studio = (row(T["s01"]) + row(T["s02"]) + row(T["s21"], mark=True, new="proposed",
                  line="every work Run type and the skill behind it, and the plan to update those skills."))
        j02 = jrow("j02_work_skill_homes", "build what b17-s02 hands over: haipipe-work's skill-homes table, and the "
                   "move list for b04", "t01_skill_homes_table · t02_move_list_b04")
        j04 = jrow("j04_work_run_types", "build what b17-s21 hands over: the Run types table and the skill update plan",
                   "t01_run_types_table · t02_skill_update_plan", mark=True, new="new")
        work = j("j01") + j02 + j("j03") + j04
    else:
        studio = (row(T["s01"]) + row(T["s02"])
                  + '<p class="pv-note diff">No topic names the work Run types: haipipe-run\'s table still lists the '
                    'six Spaces and run-ask-&lt;qNN&gt;.</p>')
        j02 = jrow("j02_work_skill_homes", "build what b17-s02 hands over: haipipe-work's skill-homes table, and the "
                   "move list for b04", "t01_skill_homes_table · t02_move_list_b04")
        work = j("j01") + j02 + j("j03")
    body = ('<div class="screens">'
            + screen("b17_theme_work", "Studio", studio, top=bar(BAR["a"], "Skill"),
                     caption="The Skill group: the topics that deliver skills.")
            + screen("b17_theme_work", "Work", work, top=bar(["Progress"], "Progress", studio=False),
                     caption="Its Jobs, each making one topic's delivery.")
            + "</div>")
    return page(f"Q2 {key.upper()} · Skills and Runs", body)


# ── Q3 · new topics ─────────────────────────────────────────────────────────────────────────────────────
J04_GUIDE = jrow("j04_work_guide", "build what b17-s31 hands over: the work Guide's text, cut by level, and its place "
                 "on the focus page", "t01_guide_text · t02_guide_place", mark=True, new="new")
J02_WIDE = jrow("j02_work_skill_homes", "build what b17-s21 hands over: the skills-and-Runs table, the move list for "
                "b04", "t01_skill_homes_table · t02_move_list_b04 · t03_run_types_table")


def q3(key: str) -> str:
    guide = group("Guide", row(T["s31"], new="proposed"), mark=True)
    levels = group("Levels", crow(T["s04"]))                       # s04 itself does not change in A, B or C
    names = BAR["a"]
    tail, work = "", j("j01") + J02_WIDE + j("j03") + J04_GUIDE
    if key == "b":
        levels = group("Levels", crow(T["s04"]) + "".join(row(T[n], mark=True, new="proposed")
                                                         for n in ("s11", "s12", "s13")))
    elif key == "c":
        names = ["Skill", "Levels", "Guide", "Slides"] + UI_BARS
        tail = group("Slides", row(T["s61"], new="proposed"), mark=True)
    elif key == "d":
        names = ["Skill", "Levels"] + UI_BARS
        levels = group("Levels", row(T["s04"], mark=True,
                                     line="Its Open 3 keeps the Guide's question: where should Guide appear?"))
        guide, work = "", j("j01") + J02_WIDE + j("j03")
    studio = levels + guide + tail
    body = ('<div class="screens">'
            + screen("b17_theme_work", "Studio", studio, top=bar(names, "Levels", mark=key in ("c", "d")),
                     caption={"c": "Levels, Guide and Slides opened, one under another.",
                              "d": "Levels opened; there is no Guide group."}.get(key, "Levels and Guide opened, one "
                                                                                    "under the other."))
            + screen("b17_theme_work", "Work", work, top=bar(["Progress"], "Progress", studio=False),
                     caption="Its Jobs; a new topic brings the Job that makes it.")
            + "</div>")
    return page(f"Q3 {key.upper()} · New topics", body)


# ── Q4 · the UI cell numbers ────────────────────────────────────────────────────────────────────────────
def renumbered(t: dict, new_nn: str) -> dict:
    return {**t, "address": re.sub(r"-s5\d:", f"-{new_nn}:", t["address"])}


def q4(key: str) -> str:
    left = "".join(row(t) for t in B16_CELLS)
    block_cells = [CELLS[nn] for nn in ("s51", "s52", "s53")]
    if key == "a":                                                  # what else changes, first, so the frame shows it
        right = '<p class="pv-note diff">Job UI s54 to s56 · Task UI s57 to s59; each form keeps its address.</p>'
        right += "".join(row(t, mark=True, verbs=interaction()) for t in block_cells)
    else:
        right = ('<p class="pv-note diff">Job UI s35 to s37 · Task UI s38 to s40; s32 given back, s51 to s59 retired; '
                 'nine forms re-addressed and rebuilt; one answered first drops off its card.</p>')
        right += "".join(row(renumbered(t, nn), mark=True, verbs=interaction(dashed=True))
                         for t, nn in zip(block_cells, ("s32", "s33", "s34")))
    body = ('<div class="screens">'
            + screen("b16_theme_paper", "Studio", left, top=bar(B16_BAR, "Block UI"), caption="b16: s32 to s40.")
            + screen("b17_theme_work", "Studio", right, top=bar(BAR["a"], "Block UI"),
                     caption="b17: the same three cells.")
            + "</div>")
    return page(f"Q4 {key.upper()} · UI cell numbers", body, block="")


def previews() -> dict:
    out = {f"q1-{k}": q1(k) for k in "abc"}
    out.update({f"q2-{k}": q2(k) for k in "abc"})
    out.update({f"q3-{k}": q3(k) for k in "abcd"})
    out.update({f"q4-{k}": q4(k) for k in "ab"})
    return out


def main() -> None:
    made = previews()
    for name, text in made.items():
        (RUN / f"option-{name}.html").write_text(text, encoding="utf-8")
    print(f"wrote {len(made)} previews into {RUN.relative_to(BLOCK)}/")


if __name__ == "__main__":
    main()
