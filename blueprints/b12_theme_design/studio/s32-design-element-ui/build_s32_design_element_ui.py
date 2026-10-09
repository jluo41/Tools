"""b12 s32 · Design element UI: s32-design-element-ui.excalidraw, the design theme's element gallery (b03's
s32-element-ui, cut to one theme): every kind of element the design theme draws, as it draws it today on the
frame (/_board/workbench at its Block, Job and Task levels, every Space and view) and on its old board and item
pages (flagged OLD), as s11 · s12 · s13 plan it, and beside each element a "· proposed" frame: the unified look
(b03's picks hold), why, a green line for what changed and a red line for what is open.

Two steps:

    uv run --no-project --with playwright --with pillow python build_s32_design_element_ui.py --shoot [--base http://127.0.0.1:5851]
        (--no-project: inside the SPACE, uv would otherwise build the SPACE's own environment)
        No Project holds a design Block on the ladder yet, so the ladder levels come from the design tests'
        placeholder Project (servers/workbench-design/tests/design_fixture.py): it is written to a temp folder
        and served live by a second host (the same serve.py, --root that folder, a free port), shot, then
        stopped. The old pages (the design board page, one design's item page, an older board on the frame)
        are shot from the SPACE's host (--base). Each element goes to shots/<element>__<card>.png, its first
        control's computed style to shots/facts.json.
    python build_s32_design_element_ui.py
        draws the gallery from shots/ and the planned screens from s11 · s12 · s13's builders; marks are kept
        on rebuild (canvas.write).

The shooting and the picture helpers are b03's (../../../b03_project_workbench/studio/s32-element-ui/
build_s32_element_ui.py), imported; the planned screens are drawn by the level builders' own screen functions
(../_build/design_ui.py), so a change there shows here on the next build. Placeholders only.
"""
from __future__ import annotations

import importlib.util
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.parse as UP
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
SPACE = HERE.parents[4]
TOOLS = HERE.parents[3]
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
B03S32 = TOOLS / "blueprints" / "b03_project_workbench" / "studio" / "s32-element-ui"
sys.path.insert(0, str(B03S32))
import build_s32_element_ui as E  # noqa: E402  (b03's gallery: PICK_JS, picture, style_line; it loads L and canvas)
sys.path.insert(0, str(HERE.parent / "_build"))
import design_ui as U  # noqa: E402  (b12's level screens, shared by s11 · s12 · s13)

L, canvas = E.L, E.canvas
INK, GRAY, RED, GREEN, MONO = L.INK, L.GRAY, L.RED, L.GREEN, L.MONO
text, base = L.text, L.base
q = E.q

# ── where each card comes from ──────────────────────────────────────────────────────────────────────
# the fixture's design ladder (design_fixture.py): a Block, its Job j03 and the Job's three kinds of Task
FX_BLOCK = "Project-DesignDemo/designs/b01_demo_app"
FX = {"Block": FX_BLOCK, "Job": FX_BLOCK + "/j03_g01_m04", "t00": FX_BLOCK + "/j03_g01_m04/t00_reason-ideas",
      "d04": FX_BLOCK + "/j03_g01_m04/t04_d04_ask-only", "t99": FX_BLOCK + "/j03_g01_m04/t99_review-whole"}
D = "examples-5-design/Project-Application-SMSDesign/designs/"
B01 = D + "_old/B01_DesignBoard-Stage25-CarryOver-261005"      # both moved into designs/_old/ on 261008
B00 = D + "_old/B00_DesignBoard-R2Messages-260821"
AUTH = D + "_old/B01_DesignBoard-AuthenUI-260917"
DESIGN01 = "2-Design-M01-goal-only/Design-01-all-patients-prescription-review-sms"
OLD_PAGES = {     # (label, URL on the SPACE's host); the design board and item pages are the theme's old pages
    "board-b01": ("Design board page · B01 (5 methods × 10)", f"/_board/design-board?path={q(B01 + '/board.md')}&file=board.md"),
    "board-b00": ("Design board page · B00 (6 design tasks)", f"/_board/design-board?path={q(B00 + '/board.md')}&file=board.md"),
    "item": ("Design item page · one design task (B01 Design-01)",
             f"/_board/design?path={q('/' + B01 + '/board.md')}&file={q(DESIGN01 + '/' + DESIGN01.split('/')[1] + '.md')}&space=design"),
    "item-goal": ("Design item page · its Design Task Space (inputs and variables)",
                  f"/_board/design?path={q('/' + B01 + '/board.md')}&file={q(DESIGN01 + '/' + DESIGN01.split('/')[1] + '.md')}&space=goal"),
    "item-ui": ("Design item page · a UI design (AuthenUI, one login card)",
                f"/_board/design?path={q('/' + AUTH + '/board.md')}&file="
                f"{q('2-Design/Design-01-all-patients-log-in-with-date-of-birth-ui-card/Design-01-all-patients-log-in-with-date-of-birth-ui-card.md')}&space=design"),
    "frame-b01": ("the frame · an older board (B01), its Block", f"/_board/workbench?path={q(B01)}"),
    "frame-b01-task": ("the frame · an older Design Folder (B01 Design-01), Work Details › Designs",
                       f"/_board/workbench?path={q(B01 + '/' + DESIGN01)}&space=Work+Details"),
}


