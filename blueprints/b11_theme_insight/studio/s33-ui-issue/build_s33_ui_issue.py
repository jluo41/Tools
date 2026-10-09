"""s33 · Insight UI issues: s33-ui-issue.excalidraw, drawn by this builder (haipipe-studio).

The review of the live Insight workbench (261008): the Board Insight-SMSR2v1, its Job, its Tasks and its
Prototype, every Space and view, shot with headless Chrome into shots/. One lines-only table, worst first
(where · what is wrong · what it should be · evidence · owner), then what works and is kept, then the open
questions in red. The rows are ISSUES below; the face (s33-ui-issue.md) carries the same list.

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s33_ui_issue.py
"""
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED = canvas.INK, canvas.RED      # the studio look: black; red for an open question; green notes
els = []
# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (JL 261007)
CHANGES = []

B, J, T, F = "Block tab (s11)", "Job tab (s12)", "Task tab (s13)", "shared frame (b03)"

# (where, what is wrong, what it should be, evidence, owner), worst first
ISSUES = [
    ("every tab › every Space › Disk box",
     "lists the vanilla files (board.md, reports/q*, studio/s*, runs/*/, delivery/), mostly 'not yet', never "
     "the files the view reads",
     "name what each view reads: release.yaml, question.md, partitions.md, thresholds.yaml, tNN/runs/rNN/run.yaml "
     "and result/report.md, reports/vs-*.md",
     "insight_views.py sets no disk=, so frame.py vanilla_disk shows; any shot", B + " · " + J + " · " + T),
    ("Job › Audience Report (and Block › Coverage) › Logic cell",
     "the id loses its DIKW letter: D01, I01, K01, W01 all read 'Question 1'; 'builds on Knowledge questions 1, 2'; "
     "no 'from the Idea Studio' line; status a bare dot or emoji",
     "'K01 · Psychological Triggers', a status word, 'from the Idea Studio: sNN ↗'",
     "insight_views.py _q_logic; shots/J__Audience-Report__Full-Current.png", J),
    ("Job › Audience Report (and Block › Coverage) › Report cell",
     "not b03's Report: no answer line, no drawing, no 'report qNN · status'; filler on all 49 rows: 'Ran on this "
     "cut', 'run r01_full · 444691 rows', 'the page: not written yet ↗ · CHECK —'; leads are raw column lines "
     "('Gap_rest_pp: 12 of 13 intervals exclude zero')",
     "title ↗, the answer in a sentence, the drawing, 'report qNN · status'; say 'not written' once, not per row",
     "insight_views.py _q_report, _job_current; shots/J__Audience-Report__Full-Current.png", J),
    ("Block › Description › Prototype; Job › Description › Prototype; every question list",
     "6 retired questions (D04, I15, I16, I18, K07, K13) shown as live, 'new' in this release, counted in 'D 0/5'; "
     "their replacements share titles, so the list shows duplicates (D04 = I19, I15 = I22, I16 = I23, I18 = I24)",
     "retired ones folded under 'retired', each '→ replaced by I19'; out of counts and report rows",
     "question.md retired: lines; insight_views.py _prototype, _job_prototype; shots/B__Description__Prototype.png", B),
    ("Job › Audience Report › Cross (and Block › Cross)",
     "all 49 questions listed, 44 say 'Not asked on this cut' twice, each with its full Task Work; no POOL or SPLIT",
     "only the 5 questions asked on Cross, each with its difference test and POOL or SPLIT",
     "shots/J__Audience-Report__Cross.png; insight_views.py _job_current", J),
    ("Task › Audience Report › Table · Reading",
     "not Question │ Work │ Report: a partition table of 'answer —, how sure —'; the run findings the Job shows are "
     "missing; Reading is 'Read by: (— ↗) · Answer: —'; W01 says 'Nothing here yet' despite 5 cite needs",
     "one row per need: need │ the Run that answers it │ what it found, by Partition × Period (s13 point 4)",
     "shots/Tt30__Audience-Report__Table.png, Tt30__Audience-Report__Reading.png, Tt48__Audience-Report__Table.png", T),
    ("Task › Description › Question · Records",
     "Question dumps question.md as raw Python dicts (needs: E1: {'kind': 'cite', ...}); no Plan, no Data view; "
     "Records is empty",
     "s13's Question · Plan · Data: the ask; the needs as a table (kind, what, pass rule, agreed); n, base rate, "
     "power per partition",
     "insight_views.py _question, _records; shots/Tt30__Description__Question.png", T),
    ("Prototype Block, its Job and Tasks (all Spaces)",
     "opens in the generic work theme: Block shows only 'board-kind' (serves: hidden); release shows only 'state: "
     "open'; each Task 'No face file … missing' though question.md and scripts/ exist; proposals/ unseen. The Job's "
     "four '… · data questions ↗' links all open this same empty page",
     "the release: its questions by DIKW level, cuts, thresholds, code, proposals; a Task: its question.md and script",
     "shots/P__home__.png, PJ__home__.png, PTt30__home__.png; insight_views.py _release_links", B),
    ("Job › Runs panel (every tab's Runs panel)",
     "each hard-run row reads 'r01_full · a run of · Run a partition' with no Task: 38 identical 'r01_full' rows",
     "'t30 K01 · r01_full' (the Task in the row)",
     "runs_panel.py _card_html (the theme sets no _of); shots/J__Runs__All.png", J),
    ("Runs panel '+N more'",
     "the fold shows '+N more' but hides nothing: all 181 run boxes stay on screen",
     "four rows, then '+N more'",
     "runs_panel.py CSS: .run-list .run-row display:grid beats [hidden]; shots/Tt30__Work-Details__Partitions.png", F),
    ("Job › Runs › launch · power · compare · propose · close; Task › Runs",
     "each Job view shows only the same run-order line; All folds the 181 Task runs closed; the Task's Runs panel "
     "says rNN_<partition> 0 while 6 runs exist",
     "each view lists its runs or says 'no launch run yet'; the Task's count matches its runs",
     "insight_views.py _job_runs, task_spaces Runs; shots/J__Runs__launch.png", J),
    ("Job › Work Details",
     "three nested boxes (content card › level fold › a boxed fold per Task), every Task closed",
     "flush rows (the .dikw / .q-table look): a Task a row, its runs opening in place",
     "insight_views.py _tree; shots/J__Work-Details__All.png", J),
    ("Block › Work Details › quick results",
     "'full ok · youngmale ok · youngfemale ok …' repeated as text on ~40 rows",
     "a Task × partition grid with one mark per cell, grouped by DIKW level",
     "insight_views.py _jobs; shots/B__Work-Details__All.png", B),
    ("Block › Audience Report › Tracks · Consistency",
     "with one Job, 49 rows of 'j01 ok · no comparison yet' and 49 rows of '— —'",
     "one line: 'one Job: nothing to track or compare yet'",
     "shots/B__Audience-Report__Full-Tracks.png, B__Audience-Report__Full-Consistency.png", B),
    ("Block › Audience Report › Findings",
     "the partition row (Full … Cross) stays, but Findings ignores it: every partition the same",
     "no partition row on Findings, or Findings by partition",
     "insight_views.py _findings; shots/B__Audience-Report__Full-Findings.png", B),
    ("Block › Description › Partitions; Job › Description › Dataset",
     "'Power floor: pp.' (null shown blank); an empty 'why' column on all 7 cuts; raw 'youngmale' beside buttons "
     "'Young male'; Dataset says power 'ok' per cut while no floor is set",
     "'power floor: not set'; drop an empty column; one label per cut; power 'not checked' until a floor exists",
     "thresholds.yaml power.smallest_effect_pp: null; shots/B__Description__Partitions.png", B),
    ("Block and Job › Description › Prototype",
     "'signed' reads a field question.md lacks (all '—') while agreed: ✅ 261002 is on disk; 'methods' empty on "
     "every row; release meta 'open · · Jobs'",
     "show agreed; drop or fill methods; no empty separators",
     "insight_views.py _prototype, _job_prototype; shots/B__Description__Prototype.png", B),
    ("Job and Task › run and answer links",
     "now open /_board/insight-run, the old run page s32 marks as retiring; inside, Ticket · Run card · Receipt and "
     "files open raw files in a new tab (landed 08:52 during the review)",
     "the run in the frame's pop-out (the page reader), no retired route",
     "insight_views.py run_url, render_run_page (uncommitted)", J),
    ("every tab › Disk box face link; Prototype › Description path",
     "a plain link to /_board/page: 59 links that leave the frame",
     "open it in the pop-out (data-pop)",
     "frame.py disk_markup (_link, not pop)", F),
    ("Job › Audience Report and Coverage rows",
     "'Question N', 'Task Work' and 'Report' drawn as pill chips on every row (138 on one view)",
     "no tags: plain words (b03 s32: no tags in any theme)",
     "insight_views.py _q_logic, _q_work, _q_report", J),
    ("Task (W) › Delivery",
     "says 'its answer goes up as a cite need', wrong for a Wisdom Task",
     "a W Task: its signed counsel goes to the Board's handoff (s13 point 7)",
     "insight_views.py task_spaces Delivery; shots/Tt48__Delivery__.png", T),
    ("Task › Description · Audience Report",
     "the carried board's answers (🟡 per cut in source.cells) are on disk in _old/ but shown only as raw text; "
     "no link to the old page",
     "'answered on the old board (🟡) ↗' until this Job's page is written",
     "question.md source.cells; tasks/_old/b52_sms_question_dikw", T),
    ("Block › Runs › from below; Job › Delivery; Board › Prototype intro",
     "Job names, 'Board › Delivery › Handoff' and the Prototype path are plain text, not links",
     "link each in the frame",
     "insight_views.py _board_runs, _job_delivery, _prototype", B),
]

