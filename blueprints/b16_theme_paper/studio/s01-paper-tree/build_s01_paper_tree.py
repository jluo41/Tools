"""s01 · Paper tree: s01-paper-tree.excalidraw, the paper's ladder drawn as b10's s01 draws the shared one
(JL 261011: "follow the b10's s01, to have the tree like that"): one node per level stepping down and right,
its specials branching right with what each holds, a box under each node (definition, on screen, variants),
and the skills that own each level in a column on the right.

Levels: the paper Theme folder, a paper Board, a version (one send), a Section, a Run. The facts come from
this topic's decisions (s01-D01..D10), b10's rules for every Block (s09-D01, D02, D05; s01-D32, D34) and a
real Board read on 261011 (Paper-ScalingGlucose-NatSeries2026). The drawing it replaced, ten frames of
boundaries and screens, is kept in history/ (build_s01_paper_tree-261011-v1.py and its drawing).

The stairs are b10's own code (build_ladder_v4.draw_ladder, its dense settings), so both trees look alike.

    python build_s01_paper_tree.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
sys.path.insert(0, str(TOOLS / "blueprints/b10_project_workbench/studio/s01-overall-tree-structure"))
sys.path.insert(0, str(TOOLS / "blueprints/b10_project_workbench/studio/_build"))
import build_ladder_v4 as L  # noqa: E402  (b10's ladder: draw_ladder, sp, its dense sizes)
sys.path.insert(0, str(TOOLS / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

sp = L.sp
NEW = "✎ 261011 "

LAYERS = [  # (level, node, [specials], [variants])
    ("Theme", "paper/", [
        sp("_archive/", "retired paper Boards"),
        sp("Paper-<name>/ …", "holds its paper Boards, one per paper idea", holds=True)],
     ["one folder per Project", "read by the paper theme"]),
    ("Board", "Paper-<name>/", [
        sp("board.md", "its face: board-kind: paper-board · spine · close · ## Questions"),
        sp("related/", "", job={
            "define": "what the paper sits beside, one table (b10 s01-D34); the Board keeps the related work",
            "node": "related.md", "node_define": "one row per item: kind · date · item · link · feeds · group",
            "tree": [("├── papers, datasets, code", "rows of related.md (s01-D02)"),
                     ("├── meetings/ · files/ · emails/", "as they came; each subfolder a group (b10 s04-D08, D09)"),
                     ("└── venues ?", "a row of kind venue, or venues/<venue>/? (s04)")]}),
        sp("studio/", "", job={
            "define": "the Board's only Studio, opened from every version and Section (b10 s09-D01)",
            "node": "sNN-<topic>/", "node_define": "one topic; Story and Ideation are topics, not Pages (s01-D06)",
            "tree": [("├── s01-ideation/", "the ideas, generated and selected (s01-D07)"),
                     ("├── s02-story-<venue>-<idea>/", "one telling: questions, claims, Section order"),
                     ("├── s03-paper-workflow/", "how the paper's work runs"),
                     ("└── sNN-<topic>.md", "Stage · decided · open")]}),
        sp("reports/", "", job={
            "define": "the research questions, each with its report (s01-D08)",
            "node": "qNN_<question>/", "node_define": "one research question: a light Page",
            "tree": [("├── qNN_<question>.md", "Answer · Evidence · Limits · Next"),
                     ("└── e.g. q00 … q06", "ScalingGlucose's seven")]}),
        sp("delivery/", "the Board's only delivery/: each version's built paper in delivery/jNN_<version>/ "
                        "(b10 s01-D32); a person marks a send done"),
        sp("runs/", "soft Runs: run-draw-<sNN> · run-report-<qNN> · run-<type>-<target>"),
        sp("jNN_<version>/ …", "holds its versions, one per send; on screen Work", holds=True)],
     ["one paper idea, venue-free (s01-D01)", "e.g. Paper-ScalingGlucose-NatSeries2026"]),
    ("Version", "jNN_v<MMDD>_<venue>/", [
        sp("jNN_<version>.md", "its face: the venue (s01-D03) · ## Narrative, the Section order (s01-D10) · "
                               "## Questions, the standing questions"),
        sp("reports/", "its own Report: the standing questions, comments and review rounds (s05 ?)"),
        sp("runs/", "run-assemble · run-check-submit · run-comments-<round>"),
        sp("tNN_<section>/ …", "holds its Sections in reading order: t0N main · t2N appendix · t3N letters",
           holds=True)],
     ["one send to one venue", "e.g. j01_v1009_nmi", "? a resubmission: a new version (s05)"]),
    ("Section", "tNN_<section>/", [
        sp("tNN_<section>.md", "its face, a Page: the Section's text; Requirement: venue rules, rubric"),
        sp("draft/", "the plan: paragraphs, Bullets, Evidence Items (haipipe-draft-structure)"),
        sp("reports/", "its own questions; often the Page itself answers them"),
        sp("runs/", "holds its Runs: run-section-<slug> · run-value|display|citation-<slug>", holds=True)],
     ["a Page Task", "e.g. t00_abstract · t02_results · t21_extended-data", "a letter: t3N_<letter>"]),
    ("Run", "runs/<run>/", [
        sp("run.yaml", "the card: kind · type · target · status · passes"),
        sp("passes/pNN-<MMDD>/", "one pass per rerun or session"),
        sp("where it lives", "soft only in a paper; its evidence comes from the Project's work/ and "
                             "discovery/ Results")],
     ["soft: write · display · value · cite · build · draw", "hard Runs: never in a paper Board"]),
]
DEFINE = {
    "Theme": "the paper Theme folder of a Project: one Board per paper idea",
    "Board": "one paper idea: its research questions, its tellings, its related work; venue-free",
    "Version": "one send to one venue: which questions and results, the Section order, the build",
    "Section": "one Section, the Abstract or a letter, written as a Page Task",
    "Run": "one soft Run of its level; each rerun or session is a pass",
}
ON_SCREEN = {
    "Board": "top row: Guide · Studio | Paper Board · Version · Section | Delivery, Related folded inside "
             "Studio (b10 s04-D05); Spaces: Description | Report | Work | Runs",
    "Version": "picked in the top row; no Related, Studio or Delivery of its own: the top row's Studio and "
               "Delivery open the Board's",
    "Section": "picked in the top row; the base's Page Task views (Draft, Evidence)",
    "Run": "a row in its level's Runs view; opens a pop-out",
}
SKILLS = {
    "Theme": ["haipipe-paper  (the door)"],
    "Board": ["haipipe-paper", "haipipe-paper-ideation", "haipipe-paper-story", "haipipe-question",
              "workbench-paper"],
    "Version": ["haipipe-paper-workflow", "haipipe-paper-venue", "haipipe-paper-assemble",
                "haipipe-paper-comments"],
    "Section": ["haipipe-paper-section", "haipipe-draft-workflow", "haipipe-draft-structure · -evidence · -writing"],
    "Run": ["haipipe-run  (soft)"],
}
LAYER_NOTES = {}


def link_back(frame):
    """A Section owns no delivery/ (JL 261011: "for the section, we will do not have the related studio and
    delivery"; "for the Jobs ... as well"): its built output goes up to the Board's delivery/, drawn as one
    dashed arrow from the Section's runs/ line to the Board's delivery/ line, through the right margin, with
    ScalingGlucose's real path beside it."""
    def find(prefix):
        return next(e for e in L.els if e["type"] == "text" and str(e.get("text", "")).startswith(prefix))
    runs = find("holds its Runs: run-section")
    deliv = find("the Board's only delivery/")
    skills_x = find("haipipe-paper-section")["x"]
    right = max(e["x"] + e["width"] for e in L.els if e["type"] in ("text", "rectangle")
                and deliv["y"] - 20 <= e["y"] <= runs["y"] + 40 and e["x"] < skills_x - 60)
    x = right + 120
    L.FRAME[0] = frame["id"]
    L.path([(runs["x"] + runs["width"] + 16, runs["y"] + 13), (x, runs["y"] + 13), (x, deliv["y"] + 13),
            (deliv["x"] + deliv["width"] + 16, deliv["y"] + 13)], dashed=True)
    y = (deliv["y"] + runs["y"]) / 2 - 90
    L.text(x + 24, y, "a Section's built output goes up to the Board's delivery/", L.z(20))
    L.text(x + 24, y + L.z(34), "delivery/jNN_<version>/tNN_<section>/latex/\n"
                                "delivery/jNN_<version>/latex/sections/tNN_<section>.tex\n"
                                "delivery/jNN_<version>/latex/master.pdf", L.z(18), L.INK, L.MONO)
    L.change_note(x + 24, y + L.z(120), NEW + "a version and a Section keep no related/, studio/ or delivery/ (JL)", 70)
    L.FRAME[0] = None


def main():
    out = HERE / "s01-paper-tree.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    saved = {k: getattr(L, k) for k in L.DENSE_S01}
    for k, v in L.DENSE_S01.items():
        setattr(L, k, v)
    try:
        frame = L.draw_ladder("1 · The paper ladder", "The paper ladder: each level, its specials, its variants",
                      "A level's node keeps its folder pattern; its specials branch to the right, each described; "
                      "related/, studio/ and reports/ open into what they hold; the box under a node holds its "
                      "definition, what shows on screen and its variants; the next level steps down and right. "
                      "Red = open; green ✎ = changed.", LAYERS, DEFINE, ON_SCREEN, SKILLS,
                      top=("Tools/", "plugins/haipipe-toolkit/skills/2_theme/paper"), layer_notes=LAYER_NOTES)
        link_back(frame)
    finally:
        for k, v in saved.items():
            setattr(L, k, v)
    canvas.write(out, list(L.els), "build_s01_paper_tree.py")


if __name__ == "__main__":
    main()
