"""b17-s01:theme_work @ work_ladder, its drawing: haipipe-studio's five parts (scripts/five_parts.py), as b16-s01.

Its Design is the work ladder itself, as haipipe-work's SKILL.md will say it (JL 261031: "this studio's content need
to be totally rewrite, I think the draw need to be updated as well?"):

    A  one rung per level (a work Block, Job, Task, Run and Studio topic): its folder, what it holds, whether it gets
       a page; a Run and a topic get none (JL 261031: "run will not get its page, and also the studio will not has
       its own page as well"); under it the terms it uses and what happens next
    B  what A leans on: the door, haipipe-work, sending each kind of request to the skill that owns it
    ?  the face's three open points in red where they sit: Open 1 as a box with its options and the leaning
       starred (drop the work scaffold), Open 2 on its route (an older Block's Questions), Open 3 by A's title

"What s01 hands over" lists the pieces of delivery/render.yaml, each ticked when the Run its `by:` names is done; the
Idea's words, the rungs and the routes are typed here, since they are the proposal. five_parts rewrites the drawing on
every build, so a change goes into this file, never onto the canvas.

    python build_s01_work_ladder.py        writes s01-work-ladder.excalidraw and its card s01-work-ladder.png
"""
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
import five_parts  # noqa: E402

JOB = HERE.parent / "j01_work_ladder_contract"


def pieces():
    """What s01 hands over, read from delivery/render.yaml: (icon, name, why, done), done when its Run is."""
    card = yaml.safe_load((HERE / "delivery" / "render.yaml").read_text(encoding="utf-8")) or {}
    out = []
    for pc in card.get("pieces") or []:
        name, _, why = (pc.get("code") or pc.get("from") or "").partition(": ")
        out.append(("book", name, why, five_parts._closed(HERE, pc.get("by", ""))))
    return out


SPEC = {
    "title": "Work ladder: haipipe-work's SKILL.md, rung by rung",
    "why": {"question": "why do we need s01?",
            "notes": ["haipipe-work still\ndraws Questions,\nreports/ and studio/",
                      "its Runs sit in the\nold runs/ + results/\nlayout",
                      "no rung says which\nlevel gets a page"],
            "quote": "JL 261031: \"this studio's content need to be totally rewrite\""},
    "what": {"head": "② what s01 hands over: haipipe-work, rewritten", "icon": "book", "name": "haipipe-work",
             "type": "skill", "deck_why": "stays in s01's delivery/deck/, so anyone gets it in a minute",
             "parts": pieces()},
    "job": JOB,
    "target": "skills/2_theme/work/haipipe-work/SKILL.md",
    "missing": [],
}

# ── A · the rungs: (name, folder, holds, its face or kinds, a fourth line, gets a page) ─────────────────────────────
RUNGS = [
    ("\U0001f9f1 Block", "work/bNN_<topic>/",
     "its Jobs · sNN (≤ 9) · runs/ (soft, forms) · related/ · src/ · delivery/",
     "board.md: spine · close · ## Topic · ## Deliveries; no ## Questions", "", True),
    ("\U0001f9f0 Job", "jNN_<job>/",
     "its Tasks · sNN (≤ 5) · runs/ (soft) · src/ · sbatch/ · delivery/",
     "jNN_<job>.md: goal · close · ## Topic, the sNN it makes · ## Tasks in order", "", True),
    ("\U0001f6e0 Task", "tNN_<task>/",
     "scripts/ · runs/<run>/ · sNN (≤ 3) · notebooks/ · sbatch/ · delivery/",
     "tNN_<task>.md: state · goal · close · task-type ▸ haipipe-task-for-<kind>", "", True),
    ("⚙️ Run", "runs/<run>/",
     "run.yaml · ticket · config.yaml · result/ (hard only) · passes/pNN-<MMDD>/",
     "hard rNN_<slug> · soft run-<type>-<target> · form rNN_collect_<slug>",
     "opens as a row on its Task's Work, in the pop-out", False),
    ("\U0001f4a1 Studio topic", "sNN-<topic>/ beside its Jobs or Tasks",
     "face · drawing and preview · mind map · ideas, slides · delivery/ · result/",
     "one idea, one delivery of one type, made by the Job beside it",
     "opens as a card where it sits: Slide · Draw · Mind map · Work · Delivery · Interaction", False),
]
TERMS = ("hard Run: a ticket, writes only its result/ · soft Run: agent work in its level · "
         "form: a person's questions")

