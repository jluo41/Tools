"""Prose into TeX: escaping, code spans, display placeholders, fences, the section title and keywords."""

import pathlib
import re

REF = re.compile(r"\\(?:auto|C|c)?ref\{((?:tab|fig):[^}]*)\}")
LEVEL = ("section", "subsection", "subsubsection")


def strip_number(title):
    """`2.1 Study Setting` -> `Study Setting`.

    LaTeX numbers its own sections; carrying the number in the title too gives
    "2.1 2.1 Study Setting" in the compiled PDF. A board division
    writes `1 · The contract`, so the separator dot goes with the number:
    leaving it produced `\\section{· The contract}` (JL 260815, on QPf6).
    """
    return re.sub(r"^\d+(?:\.\d+)*\s*(?:·\s*)?", "", title).strip()


SECTION_TITLE = re.compile(r"(?m)^section_title:\s*(.+?)\s*$")
# A caption or group title: `**Name**: what this shows.` on its own line. It is
# SCAFFOLDING, exactly like the `(job)` line under a ####, and it usually
# captions a fenced sketch that was already dropped. It reached the .tex as
# literal `**bold**`, which LaTeX renders as asterisks around the words.
GROUP_TITLE = re.compile(r"^\*\*[^*]+\*\*\s*[:：]")
# A division's own summary line, `<emoji> Establishes …`. It tells a BOARD
# reader what the division is for, which a paper's reader learns from the prose
# itself. Same class as the group title above: scaffolding, not manuscript.
ESTABLISHES = re.compile(r"^\W*\s*Establishes\b")
# Inline code is markdown's, not LaTeX's: `x` reached the .tex as literal
# backticks around the word.
CODE_SPAN = re.compile(r"`([^`]+)`")

# The working Page keeps unresolved displays in the stable
# `\table{D_xxx}` / `\figure{D_xxx}` / `\algorithm{D_xxx}` form. These are
# Page bindings, not native LaTeX commands; delivery renders an unbound token
# as a legible pending note. The slash spelling remains a migration alias.
DISPLAY_PLACEHOLDER = re.compile(
    r"(?:\\|/)(table|figure|algorithm)\s*\{\s*([^}]+?)\s*\}"
)

# Task Pages carry a small reader-facing status tail after their manuscript
# content. It belongs on the Board Page, not in a paper export. Likewise, the
# reading anchor is HTML apparatus rather than prose.
EXPORT_SCAFFOLD = re.compile(r"^(?:answers\b|not\s+answered\b|next\s+run\b)",
                             re.I)

# A percentage in board prose ("26% of the headline cohort") reached raw LaTeX
# as a live comment character: `%` and everything after it on the line vanished
# from the compiled PDF with no error, no warning, just a shorter sentence
# (found 260820 on QC3-visitheadache, where "N = 200,517 is 26% of..." printed
# as "N = 200,517 is 26"). code_span_tex (below) escapes `%` `&` `#` `$` `_`
# `~` `^` inside backtick spans only; PLAIN prose text never passed through any
# escape at all. `$` is left alone deliberately: board prose does not use TeX
# math, and an accidental `$` (a real dollar figure) is rarer than the display
# damage a stray unmatched `$` would cause by opening math mode. `~` is TeX's
# non-breaking space, so "conventional ~16.4 rule of thumb" silently dropped
# its own tilde and printed "conventional 16.4" (same 260820 QC3 find).
_PLAIN_SPECIALS = [("%", "\\%"), ("&", "\\&"), ("#", "\\#"),
                    ("~", "\\textasciitilde{}"), ("_", "\\_")]


def escape_prose(s):
    """Escape TeX specials in board prose OUTSIDE backtick code spans, so a
    literal `%`, `&` or `#` a person typed renders instead of truncating or
    misparsing the sentence. Backtick spans are left untouched here because
    `code_span_tex` (below) already escapes their own content in full."""
    # An underscore in prose (`action_name`, `column_inventory.csv`) is a literal; unescaped,
    # TeX read it as a math subscript and ran the sentence off the page (JL 261004). Math
    # spans (`$x_1$`), code spans and a command's argument (`\\citep{key_a}`) keep their own
    # rules, so all three stay untouched here.
    # A display equation ($$ ... $$) is math too (JL 261104: both of a paper's regression equations printed "Y\\_ijc").
    parts = re.split(r"(`[^`]*`|\$\$.+?\$\$|\$[^$\n]+\$|\\[A-Za-z]+\*?(?:\[[^\]]*\])*\{[^}]*\})", s, flags=re.S)
    for i in range(0, len(parts), 2):
        for a, b in _PLAIN_SPECIALS:
            parts[i] = re.sub(
                r"(?<!\\)" + re.escape(a),
                lambda _match, value=b: value,
                parts[i],
            )
    return "".join(parts)


def display_placeholder_tex(m):
    noun = m.group(1).capitalize()
    label = m.group(2).strip().replace("_", r"\_")
    return r"\textit{[%s pending: %s]}" % (noun, label)


def render_prose(s):
    """Keep unresolved display placeholders readable in delivery output."""
    parts = re.split(r"(`[^`]*`)", s)
    for i in range(0, len(parts), 2):
        parts[i] = DISPLAY_PLACEHOLDER.sub(display_placeholder_tex, parts[i])
    return escape_prose("".join(parts))

