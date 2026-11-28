"""latex_table.py: a LaTeX table's rows, cells, column spans and header rows, read for Word's add_table.
Moved out of latex_parse.py (over 700 lines) when the cell math and the header count changed (261118). It runs inside
latex_room_to_docx.py's namespace like latex_parse.py (_load_part), which loads it."""
from __future__ import annotations

import re

CELL_LEFT = "\x14"     # a \\multicolumn{n}{l} cell: add_table sets it left instead of centring the merge
TABULAR_BEGIN = re.compile(r"\\begin\{(tabularx|tabular\*|tabular|longtable|array)\}")


def _split_depth0(text: str, sep: str) -> list[str]:
    """split on ``sep`` only at brace depth 0 and not escaped; ``sep`` is "\\\\" or "&"."""
    parts, depth, cur, i = [], 0, [], 0
    while i < len(text):
        ch = text[i]
        esc = i > 0 and text[i - 1] == "\\"
        if ch == "{" and not esc: depth += 1
        elif ch == "}" and not esc: depth -= 1
        if depth == 0 and text.startswith(sep, i) and not esc:
            parts.append("".join(cur)); cur = []; i += len(sep)
            if sep == "\\\\":                                   # optional [skip] after a row break
                m = re.match(r"\s*\[[^\]]*\]", text[i:])
                if m: i += m.end()
            continue
        cur.append(ch); i += 1
    parts.append("".join(cur))
    return parts


def _expand_cell(cell: str) -> list[str]:
    """one LaTeX cell -> its text, padded with empties for a \\multicolumn span."""
    span, left = 1, False
    m = re.match(r"\s*\\multicolumn\s*\{\s*(\d+)\s*\}", cell)
    if m:
        span = int(m.group(1))
        g1 = parse_group_at(cell, m.end())          # the column spec
        g2 = parse_group_at(cell, g1[1]) if g1 else None
        cell = g2[0] if g2 else cell
        left = bool(g1 and re.match(r"\s*(?:\|\s*)?[lp]", g1[0]))   # {l}: a panel title set left, not centred
    # \shortstack{a\\b} stacks lines inside ONE cell; keep it one cell
    while True:
        m2 = re.search(r"\\shortstack(?:\[[^\]]*\])?", cell)
        if not m2: break
        g = parse_group_at(cell, m2.end())
        if not g: break
        cell = cell[:m2.start()] + g[0].replace("\\\\", " ") + cell[g[1]:]
    cell = LAYOUT_ASSIGNMENT.sub("", cell)
    indent = re.match(r"\s*\\hspace\*?\s*\{\s*([\d.]+)\s*em\s*\}", cell)
    # mark_emphasis keeps \\textbf and \\textit as marks (and raises \\textsuperscript): a panel title printed plain
    # and an italic column name upright in Word (ScalingGlucose ED Table 5, 261118)
    text = true_minus(latex_to_text(mark_emphasis(math_scripts_raised(cell))).strip())
    if indent and text:
        text = INDENT_MARK * max(1, round(float(indent.group(1)))) + text
    if left and text:
        text = CELL_LEFT + text
    return [text] + [""] * (span - 1)


def parse_table_rows(block: str) -> list[list[str]]:
    r"""Rows of the first tabular-like environment in ``block``.

    0.7.1: brace-aware. The old regex read the column spec as ``\{[^{}]*\}`` and so
    returned NO rows for any spec with nested braces (``p{3cm}``, ``@{}``,
    ``>{\\raggedright\\arraybackslash}``, ``*{6}{X}``), which is most real
    tables; Word then got the caption with nothing under it. Rows also split on
    ``\\\\`` only at depth 0, so ``\\shortstack{a\\\\b}`` stays one cell, and a
    ``\\multicolumn{n}`` cell pads ``n-1`` empties so columns line up.
    """
    m = TABULAR_BEGIN.search(block)
    if m is None:
        return []
    env = m.group(1)
    pos = m.end()
    opt = re.match(r"\s*\[[^\]]*\]", block[pos:])            # [t] / [h] position
    if opt: pos += opt.end()
    if env in ("tabularx", "tabular*"):                          # width argument first
        g = parse_group_at(block, pos)
        if g is None: return []
        pos = g[1]
    g = parse_group_at(block, pos)                               # the column spec, braces and all
    if g is None: return []
    pos = g[1]
    end = re.compile(r"\\end\{" + re.escape(env) + r"\}").search(block, pos)
    body = block[pos:end.start()] if end else block[pos:]
    body = re.sub(
        r"\\(?:toprule|midrule|bottomrule|hline|addlinespace(?:\[[^\]]*\])?|cline\{[^}]*\}|cmidrule(?:\([^)]*\))?\{[^}]*\})",
        "", body,
    )
    rows, _spans = _rows_and_spans(body)
    return rows


