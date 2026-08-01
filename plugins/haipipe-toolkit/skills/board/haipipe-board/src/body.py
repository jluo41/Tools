"""The board's body grammar -> html (ref/board-form.md §5): inline marks, link
resolution, topic/explanation bullets, checklists, fences, comment lanes, logs.
BASE (the board folder) is set by the entry point; LINKS is filled by
parse.parse_board from board.md's ## Links. Both live here because inline()
is where paths become hrefs."""
import re
from functools import lru_cache

from .common import esc, who_class
from .page_stage import EMBED, embed_block

BASE = None            # 当前这块板的文件夹，build.py 的入口设；用来把路径解析成链接
LINKS = {}             # board.md 的 ## Links 声明的： 反引号里的写法 -> 相对路径
EXT = ("md", "py", "html", "css", "js", "json", "yaml", "yml", "sh", "txt", "ipynb",
       "do", "R", "r", "sql", "tex", "bib", "toml", "csv", "tsv", "ps1", "log")


def resolve(token):
    """`反引号里的路径` -> 相对 Board source root 的 href，解析不到就返回 None。

    板上讨论的东西（SKILL.md、build.py、另一块板…）和板本身是分开放的，
    光写个路径读者点不动。这里做的事：从板的文件夹往上一路找，
    第一个真实存在的匹配就变成可点的链接。**文件必须真的存在**才链 ——
    否则 `Q*.md`、`- [ ]` 这种也会被误当成路径。
    """
    if not token:
        return None
    if token in LINKS:                      # 板自己声明的，优先，且不做存在性猜测
        return LINKS[token]
    if BASE is None or " " in token:
        return None
    tok = token.rstrip("/")
    if "/" not in tok and tok.rsplit(".", 1)[-1] not in EXT:
        return None
    if any(c in tok for c in "*?<>|"):
        return None
    here = BASE
    for _ in range(8):
        cand = (here / tok)
        if cand.exists():
            try:
                import os
                return os.path.relpath(cand, BASE)
            except ValueError:
                return None
        if (here / ".git").exists() or (here / "pyproject.toml").exists():
            break
        if here.parent == here:
            break
        here = here.parent
    return None


LABEL_TOK = re.compile(r"^(?:tab|fig):[a-z0-9_-]+$")


def code_or_link(m):
    tok = m.group(1)          # 已经过外层 esc()，别再转义一次（否则 `>` 显示成 &gt;）
    # `fig:discretion-gradient` in backticks is a FLOAT LABEL, not a path. It
    # resolves to nothing, so it would render as inert grey code; make it a chip
    # here, because the rewriter is forbidden to reach inside a code span.
    if PAPER is not None and LABEL_TOK.match(tok):
        return _ref(tok)
    href = resolve(tok)
    if href:
        return f'<a class="fp" href="{esc(href)}"><code>{tok}</code></a>'
    return f"<code>{tok}</code>"


# The paper dialect's index, or None. build.py sets it once per build; a board
# that does not declare `dialect: paper` never pays for any of this.
PAPER = None

# The board's own Excalidraw host, set per build from board.md's `excalidraw:` key.
EXCAL_HOST = ""

# Every paper marker in ONE alternation, so a single left-to-right pass
# consumes each one exactly once and nothing a chip emits is ever re-scanned.
#   1 keys  2 qid   \citep{a,b} · \cite{TOADD} [Q-Sec6Results-4]
#   3 desc  4 qid   {VAL:? what the number is} [Q-Sec6Results-4]
#   5 qid           a bare [Q-Sec6Results-4], which the other two did not claim
#                   The stage token may carry digits (a per-unit stage names
#                   its unit in it), which is why it is [A-Za-z0-9]+ below.
#   6 did           a display unit, in either layout and either length:
#                   S-Display-4a · S-Display-4a-main-regression (workspace, the
#                   folder is named for its page) · display02 · display02-x
#                   (legacy). A page may write the SHORT form and a Section the
#                   long one; both name the same unit.
#                   ALWAYS A CARD, ruled by JL 260727. A unit name in prose
#                   renders as the evidence card, never as a bare page link,
#                   because the card already carries the owning page's anchor
#                   and its state line, so the card is a strict superset. The
#                   page ANCHOR keeps the uppercase short id (S-Display-4A),
#                   so the two identities never collide on one string.
#   7 label         \ref{tab:…} / \autoref{fig:…}, the LaTeX form
#   8 label         a bare tab:… / fig:… label, which is how a page names a
#                   float without writing LaTeX. Not inside \label{}.
# The bracket sits BESIDE its marker and is never fused into it.
# The display id is fenced by lookarounds so `displays/display02-x/float.tex`
# stays a path: no shorter prefix can satisfy the trailing guard either.
MARKER = re.compile(
    r"\\cite[tp]?\*?\{([^}]*)\}(?:\s*\[(Q-[A-Za-z0-9]+-\d+)\])?"
    r"|\{VAL:\?([^}]*)\}(?:\s*\[(Q-[A-Za-z0-9]+-\d+)\])?"
    r"|\[(Q-[A-Za-z0-9]+-\d+)\]"
    r"|(?<![\w/-])((?:S-Display-\d+[a-z]?(?:[a-z]\d+)?|display\d{2}[a-z]?)"
    r"(?:-[a-z0-9-]+)?)(?![\w/-])"
    r"|\\(?:auto|C|c)?ref\{((?:tab|fig):[^}]*)\}"
    r"|(?<![\w:/{-])((?:tab|fig):[a-z0-9_-]+)(?![\w-])"
    #   9 num  10 pct   a NUMBER in the prose. Last in the alternation on
    #                   purpose: every branch above consumes its own digits
    #                   first, so the 6 and 2 in [Q-Sec6Results-2], the 04 in display04
    #                   and the 2024 in \citep{smith2024} are never seen here.
    #                   Only chipped when the string already carries a [Q-…],
    #                   which is what scopes this to sentences that CLAIM
    #                   something measured (see cite_chips).
    r"|(?<![\w.,$/-])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\.\d+|\d+)(%)?(?![\w.,]*[\w])")

# A year is a date, not a measurement, and a lone 0 or 1 is almost never a
# finding. Skipping them is the difference between a highlight and a mess.
YEAR = re.compile(r"^(1[89]|20)\d{2}$")
# A BOUND immediately before the number: `p < 0.001`, `N >= 500`. The sentence
# never claimed the figure EQUALS that, so checking it against the run finds
# every recorded value under the bound and cries ambiguity.
# A bare `=` is NOT a bound and must not be here (JL 260727). `N = 1,204,607`
# is a measurement stated the ordinary way, and swallowing it silently
# un-checked four of the five cohort sample sizes on `S-Main-5`, which is the
# whole sampling claim of the paper. `=?` still absorbs the `=` of `<=` / `>=`,
# so the case the guard was written for is unaffected.
CMP = re.compile(r"(?:&lt;|&gt;|<|>|≤|≥)=?\s*$")


