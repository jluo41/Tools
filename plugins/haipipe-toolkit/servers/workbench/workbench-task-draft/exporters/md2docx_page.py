"""Parsing a Page into its sections, with LaTeX content turned into Markdown first."""

import re
from md2docx_layout import (
    ABSTRACT_DIVISIONS, DISCUSSION_LANES, EVIDENCE_LANES, SKIP_DIVISIONS, WORKING_LANES, abstract_label,
    is_abstract_page, is_manuscript_heading,
)

# --------------------------------------------------------------- page parse

# A Page whose head says `content-format: latex` keeps LaTeX source in Content
# (a Section migrated from a manuscript). Word has no LaTeX, so its lines are
# turned into the Markdown this reader already knows before it reads them:
# markup to **bold** / *italic* / `code`, math symbols to characters, a float
# to one italic line naming it, a list item to a bullet line. \cite and \ref
# stay as they are; the Inline resolver below handles them.
_TEX_SYMBOLS = {"sim": "∼", "times": "×", "approx": "≈", "geq": "≥", "ge": "≥", "leq": "≤",
                "le": "≤", "Delta": "Δ", "delta": "δ", "pm": "±", "sigma": "σ", "mu": "μ",
                "alpha": "α", "beta": "β", "gamma": "γ", "lambda": "λ", "in": "∈", "mid": "|",
                "cdot": "·", "quad": " ", "qquad": " ", "infty": "∞", "neq": "≠", "to": "→",
                "rightarrow": "→", "sum": "Σ", "log": "log", "min": "min", "max": "max",
                "ldots": "…", "dots": "…", "hat": "", "sqrt": "√", "lvert": "|", "rvert": "|"}
_KEEP = re.compile(r"\\(?:cite[a-z]*|(?:auto|C|c)?ref)\*?(?:\[[^\]]*\])*\{[^}]*\}")


def content_format(raw_page):
    m = re.search(r"(?m)^content-format:\s*(\S+)\s*$", raw_page.split("\n## ", 1)[0])
    return m.group(1).lower() if m else "markdown"


def _unwrap(text, command, left="", right=""):
    """`\\command{...}` -> left + ... + right, braces matched."""
    token = "\\" + command + "{"
    while token in text:
        i = text.index(token)
        k, depth = i + len(token), 1
        while k < len(text) and depth:
            depth += (text[k] == "{") - (text[k] == "}")
            k += 1
        text = text[:i] + left + text[i + len(token):k - 1] + right + text[k:]
    return text


def _tex_math(body):
    for command in ("text", "mathrm", "mathbf", "operatorname"):
        body = _unwrap(body, command)
    body = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", body)
    body = re.sub(r"\\([A-Za-z]+)", lambda m: _TEX_SYMBOLS.get(m.group(1), m.group(1)), body)
    body = re.sub(r"([_^])\{([^{}]*)\}", r"\1\2", body)
    return body.replace("{", "").replace("}", "").replace("\\", "")


def tex_inline_md(s):
    """One LaTeX source line -> the Markdown this reader renders."""
    kept = []
    s = _KEEP.sub(lambda m: kept.append(m.group(0)) or "\x00%d\x00" % (len(kept) - 1), s)
    s = re.sub(r"\$([^$]*)\$", lambda m: _tex_math(m.group(1)), s)
    s = re.sub(r"\\paragraph\*?\{([^{}]*)\}", r"**\1**", s)
    for command, left, right in (("textbf", "**", "**"), ("emph", "", ""), ("textit", "", ""),
                                 ("texttt", "`", "`"), ("underline", "", ""), ("url", "", ""),
                                 ("textsuperscript", "", ""), ("text", "", "")):
        s = _unwrap(s, command, left, right)
    for old, new in (("{,}", ","), ("\\,", " "), ("\\ ", " "), ("~", " "), ("---", "—"), ("--", "–"),
                     ("\\%", "%"), ("\\&", "&"), ("\\_", "_"), ("\\#", "#"), ('\\"i', "ï"),
                     ('\\"o', "ö"), ('\\"u', "ü"), ('\\"a', "ä"), ("\\'e", "é"), ("``", '"'), ("''", '"')):
        s = s.replace(old, new)
    s = re.sub(r"\\(?:noindent|centering|small|footnotesize|hfill|par|clearpage|newpage)\b\s*", "", s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\\([A-Za-z]+)", lambda m: _TEX_SYMBOLS.get(m.group(1), ""), s)
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], s)
    return " ".join(s.split())


