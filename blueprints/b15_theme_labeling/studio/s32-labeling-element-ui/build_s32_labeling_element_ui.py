"""b15 s32 · Labeling element UI: s32-labeling-element-ui.excalidraw, the labeling theme's element gallery (b03's
s32-element-ui, cut to one theme): every kind of element the labeling theme draws, as it draws it today on the
frame (/_board/workbench at its Block, Job and Task levels, every Space and view) and on its old board and job
pages (flagged OLD), as b03's s11 · s12 · s13 plan it for labeling, and beside each element a "· proposed" frame:
the unified look (b03's picks hold), why, a green line for what changed and a red line for what is open.

Two steps:

    uv run --no-project --with playwright --with pillow python build_s32_labeling_element_ui.py --shoot [--base http://127.0.0.1:5851]
        (--no-project: inside the SPACE, uv would otherwise build the SPACE's own environment)
        walks the labeling Blocks on the frame (Block, Job, Task × the six Spaces × every view) and the old pages
        (the labeling board page and the labeling job page, its four Spaces × three views each); screenshots each
        element version into shots/<element>__NN.png, writes where it was seen and its computed style into
        shots/facts.json, and every button met (its words, its engine op, where) into facts.json's "_buttons",
        and whether the job links answer ("_links").
    python build_s32_labeling_element_ui.py
        draws the gallery from shots/ and the planned screens from b03's s11 · s12 · s13 rows for labeling
        (build_ladder_v4.block_views, level_views.proposed and task_proposed, sliced to one screen); marks are
        kept on rebuild (canvas.write).

The picture helpers and the pick script are b03's (build_s32_element_ui.py), imported; a button's Run name is
b03's run_names.name_of, read off the server code, so the Run names frame follows the code on every build.
"""
from __future__ import annotations

import json
import sys
import urllib.parse as UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
TOOLS = Path(__file__).resolve().parents[4]
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
B03 = TOOLS / "blueprints" / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"
sys.path.insert(0, str(B03 / "s32-element-ui"))
import build_s32_element_ui as E  # noqa: E402  (b03's gallery: PICK_JS, picture, style_line; it loads L and canvas)
import level_views as LV  # noqa: E402  (b03's planned Job and Task screens; on the path through E)
import run_names as RN  # noqa: E402  (b03's _build: each button's Run name, read off the server code)

L, canvas = E.L, E.canvas
INK, RED, GREEN, MONO = canvas.INK, canvas.RED, canvas.GREEN, L.MONO
text, base = L.text, L.base
CARD_W, MAX_H = E.CARD_W, E.MAX_H
DATE = "261008"


def frame_url(folder: str, space: str = "", sub: str = "") -> str:
    return "/_board/workbench?" + UP.urlencode({"path": folder, **({"space": space} if space else {}),
                                                **({"sub": sub} if sub else {})})


# ── what is shot ────────────────────────────────────────────────────────────────────────────────
P = "examples-6-labeling/Project-Labeling-SafeResponse/tasks/"
BL = P + "b61_response_safety"                       # schema.yaml, reports/, j01 › t01 (a labeling job's Page)
JOB, TASK = BL + "/j01_building_corpus", BL + "/j01_building_corpus/t01_dices350_labeling"
BL2 = P + "b62_depression_symptoms"
TASK2 = BL2 + "/j01_building_corpus/t01_redsm5_labeling"
SPACES = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
# (key, label, folder); the first three give the per-level cards, all are walked
LEVELS = [("block", "Block · b61 (its schema, its Jobs)", BL), ("job", "Job · j01_building_corpus", JOB),
          ("task", "Task · a labeling job (j01 › t01_dices350_labeling)", TASK),
          ("block2", "Block · b62 (a second labeling Block)", BL2), ("task2", "Task · b62's labeling job", TASK2)]
LEVEL_OF = {k: lbl.split(" · ")[0] for k, lbl, _ in LEVELS}
MAIN = ("block", "job", "task")


def job_url(block: str, page_file: str, space: str = "", view: str = "", slash: bool = True) -> str:
    """The labeling job page. The route checks its page= against path=; it answers only when path= starts with
    "/" (the labeling board writes it without one, and that link answers 400)."""
    b = ("/" if slash else "") + block
    page = "/_board/page?path=" + UP.quote(f"{b}/{page_file}", safe="/")
    url = "/_board/labeling?path=%s&file=%s&page=%s" % (UP.quote(b + "/board.md"), UP.quote(page_file), UP.quote(page))
    return url + (f"&space={space}&view={view}" if space else "")


JOB_PAGE = "j01_building_corpus/t01_dices350_labeling/t01_dices350_labeling.md"
OLD_JOB_VIEWS = {"data": ["preparation", "contract", "embedding"], "labeling": ["definition", "rounds", "guideline"],
                 "quality": ["test", "evaluation", "audit"], "delivery": ["handoff", "scan", "final"]}
OLD_SPACE = {"data": "Data", "labeling": "Labeling", "quality": "Quality", "delivery": "Delivery"}
OLD_PAGES = {   # key: (label, url)
    "old-board": ("the labeling board page (/_board/labeling-board: Guide · Jobs)",
                  f"/_board/labeling-board?path={UP.quote(BL + '/board.md', safe='')}&file=board.md"),
    "old-job": ("the labeling job page (/_board/labeling: Data · Labeling · Quality · Delivery)", job_url(BL, JOB_PAGE)),
}


def old_reason(key: str) -> str:
    """Why a card's page is old, read off the code; "" for the frame."""
    if not (SERVERS / "workbench-labeling" / "labeling_theme.py").is_file():
        return ""
    if key == "old-board":
        return "old page: the labeling theme draws on the frame now; its Jobs list is Block › Work Details › Labeling"
    if key == "old-job":
        return ("old page: the frame's Task shows the job's status and links here; still the one write door, "
                "so it retires last")
    return ""