# One popover panel per chip. They are COLLECTED rather than emitted inline,
# because a chip usually sits inside a sentence's <summary>, which may hold
# phrasing content only: a <div popover> there would be invalid HTML. The top
# layer ignores DOM position, so they all flush at the end of the document.
CARDS = []
CHIP_N = 0

# Face ids on THIS board, set once per build. Lets a chip link to a sibling
# page only when that page actually exists here.
FACE_IDS = set()
# Group tokens on THIS board ("QA", "QAa", "Q-Skill"), same lifecycle. A group is
# not a page, so it anchors at `#group-<token>` on the index instead.
GROUP_IDS = set()


def group_token(heading):
    """"QA · Defining a board" -> "QA": the group's travelling name.

    Every group heading on every board is `<token> · <words>`; the fallback to
    the first whitespace token keeps a heading that forgot the separator from
    anchoring at the whole sentence."""
    head = heading.split("·", 1)[0].strip()
    return head.split()[0] if head.split() else heading.strip()


@lru_cache(maxsize=8)
def _face_pat(faces, groups, aliases=frozenset()):
    """One alternation over every id this board can travel to, LONGEST FIRST.

    Longest-first is what keeps `QAa0` from being read as the group `QAa`, and
    `QA6` from being read as `QA`. The set itself is the pattern, so an id shaped
    unlike the others (`Q-Skill-haipipe-board`) needs no special case."""
    toks = sorted(faces | groups | aliases, key=len, reverse=True)
    if not toks:
        return None
    return re.compile(r"(?<![\w#/.-])(" + "|".join(re.escape(t) for t in toks)
                      + r")(?![\w-])")


def link_faces(code):
    """Page and group ids inside an ASCII figure become links (JL 260730).

    A canvas is only a map if you can travel on it. The wrap happens AFTER
    esc() and adds no characters to the line, so every column stays where its
    author put it; the anchor is a plain fragment, so it travels with scripts
    off, on a static host, exactly like an index row.

    FACE_IDS / GROUP_IDS are the authority: a token that is not a page or group
    on THIS board stays plain text. A retired or renamed id therefore shows up
    as dead text in the figure rather than as a link that goes nowhere, which
    makes the canvas check itself on every build.
    """
    alias = _alias_ids()
    pat = _face_pat(frozenset(FACE_IDS), frozenset(GROUP_IDS), frozenset(alias))
    if pat is None:
        return code

    def one(m):
        t = m.group(1)
        if t in FACE_IDS:
            href = f"#{t}"
        elif t in GROUP_IDS:
            href = f"#group-{t}"
        else:
            href = f"#{alias[t]}"
        return f'<a class="fl" href="{href}">{t}</a>'

    return pat.sub(one, code)


def _alias_ids():
    """A declared Link whose target is a page on THIS board -> {old id: new id}.

    Renaming 36 pages to match their groups (JL 260731) left every older id
    stranded in the figures that cite it: `QAa5` was suddenly not a page, so it
    rendered as dead text even though `## Links` still knew exactly where it went.
    An alias is a real address, so it travels like one. The id shown stays the
    OLD one, because that is what the figure's author wrote and what a reader is
    looking for; only the destination is current.
    """
    out = {}
    for old, target in LINKS.items():
        stem = target.rsplit("/", 1)[-1]
        if not stem.endswith(".md"):
            continue
        stem = stem[:-3]
        if re.match(r"^Q-[A-Z]", stem):
            pid = stem
        elif stem.startswith(("Skill-", "Agent-")):
            # the skill and agent page kinds: the id is `<Kind>-<unit>`,
            # never the whole stem
            m = re.match(r"^((?:Skill|Agent)-\d+)", stem)
            pid = m.group(1) if m else stem
        else:
            pid = stem.split("-", 1)[0]
        if pid in FACE_IDS and old not in FACE_IDS and old not in GROUP_IDS:
            out[old] = pid
    return out


def _rel(p):
    """An absolute path -> an href relative to the Board source root."""
    try:
        import os
        return os.path.relpath(p, BASE)
    except (ValueError, TypeError):
        return None


def _sources(meta):
    """The dialect returns DATA about where a marker's source lives (QBc5);
    turning it into links is the board's job, and it happens here.

    Three kinds, in the order a reader wants them: the DEFINITION (which .bib
    file, which line), the SOURCE ITSELF (doi / arXiv / url, off-site), and the
    raw entry as written, so the panel answers "is this the right work" without
    a round trip.
    """
    if not meta:
        return ""
    # A figure's evidence is the picture, so the panel SHOWS it rather than
    # linking to it, and every image is labelled LIVE or CANDIDATE (QC4's law).
    # A table's evidence is its rows, so the body is shown as text (QC3).
    prev = []
    for kind, label, path, text in meta.get("preview", []):
        href = _rel(path)
        cap = f'<figcaption>{esc(label)}</figcaption>'
        if kind == "img" and href:
            prev.append(f'<figure class="ccprev">{cap}'
                        f'<img src="{esc(href)}" alt="{esc(label)}" '
                        f'loading="lazy"></figure>')
        elif kind == "pdf" and href:
            # <object>, not <img>: a browser renders a PDF natively and this
            # stays script-free. The link inside is the fallback a viewer-less
            # browser shows, so the evidence is never a blank rectangle.
            prev.append(f'<figure class="ccprev">{cap}'
                        f'<object class="ccpdf" data="{esc(href)}" '
                        f'type="application/pdf">'
                        f'<a class="fp" href="{esc(href)}">open {esc(label)}</a>'
                        f'</object></figure>')
        elif kind == "text":
            prev.append(f'<figure class="ccprev">{cap}'
                        f'<pre class="ccraw">{esc(text)}</pre></figure>')
    # A citation's preview is the REFERENCE as the manuscript will print it,
    # rendered by the paper's own .bst (see refs.py). Same job as the picture
    # for a figure and the rows for a table: show the thing, do not describe it.
    if meta.get("reference"):
        prev.append('<figure class="ccprev"><figcaption>AS IT WILL PRINT · '
                    'the paper\'s own .bst</figcaption>'
                    f'<div class="ccref">{esc(meta["reference"])}</div></figure>')
    prev = "".join(prev)
    out = []
    # The S-Display page that OWNS this unit, as a same-board anchor. Emitted
    # only when that face is really on this board, so a board whose paper-root
    # has no lifecycle tree simply does not show it (JL 260727).
    sd = meta.get("sdisplay")
    if sd and sd in FACE_IDS:
        st = meta.get("sdstate") or ""
        out.append(f'<a class="fp sdl" href="#{esc(sd)}">🗂 {esc(sd)}'
                   + (f' · {esc(st)}' if st else "") + '</a>')
    e = meta.get("entry")
    if e is not None:
        href = _rel(e.path)
        where = f"{e.path.name}:{e.line}"
        out.append(f'<a class="fp" href="{esc(href)}">📄 {esc(where)}</a>'
                   if href else f"<span>📄 {esc(where)}</span>")
    for item in meta.get("links", []):
        # (label, href) or (label, href, glyph). The glyph is how a SEARCH link
        # is told apart from an identifier at a glance, without a second row.
        lbl, href = item[0], item[1]
        icon = item[2] if len(item) > 2 else "🔗"
        out.append(f'<a class="fp" href="{esc(href)}" target="_blank" '
                   f'rel="noopener">{icon} {esc(lbl)}</a>')
    for rel, path in meta.get("files", []):
        href = _rel(path)
        out.append(f'<a class="fp" href="{esc(href)}">📄 {esc(rel)}</a>'
                   if href else f"<span>📄 {esc(rel)}</span>")
    if meta.get("target"):
        out.append(f'<span class="cctgt">🎯 {esc(meta["target"])}</span>')
    # preview first: it is the answer to "is this the right thing", and the
    # links are what you reach for only once it is not.
    html = prev + (f'<div class="ccl">{"".join(out)}</div>' if out else "")
    if e is not None:
        html += f'<pre class="ccraw">{esc(e.raw)}</pre>'
    if meta.get("suggest"):
        rows = "".join(f'<div><b>{esc(k)}</b> {esc(one)}</div>'
                       for k, one in meta["suggest"])
        html += (f'<div class="ccsug"><span class="cck">keys that DO resolve, '
                 f'nearest first</span>{rows}</div>')
    return html