def latex_content_to_markdown(lines):
    """Content lines of a `content-format: latex` Page -> Markdown lines."""
    out, i = [], 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        i += 1
        if not s or s.startswith(("#", ">")):
            out.append(raw)
            continue
        m = re.match(r"^\\begin\{([^}]+)\}", s)
        if m and m.group(1) != "abstract":
            env, block, depth = m.group(1), [s], s.count("\\begin{%s}" % m.group(1)) - s.count("\\end{%s}" % m.group(1))
            while depth > 0 and i < len(lines):
                block.append(lines[i].strip())
                depth += lines[i].count("\\begin{%s}" % env) - lines[i].count("\\end{%s}" % env)
                i += 1
            text = " ".join(block)
            if env.rstrip("*") in ("figure", "table"):
                cap = re.search(r"\\caption\{", text)
                caption = ""
                if cap:
                    k, depth = cap.end(), 1
                    while k < len(text) and depth:
                        depth += (text[k] == "{") - (text[k] == "}")
                        k += 1
                    caption = tex_inline_md(text[cap.end():k - 1])
                noun = "Table" if env.startswith("table") else "Figure"
                out.append("*[%s: %s]*" % (noun, caption or "see the PDF"))
            elif env in ("itemize", "enumerate", "description"):
                for item in re.split(r"\\item\b", text)[1:]:
                    item = re.sub(r"\\end\{%s\}.*$" % re.escape(env), "", item)
                    out.append("• " + tex_inline_md(item))
            else:
                inner = re.sub(r"\\(?:begin|end)\{[^}]+\}(?:\[[^\]]*\])?", " ", text)
                out.append(tex_inline_md(inner))
            continue
        if re.match(r"^\\(?:sub)*section\*?\{|^\\(?:begin|end)\{abstract\}|^\\(?:clearpage|newpage|vspace)", s):
            continue
        if s.startswith("\\input{"):
            out.append("*[Table: %s]*" % s[7:].rstrip("}").split("/")[-1])
            continue
        if s.startswith("\\keywords{"):
            words = _unwrap(s, "keywords").replace("\\and", "·")
            out.append("**Keywords:** " + " ".join(words.split()))
            continue
        line = tex_inline_md(s)
        if line:
            out.append(line)
    return out