# ── the elements ────────────────────────────────────────────────────────────────────────────────
# mode "level": one card per level (at `space`) and per old page; "views": one per level × Space with a third row,
# and per old Space; "space": one per level × Space, and per old Space; "distinct": every view of every page is
# walked and each look met is one card (its first place, + the count of places); "item": the listed places.
TAB_SEL = "nav.levels|nav.spaces"
ELEMENTS = [
    dict(key="tabs", title="1 · Top tabs", what="the rows you choose a level and a Space from", mode="level",
         space="Work Details", frame=TAB_SEL, old={"old-board": "nav.spaces", "old-job": "nav.spaces"}),
    dict(key="views", title="2 · View row (third row)", what="the views of the open Space", mode="views",
         frame="nav.subs", old={"old-job": ".views"}),
    dict(key="report", title="3 · Audience Report: the Question rows", what="one question with its work and its report",
         mode="distinct", only=("Audience Report",), frame=[".q-row:not(.q-head-row)", "details.qc", "div.lw-row"],
         old={}),
    dict(key="space", title="4 · The Space body", what="the open Space's box, its first screen (its first view)",
         mode="space", frame=".split", old={"old-board": ".space-main", "old-job": ".split"}),
    dict(key="table", title="5 · Tables", what="rows of items in a table", mode="distinct",
         frame=["table"], old={"old-board": ["table"], "old-job": ["table"]}),
    dict(key="cards", title="6 · Rows and cards", what="one item, closed or open", mode="distinct",
         frame=["details.topic", "div.topic", "div.card", "details.card", "div.item-row", "details.q-more"],
         old={"old-board": ["div.card", "a.rec"], "old-job": ["div.card", "details", "dl.brief"]}),
    dict(key="runs", title="7 · Disk · Runs panel", what="the files behind the open Space, its run types and their Runs",
         mode="level", space="Work Details", frame="section.runs-panel", old={"old-job": "section.runs-panel"}),
    dict(key="tags", title="8 · Tags and pills", what="a state, a kind or a count on an item", mode="distinct",
         frame=[".chip", ".pill", ".st-ok", ".st-warn", ".tag", ".badge", "span.kind", ".item-kind", ".item-status"],
         old={"old-board": [".pill", ".chip", ".rid"], "old-job": [".pill", ".chip", ".badge", ".tag", ".st-ok", ".st-warn"]}),
    dict(key="header", title="9 · Page header", what="the title line at the top", mode="level", space="Work Details",
         frame="header", old={"old-board": ".wb-band", "old-job": "h1.pagetitle|.wb-band"}),
    dict(key="item", title="10 · One labeling job's display", what="one labeling job, the item itself", mode="item"),
    # the labeling theme's own elements
    dict(key="status", title="11 · Job status and the way out (labeling only)",
         what="a labeling job's status (no item text) and the link that opens the job page", mode="item"),
    dict(key="schema", title="12 · The schema (labeling only)", what="the label the Block builds: schema.yaml", mode="item"),
    dict(key="definition", title="13 · Label meanings and the G0 gate (labeling only)",
         what="what each label means, confirmed by the person before any round", mode="item"),
    dict(key="rounds", title="14 · Calibration rounds (labeling only)",
         what="a round drawn, released, labeled by the person; item text shows only here", mode="item"),
    dict(key="prep", title="15 · Corpus preparation and the map (labeling only)",
         what="the corpus prepared into items (sealed test held back) and the embedding map", mode="item"),
    dict(key="quality", title="16 · Quality and delivery: test · evaluation · audit · handoff · scan · final (labeling only)",
         what="Scanning: executors qualified on the sealed test, the scan, the audit, the signed handoff", mode="item"),
]
OWN = ("status", "schema", "definition", "rounds", "prep", "quality")


def F(level: str, space: str, sub: str = "") -> str:
    return frame_url(dict((k, f) for k, _, f in LEVELS)[level], space, sub)


def O(space: str, view: str) -> str:
    return f"old-job#{space}/{view}"


# item and own elements: (label, url, selector); a "old-job#space/view" url is the old job page at that view
ITEMS = {
    "item": [("Task › Work Details › Rounds: the job's status, ↗ out", F("task", "Work Details", "Rounds"), ".space-main"),
             ("Task › Description › Contract", F("task", "Description", "Contract"), ".space-main"),
             ("Block › Work Details › Labeling: the job as one row", F("block", "Work Details", "Labeling"), ".space-main"),
             ("old job page › Labeling › Rounds", O("labeling", "rounds"), ".split"),
             ("old job page › Data › Contract", O("data", "contract"), ".split")],
    "status": [("Block › Work Details › Labeling (status table, open ↗)", F("block", "Work Details", "Labeling"), ".space-main"),
               ("Task › Work Details › Preparation (facts, open in the Labeling workbench ↗)",
                F("task", "Work Details", "Preparation"), ".space-main"),
               ("Block › Work Details › Labeling (b62)", F("block2", "Work Details", "Labeling"), ".space-main"),
               ("old board page › Jobs: one card per job", "old-board", ".space-main")],
    "schema": [("Block › Description › Schema", F("block", "Description", "Schema"), ".space-main"),
               ("Block › Description › Schema (b62)", F("block2", "Description", "Schema"), ".space-main"),
               ("Job › Description (the face; no schema here)", F("job", "Description"), ".space-main")],
    "definition": [("Task › Work Details › Definition", F("task", "Work Details", "Definition"), ".space-main"),
                   ("old job page › Labeling › Definition", O("labeling", "definition"), ".space-main")],
    "rounds": [("Task › Work Details › Rounds", F("task", "Work Details", "Rounds"), ".space-main"),
               ("old job page › Labeling › Rounds", O("labeling", "rounds"), ".space-main"),
               ("old job page › Labeling › Guideline", O("labeling", "guideline"), ".space-main")],
    "prep": [("Task › Work Details › Preparation", F("task", "Work Details", "Preparation"), ".space-main"),
             ("Task › Work Details › Embedding", F("task", "Work Details", "Embedding"), ".space-main"),
             ("old job page › Data › Preparation", O("data", "preparation"), ".space-main"),
             ("old job page › Data › Embedding", O("data", "embedding"), ".space-main")],
    "quality": [("Task › Work Details › Test", F("task", "Work Details", "Test"), ".space-main"),
                ("Task › Delivery › Handoff", F("task", "Delivery", "Handoff"), ".space-main"),
                ("Task › Audience Report › Report", F("task", "Audience Report", "Report"), ".space-main"),
                ("old job page › Quality › Test", O("quality", "test"), ".space-main"),
                ("old job page › Quality › Audit", O("quality", "audit"), ".space-main"),
                ("old job page › Delivery › Handoff", O("delivery", "handoff"), ".space-main"),
                ("old job page › Delivery › Final labels", O("delivery", "final"), ".space-main")],
}

# ── as b03's s11 · s12 · s13 plan it for labeling: (level, Space, its index in that level's row of screens) ──
# Block: build_ladder_v4.BLOCK_COLUMNS; Job: level_subs(labeling, Job); Task: Guide, then task_screens(labeling Task)
PLANNED = {
    "tabs": [("Task", "Work Details › Rounds", 4)],
    "views": [("Task", "Work Details › Rounds", 4), ("Job", "Work Details", 3)],
    "report": [("Job", "Audience Report › Scored", 2), ("Block", "Audience Report", 6)],
    "space": [("Job", "Work Details", 3)],
    "table": [("Block", "Runs", 8)],
    "cards": [("Block", "Work Details › Jobs", 7)],
    "runs": [("Task", "Runs", 5)],
    "item": [("Task", "Description › Scope", 1)],
    "status": [("Block", "Work Details › Jobs", 7)],
    "schema": [("Job", "Description › Dataset", 0), ("Block", "Description › Scope", 1)],
    "definition": [("Task", "Work Details › Rounds", 4)],
    "rounds": [("Task", "Work Details › Rounds", 4)],
    "prep": [("Job", "Work Details", 3)],
    "quality": [("Task", "Delivery", 6), ("Task", "Audience Report › Report", 3)],
}