def fx(level, space, view=""):
    """A fixture page: ("fx", level, space, view)."""
    return ("fx", level, space, view)


def fx_url(level, space, view=""):
    return "/_board/workbench?" + UP.urlencode({"path": FX[level], "space": space, **({"sub": view} if view else {})})


def label_of(src) -> str:
    if src[0] == "fx":
        _, level, space, view = src
        lv = {"Block": "Block", "Job": "Job j03", "t00": "Task t00", "d04": "Task d04", "t99": "Task t99"}[level]
        return f"the frame · {lv} › {space}" + (f" › {view}" if view else "")
    return OLD_PAGES[src[1]][0]


def old_reason(src) -> str:
    """Why a card's page is old, read off the code; "" for the frame."""
    if src[0] == "old" and OLD_PAGES[src[1]][1].startswith(("/_board/design-board", "/_board/design?")) \
            and (SERVERS / "workbench-design" / "design_theme.py").is_file():
        return "old page: the design theme draws on the frame now; this page retires"
    return ""


def old(key):
    return ("old", key)


# ── the elements: (key, title, what, [(card source, selector)]) ──────────────────────────────────────
# a selector as b03's: "a|b" the box around both, "parent:x" x's parent, "a,b" the first found;
# [data-bubble] is a design's phone (tagged after load: the div whose first line reads "Text message")
TABS, SUBS = "nav.levels|nav.spaces", "nav.subs"
ELEMENTS = [
    ("tabs", "1 · Top tabs", "the level row (Guide · Design Board · Job ▾ · Task ▾) and the six Spaces",
     [(fx("Block", "Audience Report"), TABS), (fx("Job", "Audience Report"), TABS), (fx("d04", "Description"), TABS),
      (old("board-b01"), "nav.spaces"), (old("item"), "nav.tabs")]),
    ("views", "2 · View row (third row)", "the views of the open Space",
     [(fx("Block", "Description"), SUBS), (fx("Job", "Audience Report"), SUBS), (fx("Job", "Work Details"), SUBS),
      (fx("d04", "Runs"), SUBS), (old("board-b01"), ".views"), (old("board-b00"), ".views")]),
    ("report", "3 · Audience Report rows", "one Question (or one design) with its work and its report: Question │ Work │ Report",
     [(fx("Block", "Audience Report", "Questions"), "parent:.q-row"),
      (fx("Block", "Audience Report", "Predicted vs observed"), "parent:.q-row"),
      (fx("Job", "Audience Report", "Predicted vs observed"), "parent:.q-row"),
      (fx("d04", "Description", "Design"), "parent:.q-row")]),
    ("space", "4 · The Space body", "the open Space's box beside Disk · Runs, its first screen",
     [(fx("Block", "Work Details", "All"), ".split"), (fx("Job", "Audience Report", "Design display"), ".split"),
      (fx("t00", "Audience Report", "Topics"), ".split"), (fx("d04", "Description", "Design"), ".split"),
      (fx("t99", "Work Details"), ".split"), (old("board-b01"), ".pane.on"), (old("board-b00"), ".pane.on"),
      (old("frame-b01"), ".split")]),
    ("table", "5 · Tables", "rows of items",
     [(fx("Block", "Description", "Map"), "table.wf-table"), (fx("t99", "Audience Report", "Ranking"), "table.wf-table"),
      (fx("Job", "Audience Report", "Performance"), "table.wf-table"), (fx("t00", "Audience Report", "Ideas"), "table.wf-table"),
      (fx("d04", "Work Details"), "table.wf-table"), (fx("Job", "Runs", "Conduct & review"), ".space-main"),
      (old("board-b01"), "table.msgs"), (old("board-b00"), ".pane.on table"),
      (old("item-goal"), ".pane.on table.grid")]),
    ("cards", "6 · Rows and cards", "one item, closed or open",
     [(fx("Block", "Description", "Goals"), "parent:.space-main details"),
      (fx("Block", "Description", "Methods"), "parent:.space-main details"),
      (fx("Block", "Runs", "All"), "parent:.space-main details"),
      (fx("Job", "Description", "Method"), "parent:.space-main details"),
      (fx("t99", "Work Details"), "parent:.space-main details"),
      (old("board-b01"), ".pane.on .step-card"), (old("item"), ".pane.on")]),
    ("runs", "7 · Disk · Runs panel", "the files behind the open Space, its run types and their Runs (Disk inside, one fold)",
     [(fx("Block", "Runs"), "section.runs-panel"), (fx("Job", "Work Details", "Conduct & review"), "section.runs-panel"),
      (fx("d04", "Runs"), "section.runs-panel"), (fx("t00", "Audience Report"), "section.runs-panel"),
      (old("board-b01"), ".pane.on .runs-panel,.runs-panel"), (old("item"), ".runs-panel")]),
    ("tags", "8 · Tags and pills", "a state, an id or a count on an item (A, B: where the chips were, plain text since 261008)",
     [(fx("Job", "Description", "Inputs"), ".space-main table.wf-table"),          # the chips there went 261008: plain text now
      (fx("Job", "Audience Report", "Reason ideas"), ".space-main details[open] p"),
      (fx("Block", "Audience Report", "Questions"), "parent:.item-kind")]),
    ("header", "9 · Page header", "the title line at the top",
     [(fx("Block", "Description"), "header"), (fx("Job", "Description"), "header"), (fx("d04", "Description"), "header"),
      (old("board-b01"), "header"), (old("item"), "header")]),
    ("item", "10 · One design's display", "one design, the item itself",
     [(fx("d04", "Description", "Design"), ".space-main"), (fx("d04", "Audience Report", "Drafts"), ".space-main"),
      (old("frame-b01-task"), ".space-main"), (old("item"), ".pane.on"),
      (old("item-ui"), ".pane.on")]),
    ("design", "11 · Design display", "a design Job's N designs: the Job's Audience Report › Design display (b03 s32-D11)",
     [(fx("Job", "Audience Report", "Design display"), ".space-main"), (fx("Block", "Work Details", "All"), ".space-main"),
      (fx("Job", "Delivery", "designs.md"), ".space-main"), (fx("Block", "Delivery"), ".space-main"),
      (old("board-b01"), ".pane.on"), (old("item"), ".pane.on")]),
    # the design theme's own elements
    ("phone", "12 · A design as it reads (design only)", "one SMS as the reader sees it: a phone, one bubble",
     [(fx("Job", "Audience Report", "Design display"), "[data-bubble]"), (fx("d04", "Audience Report", "Drafts"), "[data-bubble]"),
      (fx("Block", "Audience Report", "Predicted vs observed"), "[data-bubble]"), (fx("Block", "Delivery"), "[data-bubble]"),
      (old("board-b01"), "parent:td.msg-text")]),
    ("map", "13 · Goal × method Map (design only)", "goals down, registered methods across, the chain of Jobs in each cell",
     [(fx("Block", "Description", "Map"), ".space-main"),
      (fx("Block", "Description", "Map/j02_g01_m04~j03_g01_m04"), ".space-main"),
      (old("board-b00"), ".pane.on"), (old("board-b01"), ".views")]),
    ("inputs", "14 · Inputs fence (design only)", "what the design work may see: a Job's inputs/, its parts and manifest",
     [(fx("Job", "Description", "Inputs"), ".space-main"), (fx("Block", "Description", "Inputs"), ".space-main"),
      (old("item-goal"), ".pane.on")]),
    ("chains", "15 · Reasoning chains (design only)", "step ②: one card per topic, its steps (from · says · so) → its ideas",
     [(fx("t00", "Audience Report", "Topics"), ".space-main"), (fx("Job", "Audience Report", "Reason ideas"), ".space-main"),
      (fx("t00", "Work Details"), ".space-main")]),
    ("observed", "16 · Predicted vs observed, cost (design only)", "a frozen prediction beside the Exp's arm; what each design cost",
     [(fx("Block", "Audience Report", "Predicted vs observed"), ".space-main"),
      (fx("Block", "Audience Report", "Method scorecard"), ".space-main"), (fx("Block", "Audience Report", "Cost"), ".space-main"),
      (fx("Job", "Audience Report", "Performance"), ".space-main"), (fx("d04", "Audience Report", "Performance"), ".space-main")]),
    ("review", "17 · Review: tests and ranking (design only)", "step ④ on one design (T0 – T3), step ⑤ on the N",
     [(fx("d04", "Audience Report", "Tests"), ".space-main"), (fx("d04", "Description", "Evaluation"), ".space-main"),
      (fx("t99", "Audience Report", "Ranking"), ".space-main"), (fx("t99", "Audience Report", "Coverage"), ".space-main"),
      (old("item"), ".pane.on table,.pane.on")]),
]

