"""b14 s32 · Discovery element UI: s32-discovery-element-ui.excalidraw, the discovery theme's element gallery (b03's
s32-element-ui, cut to one theme): every kind of element the discovery theme draws, as it draws it today on the frame
(/_board/workbench at its Block, Job and Task levels, every Space and view) and on its old pages (the Discovery board
page, the Page workbench a Task opens in, the file route a Result Card opens in; flagged OLD), as b03's s11 · s12 ·
s13 plan it for discovery, and beside each element a "· proposed" frame: the unified look (b03's picks hold), why,
a green line for what changed and a red line for what is open. Then the theme's own elements, its buttons and the
Run name each one needs.

Two steps:

    uv run --no-project --with playwright --with pillow python build_s32_discovery_element_ui.py --shoot [--base http://127.0.0.1:5851]
        (--no-project: inside the SPACE, uv would otherwise build the SPACE's own environment)
        walks the discovery Block with the most on disk (SMSEngagement: 5 Jobs, 10 Tasks, 51 Paper Runs) on the
        frame and on its old pages, screenshots each element into shots/<element>__NN.png, writes its page,
        selector and computed style into shots/facts.json, and every button met (its Run name, or none) into
        facts.json's "_buttons". No discovery Block registers a Question yet, so the Question rows come from a
        small placeholder Block (written to a temp folder, rendered by the SPACE's own Python, shown on the host's
        origin); placeholders only.
    python build_s32_discovery_element_ui.py
        draws the gallery from shots/ and the planned screens from b03's level definitions (build_ladder_v4.py,
        level_views.py: the discovery rows, b14 Q01); marks are kept on rebuild (canvas.write).

The shooting and picture helpers are b03's (../../../b03_project_workbench/studio/s32-element-ui/
build_s32_element_ui.py), imported. b14 has no s11 · s12 · s13 of its own: its level designs are the discovery rows
of b03's s11-block-variants, s12-job-variants and s13-task-variants, drawn here by b03's own wireframe().
"""
from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse as UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SPACE = HERE.parents[4]
TOOLS = HERE.parents[3]
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
B03S32 = TOOLS / "blueprints" / "b03_project_workbench" / "studio" / "s32-element-ui"
sys.path.insert(0, str(B03S32))
import build_s32_element_ui as E  # noqa: E402  (b03's gallery: PICK_JS, picture, style_line; it loads L and canvas)
import level_views as LV  # noqa: E402  (b03's s11 · s12 · s13 screens; on the path E set up)

L, canvas = E.L, E.canvas
INK, GRAY, RED, GREEN, MONO = L.INK, L.GRAY, L.RED, L.GREEN, L.MONO
text, base = L.text, L.base
q = E.q
MAX_H, CARD_W = E.MAX_H, E.CARD_W

# ── where each card comes from ──────────────────────────────────────────────────────────────────────
# the discovery Block with the most on disk; its first Job; the Job's Task that has a typed record (verdict.md)
BLOCK = "examples-2-analysis/Project-ExpAnalysis-SMSEngagement/discoveries/b01_sms_engagement_evidence"
JOB = BLOCK + "/j01_smsr_literature_inquiry"
TASK = JOB + "/t03_novelty_check"
FOLDER = {"Block": BLOCK, "Job": JOB, "Task": TASK}
SPACES = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
OLD_BOARD = "/_board/discovery-board?path=" + q(BLOCK + "/board.md")
B03_FRAME = E.FRAME_URL                                        # b03's own Block on the frame (the vanilla base)


def fr(level, space, view=""):
    """A frame page of the discovery Block, at one level, Space and view."""
    return ("fr", level, space, view)


def demo(level, space, view=""):
    """A frame page of the placeholder Block (Questions registered), rendered by the SPACE's Python."""
    return ("demo", level, space, view)


def old(page, space="", view=""):
    """An old page: "board" (the Discovery board page, a Space and a view clicked open), "draft" (the Page
    workbench a Task's link opens), "card" (a Paper Run's Result Card, the file route its link opens)."""
    return ("old", page, space, view)


def frame_url(folder, space="", view=""):
    query = {"path": folder}
    if space:
        query["space"] = space
    if view:
        query["sub"] = view
    return "/_board/workbench?" + UP.urlencode(query)


def label_of(src) -> str:
    kind, a, b, c = src
    if kind == "fr":
        return f"the frame · {a} › {b}" + (f" › {c}" if c else "")
    if kind == "demo":
        return f"the frame · placeholder Block (Questions) · {a} › {b}" + (f" › {c}" if c else "")
    if kind == "b03":
        return "the frame · b03's own Block (the vanilla base)"
    if kind == "pop":
        return f"the frame · {a} › {b} › {c}: a paper row clicked, its Result Card in the pop-out"
    return {"board": f"Discovery board page › {b}" + (f" › {c}" if c else ""),
            "draft": "Page workbench page (/_board/draft), where a Task opens",
            "card": "a Paper Run's Result Card (the board page's file route)"}[a]


OLD_WHY = {"board": "old page: the discovery theme draws on the frame now; this page retires",
           "draft": "old item page: a Task row's link leaves the frame for the Page workbench",
           "card": "old route: a Result Card opens through the old board page's reader"}


def old_reason(src) -> str:
    """Why a card's page is old, read off the code; "" for the frame."""
    if src[0] != "old":
        return ""
    if src[1] == "board" and not (SERVERS / "workbench-discovery" / "discovery_theme.py").is_file():
        return ""
    return OLD_WHY[src[1]]


