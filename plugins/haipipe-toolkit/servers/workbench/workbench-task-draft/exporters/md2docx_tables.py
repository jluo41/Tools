"""Reading a LaTeX table: its body, rows, cells and column alignment."""

import os, re
from md2docx_inputs import detex

# --------------------------------------------------------------- table parse

def _braced_arg(text, pos):
    """Return (content, next_pos) for one balanced braced argument."""
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != "{":
        return None, pos
    start, depth, pos = pos + 1, 1, pos + 1
    while pos < len(text) and depth:
        depth += (text[pos] == "{") - (text[pos] == "}")
        pos += 1
    return (text[start:pos - 1], pos) if depth == 0 else (None, pos)


def _environment_body(raw):
    """Extract tabular or tabularx with balanced width/column arguments."""
    for env, nargs in (("tabularx", 2), ("tabular", 1)):
        token = "\\begin{%s}" % env
        start = raw.find(token)
        if start < 0:
            continue
        pos, args = start + len(token), []
        # tabular may carry a vertical-position option before its column spec.
        while pos < len(raw) and raw[pos].isspace():
            pos += 1
        if pos < len(raw) and raw[pos] == "[":
            close = raw.find("]", pos + 1)
            pos = close + 1 if close >= 0 else pos
        for _ in range(nargs):
            arg, pos = _braced_arg(raw, pos)
            if arg is None:
                break
            args.append(arg)
        if len(args) != nargs:
            continue
        end = raw.find("\\end{%s}" % env, pos)
        if end >= 0:
            return args[-1], raw[pos:end]
    return "", raw


def _command_args(text, command, count):
    """Parse balanced braced arguments when a table cell is one TeX command."""
    if not text.startswith(command):
        return None
    pos, args = len(command), []
    for _ in range(count):
        arg, pos = _braced_arg(text, pos)
        if arg is None:
            return None
        args.append(arg)
    return args if not text[pos:].strip() else None

def parse_table_body(path):
    """A booktabs tabular body into rows of (text, bold, gridspan).

    Measured on the six MISQ table units: toprule/midrule/bottomrule,
    \\multicolumn and \\textbf appear; \\multirow does not, which is the one
    that would have needed a vertical merge."""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as handle:
        raw = handle.read()
    raw = re.sub(r"(?m)^\s*%.*$", "", raw)                       # comments
    # Take ONLY the tabular body. The first version fed the whole file to the
    # cell splitter, so \renewcommand{\arraystretch}{1.15} and the column spec
    # survived detex as the literal "1.15 tabularl r r r" glued to the front of
    # the first cell, which also stopped \multicolumn from matching at ^.
    align, body = _environment_body(raw)
    if body is not raw:
        raw = body
    else:
        raw = re.sub(r"\\renewcommand\s*\{[^}]*\}\s*\{[^}]*\}", "", raw)
    raw = re.sub(r"\\(?:top|mid|bottom)rule\b", "", raw)
    raw = re.sub(r"\\cmidrule\s*(\([^)]*\))?\s*\{[^}]*\}", "", raw)
    raw = re.sub(r"\\addlinespace(?:\[[^\]]*\])?", "", raw)
    raw = re.sub(r"\\(?:noalign|centering|small|footnotesize)\b", "", raw)
    rows = []
    # `\\` is both a tabular row terminator and a line break inside commands
    # such as `\shortstack{(1)\\Basic}`. Splitting the raw string first made
    # Word's Table 2 header become six one-cell rows. Respect TeX brace depth:
    # only a top-level `\\` ends a row; an inner one is ordinary text and is
    # later rendered as a space by `detex`.
    for line in _split_table_rows(raw):
        line = re.sub(r"^\s*\[[0-9.]+\s*[a-z]*\]", "", line.strip())   # \\[2pt]
        line = line.replace("$", "")                                    # math mode
        line = line.strip()
        if not line:
            continue
        cells = []
        for cell in split_cells(line):
            span, text, bold = 1, cell.strip(), False
            multi = _command_args(text, r"\multicolumn", 3)
            if multi:
                span, text = int(multi[0]), multi[2]
            if "\\textbf" in text:
                bold = True
            cells.append((detex(text), bold, span))
        if any(c[0] for c in cells):
            rows.append(cells)
    return (rows, align) if rows else None


def split_cells(line):
    """Split on & that is not escaped."""
    out, buf, i = [], "", 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line):
            buf += line[i:i + 2]
            i += 2
            continue
        if line[i] == "&":
            out.append(buf)
            buf = ""
            i += 1
            continue
        buf += line[i]
        i += 1
    out.append(buf)
    return out


def _alignment_columns(spec):
    """Read effective left/centre/right alignment from a LaTeX preamble.

    Table units commonly use ``>{\\raggedright}p{...}`` and repeated
    ``*{6}{>{\\centering}X}`` columns. Taking every ``l``, ``c`` and ``r``
    character from the raw preamble accidentally treated letters in commands
    such as ``\\raggedright`` as column declarations, which centred the first
    label column in Word. This small parser expands repeats and skips modifiers.
    """
    columns, pending, i = [], None, 0

    while i < len(spec):
        if spec[i] in "><":
            arg, end = _braced_arg(spec, i + 1)
            if arg is not None:
                if "\\raggedright" in arg:
                    pending = "l"
                elif "\\centering" in arg:
                    pending = "c"
                elif "\\raggedleft" in arg:
                    pending = "r"
                i = end
                continue
        if spec[i] == "*":
            count, pos = _braced_arg(spec, i + 1)
            inner, end = _braced_arg(spec, pos) if count is not None else (None, pos)
            if count is not None and inner is not None:
                try:
                    columns.extend(_alignment_columns(inner) * int(count))
                except ValueError:
                    pass
                i = end
                pending = None
                continue
        if spec[i] in "lcr":
            columns.append(pending or spec[i])
            pending = None
            i += 1
            continue
        if spec[i] in "pmbX":
            columns.append(pending or ("c" if spec[i] == "X" else "l"))
            pending = None
            i += 1
            if spec[i - 1] in "pmb" and i < len(spec) and spec[i] == "{":
                _width, i = _braced_arg(spec, i)
            continue
        i += 1
    return columns


def _split_table_rows(raw):
    """Split tabular content on top-level TeX row breaks only."""
    rows, buf, depth, i = [], [], 0, 0
    while i < len(raw):
        ch = raw[i]
        if ch == "{":
            depth += 1
            buf.append(ch)
            i += 1
            continue
        if ch == "}":
            depth = max(0, depth - 1)
            buf.append(ch)
            i += 1
            continue
        if ch == "\\" and i + 1 < len(raw) and raw[i + 1] == "\\":
            if depth == 0:
                rows.append("".join(buf))
                buf = []
            else:
                buf.extend((ch, raw[i + 1]))
            i += 2
            continue
        buf.append(ch)
        i += 1
    if buf:
        rows.append("".join(buf))
    return rows