# ── as s11 · s12 · s13 plan it: (topic, band, Space, view) drawn by that builder's own screen ───────────
PLANNED = {
    "tabs": [("s13", "d04", "Description", "Design")],
    "views": [("s12", None, "Runs", "Setup")],
    "report": [("s11", None, "Audience Report", "Questions")],
    "space": [("s12", None, "Audience Report", "Reason ideas")],
    "table": [("s13", "t99", "Audience Report", "Ranking")],
    "cards": [("s11", None, "Description", "Goals")],
    "runs": [("s12", None, "Work Details", "Conduct & Review")],
    "item": [("s13", "d04", "Description", "Design")],
    "design": [("s12", None, "Audience Report", "Design display")],
    "phone": [("s13", "d04", "Audience Report", "Drafts")],
    "map": [("s11", None, "Description", "Map")],
    "inputs": [("s12", None, "Description", "Inputs")],
    "chains": [("s13", "t00", "Audience Report", "Topics")],
    "observed": [("s11", None, "Audience Report", "Predicted vs observed")],
    "review": [("s13", "d04", "Audience Report", "Tests"), ("s13", "t99", "Audience Report", "Coverage")],
}

# ── the proposed look: (source, selector, why, changed (green), open (red)) ───────────────────────────
# b03's picks hold (s32-D01 tabs D · E, D02 view row E, D05 the Question cell as Insight's row, D08 Disk inside
# the Runs panel, D09 no tags); where the frame already draws the look, its own version is the proposal
PROPOSALS = {
    "tabs": (fx("Job", "Audience Report"), TABS,
             ["b03's D · E look (s32-D01): the design theme gives the words only",
              "Guide · Design Board · Job ▾ · Task ▾, then the six Spaces, the same at every level"],
             "changed: the Task select by step, 'Task · d04 · ask-only' (option hook, 261008)",
             ""),
    "views": (fx("Job", "Audience Report"), SUBS,
              ["b03's E look (s32-D02): the tabs' shape, one family", "a level's views are its run types' Results (s13)"],
              "changed: one casing, Reason ideas · Conduct & review · Review whole (261008)",
              ""),
    "report": (fx("Block", "Audience Report", "Questions"), "parent:.q-row",
               ["one Question │ Work │ Report row per Question, as every theme (b03 s04-D04)",
                "the Question cell as the Insight row: label and state dot, short name, one sentence, › More"],
               "kept: the Question cell as Insight's (b03 s32-D05)",
               "? Predicted vs observed and Description › Design reuse the row as Design │ Predicted │ Observed: keep, or the design card"),
    "space": (fx("Job", "Audience Report", "Design display"), ".split",
              ["one content box and one right column, Disk · Runs", "the design theme fills the box; it draws no page of its own"],
              "changed: no tile grid; the base table, the phone the theme's own (261008)",
              ""),
    "table": (fx("t99", "Audience Report", "Ranking"), "table.wf-table",
              ["the frame's light table: small grey heads, rows ruled by one line", "a design with a body is a row (6), not a cell"],
              "changed: Conduct & review: a row per design Task, its Runs folded (261008)",
              ""),
    "cards": (fx("Block", "Description", "Goals"), "parent:.space-main details",
              ["one closed row per item: ▸ name · its facts, opened in place (the design's folding card, s11 · s12)",
               "the same row for a goal, a method, a Run, a design"],
              "changed: the dropped plain and folded, no red box (261008)",
              ""),
    "runs": (fx("Job", "Work Details", "Conduct & review"), "section.runs-panel",
             ["Disk, then Runs, one panel, one fold (b03 s32-D08)",
              "one row per run type, named run-<type>-<target>; a type's Runs as rows"],
             "changed: 4 Runs per type, then +N more, as Disk (base, 261008)",
             ""),
    "tags": (("none",), "",
             ["none: no tags in any theme (b03 s32-D09)", "a state is a word (passed · verify · revise · dropped)",
              "an id is plain text where it stands (I04, d04, run-verify-d04-v1)"],
             "changed: no tags; the chips removed, an id in mono with its words (261008)",
             ""),
    "header": (fx("Job", "Description"), "header",
               ["one line: the theme's icon · Design · the folder; the path on hover", "no band, no counts line above the tabs"],
               "kept: one line, no band (the old board's blue band retires)",
               "? none open"),
    "item": (fx("d04", "Description", "Design"), ".space-main",
             ["one design opens as its own Task (s13): Description › Design is the Job's design card, opened",
              "no item page beside the frame: the design item page retires"],
             "built: a design is a Task, Description › Design (s13)",
             "? an older Design Folder on the frame embeds its old item page (Work Details › Designs) until it moves onto the ladder"),
    "design": (fx("Job", "Audience Report", "Design display"), ".space-main",
               ["one row per design: the design as it reads │ its process (③) │ its review (④ ⑤)",
                "the first open, the rest one line each; the dropped folded, kept for the record"],
               "changed: a UI design shows its screens/ PNG in the phone's cell (261008)",
               "? no UI design on the ladder yet to show it with (the sample is SMS only)"),
    "phone": (fx("Job", "Audience Report", "Design display"), "[data-bubble]",
              ["a design reads as its reader sees it (s11 · s12): an SMS is one phone bubble, {LINK} where it goes",
               "the same phone in Design display, Drafts, Predicted vs observed and Delivery"],
              "kept: one phone for an SMS, the theme's own (b03, 261008)",
              ""),
    "map": (fx("Block", "Description", "Map"), ".space-main",
            ["goals down, registered methods across, a cell the chain of Jobs (s11)", "two Jobs of one cell compare in a pop-out"],
            "changed: a column per registered method, empty where no Job (261008)",
            ""),
    "inputs": (fx("Job", "Description", "Inputs"), ".space-main",
               ["the Job's inputs/ is the only folder the design work sees (s12)",
                "its parts by step ①, each file's source and sha256, the frozen manifest"],
               "changed: each choice as plain text, no chip (261008)",
               ""),
    "chains": (fx("t00", "Audience Report", "Topics"), ".space-main",
               ["one card per topic: from · says · so → its ideas (s13)", "Job › Reason ideas shows the same, read from t00"],
               "changed: idea ids in mono with their words, no chip (261008)",
               ""),
    "observed": (fx("Block", "Audience Report", "Predicted vs observed"), ".space-main",
                 ["each tested design as it reads, its frozen prediction beside the Exp's arm (s11)",
                  "Cost, scorecard and Performance as the frame's table"],
                 "built: predicted vs observed, scorecard, cost (s11 · s12)",
                 "? tokens show '—': the Run receipt has no usage: yet (another owner, s11)"),
    "review": (fx("d04", "Audience Report", "Tests"), ".space-main",
               ["④ a table of the reviewer's tests per draft, ⑤ the ranking with its kept line",
                "the reviewer is always another agent (s13)"],
               "built: Tests from each run-verify, Ranking from run-rank-t99 (s13)",
               "? the sample's verify Runs carry T0 · T1 only, so s13's T2 critique and T3 pretest are not seen here yet"),
}
# the extra pictures of a proposed frame, below its first: (source, selector, caption)
EXTRA_PROPOSALS = {
    "space": [(fx("t00", "Audience Report", "Topics"), ".split", "the same body at a Task: t00's topics")],
    "design": [(fx("Block", "Work Details", "All"), ".space-main", "the Block's Work Details previews each Job's designs as small phones")],
}