# ── the elements: (key, title, what, [(card source, selector)]) ──────────────────────────────────────
# a selector as b03's: "a|b" the box around both, "parent:x" x's parent, "a,b" the first found
TABS, SUBS, SPLIT, MAIN = "nav.levels|nav.spaces", "nav.subs", ".split", ".space-main"
OLDTAB, OLDVIEW = ".pane.on .wtabs", ".pane.on section.view.on"
ELEMENTS = [
    ("tabs", "1 · Top tabs", "the level row (Block · Job ▾ · Task ▾) and the six Spaces",
     [(fr("Block", "Audience Report"), TABS), (fr("Job", "Work Details"), TABS), (fr("Task", "Work Details"), TABS),
      (old("board", "Work", "Papers"), "nav.spaces"), (old("draft"), "nav.spaces,div.spaces")]),
    ("views", "2 · View row (third row)", "the views of the open Space",
     [(fr("Block", "Description"), SUBS), (fr("Block", "Audience Report"), SUBS), (fr("Block", "Work Details"), SUBS),
      (fr("Block", "Runs"), SUBS), (fr("Block", "Delivery"), SUBS), (fr("Task", "Description"), SUBS),
      (fr("Task", "Audience Report"), SUBS), (fr("Task", "Work Details"), SUBS), (fr("Task", "Runs"), SUBS),
      (fr("Task", "Delivery"), SUBS), (old("board", "Scope", "Block"), OLDTAB), (old("board", "Work", "Papers"), OLDTAB),
      (old("draft"), ".draft-mode-switcher")]),
    ("report", "3 · Audience Report rows", "one Question with its work and its report: Question │ Work │ Report",
     [(demo("Block", "Audience Report", "Questions"), ".q-head-row|.q-row:not(.q-head-row)"),
      (demo("Job", "Audience Report"), MAIN), (demo("Block", "Audience Report", "Reports"), MAIN),
      (fr("Block", "Audience Report", "Questions"), MAIN), (fr("Task", "Audience Report", "Synthesis"), MAIN),
      (old("board", "Scope", "Questions"), OLDVIEW)]),
    ("space", "4 · The Space body", "the open Space's box beside Disk · Runs, its first screen",
     [(fr(lv, sp), SPLIT) for lv in ("Block", "Job", "Task") for sp in SPACES]
     + [(old("board", s, v), ".pane.on") for s, v in (("Scope", "Block"), ("Work", "Papers"), ("Check", "Runs"),
                                                      ("Delivery", "Reports"))]
     + [(old("draft"), ".space-main,main")]),
    ("table", "5 · Tables", "rows of items in a table",
     [(fr("Block", "Description", "Block"), "table.wf-table"), (fr("Block", "Work Details", "Papers"), "table.wf-table"),
      (fr("Block", "Work Details", "Tasks"), "table.wf-table"), (fr("Block", "Runs", "All"), "table.wf-table"),
      (fr("Task", "Description", "Face"), "table.wf-table"), (fr("Task", "Runs", "All"), "table.wf-table"),
      (old("board", "Scope", "Block"), ".pane.on section.view.on table"),
      (old("board", "Work", "Papers"), ".pane.on section.view.on table"),
      (old("board", "Check", "Runs"), ".pane.on section.view.on table")]),
    ("cards", "6 · Rows and cards", "one item, closed or open",
     [(fr("Block", "Description", "Resources"), MAIN), (demo("Block", "Audience Report", "Reports"), "details.topic"),
      (fr("Task", "Audience Report", "Synthesis"), "details.topic"), (fr("Task", "Work Details", "Notes"), MAIN),
      (old("board", "Scope", "Resources"), OLDVIEW), (old("board", "Scope", "RoadMap Draw"), OLDVIEW),
      (old("board", "Check", "Reports"), OLDVIEW)]),
    ("runs", "7 · Disk · Runs panel", "the files behind the open Space, its run types and their Runs (Disk inside, one fold)",
     [(fr("Block", "Audience Report"), "section.runs-panel"), (fr("Block", "Work Details"), "section.runs-panel"),
      (fr("Job", "Work Details"), "section.runs-panel"), (fr("Task", "Runs"), "section.runs-panel"),
      (fr("Task", "Description"), "section.runs-panel"), (old("board", "Work", "Papers"), ".pane.on .runs-panel"),
      (old("draft"), ".runs-panel")]),
    ("tags", "8 · Tags and pills", "a state, an id or a count on an item",
     [(fr("Block", "Description", "Block"), "parent:.chip"), (fr("Block", "Work Details", "Papers"), "parent:td .chip"),
      (fr("Block", "Runs", "All"), "parent:td .st-ok"), (fr("Task", "Work Details", "Papers"), "parent:.st-ok"),
      (demo("Block", "Audience Report", "Questions"), "parent:.kind"),
      (demo("Block", "Audience Report", "Questions"), "parent:.rp-tags"),
      (old("board", "Work", "Papers"), "parent:.pill"), (old("board", "Work", "Tasks"), "parent:.idtag")]),
    ("header", "9 · Page header", "the title line at the top",
     [(fr("Block", "Description"), "header"), (fr("Job", "Description"), "header"), (fr("Task", "Description"), "header"),
      (old("board", "Scope", "Block"), ".dataset,header"), (old("draft"), "header,h1")]),
    ("item", "10 · One item's display", "one paper (its Result Card), one Task Page: the item itself",
     [(("pop", "Task", "Work Details", "Papers"), "dialog[open]"), (fr("Task", "Description", "Face"), MAIN),
      (old("card"), "main,body"), (old("draft"), ".space-main,main")]),
    # the discovery theme's own elements
    ("papers", "11 · Paper rows (discovery only)", "one Paper Run per row: the paper, its readout, its source, how deep it "
     "was read, whether its citation is verified, its state",
     [(fr("Task", "Work Details", "Papers"), "table.wf-table"), (fr("Block", "Work Details", "Papers"), MAIN),
      (fr("Block", "Work Details", "Citations"), MAIN), (old("board", "Work", "Papers"), OLDVIEW),
      (old("board", "Check", "Citations"), OLDVIEW)]),
    ("tasks", "12 · Sub-question rows (discovery only)", "one Task per row: its type, its Runs, what waits on a person, "
     "its synthesis",
     [(fr("Job", "Work Details"), MAIN), (fr("Block", "Work Details", "Tasks"), MAIN), (old("board", "Work", "Tasks"), OLDVIEW)]),
    ("synthesis", "13 · Synthesis (discovery only)", "a Task's answer: its typed record (summary · verdict · landscape) and "
     "its article",
     [(fr("Task", "Audience Report", "Synthesis"), MAIN), (fr("Task", "Audience Report", "Draft"), MAIN),
      (fr("Block", "Delivery", "Reports"), MAIN), (demo("Block", "Delivery", "Reports"), MAIN),
      (old("board", "Delivery", "Reports"), OLDVIEW)]),
    ("bib", "14 · BibTeX (discovery only)", "the Bib entries the Paper Runs wrote, merged upward",
     [(fr("Block", "Delivery", "BibTeX"), MAIN), (fr("Task", "Delivery", "Files"), MAIN), (fr("Job", "Delivery"), MAIN),
      (old("board", "Delivery", "BibTeX"), OLDVIEW)]),
    ("scope", "15 · Scope and resources (discovery only)", "what the Block or Task asks, where it searches, its "
     "admission rule",
     [(fr("Block", "Description", "Block"), MAIN), (fr("Block", "Description", "Resources"), MAIN),
      (fr("Task", "Description", "Face"), MAIN), (fr("Task", "Description", "Folder"), MAIN), (fr("Job", "Description"), MAIN),
      (old("board", "Scope", "Block"), OLDVIEW), (old("board", "Scope", "Resources"), OLDVIEW)]),
    ("intake", "16 · Intake: screened candidates (discovery only)", "the candidates a search returned, each admitted, "
     "excluded or unresolved (discovery.yaml candidate_decisions)", []),
]

