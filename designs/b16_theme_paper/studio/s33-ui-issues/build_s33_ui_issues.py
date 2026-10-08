"""b16 s33 · the paper workbench's UI issues: s33-ui-issues.excalidraw (review of the served frame, 261008).

A read-only review of the paper theme as the shared frame serves it, at every level and every view: the Board
tab (s11), a version tab (s12) and a Section tab (s13), with the links each view prints. Each issue is one row:
where, what is wrong, what it should be, where in the code, and who owns it. Issues are written in placeholders
(Tools stays generic): <board>, jNN_<sent>, jNN_<next>, tNN_<section>, qNN_<question>.

Frames, top to bottom: the title; one frame per owner (shared frame · Board · version · Section), each a map of
its Spaces and views with the issue ids beside them, then the issue table; what works (keep); open.
Black lines and boxes; red = open (an issue not fixed yet, or a question). Drawn with b04's studio helpers
through haipipe-studio's canvas.write, so a person's marks survive a rebuild.

    python build_s33_ui_issues.py [out.excalidraw]
"""
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1].parent / "b04_skill_folder" / "studio" / "_build"))
from sketch import GRAY, INK, MONO, RED, SANS, base, close_frame, open_frame, save, text  # noqa: E402

DATE = "261008"
CODE = "servers/"                       # code paths below are under Tools/plugins/haipipe-toolkit/servers/

# ── the issues, worst first inside each owner ───────────────────────────────────────────────────────────────
# (id, where, what is wrong, what it should be, code)
FRAME_ISSUES = [
    ("F1", "every tab · band, Scope, Ideation, Narrative, Evidence, Plan, Records, Requirement, Disk boxes",
     "An open link to a file that is not a Page Face (a Board or version face, a studio topic face, a draft plan, "
     "a record, an evidence-items file, the rubric) goes to /_board/page, which answers 404 \"Not a Page\".",
     "A plain reader for any file; the Page view only for a Page Face.", "workbench/frame.py:288 _reader"),
    ("F2", "Section › Runs",
     "Embeds the Page's own runs screen with a fourth tab row (Workflow map · Page Writing · …); \"No <kind> Run "
     "yet.\" four times; the side panel says \"No runs yet.\" while the body counts Writing Runs.",
     "One runs list in the Space's own look; one empty note.", "page_task_spaces"),
    ("F3", "Section › Table, Reading, Draft-…, Evidence-…",
     "Each view is an iframe card inside the Space card, with its own inner tab row (All items · Card · Source): "
     "a box in a box. The fixed frame height leaves a large blank area under a short view.",
     "Embed without the outer card; size the frame to its content.", "workbench/frame.py page_view_url"),
    ("F4", "Section › Delivery, a lane",
     "\"built; no preview for this kind yet\" when the lane's only file is a selection list, beside \"not built\".",
     "One honest lane state: not built.", "workbench/frame.py:1227"),
    ("F5", "every page",
     "The page never finishes loading, so a headless screenshot hangs unless it is given a timeout.",
     "The load event fires; long requests start after it.", "?"),
]