def _rows_and_spans(body: str) -> tuple[list[list[str]], list[list[int]]]:
    """Cell texts and, aligned with them, each cell's column span: a \\multicolumn{n}
    start cell carries n, the n-1 cells it covers carry 0, every other cell 1."""
    rows: list[list[str]] = []
    spans: list[list[int]] = []
    for raw in _split_depth0(body, "\\\\"):
        raw = raw.strip()
        if not raw or re.fullmatch(r"(?:\\\w+\s*)+", raw):    # rule-only leftovers
            continue
        cells: list[str] = []
        row_spans: list[int] = []
        for cell in _split_depth0(raw, "&"):
            expanded = _expand_cell(cell)
            cells.extend(expanded)
            row_spans.extend([len(expanded)] + [0] * (len(expanded) - 1))
        if any(cells):
            rows.append(cells)
            spans.append(row_spans)
    width = max((len(row) for row in rows), default=0)
    return ([row + [""] * (width - len(row)) for row in rows],
            [s + [1] * (width - len(s)) for s in spans])


_RULES = re.compile(
    r"\\(?:toprule|midrule|bottomrule|hline|addlinespace(?:\[[^\]]*\])?|cline\{[^}]*\}|cmidrule(?:\([^)]*\))?\{[^}]*\})")


def _tabular_raw_body(block: str) -> str | None:
    """The first tabular-like environment's body, rules still in place."""
    m = TABULAR_BEGIN.search(block)
    if m is None:
        return None
    env, pos = m.group(1), m.end()
    opt = re.match(r"\s*\[[^\]]*\]", block[pos:])
    if opt: pos += opt.end()
    if env in ("tabularx", "tabular*"):
        g = parse_group_at(block, pos)
        if g is None: return None
        pos = g[1]
    g = parse_group_at(block, pos)
    if g is None: return None
    pos = g[1]
    end = re.compile(r"\\end\{" + re.escape(env) + r"\}").search(block, pos)
    return block[pos:end.start()] if end else block[pos:]


def math_scripts_raised(cell: str) -> str:
    """Inline math in a table cell: its ^{...} and ^x become \\textsuperscript, so Word raises them. A cell is plain
    runs, not an equation, and latex_to_text dropped the caret: "$L = E + A N^{-\\alpha}$" printed "A N-α"
    (JL 261118, ED Table 2 in Word)."""
    def raise_in(m: re.Match) -> str:
        body = re.sub(r"\^\{([^{}]*)\}", r"\\textsuperscript{\1}", m.group(1))
        body = re.sub(r"\^(\\[A-Za-z]+|[^\s{\\])", r"\\textsuperscript{\1}", body)
        return "$" + body + "$"
    return re.sub(r"(?<!\\)\$([^$]+?)\$", raise_in, cell)


def parse_table_spans(block: str) -> list[list[int]]:
    """Column spans aligned with parse_table_rows(block) (0.8.4)."""
    body = _tabular_raw_body(block)
    return [] if body is None else _rows_and_spans(_RULES.sub("", body))[1]


def count_header_rows(block: str) -> int:
    """Rows above the first \\midrule: the table's header, repeated on every page in Word (0.8.4).
    Before, only row 0 repeated, so a continued table showed "Section 3 classification" and
    lost its column names (JL 260928 screenshot)."""
    body = _tabular_raw_body(block)
    if body is None:
        return 1
    mid = re.search(r"\\midrule|\\hline", body)
    if mid is None:
        return 1
    head_rows, _ = _rows_and_spans(_RULES.sub("", body[:mid.start()]))
    # a table whose first \midrule closes a whole panel (a panel title, its column names, its data rows) has no
    # real header above it: bolding those rows set every data row of ED Table 2's top panel bold (JL 261118 "how do
    # you think the display of the word?"). A header is at most 3 rows; more means a panel, so only row 0 is the head.
    return 1 if len(head_rows) > 3 else max(1, len(head_rows))