# ── as b03's s11 · s12 · s13 plan it for discovery: (level, key), drawn by b03's own wireframe() ───────
# Block keys are s11's columns (Scope · Resources · Studio · Reports · Jobs · Runs · Delivery); Job keys its Spaces;
# Task keys s13's screens or the groups of its Audience Report and Work Details (Table · Reading · Papers · Intake · Draft)
PLANNED = {
    "tabs": [("Task", "Papers")],
    "views": [("Job", "Work Details")],
    "report": [("Block", "Reports"), ("Job", "Audience Report"), ("Task", "Table")],
    "space": [("Job", "Description")],
    "table": [("Block", "Runs")],
    "cards": [("Block", "Jobs")],
    "runs": [("Task", "Runs")],
    "item": [("Task", "Papers")],
    "papers": [("Task", "Papers")],
    "tasks": [("Job", "Work Details"), ("Block", "Jobs")],
    "synthesis": [("Task", "Reading"), ("Task", "Table")],
    "bib": [("Task", "Delivery"), ("Block", "Delivery"), ("Job", "Delivery")],
    "scope": [("Block", "Resources"), ("Task", "Description"), ("Job", "Description")],
    "intake": [("Task", "Intake")],
}

# ── the proposed look: (source, selector, why, changed (green), open (red)) ───────────────────────────
# b03's picks hold (s32-D01 tabs D · E, D02 view row E, D05 the Question cell as Insight's row, D08 Disk inside
# the Runs panel, D09 no tags); where the frame already draws the look, its own version is the proposal
PROPOSALS = {
    "tabs": (fr("Task", "Work Details"), TABS,
             ["b03's D · E look (s32-D01), drawn by the base: discovery gives the words only",
              "Block · Job ▾ · Task ▾, then the six Spaces, the same at every level"],
             "kept: the frame's D · E tabs (b03 s32-D01)",
             "? the Job and Task selects read folder names (j01_smsr_literature_inquiry); a short label "
             "'j01 · <inquiry>' through the base's option() hook (b03, 261008)"),
    "views": (fr("Task", "Work Details"), SUBS,
              ["b03's E look (s32-D02): the tabs' shape, one family",
               "the views s11 · s12 · s13 plan, in their order, on this one row"],
              "kept: the frame's E view row (b03 s32-D02)",
              "? the Job draws no third row at all; s12 plans Description: Inquiry · Resources, Work Details: All · "
              "Search · Review · Synthesize, Runs: All · plan · delivery · from below"),
    "report": (("b03", "", "", ""), ".q-head-row|.q-row:not(.q-head-row)",
               ["one Question │ Work │ Report row per Question, as every theme (b03 s04-D04)",
                "the Question cell as the Insight row: label and state dot, short name, one sentence, › More",
                "the Work cell: the Tasks that answer it and the papers they read (r01 · r02)"],
               "changed: the Question cell as Insight's (b03 s32-D05)",
               "? discovery_theme._questions draws its own older cell (a Q01 tag, the whole question, the hypothesis); "
               "use the base's question_cell(); no discovery Block registers a Question yet"),
    "space": (fr("Job", "Work Details"), SPLIT,
              ["one content box and one right column, Disk · Runs", "discovery fills the box; it draws no page of its own"],
              "kept: the frame's body, every level",
              "? Job › Description is empty (no jNN_<inquiry>.md face on disk); Job › Delivery and Idea Studio are "
              "empty at every level of this Block"),
    "table": (fr("Task", "Runs", "All"), "table.wf-table",
              ["the frame's light table: small grey heads, rows ruled by one line",
               "an item with a body (a paper's readout) is a row (6) that folds open, not a tall cell"],
              "kept: the frame's table",
              "? the Papers table puts a 220-character readout under each title, so one row is 3-4 lines"),
    "cards": (fr("Task", "Audience Report", "Synthesis"), "details.topic",
              ["one closed row per item: ▸ name · its facts, opened in place (Idea Studio's topic rows)",
               "the same row for a resource, a report, a synthesis, a note"],
              "kept: the frame's folding row",
              "? an opened synthesis or note shows its raw markdown in a pre (space-source), not the Page reader"),
    "runs": (fr("Task", "Runs"), "section.runs-panel",
             ["Disk, then Runs, one panel, one fold (b03 s32-D08)",
              "one row per run type, named run-<type>-<target>; a hard Paper Run keeps rNN_<author><year>_<subject>"],
             "kept: Disk inside Runs, the theme's buttons named by RUN_NAMES",
             "? Task › Audience Report offers 'Synthesize a Task' from the Block's Tasks view; s13 plans Synthesize · "
             "Section revise there, and Scope the Task · Freeze the rule in Description"),
    "tags": (("none", "", "", ""), "",
             ["none: no tags in any theme (b03 s32-D09)", "a state is a word (complete · blocked · to verify)",
              "an id is plain text where it stands (j01 t03, r02_keller2025_adherencecomm, Q01)"],
             "changed: no tags (b03 s32-D09)",
             "? to change in discovery_theme.py: {n} kinds drawn today (chip for Job, Task and Run ids; kind for a "
             "Question id; st-ok / st-warn for a state; rp-tags)"),
    "header": (fr("Job", "Description"), "header",
               ["one line: 🔭 Discovery · the folder; the path on hover", "no dataset band, no counts line above the tabs"],
               "kept: one line, no band (the old board's dataset band retires)", ""),
    "item": (("pop", "Task", "Work Details", "Papers"), "dialog[open]",
             ["a paper opens in the frame's pop-out from its row: its Result Card, facts, Bib entry",
              "a Task opens as its own level (the Task tab), never the Page workbench page"],
             "proposed: a Result Card in the pop-out, read by the base reader (/_board/page)",
             "? today the pop-out loads the old board page's file route (/_board/discovery-board?show=…); the old "
             "board's Task link opens /_board/draft"),
    "papers": (fr("Task", "Work Details", "Papers"), "table.wf-table",
               ["one row per Paper Run: the paper, the source, how deep it was read, the citation's state, its state",
                "the readout folds under the row; the Run id is plain mono text, not a chip"],
               "kept: the base table, one row per Paper Run",
               "? s13 plans paper · depth · claim · cite and papers grouped by role (b14 Q02); today 7 columns, "
               "ids as chips, no claim column"),
    "tasks": (fr("Job", "Work Details"), "table.wf-table",
              ["one row per sub-question Task, folding open to its papers (s12)",
               "grouped by the specialist that runs it: Search · Review · Synthesize"],
              "kept: the base table",
              "? s12 plans ▾ t01 … r01 · r02 (a Task opening to its papers) and the third row by specialist; today a "
              "flat table with a Job chip and a Findings column"),
    "synthesis": (fr("Task", "Audience Report", "Synthesis"), MAIN,
                  ["a Task's answer is a Page: Table (one row per division: ask │ papers read │ state) and Reading (s13)",
                   "the typed record (summary · verdict · landscape) is a fold under the Table, read by the Page reader"],
                  "kept: the typed record in one fold",
                  "? s13 plans Table · Reading; today Synthesis (raw verdict.md) · Draft (the base's Page view); Block › "
                  "Delivery › Reports shows only answered reports, so this Block's is empty"),
    "bib": (fr("Block", "Delivery", "BibTeX"), MAIN,
            ["the Bib is a Delivery card: tNN_<task>.bib at the Task, merged at the Job and the Block (s11 · s13)",
             "its entries in one mono block, one link per Run's .bib"],
            "kept: one block of entries, its files above it",
            "? the Task's Delivery (Files · Lanes) and the Job's Delivery show no Bib; s13 plans an Article card and an "
            "Export card (tNN_<task>.bib)"),
    "scope": (fr("Block", "Description", "Block"), "table.wf-table",
              ["the Block's facts as a two-column base table (state · spine · close · jobs · reading)",
               "a resource is a folding row; a Task's Scope · Admission · Records come from discovery.yaml (s13)"],
              "kept: the base table and folding rows",
              "? s13's Task Description › Scope · Admission · Records is not drawn (today the base's Face · Folder); "
              "s12's Job › Inquiry needs a jNN_<inquiry>.md face"),
    "intake": (("none", "", "", ""), "",
               ["screened candidates beside Papers (s13 Task › Work Details › Intake): candidate · disposition · why",
                "from discovery.yaml's candidate_decisions; an admitted one links to its Paper Run"],
               "proposed: a base table under Work Details › Intake",
               "? not drawn at any level today; the candidates sit in results/search/ (s01 Open 4)"),
}