BOARD_ISSUES = [
    ("B1", "Audience Report › High-level logic + Low-level work",
     "The Report column says \"No report yet.\" though reports/qNN_<question>/ exist with a state and an answer.",
     "b03's report cell: title ↗, the answer line, the drawing, \"report qNN · state\".",
     "workbench-paper/paper.py:1937 _report_cell"),
    ("B2", "Audience Report › Narrative",
     "Three stock rows (editor · reviewer · public), each \"not judged yet\" and \"No report yet: run Review for an "
     "audience\". The telling's identity, pitch and stakes are not written out; their links 404.",
     "Write out Identity (title, one sentence, unit, scope), Pitch (tension, what the study does, answer) and "
     "Stakes from the telling's face; \"not reviewed yet\" once.", "paper_theme.py:603-616"),
    ("B3", "Work Details › Evidence",
     "Every evidence item twice (one per version), with no version column; \"contract only\" on every row; each "
     "Open ↗ is an old /_board/draft link that leaves the frame.",
     "One version, or a version column; no repeated state word; open inside the frame.", "paper_theme.py _sections"),
    ("B4", "High-level logic › \"Not under a question\"",
     "Rows the telling gives an RQ (a check on a hypothesis, a discovery that serves both RQs) are left here.",
     "Place each row by its RQ column.", "workbench-paper/paper.py:2066 _rest_block"),
    ("B5", "High-level logic › the work column",
     "\"no folder yet\" twice on most rows; \"no receipt\" under every run; the same work rows repeated under each "
     "question; long run names run into the Report column.",
     "At most one \"no folder yet\"; a receipt state once per run list; names wrap.", "paper.py:1853, 1911"),
    ("B6", "High-level logic › a discovery row",
     "A discovery whose folder sits outside the grammar says \"no folder yet\"; a finished one reads \"pending · N "
     "runs · done N\".", "Name the folder the telling gives; one state word.", "paper.py _bjtr"),
    ("B7", "Description › Scope",
     "Only spine and close, in the face's older story words. The face's Topic and the telling it follows are "
     "missing, though the Disk box says \"spine · close · Topic\".",
     "Show the Topic and the current telling (story-current).", "paper_theme.py _description"),
    ("B8", "Description › Venue",
     "\"Target now: — (from the Story)\" though the Board's Topic and every version face name the venue.",
     "Read the venue from the faces.", "paper_theme.py:219"),
    ("B9", "Delivery › Rounds",
     "\"No round yet.\" while a version holds a comments report (page-type: comments).",
     "List each comments report as a round.", "paper_theme.py:774"),
    ("B10", "Work Details › Main · Appendix  vs  Delivery",
     "Main and Appendix silently show the newest version's Sections; Delivery silently shows the last built "
     "version's paper; the Disk box names that version's file as the Board's.",
     "Name the version on screen, or show each version's build (s11).", "paper.py:1339 delivery_dir"),
    ("B11", "Description › Resources",
     "\"Nothing here yet.\"; the Disk box names a \"## Related resources\" heading the face does not have; the "
     "face's blocks, discoveries and ## Links are not shown.",
     "Show the face's resources; Disk lists only what exists.", "paper_theme.py:224, 1419"),
    ("B12", "Work Details › Jobs · the Version ▾ list",
     "A presentation Job (slides, not a send) is kind \"send\" and offered as a version; rows carry no send date, "
     "venue or state.", "Kind presentation, kept out of the version list; a state column.", "paper_theme.py:1246"),
    ("B13", "Idea Studio",
     "A loose drawing at studio/ root with a topic's name makes a second row of that name; the topic's own row "
     "has no drawing.", "One row per topic; the drawing moves into its topic (a Board file).", "_studio"),
    ("B14", "Audience Report › Ideation",
     "Only the idea rows: the direction (space · why now · worth it), the risk, the objection, the "
     "recommendation and the next step of the ideation face are missing.",
     "The direction and the next step above the rows.", "paper_theme.py _ideation_rows"),
    ("B15", "Audience Report › Related Questions",
     "The empty note is a run-on line with raw syntax (\"board.md ## Questions, group: …\"); the Disk box lists "
     "reports this view does not show.", "One plain empty line; Disk lists what this view reads.",
     "paper_theme.py:575"),
    ("B16", "Narrative · Evidence",
     "The theme's rewrite of old Page links is not applied here: /_board/draft links stay; some 404, the rest "
     "leave the frame.", "Every view goes through the rewrite.", "paper_theme.py:110-131 _frame_links"),
    ("B17", "Work Details › Main · Appendix (also the version's)",
     "Rows read \"v0.1 · Open · Open ↗\" (a state and a link, same word); titles made from slugs; none of the old "
     "Section list's content (reader question, story row, words, evidence).",
     "The old spine-card row; the face's title.", "paper_theme.py _sections"),
    ("B18", "Work Details › Jobs", "The links to a version tab drop theme=paper.", "Keep the theme on every link.",
     "paper_theme.py _jobs"),
]

