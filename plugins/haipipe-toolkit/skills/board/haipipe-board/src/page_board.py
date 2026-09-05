"""The cover + index + whole-page assembly (QB5: render(), asset inlining,
CJK scrub, JSON emission — moved verbatim from build.py)."""
import base64
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote

from . import body as bd
from .body import body, inline, nav_inline
from .common import aim_progress, esc, sec, stinfo
from .item_table import (action_label, compact_global_run, planned_route_anchor,
                         read_items, readable_global_run, readable_task,
                         repo_root, run_registry)
from .page_question import (has_outline_plan, parse_content_sections,
                            render_question, split_stage_record, structure_rows)
from .page_stage import render_doc_slide


# The map answers BOTH halves of "where am I" (JL 260731: "did you say what
# folders are used here? engine folder, output folder ... I think here we need
# to mention this as well"). A reader who knows how the groups connect but not
# which folder holds the engine still cannot act, so the heading names folders
# first and pages second.
def server_root(board_dir):
    """The folder `/_excalidraw/?board=<rel>` paths are relative to.

    The proxy resolves scene paths against the folder serve.py was started
    in, and the convention (QO13) starts it at the repo root — so the root
    marker is the repo's own: `.git`, with `pyproject.toml` kept for trees
    that carry one above the boards. Returning None blanks every canvas that
    needs it, which is the honest fallback on a bare static host.
    """
    return next((p for p in (board_dir, *board_dir.parents)
                 if (p / "pyproject.toml").is_file() or (p / ".git").exists()),
                None)


MAP_HEAD = ('<div class="board-map-head">'
            '<div><span class="board-map-kicker">BOARD MAP</span>'
            '<h2 id="board-map-title">Folders, pages, and how they connect</h2></div>'
            '<p>Which folder holds what, and which pages depend on which. '
            'Arrows are authored; placement is not.</p>'
            '</div>')


def board_map(meta):
    """The Board-level relationship map, if this Board has one.

    THREE sources, and an ASCII `## Board Map` beats both canvases (JL 260730:
    "I think I might need the ASCII version"). The reason is reach: a fenced
    figure draws on a static host with no Excalidraw endpoint and no share URL,
    it survives with scripts off, and since 0.53.0 every page and group id
    inside it is a real link, so the map is the only one you can travel on. An
    iframe can do none of that.

    It is also a DISCLOSURE rather than a fixed 62vh block, because a map you
    cannot shut is a map that pushes the index off the first screen.

    The scene, whichever source wins, is never a second registry of pages:
    arrows are authored deliberately, and proximity or index order never imply
    a dependency.
    """
    ascii_map = (meta.get("map") or "").strip()
    if ascii_map:
        return (
            # Shut by default (JL 260801: "默认的话我们还是把它合起来吧，每次
            # 打开的话非常难看"). The map is orientation, not the first thing to
            # read: open, it pushes the page roster off the first screen.
            '<details class="board-map board-map-ascii">'
            f'<summary>{MAP_HEAD}</summary>'
            f'<div class="board-map-body">{body(ascii_map, fold_code=False)}</div>'
            '</details>'
        )

    declared = (meta.get("board_map") or "").strip()
    if declared.startswith(("https://", "http://")):
        # A static host cannot proxy `/_excalidraw`. A Board may therefore
        # declare the share URL of its relationship canvas explicitly; it is
        # still only a view of the map, never a second page registry.
        url = declared
        return (
            '<section class="board-map" aria-labelledby="board-map-title">'
            + MAP_HEAD +
            f'<iframe title="{esc(meta["title"])} Board Map" src="{esc(url)}" '
            'referrerpolicy="no-referrer"></iframe>'
            '<div class="board-map-foot"><span>Shared canvas · pan and zoom in the full view</span>'
            f'<a class="fp" href="{esc(url)}" target="_blank" rel="noopener">↗ Open canvas</a>'
            '</div></section>'
        )

    host = (meta.get("excalidraw") or "").strip().rstrip("/")
    board_dir = Path(meta.get("dir") or "")
    if not host or not board_dir.is_dir():
        return ""
    scene = board_dir / "board.excalidraw"
    if not scene.is_file():
        scene = board_dir / "fig" / "board.excalidraw"  # legacy Boards
    if not scene.is_file():
        return ""
    root = server_root(board_dir)
    if root is None:
        return ""
    try:
        rel = scene.relative_to(root).as_posix()
    except ValueError:
        return ""
    url = f"{host}/?board={quote(rel, safe='/')}"
    edit = f"{url}&edit=1"
    return (
        '<section class="board-map" aria-labelledby="board-map-title">'
        + MAP_HEAD +
        f'<iframe title="{esc(meta["title"])} Board Map" src="{esc(url)}" '
        'referrerpolicy="no-referrer"></iframe>'
        '<div class="board-map-foot"><span>Read-only here · pan and zoom freely</span>'
        f'<a class="fp" href="{esc(edit)}" target="_blank" rel="noopener">✏️ Edit map</a>'
        f'<a class="fp" href="{esc(url)}" target="_blank" rel="noopener">↗ Full map</a>'
        '</div></section>'
    )


def pages_only_index(meta):
    """Whether this Board opts into the deliberately quiet Pages-only index."""
    return (meta.get("index_view") or "").strip().lower() == "pages"


def group_canvas(meta, group, members):
    """The live linked drawing for one generated Group page."""
    host = (meta.get("excalidraw") or "").strip().rstrip("/")
    board_dir = Path(meta.get("dir") or "")
    if not host or not board_dir.is_dir() or not members:
        return ""
    # The group folder is the members' shared FIRST path segment, not their
    # files' shared parent: a folded page (`<name>/<name>.md`, JL 260815)
    # gives every member a different parent, which silently blanked every
    # group canvas until the 260815 restructure surfaced it.
    heads = {Path(member.get("file") or "").parts[0]
             for member in members if member.get("file")}
    if len(heads) != 1:
        return ""
    head = heads.pop()
    if not (board_dir / head).is_dir():
        return ""
    scene = board_dir / head / "draw" / "group.excalidraw"
    if not scene.is_file():
        return ""
    root = server_root(board_dir)
    if root is None:
        return ""
    try:
        rel = scene.relative_to(root).as_posix()
    except ValueError:
        return ""
    # NO INLINE CANVAS ON STAGE (JL 260815: "I don't want the draw in here").
    # The same ruling that keeps Excalidraw out of `## Outline` applies one level
    # up: a group page's body stays prose, and the composed drawing opens in the
    # Draw split. What the page emits is only the OWNER ADDRESS, invisible, so
    # the plugin can derive the scene without the build and the client keeping
    # two copies of the path logic.
    return (f'<div class="group-draw-owner" hidden data-scene="{esc(rel)}" '
            f'data-label="{esc(group)}"></div>')


RELATED_MAX_DEPTH = 4      # how deep the walk descends
RELATED_MAX_ENTRIES = 300  # per folder, so one huge directory cannot flood the page
RELATED_SKIP = {"__pycache__", ".git", ".DS_Store", "node_modules",
                ".haipipe-board", ".pytest_cache", ".ruff_cache", ".venv"}