# What a code span QUOTES must never EXECUTE: `\citep` inside \texttt{} ran the
# macro and printed "[]" in QPf6's compiled PDF (JL 260815). Backslash first,
# then TeX's other specials; the placeholder keeps the escaped backslash's own
# braces out of the second pass.
_TEX_SPECIALS = [("\\", "\x00BS\x00"), ("{", "\\{"), ("}", "\\}"),
                 ("\x00BS\x00", "\\textbackslash{}"),
                 ("&", "\\&"), ("%", "\\%"), ("$", "\\$"), ("#", "\\#"),
                 ("_", "\\_"), ("~", "\\textasciitilde{}"),
                 ("^", "\\textasciicircum{}")]


# A code span with no space is one TeX "word": LaTeX only breaks lines at
# glue (spaces) or hyphenation points, never inside a bare \texttt run, so a
# long identifier with no internal space runs off the page margin instead of
# wrapping (QC5-visitt2d 260820: `run-6/7-VisitT2D_1stPair_{...}-*.do`, 81
# chars, physical page 2 cut off mid-word). \seqsplit makes every character a
# legal break point; reserved for spans actually at risk, since it also
# breaks short spans awkwardly at any width.
_SEQSPLIT_MIN = 40


def code_span_tex(m):
    s = m.group(1)
    needs_seqsplit = len(s) >= _SEQSPLIT_MIN and " " not in s
    for a, b in _TEX_SPECIALS:
        s = s.replace(a, b)
    if needs_seqsplit:
        return "\\texttt{\\seqsplit{%s}}" % s
    return "\\texttt{%s}" % s


# LaTeX text fonts may lack the box glyphs and emoji a board sketch leans on; a
# verbatim block full of .notdef blanks reads worse than plain ASCII. So a kept
# fence is transliterated: box drawing to +-| art, arrows to ASCII, and any
# glyph still outside Latin-1 dropped.
_FENCE_MAP = str.maketrans({"─": "-", "━": "-", "│": "|", "┌": "+", "┐": "+",
                            "└": "+", "┘": "+", "├": "+", "┤": "+", "┬": "+",
                            "┴": "+", "┼": "+", "▶": ">", "◀": "<", "·": ".",
                            "—": "-", "…": "...", "§": "S"})

# A glyph PROSE points at may not die silently: with 🅰 dropped, "🅰 lost the
# way…" fused onto the sentence before it and read as gibberish, and the
# figure's two candidates lost their names (JL 260815, the QPf3 comparison).
# Reference-bearing glyphs get a textual body, in FENCES and PROSE alike;
# decorative emoji still fall out, because a page of [🔥][📦] is not a paper.
_BADGE = {"🅰": "[A]", "🅱": "[B]", "🅲": "[C]", "🅳": "[D]",
          "✅": "[x]", "⬜": "[ ]", "⭐": "*", "🛑": "[!]"}
_BADGE.update({chr(0x2460 + i): "(%d)" % (i + 1) for i in range(20)})  # ①…⑳


def badge_sub(s):
    for a, b in _BADGE.items():
        if a in s:
            s = s.replace(a, b)
    return s


def fence_verbatim(rows):
    out = []
    for r in rows:
        r = badge_sub(r).translate(_FENCE_MAP)
        r = "".join(c for c in r if ord(c) < 256)
        out.append(r.rstrip())
    while out and not out[-1]:
        out.pop()
    return "\\begin{verbatim}\n%s\n\\end{verbatim}\n" % "\n".join(out)


def section_title_of(page):
    """The name this page's `\\section{}` takes, if the page declares one.

    The page TITLE has two readers with different needs: a board reader wants
    to know what kind of page it is, and LaTeX wants the section's real name.
    Making one string serve both produced `\\section{page-type SECTION · owns
    ONE FLAT .tex ...}`. The head key lets each have its own.
    """
    head = pathlib.Path(page).read_text(encoding="utf-8", errors="ignore")[:1500]
    m = SECTION_TITLE.search(head)
    return m.group(1) if m else None


def keywords_text_of(page):
    """Return reader prose from an optional ``### Keywords`` division.

    ``md2docx.parse_page`` deliberately drops unnumbered working headings, so
    the Keywords heading itself is absent from its shared block stream.  The
    prose still arrives, previously joining the final abstract sentence in the
    LaTeX projection.  Read this one manuscript metadata division by name so
    the LaTeX writer can restore its conventional inline label and spacing.
    """
    raw = pathlib.Path(page).read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    lines = raw.splitlines()
    in_content = False
    in_keywords = False
    kept = []
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped == "## Content":
            in_content = True
            continue
        if in_content and stripped.startswith("## "):
            break
        if not in_content:
            continue
        if stripped.startswith("### "):
            in_keywords = stripped[4:].strip() == "Keywords"
            continue
        if not in_keywords or not stripped:
            continue
        if stripped.startswith(("#### ", ">", "(", "```")):
            continue
        kept.append(re.sub(r"^[-*]\s+", "", stripped))
    return " ".join(kept).strip()


CONTENT_FORMAT = re.compile(r"(?m)^content-format:\s*(\S+)\s*$")


def content_format_of(page):
    """The Page head's `content-format:` (`markdown` when absent).

    `latex` says the Draft sentences ARE LaTeX source: a paper Section migrated
    from a manuscript keeps its floats, equations and lists as written, so the
    LaTeX lane must pass them through instead of escaping them as prose."""
    raw = pathlib.Path(page).read_text(encoding="utf-8", errors="ignore")
    m = CONTENT_FORMAT.search(raw.split("\n## ", 1)[0])
    return m.group(1).lower() if m else "markdown"
