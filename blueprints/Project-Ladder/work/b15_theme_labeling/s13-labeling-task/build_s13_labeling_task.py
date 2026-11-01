"""b15 · s13-labeling-task's drawing: the slide deck's steps (version 12) placed on a labeling Job's six Task types,
in haipipe-studio's five parts (scripts/five_parts.py). Its Design is one map, step → Task → view → what it writes →
the person's gate, then the two loops (🧭 meaning, 🛠 expression) and the round report; the first drawing (261014, the five types with the
old stage names) is kept whole below it (JL 261030: "We should keep them").

The steps and their words come from s03's deck (delivery/deck/source/deck-content-v12.json); the files each step
writes are CONTRACTS.md version 2's lanes (s03-agent-role/implementation-plan/). JL 261101: "go ahead and update them".

    python build_s13_labeling_task.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403  (the helpers and build())
from five_parts import _el  # noqa: E402
import five_parts  # noqa: E402

# step · what happens · Task · its view · what it writes (CONTRACTS.md v2) · the person's gate
MAP = [
    ("0 · corpus into items", "itemize; Train and Test roles by source group", "📦 items", "Data · Items · Embedding · Split",
     "items manifest · splits/manifest-vNN", "✍️ sign the recipe"),
    ("1 · frame the task", "the label, who decides, its values", "🧭 meaning", "Frame", "task frame fNN",
     "🙋 interaction: 3 questions"),
    ("2 · investigate", "search, compare, group: an interaction report", "🧭 meaning", "Report", "runs/rNN_collect_report_mNN", ""),
    ("3 · collect preferences", "cards: choose, own rule, defer", "🧭 meaning", "Preferences",
     "…/result/answer_collection.md", "🙋 interaction: the cards"),
    ("4 · update and check", "new meaning mNN; affected items rechecked", "🧭 meaning", "Update",
     "policy/versions/ · gold/versions/lNN", ""),
    ("5 · execute, evaluate", "rewrite from Train; run Train + Test; report", "🛠 expression", "Rewrite · Run · Evaluate",
     "expressions/ · staging/round-NN/", ""),
    ("6 · freeze, release check", "rules, wording, labels, settings frozen", "🛠 expression", "Release", "handoff/hNN",
     "✍️ sign the release"),
    ("7 · label at scale, audit", "batches; risky cases; random audit", "🔍 scanning", "Batches · Audit · Final labels",
     "production/ · audit/", "✍️ accept the delivery"),
    ("evaluation", "final labels against the experts' gold", "📊 score", "Agreement", "the score Task's result/", ""),
    ("(input)", "the dataset's own labels, fenced", "📏 ground truth", "Labels", "the raw Task's result/", ""),
]
COLS = ("step (slides v12)", "what happens", "Task", "its views", "what it writes", "your gate")
WIDTHS = (230, 380, 150, 290, 300, 200)
TEAM = "#1971c2"


def box(eid, x, y, w, h, words, stroke=INK, fill="#ffffff", size=15):
    return [_el("rectangle", eid, x, y, w, h, stroke, fill, roundness={"type": 3})] + text(eid + "_t", x + 12, y + 10, words, size, INK)


def loop(x, y):
    """The two loops and the round report between them (pages 6, 12 and 12a): meaning Loop 1, 2 … (making m01, m02 …)
    with you; expression rounds e01, e02 … under one approved meaning, without you; the round report sends expression back."""
    els = text("lp_h", x, y, "two loops: 🧭 meaning asks you; 🛠 expression never does; the round report links them", 17, TITLE)
    y += 90
    els += box("lp_rep", x, y, 200, 64, "Report\n2 investigate", TEAM, "#ffffff")
    els += box("lp_pre", x + 260, y, 220, 64, "Preferences\n3 🙋 your interaction", OR, SEM["start"][0])
    els += box("lp_upd", x + 540, y, 200, 64, "Update\n4 new meaning mNN", TEAM, "#ffffff")
    for k, (a, b) in enumerate(((200, 260), (480, 540))):
        els += arrow(f"lp_a{k}", [(x + a, y + 32), (x + b, y + 32)], ROOM)
    els += arrow("lp_m", [(x + 640, y), (x + 640, y - 30), (x + 100, y - 30), (x + 100, y)], TEAM)
    els += text("lp_m_t", x + 230, y - 54, "open or conflicting: the next meaning loop", 12, TEAM)
    y2 = y + 150
    els += box("lp_rew", x, y2, 200, 64, "Rewrite\n5 from Train only", PU, "#ffffff")
    els += box("lp_run", x + 260, y2, 220, 64, "Run\n5 Train + Test", PU, "#ffffff")
    els += box("lp_eva", x + 540, y2, 200, 64, "Evaluate\n5 round report", PU, "#ffffff")
    els += box("lp_rel", x + 860, y2, 200, 64, "Release\n6 ✍️ sign", GR, SEM["end"][0])
    for k, (a, b) in enumerate(((200, 260), (480, 540), (740, 860))):
        els += arrow(f"lp_b{k}", [(x + a, y2 + 32), (x + b, y2 + 32)], ROOM)
    els += text("lp_go", x + 760, y2 + 4, "criteria met", 12, GR)
    els += arrow("lp_x", [(x + 640, y2 + 64), (x + 640, y2 + 100), (x + 100, y2 + 100), (x + 100, y2 + 64)], PU)
    els += text("lp_x_t", x + 210, y2 + 108, "wording issue: the next expression round, same meaning", 12, PU)
    els += arrow("lp_dn", [(x + 740, y + 32), (x + 800, y + 32), (x + 800, y2 - 26), (x + 50, y2 - 26), (x + 50, y2)], TEAM)
    els += text("lp_dn_t", x + 812, y + 70, "approved mNN → the next Rewrite", 12, TEAM)
    els += arrow("lp_up", [(x + 620, y2), (x + 620, y + 100), (x + 150, y + 100), (x + 150, y + 64)], OR)
    els += text("lp_up_t", x + 250, y + 78, "rule or label issue: the round report → the next Report", 12, OR)
    els += text("lp_tt", x, y2 + 150, "Train: develops the wording. Test: labeled, scored and audited; its issues go to meaning, "
                                       "never to the rewriting. Every meaning loop records its interaction (the history).", 14, INK)
    return els, y2 + 190


def build(topic: Path):
    topic = Path(topic).resolve()
    skill = topic / "delivery" / "skill" / "labeling-task-types.md"
    spec = {"title": "Labeling Task: the slides' steps on six Task types",
            "why": {"question": "why do we need s13?",
                    "notes": ["the types used stage\nnames from 261014", "slides v12 moved to\ntwo loops and rounds",
                              "each screen needs\none step-to-view map"],
                    "quote": "JL 261101: go ahead and update them"},
            "what": {"head": "② what s13 hands over: the map", "icon": "book", "name": "skill/", "type": "skill",
                     "deck_why": "stays in s13's delivery/deck/, so anyone gets it in a minute",
                     "parts": [("book", "skill/labeling-task-types.md", "the map, for haipipe-labeling and labeling_theme.py",
                                skill.exists())]},
            "job": None,
            "target": "skills/2_theme/labeling/haipipe-labeling · labeling_theme.py TYPES",
            "missing": [] if skill.exists() else [("skill/labeling-task-types.md", "not written yet")]}

    def design():
        x, y = 690, 280
        els = text("maptitle", x, y, "one map: each step of the slides (version 12) → its Task → its views → what it writes → your gate", 18, TITLE)
        t, bottom = data_table("map", x, y + 40, "steps 0 to 7, plus the two inputs and the evaluation", COLS, WIDTHS,
                               MAP, TITLE, "#e7f5ff", note="from deck-content-v12.json and CONTRACTS.md v2", rh=26)
        els += t
        lp, bottom = loop(x, bottom + 70)
        els += lp
        els += sticky("open_s13", x + 1500, bottom - 120, 330, 110,
                      "❓ release: inside expression,\nor a Task of its own?\n"
                      "❓ items for several labels:\nBlock or Job?", 14, -0.02, RED, RE)
        return els + five_parts.kept_first(topic, bottom + 120, label="kept: s13's first drawing (261014), "
                                           "the five types with the old stage names")

    els = design()                                    # measured first: the Design is moved and grown 1.25x when placed
    right = max(e["x"] + e["width"] for e in els)
    shift = int(1400 + (right - 690) * 1.25 + 160 - 2210)   # Process starts at 2210; it must clear the grown Design
    return five_parts.build(topic, spec, lambda: els, shift=shift)


if __name__ == "__main__":
    build(HERE)
