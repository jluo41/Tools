"""📃 Page · the Page view's side parts: the board-level link, the band under the title, RoadMap Draw, and the no-plan note.

Moved out of outline.py (the 600-line rule); outline re-exports every name here.
"""
import re
from pathlib import Path
from urllib.parse import quote

from src.common import delivery_read_lane_dir
from src.outline_version import plan_dir, latest_outline, version_tag
from live.outline_plan_html import _e


# The page-level surface has to be able to get back to the board-level one.
# `servers/workbench-design/design.py` has carried `↑ Board level` on its Page surface since the
# design workbench shipped (design.py, the `board_link` line), and its board
# surface links back DOWN to each page. 📃 Page had only the downward half:
# the Paper Workbench emits 202 links into page Outlines on one real board, and
# the Outline page emitted zero links back (JL 260921). One breadcrumb closes
# the loop for every board kind that HAS a board-level surface.
_BOARD_LEVEL_ROUTES = {
    "dialect": {"paper": ("paper", "\U0001F4C4")},
    "board-kind": {"design-board": ("design-board", "\U0001F3A8"),
                   "insight-board": ("insight-board", "\U0001F4A1"),
                   "labeling-board": ("labeling-board", "\U0001F3F7")},
}


def _board_line(link, page_src=None, root=None):
    """The `↑ Board level` link on its own line under the title, or nothing (standalone).
    No `all boards · board index` line (JL 261003: "I think we can delete this")."""
    return '<div class="wb-links mut">%s</div>' % link.replace(' \u00b7 ', '', 1) if link else ""


def page_roadmap_html(page_src, root):
    """Draft › RoadMap Draw, two cards (JL 261003). **Logic**: the Section's logic tree,
    `studio/<stem>-roadmap.excalidraw`, the person's drawing: an agent draws its first
    version (skill `draw-logic-tree`) and the person edits it here (edit=1; each stroke saves
    through Studio). **Section map**: where each part sits, `studio/<stem>-sections.excalidraw`,
    generated from the plan and its Evidence Items (skill `excalidraw-draft`), so it opens
    view only and says when the plan changed after it was drawn. Rendering writes nothing."""
    if page_src is None or root is None:
        return ""
    folder, stem = Path(page_src).parent, Path(page_src).stem

    def rel(path):
        try:
            return path.resolve().relative_to(Path(root).resolve()).as_posix()
        except ValueError:
            return ""

    def card(title, body, opened):
        return ('<details class=rd-card%s><summary>%s</summary>%s</details>'
                % (" open" if opened else "", _e(title), body))

    def frame(path, edit, label):
        url = _e("/_excalidraw/?board=%s%s" % (quote(rel(path), safe="/"), "&edit=1" if edit else ""))
        # no referrer: Excalidraw refuses a same-site embed, as on Paper's RoadMap Draw
        return ('<div class=rd-bar><a class=rd-open href="%s" target=_blank rel=noopener>Open full screen ↗</a></div>'
                '<iframe class=page-roadmap-frame title="%s" referrerpolicy=no-referrer data-src="%s"></iframe>'
                % (url, _e(label), url))

    beside = lambda name: folder / name if (folder / name).is_file() or not (folder / "studio" / name).is_file() \
        else folder / "studio" / name                     # beside the face; an old studio/ copy still reads (JL 261031)
    logic = beside("%s-roadmap.excalidraw" % stem)
    logic_body = frame(logic, True, "Logic") if logic.is_file() and rel(logic) else (
        '<div class=space-empty>No logic drawing yet. Draw the logic in the Runs panel copies the '
        'prompt that draws this Section&#39;s logic tree.</div>')
    smap = beside("%s-sections.excalidraw" % stem)
    if smap.is_file() and rel(smap):
        plan = latest_outline(plan_dir(folder), stem)
        items = folder / "draft" / ("%s-evidence-items.md" % stem)
        newer = [p.name for p in (plan, items) if p is not None and p.is_file()
                 and p.stat().st_mtime > smap.stat().st_mtime]
        note = ('<p class=rd-stale>❗ %s changed after this map was drawn: Redraw the Section map in the '
                'Runs panel.</p>' % _e(" and ".join(newer))) if newer else ""
        map_body = note + frame(smap, False, "Section map")
    else:
        map_body = ('<div class=space-empty>No Section map yet. Redraw the Section map in the Runs panel '
                    'copies the prompt that draws it from the plan.</div>')
    return card("Logic · why the claim holds (your drawing)", logic_body, True) + \
        card("Section map · where each part sits (generated)", map_body, True)


