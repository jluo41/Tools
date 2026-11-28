"""🎨 Design Board · the Board-level grain of the Design workbench.

One DesignBoard holds a Brief with a list of designs (one line per audience ×
job × venue, with how many designs it asks for and which Insight board it
draws from) and many Design Folders under ``2-Design/``.  This presenter
stacks every folder's ``design_snapshot`` into one view, in the same five
Spaces as the Page level, one grain up: Goal (the list of design tasks),
Design (every item), Insight (the boards and pages the programme draws on),
Run (who is waited on, what ran), Delivery (what is ready for handoff).  It reads the
same files as the Page level and stores nothing of its own.  Its two writes
are adding design tasks to the design task file (0-BR-brief) and opening a Design Folder for a
line that has none yet.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlencode, urlparse  # noqa: F401

from live.design import (  # noqa: F401  (kept as before the split: readers reach these through designboard)
    _READS as _READS_LINE, _TITLE, _declared_insight_boards, _escape as _e, _handoff_says, _insight_bindings, _json, _read,
    because_words, shared_rules,
    brief_page, brief_rows, with_link, design_runs_panel, design_snapshot, design_title, runs_panel_assets,
    is_task_header, venue_word,
)

# The board lives in designboard_<part>.py, one module per part; every name stays importable from here
# (serve.py, design.py, home, the Guide, insightboard and the tests read them as designboard.<name>).
from live.designboard_snapshot import (  # noqa: F401
    _FIELD, _DESIGN_BOARD, _BOARD_GLOBS, DESIGN_GROUP, _FOLDER_ID, _METHOD_GROUP, METHOD_CARD, _field,
    is_design_board, design_groups, design_boards, resolve_board, reads_names, design_board_snapshot,
    _folder_summary, _board_insight_space)
from live.designboard_writes import (  # noqa: F401
    _ROW, _TABLE_COLUMNS, _FILLER, _slug, _table_bounds, _ensure_columns, add_tasks, new_folder,
    _write_design_folder, _finish_new_folder, _new_method_folder, _owner, _list_page)
from live.designboard_style import (  # noqa: F401
    _CSS, _THEORY_JS, _NO_PINCH)
from live.designboard_theory import (  # noqa: F401
    METHODS, THEORY, B12, B12_METHODS, STUDIO, UNIT, _pipe_rows, _plain_md, THEORY_VIEWS, studio_html, PAPER_ROLES,
    UTD24, _href, _paper_card, _paper_pdf, _run_abstract, is_utd24, paper_id, paper_rows, paper_runs, short_cite,
    _papers_page, PAPERS, papers_page, method_card_fields, CARD_KEYS, LIT_FIELDS, AI_FIELDS, method_cards)
from live.designboard_render import (  # noqa: F401
    _page_url, _method_views, _card_parts, _rationale, _method_steps, render_design_board, board_path_of,
    bundle_rows, bundle_csv)


def theory_page(board: Path, root: Path | None = None, view: str = "design-theory", only=None) -> str:
    """The theory of design: one view at a time, its name in a bar above it. `only` keeps a
    subset of the views, in its order (Guide's Method shows the methods, the studio and
    the theory; its Related Paper shows the papers alone)."""
    def article(path: Path, cls: str, empty: str) -> str:
        if path.is_file():
            return f'<article class="{cls}">{_plain_md(path.read_text(encoding="utf-8"))}</article>'
        return f'<div class=empty>{empty}</div>'
    # build only the views this page shows: the papers
    # view reads every Paper Run, about six seconds, and Guide › Method never shows it
    builders = {
        "design-theory": lambda: article(THEORY, "theory", "No design theory file is present."),
        "methods": lambda: (f'<article class="theory">{_plain_md(_read(METHODS), method_cards(board, root or board, METHODS, PAPERS, in_use="in the Exp", now="in Evaluate"))}</article>'
                            if METHODS.is_file() else '<div class=empty>No design methods file is present.</div>'),
        "studio": lambda: studio_html(root or board, STUDIO),
        "unit": lambda: studio_html(root or board, UNIT, "One design unit in five steps; ③ and ④ run once per "
                                    "idea. Above, every choice in each step; below, one row per method, holding "
                                    "only the choices that make it."),
        "papers": lambda: papers_page(board, root or board, PAPERS)}
    wanted = set(only) if only else {k for k, _ in THEORY_VIEWS if k != "method"}
    if "method" in wanted:
        wanted |= {"methods", "studio", "unit"}
    views = {k: build() for k, build in builders.items() if k in wanted}
    if "method" in wanted:
        untitled = lambda h: re.sub(r"<h1>.*?</h1>", "", h, count=1)
        # the drawing first, the method in one picture
        page = untitled(views["methods"])
        # every part folds, in the drawing's card style,
        # and every card starts closed, as on the shared Method page ("make it into this style")
        inner = page[page.find(">") + 1:page.rfind("</article>")] if page.startswith("<article") else page
        bits = re.split(r"(<h2>.*?</h2>)", inner)
        cards = bits[0]
        for title_html, body in zip(bits[1::2], bits[2::2]):
            title = re.sub(r"<[^>]+>", "", title_html)
            cards += (f'<details class=sec-fold><summary><strong>{title}</strong>'
                      f'</summary><div class=sec-body>{body}</div></details>')
        page = f'<article class="theory">{cards}</article>'
        # the drawing in a folding card, as Guide › RoadMap Draw shows "Workbench design"
        # no subtitle under the card's name
        views["method"] = ('<details class=draw-fold><summary><strong>Method design</strong>'
                           f'</summary><div class=draw-body>{views["studio"]}</div></details>'
                           # the design unit beside it
                           '<details class=draw-fold><summary><strong>Design unit · See input → Reason ideas → '
                           'Conduct process → Check output → Check overall</strong></summary>'
                           f'<div class=draw-body>{views["unit"]}</div></details>' + page)
    labels = dict(THEORY_VIEWS)        # `only` also sets the order (Guide's Method: methods first, theory last)
    plain = [(k, v) for k, v in THEORY_VIEWS if k != "method"]    # Method shows only when asked for
    shown = [(k, labels[k]) for k in only if k in labels] if only else plain
    shown = shown or plain
    view = view if view in dict(shown) else shown[0][0]
    bar = "".join(f'<button type=button data-view="{k}"{" class=on" if k == view else ""}>{_e(label)}</button>'
                  for k, label in shown)
    return ((f'<div class=views>{bar}</div>' if len(shown) > 1 else "")
            + "".join(f'<div class="view{" on" if k == view else ""}" data-view="{k}">{views[k]}</div>' for k, _ in shown))


def render_theory_embed(snapshot: dict, view: str = "methods", only=None) -> str:
    """The theory of design as one page, for Guide › Method to frame: Design
    theory · Design methods (the method cards) · Methods studio · Papers, one view at a time.
    Read-only; it tells its frame how tall it is."""
    theory_html = theory_page(Path(snapshot["board"]), Path(snapshot["root"]), view, only)
    height = ("<script>(function(){function post(){parent.postMessage({kind:'hai-explain-height',"
              "height:document.documentElement.scrollHeight},location.origin)}"
              "if(window.ResizeObserver)new ResizeObserver(post).observe(document.body);"
              "addEventListener('load',post);document.addEventListener('toggle',post,true);"
              "document.addEventListener('click',function(){setTimeout(post,60)},true)})()</script>")
    return ('<!doctype html><html lang=en><head><meta charset=utf-8>'
            '<meta name=viewport content="width=device-width,initial-scale=1">'
            # inside Guide this page's frame takes the page's own height, so nothing here is sized by the
            # viewport: a 100vh canvas would grow the frame, which grows the canvas, without end
            f'<title>🎨 Design · {_e(view)}</title><style>{_CSS}body{{max-width:none;padding:2px 2px 12px}}.st-frame{{height:640px;min-height:0}}.rp-frame{{height:720px}}</style></head><body>'
            f'<main><section class="pane on" data-space=theory><div class=space-main>{theory_html}</div></section></main>'
            f'<script>(function(){{{_THEORY_JS}}})();</script>{height}{_NO_PINCH}</body></html>')


THEORY_SPACES = ("theory", "theories", "knowledge", "methods", "studio", "papers")


class DesignBoardMixin:
    """GET/HEAD/POST surface for a whole DesignBoard."""

    def _design_board_target(self, raw: str) -> Path | None:
        return resolve_board(Path(self.root), raw)

    def design_board_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        raw = (query.get("board") or query.get("path") or [""])[0]
        board = self._design_board_target(raw)
        if board is None or not is_design_board(board):
            items = "".join(
                f'<li><a href="/_board/design-board?board={quote(b.name)}">{_e(b.name)}</a></li>'
                for b in design_boards(Path(self.root))) or "<li>No DesignBoard under this root.</li>"
            body = ("<!doctype html><meta charset=utf-8><title>🎨 Design Board</title>"
                    '<body style="font:14px/1.5 system-ui;margin:24px"><h1>🎨 Design Board</h1>'
                    f"<p>This link does not name a DesignBoard (got <code>{_e(raw) or 'nothing'}</code>). Pick one:</p>"
                    f"<ul>{items}</ul></body>").encode("utf-8")
            # a bare link is a question with a good answer (the list); a wrong name is a 404
            return self._design_board_send(body, 404 if raw else 200, head_only)
        space, view = (query.get("space") or ["goal"])[0], (query.get("view") or [""])[0]
        embed = (query.get("embed") or [""])[0]
        if space in THEORY_SPACES and embed != "theory":
            # the theory moved into Guide: an old link opens Guide › Method (papers: Related Paper)
            self.send_response(303)
            # Guide's views (261002): Method holds the theory; Related Paper the papers
            target = "related-paper" if space == "papers" or view == "papers" else "method"
            self.send_header("Location", "/_board/design-board?" + urlencode({"path": raw, "guide": target}))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if embed == "theory":
            # the theory page reads only the board's place, never its pages, items or runs: building
            # the whole board snapshot first took about six seconds
            only = [v for v in ((query.get("views") or [""])[0]).split(",") if v] or None
            body = render_theory_embed({"board": board, "root": self.root}, view or "methods", only).encode("utf-8")
        else:
            snapshot = design_board_snapshot(board, self.root)
            body = render_design_board(snapshot, space, view or "design-theory").encode("utf-8")
        return self._design_board_send(body, 200, head_only)

    def design_bundle_view(self, head_only=False):
        """GET /_board/design-bundle?path=… -> every design on the board as CSV."""
        query = parse_qs(urlparse(self.path).query)
        board = self._design_board_target((query.get("board") or query.get("path") or [""])[0])
        if board is None or not is_design_board(board):
            return self._design_board_send(b"no DesignBoard at that path", 404, head_only)
        snapshot = design_board_snapshot(board, self.root)
        body = bundle_csv(snapshot, (query.get("folder") or [""])[0]).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{board.name}-design-bundle.csv"')
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def _design_board_send(self, body: bytes, code: int, head_only: bool):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_design_board(self, payload):
        board = self._design_board_target(payload.get("path") or "")
        if board is None:
            return None, "path must identify a Board with board.md"
        if not is_design_board(board):
            return None, "selected Board is not a DesignBoard"
        return {"url": "/_board/design-board?path=%s" % quote(payload.get("path") or "")}, None

    def design_board_act(self, payload):
        board = self._design_board_target(payload.get("path") or "")
        if board is None or not is_design_board(board):
            return None, "path must identify a DesignBoard"
        action = payload.get("action")
        path_q = quote(payload.get("path") or "")
        try:
            if action == "new-folder":
                out = new_folder(board, str(payload.get("row") or ""), str(payload.get("method") or ""))
                out["url"] = "/_board/design?path=%s&file=%s&space=goal" % (path_q, quote(out["rel"], safe=""))
            elif action == "add-tasks":
                try:
                    designs = int(str(payload.get("designs") or "0").strip() or "0")
                except ValueError:
                    raise ValueError("how many designs must be a whole number") from None
                out = add_tasks(board, str(payload.get("subgroups") or "").splitlines(),
                                str(payload.get("job") or ""), str(payload.get("venue") or ""), designs,
                                str(payload.get("insight") or "").strip(),
                                str(payload.get("open") or "yes").lower() not in ("no", "false", "0", ""))
                out["url"] = "/_board/design-board?path=%s&space=goal" % path_q
            else:
                return None, f"unknown action {action!r}"
        except (ValueError, OSError) as exc:
            return None, str(exc)
        return out, None