# what the discovery theme draws, by level (asked by b03 for JL: "which element UI each level uses")
# (element, level, Space › view, base or its own and why, drawn today ("" yes) or the gap)
THEME_ELEMENTS = [
    ("top tabs", "every level", "the level row and the six Spaces", "the base", "",),
    ("view row", "Block · Task", "every Space with views", "the base", "GAP: the Job draws no third row (s12 plans "
     "Inquiry · Resources, All · Search · Review · Synthesize, All · plan · delivery · from below)"),
    ("Question rows", "Block · Job", "Audience Report › Questions; Job › Audience Report", "the base (Insight's row)",
     "GAP: its own older cell (_questions); no Block on disk registers a Question"),
    ("Question rows (divisions)", "Task", "Audience Report › Table", "the base row: division │ papers read │ state (s13)",
     "GAP: not drawn; today Synthesis · Draft"),
    ("Reports folds", "Block", "Audience Report › Reports", "the base folding row", ""),
    ("Space body + Disk · Runs", "every level", "every Space", "the base", ""),
    ("table", "every level", "Block facts, Papers, Tasks, Citations, Runs, Task Face", "the base", ""),
    ("folding row", "Block · Task", "Resources, Reports, Synthesis, Notes", "the base row",
     "GAP: an open fold shows raw markdown, not the reader"),
    ("Runs panel", "every level", "every Space", "the base; run types from the Workbench Table, named by RUN_NAMES", ""),
    ("tags", "every level", "Job, Task and Run ids; Question id; state", "none (b03 s32-D09)",
     "GAP: chip · kind · st-ok · st-warn · rp-tags drawn"),
    ("header", "every level", "the top line", "the base", ""),
    ("paper row", "Block · Task", "Work Details › Papers, Citations", "its own: a Paper Run is read by depth, claim "
     "and citation, which no other theme has", "GAP: s13's paper · depth · claim · cite and roles (Q02) not drawn"),
    ("Result Card", "Task (pop-out)", "a paper row's link", "its own: one Paper Run's card, facts and Bib entry",
     "GAP: opens through the old board's file route"),
    ("sub-question row", "Block · Job", "Work Details › Tasks; Job › Work Details", "the base table, discovery's "
     "columns (type · Runs · to verify · synthesis)", "GAP: s12's fold-open to papers and the specialist row"),
    ("synthesis", "Task", "Audience Report › Synthesis", "its own: the typed record (summary · verdict · landscape)",
     "GAP: s13's Table · Reading not drawn"),
    ("BibTeX", "Block (Task · Job planned)", "Delivery › BibTeX", "its own: the merged Evidence Bib",
     "GAP: Task and Job Delivery show no Bib"),
    ("Scope · Admission · Records", "Task", "Description", "its own: discovery.yaml's question, type and rule",
     "GAP: today the base's Face · Folder"),
    ("Inquiry face", "Job", "Description › Inquiry", "its own: jNN_<inquiry>.md (s12)", "GAP: empty (no face on disk)"),
    ("Intake", "Task", "Work Details › Intake", "the base table: screened candidates (s13)", "GAP: not drawn"),
    ("Idea Studio", "every level", "Idea Studio", "the base (b03 s32-D06)", "drawn (no studio/ in this Block)"),
    ("the Discovery board page", "(old)", "/_board/discovery-board", "retires: the frame draws every level", "old page"),
    ("the Page workbench page", "(old)", "/_board/draft, from a Task link", "retires: a Task is the Task tab", "old page"),
]

# each discovery button and its Run (haipipe-run rule 6: every soft Run button named run-<type>-<target>); the
# names discovery_theme.RUN_NAMES and the base give are read off the code; these are the proposals for the rest
# b03's ruling (261008): a button the base already names keeps that name in every theme; a theme's own
# button takes a name of its own (here: add-paper, freeze-admission, admit); a target is the folder's number
PROPOSED_NAMES = {
    "Add a paper": "run-add-paper-<key>", "Open a Job": "run-add-<jNN>", "Update the inquiry": "run-face-<jNN>",
    "Plan its Tasks": "run-plan-<tNN>", "Add a Task": "run-add-<tNN>", "Check a Task": "run-check-<tNN>",
    "Scope the Task": "run-face-<tNN>", "Freeze the rule": "run-freeze-admission-<tNN>",
    "Admit a candidate": "run-admit-<candidate>", "Structure revise": "run-structure-<slug>",
    "Section revise": "run-section-<slug>", "Build the article": "run-delivery-<target>",
    "Export BibTeX": "run-delivery-<target>", "Build a delivery": "run-delivery-<target>",
    "Save resource": "run-add-resource-<slug>", "+ Add drawing": "run-draw-<sNN>", "Draw": "run-draw-<sNN>",
    "Rerun": "rNN_<author><year>_<subject> (a new pass of the hard Run)",
    "+ New Run": "none: it asks for a run type, then takes that type's name",
}
BASE_NAMES = {"Draw": "run-draw-<sNN>", "Build a delivery": "run-delivery-<target>",
              "update the description": "run-face-<target>"}     # what the frame names for every theme