def related_folders(meta, base=None):
    """The RELATED FOLDERS fold (QB2, JL 260731/260801).

    A plain DIRECTORY BROWSER, not a reader: "what I want is the pure folder
    that can be opened, don't need to put the content here. It is just like the
    folder hosted in the browser, I can open and navigate." The first version
    embedded each declared file's text, which answered a question JL had not
    asked and buried the structure it was supposed to show.

    So this walks the real folder and renders its tree: a subfolder is a nested
    <details> that opens to its own children, a file is a row with its size.
    The walk happens at BUILD and the tree ships collapsed, so navigating costs
    no request and works with scripts stripped and on a static host (QE3's Law).

    The `## Related Folders` grammar in board.md is one line per root:
        @ <folder path, board-relative> | <label>
    QA0 owns which roots are listed. Everything below a root is discovered, not
    declared, because the point is to show what is actually there.
    """
    text = (meta.get("related") or "").strip()
    if not text:
        return ""
    board_dir = Path(meta.get("dir") or "")
    root = server_root(board_dir)
    # A file row links to the real file (JL 260801: "I cannot click the files
    # if I want?"). The href is relative to the BOARD SOURCE folder, which is
    # the same convention every authored relative path on a board uses:
    # `tree_reroot()` re-sites it for `board/`, so this must NOT pre-apply the
    # output offset or the path ends up one level too high.
    html_dir = Path(base) if base else board_dir

    intro, roots = [], []
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("@ "):
            path, _, label = s[2:].partition("|")
            roots.append({"path": path.strip(), "label": label.strip() or path.strip()})
        elif s.startswith("- "):
            continue  # legacy per-file lines: the whole folder is browsable now
        elif s and not roots:
            intro.append(s)

    def size_of(n):
        return f"{n / 1024:.0f} KB" if n >= 1024 else f"{n} B"

    def walk(d, depth):
        """One folder's children as HTML: subfolders first, then files."""
        if depth > RELATED_MAX_DEPTH:
            return '<div class="rf-more">deeper levels not shown</div>'
        try:
            kids = sorted(d.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except OSError:
            return '<div class="rf-miss">unreadable</div>'
        kids = [k for k in kids if k.name not in RELATED_SKIP
                and not k.name.endswith(".pyc")]
        clipped = len(kids) > RELATED_MAX_ENTRIES
        rows = []
        for k in kids[:RELATED_MAX_ENTRIES]:
            if k.is_dir():
                try:
                    n = len([x for x in k.iterdir() if x.name not in RELATED_SKIP])
                except OSError:
                    n = 0
                rows.append(
                    f'<details class="rf-dir"><summary><span class="rf-n">{esc(k.name)}/</span>'
                    f'<span class="rf-c">{n}</span></summary>'
                    f'<div class="rf-kids">{walk(k, depth + 1)}</div></details>')
            else:
                try:
                    sz = size_of(k.stat().st_size)
                except OSError:
                    sz = ""
                try:
                    href = quote(os.path.relpath(k, html_dir).replace(os.sep, "/"))
                except (OSError, ValueError):
                    href = ""
                if href:
                    rows.append(f'<a class="rf-f" href="{esc(href)}" target="_blank" '
                                f'rel="noopener"><span class="rf-n">{esc(k.name)}</span>'
                                f'<span class="rf-c">{esc(sz)}</span></a>')
                else:
                    rows.append(f'<div class="rf-f"><span class="rf-n">{esc(k.name)}</span>'
                                f'<span class="rf-c">{esc(sz)}</span></div>')
        if clipped:
            rows.append(f'<div class="rf-more">+{len(kids) - RELATED_MAX_ENTRIES} more</div>')
        return "".join(rows) or '<div class="rf-more">empty</div>'

    blocks = []
    for fo in roots:
        try:
            base = (board_dir / fo["path"]).resolve()
        except OSError:
            base = None
        if base is None or not base.is_dir():
            blocks.append('<div class="rf-miss">\u26d4 <code>'
                          f'{esc(fo["path"])}</code> \u2014 folder not found</div>')
            continue
        if root is not None and root not in (base, *base.parents):
            blocks.append('<div class="rf-miss">\u26d4 <code>'
                          f'{esc(fo["path"])}</code> \u2014 outside the repo root</div>')
            continue
        try:
            shown = base.relative_to(root).as_posix() if root else fo["path"]
        except ValueError:
            shown = fo["path"]
        # The full path used to sit in the header as raw text (JL 260801: "这些
        # 路径 URL 能不能别露出来 ... 做成 clickable 的"). A repo path is long,
        # it is not what a reader is scanning for, and printed in full it makes
        # every folder row look the same. It is now one ↗ that OPENS the folder
        # — the server answers a directory with a real listing — and the path
        # itself survives as the hover title for anyone who wants it.
        try:
            fhref = quote(os.path.relpath(base, board_dir).replace(os.sep, "/")) + "/"
        except (OSError, ValueError):
            fhref = ""
        open_link = (f'<a class="rf-open" href="{esc(fhref)}" target="_blank" rel="noopener" '
                     f'title="{esc(shown)}" aria-label="Open {esc(shown)}">↗</a>'
                     ) if fhref else ""
        blocks.append(
            f'<details class="rf-folder"><summary title="{esc(shown)}">'
            f'{inline(fo["label"])}{open_link}</summary>'
            f'<div class="rf-files">{walk(base, 1)}</div></details>')

    intro_html = f'<p class="rf-intro">{inline(" ".join(intro))}</p>' if intro else ""
    return ('<details class="board-status related-folders">'
            '<summary>RELATED FOLDERS \u00b7 open a folder and navigate it</summary>'
            f'{intro_html}{"".join(blocks)}</details>')


def board_status(qs):
    """The SECTION MATRIX (QB2, JL 260731: "a dashboard to show the status of
    the board. Each row is a page, each column is a subsection").

    One row per page, one column per section, every cell computed at build
    from the same parses the pages themselves render from, so the matrix is
    derived and can never disagree with a page. Cells link: click one and the
    page opens at that section (board.js). The 📚 cell reports face-diagram
    coverage (divisions · with-diagram), which is how the QB4c retrofit is
    watched."""
    body_rows, cur = [], None
    for q in qs:
        if q.get("kind") == "doc":
            continue
        if q.get("group") and q["group"] != cur:
            cur = q["group"]
            body_rows.append(f'<tr class="bsg"><td colspan="8">{inline(cur)}</td></tr>')
        d = q["sec"]
        tok, _, _ = stinfo(q["state"])
        pid = q["id"]

        def cell(key, state, txt):
            return (f'<td class="bs-{state}">'
                    f'<a href="#{pid}" data-k="{key}">{txt}</a></td>')

        cells = []
        cells.append(cell("opening", "ok" if sec(d, "Opening").strip() else "no",
                          "✓" if sec(d, "Opening").strip() else "—"))
        page_src = (Path(bd.BASE or ".") / q["file"]
                    if q.get("file") else None)
        has_plan = has_outline_plan(page_src)
        dtxt = "▤" if has_plan else ""
        cells.append(cell("outline", "ok" if dtxt else "no", dtxt or "—"))
        divs = [(h, b) for h, b in parse_content_sections(sec(d, "Content")) if h]
        faced = sum(1 for _h, b in divs if b.lstrip().startswith("```"))
        if divs:
            cells.append(cell("content", "ok" if faced == len(divs) else "warn",
                              f"{len(divs)}÷·{faced}🖼"))
        elif sec(d, "Content").strip():
            cells.append(cell("content", "ok", "flat"))
        else:
            cells.append(cell("content", "no", "—"))
        aims = sec(d, "Done when")
        state = sec(d, "Now")
        progress = aim_progress(aims, state)
        if progress["total"]:
            cells.append(cell("items", "ok" if progress["closed"] == progress["total"] else "warn",
                              f'{progress["closed"]}/{progress["total"]}'))
        else:
            cells.append(cell("items", "no", "—"))
        owed = sum(len(re.findall(r"(?m)^\s*[-*] \[ \]", b))
                   for h, b in parse_content_sections(state)
                   if h and "Decision Now" in h)
        if owed:
            cells.append(cell("now", "dn", f"DN·{owed}"))
        elif state.strip():
            dated = len(re.findall(r"(?m)^- ?\d{6}", state))
            cells.append(cell("now", "ok", f"e{dated}" if dated else "✓"))
        else:
            cells.append(cell("now", "no", "—"))
        ftxt = sec(d, "Files")
        nf = len(re.findall(r"(?m)^- ", ftxt))
        ngrp = len([h for h, _ in parse_content_sections(ftxt) if h])
        ft = (f"{nf}·{ngrp}g" if ngrp else str(nf)) if nf else "—"
        cells.append(cell("files", "ok" if nf else "no", ft))
        nlog = len(re.findall(r"(?m)^\d{6}", sec(d, "Log")))
        cells.append(cell("folds", "ok" if nlog else "no",
                          f"L{nlog}" if nlog else "—"))

        body_rows.append(
            f'<tr><th class="bsp"><a href="#{pid}">{tok} {esc(pid)}</a></th>'
            + "".join(cells) + "</tr>")

    head = ("<tr><th>page</th><th>🧭</th><th>▤</th><th>📚</th>"
            "<th>🎯</th><th>📍</th><th>📎</th><th>🗄</th></tr>")
    legend = ('🧭 <code>▤</code> current plan table &nbsp;·&nbsp; '
              '📚 <code>n÷·m🖼</code> divisions · with face diagram &nbsp;·&nbsp; '
              '🎯 <code>met/total</code> aims &nbsp;·&nbsp; '
              '📍 <code>DN·k</code> Decision Now ticks owed, <code>e</code> dated entries '
              '&nbsp;·&nbsp; 📎 <code>n·gg</code> files · groups &nbsp;·&nbsp; '
              '🗄 <code>Ln</code> Log lines &nbsp;·&nbsp; a cell opens its section')
    return ('<details class="board-status">'
            '<summary>SECTION MATRIX · every page × every section, computed at build</summary>'
            f'<div class="bstat-scroll"><table class="bstat"><thead>{head}</thead>'
            f'<tbody>{"".join(body_rows)}</tbody></table></div>'
            f'<p class="bstat-legend">{legend}</p></details>')


def _gt_link(group, group_href):
    """A group heading links to its own page when the packaging has one."""
    h = group_href(bd.group_token(group))
    return f'<a href="{h}">{inline(group)}</a>' if h else inline(group)


# ── desk sub-blocks (PaperSkillBoard QA1 Decision Now, JL 260831) ──────────
# A paper board keeps ONE group per desk (`B<x>-<desk>`) holding its section
# pages (S<D> token = main, A<D> token = appendix) and its rounds (RD token)
# together; that is the layout law of haipipe-paper-workflow §Group mapping.
# Sixteen rows under one heading hid the paper's shape (JL 260831, reading the
# MISQ index), so the index and the Pages sidebar cut a desk group into
# sub-blocks by the page-id TOKEN instead of renaming folders. Only a
# `dialect: paper` board, only a group whose pages span two or more token
# families; every other board renders exactly as before.
def _id_token(qid):
    m = re.match(r"[A-Za-z]+", qid or "")
    return m.group(0) if m else (qid or "")


def _token_label(tok):
    u = tok.upper()
    if u == "RD":
        return "rounds"
    if u == "SA":                      # Section-Appendix (JL 260831)
        return "appendix"
    if u == "STORY":                   # journey pages incl. the narrative (JL 260831)
        return "story"
    if u.startswith("S"):
        return "main sections"
    if u.startswith("A"):              # grandfathered A<D> boards
        return "appendix"
    return tok


def desk_subblocks(meta, qs):
    """{group: True} for every group of a paper board whose pages span two
    or more id-token families; the caller emits a sub-heading where the
    token changes. Empty for any other board, so nothing else moves."""
    dialect = ((meta or {}).get("dialect") or "").split("#", 1)[0].strip()
    if dialect != "paper":
        return {}
    fam = {}
    for q in qs:
        if q.get("kind") == "doc" or not q.get("group"):
            continue
        fam.setdefault(q["group"], set()).add(_id_token(q["id"]))
    return {g: True for g, s in fam.items() if len(s) >= 2}


def _gi_body(gi):
    """The group intro's expandable body, shared by the index listing and the
    group's own page: prose lines join with <br> (keeping the author's line
    breaks), and a ``` fence becomes a <pre class="gidia"> ascii figure."""
    parts, prose, fence, inf = [], [], [], False
    for x in gi[1:]:
        s = x.strip()
        if s.startswith("```"):
            if inf:
                parts.append('<pre class="gidia">'
                             + bd.link_faces(esc(chr(10).join(fence)))
                             + '</pre>')
                fence, inf = [], False
            else:
                if prose:
                    parts.append("<br>".join(inline(p) for p in prose)); prose = []
                inf = True
            continue
        if inf:
            fence.append(x)          # 原样，保对齐
        elif s:
            prose.append(s)
    if prose:
        parts.append("<br>".join(inline(p) for p in prose))
    return "".join(parts)


def index_rows(meta, qs, href_for=None, group_href=None):
    """The index listing: group headings, group intros (prose AND their ascii
    figures), and one row per page.

    ONE implementation reused by the generated Index, group pages, sidebar,
    and the legacy single-Markdown renderer. Hand-rewriting this for the board/
    tree dropped every `.gi` / `.gib` / `.gidia` block, so the group intros and the
    lane figures vanished and their ascii stopped being ascii (JL 260731, the
    third time this file's own "never two implementations" law bit its author).
    `href_for` maps a page to its link and `group_href` a group token to its
    own; the single file passes fragments, the tree passes paths.
    """
    href_for = href_for or (lambda q: "#" + q["id"])
    group_href = group_href or (lambda tok: None)

    def st(q):
        return stinfo(q["state"])

    def frac_done(q):
        progress = aim_progress(sec(q.get("sec", {}), "Done when"),
                                sec(q.get("sec", {}), "Now"))
        return (progress["closed"] / progress["total"]
                if progress["total"] else 0.0)

    ginfo = meta.get("groups") or {}
    dsubs = desk_subblocks(meta, qs)
    rows, cur, cur_tok = [], None, None
    for q in qs:
        if q.get("group") and q["group"] != cur:
            cur = q["group"]
            cur_tok = None
            # A group is a place you can travel to (JL 260730): the canvas draws
            # groups, so a group heading needs an anchor of its own. It is NOT a
            # page — `#group-QA` scrolls the index, it does not open a card — so
            # the id stays in its own namespace and never collides with a page.
            rows.append(f'<div class="grp" id="group-{esc(bd.group_token(cur))}"'
                        f' data-g="{esc(cur)}">'
                        f'<span class="gt">{_gt_link(cur, group_href)}</span></div>')
            # Group intro (QC2): one sentence always visible; if more lines follow,
            # they open on click via a native <details>. No script involved, so the
            # strip-scripts invariant is untouched.
            gi = ginfo.get(cur)
            if gi:
                summary = inline(gi[0].strip())
                # 展开的 body：散文按行 <br> 接（保作者断行），碰到 ``` 就当 ascii 图铺成 <pre>。
                gib = _gi_body(gi)
                if gib:
                    rows.append(f'<details class="gi"><summary>{summary}</summary>'
                                f'<div class="gib">{gib}</div></details>')
                else:
                    rows.append(f'<div class="gi one">{summary}</div>')
        if q.get("kind") == "doc":
            rows.append(
                f'<a class="ir doc" href="{href_for(q)}">'
                f'<span class="s">📄</span><span class="i">{esc(q["id"])}</span>'
                f'<span class="t">{nav_inline(q["title"])}</span>'
                f'<span class="w"></span></a>')
            continue
        if dsubs.get(cur):
            tok = _id_token(q["id"])
            if tok != cur_tok:
                cur_tok = tok
                rows.append(f'<div class="dsub" data-sub="{esc(tok)}">'
                            f'<span class="st">{esc(tok)}</span>'
                            f'<span class="sl">{esc(_token_label(tok))}</span></div>')
        # 完成度上色：一条没做 = 白，越接近做完越绿（绿色叠加的透明度 = 完成比例）
        fr = frac_done(q)
        pct = round(fr * 100)
        fill = (f' style="--fill:{fr:.3f}"') if fr > 0 else ""
        df = f' data-f="{esc(q["file"])}"' if q.get("file") else ""
        rows.append(
            f'<a class="ir {st(q)[1]}" href="{href_for(q)}"{fill}{df} title="{pct}% done">'
            f'<span class="s">{st(q)[0]}</span><span class="i">{q["id"]}</span>'
            f'<span class="t">{nav_inline(q["title"])}</span>'
            + f'<span class="w">{"🧠 JL" if q["owner"]=="JL" else ("🔧 "+q["owner"] if q["owner"] else "")}</span></a>')
    return rows


def sidebar_rows(qs, href_for=None, group_href=None, meta=None):
    """The sidebar's rows: group links, page links, and each page's section
    outline. ONE implementation for the canonical site and legacy renderer.
    `meta` carries the board dialect for the desk sub-blocks; without it the
    sidebar renders flat groups, as every non-paper board does anyway."""
    href_for = href_for or (lambda q: "#" + q["id"])
    group_href = group_href or (lambda tok: "#group-" + tok)
    dsubs = desk_subblocks(meta, qs)

    def st(q):
        return stinfo(q["state"])

    sb, sbcur, sbtok = [], None, None
    for q in qs:
        if q.get("group") and q["group"] != sbcur:
            sbcur = q["group"]
            sbtok = None
            sb.append(f'<a class="sb-g" href="{group_href(bd.group_token(sbcur))}">'
                      f'{nav_inline(sbcur)}</a>')
        if dsubs.get(sbcur) and q.get("kind") != "doc":
            tok = _id_token(q["id"])
            if tok != sbtok:
                sbtok = tok
                sb.append(f'<div class="sb-sub" data-sub="{esc(tok)}">'
                          f'<span class="st">{esc(tok)}</span> '
                          f'<span class="sl">{esc(_token_label(tok))}</span></div>')
        chev = ('' if q.get("kind") == "doc"
                else '<span class="sb-x" title="sections">▸</span>')
        # `data-page` is what the sidebar matches the open page against. The href
        # cannot serve: it is `#QB5c` in the one-file board and
        # `QB/QB5c-editing.html` in the tree, and mark() used to compare it to
        # `location.hash`, which a tree page does not have. So no row was ever
        # marked and no outline ever opened there (JL 260801). The id is the
        # same in both packagings, and `.sb-out` already keys on it.
        sb.append(f'<a class="sb-p" data-page="{esc(q["id"])}" href="{href_for(q)}">'
                  f'<span class="s">{"📄" if q.get("kind") == "doc" else st(q)[0]}</span>'
                  f'<span class="i">{esc(q["id"])}</span>'
                  f'<span class="t">{nav_inline(q["title"])}</span>{chev}</a>')
        # The per-page outline (QB2a, JL 260731): the Structure rows again,
        # so the sidebar and the Opening drawer can never disagree. Hidden until
        # this page is the open one — only ONE page's sections show at a time.
        if q.get("kind") != "doc":
            out = []
            # 同一份 Content 切分：抬走的那块（legacy `### Stage Record`）在这里
            # 也得抬走，不然 sidebar 比正文多一节，而 `data-div` 是按顺序编号的，
            # 于是那一页每一个 division 链接都错开一格（JL 260801 统一命名时发现）。
            _, csecs = split_stage_record(
                q.get("kind"), parse_content_sections(sec(q["sec"], "Content")))
            page_src = (Path(bd.BASE or ".") / q["file"]
                        if q.get("file") else None)
            for key, label, val, subs in structure_rows(
                    q["sec"], csecs, has_outline_plan(page_src),
                    q.get("page_type", "")):
                out.append(f'<a class="sb-s" data-k="{key}" href="{href_for(q)}">'
                           f'<span class="t">{esc(label)}</span>'
                           f'<span class="m">{esc(val)}</span></a>')
                for j, (disp, t) in enumerate(subs):
                    # Content divisions are found by ORDER (data-div, the same
                    # Cn order the chat addresses use); other subsections by
                    # their heading text (data-t → the rendered .sh).
                    how = (f'data-div="{j}"' if key == "content"
                           else f'data-t="{esc(t)}"')
                    out.append(f'<a class="sb-ss" data-k="{key}" {how} '
                               f'href="{href_for(q)}">{nav_inline(disp)}</a>')
            sb.append(f'<div class="sb-out" data-out="{esc(q["id"])}">'
                      + "".join(out) + '</div>')
    return sb


def render(meta, qs):
    # Questions and S families share one page grammar, but their progress answers
    # different things: rulings settle; lifecycle pages pass human CHECK gates.
    # A skill page is a synced MIRROR of a shipped unit, not a decision, so it
    # never enters the settled count (JL 260731). That contradiction was the
    # old `Q-Skill` name: it was counted as a question and declared not to be one.
    # `meeting` joined this list on 260806. Two contracts already said it should
    # be here, `haipipe-page` ("mirror and Meeting pages are NEVER counted
    # in a board's settled totals") and `-for-meeting` ("NEVER counted in settled
    # totals"), and the code counted it anyway, so every board holding a meeting
    # reported a denominator one too large. A meeting page decides nothing: what
    # was ruled in the room is routed to the page that owns it, and that page
    # carries the count.
    task_board = meta.get("board_kind") == "task-block"
    qonly = ([q for q in qs if q.get("kind") == "task"] if task_board else
             [q for q in qs
              if q.get("kind") not in ("doc", "stage", "skill", "agent", "meeting", "task")])
    sonly = [q for q in qs if q.get("kind") == "stage"]
    done = sum(1 for q in qonly if q["state"].startswith("✅"))
    nq = len(qonly)
    sfamilies = [
        ("open", "Open"),
        ("seed", "Seed"),
        ("work", "Work"),
        ("venue", "Venue"),
        ("literature", "Literature"),
        ("value", "Value"),
        ("display", "Display"),
        ("main", "Main"),
        ("appendix", "Appendix"),
        ("submission", "Submission"),
        ("round", "Round"),
        ("label", "Label"),
        ("stage", "legacy stages"),
    ]
    bar = "█" * round(done / nq * 14) + "░" * (14 - round(done / nq * 14)) if nq else ""
    n = len(qs)

    def st(q):
        return stinfo(q["state"])

    def frac_done(q):
        """Completion 0..1 from Aim State; settled/held pages stay full."""
        s = q["state"]
        if s.startswith("✅") or s.startswith("⏸"):
            return 1.0
        progress = aim_progress(sec(q["sec"], "Done when"), sec(q["sec"], "Now"))
        return (progress["closed"] / progress["total"]
                if progress["total"] else 0.0)

    rows = index_rows(meta, qs)
    idx = "\n".join(rows)

    # Pages sidebar (JL 260731): the .idx listing compressed to a fixed sidebar,
    # Index → group → page, so a reader can jump from anywhere. It lives
    # OUTSIDE .wrap, so the :target show/hide rules never touch it; a group
    # link re-targets #group-… which also brings the index back on stage.
    sb = sidebar_rows(qs, meta=meta)
    # The Index row unfolds too (QB2a, JL 260731: "what should be the index's
    # section content? Please add them as well"): its rows are the Index's own
    # components in on-page order, each present only when the board has it.
    minimal_index = pages_only_index(meta)
    bmap = "" if minimal_index else board_map(meta)
    rf = "" if minimal_index else related_folders(meta)
    ix = []

    def ixrow(key, label, mtxt=""):
        m = f'<span class="m">{esc(mtxt)}</span>' if mtxt else ""
        ix.append(f'<a class="sb-s" data-k="{key}" href="#top">'
                  f'<span class="t">{label}</span>{m}</a>')

    if bmap:
        ixrow("map", "🗺 Board Map")
    if rf:
        ixrow("related", "🗂 Related Folders")
    ixrow("pages", "📄 All Tasks" if task_board else "📄 All Pages", str(n))
    if not minimal_index:
        ixrow("status", "🩺 Section Matrix",
              f"{len([q for q in qs if q.get('kind') != 'doc'])} × 7")
        ixrow("activity", "📈 Activity")

    sidebar = ('<button type="button" id="sbtoggle" class="sbtoggle" '
               'aria-label="Toggle the pages sidebar">☰</button>'
               '<div class="sbrz" title="Drag to resize"></div><nav class="sidebar" id="sidebar" aria-label="Pages">'
               '<a class="sb-top" data-page="top" href="#top">🗂 Index'
               '<span class="sb-x" title="sections">▸</span></a>'
               f'<div class="sb-out" data-out="top">{"".join(ix)}</div>'
               + "".join(sb) + '</nav>')

    cards = []
    for i, q in enumerate(qs):
        prv, nxt = (qs[i - 1] if i else None), (qs[i + 1] if i + 1 < n else None)
        cards.append(render_doc_slide(q, prv, nxt) if q.get("kind") == "doc"
                     else render_question(q, prv, nxt))

    # The three ctx disclosures (🦴 Topic · 🔄 Pipeline · 🧭 Board-Structure)
    # left the Index on JL's 260731 ruling ("I want to just remove this"): the
    # spine, the Board Map, and the SECTION MATRIX already orient a reader, and
    # board.md keeps the sections as source-only documentation. QB2 records it.

    stagebits = []
    for family, label in sfamilies:
        pages = [q for q in sonly if (q.get("family") or "stage") == family]
        if pages:
            gated = sum(1 for q in pages if q["state"].startswith("✅"))
            stagebits.append(f"{gated}/{len(pages)} {label}")
    stagebar = (" · " + " · ".join(stagebits)) if stagebits else ""
    heading = ('<div class="board-heading"><span class="board-mark" aria-hidden="true">'
               + MARK_SVG + f'</span><h1 class="h1">{esc(meta["title"])}</h1></div>')
    pages = (f'<h3 class="sec" id="qlist">{"ALL TASKS" if task_board else "ALL PAGES"}'
             '<span class="hint">click a row → open it · <a href="#all">show all</a></span></h3>'
             f'<div class="idx">{idx}</div>')
    progress_label = "tasks closed" if task_board else "questions settled"
    overview = (heading + pages if minimal_index else
                heading + f'<div class="spine"><p><b>🦴 Spine</b> {inline(meta["spine"])}</p>'
                f'<p><b>🏁 Close when</b> {inline(meta["close"])}</p></div>'
                f'<p class="bar">{bar}  {done}/{nq} {progress_label}{stagebar}</p>'
                + bmap + rf + board_status(qs) + pages)
    return TPL.format(title=esc(meta["title"]), overview=overview,
                      activity="" if minimal_index else ACTIVITY_HTML,
                      index=idx,
                      sidebar=sidebar,
                      cards="\n".join(cards), js=JS, css=CSS,
                      assets_stamp=ASSETS_STAMP, css_stamp=CSS_STAMP, js_stamp=JS_STAMP,
                      mark=MARK_SVG, favicon=MARK_FAVICON,
                      # chip panels last: they are top-layer, so DOM position
                      # is free, and out here they are never inside a <summary>
                      popcards="\n".join(bd.CARDS),
                      boarddir=esc(meta.get("dir", "")),
                      bsession=esc(meta.get("session", "")))


# ── page assets (QB4, JL 260724: build.py was one 2,500-line file) ─────────
# The page's JS and CSS live in assets/ as REAL .js/.css files: editable,
# lintable, and node-checkable. A Board folder build assembles each family once
# into board/_assets/, and every generated page links that shared copy. The
# legacy single-Markdown build still inlines them into its one output file.
HERE = Path(__file__).resolve().parent.parent
# Assembled from assets/js/** and assets/css/** in sorted path order; see
# src/assets.py for why the parts exist and why the order is load-bearing.
from . import assets as _assets            # noqa: E402
_JS_PROBLEMS = _assets.verify()
if _JS_PROBLEMS:
    raise RuntimeError("browser assets are broken:\n  " + "\n  ".join(_JS_PROBLEMS))
JS = "\n<script>\n" + _assets.js().rstrip("\n") + "\n</script>\n"
CSS = _assets.css().rstrip("\n")
# The live refresh swaps div.wrap and NEVER re-runs scripts, so a long-lived tab
# keeps the JS/CSS it was opened with. This stamp lets tick() detect that the
# assets changed under it and do the one full reload that heals a stale tab
# (JL 260731: dead ➕ buttons after a day of shipping under an open tab).
# ONE stamp for both files meant a CSS-only change looked like a JS change, and
# a JS change is the only thing that can force a full reload. Stamp them apart
# so the page can take new CSS by swapping a <link> and never reload for it
# (JL 260801: "我一旦改了之后，我想看到这个变化是 immediate 的变化" and
# "只更新这个配置的一小部分").
CSS_STAMP = hashlib.md5(CSS.encode("utf-8")).hexdigest()[:12]
JS_STAMP = hashlib.md5(JS.encode("utf-8")).hexdigest()[:12]
ASSETS_STAMP = hashlib.md5((JS + CSS).encode("utf-8")).hexdigest()[:12]
MARK_SVG = (HERE / "assets" / "board-mark.svg").read_text(encoding="utf-8").strip()
MARK_FAVICON = ("data:image/svg+xml;base64,"
                + base64.b64encode(MARK_SVG.encode("utf-8")).decode("ascii"))

ACTIVITY_HTML = """<section class="activity" id="activity" aria-labelledby="activity-title">
<div class="act-head">
  <div><span class="act-kicker">ACTIVITY</span><h2 id="activity-title">When, then where</h2></div>
  <span class="act-status" id="activity-status">waiting for the board server</span>
</div>
<p class="act-note">One update is one dated line in one page's <code>## Log</code>. The count is read from the Markdown itself, so it sees every change any tool made, not only the ones a browser watched.</p>
<div id="activity-body"><p class="act-empty">Open this board through <code>serve.py</code> to count updates. The dashboard is an enhancement; the board remains complete without it.</p></div>
</section>"""

TPL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="board-assets" content="{assets_stamp}">
<meta name="board-css" content="{css_stamp}">
<meta name="board-js" content="{js_stamp}">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="{favicon}">
<style>
{css}
</style></head><body class="single" data-board="{boarddir}">{sidebar}<div class="wrap" id="top" data-bsession="{bsession}">

{overview}

<span id="all"></span>
{cards}

{activity}

<p class="foot">Content comes from <code>board.md</code> (board-level), <code>QX-xxx.md</code>
(one per ruling), and named lifecycle pages such as <code>S-Seed-0-xxx.md</code>,
<code>S-Display-0-xxx.md</code>, <code>S-Main-3-xxx.md</code>, or
<code>S-Appendix-A-xxx.md</code>. Edit those, then rebuild:
<code>python3 build.py</code>.<br>Every page is real HTML — the page reads fine
with JavaScript off; the script only adds commenting.</p>
</div><div id="popcards">{popcards}</div>{js}</body></html>
"""

_CJK = re.compile(r"[一-鿿]")


def scrub_cjk_comments(txt):
    """Drop CSS/JS comments that contain CJK from the EMITTED page (the source
    keeps its comments for developers; the output stays fully English — JL 260724).
    Scoped to <style>/<script> blocks ONLY: body prose may legally contain `/*`
    (QD3's `GET /_board/asset/*` glob), and a page-wide pass once swallowed five
    slides between that glob and the next `*/` as soon as CJK landed in between
    (260724, caught by build.py's no-JS invariant). Inside a block, only comments
    are touched: /*…*/ spans, and //-to-EOL tails whose line prefix has balanced
    quotes (so a // inside a string is never mistaken for a comment)."""
    def scrub(seg):
        seg = re.sub(r"/\*.*?\*/", lambda m: "" if _CJK.search(m.group(0)) else m.group(0),
                     seg, flags=re.S)
        def line(ln):
            i = ln.find("//")
            while i != -1:
                pre = ln[:i]
                if pre.count("'") % 2 == 0 and pre.count('"') % 2 == 0 and pre.count("`") % 2 == 0:
                    return pre.rstrip() if _CJK.search(ln[i:]) else ln
                i = ln.find("//", i + 1)
            return ln
        return "\n".join(line(l) if _CJK.search(l) else l for l in seg.split("\n"))
    return re.sub(r"(?s)(<(style|script)\b[^>]*>)(.*?)(</\2>)",
                  lambda m: m.group(1) + scrub(m.group(3)) + m.group(4), txt)


def to_json(meta, qs, warn):
    """`build.py <dir> --json` — the parser as a service (QE3: one grammar,
    two render paths). Emits the same data the HTML is built from, plus the
    derived numbers the index shows, so JSON and HTML cannot disagree."""
    def q_json(q):
        progress = aim_progress(sec(q["sec"], "Done when"), sec(q["sec"], "Now"))
        tok, cls, lab = stinfo(q["state"])
        return dict(id=q["id"], title=q["title"], group=q["group"], file=q["file"],
                    state=q["state"], state_token=tok, state_label=lab,
                    owner=q["owner"], method=q["method"], session=q["session"],
                    kind=q.get("kind", ""), family=q.get("family", ""),
                    requires=q.get("requires", ""),
                    style_from=q.get("style_from", ""),
                    provides=q.get("provides", ""),
                    contract_source_hash=q.get("contract_source_hash", ""),
                    files=q.get("files", []),
                    done=progress["closed"], total=progress["total"],
                    aims={k: progress[k] for k in
                          ("mode", "met", "active", "waiting", "open", "hold")},
                    sections={k: v for k, v in q["sec"].items()})
    return json.dumps({"meta": meta, "questions": [q_json(q) for q in qs],
                       "warnings": warn}, ensure_ascii=False, indent=1)


# ── the board/ tree (QC9, JL 260731) ──────────────────────────────────────
# One file per page and one per group, sharing ONE copy of the css and js,
# so a reader downloads ~34 KB instead of the whole board, a page has a real
# URL, and a write to page C rewrites page C's file alone.
#
# Same parser, same renderers: the tree reuses `render()`'s parts rather than
# maintaining a second implementation. For a Board folder this is now the only
# generated packaging. A single Markdown target may still render one file.
TREE_TPL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="board-assets" content="{assets_stamp}">
<meta name="board-css" content="{css_stamp}">
<meta name="board-js" content="{js_stamp}">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="{favicon}">
<link rel="stylesheet" href="{root}_assets/board.css?v={css_stamp}">
</head><body class="single split" data-board="{boarddir}" data-board-root="{root}" data-xcal="{xcal}">{sidebar}<div class="wrap" id="top" data-bsession="{bsession}">
<nav class="sitebar" aria-label="Breadcrumb"><a href="/boards">🏠 Boards</a><span class="sb-sep">›</span><a href="{root}index.html">🗂 Index</a>{crumb}</nav>
{body}
</div><div id="popcards">{popcards}</div>
<script src="{root}_assets/board.js?v={js_stamp}"></script></body></html>
"""





def tree_href_map(qs):
    """`#QA1` -> `QA/QA1-slug.html`, and `#group-QA` -> `QA.html`.

    The Board Map, the Section Matrix and the Activity panel are all REUSED
    from `render()` rather than rewritten (the index-rows lesson, JL 260731),
    but every link they emit is a fragment into a one-document board. In the
    tree those fragments point at nothing, so their hrefs are rewritten here
    and nowhere else.
    """
    m = {}
    for q in qs:
        gt = bd.group_token(q.get("group") or "") or "_ungrouped"
        m["#" + q["id"]] = f'{gt}/{tree_page_name(q)}'
    for q in qs:
        g = q.get("group")
        if g:
            tok = bd.group_token(g)
            m["#group-" + tok] = f"{tok}.html"
    return m


def tree_relink(html, hrefs):
    """Rewrite every `href="#id"` the reused generators emitted."""
    def sub(mo):
        return 'href="' + hrefs.get(mo.group(1), mo.group(1)) + '"'
    return re.sub(r'href="(#[^"]+)"', sub, html)


# Links and media emitted by page renderers are authored relative to the Board
# source folder. A generated group page sits one directory below that folder,
# and a generated question page sits two directories below it. Re-root every
# local URL-bearing attribute together: fixing href alone leaves evidence-card
# images and PDF objects visibly broken even when their text links work.
_TREE_SOURCE_URL = re.compile(
    r'(?P<attr>href|src|data)="(?!https?:|mailto:|data:|#|/)(?P<url>[^"]+)"')


def tree_reroot(html, up, src_dir=None):
    """Move Board-root-relative href/src/data URLs under a split page."""
    def fix(m):
        url = m.group("url")
        bare = url.split("#", 1)[0].split("?", 1)[0]
        # Authored documentation commonly names the generated output itself as
        # `board/index.html` or `board/_assets/...`. Those paths are relative to
        # the Board source folder, just like `_fixture/...`, even though they
        # happen to end in generated filenames.
        if bare.startswith("board/"):
            return f'{m.group("attr")}="{up}{url}"'
        if bare.endswith(".html"):
            # Two kinds of url end in .html and only one of them is sited. A
            # GENERATED page link (`QA/QA0-x.html` on a group index,
            # `../QB/x.html` after tree_relink) names an output file, which
            # never exists in the SOURCE folder. An AUTHORED html file (the
            # deck a slide page's embed points at, JL 260805 on QA4) does
            # exist there, and it needs the hop exactly like a png. The
            # filesystem is the one witness that tells them apart.
            if src_dir is not None and (src_dir / unquote(bare)).exists():
                return f'{m.group("attr")}="{up}{url}"'
            return m.group(0)
        if "_assets/" in bare:          # TREE_TPL owns shared asset paths
            return m.group(0)
        return f'{m.group("attr")}="{up}{url}"'
    return _TREE_SOURCE_URL.sub(fix, html)


def tree_sidebar(meta, qs, root):
    """The left sidebar for the tree.

    Reuses `sidebar_rows()`, the SAME builder the single file uses, so the sidebar
    keeps its per-page section outline (`.sb-out` / `.sb-s` / `.sb-ss`). A first
    version hand-rolled a flat list and silently dropped that outline, which is
    the third time this file's own law caught its author (JL 260731).
    """
    def _href(q):
        gt = bd.group_token(q.get("group") or "") or "_ungrouped"
        return f"{root}{gt}/{tree_page_name(q)}"
    return ('<button type="button" id="sbtoggle" class="sbtoggle" '
            'aria-label="pages">☰</button>'
            '<div class="sbrz" title="Drag to resize"></div><nav class="sidebar" id="sidebar" aria-label="Pages">'
            f'<a class="sb-top" data-page="top" href="{root}index.html">🗂 Index</a>'
            + "".join(sidebar_rows(qs, href_for=_href,
                                   group_href=lambda tok: f"{root}{tok}.html",
                                   meta=meta))
            + '</nav>')


def tree_row(q, href):
    """One index row, in the SAME markup `render()` emits.

    The classes are load-bearing: `.ir` with `.s/.i/.t/.w` is what board.css
    styles. A first pass here invented `.row/.st/.qid/.qt`, so not one rule
    applied and the index rendered as a wall of inline links (JL 260731, with
    a screenshot). Only the href differs between its consumers.
    """
    if q.get("kind") == "doc":
        return (f'<a class="ir doc" href="{href}">'
                f'<span class="s">📄</span><span class="i">{esc(q["id"])}</span>'
                f'<span class="t">{nav_inline(q["title"])}</span>'
                f'<span class="w"></span></a>')
    fr = frac_done_of(q)
    fill = (f' style="--fill:{fr:.3f}"') if fr > 0 else ""
    df = f' data-f="{esc(q["file"])}"' if q.get("file") else ""
    owner = ("🧠 JL" if q["owner"] == "JL"
             else ("🔧 " + q["owner"] if q.get("owner") else ""))
    return (f'<a class="ir {stinfo(q["state"])[1]}" href="{href}"{fill}{df}'
            f' title="{round(fr * 100)}% done">'
            f'<span class="s">{stinfo(q["state"])[0]}</span>'
            f'<span class="i">{esc(q["id"])}</span>'
            f'<span class="t">{nav_inline(q["title"])}</span>'
            f'<span class="w">{owner}</span></a>')


def frac_done_of(q):
    """The same completion fraction render() colours its rows with."""
    progress = aim_progress(sec(q.get("sec", {}), "Done when"),
                            sec(q.get("sec", {}), "Now"))
    return (progress["closed"] / progress["total"]
            if progress["total"] else 0.0)


def tree_page_name(q):
    """One Page, one guessable file; Task Pages lead with their full address."""
    stem = Path(q.get("file") or q["id"]).stem
    if q.get("kind") == "task":
        slug = re.sub(r"^t\d{2}_", "", stem)
        return f"{q['id']}-{slug}.html"
    return f"{stem}.html"


def run_index_body(qs):
    """Compatibility page for former static Run Index URLs.

    Run lineage now has two focused surfaces: 🧾 Evidence Items for
    Supporting and planned work, and ⚙️ Runs for allocated page-local
    Run→Result pairs.  Retaining only this small page avoids breaking old
    bookmarks without rebuilding the crowded global index or promoting a
    ``new-*`` plan into a pretend Run.
    """
    return (
        '<div class="board-heading"><h1 class="h1">Runs moved</h1></div>'
        '<p class="gpurpose">Use a Section’s <b>🧾 Evidence Items</b> '
        'to inspect Supporting Runs, rerun findings, and unallocated plans. '
        'Use <b>⚙️ Runs</b> for real page-local Run → Result pairs only.</p>'
    )

    # Retained below temporarily as a migration reference for old generated
    # trees; it is intentionally unreachable and no longer rendered.
    base = Path(bd.BASE or ".")
    root = repo_root(base)
    registry = run_registry(str(root))
    refs = {}
    plans = {}

    def record(address, q, item, layer, declaration):
        compact = compact_global_run(address)
        if not compact:
            return
        refs.setdefault(compact, []).append({
            "page": q,
            "item": item["item"],
            "layer": layer,
            "declaration": declaration,
        })

    def plan(address, action, family, q, item, layer, declaration):
        """Collect an unallocated route without manufacturing a Run identity."""
        if not action.startswith("new-"):
            return
        anchor = planned_route_anchor(
            address, action, page_id=q["id"], item_id=item["item"], layer=layer,
        )
        entry = plans.setdefault(anchor, {
            "address": address,
            "action": action,
            "family": family,
            "expected": item["expected"],
            "acceptance": item["acceptance"],
            "local_input": item["local_input"],
            "uses": [],
        })
        entry["uses"].append({
            "page": q,
            "item": item["item"],
            "layer": layer,
            "declaration": declaration,
        })

    for q in qs:
        source = base / (q.get("file") or "")
        if not source.is_file():
            continue
        for item in read_items(source).values():
            for entry in item["supporting_runs"].split(";"):
                parts = [part.strip() for part in entry.split("·")]
                if len(parts) >= 3:
                    plan(parts[2], parts[1].lower(), parts[0], q, item,
                         "Supporting", entry.strip())
                    record(parts[2], q, item, "Supporting", entry.strip())
            plan(item.get("address", ""), item.get("action", ""),
                 "Page · Evidence Item", q, item, "Local", item["local_run"])
            record(item.get("address", ""), q, item, "Local", item["local_run"])

    heading = ('<div class="board-heading"><h1 class="h1">Run index</h1></div>'
               '<p class="gpurpose">Planned and registered routes cited by this '
               'Board’s Evidence Item ledgers. A planned route explains what will '
               'be made; a registered Run links its Ticket and Result receipt.</p>')
    if not refs and not plans:
        return (heading + '<p class="mut">No Run route has been declared on this '
                'Board yet.</p>')

    def use_list(refs_for_route):
        uses = []
        for ref in refs_for_route:
            q = ref["page"]
            group = bd.group_token(q.get("group") or "") or "_ungrouped"
            href = f'{group}/{tree_page_name(q)}'
            uses.append(
                '<li><a href="%s">%s · %s</a> <span class="mut">%s</span></li>' %
                (esc(href), esc(q["id"]), esc(ref["item"]), esc(ref["layer"])))
        return "".join(uses)

    rows = []
    for anchor, route in sorted(plans.items()):
        readable = (readable_global_run(route["address"])
                    or readable_task(route["address"])
                    or "Page evidence task")
        action = action_label(route["action"])
        paths = [
            '<p class="run-index-path"><b>Family</b> <code>%s</code></p>' %
            esc(route["family"]),
            '<p class="run-index-path"><b>Expected</b> <span>%s</span></p>' %
            esc(route["expected"]),
            '<p class="run-index-path"><b>Acceptance</b> <span>%s</span></p>' %
            esc(route["acceptance"]),
            '<p class="run-index-path"><b>Ticket</b> '
            '<span class="mut">not allocated yet</span></p>',
            '<p class="run-index-path"><b>Result receipt</b> '
            '<span class="mut">not allocated yet</span></p>',
        ]
        if route["local_input"]:
            paths.insert(
                2,
                '<p class="run-index-path"><b>Planned input</b> <span>%s</span></p>' %
                esc(route["local_input"]),
            )
        rows.append(
            '<section class="run-index-row run-index-plan" id="%s"><h3><code>%s</code> '
            '<span class="run-index-action %s">%s</span></h3>'
            '<div class="run-index-paths">%s</div><ul>%s</ul></section>' %
            (esc(anchor), esc(readable), esc(route["action"]), esc(action),
             "".join(paths), use_list(route["uses"])))
    for compact in sorted(refs):
        readable = readable_global_run(compact)
        record = registry.get(compact)
        if record:
            ticket_href = os.path.relpath(root / record["ticket"], base / "board")
            paths = [
                '<p class="run-index-path"><b>Ticket</b> '
                '<a href="%s"><code>%s</code></a></p>' %
                (esc(ticket_href), esc(record["ticket"])),
            ]
            if record.get("task_root"):
                paths.insert(
                    0,
                    '<p class="run-index-path"><b>Task</b> <code>%s</code></p>' %
                    esc(record["task_root"]),
                )
            if record.get("runtime"):
                runtime_href = os.path.relpath(root / record["runtime"], base / "board")
                paths.append(
                    '<p class="run-index-path"><b>Result receipt</b> '
                    '<a href="%s"><code>%s</code></a></p>' %
                    (esc(runtime_href), esc(record["runtime"])),
                )
            else:
                paths.append(
                    '<p class="run-index-path"><b>Result receipt</b> '
                    '<span class="mut">not created yet</span></p>'
                )
            meta = ('<p><span class="run-index-status">%s</span></p>'
                    '<div class="run-index-paths">%s</div>' %
                    (esc(record["label"]), "".join(paths)))
        else:
            meta = '<p class="mut">Unregistered: no Ticket + runtime receipt found.</p>'
        rows.append(
            '<section class="run-index-row" id="run-%s"><h3><code>%s</code></h3>%s'
            '<ul>%s</ul></section>' %
            (esc(compact), esc(readable), meta, use_list(refs[compact])))
    return heading + '<div class="run-index">%s</div>' % "".join(rows)


def render_tree(meta, qs, out_dir, only=None):
    """Write the board/ tree. Returns the list of files written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    assets = out_dir / "_assets"
    assets.mkdir(exist_ok=True)
    # One file each, assembled from the parts (src/assets.py). The split site
    # links these rather than inlining, so the browser caches one copy for all
    # 61 pages and the ?v= stamp is what makes a ship land.
    # CSS is rstripped; `@charset` goes in front and nothing may precede it.
    # See src/assets.py CSS_CHARSET for why a stylesheet needs to declare its
    # own encoding even when the page that links it already declared one.
    (assets / "board.css").write_text(_assets.CSS_CHARSET + CSS, encoding="utf-8")
    (assets / "board.js").write_text(_assets.js(), encoding="utf-8")

    written = []
    groups = {}
    for q in qs:
        groups.setdefault(q.get("group") or "", []).append(q)

    def shell(title, body, root, crumb="", sidebar=""):
        # `root` is already the hop from this file up to board/, and the board
        # FOLDER is one further up.
        up = root + "../"
        body = tree_reroot(body, up, out_dir.parent)
        popcards = tree_reroot("\n".join(bd.CARDS), up, out_dir.parent)
        return TREE_TPL.format(
            title=esc(title), body=body, root=root, crumb=crumb,
            sidebar=sidebar, popcards=popcards,
            assets_stamp=ASSETS_STAMP, css_stamp=CSS_STAMP, js_stamp=JS_STAMP, favicon=MARK_FAVICON,
            # The drawing host, so a plugin can open a Page's own source without
            # the browser re-deriving what the build already knows. Empty on a
            # Board that declares no `excalidraw:`, which is how 🖌 Draw stays
            # out of the menu rather than offering a surface that cannot open.
            xcal=esc((meta.get("excalidraw") or "").strip().rstrip("/")),
            boarddir=esc(meta.get("dir", "")), bsession=esc(meta.get("session", "")))

    # one file per page, inside its group's folder.
    # `only` limits the rewrite to the pages whose .md actually changed, so a
    # write to one page leaves every other page's FILE untouched and a reader
    # sitting on one of them is never disturbed (QC9, JL 260731).
    n = len(qs)
    for i, q in enumerate(qs):
        if only and Path(q.get("file") or "").name not in only:
            continue
        prv, nxt = (qs[i - 1] if i else None), (qs[i + 1] if i + 1 < n else None)
        # One page, one card buffer. `_chip()` appends to the module-global
        # `bd.CARDS` and shell() dumps all of it, so without this reset a page
        # inherits every earlier page's panels as orphans: a <div popover> whose
        # `popovertarget` button lives in a different document and can never open it.
        bd.CARDS.clear()
        bd.CHIP_N = 0
        bd.EMBED_SEEN.clear()
        bd.EMBEDS.clear()
        card = (render_doc_slide(q, prv, nxt) if q.get("kind") == "doc"
                else render_question(q, prv, nxt))
        # The shared page renderer emits fragment navigation because that is
        # correct for a single Markdown target. In the canonical Board tree,
        # prev/next and the links labelled Index must be real files so the page
        # also navigates with JavaScript disabled.
        page_hrefs = {key: "../" + value for key, value in tree_href_map(qs).items()}
        page_hrefs["#top"] = "../index.html"
        card = tree_relink(card, page_hrefs)
        # Span-Card payloads may name another Board Page. `_chip()` emits the
        # same fragment route as an ASCII map; relink the detached popover HTML
        # too, or the link incorrectly searches for that Page inside the
        # current document instead of opening its generated Page.
        bd.CARDS[:] = [tree_relink(popcard, page_hrefs) for popcard in bd.CARDS]
        gtok = bd.group_token(q.get("group") or "") or "_ungrouped"
        gdir = out_dir / gtok
        gdir.mkdir(exist_ok=True)
        f = gdir / tree_page_name(q)
        crumb = (f' <span class="sb-sep">›</span> '
                 f'<a href="../{gtok}.html">{esc(gtok)}</a>'
                 f' <span class="sb-sep">›</span> <b>{esc(q["id"])}</b>')
        # The tab carries the ID first (JL 260801). A browser tab shows maybe
        # 20 characters, and with a dozen board tabs open the titles all begin
        # with the same kind of phrase; the id is the one token that tells them
        # apart, and it is what JL says out loud when naming a page.
        f.write_text(scrub_cjk_comments(shell(f'{q["id"]} · {q["title"]}', card, "../", crumb,
                                      tree_sidebar(meta, qs, "../"))),
                     encoding="utf-8")
        written.append(f)

    # one file per group: the group's own page (JL 260731).
    # Under `only`, a group is rewritten just when one of ITS pages changed;
    # the index always is, because it lists every page's state.
    for g, members in groups.items():
        if not g:
            continue
        if only and not any(Path(m.get("file") or "").name in only for m in members):
            continue
        bd.CARDS.clear()
        bd.CHIP_N = 0
        bd.EMBED_SEEN.clear()
        bd.EMBEDS.clear()
        gtok = bd.group_token(g)
        rows = []
        for q in members:
            gt = bd.group_token(q.get("group") or "") or "_ungrouped"
            rows.append(tree_row(q, f'{gt}/{tree_page_name(q)}'))
        # A group page is not a bare list (JL 260731: "can we give the group
        # some things too, like what the purpose of this group is"). The intro
        # already lives in board.md under the `### ` heading and was simply
        # never rendered here; line 1 is the purpose, the rest is the why.
        gi = (meta.get("groups") or {}).get(g) or []
        purpose = f'<p class="gpurpose">{inline(gi[0].strip())}</p>' if gi else ""
        # Same body the index shows: prose joined with <br>, any ``` fence as a
        # <pre class="gidia"> figure. This path used to flatten the fence into
        # <p> rows, which is how a group intro's ladder arrived as mangled
        # prose inside "why this group exists" (JL 260801).
        rest = _gi_body(gi)
        why = (f'<details class="gwhy"><summary>why this group exists</summary>'
               f'<div class="gwhy-b">{rest}</div></details>') if rest else ""
        task_group = meta.get("board_kind") == "task-block"
        done = sum(1 for m in members
                   if m["state"].startswith("✅") and m.get("kind") not in ("skill", "agent"))
        counted = [m for m in members if m.get("kind") not in ("skill", "agent")]
        body = (f'<div class="board-heading"><h1 class="h1">{esc(g)}</h1></div>'
                + purpose + why
                + f'<p class="bar">{len(members)} {"tasks" if task_group else "pages"} · '
                  f'{done}/{len(counted)} {"closed" if task_group else "settled"}</p>'
                + group_canvas(meta, g, members)
                + f'<div class="idx">{"".join(rows)}</div>')
        # Group prose may contain authored Q/S references; in a split group
        # page those are file links, not fragments into a monolith.
        body = tree_relink(body, tree_href_map(qs))
        crumb = f' <span class="sb-sep">›</span> <b>{esc(gtok)}</b>'
        f = out_dir / f"{gtok}.html"
        f.write_text(scrub_cjk_comments(shell(g, body, "", crumb,
                                      tree_sidebar(meta, qs, ""))), encoding="utf-8")
        written.append(f)

    # the index: the same rows the single file uses, pointed at the tree
    # The SAME listing the single file builds, including every group intro and
    # its ascii figure, with the links pointed at the tree (JL 260731).
    def _href(q):
        gt = bd.group_token(q.get("group") or "") or "_ungrouped"
        return f"{gt}/{tree_page_name(q)}"
    bd.CARDS.clear()
    bd.CHIP_N = 0
    bd.EMBED_SEEN.clear()
    bd.EMBEDS.clear()
    rows = index_rows(meta, qs, href_for=_href,
                      group_href=lambda tok: f"{tok}.html")
    # The default index carries Board-level orientation; a Board can opt into
    # `index-view: pages` when the page roster is the only useful landing view.
    hrefs = tree_href_map(qs)
    heading = (f'<div class="board-heading">'
               f'<span class="board-mark" aria-hidden="true">{MARK_SVG}</span>'
               f'<h1 class="h1">{esc(meta["title"])}</h1></div>')
    task_board = meta.get("board_kind") == "task-block"
    pages = (f'<h3 class="sec" id="qlist">{"ALL TASKS" if task_board else "ALL PAGES"}</h3>'
             f'<div class="idx">{"".join(rows)}</div>')
    task_pages = [q for q in qs if q.get("kind") == "task"]
    task_done = sum(1 for q in task_pages if q["state"].startswith("✅"))
    task_progress = (
        f'<p class="bar">{task_done}/{len(task_pages)} tasks closed</p>'
        if task_board else ""
    )
    body = (heading + pages if pages_only_index(meta) else
            heading + f'<div class="spine"><p><b>🦴 Spine</b> {inline(meta["spine"])}</p>'
            f'<p><b>🏁 Close when</b> {inline(meta["close"])}</p></div>'
            + task_progress
            + tree_relink(board_map(meta), hrefs)
            + tree_relink(related_folders(meta), hrefs)
            + tree_relink(board_status(qs), hrefs)
            + pages + ACTIVITY_HTML)
    # `index_rows()` also renders each group's authored intro and ASCII map, so
    # relink the complete body rather than only the three Board-level panels.
    body = tree_relink(body, hrefs)
    f = out_dir / "index.html"
    f.write_text(scrub_cjk_comments(shell(meta["title"], body, "", "",
                                     tree_sidebar(meta, qs, ""))),
                 encoding="utf-8")
    written.append(f)

    # Compatibility page only. The live Evidence and Runs plugins own the
    # normal surfaces; this keeps bookmarks from becoming a 404.
    bd.CARDS.clear()
    bd.CHIP_N = 0
    bd.EMBED_SEEN.clear()
    bd.EMBEDS.clear()
    f = out_dir / "runs.html"
    f.write_text(scrub_cjk_comments(shell("Run index", run_index_body(qs), "", "",
                                     tree_sidebar(meta, qs, ""))),
                 encoding="utf-8")
    written.append(f)

    # Prune orphans. Deleting or renaming a page's .md used to leave its .html
    # in the tree forever: still linkable, still looking real, describing a page
    # that no longer exists (JL 260731, found by deleting one and rebuilding).
    # The expected set is computed from EVERY page, not from `written`, so this
    # is correct under --only too.
    expected = {out_dir / "index.html", out_dir / "runs.html"}
    for q in qs:
        gt = bd.group_token(q.get("group") or "") or "_ungrouped"
        expected.add(out_dir / gt / tree_page_name(q))
    for g in groups:
        if g:
            expected.add(out_dir / f"{bd.group_token(g)}.html")
    for stale in sorted(out_dir.rglob("*.html")):
        if stale not in expected:
            stale.unlink()
            print(f"   🗑 pruned orphan {stale.relative_to(out_dir)}")
    for d in sorted(out_dir.iterdir()):
        if d.is_dir() and d.name != "_assets" and not any(d.iterdir()):
            d.rmdir()
    return written
