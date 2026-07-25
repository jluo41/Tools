"""Stage/source content on a slide (QF1, JL 260724): the `![[path]]` /
`![[path#Section]]` embed and the generic markdown renderer behind it.

A face stays q-template; whatever it embeds is shown VERBATIM-generically —
headings (atx AND setext), fences, lists, quotes, record lines, paragraphs —
with ZERO knowledge of the source's dialect. Content is read fresh at every
build, so an embed can never drift from its source. A missing target renders
a visible warning box, never a silent gap.

Import discipline: this module imports body ONLY inside functions (body.py
imports EMBED/embed_block from here at module level; lazy imports here break
the cycle)."""
import os
import re

from .common import esc

# One embed per line, on its own line: ![[relative/path.md]] or
# ![[relative/path.md#Section heading]]
EMBED = re.compile(r"^\s*!\[\[([^\]#|]+?)(?:#([^\]|]+))?\]\]\s*$")

_SETEXT = re.compile(r"^\s*(=+|-+)\s*$")
_ATX = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def _find(token):
    """Resolve an embed path: board-relative first, then walk up toward the
    repo root (same ladder as body.resolve). The file must exist; absolute
    paths and `..` climbing are refused."""
    from . import body as B
    tok = (token or "").strip().replace("\\", "/")
    if not tok or tok.startswith("/") or ".." in tok.split("/"):
        return None
    if B.BASE is None:
        return None
    here = B.BASE
    for _ in range(8):
        cand = here / tok
        if cand.is_file():
            return cand
        if (here / ".git").exists() or (here / "pyproject.toml").exists():
            break
        if here.parent == here:
            break
        here = here.parent
    return None


def _is_setext_head(lines, i):
    """lines[i] is a setext heading title? (next line ===/--- of length >= 3,
    and the title line is not itself a list item / quote / atx heading /
    numbered line — those never make setext headings in these docs)."""
    ln = lines[i]
    if not ln.strip() or i + 1 >= len(lines):
        return 0
    nxt = lines[i + 1]
    if not _SETEXT.match(nxt) or len(nxt.strip()) < 3:
        return 0
    if re.match(r"^\s*([-*>#]|\d)", ln):
        return 0
    return 1 if nxt.strip()[0] == "=" else 2


def _section(text, name):
    """Extract one section by heading text. Accepts atx (# … ######) AND
    setext (title underlined with === or ---, the paper stage docs' form).
    The section runs until the next heading of the same or a higher level.
    Returns None when no heading matches `name` exactly (after strip)."""
    lines = text.split("\n")
    start = level = None
    fence = False
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = _ATX.match(ln)
        if m and m.group(2).strip() == name:
            start, level = i + 1, len(m.group(1))
            break
        lv = _is_setext_head(lines, i)
        if lv and ln.strip() == name:
            start, level = i + 2, lv
            break
    if start is None:
        return None
    out, fence, i = [], False, start
    while i < len(lines):
        ln = lines[i]
        if ln.lstrip().startswith("```"):
            fence = not fence
        if not fence:
            m = _ATX.match(ln)
            if m and len(m.group(1)) <= level:
                break
            lv = _is_setext_head(lines, i)
            if lv and lv <= level:
                break
        out.append(ln)
        i += 1
    return "\n".join(out).strip()


def render_doc(text):
    """Generic markdown -> html, dialect-free and unfolded: sized headings,
    fences as <pre>, `- ` lists as <ul>, `> ` lines as quote rows, `|` rows
    kept line-by-line (record lines / pipe tables stay aligned), blank-line
    paragraphs. Inline marks go through body.inline, so backticked paths
    resolve to links exactly as they do in Q bodies. `![[...]]` lines inside
    an embedded file are NOT expanded (no recursion, no cycles)."""
    from .body import inline
    out, fence, para, ul = [], None, [], []

    def close_para():
        if para:
            out.append(f'<p>{inline(" ".join(para))}</p>')
            para.clear()

    def close_ul():
        if ul:
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in ul) + "</ul>")
            ul.clear()

    lines = text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.lstrip().startswith("```"):
            close_para(); close_ul()
            if fence is None:
                fence = []
            else:
                out.append(f"<pre>{esc(chr(10).join(fence))}</pre>")
                fence = None
            i += 1
            continue
        if fence is not None:
            fence.append(ln)
            i += 1
            continue
        m = _ATX.match(ln)
        if m:
            close_para(); close_ul()
            out.append(f'<div class="eh eh{len(m.group(1))}">{inline(m.group(2))}</div>')
            i += 1
            continue
        lv = _is_setext_head(lines, i)
        if lv:
            close_para(); close_ul()
            out.append(f'<div class="eh eh{lv}">{inline(ln.strip())}</div>')
            i += 2
            continue
        if not ln.strip():
            close_para(); close_ul()
            i += 1
            continue
        m = re.match(r"^\s*[-*]\s+(.+)$", ln)
        if m:
            close_para()
            ul.append(m.group(1).strip())
            i += 1
            continue
        if ln.lstrip().startswith(">"):
            close_para(); close_ul()
            out.append(f'<div class="eq">{inline(ln.lstrip().lstrip(">").strip())}</div>')
            i += 1
            continue
        if ln.lstrip().startswith("|"):
            close_para(); close_ul()
            out.append(f'<div class="er">{inline(ln.strip())}</div>')
            i += 1
            continue
        para.append(ln.strip())
        i += 1
    close_para(); close_ul()
    if fence is not None:
        out.append(f"<pre>{esc(chr(10).join(fence))}</pre>")
    return "\n".join(out)