def theme_run_names() -> dict:
    """discovery_theme.RUN_NAMES, read off the code (no import: it needs the host's paths)."""
    src = (SERVERS / "workbench-discovery" / "discovery_theme.py").read_text(encoding="utf-8")
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "RUN_NAMES" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def planned_buttons() -> dict:
    """{button: [where]} of every run button b03's s11 · s12 · s13 discovery rows draw."""
    out = {}
    for key, spec in L.VIEW_FAMILY["discovery"].items():
        for b in spec[1]:
            out.setdefault(b, []).append(f"s11 Block › {key}")
    for key, spec in LV.JOB_FAMILY_VIEWS["discovery"].items():
        for b in spec[1]:
            out.setdefault(b, []).append(f"s12 Job › {key}")
    for key, spec in LV.TASK_VARIANT_VIEWS["discovery Task"].items():
        for b in spec[1]:
            out.setdefault(b, []).append(f"s13 Task › {key}")
    return out


CHANGES = ["new topic: the discovery theme's element gallery, after b03's s32 (b03's picks hold)",
           "the ladder shot live from SMSEngagement's discovery Block (Block · j01 · t03), the old board and item pages "
           "flagged OLD",
           "Question rows from a placeholder Block (none on disk registers one), rendered by the SPACE's Python",
           "b03's s11 · s12 · s13 discovery rows drawn as the planned screens, by b03's own wireframe()",
           "Theme elements and Run names frames: what each level uses, the gaps and each unnamed button in red",
           "b03's ruling: a button the base names keeps its name (run-add, run-plan, run-check, run-face, "
           "run-structure, run-section, run-delivery); only add-paper, freeze-admission, admit are discovery's own"]
PICKED = {"tabs": "D · E (b03 s32-D01)", "views": "E (b03 s32-D02)", "report": "the Question cell as Insight's (b03 s32-D05)",
          "runs": "Disk inside the Runs panel (b03 s32-D08)", "tags": "none (b03 s32-D09)"}


# ── shooting ────────────────────────────────────────────────────────────────────────────────────────
DEMO_PY = r"""
import json, sys, tempfile
from pathlib import Path
T, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(T / "_host"))
from host_paths import bootstrap; bootstrap()
from live import frame
from live.discovery_theme import THEME
def w(p, t):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(t, encoding="utf-8")
root = Path(tempfile.mkdtemp()).resolve()
b = root / "examples-x/Project-Demo/discoveries/b01_topic"
w(b / "board.md", "# A topic\nboard-kind: discovery-block\nstate: open\nspine: Papers on a topic.\n"
  "close: Each Task has a synthesis.\n\n## Questions\n\n```yaml\nquestions:\n- id: Q01\n  title: Which method works\n"
  "  question: Which method works best on the topic? And why.\n  hypothesis: Method A, by its prior.\n  work:\n"
  "  - j01_methods/t01_survey\n  report: reports/q01_method/q01_method.md\n- id: Q02\n  title: Where they differ\n"
  "  question: Where do the two families of methods differ?\n  work: []\n```\n")
w(b / "reports/q01_method/q01_method.md", "# Q01 · Which method works\n\nanswer-status: answered\n\n## Answer\n\n"
  "Method A, in 4 of 6 papers.\n\n## Next\n\nRead two more.\n")
t = b / "j01_methods/t01_survey"
w(t / "t01_survey.md", "---\nfolder-kind: discovery\n---\n# A survey\n\n## Opening\n\nWhy.\n")
w(t / "discovery.yaml", "version: 6\nkind: discovery\ndiscovery_type: topic-summary\njob:\n  title: \"Methods\"\n")
w(t / "summary.md", "# Summary\n\nThe placeholder synthesis.\n")
for n, (nm, st, v) in enumerate([("r01_one2024_a", "complete", "VERIFIED"), ("r02_two2025_b", "blocked", "NEEDS-VERIFICATION")], 1):
    w(t / "runs" / f"{nm}.sh", "#!/usr/bin/env bash\necho read\n")
    r = t / "results" / nm
    w(r / f"{nm}.md", f"# Paper {n}\n\n- run: {nm}\n- cite: @{nm}\n- subject: https://example.org/{nm}\n"
      f"- verification: {v}\n\n## Readout\n\nOne clear thing.\n")
    w(r / "runtime.yaml", f"run: {nm}\nfamily: discovery\nstatus: {st}\nsubject:\n  kind: paper\n  title: \"Paper {n}\"\n"
      "analysis:\n  reading_depth: full-text\n")
    w(r / f"{nm}.bib", f"@article{{{nm},\n  title = {{Paper {n}}}\n}}\n")
levels = {"Block": b, "Job": b / "j01_methods", "Task": t}
for name, (level, space, view) in json.loads(sys.argv[3]).items():
    (out / f"{name}.html").write_text(frame.render(THEME, root, levels[level], space, view), encoding="utf-8")
"""
UNFOLD = "document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))"
BUTTONS_JS = """() => ({types: [...document.querySelectorAll('.run-type[data-type]')].map(b => {
    const n = b.querySelector('.run-name'), d = b.querySelector('.run-doing');
    return [(n ? n.textContent : b.getAttribute('data-label') || b.textContent.replace(/\\s*\\d+$/, '')).trim(),
            d ? d.textContent.trim() : ''] }),
  body: [...document.querySelectorAll('.space-main button, .run-card button')]
          .filter(b => !b.closest('.wtabs, nav, .draft-mode-switcher, [role=tablist]') && !b.classList.contains('wtab'))
          .map(b => b.textContent.trim()).filter(t => t && t.length < 40)})"""


def demo_key(src) -> str:
    return "demo-" + "-".join(s.replace(" ", "_") for s in src[1:] if s)