def _chip(kind, state, label, tip, meta=None):
    """A chip is a BUTTON that opens an attached panel, and the panel is real
    body text (JL 260726).

    The `title=` stays underneath as the floor: hover keeps working, and if
    `popover` is unsupported the record is still reachable. The gain over a
    tooltip is not comfort. A tooltip lives in an ATTRIBUTE, which the build's
    "chars of body surviving with JS stripped" assertion does not count, so the
    evidence passed that test on a technicality. In a panel it is counted,
    Ctrl-F findable, and printable.
    """
    global CHIP_N
    CHIP_N += 1
    cid, anc = f"pc{CHIP_N}", f"--a{CHIP_N}"
    # The tooltip IS the reference for a resolved citation, because hover is the
    # floor and the floor should carry the best thing available. In the panel
    # that would print it twice, so the body drops any line the preview repeats.
    shown = (meta or {}).get("reference", "")
    rows = [x.strip() for x in tip.split("\n")
            if x.strip() and x.strip() != shown]
    body = "".join(f"<p>{esc(x)}</p>" for x in rows)
    CARDS.append(
        f'<div popover id="{cid}" class="chipcard {kind} {state}"'
        f' style="position-anchor:{anc}">'
        f'<div class="cch"><span class="cck">{esc(kind)} · {esc(state)}</span>'
        f'<b>{esc(label)}</b></div>'
        f'<div class="ccb">{body}</div>{_sources(meta)}</div>')
    return (f'<button type="button" class="chip {kind} {state}"'
            f' popovertarget="{cid}" style="anchor-name:{anc}"'
            f' title="{esc(tip)}">{esc(label)}</button>')


def _unesc(s):
    """inline() escapes before we run, so a captured description arrives as
    `the model&#x27;s MAE`. Put it back before it goes into a title=, which
    _chip escapes again."""
    for a, b in (("&#x27;", "'"), ("&quot;", '"'), ("&gt;", ">"),
                 ("&lt;", "<"), ("&amp;", "&")):
        s = s.replace(a, b)
    return s


# A landed answer under a marker that still says "owed" is not an error and not
# fine: it is work sitting on the table, and it deserves its own colour.
def _landed(state, tip, meta, still):
    if state != "ok":
        return state, tip, meta
    return ("ready",
            f"THE ANSWER HAS LANDED and the prose still says {still}.\n{tip}",
            meta)


# Never rewrite inside a code span or inside a tag's attributes. A page that
# DISCUSSES placeholders writes `\cite{TOADD}` in backticks, and chipping that
# turns documentation into a false defect report.
NO_CHIP = re.compile(r"(<code>.*?</code>|<[^>]+>)", re.S)

# The same trap one level up (260726). A human writing
#   > JL: I think you should use \citep{xxx}
#   > CC: Mafi 2013 is still open -> add \citep{mafi...} or a \cite{TOADD}
# is ASKING for a citation, not making one. Backticks are optional in a comment
# and nobody will remember them, so the whole discussion lane opts out instead.
# Typed evidence lanes (`> Citation:`, `> Value:`, `> Display:`) still chip:
# those ARE claims about the sentence, and their state is the point.
QBRACKET = re.compile(r"\[(Q-[A-Za-z0-9]+-\d+)\]")

NOTE = False


def note(s):
    """inline() for discussion text: same rendering, no chips."""
    global NOTE
    prev, NOTE = NOTE, True
    try:
        return inline(s)
    finally:
        NOTE = prev


def note_body(txt, **kw):
    """body() for narration ABOUT the work (`## Log`): same rendering, no chips.

    Same ruling as the discussion lanes, for the same reason. A log line QUOTES
    markers while explaining what changed; it does not make the claim. Left
    chipped, a line saying "the composite named [Q-Section-7] while its
    explanation named [Q-Section-1]" scopes number-chipping across the whole
    line, and its own DATE came out as an unverified measurement (260726).
    """
    global NOTE
    prev, NOTE = NOTE, True
    try:
        return body(txt, **kw)
    finally:
        NOTE = prev


def _cite(keys_raw, qid, raw):
    keys = [k.strip() for k in keys_raw.split(",") if k.strip()]
    out, took_q = [], False
    for k in keys:
        if k.upper() != "TOADD":
            state, label, tip, meta = PAPER.citation(k)
            out.append(_chip("cite", state, label, tip, meta))
            continue
        if not qid:
            out.append(_chip("cite", "unowned", "TOADD (no question)",
                             "a placeholder with no [Q-…] bracket beside it. "
                             "Nothing will ever resolve this one."))
            continue
        took_q = True
        state, tip, meta = _landed(*PAPER.question(qid), "TOADD")
        out.append(_chip("cite", state, f"TOADD → {qid}",
                         "owed citation. The .bib is HUMAN-ONLY: an agent may "
                         "grep it and report a missing key, never write one.\n"
                         + tip, meta))
    if not out:
        return raw
    if qid and not took_q:                 # \citep{realkey} [Q-…]: keep both
        out.append(_qref(qid))
    return "".join(out)