# ── the proposed look: (source, selector, why, changed (green), open (red)) ───────────────────────────
# b03's picks hold (s32-D01 tabs D · E, D02 view row E, D05 the Question cell as Insight's row, D08 Disk inside
# the Runs panel, D09 no tags); where the frame already draws the look, its own version is the proposal; the
# labeling theme's own elements carry the old job page's content over into the frame (JL: carry over what exists)
PROPOSALS = {
    "tabs": (F("task", "Work Details", "Rounds"), TAB_SEL,
             ["b03's D · E look (b03 s32-D01): the labeling theme gives the words only",
              "Guide · Block · Job ▾ · Task ▾, then the six Spaces, the same at every level",
              "the job page's own four Spaces (Data · Labeling · Quality · Delivery) go: they are the Task's views"],
             "kept: the frame's D · E tabs (b03 s32-D01)",
             "? the old job page still draws its own four Spaces, a second set of tabs, while it is the write door"),
    "views": (F("task", "Work Details", "Rounds"), "nav.subs",
              ["b03's E look (b03 s32-D02): the tabs' shape, one family",
               "s13 groups the Task's Work Details by side: Embedding · Definition · Rounds · Guideline | Test · "
               "Evaluation · Scan · Audit"],
              "kept: the frame's E view row (b03 s32-D02)",
              "? Task › Work Details: Preparation sits here (s13: Description), Scan sits in Delivery (s13: Work "
              "Details), no Building | Scanning divider, and the base's Evidence · Value follow in the same row"),
    "report": (F("block", "Audience Report"), ".q-head-row|.q-row:not(.q-head-row)",
               ["one Question │ Work │ Report row per Question at every level (b03 s04-D04)",
                "the Question cell as the Insight row (b03 s32-D05): label and state dot, short name, one sentence, › More"],
               "kept: the Question cell as Insight's (b03 s32-D05)",
               "? Job › Audience Report draws no rows: s12 plans ours vs the dataset's keys (Scored · Building), "
               "read from t04's scoring Runs; j01 has no reports/ and no t04 yet"),
    "space": (F("block", "Work Details", "Labeling"), ".split",
              ["one content box and one right column, Disk · Runs, at every labeling level",
               "the theme fills the box; the job page's own page around it retires"],
              "kept: the frame's body, every level", ""),
    "table": (F("block", "Work Details", "Labeling"), "table.wf-table",
              ["the frame's light table: small grey heads, rows ruled by one line",
               "a job with a body is a row (6), not a cell; the job page's step tables take this table"],
              "kept: the frame's table (wf-table)",
              "? the old job page draws its own step table (table.steptable) in Data › Preparation"),
    "cards": (F("block", "Idea Studio"), ".space-main",
              ["one closed row per item: ▸ name · its facts, opened in place (the Idea Studio's topic rows)",
               "a round, a Run, a labeling job: the same row; a card only for the one item that is open"],
              "kept: the frame's rows",
              "? the old job page's cards (div.card with a primary button) carry the gated actions; they move "
              "into rows with a Run button"),
    "runs": (F("task", "Work Details", "Rounds"), "section.runs-panel",
             ["Disk, then Runs, one panel, one fold (b03 s32-D08)",
              "one row per run type, named run-<type>-<target>: the labeling ones run-labeling-<op>-<target>",
              "a round is its own Run (run-labeling-round-<NN>); its steps are passes of it"],
             "changed: Disk inside Runs; the frame names each labeling button by its Run",
             "? the old job page's panel names none: {unnamed} buttons have no Run name yet (frame: Run names)"),
    "tags": (("none",), "",
             ["none: no tags in any theme (b03 s32-D09)",
              "a state is a word (judged · hold · repair · empty) or the Question's state dot",
              "an id is plain text where it stands (G0, round_04, run-labeling-round-04)"],
             "changed: no tags (b03 s32-D09)",
             "? {tags} kind(s) drawn today on the frame: the 'open ↗' chip (a job with a state adds the st-ok · "
             "st-warn span); the old pages' pills"),
    "header": (F("block", "Work Details"), "header",
               ["one line: 🏷 Labeling · the folder; the path on hover",
                "no band, no links row above the tabs (the old pages' wb-band and wb-links)"],
               "kept: one line, no band", ""),
    "item": (F("task", "Work Details", "Rounds"), ".space-main",
             ["one labeling job opens as its Task in the frame (s13): its views are the Task's Spaces",
              "no item page beside the frame once the frame hosts the gated actions (G0, release, label)"],
             "proposed: a labeling job is a Task; its page retires when the frame takes the write door",
             "? today the frame shows status only and sends the person out (↗) to act; {links}"),
    "status": (F("block", "Work Details", "Labeling"), ".space-main",
               ["one row per labeling job: job · Page · state · phase · rounds · next (no item text)",
                "the state a word, not a span with a colour; 'open ↗' a plain link, not a chip",
                "s11 plans it as Block › Work Details › Jobs, grouped by label, a Job's Tasks under it"],
               "kept: the status table, the theme's own (read only, from labeling.board_jobs)",
               "? two lists: Work Details › Jobs (vanilla, the jNN_ folders) and › Labeling (the jobs); s11 plans one"),
    "schema": (F("block", "Description", "Schema"), ".space-main",
               ["the label the Block builds, as schema.yaml reads, under Description",
                "s12 plans it per Job (one label each, by version: Description › Label)"],
               "kept: Description › Schema, the file as it reads (space-source)",
               "? where it lives: the Block today, per Job in s12 (b15 Q03 open)"),
    "definition": (O("labeling", "definition"), ".space-main",
                   ["each label's meaning before and after the talk, then Confirm meaning (G0): the person's gate",
                    "carried over into the frame's Task › Work Details › Definition, in base rows; the gate stays "
                    "an engine-checked action (POST /_board/labeling/act)"],
                   "carry over: the job page's Definition view into the frame (JL: carry over what exists)",
                   "? the frame's Definition shows the job's status only; the gate is reachable only on the old page"),
    "rounds": (O("labeling", "rounds"), ".space-main",
               ["a round as one row: round · items · state; opened, its card · prospect · judgments · rules · result",
                "item text shows only here, for the person labeling (never on a status view)"],
               "carry over: the job page's Rounds view into the frame",
               "? the frame's Rounds shows status only; Draw one round and You label one round have no Run name"),
    "prep": (O("data", "preparation"), ".space-main",
             ["the five preparation steps as one table (the base's), each a pass of the corpus's Run",
              "the embedding map as a picture in the box, its build settings as a row"],
             "carry over: Data › Preparation and Embedding into the frame",
             "? the five preparation buttons have no Run name; 'Build a map' reads as run-draw-<sNN> (a clash)"),
    "quality": (F("task", "Delivery", "Handoff"), ".space-main",
                ["Test · Evaluation · Audit as Work Details views (Scanning), Handoff · Final labels as Delivery",
                 "the signed handoff is the one crossing: a Delivery row with its version and signature"],
                "kept: the frame's Delivery › Handoff · Scan · Final labels (status + ↗)",
                "? the engine's Scanning Runs are not built yet (test-gold-lock … dstar-materialize): the views "
                "are empty on every job; Scan sits in Delivery, s13 has it in Work Details"),
}
EXTRA_PROPOSALS = {
    "rounds": [(F("task", "Work Details", "Rounds"), ".space-main", "the frame's Rounds today: the box it moves into")],
    "definition": [(F("task", "Work Details", "Definition"), ".space-main", "the frame's Definition today: status only")],
}

