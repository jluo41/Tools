"""🔎 Insight Board · one dataset, four Spaces, logic left and work right.

One workbench reads one extract (MT00 names it; a new extract is a new board).
Scope shows the dataset, its segments and the question registers.  Insight
shows one High/Low table per partition: on the left the questions asked at
Data, Information, Knowledge and Wisdom (MT01-MT04), on the right the runs
that answer them, joined by each task config's `answers:` line.  Check shows
the gates, the mechanical checks and the workflow runtime; Delivery the signed
handoffs.  Each Space has its Runs panel; a run line opens its results, and a
page opens as a document, in a pop-out.  Design: Tools/blueprints/Project-Ladder/work/b11_theme_insight/s02-insight-workbench/insight-workbench-design.excalidraw.
An Insight Block (a task Block with workbench: insight) is read by instance_reader.py into the same snapshot.
Insight › Studio lists the board's own studio/*.excalidraw drawings; the shared Studio
routes save them.  The shared Guide (workbench) mounts before Scope.

The board on disk stays authoritative.  This module only reads: the register
pages (their ASCII cell grids), the answering pages, the task configs whose
`store:` is this board's store, and their `runtime.yaml` receipts.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

from .insight_board_reader import (  # noqa: F401 · this module keeps answering these names
    _TITLE, _INSIGHT_BOARD, _LEVELS, _LEVEL_OF, _LEVEL_LABEL, _SKIP, _PAGE_ID, _PAGE_STEM, _PART_DIR, FULL,
    CROSS, _QID, _MARK, _LOG_LINE, _SERVES, _SIGNED, _CACHE, _read, _e, _header, _field, _section,
    is_insight_board, _safe_board, _BOARD_GLOBS, insight_boards, _board_by_name, _pages, _page_link,
    _grid_lines, _CELL_TOKEN, _cell_tokens, _parse_register, _parse_transposed, _parse_cell, _yaml_flat,
    _receipts, _receipt_row, _log_events, _parents, _rows, _inline, _partitions, _extract_context,
    board_snapshot, _first_para, handoff_records, _workflow_runtimes)
from .insight_board_assets import (  # noqa: F401 · this module keeps answering these names
    _CSS, _POP, _JS, _STUDIO_JS)
from .insight_board_register import (  # noqa: F401 · this module keeps answering these names
    _main, register_question, _register_question, _prepare_question_row)
from .insight_board_parts import (  # noqa: F401 · this module keeps answering these names
    _cell_view, _gates, _pill, _clip, _slug, _link, _tabs, _view, display_id, _spell_ids, render_board_list,
    _HEADS, _pretty, _partition_name, _GRAIN, _SHAPE, _WINDOW, _VARIANTS, _ROWS, _SIDECARS, _input_facts,
    _render_input_data, _TICKET_TARGET, _WORDS, _short_window, _dataset_line)
from .insight_board_runtime import (  # noqa: F401 · this module keeps answering these names
    _render_runtime_inventory, _tasks_root, _task_calls, groom_snapshot)
from .insight_board_work import (  # noqa: F401 · this module keeps answering these names
    page_cells, _REASONS, _SPACES, _ANSWERS, _STAGE, _part_label, _call_config, work_runs, page_tickets,
    _run_url, _pop_url, _answered_by, _builds_on, _behind, _numbers, _task_name, _idname, _run_note, _run_lines,
    _bindings, _STEP_WORD, _step_label, _needs_list, _instance_binding, _work_cell, _DIVISION, _FIELD, _NEED,
    question_notes)
from .insight_board_questions import (  # noqa: F401 · this module keeps answering these names
    _STRENGTH, _report_path, _sentences, report, _LEAD, _run_report, _report_cell, _logic_cell,
    _questions_table, _render_questions)
from .insight_board_studio import (  # noqa: F401 · this module keeps answering these names
    METHODS_REF, METHOD_STUDIO, METHOD_VIEWS, _studio_html, _board_drawings, _generated, _render_studio)
from .insight_board_spaces import (  # noqa: F401 · this module keeps answering these names
    _runs_panel, _resting, _run_rows, _report_rows, _space_kinds, _render_scope, _render_prototype_space,
    _gate_label, _gate_blocks, _render_check, _render_delivery)


METHOD_DOC = METHODS_REF / "method.md"
METHOD_PAPERS = METHODS_REF.parent / "related" / "papers.md"


def _render_methods(snap: dict, view: str = "method", only: tuple = (), editable: bool = True) -> str:
    """Guide › Method or Guide › Related Paper, one per page; `only` keeps those views."""
    from .designboard import _plain_md, method_cards
    from .related_papers import papers_page   # the shared Related Paper renderer (table-papers)
    board, root = snap["board"], Path(snap["root"])

    def method() -> str:
        # one page, as the Design family's: the drawing, then the six steps as the spine, the
        # steps that need detail in depth, why it works, and the reference. Every section is a fold card in
        # the Guide's RoadMap style ("I want the style like this"; "make each section collapsable"); the
        # six steps open, the rest closed, so the page opens as its outline. No tab bar.
        def fold(title: str, body: str, open_: bool = False) -> str:
            return (f'<details class=msec{" open" if open_ else ""}><summary><strong>{title}</strong></summary>'
                    f'<div class=msec-body>{body}</div></details>')
        drawing = fold("Methods drawing", _studio_html(root, editable))
        if not METHOD_DOC.is_file():
            return drawing + f'<p class=note>No method file yet: the insight workbench keeps it as <code>guide/{METHOD_DOC.name}</code>.</p>'
        html = re.sub(r"<h1>.*?</h1>", "", _plain_md(_read(METHOD_DOC), method_cards(board, root, METHOD_DOC, METHOD_PAPERS)), count=1)
        parts = re.split(r"<h2>(.*?)</h2>", html)            # [before, title, body, title, body, ...]
        cards = "".join(fold(parts[k], parts[k + 1], open_=(k == 1)) for k in range(1, len(parts), 2))
        return drawing + f'<article class=mdoc>{parts[0]}{cards}</article>'
    views = {"method": method,
             "papers": (lambda: papers_page(board, root, METHOD_PAPERS) if METHOD_PAPERS.is_file() else
                        f'<p class=note>No papers file yet: the insight workbench keeps it as <code>related/{METHOD_PAPERS.name}</code>.</p>')}
    shown = [(k, label) for k, label in METHOD_VIEWS if not only or k in only]
    view = view if view in dict(shown) else shown[0][0]
    bar = "".join(f'<button type=button data-mview="{k}"{" class=on" if k == view else ""}>{_e(label)}</button>'
                  for k, label in shown) if len(shown) > 1 else ""
    return (f'<div class=mlib><div class=mviews>{bar}</div>'
            + "".join(f'<div class="mview{" on" if k == view else ""}" data-mview="{k}">{views[k]()}</div>'
                      for k, _ in shown) + '</div>')


# Guide › Method and Guide › Related Paper frame the family's methods (Guide is the method and
# the skills, shared across workbenches; Scope is the board's own data). The pages are the same on every
# board, so no board is named. Read-only; the page tells its frame how tall it is, as Design's theory does.
_EXPLAIN_HEIGHT = ("<script>(function(){function post(){parent.postMessage({kind:'haipipe-explain-height',"
                   "height:document.documentElement.scrollHeight},location.origin)}"
                   "if(window.ResizeObserver)new ResizeObserver(post).observe(document.body);"
                   "addEventListener('load',post);document.addEventListener('toggle',post,true);"
                   "document.addEventListener('click',function(){setTimeout(post,60)},true)})()</script>")


# the methods page sits inside Guide: a pinch over it must not zoom the tab (guide-mount.js says why)
_NO_PINCH = ("<script>addEventListener('wheel',function(e){if(e.ctrlKey)e.preventDefault()},{passive:false});"
             "['gesturestart','gesturechange','gestureend'].forEach(function(t){addEventListener(t,function(e){e.preventDefault()},{passive:false})})</script>")


def render_methods_embed(root: Path, view: str = "method") -> str:
    """`method`: one page, the Insight method (question-asking, question-answering, question-results reading), then the methods drawing (its
    canvas editable, as the Design family's); `papers`: the papers."""
    snap = {"board": Path(root), "root": Path(root)}
    body = (_render_methods(snap, "papers", only=("papers",)) if view == "papers" else
            _render_methods(snap, "method", only=("method",)))
    return ('<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">'
            # inside Guide this page's frame takes the page's own height, so nothing here is sized by the
            # viewport: a 100vh canvas would grow the frame, which grows the canvas, without end
            f'<title>🔎 Insight · {_e(view)}</title><style>{_CSS}body{{max-width:none;padding:2px 2px 12px}}.shell{{border:0;padding:0;border-radius:0}}.st-frame{{height:640px;min-height:0}}.rp-frame{{height:720px}}</style></head>'
            f'<body data-space=scope><main><div class=shell>{body}</div></main>{_JS}{_EXPLAIN_HEIGHT}{_NO_PINCH}</body></html>')


def render_insight_board(snapshot: dict, space: str = "insight",
                         selected_question: str = "", selected_partition: str = "") -> str:
    snap = snapshot
    aliases = {"overview": "scope", "registers": "scope", "partitions": "scope", "workspace": "scope",
               "evidence": "insight", "run": "check", "workflow": "check", "groom": "check"}
    space = aliases.get(space, space)
    if space not in {k for k, _ in _SPACES}:
        space = "insight"
    qids = snap["question_ids"]
    pids = [row["id"] for row in snap["partitions"]]
    qid = selected_question if selected_question in qids else ("QW1" if "QW1" in qids else (qids[0] if qids else ""))
    pid = selected_partition if selected_partition in pids else (FULL if FULL in pids else (pids[0] if pids else ""))
    sel = f"{pid}:{qid}" if qid and pid else ""
    kinds = _space_kinds(snap)
    bodies = {"prototype": _render_prototype_space(snap), "scope": _render_scope(snap), "insight": _render_questions(snap, pid, sel),   # its Views are the segments
              "check": _render_check(snap), "delivery": _render_delivery(snap)}
    nav = '<nav class=spaces>' + "".join(f'<button class=space type=button data-space="{k}">{label}</button>'
                                         for k, label in _SPACES) + '</nav>'
    panes = "".join(f'<section class=pane data-space="{k}"><div class=split><div class=shell>{bodies[k]}</div>'
                    f'{_runs_panel(k, kinds[k])}</div></section>' for k, _ in _SPACES)
    document = _spell_ids(snap, "".join([
        '<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        f'<title>🔎 {_e(snap["title"])}</title><style>{_CSS}</style></head>'
        f'<body data-space="{_e(space)}" data-sel="{_e(sel)}"><main>',
        f'<header><h1>🔎 {_e(snap["title"])}</h1></header>',   # no `all boards · board index` line; no dataset banner
        nav, panes, _POP, "</main>", _JS, _STUDIO_JS, "</body></html>",
    ]))
    if snap["static"]:
        return document
    from live.workbench_guide import mount_guide
    return mount_guide(document, "insight", {"path": (snap["relative"] + "/board.md").lstrip("/"), "file": "board.md"},
                       "nav.spaces", ".pane")


# ─── pop-outs: a run's results, a page as a document ────────────────────────

def _result_kit():
    from .paper import _RESULT_PAGE, _csv_view, _md_view
    return _RESULT_PAGE, _csv_view, _md_view


def render_insight_run(snap: dict, task_rel: str, call: str, page: str = "") -> str:
    """One task call's results: its receipt, then summaries, figures, tables and
    every other file.  The run's results are the answer; no page stands between."""
    page_tpl, csv_view, md_view = _result_kit()
    root = Path(snap["root"]).resolve()
    run = next((r for r in work_runs(snap) if r["call"] == call and r.get("page", "") == page and
                r["task_path"].resolve().relative_to(_tasks_root(snap).resolve()).as_posix() == task_rel.strip("/")), None)
    if run is None:
        raise FileNotFoundError(f"{task_rel} · {call}")
    raw = lambda f: "/" + quote(f.resolve().relative_to(root).as_posix(), safe="/")
    inside = lambda f: f.resolve().is_relative_to(root)
    res = run["receipt"].parent
    files = sorted(f for f in res.rglob("*") if f.is_file() and not f.name.startswith(".")) if res.is_dir() else []
    qa = sorted((res.parent.parent / "QA").glob("*.md")) if (res.parent.parent / "QA").is_dir() else []
    links = [f'<a href="{_e(raw(f))}" target=_blank rel=noopener>{label} ↗</a>'
             for f, label in ((run["ticket"], "Run script"), (run["config"], "Config")) if f and f.is_file() and inside(f)]
    body = [f'<h1>{_e(call)}</h1><p class="where mut"><code>{_e(res.resolve().relative_to(root).as_posix() if inside(res) else res.name)}</code>'
            f' · answers {_e(", ".join(run["answers"]) or "no question")}</p>', f'<div class=links>{"".join(links)}</div>']
    if run["receipt"].is_file():
        body.append(f'<h2>Receipt</h2><pre>{_e(_read(run["receipt"])[:4000])}</pre>')
    else:
        body.append('<p class=mut>Not run yet: no receipt.</p>')
    docs = qa + [f for f in files if f.suffix.lower() in {".md", ".txt"}]
    if docs:
        body.append(f'<h2>Summaries · {len(docs)}</h2>' + "".join(
            f'<div class=doc><h3>{_e(f.name)}</h3>{md_view(_read(f)) if f.stat().st_size < 200_000 else "<p class=mut>too long to show here</p>"}</div>'
            for f in docs))
    figs = [f for f in files if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".webp"}]
    if figs:
        body.append(f'<h2>Figures · {len(figs)}</h2><div class=figs>' + "".join(
            f'<figure><img loading=lazy src="{_e(raw(f))}" alt="{_e(f.name)}"><figcaption>{_e(f.name)}</figcaption></figure>'
            for f in figs if inside(f)) + '</div>')
    tabs = [f for f in files if f.suffix.lower() in {".csv", ".tsv"}]
    for f in tabs:
        if f is tabs[0]:
            body.append(f'<h2>Tables · {len(tabs)}</h2>')
        body.append(f'<h3>{_e(f.name)}</h3>{csv_view(f)}')
    rest = [f for f in files if f not in docs and f not in figs and f not in tabs and f != run["receipt"]]
    if rest:
        body.append(f'<h2>Other files · {len(rest)}</h2><ul class=files>' + "".join(
            f'<li><a href="{_e(raw(f))}" target=_blank rel=noopener>{_e(f.name)}</a></li>' if inside(f) else f'<li>{_e(f.name)}</li>'
            for f in rest) + '</ul>')
    return page_tpl.format(title=_e(call), body="\n".join(body))