# what the design theme draws, by level (JL 261008, by way of b03: "which element UI each level will use")
# (element, level, Space › view, base or its own and why, served today, gap)
THEME_ELEMENTS = [
    ("top tabs", "every level", "the level row and the six Spaces", "the base", "yes",
     ""),
    ("view row", "every level", "every Space's views", "the base", "yes", ""),
    ("Question rows", "Block", "Audience Report › Questions", "the base (Insight's row)", "yes", ""),
    ("Question-style row", "Block · Job · Task", "Predicted vs observed; Description › Design",
     "the base row, columns Design │ Predicted │ Observed", "yes", ""),
    ("Space body + Disk · Runs", "every level", "every Space", "the base", "yes", ""),
    ("table", "every level", "Map, Inputs, Cost, Ranking, Ideas, Elements, Tests, Runs", "the base", "yes",
     ""),
    ("folding row (card)", "Block · Job · Task", "Goals, Methods, Inputs, Runs, Method, Kept · Dropped",
     "the base row; s11 · s12 call it the folding card", "yes", ""),
    ("Runs panel", "every level", "every Space", "the base (4 per type, then +N more)", "yes", ""),
    ("tags", "Job · t00", "Inputs choices; Reason ideas, Topics idea ids", "none (b03 s32-D09)", "drawn as chips",
     ""),
    ("header", "every level", "top line", "the base", "yes", ""),
    ("design card (Design │ Process │ Review)", "Job · Task", "Audience Report › Design display; Task Description › Design",
     "its own: a design is read three ways side by side", "yes", "no UI design on the ladder yet to show"),
    ("Design display", "Job", "Audience Report › Design display", "its own: the N designs in order, dropped folded",
     "yes", ""),
    ("phone (a design as it reads)", "Block · Job · Task", "Design display, Drafts, Predicted vs observed, Delivery",
     "its own: a design shows as its reader sees it (b03, 261008)", "yes", ""),
    ("goal × method Map", "Block", "Description › Map (+ compare pop-out)", "its own: Jobs placed by goal and method",
     "yes", ""),
    ("inputs fence", "Block · Job", "Description › Inputs", "its own: what the design work may see", "yes",
     ""),
    ("Reason ideas (chains)", "Job · t00", "Audience Report › Reason ideas; t00 › Topics, Chains",
     "its own: step ②'s topics and chains", "yes", ""),
    ("Review whole (ranking)", "Job · t99", "Audience Report › Review whole; t99 › Ranking, Coverage, Kept · Dropped",
     "the base table + its own kept line", "yes", ""),
    ("Tests (④)", "Task", "Audience Report › Tests; Description › Evaluation", "the base table", "yes", "T2 · T3 not in the sample yet"),
    ("predicted vs observed, scorecard, cost", "Block · Job · Task", "Audience Report views; Performance",
     "the base table + the phone", "yes", "tokens empty: no usage: in the receipt"),
    ("Idea Studio", "every level", "Idea Studio", "the base (b03 s32-D06)", "yes", ""),
    ("one design's own page", "(old)", "/_board/design", "retires: a design is a Task", "old page", ""),
]