def render_doc_slide(q, prv, nxt):
    """One Roster `doc:` entry -> one slide (QF2): the listed source files
    rendered directly, stacked, each under a linked header. No state pill, no
    Items counting, no comment target — the sources stay untouched and the
    slide is a pure view of them."""
    from . import body as B
    parts = []
    for rel in q["files"]:
        src = _find(rel)
        if src is None or src.suffix.lower() not in (".md", ".txt"):
            parts.append(f'<div class="embed miss">⚠ doc not found (or not .md/.txt): '
                         f'<code>{esc(rel)}</code></div>')
            continue
        try:
            href = os.path.relpath(src, B.BASE)
        except ValueError:
            href = None
        head = (f'<a class="fp" href="{esc(href)}">📄 {esc(rel)}</a>' if href
                else f'<span>📄 {esc(rel)}</span>')
        parts.append(f'<div class="embed doc"><div class="emh">{head}'
                     f'<span class="elive">rendered from source</span></div>'
                     f'<div class="emb">{render_doc(src.read_text(encoding="utf-8"))}</div></div>')
    nav = ('<div class="nav">'
           + (f'<a href="#{prv["id"]}">← {prv["id"]}</a>' if prv else '<span></span>')
           + f'<a class="all" href="#top">☰ Index</a>'
           + (f'<a href="#{nxt["id"]}">{nxt["id"]} →</a>' if nxt else '<span></span>')
           + '</div>')
    return (f'<section class="slide q doc" id="{q["id"]}" data-title="{esc(q["title"])}">'
            f'<div class="qh"><span class="qid">📄</span>'
            f'<span class="pill docp">source doc</span>'
            f'<a class="top" href="#top">↑ Index</a></div>'
            f'<h2 class="h2"><span class="hid">{esc(q["id"])} </span>{esc(q["title"])}</h2>'
            + "".join(parts) + nav + '</section>')


def embed_block(path_token, section):
    """One `![[path]]` / `![[path#Section]]` line -> a live-from-source block.
    Every failure mode is VISIBLE on the page (missing file, wrong extension,
    heading not found) — an embed never silently renders empty."""
    from . import body as B
    src = _find(path_token)
    label = esc(path_token) + (f'<span class="es">#{esc(section.strip())}</span>'
                               if section else "")
    if src is None:
        return (f'<div class="embed miss">⚠ embed not found: '
                f'<code>{esc(path_token)}</code></div>')
    if src.suffix.lower() not in (".md", ".txt"):
        return (f'<div class="embed miss">⚠ embed: only .md / .txt sources '
                f'(got <code>{esc(src.name)}</code>)</div>')
    text = src.read_text(encoding="utf-8")
    if section is not None:
        sub = _section(text, section.strip())
        if sub is None:
            return (f'<div class="embed miss">⚠ embed: no heading '
                    f'"{esc(section.strip())}" in <code>{esc(path_token)}</code></div>')
        text = sub
    try:
        href = os.path.relpath(src, B.BASE)
    except ValueError:
        href = None
    head = (f'<a class="fp" href="{esc(href)}">📄 {label}</a>' if href
            else f'<span>📄 {label}</span>')
    return (f'<div class="embed"><div class="emh">{head}'
            f'<span class="elive">live from source</span></div>'
            f'<div class="emb">{render_doc(text)}</div></div>')