def render_insight_report(snap: dict, qid: str, pid: str) -> str:
    """One report file as a document, for the pop-out."""
    page_tpl, _, md_view = _result_kit()
    text = _read(_report_path(snap, qid, pid))
    title = _TITLE.search(text)
    body = re.sub(r"\A#[^\n]*\n", "", text)
    return page_tpl.format(title=_e(title.group(1) if title else qid), body=(
        f'<h1>{_e(title.group(1).strip() if title else qid)}</h1>'
        f'<p class="where mut">{_e(_STAGE.get(qid[1:2], ""))} question {_e(qid[2:])} on {_e(_part_label(snap, pid))}</p>'
        + md_view(body)))


def render_insight_page(snap: dict, page: dict) -> str:
    """One page as a document, for the pop-out: the shared Page reader, the same document the
    web delivery writes (workbench/page/page_reader.py)."""
    from live.page_reader import page_document
    cells = page_cells(snap, page)
    where = " · ".join(f'{_STAGE[q[1]]} question {q[2:]} on {_part_label(snap, p)}' for q, p in cells) or "answers no register question"
    name = display_id(page["id"], {p["id"]: p["name"] for p in snap["partitions"]})
    source = "/" + quote(f"{snap['relative']}/{page['rel']}", safe="/")
    return page_document(page["path"], snap["root"],
                         f'<span class=mut>{_e(name)} · {_e(where)}</span> '
                         f'<a href="{_e(source)}" target=_blank rel=noopener>Source ↗</a>')