PICKED = {"tabs": "D · E (b03 s32-D01)", "views": "E (b03 s32-D02)", "report": "the Question cell as Insight's (b03 s32-D05)",
          "runs": "Disk inside the Runs panel (b03 s32-D08)", "tags": "none (b03 s32-D09)",
          "design": "Job › Audience Report › Design display (b03 s32-D11)"}
CHANGES = ["new topic: the design theme's element gallery, after b03's s32 (b03's picks hold)",
           "the ladder levels shot live from a fixture host (design_fixture.py), the old pages from the SPACE's host",
           "s11 · s12 · s13's planned screens drawn beside today's, by their own builders",
           "a Theme elements frame: what each level uses, base or its own, gaps in red (asked by b03)",
           "b03's rulings on the 9 gaps: Runs paging and the select hook in the base, the rest fixed in the design theme"]

BUBBLE_JS = ("document.querySelectorAll('div').forEach(d => { const f = d.firstElementChild;"
             " if (f && f.textContent.trim() === 'Text message') d.setAttribute('data-bubble', '1'); })")


# ── shooting ────────────────────────────────────────────────────────────────────────────────────────
def start_fixture_host():
    """The design tests' placeholder Project in a temp folder, served by a second host. Returns (url, proc, dir)."""
    tmp = Path(tempfile.mkdtemp(prefix="s32-design-fx-"))
    py = SPACE / ".venv" / "bin" / "python"
    sys.path.insert(0, str(SERVERS / "workbench-design" / "tests"))
    done = subprocess.run([str(py), str(SERVERS / "workbench-design" / "tests" / "design_fixture.py"), str(tmp)],
                          capture_output=True, text=True)
    if done.returncode:
        raise SystemExit("design fixture: " + done.stderr.strip().splitlines()[-1])
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen([str(py), str(SERVERS / "_host" / "serve.py"), "--root", str(tmp), "--port", str(port),
                             "--host", "127.0.0.1", "--no-auth", "--no-terminal"], cwd=str(SPACE),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}"
    for _ in range(60):
        try:
            urllib.request.urlopen(url + "/", timeout=1)
            return url, proc, tmp
        except Exception:
            time.sleep(0.5)
    proc.terminate()
    raise SystemExit("the fixture host did not start")


