"""The insight Board's Studio: where the method guide lives, the Board's drawings and what was generated."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

from .insight_board_reader import (  # noqa: F401 · this module keeps answering these names
    _e)


# Guide › Method: one file, the Insight method,
# naming its methods after the three columns of every question: question-asking (Logic, before any data
# is read), question-answering (Work, the run) and question-results reading (Report, the page). Not "design" or "discovery": those are the
# Design and Discovery families. The files are the workbench's own, the same for every board, kept with
# this server as every theme's Guide is (261007): guide/ (method, cards, canvas) and related/ (papers);
# the cards and paper cards are drawn as the Design workbench draws its methods.
METHODS_REF = Path(__file__).resolve().parent / "guide"


# The methods drawing (as the Design family's): one Excalidraw drawing of the loop and the
# question-asking, question-answering and question-results reading methods, opened in the self-hosted canvas and saved back.
METHOD_STUDIO = METHODS_REF / "methods.excalidraw"
METHOD_VIEWS = (("method", "Method"), ("papers", "Papers"))


def _studio_html(root: Path, editable: bool = True) -> str:
    """The methods drawing in the Excalidraw canvas. It loads only when shown; inside Guide it is view only."""
    from .designboard import _href
    rel = _href(root, METHOD_STUDIO) if METHOD_STUDIO.is_file() else ""
    if not rel:
        return f'<p class=note>No methods drawing yet: the insight workbench keeps it as <code>guide/{METHOD_STUDIO.name}</code>.</p>'
    url = "/_excalidraw/?board=" + quote(rel.lstrip("/"), safe="/") + ("&edit=1" if editable else "")
    return ('<div class=st-bar><span class=mut>The six steps, and the question-asking, question-answering and question-results reading methods of '
            'steps 1, 3 and 5. You can edit it here.</span>'
            f'<a href="{_e(url)}" target="_blank" rel="noopener">Open full screen ↗</a></div>'
            # no referrer: Excalidraw refuses a same-site embed ("I'm not a pretzel!")
            f'<iframe class=st-frame title="Methods studio" referrerpolicy="no-referrer" data-src="{_e(url)}"></iframe>')


# Question Book › RoadMap Draw: the Question Book's studio/ (workbench README, "Task alignment"): a
# freeform list of folding rows, one per studio/<name>.excalidraw beside its board.md. A row's canvas
# loads when it opens, view only; Edit drawing hands it the pen. The shared Studio routes (xcal.py)
# save the scene. The family's own explanatory drawings stay in Guide.


def _board_drawings(snap: dict) -> tuple[str, list[dict]]:
    """The studio/ folder (relative to the served root) and its drawings, in name order: the Question Book's
    when the board reads through one (RoadMap Draw lives in the Question Book), else the board's."""
    root = Path(snap["root"]).resolve()
    board = Path(snap.get("prototype") or snap["board"]).resolve()
    if not board.is_relative_to(root):
        return "", []
    studio = board / "studio"
    drawings = [{"title": p.stem.replace("_", " ").replace("-", " ").capitalize(),
                 "path": p.resolve().relative_to(root).as_posix(), **_generated(p, board)}
                for p in sorted(studio.glob("*.excalidraw"))
                if p.is_file() and p.resolve().is_relative_to(studio)] if studio.is_dir() else []
    drawings.sort(key=lambda d: not d.get("source"))       # the generated question map first
    return (board / "studio").relative_to(root).as_posix(), drawings


def _generated(path: Path, board: Path) -> dict:
    """A drawing a script writes (its `source` names the script, as the question map's does): shown view
    only, and `stale` when a question file is newer than it, so its script reruns."""
    try:
        source = json.loads(path.read_text(encoding="utf-8")).get("source", "")
    except (OSError, ValueError):
        return {}
    if not str(source).endswith(".py"):
        return {}
    made = path.stat().st_mtime
    stale = any(q.stat().st_mtime > made for q in board.glob("[1-4]-*/[DIKW][0-9][0-9]-*/[DIKW][0-9][0-9]-*.md"))
    return {"source": source, "stale": stale}


def _render_studio(snap: dict) -> str:
    folder, drawings = _board_drawings(snap)
    lead = ('<h2>RoadMap Draw</h2><p class=lead>The Question Book\'s studio: the question map, drawn from the question '
            'files, then any sketch in its studio/. Every board that reads this Question Book sees the same ones. Each '
            'drawing opens on its own, and several can stay open. How the Insight family works is in Guide.</p>')
    if snap["static"] or not folder:
        rows = "".join(f'<li><span class=mono>{_e(d["path"])}</span></li>' for d in drawings)
        return lead + (f'<ul>{rows}</ul>' if rows else '<p class=note>No drawings yet.</p>') + \
            '<p class=note>Drawings open and save on the live workbench.</p>'

    def row(d: dict) -> str:
        url = "/_excalidraw/?board=" + quote(d["path"], safe="/")
        if d.get("source"):                              # generated: view only, rerun its script
            note = ('❗ a question changed after it was drawn: rerun ' if d["stale"] else 'generated by ')
            return (f'<details class=draw data-board="{_e(d["path"])}"><summary>{_e(d["title"])}</summary>'
                    f'<div class=st-bar><span class=mut>{note}<span class=mono>{_e(d["source"])}</span>, never edited</span>'
                    f'<a href="{_e(url)}" target=_blank rel=noopener>Open full screen ↗</a></div>'
                    f'<iframe class=st-frame title="{_e(d["title"])}" referrerpolicy=no-referrer data-src="{_e(url)}"></iframe>'
                    '</details>')
        return (f'<details class=draw data-board="{_e(d["path"])}"><summary>{_e(d["title"])}</summary>'
                f'<div class=st-bar><span><button type=button class=draw-edit>Edit drawing</button> '
                f'<span class="mono mut">{_e(d["path"])}</span></span>'
                f'<a href="{_e(url)}&amp;edit=1" target=_blank rel=noopener>Open full screen ↗</a></div>'
                # no referrer: Excalidraw refuses a same-site embed ("I'm not a pretzel!")
                f'<iframe class=st-frame title="{_e(d["title"])}" referrerpolicy=no-referrer data-src="{_e(url)}"></iframe>'
                '</details>')
    empty = ('<p class=note id=draw-none>No drawings yet: run "Draw the question map" in the Runs panel.</p>')
    # no Add drawing form: the studio's drawings are the generated
    # question map and any sketch a run writes into studio/
    return (lead + f'<div class=draw-list data-studio="{_e(folder)}">'
            + ("".join(row(d) for d in drawings) or empty) + '</div>')