def _no_plan_html(page_src):
    """The Draft Space of a page with no plan yet (JL 261005: "why this is empty?"): say so, name
    the run that writes the first plan, and show the words as they stand, read from the page's
    own delivery fragment `delivery/latex/<stem>.tex` when it has one, so the page still reads."""
    note = ('<div class=card><h2>No plan yet</h2><p class=mut>This page has no Draft plan, so Table, '
            'Reading and Revise have nothing to show. <b>Structure revise</b>, in the Runs panel, '
            'writes the first plan: its headings, paragraph jobs and Bullet Points.</p></div>')
    tex = delivery_read_lane_dir(Path(page_src).parent, "latex") / (Path(page_src).stem + ".tex")
    try:
        raw = tex.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return note
    lines = [ln for ln in raw.splitlines() if not ln.lstrip().startswith("%")]   # LaTeX comments off
    paras = [p.strip() for p in re.split(r"\n\s*\n", "\n".join(lines)) if p.strip()]
    if not paras:
        return note
    body = "".join('<p style="margin:0 0 12px;line-height:1.6;white-space:pre-wrap">%s</p>' % _e(x) for x in paras)
    return note + ('<div class=card><h2>The words as they stand</h2><p class=mut>From <code>delivery/latex/%s</code>, '
                   'read only; the plan, once written, drives them.</p>%s</div>' % (_e(tex.name), body))


def _page_band(page_src):
    """The band under the title: the page's kind, its state and its plan version, read
    from the page and its draft/ folder. Empty for a standalone page."""
    if page_src is None:
        return ""
    try:
        text = Path(page_src).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    def field(key):
        got = re.search(r"(?m)^%s:\s*(.+?)\s*$" % re.escape(key), text)
        return re.sub(r"[*_`]+", "", got.group(1)).strip() if got else ""
    plan = latest_outline(plan_dir(Path(page_src).parent), Path(page_src).stem)
    # the state's word only, no emoji (JL 261003: "I don't want 🟡"): `🟡 PARTIAL - prose
    # inherited, …` reads `Partial`
    state = re.split(r"\s+[-–—·]\s+|[:,(]", field("state"), maxsplit=1)[0]
    state = re.sub(r"^[^A-Za-z]+", "", state).strip().capitalize()
    parts = [field("page-type") or field("folder-kind"), state,
             "draft %s" % version_tag(plan) if plan else "no draft yet"]
    parts = [x for x in parts if x]
    return '<div class="wb-band">%s</div>' % _e(" · ".join(parts)) if parts else ""


def board_level_link(page_src, root):
    """`· ↑ Board level 📄` when this page's board has a board-level surface.

    Returns "" for a standalone page, a page outside `--root`, or a board whose
    declared dialect/kind has no board-level workbench. A board-level route always
    takes `path=<board>/board.md&file=board.md`.
    """
    if page_src is None or root is None:
        return ""
    try:
        root_p = Path(root).resolve()
        here = Path(page_src).resolve().parent
    except (OSError, RuntimeError, ValueError):
        return ""
    board = None
    while here == root_p or root_p in here.parents:
        if (here / "board.md").is_file():
            board = here
            break
        if here == root_p:
            break
        here = here.parent
    if board is None:
        return ""
    try:
        text = (board / "board.md").read_text(encoding="utf-8", errors="replace")
        rel = board.relative_to(root_p)
    except (OSError, UnicodeError, ValueError):
        return ""
    route = mark = None
    for key, table in _BOARD_LEVEL_ROUTES.items():
        got = re.search(rf"(?m)^{re.escape(key)}:\s*(\S+)\s*$", text)
        if got and got.group(1).strip() in table:
            route, mark = table[got.group(1).strip()]
            break
    if not route:
        return ""
    path_param = quote(str(rel / "board.md"), safe="")
    return (' \u00b7 <a href="/_board/%s?path=%s&file=board.md">'
            '\u2191 Board level %s</a>' % (route, path_param, mark))