KEEP = [
    "every Space and third-row view answers 200 at Block, Job and Task; Job ▾ / Task ▾ keep the open Space",
    "no link to the old /_board/insight-board pages; 3798 pop-out links, every target on disk",
    "Map: releases × data versions, the Job in its cell; Board and Job Dataset facts",
    "Block › Work Details' Job row: pins, the clock that moved, answered by DIKW level, state",
    "Job Current's Task Work steps (Compute · Reuse · Answer → the file), 'builds on', the lead lines' real numbers",
    "Job Dataset: n and refused cuts per partition (K17 in warn)",
    "partition buttons in words (Young male …); vs previous on a first Job: one line",
    "Runs panel buttons named by their Run, the words under, the owner skill",
    "the new flush level rows (.dikw) on Audience Report, as the old board drew them",
]

OPEN = [
    "? one owner for the Disk box: the theme per Space, or the frame reading a theme's file list",
    "? Cross and Findings: hide the partition row, or keep it greyed",
    "? retired questions: still Tasks in a Job, or only in the release",
    "? Guide tab not reviewed (mounted by script; headless shots do not open it)",
]

COLS = (("#", 50, 4), ("where", 330, 27), ("what is wrong", 640, 54), ("what it should be", 470, 39),
        ("evidence", 420, 35), ("owner", 230, 19))
