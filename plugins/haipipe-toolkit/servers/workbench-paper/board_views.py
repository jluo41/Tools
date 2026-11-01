"""A paper Board's Report and Work views (b16 s32, s33): each view in two bands, RESULTS and PROCESS, numbered from 1
in each; the Report is its sections only (s32-D27), Work PROCESS then RESULTS, the same code, so they agree.
focus_page.py asks board_report_views and board_work_views; its captions go in board_read.PAPER_CAPTIONS."""
from __future__ import annotations

import re
from pathlib import Path

from live.ui_parts import BOARD_CSS, PB_CSS, PB_JS, PROCESS, RESULTS, _band
from live.focus_draft import CSS, JS
from live.board_read import PAPER_CAPTIONS, BOARD_PARTS, board_topic, explore_tree, is_version
from live.board_interactions import ix_item
from live.paper_version import VERSION_CSS
from live.board_results import displays_view, ANSWER_FIRST, SHAPED, _topic_view, evidence_view, explore_view, writing_view
from live.board_process import process_html


BOARD_CAPTIONS = {"idea": "The idea: the direction chosen, and the others considered.",
                  "story": "What the paper says, and where it is sent.",
                  "venue": "Where it is sent: the venue's desk rules, the ladder of journals, and the venue's own papers.",
                  "dataflow": "How the data becomes each answer: the Runs, the evidence, the claims.",
                  "paperflow": "The Sections in reader order, their displays, and the steps to the send."}


# side tabs on a paper Board: the list and the open panel the same height, each with its own scroll bar (JL 261101:
# "how could you make it to be of the same length and there is a scroll bar?"); short content stays short, the taller of
# the two sets the height, capped at 72% of the window. This theme's own rule; ui_parts' side tabs stay as they are.
SIDE_CSS = ("<style>.pb-side{align-items:stretch}"
            ".pb-side>.pb-list{position:static;max-height:72vh;overflow-y:auto;padding:1px 4px 1px 1px;flex-wrap:nowrap}"
            ".pb-side>.pb-read{max-height:72vh;display:flex;flex-direction:column;min-height:0}"
            ".pb-side>.pb-read>.pb-panel:not([hidden]){flex:1 1 auto;min-height:0;overflow-y:auto;box-sizing:border-box}"
            "@media(max-width:600px){.pb-side>.pb-list{max-height:none;overflow:visible;flex-wrap:wrap}"
            ".pb-side>.pb-read{max-height:80vh}}</style>")


def banded(board: Path, key: str, results: str, root: Path, md, items, work: bool, item_html=None) -> str:
    """One view: Report its own numbered sections only; Work in two bands, PROCESS then RESULTS (RESULTS is the Report's
    sections, drawn by the same code); the helpers (the drawing, the mind map) stay at the bottom, after the dashed rule."""
    res, rule, helpers = results.partition("<hr class=pb-rule>")
    # the Report is the view's own sections only, 1, 2, 3 (JL 261101: "for the Results and Process, they will just be
    # in the Work, why report have that? report will only have the things like the 1, 2, 3, 4"; b16 s32-D27)
    body = (_band(PROCESS, process_html(board, key, root, md, items, work, item_html)) + _band(RESULTS, res)) if work else res
    # VERSION_CSS: Writing's step words; PB_JS: the tab clicks and flow wires; JS: the folds and Copy prompt
    return (CSS + BOARD_CSS + VERSION_CSS + PB_CSS + SIDE_CSS + body
            + (rule + helpers if helpers.strip() else "") + PB_JS + JS)


def _results(board: Path, key: str, root: Path, md, items) -> str:
    """The RESULTS band's html of one view: the Report view's own sections."""
    if key in SHAPED:
        topic = board_topic(board, key, dict((k, pat) for k, _, pat in BOARD_PARTS)[key])
        return SHAPED[key](board, topic, root, md, items) if topic is not None else ""
    return {"explore": explore_view, "evidence": evidence_view, "displays": displays_view, "draft": writing_view}[key](board, root, md, items)