def _value(desc, qid):
    d = " ".join(_unesc(desc).split())
    want = ("WANTED: " + d) if d else \
        "WANTED: the marker does not even say WHICH number is missing."
    if not qid:
        return _chip("val", "unowned", "VAL? (no question)",
                     want + "\nNo [Q-…] bracket beside it, so no question owes "
                     "this number and nothing will ever fill it.")
    state, tip, meta = _landed(*PAPER.question(qid), "{VAL:?}")
    return _chip("val", state, f"VAL? → {qid}", f"{want}\n{tip}", meta)


def _qref(qid):
    state, tip, meta = PAPER.question(qid)
    return _chip("qref", state, qid, tip, meta)


def _number(raw, pct, qid):
    """A measured number in a sentence that names the question owing it.

    JL 260726: the NUMBER is the claim and the bracket is the bookkeeping, so
    the number is what carries the colour. The bracket stays, quieter, because
    it is still the binding.
    """
    if YEAR.match(raw) and not pct:
        return raw + (pct or "")
    if not pct and len(raw) == 1 and raw in "01":
        return raw
    state, tip, meta = PAPER.check_number(qid, raw)
    return _chip("num", state, raw + (pct or ""), tip, meta)


def _kind(u, fallback_label=""):
    """A table and a figure are two pages (QC3, QC4) because a reader can check
    a table on sight and cannot check a figure at all, so the chip says which
    BEFORE the state. When the unit is unknown the label prefix is the only
    hint there is, and an unresolved marker still deserves the right icon."""
    if u is not None:
        return "tab" if u.kind == "table" else "fig"
    return "tab" if fallback_label.startswith("tab:") else "fig"


def _display(did):
    state, tip, meta = PAPER.display(did)
    return _chip("disp " + _kind(PAPER.unit(did)), state, did, tip, meta)


def _ref(label):
    state, tip, meta = PAPER.ref(label)
    return _chip("disp " + _kind(PAPER.by_label.get(label), label),
                 state, label, tip, meta)


def cite_chips(s):
    """Rewrite every paper marker into a chip that knows its own state.

    Runs LAST in inline(), so the HTML it emits is never re-processed by the
    earlier substitutions. Without the paper dialect it is a no-op.
    """
    if PAPER is None or NOTE:
        return s
    # Numbers are only chipped in a sentence that already names the question
    # owing them. Without this scope every section number, count and year on
    # the board would light up, and the signal would be worth nothing.
    owner = QBRACKET.search(s)
    qid_here = [owner.group(1) if owner else ""]

    def one(m):
        if m.group(9):                       # a number in the prose
            # `p < 0.001` is a BOUND, not a measurement. Checking it against the
            # run finds every recorded p-value under a thousandth and calls the
            # sentence ambiguous, which is noise: the sentence never claimed the
            # figure equals 0.001. Numbers after a comparison are left alone.
            # (The text is already HTML-escaped here, so the operator is &lt;.)
            if CMP.search(m.string[max(0, m.start() - 7):m.start()]):
                return m.group(0)
            return (_number(m.group(9), m.group(10), qid_here[0])
                    if qid_here[0] else m.group(0))
        if m.group(7) or m.group(8):         # \ref{tab:…}, or a bare label
            return _ref(m.group(7) or m.group(8))
        if m.group(6):                       # a unit name -> ALWAYS the card
            return _display(m.group(6))
        if m.group(5):                       # a bare [Q-…]
            return _qref(m.group(5))
        if m.group(3) is not None:           # {VAL:? …}
            return _value(m.group(3), m.group(4))
        return _cite(m.group(1), m.group(2), m.group(0))

    parts = NO_CHIP.split(s)
    for i in range(0, len(parts), 2):      # even slices are plain text
        parts[i] = MARKER.sub(one, parts[i])
    return "".join(parts)


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", code_or_link, s)
    # The next four run OUTSIDE code spans only. `code_or_link` has already
    # emitted <code>…</code>, and a rule applied over the whole string reaches
    # inside it: a page that WROTE `![](path)` in backticks, to talk about the
    # syntax, had it rendered as a real (and dead) image.
    #
    # IMAGE BEFORE LINK, because `![alt](path)` contains `[alt](path)`, so a link
    # rule running first consumes it and leaves a literal `!` in front of a link.
    # No markdown image had ever rendered on any board for that reason; QD3's
    # screenshot had been showing as `!` plus a link since the day it was added.
    def _marks(seg):
        def media(m):
            alt, src = m.group(1), m.group(2)
            # A PDF is a real readable display, not a broken image. Keep the
            # familiar Markdown image form so a page author need not write raw
            # HTML (which Board escapes), but render it as a native PDF object
            # with an always-visible fallback link for viewer-less browsers.
            if re.search(r"\.pdf(?:[?#].*)?$", src, re.I):
                return (f'<object class="figpdf" data="{src}" '
                        f'type="application/pdf"><a class="fp" href="{src}">'
                        f'open {alt or "PDF"}</a></object>')
            return f'<img class="fig" alt="{alt}" src="{src}" loading="lazy">'

        seg = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", media, seg)
        seg = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a class="fp" href="\2">\1</a>', seg)
        seg = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", seg)
        return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", seg)

    # Code spans are held OUT of _marks so `**` inside them stays literal. But
    # splitting on them also cut every mark that SPANS one, so `**run `x.py`
    # now**` rendered as literal asterisks around a code span, on every board
    # since the split was written (found 260727 on a skill page, where SKILL.md
    # writes that shape often). Fix: swap each code span for an opaque sentinel,
    # run the marks over the whole string, then put the spans back. The sentinel
    # holds no `*`, `[`, or `!`, so it cannot be eaten by any rule.
    held = []

    def _stash(m):
        held.append(m.group(0))
        return f"\x00{len(held) - 1}\x00"

    s = re.sub(r"<code>.*?</code>", _stash, s, flags=re.S)
    s = _marks(s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: held[int(m.group(1))], s)
    # 裸 URL 自动变链接（放最后）。前面那个 lookbehind 是为了别去动已经躺在
    # href="…" / src="…" 里的地址 —— 否则会把链接再套一层链接。
    s = re.sub(r'(?<![\"\'=])(https?://[^\s<>"\')]+)',
               r'<a class="fp" href="\1" target="_blank" rel="noopener">\1</a>', s)
    return cite_chips(s)


# The leading `- ` is optional and must be: nearly every Log line on every board
# is written as a bullet (`- 260726 · …`), and without it those lines matched
# nothing. They were neither sorted nor counted, so a page could show four
# entries under a header reading "Log (0)".
LG_HEAD = re.compile(r"^(?:[-*]\s+)?(\d{6})(?:\s+(\d{3,4}))?\s*[·|]\s*(.*)$")