# what the labeling theme draws, by level (asked by b03 for its s32's Theme elements frame)
# (element, level, Space › view, base or its own and why, drawn today ("" yes), gap)
THEME_ELEMENTS = [
    ("top tabs", "every level", "the level row and the six Spaces", "base", "", ""),
    ("top tabs", "Task (old page)", "Data · Labeling · Quality · Delivery", "retires: the Task's views", "old page",
     "the job page keeps its own four Spaces while it is the write door"),
    ("view row", "every level", "every Space's views", "base", "", ""),
    ("view row", "Task", "Work Details › Preparation … Audit, then Evidence · Value", "base row, the theme's views",
     "yes", "s13: Preparation to Description, Scan to Work Details, a Building | Scanning divider"),
    ("Question rows", "Block", "Audience Report", "base (the Insight row)", "", ""),
    ("Question rows", "Job", "Audience Report › Scored · Building (ours vs the keys)", "base row, the labeling words",
     "no", "not drawn: no reports/ in the Job, no t04 scoring Task yet"),
    ("Question rows", "Task", "Audience Report › Report (REPORT.md)", "base (a work Task's Report)", "yes",
     "REPORT.md is the engine's render; s13: the guideline's cheatsheet inside it"),
    ("Space body + Disk · Runs", "every level", "every Space", "base", "", ""),
    ("table", "Block · Task", "Work Details › Labeling; the job's facts", "base (wf-table)", "", ""),
    ("table", "Task (old page)", "Data › Preparation steps", "base table", "old page", "steptable, its own"),
    ("rows", "every level", "Idea Studio; Work Details › Jobs", "base", "", ""),
    ("Runs panel", "every level", "every Space", "base; buttons named run-labeling-<op>-<target>", "",
     "the old page's panel names none (see Run names)"),
    ("tags", "Block · Task", "state spans, 'open ↗' chips", "none (b03 s32-D09)", "drawn",
     "state as a word; ↗ as a plain link"),
    ("header", "every level", "top line", "base", "", ""),
    ("job status (no item text)", "Block · Task", "Block › Work Details › Labeling; Task › each view",
     "its own: a labeling job's status, read only", "yes", "two lists at the Block (Jobs and Labeling)"),
    ("way out ↗", "Block · Task", "every labeling view", "its own until the frame hosts the gates",
     "yes", ""),
    ("schema", "Block (Job in s12)", "Description › Schema", "its own: the label, as the file reads", "yes",
     "per Job in s12 (b15 Q03)"),
    ("label meanings + G0 gate", "Task", "Work Details › Definition", "its own: the person's gate", "old page only",
     "carry over into the frame; the act door stays the engine's"),
    ("calibration rounds", "Task", "Work Details › Rounds", "its own: item text only here", "old page only",
     "carry over; round steps = passes of run-labeling-round-<NN>"),
    ("corpus preparation + map", "Task (Job in s12: t01 items)", "Work Details › Preparation · Embedding",
     "base table + its own map", "old page only", "s12 makes preparation the Job's t01 (a work Task)"),
    ("guideline", "Task", "Work Details › Guideline", "its own: the versions G_NN", "old page only", "carry over"),
    ("test · evaluation · audit", "Task", "Work Details (Scanning)", "base table", "empty",
     "the engine's Scanning Runs are not built yet"),
    ("handoff · scan · final labels", "Task → Job → Block", "Delivery", "base rows; the handoff its own (signed)",
     "status only", "s12 · s11 roll them up into the Job's and the Block's Delivery"),
    ("Idea Studio", "every level", "Idea Studio", "base (b03 s32-D06)", "", ""),
    ("the labeling board page", "(old)", "/_board/labeling-board", "retires: Block › Work Details", "old page", ""),
    ("the labeling job page", "(old)", "/_board/labeling", "retires last: it is the write door", "old page",
     "its gated actions move to the frame first"),
]

# every button with no Run name yet: its proposed Run, by the rule the theme already uses (a view's button is
# run-labeling-<view>-<job>; an engine step inside a view is a pass of that view's Run; a round is its own Run)
OP_RUN = {"source-normalize": "run-labeling-corpus-<corpus>", "unit-recipe": "run-labeling-corpus-<corpus>",
          "unit-materialize": "run-labeling-corpus-<corpus>", "unit-check": "run-labeling-corpus-<corpus>",
          "initial-group-reserve": "run-labeling-corpus-<corpus>", "corpus-contract": "run-labeling-contract-<job>",
          "test-reserve": "run-labeling-contract-<job>", "embedding-build": "run-labeling-embedding-<job>",
          "discovery-search": "run-labeling-definition-<job>", "definition-discussion": "run-labeling-definition-<job>",
          "guideline-seed": "run-labeling-guideline-<job>", "guideline-learn": "run-labeling-guideline-<job>",
          "round-prepare": "run-labeling-round-<NN>", "weak-prelabel": "run-labeling-round-<NN>",
          "human-calibration": "run-labeling-round-<NN>", "round-measure": "run-labeling-round-<NN>",
          "round-close": "run-labeling-round-<NN>", "handoff-freeze": "run-labeling-handoff-<job>",
          "test-gold-lock": "run-labeling-test-<job>", "executor-predict": "run-labeling-test-<job>",
          "executor-score": "run-labeling-evaluation-<job>", "executor-select": "run-labeling-evaluation-<job>",
          "scan-preflight": "run-labeling-scan-<job>", "scan-shard": "run-labeling-scan-<job>",
          "risk-route": "run-labeling-scan-<job>", "human-review": "run-labeling-scan-<job>",
          "reconcile": "run-labeling-scan-<job>", "audit-sample": "run-labeling-audit-<job>",
          "audit-human-gold": "run-labeling-audit-<job>", "audit-analyze": "run-labeling-audit-<job>",
          "dstar-materialize": "run-labeling-final-<job>"}