def url_of(src, base_url, fx_url_base):
    if src[0] == "fx":
        return fx_url_base + fx_url(*src[1:])
    return base_url + OLD_PAGES[src[1]][1]


def shoot(base_url: str) -> None:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    for f in SHOTS.glob("*.png"):
        f.unlink()
    facts, missing = {}, []
    fx_base, proc, tmp = start_fixture_host()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome", headless=True)
            page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
            current = [None]

            def grab(src, sel, out, label):
                url = url_of(src, base_url, fx_base)
                if current[0] != url:
                    try:
                        resp = page.goto(url, timeout=60000)
                    except Exception as err:          # a slow or busy host: skip this card, say so
                        missing.append(f"{out}: {type(err).__name__}")
                        current[0] = None
                        return
                    page.wait_for_timeout(1500 if src[0] == "old" else 500)
                    page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
                    page.evaluate(BUBBLE_JS)
                    page.wait_for_timeout(150)
                    current[0] = url
                    if not resp or resp.status != 200:
                        missing.append(f"{out}: HTTP {resp.status if resp else '?'}")
                        return
                box = None
                for alt in sel.split(","):
                    box = page.evaluate(E.PICK_JS, alt.strip())
                    if box:
                        break
                if not box:
                    missing.append(f"{out}: {sel} not found")
                    return
                page.screenshot(path=str(SHOTS / f"{out}.png"), full_page=True,
                                clip={"x": box["x"], "y": box["y"], "width": max(box["w"], 1),
                                      "height": min(max(box["h"], 1), E.MAX_H)})
                facts[out] = {"page": label, "url": url.replace(fx_base, "<fixture>").replace(base_url, ""),
                              "selector": sel, "cut": box["h"] > E.MAX_H, **box["style"]}

            for ekey, _, _, cards in ELEMENTS:
                for i, (src, sel) in enumerate(cards):
                    grab(src, sel, f"{ekey}__{i:02d}", label_of(src))
            for ekey, (src, sel, *_) in PROPOSALS.items():
                if src[0] != "none":
                    grab(src, sel, f"proposed__{ekey}", "proposed")
            for ekey, extras in EXTRA_PROPOSALS.items():
                for n, (src, sel, _) in enumerate(extras, 1):
                    grab(src, sel, f"proposed__{ekey}__{n}", "proposed")
            browser.close()
    finally:
        proc.terminate()
        shutil.rmtree(tmp, ignore_errors=True)
    (SHOTS / "facts.json").write_text(json.dumps(facts, indent=1, ensure_ascii=False))
    print(f"{len(facts)} shots in {SHOTS.relative_to(HERE.parent)}")
    for m in missing:
        print("  not shot:", m)