# ─── server mixin ───────────────────────────────────────────────────────────

_RETIRED_SPACE = {"scope": "Description", "prototype": "Description", "insight": "Audience Report",
                  "check": "Runs", "delivery": "Delivery"}


class InsightBoardMixin:
    """GET/HEAD/POST read-only surface for a whole InsightBoard."""

    def _insight_target(self, raw: str) -> Path | None:
        return _safe_board(Path(self.root), raw) or _board_by_name(Path(self.root), raw)

    def insight_board_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        raw = (query.get("board") or query.get("path") or [""])[0]
        embed = (query.get("embed") or [""])[0]
        if embed == "methods":
            view = (query.get("view") or ["method"])[0]
            return self._insight_board_send(render_methods_embed(Path(self.root), view).encode("utf-8"), 200, head_only)
        board = self._insight_target(raw)
        if board is None:
            # The workbench has two levels, board and page, and no list of its
            # own.  No board named: go to the one InsightBoard
            # when there is exactly one.  Otherwise a short 404 that names
            # what was asked and what exists.
            boards = insight_boards(Path(self.root))
            if not raw and len(boards) == 1:
                self.send_response(302)
                self.send_header("Location", f"/_board/insight-board?board={quote(boards[0].name)}")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            body = render_board_list(Path(self.root), raw).encode("utf-8")
            return self._insight_board_send(body, 404, head_only)
        from .instance_reader import board_kind, legacy_snapshot, render_file
        kind = board_kind(board)
        if not (query.get("file") or [""])[0]:
            # Retired: the board opens in the workbench (/_board/workbench, the insight theme,
            # b11 s11 · s12 · s13). Its old Spaces map to the new ones; screenshots of this page are kept in
            # Tools/blueprints/Project-Ladder/work/b11_theme_insight/s11-block-level/old-insight-board/.
            old_space = (query.get("space") or ["insight"])[0]
            space = _RETIRED_SPACE.get(old_space, "Audience Report")
            from .insight_plan_c import JOB_NAME
            jobs = sorted(j for j in board.iterdir() if j.is_dir() and JOB_NAME.match(j.name))
            target = jobs[-1] if jobs and old_space in ("insight", "check") else board   # the Q │ W │ R rows: a Job's
            try:
                where = target.resolve().relative_to(Path(self.root).resolve()).as_posix()
            except ValueError:
                where = board.name
            self.send_response(302)
            self.send_header("Location", f"/_board/workbench?path={quote(where)}&space={quote(space)}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        if kind:
            # an Insight Block (haipipe-insight ref/block-contract.md): the same workbench, its data
            # read by instance_reader for one dataset; a file opens in the pop-out
            wanted = (query.get("file") or [""])[0]
            if wanted == "board.md":                 # the Board's own face (the `/w/` and Home link): the board
                wanted = ""
            if wanted:
                code, page = render_file(board, Path(self.root), wanted)
                return self._insight_board_send(page.encode("utf-8"), code, head_only)
            body = render_insight_board(
                legacy_snapshot(board, Path(self.root), (query.get("dataset") or [""])[0]),
                (query.get("space") or ["insight"])[0],
                (query.get("q") or query.get("question") or [""])[0],
                (query.get("p") or query.get("partition") or [""])[0]).encode("utf-8")
            return self._insight_board_send(body, 200, head_only)
        snapshot = board_snapshot(board, self.root, raw)
        body = render_insight_board(
            snapshot, (query.get("space") or ["insight"])[0],
            (query.get("q") or query.get("question") or [""])[0],
            (query.get("p") or query.get("partition") or [""])[0],
        ).encode("utf-8")
        return self._insight_board_send(body, 200 if snapshot["current"] else 404, head_only)

    def insight_page_view(self, head_only=False):
        """GET /_board/insight?path=<board>&file=<page.md>: one page as a document (the pop-out)."""
        query = parse_qs(urlparse(self.path).query)
        payload = {"path": (query.get("path") or [""])[0], "file": (query.get("file") or [""])[0]}
        short_board = (query.get("board") or [""])[0]
        short_page = (query.get("page") or [""])[0].strip()     # `W02-full`: ids keep their case
        wanted = (query.get("report") or [""])[0]
        if short_board and ":" in wanted:
            # ?board=<name>&report=<segment>:<question>: one report file as a document
            board = _board_by_name(Path(self.root), short_board)
            snap = board_snapshot(board, self.root) if board else None
            pid, qid = wanted.split(":", 1)
            path = _report_path(snap, qid, pid) if snap else None
            if path is None or not path.is_file():
                return self._insight_board_send(f"<p>No report {_e(wanted)} on this board.</p>".encode("utf-8"), 404, head_only)
            return self._insight_board_send(render_insight_report(snap, qid, pid).encode("utf-8"), 200, head_only)
        if short_board and short_page:
            # Short form for a terminal: ?board=<folder name>&page=<page id>.
            board = _board_by_name(Path(self.root), short_board)
            hit = next((p for p in (_pages(board) if board else []) if p["id"].lower() == short_page.lower()), None)
            if board is None or hit is None:
                body = f"<h1>🔎 Insight</h1><p>no page {_e(short_page)} on board {_e(short_board)}</p>".encode("utf-8")
                return self._insight_board_send(body, 404, head_only)
            payload = {"path": "/" + board.relative_to(Path(self.root)).as_posix() + "/board.md", "file": hit["rel"]}
        got = self.target(payload)
        if got[0] is None:
            body = f"<h1>🔎 Insight</h1><p>{_e(got[1])}</p>".encode("utf-8")
            return self._insight_board_send(body, 404, head_only)
        page_src, board = Path(got[0]), Path(got[1])
        snapshot = board_snapshot(board, self.root, payload["path"])
        page = next((p for p in snapshot["pages"] if p["path"].resolve() == page_src.resolve()), None)
        if page is None:
            body = "<h1>🔎 Insight</h1><p>this file is not a page of an InsightBoard</p>".encode("utf-8")
            return self._insight_board_send(body, 404, head_only)
        body = render_insight_page(snapshot, page).encode("utf-8")
        return self._insight_board_send(body, 200 if snapshot["current"] else 404, head_only)

    def insight_run_view(self, head_only=False):
        """GET /_board/insight-run?board=<name>&task=<task folder>&call=<call>: one run's results."""
        query = parse_qs(urlparse(self.path).query)
        answer = (query.get("answer") or [""])[0]
        if answer:                                  # a plan-C Task: its answer page, from its face and runs
            root = Path(self.root).resolve()
            tdir = (root / answer.lstrip("/")).resolve()
            if not tdir.is_relative_to(root) or not (tdir / f"{tdir.name}.md").is_file():
                return self._insight_board_send("<p>No such Task.</p>".encode("utf-8"), 404, head_only)
            from .insight_views import render_task_page
            return self._insight_board_send(render_task_page(tdir, root).encode("utf-8"), 200, head_only)
        wanted = (query.get("run") or [""])[0]
        if wanted:                                  # a plan-C hard Run: <Board>/<Job>/<Task>/runs/rNN_<segment>/
            root = Path(self.root).resolve()
            rundir = (root / wanted.lstrip("/")).resolve()
            if not rundir.is_relative_to(root) or rundir.parent.name != "runs" or not (rundir / "run.yaml").is_file():
                return self._insight_board_send("<p>No such run.</p>".encode("utf-8"), 404, head_only)
            from .insight_views import render_run_page
            return self._insight_board_send(render_run_page(rundir, root).encode("utf-8"), 200, head_only)
        board = self._insight_target((query.get("board") or [""])[0])
        if board is None:
            return self._insight_board_send("<p>No such InsightBoard.</p>".encode("utf-8"), 404, head_only)
        from .instance_reader import board_kind, render_run
        if board_kind(board) == "insight-block":
            try:
                body = render_run(board, Path(self.root), (query.get("task") or [""])[0], (query.get("call") or [""])[0])
            except (FileNotFoundError, ValueError) as exc:
                return self._insight_board_send(f"<p>No such run on this board: {_e(exc)}</p>".encode("utf-8"), 404, head_only)
            return self._insight_board_send(body.encode("utf-8"), 200, head_only)
        snapshot = board_snapshot(board, self.root)
        try:
            body = render_insight_run(snapshot, (query.get("task") or [""])[0], (query.get("call") or [""])[0],
                                      (query.get("page") or [""])[0])
        except (FileNotFoundError, ValueError) as exc:
            return self._insight_board_send(f"<p>No such run on this board: {_e(exc)}</p>".encode("utf-8"), 404, head_only)
        return self._insight_board_send(body.encode("utf-8"), 200, head_only)

    def plug_insight_page(self, payload):
        got = self.target(payload)
        if got[0] is None:
            return None, got[1]
        if not is_insight_board(Path(got[1])):
            return None, "this page is not on an InsightBoard"
        return {"url": "/_board/insight?path=%s&file=%s"
                % (quote(payload.get("path") or ""), quote(payload.get("file") or ""))}, None

    def _insight_board_send(self, body: bytes, code: int, head_only: bool):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_insight_board(self, payload):
        board = self._insight_target(payload.get("path") or payload.get("board") or "")
        if board is None:
            return None, "path must identify a Board with board.md"
        if not is_insight_board(board):
            return None, "selected Board is not an InsightBoard"
        if payload.get("action") == "ask":
            try:
                qid, pids = register_question(
                    board, payload.get("level", ""), payload.get("question", ""),
                    payload.get("partition") or payload.get("partitions") or "",
                    payload.get("origin", ""), payload.get("parent", ""),
                    workflow_runtime_id=payload.get("workflow_runtime_id", ""),
                    actor=payload.get("actor") or "board-ask")
            except ValueError as exc:
                return None, str(exc)
            return {"url": f"/_board/insight-board?board={quote(board.name)}&space=insight&q={qid}&p={pids[0]}",
                    "question": qid, "partitions": pids}, None
        return {"url": "/_board/insight-board?board=%s" % quote(board.name)}, None



if __name__ == "__main__":
    import sys
    raise SystemExit(_main(sys.argv[1:]))