WORDS_RUN = {"copy setup request": "run-labeling-corpus-<corpus>", "edit the schema": "run-labeling-schema-<jNN>",
             "score against the keys": "run-labeling-score-<jNN>", "render the report": "run-labeling-report-<job>",
             "confirm meaning": "run-labeling-definition-<job>"}
# the planned screens' buttons (b03's s11 · s12 · s13 rows for labeling), checked the same way
PLANNED_BUTTONS = sorted({b for spec in (list(L.VIEW_FAMILY["labeling"].values()) + list(LV.JOB_FAMILY_VIEWS["labeling"].values())
                                        + list(LV.TASK_VARIANT_VIEWS["labeling Task"].values())) for b in spec[1]})
# a button whose words b03's run_names reads as another theme's or the base's Run (a clash in its DRAWN table)
CLASH = {"set up the job": ("Data › Contract: the job's contract", "run-labeling-contract-<job>"),
         "build a map": ("Data › Embedding: the embedding map", "run-labeling-embedding-<job>"),
         "measure": ("Rounds: one round's metrics, a pass of it", "run-labeling-round-<NN>")}

PICKED = {"tabs": "D · E (b03 s32-D01)", "views": "E (b03 s32-D02)", "report": "the Question cell as Insight's (b03 s32-D05)",
          "runs": "Disk inside the Runs panel (b03 s32-D08)", "tags": "none (b03 s32-D09)"}
CHANGES = ["new topic: the labeling theme's element gallery, after b03's s32 (b03's picks hold)",
           "shot live from b61 · b62 (Block, Job, Task, every Space and view) and the old board and job pages",
           "b03's s11 · s12 · s13 labeling screens drawn beside today's, sliced from b03's own row builders",
           "Theme elements and Run names frames: what each level uses, and every button with no Run name",
           "b03's fixes: both job links answer 200; the three clashing words read the labeling Runs"]


# ── shooting ────────────────────────────────────────────────────────────────────────────────────────
COLLECT_JS = """([sels, scope, tagmode]) => {
  const root = scope ? [...document.querySelectorAll(scope)].find(e => e.getBoundingClientRect().width > 4) : document;
  if (!root) return [];
  const folded = e => { for (let d = e.parentElement; d; d = d.parentElement) {
      if (d.tagName === 'DETAILS' && !d.open && !e.closest('summary')?.parentElement?.isSameNode(d)) return true; }
    return false; };
  const out = [], seen = new Set();
  for (const sel of sels) for (const e of root.querySelectorAll(sel)) {
    const r = e.getBoundingClientRect();
    if (r.width < 4 || r.height < 4 || e.closest('dialog') || folded(e)) continue;
    if (e.closest('.runs-panel') || e.closest('nav') || e.closest('.views')) continue;   // their own elements
    const ce = getComputedStyle(e);
    const cls = e.tagName.toLowerCase() + '.' + (String(e.className).trim().split(/\\s+/)[0] || '');
    const sig = cls + '|' + ce.fontSize + '|' + ce.borderTopLeftRadius + '|' + ce.paddingTop + ' ' + ce.paddingLeft
                + '|' + ce.borderTopWidth + ' ' + ce.borderTopStyle;
    if (seen.has(sig)) continue;
    seen.add(sig);
    let b = r;
    if (tagmode) { const c = e.closest('tr,p,li,summary,.rh,dd'); if (c && c.getBoundingClientRect().height < 90) b = c.getBoundingClientRect(); }
    const pad = tagmode ? 4 : 0;
    const probe = e.querySelector('button, a, select, th, td, summary') || e, cs = getComputedStyle(probe);
    out.push({sig, x: b.left + scrollX - pad, y: b.top + scrollY - pad, w: Math.min(b.width + 2 * pad, 1400), h: b.height + 2 * pad,
              style: {font: cs.fontSize + ' ' + cs.fontWeight, radius: cs.borderTopLeftRadius,
                      padding: cs.paddingTop + ' ' + cs.paddingLeft, border: cs.borderTopColor, fill: cs.backgroundColor,
                      tag: cls}});
  }
  return out;
}"""
BUTTONS_JS = """() => [...document.querySelectorAll('button.run-type[data-label], .space-main button, .space-main a.btn')]
  .filter(b => b.getBoundingClientRect().width > 0 && !b.closest('nav') && !b.closest('.views') && !b.classList.contains('run-new') && !b.classList.contains('runs-fold')
               && !b.classList.contains('run-copy'))
  .map(b => ({words: (b.dataset.label || b.textContent).trim().replace(/\\s+/g, ' ').replace(/ \\d+$/, ''),
              doing: (b.querySelector('.run-doing') || {}).textContent || '', op: b.dataset.op || ''}))
  .filter(b => b.words && b.words.length < 60)"""