JOB_ISSUES = [
    ("J1", "Audience Report › Comments",
     "Proposed-route cells print raw Markdown links, and they point at the previous version's Sections; \"open\" "
     "and the report link repeat on every card; each card is a box around a bordered table.",
     "Rendered links to this version's Sections; one state mark; no inner box.", "paper_theme.py:898-928 _comments"),
    ("J2", "Audience Report › Draft-Main",
     "Each Section is a card around a bordered table (nested boxes); a card does not open its Section. The face's "
     "whole-paper Narrative (reader and promise, claim system, arc, reader journey, risks) shows nowhere.",
     "That prose above the Sections; folded cards as Draft-Appendix; each opens its Section.", "_draft_rows"),
    ("J3", "the sent version (jNN_<sent>)",
     "No comments row or item though the decision answers this send; its state names a report that lives in the "
     "next version; its Delivery shows a later draft build, while what was sent shows under the next version's "
     "Delivery › Sent.", "The sent version shows what was sent and its decision; the next one, what it answers.",
     "the faces + _version_delivery"),
    ("J4", "Audience Report › Questions",
     "Four or five stock rows, each \"not asked yet\" and the same \"no report yet · Ask a Question writes it into "
     "## Questions with its report\"; Work cells are template paths (studio/sNN-story-…, venues/<venue>/call.md).",
     "One hint line; real files in the Work cells.", "paper_theme.py:964"),
    ("J5", "Description › Venue rules", "\"Venue: — (from the Story)\" though the face names the venue.",
     "Read it from the face.", "paper_theme.py:952"),
    ("J6", "Delivery · Cover letter",
     "\"not built\" twice per card; \"not written yet\" on every paragraph; three different empty notes; raw "
     "\"### Cover letter\" in the text; Sent lists every file.",
     "One line per item; Sent folds to the PDF and a count.", "paper_theme.py:780-830, 1109-1129"),
    ("J7", "Draft-Main · Draft-Appendix · Version ▾",
     "Draft-Main opens expanded, Draft-Appendix folded; the version list shows folder names only (no sent / next).",
     "Both folded alike; the list says sent <date> · next.", "_draft_rows · the band"),
]

TASK_ISSUES = [
    ("T1", "Audience Report › Comments",
     "\"No Review Items yet\" though the version's comments report routes items to this Section and its plan "
     "counts them as routed; the view reads a \"## Review Items\" table the report does not have.",
     "The items routed to this Section.", "paper_theme.py:1352-1357 _reviews"),
    ("T2", "Description › Plan",
     "The draft plan is dumped as raw Markdown in a monospace box; its path link 404s; the Disk box names only "
     "the face.", "The plan rendered in the old Outline look; Disk names draft/<stem>-draft-vN.md.", "Plan view"),
    ("T3", "Delivery › Ready",
     "\"outline approved\" while the plan's approved box is empty; a copied Section without its .tex fragment "
     "shows LaTeX \"not built\" and \"built\" at once; \"not built yet: run Build\" three times.",
     "A true Ready line; one state per lane; one empty note.", "paper_theme.py _ready · frame.py:1227"),
    ("T4", "Description › Scope",
     "Two tables stacked; the second repeats the title with a long full-path link; a stale story-row is not "
     "marked though the view's note says it should be.", "One table; mark the stale story-row.",
     "paper_theme.py _contract"),
    ("T5", "Disk boxes",
     "Work Details says \"its own folders ./ N\" instead of the file the view reads; Comments lists the Questions "
     "files; a studio topic link 404s.", "Name the file each view reads.", "page_task_spaces disk"),
]