def sort_log(txt):
    """## Log 按时间倒序 —— 最新的在最上面。

    你在 md 里加到哪一行都行，生成时统一排。跨行的条目（缩进的续行）
    跟着它的头一行一起搬。没有时间戳的行原样留在最前面。
    """
    head, ents, cur = [], [], None
    for ln in (txt or "").split("\n"):
        m = LG_HEAD.match(ln.strip())
        if m:
            cur = [(m.group(1), (m.group(2) or "0000").zfill(4)), [ln]]
            ents.append(cur)
        elif cur is not None:
            cur[1].append(ln)
        elif ln.strip():
            head.append(ln)
    ents.sort(key=lambda e: e[0], reverse=True)
    return "\n".join(head + [l for e in ents for l in e[1]])


STAMP = re.compile(r"^(\d{6})\s+([A-Z]{1,4}\d{0,4})\s*·\s*(.+)$")


def split_stamp(text):
    """item 名字开头的「260722 JL · …」→ (右侧灰印, 真标题)。

    日期和人不该混进标题文字里（JL 260724）。抽出来单独渲染成一个淡印，
    标题只留后半句。没有前缀就原样返回。
    """
    m = STAMP.match(text.strip())
    if not m:
        return "", text
    d = m.group(1)
    stamp = (f'<span class="stmp"><span class="sd">{d[:2]}-{d[2:4]}-{d[4:]}</span>'
             f'<span class="sw {who_class(m.group(2))}">{esc(m.group(2))}</span></span>')
    return stamp, m.group(3)


def flat_rows(txt):
    """把「- 小标题 / 缩进解释」铺成扁平的一行行 <p><b>小标题</b> 解释</p>。

    给 Boundary 这种收进折叠块的短内容用 —— 折叠块里不该再套一层折叠（JL 260724）。
    """
    items, cur = [], None
    for ln in (txt or "").split("\n"):
        m = re.match(r"^[-*]\s+(.+)$", ln)
        if m:
            if cur:
                items.append(cur)
            cur = [m.group(1).strip(), []]
        elif cur is not None and ln.strip():
            cur[1].append(ln.strip())
    if cur:
        items.append(cur)
    rows = []
    for head, exp in items:
        e = " ".join(exp)
        rows.append(f'<p class="brow"><b>{inline(head)}</b>'
                    + (f' {inline(e)}' if e else "") + "</p>")
    return "".join(rows)


def mark_span(html, needle, kls):
    """把 needle（已转义的纯文字）在 html 里对应的那一段包进 <mark>，
    **哪怕这段横跨行内标签**（`代码`→<code>、**粗**→<b>）。

    做法：建一张「可见文字下标 → html 下标」的映射（跳过 <...> 里的东西），
    在可见文字里找 needle，然后在对应的 html 位置插 <mark>…</mark>。
    这样评论选中的句子即使中间夹着 <code> 也能正确描黄 —— 之前 naive 的
    `needle in html` 一遇标签就对不上，评论就「贴不到原文」了（JL 260723）。
    返回 (新 html, 是否命中)。
    """
    idx, intag, i = [], False, 0
    vis = []
    while i < len(html):
        ch = html[i]
        if ch == "<":
            intag = True
        elif ch == ">":
            intag = False
        elif not intag:
            vis.append(ch)
            idx.append(i)
        i += 1
    pos = "".join(vis).find(needle)
    if pos < 0:
        return html, False
    s, e = idx[pos], idx[pos + len(needle) - 1] + 1
    return html[:s] + f"<mark{kls}>" + html[s:e] + "</mark>" + html[e:], True


# 组标题（整行加粗）开头若写了个 emoji，就拿它当记号：**🎨 版式落地** → 🎨。
# 没写就默认 🔹。build.py 不去猜——图标随内容变，是作者写的，不是机器生成的（QA9 写法规矩）。
# 只认真 emoji 开头：中文、英文、▸(U+25B8) 都不在这些区段，不会误判成图标。
_EMO = ("\U0001F000-\U0001FAFF"      # 大部分 emoji（🔹🎨📍…）
        "\U00002600-\U000027BF"      # 杂项符号 + dingbats（✅⚠⚙…）
        "\U00002B00-\U00002BFF"      # ⭐ 等
        "\U00002190-\U000021FF"      # 箭头
        "\U00002300-\U000023FF")     # ⏰⌛ 等
GT_ICON = re.compile("^([" + _EMO + "]"
                     "[" + _EMO + "️‍\U0001F3FB-\U0001F3FF]*)"
                     r"\s+(.+)$")


LANE = re.compile(r"^>+\s*(Citation|Value|Display|Check|Q-consumer|Link|Source|Note)"
                  r"\s*[:：]\s*(.*)$", re.I)
LANE_ICON = {"citation": "📚", "value": "🔢", "display": "🖼", "check": "⚠️",
             "q-consumer": "🔎", "link": "🔗", "source": "📄", "note": "📝"}


def render_change(text):
    """One edit record's whole-sentence diff.

    The source deliberately stays tiny and readable: ``~removed~`` and
    ``*added*`` are the only two marks the editor writes.  They are not normal
    emphasis here; they are a sentence-local change record, so render them as
    deletion/addition rather than leaking the punctuation onto the page.
    """
    out = esc(text)
    out = re.sub(r"~([^~]+)~", r'<del class="chg-old">\1</del>', out)
    return re.sub(r"\*([^*]+)\*", r'<ins class="chg-new">\1</ins>', out)


def render_apparatus(lines):
    """一句话的随行装置（QA8，JL 260725）：typed `> Kind:` 行 + `> WHO:` 讨论，
    折叠在它们讨论的那一句下面。返回 (html, 头行数)。"""
    rows, heads, in_note, show = [], 0, False, False
    for ln in lines:
        m = re.match(r"^>+\s*✎\s*(.*?)\s*·\s*([A-Z]{1,4})\s*·\s*"
                     r"(\d{6}(?:\s+\d{3,4})?)\s*$", ln)
        if m:
            rows.append(f'<div class="change"><b>✎</b> {render_change(m.group(1))}'
                        f'<span class="cw"> · {esc(m.group(2))} · {esc(m.group(3))}'
                        '</span></div>')
            heads += 1
            in_note = True
            show = True
            continue
        m = LANE.match(ln)
        if m:
            kind = m.group(1).lower()
            lbl = m.group(1)[0].upper() + m.group(1)[1:].lower()
            rows.append(f'<div class="lane"><b>{LANE_ICON.get(kind, "📎")} {esc(lbl)}</b> '
                        f'{inline(m.group(2))}</div>')
            heads += 1
            in_note = False           # a typed evidence lane: chips ON
            continue
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*[「\"]([^」\"]+)[」\"]\s*[:：]\s*(.*)$", ln)
        if m:
            rows.append(f'<div class="cmt {who_class(m.group(2))}"><b>{esc(m.group(2))}</b>'
                        f'<span class="qt">「{note(m.group(3))}」</span> {note(m.group(4))}</div>')
            heads += 1
            in_note = True            # a person talking: chips OFF
            show = True
            continue
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*(\[[^\]]+\])?\s*[:：]\s*(.*)$", ln)
        if m:
            rows.append(f'<div class="cmt {who_class(m.group(2))}"><b>{esc(m.group(2))}</b> '
                        f'{note(m.group(4))}</div>')
            heads += 1
            in_note = True
            show = True
            continue
        # a continuation line inherits the mode of the lane it continues
        render = note if in_note else inline
        rows.append(f'<div class="lane-cont">{render(ln.lstrip(">").strip())}</div>')
    return "".join(rows), heads, show


