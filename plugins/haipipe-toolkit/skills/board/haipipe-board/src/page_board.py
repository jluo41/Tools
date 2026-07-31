"""The cover + index + whole-page assembly (QB5: render(), asset inlining,
CJK scrub, JSON emission — moved verbatim from build.py)."""
import base64
import json
import re
from pathlib import Path
from urllib.parse import quote

from . import body as bd
from .body import body, inline
from .common import esc, sec, stinfo
from .page_question import render_question
from .page_stage import render_doc_slide


# The map answers BOTH halves of "where am I" (JL 260731: "did you say what
# folders are used here? engine folder, output folder ... I think here we need
# to mention this as well"). A reader who knows how the groups connect but not
# which folder holds the engine still cannot act, so the heading names folders
# first and pages second.
MAP_HEAD = ('<div class="board-map-head">'
            '<div><span class="board-map-kicker">BOARD MAP</span>'
            '<h2 id="board-map-title">Folders, pages, and how they connect</h2></div>'
            '<p>Which folder holds what, and which pages depend on which. '
            'Arrows are authored; placement is not one.</p>'
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
            '<details class="board-map board-map-ascii" open>'
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
    root = next((p for p in (board_dir, *board_dir.parents)
                 if (p / "pyproject.toml").is_file()), None)
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


def render(meta, qs):
    # Questions and S families share one page grammar, but their progress answers
    # different things: rulings settle; lifecycle pages pass human CHECK gates.
    # A skill page is a synced MIRROR of a shipped unit, not a decision, so it
    # never enters the settled count (JL 260731). That contradiction was the
    # old `Q-Skill` name: it was counted as a question and declared not to be one.
    qonly = [q for q in qs if q.get("kind") not in ("doc", "stage", "skill", "agent")]
    sonly = [q for q in qs if q.get("kind") == "stage"]
    done = sum(1 for q in qonly if q["state"].startswith("✅"))
    nq = len(qonly)
    sfamilies = [
        ("seed", "Seed"),
        ("work", "Work"),
        ("venue", "Venue"),
        ("display", "Display"),
        ("main", "Main"),
        ("appendix", "Appendix"),
        ("submission", "Submission"),
        ("stage", "legacy stages"),
    ]
    bar = "█" * round(done / nq * 14) + "░" * (14 - round(done / nq * 14)) if nq else ""
    n = len(qs)

    def st(q):
        return stinfo(q["state"])

    def frac_done(q):
        """完成度 0..1：Done when 勾了几条。✅ 一律满格，⏸️ 当作定了也满格。"""
        s = q["state"]
        if s.startswith("✅") or s.startswith("⏸"):
            return 1.0
        boxes = re.findall(r"^\s*[-*]\s*\[([ xX])\]", sec(q["sec"], "Done when"), re.M)
        if not boxes:
            return 0.0
        return sum(1 for b in boxes if b.lower() == "x") / len(boxes)

    ginfo = meta.get("groups") or {}
    rows, cur = [], None
    for q in qs:
        if q.get("group") and q["group"] != cur:
            cur = q["group"]
            # A group is a place you can travel to (JL 260730): the canvas draws
            # groups, so a group heading needs an anchor of its own. It is NOT a
            # page — `#group-QA` scrolls the index, it does not open a card — so
            # the id stays in its own namespace and never collides with a page.
            rows.append(f'<div class="grp" id="group-{esc(bd.group_token(cur))}"'
                        f' data-g="{esc(cur)}">'
                        f'<span class="gt">{inline(cur)}</span></div>')
            # Group intro (QC2): one sentence always visible; if more lines follow,
            # they open on click via a native <details>. No script involved, so the
            # strip-scripts invariant is untouched.
            gi = ginfo.get(cur)
            if gi:
                summary = inline(gi[0].strip())
                # 展开的 body：散文按行 <br> 接（保作者断行），碰到 ``` 就当 ascii 图铺成 <pre>。
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
                gib = "".join(parts)
                if gib:
                    rows.append(f'<details class="gi"><summary>{summary}</summary>'
                                f'<div class="gib">{gib}</div></details>')
                else:
                    rows.append(f'<div class="gi one">{summary}</div>')
        if q.get("kind") == "doc":
            rows.append(
                f'<a class="ir doc" href="#{q["id"]}">'
                f'<span class="s">📄</span><span class="i">{esc(q["id"])}</span>'
                f'<span class="t">{inline(q["title"])}</span>'
                f'<span class="w"></span></a>')
            continue
        # 完成度上色：一条没做 = 白，越接近做完越绿（绿色叠加的透明度 = 完成比例）
        fr = frac_done(q)
        pct = round(fr * 100)
        fill = (f' style="--fill:{fr:.3f}"') if fr > 0 else ""
        df = f' data-f="{esc(q["file"])}"' if q.get("file") else ""
        rows.append(
            f'<a class="ir {st(q)[1]}" href="#{q["id"]}"{fill}{df} title="{pct}% done">'
            f'<span class="s">{st(q)[0]}</span><span class="i">{q["id"]}</span>'
            f'<span class="t">{inline(q["title"])}</span>'
            + f'<span class="w">{"🧠 JL" if q["owner"]=="JL" else ("🔧 "+q["owner"] if q["owner"] else "")}</span></a>')
    idx = "\n".join(rows)

    cards = []
    for i, q in enumerate(qs):
        prv, nxt = (qs[i - 1] if i else None), (qs[i + 1] if i + 1 < n else None)
        cards.append(render_doc_slide(q, prv, nxt) if q.get("kind") == "doc"
                     else render_question(q, prv, nxt))

    ctx = ""
    # A board-level figure NEVER folds again (JL 260730). These three sections are
    # already behind a <details class="ctx">, so letting a long fence fold itself
    # into "</> code · N lines" in there is the double-fold the board's own Law
    # forbids: a fold that works and cannot be seen. A board-level canvas is the
    # content of its section, the same argument split_diagram makes for a page's
    # figure, so it stays on stage at any length.
    if meta["theme"]:
        ctx += (f'<details class="ctx"><summary>🦴 Topic — what this board is about</summary>'
                f'<div class="fb">{body(meta["theme"], fold_code=False)}</div></details>')
    if meta["pipeline"]:
        ctx += (f'<details class="ctx"><summary>🔄 Pipeline — how these Qs are ordered</summary>'
                f'<div class="fb">{body(meta["pipeline"], fold_code=False)}</div></details>')
    if meta.get("structure"):
        ctx += (
            '<details class="ctx board-structure">'
            '<summary>🧭 Board-Structure — Board-Folder and Board-Webpage</summary>'
            f'<div class="fb">{body(meta["structure"], fold_code=False)}</div></details>'
        )

    stagebits = []
    for family, label in sfamilies:
        pages = [q for q in sonly if (q.get("family") or "stage") == family]
        if pages:
            gated = sum(1 for q in pages if q["state"].startswith("✅"))
            stagebits.append(f"{gated}/{len(pages)} {label}")
    stagebar = (" · " + " · ".join(stagebits)) if stagebits else ""
    return TPL.format(title=esc(meta["title"]), spine=inline(meta["spine"]),
                      close=inline(meta["close"]), bar=bar, done=done, n=nq,
                      stagebar=stagebar,
                      board_map=board_map(meta), ctx=ctx, index=idx,
                      cards="\n".join(cards), js=JS, css=CSS,
                      mark=MARK_SVG, favicon=MARK_FAVICON,
                      # chip panels last: they are top-layer, so DOM position
                      # is free, and out here they are never inside a <summary>
                      popcards="\n".join(bd.CARDS),
                      boarddir=esc(meta.get("dir", "")),
                      bsession=esc(meta.get("session", "")))


# ── page assets (QB4, JL 260724: build.py was one 2,500-line file) ─────────
# The page's JS and CSS live in assets/ as REAL .js/.css files — editable,
# lintable, node --check-able. build.py INLINES them at build time, so the
# output stays ONE self-contained board.html and the offline invariant holds.
HERE = Path(__file__).resolve().parent.parent
JS = ("\n<script>\n"
      + (HERE / "assets" / "board.js").read_text(encoding="utf-8").rstrip("\n")
      + "\n</script>\n")
CSS = (HERE / "assets" / "board.css").read_text(encoding="utf-8").rstrip("\n")
MARK_SVG = (HERE / "assets" / "board-mark.svg").read_text(encoding="utf-8").strip()
MARK_FAVICON = ("data:image/svg+xml;base64,"
                + base64.b64encode(MARK_SVG.encode("utf-8")).decode("ascii"))

TPL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="{favicon}">
<style>
{css}
</style></head><body class="single" data-board="{boarddir}"><div class="wrap" id="top" data-bsession="{bsession}">

<div class="board-heading"><span class="board-mark" aria-hidden="true">{mark}</span>
<h1 class="h1">{title}</h1></div>
<div class="spine"><p><b>🦴 Spine</b> {spine}</p><p><b>🏁 Close when</b> {close}</p></div>
<p class="bar">{bar}  {done}/{n} questions settled{stagebar}</p>

{board_map}

{ctx}

<h3 class="sec" id="qlist">ALL PAGES<span class="hint">click a row → open it · <a href="#all">show all</a></span></h3>
<div class="idx">{index}</div>

<span id="all"></span>
{cards}

<section class="activity" id="activity" aria-labelledby="activity-title">
<div class="act-head">
  <div><span class="act-kicker">ACTIVITY</span><h2 id="activity-title">When, then where</h2></div>
  <span class="act-status" id="activity-status">waiting for the board server</span>
</div>
<p class="act-note">One update is one dated line in one page's <code>## Log</code>. The count is read from the Markdown itself, so it sees every change any tool made, not only the ones a browser watched.</p>
<div id="activity-body"><p class="act-empty">Open this board through <code>serve.py</code> to count updates. The dashboard is an enhancement; the board remains complete without it.</p></div>
</section>

<p class="foot">Content comes from <code>board.md</code> (board-level), <code>QX-xxx.md</code>
(one per ruling), and named lifecycle pages such as <code>S-Seed-0-xxx.md</code>,
<code>S-Display-0-xxx.md</code>, <code>S-Main-3-xxx.md</code>, or
<code>S-Appendix-A-xxx.md</code>. Edit those, then rebuild:
<code>python3 build.py</code>.<br>Every page is real HTML — the page reads fine
with JavaScript off; the script only adds commenting.</p>
</div>{popcards}{js}</body></html>
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
        boxes = re.findall(r"^\s*[-*]\s*\[([ xX])\]", sec(q["sec"], "Done when"), re.M)
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
                    done=sum(1 for b in boxes if b.lower() == "x"), total=len(boxes),
                    sections={k: v for k, v in q["sec"].items()})
    return json.dumps({"meta": meta, "questions": [q_json(q) for q in qs],
                       "warnings": warn}, ensure_ascii=False, indent=1)
