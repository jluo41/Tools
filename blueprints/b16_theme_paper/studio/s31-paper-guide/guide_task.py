"""The paper Guide's Task section, one part of s31 (build_s31_paper_guide.py draws it).

A paper Task is a Section, a Page Task (b03 s13: a Section opens as a Page). What the four Guide Views
show at Task level: the live rows first (read by paper_guide_live.py: method.md's **Task · …** table and
method cards, guide.yaml roadmap: Task, related/papers.md rows with level Task), then the Task session's
proposal, each line a "?" (drawn red) until JL settles it. Placeholders only.

Exports LEVEL = {View: items} in s31's item kinds (c cards, w drawing cards, t line, m mono line),
ON_DISK = {View: [(line, meaning)]} and OPEN = ["? …"].
"""
import paper_guide_live as G


def _live_steps():
    return [(f"today · {t}", what, line) for t, what, line in G.steps("Task")]


# Proposed: the six Space cards of a Section's tab, in paper words (the base Page Task's, plus what the
# paper adds: the reader contract, the venue's rules, form stats, the Section's own PDF and readiness).
SPACES = [
    ("? Description", "the Section's face: its reader contract",
     "sub: Scope · Plan · Requirement   reads: t0N_<title>.md · <stem>-requirement.md   runs: Context"),
    ("Idea Studio", "the Section's logic, one drawing per topic",
     "sub: —   reads: studio/sNN-<topic>/   runs: Draw the logic"),
    ("Audience Report", "what the reader reads; its content changes through Work Details' Runs",
     "sub: Table · Reading · Questions · Comments   reads: draft/ · reports/ · the version's comments reports   runs: Ask"),
    ("Work Details", "how the Section is made: its draft and its bound evidence",
     "sub: Draft-… · Evidence-…   reads: draft/ · results/   runs: Structure · Section revise · Bind"),
    ("Runs", "the Section's soft Runs, one card each, grouped by kind",
     "sub: — (the Page Runs view: Workflow map · Page Writing · Evidence · Supporting Runs)   reads: runs/run-<type>-<slug>.md   runs: Run"),
    ("? Delivery", "its own PDF, the piece the version pulls in, ready ●●○ · CHECK ○",
     "sub: — (a preview card per kind: Web · LaTeX · Word · Slides)   runs: Build · Check"),
]

# Proposed: the Page method's six steps in paper words; where each happens; who signs.
STEPS = [
    ("? 1 · Resolve", "its row in the version face's ## Narrative + the venue's section → reader contract, V-rules",
     "where: Description › Requirement   signs: — (a stale row goes back: HOLD)"),
    ("? 2 · Plan", "paragraphs and Bullets, one role each",
     "where: Draft-Scratch   methods: By outline first   signs: a person, the plan"),
    ("? 3 · Draw the logic", "the claim left, its reasons beside it, every Bullet a row",
     "where: Idea Studio   methods: By logic tree   signs: —"),
    ("? 4 · Bind the evidence", "every value, citation and display to its Result",
     "where: Evidence-…   methods: By bound value · By provenance   signs: a person"),
    ("? 5 · Write and adopt", "one sentence per Bullet; form stats against the venue's budget",
     "where: Audience Report › Table   methods: By reader expectations   signs: a person"),
    ("? 6 · Check and build", "ready for the build (plan ✓ · previews ✓ · PDF ✓); done = Page CHECK",
     "where: Delivery   methods: By single source · By independent check   signs: CHECK"),
]

LEVEL = {
    "Description": [
        ("t", "one Section, a Page Task: it tells one Narrative row to its reader"),
        ("c", SPACES),
        ("m", "skills   haipipe-paper-section owns · haipipe-page-workflow works · workbench-paper shows"),
        ("t", "? variants: Section (Main · Appendix) · Round · Letter; only the Section is drawn yet"),
    ],
    "Method": [
        ("c", _live_steps()),
        ("t", "? proposed: the Page method's steps, in the paper's words"),
        ("c", STEPS),
        ("t", "method cards"),
        ("c", G.method_cards("Task")),
    ],
    "RoadMap Draw": [("w", G.drawings("Task"))] if G.drawings("Task") else [("t", "(no Task drawing listed yet)")],
    "Related Paper": [("c", G.papers("Task"))] if G.papers("Task") else [("t", "(no Task paper yet)")],
}

ON_DISK = {
    "Description": [
        ("servers/workbench-paper/guide/guide.yaml", ""),
        ("    levels: Task: role · spaces:", "the six card words above (proposed)"),
        ("t0N_<title>/ · t2N_<title>/", "a Section folder"),
        ("├── t0N_<title>.md", "reader-question · entry/exit-state · must-establish · story-row"),
        ("├── draft/records/<stem>-requirement.md", "V-rules (venue) · W-rules (page)"),
        ("├── draft/ · results/ · runs/", "the Page's plan, Results, soft Runs"),
        ("├── studio/sNN-<topic>/ · reports/qNN_<topic>/", "its drawings · its questions' reports"),
        ("└── delivery/latex/", "<page>-master.tex → <page>.pdf · <page>.tex"),
    ],
    "Method": [
        ("servers/workbench-paper/guide/method.md", ""),
        ("    Task · one Section, a Page", "the step cards (today one row)"),
        ("servers/workbench/task-page/guide/methods/", "the Page method's cards"),
        ("servers/workbench-paper/guide/methods/writing/", "the paper's Writing cards"),
    ],
    "RoadMap Draw": [
        ("servers/workbench-paper/guide/guide.yaml", ""),
        ("    roadmap: Task:", "one drawing card each"),
        ("Tools/blueprints/b16_theme_paper/studio/s13-paper-task/", "a Section's screens"),
    ],
    "Related Paper": [
        ("servers/workbench-paper/related/papers.md", ""),
        ("    rows with level: Task", "one paper card each"),
    ],
}

OPEN = [
    "? The Task steps: the Page method's six in paper words here, or one row pointing to the Page Guide?",
    "? One 'By reader expectations' card: keep the paper's (Gopen & Swan), the Page step points to it?",
    "? The citation file has three homes: <stem>.bib · selected-bibliography/ · delivery/latex/draft-bibliography/",
    "? A Section's question that outgrows it: does its report move to the Block's reports/?",
    "? Round and Letter Tasks: their own steps and Space cards (with Q03)",
]

CHANGES = ["Runs: the Page's own Runs view, embedded, no third row (was All · <type>, a thin table)",
           "Run names carry no date: runs/run-<type>-<slug>.md (was run-<type>-<MMDD>-<slug>)",
           "a Section folder is t0N_<title>/ · t2N_<title>/ (was S-<desk>-<Group>-<N>-<Title>/)",
           "story-row: the version face's ## Narrative row (was the Story Page's §8); comments: a report of type comments"]