def board_report_views(board: Path, root: Path, md, items=()) -> dict:
    """{key: (name, builder)} for the paper parts this Board has, in the paper's own order; `md(text, base)` renders
    Markdown with links relative to `base` (the focus page's renderer)."""
    views = {}
    for key, name, pattern in BOARD_PARTS:
        if key == "venue":                       # merged into Story's 4 · Venues (b16 s32 B, JL 261031)
            continue
        topic = board_topic(board, key, pattern)
        if topic is not None and key in SHAPED:
            views[key] = (name, lambda k=key: banded(board, k, _results(board, k, root, md, items), root, md, items, False))
        elif topic is not None:
            views[key] = (name, lambda t=topic, k=key: CSS + BOARD_CSS + _topic_view(t, root, md, items, k in ANSWER_FIRST) + JS)
    tree = explore_tree(board)                     # the work and discovery Blocks this paper draws on (JL 261031), by
    if any(tree.get(k) for k in ("work", "discovery")):   # path, address or another Project, as the view draws them
        views["explore"] = ("Support blocks", lambda: banded(board, "explore", _results(board, "explore", root, md, items), root, md, items, False))   # JL 261031: "support-blocks"
    if any(not is_version(d) for d in board.glob("j[0-9]*_*") if d.is_dir()):
        views["evidence"] = ("Evidence", lambda: banded(board, "evidence", _results(board, "evidence", root, md, items), root, md, items, False))
    if any(re.search(r"evidence_display|_displays", d.name) for d in board.glob("j[0-9]*_*") if d.is_dir()) \
            or any(board.glob("s??-paper-displays")):     # its own view, after Evidence, before Writing (JL 261101)
        views["displays"] = ("Displays", lambda: banded(board, "displays", _results(board, "displays", root, md, items), root, md, items, False))
    if any(d.is_dir() for d in board.glob("j[0-9]*_*")):
        views["draft"] = ("Writing", lambda: banded(board, "draft", _results(board, "draft", root, md, items), root, md, items, False))  # j11_writing_… (JL 261031)
    return views


PAPER_CAPTIONS.update(BOARD_CAPTIONS)


BOARD_CAPTIONS.update({"draft": "Each writing Job, one per version: its Sections in reader order, to read, and its assembled paper."})


BOARD_WORK_CAPTIONS = {
    "idea": "The idea: what waits on you, what is open, its skills; then the direction chosen.",
    "story": "The story: what waits on you, what is open, its skills; then the pitch, questions and venues.",
    "venue": "The venue: what waits on you, what is open, its skills.",
    "dataflow": "The data flow: what waits on you, its plan (each step a skill and a prompt), the Runs to do; then the map and the questions.",
    "paperflow": "The paper flow: what waits on you, what is open, its skills; then the send, Sections and timeline.",
    "explore": "The support blocks: what waits on you, their skills; then the folder trees.",
    "evidence": "The evidence: what waits on you, where each item stands, its skills; then the values and citations.",
    "displays": "The displays: what waits on you, where each display stands, its skills; then the plan and each display.",
    "draft": "The writing: what waits on you, each Section's steps, its skills; then the text and the assembled paper."}


def board_work_views(board: Path, root: Path, md, versions: str = "", items=(), item_html=None) -> dict:
    """{key: (name, builder)}: the Report's list, each view in its two bands, PROCESS first (what waits on you, what is
    open or where each item stands, the skills that do it), then RESULTS, the Report view itself, so the two agree
    (JL 261101: "the results should be consistent to the report")."""
    item_html = (lambda r: ix_item(r, root)) if item_html else None     # each item a folded row (JL 261031)
    views = {}
    for key, (name, _) in board_report_views(board, root, md, items).items():
        if key in SHAPED or key in ("explore", "evidence", "displays", "draft"):
            views["work-" + key] = (name, lambda k=key: banded(board, k, _results(board, k, root, md, items), root, md, items,
                                                                True, item_html))
    views.setdefault("work-draft", ("Writing", lambda: banded(board, "draft", _results(board, "draft", root, md, items), root, md,
                                                              items, True, item_html)))   # Writing holds the versions, even before one
    return views


PAPER_CAPTIONS.update({"work-" + k: v for k, v in BOARD_WORK_CAPTIONS.items()})


PAPER_CAPTIONS["draft"] = BOARD_CAPTIONS["draft"]


# ── Interactions on a paper Board: Report says what was decided, Work what waits on you ──────────────────────────────
BOARD_CAPTIONS.update({"interactions": "What we decided: each answered form, then each part's recorded decisions."})


BOARD_WORK_CAPTIONS.update({"interactions": "What waits on you: the open forms, then the decisions an agent proposed."})


PAPER_CAPTIONS.update({"interactions": BOARD_CAPTIONS["interactions"], "work-interactions": BOARD_WORK_CAPTIONS["interactions"]})


BOARD_CAPTIONS.update({"evidence": "What the paper quotes: its values and its citations, from work's Results.",
                       "displays": "What the reader sees: each display planned against the venue's rules, then each one as the paper prints it."})


PAPER_CAPTIONS.update({"evidence": BOARD_CAPTIONS["evidence"], "work-evidence": "What the evidence still waits on: each value and citation, and its state.",
                       "displays": BOARD_CAPTIONS["displays"], "work-displays": "What the displays still wait on: each display, its Run and the venue check."})


BOARD_CAPTIONS.update({"explore": "The Blocks that support this paper: work Blocks explore inside (the analysis and its Runs), discovery Blocks outside."})


PAPER_CAPTIONS.update({"explore": BOARD_CAPTIONS["explore"], "work-explore": "The work and discovery Blocks this paper draws on, each to open."})


PAPER_CAPTIONS.update({"work-values": "The printed numbers, one Task per group, each read from a returned Result.",
                 "work-citations": "The citations, one Task per claim group, each paper checked."})