class Shooter:
    def __init__(self, page, base_url):
        self.page, self.base = page, base_url
        self.facts, self.n, self.seen = {}, {}, {}
        self.buttons, self.links, self.missing = {}, {}, []

    def snap(self, box, path):
        """Scroll the box to the top, then clip in the viewport (a full-page shot moves the frame's 100vh boxes)."""
        top = self.page.evaluate("y => { window.scrollTo(0, Math.max(0, y - 8)); return window.scrollY; }", box["y"])
        self.page.wait_for_timeout(120)
        clip = {"x": max(box["x"], 0), "y": max(box["y"] - top, 0), "width": max(min(box["w"], 1490 - max(box["x"], 0)), 1),
                "height": min(max(box["h"], 1), MAX_H)}
        self.page.screenshot(path=str(path), clip=clip)

    def shot(self, ekey, box, place, url, sel, old=""):
        n = self.n.get(ekey, 0) + 1
        name = f"{ekey}__{n:02d}"
        try:
            self.snap(box, SHOTS / f"{name}.png")
        except Exception as exc:                          # off the page: no card
            self.missing.append(f"{ekey} at {place}: {str(exc).splitlines()[0]}")
            return None
        self.n[ekey] = n
        self.facts[name] = {"element": ekey, "place": place, "url": url, "selector": sel, "old": old,
                            "cut": box["h"] > MAX_H, "seen": [place], **box["style"]}
        return name

    def goto(self, url):
        """A frame URL, "old-board", or "old-job#space/view"; True when it answered 200."""
        if url.startswith("old-job"):
            sv = url.partition("#")[2]
            s, _, v = sv.partition("/")
            url = OLD_PAGES["old-job"][1] + (f"&space={s}&view={v}" if s else "")
        elif url in OLD_PAGES:
            url = OLD_PAGES[url][1]
        try:
            resp = self.page.goto(self.base + url, timeout=60000)
        except Exception as err:
            self.missing.append(f"{url[:80]}: {type(err).__name__}")
            return False
        self.page.wait_for_timeout(800)
        self.page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
        self.page.wait_for_timeout(150)
        return bool(resp and resp.status == 200)

    def one(self, sel):
        for alt in sel.split(","):
            box = self.page.evaluate(E.PICK_JS, alt.strip())
            if box:
                return box
        return None

    def note_buttons(self, place):
        for b in self.page.evaluate(BUTTONS_JS):
            row = self.buttons.setdefault(b["words"], {"op": b["op"], "doing": b["doing"].strip(), "places": []})
            if place not in row["places"]:
                row["places"].append(place)

    def distinct(self, el, sels, scope, place, url, old=""):
        for box in self.page.evaluate(COLLECT_JS, [sels, scope, el["key"] == "tags"]):
            k = (el["key"], box["sig"], bool(old))
            if k in self.seen:
                if place not in self.facts[self.seen[k]]["seen"]:
                    self.facts[self.seen[k]]["seen"].append(place)
                continue
            name = self.shot(el["key"], box, place, url, box["sig"], old)
            if name:
                self.seen[k] = name

    def walk(self):
        """Every frame page (level × Space × view), then the old pages, each element taken as its mode says."""
        for lkey, llabel, folder in LEVELS:
            main = lkey in MAIN
            for space in SPACES:
                if not self.goto(frame_url(folder, space)):
                    self.missing.append(f"{lkey} {space}: not 200")
                    continue
                subs = self.page.evaluate("[...document.querySelectorAll('nav.subs a')].map(a => a.textContent.trim())")
                for i, sub in enumerate(subs or [""]):
                    if i and not self.goto(frame_url(folder, space, sub)):
                        continue
                    url = frame_url(folder, space, sub if i else "")
                    place = f"{LEVEL_OF[lkey]} › {space}" + (f" › {sub}" if sub else "") + ("" if main else f" ({llabel})")
                    self.note_buttons(place)
                    for el in ELEMENTS:
                        mode = el["mode"]
                        if mode == "distinct" and (not el.get("only") or space in el["only"]):
                            self.distinct(el, el["frame"], ".space-main", place, url)
                        if not main or i:
                            continue
                        if mode == "level" and space == el["space"] or mode == "space" or mode == "views" and subs:
                            box = self.one(el["frame"])
                            if box:
                                self.shot(el["key"], box, llabel if mode == "level" else f"{LEVEL_OF[lkey]} › {space}",
                                          url, el["frame"])
        # the old board page
        if self.goto("old-board"):
            why = old_reason("old-board")
            self.note_buttons("old board page")
            for el in ELEMENTS:
                sel = el.get("old", {}).get("old-board")
                if not sel:
                    continue
                if el["mode"] == "distinct":
                    self.distinct(el, sel, ".space-main", "old board page › Jobs", OLD_PAGES["old-board"][1], why)
                else:
                    box = self.one(sel)
                    if box:
                        self.shot(el["key"], box, OLD_PAGES["old-board"][0], OLD_PAGES["old-board"][1], sel, why)
        # the old job page: its four Spaces × three views
        why = old_reason("old-job")
        for s, views in OLD_JOB_VIEWS.items():
            for n, v in enumerate(views):
                if not self.goto(O(s, v)):
                    self.missing.append(f"old job page {s}/{v}: not 200")
                    continue
                place = f"old job page › {OLD_SPACE[s]} › {v}"
                url = OLD_PAGES["old-job"][1] + f"&space={s}&view={v}"
                self.note_buttons(place)
                for el in ELEMENTS:
                    sel = el.get("old", {}).get("old-job")
                    if not sel:
                        continue
                    if el["mode"] == "distinct":
                        self.distinct(el, sel, ".space-main", place, url, why)
                    elif el["mode"] in ("space", "views") and n == 0:
                        box = self.one(sel)
                        if box:
                            self.shot(el["key"], box, f"old job page › {OLD_SPACE[s]}", url, sel, why)
                    elif el["mode"] == "level" and s == "data" and n == 0:
                        box = self.one(sel)
                        if box:
                            self.shot(el["key"], box, OLD_PAGES["old-job"][0], url, sel, why)

    def check_links(self):
        """Whether the job links the board page and the frame write answer (the route checks path= and page=)."""
        self.goto("old-board")
        href = self.page.evaluate("() => { const a = [...document.querySelectorAll('a[href]')].find(a => "
                                  "a.getAttribute('href').startsWith('/_board/labeling?')); return a ? a.getAttribute('href') : ''; }")
        self.goto(F("task", "Work Details", "Rounds"))
        out = self.page.evaluate("() => { const a = [...document.querySelectorAll('.space-main a[href]')].find(a => "
                                 "a.getAttribute('href').startsWith('/_board/labeling?')); return a ? a.getAttribute('href') : ''; }")
        for name, h in (("the board page's job link", href), ("the frame's 'open in the Labeling workbench ↗'", out),
                        ("the same link with path= starting '/'", job_url(BL, JOB_PAGE))):
            if not h:
                self.links[name] = "none"
                continue
            resp = self.page.goto(self.base + h)
            self.links[name] = resp.status if resp else "?"

    def items(self):
        for ekey, rows in ITEMS.items():
            for label, url, sel in rows:
                if not self.goto(url):
                    self.missing.append(f"{ekey}: {label}: not 200")
                    continue
                self.page.wait_for_timeout(400)
                box = self.one(sel)
                key = "old-board" if url == "old-board" else "old-job" if url.startswith("old-job") else ""
                if box:
                    self.shot(ekey, box, label, url, sel, old_reason(key) if key else "")
                else:
                    self.missing.append(f"{ekey}: {label}: {sel} not found")

    def proposals(self):
        for key, (src, sel, *_rest) in PROPOSALS.items():
            if isinstance(src, tuple):
                continue
            self.goto(src)
            box = self.page.evaluate(E.PICK_JS, sel)
            if not box:
                self.missing.append(f"proposal {key}: {sel} not found")
                continue
            self.snap(box, SHOTS / f"proposed__{key}.png")
            self.facts[f"proposed__{key}"] = {"element": key, "place": "proposed", "url": src, "selector": sel,
                                              "old": "", "cut": box["h"] > MAX_H, "seen": [], **box["style"]}
        for key, extras in EXTRA_PROPOSALS.items():
            for n, (src, sel, _) in enumerate(extras, 1):
                self.goto(src)
                box = self.page.evaluate(E.PICK_JS, sel)
                if box:
                    self.snap(box, SHOTS / f"proposed__{key}__{n}.png")