# ── B · where a request goes: (the skill, its tools, the request); the five rung owners first, in rung order ────────
ROUTES = [
    ("haipipe-block", "new_board.py --no-questions", "a new work Block, its face"),
    ("haipipe-job", "new_job.py job · task · check", "a new Job, its Tasks in order"),
    ("haipipe-task", "task-type ▸ haipipe-task-for-<kind>", "build, run or close a Task, of its kind"),
    ("haipipe-run", "soft_run.py new · pass", "a Run's card, a pass, a Workflow"),
    ("haipipe-studio", "new_topic.py · render_delivery.py", "an sNN: its face, drawing and delivery/"),
    ("haipipe-interaction", "collect.py", "a question for the person, as a form"),
    ("workbench-work", "", "the pages, planned: Report · Work · Studio"),
    ("haipipe-project", "ladder.py audit", "the shape every theme shares"),
    ("haipipe-related", "related/related.md", "what came in from outside"),
    ("haipipe-delivery", "", "a Block's, Job's or Task's own delivery/"),
    ("haipipe-data · -nn · -end · -individual", "", "the pipelines a Task runs, not the theme"),
    ("haipipe-report", "", "? older Blocks' Questions, until moved"),       # Open 2, still open: red, in place
]
OPEN1 = ("? drop the work scaffold (Open 1)", [("A", "drop it: the base skills make every rung", True),
                                           ("B", "keep a thin one that calls them in order", False),
                                           ("C", "a scaffold of its own (t02, now in _old/)", False)])

ROW, TOP, BX, BW = 124, 350, 770, 920          # a rung's step, the first rung's top, the rung box's left and width


def rung(i, name, folder, holds, face, more, page):
    y = TOP + i * ROW
    els = [_el("rectangle", f"rg{i}", BX, y, BW, 110, NAVY if page else ROOM, "#ffffff" if page else "#f8f9fa",
               roundness={"type": 3})]
    els += line(f"rg{i}_step", [(700, y + 55), (744, y + 55)], INK, 3)             # the ladder's rung itself
    els += text(f"rg{i}_n", BX + 16, y + 10, name, 20, TITLE)
    els += text(f"rg{i}_f", BX + 16 + len(name) * 20 * 0.62 + 22, y + 14, folder, 15, INK)
    els += text(f"rg{i}_h", BX + 16, y + 44, holds, 13, INK)
    els += text(f"rg{i}_x", BX + 16, y + 66, face, 13, BODY)
    if more:
        els += text(f"rg{i}_m", BX + 16, y + 88, more, 12, OR)
    bx = BX + BW - 286                                                              # its page, or none
    if page:
        els += [_el("rectangle", f"rg{i}_pg", bx, y + 10, 268, 80, GR, "#ebfbee", roundness={"type": 3})]
        els += text(f"rg{i}_pg_t", bx + 14, y + 16, "\U0001f4c4 its page", 15, GR)
        els += text(f"rg{i}_pg_s", bx + 14, y + 40, "Report · Work · Studio", 13, INK)
        els += text(f"rg{i}_pg_v", bx + 14, y + 62, "check · do · think", 12, BODY)
    else:
        els += [_el("rectangle", f"rg{i}_pg", bx, y + 10, 268, 62, ROOM, "#ffffff", strokeStyle="dashed",
                    roundness={"type": 3})]
        els += text(f"rg{i}_pg_t", bx + 14, y + 16, "no page", 15, INK)
        els += text(f"rg{i}_pg_s", bx + 14, y + 40, "it opens where it sits", 13, BODY)
        els += text(f"rg{i}_new", bx + 140, y + 80, "✎ 261031 no page", 12, GR)      # where JL's answer landed
    return els


DOOR_X, FAN_X, FAN_W, FAN_STEP = 1716, 2010, 396, 56     # the door, then one box per owner