def parse_page(path, keep_fences=False):
    """Return the blocks of `## Content`, dropping what QC5's read-and-drop
    table drops. A `>` lane binds to the paragraph ABOVE it, which is QC0's
    adjacency law.

    `keep_fences` is the BOARD exporter's switch (JL 260815: a board page's
    figure-only division exported as an empty section). A paper still drops
    sketches, because its figures are display units; a board page's sketch IS
    the content, so the board asks for `("fence", text)` blocks instead."""
    with open(path, encoding="utf-8", errors="replace") as source:
        raw_page = source.read()
    # HTML comments are invisible Markdown apparatus. Stable Bullet-address
    # receipts such as ``<!-- realizes: C1.P1.B1 -->`` must remain available
    # to Board checks without leaking into either Word or LaTeX prose.
    raw_page = re.sub(r"<!--.*?-->", "", raw_page, flags=re.S)
    lines = raw_page.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "## Content")
    except StopIteration:
        raise SystemExit(f"{path}: no ## Content section")
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("## ")), len(lines))

    # SIX OF THE NINE SECTIONS DECLARE NO SECTION TITLE in ## Content: they open
    # at `### §2.1`, so the manuscript had a 2.1 with no 2 above it (JL 260727).
    # The title exists, on the page's own `# S Main 2 · §2 Literature Review`
    # line, which is canonical. Derived from there and emitted first, and only
    # when Content carries no level-1 heading of its own, so a page that does
    # declare one (§1, §8, the abstract) is untouched.
    page_title = ""
    for l in lines[:6]:
        if l.startswith("# "):
            page_title = l[2:].split("\u00b7")[-1].strip().lstrip("\u00a7").strip()
            break
    own_h1 = any(re.match(r"^### (?:\u00a7\s*)?\d+\s", l) or
                 l.strip() in ("### Abstract",)
                 for l in lines[start + 1:end])

    blocks, skipping, prev_was_para = [], False, False
    # An Insight answering Page (folder-kind data, information, knowledge or wisdom) numbers
    # its subsections `#### 1.1 · …` and states lists as pipe tables; both are its content,
    # not a manuscript paragraph's working label (JL 261004: Insight pages export to LaTeX
    # and Word). Every other Page keeps the manuscript rules below, byte for byte.
    insight = bool(re.search(r"(?m)^folder-kind:\s*(data|information|knowledge|wisdom)\s*$",
                             raw_page.split("\n## ", 1)[0]))
    abstract = is_abstract_page(raw_page)
    if page_title and not own_h1:
        blocks.append(("h", 1, page_title))
    in_fence, fenced = False, 0
    body = lines[start + 1:end]
    if content_format(raw_page) == "latex":
        body = latex_content_to_markdown(body)
    for raw in body:
        line = raw.rstrip()
        # A ``` fence inside ## Content is an ASCII SKETCH: a hand-drawn table, a
        # structure outline, a form block. It is not prose, and shipping it to a
        # reader produced a literal ASCII bar chart with its fence marks in the
        # middle of §4 (JL found it 2026-07-27). Skipped, and counted, because a
        # silent drop is worse: the sketch is usually a display unit that has not
        # been built yet, and the reader should learn that from a report rather
        # than from a missing table.
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            if in_fence:
                fenced += 1
                if keep_fences:
                    blocks.append(("fence", []))
            continue
        if in_fence:
            if keep_fences:
                blocks[-1][1].append(line)
            continue
        s = line.strip()

        if s.startswith("### "):
            # The § is BOARD notation for "this is section N of the manuscript".
            # MISQ's heading contract is `1 MAJOR HEAD` / `1.1 First Subhead`,
            # so the sigil is stripped on the way out (JL 2026-07-27). A heading
            # that was ONLY a § carries no title and is dropped.
            title = s[4:].strip().lstrip("\u00a7").strip()
            if not title:
                prev_was_para = False
                continue
            skipping = any(title.startswith(x) for x in SKIP_DIVISIONS)
            if not skipping and not is_manuscript_heading(title) \
                    and not (abstract and title in ABSTRACT_DIVISIONS):
                # working structure, not a manuscript division: its PROSE, if it
                # has any, still belongs to the section, so do not set `skipping`
                prev_was_para = False
                continue
            if not skipping:
                # MISQ's contract is three LEVELS, and the number says which:
                #   1      MAJOR HEAD    bold, ALL CAPS, centered
                #   1.1    First Subhead bold, title case, centered
                #   1.1.1  Second        bold, title case, flush left
                # Everything used to emit as Heading1, so `2.1` rendered ALL CAPS
                # like a major head (JL 260727).
                m = re.match(r"^(\d+(?:\.\d+)*)\s", title)
                lvl = min(3, title.split()[0].count(".") + 1) if m else 1
                # `### Appendix A · Extended Data` repeats the title already
                # emitted from the page's `#` line: the PDF printed two
                # sections, "Extended Data" then "Appendix A · Extended Data"
                # (JL 261113, NMI ScalingGlucose). Print it once.
                same = re.sub(r"^Appendix\s+[A-Z]\s*·\s*", "", title).strip()
                if lvl == 1 and page_title and not own_h1 and same == page_title \
                        and blocks and blocks[0] == ("h", 1, page_title):
                    prev_was_para = False
                    continue
                blocks.append(("h", lvl, title))
            prev_was_para = False
            continue
        if skipping:
            continue
        if insight and re.match(r"^#### \d+(?:\.\d+)+\s", s):
            title = s[5:].strip()
            blocks.append(("h", min(3, title.split()[0].count(".") + 1), title))
            prev_was_para = False
            continue
        if insight and s.startswith("|"):
            if re.match(r"^\|?\s*:?-{2,}", s):
                continue                                  # the header rule
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if blocks and blocks[-1][0] == "table":
                blocks[-1][1].append(cells)
            else:
                blocks.append(("table", [cells]))
            prev_was_para = False
            continue
        if s.startswith("#### "):
            # the paragraph job line is SCAFFOLDING, not manuscript. But the
            # heading itself IS the paragraph boundary, and nothing downstream
            # could see that before, so joining had nowhere to break.
            blocks.append(("pbreak",))
            label = abstract_label(s[5:]) if abstract else None
            if label:
                blocks.append(("label", label))
            prev_was_para = False
            continue
        if not s:
            prev_was_para = False
            continue
        if s.startswith(">"):
            m = re.match(r">\s*([A-Za-z]+)\s*:\s*(.*)$", s)
            if not m:
                continue
            kind, body = m.group(1), m.group(2)
            if kind in WORKING_LANES:
                blocks.append(("skipped-lane", kind))
                continue
            if kind in DISCUSSION_LANES or kind not in EVIDENCE_LANES:
                continue
            owner = blocks[-1] if blocks else None
            if owner and owner[0] == "table" and len(blocks) > 1 and blocks[-2][0] == "p":
                owner = blocks[-2]                       # a Bullet's table: the lane is its sentence's
            if owner and owner[0] == "p":
                owner[3].append((kind, body))
            continue
        # A PIPE ROW IS NEVER PROSE, and a numbered list item is not a manuscript
        # sentence. Both were gated on `not prev_was_para`, so one following a
        # real sentence leaked into the export: §5 shipped a `| Variable |
        # Definition |` row and §7 shipped `1. Word budget (blueprint gap)…`
        # from its questions block (JL found the § inside them, 2026-07-27).
        if s.startswith("|") or re.match(r"^\d+\.\s", s):
            continue
        if s.startswith(("(", "-", "*", "`")) and not prev_was_para:
            # a preview line under a heading, or a bullet: not prose
            if s.startswith("("):
                continue
        blocks.append(["p", s, None, []])
        prev_was_para = True
    return blocks, fenced