class Shooter:
    def __init__(self, page, base_url, demos):
        self.page, self.base, self.demos = page, base_url, demos
        self.facts, self.missing, self.buttons = {}, [], {}
        self.at = None                                   # the source the page shows now
        self.urls = {}                                   # the old item pages, found on their board

    def snap(self, box, path):
        """Screenshot a box in page coordinates: scroll it to the top, clip in the viewport (a full-page shot
        resizes the viewport, and the frame's 100vh boxes move under it)."""
        top = self.page.evaluate("y => { window.scrollTo(0, Math.max(0, y - 8)); return window.scrollY; }", box["y"])
        self.page.wait_for_timeout(120)
        clip = {"x": max(box["x"], 0), "y": max(box["y"] - top, 0),
                "width": max(min(box["w"], 1490 - max(box["x"], 0)), 1), "height": min(max(box["h"], 1), MAX_H)}
        self.page.screenshot(path=str(path), clip=clip)

    def note_buttons(self, where):
        try:
            got = self.page.evaluate(BUTTONS_JS)
        except Exception:                                # the page moved on under us (a late redirect): skip it
            return
        for name, doing in got["types"]:
            self.buttons.setdefault(name, {"doing": doing, "where": []})
            if where not in self.buttons[name]["where"]:
                self.buttons[name]["where"].append(where)
        for b in got["body"]:
            self.buttons.setdefault(b, {"doing": "", "where": []})
            if where + " (body)" not in self.buttons[b]["where"]:
                self.buttons[b]["where"].append(where + " (body)")

    def goto(self, src) -> bool:
        if self.at == src:
            return True
        kind = src[0]
        try:
            if kind in ("fr", "pop"):
                resp = self.page.goto(self.base + frame_url(FOLDER[src[1]], src[2], src[3]), timeout=90000)
                ok = bool(resp and resp.status == 200)
                self.page.wait_for_timeout(500)
                if kind == "pop" and ok:                 # open the first paper's Result Card in the pop-out
                    ok = self.page.evaluate("() => { const a = document.querySelector('.space-main table a[data-pop]');"
                                            " if (a) a.click(); return !!a; }")
                    self.page.wait_for_timeout(1500)
            elif kind == "b03":
                resp = self.page.goto(self.base + B03_FRAME + "&space=Audience+Report", timeout=90000)
                ok = bool(resp and resp.status == 200)
            elif kind == "demo":
                html = self.demos.get(demo_key(src))
                if html is None:
                    self.missing.append(f"{label_of(src)}: no placeholder page")
                    return False
                self.page.goto(self.base + frame_url(BLOCK), timeout=90000)   # the host's origin, so links resolve
                self.page.set_content(html, wait_until="load")
                ok = True
            elif src[1] == "board":
                if not (self.at and self.at[:2] == ("old", "board")):
                    resp = self.page.goto(self.base + OLD_BOARD, timeout=90000)
                    if not resp or resp.status != 200:
                        self.missing.append(f"old board: HTTP {resp.status if resp else '?'}")
                        return False
                    self.page.wait_for_timeout(1200)
                ok = self.page.evaluate("""([s, v]) => {
                    const sp = [...document.querySelectorAll('nav.spaces button.space')].find(b => b.textContent.trim() === s);
                    if (!sp) return false; sp.click();
                    const tab = [...document.querySelectorAll('.pane.on button.wtab')].find(b => b.textContent.trim() === v);
                    if (tab) tab.click(); return !!tab || !v; }""", [src[2], src[3]])
            else:                                        # an old item page, found as its board links to it
                url = self.urls.get(src[1])
                if url is None:
                    self.goto(old("board", "Work", "Tasks") if src[1] == "draft" else fr("Task", "Work Details", "Papers"))
                    css = ("a[href^='/_board/draft'][href*='t03_novelty_check'],a[href^='/_board/draft']" if src[1] == "draft"
                           else ".space-main table a[data-pop]")
                    url = self.page.evaluate("c => { for (const s of c.split(',')) { const a = document.querySelector(s);"
                                             " if (a) return a.getAttribute('href'); } return ''; }", css)
                    self.urls[src[1]] = url
                if not url:
                    self.missing.append(f"{label_of(src)}: no link to it")
                    return False
                resp = self.page.goto(self.base + url, timeout=90000)
                ok = bool(resp and resp.status == 200)
                self.page.wait_for_timeout(800)
        except Exception as err:                         # a slow or busy host: skip this card, say so
            self.missing.append(f"{label_of(src)}: {type(err).__name__}")
            self.at = None
            return False
        self.page.evaluate(UNFOLD)
        self.page.wait_for_timeout(200)
        self.at = src
        if ok and (kind == "fr" or src[:2] == ("old", "board")):
            self.note_buttons(label_of(src))   # the frame's and the old board's; a Page workbench's are the Page's
        return ok

    def grab(self, src, sel, out, label):
        if not self.goto(src):
            self.missing.append(f"{out}: {label} not on screen")
            return
        box = None
        for alt in sel.split(","):
            box = self.page.evaluate(E.PICK_JS, alt.strip())
            if box:
                break
        if not box:
            self.missing.append(f"{out}: {sel} not found on {label}")
            return
        try:
            self.snap(box, SHOTS / f"{out}.png")
        except Exception as err:
            self.missing.append(f"{out}: {str(err).splitlines()[0]}")
            return
        self.facts[out] = {"page": label, "src": list(src), "selector": sel, "cut": box["h"] > MAX_H, **box["style"]}


def render_demos() -> dict:
    """{demo key: HTML} of every placeholder page the cards and proposals ask for."""
    want = {demo_key(src): list(src[1:]) for _, _, _, cards in ELEMENTS for src, _ in cards if src[0] == "demo"}
    tmp = Path(tempfile.mkdtemp(prefix="s32-discovery-demo-"))
    try:
        done = subprocess.run([str(SPACE / ".venv" / "bin" / "python"), "-c", DEMO_PY, str(SERVERS), str(tmp),
                               json.dumps(want)], capture_output=True, text=True)
        if done.returncode:
            print("placeholder Block:", (done.stderr or "").strip().splitlines()[-1:] or "failed")
        return {p.stem: p.read_text(encoding="utf-8") for p in tmp.glob("*.html")}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def shoot(base_url: str) -> None:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    for f in SHOTS.glob("*.png"):
        f.unlink()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
        s = Shooter(page, base_url, render_demos())
        for ekey, _, _, cards in ELEMENTS:
            for i, (src, sel) in enumerate(cards):
                s.grab(src, sel, f"{ekey}__{i:02d}", label_of(src))
        for ekey, (src, sel, *_) in PROPOSALS.items():
            if src[0] != "none":
                s.grab(src, sel, f"proposed__{ekey}", "proposed")
        for lv in ("Block", "Job", "Task"):              # every Space and view, for its buttons
            for sp in SPACES:
                s.goto(fr(lv, sp))
                for v in page.evaluate("[...document.querySelectorAll('nav.subs a')].map(a => a.textContent)")[1:]:
                    s.goto(fr(lv, sp, v))
        for sp, views in (("Scope", ["Block", "Questions", "Resources", "RoadMap Draw"]), ("Work", ["Papers", "Tasks", "Questions"]),
                          ("Check", ["Runs", "Citations", "Reports"]), ("Delivery", ["Reports", "BibTeX"])):
            for v in views:
                s.goto(old("board", sp, v))
        browser.close()
    s.facts["_buttons"] = s.buttons
    (SHOTS / "facts.json").write_text(json.dumps(s.facts, indent=1, ensure_ascii=False))
    print(f"{len(s.facts) - 1} shots in {SHOTS.relative_to(HERE.parent)}, {len(s.buttons)} buttons met")
    for m in s.missing:
        print("  not shot:", m)


