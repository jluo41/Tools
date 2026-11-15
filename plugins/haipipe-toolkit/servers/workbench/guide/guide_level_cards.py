"""The card Guide: Block · Job · Task sections of cards for every View, and level_steps."""

import re
from pathlib import Path
from urllib.parse import urlencode

from live.guide_core import REPOSITORY, VIEWS, drawing_url, esc, family_drawing
from live.guide_families import LEVEL_NAMES

# ── the card Guide (b03 s31-guide, s31-D05 to D08) ──────────────────────────────────────────────
# A family whose guide.yaml declares `levels:` shows every View as a lead line, then three folding
# sections, Block · Job · Task (a heading, never a box), each a stack of cards, one card shape per
# View and the same in every theme. The View's earlier body stays below, in a closed "All levels"
# fold. Every section starts closed (JL 261008: "collapsed by default"); the level the Guide was opened
# from (context `level`) is marked data-here on its section.
LEVEL_CSS = (".wg-lead{color:var(--wg-muted)}"
             ".wg-level{margin:0 0 6px}.wg-level>summary{list-style:none;cursor:pointer;padding:10px 2px;"
             "display:flex;gap:14px;align-items:baseline}.wg-level>summary::-webkit-details-marker{display:none}"
             ".wg-level>summary::before{content:'▸';color:var(--wg-muted);width:1em}"
             ".wg-level[open]>summary::before{content:'▾'}.wg-level>summary b{font-size:19px;font-weight:500}"
             ".wg-level-line{color:var(--wg-muted);font-size:14px}.wg-level[open] .wg-level-line{display:none}"
             ".wg-level-role{color:var(--wg-muted);font-size:14px;margin:0 0 8px 2px}"
             ".wg-card{border:1px solid var(--wg-rule);border-radius:8px;padding:9px 14px;margin:0 0 8px}"
             ".wg-card-head{margin:0;display:flex;gap:16px;align-items:baseline;flex-wrap:wrap}"
             ".wg-card-head b{font-weight:600}.wg-card-head span{color:var(--wg-muted);font-size:14px}"
             ".wg-card-line{margin:4px 0 0;font:12.5px ui-monospace,monospace;overflow-wrap:anywhere;white-space:pre-wrap}"
             ".wg-card.wg-drawing{padding:0}.wg-card.wg-drawing>summary{padding:9px 14px;list-style:none}"
             ".wg-card.wg-drawing>summary::-webkit-details-marker{display:none}"
             ".wg-card.wg-drawing>summary .wg-card-head b::before{content:'▸ ';color:var(--wg-muted)}"
             ".wg-card.wg-drawing[open]>summary .wg-card-head b::before{content:'▾ '}"
             ".wg-card.wg-drawing>summary .wg-card-head b{color:var(--wg-ink)}"
             ".wg-all>summary b{font-size:16px}")
FOLDED = {"description": "Space", "method": "step", "roadmap-draw": "drawing", "related-paper": "paper"}


def _count(view, n):
    """A folded level's line: `1 drawing`, `6 Spaces`."""
    return f"{n} {FOLDED[view]}" + ("" if n == 1 else "s")


def _card(title, desc, line, cls="wg-card", key=""):
    """One card: its title and what it is, then one line of its parts."""
    head = f'<p class="wg-card-head"><b>{esc(title)}</b><span>{esc(desc)}</span></p>'
    return f'<div class="{cls}">{head}<p class="wg-card-line">{line}</p></div>'


def _level_folders(context, root):
    """{level: folder} for the folder the Guide was opened from, or {} with none."""
    from live import frame
    path = (context.get("path") or "").lstrip("/")
    if not path or root is None:
        return {}
    at = (Path(root) / path).resolve()
    at = at.parent if at.suffix == ".md" else at
    return frame.level_folders(at, Path(root)) if at.is_dir() else {}


def project_link(context, root):
    """(href, name) of the Project the Guide's folder sits in, as SPACE Home's `?project=` names it, or None.
    A folder outside any Project links to its SPACE bucket (SPACE / Shared) by its key."""
    path = (context.get("path") or context.get("file") or "").lstrip("/")
    if not path or root is None:
        return None
    from live.home import project_owner
    root = Path(root).resolve()
    at = (root / path).resolve()
    if not at.exists() or not at.is_relative_to(root):
        return None
    owner = project_owner(at if at.is_dir() else at.parent, root)
    key = owner["project_path"] if owner["project_scope"] == "project" else owner["project_key"]
    return "/?" + urlencode({"project": key}), owner["project"]


def space_cards_html(family, profile, level, folders, root):
    """Description: the six Space cards of one level; sub and runs read live from the frame."""
    from live import frame
    theme = frame.theme_for_guide(family)
    words = (profile["levels"].get(level) or {}).get("spaces") or {}
    cards = []
    for space, subs, runs in frame.space_cards(theme, level, folders.get(level), Path(root or REPOSITORY.parent)):
        w = words.get(space) or {}
        line = (f'sub: {esc(" · ".join(subs) or "—")}   reads: {esc(w.get("reads") or "—")}   '
                f'runs: {esc(" · ".join(runs) or "—")}')
        cards.append(_card(space, w.get("is", ""), line))
    return cards


# a level's heading: `## Task …`, a whole bold line `**Job · …**`, or a line underlined with ---
LEVEL_HEAD = re.compile(r"^(?:#{1,6}\s*(Block|Job|Task)\b.*|\*\*(Block|Job|Task)\b[^*]*\*\*)$")
LEVEL_WORD = re.compile(r"^(Block|Job|Task)\b")