DIAGRAM_MAX_LINES = 40   # a fence this long or shorter, in one of these
DIAGRAM_LANGS = {"", "text", "txt", "plain", "ascii", "diagram"}   # ...shows on stage

# ── an emoji in a figure is NOT monospace, and that is why figures looked
#    ragged (JL 260731, of QB4f's head figure: "it is very hard to read. Why?").
#    A figure is authored in a terminal, where every emoji occupies exactly TWO
#    cells, and the author aligns the columns against that. The browser breaks
#    the contract: `pre` asks for ui-monospace, the emoji falls back to the
#    system colour-emoji font, and each one lands at its own ~1.4-1.6ch. So a
#    column that is straight in the .md arrives bent on the page, differently
#    per emoji, and the reader blames the drawing.
#    The fix restores the terminal's contract at render: each emoji cluster is
#    wrapped and pinned to exactly 2ch. The SOURCE is untouched, so the figure
#    still survives being copied into chat or a mail, which is QB4b §0's rule.
#    Matched set = Emoji_Presentation=Yes (renders as emoji with no help), or
#    any character wearing U+FE0F (which is what asks for emoji presentation),
#    plus skin tones and ZWJ joins. A bare ▶ or → is deliberately NOT matched:
#    it has text presentation and already measures one cell.
_EMOJI_DEF = (
    "[\U0001F000-\U0001FAFF]"
    "|[⌚⌛⏩-⏬⏰⏳◽◾☔☕"
    "♈-♓♿⚓⚡⚪⚫⚽⚾⛄⛅"
    "⛎⛔⛪⛲⛳⛵⛺⛽✅✊✋"
    "✨❌❎❓-❕❗➕-➗➰➿"
    "⬛⬜⭐⭕]"
)
_EMOJI_TEXT = "[©®‼⁉™ℹ↔-↪⏏" \
              "⏭-⏯⏱⏲⏸-⏺Ⓜ▪-◼" \
              "☀-☄☎☑☘☝☠☢☣☦" \
              "☪☮☯☸-☺♀♂♟♠♣" \
              "♥♦♨♻♾⚒⚔-⚗⚙" \
              "⚛⚜⚠⚧⚰⚱⛈⛏⛑⛓" \
              "⛩⛰⛱⛴⛷-⛹✂✈✉" \
              "✌✍✏✒✔✖✝✡✳✴" \
              "❄❇❣❤➡⤴⤵⬅-⬇" \
              "〰〽㊗㊙]️"
_EMOJI_ONE = f"(?:(?:{_EMOJI_DEF})️?|(?:{_EMOJI_TEXT}))[\U0001F3FB-\U0001F3FF]?"
EMOJI = re.compile(f"(?:{_EMOJI_ONE})(?:‍(?:{_EMOJI_ONE}))*")


def pad_emoji(html):
    """Pin every emoji in a FIGURE to two monospace cells.

    Applied only to ascii figures, never to a language-tagged code listing,
    where an emoji inside a string is somebody else's source and must arrive
    byte-shaped. Runs on already-escaped html; the pattern matches only emoji
    codepoints, so it can never touch a tag or an entity."""
    return EMOJI.sub(lambda m: f'<span class="eu">{m.group(0)}</span>', html)


