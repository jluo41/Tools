"""b16-s01:theme_paper @ paper_tree_concept, its drawing: haipipe-studio's five parts (scripts/five_parts.py), as b17-s04.
Its Design is the paper's four layers and how they feed each other (JL 261031): the plan layer (the Board's own
topics: idea, story, venue, data flow, paper flow), the explore layer (internal: work Blocks; external: discovery
Blocks), the evidence layer (values from the internal side, citations from the external side, displays), and the
writing layer (one writing Job per send). Its sentence: one paper Block links many discovery Blocks (external) and
work Blocks (internal), deposits them into its evidence Jobs, and writes them into papers."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
from five_parts import *  # noqa: E402,F401,F403
from five_parts import _el  # noqa: E402
import five_parts  # noqa: E402

SKILL = TOOLS / "plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper/SKILL.md"

SPEC = {
    "title": "Paper tree concept: plan, explore, evidence, writing",
    "why": {"question": "why do we need s01?",
            "notes": ["displays were drawn\nin the work Block", "versions and evidence\nshared one jNN list",
                      "no line said where\nthe idea and story sit"],
            "quote": "JL 261031: plan layer, explore layer, evidence layer, writing layer"},
    "what": {"head": "② what s01 hands over: the paper's layers, as skill rules", "icon": "code", "name": "haipipe-paper",
             "type": "skill", "deck_why": "stays in s01's delivery/deck/, so anyone gets it in a minute",
             "parts": [("code", "haipipe-paper/SKILL.md", "the four layers, the Job names", "four layers" in SKILL.read_text()),
                       ("code", "paper_ladder.py evidence", "makes j01-j03; versions from j11", True),
                       ("code", "haipipe-paper/checklist.md", "where a paper stands, layer by layer",
                        (SKILL.parent / "checklist.md").is_file()),
                       ("code", "paper_check.py <Paper-Board>", "ticks the checklist from the Board's files",
                        (SKILL.parent / "scripts/paper_check.py").is_file()),
                       ("page", "this drawing", "how the layers feed each other", True)]},
    "job": None,
    "target": "skills/2_theme/paper/haipipe-paper (SKILL.md, scripts/paper_ladder.py), haipipe-paper-evidence",
    "missing": [],
}


def box(eid, x, y, w, h, title, lines, color, fill="#ffffff", size=15):
    els = [_el("rectangle", eid, x, y, w, h, color, fill, roundness={"type": 3})]
    els += text(eid + "_t", x + 14, y + 10, title, size + 2, color)
    for k, ln in enumerate(lines):
        els += text(f"{eid}_l{k}", x + 14, y + 40 + 24 * k, ln, 13, INK)
    return els


def lane(eid, x, y, name, sub):
    return text(eid, x, y, name, 20, TITLE) + text(eid + "_s", x, y + 28, sub, 13, BODY)


def design():
    els, X, Y = [], 690, 300
    cols = (X, X + 470, X + 940, X + 1410)            # plan · explore · evidence · writing, left to right
    names = (("① Plan layer", "the paper Board's own topics"), ("② Explore layer", "where the material is made"),
             ("③ Evidence layer", "what this paper quotes, beside the versions"), ("④ Writing layer", "one Job per send"))
    for k, (n, s) in enumerate(names):
        els += lane(f"ln{k}", cols[k], Y, n, s)
    # ① plan: the Board's topics, the idea first
    els += box("pl", cols[0], Y + 70, 380, 300, "paper Board · Paper-<Slug>/",
               ["💡 Idea         s01-ideation", "📖 Story        s02-story-<telling>", "🏛 Venue        venues/<venue>/",
                "🔀 Data flow    s03-paper-dataflow", "🗺 Paper flow   s04-paper-workflow", "📚 Related      s10 (the venue's papers)",
                "    the questions, the telling, the plan"], NAVY)
    # ② explore: internal (work) and external (discovery)
    els += box("in", cols[1], Y + 70, 380, 150, "🧪 Internal · work Blocks",
               ["work/bNN_…: datasets, regressions", "on raw data (CMS stays here)", "→ returned, aggregated Results"], OR, "#fff4e6")
    els += box("ex", cols[1], Y + 250, 380, 150, "🔎 External · discovery Blocks",
               ["discovery/bNN_…: papers, sources", "each read by a Run", "→ cards, facts, verified BibTeX"], PU, "#f3f0ff")
    # ③ evidence: three Jobs
    els += box("ev1", cols[2], Y + 70, 380, 100, "🔢 j02_evidence_value",
               ["printed numbers, one Task per group", "← internal Results"], OR, "#fff4e6")
    els += box("ev2", cols[2], Y + 190, 380, 100, "🖼 j01_evidence_display",
               ["figures and tables (t01- main, t51- app.)", "← internal Results, drawn here"], GR, "#ebfbee")
    els += box("ev3", cols[2], Y + 310, 380, 100, "📎 j03_evidence_cite",
               ["citations, one Task per claim group", "← external, verified CITE Results"], PU, "#f3f0ff")
    # ④ writing
    els += box("wr", cols[3], Y + 70, 380, 300, "✍️ j11_writing_v<MMDD>_<desk>",
               ["one Job per send: j11, j12, …", "t00 Summary · t01-t19 Sections", "t20-t29 Appendix · t30-t39 letters",
                "each Section quotes the evidence,", "never computes it", "", "the venue's form is applied here"], NAVY)
    # the flows
    els += arrow("a1", [(cols[0] + 380, Y + 160), (cols[1], Y + 145)], ROOM, width=2)
    els += arrow("a2", [(cols[0] + 380, Y + 250), (cols[1], Y + 325)], ROOM, width=2)
    els += arrow("a3", [(cols[1] + 380, Y + 140), (cols[2], Y + 120)], OR, width=2)
    els += arrow("a4", [(cols[1] + 380, Y + 160), (cols[2], Y + 240)], OR, width=2)
    els += arrow("a5", [(cols[1] + 380, Y + 330), (cols[2], Y + 360)], PU, width=2)
    for k, yy in enumerate((Y + 120, Y + 240, Y + 360)):
        els += arrow(f"a6{k}", [(cols[2] + 380, yy), (cols[3], Y + 220)], GR, width=2)
    els += arrow("a7", [(cols[0] + 190, Y + 370), (cols[0] + 190, Y + 470), (cols[3] + 190, Y + 470), (cols[3] + 190, Y + 370)],
                 NAVY, width=1)
    els += text("a7_t", cols[1] + 120, Y + 480, "the story and paper flow say what each Section tells", 14, BODY)
    els += text("sent", X, Y + 530,
                "One paper Block links many discovery Blocks (external) and work Blocks (internal), deposits them into its "
                "evidence Jobs, and writes them into papers.", 17, TITLE)
    return els


if __name__ == "__main__":
    five_parts.build(HERE, SPEC, design, shift=1500)   # four lanes need room before Process