def door():
    """B: the door takes every request in and sends it to its owner: a fan of arrows, the rung owners first."""
    dx, dy = DOOR_X, TOP + (len(ROUTES) * FAN_STEP - 6) / 2 - 48
    els = [_el("rectangle", "fan_door", dx, dy, 200, 96, PU, SEM["agent"][0], roundness={"type": 3})]
    els += text("fan_door_t", dx + 14, dy + 10, "haipipe-work", 18, PU)
    els += text("fan_door_s", dx + 14, dy + 38, "the door: it names", 13, INK)
    els += text("fan_door_s2", dx + 14, dy + 58, "the owner, never acts", 13, INK)
    els += arrow("fan_in", [(dx + 100, dy - 70), (dx + 100, dy)], PU, width=2)
    els += text("fan_in_t", dx + 4, dy - 102, "a request comes in", 14, PU)
    els += text("fan_key", dx, dy + 112, "dark: a rung's owner\ngrey: another request\nred: still open", 12, BODY)
    for k, (skill, tools, ask) in enumerate(ROUTES):
        y = TOP + k * FAN_STEP
        rung_owner, still_open = k < len(RUNGS), ask.startswith("?")
        edge = RE if still_open else NAVY if rung_owner else ROOM
        els += [_el("rectangle", f"own{k}", FAN_X, y, FAN_W, 50, edge, "#fff5f5" if still_open else "#ffffff",
                    strokeStyle="dashed" if still_open else "solid", roundness={"type": 3})]
        els += text(f"own{k}_s", FAN_X + 12, y + 6, skill, 14, RE if still_open else TITLE if rung_owner else INK)
        if tools:
            els += text(f"own{k}_t", FAN_X + 22 + len(skill) * 14 * 0.62, y + 9, tools, 11, BODY)
        els += text(f"own{k}_a", FAN_X + 12, y + 28, ask, 12, RE if still_open else INK)
        els += arrow(f"fan{k}", [(dx + 200, dy + 48), (FAN_X, y + 25)], edge, width=1, dashed=still_open)
    return els


def open_one(x, y):
    """The face's Open 1, its options side by side with the leaning starred: the one question this Design waits on."""
    ask, options = OPEN1
    els = [_el("rectangle", "askD", x, y, 520, 40 + 30 * len(options), RE, SEM["warn"][0], roundness={"type": 3})]
    els += text("askD_q", x + 16, y + 10, ask, 17, RE)
    for k, (key, words, lean) in enumerate(options):
        els += text(f"askD_o{k}", x + 28, y + 42 + 30 * k, f"{key}  {words}" + ("  ★ leaning" if lean else ""), 14,
                    GR if lean else INK)
    return els


def design():
    els = text("skA", 690, 280, "A · the work ladder: what each rung holds, whether it gets a page", 18, TITLE)
    els += text("skA_q", 1310, 308, "? in the SKILL.md: one line a rung (Open 3)", 13, RE)   # still open, in place
    els += shapes("skA_s", 690, 306, "haipipe-work/SKILL.md › The work ladder: one rung per level")
    bottom = TOP + (len(RUNGS) - 1) * ROW + 110
    els += line("lad_l", [(700, TOP), (700, bottom)], INK, 3) + line("lad_r", [(744, TOP), (744, bottom)], INK, 3)
    for i, r in enumerate(RUNGS):
        els += rung(i, *r)
    els += text("lad_note", BX, bottom + 14, "each rung's own contract stays with its owner (B); the shape every theme "
                "shares is haipipe-project's ref/ladder.md", 13, BODY)
    els += text("lad_terms", BX, bottom + 36, TERMS, 13, BODY)
    els += text("lad_next", BX, bottom + 58, "next: t01 rewrites the SKILL.md once s01 is agreed; then t03 checks it "
                "with a fresh agent", 13, PU)
    els += text("skB", DOOR_X, 280, "B · what A leans on: the door and each owner", 18, TITLE)
    els += shapes("skB_s", DOOR_X, 306, "haipipe-work/SKILL.md › Where a request goes")
    els += door()
    return els + open_one(BX + 130, bottom + 100)


if __name__ == "__main__":
    for name, _, holds, face, more, _ in RUNGS:                      # a rung's words stay inside its box
        assert len(holds) <= 76 and len(face) <= 76 and len(more) <= 86, name
    assert len(TERMS) * 13 * 0.62 <= DOOR_X - BX - 10, "the terms line runs into B"
    assert all(len(f"{k}  {w}  * leaning") * 14 * 0.62 + 28 <= 520 for k, w, _ in OPEN1[1]), "an option overflows its box"
    for skill, tools, ask in ROUTES:                                 # an owner's words stay inside its box
        assert len(skill) * 14 * 0.62 + len(tools) * 11 * 0.62 + 34 <= FAN_W and len(ask) * 12 * 0.62 + 24 <= FAN_W, skill
    five_parts.build(HERE, SPEC, design, shift=1600)                 # the fan needs room before Process
