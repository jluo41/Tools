"""b13 s32 · Cowork element UI: s32-cowork-element-ui.excalidraw, the cowork theme's element gallery (b03's
s32-element-ui, cut to one theme): every kind of element the cowork theme draws, as it draws it today on the frame
(/_board/workbench at its Block, Job and Task levels, every Space and view) and on its old board page
(/_board/cowork-board, flagged OLD), as b03's s11 · s12 cowork rows plan it, and beside each element a
"· proposed" frame: the unified look (b03's picks hold), why, a green line for what changed and a red line for
what is open. Then the buttons that have no Run name yet, each with a proposed run-<type>-<target>.

Two steps:

    uv run --no-project --with playwright --with pillow python build_s32_cowork_element_ui.py --shoot [--base http://127.0.0.1:5851]
        (--no-project: inside the SPACE, uv would otherwise build the SPACE's own environment)
        No cowork Block is on disk in this SPACE (261008), so the ladder levels and the old board page come from
        a placeholder Block (cowork_fixture.py, the cowork theme's test Block and a little more): written to a
        temp folder and served live by a second host (the same serve.py, --root that folder, a free port), shot,
        then stopped. The SPACE's host (--base) gives the old page's every-Project list and the base's Question
        row on a real Block. Each element goes to shots/<element>__NN.png, its first control's computed style
        to shots/facts.json; the walk over every level × Space × view writes each page's buttons there too.
    python build_s32_cowork_element_ui.py
        draws the gallery from shots/ and the planned screens from b03's shared cowork rows; marks are kept on
        rebuild (canvas.write).

The shooting and picture helpers are b03's (../../../b03_project_workbench/studio/s32-element-ui/
build_s32_element_ui.py), imported; the planned screens are drawn by b03's shared ladder helpers
(s01-overall-tree-structure: build_ladder_v4.wireframe, level_views' cowork Job views), so a change there shows
here on the next build. Placeholders only.
"""
from __future__ import annotations

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
SPACE = Path(__file__).resolve().parents[5]
TOOLS = Path(__file__).resolve().parents[4]
SERVERS = TOOLS / "plugins" / "haipipe-toolkit" / "servers"
sys.path.insert(0, str(TOOLS / "blueprints" / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio" / "s32-element-ui"))
import build_s32_element_ui as E  # noqa: E402  (b03's gallery: PICK_JS, picture, style_line; it loads L and canvas)
import level_views as LV  # noqa: E402  (b03's level views: the cowork Job's planned screens; on E's path)
sys.path.insert(0, str(HERE))
import cowork_fixture as FX  # noqa: E402  (the placeholder cowork Block)

L, canvas = E.L, E.canvas
INK, RED, GREEN, MONO = canvas.INK, canvas.RED, canvas.GREEN, L.MONO
text, base = L.text, L.base
q = E.q
DATE = "261008"

# ── where each card comes from ──────────────────────────────────────────────────────────────────────
BL = FX.PROJECT + "/" + FX.BLOCK                       # the placeholder Block, on the fixture host
FOLDER = {"Block": BL, "Job": BL + "/j01_request", "Job·j02": BL + "/j02_review", "Job·j03": BL + "/j03_done",
          "Task": BL + "/j01_request/t01_protocol"}
LEVEL_LABEL = {"Block": "Block b01", "Job": "Job j01 (has a Task)", "Job·j02": "Job j02 (waiting on us)",
               "Job·j03": "Job j03 (done, no Task)", "Task": "Task t01 (a document in rounds)"}
SPACES = ("Description", "Idea Studio", "Audience Report", "Work Details", "Runs", "Delivery")
WALKED = ("Block", "Job", "Job·j03", "Task")          # every Space and view of these is walked
OLD_VIEWS = {"scope": ("block", "people", "resources", "studio"), "work": ("jobs", "questions", "emails", "meetings"),
             "check": ("waiting", "drafts", "progress"), "delivery": ("delivery", "done")}
OLD_NAME = {"block": "Scope › Block", "people": "Scope › People", "resources": "Scope › Resources",
            "studio": "Scope › RoadMap Draw", "jobs": "Work › Jobs", "questions": "Work › Questions",
            "emails": "Work › Emails", "meetings": "Work › Meetings", "waiting": "Check › Waiting on",
            "drafts": "Check › Drafts", "progress": "Check › Reports", "delivery": "Delivery › Reports",
            "done": "Delivery › Done jobs"}
EMAIL = "j01_request/emails/2026-10-03-v2-draft.md"
# on the SPACE's host: the old page's every-Project list, and the base's Question row on a real Block (b13 itself,
# a design Block the frame draws with the base's rows)
SPACE_PAGES = {"old-projects": ("the old CoWork page · every Project (/_board/cowork-board, no Block)", "/_board/cowork-board"),
               "b13-report": ("the frame · a Block on the base's rows (b13 itself), Audience Report",
                              "/_board/workbench?" + UP.urlencode({"path": "Tools/blueprints/b13_theme_cowork",
                                                                   "space": "Audience Report"}))}


def fx(level, space, view=""):
    return ("fx", level, space, view)


def old(view):
    return ("old", view)


def frame_url(folder, space="", view=""):
    query = {"path": folder}
    if space:
        query["space"] = space
    if view:
        query["sub"] = view
    return "/_board/workbench?" + UP.urlencode(query)


def url_of(src, fx_base, space_base):
    kind = src[0]
    if kind == "fx":
        return fx_base + frame_url(FOLDER[src[1]], src[2], src[3])
    if kind == "old":
        return fx_base + "/_board/cowork-board?" + UP.urlencode({"path": BL, "view": src[1]})
    if kind == "old-show":
        return fx_base + "/_board/cowork-board?" + UP.urlencode({"path": BL, "show": src[1]})
    if kind == "old-report":
        return fx_base + "/_board/cowork-board?" + UP.urlencode({"path": BL, "report": src[1]})
    if kind == "reader":
        return fx_base + "/_board/page?" + UP.urlencode({"path": "/" + BL + "/" + src[1]})
    return space_base + SPACE_PAGES[src[1]][1]


def label_of(src) -> str:
    kind = src[0]
    if kind == "fx":
        _, level, space, view = src
        return f"the frame · {LEVEL_LABEL[level]} › {space}" + (f" › {view}" if view else "")
    if kind == "old":
        return f"the old CoWork page · {OLD_NAME[src[1]]}"
    if kind == "old-show":
        return f"the old CoWork page's file pop-out · {src[1]}"
    if kind == "old-report":
        return f"the old CoWork page's report pop-out · {src[1]}"
    if kind == "reader":
        return f"the Page reader (a row's link) · {src[1].rsplit('/', 1)[-1]}"
    return SPACE_PAGES[src[1]][0]


def old_reason(src) -> str:
    """Why a card's page is old, read off the code; "" for the frame (and the Page reader)."""
    oldpage = src[0] in ("old", "old-show", "old-report") or (src[0] == "space" and src[1] == "old-projects")
    if oldpage and (SERVERS / "workbench-cowork" / "cowork_theme.py").is_file():
        return "old page: retires (cowork draws on the frame)"
    return ""


# ── the elements: (key, title, what, [(card source, selector)]) ──────────────────────────────────────
# a selector as b03's: "a|b" the box around both, "parent:x" x's parent, "a,b" the first found
TABS, SUBS, SPLIT, MAIN, RUNS = "nav.levels|nav.spaces", "nav.subs", ".split", ".space-main", "section.runs-panel"
OLD_MAIN = ".pane.on .space-main"
ELEMENTS = [
    ("tabs", "1 · Top tabs", "the level row (Guide · Block · Job ▾ · Task ▾) and the six Spaces",
     [(fx("Block", "Audience Report"), TABS), (fx("Job", "Audience Report"), TABS), (fx("Job·j03", "Audience Report"), TABS),
      (fx("Task", "Audience Report"), TABS), (old("jobs"), "nav.spaces")]),
    ("views", "2 · View row (third row)", "the views of the open Space",
     [(fx("Block", "Description"), SUBS), (fx("Block", "Work Details"), SUBS), (fx("Block", "Delivery"), SUBS),
      (fx("Block", "Runs"), SUBS), (fx("Job", "Description"), SUBS), (fx("Job", "Work Details"), SUBS),
      (fx("Job", "Runs"), SUBS), (fx("Task", "Description"), SUBS), (fx("Task", "Work Details"), SUBS),
      (old("block"), ".pane.on .wtabs"), (old("jobs"), ".pane.on .wtabs"), (old("waiting"), ".pane.on .wtabs")]),
    ("report", "3 · Audience Report rows", "one Question with its work and its report: Question │ Work │ Report",
     [(fx("Block", "Audience Report"), "table.wf-table"), (fx("Job", "Audience Report"), "table.wf-table"),
      (fx("Task", "Audience Report"), MAIN), (old("questions"), ".pane.on .hl-row"),
      (old("progress"), ".pane.on .card")]),
    ("space", "4 · The Space body", "the open Space's box beside Disk · Runs, its first screen (its first view)",
     [(fx(lv, sp), SPLIT) for lv in ("Block", "Job", "Task") for sp in SPACES]
     + [(old(views[0]), ".pane.on .split") for views in OLD_VIEWS.values()]
     + [(("space", "old-projects"), "main")]),
    ("table", "5 · Tables", "rows of items in a table",
     [(fx("Block", "Work Details", "All"), "table.wf-table"), (fx("Block", "Description", "Scope"), "table.wf-table"),
      (fx("Block", "Description", "Resources"), "table.wf-table"), (fx("Block", "Runs"), "table.wf-table"),
      (fx("Block", "Delivery", "Done jobs"), "table.wf-table"), (fx("Job", "Description", "Job"), "table.wf-table"),
      (fx("Job", "Work Details", "Checklist"), "table.wf-table"), (fx("Job", "Runs"), "table.wf-table"),
      (old("jobs"), ".pane.on table"), (old("emails"), ".pane.on table"), (old("block"), ".pane.on table")]),
    ("cards", "6 · Rows and cards", "one item, closed or open",
     [(fx("Block", "Idea Studio"), "parent:.space-main details"), (old("studio"), ".pane.on details.draw"),
      (old("resources"), ".pane.on details.draw"), (old("jobs"), ".pane.on details.ws"),
      (old("delivery"), ".pane.on .card"), (old("questions"), ".pane.on details.q-more")]),
    ("runs", "7 · Disk · Runs panel", "the files behind the open Space, its run types and their Runs (Disk inside, one fold)",
     [(fx("Block", "Audience Report"), RUNS), (fx("Block", "Runs"), RUNS), (fx("Job", "Work Details"), RUNS),
      (fx("Job", "Runs"), RUNS), (fx("Task", "Runs"), RUNS), (old("jobs"), ".pane.on .runs-panel"),
      (old("waiting"), ".pane.on .runs-panel")]),
    ("tags", "8 · Tags and pills", "a state, an id or a count on an item",
     [(old("jobs"), "parent:.pane.on .pill"), (old("emails"), "parent:.pane.on .pill"),
      (old("questions"), "parent:.pane.on .rp-tags"), (old("block"), "parent:.pane.on .idtag"),
      (old("progress"), "parent:.pane.on .card .pill"), (fx("Job", "Work Details", "Timeline"), "parent:td b")]),
    ("header", "9 · Page header", "the title line at the top",
     [(fx("Block", "Description"), "header"), (fx("Job", "Description"), "header"), (fx("Task", "Description"), "header"),
      (old("jobs"), "header|.dataset"), (("old-show", EMAIL), "header"), (("space", "old-projects"), "header,h1")]),
    ("item", "10 · One item's display", "one email, one meeting, one report, one document: the item itself",
     [(fx("Job", "Work Details", "Emails"), MAIN), (("reader", EMAIL), "main,body"),
      (("reader", "reports/q01_ready/q01_ready.md"), "main,body"), (fx("Task", "Description"), MAIN),
      (("old-show", EMAIL), "body"), (("old-report", "Q01"), "body")]),
    # the cowork theme's own elements
    ("jobstate", "11 · A Job's state: waiting on · since · next (cowork only)",
     "who has the next move, since when, what is next: the Job page's header, read into rows",
     [(fx("Job", "Description", "Job"), MAIN), (fx("Block", "Work Details", "All"), MAIN),
      (fx("Job·j02", "Description", "Job"), MAIN), (old("jobs"), OLD_MAIN), (old("block"), OLD_MAIN)]),
    ("timeline", "12 · Timeline, checklist, emails, meetings (cowork only)",
     "a Job's items as dated rows, not Tasks (b13 Q01)",
     [(fx("Job", "Work Details", "Timeline"), MAIN), (fx("Job", "Work Details", "Checklist"), MAIN),
      (fx("Job", "Work Details", "Emails"), MAIN), (fx("Job", "Work Details", "Meetings"), MAIN),
      (old("emails"), OLD_MAIN), (old("meetings"), OLD_MAIN)]),
    ("people", "13 · People, resources, files (cowork only)", "who to ask and what the Block and its Jobs use",
     [(fx("Block", "Description", "People"), MAIN), (fx("Block", "Description", "Resources"), MAIN),
      (fx("Block", "Description", "Related"), MAIN), (fx("Job", "Description", "Files"), MAIN),
      (old("people"), OLD_MAIN), (old("resources"), OLD_MAIN)]),
    ("check", "14 · Waiting on, drafts, done (cowork only; was Check)", "who we wait on, what is not sent, what is done",
     [(fx("Block", "Work Details", "waiting"), MAIN), (fx("Block", "Work Details", "done"), MAIN),
      (fx("Block", "Delivery", "Done jobs"), MAIN), (fx("Job", "Runs"), MAIN), (old("waiting"), OLD_MAIN),
      (old("drafts"), OLD_MAIN), (old("progress"), OLD_MAIN), (old("done"), OLD_MAIN)]),
]

# ── as b03's s11 (Block) and s12 (Job) cowork rows plan it; cowork has no s13 row (a Task is the Page Task) ──
# ("Block", column of build_ladder_v4.BLOCK_COLUMNS) or ("Job", Space of level_views' cowork Job)
PLANNED = {
    "tabs": [("Job", "Description")], "views": [("Job", "Work Details")], "report": [("Block", "Reports"), ("Job", "Audience Report")],
    "space": [("Block", "Jobs")], "table": [("Block", "Runs")], "cards": [("Block", "Studio")],
    "runs": [("Job", "Runs")], "item": [("Job", "Work Details")], "jobstate": [("Job", "Description"), ("Block", "Jobs")],
    "timeline": [("Job", "Work Details")], "people": [("Block", "People"), ("Block", "Resources")],
    "check": [("Block", "Jobs"), ("Block", "Delivery"), ("Job", "Delivery")],
}

# ── the proposed look: (source, selector, why, changed (green), open (red)) ───────────────────────────
# b03's picks hold (s32-D01 tabs D · E, D02 view row E, D05 the Question cell as Insight's row, D08 Disk inside
# the Runs panel, D09 no tags); where the frame already draws the look, its own version is the proposal
PROPOSALS = {
    "tabs": (fx("Job", "Audience Report"), TABS,
             ["b03's D · E look (s32-D01): the cowork theme gives the words only (🤝 CoWork)",
              "Guide · Block · Job ▾ · Task ▾, then the six Spaces, the same at every level",
              "Task ▾ greyed until the open Job has a tNN_<doc>/ (b13 Q01), drawn by the base"],
             "kept: the base's D · E tabs; Task ▾ greyed without a document Task",
             "? the Job and Task selects read folder names (j01_request, t01_protocol), not the Job's title"),
    "views": (fx("Job", "Work Details"), SUBS,
              ["b03's E look (s32-D02): the tabs' shape, one family",
               "Block: Scope · People · Resources · Related | All · open · waiting · done; Job: Job · Files | "
               "Timeline · Checklist · Emails · Meetings (s11 · s12)"],
              "kept: the base's E view row at every level",
              "? one casing: open · waiting · done and delivery/ are lower case beside Timeline · Checklist; "
              "Job › Runs groups by email · meeting, s12 plans email · notes · update · check"),
    "report": (("space", "b13-report"), "parent:.q-row",
               ["one Question │ Work │ Report row per Question, as every theme (b03 s04-D04)",
                "the Question cell as the Insight row (b03 s32-D05): label pill and state dot, the slug, one "
                "sentence, › More; the base's question_cell(), as the frame draws it on a real Block",
                "the Job's Audience Report: the same rows, only the Block's Questions that cite this Job"],
               "proposed: Block and Job Audience Report take the base's row and question_cell() (b03 s32-D05)",
               "? to build in cowork_theme.py: both draw a plain table (Question │ Work │ Report), no label, no "
               "state dot, the status a word in the Report cell"),
    "space": (fx("Job", "Work Details"), SPLIT,
              ["one content box and one right column, Disk · Runs", "the cowork theme fills the box; it draws no page of its own"],
              "kept: the base's body at every level",
              "? the Task level draws the vanilla Task (Face · Folder | Folders · Evidence · Value), not the base's "
              "Page Task views (page_task_spaces), which b13 Q01 names for a document written in rounds"),
    "table": (fx("Block", "Work Details", "All"), "table.wf-table",
              ["the base's light table: small grey heads, rows ruled by one line",
               "Jobs, the Job's fields, the checklist, files and Runs are this table; an item with a body is a row (6)"],
              "kept: the base's table (wf-table) everywhere on the frame", ""),
    "cards": (fx("Block", "Idea Studio"), "parent:.space-main details",
              ["one closed row per item: ▸ name · its facts, opened in place (Idea Studio's topic rows, b03 s32-D06)",
               "the old page's folding cards (a Job's files, a resource, a drawing) become these rows"],
              "kept: the base's rows; the old page's details.draw cards retire with it", ""),
    "runs": (fx("Job", "Runs"), RUNS,
             ["Disk, then Runs, one panel, one fold (b03 s32-D08)",
              "one row per run type, named run-<type>-<target>, what it does under it; a type's Runs as rows"],
             "kept: Disk inside Runs; the server's Run names win, s12 now reads them (b03, 261008)",
             "? run-review-questions has no target; Draft a follow-up and Close the Job have no Run (cowork_theme.py, waits for JL)"),
    "tags": (("none",), "",
             ["none: no tags in any theme (b03 s32-D09)", "a state is a word: open · waiting · done, draft ✎",
              "an id is plain text where it stands (j01_request, Q01, run-email-v2)"],
             "kept: the frame draws no tags for cowork (b03 s32-D09)",
             "the old page's pills (waiting on, draft, report status) and id tags retire with it"),
    "header": (fx("Job", "Description"), "header",
               ["one line: 🤝 CoWork · the folder; the path on hover",
                "no band: the old page's counts line (open jobs · waiting on others · drafts) goes"],
               "kept: one line, no band", "? the old page's icon was 📨, the frame's is 🤝: one icon"),
    "item": (fx("Job", "Work Details", "Emails"), MAIN,
             ["an email, a meeting or a step is a row of its Job (b13 Q01), not a Task: it opens in the frame's "
              "pop-out from its row, the frame staying behind it",
              "a document written with others in rounds is a Page Task: the Task tab"],
             "proposed: a row opens its file in the pop-out (pop(), not link())",
             "? to build in cowork_theme.py: a row's link opens the Page reader in place of the workbench"),
    "jobstate": (fx("Job", "Description", "Job"), MAIN,
                 ["the Job page's header is the only place its state is written: state · waiting-on · since · "
                  "next · ticket · url (b13 Q01)", "the Block's Jobs rows read the same fields, the days waited after"],
                 "built: Job › Description › Job and Block › Work Details rows (cowork_theme.py)",
                 "? waiting-on and since are separate fields; s11 plans one line \"waiting on <person> · 3 days\""),
    "timeline": (fx("Job", "Work Details", "Timeline"), MAIN,
                 ["Timeline: every dated thing of the Job, newest first (entries, emails, meetings)",
                  "Checklist · Emails · Meetings as the base table; a draft reads draft ✎"],
                 "built: Timeline · Checklist · Emails · Meetings (cowork_theme.py)",
                 "? s12 plans a state per row (waiting 3 days · done · notes); today only a draft has one"),
    "people": (fx("Block", "Description", "Resources"), MAIN,
               ["People, Resources, Related and a Job's Files are lists of what the work uses: the base's table"],
               "built: Resources and Files as the base table",
               "? People shows j00_people.md as written (a <pre>), not rows; s11 plans person · role · waiting on · "
               "since; whether j00_people/ becomes people.md is JL's call (Q01)"),
    "check": (fx("Block", "Work Details", "waiting"), MAIN,
              ["Check retires (b13 Q01): Waiting on is Block › Work Details › waiting, Drafts are open "
               "run-email-<thread> Runs, Reports is run-check-<qNN>, done Jobs are Delivery › Done jobs"],
              "changed: no Check Space; its views live in Work Details, Runs and Delivery",
              "? Q02 is still open: no stale state on a Job row; Draft a follow-up has no Run name"),
}

# what the cowork theme draws, by level (b03 asks each theme: "which element UI each level will use")
# (element, level, Space › view, base or its own and why, drawn today or "GAP: …")
THEME_ELEMENTS = [
    ("top tabs", "every level", "the level row and the six Spaces", "the base", "drawn"),
    ("Task ▾ greyed", "Block · Job", "the level row", "the base (a Job without tNN_<doc>/ has no Task)", "drawn"),
    ("view row", "every level", "every Space's views", "the base", "drawn · GAP: one casing (open · waiting · done)"),
    ("Question rows", "Block", "Audience Report", "the base (Insight's row)", "GAP: a plain table, no question_cell()"),
    ("Question rows", "Job", "Audience Report (the Block's Questions citing this Job)", "the base (Insight's row)",
     "GAP: a plain table, no question_cell()"),
    ("Space body", "every level", "every Space", "the base", "drawn"),
    ("table", "Block · Job", "Scope, Resources, Jobs, Runs, Done jobs; Job, Files, Checklist, Emails, Meetings",
     "the base (wf-table)", "drawn"),
    ("rows", "every level", "Idea Studio", "the base (b03 s32-D06)", "drawn"),
    ("Disk · Runs panel", "every level", "every Space", "the base", "drawn (Run names as the server's, b03 261008)"),
    ("tags", "—", "—", "none (b03 s32-D09)", "drawn: none on the frame"),
    ("header", "every level", "the top line", "the base", "drawn"),
    ("one item", "Job", "Work Details › Emails · Meetings · Timeline", "the base's pop-out",
     "GAP: a row's link leaves the frame for the Page reader"),
    ("Job state", "Block · Job", "Work Details › All · open · waiting · done; Description › Job",
     "its own: the Job page's header fields are cowork's only state", "drawn"),
    ("Timeline", "Job", "Work Details › Timeline", "its own: every dated thing of a Job, newest first", "drawn"),
    ("Checklist · Emails · Meetings", "Job", "Work Details", "the base table, cowork's words", "drawn"),
    ("People", "Block", "Description › People", "its own: who to ask, their role, who we wait on",
     "GAP: j00_people.md as written, not rows"),
    ("Resources · Related · Files", "Block · Job", "Description › Resources · Related; Job › Files", "the base table",
     "drawn"),
    ("Done jobs", "Block", "Delivery › Done jobs", "the base table", "drawn · GAP: Q03 open (what a Job delivers)"),
    ("Job Delivery", "Job", "Delivery", "the base (vanilla)", "GAP: no cowork content (b13 Q03)"),
    ("Page Task", "Task", "every Space", "the base's Page Task views", "GAP: the vanilla Task is drawn"),
    ("old CoWork page", "(old)", "/_board/cowork-board: Scope · Work · Check · Delivery", "retires: the frame draws cowork",
     "old page"),
]

# the buttons with no Run name yet (haipipe-run: every soft Run button named run-<type>-<target>), each with a
# proposed name: (button, where, proposed). The walk adds any button it finds without a run- name.
UNNAMED = [
    ("Draft a follow-up", "old page › Check › Waiting on (no frame button)", "run-email-<slug> (a follow-up is the thread's next pass)"),
    ("Add a paper", "Guide › Related Paper (the CoWork Guide)", "run-add-paper-<slug>"),
    ("Save resource (+ Add resource form)", "old page › Scope › Resources", "run-add-resource-<slug>"),
    ("Add drawing (form)", "old page › Scope › RoadMap Draw", "run-draw-<sNN>"),
    ("Edit (drawing)", "frame › Idea Studio (Edit) · old page › RoadMap Draw (Edit drawing)", "run-draw-<sNN> (a pass)"),
    ("Close the Job", "planned: s12 Job › Delivery (not drawn)", "run-close-<jNN>"),
    ("Review the questions", "frame › Block › Audience Report: run-review-questions, no target", "run-review-questions-<bNN>"),
]
RENAMES = [   # named differently by the server and b03 s12; decided (b03, 261008): the server's names win, s12 rebuilt
    ("Write meeting notes", "run-meeting-<slug>", "run-notes-<meeting>", "run-meeting-<slug>"),
    ("Update the Job", "run-face-<jNN>", "run-update-job", "run-face-<jNN>"),
    ("Review a draft", "run-review-email-<slug>", "run-check-<thread>", "run-review-email-<slug>"),
    ("Draft an email", "run-email-<slug>", "run-email-<thread>", "run-email-<slug>"),
]

PICKED = {"tabs": "D · E (b03 s32-D01)", "views": "E (b03 s32-D02)", "report": "the Question cell as Insight's (b03 s32-D05)",
          "runs": "Disk inside the Runs panel (b03 s32-D08)", "tags": "none (b03 s32-D09)"}
CHANGES = ["new topic: the cowork theme's element gallery, after b03's s32 (b03's picks hold)",
           "the ladder levels shot live from a placeholder Block on a fixture host (cowork_fixture.py); the SPACE "
           "holds no cowork Block",
           "b03's s11 · s12 cowork rows drawn as the planned screen beside today's",
           "Theme elements, and the buttons with no Run name, each with a proposed run-<type>-<target>",
           "b03's ruling: the server's Run names win (s12 rebuilt); the other gaps wait for JL in cowork_theme.py"]


# ── shooting ────────────────────────────────────────────────────────────────────────────────────────
def start_fixture_host():
    """The placeholder cowork Project in a temp folder, served by a second host. Returns (url, proc, dir)."""
    tmp = Path(tempfile.mkdtemp(prefix="s32-cowork-fx-"))
    FX.make(tmp)
    py = SPACE / ".venv" / "bin" / "python"
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen([str(py), str(SERVERS / "_host" / "serve.py"), "--root", str(tmp), "--port", str(port),
                             "--host", "127.0.0.1", "--no-auth", "--no-terminal"], cwd=str(SPACE),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}"
    for _ in range(80):
        try:
            urllib.request.urlopen(url + "/", timeout=1)
            return url, proc, tmp
        except Exception:
            time.sleep(0.5)
    proc.terminate()
    raise SystemExit("the fixture host did not start")


# every button on a page: inside the Runs panel its Run name (and what it does), elsewhere its words
BUTTONS_JS = """() => {
  const vis = e => { const r = e.getBoundingClientRect(); return r.width > 2 && r.height > 2; };
  const scope = document.querySelector('.pane.on') || document.querySelector('.space-main') || document.body;
  const panel = [...scope.querySelectorAll('.runs-panel button.run-type')].map(t => ({
      name: t.dataset.label || '', doing: (t.querySelector('.run-doing') || {}).textContent || ''}));
  const other = [...scope.querySelectorAll('button')].filter(b => vis(b) && !b.closest('.runs-panel')
      && !b.matches('.wtab,.space,.pop-x') && !b.closest('nav')).map(b => b.textContent.trim()).filter(Boolean);
  const tags = scope.querySelectorAll('.pill,.tag,.chip,.idtag,.rp-tags').length;
  return {panel, other: [...new Set(other)], tags};
}"""


def shoot(space_base: str) -> None:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    for f in SHOTS.glob("*.png"):
        f.unlink()
    facts, missing, walk = {}, [], []
    fx_base, proc, tmp = start_fixture_host()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome", headless=True)
            page = browser.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1)
            current, status = [None], [0]

            def visit(url):
                if current[0] == url:
                    return True
                try:
                    resp = page.goto(url, timeout=60000)
                except Exception as err:                 # a slow or busy host: skip, say so
                    missing.append(f"{url}: {type(err).__name__}")
                    current[0] = None
                    return False
                page.wait_for_timeout(700)
                page.evaluate("document.querySelectorAll('.runs-panel.folded').forEach(p => p.classList.remove('folded'))")
                page.wait_for_timeout(150)
                current[0] = url
                status[0] = resp.status if resp else 0
                return status[0] == 200

            def grab(src, sel, out, label):
                url = url_of(src, fx_base, space_base)
                if not visit(url) and not (src[0] == "reader" and status[0]):   # a reader error is itself shown
                    missing.append(f"{out}: not 200")
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
                facts[out] = {"page": label, "url": url.replace(fx_base, "<fixture>").replace(space_base, ""),
                              "selector": sel, "cut": box["h"] > E.MAX_H, "status": status[0], **box["style"]}

            # the walk: every level × Space × view on the frame, every view of the old page, and their buttons
            for level in WALKED:
                for space in SPACES:
                    if not visit(fx_base + frame_url(FOLDER[level], space)):
                        continue
                    subs = page.evaluate("[...document.querySelectorAll('nav.subs a')].map(a => a.textContent.trim())")
                    for i, sub in enumerate(subs or [""]):
                        if i and not visit(fx_base + frame_url(FOLDER[level], space, sub)):
                            continue
                        walk.append({"place": f"frame · {LEVEL_LABEL[level]} › {space}" + (f" › {sub}" if sub else ""),
                                     **page.evaluate(BUTTONS_JS)})
            for views in OLD_VIEWS.values():
                for view in views:
                    if visit(url_of(old(view), fx_base, space_base)):
                        walk.append({"place": f"old page · {OLD_NAME[view]}", **page.evaluate(BUTTONS_JS)})

            for ekey, _, _, cards in ELEMENTS:
                for i, (src, sel) in enumerate(cards):
                    grab(src, sel, f"{ekey}__{i:02d}", label_of(src))
            for ekey, (src, sel, *_) in PROPOSALS.items():
                if src[0] != "none":
                    grab(src, sel, f"proposed__{ekey}", "proposed")
            browser.close()
    finally:
        proc.terminate()
        shutil.rmtree(tmp, ignore_errors=True)
    facts["_walk"] = walk
    (SHOTS / "facts.json").write_text(json.dumps(facts, indent=1, ensure_ascii=False))
    print(f"{len(facts) - 1} shots, {len(walk)} pages walked, in {SHOTS.relative_to(HERE.parent)}")
    for m in missing:
        print("  not shot:", m)


# ── the planned screens: b03's s11 (Block) and s12 (Job) cowork rows, drawn by b03's own helpers ───────
def planned_block(col, x, y) -> float:
    """One Block column as s11's block_views draws it for cowork; returns its bottom."""
    _, space, view = next(c for c in L.BLOCK_COLUMNS if c[0] == col)
    spec = L.VIEW_FAMILY.get("cowork", {}).get(col) or L.VIEW_DEFAULT[col]
    lines, runs = spec[0], spec[1]
    pick = spec[2] if len(spec) > 2 else None
    lines = [ln.replace("{kind}", L.KIND["cowork"]) if isinstance(ln, str) else ln for ln in lines]
    groups = L.JOB_GROUPS["cowork"]
    open_group = view or (groups[1] if col == "Jobs" else None)
    body = {"Studio": "studio", "Reports": "qwr", "Runs": "table"}.get(col, "lines")
    row = L.BLOCK_ROWS.get(("cowork", col))
    if row:
        open_group, view = row[1], row[1]
    sp_ = ("cowork", "Block", None, space, open_group, body, "", L.FAMILY_CAPTIONS.get(("cowork", col), ""))
    return L.wireframe(x, y, sp_, lines=lines, runs=runs, pick=pick, groups=row[0] if row else None,
                       header=f"s11 · cowork Block · Block › {space}" + (f" › {view}" if view else ""))


def planned_job(space, x, y) -> float:
    """One Job Space as s12's proposed() draws it for the cowork Job; returns its bottom."""
    spec = LV.JOB_FAMILY_VIEWS["cowork"].get(space) or LV.JOB_DEFAULT.get(space) or ([space, "(to fill)"], ["—"])
    lines, runs = spec[0], spec[1]
    pick = spec[2] if len(spec) > 2 else None
    tup = bool(lines) and isinstance(lines[0], tuple)
    body = "studio" if space == "Idea Studio" and tup else "table" if tup else "lines"
    row = LV.COWORK_ROWS.get(space)
    opened = LV.FAMILY_OPEN.get(("cowork", space)) or (row[0] if row else None)
    sp_ = ("cowork", "Job", "cowork Job", space, opened, body, "", LV.COWORK_NOTES.get(space, ""))
    return L.wireframe(x, y, sp_, lines=lines, runs=runs, pick=pick, groups=row,
                       header=f"s12 · cowork Job · Job › {space}" + (f" › {opened}" if row else ""))


# ── the drawing ─────────────────────────────────────────────────────────────────────────────────────
CARD_W = E.CARD_W


def note(x, y, what, size=18):
    """A short green line: what changed here (or what is kept), ✎ <date> first."""
    L.els.append(canvas.change_note(x, y, what, DATE, L.FRAME[0], size))


def frame_element(ekey, title, what, cards, x0, y0, facts, per_row=3) -> dict:
    fr = L.open_frame(title)
    text(x0, y0, title, 34)
    shown = [(i, src) for i, (src, _) in enumerate(cards) if (SHOTS / f"{ekey}__{i:02d}.png").exists()]
    olds = sum(bool(old_reason(src)) for _, src in shown)
    text(x0, y0 + 50, f"{what} · {len(shown)} versions as the cowork theme draws them today, {olds} on old pages "
                      "(flagged OLD: the cowork theme draws on the frame now, cowork_theme.py, so /_board/cowork-board retires; a look "
                      "from one may still be picked); then as s11 · s12 plan it", 18)
    x, y, row_h = x0, y0 + 130, 0
    for n, (i, src) in enumerate(shown):
        if n and n % per_row == 0:
            x, y, row_h = x0, y + row_h + 80, 0
        f = facts.get(f"{ekey}__{i:02d}", {})
        why = old_reason(src)
        if why:                                   # an old page: flagged, a red dashed box around it
            text(x, y - 26, "OLD · " + why, 14, RED)
        elif src[0] == "reader":
            text(x, y - 26, "? leaves the frame" + (f" · HTTP {f.get('status')}: not a Page"
                                                    if f.get("status") not in (None, 200) else ""), 14, RED)
        text(x, y, f"{chr(65 + n)} · {label_of(src)}", 20)
        h = E.picture(SHOTS / f"{ekey}__{i:02d}.png", x, y + 40, CARD_W)
        if why:
            base("rectangle", x - 8, y + 32, E.LAST_W[0] + 16, h + 16, RED, 1.5, dashed=True, rough=0)
        text(x, y + 52 + h, E.style_line(f) + ("\n(cut at its first screen)" if f.get("cut") else ""), 14, INK, MONO)
        row_h = max(row_h, 52 + h + 60)
        x += CARD_W + 80
    if not shown:
        text(x0, y0 + 130, "? no shots yet: run with --shoot", 18, RED)
    y += row_h + 40
    gone = [label_of(src) for i, (src, _) in enumerate(cards) if not (SHOTS / f"{ekey}__{i:02d}.png").exists()]
    if gone and shown:
        text(x0, y, "? not on the page today: " + " · ".join(gone), 16, RED)
        y += 40
    planned = PLANNED.get(ekey, [])
    if planned:
        text(x0, y + 20, "as planned · b03's s11 (Block) · s12 (Job) cowork rows, the same screen as there "
                         "(not served yet); cowork has no s13 row: a Task is the shared Page Task", 22)
        px = x0
        for k, (level, key) in enumerate(planned):
            text(px, y + 70, f"P{k + 1} · {'s11' if level == 'Block' else 's12'} · cowork {level} · {key}", 20)
            (planned_block if level == "Block" else planned_job)(key, px, y + 110)
            px += L.UI_W + 120
    L.close_frame(fr)
    return fr


def frame_proposed(ekey, title, x0, y0, facts) -> dict:
    fr = L.open_frame(title + " · proposed")
    text(x0, y0, title + " · proposed", 34)
    src, _, why, changed, open_ = PROPOSALS[ekey]
    text(x0, y0 + 50, "one look for every theme, drawn by the base (servers/workbench); the cowork theme gives the "
                      "words and, for its own elements, the rows", 18)
    y = y0 + 110
    note(x0, y, changed, 20)                      # green: what changed (or is kept) here
    y += 40
    if open_:
        text(x0, y, open_ if open_.startswith("?") else "? " + open_, 18, RED)   # red: still open
        y += 40
    shot = SHOTS / f"proposed__{ekey}.png"
    if shot.exists():
        h = E.picture(shot, x0, y, 1000)
        text(x0, y + h + 12, E.style_line(facts.get(f"proposed__{ekey}", {})), 14, INK, MONO)
        y += h + 70
    elif src[0] == "none":
        text(x0, y, "(none)", 28)
        y += 60
    else:
        text(x0, y, "? no shot yet: run with --shoot", 18, RED)
        y += 40
    text(x0, y + 10, "why", 22)
    for i, line in enumerate(why):
        text(x0 + 20, y + 50 + i * 30, "· " + line, 17)
    L.close_frame(fr)
    return fr


def frame_title(x0, y0, facts) -> dict:
    fr = L.open_frame("s32 · Cowork element UI")
    text(x0, y0, "s32 · Cowork element UI: every element the cowork theme draws, today and as planned", 40)
    n = sum(1 for k in facts if not k.startswith(("proposed__", "_")))
    olds = sum(1 for k, f in facts.items() if not k.startswith("_") and "cowork-board" in str(f.get("url", "")))
    text(x0, y0 + 60, f"after b03's s32-element-ui; {n} cards today ({olds} on the old CoWork page), one frame per "
                      "element with the planned screen from b03's s11 · s12 cowork rows, its '· proposed' frame to "
                      "the right; OLD = an old page, red dashed", 20)
    for k, c in enumerate(CHANGES):
        note(x0, y0 + 120 + k * 30, c)
    L.close_frame(fr)
    return fr


def frame_theme_elements(x0, y0) -> dict:
    fr = L.open_frame("Theme elements")
    text(x0, y0, "Theme elements: what the cowork theme uses, by level", 34)
    text(x0, y0 + 50, "element · level · Space › view · the base's or its own (why) · drawn today; red = a gap", 18)
    cols = (0, 380, 620, 1420, 2200)
    for c, h in zip(cols, ("element", "level", "Space › view", "base or its own", "today")):
        text(x0 + c, y0 + 110, h, 18)
    L.path([(x0, y0 + 140), (x0 + 3000, y0 + 140)], arrow=False, color=INK)
    for k, row in enumerate(THEME_ELEMENTS):
        y = y0 + 155 + k * 38
        for c, s in zip(cols, row):
            text(x0 + c, y, s, 16, RED if "GAP" in s else INK)
    L.close_frame(fr)
    return fr


def frame_run_names() -> dict:
    """cowork_theme.RUN_NAMES, read off the theme's source (importing it needs the host's packages)."""
    import ast
    tree = ast.parse((SERVERS / "workbench-cowork" / "cowork_theme.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "RUN_NAMES" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def walked_unnamed(facts) -> list:
    """(button, where) for every button the walk met that carries no run- name."""
    seen = {}
    for w in facts.get("_walk", []):
        for b in w.get("panel", []):
            name = b["name"].strip()
            if name and not name.startswith("run-"):
                seen.setdefault(name, w["place"])
        for b in w.get("other", []):
            seen.setdefault(b, w["place"])
    return sorted(seen.items())


def frame_buttons(x0, y0, facts) -> dict:
    fr = L.open_frame("Buttons with no Run name")
    text(x0, y0, "Buttons with no Run name yet, and a proposed run-<type>-<target>", 34)
    text(x0, y0 + 50, "every soft Run button is named by its Run (haipipe-run); the frame's buttons all carry one "
                      "(cowork_theme.RUN_NAMES), so these are the old page's, the Guide's and the planned ones", 18)
    y = y0 + 110
    for c, h in zip((0, 520, 1400), ("button", "where", "proposed Run")):
        text(x0 + c, y, h, 18)
    y += 36
    for button, where, name in UNNAMED:
        text(x0, y, button, 17, RED)
        text(x0 + 520, y, where, 17)
        text(x0 + 1400, y, name, 17, INK, MONO)
        y += 32
    known = ("Edit", "+ Add drawing", "Save resource") + tuple(u[0].split(" (")[0] for u in UNNAMED)
    walked = [(b, w) for b, w in walked_unnamed(facts) if not b.startswith(known)]
    if walked:
        named = frame_run_names()
        y += 20
        text(x0, y, f"met on the walk with no run- name ({len(walked)}): the old page's run types; the frame already "
                    "names the same button, so that name is the proposal", 18)
        y += 34
        for b, w in walked:
            text(x0, y, b, 16, RED)
            text(x0 + 520, y, w, 16)
            text(x0 + 1400, y, named.get(b, "? none yet"), 16, INK if b in named else RED, MONO)
            y += 28
    y += 30
    note(x0, y, "decided (b03): the server's names win; b03's s12 cowork Runs rows now read them, s12 rebuilt", 20)
    y += 36
    for c, h in zip((0, 520, 980, 1400), ("button", "today (RUN_NAMES)", "s12's old plan", "kept")):
        text(x0 + c, y, h, 18)
    y += 34
    for button, today, plan, prop in RENAMES:
        for c, s, col in ((0, button, INK), (520, today, INK), (980, plan, INK), (1400, prop, GREEN)):
            text(x0 + c, y, s, 16, col, MONO if c else L.SANS)
        y += 30
    L.close_frame(fr)
    return fr


def frame_pick(x0, y0) -> dict:
    fr = L.open_frame("Pick")
    text(x0, y0, "Pick: one look per cowork element", 34)
    text(x0, y0 + 50, "b03's picks already hold (green); write the letter you keep for the rest (or draw a new one)", 18)
    for i, (key, title, what, _) in enumerate(ELEMENTS):
        text(x0, y0 + 120 + i * 44, title, 20)
        if key in PICKED:
            text(x0 + 900, y0 + 120 + i * 44, "kept: " + PICKED[key], 20, GREEN)
        else:
            text(x0 + 900, y0 + 120 + i * 44, "? keep: __ (proposed: " + PROPOSALS[key][3].split(":", 1)[-1].strip()[:70] + ")",
                 20, RED)
    L.close_frame(fr)
    return fr


def draw(out: Path) -> None:
    facts = json.loads((SHOTS / "facts.json").read_text()) if (SHOTS / "facts.json").exists() else {}
    L.els.clear()
    L.FRAME[0] = None
    E.FILES.clear()
    title = frame_title(0, -2200, facts)
    te = frame_theme_elements(title["x"] + title["width"] + 200, -2200)
    bt = frame_buttons(te["x"] + te["width"] + 200, -2200, facts)
    frame_pick(bt["x"] + bt["width"] + 200, -2200)
    y = max(title["y"] + title["height"], te["y"] + te["height"], bt["y"] + bt["height"]) + 300
    for ekey, title_, what, cards in ELEMENTS:
        per_row = 4 if ekey in ("space", "views", "table") else 3
        fr = frame_element(ekey, title_, what, cards, 0, y, facts, per_row)
        pr = frame_proposed(ekey, title_, fr["x"] + fr["width"] + 200, y, facts)
        y = max(fr["y"] + fr["height"], pr["y"] + pr["height"]) + 200
    canvas.write(out, list(L.els), Path(__file__).name, files=E.FILES)


if __name__ == "__main__":
    if "--shoot" in sys.argv:
        url = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://127.0.0.1:5851"
        shoot(url.rstrip("/"))
    draw(Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].endswith(".excalidraw")
         else HERE / "s32-cowork-element-ui.excalidraw")