def body(txt, fold_code=True, apparatus=True):
    """paragraphs + ``` blocks + comment lanes + topic/explanation bullets -> html

    An `<!-- ... -->` block is dropped, everywhere, not rendered as escaped text.
    `ref/q-template.md` has always told authors a comment "is dropped at
    generation either way", and that was only true where nobody looked: the sole
    strip lived in the Stage Contract path, and the template's own comments
    happen to sit outside any rendered section. Written anywhere else the comment
    came out as visible `&lt;!--` prose (found 260726 while making the ＋ button's
    stub name its optional sections). Notes to the author now behave the way the
    template promised.

    要点式排版（JL 260723）：一行 `- 小标题`，下面缩进两格的行是它的解释。
        - 选中就能评论
          光标下冒出「💬 Comment」，点它填字保存。
          保存的瞬间那句话变黄底高亮。
    比一段接一段的散句好扫。`- [ ]` 是勾选清单，不走这条路。

    fold_code=True（默认）：``` 代码块也收进 <details>，默认合着、想看再点开（JL 260723），
    跟节标题的 expand-all 联动。传 False 才铺开（`## Diagram` 那张招牌图就用它）。
    """
    out, fence, blt, lg, flang = [], None, None, None, ""
    ifence = None    # 缩进在 item 下的 ``` 块：收进这个 item 的折叠区（JL 260724）
    last_p, appar = None, {}   # 最近一句正文的 out 下标 → 它收集到的 `>` 装置行（QA8）
    para_head = False          # 上一行是不是 #### 段落标题（决定紧跟的 (…) 是不是它的活儿）

    def flush():
        """把攒着的要点 / 勾选项吐出来。两者共用「小标题 + 缩进解释」这套结构。"""
        nonlocal blt, last_p
        if blt is None:
            return
        last_p = None
        kind, top, det, on = blt
        name_cls = "ct" if kind == "ck" else "bt"
        # item = 名字 + 解释。名字永远在台面上；有解释时把它收进 native <details>，
        # 想看再点开 —— 纯 CSS，零脚本（JL 260723）。没解释就是一行光名字。
        # 名字开头的「260722 JL ·」抽成右侧灰印，标题只留后半句（JL 260724）。
        stamp, title = split_stamp(top)
        # 标题开头写个 emoji 就当图标（跟组标题一个规矩，作者写、机器不猜）。
        im = GT_ICON.match(title)
        icon = f'<span class="ti">{im.group(1)}</span>' if im else ""
        if im:
            title = im.group(2).strip()
        if det:
            # 「click the row」，收干净（JL 260724）：台面上只留标题（图标+灰印+caret）；
            #   一句话摘要和长解释【都】藏起来，点这一整行才铺开。
            #   摘要是解释的第一段（.ld，深一档），其余段落淡一档，展开后一眼分层。
            head = (f'<div class="{name_cls} nof">{icon}'
                    f'<span class="ttl">{inline(title)}</span>'
                    f'{stamp}<span class="cv"></span></div>')
            parts, lead = [], True
            for x in det:
                if isinstance(x, tuple):   # ("pre", lines): 折叠区里的 ascii 图
                    parts.append('<pre class="ip">'
                                 f'{pad_emoji(link_faces(esc(chr(10).join(x[1]))))}</pre>')
                elif lead:
                    parts.append(f'<p class="ld">{inline(x)}</p>')
                    lead = False
                else:
                    parts.append(f'<p>{inline(x)}</p>')
            exp = "".join(parts)
            item = (f'<details class="it row"><summary>{head}</summary>'
                    f'<div class="bd">{exp}</div></details>')
        else:
            item = (f'<div class="{name_cls} nod">{icon}'
                    f'<span class="ttl">{inline(title)}</span>{stamp}</div>')
        if kind == "ck":
            out.append(f'<div class="ck{" on" if on else ""}">'
                       f'<span class="bx">{"☑" if on else "☐"}</span>'
                       f'<div class="itw">{item}</div></div>')
        else:
            out.append(f'<div class="blt">{item}</div>')
        blt = None

    for ln in (txt or "").split("\n"):
        # A `<!-- haipipe:… -->` MACHINE MARKER never reaches the page (JL
        # 260726, seeing six of them printed on the first generated skill page).
        # `parse.strip_notes` keeps them on purpose, because the file is where
        # stage.py and skillpage.py find their managed spans; but a marker is
        # addressed to a script, and a reader has no use for it. Dropped here,
        # at render, so the file keeps its markers and the page never shows one.
        if ln.lstrip().startswith("<!--") and "haipipe:" in ln and ln.rstrip().endswith("-->"):
            continue
        # 缩进的 ``` 属于当前 item：ascii 收进它的折叠区（JL 260724 QC10）。
        # 顶格的 ``` 照旧 flush 成兄弟块 —— 台面只放标题，图藏在点开之后。
        if ifence is not None:
            if ln.strip().startswith("```"):
                pad = min((len(x) - len(x.lstrip()) for x in ifence if x.strip()),
                          default=0)
                blt[2].append(("pre", [x[pad:] if x.strip() else "" for x in ifence]))
                ifence = None
            else:
                ifence.append(ln)
            continue
        if blt is not None and re.match(r"^\s{2,}```", ln):
            ifence = []
            continue
        if ln.lstrip().startswith("```"):
            flush()
            if fence is None:
                fence = []
                flang = ln.lstrip()[3:].strip()
            else:
                code = esc(chr(10).join(fence))
                # Only a FIGURE gets travelling ids. A language-tagged code
                # fence is quoted source, where `QA1` is a string in someone
                # else's program, not a place on this board.
                if flang.lower() in DIAGRAM_LANGS:
                    code = pad_emoji(link_faces(code))
                # An UNTAGGED short fence is an ascii diagram, not code: it is the
                # picture the sentence above is making, and hiding it behind
                # "</> code · 4 lines" costs a click to see the thing you came for
                # (JL 260726). Fold real code (language-tagged) and long blocks only.
                is_diagram = (flang.lower() in DIAGRAM_LANGS
                              and len(fence) <= DIAGRAM_MAX_LINES)
                if fold_code and not is_diagram:
                    lab = ('&lt;/&gt; code'
                           + (f' · {esc(flang)}' if flang else '')
                           + f' · {len(fence)} lines')
                    out.append(f'<details class="it codef"><summary class="cs">{lab}'
                               f'</summary><pre>{code}</pre></details>')
                else:
                    out.append(f'<pre{" class=" + chr(34) + "asc" + chr(34) if is_diagram else ""}>'
                               f'{code}</pre>')
                fence = None
                last_p = None
            continue
        if fence is not None:
            fence.append(ln)
            continue
        # (fenced block accumulates verbatim; flushed on the closing ```)
        if blt is not None and re.match(r"^\s{2,}\S", ln):
            blt[2].append(ln.strip())
            continue
        if lg is not None and re.match(r"^\s{2,}\S", ln):   # Log 条目的续行
            out[lg] = out[lg].replace("</span></div>",
                                      " " + inline(ln.strip()) + "</span></div>")
            continue
        lg = None
        m = re.match(r"^[-*]\s+(?!\[[ xX]\])(.+)$", ln)
        if m:
            flush()
            last_p = None
            blt = ["blt", m.group(1).strip(), [], False]
            continue
        flush()
        if not ln.strip():
            continue
        # 句子随行装置（QA8，JL 260725）：紧跟在一句正文后面的 `>` 行
        # （> Citation: / > Value: / > Check: / > JL: …，可隔空行）收进那一句的
        # 抽屉；句尾挂 ⚑N，点开才现。没有前一句的 `>` 行照旧渲染。
        if apparatus and ln.lstrip().startswith(">") and last_p is not None:
            appar.setdefault(last_p, []).append(ln.strip())
            continue
        # 260723 0940 · 改了什么      （时间可省，省了就只显示日期）
        m = re.match(r"^(\d{6})(?:\s+(\d{3,4}))?\s*[·|]\s*(.*)$", ln)
        if m:
            d, hm = m.group(1), m.group(2)
            stamp = f"{d[:2]}-{d[2:4]}-{d[4:]}"
            if hm:
                hm = hm.zfill(4)
                stamp += f" {hm[:2]}:{hm[2:]}"
            out.append(f'<div class="lg"><span class="d">{stamp}</span>'
                       f'<span>{inline(m.group(3))}</span></div>')
            lg = len(out) - 1
            last_p = None
            continue
        m = re.match(r"^\s*[-*]\s*\[([ xX])\]\s*(.*)$", ln)   # - [ ] / - [x]
        if m:
            flush()
            last_p = None
            blt = ["ck", m.group(2), [], m.group(1).lower() == "x"]
            continue
        # ![[path]] / ![[path#Section]]（QF1，JL 260724）：把另一份文件的内容按
        # 【引用】嵌进这一题 —— 生成时现读，零拷贝零漂移。板永远不学源文件的方言：
        # page_stage.render_doc 是通用渲染。嵌不到会就地标红，绝不悄悄空掉。
        m = EMBED.match(ln)
        if m:
            flush()
            out.append(embed_block(m.group(1).strip(), m.group(2), m.group(3)))
            last_p = None
            continue
        # 一行只放一个 excalidraw 分享链接 → 嵌成一块可交互画布，底下再给一条链接。
        # 为什么敢嵌：excalidraw.com 没有 X-Frame-Options / frame-ancestors（实测）。
        # 为什么还要那条链接：断网 / iframe 被拦时，画布是空的，链接仍然点得开 —— 不靠 iframe 才读得到。
        # A self-hosted Excalidraw is embedded on the same terms as the hosted one.
        # The host is not guessable, so board.md declares it once (`excalidraw:`)
        # and every page composes its own `#url=` off it: declare once, compose
        # per page, which is the identity rule this board keeps relearning.
        m = re.match(r"^\s*(https?://(?:app\.)?excalidraw\.com/\S+)\s*$", ln)
        ours = False
        if not m and EXCAL_HOST:
            m = re.match(r"^\s*(" + re.escape(EXCAL_HOST) + r"/\S+)\s*$", ln)
            ours = bool(m)
        if m:
            u = esc(m.group(1))
            # READ here, EDIT in a tab, but ONLY for a scene we serve. A board
            # carries one iframe per page and they share an origin, so an
            # editable embed would have every page writing the same browser
            # storage and reading back somebody else's drawing. ✏️ Edit opens
            # the one tab that writes, and what it writes is the file every
            # page reads (QA4a).
            #
            # A pasted app.excalidraw.com link is still a first-class thing to
            # put here (QD7) and it gets the plain link it always had: there is
            # no frame in it to edit, `edit=1` would mean nothing to that app,
            # and the save loop lives on our origin, not theirs.
            if ours:
                ed, label = (u + ("&amp;" if "?" in u else "?") + "edit=1",
                             "✏️ Edit this frame")
            else:
                ed, label = u, "↗ Open in Excalidraw"
            out.append(f'<div class="xcal"><iframe src="{u}" loading="lazy" '
                       f'referrerpolicy="no-referrer"></iframe>'
                       f'<a class="fp xopen" href="{ed}" target="_blank" rel="noopener">'
                       f'{label}</a>'
                       f'<code class="xurl">{u}</code></div>')
            last_p = None
            continue
        # ### inside a NON-Content section = a subsection heading (`### Decision
        # Now` in Where we are is the canonical case, JL 260731). Content never
        # reaches here at this level: its ### lines were split into divisions
        # before body() ran. Without this rule the line rendered as literal
        # "### …" prose. `.sh` is also the anchor the sidebar outline scrolls to.
        m = re.match(r"^###\s+(.+?)\s*$", ln)
        if m:
            out.append(f'<div class="sh">{inline(m.group(1))}</div>')
            last_p = None
            continue
        # #### = 段落标题（一节里的一个 ¶）。以前被压成 **…**，于是套上了组标题的
        # 🔹，把「一个段落」说成了「领一串 item 的一句话」（JL 260725）。现在它是
        # 自己的层级：没有图标，比组标题小，紧跟其后的整行括号是这一段的活儿。
        m = re.match(r"^#{4,6}\s+(.+?)\s*$", ln)
        if m:
            out.append(f'<div class="ph">{inline(m.group(1))}</div>')
            last_p = None
            para_head = True
            continue
        # 段落标题后面紧跟的整行 (…) 是这一段要干的活：留在页面上（它是扫读用的），
        # 但排成灰斜体，跟正文分开（JL 260725）。只认紧跟标题的那一行。
        if para_head and re.match(r"^\(.+\)\s*$", ln):
            out.append(f'<div class="pj">{inline(ln.strip()[1:-1].strip())}</div>')
            last_p = None
            para_head = False
            continue
        para_head = False
        # 整行加粗 = 组标题：领着下面一串 item 的一句话。图标 + 略大 + 上间距，
        # 夹在节标题(.ch)和 item 名字(.bt)中间一层，把层级拉开（JL 260723）。
        # 只认「整行都在 **…** 里」的（内部不含 **），混排的加粗照旧走 <p>。
        # 图标随内容变：加粗开头写个 emoji 就用它（GT_ICON），没写用默认 🔹。
        m = re.match(r"^\*\*((?:(?!\*\*).)+)\*\*\s*$", ln)
        if m:
            inner = m.group(1).strip()
            im = GT_ICON.match(inner)
            icon, txt = (im.group(1), im.group(2).strip()) if im else ("🔹", inner)
            out.append(f'<div class="gt"><span class="gi">{icon}</span>{inline(txt)}</div>')
            last_p = None
            continue
        # > JL 「被选中的原句」: 评论    ← 行内评论；引号里那段会在正文里高亮
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*[「\"]([^」\"]+)[」\"]\s*[:：]\s*(.*)$", ln)
        if m:
            who = m.group(2)
            k = who_class(who)
            out.append(f'<div class="cmt {k}"><b>{esc(who)}</b>'
                       f'<span class="qt">「{note(m.group(3))}」</span> {note(m.group(4))}</div>')
            last_p = None
            continue
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*(\[[^\]]+\])?\s*[:：]\s*(.*)$", ln)
        if m:
            who = m.group(2)
            k = who_class(who)
            out.append(f'<div class="cmt {k}"><b>{esc(who)}</b> {note(m.group(4))}</div>')
            last_p = None
        else:
            out.append(f"<p>{inline(ln)}</p>")
            last_p = len(out) - 1
    flush()
    # 把收集到的装置行折进各自的句子（native <details>，零脚本不变量成立）
    for idx, lines in appar.items():
        inner, heads, show = render_apparatus(lines)
        # 句尾挂 ⚑N：徽标塞进一个 0 宽的行内块（.sbz），断行时当它不存在，
        # 因此永远不可能被推到下一行（JL 260731 两次：先是徽标单独落一行，
        # 后是「词 + 徽标」整团落一行，同样扎眼）。它挂在句末最后一个字符右侧，
        # 该行已满时越界画进右侧留白，读起来仍然是句尾。
        summary = _hang_badge(out[idx], f'<span class="sbadge">⚑ {heads}</span>')
        out[idx] = ('<details class="sent"' + (' open' if show else '') + '><summary>' + summary
                    + '</summary>'
                    f'<div class="sapp">{inner}</div></details>')
    return "\n".join(out)


def _hang_badge(p_html, badge):
    """把 ⚑ 徽标挂在句尾，且不占任何排版宽度，因此绝不可能自己另起一行。

    徽标裹进 `.sbz`（inline-block，width:0，overflow 可见）：浏览器断行时按
    「徽标不存在」来算，句子怎么排都和没有徽标时一样；徽标从最后一个字符右侧
    画出去，行尾没地方时越界到右侧留白里。紧贴最后一个字符插入（前面不留空白）
    是关键 —— 有空白就有断行机会，徽标就又可能被推到下一行。
    """
    hung = f'<span class="sbz">{badge}</span>'
    if p_html.startswith("<p>") and p_html.endswith("</p>"):
        return "<p>" + p_html[3:-4].rstrip() + hung + "</p>"
    return p_html.rstrip() + hung