# a map per tab: (Space, [(view, [issue ids])]); an empty id list = no issue found
MAPS = {
    "Board tab": [
        ("Description", [("Scope", ["B7"]), ("Venue", ["B8"]), ("Resources", ["B11"]), ("Related", [])]),
        ("Idea Studio", [("", ["B13"])]),
        ("Audience Report", [("Ideation", ["B14"]), ("Narrative", ["B2", "B16"]),
                             ("High-level logic + Low-level work", ["B1", "B4", "B5", "B6"]),
                             ("Related Questions", ["B15"])]),
        ("Work Details", [("Jobs", ["B12", "B18"]), ("Main", ["B10", "B17"]), ("Appendix", ["B10", "B17"]),
                          ("Evidence", ["B3", "B16"])]),
        ("Runs", [("", [])]),
        ("Delivery", [("LaTeX", ["B10"]), ("Word", []), ("Cover letter", []), ("Rounds", ["B9"])]),
    ],
    "version tab": [
        ("Description", [("Version", ["J3"]), ("Venue rules", ["J5"])]),
        ("Idea Studio", [("", [])]),
        ("Audience Report", [("Questions", ["J4"]), ("Draft-Main", ["J2", "J7"]), ("Draft-Appendix", ["J7"]),
                             ("Comments", ["J1", "J3"]), ("Cover letter", ["J6"])]),
        ("Work Details", [("All", ["B17"]), ("Main", ["B17"]), ("Appendix", ["B17"]), ("Letters", [])]),
        ("Runs", [("", [])]),
        ("Delivery", [("", ["J3", "J6"])]),
    ],
    "Section tab": [
        ("Description", [("Scope", ["T4"]), ("Plan", ["T2"]), ("Requirement", ["F1"]), ("Records", ["F1"])]),
        ("Idea Studio", [("", [])]),
        ("Audience Report", [("Table", ["F3"]), ("Reading", ["F3"]), ("Questions", []), ("Comments", ["T1", "T5"])]),
        ("Work Details", [("Draft-Scratch", ["F3"]), ("Draft-Revise", ["F3"]), ("Evidence-…", ["F3", "T5"])]),
        ("Runs", [("", ["F2"])]),
        ("Delivery", [("", ["T3", "F4"])]),
    ],
}

KEEP = [
    "Description › Related: paper cards by group (closest · one RQ · background · cautions); every PDF and summary opens",
    "the question row (Logic │ Work │ Report) on Ideation and on the version's comments question: title ↗, "
    "answer, drawing, \"report qNN · state\"",
    "High-level logic: each question block keeps its inputs, hypotheses → claims → contributions, and typed work "
    "rows with their B → J → T → R tree",
    "version › Draft-Appendix: folded cards (letter, reader question, state); the model for Draft-Main and the "
    "Work Details lists",
    "Section › Table: Bullet │ Draft with roles and evidence chips; Scope's reader-contract table; the Section's "
    "studio row with its run-draw Run",
    "the frame: a Disk box and run cards on every view; a Section opens its own tab; a report opens in the pop-out",
]

OPEN = [
    "? the Board's Main · Appendix · Delivery: the newest version only, or each version side by side?",
    "? Section › Comments: read the report's concern table as it is, or give a comments report a ## Review Items table?",
    "? the sent version: do its sent files and its decision live in it, or in the next version's comments report?",
    "? the Board's Evidence list: drop it (each version has its own), or keep it with a version column?",
    "? F5: what keeps the page loading (a long-lived request?), and does it matter beyond headless shots?",
]

LINE = 24
COLS = (("id", 60), ("where", 300), ("what is wrong", 640), ("what it should be", 470), ("code", 300))


def wrap(s, w, size=15):
    return textwrap.wrap(s, max(8, int(w / (size * 0.52))), break_on_hyphens=False) or [""]


def issue_table(x, y, rows):
    """A lines-only table, cells wrapped; the id in red (open). Returns the bottom."""
    width = sum(w for _, w in COLS)
    cx = x
    for head, w in COLS:
        text(cx + 8, y, head, 15, GRAY)
        cx += w
    y += 28
    base("line", x, y, width, 0, INK, sw=1, rough=0).update(points=[[0, 0], [width, 0]])
    for row in rows:
        cells = [wrap(c, w - 16) for c, (_, w) in zip(row, COLS)]
        h = max(len(c) for c in cells) * LINE + 16
        cx = x
        for k, (lines, (_, w)) in enumerate(zip(cells, COLS)):
            color = RED if k == 0 or lines == ["?"] else INK
            text(cx + 8, y + 8, "\n".join(lines), 15, color, MONO if k in (0, 4) else SANS)
            cx += w
        y += h
        base("line", x, y, width, 0, GRAY, sw=1, rough=0).update(points=[[0, 0], [width, 0]])
    return y


