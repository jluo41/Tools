"""The nine sNN of j03 · The work pages, level by level: one per level (Block, Job, Task) and section (Report, Work,
Studio), each drawn in haipipe-studio's five parts (scripts/five_parts.py), as b16's paper_ui_cells.py draws the
paper's (JL 261031: "I think you should focus on the things like ... b16_theme_paper ... studio ... UI and think about
how you should update the work_theme's workbench UI"). Each sNN's builder is `build(Path(__file__).parent)`: its cell
is found by its folder name (s51-block-ui-report → block, report).

A cell's Design is two sketches: A, the screen as proposed (its page, its view-button-list, its content), and B, the
detail A leans on; each carries its open question in red. The sample pages are b17's own (a Tools blueprint, public).
The Block's Report carries JL's r01 answers (t01_block_page/runs/r01_collect_report_and_delivery).
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
import five_parts  # noqa: E402

VERB = {"report": "Report · check", "work": "Work · do", "studio": "Studio · think"}
PAGE = {"block": ("b17_theme_work", "…/work/b17_theme_work"),
        "job": ("j01_work_ladder_contract", "…/b17_theme_work/j01_work_ladder_contract"),
        "task": ("t01_skill_section", "…/j01_work_ladder_contract/t01_skill_section")}
TAGS = "Slide · Draw · Mind map · Work · Delivery"         # the tags below an sNN (r01 Q3)
WAITS = ("sign", "asked", "pass", "send", "open", "planned")


# ── the screen's parts, drawn plainly ───────────────────────────────────────────────────────────────────────────
def window(eid, x, y, w, h, url):
    els = [_el("rectangle", eid, x, y, w, h, INK, "#ffffff", roundness={"type": 3})]
    els += line(eid + "_bar", [(x, y + 28), (x + w, y + 28)], ROOM, 1)
    return els + [_el("ellipse", f"{eid}_d{k}", x + 10 + k * 14, y + 9, 9, 9, ROOM, ROOM) for k in range(3)] + \
        text(eid + "_url", x + 60, y + 7, url, 12, BODY)


def head(eid, x, y, name, section, views, on=0):
    """The title-&-section, then the view-button-list, the open view in orange."""
    els = text(eid + "_t", x, y, name, 20, INK) + text(eid + "_s", x + 12 * len(name) + 20, y + 4, VERB[section], 15, ROOM)
    cx = x
    for k, v in enumerate(views):
        w = 12 + 8 * len(v)
        els += [_el("rectangle", f"{eid}_v{k}", cx, y + 38, w, 24, OR if k == on else ROOM,
                    "#fff4e6" if k == on else "#ffffff", roundness={"type": 3})] + text(f"{eid}_v{k}_t", cx + 6, y + 42, v, 12, INK)
        cx += w + 8
    return els


def row(eid, x, y, w, name, words, state=""):
    els = [_el("rectangle", eid, x, y, w, 50, ROOM, "#ffffff", roundness={"type": 3})]
    els += text(eid + "_n", x + 12, y + 7, name, 14, TITLE) + text(eid + "_d", x + 12, y + 28, words, 11, BODY)
    return els + (text(eid + "_w", x + w - 90, y + 16, state, 13, OR if state.split()[0] in WAITS else GR) if state else [])


def card(eid, x, y, w, addr, words, word="", tags=TAGS):
    """An sNN as the Studio card draws it: address, one line, its word, the tags below that open each part (r01 Q3:
    "we just need to click the tags below the sNN"), its picture on the right."""
    els = [_el("rectangle", eid, x, y, w, 70, ROOM, "#ffffff", roundness={"type": 3})]
    els += [_el("rectangle", eid + "_p", x + w - 96, y + 10, 84, 50, ROOM, "#f1f3f5")]
    els += text(eid + "_a", x + 12, y + 8, addr, 13, TITLE) + text(eid + "_w", x + 12, y + 28, words, 11, BODY)
    els += text(eid + "_v", x + 12, y + 48, tags, 11, INK)
    return els + (text(eid + "_s", x + w - 190, y + 8, word, 12, OR if word in WAITS else GR) if word else [])


def bar(eid, x, y, w, words, warn=False):
    """A full-width line of the content: a waiting row (orange), a folded section (▾), a note."""
    return [_el("rectangle", eid, x, y, w, 40, OR if warn else ROOM, "#fff4e6" if warn else "#ffffff",
                roundness={"type": 3})] + text(eid + "_t", x + 14, y + 12, words, 13, INK)


def doc(eid, x, y, w, title, n=4):
    """A result as it reads: its title, then its lines."""
    els = [_el("rectangle", eid, x, y, w, 30 + 22 * n, ROOM, "#ffffff", roundness={"type": 3})] + text(eid + "_t", x + 12, y + 8, title, 13, TITLE)
    return els + [e for k in range(n) for e in line(f"{eid}_l{k}", [(x + 12, y + 44 + 22 * k), (x + w - 40 - 60 * (k % 2), y + 44 + 22 * k)], ROOM, 2)]


def notes(eid, x, y, items):
    """Small labelled lines under a sketch: (title, words)."""
    els = []
    for k, (t, w) in enumerate(items):
        yy = y + 64 * k
        els += i_page(f"{eid}{k}", x, yy) + text(f"{eid}{k}_n", x + 50, yy - 2, t, 15, TITLE) + text(f"{eid}{k}_w", x + 50, yy + 22, w, 13, BODY)
    return els


# ── the nine cells: Idea's words, the delivery piece, the two sketches and their open questions ───────────────────
def a_frame(cell, views, on, h):
    level, section = cell
    name, path = PAGE[level]
    els = window("wA", 690, 340, 700, h, f"…&path={path}&section={section}")
    return els + head("hA", 730, 384, name, section, views, on)


def block_report():
    # r01: one view per delivery type (Q2: C); a delivery opens from its tags (Q3); planned until made (Q4: A); no
    # Questions (Q5: A); one word, its current version (Q6: A). r02's proposal: the map branches by Job, and the UI view
    # opens with the live Block, Job and Task pages
    els = a_frame(("block", "report"), ("MindMap", "Skill", "UI"), 1, 300)
    els += card("rA0", 730, 460, 620, "b17-s01 · haipipe-work", "skills/2_theme/work/haipipe-work/SKILL.md", "planned")
    els += card("rA1", 730, 544, 620, "b17-s02 · workbench-work", "skills/2_theme/work/workbench-work/SKILL.md", "planned")
    b = notes("nB", 1500, 360, (("MindMap", "first: each Job, what it makes, its Tasks"),
                                ("Skill · UI", "one view per delivery type, never per name"),
                                ("the UI view", "opens with the live Block, Job, Task pages"),
                                ("one word", "its current version, or planned")))
    return els, b, "? the row's picture: the topic's\ndrawing, or its delivery's"


def block_work():
    # r03's proposal: one view; what waits first; a section per Job; the Block's own Runs last (s52-D01: status lives here)
    els = a_frame(("block", "work"), ("Progress",), 0, 360)
    els += bar("iA", 730, 460, 620, "🙋 Interactions: forms wait on you  ·  Answer all", True)
    for k, (j, w, s) in enumerate((("j01_work_ladder_contract", "makes s01 · haipipe-work · planned", "open"),
                                   ("j02_workbench_work_skill", "makes s02 · workbench-work · planned", "open"),
                                   ("j03_work_workbench_pages", "makes s04 and the nine UI sNN", "open"))):
        els += row(f"rA{k}", 730, 512 + 60 * k, 620, j, w, s)
    els += bar("oA", 730, 696, 620, "▾ Its own Runs", False)
    b = notes("nB", 1500, 360, (("Interactions", "every waiting form, first, orange"),
                                ("a Job section", "what it makes, each Task one line"),
                                ("its own Runs", "the Block's runs/, last")))
    return els, b, "? a Job's section: every Task,\nor only the next one"


def block_studio():
    # r04's proposal: one view per delivery type, split by where each topic sits, a waiting card first
    els = a_frame(("block", "studio"), ("Skill", "UI"), 1, 330)
    els += text("gA", 730, 456, "b17_theme_work", 13, TITLE)
    els += card("rA0", 730, 478, 620, "b17-s04 @ page frame", "what every work page shares", "shaping", TAGS + " · Interaction")
    els += text("gB", 730, 560, "j03 · t01_block_page", 13, TITLE)
    els += card("rA1", 730, 582, 620, "b17.j03.t01-s51 @ block_ui_report", "the Block's Report", "explore", TAGS + " · Interaction")
    b = notes("nB", 1500, 360, (("Skill · UI", "one view per delivery type, as the Report"),
                                ("sections", "where each topic sits: Block, Job, Task"),
                                ("a waiting card", "first, orange")))
    return els, b, "? views by delivery type,\nor one per level as today"


def job_report():
    # r01's proposal (t02): MindMap, then the one type the Job makes: its delivery's card, then its pieces by Task
    els = a_frame(("job", "report"), ("MindMap", "Skill"), 1, 330)
    els += card("rA0", 730, 460, 620, "b17-s01 · haipipe-work", "what this Job makes: haipipe-work's SKILL.md", "planned")
    els += text("pA", 730, 548, "its pieces, by Task", 13, TITLE)
    for k, (t, w) in enumerate((("t01_skill_section", "haipipe-work's SKILL.md, rewritten"), ("t03_demo_fixture", "a fresh agent's check"))):
        els += row(f"rB{k}", 730, 572 + 58 * k, 620, t, w, "planned")
    b = notes("nB", 1500, 360, (("MindMap", "what it makes, its Tasks, their Runs"), ("Skill", "the one delivery this Job makes"),
                                ("its pieces", "one row each, by the Task that makes it")))
    return els, b, "? each Task's result too,\nor only the Job's delivery"


def job_work():
    # r02's proposal (t02): one view; an Interactions box first; Task rows in the face's order with their Runs
    els = a_frame(("job", "work"), ("Tasks",), 0, 340)
    els += bar("iA", 730, 460, 620, "🙋 Interactions: a form waits on you  ·  Answer", True)
    for k, (t, w, s) in enumerate((("t01_skill_section", "rewrites haipipe-work's SKILL.md · run-write-ladder-section", "open"),
                                   ("t03_demo_fixture", "tests haipipe-work with a fresh agent", "open"))):
        els += row(f"rA{k}", 730, 512 + 60 * k, 620, t, w, s)
    b = notes("nB", 1500, 360, (("Interactions", "what waits on you, first"), ("a Task row", "its goal, the piece it makes, its Runs"),
                                ("order", "the face's ## Tasks")))
    return els, b, "? a Task's Runs under its row,\nor a Runs view"


def job_studio():
    # r03's proposal (t02): its groups' views; in each, what waits, then the Block topic this Job makes, then its own
    els = a_frame(("job", "studio"), ("Skill",), 0, 280)
    els += text("hA", 730, 456, "This Job makes", 13, TITLE)
    els += card("rA0", 730, 478, 620, "b17-s01 · haipipe-work", "the Block topic this Job makes", "explore")
    els += text("nA", 730, 566, "No sNN sits at j01 or its Tasks yet.", 13, BODY)
    b = notes("nB", 1500, 360, (("This Job makes", "the Block topic its Runs deliver"), ("its own", "five sNN at most"),
                                ("each Task's", "three at most, under its Task")))
    return els, b, "? show the Block topic this\nJob makes, or only its own"


def task_report():
    # r01's proposal (t03): MindMap, then the Task's type: one row per current Run, the thing it made, small
    els = a_frame(("task", "report"), ("MindMap", "Skill"), 1, 330)
    els += text("hA", 730, 456, "make", 13, TITLE)
    els += row("rA0", 730, 478, 620, "run-write-ladder-section", "the section it wrote, as it reads now", "planned")
    els += doc("dA", 730, 542, 620, "haipipe-work SKILL.md › The work ladder")
    b = notes("nB", 1500, 360, (("one row per Run", "under its role: make, check, figures"),
                                ("the thing, small", "a table, a figure, or the section"), ("one word", "its version, or planned")))
    return els, b, "? the newest Run's result,\nor every Run's"


def task_work():
    # r02's proposal (t03): one view; what waits first; every Run by role; Ask the agent last; a Run opens in the pop-out
    els = a_frame(("task", "work"), ("Runs",), 0, 340)
    els += bar("aA", 730, 460, 620, "🙋 Waits for you: a form to answer  ·  Answer", True)
    els += text("hA", 730, 516, "make", 13, TITLE)
    els += row("rA0", 730, 538, 620, "run-write-ladder-section", "soft · design · queued · no pass yet", "next")
    els += bar("bA", 730, 604, 620, "▾ Ask the agent  ·  Copy prompt", False)
    b = notes("nB", 1500, 360, (("a Run row", "its line, its word, its newest pass"), ("what waits", "orange, first"),
                                ("a Run", "opens in the pop-out, no page")))
    return els, b, "? a row per Run,\nor one per pass"


def task_studio():
    # r03's proposal (t03): on every Task's rail: what this Task makes, its own topics, Ask the agent last
    els = a_frame(("task", "studio"), ("Skill",), 0, 300)
    els += text("hA", 730, 456, "This Task makes", 13, TITLE)
    els += card("rA0", 730, 478, 620, "b17-s01 · haipipe-work", "its piece: the SKILL.md section", "explore")
    els += text("nA", 730, 566, "Its topics: none sits at t01_skill_section yet.", 13, BODY)
    els += bar("aA", 730, 594, 620, "▾ Ask the agent  ·  Copy prompt: start a topic", False)
    b = notes("nB", 1500, 360, (("This Task makes", "the Block topic its Run delivers"), ("its topics", "three at most"),
                                ("Ask the agent", "last, plain")))
    return els, b, "? start an sNN here\nwith one click"


CELLS = {
    ("block", "report"): (block_report, "the Block's Report: the map and its deliveries by type",
                          ["the Report showed Status,\nFindings and Questions", "a delivery opened only\nfrom a Studio row",
                           "views would name each\ndelivery, not its type"]),
    ("block", "work"): (block_work, "the Block's Work: one row per Job",
                        ["where things stand sat\nin the Report", "a Job row did not say\nwhich sNN it makes",
                         "a waiting form was\nhard to find"]),
    ("block", "studio"): (block_studio, "the Block's Studio: its topics by group",
                          ["topics sat in studio/,\nout of sight", "one topic held all\nthe work pages",
                           "a card's tags did not\nsay what they open"]),
    ("job", "report"): (job_report, "a Job's Report: the delivery it makes",
                        ["a Job page repeated\nthe Block's views", "its delivery sat in\nthe Block's topic",
                         "no view said what\nthe Job hands over"]),
    ("job", "work"): (job_work, "a Job's Work: its Tasks in order",
                      ["Tasks sat as cards\nwith many tabs", "the order was the\nfolders', not the plan's",
                       "a Run hid two\nclicks deep"]),
    ("job", "studio"): (job_studio, "a Job's Studio: the topics it makes",
                        ["a Job had no Studio\nof its own", "the topic it makes\nsat at the Block",
                         "nothing linked the two"]),
    ("task", "report"): (task_report, "a Task's Report: its newest result",
                         ["a Task's Report listed\nreceipts, not results", "the newest result was\nclicks away",
                          "a soft Run's pass\nhad no place"]),
    ("task", "work"): (task_work, "a Task's Work: its Runs and what waits",
                       ["Runs sat in old\nSpaces and tabs", "a pass had no row", "the next step was\nnot said"]),
    ("task", "studio"): (task_studio, "a Task's Studio: its own topics",
                         ["a Task had no Studio", "its sNN sat in the\nBlock's studio/", "no talk-and-sketch\nprompt"]),
}


def build(topic: Path):
    topic = Path(topic).resolve()
    m = re.match(r"s(\d+)-(block|job|task)-ui-(report|work|studio)$", topic.name)
    nn, level, section = m.group(1), m.group(2), m.group(3)
    sketch, piece, why = CELLS[(level, section)]
    ui = topic / "delivery" / "ui"
    part = f"ui/{level}-{section}"
    spec = {"title": f"{level.capitalize()} UI · {VERB[section]}: {piece.split(': ', 1)[1]}",
            "why": {"question": f"why do we need s{nn}?", "notes": why,
                    "quote": "JL 261031: like b16's Studio UI, 3 x 3, Block, Job, Task × Report, Work, Studio"},
            "what": {"head": f"② what s{nn} hands over: one screen", "icon": "page", "name": "delivery/ui/", "type": "ui",
                     "deck_why": f"stays in s{nn}'s delivery/deck/, so anyone gets it in a minute",
                     "parts": [("page", part, piece, (ui / f"{level}-{section}").exists())]},
            "job": topic.parent.parent,
            "target": "servers/workbench/focus_page.py (the base page, design_b02_workbench)",
            "missing": [] if (ui / f"{level}-{section}").exists() else [(part, "the agreed screen, not drawn yet")]}

    def design():
        a, b, ask = sketch()
        els = text("skA", 690, 280, f"A · {piece}", 18, TITLE) + shapes("skA_s", 690, 306, f"delivery/{part}") + a
        els += text("skB", 1500, 280, "B · what A leans on", 18, TITLE) + shapes("skB_s", 1500, 306, "the parts, one line each") + b
        bottom = max(e["y"] + e["height"] for e in a)
        return els + sticky("askD", 1180, bottom + 60, 320, 76, ask, 15, -0.03, RED, RE)

    return five_parts.build(topic, spec, design)