# ── the planned screens (s11 · s12 · s13's own builders) ──────────────────────────────────────────────
_MODS = {}
LEVEL_BUILDERS = {"s11": ("s11-design-block/build_s11_design_block.py", "Block", 980),
                  "s12": ("s12-design-job/build_s12_design_job.py", "Job", 1180),
                  "s13": ("s13-design-task/build_s13_design_task.py", "Task", 980)}


def level_module(topic):
    if topic not in _MODS:
        rel, _, _ = LEVEL_BUILDERS[topic]
        spec = importlib.util.spec_from_file_location(f"b12_{topic}_builder", HERE.parent / rel)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MODS[topic] = mod
    return _MODS[topic]


def planned_screen(topic, band, space, view, x, y) -> float:
    """One planned screen at (x, y), drawn by its level's builder; returns its height (0 if not found)."""
    mod = level_module(topic)
    _, level, sh = LEVEL_BUILDERS[topic]
    tab_text = None
    screens = getattr(mod, "SCREENS", [])
    if topic == "s13":
        b = {"t00": "BAND_A", "d04": "BAND_B", "t99": "BAND_C"}[band]
        screens = getattr(mod, b)
        tab_text = next(t for name, _, t, scs in mod.BANDS if scs is screens)
    for sc in screens:
        sp, third, runs, recent, body, _, _ = U._split(sc)
        on = [lab.lstrip("? ") for lab, o in (third or []) if o]
        if sp == space and ((not view and not third) or view in on):
            U.SH = sh
            body(*U.screen(x, y, level, sp, third, runs, recent, tab_text))
            return sh
    text(x, y, f"? {topic} draws no {space} › {view}", 20, RED)
    return 40


# ── the drawing ─────────────────────────────────────────────────────────────────────────────────────
CARD_W = E.CARD_W


def frame_element(ekey, title, what, cards, x0, y0, facts) -> dict:
    fr = L.open_frame(title)
    text(x0, y0, title, 34)
    shown = [(i, src) for i, (src, _) in enumerate(cards) if (SHOTS / f"{ekey}__{i:02d}.png").exists()]
    olds = sum(bool(old_reason(src)) for _, src in shown)
    text(x0, y0 + 50, f"{what} · {len(shown)} versions today, {olds} of them on old pages (flagged OLD: they retire; "
                      "a look from one may still be picked); then as s11 · s12 · s13 plan it", 18, GRAY)
    x, y, row_h = x0, y0 + 120, 0
    for n, (i, src) in enumerate(shown):
        if n and n % 3 == 0:
            x, y, row_h = x0, y + row_h + 80, 0
        f = facts.get(f"{ekey}__{i:02d}", {})
        why = old_reason(src)
        if why:                                   # an old page: flagged, a red dashed box around it
            text(x, y - 26, "OLD · " + why, 14, RED)
        text(x, y, f"{chr(65 + n)} · {label_of(src)}", 20, GRAY if why else INK)
        h = E.picture(SHOTS / f"{ekey}__{i:02d}.png", x, y + 40, CARD_W)
        if why:
            base("rectangle", x - 8, y + 32, E.LAST_W[0] + 16, h + 16, RED, 1.5, dashed=True, rough=0)
        text(x, y + 52 + h, E.style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 14, GRAY, MONO)
        row_h = max(row_h, 52 + h + 60)
        x += CARD_W + 80
    if not shown:
        text(x0, y0 + 120, "no shots yet: run with --shoot", 18, RED)
    gone = [label_of(src) for i, (src, _) in enumerate(cards) if not (SHOTS / f"{ekey}__{i:02d}.png").exists()]
    y += row_h + 40
    if gone and shown:
        text(x0, y, "? not on the page today: " + " · ".join(gone), 16, RED)
        y += 40
    planned = PLANNED.get(ekey, [])
    if planned:
        text(x0, y + 20, "as planned · drawn in s11 · s12 · s13, the same screen as there (black lines, not served yet)", 22)
        px, ph = x0, 0
        for k, (topic, band, space, view) in enumerate(planned):
            where = f"P{k + 1} · {topic}" + (f" · {band}" if band else "") + f" · {space}" + (f" › {view}" if view else "")
            text(px, y + 70, where, 20)
            ph = max(ph, planned_screen(topic, band, space, view, px, y + 110))
            px += U.SW + 120
    L.close_frame(fr)
    return fr