def tab_map(x, y, name, spaces):
    """The tab's Spaces and views as a tree in a box, each view's issue ids beside it in red. Returns (right, bottom)."""
    rows = []
    for i, (space, views) in enumerate(spaces):
        last = i == len(spaces) - 1
        for j, (view, ids) in enumerate(views):
            branch = ("└── " if last else "├── ") + space if j == 0 else ("    " if last else "│   ") + " " * len(space)
            label = f"{branch}  {view}" if view else branch
            rows.append((label, ids))
    w = max(len(r) for r, _ in rows) * 15 * 0.6 + 260
    text(x, y, name, 18, GRAY)
    top = y + 32
    base("rectangle", x, top, w, 20 + len(rows) * 26, INK, sw=1, rough=0)
    for i, (label, ids) in enumerate(rows):
        ty = top + 12 + i * 26
        text(x + 18, ty, label, 15, INK, MONO)
        ix = x + 18 + (max(len(r) for r, _ in rows) + 3) * 15 * 0.6
        text(ix, ty, " ".join(ids) if ids else "·", 15, RED if ids else GRAY, MONO)
    return x + w, top + 20 + len(rows) * 26


def owner_frame(y0, n, title, owner, subtitle, maps, rows):
    fr = open_frame(f"{n} · {title}")
    text(0, y0, f"{n} · {title}", 30)
    text(0, y0 + 44, f"owner: {owner}  ·  {subtitle}", 18, GRAY)
    y = y0 + 100
    x, bottom = 0, y
    for name, spaces in maps:
        r, b = tab_map(x, y, name, spaces)
        x, bottom = r + 80, max(bottom, b)
    issue_table(0, bottom + 60 if maps else y, rows)
    return close_frame(fr)


def frame_keep(y0):
    fr = open_frame("5 · what works: keep it")
    text(0, y0, "5 · what works: keep it", 30)
    text(0, y0 + 44, "Carried into every fix above; nothing here is asked to change.", 18, GRAY)
    for i, k in enumerate(KEEP):
        text(0, y0 + 100 + i * 32, f"{i + 1}. {k}", 17, INK)
    return close_frame(fr)


def frame_open(y0):
    fr = open_frame("open")
    text(0, y0, "open", 30, RED)
    for i, o in enumerate(OPEN):
        text(0, y0 + 56 + i * 32, o, 18, RED)
    return close_frame(fr)


def main():
    n = len(FRAME_ISSUES) + len(BOARD_ISSUES) + len(JOB_ISSUES) + len(TASK_ISSUES)
    text(0, -150, "b16 s33 · the paper workbench's UI issues, as served", 40)
    text(0, -92, f"Reviewed {DATE}: every level, every Space and view, every link on them. {n} issues, worst first "
                 "inside each owner. Red = open. Placeholders only: <board> · jNN_<sent> · jNN_<next> · tNN_<section>.",
         18, GRAY)
    text(0, -60, f"Judged against: no nested boxes, no filler repeated per row, the old page's cards, b03's question "
                 f"row, content written out, links inside the frame, a Disk box naming real files. Code under "
                 f"Tools/plugins/haipipe-toolkit/{CODE}.", 18, GRAY)
    y = owner_frame(60, 1, "shared frame", "b03", "every tab: links, embeds, lanes", [], FRAME_ISSUES) + 220
    y = owner_frame(y, 2, "Board tab", "design_b16_theme_paper-s11-block",
                    "Paper Board: Description · Idea Studio · Audience Report · Work Details · Runs · Delivery",
                    [("Board tab", MAPS["Board tab"])], BOARD_ISSUES) + 220
    y = owner_frame(y, 3, "version tab", "design_b16_theme_paper-s12-job",
                    "a send jNN_v<MMDD>_<desk>: the sent one and the next one",
                    [("version tab", MAPS["version tab"])], JOB_ISSUES) + 220
    y = owner_frame(y, 4, "Section tab", "design_b16_theme_paper-s13-task", "a Section tNN_<section> in a version",
                    [("Section tab", MAPS["Section tab"])], TASK_ISSUES) + 220
    y = frame_keep(y) + 220
    frame_open(y)
    save(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s33-ui-issues.excalidraw", "build_s33_ui_issues.py")


if __name__ == "__main__":
    main()