def shoot(base_url: str) -> None:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    for f in SHOTS.glob("*.png"):
        f.unlink()
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
        s = Shooter(page, base_url)
        s.walk()
        s.items()
        s.proposals()
        s.check_links()
        browser.close()
    s.facts["_buttons"], s.facts["_links"], s.facts["_missing"] = s.buttons, s.links, s.missing
    (SHOTS / "facts.json").write_text(json.dumps(s.facts, indent=1, ensure_ascii=False))
    print(f"{len([k for k in s.facts if not k.startswith('_')])} shots in {SHOTS.relative_to(HERE.parent)}")
    for m in s.missing:
        print("  not shot:", m)


# ── the planned screens: b03's own row builders, one screen sliced out ─────────────────────────────────
_ROWS = {}


def _row(level):
    """Every element b03 draws for labeling's row of screens at `level`, drawn at (0, 0), and the stride."""
    if level not in _ROWS:
        keep, frame = list(L.els), L.FRAME[0]
        L.els.clear()
        L.FRAME[0] = None
        if level == "Block":
            L.block_views(0, 0, "labeling Block")
            stride = L.UI_W + L.VIEW_GAP
        elif level == "Job":
            LV.proposed(0, 0, "labeling Job", "Job")
            stride = L.UI_W + LV.GAP
        else:
            LV.task_proposed(0, 0, "labeling Task")
            stride = L.UI_W + LV.GAP
        _ROWS[level] = ([dict(e) for e in L.els], stride)
        L.els[:] = keep
        L.FRAME[0] = frame
    return _ROWS[level]


def planned_screen(level, idx, x, y) -> float:
    """Screen `idx` of b03's labeling row at `level`, moved to (x, y) in the open frame; returns its height."""
    els, stride = _row(level)
    x0 = idx * stride
    part = [e for e in els if x0 - 4 <= e["x"] < x0 + stride - 20 and e["type"] != "frame"]
    if not part:
        text(x, y, f"? b03 draws no labeling {level} screen {idx}", 20, RED)
        return 40
    top = min(e["y"] for e in part)
    for k, e in enumerate(part):
        e = dict(e, id=f"pl-{level}-{idx}-{round(x)}-{round(y)}-{k}", frameId=L.FRAME[0])
        e["x"], e["y"] = e["x"] - x0 + x, e["y"] - top + y
        L.els.append(e)
    return max(e["y"] + e["height"] for e in part) - top


# ── the drawing ─────────────────────────────────────────────────────────────────────────────────────
def card(x, y, letter, f, path) -> float:
    """One version: its place, its picture, its style line; an old one flagged OLD, red dashed. Its height."""
    old = f.get("old", "")
    if old:
        text(x, y - 26, "OLD · " + old, 14, RED)
    seen = f.get("seen", [])
    more = f"  (+{len(seen) - 1} more places)" if len(seen) > 1 else ""
    text(x, y, f"{letter} · {f.get('place', '')}{more}", 18)
    h = E.picture(path, x, y + 36, CARD_W)
    if old:
        base("rectangle", x - 8, y + 28, E.LAST_W[0] + 16, h + 16, RED, 1.5, dashed=True, rough=0)
    text(x, y + 48 + h, E.style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 13, INK, MONO)
    return 48 + h + 50


def frame_element(el, x0, y0, facts, per_row=3) -> dict:
    fr = L.open_frame(el["title"])
    text(x0, y0, el["title"], 34)
    keys = sorted(k for k, f in facts.items() if not k.startswith(("_", "proposed__")) and f.get("element") == el["key"])
    olds = sum(bool(facts[k].get("old")) for k in keys)
    text(x0, y0 + 50, f"{el['what']} · {len(keys)} versions as the labeling theme draws them today, {olds} on old pages "
                      "(flagged OLD: they retire; a look from one may still be picked); then as s11 · s12 · s13 plan it", 18)
    x, y, row_h = x0, y0 + 130, 0
    for i, k in enumerate(keys):
        if i and i % per_row == 0:
            x, y, row_h = x0, y + row_h + 70, 0
        letter = chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)
        row_h = max(row_h, card(x, y, letter, facts[k], SHOTS / f"{k}.png"))
        x += CARD_W + 80
    if not keys:
        text(x0, y0 + 130, "? no shots yet: run with --shoot", 18, RED)
    y += row_h + 40
    planned = PLANNED.get(el["key"], [])
    if planned:
        text(x0, y + 20, "as planned · b03's s11 · s12 · s13 labeling screens, the same as there (not served yet; a "
                         "button with no Run name ends in ?)", 22)
        px = x0
        for k, (level, where, idx) in enumerate(planned):
            text(px, y + 70, f"P{k + 1} · {level} › {where}", 20)
            planned_screen(level, idx, px, y + 110)
            px += L.UI_W + 160
    L.close_frame(fr)
    return fr


def fill(s: str, facts) -> str:
    """The counts and link states an open line names, read off this shoot."""
    unnamed = len(unnamed_buttons(facts))
    tags = sum(1 for k, f in facts.items() if not k.startswith("_") and f.get("element") == "tags" and not f.get("old"))
    links = facts.get("_links", {})
    bad = [f"{k} answers {v}" for k, v in links.items() if v != 200 and "'/'" not in k]
    return (s.replace("{unnamed}", str(unnamed)).replace("{tags}", str(tags))
             .replace("{links}", "; ".join(bad) if bad else "the job links answer"))


def frame_proposed(key, title, x0, y0, facts) -> dict:
    fr = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    src, _, why, changed, open_ = PROPOSALS[key]
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench); the labeling theme gives the "
                      "words and, for its own elements, the layout", 18)
    y = y0 + 110
    L.els.append(canvas.change_note(x0, y, changed, DATE, L.FRAME[0], 20))     # green: what changed (or is kept)
    y += 40
    if open_:
        text(x0, y, fill(open_, facts), 18, RED)                               # red: still open
        y += 40
    shot = SHOTS / f"proposed__{key}.png"
    if shot.exists():
        h = E.picture(shot, x0, y, 1000)
        text(x0, y + h + 12, E.style_line(facts.get(f"proposed__{key}", {})), 13, INK, MONO)
        y += h + 70
    elif isinstance(src, tuple):
        text(x0, y, "(none)", 28)
        y += 60
    else:
        text(x0, y, "? no shot yet: run with --shoot", 18, RED)
        y += 40
    for n, (_, _, caption) in enumerate(EXTRA_PROPOSALS.get(key, []), 1):
        extra = SHOTS / f"proposed__{key}__{n}.png"
        if extra.exists():
            text(x0, y, caption, 17)
            h = E.picture(extra, x0, y + 34, 1000)
            y += h + 80
    text(x0, y + 10, "why", 22)
    for i, line in enumerate(why):
        text(x0 + 20, y + 50 + i * 30, "· " + line, 17)
    L.close_frame(fr)
    return fr