def frame_proposed(ekey, title, x0, y0, facts) -> dict:
    fr = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    src, _, why, changed, open_ = PROPOSALS[ekey]
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench); the design theme gives the words "
                      "and, for its own elements, the layout", 18, GRAY)
    y = y0 + 110
    text(x0, y, changed, 20, GREEN)              # green: what changed (or is kept) here
    y += 40
    if open_ and open_ != "? none open":
        text(x0, y, open_, 18, RED)              # red: still open
        y += 40
    shot = SHOTS / f"proposed__{ekey}.png"
    if shot.exists():
        h = E.picture(shot, x0, y, 1000)
        text(x0, y + h + 12, E.style_line(facts.get(f"proposed__{ekey}", {})), 14, GRAY, MONO)
        y += h + 70
    elif src[0] == "none":
        text(x0, y, "(none)", 28, GRAY)
        y += 60
    else:
        text(x0, y, "no shot yet: run with --shoot", 18, RED)
        y += 40
    for n, (_, _, caption) in enumerate(EXTRA_PROPOSALS.get(ekey, []), 1):
        extra = SHOTS / f"proposed__{ekey}__{n}.png"
        if extra.exists():
            text(x0, y, caption, 17)
            h = E.picture(extra, x0, y + 34, 1000)
            y += h + 80
    text(x0, y + 10, "why", 22)
    for i, line in enumerate(why):
        text(x0 + 20, y + 50 + i * 30, "· " + line, 17)
    L.close_frame(fr)
    return fr


def frame_title(x0, y0) -> dict:
    fr = L.open_frame("s32 · Design element UI")
    text(x0, y0, "s32 · Design element UI: every element the design theme draws, today and as planned", 40)
    text(x0, y0 + 60, "after b03's s32-element-ui; one frame per element (a card per version today, then the planned screen "
                      "from s11 · s12 · s13), its '· proposed' frame to the right; OLD = an old page, red dashed", 20, GRAY)
    for k, c in enumerate(CHANGES):
        L.els.append(canvas.change_note(x0, y0 + 120 + k * 30, c, "261008", L.FRAME[0], 18))
    L.close_frame(fr)
    return fr


def frame_theme_elements(x0, y0) -> dict:
    fr = L.open_frame("Theme elements")
    text(x0, y0, "Theme elements: what the design theme uses, by level", 34)
    text(x0, y0 + 50, "element · level · Space › view · the base's or its own (why) · drawn today; red = a gap", 18, GRAY)
    cols = (0, 430, 760, 1460, 2280)
    for c, h in zip(cols, ("element", "level", "Space › view", "base or its own", "today")):
        text(x0 + c, y0 + 110, h, 18, GRAY)
    for k, (el, lv, where, own, today, gap) in enumerate(THEME_ELEMENTS):
        y = y0 + 150 + k * 40
        for c, s in zip(cols, (el, lv, where, own, today)):
            text(x0 + c, y, s, 17)
        if gap:
            text(x0 + cols[-1] + 170, y, "? " + gap, 17, RED)
    L.close_frame(fr)
    return fr


def frame_pick(x0, y0) -> dict:
    fr = L.open_frame("Pick")
    text(x0, y0, "Pick: one look per element", 34)
    text(x0, y0 + 50, "write the letter you keep beside each (or a new one); b03's picks already hold", 18, GRAY)
    for i, (key, title, what, _) in enumerate(ELEMENTS):
        text(x0, y0 + 120 + i * 44, title, 20)
        if key in PICKED:
            text(x0 + 700, y0 + 120 + i * 44, "kept: " + PICKED[key], 20, GREEN)
        else:
            text(x0 + 700, y0 + 120 + i * 44, "? keep: __ (proposed: " + PROPOSALS[key][3].split(":", 1)[-1].strip() + ")", 20, RED)
    L.close_frame(fr)
    return fr


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    E.FILES.clear()
    title = frame_title(0, -1700)
    te = frame_theme_elements(title["x"] + title["width"] + 200, -1700)
    frame_pick(te["x"] + te["width"] + 200, -1700)
    y = max(title["y"] + title["height"], te["y"] + te["height"]) + 300
    for ekey, title_, what, cards in ELEMENTS:
        fr = frame_element(ekey, title_, what, cards, 0, y, facts)
        pr = frame_proposed(ekey, title_, fr["x"] + fr["width"] + 200, y, facts)
        y = max(fr["y"] + fr["height"], pr["y"] + pr["height"]) + 200
    canvas.write(out, list(L.els), Path(__file__).name, files=E.FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        url = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://127.0.0.1:5851"
        shoot(url.rstrip("/"))
    draw(Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].endswith(".excalidraw")
         else HERE / "s32-design-element-ui.excalidraw")