SIZE, LINE = 16, 28


def el(kind, x, y, w, h, **extra):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
          "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
          "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None,
          "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
          "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size=20, frame=None, color=INK):
    lines = s.split("\n")
    return el("text", x, y, max(len(l) for l in lines) * size * 0.55, len(lines) * size * 1.25, text=s,
              originalText=s, fontSize=size, fontFamily=1, textAlign="left", verticalAlign="top",
              containerId=None, autoResize=True, lineHeight=1.25, frameId=frame, strokeColor=color)


def line(x1, y1, x2, y2, frame):
    return el("line", x1, y1, x2 - x1, y2 - y1, points=[[0, 0], [x2 - x1, y2 - y1]], frameId=frame,
              startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None, lastCommittedPoint=None)


def table(x0, y0, frame) -> float:
    """The issues as a lines-only table: a head row, then a row per issue, ruled by one line each."""
    width = sum(w for _, w, _ in COLS)
    x = x0
    for head, w, _ in COLS:
        text(x + 8, y0, head, 18, frame)
        x += w
    y = y0 + 32
    line(x0, y, x0 + width, y, frame)
    for n, row in enumerate(ISSUES, 1):
        cells = [str(n)] + list(row)
        wrapped = [textwrap.fill(c, cpl) for c, (_, _, cpl) in zip(cells, COLS)]
        h = max(w.count("\n") + 1 for w in wrapped) * LINE + 14
        x = x0
        for w_text, (_, w, _) in zip(wrapped, COLS):
            text(x + 8, y + 7, w_text, SIZE, frame)
            x += w
        y += h
        line(x0, y, x0 + width, y, frame)
    return y


def main():
    out = HERE / "s33-ui-issue.excalidraw"
    els.clear()
    width = sum(w for _, w, _ in COLS)
    f1 = el("frame", 0, 0, width + 80, 100, name="1 · Insight UI issues, worst first")
    text(40, 30, "s33 · Insight UI issues · the live workbench, 261008", 34, f1["id"])
    text(40, 80, "Board Insight-SMSR2v1 · its Job j01_p1_SMSR2v1 · Tasks K01, D01, W01 · the Prototype and its Job "
                 "and Tasks; every Space and view, shot into shots/", 18, f1["id"])
    for i, (date, what) in enumerate(CHANGES):          # the title frame's list of changes
        els.append(canvas.change_note(40, 112 + i * 26, what, date, f1["id"]))
    bottom = table(40, 150 + len(CHANGES) * 26, f1["id"])
    f1["height"] = bottom + 40

    f2 = el("frame", width + 200, 0, 1100, 100, name="2 · What works, kept")
    text(width + 240, 30, "What works, kept", 30, f2["id"])
    y = 90
    for k in KEEP:
        s = textwrap.fill("· " + k, 90)
        text(width + 240, y, s, 18, f2["id"])
        y += (s.count("\n") + 1) * 24 + 10
    y += 30
    text(width + 240, y, "Open", 30, f2["id"])
    y += 50
    for o in OPEN:
        s = textwrap.fill(o, 90)
        text(width + 240, y, s, 18, f2["id"], RED)
        y += (s.count("\n") + 1) * 24 + 10
    f2["height"] = y + 30

    for e in canvas.off_palette(els):                    # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, els, "build_s33_ui_issue.py")


if __name__ == "__main__":
    main()