def frame_title(x0, y0, facts) -> dict:
    fr = L.open_frame("s32 · Labeling element UI")
    n = sum(1 for k in facts if not k.startswith(("_", "proposed__")))
    olds = sum(1 for k, f in facts.items() if not k.startswith("_") and f.get("old"))
    text(x0, y0, "s32 · Labeling element UI: every element the labeling theme draws, today and as planned", 40)
    text(x0, y0 + 60, f"after b03's s32-element-ui; {n} versions ({olds} on old pages), one frame per element (a card per "
                      "version today, then b03's s11 · s12 · s13 labeling screen), its '· proposed' frame to the right; "
                      "OLD = an old page, red dashed", 20)
    for k, c in enumerate(CHANGES):
        L.els.append(canvas.change_note(x0, y0 + 120 + k * 30, c, DATE, L.FRAME[0], 18))
    yy = y0 + 140 + len(CHANGES) * 30
    for k, (name, status) in enumerate(facts.get("_links", {}).items()):
        if status == 200:                               # a link that answers: green
            L.els.append(canvas.change_note(x0, yy + k * 30, f"{name}: HTTP 200", DATE, L.FRAME[0], 18))
        else:
            text(x0, yy + k * 30, f"? {name}: HTTP {status}", 18, RED)
    L.close_frame(fr)
    return fr


def frame_theme_elements(x0, y0) -> dict:
    fr = L.open_frame("Theme elements")
    text(x0, y0, "Theme elements: what the labeling theme uses, by level", 34)
    text(x0, y0 + 50, "element · level · Space › view · the base's or its own (why) · drawn today; red = a gap "
                      "(b03's s32 reads the same list from the notes)", 18)
    cols = (0, 380, 720, 1520, 2280, 2480)
    for c, h in zip(cols, ("element", "level", "Space › view", "base or its own", "today", "gap")):
        text(x0 + c, y0 + 110, h, 18)
    for k, (el, lv, where, own, today, gap) in enumerate(THEME_ELEMENTS):
        y = y0 + 150 + k * 36
        for c, s in zip(cols, (el, lv, where, own, today or "yes")):
            text(x0 + c, y, s, 16)
        if gap:
            text(x0 + cols[-1], y, "? " + gap, 16, RED)
    L.close_frame(fr)
    return fr


def unnamed_buttons(facts) -> list:
    """(words, where, op, proposed Run) for every button met (live) or planned that has no Run name yet."""
    out = []
    for words, row in sorted(facts.get("_buttons", {}).items()):
        if RN.named(words):
            continue
        prop = OP_RUN.get(row.get("op", "")) or WORDS_RUN.get(words.lower(), "?")
        where = row["places"][0] + (f" (+{len(row['places']) - 1})" if len(row["places"]) > 1 else "")
        out.append((words, where, row.get("op", ""), prop))
    for words in PLANNED_BUTTONS:
        if not RN.named(words) and words.lower() not in {w.lower() for w, *_ in out}:
            out.append((words, "planned (b03 s11 · s12 · s13)", "", WORDS_RUN.get(words.lower(), "?")))
    return out


def frame_run_names(x0, y0, facts) -> dict:
    fr = L.open_frame("Run names")
    rows = unnamed_buttons(facts)
    text(x0, y0, f"Run names: {len(rows)} labeling buttons with no Run name yet, and what each should be", 34)
    text(x0, y0 + 50, "read off the live pages and b03's planned screens; named by b03's run_names (the server code); "
                      "proposed by the theme's own rule: a view's Run run-labeling-<view>-<job>, an engine step inside a "
                      "view a pass of it, a round its own Run", 18)
    cols = (0, 380, 1040, 1300)
    for c, h in zip(cols, ("button (its words)", "where", "engine op", "proposed Run")):
        text(x0 + c, y0 + 110, h, 18)
    y = y0 + 150
    for words, where, op, prop in rows:
        for c, s in zip(cols, (words, where, op or "—")):
            text(x0 + c, y, L.short(s, 60), 16)
        text(x0 + cols[-1], y, prop, 16, RED)          # proposed, not yet in the code: open
        y += 34
    y += 30
    text(x0, y, "clashes: words b03's run_names read as another Run (green once it reads the labeling Run)", 22)
    for k, (words, (where, right)) in enumerate(CLASH.items()):
        now = RN.name_of(words)
        if now == right:                                # fixed in b03's run_names.DRAWN
            L.els.append(canvas.change_note(x0, y + 40 + k * 32, f"'{words}' → {now} ({where})", DATE, L.FRAME[0], 17))
        else:
            text(x0, y + 40 + k * 32, f"? '{words}' → {now}  ·  here it is {where}, {right}", 17, RED)
    L.close_frame(fr)
    return fr


def frame_pick(x0, y0) -> dict:
    fr = L.open_frame("Pick")
    text(x0, y0, "Pick: one look per element", 34)
    text(x0, y0 + 50, "write the letter you keep beside each (or a new one); b03's picks already hold", 18)
    for i, el in enumerate(ELEMENTS):
        text(x0, y0 + 120 + i * 44, el["title"], 20)
        if el["key"] in PICKED:
            text(x0 + 1100, y0 + 120 + i * 44, "kept: " + PICKED[el["key"]], 20, GREEN)
        else:
            text(x0 + 1100, y0 + 120 + i * 44, "? keep: __ (proposed: " + PROPOSALS[el["key"]][3].split(":", 1)[-1].strip()
                 + ")", 20, RED)
    L.close_frame(fr)
    return fr


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    E.FILES.clear()
    title = frame_title(0, -2600, facts)
    te = frame_theme_elements(title["x"] + title["width"] + 200, -2600)
    rn = frame_run_names(te["x"] + te["width"] + 200, -2600, facts)
    frame_pick(rn["x"] + rn["width"] + 200, -2600)
    y = 300
    for el in ELEMENTS:
        per_row = 4 if el["key"] in ("space", "tags", "views") else 3
        fr = frame_element(el, 0, y, facts, per_row)
        pr = frame_proposed(el["key"], el["title"], fr["x"] + fr["width"] + 200, y, facts)
        y = max(fr["y"] + fr["height"], pr["y"] + pr["height"]) + 200
    canvas.write(out, list(L.els), Path(__file__).name, files=E.FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        url = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://127.0.0.1:5851"
        shoot(url.rstrip("/"))
    draw(Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].endswith(".excalidraw")
         else HERE / "s32-labeling-element-ui.excalidraw")