# ── the planned screens (b03's s11 · s12 · s13 discovery rows, drawn by b03's wireframe) ───────────────
TV = "discovery Task"


def planned_screen(level, key, x, y) -> float:
    """One planned screen at (x, y) from b03's discovery definitions; returns its height."""
    if level == "Block":
        _, space, view = next(c for c in L.BLOCK_COLUMNS if c[0] == key)
        spec = L.VIEW_FAMILY["discovery"].get(key) or L.VIEW_DEFAULT[key]
        lines = [ln.replace("{kind}", L.KIND["discovery"]) if isinstance(ln, str) else ln for ln in spec[0]]
        opened = view or ("j1N" if key == "Jobs" else None)
        body = {"Studio": "studio", "Reports": "qwr", "Runs": "table"}.get(key, "lines")
        sp = ("discovery", "Block", None, space, opened, body, "", L.FAMILY_CAPTIONS.get(("discovery", key), ""))
        head = f"discovery Block · Block › {space}" + (f" › {view}" if view else "")
        return L.wireframe(x, y, sp, lines=lines, runs=spec[1], pick=spec[2] if len(spec) > 2 else None, header=head) - y
    if level == "Job":
        spec = LV.JOB_FAMILY_VIEWS["discovery"][key]
        tup = bool(spec[0]) and isinstance(spec[0][0], tuple)
        body = "studio" if key == "Idea Studio" and tup else "table" if tup else "lines"
        row = LV.DISCOVERY_ROWS.get(key) or None
        opened = row[0] if row else None
        sp = ("discovery", "Job", "discovery Job", key, opened, body, "", LV.DISCOVERY_NOTES.get(key, ""))
        head = f"discovery Job · Job › {key}" + (f" › {opened}" if row else "")
        return L.wireframe(x, y, sp, lines=spec[0], runs=spec[1], pick=spec[2] if len(spec) > 2 else None,
                           header=head, groups=row) - y
    space = group = row = None                          # Task: a group of Audience Report or Work Details, or a Space
    for sp_name, groups in (("Audience Report", LV.REPORT_GROUPS[TV]), ("Work Details", LV.WORK_GROUPS[TV])):
        if key in groups:
            space, group, row = sp_name, key, groups
    if space is None:
        space, group, _, row = next(s for s in LV.task_screens(TV) if s[2] == key)
    spec = LV.TASK_VARIANT_VIEWS[TV].get(key) or LV.TASK_DEFAULT.get(key) or ([key, "(to fill)"], ["—"])
    tup = bool(spec[0]) and isinstance(spec[0][0], tuple)
    body = "studio" if key == "Idea Studio" else "table" if key == "Table" else "qwr" if tup else "lines"
    if key == "Delivery":
        row = []                                         # no third row: groups are headings over cards
    sp = ("discovery", "Task", TV, space, group, body, "", "")
    head = f"discovery Task · Task › {space}" + (f" › {group}" if group else "")
    bottom = L.wireframe(x, y, sp, lines=spec[0], runs=spec[1], pick=spec[2] if len(spec) > 2 else None, header=head,
                         groups=row, wrap=True)
    if key == "Delivery":
        LV.cards(x + 12, y + 24 + 80, LV.DELIVERY_CARDS[TV])
    return bottom - y


# ── the drawing ─────────────────────────────────────────────────────────────────────────────────────
def card(x, y, letter, src, f, path) -> float:
    """One version: where it is, its picture, its style line; an old one flagged OLD, red dashed. Its height."""
    why = old_reason(src)
    if why:
        text(x, y - 26, "OLD · " + why, 14, RED)
    text(x, y, f"{letter} · {label_of(src)}", 20, GRAY if why else INK)
    h = E.picture(path, x, y + 40, CARD_W)
    if why:
        base("rectangle", x - 8, y + 32, E.LAST_W[0] + 16, h + 16, RED, 1.5, dashed=True, rough=0)
    text(x, y + 52 + h, E.style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 11, GRAY, MONO)
    return 52 + h + 60


def frame_element(ekey, title, what, cards, x0, y0, facts, per_row=3) -> dict:
    fr_ = L.open_frame(title)
    text(x0, y0, title, 34)
    shown = [(i, src) for i, (src, _) in enumerate(cards) if (SHOTS / f"{ekey}__{i:02d}.png").exists()]
    olds = sum(bool(old_reason(src)) for _, src in shown)
    text(x0, y0 + 50, f"{what}\n{len(shown)} versions today, {olds} of them on old pages (flagged OLD: they retire; "
                      "a look from one may still be picked); then as s11 · s12 · s13 plan it", 18, GRAY)
    x, y, row_h = x0, y0 + 150, 0
    for n, (i, src) in enumerate(shown):
        if n and n % per_row == 0:
            x, y, row_h = x0, y + row_h + 110, 0
        row_h = max(row_h, card(x, y, chr(65 + n) if n < 26 else "A" + chr(39 + n), src,
                                facts.get(f"{ekey}__{i:02d}", {}), SHOTS / f"{ekey}__{i:02d}.png"))
        x += CARD_W + 80
    if not cards:
        text(x0, y, "? none today: the discovery theme draws this nowhere yet", 22, RED)
        row_h = 40
    elif not shown:
        text(x0, y, "? no shots yet: run with --shoot", 18, RED)
        row_h = 40
    gone = [label_of(src) for i, (src, _) in enumerate(cards) if not (SHOTS / f"{ekey}__{i:02d}.png").exists()]
    y += row_h + 40
    if gone and shown:
        text(x0, y, "? not on the page today: " + " · ".join(gone), 16, RED)
        y += 40
    planned = PLANNED.get(ekey, [])
    if planned:
        text(x0, y + 20, "as planned · b03's s11 · s12 · s13 discovery rows, the same screen as there (black lines, "
                         "not served yet)", 22)
        px = x0
        for k, (level, key) in enumerate(planned):
            text(px, y + 70, f"P{k + 1} · s1{'123'['Block Job Task'.split().index(level)]} · {level} › {key}", 20)
            planned_screen(level, key, px, y + 110)
            px += L.UI_W + 120
    L.close_frame(fr_)
    return fr_