def level_steps(doc):
    """{level: [step row]} from a method file's level tables: a heading or bold line naming the level
    (`Block`, `**Job · …**`, `## Task`), then a table whose header has `step` and `where in the workbench`."""
    out, level, head = {}, None, None
    try:
        lines = Path(doc).read_text(encoding="utf-8").splitlines()
    except OSError:
        return out
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.strip().startswith("|") else None
        if cells is None:
            head = None
            m = LEVEL_HEAD.match(line.strip())
            under = i + 1 < len(lines) and re.fullmatch(r"-{3,}", lines[i + 1].strip())
            if m:
                level = m.group(1) or m.group(2)
            elif under:                             # an underlined section: a level's, or another that ends it
                w = LEVEL_WORD.match(line.strip())
                level = w.group(1) if w else None
            continue
        if head is None:
            low = [c.lower() for c in cells]
            head = low if level and "step" in low and "where in the workbench" in low else []
            continue
        if not head or all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        out.setdefault(level, []).append(dict(zip(head, cells + [""] * (len(head) - len(cells)))))
    return out


def step_cards_html(profile, level):
    rows = level_steps(REPOSITORY / profile["method_doc"]).get(level, []) if profile.get("method_doc") else []
    cards = []
    for n, r in enumerate(rows, 1):
        step = r.get("step", "")
        title = step if re.match(r"^\d", step) else f"{n} · {step}"
        line = (f'where: {esc(r.get("where in the workbench") or "—")}   methods: {esc(r.get("methods") or "—")}   '
                f'signs: {esc(r.get("who signs") or "—")}')
        cards.append(_card(title, r.get("what happens", ""), line))
    return cards


def drawing_cards_html(family, profile, level):
    """RoadMap Draw: a card per drawing guide.yaml roadmap: names for this level; opened, the
    drawing fills it, view only (it loads when the card opens, guide.js)."""
    cards = []
    for n, d in enumerate((profile.get("roadmap") or {}).get(level) or []):
        key = f"roadmap-{level}-{n}"
        rel = family_drawing(profile, key)
        board = str(d.get("board", ""))
        if not rel or not (REPOSITORY / rel).is_file():
            cards.append(_card(d.get("title", board), d.get("shows", ""), f"not found: {esc(board)}"))
            continue
        here = (REPOSITORY / rel).parent              # its builder: build_*.py beside it, or <stem>.py
        builder = next(iter(sorted(here.glob("build_*.py")) + sorted(here.glob(Path(rel).stem + ".py"))), None)
        src = drawing_url(family, key, rel)
        line = (f'source: {esc(board)}   built by: {esc(builder.name if builder else "by hand")}   '
                f'<a href="{esc(src)}" target="_blank" rel="noopener">↗ full size</a>')
        cards.append(f'<details class="wg-card wg-drawing" data-drawing="{esc(key)}"><summary>'
                     f'<p class="wg-card-head"><b>{esc(d.get("title", Path(board).stem))}</b><span>{esc(d.get("shows", ""))}</span></p>'
                     f'<p class="wg-card-line">{line}</p></summary><div class="wg-drawing-body">'
                     f'<iframe title="{esc(d.get("title", ""))}" referrerpolicy="no-referrer" data-src="{esc(src)}"></iframe>'
                     '</div></details>')
    return cards


def paper_cards_html(profile, level):
    """Related Paper: a card per paper whose `level` cell names this level (or `all`)."""
    if not profile.get("papers_table"):
        return []
    from live.related_papers import paper_rows
    cards = []
    for r in paper_rows(REPOSITORY / profile["papers_table"]):
        levels = [x.strip().lower() for x in (r.get("level") or "").split(";")]
        if level.lower() not in levels and "all" not in levels:
            continue
        who, _, title = (r.get("paper") or "").partition(" · ")
        doi = r.get("doi") or ""
        href = ("https://doi.org/" + doi) if doi.startswith("10.") else doi
        line = (f'role: {esc(r.get("role") or "—")}   why here: {esc(r.get("why here") or "—")}'
                + (f'   <a href="{esc(href)}" target="_blank" rel="noopener">↗ doi</a>' if href else ""))
        cards.append(_card(title or who, f'{who} · {r.get("venue", "")}', line))
    return cards


def level_view(family, view, profile, context, root, earlier):
    """One View of the card Guide: a lead line, Block · Job · Task, then the View's earlier body."""
    here = context.get("level") if context.get("level") in LEVEL_NAMES else ""
    folders = _level_folders(context, root) if view == "description" else {}
    lead = (f'<p class="wg-lead">{esc(profile.get("description") or "")}</p>' if view == "description" else
            f'<p class="wg-lead">{esc(dict((k, q) for k, _, q in VIEWS)[view])}</p>')
    parts = [lead]
    for level in LEVEL_NAMES:
        cards = (space_cards_html(family, profile, level, folders, root) if view == "description" else
                 step_cards_html(profile, level) if view == "method" else
                 drawing_cards_html(family, profile, level) if view == "roadmap-draw" else
                 paper_cards_html(profile, level))
        role = (profile["levels"].get(level) or {}).get("role", "")
        body = "".join(cards) or f'<p class="wg-level-role">Nothing for the {level} level yet.</p>'
        parts.append(f'<details class="wg-level" data-drawing="level-{level}" data-level="{level}"'
                     f'{" data-here" if level == here else ""}><summary><b>{level}</b>'
                     f'<span class="wg-level-line">{esc(_count(view, len(cards)))}</span></summary>'
                     f'<p class="wg-level-role">{esc(role)}</p>{body}</details>')
    if earlier:
        parts.append('<details class="wg-level wg-all" data-drawing="level-all"><summary><b>All levels</b>'
                     '<span class="wg-level-line">this View as it was before the levels</span></summary>'
                     f'{earlier}</details>')
    return "".join(parts)