def frame_proposed(ekey, title, x0, y0, facts) -> dict:
    fr_ = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    src, _, why, changed, open_ = PROPOSALS[ekey]
    n_tags = len({facts[k].get("tag") for k in facts if k.startswith("tags__") and not old_reason(facts[k].get("src", ["fr"]))})
    open_ = open_.replace("{n}", str(n_tags))
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench); the discovery theme gives the "
                      "words and, for its own elements, the columns", 18, GRAY)
    y = y0 + 110
    L.els.append(canvas.change_note(x0, y, changed, "261008", L.FRAME[0], 20))   # green: what changed (or is kept)
    y += 40
    if open_:
        text(x0, y, open_, 18, RED)                     # red: still open
        y += 40
    shot = SHOTS / f"proposed__{ekey}.png"
    if shot.exists():
        h = E.picture(shot, x0, y, 1000)
        text(x0, y + h + 12, E.style_line(facts.get(f"proposed__{ekey}", {})), 14, GRAY, MONO)
        y += h + 70
    elif src[0] == "none":
        text(x0, y, "(none today)", 28, GRAY)
        y += 60
    else:
        text(x0, y, "? no shot yet: run with --shoot", 18, RED)
        y += 40
    text(x0, y + 10, "why", 22)
    for i, line in enumerate(why):
        text(x0 + 20, y + 50 + i * 30, "· " + line, 17)
    L.close_frame(fr_)
    return fr_


def frame_title(x0, y0, facts) -> dict:
    fr_ = L.open_frame("s32 · Discovery element UI")
    text(x0, y0, "s32 · Discovery element UI: every element the discovery theme draws, today and as planned", 40)
    n = sum(1 for k in facts if "__" in k and not k.startswith("proposed__"))
    olds = sum(1 for k, f in facts.items() if "__" in k and not k.startswith("proposed__") and old_reason(f.get("src", ["fr"])))
    text(x0, y0 + 60, f"after b03's s32-element-ui; {n} versions today ({olds} on old pages), one frame per element (a card "
                      "per version, then the planned screen from s11 · s12 · s13), its '· proposed' frame to the right; "
                      "OLD = an old page, red dashed", 20, GRAY)
    for k, c in enumerate(CHANGES):
        L.els.append(canvas.change_note(x0, y0 + 120 + k * 30, c, "261008", L.FRAME[0], 18))
    L.close_frame(fr_)
    return fr_


def frame_theme_elements(x0, y0) -> dict:
    fr_ = L.open_frame("Theme elements")
    text(x0, y0, "Theme elements: what the discovery theme uses, by level", 34)
    text(x0, y0 + 50, "element · level · Space › view · the base's or its own (why) · drawn today; red = a gap", 18, GRAY)
    cols = (0, 380, 700, 1400, 2300)
    for c, h in zip(cols, ("element", "level", "Space › view", "base or its own", "today")):
        text(x0 + c, y0 + 110, h, 18, GRAY)
    for k, (el, lv, where, own, today) in enumerate(THEME_ELEMENTS):
        y = y0 + 150 + k * 40
        for c, s in zip(cols, (el, lv, where, own)):
            text(x0 + c, y, s, 17)
        text(x0 + cols[-1], y, today or "drawn", 17, RED if today.startswith("GAP") else INK)
    L.close_frame(fr_)
    return fr_


def button_rows(facts) -> list:
    """(button, where, its Run name today or "", the proposed name) for every discovery button met or planned."""
    named = dict(theme_run_names(), **BASE_NAMES)
    runs = set(named.values())
    rows, seen = [], set()
    met = facts.get("_buttons", {})
    for b, info in sorted(met.items()):
        if b in runs or re.match(r"^(run-|rNN_)", b):  # already a Run name on its button
            continue
        if b in ("Copy", "Prompt Copy", "▸", "◂", "×", "+1 more") or re.match(r"^\+\d+ more$", b):
            continue                                    # a control, not a Run
        where = info["where"]
        rows.append((b, "today: " + ("the old board page" if all("board page" in w for w in where)
                                     else "the frame") + f" ({len(where)} places)",
                     named.get(b, ""), PROPOSED_NAMES.get(b, "")))
        seen.add(b)
    for b, where in sorted(planned_buttons().items()):
        if b in seen:
            continue
        rows.append((b, "planned: " + " · ".join(sorted(set(w.split(" ›")[0] for w in where))), named.get(b, ""),
                     PROPOSED_NAMES.get(b, "")))
    return rows


def frame_run_names(x0, y0, facts) -> dict:
    fr_ = L.open_frame("Run names")
    text(x0, y0, "Run names: every discovery button, and the Run it starts", 34)
    text(x0, y0 + 50, "named today by discovery_theme.RUN_NAMES or the base (black); no name yet (red), with the name "
                      "proposed (haipipe-run rule 6: run-<type>-<target>)", 18, GRAY)
    cols = (0, 400, 1100, 1600)
    for c, h in zip(cols, ("button", "where", "its Run today", "proposed")):
        text(x0 + c, y0 + 110, h, 18, GRAY)
    for k, (b, where, today, prop) in enumerate(button_rows(facts)):
        y = y0 + 150 + k * 36
        text(x0, y, b, 17)
        text(x0 + cols[1], y, where, 15, GRAY)
        text(x0 + cols[2], y, today or "—", 16, INK if today else RED, MONO)
        if not today:
            text(x0 + cols[3], y, prop or "? name: __", 16, RED, MONO)
    L.close_frame(fr_)
    return fr_


def frame_pick(x0, y0) -> dict:
    fr_ = L.open_frame("Pick")
    text(x0, y0, "Pick: one look per element", 34)
    text(x0, y0 + 50, "write the letter you keep beside each (or a new one); b03's picks already hold", 18, GRAY)
    for i, (key, title, _, _) in enumerate(ELEMENTS):
        text(x0, y0 + 120 + i * 44, title, 20)
        if key in PICKED:
            text(x0 + 760, y0 + 120 + i * 44, "kept: " + PICKED[key], 20, GREEN)
        else:
            text(x0 + 760, y0 + 120 + i * 44, "? keep: __ (proposed: " + PROPOSALS[key][3].split(":", 1)[-1].strip() + ")",
                 20, RED)
    L.close_frame(fr_)
    return fr_


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    E.FILES.clear()
    title = frame_title(0, -2400, facts)
    te = frame_theme_elements(title["x"] + title["width"] + 200, -2400)
    rn = frame_run_names(te["x"] + te["width"] + 200, -2400, facts)
    pk = frame_pick(rn["x"] + rn["width"] + 200, -2400)
    y = max(f["y"] + f["height"] for f in (title, te, rn, pk)) + 300
    for ekey, title_, what, cards in ELEMENTS:
        fr_ = frame_element(ekey, title_, what, cards, 0, y, facts, 4 if ekey in ("space", "views") else 3)
        pr = frame_proposed(ekey, title_, max(fr_["x"] + fr_["width"], 2500) + 200, y, facts)   # clear of its subtitle
        y = max(fr_["y"] + fr_["height"], pr["y"] + pr["height"]) + 200
    canvas.write(out, list(L.els), Path(__file__).name, files=E.FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        url = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://127.0.0.1:5851"
        shoot(url.rstrip("/"))
    draw(Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].endswith(".excalidraw")
         else HERE / "s32-discovery-element-ui.excalidraw")
